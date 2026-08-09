// 03-bullet.mjs, Bullet chart: thực tế vs kế hoạch/mục tiêu, có dải định tính
// Dùng khi: so KPI thực tế với 1 mục tiêu (target) trên nền dải định tính
// (kém/đạt/tốt), gọn hơn gauge khi cần xếp nhiều KPI thành 1 cột.
// Dữ liệu cần: mỗi hàng {label, actual, target, bands:[low,mid,high]}.
// Bẫy thường gặp: (1) tô dải định tính bằng đỏ/vàng/xanh (traffic-light) ->
// CẤM theo brief, ở đây dùng 3 sắc độ XÁM của cùng 1 ramp trung tính;
// (2) target vẽ bằng bar chồng lên nhau gây rối -> phải là 1 VẠCH (marker),
// không phải 1 thanh; (3) trục không bắt đầu từ 0 làm méo % hoàn thành.
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault } from './theme.mjs';
import { fmtCompact } from './fmt.mjs';

// 3 dải định tính là 3 sắc độ xám (KHÔNG traffic-light), actual = accent
export const MAC_DINH = {
  rows: [
    { label: 'Doanh thu thuần', actual: 118, target: 125, bands: [70, 105, 140] },
    { label: 'EBITDA', actual: 46, target: 40, bands: [20, 35, 55] },
    { label: 'Dòng tiền HĐKD', actual: 32, target: 38, bands: [15, 30, 48] },
    { label: 'Vòng quay hàng tồn kho', actual: 6.2, target: 6.0, bands: [3, 5, 8] },
  ],
  title: 'Bullet: Thực tế vs kế hoạch theo KPI',
  subtitle: 'Đơn vị: tỷ đồng (riêng vòng quay HTK: lần)',
};

export function option(params) {
  const { rows, title, subtitle } = params;
  const categories = rows.map((r) => r.label);
  const max = Math.max(...rows.map((r) => r.bands[2]));
  const bandColors = [PALETTE.bandLo, PALETTE.bandMid, PALETTE.bandHi]; // 3 sắc xám LẠNH cùng ramp (theme.mjs), KHÔNG traffic-light

  return {
    ...baseOption({ title, subtitle }),
    tooltip: tooltipDefault,
    grid: { left: 170, right: 40, top: 60, bottom: 30 },
    xAxis: { type: 'value', max, axisLabel: TYPOGRAPHY.axisLabel, splitLine: { lineStyle: { color: PALETTE.line } } },
    yAxis: { type: 'category', data: categories, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    series: [
      { name: 'Dải kém', type: 'bar', stack: 'band', barWidth: 18, silent: true, itemStyle: { color: bandColors[0] }, data: rows.map((r) => r.bands[0]) },
      { name: 'Dải đạt', type: 'bar', stack: 'band', barWidth: 18, silent: true, itemStyle: { color: bandColors[1] }, data: rows.map((r) => r.bands[1] - r.bands[0]) },
      { name: 'Dải tốt', type: 'bar', stack: 'band', barWidth: 18, silent: true, itemStyle: { color: bandColors[2] }, data: rows.map((r) => r.bands[2] - r.bands[1]) },
      {
        name: 'Thực tế', type: 'bar', barWidth: 7, barGap: '-50%',
        itemStyle: { color: PALETTE.accent },
        data: rows.map((r) => r.actual),
        z: 5,
        label: { show: true, position: 'right', formatter: (p) => fmtCompact(p.value, { baseUnit: 'ty', decimals: 1 }), ...TYPOGRAPHY.dataLabel },
      },
      {
        name: 'Mục tiêu', type: 'custom',
        renderItem: (params, api) => {
          const y = api.coord([0, params.dataIndex])[1];
          const x = api.coord([api.value(0), params.dataIndex])[0];
          return {
            type: 'line',
            shape: { x1: x, y1: y - 12, x2: x, y2: y + 12 },
            style: { stroke: PALETTE.ink, lineWidth: 3 },
          };
        },
        data: rows.map((r) => r.target),
        z: 6,
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
  const svg = renderStatic(option, MAC_DINH, { width: 700, height: 360 });
  writeFileSync(new URL('./out-03-bullet.svg', import.meta.url), svg);
  console.log('03-bullet: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
