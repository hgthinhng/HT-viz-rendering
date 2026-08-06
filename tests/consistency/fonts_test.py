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
Marks (U+0300-036F) khi subset.

Round 6 bo sung (H1, H2), tu re-review:
- H1: ca lop phong ve 2 cua G1 (trong build-fonts.py) lan test
  test_moi_to_hop_khong_mat_codepoint_so_voi_font_goc tinh ky vong bang
  `ranges[key] & goc_cmap`, ma `ranges[key]` DEN TU chinh unicode-range
  Google cong bo -- tuc kiem dau ra bang chinh nguon tao ra dau ra, GROUND
  TRUTH VONG TRON. Bang chung: ba dau bien am thieu o CA 12 to hop nhung
  hai lop do van xanh 16/16 va 34/34 tren dung file dang thieu chung, vi
  ca hai deu hoi Google xem Google co dung khong. Da dung DAC_TA_TIENG_
  VIET_DOC_LAP (134 ky tu NFC + 8 dau ket hop + ASCII co ban, sinh bang
  Python, KHONG di qua unicode-range Google) lam ground truth that.
  test_moi_to_hop_khong_mat_codepoint_so_voi_font_goc VAN GIU LAI vi van
  huu ich (bat subsetting lam rot thu Google DA cong bo), nhung CHI bao
  dam dieu do, KHONG bao dam du tieng Viet -- xem comment tai cho khai bao.
- H2: test_moi_to_hop_khong_mat_codepoint_so_voi_font_goc can mang de tai
  font goc. Truoc chi DAN nguoi doc tu phan biet loi mang, khong phai co
  che that; tren may offline no ném URLError va hien ra ERROR (khong phai
  SKIPPED), lam ca `pytest tests/` do khi chay tu shell moi khong co mang.
  Da boc rieng loi ket noi (urllib.error.URLError/TimeoutError/
  ConnectionError) va goi pytest.skip(), KHONG bat Exception chung chung
  (se giau loi that). Bo sung: HTTPError la lop con cua URLError nen phai
  bat RIENG va cho FAILED (Google doi API/chan scrape thi phai bao, khong
  duoc coi la "offline").

