#!/usr/bin/env python3
"""
render_engine.py - Parse .markup.md tags and produce a complete unpacked OOXML folder.

Usage:
    python3 render_engine.py input.markup.md output_dir/ \
        --subject "Corporate Issuers" --module-num 2 \
        --module-name "ESG Considerations in Investment Analysis"

Output: a ready-to-pack folder at output_dir/ with word/document.xml etc.
"""

import argparse, os, re, sys, textwrap

# ===============================================================================
# CANONICAL CONSTANTS
# ===============================================================================

C = {
    # Page
    "page_bg":        "FAFAF7",   # Cream paper

    # Text
    "body":           "1C1C1C",   # Near-black, slightly warmer
    "secondary":      "3B3B3B",   # Darker secondary for better contrast
    "muted":          "6B6B6B",   # Deeper muted, less washed-out

    # Brand - deep, editorial
    "indigo":         "2E3B7C",   # Deep navy-indigo
    "section_purple": "2C3878",   # Deep royal blue
    "gold":           "C49A1A",   # Rich antique gold
    "section_num_orange": "B85A1C",  # Burnt sienna
    "dark_amethyst": "5C2D91",       # Dark amethyst for Công thức cross-reference (distinct from subtitle)
    "dark_olive_gold": "7A5C00",     # Dark olive gold for Ví dụ cross-reference (distinct from icon_gold)
    "dark_teal":      "1E3A5F",   # Deep blue-black for cover module number
    "term_teal":      "0E6B85",   # Vibrant teal for [T:] terminology English term — visible "màu xanh"

    # Box backgrounds - very light tinted paper per box type
    # Each is a heavily diluted version of the accent hue — distinguishable but never glaring
    "box_purple_bg":  "EEE8F7",   # Very light lavender  (accent: icon_purple #6B3FA0)
    "box_gold_bg":    "F6EDD5",   # Very light warm cream (accent: icon_gold   #8B6B20)
    "box_green_bg":   "E4F0E9",   # Very light sage       (accent: icon_green  #2D6A4F)
    "box_orange_bg":  "F7E9E6",   # Very light coral/rose (accent: icon_orange #A04030)
    "box_blue_bg":    "E4ECF6",   # Very light slate blue (accent: icon_blue   #2B5597)

    # Highlight
    "highlight_bg":   "E8DEB0",   # Warm highlight

    # Box label/accent colors - deep, authoritative
    "icon_purple":    "6B3FA0",   # Rich purple
    "icon_gold":      "8B6B20",   # Dark goldenrod
    "icon_green":     "2D6A4F",   # Forest green
    "icon_orange":    "A04030",   # Brick red
    "icon_blue":      "2B5597",   # Steel blue

    # Header/footer
    "header_footer":  "5A5A5A",
    "rule_muted":     "CECECE",   # Thin rule between content and header/footer zones
}

# Color palette for formula variable color-coding - rich, editorial
FORMULA_VAR_COLORS = [
    "B83030",  # deep red
    "2B5597",  # steel blue
    "2D6A4F",  # forest green
    "7B3FA0",  # rich purple
    "A07820",  # dark gold
    "1A7A7A",  # deep teal
    "A04030",  # brick
    "5B3FA0",  # deep violet
]

# Subtle character tracking on body text — barely perceptible individually,
# but gives the whole document a more "set" typographic quality
BODY_TRACKING = 8  # twips (1 twip = 1/20 pt, so 8 = 0.4pt letter-spacing)

# Per-subject accent colors for the cover page subject line.
# One color per CFA subject area — premium editorial palette, dark and restrained.
# Lookup is case-insensitive partial match on the subject string.
SUBJECT_COLORS = {
    "corporate issuers":        "8B3A20",   # Terra cotta
    "fixed income":             "1A5270",   # Ocean blue
    "equity":                   "2E6B3E",   # Forest green
    "derivatives":              "5C3A8B",   # Deep violet
    "alternative":              "1A5B5B",   # Teal
    "portfolio management":     "6B4010",   # Dark walnut
    "quantitative":             "3A3A7C",   # Dark navy
    "financial statement":      "6B2020",   # Deep burgundy
    "economics":                "3A5A20",   # Olive green
    "ethics":                   "204A7B",   # Steel blue
}

# CLI --subject-color override (baseline colors per workspace CLAUDE.md may differ
# from engine defaults, e.g. FI burgundy #6B1B2C vs engine ocean blue).
SUBJECT_COLOR_OVERRIDE = [None]
CFA_LEVEL = ["I"]  # PATCH multi-level: --level I/II/III

def _subject_color(subject):
    """Return the accent color for a given subject name (case-insensitive partial match).
    A --subject-color CLI override always wins."""
    if SUBJECT_COLOR_OVERRIDE[0]:
        return SUBJECT_COLOR_OVERRIDE[0]
    sl = subject.lower()
    for key, val in SUBJECT_COLORS.items():
        if key in sl:
            return val
    return C["muted"]  # fallback: muted gray

BOX_SPECS = {
    "BOX_PURPLE":  {"label": "G\u1ee2I \u00dd H\u00ccNH MINH H\u1eccA",  "bg": C["box_purple_bg"], "accent": C["icon_purple"]},
    "BOX_KEY":     {"label": "\u0110I\u1ec2M M\u1ea4U CH\u1ed0T",          "bg": C["box_gold_bg"],   "accent": C["icon_gold"]},
    "BOX_EXAMPLE": {"label": "V\u00cd D\u1ee4 MINH H\u1eccA",             "bg": C["box_green_bg"],  "accent": C["icon_green"]},
    "BOX_WARN":    {"label": "L\u01AFU \u00dd QUAN TR\u1eccNG",            "bg": C["box_orange_bg"], "accent": C["icon_orange"]},
    "BOX_NOTE":    {"label": "GHI CH\u00da B\u1ed4 SUNG",                  "bg": C["box_blue_bg"],   "accent": C["icon_blue"]},
    # Distinct treatment for image-hint blocks (BOX_NOTE carrying Caption + Prompt pair
    # for external image generation). Auto-detected in render_box.
    "IMAGE_HINT":  {"label": "G\u1ee2I \u00dd H\u00ccNH MINH HO\u1ea0 (AI PROMPT)",  "bg": C["box_purple_bg"], "accent": C["icon_purple"]},
    "BOX_TAKEAWAY": {"label": "KEY TAKEAWAYS",                    "bg": C["box_gold_bg"],   "accent": C["icon_gold"]},
}

# ===============================================================================
# XML HELPERS
# ===============================================================================

_pid_counter = [0x50000001]

def pid():
    v = _pid_counter[0]
    _pid_counter[0] += 1
    return f"{v:08X}"

_GLYPH_FIX = [
    ("\U0001F4A1 ", ""), ("\U0001F4A1", ""),                     # 💡 light bulb
    ("\u26A0\uFE0F ", ""), ("\u26A0\uFE0F", ""),                 # ⚠️ warning+VS16
    ("\u26A0 ", ""), ("\u26A0", ""),                              # ⚠ warning
    ("\uFE0F", ""),                                               # stray variation selector
    ("\U0001F4F7 ", ""), ("\U0001F4F7", ""),                     # 📷 camera
    ("\u2756", "\u00B7"),                                         # ❖ -> · (middle dot)
    ("\u2192", "\u00BB"),                                         # → -> » (author text only; OMML bypasses esc)
    ("\u22EF", "..."),                                           # ⋯ -> ...
]
def esc(text):
    """Escape the 4 XML special characters; also normalize glyphs absent from Lato/Lora
    (they render as tofu/replacement boxes in MS Word). OMML formulas bypass esc, so math is untouched."""
    for _bad, _good in _GLYPH_FIX:
        if _bad in text:
            text = text.replace(_bad, _good)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def rpr(font="Lato", sz=20, bold=False, italic=False, color="1F1F1F", shd_fill=None,
        subscript=False, superscript=False, small_caps=False, letter_spacing=None):
    """Build a <w:rPr> interior string."""
    parts = [
        f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{font}"/>',
    ]
    if bold:
        parts.append("<w:b/><w:bCs/>")
    if italic:
        parts.append("<w:i/><w:iCs/>")
    if small_caps:
        parts.append("<w:smallCaps/>")
    parts.append(f'<w:color w:val="{color}"/>')
    parts.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    if letter_spacing is not None:
        # letter_spacing in twentieths of a point (e.g. 20 = 1pt, 40 = 2pt, 80 = 4pt)
        parts.append(f'<w:spacing w:val="{letter_spacing}"/>')
    if shd_fill:
        parts.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shd_fill}"/>')
    if subscript:
        parts.append('<w:vertAlign w:val="subscript"/>')
    if superscript:
        parts.append('<w:vertAlign w:val="superscript"/>')
    return "".join(parts)

def run(text, **rpr_kwargs):
    """A single <w:r> element."""
    return f'<w:r><w:rPr>{rpr(**rpr_kwargs)}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def run_break():
    """A line break <w:br/> run."""
    return '<w:r><w:br/></w:r>'

def para(runs_xml, pid_val=None, ppr_extra="", spacing_before=60, spacing_after=60, jc=None):
    """A complete <w:p> element."""
    if pid_val is None:
        pid_val = pid()
    sp = f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}" w:line="260" w:lineRule="auto"/>'
    jc_xml = f'<w:jc w:val="{jc}"/>' if jc else ""
    return (
        f'<w:p w14:paraId="{pid_val}" w14:textId="{pid_val}">'
        f'<w:pPr>{sp}{jc_xml}{ppr_extra}</w:pPr>'
        f'{runs_xml}'
        f'</w:p>'
    )

# ===============================================================================
# SUBSCRIPT HELPER
# ===============================================================================


def _preprocess_latex_commands(text):
    """Preprocess LaTeX-style commands with arguments before tokenization or Greek replacement.
    Handles: \sqrt{X} -> √X, \text{X} -> X, \ln/\log/\exp -> text literal,
    auto-bracket ^+/^-/^* and _+/_-/_*.
    Also strips null bytes and markdown ** bold artifacts (content authoring leftovers).
    """
    # Strip null bytes (invalid XML chars)
    text = text.replace('\x00', '')
    # Strip markdown ** bold artifacts (content authoring leftovers, should be [HL] or removed)
    text = text.replace('**', '')
    # \sqrt{X} -> √X
    text = re.sub(r'\\sqrt\{([^}]*)\}', '\u221A' + r'\1', text)
    # \text{X} -> X (strip wrapper)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    # \overline{X} / \bar{X} / \overline X / \bar X -> base + combining macron (legend/text path only)
    text = re.sub(r'\\(?:overline|bar)\s*\{([^}]*)\}', lambda m: m.group(1) + '\u0304', text)
    text = re.sub(r'\\(?:overline|bar)\s+([A-Za-z\u0370-\u03FF])', lambda m: m.group(1) + '\u0304', text)
    # \ln, \log, \exp, \min, \max, etc. -> text literal (preserve word boundary)
    text = re.sub(r'\\(ln|log|exp|min|max|lim|sup|inf|arg)\b', r'\1', text)
    # Auto-bracket unbraced ^+, ^-, ^* superscripts and _+, _-, _* subscripts
    text = re.sub(r'([A-Za-z\)\}])\^([+\-\*])(?![A-Za-z0-9{])', r'\1^{\2}', text)
    text = re.sub(r'([A-Za-z\)\}])_([+\-\*])(?![A-Za-z0-9{])', r'\1_{\2}', text)
    return text


def render_subscript_text(text, font="Lato", sz=26, color="4338CA", bold=False):
    """
    Convert text with sub/superscript notation into proper OOXML runs.

    Supported patterns:
        Simple subscript:   w_d, r_e, P_0       -> w + d(sub)
        Braced subscript:   l_{t,s}, P_{t+1}    -> l + t,s(sub)
        Simple superscript: P^n, x^2            -> P + n(sup)
        Braced superscript: P^{n+1}             -> P + n+1(sup)
        Combined:           P_0^n, r_{f}^{*}    -> P + 0(sub) + n(sup)
        Greek aliases:      \\theta, \\pi, \\rho, \\sigma, \\alpha, \\beta, \\gamma, \\delta,
                            \\lambda, \\mu, \\omega, \\phi, \\epsilon, \\eta, \\nu, \\tau, \\xi, \\zeta
    """
    # First pass: handle LaTeX commands with arguments
    text = _preprocess_latex_commands(text)

    # Second pass: replace Greek aliases with Unicode characters
    GREEK = {
        # Lowercase Greek
        r'\theta': '\u03B8', r'\vartheta': '\u03D1',
        r'\pi': '\u03C0', r'\varpi': '\u03D6',
        r'\rho': '\u03C1', r'\varrho': '\u03F1',
        r'\sigma': '\u03C3', r'\varsigma': '\u03C2',
        r'\alpha': '\u03B1', r'\beta': '\u03B2', r'\gamma': '\u03B3',
        r'\delta': '\u03B4', r'\epsilon': '\u03B5', r'\varepsilon': '\u03B5',
        r'\zeta': '\u03B6', r'\eta': '\u03B7', r'\iota': '\u03B9',
        r'\kappa': '\u03BA', r'\lambda': '\u03BB', r'\mu': '\u03BC',
        r'\nu': '\u03BD', r'\xi': '\u03BE', r'\omicron': '\u03BF',
        r'\tau': '\u03C4', r'\upsilon': '\u03C5',
        r'\phi': '\u03C6', r'\varphi': '\u03D5',
        r'\chi': '\u03C7', r'\psi': '\u03C8', r'\omega': '\u03C9',
        # Uppercase Greek
        r'\Theta': '\u0398', r'\Pi': '\u03A0', r'\Sigma': '\u03A3',
        r'\Delta': '\u0394', r'\Lambda': '\u039B', r'\Xi': '\u039E',
        r'\Gamma': '\u0393', r'\Phi': '\u03A6', r'\Psi': '\u03A8',
        r'\Omega': '\u03A9', r'\Upsilon': '\u03A5',
        # Math operators and symbols
        r'\sum': '\u2211', r'\prod': '\u220F', r'\int': '\u222B',
        r'\infty': '\u221E', r'\partial': '\u2202', r'\nabla': '\u2207',
        r'\neq': '\u2260', r'\leq': '\u2264', r'\geq': '\u2265',
        r'\approx': '\u2248', r'\equiv': '\u2261', r'\propto': '\u221D',
        r'\cdot': '\u00B7', r'\times': '\u00D7', r'\div': '\u00F7',
        r'\pm': '\u00B1', r'\mp': '\u2213',
        r'\in': '\u2208', r'\notin': '\u2209',
        r'\subset': '\u2282', r'\subseteq': '\u2286',
        r'\supset': '\u2283', r'\supseteq': '\u2287',
        r'\cup': '\u222A', r'\cap': '\u2229',
        r'\forall': '\u2200', r'\exists': '\u2203',
        r'\rightarrow': '\u2192', r'\leftarrow': '\u2190',
        r'\Rightarrow': '\u21D2', r'\Leftarrow': '\u21D0',
        r'\to': '\u2192', r'\mapsto': '\u21A6',
        r'\sqrt': '\u221A',  # Standalone backup if \sqrt{} regex didn't catch
    }
    for alias, char in GREEK.items():
        text = text.replace(alias, char)

    def _match_braces(s, start):
        """Find matching closing brace for opening at start. Returns end index after }, or -1."""
        if start >= len(s) or s[start] != '{':
            return -1
        depth = 1
        i = start + 1
        while i < len(s):
            if s[i] == '{':
                depth += 1
            elif s[i] == '}':
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return -1  # unmatched

    def _parse_simple_arg(s, start):
        """After _ or ^, parse simple arg [A-Za-z0-9] possibly with leading -. Returns (arg, end) or (None, start)."""
        i = start
        if i < len(s) and s[i] == '-':
            i += 1
        arg_start = i
        while i < len(s) and (s[i].isalnum() or s[i] == '*'):
            i += 1
        if i > arg_start:
            return s[start:i], i
        return None, start

    runs = []
    base_re = re.compile(r'[A-Za-z\u0370-\u03FF\)\u221A]+')

    pos = 0
    while pos < len(text):
        m = base_re.match(text, pos)
        if not m:
            runs.append(run(text[pos], font=font, sz=sz, bold=bold, color=color))
            pos += 1
            continue

        base = m.group(0)
        end = m.end()

        # Look for subscript and/or superscript after base
        subscr = None
        superscr = None
        scan_pos = end

        # Try subscript first
        if scan_pos < len(text) and text[scan_pos] == '_':
            if scan_pos + 1 < len(text) and text[scan_pos + 1] == '{':
                close = _match_braces(text, scan_pos + 1)
                if close > 0:
                    subscr = text[scan_pos + 2:close - 1]
                    scan_pos = close
            else:
                arg, new_pos = _parse_simple_arg(text, scan_pos + 1)
                if arg:
                    subscr = arg
                    scan_pos = new_pos

        # Try superscript
        if scan_pos < len(text) and text[scan_pos] == '^':
            if scan_pos + 1 < len(text) and text[scan_pos + 1] == '{':
                close = _match_braces(text, scan_pos + 1)
                if close > 0:
                    superscr = text[scan_pos + 2:close - 1]
                    scan_pos = close
            else:
                arg, new_pos = _parse_simple_arg(text, scan_pos + 1)
                if arg:
                    superscr = arg
                    scan_pos = new_pos

        # If we found sub or sup, emit base + sub/sup runs
        if subscr or superscr:
            # User feedback: sub/sup quá nhỏ. 80% scale + min 16 (8pt) cho dễ đọc.
            small_sz = max(int(sz * 0.8), 16)
            runs.append(run(base, font=font, sz=sz, bold=bold, color=color))
            if subscr:
                runs.append(run(subscr, font=font, sz=small_sz, bold=bold, color=color, subscript=True))
            if superscr:
                runs.append(run(superscr, font=font, sz=small_sz, bold=bold, color=color, superscript=True))
            pos = scan_pos
        else:
            # Plain base, emit and advance
            runs.append(run(base, font=font, sz=sz, bold=bold, color=color))
            pos = end

    return "".join(runs)


def render_subscript_colored(text, color, font="Lato", sz=26, bold=False):
    """Render text with subscript notation in a specific color."""
    return render_subscript_text(text, font=font, sz=sz, color=color, bold=bold)

# ===============================================================================
# INLINE TAG PARSER
# ===============================================================================

def parse_inline(text):
    """
    Parse inline tags within body text and return w:r XML string.
    Handles [T: term | meaning], [T: term], [HL]...[/HL], [F]...[/F].
    Auto-strips null bytes and markdown ** from content authoring artifacts.
    """
    # Auto-clean content authoring artifacts
    text = text.replace('\x00', '').replace('**', '')
    runs = []
    remaining = text

    while remaining:
        # [T: term | meaning] - English term bold vibrant teal + Vietnamese meaning italic muted gray smaller
        # Disallow '[', ']', '|' inside term/meaning so we don't span across multiple [T:] tags.
        # Tolerate authoring artifacts: trailing ']' duplicates ([T: x]] or [T: x|y]]).
        m = re.match(r'^\[T:\s*([^\[\]\|]+?)\s*\|\s*([^\[\]]+?)\s*\]+', remaining)
        if m:
            term, meaning = m.group(1), m.group(2)
            runs.append(run(term, font="Lato", sz=20, bold=True, color=C["term_teal"]))
            # Meaning: italic, gray-muted, 1 size smaller — exactly per user spec
            runs.append(run(f" (", font="Lato", sz=18, italic=True, color=C["muted"]))
            runs.append(run(meaning, font="Lato", sz=18, italic=True, color=C["muted"]))
            runs.append(run(")", font="Lato", sz=18, italic=True, color=C["muted"]))
            remaining = remaining[m.end():]
            continue

        # [T: term] - tolerate trailing ']' duplicates; disallow '[' and ']' inside term
        m = re.match(r'^\[T:\s*([^\[\]]+?)\s*\]+', remaining)
        if m:
            runs.append(run(m.group(1), font="Lato", sz=20, bold=True, color=C["term_teal"]))
            remaining = remaining[m.end():]
            continue

        # [HL]...[/HL]
        m = re.match(r'^\[HL\](.*?)\[/HL\]', remaining, re.DOTALL)
        if m:
            runs.append(run(m.group(1), font="Lato", sz=20, color=C["body"], shd_fill=C["highlight_bg"]))
            remaining = remaining[m.end():]
            continue

        # [F]...[/F] inline formula with subscript support
        m = re.match(r'^\[F\](.*?)\[/F\]', remaining, re.DOTALL)
        if m:
            runs.append(render_subscript_text(m.group(1), font=ACTIVE_FONTS.get("mono", "Lato"), sz=20, color=C["indigo"]))
            remaining = remaining[m.end():]
            continue

        # Plain text: consume up to the next tag or end
        m = re.match(r'^(.*?)(?=\[T:|\[HL\]|\[F\])', remaining, re.DOTALL)
        if m and m.group(1):
            runs.extend(_plain_text_runs(m.group(1)))
            remaining = remaining[m.end():]
            continue

        # No more tags: rest is plain text
        runs.extend(_plain_text_runs(remaining))
        break

    return "".join(runs)


