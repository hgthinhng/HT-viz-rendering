// 19-raincloud.mjs, Raincloud: hình dạng phân phối đầy đủ, không giấu cỡ mẫu
// Dùng khi: cần so HÌNH DẠNG phân phối của một chỉ tiêu giữa 2-5 nhóm và n đủ lớn
// (~20-200) để hình dạng có nghĩa, vd phân phối biên lợi nhuận của các doanh nghiệp
// trong ba ngành, hoặc phân phối lợi suất ngày của ba quỹ.
// KHÔNG dùng khi: n dưới 15 mỗi nhóm (đường mật độ thành hình bịa, dùng
// 16-dot-distribution để thấy từng điểm); cần quartile chính xác bằng số (dùng bảng);
// quá 5 nhóm (chiều cao mỗi hàng co lại tới mức đám mây thành một vệt).
//
// Ba lớp chồng lên nhau, mỗi lớp trả lời một câu hỏi khác nhau, và đó là toàn bộ lý do
// preset này tồn tại thay vì một boxplot:
//   đám mây  hình dạng phân phối. Boxplot giấu mất chuyện phân phối hai đỉnh: hai nhóm
//            có cùng trung vị và cùng quartile vẫn có thể mang hai câu chuyện khác hẳn.
//   hộp      quartile và trung vị, để so nhanh giữa các nhóm bằng một mốc chung.
//   mưa      từng quan sát một. Người đọc thấy cỡ mẫu thật thay vì phải tin.
//
// Dữ liệu cần: nhóm {name, values:number[]}. Bẫy: (1) jitter ngẫu nhiên làm mỗi lần
// render ra một ảnh khác nhau, phá visual regression, nên dùng công thức TẤT ĐỊNH theo
// chỉ số; (2) bandwidth cố định làm nhóm phương sai nhỏ trông phẳng lì, nên tính theo
// quy tắc Silverman trên CHÍNH nhóm đó; (3) vẽ đám mây đối xứng hai bên như violin thì
// mất chỗ cho mưa, nên chỉ vẽ NỬA trên.
import { baseOption, TYPOGRAPHY, PALETTE } from './theme.mjs';
import { dinhDangTheoDonVi } from './fmt.mjs';
import { validateSeries } from './schema.mjs';

export const MAC_DINH = {
  groupNames: ['Ngân hàng', 'Bất động sản', 'Bán lẻ'],
  // Biên lợi nhuận minh hoạ theo ngành, KHÔNG phải số thật. Nhóm 2 CỐ Ý hai đỉnh để
  // cho thấy đúng thứ mà một boxplot sẽ giấu đi.
  groupValues: [
    [18.2, 19.5, 17.8, 20.1, 18.9, 21.3, 17.2, 19.8, 20.5, 18.4, 19.1, 22.0, 16.9, 19.3, 20.8],
    [8.1, 9.0, 7.5, 8.8, 9.4, 24.2, 25.1, 23.8, 26.0, 24.9, 8.3, 9.2, 25.5, 7.9, 24.4],
    [12.4, 13.1, 11.8, 14.0, 12.9, 13.6, 11.5, 12.2, 13.8, 12.7, 14.3, 11.9, 13.3, 12.5, 13.0],
  ],
  trongTamIndex: 1,
  title: 'Phân phối biên lợi nhuận theo ngành',
  subtitle: 'Đơn vị: %, mỗi chấm là một doanh nghiệp. Số minh hoạ.',
  // Khoi meta BAT BUOC cua moi preset: don vi va nguon. Xem charts/echarts/schema.mjs.
  series: {
    unit: 'phan_tram',
    source: { tier: 'uoc-tinh', label: 'Số minh hoạ, không phải số công bố' },
    as_of: '2026-08-09',
  },
};

const W = 720;
const H = 420;

function sapXep(v) {
  return [...v].sort((a, b) => a - b);
}

function phanVi(daSap, p) {
  const i = (daSap.length - 1) * p;
  const lo = Math.floor(i);
  const hi = Math.ceil(i);
  return lo === hi ? daSap[lo] : daSap[lo] + (daSap[hi] - daSap[lo]) * (i - lo);
}

