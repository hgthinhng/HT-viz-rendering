# `waterfall` - chuỗi changes A → B từng bước

**Wave:** 1-3  
**Output:** HTML+SVG  
**Render:** `from viz import waterfall`

---

## Khi nào dùng

- P&L bridge: Revenue → COGS → Gross Margin → OpEx → Operating Profit.
- Capital adequacy walk: CAR start → +retained earnings → -RWA growth → CAR end.
- Net change breakdown 4-7 components dẫn từ value start tới value end.

## Khi nào KHÔNG dùng

- Single change A → B - dùng `before_after_comparison`.
- Multiple entities cùng metric - dùng `bar_horizontal`.
- Causal mechanism (không phải numerical breakdown) - dùng `flow_bridge`.

## Pair với

- `gauge` mở Phần với metric kết, waterfall breakdown từng phần.
- `marginalia` chú thích methodology calc.

## Params

```python
waterfall(
    items: list[dict],     # [{"label", "value", "type": "start"|"positive"|"negative"|"end"}]
    title: str = "",
    unit: str = "tỷ",
)
```

## Code template

```python
from viz import waterfall

html = waterfall(
    items=[
        {"label": "CAR đầu kỳ", "value": 12.5, "type": "start"},
        {"label": "Lợi nhuận giữ lại", "value": 1.2, "type": "positive"},
        {"label": "Phát hành thêm cổ phiếu", "value": 0.8, "type": "positive"},
        {"label": "RWA tăng", "value": -1.5, "type": "negative"},
        {"label": "Trả cổ tức", "value": -0.3, "type": "negative"},
        {"label": "CAR cuối kỳ", "value": 12.7, "type": "end"},
    ],
    title="CAR walk Q1-Q4 2025",
    unit="%",
)
```

## Failure modes

- **sum positive + negative không khớp end - start**: visual sai. Verify math trước khi render.
- **> 8 items**: chart quá dài, mất focus. Group nhỏ thành "Other adjustments".

## Notes

- Color: positive xanh, negative đỏ, start/end slate.
- Connector lines giữa các bar tự động.
