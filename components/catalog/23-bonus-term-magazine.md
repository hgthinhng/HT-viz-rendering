# Ba thuật ngữ ngành, trình bày kiểu tạp chí

`KHỐI PHỤ · THUẬT NGỮ DẠNG TẠP CHÍ`

## Mô tả / khi nào dùng

Không tính vào 22 component chính nhưng đủ tổng quát để đưa vào thư viện: giải nghĩa viết tắt kỹ thuật mà không cần footnote rời. KHÔNG dùng khi số thuật ngữ khác 3: `.term-mag` cố định `grid-template-columns: repeat(3, 1fr)` và luật bỏ `border-left` chỉ áp cho `.term:first-child` của toàn khối chứ không phải đầu mỗi hàng, nên từ thuật ngữ thứ 4 trở đi một đường kẻ dọc mồ côi xuất hiện ở đầu hàng mới; ít hơn 3 để lại cột trống lệch trái. Cũng KHÔNG dùng khi thuật ngữ đã quen thuộc với người đọc mục tiêu, vì giải nghĩa cái ai cũng biết làm báo cáo đọc chậm không cần thiết.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="term-mag">
    <div class="term"><div class="t-abbr">DWT</div><div class="t-full">Deadweight Tonnage</div><div class="t-gist">Trọng tải toàn phần tàu có thể chở, gồm hàng hóa, nhiên liệu, nước, thuyền viên. Chỉ tiêu chuẩn để so sánh quy mô đội tàu.</div></div>
    <div class="term"><div class="t-abbr">TEU</div><div class="t-full">Twenty-foot Equivalent Unit</div><div class="t-gist">Đơn vị quy đổi container 20 feet, dùng đo năng lực khai thác tàu container, không áp dụng cho tàu hàng rời.</div></div>
    <div class="term"><div class="t-abbr">CII</div><div class="t-full">Carbon Intensity Indicator</div><div class="t-gist">Chỉ số cường độ carbon theo IMO, xếp hạng A-E theo từng tàu mỗi năm; hạng D/E liên tiếp buộc phải có kế hoạch khắc phục.</div></div>
  </div>
```
