// 09-candlestick.mjs, Candlestick + volume: biến động giá cổ phiếu theo phiên
// Dùng khi: trình bày giá OHLC (mở/cao/thấp/đóng) theo thời gian, thường kèm
// khối lượng giao dịch ở panel dưới cùng trục x để đối chiếu breakout với
// thanh khoản. Dữ liệu cần: mảng {date, open, close, low, high, volume}.
// Bẫy thường gặp: (1) không đồng bộ trục x giữa panel giá và panel volume khi
// zoom -> lệch ngày; (2) dùng xanh lá/đỏ theo quy ước CHỨNG KHOÁN MỸ (tăng=
// xanh lá, giảm=đỏ) trong khi sàn HOSE/HNX niêm yết dùng xanh LAM=tăng, ĐỎ=
// giảm, VÀNG=đứng giá, nhầm quy ước màu là lỗi nghiêm trọng với người đọc VN;
// (3) trục giá không nên ép bắt đầu từ 0 (khác bar chart) vì sẽ nén biến động
// nến vào 1 dải hẹp không đọc được, đây là NGOẠI LỆ có chủ đích của quy tắc
// "trục phải bắt đầu từ 0", vì OHLC là toạ độ tuyệt đối không phải magnitude.
import { TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { validateSeries, epDonVi } from './schema.mjs';

// quy ước sàn HOSE: tăng = xanh lam (dùng accent), giảm = đỏ (dùng negative), đứng giá = vàng tham chiếu (không dùng ở đây vì không có phiên đứng giá trong mẫu)
export const MAC_DINH = {
  dates: ['02/12', '03/12', '04/12', '05/12', '08/12', '09/12', '10/12', '11/12', '12/12', '15/12'],
  ohlc: [
    [28.5, 29.2, 28.3, 29.4], [29.2, 28.8, 28.5, 29.5], [28.8, 30.1, 28.7, 30.3],
    [30.1, 29.6, 29.4, 30.2], [29.6, 29.9, 29.3, 30.0], [29.9, 31.2, 29.8, 31.5],
    [31.2, 30.8, 30.5, 31.4], [30.8, 30.2, 29.9, 31.0], [30.2, 30.6, 30.0, 30.9],
    [30.6, 32.1, 30.5, 32.3],
  ],
  volume: [1.2, 0.9, 2.1, 1.5, 1.0, 3.2, 1.8, 1.1, 0.8, 2.6], // triệu cp
  // Khoi meta BAT BUOC cua moi preset: don vi va nguon. Xem charts/echarts/schema.mjs.
  series: {
    unit: 'nghin_dong_cp',
    source: { tier: 'uoc-tinh', label: 'Số minh hoạ, không phải số công bố' },
    as_of: '2026-08-09',
  },
};

export function option(params) {
  const { dates, ohlc, volume , series} = params;
  // Moi preset deu di qua lop schema. `epDonVi` la loi khai THAT THA cua preset
  // nay: ham dinh dang cua no gan chat voi don vi nghin_dong_cp, nen truyen don vi
  // khac se cho mot nhan sai su that. Bao loi luc build con hon ve ra nhan sai.
  validateSeries(series);
  epDonVi(series, ['nghin_dong_cp']);
  return {
    // File nay tu dung option chu khong qua baseOption(), va KHONG tu khai animation
    // o day -- viec do thuoc renderStatic()/mountLive().
    backgroundColor: PALETTE.paper,
    textStyle: { fontFamily: FONT_STACK },
    title: { text: 'Giá và khối lượng giao dịch, mã minh hoạ VNM', subtext: 'Đơn vị: nghìn đồng/cp; khối lượng: triệu cp; quy ước màu sàn HOSE (tăng=lam, giảm=đỏ)', left: 16, top: 8, textStyle: TYPOGRAPHY.title, subtextStyle: TYPOGRAPHY.subtitle },
    axisPointer: { link: [{ xAxisIndex: 'all' }] },
    grid: [
      { left: 60, right: 24, top: 64, height: 220 },
      { left: 60, right: 24, top: 310, height: 70 },
    ],
    xAxis: [
      { type: 'category', data: dates, gridIndex: 0, axisLabel: { show: false }, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, splitLine: { show: false } },
      { type: 'category', data: dates, gridIndex: 1, axisLabel: TYPOGRAPHY.axisLabel, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, splitLine: { show: false } },
    ],
    yAxis: [
      { type: 'value', gridIndex: 0, scale: true, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => v.toFixed(1) }, splitLine: { lineStyle: { color: PALETTE.line } } }, // scale:true = KHÔNG ép về 0 (ngoại lệ có chủ đích cho OHLC)
      { type: 'value', gridIndex: 1, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => v + 'tr' }, splitLine: { show: false }, min: 0 },
    ],
    series: [
      {
        type: 'candlestick', data: ohlc, xAxisIndex: 0, yAxisIndex: 0,
        itemStyle: { color: PALETTE.accent, color0: PALETTE.negative, borderColor: PALETTE.accent, borderColor0: PALETTE.negative },
      },
      {
        type: 'bar', data: volume.map((v, i) => ({ value: v, itemStyle: { color: ohlc[i][1] >= ohlc[i][0] ? PALETTE.accent : PALETTE.negative, opacity: 0.5 } })),
        xAxisIndex: 1, yAxisIndex: 1,
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
  const svg = renderStatic(option, MAC_DINH, { width: 720, height: 420 });
  writeFileSync(new URL('./out-09-candlestick.svg', import.meta.url), svg);
  console.log('09-candlestick: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