function doLechChuan(v) {
  const tb = v.reduce((a, b) => a + b, 0) / v.length;
  return Math.sqrt(v.reduce((a, b) => a + (b - tb) ** 2, 0) / v.length);
}

/** Mat do nhan Gauss, bandwidth theo quy tac Silverman tren CHINH nhom do.
 *
 * Bandwidth co dinh se lam nhom phuong sai nho trong phang li va nhom phuong sai lon
 * trong nhoe, tuc hai nhom trong khac nhau vi mot tham so ve chu khong vi du lieu. */
function matDo(values, luoi) {
  const n = values.length;
  const daSap = sapXep(values);
  const iqr = phanVi(daSap, 0.75) - phanVi(daSap, 0.25);
  const sigma = Math.min(doLechChuan(values), iqr > 0 ? iqr / 1.349 : Infinity);
  // He so 0,55 chu khong phai 0,9 cua Silverman goc. Silverman toi uu cho phan phoi MOT
  // dinh; voi phan phoi hai dinh no lam muot qua tay va noi hai buou thanh mot cao nguyen
  // phang, tuc xoa mat dung cai ma preset nay sinh ra de cho thay. Do tren nhom demo hai
  // cum (8-9 va 24-26): he so 0,9 cho mot khoi gan phang, 0,55 cho hai buou tach roi.
  const h = 0.55 * (Number.isFinite(sigma) ? sigma : doLechChuan(values)) * Math.pow(n, -0.2) || 1;
  return luoi.map((x) => {
    let tong = 0;
    for (const v of values) {
      const z = (x - v) / h;
      tong += Math.exp(-0.5 * z * z);
    }
    return tong / (n * h * Math.sqrt(2 * Math.PI));
  });
}

/** Jitter TAT DINH theo chi so, khong dung Math.random().
 *
 * Mot chart doi hinh moi lan render thi visual regression khong con nghia gi, va nguoi
 * doc so hai ban cua cung mot bao cao se thay hai hinh khac nhau. Day so nay trai deu
 * va khong tao van deu mat vi buoc nhay khong chia het cho chu ky nao. */
function jitter(i) {
  return ((i * 2654435761) % 1000) / 1000 - 0.5;
}

