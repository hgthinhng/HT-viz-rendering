// 04-dumbbell.mjs — Dumbbell: so 2 thời điểm cho nhiều hạng mục cùng lúc
// Dùng khi: "biên lợi nhuận gộp từng mảng kinh doanh thay đổi ra sao từ
// 2025 sang 2026" — tốt hơn 2 cột cạnh nhau vì nhấn vào ĐỘ CHÊNH LỆCH,
// không phải giá trị tuyệt đối từng cột.
// Dữ liệu cần: danh sách {label, before, after}. Nên SẮP THEO độ chênh lệch
// (ranking rule của FT) để mắt đọc pattern nhanh hơn.
// Bẫy thường gặp: (1) không sắp xếp -> nhìn như nhiễu; (2) dùng 2 màu tuỳ ý
// cho before/after thay vì 1 hue 2 sắc độ (trước=nhạt, sau=đậm) -> đọc thành
// 2 series không liên quan thay vì "trước->sau" của CÙNG một thực thể;
// (3) không note chiều mũi tên/nhãn -> không biết bên nào là "sau".
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';

const raw = [
  { label: 'Bán lẻ', before: 18.2, after: 22.5 },
  { label: 'Bất động sản KCN', before: 34.0, after: 31.2 },
  { label: 'Vật liệu xây dựng', before: 12.5, after: 14.1 },
  { label: 'Logistics', before: 15.8, after: 15.1 },
  { label: 'Năng lượng tái tạo', before: 26.4, after: 33.0 },
];
// sắp theo |chênh lệch| giảm dần (ranking rule)
const rows = [...raw].sort((a, b) => Math.abs(b.after - b.before) - Math.abs(a.after - a.before));
const categories = rows.map((r) => r.label);

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 700, height: 380 });
chart.setOption({
  ...baseOption({ title: 'Biên lợi nhuận gộp theo mảng: 2025 so với 2026', subtitle: 'Đơn vị: %, sắp theo mức thay đổi' }),
  tooltip: tooltipDefault,
  grid: { left: 150, right: 60, top: 60, bottom: 40 },
  xAxis: { type: 'value', name: '%', axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtPercent(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
  yAxis: { type: 'category', data: categories, inverse: true, // sắp theo độ chênh: chênh lớn nhất phải ở TRÊN CÙNG; ECharts mac dinh dat index 0 o DAY nen phai dao truc, khong dao thi hinh ra nguoc voi y dinh ghi o dau file
         axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
  series: [
    {
      name: 'Đoạn nối', type: 'custom', z: 1,
      renderItem: (params, api) => {
        const y = api.coord([0, params.dataIndex])[1];
        const x1 = api.coord([api.value(1), params.dataIndex])[0];
        const x2 = api.coord([api.value(2), params.dataIndex])[0];
        return { type: 'line', shape: { x1, y1: y, x2, y2: y }, style: { stroke: PALETTE.line, lineWidth: 4 } };
      },
      data: rows.map((r) => [0, r.before, r.after]),
      encode: { x: [1, 2], y: 0 },
    },
    {
      name: '2025', type: 'scatter', symbolSize: 14, z: 3,
      itemStyle: { color: PALETTE.inkLo },
      data: rows.map((r) => r.before),
      label: { show: true, formatter: (p) => fmtPercent(p.value, { decimals: 1 }), position: 'top', ...TYPOGRAPHY.dataLabel, color: PALETTE.inkMd },
    },
    {
      name: '2026', type: 'scatter', symbolSize: 14, z: 4,
      itemStyle: { color: PALETTE.accent },
      data: rows.map((r) => r.after),
      label: { show: true, formatter: (p) => fmtPercent(p.value, { decimals: 1 }), position: 'top', ...TYPOGRAPHY.dataLabel },
    },
  ],
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-04-dumbbell.svg', import.meta.url), svg);
console.log('04-dumbbell: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));

chart.dispose();
process.exit(0);
