"""
StockLPT Deep Analysis - Section Opener Variants

3 variants để mở Phần I/II/III của bài deep analysis:
- standard: current behavior (Roman + title + dek)
- hero_stat: mở Phần với 1 mega number signature
- quote: mở Phần với pull quote dramatic

Usage:
    from section_openers import section_opener_styles, section_opener_standard, ...
    css = build_css(...) + viz_styles() + cover_styles() + section_opener_styles()
"""
from __future__ import annotations
from html import escape


def section_opener_styles() -> str:
    """Shared CSS cho 3 section opener variants."""
    return r"""
/* ============ SECTION OPENER VARIANTS ============ */

/* ---------- VARIANT 1: STANDARD (current) ---------- */
/* Existing .section-opener handles this - reuse */

/* ---------- VARIANT 2: HERO-STAT OPENER ---------- */
.section-opener-hero {
  margin: 14mm -24mm 12mm -24mm;
  padding: 12mm 24mm 10mm 24mm;
  background: #F4F6F9;
  border-top: 3px solid #16633C;
  border-bottom: 3px solid #16633C;
  position: relative;
  page-break-after: avoid;
  page-break-inside: avoid;
}
.section-opener-hero .so-h-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #16633C; margin-bottom: 4mm;
}
.section-opener-hero .so-h-grid {
  display: grid; grid-template-columns: 70mm 1fr;
  gap: 10mm; align-items: start;
}
.section-opener-hero .so-h-mega {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 60pt; font-weight: 700;
  color: #2A1A4A; line-height: 0.95;
  letter-spacing: -0.02em;
  margin-bottom: 1mm;
}
.section-opener-hero .so-h-unit {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9pt; font-weight: 600;
  letter-spacing: 0.05em; color: #514B78;
}
.section-opener-hero .so-h-content h2 {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 22pt; font-weight: 700;
  line-height: 1.15; color: #2A1A4A;
  margin: 0 0 4mm 0; letter-spacing: -0.005em;
}
.section-opener-hero .so-h-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10.5pt; font-weight: 500;
  font-style: italic; color: #514B78;
  line-height: 1.55;
}

/* ---------- VARIANT 3: QUOTE OPENER ---------- */
.section-opener-quote {
  margin: 14mm 0 12mm 0;
  padding: 0;
  page-break-after: avoid;
  page-break-inside: avoid;
}
.section-opener-quote .so-q-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #16633C; margin-bottom: 4mm;
}
.section-opener-quote .so-q-mark {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 80pt; font-weight: 700;
  color: #16633C; line-height: 0.6;
  margin: 0 0 -6mm -2mm;
  font-style: italic;
}
.section-opener-quote .so-q-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 18pt; font-weight: 500;
  font-style: italic; color: #2A1A4A;
  line-height: 1.4; margin-bottom: 6mm;
  max-width: 150mm;
}
.section-opener-quote .so-q-attribution {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; font-weight: 600;
  color: #645B76; margin-bottom: 8mm;
  letter-spacing: 0.04em;
}
.section-opener-quote .so-q-attribution::before {
  content: "-- ";
  color: #16633C;
}
.section-opener-quote h2 {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 22pt; font-weight: 700;
  line-height: 1.15; color: #2A1A4A;
  margin: 0 0 4mm 0; letter-spacing: -0.005em;
  padding-top: 6mm;
  border-top: 1px solid rgba(81,75,120,0.25);
}
.section-opener-quote .so-q-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10.5pt; font-weight: 500;
  font-style: italic; color: #514B78;
  line-height: 1.55; max-width: 145mm;
}
"""


def section_opener_hero_stat(
    section_num: str,
    title: str,
    dek: str,
    mega_value: str,
    mega_unit: str,
) -> str:
    """
    Section opener với 1 mega number bên trái + heading bên phải.

    Use case: Phần II hoặc V khi có 1 data point central.

    Args:
        section_num: "Phần II" hoặc "PHẦN II"
        title: heading text
        dek: italic subtitle
        mega_value: big number
        mega_unit: unit + context
    """
    return f"""
<div class="section-opener-hero">
  <div class="so-h-eyebrow">{escape(section_num)}</div>
  <div class="so-h-grid">
    <div>
      <div class="so-h-mega">{escape(mega_value)}</div>
      <div class="so-h-unit">{escape(mega_unit)}</div>
    </div>
    <div class="so-h-content">
      <h2>{escape(title)}</h2>
      <div class="so-h-dek">{escape(dek)}</div>
    </div>
  </div>
</div>
"""


def section_opener_quote(
    section_num: str,
    quote: str,
    attribution: str,
    title: str,
    dek: str,
) -> str:
    """
    Section opener với pull quote dramatic + heading.

    Use case: Phần với 1 statement signature từ NHNN, expert, hoặc framing.

    Args:
        section_num: "Phần III"
        quote: italic quote text
        attribution: source (e.g. "Phó Thống đốc NHNN, Q1/2026")
        title: heading sau quote
        dek: italic subtitle
    """
    return f"""
<div class="section-opener-quote">
  <div class="so-q-eyebrow">{escape(section_num)}</div>
  <div class="so-q-mark">"</div>
  <div class="so-q-text">{escape(quote)}</div>
  <div class="so-q-attribution">{escape(attribution)}</div>
  <h2>{escape(title)}</h2>
  <div class="so-q-dek">{escape(dek)}</div>
</div>
"""
