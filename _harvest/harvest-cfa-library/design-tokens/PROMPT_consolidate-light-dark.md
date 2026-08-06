# PROMPT — Hợp nhất (consolidate) toàn bộ mã thành 1 list đầy đủ, 2 nhóm SÁNG / TỐI

> Phase consolidate. Mục tiêu: gom MỌI token màu/font của 3 dự án vào ĐÚNG 2 ô lớn
> SÁNG (Light) và TỐI (Dark) — nhưng GIỮ NGUYÊN từng variant, không bỏ, không gộp mất.
> Copy nguyên khối dưới đây vào session AI có quyền đọc 3 folder (hoặc có sẵn brand-style.md).

---

```
VAI TRÒ
Bạn là design-system librarian. Nhiệm vụ DUY NHẤT: hợp nhất mọi mã màu/font đã được
catalog thành MỘT danh sách thống nhất đầy đủ, phân theo ĐÚNG 2 nhóm lớn:
SÁNG (Light) và TỐI (Dark). Bạn KHÔNG redesign, KHÔNG chọn "1 mã thắng", KHÔNG bịa.

BỐI CẢNH
Tôi có bản catalog hiện trạng 3 dự án ở `brand-style.md` (StoiX Read = web báo;
StoiX exam-ops = app, có design-system S2 với 5 tone + Brand Book v2.1 "Ledger
Doctrine"; CFA Notes = hệ render .docx). Mỗi dự án có nhiều theme/tone/phiên bản.
Phase này chỉ XẾP TẦNG: đưa tất cả vào 2 ô Sáng/Tối, mỗi theme là 1 variant con.

INPUT
- `brand-style.md` (catalog token đầy đủ — nguồn chính).
- Nếu thiếu/nghi ngờ, probe lại design (CHỈ file thiết kế, loại trừ node_modules,
  .git, .next, dist, .vercel, .playwright-cli, Extensions, .qbank-artifacts):
  · CFA Notes: render_engine.py (palette C, FONT_STACKS, FORMULA_VAR_COLORS,
    SUBJECT_COLORS, BOX_SPECS)
  · StoiX Read: styles.css + styles-v3/v4.css
  · exam-ops: src/ds/tokens/* + src/styles/v2-tokens.css

NGUYÊN TẮC PHÂN LOẠI (chỉ 2 ô lớn)
- SÁNG = mọi variant có surface nền sáng (ivory/cream/giấy ấm/paper).
- TỐI  = mọi variant có surface nền tối (noir/navy/midnight/warm-black).
- Một dự án có CẢ light lẫn dark → tách thành 2 variant, mỗi cái vào 1 ô.
- "+ variant" giữ NGUYÊN: mỗi tone/phiên bản/box-set/subject-accent là 1 mục con
  riêng, KHÔNG gộp kể cả khi gần giống (vd 4 sắc vàng vẫn liệt kê đủ 4).

NHIỆM VỤ (trình bày lý do từng bước)
B1. Liệt kê MỌI variant từ catalog; đếm n_variant.
   (Tối thiểu phải có: Notes ivory-editorial; Notes box-set + subject-accents;
    Read newsprint-light; Read dark-mode; Read sub-pages; exam paper; exam Ledger
    v2.1 paper; exam catalog cream/sage; exam study noir; exam funnel Platinum
    Noir; exam catalog indigo-noir; exam catalog-v4 Midnight Champagne.)
B2. Gán mỗi variant vào SÁNG hoặc TỐI theo độ sáng surface.
B3. Trong mỗi ô lớn, với MỖI variant in đủ token: nền/surface, ink/text, accent
    chính, vàng, đỏ, rule, + font (display/body/mono) + nguồn (dự án · file).
B4. Thêm "MASTER FLAT LIST" — 1 bảng phẳng: mỗi dòng = Nhóm(Sáng/Tối) | Variant |
    Vai trò | Hex/Font | Nguồn. Đây là "list full đầy đủ" để tra nhanh.
B5. SELF-CHECK: tổng token in ra = tổng token trong catalog (không mất mã nào).
    Báo n_variant và n_token cho mỗi ô; liệt kê mã nào "lưỡng cư" (xuất hiện 2 ô).

FORMAT OUTPUT
- File `brand-consolidated-light-dark.md` gồm:
  `# 0. Tổng quan + đếm`
  `# 1. SÁNG (Light)`  → từng variant con (token đủ + nguồn)
  `# 2. TỐI (Dark)`    → từng variant con (token đủ + nguồn)
  `# 3. MASTER FLAT LIST` (bảng phẳng toàn bộ mã)
  `# 4. Self-check + ghi chú` (điểm trôi dạt: nhiều sắc vàng/đỏ, serif khác họ,
       Dark có 2 tính cách ấm/lạnh) — chỉ GHI NHẬN, không tự quyết bỏ.
- (Tùy chọn) cập nhật `brand_theme_preview.html`: gom các tile thành đúng 2 cụm
  lớn "SÁNG" và "TỐI", mỗi tile vẫn render đúng màu thật của variant.
- Lưu vào folder CFA Notes (hoặc [FOLDER_OUTPUT]).

RÀNG BUỘC (đọc kỹ)
- SÁNG/TỐI chỉ là 2 ô phân loại cấp cao. TUYỆT ĐỐI không dùng nó như cớ để cắt
  giảm số theme/variant. Giữ 100% variant.
- KHÔNG gộp 2 variant thành 1, KHÔNG chọn mã "đại diện", KHÔNG đổi/bịa hex.
- Mọi giá trị phải trích từ catalog/code; file nào không đọc được thì ghi
  "chưa probe được", không đoán.
- Không em-dash trong văn bản tiếng Việt.
- Kết thúc bằng 1 dòng xác nhận: "Đã giữ N variant / M mã, 0 mã bị mất."
```

---

### Ghi chú dùng prompt
- **Structured mode**, Score 3. Kỹ thuật nhúng ngầm: CoT ("lý do từng bước"),
  self-consistency (B5 đếm token vào = ra), negative-space (cấm gộp/giảm/bịa),
  anti-hallucination ("ghi chưa probe được thay vì đoán"), persona ("librarian").
- Điểm mấu chốt mình khóa cứng theo yêu cầu của bạn: **Sáng/Tối = 2 big category,
  giữ toàn bộ + variant**. Prompt nhắc lại điều này ở cả NGUYÊN TẮC, NHIỆM VỤ và
  RÀNG BUỘC để AI không tự ý "tối giản".
- `[BIẾN]` cần thay khi tái dùng: `[FOLDER_OUTPUT]`, và 3 đường dẫn nguồn nếu khác.
- Khi muốn đi xa hơn (chọn 1 bộ token canonical thật sự): bỏ ràng buộc "KHÔNG chọn
  mã đại diện" và thêm "đề xuất 1 mã canonical cho mỗi vai trò, các mã còn lại
  đánh dấu legacy".
