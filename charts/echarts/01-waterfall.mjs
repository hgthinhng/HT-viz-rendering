// 01-waterfall.mjs, Waterfall: cầu nối P&L (Doanh thu -> Lợi nhuận ròng)
// Dùng khi: giải thích một tổng số bị phân rã bởi các khoản cộng/trừ tuần tự
// (doanh thu -> COGS -> CP vận hành -> thuế -> LNST; hoặc biến động vốn CSH).
// Dữ liệu cần: 1 cột nhãn hạng mục + 1 cột giá trị (dương=cộng, âm=trừ),
// hạng mục đầu/cuối là "mốc tuyệt đối" (subtotal), giữa là "delta".
// Bẫy thường gặp: (1) quên đánh dấu subtotal khác màu với delta -> người đọc
// tưởng lợi nhuận ròng cũng là một khoản "cộng thêm"; (2) trục y không bắt đầu
// từ 0 làm méo tỷ lệ các thanh; (3) không note đơn vị -> nhầm tỷ với triệu.
import { baseOption, valueAxis, categoryAxis, tooltipDefault, PALETTE, TYPOGRAPHY } from './theme.mjs';
import { fmtCompact, fmtDelta } from './fmt.mjs';
import { renderStatic } from './render-static.mjs';

// MAC_DINH: bo du lieu demo (truoc ban tach option/render day la hang so top-level).
export const MAC_DINH = {
  categories: ['Doanh thu thuần', 'Giá vốn hàng bán', 'Chi phí vận hành', 'Chi phí thuế', 'Lợi nhuận ròng'],
  values: [120, -45, -20, -8, 47], // đơn vị: tỷ đồng
  title: 'Cầu nối P&L: Từ doanh thu đến lợi nhuận ròng',
  subtitle: 'Đơn vị: tỷ đồng, Q4/2026',
};

/** Tra ve OBJECT OPTION thuan (khong echarts.init, khong ghi file, khong tu khai
 * animation -- viec do thuoc renderStatic()/mountLive()). */
export function option(params) {
  const { categories, values, title, subtitle } = params;
  const isEdge = (i) => i === 0 || i === values.length - 1;

  let cum = 0;
  const base = [], pos = [], neg = [];
  values.forEach((v, i) => {
    if (isEdge(i)) {
      base.push(0);
      pos.push('-'); neg.push('-');
      cum = v;
    } else if (v >= 0) {
      base.push(cum); pos.push(v); neg.push('-');
      cum += v;
    } else {
      cum += v;
      base.push(cum); pos.push('-'); neg.push(-v);
    }
  });
  // subtotal (đầu/cuối) vẽ riêng để tô neutralDark thay vì accent/negative
  const subtotal = values.map((v, i) => (isEdge(i) ? v : '-'));

  return {
    ...baseOption({ title, subtitle }),
    tooltip: tooltipDefault,
    xAxis: categoryAxis(categories),
    yAxis: valueAxis({ axisLabelFormatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals: 0 }) }),
    series: [
      { name: 'nền (ẩn)', type: 'bar', stack: 'total', itemStyle: { color: 'transparent' }, data: base, silent: true, tooltip: { show: false } },
      {
        name: 'Mốc tuyệt đối', type: 'bar', stack: 'total', barWidth: 40,
        itemStyle: { color: PALETTE.ink, borderRadius: [3, 3, 0, 0] },
        data: subtotal,
        label: { show: true, position: 'top', formatter: (p) => fmtCompact(p.value, { baseUnit: 'ty', decimals: 0 }), ...TYPOGRAPHY.dataLabel },
      },
      {
        name: 'Tăng', type: 'bar', stack: 'total', barWidth: 40,
        itemStyle: { color: PALETTE.accent, borderRadius: [3, 3, 0, 0] },
        data: pos,
        label: { show: true, position: 'top', formatter: (p) => fmtDelta(p.value, { decimals: 0 }), ...TYPOGRAPHY.dataLabel },
      },
      {
        name: 'Giảm', type: 'bar', stack: 'total', barWidth: 40,
        itemStyle: { color: PALETTE.negative, borderRadius: [3, 3, 0, 0] },
        data: neg,
        label: { show: true, position: 'top', formatter: (p) => fmtDelta(-p.value, { decimals: 0 }), ...TYPOGRAPHY.dataLabel },
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs): `process` khong ton tai trong DOM, va toan
// bo dieu kien phai KHONG DUNG TOI process.argv khi nhanh do khong chay. `node:fs` cung
// chuyen sang import DONG (chi load luc nhanh nay THAT SU chay), vi import TINH o dinh
// file se bi trinh duyet co gang resolve 'node:fs' ngay ca khi nhanh CLI khong bao gio
// chay toi, lam ca module load loi.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: 700, height: 400 });
  writeFileSync(new URL('./out-01-waterfall.svg', import.meta.url), svg);
  console.log('01-waterfall: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
