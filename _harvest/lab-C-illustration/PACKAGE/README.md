# HT-viz-rendering — minh hoạ ngành bằng SVG tay + lớp chú thích

Module này giải quyết một việc cụ thể: **báo cáo ngành X cần một hình vẽ
tay (con tàu, nhà máy, ngân hàng...) rồi neo số liệu thật lên đúng bộ phận
của hình đó** — không phải icon trang trí, không phải ảnh AI-gen (đẹp hơn
nhưng không sửa được, không gắn callout được, xem "So sánh với ảnh AI-gen"
bên dưới). Tài liệu này viết cho một Claude (hoặc người) CHƯA biết gì về dự
án — đọc xong là dùng được ngay, không cần hỏi lại.

## Nó gồm những gì

```
PACKAGE/
├── illustrations/        11 file .svg — minh hoạ ngành, KHÔNG có callout (file "sạch")
├── annotate.js            module JS gắn callout runtime lên 1 SVG đã nhúng vào HTML
├── annotate.css           style cho "drill card" (thẻ chi tiết khi click callout)
├── examples/              3 file HTML CHẠY ĐƯỢC minh hoạ cách gọi annotate.js
├── gen-vietnam-path.mjs   script sinh path bản đồ từ dữ liệu địa lý thật (không tay-gõ)
├── verify-path-lengths.mjs   đo thật độ dài leader-line, gate CI được (exit code)
├── verify-label-bounds.mjs   đo thật hộp nhãn có tràn viewBox không, gate CI được
├── grammar.md             NGỮ PHÁP VẼ — đọc TRƯỚC KHI vẽ minh hoạ mới
├── metaphor-table.md       bảng tra: ngành/luận điểm nào → vẽ vật gì
├── prompt-template.md      prompt dán nguyên khối để vẽ 1 minh hoạ ngành MỚI
└── README.md              (chính là file này)
```

## 30 giây: đây là 2 thứ tách biệt

1. **`illustrations/*.svg`** — hình vẽ tay, viewBox chuẩn, không có số liệu
   bên trong, dùng LẶP LẠI được cho nhiều báo cáo khác nhau. Đổi màu theo
   ngành bằng 1 biến CSS `--accent` đặt trên thẻ `<svg style="--accent:#...">`.
2. **`annotate.js`** — module JS chèn callout (chấm neo + đường dẫn + hộp
   nhãn + thẻ chi tiết khi click) vào 1 bản SVG **đã nhúng vào trang HTML**
   (không chèn được vào file `.svg` đứng một mình — phải là SVG inline
   trong DOM của 1 trang HTML, vì module dùng `document.createElementNS`).

Quy trình dùng thật cho 1 báo cáo: mở 1 file `.svg` trong `illustrations/`,
**copy-paste TOÀN BỘ nội dung `<svg>...</svg>`** (không phải `<img src=...>`
— phải là SVG *inline*) vào giữa `<body>` của trang HTML báo cáo, gán `id`
cho nó, rồi gọi `Annotate.annotate(svgElement, [...])` với số liệu thật của
báo cáo đó.

## Cách render ra PNG để tự kiểm bằng mắt

Không có công cụ xem SVG/HTML trực tiếp bằng mắt trong hầu hết harness LLM
— phải render ra PNG rồi dùng công cụ đọc ảnh (Read tool, hoặc tương
đương). Dùng `playwright-core` (KHÔNG cần cài `playwright` đầy đủ, chỉ cần
gói `-core` + trỏ tới 1 bản Chromium đã tải sẵn trên máy):

```js
import { chromium } from "playwright-core";
const browser = await chromium.launch({
  executablePath: "/đường/dẫn/tới/chrome-linux64/chrome", // vd ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome
  headless: true,
});
const page = await browser.newPage();
await page.goto("file://" + đường_dẫn_tuyệt_đối_tới_file.html, { waitUntil: "networkidle" });
await page.screenshot({ path: "out.png", fullPage: true });
await browser.close();
```

Nếu máy chưa có Chromium cache sẵn: `npx playwright install chromium` (tải
~150MB), rồi tìm đường dẫn bằng `find ~/.cache/ms-playwright -name chrome
-type f` (Linux) hoặc thư mục tương ứng trên hệ điều hành khác. `annotate.js`
dùng `document.createElementNS` và `getBoundingClientRect` — chạy được
trong Chromium headless bình thường, không cần GPU.

Cả 2 script `verify-*.mjs` trong gói này (xem mục dưới) đã tự làm việc
render+đo, không cần viết lại — copy cách chúng mở Chromium nếu cần một
script mới.

