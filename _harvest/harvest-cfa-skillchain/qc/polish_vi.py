#!/usr/bin/env python3
"""polish_vi.py - Vietnamese naturalization sweep (Phase 1.5 / polish_only subpath).

4-tier calque lexicon rebuilt and expanded from every documented lesson across
15+ module runs. Tier A is blanket-safe (auto-apply with --apply); Tiers B-D are
report-only context-dependent candidates for the humanize agent pass.

Hard rules preserved (NEVER touched by this script):
- 3 banned layers stay banned (pronouns, "hãy" imperatives, reader refs) — this
  script never introduces them and voice_check.py still enforces them.
- Protected zones: FORMULA blocks, [T:] tags, COVER, SECTION/SUBSECTION title lines,
  SECTION_OPEN/RECAP_HANDOFF field labels, TABLE/DIAGRAM/VIZ/FIGURE lines,
  name= params, image-hint Prompt lines (English by design).
- Protected collocations: technical phrases where the English word must stay.

Usage:
  python3 polish_vi.py MARKUP.md             # dry-run report
  python3 polish_vi.py MARKUP.md --apply     # write Tier A swaps in place
"""
import argparse, re, sys
from pathlib import Path

# ---------------------------------------------------------------- lexicon

# Tier A — blanket-safe prose swaps (case-preserving), from CLAUDE.md history sweeps
TIER_A = [
    ("khởi đi từ", "xuất phát từ"),
    ("lối vào", "cách tiếp cận"),
    ("driver", "động lực"),
    ("drivers", "các động lực"),
    ("framework", "khung phân tích"),
    ("decomposition", "phân tách"),
    ("mispricing", "định giá sai"),
    ("overvalue", "định giá cao"),
    ("undervalue", "định giá thấp"),
    ("efficiency", "hiệu quả"),
    ("operational", "vận hành"),
    ("simulation", "mô phỏng"),
    ("reconciliation", "đối chiếu"),
    ("insight", "nhận định"),
    ("insights", "các nhận định"),
    ("overview", "tổng quan"),
    ("perspective", "góc nhìn"),
    ("outcome", "kết quả"),
    ("architecture", "kiến trúc"),
    ("noise", "nhiễu"),
    ("financing", "tài trợ"),
    ("consistent với", "nhất quán với"),
    ("reasonableness", "tính hợp lý"),
    ("investigate", "xem xét"),
    ("missing", "thiếu"),
    ("intensity", "mức độ thâm dụng"),
    ("luxury goods", "hàng cao cấp"),
    ("divergence", "phân kỳ"),
    ("convergence", "hội tụ"),
    ("magnitude", "độ lớn"),
    ("robust", "vững"),
    ("robustness", "tính vững"),
    ("threshold", "ngưỡng"),
    ("trade-off", "đánh đổi"),
    ("tradeoff", "đánh đổi"),
]

# Tier B — context-dependent (REPORT ONLY)
TIER_B = [
    ("bị bào mòn", "bị xói mòn"),
    ("đối ứng", "đối xứng (nếu nói hình học) / tương ứng (nếu nói mapping)"),
    ("mang tính", "(thường thừa, xét bỏ)"),
    ("thực hiện việc", "(rút gọn: bỏ 'việc')"),
]

# Tier C — technical misuse (REPORT ONLY)
TIER_C = [
    ("tinh tế", "tinh chỉnh (trong ngữ cảnh kỹ thuật)"),
    ("bóc tách", "phân tách (chuẩn hơn trong phân tích)"),
]

# Tier D — Vietnamese awkward / machine-prose tells (REPORT ONLY)
TIER_D = [
    ("một cách", "(adverb calque: 'một cách nhanh chóng' → 'nhanh chóng')"),
    ("khá là", "(filler, xét bỏ)"),
    ("trong khi đó", "(nếu lặp >2 lần: thay bằng nối ý trực tiếp)"),
]

# Collocations where the English word must stay (checked ±34 chars around match)
PROTECTED_COLLOCATIONS = [
    "growth rate", "sustainable growth", "terminal growth", "growth phase",
    "implied growth", "dividend growth",
    "credit spread", "swap spread", "z-spread", "bid-ask spread", "option-adjusted",
    "tracking error", "active risk", "risk driver",
    "cash flow", "free cash flow",
    "efficiency ratio", "operational risk",  # giữ nguyên khi là tên measure chuẩn
    "monte carlo simulation",
]

