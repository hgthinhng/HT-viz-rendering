"""
opvia_DailyReport_polish.render
================================
Module render PDF cho skill opvia-DailyReport-polish. Chỉ phục vụ DAILY report.

Usage:
    from render import build_css, render_pdf

    css = build_css(date_str='23/04/2026')
    html = f'<!DOCTYPE html><html><head><style>{css}</style></head><body>...</body></html>'
    render_pdf(html, '/path/to/output.pdf')
"""

import os
import re
import warnings

warnings.filterwarnings('ignore')


def get_fonts_dir() -> str:
    """Trả về absolute path tới folder fonts kèm theo skill."""
    here = os.path.dirname(os.path.abspath(__file__))
    fonts = os.path.join(here, 'fonts')
    if not os.path.isdir(fonts):
        raise RuntimeError(f"Fonts folder không tìm thấy: {fonts}")
    return fonts


def build_font_face(fonts_dir: str = None) -> str:
    """
    Sinh @font-face block cho cả Latin và Vietnamese subsets.
    
    FONT MAPPING (Wave 1.7 - Lora + Plex Mono):
    - PFD/PFDVN aliases → Lora (heading + body serif)
    - JBM/JBMVN aliases → IBM Plex Mono (numbers, ticker badges)
    - Inter aliases unchanged (UI/labels/eyebrows)
    Aliases preserved để không phải đổi 100+ references.
    """
    F = fonts_dir or get_fonts_dir()
    return f"""
@font-face {{ font-family: 'Inter'; font-weight: 400; src: url('file://{F}/inter-latin-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 500; src: url('file://{F}/inter-latin-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 600; src: url('file://{F}/inter-latin-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 700; src: url('file://{F}/inter-latin-700.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 400; src: url('file://{F}/inter-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 500; src: url('file://{F}/inter-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 600; src: url('file://{F}/inter-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 700; src: url('file://{F}/inter-vn-700.woff2') format('woff2'); }}

/* JBM/JBMVN aliases → IBM Plex Mono */
@font-face {{ font-family: 'JBM'; font-weight: 400; src: url('file://{F}/plex-mono-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 500; src: url('file://{F}/plex-mono-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 600; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 700; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 400; src: url('file://{F}/plex-mono-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 500; src: url('file://{F}/plex-mono-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 600; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 700; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}

/* PFD/PFDVN aliases → Lora */
@font-face {{ font-family: 'PFD'; font-weight: 400; src: url('file://{F}/lora-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFD'; font-weight: 500; src: url('file://{F}/lora-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFD'; font-weight: 600; src: url('file://{F}/lora-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFD'; font-weight: 700; src: url('file://{F}/lora-vn-700.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFD'; font-weight: 400; font-style: italic; src: url('file://{F}/lora-vn-400i.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFD'; font-weight: 500; font-style: italic; src: url('file://{F}/lora-vn-500i.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 400; src: url('file://{F}/lora-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 500; src: url('file://{F}/lora-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 600; src: url('file://{F}/lora-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 700; src: url('file://{F}/lora-vn-700.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 400; font-style: italic; src: url('file://{F}/lora-vn-400i.woff2') format('woff2'); }}
@font-face {{ font-family: 'PFDVN'; font-weight: 500; font-style: italic; src: url('file://{F}/lora-vn-500i.woff2') format('woff2'); }}
"""


# Font stacks - dùng ở mọi nơi
SANS = "'Inter', 'InterVN', sans-serif"
MONO = "'JBM', 'JBMVN', monospace"
SERIF = "'PFD', 'PFDVN', serif"


