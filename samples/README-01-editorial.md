# Mẫu editorial (research/01-editorial)

Năm file dưới đây minh hoạ các thủ pháp thiết kế editorial trong `research/01-editorial/FINDINGS.md`.
Mỗi file tự chứa (mở bằng trình duyệt là chạy ngay), có khối comment mở đầu nói rõ lấy cảm hứng
từ đâu và khi nào KHÔNG nên dùng. Số liệu công ty "CTCP Nông sản Cửu Long" / mã "CLF*" xuyên suốt
cả 5 file là HƯ CẤU, dùng chung một mạch nội dung để đọc liền mạch như một báo cáo giả định.

| File | Minh hoạ ý gì |
|---|---|
| `editorial-mo-dau-kicker-dek.html` | Trang mở đầu khác trang thân bài (lưới 1 cột và 2 cột), bộ khung kicker/headline/dek/nut-graf |
| `editorial-tufte-sidenote-margin.html` | Sidenote kiểu Tufte thay footnote, drop cap, pull-quote không rẻ tiền, neo số bằng màu tiết chế |
| `editorial-luoi-modular-spiegel.html` | Lưới module 12 cột co giãn theo nội dung, quy tắc tràn lề/thu cột, wall small multiples, trang ngăn phần |
| `editorial-chu-thich-nguon-rest-of-world.html` | Chú thích/tín dụng nguồn kiểu mono, đánh số hình/bảng, mô-típ tham chiếu chéo tự thiết kế, tabular figures |
| `editorial-nhip-tuong-phan-mat-do.html` | Nhịp mật độ biến thiên có chủ đích (thoáng/dồn dập/thoáng), kỷ luật phá thang chữ tối đa 1 lần/trang |

## Kiểm chứng thật, không phải khẳng định suông

Cả 5 file đã được render qua **WeasyPrint 69.0** (engine PDF thật của repo, xem `memory.md`)
bằng lệnh `weasyprint samples/<file>.html <output>.pdf`, sau đó kiểm bằng
`python3 scripts/count_raster.py <output>.pdf --max 0`.

| File | Ảnh raster | Kích thước trang | Số trang |
|---|---|---|---|
| editorial-mo-dau-kicker-dek | 0 | 210,0 x 297,0 mm (A4 đúng chuẩn) | 2 |
| editorial-tufte-sidenote-margin | 0 | 210,0 x 297,0 mm | 2 |
| editorial-luoi-modular-spiegel | 0 | 210,0 x 297,0 mm | 2 |
| editorial-chu-thich-nguon-rest-of-world | 0 | 210,0 x 297,0 mm | 2 |
| editorial-nhip-tuong-phan-mat-do | 0 | 210,0 x 297,0 mm | 2 |

Trong lúc render thật, phát hiện ba giới hạn CSS của WeasyPrint 69.0 không liên quan gì đến nội
dung thiết kế nhưng ảnh hưởng đến cách viết CSS cho đúng pipeline này: `box-shadow` không được
hỗ trợ dưới bất kỳ hình thức nào (kể cả blur = 0), cú pháp media query CSS3/4 dạng
`@media screen and (max-width: ...)` không được phân tích cú pháp (dù đúng theo ràng buộc cứng
của repo cho trình duyệt thật), và các hàm toán học CSS (`clamp()`/`min()`/`max()`) bị bỏ qua âm
thầm. Chi tiết đầy đủ, gồm cách tái hiện và ý nghĩa cho hệ thống component hiện tại, xem mục "0.
Bốn phát hiện kỹ thuật" ở đầu `research/01-editorial/FINDINGS.md`.

Cả 5 file đều đã tuân theo đúng cách viết an toàn (không dùng hàm toán học cho font-size, box-shadow
chỉ dùng trang trí cho bản xem màn hình và tắt hẳn ở `@media print`, media query màn hình vẫn viết
đúng chuẩn `screen and` vì đó là hành vi ĐÚNG khi ai đó mở file bằng trình duyệt thật).

**Cảnh báo font nhận từ controller, đã đối chiếu và xác nhận KHÔNG dính**: `design-system/fonts/fonts-embedded.css`
đang có bug làm lộn glyph tiếng Việt trong WeasyPrint (`nghệ` ra `nght`) do hai khối `@font-face`
trùng family/weight chỉ khác `unicode-range`, trong khi trình duyệt hiển thị bình thường nên dễ
lọt qua nếu chỉ nghiệm thu bằng mắt trên trình duyệt. Cả 5 file ở đây KHÔNG nạp file đó và không
tự khai `@font-face` nào, chỉ dùng font-family stack có fallback thật từ `tokens.css`. Đã xác
nhận lại bằng cách trích tầng text thật của cả 5 PDF (không đọc bằng mắt): các từ có dấu phức
tạp (`liệu`, `nguyên`, `xuất`, `khẩu`, `giữa`, `biến`, `chuyển`) đều ra nguyên vẹn. Chi tiết đầy
đủ xem mục 0.4 `research/01-editorial/FINDINGS.md`.
