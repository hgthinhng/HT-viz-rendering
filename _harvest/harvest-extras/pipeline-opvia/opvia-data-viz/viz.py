"""
Opvia Data Viz - 6 components cho bài phân tích sâu tài chính
Tất cả render qua HTML + inline SVG, tương thích WeasyPrint.

Usage:
    from viz import viz_styles, bar_horizontal, gauge, heatmap, flow_bridge, scenario_cards, timeline_horizontal
    from viz import format_number, color_for_ticker, smart_wrap

    css = build_css(...) + viz_styles()
    body = f'''
      ...
      {bar_horizontal(items=[...], threshold=30)}
      {gauge(value=111.9, max_val=120, threshold=85, label="LDR hệ thống", value_format="{{:.1f}}%")}
      ...
    '''
"""
from __future__ import annotations
import math
from html import escape


# ============================================================
# UTILITIES (Wave 1)
# ============================================================

def format_number(
    value: float,
    unit: str = "",
    precision: int = 1,
    style: str = "vn",
) -> str:
    """
    Smart format số liệu tài chính theo chuẩn VN.

    Args:
        value: số cần format
        unit: "", "%", "VND", "USD", "bps", "pp" (percentage points)
        precision: số chữ số sau dấu phẩy (default 1)
        style: "vn" (default) dùng dấu phẩy decimal + dấu chấm thousands;
               "en" dùng ngược lại.

    Examples:
        format_number(111.9, "%") -> "111,9%"
        format_number(0.0089, "%") -> "0,89%"  hoặc "89 bps" nếu unit="bps"
        format_number(1234567, "VND") -> "1,23 triệu VND" hoặc "1,23M"
        format_number(406000, "VND_short") -> "406K"
        format_number(-5.2, "pp") -> "-5,2 đp"
    """
    sign = "-" if value < 0 else ""
    v = abs(value)

    # Bps conversion (cho rate < 1%)
    if unit == "bps":
        bps = v * 10000  # 0.0089 -> 89
        return f"{sign}{bps:.0f} bps"

    # Percent
    if unit == "%":
        formatted = _vn_decimal(v, precision)
        return f"{sign}{formatted}%"

    # Percentage points (đp)
    if unit == "pp":
        formatted = _vn_decimal(v, precision)
        return f"{sign}{formatted} đp"

    # VND auto-scale
    if unit == "VND":
        if v >= 1_000_000_000_000:  # >= 1 nghìn tỷ
            scaled = v / 1_000_000_000_000
            return f"{sign}{_vn_decimal_smart(scaled, 1)} nghìn tỷ"
        elif v >= 1_000_000_000:  # >= 1 tỷ
            scaled = v / 1_000_000_000
            return f"{sign}{_vn_decimal_smart(scaled, 1)} tỷ"
        elif v >= 1_000_000:  # >= 1 triệu
            scaled = v / 1_000_000
            return f"{sign}{_vn_decimal_smart(scaled, 1)} triệu"
        else:
            return f"{sign}{_vn_thousands(int(v))}"

    # VND_short: K notation cho dashboard
    if unit == "VND_short":
        if v >= 1_000_000_000:
            return f"{sign}{_vn_decimal(v/1_000_000_000, 1)}B"
        elif v >= 1_000_000:
            return f"{sign}{_vn_decimal(v/1_000_000, 0)}M"
        elif v >= 1_000:
            return f"{sign}{_vn_decimal(v/1_000, 0)}K"
        else:
            return f"{sign}{int(v)}"

    # USD auto-scale
    if unit == "USD":
        if v >= 1_000_000_000:
            return f"{sign}${_vn_decimal(v/1_000_000_000, 1)}B"
        elif v >= 1_000_000:
            return f"{sign}${_vn_decimal(v/1_000_000, 1)}M"
        elif v >= 1_000:
            return f"{sign}${_vn_decimal(v/1_000, 1)}K"
        else:
            return f"{sign}${int(v)}"

    # Default: number with VN formatting
    if v == int(v):
        return f"{sign}{_vn_thousands(int(v))}"
    return f"{sign}{_vn_decimal(v, precision)}"


def _vn_decimal(value: float, precision: int) -> str:
    """Format decimal với dấu phẩy: 111.9 -> '111,9'."""
    formatted = f"{value:.{precision}f}"
    return formatted.replace(".", ",")


def _vn_decimal_smart(value: float, precision: int) -> str:
    """Format decimal nhưng drop .0 trailing nếu integer.
    406.0 -> '406', 1.5 -> '1,5'.
    """
    if value == int(value):
        return f"{int(value)}"
    formatted = f"{value:.{precision}f}"
    return formatted.replace(".", ",")


def _vn_thousands(value: int) -> str:
    """Format thousands với dấu chấm: 1234567 -> '1.234.567'."""
    return f"{value:,}".replace(",", ".")


# ============================================================
# SECTOR COLOR CODING (Wave 1)
# ============================================================

SECTOR_COLORS = {
    # Banks
    "big4_socb": "#003153",      # prussian
    "tier1_jsb": "#4A6FA5",      # slate
    "tier2_jsb": "#B5A642",      # brass
    "tier3_jsb": "#6B6760",      # gray
    "foreign_bank": "#722F37",   # bordeaux

    # Non-banks
    "real_estate": "#4F4A2C",    # olive
    "retail": "#5C7A8C",         # steel blue
    "energy": "#7A4A2C",         # rust
    "tech": "#3D5A6C",           # navy steel
    "industrial": "#8B7355",     # taupe
    "consumer": "#A6864A",       # bronze

    # Default
    "default": "#4A6FA5",        # fallback slate
}


TICKER_TO_SECTOR = {
    # Big4 SOCB
    "VCB": "big4_socb", "CTG": "big4_socb", "BID": "big4_socb", "AGR": "big4_socb",

    # Tier-1 JSB
    "TCB": "tier1_jsb", "VPB": "tier1_jsb", "MBB": "tier1_jsb", "ACB": "tier1_jsb",
    "MB": "tier1_jsb",

    # Tier-2 JSB
    "HDB": "tier2_jsb", "VIB": "tier2_jsb", "SHB": "tier2_jsb", "TPB": "tier2_jsb",
    "EIB": "tier2_jsb", "OCB": "tier2_jsb", "STB": "tier2_jsb", "LPB": "tier2_jsb",
    "MSB": "tier2_jsb", "SSB": "tier2_jsb",

    # Tier-3 JSB
    "NCB": "tier3_jsb", "BVB": "tier3_jsb", "ABB": "tier3_jsb", "KLB": "tier3_jsb",
    "NAB": "tier3_jsb", "PGB": "tier3_jsb", "VBB": "tier3_jsb", "VAB": "tier3_jsb",

    # Real estate
    "VHM": "real_estate", "NVL": "real_estate", "KDH": "real_estate", "PDR": "real_estate",
    "DXG": "real_estate", "NLG": "real_estate", "DIG": "real_estate", "VIC": "real_estate",
    "VRE": "real_estate", "BCM": "real_estate",

    # Retail
    "MWG": "retail", "FRT": "retail", "PNJ": "retail", "DGW": "retail",

    # Energy
    "GAS": "energy", "PVS": "energy", "PVD": "energy", "BSR": "energy", "PLX": "energy",
    "POW": "energy",

    # Industrial / steel
    "HPG": "industrial", "HSG": "industrial", "NKG": "industrial",

    # Consumer
    "VNM": "consumer", "MSN": "consumer", "SAB": "consumer", "BHN": "consumer",
}


def color_for_ticker(ticker: str) -> str:
    """
    Trả về màu hex cho ticker dựa trên sector.
    Fallback default nếu ticker không có trong dictionary.

    Examples:
        color_for_ticker("VCB") -> "#003153"
        color_for_ticker("VPB") -> "#4A6FA5"
        color_for_ticker("UNKNOWN") -> "#4A6FA5" (fallback)
    """
    sector = TICKER_TO_SECTOR.get(ticker.upper(), "default")
    return SECTOR_COLORS.get(sector, SECTOR_COLORS["default"])


def sector_for_ticker(ticker: str) -> str:
    """Trả về sector key cho ticker."""
    return TICKER_TO_SECTOR.get(ticker.upper(), "default")


# ============================================================
# TEXT WRAP INTELLIGENCE (Wave 1)
# ============================================================

def smart_wrap(text: str, max_chars: int) -> tuple[str, str]:
    """
    Smart line break tại natural pause point thay vì simple middle split.

    Priority break points (highest → lowest):
    1. ", " (comma + space)
    2. " - " hoặc " – "
    3. " và ", " hoặc ", " nhưng ", " với ", " để "
    4. ". " (period + space)
    5. " " gần middle (fallback)

    Returns: (line1, line2). Nếu text ngắn hơn max_chars, trả về (text, "").

    Examples:
        smart_wrap("Big4 hưởng lợi gấp đôi nhờ TGKB", 18)
            -> ("Big4 hưởng lợi", "gấp đôi nhờ TGKB")
        smart_wrap("Phương án A là cứu sinh, B là cú đánh", 25)
            -> ("Phương án A là cứu sinh,", "B là cú đánh")
    """
    if len(text) <= max_chars:
        return (text, "")

    target_idx = max_chars  # ideal break around max_chars
    search_window = (max(0, target_idx - 12), min(len(text), target_idx + 8))
    window_text = text[search_window[0]:search_window[1]]

    # Priority 1: comma+space
    for marker in [", "]:
        idx = window_text.rfind(marker)
        if idx != -1:
            absolute_idx = search_window[0] + idx + len(marker)
            return (text[:absolute_idx].rstrip(), text[absolute_idx:].lstrip())

    # Priority 2: dash with spaces
    for marker in [" - ", " – "]:
        idx = window_text.rfind(marker)
        if idx != -1:
            absolute_idx = search_window[0] + idx + 1  # break after first space, before dash
            return (text[:absolute_idx].rstrip(), text[absolute_idx:].lstrip())

    # Priority 3: VN conjunctions
    for marker in [" và ", " hoặc ", " nhưng ", " với ", " để ", " khi ", " mà "]:
        idx = window_text.rfind(marker)
        if idx != -1:
            absolute_idx = search_window[0] + idx + 1  # break before conjunction
            return (text[:absolute_idx].rstrip(), text[absolute_idx:].lstrip())

    # Priority 4: period
    idx = window_text.rfind(". ")
    if idx != -1:
        absolute_idx = search_window[0] + idx + 2
        return (text[:absolute_idx].rstrip(), text[absolute_idx:].lstrip())

    # Fallback: nearest space to middle
    mid = len(text) // 2
    space_left = text.rfind(" ", 0, mid + 5)
    space_right = text.find(" ", mid - 5)
    if space_left != -1:
        return (text[:space_left].rstrip(), text[space_left:].lstrip())
    if space_right != -1:
        return (text[:space_right].rstrip(), text[space_right:].lstrip())

    # No space found - hard split
    return (text[:max_chars], text[max_chars:])


