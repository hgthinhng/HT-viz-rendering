#!/usr/bin/env python3
"""pdf_checks.py — moi phep do chi lam duoc tren PDF nhi phan. In mot dong JSON.

Cach dung: python3 gates/pdf_checks.py <file.pdf>

Goi tu `gates/run.mjs` dung MOT lan roi chia ket qua cho nhieu gate, vi mo va quet
toan bo xref cua mot PDF nhieu trang la phan dat nhat cua ca bo gate.

Bon nhom phep do:

`fonts`       Ten font THAT duoc nhung trong PDF. Day la phep do quan trong nhat ma bo
              gate cu khong co. Da do bang so trong Phase 2: mot trang khai @font-face
              base64 cho ra `Spectral` va `IBM-Plex-Mono`, con chinh trang do bo di
              @font-face thi cho ra `Noto-Serif` va `Liberation-Mono`. CA HAI ban deu
              cho tang text dung y nguyen, 0 ky tu synthetic, 0 FFFD. Nghia la phep do
              tang text KHONG phan biet duoc file dung font that voi file am tham roi
              ve font he thong Linux. Chi doc ten font trong PDF moi phan biet duoc.

`raster`      Dem object `/Subtype /Image` qua `xref_object`, KHONG dung `get_images()`,
              vi `get_images()` bo sot anh nam trong Tiling Pattern, dung kieu anh ma
              Chromium sinh ra khi nuong gradient hay shadow co blur.

`diacritics`  Dem U+FFFD va ky tu "synthetic" tren RIENG tap ky tu co dau tieng Viet.
              Khong dem synthetic tren toan van ban: font subset khong nhung glyph dau
              CACH nen MuPDF danh dau moi dau cach la synthetic, va mot ban PDF sach 6
              trang cho ra 235 ca nhu vay. Dem ca thi gate do vinh vien.

`pagebreak`   Hinh hoc that: tim hinh chu nhat bi cat dung tai bien trang, tuc mep duoi
              trang N cham mep tren trang N+1, cung mau, cung toa do trai phai.

`text`        Toan bo tang text, va ban da bo het khoang trang. Ban bo trang la bat buoc
              cho phep doi chieu chuoi: trich text tu PDF nuot khoang trang giua cac
              glyph sat nhau, "475 TY USD" ra thanh "475 TYUSD". So nguyen van se bao
              thieu mot chuoi dang co that tren giay.
"""
from __future__ import annotations

import json
import os
import re
import sys

import fitz  # pymupdf

DAU_TIENG_VIET = set(
    "ăâêôơưđ"
    "ẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ".lower()
    + "ẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ"
)


def do_font(doc: "fitz.Document") -> dict:
    ho = {}
    for pno in range(doc.page_count):
        for f in doc.get_page_fonts(pno, full=True):
            # (xref, ext, type, basefont, name, encoding, referencer)
            ten = f[3]
            # Bo tien to subset dang "ABCDEF+"
            sach = re.sub(r"^[A-Z]{6}\+", "", ten)
            ho.setdefault(sach, {"ten_day_du": ten, "duoi": f[1], "nhung": f[1] != "n/a"})
    return {"ho_font": ho}


def do_raster(doc: "fitz.Document") -> dict:
    so_object = 0
    anh_lon = []
    tong_px = 0
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=True)
        except Exception:
            continue
        if "/Subtype/Image" not in obj.replace(" ", ""):
            continue
        so_object += 1
        w = re.search(r"/Width\s*(\d+)", obj)
        h = re.search(r"/Height\s*(\d+)", obj)
        if w and h:
            wv, hv = int(w.group(1)), int(h.group(1))
            tong_px += wv * hv
            if wv * hv > 500_000:
                anh_lon.append({"xref": xref, "w": wv, "h": hv, "px": wv * hv})
    return {"so_object": so_object, "anh_toan_panel": anh_lon, "tong_px": tong_px}


