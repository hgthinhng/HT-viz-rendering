#!/usr/bin/env python3
"""render_pdf.py — HTML tu du sang PDF bang WeasyPrint, co kiem ngay sau khi ghi.

Cach dung:
    python3 pipeline/render_pdf.py <vao.html> <ra.pdf> [--cho-phep-anh=N]

## Vi sao WeasyPrint chu khong phai Chromium

Da do tren bao cao that 9 trang: WeasyPrint cho 0 object anh raster, Chromium tren
cung mot file tao mot anh JPEG an trong Tiling Pattern ma `get_images()` khong thay.
Ban in phai la vector, vi anh raster trong PDF vua nang file vua vo net khi phong to
vua khong con chon duoc chu.

## Vi sao ghi xong phai mo lai kiem

Day chinh la cho bug 12 chart chui qua duoc suot ca mot phase. WeasyPrint gap SVG
khong hop le XML thi bo qua CA FILE, khong nem loi, khong ghi canh bao. Lenh chay
xong, exit 0, file PDF ton tai, dung kich thuoc hop ly, va rong khong mot net ve.
Neu buoc render khong tu mo lai file ma dem, thi khong con ai dem nua.

Ba nguong chan cung o day, cai nao vi pham cung dung han:
  - 0 trang: khong co gi de giao
  - 0 net ve: trang trang, gan nhu chac chan la SVG bi bo qua
  - anh raster vuot muc cho phep (mac dinh 0): ban in mat tinh vector
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import fitz  # pymupdf
from weasyprint import HTML


def dem_anh_raster(doc: "fitz.Document") -> list[dict]:
    """Dem anh qua `xref_object`, KHONG dung `get_images()`.

    `get_images()` bo sot anh nam trong Tiling Pattern, va do dung la kieu anh ma
    Chromium sinh ra khi nuong gradient hoac shadow co blur. Mot phep dem bo sot dung
    truong hop can bat nhat thi khong phai phep dem.
    """
    ra = []
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=True)
        except Exception:
            continue
        if "/Subtype/Image" not in obj.replace(" ", ""):
            continue
        w = re.search(r"/Width\s*(\d+)", obj)
        h = re.search(r"/Height\s*(\d+)", obj)
        ra.append(
            {
                "xref": xref,
                "w": int(w.group(1)) if w else 0,
                "h": int(h.group(1)) if h else 0,
            }
        )
    return ra


def render(vao: Path, ra: Path, cho_phep_anh: int = 0) -> dict:
    if not vao.exists():
        raise SystemExit(f"render_pdf FAIL: khong tim thay {vao}")
    ra.parent.mkdir(parents=True, exist_ok=True)

    HTML(filename=str(vao), base_url=str(vao.parent)).write_pdf(str(ra))

    doc = fitz.open(str(ra))
    so_trang = doc.page_count
    net_ve = sum(len(doc[i].get_drawings()) for i in range(so_trang))
    chu = sum(len(doc[i].get_text()) for i in range(so_trang))
    anh = dem_anh_raster(doc)
    doc.close()

    ket = {
        "pdf": str(ra),
        "so_trang": so_trang,
        "net_ve": net_ve,
        "ky_tu_chu": chu,
        "anh_raster": len(anh),
        "kich_thuoc_kb": round(ra.stat().st_size / 1024, 1),
    }

    loi = []
    if so_trang == 0:
        loi.append("PDF khong co trang nao")
    if net_ve == 0:
        loi.append(
            "PDF khong co net ve nao. Gan nhu chac chan mot SVG khong hop le XML da bi "
            "WeasyPrint bo qua tron file, hoac trang that su trong"
        )
    if len(anh) > cho_phep_anh:
        kich = ", ".join(f"{a['w']}x{a['h']}" for a in anh[:3])
        loi.append(
            f"{len(anh)} anh raster, vuot muc cho phep {cho_phep_anh} ({kich}). "
            f"Ban in phai la vector"
        )
    if loi:
        for l in loi:
            print(f"render_pdf FAIL: {l}", file=sys.stderr)
        raise SystemExit(1)

    return ket


def main() -> int:
    ap = argparse.ArgumentParser(description="HTML sang PDF bang WeasyPrint")
    ap.add_argument("vao", type=Path)
    ap.add_argument("ra", type=Path)
    ap.add_argument(
        "--cho-phep-anh",
        dest="cho_phep_anh",
        type=int,
        default=0,
        help="so anh raster duoc phep, mac dinh 0. Chi noi len khi bao cao co anh chup that",
    )
    t = ap.parse_args()
    k = render(t.vao, t.ra, t.cho_phep_anh)
    print(
        f"render_pdf OK -> {k['pdf']} ({k['so_trang']} trang, {k['net_ve']} net ve, "
        f"{k['ky_tu_chu']} ky tu chu, {k['anh_raster']} anh raster, {k['kich_thuoc_kb']}KB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
