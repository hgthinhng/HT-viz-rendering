# Mẫu editorial (research/01-editorial)

Năm file dưới đây minh hoạ các thủ pháp thiết kế editorial trong `research/01-editorial/FINDINGS.md`.
Mỗi file tự chứa (mở bằng trình duyệt là chạy ngay), có khối comment mở đầu nói rõ lấy cảm hứng
từ đâu và khi nào KHÔNG nên dùng. Số liệu công ty "CTCP Nông sản Cửu Long" / mã "CLF*" xuyên suốt
cả 5 file là HƯ CẤU, dùng chung một mạch nội dung để đọc liền mạch như một báo cáo giả định.

| File | Minh hoạ ý gì |
|---|---|
| `editorial-mo-dau-kicker-dek.html` | Trang mở đầu khác trang thân bài (lưới 1 cột và 2 cột), bộ khung kicker/headline/dek/nut-graf |
| `editorial-tufte-sidenote-margin.html` | Sidenote kiểu Tufte thay footnote, pull-quote không rẻ tiền, neo số bằng màu tiết chế (drop cap đã gỡ, xem dưới) |
| `editorial-luoi-modular-spiegel.html` | Lưới module 12 cột co giãn theo nội dung, quy tắc tràn lề/thu cột, wall small multiples, trang ngăn phần |
| `editorial-chu-thich-nguon-rest-of-world.html` | Chú thích/tín dụng nguồn kiểu mono, đánh số hình/bảng, mô-típ tham chiếu chéo tự thiết kế, tabular figures |
| `editorial-nhip-tuong-phan-mat-do.html` | Nhịp mật độ biến thiên có chủ đích (thoáng/dồn dập/thoáng), kỷ luật phá thang chữ tối đa 1 lần/trang |

## Kiểm chứng thật, không phải khẳng định suông

