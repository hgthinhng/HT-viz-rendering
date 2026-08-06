# `stat_dashboard` - 4-6 stats grid header overview

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import stat_dashboard`

---

## Khi nào dùng

- Mở Phần overview với 4-6 KPI Bird-eye.
- Daily report header (VN-Index, GTGD, NĐT khối ngoại, ...).
- Earnings review summary (Revenue, EPS, Margin, ROE, EPS surprise).

## Khi nào KHÔNG dùng

- Cần sparkline visual cho mỗi stat - dùng `dashboard_grid` (Wave 10).
- Single signature stat - dùng `data_hero` hoặc `gauge`.
- > 6 stat - quá đông, pick top 6 hoặc dùng `narrative_strip`.

## Pair với

- `gauge` cho stat hot nhất follow up sau dashboard.
- `marginalia` source/methodology note.

## Params

```python
stat_dashboard(
    stats: list[dict],    # [{"label", "value", "unit"?, "delta"?, "tone"?}]
    title: str = "",
    columns: int = 3,     # 2, 3, 4 columns
)
```

## Code template

```python
from viz import stat_dashboard

html = stat_dashboard(
    stats=[
        {"label": "VN-Index", "value": "1.347,5", "delta": "+1,2%", "tone": "positive"},
        {"label": "GTGD HOSE", "value": "22,3K tỷ", "delta": "-3,5%", "tone": "negative"},
        {"label": "NĐT NN mua ròng", "value": "+285 tỷ", "tone": "positive"},
        {"label": "Số mã tăng/giảm", "value": "256/142"},
        {"label": "Phá đỉnh 1Y", "value": "12 mã"},
        {"label": "Volume / 20D MA", "value": "1,15x"},
    ],
    title="Phiên 02/05/2026",
    columns=3,
)
```

## Failure modes

- **value text quá dài**: card width fixed. Format gọn (vd "22,3K tỷ" thay vì "22.345.678.000.000 VND").
- **delta sign confusion**: tone="positive" với delta âm = mâu thuẫn visual. Match tone với delta.

## Notes

- Default 3 columns. 2 cho ít stats, 4 cho nhiều stats.
- Tone tô viền card (positive/negative/neutral).
