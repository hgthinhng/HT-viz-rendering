// 05-slope.mjs, Slope chart: đổi thứ hạng/giá trị giữa 2 mốc cho nhiều thực thể
// Dùng khi: "thị phần các ngân hàng thay đổi thế nào từ 2025 sang 2026", // khác dumbbell ở chỗ slope nhấn TRỤC THỜI GIAN có hướng (trái->phải), dumbbell
// nhấn CHÊNH LỆCH không có ý niệm thời gian rõ. Slope hợp khi >4-5 thực thể vì
// độ dốc đường nói lên "ai tăng nhanh hơn ai" ngay cả khi không đổi hạng.
// Dữ liệu cần: {label, t1, t2} cho từng thực thể.
// Bẫy thường gặp: (1) >6-8 đường thì nhãn chồng nhau, phải chọn nhấn 1-2 thực
// thể (emphasis) và làm mờ phần còn lại; (2) 2 trục x không đều khoảng cách
// thời gian thực (slope chart giả định khoảng cách đều, ghi rõ nếu không đều).
import { baseOption, TYPOGRAPHY, PALETTE, tooltipDefault, FONT_STACK_MONO } from './theme.mjs';
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
    // Nhan KHONG ve bang `label` cua series nua, ma ve bang `graphic` trong
    // `_veSauLayout` ben duoi. Ly do o cuoi file muc "Vi sao nhan ve bang graphic".
    label: { show: false },
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

    /** Ve nhan hai dau bang graphic, sau khi truc da layout, va TACH chung theo truc doc.
     *
     * Vi sao khong dung `label` cua series: slope chart theo dinh nghia la nhieu duong
     * ket thuc gan nhau, nen nhan hai dau chong len nhau la trang thai MAC DINH chu khong
     * phai truong hop hiem. Do duoc tren chinh ban demo nay: ba nhan ben phai giao nhau
     * 40% dien tich, anh chup ra mot khoi chu khong doc noi.
     *
     * Da can va LOAI hai duong san co cua ECharts:
     *   - `labelLayout: { hideOverlap: true }` chay that va lam hinh sach, nhung no AN
     *     nhan, tuc xoa ten mot ngan hang khoi mot bieu do so sanh thi phan. Giau du lieu
     *     de cho hinh dep la thu repo nay khong lam.
     *   - `labelLayout: { moveOverlap: 'shiftY' }` dung y dinh nhung do THAT thi khong
     *     dich du: sau khi bat, hai cap nhan van con giao 40%.
     *
     * Nen tu tach: lay toa do pixel that, sap theo y, day xuong cho du khoang cach toi
     * thieu, roi neu tran day thi day nguoc len. Nhan lech khoi dau mut vai pixel nhung
     * moi thuc the deu con ten va deu doc duoc.
     */
    _veSauLayout(chart) {
      const W = chart.getWidth();
      const CAO_DONG = 15; // khoang cach doc toi thieu giua hai nhan, do tu fontSize 11
      const graphics = [];

      for (const dauMut of [0, 1]) {
        const diem = entities.map((e, i) => {
          const gt = dauMut === 0 ? e.t1 : e.t2;
          const [, py] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [dauMut, gt]);
          return { i, e, gt, y: py };
        });
        diem.sort((a, b) => a.y - b.y);
        for (let k = 1; k < diem.length; k++) {
          if (diem[k].y - diem[k - 1].y < CAO_DONG) diem[k].y = diem[k - 1].y + CAO_DONG;
        }
        // Day nguoc len neu cum bi tran xuong duoi vung ve.
        const day = chart.getHeight() - 46;
        const tran = diem[diem.length - 1].y - day;
        if (tran > 0) for (const d of diem) d.y -= tran;

        for (const d of diem) {
          graphics.push({
            type: 'text',
            x: dauMut === 0 ? 82 : W - 82,
            y: d.y - 6,
            style: {
              text: `${d.e.label} ${dinhDangSo(d.gt, { decimals: 1 })}`,
              font: `${d.e.highlight ? 'bold ' : ''}11px ${FONT_STACK_MONO}`,
              fill: d.e.highlight ? PALETTE.ink : PALETTE.inkLo,
              textAlign: dauMut === 0 ? 'right' : 'left',
            },
            silent: true,
          });
        }
      }
      return graphics;
    },
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
