import * as echarts from 'echarts';
import fs from 'node:fs';

// Waterfall chart (typical financial report chart type) using ECharts SSR
const chart = echarts.init(null, null, {
  renderer: 'svg',
  ssr: true,
  width: 700,
  height: 400,
});

const categories = ['Doanh thu Q1', 'Chi phi COGS', 'Chi phi VH', 'Thue', 'Loi nhuan rong'];
// waterfall trick: invisible base bar + visible delta bar
const data = [120, -45, -20, -8, 47];
let cum = 0;
const base = [];
const pos = [];
const neg = [];
data.forEach((d, i) => {
  if (i === 0 || i === data.length - 1) {
    base.push(0);
    if (d >= 0) { pos.push(d); neg.push('-'); } else { pos.push('-'); neg.push(d); }
    cum = d;
  } else {
    if (d >= 0) {
      base.push(cum);
      pos.push(d);
      neg.push('-');
      cum += d;
    } else {
      cum += d;
      base.push(cum);
      pos.push('-');
      neg.push(-d);
    }
  }
});

chart.setOption({
  backgroundColor: '#ffffff',
  title: { text: 'Waterfall: Tu doanh thu den loi nhuan rong (ty VND)', left: 'center', textStyle: { fontSize: 14 } },
  xAxis: { type: 'category', data: categories },
  yAxis: { type: 'value' },
  series: [
    { name: 'base', type: 'bar', stack: 'total', itemStyle: { color: 'transparent' }, data: base },
    { name: 'tang', type: 'bar', stack: 'total', itemStyle: { color: '#16a34a' }, data: pos },
    { name: 'giam', type: 'bar', stack: 'total', itemStyle: { color: '#dc2626' }, data: neg },
  ],
});

const svgStr = chart.renderToSVGString();
fs.writeFileSync('echarts-waterfall.svg', svgStr);
console.log('SVG length:', svgStr.length, 'bytes; contains <image>?', svgStr.includes('<image'));
