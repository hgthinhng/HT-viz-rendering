---
name: HT-viz-rendering
description: Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản, xuất HTML self-contained và PDF in được. Có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG neo được số liệu vào từng bộ phận vật thể. Dùng khi cần làm báo cáo ngành, báo cáo cổ phiếu, bản tin thị trường, hoặc deal pack.
---

# HT-viz-rendering

File này chỉ ĐỊNH TUYẾN. Đọc phần liên quan tới việc đang làm, đừng đọc hết.

## Tầng doctrine (tư duy thiết kế)

Chưa có ở Phase 1. Bảy file tầng doctrine (đọc trước khi vẽ, chọn kịch bản kể chuyện, gắn nguồn,
chọn chart, viết chữ, vẽ minh hoạ, quyết định khó) sẽ tới ở Phase 3. Cho tới lúc đó, dùng mục
"Ý tham khảo" bên dưới và `CLAUDE.md` làm kim chỉ nam.

## Ràng buộc cứng, không có ngoại lệ

Đây là kết quả ĐO ĐƯỢC, vi phạm là hỏng file giao đi. Chi tiết và lý do ở `CLAUDE.md`.

- Shadow chỉ dùng offset cứng, blur phải bằng 0
- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải có `screen`
- Cấm gauge và radar
- Đếm ảnh raster bằng `doc.xref_object`, không dùng `get_images`
- Không em-dash và en-dash trong mọi nội dung hiển thị
- `font-family` phải là list kết thúc generic keyword, không dùng một tên trần
- `design-system/tokens.css` có hai khối `:root`, không khai một biến ở cả hai khối
- Shadow viết `rgba(R G B / A)`, không dùng dấu phẩy trong ngoặc màu

## Theo thành phần

| Cần | Ở đâu |
|---|---|
| Màu, font, spacing, shadow | `design-system/tokens.css` |
| Component kể chuyện | `components/catalog/` rồi `components/gallery.html` |
| Chart tĩnh cho PDF | `charts/matplotlib/` |
| Chart tương tác cho HTML | `charts/echarts/` |
| Minh hoạ ngành | `illustrations/svg/` và `illustrations/grammar.md` |

## Ý tham khảo, không phải khuôn ép

Component, preset, và minh hoạ trong repo là THƯ VIỆN THAM KHẢO ĐỂ LẤY Ý, không bắt buộc dùng
hết hay dùng đúng nguyên bản. Thiết kế có tự do sáng tạo, miễn hợp lý.

- Bố cục, nhịp, cách vào bài: xem thư mục `research/` để lấy hướng, đừng chép nguyên.
- Ví dụ báo cáo tham chiếu: xem thư mục `samples/`.
- Ngữ pháp vẽ minh hoạ ngành: `illustrations/grammar.md`.

## Trước khi giao file

Chạy `npm run verify`. FAIL là không được giao. Quy ước làm việc chi tiết ở `CLAUDE.md`.
