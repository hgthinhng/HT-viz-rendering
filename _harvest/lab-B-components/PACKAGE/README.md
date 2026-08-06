# Thư viện Component Kể Chuyện (Nhóm B) — báo cáo tài chính/ngành

Viết cho: một phiên Claude khác đọc và dùng lại NGAY, không cần hỏi lại người giao việc. Nếu bạn là Claude đang đọc file này để tích hợp vào `~/HT-viz-rendering` hoặc dựng báo cáo mới — đọc hết mục "Quick start" và "Việc còn để ngỏ" trước khi sửa bất cứ gì.

## 0. Đây là gì

24 component HTML/CSS thuần (22 chính + 2 bonus) để KỂ CHUYỆN trong báo cáo tài chính/ngành — KHÔNG phải chart số liệu (chart là nhóm khác, xem `doctrine`/`design-system` ở repo cha nếu có). Toàn bộ đã render thật và nghiệm thu bằng số đo (không phải mô tả suông): 0 lỗi console, PDF xuất ra 0 ảnh raster ẩn, chạy được hoàn toàn offline (đã verify bằng cách chặn mọi request mạng), 16 trang in không cắt ngang component nào.

Không có chart, không có vẽ SVG số liệu trong package này. Nếu bạn cần chart, đây không phải chỗ.

## 1. Quick start

Xem toàn bộ 24 component cùng lúc kèm dữ liệu mẫu tiếng Việt (ngành vận tải biển, HƯ CẤU):

```bash
# Mở trực tiếp bằng trình duyệt bất kỳ — không cần server, không cần mạng.
xdg-open gallery.html   # hoặc mở bằng tay
```

Dùng 1 component trong file HTML mới của bạn:

```html
<head>
  <link rel="stylesheet" href="fonts-embedded.css">  <!-- font offline, bắt buộc -->
  <link rel="stylesheet" href="components.css">
</head>
<body>
  <!-- copy HTML từ catalog/<tên-file>.md -->
  <script src="components.js"></script>  <!-- chỉ cần nếu dùng wall-chart hoặc drill-card -->
</body>
```

Tra cứu component nào dùng khi nào: mở `catalog/` — mỗi file 1 component, có sẵn HTML copy-paste được. Xem mục 7 để có danh sách đầy đủ.

## 2. Cấu trúc thư mục

```
PACKAGE/
├── README.md              file này
├── gallery.html            demo đầy đủ 24 component, dữ liệu mẫu thật
├── components.css          toàn bộ style — ĐỌC ĐẦU FILE, có token + lịch sử quyết định
├── components.js           JS tối thiểu: thuật toán wall-chart + toggle drill-card
├── fonts-embedded.css      font base64 offline (~500KB) — sinh bởi build-fonts.py
├── build-fonts.py          script tải lại/đổi font, tự chạy lại khi cần đổi weight
├── catalog/                24 file .md, mỗi file 1 component: khi nào dùng + HTML mẫu
└── scripts/
    ├── verify.mjs          CLI gate nghiệm thu: PASS/FAIL + exit code, dùng cho CI
    ├── count_raster.py     đếm ảnh raster ẩn trong PDF (dùng bởi verify.mjs)
    └── measure-density.mjs công cụ đo mật độ ký tự/ink-height (không phải gate)
```

`node_modules/playwright-core` PHẢI tồn tại trong thư mục này (hoặc thư mục cha gần nhất) để `verify.mjs`/`measure-density.mjs` chạy được — ESM resolve theo VỊ TRÍ FILE, không theo cwd. Nếu thiếu:

```bash
npm i -D playwright-core   # nhẹ, không tải browser
# rồi trỏ --chromium=<path> vào 1 bản Chromium đã cache sẵn, ví dụ:
find ~/.cache/ms-playwright -maxdepth 1 -name "chromium-*"
```

## 3. Design tokens — nguồn và lịch sử (ĐỌC TRƯỚC KHI ĐỔI MÀU)

