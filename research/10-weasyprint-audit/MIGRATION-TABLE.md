# Bảng chuyển đổi: chỗ cần sửa khi khoá WeasyPrint làm engine PDF

Sắp theo HẬU QUẢ giảm dần, không theo tên file. Chi tiết đo đạc từng dòng ở `FINDINGS.md`.

Tổng số chỗ khai `box-shadow` tìm được trong 4 thư mục mục tiêu: **3** (không phải 2 - đếm đủ cả
`illustrations/annotate.css:14`, thuộc lớp minh hoạ, dễ bị đếm sót nếu chỉ nghĩ "minh hoạ = file
`.svg`). Trong 3 chỗ đó: **2 chỗ cần hành động thật** (M1, M2 - cả hai trong
`components/components.css`) + **1 chỗ không cần hành động** (`illustrations/annotate.css:14`,
xem bảng cuối file - screen-only, tự khai `display:none` khi in nên chưa từng định render trong
PDF). Cộng thêm, NGOÀI phạm vi 3 chỗ box-shadow này: **1 chỗ ngoài phạm vi 4 thư mục đã ĐÓNG bởi
vòng khác trong lúc audit này đang chạy** (giữ lại để đủ sổ sách) + **1 dòng dọn dẹp không liên
quan bẫy WeasyPrint** (4 token shadow chưa từng dùng).

## Mức 1: hỏng thật, cần sửa (nhưng cả hai đều nhẹ, không có mức "nghiêm trọng" nào trong 4 thư mục mục tiêu)

| # | Chỗ | Bẫy | Kỹ thuật thay thế đề xuất | Ưu tiên | Công ước lượng |
|---|---|---|---|---|---|
| M1 | `components/components.css:78`, `.sg-card` | `box-shadow: var(--shadow-1)` không vẽ gì trong WeasyPrint | **Xoá thẳng dòng `box-shadow: var(--shadow-1);`.** Border + nền hiện có đã phân tách đủ, đã xác nhận bằng so byte PDF (giống hệt có/không). Nếu MUỐN giữ cảm giác "nổi khối" đã mất, dùng kỹ thuật khối lệch vị trí ở `samples/audit-kpi-card.html` khối 3 (thêm 1 `<div>` nền ink 14% lệch `position:absolute` phía sau, `z-index:0`) - nhưng đây là lựa chọn thẩm mỹ, không phải bắt buộc để "không hỏng". | Thấp (đo được là vô hại nếu bỏ qua, nhưng rẻ để sửa nên nên làm luôn) | 1 dòng xoá, hoặc ~15 phút nếu chọn dựng lại bằng khối lệch vị trí (thêm 1 phần tử DOM x N thẻ) |
| M2 | `components/components.css:238`, `.quad2x2 .q-dot` | `box-shadow: 0 0 0 1px var(--ink)` không vẽ gì; vòng ink bao ngoài biến mất, chỉ còn vòng `border` màu paper | Thay bằng khối lệch vị trí NHỎ: một `::before` hoặc `<span>` phụ, kích thước lớn hơn dot 2px, nền `var(--ink)`, đặt `z-index: -1` phía sau dot hiện tại - tái tạo đúng hiệu ứng "vòng viền tối bao ngoài vòng trắng" bằng phần tử thật thay vì shadow. Xem kỹ thuật lớp phủ ở `samples/audit-strong-layering.html` khối 3 (cùng họ, khác tỷ lệ). | Trung bình (ảnh hưởng khả năng đọc marker ở vị trí biên ô, không phải thẩm mỹ thuần) | ~20 phút, cần thêm 1 phần tử con cho mỗi `.q-dot`, kiểm lại `z-index`/`overflow` của `.q-plot`/`.q-cell` không cắt phần tử mới |

## Mức 2: đã đóng trong lúc audit đang chạy, giữ lại để đủ sổ sách

| # | Chỗ | Bẫy | Trạng thái | Ưu tiên | Công ước lượng |
|---|---|---|---|---|---|
| M3 | `samples/report-exec-brief-action-first.html`, `h1.verdict` (thuộc vòng nghiên cứu 02, NGOÀI 4 thư mục được giao cho agent này) | `font-size: clamp(1.55rem, 1.1rem + 1.6vw, 2.15rem)` bị bỏ qua hoàn toàn, đo lúc phát hiện ra `12.0pt` - bằng cỡ chữ thân bài, mất hết phân cấp cho dòng kết luận hành động chính | **ĐÃ SỬA bởi commit `75e5ffb` trong lúc audit này đang chạy** - nay khai `font-size: 1.9rem` cố định cho in, `clamp()` gốc chuyển vào `@media screen { }` chỉ áp khi xem trên trình duyệt. Đo lại xác nhận: `22.8pt` cố định. Không còn việc phải làm. | Đã đóng | 0 (đã xong) |

## Mức 3: dọn dẹp, không liên quan trực tiếp bẫy WeasyPrint

| # | Chỗ | Vấn đề | Đề xuất | Ưu tiên | Công ước lượng |
|---|---|---|---|---|---|
| M4 | `design-system/tokens.css:70-72,185`, token `--shadow-2`, `--shadow-3`, `--shadow-hairline`, `--shadow-none` | 0 nơi tham chiếu qua `var()` trong `components/`, `charts/`, `design-system/`, `illustrations/` - code chết | Không bắt buộc xoá (có thể dành cho component tương lai), nhưng NẾU giữ, thêm một dòng comment cạnh mỗi token nhắc "box-shadow không render trong WeasyPrint 69.0, xem `research/10-weasyprint-audit/FINDINGS.md` trước khi dùng" để chặn lỗi tái diễn khi ai đó bắt đầu dùng chúng | Thấp | 5 phút (chỉ thêm comment) hoặc 0 phút (bỏ qua) |

## Không cần hành động, liệt kê để đủ sổ sách

| # | Chỗ | Vì sao không cần sửa |
|---|---|---|
| M0 | `illustrations/annotate.css:14`, `#annotate-drill-card` (box-shadow CÓ blur 40px) - **chỗ thứ 3 trong tổng 3 chỗ box-shadow của toàn bộ audit, thuộc lớp minh hoạ** | Chỉ hiện trên màn hình, tự khai `display:none` trong `@media print`, không bao giờ vào PDF |
| - | `illustrations/examples/example-vertical-axis-ship.html:14`, `#ship-svg { height:auto }` | Dạng CSS property, đã đo render ĐÚNG trong WeasyPrint (42 drawings, hình đầy đủ), KHÁC bẫy thuộc tính HTML `height="auto"` |
| - | `illustrations/examples/example-horizontal-axis-banner.html:14`, `#banner-svg { height:auto }` | Tương tự dòng trên, đã đo render ĐÚNG (25 drawings, hình đầy đủ) |
| - | `components/gallery.html:19`, `<h1>` demo dùng `clamp()` | Nằm trong `.no-print`, biến mất hoàn toàn khi in bằng WeasyPrint, đã xác nhận bằng render 16 trang không tìm thấy chuỗi text của H1 này ở đâu |
| - | Mọi SVG trong `charts/echarts/` (12 file) | `width`/`height` là số px cố định khớp `viewBox`, đúng mẫu an toàn |
| - | Mọi SVG trong `illustrations/svg/` (11 file) | Không khai `width`/`height` gì (chỉ `viewBox`), không rơi vào bẫy vì không có giá trị "auto" nào để bỏ qua |
| - | `filter: grayscale()` / mọi `filter` khác | 0 chỗ trong toàn bộ 4 thư mục, cả CSS lẫn cấu hình ECharts lẫn SVG xuất ra |
