# Nghiên cứu thiết kế editorial: từ toà soạn hàng đầu sang báo cáo tài chính tiếng Việt

Đây là **thư viện tham khảo để lấy ý**, không phải khuôn ép. Mỗi mục dưới đây nêu: nguồn cụ
thể, thủ pháp là gì, tại sao nó hiệu quả, chuyển sang báo cáo tài chính tiếng Việt (in PDF)
thì thành cái gì, và khi nào ĐỪNG dùng. Không ai bắt buộc dùng hết hay dùng đúng nguyên bản.

Ràng buộc cứng của repo (không thương lượng, xem `CLAUDE.md` gốc và `design-system/tokens.css`)
được tôn trọng xuyên suốt tài liệu này và các mẫu HTML đi kèm: shadow blur = 0, cấm
`filter: blur()`/`backdrop-filter`, media query màn hình phải có `screen`, cấm em-dash/en-dash,
font-family phải kết thúc bằng generic keyword, cấm gauge/radar, màu neo theo token
(`--paper #FFFFFF`, `--ink #051C2C`, `--accent #2251FF`), font Spectral (văn) + IBM Plex Mono
(số liệu/nhãn kỹ thuật).

**Ghi chú kỹ thuật quan trọng**: pipeline PDF của repo này dùng **WeasyPrint 69.0**, không phải
Chromium print. Mọi kỹ thuật layout trong tài liệu này được chọn vì tương thích tốt với
WeasyPrint (float, negative margin, `::first-letter`), tránh CSS Grid phức tạp hoặc
`initial-letter` property mà WeasyPrint hỗ trợ không chắc chắn. Các mẫu HTML đã được render
thật qua WeasyPrint và đếm ảnh raster bằng `scripts/count_raster.py` để xác nhận, xem `samples/README-01-editorial.md`.

---

## 0. Bốn phát hiện kỹ thuật xác minh bằng cách render THẬT qua WeasyPrint 69.0, cộng một nguyên tắc bao trùm

Trong lúc render 5 mẫu HTML của mục nghiên cứu này qua WeasyPrint 69.0 để tự kiểm (đúng yêu
cầu "mỗi file phải in ra A4 được"), ba giới hạn CSS sau xuất hiện ở MỌI file, được cô lập và tái
hiện lại bằng file test tối giản riêng để loại trừ khả năng lỗi do nội dung cụ thể; mục thứ tư
(0.4) là một cảnh báo nhận từ controller trong lúc làm vòng này, đã đối chiếu lại với 5 mẫu của
chính agent này để xác nhận không dính. Đây không phải phát hiện thiết kế editorial, mà là giới
hạn ENGINE hoặc bug cụ thể, ảnh hưởng đến toàn bộ repo chứ không riêng gì các mẫu ở đây, nên ghi
lại rõ ràng để không ai phải tái khám phá. Mục 0.2 đã được controller sửa lại sau một lần đọc
phản biện (bản đầu kết luận sai, xem ghi chú "SỬA LẠI" ngay đầu mục 0.2); mục 0.5 đúc kết nguyên
tắc chung rút ra từ cả bốn phát hiện.

### 0.1 `box-shadow` KHÔNG được WeasyPrint hỗ trợ, dưới bất kỳ hình thức nào, kể cả blur = 0

