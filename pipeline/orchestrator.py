#!/usr/bin/env python3
"""orchestrator.py, nối trọn đường ống, từ một file nội dung tới PDF đã qua gate.

Cách dùng:
    python3 pipeline/orchestrator.py <noi-dung.md> [--ra=<thu-muc>] [--bo-qua-gate]
                                     [--cho-phep-anh=N] [--chi=<buoc>]

Chạy đủ sáu bước:

    1. HÌNH      chạy mọi `hinh/*.mjs` và `hinh/*.py`, bake mọi `hinh/*.html`
    2. CK1       ghi kịch bản kể chuyện: mỗi section một câu hỏi, hình nào trả lời
    3. CK2       dựng ba bản bìa bằng nội dung thật, đủ ba kiểu, để chọn một
    4. DỰNG      HTML tự đủ, cả bản nội bộ lẫn bản gửi đi
    5. CK3       xuất PDF cả hai bản
    6. GATE      chạy mười gate trên cả hai bản

## Ba checkpoint không chặn, và vì sao

Checkpoint ghi artifact ra đĩa rồi in đường dẫn, không hỏi y/n trên terminal. Lý do là
thứ đo được chứ không phải khẩu vị: một script dừng chờ gõ phím thì không chạy được
trong test tự động, không chạy được khi Claude gọi, và không chạy được trong batch. Ba
artifact vẫn nằm đó để người duyệt mở ra xem trước khi chạy bước sau, nên tính chất
"có điểm dừng để duyệt" được giữ nguyên, chỉ khác ở chỗ ai bấm nút.

## Hai bản, một nguồn

Bản `noi-bo` nhúng đủ sổ nguồn, bản `gui-di` không nhúng và quy đổi nguồn nội bộ sang
nhãn công khai. Cả hai dựng từ cùng một file markdown, nên không có đường nào để hai
bản nói hai điều khác nhau.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "pipeline"))

from build_html import LoiDung, SoNguon, dung, tach_front_matter  # noqa: E402

BUOC = ["hinh", "ck1", "ck2", "dung", "ck3", "gate"]


def chay(lenh: list[str], mo_ta: str) -> None:
    ket = subprocess.run(lenh, cwd=str(REPO), capture_output=True, text=True)
    if ket.returncode != 0:
        print(f"  FAIL  {mo_ta}", file=sys.stderr)
        print((ket.stdout or "") + (ket.stderr or ""), file=sys.stderr)
        raise SystemExit(1)
    dong_cuoi = [d for d in (ket.stdout or "").strip().split("\n") if d.strip()]
    print(f"  ok    {mo_ta}" + (f"  ({dong_cuoi[-1]})" if dong_cuoi else ""))


# --------------------------------------------------------------------------- #
# Buoc 1: sinh hinh
# --------------------------------------------------------------------------- #
def sinh_hinh(thu_muc_bao_cao: Path) -> int:
    thu_muc = thu_muc_bao_cao / "hinh"
    if not thu_muc.exists():
        print("  bo qua: bao cao khong co thu muc hinh/")
        return 0

    so = 0
    for f in sorted(thu_muc.glob("*.mjs")):
        chay(["node", str(f)], f"chart ECharts {f.name}")
        so += 1
    for f in sorted(thu_muc.glob("*.py")):
        chay(["python3", str(f)], f"chart matplotlib {f.name}")
        so += 1
    for f in sorted(thu_muc.glob("*.html")):
        # Minh hoa co callout ve bang JavaScript luc chay. WeasyPrint khong chay JS nen
        # phai dong bang thanh SVG tinh truoc, neu khong PDF mat sach lop chu thich.
        ten_ra = f.parent / f"ra-{f.stem}.svg"
        chay(
            ["node", str(REPO / "pipeline/bake_svg.mjs"), str(f), str(ten_ra), "--selector=svg"],
            f"bake minh hoa {f.name}",
        )
        so += 1
    return so


# --------------------------------------------------------------------------- #
# Buoc 2: CK1, kich ban ke chuyen
# --------------------------------------------------------------------------- #
def ghi_ck1(nguon_md: Path, ra: Path) -> Path:
    van_ban = nguon_md.read_text(encoding="utf-8")
    meta, than = tach_front_matter(van_ban)

    muc: list[dict] = []
    for dong in than.split("\n"):
        t = dong.strip()
        if t.startswith("## "):
            muc.append({"ten": t[3:].strip(), "hinh": [], "so_doan": 0})
        elif t.startswith("::: ") and muc:
            loai = t[4:].split()[0]
            if loai in ("chart", "minh-hoa"):
                chu = ""
                if "chu=" in t:
                    sau = t.split("chu=", 1)[1]
                    chu = sau[1:].split('"')[0] if sau.startswith('"') else sau.split()[0]
                muc[-1]["hinh"].append({"loai": loai, "chu": chu})
        elif t and not t.startswith(("#", ":::")) and muc:
            muc[-1]["so_doan"] += 1

    dong_ra = [
        f"# CK1: kịch bản kể chuyện, {meta.get('tieu_de', '(chưa có tiêu đề)')}",
        "",
        "Mỗi section phải trả lời đúng một câu hỏi, và phải có hình trả lời câu hỏi đó.",
        "Section nào không có hình thì kiểm lại: hoặc câu hỏi chưa đủ sắc để cần hình,",
        "hoặc hình còn thiếu.",
        "",
        "| Section | Số đoạn | Hình | Chú thích hình |",
        "|---|---:|---|---|",
    ]
    for m in muc:
        if m["hinh"]:
            for i, h in enumerate(m["hinh"]):
                ten = m["ten"] if i == 0 else ""
                so_doan = str(m["so_doan"]) if i == 0 else ""
                dong_ra.append(f"| {ten} | {so_doan} | {h['loai']} | {h['chu'][:70]} |")
        else:
            dong_ra.append(f"| {m['ten']} | {m['so_doan']} | KHÔNG CÓ HÌNH | |")

    thieu = [m["ten"] for m in muc if not m["hinh"]]
    dong_ra += ["", f"Tổng: {len(muc)} section, {sum(len(m['hinh']) for m in muc)} hình."]
    if thieu:
        dong_ra.append(f"Section chưa có hình: {', '.join(thieu)}.")

    ra.write_text("\n".join(dong_ra) + "\n", encoding="utf-8")
    return ra


# --------------------------------------------------------------------------- #
# Buoc 3: CK2, ba ban bia bang noi dung that
# --------------------------------------------------------------------------- #
def ghi_ck2(nguon_md: Path, thu_muc_ra: Path) -> list[Path]:
    van_ban = nguon_md.read_text(encoding="utf-8")
    da_ghi = []
    for kieu in ("dac", "hairline", "vien-accent"):
        # Ban markdown tam phai nam CUNG thu muc voi ban goc, khong phai trong thu muc
        # dau ra: `so_nguon` va `src` cua hinh deu la duong dan tuong doi tinh tu file
        # noi dung, dat lech mot cap thu muc la moi tham chieu do gay het.
        tam = nguon_md.parent / f"_ck2-tam-{kieu}.md"
        if "bia_kieu:" in van_ban:
            sua = "\n".join(
                f"bia_kieu: {kieu}" if d.strip().startswith("bia_kieu:") else d
                for d in van_ban.split("\n")
            )
        else:
            sua = van_ban.replace("---\n", f"---\nbia_kieu: {kieu}\n", 1)
        tam.write_text(sua, encoding="utf-8")
        ra_html = thu_muc_ra / f"ck2-bia-{kieu}.html"
        try:
            dung(tam, ra_html, "noi-bo")
            chay(
                ["python3", str(REPO / "pipeline/render_pdf.py"), str(ra_html), str(ra_html.with_suffix(".pdf"))],
                f"CK2 bia kieu {kieu}",
            )
        finally:
            tam.unlink(missing_ok=True)
        da_ghi.append(ra_html.with_suffix(".pdf"))
    return da_ghi


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Tu mot file noi dung ra PDF da qua gate")
    ap.add_argument("nguon", type=Path)
    ap.add_argument("--ra", dest="ra", type=Path, default=None, help="thu muc dau ra, mac dinh <thu-muc-bao-cao>/ra")
    ap.add_argument("--bo-qua-gate", dest="bo_qua_gate", action="store_true")
    ap.add_argument("--cho-phep-anh", dest="cho_phep_anh", type=int, default=0)
    ap.add_argument("--chi", dest="chi", default=None, help="chi chay mot buoc: " + ", ".join(BUOC))
    t = ap.parse_args()

    nguon = t.nguon.resolve()
    if not nguon.exists():
        print(f"orchestrator FAIL: khong tim thay {nguon}", file=sys.stderr)
        return 1
    thu_muc_bao_cao = nguon.parent
    thu_muc_ra = (t.ra or (thu_muc_bao_cao / "ra")).resolve()
    thu_muc_ra.mkdir(parents=True, exist_ok=True)

    can_chay = BUOC if not t.chi else [t.chi]
    ten = nguon.stem

    try:
        if "hinh" in can_chay:
            print("[1/6] HINH")
            so = sinh_hinh(thu_muc_bao_cao)
            print(f"  {so} hinh da sinh")

        if "ck1" in can_chay:
            print("[2/6] CK1 kich ban ke chuyen")
            p = ghi_ck1(nguon, thu_muc_ra / "ck1-kich-ban.md")
            print(f"  ok    {p}")

        if "ck2" in can_chay:
            print("[3/6] CK2 ba ban bia bang noi dung that")
            ghi_ck2(nguon, thu_muc_ra)

        ban = {}
        if "dung" in can_chay:
            print("[4/6] DUNG HTML")
            for che_do in ("noi-bo", "gui-di"):
                ra_html = thu_muc_ra / f"{ten}-{che_do}.html"
                dung(nguon, ra_html, che_do)
                ban[che_do] = ra_html
                print(f"  ok    {ra_html} ({ra_html.stat().st_size / 1024:.0f}KB)")

        if "ck3" in can_chay:
            print("[5/6] CK3 xuat PDF")
            for che_do in ("noi-bo", "gui-di"):
                ra_html = thu_muc_ra / f"{ten}-{che_do}.html"
                ra_pdf = ra_html.with_suffix(".pdf")
                chay(
                    ["python3", str(REPO / "pipeline/render_pdf.py"), str(ra_html), str(ra_pdf),
                     f"--cho-phep-anh={t.cho_phep_anh}"],
                    f"PDF ban {che_do}",
                )

        if "gate" in can_chay and not t.bo_qua_gate:
            print("[6/6] GATE")
            hong = False
            for che_do in ("noi-bo", "gui-di"):
                ra_html = thu_muc_ra / f"{ten}-{che_do}.html"
                ra_pdf = ra_html.with_suffix(".pdf")
                ket = subprocess.run(
                    ["node", str(REPO / "gates/run.mjs"), str(ra_html), str(ra_pdf),
                     f"--che-do={che_do}", f"--cho-phep-anh={t.cho_phep_anh}"],
                    cwd=str(REPO), capture_output=True, text=True,
                )
                print(ket.stdout)
                if ket.returncode != 0:
                    print(ket.stderr, file=sys.stderr)
                    hong = True
            if hong:
                print("orchestrator: co gate FAIL, khong duoc giao file", file=sys.stderr)
                return 1

    except LoiDung as e:
        print(f"orchestrator FAIL: {e}", file=sys.stderr)
        return 1

    # Chi liet ke artifact cua BUOC DA CHAY. In ca ba checkpoint sau mot lan chay
    # `--chi=ck1` la bao cao sai su that: nguoi doc tuong ba ban bia va hai ban PDF vua
    # duoc sinh lai, trong khi chung con nguyen tu lan chay truoc hoac chua ton tai.
    print()
    print("XONG. Artifact nam o", thu_muc_ra)
    if "ck1" in can_chay:
        print("  CK1 kich ban:      ck1-kich-ban.md")
    if "ck2" in can_chay:
        print("  CK2 ba ban bia:    ck2-bia-dac.pdf, ck2-bia-hairline.pdf, ck2-bia-vien-accent.pdf")
    if "ck3" in can_chay:
        print(f"  CK3 ban day du:    {ten}-noi-bo.pdf va {ten}-gui-di.pdf")
    if "hinh" in can_chay:
        print(f"  Hinh da sinh:      {thu_muc_bao_cao / 'hinh'}/ra-*.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