## `annotate.js` — API đầy đủ

```js
Annotate.annotate(svgElement, items, opts);
```

`svgElement`: phần tử `<svg>` **đã có `viewBox`** và đã nằm trong DOM
(không cần đã render xong, nhưng phải `document.getElementById(...)` lấy
được).

`items`: mảng object, mỗi object là 1 callout:

```js
{
  anchor: [x, y],           // toạ độ điểm neo TRÊN VẬT THỂ, hệ toạ độ = viewBox của svg
  label: { x, y },          // toạ độ MONG MUỐN của nhãn — ý nghĩa của x/y phụ thuộc axis, xem bên dưới
  head: "475 TỶ USD",       // dòng tiêu đề, in đậm
  sub: "Container = kim ngạch xuất khẩu 2025",   // dòng phụ, tự động xuống dòng tối đa 2 dòng
  tone: "neutral",          // 'neutral' | 'negative' | 'accent' — XEM LUẬT MÀU bên dưới, bắt buộc đọc
  drill: {                  // optional — nếu có, callout click được để mở thẻ chi tiết
    title: "HÀNG HOÁ TRÊN BOONG",
    value: "475 tỷ USD",
    sub: "Tổng giá trị xuất khẩu ước tính đi qua đường biển.",
    source: "Tổng cục Hải quan, 2026",
  },
}
```

`opts` (tất cả optional):

| key | mặc định | ý nghĩa |
|---|---|---|
| `avoidBox` | `null` | `{x,y,width,height}` — bbox (hệ toạ độ viewBox) của vật thể chính. **Luôn truyền** cho hình có mật độ chi tiết cao (tàu, nhà máy, tháp...); có thể bỏ qua cho hình rất thưa (phễu, cán cân). Không truyền = leader-line có thể cắt qua vật thể. |
| `axis` | `'vertical'` | `'vertical'` \| `'horizontal'` — xem mục "Hai mode axis" bên dưới, **bắt buộc hiểu đúng trước khi gọi** |
| `minGap` | `14` | khoảng cách tối thiểu giữa 2 hộp nhãn liền kề (px, hệ toạ độ viewBox) |
| `boxPad` | `10` | padding trong hộp nhãn |
| `headSize` / `subSize` | `13` / `10.5` | cỡ chữ (px) |
| `maxSubChars` | `34` | số ký tự tối đa mỗi dòng phụ trước khi tự xuống dòng |

Trả về: phần tử `<g class="annotations">` vừa tạo (gọi lại `annotate()`
trên cùng svg sẽ tự xoá bản cũ trước khi vẽ bản mới — đổi bộ số liệu không
cần tự dọn dẹp).

### Luật màu cho `tone` — CHỈ 3 GIÁ TRỊ, đọc kỹ trước khi dùng

