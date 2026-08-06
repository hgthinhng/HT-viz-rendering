#!/usr/bin/env python3
"""humanize_check.py - Anti-AI-style detector cho teaching flow (Phase 3).

Bắt văn máy mà voice_check.py (vốn check banned constructs) không nhìn thấy:
nhịp câu đều tăm tắp, connector lặp công thức, mở đoạn trùng từ, chuỗi danh hoá,
filler dạy học rỗng. TÔN TRỌNG textbook voice: 3 lớp cấm giữ nguyên, detector này
chỉ nhắm "đúng luật nhưng đọc như máy".

Findings (advisory, exit 0; --strict exit 1 khi có HIGH):
  H01 RHYTHM_FLAT       : BODY ≥4 câu mà độ lệch độ dài câu quá thấp (đều tăm tắp)
  H02 CONNECTOR_LOOP    : connector công thức lặp dày ("Hơn nữa", "Bên cạnh đó", ...)
  H03 PARA_ECHO         : ≥3 BODY liên tiếp mở đầu bằng cùng một từ
  H04 NOMINAL_CHAIN     : chuỗi "việc/sự + động từ" hoặc ≥4 "của" trong một câu
  H05 STRAY_RECAP       : "Tóm lại" xuất hiện ngoài RECAP_HANDOFF (mất lực recap thật)
  H06 EMPTY_INTENSIFIER : "rất quan trọng", "vô cùng", "cực kỳ", "đặc biệt là" mật độ cao
  H07 FILLER_TEACHING   : "có thể thấy rằng", "cần lưu ý rằng", "không khó để nhận ra"...
  H08 NOT_ONLY_LOOP     : "không chỉ ... mà còn" dùng >2 lần trong module

Usage: python3 humanize_check.py MARKUP.md [--output humanize_report.md] [--strict]
"""
import argparse, re, statistics, sys
from pathlib import Path
from collections import defaultdict

CONNECTORS = ["hơn nữa", "bên cạnh đó", "ngoài ra", "đáng chú ý", "quan trọng hơn",
              "nói cách khác", "trên thực tế", "về bản chất"]
FILLERS = ["có thể thấy rằng", "cần lưu ý rằng", "không khó để nhận ra",
           "dễ dàng nhận thấy", "như một hệ quả tất yếu", "đóng vai trò quan trọng",
           "là một trong những"]
INTENSIFIERS = ["rất quan trọng", "vô cùng(?! nhỏ)", "cực kỳ", "hết sức"]