Bộ màu/font hiện tại (bản 3, CHỐT) lấy nguyên từ `reference-kimi.html` — một báo cáo nghiên cứu thị trường thật mà operator tự đánh giá cao nhất, đúng thể loại với package này. Ba nguồn độc lập không ai chép ai hội tụ cùng bộ màu này: reference-kimi.html, `huashu-design/references/design-styles.md` (mục Two-Font Consulting, gọi đúng tông này là "McKinsey deep-blue"), và một giáo trình thiết kế operator đưa thêm sau. Khi ba nguồn độc lập trùng nhau, đó là tín hiệu mạnh hơn bất kỳ lựa chọn đơn lẻ nào — ĐỪNG đổi lại trừ khi có nguồn thứ tư cũng độc lập và cũng mạnh như vậy.

```css
--ink        #051C2C   /* chữ chính, nền bìa tối nếu cần */
--ink-md     #42566A   /* phụ đề, đoạn văn phụ */
--ink-lo     #8595A6   /* chú thích, nhãn trục, dòng nguồn */
--line       #DBE2EA   /* hairline phân cách */
--paper      #FFFFFF
--paper-hi   #F7F9FC   /* nền panel/card */
--accent     #2251FF   /* xanh điện — nhấn chính, kicker, MUST */
--accent-hi  #1233B8   /* xanh đậm hơn — hover/emphasis */
--accent-soft #7D9BFF  /* chuỗi phụ */
--warn       #B07A10   /* vàng/đồng — cảnh báo/SHOULD, TÁCH biệt accent chính (đừng lẫn) */
--pos        #008A6D   /* DÙNG CỰC TIẾT CHẾ theo chỉ đạo operator — không rải khắp trang */
--neg        #C22F4E
```

Font: **Spectral cho MỌI vai trò chữ** (tiêu đề + thân bài, không tách display/serif). **IBM Plex Mono cho số liệu và MỌI nhãn kỹ thuật/trạng thái** (kicker, badge nguồn, status chip — kể cả nhãn không phải số, xem mục 4). **IBM Plex Sans** chỉ dùng cho ô bảng dữ liệu dày đặc (`table.dt td`, `table.opt-compare td`, `.heatmatrix td`, `.sl-card`) — KHÔNG BAO GIỜ cho tiêu đề hay thân bài.

### Lịch sử 3 bản (để không lặp lại vòng khám phá)

1. **Bản 1** (tự thiết kế độc lập): giấy ngà + hổ phách + Spectral/IBM Plex Mono. Chưa đối chiếu nguồn nào.
2. **Bản 2** (hoà theo `harvest-cfa-library/design-tokens/tokens.css`, brand StoiX): giấy ngà #F2E9D2 + walnut + gold + Fraunces/EB Garamond/Inter/JetBrains Mono. BỊ THAY vì tokens.css phục vụ pipeline CFA study notes (sách giáo khoa đọc dài) — khác thể loại với research report tài chính. Nếu bạn thấy code cũ/git history nhắc Fraunces hay EB Garamond, đó là di tích bản 2, ĐỪNG khôi phục.
3. **Bản 3** (CHỐT, đang dùng): theo reference-kimi.html — xem trên. `render_engine.py` (một pipeline DOCX khác) dùng ink #FAFAF7/indigo #2E3B7C — ĐÃ CÂN NHẮC VÀ LOẠI, vì đó là bảng màu riêng cho Word document (medium khác, thể loại khác), không phải nguồn cho HTML report. Chỉ giữ lại 1 kỹ thuật trình bày của nó (khối điểm mấu chốt, khối phụ 2), tái tô màu theo bản 3.

## 4. Vai trò font — quy tắc quyết định khi thêm component mới

Khi thêm 1 component mới, tự hỏi theo thứ tự:

1. Đây có phải SỐ LIỆU không (giá trị, phần trăm, ngày tháng, mã tham chiếu)? → `var(--font-mono)`.
2. Đây có phải NHÃN KỸ THUẬT/TRẠNG THÁI không (kicker, badge, status chip, label viết hoa nhỏ) dù không chứa số? → vẫn `var(--font-mono)` — đây là quy ước hay bị hiểu nhầm nhất, xem bản 2 từng gán sai sang font-sans rồi phải sửa lại toàn bộ 7 chỗ.
3. Đây có phải Ô BẢNG DỮ LIỆU DÀY ĐẶC không (bảng nhiều cột, thẻ trong lưới hẹp <200px)? → `var(--font-sans)`.
4. Còn lại (tiêu đề, thân bài, trích dẫn, mô tả) → `var(--font-serif)` hoặc `var(--font-display)` (hiện hai biến này trỏ CÙNG giá trị Spectral, tách biến chỉ để dễ đổi lại sau nếu cần).

