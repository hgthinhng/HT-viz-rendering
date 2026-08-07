# HT-viz-rendering

**Đọc `memory.md` trước tiên.** Nó nói đang ở đâu và làm gì tiếp.

Repo sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF in được.

Cổng vào cho Claude là `SKILL.md`, chỉ định tuyến, không nhồi nội dung. File này (`CLAUDE.md`) là quy ước làm việc chi tiết cho người sửa code trong repo.

## Ràng buộc cứng và ý tham khảo, phân biệt rõ

- **Ràng buộc cứng**: mục dưới đây. Vi phạm là hỏng file giao đi vì đây là kết quả ĐO ĐƯỢC, không phải sở thích. Không thương lượng.
- **Ý tham khảo**: component, preset trong `components/`, `charts/`, `illustrations/`, và tài liệu trong `research/`, `samples/` là THƯ VIỆN ĐỂ LẤY Ý, không phải khuôn ép. Thiết kế có tự do sáng tạo, miễn hợp lý: không bắt buộc dùng hết, không bắt buộc dùng đúng nguyên bản. Bố cục, nhịp, tỷ lệ, cách vào bài viết dạng gợi ý, không viết dạng mệnh lệnh.

## Luật cứng, không có ngoại lệ

- Shadow chỉ dùng offset cứng, blur phải bằng 0
- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải viết `@media screen and (max-width: ...)`
- Cấm gauge và radar
- Đếm ảnh raster trong PDF bằng `doc.xref_object`, không dùng `get_images`
- Khai `font-family` phải là list kết thúc bằng generic keyword, không dùng một tên trần
- Không em-dash và en-dash trong mọi nội dung hiển thị
- Mọi script verify phải trả exit code, 0 là PASS
- File giao khách phải khoá sáng: `<html lang="vi" data-theme="light">`
- Font phải nhúng trong file, không trỏ tới đường dẫn tuyệt đối trên máy nào cả
- Mọi chỗ mở Chromium phải đi qua `scripts/lib/chromium.mjs`

## `npm test` chỉ quét đúng khi có dấu ngoặc kép trong package.json

Script test là `node --test "tests/**/*.test.mjs"`. npm chạy script qua `sh`, và dấu ngoặc kép quanh glob là bắt buộc để `sh` giao nguyên chuỗi cho Node tự xử lý đệ quy. Bỏ ngoặc thì `sh` tự rút gọn `**` thành `*`, và test đặt ở cấp một hoặc cấp ba thư mục bị loại IM LẶNG, exit code vẫn 0. Đã tái hiện thật: không quote bắt 1 trên 3 file test, có quote bắt đủ 3. Đặt file test mới trong `tests/smoke/` hoặc `tests/consistency/` (đúng hai cấp), và đừng bao giờ bỏ dấu ngoặc kép trong script `test` của `package.json`.

## Ranh giới em-dash

Cấm `—` và `–` trong mọi thứ HIỂN THỊ: nội dung HTML, nhãn và tiêu đề chart, `<title>` và `<desc>` của SVG (desc là text trình đọc màn hình đọc lên nên nó có hiển thị), file `.md` trong `components/catalog/`, và mọi chuỗi đi ra `console.log` hoặc `print`. Được phép giữ trong comment mã nguồn và docstring Python, vì đó không phải nội dung giao cho người đọc báo cáo. Đã lọt lưới bốn lần trong Phase 1, gồm một lần ra tận ảnh render.

## `design-system/tokens.css` có hai khối `:root`, đó là chủ ý

Khối đầu giữ 12 biến màu và `--shadow-2/3/none`. Khối sau giữ font, thang chữ, `--space-*`, `--radius-*`, `--shadow-1`, `--shadow-hairline`. Không biến nào được khai ở cả hai khối, có test ép điều đó. Lý do phải có test: hai khối `:root` cùng specificity thì khối SAU thắng trong cascade, nên khai trùng sẽ làm giá trị render khác giá trị đang ghi trong `tokens.py` mà không ai biết. Đã xảy ra thật với `--space-6`.

## Cú pháp shadow dùng `rgba(R G B / A)`, không dùng dấu phẩy trong ngoặc

Test tách các lớp shadow bằng `split(",")`. Dấu phẩy bên trong `rgba()` (cú pháp cũ `rgba(R, G, B, A)`) làm hỏng phép tách đó. Giữ nguyên trị số, chỉ đổi cách viết sang cú pháp khoảng trắng và dấu gạch chéo.

## Ba thuộc tính CSS mà WeasyPrint bỏ qua, đều đã cắn thật

Cả ba cùng một lớp lỗi: trình duyệt chạy đúng nên bản HTML đẹp, engine đích bỏ qua nên bản PDF
hỏng, và không ai biết cho tới lúc mở file PDF ra nhìn.

| Thuộc tính | WeasyPrint làm gì | Dùng gì thay |
|---|---|---|
| `aspect-ratio` | Bỏ qua, khối ra cao 0 | Khai `height` bằng px |
| `overflow`/`clip` trên `<table>` | Bỏ qua, bảng vẫn in ra | Bọc bảng trong `<div class="visually-hidden">` |
| `writing-mode` | Bỏ qua nhưng VẪN áp `transform` | Quay bằng transform thuần |

