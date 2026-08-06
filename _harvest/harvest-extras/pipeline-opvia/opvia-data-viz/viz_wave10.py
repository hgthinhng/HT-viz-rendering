"""
Opvia Wave 10 - Composite Poster Layouts
==========================================

Layouts cao cấp combines multiple atoms vào 1 visual unit. Đây không phải
"thêm 1 chart" mà là "1 trang information design."

Components:
1. dashboard_grid       - 2x2 grid 4 cells, mỗi cell 1 KPI + sparkline
2. narrative_strip      - 3 mini chart hàng ngang + caption single line dưới
3. infographic_panel    - 1 hero stat trái + 4-5 supporting facts phải

Triết lý: A4 trang trống là phần phí phạm. Composite layouts giải quyết
"data đủ, nhưng cách bố trí kém" - vấn đề lớn nhất khi LLM tự generate viz.
"""
from __future__ import annotations
from html import escape

from _tokens import COLORS, FONTS
from _svg_helpers import path_smooth, fmt_number, fmt_compact


# ============================================================
# COMPONENT 1: DASHBOARD GRID
# ============================================================

def dashboard_grid(
    cells: list[dict],
    title: str = "",
    subtitle: str = "",
    cols: int = 2,
) -> str:
    """
    2x2 (hoặc 3x1, 2x3) grid cells, mỗi cell:
    - KPI giá trị lớn (mono)
    - Label uppercase nhỏ
    - Sparkline mini
    - Delta % với arrow
    - Context line italic 1 dòng

    cells: [{
        "kpi": "1.347,82",
        "label": "VN-INDEX",
        "delta": "+0,68%",
        "delta_type": "up"|"down"|"flat",
        "spark_data": [1305, 1310, ..., 1347],
        "context": "Phiên xanh thứ 4 liên tiếp.",
        "highlight": True,             # optional - nền brass nhẹ
    }]
    cols: 2 (default 2x2 cho 4 cells), 3 (3x1 cho 3 cells)

    Use case: Overview dashboard đầu báo cáo daily, KPI grid cho ngân hàng,
    sector overview. Khác với stat_card_pro hiện có ở chỗ là LAYOUT
    composite không phải atom.
    """
    if not cells:
        return ""

    cards_html = []
    for c in cells:
        kpi = escape(c.get("kpi", ""))
        label = escape(c.get("label", "").upper())
        delta = c.get("delta", "")
        delta_type = c.get("delta_type", "flat")
        context = escape(c.get("context", ""))
        is_hl = c.get("highlight", False)
        spark = c.get("spark_data", [])

        # Delta colors and arrow
        if delta_type == "up":
            delta_color = COLORS.POSITIVE
            arrow = "▲"
        elif delta_type == "down":
            delta_color = COLORS.NEGATIVE
            arrow = "▼"
        else:
            delta_color = COLORS.SLATE
            arrow = "─"

        # Sparkline SVG
        spark_html = ""
        if spark and len(spark) > 1:
            sw, sh = 100, 24
            mn, mx = min(spark), max(spark)
            rng = mx - mn or 1
            pts = []
            for i, v in enumerate(spark):
                x = i * sw / (len(spark) - 1)
                y = sh - (v - mn) / rng * (sh - 4) - 2
                pts.append((x, y))
            d = path_smooth(pts)
            # area
            base_y = sh - 1
            area_d = f"{d} L {pts[-1][0]:.2f} {base_y} L {pts[0][0]:.2f} {base_y} Z"
            line_color = delta_color
            spark_html = (
                f'<svg viewBox="0 0 {sw} {sh}" xmlns="http://www.w3.org/2000/svg" '
                f'class="vw-dash-spark" preserveAspectRatio="none">'
                f'<path d="{area_d}" fill="{line_color}" fill-opacity="0.12" stroke="none"/>'
                f'<path d="{d}" fill="none" stroke="{line_color}" stroke-width="1.4" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2" '
                f'fill="{line_color}" stroke="{COLORS.IVORY}" stroke-width="1"/>'
                f'</svg>'
            )

        hl_class = " vw-dash-cell-hl" if is_hl else ""

        cards_html.append(f'''
<div class="vw-dash-cell{hl_class}">
  <div class="vw-dash-label">{label}</div>
  <div class="vw-dash-row">
    <div class="vw-dash-kpi">{kpi}</div>
    <div class="vw-dash-delta" style="color: {delta_color};">{arrow} {escape(delta)}</div>
  </div>
  {spark_html}
  <div class="vw-dash-context">{context}</div>
</div>
''')

    title_html = f'<div class="vw-dash-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-dash-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-dashboard">
  {title_html}
  {sub_html}
  <div class="vw-dash-grid" style="grid-template-columns: repeat({cols}, 1fr);">
    {"".join(cards_html)}
  </div>
