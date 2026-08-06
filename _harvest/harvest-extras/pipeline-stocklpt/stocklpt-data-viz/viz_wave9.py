"""
StockLPT Wave 9 - Editorial Signatures
=====================================

Editorial flourishes làm output StockLPT khác biệt với output AI generic.
Đây không phải data viz - đây là typographic furniture.

Components:
1. marginalia        - Chú thích lề accent italic, có thể có pull-out arrow
2. chart_dropcap     - Drop cap chữ đầu đoạn cạnh chart, body wraps around
3. path_progression  - Đường accent mảnh chạy ngang qua section với milestones

Triết lý: chart kể fact, editorial signature kể "ai đang nói." Không
có editorial = nội dung trông như Wikipedia. Có editorial = trông như
The Atlantic.
"""
from __future__ import annotations
from html import escape

from _tokens import COLORS, FONTS
from _svg_helpers import path_smooth


# ============================================================
# COMPONENT 1: MARGINALIA
# ============================================================

def marginalia(
    body_html: str,
    note_text: str,
    note_label: str = "",
    side: str = "right",
    width_pct: int = 22,
) -> str:
    """
    Wrap body trong layout 2 cột với chú thích lề accent italic.

    Layout:
      [body 75%]  [margin 22%]
      [body...]    rule accent dọc
                   eyebrow uppercase
                   italic note...

    Args:
        body_html: HTML đoạn văn body
        note_text: Chú thích italic, max 30-40 từ
        note_label: Eyebrow uppercase (e.g. "PHƯƠNG PHÁP", "GHI CHÚ")
        side: 'right' (default) | 'left'
        width_pct: % chiều rộng cột margin

    Use case:
        - Định nghĩa thuật ngữ ngắn cho 1 từ trong body
        - Cảnh báo phương pháp tính
        - Pointer đến section khác trong bài
        - Voice của editor xen vào prose của analyst
    """
    body_pct = 100 - width_pct - 3  # 3% gap
    label_html = f'<div class="vw-margin-label">{escape(note_label)}</div>' if note_label else ""

    side_class = "vw-margin-right" if side == "right" else "vw-margin-left"

    return f'''
<div class="vw-marginalia {side_class}">
  <div class="vw-margin-body" style="flex: 0 0 {body_pct}%;">{body_html}</div>
  <div class="vw-margin-note" style="flex: 0 0 {width_pct}%;">
    <div class="vw-margin-rule"></div>
    {label_html}
    <div class="vw-margin-text">{escape(note_text)}</div>
  </div>
</div>
'''


# ============================================================
# COMPONENT 2: CHART DROPCAP
# ============================================================

def chart_dropcap(
    body_text: str,
    chart_html: str,
    chart_position: str = "left",
    chart_width_pct: int = 38,
    dropcap_letter: str = "",
) -> str:
    """
    Đoạn văn opening Phần với chart cạnh nó. Body wrap around chart
    nhờ float CSS. Drop cap chữ đầu serif lớn.

    Args:
        body_text: Text plain hoặc HTML markup nhẹ
        chart_html: HTML output từ Wave 8 component
        chart_position: 'left' | 'right'
        chart_width_pct: 35-45 thường tốt
        dropcap_letter: Override drop cap. Nếu rỗng, dùng chữ đầu body_text.

    Use case:
        - Mở Phần với chart hero + text intro chạy quanh
        - Tránh layout boring: chart trên, text dưới
        - Magazine-style flow giữa văn và data

    Lưu ý Vietnamese diacritic:
        Chữ đầu có dấu thanh phía trên (Đ, Ô, Â, Ê, Ơ, Ư) có thể bị đè lên
        text dòng đầu. Khuyến nghị dùng chữ Latin thường (T, M, V, K, S)
        làm chữ đầu, hoặc override qua dropcap_letter parameter.
    """
    text = body_text.strip()
    if not dropcap_letter:
        dropcap_letter = text[0] if text else ""
        text = text[1:].lstrip()

    pos_class = "vw-cd-chart-left" if chart_position == "left" else "vw-cd-chart-right"

    return f'''
<div class="vw-chart-dropcap {pos_class}">
  <div class="vw-cd-chart" style="width: {chart_width_pct}%;">{chart_html}</div>
  <div class="vw-cd-body">
    <span class="vw-cd-letter">{escape(dropcap_letter)}</span>{text}
  </div>
</div>
'''


# ============================================================
# COMPONENT 3: PATH PROGRESSION
# ============================================================