def viz_styles() -> str:
    """CSS cho tất cả 6 components - include 1 lần ở đầu file CSS."""
    return r"""
/* ============================================================
   OPVIA DATA VIZ - components stylesheet
   ============================================================ */

/* ---------- BAR HORIZONTAL ---------- */
.viz-bar {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-bar-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-bar-subtitle {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; font-weight: 400; color: #4A6FA5;
  margin-bottom: 4mm;
}
.viz-bar-row {
  display: grid; grid-template-columns: 22mm 1fr 18mm;
  gap: 8px; align-items: center;
  padding: 5px 0; border-bottom: 0.4px solid rgba(74,111,165,0.08);
}
.viz-bar-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9pt; font-weight: 600; color: #003153;
}
.viz-bar-note {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 400; font-style: italic;
  color: #6B6760;
}
.viz-bar-track {
  position: relative; height: 14px;
  background: rgba(74,111,165,0.08); border-radius: 2px;
}
.viz-bar-fill {
  height: 100%; border-radius: 2px;
  background: #003153;
}
.viz-bar-fill.danger { background: #C0392B; }
.viz-bar-fill.warn { background: #B5A642; }
.viz-bar-fill.positive { background: #2E7D52; }
.viz-bar-threshold {
  position: absolute; top: -3px; bottom: -3px;
  width: 1.5px; background: #722F37;
}
.viz-bar-threshold-label {
  position: absolute; top: -16px; transform: translateX(-50%);
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 7pt; font-weight: 600; color: #722F37;
  white-space: nowrap; letter-spacing: 0.06em;
}
.viz-bar-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 600; color: #003153;
  text-align: right;
}
.viz-bar-value.danger { color: #C0392B; font-weight: 700; }

/* ---------- GAUGE ---------- */
.viz-gauge {
  display: inline-block; vertical-align: top;
  margin: 4mm 0; page-break-inside: avoid;
  width: 100%; max-width: 110mm;
}
.viz-gauge-svg { display: block; width: 100%; height: auto; }
.viz-gauge-bg-arc { fill: none; stroke: #E5E0D5; stroke-width: 14; stroke-linecap: round; }
.viz-gauge-fill-arc { fill: none; stroke-width: 14; stroke-linecap: round; }
.viz-gauge-fill-arc.normal { stroke: #B5A642; }
.viz-gauge-fill-arc.danger { stroke: #C0392B; }
.viz-gauge-threshold-tick { stroke: #722F37; stroke-width: 2.5; }
.viz-gauge-value-text {
  font-family: 'JBM', 'JBMVN', monospace; font-weight: 700; fill: #003153;
}
.viz-gauge-label-text {
  font-family: 'Inter', 'InterVN', sans-serif; font-weight: 700; fill: #6B6760;
  letter-spacing: 0.14em; text-transform: uppercase;
}
.viz-gauge-threshold-text {
  font-family: 'JBM', 'JBMVN', monospace; font-weight: 600; fill: #722F37;
  letter-spacing: 0.06em;
}
.viz-gauge-desc {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9pt; line-height: 1.4; color: #2B2B2B;
  margin-top: 2mm; max-width: 88mm;
}

/* ---------- HEATMAP ---------- */
.viz-heatmap {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-heatmap-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-heatmap-subtitle {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; color: #4A6FA5; margin-bottom: 4mm;
}
.viz-heatmap-grid {
  display: grid; gap: 2px;
  border: 0.6px solid rgba(74,111,165,0.15);
  background: rgba(74,111,165,0.10);
}
.viz-heatmap-cell {
  padding: 6px 10px; min-height: 32px;
  display: flex; flex-direction: column; justify-content: center;
  background: #FAF7F0;
  font-family: 'Inter', 'InterVN', sans-serif;
  text-align: left;
}
.viz-heatmap-corner {
  background: #FAF7F0;
}
.viz-heatmap-row-header {
  background: #FAF7F0; font-weight: 700; color: #003153;
  font-size: 8.5pt; padding: 6px 8px; min-height: 32px;
  display: flex; align-items: center;
}
.viz-heatmap-col-header {
  background: #FAF7F0; font-weight: 700; color: #003153;
  font-size: 7.5pt; letter-spacing: 0.10em; text-transform: uppercase;
  padding: 5px 8px; text-align: center;
}
.viz-heatmap-cell .cell-text {
  font-size: 8.5pt; font-weight: 600;
}
.viz-heatmap-cell .cell-note {
  font-size: 7pt; color: #6B6760;
  margin-top: 2px;
}
.viz-heatmap-cell.pos-strongest {
  background: #2E7D52; color: #FFFFFF;
}
.viz-heatmap-cell.pos-strong {
  background: rgba(46,125,82,0.55); color: #003153;
}
.viz-heatmap-cell.pos {
  background: rgba(46,125,82,0.22); color: #003153;
}
.viz-heatmap-cell.neutral {
  background: rgba(74,111,165,0.08); color: #4A6FA5;
}
.viz-heatmap-cell.neg {
  background: rgba(192,57,43,0.18); color: #722F37;
}
.viz-heatmap-cell.neg-strong {
  background: rgba(192,57,43,0.45); color: #722F37;
}
.viz-heatmap-cell.neg-strongest {
  background: #C0392B; color: #FFFFFF;
}
.viz-heatmap-cell.pos-strongest .cell-note,
.viz-heatmap-cell.neg-strongest .cell-note { color: rgba(255,255,255,0.8); }

/* ---------- FLOW BRIDGE ---------- */
.viz-flow {
  margin: 7mm auto; page-break-inside: avoid;
  text-align: center;
  max-width: 110mm;
}
.viz-flow-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
  text-align: left;
}
.viz-flow-svg { display: block; margin: 0 auto; width: 100%; height: auto; }
.viz-flow-node-rect.cause { fill: #003153; }
.viz-flow-node-rect.intermediate { fill: #FAF7F0; stroke: #4A6FA5; stroke-width: 0.8; }
.viz-flow-node-rect.result { fill: #B5A642; }
.viz-flow-node-text {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; font-weight: 600;
}
.viz-flow-node-text.light { fill: #FAF7F0; }
.viz-flow-node-text.dark { fill: #003153; }
.viz-flow-arrow { stroke: #4A6FA5; stroke-width: 1.2; fill: none; }
.viz-flow-arrowhead { fill: #4A6FA5; }

/* ---------- SCENARIO CARDS ---------- */
.viz-scenarios {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 4mm; margin: 7mm 0;
  page-break-inside: avoid;
}
.viz-scenario {
  background: #FAF7F0; border-top: 3px solid #B5A642;
  padding: 5mm 5mm 5mm; border-radius: 2px;
  page-break-inside: avoid;
  display: flex; flex-direction: column;
}
.viz-scenario.base { border-top-color: #4A6FA5; }
.viz-scenario.positive { border-top-color: #2E7D52; }
.viz-scenario.negative { border-top-color: #C0392B; }
.viz-scenario-header {
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 3mm; padding-bottom: 2mm;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-scenario-name {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 12pt; font-weight: 700; color: #003153;
}
.viz-scenario-prob {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 11pt; font-weight: 700; color: #B5A642;
}
.viz-scenario-row {
  margin-bottom: 2.5mm;
}
.viz-scenario-row:last-child { margin-bottom: 0; }
.viz-scenario-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700; letter-spacing: 0.14em;
  text-transform: uppercase; color: #6B6760;
  margin-bottom: 1px;
}
.viz-scenario-value {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; line-height: 1.45; color: #2B2B2B;
}
.viz-scenario-value.winners { color: #2E7D52; font-weight: 600; }
.viz-scenario-value.losers { color: #C0392B; font-weight: 600; }

/* ---------- TIMELINE HORIZONTAL ---------- */
.viz-timeline {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-timeline-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-timeline-svg { display: block; width: 100%; height: auto; margin-top: 4mm; }
.viz-timeline-axis { stroke: #4A6FA5; stroke-width: 0.8; }
.viz-timeline-tick { stroke: #4A6FA5; stroke-width: 0.8; }
.viz-timeline-dot.milestone { fill: #4A6FA5; }
.viz-timeline-dot.decision { fill: #B5A642; }
.viz-timeline-dot.result { fill: #2E7D52; }
.viz-timeline-dot.current { fill: #C0392B; }
.viz-timeline-date {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 7pt; font-weight: 600; fill: #003153;
}
.viz-timeline-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; fill: #2B2B2B;
}
""" + WAVE2_STYLES + WAVE3_STYLES


# ============================================================
# COMPONENT 1: BAR HORIZONTAL
# ============================================================
def bar_horizontal(
    items: list[dict],
    threshold: float | None = None,
    threshold_label: str = "Trần",
    max_val: float | None = None,
    title: str = "",
    subtitle: str = "",
    auto_sector_color: bool = False,
) -> str:
    """
    Bar chart ngang cho so sánh metric giữa nhiều ngân hàng/quý/...

    Args:
        items: [{
            "label": str,           # ticker hoặc label
            "value": float,         # giá trị
            "danger": bool,         # bar đỏ
            "warn": bool,           # bar brass
            "positive": bool,       # bar xanh
            "value_label": str,     # custom format thay default "X%"
            "note": str,            # ghi chú italic dưới label (Wave 1)
        }]
        threshold: optional, nếu có sẽ vẽ vertical line marker
        threshold_label: label cho threshold ("Trần SFL", "Trần LDR"...)
        max_val: max scale; nếu None thì auto = max(items.value, threshold) * 1.15
        title, subtitle: optional headings
        auto_sector_color: nếu True và label là ticker, auto color theo sector
            (override danger/warn/positive flag) (Wave 1)
    """
    values = [i["value"] for i in items]
    if max_val is None:
        candidates = list(values)
        if threshold is not None:
            candidates.append(threshold)
        max_val = max(candidates) * 1.15

    rows_html = []
    for it in items:
        label = escape(it["label"])
        value = it["value"]
        danger = it.get("danger", False)
        positive = it.get("positive", False)
        warn = it.get("warn", False)
        note = it.get("note", "")
        cls = "danger" if danger else ("positive" if positive else ("warn" if warn else ""))
        val_cls = "danger" if danger else ""
        pct = min(100, (value / max_val) * 100)

        # Auto sector color override (Wave 1)
        custom_style = ""
        if auto_sector_color and not (danger or positive or warn):
            ticker_color = color_for_ticker(it["label"])
            custom_style = f"background: {ticker_color};"

        # value label format
        if isinstance(value, float) and not value.is_integer():
            val_str = f"{value:.1f}".replace(".", ",")
        else:
            val_str = f"{value:.0f}".replace(".", ",")
        val_str = it.get("value_label", val_str + "%")

        # Label with optional note
        label_html = f'<div class="viz-bar-label">{label}'
        if note:
            label_html += f'<span class="viz-bar-note"> {escape(note)}</span>'
        label_html += '</div>'

        # Build fill style (sector color override)
        if custom_style:
            fill_html = f'<div class="viz-bar-fill" style="width: {pct:.1f}%; {custom_style}"></div>'
        else:
            fill_html = f'<div class="viz-bar-fill {cls}" style="width: {pct:.1f}%"></div>'

        rows_html.append(f"""
        <div class="viz-bar-row">
          {label_html}
          <div class="viz-bar-track">
            {fill_html}
          </div>
          <div class="viz-bar-value {val_cls}">{val_str}</div>
        </div>
        """)

    # threshold marker - position absolute trong row (visual hint at top)
    threshold_html = ""
    if threshold is not None:
        thr_pct = (threshold / max_val) * 100
        threshold_label_str = f"{escape(threshold_label)} {threshold:.0f}%".replace(".", ",")
        # Place threshold as a row-overlay sibling at top
        threshold_html = f"""
        <div class="viz-bar-row" style="height: 14px; padding: 0; border: none; position: relative; margin-top: 14px;">
          <div></div>
          <div style="position: relative; height: 1px;">
            <div class="viz-bar-threshold" style="left: {thr_pct:.1f}%; height: 200%; top: -8px;"></div>
            <div class="viz-bar-threshold-label" style="left: {thr_pct:.1f}%;">{threshold_label_str}</div>
          </div>
          <div></div>
        </div>
        """

    title_html = f'<div class="viz-bar-title">{escape(title)}</div>' if title else ""
    subtitle_html = f'<div class="viz-bar-subtitle">{escape(subtitle)}</div>' if subtitle else ""

    return f"""
<div class="viz-bar">
  {title_html}
  {subtitle_html}
  {threshold_html}
  {''.join(rows_html)}
</div>
"""


