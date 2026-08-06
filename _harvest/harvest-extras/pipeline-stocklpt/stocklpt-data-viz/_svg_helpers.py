"""
StockLPT SVG Helpers - Reusable primitives.
==========================================

Helper functions cho mọi viz module:
- Format VN style (decimal comma)
- Nice axis ticks
- Bezier path smoothing
- Multi-line SVG text
- Collision resolution
"""
from __future__ import annotations
import math
from html import escape

from _tokens import COLORS, FONTS, METRICS


# ============================================================
# NUMBER FORMATTING
# ============================================================

def fmt_number(v: float, prec: int = 1) -> str:
    """Format số theo style VN (decimal comma)."""
    if v == int(v):
        return f"{int(v)}"
    return f"{v:.{prec}f}".replace(".", ",")


def fmt_compact(v: float) -> str:
    """Compact format: 1.234.567 -> '1,2M'. Cho axis labels."""
    av = abs(v)
    if av >= 1_000_000:
        return fmt_number(v / 1_000_000, 1) + "M"
    if av >= 1_000:
        return fmt_number(v / 1_000, 1) + "K"
    return fmt_number(v, 1)


# ============================================================
# AXIS TICKS
# ============================================================

def nice_step(value_range: float, max_ticks: int = 5) -> float:
    """Trả về step "đẹp" (1, 2, 2.5, 5 * 10^k) cho axis."""
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


def nice_ticks(min_v: float, max_v: float, max_ticks: int = 5) -> list[float]:
    """Generate axis ticks với nice numbers."""
    step = nice_step(max_v - min_v, max_ticks)
    start = math.floor(min_v / step) * step
    out = []
    v = start
    while v <= max_v + step * 0.001:
        if v >= min_v - step * 0.001:
            out.append(round(v, 8))
        v += step
    return out


# ============================================================
# PATH HELPERS
# ============================================================

def path_smooth(points: list[tuple[float, float]], smoothing: float = 0.18) -> str:
    """Cubic bezier smoothing path từ points list."""
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


def path_curve(x1: float, y1: float, x2: float, y2: float, curvature: float = 0.4) -> str:
    """Single Bezier curve giữa 2 điểm. Curvature trong 0-1."""
    dx = x2 - x1
    cx1 = x1 + dx * curvature
    cx2 = x2 - dx * curvature
    return f"M {x1:.2f} {y1:.2f} C {cx1:.2f} {y1:.2f}, {cx2:.2f} {y2:.2f}, {x2:.2f} {y2:.2f}"


# ============================================================
# TEXT HELPERS
# ============================================================

def multiline_svg_text(
    x: float, y: float, text: str,
    anchor: str = "start",
    fill: str = COLORS.CHARCOAL,
    size: float = 9.5,
    font: str = FONTS.SERIF,
    style: str = "italic",
    weight: str = "400",
    opacity: float = 1.0,
    vertical_align: str = "top",
    line_height_pad: float = 2.0,
) -> str:
    """
    Render multi-line SVG text. Split bằng '|' hoặc '\\n'.

    SVG <text> không parse \\n native, nên phải tách thành nhiều <text> elements
    hoặc tspan với x reset.
    """
    lines = text.replace("\\n", "|").split("|")
    if len(lines) == 1:
        return (
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-style="{style}" font-weight="{weight}" opacity="{opacity}">{escape(lines[0].strip())}</text>'
        )
    line_height = size + line_height_pad
    if vertical_align == "bottom":
        y_start = y - (len(lines) - 1) * line_height
    else:
        y_start = y
    parts = []
    for i, line in enumerate(lines):
        ty = y_start + i * line_height
        parts.append(
            f'<text x="{x}" y="{ty}" text-anchor="{anchor}" '
            f'font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-style="{style}" font-weight="{weight}" opacity="{opacity}">{escape(line.strip())}</text>'
        )
    return "".join(parts)


# ============================================================
# COLLISION RESOLUTION
# ============================================================

def resolve_label_collisions(
    items: list[dict],
    y_key: str = "y_target",
    min_gap: float = METRICS.LABEL_MIN_GAP,
    max_iterations: int = 40,
) -> list[dict]:
    """
    Iteratively push apart labels gần nhau theo y axis.
    Mỗi item phải có key `y_target` (sẽ bị mutate).

    Returns sorted list theo y_target.
    """
    if not items:
        return items
    sorted_items = sorted(items, key=lambda x: x[y_key])
    for _ in range(max_iterations):
        moved = False
        for i in range(len(sorted_items) - 1):
            gap = sorted_items[i + 1][y_key] - sorted_items[i][y_key]
            if gap < min_gap:
                push = (min_gap - gap) / 2
                sorted_items[i][y_key] -= push
                sorted_items[i + 1][y_key] += push
                moved = True
        if not moved:
            break
    return sorted_items


# ============================================================
# COLOR HELPERS
# ============================================================

def color_for_polarity(
    first_v: float, last_v: float,
    polarity: str = "up_is_good",
    threshold_pct: float = 0.05,
) -> str:
    """
    Trả về color dựa trên direction và polarity.

    polarity:
      'up_is_good' - tăng = green, giảm = red
      'up_is_bad'  - tăng = red, giảm = green
      'neutral'    - luôn slate
    """
    if polarity == "neutral":
        return COLORS.SLATE
    rising = last_v > first_v * (1 + threshold_pct)
    falling = last_v < first_v * (1 - threshold_pct)
    if polarity == "up_is_bad":
        if rising:
            return COLORS.NEGATIVE
        if falling:
            return COLORS.POSITIVE
        return COLORS.SLATE
    # up_is_good (default)
    if rising:
        return COLORS.POSITIVE
    if falling:
        return COLORS.NEGATIVE
    return COLORS.SLATE


def hex_with_opacity(hex_color: str, opacity: float) -> str:
    """Convert #RRGGBB to rgba() string."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{opacity})"
