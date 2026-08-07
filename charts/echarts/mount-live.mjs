// mount-live.mjs, duong mount CHUNG cho lan `html-song`: option() thuan -> instance
// ECharts SONG trong DOM cua trinh duyet.
//
// Khac render-static.mjs o hai diem, ca hai deu CO CHU Y:
//   - KHONG dat ssr:true / renderer:'svg' rieng: echarts.init(container) tu doc kich
//     thuoc that cua container (clientWidth/clientHeight) va chon renderer canvas mac
//     dinh cua ECharts trong trinh duyet, hop voi mot trang tu du co JavaScript luc
//     chay, KHAC ban tinh nhung vao bao cao.
//   - KHONG ep animation:false: lan html-song khong di qua duong SSR xuat CSS
//     @keyframes gay loi keo marker ve goc toa do (xem render-static.mjs), nen duoc
//     giu nguyen animation mac dinh cua ECharts -- day chinh la nang luc lan
//     html-song co ma lan pdf-so khong co.
//   - KHONG hau xu ly mau: chart mount song trong DOM da doc duoc `var(--accent)`
//     v.v. qua getComputedStyle() ngay tu itemStyle.color goc (JS truyen thang gia
//     tri), khong can buoc doi hex sang var() nhu SVG tinh.
import * as echarts from 'echarts';

/** Mount 1 preset SONG vao 1 phan tu DOM.
 *
 * @param {(params: object) => object} optionFn thuong la `option` export tu 1 preset
 * @param {object} params du lieu dua vao optionFn (MAC_DINH cua preset, hoac du lieu
 *   that cua bao cao dung dung hinh dang MAC_DINH mong doi)
 * @param {HTMLElement} container phan tu DOM da co kich thuoc (khong 0x0)
 * @returns {import('echarts').ECharts} instance ECharts, goi .dispose()/.resize() sau
 */
export function mountLive(optionFn, params, container) {
  const chart = echarts.init(container);
  const optTho = optionFn(params);
  const { _veSauLayout: veSauLayout, ...opt } = optTho;
  chart.setOption(opt);
  if (typeof veSauLayout === 'function') {
    chart.setOption({ graphic: veSauLayout(chart) });
  }
  return chart;
}
