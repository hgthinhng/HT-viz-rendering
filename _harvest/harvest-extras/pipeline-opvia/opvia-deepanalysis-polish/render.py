"""
opvia_DeepAnalysis_polish.render
=================================
Module render PDF cho skill opvia-DeepAnalysis-polish.
CSS editorial premium - dành riêng cho bài phân tích sâu / xã luận của Opvia Academy.

Khác với daily report skill: layout 3-stage (cover → TOC → content),
typography editorial (10.5pt + line-height 1.78), drop cap dramatic (56pt floated),
pull quote 3 variants, callout 5 loại, header strip per-page, glossary support.

Usage:
    from render import build_css, render_pdf

    css = build_css(
        date_str='25/04/2026',
        short_title='Đề xuất sửa đổi Thông tư 22/2019',
    )
    render_pdf(html, '/path/to/output.pdf')
"""

import os
import re
import warnings

warnings.filterwarnings('ignore')


def get_fonts_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    fonts = os.path.join(here, 'fonts')
    if not os.path.isdir(fonts):
        raise RuntimeError(f"Fonts folder không tìm thấy: {fonts}")
    return fonts


def build_font_face(fonts_dir: str = None) -> str:
    F = fonts_dir or get_fonts_dir()
    # FONT MAPPING (Wave 1.7 - Lora + Plex Mono):
    # PFD/PFDVN aliases → Lora (heading + body serif)
    # JBM/JBMVN aliases → IBM Plex Mono (numbers, code)
    # Inter aliases unchanged (UI/labels/eyebrows)
    # Aliases preserved để không phải đổi 100+ references trong viz.py + render.py
    return f"""
@font-face {{ font-family: 'Inter'; font-weight: 400; src: url('file://{F}/inter-latin-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 500; src: url('file://{F}/inter-latin-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 600; src: url('file://{F}/inter-latin-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'Inter'; font-weight: 700; src: url('file://{F}/inter-latin-700.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 400; src: url('file://{F}/inter-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 500; src: url('file://{F}/inter-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 600; src: url('file://{F}/inter-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'InterVN'; font-weight: 700; src: url('file://{F}/inter-vn-700.woff2') format('woff2'); }}

/* JBM/JBMVN aliases → IBM Plex Mono (numbers, ticker badges) */
@font-face {{ font-family: 'JBM'; font-weight: 400; src: url('file://{F}/plex-mono-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 500; src: url('file://{F}/plex-mono-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 600; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBM'; font-weight: 700; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 400; src: url('file://{F}/plex-mono-vn-400.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 500; src: url('file://{F}/plex-mono-vn-500.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 600; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}
@font-face {{ font-family: 'JBMVN'; font-weight: 700; src: url('file://{F}/plex-mono-vn-600.woff2') format('woff2'); }}

/* PFD/PFDVN aliases → Lora (heading + body serif) */
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


# Font stacks
SANS = "'Inter', 'InterVN', sans-serif"
MONO = "'JBM', 'JBMVN', monospace"
SERIF = "'PFD', 'PFDVN', serif"


def build_css(date_str: str, short_title: str = "OPVIA RESEARCH", fonts_dir: str = None) -> str:
    """
    Sinh CSS editorial premium đầy đủ cho 1 bài deep analysis.

    date_str: "25/04/2026" sẽ chèn vào header strip + footer
    short_title: tiêu đề ngắn (UPPERCASE) cho header strip per-page,
                 ví dụ "ĐỀ XUẤT SỬA ĐỔI THÔNG TƯ 22"
    """
    font_face = build_font_face(fonts_dir)
    short_upper = short_title.upper()
    return f"""
{font_face}

:root {{
  --prussian: #003153; --prussian-50: #E8F2F9; --prussian-100: #B3D1E6; --prussian-700: #001A2E; --prussian-900: #000d18;
  --brass: #B5A642; --brass-300: #CCC46B; --brass-100: #E8E2B8;
  --slate: #4A6FA5; --slate-light: #7B96BD;
  --ivory: #F5F1E8; --ivory-deep: #EDE6D3; --paper: #FAF7F0;
  --charcoal: #2B2B2B; --ink: #1A1A1A;
  --text-secondary: #6B6760; --text-muted: #9A9688;
  --bordeaux: #722F37; --bordeaux-50: #F5ECED;
  --positive: #2E7D52; --positive-bg: #EDF7F1;
  --negative: #C0392B; --negative-bg: #FBEEEC;
  --rule-soft: rgba(181,166,66,0.30);
  --rule-hard: rgba(181,166,66,0.62);
}}