## 5. Print-safety — bẫy đã đo được (không suy đoán, tất cả có bằng chứng thực nghiệm)

Đọc đầu `components.css` để có ghi chú tại từng chỗ. Tóm tắt:

| Bẫy | Vì sao xảy ra | Cách đã sửa |
|---|---|---|
| `box-shadow` có `blur-radius > 0` | Chromium in-PDF rasterize MỌI shadow có blur thành ảnh JPEG ẩn (kể cả không đụng `filter`/`backdrop-filter`) | `--shadow-1` chỉ dùng offset cứng blur=0 ("stamped hard shadow") — đo thực nghiệm 3 biến thể xác nhận blur=0 luôn 0 ảnh raster |
| `@media (max-width:Npx)` không giới hạn `screen` | Vùng in A4 (~688-717px sau margin) hẹp hơn nhiều breakpoint mobile phổ biến (700/760/860/900px) → breakpoint tự kích hoạt khi in | Mọi breakpoint co giãn phải viết `@media screen and (max-width:...)` |
| `overflow-x:auto` + `min-width` cố định | overflow-x:auto vô nghĩa trên giấy in, tương đương overflow:hidden | Bảng/lưới nhiều cột (swimlane) cần override `min-width:0` + cột co giãn riêng cho `@media print` |
| Flex/grid item không `break-inside:avoid` | Bị cắt đôi giữa 2 trang in (bắt được thật ở margin-note: giá trị 1 trang, nhãn rơi sang trang khác) | Thêm `break-inside: avoid` cho mọi item có thể đứng một mình về mặt nghĩa |
| `white-space: nowrap` trên badge trong thẻ hẹp | Statgrid co về 3 cột hẹp khi in (~208px/thẻ), badge dài tràn viền | Bỏ nowrap, cho phép badge xuống 2 dòng |
| JS `root.querySelector` sai phạm vi | Element cần tìm nằm NGOÀI root truyền vào, tìm không thấy, im lặng bỏ qua (không lỗi console) | Đảm bảo mọi element JS cần thao tác nằm ĐÚNG bên trong root — bắt bằng cách render PDF thật rồi soi, không phải đọc code |

Nguyên tắc rút ra: **KHÔNG BAO GIỜ tin "chắc là an toàn khi in" — luôn render PDF thật, đếm ảnh raster bằng `doc.xref_object` (KHÔNG dùng `get_images()`, nó bỏ sót ảnh trong Tiling Pattern/object stream nén), và soi từng trang bằng mắt.** `scripts/verify.mjs` tự động hoá toàn bộ quy trình này.

## 6. Accessibility — cách sửa đúng, cách sửa sai

Bản tham chiếu Kimi dùng SVG/canvas cho mọi chart, gần như không có text thay thế cho screen reader (11 thuộc tính aria trên toàn file 815KB). Component ở đây SỬA điểm yếu đó, nhưng theo cách đúng:

- **ĐÚNG**: nếu component là HTML/CSS thật (div/table có text thật, ví dụ wall-chart, ma trận 2×2) → không cần `role="img"`. Nếu bản trực quan phức tạp (nhiều lớp định vị tuyệt đối) khó đọc tuần tự, đánh dấu nó `aria-hidden="true"` và cung cấp MỘT bản thay thế thật riêng (danh sách phẳng sr-only cho wall-chart, bảng dữ liệu sr-only cho ma trận 2×2) — xem `.wc-fallback-list`, bảng `.visually-hidden` trước `.quad2x2`.
- **SAI (đã tự bắt lỗi và sửa)**: gắn `role="img"` thẳng lên một container HTML thật có nhiều phần tử text con — điều này khiến trình đọc màn hình sụp toàn bộ subtree thành MỘT ảnh mô tả bằng `aria-label`, CHE MẤT nội dung text thật bên trong. `role="img"` chỉ nên dùng cho SVG/canvas thật (nội dung pixel, không phải DOM text).
- Mọi phần tử `aria-hidden="true"` không được chứa phần tử focusable (không `tabindex`, không `role="button"` có handler) — kiểm tra kỹ nếu thêm tương tác mới vào nhánh đã đánh dấu ẩn.

