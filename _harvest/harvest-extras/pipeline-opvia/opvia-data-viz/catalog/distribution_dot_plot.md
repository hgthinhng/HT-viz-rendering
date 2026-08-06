# `distribution_dot_plot` - dots trên axis (HTML version Wave 1-3)

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import distribution_dot_plot`

---

## Khi nào dùng

- Sector outliers identification: 30 stocks P/B distribution.
- Bank ROE distribution với industry median line.
- Compact display khi cần inline trong prose flow.

## Khi nào KHÔNG dùng

- Cần quartile band + median + threshold visual đậm - dùng `dot_plot_distribution` (Wave 8 SVG).
- n < 8 - dùng `bar_horizontal`.
- Cần highlight specific entity - dùng Wave 8 version với better annotation.

## Pair với

- `marginalia` chú thích median value, source.

## Params

```python
distribution_dot_plot(
    items: list[dict],     # [{"label"?, "value", "highlight"?: bool}]
    title: str = "",
    unit: str = "",
    threshold: float = None,
    threshold_label: str = "",
)
```

## Code template

```python
from viz import distribution_dot_plot

html = distribution_dot_plot(
    items=[
        {"label": "VCB", "value": 2.1, "highlight": True},
        {"value": 1.8}, {"value": 1.5}, {"value": 1.3},
        # ... 30 banks total
    ],
    title="P/B distribution 30 NHTM Q1/2026",
    unit="x",
    threshold=1.0,
    threshold_label="Median",
)
```

## Notes

- Wave 1-3 version: HTML simpler, không có quartile band.
- Cho deep analysis, ưu tiên Wave 8 `dot_plot_distribution` SVG.
