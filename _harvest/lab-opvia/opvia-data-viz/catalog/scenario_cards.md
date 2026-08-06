# `scenario_cards` - 3 kịch bản với probability

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import scenario_cards`

---

## Khi nào dùng

- Cuối bài deep analysis có scenario discussion (base/bull/bear).
- Policy uncertainty cần break thành 3-4 outcome paths.
- Forecast với explicit probability assignment.

## Khi nào KHÔNG dùng

- 2 outcome - dùng `comparison_cards` hoặc `policy_fork`.
- Scenario có cả probability + impact dimension - dùng `scenario_matrix` 2D.
- > 4 scenario - quá nhiều, force pick 3 chính.

## Pair với

- `timeline_horizontal` cho timing forecast của mỗi scenario.
- `executive_summary_box` summary cuối bài, scenario_cards là 1 trong 4 quadrant.

## Params

```python
scenario_cards(
    scenarios: list[dict],  # [{"name", "probability", "tone", "headline", "details": list[str]}]
)

# tone: "positive" (bull), "negative" (bear), "neutral" (base)
# probability cộng = 100% (validator check)
```

## Code template

```python
from viz import scenario_cards

html = scenario_cards(
    scenarios=[
        {
            "name": "Cơ sở",
            "probability": 50,
            "tone": "neutral",
            "headline": "Phương án A thông qua, trần SFL nâng từ 30% lên 35%",
            "details": [
                "VPB và TCB thoát pressure ngay quý sau",
                "Lợi suất TPCP tăng nhẹ +20bps trong 6 tháng",
                "Tăng trưởng tín dụng giữ 14-15%",
            ],
        },
        {
            "name": "Tích cực",
            "probability": 20,
            "tone": "positive",
            "headline": "Phương án A + đi kèm gói monetary easing",
            "details": ["...", "..."],
        },
        {
            "name": "Tiêu cực",
            "probability": 30,
            "tone": "negative",
            "headline": "Phương án B áp dụng - thay NSFR thay vì nới SFL",
            "details": ["...", "..."],
        },
    ],
)
```

## Failure modes

- **probability không cộng = 100%**: validator fail. Round error ±1% OK.
- **details > 4 bullet/card**: card overflow vertical. Pick 3 bullet quan trọng nhất.
- **headline > 80 chars**: wrap nhiều dòng. Edit cô đọng.

## Notes

- Tone color: positive xanh, negative đỏ, neutral slate.
- Probability hiển thị monospace lớn ở góc card.
