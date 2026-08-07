# HT-viz-rendering: bàn giao cho phiên mới

Đọc file này trước tiên. Nó cho biết đang ở đâu và làm gì tiếp.

## ĐỌC MỤC NÀY TRƯỚC: tiền đề của repo đã đổi (07-08)

Repo được xây trên tiền đề **"PDF IN ĐƯỢC"**. Người dùng đã phán quyết tiền đề đó sai với thực
tế: không ai in bản giấy nữa. Giữ nó là tự bóp chính mình, vì nó loại oan trọn hai trường phái
mạnh nhất của nghiên cứu (narrative formats và motion idioms) chỉ vì WeasyPrint không chạy
JavaScript.

**Đích mới: DIGITAL ONLY, hai làn, người dùng chọn theo từng ấn phẩm.**

| Làn | Là gì | Được phép | Còn ràng buộc |
|---|---|---|---|
| `html-song` | HTML tự đủ mở bằng trình duyệt | animation, tương tác, scrollytelling, tooltip, hover, JavaScript lúc chạy, canvas, WebGL, blur, dark mode, responsive | một file tự đủ, chạy offline, không CDN ngoài, font nhúng |
| `pdf-so` | PDF đọc trên MÀN HÌNH, không phải để in | khổ ngang, màu RGB, siêu liên kết, bookmark, hết lo lề nhà in | tĩnh hoàn toàn, chữ chọn được trong tầng text |

**Engine PDF: người dùng đã chốt GIỮ WeasyPrint**, không đổi Chromium. Nên `bake_svg.mjs`,
gate 6, bảng ba thuộc tính WeasyPrint bỏ qua, và lệnh cấm `color-mix()` đều GIỮ NGUYÊN cho làn
`pdf-so`. Siêu liên kết và bookmark vẫn làm được qua `bookmark-level` mà WeasyPrint hỗ trợ sẵn.

**Bảng màu ĐÃ MỞ**: trắng lạnh nay là MẶC ĐỊNH, không còn là hằng số. Ràng buộc con giữ nguyên
độ cứng: một báo cáo chỉ MỘT bảng màu, báo cáo chọn TÊN bảng chứ không chọn hex, và mọi bảng
mới phải qua gate tương phản. Gate đó CHƯA CÓ, là việc mới đẻ ra từ quyết định này.

**Bốn luật KHÔNG được nới theo**, vì chúng không sinh ra từ in ấn: cấm gauge và radar (lý do
đúng sai phân tích) · cấm em-dash, en-dash, AI-slop, câu kết cách ngôn (văn phong) · font phải
nhúng (máy khách không có font) · mọi số phải có nguồn.

### Đã làm được gì cho cú bẻ lái (commit `e9a1336`)

Bước 1 và 2 XONG. Cả hai đều là GỠ ràng buộc, không thêm tính năng, nên mọi lời gọi cũ giữ
nguyên hành vi.

- `nap_svg()` nhận `cho_phep_raster`, `lap_trang()` nhận `chu_de`, `dung()` nhận `lan` và
  `chu_de`, CLI có `--lan` và `--chu-de`. Mặc định `pdf-so` và `light`.
- `catalog_drift.test.mjs` đổi từ `assert.equal(29)` sang SÀN, nên thêm component không còn làm
  `npm test` đỏ ở bước đếm.
- Luật `rgba(R G B / A)` GỠ HẲN. Luật `blur=0` giữ nhưng lý do đã đính chính.

### Việc tiếp theo, ĐÚNG THỨ TỰ NÀY

3. `design-system/themes/*.json` làm nguồn sự thật duy nhất, cộng generator sinh ra cả
   `tokens.css`, `tokens.py` và `theme.mjs`, cộng test drift. **Bảng màu hiện nằm ở 5 nơi viết
   tay**, trong đó hai nơi là TEST tự hardcode kỳ vọng (`tokens_test.py:37-45`,
   `chart_theme.test.mjs:12-22`), tức thứ canh gác lại là bản sao của thứ bị canh.
4. Migrate **345 hex viết cứng trong 11 file `illustrations/svg/`** sang `var()`. Không tự động
   hoá được vì cùng một hex đóng nhiều vai trong cùng một hình. Trả HAI nợ một lần, xem mục
   "Hai hệ màu song song" bên dưới.
