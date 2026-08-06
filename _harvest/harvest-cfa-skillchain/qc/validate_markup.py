#!/usr/bin/env python3
"""
validate_markup.py - Pre-render validator for note-pipeline markup files.
Implements error codes E01-E39 + warnings W08, W11-W26, W30-W34 (viz + formula notation).

Usage: python validate_markup.py path/to/module.markup.md
Exit code 1 if any error (E*); 0 if only warnings (W*) or clean.

Error codes:
  E01: em-dash or `--`
  E02: [DATA_CARDS] forbidden
  E03: banned pronoun/imperative/reader-ref in render zone
  E04: banned source-marker phrase
  E05: provider name in body
  E06: [FORMULA] missing where-section
  E08: 4+ consecutive [BODY] (downgraded to W08)
  E09: unknown LaTeX command
  E10: nested braces in sub/sup
  E13: §N reference to non-existent section
  E16: unmatched tag pairs
  E18: foreign-language word (Indonesian/Malay/etc.)
  E19: ## markdown prefix before structural tag
  E20: FORMULA tag with title-style param
  E21: nested [BODY] inside [BOX_*]
  E22: [BOX_KEY] contains worked calculation
  E23: BODY block contains chained worked calculation
  E24: [SECTION_OPEN] missing why_now or preview
  E25: malformed [T:] term tag (double bracket)
  E26: BOX_EXAMPLE > 1500 chars
  E27: RUNIN > 500 chars
  E28: TABLE row column count mismatch
  E29: SUBSECTION format inconsistent
  E30: Term [T:] used 3+ times all with full gloss
  E31: FORMULA where: section missing variables
  E32: BODY > 800 chars
  E33: BOX_KEY < 80 chars
  E34: SECTION numbering out of order
  E35: RUNIN prefix style inconsistent

Warning codes:
  W08: 4+ consecutive [BODY]
  W11: unbraced superscript
  W12: section opener variety low
  W14: high English-word density (Vietlish)
  W15: inline (i)(ii)(iii) listing
  W16: sequential numbered listing as separate BODY
  W17: BOX_KEY > 600 chars
  W18: BOX_EXAMPLE missing structure markers
  W20: 3+ consecutive BOX_* same type
  W22: banned filler phrase
  W23: BODY starts with low-effort preamble
  W24: sentence opener variety
  W25: number formatting inconsistent
"""

import os, re
import sys
from collections import Counter


BANNED_PRONOUNS = [
    r'\bbạn\b', r'\bchúng ta\b', r'\bchúng tôi\b', r'\bmình\b',
    r'\btôi\b', r'\bcác bạn\b',
]
BANNED_IMPERATIVES = [
    r'\bhãy\s+(xét|nhìn|nhớ|tính|áp dụng|chú ý|so sánh|phân biệt|ghi nhớ|thử)',
]
BANNED_READER_REFS = [
    r'\bngười đọc\b', r'\bngười thi\b', r'\bngười làm bài\b',
    r'\bngười học\b', r'\bhọc viên\b', r'\bthí sinh\b', r'\bsinh viên\b',
]
BANNED_PROVIDER_NAMES = [
    r'\bSchweser\b', r'\bKaplan\b', r'\bAnalystPrep\b', r'\bUWorld\b',
    r'\bIFT World\b', r'\bHull\b', r'\bFabozzi\b',
]
BANNED_SOURCE_MARKERS = [
    r'\bnhư đã nói ở trên\b', r'\bphần trước đã trình bày\b',
    r'\btheo nguồn\b', r'\bnhư đã đề cập\b',
]
BANNED_FOREIGN_WORDS = [
    r'\bmemiliki\b', r'\bmempunyai\b', r'\bbukan\b', r'\badalah\b',
    r'\buntuk\b', r'\bdengan\b', r'\bdari\b', r'\byang\b(?=\s+[a-zA-Z])',
    r'\bdapat\b', r'\bakan\b(?=\s+[a-zA-Z])', r'\bsedang\b', r'\btelah\b',
    r'\bsudah\b', r'\bbelum\b', r'\bharus\b', r'\bbisa\b',
    r'\bsaya\b', r'\bkamu\b', r'\bkita\b(?=\s+[a-zA-Z])', r'\bmereka\b',
    r'\bmenjadi\b', r'\bmembuat\b', r'\bmendapat\b', r'\bmengerti\b',
    r'\bsemua\b', r'\bbeberapa\b', r'\bsetiap\b', r'\bsemoga\b',
    r'\bbagaimana\b', r'\bmengapa\b', r'\bdimana\b', r'\bkapan\b',
    r'\bnakaka\b', r'\bnaging\b', r'\bmaaari\b', r'\bayaw\b',
    r'\bpara\b(?=\s+[a-zA-Z]{4,})', r'\bcomo\b(?=\s+[a-zA-Z]{4,})',
]


