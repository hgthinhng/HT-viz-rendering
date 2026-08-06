---
name: note-pipeline
description: Orchestrator skill cho pipeline xuất bản CFA Level I/II/III study note end-to-end. Coordinate 7 child skills (note-pipeline-create, note-pipeline-render, note-pipeline-viz, note-pipeline-qc, note-pipeline-humanizer, note-pipeline-audit, note-pipeline-deliver). LUÔN dùng skill này khi user yêu cầu "tạo note", "build note", "make CFA note", "render lại docx", "audit note", "kiểm tra độc lập", "deliver note", "render viz", "thêm chart", "build figures", "polish tiếng Việt", "humanize giọng văn", hoặc "/note-pipeline {command}". KHÔNG gọi child skill trực tiếp trừ khi user explicit chỉ định 1 phase cụ thể.
---

# note-pipeline — Orchestrator

## Purpose

Pipeline xuất bản end-to-end cho CFA Level I/II/III study note. Đọc user intent, classify action, dispatch tới child skill phù hợp, enforce gates, manage state qua `_pipeline_state.json`. Orchestrator là nơi DUY NHẤT quyết định thứ tự phase và điều kiện dừng.

## Child skills coordinated

| Child | Purpose | Phases owned |
|-------|---------|--------------|
| note-pipeline-create | Source survey → outline → teaching script → markup | 0, 1.0-1.4 |
| note-pipeline-render | Markup → docx → screenshots | 2.1-2.3 |
| note-pipeline-qc | Polish-vi + cross-source supplements + image hints | 1.5, 4, 4.5 |
| note-pipeline-humanizer | **BẮT BUỘC** — áp giọng Việt "thầy đã đi thi" (VOICE_PROFILE distill từ 102 module note user) | 3 |
| note-pipeline-viz | Data figures: advise → spec → render (matplotlib mặc định + **48 EIR** qua note-pipeline-viz-library/`viz_super.py`; viz-factory PowerShell = legacy) → insert; ƯU TIÊN viz-rich + GATE VIZ | 4.6 |
| note-pipeline-audit | Sanity audits + numeric verification + independent harsh review | gates, 4.7, 5 |
| note-pipeline-deliver | Final pack + handoff + CLAUDE.md update | 6 |

## Canonical phase map (create_full)

```
Phase 0     Intake + state init                    [create]
Phase 1.0   Source survey (1 agent/LOS cho L1; 1/PDF cho L2-L3; song song ≤2) [create]
Phase 1.1   Outline — CHECKPOINT với user          [create]
Phase 1.2   Subsection plan                        [create]
Phase 1.3   Teaching scripts (song song ≤2)        [create]
Phase 1.4   Markup conversion + assemble           [create]
── GATE 1   validate_markup.py exit 0 ──────────────────────
Phase 1.5   Polish-VI Tier A (deterministic)       [qc]
Phase 2.1   Render docx                            [render]
Phase 2.2   Pack + PDF nội bộ                      [render]
── GATE 2   audit_render_sanity CRITICAL = 0 ───────────────
Phase 2.3   VISUAL QC BẮT BUỘC (screenshots)       [render]
Phase 3     HUMANIZE giọng Việt — BẮT BUỘC         [humanizer]
── GATE VOICE  áp VOICE_PROFILE qua note-pipeline-humanizer ─
Phase 3.5   RE-RENDER docx (markup đã đổi) + GATE 2 [render]
Phase 4     Cross-source supplement assessment     [qc]
Phase 4.5   Image hints (conceptual, BOX_NOTE)     [qc]
Phase 4.6   Viz data figures (optional)            [viz]
Phase 4.7   NUMERIC VERIFICATION BẮT BUỘC          [audit]
Phase 5     Independent harsh audit + fixes        [audit]
── GATE 3   audit_render_output CRITICAL = 0 ───────────────
Phase 6     Deliver + handoff + CLAUDE.md          [deliver]
```

Mỗi lần markup bị sửa SAU một gate, gate đó phải chạy lại trước khi đi tiếp (regression rule).

## Workflow

