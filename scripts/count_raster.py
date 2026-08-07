#!/usr/bin/env python3
"""
count_raster.py, đếm object /Subtype /Image trong một file PDF bằng cách
quét TOÀN BỘ xref qua doc.xref_object(xref, compressed=True), KHÔNG dùng
doc.get_images(). Lý do bắt buộc dùng xref_object: get_images() bỏ sót ảnh
nằm trong Tiling Pattern / object stream nén, đã bắt được thật ít nhất 2 lần
trong quá trình build thư viện này (xem README.md gốc, mục "bẫy đã đo được").

Dùng làm gate: exit code 0 nếu count <= --max, exit code 1 nếu vượt.

Usage:
    python3 count_raster.py <pdf-path> [--max N] [--json]

Yêu cầu: pip install pymupdf
"""
import sys
import json
import argparse


def count_raster_images(pdf_path):
    import fitz  # pymupdf

    doc = fitz.open(pdf_path)
    xrefs = []
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=True)
        except Exception:
            continue
        if "/Subtype/Image" in obj.replace(" ", ""):
            xrefs.append(xref)
    return {
        "pdf_path": pdf_path,
        "page_count": doc.page_count,
        "raster_count": len(xrefs),
        "raster_xrefs": xrefs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--max", type=int, default=0, help="Số ảnh raster tối đa cho phép (mặc định 0)")
    ap.add_argument("--json", action="store_true", help="In JSON thay vì dòng người đọc")
    args = ap.parse_args()

    result = count_raster_images(args.pdf_path)
    passed = result["raster_count"] <= args.max
    result["max_allowed"] = args.max
    result["passed"] = passed

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {args.pdf_path}: {result['raster_count']} ảnh raster "
              f"(cho phép tối đa {args.max}), {result['page_count']} trang")
        if result["raster_xrefs"]:
            print("  xref:", result["raster_xrefs"])

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
