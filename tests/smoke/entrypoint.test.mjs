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

test('SKILL.md ngan, chi dinh tuyen', () => {
  const s = readFileSync(path.join(ROOT, 'SKILL.md'), 'utf8');
  assert.ok(
    s.length < 12000,
    `SKILL.md dai ${s.length} ky tu. No chi duoc dinh tuyen, khong nhoi noi dung. ` +
      `design-taste-frontend nhoi 88KB vao mot file va moi lan goi la nuot het.`,
  );
});

test('moi duong dan SKILL.md tro toi deu ton tai', () => {
  const s = readFileSync(path.join(ROOT, 'SKILL.md'), 'utf8');
  // Regex mo bang [A-Za-z] chu khong phai [a-z]: ban cu bo qua MOI duong dan
  // bat dau bang chu hoa, tuc bo qua dung hai file quan trong nhat ma SKILL.md
  // tro toi la `CLAUDE.md` va `README.md`. Hai cai do chua bao gio duoc kiem,
  // gate xanh suot Phase 1 ma khong cham vao chung.
  const refs = [...s.matchAll(/`([A-Za-z][\w./-]+\.(?:md|css|py|mjs|js|json|html))`/g)].map(
    (m) => m[1],
  );
  assert.ok(refs.length > 0, 'khong trich duoc duong dan nao tu SKILL.md, regex hong');
  assert.ok(
    refs.includes('CLAUDE.md'),
    `regex khong bat duoc CLAUDE.md, ma SKILL.md co tro toi no. Bat duoc: ${refs.join(', ')}`,
  );
  const missing = refs.filter((r) => !existsSync(path.join(ROOT, r)));
  assert.deepEqual(missing, [], `SKILL.md tro toi file khong ton tai: ${missing.join(', ')}`);
});

test('README.md liet ke lenh cai dat va lenh verify', () => {
  const s = readFileSync(path.join(ROOT, 'README.md'), 'utf8');
  assert.match(s, /npm install/, 'README thieu lenh cai dat Node');
  assert.match(s, /pip install|requirements\.txt/, 'README thieu lenh cai dat Python');
  assert.match(s, /npm run verify/, 'README thieu lenh verify');
});
