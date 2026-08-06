"""Fix round 3 (goc): bug lon glyph tieng Viet trong WeasyPrint.

fonts-embedded.css tung sinh HAI khoi @font-face cho MOI to hop
(family, style, weight) -- mot cho subset latin, mot cho subset vietnamese,
dung cach Google Fonts phuc vu qua mang. WeasyPrint khong chon dung subset
khi nhieu @font-face trung family/style/weight, dan toi LON GLYPH (khong
phai tofu, khong phai loi font-family ten tran da biet): ky tu "e^." (U+1EC7)
bi tra ra glyph cua "t", "nghe^." thanh "nght", "lie^.u" thanh "litu". Day la
loi toan ven du lieu o TANG TEXT cua PDF, khong chi loi hinh anh -- copy chu
tu PDF ra cung sai.

Fix round 4: ba lo them sau khi round 3 dong.
- G1: _parse_legacy_sources co the ghi de am tham neu Google tra ve nhieu
  hon 1 khoi cho cung to hop o nhanh UA cu. Da vao build-fonts.py, kiem lai
  bang test offline (khong can mang) o duoi.
- G2: round-trip cu chi phu 1/12 to hop (Spectral normal 400) va CHUOI_THU
  thieu han dau HUYEN. Da mo rong CHUOI_THU du 6 thanh + ă/â/đ/ê/ô/ơ/ư ca
  hoa lan thuong, va tham so hoa round-trip qua CA 12 to hop that (doc dong
  tu fonts-embedded.css, khong hard-code danh sach).
- G3: lap luan "kich thuoc gan nhu y het" o report round 3 la SAI cho ca
  file (chi do tay 1 to hop roi suy rong). Thay bang assert THAT: doi chieu
  cmap cua font da nhung voi cmap cua font GOC + tap unicode ky vong doc
  dong, khong con suy tu kich thuoc byte.

Fix round 6: thieu dau BIEN AM tieng Viet (mu U+0302, trang U+0306, moc
U+031B). Nam dau THANH (huyen/sac/nga/hoi/nang) thi co vi dung chung voi
Latin khac nen nam trong subset latin/latin-ext; ba dau bien am gan nhu chi
tieng Viet dung nen Google KHONG gan nhan trong unicode-range cua bat ky
subset nao, du font goc co du ca ba. Anh huong: van ban Unicode dang NFD
(chu nen + dau roi) se mat dau bien am; NFC (dang to hop san, pho bien hon)
thi khong sao. Da sua build-fonts.py ep them ca khoi Combining Diacritical
Marks (U+0300-036F) khi subset. Test moi o duoi: kiem cmap du 8 dau (offline,
khong can mang) va round-trip qua chinh van ban dang NFD.
"""
import base64
import importlib.util
import io
import re
import unicodedata
import urllib.request
from pathlib import Path

import fitz
import pytest
from fontTools.ttLib import TTFont
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[2]
FONTS_CSS = ROOT / "design-system" / "fonts" / "fonts-embedded.css"
BUILD_FONTS_PATH = ROOT / "design-system" / "fonts" / "build-fonts.py"

# Chuoi thu, fix round 4: ban truoc thieu han dau HUYEN (khong co a-huyen,
# o-huyen...). Chuoi nay du ca SAU thanh (ngang/huyen/sac/hoi/nga/nang, da
# tu kiem bang unicodedata truoc khi chot) va du ca 7 nguyen am/phu am co
# dau phu (ă â đ ê ô ơ ư) O CA DANG HOA LAN THUONG.
CHUOI_THU = (
    "Giá trị sổ sách hiện tại là 1.240 tỷ đồng, thấp hơn giá thị trường. "
    "Số liệu tại 06/2026, chiết khấu 14%, TRƯỢT ngưỡng, hấp dẫn từ vùng này, "
    "đường cong lợi suất phẳng dần. Ăn theo đà tăng, Âm thầm tích luỹ, "
    "Đầu tư dài hạn, Êm ả hơn dự báo, Ôn định dòng tiền, Ở mức hợp lý, "
    "Ưu tiên chất lượng."
)


