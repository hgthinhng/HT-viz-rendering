// mount_song.test.mjs, phep do DIEU KIEN DU cho lan `html-song`: mount ca 18 preset
// bang Chromium that roi dem net ve trong DOM.
//
// Vi sao khong du neu chi co bundle_song.test.mjs: nhung test kia doc ma nguon va doc
// kich thuoc file, deu la dieu kien CAN. Repo nay da tra gia dung mot lan cho kieu
// nghiem thu do: 12 chart xuat SVG khong hop le XML, moi phep dem chuoi va dem phan tu
// deu xanh, va ban PDF mat sach chart suot mot phase. Chi co mo that ra moi biet.
//
// Ba thu duoc do, va moi thu chan mot benh khac nhau:
//   - `netVe > 0`   chart co ve that, khong phai mount xong ra khung rong.
//   - `data-theme`  chart song nam trong tam gate THEME-MATCH (xem mount-live.mjs).
//   - `animation`   duong song KHONG bi ep tat. Day la nang luc rieng cua lan nay so
//                   voi lan `pdf-so`, va no de mat am tham vi `baseOption()` dung chung
//                   cho ca hai lan von khai `animation: false`.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { kiemTraChromium, launchChromium } from '../../scripts/lib/chromium.mjs';
import { PRESETS } from '../../charts/echarts/registry.mjs';
import { dungBundle, DUONG_BUNDLE } from '../../scripts/build-bundle-song.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const MA_PRESET = Object.keys(PRESETS);
const co_chromium = kiemTraChromium().ok;

let browser = null;
let ketQua = null;
let loiTrang = [];

before(async () => {
  if (!co_chromium) return;
  await dungBundle({ im: true });
  const bundle = readFileSync(DUONG_BUNDLE, 'utf8');
  const html = `<!doctype html>
<html lang="vi" data-theme="light"><head><meta charset="utf-8"><title>mount song</title>
<style>body{background:#fff;margin:0}.o{width:680px;height:380px}</style></head><body>
${MA_PRESET.map((m) => `<div class="o" data-preset="${m}"></div>`).join('\n')}
<script type="module">
${bundle}
window.__kq = [];
for (const el of document.querySelectorAll('[data-preset]')) {
  try {
    const c = window.HTViz.mount(el.dataset.preset, null, el);
    const svg = el.querySelector('svg');
    window.__kq.push({
      ma: el.dataset.preset,
      netVe: svg ? svg.querySelectorAll('path,rect,circle,polyline,polygon,line').length : 0,
      chuDe: svg ? svg.getAttribute('data-theme') : null,
      animation: c.getOption().animation,
    });
  } catch (e) { window.__kq.push({ ma: el.dataset.preset, loi: e.message }); }
}
window.__xong = true;
</script></body></html>`;
  const thuMuc = mkdtempSync(path.join(os.tmpdir(), 'htviz-song-'));
  const duong = path.join(thuMuc, 'mount.html');
  writeFileSync(duong, html);

  browser = await launchChromium();
  const page = await browser.newPage();
  page.on('pageerror', (e) => loiTrang.push(String(e)));
  await page.goto(`file://${duong}`);
  await page.waitForFunction('window.__xong === true', { timeout: 30000 });
  ketQua = await page.evaluate('window.__kq');
});

after(async () => { if (browser) await browser.close(); });

test('ca 18 preset mount song duoc va ve ra net that', { skip: !co_chromium && 'chua co Chromium, chay npm run setup:browser' }, () => {
  assert.equal(loiTrang.length, 0, `trang nem loi: ${loiTrang.slice(0, 3).join(' | ')}`);
  const hong = ketQua.filter((r) => r.loi || !(r.netVe > 0));
  assert.deepEqual(
    hong.map((r) => `${r.ma}: ${r.loi || 'khong co net ve'}`),
    [],
    'co preset khong mount song duoc',
  );
  assert.equal(ketQua.length, MA_PRESET.length);
});

test('chart song tu khai data-theme nen gate THEME-MATCH khong mu', { skip: !co_chromium && 'chua co Chromium' }, () => {
  const thieu = ketQua.filter((r) => r.chuDe !== 'light').map((r) => r.ma);
  assert.deepEqual(thieu, [], 'co chart song khong mang data-theme, gate THEME-MATCH se do oan');
});

test('duong song KHONG bi ep tat animation', { skip: !co_chromium && 'chua co Chromium' }, () => {
  const bi_tat = ketQua.filter((r) => r.animation === false).map((r) => r.ma);
  assert.deepEqual(
    bi_tat,
    [],
    'animation bi ep false: lan html-song mat dung nang luc phan biet no voi lan pdf-so',
  );
});