Cả 5 file đã được render qua **WeasyPrint 69.0** (engine PDF thật của repo, xem `memory.md`)
bằng lệnh `weasyprint samples/<file>.html <output>.pdf`, sau đó kiểm bằng
`python3 scripts/count_raster.py <output>.pdf --max 0`, đo số trang/số path vẽ bằng PyMuPDF
(`page.get_drawings()`), và **mở ảnh PNG xuất từ PDF bằng mắt** (không chỉ tin "không có CSS
warning là xong") để xác nhận phân lớp thị giác không bị lỗi.

| File | Ảnh raster | Kích thước trang | Số trang | Số drawing (trước dọn box-shadow / sau) |
|---|---|---|---|---|
| editorial-mo-dau-kicker-dek | 0 | 210,0 x 297,0 mm (A4 đúng chuẩn) | 2 | 14 / 14 |
| editorial-tufte-sidenote-margin | 0 | 210,0 x 297,0 mm | 2 | 14 / 14 |
| editorial-luoi-modular-spiegel | 0 | 210,0 x 297,0 mm | 2 | 34 / 34 |
| editorial-chu-thich-nguon-rest-of-world | 0 | 210,0 x 297,0 mm | 2 | 58 / 58 |
| editorial-nhip-tuong-phan-mat-do | 0 | 210,0 x 297,0 mm | 2 | 40 / 40 |

Số drawing KHÔNG đổi trước/sau khi gỡ `box-shadow` ở cả 5 file - bằng chứng trực tiếp rằng
`box-shadow` chưa từng đóng góp một nét vẽ nào vào PDF thật, đúng như phát hiện ở mục 0.1
`FINDINGS.md`.

## Dọn box-shadow chết (theo yêu cầu controller, quét 41 mẫu toàn repo)

Cả 5 file từng khai `box-shadow: 4px 4px 0 rgba(...)` trên `.page` (hiệu ứng trang trí thuần
màn hình, mô phỏng "trang A4 nổi trên nền màu" khi xem trực tiếp bằng trình duyệt) và một dòng
`box-shadow: none` thừa trong `@media print`. Cả hai đều là CSS CHẾT với WeasyPrint (xem mục 0.1
`FINDINGS.md`: `box-shadow` không tồn tại dưới bất kỳ hình thức nào trong WeasyPrint 69.0). Đã
gỡ SẠCH cả 10 chỗ (2 chỗ mỗi file x 5 file), KHÔNG thay bằng kỹ thuật khác (border/offset-duplicate
theo catalog ở `research/04-wow-layer/FINDINGS.md` mục 8): tương phản trắng/xám-xanh giữa `.page`
và nền `html` đã đủ tách lớp thị giác, shadow chỉ là trang trí thêm không mang việc phân tầng
thật, nên đúng theo khung quyết định của controller ("không dựa vào bóng đổ để tách lớp thì chỉ
cần xoá") là xoá thẳng, không cần kỹ thuật thay thế.

## Ba lỗi layout THẬT phát hiện thêm trong lúc mở ảnh xác nhận (không liên quan box-shadow)

Bước xác nhận "mở ảnh nhìn tận mắt" theo yêu cầu của controller phát hiện ba lỗi WeasyPrint khác,
không phải box-shadow, nhưng trực tiếp phá "phân lớp thị giác rõ" nên đã sửa luôn:

1. **Drop cap float đè chữ** (`editorial-tufte-sidenote-margin.html`): `::first-letter { float:
   left }` (và cả một `<span>` float thật) không được WeasyPrint 69.0 chừa chỗ đúng ở dòng đầu,
   chữ theo sau in đè lên chữ cái phóng to. ĐÃ GỠ drop cap khỏi file, xem mục 2.3 và 0.6
   `FINDINGS.md` (đính chính một khẳng định sai trước đó rằng kỹ thuật này "đã kiểm chứng an toàn").
2. **`width` phần trăm tính sai, chỉ khi cột chứa nó vừa là flex-item vừa là flex container theo
   hướng cột** (`editorial-luoi-modular-spiegel.html`): `.bar { width: 62% }` bên trong
   `.bar-col { flex: 1; display: flex; flex-direction: column }` bị WeasyPrint tính theo chiều
   rộng flex container NGOÀI CÙNG thay vì `.bar-col`, khiến mỗi cột biểu đồ tràn lấn sang cột bên
   phải. Đã đổi sang `width: 40px` cố định. LƯU Ý: chẩn đoán nguyên nhân đã được controller phản
   biện và cô lập lại một lần (bản đầu quy nạp quá rộng thành "mọi flex-item lồng nhau", ca tối
   giản của controller chứng minh KHÔNG PHẢI vậy - chỉ sai khi cột đó CÙNG LÚC là flex-item và
   flex-column). Xem mục 0.7 `FINDINGS.md` (đã viết lại, có bảng 7 biến thể cô lập).
3. **`display: inline-flex` giữa dòng văn bản làm ngắt dòng sai** (`editorial-chu-thich-nguon-rest-of-world.html`):
   mô-típ tham chiếu chéo `.xref-mark` dùng `inline-flex` bị đẩy xuống dòng mới dù còn chỗ, và
   dấu câu ngay sau nó văng tới vị trí vô nghĩa. Đã đổi sang `inline-block` + `vertical-align`.
   Xem mục 0.8 `FINDINGS.md`.

Ngoài ra, `editorial-mo-dau-kicker-dek.html` có một lỗi tràn nội dung (footer `position: absolute;
bottom: 14mm` đè lên đoạn nut-graf khi văn bản dài), không liên quan WeasyPrint mà do tự viết CSS
dễ vỡ - đã đổi footer sang luồng bình thường (`margin-top`), robust với mọi độ dài nội dung.

Cả bốn lỗi trên đều được xác nhận đã sửa bằng cách render lại và mở ảnh PNG xuất từ PDF, không
chỉ đọc code.

Trong lúc render thật, phát hiện ba giới hạn CSS của WeasyPrint 69.0 không liên quan gì đến nội
dung thiết kế nhưng ảnh hưởng đến cách viết CSS cho đúng pipeline này: `box-shadow` không được
hỗ trợ dưới bất kỳ hình thức nào (kể cả blur = 0); WeasyPrint CÓ hỗ trợ `@media` cho danh sách
media-type kiểu CSS2 (`screen`, `print`, `all`... đã xác nhận `@media print` áp dụng đúng thật),
nhưng KHÔNG parse được cú pháp media-feature `(max-width: ...)` dưới bất kỳ tổ hợp nào, kể cả sau
`screen and` - ĐÂY KHÔNG PHẢI LÝ DO ĐỂ GỠ ràng buộc cứng "media query màn hình phải viết
`@media screen and (max-width: ...)`" của repo, ràng buộc đó vẫn cần giữ nguyên vì nó đúng và cần
thiết cho trình duyệt thật; và các hàm toán học CSS (`clamp()`/`min()`/`max()`) bị bỏ qua âm
thầm. Chi tiết đầy đủ, gồm ba phép đo dùng để phân định rạch ròi "không parse được" với "parse
được nhưng đánh giá khác", xem mục "0. Bốn phát hiện kỹ thuật" ở đầu
`research/01-editorial/FINDINGS.md` (mục 0.2 đã được controller yêu cầu sửa lại một lần vì bản
đầu suy luận sai).

Cả 5 file đều đã tuân theo đúng cách viết an toàn (không dùng hàm toán học cho font-size, box-shadow
chỉ dùng trang trí cho bản xem màn hình và tắt hẳn ở `@media print`, media query màn hình vẫn viết
đúng chuẩn `screen and` vì đó là hành vi ĐÚNG khi ai đó mở file bằng trình duyệt thật, và ĐỪNG bỏ
`screen` dù WeasyPrint không parse được cú pháp đó).

**Cảnh báo font nhận từ controller, đã đối chiếu và xác nhận KHÔNG dính**: `design-system/fonts/fonts-embedded.css`
đang có bug làm lộn glyph tiếng Việt trong WeasyPrint (`nghệ` ra `nght`) do hai khối `@font-face`
trùng family/weight chỉ khác `unicode-range`, trong khi trình duyệt hiển thị bình thường nên dễ
lọt qua nếu chỉ nghiệm thu bằng mắt trên trình duyệt. Cả 5 file ở đây KHÔNG nạp file đó và không
tự khai `@font-face` nào, chỉ dùng font-family stack có fallback thật từ `tokens.css`. Đã xác
nhận lại bằng cách trích tầng text thật của cả 5 PDF (không đọc bằng mắt): các từ có dấu phức
tạp (`liệu`, `nguyên`, `xuất`, `khẩu`, `giữa`, `biến`, `chuyển`) đều ra nguyên vẹn. Chi tiết đầy
đủ xem mục 0.4 `research/01-editorial/FINDINGS.md`.
