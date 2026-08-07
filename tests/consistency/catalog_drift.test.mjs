import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const CATALOG = path.join(ROOT, 'components/catalog');
const CSS = readFileSync(path.join(ROOT, 'components/components.css'), 'utf8');
const JS = readFileSync(path.join(ROOT, 'components/components.js'), 'utf8');
const TOKENS_CSS = readFileSync(path.join(ROOT, 'design-system/tokens.css'), 'utf8');

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

// Nguon that thu ba: slug cua chinh 24 file catalog (vi du "09-note-box.md"
// -> "note-box"), dung de kiem cross-ref "dung X thay the" co tro toi mot
// component THAT hay khong, thay vi chi dem so lan chu "dung" xuat hien.
const catalogSlugs = catalogFiles.map((f) => f.replace(/^\d+-/, '').replace(/\.md$/, ''));

// Nguon that thu tu: bien CSS THAT duoc DINH NGHIA (khong phai chi nhac
// ten) trong components.css hoac design-system/tokens.css, dung de kiem
// noi dung trong backtick co phai bia hay khong. Loai cac tien to qua
// chung chung (--space-, --fs-, --lh-, --radius-): day la thang do kich
// thuoc/khoang cach dung o GAN NHU MOI rule trong he thong, nhac ten mot
// bien nhom nay khong noi len dieu gi rieng cho component dang xet (vi du
// "--space-2" la that 100% nhung khong lien quan gi den ly do KHONG dung
// mot component cu the). Giu lai nhom mau sac/font/shadow vi chung mang
// nghia rieng (vi du "--warn" giai thich TAI SAO doi mau, "--ink-md" giai
// thich TAI SAO chu nhat hon).
const TOKENS_NO_COMMENTS = TOKENS_CSS.replace(/\/\*[\s\S]*?\*\//g, '');
const GENERIC_PROP_PREFIXES = ['--space-', '--fs-', '--lh-', '--radius-'];
const realCustomProps = new Set();
for (const src of [CSS_NO_COMMENTS, TOKENS_NO_COMMENTS]) {
  for (const m of src.matchAll(/(--[a-zA-Z][\w-]*)\s*:/g)) {
    if (!GENERIC_PROP_PREFIXES.some((p) => m[1].startsWith(p))) realCustomProps.add(m[1]);
  }
}

// Con so nguong that: mot chu so PHAI di kem mot dau hieu nghuong/don vi
// trong ban kinh 20 ky tu quanh no, khong chi la "co chu so nao do trong
// doan". Chan duoc kieu "...nam 2026..." (nam la mot chu so tran, khong co
// dau hieu nguong nao ben canh).
const COMPARISON_UNIT =
  /[<>≤≥±×]|\b(?:dưới|trên|quá|hơn|ít hơn|nhiều hơn|từ|chỉ|mỗi)\b|px|%|\b(?:cột|dòng|hàng|mục|trang|section|bước|mốc|điểm|câu|cặp|chỉ tiêu|biến|trạng thái|ràng buộc|giai đoạn|hạng mục|số)\b/i;

function hasRealThreshold(tail) {
  const WINDOW = 20;
  for (const m of tail.matchAll(/\d+/g)) {
    const start = Math.max(0, m.index - WINDOW);
    const end = Math.min(tail.length, m.index + m[0].length + WINDOW);
    if (COMPARISON_UNIT.test(tail.slice(start, end))) return true;
  }
  return false;
}

// Tham chieu component thay the PHAI trung slug that cua mot file catalog
// KHAC (khong tinh chinh no), khong chi dem so lan chu "dung" xuat hien.
function hasRealCrossRef(tail, ownSlug) {
  const low = tail.toLowerCase();
  return catalogSlugs.some((slug) => slug !== ownSlug && low.includes(slug.toLowerCase()));
}

// Noi dung trong backtick PHAI la mot class hoac custom property THAT SU
// TON TAI (doi chieu voi definedClasses/realCustomProps da dung nguyen o
// tren cho chinh test class-drift), khong chi can co dau backtick.
function hasRealCssAnchor(tail) {
  for (const span of [...tail.matchAll(/`([^`]+)`/g)].map((m) => m[1])) {
    for (const cm of span.matchAll(/\.([a-zA-Z][\w-]*)/g)) {
      if (definedClasses.has(cm[1])) return true;
    }
    for (const cm of span.matchAll(/(--[a-zA-Z][\w-]*)/g)) {
      if (realCustomProps.has(cm[1])) return true;
    }
  }
  return false;
}

// Fix round 3 (F1 van mo): re-reviewer viet duoc 2 cau rong nghia moi lot
// qua ca ba neo da siet o round 2, vi ca ba neo chi hoi "co mot MANH tin
// hieu nao do trong doan hay khong", khong hoi "MANH tin hieu do co thuc su
// la LY DO hay khong":
//   A. "...hay xem note-box de biet them" -> qua vi crossRef=true (trung
//      slug that "note-box"), nhung cau khong noi ro TAI SAO khong dung.
//   B. "...da dung o 3 trang khac" -> qua vi threshold=true ("3 trang" khop
//      dung mau so+don vi), nhung "da dung o dau" la so lan su dung, KHONG
//      phai mot NGUONG cua component.
// Ca hai cau co diem chung: cum tu NGAY SAU trigger ("khong phu hop",
// "khong hop") la mot LY DO RONG, moi thu phia sau (slug that, con so that)
// chi la trang tri gan vao mot cai khung rong. Day la gioi han cau truc cua
// ca 3 neo hien co: chung kiem "co mot manh THAT o dau do trong doan" chu
// khong kiem duoc "cau co Y NGHIA hay khong" (kiem y nghia van xuoi tu do
// bang regex la bat kha thi noi chung).
//
// Da can nhac 3 huong (xem task-7-report.md muc Fix round 3 de co phan
// tich day du): (1) ha ky vong, ghi ro gioi han; (2) doi thanh ">=2 loai
// neo" thay vi ">=1"; (3) danh sach den cum rong nghia hay gap. Loai (2) vi
// dem lai bang script rieng tren 24 file that (khong doan): dung 1 neo
// 17/24, 0 neo 0/24, tu 2 neo tro len 7/24 - tuc 71% file TOT hien chi co
// DUNG MOT loai neo. Ep len 2 se buoc phai viet them noi dung gia tao vao
// 71% file dang dung, dung chinh cai bay da gay ra F2 (bia mot su that CSS
// de thoa neo). Chon KET HOP (1) + (3): them mot danh sach den nham THANG
// vao cum mo dau rong nghia da biet (VACUOUS_OPENING), VA ghi ro trong
// comment nay rang test khong the kiem duoc y nghia noi dung noi chung, chi
// chan duoc cac dang rong nghia da biet + doi hoi it nhat mot manh THAT di
// kem. Day la gioi han THAT, khong phai loi chua sua.
//
// Fix round 4 (V2, cung mot re-reviewer): comment tren chi thanh that MOT
// CHIEU (chieu LOT mot cau gia). Con chieu nguoc lai cung THAT va da duoc
// tu tay dung lai:
//   - CHIEU LOT (da biet): VACUOUS_OPENING chi chan duoc DUNG CAC DANG da
//     liet ke. Doi mot chu la lach duoc: "khong phu hop" -> "chua phu hop"
//     hoac "it phu hop" van la ly do rong hoan toan nhung KHONG khop danh
//     sach den (da tu kiem lai: ca hai bien the deu cho vacuous=false).
//   - CHIEU OAN (moi phat hien, CO THAT, khong phai gia thuyet): mot cau
//     DUNG va dung duoc nhung TINH CO mo dau bang mot cum trong danh sach
//     den van bi chan. Vi du that da tu chay kiem chung:
//       "KHÔNG dùng khi không phù hợp với khổ hẹp dưới 700px vì
//       `.term-mag` cố định 3 cột."
//     Cau nay co nguong that (duoi 700px) VA neo CSS that (`.term-mag` co
//     that trong components.css), noi dung dung va dung duoc, nhung van bi
//     VACUOUS_OPENING chan vi mo dau trung "khong phu hop". Neu gap tinh
//     huong nay: viet lai cau de KHONG mo dau bang cum trong danh sach den
//     (vi du doi thanh "KHÔNG dùng cho khổ hẹp dưới 700px: `.term-mag` cố
//     định 3 cột."), DUNG di sua test rong danh sach den, vi noi long danh
//     sach den se mo lai chinh ke ho F1 vua dong.
const VACUOUS_OPENING =
  /^(?:KHÔNG dùng|không nên dùng|Khong dung)\s*(?:khi|để|cho|nếu)?\s*(?:không\s+)?(?:phù\s*hợp|hợp\s*lý|thích\s*hợp|hợp\b|cần\s*thiết|đúng(?:\s+ngữ\s*cảnh)?|tùy\s*(?:trường\s*hợp|tình\s*huống))/i;

test('co du 29 file catalog', () => {
  assert.equal(catalogFiles.length, 29, `co ${catalogFiles.length} file, mong doi 29`);
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
// that), roi doi hoi CA HAI dieu kien: (1) do dai toi thieu 40 ky tu, (2)
// it nhat MOT neo cu the.
//
// Fix round 2 (F1 reviewer, re-review NOT ADDRESSED): ba neo cua round 1
// (con so bat ky, chu "dung" xuat hien lan 2, co backtick bat ky) deu qua
// de thoa bang noi dung rong nghia. Reviewer tu viet duoc 3 cau rong nghia
// lot qua ca 3 neo do va CHUNG MINH bang so:
//   1. "...nen dung cach khac thay the cho tinh huong nay" -> qua vi chu
//      "dung" xuat hien 2 lan nhung KHONG neu ten component nao ca.
//   2. "...nhieu lan trong nam 2026..." -> qua vi hasThreshold cu chi doi
//      MOT chu so bat ky, "2026" la mot NAM chu khong phai mot NGUONG.
//   3. "...xem them `--space-2` de biet chi tiet." -> qua vi hasCssAnchor cu
//      chi doi CO backtick, khong kiem noi dung trong do co that hay khong.
// Siet lai ca 3 neo (bo han neo "vi du trich dan" vi no de thoa nhat bang
// noi dung rong, kieu "khong phu hop voi \"ngu canh nay\"" cung se lot qua
// neu chi doi co dau ngoac kep):
//   - Neo con so: PHAI co dau hieu nguong/don vi (<,>,quá,hơn,dưới,trên,
//     px,%,hang,cot,muc,trang,section,buoc,diem,... ) trong ban kinh 20 ky
//     tu quanh chu so, khong chi "co chu so nao do". Ham hasRealThreshold.
//   - Neo tham chieu: PHAI trung slug THAT cua mot trong 24 file catalog
//     (bien catalogSlugs, tu chinh danh sach catalogFiles dang co san),
//     khong chi dem so lan chu "dung". Ham hasRealCrossRef.
//   - Neo CSS: noi dung TRONG backtick phai la mot class hoac custom
//     property THAT SU duoc DINH NGHIA trong components.css/tokens.css
//     (tai dung definedClasses + tap realCustomProps moi), khong chi can
//     co dau backtick. Loai rieng cac tien to qua chung chung (--space-,
//     --fs-, --lh-, --radius-) vi mot bien that nhung chung chung (vi du
//     "--space-2" co that 100%) khong noi len ly do KHONG dung component
//     nay. Ham hasRealCssAnchor.
// Da chay dieu kien moi tren CA 24 file TRUOC khi chot (xem
// task-7-report.md muc Fix round 2 de co bang day du): 4 file FAIL that su
// (07-pull-quote, 13-options-comparison-table, 18-toc-with-milestones,
// 20-source-badge-k-anchor) vi cau goc chi la loi nhac nho chung chung,
// khong neo vao con so/slug/CSS nao. Ca 4 duoc bo sung mot su that CSS that
// (vi du 18: `.toc-mark` chi to mau cho dung 3 gia tri data-status; 20:
// `.src-badge` chi dinh nghia mau cho dung 4 gia tri data-tier) thay vi noi
// long dieu kien, dung tinh than "sua file that su thieu, dung sua-cho-vua-
// test" da lam o round 1 voi 17-methodology-box.md. Sau do ca 24 file qua.
//
// F2 nghiem trong o Fix round 3: cau bo sung cho 13-options-comparison-
// table.md o buoc tren KHANG DINH SAI SU THAT ("table.opt-compare khong co
// tr{break-inside:avoid} nhu table.dt") - ca hai thuc ra co CUNG mot rule
// (`components.css` dong 302 va 314, gop chung o dong 471), rule dong 314
// co tu commit Task 3 (`f458261`), tuc TRUOC CA round 1 lan round 2 cua
// chinh file test nay. Day la catalog drift THAT, tu tay dua vao chi de
// thoa dung cai test nay sinh ra de chong drift - bai hoc: mot gate doi
// bang chung CSS ma khong ai doi chieu lai se tao dong co bia bang chung.
// Da sua: bo han cau CSS bia, chi giu nguong so hang voi ly do thiet ke
// that (lay thang tu chinh cau "Tra loi" cua file, khong bia them CSS moi).
// Xem task-7-report.md muc Fix round 3 phan "F2" de co file:dong lam bang
// chung cho MOI khang dinh CSS con lai trong ca 4 file (07/13/18/20).
//
// GIOI HAN THAT cua test nay (ghi ro de khong ai tuong no bao dam hon thuc
// te): no KHONG the kiem "cau nay co Y NGHIA that hay khong" bang regex.
// No chi kiem duoc: (a) co du dai toi thieu, (b) co it nhat mot MANH THAT
// (con so kem nguong, slug catalog that, hoac class/property CSS that), va
// (c) phan mo dau ngay sau trigger khong roi vao mot danh sach cum rong
// nghia DA BIET (VACUOUS_OPENING). Mot cau du de deliberately gian nguoi
// van co the lot qua neu no tranh duoc ca ba dieu nay (vi du ghep mot slug
// that vao mot ly do vo ly nhung khong mo dau bang cum rong nghia da biet).
// Test nay LA MOT SMOKE TEST CHONG DRIFT HINH THUC RO RANG, khong phai mot
// bo kiem duyet noi dung hoan chinh; nguoi doc report van la lop kiem cuoi
// cung cho chat luong ly do.
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
    const ownSlug = file.replace(/^\d+-/, '').replace(/\.md$/, '');

    const lenOk = tail.length >= MIN_TAIL_LEN;
    const hasThreshold = hasRealThreshold(tail);
    const hasCrossRef = hasRealCrossRef(tail, ownSlug);
    const hasCssAnchor = hasRealCssAnchor(tail);
    const anchorOk = hasThreshold || hasCrossRef || hasCssAnchor;
    const vacuousOpening = VACUOUS_OPENING.test(tail);

    // Mot assert DUY NHAT, bao ca ba dieu kien cung luc: nguoi sua khong
    // the chi doc "thieu do dai" roi viet dai ra ma van rong nghia, vi
    // thong bao luon noi ro CA trang thai neo VA trang thai mo dau
    // (Fix round 2 + round 3, re-reviewer).
    assert.ok(
      lenOk && anchorOk && !vacuousOpening,
      `${file}: do dai=${tail.length} ky tu (can >= ${MIN_TAIL_LEN}, ${lenOk ? 'OK' : 'THIEU'}); ` +
        `neo=[nguong:${hasThreshold ? 'co' : 'khong'}, tham-chieu-component-that:${hasCrossRef ? 'co' : 'khong'}, ` +
        `css-anchor-that:${hasCssAnchor ? 'co' : 'khong'}] (can it nhat 1 "co", hien ${anchorOk ? 'OK' : 'THIEU CA BA'}); ` +
        `mo-dau-rong-nghia:${vacuousOpening ? 'CO, BI CHAN' : 'khong'}. ` +
        `Day la dang cau rong nghia ma test nay sinh ra de chan. Noi dung dang xet: "${tail}"`,
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

// ── Hai bay WeasyPrint da gap that o khoi ma tran 2x2, chan tai pham ──────
//
// Ca hai deu thuoc mot lop loi: CSS chay dung tren trinh duyet nhung engine
// dich bo qua thuoc tinh, va vi ban HTML van dep nen khong ai phat hien cho
// toi luc mo file PDF ra nhin. Test o day chan bang cach doc NGUON, khong
// render, de no chay nhanh va chay duoc ca khi khong co WeasyPrint.

test('khong dat class visually-hidden thang len the table', () => {
  // WeasyPrint 69.0 khong ap overflow:hidden lan clip len table box, nen
  // <table class="visually-hidden"> VAN VE RA trong PDF trong khi trinh duyet
  // an dung. Da do bang ca toi gian: cung class, <span> an dung con <table>
  // hien nguyen. Hau qua that: bang du lieu cho trinh doc man hinh cua khoi
  // ma tran 2x2 in de len chinh khoi do. Cach dung la boc <table> trong mot
  // <div class="visually-hidden">, vi nhu vay table giu nguyen ngu nghia bang
  // cho trinh doc man hinh.
  const nguon = [
    ['components/gallery.html', readFileSync(path.join(ROOT, 'components/gallery.html'), 'utf8')],
    ...catalogFiles.map((f) => [`components/catalog/${f}`, readFileSync(path.join(CATALOG, f), 'utf8')]),
  ];
  const viPham = [];
  for (const [ten, src] of nguon) {
    // Bat ca hai thu tu thuoc tinh: <table class="visually-hidden"> lan
    // <table id="x" class="a visually-hidden">.
    const re = /<table\b[^>]*\bclass\s*=\s*"[^"]*\bvisually-hidden\b/g;
    const so = (src.match(re) || []).length;
    if (so) viPham.push(`${ten}: ${so} cho`);
  }
  assert.deepEqual(
    viPham,
    [],
    'Dat class sr-only len div BOC NGOAI thay vi len chinh the <table>. ' +
      `WeasyPrint van in bang do ra PDF. Vi pham:\n${viPham.join('\n')}`,
  );
});

test('components.css khong dung aspect-ratio', () => {
  // WeasyPrint 69.0 khong ho tro aspect-ratio: mot khoi width:200px voi
  // aspect-ratio:1/0.72 ra cao 0, sap thanh dung mot duong ke. Khoi .q-grid
  // tung dinh dung bay nay: khung ma tran co lai bang chieu cao noi dung, bon
  // cham dinh vi theo phan tram cua mot khung det nen don cum va nhan tran ra
  // ngoai. Dung chieu cao khai bang px de hai engine cao bang nhau.
  // Phai boc HET comment khoi /* ... */ truoc khi quet, khong loc theo tung
  // dong. Ban dau test nay loc dong mo dau bang "/*" hoac "*", va no do ngay
  // tren chinh doan comment GIAI THICH vi sao khong duoc dung aspect-ratio,
  // vi cac dong giua cua khoi comment do bat dau bang khoang trang roi chu.
  // Ke lai cai bay trong comment thi duoc, dung that thi khong.
  const cssSachComment = CSS.replace(/\/\*[\s\S]*?\*\//g, (khoi) =>
    khoi.replace(/[^\n]/g, ' '),
  );
  const dong = cssSachComment
    .split('\n')
    .map((l, i) => [i + 1, l])
    .filter(([, l]) => /(^|[^-\w])aspect-ratio\s*:/.test(l));
  assert.deepEqual(
    dong.map(([i]) => `dong ${i}: ${CSS.split('\n')[i - 1].trim()}`),
    [],
    'aspect-ratio khong render trong WeasyPrint, dung height/width bang px.',
  );
});
