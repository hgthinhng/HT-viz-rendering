# Ma trận khả thi: mảng kinh doanh × điều kiện pháp lý

`KHỐI 05 · MA TRẬN NHIỆT DẠNG BẢNG`

## Mô tả / khi nào dùng

Trả lời: "Trong N mảng kinh doanh, mảng nào mở ngay, mảng nào có điều kiện, mảng nào đóng?" Đầu vào: hàng × cột với trạng thái {mở/có điều kiện/đóng} + ghi chú ngắn. Dùng bảng HTML thật (không canvas) để screen reader đọc được từng ô. Điểm yếu chính của bản Kimi tham chiếu là ma trận tương tự dựng bằng SVG không có text thay thế. KHÔNG dùng khi chỉ có 2 trạng thái nhị phân (dùng bảng so sánh phương án).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="table-wrap">
  <table class="heatmatrix">
    <caption class="visually-hidden">Ma trận khả thi theo mảng kinh doanh và điều kiện pháp lý, ô màu xanh là mở, ô gạch chéo là có điều kiện, ô xám là đóng</caption>
    <thead><tr><th scope="col">Mảng kinh doanh</th><th scope="col">Vốn tối thiểu</th><th scope="col">Thời gian cấp phép</th><th scope="col">Rào cản chính</th></tr></thead>
    <tbody>
      <tr class="c-open"><td><span class="cell-tag">MỞ</span>Vận tải hàng rời nội địa</td><td>Không yêu cầu riêng</td><td>0 tháng (đang khai thác)</td><td>Cạnh tranh cước giao ngay</td></tr>
      <tr class="c-open"><td><span class="cell-tag">MỞ</span>Đại lý tàu biển &amp; giao nhận</td><td>Vốn pháp định ~5 tỷ VND</td><td>1–2 tháng</td><td>Biên phí thấp, cần quy mô</td></tr>
      <tr class="c-cond"><td><span class="cell-tag">CÓ ĐIỀU KIỆN</span>Vận tải container feeder quốc tế</td><td>Đội tàu treo cờ VN ≥30%</td><td>3–6 tháng đăng ký tuyến</td><td>Hạn ngạch cảng, đàm phán slot</td></tr>
      <tr class="c-cond"><td><span class="cell-tag">CÓ ĐIỀU KIỆN</span>Kho ngoại quan &amp; logistics tích hợp</td><td>Vốn pháp định ~10 tỷ VND</td><td>4–8 tháng</td><td>Quy hoạch đất cảng hạn chế</td></tr>
      <tr class="c-closed"><td><span class="cell-tag">ĐÓNG (giai đoạn này)</span>Vận hành cảng nước sâu tự doanh</td><td>Vốn &gt;500 tỷ VND</td><td>18–24 tháng quy hoạch</td><td>Cần đối tác chiến lược nước ngoài</td></tr>
      <tr class="c-closed"><td><span class="cell-tag">ĐÓNG (giai đoạn này)</span>Vận tải dầu thô đường dài</td><td>Chuẩn tàu chở dầu OCIMF/TMSA</td><td>&gt;24 tháng đạt chuẩn</td><td>Yêu cầu vốn &amp; tiêu chuẩn quốc tế cao</td></tr>
    </tbody>
  </table>
  </div>
```
