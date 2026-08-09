// song-entry.mjs, diem vao DUY NHAT cua bundle lan `html-song`.
//
// File nay khong chua logic. No chi gom ba thu ma mot trang an pham can va dat len
// `window.HTViz`, de trang chi phai goi mot ham chu khong phai biet gi ve cach preset
// duoc to chuc:
//
//   HTViz.mount('13-line-annotated', duLieu, document.getElementById('hinh-x'))
//
// Trang tu du KHONG dung `<script type="module">`: mot trang mo bang `file://` khong
// fetch duoc module anh em, va an pham nay phai mo duoc bang cach nhay chuot hai lan
// vao file. Nen bundle xuat dinh dang IIFE gan vao mot bien toan cuc.
import { mountLive } from './mount-live.mjs';
import { PRESETS } from './registry.mjs';
import { echarts, SERIES_DUOC_PHEP } from './echarts-song.mjs';

/** Mount 1 preset theo MA preset, vd '01-waterfall'.
 *
 * Nem loi voi ma khong co that thay vi im lang tra ve undefined: mot chart thieu trong
 * ban bao cao da gui di thi khong goi lai duoc, con mot loi trong console lam nguoi
 * dung thay ngay luc dung thu.
 */
function mount(maPreset, duLieu, container) {
  const preset = PRESETS[maPreset];
  if (!preset) {
    throw new Error(
      `HTViz.mount: khong co preset "${maPreset}". Co san: ${Object.keys(PRESETS).join(', ')}`,
    );
  }
  if (!container) throw new Error(`HTViz.mount: thieu container cho preset "${maPreset}"`);
  return mountLive(preset.option, duLieu || preset.MAC_DINH, container);
}

/** Mount moi phan tu [data-preset] tren trang, va tu resize theo cua so.
 *
 * Du lieu doc tu the <script type="application/json"> dat NGAY BEN TRONG container, nen
 * du lieu cua tung hinh nam canh chinh hinh do trong ma nguon trang thay vi gom thanh
 * mot khoi roi o dau trang. Khong co the do thi dung MAC_DINH cua preset.
 */
function mountTatCa(goc) {
  const root = goc || document;
  const daMount = [];
  root.querySelectorAll('[data-preset]').forEach((el) => {
    const the = el.querySelector('script[type="application/json"]');
    let duLieu = null;
    if (the) {
      try {
        duLieu = JSON.parse(the.textContent);
      } catch (e) {
        throw new Error(`HTViz: du lieu JSON hong o "${el.id || el.dataset.preset}": ${e.message}`);
      }
    }
    daMount.push(mount(el.dataset.preset, duLieu, el));
  });
  let hen = null;
  window.addEventListener('resize', () => {
    clearTimeout(hen);
    hen = setTimeout(() => daMount.forEach((c) => c.resize()), 120);
  });
  return daMount;
}

const HTViz = { mount, mountTatCa, PRESETS, echarts, SERIES_DUOC_PHEP };
if (typeof window !== 'undefined') window.HTViz = HTViz;

export default HTViz;
