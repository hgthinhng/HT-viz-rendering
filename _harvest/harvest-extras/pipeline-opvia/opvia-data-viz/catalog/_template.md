# `<component_name>` - <one-liner mô tả>

**Wave:** 1-3 / 8 / 9 / 10
**Output:** HTML+CSS / Inline SVG / HTML+SVG composite
**Render:** `from <module> import <function>`

---

## Khi nào dùng

Liệt kê 3-5 use case cụ thể. Mỗi case 1 dòng. Tránh mơ hồ. Ví dụ:
- Có 1 ratio quy chiếu trần (LDR=111,9% trần=85%) - ưu tiên `gauge` hơn bar 1-cell.
- Bài deep dive cần con số signature mở Phần I, max 1 lần per Phần.

---

## Khi nào KHÔNG dùng

Liệt kê 2-4 case mismatch để tránh nhầm lẫn. Ví dụ:
- Daily report header có 4 KPIs - dùng `dashboard_grid` thay vì 4 gauge cạnh nhau.
- Multiple entities cùng metric - dùng `bar_horizontal` hoặc `dot_plot_distribution`.

---

## Pair với (composition pattern)

Component nào hay đi kèm và tại sao. Ví dụ:
- `gauge` + `compass_callout`: wrap gauge bằng editorial caption sidebar.
- `gauge` + `marginalia`: chú thích methodology bên lề.

---

## Params

```python
component_name(
    param1: type,           # mô tả
    param2: type = default, # mô tả + default behavior
    ...
)
```

Ghi rõ:
- Param bắt buộc vs optional
- Range value hợp lệ (vd: `value` từ 0 đến `max_val`)
- Default behavior khi optional

---

## Code template

```python
from <module> import <function>

html = component_name(
    # ... params với value mẫu ...
)

# Inject vào body
body += html
```

---

## Examples

### Example 1: <case 1 specific>

```python
gauge(
    value=111.9,
    max_val=120,
    threshold=85,
    label="LDR hệ thống",
    danger_above=True,
)
```

Output: gauge với fill bordeaux (vì danger_above=True và value > threshold), threshold tick ở 85, value 111.9 hiển thị mã ô lớn.

### Example 2: <case 2 specific>

(2-3 examples is plenty, không nên >5).

---

## Failure modes

- **Failure 1**: mô tả + cách fix
- **Failure 2**: mô tả + cách fix

---

## Notes

- WeasyPrint quirks (nếu có)
- Font dependency (PFD italic, JetBrains Mono?)
- Color polarity convention
- Các edge case khác
