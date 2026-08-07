#!/usr/bin/env python3
"""sinh_catalog.py, dung mot muc luc DUY NHAT cho ca thu vien hinh.

    python3 scripts/sinh_catalog.py            # ghi catalog/INDEX.json va catalog/CATALOG.md
    python3 scripts/sinh_catalog.py --kiem     # khong ghi, chi bao co lech khong (exit 1 neu lech)

## Van de no giai

Thu vien co bon nhom tai san nam bon cho, mo ta theo bon khuon khac nhau: comment dau
file cua preset ECharts, docstring cua component matplotlib, muc "Mo ta / khi nao dung"
cua catalog component, va cap <title>/<desc> cua minh hoa SVG. Muon biet "thu vien co gi,
hinh nao tra loi cau hoi nao" thi phai mo bon cho va doc bon kieu.

Muc luc nay gom ca bon ve MOT dang, sinh tu CHINH ma nguon chu khong go tay. Go tay thi
sau ba lan sua code no thanh mot ban do cu cua mot thanh pho da doi duong, va do la kieu
tai lieu con te hon khong co tai lieu: no van doc tron tru va no dan sai duong.

## Thanh that ve cho thieu

Tai san nao khong tu mo ta duoc thi muc luc ghi thang `null` va CATALOG.md in "CHUA CO
MO TA". Khong suy dien tu ten ham, khong dien vao cho trong. Mot muc luc bia mo ta se
lam nguoi doc tin rang cai hop rong la cai hop day.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THU_MUC_CATALOG = REPO / "catalog"

# Cau bat dau bang mot trong cac cum nay duoc coi la loi canh bao "khi nao dung".
DAU_HIEU_KHONG_DUNG = re.compile(
    r"(KHÔNG dùng|Không dùng|không nên dùng|đừng dùng|KHÔNG nên dùng|cấm dùng)", re.I
)


def cau_chua_canh_bao(van_ban: str) -> str | None:
    """Cau dau tien noi ve viec KHONG nen dung. Tra ve None neu khong co."""
    for cau in re.split(r"(?<=[.;])\s+", van_ban.replace("\n", " ")):
        if DAU_HIEU_KHONG_DUNG.search(cau):
            return re.sub(r"\s+", " ", cau).strip()
    return None


# --------------------------------------------------------------------------- #
# Nhom A1: preset ECharts
# --------------------------------------------------------------------------- #
def quet_echarts() -> list[dict]:
    ra = []
    for f in sorted((REPO / "charts/echarts").glob("[0-9][0-9]-*.mjs")):
        dong = f.read_text(encoding="utf-8").split("\n")
        # Comment dau file, den dong khong phai comment thi dung.
        khoi = []
        for d in dong:
            if d.startswith("//"):
                khoi.append(d[2:].strip())
            elif d.strip() == "":
                continue
            else:
                break
        van_ban = "\n".join(khoi)

        ten = None
        m = re.match(r"^[\w.-]+,\s*(.+)$", khoi[0]) if khoi else None
        if m:
            ten = m.group(1).strip()

        def muc(nhan: str) -> str | None:
            m = re.search(rf"{nhan}:\s*(.+?)(?=\n[A-ZĐ][\w ]{{2,}}:|\Z)", van_ban, re.S)
            if not m:
                return None
            # Bo dau "//" con sot khi mot dong comment tu no bat dau bang "//".
            return re.sub(r"\s+", " ", m.group(1).replace("//", " ")).strip()

        ra.append({
            "ma": f.stem,
            "nhom": "chart-echarts",
            "ten": ten,
            "tep": str(f.relative_to(REPO)),
            "dinh_dang_giao": "HTML tuong tac",
            "tra_loi": muc("Dùng khi"),
            "du_lieu_can": muc("Dữ liệu cần"),
            "khong_dung_khi": cau_chua_canh_bao(van_ban) or muc("Bẫy thường gặp"),
            "xem_truoc": f"charts/echarts/out-{f.stem}.svg",
        })
    return ra


# --------------------------------------------------------------------------- #
# Nhom A2: component matplotlib
# --------------------------------------------------------------------------- #
def quet_matplotlib() -> list[dict]:
    ra = []
    for f in sorted((REPO / "charts/matplotlib").glob("viz_eir*.py")):
        cay = ast.parse(f.read_text(encoding="utf-8"))
        for nut in ast.walk(cay):
            if not isinstance(nut, ast.FunctionDef) or not nut.name.startswith("c_"):
                continue
            doc = ast.get_docstring(nut)
            ten = tra_loi = du_lieu = None
            if doc:
                dong = [d.strip() for d in doc.split("\n")]
                ten = dong[0].rstrip(".") or None
                than = "\n".join(dong[1:])
                m = re.search(r"Trả lời:\s*(.+?)(?=\n\s*\n|\Z)", than, re.S)
                tra_loi = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
                m = re.search(r"Dữ liệu cần:\s*(.+?)(?=\n\s*\n|\Z)", than, re.S)
                du_lieu = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
            ra.append({
                "ma": nut.name[2:],
                "nhom": "chart-matplotlib",
                "ten": ten,
                "tep": f"{f.relative_to(REPO)}:{nut.lineno}",
                "dinh_dang_giao": "PDF tinh",
                "tra_loi": tra_loi,
                "du_lieu_can": du_lieu,
                "khong_dung_khi": cau_chua_canh_bao(doc) if doc else None,
                # Ban xem truoc chi ton tai neu component do co bo tham so vi du trong
                # spec_showcase.json va da chay `scripts/sinh_xem_truoc.py`. Tro toi mot
                # file khong co thi contact sheet se hien o trong, nen kiem su ton tai.
                "xem_truoc": (
                    f"catalog/xem-truoc/{nut.name[2:]}.svg"
                    if (REPO / f"catalog/xem-truoc/{nut.name[2:]}.svg").exists()
                    else None
                ),
            })
    return sorted(ra, key=lambda x: x["ma"])


# --------------------------------------------------------------------------- #
# Nhom B: component ke chuyen
# --------------------------------------------------------------------------- #
def quet_component() -> list[dict]:
    ra = []
    for f in sorted((REPO / "components/catalog").glob("*.md")):
        s = f.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", s, re.M)
        ten = m.group(1).strip() if m else None
        m = re.search(r"^## Mô tả / khi nào dùng\s*\n+(.+?)(?=\n## |\Z)", s, re.S | re.M)
        than = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        # "Tra loi:" va "Tra loi cau hoi:" deu xuat hien trong catalog. Cat truoc muc
        # ke tiep de cot nay khong nuot luon phan canh bao cua cot ben canh.
        m2 = re.search(
            r"Trả lời(?:\s+câu hỏi)?:\s*(.+?)(?=\s(?:Đầu vào|Bắt buộc|KHÔNG dùng|Không dùng)|\Z)",
            than,
        )
        ra.append({
            "ma": f.stem,
            "nhom": "component",
            "ten": ten,
            "tep": str(f.relative_to(REPO)),
            "dinh_dang_giao": "HTML va PDF",
            "tra_loi": (m2.group(1).strip() if m2 else (than[:180] or None)),
            "du_lieu_can": None,
            "khong_dung_khi": cau_chua_canh_bao(than),
            "xem_truoc": "components/gallery.html",
        })
    return ra


# --------------------------------------------------------------------------- #
# Nhom C: minh hoa nganh
# --------------------------------------------------------------------------- #
def quet_minh_hoa() -> list[dict]:
    ra = []
    for f in sorted((REPO / "illustrations/svg").glob("*.svg")):
        s = f.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        ten = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        m = re.search(r"<desc>(.*?)</desc>", s, re.S)
        mo_ta = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        ra.append({
            "ma": f.stem,
            "nhom": "minh-hoa",
            "ten": ten,
            "tep": str(f.relative_to(REPO)),
            "dinh_dang_giao": "HTML va PDF, phai bake truoc neu co callout",
            "tra_loi": mo_ta,
            "du_lieu_can": None,
            "khong_dung_khi": cau_chua_canh_bao(mo_ta) if mo_ta else None,
            "xem_truoc": str(f.relative_to(REPO)),
        })
    return ra


# --------------------------------------------------------------------------- #
def dung_muc_luc() -> dict:
    muc = quet_echarts() + quet_matplotlib() + quet_component() + quet_minh_hoa()
    thieu = [m["ma"] for m in muc if not m["tra_loi"]]
    return {
        "_doc": [
            "Sinh tu dong bang scripts/sinh_catalog.py, DUNG SUA TAY.",
            "Sua mo ta thi sua o NGUON: comment dau file preset, docstring component,",
            "muc 'Mo ta / khi nao dung' cua catalog, hoac <desc> cua SVG. Roi chay lai.",
        ],
        "tong": len(muc),
        "theo_nhom": {n: sum(1 for m in muc if m["nhom"] == n) for n in
                      ("chart-echarts", "chart-matplotlib", "component", "minh-hoa")},
        "thieu_mo_ta": thieu,
        "muc": muc,
    }


def dung_markdown(ml: dict) -> str:
    NHOM = {
        "chart-echarts": ("Chart ECharts, cho bản HTML tương tác", "charts/echarts/"),
        "chart-matplotlib": ("Component matplotlib EIR, cho bản PDF tĩnh", "charts/matplotlib/"),
        "component": ("Component kể chuyện", "components/catalog/"),
        "minh-hoa": ("Minh hoạ ngành", "illustrations/svg/"),
    }
    d = [
        "# Mục lục thư viện hình",
        "",
        "**File này sinh tự động bằng `python3 scripts/sinh_catalog.py`. Đừng sửa tay.**",
        "Sửa mô tả thì sửa ở nguồn (comment đầu file preset, docstring component, mục",
        "`Mô tả / khi nào dùng` của catalog, hoặc `<desc>` của SVG) rồi chạy lại.",
        "",
        f"Tổng {ml['tong']} tài sản: " + ", ".join(
            f"{v} {k}" for k, v in ml["theo_nhom"].items()) + ".",
        "",
    ]
    if ml["thieu_mo_ta"]:
        d += [
            f"**{len(ml['thieu_mo_ta'])} tài sản chưa có mô tả**, liệt kê thẳng ở đây thay vì",
            "để mục lục nói dối rằng thư viện đã đủ tài liệu: "
            + ", ".join(f"`{x}`" for x in ml["thieu_mo_ta"]) + ".",
            "",
        ]
    for nhom, (tieu_de, duong) in NHOM.items():
        cac_muc = [m for m in ml["muc"] if m["nhom"] == nhom]
        d += [f"## {tieu_de}", "", f"Nguồn: `{duong}`", "",
              "| Mã | Trả lời câu hỏi gì | Khi nào đừng dùng |", "|---|---|---|"]
        for m in cac_muc:
            tra_loi = m["tra_loi"] or "**CHƯA CÓ MÔ TẢ**"
            canh_bao = m["khong_dung_khi"] or ""
            cat = lambda s, n: (s[:n].rsplit(" ", 1)[0] + "..." if len(s) > n else s)
            d.append(f"| `{m['ma']}` | {cat(tra_loi, 190)} | {cat(canh_bao, 130)} |")
        d.append("")
    return "\n".join(d) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Dung muc luc thu vien hinh tu chinh ma nguon")
    ap.add_argument("--kiem", action="store_true", help="khong ghi, chi bao co lech khong")
    t = ap.parse_args()

    ml = dung_muc_luc()
    md = dung_markdown(ml)
    p_json = THU_MUC_CATALOG / "INDEX.json"
    p_md = THU_MUC_CATALOG / "CATALOG.md"
    noi_dung_json = json.dumps(ml, ensure_ascii=False, indent=2) + "\n"

    if t.kiem:
        lech = []
        for p, moi in ((p_json, noi_dung_json), (p_md, md)):
            if not p.exists():
                lech.append(f"{p.relative_to(REPO)} chua ton tai")
            elif p.read_text(encoding="utf-8") != moi:
                lech.append(f"{p.relative_to(REPO)} da troi khoi ma nguon")
        if lech:
            for l in lech:
                print(f"catalog LECH: {l}", file=sys.stderr)
            print("Chay: python3 scripts/sinh_catalog.py", file=sys.stderr)
            return 1
        print(f"catalog khop ma nguon ({ml['tong']} tai san, {len(ml['thieu_mo_ta'])} chua co mo ta)")
        return 0

    THU_MUC_CATALOG.mkdir(parents=True, exist_ok=True)
    p_json.write_text(noi_dung_json, encoding="utf-8")
    p_md.write_text(md, encoding="utf-8")
    print(f"catalog OK: {ml['tong']} tai san, {len(ml['thieu_mo_ta'])} chua co mo ta")
    for n, so in ml["theo_nhom"].items():
        print(f"  {n:20s} {so}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
