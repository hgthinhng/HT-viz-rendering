# `scenario_matrix` - 2D Probability × Impact policy uncertainty

**Wave:** 1-3  
**Output:** HTML+CSS+SVG  
**Render:** `from viz import scenario_matrix`

---

## Khi nào dùng

- Policy uncertainty cần map probability + impact dimension.
- Risk matrix: high prob × high impact = focus zone.
- 4-6 outcome scenarios với cả prob và impact varying.

## Khi nào KHÔNG dùng

- Cần probability cộng = 100% - dùng `scenario_cards`.
- Single dimension - dùng `bar_horizontal`.

## Pair với

- `scenario_cards` follow up cho 2-3 scenario quan trọng nhất.

## Params

```python
scenario_matrix(
    scenarios: list[dict],   # [{"name", "probability": 0-100, "impact": -5..+5, "tone"?}]
    title: str = "",
)
```

## Code template

```python
from viz import scenario_matrix

html = scenario_matrix(
    scenarios=[
        {"name": "PA-A passes Q3", "probability": 50, "impact": 3, "tone": "positive"},
        {"name": "PA-B substituted", "probability": 25, "impact": -2, "tone": "negative"},
        {"name": "Status quo extended", "probability": 15, "impact": -4, "tone": "negative"},
        {"name": "PA-A + monetary easing", "probability": 10, "impact": 5, "tone": "positive"},
    ],
    title="Probability x Impact matrix - sửa Thông tư 22",
)
```

## Notes

- X-axis probability 0-100, Y-axis impact -5 đến +5.
- Quadrant labels italic mờ ở 4 góc.
