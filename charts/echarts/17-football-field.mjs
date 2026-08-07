// 17-football-field.mjs — Football field: dải định giá nhiều phương pháp, vạch giá thị trường
// Dùng khi: tổng hợp nhiều phương pháp định giá (DCF, comps, giao dịch tiền lệ, biên độ
// 52 tuần) thành kết luận VÙNG, thay vì báo cáo N con số rời rạc. Sức mạnh nằm ở VÙNG HỘI
// TỤ (nơi các dải NỘI TẠI chồng lên nhau), không phải trung bình cộng mọi dải.
// KHÔNG dùng khi: <2 phương pháp (không đủ tạo vùng hội tụ có nghĩa, dùng bảng số); các
// phương pháp không quy đổi về cùng 1 trục (trộn giá/cp với EV tuyệt đối); thứ tự phương
// pháp xáo trộn ngẫu nhiên thay vì logic nhất quán (ở đây: nội tại trước, quan sát thị
// trường sau, khớp mẫu đã duyệt samples/chart-football-field-dinh-gia.html).
// Dữ liệu cần: series schema dùng chung (charts/echarts/schema.mjs), rows là
// {entity:{code}, low, high, group}[] + currentPrice riêng (không phải 1 hàng xếp hạng).
// entity.code ở đây CHÍNH LÀ tên phương pháp đầy đủ có dấu (vd "Giao dịch tiền lệ"), vì
// schema không ép viết hoa không dấu, chỉ ép NGẮN <=24 ký tự -- mọi tên phương pháp trong
// mẫu đều đủ ngắn nên không cần rút gọn thêm.
// Bẫy: (1) quên yAxis.inverse:true -> hàng đầu mảng (DCF) rơi xuống ĐÁY thay vì đỉnh; (2)
// vùng hội tụ tính SAI nếu lấy min/max của MỌI dải thay vì CHỈ dải group:'intrinsic'
// (giao dịch tiền lệ/biên độ 52 tuần là quan sát thị trường, không phải ước tính nội tại,
// không gộp vào vùng hội tụ); (3) 2 nhãn low/high ở 2 đầu dải cần đủ margin trái/phải,
// method có low gần biên trục dễ bị nhãn "low" đè lên nhãn tên phương pháp bên trái, PHẢI
// mở SVG nhìn thật (gate chỉ đếm phần tử, không đo va chạm hình học).
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, PALETTE, FONT_STACK, FONT_STACK_MONO, TYPOGRAPHY } from './theme.mjs';
import { fmtNumber } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi } from './schema.mjs';

// thứ tự hàng = thứ tự đọc mong muốn (trên -> dưới): nội tại (DCF, comps) trước, quan sát
// thị trường (giao dịch tiền lệ, biên độ 52 tuần) sau, khớp mẫu đã duyệt.
const series = {
  unit: 'nghin_dong_cp',
  source: { tier: 'uoc-tinh', label: 'Mô hình định giá nội bộ, minh hoạ' },
  as_of: '2026-08-07',
  decimals: 0, // ghi đè mặc định vocab (1): giá/cp trên dải đọc gọn hơn ở số nguyên, khớp mẫu HTML đã duyệt ("38" chứ không phải "38,0")
  rows: [
    { entity: { code: 'DCF (FCFF)' }, low: 38, high: 52, group: 'intrinsic' },
    { entity: { code: 'Comps EV/EBITDA' }, low: 40, high: 48, group: 'intrinsic' },
    { entity: { code: 'Comps P/E' }, low: 36, high: 46, group: 'intrinsic' },
    { entity: { code: 'Giao dịch tiền lệ' }, low: 44, high: 58, group: 'observed' },
    { entity: { code: 'Biên độ 52 tuần' }, low: 30, high: 50, group: 'observed' },
  ], // đơn vị nghìn đồng/cổ phiếu, minh hoạ 1 công ty niêm yết giả định, KHÔNG phải số thật
};
series.rows = series.rows.map((r) => ({ ...r, value: Math.round((r.low + r.high) / 2) })); // schema đòi mỗi hàng có 1 value số thực (status mặc định co_that) -- dùng trung điểm dải làm giá trị đại diện cho hàng, low/high vẫn giữ nguyên để vẽ dải
validateSeries(series); // FAIL ngay nếu entity.code quá dài hoặc thiếu unit/source
const rows = series.rows;
const decimals = soThapPhan(series);
const donVi = nhanDonVi(series.unit);

const currentPrice = 42; // giá thị trường hiện tại: 1 mốc tham chiếu riêng, không phải 1 hàng trong lượt xếp hạng nên không đi qua schema hàng

