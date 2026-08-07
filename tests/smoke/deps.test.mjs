import { test } from 'node:test';
import assert from 'node:assert/strict';

const REQUIRED = [
  'playwright-core',
  'echarts',
  'd3-geo',
  'topojson-client',
  'topojson-simplify',
];

for (const pkg of REQUIRED) {
  test(`import duoc goi ${pkg}`, async () => {
    const mod = await import(pkg);
    assert.ok(mod, `${pkg} import ve undefined`);
  });
}

test('Chromium cache ton tai va chay duoc', async () => {
  // Truoc: hardcode "chromium-1228". Tren may sach thi ENOENT, va tren may
  // nay thi no chay ban KHAC voi verify-components.mjs. Gio ca ba cho cung
  // hoi scripts/lib/chromium.mjs, tuc cung hoi playwright-core.
  const { kiemTraChromium, launchChromium } = await import('../../scripts/lib/chromium.mjs');
  const kiem = kiemTraChromium();
  assert.ok(kiem.ok, kiem.message);
  const browser = await launchChromium();
  const version = browser.version();
  await browser.close();
  assert.match(version, /^\d+\./, `version bat thuong: ${version}`);
});

test('moi cho mo Chromium deu di qua scripts/lib/chromium.mjs', async () => {
  // Gate chong tai pham: cam hardcode lai duong dan cache, va cam goi
  // chromium.launch() truc tiep trong scripts/ va tests/. Neu khong co gate
  // nay thi lan sau ai do them mot script verify moi lai copy nguyen doan
  // duong dan cu, va repo lai co hai binary nhu truoc.
  const { readdirSync, readFileSync, statSync } = await import('node:fs');
  const { fileURLToPath } = await import('node:url');
  const path = (await import('node:path')).default;
  const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

  const quet = (dir, acc = []) => {
    for (const ten of readdirSync(dir)) {
      if (ten === 'node_modules' || ten === '__pycache__') continue;
      const p = path.join(dir, ten);
      if (statSync(p).isDirectory()) quet(p, acc);
      else if (ten.endsWith('.mjs') || ten.endsWith('.js')) acc.push(p);
    }
    return acc;
  };

  const files = [...quet(path.join(ROOT, 'scripts')), ...quet(path.join(ROOT, 'tests'))].filter(
    (p) => !p.endsWith(path.join('lib', 'chromium.mjs')),
  );

  // Hai mau CAM duoc GHEP LUC CHAY chu khong viet lien trong nguon. Ly do rat
  // cu the: ban dau chung viet lien, va gate nay FAIL ngay tren chinh file
  // dang chua no, vi ban than dong regex la mot chuoi khop. Ghep luc chay giu
  // duoc quet CA file nay (khong phai mien tru chinh minh, vi mien tru thi
  // file gate thanh vung mu) ma khong tu to cao.
  const CAM = [
    { re: new RegExp(['ms', 'playwright'].join('-')), moTa: 'hardcode duong dan cache Chromium' },
    { re: new RegExp('chromium' + '\\.launch\\s*\\('), moTa: 'goi launch() truc tiep thay vi launchChromium()' },
  ];

  const viPham = [];
  for (const f of files) {
    const src = readFileSync(f, 'utf8');
    // Bo dong comment truoc khi quet, vi chinh cac file nay co comment KE LAI
    // duong dan cu de giai thich bug. Ke lai thi duoc, dung that thi khong.
    const code = src
      .split('\n')
      .filter((l) => !/^\s*(\/\/|\*|\/\*)/.test(l))
      .join('\n');
    for (const { re, moTa } of CAM) {
      if (re.test(code)) viPham.push(`${path.relative(ROOT, f)}: ${moTa}`);
    }
  }
  assert.deepEqual(viPham, [], `phai dung launchChromium() tu scripts/lib/chromium.mjs:\n${viPham.join('\n')}`);
});
