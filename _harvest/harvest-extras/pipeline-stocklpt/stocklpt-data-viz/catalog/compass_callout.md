# `compass_callout` - wrapper bọc chart + editorial caption sidebar

**Wave:** 8  
**Output:** HTML wrap SVG  
**Render:** `from viz_wave8 import compass_callout`

---

## Khi nào dùng

- Wrap Wave 8 atomic chart bằng editorial caption sidebar.
- Cần punch line takeaway next to chart.
- Convert atomic chart thành editorial signature unit.

## Khi nào KHÔNG dùng

- Wrap Wave 1-3 components - không tương thích.
- Wrap Wave 9/10 - đã có editorial layout sẵn.

## Pair với

- Wrap `line_with_annotations`, `dot_plot_distribution`, `slopegraph`, `sankey_mini`, `quadrant_scatter`.

## Params

```python
compass_callout(
    chart_html: str,        # output từ Wave 8 component
    caption_title: str,     # short title
    caption_body: str,      # 1-2 sentence takeaway
    side: str = "right",    # "left" | "right"
)
```

## Code template

```python
from viz_wave8 import compass_callout, slopegraph

slope_html = slopegraph(items=[...], label_before="...", label_after="...")

html = compass_callout(
    chart_html=slope_html,
    caption_title="Rerank VPB",
    caption_body="VPB từ vị trí #4 leo lên #1 sau Phương án A. Đường đan chéo TCB và MBB là tín hiệu sắp xếp lại trật tự cạnh tranh.",
    side="right",
)
```

## Notes

- Layout 75/25 (chart/caption) hoặc 70/30.
- Caption có accent rule vertical divider.
