import { test } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

// Chay generator VAO BO NHO (import ham thuan tuy, khong spawn subprocess, khong ghi
// dia) roi so voi noi dung THAT dang nam tren ba file dich. Day la ban sinh doi cua
// che do --kiem trong design-system/generate-tokens.mjs, nhung chay nhu mot test binh
// thuong trong `npm test` thay vi phai nho goi rieng mot lenh CLI.
//
// Neu test nay do: mot trong ba file (tokens.css, tokens.py, theme.mjs) da bi sua tay
// trong vung marker THEME-TOKENS, hoac file JSON o design-system/themes/ da doi ma
// chua chay lai generator. Sua bang: node design-system/generate-tokens.mjs
test('ba dich (tokens.css, tokens.py, theme.mjs) khong troi khoi design-system/themes/*.json', async () => {
  const { docTatCaChuDe, CAU_HINH_DICH, tinhNoiDungMoi } = await import(
    path.join(ROOT, 'design-system/generate-tokens.mjs')
  );

  const dsChuDe = docTatCaChuDe();
  assert.ok(dsChuDe.length >= 1, 'phai doc duoc it nhat mot chu de tu design-system/themes/*.json');

  const lech = [];
  for (const muc of CAU_HINH_DICH) {
    const { noiDungCu, noiDungMoi } = tinhNoiDungMoi(muc, dsChuDe);
    if (noiDungCu !== noiDungMoi) lech.push(muc.ten);
  }
  assert.deepEqual(
    lech,
    [],
    `cac file sau da troi khoi design-system/themes/*.json, chay lai ` +
      `node design-system/generate-tokens.mjs: ${lech.join(', ')}`,
  );
});

// Bang chung gate PHAN BIET DUOC hai trang thai, khong phai phep do rong: dua vao
// mot noi dung file GIA (mot ky tu hex bi sua) roi xac nhan ham so sanh bao LECH that.
// Khong doc/ghi dia that trong test nay, chi kiem chinh logic apDungKhoi + so sanh.
test('gate nay PHAN BIET DUOC hai trang thai: fixture lech phai bi bat', async () => {
  const { docTatCaChuDe, sinhThanCss, apDungKhoi } = await import(
    path.join(ROOT, 'design-system/generate-tokens.mjs')
  );
  const dsChuDe = docTatCaChuDe();
  const thanDung = sinhThanCss(dsChuDe);

  const moMarker = '/* THEME-TOKENS:BAT-DAU */';
  const ketMarker = '/* THEME-TOKENS:KET-THUC */';
  const fileGoc = `:root { --khac: #000000; }\n\n${moMarker}\n${thanDung}\n${ketMarker}\n`;

  // Trang thai XANH: ghep dung than sinh ra, phai khop chinh no.
  const ghepDung = apDungKhoi(fileGoc, moMarker, ketMarker, thanDung, '/* header gia */');
  assert.equal(ghepDung, fileGoc, 'ghep lai voi than dung phai tra ve dung noi dung ban dau');

  // Trang thai DO: pha mot ky tu hex trong than roi ghep lai, phai KHAC fileGoc.
  const thanHong = thanDung.replace('#2251FF', '#000000');
  assert.notEqual(thanHong, thanDung, 'fixture pha hong phai thuc su khac ban dung, neu khong phep thu nay vo nghia');
  const ghepHong = apDungKhoi(fileGoc, moMarker, ketMarker, thanHong, '/* header gia */');
  assert.notEqual(ghepHong, fileGoc, 'ghep voi than da pha hong PHAI khac noi dung dung, neu khong gate nay mu');
});
