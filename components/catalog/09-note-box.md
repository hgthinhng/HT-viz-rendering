# Giả định · Cảnh báo · Điều kiện hủy

`KHỐI 09 · NOTE-BOX (3 BIẾN THỂ)`

## Mô tả / khi nào dùng

Ba biến thể dùng chung khung (border-top/bottom hairline, nhãn mono viết hoa) nhưng khác màu nhãn để phân biệt mức độ nghiêm trọng. KHÔNG lạm dụng quá 1 note-box mỗi 2 màn hình cuộn; dùng nhiều sẽ mất tác dụng nhấn. KHÔNG dùng khi nội dung là luận điểm chính của mục: `color: var(--ink-md)` làm chữ nhạt hơn thân bài và khung chỉ có hairline mỏng, đưa luận điểm chính vào đây sẽ đọc như một ghi chú phụ chứ không phải kết luận; dùng assertion-evidence (khối 10) hoặc key-point (khối phụ 2) khi cần nhấn mạnh.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="note-box assumption">
    <p>Toàn bộ dự phóng doanh thu giả định giá dầu VLSFO bình quân 620 USD/tấn trong 12 tháng tới (bình quân 6 tháng gần nhất: 598 USD/tấn). Nếu giá vượt 700 USD/tấn, biên EBITDA giảm thêm ước tính 3,5 điểm phần trăm.</p>
  </div>
  <div class="note-box warning">
    <p>Cước giao ngay tuyến nội Á đã biến động ±22% chỉ trong quý 1/2026 do gián đoạn tuyến Biển Đỏ. Hợp đồng khai thác dài hạn hiện chỉ phủ 58% công suất đội tàu, phần còn lại chịu rủi ro giá giao ngay trực tiếp.</p>
  </div>
  <div class="note-box kill">
    <p>Dừng kế hoạch đóng mới 2 tàu hàng rời nếu: (a) tỷ lệ nợ vay/vốn chủ vượt 1,8× tại thời điểm giải ngân đợt 2, HOẶC (b) giá đóng tàu tại xưởng đối tác tăng &gt;12% so với báo giá tham chiếu 2026-Q1, HOẶC (c) biên EBITDA dưới 15% trong 2 quý liên tiếp.</p>
  </div>
```
