// 12-area-stack.mjs, Area stack: cơ cấu GIÁ TRỊ TUYỆT ĐỐI theo thời gian
// Dùng khi: vừa muốn thấy TỔNG tăng/giảm ra sao, vừa muốn thấy từng phần đóng
// góp bao nhiêu, khác stacked-bar-100 ở chỗ area-stack giữ nguyên đơn vị
// tuyệt đối (không chuẩn hoá về %). Hợp cho ≤4 dải; quá nhiều dải thì dải giữa
// (không chạm baseline) rất khó đọc biến động riêng, đây chính là bẫy Tufte
// hay cảnh báo về area chart nhiều lớp.
// Dữ liệu cần: {period, [series]: giá trị tuyệt đối cùng đơn vị}.
// Bẫy thường gặp: (1) >4 dải -> dải giữa vô nghĩa, nên chuyển sang small
// multiples; (2) area fill đặc (opacity=1) che mất gridline/dải phía dưới ->
// theo spec mark, area fill chỉ ~10% opacity, ở đây stack cần rõ dải nên tăng
// có kiểm soát nhưng KHÔNG vượt quá độ để gridline vẫn xuyên qua được;
// (3) không label dải cuối cùng ở đầu phải -> khó biết dải nào là dải nào nếu
// không có sẵn legend.
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';
import { renderStatic } from './render-static.mjs';

export const MAC_DINH = {
  periods: ['Q1/2026', 'Q2/2026', 'Q3/2026', 'Q4/2026'],
  seriesData: {
    'Bán lẻ': [42, 45, 48, 55],
    'Bất động sản KCN': [30, 28, 33, 31],
    'Vật liệu XD': [15, 17, 16, 19],
  },
};

export function option(params) {
  const { periods, seriesData } = params;

  return {
    ...baseOption({ title: 'Doanh thu theo mảng, cộng dồn', subtitle: 'Đơn vị: tỷ đồng, tối đa 4 dải để dải giữa vẫn đọc được' }),
    tooltip: { ...tooltipDefault, valueFormatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals: 0 }) },
    // Le phai 90 CHUA DU: nhan chuoi dai nhat "Bat dong san KCN" tran ra ngoai
    // viewBox 680px mat 24px va bi cat. Cung benh voi 02-sankey, do bang gate
    // `chu_khong_tran_viewbox.test.mjs` ngay 08-08.
    grid: { left: 60, right: 118, top: 60, bottom: 60 },
    xAxis: { type: 'category', data: periods, boundaryGap: false, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    yAxis: { type: 'value', min: 0, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
    // Override mang color mac dinh cua baseOption() ([accent, negative, inkLo, ink]):
    // day la 3 manh doanh thu NGANG HANG, khong phai delta/so sanh bat loi, nen
    // KHONG duoc de "Bat dong san KCN" roi dung vao slot negative/do chi vi trung
    // vi tri index trong mang mac dinh. Dung rieng 1 bo hue trung tinh + accent.
    color: [PALETTE.accent, PALETTE.accentHi, PALETTE.inkLo],
    series: Object.entries(seriesData).map(([name, data]) => ({
      name, type: 'line', stack: 'total', areaStyle: { opacity: 0.55 }, lineStyle: { width: 2 },
      symbol: 'circle', symbolSize: 5, smooth: false, data,
      endLabel: { show: true, formatter: (p) => `${p.seriesName}`, ...TYPOGRAPHY.dataLabel },
    })),
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: 680, height: 380 });
  writeFileSync(new URL('./out-12-area-stack.svg', import.meta.url), svg);
  console.log('12-area-stack: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
