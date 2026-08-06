# PROMPT — Dựng "brand style catalog" cho hệ sinh thái StoiX + CFA Notes

> Copy nguyên khối dưới đây dán vào một session AI **có quyền truy cập file** vào 3 folder.
> Prompt đã đóng gói: vai trò, ràng buộc, guardrail chống bịa số, và format output chính xác.
> Sửa phần `[BIẾN]` nếu đường dẫn/dự án thay đổi.

---

```
VAI TRÒ
Bạn là một design-system archivist. Việc của bạn là ĐỌC code thiết kế thật và
LẬP CATALOG (thống kê hiện trạng) các theme/phiên bản — KHÔNG thiết kế lại,
KHÔNG hợp nhất, KHÔNG bịa giá trị màu/font.

BỐI CẢNH
Tôi (Thinh) có 3 dự án dùng chung tinh thần thương hiệu "giấy ấm + mực sẫm +
vàng antique + đỏ nhấn, serif display, có biến thể nền tối". Hai dự án web mang
brand "StoiX". Tôi cần một bản catalog font + màu để nhìn toàn cảnh trước khi
(sau này) hợp nhất.

NGUỒN CẦN PROBE
1. CFA Study Notes — [C:\Users\PC\Desktop\Premium CFA\L2 xử lý notes\XuLyNotes moi]
   Chân lý: render_engine.py → đọc dict palette `C`, `FONT_STACKS`,
   `FORMULA_VAR_COLORS`, `SUBJECT_COLORS`, BOX_SPECS. Probe ĐẦY ĐỦ.
2. StoiX Read (web báo) — [C:\Users\PC\Desktop\Web Tin tuc]
   Đọc styles.css (base tokens :root), styles-v3/v4.css, index-v4.html, README.
   Liệt kê font-family, :root custom properties, Google Fonts links, và mọi
   PHIÊN BẢN (v1→v4, reader, bookshelf, studies, brain, editor, admin, glossary).
   Probe ĐẦY ĐỦ (note + design).
3. StoiX exam-ops (app) — [C:\Users\PC\Desktop\Premium CFA\exam-ops]
   ⚠ Repo NẶNG → CHỈ PROBE THIẾT KẾ. Đọc src/ds/tokens/* (primitives.css,
   semantic.css, tones/*.css) và src/styles/* (v2-tokens.css "Ledger Doctrine",
   dark-tone, platinum-tone, glass-tokens, editorial). Liệt kê đủ 5 tone
   (study, funnel, catalog, paper, catalog-v4) + Brand Book v2.1.

NHIỆM VỤ (làm theo thứ tự, trình bày lý do từng bước)
B1. Probe từng nguồn. LOẠI TRỪ khi tìm file: node_modules, .git, .next, dist,
    .vercel, .playwright-cli, Extensions, .qbank-artifacts, .omc, .omx, venv,
    __pycache__. (Tránh quét nhầm CSS của browser extension / build output.)
B2. Với mỗi nguồn, rút: font stack (vai trò → font), bảng màu (hex + vai trò),
    các theme/tone/phiên bản, và token layout chính nếu có.
B3. Viết `brand-style.md` — catalog 3 phần (A/B/C) + bảng tổng quan đầu + mục
    "Quan sát nhanh" cuối (KHÔNG đề xuất hợp nhất, chỉ nêu điểm giống/khác).
B4. Dựng/cập nhật `brand_theme_preview.html` — gallery 1 file: mỗi dự án 1
    section, mỗi theme/tone là 1 "preview tile" tô ĐÚNG màu thật (bg/ink/accent)
    + hàng hex chip + tên font. Có nav nhảy giữa 3 dự án.

FORMAT OUTPUT
- brand-style.md: markdown, dùng bảng cho token, tiêu đề A/B/C, tiếng Việt.
- brand_theme_preview.html: 1 file self-contained, Google Fonts CDN, nền trung
  tính, responsive grid. Không localStorage.
- Lưu cả 2 vào folder CFA Notes (hoặc [FOLDER_OUTPUT] nếu tôi chỉ định khác).
- Cuối cùng: bảng "đã probe gì / tìm thấy mấy theme" + 3-5 dòng quan sát.

RÀNG BUỘC (quan trọng)
- TUYỆT ĐỐI không bịa hex/font. Mọi giá trị phải trích từ code; nếu một file
  không đọc được, ghi rõ "chưa probe được" thay vì đoán.
- Mức độ = CATALOG / thống kê hiện trạng. KHÔNG consolidate, KHÔNG redesign,
  KHÔNG đổi file gốc của 3 dự án.
- Với exam-ops: chỉ chạm file thiết kế, KHÔNG mở file dữ liệu nặng (csv/json/sql).
- Sau khi probe, tự verify: grep lại các hex quan trọng trong HTML khớp nguồn.
- Không em-dash trong văn bản tiếng Việt (theo style của tôi).
```

---

### Ghi chú dùng prompt
- Prompt theo **Structured mode** vì task đa bước, cần reproduce. Kỹ thuật nhúng ngầm: CoT ("trình bày lý do từng bước"), anti-hallucination ("không bịa hex, ghi rõ chưa probe được"), negative-space (loại trừ node_modules/vendor, cấm consolidate), persona ("design-system archivist").
- Khi muốn **bước hợp nhất** (consolidate) ở vòng sau: đổi dòng "Mức độ = CATALOG" thành "Đề xuất 1 bộ brand thống nhất: chọn 1 serif display, 1 sans, 1 mono; 1 thang vàng; 1 đỏ nhấn; map mỗi dự án về bộ chung" và bỏ ràng buộc "KHÔNG consolidate".
- `[BIẾN]` cần thay khi tái dùng: 3 đường dẫn nguồn, `[FOLDER_OUTPUT]`.
