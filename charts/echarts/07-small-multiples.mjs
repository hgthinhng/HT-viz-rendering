// 07-small-multiples.mjs, Small multiples: cùng 1 chỉ số, nhiều thực thể, cùng thang đo
// Dùng khi: so "hình dạng" xu hướng của nhiều mảng/công ty mà 1 chart chồng
// nhiều đường sẽ rối (>4-5 series), mỗi ô 1 thực thể, TẤT CẢ chung 1 trục y
// (bắt buộc, nếu không sẽ đánh lừa mắt về độ lớn tương đối).
// Dữ liệu cần: {entity, series:[q1..q4]} cho N thực thể, cùng đơn vị.
// Bẫy thường gặp: (1) mỗi ô tự scale riêng -> ô nhỏ trông "biến động dữ dội"
// ngang bằng ô lớn dù giá trị tuyệt đối chênh nhau 10 lần, PHẢI SAI nếu không
// ghi rõ; (2) quá nhiều ô (>9-12) làm mỗi ô quá nhỏ để đọc; (3) thiếu 1 trục
// tham chiếu chung (vd đường 0 hoặc trung bình ngành) khiến so sánh khó.
import { TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';
import { renderStatic } from './render-static.mjs';

export const MAC_DINH = {
  quarters: ['Q1/2026', 'Q2/2026', 'Q3/2026', 'Q4/2026'],
  segments: [
    { name: 'Bán lẻ', data: [42, 45, 48, 55] },
    { name: 'Bất động sản KCN', data: [30, 28, 33, 31] },
    { name: 'Vật liệu XD', data: [15, 17, 16, 19] },
    { name: 'Logistics', data: [22, 21, 24, 23] },
    { name: 'Năng lượng tái tạo', data: [8, 11, 14, 18] },
    { name: 'Tài chính tiêu dùng', data: [12, 13, 12, 14] },
  ],
  cols: 3,
};

const CELL_W = 220, CELL_H = 150, PAD_TOP = 60, PAD_LEFT = 20, GAP = 10;

/** Kich thuoc canvas phu thuoc SO LUONG thuc the (segments.length), khong phai hang
 * so co dinh -- CLI tail va option() dung CHUNG ham nay de khong lech nhau. */
export function kichThuoc(params) {
  const { segments, cols = MAC_DINH.cols } = params;
  const rows = Math.ceil(segments.length / cols);
  return {
    width: cols * CELL_W + PAD_LEFT * 2,
    height: rows * CELL_H + PAD_TOP + 30,
  };
}

export function option(params) {
  const { quarters, segments, cols = MAC_DINH.cols } = params;
  const allValues = segments.flatMap((s) => s.data);
  const sharedMax = Math.ceil(Math.max(...allValues) / 10) * 10; // CHUNG 1 thang đo cho mọi ô, bắt buộc

  const grids = [], xAxes = [], yAxes = [], series = [];
  segments.forEach((seg, i) => {
    const col = i % cols, row = Math.floor(i / cols);
    const left = PAD_LEFT + col * (CELL_W + GAP);
    const top = PAD_TOP + row * (CELL_H + GAP);
    grids.push({ left, top, width: CELL_W - GAP, height: CELL_H - 30, gridIndex: i });
    xAxes.push({ gridIndex: i, type: 'category', data: quarters, axisLabel: { show: false }, axisLine: { lineStyle: { color: PALETTE.line } }, axisTick: { show: false } });
    yAxes.push({ gridIndex: i, type: 'value', min: 0, max: sharedMax, axisLabel: { show: false }, axisLine: { show: false }, splitLine: { show: false } });
    series.push({
      type: 'line', xAxisIndex: i, yAxisIndex: i, data: seg.data, symbol: 'circle', symbolSize: 5,
      lineStyle: { color: PALETTE.accent, width: 2 }, itemStyle: { color: PALETTE.accent }, areaStyle: { color: PALETTE.accent, opacity: 0.08 },
    });
  });

  return {
    // File nay tu dung option chu khong qua baseOption(), nen KHONG thua ke gi ca --
    // va cung KHONG tu khai animation o day, viec do thuoc renderStatic()/mountLive().
    backgroundColor: PALETTE.paper,
    textStyle: { fontFamily: FONT_STACK },
    title: {
      text: 'Doanh thu theo mảng kinh doanh, 2026 (small multiples)',
      subtext: `Đơn vị: tỷ đồng, CÙNG thang trục 0-${sharedMax} cho mọi ô`,
      left: 16, top: 8, textStyle: TYPOGRAPHY.title, subtextStyle: TYPOGRAPHY.subtitle,
    },
    grid: grids,
    xAxis: xAxes,
    yAxis: yAxes,
    series,
    graphic: segments.map((seg, i) => {
      const col = i % cols, row = Math.floor(i / cols);
      const left = PAD_LEFT + col * (CELL_W + GAP);
      const top = PAD_TOP + row * (CELL_H + GAP) - 4;
      return { type: 'text', left, top, style: { text: `${seg.name}  ·  ${fmtCompact(seg.data[seg.data.length - 1], { baseUnit: 'ty', decimals: 0 })} (Q4)`, font: `bold 11px ${FONT_STACK}`, fill: PALETTE.ink } };
    }),
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const { width, height } = kichThuoc(MAC_DINH);
  const svg = renderStatic(option, MAC_DINH, { width, height });
  writeFileSync(new URL('./out-07-small-multiples.svg', import.meta.url), svg);
  console.log('07-small-multiples: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
