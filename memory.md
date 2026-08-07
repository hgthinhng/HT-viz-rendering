# HT-viz-rendering: bàn giao cho phiên mới

Đọc file này trước tiên. Nó cho biết đang ở đâu và làm gì tiếp.

## Đang ở đâu

**Phase 1 ĐÓNG.** Cả 8 task review sạch, 50 commit. Đợt dọn sau Phase 1 cũng xong: repo giờ
chạy được từ một máy chưa có gì, và ba việc treo chờ người dùng quyết đã có phán quyết.

Nghiệm thu gần nhất, chạy thật chứ không chép lại:

| Lệnh | Kết quả |
|---|---|
| `npm test` | 54 pass, 0 fail |
| `npm run verify` | exit 0, 23 gate PASS và 2 SKIP có ghi rõ lý do |
| `python3 -m pytest tests/ -v` | 38 passed |

Hai SKIP là cố ý, không phải gate hỏng: `gallery.html` là trang nội bộ nên không khai
`data-theme="light"`, và `vietnam-simplification-comparison.html` không dùng lớp annotation.

Trong repo: 50 mẫu ở `samples/`, 12 hồ sơ ở `research/`, 24 catalog spec, 11 minh hoạ SVG,
14 script chart ECharts, 48 component matplotlib EIR.

## Việc tiếp theo, làm ngay

**Viết plan Phase 2 rồi thi công**: pipeline HTML sang PDF và bộ gate nghiệm thu. Nguyên liệu
đã có sẵn trong `_harvest/`: pipeline hoàn chỉnh ở `harvest-extras/pipeline-stocklpt/`, 6 gate
và evidence ledger ở `lab-gate/` với `lab-evidence/`. Scope chi tiết nằm ở cuối
`docs/superpowers/plans/2026-08-06-ht-viz-rendering-phase1.md`.

Khối `.quad2x2` vỡ bố cục trong WeasyPrint: **đã sửa xong**, xem mục dưới. Nghi can ban đầu
(`position: absolute` cộng `transform: translate(-50%, -50%)`) hoá ra vô can, cả hai chạy đúng
trong WeasyPrint.

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
2. **Hệ màu tối: GIỮ cho trang nội bộ, KHOÁ SÁNG cho file giao đi.** File giao khách phải khai
   `<html lang="vi" data-theme="light">`. Gate `khoa-sang-khong-doi-theo-may-khach` đo bằng cách
   mở trang ở hai context màu rồi so nền với màu chữ. Đã đo hậu quả thật nếu quên khai: nền đổi
   từ `#FFFFFF` sang `#0A1420` trên máy khách đặt theme tối, trong khi chart vẫn nền trắng.
   Lý do đầy đủ ở `CLAUDE.md`.
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

## Ba xung đột đã phân xử, đừng mở lại

- **Bảng màu**: chốt trắng lạnh (`#051C2C` ink, `#2251FF` accent) chứ không phải giấy ngà ấm.
- **Gauge và radar**: cấm. Gauge gợi ý độ chính xác không có thật, radar có trục không độc lập.
- **Engine PDF**: WeasyPrint, không phải Chromium. Chromium tạo ảnh JPEG ẩn trong Tiling Pattern.

## Sổ nợ, chưa chặn ai

- Em-dash trong comment và tài liệu của tài sản harvest: `annotate.js` 33 chỗ, `grammar.md` 44,
  `metaphor-table.md` 25, `prompt-template.md` 18, comment `tokens.css` khoảng 26. Không phải nội
  dung hiển thị nên không chặn. Làm một task dọn riêng.
- `charts/echarts/out/` là thư mục rỗng, verify ghi ra `out-*.svg` ở cấp trên. Xoá hoặc dùng cho đúng.
- `verify-illustrations.mjs` so khớp lỗi phía `pageerror` theo nội dung văn bản, chưa trích file
  path từ stack rồi so basename như phía network. Chưa xảy ra trên codebase hiện tại.
- `_harvest/` vẫn còn 57MB, 860 file. Phase 2 và 3 dỡ dần vào đúng chỗ.

## Các phase sau

Viết plan riêng khi phase trước nghiệm thu xong. Phase 2 pipeline và gate. Phase 3 doctrine và
preset. Phase 4 báo cáo mẫu vận tải biển.
