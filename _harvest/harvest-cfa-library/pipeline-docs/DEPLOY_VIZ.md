# DEPLOY: viz-factory integration vào note-pipeline chain (2026-06-10)

## Đã thay đổi gì

| File | Thay đổi |
|---|---|
| `note-pipeline-viz/` (MỚI) | Child skill Phase 4.6: SKILL.md + viz_env_check.py + figures_insert.py |
| `note-pipeline-render/scripts/render_engine.py` | +147 dòng: block `[FIGURE: path \| caption]` (embed PNG full column width + caption Inter 9pt muted italic, placeholder nếu thiếu file) và `[VIZ: ...]` (placeholder strip tinted theo MARKER_CONVENTION). Golden test EQ_M3: 12 file output byte-identical khi markup không có 2 tag mới. |
| `note-pipeline-create/scripts/validate_markup.py` | +W30 (FIGURE path thiếu), W31 (VIZ thiếu id/caption), W32 (VIZ id trùng). [VIZ:]/[FIGURE:] là tag hợp lệ. |
| `note-pipeline/SKILL.md` | 6 child skills, Phase 4.6 viz, action viz_only, phân công image hints (conceptual, DALL-E prompt user tự tạo) vs viz-factory (data figures). |
| `note-pipeline/scripts/intent_classifier.py` | Action `viz_only`: "render viz", "thêm chart", "build figures", "vẽ hình cho note"... (đặt TRƯỚC pattern render_only). |

viz-factory folder GIỮ NGUYÊN độc lập (không merge vào skill nào). Engine không bị sửa.

## Deploy

### Claude app (Cowork): đã build sẵn bundle
4 file .skill trong folder "note_pipeline Claude skill" đã được cập nhật (bản cũ backup `.pre-viz.bak`):
note-pipeline.skill, note-pipeline-create.skill, note-pipeline-render.skill, note-pipeline-viz.skill (MỚI).
Cài lại qua Settings > Capabilities (gỡ bản cũ, add bản mới; note-pipeline-viz add lần đầu).

### Claude Code (~/.claude/skills): copy 3 lệnh
```powershell
robocopy "<staging>\note-pipeline-viz" "$env:USERPROFILE\.claude\skills\note-pipeline-viz" /E
copy "<staging>\note-pipeline-render\scripts\render_engine.py" "$env:USERPROFILE\.claude\skills\note-pipeline-render\scripts\" /Y
copy "<staging>\note-pipeline-create\scripts\validate_markup.py" "$env:USERPROFILE\.claude\skills\note-pipeline-create\scripts\" /Y
copy "<staging>\note-pipeline\SKILL.md" "$env:USERPROFILE\.claude\skills\note-pipeline\" /Y
copy "<staging>\note-pipeline\scripts\intent_classifier.py" "$env:USERPROFILE\.claude\skills\note-pipeline\scripts\" /Y
```
`<staging>` = folder chứa file này. Sau copy: xoá `__pycache__` trong các skill folder.

## Cách dùng (sau deploy)

- Trong pipeline: orchestrator tự chạy Phase 4.6 sau image hints (optional, advisor quyết định).
- Standalone: "render viz cho EQ_M3" / "thêm chart cho FI_M1" → action viz_only.
- Trong Cowork: Pass B sẽ ghi `work_{module}/render_manifest.md` chứa 1 lệnh PowerShell; chạy lệnh đó
  trên Windows rồi nói "tiếp tục" để Pass C chèn hình. Trong Claude Code (Windows): tự động hoàn toàn.

## Smoke test đã chạy (2026-06-10, Cowork sandbox)

- Golden test: EQ_M3.markup.md (không VIZ/FIGURE) render qua engine cũ vs mới: 12/12 file byte-identical.
- Embed test: chèn [FIGURE] (PNG thật từ viz-factory/out) + [VIZ] chưa render vào EQ_M3 → docx 219 KB,
  PDF trang 4 hiển thị: hình yield curve full column width + caption đúng style, placeholder strip
  【HÌNH 2.1.b】 với gold rule + dòng "chèn ảnh: *_2.1.b.png". Screenshot: outputs/smoke_p4.png.
- Validator: 0 error trên markup có VIZ/FIGURE hợp lệ; W30/W31/W32 bắt đúng case thiếu file/thiếu id/trùng id.
- intent_classifier: "render viz cho EQ_M3" → viz_only; "render lại docx" vẫn → render_only.

## Chưa làm (ngoài phạm vi đợt này)

- markup_to_spec.ps1 tự sinh spec từ [VIZ:] markers: đã có sẵn trong viz-factory, Pass A gọi khi trên
  Windows; trong Cowork thì LLM tự author spec.json (đúng thiết kế).
- GATE 2/3 numeric cross-check giữa params và prose: hiện dựa vào audit harsh thủ công Phase 5.

## Hardening round (2026-06-10, cùng ngày)

Audit 17 scripts toàn chain: 17/17 syntax OK. 4 bug root-cause được fix trong render_engine.py:

1. **Thiếu `if __name__ == '__main__'` guard** (file bị cụt đuôi từ bản copy cũ): đây là root cause
   của workaround "import render_engine + sys.argv injection" lặp lại 6+ session. CLI giờ chạy thẳng.
2. **"collected N formulas" misleading**: regex prescan chỉ đếm [FORMULA] bare, bỏ sót [FORMULA: name=...].
   EQ_M3 giờ báo đúng 14 thay vì 3.
3. **name= regex `\w+` silent fail**: FORMULA/BOX_* với name có space hoặc tiếng Việt có dấu giờ parse
   bình thường, hết phải slugify thủ công mỗi module.
4. **Compound ref renumber bug** ("Công thức 3.1 và 3.2" chỉ đổi số đầu): chain-aware scan + replace,
   có guard chống false-positive với phần trăm (4.2%) và số thường (5.3 tỷ).

Golden test EQ_M3 sau hardening: 12/12 file output byte-identical. Unit tests: chain renumber,
percentage guard, Vietnamese name parse, CLI --help đều pass.

Folder cài đặt: "SKILL CAI MOI 2026-06-10" chứa đủ 7 .skill (6 chain + viz), tất cả qua
package_skill validator của skill-creator. qc/audit/deliver không sửa nhưng đóng gói lại cùng đợt
để 1 folder = trọn bộ chain.
