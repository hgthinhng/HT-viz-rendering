# `bar_horizontal` - bar chart ngang 3-6 entity + threshold

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import bar_horizontal`

---

## Khi nào dùng

- So sánh 3-6 entity cùng 1 metric (vd LDR của 5 ngân hàng).
- Cần threshold reference line (trần/sàn quy chiếu).
- Label entity dài tiếng Việt (NHTM Cổ phần Á Châu, ...) - bar ngang đọc tốt hơn bar dọc.
- Highlight 1 entity là focal point của câu chuyện.

## Khi nào KHÔNG dùng

- n entity >= 8 - dùng `dot_plot_distribution` để show phân phối.
- n entity = 2 - dùng `before_after_comparison` hoặc `comparison_cards`.
- Có 2 metric cần co-plot - dùng `quadrant_scatter`.
- Time series - dùng `line_with_annotations`.

## Pair với

- `gauge` - mở section bằng gauge (1 con số), follow-up bar_horizontal (cross-entity).
- `marginalia` - chú thích nguồn data, definition.

## Params

```python
bar_horizontal(
    items: list[dict],         # [{"label", "value", "highlight"?, "annotate"?}]
    threshold: float = None,   # threshold line (optional)
    threshold_label: str = "", # nhãn threshold
    title: str = "",           # tiêu đề chart
    unit: str = "%",           # đơn vị value
    sort_desc: bool = True,    # sort giảm dần
)
```

## Code template

```python
from viz import bar_horizontal

html = bar_horizontal(
    items=[
        {"label": "VCB", "value": 88.0},
        {"label": "VPB", "value": 92.5, "highlight": True, "annotate": "Cận trần"},
        {"label": "TCB", "value": 86.0},
    ],
    threshold=85,
    threshold_label="Trần LDR",
    title="LDR Q1/2026 - top 5 NHTM",
    unit="%",
)
```

## Examples

### Example: SFL 5 banks với threshold 30%

```python
bar_horizontal(
    items=[
        {"label": "VPB", "value": 28.3, "highlight": True, "annotate": "Sát trần"},
        {"label": "TCB", "value": 26.9},
        {"label": "MBB", "value": 22.1},
        {"label": "ACB", "value": 19.5},
        {"label": "VCB", "value": 14.2},
    ],
    threshold=30,
    threshold_label="Trần SFL",
    title="Tỷ lệ vốn ngắn hạn cho vay trung dài hạn",
    unit="%",
)
```

VPB highlight + annotate "Sát trần" tạo focal point câu chuyện.

## Failure modes

- **value spread quá lớn (1, 2, 95)**: bar value nhỏ vô hình. Cân nhắc log scale hoặc split thành 2 chart.
- **highlight quá 2 entity**: mất focal effect. Pick 1, max 2 entity highlight.

## Notes

- highlight=True đổi color từ slate → accent.
- Annotate text hiện next to bar, italic PFD.
