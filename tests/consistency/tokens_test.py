import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "design-system" / "tokens.css"


def parse_css_root():
    text = CSS.read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\}", text, re.S)
    assert block, "khong tim thay khoi :root trong tokens.css"
    out = {}
    for line in block.group(1).split("\n"):
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


def test_python_khop_css():
    import sys

    sys.path.insert(0, str(ROOT / "design-system"))
    import tokens

    css = parse_css_root()
    for name, hexval in tokens.COLORS.items():
        css_name = name.replace("_", "-")
        assert css_name in css, f"tokens.py co {name} nhung tokens.css khong co"
        assert css[css_name].upper() == hexval.upper(), (
            f"{name} lech giua hai ban: py={hexval} css={css[css_name]}"
        )


def test_shadow_khong_co_blur():
    css = parse_css_root()
    for name, val in css.items():
        if name.startswith("shadow"):
            parts = [p.strip() for p in val.split(",")]
            for p in parts:
                nums = re.findall(r"(-?\d+(?:\.\d+)?)px", p)
                assert len(nums) >= 3, f"--{name} thieu thanh phan: {p}"
                assert float(nums[2]) == 0.0, (
                    f"--{name} co blur={nums[2]}px, phai bang 0 (bay raster khi in)"
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
