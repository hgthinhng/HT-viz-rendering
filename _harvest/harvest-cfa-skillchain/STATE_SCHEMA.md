# `_pipeline_state.json` Schema

State file lưu progress của 1 module qua orchestrator. Single source of truth.

## Location

`work_{module_id}/{module_id}_state.json`

Example: `work_EQ_M1/EQ_M1_state.json`

## Full schema

```json
{
  "module_id": "EQ_M1",
  "subject": "Equity",
  "module_num": 1,
  "module_name": "Equity Valuation: Applications and Processes",
  "started": "2026-05-05T10:00:00",
  "last_updated": "2026-05-05T12:30:00",
  "phases": {
    "create": {
      "status": "complete|in_progress|pending|failed",
      "started": "2026-05-05T10:00:00",
      "completed": "2026-05-05T11:00:00",
      "outputs": [
        "ref_APP.md",
        "ref_IFT.md",
        "ref_SCH.md",
        "ref_UWD.md",
        "01_outline_EQ_M1.md",
        "02_subsection_plan_EQ_M1.md",
        "teaching_scripts/section_1.md",
        "...",
        "EQ_M1.markup.md"
      ],
      "metrics": {
        "validator_errors": 0,
        "validator_warnings": 22,
        "term_count": 41,
        "section_count": 8,
        "block_count": 285
      }
    },
    "render": {
      "status": "complete",
      "outputs": ["EQ_M1.docx", "qc_screenshots/"],
      "metrics": {"page_count": 41, "file_size_kb": 111}
    },
    "qc": {
      "status": "pending",
      "outputs": [],
      "metrics": {}
    },
    "audit": {
      "status": "pending",
      "outputs": [],
      "metrics": {"critical": 0, "important": 0, "minor": 0}
    },
    "deliver": {
      "status": "pending",
      "outputs": [],
      "metrics": {}
    }
  },
  "user_decisions": {
    "font_stack": "B",
    "build_mode": "digital",
    "subject_color": "forest_green",
    "hero_image": "procedural",
    "phase4_qc_mode": "marked"
  },
  "global_metrics": {
    "total_chars": 18656,
    "total_pages": 41,
    "total_runtime_seconds": 9000
  }
}
```

## Phase status lifecycle

```
pending → in_progress → complete
                     ↓
                   failed (if error, orchestrator stops)
```

## Reading state

Each child skill on start:
1. Read state from `work_{module_id}/{module_id}_state.json`
2. Check inputs available (paths in previous phase outputs)
3. If running standalone (no orchestrator), can pass `--state-file` arg explicitly

## Writing state — ORCHESTRATOR ONLY (race-safe rule)

**Quy tắc:** Chỉ orchestrator (Claude main) ghi state. Child skill và spawned agent KHÔNG ghi.

**Lý do:** Phase 1.0 và Phase 1.3 spawn 4-8 agent song song. Nếu mỗi agent tự ghi state, có race condition (concurrent write → mất hash, mất output entry).

**Pattern đúng:**

1. Orchestrator spawn child với context (module_id, phase, decisions từ state).
2. Child/agent return value (qua text output): `{"status": "...", "outputs": [...], "metrics": {...}}`.
3. Sau khi tất cả agent join, orchestrator parse return values, aggregate, ghi state 1 lần.

**Pattern sai (race-prone):** child ghi state song song không qua orchestrator → mất update. Nguyên tắc: aggregate rồi ghi 1 lần (mục trên).

## v2 additions (2026-06-10 upgrade)

Các field mới orchestrator ghi thêm vào schema trên:

```json
{
  "environment": {
    "can_powershell": false,
    "can_matplotlib": true,
    "can_libreoffice": true,
    "is_cowork_mount": true,
    "detected_at": "2026-06-10T12:00:00"
  },
  "phases": {
    "polish_vi":            {"status": "...", "swaps_applied": 0},
    "visual_qc":            {"status": "...", "mode": "screenshot|xml_only", "screenshots": []},
    "viz":                  {"status": "...", "engine": "viz_factory|python_fallback|manifest_wait", "figures": []},
    "numeric_verification": {"status": "...", "checklist": "numeric_checklist.md", "total": 0, "verified": 0, "mismatches": 0},
    "humanize":             {"status": "...", "findings": 0, "fixed": 0}
  },
  "gates": {
    "gate1": {"status": "pass|fail|stale", "last_run": "...", "errors": 0},
    "gate2": {"status": "pass|fail|stale", "last_run": "...", "critical": 0},
    "gate3": {"status": "pass|fail|stale", "last_run": "...", "critical": 0}
  },
  "user_decisions": {
    "numbering": "section|module",
    "subject_color": "#6B1B2C"
  }
}
```

**Gate staleness rule**: markup file mtime > gate.last_run → gate status tự chuyển `stale`, orchestrator phải re-run gate đó trước khi đi tiếp.

## Writing state — ORCHESTRATOR ONLY (race-safe rule)

Child agent KHÔNG ghi state file. Child trả value qua final message, orchestrator aggregate rồi ghi MỘT lần. Spawn song song mà mỗi child tự ghi state = race condition, bản ghi sau đè bản trước.
