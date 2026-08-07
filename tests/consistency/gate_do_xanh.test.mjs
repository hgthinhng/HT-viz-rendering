/**
 * gate_do_xanh.test.mjs — moi gate phai PHAN BIET DUOC hai trang thai.
 *
 * Voi tung gate: mot fixture phai PASS va mot fixture phai FAIL. Gate nao khong do
 * duoc voi fixture do cua chinh no thi gate do chua ton tai, du no dang bao xanh tren
 * moi file that. Repo nay da co ba gate nhu vay o Phase 1, xem gates/fixtures/README.md.
 *
 * Fixture dung o day la du lieu tong hop chu khong phai file that, vi gate la ham thuan
 * nhan {html, pdf}. Rang buoc rieng "cau truc pdf_checks.py sinh ra van khop voi thu
 * gate mong doi" do tests/smoke/pipeline_that.test.mjs giu.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  gateFontHtml,
  gateFontPdf,
  gateRaster,
  gateDau,
  gateChartSong,
  gateCalloutBaked,
  gateVanPhong,
  gateNgatTrang,
  gateRoRiNguon,
  gateSoNguon,
  boTrang,
  tachSvg,
} from '../../gates/gates.mjs';
import fs from 'node:fs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const FIX = path.join(GOC, 'gates/fixtures');

/** Goi pdf toi thieu dung cau truc pdf_checks.py tra ve. */
function pdfMau(ghiDe = {}) {
  return {
    kich_thuoc_byte: 80000,
    so_trang: 4,
    byte_moi_trang: 20000,
    net_ve_theo_trang: [3, 20, 40, 10],
    net_ve_tong: 73,
    font: { ho_font: { Spectral: { nhung: true, duoi: 'ttf' }, 'IBM-Plex-Mono': { nhung: true, duoi: 'ttf' } } },
    raster: { so_object: 0, anh_toan_panel: [], tong_px: 0 },
    dau: { tong_ky_tu: 5000, fffd: 0, dau_tong: 900, dau_synthetic: 0, synthetic_khoang_trang: 120 },
    ngat_trang: { the_bi_cat: [], so_lan: 0 },
    text: '',
    text_bo_trang: '',
    ...ghiDe,
  };
}

const SVG_HOP_LE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><text x="4" y="20">Giá bán bình quân</text></svg>';
// Nhay kep long trong nhay kep, dung loi da lam 12 chart bien mat khoi PDF suot Phase 1.
const SVG_HONG_XML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><text style="font-family:"Spectral", serif" x="4" y="20">Giá bán bình quân</text></svg>';

const boc = (svg, ma = 'hinh-1') =>
  `<figure class="hinh" id="${ma}"><div class="hinh-khung">${svg}</div><figcaption class="hinh-chu">Chu thich</figcaption></figure>`;

// --------------------------------------------------------------------------- //
test('gate 1 FONT-HTML phan biet font nhung base64 voi font tran', () => {
  const xanh = `<style>@font-face{font-family:'Spectral';src:url(data:font/woff2;base64,AAA) format('woff2');}
    body{font-family:'Spectral', Georgia, serif;}</style>`;
  const do_ = `<style>body{font-family:'Spectral', Georgia, serif;}</style>`;

  assert.equal(gateFontHtml({ html: xanh }).trang_thai, 'PASS');
  assert.equal(gateFontHtml({ html: do_ }).trang_thai, 'FAIL');
});

test('gate 2 FONT-PDF phan biet font repo voi font he thong Linux', () => {
  const xanh = pdfMau();
  // Day dung la ket qua do duoc khi mot trang quen khai @font-face: tang text van
  // dung y nguyen, chi ten font trong PDF la khac.
  const do_ = pdfMau({
    font: { ho_font: { 'Noto-Serif': { nhung: true, duoi: 'ttf' }, 'Liberation-Mono': { nhung: true, duoi: 'ttf' } } },
  });

  assert.equal(gateFontPdf({ pdf: xanh }).trang_thai, 'PASS');
  const kq = gateFontPdf({ pdf: do_ });
  assert.equal(kq.trang_thai, 'FAIL');
  assert.match(kq.ly_do.join(' '), /Noto-Serif/);
});

test('gate 2 FONT-PDF do khi PDF khong nhung font nao', () => {
  assert.equal(gateFontPdf({ pdf: pdfMau({ font: { ho_font: {} } }) }).trang_thai, 'FAIL');
});