def build_css(date_str: str, fonts_dir: str = None) -> str:
    """
    Sinh CSS đầy đủ cho 1 daily report.
    date_str: "23/04/2026" sẽ chèn vào footer
    """
    font_face = build_font_face(fonts_dir)
    return f"""
{font_face}

:root {{
  --prussian: #003153; --prussian-50: #E8F2F9; --prussian-100: #B3D1E6; --prussian-700: #001A2E;
  --brass: #B5A642; --brass-300: #CCC46B;
  --slate: #4A6FA5; --ivory: #F5F1E8; --charcoal: #2B2B2B; --ink: #1A1A1A;
  --text-secondary: #9A9688;
  --bordeaux: #722F37; --bordeaux-50: #F5ECED;
  --positive: #2E7D52; --positive-bg: #EDF7F1;
  --negative: #C0392B; --negative-bg: #FBEEEC;
}}

@page {{
  size: A4;
  margin: 16mm 0 16mm 0;
  @bottom-left {{
    content: "OPVIA ADVISORY  ·  {date_str}";
    font-family: {SANS}; font-size: 7pt; color: #9A9688;
    border-top: 1px solid rgba(181,166,66,0.35);
    padding-top: 5px; padding-left: 20mm; width: 50%;
  }}
  @bottom-right {{
    content: counter(page);
    font-family: {SANS}; font-size: 7pt; color: #9A9688;
    border-top: 1px solid rgba(181,166,66,0.35);
    padding-top: 5px; padding-right: 20mm; text-align: right; width: 50%;
  }}
}}
@page :first {{ margin-top: 0; }}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: {SERIF}; font-size: 9.5pt; line-height: 1.65; font-weight: 450; color: var(--charcoal); orphans: 4; widows: 4; }}

/* Body paragraph explicit Lora 450 */
p {{ font-family: {SERIF}; font-weight: 450; }}

.path {{ width: 100%; height: 1.5px; background: var(--brass); opacity: 0.38; margin: 6px 0; }}
.path-strong {{ width: 100%; height: 1.5px; background: var(--brass); opacity: 0.62; margin: 0 0 18px; }}

/* ============ COVER DAILY ============ */
.cover-daily {{ background: var(--prussian-700); padding: 0 20mm 28px; page-break-after: avoid; }}
.cover-daily .top-accent {{ height: 4px; background: var(--brass); opacity: 0.75; margin-bottom: 28px; }}
.cover-daily .brand-row {{
  font-family: {SANS}; font-size: 7pt; font-weight: 600; letter-spacing: 0.28em;
  text-transform: uppercase; color: var(--brass-300); margin-bottom: 14px;
  display: flex; align-items: center; gap: 10px;
}}
.cover-daily .brand-row::after {{ content: ''; flex: 1; height: 1px; background: rgba(181,166,66,0.22); }}
.cover-daily h1 {{ font-family: {SERIF}; font-size: 24pt; font-weight: 700; color: var(--ivory); line-height: 1.15; }}

.content {{ padding: 20px 20mm 0; }}

/* ============ STAT BAR ============ */
.stat-bar {{ display: flex; gap: 10px; margin: 0 0 22px; align-items: stretch; }}
.stat-card {{
  flex: 1; background: var(--prussian-50); border-radius: 6px;
  padding: 14px 16px 16px; border-top: 3px solid var(--brass);
  display: flex; flex-direction: column; justify-content: flex-start;
  position: relative; overflow: hidden;
}}
.stat-card.neg-card {{ border-top-color: var(--negative); background: var(--negative-bg); }}
.stat-card.pos-card {{ border-top-color: var(--positive); background: var(--positive-bg); }}
.stat-label {{
  font-family: {SANS}; font-size: 6.5pt; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-secondary);
  line-height: 1.4; margin-bottom: 12px; min-height: 18px;
}}
.stat-value-wrap {{ display: flex; align-items: baseline; gap: 4px; }}
.stat-value {{
  font-family: {MONO}; font-size: 22pt; font-weight: 700;
  color: var(--prussian); line-height: 1; letter-spacing: -0.02em;
}}
.stat-card.neg-card .stat-value {{ color: var(--negative); }}
.stat-card.pos-card .stat-value {{ color: var(--positive); }}
.stat-unit {{
  font-family: {MONO}; font-size: 13pt; font-weight: 500;
  color: inherit; opacity: 0.55; margin-left: 1px;
}}
.stat-context {{
  font-family: {SANS}; font-size: 6.5pt; font-weight: 500;
  color: var(--text-secondary); margin-top: 6px; letter-spacing: 0.04em;
}}

/* ============ EXEC SUMMARY ============ */
.exec-summary {{ background: var(--prussian); border-radius: 6px; padding: 16px 20px; margin: 0 0 18px; page-break-inside: avoid; }}
.exec-label {{ font-family: {SANS}; font-size: 8.5pt; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--brass-300); margin-bottom: 12px; }}
.exec-summary ul {{ margin: 0; padding-left: 20px; }}
.exec-summary li {{ font-family: {SANS}; font-size: 9pt; line-height: 1.6; color: var(--ivory); margin-bottom: 6px; }}
.exec-summary li::marker {{ color: var(--brass); }}
.exec-summary li:last-child {{ margin-bottom: 0; }}
.exec-summary li strong, .exec-summary li .t {{ color: var(--brass-300); font-weight: 700; }}

/* ============ SECTION HEADERS ============ */
.section-header {{ display: flex; align-items: baseline; gap: 11px; margin: 26px 0 6px; page-break-after: avoid; }}
.section-num {{ font-family: {MONO}; font-size: 11pt; font-weight: 700; color: var(--brass); flex-shrink: 0; }}
.section-title {{ font-family: {SERIF}; font-size: 15pt; font-weight: 700; color: var(--prussian); line-height: 1.2; }}

h3 {{ font-family: {SANS}; font-size: 9pt; font-weight: 700; color: var(--charcoal); margin: 16px 0 6px; text-transform: uppercase; letter-spacing: 0.06em; page-break-after: avoid; }}

p {{ margin-bottom: 8px; text-align: justify; font-size: 9.5pt; }}

mark {{ background: rgba(181,166,66,0.16); border-bottom: 1.5px solid var(--brass); padding: 0 3px 1px; border-radius: 2px; color: inherit; font-weight: 600; }}
.t {{ font-weight: 700; color: var(--prussian); }}
strong {{ font-weight: 700; }}

/* ============ TABLES ============ */
table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 8px 0 14px; page-break-inside: avoid; }}
thead tr {{ background: var(--prussian); color: var(--ivory); }}
thead th:first-child {{ border-radius: 6px 0 0 0; }}
thead th:last-child {{ border-radius: 0 6px 0 0; }}
thead th {{ font-family: {SANS}; font-weight: 600; padding: 8px 10px; text-align: left; font-size: 7.5pt; letter-spacing: 0.05em; text-transform: uppercase; }}
thead th.th-num {{ text-align: right; }}
tbody tr:nth-child(even) {{ background: var(--prussian-50); }}
tbody tr:nth-child(odd) {{ background: white; }}
tbody tr.spotlight {{ background: rgba(181,166,66,0.12); border-left: 3px solid var(--brass); }}
td {{ padding: 7px 10px; border-bottom: 1px solid rgba(74,111,165,0.10); font-family: {SANS}; font-size: 9pt; vertical-align: middle; }}

.ticker-badge {{ display: inline-block; background: var(--prussian-50); color: var(--prussian); font-family: {MONO}; font-size: 8pt; font-weight: 700; padding: 1px 7px; border-radius: 3px; border: 1px solid var(--prussian-100); white-space: nowrap; }}
.num {{ font-family: {MONO}; font-size: 10pt; font-weight: 600; color: var(--ink); text-align: right; }}
.pos {{ color: var(--positive); font-weight: 700; font-family: {MONO}; font-size: 10pt; text-align: right; }}
.neg {{ color: var(--negative); font-weight: 700; font-family: {MONO}; font-size: 10pt; text-align: right; }}
.sig-pos {{ color: var(--positive); font-weight: 700; }}
.sig-neg {{ color: var(--negative); font-weight: 700; }}
.badge-new {{ display: inline-block; background: var(--brass); color: white; font-family: {SANS}; font-size: 6pt; font-weight: 700; padding: 1px 6px; border-radius: 999px; letter-spacing: 0.08em; text-transform: uppercase; vertical-align: middle; margin-left: 4px; white-space: nowrap; }}
.muted {{ color: var(--text-secondary); font-size: 8.5pt; }}

/* ============ CALLOUT 3 levels ============ */
.callout {{ border-left: 3px solid var(--brass); background: rgba(181,166,66,0.07); padding: 11px 15px; margin: 10px 0; border-radius: 0 4px 4px 0; page-break-inside: avoid; font-size: 9.5pt; line-height: 1.62; }}
.callout p {{ margin: 0; text-align: left; }}
.callout.warn {{ border-left-color: var(--bordeaux); background: var(--bordeaux-50); }}
.callout.key {{ border: none; border-radius: 6px; background: var(--prussian); padding: 20px 24px; margin: 18px 0; }}
.callout.key .key-label {{ font-family: {SANS}; font-size: 8.5pt; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--brass-300); margin-bottom: 10px; }}
.callout.key p {{ font-family: {SANS}; font-size: 10pt; color: var(--ivory); line-height: 1.65; margin: 0; text-align: left; }}
.callout.key strong {{ color: var(--brass-300); font-weight: 700; }}

/* ============ DISCLAIMER CARD ============ */
.disclaimer-card {{ margin-top: 24px; background: var(--prussian-50); border-radius: 6px; padding: 16px 20px; border-top: 3px solid var(--brass); page-break-before: avoid; }}
.disclaimer-label {{ font-family: {SANS}; font-size: 7.5pt; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--brass); margin-bottom: 8px; }}
.disclaimer-card p {{ font-size: 8.5pt; color: var(--charcoal); font-family: {SANS}; line-height: 1.6; margin: 0; }}
"""


