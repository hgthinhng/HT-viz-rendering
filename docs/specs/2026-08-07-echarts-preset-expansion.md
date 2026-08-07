# Đặc tả thi công 6 preset ECharts còn thiếu (13-18)

Phạm vi: `charts/echarts/13-line-annotated.mjs` tới `18-sensitivity-grid.mjs`. Nguồn: đọc
`theme.mjs`, `fmt.mjs`, 8 preset mẫu hiện có (01,03,04,05,06,07,08,09,12),
`research/13-chart-component-gap/FINDINGS.md`, `research/03-chart-doctrine/*`, 3 mẫu HTML
vẽ tay (`chart-football-field-dinh-gia.html`, `chart-luoi-do-nhay-hai-chieu.html`,
`chart-radar-vs-cleveland.html`), `scripts/verify-charts.mjs`, và 1 vòng góp ý từ broadcast
4 mô hình ngoài (đã hợp nhất vào bản này, không để rời thành bản vá riêng).

Không phát hiện preset nào trong 6 cái này trùng lặp chart đã có, cả 6 lấp đúng lỗ hổng đã
đo bằng số trong `FINDINGS.md` (13/14/15/16 là P0 "rẻ và chặn nhiều báo cáo nhất", 17/18 là 2
chart chuẩn ngành đã có mẫu HTML nhưng chưa lên `.mjs`).

═══════════════════════════════════════════════════
## Mục 00. Schema dữ liệu dùng chung (ECharts + matplotlib)

Nếu mỗi preset tự định nghĩa đơn vị/kỳ báo cáo/nguồn/nhãn riêng thì thêm 6 chart là thêm 6
chỗ để bản HTML lệch bản PDF, đúng loại lỗi repo đã cắn nhiều lần (xem mục 0.5 dưới, và bảng
"Ba thuộc tính CSS mà WeasyPrint bỏ qua" trong `CLAUDE.md`). Đề xuất file mới
`charts/echarts/schema.mjs`, cả 6 preset import và gọi `validateChartRows()` ngay đầu:

```js
// charts/echarts/schema.mjs, Schema dữ liệu dùng chung cho MỌI preset chart (ECharts và
// matplotlib). Mục tiêu: HTML và PDF không lệch nhau vì hai engine tự định nghĩa riêng
// đơn vị/kỳ báo cáo/giá trị thiếu/nguồn/nhãn. Phía matplotlib cần bản tương đương
// charts/matplotlib/schema.py CÙNG TÊN FIELD, NGOÀI PHẠM VI đặc tả này (chỉ phủ 6 preset
// ECharts), cần 1 task riêng để đồng bộ 2 phía, nêu ra để không quên.

export const UNITS = Object.freeze([
  'ty_dong', 'trieu_dong', 'nghin_dong_cp', 'phan_tram', 'lan', 'diem',
]); // đơn vị canonical cố định. Thêm đơn vị mới PHẢI khai ở ĐÂY trước, không tự chế string rải rác trong preset.

export const SOURCE_TIERS = Object.freeze(['noi-bo', 'cong-bo', 'uoc-tinh']); // khớp đúng data-tier đã dùng trong components/catalog (01-kpi-stat-grid.md), không bịa tier mới

/**
 * @typedef {Object} ChartEntity
 * @property {string} code  Mã CHUẨN HOÁ: viết hoa, KHÔNG dấu, ngắn (lý tưởng <=6 ký tự).
 *   Đây là nhãn LÊN TRỤC/LABEL TRỰC TIẾP. Rút gọn phải quyết Ở ĐÂY lúc NHẬP dữ liệu, không
 *   phải để thuật toán chống-đè-nhãn của ECharts tự đoán lúc render, thuật toán đó
 *   (`labelLayout.moveOverlap`, `axisLabel.overflow`) hoạt động kém với chuỗi dài có dấu
 *   tiếng Việt.
 * @property {string} name  Tên đầy đủ tiếng Việt có dấu. CHỈ dùng ở tooltip hoặc 1 dòng chú
 *   giải "mã = tên" dưới chart, KHÔNG BAO GIỜ lên trục/nhãn trực tiếp.
 */

/** Kỳ báo cáo, 1 trong 3 dạng, tương thích trực tiếp với fmtQuarter() đã có trong fmt.mjs:
 * { type: 'quarter', q: 1-4, y: number } | { type: 'year', y: number } |
 * { type: 'point_in_time', label: string } */

/** Fail-fast lúc build nếu dữ liệu vi phạm ràng buộc dùng chung. Gọi ngay đầu mỗi preset. */
export function validateChartRows(rows, { requireUniformUnit = true } = {}) {
  if (requireUniformUnit) {
    const units = new Set(rows.map((r) => r.unit));
    if (units.size > 1) {
      throw new Error(`Cac hang phai CUNG 1 don vi (dang co: ${[...units].join(', ')}) -- xep hang/so sanh khac don vi la vo nghia nhu radar (xem CLAUDE.md cam radar).`);
    }
  }
  rows.forEach((r) => {
    if (r.unit && !UNITS.includes(r.unit)) throw new Error(`Don vi "${r.unit}" khong nam trong UNITS canonical -- them vao charts/echarts/schema.mjs truoc, dung tu che string moi trong preset.`);
    if (r.entity && !r.entity.code) throw new Error('entity co nhung thieu entity.code (nhan truc ngan) -- rut gon o TANG DU LIEU luc nhap, khong de wrapLabel() xu ly ten dai tren truc.');
  });
  return true;
}

/** Quy ước mã hoá 2 KỲ ĐO trên cùng 1 series (vd kỳ hiện tại vs kỳ trước): chấm ĐẶC cho kỳ
 * hiện tại, chấm RỖNG viền đậm cho kỳ trước. Bằng HÌNH DẠNG, không chỉ màu, xem lý do số
 * liệu ở mục 6 (16-dot-distribution) dưới. */
export function periodMarkerStyle(period, { accent, ink, paper }) {
  return period === 'current'
    ? { color: accent }
    : { color: paper, borderColor: ink, borderWidth: 2 };
}
```

Field bắt buộc mỗi hàng dữ liệu: `entity:{code,name}`, `unit` (1 trong `UNITS`), `period` (1
trong 3 dạng trên), `value` (number hoặc `null` tường minh khi thiếu, KHÔNG dùng 0 hay chuỗi
rỗng để biểu diễn "không có dữ liệu", vì 0 là 1 giá trị thật khác nghĩa), `source:{tier,label}`
(khớp `SOURCE_TIERS`). "Ngưỡng"/base-case luôn là CỜ tính từ INDEX nguyên (`isBase`,
`isOutlier`) chứ không so sánh giá trị float, đã áp dụng đúng cách này ở preset 18
(`baseRow===ri && baseCol===ci`) và 16 (`isOutlier()` theo rule IQR tường minh) dưới.

═══════════════════════════════════════════════════
## Mục 0. Phát hiện nền tảng, xử lý TRƯỚC khi viết 6 file

### 0.1 Bug thứ tự render trục hạng mục, ĐÃ XÁC NHẬN VÀ ĐÃ VÁ

Khi soát `04-dumbbell.mjs`/`06-tornado.mjs` để chuẩn bị đặc tả này, tôi grep toạ độ `y` thật
trong `out-06-tornado.svg`/`out-04-dumbbell.svg` đã render sẵn trong repo và thấy `categories[0]`
(phần tử đầu mảng, biến có biên độ LỚN NHẤT sau `sort` giảm dần) luôn render ở toạ độ y LỚN
NHẤT, tức ĐÁY hình, ngược với comment đầu file `06-tornado.mjs`: "sắp theo biên độ giảm dần để
biến quan trọng nhất nằm TRÊN CÙNG". **Team-lead đã xác minh độc lập và vá xong**: thêm
`inverse: true` cho cả `06-tornado.mjs` và `04-dumbbell.mjs`, render lại, WACC (biên độ lớn
nhất) nay ở y=88 (đỉnh) đúng như comment mô tả. `npm run verify` không bắt được lớp lỗi này vì
nó không kiểm thứ tự đọc, chỉ đếm phần tử SVG.

**Quy tắc cho preset 14 và 17 (đã thiết kế đúng ngay từ đầu, và nay có 2 lần xác nhận độc lập ,
của tôi và của team-lead)**: xây mảng dữ liệu theo đúng thứ tự đọc mong muốn (trên→dưới), rồi
bật `yAxis: { inverse: true }`, KHÔNG cần reverse mảng thủ công. Đã verify bằng thực nghiệm:
script test 3 hạng mục `ITEM_FIRST_LARGEST/SECOND/THIRD` với `inverse: true`, giữ nguyên thứ tự
mảng tự nhiên → `ITEM_FIRST_LARGEST` (index 0) ra y=70 (đỉnh), `ITEM_THIRD_SMALLEST` ra y=230
(đáy), đúng kỳ vọng.

### 0.2 `chart.convertToPixel()` hoạt động đúng trong chế độ `ssr:true`, đã verify

Không preset nào hiện có gọi `convertToPixel` (`06-tornado.mjs` dùng cách khác: `getOption()`
rồi `setOption()` lại để vá thêm `markLine`). Script test độc lập chạy thật trong
`charts/echarts/`: `convertToPixel({xAxisIndex:0, yAxisIndex:0}, [1,5])` trả về `[291, 168.75]`
đúng kỳ vọng hình học, và `chart.setOption({graphic:[...]})` gọi LẦN 2 sau đó để thêm annotation
vẫn giữ nguyên series gốc, xuất ra SVG có đủ cả `<path>` của line lẫn `<text>`/`<circle>` của
annotation. **Preset 13-line-annotated dựa vào cơ chế này, đã verify chạy được, không phải suy
đoán.**

### 0.3 `type:'custom'` renderItem trả `{type:'rect'}` xuất ra `<path>`, KHÔNG PHẢI `<rect>`, đã verify

