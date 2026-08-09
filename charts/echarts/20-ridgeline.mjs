// 20-ridgeline.mjs, Ridgeline: phân phối DỊCH CHUYỂN thế nào qua nhiều kỳ liên tiếp
// Dùng khi: cùng một chỉ tiêu đo lặp lại qua 4-12 kỳ và câu hỏi là hình dạng phân phối
// dịch đi đâu, vd phân phối lợi suất ngày của thị trường theo từng năm, hay phân phối
// biên lợi nhuận toàn ngành qua các quý.
// KHÔNG dùng khi: chỉ có 2-3 kỳ (dùng 19-raincloud, xếp chồng ít hàng thì không thành
// dãy núi mà chỉ là ba hình rời); mỗi kỳ dưới 20 quan sát (đường mật độ thành hình bịa);
// cần đọc GIÁ TRỊ chính xác từng kỳ (dùng bảng, ridgeline chỉ đọc được hình dạng).
//
// Khác 19-raincloud ở CÂU HỎI chứ không ở kỹ thuật vẽ: raincloud so vài nhóm KHÔNG có
// thứ tự, ridgeline so nhiều kỳ CÓ thứ tự và cố ý cho các hàng chồng lấn nhau để mắt
// bắt được chuyển động của đỉnh. Chồng lấn là tính năng, không phải lỗi bố cục.
//
// Dữ liệu cần: {kyNames:string[], kyValues:number[][]}. Bẫy: (1) chuẩn hoá mật độ theo
// từng kỳ sẽ giấu mất chuyện kỳ nào tập trung hơn kỳ nào, nên preset này chuẩn hoá theo
// ĐỈNH CHUNG của mọi kỳ; (2) chồng lấn quá 70% làm hàng dưới nuốt hàng trên; (3) vẽ
// đường mật độ mà không tô nền thì các hàng đan vào nhau không phân biệt được.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK_MONO } from './theme.mjs';
import { dinhDangTheoDonVi } from './fmt.mjs';

export const MAC_DINH = {
  kyNames: ['2021', '2022', '2023', '2024', '2025', '2026'],
  // Lợi suất ngày minh hoạ theo năm, KHÔNG phải số thật. Cố ý cho phân phối dịch phải
  // dần và hẹp lại, tức thị trường vừa khá lên vừa bớt biến động.
  kyValues: [
    [-3.1, -2.4, -1.8, -1.2, -0.6, 0.1, 0.4, 0.9, 1.5, 2.2, 2.9, -2.0, -0.9, 0.6, 1.1],
    [-2.6, -2.0, -1.4, -0.8, -0.2, 0.3, 0.7, 1.2, 1.8, 2.5, -1.6, -0.5, 0.9, 1.4, 0.2],
    [-2.2, -1.6, -1.0, -0.4, 0.2, 0.6, 1.0, 1.5, 2.0, -1.2, -0.3, 0.8, 1.3, 0.5, 1.7],
    [-1.7, -1.1, -0.5, 0.1, 0.5, 0.9, 1.3, 1.8, -0.8, 0.3, 1.0, 1.5, 0.7, 1.2, 2.1],
    [-1.2, -0.6, 0.0, 0.4, 0.8, 1.2, 1.6, -0.3, 0.6, 1.1, 1.4, 0.9, 1.3, 1.8, 0.5],
    [-0.9, -0.3, 0.2, 0.6, 1.0, 1.4, 1.7, 0.1, 0.8, 1.2, 1.5, 1.1, 1.3, 0.9, 1.6],
  ],
  trongTamIndex: 5,
  title: 'Phân phối lợi suất ngày dịch dần sang phải',
  subtitle: 'Đơn vị: %, mỗi hàng là một năm. Số minh hoạ.',
  donVi: 'phan_tram',
};

const W = 700;
const H = 460;
/** Chieu cao mot duong nui tinh theo BUOC hang. 1,9 nghia la moi hang phu gan hai hang
 * duoi no. Duoi 1,2 thi cac hang roi rac va mat hieu ung day nui; tren 2,4 thi hang duoi
 * bi nuot gan het. */
const HE_SO_CHONG = 1.9;

function doLechChuan(v) {
  const tb = v.reduce((a, b) => a + b, 0) / v.length;
  return Math.sqrt(v.reduce((a, b) => a + (b - tb) ** 2, 0) / v.length);
}