/* ============ PAGE RULES ============ */
@page {{
  size: A4;
  margin: 18mm 0 14mm 0;
  @top-center {{
    content: "OPVIA RESEARCH  ·  {short_upper}  ·  {date_str}";
    font-family: {SANS}; font-size: 6.5pt; font-weight: 600;
    letter-spacing: 0.12em; color: var(--text-muted);
    padding-bottom: 5px; padding-top: 5mm;
    border-bottom: 0.6px solid var(--rule-soft);
    width: calc(100% - 44mm); margin: 0 22mm;
  }}
  @bottom-left {{
    content: "OPVIA RESEARCH  ·  {date_str}";
    font-family: {SANS}; font-size: 7pt; color: var(--text-muted);
    border-top: 1px solid var(--rule-soft);
    padding-top: 4px; padding-left: 22mm; width: 50%;
  }}
  @bottom-right {{
    content: counter(page);
    font-family: {MONO}; font-size: 7pt; color: var(--text-muted);
    border-top: 1px solid var(--rule-soft);
    padding-top: 4px; padding-right: 22mm; text-align: right; width: 50%;
  }}
}}
@page :first {{
  margin: 0;
  background-color: #000d18;
  @top-center {{ content: ""; border: none; }}
  @bottom-left {{ content: ""; border: none; }}
  @bottom-right {{ content: ""; border: none; }}
}}
@page toc {{
  margin: 18mm 0 14mm 0;
  @top-center {{ content: ""; border: none; }}
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: {SERIF}; font-size: 10.5pt; line-height: 1.7;
  font-weight: 450;
  color: var(--charcoal); orphans: 3; widows: 3;
  hyphens: manual;
  background: var(--paper);
}}

/* Explicit body paragraph - Lora 450 cho long-form readability */
p {{
  font-family: {SERIF}; font-weight: 450;
}}

/* ============ COVER (page 1, full bleed) - hero landing ============ */
.cover-deep {{
  background: var(--prussian-900);
  height: 297mm; width: 100%;
  padding: 24mm 24mm 18mm 24mm;
  display: flex; flex-direction: column;
  page-break-after: always; position: relative;
  color: var(--ivory);
}}
/* MAGAZINE MASTHEAD - brand center, info row 2-cột */
.cover-masthead {{
  margin-bottom: 14mm;
}}
.masthead-rule-top {{
  height: 1.5px; background: var(--brass);
  width: 56mm; margin: 0 auto 5mm;
}}
.masthead-brand {{
  font-family: {SERIF}; font-size: 14pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--brass); text-align: center;
  margin-bottom: 5mm;
}}
.masthead-rule-mid {{
  height: 0.6px; background: rgba(181,166,66,0.45);
  width: 100%; margin-bottom: 4mm;
}}
.masthead-meta {{
  display: flex; justify-content: space-between; align-items: baseline;
}}
.masthead-meta .meta-left {{
  font-family: {SANS}; font-size: 8.5pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass-300);
}}
.masthead-meta .meta-right {{
  font-family: {MONO}; font-size: 8pt; font-weight: 500;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: rgba(245,241,232,0.72);
}}
.cover-deep h1 {{
  font-family: {SERIF}; font-size: 38pt; font-weight: 700;
  color: var(--ivory); line-height: 1.04; letter-spacing: -0.01em;
  margin-bottom: 6mm; max-width: 95%;
}}
.cover-deep .cover-subtitle {{
  font-family: {SERIF}; font-style: italic; font-weight: 400;
  font-size: 13pt; line-height: 1.4;
  color: var(--brass-300); margin-bottom: 8mm; max-width: 80%;
}}
.cover-deep .cover-dek {{
  font-family: {SANS}; font-size: 10pt; font-weight: 400;
  line-height: 1.62; color: rgba(245,241,232,0.78);
  max-width: 78%; margin-bottom: 8mm;
  border-left: 2px solid var(--brass); padding-left: 14px;
}}

/* Cover hero stat block - 1 con số signature */
.cover-deep .cover-hero-stat {{
  display: flex; align-items: center; gap: 16px;
  margin-bottom: 6mm; padding-top: 4mm;
  border-top: 0.6px solid rgba(181,166,66,0.35);
}}
.cover-deep .cover-hero-num {{
  font-family: {MONO}; font-size: 44pt; font-weight: 700;
  color: var(--brass); line-height: 1;
  letter-spacing: -0.03em;
  flex-shrink: 0;
}}
.cover-deep .cover-hero-cap {{ flex: 1; }}
.cover-deep .cover-hero-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass-300); margin-bottom: 4px;
}}
.cover-deep .cover-hero-desc {{
  font-family: {SANS}; font-size: 10pt; font-weight: 400;
  line-height: 1.5; color: rgba(245,241,232,0.85);
}}