5. **29 chỗ `color=PAPER` / `fg=PAPER` / `c=PAPER` trong matplotlib sang một hằng số riêng
   `ON_INK`. PHẢI XONG TRƯỚC KHI BẬT BẤT KỲ CHỦ ĐỀ NỀN TỐI NÀO.** Chúng là chữ trắng đặt trên
   khối màu đậm; trên nền tối `PAPER` thành màu tối và ta được chữ tối trên nền tối, đúng lớp
   lỗi `.bia h1` mà mọi phép đếm đều báo bình thường. 43 chỗ `facecolor=PAPER` thì TỰ ĐÚNG.

**Chưa render thêm một tài sản mới nào.** Kho vẫn đúng 108 như trước. Danh sách nạp đã lọc qua
khung digital nằm ở memory toàn cục `project_ht_viz_rendering_2026-08-06.md`.

### Hai hệ màu song song, nợ có từ TRƯỚC cú bẻ lái

11 minh hoạ SVG dùng **345 hex viết cứng, và không một mã nào là `#051C2C` hay `#2251FF`**.
Chúng là bảng Tailwind (`#0f172a`, `#e2e8f0`, `#64748b`, `#2563eb`, `#f59e0b`, `#0d9488`). Tầng
minh hoạ **chưa bao giờ đi qua cửa `tokens`**, trong khi nhóm matplotlib đã bị ép đi qua bằng cả
một khối lập luận ở `_eir_style.py:29-52`. Chỉ `--accent` là di động, xuất hiện đúng 2 lần trong
89 dòng của `logistics-container-ship.svg`.

Chuyển 345 hex sang `var()` trả cả hai nợ một lượt. Sơn tay sang bảng tối thì trả một nợ và đẻ
thêm một nợ (22 file thay vì 11).

### Bẫy kiến trúc ECharts phải chốt TRƯỚC khi động vào `theme.mjs`

ECharts SSR ghi hex **thẳng** vào SVG tĩnh, không `var()` nào chạy lúc người đọc xem (kiểm được
trên `out-01-waterfall.svg`: 0 lần `var(--`, cả 8 mã hex đã bake thành chữ literal). Nên "chart
theo chủ đề người đọc chọn" KHÔNG làm được bằng CSS. Hai đường, chưa chọn: sinh N bản SVG mỗi
chart (chi phí nhân theo số chủ đề), hoặc hậu xử lý đổi hex thành `var()` (một bản duy nhất,
nhưng sót một hex là ra vệt màu lạc rất khó bắt bằng mắt, phải có gate đếm hex còn sót).

### Ba gate rỗng MỚI phát hiện, cộng vào ba cái của Phase 1

4. `gates/gates.mjs:261-264` gate 5 CHART-SONG: SVG không có chuỗi chữ dài từ 4 ký tự thì
   `continue` mà KHÔNG đổi `trang_thai`. Hình đó vẫn PASS, chỉ còn được che bởi phép kiểm yếu
   nhất là XML parse được.
5. Gate `khoa-sang-khong-doi-theo-may-khach` chỉ đọc `getComputedStyle(document.body)`, tức
   KHÔNG nhìn thấy chart hay minh hoạ, nên không có khả năng phát hiện đúng bệnh mà luật khoá
   sáng sinh ra để tránh.
6. `--shadow-*` blur bằng 0 canh một thứ WeasyPrint chưa bao giờ vẽ. Xem mục dưới.

### Một luật cấp hệ thống đã vô nghĩa suốt hai phase

`docs/specs/...design.md:79` chốt "shadow offset cứng là ngôn ngữ độ nổi DUY NHẤT của toàn hệ",
dựa trên phép đo chạy trên **Chromium in**. Nhưng engine chốt là **WeasyPrint**, và WeasyPrint
**không vẽ box-shadow bằng bất kỳ cú pháp nào**. Luật đó chưa bao giờ bảo vệ bản giao đi; nó chỉ
bó tay bản trình duyệt. Nó còn đẻ ra luật con `rgba(R G B / A)` tồn tại CHỈ để một dòng
`split(",")` trong test chạy đúng.

**Bài học cấp doctrine**: repo có gate ép mọi gate phải tự đỏ được, nhưng KHÔNG có gate nào hỏi
**"luật này còn lý do không"**. Mỗi luật cứng từ nay phải ghi LÝ DO và ĐIỀU KIỆN HẾT HIỆU LỰC
ngay cạnh nó.

### Nợ nhỏ: SVG sinh ra không tái lập được

