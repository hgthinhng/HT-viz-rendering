#!/usr/bin/env python3
"""
Kiem tra nhat quan so lieu giua 2 exhibit cua CUNG mot mo hinh DCF trong 1 file
HTML bao cao: football field (dai gia tri) va luoi do nhay 2 chieu WACC x g.

Doc research/12-cross-exhibit/CONSISTENCY-CHECK.md truoc khi dung file nay -
no giai thich quy uoc data-* va khi nao mot "khac biet" giua 2 exhibit la HOP
LE (vi du dai khuyen nghi hep hon la mot TAP CON co chu y cua luoi stress-test
day du), chu khong phai loi tu mau thuan can sua.

Dung:
    python3 check_cross_exhibit.py <file1.html> [file2.html ...]

Exit code: 0 neu TAT CA file PASS, 1 neu bat ky file nao FAIL hoac thieu du
lieu can de doi chieu (thieu du lieu KHONG duoc coi la PASS im lang).

Co che: file HTML phai nhung dung 1 khoi
    <script type="application/json" class="dcf-assumptions">{...}</script>
la NGUON DUY NHAT cua cac tham so mo hinh (fcff chuan hoa, no rong, so co
phieu luu hanh). Script tu tinh lai EV va gia/co phieu tu cong thuc Gordon
growth 1 giai doan cho TUNG o luoi (doc tu thuoc tinh data-wacc/data-g/
data-ev/data-price cua cac phan tu class="grid-cell"), roi doi chieu voi
dai DCF tren football field (doc tu phan tu class="ff-band-dcf", thuoc tinh
data-method/data-price-min/data-price-max). Neu so ghi tren hinh lech so
tinh lai qua nguong dung sai lam tron hien thi, bao FAIL kem so lieu cu the.
"""
import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Dung sai cho phep: bang 1 don vi lam tron hien thi cuoi (1 chu so thap phan
# cho gia/co phieu, do -> 0.05; EV hien thi cung 1 chu so thap phan tren don
# vi ty dong lon hon nhieu nen cho dung sai rong hon mot chut).
TOL_PRICE = 0.05   # nghin dong / co phieu
TOL_EV = 0.2       # ty dong


def compute(fcff_ty, net_debt_ty, shares_trieu, wacc_pct, g_pct):
    """Gordon growth 1 giai doan: EV = FCFF / (WACC - g). Tra ve (EV, von chu
    so huu, gia/co phieu) deu theo don vi da ghi trong khoi assumptions."""
    spread = (wacc_pct - g_pct) / 100.0
    if spread <= 0:
        raise ValueError(f"WACC ({wacc_pct}%) phai lon hon g ({g_pct}%), spread={spread:.4f}")
    ev = fcff_ty / spread
    equity = ev - net_debt_ty
    price = equity / shares_trieu
    return ev, equity, price


def close(a, b, tol):
    return abs(a - b) <= tol


def check_file(path):
    html = Path(path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    problems = []

    assum_tag = soup.find("script", attrs={"type": "application/json", "class": "dcf-assumptions"})
    if assum_tag is None or not assum_tag.string:
        return False, ["KHONG tim thay khoi nguon-mot-noi <script type=application/json "
                        "class=dcf-assumptions>: khong co gi de doi chieu, tu dong FAIL."]
    try:
        assum = json.loads(assum_tag.string)
        fcff = float(assum["fcff_chuan_hoa_ty"])
        net_debt = float(assum["no_rong_ty"])
        shares_m = float(assum["co_phieu_luu_hanh_trieu"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        return False, [f"Khoi dcf-assumptions khong doc duoc hoac thieu truong bat buoc: {e}"]

    # --- 1. doi chieu tung o luoi do nhay voi cong thuc tinh lai ---
    cells = soup.select(".grid-cell")
    if not cells:
        problems.append("KHONG tim thay o luoi nao (class=grid-cell): khong kiem duoc luoi do nhay.")
    grid_prices = []
    for c in cells:
        try:
            w = float(c["data-wacc"])
            g = float(c["data-g"])
            ev_d = float(c["data-ev"])
            price_d = float(c["data-price"])
        except (KeyError, ValueError) as e:
            problems.append(f"O luoi thieu/hong thuoc tinh data-wacc/data-g/data-ev/data-price: {e}")
            continue
        try:
            ev_c, _eq_c, price_c = compute(fcff, net_debt, shares_m, w, g)
        except ValueError as e:
            problems.append(f"O WACC={w}% g={g}%: {e}")
            continue
        grid_prices.append(price_c)
        if not close(ev_d, ev_c, TOL_EV):
            problems.append(
                f"O WACC={w}% g={g}%: EV ghi tren hinh {ev_d} nhung tinh lai tu assumptions ra "
                f"{ev_c:.2f} (lech {abs(ev_d - ev_c):.2f} ty dong)"
            )
        if not close(price_d, price_c, TOL_PRICE):
            problems.append(
                f"O WACC={w}% g={g}%: gia ghi tren hinh {price_d} nhung tinh lai {price_c:.4f} "
                f"(lech {abs(price_d - price_c):.4f} nghin dong/cp)"
            )

    if not grid_prices:
        return False, problems or ["Luoi rong, khong co gia tri nao doi chieu duoc."]

    grid_min, grid_max = min(grid_prices), max(grid_prices)

    # --- 2. doi chieu dai DCF tren football field voi luoi vua tinh lai ---
    ff = soup.select_one(".ff-band-dcf")
    if ff is None:
        problems.append("KHONG tim thay dai DCF tren football field (class=ff-band-dcf).")
    else:
        method = ff.get("data-method", "")
        try:
            p_min = float(ff["data-price-min"])
            p_max = float(ff["data-price-max"])
        except (KeyError, ValueError) as e:
            problems.append(f"Dai DCF thieu/hong data-price-min hoac data-price-max: {e}")
            p_min = p_max = None

        if p_min is not None:
            if method == "grid-full-range":
                # Doc duoc TOAN BO luoi: dai phai bang dung MIN/MAX cua luoi.
                if not close(p_min, grid_min, TOL_PRICE):
                    problems.append(
                        f"Dai DCF ghi min={p_min} nhung MIN thuc cua luoi la {grid_min:.4f} "
                        f"(lech {abs(p_min - grid_min):.4f}) -- day la LOI MAU THUAN, khong phai lam tron."
                    )
                if not close(p_max, grid_max, TOL_PRICE):
                    problems.append(
                        f"Dai DCF ghi max={p_max} nhung MAX thuc cua luoi la {grid_max:.4f} "
                        f"(lech {abs(p_max - grid_max):.4f}) -- day la LOI MAU THUAN, khong phai lam tron."
                    )
            elif method == "house-view-subset":
                # Dai hep hon co chu y: chi lay 2 diem WACC (g co dinh o base),
                # phai KHOP dung 2 diem do VA phai NAM TRONG luoi day du.
                try:
                    w_lo = float(ff["data-wacc-min"])
                    w_hi = float(ff["data-wacc-max"])
                    g_fix = float(ff["data-g-fixed"])
                except (KeyError, ValueError) as e:
                    problems.append(f"method=house-view-subset nhung thieu data-wacc-min/max hoac data-g-fixed: {e}")
                else:
                    _, _, p_at_lo = compute(fcff, net_debt, shares_m, w_lo, g_fix)
                    _, _, p_at_hi = compute(fcff, net_debt, shares_m, w_hi, g_fix)
                    sub_min, sub_max = min(p_at_lo, p_at_hi), max(p_at_lo, p_at_hi)
                    if not close(p_min, sub_min, TOL_PRICE) or not close(p_max, sub_max, TOL_PRICE):
                        problems.append(
                            f"Dai DCF (house-view-subset) ghi {p_min}-{p_max} nhung tinh lai tu "
                            f"WACC {w_lo}%/{w_hi}% (g co dinh {g_fix}%) ra {sub_min:.4f}-{sub_max:.4f}"
                        )
                    pad = TOL_PRICE
                    if not (grid_min - pad <= p_min <= grid_max + pad and grid_min - pad <= p_max <= grid_max + pad):
                        problems.append(
                            f"Dai house-view {p_min}-{p_max} NAM NGOAI luoi day du {grid_min:.2f}-{grid_max:.2f}: "
                            f"day khong con la mot TAP CON hop le, phai coi la mau thuan that."
                        )
            else:
                problems.append(
                    f"data-method='{method}' khong nhan dien duoc "
                    f"(chi ho tro 'grid-full-range' hoac 'house-view-subset')."
                )

    ok = not problems
    return ok, problems


def main(argv):
    if len(argv) < 2:
        print(f"Dung: python3 {argv[0]} <file1.html> [file2.html ...]")
        return 2
    overall_ok = True
    for path in argv[1:]:
        ok, problems = check_file(path)
        overall_ok = overall_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {path}")
        for p in problems:
            print(f"    - {p}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