def _plain_text_runs(text):
    """Convert plain text to runs. (N) patterns become line-broken list items using bold typographic (N).
    A sentence immediately before (1) that ends with ':' is rendered bold + underlined.
    Also auto-formats 'Công thức N.M' and 'Ví dụ N.M' references with editorial styling."""
    result = []

    # Pre-process: highlight 'Công thức N.M' and 'Ví dụ N.M' references with subtle styling
    # Use Unicode private-use area chars as markers (valid in XML, won't appear naturally)
    _MARK_BEGIN = "\uE000"
    _MARK_END = "\uE001"
    _MARK_VD_BEGIN = "\uE002"
    _MARK_VD_END = "\uE003"
    text = re.sub(r'(Công thức\s+\d+\.\d+)', _MARK_BEGIN + r'\1' + _MARK_END, text)
    text = re.sub(r'(Ví dụ\s+\d+\.\d+)', _MARK_VD_BEGIN + r'\1' + _MARK_VD_END, text)
    # Step/sequence markers: bold + process-orange so multi-step reasoning scans as ONE quy trình
    _MARK_ST_BEGIN = "\uE004"
    _MARK_ST_END = "\uE005"
    _STEP_PAT = (r'(?:^|(?<=\. )|(?<=: )|(?<=\n))'
                 r'(Thứ (?:nhất|hai|ba|tư|năm|sáu|bảy|tám)|Bước \d+[a-z]?|'
                 r'Đầu tiên|Tiếp theo|Sau đó|Kế tiếp|Cuối cùng|Một,|Hai,|Ba,|Bốn,|Năm,)')
    text = re.sub(_STEP_PAT, _MARK_ST_BEGIN + r'\1' + _MARK_ST_END, text)


    has_list = bool(re.search(r'\(1\)\s*\S+', text) and re.search(r'\(2\)\s*\S+', text))  # real inline list starts at (1) with >=2 items; avoids math like 0.25(33)
    if not has_list:
        if text:
            # Split text by reference markers and style each segment differently
            segments = []  # list of (text, style_kind)
            remaining = text
            while remaining:
                # Find next marker (any kind)
                m_ct = remaining.find(_MARK_BEGIN)
                m_vd = remaining.find(_MARK_VD_BEGIN)
                m_st = remaining.find(_MARK_ST_BEGIN)
                # Pick the earliest of the three marker kinds
                _cands = [(m_ct, 'ct'), (m_vd, 'vd'), (m_st, 'st')]
                _cands = [(i, k) for i, k in _cands if i >= 0]
                next_marker, marker_type = (min(_cands) if _cands else (-1, None))
                if next_marker < 0:
                    segments.append((remaining, 'plain'))
                    break
                # Plain part before marker
                if next_marker > 0:
                    segments.append((remaining[:next_marker], 'plain'))
                # Find end marker
                if marker_type == 'ct':
                    start = next_marker + len(_MARK_BEGIN)
                    end = remaining.find(_MARK_END, start)
                    if end < 0:
                        segments.append((remaining[next_marker:], 'plain'))
                        break
                    segments.append((remaining[start:end], 'comthuc'))
                    remaining = remaining[end + len(_MARK_END):]
                elif marker_type == 'vd':
                    start = next_marker + len(_MARK_VD_BEGIN)
                    end = remaining.find(_MARK_VD_END, start)
                    if end < 0:
                        segments.append((remaining[next_marker:], 'plain'))
                        break
                    segments.append((remaining[start:end], 'vidu'))
                    remaining = remaining[end + len(_MARK_VD_END):]
                else:  # st (step marker)
                    start = next_marker + len(_MARK_ST_BEGIN)
                    end = remaining.find(_MARK_ST_END, start)
                    if end < 0:
                        segments.append((remaining[next_marker:], 'plain'))
                        break
                    segments.append((remaining[start:end], 'step'))
                    remaining = remaining[end + len(_MARK_ST_END):]

            for seg_text, kind in segments:
                if not seg_text:
                    continue
                if kind == 'comthuc':
                    # "Công thức N.M": italic + dark amethyst (distinct from subtitle), no bold no enlarge
                    result.append(run(seg_text, font="Lato", sz=20, italic=True, color=C["dark_amethyst"], letter_spacing=10))
                elif kind == 'step':
                    # Sequence marker: bold + process orange (same family as section numbers)
                    result.append(run(seg_text, font="Lato", sz=20, bold=True, color=C["section_num_orange"]))
                elif kind == 'vidu':
                    # "Ví dụ N.M": italic + dark olive gold (distinct from icon_gold), no bold no enlarge
                    result.append(run(seg_text, font="Lato", sz=20, italic=True, color=C["dark_olive_gold"], letter_spacing=10))
                else:
                    # Auto-detect subscript/superscript patterns in plain text
                    if re.search(r'[A-Za-z]+_\{[^}]+\}|[A-Za-z]+_[A-Za-z0-9]+|[A-Za-z\)]\^\{[^}]+\}|[A-Za-z\)]\^-?[A-Za-z0-9]+|\\[A-Za-z]+', seg_text):
                        result.append(render_subscript_text(seg_text, font="Lato", sz=20, color=C["body"]))
                    else:
                        result.append(run(seg_text, font="Lato", sz=20, color=C["body"], letter_spacing=BODY_TRACKING))
        return result

    # Split on (N) patterns and format as list with line breaks
    # Uses bold typographic (N) instead of emoji circled numbers - cleaner, more editorial
    parts = re.split(r'\((\d+)\)', text)
    i = 0
    first_item = True  # Track whether we're at the first list item
    while i < len(parts):
        if i + 1 < len(parts) and parts[i + 1].isdigit():
            before = parts[i].strip()
            if before:
                # If this is the intro text (before first list item) and ends with ':'
                # only the LAST sentence (ending with ':') gets bold + underline.
                # Earlier text in the same chunk renders as plain body.
                if first_item and before.rstrip().endswith(':'):
                    # Split at the last sentence boundary before the intro sentence
                    # A sentence boundary is ". " or "\n" followed by a capital letter
                    m_split = re.search(r'^(.*?[.!?])\s+([^.!?].*:)\s*$', before.strip(), re.DOTALL)
                    if m_split:
                        prior_text = m_split.group(1).strip()
                        intro_text = m_split.group(2).strip()
                    else:
                        prior_text = ""
                        intro_text = before.strip()
                    if prior_text:
                        result.append(run(prior_text + " ", font="Lato", sz=20, color=C["body"], letter_spacing=BODY_TRACKING))
                    intro_rpr_inner = (
                        f'<w:rFonts w:ascii="Lato" w:hAnsi="Lato" w:cs="Lato" w:eastAsia="Lato"/>'
                        f'<w:b/><w:bCs/>'
                        f'<w:u w:val="single"/>'
                        f'<w:color w:val="{C["body"]}"/>'
                        f'<w:sz w:val="20"/><w:szCs w:val="20"/>'
                    )
                    result.append(
                        f'<w:r><w:rPr>{intro_rpr_inner}</w:rPr>'
                        f'<w:t xml:space="preserve">{esc(intro_text)}</w:t></w:r>'
                    )
                else:
                    result.append(run(before + " ", font="Lato", sz=20, color=C["body"], letter_spacing=BODY_TRACKING))
            num = int(parts[i + 1])
            result.append(run_break())
            # Custom typographic glyph for numbered lists (Unicode circled numbers)
            glyphs = ["\u2776", "\u2777", "\u2778", "\u2779", "\u277A",
                      "\u277B", "\u277C", "\u277D", "\u277E", "\u277F"]
            glyph = glyphs[num-1] if 1 <= num <= 10 else f"({num})"
            result.append(run(glyph, font="Lato", sz=22, bold=True, color=C["section_purple"]))
            result.append(run("  ", font="Lato", sz=20, color=C["body"]))
            first_item = False
            i += 2
        else:
            text_part = parts[i].strip().rstrip(',').strip()
            if text_part:
                result.append(run(text_part, font="Lato", sz=20, color=C["body"], letter_spacing=BODY_TRACKING))
            i += 1

    return result

# ===============================================================================
# BLOCK RENDERERS
# ===============================================================================

_section_counter = [0]

# Font stack options for --font-stack flag
FONT_STACKS = {
    "A": {  # Editorial Textbook
        "body": "Source Serif Pro",
        "display": "Fraunces",
        "mono": "Source Code Pro",
        "math": "STIX Two Math",
    },
    "B": {  # Modern Hybrid (default, currently used)
        "body": "Lato",
        "display": "Lora",
        "mono": "Lato",
        "math": "Lato",
    },
    "C": {  # Vietnamese-Optimized
        "body": "Be Vietnam Pro",
        "display": "Be Vietnam Pro",
        "mono": "Source Code Pro",
        "math": "STIX Two Math",
    },
}

FONT_STACKS["D"] = {  # Editorial Institutional Research: serif display full Vietnamese
    "body": "Lato",
    "display": "Lora",
    "mono": "JetBrains Mono",
    "math": "JetBrains Mono",
}

# EIR style flag (--style eir): Exhibit numbering + KEY TAKEAWAYS treatment
STYLE_EIR = [False]
EXHIBIT_COUNTER = [0]

# Active fonts (initialized to default B; overridden by --font-stack)
ACTIVE_FONTS = FONT_STACKS["B"].copy()




def render_end_paper(position="front"):
    """Render decorative end paper page (Tầng I.3).
    position: 'front' (before cover) or 'back' (after colophon)
    Uses subtle Art Deco geometric pattern: chevron/diamond ornaments centered.
    """
    parts = []

    # Top space push to vertical center
    parts.append(para("", spacing_before=2400, spacing_after=0))

    # Decorative pattern - 5 lines of geometric ornaments at increasing/decreasing density
    if position == "front":
        # Lines build up
        patterns = [
            ("\u2756", 24),
            ("\u2756  \u2756", 28),
            ("\u2756  \u2756  \u2756", 32),
            ("\u2756  \u2756  \u2756  \u2756", 36),
            ("\u2756  \u2756  \u2756  \u2756  \u2756", 40),
        ]
    else:
        # Lines wind down
        patterns = [
            ("\u2756  \u2756  \u2756  \u2756  \u2756", 40),
            ("\u2756  \u2756  \u2756  \u2756", 36),
            ("\u2756  \u2756  \u2756", 32),
            ("\u2756  \u2756", 28),
            ("\u2756", 24),
        ]

    for txt, sz in patterns:
        # Alternate gold and indigo
        for i, (pattern_text, pattern_sz) in enumerate([(txt, sz)]):
            color = C["gold"] if (i + len(patterns)) % 2 == 0 else C["section_purple"]
            orn_run = run(pattern_text, font=ACTIVE_FONTS.get("display", "Lora"), sz=pattern_sz, color=color, letter_spacing=80)
            parts.append(para(orn_run, spacing_before=80, spacing_after=80, jc="center"))

    # Page break to next page
    parts.append(f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}"><w:r><w:br w:type="page"/></w:r></w:p>')

    return "\n".join(parts)

def render_cover(subject, title, subtitle, hero_prompt=""):
    """Generate the cover page paragraphs. Subtitle is accepted but not rendered.

    Cover layout (Bloomberg/editorial style):
    1. Thick gold top rule
    2. Subject: Raleway 15pt, muted, OOXML letter-spacing (no spaced character hack)
    3. Single line: "Module {#} : {Module Name}" — module# in per-module accent color,
       separator and name in purple, all Raleway Bold 22pt
    4. Single medium gold rule below title
    5. "CFA LEVEL I" badge: Raleway italic, muted, letter-spaced ALL CAPS
    """
    paras = []
    # Large top spacer to push content toward vertical center
    paras.append(para("", spacing_before=2800, spacing_after=0))

    # Thick gold top rule (4pt = sz=32)
    top_rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="32" w:space="12" w:color="{C["gold"]}"/></w:pBdr>'
    )
    paras.append(para("", ppr_extra=top_rule_ppr, spacing_before=0, spacing_after=280))

    # Subject line: Raleway 17pt (sz=34), BOLD, subject-specific accent color, letter-spaced ALL CAPS
    subj_color = _subject_color(subject)
    subject_rpr = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=34, bold=True, color=subj_color, letter_spacing=80)
    paras.append(para(
        f'<w:r><w:rPr>{subject_rpr}</w:rPr><w:t xml:space="preserve">{esc(subject.upper())}</w:t></w:r>',
        spacing_before=0, spacing_after=200, jc="center"
    ))

    # Hero placeholder: a decorative procedural geometric block (Art Deco vibe)
    # Default fallback when no AI image generation available.
    # Renders as: a centered framed block with diagonal pattern and gold ornament
    if hero_prompt or True:  # Always render placeholder for now
        # Top thin gold rule for hero frame
        hero_top = f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
        paras.append(para("", ppr_extra=hero_top, spacing_before=120, spacing_after=80))

        # User removed ornaments. Render empty labeled image slot for manual image insertion.
        label_run = run("HÌNH ẢNH", font=ACTIVE_FONTS.get("display", "Lora"), sz=18, italic=True, color=C["muted"], letter_spacing=80)
        paras.append(para(label_run, spacing_before=120, spacing_after=120, jc="center"))
        # Vertical room for inserted image (~ 6 cm)
        for _ in range(6):
            paras.append(para("", spacing_before=80, spacing_after=80))

        # Bottom thin gold rule for hero frame
        hero_bottom = f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
        zwsp_run = run("\u200B", font="Lato", sz=10, color=C["page_bg"])
        paras.append(para(zwsp_run, ppr_extra=hero_bottom, spacing_before=80, spacing_after=200))

    # Single-line title: "Module {#} : {Module Name}"
    # "Module #" slightly darker than module name for gentle contrast.
    # Both drawn from the same purple family — not dramatically different.
    MODULE_NUM_COLOR  = "1E2862"   # Slightly darker purple for "Module #"
    MODULE_NAME_COLOR = C["section_purple"]  # Standard purple for module name

    mod_match = re.match(r'^Module\s+(\d+)\s*:\s*(.+)$', title, re.IGNORECASE)
    if mod_match:
        mod_num = int(mod_match.group(1))
        mod_name = mod_match.group(2).strip()
        num_rpr  = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=44, bold=True,  color=MODULE_NUM_COLOR)
        sep_rpr  = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=44, bold=False, color=C["muted"])
        name_rpr = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=44, bold=True,  color=MODULE_NAME_COLOR)
        title_xml = (
            f'<w:r><w:rPr>{num_rpr}</w:rPr><w:t xml:space="preserve">Module {mod_num}</w:t></w:r>'
            f'<w:r><w:rPr>{sep_rpr}</w:rPr><w:t xml:space="preserve"> : </w:t></w:r>'
            f'<w:r><w:rPr>{name_rpr}</w:rPr><w:t xml:space="preserve">{esc(mod_name)}</w:t></w:r>'
        )
    else:
        name_rpr = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=44, bold=True, color=MODULE_NAME_COLOR)
        title_xml = f'<w:r><w:rPr>{name_rpr}</w:rPr><w:t xml:space="preserve">{esc(title)}</w:t></w:r>'

    paras.append(para(title_xml, spacing_before=0, spacing_after=260, jc="center"))

    # Single medium gold rule below title (no blue/indigo rule)
    gold_rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="20" w:space="10" w:color="{C["gold"]}"/></w:pBdr>'
    )
    paras.append(para("", ppr_extra=gold_rule_ppr, spacing_before=0, spacing_after=300))

    # "CFA LEVEL I" badge: Raleway italic, muted, letter-spaced
    badge_rpr = rpr(font=ACTIVE_FONTS.get("display", "Lora"), sz=18, italic=True, color=C["muted"], letter_spacing=40)
    paras.append(para(
        f'<w:r><w:rPr>{badge_rpr}</w:rPr><w:t xml:space="preserve">CFA LEVEL {CFA_LEVEL[0]}</w:t></w:r>',
        spacing_before=0, spacing_after=0, jc="center"
    ))

    paras.append(
        f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}">'
        f'<w:r><w:br w:type="page"/></w:r></w:p>'
    )

    return "\n".join(paras)






def render_toc():
    """Render an auto-TOC using OOXML w:sdt + TOC field. User must update fields when opening doc."""
    parts = []

    # TOC heading
    toc_heading = run("Mục lục", font=ACTIVE_FONTS.get("display", "Lora"), sz=36, bold=True, color=C["section_purple"])
    parts.append(para(toc_heading, spacing_before=400, spacing_after=240, jc="center"))

    # Gold rule below
    rule_ppr = f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:color="{C["gold"]}"/></w:pBdr>'
    parts.append(para("", ppr_extra=rule_ppr, spacing_before=0, spacing_after=200))

    # TOC field - "TOC \o \"1-3\" \h \z \u" - generates from Heading 1-3 styles
    # Note: requires Update Fields on open
    toc_field = (
        f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}">'
        '<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9000"/></w:tabs></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o &quot;1-3&quot; \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:rPr><w:rFonts w:ascii="Lato" w:hAnsi="Lato"/><w:i/><w:color w:val="6B6B6B"/><w:sz w:val="20"/></w:rPr>'
        '<w:t xml:space="preserve">Right-click and Update Field to populate the table of contents.</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p>'
    )
    parts.append(toc_field)

    # Page break
    parts.append(f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}"><w:r><w:br w:type="page"/></w:r></w:p>')

    return "\n".join(parts)


def render_formula_card(formulas):
    """Render formula card at end of module: 2-col dense layout with all formulas listed."""
    parts = []

    # Heading
    heading = run("Formula Card", font=ACTIVE_FONTS.get("display", "Lora"), sz=36, bold=True, color=C["section_purple"])
    parts.append(para(heading, spacing_before=400, spacing_after=120, jc="center"))

    sub = run("Tổng hợp công thức của module", font="Lato", sz=18, italic=True, color=C["muted"])
    parts.append(para(sub, spacing_before=0, spacing_after=240, jc="center"))

    rule_ppr = f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:color="{C["gold"]}"/></w:pBdr>'
    parts.append(para("", ppr_extra=rule_ppr, spacing_before=0, spacing_after=200))

    # Render formulas as compact list
    for idx, f_text in enumerate(formulas, 1):
        # Formula number label
        num_run = run(f"({idx})  ", font="Lato", sz=18, bold=True, color=C["section_num_orange"])
        # Formula main line
        f_main = f_text.split('\n')[0].strip() if '\n' in f_text else f_text.strip()
        f_runs = render_subscript_text(f_main, font=ACTIVE_FONTS.get("mono", "Lato"), sz=20, color=C["indigo"])
        ppr = '<w:ind w:left="240" w:right="240"/>'
        parts.append(para(num_run + f_runs, ppr_extra=ppr, spacing_before=40, spacing_after=40))

    return "\n".join(parts)




