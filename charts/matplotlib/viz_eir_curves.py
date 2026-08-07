#!/usr/bin/env python3
"""viz_eir_curves.py, duong cong lai suat va duong cong gia ky han (matplotlib, tinh).

Theo dac ta docs/specs/2026-08-07-yield-forward-curve-design.md. Cung khuon 5 module EIR
hien co (kicker/tieu de serif/subtitle/source line, cung hop dong spec.json), them 2
component:

  yield_curve    -> c_yield_curve    duong cong loi suat, toi da 3 thoi diem chong nhau
  futures_curve  -> c_futures_curve  duong cong gia ky han, tham chieu spot,
                                      badge contango/backwardation

Ba quyet dinh da chot trong dac ta, khong mo lai o day:
  - Truc ky han la TRUC HANG MUC (category, cach deu), khong tuyen tinh theo nam, khong
    log (muc 1). Vi vay KHONG duoc doc do doc tren chart nhu bps/nam.
  - Noi THANG giua cac diem ky han, KHONG spline (spline qua diem roi rac la bia du lieu
    o khoang giua).
  - Truc gia tri (truc y) KHONG bat dau tu 0, tu co theo du lieu.

Day la module matplotlib DAU TIEN dung schema.py (validate_series/validate_row/cach_ve/
so_thap_phan/nhan_don_vi/co_co). Ky han thua du lieu (muc 5 cua dac ta) tu dat ten rieng
"quan_sat"/"uoc_tinh"/"bo han diem" TRUOC KHI schema.py ton tai; o day anh xa lai sang
dung tu vung schema thay vi dung mot he ten thu hai:
  - do TIN CAY cua 1 diem CO gia tri (quan sat that, noi suy, hay uoc tinh dealer) ->
    VOCAB["do_tin_cay"] ("quan_sat"/"noi_suy"/"uoc_tinh") o cap TUNG DIEM. Day la truong
    RIENG, khac han `source.tier` von la bac cua ca series. Ban dau module nay tai dung
    `source_tier` o cap diem vi chua co truong rieng, va cach do roi: doc mot diem thi
    khong biet no dang noi ve nguon cua ca duong hay ve chinh no. Spec cu con dat `tier`
    o cap diem van chay duoc, `_tu_tier_cu()` quy ve tu vung moi ngay tai cua vao.
  - do CO/KHONG CO gia tri (mot ky han hoan toan khong xuat hien cho 1 snapshot) -> dung
    dung `status` cua schema (co_that/chua_cong_bo/khong_ton_tai/loai_bat_thuong) qua
    `cach_ve()`, khong bia trang thai moi.

Usage:
  python3 viz_eir_curves.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_eir_curves.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _eir_style as S
from _eir_style import (
    PAPER, ON_INK, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge, tint,
)
from schema import ERR, LoiSchema, VOCAB, cach_ve, co_co, nhan_don_vi, so_thap_phan, validate_row, validate_series
import matplotlib.pyplot as plt

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved


# Anh xa tuong thich nguoc: spec cu dat `tier` o cap DIEM voi tu vung `source_tier`, vi
# luc do chua co truong rieng cho do tin cay cua tung diem. Giu duong doc do lai de spec
# da viet khong gay, nhung quy ve tu vung moi ngay tai cua vao, de phan con lai cua module
# chi con lam viec voi MOT he ten.
_TIER_CU_SANG_DO_TIN_CAY = {
    "cong-bo": "quan_sat",
    "uoc-tinh": "uoc_tinh",
    "noi-bo": "uoc_tinh",
}


def _tu_tier_cu(tier):
    """None neu khong khai. Nem LoiSchema neu khai mot gia tri khong hieu duoc."""
    if tier is None:
        return None
    if tier not in _TIER_CU_SANG_DO_TIN_CAY:
        raise LoiSchema(
            ERR.DO_TIN_CAY_LA,
            f'tier cu "{tier}" o cap diem khong anh xa duoc sang do_tin_cay. '
            f'Dung thang do_tin_cay: {", ".join(VOCAB["do_tin_cay"])}',
        )
    return _TIER_CU_SANG_DO_TIN_CAY[tier]


# --------------------------------------------------------- shared helpers (verbatim
# from viz_eir.py so a spec routed here behaves identically) -----------------------
def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


def _fmt(p, v):
    return fmt_value(v, p.get("y_format", "num"), p.get("currency", "$"), p.get("dp"))


# ============================================================= khung dung chung

# Thu tu ky han CHUAN, KHONG sort theo gia tri (quyet dinh #1.2 cua dac ta). VN gan nhu
# khong co 1M/3M/6M o TPCP thu cap co y nghia phan tich (muc 5.2) nen khong co trong danh
# sach nay; neu can hang hoa/lai suat co ky han ngan hon, ho so goi component khac.
_TENOR_ORDER = ["1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "15Y", "20Y", "30Y"]

# 3 tang tuoi cua duong (muc 2 cua dac ta): do dam net, kieu net NEN (bi de len boi
# _UNCERTAIN_DASH khi diem la nguon "uoc tinh"), va co so kich thuoc marker.
_AGE_STYLE = [
    {"lw": 2.6, "dash": "-", "marker": 8},
    {"lw": 1.8, "dash": (0, (5, 2)), "marker": 6.4},
    {"lw": 1.4, "dash": (0, (1, 2)), "marker": 5},
]
# Net dut rieng cho doan/diem co nguon "uoc tinh dealer" (khac ca 3 kieu net tuoi o tren
# de khong lan nghia); chi ap dung o tuoi "hom nay" (chi so 0) vi 2 tuoi con lai da tu
# mang net dut/cham roi, chong them mot quy uoc thu 3 se roi.
_UNCERTAIN_DASH = (0, (4, 3))


def _age_color(accent, idx):
    """Mau theo tuoi duong: hom nay = accent nguyen ban, 1 thang truoc = accent nhat 35%,
    1 nam truoc = FAINT (khong con dung accent), dung dung 3 muc da chot o muc 2."""
    if idx == 0:
        return accent
    if idx == 1:
        return tint(accent, 0.65)
    return FAINT


def _draw_curve_line(ax, xs, values, uncertain, color, lw, base_dash, marker_size,
                      hollow_all=False, zorder=3):
    """Ve 1 duong tren TRUC HANG MUC xs=0..n-1, noi THANG (khong spline), va KHONG noi
    qua bat ky vi tri nao co values[i] is None (khop dung "khong noi suy ngam" da chot o
    muc 1.2/4.1/5 cua dac ta: chi noi 2 diem that su LIEN KE nhau tren truc).

    uncertain[i]: True neu diem la nguon "uoc tinh dealer" (tier != cong-bo) -> marker
    RONG va doan cham vao no doi sang net dut rieng. hollow_all ep TOAN BO marker rong
    (dung cho tuoi "1 nam truoc": rong vi ca 2 ly do tuoi lan do tin cay, khong can chong
    them ky hieu - dung nhu muc 2 cua dac ta mo ta).

    Tra ve danh sach (chi_so, gia_tri) cac diem THAT SU duoc ve, de ham goi tiep dung cho
    nhan cuoi duong / danh dau doan dao nguoc.
    """
    pts = [(i, v) for i, v in enumerate(values) if v is not None]
    idx_that = {i for i, _ in pts}
    for i in range(len(pts) - 1):
        i0, v0 = pts[i]; i1, v1 = pts[i + 1]
        if i1 - i0 != 1:
            continue  # co khoang trong (ky han bi loai/chua ton tai) -> KHONG noi qua
        dash = _UNCERTAIN_DASH if (uncertain[i0] or uncertain[i1]) else base_dash
        ax.plot([xs[i0], xs[i1]], [v0, v1], color=color, lw=lw, linestyle=dash,
                zorder=zorder, solid_capstyle="round")
    for i, v in pts:
        hollow = hollow_all or uncertain[i]
        ax.plot(xs[i], v, marker="o", markersize=marker_size,
                markerfacecolor=(PAPER if hollow else color), markeredgecolor=color,
                markeredgewidth=1.6, linestyle="none", zorder=zorder + 1)
    del idx_that
    return pts


def _badge_at_data(ax, fig, xd, yd, text, ha="center", bg=NAVY, fg=ON_INK, dy=0.045):
    """`_badge()` lam viec theo toa do AXES-FRACTION khi truyen ax= (xem c_lorenz trong
    viz_eir.py), nhung badge dao nguoc/contango o day phai neo vao 1 VI TRI TREN DUONG
    CONG (toa do du lieu), khong phai 1 goc co dinh cua khung hinh. Doi toa do bang chinh
    transData/transAxes hien hanh cua ax, nen PHAI goi SAU KHI da chot xlim/ylim."""
    xf, yf = ax.transAxes.inverted().transform(ax.transData.transform((xd, yd)))
    return _badge(fig, xf, min(yf + dy, 0.97), text, ha=ha, bg=bg, fg=fg, ax=ax)


def _clear_y(all_values_by_snapshot, i0, i1):
    """Gia tri Y CAO NHAT ma BAT KY duong nao (moi snapshot) di qua trong pham vi cot
    [i0, i1] (bao gom ca cac cot o giua neu doan trai dai qua nhieu ky han, vd 2Y-10Y).
    Dung de dat badge dao nguoc/2s10s O TREN toan bo vung do, thay vi o trung diem doan -
    trung diem doan de badge de len chinh cac duong khac dang chay ngang qua do (da thay
    that trong 1 lan render thu nghiem: 3 duong chong nhau lam badge khong doc duoc)."""
    lo, hi = min(i0, i1), max(i0, i1)
    vals = [v for arr in all_values_by_snapshot for v in arr[lo:hi + 1] if v is not None]
    return max(vals) if vals else None


def _draw_axis_marks(ax, xs, marks):
    """Danh dau tren TRUC cho 2 trong 3 trang thai thieu cua schema (muc 5 dac ta +
    CLAUDE.md "loai_bat_thuong ngat va danh dau tren truc de biet la BI LOAI chu khong
    phai THIEU"). Chu Y: chi ap dung cho status DUOC TAC GIA GAN TUONG MINH
    (chua_cong_bo/loai_bat_thuong); truong hop pho bien hon - 1 ky han hoan toan khong
    xuat hien trong points cua 1 snapshot - la khong_ton_tai NGAM DINH, cach_ve() cua no
    tra ve danh_dau_truc=None (khong ve gi, dung nhu "bo han diem, khong chua cho" o muc
    5.2), nen se KHONG lot vao dict `marks` nay.

    Dung 2 ky hieu ASCII (khong dung glyph Unicode nhu ✕) vi _badge()/annotate mac dinh
    render bang SANS, va _delta_arrow() trong viz_eir_kpi.py da ghi ro mui ten ▲▼ chi
    duoc XAC NHAN an toan trong MONO, khong phai SANS - repo nay tung lot glyph thieu 4
    lan trong Phase 1 (CLAUDE.md), nen khong danh cuoc them mot glyph chua kiem chung.
    """
    for i, mark in marks.items():
        glyph = "X" if mark == "da_loai" else "..."
        ax.annotate(glyph, (xs[i], 0), xycoords=("data", "axes fraction"),
                    textcoords="offset points", xytext=(0, -20), ha="center", va="top",
                    fontsize=9, color=FAINT, fontweight=("bold" if mark == "da_loai" else "normal"))


# =============================================================== 1. yield_curve
def c_yield_curve(p, accent):
    """Duong cong loi suat, toi da 3 snapshot chong nhau, truc hang muc.

    p = {
      # meta chuan EIR: kicker, title, subtitle, source, asof, rating, firm
      "unit": "phan_tram",   # phai nam trong VOCAB["unit"] (schema.vocab.json)
      "dp": 2,               # so chu so thap phan; mac dinh 2 (khong phai 1 mac dinh cua
                              # fmt_value), vi chenh 10bps giua cac ky han lien ke se bien
                              # mat o 1 chu so (muc 7.2 cua dac ta)
      "snapshots": [         # toi da 3, qua 3 dung small_multiples (07-small-multiples.mjs)
        {
          "name": "Hôm nay (07/08/2026)",
          "source_tier": "cong-bo",   # tuy chon, cap SERIES, mac dinh "cong-bo"
          "points": [
            {"tenor": "1Y", "value": 2.85, "tier": "uoc-tinh"},   # tier cap DIEM: do tin
                                                                    # cay nguon cua RIENG
                                                                    # diem nay (muc 5.2:
                                                                    # 1Y/2Y luon thanh
                                                                    # khoan thap)
            {"tenor": "3Y", "value": 3.05, "tier": "cong-bo"},
            {"tenor": "30Y", "value": None, "status": "khong_ton_tai"},  # VN chua phat
                                                                           # hanh ky han
                                                                           # nay o thoi
                                                                           # diem do
          ],
        },
        ...
      ],
      "inversions": [{"from": "2Y", "to": "10Y", "bps": -18}],  # TUY CHON, bo sung cho
          # phat hien tu dong (xem docstring duoi), khong thay the no
      "butterfly": {"wings": ["2Y", "10Y"], "belly": "5Y"},      # TUY CHON, day cung
    }

    Moi diem: mac dinh status="co_that" (co gia tri). Khi status khac "co_that" (
    "chua_cong_bo"/"khong_ton_tai"/"loai_bat_thuong"), value PHAI la None/vang mat -
    validate_series() se nem LoiSchema neu vi pham (VALUE_PHAI_NULL). Khi 1 ky han khong
    xuat hien trong points cua 1 snapshot, ham nay TU coi la status="khong_ton_tai" cho
    RIENG snapshot do (bo diem, khong noi suy ngam, dung quy tac muc 1.2/5.2).

    Dao nguoc (muc 3.1): TU DONG phat hien tren duong "hom nay" (snapshot dau tien theo
    thu tu, xac dinh bang co_co()) - lap qua tung CAP DIEM LIEN KE tren truc, neu gia tri
    giam thi to doan do BRICK + gan badge bps. Neu p["inversions"] duoc cung cap them, moi
    muc la mot NHAN THU CONG bo sung (vi du 2s10s kinh dien khi 2 dau khong lien ke nhau
    tren truc do co ky han khac chen giua) - khong thay the phat hien tu dong.

    Trả lời: "Đường cong lợi suất đang dốc lên hay đảo ngược, và nó đã dịch thế nào
    so với kỳ trước?" Tối đa ba lớp chồng nhau cho ba thời điểm.

    Dữ liệu cần: tenors, snapshots dạng {name, points}, mỗi điểm mang value và
    do_tin_cay ở cấp điểm.

    KHÔNG dùng quá ba lớp, vì lớp thứ tư trở đi làm mất hẳn khả năng đọc chiều dịch
    chuyển. Và mọi báo cáo dùng hình này phải ghép thêm bảng số liệu, vì đọc chênh
    lệch vài điểm cơ bản trên trục không phải là phép đọc chart làm được.
    """
    unit = p.get("unit", "phan_tram")
    dp = p.get("dp", 2)
    dp_use = so_thap_phan({"unit": unit, "decimals": dp})

    snapshots = list(p["snapshots"])
    if not snapshots:
        raise ValueError("c_yield_curve: can it nhat 1 snapshot")
    if len(snapshots) > 3:
        raise ValueError(
            f"c_yield_curve: toi da 3 duong/1 chart (dang nhan {len(snapshots)}); qua 3 "
            "thoi diem chuyen sang small_multiples (07-small-multiples.mjs) theo dung "
            "muc 2 cua docs/specs/2026-08-07-yield-forward-curve-design.md"
        )
    la_dau = co_co(0, len(snapshots))  # co "day la snapshot chinh/hom nay" tinh tu CHI SO

    # --- truc hang muc = UNION cac tenor xuat hien o BAT KY snapshot nao, giu dung thu
    # tu chuan (quyet dinh #1.2, khong sort theo gia tri) ---
    lookups = [{pt["tenor"]: pt for pt in (snap.get("points") or [])} for snap in snapshots]
    cats = [t for t in _TENOR_ORDER if any(t in lk for lk in lookups)]
    if not cats:
        raise ValueError("c_yield_curve: khong ky han nao trong snapshots khop _TENOR_ORDER")
    n = len(cats)
    xs = np.arange(n)

    fig, ax = eir_fig(_meta(p, accent), figsize=(8.6, 5.1), rect=(0.095, 0.225, 0.705, 0.535))
    despine(ax, keep=("left", "bottom"), grid_axis="y")

    axis_marks = {}           # chi_so tren truc -> "chua_cong_bo" | "da_loai"
    end_labels = []           # [x, y, ten, mau, la_snapshot_chinh]
    any_uncertain = False
    primary_values = None     # gia tri cua snapshot chinh, dung cho dao nguoc/butterfly
    all_values_by_snapshot = []  # de tinh vi tri Y "khong duong nao di qua" cho badge

    for si, (snap, lk) in enumerate(zip(snapshots, lookups)):
        source_tier = snap.get("source_tier", "cong-bo")
        rows = []
        values = [None] * n
        uncertain = [False] * n
        for i, tenor in enumerate(cats):
            pt = lk.get(tenor)
            if pt is None:
                status, value, tier = "khong_ton_tai", None, None
            else:
                status = pt.get("status", "co_that")
                value = pt.get("value")
                # `do_tin_cay` la truong RIENG o cap diem, thay cho cach cu tai dung
                # `source_tier` (von la bac cua ca series). `tier` cu van doc duoc de
                # spec cu khong gay, nhung anh xa thang sang tu vung moi.
                if status == "co_that":
                    tin_cay = pt.get("do_tin_cay") or _tu_tier_cu(pt.get("tier"))
                else:
                    tin_cay = None
            hang = {"entity": {"code": tenor}, "status": status, "value": value}
            if tin_cay is not None:
                hang["do_tin_cay"] = tin_cay
            rows.append(hang)
            if status == "co_that":
                values[i] = None if value is None else float(value)
                uncertain[i] = tin_cay != "quan_sat"
                any_uncertain = any_uncertain or uncertain[i]
            else:
                mark = cach_ve(status)["danh_dau_truc"]
                if mark and axis_marks.get(i) != "da_loai":
                    axis_marks[i] = mark

        series = {"unit": unit, "source": {"tier": source_tier}, "decimals": dp, "rows": rows}
        validate_series(series)  # fail-fast: status/value/tier sai deu no o day, TRUOC
                                  # khi ve bat ky net nao
        all_values_by_snapshot.append(values)

        style = _AGE_STYLE[min(si, 2)]
        color = _age_color(accent, si)
        pts_that = _draw_curve_line(ax, xs, values, uncertain, color, style["lw"],
                                     style["dash"], style["marker"],
                                     hollow_all=(si == 2), zorder=4 - min(si, 2))
        if la_dau(si):
            primary_values = values
        if pts_that:
            li, lv = pts_that[-1]
            end_labels.append([xs[li], lv, snap.get("name", ""), color, la_dau(si)])

    ax.set_xticks(xs); ax.set_xticklabels(cats, fontsize=9.5, color=INK)
    ax.set_xlim(-0.5, n - 0.5)
    ax.margins(y=0.16)  # KHONG set_ylim(bottom=0): truc gia tri tu co theo du lieu (#1.2)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.{dp_use}f}%"))
    if unit in VOCAB["unit"]:
        ax.set_ylabel(nhan_don_vi(unit), fontsize=9, color=MUTED)

    _draw_axis_marks(ax, xs, axis_marks)

    # nhan cuoi duong, lech doc nhe neu 2 duong ket thuc qua gan nhau (goi y o muc 2)
    end_labels.sort(key=lambda r: r[1])
    ylo, yhi = ax.get_ylim(); min_gap = (yhi - ylo) * 0.075
    for k in range(1, len(end_labels)):
        if end_labels[k][1] - end_labels[k - 1][1] < min_gap:
            end_labels[k][1] = end_labels[k - 1][1] + min_gap
    for xe, ye, text, color, bold in end_labels:
        if not text:
            continue
        ax.annotate(" " + text, (xe, ye), color=color, fontsize=8.8,
                    fontweight="bold" if bold else "normal", va="center", ha="left",
                    xytext=(6, 0), textcoords="offset points")

    # --- dao nguoc (muc 3.1): CHI coi la dao nguoc khi gia tri THAT SU giam (v1 < v0),
    # ke ca voi cap "from/to" nguoi dung tu cung cap trong p["inversions"] - neu khong,
    # se ve mot doan BRICK + nhan "DAO NGUOC" cho mot doan dang TANG, tuc bia bang chung.
    # Vi tri badge KHONG dat o trung diem doan (da thay that: bi 2-3 duong khac chong len
    # lam khong doc duoc), ma dat TREN diem cao nhat ma BAT KY duong nao di qua trong ca
    # pham vi cot cua doan (_clear_y), roi mem "day" cac badge o gan nhau ra xa nhau.
    if primary_values is not None:
        badge_specs = []  # (i0, i1, text)
        pts0 = [(i, v) for i, v in enumerate(primary_values) if v is not None]
        for k in range(len(pts0) - 1):
            i0, v0 = pts0[k]; i1, v1 = pts0[k + 1]
            if i1 - i0 != 1 or v1 >= v0:
                continue
            bps = round((v1 - v0) * 100) if unit == "phan_tram" else round(v1 - v0)
            ax.plot([xs[i0], xs[i1]], [v0, v1], color=BRICK, lw=2.6, zorder=6,
                    solid_capstyle="round")
            badge_specs.append((i0, i1, f"ĐẢO NGƯỢC {cats[i0]}-{cats[i1]}: {bps:+.0f} bps"))
        for inv in (p.get("inversions") or []):
            t_from, t_to = inv["from"], inv["to"]
            if t_from not in cats or t_to not in cats:
                continue
            i0, i1 = cats.index(t_from), cats.index(t_to)
            v0, v1 = primary_values[i0], primary_values[i1]
            if v0 is None or v1 is None or v1 >= v0:
                continue  # bo qua, KHONG bia nhan "dao nguoc" cho doan dang tang
            bps = inv.get("bps")
            if bps is None:
                bps = round((v1 - v0) * 100) if unit == "phan_tram" else round(v1 - v0)
            ax.plot([xs[i0], xs[i1]], [v0, v1], color=BRICK, lw=1.6, ls=(0, (4, 3)), zorder=5)
            badge_specs.append((i0, i1, f"ĐẢO NGƯỢC {t_from}-{t_to}: {bps:+.0f} bps"))

        if badge_specs:
            ylo2, yhi2 = ax.get_ylim(); pad = (yhi2 - ylo2) * 0.05
            placed = []
            for i0, i1, text in badge_specs:
                clear = _clear_y(all_values_by_snapshot, i0, i1)
                base = clear if clear is not None else max(primary_values[i0], primary_values[i1])
                placed.append([(xs[i0] + xs[i1]) / 2.0, base + pad, text])
            placed.sort(key=lambda r: r[0])
            min_gap_b = (yhi2 - ylo2) * 0.09
            for k in range(1, len(placed)):
                if abs(placed[k][0] - placed[k - 1][0]) < max(1.5, n * 0.15) and \
                        placed[k][1] - placed[k - 1][1] < min_gap_b:
                    placed[k][1] = placed[k - 1][1] + min_gap_b
            for xm, ym, text in placed:
                _badge_at_data(ax, fig, xm, ym, text, dy=0.0)

        bf = p.get("butterfly")
        if bf:
            w1, w2 = bf["wings"][0], bf["wings"][1]
            if w1 in cats and w2 in cats:
                i0, i1 = cats.index(w1), cats.index(w2)
                v0, v1 = primary_values[i0], primary_values[i1]
                if v0 is not None and v1 is not None:
                    ax.plot([xs[i0], xs[i1]], [v0, v1], color=FAINT, lw=1.2,
                            ls=(0, (4, 3)), zorder=1)

    if any_uncertain:
        fig.text(0.035, 0.10,
                  "Chấm đặc, nét liền = quan sát được từ giá đóng cửa/broker quote  ·  "
                  "Chấm rỗng, nét đứt = ước tính dealer, thanh khoản thấp",
                  fontsize=7.6, color=MUTED, family=SANS, ha="left", va="bottom")
    return fig


# ============================================================== 2. futures_curve
def c_futures_curve(p, accent):
    """Duong cong gia ky han, tham chieu spot, badge contango/backwardation trung tinh.

    p = {
      meta chuan EIR...
      "spot": 82.4, "spot_label": "Giá giao ngay",
      "unit": "usd_thung",   # TUY CHON nhung NEN khai. Tu vung nay co du don vi hang
                              # hoa: "usd_tan" ca phe, "usd_thung" dau tho, "usd_oz" kim
                              # loai quy. Ban truoc phai bo qua rieng phep kiem don vi cap
                              # series vi hai don vi sau chua co trong tu vung; nay co roi
                              # nen khai unit la duoc validate_series() day du.
      "contracts": [
        {"month": "M1 (09/2026)", "price": 83.1, "liquid": True},
        {"month": "M12 (08/2027)", "price": 86.4, "liquid": False},  # -> tier "uoc-tinh"
        {"month": "M13", "status": "khong_ton_tai"},  # thang khong co open interest
      ],
      "y_format": "cur", "currency": "$",
      "roll_note": "Roll yield ước tính khoảng -2,1%/năm nếu nắm giữ hợp đồng gần liên tục",
    }

    "liquid" (mac dinh True) la loi tat cho "tier": liquid=False tuong duong tier=
    "uoc-tinh" (marker rong, doan net dut), dung CHINH quy tac tin cay cua c_yield_curve
    (muc 4.1: "ap dung quy tac ky han thua o muc 5"), khong tao mot quy uoc rieng.

    Trả lời: "Đường cong kỳ hạn đang contango hay backwardation, và chi phí quay vòng
    hợp đồng là bao nhiêu?"

    Dữ liệu cần: contracts dạng {month, price, do_tin_cay}, spot là giá giao ngay,
    unit lấy từ từ vựng schema.

    KHÔNG dùng cho hàng hoá mà kỳ hạn xa gần như không có giao dịch, vì đường nối
    những mức giá không ai giao dịch tạo ra một hình dạng thị trường không tồn tại.
    """
    contracts = list(p["contracts"])
    if not contracts:
        raise ValueError("c_futures_curve: can it nhat 1 contract")
    unit = p.get("unit")
    dp = p.get("dp")
    currency = p.get("currency", "$")

    months = [str(c["month"]) for c in contracts]
    n = len(months)
    xs = np.arange(n)

    values = [None] * n
    uncertain = [False] * n
    rows = []
    axis_marks = {}
    for i, c in enumerate(contracts):
        status = c.get("status", "co_that")
        value = c.get("price")
        rows.append({"entity": {"code": months[i][:24]}, "status": status, "value": value})
        if status == "co_that":
            values[i] = None if value is None else float(value)
            liquid = c.get("liquid", True)
            tin_cay = c.get("do_tin_cay") or _tu_tier_cu(c.get("tier")) or (
                "quan_sat" if liquid else "uoc_tinh")
            if tin_cay not in VOCAB["do_tin_cay"]:
                raise LoiSchema(ERR.DO_TIN_CAY_LA,
                    f'hop dong "{months[i]}" co do_tin_cay "{tin_cay}" khong nam trong tu vung')
            rows[-1]["do_tin_cay"] = tin_cay
            uncertain[i] = tin_cay != "quan_sat"
        else:
            mark = cach_ve(status)["danh_dau_truc"]
            if mark and axis_marks.get(i) != "da_loai":
                axis_marks[i] = mark

    if unit and unit in VOCAB["unit"]:
        series = {"unit": unit, "source": {"tier": p.get("source_tier", "cong-bo")}, "rows": rows}
        if dp is not None:
            series["decimals"] = dp
        validate_series(series)
    else:
        for i, row in enumerate(rows):
            validate_row(row, i)

    fig, ax = eir_fig(_meta(p, accent), figsize=(7.8, 4.8), rect=(0.10, 0.20, 0.74, 0.56))
    despine(ax, keep=("left", "bottom"), grid_axis="y")

    spot = float(p["spot"])
    ax.axhline(spot, color=FAINT, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.annotate(" " + p.get("spot_label", "Giá giao ngay"), (xs[0], spot), color=MUTED,
                fontsize=8.6, va="bottom", ha="left", xytext=(-4, 3),
                textcoords="offset points", fontstyle="italic")

    pts_that = _draw_curve_line(ax, xs, values, uncertain, accent, 2.4, "-", 7, zorder=3)

    ax.set_xticks(xs); ax.set_xticklabels(months, fontsize=9, color=INK)
    ax.set_xlim(-0.5, n - 0.5)
    ax.margins(y=0.18)
    if unit and unit in VOCAB["unit"]:
        dp_use = so_thap_phan({"unit": unit, **({"decimals": dp} if dp is not None else {})})
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.{dp_use}f}"))
        ax.set_ylabel(nhan_don_vi(unit), fontsize=9, color=MUTED)
    else:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_value(v, "cur", currency)))

    _draw_axis_marks(ax, xs, axis_marks)

    real_vals = [v for v in values if v is not None]
    shape = None
    if real_vals:
        if all(v > spot for v in real_vals):
            shape = "contango"
        elif all(v < spot for v in real_vals):
            shape = "backwardation"
    # hon hop: KHONG tu dong gan badge (muc 7.3), de tac gia bao cao tu chu thich bang tay
    if shape and pts_that:
        anchor_i, anchor_v = max(pts_that, key=lambda iv: abs(iv[1] - spot))
        _badge_at_data(ax, fig, xs[anchor_i], anchor_v,
                       "CONTANGO" if shape == "contango" else "BACKWARDATION")
    # roll_note luon dat O 1 VI TRI CO DINH (axes-fraction, goc tren-giua), KHONG neo
    # theo anchor cua badge: anchor co the nam sat dinh truc y (nhu contango voi hop
    # dong xa nhat), day chu thich troi len tan hang subtitle - da thay that trong 1
    # lan render thu.
    if p.get("roll_note"):
        ax.annotate(p["roll_note"], (0.5, 0.97), xycoords="axes fraction", ha="center",
                    va="top", fontsize=8, color=MUTED, fontstyle="italic")

    if any(uncertain):
        fig.text(0.035, 0.085,
                  "Chấm đặc = quan sát được, thanh khoản tốt  ·  "
                  "Chấm rỗng = ước tính, thanh khoản thấp hoặc chưa khớp lệnh",
                  fontsize=7.6, color=MUTED, family=SANS, ha="left", va="bottom")
    return fig


COMPONENTS = {
    "yield_curve": c_yield_curve,
    "futures_curve": c_futures_curve,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--out-dir")
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR curve components:", ", ".join(sorted(COMPONENTS))); return 0
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    module = spec.get("module", "MOD")
    accent = (spec.get("theme") or {}).get("accent", TEAL)
    os.makedirs(args.out_dir, exist_ok=True)
    ok = fail = 0
    for fs in spec.get("figures", []):
        fid = fs.get("id"); comp = fs.get("component")
        if args.only and fid != args.only:
            continue
        fn = COMPONENTS.get(comp)
        if fn is None:
            sys.stderr.write(f"WARN unknown EIR-curve component '{comp}' (id={fid})\n"); fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(args.out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir_curves: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
