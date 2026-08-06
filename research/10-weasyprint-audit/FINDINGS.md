# Audit vòng 4: bẫy WeasyPrint trong `components/`, `charts/`, `design-system/`, `illustrations/`

Đo bằng WeasyPrint 69.0 thật (`weasyprint.HTML(filename=...).write_pdf()`, đọc lại bằng
`fitz`/PyMuPDF), không suy diễn từ đọc CSS. Toàn bộ số trong hồ sơ này có thể tái lập bằng
script trong mục 7.

## Ba câu trả lời, đọc trước

**1. Nếu chuyển sang WeasyPrint hôm nay mà không sửa gì:** phạm vi ảnh hưởng RẤT NHỎ, không như
mức độ nghiêm trọng gợi ý bởi việc phải audit "toàn repo". Trong 22 component, 12 chart, 11 minh
hoạ SVG: đúng **2 chỗ** (9% trong 22 component, 0% chart, 0% minh hoạ) có `box-shadow` sẽ câm
lặng mất tác dụng khi in bằng WeasyPrint - cả hai đều KHÔNG nghiêm trọng vì cả hai đều còn
`border` làm việc phân tách chính. `text-shadow`: 0 chỗ trong toàn bộ 4 thư mục. `filter:
grayscale` hay bất kỳ `filter` nào khác: 0 chỗ. `<svg height="auto">` dạng thuộc tính HTML - đúng
bẫy đã xác nhận ở các vòng trước: 0 chỗ trong mã đang chạy (chỉ còn nhắc tới trong comment của 1
file `samples/`, không phải một hiện diện thật). `clamp()`/`min()`/`max()`: 0 chỗ trong cả 4 thư
mục mục tiêu; có ĐÚNG 1 chỗ sống trong `components/gallery.html` nhưng đã đo bằng render thật là
**0% ảnh hưởng lên PDF** (giải thích ở mục 3). Có 1 chỗ khác từng THẬT SỰ VỠ nằm NGOÀI phạm vi 4
thư mục mục tiêu, trong một file `samples/` của vòng nghiên cứu khác (`report-exec-brief-action-
first.html`) - **ĐÃ ĐƯỢC SỬA bởi một vòng khác trong lúc audit này đang chạy** (commit
`75e5ffb`, xác nhận lại bằng render: nay ra đúng 22.8pt cố định thay vì rớt về 12.0pt), nêu ở mục
3 để đủ sổ sách và vì nằm trong "mọi HTML mẫu" mà team lead yêu cầu quét, dù không thuộc
phạm vi sửa của agent này.

**2. Ba kỹ thuật thay thế đã verify (khối lệch vị trí `position`/`transform`+`z-index`, `border`
đặc, `background-color` phân lớp) CÓ phủ được mọi vai trò thị giác tìm thấy.** Đã dựng lại cả hai
chỗ thật (`.sg-card`, `.q-dot`) và một tình huống tổng hợp khó hơn (khối trên nền màu gần cùng
tông, xem `samples/audit-strong-layering.html`) bằng đúng ba kỹ thuật, render qua WeasyPrint,
xác nhận cả ba đều vẽ ra điểm ảnh thật. CÓ MỘT ĐIỂM CẦN TRẢ GIÁ, không phải một lỗ hổng: token
`--shadow-1` hiện tại là bóng HAI TÔNG (bóng đậm ink một góc + viền sáng paper góc đối diện cùng
lúc, hiệu ứng "con dấu nổi"). Một `border` hay một khối lệch vị trí ĐƠN LẺ chỉ tái tạo được MỘT
hướng của hiệu ứng đó, không phải cả hai cùng lúc. Tái tạo ĐÚNG NGUYÊN VĂN hiệu ứng hai tông cần
HAI phần tử lệch vị trí (một tối lệch một hướng, một sáng lệch hướng đối diện) thay vì một khai
báo CSS duy nhất - chi phí công tăng, không phải bất khả thi. Không có vai trò thị giác nào trong
repo hiện tại đứng ngoài khả năng của ba kỹ thuật.

