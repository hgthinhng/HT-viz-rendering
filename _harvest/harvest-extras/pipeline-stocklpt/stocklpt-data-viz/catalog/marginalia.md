# `marginalia` - chú thích lề accent italic 75/22

**Wave:** 9  
**Output:** HTML+CSS  
**Render:** `from viz_wave9 import marginalia`

---

## Khi nào dùng

- Methodology notes bên lề (cách tính ratio, source data).
- Definition tooltips inline với prose chính.
- Source disclosure / disclaimer footer kiểu editorial.

## Khi nào KHÔNG dùng

- Note quan trọng trung tâm câu chuyện - dùng prose chính, không bên lề.
- Long explanation > 100 chars - gây mất focus, dùng footnote inline.

## Pair với

- Wrap kèm bất kỳ chart Wave 1-10 cần methodology note.

## Params

```python
marginalia(
    main_html: str,        # nội dung chính
    margin_text: str,      # text chú thích lề
    side: str = "right",   # "left" | "right"
)
```

## Code template

```python
from viz_wave9 import marginalia

main_html = "<p>...prose chính...</p>" + chart_html

html = marginalia(
    main_html=main_html,
    margin_text="LDR = (Tín dụng) / (Tiền gửi). Theo Thông tư 22, không tính cho vay liên ngân hàng.",
    side="right",
)
```

## Notes

- Layout 75% main / 22% margin / 3% gap.
- Margin text PFD italic accent color.