def write_subject_handoff(subject, module_num, module_name, terms_dict, formulas_list, workspace_dir):
    """Write or append subject-level handoff document for continuity across modules.

    Saves to {workspace_dir}/../subjects/{SUBJ}_handoff.md.
    Future modules of same subject load this for terminology/notation consistency.
    """
    import os
    import datetime

    # Get subject prefix (e.g., "Derivatives" -> "DER")
    subject_codes = {
        "Corporate Issuers": "CI",
        "Fixed Income": "FI",
        "Equity": "EQ",
        "Derivatives": "DER",
        "Alternative Investments": "AI",
        "Portfolio Management": "PM",
        "Quantitative Methods": "QM",
        "Financial Statement Analysis": "FSA",
        "Economics": "ECO",
        "Ethics": "ETH",
    }
    subj_code = subject_codes.get(subject, subject[:3].upper())

    handoff_dir = os.path.join(os.path.dirname(workspace_dir), "subjects")
    os.makedirs(handoff_dir, exist_ok=True)
    handoff_path = os.path.join(handoff_dir, f"{subj_code}_handoff.md")

    # Read existing or create new
    existing = ""
    if os.path.exists(handoff_path):
        with open(handoff_path, "r", encoding="utf-8") as f:
            existing = f.read()
    else:
        existing = f"""# {subject} Subject Handoff

This document tracks conventions and decisions across modules of {subject} for consistency.
"""

    # Append module entry (or update if already exists)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    module_entry = f"""

## Module {module_num}: {module_name}
*Rendered: {timestamp}*

### Terminology used ({len(terms_dict)} terms)
"""
    # First 10 terms
    for i, (term, meaning) in enumerate(sorted(terms_dict.items())[:10]):
        module_entry += f"- **{term}**: {meaning}\n"
    if len(terms_dict) > 10:
        module_entry += f"- ... ({len(terms_dict) - 10} more)\n"

    module_entry += f"""
### Formulas referenced ({len(formulas_list)} formulas)
- Total Công thức blocks: {len(formulas_list)}
- Numbering scheme: {module_num}.1 through {module_num}.{len(formulas_list)} (running counter)