`hinh/ra-*.svg` được commit nhưng matplotlib nhúng `<dc:date>` và một `clip-path` id ngẫu nhiên,
nên mỗi lần chạy `npm run mau` là cây git bẩn thêm một file dù không có gì đổi thật. Chữa bằng
`svg.hashsalt` và tắt metadata.

## Đang ở đâu

**Phase 2 ĐÓNG.** Đường ống từ markdown ra PDF đã qua gate chạy được bằng một lệnh, và
mười gate đều đã chứng minh là đỏ được với fixture đỏ của chính chúng.

Nghiệm thu gần nhất, chạy thật chứ không chép lại:

| Lệnh | Kết quả |
|---|---|
| `npm test` | 109 pass, 0 fail |
| `npm run verify` | exit 0, mọi gate PASS và 2 SKIP có ghi rõ lý do |
| `python3 -m pytest tests/ -q` | 48 passed |
| `npm run mau` | 6 trang, 169 nét vẽ, 0 ảnh raster, 10 gate PASS ở bản nội bộ và 9 PASS 1 SKIP ở bản gửi đi |

Phase 1 đóng trước đó: 8 task review sạch, 50 commit, cộng đợt dọn và đợt mở rộng thư viện.

Hai SKIP là cố ý, không phải gate hỏng: `gallery.html` là trang nội bộ nên không khai
`data-theme="light"`, và `vietnam-simplification-comparison.html` không dùng lớp annotation.

Trong repo: 50 mẫu ở `samples/`, 14 hồ sơ ở `research/`, 29 catalog spec, 11 minh hoạ SVG,
18 preset chart ECharts, 50 component matplotlib EIR.

**Đợt mở rộng thư viện đã xong**, làm một lần cho lâu dài. Bốn thứ mới:

1. **Lớp schema dùng chung hai engine**: `charts/schema.vocab.json` (từ vựng, cả hai ngôn ngữ
   cùng đọc), `charts/echarts/schema.mjs`, `charts/matplotlib/schema.py`, và 28 ca hợp đồng ở
   `charts/fixtures/schema-cases.json` chạy ở CẢ HAI phía. Mọi preset mới phải đi qua lớp này.
   Quy ước đầy đủ trong `CLAUDE.md`.
2. **Sáu preset ECharts mới** 13 tới 18: line có chú thích, bar ngang xếp hạng kèm biến thể
   Cleveland dot, scatter chia phần tư, dot strip phân phối, football field, lưới độ nhạy.
3. **Năm component nhóm B** khối 25 tới 29: tóm tắt điều hành bốn ô, thẻ kịch bản, dải thắng
   thua, ngã ba chính sách, dải tự sự.
4. **Họ đường cong** cho matplotlib: `viz_eir_curves.py` với `c_yield_curve` và
   `c_futures_curve`, cộng cờ `zero_is_signal` thêm vào `c_spread`.

## Phase 2 đã dựng gì

Kế hoạch và lý do đầy đủ ở `docs/superpowers/plans/2026-08-07-phase2-pipeline-va-gate.md`.
Quy ước dùng hàng ngày ở `CLAUDE.md`. Tóm tắt để biết cái gì nằm đâu:

```
pipeline/
├── orchestrator.py   một lệnh chạy trọn sáu bước, ba checkpoint ghi artifact
├── build_html.py     markdown + sổ nguồn -> một file HTML tự đủ
├── render_pdf.py     WeasyPrint, và tự mở lại file kiểm ngay sau khi ghi
├── bake_svg.mjs      đóng băng callout của annotate.js thành SVG tĩnh
└── report.css        trang giấy: khổ, lề, chạy đầu chân trang, ba kiểu bìa

gates/
├── run.mjs           runner, in bảng, trả exit code
├── gates.mjs         mười gate, mỗi gate một hàm thuần để test gọi thẳng
├── pdf_checks.py     mọi phép đo trên PDF nhị phân, gọi một lần dùng chung
└── fixtures/         cặp đỏ và xanh cho từng gate

examples/mau-phase2/  báo cáo mẫu 6 trang, chạm cả hai engine chart và một minh hoạ
```

Một lệnh chạy hết: `npm run mau`.

## Bốn thứ Phase 2 tìm ra, đều đo được bằng số