function matDo(values, luoi) {
  const n = values.length;
  const h = 0.9 * doLechChuan(values) * Math.pow(n, -0.2) || 1;
  return luoi.map((x) => {
    let tong = 0;
    for (const v of values) {
      const z = (x - v) / h;
      tong += Math.exp(-0.5 * z * z);
    }
    return tong / (n * h * Math.sqrt(2 * Math.PI));
  });
}

export function option(params) {
  const { kyNames, kyValues, trongTamIndex, title, subtitle, donVi = 'phan_tram' } = params;
  if (kyNames.length < 4) {
    throw new Error('20-ridgeline: duoi 4 ky thi khong thanh day nui, dung 19-raincloud');
  }
  const dinhDangSo = dinhDangTheoDonVi(donVi);
  const tatCa = kyValues.flat();
  const min = Math.min(...tatCa);
  const max = Math.max(...tatCa);
  const dem = (max - min) * 0.1;
  const LUOI = 72;
  const luoi = Array.from({ length: LUOI }, (_, k) => min - dem + ((max - min + 2 * dem) * k) / (LUOI - 1));

  // Chuan hoa theo DINH CHUNG cua moi ky, khong theo tung ky. Chuan hoa tung ky se lam
  // moi hang cao bang nhau, tuc giau mat chuyen mot ky tap trung hon hay phan tan hon
  // ky khac, ma do chinh la mot nua cau chuyen ma ridgeline sinh ra de ke.
  const cacMatDo = kyValues.map((v) => matDo(v, luoi));
  const dinhChung = Math.max(...cacMatDo.flat());

  return {
    ...baseOption({ title, subtitle, width: W, height: H }),
    legend: { show: false },
    tooltip: { show: false },
    grid: { left: 76, right: 40, top: 68, bottom: 48 },
    xAxis: {
      type: 'value',
      min: min - dem,
      max: max + dem,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => dinhDangSo(v, { decimals: 0 }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    yAxis: {
      type: 'category',
      data: kyNames,
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { ...TYPOGRAPHY.axisLabel, fontFamily: FONT_STACK_MONO },
    },
    series: [
      {
        name: 'Dãy núi', type: 'custom', z: 1, silent: true,
        // Thu tu ve la thu tu cua mang `data`, tuc ky DAU tien ve truoc va ky CUOI cung
        // ve sau, nen hang duoi de len hang tren. Dung chieu chong lan cua mot day nui
        // nhin tu xa: ngon gan nguoi xem che ngon o xa.
        //
        // Da thu them `.reverse()` vao `data` va do la mot phep sua VO NGHIA: renderItem
        // tra du lieu bang `itemParams.dataIndex` chu khong bang gia tri trong mang, nen
        // dao mang chi doi thu tu duyet ma khong doi gi ca. Bo di thay vi de lai mot dong
        // ma trong nhu co tac dung.
        renderItem: (itemParams, api) => {
          const ki = itemParams.dataIndex;
          const yGoc = api.coord([0, ki])[1];
          const buoc = api.size([0, 1])[1];
          const cao = buoc * HE_SO_CHONG;
          const diem = cacMatDo[ki].map((d, k) => [
            api.coord([luoi[k], ki])[0],
            yGoc - (d / dinhChung) * cao,
          ]);
          const day = [
            [api.coord([luoi[LUOI - 1], ki])[0], yGoc],
            [api.coord([luoi[0], ki])[0], yGoc],
          ];
          const trongTam = ki === trongTamIndex;
          return {
            type: 'group',
            children: [
              {
                type: 'polygon',
                shape: { points: [...diem, ...day] },
                // To NEN chu khong chi ve duong: cac hang chong lan nhau, khong to thi
                // chung dan vao nhau thanh mot mo duong khong tach duoc bang mat.
                style: {
                  fill: trongTam ? PALETTE.accentSoft : PALETTE.paper,
                  opacity: trongTam ? 0.9 : 0.92,
                  stroke: trongTam ? PALETTE.accent : PALETTE.inkLo,
                  lineWidth: trongTam ? 1.8 : 1,
                },
              },
            ],
          };
        },
        data: kyNames.map((_, i) => [0, i]),
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. Chi tiet: 01-waterfall.mjs.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-20-ridgeline.svg', import.meta.url), svg);
  console.log('20-ridgeline: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
