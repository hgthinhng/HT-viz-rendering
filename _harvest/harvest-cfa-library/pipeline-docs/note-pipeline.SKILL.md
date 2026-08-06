---
name: note-pipeline
description: Orchestrator skill cho pipeline xuất bản CFA Level II study note end-to-end. Coordinate 6 child skills (note-pipeline-create, note-pipeline-render, note-pipeline-viz, note-pipeline-qc, note-pipeline-audit, note-pipeline-deliver). LUÔN dùng skill này khi user yêu cầu "tạo note", "build note", "make CFA note", "render lại docx", "audit note", "kiểm tra độc lập", "deliver note", "render viz", "thêm chart", "build figures", hoặc "/note-pipeline {command}". KHÔNG gọi child skill trực tiếp trừ khi user explicit chỉ định 1 phase cụ thể.
---

# note-pipeline — Orchestrator

## Purpose

Pipeline xuất bản end-to-end cho CFA Level II study note. Đọc user intent, classify action, dispatch tới child skill phù hợp, manage state qua `_pipeline_state.json`.

## When to invoke

User says ONE of:
- "tạo note mới [module]", "build note [module]", "create note for [module]"
- "render lại docx", "re-render", "rebuild docx"
- "audit", "harsh review", "kiểm tra độc lập"
- "fix voice", "voice check"
- "supplement", "bổ sung note"
- "deliver", "pack final"
- "render viz", "thêm chart", "build figures", "vẽ hình cho note"
- "resume"
- "/note-pipeline {action}"

## Child skills coordinated

| Child | Purpose | Phases |
|-------|---------|-----------------|
| note-pipeline-create | Source survey → outline → teaching script → markup | 0, 1.0-1.4 |
| note-pipeline-render | Markup → docx → screenshots | 2.1-2.3 |
| note-pipeline-qc | Voice check + cross-source supplements | 3, 4 |
| note-pipeline-viz | Data figures qua viz-factory: advise → spec → render → insert [FIGURE:] | 4.6 |
| note-pipeline-audit | Independent harsh review + sanity audits | post-2, post-5 |
| note-pipeline-deliver | Final pack + handoff + CLAUDE.md update | 5 |

## Workflow

### 1. Read user intent

Map keywords to action.

### 2. Initialize / read state

Run `scripts/state_init.py {module_id}`. State location: `work_{module}/{module_id}_state.json`.

### 3. Classify intent precisely

`scripts/intent_classifier.py "{user_message}"` returns JSON.

### 4. Dispatch with MANDATORY GATE ENFORCEMENT

Based on action, invoke child skills in order with hard gates:

**create_full**: create → **GATE 1: validator E* = 0** → render → **GATE 2: sanity audit CRITICAL = 0** → qc → (4.5 image hints cho hình conceptual) → (4.6 viz: data figures, optional) → audit → deliver → **GATE 3: render output audit CRITICAL = 0**  
**render_only**: render → **GATE 2: sanity audit CRITICAL = 0**  
**audit_only**: audit  
**qc_only**: qc  
**supplement_only**: qc (supplement subpath)  
**deliver_only**: deliver → **GATE 3: render output audit CRITICAL = 0**  
**viz_only**: viz (Pass A author → Pass B render hoặc manifest → Pass C insert) → render → **GATE 2** → **GATE 3**  
**resume**: read state, find first phase != complete

**Gate enforcement rules** (HARD STOP if violated):

#### GATE 1: After Phase 1.4 Markup Conversion

```bash
python3 .claude/skills/note-pipeline-create/scripts/validate_markup.py work_{module}/{module_id}.markup.md
```

- If exit code != 0 (any E01-E35) → **STOP pipeline**, fix markup, re-validate
- DO NOT proceed to render until 0 errors
- Warnings (W*) are advisory only

#### GATE 2: After Phase 2 Render

```bash
python3 .claude/skills/note-pipeline-audit/scripts/audit_render_sanity.py \
  work_{module}/{module_id}.markup.md \
  --render-out=/tmp/render_sanity_check
```