# Tags whose whole line is protected
LINE_PROTECT = re.compile(
    r'^\s*(\[(COVER|SECTION|SUBSECTION|DIAGRAM|VIZ|FIGURE|TABLE|T):|'
    r'\[(/?)(FORMULA|SECTION_OPEN|RECAP_HANDOFF)\b|why_now:|preview:|recap:|handoff:|'
    r'\*\*Prompt|Prompt \(English\)|AI prompt:|Caption \(|\|)'
)

def in_formula_or_t(text, pos):
    pre = text[:pos]
    if pre.rfind("[FORMULA") > pre.rfind("[/FORMULA]"):
        return True
    # inside a [T: ...] tag span on the same line
    line_start = pre.rfind("\n") + 1
    line = text[line_start:text.find("\n", pos) if text.find("\n", pos) != -1 else len(text)]
    col = pos - line_start
    for m in re.finditer(r'\[T:[^\]]*\]', line):
        if m.start() <= col < m.end():
            return True
    return False

def collocation_protected(text, start, end):
    lo = max(0, start - 34); hi = min(len(text), end + 34)
    window = text[lo:hi].lower()
    return any(c in window for c in PROTECTED_COLLOCATIONS)

def preserve_case(src_word, repl):
    if src_word.isupper():
        return repl.upper()
    if src_word[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl

def sweep(text, apply_a=False):
    lines = text.split("\n")
    line_offsets = []
    off = 0
    for ln in lines:
        line_offsets.append(off)
        off += len(ln) + 1

    protected_lines = set()
    for idx, ln in enumerate(lines):
        if LINE_PROTECT.search(ln):
            protected_lines.add(idx)

    def line_of(pos):
        import bisect
        return bisect.bisect_right(line_offsets, pos) - 1

    report = {"A": [], "B": [], "C": [], "D": []}
    swaps = []  # (start, end, replacement)

    for eng, vn in TIER_A:
        for m in re.finditer(rf"(?i)\b{re.escape(eng)}\b", text):
            li = line_of(m.start())
            if li in protected_lines: continue
            if in_formula_or_t(text, m.start()): continue
            if collocation_protected(text, m.start(), m.end()): continue
            repl = preserve_case(m.group(0), vn)
            report["A"].append((li + 1, m.group(0), vn))
            swaps.append((m.start(), m.end(), repl))

    for tier, lex in (("B", TIER_B), ("C", TIER_C), ("D", TIER_D)):
        for pat, note in lex:
            for m in re.finditer(rf"(?i){re.escape(pat)}", text):
                li = line_of(m.start())
                if li in protected_lines: continue
                if in_formula_or_t(text, m.start()): continue
                report[tier].append((li + 1, m.group(0), note))

    new_text = text
    if apply_a and swaps:
        for s, e, r in sorted(swaps, key=lambda x: -x[0]):
            new_text = new_text[:s] + r + new_text[e:]
    return new_text, report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markup")
    ap.add_argument("--apply", action="store_true", help="Write Tier A swaps in place")
    ap.add_argument("--report", default=None, help="Write report md here")
    args = ap.parse_args()

    text = Path(args.markup).read_text(encoding="utf-8")
    new_text, report = sweep(text, apply_a=args.apply)

    total_a = len(report["A"])
    out = ["# Polish-VI report", "", f"File: {args.markup}", ""]
    out.append(f"## Tier A (blanket-safe) — {total_a} match" + (" [APPLIED]" if args.apply else " [DRY-RUN]"))
    for ln, src_w, vn in report["A"][:60]:
        out.append(f"- L{ln}: {src_w} → {vn}")
    for tier, label in (("B", "Tier B (context-dependent, review)"),
                        ("C", "Tier C (technical misuse, review)"),
                        ("D", "Tier D (machine-prose tells, review)")):
        items = report[tier]
        out.append("")
        out.append(f"## {label} — {len(items)} match")
        for ln, src_w, note in items[:40]:
            out.append(f"- L{ln}: '{src_w}' — {note}")

    report_text = "\n".join(out)
    if args.report:
        Path(args.report).write_text(report_text, encoding="utf-8")
    print(report_text[:2000])
    if args.apply and total_a:
        Path(args.markup).write_text(new_text, encoding="utf-8")
        print(f"\nAPPLIED {total_a} Tier A swaps.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
