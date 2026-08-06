"""
StockLPT Data Viz - Wave 8
========================
6 chart components còn thiếu trong thư viện hiện có + compass_callout wrapper.

Refactor patterns:
- Tokens centralized (COLORS, METRICS)
- Helper SVG primitives (svg_line, svg_text, axis_ticks)
- Composeable structure: small helpers -> large composers
- Sane defaults: most args optional with smart auto-scaling

Components (Wave 8):
1. line_with_annotations  - SVG line/area chart với annotation callouts
2. dot_plot_distribution  - Phân phối dot thật, quartile bands, median
3. small_multiples_grid   - Lưới 6-9 mini chart (Tufte signature)
4. quadrant_scatter       - 2D risk-return với 4 quadrant labels
5. slopegraph             - Paired change before/after với connecting lines
6. sankey_mini            - Flow nhỏ 3-5 sources -> 3-5 destinations

Editorial signature (Wave 9):
7. compass_callout        - Wrapper bọc viz với accent leader line + sidebar caption

Usage:
    from viz_wave8 import (
        wave8_styles,
        line_with_annotations, dot_plot_distribution, small_multiples_grid,
        quadrant_scatter, slopegraph, sankey_mini, compass_callout,
    )
    css = build_css(...) + viz_styles() + wave8_styles()
"""
from __future__ import annotations
import math
from html import escape
from typing import Sequence


# ============================================================
# CENTRALIZED TOKENS
# ============================================================

class COLORS:
    """Single source of truth cho mọi color hex (WeasyPrint SVG không reliable với CSS class)."""
    INDIGO = "#2A1A4A"
    INDIGO_50 = "#E8E5EF"
    INDIGO_100 = "#C2BBD4"
    INDIGO_700 = "#1D1238"

    ACCENT = "#16633C"
    ACCENT_300 = "#3C8C5E"
    ACCENT_100 = "#C5E3D0"
    ACCENT_50 = "#E8F3EC"

    SLATE = "#514B78"
    SLATE_LIGHT = "#847FA3"

    IVORY = "#EBEFF4"
    IVORY_DEEP = "#DDE4EC"
    PAPER = "#F4F6F9"

    CHARCOAL = "#221A34"
    INK = "#151022"
    TEXT_SECONDARY = "#645B76"
    TEXT_MUTED = "#8E87A0"

    BORDEAUX = "#7A1F35"
    POSITIVE = "#21B36A"
    POSITIVE_LIGHT = "#ABE5C6"
    NEGATIVE = "#E13453"
    NEGATIVE_LIGHT = "#F2B0BC"

    GRID = "#DEE4EC"
    AXIS = "#8E87A0"


class FONTS:
    """Font stack strings dùng inline trong SVG attribute."""
    SANS = "'Inter','InterVN',sans-serif"
    SERIF = "'PFD','PFDVN',Georgia,serif"
    MONO = "'JBM','JBMVN','IBM Plex Mono',monospace"


# ============================================================
# SVG PRIMITIVE HELPERS
# ============================================================

def _fmt(v: float, prec: int = 1) -> str:
    """Format float to VN style (decimal comma) - dùng cho axis labels."""
    if v == int(v):
        return f"{int(v)}"
    return f"{v:.{prec}f}".replace(".", ",")


def _nice_step(value_range: float, max_ticks: int = 5) -> float:
    """Trả về 1 step "đẹp" (1, 2, 2.5, 5 * 10^k) cho axis."""
    if value_range <= 0:
        return 1.0
    raw = value_range / max_ticks
    mag = 10 ** math.floor(math.log10(raw))
    norm = raw / mag
    if norm < 1.5:
        nice = 1
    elif norm < 3:
        nice = 2
    elif norm < 7:
        nice = 5
    else:
        nice = 10
    return nice * mag


def _ticks(min_v: float, max_v: float, max_ticks: int = 5) -> list[float]:
    step = _nice_step(max_v - min_v, max_ticks)
    start = math.floor(min_v / step) * step
    out = []
    v = start
    while v <= max_v + step * 0.001:
        if v >= min_v - step * 0.001:
            out.append(round(v, 8))
        v += step
    return out


def _path_smooth(points: list[tuple[float, float]], smoothing: float = 0.18) -> str:
    """Cubic bezier smoothing cho line chart - cho line cong nhẹ thay vì gãy góc."""
    if len(points) < 2:
        return ""
    if len(points) == 2:
        return f"M {points[0][0]:.2f} {points[0][1]:.2f} L {points[1][0]:.2f} {points[1][1]:.2f}"

    d = [f"M {points[0][0]:.2f} {points[0][1]:.2f}"]
    for i in range(1, len(points)):
        p0 = points[i - 2] if i >= 2 else points[i - 1]
        p1 = points[i - 1]
        p2 = points[i]
        p3 = points[i + 1] if i + 1 < len(points) else p2

        c1x = p1[0] + (p2[0] - p0[0]) * smoothing
        c1y = p1[1] + (p2[1] - p0[1]) * smoothing
        c2x = p2[0] - (p3[0] - p1[0]) * smoothing
        c2y = p2[1] - (p3[1] - p1[1]) * smoothing
        d.append(f"C {c1x:.2f} {c1y:.2f}, {c2x:.2f} {c2y:.2f}, {p2[0]:.2f} {p2[1]:.2f}")
    return " ".join(d)


# ============================================================
# COMPONENT 1: LINE WITH ANNOTATIONS
# ============================================================