### 1. Classify intent

```bash
python3 scripts/intent_classifier.py "{user_message}"
```

Trả JSON `{action, module_id, subject, module_num, needs_clarification}`. Nếu thiếu module_id hoặc action: hỏi user qua AskUserQuestion, KHÔNG đoán.

### 2. Initialize / read state

```bash
python3 scripts/state_init.py {module_id}
```

State: `work_{module}/{module_id}_state.json`. Nếu state đã tồn tại và last activity < 24h, mặc định đề nghị resume thay vì tạo lại.

### 3. Detect environment (trước khi dispatch)

| Check | Cách detect | Ảnh hưởng |
|-------|------------|-----------|
| Matplotlib (mặc định Cowork) / PowerShell legacy | `viz_env_check.py` | Phase 4.6: python/matplotlib mặc định; viz-factory PS chỉ khi user explicit trên Windows |
| matplotlib | `python3 -c "import matplotlib"` | Python fallback renderer khả dụng |
| libreoffice + pdftoppm | `which libreoffice pdftoppm` | Phase 2.3 screenshot được hay chỉ XML-level QC |
| Cowork mount | path chứa `/mnt/` | zip qua /tmp trước rồi cp; folder render mới mỗi lần; KHÔNG rm trong render_out |

Ghi kết quả vào `state["environment"]`.

### 4. Dispatch theo bảng

| action | Chuỗi thực thi | Gates |
|--------|----------------|-------|
| `create_full` | create → qc(1.5) → render → **humanizer(3, BẮT BUỘC)** → **re-render docx + GATE 2 (docx phải khớp bản humanize)** → qc(4) → viz? → audit(4.7) → audit(5) → deliver | 1, 2, 3, **VOICE** |
| `create_only` | create | 1 |
| `render_only` | render | 2 |
| `qc_only` | **humanizer(3)** + qc (polish/supplement subpath) | **VOICE** |
| `polish_only` | qc (polish-vi) → **humanizer(3)** → nếu markup đổi: render → GATE 2 | 2 nếu re-render, **VOICE** |
| `supplement_only` | qc (supplement subpath) → render → GATE 2 | 2 |
| `viz_only` | viz (Pass A→B→C) → render → GATE 2 → GATE 3 | 2, 3 |
| `figure_suggest_only` | qc (image-hint subpath, Phase 4.5) | — |
| `audit_only` | audit (5; thêm 4.7 nếu chưa từng chạy) | — |
| `deliver_only` | deliver | 3 |
| `resume` | đọc state, chạy từ phase đầu tiên != complete | gates còn thiếu |

### 5. Gate enforcement (HARD STOP)

> **SKILLS_ROOT resolution**: `<SKILLS_ROOT>` = nơi deploy skill — Claude Code: `%USERPROFILE%\.claude\skills`; trên Cowork/mount khác: folder chứa các skill `note-pipeline-*`. Thay `<SKILLS_ROOT>` bằng đường thật của môi trường trước khi chạy (tránh hardcode path không resolve).

#### GATE 1 — sau Phase 1.4

```bash
python3 <SKILLS_ROOT>/note-pipeline-create/scripts/validate_markup.py work_{module}/{module_id}.markup.md
```

Exit != 0 (bất kỳ E*) → STOP, fix markup, re-validate. W* chỉ advisory.

#### GATE 2 — sau Phase 2.2

```bash
python3 <SKILLS_ROOT>/note-pipeline-audit/scripts/audit_render_sanity.py \
  work_{module}/{module_id}.markup.md --render-out=/tmp/render_sanity_check
```

CRITICAL > 0 → STOP. KHÔNG BAO GIỜ bỏ qua mismatch giữa "Parsed N blocks / collected M formulas" và tag count trong markup, đó là silent parser fail, không phải "known issue".

#### Phase 2.3 — Visual QC bắt buộc (không phải gate script, là bước bắt buộc)