/* Cover key takeaways - 3 bullets đề mục chính */
.cover-deep .cover-takeaways {{
  margin-bottom: auto; padding-top: 5mm;
  border-top: 0.6px solid rgba(181,166,66,0.35);
}}
.cover-deep .cover-takeaways-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 4mm;
}}
.cover-deep .cover-takeaways ul {{ list-style: none; padding: 0; margin: 0; }}
.cover-deep .cover-takeaways li {{
  font-family: {SANS}; font-size: 9.5pt; line-height: 1.5;
  color: rgba(245,241,232,0.88); margin-bottom: 7px;
  padding-left: 16px; position: relative;
}}
.cover-deep .cover-takeaways li::before {{
  content: '▸'; color: var(--brass); position: absolute;
  left: 0; top: 0; font-size: 9pt;
}}
.cover-deep .cover-takeaways li strong {{
  color: var(--brass-300); font-weight: 700;
}}

.cover-deep .cover-bottom-rule {{
  height: 0.6px; background: rgba(181,166,66,0.4); margin: 8mm 0 6mm;
}}
.cover-deep .cover-meta-strip {{
  display: flex; justify-content: space-between; align-items: flex-end;
  font-family: {SANS}; font-size: 7.5pt; letter-spacing: 0.12em;
  text-transform: uppercase; color: rgba(245,241,232,0.55);
}}
.cover-deep .cover-meta-strip strong {{
  color: var(--brass-300); font-weight: 700; display: block;
  font-size: 8.5pt; letter-spacing: 0.12em; margin-bottom: 2px;
}}
.cover-deep .cover-meta-strip .meta-block {{ flex: 1; }}
.cover-deep .cover-meta-strip .meta-block:nth-child(2) {{ text-align: center; }}
.cover-deep .cover-meta-strip .meta-block:nth-child(3) {{ text-align: right; }}

/* ============ TOC (page 2) - compressed + alert inline ============ */
.toc-page {{ page: toc; padding: 0 24mm; page-break-after: always; }}
.toc-eyebrow {{
  font-family: {SANS}; font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 3mm;
}}
.toc-title-main {{
  font-family: {SERIF}; font-size: 20pt; font-weight: 700;
  color: var(--prussian); line-height: 1.08; margin-bottom: 3mm;
}}
.toc-intro {{
  font-family: {SERIF}; font-style: italic; font-size: 10pt;
  line-height: 1.5; color: var(--slate); margin-bottom: 4mm;
  max-width: 85%;
}}
.toc-rule {{ height: 1.5px; background: var(--brass); width: 100%; margin-bottom: 3mm; }}

.toc-list {{ display: block; }}
.toc-entry {{
  display: grid;
  grid-template-columns: 22mm 1fr 14mm;
  gap: 12px;
  padding: 3mm 0 3mm;
  border-bottom: 0.6px solid var(--rule-soft);
  page-break-inside: avoid;
}}
.toc-entry:last-child {{ border-bottom: none; }}
.toc-num {{
  font-family: {MONO}; font-size: 18pt; font-weight: 700;
  color: var(--brass); line-height: 0.95;
  letter-spacing: -0.02em;
}}
.toc-body {{ display: flex; flex-direction: column; }}
.toc-name {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--text-secondary); margin-bottom: 2px;
}}
.toc-headline {{
  font-family: {SERIF}; font-size: 11.5pt; font-weight: 700;
  color: var(--prussian); line-height: 1.18; margin-bottom: 2px;
}}
.toc-hook {{
  font-family: {SERIF}; font-style: italic; font-size: 9pt;
  line-height: 1.38; color: var(--charcoal); opacity: 0.78;
}}
.toc-page-num {{
  font-family: {MONO}; font-size: 10pt; font-weight: 600;
  color: var(--prussian); text-align: right;
  align-self: flex-start; padding-top: 4px;
}}

/* Alert box inline trên TOC page (cuối trang) */
.toc-alert {{
  margin-top: 6mm;
  background: var(--bordeaux-50); border-left: 3px solid var(--bordeaux);
  padding: 11px 16px;
  font-family: {SANS}; font-size: 8.5pt; line-height: 1.55;
  color: var(--charcoal); border-radius: 0 4px 4px 0;
  page-break-inside: avoid;
}}
.toc-alert strong {{ color: var(--bordeaux); font-weight: 700; }}
.toc-alert .toc-alert-label {{
  display: block; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--bordeaux); margin-bottom: 4px;
}}