Đây là luật đã bị vi phạm 1 lần trong quá trình xây module này (bản đầu có
5 tone, 7 callout dùng hết 5 màu viền khác nhau trên 1 hình — "traffic-light
hoá", operator bác thẳng) nên nhắc lại ở đây, không chỉ trong code comment:

- **`neutral`** (mặc định) — dùng cho HẦU HẾT callout, thông tin thường.
- **`negative`** — CHỈ dùng cho callout mang tin xấu/rủi ro thật (chi phí
  vượt ngưỡng, tỷ lệ trả hàng cao, rủi ro tín dụng...). Không dùng cho tin
  tốt — tin tốt cũng để `neutral`, KHÔNG có tone "tích cực" riêng.
- **`accent`** — CHỈ dùng cho **ĐÚNG 1 callout mỗi hình**, con số quan
  trọng nhất/đại diện nhất. Module không ép được số lượng này bằng code
  (không có gì ngăn bạn đặt `tone:'accent'` cho 5 callout) — đây là kỷ
  luật của người gọi, **tự đếm lại bằng mắt trước khi giao** báo cáo.

Nếu thấy mình cần nhiều hơn 3 mức phân loại (vd muốn phân biệt "cảnh báo
nhẹ" khác "rủi ro nặng"), đừng thêm tone mới — dùng chữ trong `sub` để diễn
đạt mức độ, giữ hệ màu tối giản.

### Hai mode `axis` — chọn đúng theo TỶ LỆ KHUNG của minh hoạ, không phải theo sở thích

Đây là 2 chiến lược bố cục callout HOÀN TOÀN KHÁC NHAU, không dùng chung
được cho cùng 1 hình:

**`axis: 'vertical'`** (mặc định) — dùng khi vật thể CAO/DÀY ĐẶC chiếm gần
hết chiều cao khung (tàu, nhà máy, tháp căn hộ...). Nhãn xếp thành 2 CỘT
DỌC ở lề TRÁI và PHẢI (quyết định cột nào dựa vào `label.x` so với giữa
khung). `label.y` = TÂM DỌC mong muốn của hộp — module tự nắn (dời) `y` này
ra khỏi dải y bận của `avoidBox` nếu cần, rồi giải va chạm để không hộp nào
chồng nhau theo chiều dọc. Xem `examples/example-vertical-axis-ship.html`.

**`axis: 'horizontal'`** — dùng khi vật thể nằm trong 1 DẢI NGANG Ở GIỮA
khung, viền TRÊN và DƯỚI để trống (bố cục kiểu banner biên tập/bìa tạp
chí — object chiếm gần hết BỀ NGANG nhưng chỉ 1 phần BỀ CAO ở giữa). Nhãn
xếp thành 2 HÀNG NGANG ở TRÊN và DƯỚI (quyết định hàng nào dựa vào
`anchor[1]` — toạ độ y của điểm neo — so với giữa `avoidBox`). `label.x` ở
đây là **TÂM NGANG** của hộp (khác nghĩa với mode 'vertical', ở đó `label.x`
là CẠNH của hộp) — dễ nhầm, đọc lại code trong `examples/example-horizontal-axis-banner.html`
nếu không chắc. Bố cục này vay mượn từ 1 kho ảnh AI-gen khác (xem mục "So
sánh với ảnh AI-gen") có ràng buộc "đặt chủ thể trong dải ngang giữa khung,
để trống viền trên/dưới cho tiêu đề đè lên".

**KHÔNG có mode tự động phát hiện** — người gọi phải tự biết minh hoạ của
mình thuộc dạng nào (nhìn tỷ lệ viewBox: cao/hẹp → 'vertical'; ngang/thấp
với object ở giữa → 'horizontal') và truyền đúng `axis`. Trong 11 file ở
`illustrations/`, 9 file dùng bố cục "tràn khung" phù hợp mode 'vertical'
(hoặc không cần callout dày như phễu/cán cân); chưa có file nào trong
`illustrations/` được thiết kế sẵn theo bố cục "dải giữa" — muốn dùng mode
`'horizontal'`, phải tự bố trí lại 1 minh hoạ theo kiểu
`examples/example-horizontal-axis-banner.html` (đặt object trong 1
`<g transform="translate(...)">` ở giữa khung, KHÔNG vẽ nền đất/trời tràn
viền).

### Ràng buộc cứng đã code (không cần tự kiểm tay, nhưng NÊN tự đo lại bằng script)

- **Leader-line không dài quá 1.6× khoảng cách thẳng** neo→nhãn — đạt bằng
  hình học (tuyến gấp khúc 1 góc vuông bo tròn nhẹ luôn ≤ √2≈1.414×), không
  phải dò từng trường hợp. Đo lại bằng `verify-path-lengths.mjs` (xem dưới).
- **Hộp nhãn luôn nằm trọn trong viewBox** — nếu vị trí tính ra bị tràn,
  module tự thu hẹp bề rộng hộp trước (đến tối thiểu 90px), rồi mới dịch cả
  hộp vào trong nếu vẫn chưa đủ. Đo lại bằng `verify-label-bounds.mjs`.
- **Leader-line không cắt qua vật thể chính** (khi có truyền `avoidBox`) —
  bằng cách buộc nhãn (mode vertical) hoặc hàng nhãn (mode horizontal) luôn
  ở vùng trống trước khi vẽ đường, rồi chỉ nối 1 góc vuông. Không có script
  đo tự động cho tiêu chí này (khó đo bằng hình học đơn giản như 2 cái
  trên) — tự kiểm bằng mắt qua ảnh render.

## Chạy 2 script tự kiểm (`verify-*.mjs`)

Cả hai cần `playwright-core` (npm install nếu chưa có) và biến môi trường
`CHROME_PATH` trỏ tới Chromium (mặc định code trỏ tới 1 đường dẫn cụ thể
của máy phát triển — **gần như chắc chắn phải đổi trên máy khác**, xem mục
"3 việc còn để ngỏ" bên dưới).

```bash
npm install playwright-core   # nếu chưa có sẵn trong node_modules gần đó

CHROME_PATH=/đường/dẫn/chrome node verify-path-lengths.mjs examples/example-vertical-axis-ship.html ship-svg
CHROME_PATH=/đường/dẫn/chrome node verify-label-bounds.mjs examples/example-vertical-axis-ship.html ship-svg
```

Tham số: `<file.html> [id-svg] [margin (chỉ verify-label-bounds, mặc định 8)]`.
Không truyền `id-svg` thì lấy `<svg>` đầu tiên trong trang. Cả 2 thoát
bằng exit code 1 nếu vi phạm — gắn được vào CI/gate.

## Vẽ 1 minh hoạu ngành MỚI (chưa có trong `illustrations/`)

1. Đọc `metaphor-table.md` — tra xem ngành/luận điểm cần vẽ nên dùng ẩn dụ
   vật lý gì (hoặc tự nghĩ ẩn dụ mới theo 5 nguyên tắc "khi nào không nên
   dùng ẩn dụ" ở cuối file đó).
2. Đọc `grammar.md` toàn bộ — đặc biệt mục 3 (ngưỡng số lượng shape), mục 4
   (luật màu — KHÁC luật màu của `tone` ở trên, đây là luật màu CHO BẢN
   THÂN HÌNH VẼ), mục 5 (tỷ lệ), mục 7 (cấm tuyệt đối: filter/gradient
   nhiều stop/clipPath lồng/mask/ảnh raster — lý do kỹ thuật cụ thể, không
   phải sở thích thẩm mỹ).
3. Copy khối prompt trong `prompt-template.md`, điền 4 chỗ trống, tự vẽ
   file `.svg` theo đúng khung bắt buộc ở quy tắc 9.
4. Render ra PNG (xem mục "Cách render" ở trên), TỰ NHÌN ảnh, đánh giá thật
   thà theo bước 10 trong prompt-template.md. Lặp lại tới khi đạt — ghi lại
   số vòng lặp thật khi báo cáo, đừng làm tròn hay tự nhận PASS ngay vòng 1
   nếu thực tế phải sửa.
5. Nếu minh hoạ cần vẽ theo dữ liệu địa lý/hình học có sẵn nguồn công khai
   (bản đồ, ranh giới, mạng lưới...) — KHÔNG tay-gõ toạ độ, viết script
   theo mẫu `gen-vietnam-path.mjs` (đổi `COUNTRY_ID` hoặc nguồn dữ liệu).

## `gen-vietnam-path.mjs` — sinh hình học thật, không tay-gõ

```bash
npm install d3-geo topojson-client topojson-simplify world-atlas
node gen-vietnam-path.mjs                        # mặc định SIMPLIFY_WEIGHT=0.05 (~72 điểm)
SIMPLIFY_WEIGHT=0.02 node gen-vietnam-path.mjs    # chi tiết hơn (~118 điểm)
COUNTRY_ID=764 node gen-vietnam-path.mjs          # đổi sang nước khác (764=Thái Lan, tra mã ISO numeric)
```

In path `d` ra `stdout`, log tiến trình + toạ độ 3 mốc thành phố ra
`stderr`, ghi thêm `vietnam-path-raw.txt` cạnh script. Dán `d` vào 1
`<path>` trong SVG, dán toạ độ thành phố vào `<circle cx cy>`.

**Bài học quan trọng nếu viết script tương tự cho dữ liệu khác**: đã thử
`SIMPLIFY_WEIGHT` từ `0.0000012` (gần như không đổi, còn ~550 điểm, quá
dày cho 1 icon) tới `0.1` (còn ~50 điểm, hơi thô). `0.05` (~72 điểm) là
điểm cân bằng đã chọn sau khi so sánh trực tiếp 3 mức — xem
`examples/vietnam-simplification-comparison.html`. Không có công thức tính
sẵn ngưỡng này, phải thử-nhìn-chọn cho mỗi bộ dữ liệu mới.

## Bảng màu thay thế "editorial" (cream/navy/teal/gold)

`grammar.md` mục 4 có ghi 1 bảng màu thay thế mượn từ 1 kho ảnh AI-gen
khác (cream `#F5EFE2` / navy `#16283F` / teal `#2F7E7A` / gold `#C9A227`),
dùng khi báo cáo cần cảm giác "1 ấn phẩm nhất quán" thay vì mỗi ngành 1
accent bão hoà riêng. Đã test đổi màu **1 trong 11** file
(`logistics-container-ship.svg`, không kèm bản đã đổi màu trong gói này —
tự làm lại bằng cách thay các mã màu neutral `#1e293b/#475569/#94a3b8/#e2e8f0`
→ `#16283F/#2F4A63/#6B8299/(nền cream)` và đổi `--accent` mặc định).

## So sánh với ảnh AI-gen (khi nào dùng đường nào)

Có 1 kho ~97 ảnh minh hoạ tài chính do AI sinh (phong cách bìa The
Economist/Bloomberg Businessweek, palette cream/navy/teal/gold, có
grain/soft-shadow/glow) — đã so sánh trực tiếp với minh hoạ trong gói này.
Kết luận (chi tiết + ví dụ cụ thể trong lịch sử phát triển dự án, không lặp
lại hết ở đây):

- **Ảnh AI-gen THẮNG RÕ** về chất liệu bề mặt (grain, đổ bóng mềm có
  hướng, glow) — gần như không sửa được trong SVG phẳng nếu giữ đúng luật
  "không gradient/không filter" của `grammar.md` (luật đó tồn tại để đổi
  lấy khả năng xuất PDF/PPTX không vỡ — đánh đổi có chủ đích).
- **SVG tay trong gói này THẮNG** ở mọi tiêu chí liên quan tới TÁI SỬ DỤNG:
  gắn callout số liệu thật vào từng bộ phận (ảnh raster không làm được),
  sửa lại không tốn phí, xuất PDF/PPTX không vỡ nét, file nhẹ (4-8KB so với
  ảnh raster 500KB-1MB mỗi tấm).
- **Quy tắc chọn**: banner/bìa trang trí không cần callout, không cần sửa
  lại → dùng AI-gen. Minh hoạ cần neo số liệu thật của MỘT báo cáo cụ thể
  (đúng việc gói này được tạo ra để làm) → dùng SVG tay, không có lựa chọn
  nào khác khả thi.

## Ba việc còn để ngỏ (nói thẳng, không giấu)

1. **Chưa test round-trip PPTX/PDF thật.** `grammar.md` cấm `<filter>`,
   gradient nhiều stop, `clipPath` lồng, `<mask>` dựa trên LÝ DO ĐÃ BIẾT
   (rasterization khi Chromium in PDF, import PowerPoint không nhất quán —
   có 1 case thực nghiệm `case6-filterblur.html` chứng minh vế PDF). Nhưng
   CHƯA có ai thật sự convert 1 file trong `illustrations/` ra `.pptx`
   (qua `python-pptx` hoặc LibreOffice) hoặc in ra PDF rồi MỞ LẠI kiểm tra
   bằng mắt xem có đúng như kỳ vọng không — luật đang dựa trên suy luận từ
   nguyên lý + 1 case thử filter, chưa dựa trên toàn bộ 11 file thật.
2. **Đường dẫn Chromium/font là tuyệt đối, không di động.** `render.mjs`
   (không có trong gói này, chỉ có trong lab gốc) và mặc định
   `CHROME_PATH` trong 2 script `verify-*.mjs` trỏ cứng tới đường dẫn của
   máy phát triển ban đầu. Mọi font `Be Vietnam Pro` dùng trong các file
   `examples/*.html` cũng nạp qua `@font-face` trỏ file `.ttf` tuyệt đối
   trên máy đó. Chạy trên máy khác: PHẢI đặt `CHROME_PATH` đúng máy, và
   hoặc trỏ lại đường dẫn font hoặc chấp nhận fallback sang font hệ thống
   (chữ vẫn đọc được, chỉ khác kiểu chữ so với bản gốc).
3. **Nhánh "thu hẹp bề rộng hộp" trong `clampBoxToViewport` (annotate.js)
   viết ra nhưng chưa có ca thật nào kích hoạt.** Bug tràn khung đã sửa
   (xem `grammar.md` mục 9) được xác nhận qua nhánh "kẹp vị trí" (dịch hộp
   vào trong) — nhánh "co bề rộng hộp xuống tối thiểu 90px" mới chỉ chạy
   qua bằng chứng lý thuyết (đọc code), chưa có ảnh render thật nào chứng
   minh nó hoạt động đúng khi hộp thật sự không đủ chỗ ngang. Nếu gặp báo
   cáo có nhiều callout chữ dài chen trong khung hẹp, kiểm tra kỹ nhánh này
   bằng `verify-label-bounds.mjs` trước khi tin tưởng.

Ngoài 3 việc trên: `metaphor-table.md` có đề xuất thêm ẩn dụ "tảng băng"
(giá nổi/giá trị chìm) chưa được vẽ thành file trong `illustrations/` —
để dành cho đợt mở rộng sau nếu cần.
