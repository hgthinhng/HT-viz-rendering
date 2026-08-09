// 21-upset.mjs, UpSet: các tập hợp CHỒNG LẤN nhau ra sao khi có quá 3 tập
// Dùng khi: cần thấy bao nhiêu phần tử thuộc về đúng tổ hợp tập hợp nào, vd bao nhiêu
// mã cổ phiếu vừa qua bộ lọc giá trị vừa qua bộ lọc đà tăng nhưng trượt bộ lọc chất
// lượng, hay bao nhiêu khách hàng dùng đúng hai trong bốn sản phẩm.
// KHÔNG dùng khi: chỉ có 2-3 tập (biểu đồ Venn đọc nhanh hơn và ai cũng hiểu ngay);
// quan tâm TỔNG mỗi tập chứ không quan tâm phần giao (dùng 14-bar-ranking); số tổ hợp
// có thật vượt 15 (cột thành rừng, cắt bớt theo ngưỡng trước khi vẽ).
//
// Vì sao không dùng Venn cho từ 4 tập trở lên: Venn bốn vòng tròn KHÔNG vẽ được đủ 15
// vùng giao, nên mọi bản Venn bốn tập đều phải bóp méo hình và bỏ sót vùng. UpSet đổi
// bài toán từ hình học sang bảng: mỗi tổ hợp là một cột, ma trận chấm bên dưới nói cột
// đó gồm những tập nào.
//
// Dữ liệu cần: {tapNames:string[], toHop:[{tap:number[], soLuong:number}]}. Bẫy:
// (1) sắp tổ hợp theo thứ tự bảng chữ cái thì mắt không đọc ra gì, phải sắp theo SỐ
// LƯỢNG giảm dần; (2) quên vẽ chấm mờ cho tập KHÔNG thuộc tổ hợp thì mắt mất lưới neo;
// (3) để cột tổng của từng tập cùng thang với cột tổ hợp làm cột tổ hợp bị nén phẳng.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK_MONO } from './theme.mjs';
import { fmtNumber } from './fmt.mjs';

export const MAC_DINH = {
  tapNames: ['Định giá rẻ', 'Đà tăng', 'Chất lượng', 'Thanh khoản'],
  // Số mã minh hoạ qua từng tổ hợp bộ lọc, KHÔNG phải số thật.
  toHop: [
    { tap: [3], soLuong: 84 },
    { tap: [0, 3], soLuong: 61 },
    { tap: [1, 3], soLuong: 47 },
    { tap: [0, 2, 3], soLuong: 29 },
    { tap: [2, 3], soLuong: 24 },
    { tap: [0, 1, 3], soLuong: 18 },
    { tap: [0, 1, 2, 3], soLuong: 6 },
  ],
  title: 'Bao nhiêu mã qua được tổ hợp bộ lọc nào',
  subtitle: 'Đơn vị: số mã. Mỗi cột là một tổ hợp loại trừ lẫn nhau. Số minh hoạ.',
};

const W = 720;
const H = 440;
/** Chieu cao danh cho ma tran cham, tinh tu day khung len. */
const CAO_MA_TRAN = 132;

