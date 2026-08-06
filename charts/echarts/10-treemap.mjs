// 10-treemap.mjs — Treemap: cơ cấu vốn hoá/doanh thu theo ngành-mã
// Dùng khi: thể hiện phần-trong-tổng của NHIỀU hạng mục (>8-10) mà stacked bar
// sẽ quá chật — diện tích ô = độ lớn, phân cụm = nhóm cha (ngành).
// Dữ liệu cần: cây 2 cấp {group, name, value}. Không hợp khi cần so sánh
// CHÍNH XÁC 2 giá trị gần nhau (mắt người ước lượng diện tích kém hơn chiều dài).
// Bẫy thường gặp: (1) tô màu ngẫu nhiên theo từng ô lá thay vì theo NHÓM CHA
// (categorical theo group, sắc độ theo con) -> mất cấu trúc phân cấp;
// (2) nhãn bị cắt chữ trong ô quá nhỏ -> phải ẩn nhãn khi ô < ngưỡng, không
// dùng overflow:hidden cắt chữ nham nhở; (3) quá nhiều nhóm cha (>5-6) làm
// bảng màu categorical vượt ngưỡng an toàn CVD.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';

// nhóm cha = ngành (categorical, tối đa 4 để an toàn CVD all-pairs theo dataviz skill)
const groupColor = { 'Ngân hàng': PALETTE.accent, 'Bất động sản': PALETTE.ink, 'Tiêu dùng': PALETTE.inkLo, 'Năng lượng': PALETTE.accentHi };
const data = [
  { name: 'Ngân hàng', itemStyle: { color: groupColor['Ngân hàng'] }, children: [
    { name: 'VCB', value: 480 }, { name: 'BID', value: 310 }, { name: 'CTG', value: 260 }, { name: 'TCB', value: 190 },
  ]},
  { name: 'Bất động sản', itemStyle: { color: groupColor['Bất động sản'] }, children: [
    { name: 'VHM', value: 220 }, { name: 'VIC', value: 180 }, { name: 'NVL', value: 40 },
  ]},
  { name: 'Tiêu dùng', itemStyle: { color: groupColor['Tiêu dùng'] }, children: [
    { name: 'MSN', value: 95 }, { name: 'VNM', value: 130 }, { name: 'SAB', value: 70 },
  ]},
  { name: 'Năng lượng', itemStyle: { color: groupColor['Năng lượng'] }, children: [
    { name: 'GAS', value: 150 }, { name: 'POW', value: 55 },
  ]},
];

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 720, height: 420 });
chart.setOption({
  backgroundColor: PALETTE.paper,
  textStyle: { fontFamily: FONT_STACK },
  title: { text: 'Cơ cấu vốn hoá theo ngành và mã (minh hoạ VN30)', subtext: 'Đơn vị: nghìn tỷ đồng, màu theo NHÓM NGÀNH, diện tích theo vốn hoá', left: 16, top: 8, textStyle: TYPOGRAPHY.title, subtextStyle: TYPOGRAPHY.subtitle },
  tooltip: { formatter: (p) => `${p.name}: ${fmtCompact(p.value, { baseUnit: 'ty', decimals: 0 })} nghìn tỷ`, textStyle: { fontSize: 12 } },
  series: [
    {
      type: 'treemap', top: 60, left: 8, right: 8, bottom: 8,
      roam: false, nodeClick: false, breadcrumb: { show: false },
      label: { show: true, formatter: '{b}', ...TYPOGRAPHY.dataLabel, color: PALETTE.paper },
      upperLabel: { show: true, height: 24, color: PALETTE.paper, fontFamily: FONT_STACK, fontWeight: 'bold' },
      itemStyle: { borderColor: PALETTE.paper, borderWidth: 2, gapWidth: 2 }, // surface gap giữa các ô, không dùng viền màu
      levels: [
        { itemStyle: { borderWidth: 0, gapWidth: 3 } },
        { itemStyle: { gapWidth: 2 }, colorSaturation: [0.35, 0.55] },
      ],
      data,
    },
  ],
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-10-treemap.svg', import.meta.url), svg);
console.log('10-treemap: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
chart.dispose();
process.exit(0);