1. **Callout của minh hoạ mất sạch trong PDF.** `annotate.js` vẽ bằng JavaScript lúc chạy,
   WeasyPrint không chạy JS. Bản gốc con tàu qua WeasyPrint cho 42 nét vẽ và 0 trên 7
   callout; bản đã bake cho 74 nét vẽ và đủ 7. Bug lớp thứ tư cùng họ với ba lớp cũ, đã
   sống trong repo suốt Phase 1.
2. **Tầng text không phân biệt được font đúng với font hệ thống.** Cùng một trang, bản có
   `@font-face` cho `Spectral`, bản bỏ `@font-face` cho `Noto-Serif`. Cả hai đều 0 FFFD,
   0 ký tự synthetic, tầng text đúng dấu y hệt. Gate 2 FONT-PDF sinh ra từ đây.
3. **Callout khai `'Be Vietnam Pro'`, một font repo không nhúng.** Mọi callout đang in
   bằng font hệ thống. Đã vá `annotate.js` sang `'IBM Plex Sans'`.
4. **Trục giá trị in `1,200` thay vì `1.200`.** Mặc định của ECharts, ảnh hưởng mọi preset
   không tự truyền formatter. Đã vá `valueAxis` trong `theme.mjs`.

## Ba cái bẫy của tầng trang giấy, đã cắn thật

- `string-set: content()` đặt lên `body` biến toàn bộ văn bản thành chuỗi chân trang, và
  WeasyPrint in nguyên khối đó tràn đè lên cả trang.
- `.bao-cao h1 { color: var(--ink) }` đè màu kế thừa từ `.bia`, cho ra chữ ink trên nền
  ink. Tiêu đề biến mất khỏi bìa mà vẫn nguyên trong tầng text.
- `name` của `valueAxis` đè lên `title.subtext` vì cả hai đóng ở đỉnh trục.

## Một việc nhỏ còn nợ, làm kèm lúc nào cũng được

- Bảng số liệu đi kèm đường cong là ràng buộc cứng của đặc tả nhưng thuộc tầng HTML, chart
  không tự lo được. Mọi báo cáo dùng `c_yield_curve` phải ghép thêm `12-hairline-data-table`.

Hai việc còn lại của mục này đã đóng ở đợt dọn 07-08: schema nay có trường `do_tin_cay` riêng
ở cấp điểm, và từ vựng có đủ `usd_thung` cùng `usd_oz` nên `c_futures_curve` không phải bỏ
phép kiểm đơn vị nữa.

## Chạy được từ máy sạch

```bash
cd ~/HT-viz-rendering
npm install
npm run setup:browser      # BUOC RIENG, playwright-core khong tu tai browser
pip install --break-system-packages -r requirements.txt
npm test && npm run verify && python3 -m pytest tests/ -v
```

Không cần cài font hệ thống: bản HTML nhúng base64 trong `design-system/fonts/fonts-embedded.css`,
chart matplotlib đọc `design-system/fonts/ttf/` (6 face, 404KB, đã commit). Sinh lại bằng
`python3 design-system/fonts/extract-ttf.py`, script này trích ngược từ chính file CSS kia nên
chạy offline. Phải có bản `.ttf` riêng vì matplotlib không đọc được woff2.

Mọi chỗ mở Chromium đều đi qua `scripts/lib/chromium.mjs`, tức hỏi thẳng `playwright-core` xem
bản nào khớp phiên bản thư viện. Trước đợt dọn, `verify-illustrations.mjs` và `deps.test.mjs`
hardcode `chromium-1228` còn `verify-components.mjs` tự dò bản mới nhất, nên `npm run verify`
nghiệm thu bằng hai binary khác nhau trong cùng một lần chạy, và trên máy sạch thì chết ENOENT.
Có gate trong `deps.test.mjs` chặn tái phạm: nó quét `scripts/` và `tests/` tìm đường dẫn cache
hardcode lẫn lời gọi `launch()` trực tiếp.

## Repo này là gì

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF
in được, có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG
neo được số liệu vào từng bộ phận vật thể.

Thiết kế đầy đủ ở `docs/specs/2026-08-06-ht-viz-rendering-design.md`, 15 mục. Đọc mục 3 (bảng
quyết định đã chốt) và mục 5 (kiến trúc) trước khi động vào code. Quy ước làm việc chi tiết ở
`CLAUDE.md`, cổng vào cho Claude là `SKILL.md`.

## Ba phán quyết của người dùng ở đợt dọn sau Phase 1