def do_dau(doc: "fitz.Document") -> dict:
    tong_ky_tu = 0
    fffd = 0
    dau_tong = 0
    dau_synthetic = 0
    synthetic_khoang_trang = 0
    for pno in range(doc.page_count):
        raw = doc[pno].get_text("rawdict")
        for khoi in raw.get("blocks", []):
            if "lines" not in khoi:
                continue
            for dong in khoi["lines"]:
                for span in dong["spans"]:
                    for ch in span["chars"]:
                        tong_ky_tu += 1
                        c = ch["c"]
                        synth = bool(ch.get("synthetic"))
                        if c == "�":
                            fffd += 1
                        if synth and c.isspace():
                            synthetic_khoang_trang += 1
                        if c in DAU_TIENG_VIET:
                            dau_tong += 1
                            if synth:
                                dau_synthetic += 1
    return {
        "tong_ky_tu": tong_ky_tu,
        "fffd": fffd,
        "dau_tong": dau_tong,
        "dau_synthetic": dau_synthetic,
        "synthetic_khoang_trang": synthetic_khoang_trang,
    }


def do_ngat_trang(doc: "fitz.Document", eps_bien=1.5, eps_x=3.0, eps_mau=0.02) -> dict:
    def gan(a, b, eps):
        return abs(a - b) <= eps

    def mau_gan(c1, c2, eps=eps_mau):
        if c1 is None or c2 is None:
            return c1 == c2
        return all(abs(a - b) <= eps for a, b in zip(c1, c2))

    theo_trang = []
    for i in range(doc.page_count):
        pg = doc[i]
        hinh = []
        for d in pg.get_drawings():
            to = d.get("fill")
            khung = d.get("rect")
            if to is None or khung is None:
                continue
            if khung.width < 20 or khung.height < 4:
                continue
            if khung.width >= pg.rect.width * 0.95 and khung.height >= pg.rect.height * 0.95:
                continue  # nen toan trang, khong phai the noi dung
            hinh.append((khung, to))
        theo_trang.append((pg.rect.height, hinh))

    trung = []
    for i in range(doc.page_count - 1):
        h, hinh = theo_trang[i]
        _, hinh2 = theo_trang[i + 1]
        cham_day = [(r, f) for r, f in hinh if gan(r.y1, h, eps_bien)]
        cham_dinh = [(r, f) for r, f in hinh2 if gan(r.y0, 0, eps_bien)]
        for r1, f1 in cham_day:
            for r2, f2 in cham_dinh:
                if gan(r1.x0, r2.x0, eps_x) and gan(r1.x1, r2.x1, eps_x) and mau_gan(f1, f2):
                    trung.append({"trang_a": i + 1, "trang_b": i + 2, "mau": list(f1)})
    return {"the_bi_cat": trung, "so_lan": len(trung)}


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"loi": "usage: pdf_checks.py <file.pdf>"}, ensure_ascii=False))
        return 2
    duong = sys.argv[1]
    if not os.path.exists(duong):
        print(json.dumps({"loi": f"khong tim thay file: {duong}"}, ensure_ascii=False))
        return 2

    doc = fitz.open(duong)
    text = "\n".join(doc[i].get_text() for i in range(doc.page_count))
    net_ve_theo_trang = [len(doc[i].get_drawings()) for i in range(doc.page_count)]
    ra = {
        "file": duong,
        "kich_thuoc_byte": os.path.getsize(duong),
        "so_trang": doc.page_count,
        "byte_moi_trang": os.path.getsize(duong) / doc.page_count if doc.page_count else None,
        "net_ve_theo_trang": net_ve_theo_trang,
        "net_ve_tong": sum(net_ve_theo_trang),
        "font": do_font(doc),
        "raster": do_raster(doc),
        "dau": do_dau(doc),
        "ngat_trang": do_ngat_trang(doc),
        "text": text,
        "text_bo_trang": "".join(text.split()),
    }
    doc.close()
    print(json.dumps(ra, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
