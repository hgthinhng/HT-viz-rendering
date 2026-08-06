# `risk_radar` - radar chart 5-7 axes entity profile multi-dim

**Wave:** 1-3  
**Output:** Inline SVG  
**Render:** `from viz import risk_radar`

---

## Khi nào dùng

- 1 stock profile 5-7 risk axes (liquidity, credit, market, ops, regulatory).
- 2-3 entity overlay so sánh profile.
- ESG score radar 7 dimensions.

## Khi nào KHÔNG dùng

- < 5 axes - dùng `bar_horizontal` đơn giản hơn.
- > 7 axes - radar quá rối.
- Magnitude quan trọng (không phải shape) - dùng `bar_horizontal`.

## Pair với

- `marginalia` chú thích từng axis definition.

## Params

```python
risk_radar(
    entities: list[dict],   # [{"name", "scores": list[float], "color"?}]
    axes: list[str],        # axis labels
    scale_max: float = 5,
    title: str = "",
)
```

## Code template

```python
from viz import risk_radar

html = risk_radar(
    entities=[
        {"name": "VPB", "scores": [3.5, 4.2, 2.8, 3.0, 4.5]},
        {"name": "VCB", "scores": [2.0, 1.5, 2.5, 1.8, 2.0]},
    ],
    axes=["Liquidity risk", "Credit risk", "Market risk", "Ops risk", "Regulatory risk"],
    scale_max=5,
    title="Risk profile so sánh: VPB vs VCB",
)
```

## Notes

- Multiple entities overlay với fill alpha 0.3.
- Axis labels rotate theo angle.