// vùng hội tụ = giao CỦA CHỈ các dải group:'intrinsic', tính TRONG code bằng max(lows)/
// min(highs), KHÔNG gộp dải quan sát thị trường, KHÔNG hardcode số như bản HTML tay.
const intrinsicRows = rows.filter((r) => r.group === 'intrinsic');
const convLow = Math.max(...intrinsicRows.map((r) => r.low));
const convHigh = Math.min(...intrinsicRows.map((r) => r.high));
const hasConvergence = intrinsicRows.length >= 2 && convLow < convHigh; // nếu các dải nội tại không giao nhau thì KHÔNG vẽ vùng hội tụ, không bịa

const W = 780, H = 450;
const GRID = { left: 195, right: 56, top: 96, bottom: 64 };
const plotTop = GRID.top;
const plotBottom = H - GRID.bottom;

// KHÔNG dùng scale:true để auto-suy min/max: series 'custom' không tự khai encode nên
// ECharts suy trục giá trị từ CHIỀU ĐẦU của mảng data ([i, low, high] -> lấy nhầm chỉ số
// hàng 0..4 làm miền giá trị, đã tự bắt lỗi này bằng ảnh chụp thật, trục ra 0-4 thay vì
// 25-65). Tự tính min/max từ chính dữ liệu low/high/currentPrice, làm tròn bậc 5 cho dễ
// đọc. KHÔNG ép bắt đầu từ 0: đây là toạ độ giá tuyệt đối (khoảng min-max của 1 dải),
// không phải magnitude từ gốc -- cùng ngoại lệ đã có tiền lệ ở 09-candlestick.mjs cho
// trục giá OHLC, và khớp mẫu HTML đã duyệt (trục bắt đầu từ 25, không phải 0).
const priceExtent = [...rows.map((r) => r.low), ...rows.map((r) => r.high), currentPrice];
const dataMin = Math.min(...priceExtent), dataMax = Math.max(...priceExtent);
const pad = (dataMax - dataMin) * 0.12;
const axisMin = Math.max(0, Math.floor((dataMin - pad) / 5) * 5);
const axisMax = Math.ceil((dataMax + pad) / 5) * 5;

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });
chart.setOption({
  ...baseOption({ title: 'Định giá tổng hợp: 5 phương pháp', subtitle: `Đơn vị: ${donVi}, minh hoạ, không phải số thật`, width: W, height: H }),
  tooltip: { trigger: 'item', formatter: (p) => `${rows[p.dataIndex].entity.code}: ${fmtNumber(rows[p.dataIndex].low, { decimals })} - ${fmtNumber(rows[p.dataIndex].high, { decimals })}` },
  legend: { show: false },
  grid: GRID,
  xAxis: {
    type: 'value',
    min: axisMin, max: axisMax,
    axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtNumber(v, { decimals }) },
    splitLine: { lineStyle: { color: PALETTE.line } },
  },
  // yAxis category giả (chỉ để custom series có hệ toạ độ, nhãn thật vẽ tay trong
  // renderItem để toàn quyền font-weight); inverse:true để rows[0] (DCF) ở đỉnh
  yAxis: { type: 'category', data: rows.map((r) => r.entity.code), inverse: true, axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false }, splitLine: { show: false } },
  series: [{
    type: 'custom', z: 2,
    renderItem: (params, api) => {
      const i = params.dataIndex;
      const row = rows[i];
      const y = api.coord([0, i])[1];
      const xLow = api.coord([row.low, i])[0];
      const xHigh = api.coord([row.high, i])[0];
      const barColor = row.group === 'intrinsic' ? PALETTE.accent : PALETTE.inkLo;
      const valueColor = row.group === 'intrinsic' ? PALETTE.ink : PALETTE.inkMd;
      return {
        type: 'group',
        children: [
          // x là toạ độ PIXEL TUYỆT ĐỐI trên toàn canvas (giống api.coord ở trên), không
          // phải toạ độ tương đối trong group -- đặt "-14" trần sẽ rơi ra ngoài canvas về
          // phía trái (đã tự bắt lỗi này bằng ảnh chụp thật, nhãn tên phương pháp biến
          // mất). Neo đúng ngay sát mép trái của grid.
          { type: 'text', style: { text: row.entity.code, x: GRID.left - 14, y, fill: PALETTE.ink, font: `600 13px ${FONT_STACK}`, textAlign: 'right', textVerticalAlign: 'middle' } },
          { type: 'rect', shape: { x: xLow, y: y - 13, width: xHigh - xLow, height: 26, r: 2 }, style: { fill: barColor } },
          { type: 'text', style: { text: fmtNumber(row.low, { decimals }), x: xLow - 8, y, fill: valueColor, font: `700 11px ${FONT_STACK_MONO}`, textAlign: 'right', textVerticalAlign: 'middle' } },
          { type: 'text', style: { text: fmtNumber(row.high, { decimals }), x: xHigh + 8, y, fill: valueColor, font: `700 11px ${FONT_STACK_MONO}`, textAlign: 'left', textVerticalAlign: 'middle' } },
        ],
      };
    },
    // data chỉ cần đúng số phần tử để ECharts cấp dataIndex cho renderItem -- nội dung
    // thật lấy từ closure `rows` phía trên, KHÔNG qua api.value() (tiền lệ 0.3 trong đặc
    // tả: {type:'rect'} trả ra <path> trong SVG, không phải <rect>, không ảnh hưởng gì).
    data: rows.map((r, i) => [i, r.low, r.high]),
  }],
});

