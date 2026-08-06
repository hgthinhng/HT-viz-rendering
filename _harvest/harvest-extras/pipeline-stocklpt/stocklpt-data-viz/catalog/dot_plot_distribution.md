# `dot_plot_distribution` - phân phối dots với quartile band (SVG)

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import dot_plot_distribution`

---

## Khi nào dùng

- n=10+ entity với threshold (12 banks SFL).
- Cần show median + IQR + outlier rõ ràng.
- Sector distribution 30 stocks P/B với industry median.

## Khi nào KHÔNG dùng

- n < 8 - dùng `bar_horizontal`.
- Multiple groups overlay - dùng small_multiples_grid hoặc box plot.
- Cần specific entity highlight đậm - kết hợp `compass_callout`.

## Pair với

- `compass_callout` editorial wrap.
- `marginalia` source.
- `slopegraph` follow up cho before/after toàn bộ phân phối.

## Params

```python
dot_plot_distribution(
    items: list[dict],       # [{"label", "value", "highlight"?, "annotate"?}]
    threshold: float = None,
    threshold_label: str = "",
    title: str = "",
    x_unit: str = "",
    show_quartiles: bool = True,
    show_median: bool = True,
)
```

## Code template

```python
from viz_wave8 import dot_plot_distribution

html = dot_plot_distribution(
    items=[
        {"label": "VPB", "value": 28.3, "highlight": True, "annotate": "Sát trần"},
        {"label": "TCB", "value": 26.9, "highlight": True},
        {"label": "MBB", "value": 22.1},
        # ... 12 banks total
    ],
    threshold=30,
    threshold_label="Trần SFL",
    title="Phân phối SFL Q1/2026, 12 NHTM lớn nhất",
    x_unit="%",
)
```

## Notes

- Quartile band Q1-Q3 màu paper darker.
- Median line dashed slate.
- Threshold line bordeaux solid.