def line_with_annotations(
    series: list[dict],
    annotations: list[dict] | None = None,
    title: str = "",
    subtitle: str = "",
    y_label: str = "",
    y_unit: str = "",
    height: int = 200,
    show_area: bool = True,
    show_dots: bool = False,
    threshold: float | None = None,
    threshold_label: str = "",
) -> str:
    """
    SVG line/area chart với annotation callouts.

    series: list of dicts, mỗi dict 1 line:
        {
            "name": "DXY",
            "color": "#2A1A4A",      # optional, default Indigo
            "data": [(x_label, y_value), ...],  # x_label là string, y_value float
            "style": "solid"|"dashed", # optional
        }
    annotations: list of dicts, mỗi dict 1 callout:
        {
            "x_index": 3,             # index trong data array
            "series_index": 0,        # default 0
            "text": "Cuối Q3 đỉnh điểm",
            "anchor": "above"|"below"|"right"|"left",  # default above
            "value_label": "+12,3%",  # optional, bonus value display
        }
    threshold: optional horizontal reference line at y=threshold
    """
    if not series:
        return ""

    annotations = annotations or []

    W, H = 720, height
    PAD_L, PAD_R, PAD_T, PAD_B = 56, 32, 28, 38
    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B

    # determine global y range
    all_y = []
    for s in series:
        all_y.extend([d[1] for d in s["data"]])
    if threshold is not None:
        all_y.append(threshold)

    y_min = min(all_y)
    y_max = max(all_y)
    y_pad = (y_max - y_min) * 0.15 or abs(y_max) * 0.1 or 1
    y_min_p = y_min - y_pad * 0.5
    y_max_p = y_max + y_pad

    # x is index-based across longest series
    x_count = max(len(s["data"]) for s in series)
    x_labels = series[0]["data"]  # use first series for x labels

    def x_to_px(i: int) -> float:
        if x_count == 1:
            return PAD_L + plot_w / 2
        return PAD_L + (i / (x_count - 1)) * plot_w

    def y_to_px(y: float) -> float:
        return PAD_T + plot_h - ((y - y_min_p) / (y_max_p - y_min_p)) * plot_h

    # === GRID + AXIS ===
    y_ticks = _ticks(y_min_p, y_max_p, 4)
    grid_lines = []
    y_axis_labels = []
    for t in y_ticks:
        py = y_to_px(t)
        grid_lines.append(
            f'<line x1="{PAD_L}" y1="{py:.1f}" x2="{W - PAD_R}" y2="{py:.1f}" '
            f'stroke="{COLORS.GRID}" stroke-width="0.5" stroke-dasharray="2,2"/>'
        )
        label = _fmt(t, 1)
        if y_unit:
            label += y_unit
        y_axis_labels.append(
            f'<text x="{PAD_L - 8}" y="{py + 3:.1f}" text-anchor="end" '
            f'font-family="{FONTS.MONO}" font-size="7.5" fill="{COLORS.TEXT_SECONDARY}">{label}</text>'
        )

    # === X AXIS ===
    # show labels at ~5-7 positions max
    n_labels = min(7, x_count)
    step = max(1, (x_count - 1) // (n_labels - 1)) if n_labels > 1 else 1
    x_axis_labels = []
    for i in range(0, x_count, step):
        if i >= x_count:
            break
        px = x_to_px(i)
        lbl = escape(str(x_labels[i][0]))
        x_axis_labels.append(
            f'<text x="{px:.1f}" y="{H - PAD_B + 16}" text-anchor="middle" '
            f'font-family="{FONTS.SANS}" font-size="7.5" fill="{COLORS.TEXT_SECONDARY}" font-weight="500">{lbl}</text>'
        )
    # always show last
    if (x_count - 1) % step != 0:
        i = x_count - 1
        px = x_to_px(i)
        lbl = escape(str(x_labels[i][0]))
        x_axis_labels.append(
            f'<text x="{px:.1f}" y="{H - PAD_B + 16}" text-anchor="middle" '
            f'font-family="{FONTS.SANS}" font-size="7.5" fill="{COLORS.TEXT_SECONDARY}" font-weight="500">{lbl}</text>'
        )

    # === SERIES ===
    series_paths = []
    for s_idx, s in enumerate(series):
        color = s.get("color", COLORS.INDIGO if s_idx == 0 else COLORS.SLATE)
        style = s.get("style", "solid")
        dasharray = ' stroke-dasharray="4,3"' if style == "dashed" else ""
        pts = [(x_to_px(i), y_to_px(d[1])) for i, d in enumerate(s["data"])]

        # area fill (only first series, only if show_area)
        if show_area and s_idx == 0:
            area_path = _path_smooth(pts)
            # close to baseline
            baseline_y = y_to_px(max(y_min_p, 0)) if y_min_p < 0 else PAD_T + plot_h
            area_close = f"L {pts[-1][0]:.2f} {baseline_y:.2f} L {pts[0][0]:.2f} {baseline_y:.2f} Z"
            series_paths.append(
                f'<path d="{area_path} {area_close}" fill="{color}" fill-opacity="0.08" stroke="none"/>'
            )

        # line
        line_d = _path_smooth(pts)
        series_paths.append(
            f'<path d="{line_d}" fill="none" stroke="{color}" stroke-width="2"{dasharray} '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

        # dots
        if show_dots:
            for px, py in pts:
                series_paths.append(
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="{COLORS.IVORY}" '
                    f'stroke="{color}" stroke-width="1.4"/>'
                )

    # === THRESHOLD ===
    threshold_html = ""
    if threshold is not None:
        py = y_to_px(threshold)
        threshold_html = f'''
        <line x1="{PAD_L}" y1="{py:.1f}" x2="{W - PAD_R}" y2="{py:.1f}"
              stroke="{COLORS.BORDEAUX}" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.7"/>
        <text x="{W - PAD_R - 4}" y="{py - 4:.1f}" text-anchor="end"
              font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.BORDEAUX}" font-weight="600">
          {escape(threshold_label)} {_fmt(threshold)}
        </text>
        '''

    # === ANNOTATIONS ===
    ann_html = []
    for ann in annotations:
        s_idx = ann.get("series_index", 0)
        x_i = ann["x_index"]
        s_data = series[s_idx]["data"]
        if x_i >= len(s_data):
            continue
        y_val = s_data[x_i][1]
        ax = x_to_px(x_i)
        ay = y_to_px(y_val)

        anchor = ann.get("anchor", "above")
        text = ann.get("text", "")
        value_label = ann.get("value_label", "")

        # offset based on anchor
        if anchor == "above":
            tx, ty = ax, ay - 16
            text_anchor = "middle"
            line_y2 = ty + 4
            line_x2 = tx
        elif anchor == "below":
            tx, ty = ax, ay + 22
            text_anchor = "middle"
            line_y2 = ty - 8
            line_x2 = tx
        elif anchor == "right":
            tx, ty = ax + 14, ay - 2
            text_anchor = "start"
            line_x2 = tx - 4
            line_y2 = ty + 2
        else:  # left
            tx, ty = ax - 14, ay - 2
            text_anchor = "end"
            line_x2 = tx + 4
            line_y2 = ty + 2

        # marker dot
        ann_html.append(
            f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3.5" fill="{COLORS.ACCENT}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1.5"/>'
        )
        # leader line
        ann_html.append(
            f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{line_x2:.1f}" y2="{line_y2:.1f}" '
            f'stroke="{COLORS.ACCENT}" stroke-width="0.7" stroke-dasharray="1.5,1.5"/>'
        )
        # value label (mono, larger)
        if value_label:
            ann_html.append(
                f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{text_anchor}" '
                f'font-family="{FONTS.MONO}" font-size="8.5" fill="{COLORS.INDIGO}" font-weight="600">{escape(value_label)}</text>'
            )
            ty_text = ty + 9
        else:
            ty_text = ty
        # caption text
        ann_html.append(
            f'<text x="{tx:.1f}" y="{ty_text:.1f}" text-anchor="{text_anchor}" '
            f'font-family="{FONTS.SANS}" font-size="7" fill="{COLORS.TEXT_SECONDARY}" font-style="italic">{escape(text)}</text>'
        )

    # === LEGEND (if multi-series) ===
    legend_html = ""
    if len(series) > 1:
        items = []
        x_offset = PAD_L
        for s_idx, s in enumerate(series):
            color = s.get("color", COLORS.INDIGO if s_idx == 0 else COLORS.SLATE)
            name = escape(s.get("name", f"Series {s_idx+1}"))
            items.append(
                f'<g transform="translate({x_offset}, {PAD_T - 16})">'
                f'<line x1="0" y1="3" x2="14" y2="3" stroke="{color}" stroke-width="2.2"/>'
                f'<text x="18" y="6" font-family="{FONTS.SANS}" font-size="7.5" fill="{COLORS.CHARCOAL}" font-weight="600">{name}</text>'
                f'</g>'
            )
            x_offset += 8 + len(name) * 5 + 18
        legend_html = "".join(items)

    # === Y LABEL ROTATED ===
    y_label_html = ""
    if y_label:
        cy_label = PAD_T + plot_h / 2
        y_label_html = (
            f'<text x="14" y="{cy_label:.1f}" text-anchor="middle" '
            f'transform="rotate(-90, 14, {cy_label:.1f})" '
            f'font-family="{FONTS.SANS}" font-size="7" fill="{COLORS.TEXT_SECONDARY}" '
            f'font-weight="600" letter-spacing="0.08em">{escape(y_label.upper())}</text>'
        )

    title_html = f'<div class="vw-line-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-line-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-line-chart">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-line-svg">
    {y_label_html}
    {"".join(grid_lines)}
    {"".join(y_axis_labels)}
    {"".join(x_axis_labels)}
    {threshold_html}
    {"".join(series_paths)}
    {"".join(ann_html)}
    {legend_html}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 2: DOT PLOT DISTRIBUTION
# ============================================================

def dot_plot_distribution(
    items: list[dict],
    threshold: float | None = None,
    threshold_label: str = "Trần",
    show_quartiles: bool = True,
    show_median: bool = True,
    title: str = "",
    subtitle: str = "",
    x_unit: str = "%",
    height: int = 130,
) -> str:
    """
    Phân phối dot thật với quartile box + median line.

    items: [{"label": "VPB", "value": 28.3, "highlight": True, "annotate": "Sát trần"}]
    """
    if not items:
        return ""
    values = [i["value"] for i in items]
    sorted_v = sorted(values)
    n = len(sorted_v)

    def quantile(p: float) -> float:
        idx = p * (n - 1)
        lo, hi = int(math.floor(idx)), int(math.ceil(idx))
        if lo == hi:
            return sorted_v[lo]
        return sorted_v[lo] + (sorted_v[hi] - sorted_v[lo]) * (idx - lo)

    q1 = quantile(0.25)
    median = quantile(0.5)
    q3 = quantile(0.75)

    W, H = 720, height
    PAD_L, PAD_R, PAD_T, PAD_B = 24, 24, 36, 44
    plot_w = W - PAD_L - PAD_R

    v_min = min(values + ([threshold] if threshold else []))
    v_max = max(values + ([threshold] if threshold else []))
    pad = (v_max - v_min) * 0.08 or 1
    scale_min = max(0, v_min - pad)
    scale_max = v_max + pad

    def to_px(v: float) -> float:
        return PAD_L + (v - scale_min) / (scale_max - scale_min) * plot_w

    cy = PAD_T + (H - PAD_T - PAD_B) / 2

    # Quartile box (light accent band)
    quartile_html = ""
    if show_quartiles:
        x_q1 = to_px(q1)
        x_q3 = to_px(q3)
        quartile_html = (
            f'<rect x="{x_q1:.1f}" y="{cy - 18}" width="{x_q3 - x_q1:.1f}" height="36" '
            f'fill="{COLORS.ACCENT_50}" stroke="{COLORS.ACCENT_300}" stroke-width="0.6" rx="2"/>'
        )

    # Baseline
    baseline = (
        f'<line x1="{PAD_L}" y1="{cy:.1f}" x2="{W - PAD_R}" y2="{cy:.1f}" '
        f'stroke="{COLORS.AXIS}" stroke-width="0.6"/>'
    )

    # Median line
    median_html = ""
    if show_median:
        x_m = to_px(median)
        median_html = (
            f'<line x1="{x_m:.1f}" y1="{cy - 22}" x2="{x_m:.1f}" y2="{cy + 22}" '
            f'stroke="{COLORS.INDIGO}" stroke-width="1.6"/>'
            f'<text x="{x_m:.1f}" y="{cy - 26}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.INDIGO}" font-weight="600">'
            f'Trung vị {_fmt(median, 1)}</text>'
        )

    # Threshold
    threshold_html = ""
    if threshold is not None:
        x_t = to_px(threshold)
        threshold_html = (
            f'<line x1="{x_t:.1f}" y1="{cy - 30}" x2="{x_t:.1f}" y2="{cy + 30}" '
            f'stroke="{COLORS.BORDEAUX}" stroke-width="1.4" stroke-dasharray="3,2"/>'
            f'<text x="{x_t:.1f}" y="{cy + 42}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="7.5" fill="{COLORS.BORDEAUX}" font-weight="700">'
            f'{escape(threshold_label)} {_fmt(threshold, 1)}{x_unit}</text>'
        )

    # Dots (with collision-aware vertical offset)
    dots_html = []
    seen_x: dict[int, list[float]] = {}
    for it in items:
        v = it["value"]
        x = to_px(v)
        x_bucket = int(x / 8)  # 8px buckets
        offsets = seen_x.setdefault(x_bucket, [])
        n_existing = len(offsets)
        # alternate above/below
        offset = 0 if n_existing == 0 else (
            (n_existing // 2 + 1) * 7 * (-1 if n_existing % 2 == 0 else 1)
        )
        offsets.append(offset)
        py = cy + offset

        is_hl = it.get("highlight", False)
        color = COLORS.BORDEAUX if it.get("danger") else (
            COLORS.ACCENT if is_hl else COLORS.INDIGO
        )
        r = 5.5 if is_hl else 4.0
        opacity = "1" if is_hl else "0.85"

        dots_html.append(
            f'<circle cx="{x:.1f}" cy="{py:.1f}" r="{r}" fill="{color}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1.2" opacity="{opacity}"/>'
        )

        # Label above dot if highlight or every other one
        label = escape(it["label"])
        label_y = py - r - 4 if offset <= 0 else py + r + 9
        weight = "700" if is_hl else "500"
        fill = color if is_hl else COLORS.CHARCOAL
        dots_html.append(
            f'<text x="{x:.1f}" y="{label_y:.1f}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="6.8" fill="{fill}" font-weight="{weight}">{label}</text>'
        )

        # Optional annotation for highlight
        if is_hl and it.get("annotate"):
            ann = escape(it["annotate"])
            dots_html.append(
                f'<text x="{x:.1f}" y="{label_y - 9:.1f}" text-anchor="middle" '
                f'font-family="{FONTS.SANS}" font-size="6.5" fill="{COLORS.TEXT_SECONDARY}" font-style="italic">{ann}</text>'
            )

    # X-axis ticks
    x_ticks = _ticks(scale_min, scale_max, 5)
    tick_html = []
    for t in x_ticks:
        x_p = to_px(t)
        lbl = _fmt(t, 0) + x_unit
        tick_html.append(
            f'<line x1="{x_p:.1f}" y1="{cy + 22}" x2="{x_p:.1f}" y2="{cy + 26}" '
            f'stroke="{COLORS.AXIS}" stroke-width="0.6"/>'
            f'<text x="{x_p:.1f}" y="{H - PAD_B + 24}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="6.8" fill="{COLORS.TEXT_SECONDARY}">{lbl}</text>'
        )

    title_html = f'<div class="vw-dot-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-dot-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-dot-plot">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-dot-svg">
    {quartile_html}
    {baseline}
    {"".join(tick_html)}
    {threshold_html}
    {median_html}
    {"".join(dots_html)}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 3: SMALL MULTIPLES GRID
# ============================================================

def small_multiples_grid(
    panels: list[dict],
    cols: int = 3,
    title: str = "",
    subtitle: str = "",
    shared_y: bool = True,
    panel_height: int = 84,
    show_baseline: bool = True,
    polarity: str = "up_is_good",
) -> str:
    """
    Lưới mini line/bar charts (Tufte signature).

    panels: [{
        "label": "VPB",
        "data": [(x_label, y_value), ...],
        "highlight_index": 5,    # optional, dot ở index này
        "value_label": "+18%",   # corner value
        "value_color": "positive"|"negative"|"neutral",  # explicit override
        "color": "#xxx",          # full color override (skip auto)
    }]
    polarity: "up_is_good" (default) | "up_is_bad" | "neutral"
        - up_is_good: rising = green, falling = red (revenue, ROE, GDP)
        - up_is_bad: rising = red, falling = green (LDR, NPL, debt)
        - neutral: all slate (no semantic)
    """
    if not panels:
        return ""

    rows = math.ceil(len(panels) / cols)

    # Determine y range
    if shared_y:
        all_y = [d[1] for p in panels for d in p["data"]]
        y_min = min(all_y)
        y_max = max(all_y)
        pad = (y_max - y_min) * 0.12 or 1
        y_min_g = y_min - pad
        y_max_g = y_max + pad

    panel_w_unit = 220
    gap = 18
    PAD_L, PAD_R, PAD_T, PAD_B = 8, 8, 18, 14

    panels_html = []
    for idx, p in enumerate(panels):
        row = idx // cols
        col = idx % cols
        ox = col * (panel_w_unit + gap)
        oy = row * (panel_height + gap)

        if not shared_y:
            ys = [d[1] for d in p["data"]]
            y_lo, y_hi = min(ys), max(ys)
            pad = (y_hi - y_lo) * 0.15 or abs(y_hi) * 0.1 or 1
            y_min_p, y_max_p = y_lo - pad, y_hi + pad
        else:
            y_min_p, y_max_p = y_min_g, y_max_g

        plot_w = panel_w_unit - PAD_L - PAD_R
        plot_h = panel_height - PAD_T - PAD_B
        n = len(p["data"])

        def y2px(y):
            return oy + PAD_T + plot_h - ((y - y_min_p) / (y_max_p - y_min_p)) * plot_h

        def x2px(i):
            if n == 1:
                return ox + PAD_L + plot_w / 2
            return ox + PAD_L + i * plot_w / (n - 1)

        pts = [(x2px(i), y2px(d[1])) for i, d in enumerate(p["data"])]

        # baseline at y=0 if shown
        baseline_html = ""
        if show_baseline and y_min_p < 0 < y_max_p:
            zero_y = y2px(0)
            baseline_html = (
                f'<line x1="{ox + PAD_L}" y1="{zero_y:.1f}" x2="{ox + panel_w_unit - PAD_R}" y2="{zero_y:.1f}" '
                f'stroke="{COLORS.GRID}" stroke-width="0.5"/>'
            )

        # area + line
        area_d = _path_smooth(pts)
        last_x, _ = pts[-1]
        first_x, _ = pts[0]
        baseline_y = y2px(min(y_min_p, 0)) if y_min_p < 0 else oy + PAD_T + plot_h
        area_close = f"L {last_x:.2f} {baseline_y:.2f} L {first_x:.2f} {baseline_y:.2f} Z"

        # Determine color based on polarity
        first_v = p["data"][0][1]
        last_v = p["data"][-1][1]
        rising = last_v > first_v * 1.05
        falling = last_v < first_v * 0.95

        if polarity == "neutral":
            line_color = COLORS.SLATE
        elif polarity == "up_is_bad":
            if rising:
                line_color = COLORS.NEGATIVE
            elif falling:
                line_color = COLORS.POSITIVE
            else:
                line_color = COLORS.SLATE
        else:  # up_is_good
            if rising:
                line_color = COLORS.POSITIVE
            elif falling:
                line_color = COLORS.NEGATIVE
            else:
                line_color = COLORS.SLATE
        # Override
        if p.get("color"):
            line_color = p["color"]

        area_html = (
            f'<path d="{area_d} {area_close}" fill="{line_color}" fill-opacity="0.10" stroke="none"/>'
        )
        line_html = (
            f'<path d="{area_d}" fill="none" stroke="{line_color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )

        # Highlight dot
        highlight_html = ""
        hi = p.get("highlight_index", n - 1)  # default = last
        if 0 <= hi < n:
            hx, hy = pts[hi]
            highlight_html = (
                f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="2.8" fill="{COLORS.IVORY}" '
                f'stroke="{line_color}" stroke-width="1.6"/>'
            )

        # Label (top-left of panel)
        panel_label = escape(p["label"])
        # Value label (top-right)
        vl = p.get("value_label", "")
        v_color_key = p.get("value_color", "neutral")
        v_color = {
            "positive": COLORS.POSITIVE,
            "negative": COLORS.NEGATIVE,
            "neutral": COLORS.INDIGO,
        }.get(v_color_key, COLORS.INDIGO)

        panels_html.append(f'''
        <g>
          <rect x="{ox}" y="{oy}" width="{panel_w_unit}" height="{panel_height}"
                fill="{COLORS.PAPER}" stroke="{COLORS.GRID}" stroke-width="0.5" rx="3"/>
          <text x="{ox + 8}" y="{oy + 12}" font-family="{FONTS.SANS}" font-size="7.8"
                font-weight="700" fill="{COLORS.INDIGO}" letter-spacing="0.04em">{panel_label}</text>
          <text x="{ox + panel_w_unit - 8}" y="{oy + 12}" text-anchor="end"
                font-family="{FONTS.MONO}" font-size="8.5" font-weight="700" fill="{v_color}">{escape(vl)}</text>
          {baseline_html}
          {area_html}
          {line_html}
          {highlight_html}
        </g>
        ''')

    total_w = cols * panel_w_unit + (cols - 1) * gap
    total_h = rows * panel_height + (rows - 1) * gap

    title_html = f'<div class="vw-multi-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-multi-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-multi-grid">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" class="vw-multi-svg">
    {"".join(panels_html)}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 4: QUADRANT SCATTER
# ============================================================

def quadrant_scatter(
    points: list[dict],
    x_label: str,
    y_label: str,
    quadrants: dict | None = None,
    title: str = "",
    subtitle: str = "",
    median_split: bool = True,
    height: int = 320,
) -> str:
    """
    2D scatter với 4-quadrant labels.

    points: [{"label": "VCB", "x": 1.2, "y": 19.2, "color": "#2A1A4A", "size": 1.0}]
    quadrants: {"tl": "Quá đắt", "tr": "Sweet spot", "bl": "Tránh", "br": "Cơ hội"}
    median_split: nếu True, kẻ median lines; nếu False, kẻ ở 0
    """
    if not points:
        return ""
    quadrants = quadrants or {}

    W, H = 540, height
    PAD_L, PAD_R, PAD_T, PAD_B = 56, 24, 36, 44
    plot_w = W - PAD_L - PAD_R
    plot_h = H - PAD_T - PAD_B

    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    x_pad = (max(xs) - min(xs)) * 0.15 or abs(max(xs)) * 0.1 or 1
    y_pad = (max(ys) - min(ys)) * 0.15 or abs(max(ys)) * 0.1 or 1
    x_min, x_max = min(xs) - x_pad, max(xs) + x_pad
    y_min, y_max = min(ys) - y_pad, max(ys) + y_pad

    def x2px(x):
        return PAD_L + (x - x_min) / (x_max - x_min) * plot_w

    def y2px(y):
        return PAD_T + plot_h - (y - y_min) / (y_max - y_min) * plot_h

    # Median split lines
    if median_split:
        x_split = sorted(xs)[len(xs) // 2]
        y_split = sorted(ys)[len(ys) // 2]
    else:
        x_split = 0
        y_split = 0

    sx = x2px(x_split)
    sy = y2px(y_split)

    split_html = (
        f'<line x1="{sx:.1f}" y1="{PAD_T}" x2="{sx:.1f}" y2="{PAD_T + plot_h}" '
        f'stroke="{COLORS.GRID}" stroke-width="0.8" stroke-dasharray="3,2"/>'
        f'<line x1="{PAD_L}" y1="{sy:.1f}" x2="{PAD_L + plot_w}" y2="{sy:.1f}" '
        f'stroke="{COLORS.GRID}" stroke-width="0.8" stroke-dasharray="3,2"/>'
    )

    # Quadrant labels (italic, opacity) - support multi-line via "|" separator
    def _multiline_text(x, y, text, anchor, fill, size, opacity, vertical_align="top"):
        """Render multi-line text (split by | or \\n) using tspans."""
        lines = text.replace("\\n", "|").split("|")
        if len(lines) == 1:
            return (
                f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                f'font-family="{FONTS.SERIF}" font-size="{size}" fill="{fill}" '
                f'font-style="italic" opacity="{opacity}">{escape(lines[0].strip())}</text>'
            )
        line_height = size + 2
        if vertical_align == "bottom":
            # Adjust y so total block ends at given y
            y_start = y - (len(lines) - 1) * line_height
        else:
            y_start = y
        tspans = []
        for i, line in enumerate(lines):
            ty = y_start + i * line_height
            tspans.append(
                f'<text x="{x}" y="{ty}" text-anchor="{anchor}" '
                f'font-family="{FONTS.SERIF}" font-size="{size}" fill="{fill}" '
                f'font-style="italic" opacity="{opacity}">{escape(line.strip())}</text>'
            )
        return "".join(tspans)

    quad_html = []
    if quadrants.get("tl"):
        quad_html.append(_multiline_text(
            PAD_L + 8, PAD_T + 14, quadrants["tl"], "start", COLORS.SLATE, 9.5, 0.55, "top"
        ))
    if quadrants.get("tr"):
        quad_html.append(_multiline_text(
            W - PAD_R - 8, PAD_T + 14, quadrants["tr"], "end", COLORS.ACCENT, 9.5, 0.7, "top"
        ))
    if quadrants.get("bl"):
        quad_html.append(_multiline_text(
            PAD_L + 8, PAD_T + plot_h - 6, quadrants["bl"], "start", COLORS.BORDEAUX, 9.5, 0.55, "bottom"
        ))
    if quadrants.get("br"):
        quad_html.append(_multiline_text(
            W - PAD_R - 8, PAD_T + plot_h - 6, quadrants["br"], "end", COLORS.SLATE, 9.5, 0.55, "bottom"
        ))

    # Axis labels
    axis_html = (
        f'<text x="{W / 2:.1f}" y="{H - 6}" text-anchor="middle" '
        f'font-family="{FONTS.SANS}" font-size="8" fill="{COLORS.CHARCOAL}" '
        f'font-weight="600" letter-spacing="0.06em">{escape(x_label.upper())}</text>'
        f'<text x="14" y="{H / 2:.1f}" text-anchor="middle" transform="rotate(-90, 14, {H / 2:.1f})" '
        f'font-family="{FONTS.SANS}" font-size="8" fill="{COLORS.CHARCOAL}" '
        f'font-weight="600" letter-spacing="0.06em">{escape(y_label.upper())}</text>'
    )

    # X axis ticks
    x_ticks = _ticks(x_min, x_max, 5)
    y_ticks = _ticks(y_min, y_max, 5)
    tick_html = []
    for t in x_ticks:
        xp = x2px(t)
        tick_html.append(
            f'<text x="{xp:.1f}" y="{H - PAD_B + 12}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">{_fmt(t, 1)}</text>'
        )
    for t in y_ticks:
        yp = y2px(t)
        tick_html.append(
            f'<text x="{PAD_L - 6}" y="{yp + 3:.1f}" text-anchor="end" '
            f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">{_fmt(t, 1)}</text>'
        )

    # Frame
    frame_html = (
        f'<rect x="{PAD_L}" y="{PAD_T}" width="{plot_w}" height="{plot_h}" '
        f'fill="{COLORS.PAPER}" stroke="{COLORS.GRID}" stroke-width="0.6" rx="2"/>'
    )

    # Points
    pts_html = []
    for p in points:
        px = x2px(p["x"])
        py = y2px(p["y"])
        size = p.get("size", 1.0)
        r = 5 + size * 2
        color = p.get("color", COLORS.INDIGO)
        # halo
        pts_html.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r + 2}" fill="{color}" opacity="0.18"/>'
        )
        pts_html.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{color}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1.5"/>'
        )
        # label
        lbl = escape(p["label"])
        pts_html.append(
            f'<text x="{px:.1f}" y="{py - r - 5:.1f}" text-anchor="middle" '
            f'font-family="{FONTS.MONO}" font-size="7.5" fill="{COLORS.INDIGO}" font-weight="700">{lbl}</text>'
        )

    title_html = f'<div class="vw-quad-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-quad-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-quadrant">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-quad-svg">
    {frame_html}
    {split_html}
    {"".join(quad_html)}
    {"".join(tick_html)}
    {"".join(pts_html)}
    {axis_html}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 5: SLOPEGRAPH
# ============================================================

def slopegraph(
    items: list[dict],
    label_before: str = "Trước",
    label_after: str = "Sau",
    title: str = "",
    subtitle: str = "",
    unit: str = "%",
    height: int = 280,
) -> str:
    """
    Slopegraph (paired change dots) - Tufte favorite.

    items: [{"label": "VPB", "before": 28.3, "after": 35.0, "highlight": True}]
    """
    if not items:
        return ""

    W, H = 520, height
    PAD_T, PAD_B = 36, 28
    LEFT_X = 130
    RIGHT_X = W - 130
    plot_h = H - PAD_T - PAD_B

    all_v = [i["before"] for i in items] + [i["after"] for i in items]
    v_min, v_max = min(all_v), max(all_v)
    pad = (v_max - v_min) * 0.08 or 1
    s_min, s_max = v_min - pad, v_max + pad

    def y2px(v):
        return PAD_T + plot_h - (v - s_min) / (s_max - s_min) * plot_h

    # Header columns
    header_html = (
        f'<text x="{LEFT_X:.1f}" y="20" text-anchor="middle" '
        f'font-family="{FONTS.SANS}" font-size="8.5" font-weight="700" fill="{COLORS.INDIGO}" '
        f'letter-spacing="0.08em">{escape(label_before.upper())}</text>'
        f'<text x="{RIGHT_X:.1f}" y="20" text-anchor="middle" '
        f'font-family="{FONTS.SANS}" font-size="8.5" font-weight="700" fill="{COLORS.INDIGO}" '
        f'letter-spacing="0.08em">{escape(label_after.upper())}</text>'
    )

    # Vertical guide rules
    rules = (
        f'<line x1="{LEFT_X}" y1="{PAD_T}" x2="{LEFT_X}" y2="{PAD_T + plot_h}" '
        f'stroke="{COLORS.GRID}" stroke-width="0.6"/>'
        f'<line x1="{RIGHT_X}" y1="{PAD_T}" x2="{RIGHT_X}" y2="{PAD_T + plot_h}" '
        f'stroke="{COLORS.GRID}" stroke-width="0.6"/>'
    )

    # Sort by before for stable label placement
    sorted_items = sorted(items, key=lambda x: -x["before"])

    # Collision-aware label y positions
    # min spacing between labels = 11 px (font size + breathing)
    MIN_GAP = 11

    def _resolve_collisions(items_with_y, key="y_target"):
        """Push labels apart so no two are within MIN_GAP."""
        # Sort by target y, then iteratively push
        sorted_items = sorted(items_with_y, key=lambda x: x[key])
        for _ in range(40):  # max iterations
            moved = False
            for i in range(len(sorted_items) - 1):
                gap = sorted_items[i + 1][key] - sorted_items[i][key]
                if gap < MIN_GAP:
                    push = (MIN_GAP - gap) / 2
                    sorted_items[i][key] -= push
                    sorted_items[i + 1][key] += push
                    moved = True
            if not moved:
                break
        return sorted_items

    # Compute target y for each label on each side
    left_targets = [{"item": it, "y_target": y2px(it["before"])} for it in sorted_items]
    right_targets = [{"item": it, "y_target": y2px(it["after"])} for it in sorted_items]
    left_resolved = _resolve_collisions(left_targets)
    right_resolved = _resolve_collisions(right_targets)
    left_label_y = {id(it["item"]): it["y_target"] for it in left_resolved}
    right_label_y = {id(it["item"]): it["y_target"] for it in right_resolved}

    lines_html = []
    labels_left_html = []
    labels_right_html = []
    dots_html = []

    for it in sorted_items:
        b, a = it["before"], it["after"]
        is_hl = it.get("highlight", False)
        delta = a - b
        if is_hl:
            color = COLORS.ACCENT if delta > 0 else COLORS.BORDEAUX
        elif delta > 0:
            color = COLORS.POSITIVE
        elif delta < 0:
            color = COLORS.NEGATIVE
        else:
            color = COLORS.SLATE

        opacity = "1" if is_hl else "0.55"
        sw = "1.6" if is_hl else "1.0"

        y_b = y2px(b)
        y_a = y2px(a)

        lines_html.append(
            f'<line x1="{LEFT_X}" y1="{y_b:.1f}" x2="{RIGHT_X}" y2="{y_a:.1f}" '
            f'stroke="{color}" stroke-width="{sw}" opacity="{opacity}"/>'
        )

        # Dots
        r = 3.6 if is_hl else 2.8
        dots_html.append(
            f'<circle cx="{LEFT_X}" cy="{y_b:.1f}" r="{r}" fill="{color}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1"/>'
        )
        dots_html.append(
            f'<circle cx="{RIGHT_X}" cy="{y_a:.1f}" r="{r}" fill="{color}" '
            f'stroke="{COLORS.IVORY}" stroke-width="1"/>'
        )

        # Resolved label positions (collision-free)
        ly_left = left_label_y[id(it)]
        ly_right = right_label_y[id(it)]

        # Tiny connector if label moved away from its dot
        if abs(ly_left - y_b) > 2.5:
            labels_left_html.append(
                f'<line x1="{LEFT_X - 4:.1f}" y1="{y_b:.1f}" x2="{LEFT_X - 8:.1f}" y2="{ly_left:.1f}" '
                f'stroke="{color}" stroke-width="0.5" opacity="0.4"/>'
            )
        if abs(ly_right - y_a) > 2.5:
            labels_right_html.append(
                f'<line x1="{RIGHT_X + 4:.1f}" y1="{y_a:.1f}" x2="{RIGHT_X + 8:.1f}" y2="{ly_right:.1f}" '
                f'stroke="{color}" stroke-width="0.5" opacity="0.4"/>'
            )

        # Labels
        lbl = escape(it["label"])
        weight = "700" if is_hl else "500"
        ink = COLORS.INDIGO if is_hl else COLORS.CHARCOAL
        labels_left_html.append(
            f'<text x="{LEFT_X - 10}" y="{ly_left + 3:.1f}" text-anchor="end" '
            f'font-family="{FONTS.SANS}" font-size="8" fill="{ink}" font-weight="{weight}" opacity="{opacity}">'
            f'<tspan>{lbl}</tspan> '
            f'<tspan fill="{COLORS.TEXT_SECONDARY}" font-family="{FONTS.MONO}" font-size="7.5">{_fmt(b, 1)}{unit}</tspan>'
            f'</text>'
        )
        labels_right_html.append(
            f'<text x="{RIGHT_X + 10}" y="{ly_right + 3:.1f}" text-anchor="start" '
            f'font-family="{FONTS.SANS}" font-size="8" fill="{ink}" font-weight="{weight}" opacity="{opacity}">'
            f'<tspan fill="{COLORS.TEXT_SECONDARY}" font-family="{FONTS.MONO}" font-size="7.5">{_fmt(a, 1)}{unit}</tspan>'
            f' <tspan>{lbl}</tspan>'
            f'</text>'
        )

    title_html = f'<div class="vw-slope-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-slope-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-slopegraph">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-slope-svg">
    {header_html}
    {rules}
    {"".join(lines_html)}
    {"".join(dots_html)}
    {"".join(labels_left_html)}
    {"".join(labels_right_html)}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 6: SANKEY MINI
# ============================================================

def sankey_mini(
    sources: list[dict],
    targets: list[dict],
    flows: list[dict],
    title: str = "",
    subtitle: str = "",
    unit: str = "tỷ",
    height: int = 280,
) -> str:
    """
    Sankey nhỏ 3-5 sources -> 3-5 targets với Bezier curves.

    sources / targets: [{"id": "ng_hang", "label": "Ngân hàng", "color": "#2A1A4A"}]
    flows: [{"source": "ng_hang", "target": "tpdn", "value": 520}]
    """
    if not flows or not sources or not targets:
        return ""

    W, H = 560, height
    PAD_T, PAD_B = 36, 24
    LEFT_X, RIGHT_X = 110, W - 110
    NODE_W = 14
    plot_h = H - PAD_T - PAD_B

    # compute node values from flows
    src_values = {s["id"]: 0 for s in sources}
    tgt_values = {t["id"]: 0 for t in targets}
    for f in flows:
        src_values[f["source"]] = src_values.get(f["source"], 0) + f["value"]
        tgt_values[f["target"]] = tgt_values.get(f["target"], 0) + f["value"]

    total = sum(src_values.values()) or 1
    gap = 8

    # Source positions
    src_y = PAD_T
    src_layout = {}
    for s in sources:
        v = src_values.get(s["id"], 0)
        h = (v / total) * (plot_h - gap * (len(sources) - 1))
        src_layout[s["id"]] = {"y": src_y, "h": h, "value": v, "label": s.get("label", s["id"]),
                                "color": s.get("color", COLORS.INDIGO)}
        src_y += h + gap

    # Target positions
    tgt_y = PAD_T
    tgt_layout = {}
    for t in targets:
        v = tgt_values.get(t["id"], 0)
        h = (v / total) * (plot_h - gap * (len(targets) - 1))
        tgt_layout[t["id"]] = {"y": tgt_y, "h": h, "value": v, "label": t.get("label", t["id"]),
                                "color": t.get("color", COLORS.SLATE)}
        tgt_y += h + gap

    # Track offset per node for stacking flows
    src_off = {s["id"]: 0 for s in sources}
    tgt_off = {t["id"]: 0 for t in targets}

    # Header
    header_html = (
        f'<text x="{LEFT_X + NODE_W/2:.1f}" y="20" text-anchor="middle" '
        f'font-family="{FONTS.SANS}" font-size="8" font-weight="700" fill="{COLORS.INDIGO}" '
        f'letter-spacing="0.1em">NGUỒN</text>'
        f'<text x="{RIGHT_X + NODE_W/2:.1f}" y="20" text-anchor="middle" '
        f'font-family="{FONTS.SANS}" font-size="8" font-weight="700" fill="{COLORS.INDIGO}" '
        f'letter-spacing="0.1em">ĐÍCH</text>'
    )

    # Flows (draw before nodes)
    flows_html = []
    # Sort flows for visual stacking - largest first
    sorted_flows = sorted(flows, key=lambda x: -x["value"])
    for f in sorted_flows:
        s_id, t_id = f["source"], f["target"]
        v = f["value"]
        if s_id not in src_layout or t_id not in tgt_layout:
            continue
        s = src_layout[s_id]
        t = tgt_layout[t_id]

        # height of this flow at each side (proportional to value)
        sh = (v / total) * (plot_h - gap * (len(sources) - 1))
        th = (v / total) * (plot_h - gap * (len(targets) - 1))

        sy0 = s["y"] + src_off[s_id]
        sy1 = sy0 + sh
        ty0 = t["y"] + tgt_off[t_id]
        ty1 = ty0 + th

        src_off[s_id] += sh
        tgt_off[t_id] += th

        # Bezier path
        x0 = LEFT_X + NODE_W
        x1 = RIGHT_X
        cx1 = x0 + (x1 - x0) * 0.5
        cx2 = x1 - (x1 - x0) * 0.5

        path = (
            f"M {x0} {sy0:.2f} "
            f"C {cx1:.1f} {sy0:.2f}, {cx2:.1f} {ty0:.2f}, {x1} {ty0:.2f} "
            f"L {x1} {ty1:.2f} "
            f"C {cx2:.1f} {ty1:.2f}, {cx1:.1f} {sy1:.2f}, {x0} {sy1:.2f} Z"
        )
        flow_color = f.get("color", s["color"])
        flows_html.append(
            f'<path d="{path}" fill="{flow_color}" fill-opacity="0.32" stroke="none"/>'
        )

    # Nodes
    nodes_html = []
    MIN_NODE_H_FOR_LABEL = 14  # if node smaller, label sits in 2 lines anyway, push outside
    for s_id, s in src_layout.items():
        nodes_html.append(
            f'<rect x="{LEFT_X}" y="{s["y"]:.1f}" width="{NODE_W}" height="{s["h"]:.1f}" '
            f'fill="{s["color"]}" rx="1.5"/>'
        )
        # Position labels: if node tall enough, center; else push to top with gap
        cy_label = s["y"] + s["h"] / 2
        if s["h"] < MIN_NODE_H_FOR_LABEL:
            # If too small, place label aligned to node top with offset to avoid overlap
            cy_label = s["y"] + s["h"] / 2
        nodes_html.append(
            f'<text x="{LEFT_X - 8}" y="{cy_label - 2:.1f}" text-anchor="end" '
            f'font-family="{FONTS.SANS}" font-size="8" font-weight="600" fill="{COLORS.CHARCOAL}">'
            f'{escape(s["label"])}</text>'
            f'<text x="{LEFT_X - 8}" y="{cy_label + 8:.1f}" text-anchor="end" '
            f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">'
            f'+{_fmt(s["value"], 0)} {unit}</text>'
        )
    for t_id, t in tgt_layout.items():
        nodes_html.append(
            f'<rect x="{RIGHT_X}" y="{t["y"]:.1f}" width="{NODE_W}" height="{t["h"]:.1f}" '
            f'fill="{t["color"]}" rx="1.5"/>'
        )
        cy_label = t["y"] + t["h"] / 2
        nodes_html.append(
            f'<text x="{RIGHT_X + NODE_W + 8}" y="{cy_label - 2:.1f}" text-anchor="start" '
            f'font-family="{FONTS.SANS}" font-size="8" font-weight="600" fill="{COLORS.CHARCOAL}">'
            f'{escape(t["label"])}</text>'
            f'<text x="{RIGHT_X + NODE_W + 8}" y="{cy_label + 8:.1f}" text-anchor="start" '
            f'font-family="{FONTS.MONO}" font-size="7" fill="{COLORS.TEXT_SECONDARY}">'
            f'-{_fmt(t["value"], 0)} {unit}</text>'
        )

    title_html = f'<div class="vw-sankey-title">{escape(title)}</div>' if title else ""
    sub_html = f'<div class="vw-sankey-sub">{escape(subtitle)}</div>' if subtitle else ""

    return f'''
<div class="vw-sankey">
  {title_html}
  {sub_html}
  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="vw-sankey-svg">
    {header_html}
    {"".join(flows_html)}
    {"".join(nodes_html)}
  </svg>
</div>
'''


# ============================================================
# COMPONENT 7: COMPASS CALLOUT (editorial signature wrapper)
# ============================================================

def compass_callout(
    inner_html: str,
    callout_text: str,
    callout_label: str = "",
    position: str = "right",
    target_x_pct: float = 0.5,
    target_y_pct: float = 0.5,
) -> str:
    """
    Wrapper bọc bất kỳ viz HTML, thêm:
    - Accent dot ở target point
    - Leader line cong nhẹ (Bezier) chạy ra sidebar
    - Italic caption ở sidebar với vertical accent rule

    inner_html: HTML output từ bất kỳ component (gauge, line, ...)
    callout_text: caption italic
    callout_label: small uppercase eyebrow above caption
    position: "right" | "left"
    target_x_pct: x position (0-1) of target dot relative to inner viz width
    target_y_pct: y position (0-1) of target dot relative to inner viz height
    """
    label_html = ""
    if callout_label:
        label_html = f'<div class="vw-compass-label">{escape(callout_label)}</div>'

    pos_class = "vw-compass-right" if position == "right" else "vw-compass-left"

    return f'''
<div class="vw-compass {pos_class}" data-target-x="{target_x_pct}" data-target-y="{target_y_pct}">
  <div class="vw-compass-inner">{inner_html}</div>
  <div class="vw-compass-sidebar">
    <div class="vw-compass-rule"></div>
    {label_html}
    <div class="vw-compass-text">{escape(callout_text)}</div>
  </div>
</div>
'''


# ============================================================
# WAVE 8 STYLES
# ============================================================

def wave8_styles() -> str:
    """CSS riêng cho Wave 8 components - append after viz_styles()."""
    return """
/* ============ WAVE 8 - CHART LANGUAGE ============ */

/* Universal chart container */
.vw-line-chart, .vw-dot-plot, .vw-multi-grid, .vw-quadrant, .vw-slopegraph, .vw-sankey {
  background: var(--paper, #F4F6F9);
  border: 0.6px solid var(--rule-soft, rgba(22,99,60,0.30));
  border-radius: 4px;
  padding: 14px 16px 12px 16px;
  margin: 14px 0;
  page-break-inside: avoid;
}

.vw-line-svg, .vw-dot-svg, .vw-multi-svg, .vw-quad-svg, .vw-slope-svg, .vw-sankey-svg {
  display: block;
  width: 100%;
  height: auto;
  max-width: 100%;
}

/* Titles - shared pattern */
.vw-line-title, .vw-dot-title, .vw-multi-title, .vw-quad-title, .vw-slope-title, .vw-sankey-title {
  font-family: 'PFD','PFDVN',Georgia,serif;
  font-size: 11pt;
  font-weight: 600;
  color: var(--indigo, #2A1A4A);
  margin-bottom: 2px;
  line-height: 1.25;
}

.vw-line-sub, .vw-dot-sub, .vw-multi-sub, .vw-quad-sub, .vw-slope-sub, .vw-sankey-sub {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 8pt;
  color: var(--text-secondary, #645B76);
  margin-bottom: 10px;
  line-height: 1.4;
  font-style: italic;
}

/* Slopegraph - extra spacing for side labels */
.vw-slopegraph {
  padding: 14px 8px 12px 8px;
}

/* ============ COMPASS CALLOUT (Wave 9) ============ */

.vw-compass {
  display: flex;
  gap: 18px;
  align-items: stretch;
  margin: 16px 0;
  page-break-inside: avoid;
}

.vw-compass-right .vw-compass-inner { flex: 1 1 75%; min-width: 0; }
.vw-compass-right .vw-compass-sidebar { flex: 0 0 23%; }

.vw-compass-left { flex-direction: row-reverse; }
.vw-compass-left .vw-compass-inner { flex: 1 1 75%; min-width: 0; }
.vw-compass-left .vw-compass-sidebar { flex: 0 0 23%; }

.vw-compass-sidebar {
  display: flex;
  flex-direction: column;
  position: relative;
  padding: 4px 0 4px 14px;
}

.vw-compass-rule {
  position: absolute;
  left: 0; top: 8px; bottom: 8px;
  width: 1.4px;
  background: var(--accent, #16633C);
}

.vw-compass-label {
  font-family: 'Inter','InterVN',sans-serif;
  font-size: 6.5pt;
  font-weight: 700;
  color: var(--accent, #16633C);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.vw-compass-text {
  font-family: 'PFD','PFDVN',Georgia,serif;
  font-size: 9pt;
  font-style: italic;
  line-height: 1.5;
  color: var(--charcoal, #221A34);
}

/* ============ FINE-TUNING for SVG text */
/* Small multiples and quadrant frames need slightly tighter padding */
.vw-multi-grid { padding: 12px 14px; }
.vw-quadrant { padding: 12px 14px; }

/* Center sankey/slopegraph SVG */
.vw-sankey-svg, .vw-slope-svg, .vw-quad-svg {
  margin: 0 auto;
}
"""
