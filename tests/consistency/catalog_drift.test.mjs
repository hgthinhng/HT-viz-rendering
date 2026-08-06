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

// Fix round 1 (F1 reviewer): ban cu chi kiem SU HIEN DIEN cua cum tu, nen
// mot cau rong nghia kieu "KHONG dung khi khong phu hop" van PASS. Sua lai:
// lay tu vi tri cum tu KHONG-dung dau tien den HET DOAN VAN chua no (doan
// "## Mo ta / khi nao dung" luon ket bang chinh cau KHONG-dung, xem 24 file
// that), roi doi hoi CA HAI dieu kien:
// 1. Do dai toi thieu (huong 1 cua reviewer, 40 ky tu) - loai cau qua ngan
//    kieu "khong phu hop".
// 2. Co it nhat MOT neo cu the (huong 2 cua reviewer, mo rong): mot con so
//    nguong (vi du "<5 moc", "1-2 so"), MOT tham chieu chuoi thay the that
//    (dang "khi do dung X", tuc chu "dung" xuat hien LAN THU HAI tro len
//    trong doan, vi ca cum trigger da chua san 1 lan), MOT class/property
//    CSS that trong dau backtick, hoac MOT vi du trich dan cu the trong dau
//    ngoac kep. Da chay dieu kien nay tren CA 24 file truoc khi chon: ban
//    dau huong 2 THUAN (chi nhan class/property, dung "\.[\w-]+|--[\w-]+")
//    la QUA CHAT, danh trot 19/24 file vi da so file tham chieu component
//    khac bang ten (vi du "dung note-box", "dung swimlane") hoac bang con
//    so nguong (vi du "<5 moc", ">8 diem") chu khong phai cu phap CSS
//    literal, ep vao se phai sua sai 19 file dang dung de vua test, dung
//    dieu bi cam. Bo sung them 2 neo (cross-ref "dung X" va vi du trich
//    dan) de khong danh oan noi dung tot; ket qua ca 24 file deu qua sau
//    khi 17-methodology-box.md duoc bo sung mot neo CSS that (`break-inside:
//    avoid` ap ca khoi, xem file do) vi cau cu chi canh bao dao duc ("dung
//    de che giau phuong phap yeu") ma khong neo vao dieu gi kiem duoc.
test('moi catalog deu noi ro khi nao KHONG nen dung, co neo cu the chu khong rong nghia', () => {
  const TRIGGER = /KHÔNG dùng|không nên dùng|Khong dung/i;
  const MIN_TAIL_LEN = 40;

  for (const file of catalogFiles) {
    const md = readFileSync(path.join(CATALOG, file), 'utf8');
    const idx = md.search(TRIGGER);
    assert.notEqual(idx, -1, `${file} thieu muc "khi nao KHONG nen dung"`);

    let paraEnd = md.indexOf('\n\n', idx);
    if (paraEnd === -1) paraEnd = md.length;
    const tail = md.slice(idx, paraEnd).trim();

    assert.ok(
      tail.length >= MIN_TAIL_LEN,
      `${file}: phan "KHONG dung" chi dai ${tail.length} ky tu (can >= ${MIN_TAIL_LEN}), ` +
        `qua ngan de mang noi dung that: "${tail}"`,
    );

    const hasThreshold = /\d/.test(tail);
    const dungCount = (tail.match(/dùng/gi) || []).length;
    const hasCrossRef = dungCount >= 2; // 1 lan la chinh trigger, >=2 la co tham chieu thay the
    const hasCssAnchor = /`[^`]+`/.test(tail);
    const hasQuotedExample = /"[^"]{2,40}"/.test(tail);
    const hasAnchor = hasThreshold || hasCrossRef || hasCssAnchor || hasQuotedExample;

    assert.ok(
      hasAnchor,
      `${file}: cau "KHONG dung" khong neo vao dieu gi kiem chung duoc ` +
        `(khong con so nguong, khong ten component thay the, khong class/property CSS trong backtick, ` +
        `khong vi du trich dan). Day la dang cau rong nghia kieu "khong phu hop" ma test nay sinh ra de chan: "${tail}"`,
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
