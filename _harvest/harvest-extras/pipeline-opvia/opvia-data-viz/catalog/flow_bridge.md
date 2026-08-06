# `flow_bridge` - chuỗi nhân quả vertical A → B → C

**Wave:** 1-3  
**Output:** HTML+CSS+SVG  
**Render:** `from viz import flow_bridge`

---

## Khi nào dùng

- Mechanism explanation: tại sao A dẫn đến Z qua 3-5 bước trung gian.
- Counterintuitive result: "sửa LDR mà lại đẩy lợi suất TPCP tăng" - flow_bridge breakdown logic.
- Causal chain với arrows + node text ngắn.

## Khi nào KHÔNG dùng

- Process timeline có thời gian - dùng `timeline_horizontal` hoặc `path_progression`.
- Capital flow nguồn → đích nhiều-nhiều - dùng `sankey_mini`.
- Decision tree với branches - dùng `policy_fork`.

## Pair với

- `gauge` mở Phần với conclusion number, flow_bridge giải thích why.
- `marginalia` chú thích từng node nếu cần.

## Params

```python
flow_bridge(
    nodes: list[dict],   # [{"label": str, "value"?: str, "tone"?: "positive"|"negative"|"neutral"}]
    title: str = "",
)
```

## Code template

```python
from viz import flow_bridge

html = flow_bridge(
    nodes=[
        {"label": "Sửa Thông tư 22 nới SFL", "tone": "neutral"},
        {"label": "NHTM phát hành thêm trái phiếu dài hạn", "tone": "neutral"},
        {"label": "Cung TPCP giảm tương đối", "value": "-15K tỷ/năm", "tone": "negative"},
        {"label": "Lợi suất TPCP 10y tăng", "value": "+30 bps", "tone": "negative"},
    ],
    title="Mechanism: Phương án A → lợi suất TPCP",
)
```

## Examples

### Example: 4-step causal chain

```python
flow_bridge(
    nodes=[
        {"label": "Lãi suất Fed cut 50bps"},
        {"label": "DXY giảm 2%"},
        {"label": "VND tăng giá so với USD", "tone": "positive"},
        {"label": "Pressure imported inflation giảm", "tone": "positive"},
    ],
    title="Cơ chế truyền dẫn Fed cut → CPI VN",
)
```

"tone" set màu border: positive xanh, negative đỏ, neutral slate.

## Failure modes

- **node label > 42 chars**: overflow viewBox. smart_wrap auto-split nhưng break có thể xấu. Edit label ngắn lại.
- **quá 6 nodes**: flow chart dài lê thê, reader mất focus. Split thành 2 flow_bridge hoặc dùng `mechanism_breakdown` 3-stage.

## Notes

- Auto smart_wrap label > 42 chars (split ở conjunction VN gần middle).
- Arrow màu brass.