### Notation conventions
- Subscript notation: simple `w_d`, braced `l_{{t,s}}`
- Greek letters via LaTeX: `\\theta`, `\\sigma`, `\\rho`
- All formulas have where-section
- Cross-references via §N or {{ref:name}}
"""

    # Remove old entry for same module if exists, append new
    import re as _re
    old_section_pattern = _re.compile(rf"\n## Module {module_num}:.*?(?=\n## Module |\Z)", _re.DOTALL)
    existing = old_section_pattern.sub("", existing)

    final = existing.rstrip() + module_entry

    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(final)

    return handoff_path

def render_glossary(terms_dict):
    """Render glossary appendix from collected [T:term|meaning] pairs.
    terms_dict: {term: meaning}"""
    if not terms_dict:
        return ""

    parts = []

    # Page break before
    parts.append(f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}"><w:r><w:br w:type="page"/></w:r></w:p>')

    heading = run("Thuật ngữ", font=ACTIVE_FONTS.get("display", "Lora"), sz=36, bold=True, color=C["section_purple"])
    parts.append(para(heading, spacing_before=400, spacing_after=120, jc="center"))

    sub = run("Glossary, sắp theo bảng chữ cái", font="Lato", sz=18, italic=True, color=C["muted"])
    parts.append(para(sub, spacing_before=0, spacing_after=240, jc="center"))

    rule_ppr = f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:color="{C["gold"]}"/></w:pBdr>'
    parts.append(para("", ppr_extra=rule_ppr, spacing_before=0, spacing_after=200))

    for term in sorted(terms_dict.keys(), key=lambda x: x.lower()):
        meaning = terms_dict[term]
        term_run = run(term, font="Lato", sz=20, bold=True, color=C["indigo"])
        sep_run = run("  :  ", font="Lato", sz=20, color=C["muted"])
        meaning_run = run(meaning, font="Lato", sz=20, italic=True, color=C["secondary"])
        ppr = '<w:ind w:left="0" w:right="0" w:hanging="0"/>'
        parts.append(para(term_run + sep_run + meaning_run, ppr_extra=ppr, spacing_before=30, spacing_after=30))

    return "\n".join(parts)

def render_halftitle(subject, title, module_num, module_name):
    """Render half-title page: pure typography, minimal, no ornaments.
    Editorial standard: just module name centered with significant whitespace."""
    paras = []

    # Vertical center push (about 35% of page height)
    paras.append(para("", spacing_before=4800, spacing_after=0))

    # Just the module name in italic display font, small caps style via letter spacing
    name_run = run(module_name, font=ACTIVE_FONTS.get("display", "Lora"), sz=44, italic=True,
                    color=C["section_purple"], letter_spacing=20)
    paras.append(para(name_run, spacing_before=0, spacing_after=400, jc="center"))

    # Single thin gold rule centered
    rule_ppr = f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="{C["gold"]}"/><w:left w:val="nil"/><w:right w:val="nil"/></w:pBdr><w:ind w:left="3000" w:right="3000"/>'
    paras.append(para("", ppr_extra=rule_ppr, spacing_before=0, spacing_after=160))

    # Subject in tiny letter-spaced caps
    subj_run = run(f"Module {module_num}  \u00B7  {subject}", font=ACTIVE_FONTS.get("display", "Lora"), sz=16,
                   italic=True, color=C["muted"], letter_spacing=60)
    paras.append(para(subj_run, spacing_before=0, spacing_after=0, jc="center"))

    # Page break
    paras.append(f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}"><w:r><w:br w:type="page"/></w:r></w:p>')

    return "\n".join(paras)



def render_footnote(content):
    """Render an inline footnote: small italic text with leading marker, hairline rule above."""
    foot_ppr = (
        f'<w:pBdr><w:top w:val="single" w:sz="2" w:space="2" w:color="{C["rule_muted"]}"/></w:pBdr>'
        f'<w:ind w:left="240" w:right="240"/>'
    )
    marker_run = run("\u2020 ", font="Lato", sz=14, color=C["icon_gold"])
    body_runs = parse_inline(content.strip())
    import re as _re
    body_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', body_runs)
    return para(marker_run + body_runs, ppr_extra=foot_ppr, spacing_before=80, spacing_after=80)


def render_hanging_def(term, meaning):
    """Render a definition with hanging indent: term flush, meaning indented after dash."""
    hang_ppr = '<w:ind w:left="600" w:hanging="600"/>'
    term_run = run(term, font="Lato", sz=20, bold=True, color=C["indigo"])
    sep_run = run("\u2003:\u2003", font="Lato", sz=20, color=C["muted"])
    meaning_run = run(meaning, font="Lato", sz=20, color=C["secondary"])
    return para(term_run + sep_run + meaning_run, ppr_extra=hang_ppr, spacing_before=40, spacing_after=40)


def render_colophon(subject, module_num, module_name):
    """Render colophon page at end of module: editorial detail, who/how/font info."""
    parts = []

    # Page break before colophon
    parts.append(f'<w:p w14:paraId="{pid()}" w14:textId="{pid()}"><w:r><w:br w:type="page"/></w:r></w:p>')

    # Push to vertical center
    parts.append(para("", spacing_before=4500, spacing_after=0))

    # Single fleuron
    fleuron_run = run("\u2766", font=ACTIVE_FONTS.get("display", "Lora"), sz=48, color=C["gold"])
    parts.append(para(fleuron_run, spacing_before=0, spacing_after=240, jc="center"))

    # Colophon text
    lines = [
        ("This module is set in Inter and Raleway,", 18, "muted"),
        ("with formulas in Consolas.", 18, "muted"),
        ("", 12, "muted"),  # spacer
        (f"CFA Level {CFA_LEVEL[0]} \u00B7 {subject} \u00B7 Module {module_num}", 16, "icon_gold"),
        (f"{module_name}", 18, "section_purple"),
    ]
    for text, sz, color_key in lines:
        if not text:
            parts.append(para("", spacing_before=80, spacing_after=80))
            continue
        ln_run = run(text, font=ACTIVE_FONTS.get("display", "Lora"), sz=sz, italic=True, color=C[color_key], letter_spacing=20)
        parts.append(para(ln_run, spacing_before=20, spacing_after=20, jc="center"))

    return "\n".join(parts)


def render_section_tab(section_num, section_total=8):
    """Render a small color-coded tab indicator at section start (visible at page edge).
    Uses positioned graphic on right margin via w:framePr.
    """
    # Color shifts through section family
    section_tab_colors = ["1E2862", "232D6E", "283278", "2C3878", "323D80", "384388", "3E4990", "445098"]
    tab_color = section_tab_colors[(section_num - 1) % len(section_tab_colors)]

    # Small tab using framePr positioned to right margin
    tab_pid = pid()
    # Vertical position based on section number for staggered tabs
    v_offset = 1500 + (section_num - 1) * 800

    tab_xml = (
        f'<w:p w14:paraId="{tab_pid}" w14:textId="{tab_pid}">'
        f'<w:pPr>'
        f'<w:framePr w:w="240" w:h="600" w:hSpace="0" w:vSpace="0" w:wrap="around" '
        f'w:vAnchor="page" w:hAnchor="page" w:x="11700" w:y="{v_offset}"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{tab_color}"/>'
        f'<w:spacing w:before="0" w:after="0"/>'
        f'</w:pPr>'
        f'<w:r><w:rPr><w:color w:val="{tab_color}"/><w:sz w:val="2"/></w:rPr><w:t xml:space="preserve">.</w:t></w:r>'
        f'</w:p>'
    )
    return tab_xml

def render_section(en_title, brief):
    """Generate section heading: number + title on one line, 18pt, with thin rule below.
    Adds color-coded section tab at right margin (Tầng E.5)."""
    _section_counter[0] += 1
    num = _section_counter[0]
    paras = []

    # Color-coded section tab at right margin (Tầng E.5) DISABLED per user feedback (random colored dashes on right margin)

    # User preference: page break before each new section (clean separation)
    # Each [SECTION] starts on a fresh page
    _pbb = '<w:pageBreakBefore/>' if num > 1 else ''  # PATCH L1: pageBreakBefore tranh trang trong

    # User feedback: gap số-title quá rộng + size quá to. 
    # Giảm em-space xuống 1 (và dùng "." separator), giảm size từ 18pt (sz=36) xuống 16pt (sz=32).
    num_run = run(f"{num}.\u2002", font=ACTIVE_FONTS.get("display", "Lato"), sz=32, bold=True, color=C["section_num_orange"], letter_spacing=20)
    section_colors = ["1E2862", "232D6E", "283278", "2C3878", "323D80", "384388", "3E4990", "445098"]
    sec_color = section_colors[(num - 1) % len(section_colors)]
    title_run = run(en_title, font=ACTIVE_FONTS.get("display", "Lato"), sz=32, bold=True, color=sec_color)
    paras.append(para(num_run + title_run, ppr_extra=_pbb, spacing_before=240, spacing_after=40))

    # Thin purple rule below title
    rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="{C["section_purple"]}"/></w:pBdr>'
    )
    paras.append(para("", ppr_extra=rule_ppr, spacing_before=0, spacing_after=40))

    # User feedback: bỏ section brief subtitle (e.g., "Khung carry arbitrage làm nền cho toàn module")
    # vì redundant với SECTION_OPEN pre-text. Brief vẫn parsed để giữ backward-compat
    # nhưng KHÔNG render trên doc.

    return "\n".join(paras)


def render_subsection(en_title, vi_title):
    """Generate subsection heading using a proper OOXML left border rule instead of
    a Unicode text character. This renders as a true graphic rule in Word."""
    paras = []

    # User feedback: subsection inclined line đổi sang navy blue (fitting với header).
    # Gold rule was clashing with INTUITION/SECTION_OPEN gold accents.
    sub_ppr = (
        f'<w:pBdr>'
        f'<w:left w:val="single" w:sz="16" w:space="12" w:color="{C["section_purple"]}"/>'
        f'</w:pBdr>'
        f'<w:ind w:left="240"/>'
    )
    title_run = run(en_title, font="Lato", sz=26, bold=True, color=C["section_purple"])
    paras.append(para(title_run, ppr_extra=sub_ppr, spacing_before=320, spacing_after=120))

    if vi_title:
        # Vietnamese subtitle: no gold border, just deeper indent to align under the English title
        vi_ppr = f'<w:ind w:left="360"/>'
        vi_run = run(vi_title, font="Lato", sz=16, italic=True, color=C["muted"], letter_spacing=10)
        paras.append(para(vi_run, ppr_extra=vi_ppr, spacing_before=0, spacing_after=160))

    return "\n".join(paras)




def render_body_with_dropcap(text, standfirst=False):
    """Render body paragraph with optional drop cap (first letter 3-line) and italic standfirst.
    First letter goes into a w:framePr w:dropCap drop cap frame; rest of paragraph is italic if standfirst.
    """
    if not text or len(text) < 2:
        return render_body(text)

    # Strip leading [BODY] tag if present (shouldn't be here but defensive)
    text = text.strip()
    if text.startswith('[BODY]'):
        text = text[len('[BODY]'):]
    if text.endswith('[/BODY]'):
        text = text[:-len('[/BODY]')]
    text = text.strip()

    # First character for drop cap (skip leading whitespace)
    first_char = text[0]
    rest = text[1:]

    # Drop cap paragraph: w:framePr with dropCap=margin, lines=3
    drop_pid = pid()
    drop_para_xml = (
        f'<w:p w14:paraId="{drop_pid}" w14:textId="{drop_pid}">'
        f'<w:pPr>'
        f'<w:framePr w:dropCap="margin" w:lines="3" w:wrap="around" '
        f'w:vAnchor="text" w:hAnchor="text" w:w="900"/>'
        f'<w:spacing w:before="0" w:after="0" w:line="260" w:lineRule="auto"/>'
        f'<w:rPr><w:position w:val="0"/></w:rPr>'
        f'</w:pPr>'
        f'<w:r><w:rPr>'
        f'<w:rFonts w:ascii="Lora" w:hAnsi="Lora" w:cs="Lora" w:eastAsia="Lora"/>'
        f'<w:b/><w:bCs/>'
        f'<w:position w:val="0"/>'
        f'<w:color w:val="{C["section_purple"]}"/>'
        f'<w:sz w:val="120"/><w:szCs w:val="120"/>'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{esc(first_char)}</w:t>'
        f'</w:r>'
        f'</w:p>'
    )

    # Body paragraph with the rest of text (italic if standfirst)
    inline_runs = parse_inline(rest.lstrip())
    if standfirst:
        # Wrap inline_runs in italic by adding italic color/style override
        # Simplest: re-parse with custom styling - but parse_inline returns runs already.
        # Hack: replace <w:i/> presence flag - actually use a custom rendering
        # For now: render plain with italic via rPr injection -- inject <w:i/> into all rPr blocks
        import re as _re
        inline_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', inline_runs)

    body_pid = pid()
    body_para_xml = (
        f'<w:p w14:paraId="{body_pid}" w14:textId="{body_pid}">'
        f'<w:pPr>'
        f'<w:spacing w:before="50" w:after="50" w:line="260" w:lineRule="auto"/>'
        f'</w:pPr>'
        f'{inline_runs}'
        f'</w:p>'
    )

    return drop_para_xml + "\n" + body_para_xml

def render_body(text):
    """Render a body paragraph with inline tag parsing.
    Auto-strips null bytes and markdown bold artifacts."""
    # Strip content authoring artifacts before parsing
    text = text.replace('\x00', '').replace('**', '')
    inline_xml = parse_inline(text.strip())
    return para(inline_xml, spacing_before=50, spacing_after=50)


def render_divider():
    """Render a gold horizontal divider line for visual separation between topics."""
    rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{C["gold"]}"/></w:pBdr>'
    )
    return para("", ppr_extra=rule_ppr, spacing_before=200, spacing_after=200)



def render_pullquote(content):
    """Render a pull-quote: italic 16pt indigo, gold rule above and below, centered, no bg.
    Used to highlight key insights mid-section. Editorial magazine standard."""
    paras = []

    # Top gold rule
    top_rule_ppr = f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
    paras.append(para("", ppr_extra=top_rule_ppr, spacing_before=160, spacing_after=80))

    # The quote itself: 14pt italic, indigo, centered, indented
    quote_ppr = '<w:ind w:left="720" w:right="720"/>'
    quote_run = run(content.strip(), font="Lato", sz=28, italic=True, color=C["indigo"])
    paras.append(para(quote_run, ppr_extra=quote_ppr, spacing_before=80, spacing_after=80, jc="center"))

    # Bottom gold rule
    bottom_rule_ppr = f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
    zwsp_run = run("\u200B", font="Lato", sz=10, color=C["page_bg"])
    paras.append(para(zwsp_run, ppr_extra=bottom_rule_ppr, spacing_before=80, spacing_after=160))

    return "\n".join(paras)


def render_runin(title, content):
    """Render a run-in heading: bold title + period, then body content on same line.
    Editorial standard for definitions, theorems, minor headings."""
    title_part = title.strip()
    if not title_part.endswith('.'):
        title_part += '.'
    title_run = run(title_part + " ", font="Lato", sz=20, bold=True, color=C["section_purple"])
    # Process body content through inline parser
    body_runs = parse_inline(content.strip())
    # Increased spacing for clearer visual separation between consecutive RUNINs (e.g. Bước 1/2/3 listings)
    return para(title_run + body_runs, spacing_before=200, spacing_after=120)


def render_section_ornament():
    """Render a centered decorative ornament marking section end. Editorial typography."""
    ornament = "\u2756 \u2756 \u2756"  # ❖ ❖ ❖
    orn_run = run(ornament, font="Lato", sz=20, color=C["gold"], letter_spacing=80)
    return para(orn_run, spacing_before=180, spacing_after=180, jc="center")

def render_table(title, header_cells, rows):
    """Render an OOXML table with editorial styling.
    title: optional caption above table
    header_cells: list of column headers
    rows: list of row data (each row is a list of cell strings)
    """
    n_cols = len(header_cells) if header_cells else (max(len(r) for r in rows) if rows else 1)

    parts = []

    # Title above table (if provided)
    if title:
        title_run = run(title, font="Lato", sz=18, italic=True, color=C["muted"], letter_spacing=15)
        parts.append(para(title_run, spacing_before=120, spacing_after=60))

    # Build table
    # Total table width: ~9000 twips (6.25 inches), let cols share equally
    col_w = 9000 // max(n_cols, 1)

    # Table properties: top + bottom gold borders only
    tbl_pr = (
        '<w:tblPr>'
        f'<w:tblW w:w="9000" w:type="dxa"/>'
        '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        f'<w:top w:val="single" w:sz="12" w:space="0" w:color="{C["gold"]}"/>'
        f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="{C["gold"]}"/>'
        '<w:left w:val="nil"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar>'
        '<w:top w:w="60" w:type="dxa"/>'
        '<w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/>'
        '<w:right w:w="100" w:type="dxa"/>'
        '</w:tblCellMar>'
        '</w:tblPr>'
    )

    # Grid
    tbl_grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(n_cols)) + '</w:tblGrid>'

    # Header row
    header_row_xml = ''
    if header_cells:
        cells_xml = ''
        for hc in header_cells:
            # Header cell: indigo bg, white bold text, sz 18 (9pt)
            cell_run = run(hc.strip(), font="Lato", sz=18, bold=True, color="FFFFFF")
            cell_para_xml = para(cell_run, spacing_before=0, spacing_after=0, jc="left")
            tc_pr = (
                f'<w:tcPr>'
                f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{C["section_purple"]}"/>'
                f'<w:tcBorders>'
                f'<w:bottom w:val="single" w:sz="4" w:color="{C["gold"]}"/>'
                f'</w:tcBorders>'
                f'</w:tcPr>'
            )
            cells_xml += f'<w:tc>{tc_pr}{cell_para_xml}</w:tc>'
        header_row_xml = f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{cells_xml}</w:tr>'

    # Data rows with alternating bg
    data_rows_xml = ''
    for ri, row in enumerate(rows):
        bg = "F8F5EE" if ri % 2 == 1 else C["page_bg"]  # subtle alternating
        cells_xml = ''
        for ci in range(n_cols):
            cell_text = row[ci].strip() if ci < len(row) else ''
            # Cell content: process for sub/sup notation
            if cell_text:
                cell_run = render_subscript_text(cell_text, font="Lato", sz=18, color=C["body"])
            else:
                cell_run = run("", font="Lato", sz=18, color=C["body"])
            cell_para_xml = para(cell_run, spacing_before=0, spacing_after=0)
            tc_pr = (
                f'<w:tcPr>'
                f'<w:tcW w:w="{col_w}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>'
                f'</w:tcPr>'
            )
            cells_xml += f'<w:tc>{tc_pr}{cell_para_xml}</w:tc>'
        data_rows_xml += f'<w:tr>{cells_xml}</w:tr>'

    table_xml = f'<w:tbl>{tbl_pr}{tbl_grid}{header_row_xml}{data_rows_xml}</w:tbl>'
    parts.append(table_xml)

    # Bottom spacer paragraph
    parts.append(para("", spacing_before=120, spacing_after=0))

    return "\n".join(parts)


def _embed_formula_image_para(imgname):
    import os as _os
    path = _os.path.join('formula_imgs', imgname + '.png')
    if not _os.path.exists(path):
        return para(run('[thieu anh: '+imgname+']', font="Lato", sz=18, color=C["muted"]), jc="center")
    n = len(FIGURE_MEDIA) + 1
    FIGURE_MEDIA.append({"n": n, "src": _os.path.abspath(path)})
    dims = _png_size(path) or (1200, 300)
    w_px, h_px = dims
    nat_emu = int(w_px * 4762.5)
    col_emu = 6126480
    cx = min(col_emu, nat_emu)
    cy = int(cx * h_px / w_px) if w_px else col_emu
    rid = f"rIdFig{n}"; docpr_id = 9000 + n
    drawing = ('<w:r><w:rPr/><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Formula {n}"/><wp:cNvGraphicFramePr/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="fmla{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
    return para(drawing, jc="center", spacing_before=60, spacing_after=50)


_OMML_CACHE = {}
def _omml_for_latex(latex):
    """LaTeX -> OMML fragment via Pandoc (cached). Returns <m:oMathPara>... or None."""
    import subprocess, zipfile, re as _re, tempfile, os as _os
    latex = (latex or '').strip()
    if not latex:
        return None
    if latex in _OMML_CACHE:
        return _OMML_CACHE[latex]
    try:
        tmp = tempfile.NamedTemporaryFile(suffix='.docx', delete=False); tmp.close()
        md = '$$' + latex + '$$'
        subprocess.run(['pandoc','-f','markdown','-t','docx','-o',tmp.name],
                       input=md.encode('utf-8'), capture_output=True, timeout=30)
        with zipfile.ZipFile(tmp.name) as z:
            x = z.read('word/document.xml').decode('utf-8')
        _os.unlink(tmp.name)
        m = _re.search(r'<m:oMathPara>.*?</m:oMathPara>', x, _re.S) or _re.search(r'<m:oMath>.*?</m:oMath>', x, _re.S)
        frag = m.group(0) if m else None
        _OMML_CACHE[latex] = frag
        return frag
    except Exception:
        return None

def _colorize_omml(frag, var_color_map):
    """Color variable glyphs inside an OMML fragment to match the legend colors,
    while keeping it an editable Word equation. Pandoc emits one <m:r> per char,
    so we greedily match where-section variable signatures against the run stream.
    Operators, constants, and unmatched glyphs stay black; injection is a no-op
    when nothing matches, so a bad match never corrupts the equation."""
    if not frag or not var_color_map:
        return frag
    import re as _re
    _GREEK = {'\\pi':'π','\\sigma':'σ','\\mu':'μ','\\rho':'ρ','\\theta':'θ',
              '\\beta':'β','\\alpha':'α','\\lambda':'λ','\\gamma':'γ','\\delta':'δ',
              '\\tau':'τ','\\omega':'ω','\\phi':'φ','\\epsilon':'ε'}
    def _sig(name):
        s = name
        for k,v in _GREEK.items(): s = s.replace(k, v)
        s = _re.sub(r'\\(dot|bar|hat|tilde|vec|overline|mathrm|mathbf|text)\b','',s)
        s = _re.sub(r'\\(left|right|,|;| )','',s)
        s = _re.sub(r'[{}()\[\]\\^_,.\s]','',s)
        return tuple(s)
    sigs = []
    for name,hexc in var_color_map.items():
        t = _sig(name)
        if t: sigs.append((t,hexc))
    sigs.sort(key=lambda x:-len(x[0]))
    runs = list(_re.finditer(
        r'<m:r>(?:<m:rPr>.*?</m:rPr>)?(?:<w:rPr>.*?</w:rPr>)?<m:t[^>]*>(.*?)</m:t></m:r>',
        frag, _re.S))
    if not runs: return frag
    chars = [m.group(1) for m in runs]
    colors = [None]*len(chars)
    _LET = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZπσμρθβαλγδτωφεΠΣ')
    _SKIP = set('=+-−×·*/()[].,;:    ')
    i=0; n=len(chars)
    while i<n:
        if chars[i] in _LET:
            matched=None
            for t,hexc in sigs:
                j=i; k=0; idxs=[]
                while k<len(t) and j<n:
                    if chars[j]==t[k]:
                        idxs.append(j); j+=1; k+=1
                    elif chars[j] in _SKIP and idxs:
                        j+=1
                    else:
                        break
                if k==len(t):
                    matched=(idxs,hexc); break
            if matched:
                for idx in matched[0]: colors[idx]=matched[1]
                i=matched[0][-1]+1; continue
        i+=1
    out=[]
    for mi,m in enumerate(runs):
        if colors[mi] and '<w:rPr>' not in m.group(0):
            colored=_re.sub(r'(<m:r>(?:<m:rPr>.*?</m:rPr>)?)',
                            r'\1<w:rPr><w:color w:val="%s"/></w:rPr>'%colors[mi],
                            m.group(0), count=1, flags=_re.S)
            out.append((m.start(),m.end(),colored))
    res=frag
    for st,en,colored in sorted(out, reverse=True):
        res=res[:st]+colored+res[en:]
    return res

def _embed_formula_omml_para(latex, var_color_map=None):
    frag = _omml_for_latex(latex)
    if not frag:
        return None
    if var_color_map:
        frag = _colorize_omml(frag, var_color_map)
    return para(frag, jc="center", spacing_before=60, spacing_after=50)

def render_formula(content, name=None):
    """
    Render a FORMULA block. Academic textbook style (Hull/Fabozzi):
    - No colored background, no left border accent
    - Whitespace and indentation only to signal formula territory
    - Thin gold rules above and below as delimiters
    - Color-coded variables with proper subscripts in the formula line
    - Legend entries indented, matching variable colors

    Expected format:
        WACC = w_d * r_d * (1 - t) + w_p * r_p + w_e * r_e
        where:
        w_d = weight of debt | trong so no vay
        r_d = pre-tax cost of debt | chi phi no truoc thue
    """
    # Normalize bare greek/function words to glyphs so SDE-style markup
    # ("dr = a(b - r) dt + sigma sqrt(r) dW") renders symbols, not words.
    # Applied to the WHOLE block (formula lines + where lines) so the
    # var_color_map keys stay consistent with the displayed tokens.
    _GREEK_WORDS = [
        ('sigma', 'σ'), ('theta', 'θ'), ('rho', 'ρ'), ('lambda', 'λ'),
        ('gamma', 'γ'), ('alpha', 'α'), ('beta', 'β'), ('delta', 'δ'),
        ('epsilon', 'ε'), ('omega', 'ω'), ('phi', 'φ'), ('mu', 'μ'), ('tau', 'τ'),
        ('Sigma', 'Σ'), ('Theta', 'Θ'), ('Gamma', 'Γ'), ('Delta', 'Δ'),
        ('Omega', 'Ω'), ('Phi', 'Φ'), ('Pi', 'Π'),
    ]
    for _w, _g in _GREEK_WORDS:
        # (?<!\\) so bare words become glyphs, but LaTeX commands (\sigma) stay intact for Pandoc->OMML.
        content = re.sub(rf'(?<!\\)\b{_w}\b', _g, content)
    content = re.sub(r'(?<!\\)\bsqrt\s*\(', '√(', content)

    lines = content.strip().split('\n')
    paras = []

    # Formula content: deep indent only, no background shading
    formula_ppr = f'<w:ind w:left="720" w:right="360"/>'

    # Split into formula line(s) and where-section
    formula_lines = []
    where_lines = []
    in_where = False
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith('where:') or stripped.lower() == 'where':
            in_where = True
            continue
        if in_where:
            if stripped:
                where_lines.append(stripped)
        else:
            if stripped:
                formula_lines.append(stripped)

    # Build color map from where-section variables
    # Supports both simple (w_d) and braced (l_{t,s}, \theta_{t,s}) variable names
    var_color_map = {}
    color_idx = 0
    for wl in where_lines:
        m = re.match(r'^((?:\\[A-Za-z]+)?[A-Za-z\u0370-\u03FF]*(?:\([A-Za-z]\))?(?:_\{[^}]+\}|_[A-Za-z0-9]+)?(?:\^\{[^}]+\}|\^[A-Za-z0-9]+)?)\s*=', wl)
        if m:
            var_name = m.group(1).strip()
            if var_name and var_name not in var_color_map and color_idx < len(FORMULA_VAR_COLORS):
                var_color_map[var_name] = FORMULA_VAR_COLORS[color_idx]
                color_idx += 1

    # Thin gold top rule - signals entry into formula territory
    top_rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
    )
    paras.append(para("", ppr_extra=top_rule_ppr, spacing_before=120, spacing_after=60))

    # Render main formula: uu tien anh typeset formula_imgs/{name}.png (LaTeX -> PNG qua prep script);
    # fallback @name directive; fallback cuoi cung render LaTeX line nhu text mau.
    import os as _osf
    for fl in formula_lines:
        _fls = fl.strip()
        _m_img = re.match(r'^@(\S+)', _fls)
        if _m_img:
            paras.append(_embed_formula_image_para(_m_img.group(1)))
            continue
        _omml = _embed_formula_omml_para(_fls, var_color_map)   # best-of-both: editable OMML + colored vars
        if _omml is not None:
            paras.append(_omml)
        else:
            formula_runs = _render_formula_line_colored(_fls, var_color_map)
            paras.append(para(formula_runs, ppr_extra=formula_ppr, spacing_before=60, spacing_after=40, jc="center"))

    # Legend: gom moi entry vao MOT para, ngan bang dau cham -> Word tu wrap = flow packing
    _leg = ""
    _sep = run("    \u00B7    ", font="Lato", sz=15, color=C["muted"])
    _fv = True
    for wl in where_lines:
        m = re.match(r'^((?:\\[A-Za-z]+)?[A-Za-z\u0370-\u03FF]*(?:\([A-Za-z]\))?(?:_\{[^}]+\}|_[A-Za-z0-9]+)?(?:\^\{[^}]+\}|\^[A-Za-z0-9\*]+)?)\s*=\s*(.+)$', wl)
        if not m: continue
        var_name = m.group(1).strip(); description = m.group(2).strip()
        var_color = var_color_map.get(var_name, C["body"])
        vr = render_subscript_colored(var_name, color=var_color, font=ACTIVE_FONTS.get("display","Lora"), sz=16, bold=True)
        er = run(" = ", font="Lato", sz=16, color=C["secondary"])
        eng = description.split('|',1)[0].strip()
        dr = render_subscript_text(eng, font="Lato", sz=16, color=C["secondary"])
        if not _fv: _leg += _sep
        _leg += vr + er + dr; _fv = False
    if _leg:
        paras.append(para(_leg, ppr_extra=formula_ppr, spacing_before=30, spacing_after=20))

    # Thin gold bottom rule - signals exit from formula territory
    # Use a zero-width space run to prevent Word from collapsing the empty paragraph
    bottom_rule_ppr = (
        f'<w:pBdr><w:top w:val="single" w:sz="4" w:space="6" w:color="{C["gold"]}"/></w:pBdr>'
    )
    zwsp_run = run("\u200B", font="Lato", sz=10, color=C["page_bg"])  # invisible spacer
    paras.append(para(zwsp_run, ppr_extra=bottom_rule_ppr, spacing_before=60, spacing_after=120))

    return "\n".join(paras)


def _render_formula_line_colored(formula_text, var_color_map):
    """Render a formula line with color-coded variables, proper sub/superscripts, and math symbols.

    Supports braced subscript/superscript: l_{t,s}, P_{t+1}^{n}, \\theta_{t,s}, etc.
    Greek aliases (\\theta, \\pi, etc.) are resolved by render_subscript_text.
    """
    # Preprocess LaTeX commands with arguments BEFORE tokenization
    formula_text = _preprocess_latex_commands(formula_text)

    runs_xml = ""

    # Manual tokenizer with proper brace matching for nested {...} support
    def _tokenize_formula(s):
        """Tokenize formula, handling nested braces in sub/superscripts.
        Returns list of token strings."""
        def _match_brace(s, start):
            """Find matching close brace for { at start. Returns end index after }, or -1."""
            if start >= len(s) or s[start] != '{':
                return -1
            depth = 1
            i = start + 1
            while i < len(s):
                if s[i] == '{':
                    depth += 1
                elif s[i] == '}':
                    depth -= 1
                    if depth == 0:
                        return i + 1
                i += 1
            return -1

        def _consume_subsup(s, start):
            """If s[start:] starts with _{...} or _xyz or ^{...} or ^xyz, return (consumed_text, new_pos).
            Otherwise (None, start)."""
            if start >= len(s):
                return None, start
            ch = s[start]
            if ch not in '_^':
                return None, start
            i = start + 1
            if i < len(s) and s[i] == '{':
                close = _match_brace(s, i)
                if close > 0:
                    return s[start:close], close
                return None, start
            else:
                # Simple sub/sup: optional minus, then alphanumeric or *
                j = i
                if j < len(s) and s[j] == '-':
                    j += 1
                arg_start = j
                while j < len(s) and (s[j].isalnum() or s[j] == '*'):
                    j += 1
                if j > arg_start:
                    return s[start:j], j
                return None, start

        tokens = []
        pos = 0
        n = len(s)

        # Patterns for base tokens (without sub/super attached yet)
        backslash_word_re = re.compile(r'\\[A-Za-z]+')
        word_re = re.compile(r'[A-Za-z\u0370-\u03FF\u221A]+')
        number_re = re.compile(r'[0-9]+\.?[0-9]*')
        space_re = re.compile(r'\s+')

        while pos < n:
            ch = s[pos]
            base_token = None
            base_end = pos

            # Try backslash word (Greek/command not yet replaced)
            m = backslash_word_re.match(s, pos)
            if m:
                base_token = m.group(0)
                base_end = m.end()
            else:
                m = word_re.match(s, pos)
                if m:
                    base_token = m.group(0)
                    base_end = m.end()
                else:
                    m = number_re.match(s, pos)
                    if m:
                        tokens.append(m.group(0))
                        pos = m.end()
                        continue
                    m = space_re.match(s, pos)
                    if m:
                        tokens.append(m.group(0))
                        pos = m.end()
                        continue
                    # Single operator/symbol char
                    tokens.append(s[pos])
                    pos += 1
                    continue

            # Have base_token; look for optional subscript and/or superscript
            attach = ''
            scan = base_end
            sub, new_pos = _consume_subsup(s, scan)
            if sub is not None and sub.startswith('_'):
                attach += sub
                scan = new_pos
            sup, new_pos = _consume_subsup(s, scan)
            if sup is not None and sup.startswith('^'):
                attach += sup
                scan = new_pos
            # Allow super-then-sub order too
            if not attach.startswith('_'):
                # We may have caught super before sub; try sub again
                sub2, new_pos2 = _consume_subsup(s, scan)
                if sub2 is not None and sub2.startswith('_'):
                    attach += sub2
                    scan = new_pos2

            tokens.append(base_token + attach)
            pos = scan

        return tokens

    tokens = _tokenize_formula(formula_text)

    for _ti, token in enumerate(tokens):
        if not token:
            continue

        # Strip sub/super for var_color_map lookup: "l_{t,s}" -> "l_{t,s}", "w_d" -> "w_d"
        base_for_lookup = token.split('_')[0].split('^')[0] if ('_' in token or '^' in token) else token
        full_token_lookup = token  # also try full match

        # Check var_color_map: try full token first, then base only
        if full_token_lookup in var_color_map:
            runs_xml += render_subscript_colored(token, color=var_color_map[full_token_lookup], font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, bold=True)
        elif base_for_lookup in var_color_map:
            runs_xml += render_subscript_colored(token, color=var_color_map[base_for_lookup], font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, bold=True)
        # Has subscript/superscript notation
        elif '_' in token or '^' in token or '\\' in token:
            runs_xml += render_subscript_colored(token, color=C["indigo"], font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, bold=True)
        # Multi-letter word not in map
        elif re.match(r'^[A-Za-z\u0370-\u03FF]+$', token) and len(token) > 1:
            runs_xml += run(token, font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, bold=True, color=C["section_purple"])
        # Single letter not in map
        elif re.match(r'^[A-Za-z\u0370-\u03FF]$', token):
            runs_xml += run(token, font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, bold=True, color=C["secondary"])
        # Whitespace
        elif token.strip() == '':
            runs_xml += run(token, font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, color=C["secondary"])
        # Operators and symbols: auto-convert * to multiplication sign ONLY in binary
        # operator position (an operand follows). Unary/postfix star like Taylor-rule
        # notation "pi*" stays as a literal asterisk (documented pi* -> pi-times bug).
        else:
            display = token
            if token == '*':
                _next_tok = next((t for t in tokens[_ti + 1:] if t and t.strip()), None)
                if _next_tok is not None and (_next_tok[0].isalnum() or _next_tok[0] in '([{\\'):
                    display = '\u00d7'
            runs_xml += run(display, font=ACTIVE_FONTS.get("mono", "Lato"), sz=26, color=C["secondary"])

    return runs_xml




def render_intuition(content):
    """Render [INTUITION] block: italic 11pt indigo, gold left rule, no bg.
    Used after a formula to provide intuition explanation."""
    intuit_ppr = (
        f'<w:pBdr><w:left w:val="single" w:sz="16" w:space="12" w:color="{C["gold"]}"/></w:pBdr>'
        f'<w:ind w:left="360"/>'
    )
    label_run = run("Trực giác:  ", font="Lato", sz=18, bold=True, italic=True, color=C["icon_gold"])
    body_runs = parse_inline(content.strip())
    # Make body italic
    import re as _re
    body_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', body_runs)
    return para(label_run + body_runs, ppr_extra=intuit_ppr, spacing_before=80, spacing_after=80)


def render_check(content):
    """Render [CHECK] block: green-tinted box for sanity check after example.
    Format: ✓ Đối chiếu: ..."""
    check_ppr = (
        f'<w:pBdr><w:left w:val="single" w:sz="16" w:space="12" w:color="{C["icon_green"]}"/></w:pBdr>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="EAF4ED"/>'
        f'<w:ind w:left="360" w:right="240"/>'
    )
    label_run = run("\u2713 Đối chiếu.  ", font="Lato", sz=18, bold=True, color=C["icon_green"])
    body_runs = parse_inline(content.strip())
    return para(label_run + body_runs, ppr_extra=check_ppr, spacing_before=60, spacing_after=60)


def render_diagram(diagram_type, params):
    """Render [DIAGRAM] primitives via simple OOXML tables/text shapes.
    diagram_type: timeline, hub, flow, tree2x2, payoff
    params: dict of named params from the markup
    """
    parts = []

    # Caption above
    caption = params.get("title", f"Diagram: {diagram_type}")
    cap_run = run(caption, font="Lato", sz=18, italic=True, color=C["muted"], letter_spacing=15)
    parts.append(para(cap_run, spacing_before=120, spacing_after=80, jc="center"))

    if diagram_type == "timeline":
        # Horizontal timeline: render as 1-row table with N cells, gold dividers
        events = []
        i = 0
        while True:
            key = f"t{i}"
            if key in params:
                events.append((key, params[key]))
                i += 1
            else:
                break
        if events:
            n_cells = len(events)
            cell_w = 9000 // n_cells
            tbl_pr = (
                '<w:tblPr>'
                '<w:tblW w:w="9000" w:type="dxa"/>'
                '<w:jc w:val="center"/>'
                '<w:tblBorders>'
                f'<w:top w:val="single" w:sz="12" w:space="0" w:color="{C["gold"]}"/>'
                f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="{C["gold"]}"/>'
                '<w:left w:val="nil"/><w:right w:val="nil"/>'
                f'<w:insideV w:val="dashed" w:sz="4" w:space="0" w:color="{C["gold"]}"/>'
                '<w:insideH w:val="nil"/>'
                '</w:tblBorders>'
                '<w:tblLayout w:type="fixed"/>'
                '<w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/>'
                '<w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>'
                '</w:tblPr>'
            )
            tbl_grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{cell_w}"/>' for _ in range(n_cells)) + '</w:tblGrid>'
            cells_xml = ''
            for label, val in events:
                # Cell content: bold label on top, regular text below
                lbl_run = run(label, font="Lato", sz=16, bold=True, color=C["section_num_orange"])
                lbl_p = para(lbl_run, spacing_before=0, spacing_after=20, jc="center")
                val_runs = render_subscript_text(val.strip(), font="Lato", sz=18, color=C["body"])
                val_p = para(val_runs, spacing_before=0, spacing_after=0, jc="center")
                tc_pr = f'<w:tcPr><w:tcW w:w="{cell_w}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                cells_xml += f'<w:tc>{tc_pr}{lbl_p}{val_p}</w:tc>'
            tbl_xml = f'<w:tbl>{tbl_pr}{tbl_grid}<w:tr>{cells_xml}</w:tr></w:tbl>'
            parts.append(tbl_xml)

    elif diagram_type == "hub":
        # Center + spokes: render as text with center bold + spokes around
        center_text = params.get("center", "")
        spokes = params.get("spokes", "").split(",")
        spokes = [s.strip() for s in spokes if s.strip()]
        if center_text:
            ctr_run = run(center_text, font="Lato", sz=24, bold=True, color=C["section_purple"], letter_spacing=20)
            parts.append(para(ctr_run, spacing_before=80, spacing_after=120, jc="center"))
        if spokes:
            spoke_text = "  \u2756  ".join(spokes)
            sp_run = run(spoke_text, font="Lato", sz=18, italic=True, color=C["icon_gold"])
            parts.append(para(sp_run, spacing_before=0, spacing_after=120, jc="center"))

    elif diagram_type == "flow":
        # Sequential steps with arrows between
        steps = []
        i = 1
        while True:
            key = f"step{i}"
            if key in params:
                steps.append(params[key])
                i += 1
            else:
                break
        if steps:
            joined = "  \u00BB  ".join(steps)
            run_xml = render_subscript_text(joined, font="Lato", sz=20, color=C["body"])
            ppr = '<w:ind w:left="360" w:right="360"/>'
            parts.append(para(run_xml, ppr_extra=ppr, spacing_before=80, spacing_after=80, jc="center"))

    elif diagram_type == "tree2x2":
        # 2x2 grid (NW, NE, SW, SE)
        cells_data = [(params.get("NW", ""), params.get("NE", "")),
                      (params.get("SW", ""), params.get("SE", ""))]
        cell_w = 4500
        tbl_pr = (
            '<w:tblPr>'
            '<w:tblW w:w="9000" w:type="dxa"/>'
            '<w:jc w:val="center"/>'
            '<w:tblBorders>'
            f'<w:top w:val="single" w:sz="8" w:color="{C["gold"]}"/>'
            f'<w:bottom w:val="single" w:sz="8" w:color="{C["gold"]}"/>'
            f'<w:left w:val="single" w:sz="8" w:color="{C["gold"]}"/>'
            f'<w:right w:val="single" w:sz="8" w:color="{C["gold"]}"/>'
            f'<w:insideH w:val="single" w:sz="6" w:color="{C["gold"]}"/>'
            f'<w:insideV w:val="single" w:sz="6" w:color="{C["gold"]}"/>'
            '</w:tblBorders>'
            '<w:tblLayout w:type="fixed"/>'
            '<w:tblCellMar><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/>'
            '<w:left w:w="180" w:type="dxa"/><w:right w:w="180" w:type="dxa"/></w:tblCellMar>'
            '</w:tblPr>'
        )
        tbl_grid = f'<w:tblGrid><w:gridCol w:w="{cell_w}"/><w:gridCol w:w="{cell_w}"/></w:tblGrid>'
        rows_xml = ''
        for row_pair in cells_data:
            cells_xml = ''
            for cell_text in row_pair:
                cell_runs = render_subscript_text(cell_text.strip(), font="Lato", sz=18, color=C["body"])
                cell_p = para(cell_runs, spacing_before=0, spacing_after=0, jc="center")
                tc_pr = f'<w:tcPr><w:tcW w:w="{cell_w}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                cells_xml += f'<w:tc>{tc_pr}{cell_p}</w:tc>'
            rows_xml += f'<w:tr>{cells_xml}</w:tr>'
        parts.append(f'<w:tbl>{tbl_pr}{tbl_grid}{rows_xml}</w:tbl>')

    elif diagram_type == "payoff":
        # Simple text representation of payoff diagram parameters
        otype = params.get("type", "long_call")
        strike = params.get("strike", "X")
        text = f"Payoff: {otype} at strike {strike}"
        run_xml = render_subscript_text(text, font="Lato", sz=20, italic=True, color=C["secondary"])
        parts.append(para(run_xml, spacing_before=80, spacing_after=80, jc="center"))

    else:
        # Fallback: try render_engine_extras registry (matrix2x3, pyramid, cycle, comparison, gauge)
        try:
            # Lazy import to avoid circular dep at module load
            from render_engine_extras import DIAGRAM_REGISTRY as _EXTRAS_REGISTRY
            if diagram_type in _EXTRAS_REGISTRY:
                extra_xml = _EXTRAS_REGISTRY[diagram_type](params)
                parts.append(extra_xml)
            else:
                sys.stderr.write(f"WARN: Unknown DIAGRAM type '{diagram_type}'\n")
        except ImportError:
            sys.stderr.write(f"WARN: render_engine_extras not available, skipping DIAGRAM '{diagram_type}'\n")

    # Trailing space
    parts.append(para("", spacing_before=80, spacing_after=0))
    return "\n".join(parts)







def render_epigraph(source, content):
    """Render [EPIGRAPH] block: italic quote with attribution before section.
    Editorial chapter epigraph (Tầng I.4)."""
    parts = []

    # Indent + italic quote
    epi_ppr = '<w:ind w:left="2400" w:right="600"/>'
    quote_runs = parse_inline(content.strip())
    import re as _re
    quote_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', quote_runs)
    parts.append(para(quote_runs, ppr_extra=epi_ppr, spacing_before=120, spacing_after=40))

    # Source attribution (no em-dash, just italic gold + comma indent)
    if source:
        attr_ppr = '<w:ind w:left="2400" w:right="600"/>'
        attr_run = run(f", {source.strip()}", font="Lato", sz=16, italic=True,
                       color=C["icon_gold"], letter_spacing=15)
        parts.append(para(attr_run, ppr_extra=attr_ppr, spacing_before=0, spacing_after=160, jc="right"))

    return "\n".join(parts)



def render_foldout(content):
    """Render [FOLDOUT] block: indicate page should be landscape orientation.
    For diagrams/timelines that need wider layout. Adds section break with landscape orientation."""
    parts = []

    # Section break to landscape, render content, section break back
    # OOXML: w:sectPr with w:pgSz w:orient="landscape"

    # Indicator paragraph (small italic)
    note_run = run("[Foldout: landscape orientation]", font="Lato", sz=14, italic=True, color=C["muted"])
    parts.append(para(note_run, spacing_before=120, spacing_after=80, jc="center"))

    # Content (could be a diagram, timeline, or rich content)
    content_runs = parse_inline(content.strip())
    parts.append(para(content_runs, spacing_before=80, spacing_after=80))

    return "\n".join(parts)

def render_quote(source, content):
    """Render block quote with editorial styling: italic body, decorative " marks, gold attribution."""
    parts = []

    # Opening decorative quote mark (large, gold)
    open_q_run = run("\u201C", font=ACTIVE_FONTS.get("display", "Lora"), sz=72, color=C["icon_gold"])
    parts.append(para(open_q_run, spacing_before=80, spacing_after=0, jc="left"))

    # Content (italic, indented)
    quote_ppr = '<w:ind w:left="720" w:right="720"/>'
    content_runs = parse_inline(content.strip())
    # Make italic
    import re as _re
    content_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', content_runs)
    parts.append(para(content_runs, ppr_extra=quote_ppr, spacing_before=0, spacing_after=40))

    # Attribution
    if source:
        attr_run = run(f"  {source.strip()}", font="Lato", sz=18, italic=True, color=C["icon_gold"], letter_spacing=15)
        parts.append(para(attr_run, ppr_extra=quote_ppr, spacing_before=0, spacing_after=80, jc="right"))

    return "\n".join(parts)



