# `sparkline` - mini chart inline trong prose

**Wave:** 1-3  
**Output:** Inline SVG  
**Render:** `from viz import sparkline`

---

## Khi nào dùng

- Inline trong câu: "VPB CASA chỉ ~12% [sparkline] giảm liên tục 6 quý".
- Cell của bảng có thêm trend mini-chart.
- Stat card kèm 12-period trend mini.

## Khi nào KHÔNG dùng

- Cần annotation/label - dùng `line_with_annotations` (Wave 8).
- Cần value axis cụ thể - sparkline không có axis.

## Pair với

- `stat_dashboard` - mỗi stat kèm sparkline 12 period.
- Embed inline trong prose như punctuation visual.

## Params

```python
sparkline(
    values: list[float],     # 6-24 data point
    width: int = 60,         # px
    height: int = 16,        # px (fit inline với line-height)
    tone: str = "neutral",   # "positive"|"negative"|"neutral"
)
```

## Code template

```python
from viz import sparkline

sp = sparkline(values=[12.1, 11.9, 11.5, 11.2, 11.0, 10.8], tone="negative")
prose = f"VPB CASA tỷ lệ {sp} giảm liên tục 6 quý từ Q3/2024."
```

## Failure modes

- **values < 4**: sparkline trivial, không kể được trend. Min 6 points.
- **values mix order of magnitude**: auto-scale làm flatten một số cluster. Pre-normalize nếu cần.

## Notes

- Default 60x16 px - fit line-height body.
- Không có axis, không có annotation - chỉ trend shape.
