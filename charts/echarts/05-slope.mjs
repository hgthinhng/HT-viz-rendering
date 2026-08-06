// 05-slope.mjs — Slope chart: đổi thứ hạng/giá trị giữa 2 mốc cho nhiều thực thể
// Dùng khi: "thị phần các ngân hàng thay đổi thế nào từ 2025 sang 2026" —
// khác dumbbell ở chỗ slope nhấn TRỤC THỜI GIAN có hướng (trái->phải), dumbbell
// nhấn CHÊNH LỆCH không có ý niệm thời gian rõ. Slope hợp khi >4-5 thực thể vì
// độ dốc đường nói lên "ai tăng nhanh hơn ai" ngay cả khi không đổi hạng.
// Dữ liệu cần: {label, t1, t2} cho từng thực thể.
// Bẫy thường gặp: (1) >6-8 đường thì nhãn chồng nhau, phải chọn nhấn 1-2 thực
// thể (emphasis) và làm mờ phần còn lại; (2) 2 trục x không đều khoảng cách
// thời gian thực (slope chart giả định khoảng cách đều, ghi rõ nếu không đều).
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';

const entities = [
  { label: 'VCB', t1: 18.2, t2: 17.5, highlight: false },
  { label: 'TCB', t1: 9.1, t2: 11.8, highlight: true }, // câu chuyện: TCB tăng nhanh nhất
  { label: 'MBB', t1: 8.4, t2: 9.0, highlight: false },
  { label: 'ACB', t1: 7.9, t2: 7.6, highlight: false },
  { label: 'VPB', t1: 7.2, t2: 8.1, highlight: false },
];

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 700, height: 400 });
const series = entities.map((e) => ({
  name: e.label,
  type: 'line',
  data: [e.t1, e.t2],
  symbolSize: 8,
  lineStyle: { width: e.highlight ? 3 : 1.5, color: e.highlight ? PALETTE.accent : PALETTE.inkLo },
  itemStyle: { color: e.highlight ? PALETTE.accent : PALETTE.inkLo },
  label: {
    show: true,
    formatter: (p) => `${e.label} ${fmtPercent(p.value, { decimals: 1 })}`,
    color: e.highlight ? PALETTE.ink : PALETTE.inkLo,
    fontWeight: e.highlight ? 'bold' : 'normal',
    position: (p) => (p.dataIndex === 0 ? 'left' : 'right'),
    ...TYPOGRAPHY.dataLabel,
  },
  z: e.highlight ? 5 : 1,
}));

chart.setOption({
  ...baseOption({ title: 'Thị phần tín dụng: Q4/2025 so với Q4/2026', subtitle: 'Đơn vị: %, nhấn mạnh TCB (tăng nhanh nhất)' }),
  tooltip: tooltipDefault,
  legend: { show: false },
  grid: { left: 90, right: 90, top: 60, bottom: 40 },
  xAxis: { type: 'category', data: ['Q4/2025', 'Q4/2026'], boundaryGap: false, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel, splitLine: { show: false } },
  yAxis: { type: 'value', show: false, min: 0 },
  series,
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-05-slope.svg', import.meta.url), svg);
console.log('05-slope: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));

chart.dispose();
process.exit(0);
