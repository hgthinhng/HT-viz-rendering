import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EIR = ROOT / "charts" / "matplotlib"

VIET_TEST = "Số liệu tại 06/2026 · chiết khấu 14% · Nguồn: BCTC"


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