</div>
'''


# ============================================================
# COMPONENT 2: NARRATIVE STRIP
# ============================================================

def narrative_strip(
    panels: list[dict],
    main_caption: str,
    title: str = "",
    cols: int = 3,
) -> str:
    """
    3 (hoặc 4) mini chart hàng ngang, mỗi panel có 1 mini line chart và
    1 stat ngắn. Dưới cùng là 1 caption editorial single line tổng kết
    cho toàn strip.

    panels: [{
        "label": "DXY",
        "value": "109,3",
        "context": "Q4/2025",
        "data": [...],            # mini timeseries 6-12 points
        "color": "#003153",       # optional override
    }]
    main_caption: Câu summary tổng cho 3 panels (Economist-style editorial)

    Use case:
        - Overview macro (DXY, USD/VND, Brent) ở đầu bài
        - Performance multi-bank quick scan
        - Khác với small_multiples_grid ở chỗ chỉ 3 panels và có editorial
          caption ăn ý nhau

    Đây là idiom mạnh của Economist: "DXY mạnh, Brent cao, VND căng" -
    3 chart nhỏ và 1 câu kể câu chuyện. Mắt đọc 5 giây tiếp thu hết.
    """
    if not panels:
        return ""

    panel_w = 220
    panel_h = 90
    PAD = 12

    panel_html_list = []
    for p in panels:
        label = escape(p.get("label", "").upper())
        value = escape(p.get("value", ""))
        ctx = escape(p.get("context", ""))
        data = p.get("data", [])
        color = p.get("color", COLORS.PRUSSIAN)

        # Mini chart
        chart_html = ""
        if data and len(data) > 1:
            mn, mx = min(data), max(data)
            rng = mx - mn or 1
            sw = panel_w - 2 * PAD
            sh = 36
            pts = []
            for i, v in enumerate(data):
                x = PAD + i * sw / (len(data) - 1)
                y = sh + 26 - (v - mn) / rng * (sh - 6) - 2
                pts.append((x, y))
            d = path_smooth(pts)
            base_y = sh + 26 - 1
            area_d = f"{d} L {pts[-1][0]:.2f} {base_y} L {pts[0][0]:.2f} {base_y} Z"
            chart_html = (
                f'<path d="{area_d}" fill="{color}" fill-opacity="0.10" stroke="none"/>'
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2.4" '
                f'fill="{COLORS.IVORY}" stroke="{color}" stroke-width="1.4"/>'
            )

        panel_html_list.append(f'''
<svg viewBox="0 0 {panel_w} {panel_h}" xmlns="http://www.w3.org/2000/svg" class="vw-strip-panel-svg">
  <text x="{PAD}" y="14" font-family="{FONTS.SANS}" font-size="7.5"
        font-weight="700" fill="{COLORS.PRUSSIAN}" letter-spacing="0.12em">{label}</text>
  <text x="{panel_w - PAD}" y="14" text-anchor="end"
        font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">{ctx}</text>
  <text x="{PAD}" y="36" font-family="{FONTS.MONO}" font-size="16"
        font-weight="700" fill="{COLORS.PRUSSIAN}">{value}</text>
  {chart_html}
</svg>
''')

    title_html = f'<div class="vw-strip-title">{escape(title)}</div>' if title else ""

    return f'''
<div class="vw-narrative-strip">
  {title_html}
  <div class="vw-strip-grid" style="grid-template-columns: repeat({cols}, 1fr);">
    {"".join(panel_html_list)}
  </div>
  <div class="vw-strip-caption">
    <div class="vw-strip-rule"></div>
    <div class="vw-strip-text">{escape(main_caption)}</div>
  </div>
