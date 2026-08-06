# `chart_dropcap` - mở Phần với chart hero + drop cap 32pt

**Wave:** 9  
**Output:** HTML+CSS+SVG  
**Render:** `from viz_wave9 import chart_dropcap`

---

## Khi nào dùng

- Signature opening cho Phần long-form.
- Pull quote + data hero kết hợp với prose wrap around.

## Khi nào KHÔNG dùng

- Mở section ngắn - dùng `gauge` hoặc `data_hero`.
- Mid-section - không phù hợp position.
- Daily report - quá heavy cho format ngắn.

## Pair với

- `gauge` hoặc `infographic_panel` cho hero chart.
- `marginalia` chú thích chart.

## Params

```python
chart_dropcap(
    initial_letter: str,    # 1 ký tự T, M, V, K, S (Latin tránh dấu)
    chart_html: str,        # chart inline với prose
    body_text: str,         # text wrap around 80-150 từ
    title: str = "",
)
```

## Code template

```python
from viz_wave9 import chart_dropcap, gauge

gauge_html = gauge(value=111.9, max_val=120, threshold=85, label="LDR")

html = chart_dropcap(
    initial_letter="T",
    chart_html=gauge_html,
    body_text="rần LDR 85% theo Thông tư 22 đã không còn phản ánh đúng thực tế hệ thống ngân hàng Việt Nam năm 2026. Số liệu Q1/2026 cho thấy 9/10 NHTM lớn nhất đều vượt trần. Câu hỏi không còn là 'có nên sửa hay không' mà là 'sửa thế nào'.",
    title="Phần I - Tại sao có chuyện sửa đổi",
)
```

## Notes

- Drop cap 32pt PFD italic brass.
- Initial letter ưu tiên Latin thường (T, M, V, K, S, B) để tránh dấu thanh đè text.
