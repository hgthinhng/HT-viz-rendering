"""
StockLPT Deep Analysis - Polish Extras
- sidebar_note: callout aside notes (methodology, definitions)
- glossary_alpha: auto-sort glossary terms alphabetical, group by first letter
- footnote_marker / footnote_list: footnote system

Usage:
    from extras import extras_styles, sidebar_note, glossary_alpha, footnote_marker, footnote_list
"""
from __future__ import annotations
from html import escape
from collections import defaultdict


def extras_styles() -> str:
    """Shared CSS cho sidebar, glossary, footnotes."""
    return r"""
/* ============ SIDEBAR CALLOUTS ============ */
.sidebar-note {
  margin: 6mm 0;
  padding: 5mm 6mm;
  background: #F4F6F9;
  border-left: 3px solid #16633C;
  page-break-inside: avoid;
}
.sidebar-note.methodology {
  border-left-color: #514B78;
}
.sidebar-note.warning {
  border-left-color: #E13453;
  background: #FCEAEC;
}
.sidebar-note.tip {
  border-left-color: #21B36A;
  background: #E8F7EF;
}
.sidebar-note-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  margin-bottom: 2mm;
}
.sidebar-note .sidebar-note-label { color: #16633C; }
.sidebar-note.methodology .sidebar-note-label { color: #514B78; }
.sidebar-note.warning .sidebar-note-label { color: #E13453; }
.sidebar-note.tip .sidebar-note-label { color: #21B36A; }
.sidebar-note-content {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9pt; font-weight: 450;
  line-height: 1.55; color: #221A34;
}
.sidebar-note-content em {
  font-style: italic; color: #514B78;
}
.sidebar-note-content strong {
  font-weight: 700; color: #2A1A4A;
}

/* ============ GLOSSARY ALPHABETICAL (compact inline letter) ============ */
.glossary-alpha {
  margin-top: 8mm;
  page-break-inside: auto;
}
.glossary-alpha-header {
  display: flex; justify-content: space-between;
  align-items: baseline; padding-bottom: 3mm;
  border-bottom: 1px solid #16633C; margin-bottom: 4mm;
}
.glossary-alpha-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 14pt; font-weight: 700;
  color: #2A1A4A;
}
.glossary-alpha-meta {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 600;
  color: #645B76; letter-spacing: 0.1em;
}
/* Compact 3-column row: letter | term | definition */
.glossary-alpha-row {
  display: grid; grid-template-columns: 6mm 30mm 1fr;
  gap: 4mm; padding: 2mm 0;
  border-bottom: 0.4px solid rgba(81,75,120,0.10);
  font-size: 9.5pt;
  align-items: baseline;
  page-break-inside: avoid;
}
.glossary-alpha-row.letter-start {
  border-top: 0.5px solid rgba(22,99,60,0.35);
  padding-top: 3mm; margin-top: 1mm;
}
.glossary-alpha-row.letter-start:first-child {
  border-top: none; padding-top: 2mm; margin-top: 0;
}
.glossary-alpha-letter-cell {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 700;
  color: #16633C; line-height: 1;
  letter-spacing: -0.01em;
}
.glossary-alpha-term {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-weight: 700; color: #2A1A4A;
}
.glossary-alpha-def {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; color: #221A34;
  line-height: 1.5;
}
.glossary-alpha-def em {
  font-style: italic; color: #645B76;
}

/* ============ FOOTNOTES ============ */
.fn-marker {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  vertical-align: super; line-height: 0;
  color: #16633C; padding: 0 0.5mm;
}
.footnotes-list {
  margin-top: 12mm;
  padding-top: 4mm;
  border-top: 1px solid rgba(81,75,120,0.3);
  page-break-inside: auto;
}
.footnotes-list-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #16633C; margin-bottom: 3mm;
}
.fn-item {
  display: grid; grid-template-columns: 8mm 1fr;
  gap: 2mm; padding: 1.5mm 0;
  font-size: 8.5pt;
}
.fn-num {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 700; color: #16633C;
  text-align: right; padding-right: 1mm;
}
.fn-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; line-height: 1.45;
  color: #514B78;
}
.fn-text em {
  font-style: italic; color: #645B76;
}
"""


# ============================================================
# SIDEBAR NOTE
# ============================================================
def sidebar_note(
    content: str,
    note_type: str = "note",
    label: str = None,
) -> str:
    """
    Sidebar callout aside.

    Args:
        content: HTML-allowed text (em/strong supported)
        note_type: 'note' (accent) | 'methodology' (slate) | 'warning' (red) | 'tip' (green)
        label: custom label, default based on note_type
    """
    default_labels = {
        "note": "Lưu ý",
        "methodology": "Phương pháp",
        "warning": "Cảnh báo",
        "tip": "Mẹo",
    }
    if label is None:
        label = default_labels.get(note_type, "Lưu ý")

    return f"""
<div class="sidebar-note {note_type}">
  <div class="sidebar-note-label">{escape(label)}</div>
  <div class="sidebar-note-content">{content}</div>
</div>
"""


# ============================================================
# GLOSSARY ALPHABETICAL
# ============================================================
def glossary_alpha(
    terms: list[dict],
    title: str = "Thuật ngữ",
    subtitle: str = "",
) -> str:
    """
    Auto-sort glossary terms alphabetically. Compact 3-column row layout:
    [letter] [term] [definition]. Letter chỉ hiện ở first row của mỗi letter group;
    continuation rows letter cell empty (alignment preserved).

    Args:
        terms: list of {"term": str, "def": str, "context": str (optional)}
    """
    # Sort by term (case-insensitive)
    sorted_terms = sorted(terms, key=lambda t: t.get("term", "").upper())

    # Build flat rows; track letter changes to mark .letter-start rows
    rows = []
    prev_letter = None
    for t in sorted_terms:
        term_str = t.get("term", "")
        first = term_str.upper()
        letter = first[0] if first else "#"

        is_letter_start = letter != prev_letter
        letter_cell = letter if is_letter_start else ""
        row_cls = "glossary-alpha-row letter-start" if is_letter_start else "glossary-alpha-row"

        def_text = t.get("def", "")
        if t.get("context"):
            def_text += f' <em>{escape(t["context"])}</em>'

        rows.append(f"""
        <div class="{row_cls}">
          <div class="glossary-alpha-letter-cell">{escape(letter_cell)}</div>
          <div class="glossary-alpha-term">{escape(term_str)}</div>
          <div class="glossary-alpha-def">{def_text}</div>
        </div>""")

        prev_letter = letter

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="glossary-alpha-meta">{escape(subtitle)}</div>'

    return f"""
<div class="glossary-alpha">
  <div class="glossary-alpha-header">
    <div class="glossary-alpha-title">{escape(title)}</div>
    {subtitle_html}
  </div>
  {''.join(rows)}
</div>
"""


# ============================================================
# FOOTNOTE SYSTEM
# ============================================================
def footnote_marker(n: int) -> str:
    """Inline superscript footnote marker. Use trong body text."""
    return f'<span class="fn-marker">[{n}]</span>'


def footnote_list(
    items: list[str],
    label: str = "Chú thích",
) -> str:
    """
    Footnote list ở cuối Phần hoặc cuối bài.

    Args:
        items: list of footnote text strings (numbered automatically)
    """
    rows = []
    for i, item in enumerate(items, 1):
        rows.append(f"""
        <div class="fn-item">
          <div class="fn-num">{i}.</div>
          <div class="fn-text">{item}</div>
        </div>
        """)

    return f"""
<div class="footnotes-list">
  <div class="footnotes-list-label">{escape(label)}</div>
  {''.join(rows)}
</div>
"""