def _chuan_hoa_khoang_trang(s):
    return re.sub(r"\s+", " ", s).strip()


def _load_build_fonts_module():
    """Nap build-fonts.py nhu mot module de tai su dung ham parse, khong
    chay lai main() (duoc bao ve boi if __name__ == "__main__"). Ten file
    co dau gach ngang nen khong import truc tiep duoc, phai qua importlib.
    """
    spec = importlib.util.spec_from_file_location("build_fonts_mod_test", BUILD_FONTS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _parse_font_face_that(text):
    """Chi khop khoi @font-face THAT (ngay sau dau { khong co khoang
    trang), tranh khop nham chu "@font-face" xuat hien trong comment giai
    thich dau file fonts-embedded.css.
    """
    return re.findall(
        r"@font-face\{font-family:'([^']+)';font-style:(\w+);font-weight:(\d+);"
        r"font-display:swap;src:url\(data:font/woff2;base64,([^)]+)\) format\('woff2'\);\}",
        text,
    )


_FONT_CSS_TEXT = FONTS_CSS.read_text(encoding="utf-8")
_BLOCKS = _parse_font_face_that(_FONT_CSS_TEXT)


def _render_va_doc_lai(font_css_text, family, style, weight, chuoi):
    """Dung mot trang HTML nap fonts-embedded.css, in `chuoi` bang dung
    family/style/weight duoc chi dinh, render PDF that bang WeasyPrint, doc
    lai tang text bang fitz (pymupdf), roi so sanh sau khi chuan hoa khoang
    trang (WeasyPrint co the ngat dong giua cau, fitz.get_text() chen "\\n"
    o cho ngat, khong phai loi glyph).
    """
    # @page phai RONG HON chieu dai chuoi thu o kho chu nay, khong chi rong
    # hon "body". Fix round 4: ban truoc chi dat width:1400px tren body ma
    # KHONG dat @page, trong khi trang mac dinh cua WeasyPrint la A4
    # (~793px ngang). Box rong hon trang bi CAT NGANG o mep trang (khong
    # phai ngat sang trang 2), lam MAT CHU that su -- trieu chung nhin
    # giong lon glyph nhung nguyen nhan la trang qua hep, khong phai font.
    # Da tai hien va xac nhan bang tay truoc khi sua: chuoi dai hon (them
    # dau huyen o G2) bi cat giua cau, vi du "06/202" roi nhay sang doan
    # sau. Dat @page rong 2400px de chua vua ca cau tren MOT dong.
    html = f"""
    <html><head><style>
    {font_css_text}
    @page {{ size: 2400px 500px; margin: 10px; }}
    body {{
      font-family: '{family}', serif;
      font-style: {style};
      font-weight: {weight};
      font-size: 20px;
    }}
    </style></head>
    <body><p>{chuoi}</p></body></html>
    """
    pdf_bytes = HTML(string=html).write_pdf()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    so_trang = doc.page_count
    text = doc[0].get_text()
    doc.close()
    return _chuan_hoa_khoang_trang(text), so_trang


@pytest.mark.parametrize(
    "fam,style,weight",
    [(b[0], b[1], b[2]) for b in _BLOCKS],
    ids=[f"{b[0]}-{b[1]}-{b[2]}" for b in _BLOCKS],
)
def test_font_khong_lon_glyph_qua_weasyprint(fam, style, weight):
    """Fix round 4 (G2): tham so hoa qua TAT CA to hop that trong
    fonts-embedded.css (doc dong, khong hard-code), khong chi rieng Spectral
    normal 400 nhu ban round 3. Khi do se biet CHINH XAC to hop nao hong
    thay vi mot test gop bao chung chung.

    Chan TRAN TRANG truoc khi so ky tu (theo goi y reviewer): mat chu do
    @page qua hep so voi chuoi thu (PDF paginated khong tu "cuon ngang" nhu
    trinh duyet, phan tran bi CAT chu khong ngat sang trang 2) nhin GIONG
    lon glyph nhung nguyen nhan hoan toan khac -- da tung gap that o chinh
    file nay khi CHUOI_THU dai ra o G2, xem lich su sua trong
    _render_va_doc_lai. Hai dau hieu KHONG duoc lan voi nhau:
      - so trang != 1, hoac chuoi doc duoc NGAN HON chuoi goc: nghi TRAN
        TRANG, khong phai loi font.
      - chuoi doc duoc CUNG DO DAI nhung KHAC noi dung: moi thuc su nghi
        LON GLYPH.
    """
    doc_duoc, so_trang = _render_va_doc_lai(_FONT_CSS_TEXT, fam, style, weight, CHUOI_THU)

    assert so_trang == 1, (
        f"'{fam}' style={style} weight={weight}: PDF ra {so_trang} trang, "
        f"ky vong 1. Day la dau hieu TRAN KHOI KHUNG TRANG (@page trong "
        f"_render_va_doc_lai qua hep so voi chuoi thu), KHONG PHAI loi lon "
        f"glyph. Dung di kiem test_moi_to_hop_font_chi_khai_dung_1_lan cho "
        f"truong hop nay."
    )
    if len(doc_duoc) < len(CHUOI_THU):
        raise AssertionError(
            f"'{fam}' style={style} weight={weight}: chuoi doc duoc NGAN "
            f"HON chuoi dua vao ({len(doc_duoc)} so voi {len(CHUOI_THU)} ky "
            f"tu). Day la dau hieu TRAN TRANG (mot doan giua hoac cuoi bi "
            f"cat mat, khong duoc render nen khong doc duoc), KHONG PHAI loi "
            f"lon glyph. Kiem tra @page trong _render_va_doc_lai co du rong "
            f"cho chuoi thu khong; DUNG di kiem test_moi_to_hop_font_chi_"
            f"khai_dung_1_lan cho truong hop nay.\n"
            f"doc duoc: {doc_duoc!r}\ndua vao : {CHUOI_THU!r}"
        )
    assert doc_duoc == CHUOI_THU, (
        f"Glyph lon khi render '{fam}' style={style} weight={weight} qua "
        f"WeasyPrint (chuoi doc duoc CUNG DO DAI voi ban goc nhung KHAC noi "
        f"dung, nen day la LON GLYPH that su, khong phai tran trang): doc "
        f"duoc {doc_duoc!r}, dua vao {CHUOI_THU!r}. Kiem tra fonts-embedded.css "
        f"co con khai hai @font-face cho cung mot to hop khong (xem "
        f"test_moi_to_hop_font_chi_khai_dung_1_lan)."
    )


def test_moi_to_hop_font_chi_khai_dung_1_lan():
    """Dieu kien cau truc: fonts-embedded.css khong duoc co hai khoi
    @font-face cho cung (family, style, weight). Bat loi ngay ca khi ai do
    tai sinh file bang ban build-fonts.py CU (tach subset latin/vietnamese),
    truoc khi can render thu de phat hien lon glyph.
    """
    assert _BLOCKS, "khong tim thay khoi @font-face nao trong fonts-embedded.css"
    seen = {}
    for fam, style, weight, _b64 in _BLOCKS:
        key = (fam, style, weight)
        seen[key] = seen.get(key, 0) + 1
    trung = {k: v for k, v in seen.items() if v > 1}
    assert not trung, (
        f"Cac to hop (family, style, weight) sau bi khai NHIEU HON 1 lan: "
        f"{trung}. Moi to hop chi duoc co dung mot @font-face, khong tach "
        f"subset latin/vietnamese rieng (xem docstring dau build-fonts.py)."
    )


def test_parse_legacy_sources_bat_duoc_trung_lap():
    """Fix round 4 (G1): _parse_legacy_sources() trong build-fonts.py phai
    NO khi CSS UA cu tra ve NHIEU HON 1 khoi @font-face cho cung mot to hop,
    khong duoc am tham chi giu URL cuoi cung (fallback im lang). Test offline,
    khong can mang, dung CSS gia lap trung lap.
    """
    bf = _load_build_fonts_module()
    css_trung = (
        "@font-face { font-family: 'Spectral'; font-style: normal; "
        "font-weight: 400; src: url(https://a.example/x.woff) format('woff'); }\n"
        "@font-face { font-family: 'Spectral'; font-style: normal; "
        "font-weight: 400; src: url(https://a.example/y.woff) format('woff'); }\n"
    )
    with pytest.raises(AssertionError, match="KHAC 1 khoi"):
        bf._parse_legacy_sources(css_trung)


def test_parse_legacy_sources_khong_bao_dong_gia_khi_dung_1_khoi():
    """Doi chung cua test tren: dung 1 khoi/to hop thi KHONG duoc bao dong,
    va URL doc ra phai dung."""
    bf = _load_build_fonts_module()
    css_dung = (
        "@font-face { font-family: 'Spectral'; font-style: normal; "
        "font-weight: 400; src: url(https://a.example/x.woff) format('woff'); }\n"
    )
    sources = bf._parse_legacy_sources(css_dung)
    assert sources == {("Spectral", "normal", "400"): "https://a.example/x.woff"}


def test_moi_to_hop_khong_mat_codepoint_so_voi_font_goc():
    """Fix round 4 (G3): report round 3 lap luan "dung luong gan nhu y het"
    bang cach chi do tay MOT to hop (Spectral 400 normal) roi suy rong cho
    ca file. Sai: IBM Plex Sans lech toi -40%. Thay lap luan do kich thuoc
    bang phep kiem TRUC TIEP tren noi dung glyph: voi moi to hop trong 12,
    giai ma base64 dang nhung, mo bang fontTools, doc cmap, doi chieu voi
    PHAN GIAO giua tap unicode ky vong (doc DONG tu Google Fonts CSS hien
    dai, khong hard-code) va cmap cua chinh font GOC (tai truc tiep qua UA
    cu). Khong doi hoi nhung gi font goc von khong co (do la gioi han cua
    Google, khong phai loi subset), chi bat truong hop subsetting lam RON
    glyph so voi chinh font goc da tai ve.

    Test nay CAN MANG. Neu that bai vi loi ket noi (urllib timeout/DNS...)
    chu khong phai AssertionError ve codepoint, do la van de moi truong,
    khong phai bug font. Doc thong bao loi that truoc khi ket luan.
    """
    bf = _load_build_fonts_module()
    modern_css = bf._fetch_css(bf.UA_MODERN)
    ranges = bf._parse_unicode_ranges(modern_css)
    legacy_css = bf._fetch_css(bf.UA_LEGACY)
    sources = bf._parse_legacy_sources(legacy_css)

    assert len(_BLOCKS) == 12, f"ky vong 12 to hop, thay {len(_BLOCKS)}"

    loi = []
    for fam, style, weight, b64 in _BLOCKS:
        key = (fam, style, weight)
        assert key in ranges, f"khong doc duoc tap unicode ky vong cho {key}"
        assert key in sources, f"khong tim thay font goc (UA cu) cho {key}"

        embedded_font = TTFont(io.BytesIO(base64.b64decode(b64)))
        embedded_cmap = set(embedded_font.getBestCmap().keys())

        req = urllib.request.Request(sources[key], headers={"User-Agent": bf.UA_LEGACY})
        goc_bytes = urllib.request.urlopen(req, timeout=20).read()
        goc_cmap = set(TTFont(io.BytesIO(goc_bytes)).getBestCmap().keys())

        ky_vong_that = ranges[key] & goc_cmap
        thieu = sorted(ky_vong_that - embedded_cmap)
        if thieu:
            loi.append((key, thieu))

    assert not loi, (
        f"Cac to hop sau THIEU codepoint so voi font goc (da subset RON "
        f"glyph so voi chinh nguon da tai ve): "
        f"{[(k, [hex(c) for c in v[:10]]) for k, v in loi]}"
    )


# Fix round 6: ten tieng Viet cho 8 dau ket hop can kiem, dung trong thong
# bao loi de nguoi doc log khong phai tra U+031B la dau gi. Nam dau dau la
# THANH (dung chung Latin khac), ba dau sau la BIEN AM (gan nhu chi tieng
# Viet dung, la trong tam cua round 6).
DAU_KET_HOP = {
    0x0300: "huyen",
    0x0301: "sac",
    0x0303: "nga",
    0x0309: "hoi",
    0x0323: "nang",
    0x0302: "mu, dung cho a-mu, e-mu, o-mu (chu la a, e, o co dau mu)",
    0x0306: "trang, dung cho a-trang (chu la a co dau trang)",
    0x031B: "moc, dung cho o-moc va u-moc (chu la o, u co dau moc)",
}


def test_moi_to_hop_du_dau_ket_hop_tieng_viet():
    """Fix round 6: unicode-range Google cong bo cho MOI subset (ke ca
    subset ten "vietnamese") khong liet ke U+0302 (mu), U+0306 (trang),
    U+031B (moc) -- ba dau BIEN AM phan biet "a e o u" voi "a e o u co dau
    bien am" (tuc "â ă ê ô ơ ư"), gan nhu chi tieng Viet dung nen khong nam
    trong subset nao Google cong bo, DU FONT GOC CO DU CA BA (da verify
    bang tay qua fontTools truoc khi sua build-fonts.py). Nam dau THANH thi
    co vi dung chung voi Latin khac. Test nay kiem TRUC TIEP tren file da
    nhung, offline, khong can mang -- re va nen chay moi lan, khong doi hoi
    render PDF.
    """
    loi = []
    for fam, style, weight, b64 in _BLOCKS:
        cmap = set(TTFont(io.BytesIO(base64.b64decode(b64))).getBestCmap().keys())
        thieu = [f"U+{cp:04X} ({ten})" for cp, ten in DAU_KET_HOP.items() if cp not in cmap]
        if thieu:
            loi.append(((fam, style, weight), thieu))
    assert not loi, (
        f"Cac to hop sau THIEU dau ket hop tieng Viet trong cmap (van ban "
        f"Unicode dang NFD, chu nen + dau roi, se mat dau khi gap to hop "
        f"nay): {loi}"
    )


def test_font_nfd_khong_mat_dau_bien_am():
    """Fix round 6: van ban Unicode dang NFD (chu nen + dau ket hop roi,
    gap khi copy tu macOS, tu PDF cu, hoac mot so API) phai giu dung dau
    bien am khi render qua WeasyPrint, khong chi dang NFC (to hop san) da
    test o test_font_khong_lon_glyph_qua_weasyprint.

    QUAN TRONG: hanh vi tang text voi input NFD KHONG CO DINH -- neu MOT
    font du glyph ve ca cum (dung truong hop o day, sau round 6) thi
    HarfBuzz co the tai to hop ve NFC khi xuat text layer; neu phai dung
    NHIEU font thi giu nguyen NFD. Vi vay PHAI chuan hoa CA HAI ve VE CUNG
    MOT DANG (NFC) truoc khi so, neu khong test se do gia tuy may/tuy ban
    HarfBuzz.
    """
    chuoi_nfc = "Tu khoa: ăn, âu, đêm, hôm, mơ, ưu."
    chuoi_nfd = unicodedata.normalize("NFD", chuoi_nfc)
    assert chuoi_nfd != chuoi_nfc, "chuoi thu chua co dau bien am nao de NFD hoa, sua lai chuoi"

    doc_duoc, so_trang = _render_va_doc_lai(_FONT_CSS_TEXT, "Spectral", "normal", "400", chuoi_nfd)

    assert so_trang == 1, (
        f"PDF ra {so_trang} trang, ky vong 1. Nghi TRAN TRANG, khong phai "
        f"loi mat dau NFD."
    )

    doc_duoc_nfc = unicodedata.normalize("NFC", doc_duoc)
    ky_vong_nfc = unicodedata.normalize("NFC", chuoi_nfc)
    assert doc_duoc_nfc == ky_vong_nfc, (
        f"Van ban dang NFD bi mat dau bien am khi render qua WeasyPrint "
        f"(da chuan hoa ca hai ve NFC truoc khi so, nen day khong phai do "
        f"khac bieu dien NFC/NFD): doc duoc {doc_duoc_nfc!r}, ky vong "
        f"{ky_vong_nfc!r}. Kiem tra build-fonts.py co con ep COMBINING_"
        f"DIACRITICS khi subset khong (xem "
        f"test_moi_to_hop_du_dau_ket_hop_tieng_viet)."
    )
