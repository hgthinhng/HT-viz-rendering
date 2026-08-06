import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('gallery.html ton tai va tro dung tokens.css', () => {
  const p = path.join(ROOT, 'components/gallery.html');
  assert.ok(existsSync(p), 'thieu components/gallery.html');
  const html = readFileSync(p, 'utf8');
  assert.match(html, /design-system\/tokens\.css/, 'gallery khong nap tokens.css tu design-system');
  assert.match(html, /fonts-embedded\.css/, 'gallery khong nap font nhung');
});

test('components.css khong con khoi token rieng', () => {
  const css = readFileSync(path.join(ROOT, 'components/components.css'), 'utf8');
  assert.doesNotMatch(css, /--accent\s*:\s*#/, 'components.css van tu khai bao --accent, phai lay tu tokens.css');
});

test('components.css khong vi pham lenh cam', () => {
  const css = readFileSync(path.join(ROOT, 'components/components.css'), 'utf8');
  assert.doesNotMatch(css, /filter\s*:\s*blur/, 'con filter: blur');
  assert.doesNotMatch(css, /backdrop-filter/, 'con backdrop-filter');
  const badMedia = css.match(/@media\s*\(\s*max-width/g) || [];
  assert.equal(badMedia.length, 0, `${badMedia.length} media query thieu "screen", se tu kich hoat khi in`);
});

test('verify-components.mjs chay va tra exit 0', () => {
  const out = execFileSync('node', [path.join(ROOT, 'scripts/verify-components.mjs')], {
    cwd: ROOT,
    encoding: 'utf8',
    timeout: 180000,
  });
  assert.match(out, /\[PASS\]/, 'khong thay dong PASS nao');
  assert.doesNotMatch(out, /\[FAIL\]/, `co gate FAIL:\n${out}`);
});
