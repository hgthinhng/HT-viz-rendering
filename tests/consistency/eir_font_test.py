import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EIR = ROOT / "charts" / "matplotlib"

VIET_TEST = "Số liệu tại 06/2026 · chiết khấu 14% · Nguồn: BCTC"

# Chuoi dau chong phuc tap, dung rieng cho test phu cmap: khong chi dau don ma
# ca dau tren nguyen am hoa (TRUONG hoa: TRUOT, GIA TRI) va dau doi (hap dan).
HARD_MIXED_DIACRITICS = (
    "Số liệu tại 06/2026, chiết khấu 14%, Nguồn: BCTC. TRƯỢT, hấp dẫn, GIÁ TRỊ"
)


def test_khong_hardcode_liberation2():
    src = (EIR / "_eir_style.py").read_text(encoding="utf-8")
    assert "liberation2" not in src, (
        "con hardcode duong dan 'liberation2', thu muc that la 'liberation' "
        "-> os.path.exists tra False -> roi tu do ve DejaVu -> mat dau tieng Viet"
    )


def test_setup_fonts_tra_ve_list_ket_thuc_generic():
    sys.path.insert(0, str(EIR))
    import _eir_style

    sans, mono = _eir_style.setup_fonts()
    assert isinstance(sans, list), f"sans phai la list, dang la {type(sans)}"
    assert isinstance(mono, list), f"mono phai la list, dang la {type(mono)}"
    assert sans[-1] in ("sans-serif", "serif"), f"sans khong ket thuc generic: {sans}"
    assert mono[-1] == "monospace", f"mono khong ket thuc generic: {mono}"


def test_render_khong_canh_bao_thieu_glyph():
    script = f"""
import sys, warnings
sys.path.insert(0, {str(EIR)!r})
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
import _eir_style
sans, mono = _eir_style.setup_fonts()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.text(0.05, 0.5, {VIET_TEST!r}, fontfamily=sans, fontsize=12)
    ax.set_axis_off()
    fig.savefig("/dev/null", format="svg")
    plt.close(fig)
missing = [str(w.message) for w in caught if "missing from font" in str(w.message)]
print("MISSING:", len(missing))
for m in missing[:3]:
    print("  ", m)
"""
    out = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=120
    )
    assert "MISSING: 0" in out.stdout, (
        f"con canh bao thieu glyph -> se ra tofu:\n{out.stdout}\n{out.stderr}"
    )


def test_svg_giu_text_that_khong_bien_thanh_path():
    script = f"""
import sys
sys.path.insert(0, {str(EIR)!r})
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
import _eir_style
sans, mono = _eir_style.setup_fonts()
fig, ax = plt.subplots(figsize=(6, 2))
ax.text(0.05, 0.5, {VIET_TEST!r}, fontfamily=sans, fontsize=12)
ax.set_axis_off()
fig.savefig("/tmp/eir_font_check.svg", format="svg")
plt.close(fig)
"""
    subprocess.run([sys.executable, "-c", script], check=True, timeout=120)
    svg = Path("/tmp/eir_font_check.svg").read_text(encoding="utf-8")
    assert "<text" in svg, "svg.fonttype khong phai 'none', chu da bien thanh path"
    assert "chiết khấu" in svg, "chu tieng Viet khong con nguyen ven trong SVG"
    assert "<image" not in svg, "SVG nhung anh raster"


