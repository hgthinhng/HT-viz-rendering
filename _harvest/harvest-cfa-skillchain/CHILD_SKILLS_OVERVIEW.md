# Child Skills Overview

7 child skills coordinated by orchestrator (create · render · viz · qc · humanizer · audit · deliver). Each runs standalone or under orchestrator. Plus `note-pipeline-viz-library` = sub-dependency của viz (không dispatch trực tiếp).

## note-pipeline-create

**Role**: Source survey → outline → subsection plan → teaching script → markup conversion + validation

**Inputs**:
- 4 source PDFs (e.g., `5.EQ_M1_APP.pdf`, `5.EQ_M1_IFT.pdf`, ...)
- User decisions: font stack, build mode, subject color, hero image
- Module info: subject, module_num, module_name

**Outputs**:
- `ref_*.md` (4 source surveys, parallelized agents)
- `01_outline_{module}.md` (CHECKPOINT with user)
- `02_subsection_plan_{module}.md`
- `teaching_scripts/section_{1..N}.md` (prose, parallelized agents)
- `teaching_scripts/section_{1..N}.markup.md` (markup conversion)
- `{module}.markup.md` (assembled master, validated clean)

**Phases (legacy)**: 0, 1.0, 1.1, 1.2, 1.3, 1.4

## note-pipeline-render

**Role**: Markup → docx + PDF + screenshots

**Inputs**:
- `{module}.markup.md`
- Subject, module_num, module_name (CLI args)
- Build mode (print|digital|both), font stack (A|B|C)

**Outputs**:
- `{module}.docx`
- `{module}.pdf` (via libreoffice)
- `qc_screenshots/p_*.png` (8-10 representative pages)

**New visual primitives** (refactor enrichment):
- `[DIAGRAM: matrix2x3]`, `[DIAGRAM: pyramid]`, `[DIAGRAM: cycle]`, `[DIAGRAM: comparison]`, `[DIAGRAM: gauge]`
- Inline: `[KEYWORD]`, `[CALLOUT]`, `[ICON]`, `[LAYOUT: 2col]`

**Phases (legacy)**: 2.1, 2.2, 2.3

## note-pipeline-viz

**Role**: Data figures — advise → author [VIZ] markers + spec → render PNG → insert [FIGURE:]

**Inputs**: `{module}.markup.md`, spec.json

**Outputs**: `[FIGURE:]` blocks + PNGs (`work_{module}/viz_out/`), markup re-rendered

**Engine (CHUẨN 2026-07)**: matplotlib mặc định — (a) 10 core + 95 KHO KHUÔN (`viz_render_py.py`/`viz_render.py`); (b) **48 EIR super-viz-factory** qua skill con `note-pipeline-viz-library/scripts/viz_super.py`. viz-factory PowerShell = LEGACY chỉ Windows. **Ưu tiên viz-rich (5-9 figure module tính toán) + BẮT BUỘC GATE VIZ (soi từng PNG, không chồng chữ/legend).**

**Standalone**: YES — "render viz", "thêm chart".

## note-pipeline-viz-library (sub-dependency của viz, KHÔNG dispatch trực tiếp)

**Role**: Kho 48 component EIR institutional (matplotlib PNG — dumbbell/fan/football_field/tornado/sankey/decision_tree/scenario_cards/exec_dashboard...), dùng BỞI note-pipeline-viz qua `viz_super.py` (cùng spec.json contract). Advisor + params: `references/CATALOG.md`; design: `EIR_DESIGN.md`.

## note-pipeline-qc

**Role**: Voice + cross-reference QC + cross-source supplements

**Inputs**:
- `{module}.markup.md`, `{module}.docx`
- Source ref files (`ref_*.md`)

**Outputs**:
- `voice_qc_report.md` (banned words, Vietlish density per block)
- `cross_ref_check.md` (§N references valid)
- `supplement_blocks.md` (cross-source insights to add, if marked mode)