## 7. Danh mục 24 component

| # | File | Dùng khi |
|---|---|---|
| 01 | `01-kpi-stat-grid.md` | tổng quan 5-6 số liệu lớn |
| 02 | `02-gate-ladder.md` | thang ràng buộc pháp lý xếp theo độ cứng |
| 03 | `03-wall-chart-timeline.md` | mốc lịch sử/pháp lý, chống chồng nhãn tự động |
| 04 | `04-swimlane-roadmap.md` | lộ trình N giai đoạn × M hạng mục, ưu tiên MoSCoW |
| 05 | `05-heat-matrix-table.md` | ma trận khả thi dạng bảng HTML thật (không canvas) |
| 06 | `06-quad-2x2-positioning.md` | định vị danh mục theo 2 trục liên tục |
| 07 | `07-pull-quote.md` | trích dẫn cá nhân nổi bật |
| 08 | `08-legal-quote.md` | trích dẫn văn bản pháp lý có mã hiệu lực |
| 09 | `09-note-box.md` | giả định / cảnh báo / kill-criteria |
| 10 | `10-assertion-evidence.md` | luận điểm câu đầy đủ + 1 bằng chứng (Tufte) |
| 11 | `11-exec-qa.md` | hỏi-đáp điều hành ngắn |
| 12 | `12-hairline-data-table.md` | bảng số liệu nhiều cột |
| 13 | `13-options-comparison-table.md` | so sánh N phương án loại trừ nhau |
| 14 | `14-before-after.md` | trước/sau, đúng 1 số mỗi bên |
| 15 | `15-ranked-risk-block.md` | rủi ro xếp hạng đơn trục |
| 16 | `16-process-step-chain.md` | quy trình tuần tự ≤6 bước |
| 17 | `17-methodology-box.md` | công khai cách tính một con số |
| 18 | `18-toc-with-milestones.md` | mục lục kèm trạng thái kiểm chứng được |
| 19 | `19-drill-card.md` | số liệu trong văn xuôi, bấm xem gốc |
| 20 | `20-source-badge-k-anchor.md` | badge nguồn NỀN TẢNG {value,source,date,tier} |
| 21 | `21-chapter-progress-bar.md` | định vị "đang ở đâu", tĩnh không fixed |
| 22 | `22-margin-dashboard-note.md` | rail ngữ cảnh bên lề, print-safe |
| 23 | `23-bonus-term-magazine.md` | (bonus) giải nghĩa thuật ngữ kiểu tạp chí |
| 24 | `24-bonus-key-point-callout.md` | (bonus) một câu kết luận, hai hairline |

Mỗi file có: câu hỏi component trả lời, đầu vào cần có, khi nào KHÔNG dùng, và HTML copy-paste được (trích thật từ `gallery.html`, không phải viết lại).

## 8. Nghiệm thu — chạy trước khi giao bất kỳ file HTML nào dùng thư viện này

```bash
# Gate đầy đủ: console error, page error, reduced-motion, offline, PDF+raster, soi từng trang
node scripts/verify.mjs --html=gallery.html --out=/tmp/verify-out
echo "exit code: $?"   # 0 = PASS, 1 = FAIL, 2 = lỗi cấu hình (thiếu chromium/html)

# Chỉ đo mật độ ký tự (không phải gate, không có PASS/FAIL) khi đổi font/cỡ chữ
node scripts/measure-density.mjs --html=gallery.html --font=Spectral --size=17 --line-height=1.7

# Đếm raster của một PDF bất kỳ (không chỉ của thư viện này)
python3 scripts/count_raster.py path/to/file.pdf --max 0
```

`verify.mjs` ghi `verify-report.json` + `verify-screenshot.png` + `verify-pages/page-NN.png` vào `--out`. Soi `verify-pages/` bằng mắt để bắt lỗi ngắt trang — KHÔNG có cách tự động 100% để phát hiện "component bị cắt ngang trang" (break-inside:avoid giảm rủi ro nhưng không loại trừ tuyệt đối mọi trường hợp), phải nhìn.

