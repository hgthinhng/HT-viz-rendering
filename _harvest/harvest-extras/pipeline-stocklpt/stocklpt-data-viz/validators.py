"""
StockLPT Data Viz - Validators + Ticker matcher
=============================================

Thay thế viz_advisor.py cũ. Triết lý:

- LLM (Opus đang chạy skill này) là advisor. Nó đọc content, decide component,
  generate params - không cần regex heuristic engine.

- Module này chỉ làm 3 việc deterministic:
  1. Ticker whitelist matching - fast lookup, không cần LLM phí token.
  2. Number formatter VN-style - precision-sensitive, LLM dễ mistake decimal.
  3. Post-render validators - palette, em-dash, font, VN number, no overflow.

Usage:
    from validators import (
        is_valid_ticker, get_ticker_sector,
        format_vn_number,
        validate_no_em_dash, validate_palette,
        validate_vn_numbers, validate_font_whitelist,
        validate_html,
    )

    # Pre-render: extract data
    if is_valid_ticker("VPB"):
        sector = get_ticker_sector("VPB")  # "banking"
        num_str = format_vn_number(111.9, "%")  # "111,9%"

    # Post-render: validate HTML body
    errors = validate_html(html_body)
    if errors:
        for e in errors:
            print(f"  - {e}")
"""
from __future__ import annotations
import re
from typing import Literal

# Brand engine: palette allow-list theo brand đang active.
# Same-dir import; fallback an toàn nếu chạy lẻ ngoài context.
try:
    from _brand import current_brand, STOCKLPT_PALETTE_LOWER as _STOCKLPT_PAL
except Exception:  # pragma: no cover
    current_brand = None
    _STOCKLPT_PAL = frozenset()


# ============================================================
# TICKER WHITELIST
# ============================================================

BANK_TICKERS = [
    "VCB", "CTG", "BID", "AGR",                # SOCB Big4
    "TCB", "VPB", "MBB", "ACB",                # tư nhân lớn
    "HDB", "STB", "EIB", "VIB", "SHB",         # nhóm B
    "NCB", "BVB", "ABB", "KLB",                # nhóm C
    "OCB", "LPB", "MSB", "TPB",                # mid-tier
    "NAB", "PGB", "SSB", "VAB",                # smaller
]

STOCK_TICKERS = {
    "steel": ["HPG", "HSG", "NKG", "TVN"],
    "retail": ["MWG", "FRT", "PNJ", "DGW"],
    "real_estate": ["VHM", "VIC", "VRE", "NVL", "KDH", "DXG", "PDR", "DIG"],
    "energy": ["GAS", "PLX", "POW", "PVS", "PVD", "PVT"],
    "logistics": ["GMD", "VTP", "HVN", "VJC", "ACV"],
    "agri_chem": ["DBC", "GVR", "DGC", "DCM", "DPM", "BAF"],
    "tech": ["FPT", "CMG", "CTR", "ELC"],
    "consumer": ["SAB", "VNM", "MSN", "VHC", "QNS"],
    "construction": ["CTD", "VCG", "HBC", "ROS"],
    "utilities": ["REE", "PPC", "NT2", "BWE"],
    "insurance": ["BVH", "BIC", "PVI", "MIG"],
    "securities": ["SSI", "VND", "HCM", "VCI", "FTS"],
}

ALL_TICKERS = set(BANK_TICKERS)
for sector_list in STOCK_TICKERS.values():
    ALL_TICKERS.update(sector_list)


def is_valid_ticker(s: str) -> bool:
    """True nếu s là ticker VN biết trước (bank hoặc stock)."""
    return s.upper() in ALL_TICKERS


def get_ticker_sector(ticker: str) -> str | None:
    """Return sector name của ticker, hoặc None nếu không biết.

    "VPB" -> "banking"
    "HPG" -> "steel"
    "XYZ" -> None
    """
    t = ticker.upper()
    if t in BANK_TICKERS:
        return "banking"
    for sector, tickers in STOCK_TICKERS.items():
        if t in tickers:
            return sector
    return None


