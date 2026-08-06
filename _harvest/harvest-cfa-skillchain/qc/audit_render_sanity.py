#!/usr/bin/env python3
"""
audit_render_sanity.py - Post-render sanity check.

Catches "silently failed parse" issues that escape validate_markup.py + render_engine.

Usage:
    python audit_render_sanity.py path/to/module.markup.md [--render-out=/tmp/render]

Exit code 0 if clean, 1 if any CRITICAL finding.

Anti-patterns:
  B1: ## markdown prefix before structural tag
  B2: [FORMULA: title] title-style param
  B3: nested [BODY] inside [BOX_*]
  B4: BOX_KEY with worked calculation
  B5: BODY with chained calculation
  B6: malformed [T:]] double bracket
  B7: BOX_KEY > 600 chars
  B8: multiple RECAP_HANDOFF per section
  B9: BOX_KEY contains structure markers (Bước/Phương án)
  B10: BOX_EXAMPLE too thin (< 200 chars, single paragraph)
  B11: TABLE > 8 columns
  B12: TABLE > 15 rows
  B13: RUNIN with 5+ sentences
  B14: 4+ consecutive [DIAGRAM: type] same type
  B15: §N reference in RECAP_HANDOFF mismatch section count
  B16: SECTION_OPEN preview claims subsection count != actual
"""

import argparse
import os
import re
import subprocess
import sys


def count_markup_tags(markup_text):
    counts = {
        'SECTION': len(re.findall(r'^\[SECTION:', markup_text, re.MULTILINE)),
        'SUBSECTION': len(re.findall(r'^\[SUBSECTION:', markup_text, re.MULTILINE)),
        'BODY': len(re.findall(r'^\[BODY\]', markup_text, re.MULTILINE)),
        'FORMULA': len(re.findall(r'^\[FORMULA(?::|\])', markup_text, re.MULTILINE)),
        'BOX_KEY': len(re.findall(r'^\[BOX_KEY', markup_text, re.MULTILINE)),
        'BOX_EXAMPLE': len(re.findall(r'^\[BOX_EXAMPLE', markup_text, re.MULTILINE)),
        'BOX_WARN': len(re.findall(r'^\[BOX_WARN', markup_text, re.MULTILINE)),
        'BOX_NOTE': len(re.findall(r'^\[BOX_NOTE', markup_text, re.MULTILINE)),
        'INTUITION': len(re.findall(r'^\[INTUITION', markup_text, re.MULTILINE)),
        'TABLE': len(re.findall(r'^\[TABLE', markup_text, re.MULTILINE)),
        'RUNIN': len(re.findall(r'^\[RUNIN', markup_text, re.MULTILINE)),
        'DIAGRAM': len(re.findall(r'^\[DIAGRAM', markup_text, re.MULTILINE)),
        'TERM': len(re.findall(r'\[T:', markup_text)),
        'RECAP_HANDOFF': len(re.findall(r'^\[RECAP_HANDOFF\]', markup_text, re.MULTILINE)),
    }
    return counts