Round 6 bo sung tiep (do duoc them 3 nhom ky hieu bao cao tai chinh thieu
o 12/12 to hop): dau cong tru/so sanh/mui ten (U+00B1/2264/2265/2260/2191/
2193) co o CA BA ho font nen da them vao DAC_TA_TIENG_VIET_DOC_LAP (dac ta
cung). Delta hoa/tam giac/Hy Lap thuong KHONG the phu dong deu 3 ho font
(gioi han tai san font Google, khong phai loi subset -- da do bang tay
tren font goc truoc khi ket luan), nen kiem RIENG bang
test_ky_hieu_hy_lap_tam_giac_dat_dung_tran_theo_ho_font, assert dung tran
da do thay vi doi hoi 100% khong dat duoc.
"""
import base64
import importlib.util
import io
import re
import socket
import unicodedata
import urllib.error
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

    GIOI HAN PHAM VI (H1, tu re-review round 6): tap "ky vong" o day tinh
    tu `ranges[key]`, tuc CHINH unicode-range Google cong bo. Test nay chi
    bao dam "khong lam rot thu Google DA CONG BO", KHONG bao dam "du tieng
    Viet can" -- day la GROUND TRUTH VONG TRON, tung de lot 3 dau bien am
    (U+0302/0306/031B) ma Google khong gan nhan o BAT KY subset nao du font
    goc co du. Ground truth THAT, doc lap voi Google, nam o
    test_moi_to_hop_du_dac_ta_tieng_viet_doc_lap ben duoi (offline, khong
    can mang). Giu test nay lai vi van huu ich cho MUC DICH RIENG cua no:
    phat hien subsetting tu lam rot du lieu so voi chinh nguon da tai ve.

    Test nay CAN MANG (H2, tu re-review round 6): boc rieng loi KET NOI
    (URLError/TimeoutError/socket.timeout), goi pytest.skip() khi gap, de
    khong lam do oan ca bo `pytest tests/` tren shell offline (nghiem thu
    Phase 1 doi chay sach tu shell moi, khong ai bao dam shell do co mang).
    KHONG bat Exception chung chung o day, chi bat dung loi mang, de loi
    that (vi du AssertionError ve codepoint) van hien ra la FAILED.

    H2 bo sung (tu re-review tiep theo): `urllib.error.HTTPError` la lop
    con cua `URLError`, nen neu bat chung se SKIP ca truong hop Google tra
    ve 403/404 (doi hop dong API, chan scrape UA cu...) -- do la im lang
    SAI CHO: loi ket noi thuan tuy (khong mang, DNS chet, timeout) thi skip
    dung, con Google THAY DOI API thi phai FAILED de nguoi doc biet, khong
    duoc coi la "offline". Bat rieng HTTPError TRUOC (thu tu except quan
    trong vi no la lop con) va cho no lan ra FAILED, khong skip.
    """
    bf = _load_build_fonts_module()
    try:
        modern_css = bf._fetch_css(bf.UA_MODERN)
        ranges = bf._parse_unicode_ranges(modern_css)
        legacy_css = bf._fetch_css(bf.UA_LEGACY)
        sources = bf._parse_legacy_sources(legacy_css)
    except urllib.error.HTTPError as e:
        raise AssertionError(
            f"Google Fonts CSS API tra ve loi HTTP {e.code} ({e.reason}). Day co the "
            f"la Google da doi hop dong API hoac chan UA cu dang dung, KHONG PHAI loi "
            f"mang don thuan, nen KHONG duoc skip: {e!r}"
        ) from e
    except (urllib.error.URLError, socket.timeout, ConnectionError) as e:
        pytest.skip(f"can mang de tai font goc/CSS Google Fonts, bo qua khi offline: {e!r}")

    assert len(_BLOCKS) == 12, f"ky vong 12 to hop, thay {len(_BLOCKS)}"

    loi = []
    for fam, style, weight, b64 in _BLOCKS:
        key = (fam, style, weight)
        assert key in ranges, f"khong doc duoc tap unicode ky vong cho {key}"
        assert key in sources, f"khong tim thay font goc (UA cu) cho {key}"

        embedded_font = TTFont(io.BytesIO(base64.b64decode(b64)))
        embedded_cmap = set(embedded_font.getBestCmap().keys())

        try:
            req = urllib.request.Request(sources[key], headers={"User-Agent": bf.UA_LEGACY})
            goc_bytes = urllib.request.urlopen(req, timeout=20).read()
        except urllib.error.HTTPError as e:
            raise AssertionError(
                f"{key}: tai font goc tra ve loi HTTP {e.code} ({e.reason}), KHONG "
                f"PHAI loi mang don thuan, nen KHONG duoc skip: {e!r}"
            ) from e
        except (urllib.error.URLError, socket.timeout, ConnectionError) as e:
            pytest.skip(f"can mang de tai font goc/CSS Google Fonts, bo qua khi offline: {e!r}")
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


# Fix round 6 (H1, tu re-review): DAC TA TIENG VIET DOC LAP voi metadata
# Google. Ca lop phong ve 2 cua G1 lan test_moi_to_hop_khong_mat_codepoint_
# so_voi_font_goc deu tinh ky vong tu `ranges[key]` (chinh unicode-range
# Google cong bo) -- kiem dau ra bang nguon tao ra dau ra, GROUND TRUTH
# VONG TRON, da chung minh la co that: ba dau bien am thieu o CA 12 to hop
# nhung hai lop do van xanh vi Google cung "khong biet" no thieu. Dac ta
# duoi day KHONG di qua bat ky ham nao cua build-fonts.py, chi hoi thang
# "tieng Viet CAN gi": 134 ky tu NFC (67 chu thuong + 67 chu hoa, sinh
# bang Python tu nguyen am/phu am ghep voi 5 thanh va 3 dau bien am, KHONG
# go tay de khoi sot/sai), 8 dau ket hop, va ASCII in duoc co ban.
_5_THANH = [0x0300, 0x0301, 0x0309, 0x0303, 0x0323]  # huyen sac hoi nga nang
_3_BIEN_AM = [0x0302, 0x0306, 0x031B]  # mu trang moc

