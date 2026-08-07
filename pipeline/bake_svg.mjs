#!/usr/bin/env node
/**
 * bake_svg.mjs, dong bang minh hoa co callout thanh SVG tinh.
 *
 * VI SAO CAN BUOC NAY. `annotate.js` ve callout bang JavaScript luc chay:
 * cham neo, duong dan, hop nhan deu do `createElementNS` sinh ra sau khi trang
 * tai xong. Trinh duyet chay JS nen ban HTML dep. WeasyPrint KHONG chay JS, nen
 * ban PDF mat sach callout ma khong bao loi gi.
 *
 * Da do that trong Phase 2, tren `example-vertical-axis-ship.html`:
 *   ban goc qua WeasyPrint  -> 42 net ve, 197 ky tu text, 0 tren 7 callout
 *   ban bake qua WeasyPrint -> callout nam trong tang text, dem duoc bang so
 *
 * Day la bug lop thu tu cung ho voi ba lop da biet trong repo: trinh duyet
 * dung, engine dich hong, khong ai biet cho toi luc mo PDF ra nhin.
 *
 * Bake lam ba viec, khong lam gi hon:
 *   1. Cho annotate chay xong roi lay nguyen cay SVG.
 *   2. Resolve `var()` va `color-mix()` thanh mau that. WeasyPrint 69 khong
 *      render `color-mix()` (ra 0 fill) va khong thay bien CSS cua trang cha
 *      khi SVG duoc nhung nhu file roi.
 *   3. Ghim `font-family` da resolve cho moi node chu, doi nhay kep sang nhay
 *      DON. Nhay kep long trong thuoc tinh la dung cai lam 12 chart ECharts
 *      thanh XML khong hop le suot Phase 1.
 *
 * Usage:
 *   node pipeline/bake_svg.mjs <input.html> <output.svg> [--selector=svg] [--cho=1500]
 */
import fs from 'node:fs';
import path from 'node:path';
import { launchChromium } from '../scripts/lib/chromium.mjs';
import { kiemTraXml } from '../gates/lib/xml.mjs';

const args = process.argv.slice(2);
const positional = args.filter((a) => !a.startsWith('--'));
const [inFile, outFile] = positional;
const selector = (args.find((a) => a.startsWith('--selector=')) || '--selector=svg').split('=')[1];
// Cho mac dinh 1500ms theo bai hoc da ghi trong CLAUDE.md: chup som hon animation
// lam duong line hien ra dut doan, tao ra loi GIA.
const cho = Number((args.find((a) => a.startsWith('--cho=')) || '--cho=1500').split('=')[1]);

if (!inFile || !outFile) {
  console.error('usage: node pipeline/bake_svg.mjs <input.html> <output.svg> [--selector=svg] [--cho=1500]');
  process.exit(2);
}
if (!fs.existsSync(inFile)) {
  console.error('khong tim thay file nguon:', inFile);
  process.exit(2);
}

/** Chay trong trang: resolve bien CSS roi tra ve SVG da serialize. */
function dongBangTrongTrang(sel) {
  const svg = document.querySelector(sel);
  if (!svg) return { loi: `khong tim thay phan tu khop selector "${sel}"` };

  const CAN_RESOLVE = /var\(|color-mix\(|currentColor/i;
  const THUOC_TINH_MAU = ['fill', 'stroke', 'stop-color', 'flood-color', 'lighting-color'];
  let soMauResolve = 0;
  let soFontGhim = 0;

  const tatCa = [svg, ...svg.querySelectorAll('*')];
  for (const el of tatCa) {
    const cs = getComputedStyle(el);

    for (const ten of THUOC_TINH_MAU) {
      const attr = el.getAttribute(ten);
      const inline = el.style ? el.style.getPropertyValue(ten) : '';
      const khaiBao = inline || attr || '';
      if (!khaiBao || !CAN_RESOLVE.test(khaiBao)) continue;
      // camelCase cho stop-color/flood-color: getPropertyValue nhan ten gach noi
      const thuc = cs.getPropertyValue(ten);
      if (thuc && !CAN_RESOLVE.test(thuc)) {
        el.setAttribute(ten, thuc.trim());
        if (el.style) el.style.removeProperty(ten);
        soMauResolve += 1;
      }
    }

    // Ghim font cho node chu. Doi nhay kep sang nhay DON truoc khi ghi.
    if (el.tagName === 'text' || el.tagName === 'tspan') {
      const dangKhai = el.getAttribute('font-family') || (el.style ? el.style.fontFamily : '');
      const thuc = cs.fontFamily;
      if (thuc && (!dangKhai || CAN_RESOLVE.test(dangKhai))) {
        el.setAttribute('font-family', thuc.replace(/"/g, "'"));
        soFontGhim += 1;
      } else if (dangKhai && dangKhai.includes('"')) {
        el.setAttribute('font-family', dangKhai.replace(/"/g, "'"));
        soFontGhim += 1;
      }
    }
  }

  // XMLSerializer luon ghi xmlns, outerHTML thi khong chac. SVG thieu xmlns la
  // SVG chet khi nhung nhu file roi.
  const chuoi = new XMLSerializer().serializeToString(svg);
  const soText = svg.querySelectorAll('text').length;
  const nhanChu = Array.from(svg.querySelectorAll('text'))
    .map((t) => (t.textContent || '').trim())
    .filter(Boolean);
  return { chuoi, soMauResolve, soFontGhim, soText, nhanChu };
}

const browser = await launchChromium();
try {
  const page = await browser.newPage();
  const loiTrang = [];
  page.on('pageerror', (e) => loiTrang.push(String(e)));
  await page.goto('file://' + path.resolve(inFile), { waitUntil: 'networkidle' });
  await page.waitForTimeout(cho);

  const ket = await page.evaluate(dongBangTrongTrang, selector);
  if (ket.loi) {
    console.error('bake FAIL:', ket.loi);
    process.exit(1);
  }
  if (loiTrang.length) {
    console.error('bake FAIL: trang co loi JavaScript, callout co the thieu:');
    loiTrang.forEach((l) => console.error('  ' + l));
    process.exit(1);
  }

  const loiXml = kiemTraXml(ket.chuoi);
  if (loiXml) {
    console.error('bake FAIL: SVG sinh ra khong phai XML hop le:', loiXml);
    process.exit(1);
  }
  if (/color-mix\(|var\(/.test(ket.chuoi)) {
    console.error('bake FAIL: con var() hoac color-mix() chua resolve, WeasyPrint se ra 0 fill');
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(path.resolve(outFile)), { recursive: true });
  fs.writeFileSync(outFile, ket.chuoi, 'utf-8');
  console.log(
    `bake OK -> ${outFile} (${ket.soText} node chu, ${ket.soMauResolve} mau resolve, ${ket.soFontGhim} font ghim)`
  );
} finally {
  await browser.close();
}
process.exit(0);
