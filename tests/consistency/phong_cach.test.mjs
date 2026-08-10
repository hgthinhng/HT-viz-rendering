import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { validatePhongCach, validateGioiHanChoChuDeToi, BAY_LOAI_AN_PHAM, RE_MAU_LITERAL } from '../../phong-cach/schema.mjs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PC = path.join(REPO, 'phong-cach');
const FX = path.join(REPO, 'tests', 'fixtures', 'phong-cach');
const CAM_PDF = ['aspect-ratio', 'writing-mode', 'backdrop-filter', 'filter:'];

function docJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
function danhSachChuDe() {
  return fs.readdirSync(path.join(REPO, 'design-system', 'themes'))
    .filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, ''));
}
function chuDeLaToi(ten) {
  // Chu de toi = paper co do sang thap. Doc truc tiep tu nguon.
  const t = docJson(path.join(REPO, 'design-system', 'themes', `${ten}.json`));
  const hex = t.mau.paper.replace('#', '');
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16));
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) < 96;
}
function cacStyle() {
  return fs.readdirSync(PC, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'fixtures')
    .map((d) => d.name);
}
function tachSelectors(css) {
  const sach = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const selectors = [];
  let buf = '';
  let depth = 0;
  for (let i = 0; i < sach.length; i++) {
    const ch = sach[i];
    if (ch === '{') {
      const dau = buf.trim();
      if (!dau.startsWith('@') && dau) {
        for (const s of dau.split(',')) { const t = s.trim(); if (t) selectors.push(t); }
      }
      depth += 1; buf = '';
    } else if (ch === '}') { depth -= 1; buf = ''; }
    else if (ch === ';') { buf = ''; }
    else { buf += ch; }
  }
  return selectors;
}

test('moi phong-cach.json qua schema', () => {
  const themes = danhSachChuDe();
  for (const slug of cacStyle()) {
    const obj = docJson(path.join(PC, slug, 'phong-cach.json'));
    const kq = validatePhongCach(obj, { tenThuMuc: slug, danhSachChuDe: themes });
    assert.deepEqual(kq.loi, [], `style ${slug}: ${kq.loi.join('; ')}`);
    const kq2 = validateGioiHanChoChuDeToi(obj, chuDeLaToi(obj.chu_de_mac_dinh));
    assert.deepEqual(kq2.loi, [], `style ${slug}: ${kq2.loi.join('; ')}`);
  }
});

test('fixture xanh PASS, ba fixture do FAIL dung cho', () => {
  const themes = danhSachChuDe();
  const xanh = docJson(path.join(FX, 'xanh', 'phong-cach.json'));
  assert.equal(validatePhongCach(xanh, { tenThuMuc: 'xanh', danhSachChuDe: themes }).hopLe, true);

  const thieu = docJson(path.join(FX, 'do-thieu-truong', 'phong-cach.json'));
  const kqThieu = validatePhongCach(thieu, { tenThuMuc: 'do-thieu-truong', danhSachChuDe: themes });
  assert.equal(kqThieu.hopLe, false);
  assert.ok(kqThieu.loi.some((l) => l.includes('chart_palette')), kqThieu.loi.join('; '));

  const mau = docJson(path.join(FX, 'do-mau-literal', 'phong-cach.json'));
  const kqMau = validatePhongCach(mau, { tenThuMuc: 'do-mau-literal', danhSachChuDe: themes });
  assert.equal(kqMau.hopLe, false);
  assert.ok(kqMau.loi.some((l) => l.includes('mau literal')), kqMau.loi.join('; '));

  const toi = docJson(path.join(FX, 'do-toi-khong-gioi-han', 'phong-cach.json'));
  const kqToi = validateGioiHanChoChuDeToi(toi, true);
  assert.equal(kqToi.hopLe, false);
});

test('RE_MAU_LITERAL khong bat var() va literal phi mau', () => {
  assert.equal(RE_MAU_LITERAL.test('var(--space-6)'), false);
  assert.equal(RE_MAU_LITERAL.test('2px'), false);
  assert.equal(RE_MAU_LITERAL.test('#2251FF'), true);
  assert.equal(RE_MAU_LITERAL.test('rgb(1, 2, 3)'), true);
  assert.equal(RE_MAU_LITERAL.test('color-mix(in srgb, red, blue)'), true);
});

test('BAY_LOAI_AN_PHAM co dung 7 slug khong dau', () => {
  assert.equal(BAY_LOAI_AN_PHAM.length, 7);
  for (const s of BAY_LOAI_AN_PHAM) assert.match(s, /^[a-z0-9-]+$/);
});

test('INDEX.json la ban sinh, khop nguon', async () => {
  const { tinhIndex } = await import('../../phong-cach/sinh-index.mjs');
  const tren_dia = docJson(path.join(PC, 'INDEX.json'));
  assert.deepEqual(tren_dia, tinhIndex(REPO), 'INDEX.json lech: chay node phong-cach/sinh-index.mjs');
});

