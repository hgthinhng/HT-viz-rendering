// 10-treemap.mjs, Treemap: cơ cấu vốn hoá/doanh thu theo ngành-mã
// Dùng khi: thể hiện phần-trong-tổng của NHIỀU hạng mục (>8-10) mà stacked bar
// sẽ quá chật, diện tích ô = độ lớn, phân cụm = nhóm cha (ngành).
// Dữ liệu cần: cây 2 cấp {group, name, value}. Không hợp khi cần so sánh
// CHÍNH XÁC 2 giá trị gần nhau (mắt người ước lượng diện tích kém hơn chiều dài).
// Bẫy thường gặp: (1) tô màu ngẫu nhiên theo từng ô lá thay vì theo NHÓM CHA
// (categorical theo group, sắc độ theo con) -> mất cấu trúc phân cấp;
// (2) nhãn bị cắt chữ trong ô quá nhỏ -> phải ẩn nhãn khi ô < ngưỡng, không
// dùng overflow:hidden cắt chữ nham nhở; (3) quá nhiều nhóm cha (>5-6) làm
// bảng màu categorical vượt ngưỡng an toàn CVD.
import { TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';
import { renderStatic } from './render-static.mjs';

// nhóm cha = ngành (categorical, tối đa 4 để an toàn CVD all-pairs theo dataviz skill)
export const MAC_DINH = {
  data: [
    { name: 'Ngân hàng', children: [
      { name: 'VCB', value: 480 }, { name: 'BID', value: 310 }, { name: 'CTG', value: 260 }, { name: 'TCB', value: 190 },
    ]},
    { name: 'Bất động sản', children: [
      { name: 'VHM', value: 220 }, { name: 'VIC', value: 180 }, { name: 'NVL', value: 40 },
    ]},
    { name: 'Tiêu dùng', children: [
      { name: 'MSN', value: 95 }, { name: 'VNM', value: 130 }, { name: 'SAB', value: 70 },
    ]},
    { name: 'Năng lượng', children: [
      { name: 'GAS', value: 150 }, { name: 'POW', value: 55 },
    ]},
  ],
};

export function option(params) {
  const { data } = params;
  const groupColor = { 'Ngân hàng': PALETTE.accent, 'Bất động sản': PALETTE.ink, 'Tiêu dùng': PALETTE.inkLo, 'Năng lượng': PALETTE.accentHi };
  const data2 = data.map((g) => ({ ...g, itemStyle: { color: groupColor[g.name] } }));

  return {
    // File nay tu dung option chu khong qua baseOption(), va KHONG tu khai animation
    // o day -- viec do thuoc renderStatic()/mountLive().
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
        data: data2,
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: 720, height: 420 });
  writeFileSync(new URL('./out-10-treemap.svg', import.meta.url), svg);
  console.log('10-treemap: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
