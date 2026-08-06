# Severity Rubric — note-pipeline-audit

## Critical (Block publication)

Issue meets ANY of:
- Wrong definition of CFA core concept
- Missing core LOS coverage
- Foreign-language word leak (Indonesian/Malay/Tagalog) — E18 territory
- Structural bug breaking parser (truncated RECAP_HANDOFF, malformed tag)
- Subsection format inconsistency causing render failure
- Cross-reference §N to non-existent section
- Mathematical formula notation wrong
- Provider name leak in body (E05)

Resolution: MUST fix before delivery.

## Important (Should fix)

Issue meets ANY of:
- Sparse worked examples (≥5 subsections in section but <1 BOX_EXAMPLE)
- Inconsistent terminology (same concept 3+ different translations)
- Sequential listing in [BODY] that should be RUNIN (W16)
- Inline (i)(ii)(iii) listing in [BODY] that should be TABLE (W15)
- TABLE column count uneven across rows
- BOX type imbalance (BOX_KEY > 5/section without justification)
- RECAP_HANDOFF pair perfunctory (recap < 30 words OR handoff vague)
- SECTION_OPEN repetitive opener pattern (e.g., "§N-1 đã..." every section)
- Term tag missing on first appearance of CFA term
- Subsection title format drift (mix of `vi:` and no-prefix)

Resolution: Should fix; if many, propose generalization rule.

## Minor (Polish-level)

Issue meets ANY of:
- Sentence opener variety (top-3 dominate >40% of sentences in section, W12)
- Vietlish density 20-25% in BODY (W14)
- Paragraph length variance (some <20 words, some >150)
- Ornament placement (after every section vs. selective)
- Drop cap usage variance
- Spacing inconsistency between similar block types
- English-vs-Vietnamese balance in technical term mentions

Resolution: Note in audit report; fix if time permits; do not block.

## How to apply

For each finding:

1. Identify category (A-F)
2. Match against rubric above
3. Tag severity in finding line: `[Critical]`, `[Important]`, `[Minor]`
4. If 3+ findings have same severity in same subsection → consolidate into single critical/important issue at section level

Single-instance Minor → ignore.
Pattern Minor (3+ instances) → upgrade to Important.
Pattern Important (3+ instances) → upgrade to Critical.

## Generalization threshold

If a finding appears in 3+ sections (or 3+ modules in subject), it is SYSTEMIC. Propose:
- Validator rule (E## or W## code) to catch automatically
- Agent prompt update for Phase 1.3/1.4 to prevent
- Render engine patch if rendering issue

If finding appears <3 times, it is one-off. Note in report; do not generalize.
