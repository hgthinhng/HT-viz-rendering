# `narrative_strip` - 3-4 mini charts hàng ngang + Economist-style caption

**Wave:** 10  
**Output:** HTML+CSS+SVG  
**Render:** `from viz_wave10 import narrative_strip`

---

## Khi nào dùng

- Economist-style multi-metric strip 3-4 chart cùng theme.
- Macro snapshot: GDP, CPI, FX, lãi suất compact.
- Sector overview: 4 sector mini charts với 1 takeaway sentence.

## Khi nào KHÔNG dùng

- 4 KPI đơn giản không cần caption - dùng `dashboard_grid`.
- > 4 chart - dùng full-width separate.

## Pair với

- `marginalia` source.

## Params

```python
narrative_strip(
    panels: list[dict],   # [{"label", "chart_html"}]
    caption: str,         # 1-2 sentence editorial takeaway
    title: str = "",
)
```

## Code template

```python
from viz_wave10 import narrative_strip
from viz_wave8 import line_with_annotations

panels = [
    {
        "label": "GDP YoY",
        "chart_html": line_with_annotations(series=[{"name": "GDP", "data": [...]}]),
    },
    {
        "label": "CPI YoY",
        "chart_html": line_with_annotations(series=[{"name": "CPI", "data": [...]}]),
    },
    {
        "label": "USD/VND",
        "chart_html": line_with_annotations(series=[{"name": "USDVND", "data": [...]}]),
    },
    {
        "label": "Lãi suất OMO",
        "chart_html": line_with_annotations(series=[{"name": "OMO", "data": [...]}]),
    },
]

html = narrative_strip(
    panels=panels,
    caption="Macro VN Q1/2026: GDP và CPI cùng tăng nhẹ, áp lực FX kéo SBV nâng OMO 25bps.",
    title="Macro snapshot",
)
```

## Notes

- 4 panel hàng ngang, mỗi panel ~25% width.
- Caption block dưới với accent rule trên.