def qc_check(html: str) -> list:
    """
    Quality check trước khi render. Trả về list các issues.
    Empty list = pass.
    """
    issues = []
    # Hard rule: no em-dash or en-dash
    dashes = re.findall('[\u2014\u2013]', html)
    if dashes:
        issues.append(f"FAIL: {len(dashes)} em/en-dash found. Replace all with '-'.")
    # DAILY phải có thông điệp chính
    if 'callout key' not in html:
        issues.append("FAIL: No .callout.key found (Thông điệp chính bắt buộc)")
    if 'disclaimer-card' not in html:
        issues.append("FAIL: No .disclaimer-card found")
    if html.count('ticker-badge') < 3:
        issues.append(f"WARN: Only {html.count('ticker-badge')} ticker-badge found (expected nhiều hơn)")
    # Cover khong duoc co date-display rieng (title da co ngay)
    if 'date-display' in html:
        issues.append("WARN: date-display found on cover - title đã chứa ngày, bỏ dòng date riêng")
    return issues


def render_pdf(html_content: str, output_path: str, strict: bool = True):
    """
    Render HTML thành PDF. Chạy QC trước.
    strict=True sẽ raise lỗi nếu QC fail.
    """
    from weasyprint import HTML

    issues = qc_check(html_content)
    fail_count = sum(1 for i in issues if i.startswith('FAIL'))
    for i in issues:
        print(f"  {i}")
    if fail_count > 0 and strict:
        raise RuntimeError(f"QC failed with {fail_count} hard issues")

    HTML(string=html_content).write_pdf(output_path, presentational_hints=True)
    print(f"  Rendered: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path


# ============================================================
# WAVE 7 DAILY REPORT ENHANCEMENTS
# ============================================================

DAILY_WAVE7_STYLES = r"""
/* ============ STAT CARDS UPGRADE (delta + sparkline) ============ */
.dr-stat-card-pro {
  background: #FAF7F0;
  padding: 4mm 5mm;
  border-top: 2px solid #B5A642;
  page-break-inside: avoid;
}
.dr-stat-card-pro .dr-sc-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 2mm;
}
.dr-stat-card-pro .dr-sc-row {
  display: grid; grid-template-columns: 1fr 28mm;
  gap: 4mm; align-items: center; margin-bottom: 2mm;
}
.dr-stat-card-pro .dr-sc-value-block {
  display: flex; align-items: baseline; gap: 3mm;
}
.dr-stat-card-pro .dr-sc-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 18pt; font-weight: 700;
  color: #003153; line-height: 1;
}
.dr-stat-card-pro .dr-sc-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 700;
}
.dr-stat-card-pro .dr-sc-delta.up { color: #2E7D52; }
.dr-stat-card-pro .dr-sc-delta.down { color: #C0392B; }
.dr-stat-card-pro .dr-sc-delta.flat { color: #6B6760; }
.dr-stat-card-pro .dr-sc-spark {
  display: block; width: 100%; height: 14mm;
}
.dr-stat-card-pro .dr-sc-context {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 8pt; font-weight: 450;
  font-style: italic; color: #6B6760;
  line-height: 1.4; margin-top: 1mm;
}

/* ============ MONEY FLOW ============ */
.dr-flow {
  margin: 5mm 0;
  page-break-inside: avoid;
}
.dr-flow-title {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 700;
  color: #003153; margin-bottom: 3mm;
}
.dr-flow-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 4mm;
}
.dr-flow-side {
  background: #FAF7F0; padding: 4mm 5mm;
}
.dr-flow-side.inflow { border-top: 2px solid #2E7D52; }
.dr-flow-side.outflow { border-top: 2px solid #C0392B; }
.dr-flow-side-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  margin-bottom: 2mm;
}
.dr-flow-side.inflow .dr-flow-side-label { color: #2E7D52; }
.dr-flow-side.outflow .dr-flow-side-label { color: #C0392B; }
.dr-flow-total {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 13pt; font-weight: 700;
  color: #003153; margin-bottom: 3mm;
}
.dr-flow-row {
  display: flex; justify-content: space-between;
  padding: 1.5mm 0; font-size: 8.5pt;
  border-bottom: 0.4px solid rgba(74,111,165,0.12);
}
.dr-flow-row:last-child { border-bottom: none; }
.dr-flow-name {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-weight: 600; color: #003153;
}
.dr-flow-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 600;
}
.dr-flow-side.inflow .dr-flow-value { color: #2E7D52; }
.dr-flow-side.outflow .dr-flow-value { color: #C0392B; }

/* ============ COMPARE ACROSS DAYS ============ */
.dr-compare {
  margin: 5mm 0;
  background: #FAF7F0; padding: 4mm 5mm;
  border-left: 3px solid #4A6FA5;
  page-break-inside: avoid;
}
.dr-compare-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #4A6FA5; margin-bottom: 3mm;
}
.dr-compare-grid {
  display: grid; grid-template-columns: 1fr 8mm 1fr 16mm;
  gap: 3mm; align-items: center;
  font-size: 9pt;
  padding: 2mm 0;
  border-bottom: 0.4px solid rgba(74,111,165,0.12);
}
.dr-compare-grid:last-child { border-bottom: none; }
.dr-compare-metric {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; color: #003153;
}
.dr-compare-day {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 600; color: #003153;
  text-align: right;
}
.dr-compare-day.muted { color: #6B6760; }
.dr-compare-arrow {
  font-family: 'JBM', 'JBMVN', monospace;
  text-align: center; color: #B5A642;
  font-weight: 700;
}
.dr-compare-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8.5pt; font-weight: 700;
  text-align: right;
}
.dr-compare-delta.up { color: #2E7D52; }
.dr-compare-delta.down { color: #C0392B; }
.dr-compare-delta.flat { color: #6B6760; }
"""


def stat_card_pro(
    label: str,
    value: str,
    delta: str = "",
    delta_type: str = "flat",
    spark_data: list = None,
    context: str = "",
) -> str:
    """
    Stat card upgrade với delta arrow + inline sparkline.

    Args:
        delta_type: 'up' | 'down' | 'flat'
        spark_data: list of values for inline sparkline (~10-15 points)
    """
    arrow = "▲" if delta_type == "up" else ("▼" if delta_type == "down" else "─")
    delta_html = ""
    if delta:
        delta_html = f'<div class="dr-sc-delta {delta_type}">{arrow} {escape_html(delta)}</div>'

    spark_svg = ""
    if spark_data and len(spark_data) >= 2:
        v_min = min(spark_data)
        v_max = max(spark_data)
        v_range = v_max - v_min if v_max != v_min else 1
        n = len(spark_data)
        svg_w = 100
        svg_h = 30
        pad = 2

        points = []
        for i, v in enumerate(spark_data):
            x = pad + (i / (n - 1)) * (svg_w - 2 * pad)
            y = pad + (svg_h - 2 * pad) - ((v - v_min) / v_range) * (svg_h - 2 * pad)
            points.append(f"{x:.1f},{y:.1f}")

        spark_color = "#2E7D52" if delta_type == "up" else ("#C0392B" if delta_type == "down" else "#4A6FA5")
        spark_svg = f"""
        <svg class="dr-sc-spark" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
          <polyline points="{' '.join(points)}" fill="none" stroke="{spark_color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """

    context_html = f'<div class="dr-sc-context">{escape_html(context)}</div>' if context else ""

    return f"""
<div class="dr-stat-card-pro">
  <div class="dr-sc-label">{escape_html(label)}</div>
  <div class="dr-sc-row">
    <div class="dr-sc-value-block">
      <div class="dr-sc-value">{escape_html(value)}</div>
      {delta_html}
    </div>
    {spark_svg}
  </div>
  {context_html}
</div>
"""


def money_flow(
    title: str,
    inflows: list,
    outflows: list,
    inflow_total: str = "",
    outflow_total: str = "",
) -> str:
    """
    Money flow: inflow vs outflow side-by-side.

    Args:
        inflows / outflows: list of {"name": str, "value": str}
    """
    def render_rows(items):
        rows = []
        for it in items:
            rows.append(f"""
            <div class="dr-flow-row">
              <span class="dr-flow-name">{escape_html(it.get("name", ""))}</span>
              <span class="dr-flow-value">{escape_html(it.get("value", ""))}</span>
            </div>
            """)
        return "".join(rows)

    return f"""
<div class="dr-flow">
  <div class="dr-flow-title">{escape_html(title)}</div>
  <div class="dr-flow-grid">
    <div class="dr-flow-side inflow">
      <div class="dr-flow-side-label">▲ DÒNG VÀO</div>
      <div class="dr-flow-total">{escape_html(inflow_total)}</div>
      {render_rows(inflows)}
    </div>
    <div class="dr-flow-side outflow">
      <div class="dr-flow-side-label">▼ DÒNG RA</div>
      <div class="dr-flow-total">{escape_html(outflow_total)}</div>
      {render_rows(outflows)}
    </div>
  </div>
</div>
"""


def daily_compare(
    title: str,
    today_label: str,
    yesterday_label: str,
    rows: list,
) -> str:
    """
    Compare across days table.

    Args:
        rows: list of {
            "metric": str,
            "today": str,
            "yesterday": str,
            "delta": str,
            "delta_type": "up"|"down"|"flat",
        }
    """
    rows_html = []
    for r in rows:
        dtype = r.get("delta_type", "flat")
        arrow = "↑" if dtype == "up" else ("↓" if dtype == "down" else "→")
        rows_html.append(f"""
        <div class="dr-compare-grid">
          <div class="dr-compare-metric">{escape_html(r.get("metric", ""))}</div>
          <div class="dr-compare-day muted">{escape_html(r.get("yesterday", ""))}</div>
          <div class="dr-compare-day">{escape_html(r.get("today", ""))}</div>
          <div class="dr-compare-delta {dtype}">{arrow} {escape_html(r.get("delta", ""))}</div>
        </div>
        """)

    header = f"""
    <div class="dr-compare-grid" style="border-bottom: 1px solid #4A6FA5; padding-bottom: 2mm; margin-bottom: 1mm;">
      <div style="font-family: 'Inter', 'InterVN', sans-serif; font-size: 7pt; font-weight: 700; letter-spacing: 0.12em; color: #6B6760; text-transform: uppercase;">Chỉ số</div>
      <div style="font-family: 'Inter', 'InterVN', sans-serif; font-size: 7pt; font-weight: 700; letter-spacing: 0.12em; color: #6B6760; text-align: right; text-transform: uppercase;">{escape_html(yesterday_label)}</div>
      <div style="font-family: 'Inter', 'InterVN', sans-serif; font-size: 7pt; font-weight: 700; letter-spacing: 0.12em; color: #003153; text-align: right; text-transform: uppercase;">{escape_html(today_label)}</div>
      <div style="font-family: 'Inter', 'InterVN', sans-serif; font-size: 7pt; font-weight: 700; letter-spacing: 0.12em; color: #B5A642; text-align: right; text-transform: uppercase;">Δ</div>
    </div>
    """

    return f"""
<div class="dr-compare">
  <div class="dr-compare-title">{escape_html(title)}</div>
  {header}
  {''.join(rows_html)}
</div>
"""


def escape_html(s):
    """Local escape helper."""
    from html import escape as _esc
    return _esc(str(s))


def build_full_css(date_str: str, fonts_dir: str = None) -> str:
    """Build CSS bao gồm core + Wave 7 enhancements."""
    return build_css(date_str=date_str, fonts_dir=fonts_dir) + DAILY_WAVE7_STYLES