def render_margin(margin_type, content):
    """Render [MARGIN: type=note|tip|ref] as a 2-cell table for better cross-viewer support.
    Left cell empty (body filler), right cell margin annotation.
    Italic 8pt, muted color, small width on right.
    """
    type_colors = {
        'note': C["muted"],
        'tip': C["icon_gold"],
        'ref': C["icon_blue"],
    }
    type_labels = {
        'note': "Ghi chú",
        'tip': "Mẹo",
        'ref': "Tham chiếu",
    }
    color = type_colors.get(margin_type, C["muted"])
    label_text = type_labels.get(margin_type, "Note")

    # Build 2-cell table: left empty (≈70% width), right margin content (≈30%)
    left_w = 6300
    right_w = 2700

    tbl_pr = (
        '<w:tblPr>'
        f'<w:tblW w:w="{left_w + right_w}" w:type="dxa"/>'
        '<w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="nil"/><w:bottom w:val="nil"/>'
        '<w:left w:val="nil"/><w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/><w:insideV w:val="nil"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:bottom w:w="40" w:type="dxa"/>'
        '<w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        '</w:tblPr>'
    )
    tbl_grid = f'<w:tblGrid><w:gridCol w:w="{left_w}"/><w:gridCol w:w="{right_w}"/></w:tblGrid>'

    # Left cell: empty paragraph
    left_p = para("", spacing_before=0, spacing_after=0)
    left_tc_pr = f'<w:tcPr><w:tcW w:w="{left_w}" w:type="dxa"/></w:tcPr>'

    # Right cell: label + content
    label_run = run(label_text.upper(), font="Lato", sz=14, bold=True, italic=True,
                    color=color, letter_spacing=20)
    content_runs = parse_inline(content.strip())
    import re as _re
    content_runs = _re.sub(r'<w:rPr>(?!.*<w:i/>)', '<w:rPr><w:i/><w:iCs/>', content_runs)

    label_p = para(label_run, ppr_extra=f'<w:pBdr><w:left w:val="single" w:sz="8" w:space="6" w:color="{color}"/></w:pBdr><w:ind w:left="100"/>',
                   spacing_before=0, spacing_after=20)
    content_p = para(content_runs, ppr_extra=f'<w:pBdr><w:left w:val="single" w:sz="8" w:space="6" w:color="{color}"/></w:pBdr><w:ind w:left="100"/>',
                     spacing_before=0, spacing_after=0)

    right_tc_pr = f'<w:tcPr><w:tcW w:w="{right_w}" w:type="dxa"/></w:tcPr>'

    rows_xml = (
        f'<w:tr>'
        f'<w:tc>{left_tc_pr}{left_p}</w:tc>'
        f'<w:tc>{right_tc_pr}{label_p}{content_p}</w:tc>'
        f'</w:tr>'
    )

    table_xml = f'<w:tbl>{tbl_pr}{tbl_grid}{rows_xml}</w:tbl>'

    # Spacer paragraph after
    spacer = para("", spacing_before=0, spacing_after=80)

    return table_xml + "\n" + spacer

def render_section_open(why_now, preview):
    """Render [SECTION_OPEN] block: italic standfirst with why_now + preview lines.
    Forces narrative bridge convention from caithien.md Tầng 4.4."""
    parts = []

    # User feedback: bỏ bar gold + chung 1 format duy nhất cho toàn pre-text.
    # Đã có why_now thì SKIP preview (thừa, lặp ý).
    # Toàn bộ pre-text: cùng size 11pt, cùng màu secondary, italic, indent.
    open_ppr = '<w:ind w:left="360" w:right="360"/>'

    # User feedback: render math (F_0(T)) trong pre-text + giảm size từ 11pt (sz=22) xuống 10pt (sz=20)
    def _pretext_runs(txt):
        """Token-aware: math tokens (có _ ^ \) qua subscript renderer Consolas; còn lại Inter italic."""
        if not ('_' in txt or '^' in txt or '\\' in txt):
            return run(txt, font="Lato", sz=20, italic=True, color=C["secondary"])
        out = ""
        for tok in re.split(r'(\s+)', txt):
            if not tok:
                continue
            if tok.isspace():
                out += run(tok, font="Lato", sz=20, italic=True, color=C["secondary"])
            elif '_' in tok or '^' in tok or '\\' in tok:
                out += render_subscript_text(tok, font=ACTIVE_FONTS.get("mono", "Lato"), sz=20, color=C["secondary"], bold=False)
            else:
                out += run(tok, font="Lato", sz=20, italic=True, color=C["secondary"])
        return out

    if why_now:
        parts.append(para(_pretext_runs(why_now.strip()), ppr_extra=open_ppr,
                          spacing_before=120, spacing_after=160))
    elif preview:
        parts.append(para(_pretext_runs(preview.strip()), ppr_extra=open_ppr,
                          spacing_before=120, spacing_after=160))

    return "\n".join(parts)


def render_recap_handoff(recap, handoff):
    """Render [RECAP_HANDOFF] block: 2 italic lines marking section end → next section."""
    parts = []

    if recap:
        recap_run = run(recap.strip(), font="Lato", sz=20, italic=True, color=C["secondary"])
        parts.append(para(recap_run, spacing_before=120, spacing_after=40))

    if handoff:
        # Handoff in gold italic for visual contrast
        handoff_run = run(handoff.strip(), font="Lato", sz=20, italic=True, color=C["icon_gold"])
        parts.append(para(handoff_run, spacing_before=0, spacing_after=120))

    return "\n".join(parts)

def render_box_key(content):
    # Strip content artifacts
    if isinstance(content, str):
        content = content.replace('\x00', '').replace('**', '')
    """Render BOX_KEY as a Bloomberg/McKinsey pull quote:
    - No background (transparent)
    - Gold rule above and below (thin, like the formula delimiter style)
    - Small centered label in gold ALL CAPS, slightly letter-spaced
    - Content indented at 11pt (slightly larger than body), gold color cues, italic
    This creates visual weight without the 'box' feeling that clutters the page.
    """
    paras = []
    GOLD = C["gold"]
    DARK_GOLD = C["icon_gold"]

    # Top gold rule (invisible spacer paragraph with a bottom border = visual top line)
    top_rule_ppr = (
        f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="6" w:color="{GOLD}"/></w:pBdr>'
    )
    zwsp_top = run("\u200B", font="Lato", sz=10, color=C["page_bg"])
    paras.append(para(zwsp_top, ppr_extra=top_rule_ppr, spacing_before=120, spacing_after=0))

    # Small centered label: ĐIỂM MẤU CHỐT in dark gold, 8pt, letter-spaced, centered
    label_ppr = f'<w:jc w:val="center"/><w:ind w:left="720" w:right="720"/>'
    label_run = run(
        BOX_SPECS["BOX_KEY"]["label"],
        font="Lato", sz=16, bold=True, color=DARK_GOLD, letter_spacing=30
    )
    paras.append(para(label_run, ppr_extra=label_ppr, spacing_before=60, spacing_after=40))

    # Content paragraphs: centered, indented, italic deep-muted 11pt (sz=22)
    # parse_inline handles inline tags; plain text gets the pull-quote override via
    # a small helper that renders at slightly larger size and secondary color
    def _pq_plain(text):
        """Plain-text runs for pull quote: 11pt italic Inter, secondary color.
        Math like 'r_c = 1.98%' routes through subscript renderer (Consolas, no italic).
        Mixed lines split by whitespace; math tokens detected by '_' or '^' or '\\'."""
        # Token-level: split into space-separated tokens, route each to math vs prose
        if "_" in text or "^" in text or "\\" in text:
            tokens = re.split(r'(\s+)', text)
            out = ""
            for tok in tokens:
                if not tok:
                    continue
                if tok.isspace():
                    out += run(tok, font="Lato", sz=22, italic=True, color=C["secondary"])
                elif "_" in tok or "^" in tok or "\\" in tok:
                    out += render_subscript_text(tok, font=ACTIVE_FONTS.get("mono", "Lato"), sz=22, color=C["secondary"], bold=False)
                else:
                    out += run(tok, font="Lato", sz=22, italic=True, color=C["secondary"], letter_spacing=10)
            return out
        return run(text, font="Lato", sz=22, italic=True, color=C["secondary"], letter_spacing=10)

    def _pq_inline(text):
        """Wrap parse_inline but apply pull-quote styling to bare text segments."""
        # Fast path: no tags -> styled run with subscript handling
        if "[" not in text:
            return _pq_plain(text)
        return parse_inline(text)

    content_ppr = f'<w:jc w:val="center"/><w:ind w:left="720" w:right="720"/>'
    content_paragraphs = re.split(r'\n\n+', content.strip())
    for cp in content_paragraphs:
        cp = cp.strip()
        if not cp:
            continue
        lines = cp.split('\n')
        if len(lines) == 1:
            inline_xml = _pq_inline(cp)
        else:
            parts = []
            for j, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                if j > 0:
                    parts.append(run_break())
                parts.append(_pq_inline(line))
            inline_xml = "".join(parts)
        paras.append(para(inline_xml, ppr_extra=content_ppr, spacing_before=20, spacing_after=20))

    # Bottom gold rule (paragraph with a top border = visual bottom line)
    bottom_rule_ppr = (
        f'<w:pBdr><w:top w:val="single" w:sz="6" w:space="6" w:color="{GOLD}"/></w:pBdr>'
    )
    zwsp_bottom = run("\u200B", font="Lato", sz=10, color=C["page_bg"])
    paras.append(para(zwsp_bottom, ppr_extra=bottom_rule_ppr, spacing_before=0, spacing_after=120))

    return "\n".join(paras)