def detect_bad_patterns(markup_text):
    issues = []
    lines = markup_text.split('\n')

    # B1: ## prefix before structural tag
    for ln, line in enumerate(lines, 1):
        if re.match(r'^#{1,6}\s+\[(SECTION|SUBSECTION|FORMULA|BOX_|TABLE|RUNIN)', line):
            issues.append(('CRITICAL', ln, '## markdown prefix before tag - parser fails silently'))

    # B2: FORMULA title-style
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^\[FORMULA:\s*([^\]]+)\]', line)
        if m and not re.match(r'^name\s*=\s*\w+$', m.group(1).strip()):
            issues.append(('CRITICAL', ln, f'[FORMULA: {m.group(1)[:40]}] title-style - parser fails'))

    # B3: nested [BODY] in [BOX_*]
    for bt in ['BOX_KEY', 'BOX_EXAMPLE', 'BOX_WARN', 'BOX_NOTE', 'BOX_PURPLE']:
        pattern = rf'\[{bt}(?::[^\]]*)?\](.*?)\[/{bt}\]'
        for m in re.finditer(pattern, markup_text, re.DOTALL):
            if re.search(r'\[/?BODY\]', m.group(1)):
                ln = markup_text[:m.start()].count('\n') + 1
                issues.append(('CRITICAL', ln, f'[{bt}] contains nested [BODY] - renders as raw text'))

    # B4: BOX_KEY with worked calculation
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        eq_count = inner.count('=')
        nums = len(re.findall(r'\d+[.,]\d+', inner))
        if eq_count >= 4 and nums >= 6:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[BOX_KEY] has {eq_count} = and {nums} nums - move to BOX_EXAMPLE'))

    # B5: BODY with CHAINED calculation
    body_pattern = r'\[BODY\](.*?)\[/BODY\]'
    for m in re.finditer(body_pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        chained = re.findall(
            r'=\s*[\d.,$()×÷*+/\-\s]+[×÷*+\-/]\s*[\d.,$()\s]+\s*=\s*[\d.,\-$]',
            inner
        )
        if len(chained) >= 2:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[BODY] has {len(chained)} chained calcs - wrap in [BOX_EXAMPLE]'))

    # B6: Malformed [T:]] double bracket
    for ln, line in enumerate(lines, 1):
        if re.search(r'\[T:[^\]]+\]\]', line):
            issues.append(('CRITICAL', ln, 'malformed [T:]] - Vietnamese gloss does not render blue'))

    # B7: BOX_KEY too long
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, markup_text, re.DOTALL):
        inner = m.group(1).strip()
        if len(inner) > 600:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[BOX_KEY] {len(inner)} chars (target <300, max 600)'))

    # B8: Multiple RECAP_HANDOFF per section
    sections = re.split(r'^\[SECTION:', markup_text, flags=re.MULTILINE)
    for i, sec in enumerate(sections[1:], 1):
        rh_count = sec.count('[RECAP_HANDOFF]')
        if rh_count > 1:
            issues.append(('CRITICAL', 0, f'Section {i} has {rh_count} [RECAP_HANDOFF] - should be 1'))

    # ============== BATCH 2 (B9-B16) ==============

    # B9: BOX_KEY contains structure markers
    pattern = r'\[BOX_KEY\](.*?)\[/BOX_KEY\]'
    for m in re.finditer(pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        if re.search(r'(Bước\s+\d+:|Phương án\s+\w+:|Cách\s+\d+:|Tính:|Suy ra:)', inner):
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, '[BOX_KEY] contains worked-example structure - should be [BOX_EXAMPLE]'))

    # B10: BOX_EXAMPLE thin
    pattern = r'\[BOX_EXAMPLE(?::[^\]]*)?\](.*?)\[/BOX_EXAMPLE\]'
    for m in re.finditer(pattern, markup_text, re.DOTALL):
        inner = m.group(1).strip()
        if 20 < len(inner) < 200 and inner.count('\n\n') == 0:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[BOX_EXAMPLE] {len(inner)} chars single paragraph - too thin'))

    # B11: TABLE > 8 columns
    table_pattern = r'\[TABLE(?::[^\]]*)?\](.*?)\[/TABLE\]'
    for m in re.finditer(table_pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        header_match = re.search(r'^\s*header:\s*(.+)$', inner, re.MULTILINE)
        if header_match:
            cols = len(header_match.group(1).split('|'))
            if cols > 8:
                ln = markup_text[:m.start()].count('\n') + 1
                issues.append(('IMPORTANT', ln, f'[TABLE] {cols} columns (> 8) - overflows page'))

    # B12: TABLE > 15 rows
    for m in re.finditer(table_pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        rows = len(re.findall(r'^\s*row:', inner, re.MULTILINE))
        if rows > 15:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[TABLE] {rows} rows (> 15) - paginate'))

    # B13: RUNIN >= 5 sentences
    runin_pattern = r'\[RUNIN(?::[^\]]*)?\](.*?)\[/RUNIN\]'
    for m in re.finditer(runin_pattern, markup_text, re.DOTALL):
        inner = m.group(1).strip()
        sentences = len(re.findall(r'[.!?]\s+[A-ZÀ-ỹ]', inner))
        if sentences >= 5:
            ln = markup_text[:m.start()].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[RUNIN] {sentences}+ sentences - should be [BODY]'))

    # B14: 4+ consecutive same-type DIAGRAM
    diagram_types = []
    for ln, line in enumerate(lines, 1):
        m = re.match(r'^\[DIAGRAM:\s*(\w+)', line)
        if m:
            diagram_types.append((ln, m.group(1)))
    for i in range(len(diagram_types) - 3):
        if diagram_types[i][1] == diagram_types[i+1][1] == diagram_types[i+2][1] == diagram_types[i+3][1]:
            issues.append(('IMPORTANT', diagram_types[i][0], f'4+ consecutive [DIAGRAM: {diagram_types[i][1]}]'))

    # B15: §N in RECAP_HANDOFF mismatch
    section_count = len(re.findall(r'^\[SECTION:', markup_text, re.MULTILINE))
    rh_pattern = r'\[RECAP_HANDOFF\](.*?)\[/RECAP_HANDOFF\]'
    for m in re.finditer(rh_pattern, markup_text, re.DOTALL):
        inner = m.group(1)
        for ref_m in re.finditer(r'§(\d+)(?:\.\d+)?', inner):
            ref = int(ref_m.group(1))
            if ref > section_count + 1:
                ln = markup_text[:m.start()].count('\n') + 1
                issues.append(('CRITICAL', ln, f'[RECAP_HANDOFF] references §{ref} but only {section_count} sections'))
                break

    # B16: SECTION_OPEN preview subsection count mismatch
    so_pattern = r'\[SECTION_OPEN\](.*?)\[/SECTION_OPEN\]'
    section_chunks = re.split(r'(?=^\[SECTION:)', markup_text, flags=re.MULTILINE)
    for chunk in section_chunks[1:]:
        so_m = re.search(so_pattern, chunk, re.DOTALL)
        if not so_m:
            continue
        preview_match = re.search(r'preview:\s*(.+?)(?:\n|$)', so_m.group(1), re.DOTALL)
        if not preview_match:
            continue
        preview_text = preview_match.group(1)
        preview_subs = len(re.findall(r'§\d+\.\d+', preview_text))
        actual_subs = len(re.findall(r'^\[SUBSECTION:', chunk, re.MULTILINE))
        if preview_subs > 0 and actual_subs > 0 and abs(preview_subs - actual_subs) >= 2:
            ln = markup_text[:markup_text.find(chunk)].count('\n') + 1
            issues.append(('IMPORTANT', ln, f'[SECTION_OPEN] preview claims {preview_subs} subs but section has {actual_subs}'))

    # ============== BATCH 3 (B17) - DIAGRAM coverage ==============

    # B17 (NEW): Module >=6 sections AND 0 DIAGRAM -> CRITICAL
    section_count_b17 = len(re.findall(r'^\[SECTION:', markup_text, re.MULTILINE))
    subsection_count_b17 = len(re.findall(r'^\[SUBSECTION:', markup_text, re.MULTILINE))
    diagram_count_b17 = len(re.findall(r'^\[DIAGRAM:', markup_text, re.MULTILINE))
    body_count_b17 = len(re.findall(r'^\[BODY\]', markup_text, re.MULTILINE))

    if section_count_b17 >= 6 and diagram_count_b17 == 0:
        issues.append(('CRITICAL', 0,
            f'Module has {section_count_b17} SECTION + {subsection_count_b17} SUBSECTION but 0 DIAGRAM - figure_suggest Phase 4.5 was SKIPPED. Run figure_suggest.py or insert >=3 DIAGRAM before delivery.'))
    elif subsection_count_b17 >= 30 and diagram_count_b17 < 3:
        issues.append(('IMPORTANT', 0,
            f'Module has {subsection_count_b17} subsections but only {diagram_count_b17} DIAGRAM - visual variety insufficient, target >=3'))

    return issues



def run_render_check(markup_path, render_out_dir=None):
    issues = []
    if not render_out_dir:
        return issues
    skill_dir = os.environ.get('NOTE_RENDER_DIR',
                                '/sessions/tender-sleepy-pasteur/mnt/.claude/skills/note-pipeline-render/scripts')
    engine_path = os.path.join(skill_dir, 'render_engine.py')
    if not os.path.exists(engine_path):
        return issues
    try:
        result = subprocess.run(
            ['python3', '-c',
             f'import sys; sys.path.insert(0, "{skill_dir}"); '
             f'sys.argv = ["render_engine", "{markup_path}", "{render_out_dir}", '
             f'"--subject", "Test", "--module-num", "1", "--module-name", "Test"]; '
             f'import render_engine; render_engine.main()'],
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout + result.stderr
        m = re.search(r'Parsed (\d+) blocks; collected (\d+) terms, (\d+) formulas', output)
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3)), output
    except Exception as e:
        issues.append(('CRITICAL', 0, f'render_engine failed: {e}'))
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('markup_file')
    parser.add_argument('--render-out')
    args = parser.parse_args()

    with open(args.markup_file, 'r', encoding='utf-8') as f:
        markup_text = f.read()

    print("=== Post-Render Sanity Audit ===")
    print(f"File: {args.markup_file}")
    print()

    counts = count_markup_tags(markup_text)
    print("--- Markup tag inventory ---")
    for tag, n in counts.items():
        print(f"  [{tag}]: {n}")
    print()

    print("--- Anti-pattern detection ---")
    issues = detect_bad_patterns(markup_text)
    if not issues:
        print("  Clean - no anti-patterns detected")
    else:
        crit_count = sum(1 for s, _, _ in issues if s == 'CRITICAL')
        imp_count = sum(1 for s, _, _ in issues if s == 'IMPORTANT')
        print(f"  {crit_count} CRITICAL, {imp_count} IMPORTANT")
        for severity, ln, msg in issues[:30]:
            print(f"  [{severity}] L{ln}: {msg}")
        if len(issues) > 30:
            print(f"  ... and {len(issues) - 30} more")
    print()

    if args.render_out:
        print("--- Render-time mismatch check ---")
        result = run_render_check(args.markup_file, args.render_out)
        if isinstance(result, tuple):
            parsed_blocks, collected_terms, collected_formulas, _ = result
            print(f"  Render: {parsed_blocks} blocks, {collected_terms} terms, {collected_formulas} formulas")
            warnings = []
            expected_blocks = sum(counts[k] for k in ['SECTION', 'SUBSECTION', 'BODY', 'FORMULA',
                                                       'BOX_KEY', 'BOX_EXAMPLE', 'BOX_WARN',
                                                       'BOX_NOTE', 'INTUITION', 'TABLE', 'RUNIN',
                                                       'DIAGRAM', 'RECAP_HANDOFF'])
            if parsed_blocks < expected_blocks * 0.7:
                warnings.append(f'Parsed {parsed_blocks} << expected {expected_blocks}')
            if collected_formulas < counts['FORMULA'] * 0.5 and counts['FORMULA'] >= 2:
                warnings.append(f'Formulas {collected_formulas} << markup {counts["FORMULA"]}')
            if collected_terms < counts['TERM'] * 0.5 and counts['TERM'] >= 2:
                warnings.append(f'Terms {collected_terms} < markup {counts["TERM"]}')
            for w in warnings:
                print(f"  RED FLAG: {w}")
            if not warnings:
                print(f"  Counts consistent")
        else:
            for severity, ln, msg in result:
                print(f"  [{severity}] {msg}")
    else:
        print("--- Render-time check skipped ---")

    print()
    print("=== Verdict ===")
    crit = sum(1 for s, _, _ in issues if s == 'CRITICAL')
    imp = sum(1 for s, _, _ in issues if s == 'IMPORTANT')
    if crit > 0:
        print(f"FAIL - {crit} CRITICAL, {imp} IMPORTANT. Block release.")
        return 1
    elif imp > 0:
        print(f"PASS WITH WARNINGS - 0 CRITICAL, {imp} IMPORTANT.")
        return 0
    else:
        print("PASS - clean.")
        return 0


if __name__ == '__main__':
    sys.exit(main())
