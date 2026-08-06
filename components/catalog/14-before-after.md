# Trước và sau khi lắp hệ thống lọc khí thải (scrubber)

`KHỐI 14 · SO SÁNH TRƯỚC/SAU`

## Mô tả / khi nào dùng

Trả lời: "Một thay đổi cụ thể tạo khác biệt gì, đo bằng đúng 1 con số mỗi bên?" KHÔNG dùng khi có >1 chỉ tiêu cần so sánh cùng lúc (dùng bảng hairline với 2 cột thời điểm).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="ba-compare">
    <div class="ba-panel before">
      <div class="ba-label">Trước lắp scrubber</div>
      <div class="ba-headline">612 <span style="font-size:14px;font-weight:400;">USD/tấn</span></div>
      <div class="ba-desc">Buộc dùng nhiên liệu VLSFO 0,5S đắt hơn để tuân thủ MARPOL Annex VI, không thể tận dụng chênh lệch giá với HSFO.</div>
    </div>
    <div class="ba-arrow" aria-hidden="true">→</div>
    <div class="ba-panel after">
      <div class="ba-label">Sau lắp scrubber (6 tàu)</div>
      <div class="ba-headline">471 <span style="font-size:14px;font-weight:400;">USD/tấn</span></div>
      <div class="ba-desc">Chuyển về dùng HSFO rẻ hơn kèm lọc khí thải đạt chuẩn; hoàn vốn đầu tư scrubber ước tính 22 tháng ở chênh lệch giá hiện hành.</div>
    </div>
  </div>
```