/* ============ CONTENT PAGES ============ */
.content {{ padding: 0 24mm; }}

/* Critical lưu ý đầu bài */
.alert-banner {{
  background: var(--bordeaux-50); border-left: 3px solid var(--bordeaux);
  padding: 14px 18px; margin: 0 0 18mm;
  font-family: {SANS}; font-size: 9pt; line-height: 1.6;
  color: var(--charcoal); border-radius: 0 4px 4px 0;
  page-break-inside: avoid;
}}
.alert-banner strong {{ color: var(--bordeaux); font-weight: 700; }}

/* SECTION OPENER - mỗi Phần bắt đầu trang mới */
.section-opener {{
  margin: 0 0 6mm; padding-top: 2mm;
  page-break-before: always;
  page-break-after: avoid;
  page-break-inside: avoid;
  position: relative;
}}
.section-opener.no-break {{ page-break-before: auto; }}
.section-opener .section-num-large {{
  font-family: {MONO}; font-size: 8.5pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 3mm;
  display: flex; align-items: center; gap: 12px;
}}
.section-opener .section-num-large::after {{
  content: ''; flex: 1; height: 0.6px;
  background: var(--rule-soft);
}}
/* Roman numeral background - decorative, mờ phía sau */
.section-opener .section-roman {{
  position: absolute; top: 8mm; right: 0;
  font-family: {SERIF}; font-size: 76pt; font-weight: 700;
  color: var(--brass); opacity: 0.10;
  line-height: 0.85; letter-spacing: -0.04em;
  z-index: 0; pointer-events: none;
}}
.section-opener .section-title-large {{
  font-family: {SERIF}; font-size: 20pt; font-weight: 700;
  color: var(--prussian); line-height: 1.15;
  letter-spacing: -0.005em; margin-bottom: 3mm;
  max-width: 90%; position: relative; z-index: 1;
}}
.section-opener .section-dek {{
  font-family: {SANS}; font-size: 10pt; font-weight: 400;
  line-height: 1.55; color: var(--slate); max-width: 80%;
  position: relative; z-index: 1;
}}
.section-opener .section-rule-double {{
  margin-top: 4mm;
  border-top: 1px solid var(--brass);
  border-bottom: 0.4px solid rgba(181,166,66,0.5);
  height: 2.5px;
}}

/* End-of-section ornament - ĐÃ BỎ, không dùng nữa */

/* BODY paragraphs */
p {{ margin-bottom: 12px; text-align: justify; font-size: 10.5pt; }}
p.lede {{ font-size: 11.5pt; line-height: 1.7; color: var(--charcoal); margin-bottom: 14px; }}

/* PSEUDO DROP CAP - chỉ tăng size + brass color, KHÔNG float */
p.dropcap-deep {{ margin-bottom: 12px; }}
p.dropcap-deep .dc {{
  font-family: {SERIF}; font-size: 1.7em; font-weight: 700;
  color: var(--brass); line-height: 1;
  margin-right: 1px;
  vertical-align: -2px;
}}

mark {{
  background: rgba(181,166,66,0.16); border-bottom: 1.5px solid var(--brass);
  padding: 0 3px 1px; border-radius: 2px; color: inherit; font-weight: 600;
}}
.t {{ font-weight: 700; color: var(--prussian); }}
strong {{ font-weight: 700; }}

/* H3 subheading - cleaner, KHÔNG uppercase letterspaced */
h3 {{
  font-family: {SANS}; font-size: 10.5pt; font-weight: 700;
  color: var(--prussian); margin: 14px 0 6px;
  letter-spacing: -0.005em;
  page-break-after: avoid;
  border-bottom: 0.6px solid var(--rule-soft); padding-bottom: 3px;
  position: relative;
}}
h3::before {{
  content: ""; display: inline-block;
  width: 8px; height: 8px;
  background: var(--brass); margin-right: 7px;
  vertical-align: 1px;
}}

/* H4 micro-subheading */
h4 {{
  font-family: {SERIF}; font-style: italic; font-size: 11.5pt;
  font-weight: 600; color: var(--prussian); margin: 11px 0 5px;
  page-break-after: avoid;
}}

