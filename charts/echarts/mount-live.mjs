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
import { PALETTE } from './theme.mjs';
import { TOKEN_CSS } from './hex-token.mjs';

/** Mount 1 preset SONG vao 1 phan tu DOM.
 *
 * @param {(params: object) => object} optionFn thuong la `option` export tu 1 preset
 * @param {object} params du lieu dua vao optionFn (MAC_DINH cua preset, hoac du lieu
 *   that cua bao cao dung dung hinh dang MAC_DINH mong doi)
 * @param {HTMLElement} container phan tu DOM da co kich thuoc (khong 0x0)
 * @returns {import('echarts').ECharts} instance ECharts, goi .dispose()/.resize() sau
 */
/** Doi moi hex THUOC bang mau sang gia tri THAT cua bien CSS tuong ung.
 *
 * SVG tinh giai quyet chuyen chu de bang cach boc hex thanh `var(--token, #hex-cu)`, va
 * trinh duyet lo phan con lai. Chart SONG khong dung duong do: ECharts nhan mau qua
 * JavaScript va ve thang, nen mot chart mount tren trang chu de toi van ra nen trang.
 * Do duoc tren an pham that: nen trang doi sang mau nen cua chu de toi ma nen chart van
 * giu mau giay cua chu de sang, dung benh kinh dien "chart trang tren nen toi" ma gate
 * THEME-MATCH sinh ra de bat. Ghi bang TEN token chu khong bang hex: test chart_theme
 * cam moi gia tri mau tran trong file chart, ke ca trong chu thich.
 *
 * Doc gia tri bang getComputedStyle tren CHINH container, khong doc tren `:root`: mot
 * khoi co the nam trong vung khai chu de rieng, va luc do gia tri o goc tai lieu la sai.
 */
function doiMauTheoChuDe(nut, cs, tra) {
  if (Array.isArray(nut)) return nut.map((x) => doiMauTheoChuDe(x, cs, tra));
  if (nut && typeof nut === 'object') {
    const ra = {};
    for (const [k, v] of Object.entries(nut)) ra[k] = doiMauTheoChuDe(v, cs, tra);
    return ra;
  }
  if (typeof nut === 'string') {
    const bien = tra.get(nut.toUpperCase());
    if (!bien) return nut;
    const gt = cs.getPropertyValue(bien).trim();
    return gt || nut;
  }
  return nut;
}

/** Bang tra hex sang ten bien CSS, dung chung mot nguon voi duong SVG tinh. */
function bangTra() {
  const m = new Map();
  for (const [khoa, bien] of Object.entries(TOKEN_CSS)) {
    const hex = PALETTE[khoa];
    if (hex) m.set(String(hex).toUpperCase(), bien);
  }
  return m;
}

export function mountLive(optionFn, params, container) {
  const chart = echarts.init(container, null, { renderer: 'svg' });
  const optTho = optionFn(params);
  const { _veSauLayout: veSauLayout, ...optGoc } = optTho;
  const cs = getComputedStyle(container);
  const tra = bangTra();
  const opt = doiMauTheoChuDe(optGoc, cs, tra);
  chart.setOption(opt);
  if (typeof veSauLayout === 'function') {
    // Ket qua cua `_veSauLayout` cung phai qua phep doi mau. No chay SAU setOption dau
    // tien nen no khong nam trong `optGoc`, va do la ly do bon nhan cua `13-line-annotated`
    // van giu mau chu de sang trong khi ca phan con lai cua chart da doi.
    chart.setOption({ graphic: doiMauTheoChuDe(veSauLayout(chart), cs, tra) });
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