TEN_DAU_KET_HOP = {
    0x0300: "huyen",
    0x0301: "sac",
    0x0303: "nga",
    0x0309: "hoi",
    0x0323: "nang",
    0x0302: "mu, dung cho a-mu, e-mu, o-mu (chu la a, e, o co dau mu)",
    0x0306: "trang, dung cho a-trang (chu la a co dau trang)",
    0x031B: "moc, dung cho o-moc va u-moc (chu la o, u co dau moc)",
}


def _sinh_67_ky_tu_thuong_nfc_tieng_viet():
    """Sinh 66 trong 67 ky tu tieng Viet thuong dang NFC to hop san bang
    unicodedata.normalize (khong go tay tung ky tu de khoi sot/sai): nam
    nguyen am/phu am mang duoc dau thanh truc tiep (a e i o u y) x 5 thanh,
    sau do sau to hop nguyen-am-co-dau-bien-am (a-mu, a-trang, e-mu, o-mu,
    o-moc, u-moc) x (chinh no + 5 thanh tren no). Rieng "d" co gach ngang
    (dd) PHAI go tay truc tiep vi no la U+0111, mot chu cai doc lap trong
    Unicode, KHONG tach duoc thanh chu nen cong dau ket hop nhu 66 ky tu
    con lai (khong co "d" + dau gach nao de NFC to hop). Da doi chieu bang
    tay voi danh sach 67 ky tu tieng Viet chuan (a a-thanh, a-trang(+thanh),
    a-mu(+thanh), d-gach, e-thanh, e-mu(+thanh), i-thanh, o-thanh,
    o-mu(+thanh), o-moc(+thanh), u-thanh, u-moc(+thanh), y-thanh) truoc khi
    dua vao dac ta, khop 100%.
    """

    def nfc(codepoints):
        return unicodedata.normalize("NFC", "".join(chr(c) for c in codepoints))

    ket_qua = []
    da_them = set()

    def them(c):
        if c not in da_them:
            da_them.add(c)
            ket_qua.append(c)

    for goc in "aeiouy":
        for thanh in _5_THANH:
            them(nfc([ord(goc), thanh]))

    for goc, bien_am in [("a", 0x0306), ("a", 0x0302), ("e", 0x0302), ("o", 0x0302), ("o", 0x031B), ("u", 0x031B)]:
        them(nfc([ord(goc), bien_am]))
        for thanh in _5_THANH:
            them(nfc([ord(goc), bien_am, thanh]))

    them("đ")

    assert len(ket_qua) == 67, f"sinh duoc {len(ket_qua)} ky tu thuong, ky vong 67"
    return ket_qua


# Fix round 6 (tiep, tu do dac controller): sau khoi dau bien am, do them
# sau nhom ky hieu bao cao tai chinh tieng Viet dung THAT. Ba nhom dau (tien
# dong, ngoac kep cong, cham lung) da co san trong ASCII/quotes hien co,
# khong can them. Ba nhom sau THIEU o 12/12 to hop (chua tung duoc yeu cau
# subset). Trong do CHI sau ky hieu nay co o CA BA ho font (da do bang tay
# tren font goc, xem FINANCIAL_SYMBOLS trong build-fonts.py), nen chi dua
# dung sau ky hieu nay vao dac ta CUNG (moi to hop deu phai co): dau cong
# tru (khoang tin cay/bien sai so), >= <= != (nguong covenant/kill-switch),
# mui ten len/xuong (xu huong trong bang so). Delta hoa, tam giac len/xuong,
# va Hy Lap thuong (alpha beta sigma rho, dung cho do bien dong/tuong quan)
# la tu vung that nhung KHONG the phu dong deu 3 ho font (gioi han tai san
# font cua Google, khong phai loi subset) nen KHONG dua vao dac ta cung o
# day -- xem test_ky_hieu_hy_lap_tam_giac_dat_dung_tran_theo_ho_font ben
# duoi, kiem rieng theo dung tran da do duoc.
KY_HIEU_TAI_CHINH_PHO_QUAT = {
    0x00B1: "cong tru, dung cho khoang tin cay va bien sai so",
    0x2264: "nho hon hoac bang, dung cho nguong covenant/kill-switch",
    0x2265: "lon hon hoac bang, dung cho nguong covenant/kill-switch",
    0x2260: "khac, dung cho dieu kien loai tru",
    0x2191: "mui ten len, xu huong tang trong bang so",
    0x2193: "mui ten xuong, xu huong giam trong bang so",
}