Chi tiết nếu cần đào lại: khối ma trận 2x2 dính cả ba cùng lúc. `aspect-ratio: 1 / 0.72` làm
khung sập thành một đường kẻ, `<table class="visually-hidden">` in đè lên chính khối đó, và
`writing-mode: vertical-rl` cộng `rotate(180deg)` biến nhãn trục Y thành chữ ngang lật ngược
đọc thành "← N ẠỤHN IỢL NÊIB".

Có hai test chặn tái phạm trong `tests/consistency/catalog_drift.test.mjs`, cả hai đã được kiểm
là đỏ được khi tái tạo lỗi.

## Hệ màu tối: giữ cho trang nội bộ, khoá sáng cho file giao đi

Repo có bảng màu tối (`[data-theme="dark"]` và `@media (prefers-color-scheme: dark)` trong
`tokens.css` lẫn `components.css`). Nó được GIỮ, dùng cho `gallery.html` và các trang thử
nghiệm mở trên màn hình.

File giao khách thì khác: phải khai `<html lang="vi" data-theme="light">`. Mọi rule tối đều
viết `:root:not([data-theme="light"])`, nên đúng một thuộc tính đó là khoá xong.

Lý do là thứ đo được, không phải khẩu vị. Chart matplotlib và minh hoạ SVG hiện chỉ có bảng
màu sáng, nên máy khách đặt theme tối sẽ cho trang nền `#0A1420` mà chart vẫn nền trắng, lệch
hẳn. Khoá sáng cũng làm bản HTML trùng bản PDF, vì WeasyPrint vốn vứt cả khối
`@media (prefers-color-scheme)`.

Nếu sau này muốn mở dark mode cho cả file giao đi thì Phase 2 phải gánh thêm bảng màu tối đầy
đủ cho ECharts, matplotlib EIR và minh hoạ SVG, cộng gate kiểm cả hai chế độ.

Gate `khoa-sang-khong-doi-theo-may-khach` trong `verify-components.mjs` đo bằng cách mở trang
ở hai context màu rồi so nền và màu chữ. Trang không khai thì nó SKIP kèm cảnh báo chứ không
xanh giả.

## Khi sửa token

Sửa `design-system/tokens.css` trước, rồi sửa `design-system/tokens.py` cho khớp. Test `tests/consistency/tokens_test.py` sẽ bắt nếu quên một bên.

## Khi thêm component

1. Thêm khối vào `components/gallery.html` và style vào CSS
2. Viết spec trong `components/catalog/` nói rõ trả lời câu hỏi gì, đầu vào gì, và **khi nào KHÔNG nên dùng**
3. Chạy `node --test tests/consistency/catalog_drift.test.mjs`. Test này ép mọi class trong ví dụ phải tồn tại thật trong CSS
4. Chạy `npm run verify:components`

## Khi thêm chart

Màu lấy từ `charts/echarts/theme.mjs`, không hardcode hex. Mọi script chart phải kết bằng `chart.dispose(); process.exit(0);` vì ECharts SSR không tự thoát process.

Chart matplotlib lấy font từ `design-system/fonts/ttf/`, đã nhúng trong repo, không mượn font hệ thống. Đừng thêm đường dẫn `/usr/share/fonts` mới vào `_eir_style.py`: nhánh hệ thống còn lại chỉ là dự phòng cuối. Sinh lại file `.ttf` bằng `python3 design-system/fonts/extract-ttf.py` sau khi `build-fonts.py` chạy lại.

Phải có bản `.ttf` riêng dù repo đã nhúng font base64, vì matplotlib đọc ttf/otf/ttc chứ không đọc woff2, mà `fonts-embedded.css` toàn woff2. Trích ngược từ chính file CSS đó chứ không tải mới từ Google Fonts, để chạy được offline và để bản chart với bản HTML không thể lệch font.

Một cái bẫy đã cắn khi làm việc này: Google Fonts đặt tên họ của bản 600 là `IBM Plex Sans SemiBold`, tức một HỌ KHÁC chứ không phải cấp đậm của `IBM Plex Sans`. Trích nguyên xi thì matplotlib đăng ký hai họ rời rạc, và khi chart xin bản đậm nó không tìm thấy nên tô giả. `extract-ttf.py` ép lại `nameID` 1/16 cho khớp. Kiểm bằng `findfont` chứ đừng tin danh sách tên mà `setup_fonts()` trả về.

## Khi thêm minh hoạ

Đọc `illustrations/grammar.md` trước. Ba bài tự kiểm bắt buộc: che hết chữ mà không đọc ra biến cấu trúc thì xoá, không polish; đổi ngành mà hình vẫn dùng nguyên được thì đó là trang trí chứ không phải phân tích; kiểm danh sách đen chart giả.

## Không bao giờ

- Sửa CSS cho khớp catalog. Sửa catalog cho khớp CSS, vì CSS là thứ đang chạy và đã verify
- Dùng `get_images()` để đếm ảnh trong PDF
- Tin một package là tự đủ chỉ vì nó chạy được ở thư mục gốc của nó
- Kết luận "đã kiểm an toàn" từ một phép đo mà kết quả không thể sai