test('entry chinh-thuc phai co lan_da_chung_minh', () => {
  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (e.trang_thai === 'chinh-thuc') {
      assert.ok(e.lan_da_chung_minh.length >= 1, `${e.slug} chinh-thuc ma khong co lan chung minh`);
      assert.ok(e.exemplar, `${e.slug} chinh-thuc ma khong co exemplar`);
    }
  }
});

test('tinhIndex ha cap chinh-thuc thanh vuon-uom khi exemplar thieu nghiem-thu.json', async () => {
  const { tinhIndex } = await import('../../phong-cach/sinh-index.mjs');
  const sandbox = fs.mkdtempSync(path.join(os.tmpdir(), 'phong-cach-test-'));
  try {
    // Dung sandbox: design-system/themes/sang-lanh.json, phong-cach/x/, examples/x/
    const themesDir = path.join(sandbox, 'design-system', 'themes');
    fs.mkdirSync(themesDir, { recursive: true });
    const sangLanhThuc = docJson(path.join(REPO, 'design-system', 'themes', 'sang-lanh.json'));
    fs.writeFileSync(path.join(themesDir, 'sang-lanh.json'), JSON.stringify(sangLanhThuc, null, 2) + '\n');

    const stylePath = path.join(sandbox, 'phong-cach', 'x', 'phong-cach.json');
    fs.mkdirSync(path.dirname(stylePath), { recursive: true });
    const stylePhongCach = {
      slug: 'x',
      tagline: 'Test style co trang thai chinh-thuc',
      mood: ['test'],
      formality: 'cao',
      density: 'cao',
      best_for: [],
      avoid_for: [],
      chu_de_mac_dinh: 'sang-lanh',
      gioi_han_loai_hinh: [],
      font: { kit: 'mac-dinh', hien_thi: 'Spectral', van_ban: 'Spectral', so_va_nhan: 'IBM Plex Mono' },
      token_override: {},
      chart_palette: 'sang-lanh',
      exemplar: 'examples/x',
      trang_thai: 'chinh-thuc',
    };
    fs.writeFileSync(stylePath, JSON.stringify(stylePhongCach, null, 2) + '\n');
    fs.mkdirSync(path.join(sandbox, 'examples', 'x'), { recursive: true });

    // Case do: exemplar thieu nghiem-thu.json, ha cap thanh vuon-uom
    let idx = tinhIndex(sandbox);
    const entryX = idx.danh_sach.find((e) => e.slug === 'x');
    assert.equal(entryX.trang_thai, 'vuon-uom', 'chinh-thuc phai ha cap khi thieu nghiem-thu.json');
    assert.deepEqual(entryX.lan_da_chung_minh, [], 'lan_da_chung_minh phai rong khi vo');

    // Case xanh: them nghiem-thu.json hop le, giu chinh-thuc
    const nghiemThu = {
      lan: 'html-song',
      gate: [
        { ten: 'FONT', ket_qua: 'PASS' },
        { ten: 'CHART', ket_qua: 'PASS' },
      ],
    };
    fs.writeFileSync(path.join(sandbox, 'examples', 'x', 'nghiem-thu.json'), JSON.stringify(nghiemThu, null, 2) + '\n');
    idx = tinhIndex(sandbox);
    const entryX2 = idx.danh_sach.find((e) => e.slug === 'x');
    assert.equal(entryX2.trang_thai, 'chinh-thuc', 'giu chinh-thuc khi co nghiem-thu.json hophanle');
    assert.deepEqual(entryX2.lan_da_chung_minh, ['html-song'], 'lan_da_chung_minh phai la ["html-song"]');

    // Case do thu ba: nghiem-thu.json co FAIL, ha cap lai
    const nghiemThuFail = {
      lan: 'html-song',
      gate: [
        { ten: 'FONT', ket_qua: 'PASS' },
        { ten: 'CHART', ket_qua: 'FAIL' },
      ],
    };
    fs.writeFileSync(path.join(sandbox, 'examples', 'x', 'nghiem-thu.json'), JSON.stringify(nghiemThuFail, null, 2) + '\n');
    idx = tinhIndex(sandbox);
    const entryX3 = idx.danh_sach.find((e) => e.slug === 'x');
    assert.equal(entryX3.trang_thai, 'vuon-uom', 'ha cap khi co FAIL trong gate');
    assert.deepEqual(entryX3.lan_da_chung_minh, [], 'lan_da_chung_minh phai rong khi co FAIL');
  } finally {
    fs.rmSync(sandbox, { recursive: true });
  }
});

