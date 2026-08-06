# Quy trình quyết định đầu tư tàu mới

`KHỐI 16 · CHUỖI BƯỚC QUY TRÌNH`

## Mô tả / khi nào dùng

Trả lời: "Một quy trình tuần tự có bao nhiêu bước, mỗi bước làm gì?" Mũi tên dùng CSS Grid/Flexbox thuần (KHÔNG dùng clip-path tam giác dễ vỡ khi đổ bóng hoặc khi in ở độ phân giải thấp). KHÔNG dùng khi các bước có thể chạy song song (dùng swimlane) hoặc khi >6 bước (chia 2 chuỗi).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="step-chain">
    <div class="step-item"><div class="step-num"></div><div class="step-title">Thẩm định nhu cầu tuyến</div><div class="step-desc">Phân tích cầu vận tải theo tuyến, đối chiếu công suất đội tàu hiện có</div></div>
    <div class="step-arrow" aria-hidden="true">→</div>
    <div class="step-item"><div class="step-num"></div><div class="step-title">Đàm phán đóng tàu / mua tàu</div><div class="step-desc">Chọn xưởng đóng tàu hoặc tàu đã qua sử dụng, chốt thông số kỹ thuật</div></div>
    <div class="step-arrow" aria-hidden="true">→</div>
    <div class="step-item"><div class="step-num"></div><div class="step-title">Thu xếp vốn</div><div class="step-desc">Phối hợp vay ngân hàng, trái phiếu xanh, và vốn tự có theo tỷ lệ 70/20/10</div></div>
    <div class="step-arrow" aria-hidden="true">→</div>
    <div class="step-item"><div class="step-num"></div><div class="step-title">Đăng kiểm &amp; bàn giao</div><div class="step-desc">Kiểm định theo chuẩn đăng kiểm đã chọn, nghiệm thu kỹ thuật</div></div>
    <div class="step-arrow" aria-hidden="true">→</div>
    <div class="step-item"><div class="step-num"></div><div class="step-title">Khai thác thương mại</div><div class="step-desc">Đưa vào tuyến khai thác, theo dõi hiệu suất 6 tháng đầu</div></div>
  </div>
```
