# Cơ cấu đội tàu theo loại

`KHỐI 12 · BẢNG SỐ LIỆU HAIRLINE`

## Mô tả / khi nào dùng

Trả lời: "So sánh trực tiếp N hạng mục theo nhiều chỉ tiêu cùng lúc." Bắt buộc tabular-nums cho mọi cột số, thead dùng display:table-header-group để lặp lại header mỗi trang khi in (KHÔNG dùng position:sticky: sticky vô hiệu khi in). KHÔNG dùng khi <3 hàng (câu văn xuôi rõ hơn) hoặc >12 hàng (cần phân trang/lọc).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="table-wrap">
  <table class="dt">
    <thead><tr><th scope="col">Loại tàu</th><th scope="col">Số lượng</th><th scope="col">Tổng DWT</th><th scope="col">Tuổi TB</th><th scope="col">Hiệu suất khai thác</th></tr></thead>
    <tbody>
      <tr><td>Tàu hàng rời (bulk carrier)</td><td class="num">11</td><td class="num">338.200</td><td class="num">13,1 năm</td><td class="num">91,4%</td></tr>
      <tr class="hl"><td>Container feeder</td><td class="num">6</td><td class="num">142.600</td><td class="num">10,8 năm</td><td class="num">95,2%</td></tr>
      <tr><td>Tàu dầu sản phẩm</td><td class="num">4</td><td class="num">98.400</td><td class="num">17,5 năm</td><td class="num">86,7%</td></tr>
      <tr><td>Tàu đa dụng (general cargo)</td><td class="num">2</td><td class="num">33.200</td><td class="num">22,0 năm</td><td class="num">78,3%</td></tr>
      <tr><td style="font-weight:700;">Tổng / bình quân</td><td class="num" style="font-weight:700;">23</td><td class="num" style="font-weight:700;">612.400</td><td class="num" style="font-weight:700;">14,2 năm</td><td class="num" style="font-weight:700;">90,1%</td></tr>
    </tbody>
  </table>
  </div>
```
