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

// Trich dung ma khoa CAP MOT cua khoi "TONES = { ... }" trong annotate.js.
// Khong dung regex danh sach den (dang bat 3 ten xau nghi truoc) vi no chi
// chan duoc nhung ten da nghi ra, bo lot moi ten moi (vd "good", "warn").
// Thay vao do quet can bang dau ngoac { } de tim dung khoi TONES, roi tach
// top-level theo dau phay o do sau 0 (bo qua dau phay/ngoac ben trong tung
// object con nhu { line, text, border, bg }), chi lay khoa CAP MOT. Nhan ca
// khoa bareword (neutral:) lan khoa co nhay ('neutral':, "neutral":).
function extractToneKeys(source) {
  const start = source.match(/TONES\s*=\s*\{/);
  if (!start) {
    throw new Error('khong tim thay khai bao "TONES = {" trong annotate.js');
  }
  let i = start.index + start[0].length;
  let depth = 1;
  const blockStart = i;
  while (depth > 0 && i < source.length) {
    if (source[i] === '{') depth += 1;
    else if (source[i] === '}') depth -= 1;
    i += 1;
  }
  const blockContent = source.slice(blockStart, i - 1);

  const entries = [];
  let entryStart = 0;
  let d = 0;
  for (let j = 0; j < blockContent.length; j += 1) {
    const ch = blockContent[j];
    if (ch === '{' || ch === '(' || ch === '[') d += 1;
    else if (ch === '}' || ch === ')' || ch === ']') d -= 1;
    else if (ch === ',' && d === 0) {
      entries.push(blockContent.slice(entryStart, j));
      entryStart = j + 1;
    }
  }
  entries.push(blockContent.slice(entryStart));

  const keys = [];
  for (const entry of entries) {
    const m = entry.match(/^\s*(?:['"`])?([A-Za-z_$][A-Za-z0-9_$]*)(?:['"`])?\s*:/);
    if (m) keys.push(m[1]);
  }
  return keys;
}

test('TONES trong annotate.js dung bang {neutral, negative, accent}, khong thua khong thieu', () => {
  const js = readFileSync(path.join(ROOT, 'illustrations/annotate.js'), 'utf8');
  const keys = extractToneKeys(js);
  assert.deepEqual(
    [...keys].sort(),
    ['accent', 'negative', 'neutral'],
    `TONES co khoa ${JSON.stringify(keys)}, phai dung bang {neutral, negative, accent}, khong duoc them ten moi`,
  );
});

test('verify-illustrations.mjs tra exit 0', () => {
  const out = execFileSync('node', [path.join(ROOT, 'scripts/verify-illustrations.mjs')], {
    cwd: ROOT,
    encoding: 'utf8',
    timeout: 180000,
  });
  assert.doesNotMatch(out, /\[FAIL\]/, `co gate FAIL:\n${out}`);
});
