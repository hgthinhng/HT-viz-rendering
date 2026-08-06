---
name: note-pipeline-viz
description: >
  Worker render data figures cho CFA note qua viz-factory engine (PowerShell + headless Chrome).
  Phase 4.6 cua note-pipeline chain. Ba pass gom advise + author [VIZ] markers + spec.json,
  render PNG qua build_spec.ps1 (hoac xuat render manifest neu moi truong khong render duoc),
  insert [FIGURE] blocks vao markup roi re-render docx. LUON dung khi orchestrator dispatch
  action viz_only, hoac user noi "render viz", "them chart", "build figures", "ve hinh cho note",
  "chen hinh viz". KHONG dung cho hinh minh hoa conceptual (do la image hints Phase 4.5 voi
  DALL-E prompt, user tu generate). KHONG goi truc tiep ngoai orchestrator tru khi user explicit.
---

# note-pipeline-viz

Worker biến số liệu trong note thành data figures chất lượng xuất bản, embed thẳng vào docx.
Engine là **viz-factory** (folder độc lập, KHÔNG nằm trong skill này).

## Phân công với image hints (Phase 4.5)

| Loại hình | Workflow | Ai làm |
|---|---|---|
| Data figure: chart, bảng pivot, payoff, tree, waterfall, gauge, heatmap... | viz-factory (skill này) | Pipeline render + tự chèn |
| Hình conceptual/nghệ thuật: metaphor, scene minh hoạ | Image hints: BOX_NOTE + DALL-E prompt | User generate qua trình tạo ảnh chuyên dụng, tự chèn |

Cả hai cùng tồn tại trong một module. Advisor quyết định loại nào cho từng slot.

## VIZ_ROOT resolution

Engine resolve theo thứ tự, dừng ở match đầu tiên:

1. `%USERPROFILE%\.claude\skills\viz-factory` nếu tồn tại (folder skill đã deploy).
2. Folder `viz-factory` trong workspace đang mount (repo nguồn).
3. Không thấy: hỏi user đường dẫn. Không đoán.

Catalog component + params: `<VIZ_ROOT>/catalog/INDEX.md` và `catalog/<component>.md`.
Quy trình advisor + parsimony: `<VIZ_ROOT>/references/VIZ_ADVISOR.md`.
Marker convention: `<VIZ_ROOT>/references/MARKER_CONVENTION.md`.

## Workflow: 3 pass

### Pass A: Advise + Author

1. Đọc `work_{module}/{module_id}.markup.md`. Theo VIZ_ADVISOR, chọn 2-5 data figure cho module.
   Mỗi figure phải pass parsimony test (thiếu nó người đọc mất capability thật sự). Không vẽ trang trí.
2. Tại mỗi slot, chèn directive vào markup (sau block BODY liên quan):
   ```
   [VIZ: <component> | id=<N.M.x> | caption=Hình <N.M.x>: <mô tả tiếng Việt> | params={<inline JSON>}]
   ```
   Quy tắc: id duy nhất trong module (N=section, M=subsection, x=a/b/c); caption tiếng Việt textbook
   voice, không em-dash; params đúng schema `catalog/<component>.md`; SỐ LIỆU THẬT từ prose, không bịa.
   Body text gần đó nên tham chiếu: "... được minh họa ở Hình N.M.x."
3. Sinh spec: chạy `markup_to_spec.ps1` (Windows) hoặc tự author `<VIZ_ROOT>/examples/<MODULE>/spec.json`
   theo format trong viz-factory SKILL.md. Validate qua `validate_markup.py` (W31/W32 check id + caption).

### Pass B: Render (environment-gated)

```bash
python3 scripts/viz_env_check.py --spec "<VIZ_ROOT>/examples/<MODULE>/spec.json" --manifest work_{module}/render_manifest.md
```

- `can_render: true` (Windows, có PowerShell): chạy
  `powershell -File <VIZ_ROOT>\engine\build_spec.ps1 -Spec <VIZ_ROOT>\examples\<MODULE>\spec.json`
  Output: `<VIZ_ROOT>/out/<MODULE>_<id>.png` mỗi figure. Mở từng PNG kiểm tra: text sạch, số khớp prose.
- `can_render: false` (Cowork Linux sandbox): script đã ghi `render_manifest.md` chứa đúng 1 lệnh
  PowerShell. Báo user chạy lệnh đó trên Windows rồi DỪNG chờ. Không đoán kết quả, không skip.

### Pass C: Insert + re-render

```bash
python3 scripts/figures_insert.py work_{module}/{module_id}.markup.md --out-dir "<VIZ_ROOT>/out" --module <MODULE> --apply
```

Script thay mỗi `[VIZ:]` directive có PNG tương ứng bằng `[FIGURE: <png path> | <caption>]`.
Directive thiếu PNG giữ nguyên (render thành placeholder strip 【HÌNH N.M.x】 trong docx, không phải lỗi).
Sau đó re-render docx qua note-pipeline-render. GATE 2 + GATE 3 áp dụng lại.

## Render engine contract (note-pipeline-render)

- `[FIGURE: path | caption]`: embed PNG full column width, caption Inter 9pt muted italic centered.
  Path không tồn tại: placeholder strip + warning stderr, không crash.
- `[VIZ: ...]`: render placeholder strip tinted (#F0EDE6, gold left rule) theo MARKER_CONVENTION.
- Validator: W30 (FIGURE path thiếu), W31 (VIZ thiếu id/caption), W32 (VIZ id trùng). Em-dash trong
  caption bị E01 chặn như mọi text khác.

## Constraints

1. Số liệu trong params phải khớp prose từng chữ số. Sai số liệu là CRITICAL ở audit.
2. Caption tiếng Việt, textbook voice, không em-dash, không tham chiếu người đọc.
3. Parsimony: 2-5 figure mỗi module là đủ. Bảng đã render đẹp bằng [TABLE] thì không cần viz.
4. Không sửa logic viz-factory engine từ skill này. Engine là read-only dependency.
5. Theme mặc định cfa. Không hardcode hex màu trong params trừ khi bắt buộc.

## Files

```
note-pipeline-viz/
├── SKILL.md (this)
└── scripts/
    ├── viz_env_check.py     (detect PowerShell/Chrome; ghi render_manifest.md khi không render được)
    └── figures_insert.py    ([VIZ:] markers -> [FIGURE:] blocks khi PNG sẵn sàng)
```
