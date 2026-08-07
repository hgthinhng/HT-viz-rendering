// Gate: khong the <text> nao duoc tran ra ngoai viewBox cua chinh SVG do.
//
// VI SAO CAN GATE NAY, va vi sao khong gate cu nao thay duoc no:
//
// Ngay 08-08 phat hien `out-02-sankey.svg` cat cut hai nhan ben phai, "Chi phi
// ban hang & QLDN" thanh "... & Ql". Le phai cua grid khai 140px trong khi nhan
// dai nhat can 157px, nen chu tran ra ngoai viewBox 760px roi bi khung SVG cat
// khi nhung vao HTML hoac render sang PDF.
//
// Bug do song duoc vi MOI gate hien co deu xanh voi no:
//   - dem net ve: dung, chu van duoc ve ra, chi la ve ra ngoai khung
//   - parse XML: hop le, khong co gi sai cu phap
//   - gate 5 CHART-SONG: kiem chu cua SVG co mat trong tang text cua PDF, va chu
//     CO mat that. Tang text khong biet gi ve khung nhin
//   - soi anh bang mat: chi thay khi doc DUNG cai nhan bi cat, ma nhan bi cat
//     trong van giong mot nhan ngan binh thuong
//
// Day la mot bien the nua cua bai hoc "mot gate DEM khong thay duoc mot gate
// PARSE", lan nay la "mot gate doc TANG TEXT khong thay duoc mot gate do HINH
// HOC". Chu co mat khong co nghia la chu doc duoc.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { launchChromium } from '../../scripts/lib/chromium.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const THU_MUC_CHART = path.join(GOC, 'charts/echarts');
const TAM = mkdtempSync(path.join(tmpdir(), 'tran-viewbox-'));

// Dung sai 1px: getBoundingClientRect tra so thuc, va vien chu chong rang co the
// lem duoi mot pixel ma mat khong thay. Tren 1px thi la tran that.
const DUNG_SAI = 1;

function trang(svgTho) {
  const svg = svgTho.replace(/<\?xml[^>]*\?>/, '').replace(/<!DOCTYPE[^>]*>/, '');
  // overflow:visible la CO Y: phai cho chu tran ra de DO duoc no. Neu de mac dinh
  // thi trinh duyet cat chu ngay, va phep do se bao moi thu vua khit trong khi
  // thuc te dang mat chu. Do la dung bay ma gate nay sinh ra de tranh.
  return `<!DOCTYPE html><html><head><meta charset="utf-8">
<style>html,body{margin:0;padding:0}svg{overflow:visible}</style>
</head><body>${svg}</body></html>`;
}

async function doTran(page, tenFile, svgTho) {
  const khop = svgTho.match(/viewBox="([\d.\s-]+)"/);
  if (!khop) return { boQua: true, ly_do: 'khong khai viewBox' };
  const [, , rong, cao] = khop[1].trim().split(/\s+/).map(Number);

  const f = path.join(TAM, tenFile.replace('.svg', '.html'));
  writeFileSync(f, trang(svgTho), 'utf8');
  await page.goto('file://' + f);
  // Cho 1600ms: ECharts SSR nhung CSS animation chay 1 giay. Chup hoac do som
  // hon cho ket qua nua chung, bay da ghi trong CLAUDE.md.
  await page.waitForTimeout(1600);

  return page.evaluate(
    ({ rong, cao, dungSai }) => {
      const tran = [];
      for (const t of document.querySelectorAll('text')) {
        const chu = (t.textContent || '').trim();
        if (!chu) continue;
        const b = t.getBoundingClientRect();
        const vuot = [];
        if (b.right > rong + dungSai) vuot.push(`phai +${Math.round(b.right - rong)}px`);
        if (b.bottom > cao + dungSai) vuot.push(`duoi +${Math.round(b.bottom - cao)}px`);
        if (b.left < -dungSai) vuot.push(`trai ${Math.round(b.left)}px`);
        if (b.top < -dungSai) vuot.push(`tren ${Math.round(b.top)}px`);
        if (vuot.length) tran.push(`"${chu.slice(0, 32)}" ${vuot.join(', ')}`);
      }
      return { boQua: false, tran };
    },
    { rong, cao, dungSai: DUNG_SAI },
  );
}

const cacFile = readdirSync(THU_MUC_CHART).filter((f) => /^out-\d\d.*\.svg$/.test(f)).sort();

test('moi chart ECharts: khong chu nao tran ra ngoai viewBox', async () => {
  assert.ok(cacFile.length > 0, 'khong tim thay out-*.svg nao, chay npm run verify truoc');

  const trinhDuyet = await launchChromium();
  const ctx = await trinhDuyet.newContext({ viewport: { width: 1600, height: 900 } });
  const page = await ctx.newPage();
  const hong = [];
  try {
    for (const f of cacFile) {
      const kq = await doTran(page, f, readFileSync(path.join(THU_MUC_CHART, f), 'utf8'));
      if (!kq.boQua && kq.tran.length) hong.push(`${f}: ${kq.tran.join(' | ')}`);
    }
  } finally {
    await trinhDuyet.close();
  }
  assert.equal(hong.length, 0, `chu bi cat cut o ${hong.length} chart:\n  ${hong.join('\n  ')}`);
});

test('gate tu DO DUOC: SVG co chu dat ngoai viewBox phai bi bat', async () => {
  // Fixture do dung ngay trong test, khong de file rieng, vi no chi la mot chuoi
  // va viec de no canh dinh nghia lam ro gate dang bat cai gi.
  const svgDo = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
<rect x="0" y="0" width="200" height="100" fill="#FFFFFF"/>
<text x="150" y="50" font-size="14" font-family="sans-serif">Nhan nay dai qua khung</text>
</svg>`;
  const svgXanh = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
<rect x="0" y="0" width="200" height="100" fill="#FFFFFF"/>
<text x="10" y="50" font-size="14" font-family="sans-serif">Vua khung</text>
</svg>`;

  const trinhDuyet = await launchChromium();
  const ctx = await trinhDuyet.newContext({ viewport: { width: 1600, height: 900 } });
  const page = await ctx.newPage();
  try {
    const ketDo = await doTran(page, 'fixture-do.svg', svgDo);
    const ketXanh = await doTran(page, 'fixture-xanh.svg', svgXanh);
    assert.ok(ketDo.tran.length > 0, 'fixture DO phai bi bat, nhung gate cho qua');
    assert.match(ketDo.tran[0], /phai \+\d+px/, 'phai bao ro tran ve huong nao va bao nhieu px');
    assert.equal(ketXanh.tran.length, 0, `fixture XANH phai qua, nhung bi bat: ${ketXanh.tran}`);
  } finally {
    await trinhDuyet.close();
  }
});
