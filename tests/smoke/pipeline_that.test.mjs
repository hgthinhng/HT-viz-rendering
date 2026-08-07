/**
 * pipeline_that.test.mjs — chay duong ong THAT tren bao cao mau, roi chay ca bo gate.
 *
 * Bo test gate do va gate xanh o tests/consistency/ kiem LOGIC cua tung gate bang du
 * lieu tong hop. No khong kiem duoc mot thu: cau truc JSON ma `gates/pdf_checks.py`
 * sinh ra co con khop voi thu ma gate mong doi khong. Doi ten mot khoa o phia Python
 * thi moi gate se doc `undefined` va van bao xanh, dung kieu gate rong ma repo nay da
 * dinh ba lan.
 *
 * Test nay giu dung rang buoc do. No dat hon cac test khac (dung WeasyPrint that) nen
 * chi chay MOT lan tren MOT bao cao, va co y khong chay lai buoc sinh hinh: SVG cua bao
 * cao mau da nam trong repo.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { chayTatCa } from '../../gates/gates.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const NGUON = path.join(GOC, 'examples/mau-phase2/noi-dung.md');

function dungBanThat(cheDo) {
  const tam = fs.mkdtempSync(path.join(os.tmpdir(), 'htviz-'));
  const html = path.join(tam, `mau-${cheDo}.html`);
  const pdf = path.join(tam, `mau-${cheDo}.pdf`);
  execFileSync('python3', [path.join(GOC, 'pipeline/build_html.py'), NGUON, html, `--che-do=${cheDo}`], {
    cwd: GOC, stdio: 'pipe',
  });
  execFileSync('python3', [path.join(GOC, 'pipeline/render_pdf.py'), html, pdf], {
    cwd: GOC, stdio: 'pipe',
  });
  return { tam, html, pdf };
}

test('duong ong that: ban noi bo qua duoc ca muoi gate', () => {
  const { tam, html, pdf } = dungBanThat('noi-bo');
  try {
    const ketQua = chayTatCa({ duongDanHtml: html, duongDanPdf: pdf, cheDo: 'noi-bo' });
    assert.equal(ketQua.length, 10, 'phai co du muoi gate');
    const fail = ketQua.filter((g) => g.trang_thai === 'FAIL');
    assert.deepEqual(
      fail.map((g) => `${g.ten}: ${g.ly_do[0]}`),
      [],
      'khong gate nao duoc FAIL tren bao cao mau'
    );
    // Gate nao cung phai tra ve mot trang thai hop le, khong duoc undefined am tham.
    for (const g of ketQua) {
      assert.ok(['PASS', 'WARN', 'FAIL', 'SKIP'].includes(g.trang_thai), `${g.ten} tra ve trang thai la`);
      assert.ok(g.ly_do.length > 0, `${g.ten} phai neu ly do, ke ca khi PASS`);
    }
  } finally {
    fs.rmSync(tam, { recursive: true, force: true });
  }
});

test('duong ong that: ban gui di KHONG mang so nguon va KHONG lo nguon noi bo', () => {
  const { tam, html, pdf } = dungBanThat('gui-di');
  try {
    const noiDung = fs.readFileSync(html, 'utf-8');
    assert.ok(!/id="evidence-ledger"/.test(noiDung), 'ban gui di khong duoc nhung so nguon');
    assert.ok(
      !noiDung.includes('bản nháp chưa soát xét'),
      'trich dan that cua nguon internal_only khong duoc lot vao ban gui di'
    );
    assert.ok(
      noiDung.includes('ước tính trên dữ liệu đã công bố'),
      'ban gui di phai hien nhan quy doi cua nguon internal_only'
    );

    const ketQua = chayTatCa({ duongDanHtml: html, duongDanPdf: pdf, cheDo: 'gui-di' });
    const fail = ketQua.filter((g) => g.trang_thai === 'FAIL');
    assert.deepEqual(fail.map((g) => g.ten), [], 'khong gate nao duoc FAIL tren ban gui di');
    const ledger = ketQua.find((g) => g.ten.includes('LEDGER'));
    assert.equal(ledger.trang_thai, 'SKIP', 'ban gui di khong co so nguon nen gate LEDGER phai SKIP co ly do');
  } finally {
    fs.rmSync(tam, { recursive: true, force: true });
  }
});

test('pdf_checks.py tra ve du moi khoa ma gate doc', () => {
  // Rang buoc chong troi giua hai ngon ngu: doi ten khoa o phia Python ma quen phia
  // Node thi gate doc undefined va van bao xanh.
  const { tam, pdf } = dungBanThat('noi-bo');
  try {
    const ra = JSON.parse(
      execFileSync('python3', [path.join(GOC, 'gates/pdf_checks.py'), pdf], { maxBuffer: 1 << 27 }).toString()
    );
    for (const khoa of ['so_trang', 'kich_thuoc_byte', 'byte_moi_trang', 'net_ve_tong', 'text_bo_trang']) {
      assert.ok(khoa in ra, `thieu khoa ${khoa}`);
    }
    assert.ok('ho_font' in ra.font, 'thieu font.ho_font');
    for (const khoa of ['so_object', 'anh_toan_panel']) assert.ok(khoa in ra.raster, `thieu raster.${khoa}`);
    for (const khoa of ['fffd', 'dau_tong', 'dau_synthetic', 'synthetic_khoang_trang']) {
      assert.ok(khoa in ra.dau, `thieu dau.${khoa}`);
    }
    for (const khoa of ['the_bi_cat', 'so_lan']) assert.ok(khoa in ra.ngat_trang, `thieu ngat_trang.${khoa}`);
  } finally {
    fs.rmSync(tam, { recursive: true, force: true });
  }
});