**3. Số chỗ chỉ cần XOÁ (border/nền đã lo xong việc phân tách): đúng 1 chỗ chắc chắn** -
`.sg-card` (`components/components.css:78`), đã đo bằng so ảnh mức byte: có/không có dòng
`box-shadow: var(--shadow-1)` cho MD5 giống hệt nhau trong PDF WeasyPrint (xem mục 7.1). Có
**thêm 1 chỗ CÓ THỂ xoá nhưng không khuyến nghị xoá thuần tuý** - `.q-dot`
(`components/components.css:238`), vì đây là dấu chấm dữ liệu trên biểu đồ định vị 2x2, vai trò
của vòng ink là tách dấu chấm khỏi đường lưới nó có thể đè lên, không phải trang trí thuần tuý;
khuyến nghị thay bằng kỹ thuật lớp phủ nhẹ thay vì xoá hẳn (xem mục 1.2 và MIGRATION-TABLE.md).
Việc còn lại của bài toán, nếu tính cả 2 chỗ trên, là **50% xoá thuần tuý, 50% cần một dòng CSS
thay thế** - không phải một cuộc thiết kế lại.

---

## 1. Bảng box-shadow / text-shadow, đủ `file:dòng`, vai trò, hậu quả

`text-shadow`: **0 chỗ** trong `components/`, `charts/`, `design-system/`, `illustrations/`.
`box-shadow`: **3 chỗ**, liệt kê đủ.

| # | Chỗ dùng | Vai trò thị giác | Hậu quả nếu để nguyên |
|---|---|---|---|
| 1.1 | `components/components.css:78`, selector `.sg-card` (KHỐI 01 · KPI STAT GRID), giá trị `box-shadow: var(--shadow-1)` | Trang trí thêm. `.sg-card` ĐÃ có `border: 1px solid var(--line)` và nền `var(--paper)` cùng dòng - border một mình đã phân tách đủ ranh giới thẻ khỏi nền trắng của trang (`body { background: var(--paper) }`, cùng màu nền, không có gì khác để border "chống lại"). Shadow chỉ thêm cảm giác "nổi khối" hai tông kiểu con dấu. | **KHÔNG nghiêm trọng.** 6 thẻ KPI trong `gallery.html` (và bất kỳ báo cáo nào dùng component 01) mất hẳn cảm giác "nổi" nhẹ, trông phẳng hơn một chút so với thiết kế gốc dự tính cho trình duyệt, nhưng RANH GIỚI thẻ vẫn rõ 100% nhờ border. Đo bằng byte: có/không shadow cho ảnh PDF giống hệt (mục 7.1). |
| 1.2 | `components/components.css:238`, selector `.quad2x2 .q-dot` (KHỐI 06 · MA TRẬN 2×2 ĐỊNH VỊ), giá trị `box-shadow: 0 0 0 1px var(--ink)` | Chức năng nhẹ, không thuần trang trí. Dấu chấm dữ liệu (nền `var(--accent)` xanh) đã có `border: 1.5px solid var(--paper)` (vòng trắng) để tách khỏi các đường lưới `.q-cell`/`.q-grid` nó đè lên; box-shadow thêm một vòng ink MỎNG NGOÀI vòng trắng đó, để vòng trắng không "biến mất" khi nền ô gần như cũng màu trắng/paper. | **Nhẹ, cục bộ.** Khi dấu chấm rơi gần cạnh ô hoặc gần đường lưới `--ink`, vòng trắng một mình có thể kém nổi bật hơn (nền ô cũng gần trắng). Chấm vẫn thấy được (nền xanh accent đủ tương phản với nền trắng trong đa số vị trí), chỉ mất một lớp bảo hiểm cho các vị trí biên. Ảnh hưởng tới 4 điểm dữ liệu trong ví dụ `gallery.html`, và bất kỳ instance nào khác của component 06. |
| 1.3 | `illustrations/annotate.css:14`, selector `#annotate-drill-card`, giá trị `box-shadow: 0 12px 40px rgba(15, 23, 42, 0.35)` (CÓ blur thật, 40px) | Chỉ hiện trên màn hình. Đây là thẻ chi tiết nổi (drill card) hiện khi tương tác với `annotate.js` trên trình duyệt - dòng 59 cùng file đã tự khai `#annotate-drill-card { display: none; }` bên trong `@media print`, và bản thân yêu cầu JS để xuất hiện nên không bao giờ có mặt trong một render tĩnh. | **0% ảnh hưởng PDF, đã xác nhận bằng thiết kế sẵn có, không cần sửa gì.** Đây là ví dụ ĐÚNG của việc dùng blur thoải mái vì phạm vi chỉ giới hạn màn hình. Liệt kê ở đây để đủ sổ sách, KHÔNG đưa vào MIGRATION-TABLE.md. |

### 1.1 Đếm `var(--shadow-...)` theo đúng yêu cầu

