# `infographic_panel` - dark Indigo luxury panel hero 56pt + 4 facts

**Wave:** 10  
**Output:** HTML+CSS  
**Render:** `from viz_wave10 import infographic_panel`

---

## Khi nào dùng

- Cover signature deep analysis.
- Section opener art kèm hero stat.
- Mid-section breakdown 1 mega stat + 4 supporting metrics.

## Khi nào KHÔNG dùng

- Inline mid-prose - quá heavy.
- Daily report - không phù hợp format ngắn.
- < 4 supporting facts - dùng `data_hero` đơn giản hơn.

## Pair với

- `marginalia` chú thích nếu cần.

## Params

```python
infographic_panel(
    hero_number: str,       # mega stat 56pt monospace
    hero_label: str,        # uppercase letterspaced
    supporting_facts: list[dict],   # [{"label", "value"}]
    title: str = "",
    background: str = "indigo",   # "indigo" | "ivory"
)
```

## Code template

```python
from viz_wave10 import infographic_panel

html = infographic_panel(
    hero_number="111,9%",
    hero_label="LDR HỆ THỐNG Q1/2026",
    supporting_facts=[
        {"label": "Vượt trần Thông tư 22", "value": "+26,9 đp"},
        {"label": "Cao nhất kể từ", "value": "2018"},
        {"label": "Số NHTM vượt trần", "value": "9/10"},
        {"label": "Thanh khoản LCR", "value": "82%"},
    ],
    title="Áp lực hệ thống ngân hàng",
    background="indigo",
)
```

## Notes

- Background indigo #2A1A4A với text ivory.
- Hero 56pt JetBrains Mono.
- Supporting facts grid 2x2 dưới hero.