def _sinh_dac_ta_tieng_viet_doc_lap():
    """Tra ve tap codepoint: 134 ky tu NFC tieng Viet (67 thuong + 67 hoa),
    8 dau ket hop, ASCII in duoc (U+0020-007E: chu, so, dau cau bao cao
    tai chinh), va 6 ky hieu bao cao tai chinh pho quat (xem
    KY_HIEU_TAI_CHINH_PHO_QUAT). Doc lap hoan toan voi build-fonts.py/
    Google Fonts CSS.
    """
    thuong = _sinh_67_ky_tu_thuong_nfc_tieng_viet()
    hoa = [c.upper() for c in thuong]
    tat_ca_134 = thuong + hoa
    assert len(set(tat_ca_134)) == 134, f"dac ta co {len(set(tat_ca_134))} ky tu doc nhat, ky vong 134"

    cp = {ord(c) for c in tat_ca_134}
    cp.update(_5_THANH)
    cp.update(_3_BIEN_AM)
    cp.update(range(0x20, 0x7F))  # ASCII in duoc
    cp.update(KY_HIEU_TAI_CHINH_PHO_QUAT)
    return cp


DAC_TA_TIENG_VIET_DOC_LAP = _sinh_dac_ta_tieng_viet_doc_lap()


def _ten_codepoint(c):
    if c in TEN_DAU_KET_HOP:
        return TEN_DAU_KET_HOP[c]
    if c in KY_HIEU_TAI_CHINH_PHO_QUAT:
        return KY_HIEU_TAI_CHINH_PHO_QUAT[c]
    try:
        return unicodedata.name(chr(c))
    except ValueError:
        return "khong xac dinh"


def test_moi_to_hop_du_dac_ta_tieng_viet_doc_lap():
    """Fix round 6 (H1): GROUND TRUTH THAT, thay the ban
    test_moi_to_hop_du_dau_ket_hop_tieng_viet ban dau (chi kiem 8 dau ket
    hop) bang mot dac ta rong hon va DOC LAP voi Google:
    DAC_TA_TIENG_VIET_DOC_LAP (134 ky tu NFC + 8 dau ket hop + ASCII co
    ban + 6 ky hieu bao cao tai chinh pho quat, sinh bang Python o tren,
    khong hard-code danh sach tay va khong di qua unicode-range Google
    cong bo o buoc nao). Day la phep kiem KHONG THE xanh rong nhu ca lop
    phong ve 2 cua G1 lan test_moi_to_hop_khong_mat_codepoint_so_voi_
    font_goc tung xanh rong khi thieu 3 dau bien am, vi no khong hoi
    Google, no hoi "tieng Viet can gi". Offline, khong can mang, khong
    can render PDF -- re, nen chay moi lan.

    CHI dua vao day nhung gi da xac nhan co o CA BA ho font (do bang tay
    tren font goc truoc khi chon, xem FINANCIAL_SYMBOLS trong
    build-fonts.py). Delta hoa, tam giac, Hy Lap thuong KHONG dua vao day
    vi khong the dat 100% bang subsetting -- xem
    test_ky_hieu_hy_lap_tam_giac_dat_dung_tran_theo_ho_font.
    """
    loi = []
    for fam, style, weight, b64 in _BLOCKS:
        cmap = set(TTFont(io.BytesIO(base64.b64decode(b64))).getBestCmap().keys())
        thieu_cp = sorted(DAC_TA_TIENG_VIET_DOC_LAP - cmap)
        if thieu_cp:
            thieu_ten = [f"U+{c:04X} ({_ten_codepoint(c)})" for c in thieu_cp[:15]]
            loi.append(((fam, style, weight), len(thieu_cp), thieu_ten))
    assert not loi, (
        f"Cac to hop sau THIEU codepoint so voi dac ta tieng Viet DOC LAP "
        f"(khong qua metadata Google, gom 134 ky tu NFC + 8 dau ket hop + "
        f"ASCII + 6 ky hieu tai chinh pho quat): {loi}"
    )


