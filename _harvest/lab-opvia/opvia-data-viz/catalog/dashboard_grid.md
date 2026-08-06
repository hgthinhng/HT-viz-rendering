# `dashboard_grid` - 2x2 grid 4 cells KPI + sparkline + delta

**Wave:** 10  
**Output:** HTML+CSS+SVG  
**Render:** `from viz_wave10 import dashboard_grid`

---

## Khi nào dùng

- Daily report header với 4 KPI nóng.
- Quarterly KPI overview deep analysis.
- Earnings dashboard 4 segment summary.

## Khi nào KHÔNG dùng

- Single hero - dùng `data_hero` hoặc `infographic_panel`.
- Macro strip với caption - dùng `narrative_strip`.
- > 4 KPI - quá đông, pick top 4 hoặc dùng `stat_dashboard` 6 col.

## Pair với

- `marginalia` source data note.

## Params

```python
dashboard_grid(
    cells: list[dict],   # [{"label", "value", "delta"?, "tone"?, "sparkline_data"?: list[float]}]
    title: str = "",
)
# Phải đúng 4 cells
```

## Code template

```python
from viz_wave10 import dashboard_grid

html = dashboard_grid(
    cells=[
        {
            "label": "VN-Index",
            "value": "1.347,5",
            "delta": "+1,2%",
            "tone": "positive",
            "sparkline_data": [1330, 1335, 1338, 1342, 1340, 1347],
        },
        {
            "label": "GTGD HOSE",
            "value": "22,3K tỷ",
            "delta": "-3,5%",
            "tone": "negative",
            "sparkline_data": [25, 23, 22, 24, 22, 22.3],
        },
        {
            "label": "Khối ngoại mua ròng",
            "value": "+285 tỷ",
            "tone": "positive",
        },
        {
            "label": "Số mã tăng/giảm",
            "value": "256/142",
        },
    ],
    title="Phiên 02/05/2026 - tổng quan",
)
```

## Notes

- 2x2 grid responsive.
- Sparkline optional (12-24 datapoint).
- Tone tô viền cell.
