# `line_with_annotations` - time series 8-20 điểm có pivot points

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import line_with_annotations`

---

## Khi nào dùng

- Macro time series với 2-4 highlight events (lãi suất Fed cut, COVID, war).
- Stock price 12 tháng với analyst rating changes.
- GDP growth quarterly với regime shifts.

## Khi nào KHÔNG dùng

- Inline trong câu - dùng `sparkline`.
- Multi entity overlay - dùng `small_multiples_grid`.
- 2 metric trên cùng axis - dual axis dùng custom.

## Pair với

- `marginalia` chú thích methodology + source data.
- `compass_callout` wrap line chart bằng editorial caption.

## Params

```python
line_with_annotations(
    series: list[dict],     # [{"name", "data": [(label, value), ...], "color"?}]
    annotations: list[dict] = [],   # [{"index": int, "label": str, "tone"?: str}]
    title: str = "",
    y_unit: str = "",
    smooth: bool = True,    # path_smooth Bezier
)
```

## Code template

```python
from viz_wave8 import line_with_annotations

html = line_with_annotations(
    series=[{
        "name": "Lợi suất TPCP 10y",
        "data": [
            ("Q1/24", 4.2), ("Q2/24", 4.5), ("Q3/24", 4.1),
            ("Q4/24", 3.8), ("Q1/25", 3.6), ("Q2/25", 3.9),
            ("Q3/25", 4.3), ("Q4/25", 4.7), ("Q1/26", 5.1),
        ],
    }],
    annotations=[
        {"index": 3, "label": "SBV cut OMO 50bps", "tone": "neutral"},
        {"index": 7, "label": "Lạm phát quay lại 4%", "tone": "negative"},
    ],
    title="Lợi suất TPCP 10y, 9 quý gần nhất",
    y_unit="%",
)
```

## Notes

- Annotations: chấm pivot + leader line tới label box.
- Smooth=True dùng path_smooth Bezier (smoother trend).
- Color polarity-aware (accent cho up trend, slate cho down).
