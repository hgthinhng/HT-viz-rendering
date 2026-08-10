/**
 * gates_song.mjs, chin gate nghiem thu cho lan html-song (HTML tu du mo bang
 * trinh duyet, co animation, tuong tac, JavaScript luc chay).
 *
 * KIEN TRUC KHAC gates.mjs, va khac co chu y: gates.mjs phuc vu lan pdf-so, noi
 * moi gate la mot ham THUAN nhan san {html, pdf} da do truoc boi pdf_checks.py.
 * Lan html-song khong co "PDF da do truoc" tuong duong: rui ro cua no la HANH VI
 * LUC CHAY (JavaScript loi am tham, animation khong tat, phim Tab khong toi duoc
 * mot khoi, mau doi theo chu de) ma phep do tinh (regex tren chuoi HTML) khong
 * bao gio bat duoc. Vi vay moi gate o day la ham ASYNC, tu mo mot trang Chromium
 * that qua scripts/lib/chromium.mjs, dieu khien trang bang Playwright, va DOC
 * TRANG THAI TU getComputedStyle() hoac DOM da render, KHONG doc tu bien trang
 * thai do chinh trang tu khai (neu khong gate chi hoi trang xem trang co lam
 * dung viec cua trang khong, dung benh da ghi trong gates/fixtures/README.md).
 *
 * QUY UOC MOI, chi ap dung cho lan html-song:
 *   - `.da-khoi-tao`   lop tu gan vao mot khoi tuong tac SAU KHI no khoi tao
 *                      thanh cong. Dung boi gate 2 JS-SILENT-FAIL.
 *   - `[data-tuong-tac]`  danh dau moi phan tu tuong tac (nut, khoi mo rong,
 *                      the loc...). Dung boi gate 2 va gate 4.
 *   - `data-tuong-tac-dich="id"`  tren mot phan tu [data-tuong-tac], tro toi id
 *                      cua "container dich" ma hanh dong Enter/Click phai doi
 *                      giong nhau. Dung boi gate 4 KEYBOARD-PATH.
 *   - `<svg data-theme="...">`  moi SVG nhung inline tu khai minh sinh duoi chu
 *                      de nao. Dung boi gate 9 THEME-MATCH.
 *   - `[data-theme="ten"] { --bg: ...; --text: ...; --pos: ...; --neg: ... }`
 *                      moi chu de trang khai qua selector nay tren :root/html.
 *                      Dung boi gate 5 CONTRAST-ALL-THEMES, tu dong do tinh danh
 *                      sach chu de bang regex tren nguon HTML, khong hardcode
 *                      ten chu de.
 *
 * GIOI HAN DA BIET, noi thang thay vi giau:
 *   - `effectiveBg()` (ham dung chung trong UTILS_JS) khong lam alpha compositing
 *     that: neu gap mot nen co alpha < 1 no COI NHU la nen hieu dung va dung lai,
 *     khong tron voi lop phia sau. Fixture cua repo nay deu dung nen alpha=1 nen
 *     gioi han khong lo ra, nhung mot trang that dung `rgba(x x x / 0.5)` lam nen
 *     se bi do sai. Ghi ro o day de nguoi doc sau khong tuong day la phep do day du.
 *   - Nguong SIZE-BUDGET (4MB/8MB) la SUY LUAN THIET KE, xem gate 6.
 *   - Hai gate KHONG dung noi vi khong the ep FAIL tat dinh: "chuyen dong phai
 *     muot 60fps" (may CI qua tai cho FAIL gia) va "trang phai dep". Xem
 *     CLAUDE.md muc "Chin gate lan html-song" (neu da them) hoac bao cao nghiem
 *     thu di kem file nay.
 */
import fs from 'node:fs';
import { launchChromium } from '../scripts/lib/chromium.mjs';
import { gateKhoaChuDe } from './gates.mjs';

export { gateKhoaChuDe };

function ghi(ten, trang_thai, ly_do) {
  return { ten, trang_thai, ly_do: ly_do || [] };
}

// --------------------------------------------------------------------------- //
// Tien ich chay trong TRANG (Playwright addScriptTag), dung chung cho gate 5 va 9
// --------------------------------------------------------------------------- //
const UTILS_JS = `
window.__gateSong = (function () {
  function srgbToLin(c) { c = c / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function relLum(rgb) { return 0.2126 * srgbToLin(rgb[0]) + 0.7152 * srgbToLin(rgb[1]) + 0.0722 * srgbToLin(rgb[2]); }
  function contrastRatio(rgb1, rgb2) {
    var L1 = relLum(rgb1), L2 = relLum(rgb2);
    var a = Math.max(L1, L2), b = Math.min(L1, L2);
    return (a + 0.05) / (b + 0.05);
  }
  function parseColor(str) {
    if (!str) return null;
    var m = str.match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    var p = m[1].split(',').map(function (s) { return parseFloat(s); });
    return [p[0] || 0, p[1] || 0, p[2] || 0, p.length > 3 ? p[3] : 1];
  }
  // Gioi han da biet: khong lam alpha compositing that, xem docstring dau file.
  function effectiveBg(elStart) {
    var node = elStart;
    while (node) {
      var cs = getComputedStyle(node);
      var c = parseColor(cs.backgroundColor);
      if (c && c[3] > 0.01) return [c[0], c[1], c[2]];
      node = node.parentElement;
    }
    return [255, 255, 255];
  }
  function rgbToHsl(rgb) {
    var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;
    if (max === min) { h = s = 0; }
    else {
      var d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      if (max === r) h = (g - b) / d + (g < b ? 6 : 0);
      else if (max === g) h = (b - r) / d + 2;
      else h = (r - g) / d + 4;
      h /= 6;
    }
    return [h * 360, s * 100, l * 100];
  }
  return {
    relLum: relLum, contrastRatio: contrastRatio, parseColor: parseColor,
    effectiveBg: effectiveBg, rgbToHsl: rgbToHsl,
  };
})();
`;

