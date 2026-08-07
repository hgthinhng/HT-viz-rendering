import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "design-system" / "tokens.css"


def parse_css_root():
    """Gop TAT CA cac khoi :root tran (khong bat :root:not(...)).

    Fix round 2: ban truoc dung re.search nen CHI doc khoi :root DAU TIEN.
    Sau fix round 1, --shadow-1 va --shadow-hairline da doi hen sang khoi
    :root THU HAI, nen ban cu bo sot hai bien nay hoan toan (test_shadow_
    khong_co_blur khong con kiem chung gi cho --shadow-1). Dung lai dung
    regex ranh gioi cua test_khong_bien_nao_bi_khai_hai_lan_trong_root, vi
    test do da chung minh regex tach dung 2 khoi tran. Vong lap gan gia tri
    theo THU TU khoi trong file, nen khoi sau (n dung sau trong cascade khi
    cung specificity) se de len gia tri cua khoi truoc neu trung ten; test
    test_khong_bien_nao_bi_khai_hai_lan_trong_root da dam bao khong con
    truong hop trung ten nao, nen viec gop nay an toan.
    """
    text = CSS.read_text(encoding="utf-8")
    blocks = re.findall(r"(?<![\w\-\)\]])\:root\s*\{(.*?)\n\}", text, re.S)
    assert blocks, "khong tim thay khoi :root nao trong tokens.css"
    out = {}
    for body in blocks:
        for line in body.split("\n"):
            m = re.match(r"\s*--([a-z0-9-]+)\s*:\s*([^;]+);", line)
            if m:
                out[m.group(1)] = m.group(2).strip()
    return out


def test_css_co_du_12_mau():
    css = parse_css_root()
    expected = {
        "ink": "#051C2C",
        "ink-md": "#42566A",
        "ink-lo": "#8595A6",
        "line": "#DBE2EA",
        "paper": "#FFFFFF",
        "paper-hi": "#F7F9FC",
        "accent": "#2251FF",
        "accent-hi": "#1233B8",
        "accent-soft": "#7D9BFF",
        "warn": "#B07A10",
        "pos": "#008A6D",
        "neg": "#C22F4E",
    }
    for name, hexval in expected.items():
        assert name in css, f"thieu bien --{name} trong tokens.css"
        assert css[name].upper() == hexval.upper(), (
            f"--{name} lech: css={css[name]} mong doi={hexval}"
        )


def _chuan_hoa_khoang_trang(s):
    return re.sub(r"\s+", " ", s).strip()


def test_python_khop_css():
    """Fix round 2: ban truoc chi doi chieu COLORS. FONTS/SPACING/RADIUS/
    SHADOW khong duoc kiem gi, va FONTS thuc su da lech (thieu nhanh Noto,
    "sans" thua Arial). Mo rong de dung nghia Interfaces cua brief: "test
    ep hai ban luon khop", khong chi rieng mau.
    """
    import sys

    sys.path.insert(0, str(ROOT / "design-system"))
    import tokens

    css = parse_css_root()

    # Mau
    for name, hexval in tokens.COLORS.items():
        css_name = name.replace("_", "-")
        assert css_name in css, f"tokens.py co {name} nhung tokens.css khong co"
        assert css[css_name].upper() == hexval.upper(), (
            f"{name} lech giua hai ban: py={hexval} css={css[css_name]}"
        )

    # Font: --font-serif / --font-sans / --font-mono, so sau khi chuan hoa
    # khoang trang (CSS va Python co the khac nhau cho xuong dong).
    # Lay thang tu tokens.FONTS thay vi liet ke cung ba ten: ban cu bo sot
    # "display" vi no khong nam trong danh sach cung do.
    font_map = {k: f"font-{k}" for k in tokens.FONTS}
    for py_name, css_name in font_map.items():
        assert css_name in css, f"tokens.css khong co --{css_name}"
        assert _chuan_hoa_khoang_trang(tokens.FONTS[py_name]) == _chuan_hoa_khoang_trang(
            css[css_name]
        ), f"FONTS['{py_name}'] lech: py={tokens.FONTS[py_name]!r} css={css[css_name]!r}"

    # Spacing: --space-1 toi --space-8 theo dung thu tu trong SPACING
    for i, px in enumerate(tokens.SPACING, start=1):
        css_name = f"space-{i}"
        assert css_name in css, f"tokens.css khong co --{css_name}"
        assert css[css_name] == f"{px}px", (
            f"SPACING[{i - 1}] lech: py={px}px css={css[css_name]}"
        )

    # Radius: --radius-0 (khong don vi trong CSS goc) toi --radius-3
    radius_map = {"r0": "radius-0", "r1": "radius-1", "r2": "radius-2", "r3": "radius-3"}
    for py_name, css_name in radius_map.items():
        assert css_name in css, f"tokens.css khong co --{css_name}"
        gia_tri = tokens.RADIUS[py_name]
        mong_doi = "0" if gia_tri == 0 else f"{gia_tri}px"
        assert css[css_name] == mong_doi, (
            f"RADIUS['{py_name}'] lech: py={mong_doi} css={css[css_name]}"
        )

    # Shadow: --shadow-1/2/3/none/hairline, so sau khi chuan hoa khoang trang
    shadow_map = {
        "s1": "shadow-1",
        "s2": "shadow-2",
        "s3": "shadow-3",
        "none": "shadow-none",
        "hairline": "shadow-hairline",
    }
    for py_name, css_name in shadow_map.items():
        assert css_name in css, f"tokens.css khong co --{css_name}"
        assert _chuan_hoa_khoang_trang(tokens.SHADOW[py_name]) == _chuan_hoa_khoang_trang(
            css[css_name]
        ), f"SHADOW['{py_name}'] lech: py={tokens.SHADOW[py_name]!r} css={css[css_name]!r}"