def test_font_dau_tien_phu_het_codepoint_khong_tach_roi():
    """Bit lo o cho nguy hiem nhat: test_render_khong_canh_bao_thieu_glyph chi bat
    duoc canh bao "missing from font", tuc chi bat duoc ca O VUONG TOFU. Loi DAU
    TACH ROI xay ra khi matplotlib chon FONT KHAC NHAU cho tung ky tu trong CUNG
    mot chuoi (per-glyph fallback: chu cai lay font A, dau ket hop lay font B vi
    font A thieu dung glyph do) - truong hop nay KHONG sinh canh bao nao vi glyph
    van ton tai o dau do trong list, chi la font khac nhau co the ve dau lech
    metric so voi chu cai.

    Dieu kien DU de KHONG bao gio xay ra per-glyph fallback la: font DAU TIEN
    trong list phai phu het moi codepoint cua chuoi tieng Viet kho (dau chong +
    dau tren chu hoa). Kiem bang fontTools: lay sans[0]/mono[0], dung
    matplotlib.font_manager.findfont de ra duong dan file that, mo bang TTFont,
    doc bang cmap, va assert moi codepoint trong chuoi thu deu co mat. Thong bao
    loi in ra chinh ky tu thieu va ten font, de lan sau ai cham vao biet ngay
    hong o dau."""
    script = f"""
import sys
sys.path.insert(0, {str(EIR)!r})
import _eir_style
import matplotlib.font_manager as fm
from fontTools.ttLib import TTFont

sans, mono = _eir_style.setup_fonts()
hard = {HARD_MIXED_DIACRITICS!r}

for label, fam in (("sans", sans), ("mono", mono)):
    first = fam[0]
    path = fm.findfont(fm.FontProperties(family=first), fallback_to_default=False)
    cmap = TTFont(path).getBestCmap()
    missing = [c for c in hard if ord(c) not in cmap]
    if missing:
        print(f"MISSING label={{label}} font={{first!r}} path={{path}} chars={{missing!r}}")
    else:
        print(f"OK label={{label}} font={{first!r}} path={{path}}")
"""
    out = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=120
    )
    assert "MISSING" not in out.stdout, (
        "font dau tien trong list KHONG phu het codepoint -> se roi ve per-glyph "
        f"fallback, dau tach roi troi noi ma KHONG co canh bao nao ca:\n"
        f"{out.stdout}\n{out.stderr}"
    )
    assert out.stdout.count("OK ") == 2, (
        f"khong chay du ca hai nhanh sans va mono:\n{out.stdout}\n{out.stderr}"
    )


def test_save_that_giu_van_ban_tieng_viet_qua_nhanh_svg_fonttype():
    """Test truoc (test_svg_giu_text_that_khong_bien_thanh_path) TU dat
    rcParams["svg.fonttype"] roi goi fig.savefig() TRUC TIEP, KHONG di qua
    _eir_style.save(). Nhanh code moi trong save() (neu duoi .svg thi ep
    svg.fonttype='none') vi vay CHUA TUNG duoc test nao thuc thi. Test nay goi
    dung ham save() that, qua duong dan .svg, roi kiem chu tieng Viet con
    nguyen ven va van la <text> that chu khong bi bien thanh <path>."""
    out_path = "/tmp/eir_font_check_via_save.svg"
    script = f"""
import sys
sys.path.insert(0, {str(EIR)!r})
import matplotlib.pyplot as plt
import _eir_style

sans, mono = _eir_style.setup_fonts()
fig, ax = plt.subplots(figsize=(6, 2))
ax.text(0.05, 0.5, {VIET_TEST!r}, fontfamily=sans, fontsize=12)
ax.set_axis_off()
_eir_style.save(fig, {out_path!r})
"""
    subprocess.run([sys.executable, "-c", script], check=True, timeout=120)
    svg = Path(out_path).read_text(encoding="utf-8")
    assert "<text" in svg, "save() khong ep svg.fonttype='none', chu da bien thanh path"
    assert "chiết khấu" in svg, "chu tieng Viet khong con nguyen ven qua save()"
    assert "<image" not in svg, "SVG qua save() nhung anh raster"


# ── Font nhung trong repo, khong muon font he thong ───────────────────────

TTF = ROOT / "design-system" / "fonts" / "ttf"


def test_co_du_file_ttf_trong_repo():
    """File .ttf phai NAM TRONG repo va duoc commit.

    Truoc day _eir_style.py tro thang vao /usr/share/fonts, tuc mot phu thuoc
    ngoai repo: may nao thieu Liberation thi chart roi ve DejaVu va nhan tieng
    Viet mat dau. Sinh lai bang: python3 design-system/fonts/extract-ttf.py
    """
    can = [
        "IBMPlexSans-400.ttf", "IBMPlexSans-600.ttf",
        "IBMPlexMono-400.ttf", "IBMPlexMono-600.ttf",
        "Spectral-400.ttf", "Spectral-700.ttf",
    ]
    thieu = [t for t in can if not (TTF / t).exists()]
    assert not thieu, f"thieu file font trong repo: {thieu}. Chay extract-ttf.py"


