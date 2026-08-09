// Gate: hai nhan chu trong cung mot SVG khong duoc DE LEN nhau.
//
// Anh em voi `chu_khong_tran_viewbox.test.mjs`, cung lop loi "parse dung nhung nhin
// sai", khac cho bi benh: gate kia do chu so voi KHUNG, gate nay do chu so voi CHU.
//
// Lop loi nay tung can that o mot bo phan khac cua he: nhan su kien tren bieu do TPB
// chi co hai tang, nen nhan thu ba de len nhan thu nhat. Doc tang text thi ca ba nhan
// deu co mat va deu dung chinh ta; nhin thi mot nhan bien thanh mot dong chu chong len
// nhau khong doc noi. Ke ca visual regression cung khong bat duoc neu no chong ngay tu
// anh moc dau tien: gate nay do TUYET DOI chu khong do so voi mot ban truoc.
//
// Vi sao dung sai lai rong den 40%: nhan cua chart co the nam RAT gan nhau mot cach hop
// le (nhan truc lien tiep, nhan gia tri canh cot), va bounding box cua chu bao gio cung
// rong hon net muc that vi no gom ca phan tren duoi cua font. Do dien giao nhau tren
// dien tich hop cua hai box, va chi bao khi giao qua mot phan tu dien tich hinh nho hon:
// duoi nguong do la hai nhan ke sat, tren nguong do la hai nhan de len nhau.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { kiemTraChromium, launchChromium } from '../../scripts/lib/chromium.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const THU_MUC_CHART = path.join(GOC, 'charts/echarts');
const TAM = mkdtempSync(path.join(tmpdir(), 'nhan-chong-'));
const co_chromium = kiemTraChromium().ok;

/** Ty le dien tich giao nhau tren dien tich box NHO HON, tren muc nay thi tinh la chong. */
const NGUONG_GIAO = 0.4;

function trang(svgTho) {
  const svg = svgTho.replace(/<\?xml[^>]*\?>/, '').replace(/<!DOCTYPE[^>]*>/, '');
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{margin:0;padding:0}svg{overflow:visible}</style>
</head><body>${svg}</body></html>`;
}

async function doChong(page, tenFile, svgTho) {
  const f = path.join(TAM, tenFile.replace('.svg', '.html'));
  writeFileSync(f, trang(svgTho), 'utf8');
  await page.goto('file://' + f);
  // ECharts SSR nhung CSS animation chay 1 giay; do som cho ket qua nua chung.
  await page.waitForTimeout(1600);

  return page.evaluate((nguong) => {
    const nhan = [];
    for (const t of document.querySelectorAll('text')) {
      const chu = (t.textContent || '').trim();
      if (!chu) continue;
      const b = t.getBoundingClientRect();
      if (b.width <= 0 || b.height <= 0) continue;
      const cs = getComputedStyle(t);
      if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) < 0.05) continue;
      nhan.push({ chu, x: b.left, y: b.top, r: b.right, d: b.bottom, w: b.width, h: b.height });
    }
    const chong = [];
    for (let i = 0; i < nhan.length; i++) {
      for (let j = i + 1; j < nhan.length; j++) {
        const a = nhan[i];
        const b = nhan[j];
        const gw = Math.min(a.r, b.r) - Math.max(a.x, b.x);
        const gh = Math.min(a.d, b.d) - Math.max(a.y, b.y);
        if (gw <= 0 || gh <= 0) continue;
        const giao = gw * gh;
        const nho = Math.min(a.w * a.h, b.w * b.h);
        const ty = giao / nho;
        if (ty > nguong) {
          chong.push(`"${a.chu.slice(0, 24)}" de len "${b.chu.slice(0, 24)}" (${Math.round(ty * 100)}%)`);
        }
      }
    }
    return { soNhan: nhan.length, chong };
  }, NGUONG_GIAO);
}

const cacFile = readdirSync(THU_MUC_CHART).filter((f) => /^out-\d\d.*\.svg$/.test(f)).sort();

test('khong nhan nao de len nhan khac trong moi SVG preset', { timeout: 180000, skip: !co_chromium && 'chua co Chromium' }, async () => {
  assert.ok(cacFile.length >= 18, `chi thay ${cacFile.length} file out-*.svg, chay npm run verify:charts truoc`);
  const browser = await launchChromium();
  const hong = [];
  try {
    const page = await browser.newPage();
    for (const f of cacFile) {
      const kq = await doChong(page, f, readFileSync(path.join(THU_MUC_CHART, f), 'utf8'));
      for (const c of kq.chong) hong.push(`${f}: ${c}`);
    }
  } finally {
    await browser.close();
  }
  assert.deepEqual(hong, [], `co nhan de len nhau:\n${hong.join('\n')}`);
});

test('gate tu do duoc: mot SVG co hai nhan dat trung cho phai bi bat', { timeout: 60000, skip: !co_chromium && 'chua co Chromium' }, async () => {
  const svgDo = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120" viewBox="0 0 300 120">
<text x="20" y="60" font-size="14" font-family="sans-serif">Bien loi nhuan gop</text>
<text x="24" y="62" font-size="14" font-family="sans-serif">Bien loi nhuan rong</text>
</svg>`;
  const browser = await launchChromium();
  try {
    const page = await browser.newPage();
    const kq = await doChong(page, 'fixture-do.svg', svgDo);
    assert.ok(kq.chong.length > 0, 'gate khong bat duoc hai nhan dat gan nhu trung cho');
  } finally {
    await browser.close();
  }
});

test('gate khong do oan: hai nhan ke sat nhau theo dong van phai xanh', { timeout: 60000, skip: !co_chromium && 'chua co Chromium' }, async () => {
  const svgXanh = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120" viewBox="0 0 300 120">
<text x="20" y="40" font-size="14" font-family="sans-serif">Quy I</text>
<text x="20" y="58" font-size="14" font-family="sans-serif">Quy II</text>
<text x="90" y="40" font-size="14" font-family="sans-serif">1.240</text>
</svg>`;
  const browser = await launchChromium();
  try {
    const page = await browser.newPage();
    const kq = await doChong(page, 'fixture-xanh.svg', svgXanh);
    assert.deepEqual(kq.chong, [], 'gate bao chong voi nhung nhan chi nam ke nhau');
  } finally {
    await browser.close();
  }
});
