// render-static.mjs, duong xuat CHUNG cho lan `pdf-so`: option() thuan -> chuoi SVG
// tinh, da hau xu ly mau.
//
// Day la NOI DUY NHAT preset ECharts duoc phep khai animation:false. Ly do khong con
// la tham my: ECharts SSR xuat CSS @keyframes cho moi marker, va keyframe cuoi la
// `transform: scale(n,n)` -- CSS transform THANG thuoc tinh XML, keyframe do khong
// mang phan translate, nen sau khi animation chay xong marker bi keo ve GOC TOA DO va
// phong to. Da nhin tan mat tren out-04-dumbbell.svg truoc khi va: moi cham
// before/after bien mat khoi vi tri dung, con mot cham lac o goc tren trai. Chi hong o
// ban mo bang trinh duyet; ban SSR tinh khong tu chay CSS animation nen khong dinh,
// nhung ban HTML `html-song` (qua mount-live.mjs, KHONG di qua file nay) thi co,
// nen phai tat DUT KHOAT o day truoc khi xuat chuoi SVG.
//
// Preset (charts/echarts/NN-ten.mjs) tuyet doi KHONG tu khai animation trong option()
// cua minh: viec do thuoc ve day, ap dung UNG DUNG cho MOI preset bat ke preset co
// nho khai hay khong (spread option() cua preset ROI moi ghi de animation:false).
import * as echarts from 'echarts';
import { bocMauChuDe } from './hex-token.mjs';

/** Ket noi { optionFn, params, kichThuoc } voi mot phien ECharts SSR ngan han:
 *   1. echarts.init(ssr:true, renderer:'svg') dung DUNG kich thuoc yeu cau.
 *   2. Goi optionFn(params) lay OBJECT OPTION thuan.
 *   3. Neu option co truong noi bo `_veSauLayout` (mot ham), goi SAU KHI setOption
 *      lan dau -- day la loi thoat cho cac preset can toa do PIXEL THAT sau khi truc
 *      da layout (vd markLine/graphic ban do theo mot diem du lieu cu the qua
 *      chart.convertToPixel()). `_veSauLayout` KHONG phai mot khoa ECharts, bi tach
 *      ra truoc khi setOption dau tien va khong bao gio lot vao chuoi SVG cuoi.
 *   4. animation:false ghi de LEN TREN CUNG, sau moi buoc khac.
 *   5. renderToSVGString(), dispose(), roi hau xu ly hex sang var(--token, #hex-cu)
 *      qua bocMauChuDe() (xem hex-token.mjs) truoc khi tra ve.
 *
 * @param {(params: object) => object} optionFn thuong la `option` export tu 1 preset
 * @param {object} params du lieu dua vao optionFn (MAC_DINH cua preset, hoac du lieu
 *   that cua bao cao dung dung hinh dang MAC_DINH mong doi)
 * @param {{width: number, height: number}} opts kich thuoc canvas SSR tinh bang px
 * @returns {string} chuoi SVG da hau xu ly, san sang ghi ra file hoac nhung vao PDF
 */
export function renderStatic(optionFn, params, { width, height }) {
  const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width, height });
  const optTho = optionFn(params);
  const { _veSauLayout: veSauLayout, ...opt } = optTho;
  chart.setOption({ ...opt, animation: false });
  if (typeof veSauLayout === 'function') {
    chart.setOption({ graphic: veSauLayout(chart) });
  }
  const svgTho = chart.renderToSVGString();
  chart.dispose();
  return bocMauChuDe(svgTho);
}
