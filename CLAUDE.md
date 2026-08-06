# HT-viz-rendering

**Đọc `memory.md` trước tiên.** Nó nói đang ở đâu và làm gì tiếp.

Repo sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF in được.

## Luật cứng, không có ngoại lệ

- Shadow chỉ dùng offset cứng, blur phải bằng 0
- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải viết `@media screen and (max-width: ...)`
- Cấm gauge và radar
- Đếm ảnh raster trong PDF bằng `doc.xref_object`, không dùng `get_images`
- Khai `font-family` phải là list kết thúc bằng generic keyword, không dùng một tên trần
- Không em-dash và en-dash trong mọi nội dung hiển thị
- Mọi script verify phải trả exit code, 0 là PASS

## Khi sửa token

Sửa `design-system/tokens.css` trước, rồi `design-system/tokens.py` cho khớp. Test `tests/consistency/tokens_test.py` bắt nếu quên một bên.

## Khi thêm component

Thêm khối vào gallery và style vào CSS, rồi viết spec trong `components/catalog/` nói rõ trả lời câu hỏi gì, đầu vào gì, và **khi nào KHÔNG nên dùng**. Chạy `node --test tests/consistency/catalog_drift.test.mjs`.

## Khi thêm chart

Màu lấy từ `charts/echarts/theme.mjs`, không hardcode hex. Script chart phải kết bằng `chart.dispose(); process.exit(0);` vì ECharts SSR không tự thoát process.

## Khi thêm minh hoạ

Đọc `illustrations/grammar.md` trước. Ba bài tự kiểm bắt buộc: che hết chữ mà không đọc ra biến cấu trúc thì xoá, không polish; đổi ngành mà hình vẫn dùng nguyên được thì đó là trang trí chứ không phải phân tích; kiểm danh sách đen chart giả.

## Không bao giờ

- Sửa CSS cho khớp catalog. Sửa catalog cho khớp CSS, vì CSS là thứ đang chạy và đã verify
- Tin một package là tự đủ chỉ vì nó chạy được ở thư mục gốc của nó
- Kết luận "đã kiểm an toàn" từ một phép đo mà kết quả không thể sai
