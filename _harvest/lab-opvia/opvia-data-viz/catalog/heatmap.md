# `heatmap` - ma trận cell màu pos/neg cho impact analysis

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import heatmap`

---

## Khi nào dùng

- Ai hưởng lợi ai chịu thiệt theo policy: rows = entity, cols = dimension impact.
- Sector × period với P&L change %.
- Bank × regulatory metric với compliance status.
- Cần show cả magnitude (color intensity) + direction (pos/neg).

## Khi nào KHÔNG dùng

- Chỉ 1 dimension - dùng `bar_horizontal`.
- Không có natural ordering (random categorical) - heatmap mất structure.
- < 4 cells - text bullet đơn giản hơn.

## Pair với

- `winners_losers_split` - heatmap cho ma trận, winners_losers_split cho cột đối xứng.
- `marginalia` - chú thích nguồn + methodology.

## Params

```python
heatmap(
    rows: list[str],              # entity labels
    cols: list[str],              # dimension labels
    cells: list[list[float]],     # matrix value
    title: str = "",
    unit: str = "pp",             # đơn vị (đp, %, bps...)
    polarity: str = "diverging",  # "diverging" (pos/neg) hay "sequential"
    annotate: bool = True,        # show value trong cell
)
```

## Code template

```python
from viz import heatmap

html = heatmap(
    rows=["Big4 (VCB+CTG+BID+AGR)", "Big3 (TCB+VPB+MBB)", "Nhóm C"],
    cols=["LDR Q1", "LDR Q2 ước", "Delta"],
    cells=[
        [88.0, 89.5, 1.5],
        [102.1, 108.3, 6.2],
        [95.0, 97.2, 2.2],
    ],
    title="Tác động Phương án A lên LDR theo nhóm bank",
    unit="pp",
    polarity="diverging",
)
```

## Examples

### Example: Sector × Q1-Q4 P&L change

```python
heatmap(
    rows=["Steel", "Retail", "Banking", "Real Estate"],
    cols=["Q1", "Q2", "Q3", "Q4"],
    cells=[
        [12.5, -8.2, -15.3, 4.1],
        [3.2, 5.1, 7.8, 9.2],
        [2.1, 1.8, 0.9, -1.2],
        [-22.1, -18.5, -12.3, -5.4],
    ],
    title="Sector P&L change YoY 2025 (%)",
    polarity="diverging",
)
```

Diverging palette: positive xanh (positive #2E7D52), negative đỏ (negative #C0392B).

## Failure modes

- **polarity sai**: sequential cho data có pos/neg = mất signal direction. Dùng diverging.
- **cell value range quá rộng**: 1 outlier extreme làm những cell khác bị washed out. Cân nhắc clip hoặc log scale.
- **annotate=True với matrix lớn (>30 cells)**: text chen chúc. Tắt annotate, dùng tooltip alt.

## Notes

- Diverging color anchored at 0. Sequential anchored at min.
- Row label tiếng Việt dài: nên ngắn gọn (ngắn hơn 24 chars).