/* ============ TABLES editorial ============ */
table {{
  width: 100%; border-collapse: separate; border-spacing: 0;
  margin: 10px 0 14px; page-break-inside: avoid;
  background: transparent;
}}
thead tr {{ background: transparent; color: var(--prussian); }}
thead th {{
  font-family: {SANS}; font-weight: 700; padding: 7px 10px;
  text-align: left; font-size: 7.5pt; letter-spacing: 0.10em;
  text-transform: uppercase; color: var(--prussian);
  border-bottom: 1.5px solid var(--brass);
}}
thead th.th-num {{ text-align: right; }}
tbody tr {{ background: transparent; }}
tbody tr.spotlight {{ background: rgba(181,166,66,0.10); }}
tbody tr.spotlight td:first-child {{ box-shadow: inset 3px 0 0 var(--brass); }}
td {{
  padding: 6px 10px; border-bottom: 0.5px solid rgba(74,111,165,0.12);
  font-family: {SANS}; font-size: 9.5pt; vertical-align: middle; line-height: 1.45;
}}
tbody tr:last-child td {{ border-bottom: none; }}
td:first-child {{ font-weight: 600; color: var(--prussian); }}

/* Comparison table - 2 cột vs nhau */
table.compare thead th:nth-child(2),
table.compare thead th:nth-child(3) {{ text-align: center; width: 32%; }}
table.compare tbody td:nth-child(2),
table.compare tbody td:nth-child(3) {{ text-align: center; }}
table.compare .col-winner {{ background: rgba(181,166,66,0.10); font-weight: 700; }}

.ticker-badge {{
  display: inline-block; background: var(--prussian-50); color: var(--prussian);
  font-family: {MONO}; font-size: 8pt; font-weight: 700;
  padding: 1px 7px; border-radius: 3px;
  border: 1px solid var(--prussian-100); white-space: nowrap;
}}
.num {{ font-family: {MONO}; font-size: 10pt; font-weight: 600; color: var(--ink); text-align: right; }}
.pos {{ color: var(--positive); font-weight: 700; font-family: {MONO}; font-size: 10pt; text-align: right; }}
.neg {{ color: var(--negative); font-weight: 700; font-family: {MONO}; font-size: 10pt; text-align: right; }}
.sig-pos {{ color: var(--positive); font-weight: 700; }}
.sig-neg {{ color: var(--negative); font-weight: 700; }}
.muted {{ color: var(--text-muted); font-size: 9pt; }}

/* ============ PULL QUOTES - 2 variants ============ */
blockquote {{
  border-top: 1.5px solid var(--brass); border-bottom: 1.5px solid var(--brass);
  margin: 7mm 8mm; padding: 5mm 0; text-align: center;
  page-break-inside: avoid;
  page-break-before: avoid;
}}
blockquote p {{
  font-family: {SERIF}; font-style: italic; font-size: 13pt;
  color: var(--prussian); line-height: 1.5; margin: 0; text-align: center;
}}

/* Hero pull quote - full width prussian bg */
blockquote.hero {{
  border: none; background: var(--prussian);
  margin: 8mm 0; padding: 11mm 12mm 9mm 18mm; text-align: left;
  border-radius: 4px; position: relative;
  box-shadow: 0 2px 6px rgba(0,49,83,0.18);
}}
blockquote.hero p {{
  color: var(--ivory); font-size: 18pt; line-height: 1.45;
  text-align: left; font-style: italic;
  margin: 0;
}}
blockquote.hero p::before {{
  content: '"';
  font-family: {SERIF}; font-size: 60pt;
  color: var(--brass); line-height: 1;
  position: absolute;
  left: 7mm; top: 4mm;
  font-style: normal;
}}
blockquote.hero cite {{
  display: block; margin-top: 5mm; font-family: {SANS};
  font-size: 8pt; font-style: normal; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--brass-300);
}}

/* ============ CALLOUT - 5 levels ============ */
.callout {{
  border-left: 3px solid var(--brass); background: rgba(181,166,66,0.07);
  padding: 12px 16px; margin: 12px 0; border-radius: 0 4px 4px 0;
  page-break-inside: avoid; font-size: 10pt; line-height: 1.65;
}}
.callout p {{ margin: 0; text-align: left; font-size: 10pt; }}
.callout p + p {{ margin-top: 8px; }}

.callout.warn {{ border-left-color: var(--bordeaux); background: var(--bordeaux-50); }}
.callout.warn strong {{ color: var(--bordeaux); }}

