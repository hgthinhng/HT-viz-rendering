#!/usr/bin/env node
// Verify hinh hoc cho minh hoa nhom C. Hai kiem tra deu phai do bang so,
// vi sai so qua nho de mat bat duoc tren anh full-page.
import { chromium } from 'playwright-core';
import { readdirSync, readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const EXE = `${process.env.HOME}/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`;
const MAX_RATIO = 1.6;
const MARGIN = 8;

let failed = 0;
const log = (ok, msg) => {
  console.log(`${ok ? '[PASS]' : '[FAIL]'} ${msg}`);
  if (!ok) failed += 1;
};

const browser = await chromium.launch({ executablePath: EXE });
const page = await browser.newPage();

const examples = readdirSync(path.join(ROOT, 'illustrations/examples')).filter((f) =>
  f.endsWith('.html'),
);

for (const file of examples) {
  const filePath = path.join(ROOT, 'illustrations/examples', file);

  // Khong phai moi file .html trong examples/ deu goi Annotate.annotate():
  // vietnam-simplification-comparison.html la demo do-luong 3 muc don gian
  // hoa path ban do (gen-vietnam-path.mjs), khong goi ham nay, khong co
  // callout nao ca. Ep hai kiem tra hinh hoc cua lop annotation len 1 file
  // khong lien quan se tao FAIL gia (khong phai loi hinh hoc that ma la
  // sai pham vi).
  //
  // Dieu kien SKIP CO Y kiem tra loi goi ham that "Annotate.annotate(",
  // KHONG kiem chuoi ten file "annotate.js" — vi chuoi ten file co the chi
  // xuat hien trong <script src="../annotate.js"> (dieu nap thu vien). Neu
  // mot ngay the src bi xoa/go sai duong dan (vd hoi quy giong Step 6), file
  // van con loi goi Annotate.annotate(...) trong <script> noi tuyen, nen
  // van bi coi la "co y dinh dung annotation" -> KHONG duoc SKIP -> chay
  // tiep -> Annotate la undefined -> loi goi nem ReferenceError -> khong co
  // path.anno-leader nao duoc tao -> dung [FAIL], khong phai [SKIP]/[PASS]
  // gia. Da xac nhan thuc te: banner.html CHI co dung 1 lan xuat hien chuoi
  // "annotate.js" trong toan bo file (chinh la the script src) — neu dung
  // check chuoi ten file nhu ban truoc, xoa dong do se bi SKIP oan.
  const raw = readFileSync(filePath, 'utf8');
  if (!/Annotate\s*\.\s*annotate\s*\(/.test(raw)) {
    console.log(`[SKIP] ${file}: khong goi Annotate.annotate(), khong thuoc pham vi kiem tra lop annotation`);
    continue;
  }

  const url = pathToFileURL(filePath).href;
  await page.goto(url, { waitUntil: 'networkidle' });

  const paths = await page.evaluate(() =>
    [...document.querySelectorAll('path.anno-leader')].map((p) => {
      const d = p.getAttribute('d') || '';
      const nums = d.match(/-?\d+(?:\.\d+)?/g) || [];
      const x1 = +nums[0];
      const y1 = +nums[1];
      const x2 = +nums[nums.length - 2];
      const y2 = +nums[nums.length - 1];
      return { len: p.getTotalLength(), straight: Math.hypot(x2 - x1, y2 - y1) };
    }),
  );
  if (paths.length === 0) {
    log(false, `${file}: khong tim thay path.anno-leader nao`);
  } else {
    const worst = Math.max(...paths.map((p) => p.len / Math.max(p.straight, 1)));
    log(worst <= MAX_RATIO, `${file}: ty le duong dan lon nhat ${worst.toFixed(3)}x (nguong ${MAX_RATIO}x)`);
  }

  const overflow = await page.evaluate((margin) => {
    const svg = document.querySelector('svg[viewBox]');
    if (!svg) return ['khong co svg[viewBox]'];
    const [, , vw, vh] = svg.getAttribute('viewBox').split(/\s+/).map(Number);
    const bad = [];
    for (const r of svg.querySelectorAll('rect.anno-box')) {
      const x = +r.getAttribute('x');
      const y = +r.getAttribute('y');
      const w = +r.getAttribute('width');
      const h = +r.getAttribute('height');
      if (x < margin || y < margin || x + w > vw - margin || y + h > vh - margin) {
        bad.push(`hop tai (${x},${y}) ${w}x${h} tran khoi ${vw}x${vh}`);
      }
    }
    return bad;
  }, MARGIN);
  log(overflow.length === 0, `${file}: hop nhan trong viewBox (${overflow.length} loi)${overflow.length ? ' -> ' + overflow.join('; ') : ''}`);
}

await browser.close();
console.log(failed === 0 ? 'TAT CA PASS' : `${failed} GATE FAIL`);
process.exit(failed === 0 ? 0 : 1);
