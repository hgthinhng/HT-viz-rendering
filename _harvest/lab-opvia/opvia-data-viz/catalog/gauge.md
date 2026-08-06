# `gauge` - đồng hồ áp lực 1 ratio + threshold

**Wave:** 1-3  
**Output:** HTML+SVG (inline)  
**Render:** `from viz import gauge`

---

## Khi nào dùng

- 1 ratio quy chiếu trần (LDR=111,9% trần=85%, NSFR=72% trần=80%, SFL=28,3% trần=30%).
- Mở Phần với signature stat - max 1 gauge/Phần để giữ trọng số.
- Daily report header có 1-2 KPI nóng nhất phiên.

## Khi nào KHÔNG dùng

- Có 4-6 KPI cùng lúc - dùng `stat_dashboard` (Wave 1) hoặc `dashboard_grid` (Wave 10).
- Multi entity cùng metric - dùng `bar_horizontal` (n<=6) hoặc `dot_plot_distribution` (n>=8).
- Không có threshold quy chiếu - gauge mất context, dùng `data_hero` thay.

## Pair với

- `compass_callout` - wrap gauge bằng editorial caption sidebar brass rule.
- `marginalia` - chú thích methodology bên lề về cách tính ratio.
- `flow_bridge` - explain why ratio đạt mức đó (mechanism behind the number).

## Params

```python
gauge(
    value: float,                  # giá trị hiện tại (vd 111.9)
    max_val: float,                # max scale (vd 120)
    threshold: float,              # ngưỡng quy chiếu (vd 85)
    label: str,                    # nhãn metric (vd "LDR hệ thống")
    unit: str = "%",               # đơn vị
    danger_above: bool = False,    # True = fill bordeaux khi value > threshold
    subtitle: str = "",            # dòng phụ italic (optional)
)
```

## Code template

```python
from viz import gauge

html = gauge(
    value=111.9,
    max_val=120,
    threshold=85,
    label="LDR hệ thống",
    unit="%",
    danger_above=True,
    subtitle="Q1/2026, dữ liệu SBV",
)
body += html
```

## Examples

### Example 1: LDR vượt trần

```python
gauge(
    value=111.9,
    max_val=120,
    threshold=85,
    label="LDR hệ thống",
    danger_above=True,
)
```

Output: gauge với fill bordeaux (vì danger_above=True và 111.9 > 85), threshold tick ở 85, value 111.9 hiển thị monospace lớn.

### Example 2: SFL VPB cận kề trần

```python
gauge(
    value=28.3,
    max_val=35,
    threshold=30,
    label="SFL VPB",
    subtitle="cận kề trần 30%",
    danger_above=False,
)
```

Output: fill prussian (chưa breach), nhưng visual proximity tới threshold đã đủ tension.

## Failure modes

- **value > max_val**: arc overflow ra ngoài. Set `max_val` đủ rộng (vd max_val = value * 1.1).
- **threshold > max_val**: tick mất visibility. Threshold phải nằm trong [0, max_val].
- **unit dùng "%" cho ratio rate <1**: gauge hiển thị "0,03%" khó đọc. Nên multiply 100 trước hoặc đổi unit thành "bps".

## Notes

- WeasyPrint quirk: arc dùng SVG path inline, không CSS.
- Subtitle italic dùng PFD italic - signature place.
- Color hardcoded: prussian normal, bordeaux danger, brass tick threshold.
