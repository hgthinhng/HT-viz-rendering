# `timeline_horizontal` - timeline ngang với milestones

**Wave:** 1-3  
**Output:** HTML+SVG  
**Render:** `from viz import timeline_horizontal`

---

## Khi nào dùng

- Khung thời gian implementation policy / regulatory schedule.
- Lịch trình 4-8 milestone events theo thứ tự thời gian.
- Cuối bài forecast về timing của outcome.

## Khi nào KHÔNG dùng

- Process status có completed/current/future markers - dùng `path_progression` (Wave 9).
- Time series numerical - dùng `line_with_annotations`.
- Decision branches - dùng `policy_fork`.

## Pair với

- `scenario_cards` - scenario discussion + timeline forecast.
- `flow_bridge` - mechanism + timeline implementation.

## Params

```python
timeline_horizontal(
    events: list[dict],   # [{"date": str, "label": str, "tone"?: str}]
    title: str = "",
)

# events theo thứ tự thời gian từ trái sang phải
```

## Code template

```python
from viz import timeline_horizontal

html = timeline_horizontal(
    events=[
        {"date": "Q1/2026", "label": "Dự thảo công bố"},
        {"date": "Q2/2026", "label": "Lấy ý kiến công khai"},
        {"date": "Q3/2026", "label": "Thông qua", "tone": "positive"},
        {"date": "Q4/2026", "label": "Áp dụng SFL trần mới 35%", "tone": "positive"},
        {"date": "Q1/2027", "label": "Đánh giá tác động lần 1"},
    ],
    title="Lộ trình áp dụng Phương án A",
)
```

## Failure modes

- **label > 16 chars**: auto wrap 2 lines. Quá dài vẫn overflow. Cô đọng label.
- **event không sort theo thời gian**: visual confusion. Sort trước khi pass vào.

## Notes

- Date format flexible: "Q1/2026", "T6/2026", "01/04/2026" đều OK.
- Tone: positive (green dot), negative (red), neutral (slate). Default neutral.
