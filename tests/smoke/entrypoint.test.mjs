import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('SKILL.md co frontmatter dung dinh dang', () => {
  const s = readFileSync(path.join(ROOT, 'SKILL.md'), 'utf8');
  assert.match(s, /^---\nname:\s*HT-viz-rendering\n/, 'frontmatter thieu hoac sai ten');
  assert.match(s, /^description:\s*.+$/m, 'frontmatter thieu description');
});

// TEST "SKILL.md phai ngan duoi 12KB" DA BO ngay 09-08. Ghi lai day du de nguoi sau
// khong khoi phuc lai ma khong biet vi sao no bi bo.
//
// Ly le cu: SKILL.md nap vao context moi lan goi skill, nen no phai ngan, chi dinh tuyen.
// Ly le do do CHI PHI SAI vi no chi dem phan nap tu dong ma bo qua phan phai doc them:
// ban 4,3KB cu khong tu du, agent phai mo tiep CLAUDE.md 26KB va catalog 37KB moi lam duoc
// mot an pham, tuc tong that vuot 60KB. Ban tu du 19,4KB re hon han.
//
// Dieu kien de dat lai mot nguong do dai: khi SKILL.md bat dau mang phan TRA CUU (bang
// tra, danh sach tai san, vi du dai) thay vi phan QUYET DINH. Luc do van de khong phai
// do dai ma la sai tang, va cach sua la chuyen sang doctrine/ chu khong phai cat bot chu.
//
// Nguoi dung chot bo han thay vi noi nguong: do dai la viec cua nguoi viet, khong phai
// viec cua gate. Ba phep do con lai trong tests/consistency/skill_khong_lac_hau.test.mjs
// van giu SKILL.md khoi noi sai ve repo.

// Phep kiem duong dan da chuyen sang tests/consistency/skill_khong_lac_hau.test.mjs, noi
// no kiem duoc ca duong dan THU MUC chu khong chi file co duoi. Ban o day tung bo qua moi
// duong dan bat dau bang chu hoa, tuc bo qua dung hai file quan trong nhat la CLAUDE.md va
// README.md; bay do nay duoc giu lai thanh mot phep do rieng trong file moi.

test('README.md liet ke lenh cai dat va lenh verify', () => {
  const s = readFileSync(path.join(ROOT, 'README.md'), 'utf8');
  assert.match(s, /npm install/, 'README thieu lenh cai dat Node');
  assert.match(s, /pip install|requirements\.txt/, 'README thieu lenh cai dat Python');
  assert.match(s, /npm run verify/, 'README thieu lenh verify');
});