1. **`viz_render_py.py`: XOÁ.** Nó mang bảng màu giấy ngà ấm đã bị bác và không file nào import.
   Hệ quả phải biết: repo không còn 10 primitive lõi (bar_grouped, line, waterfall, scatter,
   heatmap, donut, slope, payoff, bar_h, bar_stacked) ở đường matplotlib. Tương đương gần nhất
   trong 48 component EIR là comparison, index100, flow_bridge, comps_scatter, correlation_matrix,
   distribution. Bản gốc vẫn nằm ở `_harvest/harvest-cfa-skillchain/viz-engine/viz_render_py.py`
   nếu cần port lại sang bảng màu lạnh.
2. **Hệ màu tối: GIỮ cho trang nội bộ, KHOÁ SÁNG cho file giao đi.** ĐÃ SỬA MỘT PHẦN ở cú bẻ lái
   07-08, đọc kỹ vì luật này có HAI TẦNG và chúng có số phận khác nhau.

   *Tầng quyết định*: đã mở. `data-theme` nay là tham số `--chu-de` chứ không còn ghi cứng trong
   f-string của `lap_trang()`.

   *Tầng nợ tài sản*: **VẪN NGUYÊN, và người dùng mở bảng màu KHÔNG trả hộ được.** Lý do đo được
   ban đầu là chart matplotlib và minh hoạ SVG chỉ có bảng màu sáng, nên máy khách đặt theme tối
   cho ra trang nền `#0A1420` mà chart vẫn nền trắng. Đó là sự thật về mã nguồn, không phải về
   khẩu vị. Vì vậy **mặc định vẫn là `light`** cho tới khi trả xong nợ ở Phase 3.

   Gate `khoa-sang-khong-doi-theo-may-khach` phải viết lại: nó chỉ đọc
   `getComputedStyle(document.body)` nên KHÔNG nhìn thấy chart hay minh hoạ, tức không có khả
   năng phát hiện đúng cái bệnh mà luật này sinh ra để tránh.
3. **`.q-dot`: vá cả hai lỗi cùng một rule.** Thêm `display: inline-block` cho hết méo, và thay
   `box-shadow` chết bằng `::before` vẽ vòng tròn thật.

## Ba thuộc tính CSS mà WeasyPrint bỏ qua

Khối ma trận 2x2 dính cả ba cùng lúc, tưởng là một lỗi bố cục hoá ra là ba lỗi độc lập. Bảng
đầy đủ ở `CLAUDE.md`, tóm tắt:

| Thuộc tính | WeasyPrint làm gì | Đã thay bằng |
|---|---|---|
| `aspect-ratio` | Bỏ qua, khối cao 0 | `height: 438px` |
| `overflow`/`clip` trên `<table>` | Bỏ qua, bảng vẫn in ra | Bọc trong `<div class="visually-hidden">` |
| `writing-mode` | Bỏ qua nhưng vẫn áp `transform` | `rotate(-90deg) translateX(-100%)` |
| SVG không hợp lệ XML | Bỏ qua CẢ FILE, im lặng | Tên font bọc nháy đơn trong `theme.mjs` |

**Bẫy nặng nhất tìm được, và nó sống sót trọn Phase 1**: cả 12 chart ECharts xuất ra SVG **không
phải XML hợp lệ**, vì `FONT_STACK` bọc bằng nháy kép rồi bị ECharts nhúng vào thuộc tính
`style="..."`. WeasyPrint bỏ qua cả file, PDF ra 0 nét vẽ, chart biến mất sạch. Trình duyệt vẫn
hiện đúng nên soi bản HTML không bao giờ thấy, và mọi gate cũ chỉ đếm chuỗi chứ không parse. Đã
vá `theme.mjs`, thêm gate parse XML vào `verify-charts.mjs`, kiểm là gate đỏ được khi phá ở nguồn.
Bài học chung: **một gate đếm được không thay được một gate PARSE**.

Cách tìm ra: dựng ca tối giản đã biết là đúng rồi thêm từng yếu tố. Bốn biến thể đầu (grid lồng
grid, absolute inset 0, left/top phần trăm, translate âm) đều ĐÚNG, nên nghi can ban đầu bị loại
hết. Yếu tố thứ năm mới làm vỡ. Bài học lặp lại lần thứ tư trong repo: đoán nguyên nhân theo
trực giác thì trật, cô lập từng yếu tố thì trúng.

Cả ba đều có test chặn tái phạm, và cả ba test đã được kiểm là ĐỎ ĐƯỢC khi tái tạo lỗi.

