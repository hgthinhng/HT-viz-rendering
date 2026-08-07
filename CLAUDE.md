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

Cấm em-dash (U+2014) và en-dash (U+2013) ở MỌI NƠI trong repo chính, kể cả comment mã nguồn và docstring. Miễn trừ đúng hai chỗ, cả hai đều tường minh trong `tests/consistency/em_dash_repo.test.mjs`: thư mục `_harvest/` giữ nguyên bản gốc để còn đối chiếu, và fixture đỏ của gate STYLE bắt buộc phải chứa em-dash, nếu không thì không còn bằng chứng nào rằng gate đó đỏ được.

Ranh giới cũ là "cấm trong nội dung hiển thị, cho phép trong comment". Nó bị bỏ vì đã trả giá hai lần: ranh giới mờ để lại 514 dấu gạch ngang nằm rải trong tài liệu và comment tới mức phải dọn hàng loạt, rồi chính đợt dọn hàng loạt đó phá hai gate (xem mục dưới). Ranh giới tuyệt đối thì không còn chỗ để trôi.

**Gọi hai ký tự này bằng TÊN, đừng dán ký tự vào tài liệu hay vào regex.** Đợt dọn gạch ngang hàng loạt ngày 07-08 đã đổi chính hai ký tự nằm bên trong character class của hai gate chặn em-dash, biến chúng thành `/[--]/g`. Regex đó chỉ còn khớp dấu gạch nối thường: gate báo FAIL cho mọi nội dung bình thường và không còn bắt em-dash, mà vẫn chạy trơn tru không báo gì. Từ nay regex viết bằng escape `\u2014` và `\u2013`, tài liệu gọi tên "em-dash (U+2014)" và "en-dash (U+2013)". Bài học chung: **một phép dọn hàng loạt có thể vô hiệu hoá đúng cái gate canh nó**, nên sau mỗi đợt dọn phải chạy lại bộ test và đọc diff ở vùng mã, không chỉ ở vùng văn xuôi.

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
| SVG không phải XML hợp lệ | Bỏ qua CẢ FILE, không báo lỗi | Tên font bọc nháy đơn, xem mục dưới |

## Tên font trong chart phải bọc bằng nháy ĐƠN, nếu không PDF mất sạch chart

`charts/echarts/theme.mjs` khai `FONT_STACK` bằng nháy đơn (`'Spectral', Georgia, ...`), không phải
nháy kép. Đây không phải chuyện thẩm mỹ. ECharts nhúng nguyên font stack vào thuộc tính
`style="..."` của thẻ `<text>` trong SVG, nên nháy kép lồng trong nháy kép làm file không còn là
XML hợp lệ.

Hậu quả đo được trên engine đích: WeasyPrint bỏ qua toàn bộ file, PDF ra 0 nét vẽ, chart biến mất
sạch mà không báo lỗi gì. Đã đo cả hai chiều trên cùng một file: bản nháy kép cho 0 nét vẽ, bản
nháy đơn cho 24 nét vẽ và chữ đọc được trong tầng text của PDF.

Lỗi này sống sót suốt Phase 1 trên cả 12 chart. Nó lọt được vì trình duyệt vẫn hiện đúng (HTML
parser dễ tính hơn XML parser), nên soi bằng mắt trên bản HTML không bao giờ phát hiện ra, và vì
mọi gate cũ chỉ đếm chuỗi với đếm phần tử chứ không cái nào PARSE.

Gate `verify-charts.mjs` nay parse XML thật. Khi tự set font trong `graphic` hoặc custom
`renderItem`, luôn lấy `FONT_STACK` từ `theme.mjs`, đừng gõ lại tên font.

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

## Mọi chart phải đi qua lớp schema dùng chung

Bốn file, một hợp đồng:

| File | Vai trò |
|---|---|
| `charts/schema.vocab.json` | Từ vựng, cả hai ngôn ngữ cùng đọc. Thêm đơn vị mới thì sửa ở ĐÂY trước |
| `charts/echarts/schema.mjs` | Validator phía Node |
| `charts/matplotlib/schema.py` | Validator phía Python, giữ CÙNG tên trường và CÙNG mã lỗi |
| `charts/fixtures/schema-cases.json` | 28 ca vàng, cả hai phía cùng chạy. Đổi luật thì thêm ca vào đây TRƯỚC |