# ============================================================
# COMPONENT 2: GAUGE
# ============================================================
def gauge(
    value: float,
    max_val: float,
    threshold: float | None = None,
    label: str = "",
    description: str = "",
    value_format: str = "{:.1f}%",
    danger_above: float | None = None,
    annotations: list[dict] | None = None,
) -> str:
    """
    Half-circle gauge cho 1 số signature (LDR, SFL...).

    Args:
        value: actual value
        max_val: max scale of the gauge
        threshold: optional threshold marker (Trần)
        label: small caption below value (e.g. "TỶ LỆ LDR HỆ THỐNG")
        description: 1-line desc below gauge
        value_format: Python format string
        danger_above: if value > this, fill color = red instead of brass
        annotations: optional list of {target, text, position} dicts.
            target: "value" | "threshold" | "max"
            text: annotation text (max ~25 chars)
            position: "top" | "right" | "left" | "bottom"
            example: [{"target": "value", "text": "Vượt trần 26,9 điểm", "position": "right"}]
    """
    # SVG layout
    cx, cy = 100, 110
    r = 80
    # Angle calculation: 0deg = left edge (9 o'clock), 180deg = right edge (3 o'clock)
    # Clamp value to max_val for visual
    v_clamped = min(value, max_val)
    pct = v_clamped / max_val
    angle_deg = pct * 180

    def polar_to_xy(theta_deg: float) -> tuple[float, float]:
        theta_rad = math.radians(theta_deg)
        x = cx - r * math.cos(theta_rad)
        y = cy - r * math.sin(theta_rad)
        return x, y

    # Background arc: full half-circle
    bg_path = f"M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy}"

    # Foreground arc: from 0 to angle_deg
    end_x, end_y = polar_to_xy(angle_deg)
    large_arc = 1 if angle_deg > 180 else 0
    fg_path = f"M {cx - r} {cy} A {r} {r} 0 {large_arc} 1 {end_x:.2f} {end_y:.2f}"

    # Determine fill color
    is_danger = danger_above is not None and value > danger_above
    fill_color = "#C0392B" if is_danger else "#B5A642"

    # Threshold tick
    threshold_html = ""
    threshold_text_html = ""
    if threshold is not None and threshold <= max_val:
        thr_pct = threshold / max_val
        thr_angle = thr_pct * 180
        # Tick from outer to slightly inner
        outer_x, outer_y = polar_to_xy(thr_angle)
        # Inner point: 12 units inside (radius 68)
        inner_r = r - 12
        inner_x = cx - inner_r * math.cos(math.radians(thr_angle))
        inner_y = cy - inner_r * math.sin(math.radians(thr_angle))
        threshold_html = f'<line x1="{outer_x:.2f}" y1="{outer_y:.2f}" x2="{inner_x:.2f}" y2="{inner_y:.2f}" stroke="#722F37" stroke-width="2.5"/>'
        # Threshold label - positioned outside the arc
        outside_r = r + 8
        out_x = cx - outside_r * math.cos(math.radians(thr_angle))
        out_y = cy - outside_r * math.sin(math.radians(thr_angle))
        thr_label = value_format.format(threshold).replace(".", ",")
        # text-anchor based on position
        anchor = "end" if thr_angle < 90 else "start"
        threshold_text_html = f'<text x="{out_x:.2f}" y="{out_y:.2f}" text-anchor="{anchor}" font-family="JBM,JBMVN,monospace" font-size="7" font-weight="600" fill="#722F37">Trần {thr_label}</text>'

    # Value text
    val_str = value_format.format(value).replace(".", ",")

    # Description
    desc_html = f'<div class="viz-gauge-desc">{escape(description)}</div>' if description else ""

    # Annotations (Wave 1)
    annotations_html = ""
    if annotations:
        for ann in annotations:
            target = ann.get("target", "value")
            ann_text = ann.get("text", "")
            ann_pos = ann.get("position", "right")

            # Compute target anchor point
            if target == "value":
                # End of fill arc
                ax, ay = polar_to_xy(angle_deg)
            elif target == "threshold" and threshold is not None:
                thr_angle = (threshold / max_val) * 180
                ax, ay = polar_to_xy(thr_angle)
            elif target == "max":
                ax, ay = polar_to_xy(180)  # right end
            else:
                ax, ay = cx, cy - r  # top of arc

            # Position text relative to anchor
            if ann_pos == "right":
                tx, ty = ax + 10, ay - 4
                anchor = "start"
            elif ann_pos == "left":
                tx, ty = ax - 10, ay - 4
                anchor = "end"
            elif ann_pos == "top":
                tx, ty = ax, ay - 12
                anchor = "middle"
            else:  # bottom
                tx, ty = ax, ay + 14
                anchor = "middle"

            # Connector line (small)
            line_attrs = f'x1="{ax:.1f}" y1="{ay:.1f}" x2="{tx:.1f}" y2="{ty + 3:.1f}"'
            annotations_html += f"""
            <line {line_attrs} stroke="#722F37" stroke-width="0.6" stroke-dasharray="1.5,1"/>
            <text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-family="Inter,InterVN,sans-serif" font-size="6.5" font-weight="600" fill="#722F37">{escape(ann_text)}</text>
            """

    return f"""
<div class="viz-gauge">
  <svg class="viz-gauge-svg" viewBox="0 0 240 130" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(20, 0)">
    <path d="{bg_path}" fill="none" stroke="#E5E0D5" stroke-width="14" stroke-linecap="round"/>
    <path d="{fg_path}" fill="none" stroke="{fill_color}" stroke-width="14" stroke-linecap="round"/>
    {threshold_html}
    {threshold_text_html}
    {annotations_html}
    <text x="{cx}" y="92" text-anchor="middle" font-family="JBM,JBMVN,monospace" font-size="22" font-weight="700" fill="#003153">{val_str}</text>
    <text x="{cx}" y="115" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="6.5" font-weight="700" fill="#6B6760" letter-spacing="0.5">{escape(label)}</text>
    </g>
  </svg>
  {desc_html}
</div>
"""


# ============================================================
# COMPONENT 3: HEATMAP
# ============================================================
def heatmap(
    rows: list[str],
    cols: list[str],
    cells: list[list[dict]],
    title: str = "",
    subtitle: str = "",
) -> str:
    """
    Heatmap matrix cho impact assessment (winners/losers, scenario comparison).

    Args:
        rows: list of row labels (e.g. bank names)
        cols: list of column labels (e.g. scenarios)
        cells: 2D list. Each cell = {"text": str, "note": str (optional), "color": str}
            color in: pos-strongest, pos-strong, pos, neutral, neg, neg-strong, neg-strongest
        title, subtitle: optional headings
    """
    n_cols = len(cols)
    grid_cols = f"22mm repeat({n_cols}, 1fr)"

    # Build header row
    header_html = '<div class="viz-heatmap-corner"></div>'
    for col in cols:
        header_html += f'<div class="viz-heatmap-col-header">{escape(col)}</div>'

    # Build data rows
    rows_html = ""
    for r_idx, row_label in enumerate(rows):
        rows_html += f'<div class="viz-heatmap-row-header">{escape(row_label)}</div>'
        for c_idx in range(n_cols):
            cell = cells[r_idx][c_idx] if r_idx < len(cells) and c_idx < len(cells[r_idx]) else {}
            color = cell.get("color", "neutral")
            text = cell.get("text", "")
            note = cell.get("note", "")
            note_html = f'<div class="cell-note">{escape(note)}</div>' if note else ""
            rows_html += f"""
            <div class="viz-heatmap-cell {color}">
              <div class="cell-text">{escape(text)}</div>
              {note_html}
            </div>
            """

    title_html = f'<div class="viz-heatmap-title">{escape(title)}</div>' if title else ""
    subtitle_html = f'<div class="viz-heatmap-subtitle">{escape(subtitle)}</div>' if subtitle else ""

    return f"""
<div class="viz-heatmap">
  {title_html}
  {subtitle_html}
  <div class="viz-heatmap-grid" style="grid-template-columns: {grid_cols};">
    {header_html}
    {rows_html}
  </div>
</div>
"""


# ============================================================
# COMPONENT 4: FLOW BRIDGE
# ============================================================
def flow_bridge(nodes: list[dict], title: str = "") -> str:
    """
    Vertical flow chain - cause → effect → result.

    Args:
        nodes: [{"text": str, "type": "cause"|"intermediate"|"result"}]
        title: optional heading
    """
    n = len(nodes)
    # SVG layout: viewBox 360x(n*60+padding), node width 280, height 36, gap 24
    node_w, node_h, gap = 280, 36, 22
    cx = 40
    svg_w = 360
    svg_h = n * node_h + (n - 1) * gap + 20

    elems = []
    type_colors = {
        "cause": "#003153",
        "intermediate": "#FAF7F0",
        "result": "#B5A642",
    }
    type_strokes = {
        "cause": "none",
        "intermediate": "#4A6FA5",
        "result": "none",
    }
    for i, node in enumerate(nodes):
        node_type = node.get("type", "intermediate")
        text = node.get("text", "")
        y = 10 + i * (node_h + gap)
        text_color = "#FAF7F0" if node_type == "cause" else "#003153"
        bg = type_colors.get(node_type, "#FAF7F0")
        stroke = type_strokes.get(node_type, "none")
        stroke_attr = f'stroke="{stroke}" stroke-width="0.8"' if stroke != "none" else 'stroke="none"'

        # Wrap text if too long - dùng smart_wrap (Wave 1)
        max_chars = 42
        if len(text) > max_chars:
            line1, line2 = smart_wrap(text, max_chars)
            text_svg = f"""
            <text x="{cx + node_w/2}" y="{y + node_h/2 - 2}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="9" font-weight="600" fill="{text_color}">{escape(line1)}</text>
            <text x="{cx + node_w/2}" y="{y + node_h/2 + 11}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="9" font-weight="600" fill="{text_color}">{escape(line2)}</text>
            """
        else:
            text_svg = f'<text x="{cx + node_w/2}" y="{y + node_h/2 + 4}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="9" font-weight="600" fill="{text_color}">{escape(text)}</text>'

        elems.append(f"""
        <rect x="{cx}" y="{y}" width="{node_w}" height="{node_h}" rx="3" fill="{bg}" {stroke_attr}/>
        {text_svg}
        """)

        # Arrow to next
        if i < n - 1:
            arrow_y_start = y + node_h
            arrow_y_end = arrow_y_start + gap - 4
            ax = cx + node_w / 2
            elems.append(f"""
            <line x1="{ax}" y1="{arrow_y_start}" x2="{ax}" y2="{arrow_y_end}" stroke="#4A6FA5" stroke-width="1.2"/>
            <polygon points="{ax-3},{arrow_y_end-1} {ax+3},{arrow_y_end-1} {ax},{arrow_y_end+4}" fill="#4A6FA5"/>
            """)

    title_html = f'<div class="viz-flow-title">{escape(title)}</div>' if title else ""

    return f"""
<div class="viz-flow">
  {title_html}
  <svg class="viz-flow-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    {''.join(elems)}
  </svg>
</div>
"""


# ============================================================
# COMPONENT 5: SCENARIO CARDS
# ============================================================
def scenario_cards(scenarios: list[dict]) -> str:
    """
    3-card grid cho 3 kịch bản với probability badge.

    Args:
        scenarios: [{
            "name": str,
            "type": "base"|"positive"|"negative",
            "probability": int (0-100),
            "timing": str,
            "decision": str,
            "winners": str,
            "losers": str,
        }]
    """
    cards_html = []
    for s in scenarios:
        name = escape(s.get("name", ""))
        s_type = s.get("type", "base")
        prob = s.get("probability", 0)
        timing = escape(s.get("timing", ""))
        decision = escape(s.get("decision", ""))
        winners = escape(s.get("winners", ""))
        losers = escape(s.get("losers", ""))

        cards_html.append(f"""
        <div class="viz-scenario {s_type}">
          <div class="viz-scenario-header">
            <div class="viz-scenario-name">{name}</div>
            <div class="viz-scenario-prob">~{prob}%</div>
          </div>
          <div class="viz-scenario-row">
            <div class="viz-scenario-label">Thời điểm</div>
            <div class="viz-scenario-value">{timing}</div>
          </div>
          <div class="viz-scenario-row">
            <div class="viz-scenario-label">Quyết định</div>
            <div class="viz-scenario-value">{decision}</div>
          </div>
          <div class="viz-scenario-row">
            <div class="viz-scenario-label">Người hưởng lợi</div>
            <div class="viz-scenario-value winners">{winners}</div>
          </div>
          <div class="viz-scenario-row">
            <div class="viz-scenario-label">Người chịu thiệt</div>
            <div class="viz-scenario-value losers">{losers}</div>
          </div>
        </div>
        """)

    return f"""
<div class="viz-scenarios">
  {''.join(cards_html)}
</div>
"""


# ============================================================
# COMPONENT 6: TIMELINE HORIZONTAL
# ============================================================
def timeline_horizontal(events: list[dict], title: str = "") -> str:
    """
    Horizontal timeline với milestones.

    Args:
        events: [{"date": str, "label": str, "type": "milestone"|"decision"|"result"|"current"}]
        title: optional heading
    """
    n = len(events)
    if n == 0:
        return ""

    # SVG layout: width 600, height ~80, dots evenly spaced
    svg_w, svg_h = 600, 90
    margin_x = 30
    axis_y = 40
    usable_w = svg_w - 2 * margin_x
    gap = usable_w / (n - 1) if n > 1 else 0

    elems = [
        f'<line x1="{margin_x}" y1="{axis_y}" x2="{svg_w - margin_x}" y2="{axis_y}" stroke="#4A6FA5" stroke-width="0.8"/>'
    ]

    type_dot_colors = {
        "milestone": "#4A6FA5",
        "decision": "#B5A642",
        "result": "#2E7D52",
        "current": "#C0392B",
    }

    for i, ev in enumerate(events):
        x = margin_x + i * gap
        ev_type = ev.get("type", "milestone")
        date = ev.get("date", "")
        label = ev.get("label", "")
        dot_color = type_dot_colors.get(ev_type, "#4A6FA5")

        # Wrap label nếu dài - dùng smart_wrap (Wave 1)
        max_chars = 16
        if len(label) > max_chars:
            line1, line2 = smart_wrap(label, max_chars)
            label_svg = f"""
            <text x="{x}" y="{axis_y + 22}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="8" fill="#2B2B2B">{escape(line1)}</text>
            <text x="{x}" y="{axis_y + 32}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="8" fill="#2B2B2B">{escape(line2)}</text>
            """
        else:
            label_svg = f'<text x="{x}" y="{axis_y + 22}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="8" fill="#2B2B2B">{escape(label)}</text>'

        # Tick line and dot
        elems.append(f'<line x1="{x}" y1="{axis_y - 4}" x2="{x}" y2="{axis_y + 4}" stroke="#4A6FA5" stroke-width="0.8"/>')
        elems.append(f'<circle cx="{x}" cy="{axis_y}" r="5" fill="{dot_color}"/>')
        # Date above
        elems.append(f'<text x="{x}" y="{axis_y - 10}" text-anchor="middle" font-family="JBM,JBMVN,monospace" font-size="7" font-weight="600" fill="#003153">{escape(date)}</text>')
        # Label below
        elems.append(label_svg)

    title_html = f'<div class="viz-timeline-title">{escape(title)}</div>' if title else ""

    return f"""
<div class="viz-timeline">
  {title_html}
  <svg class="viz-timeline-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">
    {''.join(elems)}
  </svg>
</div>
"""


