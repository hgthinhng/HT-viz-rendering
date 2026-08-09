#!/usr/bin/env node
// sinh-svg-preset.mjs, sinh SVG TINH tu mot preset cong mot file du lieu JSON.
//
// Day la nua con lai cua directive `chart-song`. Trang an pham mang HAI ban cua cung
// mot hinh: ban tinh nay nhung san trong HTML, va ban song do bundle mount de len khi
// JavaScript chay. Ca hai deu di qua `option()` cua CUNG preset voi CUNG file du lieu,
// nen chung khong the lech so. Neu dung hai nguon du lieu roi thi day chinh la cho hai
// ban bat dau noi hai dieu khac nhau ma khong ai biet.
//
//   node scripts/sinh-svg-preset.mjs --preset=13-line-annotated \
//        --du-lieu=examples/x/hinh/du-lieu-13.json --ra=examples/x/hinh/ra-13.svg \
//        [--rong=680] [--cao=380]
import { readFileSync, writeFileSync } from 'node:fs';
import { PRESETS } from '../charts/echarts/registry.mjs';
import { renderStatic } from '../charts/echarts/render-static.mjs';

function doc_co(ten, mac_dinh = null) {
  const m = process.argv.find((a) => a.startsWith(`--${ten}=`));
  return m ? m.slice(ten.length + 3) : mac_dinh;
}

const maPreset = doc_co('preset');
const duongDuLieu = doc_co('du-lieu');
const duongRa = doc_co('ra');
const rong = Number(doc_co('rong', '680'));
const cao = Number(doc_co('cao', '380'));

if (!maPreset || !duongRa) {
  console.error('Thieu --preset hoac --ra. Xem chu thich dau file.');
  process.exit(2);
}
const preset = PRESETS[maPreset];
if (!preset) {
  console.error(`Khong co preset "${maPreset}". Co san: ${Object.keys(PRESETS).join(', ')}`);
  process.exit(2);
}

const duLieu = duongDuLieu ? JSON.parse(readFileSync(duongDuLieu, 'utf8')) : preset.MAC_DINH;
const svg = doc_co('qua-trinh-duyet') === 'khong'
  ? renderStatic(preset.option, duLieu, { width: rong, height: cao })
  : await renderQuaTrinhDuyet();
writeFileSync(duongRa, svg);
console.log(`${duongRa}: ${svg.length} bytes tu preset ${maPreset}`);
process.exit(0);

/** Render bang chinh Chromium thay vi SSR tren Node, roi trich the <svg> ra.
 *
 * Cham hon SSR khoang mot giay, va van doi mot giay do. Ly do la mot phep do:
 * ECharts chon SO KHOANG CHIA cua truc theo BE RONG CHU cua nhan, ma Node do chu
 * bang bang so uoc luong con trinh duyet do bang font that. Cung mot du lieu, cung
 * mot khung 624x400, ban SSR ra nhan lon nhat 5.000.000 con ban trinh duyet ra
 * 6.000.000. Hai ban cua CUNG mot hinh tren CUNG mot trang hien hai con so khac
 * nhau tuy vao JavaScript co chay hay khong, va gate 7 NO-JS-CONTENT bat dung cai
 * do. Render ca hai bang cung mot engine thi khong con cho nao de lech.
 */
async function renderQuaTrinhDuyet() {
  const { launchChromium } = await import('../scripts/lib/chromium.mjs');
  const { dungBundle, DUONG_BUNDLE } = await import('./build-bundle-song.mjs');
  await dungBundle({ im: true });
  const bundle = readFileSync(DUONG_BUNDLE, 'utf8');
  const trang = `<!doctype html><html lang="vi" data-theme="light"><head><meta charset="utf-8">
<style>html,body{margin:0;background:#fff}#k{width:${rong}px;height:${cao}px}</style></head>
<body><div id="k"></div><script type="module">
${bundle}
// Ten bien phai HIEM: doan nay nam CHUNG scope module voi ca bundle da gop, nen mot
// cai ten thuong nhu \`el\` dung ngay voi bien top-level cua bundle va ca module chet
// bang SyntaxError truoc khi chay dong nao.
window.HTViz.mount(
  ${JSON.stringify(maPreset)},
  ${JSON.stringify(duLieu)},
  document.getElementById('k'),
);
window.__xong = true;
</script></body></html>`;

  const { mkdtempSync } = await import('node:fs');
  const os = await import('node:os');
  const path = await import('node:path');
  const thuMuc = mkdtempSync(path.join(os.tmpdir(), 'htviz-svg-'));
  const duongTam = path.join(thuMuc, 'render.html');
  writeFileSync(duongTam, trang);

  const browser = await launchChromium();
  try {
    const page = await browser.newPage({ viewport: { width: rong + 40, height: cao + 40 } });
    const loi = [];
    page.on('pageerror', (e) => {
      loi.push(String(e));
      console.error(`  loi trang render: ${String(e).slice(0, 300)}`);
    });
    page.on('console', (m) => {
      if (m.type() === 'error') console.error(`  console.error: ${m.text().slice(0, 300)}`);
    });
    await page.goto(`file://${duongTam}`);
    await page.waitForFunction('window.__xong === true', { timeout: 30000 });
    // Cho animation chay xong roi moi dong bang. Chup som thi duong line ra dut doan,
    // mot cai bay da ton cong truy mot lan (xem CLAUDE.md muc soi anh chart).
    await page.waitForTimeout(1600);
    if (loi.length) throw new Error(`trang render nem loi: ${loi[0]}`);
    const ra = await page.evaluate(() => {
      const svg = document.querySelector('#k svg');
      if (!svg) throw new Error('khong thay the <svg> sau khi mount');
      return svg.outerHTML;
    });
    // ECharts khong ghi xmlns vao the <svg> khi no song trong DOM HTML, vi HTML parser
    // khong doi. Nhung file .svg roi thi PHAI co, va gate 5 CHART-SONG parse XML that.
    return ra.includes('xmlns=')
      ? ra
      : ra.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"');
  } finally {
    await browser.close();
  }
}
