// anh_moc.test.mjs, visual regression cho sau preset dai dien.
//
// Ba phep do, va thu tu quan trong: phep do 2 la dieu kien de phep do 1 co nghia gi.
//   1. Anh hien tai khop anh moc trong repo.
//   2. Phep do TAT DINH: chup cung mot preset hai lan lien tiep phai cho 0 pixel khac.
//      Mot gate visual regression khong tat dinh la mot gate do ngau nhien, va no se bi
//      tat sau vai lan do oan. Khang dinh bang so chu khong bang niem tin.
//   3. Nguong DU CHAT de bat duoc thay doi that. Con so 0,05% khong phai cam giac: no
//      den tu mutation. Doi mot nhan tu `120` sang `120,00` lam 0,242% pixel khac, nen
//      nguong 0,3% ban dau LOT QUA, gate xanh trong khi hinh da doi.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { kiemTraChromium } from '../../scripts/lib/chromium.mjs';
import { doAnhMoc, doTinhTatDinh, MUC_TIEU, THU_MUC_MOC } from '../../scripts/anh-moc.mjs';

const co_chromium = kiemTraChromium().ok;
const bo_qua = !co_chromium && 'chua co Chromium, chay npm run setup:browser';

test('du sau anh moc trong repo, khong thieu cai nao', () => {
  const thieu = MUC_TIEU.filter((m) => !existsSync(path.join(THU_MUC_MOC, `${m.ten}.png`)));
  assert.deepEqual(
    thieu.map((m) => m.ten),
    [],
    'thieu anh moc. Sinh bang: node scripts/anh-moc.mjs --cap-nhat',
  );
});

test('sau preset dai dien khop anh moc tung pixel', { timeout: 180000, skip: bo_qua }, async () => {
  const ket = await doAnhMoc();
  const lech = ket.filter((r) => r.trangThai === 'LECH');
  assert.deepEqual(
    lech.map((r) => `${r.ten}: ${r.ly_do}`),
    [],
    'hinh doi so voi anh moc. Neu doi la CO Y thi mo anh ra xem roi chay ' +
      '`node scripts/anh-moc.mjs --cap-nhat`, dung cap nhat theo phan xa',
  );
  assert.equal(ket.length, MUC_TIEU.length);
});

test('phep do TAT DINH: chup hai lan cung mot preset cho 0 pixel khac', { timeout: 120000, skip: bo_qua }, async () => {
  const d = await doTinhTatDinh('13-line-annotated');
  assert.ok(!d.kichThuocLech, `kich thuoc doi giua hai lan chup: ${d.kichThuocLech}`);
  assert.equal(
    d.khac,
    0,
    `chup hai lan cho ${d.khac} pixel khac, tuc phep do co thanh phan ngau nhien. ` +
      'Mot gate visual regression khong tat dinh se do oan roi bi tat.',
  );
});
