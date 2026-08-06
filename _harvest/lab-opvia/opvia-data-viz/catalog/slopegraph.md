# `slopegraph` - before/after với rerank visible

**Wave:** 8  
**Output:** Inline SVG  
**Render:** `from viz_wave8 import slopegraph`

---

## Khi nào dùng

- Policy impact n>=4 entity - đường đan chéo = signal rerank lớn.
- Pre-merger vs post-merger ranking.
- Q-1 vs Q stock weight portfolio rebalance.

## Khi nào KHÔNG dùng

- n=2 - dùng `before_after_comparison`.
- Entity rerank > 5 vị trí giao - quá rối, split 2 slopegraph.
- Multi-period (3+) - dùng `line_with_annotations`.

## Pair với

- `heatmap` matrix detail trước slopegraph.
- `marginalia` chú thích methodology.

## Params

```python
slopegraph(
    items: list[dict],   # [{"label", "before", "after", "highlight"?}]
    label_before: str,
    label_after: str,
    title: str = "",
    unit: str = "",
)
```

## Code template

```python
from viz_wave8 import slopegraph

html = slopegraph(
    items=[
        {"label": "VPB", "before": 28.3, "after": 35.0, "highlight": True},
        {"label": "TCB", "before": 26.9, "after": 32.5, "highlight": True},
        {"label": "MBB", "before": 22.1, "after": 26.8},
        {"label": "ACB", "before": 19.5, "after": 23.2},
    ],
    label_before="SFL hiện tại (trần 30%)",
    label_after="Sau Phương án A (trần 35%)",
    title="Tác động Phương án A lên SFL 4 NHTM",
    unit="%",
)
```

## Notes

- Lines collision-aware: auto adjust label position để không overlap.
- Highlight=True line brass + bold.
