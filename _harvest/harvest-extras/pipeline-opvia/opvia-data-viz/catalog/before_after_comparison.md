# `before_after_comparison` - state A → state B với delta

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import before_after_comparison`

---

## Khi nào dùng

- n=2 entity hoặc 1 system trước-sau policy.
- Pre-merger vs post-merger metrics.
- Q-1 vs Q ratio comparison cho 1 entity.

## Khi nào KHÔNG dùng

- n>=4 entity với rerank visible - dùng `slopegraph` (Wave 8).
- Multi-period change - dùng `line_with_annotations`.
- Same entity multi-metric - dùng `stat_dashboard`.

## Pair với

- `flow_bridge` explain mechanism làm thay đổi.
- `gauge` cho metric chính trước-sau.

## Params

```python
before_after_comparison(
    label_before: str,    # "Trước Phương án A"
    label_after: str,     # "Sau Phương án A (3 năm)"
    metrics: list[dict],  # [{"name", "before", "after", "unit"?, "tone"?}]
    title: str = "",
)
```

## Code template

```python
from viz import before_after_comparison

html = before_after_comparison(
    label_before="Trước Thông tư 22 sửa",
    label_after="Sau Phương án A (3 năm)",
    metrics=[
        {"name": "LDR hệ thống", "before": "111,9%", "after": "98,5%", "tone": "positive"},
        {"name": "VPB SFL", "before": "28,3%", "after": "32,1%", "tone": "neutral"},
        {"name": "Lợi suất TPCP 10y", "before": "3,8%", "after": "4,1%", "tone": "negative"},
    ],
    title="Tác động dự kiến Phương án A sau 3 năm",
)
```

## Notes

- Arrow giữa before/after màu brass.
- Tone: positive xanh, negative đỏ, neutral slate.
