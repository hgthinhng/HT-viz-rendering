# `winners_losers_split` - cột hưởng lợi vs chịu thiệt

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import winners_losers_split`

---

## Khi nào dùng

- Phần "Cuộc chơi phân phối": ai được, ai mất từ policy change.
- M&A deal: acquirer vs target shareholders.
- Sector winners/losers từ macro shock.

## Khi nào KHÔNG dùng

- Multi-dimension impact (entity × dimension) - dùng `heatmap`.
- Magnitude quan trọng - dùng `bar_horizontal` polarity.
- < 4 entities total - text bullet đủ.

## Pair với

- `heatmap` cho matrix detail follow up split overview.
- `marginalia` chú thích methodology classify winners/losers.

## Params

```python
winners_losers_split(
    winners: list[dict],   # [{"label", "magnitude"?, "note"?}]
    losers: list[dict],
    title: str = "",
)
```

## Code template

```python
from viz import winners_losers_split

html = winners_losers_split(
    winners=[
        {"label": "VPB", "magnitude": "+15% NIM", "note": "Thoát SFL pressure"},
        {"label": "TCB", "magnitude": "+8% NIM"},
        {"label": "MBB", "magnitude": "+5% NIM"},
    ],
    losers=[
        {"label": "VCB", "magnitude": "-3% NIM", "note": "Mất lợi thế cạnh tranh"},
        {"label": "BID", "magnitude": "-2% NIM"},
    ],
    title="Phương án A: Ai hưởng lợi ai chịu thiệt",
)
```

## Notes

- Layout 50/50 với divider giữa.
- Winners cột xanh, Losers cột đỏ.