test('lop.css theo contract: scope dung slug, khong mau literal', () => {
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'lop.css');
    if (!fs.existsSync(p)) continue;
    const css = fs.readFileSync(p, 'utf8');
    assert.equal(RE_MAU_LITERAL.test(css.replace(/\/\*[\s\S]*?\*\//g, '')), false, `${slug}/lop.css chua mau literal`);
    // Moi selector (ke ca trong @media) phai mang scope [data-phong-cach="slug"]
    const selectors = tachSelectors(css);
    for (const sel of selectors) {
      assert.ok(sel.includes(`[data-phong-cach="${slug}"]`),
        `${slug}/lop.css selector khong scope: ${sel}`);
    }
  }
});

test('tachSelectors bat duoc selector tran trong @media va nhanh phay khong scope', () => {
  const css = '@media screen and (max-width: 600px) { .naked { color: var(--ink); } }\n' +
    '[data-phong-cach="x"] .a, .b { margin: 0; }';
  const ket = tachSelectors(css);
  assert.ok(ket.includes('.naked'), 'phai thay selector trong @media');
  assert.ok(ket.includes('.b'), 'phai tach rieng nhanh phay');
  const viPham = ket.filter((s) => !s.includes('[data-phong-cach="x"]'));
  assert.deepEqual(viPham.sort(), ['.b', '.naked'], 'hai vi pham phai bi bat');
});

test('style co exemplar lan pdf-so: lop.css khong dung thuoc tinh WeasyPrint bo qua', () => {
  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (!e.lan_da_chung_minh.includes('pdf-so')) continue;
    const p = path.join(PC, e.slug, 'lop.css');
    if (!fs.existsSync(p)) continue;
    const sach = fs.readFileSync(p, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
    for (const cam of CAM_PDF) {
      assert.ok(!sach.includes(cam), `${e.slug}/lop.css dung ${cam}, WeasyPrint bo qua hoac pha`);
    }
  }
});

test('nghiem-thu.json cua exemplar khop registry gate hien hanh', async () => {
  const { TEN_GATES_PDF } = await import('../../gates/gates.mjs');
  const { TEN_GATES_SONG } = await import('../../gates/gates_song.mjs');

  // Neu vong lap ben duoi khong tim thay entry chinh-thuc nao (hien tai la vay,
  // xem phong-cach/INDEX.json), test se PASS RONG va khong chung minh gi. Ep hai
  // assert tinh o day de test luon kiem duoc mot dieu gi do that su, dung bai hoc
  // pass-rong da dinh o Task 2 va Task 3.
  assert.ok(TEN_GATES_PDF.length >= 10, `TEN_GATES_PDF phai co it nhat 10 gate, hien co ${TEN_GATES_PDF.length}`);
  assert.ok(TEN_GATES_SONG.length >= 9, `TEN_GATES_SONG phai co it nhat 9 gate, hien co ${TEN_GATES_SONG.length}`);
  assert.equal(new Set(TEN_GATES_PDF).size, TEN_GATES_PDF.length, 'TEN_GATES_PDF co ten trung nhau');
  assert.equal(new Set(TEN_GATES_SONG).size, TEN_GATES_SONG.length, 'TEN_GATES_SONG co ten trung nhau');

  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (e.trang_thai !== 'chinh-thuc') continue;
    const nt = docJson(path.join(REPO, e.exemplar, 'nghiem-thu.json'));
    const registry = nt.lan === 'html-song' ? TEN_GATES_SONG : TEN_GATES_PDF;
    assert.deepEqual(nt.gate.map((g) => g.ten), registry,
      `${e.slug}: tap gate trong nghiem-thu lech registry ${nt.lan}; chay lai npm run nghiem-thu`);
    for (const g of nt.gate) {
      assert.notEqual(g.ket_qua, 'FAIL', `${e.slug}: gate ${g.ten} FAIL trong nghiem-thu`);
      if (g.ket_qua === 'SKIP') assert.ok(g.ly_do, `${e.slug}: gate ${g.ten} SKIP khong ly do`);
    }
  }
});

test('design.md khong lap hex', () => {
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'design.md');
    if (!fs.existsSync(p)) continue;
    const md = fs.readFileSync(p, 'utf8');
    assert.equal(/#[0-9a-fA-F]{6}\b/.test(md), false, `${slug}/design.md chua hex, mau chi noi bang ten token`);
  }
});

test('design.md: tai san nhac bang backtick slug phai ton tai', () => {
  // catalog/INDEX.json hinh dang that (kiem truoc khi viet test nay): object voi
  // khoa `muc`, moi phan tu la { ma, nhom, ten, ... }. `ma` la slug that su, vi du
  // '01-waterfall' hay '13-line-annotated'. Khong phai mang tran, khong phai
  // `tai_san`/`danh_sach`.
  const catalog = docJson(path.join(REPO, 'catalog', 'INDEX.json'));
  const coThat = new Set(
    (Array.isArray(catalog) ? catalog : catalog.muc || catalog.tai_san || catalog.danh_sach || [])
      .map((t) => t.ma || t.slug || t.id).filter(Boolean),
  );
  // San chan parse rong gia: catalog that co 116 tai san, ngo qua 50 la an toan.
  assert.ok(coThat.size > 50, `catalog/INDEX.json ve chi ${coThat.size} slug, co the parse sai hinh dang`);
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'design.md');
    if (!fs.existsSync(p)) continue;
    const md = fs.readFileSync(p, 'utf8');
    // Chi soat cac backtick co dang slug tai san (bat dau bang so)
    const refs = [...md.matchAll(/`([0-9][0-9a-z-]+)`/g)].map((m) => m[1]);
    for (const r of refs) {
      assert.ok(coThat.has(r), `${slug}/design.md nhac tai san khong ton tai: ${r}`);
    }
  }
});