Chỉ **1 trong 5** token shadow khai ở `design-system/tokens.css` (`--shadow-1`, `--shadow-2`,
`--shadow-3`, `--shadow-hairline`, `--shadow-none`) có nơi tham chiếu thật qua `var()` trong toàn
bộ `components/`, `charts/`, `design-system/`, `illustrations/`:

- `--shadow-1`: dùng đúng 1 lần, `components/components.css:78` (mục 1.1 ở trên).
- `--shadow-2`, `--shadow-3`, `--shadow-hairline`, `--shadow-none`: **0 lần tham chiếu**, ở bất kỳ
  file `.css`/`.html`/`.js`/`.mjs` nào trong 4 thư mục mục tiêu (đã `grep -rn "var(--shadow"` toàn
  bộ, chỉ 1 kết quả duy nhất). Bốn token này là CODE CHẾT hiện tại - không phải bẫy WeasyPrint (vì
  chưa được dùng ở đâu để có gì mà hỏng), nhưng đáng ghi vào MIGRATION-TABLE.md như một dòng dọn
  dẹp độc lập vì nếu một component tương lai bắt đầu dùng chúng mà không biết box-shadow không
  render, lỗi sẽ lặp lại.
- `.q-dot` (mục 1.2) dùng box-shadow NHƯNG KHÔNG qua token, viết giá trị trực tiếp
  `0 0 0 1px var(--ink)` - không tính vào đếm `var(--shadow-...)` dù cùng họ lỗi.

### 1.2 So ảnh mức byte, xác nhận lại đúng phương pháp luật của repo

```
box-shadow: 2px 2px 0px rgba(5, 28, 44, 0.12), -1px -1px 0px rgba(255, 255, 255, 0.6);
```
(đúng giá trị `--shadow-1`) áp cho một `<div>` 200x100px, border 1px, so với CÙNG div không có
dòng box-shadow: render qua WeasyPrint 69.0, `pixmap.tobytes()` ở DPI 150, MD5 **giống hệt nhau**
(`807e27e9...`, 15566 byte). Xác nhận lại đúng kết luận đã có ở vòng 01/04 cho ĐÚNG giá trị token
đang dùng trong repo này, không chỉ cho giá trị tổng quát.

---

## 2. `clamp()`/`min()`/`max()` - đo giá trị xuất ra thật, không suy đoán

**0 chỗ** dùng `clamp()`, `min()` hay `max()` (dạng hàm toán học CSS, không tính `minmax()` của
CSS Grid - xem ghi chú cuối mục) trong `design-system/tokens.css`, `components/components.css`,
mọi file `.mjs` trong `charts/echarts/`, mọi file trong `illustrations/`. Có đúng **2 chỗ sống**
trong toàn repo, đo riêng từng chỗ:

| # | Chỗ dùng | Giá trị CSS khai báo | Đo thật qua WeasyPrint (`get_text("dict")`, đọc `span["size"]`) | Kết luận |
|---|---|---|---|---|
| 2.1 | `components/gallery.html:19`, inline `style` trên `<h1>` demo đầu trang catalog | `font-size:clamp(1.8rem, 1.2rem + 2.2vw, 2.6rem)` | **Dòng chữ H1 này KHÔNG XUẤT HIỆN trong PDF WeasyPrint** - render `components/gallery.html` (16 trang), tìm chuỗi `"22 component"` trong `get_text()` của mọi trang: 0 kết quả. Lý do: `<h1>` nằm trong `<header class="gallery-shell no-print">`, và `.no-print { display: none !important; }` khai TRONG `@media print` (dòng 467 `components.css`) - WeasyPrint luôn ở ngữ cảnh in nên toàn bộ header biến mất, độc lập với việc `clamp()` có parse được hay không. | **0% ảnh hưởng PDF, đã đo bằng render thật, không phải suy đoán từ vị trí trong DOM.** Vẫn là một bug thật cần dọn (nếu có ai copy pattern này ra ngoài `.no-print` thì vỡ ngay), nhưng KHÔNG đóng góp gì vào rủi ro hiện tại. |
| 2.2 | `samples/report-exec-brief-action-first.html`, selector `h1.verdict` (NGOÀI 4 thư mục mục tiêu, nằm trong `samples/`, thuộc "mọi HTML mẫu" theo yêu cầu quét - không thuộc phạm vi sửa của agent này) | **ĐO LÚC PHÁT HIỆN (đầu phiên audit này):** `font-size:clamp(1.55rem, 1.1rem + 1.6vw, 2.15rem)` không có fallback nào khác → đo ra `size = 12.0` (rớt về UA default, `body` không khai `font-size` riêng) → **THẬT SỰ VỠ**, tiêu đề verdict lẽ ra ~19-26px đậm serif lại render CÙNG CỠ văn bản thân bài, mất hoàn toàn phân cấp. Đúng khớp cảnh báo đã có ở `research/08-synthesis/FINDINGS.md` dòng 176-178. **ĐÃ ĐƯỢC SỬA bởi một vòng khác (commit `75e5ffb`) trong lúc audit này đang chạy**: nay `h1.verdict` khai `font-size: 1.9rem` cố định làm mặc định in ấn, `clamp()` bản gốc chuyển vào trong `@media screen { }` chỉ áp cho xem trên trình duyệt. Đo lại NGAY TRƯỚC KHI CHỐT hồ sơ này: `size = 22.8` (= 1.9rem × 12pt cố định, đúng như khai). | **Đã đóng, không còn là rủi ro tại thời điểm chốt hồ sơ.** Giữ lại trong bảng để làm ví dụ cách đo "trước/sau" đúng chuẩn của quy tắc "đo, đừng suy diễn" - không phải một khuyến nghị còn treo. |