def render_box_purple(content):
    # Strip content artifacts
    if isinstance(content, str):
        content = content.replace('\x00', '').replace('**', '')
    """Render BOX_PURPLE as a minimal visual suggestion annotation.
    No background, no border — just a small purple label followed by plain body text.
    This is a note for the reader/designer, not a content box.
    """
    paras = []
    # Small purple label on its own line: "GỢI Ý HÌNH MINH HỌA"
    label_rpr = rpr(font="Lato", sz=16, bold=True, italic=True, color=C["icon_purple"], letter_spacing=20)
    paras.append(para(
        f'<w:r><w:rPr>{label_rpr}</w:rPr><w:t xml:space="preserve">{BOX_SPECS["BOX_PURPLE"]["label"]}</w:t></w:r>',
        spacing_before=120, spacing_after=40
    ))
    # Content as plain muted italic text — strip any [Style] or [Type]/[Layout] etc. markup lines
    content_lines = []
    for line in content.strip().split('\n'):
        # Remove lines that start with a bracket-prefixed label like [Style]:, [Color]:
        stripped = line.strip()
        if re.match(r'^\[(?:Style|Color[^]]*)\]', stripped, re.IGNORECASE):
            continue
        content_lines.append(stripped)
    cleaned = '\n'.join(l for l in content_lines if l)
    if cleaned:
        content_rpr = rpr(font="Lato", sz=18, italic=True, color=C["muted"])
        paras.append(para(
            f'<w:r><w:rPr>{content_rpr}</w:rPr><w:t xml:space="preserve">{esc(cleaned)}</w:t></w:r>',
            spacing_before=0, spacing_after=160
        ))
    return "\n".join(paras)


def render_data_cards(content):
    """Render DATA_CARDS as a horizontal table. Each card has a gold top accent bar,
    SMALL CAPS label, large bold value, and small description line.

    Expected format:
        - label: SHORT LABEL | value: Number or fact | sub: One-line description
        - label: ANOTHER | value: Value | sub: Description
    """
    paras = []
    cards = []
    for line in content.strip().split('\n'):
        line = line.strip().lstrip('-').strip()
        if not line:
            continue
        card = {}
        for part in line.split('|'):
            part = part.strip()
            if part.lower().startswith('label:'):
                card['label'] = part[6:].strip()
            elif part.lower().startswith('value:'):
                card['value'] = part[6:].strip()
            elif part.lower().startswith('sub:'):
                card['sub'] = part[4:].strip()
        if card.get('label') or card.get('value'):
            cards.append(card)

    if not cards:
        return ""

    num_cols = len(cards)
    col_width = 9360 // num_cols  # distribute evenly across text width (12240 - 2*1440 margins)

    # Build table XML
    tbl_xml = (
        '<w:tbl>'
        '<w:tblPr>'
        '<w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '</w:tblBorders>'
        '<w:tblLayout w:type="fixed"/>'
        '</w:tblPr>'
        '<w:tblGrid>'
    )
    for _ in cards:
        tbl_xml += f'<w:gridCol w:w="{col_width}"/>'
    tbl_xml += '</w:tblGrid>'

    # Single row with all cards as cells
    tbl_xml += '<w:tr>'
    for card in cards:
        label = card.get('label', '')
        value = card.get('value', '')
        sub = card.get('sub', '')

        # Cell with gold top border
        cell_xml = (
            '<w:tc>'
            '<w:tcPr>'
            f'<w:tcW w:w="{col_width}" w:type="dxa"/>'
            f'<w:tcBorders>'
            f'<w:top w:val="single" w:sz="16" w:space="0" w:color="{C["gold"]}"/>'
            f'</w:tcBorders>'
            f'<w:tcMar>'
            f'<w:top w:w="140" w:type="dxa"/>'
            f'<w:left w:w="160" w:type="dxa"/>'
            f'<w:bottom w:w="140" w:type="dxa"/>'
            f'<w:right w:w="160" w:type="dxa"/>'
            f'</w:tcMar>'
            '</w:tcPr>'
        )

        # Label: SMALL CAPS, muted, 7.5pt
        label_run = run(label, font="Lato", sz=15, color=C["muted"], small_caps=True, letter_spacing=20)
        cell_xml += para(label_run, spacing_before=0, spacing_after=40)

        # Value: 18pt bold purple
        value_run = run(value, font="Lato", sz=36, bold=True, color=C["section_purple"])
        cell_xml += para(value_run, spacing_before=0, spacing_after=40)

        # Sub: 8.5pt secondary
        if sub:
            sub_run = run(sub, font="Lato", sz=17, color=C["secondary"])
            cell_xml += para(sub_run, spacing_before=0, spacing_after=0)

        cell_xml += '</w:tc>'
        tbl_xml += cell_xml

    tbl_xml += '</w:tr></w:tbl>'

    # Wrap in spacing paragraphs
    paras.append(para("", spacing_before=120, spacing_after=0))
    paras.append(tbl_xml)
    paras.append(para("", spacing_before=0, spacing_after=120))

    return "\n".join(paras)


def render_box(box_type, content, suppress_label=False):
    """Render a content box. Editorial callout style:
    - Per-type light tinted background
    - Left border (3pt vertical rule) in the accent color
    - Letter-spaced label (no emoji icons)
    Auto-strips markdown ** bold + null bytes.
    Auto-detects 'Bổ sung cross-source [Severity]:' prefix and replaces with proper BỔ SUNG label.
    Auto-splits long single-paragraph supplements by sentence into readable chunks.
    """
    # Strip content authoring artifacts
    if isinstance(content, str):
        content = content.replace('\x00', '').replace('**', '')

    # Image-hint auto-detect: a BOX_NOTE carrying a Caption + Prompt pair for external
    # image generation gets the distinct IMAGE_HINT treatment (purple tint, dedicated
    # label) so hints are visually separate from regular GHI CHU BO SUNG notes.
    if (box_type == "BOX_NOTE" and isinstance(content, str)
            and "Caption (ti\u1ebfng Vi\u1ec7t):" in content
            and re.search(r'\bPrompt\b', content)):
        box_type = "IMAGE_HINT"

    # Detect cross-source supplement marker at start of content and strip it.
    # Pattern: "Bổ sung cross-source [Critical]:" or "[Important]" or "[Minor]"
    # We will inject a clean "BỔ SUNG" label paragraph before the box label.
    supplement_severity = None
    if isinstance(content, str):
        m = re.match(r'^\s*B\u1ed5 sung cross-source\s*\[(Critical|Important|Minor)\]\s*:?\s*',
                     content, re.IGNORECASE)
        if m:
            supplement_severity = m.group(1).lower()
            content = content[m.end():].lstrip()

    # Auto-split wall-of-text per paragraph: any individual paragraph > 250 chars
    # gets force-split into smaller chunks for readability. Iterates each paragraph
    # in the existing content and applies sentence-boundary split per paragraph.
    if isinstance(content, str) and len(content) > 200:
        VN_UPPER = 'ĐÂÊÔƠƯÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ'
        existing_paras = re.split(r'\n\n+', content.strip())
        new_paras = []
        for ep in existing_paras:
            ep = ep.strip()
            if len(ep) <= 250:
                if ep:
                    new_paras.append(ep)
                continue
            # Sentence-split this overlong paragraph (parens-depth aware)
            sentences = []
            cur = []
            depth = 0
            j = 0
            while j < len(ep):
                ch = ep[j]
                cur.append(ch)
                if ch in '([{':
                    depth += 1
                elif ch in ')]}':
                    depth = max(0, depth - 1)
                elif ch == '.' and depth == 0:
                    if j + 1 < len(ep) and ep[j+1] == ' ':
                        nxt = ep[j+2:j+4]
                        if nxt and (nxt[0].isupper() or nxt[0] in VN_UPPER):
                            sentences.append(''.join(cur).strip())
                            cur = []
                            j += 2
                            continue
                j += 1
            if cur:
                sentences.append(''.join(cur).strip())
            # Group: each output paragraph = 1-2 sentences, force break at ~150 chars
            if len(sentences) >= 2:
                buf = []
                for s in sentences:
                    buf.append(s)
                    if sum(len(x) for x in buf) >= 150 or len(buf) >= 2:
                        new_paras.append(' '.join(buf))
                        buf = []
                if buf:
                    new_paras.append(' '.join(buf))
            else:
                new_paras.append(ep)
        content = '\n\n'.join(new_paras)

    # BOX_PURPLE: minimal annotation — just purple label + plain text
    if box_type == "BOX_PURPLE":
        return render_box_purple(content)

    # BOX_KEY gets the premium pull-quote treatment
    if box_type == "BOX_KEY":
        return render_box_key(content)

    spec = BOX_SPECS[box_type]
    paras = []
    BOX_BG = spec["bg"]

    # All paragraphs share the same pPr: left border (3pt) + background + indent
    # Invisible same-color top/bottom borders create internal spacing without visible lines
    # w:space="6" keeps left border snug against text (no visible gap)
    box_ppr = (
        f'<w:shd w:val="clear" w:color="auto" w:fill="{BOX_BG}"/>'
        f'<w:pBdr>'
        f'<w:top w:val="single" w:sz="4" w:space="8" w:color="{BOX_BG}"/>'
        f'<w:left w:val="single" w:sz="24" w:space="6" w:color="{spec["accent"]}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="8" w:color="{BOX_BG}"/>'
        f'</w:pBdr>'
        f'<w:ind w:left="200" w:right="200"/>'
    )

    # User feedback: gọi tất cả là "GHI CHÚ" — không phân severity.
    if supplement_severity:
        sup_run = run("GHI CHÚ", font="Lato", sz=16, bold=True, color=C["section_purple"], letter_spacing=30)
        paras.append(para(sup_run, ppr_extra=box_ppr, spacing_before=160, spacing_after=60))
    elif suppress_label:
        # Cluster mode: previous block was same type — skip redundant label,
        # add small spacer to keep visual separation.
        paras.append(para("", ppr_extra=box_ppr, spacing_before=80, spacing_after=20))
    else:
        # Standard box label: bold, letter-spaced, in accent color
        label_run = run(
            spec["label"],
            font="Lato", sz=16, bold=True, color=spec["accent"],
            letter_spacing=20
        )
        paras.append(para(label_run, ppr_extra=box_ppr, spacing_before=160, spacing_after=60))

    # Split on double newlines for separate paragraphs
    content_paragraphs = re.split(r'\n\n+', content.strip())

    def _wrap_math(text):
        """Auto-wrap math expressions in box content for visual emphasis.
        Patterns:
        1. Bracket-formulas: [payoff], [1 + MRR × (y-x) / 360] — common author shorthand.
        2. Tokens with _ subscript (V_0, F_0(T), r_c).
        3. Tokens with ^ superscript (P^n).
        Skip tokens already inside [F]...[/F] or [T:] tags."""
        # Step 1: Convert bare [math-only-bracket] to [F]math[/F].
        # A "math-only" bracket is one whose contents are ASCII math (no Vietnamese letters),
        # so we don't accidentally eat Vietnamese phrases inside brackets.
        def _bracket_to_F(m):
            inside = m.group(1).strip()
            # Heuristic: if inside contains only ASCII math chars + spaces, treat as formula
            if re.fullmatch(r'[A-Za-z0-9_+\-*/().,×÷·≤≥=!|\s]+', inside):
                return f'[F]{inside}[/F]'
            return m.group(0)  # leave as-is
        text = re.sub(r'\[([^\[\]]+)\]', _bracket_to_F, text)

        # Step 2: split by existing [F]/[T:] tags so we don't double-wrap
        parts = re.split(r'(\[F\].*?\[/F\]|\[T:[^\]]+\]+)', text, flags=re.DOTALL)
        out = []
        for part in parts:
            if part.startswith('[F]') or part.startswith('[T:'):
                out.append(part)  # already tagged, skip
                continue
            # Wrap simple math tokens. Pattern: identifier (1-6 chars) + (_ or ^) + arg
            # Examples matched: V_0, F_0(T), r_c, P_t^n, MRR, S_0(1+r)^T
            # We use a conservative regex to avoid false positives in prose.
            def repl(m):
                tok = m.group(0)
                return f'[F]{tok}[/F]'
            # Match math expressions: identifier followed by _ or ^ then args, possibly with parens
            part = re.sub(
                r'(?<![A-Za-z0-9_\\\[])'
                r'([A-Za-z][A-Za-z0-9]{0,10}'
                r'(?:_(?:\{[^}]+\}|[A-Za-z0-9]+))?'
                r'(?:\^(?:\{[^}]+\}|[A-Za-z0-9+\-]+))?'
                r'(?:\([^)]*\))?'
                r')'
                r'(?![A-Za-z0-9_\]])',
                lambda m: f'[F]{m.group(1)}[/F]' if ('_' in m.group(1) or '^' in m.group(1))
                                                  and not m.group(1).startswith('http') else m.group(1),
                part
            )
            out.append(part)
        return ''.join(out)

    for cp in content_paragraphs:
        cp = cp.strip()
        if not cp:
            continue
        cp = _wrap_math(cp)
        # Within each paragraph, single newlines become line breaks
        lines = cp.split('\n')
        if len(lines) == 1:
            inline_xml = parse_inline(cp)
        else:
            parts2 = []
            for j, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                if j > 0:
                    parts2.append(run_break())
                parts2.append(parse_inline(line))
            inline_xml = "".join(parts2)
        paras.append(para(inline_xml, ppr_extra=box_ppr, spacing_before=40, spacing_after=80))

    # Spacer after the box to prevent the last box paragraph from sitting flush against
    # whatever element follows (body text, another box, subsection, etc.)
    paras.append(para("", spacing_before=0, spacing_after=120))

    return "\n".join(paras)


# ===============================================================================
# MARKUP PARSER
# ===============================================================================



def _renumber_inline_refs(blocks, module_num):
    """Auto-renumber 'Công thức N.M' and 'Ví dụ N.M' inline references in body content
    to use module.running convention (n=module_num, m=running counter)."""
    import re as _re

    formula_map = {}  # (orig_n, orig_m) -> running int
    example_map = {}
    formula_counter = 0
    example_counter = 0

    # First pass: scan all blocks in order, build maps.
    # Chain-aware: compound refs ("Công thức 3.1 và 3.2", "Ví dụ 4.1, 4.2") register every
    # N.M in the chain, not just the head. Trailing bare numbers used to keep their original
    # numbering after renumber (documented bug, FI_M3 "Công thức 3.1 và 1.2" mismatch).
    _REF_CHAIN = r'(Công thức|Ví dụ)\s+(\d+)\.(\d+)((?:\s*(?:,|và)\s*\d+\.\d+(?!\d|%))*)'

    def _scan_text(text):
        nonlocal formula_counter, example_counter
        for m in _re.finditer(_REF_CHAIN, text):
            kind = m.group(1)
            pairs = [(int(m.group(2)), int(m.group(3)))]
            for tm in _re.finditer(r'(\d+)\.(\d+)', m.group(4)):
                pairs.append((int(tm.group(1)), int(tm.group(2))))
            for key in pairs:
                if kind == 'Công thức':
                    if key not in formula_map:
                        formula_counter += 1
                        formula_map[key] = formula_counter
                else:
                    if key not in example_map:
                        example_counter += 1
                        example_map[key] = example_counter

    for bt, bd in blocks:
        if isinstance(bd, str):
            _scan_text(bd)
        elif isinstance(bd, tuple):
            for item in bd:
                if isinstance(item, str):
                    _scan_text(item)
        elif isinstance(bd, dict):
            for v in bd.values():
                if isinstance(v, str):
                    _scan_text(v)

    if not formula_map and not example_map:
        return blocks

    def _replace_in_text(text):
        def _chain_replacer(m):
            kind = m.group(1)
            ref_map = formula_map if kind == 'Công thức' else example_map
            def _map_pair(a, b):
                key = (int(a), int(b))
                if key in ref_map:
                    return f"{module_num}.{ref_map[key]}"
                return f"{a}.{b}"
            head = f"{kind} {_map_pair(m.group(2), m.group(3))}"
            tail = _re.sub(r'(\d+)\.(\d+)',
                           lambda tm: _map_pair(tm.group(1), tm.group(2)), m.group(4))
            return head + tail
        return _re.sub(_REF_CHAIN, _chain_replacer, text)

    new_blocks = []
    for bt, bd in blocks:
        if isinstance(bd, str):
            new_blocks.append((bt, _replace_in_text(bd)))
        elif isinstance(bd, tuple):
            new_bd = tuple(_replace_in_text(it) if isinstance(it, str) else it for it in bd)
            new_blocks.append((bt, new_bd))
        elif isinstance(bd, dict):
            new_bd = {k: (_replace_in_text(v) if isinstance(v, str) else v) for k, v in bd.items()}
            new_blocks.append((bt, new_bd))
        else:
            new_blocks.append((bt, bd))
    return new_blocks