def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+(?=[A-ZĐÂÊÔƠƯÁÀẢÃẠ0-9§(])', text.strip())
    return [p for p in parts if len(p.split()) >= 3]

def body_blocks(text):
    """Yield (start_line, content) for each [BODY] block."""
    for m in re.finditer(r'\[BODY\](.*?)\[/BODY\]', text, re.DOTALL):
        ln = text[:m.start()].count("\n") + 1
        yield ln, m.group(1).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markup")
    ap.add_argument("--output", default="humanize_report.md")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    text = Path(args.markup).read_text(encoding="utf-8")
    # H06/H07/H08 đếm trên prose: loại FORMULA blocks (thuật ngữ toán như
    # "vô cùng nhỏ" trong where: không phải intensifier rỗng)
    prose = re.sub(r'\[FORMULA(?::[^\]]*)?\].*?\[/FORMULA\]', ' ', text, flags=re.DOTALL)
    low = prose.lower()
    findings = defaultdict(list)
    n_words = max(1, len(re.findall(r'\w+', text)))

    # H01: flat rhythm per BODY
    for ln, body in body_blocks(text):
        sents = split_sentences(body)
        if len(sents) >= 4:
            lengths = [len(s.split()) for s in sents]
            mean = statistics.mean(lengths)
            if mean > 0:
                cv = statistics.pstdev(lengths) / mean
                if cv < 0.18:
                    findings["H01_RHYTHM_FLAT"].append(
                        (ln, f"{len(sents)} câu, CV độ dài {cv:.2f} (<0.18): nhịp đều tăm tắp, "
                             f"trộn câu ngắn 6-10 từ với câu dài 25-30 từ"))

    # H02: connector density (per 1000 words)
    for c in CONNECTORS:
        cnt = len(re.findall(re.escape(c), low))
        if cnt >= 3 and cnt / n_words * 1000 > 0.8:
            first_ln = low.find(c)
            findings["H02_CONNECTOR_LOOP"].append(
                (low[:first_ln].count("\n") + 1, f"'{c}' xuất hiện {cnt} lần: đổi cách nối ý "
                                                 f"(nối bằng logic nội dung thay vì trạng ngữ)"))

    # H03: consecutive BODY opening with same first word
    opens = []
    for ln, body in body_blocks(text):
        first = re.match(r'\W*([\wÀ-ỹ]+)', body)
        opens.append((ln, first.group(1).lower() if first else ""))
    run_start, run_word, run_len = None, None, 0
    for ln, w in opens + [(None, "__end__")]:
        if w == run_word and w:
            run_len += 1
        else:
            if run_len >= 3 and run_word not in ("", "công", "ví"):
                findings["H03_PARA_ECHO"].append(
                    (run_start, f"{run_len} BODY liên tiếp mở đầu bằng '{run_word}'"))
            run_start, run_word, run_len = ln, w, 1

    # H04: nominalization chains
    for ln, body in body_blocks(text):
        for s in split_sentences(body):
            if s.count(" của ") >= 4:
                findings["H04_NOMINAL_CHAIN"].append((ln, f"≥4 'của' trong một câu: {s[:90]}"))
            if len(re.findall(r'\bviệc\s+\w+', s)) >= 3:
                findings["H04_NOMINAL_CHAIN"].append((ln, f"chuỗi 'việc + V': {s[:90]}"))

    # H05: stray "Tóm lại" outside RECAP_HANDOFF
    recap_spans = [(m.start(), m.end()) for m in
                   re.finditer(r'\[RECAP_HANDOFF\].*?\[/RECAP_HANDOFF\]', text, re.DOTALL)]
    for m in re.finditer(r'Tóm lại', text):
        if not any(a <= m.start() < b for a, b in recap_spans):
            findings["H05_STRAY_RECAP"].append(
                (text[:m.start()].count("\n") + 1, "'Tóm lại' ngoài RECAP_HANDOFF: recap giữa "
                                                   "chừng làm loãng recap cuối section"))

    # H06: empty intensifiers
    for w in INTENSIFIERS:
        cnt = len(re.findall(w, low))
        if cnt >= 3:
            findings["H06_EMPTY_INTENSIFIER"].append(
                (low.find(w) and low[:low.find(w)].count("\n") + 1,
                 f"'{w}' {cnt} lần: thay bằng lý do cụ thể vì sao quan trọng"))

    # H07: teaching fillers
    for w in FILLERS:
        cnt = len(re.findall(re.escape(w), low))
        if cnt >= 2:
            findings["H07_FILLER_TEACHING"].append(
                (low[:low.find(w)].count("\n") + 1, f"'{w}' {cnt} lần: nói thẳng nội dung"))

    # H08: "không chỉ ... mà còn" loop
    cnt = len(re.findall(r'không chỉ[^.\n]{0,80}mà còn', low))
    if cnt > 2:
        findings["H08_NOT_ONLY_LOOP"].append(
            (1, f"'không chỉ ... mà còn' {cnt} lần trong module: giữ tối đa 2"))

    # H09: SECTION_OPEN (why_now+preview) bị restate bởi BODY đầu section (seam kép).
    # FI_M2 lesson: chuỗi recap-handoff -> why_now -> bridge BODY nói cùng một ý ba lần.
    def _cw(s):
        s = re.sub(r'\[T:\s*([^|\]]+?)\s*\|[^\]]*\]', r'\1', s)
        ws = re.findall(r'[A-Za-zÀ-ỹ]{3,}', s.lower())
        stop = {'của','các','một','cho','với','trong','này','đến','được','khi','theo','như','tại','rằng'}
        return set(w for w in ws if w not in stop)
    for sm in re.finditer(r'\[SECTION_OPEN\](.*?)\[/SECTION_OPEN\](.*?)\[BODY\](.*?)\[/BODY\]', text, re.DOTALL):
        a, b = _cw(sm.group(1)), _cw(sm.group(3))
        if min(len(a), len(b)) >= 8:
            ov = len(a & b) / min(len(a), len(b))
            if ov > 0.45:
                ln = text[:sm.start()].count("\n") + 1
                findings["H09_OPEN_ECHO"].append(
                    (ln, f"BODY đầu section trùng {ov:.0%} từ vựng với why_now/preview: "
                         f"BODY phải đi thẳng vào nội dung mới, why_now đã làm nhiệm vụ nhìn lại"))

    total = sum(len(v) for v in findings.values())
    high = sum(len(v) for k, v in findings.items()
               if k in ("H01_RHYTHM_FLAT", "H03_PARA_ECHO", "H05_STRAY_RECAP", "H09_OPEN_ECHO"))
    out = ["# Humanize Report (anti-AI-style)", "",
           f"File: {args.markup}", f"Total findings: {total} (HIGH: {high})", ""]
    if not findings:
        out.append("CLEAN — flow đọc tự nhiên theo các tiêu chí đo được.")
    for code in sorted(findings):
        items = findings[code]
        out.append(f"## {code} ({len(items)})"); out.append("")
        for ln, msg in items[:25]:
            out.append(f"- L{ln}: {msg}")
        out.append("")
    out.append("LƯU Ý: detector đo được không thay được tai người đọc. Fix theo hướng: "
               "đa dạng nhịp câu, nối ý bằng logic, recap chỉ ở RECAP_HANDOFF, "
               "cụ thể thay vì cường điệu. KHÔNG thêm đại từ xưng hô khi sửa.")
    Path(args.output).write_text("\n".join(out), encoding="utf-8")
    print(f"Humanize report: {args.output}")
    print(f"Total: {total} findings (HIGH: {high})")
    return 1 if (args.strict and high) else 0

if __name__ == "__main__":
    sys.exit(main())