def test_css_khop_python_chieu_nguoc():
    """Chieu CSS -> Python. test_python_khop_css chi di MOT CHIEU: no lap
    theo tokens.py roi tim trong CSS. Them mot bien MOI vao tokens.css ma
    quen tokens.py thi khong test nao do, va pipeline WeasyPrint se im lang
    thieu token do (dung chuan CSS thi trinh duyet van dep, ban PDF thi
    thieu). Ca da xay ra that o huong nguoc lai voi --space-6.

    Test nay lap theo CSS. No khong doi MOI bien CSS phai co trong Python,
    vi tokens.css con giu bien bo tro chi dung cho man hinh (vd --line-lo,
    --shadow-*). No doi dung CAC NHOM ma tokens.py tuyen bo la minh giu:
    mau, font, spacing, radius, shadow.
    """
    import sys

    sys.path.insert(0, str(ROOT / "design-system"))
    import tokens

    css = parse_css_root()

    # Nhom mau: moi bien mau trong CSS phai co trong COLORS, TRU danh sach
    # mien tru TUONG MINH duoi day. Danh sach tuong minh chu khong phai mot
    # regex "bo qua bien phu", vi mot regex se im lang nuot ca bien moi that
    # su thieu. Them mot mau moi vao tokens.css se lam test nay do, va nguoi
    # sua phai chon: dua vao tokens.py hay khai o day kem ly do.
    CHI_DUNG_TREN_CSS = {
        "paper-hair": "nen o rong/hatch, chi ve bang CSS",
        "paper-elev": "nen card noi khoi, chi ve bang CSS",
        "ink-faint": "bac nhat trang tri, chart Python khong dung",
        "line-lo": "duong ke nhat, chi ve bang CSS",
        "neg-soft": "hang so tinh tay thay color-mix, chi dung trong CSS",
    }
    py_colors = {name.replace("_", "-") for name in tokens.COLORS}
    thieu_mau = [
        f"--{ten} = {gt}"
        for ten, gt in css.items()
        if re.fullmatch(r"#[0-9A-Fa-f]{6}", gt.strip())
        and ten not in py_colors
        and ten not in CHI_DUNG_TREN_CSS
    ]
    assert not thieu_mau, (
        "tokens.css co bien mau ma tokens.py khong co, pipeline chart Python se thieu token: "
        + ", ".join(thieu_mau)
        + ". Them vao tokens.py, hoac khai vao CHI_DUNG_TREN_CSS kem ly do."
    )

    # Chieu con lai cua chinh danh sach mien tru: mot ten trong
    # CHI_DUNG_TREN_CSS ma khong con trong tokens.css nghia la danh sach da
    # muc. Khong bat cai nay thi mien tru cu tich lai mai va che mat bien that.
    mien_tru_chet = [t for t in CHI_DUNG_TREN_CSS if t not in css]
    assert not mien_tru_chet, (
        f"CHI_DUNG_TREN_CSS con {mien_tru_chet} nhung tokens.css khong con bien do, xoa khoi danh sach"
    )

    # Nhom font: --font-* trong CSS phai co trong FONTS.
    py_fonts = {f"font-{k}" for k in tokens.FONTS}
    thieu_font = [f"--{t}" for t in css if t.startswith("font-") and t not in py_fonts]
    assert not thieu_font, f"tokens.css co {thieu_font} ma tokens.py khong co"

    # Nhom spacing: so luong --space-N phai bang do dai SPACING. Neu CSS them
    # --space-9 thi day la cho bat.
    so_space = len([t for t in css if re.fullmatch(r"space-\d+", t)])
    assert so_space == len(tokens.SPACING), (
        f"tokens.css co {so_space} bien --space-N, tokens.py khai {len(tokens.SPACING)} muc"
    )

    # Nhom radius va shadow: dem tuong tu, chan chuyen them mot ben.
    so_radius = len([t for t in css if re.fullmatch(r"radius-\d+", t)])
    assert so_radius == len(tokens.RADIUS), (
        f"tokens.css co {so_radius} bien --radius-N, tokens.py khai {len(tokens.RADIUS)} muc"
    )
    so_shadow = len([t for t in css if re.fullmatch(r"shadow-[\w-]+", t)])
    assert so_shadow == len(tokens.SHADOW), (
        f"tokens.css co {so_shadow} bien --shadow-*, tokens.py khai {len(tokens.SHADOW)} muc"
    )


