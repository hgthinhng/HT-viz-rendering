# Trích dẫn quy định, có mã hiệu lực

`KHỐI 08 · TRÍCH DẪN VĂN BẢN PHÁP LÝ`

## Mô tả / khi nào dùng

Trả lời: "Điều khoản nào đang chi phối quyết định này, còn hiệu lực không?" Khác pull-quote ở chỗ bắt buộc có mã văn bản + trạng thái hiệu lực. Đầu vào: mã văn bản, cơ quan ban hành, trạng thái, nội dung trích, ngày hiệu lực. KHÔNG dùng cho phát biểu cá nhân (dùng pull-quote) hoặc khi chưa xác minh văn bản còn hiệu lực.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="legal-quote">
    <div class="lq-code"><span>MARPOL ANNEX VI · REGULATION 14</span><span class="lq-status hieu-luc">ĐANG HIỆU LỰC</span></div>
    <blockquote>"Hàm lượng lưu huỳnh trong nhiên liệu sử dụng trên tàu không được vượt quá 0,50% m/m, áp dụng trên toàn cầu kể từ ngày 1/1/2020, trừ khu vực kiểm soát khí thải (ECA) áp dụng giới hạn 0,10% m/m."</blockquote>
    <div class="lq-cite">Tổ chức Hàng hải Quốc tế (IMO) · sửa đổi gần nhất theo MEPC.320(74) · tra cứu 2026-06-01</div>
  </div>
  <div class="legal-quote">
    <div class="lq-code"><span>NGHỊ ĐỊNH 171/2024/NĐ-CP · ĐĂNG KIỂM TÀU BIỂN</span><span class="lq-status sap-doi">SẮP SỬA ĐỔI</span></div>
    <blockquote>"Tàu biển mang cấp VR-SB khai thác tuyến ven biển phải thực hiện kiểm định định kỳ 30 tháng một lần, thay vì chu kỳ 24 tháng theo quy định cũ."</blockquote>
    <div class="lq-cite">Chính phủ nước CHXHCN Việt Nam · hiệu lực 2024-07-01 · dự thảo sửa đổi đang lấy ý kiến 2026-Q3</div>
  </div>
```