def path_progression(
    milestones: list[dict],
    title: str = "",
    subtitle: str = "",
    show_arrows: bool = True,
    height: int = 90,
) -> str:
    """
    Đường accent mảnh chạy ngang qua section với 3-7 milestones.

    Khác với timeline_horizontal (boxes + dates):
    - Đây tinh tế hơn - chỉ 1 đường + dots + label
    - Dùng cho narrative progression (quy trình, hành trình, evolution)
    - Không quy chiếu thời gian cứng

    milestones: [{
        "label": "Đề xuất",
        "caption": "T4/2026",        # optional
        "highlight": True,           # optional - dot accent to hơn
        "marker": "current",         # optional - 'current'|'completed'|'future'
    }]
    """
    if not milestones:
        return ""

    n = len(milestones)
    W = 720
    PAD = 60
    plot_w = W - 2 * PAD
    cy = 38

    def x_at(i: int) -> float:
        if n == 1:
            return W / 2
        return PAD + (i / (n - 1)) * plot_w

    # Main path (curved slightly through middle)
    path_pts = []
    for i in range(n):
        x = x_at(i)
        # subtle wave - max 4px from cy
        wave_y = cy + math.sin(i / max(1, n - 1) * math.pi) * 0  # straight for now
        path_pts.append((x, wave_y))

    main_path = path_smooth(path_pts) if len(path_pts) > 1 else ""

    # Render milestones
    items_html = []
    for i, m in enumerate(milestones):
        x = x_at(i)
        is_hl = m.get("highlight", False)
        marker = m.get("marker", "default")

        # Dot styling
        if marker == "current":
            r, fill, stroke = 6, COLORS.ACCENT, COLORS.ACCENT_700
        elif marker == "completed":
            r, fill, stroke = 5, COLORS.INDIGO, COLORS.INDIGO
        elif marker == "future":
            r, fill, stroke = 5, COLORS.PAPER, COLORS.ACCENT
        else:
            r = 5.5 if is_hl else 4.0
            fill = COLORS.ACCENT if is_hl else COLORS.SLATE
            stroke = fill

        # Outer halo for highlight
        halo_html = ""
        if is_hl or marker == "current":
            halo_html = (
                f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{r + 4}" '
                f'fill="{fill}" opacity="0.20"/>'
            )

        items_html.append(
            f'{halo_html}'
            f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1.4"/>'
            f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{r}" fill="none" '
            f'stroke="{stroke}" stroke-width="0.8" opacity="0.6"/>'
        )

        # Label below dot
        label = escape(m["label"])
        label_y = cy + r + 14
        weight = "700" if is_hl else "600"
        ink = COLORS.INDIGO if is_hl else COLORS.CHARCOAL
        items_html.append(
            f'<text x="{x:.1f}" y="{label_y:.1f}" text-anchor="middle" '
            f'font-family="{FONTS.SANS}" font-size="8.5" fill="{ink}" font-weight="{weight}">{label}</text>'
        )

        # Caption (date / context)
        cap = m.get("caption", "")
        if cap:
            items_html.append(
                f'<text x="{x:.1f}" y="{label_y + 11:.1f}" text-anchor="middle" '
                f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">{escape(cap)}</text>'
            )

        # Arrow to next milestone
        if show_arrows and i < n - 1:
            x_next = x_at(i + 1)
            arrow_x = (x + x_next) / 2
            items_html.append(
                f'<text x="{arrow_x:.1f}" y="{cy + 1:.1f}" text-anchor="middle" '
                f'font-family="{FONTS.SANS}" font-size="9" fill="{COLORS.ACCENT}" opacity="0.7">▸</text>'
            )

    title_html = f'<div class="vw-path-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-path-sub">{escape(subtitle)}</div>' if subtitle else ""

    # Calculate viewBox height based on content
    H = height + max(0, max(len(m.get("caption", "")) for m in milestones) > 0 and 14 or 0)

    return f'''
<div class="vw-path-progression">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-path-svg">
    <path d="{main_path}" fill="none" stroke="{COLORS.ACCENT}"
          stroke-width="0.8" opacity="0.5" stroke-dasharray="0"/>
    {"".join(items_html)}
  </svg>
</div>
'''


# Need math import for path_progression
import math


# ============================================================
# WAVE 9 STYLES
# ============================================================

def wave9_styles() -> str:
    """CSS cho Wave 9 editorial signatures."""
    return """
/* ============ WAVE 9 - EDITORIAL SIGNATURES ============ */

/* Marginalia */
.vw-marginalia {
  display: flex;
  gap: 3%;
  align-items: flex-start;
  margin: 14px 0 18px 0;
  page-break-inside: avoid;
}
.vw-marginalia.vw-margin-left { flex-direction: row-reverse; }

.vw-margin-body { min-width: 0; }
.vw-margin-body p {
  margin: 0 0 8px 0;
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 10pt;
  line-height: 1.65;
  color: var(--charcoal, #221A34);
}

.vw-margin-note {
  position: relative;
  padding: 4px 0 4px 12px;
  min-height: 60px;
}
.vw-margin-rule {
  position: absolute;
  left: 0; top: 6px; bottom: 6px;
  width: 1.4px;
  background: var(--accent, #16633C);
}
.vw-margin-label {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 6.5pt;
  font-weight: 700;
  color: var(--accent, #16633C);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.vw-margin-text {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 8.8pt;
  font-style: italic;
  line-height: 1.5;
  color: var(--text-secondary, #645B76);
}

/* Chart Dropcap */
.vw-chart-dropcap {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin: 12px 0 18px 0;
  page-break-inside: avoid;
}
.vw-chart-dropcap.vw-cd-chart-right { flex-direction: row-reverse; }

.vw-cd-chart {
  flex-shrink: 0;
}
.vw-cd-body {
  flex: 1;
  min-width: 0;
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 10.5pt;
  line-height: 1.7;
  color: var(--charcoal, #221A34);
  font-weight: 450;
  text-align: justify;
}
.vw-cd-letter {
  float: left;
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 32pt;
  font-weight: 700;
  color: var(--indigo, #2A1A4A);
  line-height: 0.92;
  padding-right: 8px;
  padding-top: 4px;
  margin-top: 2px;
  margin-bottom: -3px;
}

/* Path Progression */
.vw-path-progression {
  margin: 14px 0;
  padding: 10px 14px;
  background: var(--paper, #F4F6F9);
  border: 0.6px solid var(--rule-soft, rgba(22,99,60,0.30));
  border-radius: 4px;
  page-break-inside: avoid;
}
.vw-path-title {
  font-family: 'PFD','PFDVN','Lora',Georgia,serif;
  font-size: 10.5pt;
  font-weight: 600;
  color: var(--indigo, #2A1A4A);
  margin-bottom: 2px;
  line-height: 1.25;
}
.vw-path-sub {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 7.8pt;
  color: var(--text-secondary, #645B76);
  margin-bottom: 8px;
  line-height: 1.4;
  font-style: italic;
}
.vw-path-svg {
  display: block;
  width: 100%;
  height: auto;
}
"""
