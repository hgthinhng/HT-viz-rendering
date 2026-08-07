/**
 * em_dash_repo.test.mjs, chan em-dash va en-dash tai pham tren TOAN repo.
 *
 * Truoc dot don 07-08, luat cua repo la "cam trong noi dung hien thi, cho phep trong
 * comment ma nguon". Ranh gioi mo do phai tra gia hai lan:
 *
 *   1. No de lai 514 dau gach ngang nam rai trong tai lieu va comment, va den mot luc
 *      phai don hang loat.
 *   2. Chinh dot don hang loat do da doi hai ky tu nam BEN TRONG character class cua
 *      hai gate chan em-dash, bien chung thanh `[--]`. Regex do chi con khop dau gach
 *      noi thuong: gate bao FAIL cho moi noi dung binh thuong va khong con bat em-dash,
 *      ma van chay tron tru khong bao gi.
 *
 * Nen luat nay chuyen thanh tuyet doi: repo chinh khong chua hai ky tu do o bat ky dau,
 * ke ca trong comment. Ranh gioi tuyet doi thi khong con cho de troi.
 *
 * Regex o day viet bang ESCAPE, khong dan ky tu, de mot dot don ve sau khong the vo
 * hieu hoa chinh gate nay.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const GACH_NGANG = /[\u2014\u2013]/g;

// `_harvest/` la khu tam chua tai san goc chua do, giu nguyen ban goc de con doi chieu.
// `gate_do_xanh.test.mjs` mang fixture DO cua gate STYLE: no PHAI chua em-dash, neu
// khong thi khong con bang chung nao rang gate do do duoc.
const MIEN_TRU = [
  /^_harvest\//,
  /^tests\/consistency\/gate_do_xanh\.test\.mjs$/,
];

const DUOI_KIEM = new Set(['.html', '.md', '.css', '.js', '.mjs', '.py', '.json', '.svg', '.txt']);

function fileCanKiem() {
  return execFileSync('git', ['ls-files'], { cwd: GOC, encoding: 'utf-8' })
    .split('\n')
    .filter(Boolean)
    .filter((f) => DUOI_KIEM.has(path.extname(f)))
    .filter((f) => !MIEN_TRU.some((re) => re.test(f)));
}

test('khong file nao trong repo chinh con em-dash hoac en-dash', () => {
  const pham = [];
  for (const f of fileCanKiem()) {
    const s = readFileSync(path.join(GOC, f), 'utf-8');
    const hit = s.match(GACH_NGANG);
    if (hit) pham.push(`${f}: ${hit.length}`);
  }
  assert.deepEqual(pham, [], `co file con em-dash hoac en-dash:\n  ${pham.join('\n  ')}`);
});

test('gate nay PHAN BIET DUOC hai trang thai, khong phai phep do rong', () => {
  // Bang chung gate khong rong: cho no mot chuoi co em-dash va mot chuoi sach.
  assert.equal('mot hai'.match(GACH_NGANG), null, 'chuoi sach phai khong khop');
  assert.equal('mot \u2014 hai'.match(GACH_NGANG).length, 1, 'em-dash phai khop');
  assert.equal('mot \u2013 hai'.match(GACH_NGANG).length, 1, 'en-dash phai khop');
  assert.equal('mot - hai'.match(GACH_NGANG), null, 'dau gach noi thuong KHONG duoc khop');
});

test('danh sach file can kiem khong rong, neu khong gate tren la phep do rong', () => {
  // Bay da dinh that o Phase 1: mot gate dung `.every(Boolean)` tren mang rong nen
  // luon xanh. Mot vong lap tren danh sach rong cung xanh y het.
  const ds = fileCanKiem();
  assert.ok(ds.length > 50, `chi tim thay ${ds.length} file, nghi ngo lenh git ls-files hong`);
  assert.ok(ds.includes('CLAUDE.md'), 'phai kiem ca CLAUDE.md');
  assert.ok(
    ds.some((f) => f.startsWith('components/catalog/')),
    'phai kiem ca catalog component'
  );
});

test('fixture do cua gate STYLE van con em-dash, neu khong gate do het do duoc', () => {
  // Gate nay mien tru file fixture. Neu ai do "don sach" luon file do thi gate STYLE
  // mat bang chung duy nhat rang no phan biet duoc hai trang thai, va khong ai biet.
  const s = readFileSync(path.join(GOC, 'tests/consistency/gate_do_xanh.test.mjs'), 'utf-8');
  assert.ok(s.match(GACH_NGANG), 'fixture do phai giu em-dash, day la co y chu khong phai sot');
});
