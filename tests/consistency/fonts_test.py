"""Fix round 3: bug lon glyph tieng Viet trong WeasyPrint.

fonts-embedded.css tung sinh HAI khoi @font-face cho MOI to hop
(family, style, weight) -- mot cho subset latin, mot cho subset vietnamese,
dung cach Google Fonts phuc vu qua mang. WeasyPrint khong chon dung subset
khi nhieu @font-face trung family/style/weight, dan toi LON GLYPH (khong
phai tofu, khong phai loi font-family ten tran da biet): ky tu "e^." (U+1EC7)
bi tra ra glyph cua "t", "nghe^." thanh "nght", "lie^.u" thanh "litu". Day la
loi toan ven du lieu o TANG TEXT cua PDF, khong chi loi hinh anh -- copy chu
tu PDF ra cung sai.

Test nay la ROUND-TRIP qua chinh WeasyPrint (engine PDF da chot cua repo,
khong phai Chromium), vi moi test khac trong repo deu chi chay qua Chromium
nen chua bao gio cham duoc loi nay.
"""
import re
from pathlib import Path

import fitz
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
FONTS_CSS = ROOT / "design-system" / "fonts" / "fonts-embedded.css"

# Chuoi thu: du dau kho (nguyen am doi, to hop dau sac/nang/hoi/nga, chu hoa
# co dau) -- danh sach ky tu goi y tu chinh nguoi phat hien bug.
CHUOI_THU = "tưởng ổn nghệ kể, Số liệu tại 06/2026, chiết khấu 14%, TRƯỢT hấp dẫn GIÁ TRỊ"


def _chuan_hoa_khoang_trang(s):
    return re.sub(r"\s+", " ", s).strip()


def _render_va_doc_lai(font_css_text, chuoi):
    """Dung mot trang HTML nap fonts-embedded.css, in CHUOI_THU bang font
    Spectral, render PDF that bang WeasyPrint, doc lai tang text bang fitz
    (pymupdf), roi so sanh sau khi chuan hoa khoang trang (WeasyPrint co the
    ngat dong giua cau, fitz.get_text() chen "\\n" o cho ngat, khong phai
    loi glyph).
    """
    html = f"""
    <html><head><style>
    {font_css_text}
    body {{ font-family: 'Spectral', serif; font-size: 20px; width: 1400px; }}
    </style></head>
    <body><p>{chuoi}</p></body></html>
    """
    pdf_bytes = HTML(string=html).write_pdf()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = doc[0].get_text()
    doc.close()
    return _chuan_hoa_khoang_trang(text)


def test_font_khong_lon_glyph_qua_weasyprint():
    font_css_text = FONTS_CSS.read_text(encoding="utf-8")
    doc_duoc = _render_va_doc_lai(font_css_text, CHUOI_THU)
    assert doc_duoc == CHUOI_THU, (
        f"Glyph lon khi render qua WeasyPrint: doc duoc {doc_duoc!r}, "
        f"dua vao {CHUOI_THU!r}. Kiem tra fonts-embedded.css co con khai "
        f"hai @font-face cho cung mot to hop (family, style, weight) khong "
        f"(xem test_moi_to_hop_font_chi_khai_dung_1_lan)."
    )


def test_moi_to_hop_font_chi_khai_dung_1_lan():
    """Dieu kien cau truc: fonts-embedded.css khong duoc co hai khoi
    @font-face cho cung (family, style, weight). Bat loi ngay ca khi ai do
    tai sinh file bang ban build-fonts.py CU (tach subset latin/vietnamese),
    truoc khi can render thu de phat hien lon glyph.
    """
    text = FONTS_CSS.read_text(encoding="utf-8")
    # Chi khop khoi @font-face THAT (ngay sau dau { khong co khoang trang),
    # tranh khop nham chu "@font-face" xuat hien trong comment giai thich.
    blocks = re.findall(
        r"@font-face\{font-family:'([^']+)';font-style:(\w+);font-weight:(\d+);[^}]+\}",
        text,
    )
    assert blocks, "khong tim thay khoi @font-face nao trong fonts-embedded.css"
    seen = {}
    for fam, style, weight in blocks:
        key = (fam, style, weight)
        seen[key] = seen.get(key, 0) + 1
    trung = {k: v for k, v in seen.items() if v > 1}
    assert not trung, (
        f"Cac to hop (family, style, weight) sau bi khai NHIEU HON 1 lan: "
        f"{trung}. Moi to hop chi duoc co dung mot @font-face, khong tach "
        f"subset latin/vietnamese rieng (xem docstring dau build-fonts.py)."
    )
