# `policy_fork` - 2 phương án + decision factors matrix

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import policy_fork`

---

## Khi nào dùng

- Regulatory decision analysis: Phương án A vs B với 4-6 criteria evaluate.
- Vendor selection / approach selection với scoring matrix.
- Strategic options review với weighted criteria.

## Khi nào KHÔNG dùng

- 2 option đơn giản không cần matrix - dùng `comparison_cards`.
- > 3 option - matrix quá lớn, dùng `heatmap`.
- Outcome scenarios (không phải decision factors) - dùng `scenario_cards`.

## Pair với

- `comparison_cards` summary trước khi vào fork detail.
- `flow_bridge` mechanism của lựa chọn được pick.

## Params

```python
policy_fork(
    option_a: dict,    # {"name", "headline", "tone"}
    option_b: dict,
    factors: list[dict],   # [{"name", "score_a", "score_b", "weight"?}]
    title: str = "",
)

# score: -2 (rất tệ), -1, 0, +1, +2 (rất tốt)
```

## Code template

```python
from viz import policy_fork

html = policy_fork(
    option_a={
        "name": "Phương án A",
        "headline": "Nâng trần SFL 30%→35%",
        "tone": "positive",
    },
    option_b={
        "name": "Phương án B",
        "headline": "Thay SFL bằng NSFR",
        "tone": "neutral",
    },
    factors=[
        {"name": "Tốc độ thực thi", "score_a": 2, "score_b": -1},
        {"name": "Phù hợp Basel III", "score_a": -1, "score_b": 2},
        {"name": "Tác động ngắn hạn", "score_a": 2, "score_b": 0},
        {"name": "Bền vững dài hạn", "score_a": -1, "score_b": 2},
        {"name": "Khả năng thông qua", "score_a": 2, "score_b": 0},
    ],
    title="Decision factors: Phương án A vs B",
)
```

## Notes

- Score -2..+2 dùng dot fill từ ô vuông đỏ nhỏ tới xanh lớn.
- Weight optional - nếu có, factor row có column weight.