## Bảy điều đã đo được, đừng làm lại

1. **Chỉ `box-shadow` có blur mới bị nướng bitmap khi in.** Offset cứng blur 0 an toàn tuyệt đối.
   Đo bằng ba biến thể độc lập. Ngoài ra WeasyPrint không render box-shadow bằng bất kỳ cú pháp
   nào, nên bóng chỉ tồn tại trên trình duyệt.
2. **`@media (max-width: Npx)` thiếu `screen` tự kích hoạt khi in**, vì vùng in A4 chỉ 688 tới
   717px sau margin.
3. **Bug rớt dấu tiếng Việt không do engine** mà do khai `font-family` bằng một tên trần thay vì
   list kết thúc generic keyword. Lỗi ra dạng "Sô´liệu" chứ không phải ô vuông nên rất dễ lọt QC.
4. **Đo dấu tiếng Việt phải dùng mực chữ qua Canvas `measureText()`**. So
   `getBoundingClientRect().height` với `fontSize × lineHeight` là tautology, không bao giờ phát
   hiện được lỗi. Gate `offline-body-dung-font-nhung` dùng đúng phép này.
5. **Dấu tiếng Việt chỉ giảm 4% ký tự mỗi dòng**, không cần buffer line-height kiểu CJK.
6. **`echarts.init` với `ssr:true` không tự thoát process.** Mọi script chart phải kết bằng
   `chart.dispose(); process.exit(0);`.
7. **Đếm ảnh trong PDF phải dùng `doc.xref_object`**, `get_images()` bỏ sót ảnh trong Tiling Pattern.
8. **`color-mix()` không render trong WeasyPrint 69.0**, ra 0 fill. Viết `rgb(R G B / A)` thay thế.
9. **`outline` không bo theo `border-radius` trong WeasyPrint**: đặt outline lên một chấm tròn thì
   ra khung vuông. Đã thử và loại khi vá `.q-dot`.

## Bốn cái bẫy đã gặp thật, đừng lặp lại

- **Catalog drift**: bộ Opvia có file catalog mô tả HTML dùng class không tồn tại trong CSS. Trang
  vẫn chạy nhưng suy biến âm thầm. `tests/consistency/catalog_drift.test.mjs` chống đúng bệnh này.
- **PACKAGE tự nhận là tự đủ**: cả hai PACKAGE chạy được ở thư mục gốc của chúng nhưng
  `ERR_MODULE_NOT_FOUND` khi copy sang chỗ khác.
- **Verify script chọn class không tồn tại**: script verify báo PASS mà chưa kiểm gì.
- **Gate xanh vì phép đo rỗng**: ba ca đã gặp và đã vá ở đợt dọn. `reduced-motion` cũ chỉ hỏi
  Playwright xem Playwright có làm đúng việc của Playwright không, luôn true kể cả khi CSS không
  có dòng nào. `offline-fonts-available` cũ dùng `.every(Boolean)` trên mảng rỗng nên trang không
  khai font nào vẫn xanh. Regex quét `SKILL.md` mở bằng `[a-z]` nên chưa bao giờ kiểm `CLAUDE.md`
  và `README.md`. Cách chữa chung: mỗi gate phải chứng minh được nó PHÂN BIỆT ĐƯỢC hai trạng thái
  trước khi được quyền xanh, và phải tự đỏ được khi cố tình phá.

## Hai xung đột đã phân xử, đừng mở lại

- **Gauge và radar**: cấm. Gauge gợi ý độ chính xác không có thật, radar có trục không độc lập.
  Đây là lý do ĐÚNG SAI PHÂN TÍCH, không dính gì môi trường xuất bản, nên nó sống qua mọi tiền
  đề. Bảy mục trong nghiên cứu là radar cải trang và bị loại theo: `radviz`, `star-coordinates`,
  `dust-and-magnet`, `star-glyph`, `shape-coding`, `progress-ring`, `wind-rose`.
- **Engine PDF**: WeasyPrint, không phải Chromium. Chromium tạo ảnh JPEG ẩn trong Tiling Pattern.
  Đã cân lại một lần nữa ở cú bẻ lái 07-08 và người dùng CHỐT GIỮ.

