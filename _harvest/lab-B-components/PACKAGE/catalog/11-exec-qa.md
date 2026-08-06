# Bốn câu hỏi Hội đồng Quản trị hỏi nhiều nhất

`KHỐI 11 · KHỐI CÂU HỎI-TRẢ LỜI ĐIỀU HÀNH`

## Mô tả / khi nào dùng

Trả lời: "Người đọc bận rộn muốn hỏi gì trước, và câu trả lời ngắn nhất có thể là gì?" Đầu vào: câu hỏi ở giọng người đọc (không phải giọng tác giả), câu trả lời ≤3 câu. KHÔNG dùng quá 4-6 cặp hỏi-đáp mỗi trang; quá nhiều sẽ giống FAQ marketing hơn là tóm tắt điều hành.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="exec-qa-grid">
    <div class="exec-qa"><div class="qa-q">Tại sao biên EBITDA giảm dù doanh thu tăng?</div><div class="qa-a">Doanh thu tăng nhờ giá cước, nhưng chi phí nhiên liệu tăng nhanh hơn tốc độ tăng cước, khiến biên gộp khai thác co lại dù đội tàu chạy gần hết công suất.</div></div>
    <div class="exec-qa"><div class="qa-q">Đội tàu có bắt buộc phải thay mới ngay không?</div><div class="qa-a">Chưa bắt buộc theo tuổi tàu, nhưng 6 tàu &gt;20 năm sẽ khó đạt CII hạng C trở lên sau 2027, buộc phải lắp thiết bị hoặc thanh lý.</div></div>
    <div class="exec-qa"><div class="qa-q">Rủi ro Biển Đỏ ảnh hưởng thế nào đến tuyến chính?</div><div class="qa-a">Tuyến nội Á chịu ảnh hưởng gián tiếp qua giá nhiên liệu và bảo hiểm chiến tranh, không đi qua eo Bab-el-Mandeb nên rủi ro trực tiếp thấp.</div></div>
    <div class="exec-qa"><div class="qa-q">Có kế hoạch tăng vốn trong 12 tháng tới không?</div><div class="qa-a">Đang đánh giá phát hành trái phiếu xanh cho đợt đóng tàu thứ hai; chưa có kế hoạch phát hành cổ phần mới.</div></div>
  </div>
```
