# `small_multiples_grid` - cùng metric × 4-12 entity × time (Tufte signature)

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import small_multiples_grid`

---

## Khi nào dùng

- Cùng metric across 4-12 entity over time (CASA của 8 banks 12 quý).
- Sector growth rate qua quarters.
- ESG score 6 companies 5 năm.

## Khi nào KHÔNG dùng

- n < 4 entity - overlay 1 chart đủ.
- Khác metric / khác unit - dùng dashboard_grid hoặc narrative_strip.
- Cần absolute value comparison - small multiples normalize y-axis làm khó so sánh.

## Pair với

- `marginalia` chú thích y-axis normalization.
- `compass_callout` editorial wrap.

## Params

```python
small_multiples_grid(
    panels: list[dict],     # [{"name", "data": [(label, value), ...]}]
    title: str = "",
    columns: int = 4,
    polarity_aware: bool = True,    # tô color theo sign trend
)
```

## Code template

```python
from viz_wave8 import small_multiples_grid

html = small_multiples_grid(
    panels=[
        {"name": "VCB", "data": [("Q1", 35), ("Q2", 36), ("Q3", 38)]},
        {"name": "CTG", "data": [("Q1", 22), ("Q2", 21), ("Q3", 20)]},
        {"name": "VPB", "data": [("Q1", 14), ("Q2", 13), ("Q3", 12)]},
        # ... 8 banks
    ],
    title="CASA tỷ lệ 8 NHTM, 8 quý",
    columns=4,
    polarity_aware=True,
)
```

## Notes

- Y-axis shared scale auto-detect.
- Polarity-aware: trend up xanh, down đỏ.
- Panel size compact, label gọn.
