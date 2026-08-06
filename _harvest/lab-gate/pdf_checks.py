#!/usr/bin/env python3
"""pdf_checks.py — cac kiem tra chi lam duoc tren PDF nhi phan (pymupdf).
Goi tu gate.mjs, in ra 1 dong JSON duy nhat ra stdout.

Usage: python3 pdf_checks.py <file.pdf>

Cover:
  - raster: dem object /Subtype /Image qua xref_object (KHONG dung get_images,
    vi get_images bo sot anh nam trong Tiling Pattern — theo yeu cau brief).
  - diacritics: dem U+FFFD (glyph mat hoan toan) + ty le ky tu "synthetic"
    (MuPDF khong xac dinh chac chan duoc unicode that cua glyph) tren rieng
    tap ky tu co dau tieng Viet — day la tin hieu RE, KHONG PHAI thay the cho
    buoc soi tay bang mat (xem ghi chu trong gate.mjs).
  - pagebreak: do hinh hoc — tim hinh chu nhat (card/panel) bi cat dung tai
    duong bien trang: mep duoi trang N cham mep tren trang N+1, cung mau,
    cung toa do trai/phai.
"""
import sys
import re
import os
import json

import fitz  # pymupdf

VIET_DIACRITICS = set(
    "ăâêôơưđ"
    "ẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ".lower()
    + "ẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ"
)


def check_raster(doc):
    image_objs = 0
    big_images = []
    total_px = 0
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=True)
        except Exception:
            continue
        norm = obj.replace(" ", "")
        if "/Subtype/Image" in norm:
            image_objs += 1
            w = re.search(r"/Width (\d+)", obj) or re.search(r"/Width(\d+)", obj)
            h = re.search(r"/Height (\d+)", obj) or re.search(r"/Height(\d+)", obj)
            if w and h:
                wv, hv = int(w.group(1)), int(h.group(1))
                total_px += wv * hv
                if wv * hv > 500_000:  # ~ hon 1 panel 700x700, dau hieu raster toan-panel
                    big_images.append({"xref": xref, "w": wv, "h": hv, "px": wv * hv})
    return {
        "image_objects": image_objs,
        "big_panel_images": big_images,
        "total_image_px": total_px,
    }


def check_diacritics(doc):
    total_chars = 0
    synthetic_chars = 0
    fffd = 0
    viet_total = 0
    viet_synthetic = 0
    pdf_text_all = []
    for pno in range(doc.page_count):
        page = doc[pno]
        pdf_text_all.append(page.get_text())
        d = page.get_text("rawdict")
        for block in d.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    for ch in span["chars"]:
                        total_chars += 1
                        c = ch["c"]
                        is_synth = bool(ch.get("synthetic"))
                        if is_synth:
                            synthetic_chars += 1
                        if c == "�":
                            fffd += 1
                        if c in VIET_DIACRITICS:
                            viet_total += 1
                            if is_synth:
                                viet_synthetic += 1
    return {
        "total_chars": total_chars,
        "synthetic_chars": synthetic_chars,
        "synthetic_ratio": (synthetic_chars / total_chars) if total_chars else None,
        "fffd_count": fffd,
        "viet_diacritic_total": viet_total,
        "viet_diacritic_synthetic": viet_synthetic,
        "pdf_text": "\n".join(pdf_text_all),
    }


def check_pagebreak(doc, eps_edge=1.5, eps_x=3.0, eps_color=0.02):
    def close(a, b, eps):
        return abs(a - b) <= eps

    def color_close(c1, c2, eps=eps_color):
        if c1 is None or c2 is None:
            return c1 == c2
        return all(abs(a - b) <= eps for a, b in zip(c1, c2))

    per_page = []
    for i in range(doc.page_count):
        pg = doc[i]
        draws = pg.get_drawings()
        rects = []
        for d in draws:
            fill = d.get("fill")
            rect = d.get("rect")
            if fill is None or rect is None:
                continue
            if rect.width < 20 or rect.height < 4:
                continue
            if rect.width >= pg.rect.width * 0.95 and rect.height >= pg.rect.height * 0.95:
                continue  # nen toan trang, khong phai card noi dung
            rects.append((rect, fill))
        per_page.append((pg.rect.height, rects))

    hits = []
    for i in range(doc.page_count - 1):
        h, rects = per_page[i]
        _, rects2 = per_page[i + 1]
        bottom_touch = [(r, f) for r, f in rects if close(r.y1, h, eps_edge)]
        top_touch = [(r, f) for r, f in rects2 if close(r.y0, 0, eps_edge)]
        for r1, f1 in bottom_touch:
            for r2, f2 in top_touch:
                if close(r1.x0, r2.x0, eps_x) and close(r1.x1, r2.x1, eps_x) and color_close(f1, f2):
                    hits.append({"page_a": i + 1, "page_b": i + 2, "fill": list(f1)})
    return {"sliced_panel_hits": hits, "total_hits": len(hits)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: pdf_checks.py <file.pdf>"}))
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(json.dumps({"error": f"khong tim thay file: {path}"}))
        sys.exit(2)

    doc = fitz.open(path)
    out = {
        "file": path,
        "file_size_bytes": os.path.getsize(path),
        "pages": doc.page_count,
        "bytes_per_page": os.path.getsize(path) / doc.page_count if doc.page_count else None,
        "raster": check_raster(doc),
        "diacritics": check_diacritics(doc),
        "pagebreak": check_pagebreak(doc),
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