# Fix round 6 (tiep): Delta hoa, tam giac len/xuong, va Hy Lap thuong
# (alpha beta sigma rho, dung cho do bien dong/tuong quan/muc thay doi) la
# tu vung that cua bao cao tai chinh, nhung KHONG THE phu dong deu ca 3 ho
# font vi GIOI HAN TAI SAN FONT cua Google (da do bang tay tren font goc
# CHUA subset, khong phai loi build-fonts.py): Spectral va IBM Plex Mono
# KHONG CO glyph Hy Lap thuong; IBM Plex Mono cung khong co Delta hoa; ca
# ba ho deu khong co tam giac tru rieng Spectral. Mot dac ta doi hoi 100%
# cho ca 12 to hop se KHONG BAO GIO xanh duoc bang subsetting -- fontTools
# khong the sinh glyph tu khong. Test duoi day assert DUNG BANG TRAN da do
# (khong hon khong kem), de bat REGRESSION neu ai do vo tinh lam MAT THEM
# nhung gi dang co, ma khong doi hoi dieu subsetting khong lam duoc. Muon
# phu Hy Lap thuong dong deu ca 3 ho thi phai DOI NGUON FONT, ngoai pham
# vi mot task subsetting.
_TEN_KY_HIEU_GIOI_HAN = {
    0x0394: "Delta hoa, muc thay doi",
    0x25B2: "tam giac len, xu huong tang",
    0x25BC: "tam giac xuong, xu huong giam",
    0x03B1: "alpha thuong",
    0x03B2: "beta thuong",
    0x03C3: "sigma thuong, do bien dong",
    0x03C1: "rho thuong, he so tuong quan",
}

TRAN_KY_HIEU_THEO_HO_FONT = {
    "Spectral": {0x0394, 0x25B2, 0x25BC},
    "IBM Plex Mono": set(),
    "IBM Plex Sans": {0x0394, 0x03B1, 0x03B2, 0x03C3, 0x03C1},
}


def test_ky_hieu_hy_lap_tam_giac_dat_dung_tran_theo_ho_font():
    """Fix round 6 (tiep): xem giai thich day du o comment ngay tren.
    Assert cmap cua moi to hop khop CHINH XAC voi TRAN_KY_HIEU_THEO_HO_FONT
    (khong thieu, cung khong bao gio "thua" vi thua nghia la font goc cua
    Google da duoc bo sung glyph, luc do phai CAP NHAT bang tran nay).
    """
    loi = []
    for fam, style, weight, b64 in _BLOCKS:
        cmap = set(TTFont(io.BytesIO(base64.b64decode(b64))).getBestCmap().keys())
        tran = TRAN_KY_HIEU_THEO_HO_FONT.get(fam)
        assert tran is not None, f"chua biet tran ky hieu cho ho font {fam!r}, cap nhat TRAN_KY_HIEU_THEO_HO_FONT"
        co_that = {cp for cp in _TEN_KY_HIEU_GIOI_HAN if cp in cmap}
        if co_that != tran:
            thieu = sorted(tran - co_that)
            thua = sorted(co_that - tran)
            loi.append((
                (fam, style, weight),
                [f"U+{c:04X} ({_TEN_KY_HIEU_GIOI_HAN[c]})" for c in thieu],
                [f"U+{c:04X} ({_TEN_KY_HIEU_GIOI_HAN[c]})" for c in thua],
            ))
    assert not loi, (
        f"Cac to hop sau LECH so voi tran da do (cot 2 = thieu so voi tran, tuc "
        f"REGRESSION that; cot 3 = thua so voi tran, tuc tin tot, can cap nhat "
        f"TRAN_KY_HIEU_THEO_HO_FONT): {loi}"
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
        f"test_moi_to_hop_du_dac_ta_tieng_viet_doc_lap)."
    )
