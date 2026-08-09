// echarts-song.mjs, cua ECharts DUY NHAT cho lan `html-song`.
//
// Vi sao khong `import * as echarts from 'echarts'` nhu render-static.mjs: ban day du
// keo 1,1MB vao MOI file an pham, ma an pham lan nay la mot file tu du nen moi byte
// deu nam trong file nguoi doc tai ve. Ban nay khai dung nhung gi 18 preset dung toi.
// Danh sach do TU DANH SACH DA DO cua Phase 4, khong phai doan: 733KB tho so voi 1,1MB,
// giam 371KB tuc 33%.
//
// **Them preset moi ma quen them module vao day thi chart im lang khong ve gi**, khong
// bao loi ro rang. `tests/consistency/bundle_song.test.mjs` goi `option()` that cua ca
// 18 preset, gom moi `series.type` xuat hien, roi doi chieu voi danh sach duoi day, nen
// quen la test do chu khong phai nho nguoi review nhin thay.
//
// Renderer: CHI SVGRenderer, va do la mot doi huong so voi ban dau tien cua mount-live.
// Ba ly do, xep theo suc nang:
//   1. Gate `THEME-MATCH` cua lan song quet `document.querySelectorAll('svg')`. Chart
//      canvas khong sinh the <svg> nao nen gate mu hoan toan voi dung phan de sai chu
//      de nhat. Chon SVG la chon nam trong tam gate.
//   2. Chu trong chart chon duoc va copy duoc, dung mach voi mot ban bao cao.
//   3. Hai lan dung cung mot renderer nen dien mao khong the lech nhau.
// Danh doi da biet: canvas nhanh hon khi so diem rat lon. Chart bao cao tai chinh cua
// repo nay khong roi vao vung do (nhieu nhat la luoi do nhay 18 nhan mot chieu).
import * as echarts from 'echarts/core';
import {
  BarChart,
  LineChart,
  ScatterChart,
  CustomChart,
  HeatmapChart,
  SankeyChart,
  TreemapChart,
  CandlestickChart,
} from 'echarts/charts';
import {
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
  GraphicComponent,
  MarkLineComponent,
  MarkPointComponent,
  MarkAreaComponent,
  VisualMapComponent,
} from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { SVGRenderer } from 'echarts/renderers';

echarts.use([
  BarChart,
  LineChart,
  ScatterChart,
  CustomChart,
  HeatmapChart,
  SankeyChart,
  TreemapChart,
  CandlestickChart,
  GridComponent,
  TooltipComponent,
  TitleComponent,
  LegendComponent,
  GraphicComponent,
  MarkLineComponent,
  MarkPointComponent,
  MarkAreaComponent,
  VisualMapComponent,
  LabelLayout,
  SVGRenderer,
]);

/** Loai series ma cua nay phuc vu. Gate doi chieu danh sach nay voi `option()` that. */
export const SERIES_DUOC_PHEP = Object.freeze([
  'bar',
  'line',
  'scatter',
  'custom',
  'heatmap',
  'sankey',
  'treemap',
  'candlestick',
]);

export { echarts };