def extract_tickers(text: str) -> list[str]:
    """Extract tất cả ticker xuất hiện trong text, theo thứ tự gặp.

    Match pattern: 3-4 ký tự hoa, đứng riêng (không trong word lớn hơn).
    Filter qua whitelist - tránh false positive từ acronym (NSFR, CASA, FRR, ...).
    """
    found = []
    seen = set()
    # Word boundary, 3-4 uppercase letters
    for m in re.finditer(r"\b[A-Z]{3,4}\b", text):
        cand = m.group(0)
        if cand in ALL_TICKERS and cand not in seen:
            found.append(cand)
            seen.add(cand)
    return found


# ============================================================
# VN NUMBER FORMATTER
# ============================================================

def format_vn_number(
    value: float,
    unit: str = "",
    precision: int | None = None,
) -> str:
    """Format number theo chuẩn VN: dấu phẩy thập phân, dấu chấm thousands.

    Examples:
        format_vn_number(111.9, "%")              -> "111,9%"
        format_vn_number(0.0089, "bps")           -> "89 bps"   (auto rate→bps)
        format_vn_number(406_000_000_000, "VND")  -> "406 tỷ"
        format_vn_number(1_500_000_000, "VND")    -> "1,5 tỷ"
        format_vn_number(1_230_000, "USD")        -> "$1,2M"
        format_vn_number(-5.2, "pp")              -> "-5,2 đp"
        format_vn_number(406_000, "VND_short")    -> "406K"

    Notes:
        - Auto-scale VND: triệu/tỷ/nghìn tỷ
        - Auto-scale USD: K/M/B
        - bps auto-convert nếu rate < 1%
        - precision default = 1 cho %, 0 cho integer
    """
    if value is None:
        return ""

    sign = "-" if value < 0 else ""
    v = abs(value)

    # bps: auto convert from rate
    if unit == "bps":
        # Nếu input < 1, giả định là rate (0.0089 = 89 bps)
        if v < 1:
            v_bps = round(v * 10000)
            return f"{sign}{v_bps:.0f} bps"
        else:
            return f"{sign}{v:.0f} bps"

    # VND auto-scale
    if unit == "VND":
        if v >= 1e12:
            scaled = v / 1e12
            return f"{sign}{_decimal_vn(scaled, 1)} nghìn tỷ"
        elif v >= 1e9:
            scaled = v / 1e9
            return f"{sign}{_decimal_vn(scaled, 1)} tỷ"
        elif v >= 1e6:
            scaled = v / 1e6
            return f"{sign}{_decimal_vn(scaled, 1)} triệu"
        else:
            return f"{sign}{_thousands_vn(int(v))} VND"

    if unit == "VND_short":
        if v >= 1e9:
            return f"{sign}{_decimal_vn(v/1e9, 1)}B"
        elif v >= 1e6:
            return f"{sign}{_decimal_vn(v/1e6, 1)}M"
        elif v >= 1e3:
            return f"{sign}{_decimal_vn(v/1e3, 0)}K"
        else:
            return f"{sign}{_thousands_vn(int(v))}"

    # USD auto-scale
    if unit == "USD":
        if v >= 1e9:
            return f"${sign}{_decimal_vn(v/1e9, 1)}B"
        elif v >= 1e6:
            return f"${sign}{_decimal_vn(v/1e6, 1)}M"
        elif v >= 1e3:
            return f"${sign}{_decimal_vn(v/1e3, 0)}K"
        else:
            return f"${sign}{_thousands_vn(int(v))}"

    # Percentage / pp / đp
    if unit in ("%", "pp", "đp"):
        prec = precision if precision is not None else 1
        out = _decimal_vn(v, prec)
        suffix = unit if unit != "pp" else "đp"
        return f"{sign}{out}{suffix}"

    # x multiplier (P/B, P/E)
    if unit == "x":
        prec = precision if precision is not None else 1
        return f"{sign}{_decimal_vn(v, prec)}x"

    # Default: just number with VN format
    prec = precision if precision is not None else (0 if v == int(v) else 1)
    if prec == 0:
        return f"{sign}{_thousands_vn(int(v))}{(' ' + unit) if unit else ''}"
    else:
        return f"{sign}{_decimal_vn(v, prec)}{(' ' + unit) if unit else ''}"


def _decimal_vn(value: float, precision: int) -> str:
    """1234.5 with prec=1 -> '1.234,5'"""
    rounded = round(value, precision)
    int_part = int(rounded)
    frac_part = abs(rounded - int_part)
    int_str = _thousands_vn(int_part)
    if precision == 0:
        return int_str
    frac_str = f"{frac_part:.{precision}f}".split(".")[1]
    return f"{int_str},{frac_str}"