Mỗi preset gọi `validateSeries()` hoặc `validate_series()` ngay đầu file, fail-fast lúc build. Một
chart sai đơn vị trong bản PDF không gọi lại được.

Bốn điều dễ làm sai, đã có lý do cụ thể:

**Đơn vị, nguồn, số thập phân, chiều tốt xấu và loại số liệu nằm ở cấp SERIES, không ở từng hàng.**
Chính hàm kiểm "không trộn đơn vị" đã tố giác điều đó: nếu trộn đơn vị trong một lượt xếp hạng là
lỗi, thì đơn vị là thuộc tính của lượt xếp hạng.

**`entity.code` chỉ cần NGẮN, tối đa 24 ký tự, giữ nguyên dấu tiếng Việt.** Đừng ép viết hoa không
dấu. Mã chứng khoán thì đẹp, nhưng phân khúc kinh doanh và tên chính sách không có mã tự nhiên, và
"BAN LE" trên trục thì cẩu thả. Cạo dấu là thủ thuật hiển thị, không phải đặc tính dữ liệu.

**Ba loại giá trị thiếu vẽ khác nhau**, đừng gộp thành một `null` chung: `chua_cong_bo` ngắt đường
và chừa chỗ, `khong_ton_tai` ngắt hẳn, `loai_bat_thuong` ngắt và đánh dấu trên trục để người đọc
biết là BỊ LOẠI chứ không phải THIẾU. Dùng `cachVe(status)` để hai engine hành xử giống nhau.

**Cờ base case và ngoại lệ tính từ CHỈ SỐ NGUYÊN qua `coCo()`**, không so sánh giá trị số thực.
Hai giá trị bằng nhau về mặt kinh tế vẫn khác nhau ở chữ số thứ mười lăm.

Số chữ số thập phân luôn lấy từ `soThapPhan(series)`. Tự chọn ở mỗi engine là cách bản HTML hiện
15,45% còn bản PDF hiện 15,5%.

## Chart phải tắt animation, nếu không marker bị kéo về gốc toạ độ

`baseOption()` khai `animation: false`. Đây không phải chuyện thẩm mỹ mà là chuyện đúng sai.

ECharts SSR mặc định xuất CSS `@keyframes` cho mọi marker, và keyframe cuối là
`transform: scale(n,n)`. CSS transform **thắng** thuộc tính XML, mà keyframe đó không mang phần
translate, nên sau khi animation chạy xong marker bị kéo về gốc toạ độ rồi phóng to. Đã nhìn tận
mắt trên `out-04-dumbbell.svg` trước khi vá: mọi chấm biến mất khỏi vị trí đúng, còn đúng một
chấm lạc ở góc trên trái.

Chỉ hỏng ở bản HTML mở bằng trình duyệt. Bản PDF không dính vì WeasyPrint không chạy CSS
animation, và đó cũng chính là lý do bug này sống sót cả một phase: mọi phép nghiệm thu của repo
hoặc đi qua PDF, hoặc đi qua gate đếm phần tử. Không phép nào mở SVG bằng trình duyệt thật rồi
nhìn.

Preset nào tự dựng option mà không qua `baseOption()` thì phải tự khai `animation: false`. Có
gate trong `verify-charts.mjs` chặn tái phạm, đã kiểm là đỏ được khi gỡ cờ ở nguồn.

## Soi ảnh chart: hai cách tạo ra lỗi GIẢ, đã dính cả hai trong một buổi

Repo này có sẵn luật "phép cuối cùng là mở ảnh ra nhìn". Luật đó đúng, nhưng phép soi cũng hỏng
được, và khi nó hỏng thì nó báo lỗi ở chỗ không có lỗi. Hai cách đã dính:

**Chụp sớm hơn animation.** ECharts SSR nhúng CSS animation chạy 1 giây vào SVG, hiệu ứng vẽ
dần. Chụp sớm thì đường line hiện ra đứt đoạn, trông hệt chart hỏng. Đã mất công truy một ca:
path trong SVG có đủ tám điểm nối liền và có `stroke` đầy đủ, nhưng ảnh chỉ hiện bốn điểm đầu.
Chờ ít nhất 1500ms sau khi tải xong.

