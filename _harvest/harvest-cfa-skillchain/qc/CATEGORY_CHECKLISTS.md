# Category Checklists — note-pipeline-audit

Detailed checks per audit category. Use when running Phase B sub-agents.

## A. Voice & Language Quality

### A.1 Banned constructs (mechanical, validator catches but verify)
- [ ] Zero `bạn`, `tôi`, `ta`, `mình`, `chúng ta`, `chúng tôi`, `các bạn`
- [ ] Zero `hãy + verb` imperatives
- [ ] Zero `người đọc`, `người thi`, `người học`, `học viên`, `sinh viên`, `thí sinh`
- [ ] Zero provider names (Schweser, Kaplan, AnalystPrep, UWorld, IFT World, Hull, Fabozzi)
- [ ] Zero source markers (`như đã nói ở trên`, `phần trước đã trình bày`)
- [ ] Zero em-dashes / `--`

### A.2 Foreign-language leak
- [ ] No Indonesian/Malay: `memiliki`, `untuk`, `adalah`, `atau`, `dapat`, `saya`, `kamu`, `mereka`, `menjadi`, `membuat`, `dengan`, `dari`, `harus`, `bisa`
- [ ] No Tagalog: `nakaka`, `naging`, `maaari`
- [ ] No Spanish/Portuguese: `para`, `como` (in non-technical context)

### A.3 Vietlish density
- [ ] No BODY block has >25% English-like words (4+ ASCII letters)
- [ ] Heavy English verbs (signaling, extrapolating, capitalized) used <3 times per section
- [ ] Each sentence predominantly one language (no "force chúng ta confront" mix)

### A.4 Terminology consistency
- [ ] Concept appearing 3+ times has same Vietnamese translation throughout
- [ ] First appearance has [T: english | vietnamese] tag
- [ ] Subsequent appearances use English form (no random Vietnamese substitution)

### A.5 Pedagogical voice warmth
- [ ] Sentences vary in length (not all short, not all long)
- [ ] Section_open / why_now uses varied openers (not all "§N-1 đã...")
- [ ] At least 1 question form per subsection (rhetorical or framing)
- [ ] No 4+ consecutive sentences in passive voice

---

## B. Visual Structure

### B.1 Subsection format
- [ ] All `[SUBSECTION:]` use SAME pattern across module:
  - Pattern A: `[SUBSECTION: en | vi: vn]` (legacy, still works)
  - Pattern B: `[SUBSECTION: en | vn]` (new, no prefix)
  - DO NOT mix patterns within same module
- [ ] No subsection numbering (e.g., "1.1") — bare title only

### B.2 RUNIN coverage
- [ ] Sequential listings (Bước N, Lực N, Thành phần N, Chiến lược N, Tiêu chí N, Mục đích N, Giai đoạn) use [RUNIN: prefix]content[/RUNIN]
- [ ] No [BODY] starting with "Thứ nhất," "Thứ hai," "Thứ ba" 3+ times consecutively
- [ ] No (i)(ii)(iii) inline listing 4+ items long inside BODY (extract to TABLE)

### B.3 DIVIDER usage
- [ ] DIVIDER count <= 1 per subsection
- [ ] DIVIDER NEVER adjacent to TABLE/DIAGRAM/BOX/SUBSECTION/RECAP_HANDOFF/INTUITION/RUNIN
- [ ] DIVIDER only between two BODYs that have thematic break

### B.4 TABLE quality
- [ ] All rows have same column count as header
- [ ] Header cells <= 4 columns (more = hard to read)
- [ ] Row content not heavily fragmented (each cell 5-30 words)
- [ ] Title descriptive (not "Bảng so sánh" generic)

### B.5 DIAGRAM coverage
- [ ] Each major section has ≥1 DIAGRAM (flow, hub, tree2x2, timeline, payoff)
- [ ] No DIAGRAM placeholder text without actual params
- [ ] DIAGRAM placement: not adjacent to TABLE (visual collision)

### B.6 BOX_PURPLE structure
- [ ] BOX_PURPLE blocks contain Layout/Elements/Relationships sections
- [ ] No color suggestions in BOX_PURPLE (palette handles)
- [ ] Each BOX_PURPLE describes ONE diagram (not multiple)

### B.7 Page break
- [ ] Each [SECTION] starts on new page (page break before section_num > 1)
- [ ] No section_tab right-margin colored dashes (disabled)

---

## C. Pedagogical Flow

### C.1 SECTION_OPEN
- [ ] Each [SECTION] except possibly §1 has [SECTION_OPEN] block
- [ ] why_now references §N-1 motivation
- [ ] preview lists 3-5 subsections this section will cover
- [ ] why_now opener varies (not all "§N-1 đã...")

### C.2 RECAP_HANDOFF
- [ ] Each [SECTION] ends with [RECAP_HANDOFF]
- [ ] recap is substantive (≥30 words, summarizes 3-5 key points)
- [ ] handoff is specific (≥20 words, names §N+1 question)
- [ ] No truncated RECAP_HANDOFF (parser will hang)