Ngưỡng số đã verify trên `gallery.html` (bản 3, Spectral): 65ch/17px cho 67-70 ký tự/dòng tiếng Việt (dấu chỉ làm giảm ~4% so với không dấu — không cần buffer line-height kiểu CJK vì tiếng Việt viết cách từ). Ink-height dấu chồng nặng nhất (ường ệ ẫ ữ ỗ ộ...) tại body 17px/lh1.7 dư 6.9px so với line-box; tại h2 30px/lh1.28 (weight 700) dư 8.66px. Nếu đổi font/cỡ chữ, CHẠY LẠI `measure-density.mjs` — số này gắn với Spectral cụ thể, không tự suy ra cho font khác (bài học từ việc bản 2 dùng số đo sai của EB Garamond).

## 9. Việc còn để ngỏ — nói thẳng, không giấu

- **Dark mode là suy diễn của tôi, KHÔNG có trong reference-kimi.html** (Kimi thuần light/paper). Giữ để tôn trọng `prefers-color-scheme`, nhưng operator chưa xác nhận trực tiếp bộ màu tối này đẹp hay đúng tinh thần — nếu dark mode quan trọng, cần hỏi lại.
- **Vai trò IBM Plex Sans (ô bảng dày đặc) là phán đoán của tôi**, không phải chỉ đạo chi tiết đến từng selector. Tôi áp cho `table.dt td`, `table.opt-compare td`, `.heatmatrix td`, `.sl-card` — nếu thấy chỗ nào khác trông rối vì Spectral quá "rời" ở cỡ nhỏ, có thể cần thêm class này ở đó, chưa audit hết mọi khả năng.
- **Không có kiểm tra bằng screen reader thật** (VoiceOver/NVDA/JAWS) — mọi khẳng định accessibility ở đây dựa trên kiểm tra DOM/ARIA tĩnh qua Playwright (`document.fonts`, cấu trúc aria-hidden, focusable elements), KHÔNG phải trải nghiệm người dùng thật. Nếu cần mức nghiệm thu cao hơn, cần người/agent có công cụ đọc màn hình thật.
- **Không có visual-regression diffing tự động** giữa các lần sửa — mọi so sánh "trước/sau" trong quá trình build đều bằng mắt người (đọc screenshot), không có pixel-diff threshold.
- **Số KPI lớn từng bị đơn vị phụ ("DWT") rớt xuống dòng ở khổ in 3 cột hẹp khi dùng font Fraunces (bản 2)** — vấn đề TỰ BIẾN MẤT khi quay lại Spectral (bản 3) vì Spectral hẹp hơn ở cùng cỡ chữ, không cần sửa gì thêm. Nếu sau này đổi font display khác, kiểm tra lại trường hợp này (`.sg-value` trong khổ in 3 cột, xem `crop`/`pdf-page` liên quan đến khối 01 statgrid).
- **Snippet trong `catalog/*.md` được trích TỰ ĐỘNG từ `gallery.html` tại thời điểm đóng gói** (script trích xuất không giữ lại trong package, chỉ chạy 1 lần) — nếu `gallery.html` được sửa sau này, catalog KHÔNG tự đồng bộ theo, phải trích lại bằng tay hoặc viết lại script trích xuất.
- **Chưa tích hợp vào cấu trúc `~/HT-viz-rendering`** (repo cha nếu có) — package này là một khối độc lập, việc đặt nó vào `design-system/components/` hay vị trí nào khác trong repo lớn hơn là quyết định của người/agent điều phối, không phải của package này.
- **`--pos` (xanh lá #008A6D) dùng cực tiết chế theo chỉ đạo operator** — hiện chỉ xuất hiện ở statgrid (xu hướng tăng tốt) và risk-rank (rủi ro thấp). Nếu thêm component mới có ngữ nghĩa "tích cực", cân nhắc kỹ trước khi thêm màu này, đừng dùng làm màu trang trí mặc định.

## 10. Dữ liệu mẫu trong gallery.html

Toàn bộ số liệu ngành vận tải biển (đội tàu, DWT, doanh thu, chi phí nhiên liệu...) thuộc công ty HƯ CẤU "CTCP Vận tải Biển Á Châu" — không phải doanh nghiệp niêm yết có thật, dựng riêng để minh họa component. Không dùng số liệu này cho bất kỳ báo cáo thật nào; khi áp vào dự án thật, thay toàn bộ nội dung mẫu, giữ nguyên cấu trúc class CSS.