export function option(params) {
  const { groupNames, groupValues, trongTamIndex, title, subtitle , series} = params;
  // Moi preset deu di qua lop schema: `series` mang don vi va nguon, va do la
  // dieu kien de mot con so tren hinh truy nguoc duoc ve nguon cua no.
  validateSeries(series);
  const dinhDangSo = dinhDangTheoDonVi(series.unit);
  if (groupNames.length > 5) {
    throw new Error('19-raincloud: qua 5 nhom, moi hang co lai toi muc dam may thanh mot vet');
  }
  const laTrongTam = (i) => i === trongTamIndex;

  const tatCa = groupValues.flat();
  const min = Math.min(...tatCa);
  const max = Math.max(...tatCa);
  const dem = (max - min) * 0.08;
  const LUOI = 64;
  const luoi = Array.from({ length: LUOI }, (_, k) => min - dem + ((max - min + 2 * dem) * k) / (LUOI - 1));

  // Mat do chuan hoa THEO TUNG NHOM: dinh cao nhat cua moi nhom deu cham tran cua hang
  // do. Chuan hoa chung mot thang se lam nhom phan tan rong gan nhu phang, va nguoi doc
  // se doc nham do phang do thanh "khong co gi xay ra o day".
  const cacMatDo = groupValues.map((v) => {
    const d = matDo(v, luoi);
    const dinh = Math.max(...d);
    return d.map((x) => x / dinh);
  });

  return {
    ...baseOption({ title, subtitle, width: W, height: H }),
    legend: { show: false },
    tooltip: { show: false },
    grid: { left: 130, right: 40, top: 64, bottom: 48 },
    xAxis: {
      type: 'value',
      min: min - dem,
      max: max + dem,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => dinhDangSo(v, { decimals: 0 }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    yAxis: {
      type: 'category',
      data: groupNames,
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: TYPOGRAPHY.axisLabel,
    },
    series: [
      {
        // Lop 1, dam may: nua tren cua duong mat do.
        name: 'Đám mây', type: 'custom', z: 1, silent: true,
        renderItem: (itemParams, api) => {
          const gi = itemParams.dataIndex;
          const yGoc = api.coord([0, gi])[1];
          const caoHang = api.size([0, 1])[1];
          const caoMay = caoHang * 0.34;
          const diem = cacMatDo[gi].map((d, k) => {
            const x = api.coord([luoi[k], gi])[0];
            return [x, yGoc - 2 - d * caoMay];
          });
          const day = [
            [api.coord([luoi[LUOI - 1], gi])[0], yGoc - 2],
            [api.coord([luoi[0], gi])[0], yGoc - 2],
          ];
          return {
            type: 'polygon',
            shape: { points: [...diem, ...day] },
            style: {
              fill: laTrongTam(gi) ? PALETTE.accentSoft : PALETTE.line,
              opacity: laTrongTam(gi) ? 0.55 : 0.7,
              stroke: laTrongTam(gi) ? PALETTE.accent : PALETTE.inkLo,
              lineWidth: 1,
            },
          };
        },
        data: groupNames.map((_, i) => [0, i]),
      },
      {
        // Lop 2, hop: Q1 den Q3 cong vach trung vi.
        name: 'Hộp', type: 'custom', z: 3, silent: true,
        renderItem: (itemParams, api) => {
          const gi = itemParams.dataIndex;
          const daSap = sapXep(groupValues[gi]);
          const y = api.coord([0, gi])[1];
          const x1 = api.coord([phanVi(daSap, 0.25), gi])[0];
          const x3 = api.coord([phanVi(daSap, 0.75), gi])[0];
          const xm = api.coord([phanVi(daSap, 0.5), gi])[0];
          const cao = 7;
          return {
            type: 'group',
            children: [
              {
                type: 'rect',
                shape: { x: x1, y: y - cao / 2, width: x3 - x1, height: cao },
                // KHONG to nen: hop cua mot nhom hai dinh trai rat rong, to nen se che
                // mat thung lung giua hai buou, dung phan mang thong tin.
                style: { fill: 'none', stroke: PALETTE.inkMd, lineWidth: 1 },
              },
              {
                type: 'line',
                shape: { x1: xm, y1: y - cao, x2: xm, y2: y + cao },
                // Vach trung vi cua nhom trong tam DAY hon, khong doi mau: mau danh cho
                // phan loai, do day danh cho nhan manh.
                style: { stroke: PALETTE.ink, lineWidth: laTrongTam(gi) ? 3 : 1.6 },
              },
            ],
          };
        },
        data: groupNames.map((_, i) => [0, i]),
      },
      {
        // Lop 3, mua: tung quan sat mot, jitter tat dinh xuong duoi hop.
        name: 'Mưa', type: 'custom', z: 2, silent: true,
        renderItem: (itemParams, api) => {
          const gi = itemParams.dataIndex;
          const yGoc = api.coord([0, gi])[1];
          const caoHang = api.size([0, 1])[1];
          const bienDo = caoHang * 0.18;
          const cham = groupValues[gi].map((v, k) => ({
            type: 'circle',
            shape: {
              cx: api.coord([v, gi])[0],
              cy: yGoc + caoHang * 0.16 + jitter(k + gi * 97) * bienDo,
              r: 2.6,
            },
            style: {
              fill: laTrongTam(gi) ? PALETTE.accent : PALETTE.inkLo,
              opacity: 0.75,
            },
          }));
          return { type: 'group', children: cham };
        },
        data: groupNames.map((_, i) => [0, i]),
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. Chi tiet: 01-waterfall.mjs.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-19-raincloud.svg', import.meta.url), svg);
  console.log('19-raincloud: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