# ============================================================
# WAVE 2 COMPONENTS - 6 atomic mới
# ============================================================

WAVE2_STYLES = r"""
/* ---------- WATERFALL CHART ---------- */
.viz-waterfall {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-waterfall-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-waterfall-subtitle {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; color: #4A6FA5; margin-bottom: 4mm;
}
.viz-waterfall-svg { display: block; width: 100%; height: auto; }

/* ---------- RANKING LADDER ---------- */
.viz-ranking {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-ranking-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-ranking-subtitle {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; color: #4A6FA5; margin-bottom: 4mm;
}
.viz-ranking-row {
  display: grid; grid-template-columns: 8mm 1fr 18mm 14mm;
  gap: 8px; align-items: center;
  padding: 6px 0; border-bottom: 0.4px solid rgba(74,111,165,0.10);
}
.viz-ranking-rank {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 11pt; font-weight: 700; color: #B5A642;
  text-align: center;
}
.viz-ranking-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9pt; font-weight: 700; color: #003153;
}
.viz-ranking-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 600; color: #003153;
  text-align: right;
}
.viz-ranking-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; font-weight: 600;
  text-align: right;
}
.viz-ranking-delta.up { color: #2E7D52; }
.viz-ranking-delta.down { color: #C0392B; }
.viz-ranking-delta.flat { color: #6B6760; }
.viz-ranking-delta.new { color: #B5A642; font-style: italic; }

/* ---------- COMPARISON CARDS ---------- */
.viz-comparison {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-comparison-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-comparison-grid {
  display: grid; gap: 4mm;
}
.viz-comparison-grid.cols-2 { grid-template-columns: 1fr 1fr; }
.viz-comparison-grid.cols-3 { grid-template-columns: 1fr 1fr 1fr; }
.viz-comparison-grid.cols-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.viz-comparison-card {
  background: #FAF7F0; padding: 5mm;
  border-top: 3px solid #4A6FA5;
  border-radius: 2px;
  page-break-inside: avoid;
}
.viz-comparison-card.fork-a { border-top-color: #B5A642; }
.viz-comparison-card.fork-b { border-top-color: #4A6FA5; }
.viz-comparison-card.positive { border-top-color: #2E7D52; }
.viz-comparison-card.negative { border-top-color: #C0392B; }
.viz-comparison-card.neutral { border-top-color: #6B6760; }
.viz-comparison-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 2mm;
}
.viz-comparison-card-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 12pt; font-weight: 700; color: #003153;
  margin-bottom: 3mm; line-height: 1.25;
}
.viz-comparison-metrics {
  margin-bottom: 3mm; padding-bottom: 3mm;
  border-bottom: 0.5px solid rgba(74,111,165,0.15);
}
.viz-comparison-metric-row {
  display: flex; justify-content: space-between;
  padding: 3px 0; font-size: 8.5pt;
}
.viz-comparison-metric-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  color: #6B6760;
}
.viz-comparison-metric-value {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-weight: 600; color: #003153;
}
.viz-comparison-summary {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; line-height: 1.5;
  color: #2B2B2B; font-style: italic;
}

/* ---------- STAT DASHBOARD ---------- */
.viz-dashboard {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-dashboard-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-dashboard-grid {
  display: grid; gap: 3mm;
}
.viz-dashboard-grid.cols-2 { grid-template-columns: 1fr 1fr; }
.viz-dashboard-grid.cols-3 { grid-template-columns: 1fr 1fr 1fr; }
.viz-dashboard-grid.cols-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.viz-dashboard-stat {
  background: #FAF7F0; padding: 4mm 5mm;
  border-left: 2px solid #B5A642;
  border-radius: 2px;
  page-break-inside: avoid;
}
.viz-dashboard-stat-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #6B6760; margin-bottom: 2mm;
}
.viz-dashboard-stat-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 17pt; font-weight: 700; color: #003153;
  line-height: 1.1; margin-bottom: 1mm;
}
.viz-dashboard-stat-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; font-weight: 600;
}
.viz-dashboard-stat-delta.up { color: #2E7D52; }
.viz-dashboard-stat-delta.down { color: #C0392B; }
.viz-dashboard-stat-delta.flat { color: #6B6760; }
.viz-dashboard-stat-unit {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; color: #6B6760;
  margin-top: 2px;
}

/* ---------- MINI SPARKLINE (inline) ---------- */
.viz-sparkline {
  display: inline-block;
  vertical-align: -1px;
  margin: 0 2px;
}

/* ---------- DISTRIBUTION DOT PLOT ---------- */
.viz-distribution {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-distribution-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm; padding-bottom: 3px;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-distribution-svg { display: block; width: 100%; height: auto; margin-top: 4mm; }
"""


# ============================================================
# COMPONENT 7: WATERFALL CHART
# ============================================================
def waterfall(
    title: str,
    start: dict,
    steps: list[dict],
    end: dict,
    value_format: str = "{:.1f}%",
    subtitle: str = "",
) -> str:
    """
    Waterfall chart: A → through additions/subtractions → B.

    Args:
        title: heading
        start: {"label": str, "value": float}
        steps: list of {"label": str, "value": float, "type": "positive"|"negative"}
        end: {"label": str, "value": float}
        value_format: Python format string
        subtitle: optional

    Use case:
        - LDR Big4 trước/sau sửa đổi: 95% → +10 TGKB → -5 TT2 → 100%
        - P&L bridge: Q1 EPS → Q2 EPS với drivers
        - Capital walk: starting → drivers → ending
    """
    # Compute cumulative values for positioning
    cumulative = start["value"]
    bar_data = []  # list of {label, value, top, height, type}
    bar_data.append({"label": start["label"], "value": start["value"], "bottom": 0, "top": cumulative, "type": "start"})
    for step in steps:
        prev = cumulative
        delta = step["value"]
        cumulative += delta
        if delta >= 0:
            bar_data.append({"label": step["label"], "value": delta, "bottom": prev, "top": cumulative, "type": "positive"})
        else:
            bar_data.append({"label": step["label"], "value": delta, "bottom": cumulative, "top": prev, "type": "negative"})
    bar_data.append({"label": end["label"], "value": end["value"], "bottom": 0, "top": end["value"], "type": "end"})

    # Find min/max for scale
    all_tops = [b["top"] for b in bar_data]
    all_bottoms = [b["bottom"] for b in bar_data]
    y_max = max(all_tops) * 1.10
    y_min = min(0, min(all_bottoms) * 0.9)
    y_range = y_max - y_min

    # SVG layout
    n = len(bar_data)
    svg_w = 600
    svg_h = 280
    margin_top, margin_bottom, margin_left, margin_right = 30, 50, 30, 20
    chart_w = svg_w - margin_left - margin_right
    chart_h = svg_h - margin_top - margin_bottom
    bar_gap_ratio = 0.3
    bar_w = chart_w / n * (1 - bar_gap_ratio)
    bar_step = chart_w / n

    type_colors = {
        "start": "#003153",
        "end": "#003153",
        "positive": "#2E7D52",
        "negative": "#C0392B",
    }

    elems = []
    # Y-axis baseline at value 0
    y0_pos = margin_top + (y_max - 0) / y_range * chart_h
    elems.append(f'<line x1="{margin_left}" y1="{y0_pos}" x2="{svg_w - margin_right}" y2="{y0_pos}" stroke="#4A6FA5" stroke-width="0.6" stroke-opacity="0.4"/>')

    # Bars + labels + connectors
    for i, bar in enumerate(bar_data):
        x = margin_left + i * bar_step + (bar_step - bar_w) / 2
        y_top = margin_top + (y_max - bar["top"]) / y_range * chart_h
        y_bottom = margin_top + (y_max - bar["bottom"]) / y_range * chart_h
        bar_h = abs(y_bottom - y_top)
        y = min(y_top, y_bottom)

        color = type_colors.get(bar["type"], "#4A6FA5")
        elems.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{color}" rx="1.5"/>')

        # Value label trên top
        if bar["type"] in ("start", "end"):
            val_label = value_format.format(bar["value"]).replace(".", ",")
        else:
            sign = "+" if bar["value"] >= 0 else ""
            val_label = f'{sign}{value_format.format(bar["value"]).replace(".", ",")}'
        elems.append(f'<text x="{x + bar_w/2:.1f}" y="{y - 4:.1f}" text-anchor="middle" font-family="JBM,JBMVN,monospace" font-size="8" font-weight="600" fill="#003153">{val_label}</text>')

        # Label dưới đáy
        label = bar["label"]
        if len(label) > 18:
            l1, l2 = smart_wrap(label, 18)
            elems.append(f'<text x="{x + bar_w/2:.1f}" y="{svg_h - margin_bottom + 14:.1f}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="7.5" fill="#2B2B2B">{escape(l1)}</text>')
            elems.append(f'<text x="{x + bar_w/2:.1f}" y="{svg_h - margin_bottom + 24:.1f}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="7.5" fill="#2B2B2B">{escape(l2)}</text>')
        else:
            elems.append(f'<text x="{x + bar_w/2:.1f}" y="{svg_h - margin_bottom + 14:.1f}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="7.5" fill="#2B2B2B">{escape(label)}</text>')

        # Connector line đến bar tiếp theo
        if i < n - 1:
            next_bar = bar_data[i + 1]
            x_end_current = x + bar_w
            x_start_next = margin_left + (i + 1) * bar_step + (bar_step - bar_w) / 2
            # Connector ở top của current bar (vì waterfall flow)
            connector_y_pos = margin_top + (y_max - bar["top"]) / y_range * chart_h
            # Nếu next là negative, connector ở top của next (= bottom of next)
            if next_bar["type"] == "negative":
                connector_y_pos = margin_top + (y_max - next_bar["top"]) / y_range * chart_h
            elif next_bar["type"] == "end":
                connector_y_pos = margin_top + (y_max - bar["top"]) / y_range * chart_h
            elems.append(f'<line x1="{x_end_current:.1f}" y1="{connector_y_pos:.1f}" x2="{x_start_next:.1f}" y2="{connector_y_pos:.1f}" stroke="#6B6760" stroke-width="0.6" stroke-dasharray="2,2"/>')

    title_html = f'<div class="viz-waterfall-title">{escape(title)}</div>' if title else ""
    subtitle_html = f'<div class="viz-waterfall-subtitle">{escape(subtitle)}</div>' if subtitle else ""

    return f"""
<div class="viz-waterfall">
  {title_html}
  {subtitle_html}
  <svg class="viz-waterfall-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    {''.join(elems)}
  </svg>
</div>
"""


