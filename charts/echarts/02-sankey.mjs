// 02-sankey.mjs, Sankey: dòng tiền / phân bổ doanh thu qua các tầng chi phí
// Dùng khi: theo dõi MỘT đại lượng bảo toàn (tiền, khối lượng) chảy qua nhiều
// tầng phân nhánh (Doanh thu -> Giá vốn/Lợi nhuận gộp -> Chi phí/EBIT -> Thuế/LNST
// -> Cổ tức/Lợi nhuận giữ lại). KHÔNG dùng khi các tầng không cộng dồn được
// (vd trộn đơn vị tỷ đồng với tỷ lệ % trong cùng luồng).
// Dữ liệu cần: danh sách node {name} + danh sách edge {source, target, value}.
// Bẫy thường gặp: (1) tổng value ra không khớp tổng value vào tại 1 node ->
// sai bảo toàn, phải kiểm tổng trước khi vẽ; (2) quá nhiều node (>10-12) làm
// rối; (3) dùng màu ngẫu nhiên cho từng luồng thay vì tô theo node nguồn.
import { baseOption, TYPOGRAPHY, PALETTE } from './theme.mjs';
import { validateSeries, epDonVi } from './schema.mjs';

export const MAC_DINH = {
  nodes: [
    { name: 'Doanh thu thuần' },
    { name: 'Giá vốn hàng bán' },
    { name: 'Lợi nhuận gộp' },
    { name: 'Chi phí bán hàng & QLDN' },
    { name: 'EBIT' },
    { name: 'Chi phí lãi vay & thuế' },
    { name: 'Lợi nhuận sau thuế' },
    { name: 'Cổ tức chi trả' },
    { name: 'Lợi nhuận giữ lại' },
  ],
  links: [
    { source: 'Doanh thu thuần', target: 'Giá vốn hàng bán', value: 78 },
    { source: 'Doanh thu thuần', target: 'Lợi nhuận gộp', value: 42 },
    { source: 'Lợi nhuận gộp', target: 'Chi phí bán hàng & QLDN', value: 18 },
    { source: 'Lợi nhuận gộp', target: 'EBIT', value: 24 },
    { source: 'EBIT', target: 'Chi phí lãi vay & thuế', value: 9 },
    { source: 'EBIT', target: 'Lợi nhuận sau thuế', value: 15 },
    { source: 'Lợi nhuận sau thuế', target: 'Cổ tức chi trả', value: 6 },
    { source: 'Lợi nhuận sau thuế', target: 'Lợi nhuận giữ lại', value: 9 },
  ],
  title: 'Dòng phân bổ doanh thu qua các tầng chi phí',
  subtitle: 'Đơn vị: tỷ đồng, FY2026',
  // Khoi meta BAT BUOC cua moi preset: don vi va nguon. Xem charts/echarts/schema.mjs.
  series: {
    unit: 'ty_dong',
    source: { tier: 'uoc-tinh', label: 'Số minh hoạ, không phải số công bố' },
    as_of: '2026-08-09',
  },
};

function checkConservation(nodes, links) {
  const inflow = {}, outflow = {};
  links.forEach((l) => {
    outflow[l.source] = (outflow[l.source] || 0) + l.value;
    inflow[l.target] = (inflow[l.target] || 0) + l.value;
  });
  const problems = [];
  nodes.forEach((n) => {
    const hasIn = inflow[n.name] !== undefined;
    const hasOut = outflow[n.name] !== undefined;
    if (hasIn && hasOut && Math.abs(inflow[n.name] - outflow[n.name]) > 0.01) {
      problems.push(`${n.name}: vào=${inflow[n.name]} ra=${outflow[n.name]} LỆCH`);
    }
  });
  return problems;
}

/** Tra ve OBJECT OPTION thuan. FAIL ngay (throw) neu du lieu vi pham bao toan --
 * kiem TRONG option() de fail-fast luc goi voi du lieu that, khong chi voi MAC_DINH. */
export function option(params) {
  const { nodes, links, title, subtitle , series} = params;
  // Moi preset deu di qua lop schema. `epDonVi` la loi khai THAT THA cua preset
  // nay: ham dinh dang cua no gan chat voi don vi ty_dong, nen truyen don vi
  // khac se cho mot nhan sai su that. Bao loi luc build con hon ve ra nhan sai.
  validateSeries(series);
  epDonVi(series, ['ty_dong']);
  const problems = checkConservation(nodes, links);
  if (problems.length) {
    throw new Error(`02-sankey: canh bao bao toan sankey: ${problems.join('; ')}`);
  }

  return {
    ...baseOption({ title, subtitle }),
    tooltip: { trigger: 'item', textStyle: { fontSize: 12 } },
    series: [
      {
        type: 'sankey',
        // Le phai 140 CHUA DU: nhan dai nhat "Chi phi ban hang & QLDN" tran ra
        // ngoai viewBox 17px va bi cat cut thanh "... & Ql" khi SVG nhung vao
        // HTML hoac render sang PDF. Do bang getBoundingClientRect tren trinh
        // duyet that ngay 08-08.
        //
        // Cai lam bug nay song lau: KHONG gate nao bat duoc. Gate 5 CHART-SONG
        // kiem chu cua SVG co mat trong tang text cua PDF, ma chu CO mat, no chi
        // nam ngoai khung nhin. Dem net ve dung, XML hop le, gate xanh, nhan van
        // cut. Xem gate moi `chu-khong-tran-viewbox`.
        left: 16, right: 162, top: 60, bottom: 40,
        nodeWidth: 14,
        nodeGap: 14,
        layoutIterations: 32,
        data: nodes.map((n) => ({ ...n, itemStyle: { color: PALETTE.ink } })),
        links,
        lineStyle: { color: 'source', opacity: 0.35, curveness: 0.5 },
        label: { ...TYPOGRAPHY.dataLabel, position: 'right', formatter: (p) => p.name },
        emphasis: { focus: 'adjacency' },
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
  try {
    const { writeFileSync } = await import('node:fs');
    const svg = renderStatic(option, MAC_DINH, { width: 760, height: 440 });
    writeFileSync(new URL('./out-02-sankey.svg', import.meta.url), svg);
    console.log('02-sankey: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
    process.exit(0);
  } catch (e) {
    console.error('CANH BAO', e.message);
    process.exit(1);
  }
}
