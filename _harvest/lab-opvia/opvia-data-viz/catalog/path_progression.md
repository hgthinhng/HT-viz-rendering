# `path_progression` - process tracking 3-7 milestones với marker types

**Wave:** 9  
**Output:** Inline SVG  
**Render:** `from viz_wave9 import path_progression`

---

## Khi nào dùng

- Implementation status (completed/current/future markers).
- Multi-stage approval process tracking.
- Strategic roadmap với phase status.

## Khi nào KHÔNG dùng

- Pure timeline không có status - dùng `timeline_horizontal`.
- Causal flow - dùng `flow_bridge`.

## Pair với

- `scenario_cards` cho forecast outcome của process.

## Params

```python
path_progression(
    milestones: list[dict],    # [{"date", "label", "status": "completed"|"current"|"future"}]
    title: str = "",
)
```

## Code template

```python
from viz_wave9 import path_progression

html = path_progression(
    milestones=[
        {"date": "Q4/2025", "label": "Dự thảo", "status": "completed"},
        {"date": "Q1/2026", "label": "Lấy ý kiến công khai", "status": "completed"},
        {"date": "Q2/2026", "label": "Trình Quốc hội", "status": "current"},
        {"date": "Q3/2026", "label": "Thông qua", "status": "future"},
        {"date": "Q4/2026", "label": "Áp dụng", "status": "future"},
    ],
    title="Lộ trình Phương án A",
)
```

## Notes

- Marker: completed = filled circle xanh, current = ring brass, future = dotted slate.
- Path connector màu brass dotted cho future, solid cho past.