def parse_markup(markup_text):
    """
    Parse the markup text into a list of (block_type, data) tuples.
    Block types: COVER, SECTION, SUBSECTION, BODY, BOX_*, FORMULA, DIVIDER, TABLE,
    PULLQUOTE, RUNIN, ORNAMENT, INTUITION, CHECK, DIAGRAM
    Also collects: terms_dict (from [T: term | meaning] first occurrences), formulas list
    """
    blocks = []
    terms_dict = {}
    formulas_list = []
    name_map = {}  # name -> label like "Công thức 2.1" (n=module, m=running counter)
    section_counter = 0
    # Module number for numbering convention; default 1, will be overridden by main()
    module_num_for_numbering = getattr(parse_markup, '_module_num', 1)
    # Numbering mode: 'module' (n=module, m=global running) or 'section' (n=section, m resets)
    numbering_mode = getattr(parse_markup, '_numbering', 'module')
    formula_running = 0  # running counter (whole module, or within section in section mode)
    example_running = 0  # running counter (whole module, or within section in section mode)
    # Extract terms and formulas from text
    import re as _re
    for _m in _re.finditer(r'\[T:\s*([^|\]]+?)\s*\|\s*([^\]]+?)\s*\]', markup_text):
        _t = _m.group(1).strip()
        _meaning = _m.group(2).strip()
        if _t and _t not in terms_dict:
            terms_dict[_t] = _meaning
    for _m in _re.finditer(r'\[FORMULA(?::[^\]]*)?\](.+?)\[/FORMULA\]', markup_text, _re.DOTALL):
        _content = _m.group(1).strip()
        # First non-where line
        for _line in _content.split('\n'):
            _line = _line.strip()
            if _line and not _line.lower().startswith('where'):
                formulas_list.append(_line)
                break

    lines = markup_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # [COVER: subject | title | subtitle | optional hero_prompt=...]
        m = re.match(r'^\[COVER:\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*hero_prompt=(.+?)\s*\]$', line)
        if m:
            blocks.append(("COVER", {"subject": m.group(1), "title": m.group(2), "subtitle": m.group(3), "hero_prompt": m.group(4)}))
            i += 1
            continue
        m = re.match(r'^\[COVER:\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\]$', line)
        if m:
            blocks.append(("COVER", {"subject": m.group(1), "title": m.group(2), "subtitle": m.group(3), "hero_prompt": ""}))
            i += 1
            continue

        # [SECTION: en | brief] (new format) or [SECTION: en | vi: vn | brief] (legacy)
        m = re.match(r'^\[SECTION:\s*(.+?)\s*\|\s*(.+?)\s*\]$', line)
        if m:
            section_counter += 1
            if numbering_mode == 'section':
                formula_running = 0
                example_running = 0
            second_part = m.group(2).strip()
            if second_part.startswith('vi:'):
                m3 = re.match(r'^\[SECTION:\s*(.+?)\s*\|\s*vi:\s*(.+?)\s*\|\s*(.+?)\s*\]$', line)
                if m3:
                    blocks.append(("SECTION", {"en": m3.group(1), "brief": m3.group(3)}))
                else:
                    blocks.append(("SECTION", {"en": m.group(1), "brief": second_part.replace('vi:', '').strip()}))
            else:
                blocks.append(("SECTION", {"en": m.group(1), "brief": second_part}))
            i += 1
            continue

        # [SUBSECTION: en | vi: vn] (legacy format with vi: prefix)
        m = re.match(r'^\[SUBSECTION:\s*(.+?)\s*\|\s*vi:\s*(.+?)\s*\]$', line)
        if m:
            blocks.append(("SUBSECTION", {"en": m.group(1), "vi": m.group(2)}))
            i += 1
            continue

        # [SUBSECTION: en | vn] (new simpler format, no vi: prefix needed)
        m = re.match(r'^\[SUBSECTION:\s*(.+?)\s*\|\s*(.+?)\s*\]$', line)
        if m:
            blocks.append(("SUBSECTION", {"en": m.group(1), "vi": m.group(2)}))
            i += 1
            continue

        # [SUBSECTION: en] (no Vietnamese)
        m = re.match(r'^\[SUBSECTION:\s*(.+?)\s*\]$', line)
        if m:
            blocks.append(("SUBSECTION", {"en": m.group(1), "vi": ""}))
            i += 1
            continue

        # [DIVIDER]
        if line == '[DIVIDER]':
            blocks.append(("DIVIDER", None))
            i += 1
            continue

        # [FIGURE: path | caption]  (viz-factory rendered asset, embedded inline)
        m = re.match(r'^\[FIGURE:\s*(.+?)\s*\|\s*(.+?)\s*\]$', line)
        if m:
            blocks.append(("FIGURE", {"path": m.group(1).strip(), "caption": m.group(2).strip()}))
            i += 1
            continue

        # [VIZ: component | id=N.M.x | caption=... | params={...}]  (viz slot directive,
        # possibly multi-line; rendered as a tinted placeholder strip per MARKER_CONVENTION)
        if line.startswith('[VIZ:'):
            _buf = line
            _depth = _buf.count('[') - _buf.count(']')
            while _depth > 0 and i + 1 < len(lines):
                i += 1
                _buf += ' ' + lines[i].strip()
                _depth = _buf.count('[') - _buf.count(']')
            _comp = re.match(r'^\[VIZ:\s*([A-Za-z0-9_]+)', _buf)
            _vid = re.search(r'\bid=([0-9]+(?:\.[0-9]+)?(?:\.[a-z])?)', _buf)
            _cap = re.search(r'caption=([^|\]]+)', _buf)
            blocks.append(("VIZMARK", {
                "component": _comp.group(1) if _comp else "viz",
                "id": _vid.group(1) if _vid else "?",
                "caption": _cap.group(1).strip() if _cap else "",
            }))
            i += 1
            continue

        # [MARGIN: type=note|tip|ref]content[/MARGIN]
        m_marg = re.match(r'^\[MARGIN:\s*type=(\w+)\](.*?)\[/MARGIN\]', line)
        if m_marg:
            blocks.append(("MARGIN", (m_marg.group(1).strip(), m_marg.group(2).strip())))
            i += 1
            continue
        # Multi-line MARGIN
        m_marg2 = re.match(r'^\[MARGIN:\s*type=(\w+)\](.*)', line)
        if m_marg2 and '[/MARGIN]' not in line:
            mt = m_marg2.group(1).strip()
            mcontent = m_marg2.group(2)
            i += 1
            while i < len(lines):
                if '[/MARGIN]' in lines[i]:
                    mcontent += ' ' + lines[i][:lines[i].index('[/MARGIN]')]
                    break
                mcontent += ' ' + lines[i]
                i += 1
            blocks.append(("MARGIN", (mt, mcontent.strip())))
            i += 1
            continue

        # [FOLDOUT]content[/FOLDOUT]
        if line.startswith('[FOLDOUT]'):
            content = ""
            if '[/FOLDOUT]' in line:
                content = line[len('[FOLDOUT]'):line.index('[/FOLDOUT]')]
                blocks.append(("FOLDOUT", content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/FOLDOUT]' in lines[i]:
                    content += '\n' + lines[i][:lines[i].index('[/FOLDOUT]')]
                    break
                content += '\n' + lines[i]
                i += 1
            blocks.append(("FOLDOUT", content.strip()))
            i += 1
            continue

        # [EPIGRAPH: source]content[/EPIGRAPH]
        m_e = re.match(r'^\[EPIGRAPH(?::\s*(.+?))?\](.*?)\[/EPIGRAPH\]', line)
        if m_e:
            blocks.append(("EPIGRAPH", (m_e.group(1) or "", m_e.group(2).strip())))
            i += 1
            continue
        # Multi-line EPIGRAPH
        m_e2 = re.match(r'^\[EPIGRAPH(?::\s*(.+?))?\](.*)', line)
        if m_e2 and '[/EPIGRAPH]' not in line:
            esrc = m_e2.group(1) or ""
            econtent = m_e2.group(2)
            i += 1
            while i < len(lines):
                if '[/EPIGRAPH]' in lines[i]:
                    econtent += ' ' + lines[i][:lines[i].index('[/EPIGRAPH]')]
                    break
                econtent += ' ' + lines[i]
                i += 1
            blocks.append(("EPIGRAPH", (esrc, econtent.strip())))
            i += 1
            continue

        # [QUOTE: source]content[/QUOTE]
        m_q = re.match(r'^\[QUOTE(?::\s*(.+?))?\](.*?)\[/QUOTE\]', line)
        if m_q:
            blocks.append(("QUOTE", (m_q.group(1) or "", m_q.group(2).strip())))
            i += 1
            continue

        # [SECTION_OPEN]\nwhy_now: ...\npreview: ...\n[/SECTION_OPEN]
        if line.startswith('[SECTION_OPEN]'):
            why_now = ""
            preview = ""
            content_lines = []
            i += 1
            while i < len(lines):
                if '[/SECTION_OPEN]' in lines[i]:
                    break
                content_lines.append(lines[i])
                i += 1
            for cl in content_lines:
                cl = cl.strip()
                if cl.lower().startswith('why_now:'):
                    why_now = cl[len('why_now:'):].strip()
                elif cl.lower().startswith('preview:'):
                    preview = cl[len('preview:'):].strip()
            pass  # SECTION_OPEN device removed (AI-cringe "VÌ SAO BÂY GIỜ"); block consumed, NOT rendered
            i += 1
            continue

        # [RECAP_HANDOFF]\nrecap: ...\nhandoff: ...\n[/RECAP_HANDOFF]
        if line.startswith('[RECAP_HANDOFF]'):
            recap = ""
            handoff = ""
            content_lines = []
            i += 1
            while i < len(lines):
                if '[/RECAP_HANDOFF]' in lines[i]:
                    break
                content_lines.append(lines[i])
                i += 1
            for cl in content_lines:
                cl = cl.strip()
                if cl.lower().startswith('recap:'):
                    recap = cl[len('recap:'):].strip()
                elif cl.lower().startswith('handoff:'):
                    handoff = cl[len('handoff:'):].strip()
            blocks.append(("RECAP_HANDOFF", (recap, handoff)))
            i += 1
            continue

        # [FOOTNOTE]content[/FOOTNOTE]
        if line.startswith('[FOOTNOTE]'):
            content = ""
            if '[/FOOTNOTE]' in line:
                content = line[len('[FOOTNOTE]'):line.index('[/FOOTNOTE]')]
                blocks.append(("FOOTNOTE", content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/FOOTNOTE]' in lines[i]:
                    content += ' ' + lines[i][:lines[i].index('[/FOOTNOTE]')]
                    break
                content += ' ' + lines[i]
                i += 1
            blocks.append(("FOOTNOTE", content.strip()))
            i += 1
            continue

        # [INTUITION]content[/INTUITION]
        if line.startswith('[INTUITION]'):
            content = ""
            if '[/INTUITION]' in line:
                content = line[len('[INTUITION]'):line.index('[/INTUITION]')]
                blocks.append(("INTUITION", content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/INTUITION]' in lines[i]:
                    content += ' ' + lines[i][:lines[i].index('[/INTUITION]')]
                    break
                content += ' ' + lines[i]
                i += 1
            blocks.append(("INTUITION", content.strip()))
            i += 1
            continue

        # [CHECK]content[/CHECK]
        if line.startswith('[CHECK]'):
            content = ""
            if '[/CHECK]' in line:
                content = line[len('[CHECK]'):line.index('[/CHECK]')]
                blocks.append(("CHECK", content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/CHECK]' in lines[i]:
                    content += ' ' + lines[i][:lines[i].index('[/CHECK]')]
                    break
                content += ' ' + lines[i]
                i += 1
            blocks.append(("CHECK", content.strip()))
            i += 1
            continue

        # [DIAGRAM: type | param=val | param=val | ...]
        m_diag = re.match(r'^\[DIAGRAM:\s*(\w+)\s*\|\s*(.+?)\]$', line)
        if m_diag:
            d_type = m_diag.group(1).strip()
            d_params_str = m_diag.group(2).strip()
            d_params = {}
            for part in d_params_str.split('|'):
                part = part.strip()
                if '=' in part:
                    k, v = part.split('=', 1)
                    d_params[k.strip()] = v.strip()
            blocks.append(("DIAGRAM", (d_type, d_params)))
            i += 1
            continue

        # [TABLE: title]\nheader: ...\nrow: ...\n[/TABLE]
        m_table = re.match(r'^\[TABLE(?::\s*(.+?))?\]', line)
        if m_table:
            table_title = (m_table.group(1) or '').strip()
            table_lines = []
            i += 1
            while i < len(lines):
                if '[/TABLE]' in lines[i]:
                    pre = lines[i][:lines[i].index('[/TABLE]')].rstrip()
                    if pre:
                        table_lines.append(pre)
                    break
                table_lines.append(lines[i])
                i += 1
            header_cells = []
            rows = []
            for tl in table_lines:
                ts = tl.strip()
                if not ts:
                    continue
                if ts.lower().startswith('header:'):
                    header_cells = [c.strip() for c in ts[len('header:'):].split('|')]
                elif ts.lower().startswith('row:'):
                    rows.append([c.strip() for c in ts[len('row:'):].split('|')])
            blocks.append(("TABLE", (table_title, header_cells, rows)))
            i += 1
            continue

        # [PULLQUOTE]content[/PULLQUOTE]
        if line.startswith('[PULLQUOTE]'):
            pq_content = ""
            if '[/PULLQUOTE]' in line:
                pq_content = line[len('[PULLQUOTE]'):line.index('[/PULLQUOTE]')]
                blocks.append(("PULLQUOTE", pq_content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/PULLQUOTE]' in lines[i]:
                    pq_content += ' ' + lines[i][:lines[i].index('[/PULLQUOTE]')]
                    break
                pq_content += ' ' + lines[i]
                i += 1
            blocks.append(("PULLQUOTE", pq_content.strip()))
            i += 1
            continue

        # [RUNIN: title]content[/RUNIN] - supports both single-line and multi-line content
        m_runin_open = re.match(r'^\[RUNIN:\s*(.+?)\](.*)$', line)
        if m_runin_open:
            ru_title = m_runin_open.group(1).strip()
            first_part = m_runin_open.group(2)
            # Check if [/RUNIN] is on same line
            if '[/RUNIN]' in first_part:
                ru_content = first_part[:first_part.index('[/RUNIN]')].strip()
                blocks.append(("RUNIN", (ru_title, ru_content)))
                i += 1
                continue
            # Multi-line content
            ru_content = first_part.strip()
            i += 1
            while i < len(lines):
                if '[/RUNIN]' in lines[i]:
                    ru_content += (' ' if ru_content else '') + lines[i][:lines[i].index('[/RUNIN]')].strip()
                    break
                ru_content += (' ' if ru_content else '') + lines[i].strip()
                i += 1
            blocks.append(("RUNIN", (ru_title, ru_content.strip())))
            i += 1
            continue

        # [ORNAMENT]
        if line == '[ORNAMENT]':
            blocks.append(("ORNAMENT", None))
            i += 1
            continue

        # [DATA_CARDS]...[/DATA_CARDS]
        if line.startswith('[DATA_CARDS]'):
            dc_content = ""
            if '[/DATA_CARDS]' in line:
                dc_content = line[len('[DATA_CARDS]'):line.index('[/DATA_CARDS]')]
                blocks.append(("DATA_CARDS", dc_content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/DATA_CARDS]' in lines[i]:
                    dc_content += '\n' + lines[i][:lines[i].index('[/DATA_CARDS]')]
                    break
                dc_content += '\n' + lines[i]
                i += 1
            blocks.append(("DATA_CARDS", dc_content.strip()))
            i += 1
            continue

        # [FORMULA] or [FORMULA: name=foo]...[/FORMULA]
        m_form = re.match(r'^\[FORMULA(?::\s*name=([^\]]+?)\s*)?\]', line)
        if m_form:
            f_name = m_form.group(1)
            formula_content = ""
            if '[/FORMULA]' in line:
                # Extract content between tag end and [/FORMULA]
                tag_end = line.index(']') + 1
                formula_content = line[tag_end:line.index('[/FORMULA]')]
                blocks.append(("FORMULA", (formula_content.strip(), f_name)))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/FORMULA]' in lines[i]:
                    formula_content += '\n' + lines[i][:lines[i].index('[/FORMULA]')]
                    break
                formula_content += '\n' + lines[i]
                i += 1
            formula_running += 1
            if f_name:
                _n = section_counter if (numbering_mode == 'section' and section_counter > 0) else module_num_for_numbering
                name_map[f_name] = f"Công thức {_n}.{formula_running}"
            blocks.append(("FORMULA", (formula_content.strip(), f_name)))
            i += 1
            continue

        # [BODY]...[/BODY]
        m = re.match(r'^\[BODY\](.*)', line)
        if m:
            body_content = m.group(1)
            if '[/BODY]' in body_content:
                body_content = body_content[:body_content.index('[/BODY]')]
                blocks.append(("BODY", body_content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if '[/BODY]' in lines[i]:
                    body_content += '\n' + lines[i][:lines[i].index('[/BODY]')]
                    break
                body_content += '\n' + lines[i]
                i += 1
            blocks.append(("BODY", body_content.strip()))
            i += 1
            continue

        # [BOX_*] or [BOX_*: name=foo]...[/BOX_*]
        box_match = re.match(r'^\[(BOX_(?:PURPLE|KEY|EXAMPLE|WARN|NOTE))(?::\s*name=([^\]]+?)\s*)?\](.*)', line)
        if box_match:
            box_type = box_match.group(1)
            box_name = box_match.group(2)
            box_content = box_match.group(3)
            # EIR: BOX_KEY đứng trước SECTION đầu tiên là Key Takeaways của module
            if box_type == "BOX_KEY" and section_counter == 0:
                box_type = "BOX_TAKEAWAY"
            # Track example numbering
            if box_type == "BOX_EXAMPLE":
                example_running += 1
                if box_name:
                    _n = section_counter if (numbering_mode == 'section' and section_counter > 0) else module_num_for_numbering
                    name_map[box_name] = f"Ví dụ {_n}.{example_running}"
            close_tag = f'[/{box_match.group(1)}]'  # close tag theo tag GỐC (BOX_TAKEAWAY là rename nội bộ)
            if close_tag in box_content:
                box_content = box_content[:box_content.index(close_tag)]
                blocks.append((box_type, box_content.strip()))
                i += 1
                continue
            i += 1
            while i < len(lines):
                if close_tag in lines[i]:
                    box_content += '\n' + lines[i][:lines[i].index(close_tag)]
                    break
                box_content += '\n' + lines[i]
                i += 1
            blocks.append((box_type, box_content.strip()))
            i += 1
            continue

        # Unrecognized line: treat as body text
        if line and not line.startswith('['):
            blocks.append(("BODY", line))
        i += 1

    return blocks, terms_dict, formulas_list, name_map


# ===============================================================================
# FIGURE EMBEDDING (viz-factory assets)
# ===============================================================================

# Populated by render_figure() during assemble_document(); consumed by main() to copy
# media files and emit relationships. Reset at the start of every assemble_document().
FIGURE_MEDIA = []


def _png_size(path):
    """Read PNG pixel dimensions from the IHDR header (stdlib only). None if not a PNG."""
    try:
        with open(path, 'rb') as f:
            head = f.read(24)
        if len(head) >= 24 and head[:8] == b'\x89PNG\r\n\x1a\n':
            return int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big')
    except OSError:
        pass
    return None


def _figure_caption_para(caption):
    # EIR style: "Exhibit N. <caption>" (GS convention); "Hình N.M.x:" prefix replaced.
    if STYLE_EIR[0]:
        EXHIBIT_COUNTER[0] += 1
        import re as _re
        body_cap = _re.sub(r'^Hình\s+[\d.a-z]+\s*:\s*', '', caption).strip()
        caption = f"Exhibit {EXHIBIT_COUNTER[0]}. {body_cap}"
    """Caption line under a figure: Inter family 9pt, muted, centered, italic."""
    cap_runs = run(caption, font=ACTIVE_FONTS.get("body", "Lato"), sz=18,
                   color=C["muted"], italic=True)
    return para(cap_runs, jc="center", spacing_before=40, spacing_after=160)


def render_viz_marker(data):
    """Tinted placeholder strip for an un-rendered [VIZ:] slot (MARKER_CONVENTION.md).
    Box bg #F0EDE6, gold left rule, muted text. Tells the reader exactly which asset
    belongs here once rendered."""
    strip_ppr = (
        f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{C["gold"]}"/></w:pBdr>'
        '<w:shd w:val="clear" w:color="auto" w:fill="F0EDE6"/>'
        '<w:ind w:left="240" w:right="240"/>'
    )
    line1 = run(f'\u3010H\u00ccNH {data.get("id", "?")}\u3011 ', font=ACTIVE_FONTS.get("body", "Lato"),
                sz=18, color=C["secondary"], bold=True)
    line1 += run(data.get("caption", ""), font=ACTIVE_FONTS.get("body", "Lato"), sz=18, color=C["muted"])
    line2 = run(f'ch\u00e8n \u1ea3nh: *_{data.get("id", "?")}.png (component {data.get("component", "viz")})',
                font=ACTIVE_FONTS.get("body", "Lato"), sz=16, color=C["muted"], italic=True)
    return (para(line1, ppr_extra=strip_ppr, spacing_before=160, spacing_after=20)
            + para(line2, ppr_extra=strip_ppr, spacing_before=20, spacing_after=160))


def render_figure(path, caption, build_mode='both'):
    """Embed a rendered PNG asset inline at full text-column width with a caption.
    Missing file -> placeholder strip + warning on stderr (never crash)."""
    if build_mode == 'digital':
        col_tw = 12240 - 1296 - 1296
    else:
        col_tw = 12240 - 1080 - 1440
    col_emu = col_tw * 635

    if not os.path.exists(path):
        sys.stderr.write(f"WARNING: [FIGURE] file not found: {path} (rendering placeholder)\n")
        ph_ppr = (
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="{C["gold"]}"/></w:pBdr>'
            '<w:shd w:val="clear" w:color="auto" w:fill="F0EDE6"/>'
            '<w:ind w:left="240" w:right="240"/>'
        )
        ph = run('\u3010H\u00ccNH CH\u01afA RENDER\u3011 ', font=ACTIVE_FONTS.get("body", "Lato"),
                 sz=18, color=C["secondary"], bold=True)
        ph += run(caption, font=ACTIVE_FONTS.get("body", "Lato"), sz=18, color=C["muted"], italic=True)
        return para(ph, ppr_extra=ph_ppr, spacing_before=160, spacing_after=160)

    n = len(FIGURE_MEDIA) + 1
    FIGURE_MEDIA.append({"n": n, "src": os.path.abspath(path)})
    dims = _png_size(path) or (1600, 900)
    w_px, h_px = dims
    # Assets render at 2x (~192 dpi effective): natural EMU = px / 192in * 914400
    nat_emu = int(w_px * 4762.5)
    cx = min(col_emu, nat_emu)
    cy = int(cx * h_px / w_px) if w_px else col_emu
    rid = f"rIdFig{n}"
    docpr_id = 9000 + n
    drawing = (
        '<w:r><w:rPr/><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Figure {n}"/>'
        '<wp:cNvGraphicFramePr/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:nvPicPr><pic:cNvPr id="{docpr_id}" name="fig{n}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )
    _nocap = caption.strip() in ('\u2014','-','')
    fig_para = para(drawing, jc="center", spacing_before=160, spacing_after=(150 if _nocap else 40))
    if _nocap:
        return fig_para
    return fig_para + _figure_caption_para(caption)


# ===============================================================================
# DOCUMENT ASSEMBLY
# ===============================================================================

def assemble_document(blocks, subject, module_num, module_name, terms_dict=None, formulas_list=None, build_mode='both'):
    """Convert parsed blocks into the full document.xml body content."""
    FIGURE_MEDIA.clear()
    body_parts = []
    just_had_section = False  # Track for drop cap + standfirst on first body after section
    prev_block_type = None  # Track for cluster detection (e.g., consecutive BOX_WARN)

    for block_type, data in blocks:
        if block_type == "COVER":
            # Front end paper REMOVED per user — was the "blank placeholder page" before cover.
            body_parts.append(render_cover(data["subject"], data["title"], data["subtitle"], data.get("hero_prompt", "")))
            # Half-title page also REMOVED per earlier user request (avoid duplicate cover feel).
        elif block_type == "SECTION":
            body_parts.append(render_section(data["en"], data.get("brief", "")))
            just_had_section = True
            continue
        elif block_type == "SUBSECTION":
            body_parts.append(render_subsection(data["en"], data.get("vi", "")))
            just_had_section = False
        elif block_type == "BODY":
            body_parts.append(render_body(data))
        elif block_type == "FORMULA":
            if isinstance(data, tuple):
                body_parts.append(render_formula(data[0], data[1] if len(data) > 1 else None))
            else:
                body_parts.append(render_formula(data))
        elif block_type == "DATA_CARDS":
            body_parts.append(render_data_cards(data))
        elif block_type == "DIVIDER":
            body_parts.append(render_divider())
        elif block_type == "MARGIN":
            mt, mc = data
            body_parts.append(render_margin(mt, mc))
        elif block_type == "FOLDOUT":
            body_parts.append(render_foldout(data))
        elif block_type == "EPIGRAPH":
            esrc, econ = data
            body_parts.append(render_epigraph(esrc, econ))
        elif block_type == "QUOTE":
            src, qc = data
            body_parts.append(render_quote(src, qc))
        elif block_type == "SECTION_OPEN":
            why_now, preview = data
            body_parts.append(render_section_open(why_now, preview))
            just_had_section = False  # Don't double-trigger dropcap
        elif block_type == "RECAP_HANDOFF":
            recap, handoff = data
            body_parts.append(render_recap_handoff(recap, handoff))
            # NO ornament — user explicitly removed (visually 'weird').
            # Section seam is handled by RECAP_HANDOFF italic + next SECTION's heading.
        elif block_type == "FOOTNOTE":
            body_parts.append(render_footnote(data))
        elif block_type == "INTUITION":
            body_parts.append(render_intuition(data))
        elif block_type == "CHECK":
            body_parts.append(render_check(data))
        elif block_type == "DIAGRAM":
            d_type, d_params = data
            body_parts.append(render_diagram(d_type, d_params))
        elif block_type == "FIGURE":
            body_parts.append(render_figure(data["path"], data["caption"], build_mode))
        elif block_type == "VIZMARK":
            body_parts.append(render_viz_marker(data))
        elif block_type == "TABLE":
            title, headers, rows = data
            body_parts.append(render_table(title, headers, rows))
        elif block_type == "PULLQUOTE":
            body_parts.append(render_pullquote(data))
        elif block_type == "RUNIN":
            title, content = data
            body_parts.append(render_runin(title, content))
        elif block_type == "ORNAMENT":
            # User removed ornament glyphs — emit a thin gold rule instead for explicit ORNAMENT tags only
            body_parts.append(render_divider())
        elif block_type.startswith("BOX_"):
            # Cluster detection: if previous block was BOX_WARN and current is BOX_WARN,
            # skip the auto-label "LƯU Ý QUAN TRỌNG" — user feedback: too repetitive.
            cluster_pitfall = (block_type == "BOX_WARN"
                               and prev_block_type == "BOX_WARN")
            body_parts.append(render_box(block_type, data, suppress_label=cluster_pitfall))
        # Track for cluster detection on next iteration
        prev_block_type = block_type

    # Conditional margin based on build mode
    if build_mode == 'print':
        # Print: asymmetric mirror margin (wider gutter)
        margins = 'w:top="1296" w:right="1080" w:bottom="1296" w:left="1440"'
    elif build_mode == 'digital':
        # Digital: symmetric, slightly tighter  
        margins = 'w:top="1296" w:right="1296" w:bottom="1296" w:left="1296"'
    else:  # both
        margins = 'w:top="1296" w:right="1080" w:bottom="1296" w:left="1440"'

    sect_pr = (
        '<w:sectPr>'
        '<w:headerReference w:type="default" r:id="rId7"/>'
        '<w:headerReference w:type="first" r:id="rId11"/>'
        '<w:footerReference w:type="default" r:id="rId8"/>'
        '<w:footerReference w:type="first" r:id="rId12"/>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        f'<w:pgMar {margins} '
        'w:header="600" w:footer="600" w:gutter="0"/>'
        '<w:cols w:space="720"/>'
        '<w:titlePg/>'
        '<w:docGrid w:linePitch="360"/>'
        '</w:sectPr>'
    )

    # Append glossary at end (formula card removed per user request iter 4)
    if terms_dict:
        body_parts.append(render_glossary(terms_dict))

    # Colophon + back end paper REMOVED per user request.
    # Final page is glossary (or last content section if no [T:] terms collected).

    body_xml = "\n".join(body_parts)

    document_xml = textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document
        xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
        mc:Ignorable="w14">
      <w:background w:color="{C['page_bg']}"/>
      <w:body>
    {body_xml}
    {sect_pr}
      </w:body>
    </w:document>""")

    return document_xml.lstrip()


# ===============================================================================
# SUPPORTING XML FILES
# ===============================================================================

def generate_content_types(include_png=False):
    png_default = '\n  <Default Extension="png" ContentType="image/png"/>' if include_png else ''
    body = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>{PNG_DEFAULT}
      <Default Extension="xml" ContentType="application/xml"/>
      <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
      <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
      <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
      <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
      <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
      <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
      <Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
      <Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
      <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
      <Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
    </Types>""")
    return body.replace('{PNG_DEFAULT}', png_default)


def generate_rels():
    return textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    </Relationships>""")


def generate_document_rels(extra_rels=""):
    return textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
      <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
      <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
      <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
      <Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
      <Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
      <Relationship Id="rId10" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
      <Relationship Id="rId11" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header2.xml"/>
      <Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer2.xml"/>{EXTRA_RELS}
    </Relationships>""").replace('{EXTRA_RELS}', extra_rels)


def generate_styles():
    return textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:docDefaults>
        <w:rPrDefault>
          <w:rPr>
            <w:rFonts w:ascii="Lato" w:hAnsi="Lato" w:cs="Lato" w:eastAsia="Lato"/>
            <w:sz w:val="20"/>
            <w:szCs w:val="20"/>
            <w:color w:val="{C['body']}"/>
            <w:lang w:val="vi-VN" w:eastAsia="en-US" w:bidi="ar-SA"/>
          </w:rPr>
        </w:rPrDefault>
        <w:pPrDefault>
          <w:pPr>
            <w:spacing w:after="80" w:line="288" w:lineRule="auto"/>
          </w:pPr>
        </w:pPrDefault>
      </w:docDefaults>
      <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
        <w:name w:val="Normal"/>
      </w:style>
    </w:styles>""")


def generate_settings():
    return textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                mc:Ignorable="w14">
      <w:zoom w:percent="100"/>
      <w:displayBackgroundShape/>
      <w:defaultTabStop w:val="720"/>
      <w:characterSpacingControl w:val="doNotCompress"/>
      <w:compat>
        <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
      </w:compat>
    </w:settings>""")


def generate_numbering():
    return textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    </w:numbering>""")


def generate_font_table():
    return textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:font w:name="Lato">
        <w:panose1 w:val="020B0604020202020204"/>
        <w:charset w:val="00"/>
        <w:family w:val="swiss"/>
        <w:pitch w:val="variable"/>
      </w:font>
      <w:font w:name="Lora">
        <w:panose1 w:val="020B0604020202020204"/>
        <w:charset w:val="00"/>
        <w:family w:val="swiss"/>
        <w:pitch w:val="variable"/>
      </w:font>
      <w:font w:name="Lato">
        <w:panose1 w:val="020B0609020204030204"/>
        <w:charset w:val="00"/>
        <w:family w:val="modern"/>
        <w:pitch w:val="fixed"/>
      </w:font>
    </w:fonts>""")


def generate_header(subject, module_num, module_name):
    subj_color = _subject_color(subject).lstrip('#')
    return textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
           xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <w:p>
        <w:pPr>
          <w:jc w:val="right"/>
          <w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="{C['rule_muted']}"/></w:pBdr>
          <w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/></w:rPr>
        </w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['header_footer']}"/></w:rPr><w:t xml:space="preserve">CFA Level {CFA_LEVEL[0]} - </w:t></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['section_purple']}"/></w:rPr><w:t xml:space="preserve">{esc(subject)}</w:t></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['header_footer']}"/></w:rPr><w:t xml:space="preserve"> - </w:t></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['gold']}"/></w:rPr><w:t xml:space="preserve">Module {module_num}</w:t></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['header_footer']}"/></w:rPr><w:t xml:space="preserve">: {esc(module_name)}</w:t></w:r>
      </w:p>
    </w:hdr>""")


def generate_footer():
    return textwrap.dedent(f"""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:p>
        <w:pPr>
          <w:jc w:val="center"/>
          <w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="{C['rule_muted']}"/></w:pBdr>
          <w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/></w:rPr>
        </w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['header_footer']}"/></w:rPr><w:t xml:space="preserve">Page </w:t></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['section_purple']}"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['section_purple']}"/></w:rPr><w:instrText> PAGE </w:instrText></w:r>
        <w:r><w:rPr><w:rFonts w:ascii="Lora" w:hAnsi="Lora"/><w:i/><w:sz w:val="18"/><w:color w:val="{C['section_purple']}"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
      </w:p>
    </w:ftr>""")




def generate_header_first():
    """Empty first-page header (suppresses header on cover)."""
    return textwrap.dedent('''\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
           xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
      <w:p w14:paraId="40000001" w14:textId="40000001"><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>
    </w:hdr>
    ''')


def generate_footer_first():
    """Empty first-page footer (suppresses footer on cover)."""
    return textwrap.dedent('''\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
           xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
      <w:p w14:paraId="40000002" w14:textId="40000002"><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p>
    </w:ftr>
    ''')

def generate_theme():
    return textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="NoteTheme">
      <a:themeElements>
        <a:clrScheme name="Custom">
          <a:dk1><a:srgbClr val="1C1C1C"/></a:dk1>
          <a:lt1><a:srgbClr val="FFFEF8"/></a:lt1>
          <a:dk2><a:srgbClr val="2C3878"/></a:dk2>
          <a:lt2><a:srgbClr val="F0EDE6"/></a:lt2>
          <a:accent1><a:srgbClr val="2E3B7C"/></a:accent1>
          <a:accent2><a:srgbClr val="C49A1A"/></a:accent2>
          <a:accent3><a:srgbClr val="B85A1C"/></a:accent3>
          <a:accent4><a:srgbClr val="6B3FA0"/></a:accent4>
          <a:accent5><a:srgbClr val="2D6A4F"/></a:accent5>
          <a:accent6><a:srgbClr val="2B5597"/></a:accent6>
          <a:hlink><a:srgbClr val="2E3B7C"/></a:hlink>
          <a:folHlink><a:srgbClr val="6B3FA0"/></a:folHlink>
        </a:clrScheme>
        <a:fontScheme name="Custom">
          <a:majorFont><a:latin typeface="Lora"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
          <a:minorFont><a:latin typeface="Lato"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
        </a:fontScheme>
        <a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
      </a:themeElements>
    </a:theme>""")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Render markup to docx')
    parser.add_argument('input', help='Input markup file')
    parser.add_argument('output', help='Output directory')
    parser.add_argument('--subject', required=True, help='Subject area')
    parser.add_argument('--module-num', required=True, type=int, help='Module number')
    parser.add_argument('--module-name', required=True, help='Module name')
    parser.add_argument('--build', choices=['print', 'digital', 'both'], default='both',
                        help='Build mode: print (mirror margin, asymmetric header), digital (interactive), or both (default)')
    parser.add_argument('--style', choices=['default', 'eir'], default='default',
                        help='eir: Editorial Institutional Research (Exhibit numbering, KEY TAKEAWAYS box)')
    parser.add_argument('--font-stack', choices=['A', 'B', 'C', 'D'], default='B',
                        help='Font stack: A (Editorial Source Serif), B (Lato + Lora, default), C (Be Vietnam Pro)')
    parser.add_argument('--numbering', choices=['module', 'section'], default='module',
                        help='Numbering for Cong thuc/Vi du labels: module (n=module_num, m=global running; '
                             'default, backward compatible) or section (n=section, m resets per section; '
                             'inline refs kept as authored)')
    parser.add_argument('--subject-color', default=None,
                        help='Hex accent color override, e.g. #6B1B2C. Takes precedence over SUBJECT_COLORS lookup.')
    parser.add_argument('--level', choices=['I', 'II', 'III'], default='I',
                        help='CFA level shown on cover badge + header (I/II/III)')
    args = parser.parse_args()
    CFA_LEVEL[0] = args.level

    STYLE_EIR[0] = (args.style == 'eir')
    EXHIBIT_COUNTER[0] = 0

    # Subject color override (baseline colors per CLAUDE.md may differ from engine defaults)
    if args.subject_color:
        _hex = args.subject_color.lstrip('#').upper()
        if re.fullmatch(r'[0-9A-F]{6}', _hex):
            SUBJECT_COLOR_OVERRIDE[0] = _hex
        else:
            sys.stderr.write(f"WARN: --subject-color '{args.subject_color}' is not 6-digit hex, ignored\n")

    # Read markup
    with open(args.input, 'r', encoding='utf-8') as f:
        markup_text = f.read()

    # Parse
    # Set font stack
    global ACTIVE_FONTS
    ACTIVE_FONTS = FONT_STACKS.get(args.font_stack, FONT_STACKS["B"]).copy()

    # Set module number + numbering mode for numbering convention before parse
    parse_markup._module_num = args.module_num
    parse_markup._numbering = args.numbering
    blocks, terms_dict, formulas_list, name_map = parse_markup(markup_text)
    if args.numbering == 'module':
        # Renumber inline 'Công thức N.M' and 'Ví dụ N.M' refs to module.running convention
        blocks = _renumber_inline_refs(blocks, args.module_num)
    # section mode: inline refs kept exactly as authored (already section-scoped N.M);
    # name_map labels are section-scoped, so {ref:name} resolves consistently.
    # Resolve {ref:name} references in body content (post-parse pass)
    if name_map:
        new_blocks = []
        for bt, bd in blocks:
            if bt == "BODY" and isinstance(bd, str):
                resolved = bd
                for n, label in name_map.items():
                    resolved = resolved.replace('{ref:' + n + '}', label)
                new_blocks.append((bt, resolved))
            elif bt in ("BOX_KEY", "BOX_EXAMPLE", "BOX_WARN", "BOX_NOTE", "BOX_PURPLE", "BOX_TAKEAWAY") and isinstance(bd, str):
                resolved = bd
                for n, label in name_map.items():
                    resolved = resolved.replace('{ref:' + n + '}', label)
                new_blocks.append((bt, resolved))
            else:
                new_blocks.append((bt, bd))
        blocks = new_blocks
    # Render summary: per-type block counts so silent parser fails are visible at a glance.
    from collections import Counter as _Counter
    _type_counts = _Counter(bt for bt, _ in blocks)
    _summary_keys = ["SECTION", "SUBSECTION", "BODY", "FORMULA", "BOX_EXAMPLE", "BOX_KEY",
                     "BOX_WARN", "BOX_NOTE", "TABLE", "DIAGRAM", "FIGURE", "VIZ_PLACEHOLDER",
                     "RUNIN", "RECAP_HANDOFF"]
    _summary = "  ".join(f"{k}={_type_counts[k]}" for k in _summary_keys if _type_counts.get(k))
    print(f"Parsed {len(blocks)} blocks; collected {len(terms_dict)} terms, "
          f"{len(formulas_list)} formula-card entries, {len(name_map)} named labels")
    print(f"Block counts: {_summary}")

    # Assemble
    document_xml = assemble_document(blocks, args.subject, args.module_num, args.module_name, terms_dict, formulas_list, build_mode=args.build)

    # Create output dirs
    out = args.output.rstrip('/')
    os.makedirs(f"{out}/word", exist_ok=True)
    os.makedirs(f"{out}/word/theme", exist_ok=True)
    os.makedirs(f"{out}/_rels", exist_ok=True)
    os.makedirs(f"{out}/word/_rels", exist_ok=True)

    # Figures (viz-factory assets): copy media + build relationships
    figure_rels = ""
    if FIGURE_MEDIA:
        import shutil
        os.makedirs(f"{out}/word/media", exist_ok=True)
        rel_parts = []
        for fm in FIGURE_MEDIA:
            shutil.copyfile(fm["src"], f"{out}/word/media/fig{fm['n']}.png")
            rel_parts.append(
                f'\n      <Relationship Id="rIdFig{fm["n"]}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="media/fig{fm["n"]}.png"/>')
        figure_rels = "".join(rel_parts)
        print(f"  Embedded {len(FIGURE_MEDIA)} figure(s) into word/media/")

    # Write files
    files = {
        f"{out}/[Content_Types].xml": generate_content_types(include_png=bool(FIGURE_MEDIA)),
        f"{out}/_rels/.rels": generate_rels(),
        f"{out}/word/_rels/document.xml.rels": generate_document_rels(extra_rels=figure_rels),
        f"{out}/word/document.xml": document_xml,
        f"{out}/word/styles.xml": generate_styles(),
        f"{out}/word/settings.xml": generate_settings(),
        f"{out}/word/numbering.xml": generate_numbering(),
        f"{out}/word/fontTable.xml": generate_font_table(),
        f"{out}/word/header1.xml": generate_header(args.subject, args.module_num, args.module_name),
        f"{out}/word/footer1.xml": generate_footer(),
        f"{out}/word/header2.xml": generate_header_first(),
        f"{out}/word/footer2.xml": generate_footer_first(),
        f"{out}/word/theme/theme1.xml": generate_theme(),
    }

    for path, content in files.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Written: {path}")

    # Auto-update subject handoff (Nhóm 12 continuity)
    try:
        handoff_path = write_subject_handoff(args.subject, args.module_num, args.module_name,
                                              terms_dict, formulas_list, args.output)
        print(f"Subject handoff updated: {handoff_path}")
    except Exception as e:
        print(f"Note: subject handoff update skipped ({e})")

    # (Auto-screenshot hook was truncated in an earlier copy; QC screenshots are handled
    # separately by phase2_screenshot.py.)


if __name__ == '__main__':
    main()
