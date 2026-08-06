# Mục lục báo cáo kèm trạng thái từng phần

`KHỐI 18 · MỤC LỤC CÓ MỐC`

## Mô tả / khi nào dùng

Trả lời: "Báo cáo có bao nhiêu phần, phần nào đã xong/đang mở/còn chờ dữ liệu?" Khác mục lục thường ở cột trạng thái bên phải. KHÔNG dùng nhãn trạng thái mơ hồ ("đang xử lý"); phải là trạng thái có thể kiểm chứng.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<ol class="toc-milestone">
    <li data-status="done"><span class="toc-title">Tổng quan đội tàu &amp; tài chính<small>Đối chiếu BCTC kiểm toán FY2025</small></span><span class="toc-mark">XONG</span></li>
    <li data-status="done"><span class="toc-title">Khung pháp lý &amp; công ước quốc tế<small>MARPOL, SOLAS, IMO CII, đăng kiểm</small></span><span class="toc-mark">XONG</span></li>
    <li data-status="live"><span class="toc-title">Rủi ro nhiên liệu &amp; phòng vệ giá<small>Cập nhật theo giá VLSFO tuần</small></span><span class="toc-mark">ĐANG MỞ</span></li>
    <li data-status="live"><span class="toc-title">Lộ trình đầu tư đội tàu 3 giai đoạn<small>Chờ chốt lãi suất vay đợt 2</small></span><span class="toc-mark">ĐANG MỞ</span></li>
    <li data-status="cho"><span class="toc-title">Kịch bản khử carbon 2030<small>Chờ số liệu thử nghiệm nhiên liệu thay thế</small></span><span class="toc-mark">CHỜ DỮ LIỆU</span></li>
    <li data-status="cho"><span class="toc-title">Phụ lục nguồn &amp; phương pháp<small>Tổng hợp toàn bộ badge nguồn trong báo cáo</small></span><span class="toc-mark">CHỜ DỮ LIỆU</span></li>
  </ol>
```
