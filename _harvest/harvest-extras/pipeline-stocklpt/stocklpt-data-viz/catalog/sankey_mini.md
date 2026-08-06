# `sankey_mini` - capital flow Bezier 3-5 → 3-5

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import sankey_mini`

---

## Khi nào dùng

- Dòng vốn nguồn → đích (deposits sources → loan uses).
- M&A flow: target shareholders → cash + acquirer shares.
- Capital allocation: profit sources → dividend + retained + buyback.

## Khi nào KHÔNG dùng

- Single source single dest - dùng `flow_bridge`.
- > 7 source/dest mỗi side - sankey rối, cân nhắc treemap.
- Causal mechanism (không phải numerical flow) - dùng `flow_bridge`.

## Pair với

- `compass_callout` wrap với caption.
- `marginalia` source disclosure.

## Params

```python
sankey_mini(
    sources: list[dict],   # [{"label", "value"}]
    targets: list[dict],
    flows: list[dict],     # [{"source_idx", "target_idx", "value"}]
    title: str = "",
    unit: str = "",
)
```

## Code template

```python
from viz_wave8 import sankey_mini

html = sankey_mini(
    sources=[
        {"label": "Tiền gửi <12T", "value": 100},
        {"label": "Tiền gửi >12T", "value": 30},
        {"label": "Phát hành GTCG", "value": 20},
    ],
    targets=[
        {"label": "Tín dụng <12T", "value": 80},
        {"label": "Tín dụng >12T", "value": 50},
        {"label": "TPCP", "value": 20},
    ],
    flows=[
        {"source_idx": 0, "target_idx": 0, "value": 80},
        {"source_idx": 0, "target_idx": 1, "value": 20},
        {"source_idx": 1, "target_idx": 1, "value": 30},
        {"source_idx": 2, "target_idx": 1, "value": 0},
        {"source_idx": 2, "target_idx": 2, "value": 20},
    ],
    title="Dòng vốn 1 NHTM điển hình (% tổng tài sản)",
)
```

## Notes

- Bezier curves smooth giữa source/target.
- Width path proportional value.