# ============================================================
# COMPONENT 8: RANKING LADDER
# ============================================================
def ranking_ladder(
    title: str,
    items: list[dict],
    value_unit: str = "%",
    subtitle: str = "",
    auto_sector_color: bool = False,
) -> str:
    """
    Ranking 5-10 entities with delta arrows (vs prev period).

    Args:
        items: [{
            "rank": int,
            "label": str,           # ticker hoặc name
            "value": float,
            "prev_rank": int|None,  # None = new entry
            "delta": int|None,      # +2, -1, 0; None = new
        }]
        value_unit: "%" hoặc "" hoặc unit khác
        auto_sector_color: nếu True và label là ticker, color theo sector
    """
    rows_html = []
    for it in items:
        rank = it["rank"]
        label = escape(it["label"])
        value = it["value"]
        delta = it.get("delta")
        prev_rank = it.get("prev_rank")

        # Format value
        if isinstance(value, float) and not value.is_integer():
            val_str = f"{value:.1f}".replace(".", ",")
        else:
            val_str = f"{value:.0f}"
        val_str = f"{val_str}{value_unit}"

        # Delta indicator
        if prev_rank is None:
            delta_html = '<div class="viz-ranking-delta new">MỚI</div>'
        elif delta is None or delta == 0:
            delta_html = '<div class="viz-ranking-delta flat">─</div>'
        elif delta > 0:
            delta_html = f'<div class="viz-ranking-delta up">↑ {delta}</div>'
        else:
            delta_html = f'<div class="viz-ranking-delta down">↓ {abs(delta)}</div>'

        # Auto sector color cho label
        if auto_sector_color:
            try:
                color = color_for_ticker(it["label"])
                label_style = f' style="color: {color};"'
            except Exception:
                label_style = ""
        else:
            label_style = ""

        rows_html.append(f"""
        <div class="viz-ranking-row">
          <div class="viz-ranking-rank">{rank}</div>
          <div class="viz-ranking-label"{label_style}>{label}</div>
          <div class="viz-ranking-value">{val_str}</div>
          {delta_html}
        </div>
        """)

    title_html = f'<div class="viz-ranking-title">{escape(title)}</div>' if title else ""
    subtitle_html = f'<div class="viz-ranking-subtitle">{escape(subtitle)}</div>' if subtitle else ""

    return f"""
<div class="viz-ranking">
  {title_html}
  {subtitle_html}
  {''.join(rows_html)}
</div>
"""


# ============================================================
# COMPONENT 9: COMPARISON CARDS
# ============================================================
def comparison_cards(
    cards: list[dict],
    layout: str = "2-up",
    title: str = "",
) -> str:
    """
    Side-by-side comparison cards.

    Args:
        cards: list of {
            "label": str,           # eyebrow ("Phương án A")
            "title": str,           # card title ("Nới SFL 30%→35%")
            "type": "fork-a"|"fork-b"|"positive"|"negative"|"neutral",
            "key_metrics": list of {"label": str, "value": str},
            "summary": str,         # italic footer
        }
        layout: "2-up", "3-up", "4-up"
        title: optional heading
    """
    layout_map = {"2-up": "cols-2", "3-up": "cols-3", "4-up": "cols-4"}
    grid_class = layout_map.get(layout, "cols-2")

    cards_html = []
    for card in cards:
        ctype = card.get("type", "neutral")
        label = escape(card.get("label", ""))
        ctitle = escape(card.get("title", ""))
        summary = escape(card.get("summary", ""))
        metrics = card.get("key_metrics", [])

        metrics_html = ""
        if metrics:
            metric_rows = []
            for m in metrics:
                metric_rows.append(f"""
                <div class="viz-comparison-metric-row">
                  <span class="viz-comparison-metric-label">{escape(m.get("label", ""))}</span>
                  <span class="viz-comparison-metric-value">{escape(m.get("value", ""))}</span>
                </div>
                """)
            metrics_html = f'<div class="viz-comparison-metrics">{"".join(metric_rows)}</div>'

        summary_html = f'<div class="viz-comparison-summary">{summary}</div>' if summary else ""

        cards_html.append(f"""
        <div class="viz-comparison-card {ctype}">
          <div class="viz-comparison-label">{label}</div>
          <div class="viz-comparison-card-title">{ctitle}</div>
          {metrics_html}
          {summary_html}
        </div>
        """)

    title_html = f'<div class="viz-comparison-title">{escape(title)}</div>' if title else ""

    return f"""
<div class="viz-comparison">
  {title_html}
  <div class="viz-comparison-grid {grid_class}">
    {''.join(cards_html)}
  </div>
</div>
"""


# ============================================================
# COMPONENT 10: STAT DASHBOARD
# ============================================================
def stat_dashboard(
    stats: list[dict],
    layout: str = "3-cols",
    title: str = "",
) -> str:
    """
    Grid of 4-6 stat cards với label + value + delta.

    Args:
        stats: list of {
            "label": str,           # uppercase
            "value": str,           # formatted display
            "delta": str,           # "+1,2pp" hoặc None
            "delta_type": "up"|"down"|"flat",
            "unit": str (optional)  # "tỷ VND" subscript
        }
        layout: "2-cols", "3-cols", "4-cols"
        title: optional heading
    """
    layout_map = {"2-cols": "cols-2", "3-cols": "cols-3", "4-cols": "cols-4"}
    grid_class = layout_map.get(layout, "cols-3")

    stats_html = []
    for s in stats:
        label = escape(s.get("label", ""))
        value = escape(s.get("value", ""))
        delta = s.get("delta")
        delta_type = s.get("delta_type", "flat")
        unit = s.get("unit", "")

        delta_html = ""
        if delta:
            arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "─")
            delta_html = f'<div class="viz-dashboard-stat-delta {delta_type}">{arrow} {escape(delta)}</div>'

        unit_html = f'<div class="viz-dashboard-stat-unit">{escape(unit)}</div>' if unit else ""

        stats_html.append(f"""
        <div class="viz-dashboard-stat">
          <div class="viz-dashboard-stat-label">{label}</div>
          <div class="viz-dashboard-stat-value">{value}</div>
          {delta_html}
          {unit_html}
        </div>
        """)

    title_html = f'<div class="viz-dashboard-title">{escape(title)}</div>' if title else ""

    return f"""
<div class="viz-dashboard">
  {title_html}
  <div class="viz-dashboard-grid {grid_class}">
    {''.join(stats_html)}
  </div>
</div>
"""


# ============================================================
# COMPONENT 11: MINI SPARKLINE (inline)
# ============================================================
def sparkline(
    values: list[float],
    type: str = "line",
    color: str = "auto",
    size: str = "small",
) -> str:
    """
    Inline mini chart 50x14px (small) hoặc 80x20px (medium).

    Args:
        values: list of numeric values (4-12 ideal)
        type: "line" hoặc "bar"
        color: "auto" (theo trend) hoặc hex color
        size: "small" (50x14), "medium" (80x20), "large" (120x28)

    Use inline:
        f'VPB CASA chỉ ~12% {sparkline([14,13,12.5,12.1,12])} giảm liên tục'
    """
    if not values or len(values) < 2:
        return ""

    sizes = {"small": (50, 14), "medium": (80, 20), "large": (120, 28)}
    w, h = sizes.get(size, sizes["small"])

    # Auto color theo trend
    if color == "auto":
        first, last = values[0], values[-1]
        if last > first * 1.02:
            color = "#2E7D52"  # green
        elif last < first * 0.98:
            color = "#C0392B"  # red
        else:
            color = "#B5A642"  # brass

    v_min = min(values)
    v_max = max(values)
    v_range = v_max - v_min if v_max != v_min else 1

    # Padding inside SVG
    pad = 1
    chart_w = w - 2 * pad
    chart_h = h - 2 * pad

    # Compute points
    points = []
    for i, v in enumerate(values):
        x = pad + (i / (len(values) - 1)) * chart_w
        y = pad + chart_h - ((v - v_min) / v_range) * chart_h
        points.append((x, y))

    if type == "line":
        path_d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for x, y in points[1:]:
            path_d += f" L {x:.1f} {y:.1f}"
        chart_svg = f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/>'
    else:  # bar
        bar_w = chart_w / len(values) * 0.7
        bars = []
        for x, y in points:
            bars.append(f'<rect x="{x - bar_w/2:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{pad + chart_h - y:.1f}" fill="{color}"/>')
        chart_svg = "".join(bars)

    return f'<svg class="viz-sparkline" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{chart_svg}</svg>'


# ============================================================
# COMPONENT 12: DISTRIBUTION DOT PLOT
# ============================================================
def distribution_dot_plot(
    title: str,
    items: list[dict],
    x_label: str = "",
    x_range: tuple = None,
    annotations: list[dict] = None,
    subtitle: str = "",
) -> str:
    """
    Horizontal dot plot - position items on axis (e.g. CASA distribution).

    Args:
        items: list of {"label": str, "value": float, "highlight": bool (optional)}
        x_label: axis label
        x_range: (min, max) tuple; nếu None thì auto from values
        annotations: optional [{"value": float, "text": str}] - reference lines
    """
    values = [it["value"] for it in items]
    if x_range is None:
        x_min = min(values) * 0.95
        x_max = max(values) * 1.05
    else:
        x_min, x_max = x_range
    x_span = x_max - x_min if x_max != x_min else 1

    # SVG layout
    svg_w = 600
    svg_h = 140
    margin_left, margin_right = 35, 35
    margin_top, margin_bottom = 30, 35
    axis_y = svg_h - margin_bottom

    elems = []

    # X-axis line
    elems.append(f'<line x1="{margin_left}" y1="{axis_y}" x2="{svg_w - margin_right}" y2="{axis_y}" stroke="#4A6FA5" stroke-width="0.8"/>')

    # X-axis ticks (5 ticks)
    n_ticks = 5
    for i in range(n_ticks):
        tick_val = x_min + (x_max - x_min) * i / (n_ticks - 1)
        tick_x = margin_left + (svg_w - margin_left - margin_right) * i / (n_ticks - 1)
        elems.append(f'<line x1="{tick_x:.1f}" y1="{axis_y - 3}" x2="{tick_x:.1f}" y2="{axis_y + 3}" stroke="#4A6FA5" stroke-width="0.6"/>')
        tick_label = f"{tick_val:.0f}".replace(".", ",")
        elems.append(f'<text x="{tick_x:.1f}" y="{axis_y + 14}" text-anchor="middle" font-family="JBM,JBMVN,monospace" font-size="7" fill="#6B6760">{tick_label}</text>')

    # X-axis label
    if x_label:
        elems.append(f'<text x="{svg_w/2}" y="{svg_h - 5}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="600" fill="#003153">{escape(x_label)}</text>')

    # Reference annotations (lines + labels)
    if annotations:
        for ann in annotations:
            ann_val = ann["value"]
            ann_text = ann["text"]
            ann_x = margin_left + ((ann_val - x_min) / x_span) * (svg_w - margin_left - margin_right)
            elems.append(f'<line x1="{ann_x:.1f}" y1="{margin_top}" x2="{ann_x:.1f}" y2="{axis_y}" stroke="#722F37" stroke-width="0.6" stroke-dasharray="2,2" stroke-opacity="0.5"/>')
            elems.append(f'<text x="{ann_x:.1f}" y="{margin_top - 6}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="7" font-style="italic" fill="#722F37">{escape(ann_text)}</text>')

    # Plot dots với offset cho overlapping
    # Group items by approx x position để stack dots
    sorted_items = sorted(items, key=lambda x: x["value"])
    x_positions = {}
    for it in sorted_items:
        ax = margin_left + ((it["value"] - x_min) / x_span) * (svg_w - margin_left - margin_right)
        # Find existing close x (within 6px)
        stack_idx = 0
        for existing_x, count in x_positions.items():
            if abs(ax - existing_x) < 6:
                stack_idx = count
                x_positions[existing_x] = count + 1
                ax = existing_x  # snap to existing
                break
        else:
            x_positions[ax] = 1

        # Y offset for stacking
        ay = axis_y - 8 - (stack_idx * 7)

        # Dot
        radius = 4 if it.get("highlight", False) else 2.5
        fill = "#B5A642" if it.get("highlight", False) else "#4A6FA5"
        elems.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{radius}" fill="{fill}" stroke="#FAF7F0" stroke-width="0.6"/>')

        # Label cho highlighted items
        if it.get("highlight", False):
            elems.append(f'<text x="{ax:.1f}" y="{ay - 8}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="7.5" font-weight="700" fill="#003153">{escape(it["label"])}</text>')

    title_html = f'<div class="viz-distribution-title">{escape(title)}</div>' if title else ""
    subtitle_html = f'<div class="viz-distribution-subtitle">{escape(subtitle)}</div>' if subtitle else ""

    return f"""
<div class="viz-distribution">
  {title_html}
  {subtitle_html}
  <svg class="viz-distribution-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    {''.join(elems)}
  </svg>
</div>
"""


# ============================================================
# WAVE 3 COMPOSITE COMPONENTS (8 total)
# ============================================================

