# Cách tính EBITDA chuẩn hóa theo chu kỳ cước

`KHỐI 17 · HỘP PHƯƠNG PHÁP LUẬN`

## Mô tả / khi nào dùng

Trả lời: "Con số này được tính ra như thế nào, để người đọc có thể tự kiểm tra hoặc phản biện?" Đầu vào: chuỗi bước có đánh số, mỗi bước là 1 câu ngắn + giải thích. KHÔNG dùng để che giấu một phương pháp luận yếu; nếu bước nào chủ quan, phải nói rõ là ước tính. KHÔNG dùng khi chuỗi bước dài quá 5-6 bước: `.method-box { break-inside: avoid; }` áp cho TOÀN khối chứ không phải từng `li`, nên một method-box nhiều bước sẽ bị đẩy nguyên khối sang trang sau khi in, để lại khoảng trắng lớn ở cuối trang trước; lúc đó tách thành process-step-chain (khối 16, mỗi bước ngắt trang độc lập được) sẽ an toàn hơn.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="method-box">
    <div class="mb-title">PHƯƠNG PHÁP · 4 BƯỚC</div>
    <ol>
      <li><b>Lấy EBITDA báo cáo theo quý</b><span>Từ BCTC soát xét, không điều chỉnh.</span></li>
      <li><b>Loại trừ khoản mục một lần</b><span>Thanh lý tàu, hoàn nhập dự phòng, chênh lệch tỷ giá chưa thực hiện.</span></li>
      <li><b>Chuẩn hóa theo giá nhiên liệu bình quân chu kỳ 3 năm</b><span>Thay giá nhiên liệu thực tế trong quý bằng bình quân trượt 3 năm, giữ nguyên sản lượng tiêu thụ thực tế.</span></li>
      <li><b>Quy về biên EBITDA/doanh thu</b><span>Kết quả là ước tính, không phải số báo cáo, dùng để so sánh giữa các quý có chu kỳ giá nhiên liệu khác nhau.</span></li>
    </ol>
  </div>
```