**Soi ảnh toàn cảnh bị thu nhỏ.** Một chấm scatter đường kính 8px trong SVG 680px, khi xem ở
ảnh toàn cảnh đã thu nhỏ, biến mất khỏi mắt giữa đám nhãn. Suýt kết luận là "scatter không vẽ
chấm" trong khi chín chấm đều có, đúng chỗ, viền đúng vai trò. Khi nghi ngờ một chi tiết nhỏ,
**crop đúng vùng đó ở độ phóng cao** rồi mới phán.

Cách tránh cả hai: nghiệm thu chart bằng **bản PDF qua WeasyPrint**, không phải bản trình duyệt.
PDF là thứ giao đi, và nó không có animation nên không có trạng thái nửa chừng. Đếm nét vẽ bằng
`get_drawings()` cho câu trả lời bằng số trước khi cần đến mắt.

Đây là bẫy NGƯỢC với mọi bẫy khác trong file này. Các bẫy kia làm gate xanh giả trong khi thứ
giao đi đã hỏng. Bẫy này làm mắt thấy đỏ giả trong khi thứ giao đi vẫn đúng. Cả hai đều tốn thời
gian như nhau, và cái sau còn dẫn tới sửa một thứ không hỏng.

## Khi thêm chart

Màu lấy từ `charts/echarts/theme.mjs`, không hardcode hex. Mọi script chart phải kết bằng `chart.dispose(); process.exit(0);` vì ECharts SSR không tự thoát process.

Chart matplotlib lấy font từ `design-system/fonts/ttf/`, đã nhúng trong repo, không mượn font hệ thống. Đừng thêm đường dẫn `/usr/share/fonts` mới vào `_eir_style.py`: nhánh hệ thống còn lại chỉ là dự phòng cuối. Sinh lại file `.ttf` bằng `python3 design-system/fonts/extract-ttf.py` sau khi `build-fonts.py` chạy lại.

Phải có bản `.ttf` riêng dù repo đã nhúng font base64, vì matplotlib đọc ttf/otf/ttc chứ không đọc woff2, mà `fonts-embedded.css` toàn woff2. Trích ngược từ chính file CSS đó chứ không tải mới từ Google Fonts, để chạy được offline và để bản chart với bản HTML không thể lệch font.

Một cái bẫy đã cắn khi làm việc này: Google Fonts đặt tên họ của bản 600 là `IBM Plex Sans SemiBold`, tức một HỌ KHÁC chứ không phải cấp đậm của `IBM Plex Sans`. Trích nguyên xi thì matplotlib đăng ký hai họ rời rạc, và khi chart xin bản đậm nó không tìm thấy nên tô giả. `extract-ttf.py` ép lại `nameID` 1/16 cho khớp. Kiểm bằng `findfont` chứ đừng tin danh sách tên mà `setup_fonts()` trả về.

## Đường ống: từ markdown ra PDF đã qua gate

Một lệnh chạy trọn sáu bước:

```bash
python3 pipeline/orchestrator.py examples/mau-phase2/noi-dung.md   # hoặc: npm run mau
```

| Bước | Làm gì |
|---|---|
| 1 HÌNH | chạy mọi `hinh/*.mjs` và `hinh/*.py` của báo cáo, bake mọi `hinh/*.html` |
| 2 CK1 | ghi kịch bản kể chuyện: mỗi section một câu hỏi, hình nào trả lời |
| 3 CK2 | dựng ba bản bìa bằng nội dung thật, đủ ba kiểu, để chọn một |
| 4 DỰNG | HTML tự đủ, cả bản nội bộ lẫn bản gửi đi |
| 5 CK3 | xuất PDF cả hai bản |
| 6 GATE | chạy mười gate trên cả hai bản |

Checkpoint ghi artifact rồi in đường dẫn, KHÔNG hỏi y/n trên terminal. Script dừng chờ
gõ phím thì không chạy được trong test tự động, không chạy được khi Claude gọi, và
không chạy được trong batch. Điểm dừng để duyệt vẫn còn, chỉ khác ai bấm nút.

Báo cáo là một thư mục, không phải một file:

```
examples/mau-phase2/
├── noi-dung.md      front-matter + markdown + directive
├── so-nguon.json    mỗi số một nguồn, một bậc bằng chứng, một ngày lấy về
├── hinh/            script sinh hình, và file ra-*.svg chúng sinh ra
└── ra/              artifact, đã gitignore, sinh lại bằng npm run mau
```