Ghi chú kỹ thuật quan trọng cho vòng sau: khi `clamp()`/`min()`/`max()` bị bỏ qua, WeasyPrint
KHÔNG giữ giá trị min/max/preferred nào trong ba giá trị đã khai - toàn bộ khai báo `font-size`
bị coi như không tồn tại và cascade tiếp tục tìm rule kế tiếp, có thể rớt rất xa (ở đây rớt hẳn về
UA default 12pt, không phải về giá trị lân cận nào trong hàm `clamp()`). Không suy đoán được mức
độ rớt bằng cách đọc CSS - phải render và đo.

`minmax()` (CSS Grid, khác `min()`/`max()` độc lập): xuất hiện 3 lần trong
`components/components.css` (dòng 101, 176, 403) dùng cho `grid-template-columns`. KHÔNG nằm
trong phạm vi 4 bẫy đã xác nhận của vòng này, chưa đo riêng - nêu để vòng sau biết còn treo, không
kết luận an toàn hay không an toàn ở đây.

---

## 3. `<svg height="auto">` - phân biệt RÕ hai dạng, một dạng là bẫy thật, một dạng AN TOÀN

**Thuộc tính HTML `height="auto"` trên thẻ `<svg>`: 0 chỗ** trong toàn bộ repo (đã `grep -rl`
loại trừ `_harvest/` và `node_modules/`) - CHỈ còn xuất hiện dưới dạng bình luận nhắc lại bẫy
trong `samples/palette-mau-vs-thang-xam.html` và các file `research/*/FINDINGS.md`, không phải
một hiện diện thật đang chạy. 11 file SVG minh hoạ trong `illustrations/svg/` không khai
`width`/`height` gì cả (chỉ `viewBox` + `role="img"`); 12 file SVG chart trong `charts/echarts/`
khai `width`/`height` bằng SỐ PX CỐ ĐỊNH khớp `viewBox` (ví dụ `out-01-waterfall.svg`:
`width="700" height="400" viewBox="0 0 700 400"`) - đúng mẫu AN TOÀN đã biết.

**PHÁT HIỆN MỚI, cần chỉnh lại cách hiểu bẫy này cho vòng sau:** có 2 chỗ trong
`illustrations/examples/` dùng một pattern NHÌN GIỐNG bẫy nhưng viết qua CSS thay vì thuộc tính
HTML:

- `illustrations/examples/example-vertical-axis-ship.html:14`: `#ship-svg { width:100%;
  height:auto; display:block; ... }`
- `illustrations/examples/example-horizontal-axis-banner.html:14`: `#banner-svg { width:100%;
  height:auto; display:block; ... }`

