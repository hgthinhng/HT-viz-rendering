# `executive_summary_box` - 4-section dashboard cuối bài thay summary text

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import executive_summary_box`

---

## Khi nào dùng

- Cuối bài deep analysis thay summary text.
- 4 quadrant: Thesis / Catalyst / Risk / Action.
- 4 quadrant: What happened / Why it matters / What next / Action.

## Khi nào KHÔNG dùng

- < 4 takeaway - dùng prose summary thường.
- Numerical scenario - dùng `scenario_cards`.
- Cần visual hierarchy mạnh - dùng `infographic_panel` (Wave 10).

## Pair với

- `scenario_cards` ngay trước (forecast) + summary_box (action items).
- `marginalia` source disclaimer.

## Params

```python
executive_summary_box(
    quadrants: list[dict],   # [{"name", "headline", "details": list[str], "icon"?}]
    title: str = "",
)
# Phải đúng 4 quadrants
```

## Code template

```python
from viz import executive_summary_box

html = executive_summary_box(
    quadrants=[
        {
            "name": "Luận điểm",
            "headline": "Phương án A có 65% xác suất thông qua trong 6 tháng",
            "details": ["SBV ưu tiên giải áp lực ngắn hạn", "Big4 đồng thuận"],
        },
        {
            "name": "Catalyst",
            "headline": "Kỳ họp Quốc hội T6/2026 quyết định",
            "details": ["Dự thảo công bố T4", "Lấy ý kiến T5"],
        },
        {
            "name": "Rủi ro",
            "headline": "Ý kiến IMF có thể đẩy Việt Nam sang Phương án B",
            "details": ["Article IV review T7", "Basel III timeline pressure"],
        },
        {
            "name": "Action",
            "headline": "Long VPB, TCB. Short BID, VCB nếu Phương án A pass",
            "details": ["Position sizing 5-7%", "Stop-loss -8%"],
        },
    ],
    title="Tóm tắt và khuyến nghị",
)
```

## Notes

- 4-quadrant grid 2x2 hoặc 4 column tùy width.
- Headline 1 sentence per quadrant.