Bốn directive, viết trên một dòng riêng:

```
::: chart src=hinh/ra-01-x.svg id=hinh-x chu="Chú thích" nguon=K2
::: minh-hoa src=hinh/ra-03-y.svg id=hinh-y chu="Chú thích" nguon=K2
::: ngat-trang
```

Số có nguồn viết `{{ma_gia_tri}}` ngay trong câu văn. Mã không có trong sổ nguồn thì
build dừng ngay, không im lặng bỏ qua: một con số không nguồn trong bản PDF đã gửi đi
thì không gọi lại được.

## Hai chế độ xuất, không được gộp

`noi-bo` nhúng đủ sổ nguồn vào `<script id="evidence-ledger">`, danh mục nguồn hiện tên
tổ chức và trích dẫn đầy đủ. `gui-di` KHÔNG nhúng sổ nguồn, và nguồn `internal_only`
chỉ hiện `public_label`.

Lý do bản gửi đi không nhúng sổ nguồn: nhúng vào là tự đưa tên cơ quan và kênh tin ra
ngoài trong một thẻ script mà người đọc không thấy nhưng `Ctrl+U` thì thấy. Cả hai bản
dựng từ cùng một file markdown nên không có đường nào để chúng nói hai điều khác nhau.

## Minh hoạ có callout PHẢI bake trước khi vào báo cáo

`annotate.js` vẽ callout bằng JavaScript lúc chạy. WeasyPrint không chạy JavaScript.
Nhúng thẳng file HTML minh hoạ vào báo cáo thì bản PDF mất sạch lớp chú thích, tức mất
đúng phần mang giá trị của minh hoạ neo số liệu.

Đo được trên `example-vertical-axis-ship.html`: bản gốc qua WeasyPrint cho 42 nét vẽ và
197 ký tự text, 0 trên 7 callout. Bản đã bake cho 74 nét vẽ và đủ 7 callout.

```bash
node pipeline/bake_svg.mjs <vao.html> <ra.svg> --selector="#ma-svg"
```

Bake làm ba việc: chờ annotate chạy xong rồi đóng băng cây SVG, resolve `var()` và
`color-mix()` thành màu thật, ghim `font-family` đã resolve và đổi nháy kép sang nháy
đơn. Gate 6 CALLOUT-BAKED chặn nếu quên.

## Mười gate, và luật gate phải tự đỏ được

```bash
node gates/run.mjs <file.html> <file.pdf> --che-do=noi-bo|gui-di
```

| # | Gate | Bắt gì |
|---|---|---|
| 1 | FONT-HTML | font đầu stack phải Windows-safe hoặc nhúng base64 phủ dấu tiếng Việt |
| 2 | FONT-PDF | tên font THẬT trong PDF, đỏ khi thấy Noto, Liberation, DejaVu |
| 3 | RASTER | đếm `/Subtype /Image` qua `xref_object`, mặc định phải bằng 0 |
| 4 | DIACRITICS | U+FFFD và ký tự CÓ DẤU bị đánh synthetic |
| 5 | CHART-SONG | mọi SVG parse được XML, và để lại chữ trong tầng text của PDF |
| 6 | CALLOUT-BAKED | trang không còn gọi `annotate.js` lúc chạy |
| 7 | STYLE | em-dash, en-dash, AI-slop, câu kết cách ngôn |
| 8 | PAGEBREAK | CSS bảo vệ, và hình học thật tìm thẻ bị cắt ngang biên trang |
| 9 | SOURCE-LEAK | cụm từ cấm, tên riêng viết tắt, đối chiếu sổ nguồn ở bản gửi đi |
| 10 | LEDGER | sổ nguồn hợp lệ: không mồ côi, không lệch bậc, không lệch đơn vị |

**Mọi gate mới phải có cặp fixture đỏ và xanh trong `gates/fixtures/`, và phải có test
trong `tests/consistency/gate_do_xanh.test.mjs` ép bản xanh PASS và bản đỏ FAIL.** Gate
nào không đỏ được với fixture đỏ của chính nó thì gate đó chưa tồn tại. Repo này đã có
ba gate như vậy ở Phase 1, cả ba đều chạy trơn tru và cả ba đều vô dụng.

## Gate 2 FONT-PDF ra đời vì tầng text không phân biệt được font sai

