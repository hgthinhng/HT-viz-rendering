#!/usr/bin/env python3
"""
render_engine_extras.py — 5 new DIAGRAM primitives + 4 inline elements.

Designed to be imported by render_engine.py:
    from render_engine_extras import register_extras
    register_extras(render_engine)

Or used standalone for individual diagram generation.

NEW DIAGRAMs:
- matrix2x3: 2x3 grid with optional headers
- pyramid: 3-level hierarchy (top→mid→base)
- cycle: circular feedback loop with arrows
- comparison: side-by-side two-column with bullet lists
- gauge: semicircle indicator with zones

NEW inline elements:
- KEYWORD: bold+highlight emphasis
- CALLOUT: inline mini-callout (warning/tip/note variants)
- ICON: contextual icon (book, lightbulb, warning, chart, scale, gear, arrow)
- LAYOUT: 2-column floating layout

All return OOXML strings matching render_engine.py conventions.
"""

# Note: This file requires render_engine.py's helper functions (run, para, esc, pid, C palette).
# When imported, expects these to be available via from render_engine import ...

import re

try:
    from render_engine import run, para, esc, pid, C
except ImportError:
    # Standalone mode — define minimal stubs for testing
    C = {"section_purple": "2C3878", "gold": "B8941F", "muted": "6B6B6B", "icon_blue": "1A5270",
         "icon_orange": "B85A1C", "icon_green": "2E6B3E", "box_blue_bg": "EAF2F5", "box_orange_bg": "F5EDE5"}

    def run(text, **kwargs):
        return f'<r>{text}</r>'

    def para(content, **kwargs):
        return f'<p>{content}</p>'

    def esc(t):
        return t

    def pid():
        return "00000000"


# ============================================================================
# DIAGRAM: matrix2x3
# ============================================================================

def render_diagram_matrix2x3(params):
    """
    Render a 2x3 matrix grid.
    Params: r1c1, r1c2, r1c3, r2c1, r2c2, r2c3, header_top, header_left
    """
    cells = [[params.get(f"r{r}c{c}", "") for c in (1, 2, 3)] for r in (1, 2)]
    header_top = params.get("header_top", "").split(",") if params.get("header_top") else None
    header_left = params.get("header_left", "").split(",") if params.get("header_left") else None

    paras = []
    paras.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">[Diagram: 2x3 matrix]</w:t></w:r></w:p>')

    # Build TABLE with optional headers
    rows_xml = []
    if header_top:
        cells_xml = []
        if header_left:
            cells_xml.append(_table_cell("", bold=False))
        for h in header_top:
            cells_xml.append(_table_cell(h.strip(), bold=True, fill="2C3878", color="FFFFFF"))
        rows_xml.append(f'<w:tr>{"".join(cells_xml)}</w:tr>')

    for ri, row in enumerate(cells):
        cells_xml = []
        if header_left and ri < len(header_left):
            cells_xml.append(_table_cell(header_left[ri].strip(), bold=True))
        for cell_text in row:
            cells_xml.append(_table_cell(cell_text))
        rows_xml.append(f'<w:tr>{"".join(cells_xml)}</w:tr>')

    table = f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>{"".join(rows_xml)}</w:tbl>'
    paras.append(table)

    return "\n".join(paras)


def _table_cell(text, bold=False, fill=None, color="1F1F1F"):
    fill_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    bold_xml = "<w:b/>" if bold else ""
    return (
        f'<w:tc><w:tcPr><w:tcW w:w="1500" w:type="dxa"/>{fill_xml}</w:tcPr>'
        f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr>{bold_xml}<w:color w:val="{color}"/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
        f'</w:tc>'
    )


# ============================================================================
# DIAGRAM: pyramid
# ============================================================================