**Bảng màu đã RỜI khỏi danh sách này.** Nó từng chốt trắng lạnh chứ không phải giấy ngà ấm, và ba
nguồn độc lập hội tụ ủng hộ nó vẫn là bằng chứng tốt. Nhưng ngày 07-08 người dùng chủ động mở:
trắng lạnh nay là MẶC ĐỊNH chứ không phải hằng số. Cái mất là quyền phủ quyết một bảng màu khác,
không phải cái mất về bằng chứng.

## Đợt dọn sổ nợ 07-08, và cái bẫy nó tự tạo ra

Năm món nợ đã đóng: em-dash trong tài liệu và comment, thư mục `charts/echarts/out/` rỗng,
`verify-illustrations.mjs` quy lỗi theo chuỗi con, ba nợ schema chart, bảng markdown thiếu
ô gộp và caption.

**Bài học đắt nhất của đợt này**: phép dọn gạch ngang hàng loạt đã đổi chính hai ký tự nằm
bên trong character class của hai gate chặn em-dash, biến chúng thành `/[--]/g`. Regex đó
chỉ còn khớp dấu gạch nối thường, tức gate báo FAIL cho mọi nội dung bình thường và không
còn bắt em-dash, mà vẫn chạy trơn tru không báo gì. **Một phép dọn hàng loạt có thể vô
hiệu hoá đúng cái gate canh nó.** Nay hai regex đó viết bằng escape unicode, và luật
em-dash chuyển thành tuyệt đối cho toàn repo chính, có gate riêng ở
`tests/consistency/em_dash_repo.test.mjs` miễn trừ đúng hai chỗ tường minh.

Ba việc khác đáng ghi: `verify-illustrations.mjs` nay trích đường dẫn từ từng frame stack
rồi so basename, đúng cách phía network vẫn làm, nên không còn quy oan cho lớp annotation
mọi lỗi phát sinh trong file tên kiểu `annotate-demo.js`. Schema chart có trường
`do_tin_cay` riêng ở cấp điểm, tách khỏi `source.tier` ở cấp series, cộng hai đơn vị
`usd_thung` và `usd_oz`. Bảng markdown hỗ trợ ô gộp cột và `<caption>`, và ở đây cũng có
một bẫy nhỏ: `strip("|")` của Python bỏ NHIỀU pipe liên tiếp, nên hàng kết thúc bằng ô gộp
bị mất một cột mà bảng vẫn hiện ra bình thường.

## Mục lục thư viện, để phiên sau không phải dò lại

`catalog/CATALOG.md` liệt kê cả 108 tài sản dưới một dạng, mỗi dòng ghi mã, trả lời câu
hỏi gì, và khi nào đừng dùng. `catalog/INDEX.json` là bản máy đọc. `catalog/contact-sheet.pdf`
là 50 bản xem trước để nhìn cả kho một lượt. Cả ba sinh tự động bằng
`scripts/sinh_catalog.py`, `scripts/sinh_xem_truoc.py` và `scripts/sinh_contact_sheet.py`,
có test ép khớp mã nguồn nên không trôi được.

Dựng chúng đòi lấp một lỗ hổng thật: **50 trên 50 component matplotlib không có mô tả nào
dùng được**, 28 cái không có lấy một dòng docstring. Nay cả 50 đều ghi rõ trả lời câu hỏi
gì, cần dữ liệu gì, và khi nào KHÔNG nên dùng.

Hai lỗi bắt được nhờ chính contact sheet, cả hai đều nằm sẵn trong thư viện từ trước:

- **`c_sensitivity_grid` và `c_correlation_matrix` dùng `imshow`**, tức nhúng một ảnh
  BITMAP vào SVG. Báo cáo nào dùng hai component đó đều sẽ vi phạm luật vector và bị gate
  RASTER chặn. Đo được: bản cũ cho một ảnh 1216x511 trong PDF. Đã thay bằng `Rectangle` và
  `axvspan`, nay 0 ảnh.
- **CSS Grid phân trang rất tệ trong WeasyPrint**: mỗi hàng grid bị đẩy sang một trang
  mới, 29 ô ra 9 trang với hai phần ba mỗi trang bỏ trống. `inline-block` phân trang bình
  thường. Kèm hai chi tiết nhỏ: ba ô `32,4% + 1,4%` cộng lại vượt 100% nên mỗi hàng chỉ
  chứa hai ô, và SVG không khai `width`/`height` thì không co theo ô mà giữ nguyên cỡ px
  của viewBox.

## Sổ nợ, chưa chặn ai