test('gate 3 RASTER phan biet ban vector voi ban co anh nuong bitmap', () => {
  assert.equal(gateRaster({ pdf: pdfMau() }).trang_thai, 'PASS');
  const do_ = pdfMau({ raster: { so_object: 12, anh_toan_panel: [{ w: 1200, h: 800, px: 960000 }], tong_px: 960000 } });
  assert.equal(gateRaster({ pdf: do_ }).trang_thai, 'FAIL');
});

test('gate 3 RASTER cho phep anh khi khai tuong minh', () => {
  const co1anh = pdfMau({ raster: { so_object: 1, anh_toan_panel: [], tong_px: 4000 } });
  assert.equal(gateRaster({ pdf: co1anh }).trang_thai, 'FAIL');
  assert.equal(gateRaster({ pdf: co1anh, choPhepAnh: 1 }).trang_thai, 'PASS');
});

test('gate 4 DIACRITICS do khi co FFFD hoac ky tu CO DAU synthetic', () => {
  const html = '<p>Số liệu quý 3 đạt mức đã điều chỉnh</p>';
  assert.equal(gateDau({ html, pdf: pdfMau({ dau: { ...pdfMau().dau, dau_tong: 20 } }) }).trang_thai, 'PASS');
  const coFffd = pdfMau({ dau: { ...pdfMau().dau, dau_tong: 20, fffd: 3 } });
  assert.equal(gateDau({ html, pdf: coFffd }).trang_thai, 'FAIL');
  const coSynth = pdfMau({ dau: { ...pdfMau().dau, dau_tong: 20, dau_synthetic: 5 } });
  assert.equal(gateDau({ html, pdf: coSynth }).trang_thai, 'FAIL');
});

test('gate 4 DIACRITICS KHONG do vi dau cach synthetic, day la binh thuong', () => {
  const html = '<p>Số liệu quý 3 đạt mức đã điều chỉnh</p>';
  const nhieuKhoangTrang = pdfMau({ dau: { ...pdfMau().dau, dau_tong: 20, synthetic_khoang_trang: 999 } });
  assert.equal(gateDau({ html, pdf: nhieuKhoangTrang }).trang_thai, 'PASS');
});

test('gate 5 CHART-SONG do khi SVG khong phai XML hop le', () => {
  const pdf = pdfMau({ text_bo_trang: boTrang('Giá bán bình quân') });
  assert.equal(gateChartSong({ html: boc(SVG_HOP_LE), pdf }).trang_thai, 'PASS');
  const kq = gateChartSong({ html: boc(SVG_HONG_XML), pdf });
  assert.equal(kq.trang_thai, 'FAIL');
  assert.match(kq.ly_do.join(' '), /XML hop le/);
});

test('gate 5 CHART-SONG do khi hinh hop le nhung khong de lai chu trong PDF', () => {
  // Day la ca ma moi gate cu deu bo lot: SVG dep, dem duoc, ma PDF khong co gi.
  const pdfTrong = pdfMau({ text_bo_trang: 'ChuKhacHoanToan' });
  const kq = gateChartSong({ html: boc(SVG_HOP_LE), pdf: pdfTrong });
  assert.equal(kq.trang_thai, 'FAIL');
  assert.match(kq.ly_do.join(' '), /khong den duoc ban in/);
});

test('gate 6 CALLOUT-BAKED do khi trang con dua vao annotate.js luc chay', () => {
  const daBake = `<svg><g class="annotations"><text>342 nghìn đồng/tấn</text></g></svg>`;
  assert.equal(gateCalloutBaked({ html: daBake }).trang_thai, 'PASS');

  const chuaBake = `<script src="../illustrations/annotate.js"></script><svg></svg>`;
  const kq = gateCalloutBaked({ html: chuaBake });
  assert.equal(kq.trang_thai, 'FAIL');
  assert.match(kq.ly_do.join(' '), /khong chay JavaScript/);
});

test('gate 6 CALLOUT-BAKED do khi lop chu thich rong khong co chu', () => {
  const rong = `<svg><g class="annotations"><path d="M0,0 L10,10"/></g></svg>`;
  assert.equal(gateCalloutBaked({ html: rong }).trang_thai, 'FAIL');
});

