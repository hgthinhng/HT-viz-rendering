import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const CATALOG = path.join(ROOT, 'components/catalog');
const CSS = readFileSync(path.join(ROOT, 'components/components.css'), 'utf8');
const JS = readFileSync(path.join(ROOT, 'components/components.js'), 'utf8');

// Sieet: bo comment /* ... */ truoc khi quet, va chi nhan class o vi tri
// selector (doan van ban ngay truoc moi dau "{", tru phan sau dau ";" cuoi
// cung trong doan do). Ban nguyen van (khong bo comment, quet ca file) de
// lot ".css" (tu chuoi "@import url(...tokens.css)"), ".py" (tu comment
// nhac "render_engine.py"), ".xref_object" (tu comment nhac "doc.xref_object")
// vao definedClasses - ba token nay khong phai class CSS that.
const CSS_NO_COMMENTS = CSS.replace(/\/\*[\s\S]*?\*\//g, '');
const definedClasses = new Set();
for (const m of CSS_NO_COMMENTS.matchAll(/([^{}]*)\{/g)) {
  let selectorText = m[1];
  const lastSemi = selectorText.lastIndexOf(';');
  if (lastSemi !== -1) selectorText = selectorText.slice(lastSemi + 1);
  for (const cm of selectorText.matchAll(/\.([a-zA-Z][\w-]*)/g)) {
    definedClasses.add(cm[1]);
  }
}

// wc-plaque-layer la mot ngoai le that: components.js dong 50 doc no bang
// querySelector(".wc-plaque-layer") va se am tham bo qua ca buildWallChart
// (return som o dong 52) neu thieu, nhung ban than no khong co rule CSS nao
// vi la container thuan JS (JS tu set style.position="relative" luc chay,
// khong can style tinh). Day la class THAT, dung trong ca gallery.html that,
// khong phai catalog drift - chi la CSS khong phai nguon that duy nhat. Gop
// them cac class ma components.js thao tac truc tiep qua querySelector/
// className lam nguon that thu hai, thay vi xoa no khoi catalog hoac bia
// them mot rule CSS khong co tac dung.
for (const m of JS.matchAll(/querySelector(?:All)?\(\s*["'`]\.([a-zA-Z][\w-]*)["'`]\s*\)/g)) {
  definedClasses.add(m[1]);
}
for (const m of JS.matchAll(/className\s*=\s*["'`]([^"'`]+)["'`]/g)) {
  for (const c of m[1].split(/\s+/).filter(Boolean)) definedClasses.add(c);
}

const catalogFiles = readdirSync(CATALOG).filter((f) => f.endsWith('.md'));

test('co du 24 file catalog', () => {
  assert.equal(catalogFiles.length, 24, `co ${catalogFiles.length} file, mong doi 24`);
});

for (const file of catalogFiles) {
  test(`catalog ${file}: moi class trong vi du deu ton tai trong CSS`, () => {
    const md = readFileSync(path.join(CATALOG, file), 'utf8');
    const blocks = [...md.matchAll(/```html\n([\s\S]*?)```/g)].map((m) => m[1]);
    assert.ok(blocks.length > 0, `${file} khong co khoi code html nao`);

    const used = new Set();
    for (const b of blocks) {
      for (const m of b.matchAll(/class\s*=\s*"([^"]+)"/g)) {
        for (const c of m[1].split(/\s+/).filter(Boolean)) used.add(c);
      }
    }
    assert.ok(used.size > 0, `${file} khong dung class nao`);

    const missing = [...used].filter((c) => !definedClasses.has(c));
    assert.deepEqual(
      missing,
      [],
      `${file} dung ${missing.length} class KHONG co trong components.css: ${missing.join(', ')}. ` +
        `Day la catalog drift: vi du van "chay" nhung suy bien am tham.`,
    );
  });
}

test('moi catalog deu noi ro khi nao KHONG nen dung', () => {
  for (const file of catalogFiles) {
    const md = readFileSync(path.join(CATALOG, file), 'utf8');
    assert.match(
      md,
      /KHÔNG dùng|không nên dùng|Khong dung/i,
      `${file} thieu muc "khi nao KHONG nen dung"`,
    );
  }
});

test('khong catalog nao con em-dash hoac en-dash', () => {
  for (const file of catalogFiles) {
    const md = readFileSync(path.join(CATALOG, file), 'utf8');
    const bad = md.match(/[—–]/g) || [];
    assert.equal(bad.length, 0, `${file} co ${bad.length} em-dash hoac en-dash`);
  }
});