Test độc lập: series custom render 2 hàng, mỗi hàng 1 `{type:'group', children:[{type:'rect'...},
{type:'text'...}]}`. Đếm bằng regex `<rect` chỉ ra 1 (SAI cảm giác), nhưng log `ecmeta_data_index`
xác nhận `renderItem` ĐÃ được gọi đủ 2 lần, và soi trực tiếp SVG thì cả 2 hàng đều có mặt, chỉ
serialize thành `<path d="M172 199l144 0l0 22l-144 0Z" .../>` thay vì `<rect>`. Không ảnh hưởng
gate `verify-charts.mjs` (regex đếm phần tử của nó đã gồm `path`), nhưng ai debug bằng cách
`grep '<rect'` trong `.svg` xuất ra sẽ tưởng nhầm là thiếu dữ liệu. **Áp dụng cho preset 17 và 14
(biến thể dot) nếu dùng custom renderItem.**

### 0.4 Cần thêm 2 export vào `theme.mjs` trước khi viết `18-sensitivity-grid.mjs`

`mixHex()` hiện là hàm private. Preset 18 cần thang màu liên tục 1-hue (5 bậc) từ
`PALETTE.paper` đến `PALETTE.accent`, đúng khuyến nghị ở `FINDINGS.md` §9 ("mở rộng
`PALETTE.bandLo/Mid/Hi` thành thang liên tục... KHÔNG tính hex mới trong file preset"). Diff tối
thiểu, không đổi `bandLo/Mid/Hi` hiện có (chúng dùng cho bullet chart, mục đích khác):

```js
// theme.mjs, đổi 1 dòng: thêm `export`
export function mixHex(hexA, hexB, t) { /* giữ nguyên thân hàm */ }

// theme.mjs, thêm hàm mới, đặt ngay sau khối PALETTE.bandLo/Mid/Hi
/** Thang màu liên tục N bậc, 1 hue duy nhất (paper -> hex), dùng cho magnitude field liên
 * tục (vd lưới độ nhạy). KHÔNG dùng cho delta/so sánh (đã có accent/negative). */
export function sequentialScale(hex = PALETTE.accent, steps = 5) {
  return Array.from({ length: steps }, (_, i) => mixHex(PALETTE.paper, hex, 0.12 + (i / (steps - 1)) * 0.88));
}
```

### 0.5 BUG NGHIÊM TRỌNG: nháy kép lồng nháy kép trong `style="..."` làm SVG KHÔNG PHẢI XML hợp lệ, ĐÃ VÁ, RÀNG BUỘC CỨNG MỚI CHO CẢ 6 PRESET

Team-lead phát hiện khi soi ảnh nghiệm thu bản vá mục 0.1: mở `out-*.svg` bằng trình duyệt báo
"attributes construct error", **toàn bộ 12 file `out-*.svg` hiện có KHÔNG PHẢI XML hợp lệ**.
Nguyên nhân: `theme.mjs` từng khai `FONT_STACK` bọc bằng nháy KÉP, ECharts nhúng nguyên chuỗi đó
vào thuộc tính `style="..."` của thẻ `<text>`, tạo ra nháy kép lồng trong nháy kép. Hậu quả đo
được trên engine đích: **WeasyPrint bỏ qua CẢ FILE, PDF ra 0 nét vẽ, chart biến mất sạch, không
báo lỗi gì**. Trình duyệt (HTML parser dễ tính hơn XML parser) vẫn hiện đúng nên soi bằng mắt
trên bản HTML KHÔNG BAO GIỜ phát hiện được lớp lỗi này.

Team-lead đã vá `theme.mjs` (`FONT_STACK`/`FONT_STACK_MONO` nay bọc bằng nháy ĐƠN: `"'Spectral',
Georgia, 'Times New Roman', serif"`), đo cả 2 chiều trên cùng 1 file: bản nháy kép cho 0 nét vẽ,
bản nháy đơn cho 24 nét vẽ và chữ đọc được trong tầng text PDF. Đồng thời thêm gate PARSE XML
thật vào `verify-charts.mjs` (dùng `python3 -c` gọi `xml.parsers.expat`, có chặn XXE/billion-laughs
bằng entity handler từ chối mọi entity dù bề mặt tấn công bằng 0 vì input là SVG tự sinh, không
phải file ngoài), đã kiểm gate ĐỎ ĐƯỢC khi tái tạo lỗi ở nguồn. **Bài học chung: một gate đếm
được không thay được một gate PARSE.**

**RÀNG BUỘC CỨNG MỚI cho 6 preset trong đặc tả này**: mọi chỗ tự set `style`/`font` trong
`graphic` hoặc custom `renderItem` PHẢI lấy `FONT_STACK`/`FONT_STACK_MONO` từ `theme.mjs`, TUYỆT
ĐỐI không tự gõ lại tên font thành chuỗi mới (dù nháy đơn hay nháy kép), gõ lại là tái tạo đúng
lớp bug này ở preset mới, và **gate cũ (đếm chuỗi `Spectral`/`IBM Plex Mono`) KHÔNG bắt được**,
chỉ gate parse XML mới mới chặn được.

**Tự rà lại 6 khối code đã viết trước khi hợp nhất vào bản này**: phát hiện đúng 1 chỗ vi phạm ở
`13-line-annotated.mjs`, `xAxis`/`yAxis.axisLabel` dùng `fontFamily: 'IBM Plex Mono, monospace'`
gõ tay thay vì import `TYPOGRAPHY.axisLabel`/`FONT_STACK_MONO`. Đã sửa trong bản final dưới (mục
1) bằng cách import `TYPOGRAPHY` và dùng `TYPOGRAPHY.axisLabel` như mọi preset khác. 5 preset còn
lại (14, 15, 16, 17, 18) đã rà lại, mọi chỗ set font đều tham chiếu `FONT_STACK`/`FONT_STACK_MONO`
import từ `theme.mjs`, không có chuỗi gõ tay.

═══════════════════════════════════════════════════
## Verify gate, áp dụng cho cả 6 preset

`scripts/verify-charts.mjs` quét mọi file khớp `^\d\d-.*\.mjs$` trong `charts/echarts/`, với MỖI
file kiểm đúng 7 điều (7, không phải 6, đã thêm gate XML ở mục 0.5):

1. Chạy được, không lỗi, không treo quá 60s → bắt lỗi cú pháp, import sai tên export, hoặc quên
   `process.exit(0)` (ECharts SSR giữ 2 socket handle, không tự thoát).
2. File `out-NN-ten.svg` tồn tại đúng tên suy từ tên file `.mjs` → bắt quên `fs.writeFileSync`
   hoặc đặt sai tên.
3. Không chứa `<image` → bắt raster hoá nhầm (không áp dụng, cả 6 preset thuần vector).
4. Không chứa chuỗi `base64` → tương tự.
5. PHẢI chứa `Spectral` hoặc `IBM Plex Mono` → bắt quên set `fontFamily` từ `theme.mjs`. Rủi ro
   riêng cho 13, 15, 17, 18 (có phần tử `graphic`/custom renderItem không đi qua `baseOption()`)
  , phải tự set `style.font` chứa `FONT_STACK`/`FONT_STACK_MONO` trên từng `text` tự vẽ.
6. KHÔNG chứa `#2a78d6|#dc2626|Calibri` (màu/font bản cũ) → an toàn nếu luôn lấy màu qua
   `PALETTE`/`sequentialScale`.
7. Đếm `<(rect|path|text|line|circle|polygon)` phải ≥10, dưới đó bị nghi rỗng → cả 6 preset đều
   thừa.
8. **MỚI (mục 0.5): SVG phải PARSE ĐƯỢC như XML thật** (`python3` + `xml.parsers.expat`) → gate
   quan trọng nhất, bắt đúng lớp lỗi mà gate #5 (đếm chuỗi) không thấy. Đã sống sót nguyên Phase 1
   vì không gate cũ nào PARSE.

**Điều gate KHÔNG bắt được (phải soi bằng mắt), quan trọng vì đây đúng loại lỗi từng lọt lưới:**
- Luật "trục bar phải từ 0", rủi ro nếu ai thêm `min` tuỳ tiện cho 14-bar-ranking.
- Luật "không traffic-light", rủi ro cao nhất ở 15-quadrant-scatter và 17-football-field.
- Chồng nhãn thật (chỉ đếm số phần tử text, không đo va chạm hình học), phải mở ảnh nhìn.
- Cấm gauge/radar (không preset nào trong 6 cái dùng, nêu để nhớ nếu mở rộng sau).
- Print-safe đen trắng thật (không có bước desaturate rồi so sánh tự động).
- Ràng buộc đơn vị đồng nhất trong xếp hạng (mục 2 dưới), `validateChartRows()` bắt lúc chạy
  script, nhưng CHỈ nếu preset thực sự GỌI nó; gate tự động không ép gọi.

═══════════════════════════════════════════════════
## 1. `13-line-annotated.mjs`, Line có chú thích sự kiện

**Trả lời**: một chỉ tiêu (doanh thu, tỷ lệ nợ xấu...) đổi hướng ở đâu, và SỰ KIỆN nào giải
thích. Nhu cầu 8/10 loại báo cáo, đang là lỗ hổng lớn nhất (PDF có, HTML không).
**KHÔNG dùng khi**: cần chú thích >5 sự kiện (nhãn chồng không gỡ được, tách sang component
`03-wall-chart-timeline`); dưới 4 điểm dữ liệu (đường quá ngắn để thấy xu hướng, dùng
`assertion-evidence` hoặc bảng số); mục đích là so CƠ CẤU nhiều phần chứ không phải 1 chỉ tiêu
đơn (dùng `12-area-stack`).

**Quyết định màu quan trọng**: TẤT CẢ điểm sự kiện dùng CÙNG 1 màu trung tính (`PALETTE.ink`),
không phân "tích cực=xanh/tiêu cực=đỏ". Đây không phải delta hay so sánh có bên thắng-thua, mà
là chú thích nguyên nhân, tô valence ở đây là traffic-light trá hình. Người đọc tự suy tốt/xấu
từ ĐỘ DỐC đường SAU điểm đó và từ nội dung nhãn.

```js
// 13-line-annotated.mjs, Line có chú thích sự kiện: xu hướng 1 chỉ tiêu + vì sao đổi hướng
// Dùng khi: một chỉ tiêu đổi hướng rõ rệt tại vài thời điểm, người đọc cần biết SỰ KIỆN
// nào giải thích bước ngoặt, không chỉ thấy đường lên/xuống. Nhu cầu 8/10 loại báo cáo
// (research/13-chart-component-gap/FINDINGS.md) nhưng chưa có bản ECharts.
// Dữ liệu cần: 1 chuỗi {period,value} qua N kỳ + tối đa 4-5 sự kiện {index,label}.
// Bẫy thường gặp: (1) nhồi quá 5 sự kiện -> nhãn chồng không gỡ được, tách sang bảng
// dòng thời gian riêng; (2) tô màu sự kiện theo tốt/xấu (traffic-light) -> CHỦ Ý dùng
// 1 màu ink trung tính cho MỌI sự kiện, người đọc tự suy từ độ dốc đường và nội dung
// nhãn; (3) dưới 4 điểm dữ liệu thì đường không đủ dài để thấy xu hướng.
// RÀNG BUỘC CỨNG (xem docs/specs/2026-08-07-echarts-preset-expansion.md mục 0.5): mọi
// font trong graphic PHẢI lấy từ FONT_STACK/TYPOGRAPHY của theme.mjs, không gõ lại chuỗi
// font mới -- nháy kép lồng nháy kép từng làm SVG không phải XML hợp lệ, WeasyPrint bỏ
// qua cả file mà không báo lỗi.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, PALETTE, FONT_STACK, TYPOGRAPHY, tooltipDefault } from './theme.mjs';
import { fmtCompact, fmtQuarter } from './fmt.mjs';

const periods = [
  { q: 1, y: 2025 }, { q: 2, y: 2025 }, { q: 3, y: 2025 }, { q: 4, y: 2025 },
  { q: 1, y: 2026 }, { q: 2, y: 2026 }, { q: 3, y: 2026 }, { q: 4, y: 2026 },
];
const values = [180, 195, 172, 210, 225, 198, 240, 265]; // tỷ đồng, doanh thu thuần theo quý

// index trỏ vào đúng vị trí trong `values` (0-based). Nhãn được wrap tự động.
const events = [
  { index: 2, label: 'Đứt gãy chuỗi cung ứng nguyên liệu nhập khẩu' },
  { index: 4, label: 'Ký hợp đồng phân phối độc quyền khu vực miền Trung' },
  { index: 5, label: 'Đối thủ mới gia nhập, cạnh tranh giá bán lẻ' },
  { index: 7, label: 'Ra mắt dòng sản phẩm cao cấp, biên lợi nhuận cao hơn' },
];
if (events.length > 5) throw new Error('13-line-annotated: qua 5 su kien, tach sang bang dong thoi gian (03-wall-chart-timeline)');

// bọc nhãn dài theo ranh giới TỪ, không cắt giữa âm tiết. Ngưỡng 18 ký tự khớp budget
// font mono 11px trên 1 dòng annotation rộng ~110-130px. (Đây là annotation TỰ DO,
// không nằm trên trục -- khác nguyên tắc "rút gọn ở tầng dữ liệu" áp cho NHÃN TRỤC ở
// preset 14/15, xem mục 2/3 dưới.)
function wrapLabel(text, maxCharsPerLine = 18) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  for (const w of words) {
    const next = cur ? `${cur} ${w}` : w;
    if (next.length > maxCharsPerLine && cur) { lines.push(cur); cur = w; } else { cur = next; }
  }
  if (cur) lines.push(cur);
  return lines;
}

const categories = periods.map((p) => fmtQuarter(p.q, p.y));
const W = 720, H = 420;
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Doanh thu thuần theo quý, có chú thích sự kiện', subtitle: 'Đơn vị: tỷ đồng, minh hoạ 2025-2026', width: W, height: H }),
  tooltip: tooltipDefault,
  legend: { show: false },
  grid: { left: 60, right: 24, top: 108, bottom: 50 }, // top nới rộng để chừa chỗ nhãn sự kiện phía trên đường
  xAxis: { type: 'category', data: categories, boundaryGap: false, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
  yAxis: { type: 'value', min: 0, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  series: [{
    name: 'Doanh thu thuần', type: 'line', data: values, symbol: 'circle', symbolSize: 6,
    lineStyle: { width: 2, color: PALETTE.accent }, itemStyle: { color: PALETTE.accent },
  }],
});

// lớp chú thích: vẽ SAU khi có toạ độ pixel thật (convertToPixel đã verify chạy đúng ở
// chế độ ssr:true, xem mục 0.2). setOption lần 2 chỉ thêm `graphic`, KHÔNG xoá series đã có.
const graphics = [];
events.forEach((ev, i) => {
  const [px, py] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [ev.index, values[ev.index]]);
  const above = i % 2 === 0; // xen kẽ trên/dưới giảm chồng nhãn khi 2 sự kiện gần nhau
  const leaderLen = 34;
  const lines = wrapLabel(ev.label, 18);
  const labelTopStart = above ? py - leaderLen - lines.length * 13 : py + leaderLen + 4;
  graphics.push(
    { type: 'line', shape: { x1: px, y1: py, x2: px, y2: above ? py - leaderLen : py + leaderLen }, style: { stroke: PALETTE.inkMd, lineWidth: 1 }, silent: true },
    { type: 'circle', shape: { cx: px, cy: py, r: 4 }, style: { fill: PALETTE.ink, stroke: PALETTE.paper, lineWidth: 1.5 }, silent: true },
    ...lines.map((line, li) => ({
      type: 'text', left: px, top: labelTopStart + li * 13,
      style: { text: line, font: `11px ${FONT_STACK}`, fill: PALETTE.inkMd, textAlign: 'center' },
      silent: true,
    })),
  );
});
chart.setOption({ graphic: graphics });

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-13-line-annotated.svg', import.meta.url), svg);
console.log('13-line-annotated: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
```

**Xử lý nhãn dài**: nhãn sự kiện là annotation TỰ DO (không nằm trên trục), nên `wrapLabel()` ở
tầng hiển thị vẫn đúng chỗ (khác preset 14/15 dưới, nơi nhãn nằm TRÊN TRỤC nên phải rút gọn ở
tầng dữ liệu, xem mục 2/3).
**Print-safe**: 1 line + marker ink, không phụ thuộc màu để phân biệt sự kiện.
**Verify gate**: rủi ro riêng là gate #5/#8 (font + XML), mọi `text` trong `graphics[]` đã set
`font: \`11px ${FONT_STACK}\`` bằng import, không gõ tay, nên an toàn với cả 2 gate. Rủi ro
KHÔNG bị gate bắt: nhãn 2 sự kiện liền kề (vd index 4 và 5) có thể vẫn chồng dù đã xen kẽ
trên/dưới, PHẢI mở SVG nhìn thật.

═══════════════════════════════════════════════════
## 2. `14-bar-ranking.mjs`, Bar ngang xếp hạng + biến thể Cleveland dot

**Trả lời**: ai đứng đầu/cuối theo 1 chỉ tiêu, khoảng cách giữa các hạng bao nhiêu. Nhu cầu
7/10 loại báo cáo.
**KHÔNG dùng khi**: cần so 2 mốc thời gian cho cùng danh sách (dùng `04-dumbbell`/`05-slope`);
mục đích là cơ cấu %, không phải thứ hạng (dùng `11-stacked-100`); >15-18 hạng mục (lọc top-N +
"khác").

**RÀNG BUỘC CỨNG (không phải khuyến nghị)**: mọi hàng trong 1 lượt xếp hạng (CẢ bar lẫn dot)
phải CÙNG 1 đơn vị, ép bằng `validateChartRows()` ở runtime, xếp hạng NIM(%) trộn với điểm xếp
hạng tín dụng (thang 1-10) trong cùng 1 trục là đúng loại vô nghĩa mà repo cấm radar vì lý do
tương tự: trục dùng chung ngầm định "cùng đơn vị đo", trộn đơn vị phá vỡ ngầm định đó y hệt cách
radar phá vỡ ngầm định "các trục độc lập". Cần so N tiêu chí khác đơn vị → CHUẨN HOÁ về
percentile/z-score trước rồi mới xếp chung 1 trục, hoặc tách thành N nhóm dot-plot riêng (mỗi
nhóm 1 đơn vị, bọc ngoài bằng `07-small-multiples`).

**RÀNG BUỘC CỨNG THỨ HAI (rút gọn nhãn ở tầng dữ liệu, không phải tầng hiển thị)**: nhãn trục
dùng `entity.code` (mã ngắn tự đặt lúc nhập dữ liệu, KHÔNG dùng `wrapLabel()` cho nhãn TRÊN
TRỤC), thuật toán chống-đè-nhãn của ECharts hoạt động kém với chuỗi dài có dấu tiếng Việt, nên
quyết định rút gọn phải chốt lúc NHẬP dữ liệu, không phải để thuật toán tự đoán lúc render. Tên
đầy đủ chỉ xuất hiện ở tooltip và 1 dòng chú giải "mã = tên" dưới chart (bản PDF không có hover,
phải tự thân đủ nghĩa).

Script xuất **2 file SVG** từ 1 nguồn dữ liệu dùng chung: `out-14-bar-ranking.svg` (bar, khổ
rộng, file BẮT BUỘC để gate pass) và `out-14-bar-ranking-dot.svg` (Cleveland dot, khổ hẹp ,
bonus, gate không kiểm riêng nhưng không hại gì):

```js
// 14-bar-ranking.mjs, Bar ngang xếp hạng + biến thể Cleveland dot cho khổ hẹp
// Dùng khi: xếp hạng N hạng mục theo 1 chỉ tiêu, vị trí quan trọng hơn giá trị tuyệt đối.
// KHÔNG dùng khi: so 2 mốc thời gian (04-dumbbell/05-slope); mục đích là cơ cấu %
// (11-stacked-100); >15-18 hạng mục (lọc top-N + "khác").
// Dữ liệu cần: {entity:{code,name}, unit, value}[]. RÀNG BUỘC CỨNG: mọi hàng phải CÙNG
// 1 unit (validateChartRows() ép ở runtime, build FAIL nếu vi phạm) -- xếp hạng khác đơn
// vị vô nghĩa như radar (xem CLAUDE.md cấm radar). RÀNG BUỘC CỨNG THỨ HAI: nhãn trục =
// entity.code (rút gọn Ở TẦNG DỮ LIỆU lúc nhập), entity.name đầy đủ CHỈ ở tooltip + 1
// dòng chú giải dưới chart -- không dùng wrapLabel()/truncate cho nhãn TRÊN TRỤC vì thuật
// toán chống-đè-nhãn của ECharts hoạt động kém với chuỗi dài có dấu tiếng Việt.
// Bẫy khác: (1) không sort giảm dần; (2) trục giá trị không từ 0 (ràng buộc cứng cho CẢ
// HAI biến thể: dot vẫn vẽ đường nối 0->value, tức vẫn mã hoá bằng ĐỘ DÀI như bar, không
// phải scatter thuần vị trí); (3) quên yAxis.inverse:true -- xem mục 0.1, hạng 1 sẽ rơi
// xuống ĐÁY thay vì đỉnh nếu thiếu dòng này.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';
import { validateChartRows } from './schema.mjs';

const raw = [
  { entity: { code: 'NLTT', name: 'Năng lượng tái tạo' }, unit: 'phan_tram', value: 33.0 },
  { entity: { code: 'CNTT', name: 'Công nghệ thông tin' }, unit: 'phan_tram', value: 24.6 },
  { entity: { code: 'DPYT', name: 'Dược phẩm & bán lẻ y tế' }, unit: 'phan_tram', value: 21.3 },
  { entity: { code: 'BLTD', name: 'Bán lẻ tiêu dùng nhanh' }, unit: 'phan_tram', value: 18.7 },
  { entity: { code: 'VLXD', name: 'Vật liệu xây dựng' }, unit: 'phan_tram', value: 15.4 },
  { entity: { code: 'TCTD', name: 'Tài chính tiêu dùng' }, unit: 'phan_tram', value: 13.9 },
  { entity: { code: 'BKCN', name: 'Bất động sản khu công nghiệp' }, unit: 'phan_tram', value: 12.1 },
  { entity: { code: 'LOGI', name: 'Logistics & vận tải biển' }, unit: 'phan_tram', value: 9.8 },
]; // % biên lợi nhuận gộp minh hoạ theo phân khúc, KHÔNG phải số thật
validateChartRows(raw); // FAIL ngay nếu ai lỡ trộn 'phan_tram' với 'diem' vào cùng 1 lượt xếp hạng
const rows = [...raw].sort((a, b) => b.value - a.value); // sort giảm dần: hạng 1 ở index 0

// dòng chú giải "mã = tên", vì bản PDF không có hover -- annotation-first, không dựa hover
const legendLine = rows.map((r) => `${r.entity.code}=${r.entity.name}`).join(' · ');

function buildValueAxis() {
  return { type: 'value', min: 0, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtPercent(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } };
}

// --- Biến thể 1: bar ngang, khổ rộng ---
{
  const W = 700, H = 440;
  const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
  chart.setOption({
    ...baseOption({ title: 'Xếp hạng biên lợi nhuận gộp theo phân khúc', subtitle: 'Đơn vị: %, sắp giảm dần, minh hoạ FY2026', width: W, height: H }),
    tooltip: { ...tooltipDefault, formatter: (p) => `${rows[p.dataIndex].entity.name}: ${fmtPercent(p.value, { decimals: 1 })}` },
    legend: { show: false },
    grid: { left: 60, right: 50, top: 60, bottom: 50 },
    xAxis: buildValueAxis(),
    // index 0 (hạng 1) phải render ở ĐỈNH -> inverse:true, GIỮ NGUYÊN thứ tự mảng đã sort
    // (xem mục 0.1: 06-tornado.mjs từng KHÔNG làm bước này nên bị lộn ngược, nay đã vá)
    yAxis: { type: 'category', data: rows.map((r) => r.entity.code), inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    series: [{
      type: 'bar', barWidth: 20, itemStyle: { color: PALETTE.accent, borderRadius: [0, 3, 3, 0] },
      data: rows.map((r) => r.value),
      label: { show: true, position: 'right', formatter: (p) => fmtPercent(p.value, { decimals: 1 }), ...TYPOGRAPHY.dataLabel },
    }],
    graphic: [{ type: 'text', left: 60, top: H - 16, style: { text: legendLine, font: `9px ${FONT_STACK}`, fill: PALETTE.inkLo } }],
  });
  const svg = chart.renderToSVGString();
  fs.writeFileSync(new URL('./out-14-bar-ranking.svg', import.meta.url), svg);
  console.log('14-bar-ranking (bar): OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  chart.dispose();
}

// --- Biến thể 2: Cleveland dot, khổ hẹp (vd cột phụ A4) ---
{
  const W = 380, H = 460;
  const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
  chart.setOption({
    ...baseOption({ title: 'Xếp hạng biên lợi nhuận gộp', subtitle: '%, khổ hẹp', width: W, height: H }),
    tooltip: { ...tooltipDefault, formatter: (p) => `${rows[p.dataIndex].entity.name}: ${fmtPercent(p.value, { decimals: 1 })}` },
    legend: { show: false },
    grid: { left: 60, right: 40, top: 60, bottom: 60 }, // mã 4 ký tự nên left co từ 148 (khi còn dùng tên dài) xuống 60
    xAxis: buildValueAxis(),
    yAxis: { type: 'category', data: rows.map((r) => r.entity.code), inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    series: [
      {
        name: 'Đường nối', type: 'custom', z: 1, silent: true,
        renderItem: (params, api) => {
          const y = api.coord([0, params.dataIndex])[1];
          const x0 = api.coord([0, params.dataIndex])[0];
          const x1 = api.coord([api.value(1), params.dataIndex])[0];
          return { type: 'line', shape: { x1: x0, y1: y, x2: x1, y2: y }, style: { stroke: PALETTE.inkLo, lineWidth: 1.5 } };
        },
        data: rows.map((r) => [0, r.value]),
      },
      {
        name: 'Giá trị', type: 'scatter', symbolSize: 11, z: 3,
        itemStyle: { color: PALETTE.accent },
        data: rows.map((r) => r.value),
        label: { show: true, position: 'right', formatter: (p) => fmtPercent(p.value, { decimals: 1 }), ...TYPOGRAPHY.dataLabel },
      },
    ],
    graphic: [{ type: 'text', left: 20, top: H - 40, style: { text: legendLine, font: `9px ${FONT_STACK}`, fill: PALETTE.inkLo } }], // khổ hẹp -> chú giải có thể tràn xuống 2-3 dòng, đo thử khi code thật
  });
  const svg = chart.renderToSVGString();
  fs.writeFileSync(new URL('./out-14-bar-ranking-dot.svg', import.meta.url), svg);
  console.log('14-bar-ranking (dot): OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  chart.dispose();
}
process.exit(0);
```

**Xử lý nhãn dài**: rút gọn quyết Ở TẦNG DỮ LIỆU (`entity.code`, 4 ký tự, không cần wrap ở CẢ
HAI biến thể vì mã đã đủ ngắn), khác thiết kế nháp đầu tiên của tôi (đã tự sửa: bản nháp đó
dùng `wrapLabel()` ở tầng hiển thị cho biến thể dot, đúng thứ bị chỉ ra là sai vì thuật toán
declutter của ECharts không xử lý tốt chuỗi dài có dấu). Với tên doanh nghiệp/ngân hàng niêm yết
thật, `entity.code` chính là mã chứng khoán chuẩn hoá (VCB, TCB...), không phải mã tự đặt như ví
dụ phân khúc này.
**Print-safe**: cả 2 biến thể chỉ 1 màu (`accent`), không có valence giữa các hạng mục, đen
trắng vẫn đọc đúng thứ hạng qua ĐỘ DÀI (bar) hoặc VỊ TRÍ điểm (dot).
**Verify gate riêng**: `process.exit(0)` đặt Ở CUỐI file sau khi CẢ HAI chart đã `dispose()` ,
nếu tách nhầm thành 2 script riêng thì cái đầu thoát sớm sẽ chặn cái sau chạy. Gate tự động chỉ
kiểm `out-14-bar-ranking.svg`, file `-dot.svg` không bị soi riêng nhưng nên tự chạy và nhìn cả
2 file bằng mắt. Gate #8 (XML) áp dụng bình thường cho cả 2 file vì cùng dùng `TYPOGRAPHY`/
`FONT_STACK` import, không gõ tay font.

═══════════════════════════════════════════════════
## 3. `15-quadrant-scatter.mjs`, Scatter chia 4 phần tư

**Trả lời**: nhóm so sánh phân bố ra sao trên 2 tiêu chí cùng lúc, ai rơi vào góc phần tư nào
(vd định giá P/B vs hiệu quả ROE). Nhu cầu 7/10 loại báo cáo.
**KHÔNG dùng khi**: 2 trục không độc lập ý nghĩa (P/E và P/B thường tương quan cùng chiều, phần
tư không cho insight mới); <5 điểm (không đủ thấy phân bố, dùng bảng); cần thêm chiều thứ 3
quan trọng hơn logic phần tư (dùng bubble scatter thường, bỏ đường chia).

**Quyết định quan trọng, đúng doctrine baseline trong-nhóm** (khớp memory nội bộ repo: baseline
phải rút TRONG nhóm đang so sánh, không lấy từ ngoài): 2 đường chia phần tư = TRUNG VỊ của
chính tập dữ liệu đang vẽ, tính TRONG code, KHÔNG hardcode "trung bình ngành" từ nguồn khác trừ
khi đó là 1 điểm dữ liệu tường minh riêng.

**Về rút gọn nhãn**: preset này VỐN ĐÃ ĐÚNG nguyên tắc "rút gọn ở tầng dữ liệu" ngay từ bản nháp
đầu (dùng ticker ngắn VCB/TCB... làm nhãn chính), chỉ đổi tên field cho khớp schema chung
(`entity.code`/`entity.name` thay vì `ticker` phẳng), không đổi logic hiển thị.

**Phân biệt với ràng buộc đơn vị của preset 14**: 15 có 2 CHỈ TIÊU khác đơn vị trên 2 TRỤC KHÁC
NHAU (P/B là "lần", ROE là "%"), đây KHÔNG vi phạm ràng buộc "cùng đơn vị" của preset 14, vì
ràng buộc đó áp cho việc XẾP HẠNG chung 1 trục, còn scatter 2 trục vốn dĩ thiết kế cho 2 đơn vị
khác nhau trên 2 trục riêng biệt (đúng bản chất quadrant chart).

```js
// 15-quadrant-scatter.mjs, Scatter chia 4 phần tư: định vị nhóm so sánh trên 2 tiêu chí
// Dùng khi: cần thấy nhóm so sánh (ngân hàng, doanh nghiệp cùng ngành) phân bố thế nào
// trên 2 tiêu chí ĐỘC LẬP cùng lúc (vd P/B vs ROE), chia bởi đường trung vị/mốc tham
// chiếu thành 4 vùng đọc được bằng câu chữ, không chỉ bằng toạ độ.
// KHÔNG dùng khi: 2 trục tương quan mạnh (phần tư vô nghĩa); <5 điểm; cần bubble 3D.
// Dữ liệu cần: {entity:{code,name}, pb, roe}[]. Đường chia = trung vị CỦA CHÍNH NHÓM
// đang vẽ (không lấy baseline từ ngoài trừ khi có lý do rõ và ghi chú). LƯU Ý: 2 trục ở
// đây CỐ Ý khác đơn vị (P/B="lần", ROE="%") -- đây KHÔNG vi phạm ràng buộc "cùng đơn vị"
// của 14-bar-ranking, ràng buộc đó chỉ áp cho xếp hạng chung 1 trục, không áp cho 2 trục
// riêng biệt của quadrant chart.
// Bẫy thường gặp: (1) tô nền góc "tốt" bằng accent -> traffic-light trá hình, CHỦ Ý
// không tô nền quadrant nào cả, chỉ ghi chú chữ trung tính; (2) nhãn entity.code chồng
// nhau khi 2 điểm gần -> dùng labelLayout.moveOverlap (rút gọn code đã quyết Ở TẦNG DỮ
// LIỆU lúc nhập, không xử lý ở tầng hiển thị); (3) ép trục từ 0 -> scatter là mã hoá VỊ
// TRÍ không phải ĐỘ DÀI, được miễn luật "từ 0" (đúng ngoại lệ đã có tiền lệ ở
// 09-candlestick.mjs cho trục giá OHLC).
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK, tooltipDefault } from './theme.mjs';
import { fmtMultiple, fmtPercent } from './fmt.mjs';

const rows = [
  { entity: { code: 'VCB', name: 'Ngân hàng TMCP Ngoại thương Việt Nam' }, pb: 2.8, roe: 19.8 },
  { entity: { code: 'TCB', name: 'Ngân hàng TMCP Kỹ thương Việt Nam' }, pb: 1.1, roe: 14.5 },
  { entity: { code: 'MBB', name: 'Ngân hàng TMCP Quân đội' }, pb: 1.0, roe: 20.1 },
  { entity: { code: 'ACB', name: 'Ngân hàng TMCP Á Châu' }, pb: 1.5, roe: 23.0 },
  { entity: { code: 'VPB', name: 'Ngân hàng TMCP Việt Nam Thịnh Vượng' }, pb: 1.0, roe: 11.2 },
  { entity: { code: 'STB', name: 'Ngân hàng TMCP Sài Gòn Thương Tín' }, pb: 1.3, roe: 16.5 },
  { entity: { code: 'HDB', name: 'Ngân hàng TMCP Phát triển TP.HCM' }, pb: 1.4, roe: 21.5 },
  { entity: { code: 'TPB', name: 'Ngân hàng TMCP Tiên Phong' }, pb: 0.9, roe: 14.0 },
  { entity: { code: 'VIB', name: 'Ngân hàng TMCP Quốc tế Việt Nam' }, pb: 1.6, roe: 22.0 },
]; // P/B (x) và ROE % (y) minh hoạ 9 ngân hàng, KHÔNG phải số thật

function median(arr) {
  const s = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}
const medPb = median(rows.map((r) => r.pb));
const medRoe = median(rows.map((r) => r.roe));

const W = 680, H = 620; // gần vuông CHỦ Ý: quadrant méo hình chữ nhật sẽ đọc sai cảm giác "cân bằng"
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Định vị nhóm ngân hàng: P/B và ROE', subtitle: 'Trục chia = trung vị của chính 9 mã đang so sánh, không phải mốc ngoài', width: W, height: H }),
  tooltip: { ...tooltipDefault, formatter: (p) => `${p.data.entity.name}<br/>P/B: ${fmtMultiple(p.data.pb)}<br/>ROE: ${fmtPercent(p.data.roe, { decimals: 1 })}` },
  legend: { show: false },
  grid: { left: 70, right: 40, top: 70, bottom: 60 },
  xAxis: { type: 'value', scale: true, name: 'P/B', nameTextStyle: TYPOGRAPHY.axisName, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtMultiple(v, { decimals: 1 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  yAxis: { type: 'value', scale: true, name: 'ROE (%)', nameTextStyle: TYPOGRAPHY.axisName, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtPercent(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  series: [{
    type: 'scatter', symbolSize: 12, itemStyle: { color: PALETTE.accent, borderColor: PALETTE.paper, borderWidth: 1 },
    data: rows.map((r) => ({ ...r, value: [r.pb, r.roe] })),
    label: { show: true, formatter: (p) => p.data.entity.code, position: 'top', ...TYPOGRAPHY.dataLabel },
    labelLayout: { moveOverlap: 'shiftY' }, // chống chồng nhãn khi 2 mã gần nhau (đã kiểm ECharts 6.1 hỗ trợ)
    markLine: {
      silent: true, symbol: 'none',
      lineStyle: { color: PALETTE.ink, type: 'dashed', width: 1 }, // dashed CHO PHÉP ở đây: markLine tham chiếu, không phải splitLine trục giá trị (luật "không dashed" trong theme.mjs chỉ áp cho splitLine)
      label: { show: false },
      data: [{ xAxis: medPb }, { yAxis: medRoe }],
    },
  }],
  graphic: [
    { type: 'text', left: 76, top: 76, style: { text: 'Định giá thấp / Hiệu quả cao', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo } },
    { type: 'text', left: W - 40, top: 76, style: { text: 'Định giá cao / Hiệu quả cao', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo, textAlign: 'right' } },
    { type: 'text', left: 76, top: H - 68, style: { text: 'Định giá thấp / Hiệu quả thấp', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo } },
    { type: 'text', left: W - 40, top: H - 68, style: { text: 'Định giá cao / Hiệu quả thấp', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo, textAlign: 'right' } },
  ],
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-15-quadrant-scatter.svg', import.meta.url), svg);
console.log('15-quadrant-scatter: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
```

**Xử lý nhãn dài**: nhãn TICKER (`entity.code`) trên từng điểm KHÔNG wrap (sẽ phá vỡ vị trí neo
tại điểm), mã đã ngắn sẵn từ tầng dữ liệu; 4 nhãn góc phần tư là `graphic.text` tự do, dùng
`wrapLabel()` nếu đổi sang câu chú thích dài hơn.
**Print-safe**: 1 màu cho mọi điểm (không valence per-entity) + nhãn ticker trực tiếp = đọc được
không cần màu; đường chia trung vị dashed đủ tương phản khi in đen trắng.
**Verify gate riêng**: font trong `graphic` đã import `FONT_STACK`, an toàn với gate #8 (XML).
KHÔNG kiểm được việc 4 câu chú thích góc có bị scatter point đè lên hay không khi dữ liệu đổi ,
phải soi mắt.

═══════════════════════════════════════════════════
## 4. `16-dot-distribution.mjs`, Dot strip phân phối (thay boxplot khi n nhỏ)

**Trả lời**: phân phối 1 chỉ tiêu trong 1-3 nhóm nhỏ (n~5-25 mỗi nhóm) trông thế nào, có ngoại
lệ không, KHÔNG che giấu cỡ mẫu nhỏ như boxplot hay làm. Nhu cầu 5/10 loại báo cáo.
**KHÔNG dùng khi**: n>30-40/nhóm (điểm chồng dày dù có jitter, chuyển sang histogram
matplotlib); cần thống kê tứ phân vị CHÍNH XÁC bằng số (dùng boxplot matplotlib, có sẵn hạ tầng
bảng số); >3-4 nhóm cùng lúc (dùng `07-small-multiples`).

```js
// 16-dot-distribution.mjs, Dot strip phân phối: thay boxplot khi n nhỏ, không giấu cỡ mẫu
// Dùng khi: cần thấy HÌNH DẠNG phân phối 1 chỉ tiêu (vd P/E) của 1-3 nhóm nhỏ (n~5-25),
// và việc thấy TỪNG ĐIỂM (không phải chỉ quartile tóm tắt) quan trọng vì n nhỏ.
// KHÔNG dùng khi: n>30-40 (chồng điểm dù jitter -> histogram matplotlib); cần quartile
// chính xác bằng số (boxplot matplotlib); >3-4 nhóm (07-small-multiples).
// Dữ liệu cần: { group: string, values: number[] }[]. Bẫy: (1) random jitter mỗi lần
// render ra ảnh khác nhau -> dùng công thức TẤT ĐỊNH theo index sau khi sort; (2) tô
// outlier bằng màu cảnh báo (traffic-light) -> mã hoá bằng HÌNH DẠNG (viền rỗng), không
// phải màu; (3) quên vạch trung vị mỗi strip -> mắt không có mốc neo để so 2 nhóm.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtMultiple } from './fmt.mjs';

const groups = [
  { group: 'Thép', values: [8.2, 9.1, 7.5, 10.3, 8.8, 22.4, 9.6, 8.0, 9.9] },
  { group: 'Xi măng', values: [6.5, 7.2, 6.8, 15.9, 7.0, 6.3, 7.4] },
  { group: 'VLXD khác', values: [11.2, 12.5, 10.8, 13.1, 11.9, 12.0, 34.6, 11.5] },
]; // P/E minh hoạ theo phân ngành, KHÔNG phải số thật. 22.4/15.9/34.6 CỐ Ý là outlier để thử nghiệm.

function median(arr) { const s = [...arr].sort((a, b) => a - b); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }
function quartile(arr, q) { const s = [...arr].sort((a, b) => a - b); const pos = (s.length - 1) * q; const lo = Math.floor(pos), hi = Math.ceil(pos); return s[lo] + (s[hi] - s[lo]) * (pos - lo); }
function isOutlier(v, arr) { const q1 = quartile(arr, 0.25), q3 = quartile(arr, 0.75), iqr = q3 - q1; return v < q1 - 1.5 * iqr || v > q3 + 1.5 * iqr; }
// jitter TẤT ĐỊNH theo index sau khi sort trong nhóm (không Math.random -> SVG tái lập được giống hệt mỗi lần chạy)
function jitter(i, band) { const sign = i % 2 === 0 ? 1 : -1; const mag = ((i % 4) + 1) / 4; return sign * mag * band * 0.32; }

const bandHeight = 60;
const points = [];
groups.forEach((g, gi) => {
  const sorted = [...g.values].sort((a, b) => a - b);
  sorted.forEach((v, i) => {
    points.push({ group: g.group, gi, value: v, y: gi + jitter(i, 0.42) / bandHeight, outlier: isOutlier(v, g.values) });
  });
});

const W = 700, H = 60 * groups.length + 160;
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Phân phối P/E theo phân ngành', subtitle: 'Mỗi chấm = 1 mã, vòng rỗng = ngoại lệ (ngoài 1,5×IQR), minh hoạ', width: W, height: H }),
  tooltip: { ...tooltipDefault, formatter: (p) => `${p.data.group}: ${fmtMultiple(p.data.value)}${p.data.outlier ? ' (ngoại lệ)' : ''}` },
  legend: { show: false },
  grid: { left: 100, right: 40, top: 70, bottom: 40 },
  xAxis: { type: 'value', min: 0, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtMultiple(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  yAxis: { type: 'category', data: groups.map((g) => g.group), inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
  series: [
    {
      name: 'Trung vị', type: 'custom', z: 2, silent: true,
      renderItem: (params, api) => {
        const g = groups[params.dataIndex]; const med = median(g.values);
        const y = api.coord([0, params.dataIndex])[1]; const x = api.coord([med, params.dataIndex])[0];
        return { type: 'line', shape: { x1: x, y1: y - 20, x2: x, y2: y + 20 }, style: { stroke: PALETTE.ink, lineWidth: 2 } };
      },
      data: groups.map((g, i) => [0, i]),
    },
    {
      name: 'Mã bình thường', type: 'scatter', z: 3, symbolSize: 9,
      itemStyle: { color: PALETTE.accent, opacity: 0.85 },
      data: points.filter((p) => !p.outlier).map((p) => ({ value: [p.value, p.y], ...p })),
    },
    {
      name: 'Ngoại lệ', type: 'scatter', z: 4, symbolSize: 11,
      itemStyle: { color: PALETTE.paper, borderColor: PALETTE.ink, borderWidth: 2 }, // mã hoá HÌNH DẠNG (viền rỗng), không phải màu cảnh báo
      data: points.filter((p) => p.outlier).map((p) => ({ value: [p.value, p.y], ...p })),
      label: { show: true, formatter: (p) => fmtMultiple(p.data.value, { decimals: 1 }), position: 'top', ...TYPOGRAPHY.dataLabel },
    },
  ],
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-16-dot-distribution.svg', import.meta.url), svg);
console.log('16-dot-distribution: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
```

**Phần mở rộng tuỳ chọn, so 2 kỳ đo (góp ý bổ sung)**: nếu 1 báo cáo cần so phân phối CÙNG 1
nhóm giữa 2 kỳ (vd "P/E ngành Thép trước/sau 1 sự kiện"), thêm field `period: 'current'|'prior'`
vào mỗi điểm, dùng `periodMarkerStyle()` từ `schema.mjs` (mục 00) thay vì `itemStyle` cố định:

```js
import { periodMarkerStyle } from './schema.mjs';
// ...
itemStyle: periodMarkerStyle(p.period, { accent: PALETTE.accent, ink: PALETTE.ink, paper: PALETTE.paper }),
```

Quy ước: kỳ hiện tại = chấm ĐẶC (`accent`), kỳ trước = chấm RỖNG viền đậm (`paper` fill +
`ink` stroke), mã hoá bằng HÌNH DẠNG, không dựa vào cặp màu nào. Đã kiểm bằng luminance BT.709
trước khi chốt cách này: `accentSoft #7D9BFF` (Y≈156/255) và `inkLo #8595A6` (Y≈147/255) chênh
chỉ 9 điểm, gần như không phân biệt được khi in đen trắng/photocopy nếu chọn cặp màu đó cho 2
kỳ, nên hình dạng là lựa chọn an toàn tuyệt đối bất kể cặp hex nào được chọn. Cần thêm 1 dòng
chú giải hình dạng dưới chart ("● Kỳ hiện tại  ○ Kỳ trước") vì đây là mã hoá người đọc chưa quen
mặc định, khác cách đọc legend màu thông thường.

**Xử lý chồng nhãn**: KHÔNG label từng điểm bình thường (n nhỏ nhưng vẫn đủ để 9+ nhãn trên 1
strip cao ~55px chồng chắc chắn), chỉ label các điểm NGOẠI LỆ (thường ≤1-2/nhóm), số còn lại
chỉ có tooltip trên bản HTML, tự thân đủ nghĩa qua VỊ TRÍ trên bản in tĩnh.
**Print-safe**: outlier = viền rỗng (shape), không phải màu, đọc được nguyên vẹn khi khử màu.
**Verify gate riêng**: `jitter()` tất định nên SVG tái lập y hệt mỗi lần chạy, nếu ai sau này
đổi sang `Math.random()`, `npm run verify` VẪN pass (gate không diff nội dung SVG giữa 2 lần
chạy, chỉ đếm cấu trúc + parse XML), một chỗ gate không bắt được, phải tự nhớ giữ tất định.

═══════════════════════════════════════════════════
## 5. `17-football-field.mjs`, Dải định giá nhiều phương pháp

Chuyển thẳng từ mẫu đã duyệt `samples/chart-football-field-dinh-gia.html` sang `.mjs`, giữ
đúng: thứ tự hàng (nội tại trước: DCF, comps EV/EBITDA, comps P/E; quan sát thị trường sau:
giao dịch tiền lệ, biên độ 52 tuần), vùng hội tụ = giao của 3 dải NỘI TẠI (tính TRONG code bằng
`max(lows)`/`min(highs)`, không hardcode số như bản HTML tay), vạch giá thị trường hiện tại.

**Trả lời**: nhiều phương pháp định giá hội tụ về đâu, giá thị trường đứng ở đâu so với định
giá nội tại. 1 trong 2 chart chuẩn ngành ledger đã ghi nợ.
**KHÔNG dùng khi**: <2 phương pháp (không đủ tạo vùng hội tụ, dùng bảng số); các phương pháp
không quy đổi về cùng 1 trục (trộn giá/cp với EV tuyệt đối); thứ tự phương pháp bị xáo trộn
ngẫu nhiên thay vì logic nhất quán (ở đây: nội tại trước, quan sát sau).

**1 thay đổi màu so với mẫu HTML gốc, có lý do**: mẫu tay tô vạch giá thị trường hiện tại bằng
`PALETTE.negative` (đỏ). Đề xuất đổi sang `PALETTE.ink` cho preset `.mjs` chính thức, vì giá
thị trường hiện tại KHÔNG mang nghĩa "xấu/rủi ro" tự thân, dùng `negative` dễ vô tình đọc
thành "giá thị trường là tin xấu". Đây là lựa chọn đề xuất, không phải luật đã chốt, nếu
team-lead thấy đỏ vẫn hợp lý (để nhất quán thị giác với 8 mẫu HTML khác đã duyệt) thì giữ
nguyên `negative`, ghi rõ lý do trong comment (giống cách `09-candlestick.mjs` tự giải thích
lựa chọn màu HOSE).

```js
// 17-football-field.mjs, Football field: dải định giá nhiều phương pháp, vạch giá thị trường
// Dùng khi: tổng hợp nhiều phương pháp định giá (DCF, comps, giao dịch tiền lệ, biên độ
// 52 tuần) thành kết luận VÙNG, thay vì báo cáo N con số rời rạc. Sức mạnh nằm ở VÙNG HỘI
// TỤ (nơi các dải nội tại chồng lên nhau), không phải trung bình cộng mọi dải.
// KHÔNG dùng khi: <2 phương pháp; đơn vị các phương pháp không quy đổi về cùng 1 trục;
// thứ tự phương pháp xáo trộn ngẫu nhiên thay vì logic nhất quán (ở đây: nội tại trước,
// quan sát thị trường sau, khớp mẫu đã duyệt samples/chart-football-field-dinh-gia.html).
// Dữ liệu cần: {method, low, high, type:'intrinsic'|'observed'}[] + currentPrice.
// Bẫy: (1) quên đặt yAxis.inverse -> hàng đầu mảng (DCF) rơi xuống ĐÁY thay vì đỉnh, xem
// mục 0.1; (2) vùng hội tụ tính SAI nếu lấy min/max của MỌI dải thay vì CHỈ 3 dải nội tại
// (giao dịch tiền lệ/biên độ 52 tuần là quan sát, không phải ước tính nội tại, không nên
// gộp vào vùng hội tụ); (3) 2 nhãn low/high ở 2 đầu dải cần đủ margin trái/phải, method có
// low gần 0 dễ bị nhãn "low" đè lên nhãn tên phương pháp bên trái.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, PALETTE, FONT_STACK, FONT_STACK_MONO } from './theme.mjs';
import { fmtNumber } from './fmt.mjs'; // fmtNumber, KHÔNG PHẢI fmtCompact: đây là giá/cp đã quy đổi sẵn ra "nghìn đồng", không phải giá trị tuyệt đối tỷ đồng cần fmtCompact tự chọn đơn vị

// thứ tự hàng = thứ tự đọc mong muốn (trên->dưới): nội tại trước, quan sát sau
const rows = [
  { method: 'DCF (FCFF)', low: 38, high: 52, type: 'intrinsic' },
  { method: 'Comps EV/EBITDA', low: 40, high: 48, type: 'intrinsic' },
  { method: 'Comps P/E', low: 36, high: 46, type: 'intrinsic' },
  { method: 'Giao dịch tiền lệ', low: 44, high: 58, type: 'observed' },
  { method: 'Biên độ 52 tuần', low: 30, high: 50, type: 'observed' },
]; // đơn vị: nghìn đồng/cổ phiếu, minh hoạ 1 công ty niêm yết giả định, KHÔNG phải số thật
const currentPrice = 42;

const intrinsic = rows.filter((r) => r.type === 'intrinsic');
const convLow = Math.max(...intrinsic.map((r) => r.low));
const convHigh = Math.min(...intrinsic.map((r) => r.high));
const hasConvergence = convLow < convHigh; // nếu 3 dải nội tại không giao nhau thì KHÔNG vẽ vùng hội tụ, không bịa

const W = 780, H = 400;
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Định giá tổng hợp: 5 phương pháp', subtitle: 'Đơn vị: nghìn đồng/cổ phiếu, minh hoạ', width: W, height: H }),
  tooltip: { trigger: 'item', formatter: (p) => `${p.data.method}: ${fmtNumber(p.data.low)} - ${fmtNumber(p.data.high)}` },
  legend: { show: false },
  grid: { left: 170, right: 40, top: 60, bottom: 40 },
  xAxis: { type: 'value', min: 0, axisLabel: { color: PALETTE.inkMd, fontFamily: FONT_STACK_MONO, fontSize: 11, formatter: (v) => fmtNumber(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  // yAxis category giả (chỉ để custom series có hệ toạ độ); inverse:true để rows[0] (DCF) ở đỉnh
  yAxis: { type: 'category', data: rows.map((r) => r.method), inverse: true, axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false }, splitLine: { show: false } },
  series: [{
    type: 'custom', z: 2,
    renderItem: (params, api) => {
      const i = params.dataIndex; const row = rows[i];
      const y = api.coord([0, i])[1];
      const xLow = api.coord([row.low, i])[0], xHigh = api.coord([row.high, i])[0];
      const color = row.type === 'intrinsic' ? PALETTE.accent : PALETTE.inkLo;
      return {
        type: 'group',
        children: [
          { type: 'text', style: { text: row.method, x: -12, y, fill: PALETTE.ink, font: `600 13px ${FONT_STACK}`, textAlign: 'right', textVerticalAlign: 'middle' } },
          { type: 'rect', shape: { x: xLow, y: y - 13, width: xHigh - xLow, height: 26, r: 2 }, style: { fill: color } },
          { type: 'text', style: { text: fmtNumber(row.low, { decimals: 0 }), x: xLow - 8, y, fill: PALETTE.ink, font: `700 11px ${FONT_STACK_MONO}`, textAlign: 'right', textVerticalAlign: 'middle' } },
          { type: 'text', style: { text: fmtNumber(row.high, { decimals: 0 }), x: xHigh + 8, y, fill: PALETTE.ink, font: `700 11px ${FONT_STACK_MONO}`, textAlign: 'left', textVerticalAlign: 'middle' } },
        ],
      };
    },
    data: rows.map((r, i) => [i, r.low, r.high]),
  }],
  // vùng hội tụ vẽ SAU series chính bằng graphic (dưới cùng z-order), toạ độ tính thật qua convertToPixel
  graphic: hasConvergence ? (() => {
    const [x1] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [convLow, 0]);
    const [x2] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [convHigh, 0]);
    return [
      { type: 'rect', z: 0, shape: { x: x1, y: 50, width: x2 - x1, height: 260 }, style: { fill: PALETTE.accent, opacity: 0.07 }, silent: true },
      { type: 'text', z: 1, left: (x1 + x2) / 2, top: 42, style: { text: `Vùng hội tụ ${fmtNumber(convLow, { decimals: 0 })}-${fmtNumber(convHigh, { decimals: 0 })}`, font: `700 10px ${FONT_STACK_MONO}`, fill: PALETTE.accentHi, textAlign: 'center' }, silent: true },
    ];
  })() : [],
});

// vạch giá thị trường hiện tại: vẽ SAU cùng để luôn nổi trên các dải, màu ink trung tính
// (KHÔNG dùng negative, xem lý do ở trên, đây là mốc tham chiếu chứ không phải tín hiệu xấu)
{
  const [xp] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [currentPrice, 0]);
  chart.setOption({
    graphic: [
      ...chart.getOption().graphic,
      { type: 'line', z: 3, shape: { x1: xp, y1: 38, x2: xp, y2: 316 }, style: { stroke: PALETTE.ink, lineWidth: 2 }, silent: true },
      { type: 'text', z: 4, left: xp, top: 26, style: { text: `Giá hiện tại: ${fmtNumber(currentPrice, { decimals: 0 })}`, font: `700 10px ${FONT_STACK_MONO}`, fill: PALETTE.ink, textAlign: 'center' }, silent: true },
    ],
  });
}

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-17-football-field.svg', import.meta.url), svg);
console.log('17-football-field: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
```

**Xử lý nhãn dài**: tên phương pháp vẽ bằng `text` trong `renderItem` với `textAlign:'right'`
neo tại `x:-12`, không dùng category axisLabel thật (axis ẩn) để có toàn quyền font-weight như
mẫu HTML gốc. Nếu tên phương pháp dài hơn ~22 ký tự, tăng `grid.left` từ 170 tương ứng
(≈6,6px/ký tự mono) hoặc áp `wrapLabel()` + 2 dòng text (đây là text TỰ DO trong renderItem,
không phải nhãn trục ECharts, nên nguyên tắc "rút gọn ở tầng dữ liệu" của preset 14 không bắt
buộc áp dụng y hệt, nhưng nếu danh sách phương pháp mở rộng và trở thành dữ liệu tái sử dụng,
nên cân nhắc chuyển sang `entity.code`/`entity.name` cho nhất quán).
**Print-safe**: 2 màu accent/inkLo phân biệt nội tại/quan sát, đây LÀ 1 dạng phân loại 2 nhóm
bằng màu nhưng KHÔNG phải valence (không nhóm nào "tốt hơn"), không vi phạm luật; số thật ở 2
đầu MỌI dải nên đọc được cả khi khử màu hoàn toàn.
**Verify gate riêng**: `type:'custom'` renderItem trả `{type:'rect'}` xuất ra `<path>` không
phải `<rect>` (mục 0.3), gate đếm phần tử vẫn qua (regex có `path`), đừng hoảng nếu grep
`<rect` ra 0. `chart.getOption().graphic` ở khối vạch giá thị trường PHẢI gọi SAU khi graphic
vùng hội tụ đã set (tiền lệ an toàn đã có ở `06-tornado.mjs` với `markLine`). Mọi font trong
`renderItem`/`graphic` đều import `FONT_STACK`/`FONT_STACK_MONO`, an toàn với gate #8 (XML).

═══════════════════════════════════════════════════
## 6. `18-sensitivity-grid.mjs`, Lưới độ nhạy 2 chiều

**Trả lời**: kết quả mô hình (giá trị DN) thay đổi ra sao khi 2 biến giả định (WACC × g) cùng
lúc thay đổi, base case ở đâu trong lưới. Chart chuẩn phụ lục DCF, có mẫu HTML đã duyệt
(`chart-luoi-do-nhay-hai-chieu.html`), khác `08-heatmap.mjs` ở chỗ: heatmap hiện có là ma trận
DIVERGING categorical (lãi/lỗ, có cực), còn đây là magnitude field LIÊN TỤC 1 hue (không có
"âm/dương", chỉ có "thấp/cao"), và bắt buộc có 1 ô base case viền riêng, 2 nhu cầu khác nhau
về màu và về việc phải đánh dấu 1 ô đặc biệt, nên đúng là cần preset riêng, không phải trùng
lặp.
**KHÔNG dùng khi**: chỉ có 1 biến độ nhạy (dùng `06-tornado`, gọn hơn); ma trận >6x6 hoặc 7x7
(quá dày để dò mắt); 2 biến không độc lập trong mô hình (kết quả interaction giả tạo).

**Cần đổi `theme.mjs` trước (mục 0.4)**: export `mixHex` + thêm `sequentialScale()`.

**Quyết định thiết kế**: dùng băng màu RỜI RẠC 5 bậc (equal-width bin theo min/max của CHÍNH ma
trận đang vẽ) thay vì `visualMap type:'continuous'` của ECharts, lưới 5x5-7x7 nhỏ, băng rời
rạc dễ so sánh "ô này thuộc bậc nào" hơn gradient liên tục tinh vi, và khớp CHÍNH XÁC cách mẫu
HTML đã duyệt làm. Tự tính band trong JS cũng cho toàn quyền set text màu trắng/đen theo từng ô
mà không phải vật lộn với API màu điều kiện của `visualMap`.

```js
// 18-sensitivity-grid.mjs, Lưới độ nhạy 2 chiều: 2 biến cùng tác động lên 1 kết quả
// Dùng khi: 2 biến giả định thay đổi ĐỒNG THỜI (vd WACC x tăng trưởng dài hạn), kết quả
// là 1 ma trận N x M, cần đánh dấu riêng 1 ô "base case". Khác 06-tornado (1 biến/lúc)
// và khác 08-heatmap (ma trận diverging categorical, không có khái niệm base case).
// KHÔNG dùng khi: 1 biến độ nhạy (dùng 06-tornado); ma trận >6x6-7x7; 2 biến không độc
// lập trong mô hình (kết quả interaction giả).
// Dữ liệu cần: rows[] (giá trị biến 1), cols[] (giá trị biến 2), matrix[row][col],
// baseRowIndex, baseColIndex (chỉ số nguyên, KHÔNG so sánh giá trị float để tìm base).
// Bẫy: (1) dùng thang diverging 2 hue thay vì 1 hue liên tục -> đây là magnitude field,
// không phải delta/so sánh, tô 2 hue sẽ ngầm gán "tốt/xấu" sai; (2) đổi màu NỀN ô base
// case thay vì chỉ đổi VIỀN -> phá liên tục của thang màu; (3) quên set màu chữ theo độ
// đậm ô -> chữ đen trên nền accent đậm nhất KHÔNG đọc được.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, PALETTE, FONT_STACK_MONO, sequentialScale } from './theme.mjs'; // sequentialScale: xem diff đề xuất mục 0.4
import { fmtNumber, fmtPercent } from './fmt.mjs';

const waccRows = [9.0, 9.5, 10.0, 10.5, 11.0]; // %
const gCols = [2.0, 2.5, 3.0, 3.5, 4.0]; // %
const matrix = [
  [940, 965, 995, 1030, 1075],
  [890, 910, 935, 965, 1000],
  [800, 822, 850, 880, 915],
  [735, 752, 772, 795, 822],
  [680, 693, 708, 725, 745],
]; // giá trị doanh nghiệp, tỷ đồng, minh hoạ (khớp base case 850 của 06-tornado.mjs để nhất quán bối cảnh)
const baseRow = 2, baseCol = 2; // WACC 10,0% / g 3,0% = 850, base case CỦA MÔ HÌNH, không suy từ giá trị

const flat = matrix.flat();
const min = Math.min(...flat), max = Math.max(...flat);
const STEPS = 5;
const bandColors = sequentialScale(PALETTE.accent, STEPS);
const bandOf = (v) => Math.min(STEPS - 1, Math.floor(((v - min) / (max - min)) * STEPS));
const isDarkBand = (band) => band >= STEPS - 1; // chỉ bậc đậm nhất mới cần chữ trắng, khớp thực nghiệm ở mẫu HTML đã duyệt

const data = [];
waccRows.forEach((w, ri) => gCols.forEach((g, ci) => {
  const v = matrix[ri][ci];
  const band = bandOf(v);
  const isBase = ri === baseRow && ci === baseCol;
  data.push({
    value: [ci, ri, v],
    itemStyle: {
      color: bandColors[band],
      borderColor: isBase ? PALETTE.ink : PALETTE.paper,
      borderWidth: isBase ? 3 : 2,
    },
    label: { color: isDarkBand(band) ? PALETTE.paper : PALETTE.ink, fontWeight: isBase ? 'bold' : 'normal' },
  });
}));

const W = 700, H = 440;
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Lưới độ nhạy: giá trị doanh nghiệp theo WACC và tăng trưởng dài hạn', subtitle: `Đơn vị: tỷ đồng. Base case WACC ${fmtPercent(waccRows[baseRow], { decimals: 1 })} / g ${fmtPercent(gCols[baseCol], { decimals: 1 })} = ${fmtNumber(matrix[baseRow][baseCol])} (viền đậm)`, width: W, height: H }),
  tooltip: { position: 'top', formatter: (p) => `WACC ${fmtPercent(waccRows[p.data.value[1]], { decimals: 1 })}, g ${fmtPercent(gCols[p.data.value[0]], { decimals: 1 })}: ${fmtNumber(p.data.value[2])} tỷ` },
  grid: { left: 70, right: 24, top: 90, bottom: 70 },
  xAxis: { type: 'category', data: gCols.map((g) => fmtPercent(g, { decimals: 1 })), name: 'Tăng trưởng dài hạn (g)', nameLocation: 'middle', nameGap: 30, splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: PALETTE.ink, fontFamily: FONT_STACK_MONO, fontSize: 11, fontWeight: 'bold' } },
  yAxis: { type: 'category', data: waccRows.map((w) => fmtPercent(w, { decimals: 1 })), name: 'WACC', nameGap: 40, splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: PALETTE.ink, fontFamily: FONT_STACK_MONO, fontSize: 11, fontWeight: 'bold' } },
  series: [{
    type: 'heatmap', data,
    label: { show: true, formatter: (p) => fmtNumber(p.data.value[2]), fontSize: 12, fontFamily: FONT_STACK_MONO },
  }],
  // legend thang màu tự vẽ (KHÔNG dùng visualMap component, xem lý do trên)
  graphic: [
    { type: 'text', left: 70, top: H - 30, style: { text: 'Thấp', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
    ...bandColors.map((c, i) => ({ type: 'rect', left: 110 + i * 40, top: H - 34, shape: { width: 34, height: 12 }, style: { fill: c } })),
    { type: 'text', left: 110 + STEPS * 40 + 6, top: H - 30, style: { text: 'Cao', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
    { type: 'text', left: 110 + STEPS * 40 + 50, top: H - 30, style: { text: '1 hue liên tục, không traffic-light', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
  ],
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-18-sensitivity-grid.svg', import.meta.url), svg);
console.log('18-sensitivity-grid: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
```

**Xử lý nhãn dài**: không áp dụng trực tiếp (nhãn trục chỉ là % 4-5 ký tự), nếu mở rộng ma
trận thêm 1 biến thứ 3 dạng phân loại, khuyến nghị KHÔNG nhồi vào cùng lưới mà tách thành
`07-small-multiples` của nhiều lưới 5x5, mỗi ô lớn = 1 kịch bản.
**Print-safe**: MỌI ô có số thật bất kể màu (bắt buộc, đã làm), băng màu rời rạc rõ ràng hơn
gradient khi photocopy đen trắng.
**Verify gate riêng**: rủi ro lớn nhất là gate #5/#8 nếu quên set `fontFamily` trên các phần tử
`graphic` của legend tự vẽ, đã set tường minh `FONT_STACK_MONO` import ở cả 4 khối text, không
gõ tay, an toàn với cả 2 gate. Gate KHÔNG kiểm được việc `isDarkBand()` chọn đúng ngưỡng (chữ
trắng/đen tương phản đủ) khi đổi `PALETTE.accent` hoặc đổi dữ liệu khiến phân bố band lệch ,
phải mở SVG nhìn.

═══════════════════════════════════════════════════
## Danh sách việc cần làm, theo thứ tự

1. Sửa `theme.mjs`: export `mixHex`, thêm `sequentialScale()` (mục 0.4), không đổi
   `bandLo/Mid/Hi` hiện có.
2. Tạo `charts/echarts/schema.mjs` (nội dung ở mục 00) TRƯỚC khi viết bất kỳ preset nào.
3. Viết 6 file theo đúng code ở mục 1-6 (đã verify 3 cơ chế kỹ thuật mới bằng thực nghiệm:
   `convertToPixel` trong SSR, `custom renderItem` trả group{rect+text}, `yAxis.inverse`; và đã
   tự rà lại để không tái tạo bug nháy kép ở mục 0.5, mọi font đều import từ `theme.mjs`).
4. Chạy `node scripts/verify-charts.mjs`, kỳ vọng PASS cả 12 file cũ (đã vá mục 0.1/0.5) + 6
   file mới (7 file SVG kể cả `-dot.svg` bonus của preset 14), qua đủ cả 8 gate kể cả gate XML
   mới.
5. Mở TỪNG file SVG mới bằng mắt (không chỉ tin gate đếm/parse), đặc biệt kiểm chồng nhãn ở 13
   (sự kiện gần nhau) và 15 (ticker gần nhau), gate không bắt được việc này.
6. Việc ngoài phạm vi 6 preset này, cần task riêng: `charts/matplotlib/schema.py` đồng bộ field
   name với `schema.mjs` phía ECharts; cân nhắc áp `periodMarkerStyle()` cho `04-dumbbell.mjs`/
   `05-slope.mjs` đã có sẵn nếu review muốn.

Không phát hiện preset nào trong 6 cái nên bỏ hoặc gộp, cả 6 đều lấp đúng lỗ hổng đã đo bằng số
trong `research/13-chart-component-gap/FINDINGS.md`, không cái nào là biến thể vẽ lại của
preset đã có.
