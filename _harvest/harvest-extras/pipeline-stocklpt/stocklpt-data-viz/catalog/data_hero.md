# `data_hero` - 1 trang dramatic 1 mega number

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import data_hero`

---

## Khi nào dùng

- Signature page mở Phần với hero stat dramatic.
- Cuối Phần với 1 con số định-Phần (key takeaway numerical).
- Cover page deep analysis.

## Khi nào KHÔNG dùng

- Multi-stat overview - dùng `stat_dashboard`.
- Stat có context comparison - dùng `gauge` (vs threshold) hoặc `before_after_comparison`.
- > 1 hero stat - dùng `infographic_panel` (Wave 10) với 4 supporting facts.

## Pair với

- `marginalia` chú thích source/methodology.
- `flow_bridge` ngay sau để giải thích why.

## Params

```python
data_hero(
    big_number: str,      # text monospace lớn (vd "111,9%")
    label: str,           # uppercase letterspaced label
    description: str = "", # 1-2 sentence context
    tone: str = "neutral",
)
```

## Code template

```python
from viz import data_hero

html = data_hero(
    big_number="111,9%",
    label="LDR HỆ THỐNG Q1/2026",
    description="Mức cao nhất kể từ 2018, vượt kỳ vọng SBV 12 đp.",
    tone="negative",
)
```

## Notes

- big_number font-size ~80pt JetBrains Mono.
- Tone color toàn page background: positive xanh nhạt, negative bordeaux nhạt, neutral paper.
