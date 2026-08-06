// 11-stacked-100.mjs — Stacked bar 100%: cơ cấu tỷ trọng qua thời gian
// Dùng khi: quan tâm TỶ TRỌNG (luôn cộng =100%) hơn giá trị tuyệt đối, vd cơ
// cấu nguồn vốn (nợ vay/vốn CSH), cơ cấu doanh thu theo kênh bán.
// Dữ liệu cần: {period, [category]: %} với tổng mỗi period = 100.
// Bẫy thường gặp: (1) tổng không đúng 100 do làm tròn từng phần riêng lẻ ->
// phải kiểm tổng SAU KHI làm tròn, chỉnh phần lớn nhất để bù sai số làm tròn;
// (2) quá 4-5 khoảng -> khó theo dõi 1 dải cụ thể qua thời gian, nên gộp đuôi
// nhỏ vào "Khác"; (3) thứ tự xếp chồng đổi giữa các cột -> phải CỐ ĐỊNH thứ
// tự category xuyên suốt mọi cột.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';

const periods = ['2023', '2024', '2025', '2026'];
// thứ tự category CỐ ĐỊNH xuyên suốt: Nợ vay ngắn hạn / Nợ vay dài hạn / Vốn chủ sở hữu
const rows = {
  'Nợ vay ngắn hạn': [22, 19, 24, 18],
  'Nợ vay dài hạn': [35, 38, 30, 32],
  'Vốn chủ sở hữu': [43, 43, 46, 50],
};
// kiểm tổng mỗi cột phải = 100 sau làm tròn
periods.forEach((_, i) => {
  const total = Object.values(rows).reduce((s, arr) => s + arr[i], 0);
  if (total !== 100) throw new Error(`Cot ${periods[i]} tong=${total} != 100`);
});

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 680, height: 380 });
chart.setOption({
  ...baseOption({ title: 'Cơ cấu nguồn vốn, 2023–2026', subtitle: 'Đơn vị: % tổng nguồn vốn, thứ tự xếp chồng cố định' }),
  tooltip: { ...tooltipDefault, valueFormatter: (v) => fmtPercent(v, { decimals: 0 }) },
  grid: { left: 56, right: 24, top: 60, bottom: 60 },
  xAxis: { type: 'category', data: periods, axisLine: { lineStyle: { color: PALETTE.axisLine } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
  yAxis: { type: 'value', max: 100, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => v + '%' }, splitLine: { lineStyle: { color: PALETTE.gridline } } },
  color: [PALETTE.negative, PALETTE.neutralMid, PALETTE.accent], // nợ ngắn hạn=đỏ (rủi ro thanh khoản), nợ dài hạn=xám, VCSH=accent
  series: Object.entries(rows).map(([name, data]) => ({
    name, type: 'bar', stack: 'total', barWidth: 44, data,
    label: { show: true, formatter: (p) => fmtPercent(p.value, { decimals: 0 }), color: '#fff', ...TYPOGRAPHY.dataLabel },
  })),
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-11-stacked-100.svg', import.meta.url), svg);
console.log('11-stacked-100: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
