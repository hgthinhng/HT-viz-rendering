# Đội tàu lãi vận hành, lỗ chu kỳ nhiên liệu

`KHỐI 25 · TÓM TẮT ĐIỀU HÀNH BỐN Ô`

## Mô tả / khi nào dùng

Trả lời: "Nếu người đọc chỉ đọc đúng một khối trước khi rời báo cáo, khối đó nói gì?" Bốn ô cố định Luận điểm / Chất xúc tác / Rủi ro / Hành động, luôn đặt CUỐI bài, đúng một lần. Giới hạn cứng để tránh đẩy nguyên khối sang trang sau (khối dùng `break-inside: avoid`): ô Luận điểm/Hành động tối đa khoảng 3 câu, ô Chất xúc tác/Rủi ro tối đa 3 mục mỗi ô. Khác `11-exec-qa` (nhiều cặp hỏi-đáp tự do, giọng người đọc hỏi) và `24-bonus-key-point-callout` (một câu kết tự đúc kết, không có cấu trúc con). KHÔNG dùng giữa bài hoặc lặp lại nhiều lần trong cùng báo cáo: đặt quá 1 lần biến nó thành `24-bonus-key-point-callout` rải rác nhiều điểm nhấn nhỏ thay vì một điểm chốt duy nhất ở cuối. KHÔNG dùng khi báo cáo không đủ nội dung lấp cả 4 ô: chuyển sang `11-exec-qa` dạng hỏi-đáp linh hoạt hơn, không ép khung 4 ô cố định.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="exec-summary">
  <div class="es-head">
    <div class="es-kicker">Tóm tắt điều hành</div>
    <div class="es-meta">Dữ liệu chốt 30/06/2026 · Biên soạn 05/08/2026</div>
  </div>
  <div class="es-grid">
    <div class="es-cell es-thesis">
      <div class="es-label">Luận điểm</div>
      <p class="es-text">Đội tàu vận hành ở biên lãi gộp 18 đến 20%, nhưng biên EBITDA co lại vì nhiên liệu tăng nhanh hơn giá cước. Định giá P/B 0,9 lần chưa phản ánh đội tàu trẻ hơn trung bình ngành 4 năm.</p>
    </div>
    <div class="es-cell es-catalyst">
      <div class="es-label">Chất xúc tác</div>
      <ul class="es-list">
        <li><span class="es-tag">Q4/2026</span>Đợt đóng tàu thứ hai bàn giao, thêm 2 tàu feeder, nâng công suất tuyến nội Á khoảng 12%.</li>
        <li><span class="es-tag">T3/2027</span>Hạn IMO CII giai đoạn 2 buộc 6 tàu trên 20 tuổi nâng cấp hoặc thanh lý.</li>
      </ul>
    </div>
    <div class="es-cell es-risk">
      <div class="es-label">Rủi ro</div>
      <ul class="es-list">
        <li><b>Biển Đỏ kéo dài.</b> Phí bảo hiểm chiến tranh tăng theo chu kỳ căng thẳng, ăn vào biên khai thác.</li>
        <li><b>Đội tàu già hoá cục bộ.</b> 6 tàu trên 20 tuổi chiếm 26% tổng DWT, chi phí bảo dưỡng tăng nhanh.</li>
      </ul>
    </div>
    <div class="es-cell es-action">
      <div class="es-label">Hành động</div>
      <p class="es-text">Tích luỹ dưới vùng 24.000 đồng một cổ phiếu, chốt lãi một phần quanh 30.000 đồng. Theo dõi tiến độ đóng tàu quý 4 và giá dầu FO 380 làm hai biến xác nhận luận điểm.</p>
    </div>
  </div>
</div>
```