.callout.formula {{
  border: none; background: var(--ivory-deep);
  border-top: 1px solid var(--brass); border-bottom: 1px solid var(--brass);
  text-align: center; padding: 10mm 8mm; margin: 7mm 12mm;
  border-radius: 0;
  box-shadow: 0 1px 3px rgba(0,49,83,0.06);
}}
.callout.formula p {{
  font-family: {SERIF}; font-style: italic; font-size: 13pt;
  color: var(--prussian); text-align: center; line-height: 1.5;
}}
.callout.formula .formula-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 6px;
}}

/* ---------- FORMULA FRACTION (proper math display - table layout) ---------- */
.formula-fraction {{
  background: var(--ivory-deep);
  border-top: 1px solid var(--brass);
  border-bottom: 1px solid var(--brass);
  padding: 10mm 8mm 9mm 8mm;
  margin: 7mm 0;
  text-align: center;
  page-break-inside: avoid;
}}
.formula-fraction .ff-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 6mm;
}}
.formula-fraction .ff-equation {{
  display: table; margin: 0 auto;
  border-collapse: collapse;
}}
.formula-fraction .ff-cell {{
  display: table-cell; vertical-align: middle;
  padding: 0 4mm;
}}
.formula-fraction .ff-var {{
  font-family: {MONO}; font-size: 16pt; font-weight: 700;
  color: var(--prussian); letter-spacing: 0.02em;
}}
.formula-fraction .ff-eq {{
  font-family: {MONO}; font-size: 18pt; font-weight: 600;
  color: var(--brass);
}}
.formula-fraction .ff-result {{
  font-family: {MONO}; font-size: 16pt; font-weight: 700;
  color: var(--prussian); letter-spacing: 0;
}}
.formula-fraction .ff-frac {{
  display: table-cell; vertical-align: middle;
  padding: 0 4mm;
  min-width: 72mm;
}}
.formula-fraction .ff-num {{
  display: block; padding: 0 4mm 2.5mm 4mm;
  border-bottom: 1.2px solid var(--prussian);
  font-family: {SERIF}; font-size: 11pt;
  font-style: italic; color: var(--prussian);
  line-height: 1.3; text-align: center;
}}
.formula-fraction .ff-den {{
  display: block; padding: 2.5mm 4mm 0 4mm;
  font-family: {SERIF}; font-size: 11pt;
  font-style: italic; color: var(--prussian);
  line-height: 1.3; text-align: center;
}}
.formula-fraction .ff-component-key {{
  font-family: {MONO}; font-size: 11pt;
  font-weight: 700; font-style: normal;
  color: var(--brass); letter-spacing: 0.04em;
  margin-right: 2mm;
}}
.formula-fraction .ff-condition {{
  margin-top: 6mm;
  font-family: {SERIF}; font-size: 9pt;
  font-style: italic; color: var(--slate);
  line-height: 1.5;
  max-width: 130mm; margin-left: auto; margin-right: auto;
}}

.callout.contrast {{
  background: transparent; border: none; padding: 0; margin: 12px 0;
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
}}
.callout.contrast .side {{
  padding: 12px 14px; border-radius: 4px;
  font-size: 9.5pt; line-height: 1.55;
}}
.callout.contrast .side-a {{
  background: var(--positive-bg); border-left: 3px solid var(--positive);
}}
.callout.contrast .side-b {{
  background: var(--negative-bg); border-left: 3px solid var(--negative);
}}
.callout.contrast .side-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase;
  margin-bottom: 6px;
}}
.callout.contrast .side-a .side-label {{ color: var(--positive); }}
.callout.contrast .side-b .side-label {{ color: var(--negative); }}

.callout.key {{
  border: none; border-radius: 4px; background: var(--prussian);
  padding: 8mm 10mm; margin: 8mm 0;
  box-shadow: 0 2px 6px rgba(0,49,83,0.18);
}}
.callout.key .key-label {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass-300); margin-bottom: 8px;
}}
.callout.key p {{
  font-family: {SERIF}; font-style: italic; font-size: 13pt;
  color: var(--ivory); line-height: 1.55; margin: 0; text-align: left;
}}
.callout.key p + p {{ margin-top: 10px; }}
.callout.key strong {{ color: var(--brass-300); font-weight: 700; font-style: normal; }}