WAVE3_STYLES = r"""
/* ---------- POLICY FORK ---------- */
.viz-policy-fork {
  margin: 8mm 0; page-break-inside: avoid;
}
.viz-policy-fork-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 14pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm;
}
.viz-policy-fork-context {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9.5pt; font-weight: 450; color: #4A6FA5;
  font-style: italic;
  margin-bottom: 5mm; padding-bottom: 4mm;
  border-bottom: 0.6px solid rgba(74,111,165,0.18);
}
.viz-policy-fork-options {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 4mm; margin-bottom: 5mm;
}
.viz-policy-fork-option {
  background: #FAF7F0; padding: 5mm;
  border-top: 3px solid #B5A642;
  border-radius: 2px;
}
.viz-policy-fork-option.fork-a { border-top-color: #B5A642; }
.viz-policy-fork-option.fork-b { border-top-color: #4A6FA5; }
.viz-policy-fork-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 2mm;
}
.viz-policy-fork-option.fork-b .viz-policy-fork-label { color: #4A6FA5; }
.viz-policy-fork-name {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 12pt; font-weight: 700; color: #003153;
  margin-bottom: 3mm; line-height: 1.25;
}
.viz-policy-fork-winners {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; font-weight: 600;
  color: #2E7D52; margin-bottom: 3mm;
}
.viz-policy-fork-summary {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9pt; font-weight: 450;
  font-style: italic; color: #2B2B2B;
  line-height: 1.5;
}
.viz-policy-fork-decision {
  background: #FAF7F0;
  padding: 5mm 6mm;
  border-top: 2px solid #003153;
}
.viz-policy-fork-decision-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: #6B6760; margin-bottom: 4mm;
}
/* Header row with A / B columns */
.viz-policy-fork-factor-header {
  display: grid; grid-template-columns: 1fr 16mm 16mm;
  gap: 3mm; padding: 0 0 3mm 0;
  border-bottom: 1px solid #003153;
  margin-bottom: 1mm;
  align-items: baseline;
}
.viz-policy-fork-factor-header-name {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #6B6760;
}
.viz-policy-fork-factor-header-col {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9.5pt; font-weight: 700;
  text-align: center; letter-spacing: 0.1em;
}
.viz-policy-fork-factor-header-col.fork-a { color: #B5A642; }
.viz-policy-fork-factor-header-col.fork-b { color: #4A6FA5; }
.viz-policy-fork-factor {
  display: grid; grid-template-columns: 1fr 16mm 16mm;
  gap: 3mm; padding: 2.5mm 0;
  border-bottom: 0.4px solid rgba(74,111,165,0.10);
  font-size: 9pt;
  align-items: center;
}
.viz-policy-fork-factor:last-child { border-bottom: none; }
.viz-policy-fork-factor-label {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; color: #2B2B2B;
}
/* Filled / empty circles - colored by column */
.viz-policy-fork-factor-mark {
  text-align: center;
  font-size: 13pt; line-height: 1;
}
.viz-policy-fork-factor-mark.win-a { color: #B5A642; }
.viz-policy-fork-factor-mark.win-b { color: #4A6FA5; }
.viz-policy-fork-factor-mark.lose { color: rgba(74,111,165,0.18); }

/* ---------- WINNERS-LOSERS SPLIT ---------- */
.viz-wl {
  margin: 8mm 0; page-break-inside: avoid;
}
.viz-wl-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 14pt; font-weight: 700; color: #003153;
  margin-bottom: 2mm;
}
.viz-wl-summary {
  background: #003153; color: #FAF7F0;
  padding: 4mm 6mm;
  margin-bottom: 5mm;
  display: grid; grid-template-columns: 32mm 1fr;
  gap: 5mm; align-items: center;
}
.viz-wl-summary-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 18pt; font-weight: 700; color: #B5A642;
  line-height: 1;
}
.viz-wl-summary-label {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9pt; font-weight: 450;
  font-style: italic; color: rgba(250,247,240,0.85);
  line-height: 1.4;
}
.viz-wl-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 5mm;
}
.viz-wl-column {
  background: #FAF7F0; padding: 5mm;
  border-top: 3px solid;
}
.viz-wl-column.winners { border-top-color: #2E7D52; }
.viz-wl-column.losers { border-top-color: #C0392B; }
.viz-wl-col-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  margin-bottom: 2mm;
}
.viz-wl-column.winners .viz-wl-col-label { color: #2E7D52; }
.viz-wl-column.losers .viz-wl-col-label { color: #C0392B; }
.viz-wl-col-summary {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9pt; font-weight: 500;
  font-style: italic; color: #2B2B2B;
  margin-bottom: 4mm; padding-bottom: 3mm;
  border-bottom: 0.5px solid rgba(74,111,165,0.18);
}
.viz-wl-item {
  padding: 3mm 0;
  border-bottom: 0.4px solid rgba(74,111,165,0.10);
}
.viz-wl-item:last-child { border-bottom: none; }
.viz-wl-item-row {
  display: flex; justify-content: space-between;
  margin-bottom: 1mm; align-items: baseline;
}
.viz-wl-item-name {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9.5pt; font-weight: 700;
  color: #003153;
}
.viz-wl-item-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9.5pt; font-weight: 700;
}
.viz-wl-column.winners .viz-wl-item-value { color: #2E7D52; }
.viz-wl-column.losers .viz-wl-item-value { color: #C0392B; }
.viz-wl-item-detail {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 8.5pt; font-weight: 450;
  color: #6B6760;
  line-height: 1.4;
}

/* ---------- DATA HERO ---------- */
.viz-hero {
  margin: 10mm 0; page-break-inside: avoid;
  background: #FAF7F0;
  padding: 12mm 10mm;
  border-top: 3px solid #B5A642;
  border-bottom: 3px solid #B5A642;
  text-align: center;
}
.viz-hero-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 6mm;
}
.viz-hero-mega {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 80pt; font-weight: 700;
  color: #003153;
  line-height: 1;
  letter-spacing: -0.02em;
  margin-bottom: 2mm;
}
.viz-hero-unit {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 11pt; font-weight: 600;
  letter-spacing: 0.06em;
  color: #4A6FA5; margin-bottom: 4mm;
}
.viz-hero-label {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 12pt; font-weight: 500;
  font-style: italic;
  color: #003153; margin-bottom: 8mm;
  line-height: 1.4;
  max-width: 130mm; margin-left: auto; margin-right: auto;
}
.viz-hero-sub-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 5mm; margin-bottom: 6mm;
  padding-top: 5mm;
  border-top: 0.5px solid rgba(74,111,165,0.18);
}
.viz-hero-sub-stat {
  text-align: center;
}
.viz-hero-sub-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 16pt; font-weight: 700;
  color: #003153; line-height: 1;
  margin-bottom: 1mm;
}
.viz-hero-sub-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: #6B6760;
}
.viz-hero-story {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10pt; font-weight: 450;
  font-style: italic; color: #2B2B2B;
  line-height: 1.55;
  max-width: 140mm; margin: 0 auto;
}

/* ---------- MECHANISM BREAKDOWN ---------- */
.viz-mech {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-mech-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 700; color: #003153;
  margin-bottom: 4mm;
}
.viz-mech-stages {
  display: grid;
  grid-template-columns: 1fr 8mm 1fr 8mm 1fr;
  gap: 0; align-items: stretch;
  margin-bottom: 4mm;
}
.viz-mech-stage {
  background: #FAF7F0;
  padding: 5mm 4mm;
  border-top: 3px solid;
  border-radius: 2px;
}
.viz-mech-stage.input { border-top-color: #4A6FA5; }
.viz-mech-stage.process { border-top-color: #B5A642; }
.viz-mech-stage.output { border-top-color: #2E7D52; }
.viz-mech-arrow {
  display: flex; align-items: center;
  justify-content: center;
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 18pt; font-weight: 700;
  color: #B5A642;
}
.viz-mech-stage-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  margin-bottom: 2mm;
}
.viz-mech-stage.input .viz-mech-stage-label { color: #4A6FA5; }
.viz-mech-stage.process .viz-mech-stage-label { color: #B5A642; }
.viz-mech-stage.output .viz-mech-stage-label { color: #2E7D52; }
.viz-mech-stage-name {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 700;
  color: #003153; margin-bottom: 2mm;
  line-height: 1.25;
}
.viz-mech-stage-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 12pt; font-weight: 700;
  color: #003153; margin-bottom: 2mm;
}
.viz-mech-stage-detail {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 8.5pt; font-weight: 450;
  color: #4A6FA5;
  line-height: 1.45;
}
.viz-mech-outcome {
  background: #003153; color: #FAF7F0;
  padding: 4mm 6mm;
  border-left: 3px solid #B5A642;
}
.viz-mech-outcome-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 2mm;
}
.viz-mech-outcome-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10pt; font-weight: 500;
  font-style: italic;
  color: rgba(250,247,240,0.95);
  line-height: 1.5;
}

/* ---------- BEFORE-AFTER COMPARISON ---------- */
.viz-ba {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-ba-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 700; color: #003153;
  margin-bottom: 4mm;
}
.viz-ba-grid {
  display: grid; grid-template-columns: 1fr 18mm 1fr;
  gap: 0; align-items: stretch;
  margin-bottom: 4mm;
}
.viz-ba-state {
  padding: 5mm;
  background: #FAF7F0;
  border-top: 3px solid;
}
.viz-ba-state.before { border-top-color: #6B6760; opacity: 0.92; }
.viz-ba-state.after { border-top-color: #2E7D52; }
.viz-ba-state-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  margin-bottom: 2mm;
}
.viz-ba-state.before .viz-ba-state-label { color: #6B6760; }
.viz-ba-state.after .viz-ba-state-label { color: #2E7D52; }
.viz-ba-state-name {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9.5pt; font-weight: 500;
  font-style: italic; color: #4A6FA5;
  margin-bottom: 3mm;
}
.viz-ba-state-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 28pt; font-weight: 700;
  color: #003153; line-height: 1;
  margin-bottom: 4mm;
}
.viz-ba-metric {
  display: flex; justify-content: space-between;
  padding: 2mm 0; font-size: 8.5pt;
  border-bottom: 0.4px solid rgba(74,111,165,0.10);
}
.viz-ba-metric:last-child { border-bottom: none; }
.viz-ba-metric-label {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; color: #6B6760;
}
.viz-ba-metric-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 600; color: #003153;
}
.viz-ba-arrow {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
.viz-ba-arrow-symbol {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 22pt; font-weight: 700;
  color: #B5A642; line-height: 1;
}
.viz-ba-arrow-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 700;
  color: #2E7D52; margin-top: 2mm;
}
.viz-ba-changes {
  background: #FAF7F0;
  border-left: 3px solid #B5A642;
  padding: 4mm 5mm;
}
.viz-ba-changes-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 3mm;
}
.viz-ba-change {
  display: flex; justify-content: space-between;
  padding: 2mm 0; font-size: 9pt;
}
.viz-ba-change-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; color: #2B2B2B;
}
.viz-ba-change-impact {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 600; color: #003153;
}

/* ---------- EXECUTIVE SUMMARY BOX ---------- */
.viz-exec {
  margin: 8mm 0; page-break-inside: avoid;
}
.viz-exec-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642;
  margin-bottom: 3mm;
  padding-bottom: 2mm;
  border-bottom: 1px solid #B5A642;
}
.viz-exec-takeaway {
  background: #003153; color: #FAF7F0;
  padding: 6mm 7mm;
  margin-bottom: 4mm;
  border-left: 4px solid #B5A642;
}
.viz-exec-takeaway-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 3mm;
}
.viz-exec-takeaway-headline {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 600;
  color: #FAF7F0;
  line-height: 1.35; margin-bottom: 3mm;
}
.viz-exec-takeaway-body {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9.5pt; font-weight: 450;
  font-style: italic;
  color: rgba(250,247,240,0.85);
  line-height: 1.5;
}
.viz-exec-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 4mm;
}
.viz-exec-cell {
  background: #FAF7F0;
  padding: 4mm 5mm;
  border-top: 2px solid;
}
.viz-exec-cell.findings { border-top-color: #2E7D52; }
.viz-exec-cell.risks { border-top-color: #C0392B; }
.viz-exec-cell.watch { border-top-color: #4A6FA5; }
.viz-exec-cell-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  margin-bottom: 3mm;
}
.viz-exec-cell.findings .viz-exec-cell-label { color: #2E7D52; }
.viz-exec-cell.risks .viz-exec-cell-label { color: #C0392B; }
.viz-exec-cell.watch .viz-exec-cell-label { color: #4A6FA5; }
.viz-exec-bullet {
  display: grid; grid-template-columns: 4mm 1fr;
  gap: 2mm; padding: 2mm 0;
  font-size: 8.5pt;
  align-items: baseline;
}
.viz-exec-bullet-mark {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 700;
}
.viz-exec-cell.findings .viz-exec-bullet-mark { color: #2E7D52; }
.viz-exec-cell.risks .viz-exec-bullet-mark { color: #C0392B; }
.viz-exec-cell.watch .viz-exec-bullet-mark { color: #4A6FA5; }
.viz-exec-bullet-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; color: #2B2B2B;
  line-height: 1.45;
}

/* ---------- SCENARIO MATRIX ---------- */
.viz-matrix {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-matrix-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 700; color: #003153;
  margin-bottom: 4mm;
}
.viz-matrix-svg { display: block; width: 100%; height: auto; }

/* ---------- RISK RADAR ---------- */
.viz-radar {
  margin: 7mm 0; page-break-inside: avoid;
}
.viz-radar-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 700; color: #003153;
  margin-bottom: 4mm;
}
.viz-radar-svg { display: block; max-width: 130mm; height: auto; margin: 0 auto; }
.viz-radar-legend {
  display: flex; justify-content: center;
  gap: 8mm; margin-top: 3mm;
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 600;
}
.viz-radar-legend-item {
  display: flex; align-items: center; gap: 2mm;
}
.viz-radar-legend-swatch {
  width: 8px; height: 8px;
}
"""


