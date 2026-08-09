// 22-alluvial.mjs, Alluvial: cùng một tập thực thể ĐỔI NHÓM ra sao qua nhiều mốc
// Dùng khi: theo dõi một tập cố định được phân loại lại qua 3-5 mốc thời gian, vd hạng
// tín nhiệm của cùng nhóm doanh nghiệp qua ba năm, hay nhóm khách hàng chuyển bậc chi
// tiêu qua từng quý. Câu hỏi nó trả lời là AI CHUYỂN SANG ĐÂU, không phải bao nhiêu.
// KHÔNG dùng khi: đại lượng là dòng chảy bảo toàn qua các công đoạn (dùng 02-sankey,
// đó mới là sankey đúng nghĩa); chỉ có 2 mốc (dùng 05-slope, đọc nhanh hơn hẳn); quá 6
// nhóm mỗi mốc (dải chảy mảnh tới mức không lần được đường).
//
// Khác 02-sankey ở BẢN CHẤT ĐẠI LƯỢNG chứ không ở kỹ thuật vẽ, và đây là chỗ hay bị
// dùng sai: sankey theo dõi MỘT đại lượng bảo toàn (tiền, khối lượng) chảy qua các công
// đoạn khác nhau; alluvial theo dõi MỘT TẬP THỰC THỂ cố định bị phân loại lại qua các
// mốc. Ở sankey, tổng vào bằng tổng ra vì đó là cùng một dòng tiền. Ở alluvial, tổng
// mỗi mốc bằng nhau vì đó là cùng một nhóm doanh nghiệp được đếm lại.
//
// Dữ liệu cần: {mocNames:string[], nhomNames:string[], chuyen:[{tuMoc, tuNhom, denNhom,
// soLuong}]}. Bẫy: (1) đặt tên node trùng nhau giữa các mốc thì ECharts gộp chúng làm
// một và hình thành vòng lặp, nên tên node phải mang tiền tố mốc; (2) vẽ mọi dải cùng
// một màu thì mất khả năng lần theo một nhóm qua các mốc; (3) quên rằng tổng mỗi mốc
// phải bằng nhau, lệch tổng là dấu hiệu dữ liệu sai chứ không phải hình sai.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtNumber } from './fmt.mjs';

export const MAC_DINH = {
  mocNames: ['2024', '2025', '2026'],
  nhomNames: ['Hạng A', 'Hạng B', 'Hạng C'],
  // Số doanh nghiệp minh hoạ chuyển hạng tín nhiệm, KHÔNG phải số thật. Tổng mỗi mốc
  // đều là 100 vì đây là cùng một tập doanh nghiệp được xếp lại hạng.
  chuyen: [
    { tuMoc: 0, tuNhom: 0, denNhom: 0, soLuong: 22 },
    { tuMoc: 0, tuNhom: 0, denNhom: 1, soLuong: 8 },
    { tuMoc: 0, tuNhom: 1, denNhom: 0, soLuong: 6 },
    { tuMoc: 0, tuNhom: 1, denNhom: 1, soLuong: 34 },
    { tuMoc: 0, tuNhom: 1, denNhom: 2, soLuong: 10 },
    { tuMoc: 0, tuNhom: 2, denNhom: 1, soLuong: 5 },
    { tuMoc: 0, tuNhom: 2, denNhom: 2, soLuong: 15 },
    { tuMoc: 1, tuNhom: 0, denNhom: 0, soLuong: 24 },
    { tuMoc: 1, tuNhom: 0, denNhom: 1, soLuong: 4 },
    { tuMoc: 1, tuNhom: 1, denNhom: 0, soLuong: 9 },
    { tuMoc: 1, tuNhom: 1, denNhom: 1, soLuong: 33 },
    { tuMoc: 1, tuNhom: 1, denNhom: 2, soLuong: 5 },
    { tuMoc: 1, tuNhom: 2, denNhom: 1, soLuong: 11 },
    { tuMoc: 1, tuNhom: 2, denNhom: 2, soLuong: 14 },
  ],
  title: 'Hạng tín nhiệm dịch chuyển qua ba năm',
  subtitle: 'Đơn vị: số doanh nghiệp, cùng một tập 100 doanh nghiệp. Số minh hoạ.',
};

const W = 720;
const H = 420;