export function option(params) {
  const { tapNames, toHop, title, subtitle } = params;
  if (toHop.length > 15) {
    throw new Error('21-upset: qua 15 to hop, cot thanh rung; cat bot theo nguong truoc khi ve');
  }
  // Sap theo SO LUONG giam dan. Sap theo ten to hop thi mat khong doc ra gi, va cau hoi
  // dau tien cua nguoi doc luon la "to hop nao dong nhat".
  const cot = [...toHop].sort((a, b) => b.soLuong - a.soLuong);
  const nhanCot = cot.map((_, i) => String(i + 1));

  return {
    ...baseOption({ title, subtitle, width: W, height: H }),
    legend: { show: false },
    tooltip: {
      trigger: 'item',
      formatter: (p) => {
        const c = cot[p.dataIndex];
        if (!c) return '';
        const ten = c.tap.map((i) => tapNames[i]).join(' + ');
        return `${ten}<br/>${fmtNumber(c.soLuong, { decimals: 0 })} mã`;
      },
      textStyle: TYPOGRAPHY.axisLabel,
    },
    grid: { left: 140, right: 30, top: 70, bottom: CAO_MA_TRAN + 28 },
    xAxis: {
      type: 'category',
      data: nhanCot,
      axisLine: { show: false },
      axisTick: { show: false },
      // An nhan truc x: so thu tu cot khong mang thong tin gi, ma tran cham ben duoi moi
      // la thu noi cot do la to hop nao. Giu nhan la them mot hang chu vo nghia.
      axisLabel: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtNumber(v, { decimals: 0 }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    series: [
      {
        name: 'Số mã', type: 'bar', barWidth: '52%',
        data: cot.map((c) => c.soLuong),
        itemStyle: { color: PALETTE.accent },
        label: {
          show: true, position: 'top',
          formatter: (p) => fmtNumber(p.value, { decimals: 0 }),
          ...TYPOGRAPHY.dataLabel,
        },
      },
      {
        // Ma tran cham: moi hang la mot tap, moi cot la mot to hop. Ve bang custom vi no
        // nam NGOAI he truc (duoi day khung), khong the la mot series binh thuong.
        name: 'Ma trận', type: 'custom', z: 2, silent: true,
        renderItem: (itemParams, api) => {
          const ci = itemParams.dataIndex;
          const x = api.coord([ci, 0])[0];
          const yDay = api.coord([ci, 0])[1];
          const buocHang = CAO_MA_TRAN / (tapNames.length + 0.5);
          const con = [];
          const thuoc = new Set(cot[ci].tap);

          // Duong noi cac cham THUOC to hop: thieu no thi mot cot bon cham roi rac doc
          // cham hon han mot cot co duong noc.
          const cacY = [...thuoc].map((ti) => yDay + 18 + ti * buocHang);
          if (cacY.length > 1) {
            con.push({
              type: 'line',
              shape: { x1: x, y1: Math.min(...cacY), x2: x, y2: Math.max(...cacY) },
              style: { stroke: PALETTE.ink, lineWidth: 2 },
            });
          }
          tapNames.forEach((_, ti) => {
            const co = thuoc.has(ti);
            con.push({
              type: 'circle',
              shape: { cx: x, cy: yDay + 18 + ti * buocHang, r: co ? 5 : 4 },
              // Cham MO cho tap khong thuoc to hop, khong bo trong: bo trong thi mat mat
              // luoi neo va khong dem duoc hang nao la hang nao.
              style: { fill: co ? PALETTE.ink : PALETTE.line },
            });
          });
          return { type: 'group', children: con };
        },
        data: cot.map((_, i) => [i, 0]),
      },
      {
        // Ten tap, ve mot lan o cot dau tien. Dat trong custom chu khong dung yAxis thu
        // hai vi ma tran nam ngoai he truc.
        name: 'Tên tập', type: 'custom', z: 3, silent: true,
        renderItem: (itemParams, api) => {
          if (itemParams.dataIndex !== 0) return null;
          const yDay = api.coord([0, 0])[1];
          const buocHang = CAO_MA_TRAN / (tapNames.length + 0.5);
          return {
            type: 'group',
            children: tapNames.map((ten, ti) => ({
              type: 'text',
              x: 130,
              y: yDay + 12 + ti * buocHang,
              style: {
                text: ten,
                font: `11px ${FONT_STACK_MONO}`,
                fill: PALETTE.inkMd,
                textAlign: 'right',
              },
            })),
          };
        },
        data: cot.map((_, i) => [i, 0]),
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. Chi tiet: 01-waterfall.mjs.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-21-upset.svg', import.meta.url), svg);
  console.log('21-upset: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
