#!/usr/bin/env node
// Verify hinh hoc cho minh hoa nhom C. Hai kiem tra deu phai do bang so,
// vi sai so qua nho de mat bat duoc tren anh full-page.
import { chromium } from 'playwright-core';
import { readdirSync } from 'node:fs';
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
  const url = pathToFileURL(filePath).href;

  // Bat loi JS THAT xay ra luc tai trang (vd ReferenceError khi mot script
  // goi ham cua thu vien chua nap duoc) — dung ben duoi de phan biet "file
  // khong dinh dung annotation" voi "file co dinh dung nhung load hong".
  const pageErrors = [];
  const onPageError = (e) => pageErrors.push(String(e));
  page.on('pageerror', onPageError);
  await page.goto(url, { waitUntil: 'networkidle' });
  page.off('pageerror', onPageError);

  // Khong phai moi file .html trong examples/ deu dung lop annotation:
  // vietnam-simplification-comparison.html la demo do-luong 3 muc don gian
  // hoa path ban do (gen-vietnam-path.mjs), khong dung annotate.js, khong co
  // callout nao ca. Ep hai kiem tra hinh hoc cua lop annotation len 1 file
  // khong lien quan se tao FAIL gia (khong phai loi hinh hoc that ma la
  // sai pham vi).
  //
  // Dieu kien SKIP DO HANH VI THAT sau khi trang da tai xong, KHONG doan tu
  // van ban nguon. Ban truoc dua vao doc chuoi tho trong file .html (lan 1:
  // ten file "annotate.js"; lan 2: loi goi "Annotate.annotate(") — bi qua
  // mat neu ai do goi qua bien trung gian nhu
  // `const fn = Annotate.annotate; fn(svg, items)`, vi chuoi tho khong con
  // khop dang "Annotate.annotate(" du annotate.js van chay dung (DA TU KIEM
  // CHUNG THUC NGHIEM: kich ban nay lam window.Annotate = true, dung nhu ky
  // vong).
  //
  // Chi doi sang kiem `window.Annotate` khong thoi la CHUA DU: da tu kiem
  // chung thuc nghiem bang cach dung lai kich ban hong loader cua vong 1
  // (pha duong dan <script src>, giu nguyen loi goi Annotate.annotate(...))
  // va thay `window.Annotate` VAN la undefined trong truong hop nay — vi
  // annotate.js chua bao gio chay duoc nen khong co gi gan window.Annotate
  // ca. Neu chi dung mot dieu kien "khong ton tai -> SKIP" thi day lai la
  // dung CHINH LOAI SKIP OAN da sua o vong 1, chi khac co che phat hien.
  // Ket hop them tin hieu "co loi JS that luc tai trang khong" de phan
  // biet hai truong hop giong het nhau ve mat window.Annotate:
  //   - Khong co window.Annotate VA KHONG co loi JS nao -> file thuc su
  //     khong dinh dung annotation (vietnam-simplification-comparison.html)
  //     -> SKIP hop le.
  //   - Khong co window.Annotate NHUNG CO loi JS (vd "ReferenceError:
  //     Annotate is not defined") -> file co dinh goi annotation nhung
  //     thu vien khong nap duoc -> day la mot su co that, phai FAIL, khong
  //     duoc SKIP.
  //   - Co window.Annotate -> file co nap thu vien -> PHAI sinh ra
  //     path.anno-leader, khong sinh ra thi FAIL (nhanh nay khong doi).
  const hasAnnotate = await page.evaluate(() => typeof window.Annotate !== 'undefined');
  if (!hasAnnotate) {
    if (pageErrors.length > 0) {
      log(
        false,
        `${file}: window.Annotate khong ton tai VA co loi JS luc tai trang (${pageErrors.join('; ')}) -> nghi hong lop annotation, khong phai file ngoai pham vi`,
      );
    } else {
      console.log(`[SKIP] ${file}: window.Annotate khong ton tai, khong co loi JS nao luc tai trang -> khong thuoc pham vi kiem tra lop annotation`);
    }
    continue;
  }

  const paths = await page.evaluate(() =>
    [...document.querySelectorAll('path.anno-leader')].map((p) => {
      const d = p.getAttribute('d') || '';
      const nums = d.match(/-?\d+(?:\.\d+)?/g) || [];
      const x1 = +nums[0];
      const y1 = +nums[1];
      // Gia dinh: cap so cuoi cung trong "d" la DIEM CUOI THAT cua path, chu
      // khong phai toa do dieu khien cua lenh Q (bo goc bang cong tron). Da
      // tu kiem lai truc tiep trong annotate.js (ham roundedElbow, hien
      // dang o dong 197-207, so dong co the doi khi file duoc sua sau nay —
      // tim theo ten ham cho chac): CA BA nhanh deu ket thuc bang lenh L,
      // ke ca nhanh bo goc "...Q cx cy p2x p2y L lx ly" — hai so cuoi la
      // diem L, khong phai tham so Q. Neu sau nay roundedElbow doi cach ve
      // (vd ket bang Q hoac C ma khong co L theo sau), phai kiem lai gia
      // dinh nay.
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