def render_diagram_pyramid(params):
    """3-level pyramid hierarchy.
    Params: top, mid, base, top_label, mid_label, base_label
    """
    top = params.get("top", "")
    mid = params.get("mid", "")
    base = params.get("base", "")
    top_lbl = params.get("top_label", "")
    mid_lbl = params.get("mid_label", "")
    base_lbl = params.get("base_label", "")

    paras = []
    paras.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">[Diagram: Pyramid]</w:t></w:r></w:p>')

    # Use centered text with indentation for visual pyramid effect
    levels = [
        ("△  " + top + (f"  ({top_lbl})" if top_lbl else ""), C["icon_blue"], 4000),
        ("▼  " + mid + (f"  ({mid_lbl})" if mid_lbl else ""), C["icon_orange"], 2000),
        ("▼  " + base + (f"  ({base_lbl})" if base_lbl else ""), C["icon_green"], 0),
    ]
    for text, color, indent in levels:
        paras.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:ind w:left="{indent}" w:right="{indent}"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:color w:val="{color}"/><w:sz w:val="22"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
        )

    return "\n".join(paras)


# ============================================================================
# DIAGRAM: cycle
# ============================================================================

def render_diagram_cycle(params):
    """Circular feedback loop.
    Params: step1, step2, step3, step4 (and optional step5, step6), direction
    """
    steps = []
    for i in range(1, 7):
        s = params.get(f"step{i}")
        if s:
            steps.append(s)
    direction = params.get("direction", "clockwise")

    paras = []
    paras.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">[Diagram: Cycle ({direction})]</w:t></w:r></w:p>')

    # Render as text with circular arrows: A → B → C → D ↺
    arrow = " → ".join([esc(s) for s in steps])
    if direction == "clockwise":
        arrow += "  ↺"
    else:
        arrow += "  ↻"

    paras.append(
        f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        f'<w:r><w:rPr><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr>'
        f'<w:t xml:space="preserve">{arrow}</w:t></w:r></w:p>'
    )

    return "\n".join(paras)


# ============================================================================
# DIAGRAM: comparison (side-by-side)
# ============================================================================

def render_diagram_comparison(params):
    """Side-by-side comparison.
    Params: left_title, left, right_title, right
    Use \\n to separate bullets within left/right.
    """
    lt = params.get("left_title", "Left")
    rt = params.get("right_title", "Right")
    left_items = params.get("left", "").split("\\n")
    right_items = params.get("right", "").split("\\n")

    paras = []
    paras.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">[Diagram: Comparison]</w:t></w:r></w:p>')

    # 2-column table
    rows_xml = []
    # Header row
    rows_xml.append(
        f'<w:tr>'
        f'{_table_cell(lt, bold=True, fill="2C3878", color="FFFFFF")}'
        f'{_table_cell(rt, bold=True, fill="2C3878", color="FFFFFF")}'
        f'</w:tr>'
    )
    # Content rows: zip left and right items
    max_len = max(len(left_items), len(right_items))
    for i in range(max_len):
        l = left_items[i].strip() if i < len(left_items) else ""
        r = right_items[i].strip() if i < len(right_items) else ""
        rows_xml.append(
            f'<w:tr>'
            f'{_table_cell("• " + l if l else "")}'
            f'{_table_cell("• " + r if r else "")}'
            f'</w:tr>'
        )

    table = f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>{"".join(rows_xml)}</w:tbl>'
    paras.append(table)

    return "\n".join(paras)


# ============================================================================
# DIAGRAM: gauge
# ============================================================================