# ============================================================
# COMPONENT 13: POLICY FORK (composite)
# ============================================================
def policy_fork(
    title: str,
    decision_context: str,
    options: list[dict],
    decision_factors: list[dict] = None,
) -> str:
    """
    Composite: 2 phương án + decision factors matrix.

    Args:
        options: 2 dicts:
            {
                "label": str,           # eyebrow ("Phương án A")
                "name": str,            # title ("Nới SFL 30% lên 35%")
                "type": "fork-a" | "fork-b",
                "winners": str,         # "TCB, VPB" - who benefits
                "summary": str,         # italic explanation
            }
        decision_factors: optional list of:
            {
                "factor": str,          # "Đơn giản triển khai"
                "winner": "A" | "B" | "both" | "neither"
            }
    """
    options_html = []
    for opt in options:
        otype = opt.get("type", "fork-a")
        winners_html = ""
        if opt.get("winners"):
            winners_html = f'<div class="viz-policy-fork-winners">→ {escape(opt["winners"])}</div>'

        options_html.append(f"""
        <div class="viz-policy-fork-option {otype}">
          <div class="viz-policy-fork-label">{escape(opt.get("label", ""))}</div>
          <div class="viz-policy-fork-name">{escape(opt.get("name", ""))}</div>
          {winners_html}
          <div class="viz-policy-fork-summary">{escape(opt.get("summary", ""))}</div>
        </div>
        """)

    factors_html = ""
    if decision_factors:
        # Get option labels for header (Phương án A → "A", Phương án B → "B")
        a_label = options[0].get("label", "Phương án A") if len(options) > 0 else "A"
        b_label = options[1].get("label", "Phương án B") if len(options) > 1 else "B"

        factor_rows = []
        for f in decision_factors:
            winner = f.get("winner", "")
            # Filled circle for winner, empty circle for loser
            mark_a = '●' if winner in ("A", "both") else '○'
            mark_b = '●' if winner in ("B", "both") else '○'
            cls_a = "win-a" if winner in ("A", "both") else "lose"
            cls_b = "win-b" if winner in ("B", "both") else "lose"
            factor_rows.append(f"""
            <div class="viz-policy-fork-factor">
              <div class="viz-policy-fork-factor-label">{escape(f.get("factor", ""))}</div>
              <div class="viz-policy-fork-factor-mark {cls_a}">{mark_a}</div>
              <div class="viz-policy-fork-factor-mark {cls_b}">{mark_b}</div>
            </div>
            """)
        factors_html = f"""
        <div class="viz-policy-fork-decision">
          <div class="viz-policy-fork-decision-label">Tiêu chí so sánh</div>
          <div class="viz-policy-fork-factor-header">
            <div class="viz-policy-fork-factor-header-name">Yếu tố</div>
            <div class="viz-policy-fork-factor-header-col fork-a">{escape(a_label)}</div>
            <div class="viz-policy-fork-factor-header-col fork-b">{escape(b_label)}</div>
          </div>
          {''.join(factor_rows)}
        </div>
        """

    context_html = f'<div class="viz-policy-fork-context">{escape(decision_context)}</div>' if decision_context else ""

    return f"""
<div class="viz-policy-fork">
  <div class="viz-policy-fork-title">{escape(title)}</div>
  {context_html}
  <div class="viz-policy-fork-options">
    {''.join(options_html)}
  </div>
  {factors_html}
</div>
"""


# ============================================================
# COMPONENT 14: WINNERS-LOSERS SPLIT
# ============================================================
def winners_losers_split(
    title: str,
    summary_stat: dict,
    winners: dict,
    losers: dict,
) -> str:
    """
    2 cột Hưởng lợi vs Chịu thiệt với entities + magnitudes.

    Args:
        summary_stat: {"value": "12-24K tỷ", "label": "Chuyển từ Nhóm C..."}
        winners / losers: {
            "label": str,           # "HƯỞNG LỢI"
            "summary": str,         # italic 1-line summary
            "items": [
                {"name": str, "value": str, "detail": str (optional)}
            ]
        }
    """
    def render_items(items):
        out = []
        for it in items:
            detail_html = ""
            if it.get("detail"):
                detail_html = f'<div class="viz-wl-item-detail">{escape(it["detail"])}</div>'
            out.append(f"""
            <div class="viz-wl-item">
              <div class="viz-wl-item-row">
                <span class="viz-wl-item-name">{escape(it.get("name", ""))}</span>
                <span class="viz-wl-item-value">{escape(it.get("value", ""))}</span>
              </div>
              {detail_html}
            </div>
            """)
        return "".join(out)

    return f"""
<div class="viz-wl">
  <div class="viz-wl-title">{escape(title)}</div>
  <div class="viz-wl-summary">
    <div class="viz-wl-summary-value">{escape(summary_stat.get("value", ""))}</div>
    <div class="viz-wl-summary-label">{escape(summary_stat.get("label", ""))}</div>
  </div>
  <div class="viz-wl-grid">
    <div class="viz-wl-column winners">
      <div class="viz-wl-col-label">{escape(winners.get("label", "HƯỞNG LỢI"))}</div>
      <div class="viz-wl-col-summary">{escape(winners.get("summary", ""))}</div>
      {render_items(winners.get("items", []))}
    </div>
    <div class="viz-wl-column losers">
      <div class="viz-wl-col-label">{escape(losers.get("label", "CHỊU THIỆT"))}</div>
      <div class="viz-wl-col-summary">{escape(losers.get("summary", ""))}</div>
      {render_items(losers.get("items", []))}
    </div>
  </div>
</div>
"""


# ============================================================
# COMPONENT 15: DATA HERO
# ============================================================
def data_hero(
    eyebrow: str,
    mega_value: str,
    mega_unit: str,
    mega_label: str,
    sub_stats: list[dict] = None,
    story: str = "",
) -> str:
    """
    1 trang dramatic với 1 mega number signature + sub-stats grid + story footer.

    Args:
        sub_stats: optional list of {"value": str, "label": str} - 2-4 items
    """
    sub_html = ""
    if sub_stats:
        cells = []
        for s in sub_stats:
            cells.append(f"""
            <div class="viz-hero-sub-stat">
              <div class="viz-hero-sub-value">{escape(s.get("value", ""))}</div>
              <div class="viz-hero-sub-label">{escape(s.get("label", ""))}</div>
            </div>
            """)
        # Adjust grid columns based on count
        n = len(sub_stats)
        grid_cols = f"repeat({n}, 1fr)"
        sub_html = f'<div class="viz-hero-sub-grid" style="grid-template-columns: {grid_cols};">{"".join(cells)}</div>'

    story_html = f'<div class="viz-hero-story">{escape(story)}</div>' if story else ""

    return f"""
<div class="viz-hero">
  <div class="viz-hero-eyebrow">{escape(eyebrow)}</div>
  <div class="viz-hero-mega">{escape(mega_value)}</div>
  <div class="viz-hero-unit">{escape(mega_unit)}</div>
  <div class="viz-hero-label">{escape(mega_label)}</div>
  {sub_html}
  {story_html}
</div>
"""


# ============================================================
# COMPONENT 16: MECHANISM BREAKDOWN
# ============================================================
def mechanism_breakdown(
    title: str,
    stages: list[dict],
    outcome: str = "",
) -> str:
    """
    3-stage flow: Input → Process → Output.

    Args:
        stages: 3 dicts (must be 3 cho layout fit):
            {
                "stage": "INPUT" | "PROCESS" | "OUTPUT",
                "name": str,            # title
                "value": str,           # optional big number
                "detail": str,          # explanation
            }
    """
    if len(stages) != 3:
        raise ValueError("mechanism_breakdown requires exactly 3 stages")

    stage_classes = ["input", "process", "output"]
    stage_html = []
    for i, st in enumerate(stages):
        cls = stage_classes[i]
        value_html = ""
        if st.get("value"):
            value_html = f'<div class="viz-mech-stage-value">{escape(st["value"])}</div>'
        stage_html.append(f"""
        <div class="viz-mech-stage {cls}">
          <div class="viz-mech-stage-label">{escape(st.get("stage", ""))}</div>
          <div class="viz-mech-stage-name">{escape(st.get("name", ""))}</div>
          {value_html}
          <div class="viz-mech-stage-detail">{escape(st.get("detail", ""))}</div>
        </div>
        """)

    outcome_html = ""
    if outcome:
        outcome_html = f"""
        <div class="viz-mech-outcome">
          <div class="viz-mech-outcome-label">Kết quả</div>
          <div class="viz-mech-outcome-text">{escape(outcome)}</div>
        </div>
        """

    return f"""
<div class="viz-mech">
  <div class="viz-mech-title">{escape(title)}</div>
  <div class="viz-mech-stages">
    {stage_html[0]}
    <div class="viz-mech-arrow">→</div>
    {stage_html[1]}
    <div class="viz-mech-arrow">→</div>
    {stage_html[2]}
  </div>
  {outcome_html}
</div>
"""


# ============================================================
# COMPONENT 17: BEFORE-AFTER COMPARISON
# ============================================================
def before_after_comparison(
    title: str,
    before: dict,
    after: dict,
    delta: str = "",
    key_changes: list[dict] = None,
) -> str:
    """
    State A → State B với delta arrow giữa.

    Args:
        before / after: {
            "label": str,           # uppercase label "Q1/2026"
            "name": str,            # italic subtitle
            "value": str,           # large mono number
            "metrics": [{"label": str, "value": str}]
        }
        delta: e.g. "-5,7 đp"
        key_changes: optional [{"text": str, "impact": str}]
    """
    def render_metrics(metrics):
        rows = []
        for m in metrics:
            rows.append(f"""
            <div class="viz-ba-metric">
              <span class="viz-ba-metric-label">{escape(m.get("label", ""))}</span>
              <span class="viz-ba-metric-value">{escape(m.get("value", ""))}</span>
            </div>
            """)
        return "".join(rows)

    delta_html = ""
    if delta:
        delta_html = f'<div class="viz-ba-arrow-delta">{escape(delta)}</div>'

    changes_html = ""
    if key_changes:
        change_rows = []
        for c in key_changes:
            change_rows.append(f"""
            <div class="viz-ba-change">
              <span class="viz-ba-change-text">{escape(c.get("text", ""))}</span>
              <span class="viz-ba-change-impact">{escape(c.get("impact", ""))}</span>
            </div>
            """)
        changes_html = f"""
        <div class="viz-ba-changes">
          <div class="viz-ba-changes-label">Các thay đổi chính</div>
          {''.join(change_rows)}
        </div>
        """

    return f"""
<div class="viz-ba">
  <div class="viz-ba-title">{escape(title)}</div>
  <div class="viz-ba-grid">
    <div class="viz-ba-state before">
      <div class="viz-ba-state-label">{escape(before.get("label", "TRƯỚC"))}</div>
      <div class="viz-ba-state-name">{escape(before.get("name", ""))}</div>
      <div class="viz-ba-state-value">{escape(before.get("value", ""))}</div>
      {render_metrics(before.get("metrics", []))}
    </div>
    <div class="viz-ba-arrow">
      <div class="viz-ba-arrow-symbol">→</div>
      {delta_html}
    </div>
    <div class="viz-ba-state after">
      <div class="viz-ba-state-label">{escape(after.get("label", "SAU"))}</div>
      <div class="viz-ba-state-name">{escape(after.get("name", ""))}</div>
      <div class="viz-ba-state-value">{escape(after.get("value", ""))}</div>
      {render_metrics(after.get("metrics", []))}
    </div>
  </div>
  {changes_html}
</div>
"""


