# `mechanism_breakdown` - Input → Process → Output 3-stage horizontal

**Wave:** 1-3  
**Output:** HTML+CSS+SVG  
**Render:** `from viz import mechanism_breakdown`

---

## Khi nào dùng

- Mechanism explanation 3 stage rõ ràng (input/process/output).
- Production flow / value chain visualization.
- System logic explain với 3 distinct phases.

## Khi nào KHÔNG dùng

- Flow > 3 stage - dùng `flow_bridge` (vertical).
- Decision branches - dùng `policy_fork`.
- Capital flow nguồn → đích - dùng `sankey_mini`.

## Pair với

- `gauge` mở Phần với output number, mechanism_breakdown explain how.

## Params

```python
mechanism_breakdown(
    input_stage: dict,    # {"label", "items": list[str]}
    process_stage: dict,
    output_stage: dict,
    title: str = "",
)
```

## Code template

```python
from viz import mechanism_breakdown

html = mechanism_breakdown(
    input_stage={
        "label": "Input",
        "items": ["Tiền gửi <12T", "Vốn điều lệ", "Phát hành GTCG"],
    },
    process_stage={
        "label": "Quy đổi (Thông tư 22)",
        "items": ["Hệ số quy đổi 0.7", "Trừ FRR", "Cap 30% trần SFL"],
    },
    output_stage={
        "label": "Output",
        "items": ["Vốn dài hạn cho phép", "Limit tín dụng dài hạn"],
    },
    title="Cơ chế tính SFL theo Thông tư 22",
)
```

## Notes

- Arrow giữa các stage màu accent.
- Items list compact 2-4 bullet/stage.