</div>
'''


# ============================================================
# COMPONENT 3: INFOGRAPHIC PANEL
# ============================================================

def infographic_panel(
    hero_value: str,
    hero_unit: str,
    hero_label: str,
    hero_caption: str,
    facts: list[dict],
    title: str = "",
    subtitle: str = "",
    accent_color: str = COLORS.BRASS,
) -> str:
    """
    Full panel: hero stat trái lớn + 4-5 supporting facts phải.

    hero_value: con số lớn (e.g. "406")
    hero_unit: unit ngắn (e.g. "nghìn tỷ VND")
    hero_label: caption uppercase ngắn (e.g. "TIỀN GỬI KHO BẠC BIG4")
    hero_caption: 1-2 dòng prose giải thích
    facts: [{
        "value": "+18%",          # mono small accent
        "label": "vs Q4/2025",    # body label
        "detail": "...",          # optional caption italic
    }]

    Use case:
        - Hero panel mở Phần với 1 mega number
        - Tóm tắt key fact + 4 supporting numbers
        - Dùng làm ending block tóm tắt cho một section

    Khác với data_hero hiện có:
    - Layout 2 cột rõ rệt hơn (hero | facts list)
    - Facts có structure (value + label + detail)
    - Dùng cho story-telling chứ không phải dashboard
    """
    facts_html = []
    for f in facts:
        v = escape(f.get("value", ""))
        lbl = escape(f.get("label", ""))
        det = escape(f.get("detail", ""))
        det_html = f'<div class="vw-info-fact-detail">{det}</div>' if det else ""
        facts_html.append(f'''
<div class="vw-info-fact">
  <div class="vw-info-fact-value" style="color: {accent_color};">{v}</div>
  <div class="vw-info-fact-body">
    <div class="vw-info-fact-label">{lbl}</div>
    {det_html}
  </div>
</div>
''')

    title_html = f'<div class="vw-info-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-info-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-infographic">
  {title_html}
  {sub_html}
  <div class="vw-info-row">
    <div class="vw-info-hero">
      <div class="vw-info-hero-label">{escape(hero_label)}</div>
      <div class="vw-info-hero-num" style="color: {accent_color};">{escape(hero_value)}</div>
      <div class="vw-info-hero-unit">{escape(hero_unit)}</div>
      <div class="vw-info-hero-rule" style="background: {accent_color};"></div>
      <div class="vw-info-hero-caption">{escape(hero_caption)}</div>
    </div>
    <div class="vw-info-facts">
      {"".join(facts_html)}
    </div>
  </div>
</div>
'''


# ============================================================
# WAVE 10 STYLES
# ============================================================

