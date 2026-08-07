# Định vị 4 mảng khai thác theo biên lợi nhuận và tăng trưởng nhu cầu

`KHỐI 06 · MA TRẬN 2×2 ĐỊNH VỊ`

## Mô tả / khi nào dùng

Trả lời: "Trong danh mục, cái gì nên rót thêm vốn, cái gì nên thu hẹp?" Đầu vào: 2 trục liên tục + danh sách điểm {tên, x, y}. KHÔNG dùng khi có >8 điểm (chồng nhãn) hoặc khi trục không thể định lượng khách quan; khi đó dùng ma trận nhiệt dạng bảng thay thế.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<!-- Bảng dữ liệu thật cho screen reader, ẩn kiểu sr-only, đứng trước bản
       trực quan (đánh dấu aria-hidden bên dưới) để AT không phải suy luận vị
       trí điểm chấm từ toạ độ CSS (--x/--y chỉ có ý nghĩa thị giác). -->
  <!-- Class sr-only phải nằm trên DIV BỌC NGOÀI. Đặt thẳng lên <table> thì
       WeasyPrint vẫn in bảng ra và nó đè lên chính ma trận bên dưới. -->
  <div class="visually-hidden">
  <table>
    <caption>Ma trận định vị 4 mảng khai thác theo biên lợi nhuận và tăng trưởng nhu cầu</caption>
    <thead><tr><th scope="col">Mảng khai thác</th><th scope="col">Biên lợi nhuận</th><th scope="col">Tăng trưởng nhu cầu</th><th scope="col">Nhóm chiến lược</th></tr></thead>
    <tbody>
      <tr><td>Hàng rời nội địa</td><td>Cao</td><td>Thấp</td><td>Giữ &amp; tối ưu</td></tr>
      <tr><td>Feeder quốc tế</td><td>Cao</td><td>Cao</td><td>Ưu tiên rót vốn</td></tr>
      <tr><td>Tàu dầu sản phẩm</td><td>Trung bình</td><td>Trung bình</td><td>Theo dõi, chưa mở rộng</td></tr>
      <tr><td>Đại lý &amp; giao nhận</td><td>Thấp</td><td>Thấp</td><td>Cân nhắc thoái</td></tr>
    </tbody>
  </table>
  </div>
  <div class="quad2x2" aria-hidden="true">
    <div class="q-ylabel">Biên lợi nhuận →</div>
    <div class="q-grid">
      <div class="q-cell"><div class="q-cell-title">Giữ &amp; tối ưu</div></div>
      <div class="q-cell"><div class="q-cell-title">Ưu tiên rót vốn</div></div>
      <div class="q-cell"><div class="q-cell-title">Cân nhắc thoái</div></div>
      <div class="q-cell"><div class="q-cell-title">Theo dõi, chưa mở rộng</div></div>
      <div class="q-plot">
        <div class="q-dot-wrap" style="--x:26%;--y:22%;"><span class="q-dot"></span><span class="q-dot-label">Hàng rời nội địa</span></div>
        <div class="q-dot-wrap" style="--x:74%;--y:20%;"><span class="q-dot"></span><span class="q-dot-label">Feeder quốc tế</span></div>
        <div class="q-dot-wrap" style="--x:60%;--y:62%;"><span class="q-dot"></span><span class="q-dot-label">Tàu dầu sản phẩm</span></div>
        <div class="q-dot-wrap" style="--x:22%;--y:80%;"><span class="q-dot"></span><span class="q-dot-label">Đại lý &amp; giao nhận</span></div>
      </div>
    </div>
    <div class="q-xlabel">Tăng trưởng nhu cầu →</div>
  </div>
```