**Thực nghiệm**: mọi biến thể `box-shadow` test (2 giá trị, 3 giá trị blur = 0 có/không đơn vị
`px`, 4 giá trị có spread = 0, cú pháp màu `rgba(R,G,B,A)` cổ điển lẫn `rgba(R G B / A)` CSS
Color 4, kể cả `box-shadow: none`) đều bị WeasyPrint 69.0 báo `WARNING: Ignored ... unknown
property` và bỏ qua toàn bộ khai báo. Xác nhận qua tài liệu chính thức của dự án WeasyPrint
(Kozea/WeasyPrint issue #13): lý do kỹ thuật là shadow CSS dùng Gaussian blur, không biểu diễn
được bằng vector trong PDF, nên WeasyPrint (dùng cairo, không dùng engine raster như Chromium)
không triển khai property này, kể cả trường hợp blur = 0 không cần Gaussian blur thật.

**Ý nghĩa cho repo này**: comment trong `design-system/tokens.css` (dòng 172-178) khẳng định
"shadow blur = 0 an toàn tuyệt đối khi in" dựa trên thực nghiệm đo bằng **Chromium** qua
Playwright ("đo bằng ba biến thể qua playwright+pymupdf"). Kết luận đó ĐÚNG cho pipeline
Chromium, nhưng pipeline THẬT của repo hiện tại là WeasyPrint (đã chốt, xem `memory.md`: "Engine
PDF: WeasyPrint, không phải Chromium"). Với WeasyPrint, kết quả còn triệt để hơn cả "an toàn":
`box-shadow` không render ra BẤT KỲ hiệu ứng gì, có blur hay không có blur, vì property bị bỏ
qua hoàn toàn. Điều này không phải lỗi cần sửa (không có gì "vỡ" hay ra ảnh raster), nhưng nghĩa
là mọi hiệu ứng "khối nổi"/"con dấu mực" dựa vào `--shadow-1/2/3/hairline` trong hệ thống
component hiện tại SẼ KHÔNG XUẤT HIỆN trong PDF thật, dù trông đúng như thiết kế khi xem trên
trình duyệt. `scripts/count_raster.py` không bắt được việc này vì nó chỉ đếm ảnh raster, không
đếm hiệu ứng bị thiếu.

**Khuyến nghị chuyển giao cho vòng xử lý component** (ngoài phạm vi ghi file của agent nghiên
cứu này, chỉ ghi nhận tại đây): nếu cần một tín hiệu "khối nổi" thật sự xuất hiện trong PDF
WeasyPrint, phải dùng `border` (viền cứng, WeasyPrint hỗ trợ đầy đủ) hoặc một phần tử nền màu đặc
đặt lệch bằng `position: relative/absolute` mô phỏng offset shadow bằng hình khối thật, không
dùng property `box-shadow`. Trùng khớp thú vị: cách này lại CÀNG hợp với mục 6.4 của tài liệu
này (hairline rule thay khung/card kín làm trang trông đắt hơn) - giới hạn kỹ thuật ở đây tình
cờ đẩy về đúng hướng thẩm mỹ đã chọn.

### 0.2 WeasyPrint CÓ hỗ trợ `@media` dạng media-type, nhưng KHÔNG parse được cú pháp media-feature `(...)` dưới bất kỳ hình thức nào - ĐỪNG suy ra từ đây rằng ràng buộc `screen` vô nghĩa

**SỬA LẠI so với bản trước của mục này**: bản viết trước đặt tiêu đề "media query CSS3/4 không
được WeasyPrint hỗ trợ", dễ khiến người đọc hiểu lầm là `@media` nói chung không chạy trong
WeasyPrint, rồi suy tiếp (SAI) rằng ràng buộc cứng "media query màn hình phải viết
`@media screen and (max-width: ...)`" là vô nghĩa nên có thể gỡ. Controller đã tự đo lại và chỉ
ra đây là kết luận sai, cần sửa vì hồ sơ này nuôi các vòng nghiên cứu sau. Mục dưới đây viết lại
đầy đủ, kèm phép đo mới để định vị CHÍNH XÁC ranh giới hỗ trợ, không suy diễn nữa.

**Ba phép thử, ĐỀU đã tự chạy lại độc lập trên WeasyPrint 69.0, không chỉ chép báo cáo**:

1. `@media print { .mp { color: #008A6D; } }` - trích màu chữ thật từ PDF ra ĐÚNG `#008A6D`.
   Kết luận: `@media` với media-type dạng CSS2 (`screen`, `print`, `all`, danh sách phân tách
   bằng dấu phẩy) ĐƯỢC PARSE VÀ ĐƯỢC ÁP DỤNG THẬT. WeasyPrint hỗ trợ `@media`, không phải không
   hỗ trợ gì cả.
2. `@media screen and (max-width: 900px) { ... }` khi render (media context là in ấn) không áp
   dụng. Đây ĐÚNG LÀ HÀNH VI MONG MUỐN của ràng buộc cứng repo: khối dành cho `screen` không
   được lộ ra khi in.
3. **Phép đo quyết định, agent này tự thêm để phân định rạch ròi "không parse được" với "parse
   được nhưng đánh giá điều kiện khác"**: đặt cạnh nhau một điều kiện LUÔN ĐÚNG về mặt toán học
   (`@media (min-width: 0px)`) và một điều kiện LUÔN SAI (`@media (min-width: 99999px)`) trong
   cùng một file, không type nào cả, chỉ feature trần. Nếu WeasyPrint THẬT SỰ phân tích cú pháp
   và đánh giá điều kiện (chỉ là đánh giá khác Chromium do quy chiếu độ rộng khác), điều kiện
   luôn đúng phải áp dụng còn điều kiện luôn sai thì không. Kết quả đo được: CẢ HAI đều nhận
   cảnh báo GIỐNG HỆT NHAU (`Expected a media type, got '(min-width: ...)'` rồi
   `Invalid media type ... the whole @media rule was ignored`), và màu chữ cuối cùng vẫn là màu
   gốc (đen) - tức là điều kiện luôn đúng KHÔNG áp dụng. Đây là bằng chứng dứt khoát: WeasyPrint
   không "đánh giá điều kiện rồi ra kết quả khác", mà **KHÔNG PARSE ĐƯỢC cú pháp media-feature
   `(...)` ở bất kỳ vị trí ngữ pháp nào của `@media`, bất kể điều kiện đó về mặt toán học đúng
   hay sai** - toàn bộ khối bị vứt bỏ ở bước phân tích cú pháp, trước khi có bất kỳ phép so sánh
   độ rộng nào xảy ra.

**Kết luận đúng, thay cho kết luận sai ở bản trước**: WeasyPrint 69.0 hỗ trợ `@media` cho danh
sách media-type kiểu CSS2 (`screen`, `print`, `all`...), và áp dụng đúng theo media context đang
render (in thì khối `@media print` chạy, khối `@media screen` không chạy). Nhưng WeasyPrint
KHÔNG có ngữ pháp cho media-feature `(max-width: ...)`/`(min-width: ...)` dưới bất kỳ tổ hợp nào
(trần, sau `screen and`, sau `all and`, sau `not`) - đây không phải "đánh giá khác", mà là
"không đọc được cú pháp đó, vứt cả câu".

**RÀNG BUỘC CỨNG `@media screen and (max-width: ...)` CỦA REPO VẪN ĐÚNG, ĐỪNG GỠ**: quy tắc này
được viết ra để chặn một lỗi CÓ THẬT trong Chromium/trình duyệt thật (nơi CSS Media Queries L3/4
được hỗ trợ đầy đủ, và một `@media (max-width: 900px)` trần THẬT SỰ đánh giá đúng theo độ rộng,
khớp với vùng in A4 688-717px sau margin, làm layout responsive lộ sai vào bản in). Với WeasyPrint,
ràng buộc này vẫn ĐÚNG CÚ PHÁP theo chuẩn CSS thật (nó không sai ở đâu cả) và vẫn là cách viết
ĐÚNG cho người mở file bằng trình duyệt thật, chỉ là WeasyPrint tình cờ vứt luôn cả khối này vì lý
do khác (không parse được feature), không phải vì quy tắc `screen` phát huy tác dụng type-scoping
đúng như thiết kế ban đầu. Hai lý do khác nhau nhưng CÙNG một khuyến nghị: giữ nguyên ràng buộc
`screen`, viết đúng cú pháp chuẩn, không viết tắt bằng `@media (max-width: ...)` trần.

**Hệ quả thực tế cho responsive layout trong PDF**: KHÔNG có cách nào làm layout co giãn theo độ
rộng (breakpoint) hoạt động trong PDF xuất bởi WeasyPrint, bất kể viết đúng hay sai cú pháp theo
ràng buộc cứng của repo - layout trong PDF WeasyPrint luôn là layout mặc định (nằm ngoài mọi khối
`@media (feature)`), kiểm soát hoàn toàn qua `@page` và CSS không điều kiện. Năm mẫu HTML trong
`samples/` viết đúng theo ràng buộc cứng (`@media screen and (max-width: ...)`) vì đó là hành vi
ĐÚNG khi mở bằng trình duyệt thật (giá trị sử dụng chính của các mẫu tham khảo), và WeasyPrint bỏ
qua toàn bộ khối này một cách vô hại cho mục đích in (không có style responsive nào rò vào PDF),
không cần sửa gì thêm ở 5 file mẫu.

### 0.3 Hàm toán học CSS (`clamp()`, `min()`, `max()`) không được WeasyPrint hỗ trợ

**Thực nghiệm**: `font-size: clamp(2.1rem, 4.6vw, 2.369rem)` bị báo
`WARNING: Invalid math function` và toàn bộ khai báo `font-size` bị bỏ qua - phần tử RỚT VỀ
font-size của phần tử cha (đã đo bằng cách export PDF và đọc `span['size']` qua PyMuPDF: headline
lẽ ra phải to hơn 28pt lại ra đúng 12pt, bằng cỡ chữ mặc định của body). Đây là lỗi ĐÃ XẢY RA
THẬT trong bản nháp đầu của `samples/editorial-mo-dau-kicker-dek.html` (dùng `clamp()` để co
giãn cỡ headline theo `vw`) và đã được sửa lại bằng cỡ chữ cố định (`--fs-h1`) cộng một override
riêng trong khối `@media screen` cho màn hình hẹp, thay vì co giãn liên tục bằng hàm toán học.

**Khuyến nghị chung**: bất kỳ CSS nào trong repo này dùng `clamp()`/`min()`/`max()` cho
`font-size`, `width`, hay bất kỳ thuộc tính nào khác cần render đúng qua WeasyPrint, PHẢI kiểm
tra bằng cách render thật và đo giá trị xuất ra (không suy đoán từ CSS nhìn "hợp lý"), vì hàm bị
bỏ qua ÂM THẦM (chỉ có warning trong log, không có lỗi dừng chương trình) và property rớt về giá
trị kế thừa, dễ lọt qua nếu chỉ xem preview trên trình duyệt thay vì xem PDF xuất ra thật.

### 0.4 `fonts-embedded.css` (hai khối `@font-face` cùng family/weight, khác `unicode-range`) làm lộn glyph tiếng Việt trong WeasyPrint, dù trình duyệt hiển thị bình thường

**Cảnh báo nhận từ controller trong lúc làm vòng nghiên cứu này, đã đối chiếu lại với 5 mẫu của
chính agent này để xác nhận không dính lỗi**: `design-system/fonts/fonts-embedded.css` khai 24
khối `@font-face` cho 12 tổ hợp (family, style, weight), mỗi tổ hợp có HAI khối chỉ khác nhau ở
`unicode-range` (subset vietnamese và subset latin). WeasyPrint 69.0 không chọn đúng subset theo
`unicode-range` khi hai khối `@font-face` trùng family/weight/style, dẫn đến lộn glyph ở tầng
TEXT của PDF, không chỉ lộn ở tầng hiển thị: `nghệ` ra `nght`, `liệu` ra `litu`. Vì lỗi ăn vào
tầng text nên copy chữ từ PDF ra cũng sai, không phải chỉ "trông giống chữ khác" mà đúng ra là
KHÁC CHỮ THẬT.

**Điểm nguy hiểm nhất, đây là bài học quy trình chứ không chỉ là một bug**: trình duyệt (Chromium,
Firefox) xử lý `unicode-range` ĐÚNG theo đặc tả, nên nếu nghiệm thu bằng cách mở file HTML trên
trình duyệt xem có "trông đẹp" hay không, lỗi này HOÀN TOÀN không lộ ra - trang trông bình
thường tuyệt đối. Lỗi chỉ lộ khi mở đúng file PDF xuất ra bởi WeasyPrint và đọc tầng text thật
(qua PyMuPDF hoặc copy-paste từ PDF). Đây đúng là trường hợp hai engine phân kỳ ở chỗ khó thấy
nhất: cùng một file CSS, một engine (dùng để xem) đúng, một engine (dùng để giao hàng thật) sai,
và người kiểm bằng mắt trên engine sai sẽ ký nghiệm thu nhầm.

**Xác nhận cho 5 mẫu của vòng nghiên cứu này**: cả 5 file trong `samples/editorial-*.html` KHÔNG
nạp `fonts-embedded.css` và không tự khai bất kỳ khối `@font-face` nào - chỉ dùng font-family
stack có fallback thật lấy nguyên từ `tokens.css` (`"Spectral", "Noto Serif", Georgia,
"Times New Roman", serif` và `"IBM Plex Mono", "Noto Sans Mono", Menlo, Consolas,
"Liberation Mono", monospace`), nên không thể dính lỗi hai-subset này dù Spectral/IBM Plex Mono
có được cài trên máy hay không (engine sẽ rơi xuống Noto Serif/Noto Sans Mono, và bộ đôi đó render
đúng qua WeasyPrint trên máy này). Đã kiểm chứng lại bằng cách trích xuất tầng text thật của cả 5
PDF (đọc qua PyMuPDF, không đọc bằng mắt): các từ có dấu tổ hợp phức tạp xuất hiện trong nội dung
5 file (`liệu`, `nguyên`, `xuất`, `khẩu`, `giữa`, `biến`, `chuyển`) đều trích ra NGUYÊN VẸN, không
có dấu hiệu lộn glyph kiểu `nghệ` thành `nght`.

Nghiệm thu bản in KHÔNG được dừng ở bước mở file HTML bằng trình duyệt xem "có đẹp không". Phải
mở đúng PDF xuất ra bởi engine PDF thật của repo (WeasyPrint) và, với mọi nội dung có dấu tiếng
Việt, trích tầng text thật ra so sánh ký tự chứ không chỉ nhìn hình.

### 0.5 Nguyên tắc bao trùm cả bốn phát hiện trên: "đã verify" PHẢI kèm tên engine, không có ngoại lệ

Đây là bài học tổng quát nhất rút ra từ 0.1 đến 0.4, đứng riêng vì nó áp dụng vượt ra ngoài phạm
vi CSS/WeasyPrint của vòng nghiên cứu này. Nhìn lại bốn phát hiện: `box-shadow` "an toàn" đo bằng
**Chromium** hoá ra không tồn tại trong **WeasyPrint**; ràng buộc `screen` đúng cho **trình duyệt
thật** nhưng vô tác dụng cho lý do khác hẳn trong **WeasyPrint**; `clamp()` chạy tốt trong **mọi
trình duyệt** nhưng rớt âm thầm trong **WeasyPrint**; `unicode-range` đúng chuẩn trong **trình
duyệt** nhưng lộn glyph trong **WeasyPrint**. Cả bốn lần, thủ phạm giống hệt nhau: một phép đo
được gắn nhãn "đã verify" mà không ghi rõ verify TRÊN ENGINE NÀO, rồi bị coi là đúng phổ quát.

**Quy tắc**: một khẳng định "đã kiểm tra an toàn khi in" mà không nêu tên engine cụ thể
(WeasyPrint 69.0? Chromium qua Playwright? engine nào?) là một khẳng định KHÔNG ĐẦY ĐỦ, phải coi
như chưa verify cho engine còn lại. Trình duyệt và WeasyPrint là hai bộ máy layout độc lập, không
dùng chung code, nên "đúng trên cái này" không suy ra được "đúng trên cái kia" theo BẤT KỲ hướng
nào. Vì pipeline PDF thật của repo này là WeasyPrint (không phải Chromium, xem `memory.md`), mọi
kết luận "an toàn khi in" trong tài liệu của repo mà không ghi rõ đã đo trên WeasyPrint đều cần
được đo lại trước khi tin, bất kể kết luận đó cũ hay mới, đến từ nguồn nào.

---

## 1. Kiến trúc trang

### 1.1 Kicker, headline, dek, nut graf, lede: bộ khung vào bài của báo chí

**Nguồn**: quy ước báo chí Anh-Mỹ chuẩn (Poynter, thuật ngữ "hed/dek/lede/nut graf" dùng
xuyên suốt toà soạn Anglo-Saxon; xem tổng hợp tại poynter.org/reporting-editing/2025/journalism-words-reporting-terms-off-the-record/).

**Thủ pháp**: một bài luôn có 4 lớp chữ xếp chồng theo thứ tự đọc, mỗi lớp một vai trò riêng
biệt, KHÔNG lẫn vào nhau:
- **Kicker** (hoặc eyebrow): nhãn ngắn phía trên headline, báo hiệu chuyên mục/ngữ cảnh. Luôn
  nhỏ, thường viết hoa hoặc mono, không cạnh tranh với headline.
- **Headline**: câu khẳng định cụ thể (không phải tiêu đề mô tả chung chung).
- **Dek** (deck): một câu mở rộng headline, cho ngữ cảnh bổ sung mà headline không chứa hết.
- **Nut graf**: đoạn văn xuất hiện SỚM (thường ngay sau lede) nói rõ vì sao chuyện này quan
  trọng, tại sao đọc tiếp, không phải tóm tắt lại headline.

**Tại sao hiệu quả**: người đọc quyết định có đọc tiếp hay không trong vài giây đầu. Bốn lớp
này trả lời bốn câu hỏi khác nhau (chuyện gì loại gì, chuyện gì cụ thể, tại sao liên quan đến
tôi, tại sao quan trọng) mà không cái nào lặp cái nào, tránh được lỗi phổ biến là headline và
dek nói cùng một ý bằng hai cách diễn đạt khác nhau.

**Chuyển sang báo cáo tài chính tiếng Việt**: trang mở đầu báo cáo dùng đúng 4 lớp này thay vì
một khối "Tiêu đề báo cáo" chung chung:
- Kicker: `CẬP NHẬT QUÝ 2/2026 - NGÀNH NÔNG SẢN XUẤT KHẨU` (mono, viết hoa, cỡ nhỏ)
- Headline: câu khẳng định có số, ví dụ "Biên lợi nhuận gộp phục hồi về 18,4% khi giá gạo xuất
  khẩu tạo đáy mới", không viết "Báo cáo cập nhật kết quả kinh doanh quý 2"
- Dek: một câu bổ sung ngữ cảnh, ví dụ nói rõ đây là đáy 2 năm và điều gì thay đổi
- Nut graf: đoạn đầu tiên của thân báo cáo nêu thẳng luận điểm và số neo, KHÔNG mở đầu bằng
  lịch sử công ty hay bối cảnh vĩ mô chung chung (khớp với chỉ đạo đã chốt trong memory
  `feedback_exec_brief_action_first_no_recap`: verdict trước, recap sau nếu cần)

**Khi nào ĐỪNG dùng**: báo cáo nội bộ ngắn (1 trang, dạng ghi chú) không cần đủ 4 lớp, kicker
cộng headline là đủ, thêm dek và nut graf riêng biệt sẽ làm trang nặng nề so với dung lượng nội
dung thực tế. Cũng đừng dùng kicker kiểu mono-caps cho MỌI heading cấp dưới trong thân báo cáo,
chỉ dành cho điểm vào bài, lạm dụng sẽ mất tác dụng phân biệt.

### 1.2 Trang mở đầu khác trang thân bài: Financial Times, Guardian, NYT Magazine

**Nguồn**: [Financial Times redesign 2014](https://www.poynter.org/reporting-editing/2014/financial-times-a-classic-redesign-for-the-digital-age/) (giảm từ lưới 8 cột xuống 6 cột); [Guardian 2018 redesign](https://www.designweek.co.uk/issues/15-21-january-2018/guardian-introduces-tabloid-format-redesigns-platforms/) (chuyển từ Berliner sang tabloid, lưới 8 cột xuống 5 cột, đội thiết kế Alex Breuer/Chris Clarke/Ben Longden); [NYT Magazine redesign, phỏng vấn Gail Bichler trên It's Nice That](https://www.itsnicethat.com/features/gail-bichler-the-new-york-times-magazine-redesign-publication-spotlight-080426).

**Thủ pháp**: trang bìa/trang mở chuyên mục dùng MỘT cột chiếm ưu thế và khoảng trắng lớn
(giảm số cột lưới xuống còn 1 hoặc dùng lưới rộng cho hình), trong khi trang thân bài dùng lưới
hẹp nhiều cột để tối ưu mật độ chữ. FT giảm 8 xuống 6 cột toàn bộ tờ báo để "trang thở hơn, phân
tách rõ tin tức và phân tích". Guardian giảm 8 xuống 5 cột khi chuyển khổ. NYT Magazine giữ lưới
7 cột nhưng CHUYỂN vị trí page furniture (số trang, tên chuyên mục) từ cuối trang lên đầu trang,
mở rộng lề trên, theo lời Bichler: "using the space more intentionally" thay vì xếp cơ học từ
trên xuống dưới.

**Tại sao hiệu quả**: số cột ít hơn nghĩa là mỗi cột rộng hơn, nghĩa là tác giả có ít lựa chọn
bố cục hơn, buộc phải chọn phân cấp rõ ràng thay vì nhét nhiều khối cạnh tranh nhau. Việc trang
mở và trang thân dùng lưới khác nhau tạo TÍN HIỆU chuyển cảnh cho người đọc: "trang này khác,
đây là điểm vào, không phải điểm giữa".

**Chuyển sang báo cáo tài chính tiếng Việt**: trang bìa và trang mở mỗi phần lớn (ví dụ "Phần 2:
Rủi ro và định giá") dùng lưới 1 cột, headline lớn, một con số hero duy nhất chiếm không gian
đáng kể. Trang thân (phân tích chi tiết, bảng số liệu) chuyển sang lưới 2 cột hẹp hơn. Sự khác
biệt lưới giữa hai loại trang PHẢI đủ lớn để nhận ra ngay cả khi lướt nhanh, nếu trang bìa và
trang thân trông gần giống nhau, kỹ thuật này chưa đạt.

**Khi nào ĐỪNG dùng**: báo cáo dưới 4 trang không đủ dài để người đọc cảm nhận được sự
"chuyển cảnh" giữa hai loại lưới, lúc đó một lưới nhất quán xuyên suốt dễ đọc hơn là hai lưới
đổi liên tục. Cũng đừng đổi lưới ở MỌI trang mở tiểu mục, chỉ dành cho ranh giới phần lớn
(2-4 lần trong cả báo cáo), nếu không sẽ mất tác dụng làm mốc điều hướng.

### 1.3 Lưới module co giãn theo nội dung: Der Spiegel

**Nguồn**: [Der Spiegel print redesign, Medium (DEV SPIEGEL)](https://devspiegel.medium.com/wie-wir-den-gedruckten-spiegel-dezent-neu-gedacht-haben-cd7603071d09); bối cảnh chuyển in offset thay rotogravure năm 2016.

**Thủ pháp**: lưới không cố định một độ rộng cột cho mọi loại nội dung. Infographic được cấp
một "grid system giúp tích hợp linh hoạt hơn, với độ rộng và kích thước thay đổi theo nhu cầu
nội dung", nghĩa là một biểu đồ quan trọng có thể tràn 2-3 cột trong khi văn bản xung quanh vẫn
giữ 1 cột hẹp để dễ đọc.

**Tại sao hiệu quả**: ép mọi hình vào đúng độ rộng cột văn bản làm biểu đồ dày đặc bị bóp nhỏ
đến mức mất chi tiết, hoặc bị kéo giãn quá mức. Cho phép hình "xin" thêm cột khi cần giữ được cả
hai: văn bản vẫn ở độ rộng dễ đọc, hình vẫn đủ lớn để đọc số.

**Chuyển sang báo cáo tài chính tiếng Việt**: một bảng so sánh nhiều công ty cùng ngành (comps
table) hoặc biểu đồ waterfall nhiều hạng mục được phép tràn rộng hơn cột văn bản chuẩn (ví dụ
văn bản 1 cột 68 ký tự/dòng, bảng comps tràn full trang), nhưng biểu đồ phụ minh hoạ một luận
điểm nhỏ trong đoạn văn thì thu vào đúng độ rộng cột. Xem thêm mục 4 về quy tắc cụ thể khi nào
tràn, khi nào thu.

**Khi nào ĐỪNG dùng**: nếu báo cáo có nhiều hơn 3-4 mức độ rộng module khác nhau, trang sẽ trông
lộn xộn thay vì có tổ chức, giới hạn tối đa 3 mức (hẹp/chuẩn/tràn) và áp dụng nhất quán, không
tự sáng tác độ rộng mới cho từng hình.

### 1.4 Lưới linh hoạt gắn với một mô-típ đồ hoạ lặp lại: MIT Technology Review (Pentagram, 2018)

**Nguồn**: [Pentagram, case study MIT Technology Review](https://www.pentagram.com/work/mit-technology-review/story); [Nieman Lab, "Instead of abandoning print..."](https://www.niemanlab.org/2018/06/instead-of-abandoning-print-the-119-year-old-mit-technology-review-is-doubling-down-on-it/).

**Thủ pháp**: lưới 12 cột linh hoạt, nhưng đi kèm MỘT mô-típ đồ hoạ tái diễn xuyên suốt ấn phẩm
(dấu "T/r" cắt chéo 45 độ) dùng để chỉ điểm thông tin, tổ chức typography, và cắt góc ảnh. Mô
típ này xuất hiện lặp lại đủ nhiều để người đọc nhận ra nó là "ngôn ngữ điều hướng" của tạp chí,
không phải trang trí ngẫu nhiên.

**Tại sao hiệu quả**: lưới linh hoạt có nguy cơ trông rời rạc nếu không có gì neo lại. Một
mô-típ nhỏ, rẻ (không tốn không gian) nhưng LẶP LẠI NHẤT QUÁN tạo cảm giác "đây là một hệ thống
có chủ đích", không phải ứng biến trang này qua trang khác.

**Chuyển sang báo cáo tài chính tiếng Việt**: chọn một dấu hiệu thị giác nhỏ (không phải icon
sáo rỗng kiểu bóng đèn/mũi tên lên xuống) để đánh dấu nhất quán một loại nội dung xuyên suốt báo
cáo, ví dụ một dấu ngoặc vuông hở góc dùng riêng cho khối "Rủi ro cần theo dõi", hoặc một gạch
chân kép mono dùng riêng cho số liệu đã được kiểm chứng chéo 2 nguồn. Mẫu
`editorial-chu-thich-nguon-rest-of-world.html` minh hoạ một dấu hiệu tự thiết kế (không sao chép
logo T/r của MIT, vì đó là tài sản thương hiệu của họ) dùng làm neo cho tham chiếu chéo giữa các
hình.

**Khi nào ĐỪNG dùng**: đừng phát minh mô-típ mới cho từng báo cáo, giá trị của kỹ thuật này nằm
ở việc lặp lại xuyên suốt NHIỀU báo cáo để độc giả quen mắt, một mô-típ chỉ dùng một lần rồi đổi
coi như không có tác dụng.

---

## 2. Nhịp đọc

### 2.1 Mở bài đắt bằng vị trí "page furniture" và ảnh dọc: NYT Magazine

**Nguồn**: [It's Nice That, phỏng vấn Gail Bichler](https://www.itsnicethat.com/features/gail-bichler-the-new-york-times-magazine-redesign-publication-spotlight-080426).

**Thủ pháp**: chuyển số trang/tên mục lên đầu trang thay vì cuối trang tạo thêm khoảng trắng ở
lề trên, Bichler mô tả đây là cách "dùng không gian có chủ đích hơn" thay vì xếp nội dung máy
móc từ trên xuống dưới. Ảnh trong ấn bản mới thiên về bố cục DỌC để vừa dùng được cho in ấn (ảnh
lớn, tràn trang) lẫn digital (ảnh nhỏ, cạnh nội dung khác).

**Tại sao hiệu quả**: khoảng trắng ở lề trên trước headline hoạt động như một nhịp hít vào
trước khi đọc, não người có xu hướng đọc "nặng" hơn khi chữ dồn sát mép trang. Bố cục ảnh dọc
tận dụng được "sự xa xỉ" của in ấn (ảnh lớn) mà Bichler gọi thẳng là "luxury to the experience",
điều mà digital hiếm khi có được vì ảnh luôn bị các nội dung khác chen vào.

**Chuyển sang báo cáo tài chính tiếng Việt**: trang mở mỗi phần lớn nên có khoảng trắng lề trên
RÕ RỆT lớn hơn các trang thân (ví dụ gấp 1,5-2 lần margin-top thông thường) trước khi vào
headline. Nếu báo cáo có minh hoạ ngành (từ `illustrations/`), ưu tiên bố cục dọc cho minh hoạ
mở đầu phần, để minh hoạ có thể chiếm chiều cao lớn mà không phải cắt ngang nội dung văn bản.

**Khi nào ĐỪNG dùng**: đừng áp khoảng trắng lớn cho MỌI trang, chỉ trang mở phần. Một báo cáo mà
trang nào cũng "hít vào" trước tiêu đề sẽ tốn giấy in vô nghĩa và làm báo cáo trông rời rạc,
không liền mạch.

### 2.2 Nhịp bằng mật độ thay đổi có chủ đích, không phải nhịp đều: The Pudding

**Nguồn**: [Storybench, "How The Pudding structures stories as visual essays"](https://www.storybench.org/pudding-structures-stories-visual-essays/), phỏng vấn Russell Goldenberg và Ilia Blinderman.

**Thủ pháp GỐC (chỉ chạy trên web tương tác, KHÔNG chuyển thẳng sang PDF)**: The Pudding dùng
scrollytelling, mỗi lần cuộn thêm một lớp dữ liệu chồng lên biểu đồ đang có. Bài không theo một
khuôn cố định, nhưng có hai dạng "cung tường thuật" hay lặp lại: hình chữ V đối xứng (hẹp ở
giữa cao trào, rộng ở hai đầu) và hình chữ V lệch (bắt đầu cụ thể, mở rộng, rồi hẹp lại kết
luận). Điểm mấu chốt theo lời nhóm: "cả hai đều có sự thay đổi hình dạng khi câu chuyện tiến
triển, không phải một đường thẳng phẳng".

**Phần CHUYỂN ĐƯỢC sang tài liệu tĩnh**: bỏ hoàn toàn cơ chế cuộn/animation (không tồn tại
trong PDF), chỉ giữ lại NGUYÊN LÝ TRỪU TƯỢNG: mật độ thông tin trên trang nên biến thiên có chủ
đích qua các phần của báo cáo, không đều tăm tắp từ đầu đến cuối. Ví dụ: mở đầu thoáng (1 số
liệu lớn, nhiều khoảng trắng) rồi phần giữa dồn dập (bảng số liệu dày, nhiều biểu đồ nhỏ liền
nhau tại đúng đoạn có luận điểm phức tạp nhất) rồi kết luận thoáng trở lại (khuyến nghị ngắn
gọn, lại nhiều khoảng trắng).

**Tại sao hiệu quả**: một tài liệu có mật độ ĐỀU từ đầu đến cuối không cho người đọc tín hiệu
nào về việc "đoạn nào quan trọng hơn". Biến thiên mật độ đóng vai trò như dấu nhấn âm nhạc, báo
hiệu "đây là đoạn cần chậm lại" mà không cần viết thẳng "đoạn này quan trọng".

**Chuyển sang báo cáo tài chính tiếng Việt**: mẫu `editorial-nhip-tuong-phan-mat-do.html` dựng
một luồng 3 đoạn theo đúng cấu trúc V lệch: mở bằng một con số hero cộng nhiều khoảng trắng,
giữa là bảng chu kỳ tiền mặt dày đặc số liệu tại đúng đoạn phân tích rủi ro tồn kho (đoạn phức
tạp nhất của báo cáo), rồi kết bằng khuyến nghị ngắn với khoảng trắng rộng trở lại.

**Khi nào ĐỪNG dùng**: báo cáo dạng tra cứu (reference, ví dụ phụ lục số liệu, bảng tổng hợp
nhiều công ty) cần mật độ ĐỀU và có thể tiên đoán được để người đọc quét nhanh, biến thiên mật
độ ở phụ lục sẽ gây khó tra cứu, không giúp gì cho việc đọc kiểu tham khảo nhanh này.

### 2.3 Drop cap mở đoạn: quy ước cổ điển, cẩn trọng với dấu tiếng Việt và WeasyPrint

**Nguồn**: quy ước drop cap chuẩn xuất bản (Helen Yentus, [hyentus.com](https://hyentus.com/blog/how-to-use-drop-caps-effectively-in-editorial-design)); kiểm chứng kỹ thuật riêng của agent này bằng WeasyPrint 69.0 có sẵn trong repo.

**Thủ pháp**: chữ cái đầu đoạn mở bài phóng to 3-4 dòng, dùng CSS `::first-letter` với
`float: left`, KHÔNG dùng CSS property `initial-letter` (chuẩn CSS Inline Layout Level 3) vì
mức hỗ trợ của WeasyPrint với property này không chắc chắn. `::first-letter` cộng `float` là kỹ
thuật cũ hơn nhưng được hỗ trợ ổn định trên mọi engine kể cả WeasyPrint, đã kiểm chứng thật bằng
cách render mẫu `editorial-tufte-sidenote-margin.html` qua WeasyPrint 69.0 (xem `samples/README-01-editorial.md`).

**Tại sao hiệu quả**: đánh dấu điểm bắt đầu đọc mà không cần thêm một dòng nhãn "Mở đầu:", chữ
cái lớn tự nó là tín hiệu "đoạn văn bắt đầu ở đây, đọc chậm lại".

**Chuyển sang báo cáo tài chính tiếng Việt**: dùng cho đoạn mở đầu MỖI PHẦN LỚN, không phải mọi
đoạn văn. Vì dấu tiếng Việt nằm trên nguyên âm, chữ cái đầu câu tiếng Việt thường là phụ âm
không mang dấu (ví dụ "Biên", "Doanh", "Chi phí": B/D/C không có dấu), nên rủi ro dấu bị cắt khi
phóng to gần như không có. Rủi ro thật chỉ xảy ra khi đoạn mở đầu bằng một từ có nguyên âm mang
dấu ngay chữ cái đầu tiên (ví dụ "Ước tính..." với Ư mang dấu móc, hoặc "Áp lực..." với Á mang
dấu sắc): trong các trường hợp này, tăng biên trên của riêng ký tự first-letter (không phải
toàn đoạn, xem ghi chú `feedback_vietnamese_ink_metrics`: không cần buffer CJK cho line-height
toàn văn bản, nhưng chữ cái ĐƠN LẺ phóng to 4 lần thì dấu sắc/dấu móc phía trên cần biên trên
rộng hơn tỷ lệ với riêng ký tự đó) hoặc né bằng cách chọn từ mở đầu khác nếu có thể.

**Khi nào ĐỪNG dùng**: đoạn văn ngắn hơn 3 dòng khiến drop cap trông không cân xứng (chữ cái to
hơn cả đoạn văn nó mở đầu). Cũng đừng dùng ở đoạn có số liệu ngay đầu câu (ví dụ "18,4% biên lợi
nhuận..."), không phóng to được chữ số theo quy ước drop cap cổ điển, sẽ phải viết lại câu để
né, không đáng công.

### 2.4 Kicker mono cho eyebrow, không dùng serif: hội tụ ba nguồn

**Nguồn**: Rest of World (Input Mono cho chú thích/nhãn); IBM Plex Mono đã chốt trong
`design-system/tokens.css` cho "kicker, badge, status chip" (đúng theo cách `reference-kimi.html`
dùng mono cho toàn bộ nhãn loại này, xem comment trong tokens.css dòng 118-123).

**Thủ pháp**: nhãn eyebrow/kicker/badge trạng thái dùng font mono thay vì serif của thân bài,
bất kể toà soạn nào. Đây không phải trùng hợp, mono có bộ ký tự đều nhau, viết hoa tự nhiên
trông như một "nhãn dán" hơn là một câu văn, tách biệt vai trò rõ với headline serif ngay bên
dưới.

**Tại sao hiệu quả**: nếu kicker dùng cùng font với headline, mắt phải đọc kỹ để phân biệt "đây
là nhãn phụ" hay "đây là phần đầu headline", dùng font khác hẳn (mono với serif) tạo phân cấp
tức thời không cần suy nghĩ.

**Chuyển sang báo cáo tài chính tiếng Việt**: token đã chốt sẵn, không cần quyết định lại, mọi
kicker/badge/status chip dùng `--font-mono` (IBM Plex Mono), mọi headline/dek dùng `--font-serif`
(Spectral). Các mẫu HTML đều tuân theo quy tắc này.

**Khi nào ĐỪNG dùng**: đừng dùng mono cho câu có nhiều hơn 8-10 từ, mono đọc mỏi hơn serif ở
đoạn dài vì thiếu biến thiên độ rộng ký tự giúp mắt nhận diện từ theo hình dáng tổng thể.

---

## 3. Thang chữ

### 3.1 Hai cỡ quang học của cùng một họ chữ: Financier (FT), Guardian Egyptian

**Nguồn**: [Klim Type Foundry, Financier design information](https://klim.co.nz/blog/financier-design-information/); [Eye on Design, "A New Font is Giving the Financial Times a Smart, Luxurious Update"](https://eyeondesign.aiga.org/new-financier-font-gives-the-financial-times-a-smart-luxurious-update/).

**Thủ pháp**: Financier có hai bản vẽ riêng, Display (cho cỡ lớn, tương phản nét cao, dùng cho
headline) và Text (cho cỡ nhỏ, tương phản nét thấp hơn, dùng cho thân bài), không phải cùng một
file font co giãn cỡ chữ tuyến tính. Đây là kỹ thuật optical sizing truyền thống trong làm chữ
báo in: chữ nhỏ cần nét dày hơn tương đối để không "vỡ" khi in mực trên giấy báo, chữ lớn cần
nét mảnh hơn tương đối để không trông nặng nề.

**Tại sao hiệu quả**: co giãn tuyến tính một file font từ cỡ 12px lên 40px sẽ làm headline trông
"phồng" hoặc thân bài trông "gầy yếu" tuỳ hướng tối ưu gốc của font. Optical sizing giải quyết cả
hai đầu.

**Ghi chú áp dụng cho repo này, đây là trường hợp KHÔNG áp dụng, và tại sao**: `tokens.css` đã
CỐ Ý hợp nhất `--font-display` và `--font-serif` thành cùng một font-stack Spectral (xem comment
dòng 112-123: "Font - Spectral cho MỌI vai trò chữ... không tách display/serif nữa như bản 2").
Đây là quyết định đã chốt của operator, không phải thiếu sót cần "sửa" bằng cách thêm optical
sizing. Spectral tự thân có biến thể weight đủ dùng (Regular/Medium/SemiBold) để tạo phân cấp mà
không cần hai bản vẽ quang học riêng. Ghi nhận kỹ thuật này để BIẾT nó tồn tại, không phải để đề
xuất đổi lại quyết định đã chốt.

**Khi nào CÓ THỂ cân nhắc lại** (không phải khuyến nghị, chỉ nêu điều kiện): nếu một báo cáo
tương lai cần headline cực lớn (trên 48px, ví dụ trang bìa dạng poster) và Spectral Regular ở cỡ
đó trông mảnh yếu trên giấy in, có thể thử tăng weight riêng cho H1 (SemiBold/Bold) thay vì đổi
font, vẫn giữ một họ chữ, chỉ đổi độ đậm theo cỡ.

### 3.2 Tỷ lệ thang chữ 1.333 (quart) đã chốt, không phải phát hiện mới, nhưng đối chiếu ngoài

**Nguồn**: đối chiếu với tỷ lệ thang chữ phổ biến trong thiết kế xuất bản (major third 1.25,
perfect fourth 1.333, golden 1.618), `tokens.css` dòng 129-140 đã chọn 1.333 (`--fs-h1: 2.369rem`
so với `--fs-body: 1rem`).

**Thủ pháp đối chiếu**: 1.333 là tỷ lệ phổ biến trong thiết kế báo/tạp chí vì tạo đủ tương phản
giữa các cấp tiêu đề (H1 gấp khoảng 2,4 lần body) mà không nhảy cấp quá đột ngột như 1.618 (H1 sẽ
gấp khoảng 4,2 lần body nếu áp qua 3 bậc). Không phải phát hiện mới của agent này, ghi nhận ở đây
để xác nhận lựa chọn đã chốt PHÙ HỢP với thực hành xuất bản phổ biến, không phải một con số tuỳ
tiện.

**Khi nào phá thang** (đây mới là phần đáng nói): mọi ấn phẩm khảo sát đều có ít nhất MỘT thời
điểm phá thang có chủ đích, một con số hero lớn hơn cả H1 (không nằm trong bậc thang chữ nào),
dùng đúng 1 lần mỗi trang/phần để đánh dấu "đây là con số quan trọng nhất ở đây". FT và Bloomberg
Businessweek đều dùng con số cỡ cực lớn (dùng `--fs-mono-lg` hoặc lớn hơn, đặt trong mono để
đúng vai trò số liệu) tách biệt hẳn khỏi thang H1-H3 dùng cho văn bản.

**Chuyển sang báo cáo tài chính tiếng Việt**: một con số hero (ví dụ "18,4%" biên lợi nhuận gộp
ở trang mở) được phép lớn hơn `--fs-h1`, đặt bằng `--font-mono` cỡ tuỳ ý (không bắt buộc nằm
trong thang `--fs-*`), NHƯNG chỉ 1 con số hero mỗi trang/phần. Mẫu
`editorial-mo-dau-kicker-dek.html` và `editorial-nhip-tuong-phan-mat-do.html` minh hoạ.

**Khi nào ĐỪNG phá thang**: nếu một trang có từ 2 con số "hero" trở lên cạnh tranh kích thước
ngang nhau, người đọc không biết cái nào quan trọng hơn, phá thang chỉ có tác dụng khi hiếm.

### 3.3 Chữ số bảng biểu (tabular figures) cho bảng tài chính

**Nguồn**: tổng hợp từ TypeType, Fontfabric, Type Network về tabular với oldstyle figures (xem
[Type Network, "OpenType at Work: Figure Styles"](https://typenetwork.com/articles/opentype-at-work-figure-styles)).

**Thủ pháp**: số trong BẢNG (cột số liệu cần thẳng hàng theo chữ số) phải dùng tabular figures
(mỗi chữ số chiếm đúng cùng độ rộng, "1" rộng bằng "9"). Số trong VĂN XUÔI (ví dụ "doanh thu
tăng 12% trong quý") có thể dùng oldstyle figures (chiều cao như chữ thường, có nét lên/xuống)
để hoà vào nhịp đọc của câu, không "nhảy" ra khỏi dòng như số hoa (lining figures) toàn thân cao
bằng chữ hoa.

**Tại sao hiệu quả**: bảng dùng số không tabular sẽ có cột số liệu răng cưa (ví dụ cột nghìn tỷ
đồng không thẳng hàng dấu phẩy thập phân), người đọc phải dừng lại để dóng cột bằng mắt thay vì
đọc thẳng theo hàng.

**Chuyển sang báo cáo tài chính tiếng Việt và tình trạng cần xác minh thêm**: `--font-mono`
(IBM Plex Mono) vốn dĩ MỌI ký tự đều rộng bằng nhau (đặc tính mono), nên số trong bảng dùng mono
đã tự động tabular, đây là điểm mạnh sẵn có của quyết định "số liệu dùng mono" trong `tokens.css`,
không cần làm gì thêm. Điểm CHƯA XÁC MINH: liệu Spectral (dùng cho số nằm trong câu văn xuôi, ví
dụ trong đoạn phân tích) có mặc định xuất oldstyle figures hay lining figures, và liệu WeasyPrint
có hỗ trợ đọc OpenType feature `font-variant-numeric: oldstyle-nums` để chỉnh hay không, đây là
câu hỏi để lại cho vòng sau kiểm tra bằng cách render thật một đoạn số trong Spectral qua
WeasyPrint và so ảnh, KHÔNG suy đoán ở đây.

**Khi nào ĐỪNG dùng tabular cho văn xuôi**: số lẻ trong câu văn dùng tabular figures (đều nhau)
sẽ trông "cứng" và tách rời khỏi nhịp chữ xung quanh, chỉ dùng tabular cho bảng/cột số liệu thực
sự cần dóng hàng.

---

## 4. Hình trong bài

### 4.1 Quy tắc tràn lề với thu vào cột: tổng hợp từ Der Spiegel, FT, NYT Magazine

**Nguồn**: tổng hợp mục 1.3 (Der Spiegel), 1.2 (FT/Guardian), 2.1 (NYT Magazine ảnh dọc).

**Thủ pháp cụ thể** (quy tắc quyết định, không phải cảm tính):
- Hình/bảng tràn lề (full-width hoặc tràn 2 cột trở lên) khi nó là **điểm chốt của cả
  trang/phần**, một biểu đồ mà nếu bỏ đi thì luận điểm của trang sụp đổ. Tối đa 1 hình tràn lề
  mỗi trang.
- Hình thu vào đúng độ rộng cột văn bản khi nó **minh hoạ bổ sung** cho một đoạn cụ thể, người
  đọc vẫn hiểu luận điểm nếu bỏ hình, hình chỉ giúp hình dung nhanh hơn.
- KHÔNG có mức trung gian "tràn 1,5 cột", theo mục 1.3, giới hạn tối đa 3 mức độ rộng (hẹp = cột
  văn bản, chuẩn = 1,5-2 cột, tràn = full trang), chọn dứt khoát một trong ba, không tự sáng tác
  độ rộng tuỳ hứng.

**Tại sao hiệu quả**: độ rộng của hình LÀ một tín hiệu phân cấp thông tin, ngang hàng với cỡ
chữ. Nếu mọi hình đều cùng một độ rộng bất kể tầm quan trọng, người đọc mất một kênh tín hiệu
miễn phí.

**Chuyển sang báo cáo tài chính tiếng Việt**: biểu đồ waterfall lợi nhuận hoặc bảng so sánh định
giá (comps table, thường nhiều cột công ty) là ứng viên tràn lề. Biểu đồ mini minh hoạ một câu
trong đoạn phân tích rủi ro (ví dụ sparkline giá gạo xuất khẩu 12 tháng) thu vào cột văn bản.

**Khi nào ĐỪNG dùng**: đừng tràn lề CHỈ VÌ hình đó "đẹp" hoặc "phức tạp", độ rộng phải phản ánh
tầm quan trọng của luận điểm, không phản ánh độ phức tạp thị giác của hình.

### 4.2 "Wall" small multiples: Reuters Graphics / Edward Tufte

**Nguồn**: nguyên lý small multiples của Edward Tufte, áp dụng phổ biến trong graphics desk các
hãng thông tấn (Reuters, Bloomberg), xem tổng hợp tại [Juice Analytics, "Better Know a
Visualization: Small Multiples"](https://www.juiceanalytics.com/writing/better-know-visualization-small-multiples).

**Thủ pháp**: khi cần so sánh CÙNG một chỉ số trên NHIỀU thực thể (nhiều vùng, nhiều quý, nhiều
công ty), xếp một dãy biểu đồ nhỏ giống hệt nhau về loại, trục, tỷ lệ và kích thước, chỉ khác dữ
liệu, KHÔNG dồn tất cả vào một biểu đồ chồng lớp (điều mà cấm gauge/radar của repo này cũng cùng
tinh thần: tránh biểu đồ "gộp" gây khó so sánh). Thứ tự sắp xếp phải theo logic (thời gian, địa
lý, hoặc giá trị) chứ không ngẫu nhiên.

**Tại sao hiệu quả**: mắt người so sánh hình dạng lặp lại rất nhanh nếu tỷ lệ trục giống hệt
nhau, nhìn một cái thấy ngay ô nào khác biệt. Nếu mỗi ô tự chỉnh tỷ lệ trục riêng (rất hay gặp
lỗi khi tự động generate chart), việc so sánh trở nên sai lệch vì trục không đồng nhất.

**Chuyển sang báo cáo tài chính tiếng Việt**: so sánh doanh thu theo 3 vùng (ĐBSCL/Miền
Trung/Xuất khẩu trực tiếp) qua 4 quý gần nhất, dùng 3 ô small-multiple cùng trục Y, cùng thang
màu, xếp cạnh nhau, thay vì một biểu đồ cột chồng 3 màu duy nhất khó tách bạch xu hướng từng
vùng. Đây là bố cục TRANG (bao nhiêu ô, xếp thế nào), phần thiết kế CHI TIẾT bên trong mỗi ô
biểu đồ (màu, trục, gridline) thuộc phạm vi nghiên cứu doanh nghiệp chart doctrine
(`research/03-chart-doctrine/`), không lặp lại ở đây.

**Khi nào ĐỪNG dùng**: dưới 3 thực thể so sánh thì dùng biểu đồ nhóm cột thông thường đơn giản
hơn là bổ ô riêng, small multiples chỉ đáng công khi có từ 4 thực thể trở lên. Trên 9-12 ô, nên
cân nhắc bảng số liệu thay vì tường biểu đồ (quá nhiều ô nhỏ vượt khả năng quét mắt một lần).

---

## 5. Chú thích và neo số

### 5.1 Sidenote thay footnote: Edward Tufte / Tufte-CSS

**Nguồn**: [Tufte CSS, tài liệu chính thức](https://edwardtufte.github.io/tufte-css/); tổng hợp
tại [Gwern.net, "Sidenotes In Web Design"](https://gwern.net/sidenote).

**Thủ pháp**: ghi chú/nguồn không đẩy xuống cuối trang (footnote cổ điển) mà đặt NGAY BÊN CẠNH
đoạn văn liên quan, trong một cột lề phụ hẹp cùng chiều cao với dòng văn bản tương ứng. Kỹ thuật
CSS: cột lề phụ dùng `float: right` kèm `margin-right` âm để "kéo" nó ra khỏi luồng cột chính,
không cần JavaScript, không cần CSS Grid, đây là lý do kỹ thuật này AN TOÀN với WeasyPrint (float
cộng negative margin thuộc CSS2.1, được hỗ trợ ổn định từ những bản WeasyPrint đầu tiên).

**Tại sao hiệu quả**: Tufte lập luận footnote cuối trang buộc người đọc "nhảy xuống, mất mạch,
rồi tìm đường quay lại", sidenote giữ mắt người đọc gần như đứng yên, chỉ liếc ngang một chút.

**Chuyển sang báo cáo tài chính tiếng Việt**: ghi chú phương pháp luận (ví dụ "giả định giá gạo
xuất khẩu bình quân theo FOB, chưa gồm phụ phí logistics") và trích nguồn dữ liệu (Tổng cục Hải
quan, báo cáo IR doanh nghiệp) đặt ở lề phải ngang đúng đoạn văn liên quan, thay vì dồn hết
thành một khối "Nguồn: ..." ở cuối trang mà người đọc phải tra ngược lại xem số nào ứng với ghi
chú nào. Mẫu `editorial-tufte-sidenote-margin.html` minh hoạ đầy đủ, kèm số thứ tự nhỏ superscript
nối đoạn văn với sidenote tương ứng.

**Khi nào ĐỪNG dùng**: trang có nhiều hơn 4-5 sidenote dày đặc trong cùng một khung nhìn sẽ làm
cột lề phụ trông rối hơn cả footnote nó thay thế, lúc đó quay lại footnote cuối trang hoặc dồn
thành bảng chú thích riêng. Cũng ĐỪNG dùng nếu khổ trang hẹp (ví dụ báo cáo dạng A5 hoặc slide
16:9), không đủ chỗ cho cột lề phụ mà không bóp cột chính xuống dưới độ rộng đọc thoải mái (dưới
khoảng 50 ký tự/dòng).

### 5.2 Pull-quote không rẻ tiền: nguyên tắc từ thực hành NYT Magazine

**Nguồn**: [Fonts In Use, tag "pull quotes"](https://fontsinuse.com/tags/3713/pull-quotes); ghi
nhận thực hành NYT Magazine "designers sometimes use different typefaces for captions and pull
quotes rather than relying on italics alone".

**Thủ pháp cụ thể để TRÁNH pull-quote rẻ tiền** (rẻ tiền là dấu ngoặc kép khổng lồ trang trí
cộng nghiêng toàn câu cộng không có gì khác biệt ngoài kích thước):
1. Không phóng to dấu ngoặc kép làm hoạ tiết trang trí (kiểu icon "chú thích" của template
   PowerPoint), nếu cần dấu ngoặc, giữ cỡ vừa phải, không tách biệt thành hình riêng.
2. Đặt pull-quote trong một cột HẸP HƠN cột văn bản chính, không rộng bằng hoặc rộng hơn, thu
   hẹp cột tạo cảm giác "được chọn lọc/cô đọng" thay vì "được kéo giãn để lấp chỗ trống".
3. Dùng một rule mảnh (hairline, đúng token `--shadow-hairline` hoặc `border-top: 1px solid
   var(--line)`) phía trên và/hoặc dưới thay vì khung viền bao quanh hoàn chỉnh, khung kín bốn
   cạnh là dấu hiệu "card" kiểu slide, không phải kiểu xuất bản.
4. Gán nguồn trích dẫn (ai nói, chức danh) bằng cỡ chữ nhỏ, `--font-mono`, tách dòng riêng, chữ
   ký nhỏ ở dưới, không đặt trong ngoặc đơn liền câu.

**Tại sao hiệu quả**: pull-quote không phải để "trang trí giữa hai đoạn văn", mà để LÀM CHẬM
người đọc tại đúng câu quan trọng nhất bằng cách phá vỡ nhịp đọc một cách có kiểm soát. Trang
trí rẻ tiền (ngoặc kép to, khung kín) tín hiệu "đây là phần trang trí" thay vì "đây là câu quan
trọng nhất trang này", làm ngược tác dụng.

**Chuyển sang báo cáo tài chính tiếng Việt**: trích một câu từ ban lãnh đạo trong buổi họp nhà
đầu tư ("Chúng tôi kỳ vọng biên lợi nhuận quý 3 tiếp tục cải thiện nhờ giá đầu vào ổn định") đặt
làm pull-quote giữa phần phân tích, theo đúng 4 quy tắc trên. Mẫu
`editorial-tufte-sidenote-margin.html` minh hoạ.

**Khi nào ĐỪNG dùng**: đừng bịa trích dẫn không có thật (vi phạm nguyên tắc chống bịa nội dung
đã có trong memory `feedback_no_fake_social_proof`), pull-quote CHỈ dùng khi có câu trích thật từ
nguồn xác thực (biên bản họp, phát biểu công khai, báo cáo IR). Nếu không có trích dẫn thật, dùng
một con số hero (mục 3.2) thay vì pull-quote giả. Trong các mẫu HTML đi kèm, trích dẫn được ghi
rõ là hư cấu minh hoạ vì công ty là hư cấu.

### 5.3 Neo số trong prose bằng màu tiết chế, không phải bôi đậm mọi con số

**Nguồn**: đối chiếu quy tắc "direct labeling, tránh chú thích rời" từ Economist chart style
guide (v1.2, 2017, bản PDF tìm thấy công khai tại sa.ipaa.org.au, không tách được text trực tiếp
do định dạng nhị phân nén, trích qua tóm tắt tìm kiếm) áp dụng ngược vào văn xuôi thay vì biểu
đồ.

**Thủ pháp**: trong một đoạn văn phân tích, chỉ 1-2 con số QUAN TRỌNG NHẤT của cả đoạn được nhấn
bằng màu `--accent` hoặc `font-weight` đậm hơn, không phải MỌI con số xuất hiện trong câu.
Economist áp cùng nguyên lý cho biểu đồ (nhãn trực tiếp cho điểm dữ liệu quan trọng, không nhãn
hoá mọi điểm), ở đây chuyển ngược thành quy tắc cho văn xuôi.

**Tại sao hiệu quả**: nếu mọi con số trong đoạn đều được nhấn màu, mắt không còn tín hiệu để
biết "số nào là luận điểm, số nào chỉ là ngữ cảnh", nhấn tất cả tương đương nhấn không cái nào.

**Chuyển sang báo cáo tài chính tiếng Việt**: trong câu "Doanh thu thuần quý 2/2026 đạt 2.184 tỷ
đồng, tăng 14,2% so với cùng kỳ, trong khi biên lợi nhuận gộp phục hồi lên 18,4%", chỉ số 18,4%
(luận điểm chính của cả báo cáo) được nhấn `--accent`, hai số còn lại (2.184 tỷ, 14,2%) là ngữ
cảnh hỗ trợ, giữ màu `--ink` bình thường.

**Khi nào ĐỪNG dùng**: đoạn văn thuần liệt kê số liệu tham khảo (ví dụ phụ lục "các chỉ số tài
chính khác") không có một luận điểm trung tâm để nhấn, lúc đó không nhấn màu số nào cả, để tránh
nhấn tuỳ tiện không có lý do.

---

## 6. Cái gì làm một trang trông ĐẮT

Tổng hợp các yếu tố ĐO ĐƯỢC hoặc QUAN SÁT ĐƯỢC cụ thể, không dùng tính từ mơ hồ:

1. **Tỷ lệ khoảng trắng lề trên/dưới so với vùng chữ tại trang mở đầu**: các ấn phẩm khảo sát
   (NYT Magazine, FT) đều dành 25-35% chiều cao trang mở đầu cho khoảng trắng thuần (không chữ,
   không hình) trước khi vào headline, so với báo cáo doanh nghiệp phổ thông thường dưới 10%. Đo
   được bằng cách chia chiều cao vùng trắng cho tổng chiều cao trang.

2. **Số lượng độ rộng cột khác nhau trong toàn tài liệu bị giới hạn (2-3 mức, mục 1.3/4.1)**,
   không phải mỗi hình một độ rộng tuỳ hứng. Đo được: đếm số giá trị `width`/số cột lưới khác
   nhau xuất hiện trong CSS toàn báo cáo.

3. **Số điểm "phá thang chữ" mỗi trang tối đa 1 (mục 3.2)**, đếm được bằng cách đếm phần tử có
   `font-size` nằm ngoài thang `--fs-*` đã khai báo trên mỗi trang.

4. **Bo góc gần phẳng, không có border-left màu kiểu "card thông báo"**, đã là quyết định chốt
   của `tokens.css` (radius 0-6px, xem comment dòng 159-165 gọi thẳng "bo tròn lớn cộng
   border-left màu là đúng dấu hiệu AI slop"). Ghi nhận ở đây vì ba nguồn khảo sát độc lập (FT,
   Guardian, NYT Magazine) đều dùng rule mảnh (hairline) và khoảng trắng để phân tách khối,
   KHÔNG dùng khung/card khép kín, hội tụ với quyết định đã chốt, không mâu thuẫn.

5. **Một mô-típ đồ hoạ lặp lại xuyên suốt thay vì icon rời rạc mỗi lần một kiểu** (mục 1.4), đo
   được bằng cách đếm số icon/hoạ tiết KHÁC NHAU dùng cho cùng MỘT vai trò ngữ nghĩa (ví dụ "khối
   cảnh báo rủi ro") trong toàn báo cáo; con số lý tưởng là 1.

6. **Đăng ký giọng nói phù hợp thể loại, Bloomberg Businessweek là ví dụ NGƯỢC cần học có chọn
   lọc**: Businessweek dùng chart-as-illustration kiểu pop-art, hài hước, gây tranh cãi có chủ
   đích (ví dụ bìa kỷ niệm Steve Jobs qua đời từng thắng D&AD Yellow Pencil 2012), đây là ĐĂNG KÝ
   ĐÚNG cho một tạp chí kinh doanh đại chúng, nhưng SAI đăng ký cho báo cáo nghiên cứu định chế
   gửi khách hàng tổ chức. Cái làm trang "đắt" ở thể loại báo cáo tài chính KHÔNG phải sự hài
   hước/pop-art, mà là sự CHÍNH XÁC VÀ TIẾT CHẾ, kỷ luật lưới bên dưới lớp biểu hiện bề mặt
   (Turley bản thân thừa nhận dùng "grid mạnh nhưng linh hoạt học từ Mark Porter/Guardian" để
   chống đỡ cho lớp biểu hiện bề mặt phóng khoáng bên trên). Bài học chuyển được: giữ kỷ luật
   lưới nghiêm ngặt bên dưới, nhưng KHÔNG chuyển lớp biểu hiện bề mặt (màu sắc gây shock, ảnh chế
   biến, chữ khổng lồ trên ảnh) sang báo cáo tài chính tiếng Việt.

7. **Bespoke nhưng nhất quán, Stripe Press**: mỗi đầu sách của Stripe Press có bìa/màu/font riêng
   biệt nhưng cùng tuân theo MỘT bộ nguyên tắc nền (lưới, tỷ lệ margin, cách đặt số trang). Đây
   là mô hình đúng cho MỘT DÒNG báo cáo (ví dụ mọi báo cáo cập nhật quý của cùng team phân tích):
   mỗi báo cáo được phép có màu nhấn phụ hoặc minh hoạ ngành riêng theo lĩnh vực công ty, nhưng
   lưới/thang chữ/vị trí page furniture PHẢI giống hệt nhau giữa các báo cáo để độc giả thường
   xuyên (nhà đầu tư nhận báo cáo hàng quý) nhận ra ngay "đây là báo cáo của team này".

---

## Kỹ thuật KHÔNG chuyển được sang PDF tĩnh, ghi nhận riêng để không ai thử lại

- **Scrollytelling / animation kích hoạt theo cuộn (The Pudding)**: phụ thuộc hoàn toàn vào sự
  kiện cuộn trang của trình duyệt tương tác, không tồn tại khái niệm "cuộn" trong PDF in. Chỉ
  nguyên lý trừu tượng (nhịp mật độ biến thiên, mục 2.2) chuyển được, cơ chế kỹ thuật thì không.
- **Sticky/pinned chart trong lúc cuộn**: cùng lý do, phụ thuộc `position: sticky` kết hợp sự
  kiện cuộn, trên trang in, mọi phần tử đều ở vị trí cố định tuyệt đối trong luồng trang, không
  có khái niệm "dính lại khi cuộn qua".
- **Micro-interaction hover trên biểu đồ (tooltip khi rê chuột) của Reuters Graphics/D3.js**:
  không có sự kiện hover trên giấy in, mọi thông tin cần hiển thị trên PDF phải là nhãn TĨNH luôn
  hiện, không được giấu sau tương tác. Nếu bản HTML màn hình có tooltip, bản in phải có phương án
  nhãn tĩnh tương đương, không được bỏ trống thông tin đó ở bản in.

## Nguồn đã thử nhưng không truy cập được đầy đủ, ghi nhận trung thực

- The Economist, Chart style guide v1.2 (mattmclean@economist.com, cập nhật 4/5/2017), file PDF
  tìm thấy bản sao công khai tại `sa.ipaa.org.au`, nhưng nội dung là PDF nhị phân nén, không tách
  được text trực tiếp qua WebFetch. Các quy tắc trích trong mục 5.3 lấy từ tóm tắt kết quả tìm
  kiếm (thứ cấp), KHÔNG phải đọc trực tiếp trang PDF gốc, cần một agent có công cụ đọc PDF nhị
  phân (ví dụ pdftotext) để khai thác đầy đủ hơn ở vòng sau.
- Financial Times, brand guideline nội bộ đầy đủ và Guardian brand guideline 2018 đầy đủ, không
  tìm thấy bản public toàn văn, chỉ có bài báo/case study bên thứ ba tường thuật lại. Số liệu cụ
  thể (6 cột, 5 cột, tên đội thiết kế) lấy từ các bài tường thuật đó, đã dẫn nguồn rõ ở từng mục.