def render_diagram_gauge(params):
    """Semicircle gauge with zones.
    Params: label, value, min, max, zones=Low(0-3),Mid(3-7),High(7-10)
    """
    label = params.get("label", "Score")
    value = params.get("value", "0")
    vmin = params.get("min", "0")
    vmax = params.get("max", "10")
    zones = params.get("zones", "")

    paras = []
    paras.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="{C["section_purple"]}"/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">[Diagram: Gauge]</w:t></w:r></w:p>')

    # Render as text gauge: "Score: 7/10  [Low | Mid | █High█]"
    try:
        val_num = float(value)
        max_num = float(vmax)
        min_num = float(vmin)
        ratio = (val_num - min_num) / (max_num - min_num) if max_num > min_num else 0
        bar_len = 30
        filled = int(ratio * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
    except ValueError:
        bar = "?" * 30

    main_text = f"{label}: {value}/{vmax}  [{bar}]"
    paras.append(
        f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        f'<w:r><w:rPr><w:b/><w:color w:val="{C["icon_orange"]}"/><w:sz w:val="22"/><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
        f'<w:t xml:space="preserve">{esc(main_text)}</w:t></w:r></w:p>'
    )
    if zones:
        paras.append(
            f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:color w:val="{C["muted"]}"/><w:sz w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">Zones: {esc(zones)}</w:t></w:r></w:p>'
        )

    return "\n".join(paras)


# ============================================================================
# Inline elements
# ============================================================================

def render_inline_keyword(text):
    """[KEYWORD: term] → bold + yellow highlight."""
    return f'<w:r><w:rPr><w:b/><w:color w:val="1F1F1F"/><w:shd w:val="clear" w:color="auto" w:fill="FFFCEB"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def render_inline_callout(callout_type, text):
    """[CALLOUT: warning|tip|note]text[/CALLOUT] → inline mini-callout."""
    type_colors = {
        "warning": ("B85A1C", "F5EDE5"),
        "tip": ("B8941F", "FAF6E5"),
        "note": ("1A5270", "EAF2F5"),
    }
    color, fill = type_colors.get(callout_type, type_colors["note"])
    icon = {"warning": "⚠", "tip": "💡", "note": "ℹ"}.get(callout_type, "•")
    return (
        f'<w:r><w:rPr><w:b/><w:color w:val="{color}"/><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:rPr>'
        f'<w:t xml:space="preserve">  {icon} {esc(text)}  </w:t></w:r>'
    )


def render_inline_icon(icon_name):
    """[ICON: book|lightbulb|...] → inline icon character."""
    icon_map = {
        "book": "📖", "lightbulb": "💡", "warning": "⚠", "chart": "📊",
        "scale": "⚖", "gear": "⚙", "arrow": "→", "check": "✓", "cross": "✗",
        "star": "★", "info": "ℹ",
    }
    icon = icon_map.get(icon_name, "•")
    return f'<w:r><w:rPr><w:color w:val="{C["icon_blue"]}"/></w:rPr><w:t xml:space="preserve"> {icon} </w:t></w:r>'


def render_layout_2col(left, right):
    """[LAYOUT: 2col]left | right[/LAYOUT] → 2-column inline table."""
    rows_xml = (
        f'<w:tr>'
        f'{_table_cell(left, bold=False)}'
        f'{_table_cell(right, bold=False)}'
        f'</w:tr>'
    )
    table = f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9000" w:type="dxa"/></w:tblPr>{rows_xml}</w:tbl>'
    return table


# ============================================================================
# Registration helper
# ============================================================================

DIAGRAM_REGISTRY = {
    "matrix2x3": render_diagram_matrix2x3,
    "pyramid": render_diagram_pyramid,
    "cycle": render_diagram_cycle,
    "comparison": render_diagram_comparison,
    "gauge": render_diagram_gauge,
}

INLINE_REGISTRY = {
    "KEYWORD": render_inline_keyword,
    "CALLOUT": render_inline_callout,
    "ICON": render_inline_icon,
    "LAYOUT_2COL": render_layout_2col,
}


def register_extras(engine_module):
    """Patch render_engine.py to use new primitives."""
    # Add to render_engine's diagram dispatch table
    if hasattr(engine_module, "DIAGRAM_TYPES"):
        engine_module.DIAGRAM_TYPES.update(DIAGRAM_REGISTRY)
    # Add inline elements to inline parser
    if hasattr(engine_module, "INLINE_PROCESSORS"):
        engine_module.INLINE_PROCESSORS.update(INLINE_REGISTRY)


if __name__ == "__main__":
    # Quick smoke test
    print("Available DIAGRAM types:", list(DIAGRAM_REGISTRY.keys()))
    print("Available inline elements:", list(INLINE_REGISTRY.keys()))
    print("\nSample matrix2x3:")
    print(render_diagram_matrix2x3({
        "r1c1": "A", "r1c2": "B", "r1c3": "C",
        "r2c1": "D", "r2c2": "E", "r2c3": "F",
        "header_top": "Col1,Col2,Col3", "header_left": "Row1,Row2"
    })[:200])