def test_matplotlib_chon_font_trong_repo_chu_khong_phai_font_he_thong():
    """Do FILE THAT duoc chon, khong tin danh sach ten.

    setup_fonts() tra ve list ten, nhung ten nam dau list KHONG chung minh
    matplotlib se dung file do: neu ten ho bi lech (vd file 600 khai ho rieng
    la 'IBM Plex Sans SemiBold') thi xin ban dam se roi sang font khac ma
    khong bao gi. Da xay ra that o vong dau, phat hien bang chinh phep do nay.
    Vi vay test hoi thang findfont cho ca sau to hop.
    """
    sys.path.insert(0, str(EIR))
    import matplotlib

    matplotlib.use("agg")
    from matplotlib import font_manager as fm
    import _eir_style

    sans, mono = _eir_style.setup_fonts()
    lech = []
    for ten, ho in (("sans", sans), ("mono", mono), ("serif", _eir_style.SERIF)):
        for weight in ("normal", "bold"):
            duong_dan = Path(fm.findfont(fm.FontProperties(family=ho, weight=weight)))
            if duong_dan.parent != TTF:
                lech.append(f"{ten}/{weight} -> {duong_dan}")
    assert not lech, (
        "matplotlib dang dung font NGOAI repo, nhan tieng Viet co the mat dau "
        f"tren may khac:\n{chr(10).join(lech)}"
    )


def test_font_trong_repo_phu_du_dac_ta_tieng_viet():
    """Doi chieu voi dac ta DOC LAP sinh tu unicodedata, khong phai metadata
    cua chinh nha cung cap font. Day la bai hoc kiem chung vong tron da ghi
    trong progress.md: lay nguon tao ra dau ra de kiem dau ra thi luon PASS.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fonts_test import DAC_TA_TIENG_VIET_DOC_LAP as DAC_TA
    from fontTools.ttLib import TTFont

    thieu_tong = {}
    for f in sorted(TTF.glob("*.ttf")):
        font = TTFont(f)
        co = set()
        for bang in font["cmap"].tables:
            co |= set(bang.cmap.keys())
        font.close()
        # DAC_TA la set cac CODEPOINT (int), khong phai ky tu. Giu nguyen kieu
        # int de so sanh thang voi khoa cua bang cmap.
        thieu = sorted(c for c in DAC_TA if c not in co)
        if thieu:
            thieu_tong[f.name] = [f"U+{c:04X} {chr(c)!r}" for c in thieu[:10]]
    assert not thieu_tong, (
        f"font trong repo thieu codepoint tieng Viet (doi chieu {len(DAC_TA)} codepoint): {thieu_tong}"
    )


def test_dau_am_dung_ascii_khong_dung_u2212():
    """Sau `setup_fonts()`, matplotlib phai sinh dau am bang dau gach noi ASCII.

    Mac dinh cua matplotlib la `axes.unicode_minus = True`, tuc tick truc ra U+2212,
    trong khi moi formatter khac cua repo sinh ASCII. Do duoc truoc khi vá, tren
    `catalog/xem-truoc/diverging_bar.svg`: tick ra `-2` `-1` bang U+2212 con nhan gia
    tri TRONG CUNG MOT HINH ra `-2.0` `-1.1` bang ASCII. Hai ky tu nhin gan giong nhau
    nen mat khong bao gio bat duoc, chi dem codepoint moi thay.
    """
    sys.path.insert(0, str(EIR))
    import matplotlib
    matplotlib.use("Agg")
    import _eir_style

    _eir_style.setup_fonts()
    import matplotlib.pyplot as plt

    assert plt.rcParams["axes.unicode_minus"] is False, (
        "axes.unicode_minus dang bat: tick truc se ra U+2212 con nhan gia tri ra dau "
        "gach noi ASCII, mot hinh hai kieu dau am"
    )

    # Do THAT tren mot truc co gia tri am, khong chi doc rcParams.
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.plot([-2, -1, 0, 1], [1, 2, 3, 4])
    fig.canvas.draw()
    nhan = [t.get_text() for t in ax.get_xticklabels()]
    plt.close(fig)
    lan = [n for n in nhan if "−" in n]
    assert not lan, f"tick truc con dung U+2212: {lan}"