- If CRITICAL count > 0 → **STOP pipeline**, fix markup, re-render
- B1-B6 are CRITICAL: `## ` prefix, FORMULA: title-style, BODY in BOX, BOX_KEY worked calc, BODY worked calc, [T:]]
- B7-B16 are IMPORTANT: review but pipeline can proceed

#### GATE 3: After Phase 5 Delivery (before user handoff)

```bash
python3 .claude/skills/note-pipeline-audit/scripts/audit_render_output.py \
  path/to/{module_id}.docx \
  --markup work_{module}/{module_id}.markup.md \
  --expected-pages 30-50
```

- If CRITICAL count > 0 → **STOP delivery**, investigate render output
- Catches: unrendered tags in PDF text, formula color-coding missing, term gloss not blue, XML invalid, page count out of range
- This is MANDATORY before declaring "delivered" to user

#### Phase 4.6: Viz (data figures qua viz-factory, optional)

Child skill `note-pipeline-viz`. Phân công với Phase 4.5: **image hints (BOX_NOTE + DALL-E prompt) cho hình minh hoạ conceptual** (user tự generate qua trình tạo ảnh chuyên dụng); **viz-factory cho data figures** (chart, bảng pivot, payoff, tree, waterfall... với số liệu THẬT từ prose). Ba pass:

1. **Pass A (advise + author)**: áp parsimony test, chèn `[VIZ: component | id=N.M.x | caption=... | params={...}]` vào markup, sinh spec.json.
2. **Pass B (render)**: resolve VIZ_ROOT, chạy `build_spec.ps1` (PowerShell + headless Chrome). Môi trường không render được (Cowork Linux sandbox): ghi `render_manifest.md` chứa 1 lệnh PowerShell cho user, DỪNG chờ, không đoán.
3. **Pass C (insert)**: thay `[VIZ:]` marker bằng `[FIGURE: <png path> | Hình N.M.x: caption]` (scripts/figures_insert.py), re-render docx. `[VIZ:]` chưa render hiển thị thành placeholder strip trong docx, không phải lỗi.

Validator: W30 ([FIGURE] path thiếu), W31/W32 ([VIZ] thiếu id/caption, id trùng). GATE 2/3 vẫn áp dụng sau re-render.

**Bug pattern from EQ_M2 first run**: render reported "0 formulas collected" cho 20 FORMULA tags in markup, all rendered as raw text. Sanity check would catch this.

**Gate 1 + Gate 2 + Gate 3 must ALL pass before delivery**. If any gate fails:
1. Document failure in state file
2. Fix root cause (don't workaround)
3. Re-run from failed phase
4. Re-validate ALL prior gates (regression check)

### 5. Coordinate handoffs

After each child completes, update state file. Next child reads state.

### 6. Final report

Present user with:
- Summary of phases executed
- File paths to deliverables
- Key metrics
- Critical issues if any

## Critical rules

1. **NEVER call child skills outside orchestrator without explicit user permission**.
2. **State file is single source of truth**.
3. **Child skills must NOT call other child skills directly**.
4. **If child fails or any GATE fails, orchestrator stops**.
5. **Backward compatibility**: Old monolithic at `.claude/skills/note-pipeline-legacy/`.

## Files in this orchestrator skill

```
note-pipeline/
├── SKILL.md (this)
├── references/
│   ├── INTENT_ROUTING.md
│   ├── STATE_SCHEMA.md
│   └── CHILD_SKILLS_OVERVIEW.md
└── scripts/
    ├── state_init.py
    └── intent_classifier.py
```

Child skill mới: `note-pipeline-viz/` (SKILL.md + scripts/figures_insert.py + scripts/viz_env_check.py).
viz-factory engine KHÔNG nằm trong skill nào - là folder độc lập (xem note-pipeline-viz/SKILL.md mục VIZ_ROOT).
```
```

## Backward compatibility

Old `note-pipeline` skill (monolithic) is preserved as `note-pipeline-legacy`.
