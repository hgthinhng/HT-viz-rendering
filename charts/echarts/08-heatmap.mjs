// 08-heatmap.mjs, Heatmap ma trận: lợi nhuận theo tháng x năm (VN-Index)
// Dùng khi: cần quét nhanh pattern theo 2 chiều rời rạc (tháng x năm, ngành x
// tiêu chí) mà bảng số thô khó thấy pattern. ĐÂY LÀ DỮ LIỆU CÓ CỰC (lãi/lỗ)
// nên dùng thang màu DIVERGING (xanh dương=tăng, đỏ=giảm, xám=quanh 0),
// KHÔNG dùng thang sequential 1-hue vì sẽ không phân biệt được tăng/giảm,
// và CÀNG KHÔNG dùng rainbow (green-yellow-red), đó chính là traffic-light hoá.
// Dữ liệu cần: ma trận [năm][tháng] = giá trị số (ở đây: % thay đổi).
// Bẫy thường gặp: (1) thang màu không đối xứng quanh 0 -> đọc sai cường độ;
// (2) ô >2 chữ số không có label -> phải lướt mắt đoán màu, luôn nên có
// tooltip/label cho từng ô; (3) sort trục năm/tháng không theo thời gian.
import { TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { dinhDangTheoDonVi } from './fmt.mjs';

export const MAC_DINH = {
  months: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
  years: ['2023', '2024', '2025', '2026'],
  // % thay đổi VN-Index theo tháng (dữ liệu minh hoạ)
  matrix: [
    [1.2, -2.1, 3.4, 0.5, -1.8, 2.2, 1.1, -0.4, 2.8, -3.2, 1.6, 4.1],
    [-0.8, 2.5, -1.1, 1.9, 3.0, -2.6, 0.7, 1.4, -0.9, 2.1, -1.3, 0.9],
    [3.1, 1.0, -0.5, -4.2, 2.0, 1.5, -1.6, 0.3, 1.8, -0.7, 2.4, -1.0],
    [0.4, -1.5, 2.9, 1.1, -0.3, 3.6, -2.0, 1.7, 0.6, -1.1, 1.3, 0.0],
  ],
};

export function option(params) {
  // `donVi`: xem ghi chu cung ten o 04-dumbbell.mjs. Mac dinh `phan_tram`.
  const { months, years, matrix, donVi = 'phan_tram' } = params;
  const dinhDangSo = dinhDangTheoDonVi(donVi);
  const data = [];
  years.forEach((y, yi) => months.forEach((m, mi) => data.push([mi, yi, matrix[yi][mi]])));
  const maxAbs = Math.ceil(Math.max(...data.map((d) => Math.abs(d[2]))) * 10) / 10;

  return {
    // File nay tu dung option chu khong qua baseOption(), va KHONG tu khai animation
    // o day -- viec do thuoc renderStatic()/mountLive().
    backgroundColor: PALETTE.paper,
    textStyle: { fontFamily: FONT_STACK },
    title: {
      text: 'Biến động VN-Index theo tháng, 2023-2026',
      subtext: '% thay đổi so với tháng trước, thang màu đối xứng quanh 0 (diverging)',
      left: 16, top: 8, textStyle: TYPOGRAPHY.title, subtextStyle: TYPOGRAPHY.subtitle,
    },
    tooltip: {
      position: 'top',
      formatter: (p) => `${months[p.data[0]]}/${years[p.data[1]]}: ${dinhDangSo(p.data[2], { decimals: 1, showPlus: true })}`,
      textStyle: { fontSize: 12 },
    },
    grid: { left: 60, right: 24, top: 70, bottom: 30 },
    xAxis: { type: 'category', data: months, splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    yAxis: { type: 'category', data: years, splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    visualMap: {
      min: -maxAbs, max: maxAbs, calculable: true, orient: 'horizontal', left: 'right', top: 8,
      inRange: { color: [PALETTE.negative, PALETTE.line, PALETTE.accent] }, // diverging: đỏ<->xám<->xanh, KHÔNG rainbow
      textStyle: TYPOGRAPHY.axisLabel,
      itemWidth: 10, itemHeight: 80,
    },
    series: [
      {
        type: 'heatmap', data,
        label: { show: true, formatter: (p) => dinhDangSo(p.data[2], { decimals: 1 }), fontSize: 9, fontFamily: FONT_STACK },
        itemStyle: { borderColor: PALETTE.paper, borderWidth: 2 }, // surface gap giữa các ô
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  // `render-static.mjs` keo ca goi ECharts vao, nen import TINH o dinh file lam
  // bundle lan `html-song` mat sach tree-shaking va keo ban day du 1,1MB. Import
  // DONG ngay trong nhanh CLI: duong tinh van chay y het, con trinh duyet khong
  // bao gio cham toi module nay.
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: 760, height: 300 });
  writeFileSync(new URL('./out-08-heatmap.svg', import.meta.url), svg);
  console.log('08-heatmap: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