### C.3 Cross-references
- [ ] All §N refs point to existing sections (validator E13)
- [ ] §N.M refs point to actual subsections
- [ ] Forward references (§N to §N+k) actually deliver promised content
- [ ] Backward references match the original definition

### C.4 BODY chains
- [ ] No 4+ consecutive [BODY] without separator (RUNIN, BOX, FORMULA, TABLE, DIAGRAM, INTUITION, DIVIDER) (W08)
- [ ] If validator flags W08, agent should MERGE bodies, not auto-DIVIDER

### C.5 Drop cap & ornament
- [ ] Drop cap on first paragraph of each section (handled by render engine)
- [ ] Ornament placement: not after every section (selective, end-of-major-thematic-block)

---

## D. Technical Correctness

### D.1 Formulas
- [ ] All [FORMULA] blocks have `where:` section
- [ ] Notation consistent (V_E vs V_E, P vs P, lower case)
- [ ] Subscripts braced for multi-char (`R_f`, `l_{t,s}`)
- [ ] Superscripts braced for `+/-/*` (`P^{+}`, `S^{-}`)
- [ ] No unknown LaTeX commands (validator E09)
- [ ] No nested braces in sub/sup (E10)

### D.2 Definitions
- [ ] CFA core concept definitions match standard:
  - Intrinsic value: "Giá trị tài sản dưới sự hiểu biết hoàn chỉnh"
  - Going-concern: "Công ty tiếp tục hoạt động bình thường"
  - Liquidation value: "Giá trị tài sản trừ nợ nếu giải thể"
  - Fair value (accounting): "Giá trao đổi orderly giữa market participants"
  - Investment value: "Giá trị riêng cho buyer cụ thể với synergy"
- [ ] Corporate event definitions distinguish:
  - Merger: hợp nhất
  - Acquisition: mua lại
  - Divestiture: bán bộ phận
  - Spin-off: tách thành pháp nhân riêng (cổ phiếu phát hành theo tỷ lệ)
  - Split-off: đổi cổ phiếu mẹ lấy cổ phiếu con (voluntary)

### D.3 Numerical examples
- [ ] At least 1 worked numerical example per major formula
- [ ] Examples use realistic numbers (not toy ratios like 100%, 50%)
- [ ] Each example has setup → calculation → check

### D.4 Cross-reference content match
- [ ] Forward ref §N+k content matches what current section claims
- [ ] Backward ref §N-k content matches definition

---

## E. Consistency

### E.1 Subsection title format
- [ ] All sections use SAME pattern (en | vi or en | vi: vn)
- [ ] No numbering ("1.1", "2.1") in some sections but not others

### E.2 Term tagging
- [ ] [T:] tag on first appearance of all 30+ key concepts
- [ ] Vietnamese explanation in tag is concise (<15 words)
- [ ] Subsequent appearances use English form

### E.3 Subject-level conventions
- [ ] Subject color consistent (cover + section tabs)
- [ ] Font stack consistent (B Inter throughout, no mixing)
- [ ] Notation conventions match subject_handoff.md (V_E, P, V, etc.)

### E.4 Listing prefix style
- [ ] Sequential listings use uniform prefix:
  - "Bước 1, English title" (RUNIN format)
  - "Lực 1, Vietnamese (English)" (RUNIN format)
  - Consistent across listings within same section

### E.5 Module numbering in handoff
- [ ] handoff uses "M2", "M3" etc. consistently (not mix M2 and Module 2)

---

## F. Completeness vs Source Material

### F.1 LOS coverage
- [ ] All N LOS from source surveys covered (cross-check ref_*.md)
- [ ] Each LOS has at least 1 subsection or substantive treatment

### F.2 Critical concepts
- [ ] APP, IFT, SCH, UWD distinctive insights preserved
- [ ] Source-specific frameworks (e.g., Porter Five Forces) attributed correctly
- [ ] If 3+ sources mention concept, must include

### F.3 Numerical example density
- [ ] At least 1 worked example per 4-5 subsections
- [ ] Quantitative example for each calculable concept
- [ ] Narrative example for each structural concept

### F.4 Edge cases / caveats
- [ ] Important warnings from sources (e.g., "Avoid extrapolating past performance") included
- [ ] Counter-arguments / alternative perspectives mentioned
- [ ] Real-world failure cases (Enron, WorldCom, etc.) cited

---

## How to use this checklist

When running Phase B sub-agent for a category:

1. Open this file, find the category section
2. Go through each checkbox systematically
3. For each FAIL, document:
   - Location (section, subsection, line if applicable)
   - Description of issue
   - Severity (Critical / Important / Minor per SEVERITY_RUBRIC.md)
4. Output `_audit_{category}.md` with structured findings

After all 6 categories done, run synthesize.

If 3+ findings same type → propose generalization rule per GENERALIZATION_GUIDE.md.
