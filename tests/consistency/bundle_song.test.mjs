// bundle_song.test.mjs, chong troi giua cua ECharts cua lan `html-song` va thu ma 18
// preset THAT SU dung.
//
// Benh can chan: `echarts-song.mjs` khai tay danh sach module de tree-shaking an tac
// dung. Danh sach khai tay thi troi duoc, va kieu troi cua no la kieu te nhat trong
// repo nay: them mot preset dung `series.type` chua khai thi chart do KHONG ve gi ca,
// khong nem loi, khong canh bao. Giong het lop benh "gate xanh gia" da cat nhieu lan.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { statSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PRESETS } from '../../charts/echarts/registry.mjs';
import { SERIES_DUOC_PHEP } from '../../charts/echarts/echarts-song.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DUONG_BUNDLE = path.join(GOC, 'charts', 'echarts', 'ra-song', 'bundle-song.js');

/** Gom moi `series.type` xuat hien trong option() that cua mot preset. */
function gomSeriesType(opt) {
  const ra = new Set();
  const day = Array.isArray(opt.series) ? opt.series : opt.series ? [opt.series] : [];
  for (const s of day) {
    if (s && typeof s.type === 'string') ra.add(s.type);
  }
  return ra;
}

test('moi series.type cua 18 preset deu nam trong cua ECharts cua lan song', () => {
  const chuaKhai = [];
  for (const [ma, preset] of Object.entries(PRESETS)) {
    const opt = preset.option(preset.MAC_DINH);
    for (const kieu of gomSeriesType(opt)) {
      if (!SERIES_DUOC_PHEP.includes(kieu)) chuaKhai.push(`${ma} dung series.type "${kieu}"`);
    }
  }
  assert.deepEqual(
    chuaKhai,
    [],
    'Co series.type khong duoc dang ky trong echarts-song.mjs. Chart do se KHONG VE GI ' +
      'trong an pham lan html-song ma khong bao loi. Them Chart tuong ung vao echarts-song.mjs:\n' +
      chuaKhai.join('\n'),
  );
});

test('moi loai trong SERIES_DUOC_PHEP deu co preset dung toi, khong khai thua', () => {
  const dangDung = new Set();
  for (const preset of Object.values(PRESETS)) {
    for (const kieu of gomSeriesType(preset.option(preset.MAC_DINH))) dangDung.add(kieu);
  }
  const thua = SERIES_DUOC_PHEP.filter((k) => !dangDung.has(k));
  assert.deepEqual(
    thua,
    [],
    `SERIES_DUOC_PHEP khai thua ${thua.join(', ')}: khong preset nao dung, nen module tuong ung ` +
      'chi lam nang bundle. Bo khoi echarts-song.mjs, hoac them preset dung toi.',
  );
});

test('bundle da dung, va nhe hon HAN ban ECharts day du', () => {
  let st;
  try {
    st = statSync(DUONG_BUNDLE);
  } catch {
    assert.fail(`Chua co ${DUONG_BUNDLE}. Chay: npm run bundle:song`);
  }
  const day_du = statSync(path.join(GOC, 'node_modules', 'echarts', 'dist', 'echarts.min.js')).size;
  assert.ok(
    st.size < day_du * 0.85,
    `bundle-song.js ${(st.size / 1024).toFixed(1)}KB khong nhe hon 85% ban day du ` +
      `${(day_du / 1024).toFixed(1)}KB. Tree-shaking dang khong an: nhieu kha nang mot module ` +
      "vua import 'echarts' thay vi './echarts-song.mjs'.",
  );
});

test('bundle khong keo render-static, tuc khong keo ca goi ECharts qua duong CLI', () => {
  const js = readFileSync(DUONG_BUNDLE, 'utf8');
  // renderStatic() dat `ssr: true`, chuoi nay chi co trong render-static.mjs. Neu no
  // xuat hien trong bundle thi module do da bi keo vao, va keo theo ca `echarts` day du.
  assert.ok(
    !js.includes('ssr:!0') && !js.includes('ssr: true'),
    'bundle-song.js co dau vet render-static.mjs. Kiem lai `external` trong ' +
      'scripts/build-bundle-song.mjs: import DONG van bi esbuild keo vao neu khong external.',
  );
});
