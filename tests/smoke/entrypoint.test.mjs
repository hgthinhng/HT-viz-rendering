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
  const refs = [...s.matchAll(/`([a-z][\w./-]+\.(?:md|css|py|mjs|js|json|html))`/g)].map(
    (m) => m[1],
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