- Em-dash trong `_harvest/` giữ nguyên, đó là bản gốc để còn đối chiếu. Repo chính đã sạch
  tuyệt đối và có gate ép giữ vậy.

- `_harvest/` vẫn còn 57MB. Phase 2 đã dỡ `lab-gate/` và `lab-evidence/` vào `gates/`;
  `harvest-extras/pipeline-stocklpt/` chưa dỡ, chỉ mới đọc để tham khảo cách dựng markdown.
- Nhánh PPTX chưa làm. Operator chốt Phase 2 chỉ lo đường HTML sang PDF. Hai bug đã biết của
  `html2pptx.js` (SVG làm crash cả file, bảng mất trắng) vẫn nằm nguyên trong `_harvest/`.
- 18 preset ECharts vẫn là script hardcode dữ liệu demo, chưa có bề mặt gọi được với dữ liệu
  thật. Báo cáo hiện chép preset vào `hinh/` của mình rồi thay số, và cách đó đúng tinh thần
  "preset là ý tham khảo" nhưng chưa tiện. Cân nhắc ở Phase 3.
- Bảng markdown chưa hỗ trợ ô gộp HÀNG (`rowspan`), mới chỉ gộp cột. Chưa gặp bài cần tới.
- 29 trên 50 component matplotlib chưa có bản xem trước, vì chúng không có bộ tham số ví
  dụ trong `spec_showcase.json`. Contact sheet liệt kê tên chúng kèm lý do thay vì để ô
  trống. Thêm ví dụ cho chúng là việc còn lại.
- `c_sensitivity_grid` dùng bảng màu ấm `_cmap_warm()` trong khi repo đã chốt bảng màu
  lạnh. Chưa đụng vì nó nằm ngoài phạm vi đợt này.

## Các phase sau, ĐÃ ĐỊNH NGHĨA LẠI theo cú bẻ lái

Viết plan riêng khi phase trước nghiệm thu xong.

**Phase 3 nay là TRẢ NỢ NỀN, không phải xây tính năng.** Người dùng đã chốt thứ tự này. Chi tiết
ở mục đầu file. Tóm tắt: generator chủ đề từ JSON, migrate 345 hex minh hoạ, 29 chỗ `color=PAPER`
sang `ON_INK`. Xong ba việc đó thì mỗi chủ đề mới chỉ còn khoảng 5 file thay vì 17.

**Phase 4: dựng làn `html-song` cho chạy được.** Tách `option()` khỏi `render` trong ECharts để
một nguồn preset phục vụ cả hai làn, cộng bundle tree-shaken. Đã ĐO THẬT: bundle qua
`echarts/core` nặng 733KB thô so với 1,1MB của bản đầy đủ, giảm 371KB tức 33% trên mọi file làn
A, và nghiệm thu bằng render thật sankey 31/31, treemap 48/48, candlestick 49/49 nét vẽ, giống
hệt engine đầy đủ và trùng khớp file `.svg` đang commit. Danh sách đủ cho cả 18 preset: 8 Chart
(`bar/line/scatter/custom/heatmap/sankey/treemap/candlestick`), Component
(`grid/tooltip/title/legend/graphic/markLine/markPoint/markArea/visualMap`), Feature
`labelLayout`, chỉ `SVGRenderer`.

**Phase 5: bộ gate làn A.** Chín gate mới, mỗi cái đã có phép đo và mô tả fixture đỏ:
`OFFLINE-INTACT`, `JS-SILENT-FAIL`, `REDUCED-MOTION`, `KEYBOARD-PATH`, `CONTRAST-ALL-THEMES`,
`SIZE-BUDGET`, `NO-JS-CONTENT`, `RESPONSIVE-WIDTH`, `THEME-MATCH`. Đặc tả đầy đủ ở memory toàn
cục. Hai gate đã cân và LOẠI vì không dựng nổi fixture đỏ tất định: "mượt 60fps" và "trang phải
đẹp".

**Phase 6: báo cáo mẫu vận tải biển**, nghiệm thu bằng bộ gate của đúng làn nó chọn.

Mười gate cũ KHÔNG chết: cả mười sống nguyên cho làn `pdf-so`, chỉ `report.css` đổi khổ trang và
tầng 2 của gate 5 phải trỏ đúng cặp file. Cộng bốn gate mới chỉ digital PDF mới có:
`HYPERLINK-LIVE`, `BOOKMARK-OUTLINE`, `PAGE-RATIO`, `MIN-FONT-SCREEN`.
