// 04-dumbbell.mjs, Dumbbell: so 2 thời điểm cho nhiều hạng mục cùng lúc
// Dùng khi: "biên lợi nhuận gộp từng mảng kinh doanh thay đổi ra sao từ
// 2025 sang 2026", tốt hơn 2 cột cạnh nhau vì nhấn vào ĐỘ CHÊNH LỆCH,
// không phải giá trị tuyệt đối từng cột.
// Dữ liệu cần: danh sách {label, before, after}. Nên SẮP THEO độ chênh lệch
// (ranking rule của FT) để mắt đọc pattern nhanh hơn.
// Bẫy thường gặp: (1) không sắp xếp -> nhìn như nhiễu; (2) dùng 2 màu tuỳ ý
// cho before/after thay vì 1 hue 2 sắc độ (trước=nhạt, sau=đậm) -> đọc thành
// 2 series không liên quan thay vì "trước->sau" của CÙNG một thực thể;
// (3) không note chiều mũi tên/nhãn -> không biết bên nào là "sau".
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtPercent, dinhDangTheoDonVi } from './fmt.mjs';

export const MAC_DINH = {
  raw: [
    { label: 'Bán lẻ', before: 18.2, after: 22.5 },
    { label: 'Bất động sản KCN', before: 34.0, after: 31.2 },
    { label: 'Vật liệu xây dựng', before: 12.5, after: 14.1 },
    { label: 'Logistics', before: 15.8, after: 15.1 },
    { label: 'Năng lượng tái tạo', before: 26.4, after: 33.0 },
  ],
  title: 'Biên lợi nhuận gộp theo mảng: 2025 so với 2026',
  subtitle: 'Đơn vị: %, sắp theo mức thay đổi',
};

export function option(params) {
  // `donVi` la MA don vi trong charts/schema.vocab.json, mac dinh `phan_tram` de moi loi
  // goi cu giu nguyen dien mao. Truoc ban nay preset dong cung `fmtPercent`, nen dung no
  // cho mot dai luong khong phai phan tram se in ra nhan SAI SU THAT chu khong phai xau,
  // dung loi da bat duoc o `14-bar-ranking` (`5.640.000%` cho mot so dem bang TEU).
  const { raw, title, subtitle, donVi = 'phan_tram' } = params;
  const dinhDangSo = dinhDangTheoDonVi(donVi);
  // sắp theo |chênh lệch| giảm dần (ranking rule)
  const rows = [...raw].sort((a, b) => Math.abs(b.after - b.before) - Math.abs(a.after - a.before));
  const categories = rows.map((r) => r.label);

  return {
    ...baseOption({ title, subtitle }),
    tooltip: tooltipDefault,
    grid: { left: 150, right: 60, top: 60, bottom: 40 },
    xAxis: { type: 'value', name: donVi === 'phan_tram' ? '%' : '', axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => dinhDangSo(v, { decimals: 0 }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
    yAxis: { type: 'category', data: categories, inverse: true, // sắp theo độ chênh: chênh lớn nhất phải ở TRÊN CÙNG; ECharts mac dinh dat index 0 o DAY nen phai dao truc, khong dao thi hinh ra nguoc voi y dinh ghi o dau file
           axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    series: [
      {
        name: 'Đoạn nối', type: 'custom', z: 1,
        renderItem: (itemParams, api) => {
          const y = api.coord([0, itemParams.dataIndex])[1];
          const x1 = api.coord([api.value(1), itemParams.dataIndex])[0];
          const x2 = api.coord([api.value(2), itemParams.dataIndex])[0];
          return { type: 'line', shape: { x1, y1: y, x2, y2: y }, style: { stroke: PALETTE.line, lineWidth: 4 } };
        },
        data: rows.map((r) => [0, r.before, r.after]),
        encode: { x: [1, 2], y: 0 },
      },
      {
        name: '2025', type: 'scatter', symbolSize: 14, z: 3,
        itemStyle: { color: PALETTE.inkLo },
        data: rows.map((r) => r.before),
        label: { show: true, formatter: (p) => dinhDangSo(p.value, { decimals: 1 }), position: 'top', ...TYPOGRAPHY.dataLabel, color: PALETTE.inkMd },
      },
      {
        name: '2026', type: 'scatter', symbolSize: 14, z: 4,
        itemStyle: { color: PALETTE.accent },
        data: rows.map((r) => r.after),
        label: { show: true, formatter: (p) => dinhDangSo(p.value, { decimals: 1 }), position: 'top', ...TYPOGRAPHY.dataLabel },
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
  const svg = renderStatic(option, MAC_DINH, { width: 700, height: 380 });
  writeFileSync(new URL('./out-04-dumbbell.svg', import.meta.url), svg);
  console.log('04-dumbbell: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