**Phases (legacy)**: 3, 4

## note-pipeline-humanizer

**Role**: Phase 3 — áp giọng Việt "thầy đã đi thi" (BẮT BUỘC, GATE VOICE)

**Inputs**: `{module}.markup.md`, `references/VOICE_PROFILE.md` (distill 102 module note user)

**Outputs**: markup đã humanize giọng (song ngữ Anh-Việt, ví dụ VN thật, bẫy thi)

**Standalone**: YES — "humanize", "áp giọng".

## note-pipeline-audit

**Role**: Independent harsh review (audit by fresh agent, not maker)

**Inputs**:
- `{module}.markup.md`, `{module}.docx`
- Source ref files

**Outputs**:
- `_audit_state.json` (Phase A inventory)
- `_audit_voice.md`, `_audit_structure.md`, `_audit_flow.md`, etc. (Phase B per category)
- `AUDIT_REPORT_{module}.md` (synthesized final)
- `_skill_updates.md` (generalization proposals)
- `_autofix_diff.md` (if --autofix run)

**Standalone**: YES — can run without orchestrator. User invokes "/note-pipeline-audit {markup}".

## note-pipeline-deliver

**Role**: Final package + handoff + CLAUDE.md update

**Inputs**:
- `{module}.docx`, audit report, working files
- Subject handoff template

**Outputs**:
- Copy `{module}.docx` to workspace folder (user-visible)
- Write/update `{subject}_handoff.md` (subject continuity)
- Update `CLAUDE.md` with module log entry
- Generate colophon page for docx (optional)

**Phases (legacy)**: 5

## Standalone vs orchestrated

| Skill | Standalone? | Orchestrator? |
|-------|-------------|---------------|
| note-pipeline-create | YES (with explicit inputs) | YES |
| note-pipeline-render | YES (just need markup file) | YES |
| note-pipeline-viz | YES ("render viz") | YES (Phase 4.6) |
| note-pipeline-qc | YES | YES |
| note-pipeline-humanizer | YES ("humanize") | YES (Phase 3, BẮT BUỘC) |
| note-pipeline-audit | YES (most common standalone) | YES (after deliver, optional) |
| note-pipeline-deliver | YES | YES |

Orchestrator coordinates state, but each child can run independently if user knows what they want.

## v2 contract additions (2026-06-10 upgrade)

| Child | Nhận từ orchestrator | Trả về | Gate sau nó |
|-------|---------------------|--------|-------------|
| create | module_id, source PDFs (1/LOS cho L1, 1/PDF cho L2-L3), user_decisions | markup.md validated | GATE 1 |
| qc (1.5 polish-vi) | markup.md | markup.md đã sweep Tier A, swaps count | GATE 1 re-run nếu đổi |
| render | markup.md, --subject-color, --numbering | docx + render summary (block counts) | GATE 2 + Visual QC 2.3 |
| qc (3, 4) | markup.md, ref_*.md | voice report + humanize report + supplement proposals | — |
| qc (4.5 image hints) | markup.md | BOX_NOTE image-hint blocks inserted | GATE 1 re-run |
| viz (4.6) | markup.md, spec | [FIGURE:] blocks + PNGs (matplotlib mặc định: core/KHO KHUÔN + **48 EIR qua viz_super.py**; viz-factory PS legacy) — ưu tiên viz-rich + GATE VIZ | GATE 2 re-run |
| audit (4.7 numeric) | markup.md, ref_*.md | numeric_checklist.md verified, mismatches list | HARD STOP nếu mismatch |
| audit (5) | docx + markup + ref_*.md | audit report 6 category | fixes → re-render |
| deliver (6) | docx final | file ở workspace + handoff + CLAUDE.md entry | GATE 3 trước khi declare |

**Nguyên tắc bất biến**: child không gọi child; mọi handoff đi qua orchestrator + state file; mọi sửa markup sau gate làm gate đó `stale`.