def validate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    lines = content.split('\n')

    # E01: Em-dash
    for ln, line in enumerate(lines, 1):
        sanitized = re.sub(r'\^\{[+\-]+\}|_\{[+\-]+\}|\^\{--\}|_\{--\}', '', line)
        if '—' in sanitized:
            issues.append(('E01', ln, f'em-dash detected: {line[:80]}'))
        if re.search(r'(?<!\{)--(?!\})', sanitized):
            issues.append(('E01', ln, f'double-dash --: {line[:80]}'))

    # E02: DATA_CARDS
    for ln, line in enumerate(lines, 1):
        if '[DATA_CARDS]' in line:
            issues.append(('E02', ln, 'DATA_CARDS tag is forbidden'))

    # E03: Banned pronouns/imperatives/reader refs in render zones
    in_render = False
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('[BODY]') or s.startswith('[BOX_') or s.startswith('[FORMULA]'):
            in_render = True
        if s.startswith('[/BODY]') or s.startswith('[/BOX_') or s.startswith('[/FORMULA]'):
            in_render = False
        if in_render:
            for pat in BANNED_PRONOUNS:
                if re.search(pat, line, re.IGNORECASE):
                    issues.append(('E03', ln, f'banned pronoun: {pat}'))
                    break
            for pat in BANNED_IMPERATIVES:
                if re.search(pat, line, re.IGNORECASE):
                    issues.append(('E03', ln, f'banned imperative: {pat}'))
                    break
            for pat in BANNED_READER_REFS:
                if re.search(pat, line, re.IGNORECASE):
                    issues.append(('E03', ln, f'banned reader reference: {pat}'))
                    break

    # E04: Banned source markers
    for ln, line in enumerate(lines, 1):
        for pat in BANNED_SOURCE_MARKERS:
            if re.search(pat, line, re.IGNORECASE):
                issues.append(('E04', ln, f'banned source marker: {pat}'))

    # E05: Provider names in body
    in_body = False
    for ln, line in enumerate(lines, 1):
        if line.strip().startswith('[BODY]'):
            in_body = True
        if line.strip().startswith('[/BODY]'):
            in_body = False
        if in_body:
            for pat in BANNED_PROVIDER_NAMES:
                m05 = re.search(pat, line)
                if m05:
                    # Academic model names are legitimate, not provider leaks
                    # (Kalotay-Williams-Fabozzi/KWF, Hull-White term structure model)
                    ctx = line[max(0, m05.start() - 30):m05.end() + 12]
                    if re.search(r'Kalotay[-\s]Williams[-\s]Fabozzi|Hull[-\s]White', ctx):
                        continue
                    issues.append(('E05', ln, f'provider name: {pat}'))

    # E06: FORMULA missing where
    for m in re.finditer(r'\[FORMULA\](.*?)\[/FORMULA\]', content, re.DOTALL):
        if not re.search(r'\bwhere:?\s*$|\bwhere\s*\n', m.group(1), re.MULTILINE | re.IGNORECASE):
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E06', ln, 'FORMULA missing where-section'))

    # W08: 4+ consecutive BODY
    body_count = 0
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('[BODY]'):
            body_count += 1
            if body_count >= 4:
                issues.append(('W08', ln, '4+ consecutive [BODY] blocks'))
                body_count = 0
        elif s.startswith('[FORMULA]') or s.startswith('[BOX_') or s.startswith('[DIVIDER]') or s.startswith('[TABLE') or s.startswith('[DIAGRAM') or s.startswith('[INTUITION]') or s.startswith('[RUNIN'):
            body_count = 0

    # E09: Unknown LaTeX
    KNOWN_LATEX = {
        '\\alpha', '\\beta', '\\gamma', '\\delta', '\\epsilon', '\\varepsilon',
        '\\zeta', '\\eta', '\\theta', '\\vartheta', '\\iota', '\\kappa',
        '\\lambda', '\\mu', '\\nu', '\\xi', '\\omicron', '\\pi', '\\varpi',
        '\\rho', '\\varrho', '\\sigma', '\\varsigma', '\\tau', '\\upsilon',
        '\\phi', '\\varphi', '\\chi', '\\psi', '\\omega',
        '\\Theta', '\\Pi', '\\Sigma', '\\Delta', '\\Lambda', '\\Xi',
        '\\Gamma', '\\Phi', '\\Psi', '\\Omega', '\\Upsilon',
        '\\sum', '\\prod', '\\int', '\\infty', '\\partial', '\\nabla',
        '\\neq', '\\leq', '\\geq', '\\approx', '\\equiv', '\\propto',
        '\\cdot', '\\times', '\\div', '\\pm', '\\mp',
        '\\in', '\\notin', '\\subset', '\\subseteq', '\\supset', '\\supseteq',
        '\\cup', '\\cap', '\\forall', '\\exists',
        '\\rightarrow', '\\leftarrow', '\\Rightarrow', '\\Leftarrow',
        '\\to', '\\mapsto', '\\sqrt', '\\text', '\\ln', '\\log', '\\exp',
        '\\min', '\\max', '\\lim', '\\sup', '\\inf', '\\arg',
    }
    # BUGFIX batch 3: Skip DIAGRAM blocks (\\n separator in params is NOT LaTeX)
    diagram_line_set = set()
    for m in re.finditer(r'\[DIAGRAM:[^\]]+\]', content):
        ln_start = content[:m.start()].count('\n') + 1
        ln_end = content[:m.end()].count('\n') + 1
        for ln_d in range(ln_start, ln_end + 1):
            diagram_line_set.add(ln_d)
    # PATCH L1/L2/L3: bo qua dong trong [FORMULA] (gio la LaTeX nguon cho anh typeset, khong render text)
    formula_line_set = set()
    for mf in re.finditer(r'\[FORMULA(?::[^\]]*)?\](.*?)\[/FORMULA\]', content, re.DOTALL):
        fs = content[:mf.start()].count('\n') + 1
        fe = content[:mf.end()].count('\n') + 1
        for ln_f in range(fs, fe + 1):
            formula_line_set.add(ln_f)
    for ln, line in enumerate(lines, 1):
        if ln in diagram_line_set or ln in formula_line_set:
            continue
        for cmd in re.findall(r'\\[A-Za-z]+', line):
            if cmd not in KNOWN_LATEX:
                issues.append(('E09', ln, f'unknown LaTeX: {cmd}'))

    # E10: Nested braces in sub/sup
    for ln, line in enumerate(lines, 1):
        if re.search(r'[\^_]\{[^}]*\{[^}]*\}', line):
            issues.append(('E10', ln, 'nested braces in sub/sup'))

    # W11: Unbraced superscript
    for ln, line in enumerate(lines, 1):
        if re.search(r'[A-Za-z\)\}]\^[+\-\*](?![A-Za-z0-9{])', line):
            issues.append(('W11', ln, 'unbraced superscript ^+/^-/^*'))

    # E18: Foreign words
    for ln, line in enumerate(lines, 1):
        line_text = re.sub(r'\[/?[A-Z_]+(:[^]]*)?\]', ' ', line)
        for pat in BANNED_FOREIGN_WORDS:
            m = re.search(pat, line_text, re.IGNORECASE)
            if m:
                issues.append(('E18', ln, f'foreign word: "{m.group(0)}"'))

    # W15: Inline (i)(ii)(iii) listings
    body_pattern_inline = re.compile(r'\[BODY\](.*?)\[/BODY\]', re.DOTALL)
    for m in body_pattern_inline.finditer(content):
        body_text = m.group(1)
        if '(i)' in body_text and '(ii)' in body_text and '(iii)' in body_text:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('W15', ln, 'inline (i)(ii)(iii) listing - extract to TABLE'))

    # W16: Sequential numbered listings
    seq_patterns = [
        r'^\s*Thứ\s+(nhất|hai|ba|tư|năm|sáu)\b',
        r'^\s*Bước\s+\d+\b',
        r'^\s*Lực\s+\d+\b',
        r'^\s*Chiến\s+lược\s+\d+\b',
    ]
    for m in body_pattern_inline.finditer(content):
        body_text = m.group(1).strip()
        for pat in seq_patterns:
            if re.match(pat, body_text):
                ln = content[:m.start()].count('\n') + 1
                issues.append(('W16', ln, 'sequential listing in BODY - use RUNIN'))
                break

    # W14: English density per BODY
    body_pattern = re.compile(r'\[BODY\](.*?)\[/BODY\]', re.DOTALL)
    for m in body_pattern.finditer(content):
        body_text = m.group(1)
        stripped = re.sub(r'[A-Z]{1,4}/[A-Z]{1,5}|[A-Z][_^]\{?[A-Za-z0-9]+\}?|\$[A-Za-z]+|[A-Z]{2,5}\b', ' ', body_text)
        words = re.findall(r'\b[A-Za-zÀ-ỹ]{3,}\b', stripped)
        if len(words) < 30:
            continue
        en_words = [w for w in words if re.fullmatch(r'[a-zA-Z]+', w) and len(w) >= 4]
        en_words = [w for w in en_words if w.lower() not in {'investor', 'analyst', 'manager', 'company', 'industry', 'market', 'price', 'value', 'growth'}]
        pct = 100 * len(en_words) / len(words) if words else 0
        if pct > 25:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('W14', ln, f'high English density: {pct:.0f}% ({len(en_words)}/{len(words)})'))

    # W12: Sentence opener variety
    body_blocks_per_section = {}
    current_section = 0
    for ln, line in enumerate(lines, 1):
        if line.strip().startswith('[SECTION:'):
            current_section += 1
        if current_section > 0:
            bm = re.search(r'\[BODY\](.+?)\[/BODY\]', line)
            if bm:
                body_blocks_per_section.setdefault(current_section, []).append(bm.group(1))
    for sec_num, bodies in body_blocks_per_section.items():
        if len(bodies) < 6:
            continue
        opener_count = {}
        sample_count = 0
        for body in bodies:
            sentences = re.split(r'[.!?]\s+', body)
            for sent in sentences:
                sent = sent.strip()
                if not sent or len(sent) < 10:
                    continue
                words = sent.split()
                if len(words) >= 2:
                    opener = ' '.join(words[:2]).lower()
                    opener_count[opener] = opener_count.get(opener, 0) + 1
                    sample_count += 1
        if sample_count >= 8:
            top3 = Counter(opener_count).most_common(3)
            top3_total = sum(c for _, c in top3)
            if top3_total / sample_count > 0.4:
                top3_str = ', '.join(f'"{w}" ({c})' for w, c in top3)
                issues.append(('W12', 0, f'Section {sec_num}: top-3 openers dominate ({top3_total}/{sample_count}): {top3_str}'))

    # E16: Unmatched tag pairs
    tag_pairs = ['BODY', 'FORMULA', 'BOX_KEY', 'BOX_EXAMPLE', 'BOX_WARN', 'BOX_NOTE', 'BOX_PURPLE',
                 'TABLE', 'PULLQUOTE', 'INTUITION', 'CHECK', 'SECTION_OPEN', 'RECAP_HANDOFF', 'RUNIN']
    for tag in tag_pairs:
        opens = len(re.findall(rf'\[{tag}(?:[: ]|\])', content))
        closes = len(re.findall(rf'\[/{tag}\]', content))
        if opens != closes:
            issues.append(('E16', 0, f'unmatched [{tag}]: {opens} opens vs {closes} closes'))

    # E13: §N reference to non-existent section
    section_count = len(re.findall(r'^\[SECTION:', content, re.MULTILINE))
    section_refs = re.findall(r'§(\d+)(?:\.\d+)?', content)
    for ref in section_refs:
        if int(ref) > section_count:
            issues.append(('E13', 0, f'§{ref} refers to non-existent section (only {section_count})'))

    # ============== BATCH 1 RULES (E19-E25 + W17-W20) ==============

    # E19: ## markdown prefix before structural tag
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^(#{1,6})\s+\[(SUBSECTION|SECTION|FORMULA|BODY|BOX_\w+|TABLE|RUNIN|INTUITION|RECAP_HANDOFF|SECTION_OPEN)', line)
        if m:
            issues.append(('E19', ln, f'markdown header "{m.group(1)} " before [{m.group(2)}] - remove prefix'))

    # E20: FORMULA title-style param
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^\[FORMULA:\s*([^\]]+)\]', line)
        if m:
            param = m.group(1).strip()
            if not re.match(r'^name\s*=\s*\w+$', param):
                issues.append(('E20', ln, f'FORMULA title-style "[FORMULA: {param[:40]}]" - use [FORMULA] or [FORMULA: name=slug]'))

    # E21: Nested BODY in BOX_*
    box_types = ['BOX_KEY', 'BOX_EXAMPLE', 'BOX_WARN', 'BOX_NOTE', 'BOX_PURPLE']
    for bt in box_types:
        pattern = rf'\[{bt}(?::[^\]]*)?\](.*?)\[/{bt}\]'
        for m in re.finditer(pattern, content, re.DOTALL):
            inner = m.group(1)
            if re.search(r'\[/?BODY\]', inner):
                ln = content[:m.start()].count('\n') + 1
                issues.append(('E21', ln, f'[{bt}] contains nested [BODY] - strip wrapper'))

    # E22: BOX_KEY with worked calculation
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, content, re.DOTALL):
        inner = m.group(1)
        eq_chains = len(re.findall(r'=\s*[\d.,$]+\s*[/×÷*+\-]\s*[\d.,$()]+\s*=', inner))
        nums = len(re.findall(r'\d+[.,]\d+', inner))
        if eq_chains >= 2 or (nums >= 6 and inner.count('=') >= 4):
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E22', ln, f'[BOX_KEY] contains worked calculation ({eq_chains} chains, {nums} nums) - move to BOX_EXAMPLE'))

    # E23: BODY with chained calculation
    body_pattern = r'\[BODY\](.*?)\[/BODY\]'
    for m in re.finditer(body_pattern, content, re.DOTALL):
        inner = m.group(1)
        chained = re.findall(
            r'=\s*[\d.,$()×÷*+/\-\s]+[×÷*+\-/]\s*[\d.,$()\s]+\s*=\s*[\d.,\-$]',
            inner
        )
        has_step_calc = re.search(r'(Bước\s+\d+:.*?=.*?=)|(Phương án\s+\w+:.*?=.*?=)', inner, re.DOTALL)
        if len(chained) >= 2 or (has_step_calc and len(chained) >= 1):
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E23', ln, f'[BODY] contains chained calculation ({len(chained)} chains) - wrap in [BOX_EXAMPLE]'))

    # E24: SECTION_OPEN missing why_now/preview
    so_pattern = r'\[SECTION_OPEN\](.*?)\[/SECTION_OPEN\]'
    for m in re.finditer(so_pattern, content, re.DOTALL):
        inner = m.group(1)
        if 'why_now:' not in inner.lower():
            ln = content[:m.start()].count('\n') + 1
        # [removed] issues.append(('E24', ln, '[SECTION_OPEN] missing "why_now:" field'))   # SECTION_OPEN no longer required
        if 'preview:' not in inner.lower():
            ln = content[:m.start()].count('\n') + 1
        # [removed] issues.append(('E24', ln, '[SECTION_OPEN] missing "preview:" field'))   # SECTION_OPEN no longer required

    # E25: malformed [T:] term tag
    for ln, line in enumerate(lines, 1):
        if re.search(r'\[T:[^\]]+\]\]', line):
            issues.append(('E25', ln, 'malformed [T:]] double bracket'))

    # W17: BOX_KEY > 600 chars
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) > 600:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('W17', ln, f'[BOX_KEY] is {len(inner)} chars (> 600) - split insight + example'))

    # W18: BOX_EXAMPLE missing structure markers
    pattern = r'\[BOX_EXAMPLE(?::[^\]]*)?\](.*?)\[/BOX_EXAMPLE\]'
    for m in re.finditer(pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) < 100:
            continue
        has_struct = any(kw in inner for kw in ['Bước 1', 'Bước 2', 'Phương án', 'Tính', 'Cách 1', 'Bước:'])
        nums_count = len(re.findall(r'\d+[.,]\d+', inner))
        if not has_struct and nums_count >= 4:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('W18', ln, f'[BOX_EXAMPLE] has {nums_count} numerics without structure - add Bước/Tính labels'))

    # W20: 3+ consecutive BOX_* same type
    block_types_seen = []
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^\[(BOX_\w+)', line)
        if m:
            block_types_seen.append((ln, m.group(1)))
    for i in range(len(block_types_seen) - 2):
        if block_types_seen[i][1] == block_types_seen[i+1][1] == block_types_seen[i+2][1]:
            issues.append(('W20', block_types_seen[i][0], f'3+ consecutive [{block_types_seen[i][1]}] - vary box types'))

    # ============== BATCH 2 RULES (E26-E35 + W22-W25) ==============

    # E26: BOX_EXAMPLE > 1500 chars
    pattern = r'\[BOX_EXAMPLE(?::[^\]]*)?\](.*?)\[/BOX_EXAMPLE\]'
    for m in re.finditer(pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) > 1500:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E26', ln, f'[BOX_EXAMPLE] is {len(inner)} chars (> 1500) - split or simplify'))

    # E27: RUNIN > 500 chars
    runin_pattern = r'\[RUNIN(?::[^\]]*)?\](.*?)\[/RUNIN\]'
    for m in re.finditer(runin_pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) > 500:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E27', ln, f'[RUNIN] is {len(inner)} chars (> 500) - use BODY or split'))

    # E28: TABLE column count mismatch
    table_pattern = r'\[TABLE(?::[^\]]*)?\](.*?)\[/TABLE\]'
    for m in re.finditer(table_pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        header_match = re.search(r'^\s*header:\s*(.+)$', inner, re.MULTILINE)
        if not header_match:
            continue
        header_cols = len(header_match.group(1).split('|'))
        row_lines = re.findall(r'^\s*row:\s*(.+)$', inner, re.MULTILINE)
        for i, row in enumerate(row_lines, 1):
            row_cols = len(row.split('|'))
            if row_cols != header_cols:
                ln = content[:m.start()].count('\n') + 1
                issues.append(('E28', ln, f'[TABLE] row {i}: {row_cols} cols vs header {header_cols}'))
                break

    # E29: SUBSECTION format inconsistent
    subsections = re.findall(r'^\[SUBSECTION:\s*([^|\]]+)\|\s*([^\]]+)\]', content, re.MULTILINE)
    if subsections:
        with_vi_prefix = sum(1 for _, vi in subsections if vi.strip().startswith('vi:'))
        without_vi_prefix = len(subsections) - with_vi_prefix
        if with_vi_prefix > 0 and without_vi_prefix > 0:
            issues.append(('E29', 0, f'SUBSECTION format inconsistent: {with_vi_prefix} use "vi:", {without_vi_prefix} do not'))

    # E30: Term [T:] used 3+ times all with full gloss
    term_pattern = r'\[T:\s*([^|\]]+?)\s*\|\s*([^\]]+)\]'
    term_uses = {}
    for m in re.finditer(term_pattern, content):
        en = m.group(1).strip().lower()
        ln = content[:m.start()].count('\n') + 1
        term_uses.setdefault(en, []).append(ln)
    for en, lines_used in term_uses.items():
        if len(lines_used) >= 3:
            issues.append(('E30', lines_used[0], f'Term "{en}" used {len(lines_used)} times with full gloss - only first should have'))

    # E31: FORMULA where: section variable mismatch
    formula_pattern = r'\[FORMULA(?::\s*name=\w+)?\](.*?)\[/FORMULA\]'
    for m in re.finditer(formula_pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if 'where:' not in inner.lower():
            continue
        parts = re.split(r'where:', inner, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) != 2:
            continue
        formula_expr, where_section = parts
        if '\\' in formula_expr:  # PATCH: formula LaTeX-for-image -> khong check var coverage
            continue
        formula_vars = set(re.findall(r'\b([A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)?)\b', formula_expr))
        formula_vars -= {'where', 'log', 'ln', 'exp', 'min', 'max', 'sin', 'cos', 'tan', 'sum', 'and', 'or', 'in', 'of', 'is', 'to', 'sqrt', 'abs'}
        defined_vars = set()
        for line in where_section.split('\n'):
            # Accept both "var = ..." and "- var = ..." (markdown list style, FI_M1/AI_M1 lesson)
            mvar = re.match(r'^\s*(?:[-*]\s+)?(?:d\(ln\s*)?([A-Za-z][A-Za-z0-9_]*)\)?\s*(?:\([A-Za-z]\))?\s*=', line)
            if mvar:
                defined_vars.add(mvar.group(1))
        undefined = formula_vars - defined_vars - {'e', 'a', 'b', 'c', 'd', 'k', 'n', 'i', 'j', 't', 'x', 'y', 'z'}
        meaningful_undefined = [v for v in undefined if len(v) > 1 or v.isupper()]
        if len(meaningful_undefined) >= 2:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E31', ln, f'[FORMULA] vars {meaningful_undefined[:3]} not defined in where:'))

    # E32: BODY > 800 chars
    for m in re.finditer(body_pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) > 800:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E32', ln, f'[BODY] is {len(inner)} chars (> 800) - split for readability'))

    # E33: BOX_KEY < 80 chars
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, content, re.DOTALL):
        inner = m.group(1).strip()
        if 0 < len(inner) < 80:
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E33', ln, f'[BOX_KEY] is {len(inner)} chars (< 80) - too short'))

    # E34: SECTION numbers out of order
    section_titles = re.findall(r'^\[SECTION:\s*([^|]+)\s*\|\s*([^\]]+)\]', content, re.MULTILINE)
    section_num_pattern = re.compile(r'(?:Section|Mục|§|Phần)\s*(\d+)')
    nums = []
    for en, vi in section_titles:
        m1 = section_num_pattern.search(en)
        m2 = section_num_pattern.search(vi)
        if m1 or m2:
            nums.append(int((m1 or m2).group(1)))
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1] + 1:
            issues.append(('E34', 0, f'SECTION out of order: §{nums[i]} after §{nums[i-1]}'))
            break

    # E35: RUNIN prefix style inconsistent
    runin_prefixes = re.findall(r'\[RUNIN:\s*([^\]]+)\]', content)
    if runin_prefixes:
        with_colon = sum(1 for p in runin_prefixes if ':' in p[:30])
        with_dot = sum(1 for p in runin_prefixes if re.match(r'^\s*\w+\s*\d+\.\s', p))
        with_comma = sum(1 for p in runin_prefixes if re.match(r'^\s*\w+\s*\d+,\s', p))
        styles_used = sum(1 for x in [with_colon, with_dot, with_comma] if x > 0)
        if styles_used >= 2:
            issues.append(('E35', 0, f'RUNIN prefix style inconsistent: {with_colon} use ":", {with_dot} use ".", {with_comma} use ","'))

    # W22: Banned filler phrases
    BANNED_FILLERS = [
        (r'\bInsight là\b', 'Insight là'),
        (r'\bBottom line\b', 'Bottom line'),
        (r'\bTakeaway\b(?!\s*:)', 'Takeaway'),
        (r'\bForward[- ]looking\b', 'Forward-looking'),
        (r'\bBackward[- ]looking\b', 'Backward-looking'),
        (r'\bKey insight\b', 'Key insight'),
        (r'\bDeep dive\b(?!\s+\w+)', 'Deep dive'),
    ]
    for ln, line in enumerate(lines, 1):
        for pat, label in BANNED_FILLERS:
            if re.search(pat, line, re.IGNORECASE):
                issues.append(('W22', ln, f'banned filler "{label}" - replace with substantive Vietnamese'))

    # W23: BODY starts with low-effort preamble
    for m in re.finditer(r'\[BODY\]\s*(Lưu ý:|Note:|Chú ý:)', content):
        ln = content[:m.start()].count('\n') + 1
        issues.append(('W23', ln, f'BODY starts with "{m.group(1)}" preamble - integrate or use BOX_NOTE'))

    # W24: Sentence opener variety
    body_pattern_check = re.compile(r'\[BODY\]\s*([A-ZÀ-ỹ]\w+\s+\w+)', re.MULTILINE)
    openers = [m.group(1).lower() for m in body_pattern_check.finditer(content)]
    if len(openers) >= 10:
        most_common = Counter(openers).most_common(1)[0]
        if most_common[1] / len(openers) > 0.3:
            issues.append(('W24', 0, f'opener "{most_common[0]}" used {most_common[1]}/{len(openers)} - vary'))

    # W25: Number formatting consistency
    has_dot_decimal = bool(re.search(r'\$[\d,]+\.\d{2}', content))
    has_comma_decimal = bool(re.search(r'\$[\d.]+,\d{2}', content))
    if has_dot_decimal and has_comma_decimal:
        issues.append(('W25', 0, 'Number format inconsistent: mix US (1.50) and EU (1,50) styles'))

    # ============== BATCH 3 RULES (E36-E37, W26) ==============

    # E36 (NEW): File truncated - ends mid-statement
    last_500 = content[-500:].strip()
    if last_500 and not re.search(r'\[/(SECTION|BODY|BOX_\w+|RECAP_HANDOFF|FORMULA|TABLE|RUNIN|INTUITION|SECTION_OPEN)\]\s*$', last_500):
        last_line = last_500.split('\n')[-1]
        if re.search(r'[a-zA-Z\d,]\s*$', last_line):
            issues.append(('E36', 0, f'File appears truncated: "{last_line[:60]}..."'))

    # E37 (NEW): RUNIN prefix style - enforce uniform colon
    runin_prefixes_e37 = re.findall(r'\[RUNIN:\s*([^\]]+)\]', content)
    if runin_prefixes_e37:
        style_colon = sum(1 for p in runin_prefixes_e37 if re.match(r'^\s*\w+\s+\d+\s*:', p))
        style_comma = sum(1 for p in runin_prefixes_e37 if re.match(r'^\s*\w+\s+\d+\s*,', p))
        style_dot = sum(1 for p in runin_prefixes_e37 if re.match(r'^\s*\w+\s+\d+\s*\.', p))
        if (style_comma > 0 or style_dot > 0) and style_colon > 0:
            issues.append(('E37', 0, f'RUNIN prefix mixed: {style_colon} colon, {style_comma} comma, {style_dot} dot - use colon only'))

    # W26 (NEW): DIAGRAM coverage
    diagram_count_w26 = len(re.findall(r'^\[DIAGRAM:', content, re.MULTILINE))
    subsection_count_w26 = len(re.findall(r'^\[SUBSECTION:', content, re.MULTILINE))
    body_count_w26 = len(re.findall(r'^\[BODY\]', content, re.MULTILINE))
    if subsection_count_w26 >= 30 or body_count_w26 >= 100:
        if diagram_count_w26 == 0:
            issues.append(('W26', 0, f'{subsection_count_w26} subs / {body_count_w26} BODY but 0 DIAGRAM - add 3-5 visual diagrams'))
        elif diagram_count_w26 < 3 and subsection_count_w26 >= 30:
            issues.append(('W26', 0, f'{subsection_count_w26} subs but only {diagram_count_w26} DIAGRAM - target >=3'))

    # E03 scope: RUNIN, INTUITION
    extended_zones = [
        (r'\[RUNIN(?::[^\]]*)?\](.*?)\[/RUNIN\]', 'RUNIN'),
        (r'\[INTUITION\](.*?)\[/INTUITION\]', 'INTUITION'),
    ]
    for pat, zone_name in extended_zones:
        for m in re.finditer(pat, content, re.DOTALL):
            inner = m.group(1)
            ln = content[:m.start()].count('\n') + 1
            for vp in BANNED_PRONOUNS:
                if re.search(vp, inner, re.IGNORECASE):
                    issues.append(('E03', ln, f'banned pronoun in [{zone_name}]: {vp}'))
                    break

    # E38: placeholder cells/content leaked from writer agents (FI_M4 lesson:
    # "(giữa)" và "(chain calc)" cells shipped to render)
    for m in re.finditer(r'\((?:giữa|chain calc|chain|TBD|todo|điền sau|fill later|\.\.\.)\)', content, re.IGNORECASE):
        ln = content[:m.start()].count('\n') + 1
        line_text = content.split('\n')[ln - 1]
        token = m.group(0).lower()
        # "(giữa)" và "(chain)" chỉ là placeholder trong table cell ("| (giữa) |");
        # trong prose tiếng Việt chúng là mô tả hợp lệ (vd "i_2,ud (giữa)")
        _ls = line_text.lstrip()
        if token in ('(giữa)', '(chain)') and not (_ls.startswith('|') or _ls.lower().startswith('row:')):
            continue
        issues.append(('E38', ln, f'Placeholder "{m.group(0)}" leaked - compute real value before render'))

    # W33: unary/postfix asterisk in FORMULA - engine renders binary * as ×; for
    # Taylor-style notation prefer ^* (superscript star). Advisory only (engine v2
    # keeps unary * literal, but ^* is the established convention).
    for m in re.finditer(r'\[FORMULA(?::[^\]]*)?\](.*?)\[/FORMULA\]', content, re.DOTALL):
        inner = m.group(1)
        expr = inner.split('where:')[0] if 'where:' in inner.lower() else inner
        for um in re.finditer(r'[A-Za-zπσθρλ][A-Za-z0-9_]*\*(?=\s*[)\],.;]|\s*$)', expr, re.MULTILINE):
            ln = content[:m.start()].count('\n') + 1
            issues.append(('W33', ln, f'Postfix star "{um.group(0)}" - prefer ^* notation (e.g. π^*)'))
            break

    # E39: image-hint Prompt MUST be full English (user rule: BAT BUOC).
    # Vietnamese diacritics in the Prompt line = error.
    for m in re.finditer(r'^(?:\*\*)?Prompt \(English\)(?:\*\*)?:\s*(.+)$', content, re.MULTILINE):
        if re.search(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂÂÈÉẺẼẸÊÌÍỈĨỊÒÓỎÕỌÔƠÙÚỦŨỤƯỲÝĐ]', m.group(1)):
            ln = content[:m.start()].count('\n') + 1
            issues.append(('E39', ln, 'Image-hint Prompt contains Vietnamese - must be FULL English'))

    # W34: module thiếu term tagging - chuẩn AI_M1: terminology lần đầu phải có
    # [T: term | gloss] để render blue term + gloss xám nghiêng + trang Thuật ngữ cuối.
    n_tags = len(re.findall(r'\[T:\s*[^|\]]+\|', content))
    n_sections = len(re.findall(r'^\[SECTION:', content, re.MULTILINE))
    if n_sections >= 4 and n_tags < 10:
        issues.append(('W34', 0, f'Only {n_tags} [T:] term tags for {n_sections} sections - target 25-50 per module'))

    # ============== VIZ INTEGRATION RULES (W30-W32) ==============
    # [FIGURE: path | caption] embeds a rendered viz-factory PNG; [VIZ: component | id=N.M.x
    # | caption=... | params={...}] is a viz slot directive (renders as placeholder strip).
    # Both are VALID tags for render_engine - never flag them as raw/unknown.

    # W30: [FIGURE:] path does not exist (engine will render placeholder, not crash)
    for m in re.finditer(r'^\[FIGURE:\s*(.+?)\s*\|\s*(.+?)\s*\]\s*$', content, re.MULTILINE):
        fpath = m.group(1).strip()
        ln = content[:m.start()].count('\n') + 1
        if not os.path.exists(fpath):
            issues.append(('W30', ln, f'[FIGURE] path not found: {fpath[:70]} (renders placeholder)'))

    # W31/W32: [VIZ:] directive schema - id= and caption= mandatory, id unique per module
    viz_ids_seen = []
    _vlines = content.split('\n')
    _vi = 0
    while _vi < len(_vlines):
        _vs = _vlines[_vi].strip()
        if _vs.startswith('[VIZ:'):
            _start_ln = _vi + 1
            _buf = _vs
            _depth = _buf.count('[') - _buf.count(']')
            while _depth > 0 and _vi + 1 < len(_vlines):
                _vi += 1
                _buf += ' ' + _vlines[_vi].strip()
                _depth = _buf.count('[') - _buf.count(']')
            _vid = re.search(r'\bid=([0-9]+(?:\.[0-9]+)?(?:\.[a-z])?)', _buf)
            _cap = re.search(r'caption=([^|\]]+)', _buf)
            if not _vid:
                issues.append(('W31', _start_ln, '[VIZ] directive missing id=N.M.x'))
            elif _vid.group(1) in viz_ids_seen:
                issues.append(('W32', _start_ln, f'[VIZ] duplicate id={_vid.group(1)}'))
            else:
                viz_ids_seen.append(_vid.group(1))
            if not _cap or not _cap.group(1).strip():
                issues.append(('W31', _start_ln, '[VIZ] directive missing caption='))
        _vi += 1

    # ============== END OF RULES ==============

    issues.sort(key=lambda x: (x[1], x[0]))
    errors = [i for i in issues if i[0].startswith('E')]
    warnings = [i for i in issues if i[0].startswith('W')]

    print(f"=== Markup Validation Report ===")
    print(f"File: {filepath}")
    print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")
    print()

    if errors:
        print("=== ERRORS (block render) ===")
        error_counter = Counter(i[0] for i in errors)
        for code, cnt in error_counter.most_common():
            print(f"  {code}: {cnt} occurrences")
        print()
        for code, ln, msg in errors[:30]:
            print(f"  L{ln}: {code} {msg}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        print()

    if warnings:
        print("=== WARNINGS (non-blocking) ===")
        warn_counter = Counter(i[0] for i in warnings)
        for code, cnt in warn_counter.most_common():
            print(f"  {code}: {cnt} occurrences")
        print()
        for code, ln, msg in warnings[:20]:
            print(f"  L{ln}: {code} {msg}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")
        print()

    if not issues:
        print("OK Clean - no errors or warnings")

    return 1 if errors else 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: validate_markup.py <markup_file>")
        sys.exit(2)
    sys.exit(validate(sys.argv[1]))
