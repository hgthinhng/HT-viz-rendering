// 11-stacked-100.mjs, Stacked bar 100%: cơ cấu tỷ trọng qua thời gian
// Dùng khi: quan tâm TỶ TRỌNG (luôn cộng =100%) hơn giá trị tuyệt đối, vd cơ
// cấu nguồn vốn (nợ vay/vốn CSH), cơ cấu doanh thu theo kênh bán.
// Dữ liệu cần: {period, [category]: %} với tổng mỗi period = 100.
// Bẫy thường gặp: (1) tổng không đúng 100 do làm tròn từng phần riêng lẻ ->
// phải kiểm tổng SAU KHI làm tròn, chỉnh phần lớn nhất để bù sai số làm tròn;
// (2) quá 4-5 khoảng -> khó theo dõi 1 dải cụ thể qua thời gian, nên gộp đuôi
// nhỏ vào "Khác"; (3) thứ tự xếp chồng đổi giữa các cột -> phải CỐ ĐỊNH thứ
// tự category xuyên suốt mọi cột.
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';
import { renderStatic } from './render-static.mjs';

export const MAC_DINH = {
  periods: ['2023', '2024', '2025', '2026'],
  // thứ tự category CỐ ĐỊNH xuyên suốt: Nợ vay ngắn hạn / Nợ vay dài hạn / Vốn chủ sở hữu
  rows: {
    'Nợ vay ngắn hạn': [22, 19, 24, 18],
    'Nợ vay dài hạn': [35, 38, 30, 32],
    'Vốn chủ sở hữu': [43, 43, 46, 50],
  },
  title: 'Cơ cấu nguồn vốn, 2023-2026',
  subtitle: 'Đơn vị: % tổng nguồn vốn, thứ tự xếp chồng cố định',
};

/** Tra ve OBJECT OPTION thuan. FAIL ngay (throw) neu 1 cot khong cong dung 100 sau
 * lam tron -- kiem TRONG option() de fail-fast luc goi voi du lieu that. */
export function option(params) {
  const { periods, rows, title, subtitle } = params;
  // kiểm tổng mỗi cột phải = 100 sau làm tròn
  periods.forEach((_, i) => {
    const total = Object.values(rows).reduce((s, arr) => s + arr[i], 0);
    if (total !== 100) throw new Error(`11-stacked-100: cot ${periods[i]} tong=${total} != 100`);
  });

  return {
    ...baseOption({ title, subtitle }),
    tooltip: { ...tooltipDefault, valueFormatter: (v) => fmtPercent(v, { decimals: 0 }) },
    grid: { left: 56, right: 24, top: 60, bottom: 60 },
    xAxis: { type: 'category', data: periods, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    yAxis: { type: 'value', max: 100, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => v + '%' }, splitLine: { lineStyle: { color: PALETTE.line } } },
    // Đây là NHẬN ĐỊNH SO SÁNH cơ cấu (không phải delta thời gian): nợ vay ngắn
    // hạn là bên BẤT LỢI trong so sánh (rủi ro tái cấp vốn/thanh khoản ngắn hạn)
    // nên được phép dùng negative; hai hạng mục còn lại PHẢI trung tính, TUYỆT
    // ĐỐI không tô accent/positive cho VCSH dù nó thường là bên "tốt hơn", vì đó
    // là tô màu dương cho bên có lợi, đúng thứ traffic-light bị cấm.
    color: [PALETTE.negative, PALETTE.inkLo, PALETTE.inkMd],
    series: Object.entries(rows).map(([name, data]) => ({
      name, type: 'bar', stack: 'total', barWidth: 44, data,
      label: { show: true, formatter: (p) => fmtPercent(p.value, { decimals: 0 }), ...TYPOGRAPHY.dataLabel, color: PALETTE.paper },
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
  writeFileSync(new URL('./out-11-stacked-100.svg', import.meta.url), svg);
  console.log('11-stacked-100: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