def _thousands_vn(value: int) -> str:
    """1234567 -> '1.234.567'"""
    s = str(abs(value))
    if len(s) <= 3:
        return s
    parts = []
    while len(s) > 3:
        parts.insert(0, s[-3:])
        s = s[:-3]
    parts.insert(0, s)
    return ".".join(parts)


# ============================================================
# POST-RENDER VALIDATORS
# ============================================================

# Locked palette - hex must match (case-insensitive).
# NOTE: allow-list thực tế lấy LIVE từ brand engine trong
# validate_palette() => tự động chấp nhận palette của brand đang active
# (StockLPT hoặc StockLPT). Dict dưới giữ lại cho doc/external import.
PALETTE_LOCKED = {
    "#2A1A4A": "Indigo",
    "#130B24": "Indigo-900 (cover dark)",
    "#16633C": "Accent",
    "#7A1F35": "Bordeaux",
    "#514B78": "Slate",
    "#EBEFF4": "Ivory",
    "#F4F6F9": "Paper",
    "#221A34": "Charcoal",
    "#21B36A": "Positive",
    "#E13453": "Negative",
}
PALETTE_LOCKED_LOWER = {k.lower(): v for k, v in PALETTE_LOCKED.items()}

# Allow-list shades (subtle tints used in CSS)
PALETTE_ALLOWED_TINTS = {
    "#FAFBFD", "#EDF0F5", "#E2E8F0", "#D2DAE5",   # paper variants
    "#221545", "#352558",                           # indigo shades
    "#2C7A4E", "#0E4429",                           # accent shades
    "#99283F", "#531526",                           # bordeaux shades
}
# StockLPT base allow-list (fallback khi brand engine không import được).
PALETTE_ALLOWED_LOWER = (
    set(_STOCKLPT_PAL)
    or (set(PALETTE_LOCKED_LOWER.keys()) | PALETTE_ALLOWED_TINTS)
)


def _allowed_palette() -> set:
    """Allow-list LIVE: palette của brand active (gồm StockLPT nguồn + brand đích).

    Pre-remap content luôn ở không gian StockLPT nên StockLPT hex phải pass; tác giả
    có thể tự dán hex của brand đích nên cũng phải pass -> union cả hai."""
    if current_brand is not None:
        try:
            return set(current_brand().palette_allowed())
        except Exception:  # pragma: no cover
            pass
    return set(PALETTE_ALLOWED_LOWER)


# Font whitelist (CSS font-family value).
# Lưu ý: khớp font THỰC TẾ đang render. Aliases PFD/JBM map sang
# Lora / IBM Plex Mono (xem render.build_font_face). 'playfair' giữ lại
# cho tương thích ngược legacy.
FONT_WHITELIST = {
    "inter", "intervn",
    "pfd", "pfdvn", "lora",
    "jbm", "jbmvn", "ibm plex mono", "plex mono",
    "playfair display", "playfair",   # legacy alias
    "georgia",
    "serif", "sans-serif", "monospace",   # fallbacks
    "system-ui", "ui-serif", "ui-sans-serif", "ui-monospace",
}


def validate_no_em_dash(html: str) -> list[str]:
    """Return list errors. Em-dash U+2014 và en-dash U+2013 cấm tuyệt đối."""
    errors = []
    if "—" in html:
        # Find context
        idx = html.find("—")
        ctx = html[max(0, idx-30):idx+30]
        errors.append(f"Em-dash U+2014 phát hiện. Context: '...{ctx}...'")
    if "–" in html:
        idx = html.find("–")
        ctx = html[max(0, idx-30):idx+30]
        errors.append(f"En-dash U+2013 phát hiện. Context: '...{ctx}...'")
    return errors


