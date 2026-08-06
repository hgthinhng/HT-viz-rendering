# `comparison_cards` - cards so sánh side-by-side 2-3 lựa chọn

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import comparison_cards`

---

## Khi nào dùng

- Phương án A vs B: rất StockLPT signature pattern.
- 2-3 stock peers cùng sector với key metrics.
- 2 vendor / regulator approach so sánh.

## Khi nào KHÔNG dùng

- 4+ option - dùng `policy_fork` (decision matrix) hoặc `heatmap`.
- Before/after same entity - dùng `before_after_comparison`.
- 1 option deep dive - dùng prose + `data_hero`.

## Pair với

- `policy_fork` - cards là summary, fork là decision matrix.
- `scenario_cards` - cards là phương án, scenario là outcome.

## Params

```python
comparison_cards(
    cards: list[dict],   # [{"name", "tone", "headline", "metrics": [{"label", "value"}], "pros": [str], "cons": [str]}]
    title: str = "",
)
```

## Code template

```python
from viz import comparison_cards

html = comparison_cards(
    cards=[
        {
            "name": "Phương án A",
            "tone": "positive",
            "headline": "Nâng trần SFL từ 30% lên 35%",
            "metrics": [
                {"label": "Bank được lợi", "value": "5/10"},
                {"label": "Time to implement", "value": "6 tháng"},
            ],
            "pros": ["Đơn giản, dễ thông qua", "Giải áp lực ngay"],
            "cons": ["Không giải gốc rễ", "Cần re-evaluate sau 1 năm"],
        },
        {
            "name": "Phương án B",
            "tone": "neutral",
            "headline": "Thay SFL bằng NSFR theo Basel III",
            "metrics": [
                {"label": "Bank được lợi", "value": "8/10"},
                {"label": "Time to implement", "value": "18 tháng"},
            ],
            "pros": ["Theo chuẩn quốc tế", "Bền vững dài hạn"],
            "cons": ["Phức tạp", "Cần đào tạo"],
        },
    ],
    title="So sánh 2 phương án sửa Thông tư 22",
)
```

## Failure modes

- **pros/cons không cân bằng**: 1 card 5 pros 1 cons, card kia 2 pros 5 cons - reader cảm thấy bias. Cân nhắc symmetric.
- **metrics > 4**: card chật. Pick 3-4 metric nhất.

## Notes

- Tone color border: positive xanh, neutral slate, negative bordeaux.
- 2 hoặc 3 cards layout responsive.
