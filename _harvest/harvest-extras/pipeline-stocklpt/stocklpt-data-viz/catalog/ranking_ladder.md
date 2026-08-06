# `ranking_ladder` - xếp hạng entity với delta arrows vs prev period

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import ranking_ladder`

---

## Khi nào dùng

- Sector ranking Q-on-Q: thép xếp #2 (-1 vs Q3), bán lẻ #1 (+0).
- Bank size ranking với mua bán cổ phần MoM.
- Top 10 stock weight portfolio + delta vs allocation tháng trước.

## Khi nào KHÔNG dùng

- Numerical ranking không cần delta - dùng `bar_horizontal` sort_desc=True.
- Multi-period change visible - dùng `slopegraph` thay.
- < 3 entities - dùng `comparison_cards`.

## Pair với

- `heatmap` cho sector × period matrix.
- `marginalia` chú thích nguồn data.

## Params

```python
ranking_ladder(
    items: list[dict],    # [{"label", "value", "rank", "prev_rank", "delta_unit"?: str}]
    title: str = "",
    unit: str = "",
)
```

## Code template

```python
from viz import ranking_ladder

html = ranking_ladder(
    items=[
        {"label": "Bán lẻ", "value": 12.5, "rank": 1, "prev_rank": 1},
        {"label": "Thép", "value": 11.2, "rank": 2, "prev_rank": 3},
        {"label": "Bất động sản", "value": 10.8, "rank": 3, "prev_rank": 2},
        {"label": "Năng lượng", "value": 9.4, "rank": 4, "prev_rank": 5},
    ],
    title="Sector growth Q4 vs Q3 2025",
    unit="%",
)
```

## Failure modes

- **rank và prev_rank không sequential**: arrow direction sai. Verify rank integer 1..N.

## Notes

- Arrow up xanh, down đỏ, neutral slate.
- Delta = prev_rank - rank (positive = leo lên).
