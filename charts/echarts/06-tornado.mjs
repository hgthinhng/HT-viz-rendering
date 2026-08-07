// 06-tornado.mjs — Tornado: phân tích độ nhạy định giá (DCF/LBO sensitivity)
// Dùng khi: cho thấy biến nào tác động mạnh nhất lên 1 kết quả (giá trị DN,
// EPS...) khi thay đổi trong 1 khoảng giả định — sắp theo |biên độ| giảm dần
// để biến quan trọng nhất nằm trên cùng (đúng hình dạng "cái phễu lốc").
// Dữ liệu cần: {variable, low, high, base} — low/high là kết quả khi biến đó
// ở kịch bản bi quan/lạc quan, base là giá trị trung tâm để tính lệch.
// Bẫy thường gặp: (1) KHÔNG sắp theo biên độ -> mất hình phễu, khó đọc;
// (2) dùng 2 màu tuỳ ý cho low/high thay vì nhất quán xuyên suốt mọi biến;
// (3) qua dùng nhãn % mà không neo rõ base case.
// LƯU Ý MÀU: đây là NHẬN ĐỊNH SO SÁNH (dải kịch bản quanh 1 base case tĩnh,
// không phải delta thời gian), không phải cầu nối P&L. Bi quan = negative
// (bất lợi trong so sánh, được phép); lạc quan PHẢI trung tính, KHÔNG tô
// accent, vì "kịch bản tốt hơn = xanh dương" chính là tô màu dương cho bên có
// lợi, dạng traffic-light bị cấm dù đội lốt "chỉ là tô theo chiều tăng/giảm".
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';

const base = 850; // tỷ đồng, giá trị doanh nghiệp base case
const raw = [
  { variable: 'WACC (±1.5đpt)', low: 720, high: 1010 },
  { variable: 'Tăng trưởng dài hạn (±0.5đpt)', low: 790, high: 925 },
  { variable: 'Biên EBITDA (±2đpt)', low: 810, high: 895 },
  { variable: 'Vốn đầu tư/DThu (±1đpt)', low: 830, high: 875 },
  { variable: 'Thuế suất hiệu dụng (±2đpt)', low: 838, high: 862 },
];
const rows = [...raw].sort((a, b) => (b.high - b.low) - (a.high - a.low)); // sắp theo biên độ giảm dần
const categories = rows.map((r) => r.variable);

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 720, height: 380 });
chart.setOption({
  ...baseOption({ title: 'Phân tích độ nhạy giá trị doanh nghiệp (DCF)', subtitle: `Base case = ${fmtCompact(base, { baseUnit: 'ty', decimals: 0 })}, sắp theo biên độ tác động` }),
  tooltip: tooltipDefault,
  grid: { left: 200, right: 40, top: 60, bottom: 40 },
  xAxis: {
    type: 'value',
    axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtCompact(v + base, { baseUnit: 'ty', decimals: 0 }) },
    splitLine: { lineStyle: { color: PALETTE.line } },
  },
  yAxis: { type: 'category', data: categories, inverse: true, // phễu lốc: biên độ lớn nhất phải ở TRÊN CÙNG; ECharts mac dinh dat index 0 o DAY nen phai dao truc, khong dao thi hinh ra nguoc voi y dinh ghi o dau file
         axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
  series: [
    {
      name: 'Kịch bản bi quan', type: 'bar', stack: 'range', barWidth: 22,
      itemStyle: { color: PALETTE.negative },
      data: rows.map((r) => r.low - base),
      label: { show: true, position: 'left', formatter: (p) => fmtCompact(p.value + base, { baseUnit: 'ty', decimals: 0 }), ...TYPOGRAPHY.dataLabel },
    },
    {
      name: 'Kịch bản lạc quan', type: 'bar', stack: 'range', barWidth: 22,
      itemStyle: { color: PALETTE.inkLo },
      data: rows.map((r) => r.high - base),
      label: { show: true, position: 'right', formatter: (p) => fmtCompact(p.value + base, { baseUnit: 'ty', decimals: 0 }), ...TYPOGRAPHY.dataLabel },
    },
  ],
  markLine: undefined,
});

// vạch base-case ở x=0
const opt = chart.getOption();
opt.series[0].markLine = {
  silent: true,
  symbol: 'none',
  lineStyle: { color: PALETTE.ink, type: 'solid', width: 1.5 },
  label: { formatter: 'Base', ...TYPOGRAPHY.axisName },
  data: [{ xAxis: 0 }],
};
chart.setOption(opt);

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-06-tornado.svg', import.meta.url), svg);
console.log('06-tornado: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));

chart.dispose();
process.exit(0);