def wave10_styles() -> str:
    """CSS cho Wave 10 composite layouts."""
    return """
/* ============ WAVE 10 - COMPOSITE LAYOUTS ============ */

/* ============ DASHBOARD GRID ============ */
.vw-dashboard {
  background: var(--paper, #FAF7F0);
  border: 0.6px solid var(--rule-soft, rgba(181,166,66,0.30));
  border-radius: 4px;
  padding: 14px 16px 12px 16px;
  margin: 14px 0;
  page-break-inside: avoid;
}
.vw-dash-title {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 11pt;
  font-weight: 600;
  color: var(--prussian, #003153);
  margin-bottom: 2px;
}
.vw-dash-sub {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 8pt;
  color: var(--text-secondary, #6B6760);
  margin-bottom: 12px;
  line-height: 1.4;
  font-style: italic;
}
.vw-dash-grid {
  display: grid;
  gap: 10px;
}
.vw-dash-cell {
  background: white;
  border: 0.6px solid var(--rule-soft, rgba(181,166,66,0.30));
  border-radius: 4px;
  padding: 10px 12px 8px 12px;
  position: relative;
}
.vw-dash-cell-hl {
  background: rgba(181,166,66,0.06);
  border-color: rgba(181,166,66,0.55);
}
.vw-dash-label {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 6.5pt;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--text-secondary, #6B6760);
  margin-bottom: 4px;
}
.vw-dash-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 4px;
}
.vw-dash-kpi {
  font-family: 'JBM','JBMVN','IBM Plex Mono',monospace;
  font-size: 18pt;
  font-weight: 700;
  color: var(--prussian, #003153);
  line-height: 1;
  letter-spacing: -0.02em;
}
.vw-dash-delta {
  font-family: 'JBM','JBMVN','IBM Plex Mono',monospace;
  font-size: 9pt;
  font-weight: 600;
}
.vw-dash-spark {
  width: 100%;
  height: 22px;
  display: block;
  margin: 4px 0 4px 0;
}
.vw-dash-context {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 7.5pt;
  color: var(--text-secondary, #6B6760);
  line-height: 1.45;
  font-style: italic;
  margin-top: 2px;
}

/* ============ NARRATIVE STRIP ============ */
.vw-narrative-strip {
  background: var(--paper, #FAF7F0);
  border: 0.6px solid var(--rule-soft, rgba(181,166,66,0.30));
  border-radius: 4px;
  padding: 14px 16px 14px 16px;
  margin: 14px 0;
  page-break-inside: avoid;
}
.vw-strip-title {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 11pt;
  font-weight: 600;
  color: var(--prussian, #003153);
  margin-bottom: 8px;
}
.vw-strip-grid {
  display: grid;
  gap: 8px;
  margin-bottom: 12px;
}
.vw-strip-panel-svg {
  display: block;
  width: 100%;
  height: auto;
  background: white;
  border: 0.6px solid var(--rule-soft, rgba(181,166,66,0.20));
  border-radius: 3px;
}
.vw-strip-caption {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.vw-strip-rule {
  flex-shrink: 0;
  width: 2px;
  background: var(--brass, #B5A642);
  align-self: stretch;
  min-height: 22px;
}
.vw-strip-text {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 9.5pt;
  font-style: italic;
  font-weight: 450;
  line-height: 1.55;
  color: var(--charcoal, #2B2B2B);
}

/* ============ INFOGRAPHIC PANEL ============ */
.vw-infographic {
  background: var(--prussian, #003153);
  border-radius: 6px;
  padding: 22px 24px 22px 24px;
  margin: 16px 0;
  page-break-inside: avoid;
  color: var(--ivory, #F5F1E8);
}
.vw-info-title {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 11pt;
  font-weight: 600;
  color: var(--brass-300, #CCC46B);
  margin-bottom: 2px;
}
.vw-info-sub {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 8pt;
  color: rgba(245,241,232,0.65);
  margin-bottom: 14px;
  line-height: 1.4;
  font-style: italic;
}
.vw-info-row {
  display: flex;
  gap: 28px;
  align-items: flex-start;
}
.vw-info-hero {
  flex: 0 0 38%;
  position: relative;
}
.vw-info-hero-label {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 6.5pt;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: rgba(245,241,232,0.6);
  margin-bottom: 6px;
}
.vw-info-hero-num {
  font-family: 'JBM','JBMVN','IBM Plex Mono',monospace;
  font-size: 56pt;
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
  margin-bottom: 4px;
}
.vw-info-hero-unit {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 9pt;
  font-weight: 500;
  color: rgba(245,241,232,0.85);
  margin-bottom: 10px;
}
.vw-info-hero-rule {
  width: 36px;
  height: 2px;
  margin-bottom: 10px;
}
.vw-info-hero-caption {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 9.5pt;
  font-style: italic;
  font-weight: 450;
  line-height: 1.55;
  color: rgba(245,241,232,0.85);
}
.vw-info-facts {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-left: 0.8px solid rgba(181,166,66,0.40);
  padding-left: 22px;
}
.vw-info-fact {
  display: flex;
  gap: 14px;
  align-items: baseline;
  padding-bottom: 10px;
  border-bottom: 0.5px solid rgba(245,241,232,0.12);
}
.vw-info-fact:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.vw-info-fact-value {
  flex: 0 0 70px;
  font-family: 'JBM','JBMVN','IBM Plex Mono',monospace;
  font-size: 13pt;
  font-weight: 700;
  letter-spacing: -0.01em;
}
.vw-info-fact-body {
  flex: 1;
  min-width: 0;
}
.vw-info-fact-label {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 9pt;
  font-weight: 600;
  color: var(--ivory, #F5F1E8);
  line-height: 1.35;
  margin-bottom: 1px;
}
.vw-info-fact-detail {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 7.8pt;
  font-style: italic;
  color: rgba(245,241,232,0.65);
  line-height: 1.45;
}
"""