# ============================================================
# COMPONENT 18: EXECUTIVE SUMMARY BOX
# ============================================================
def executive_summary_box(
    takeaway: dict,
    findings: list[str] = None,
    risks: list[str] = None,
    watch: list[str] = None,
    title: str = "Tóm tắt điều hành",
) -> str:
    """
    4-section dashboard: Takeaway hero + Findings + Risks + Watch.

    Args:
        takeaway: {"headline": str, "body": str}
        findings, risks, watch: list of strings (3-5 items each ideal)
    """
    def render_bullets(items, mark="▸"):
        if not items:
            return ""
        rows = []
        for it in items:
            rows.append(f"""
            <div class="viz-exec-bullet">
              <div class="viz-exec-bullet-mark">{mark}</div>
              <div class="viz-exec-bullet-text">{escape(it)}</div>
            </div>
            """)
        return "".join(rows)

    findings_html = render_bullets(findings or [])
    risks_html = render_bullets(risks or [])
    watch_html = render_bullets(watch or [])

    return f"""
<div class="viz-exec">
  <div class="viz-exec-title">{escape(title)}</div>
  <div class="viz-exec-takeaway">
    <div class="viz-exec-takeaway-label">Điểm then chốt</div>
    <div class="viz-exec-takeaway-headline">{escape(takeaway.get("headline", ""))}</div>
    <div class="viz-exec-takeaway-body">{escape(takeaway.get("body", ""))}</div>
  </div>
  <div class="viz-exec-grid">
    <div class="viz-exec-cell findings">
      <div class="viz-exec-cell-label">Phát hiện chính</div>
      {findings_html}
    </div>
    <div class="viz-exec-cell risks">
      <div class="viz-exec-cell-label">Rủi ro cần chú ý</div>
      {risks_html}
    </div>
    <div class="viz-exec-cell watch">
      <div class="viz-exec-cell-label">Chỉ báo theo dõi</div>
      {watch_html}
    </div>
  </div>
</div>
"""


# ============================================================
# COMPONENT 19: SCENARIO MATRIX (2D probability x impact)
# ============================================================
def scenario_matrix(
    title: str,
    x_axis: dict,
    y_axis: dict,
    scenarios: list[dict],
    subtitle: str = "",
) -> str:
    """
    2D matrix với 4 quadrants. Scenarios placed by (x, y) coords [0..1].

    Args:
        x_axis / y_axis: {"label": str, "low": str, "high": str}
        scenarios: list of {
            "name": str,
            "x": float (0..1),
            "y": float (0..1),
            "type": "base" | "tail" | "downside" | "extreme",
            "probability": str (optional, e.g. "50%")
        }
    """
    svg_w = 600
    svg_h = 400
    margin = {"top": 30, "right": 40, "bottom": 60, "left": 70}
    chart_w = svg_w - margin["left"] - margin["right"]
    chart_h = svg_h - margin["top"] - margin["bottom"]

    elems = []

    # 4 quadrant background tints
    quadrants = [
        # (x, y, w, h, fill, opacity)
        (margin["left"], margin["top"], chart_w/2, chart_h/2, "#FAF7F0", 0.5),  # top-left
        (margin["left"] + chart_w/2, margin["top"], chart_w/2, chart_h/2, "#F0EAE0", 0.7),  # top-right (high impact + high prob = critical)
        (margin["left"], margin["top"] + chart_h/2, chart_w/2, chart_h/2, "#FAF7F0", 0.3),  # bottom-left
        (margin["left"] + chart_w/2, margin["top"] + chart_h/2, chart_w/2, chart_h/2, "#FAF7F0", 0.4),  # bottom-right
    ]
    for x, y, w, h, fill, op in quadrants:
        elems.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{op}"/>')

    # Center cross
    elems.append(f'<line x1="{margin["left"] + chart_w/2}" y1="{margin["top"]}" x2="{margin["left"] + chart_w/2}" y2="{margin["top"] + chart_h}" stroke="#4A6FA5" stroke-width="0.6" stroke-dasharray="2,2" stroke-opacity="0.4"/>')
    elems.append(f'<line x1="{margin["left"]}" y1="{margin["top"] + chart_h/2}" x2="{margin["left"] + chart_w}" y2="{margin["top"] + chart_h/2}" stroke="#4A6FA5" stroke-width="0.6" stroke-dasharray="2,2" stroke-opacity="0.4"/>')

    # Outer frame
    elems.append(f'<rect x="{margin["left"]}" y="{margin["top"]}" width="{chart_w}" height="{chart_h}" fill="none" stroke="#4A6FA5" stroke-width="0.8"/>')

    # X-axis labels
    elems.append(f'<text x="{margin["left"]}" y="{svg_h - margin["bottom"] + 18}" text-anchor="start" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="600" fill="#6B6760">{escape(x_axis.get("low", "Thấp"))}</text>')
    elems.append(f'<text x="{margin["left"] + chart_w}" y="{svg_h - margin["bottom"] + 18}" text-anchor="end" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="600" fill="#6B6760">{escape(x_axis.get("high", "Cao"))}</text>')
    elems.append(f'<text x="{margin["left"] + chart_w/2}" y="{svg_h - margin["bottom"] + 35}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="9" font-weight="700" fill="#003153" letter-spacing="0.05em">{escape(x_axis.get("label", "Probability").upper())}</text>')

    # Y-axis labels (rotated)
    y_low_x = margin["left"] - 12
    y_high_x = margin["left"] - 12
    elems.append(f'<text x="{y_low_x}" y="{margin["top"] + chart_h - 4}" text-anchor="end" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="600" fill="#6B6760">{escape(y_axis.get("low", "Thấp"))}</text>')
    elems.append(f'<text x="{y_low_x}" y="{margin["top"] + 10}" text-anchor="end" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="600" fill="#6B6760">{escape(y_axis.get("high", "Cao"))}</text>')
    # Y label rotated
    label_y = margin["top"] + chart_h/2
    elems.append(f'<text x="{margin["left"] - 35}" y="{label_y}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="9" font-weight="700" fill="#003153" letter-spacing="0.05em" transform="rotate(-90, {margin["left"] - 35}, {label_y})">{escape(y_axis.get("label", "Impact").upper())}</text>')

    # Quadrant labels (subtle)
    quadrant_labels = [
        (margin["left"] + 8, margin["top"] + 16, "TÁC ĐỘNG CAO · ÍT XÁC SUẤT"),  # top-left
        (margin["left"] + chart_w - 8, margin["top"] + 16, "CRITICAL"),  # top-right
        (margin["left"] + 8, margin["top"] + chart_h - 8, "TRUNG TÍNH"),  # bottom-left
        (margin["left"] + chart_w - 8, margin["top"] + chart_h - 8, "CƠ SỞ"),  # bottom-right
    ]
    qlabels_anchors = ["start", "end", "start", "end"]
    qlabel_colors = ["#6B6760", "#C0392B", "#6B6760", "#4A6FA5"]
    for (qx, qy, qtxt), anchor, color in zip(quadrant_labels, qlabels_anchors, qlabel_colors):
        elems.append(f'<text x="{qx}" y="{qy}" text-anchor="{anchor}" font-family="Inter,InterVN,sans-serif" font-size="6.5" font-weight="700" fill="{color}" letter-spacing="0.1em" opacity="0.6">{escape(qtxt)}</text>')

    # Scenarios
    type_colors = {
        "base": "#4A6FA5",
        "tail": "#B5A642",
        "downside": "#6B6760",
        "extreme": "#C0392B",
    }
    for sc in scenarios:
        x_pos = margin["left"] + sc["x"] * chart_w
        y_pos = margin["top"] + chart_h - (sc["y"] * chart_h)  # invert y
        color = type_colors.get(sc.get("type", "base"), "#4A6FA5")
        # Dot
        elems.append(f'<circle cx="{x_pos:.1f}" cy="{y_pos:.1f}" r="6" fill="{color}" stroke="#FAF7F0" stroke-width="1.5"/>')
        # Label
        prob_text = ""
        if sc.get("probability"):
            prob_text = f' ({escape(sc["probability"])})'
        elems.append(f'<text x="{x_pos:.1f}" y="{y_pos - 11:.1f}" text-anchor="middle" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="700" fill="#003153">{escape(sc["name"])}{prob_text}</text>')

    return f"""
<div class="viz-matrix">
  <div class="viz-matrix-title">{escape(title)}</div>
  <svg class="viz-matrix-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    {''.join(elems)}
  </svg>
</div>
"""


# ============================================================
# COMPONENT 20: RISK RADAR
# ============================================================
def risk_radar(
    title: str,
    dimensions: list[dict],
    show_target: bool = True,
    current_label: str = "Hiện tại",
    target_label: str = "Mục tiêu",
) -> str:
    """
    Radar chart 5-7 axes với current polygon và optional target polygon.

    Args:
        dimensions: list of {
            "label": str,
            "current": float (0..1),
            "target": float (0..1, optional)
        }
        show_target: vẽ thêm target polygon
    """
    n = len(dimensions)
    if n < 3:
        raise ValueError("risk_radar needs at least 3 dimensions")

    svg_w = 480
    svg_h = 380
    cx = svg_w / 2
    cy = svg_h / 2 + 5
    r_max = 110

    elems = []

    # Concentric polygons (background grid)
    for level in [0.25, 0.5, 0.75, 1.0]:
        points = []
        for i in range(n):
            angle = -math.pi/2 + (2 * math.pi * i / n)
            r = r_max * level
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append(f"{px:.1f},{py:.1f}")
        opacity = 0.08 if level < 1 else 0.25
        elems.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#4A6FA5" stroke-width="0.5" stroke-opacity="{opacity}"/>')

    # Axis lines
    for i in range(n):
        angle = -math.pi/2 + (2 * math.pi * i / n)
        ex = cx + r_max * math.cos(angle)
        ey = cy + r_max * math.sin(angle)
        elems.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#4A6FA5" stroke-width="0.4" stroke-opacity="0.2"/>')

    # Target polygon (background, brass dashed)
    if show_target and any(d.get("target") is not None for d in dimensions):
        target_points = []
        for i, d in enumerate(dimensions):
            angle = -math.pi/2 + (2 * math.pi * i / n)
            r = r_max * (d.get("target") or 0)
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            target_points.append(f"{px:.1f},{py:.1f}")
        elems.append(f'<polygon points="{" ".join(target_points)}" fill="#B5A642" fill-opacity="0.08" stroke="#B5A642" stroke-width="1" stroke-dasharray="3,2"/>')

    # Current polygon (prussian filled)
    current_points = []
    for i, d in enumerate(dimensions):
        angle = -math.pi/2 + (2 * math.pi * i / n)
        r = r_max * d.get("current", 0)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        current_points.append(f"{px:.1f},{py:.1f}")
    elems.append(f'<polygon points="{" ".join(current_points)}" fill="#4A6FA5" fill-opacity="0.25" stroke="#003153" stroke-width="1.5"/>')

    # Dots on current vertices
    for i, d in enumerate(dimensions):
        angle = -math.pi/2 + (2 * math.pi * i / n)
        r = r_max * d.get("current", 0)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        elems.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.5" fill="#003153"/>')

    # Axis labels (outside the polygon)
    for i, d in enumerate(dimensions):
        angle = -math.pi/2 + (2 * math.pi * i / n)
        label_r = r_max + 18
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)
        # Anchor based on x position
        if abs(math.cos(angle)) < 0.3:
            anchor = "middle"
        elif math.cos(angle) > 0:
            anchor = "start"
        else:
            anchor = "end"
        elems.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-family="Inter,InterVN,sans-serif" font-size="8" font-weight="700" fill="#003153" dominant-baseline="middle">{escape(d.get("label", ""))}</text>')

    # Legend
    legend_html = f"""
    <div class="viz-radar-legend">
      <div class="viz-radar-legend-item">
        <div class="viz-radar-legend-swatch" style="background: #003153;"></div>
        <span>{escape(current_label)}</span>
      </div>
    """
    if show_target and any(d.get("target") is not None for d in dimensions):
        legend_html += f"""
      <div class="viz-radar-legend-item">
        <div class="viz-radar-legend-swatch" style="background: #B5A642;"></div>
        <span>{escape(target_label)}</span>
      </div>
        """
    legend_html += "</div>"

    return f"""
<div class="viz-radar">
  <div class="viz-radar-title">{escape(title)}</div>
  <svg class="viz-radar-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    {''.join(elems)}
  </svg>
  {legend_html}
</div>
"""