def validate_palette(html: str) -> list[str]:
    """Return list errors. Tìm hex color value KHÔNG nằm trong palette + tints.

    allow-list lấy LIVE theo brand active (StockLPT)."""
    errors = []
    allowed = _allowed_palette()
    # Match hex color trong CSS / SVG attrs
    pattern = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    seen = set()
    for m in pattern.finditer(html):
        hex_val = m.group(0).lower()
        # Normalize 3-char hex to 6
        if len(hex_val) == 4:
            hex_val = "#" + "".join(c*2 for c in hex_val[1:])
        # Strip alpha if 8-char
        if len(hex_val) == 9:
            hex_val = hex_val[:7]
        if hex_val in seen:
            continue
        seen.add(hex_val)
        if hex_val not in allowed:
            # Allow #fff/#000 nhưng warn (StockLPT rule: paper/charcoal thay)
            if hex_val in ("#ffffff", "#000000"):
                errors.append(
                    f"Pure {hex_val} dùng trực tiếp - thay #F4F6F9 (paper) "
                    f"hoặc #221A34 (charcoal)."
                )
            else:
                _bn = current_brand().display_name if current_brand else "StockLPT"
                errors.append(f"Hex color {hex_val} ngoài palette {_bn}.")
    return errors


def validate_vn_numbers(html: str) -> list[str]:
    r"""Warn nếu số dùng dấu chấm thập phân thay vì dấu phẩy.

    Skip code blocks, hex colors, version strings.
    Heuristic: số có dạng 'd+\.\d+%' hoặc 'd+\.\d+ (đp|tỷ|triệu|nghìn|bps)'.
    """
    warnings = []
    # Pattern: số nguyên + dấu chấm + decimal + unit VN
    pattern = re.compile(
        r"(?<![\d.])(\d{1,4})\.(\d{1,2})\s*(%|đp|tỷ|triệu|nghìn|bps|đồng)(?!\w)"
    )
    for m in pattern.finditer(html):
        warnings.append(
            f"Số dạng '{m.group(0)}' dùng dấu chấm thập phân - VN style "
            f"là dấu phẩy ({m.group(1)},{m.group(2)}{m.group(3)})."
        )
    return warnings


def validate_font_whitelist(html: str) -> list[str]:
    """Warn nếu CSS font-family ngoài 3 stacks StockLPT."""
    warnings = []
    pattern = re.compile(r"font-family:\s*([^;'\"\}]+)", re.IGNORECASE)
    for m in pattern.finditer(html):
        family_str = m.group(1).strip()
        # Split fallback chain
        families = [f.strip().strip("'\"").lower() for f in family_str.split(",")]
        for f in families:
            # Strip quoting
            if f and f not in FONT_WHITELIST:
                # Allow generic family names + system fonts
                if not any(allowed in f for allowed in FONT_WHITELIST):
                    warnings.append(
                        f"Font '{f}' ngoài whitelist (Playfair, Inter, JetBrains)."
                    )
    return warnings


def validate_html(html: str) -> list[str]:
    """Run all validators. Return concatenated errors + warnings."""
    out = []
    out += validate_no_em_dash(html)
    out += validate_palette(html)
    out += validate_vn_numbers(html)
    out += validate_font_whitelist(html)
    return out


# ============================================================
# SMOKE TEST
# ============================================================

if __name__ == "__main__":
    # Ticker
    assert is_valid_ticker("VPB") == True
    assert is_valid_ticker("XYZ") == False
    assert get_ticker_sector("VPB") == "banking"
    assert get_ticker_sector("HPG") == "steel"

    # Extract
    text = "Q1/2026 VPB và TCB cùng chạm trần SFL. NSFR theo Basel III. HPG báo cáo Q4."
    tickers = extract_tickers(text)
    assert "VPB" in tickers
    assert "TCB" in tickers
    assert "HPG" in tickers
    assert "NSFR" not in tickers  # not in whitelist

    # Number format
    assert format_vn_number(111.9, "%") == "111,9%"
    assert format_vn_number(0.0089, "bps") == "89 bps"
    assert format_vn_number(1_500_000_000, "VND") == "1,5 tỷ"
    assert format_vn_number(-5.2, "pp") == "-5,2đp"
    assert format_vn_number(2.1, "x") == "2,1x"

    # Validators
    assert validate_no_em_dash("Bài này không có em dash") == []
    assert len(validate_no_em_dash("Bài này có — em dash")) == 1
    assert len(validate_no_em_dash("Bài này có – en dash")) == 1

    assert validate_palette('color:#2A1A4A;') == []
    assert len(validate_palette('color:#FF0000;')) == 1   # red không phải palette

    assert len(validate_vn_numbers("VPB SFL 28.3% trần 30%")) == 1
    assert validate_vn_numbers("VPB SFL 28,3% trần 30%") == []

    print("All validators OK.")