async function tiemUtils(page) {
  await page.addScriptTag({ content: UTILS_JS });
}

// --------------------------------------------------------------------------- //
// Gate 1, OFFLINE-INTACT
// --------------------------------------------------------------------------- //
/**
 * Hai lop: lop tinh quet chuoi nguon HTML tim tham chieu ra ngoai, lop thuc
 * nghiem "ngat mang that" bang Playwright route() chan moi request khong phai
 * file://, data:, about:blank roi dem so bi chan. Day la phep do THAT chu khong
 * doan bang regex: mot @font-face voi `src: url(https://...)` khong khop bat ky
 * mau tinh nao trong danh sach ma van bi lop thuc nghiem bat, vi trinh duyet
 * that su co gang tai no.
 *
 * Cong them hai phep do font TAI DUNG tu scripts/verify-components.mjs (gate
 * offline-fonts-available va offline-body-dung-font-nhung): mot font khong
 * nhung dung se KHONG tai duoc trong dung boi canh da ngat mang, va day chinh
 * la mot dang "tham chieu ra ngoai" an duoi lop CSS chu khong phai lop HTML.
 */
const RE_OFFLINE = [
  { ten: 'src=http', re: /\bsrc\s*=\s*["']https?:\/\//gi },
  { ten: 'href=http', re: /\bhref\s*=\s*["']https?:\/\//gi },
  { ten: '@import url(http', re: /@import\s+(?:url\()?\s*["']?https?:\/\//gi },
  { ten: 'fetch(', re: /\bfetch\s*\(/g },
  { ten: 'XMLHttpRequest', re: /\bXMLHttpRequest\b/g },
  { ten: 'WebSocket', re: /\bWebSocket\b/g },
];

export async function gateOffline({ html, duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  const tinh = [];
  for (const { ten, re } of RE_OFFLINE) {
    const so = (html.match(re) || []).length;
    if (so > 0) tinh.push(`${ten}: ${so} lan`);
  }
  if (tinh.length) {
    trang_thai = 'FAIL';
    ly_do.push(`lop tinh: tham chieu ra ngoai trong nguon HTML: ${tinh.join(', ')}`);
  } else {
    ly_do.push('lop tinh: khong tim thay mau tham chieu ra ngoai nao');
  }

  const ctx = await browser.newContext();
  const bloc = [];
  await ctx.route('**/*', (route) => {
    const url = route.request().url();
    if (url.startsWith('file://') || url.startsWith('data:') || url === 'about:blank') return route.continue();
    bloc.push(url);
    return route.abort();
  });
  const page = await ctx.newPage();
  await page.goto('file://' + duongDanHtml, { waitUntil: 'load' });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.evaluate(() => document.fonts.ready).catch(() => {});
  await page.waitForTimeout(500);

  if (bloc.length) {
    trang_thai = 'FAIL';
    ly_do.push(`lop thuc nghiem: ${bloc.length} request bi chan khi ngat mang that: ${bloc.slice(0, 3).join(', ')}`);
  } else {
    ly_do.push('lop thuc nghiem: 0 request bi chan khi ngat mang that (file://, data:, about:blank deu qua)');
  }

  // Tai dung tu scripts/verify-components.mjs: document.fonts.check() xac nhan
  // font THAT SU tai duoc trong boi canh da ngat mang.
  const fontFamilies = await page.evaluate(() => {
    const set = new Set();
    document.fonts.forEach((f) => set.add(f.family));
    return [...set];
  });
  const fontsOk = {};
  for (const fam of fontFamilies) {
    fontsOk[fam] = await page.evaluate((f) => document.fonts.check(`16px "${f}"`), fam);
  }
  const soFace = fontFamilies.length;
  const allFontsLoaded = soFace > 0 && Object.values(fontsOk).every(Boolean);
  if (!allFontsLoaded) {
    trang_thai = 'FAIL';
    ly_do.push(
      soFace === 0
        ? 'lop thuc nghiem: trang khong khai @font-face nao, khong tu du khi giao di'
        : `lop thuc nghiem: font khong tai duoc khi ngat mang: ${JSON.stringify(fontsOk)}`
    );
  }

  // Tai dung tu scripts/verify-components.mjs: do MUC CHU bang Canvas de bat ca
  // am tham roi ve font mac dinh (font.check() co the true ma phan tu THAT van
  // khong dung font do).
  const mucChu = await page.evaluate(() => {
    const ff = getComputedStyle(document.body).fontFamily;
    const ctx2d = document.createElement('canvas').getContext('2d');
    const mau = 'Sản lượng vận tải quý IV, tăng 12,4%';
    ctx2d.font = `16px ${ff}`;
    const wThat = ctx2d.measureText(mau).width;
    ctx2d.font = '16px "ht-viz-font-khong-ton-tai-9d3f"';
    const wMacDinh = ctx2d.measureText(mau).width;
    return { ff, wThat: Math.round(wThat * 100) / 100, wMacDinh: Math.round(wMacDinh * 100) / 100 };
  });
  const dungFontRieng = Math.abs(mucChu.wThat - mucChu.wMacDinh) > 0.5;
  if (soFace > 0 && !dungFontRieng) {
    trang_thai = 'FAIL';
    ly_do.push(`lop thuc nghiem: muc chu ${mucChu.wThat}px trung voi font mac dinh ${mucChu.wMacDinh}px (${mucChu.ff}), trang roi ve font he thong`);
  }

  await page.close();
  await ctx.close();

  if (trang_thai === 'PASS') ly_do.unshift('file tu du hoan toan: khong tham chieu ra ngoai, font nhung dung va tai duoc');
  return ghi('1. OFFLINE-INTACT', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 2, JS-SILENT-FAIL
// --------------------------------------------------------------------------- //
export async function gateJsSilentFail({ duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const pageErrors = [];
  const consoleErrors = [];
  // Dang ky TRUOC goto, dung yeu cau cua dac ta: bo lo loi neu dang ky sau.
  page.on('pageerror', (err) => pageErrors.push(String(err && err.message ? err.message : err)));
  page.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });

  await page.goto('file://' + duongDanHtml, { waitUntil: 'load' });
  await page.waitForLoadState('networkidle').catch(() => {});
  // Nguong lang: load + networkidle + dem 1500ms, dung nguong da ghi cho animation
  // trong CLAUDE.md ("Cho it nhat 1500ms sau khi tai xong").
  await page.waitForTimeout(1500);

  const thieu = await page.evaluate(() =>
    Array.from(document.querySelectorAll('[data-tuong-tac]'))
      .filter((el) => !el.classList.contains('da-khoi-tao'))
      .map((el) => el.id || el.tagName.toLowerCase())
  );
  await page.close();
  await ctx.close();

  if (pageErrors.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${pageErrors.length} loi runtime (pageerror): ${pageErrors.slice(0, 3).join(' | ')}`);
  }
  if (consoleErrors.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${consoleErrors.length} console.error: ${consoleErrors.slice(0, 3).join(' | ')}`);
  }
  if (thieu.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${thieu.length} khoi [data-tuong-tac] thieu class .da-khoi-tao sau khi lang: ${thieu.slice(0, 5).join(', ')}`);
  }
  if (trang_thai === 'PASS') ly_do.push('0 loi runtime, moi khoi [data-tuong-tac] deu da tu gan .da-khoi-tao');
  return ghi('2. JS-SILENT-FAIL', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 3, REDUCED-MOTION
// --------------------------------------------------------------------------- //
export async function gateReducedMotion({ html, duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  const css = (html.match(/<style\b[^>]*>([\s\S]*?)<\/style>/gi) || []).join('\n');
  const khaiAnimation = [...css.matchAll(/animation(?:-duration)?\s*:\s*([^;}\n]+)/gi)]
    .map((m) => m[1].trim())
    .filter((v) => v && !/^none\b/i.test(v) && !/^0s\b/i.test(v) && !/^0ms\b/i.test(v));
  ly_do.push(`lop tinh: ${khaiAnimation.length} khai bao animation khac none/0 trong CSS (khong phan biet co duoc bao ve boi @media hay khong, chi lop thuc nghiem duoi day moi ket luan)`);

  const demChuyenDong = () => {
    const doMs = (v) => v.split(',').map((s) => s.trim()).reduce((max, s) => {
      const n = s.endsWith('ms') ? parseFloat(s) : parseFloat(s) * 1000;
      return Number.isFinite(n) && n > max ? n : max;
    }, 0);
    const co = [];
    for (const el of document.querySelectorAll('*')) {
      for (const pseudo of [null, '::before', '::after']) {
        const cs = getComputedStyle(el, pseudo);
        const a = doMs(cs.animationDuration || '0s');
        if (a > 1) co.push(`${el.tagName.toLowerCase()}${pseudo || ''}`);
      }
    }
    return co;
  };

  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  const thuong = await page.evaluate(demChuyenDong);
  await page.close();
  await ctx.close();

  const ctxReduce = await browser.newContext({ reducedMotion: 'reduce' });
  const pageReduce = await ctxReduce.newPage();
  await pageReduce.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  const reduce = await pageReduce.evaluate(demChuyenDong);
  await pageReduce.close();
  await ctxReduce.close();

  if (thuong.length === 0) {
    return ghi('3. REDUCED-MOTION', 'SKIP', [
      ...ly_do,
      'trang khong co phan tu nao dang animation o che do thuong, khong chung minh duoc gate nay phan biet duoc hai trang thai, khong tinh la PASS',
    ]);
  }
  ly_do.push(`lop thuc nghiem: che do thuong ${thuong.length} phan tu dang animation, che do reduce con ${reduce.length}`);
  if (reduce.length > 0) {
    trang_thai = 'FAIL';
    ly_do.push(`con ${reduce.length} phan tu KHONG tat animation khi prefers-reduced-motion:reduce: ${reduce.slice(0, 5).join(', ')}`);
  }
  return ghi('3. REDUCED-MOTION', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 4, KEYBOARD-PATH
// --------------------------------------------------------------------------- //
/**
 * Hai phep do doc lap:
 *   1. Bam Tab lap, dung thu tu focus, moi [data-tuong-tac] phai xuat hien.
 *   2. Voi tung cap [data-tuong-tac][data-tuong-tac-dich], so "chu ky DOM" cua
 *      container dich (className + textContent) sau khi kich hoat bang Enter
 *      voi sau khi kich hoat bang Click. Hai duong phai cho cung mot ket qua.
 * Phep 2 doc lap voi phep 1: mot phan tu co the NAM TRONG duong Tab (co
 * tabindex) nhung van khong phan hoi Enter neu thieu trinh xu ly keydown, day
 * la benh pho bien nhat va la ly do gate can CA HAI phep chu khong chi mot.
 */
export async function gateKeyboardPath({ duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  // --- Phep 1: duong Tab ---
  const ctx1 = await browser.newContext();
  const page1 = await ctx1.newPage();
  await page1.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  const danhSach = await page1.evaluate(() =>
    Array.from(document.querySelectorAll('[data-tuong-tac]')).map((el) => el.id)
  );
  if (danhSach.some((id) => !id)) {
    ly_do.push('CANH BAO: co [data-tuong-tac] thieu id, khong dinh danh duoc trong duong Tab, fixture nen luon gan id');
  }

  const daFocus = new Set();
  await page1.evaluate(() => { if (document.body) document.body.setAttribute('tabindex', '-1'); document.body && document.body.focus && document.body.focus(); });
  for (let i = 0; i < danhSach.length + 10; i++) {
    await page1.keyboard.press('Tab');
    const id = await page1.evaluate(() => (document.activeElement ? document.activeElement.id : ''));
    if (id) daFocus.add(id);
  }
  await page1.close();
  await ctx1.close();

  const thieuTab = danhSach.filter((id) => id && !daFocus.has(id));
  if (thieuTab.length) {
    trang_thai = 'FAIL';
    ly_do.push(`duong Tab: ${thieuTab.length} phan tu [data-tuong-tac] KHONG xuat hien trong duong Tab: ${thieuTab.join(', ')}`);
  } else if (danhSach.length) {
    ly_do.push(`duong Tab: ${danhSach.length} phan tu [data-tuong-tac] deu xuat hien`);
  } else {
    ly_do.push('duong Tab: trang khong co [data-tuong-tac] nao');
  }

  // --- Phep 2: chu ky DOM Enter vs Click ---
  const ctxTmp = await browser.newContext();
  const pageTmp = await ctxTmp.newPage();
  await pageTmp.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  const cap = await pageTmp.evaluate(() =>
    Array.from(document.querySelectorAll('[data-tuong-tac][data-tuong-tac-dich]')).map((el) => ({
      id: el.id,
      dich: el.getAttribute('data-tuong-tac-dich'),
    }))
  );
  await pageTmp.close();
  await ctxTmp.close();

  if (cap.length === 0) {
    ly_do.push('chu ky DOM: khong co cap [data-tuong-tac][data-tuong-tac-dich] nao, bo qua phep so sanh Enter vs Click');
    return ghi('4. KEYBOARD-PATH', trang_thai, ly_do);
  }

  const chuKy = async (hanhDong) => {
    const c = await browser.newContext();
    const p = await c.newPage();
    await p.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
    const ra = {};
    for (const { id, dich } of cap) {
      if (hanhDong === 'enter') {
        await p.evaluate((elId) => document.getElementById(elId).focus(), id);
        await p.keyboard.press('Enter');
      } else {
        await p.click('#' + id);
      }
      await p.waitForTimeout(50);
      ra[id] = await p.evaluate((dichId) => {
        const el = document.getElementById(dichId);
        return el ? el.className + '|' + el.textContent.trim() : null;
      }, dich);
    }
    await p.close();
    await c.close();
    return ra;
  };

  const kqEnter = await chuKy('enter');
  const kqClick = await chuKy('click');
  let khopHet = true;
  for (const { id } of cap) {
    if (kqEnter[id] !== kqClick[id]) {
      khopHet = false;
      trang_thai = 'FAIL';
      ly_do.push(`chu ky DOM: "${id}" sau Enter ("${kqEnter[id]}") khac sau Click ("${kqClick[id]}")`);
    }
  }
  if (khopHet) ly_do.push(`chu ky DOM: ${cap.length} cap tuong tac deu cho cung ket qua giua Enter va Click`);

  return ghi('4. KEYBOARD-PATH', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 5, CONTRAST-ALL-THEMES
// --------------------------------------------------------------------------- //
/**
 * Duyet moi phan tu la co text truc tiep, o TUNG chu de dang khai (tu dong do
 * bang regex tren nguon HTML, khong hardcode ten). Nguong WCAG: 4.5:1 chu
 * thuong, 3:1 chu lon (tu 24px, hoac tu 18.66px neu dam).
 *
 * Them mot chieu rieng cua repo nay: `--pos` phai giu goc hue trong dai 120-170
 * do va `--neg` trong dai 340-20 do (quan qua 0) O MOI chu de, vi doi ho mau la
 * doi Y NGHIA so lieu (tang/giam) chu khong phai doi tham my.
 */
const RE_THEME_DECL = /\[data-theme=["']([a-z0-9_-]+)["']\]/gi;

export async function gateContrastAllThemes({ html, duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  let chuDe = [...new Set([...html.matchAll(RE_THEME_DECL)].map((m) => m[1]))];
  if (chuDe.length === 0) {
    return ghi('5. CONTRAST-ALL-THEMES', 'SKIP', ['khong tim thay chu de nao khai qua selector [data-theme="..."] trong CSS, khong co gi de doi chieu']);
  }

  // Trang KHOA cung mot chu de thi chi do chu de do.
  //
  // Ban dau gate lay moi chu de khai trong CSS roi tu bat tung cai len de do. Voi mot
  // trang khong khoa thi dung, nhung repo co mot luat cung khac: file giao khach PHAI
  // khai `<html lang="vi" data-theme="light">`, vi chart matplotlib va 11 minh hoa SVG
  // moi chi co ban sang. Tren dung file do, gate dang do MOT TRANG THAI NGUOI DOC KHONG
  // BAO GIO THAY, roi bao FAIL vi trang thai do xau. Hai luat cua cung mot repo danh nhau,
  // va ben thua la ben khong co ai bien ho.
  //
  // Cach phan xu: doc `data-theme` tren the <html>. Co khai thi do dung no; khong khai
  // thi trang de nguoi doc tu chon, va luc do do CA danh sach nhu cu. Gate khong tu noi
  // cho minh: no van do day du moi phan tu, chi thoi bia them mot boi canh khong ton tai.
  const chuDeKhoa = (html.match(/<html[^>]*\bdata-theme="([^"]+)"/i) || [])[1];
  if (chuDeKhoa) {
    ly_do.push(
      `trang KHOA chu de "${chuDeKhoa}" ngay tren the <html>, nen chi do chu de do. ` +
        `CSS con khai ${chuDe.length} chu de (${chuDe.join(', ')}) nhung nguoi doc khong ` +
        'bat duoc chung, va mot ban giao khach khoa sang la LUAT cua repo chu khong phai thieu sot',
    );
    chuDe = [chuDeKhoa];
  }

  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  await tiemUtils(page);

  const viPhamTuongPhan = [];
  const viPhamHue = [];

  for (const cd of chuDe) {
    await page.evaluate((theme) => document.documentElement.setAttribute('data-theme', theme), cd);
    await page.waitForTimeout(30);

    const doTuongPhan = await page.evaluate(() => {
      const G = window.__gateSong;
      const ra = [];
      const els = document.querySelectorAll('body *');
      for (const el of els) {
        let coChuTrucTiep = false;
        for (const child of el.childNodes) {
          if (child.nodeType === 3 && child.textContent.trim().length > 0) { coChuTrucTiep = true; break; }
        }
        if (!coChuTrucTiep) continue;
        if (el.getClientRects().length === 0) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') continue;
        const fg = G.parseColor(cs.color);
        if (!fg) continue;
        const bg = G.effectiveBg(el);
        const fontSize = parseFloat(cs.fontSize) || 16;
        const weight = cs.fontWeight;
        const dam = weight === 'bold' || parseInt(weight, 10) >= 700;
        const lon = fontSize >= 24 || (fontSize >= 18.66 && dam);
        const nguong = lon ? 3.0 : 4.5;
        const ty = G.contrastRatio([fg[0], fg[1], fg[2]], bg);
        if (ty < nguong) {
          ra.push({
            selector: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
            text: el.textContent.trim().slice(0, 30),
            ty: Math.round(ty * 100) / 100,
            nguong,
          });
        }
      }
      return ra;
    });
    for (const v of doTuongPhan) viPhamTuongPhan.push({ chuDe: cd, ...v });

    const hueRa = await page.evaluate(() => {
      const G = window.__gateSong;
      const csRoot = getComputedStyle(document.documentElement);
      const layMau = (bien) => {
        const gt = csRoot.getPropertyValue(bien).trim();
        if (!gt) return null;
        const probe = document.createElement('div');
        probe.style.color = gt;
        probe.style.display = 'none';
        document.body.appendChild(probe);
        const rgb = G.parseColor(getComputedStyle(probe).color);
        document.body.removeChild(probe);
        return rgb;
      };
      const pos = layMau('--pos');
      const neg = layMau('--neg');
      const out = {};
      if (pos) out.pos = G.rgbToHsl(pos);
      if (neg) out.neg = G.rgbToHsl(neg);
      return out;
    });
    if (hueRa.pos) {
      const h = hueRa.pos[0];
      if (!(h >= 120 && h <= 170)) viPhamHue.push({ chuDe: cd, bien: '--pos', h: Math.round(h * 10) / 10 });
    }
    if (hueRa.neg) {
      const h = hueRa.neg[0];
      const okNeg = (h >= 340 && h <= 360) || (h >= 0 && h <= 20);
      if (!okNeg) viPhamHue.push({ chuDe: cd, bien: '--neg', h: Math.round(h * 10) / 10 });
    }
  }

  await page.close();
  await ctx.close();

  if (viPhamTuongPhan.length) {
    trang_thai = 'FAIL';
    for (const v of viPhamTuongPhan.slice(0, 5)) {
      ly_do.push(`chu de "${v.chuDe}": ${v.selector} "${v.text}" tuong phan ${v.ty}:1 duoi nguong ${v.nguong}:1`);
    }
  }
  if (viPhamHue.length) {
    trang_thai = 'FAIL';
    for (const v of viPhamHue) {
      ly_do.push(`chu de "${v.chuDe}": ${v.bien} co goc hue ${v.h} do, ngoai dai cho phep (--pos 120-170, --neg 340-20)`);
    }
  }
  if (trang_thai === 'PASS') {
    ly_do.unshift(`${chuDe.length} chu de (${chuDe.join(', ')}): tuong phan dat nguong WCAG va --pos/--neg dung dai hue o tat ca`);
  }
  return ghi('5. CONTRAST-ALL-THEMES', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 6, SIZE-BUDGET
// --------------------------------------------------------------------------- //
/**
 * Khong can trinh duyet. WARN tai 4MB, FAIL tai 8MB. Hai con so nay la SUY LUAN
 * THIET KE, CHUA qua do thuc nghiem (chua co phep do "tai bao lau tren mang X
 * thi nguoi doc bo cuoc"), dung dung van hoa tu khai gioi han cua repo: ghi
 * thang ra day thay vi gia vo day la nguong khoa hoc.
 */
export function gateSizeBudget({ duongDanHtml }) {
  const MB = 1024 * 1024;
  const size = fs.statSync(duongDanHtml).size;
  const ly_do = [`kich thuoc file: ${(size / MB).toFixed(2)}MB`];
  ly_do.push('LUU Y: nguong 4MB (WARN) va 8MB (FAIL) la SUY LUAN THIET KE chua qua do thuc nghiem, theo van hoa tu khai gioi han cua repo');
  let trang_thai = 'PASS';
  if (size >= 8 * MB) {
    trang_thai = 'FAIL';
    ly_do.push('vuot tran FAIL 8MB');
  } else if (size >= 4 * MB) {
    trang_thai = 'WARN';
    ly_do.push('vuot tran WARN 4MB');
  }
  return ghi('6. SIZE-BUDGET', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 7, NO-JS-CONTENT
// --------------------------------------------------------------------------- //
const RE_SO_VIET = /\d[\d.,]*\s?(?:%|tỷ|triệu|nghìn|đồng|USD|VND)/gi;

export async function gateNoJsContent({ duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  const ctxOn = await browser.newContext({ javaScriptEnabled: true });
  const pageOn = await ctxOn.newPage();
  await pageOn.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  await pageOn.waitForTimeout(300);
  const textOn = await pageOn.evaluate(() => document.body.innerText || '');
  await pageOn.close();
  await ctxOn.close();

  const ctxOff = await browser.newContext({ javaScriptEnabled: false });
  const pageOff = await ctxOff.newPage();
  await pageOff.goto('file://' + duongDanHtml, { waitUntil: 'load' });
  const textOff = await pageOff.evaluate(() => document.body.innerText || '');
  await pageOff.close();
  await ctxOff.close();

  const soOn = [...new Set((textOn.match(RE_SO_VIET) || []).map((s) => s.replace(/\s+/g, '')))];
  const soOffGon = textOff.replace(/\s+/g, '');
  const thieu = soOn.filter((s) => !soOffGon.includes(s));

  const tyLe = textOn.length > 0 ? textOff.length / textOn.length : 1;

  ly_do.push(`${soOn.length} chuoi so kieu Viet o ban JS-BAT, ty le do dai text TAT/BAT = ${(tyLe * 100).toFixed(0)}%`);

  if (thieu.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${thieu.length} chuoi so bien mat khi tat JS: ${thieu.slice(0, 5).join(', ')}`);
  }
  if (tyLe < 0.85) {
    trang_thai = 'FAIL';
    ly_do.push(`ty le do dai text TAT/BAT ${(tyLe * 100).toFixed(0)}% duoi nguong 85%, noi dung cot loi phu thuoc JS`);
  }
  if (trang_thai === 'PASS') ly_do.unshift('noi dung cot loi ton tai san khi JS tat');
  return ghi('7. NO-JS-CONTENT', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 8, RESPONSIVE-WIDTH
// --------------------------------------------------------------------------- //
const VIEWPORTS = [
  { w: 360, h: 740, ten: '360x740' },
  { w: 768, h: 1024, ten: '768x1024' },
  { w: 1280, h: 800, ten: '1280x800' },
];

export async function gateResponsiveWidth({ duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';
  const DUNG_SAI = 4;

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
    const page = await ctx.newPage();
    await page.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
    const ra = await page.evaluate(() => {
      const doc = document.documentElement;
      const scrollW = doc.scrollWidth;
      const clientW = doc.clientWidth;
      let thuPham = null;
      if (scrollW - clientW > 4) {
        let max = { right: 0, el: null };
        for (const el of document.querySelectorAll('body *')) {
          const r = el.getBoundingClientRect();
          if (r.right > max.right) max = { right: r.right, el };
        }
        if (max.el) {
          const cls = max.el.className && typeof max.el.className === 'string'
            ? '.' + max.el.className.trim().split(/\s+/).join('.')
            : '';
          thuPham = max.el.tagName.toLowerCase() + (max.el.id ? '#' + max.el.id : '') + cls;
        }
      }
      return { scrollW, clientW, thuPham };
    });
    await page.close();
    await ctx.close();

    const chenh = ra.scrollW - ra.clientW;
    if (chenh > DUNG_SAI) {
      trang_thai = 'FAIL';
      ly_do.push(`${vp.ten}: tran ${chenh}px (scrollWidth ${ra.scrollW} vs clientWidth ${ra.clientW}), thu pham: ${ra.thuPham || 'khong xac dinh'}`);
    } else {
      ly_do.push(`${vp.ten}: OK (chenh ${chenh}px, dung sai ${DUNG_SAI}px)`);
    }
  }
  return ghi('8. RESPONSIVE-WIDTH', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 9, THEME-MATCH
// --------------------------------------------------------------------------- //
/**
 * Hai lop:
 *   1. Khai bao: moi <svg> phai tu ghi data-theme, va gia tri phai KHOP voi
 *      data-theme cua <html>. THIEU tinh la FAIL chu khong SKIP.
 *   2. Thuc nghiem: do tuong phan WCAG giua mau nen THAT cua SVG (background-
 *      color cua chinh the <svg>, hoac <rect> dau tien phu kin viewBox neu SVG
 *      trong suot, quy uoc pho bien cua SVG do matplotlib/ECharts SSR sinh ra)
 *      voi nen hieu dung cua trang tai vi tri no nam. FAIL duoi 3:1, nguong
 *      WCAG 1.4.11 cho yeu to do hoa (khong phai nguong van ban 4.5:1).
 *
 *      LOP 2 DA DOI PHEP DO (09-08). Ban dau no do NEN SVG voi NEN TRANG. Phep do
 *      do sai thu: mot chart nen trang tren mot trang nen trang cho dung 1:1 va bi
 *      bao FAIL, trong khi do la dung chuan thiet ke cua repo, tuc lop 2 do MOI an
 *      pham hop le. Bat duoc khi dung ban mau van tai bien dau tien. Thu can do la
 *      MUC voi NEN: mot hinh chim vao nen nghia la net ve cua no khong con doc duoc,
 *      chu khong phai nen cua no trung mau giay. Nay lay net ve DAM NHAT trong SVG
 *      doi chieu voi nen cua chinh SVG do. Ca hai fixture cu giu nguyen va van do
 *      dung ly do: hinh 2 cua fixture do co chu #0F1B28 tren nen #0B1522.
 *
 * Hai lop DOC LAP: mot SVG co the khai dung data-theme (qua lop 1) ma nen van
 * gan nhu trung nen trang (hong lop 2), va nguoc lai mot SVG sinh sai chu de
 * hoan toan (nen trang tren trang toi) lai co tuong phan RAT CAO, nen chi lop 1
 * bat duoc benh kinh dien "trang nen toi ma chart van nen trang" cua repo; lop
 * 2 la mot phep do bo sung, doc lap, bat truong hop nguoc lai: SVG khong con
 * phan biet duoc voi nen trang.
 */
export async function gateThemeMatch({ duongDanHtml, browser }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto('file://' + duongDanHtml, { waitUntil: 'networkidle' });
  await tiemUtils(page);

  const raw = await page.evaluate(() => {
    const G = window.__gateSong;
    const chuDeTrang = document.documentElement.getAttribute('data-theme') || '';
    const svgs = Array.from(document.querySelectorAll('svg'));
    const out = [];
    svgs.forEach((svg, i) => {
      const chuDeSvg = svg.getAttribute('data-theme');
      let nenThat = null;
      const csS = getComputedStyle(svg);
      const bgSvg = G.parseColor(csS.backgroundColor);
      if (bgSvg && bgSvg[3] > 0.01) {
        nenThat = [bgSvg[0], bgSvg[1], bgSvg[2]];
      } else {
        const rect = svg.querySelector('rect');
        if (rect) {
          const fill = getComputedStyle(rect).fill;
          const c = G.parseColor(fill);
          if (c) nenThat = [c[0], c[1], c[2]];
        }
      }
      const nenTrang = G.effectiveBg(svg.parentElement || document.body);
      // Nen de doi chieu MUC: nen rieng cua SVG neu co, khong thi nen cua trang.
      const nenDoi = nenThat || nenTrang;

      // Muc DAM NHAT trong SVG. Duyet phan tu ve, lay ca fill lan stroke, bo `none`
      // va bo trong suot, bo luon chinh o nen. Lay MAX chu khong lay min hay trung
      // binh: duong luoi va nhan phu von co y nhat, doi moi net tu 3:1 la ep chart
      // phai het nhat, con cai can bat la ca SVG chim han vao nen, va do la truong
      // hop KE CA net dam nhat cung khong noi len.
      let mucMax = null;
      let mauMuc = null;
      const ve = svg.querySelectorAll('path,rect,circle,ellipse,line,polyline,polygon,text,tspan');
      let dem = 0;
      for (const el of ve) {
        if (dem++ > 400) break;
        const cs = getComputedStyle(el);
        for (const thuoc of [cs.fill, cs.stroke]) {
          if (!thuoc || thuoc === 'none') continue;
          const c = G.parseColor(thuoc);
          if (!c || (c[3] !== undefined && c[3] < 0.35)) continue;
          const mau = [c[0], c[1], c[2]];
          if (nenThat && mau[0] === nenThat[0] && mau[1] === nenThat[1] && mau[2] === nenThat[2]) continue;
          const t = G.contrastRatio(mau, nenDoi);
          if (mucMax === null || t > mucMax) {
            mucMax = t;
            mauMuc = mau;
          }
        }
      }
      out.push({
        chiSo: i,
        id: svg.id || null,
        chuDeSvg,
        khopKhaiBao: chuDeSvg === chuDeTrang,
        nenThat,
        nenTrang,
        nenDoi,
        mauMuc,
        ty: mucMax === null ? null : Math.round(mucMax * 100) / 100,
      });
    });
    return { chuDeTrang, svgs: out };
  });
  await page.close();
  await ctx.close();

  if (raw.svgs.length === 0) {
    return ghi('9. THEME-MATCH', 'SKIP', ['trang khong co the <svg> nao, khong co gi de doi chieu']);
  }

  for (const s of raw.svgs) {
    const nhan = s.id || `svg thu ${s.chiSo + 1}`;
    if (!s.khopKhaiBao) {
      trang_thai = 'FAIL';
      ly_do.push(
        `${nhan}: data-theme khai "${s.chuDeSvg || '(THIEU)'}" khac data-theme cua trang "${raw.chuDeTrang}". ` +
        'THIEU tinh la FAIL chu khong SKIP'
      );
    }
    if (s.ty !== null && s.ty < 3.0) {
      trang_thai = 'FAIL';
      ly_do.push(
        `${nhan}: net ve dam nhat ${JSON.stringify(s.mauMuc)} chi dat ${s.ty}:1 so voi nen ` +
          `${JSON.stringify(s.nenDoi)} cua chinh no, duoi nguong 3:1 cho yeu to do hoa. ` +
          'Ca hinh chim vao nen chu khong phai mot chi tiet mo',
      );
    }
  }
  if (trang_thai === 'PASS') {
    ly_do.unshift(`${raw.svgs.length} SVG deu khai dung data-theme va tuong phan nen dat nguong`);
  }
  return ghi('9. THEME-MATCH', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Chay ca bo
// --------------------------------------------------------------------------- //
// Ten gate DUNG NHU code that o duoi, dung thu tu chay. Dung boi gates/run.mjs de
// sinh nghiem-thu.json va boi test doi chieu o tests/consistency/phong_cach.test.mjs.
export const TEN_GATES_SONG = [
  '1. OFFLINE-INTACT', '2. JS-SILENT-FAIL', '3. REDUCED-MOTION', '4. KEYBOARD-PATH',
  '5. CONTRAST-ALL-THEMES', '6. SIZE-BUDGET', '7. NO-JS-CONTENT', '8. RESPONSIVE-WIDTH',
  '9. THEME-MATCH', '10. KHOA-CHU-DE',
];

/**
 * Ham THUAN, khong throw: so ten thuc te chay ra voi registry, tra ve null neu
 * khop hoac chuoi mo ta lech neu khong. Tach rieng khoi chayTatCaSong vi mot
 * lan throw NGAY TRONG chayTatCaSong se nem loi TRUOC khi run.mjs kip in bang
 * ket qua, lam mat sach chan doan cua ca luot chay (ke ca khi da mo Chromium
 * va chay xong ca 9 gate). Goi ham nay o phia goi SAU KHI da in xong bang.
 */
export function kiemKhopRegistry(ketQua, registry = TEN_GATES_SONG) {
  const ten = ketQua.map((g) => g.ten);
  if (JSON.stringify(ten) === JSON.stringify(registry)) return null;
  return `Registry TEN_GATES_SONG lech ket qua that: ${ten.join(', ')}`;
}

export async function chayTatCaSong({ duongDanHtml }) {
  const html = fs.readFileSync(duongDanHtml, 'utf-8');
  const browser = await launchChromium();
  try {
    const goi = { html, duongDanHtml, browser };
    return [
      await gateOffline(goi),
      await gateJsSilentFail(goi),
      await gateReducedMotion(goi),
      await gateKeyboardPath(goi),
      await gateContrastAllThemes(goi),
      gateSizeBudget(goi),
      await gateNoJsContent(goi),
      await gateResponsiveWidth(goi),
      await gateThemeMatch(goi),
      gateKhoaChuDe({ html, soThuTu: 10 }),
    ];
  } finally {
    await browser.close();
  }
}
