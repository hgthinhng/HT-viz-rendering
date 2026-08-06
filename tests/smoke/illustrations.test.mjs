import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const SVG_DIR = path.join(ROOT, 'illustrations/svg');

test('co du 11 minh hoa', () => {
  const files = readdirSync(SVG_DIR).filter((f) => f.endsWith('.svg'));
  assert.equal(files.length, 11, `co ${files.length} SVG, mong doi 11`);
});

test('khong SVG nao vi pham lenh cam', () => {
  const files = readdirSync(SVG_DIR).filter((f) => f.endsWith('.svg'));
  for (const f of files) {
    const s = readFileSync(path.join(SVG_DIR, f), 'utf8');
    assert.doesNotMatch(s, /<filter/, `${f} co <filter>, se raster hoa khi in`);
    assert.doesNotMatch(s, /<linearGradient|<radialGradient/, `${f} co gradient`);
    assert.doesNotMatch(s, /<image/, `${f} nhung anh raster`);
    assert.doesNotMatch(s, /<clipPath[\s\S]*<clipPath/, `${f} co clipPath long nhau`);
  }
});

test('moi SVG co role img va title tieng Viet', () => {
  const files = readdirSync(SVG_DIR).filter((f) => f.endsWith('.svg'));
  for (const f of files) {
    const s = readFileSync(path.join(SVG_DIR, f), 'utf8');
    assert.match(s, /role\s*=\s*"img"/, `${f} thieu role="img"`);
    assert.match(s, /<title>/, `${f} thieu <title>`);
    assert.match(s, /viewBox\s*=/, `${f} thieu viewBox`);
  }
});

test('annotate.js chi cho 3 gia tri tone', () => {
  const js = readFileSync(path.join(ROOT, 'illustrations/annotate.js'), 'utf8');
  for (const bad of ['good', 'warn', 'bad']) {
    assert.doesNotMatch(
      js,
      new RegExp(`['"\`]${bad}['"\`]\\s*:`),
      `annotate.js con tone "${bad}", chi duoc neutral/negative/accent`,
    );
  }
});

test('verify-illustrations.mjs tra exit 0', () => {
  const out = execFileSync('node', [path.join(ROOT, 'scripts/verify-illustrations.mjs')], {
    cwd: ROOT,
    encoding: 'utf8',
    timeout: 180000,
  });
  assert.doesNotMatch(out, /\[FAIL\]/, `co gate FAIL:\n${out}`);
});