/* ============ HERO STAT (huge number callout) ============ */
.hero-stat {{
  page-break-inside: avoid; margin: 6mm 0;
  display: grid; grid-template-columns: auto 1fr; gap: 18px;
  align-items: center;
}}
.hero-stat-number {{
  font-family: {MONO}; font-size: 42pt; font-weight: 700;
  color: var(--brass); line-height: 0.9; letter-spacing: -0.03em;
}}
.hero-stat-caption {{ display: flex; flex-direction: column; }}
.hero-stat-label {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--text-secondary); margin-bottom: 5px;
}}
.hero-stat-desc {{
  font-family: {SANS}; font-size: 10.5pt; font-weight: 400;
  color: var(--prussian); line-height: 1.45;
}}

/* ============ GLOSSARY ============ */
.glossary-section {{ margin-top: 12mm; page-break-before: auto; }}
.glossary-eyebrow {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 3mm;
}}
.glossary-title {{
  font-family: {SERIF}; font-size: 22pt; font-weight: 700;
  color: var(--prussian); margin-bottom: 4mm;
}}
.glossary-intro {{
  font-family: {SANS}; font-size: 10pt; font-weight: 400;
  color: var(--slate); margin-bottom: 6mm; max-width: 85%;
  line-height: 1.55;
}}
/* 2-column layout cho glossary groups */
.glossary-columns {{
  column-count: 2;
  column-gap: 10mm;
  column-rule: 0.4px solid var(--rule-soft);
}}
.glossary-group {{
  margin-bottom: 6mm;
  break-inside: avoid;
  page-break-inside: avoid;
}}
.glossary-group-label {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--prussian); margin-bottom: 3mm;
  border-bottom: 0.6px solid var(--rule-soft); padding-bottom: 3px;
}}
.glossary-term-row {{
  display: block;
  padding: 4px 0;
  border-bottom: 0.4px solid rgba(74,111,165,0.08);
  break-inside: avoid;
  page-break-inside: avoid;
}}
.glossary-term {{
  font-family: {SANS}; font-size: 9pt; font-weight: 700;
  color: var(--prussian);
  display: block;
  margin-bottom: 2px;
}}
.glossary-def {{
  font-family: {SANS}; font-size: 8.5pt; line-height: 1.5;
  color: var(--charcoal);
  display: block;
}}
.glossary-def .note {{
  display: block; margin-top: 2px; font-size: 8pt;
  color: var(--text-secondary); font-style: italic;
}}

/* ============ CONCLUSION BLOCK ============ */
.conclusion-block {{
  margin: 10mm 0 6mm; padding: 8mm 10mm;
  background: var(--ivory);
  border-top: 2px solid var(--brass); border-bottom: 2px solid var(--brass);
  page-break-inside: avoid;
  box-shadow: 0 2px 4px rgba(0,49,83,0.08);
}}
.conclusion-eyebrow {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 4mm;
}}
.conclusion-block p {{
  font-family: {SERIF}; font-style: italic; font-size: 13pt;
  line-height: 1.6; color: var(--prussian); text-align: left;
  margin-bottom: 10px;
}}
.conclusion-block strong {{ color: var(--brass); font-style: normal; font-weight: 700; }}

/* ============ CONTACT/DISCLAIMER PAGE - tách trang riêng ============ */
.contact-page {{
  page-break-before: always;
  margin-top: 0; padding-top: 4mm;
}}
.contact-eyebrow {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 3mm;
}}
.contact-title {{
  font-family: {SERIF}; font-size: 28pt; font-weight: 700;
  color: var(--prussian); line-height: 1.1;
  margin-bottom: 4mm; letter-spacing: -0.005em;
}}
.contact-intro {{
  font-family: {SANS}; font-size: 10pt; font-weight: 400;
  color: var(--slate); line-height: 1.55;
  max-width: 90%; margin-bottom: 8mm;
}}

/* CTA card - prussian bg highlighted */
.contact-cta {{
  background: var(--prussian); color: var(--ivory);
  padding: 9mm 10mm; margin-bottom: 8mm;
  border-radius: 4px;
  border-top: 3px solid var(--brass);
  box-shadow: 0 3px 8px rgba(0,49,83,0.18);
  page-break-inside: avoid;
}}
.cta-eyebrow {{
  font-family: {SANS}; font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--brass-300); margin-bottom: 3mm;
}}
.cta-title {{
  font-family: {SERIF}; font-size: 17pt; font-weight: 700;
  color: var(--ivory); line-height: 1.2; margin-bottom: 3mm;
}}
.cta-text {{
  font-family: {SANS}; font-size: 10pt; line-height: 1.55;
  color: rgba(245,241,232,0.85); margin-bottom: 6mm;
  max-width: 92%;
}}
.cta-grid {{
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 6mm; padding-top: 4mm;
  border-top: 0.6px solid rgba(181,166,66,0.4);
}}
.cta-item {{
  display: flex; flex-direction: column;
}}
.cta-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass-300); margin-bottom: 4px;
}}
.cta-value {{
  font-family: {MONO}; font-size: 9pt; font-weight: 500;
  color: var(--ivory); line-height: 1.4;
}}

