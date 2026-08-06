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

  // Bat hai loai tin hieu THAT xay ra luc tai trang, dung de phan biet "file
  // khong dinh dung annotation" voi "file co dinh dung nhung lop annotation
  // hong":
  //   1) requestfailed voi URL chua "annotate.js" — bang chung TRUC TIEP
  //      nhat cho kich ban loader hong (script src tro sai/file khong ton
  //      tai). Da tu kiem chung thuc nghiem: duoi file://, mot <script src>
  //      tro toi file khong ton tai LAM NO Playwright ban 'requestfailed'
  //      that voi failure().errorText = "net::ERR_FILE_NOT_FOUND", khong
  //      phai suy doan.
  //   2) pageerror (loi JS khong bat duoc, lam mot <script> dung giua
  //      chung) — chi coi la lien quan annotation NEU noi dung loi co nhac
  //      "annotate"/"Annotate" (vd "ReferenceError: Annotate is not
  //      defined"). Loi JS KHONG nhac gi toi annotate (vd mot script do
  //      luong/demo khac tren cung trang loi rieng) KHONG duoc quy cho lop
  //      annotation.
  const pageErrors = [];
  const failedRequests = [];
  const onPageError = (e) => pageErrors.push(String(e));
  const onRequestFailed = (req) => failedRequests.push(req.url());
  page.on('pageerror', onPageError);
  page.on('requestfailed', onRequestFailed);
  // RANG BUOC: moi file examples/*.html PHAI goi Annotate.annotate() DONG BO
  // (khong duoc trong setTimeout, Promise.then, hay bat ky async handler
  // nao chua chac chan da no truoc moc networkidle). "networkidle" chi cho
  // biet mang da ngung, khong dam bao mot lenh goi bi hoan (deferred) da
  // chay xong. Neu sau nay them example goi annotate() bat dong bo, script
  // nay se FAIL SAI (bao "khong tim thay path.anno-leader" trong khi thu
  // vien se ve dung, chi la chua kip). Chap nhan rang buoc dong bo thay vi
  // doi them mot tin hieu khac (vd cho toi khi thay g.annotations xuat
  // hien) vi hai file that hien tai deu goi dong bo, va mot khoang cho co
  // dinh se la doan mo (guess) chu khong phai do bang so that.
  await page.goto(url, { waitUntil: 'networkidle' });
  page.off('pageerror', onPageError);
  page.off('requestfailed', onRequestFailed);

  // Dung "includes('annotate')" (khong doi hoi ".js" dinh kem) vi mot
  // duong dan hong that su co the doi ten hoan toan (vd go sai thanh
  // "annotate-DUONG-DAN-SAI.js" — van con chua "annotate" nhung khong con
  // nguyen cum "annotate.js"). Van an toan vi day la URL cua MOT REQUEST
  // DA THAT SU 404, khong phai doan tu van ban tuy y trong file.
  const annotateLoadFailed = failedRequests.some((u) => u.toLowerCase().includes('annotate'));
  const annotateRelatedErrors = pageErrors.filter((e) => /annotate/i.test(e));
  const unrelatedErrors = pageErrors.filter((e) => !/annotate/i.test(e));

  // Khong phai moi file .html trong examples/ deu dung lop annotation:
  // vietnam-simplification-comparison.html la demo do-luong 3 muc don gian
  // hoa path ban do (gen-vietnam-path.mjs), khong dung annotate.js, khong co
  // callout nao ca. Ep hai kiem tra hinh hoc cua lop annotation len 1 file
  // khong lien quan se tao FAIL gia (khong phai loi hinh hoc that ma la
  // sai pham vi).
  //
  // Dieu kien SKIP/FAIL DO HANH VI THAT sau khi trang da tai xong, KHONG
  // doan tu van ban nguon (lich su sua qua 2 vong truoc: vong 1 doc chuoi
  // "annotate.js" trong HTML -> bi qua mat khi loader hong; vong 2 doi sang
  // kiem window.Annotate + BAT KY loi JS nao -> qua RONG, se FAIL oan cho
  // lop annotation neu trang co loi JS o mot script khac khong lien quan).
  // Ban nay THU HEP pham vi quy loi: chi coi la loi cua lop annotation khi
  // co BANG CHUNG THAT no lien quan (xem annotateLoadFailed/
  // annotateRelatedErrors o tren, tinh tu requestfailed + pageerror loc
  // theo tu khoa "annotate").
  //   - window.Annotate TON TAI -> file co nap thu vien -> PHAI sinh ra
  //     path.anno-leader, khong sinh ra thi FAIL (nhanh nay khong doi qua
  //     ca 3 vong).
  //   - window.Annotate KHONG ton tai, VA co bang chung annotate.js nap
  //     hong (requestfailed dung URL) HOAC loi JS nhac toi annotate -> FAIL,
  //     nghi hong lop annotation, khong phai file ngoai pham vi.
  //   - window.Annotate KHONG ton tai, KHONG co bang chung lien quan
  //     annotate, NHUNG co loi JS khac (vd mot script do luong/demo khac
  //     tren cung trang loi rieng) -> DAY LA CA MOI o vong 3: khong duoc
  //     FAIL do toi nham cho annotation (repo cam quy nhan sai chu the loi),
  //     nhung cung khong duoc nuot im lang (repo cam fallback im lang) ->
  //     SKIP kem CANH BAO in nguyen van loi JS do, de nguoi chay biet trang
  //     co van de khac dang cho xu ly rieng.
  //   - window.Annotate KHONG ton tai, khong loi gi ca -> SKIP hop le nhu
  //     cac vong truoc.
  const hasAnnotate = await page.evaluate(() => typeof window.Annotate !== 'undefined');
  if (!hasAnnotate) {
    if (annotateLoadFailed || annotateRelatedErrors.length > 0) {
      const evidence = [
        ...(annotateLoadFailed ? [`requestfailed voi URL nhac annotate (${failedRequests.filter((u) => u.toLowerCase().includes('annotate')).join('; ')})`] : []),
        ...annotateRelatedErrors,
      ].join('; ');
      log(
        false,
        `${file}: window.Annotate khong ton tai VA co bang chung lien quan annotate (${evidence}) -> nghi hong lop annotation, khong phai file ngoai pham vi`,
      );
    } else if (unrelatedErrors.length > 0) {
      console.log(`[SKIP] ${file}: window.Annotate khong ton tai, khong thuoc pham vi kiem tra lop annotation. CANH BAO: trang co ${unrelatedErrors.length} loi JS KHONG lien quan annotate (${unrelatedErrors.join('; ')}) -> co the la van de khac tren trang nay, can nguoi xem lai.`);
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