1. Nếu có libreoffice: render PDF → `pdftoppm` cover + 1 trang content → ĐỌC screenshot bằng mắt: cover đúng subject color, section header (số cam + title indigo), formula color-coding, T: gloss xanh, không raw tag.
2. Nếu không có: unzip docx → check document.xml (well-formed, không raw `[TAG`), extract text check em-dash/raw markers, ghi rõ trong state là visual QC chỉ ở mức XML.
3. Lesson đã trả giá: 6 vòng QC từng miss duplicate section heading vì không nhìn screenshot.

#### GATE VOICE — sau Phase 3 (BẮT BUỘC, HARD STOP)

Mọi note PHẢI đi qua **note-pipeline-humanizer** để áp giọng Việt "thầy đã đi thi" (đọc `note-pipeline-humanizer/references/VOICE_PROFILE.md`). KHÔNG ĐƯỢC BỎ QUA — kể cả khi user không nhắc "humanize". Đây là khâu định danh chất lượng của toàn pipeline.

Checklist hard-stop (chưa pass thì KHÔNG đi tiếp / KHÔNG deliver):
- [ ] Term lõi: **English đậm** + (gloss Việt) lần đầu — không dịch cứng.
- [ ] 4 tầng nhấn đúng vai (`**bold**` term / `==highlight==` câu chốt / CAPS tương phản / `[BOX_WARN]` "GHI CHÚ BỔ SUNG").
- [ ] `💡 VÍ DỤ THỰC TẾ` (BOX_EXAMPLE) VN ở chủ đề neo được — số thật + câu hỏi phản biện.
- [ ] `[BOX_WARN]` ghé tai cho bẫy thi / nuance / hé Level II khi chủ đề có.
- [ ] Giọng "ta... nhé" trực diện, ZERO cliché AI; mật độ marker trong trần corpus.
- [ ] Sạch lỗi gốc (note trùng, bold gãy chữ, separator loạn).

#### Phase 4.7 — Numeric verification bắt buộc

**Agent-driven (KHÔNG có script riêng)** — spawn 1 agent kiểm số: trích MỌI con số trong context BOX_EXAMPLE/FORMULA của `{module}.markup.md` thành `work_{module}/numeric_checklist.md`, rồi verify TỪNG số vs `ref_APP/IFT/SCH/UWD.md`. Số fabricated = CRITICAL, phải sửa trước Phase 5. Bug thật đã xảy ra 3 lần: FI_M3 (3 số sai), DER_M1 (discount factors bịa), DER_M2 (đảo chiều overpriced/underpriced).

#### GATE 3 — trước khi declare delivered

```bash
python3 <SKILLS_ROOT>/note-pipeline-audit/scripts/audit_render_output.py \
  path/to/{module_id}.docx --markup work_{module}/{module_id}.markup.md --expected-pages 30-55
```

CRITICAL > 0 → STOP delivery.

### 6. Agent spawning — budget-aware rules

1. Tối đa 2 agents song song mỗi batch (4 agents song song đã gây "out of usage" nhiều lần).
2. Agent fail "out of usage" / "rate limited": (a) CHECK file output đã tồn tại chưa, agent thường write xong trước khi limit hit; (b) nếu thiếu, retry đúng 1 lần; (c) vẫn fail → tự self-write, KHÔNG chờ. Self-write đã proven cho voice sạch hơn agent (0 findings ở PM_M6, AI_M2, PM_M3).
3. Agent Write tool bị PostToolUse hook block trên Windows path → instruct agent dùng bash heredoc `cat > path << 'EOF'`.
4. Child agent KHÔNG ghi state file. Chỉ orchestrator aggregate và ghi (race-safe rule).

### 7. Numbering policy

- Module MỚI (chưa có docx nào): render với `--numbering section` (Ví dụ/Công thức đánh số N.M theo section, đúng convention CLAUDE.md).
- Module CŨ re-render: giữ `--numbering module` (mặc định engine) để diff ổn định với bản đã giao. Ghi lựa chọn vào `state["user_decisions"]["numbering"]`.

### 8. Final report

Sau khi mọi gate pass:

