# `quadrant_scatter` - 2D scatter X-Y với 4-quadrant labels

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import quadrant_scatter`

---

## Khi nào dùng

- Risk-return scatter (vol vs return).
- P/B vs ROE peer mapping.
- Strategic positioning (market share vs growth rate).

## Khi nào KHÔNG dùng

- Single dimension - dùng `bar_horizontal` hoặc `dot_plot_distribution`.
- Time series - dùng `line_with_annotations`.
- > 30 entity - cluttered, cân nhắc heatmap binned.

## Pair với

- `marginalia` chú thích quadrant interpretation.

## Params

```python
quadrant_scatter(
    points: list[dict],     # [{"label", "x", "y", "highlight"?}]
    x_label: str,
    y_label: str,
    x_axis_at: float = None,    # vị trí trục dọc cắt (default = mean x)
    y_axis_at: float = None,
    quadrant_labels: list[str] = None,   # 4 labels theo TR-TL-BL-BR order
    title: str = "",
)
```

## Code template

```python
from viz_wave8 import quadrant_scatter

html = quadrant_scatter(
    points=[
        {"label": "VCB", "x": 1.8, "y": 22.0, "highlight": True},
        {"label": "TCB", "x": 1.2, "y": 18.5},
        {"label": "VPB", "x": 1.0, "y": 24.0},
        {"label": "BID", "x": 1.4, "y": 12.0},
    ],
    x_label="P/B",
    y_label="ROE %",
    x_axis_at=1.3,
    y_axis_at=18,
    quadrant_labels=["Premium quality", "Cheap value", "Value trap", "Hidden gem"],
    title="Banking peers: P/B vs ROE Q1/2026",
)
```

## Notes

- Quadrant labels italic mờ 4 góc.
- Highlight=True đổi color brass + larger dot.
