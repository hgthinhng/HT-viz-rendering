// mount-live.mjs, duong mount CHUNG cho lan `html-song`: option() thuan -> instance
// ECharts SONG trong DOM cua trinh duyet.
//
// Khac render-static.mjs o ba diem, ca ba deu CO CHU Y:
//   - KHONG dat ssr:true: echarts.init(container) tu doc kich thuoc that cua container
//     (clientWidth/clientHeight), khac ban tinh nhung vao bao cao. Renderer thi CO dat,
//     va la 'svg' chu khong phai canvas mac dinh: ly do day du o `echarts-song.mjs`,
//     tom tat la gate THEME-MATCH quet the <svg> nen chart canvas nam ngoai tam gate.
//   - KHONG ep animation:false: lan html-song khong di qua duong SSR xuat CSS
//     @keyframes gay loi keo marker ve goc toa do (xem render-static.mjs), nen duoc
//     giu nguyen animation mac dinh cua ECharts -- day chinh la nang luc lan
//     html-song co ma lan pdf-so khong co.
//   - KHONG hau xu ly mau: chart mount song trong DOM da doc duoc `var(--accent)`
//     v.v. qua getComputedStyle() ngay tu itemStyle.color goc (JS truyen thang gia
//     tri), khong can buoc doi hex sang var() nhu SVG tinh.
import { echarts } from './echarts-song.mjs';

/** Mount 1 preset SONG vao 1 phan tu DOM.
 *
 * @param {(params: object) => object} optionFn thuong la `option` export tu 1 preset
 * @param {object} params du lieu dua vao optionFn (MAC_DINH cua preset, hoac du lieu
 *   that cua bao cao dung dung hinh dang MAC_DINH mong doi)
 * @param {HTMLElement} container phan tu DOM da co kich thuoc (khong 0x0)
 * @returns {import('echarts').ECharts} instance ECharts, goi .dispose()/.resize() sau
 */
export function mountLive(optionFn, params, container) {
  const chart = echarts.init(container, null, { renderer: 'svg' });
  const optTho = optionFn(params);
  const { _veSauLayout: veSauLayout, ...opt } = optTho;
  chart.setOption(opt);
  if (typeof veSauLayout === 'function') {
    chart.setOption({ graphic: veSauLayout(chart) });
  }
  ganChuDe(container);
  return chart;
}

/** Chep `data-theme` cua trang xuong the <svg> ma ECharts vua sinh.
 *
 * KHONG phai trang tri. Gate `THEME-MATCH` cua lan song doi MOI the <svg> trong DOM tu
 * khai chu de va khai dung chu de cua trang; SVG tinh nhung vao bao cao thi da mang san
 * thuoc tinh do tu luc build, con SVG do ECharts sinh luc chay thi khong ai gan cho no.
 * Thieu mot dong nay la chart song lam ca gate do, va do dung la kieu do that chu khong
 * phai do oan: mot chart mount ra khi trang dang o chu de toi ma khong ai khai gi thi
 * khong co cach nao biet no da doc dung chu de hay chua.
 */
function ganChuDe(container) {
  const chuDe = document.documentElement.getAttribute('data-theme');
  if (!chuDe) return;
  // querySelectorAll chu khong phai querySelector: ECharts voi SVGRenderer dat HAI the
  // <svg> canh nhau trong container (mot cho noi dung, mot cho lop phu tuong tac), va
  // gate THEME-MATCH duyet TUNG the <svg> tren trang chu khong duyet tung chart. Ban
  // dau tien cua ham nay chi gan cho the thu nhat, va gate do dung mot nua so chart.
  container.querySelectorAll('svg').forEach((svg) => svg.setAttribute('data-theme', chuDe));
}