def _tach_lop_shadow(val: str) -> list[str]:
    """Tach cac LOP shadow theo dau phay o CAP NGOAI CUNG, bo qua dau phay nam
    trong ngoac.

    Ban cu dung thang `val.split(",")`, va chinh dieu do de ra mot luat cung
    rieng trong CLAUDE.md: "cu phap shadow dung rgba(R G B / A), khong dung dau
    phay trong ngoac". Luat do khong bao ve gi cho ban giao di ca; no ton tai
    chi de mot phep tach chuoi trong test nay chay dung. Vao mot ngay dep troi
    ai do viet rgba(R, G, B, A) theo dung chuan CSS thi test bao loi o cho khong
    co loi. Sua phep tach thi luat con do khong con ly do ton tai.
    """
    lop: list[str] = []
    sau = 0
    hien_tai: list[str] = []
    for ky_tu in val:
        if ky_tu == "(":
            sau += 1
        elif ky_tu == ")":
            sau -= 1
        if ky_tu == "," and sau == 0:
            lop.append("".join(hien_tai).strip())
            hien_tai = []
            continue
        hien_tai.append(ky_tu)
    con_lai = "".join(hien_tai).strip()
    if con_lai:
        lop.append(con_lai)
    return lop


def test_shadow_khong_co_blur():
    """Blur phai bang 0 cho HO shadow dang dung trong bao cao.

    Dinh chinh ly do, vi ly do cu ghi trong ban truoc la SAI ke tu khi doi
    engine: "bay raster khi in". Phep do de ra luat do chay tren Chromium in
    (chi blur > 0 moi bi nuong bitmap). Nhung engine PDF cua repo la
    WeasyPrint, va WeasyPrint KHONG VE box-shadow bang bat ky cu phap nao. Tuc
    blur=0 chua bao gio bao ve ban PDF giao di; no chi rang buoc ban trinh
    duyet, suot hai phase.

    Vay tai sao van giu? Vi mot ly do NHO HON va that: bao cao lan `pdf-so` van
    co the bi nguoi doc bam in tu trinh duyet, va luc do blur > 0 se bi nuong
    bitmap that. Do la rui ro thap nhung co that, va giu nguong 0 khong ton gi
    cho ho token hien tai.

    Cai KHONG con nua: quyen phu quyet cua luat nay len toan he. Ban thiet ke
    cu chot "shadow offset cung la ngon ngu do noi DUY NHAT cua toan he" dua
    tren phep do da het hieu luc. Lan `html-song` khong di qua WeasyPrint va
    khong ai bam in, nen no duoc dung thang do noi mem day du; token man-hinh
    rieng khai o day khi nao co nguoi dung that, dat ten `--shadow-man-*` de
    vong lap duoi nay khong cham toi.
    """
    css = parse_css_root()
    for name, val in css.items():
        if not name.startswith("shadow") or name.startswith("shadow-man-"):
            continue
        for p in _tach_lop_shadow(val):
            nums = re.findall(r"(-?\d+(?:\.\d+)?)px", p)
            assert len(nums) >= 3, f"--{name} thieu thanh phan: {p}"
            assert float(nums[2]) == 0.0, (
                f"--{name} co blur={nums[2]}px, phai bang 0. Ly do khong phai "
                f"WeasyPrint (no khong ve shadow gi ca) ma la ca nguoi doc bam "
                f"in tu trinh duyet. Can shadow mem thi khai --shadow-man-*"
            )


def test_khong_bien_nao_bi_khai_hai_lan_trong_root():
    """Hai khoi :root cung specificity thi khoi SAU thang. Bug that da gap:
    --space-6 khai 24px o khoi dau va 28px o khoi sau, gia tri render la 28px
    trong khi tokens.py khai 24px. Test cu chi doc khoi :root DAU TIEN nen
    bao xanh ma khong kiem gi.
    """
    text = CSS.read_text(encoding="utf-8")
    blocks = re.findall(r"(?<![\w\-\)\]])\:root\s*\{(.*?)\n\}", text, re.S)
    assert len(blocks) >= 1, "khong tim thay khoi :root nao"
    seen = {}
    for i, body in enumerate(blocks):
        for line in body.split("\n"):
            m = re.match(r"\s*--([a-z0-9-]+)\s*:\s*([^;]+);", line)
            if m:
                name = m.group(1)
                if name in seen:
                    raise AssertionError(
                        f"--{name} khai o khoi :root #{seen[name]} VA #{i}. "
                        f"Cung specificity nen khoi sau thang ngam, tokens.py se lech."
                    )
                seen[name] = i
