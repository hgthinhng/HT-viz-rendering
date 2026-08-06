// 02-sankey.mjs — Sankey: dòng tiền / phân bổ doanh thu qua các tầng chi phí
// Dùng khi: theo dõi MỘT đại lượng bảo toàn (tiền, khối lượng) chảy qua nhiều
// tầng phân nhánh (Doanh thu -> Giá vốn/Lợi nhuận gộp -> Chi phí/EBIT -> Thuế/LNST
// -> Cổ tức/Lợi nhuận giữ lại). KHÔNG dùng khi các tầng không cộng dồn được
// (vd trộn đơn vị tỷ đồng với tỷ lệ % trong cùng luồng).
// Dữ liệu cần: danh sách node {name} + danh sách edge {source, target, value}.
// Bẫy thường gặp: (1) tổng value ra không khớp tổng value vào tại 1 node ->
// sai bảo toàn, phải kiểm tổng trước khi vẽ; (2) quá nhiều node (>10-12) làm
// rối; (3) dùng màu ngẫu nhiên cho từng luồng thay vì tô theo node nguồn.
import * as echarts from 'echarts';
import fs from 'node:fs';
import { baseOption, TYPOGRAPHY, PALETTE } from './theme.mjs';

const nodes = [
  { name: 'Doanh thu thuần' },
  { name: 'Giá vốn hàng bán' },
  { name: 'Lợi nhuận gộp' },
  { name: 'Chi phí bán hàng & QLDN' },
  { name: 'EBIT' },
  { name: 'Chi phí lãi vay & thuế' },
  { name: 'Lợi nhuận sau thuế' },
  { name: 'Cổ tức chi trả' },
  { name: 'Lợi nhuận giữ lại' },
];
// kiểm tổng bảo toàn tại từng node trước khi vẽ (không lặng lẽ chấp nhận sai lệch)
const links = [
  { source: 'Doanh thu thuần', target: 'Giá vốn hàng bán', value: 78 },
  { source: 'Doanh thu thuần', target: 'Lợi nhuận gộp', value: 42 },
  { source: 'Lợi nhuận gộp', target: 'Chi phí bán hàng & QLDN', value: 18 },
  { source: 'Lợi nhuận gộp', target: 'EBIT', value: 24 },
  { source: 'EBIT', target: 'Chi phí lãi vay & thuế', value: 9 },
  { source: 'EBIT', target: 'Lợi nhuận sau thuế', value: 15 },
  { source: 'Lợi nhuận sau thuế', target: 'Cổ tức chi trả', value: 6 },
  { source: 'Lợi nhuận sau thuế', target: 'Lợi nhuận giữ lại', value: 9 },
];

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
const problems = checkConservation(nodes, links);
if (problems.length) {
  console.error('CANH BAO bao toan sankey:', problems);
  process.exit(1);
}

const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: 760, height: 440 });
chart.setOption({
  ...baseOption({ title: 'Dòng phân bổ doanh thu qua các tầng chi phí', subtitle: 'Đơn vị: tỷ đồng, FY2026' }),
  tooltip: { trigger: 'item', textStyle: { fontSize: 12 } },
  series: [
    {
      type: 'sankey',
      left: 16, right: 140, top: 60, bottom: 40,
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
});

const svg = chart.renderToSVGString();
fs.writeFileSync(new URL('./out-02-sankey.svg', import.meta.url), svg);
console.log('02-sankey: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));

chart.dispose();
process.exit(0);
