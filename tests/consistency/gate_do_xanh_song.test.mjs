/**
 * gate_do_xanh_song.test.mjs, moi gate cua lan html-song phai PHAN BIET DUOC hai
 * trang thai, dung luat da ghi trong gates/fixtures/README.md va CLAUDE.md.
 *
 * Khac voi gate_do_xanh.test.mjs (lan pdf-so, ham THUAN nhan {html, pdf} tong
 * hop): gate cua lan html-song la ham ASYNC, tu mo Chromium that qua
 * gates/lib/chromium.mjs roi doc getComputedStyle/DOM da render. Vi vay fixture
 * o day la FILE HTML THAT tren dia (gates/fixtures/song/), khong phai du lieu
 * tong hop trong test, va moi test do phai khang dinh tren NOI DUNG thong bao
 * loi (ly_do) chu khong chi tren trang_thai, de chac gate do vi DUNG LY DO chu
 * khong phai vi thieu file hay het timeout.
 */
import { test, after } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { launchChromium } from '../../scripts/lib/chromium.mjs';
import {
  gateOffline,
  gateJsSilentFail,
  gateReducedMotion,
  gateKeyboardPath,
  gateContrastAllThemes,
  gateSizeBudget,
  gateNoJsContent,
  gateResponsiveWidth,
  gateThemeMatch,
} from '../../gates/gates_song.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const FIX = path.join(GOC, 'gates/fixtures/song');

const browser = await launchChromium();
after(async () => {
  await browser.close();
});

function goi(tenFile) {
  const duongDanHtml = path.join(FIX, tenFile);
  const html = fs.readFileSync(duongDanHtml, 'utf-8');
  return { html, duongDanHtml, browser };
}

// --------------------------------------------------------------------------- //
test('gate 1 OFFLINE-INTACT phan biet file tu du voi file con tham chieu ra ngoai', { timeout: 30000 }, async () => {
  const xanh = await gateOffline(goi('offline-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateOffline(goi('offline-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /tham chieu ra ngoai/);
  assert.match(noiDung, /bi chan khi ngat mang that/);
});

// --------------------------------------------------------------------------- //
test('gate 2 JS-SILENT-FAIL phan biet khoi khoi tao thanh cong voi khoi loi am tham', { timeout: 30000 }, async () => {
  const xanh = await gateJsSilentFail(goi('jssilent-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateJsSilentFail(goi('jssilent-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /loi runtime \(pageerror\)/);
  assert.match(noiDung, /thieu class \.da-khoi-tao/);
});

// --------------------------------------------------------------------------- //
test('gate 3 REDUCED-MOTION phan biet animation co bao ve voi animation khong tat', { timeout: 30000 }, async () => {
  const xanh = await gateReducedMotion(goi('reducedmotion-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateReducedMotion(goi('reducedmotion-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  assert.match(do_.ly_do.join(' | '), /KHONG tat animation khi prefers-reduced-motion:reduce/);
});

// --------------------------------------------------------------------------- //
test('gate 4 KEYBOARD-PATH phan biet Enter dung voi Enter khong lam gi', { timeout: 45000 }, async () => {
  const xanh = await gateKeyboardPath(goi('keyboard-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateKeyboardPath(goi('keyboard-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  assert.match(do_.ly_do.join(' | '), /chu ky DOM: "nut-1" sau Enter .* khac sau Click/);
});

// --------------------------------------------------------------------------- //
test('gate 5 CONTRAST-ALL-THEMES phan biet chu de dat nguong voi chu de mot chu de bi hong', { timeout: 30000 }, async () => {
  const xanh = await gateContrastAllThemes(goi('contrast-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateContrastAllThemes(goi('contrast-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /chu de "dark".*duoi nguong/);
  assert.match(noiDung, /--neg co goc hue.*ngoai dai cho phep/);
});

test('gate 5 chi do chu de ma trang KHOA, khong bia them boi canh nguoi doc khong thay', { timeout: 30000 }, async () => {
  // `contrast-khoa-xanh.html` giong `contrast-do.html` tung ky tu tru mot thu: the
  // <html> khoa data-theme="light". Chu de "dark" trong CSS van hong y nguyen. Cap nay
  // la bang chung cho nhanh moi: gate doc chu de khoa thay vi tu bat tung chu de len.
  // Khong co no thi nhanh do khong duoc kiem gi, va mot nhanh khong ai kiem la mot
  // nhanh co the am tham lam gate ngung bat benh that.
  const khoa = await gateContrastAllThemes(goi('contrast-khoa-xanh.html'));
  assert.equal(
    khoa.trang_thai,
    'PASS',
    `trang khoa sang ma van bao FAIL theo chu de toi: ${khoa.ly_do.join(' | ')}`,
  );
  assert.match(khoa.ly_do.join(' | '), /trang KHOA chu de "light"/);
});

// --------------------------------------------------------------------------- //
test('gate 6 SIZE-BUDGET phan biet file nho voi file vuot tran 8MB', () => {
  const xanh = gateSizeBudget({ duongDanHtml: path.join(FIX, 'size-xanh.html') });
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = gateSizeBudget({ duongDanHtml: path.join(FIX, 'size-do.html') });
  assert.equal(do_.trang_thai, 'FAIL');
  assert.match(do_.ly_do.join(' | '), /vuot tran FAIL 8MB/);
});

// --------------------------------------------------------------------------- //
test('gate 7 NO-JS-CONTENT phan biet noi dung tinh voi noi dung chi bom boi JS', { timeout: 30000 }, async () => {
  const xanh = await gateNoJsContent(goi('nojs-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateNoJsContent(goi('nojs-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /bien mat khi tat JS/);
  assert.match(noiDung, /duoi nguong 85%/);
});

// --------------------------------------------------------------------------- //
test('gate 8 RESPONSIVE-WIDTH phan biet khung co giai voi khung co dinh gay tran', { timeout: 30000 }, async () => {
  const xanh = await gateResponsiveWidth(goi('responsive-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateResponsiveWidth(goi('responsive-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /360x740: tran \d+px/);
  assert.match(noiDung, /khung-cung/);
});

// --------------------------------------------------------------------------- //
test('gate 9 THEME-MATCH phan biet SVG khai dung chu de voi SVG thieu khai bao hoac lan nen', { timeout: 30000 }, async () => {
  const xanh = await gateThemeMatch(goi('thememacth-xanh.html'));
  assert.equal(xanh.trang_thai, 'PASS');

  const do_ = await gateThemeMatch(goi('thememacth-do.html'));
  assert.equal(do_.trang_thai, 'FAIL');
  const noiDung = do_.ly_do.join(' | ');
  assert.match(noiDung, /data-theme khai "\(THIEU\)".*THIEU tinh la FAIL chu khong SKIP/);
  assert.match(noiDung, /hinh-2.*duoi nguong 3:1/);
});