export function option(params) {
  const { mocNames, nhomNames, chuyen, title, subtitle } = params;
  if (nhomNames.length > 6) {
    throw new Error('22-alluvial: qua 6 nhom moi moc, dai chay manh toi muc khong lan duoc duong');
  }

  // Kiem tong moi moc bang nhau. Lech tong o alluvial la dau hieu DU LIEU sai (mot thuc
  // the bi dem hai lan hoac roi mat), khong phai chuyen bo cuc, nen fail-fast luc build
  // chu khong de no thanh mot dai chay lech ma khong ai doi chieu.
  const tongTheoMoc = mocNames.map((_, mi) => {
    if (mi === 0) return chuyen.filter((c) => c.tuMoc === 0).reduce((a, c) => a + c.soLuong, 0);
    return chuyen.filter((c) => c.tuMoc === mi - 1).reduce((a, c) => a + c.soLuong, 0);
  });
  const khac = tongTheoMoc.filter((t) => t !== tongTheoMoc[0]);
  if (khac.length) {
    throw new Error(
      `22-alluvial: tong moi moc phai bang nhau vi day la cung mot tap thuc the, dang la ${tongTheoMoc.join(', ')}`,
    );
  }

  // Ten node PHAI mang tien to moc. Dat trung ten giua cac moc thi ECharts gop chung lam
  // mot node va hinh thanh vong lap, luc do sankey khong con la do thi khong chu trinh
  // va bo cuc vo hoan toan.
  const maNode = (mi, ni) => `${mocNames[mi]} · ${nhomNames[ni]}`;
  const nodes = [];
  mocNames.forEach((_, mi) => {
    nhomNames.forEach((ten, ni) => {
      nodes.push({
        name: maNode(mi, ni),
        // Mau theo NHOM chu khong theo moc: nho vay mat lan duoc mot nhom qua ca ba moc.
        itemStyle: { color: [PALETTE.accent, PALETTE.inkLo, PALETTE.negative][ni % 3] },
        label: { show: mi === 0, position: 'left', formatter: () => ten, ...TYPOGRAPHY.axisLabel },
      });
    });
  });

  const links = chuyen.map((c) => ({
    source: maNode(c.tuMoc, c.tuNhom),
    target: maNode(c.tuMoc + 1, c.denNhom),
    value: c.soLuong,
    lineStyle: {
      // To dai chay theo nhom NGUON: mat lan theo mot nhom di dau bang cach bam mot mau.
      color: [PALETTE.accent, PALETTE.inkLo, PALETTE.negative][c.tuNhom % 3],
      opacity: c.tuNhom === c.denNhom ? 0.22 : 0.45,
    },
  }));

  return {
    ...baseOption({ title, subtitle, width: W, height: H }),
    legend: { show: false },
    tooltip: {
      trigger: 'item',
      formatter: (p) =>
        p.dataType === 'edge'
          ? `${p.data.source} sang ${p.data.target}<br/>${fmtNumber(p.data.value, { decimals: 0 })} doanh nghiệp`
          : p.name,
      textStyle: TYPOGRAPHY.axisLabel,
    },
    series: [
      {
        type: 'sankey',
        left: 96, right: 96, top: 76, bottom: 46,
        nodeWidth: 14,
        nodeGap: 14,
        // `none` chu khong phai mac dinh `justify`: alluvial can moi moc dung thanh MOT
        // cot thang hang, con thuat toan can bang cua ECharts se keo node khong co dong
        // vao ve phia trai va lam hong cot.
        nodeAlign: 'justify',
        layoutIterations: 0,
        emphasis: { focus: 'adjacency' },
        data: nodes,
        links,
        label: { ...TYPOGRAPHY.axisLabel, fontFamily: FONT_STACK },
      },
    ],
    graphic: mocNames.map((ten, mi) => ({
      // Nhan moc ve bang graphic: sankey khong co truc x nen khong co cho nao khac de
      // dat ten moc thoi gian, ma thieu no thi nguoi doc khong biet ba cot la ba nam.
      type: 'text',
      left: 96 + (mi * (W - 192)) / (mocNames.length - 1) - 14,
      top: 58,
      style: { text: ten, font: `bold 11px ${FONT_STACK}`, fill: PALETTE.inkMd, textAlign: 'center' },
      silent: true,
    })),
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. Chi tiet: 01-waterfall.mjs.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-22-alluvial.svg', import.meta.url), svg);
  console.log('22-alluvial: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