- Phases đã chạy + số vòng iterate
- Deliverable paths (CHÍNH SÁCH: chỉ giao .docx, PDF chỉ dùng QC nội bộ)
- Metrics: trang, KB, block counts, terms, formulas, figures
- Trạng thái 3 gates + visual QC + numeric verification (bảng PASS/FAIL)
- Issues deferred kèm lý do kỹ thuật

## Critical rules

1. **NEVER call child skills outside orchestrator without explicit user permission.**
2. **State file là single source of truth.** Chỉ orchestrator ghi.
3. **Child skills KHÔNG gọi nhau trực tiếp.**
4. **Gate fail → orchestrator dừng, fix root cause, không workaround.**
5. **Mọi markup đã sửa sau gate → re-run gate (regression rule).**
6. **Visual QC và numeric verification là BẮT BUỘC trong create_full, không phải optional.**
7. **Không em-dash ở bất cứ output nào, kể cả report.**

## Files

```
note-pipeline/
├── SKILL.md (this)
├── references/
│   ├── INTENT_ROUTING.md        (bảng action + keyword patterns)
│   ├── STATE_SCHEMA.md          (schema state file + race-safe rules)
│   └── CHILD_SKILLS_OVERVIEW.md (contract từng child: input/output/gate)
└── scripts/
    ├── state_init.py
    └── intent_classifier.py
```

viz-factory PowerShell engine (LEGACY, chỉ Windows) là folder độc lập (xem note-pipeline-viz/SKILL.md mục VIZ_ROOT). Renderer chuẩn mặc định (matplotlib) nằm TRONG note-pipeline-viz.

**note-pipeline-viz-library (super-viz-factory, 48 EIR component matplotlib)** — skill CON của note-pipeline-viz: figure institutional/editorial cao cấp (dumbbell, fan, football_field, tornado, sankey, decision_tree, scenario_cards, SWOT, dupont, exec_dashboard...) render qua `<LIB_ROOT>/scripts/viz_super.py`, cùng `spec.json` contract, trộn được core + 48 EIR. Phase 4.6 ưu tiên viz-rich + BẮT BUỘC GATE VIZ (soi từng PNG, không chồng chữ/legend lên hình). Chi tiết: note-pipeline-viz/SKILL.md mục SUPER-VIZ-FACTORY + `<LIB_ROOT>/references/CATALOG.md`.

## Backward compatibility

Old monolithic skill preserved as `note-pipeline-legacy`. Markup của 15+ module cũ phải luôn validate 0 errors và render được với engine mới (numbering mặc định `module`).

## PATCHES L1/L2/L3 (v3) — orchestrator notes

- **Phase 2.1 render**: THÊM `--level {I|II|III}` (theo subject level). Công thức render thẳng thành **OMML edit được** (engine tự gọi Pandoc) — KHÔNG cần chạy `render_formula_images.py` nữa. Cách nhanh nhất: dùng `note-pipeline-render/make_note.sh`. Xem note-pipeline-render/SKILL.md.
- **Công thức**: markup `[FORMULA]` chứa LaTeX mathtext + `where:` legend tiếng Anh. KHÔNG `[ORNAMENT]`.
- **GATE 3 expected-pages theo level**: L1 = 18-30, L2 = 30-55, L3 = 30-60 (không cố định 30-55).
- **L1 nguồn**: có thể survey theo provider (4 agent, mỗi agent gom nhiều LOS PDF của 1 provider) thay vì 1 agent/PDF, vì L1 chia tới cấp LOS (8-20 PDF/module).
- **Font**: Lato/Lora (đã cài). Tránh Inter/Be Vietnam Pro/Raleway nếu chưa chắc cài.

## Sub-skill mới: note-pipeline-humanizer (Phase 3 voice)
Ở Phase 3 (voice/humanize), dùng **note-pipeline-humanizer** để áp 'giọng thầy đã đi thi' của user (song ngữ Anh-Việt, ví dụ VN, bẫy thi). Hồ sơ giọng distill từ 102 module note chuẩn hoá. note-pipeline-qc vẫn lo polish-VI/cross-ref; humanizer chuyên sâu GIỌNG.
