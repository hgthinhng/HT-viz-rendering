// 23-waffle.mjs, Waffle: tỷ trọng đọc bằng cách ĐẾM ô, không phải ước lượng góc
// Dùng khi: cần người đọc nắm chắc một cơ cấu 2-5 phần và con số phải neo lại trong
// đầu, vd cơ cấu nguồn vốn, tỷ lệ danh mục theo nhóm tài sản, phần doanh thu đến từ
// một khách hàng lớn. Một trăm ô vuông là một trăm phần trăm, đếm được từng ô.
// KHÔNG dùng khi: cần so cơ cấu qua NHIỀU kỳ (dùng 11-stacked-100, waffle nhiều lưới
// cạnh nhau đọc rất chậm); có phần dưới 1% (một ô là đơn vị nhỏ nhất, dưới đó phải làm
// tròn và làm tròn cơ cấu là chỗ dễ nói dối); quá 5 phần (bảng màu hết chỗ phân biệt).
//
// Vì sao không phải biểu đồ tròn: mắt người ước lượng GÓC kém hơn hẳn so với đếm ô hay
// so chiều dài. Waffle bỏ hẳn thao tác ước lượng: người đọc đếm, và số đếm được đúng
// bằng con số trong văn xuôi. Đó cũng là lý do preset này KHÔNG nằm trong danh sách
// cấm cùng gauge và radar dù nhìn cũng lạ mắt: nó thay một phép ước lượng bằng một
// phép đếm chứ không thay một phép so bằng một phép ước lượng.
//
// Dữ liệu cần: {phan:[{ten, phanTram}]}. Bẫy: (1) tổng không đúng 100 thì lưới thiếu
// hoặc thừa ô, phải kiểm lúc build; (2) tô ô theo hàng ngang khi cơ cấu lệch làm một
// phần bị cắt vụn qua nhiều hàng, nên tô theo CỘT; (3) đặt chú giải rời khỏi lưới buộc
// mắt nhảy qua lại, nên gắn nhãn ngay cạnh khối màu.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';

export const MAC_DINH = {
  phan: [
    { ten: 'Vốn chủ sở hữu', phanTram: 42 },
    { ten: 'Nợ vay dài hạn', phanTram: 31 },
    { ten: 'Nợ vay ngắn hạn', phanTram: 18 },
    { ten: 'Phải trả khác', phanTram: 9 },
  ],
  title: 'Cơ cấu nguồn vốn, mỗi ô là một phần trăm',
  subtitle: 'Đơn vị: %, tổng 100 ô. Số minh hoạ.',
};

const W = 680;
const H = 400;
const COT = 10;
const HANG = 10;

export function option(params) {
  const { phan, title, subtitle } = params;
  if (phan.length > 5) {
    throw new Error('23-waffle: qua 5 phan, bang mau het cho phan biet');
  }
  const tong = phan.reduce((a, p) => a + p.phanTram, 0);
  if (Math.round(tong) !== 100) {
    throw new Error(`23-waffle: tong phai bang 100, dang la ${tong}. Luoi se thieu hoac thua o`);
  }
  const duoi1 = phan.filter((p) => p.phanTram < 1);
  if (duoi1.length) {
    throw new Error(
      `23-waffle: phan duoi 1% khong ve duoc vi mot o la don vi nho nhat: ${duoi1.map((p) => p.ten).join(', ')}`,
    );
  }

  const MAU = [PALETTE.accent, PALETTE.inkLo, PALETTE.accentSoft, PALETTE.negative, PALETTE.warn];

  // To theo COT chu khong theo hang: doc theo cot thi moi phan la mot khoi lien nhau,
  // con to theo hang thi mot phan 18% bi cat vun qua hai hang va mat khong con dem duoc
  // no bang mot lan nhin.
  const oPhan = [];
  let da = 0;
  phan.forEach((p, pi) => {
    const so = Math.round(p.phanTram);
    for (let k = 0; k < so; k++) {
      const chiSo = da + k;
      oPhan.push({ cot: Math.floor(chiSo / HANG), hang: chiSo % HANG, pi });
    }
    da += so;
  });

  return {
    ...baseOption({ title, subtitle, width: W, height: H }),
    legend: { show: false },
    tooltip: { show: false },
    grid: { left: 40, right: 250, top: 70, bottom: 40 },
    xAxis: { type: 'value', min: 0, max: COT, show: false },
    yAxis: { type: 'value', min: 0, max: HANG, show: false },
    series: [
      {
        name: 'Ô', type: 'custom', z: 2, silent: true,
        renderItem: (itemParams, api) => {
          const o = oPhan[itemParams.dataIndex];
          const [x0, y0] = api.coord([o.cot, o.hang + 1]);
          const [x1, y1] = api.coord([o.cot + 1, o.hang]);
          const khe = 3;
          return {
            type: 'rect',
            shape: {
              x: x0 + khe / 2,
              y: y0 + khe / 2,
              width: Math.abs(x1 - x0) - khe,
              height: Math.abs(y1 - y0) - khe,
            },
            style: { fill: MAU[o.pi % MAU.length] },
          };
        },
        data: oPhan.map((o) => [o.cot, o.hang]),
      },
      {
        // Chu giai gan NGAY canh luoi, moi dong mot khoi mau cong ten cong con so. Dat
        // chu giai roi ra buoc mat nhay qua lai giua hai vung de doi chieu mau.
        name: 'Chú giải', type: 'custom', z: 3, silent: true,
        renderItem: (itemParams, api) => {
          if (itemParams.dataIndex !== 0) return null;
          const [xPhai] = api.coord([COT, 0]);
          const [, yDinh] = api.coord([0, HANG]);
          const buoc = 30;
          const con = [];
          phan.forEach((p, pi) => {
            const y = yDinh + 6 + pi * buoc;
            con.push(
              { type: 'rect', shape: { x: xPhai + 28, y, width: 12, height: 12 }, style: { fill: MAU[pi % MAU.length] } },
              {
                type: 'text', x: xPhai + 48, y: y - 1,
                style: { text: p.ten, font: `11px ${FONT_STACK}`, fill: PALETTE.ink, textAlign: 'left' },
              },
              {
                type: 'text', x: xPhai + 48, y: y + 13,
                style: {
                  text: fmtPercent(p.phanTram, { decimals: 0 }),
                  font: `bold 12px ${FONT_STACK}`,
                  fill: MAU[pi % MAU.length],
                  textAlign: 'left',
                },
              },
            );
          });
          return { type: 'group', children: con };
        },
        data: oPhan.map((o) => [o.cot, o.hang]),
      },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. Chi tiet: 01-waterfall.mjs.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-23-waffle.svg', import.meta.url), svg);
  console.log('23-waffle: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
