// 06-tornado.mjs, Tornado: phân tích độ nhạy định giá (DCF/LBO sensitivity)
// Dùng khi: cho thấy biến nào tác động mạnh nhất lên 1 kết quả (giá trị DN,
// EPS...) khi thay đổi trong 1 khoảng giả định, sắp theo |biên độ| giảm dần
// để biến quan trọng nhất nằm trên cùng (đúng hình dạng "cái phễu lốc").
// Dữ liệu cần: {variable, low, high, base}, low/high là kết quả khi biến đó
// ở kịch bản bi quan/lạc quan, base là giá trị trung tâm để tính lệch.
// Bẫy thường gặp: (1) KHÔNG sắp theo biên độ -> mất hình phễu, khó đọc;
// (2) dùng 2 màu tuỳ ý cho low/high thay vì nhất quán xuyên suốt mọi biến;
// (3) qua dùng nhãn % mà không neo rõ base case.
// LƯU Ý MÀU: đây là NHẬN ĐỊNH SO SÁNH (dải kịch bản quanh 1 base case tĩnh,
// không phải delta thời gian), không phải cầu nối P&L. Bi quan = negative
// (bất lợi trong so sánh, được phép); lạc quan PHẢI trung tính, KHÔNG tô
// accent, vì "kịch bản tốt hơn = xanh dương" chính là tô màu dương cho bên có
// lợi, dạng traffic-light bị cấm dù đội lốt "chỉ là tô theo chiều tăng/giảm".
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';
import { validateSeries, epDonVi } from './schema.mjs';

export const MAC_DINH = {
  base: 850, // tỷ đồng, giá trị doanh nghiệp base case
  raw: [
    { variable: 'WACC (±1.5đpt)', low: 720, high: 1010 },
    { variable: 'Tăng trưởng dài hạn (±0.5đpt)', low: 790, high: 925 },
    { variable: 'Biên EBITDA (±2đpt)', low: 810, high: 895 },
    { variable: 'Vốn đầu tư/DThu (±1đpt)', low: 830, high: 875 },
    { variable: 'Thuế suất hiệu dụng (±2đpt)', low: 838, high: 862 },
  ],
  // Khoi meta BAT BUOC cua moi preset: don vi va nguon. Xem charts/echarts/schema.mjs.
  series: {
    unit: 'ty_dong',
    source: { tier: 'uoc-tinh', label: 'Số minh hoạ, không phải số công bố' },
    as_of: '2026-08-09',
  },
};

export function option(params) {
  const { base, raw , series} = params;
  // Moi preset deu di qua lop schema. `epDonVi` la loi khai THAT THA cua preset
  // nay: ham dinh dang cua no gan chat voi don vi ty_dong, nen truyen don vi
  // khac se cho mot nhan sai su that. Bao loi luc build con hon ve ra nhan sai.
  validateSeries(series);
  epDonVi(series, ['ty_dong']);
  const rows = [...raw].sort((a, b) => (b.high - b.low) - (a.high - a.low)); // sắp theo biên độ giảm dần
  const categories = rows.map((r) => r.variable);

  return {
    ...baseOption({ title: 'Phân tích độ nhạy giá trị doanh nghiệp (DCF)', subtitle: `Base case = ${fmtCompact(base, { baseUnit: 'ty', decimals: 0 })}, sắp theo biên độ tác động` }),
    tooltip: tooltipDefault,
    // `left: 232` chu khong phai 200. Nhan truc y dai nhat la `WACC (±1.5đpt)`, va nhan gia
    // tri cua thanh dai nhat nam ben TRAI thanh do, nen hai chuoi gap nhau: anh chup ra
    // `WACC (±1.5đp720 tỷ`. Gate nhan chong bat duoc voi ty le giao 42%. Them 32px la du
    // cho ca hai, do bang cach do lai chu khong uoc luong.
    grid: { left: 232, right: 40, top: 60, bottom: 40 },
    xAxis: {
      type: 'value',
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtCompact(v + base, { baseUnit: 'ty', decimals: 0 }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    yAxis: { type: 'category', data: categories, inverse: true, // phễu lốc: biên độ lớn nhất phải ở TRÊN CÙNG; ECharts mac dinh dat index 0 o DAY nen phai dao truc, khong dao thi hinh ra nguoc voi y dinh ghi o dau file
           axisLine: { show: false }, axisTick: { show: false },
      // `margin: 34` chu khong phai mac dinh 8. Nhan gia tri cua thanh dai nhat nam ben
      // TRAI thanh do, sat mep grid, nen no gap nhan truc: anh chup ra `WACC (±1.5đp720 tỷ`.
      // Noi rong grid khong cuu duoc vi nhan truc dich theo grid; phai day rieng nhan truc
      // ra xa mep. Gate nhan chong bat duoc voi ty le giao 42%.
      axisLabel: { ...TYPOGRAPHY.axisLabel, margin: 34 } },
    // VACH BASE-CASE, nay ve THAT (09-08).
    //
    // Lich su cua no dang ghi lai vi no la mot ca mau: ban truoc ve vach nay bang
    // `const opt = chart.getOption(); opt.series[0].markLine = {...}; chart.setOption(opt)`.
    // Do bang thuc nghiem thi cach do KHONG lam markLine hien ra trong SVG: dem phan tu
    // hai ban co va khong co markLine ra dung 50 nhu nhau, va chuoi "Base" chi xuat hien
    // mot lan trong phu de. Tuc mot tinh nang nhin nhu co trong ma nhung CHUA BAO GIO ve
    // ra, va no song duoc ca hai phase vi khong phep do nao hoi "vach do co that khong".
    //
    // Cach dung la khai `markLine` THANG trong option, khong di duong getOption roi
    // setOption lai. Vach dat tai x=0 vi truc x cua tornado la do LECH so voi base, nen
    // goc toa do chinh la kich ban co so. Khong gan nhan cho vach: phu de da ghi base
    // case bang so, them mot nhan nua chi lam dong chu canh truc.
    series: [
      {
        name: 'Kịch bản bi quan', type: 'bar', stack: 'range', barWidth: 22,
        itemStyle: { color: PALETTE.negative },
        data: rows.map((r) => r.low - base),
        label: { show: true, position: 'left', formatter: (p) => fmtCompact(p.value + base, { baseUnit: 'ty', decimals: 0 }), ...TYPOGRAPHY.dataLabel },
        markLine: {
          silent: true,
          symbol: 'none',
          data: [{ xAxis: 0 }],
          lineStyle: { color: PALETTE.ink, width: 1.5, type: 'solid' },
          label: { show: false },
        },
      },
      {
        name: 'Kịch bản lạc quan', type: 'bar', stack: 'range', barWidth: 22,
        itemStyle: { color: PALETTE.inkLo },
        data: rows.map((r) => r.high - base),
        label: { show: true, position: 'right', formatter: (p) => fmtCompact(p.value + base, { baseUnit: 'ty', decimals: 0 }), ...TYPOGRAPHY.dataLabel },
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
  const svg = renderStatic(option, MAC_DINH, { width: 720, height: 380 });
  writeFileSync(new URL('./out-06-tornado.svg', import.meta.url), svg);
  console.log('06-tornado: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