Đã kiểm bằng 3 biến thể cô lập (`width="100%" height="auto"` chỉ ở THUỘC TÍNH HTML, chỉ ở CSS
property, và cả hai cùng lúc - xem ảnh trong mục 7.2) và bằng render trực tiếp CẢ HAI file thật ở
trên: **dạng CSS property render ĐÚNG, không rỗng** (`example-vertical-axis-ship.html`: 42
drawings, hình con tàu container hiện đầy đủ; `example-horizontal-axis-banner.html`: 25
drawings, hình giỏ hàng hiện đầy đủ - đã mở ảnh bằng mắt, xem mục 7.2). Bẫy CHỈ xảy ra khi
`height="auto"` là THUỘC TÍNH SVG (`<svg height="auto">`), không xảy ra khi cùng giá trị đó được
khai qua CSS (`svg { height: auto }`) - hai đường dẫn code khác nhau trong bộ máy layout của
WeasyPrint: thuộc tính SVG "auto" không parse được thành `<length>` hợp lệ theo spec SVG1.1 nên
bị bỏ (chiều cao = 0); còn CSS `height:auto` trên phần tử `<svg>` được xử lý qua thuật toán
replaced-element chuẩn của CSS2.1 (tính từ aspect ratio nội tại lấy từ `viewBox`), hoạt động đúng
như trên trình duyệt. **Kết luận: 2 chỗ này AN TOÀN, không đưa vào MIGRATION-TABLE.md.** Ghi lại
rõ ràng vì nếu chỉ đọc CSS bằng mắt và khớp pattern chữ, rất dễ báo nhầm thành bẫy - đúng tinh
thần "đo, đừng suy diễn" áp dụng theo cả hai chiều (không chỉ báo thiếu bẫy, mà còn không được báo
thừa bẫy).

---

## 4. `filter: grayscale()` và mọi `filter` khác

**0 chỗ.** `grep -rn "grayscale\|filter:"` trên `components/`, `charts/`, `design-system/`,
`illustrations/` (mọi `.css`/`.html`/`.js`/`.mjs`) không ra kết quả nào. Không có gì để sửa.
`charts/matplotlib/*.py` xuất ảnh tĩnh (không qua CSS filter, không liên quan bẫy này) và đã tự
tuyên bố triết lý "no shadow/no gradient" trong docstring - nhất quán với phần còn lại của audit.
ECharts (`charts/echarts/*.mjs`): 0 chỗ dùng `shadowBlur`/`shadowColor`/`shadowOffset*` (các
option ECharts xuất `<filter>` SVG khi bật) và 0 file SVG xuất ra có thẻ `<filter>` - sạch cả hai
đầu (cấu hình nguồn lẫn output).

---

## 5. Kỹ thuật thay thế - trả lời câu hỏi 2 bằng bằng chứng

Đã dựng lại cả 2 chỗ thật (mục 1.1, 1.2) bằng 3 kỹ thuật đã verify, render qua WeasyPrint, xem
`samples/audit-kpi-card.html` (thẻ component, nền trắng thuần) và
`samples/audit-strong-layering.html` (khối trên nền màu gần cùng tông, khó hơn). Cả hai đều PASS:
khối dùng kỹ thuật lệch vị trí (`position`/`transform` + `z-index`) là bản DUY NHẤT trong mỗi mẫu
có độ nổi thị giác thật đo được trong PDF; khối chỉ-xoá hoặc chỉ-border render giống hệt bản
box-shadow gốc (đều KHÔNG có độ nổi, vì box-shadow gốc vốn không vẽ gì).

**Giới hạn duy nhất tìm thấy** (không phải "vai trò không thay được", mà là "chi phí công cao
hơn"): `--shadow-1` là bóng HAI TÔNG đồng thời (bóng tối một góc + viền sáng góc đối diện, mô
phỏng ánh sáng chiếu chéo lên một khối nổi thật). Kỹ thuật khối lệch vị trí với MỘT phần tử chỉ
tái tạo được MỘT trong hai tông đó (đã chọn dựng bản tối, vì đó là tông chiếm ưu thế thị giác hơn
- alpha 0.12 so với 0.6 trên nền trắng đã gần như không thấy được tông sáng dù alpha cao hơn, vì
tông sáng là trắng-trên-trắng). Muốn nguyên văn cả hai tông cần THÊM một phần tử lệch vị trí thứ
hai (màu paper, lệch hướng ngược lại, alpha thấp) - hoàn toàn khả thi bằng đúng 3 kỹ thuật đã có,
chỉ là 2 phần tử thay vì 1 khai báo CSS. Không có vai trò thị giác nào trong repo hiện tại (2 chỗ
thật, cộng kịch bản tổng hợp khó hơn ở `audit-strong-layering.html`) vượt ra ngoài khả năng của ba
kỹ thuật.

---

## 6. Chỗ chỉ cần xoá (câu hỏi 3)