Đây là phép đo mà bộ gate cũ không có, và nó lấp đúng một lỗ hổng đo được bằng số. Cùng
một trang HTML:

| Bản | Font trong PDF | FFFD | Ký tự synthetic | Tầng text |
|---|---|---|---|---|
| Có `@font-face` base64 | `Spectral`, `IBM-Plex-Mono` | 0 | 0 | đúng dấu |
| Bỏ `@font-face` | `Noto-Serif`, `Liberation-Mono` | 0 | 0 | đúng dấu |

Hai bản giống hệt nhau ở mọi phép đo tầng văn bản. Chỉ đọc tên font trong PDF mới phân
biệt được. Nghĩa là gate dấu tiếng Việt, dù viết đúng tới đâu, cũng mù hoàn toàn với ca
file rơi về font hệ thống Linux.

Một hệ quả cần biết khi đọc số: font subset không nhúng glyph dấu CÁCH, nên MuPDF đánh
dấu mọi dấu cách là synthetic. Một bản PDF sạch 6 trang cho ra 119 ca như vậy. Đếm cả
thì gate đỏ vĩnh viễn, nên gate 4 chỉ đếm synthetic trên riêng tập ký tự có dấu.

## Đối chiếu chuỗi với tầng text của PDF phải bỏ hết khoảng trắng

Trích text từ PDF nuốt khoảng trắng giữa các glyph sát nhau: "475 TỶ USD" ra thành
"475TỶUSD". So nguyên văn sẽ báo thiếu một chuỗi đang có thật trên giấy. Dùng `boTrang()`
trong `gates/gates.mjs` cho mọi phép đối chiếu kiểu này.

## Ba cái bẫy của tầng trình bày, đều đã cắn thật ở Phase 2

**`string-set: ... content()` KHÔNG được đặt lên `body`.** `content()` lấy nội dung của
chính phần tử đó, nên đặt ở body thì chuỗi chạy chân trang trở thành toàn bộ văn bản của
báo cáo, và WeasyPrint in nguyên khối đó vào vùng chân trang, tràn ra đè lên cả trang.
Chỉ `h2` được khai.

**Màu tiêu đề trên nền tối phải đủ specificity.** `.bao-cao h1` khai `color: var(--ink)`
đè lên `color` kế thừa từ `.bia`, cho ra chữ `#051C2C` trên nền `#051C2C`. Tiêu đề biến
mất khỏi trang bìa mà vẫn nguyên trong tầng text, nên mọi phép đếm đều báo bình thường.

**`name` của `valueAxis` đè lên `title.subtext`.** ECharts đặt tên trục ở đỉnh trục,
đúng chỗ phụ đề đang chiếm. Quy ước của repo: đơn vị ghi ở PHỤ ĐỀ, không lặp ở tên trục.

## SVG nhúng inline phải đổi tiền tố id và bó hẹp `<style>`

Nhiều SVG trên cùng một trang mà trùng `id` thì `url(#grad)` của hình sau trỏ nhầm vào
định nghĩa của hình trước, và triệu chứng hiện ra là "hình thứ hai mất màu" chứ không
phải một lỗi rõ ràng. `build_html.py` tự đổi tiền tố.

matplotlib còn xuất kèm `<style>*{stroke-linejoin: round}</style>`. Trong file `.svg`
riêng thì `*` chỉ chạm chính nó; nhúng inline vào HTML thì `*` chạm mọi phần tử của cả
trang. `build_html.py` gắn tiền tố `#<mã-hình>` vào trước mọi selector.

## Khi thêm minh hoạ

Đọc `illustrations/grammar.md` trước. Ba bài tự kiểm bắt buộc: che hết chữ mà không đọc ra biến cấu trúc thì xoá, không polish; đổi ngành mà hình vẫn dùng nguyên được thì đó là trang trí chứ không phải phân tích; kiểm danh sách đen chart giả.

## Không bao giờ

- Sửa CSS cho khớp catalog. Sửa catalog cho khớp CSS, vì CSS là thứ đang chạy và đã verify
- Dùng `get_images()` để đếm ảnh trong PDF
- Tin một package là tự đủ chỉ vì nó chạy được ở thư mục gốc của nó
- Kết luận "đã kiểm an toàn" từ một phép đo mà kết quả không thể sai
