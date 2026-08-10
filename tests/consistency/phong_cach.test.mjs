import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validatePhongCach, validateGioiHanChoChuDeToi, BAY_LOAI_AN_PHAM, RE_MAU_LITERAL } from '../../phong-cach/schema.mjs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PC = path.join(REPO, 'phong-cach');
const FX = path.join(REPO, 'tests', 'fixtures', 'phong-cach');

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