// Toàn bộ lớp chú thích (vùng hội tụ, vạch giá thị trường, 2 chú giải màu) gom vào MỘT
// mảng rồi setOption MỘT lần duy nhất ở cuối. Đã thử tách 3 lần setOption riêng, nối tiếp
// bằng `chart.getOption().graphic` như tiền lệ markLine ở 06-tornado.mjs -- KHÔNG áp dụng
// được cho graphic: getOption().graphic trả về dạng bọc `[{elements:[...]}]` chứ không
// phải mảng phẳng đã đưa vào, spread lại tạo ra 1 phần tử group lẫn với phần tử rời rạc
// cùng cấp, ECharts âm thầm bỏ qua các phần tử thêm sau (đã tự bắt lỗi này bằng ảnh chụp
// thật: vạch giá thị trường và 2 chú giải màu biến mất hoàn toàn). convertToPixel vẫn
// dùng được ngay sau setOption đầu tiên (chỉ cần trục đã có, không cần graphic đã tồn
// tại), nên tính toạ độ trước, gom lại, rồi set 1 lần.
const graphics = [];

// LƯU Ý CHUNG cho mọi 'text' dưới đây: toạ độ đặt trong style.x/style.y (giống renderItem
// ở trên), KHÔNG dùng top-level left/top khi có style.textAlign khác mặc định -- đã tự bắt
// lỗi bằng ảnh chụp thật (top-level left + style.textAlign:'right'/'center' cho toạ độ x
// lệch hẳn ra ngoài canvas, vì ECharts đo bounding box theo neo trái mặc định rồi mới áp
// text-anchor, làm lệch kép). Cùng phát hiện đã có ở 13-line-annotated.mjs và
// 15-quadrant-scatter.mjs (bản đó dùng `right:` cho neo phải, ở đây dùng style.x/y cho cả
// 3 kiểu neo trái/giữa/phải vì cần neo GIỮA cho nhãn vùng hội tụ, `right:` không giải
// quyết được trường hợp giữa).

// vùng hội tụ = giao CỦA CHỈ các dải nội tại, không hardcode như bản HTML tay
if (hasConvergence) {
  const [x1] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [convLow, 0]);
  const [x2] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [convHigh, 0]);
  graphics.push(
    { type: 'rect', z: 0, shape: { x: x1, y: plotTop - 4, width: x2 - x1, height: (plotBottom + 4) - (plotTop - 4) }, style: { fill: PALETTE.accent, opacity: 0.07 }, silent: true },
    { type: 'text', z: 1, style: { x: (x1 + x2) / 2, y: plotTop - 24, text: `Vùng hội tụ ${fmtNumber(convLow, { decimals })}-${fmtNumber(convHigh, { decimals })}`, font: `700 10px ${FONT_STACK_MONO}`, fill: PALETTE.accentHi, textAlign: 'center' }, silent: true },
  );
}

// vạch giá thị trường hiện tại: z cao nhất để luôn nổi trên các dải và vùng hội tụ. Màu
// ink trung tính (KHÔNG dùng negative): giá thị trường hiện tại không mang nghĩa "xấu/rủi
// ro" tự thân, tô đỏ dễ vô tình đọc thành "giá thị trường là tin xấu" -- đây là 1 mốc tham
// chiếu chứ không phải 1 tín hiệu cảnh báo, khác cách dùng negative cho kịch bản bất lợi.
{
  const [xp] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [currentPrice, 0]);
  graphics.push(
    { type: 'line', z: 3, shape: { x1: xp, y1: 34, x2: xp, y2: plotBottom + 4 }, style: { stroke: PALETTE.ink, lineWidth: 2 }, silent: true },
    { type: 'text', z: 4, style: { x: xp, y: 18, text: `Giá hiện tại: ${fmtNumber(currentPrice, { decimals })}`, font: `700 10px ${FONT_STACK_MONO}`, fill: PALETTE.ink, textAlign: 'center' }, silent: true },
  );
}

// 2 chú giải màu ở chân chart -- annotation-first, không dùng legend ECharts vì chỉ có 2
// nhóm màu cố định xuyên suốt mọi hàng, ghi 1 lần dưới chart gọn hơn legend interactive.
graphics.push(
  { type: 'text', style: { x: GRID.left, y: H - 28, text: 'Giá trị nội tại/ước tính (xanh dương)', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo } },
  { type: 'text', style: { x: W - GRID.right, y: H - 28, text: 'Giá quan sát thị trường (xám)', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo, textAlign: 'right' } },
);

chart.setOption({ graphic: graphics });

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-17-football-field.svg', import.meta.url), svg);
console.log('17-football-field: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
