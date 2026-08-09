// 05-slope.mjs, Slope chart: đổi thứ hạng/giá trị giữa 2 mốc cho nhiều thực thể
// Dùng khi: "thị phần các ngân hàng thay đổi thế nào từ 2025 sang 2026", // khác dumbbell ở chỗ slope nhấn TRỤC THỜI GIAN có hướng (trái->phải), dumbbell
// nhấn CHÊNH LỆCH không có ý niệm thời gian rõ. Slope hợp khi >4-5 thực thể vì
// độ dốc đường nói lên "ai tăng nhanh hơn ai" ngay cả khi không đổi hạng.
// Dữ liệu cần: {label, t1, t2} cho từng thực thể.
// Bẫy thường gặp: (1) >6-8 đường thì nhãn chồng nhau, phải chọn nhấn 1-2 thực
// thể (emphasis) và làm mờ phần còn lại; (2) 2 trục x không đều khoảng cách
// thời gian thực (slope chart giả định khoảng cách đều, ghi rõ nếu không đều).
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { dinhDangTheoDonVi } from './fmt.mjs';

export const MAC_DINH = {
  entities: [
    { label: 'VCB', t1: 18.2, t2: 17.5, highlight: false },
    { label: 'TCB', t1: 9.1, t2: 11.8, highlight: true }, // câu chuyện: TCB tăng nhanh nhất
    { label: 'MBB', t1: 8.4, t2: 9.0, highlight: false },
    { label: 'ACB', t1: 7.9, t2: 7.6, highlight: false },
    { label: 'VPB', t1: 7.2, t2: 8.1, highlight: false },
  ],
  title: 'Thị phần tín dụng: Q4/2025 so với Q4/2026',
  subtitle: 'Đơn vị: %, nhấn mạnh TCB (tăng nhanh nhất)',
};

export function option(params) {
  // `donVi`: xem ghi chu cung ten o 04-dumbbell.mjs. Mac dinh `phan_tram` de khong doi
  // dien mao ban demo.
  const { entities, title, subtitle, donVi = 'phan_tram' } = params;
  const dinhDangSo = dinhDangTheoDonVi(donVi);
  const series = entities.map((e) => ({
    name: e.label,
    type: 'line',
    data: [e.t1, e.t2],
    symbolSize: 8,
    lineStyle: { width: e.highlight ? 3 : 1.5, color: e.highlight ? PALETTE.accent : PALETTE.inkLo },
    itemStyle: { color: e.highlight ? PALETTE.accent : PALETTE.inkLo },
    label: {
      show: true,
      formatter: (p) => `${e.label} ${dinhDangSo(p.value, { decimals: 1 })}`,
      color: e.highlight ? PALETTE.ink : PALETTE.inkLo,
      fontWeight: e.highlight ? 'bold' : 'normal',
      position: (p) => (p.dataIndex === 0 ? 'left' : 'right'),
      ...TYPOGRAPHY.dataLabel,
    },
    z: e.highlight ? 5 : 1,
  }));

  return {
    ...baseOption({ title, subtitle }),
    tooltip: tooltipDefault,
    legend: { show: false },
    grid: { left: 90, right: 90, top: 60, bottom: 40 },
    xAxis: { type: 'category', data: ['Q4/2025', 'Q4/2026'], boundaryGap: false, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel, splitLine: { show: false } },
    yAxis: { type: 'value', show: false, min: 0 },
    series,
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
  const svg = renderStatic(option, MAC_DINH, { width: 700, height: 400 });
  writeFileSync(new URL('./out-05-slope.svg', import.meta.url), svg);
  console.log('05-slope: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
