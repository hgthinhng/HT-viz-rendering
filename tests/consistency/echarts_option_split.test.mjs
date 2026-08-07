import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DIR_ECHARTS = path.join(ROOT, 'charts/echarts');

// Xac nhan ca 18 preset ECharts da tach option() khoi duong xuat (render-static.mjs cho
// lan pdf-so, mount-live.mjs cho lan html-song): moi preset phai export duoc `option`
// (ham) va `MAC_DINH` (object du lieu demo), va `option(MAC_DINH)` phai tra ve mot OBJECT
// OPTION hop le, khong throw. Day la dieu kien CAN de MOT nguon preset phuc vu duoc ca
// hai lan xuat ban -- neu mot preset con giu option/render dinh lien nhau thi khong the
// import option() rieng roi tai su dung cho ca renderStatic() lan mountLive().

function tenPreset() {
  return readdirSync(DIR_ECHARTS)
    .filter((f) => /^\d\d-.*\.mjs$/.test(f))
    .map((f) => f.replace('.mjs', ''))
    .sort();
}

test('quet dia ra dung 18 preset ECharts (NN-ten.mjs)', () => {
  const ds = tenPreset();
  assert.equal(ds.length, 18, `mong doi 18 preset, thay ${ds.length}: ${ds.join(', ')}`);
});

test('registry.mjs co dung 18 muc, khop 1-1 voi file tren dia', async () => {
  const { PRESETS } = await import(path.join(DIR_ECHARTS, 'registry.mjs'));
  const dsDia = tenPreset();
  const dsRegistry = Object.keys(PRESETS).sort();
  assert.deepEqual(dsRegistry, dsDia, 'registry.mjs PRESETS phai khop CHINH XAC danh sach file tren dia, khong thua khong thieu');
});

for (const ten of tenPreset()) {
  test(`${ten}: export duoc option() va MAC_DINH, option(MAC_DINH) hop le`, async () => {
    const mod = await import(path.join(DIR_ECHARTS, `${ten}.mjs`));

    assert.equal(typeof mod.option, 'function', `${ten}.mjs phai export function option(params)`);
    assert.equal(typeof mod.MAC_DINH, 'object', `${ten}.mjs phai export object MAC_DINH`);
    assert.ok(mod.MAC_DINH !== null, `${ten}.mjs: MAC_DINH khong duoc null`);

    let opt;
    assert.doesNotThrow(() => {
      opt = mod.option(mod.MAC_DINH);
    }, `${ten}.mjs: option(MAC_DINH) khong duoc throw voi chinh du lieu demo cua no`);

    assert.equal(typeof opt, 'object', `${ten}.mjs: option(MAC_DINH) phai tra ve mot object`);
    assert.ok(opt !== null, `${ten}.mjs: option(MAC_DINH) khong duoc tra ve null`);
    assert.ok('series' in opt, `${ten}.mjs: option tra ve phai co truong series (dac trung mot ECharts option)`);

    // Cot loi cua ban tach: option() KHONG con duoc tu khai animation. Viec do chuyen
    // han sang renderStatic()/mountLive() (xem charts/echarts/render-static.mjs). Neu
    // mot preset con tu set animation trong option cua no thi kien truc tach da vo,
    // vi renderStatic() se ghi de animation:false LEN TREN option nay du sao (an toan
    // cho lan pdf-so), nhung lan html-song (mountLive khong ghi de) se lo ra preset
    // nao lo tu khai animation:false, khoa cung mat kha nang co dong cua rieng preset
    // do o lan html-song.
    assert.equal(opt.animation, undefined, `${ten}.mjs: option() khong duoc tu khai 'animation', viec do thuoc renderStatic()/mountLive()`);
  });
}

test('cac preset dung co che _veSauLayout (13, 17, 18) phai export mot ham that trong option, khong phai gia tri khac', async () => {
  const canPostLayout = ['13-line-annotated', '17-football-field', '18-sensitivity-grid'];
  for (const ten of canPostLayout) {
    const mod = await import(path.join(DIR_ECHARTS, `${ten}.mjs`));
    const opt = mod.option(mod.MAC_DINH);
    assert.equal(typeof opt._veSauLayout, 'function', `${ten}.mjs: option() phai co _veSauLayout la function (can toa do pixel that sau khi truc da layout)`);
  }
});