/* Sources & Disclaimer sections - paper bg */
.contact-section {{
  background: var(--ivory); padding: 6mm 7mm;
  margin-bottom: 6mm;
  border-top: 1.5px solid var(--brass);
  page-break-inside: avoid;
}}
.contact-section .section-eyebrow {{
  font-family: {SANS}; font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 3mm;
}}
.contact-section p {{
  font-family: {SANS}; font-size: 9.5pt; line-height: 1.62;
  color: var(--charcoal); text-align: left;
  margin-bottom: 0;
}}
.contact-section p strong {{ color: var(--bordeaux); font-weight: 700; }}

/* Footer signature */
.contact-signature {{
  margin-top: 10mm; padding-top: 5mm;
  border-top: 0.6px solid var(--rule-soft);
  font-family: {SANS}; font-size: 8pt; font-weight: 600;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--text-secondary); text-align: center;
}}

/* Legacy disclaimer-card vẫn giữ để backward compat */
.disclaimer-card {{
  margin-top: 8mm; padding: 6mm 7mm;
  background: var(--paper); border-top: 2px solid var(--brass);
  border-radius: 0 0 4px 4px; page-break-inside: avoid;
}}
.disclaimer-label {{
  font-family: {SANS}; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--brass); margin-bottom: 6px;
}}
.disclaimer-card p {{
  font-size: 8.5pt; color: var(--text-secondary);
  font-family: {SANS}; line-height: 1.6; margin: 0; text-align: left;
}}
.disclaimer-card strong {{ color: var(--charcoal); font-weight: 600; }}
"""


def qc_check(html: str) -> list:
    """
    Quality check trước khi render. Trả về list các issues.
    """
    issues = []
    # Hard rule: no em-dash or en-dash
    dashes = re.findall('[\u2014\u2013]', html)
    if dashes:
        issues.append(f"FAIL: {len(dashes)} em/en-dash found. Replace all with '-'.")
    # Editorial phải có cover-deep (single page no flex bug)
    if 'cover-deep' not in html:
        issues.append("FAIL: No .cover-deep found (cover bắt buộc cho deep analysis)")
    # Phải có TOC
    if 'toc-page' not in html:
        issues.append("WARN: No .toc-page found (Table of Contents recommended)")
    # Phải có ít nhất 1 section opener
    if 'section-opener' not in html:
        issues.append("WARN: No .section-opener found")
    # Phải có conclusion hoặc callout key
    if 'conclusion-block' not in html and 'callout key' not in html:
        issues.append("WARN: No conclusion block or callout key found")
    # Disclaimer
    if 'disclaimer-card' not in html:
        issues.append("FAIL: No .disclaimer-card found")
    # Drop cap recommended
    if 'dropcap-deep' not in html:
        issues.append("INFO: No drop cap found - editorial recommends drop cap for opening Phần I")
    # Cover không được có date-display redundant
    if 'date-display' in html:
        issues.append("WARN: date-display found - editorial cover dùng cover-meta-strip")
    return issues


def render_pdf(html_content: str, output_path: str, strict: bool = True):
    """
    Render HTML thành PDF. Chạy QC trước.
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
# WAVE 6 INTEGRATION HELPER
# ============================================================
def build_full_css(
    date_str: str,
    short_title: str = "OPVIA RESEARCH",
    fonts_dir: str = None,
    include_polish: bool = True,
) -> str:
    """
    Build complete CSS bao gồm core + viz + polish (covers, section openers, extras).

    Use this thay vì build_css() khi muốn dùng Wave 6 polish features
    (cover variants, section opener variants, sidebar callouts, glossary alpha, footnotes).

    Args:
        include_polish: nếu False, fallback về build_css() only (backward compat)
    """
    import sys, os
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, skill_dir)

    css = build_css(date_str=date_str, short_title=short_title, fonts_dir=fonts_dir)

    if include_polish:
        try:
            from covers import cover_styles
            css += cover_styles()
        except ImportError:
            pass

        try:
            from section_openers import section_opener_styles
            css += section_opener_styles()
        except ImportError:
            pass

        try:
            from extras import extras_styles
            css += extras_styles()
        except ImportError:
            pass

    return css