test('gate 7 STYLE do voi em-dash, AI-slop va cau ket cach ngon', () => {
  assert.equal(gateVanPhong({ html: '<p>Giá than tăng 10% trong bốn tuần.</p>' }).trang_thai, 'PASS');
  assert.equal(gateVanPhong({ html: '<p>Giá than tăng 10% — rất mạnh.</p>' }).trang_thai, 'FAIL');
  assert.equal(gateVanPhong({ html: '<p>Tóm lại, ngành vẫn khó.</p>' }).trang_thai, 'FAIL');
});

test('gate 7 STYLE khong dinh em-dash nam trong CSS hay script', () => {
  const html = '<style>/* ghi chu — khong hien thi */</style><p>Nội dung sạch.</p>';
  assert.equal(gateVanPhong({ html }).trang_thai, 'PASS');
});

test('gate 8 PAGEBREAK do khi PDF co the bi cat dung bien trang', () => {
  const cssCoBaoVe = '<style>.hinh{break-inside:avoid;}</style>';
  assert.equal(gateNgatTrang({ html: cssCoBaoVe, pdf: pdfMau() }).trang_thai, 'PASS');
  const biCat = pdfMau({ ngat_trang: { the_bi_cat: [{ trang_a: 2, trang_b: 3, mau: [1, 1, 1] }], so_lan: 1 } });
  assert.equal(gateNgatTrang({ html: cssCoBaoVe, pdf: biCat }).trang_thai, 'FAIL');
});

test('gate 8 PAGEBREAK canh bao khi CSS khong co co che bao ve nao', () => {
  const kq = gateNgatTrang({ html: '<style>p{margin:0}</style>', pdf: pdfMau() });
  assert.equal(kq.trang_thai, 'WARN');
});

test('gate 9 SOURCE-LEAK phan biet ban sach voi ban lo ten rieng', () => {
  assert.equal(gateRoRiNguon({ duongDanHtml: path.join(FIX, 'nguon-xanh.html'), cheDo: 'gui-di' }).trang_thai, 'PASS');
  assert.equal(gateRoRiNguon({ duongDanHtml: path.join(FIX, 'nguon-do.html'), cheDo: 'gui-di' }).trang_thai, 'FAIL');
});

test('gate 10 LEDGER phan biet so nguon hop le voi so nguon mo coi va lech bac', () => {
  const fXanh = path.join(FIX, 'ledger-xanh.html');
  const fDo = path.join(FIX, 'ledger-do.html');
  const htmlXanh = fs.readFileSync(fXanh, 'utf-8');
  const htmlDo = fs.readFileSync(fDo, 'utf-8');

  assert.equal(gateSoNguon({ html: htmlXanh, duongDanHtml: fXanh, cheDo: 'noi-bo' }).trang_thai, 'PASS');
  const kq = gateSoNguon({ html: htmlDo, duongDanHtml: fDo, cheDo: 'noi-bo' });
  assert.equal(kq.trang_thai, 'FAIL');
  assert.match(kq.ly_do.join(' '), /orphan-value|tier-drift/);
});

test('gate 10 LEDGER do khi ban noi bo thieu han so nguon', () => {
  const html = '<p>Không có sổ nguồn</p>';
  assert.equal(gateSoNguon({ html, duongDanHtml: 'khong-can-doc', cheDo: 'noi-bo' }).trang_thai, 'FAIL');
  assert.equal(gateSoNguon({ html, duongDanHtml: 'khong-can-doc', cheDo: 'gui-di' }).trang_thai, 'SKIP');
});

// --------------------------------------------------------------------------- //
test('tachSvg lay dung ma hinh va khong bo sot SVG ngoai figure', () => {
  const html = boc(SVG_HOP_LE, 'hinh-a') + '<svg xmlns="http://www.w3.org/2000/svg"><text>logo</text></svg>';
  const ra = tachSvg(html);
  assert.equal(ra.length, 2);
  assert.equal(ra[0].maHinh, 'hinh-a');
  assert.equal(ra[1].maHinh, null);
});

test('boTrang bo moi khoang trang de doi chieu duoc chuoi trich tu PDF', () => {
  // Trich text tu PDF nuot khoang trang giua cac glyph sat nhau: "475 TY USD" ra
  // thanh "475TYUSD". So nguyen van se bao thieu mot chuoi dang co that tren giay.
  assert.equal(boTrang('475 TỶ USD'), boTrang('475TỶUSD'));
});