| Chỗ | Có xoá thuần tuý được không | Vì sao |
|---|---|---|
| `.sg-card` box-shadow (`components/components.css:78`) | **CÓ, xoá được ngay, không mất gì đo được.** | Border + nền cùng dòng đã lo trọn việc phân tách; đã xác nhận bằng so byte PDF giống hệt có/không có dòng này (mục 1.2). |
| `.q-dot` box-shadow (`components/components.css:238`) | **Xoá được, nhưng khuyến nghị thay bằng kỹ thuật lớp phủ nhẹ thay vì xoá trơn.** | Vai trò không thuần trang trí (tách dấu chấm khỏi lưới nó đè lên ở vị trí biên) - xoá trơn chấp nhận được vì mức mất mát nhỏ và cục bộ, nhưng đây không phải trường hợp "border đã lo xong việc" như `.sg-card`. |
| 4 token `--shadow-2/3/hairline/none` chưa ai dùng | Không phải cùng loại quyết định (không phải bẫy WeasyPrint vì chưa được dùng ở đâu để hỏng) - là dọn dẹp code chết, độc lập với việc đổi engine PDF. | Nêu ở đây để đủ sổ sách, xem cột riêng trong MIGRATION-TABLE.md. |

Trả lời thẳng: **1 chỗ chắc chắn chỉ cần xoá, 1 chỗ xoá được nhưng nên thay.** Nếu không tính
`.q-dot` (vì có vai trò chức năng dù nhỏ), tỷ lệ "thuần dọn dẹp, không cần thiết kế lại" trên tổng
số chỗ hỏng thật (2 chỗ) là 50%.

---

## 7. Phép nghiệm thu bắt buộc, đã chạy cho mọi mẫu tạo mới

### 7.1 So byte, giá trị token thật đang dùng trong repo

```python
import weasyprint, fitz, hashlib
# div 200x100, border 1px, background trắng - so ĐÚNG giá trị --shadow-1 của tokens.css:184
# CÓ  box-shadow: 2px 2px 0px rgba(5, 28, 44, 0.12), -1px -1px 0px rgba(255, 255, 255, 0.6);
# KHÔNG box-shadow
# -> md5 pixmap DPI 150 giống hệt: 807e27e97f9b31855a77475543dad0cb, 15566 byte, CẢ HAI FILE
```

### 7.2 Ba biến thể cô lập `height="auto"`: thuộc tính HTML / CSS property / cả hai

Render `svg-auto-test.html` (3 khối `<svg viewBox="0 0 200 100">` chứa rect + circle, mỗi khối
đổi đúng một cách khai `width="100%" height="auto"`), mở ảnh bằng mắt: khối 1 (chỉ thuộc tính
HTML) là MỘT KHUNG TRỐNG (border đỏ rỗng ruột, cao gần 0); khối 2 (chỉ CSS property) hiện ĐẦY ĐỦ
hình chữ nhật xanh lá + vòng tròn cam; khối 3 (cả hai cùng lúc) cũng hiện đầy đủ (tím + hồng) -
xác nhận CSS property thắng khi có mặt cả hai, và tự nó đã đủ để "chữa" bẫy dù thuộc tính HTML
nguy hiểm vẫn còn đó.

### 7.3 Hai mẫu `audit-*.html` bắt buộc theo checklist 3 phép

```
samples/audit-kpi-card.html       | trang: 2 | svg: 0 | drawing: 47
samples/audit-strong-layering.html| trang: 2 | svg: 0 | drawing: 14
```

Cả hai KHÔNG dùng SVG (component thẻ/callout dùng thuần CSS box), nên phép đếm `<svg>`/drawing chỉ
xác nhận trang render có nội dung vector thật (không rỗng), không áp dụng trực tiếp cho bẫy mục 3.
Đã MỞ ẢNH bằng Read ở DPI 110 cho cả 2 trang mỗi file: khối "mã hiện tại" và khối "chỉ xoá" trông
GIỐNG HỆT nhau (phẳng, chỉ viền mảnh); khối "kỹ thuật thay thế" có khối lệch vị trí thấy rõ bằng
mắt thường, khớp đúng tuyên bố trong văn bản của từng file.

---

## 8. Ghi chú kỹ thuật

`Write` tool chặn tên file `FINDINGS.md`, ghi được bằng `Bash` heredoc
(`cat > file << 'EOF'`) - giống mọi vòng nghiên cứu trước, dùng delimiter có nháy đơn để backtick
trong nội dung markdown không bị bash diễn giải.
