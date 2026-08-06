# PROMPT — Harsh-review + chốt 1 "theme.md" canonical (StoiX)

> Mục tiêu: từ catalog đầy đủ, RA QUYẾT ĐỊNH — mỗi vai trò 1 giá trị canonical, 2 mode
> Light/Dark, GIỮ variant cũ làm alias (appendix), không xoá. Đây là bước biến catalog
> thành brand theme thật. Copy khối dưới vào session có brand-consolidated-light-dark.md.

---

```
VAI TRÒ
Bạn là brand director kiêm design-token lead. Việc của bạn KHÔNG phải liệt kê (đã có
catalog), mà là RA QUYẾT ĐỊNH có kỷ luật: chốt MỘT bộ token canonical cho brand StoiX,
2 mode Light/Dark. Bạn được phép nói thẳng chỗ nào đang "thừa màu / trôi dạt".

BỐI CẢNH
- Catalog đầy đủ ở `brand-consolidated-light-dark.md` (14 variant + nhóm trung lập,
  3 dự án: StoiX Read, exam-ops, CFA Notes). Brand book chính thức nhất = exam-ops
  v2-tokens.css "The Ledger Doctrine v2.1".
- Vấn đề đã biết (drift cần quyết): vàng 4 sắc; đỏ 3 sắc (pen-red/Pompeii/cam-đất);
  serif display 3-4 họ; giấy sáng 4 độ ngà.
- Multiplicity HỢP LỆ (giữ, KHÔNG coi là thừa): subject accents (10 môn), formula var
  cycle (8), box callout (5), semantic status. Đây là màu theo CHỨC NĂNG.

NHIỆM VỤ (trình bày lý do từng bước)
B1. Với mỗi vai trò brand (paper/bg, ink/text, gold, red accent, rule, serif display,
    sans, mono): chọn 1 giá trị CANONICAL cho Light và 1 cho Dark. Nêu lý do 1 dòng,
    ưu tiên anchor theo "Ledger Doctrine v2.1" rồi hoà với 2 surface còn lại.
B2. Gộp vàng về MỘT thang (deep → mid → bright → glow) thay vì 4 mã rời.
B3. Giữ nguyên các functional palette (subject/formula/box/semantic) thành mục riêng,
    ghi rõ "giữ vì theo chức năng".
B4. Liệt kê DRIFT còn mở cần người chốt (vd chọn serif nào) — đánh dấu [OPEN], đề xuất
    phương án mặc định nhưng KHÔNG tự quyết thay người.
B5. APPENDIX: bảng map MỌI variant cũ (14) → canonical Light/Dark + token nào thành
    alias. Không variant nào bị xoá; phải truy được đường migrate.
B6. Self-check: mọi token canonical phải truy ngược về 1 hex THẬT trong catalog (không
    bịa). Đếm: canonical bao nhiêu token, alias bao nhiêu, functional giữ bao nhiêu.

FORMAT OUTPUT — file `theme.md`
  # 0 Nguyên tắc (1 brand, 2 mode, theme = opinionated)
  # 1 Type (canonical serif/sans/mono + alt)
  # 2 LIGHT (Paper) — bảng token canonical
  # 3 DARK (Noir) — bảng token canonical
  # 4 Gold — 1 thang
  # 5 Functional palettes (giữ: subject/formula/box/semantic)
  # 6 Drift cần quyết [OPEN]
  # 7 Appendix: variant → canonical alias map
  # 8 Self-check + đếm
Dùng CSS custom property naming (--paper, --ink, --gold, --accent...) để dễ wire code.

RÀNG BUỘC
- theme.md là OPINIONATED: mỗi vai trò 1 canonical. KHÔNG bê nguyên 14 variant vào core.
- KHÔNG xoá variant: cái không lên canonical thì xuống Appendix làm alias.
- KHÔNG bịa hex; chỉ dùng giá trị có thật trong catalog/code; chưa chắc thì ghi [OPEN].
- Phân biệt rạch ròi "drift (thừa, cần gộp)" vs "functional (giữ)".
- Không em-dash. Kết thúc bằng: "Canonical N token · alias M · functional K · 0 hex bịa."
```

---

### Ghi chú
- **Structured mode**, Score 3. Kỹ thuật ngầm: CoT (lý do từng bước), self-consistency
  (B6 truy ngược hex + đếm), negative-space (cấm bê 14 variant vào core, cấm bịa, cấm
  xoá), persona ("brand director" để dám ra quyết định harsh).
- Điểm khoá: tách bạch **drift (gộp)** vs **functional (giữ)** — đây là cái khiến output
  ra một theme gọn mà không mất chức năng.
- `[OPEN]` để dành đúng chỗ cần người quyết (vd serif display), AI không tự áp đặt.
