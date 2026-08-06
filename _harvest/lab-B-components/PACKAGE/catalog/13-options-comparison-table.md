# Ba phương án bổ sung năng lực đội tàu

`KHỐI 13 · BẢNG SO SÁNH PHƯƠNG ÁN`

## Mô tả / khi nào dùng

Trả lời: "Trong N phương án loại trừ lẫn nhau, phương án nào thắng theo tiêu chí nào?" Cột khuyến nghị được tô nền nhẹ (không dùng viền trái màu để tránh dấu hiệu "AI slop"). KHÔNG dùng khi các phương án không loại trừ nhau (có thể làm song song); khi đó dùng swimlane.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="table-wrap">
  <table class="opt-compare">
    <thead><tr><th scope="col">Tiêu chí</th><th scope="col">Đóng mới</th><th scope="col" class="rec">Mua tàu đã qua sử dụng</th><th scope="col">Thuê định hạn (charter-in)</th></tr></thead>
    <tbody>
      <tr><td>CAPEX ban đầu</td><td>Cao (28–32 triệu USD/tàu)</td><td class="rec">Trung bình (14–17 triệu USD/tàu)</td><td>Thấp (không CAPEX)</td></tr>
      <tr><td>Thời gian triển khai</td><td><span class="mark-no">✕</span> 22–26 tháng</td><td class="rec"><span class="mark-yes">✓</span> 2–4 tháng</td><td><span class="mark-yes">✓</span> 1–2 tháng</td></tr>
      <tr><td>Tuổi thọ khai thác còn lại</td><td><span class="mark-yes">✓</span> 25 năm</td><td class="rec"><span class="mark-partial">◐</span> 12–15 năm</td><td><span class="mark-no">✕</span> theo hợp đồng</td></tr>
      <tr><td>Tuân thủ CII dài hạn</td><td><span class="mark-yes">✓</span> Đạt chuẩn mới nhất</td><td class="rec"><span class="mark-partial">◐</span> Cần nâng cấp</td><td><span class="mark-partial">◐</span> Phụ thuộc chủ tàu</td></tr>
      <tr><td>IRR ước tính (10 năm)</td><td>9,8%</td><td class="rec">13,4%</td><td>N/A (không sở hữu)</td></tr>
    </tbody>
  </table>
  </div>
```
