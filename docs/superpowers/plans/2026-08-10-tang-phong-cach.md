# Tầng phong-cách Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng tầng phong-cách (style layer) cho HT-viz-rendering theo spec `docs/specs/2026-08-09-tang-phong-cach-design.md` v2 (commit 38cf96a): hạ tầng compose + 4 style + 4 exemplar qua gate + track research song song.

**Architecture:** Tầng compose đứng trên hệ chủ đề màu hiện có. Mỗi style là một thư mục trong `phong-cach/` với `phong-cach.json` (nguồn sự thật duy nhất), `design.md`, `lop.css`. `INDEX.json` sinh tự động. `build_html.py` đọc style từ front-matter bắt buộc. Gate mới KHOA-CHU-DE ở cả hai làn. `nghiem-thu.json` do `gates/run.mjs` sinh.

**Tech Stack:** Node >= 22 (node:test, ajv có sẵn trong deps), Python 3.12 (pipeline), WeasyPrint (làn pdf-so), ECharts SVGRenderer (làn html-song), fontTools (kiểm phủ glyph).

## Global Constraints

- Cấm em-dash (U+2014) và en-dash (U+2013) ở MỌI NƠI, kể cả comment; regex viết bằng escape dạng backslash-u2014, tài liệu gọi hai ký tự này bằng TÊN, không dán ký tự thật. Test `em_dash_repo.test.mjs` canh toàn repo.
- Hex màu CHỈ sống trong `design-system/themes/*.json`. Sửa màu: sửa JSON rồi chạy `node design-system/generate-tokens.mjs`; ba bản chép tay phải sửa kèm (khối `:root` đầu tokens.css, dict đầu tokens.py, `PALETTE` phẳng trong theme.mjs); `theme_tokens_drift.test.mjs` và `chart_theme.test.mjs` canh.
- Mọi gate hoặc test mới phải có cặp fixture đỏ và xanh, và test ép bản đỏ FAIL thật.
- Font phải nhúng: woff2 base64 trong `fonts-embedded.css`, bản ttf trích bằng `design-system/fonts/extract-ttf.py` cho matplotlib. Bẫy đã biết: Google Fonts đặt bản đậm thành HỌ RIÊNG, extract-ttf.py ép lại nameID.
- File test mới đặt đúng hai cấp: `tests/consistency/` hoặc `tests/smoke/`. Không bỏ dấu ngoặc kép trong script test của package.json.
- Mọi chỗ mở Chromium đi qua `scripts/lib/chromium.mjs`.
- Commit message tiếng Việt không dấu, câu ngắn tả việc, kết bằng trailer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Làm trên nhánh `feat/digital-only-buoc-1-2`. KHÔNG merge, KHÔNG push khi chưa có lệnh operator.
- Số liệu exemplar là số minh hoạ, khai rõ ở dek theo tiền lệ van-tai-bien. Không mượn số công bố của tổ chức thật, không bịa testimonial.
- `npm test` phải 176/176 pass trở lên sau MỖI task; task nào làm đỏ test cũ thì sửa trong task đó.

## Sơ đồ file toàn arc

```
phong-cach/
  INDEX.json                    (sinh, Task 2)
  sinh-index.mjs                (Task 2)
  schema.mjs                    (Task 1)
  alias.json                    (Task 4)
  README.md                     (Task 8)
  thep-xanh/{phong-cach.json, design.md, lop.css}      (Task 1, 7)
  giay-am/{phong-cach.json, design.md, lop.css}        (Task 9, 12)
  nhung-toi/{phong-cach.json, design.md, lop.css}      (Task 10, 14)
  poster-dac/{phong-cach.json, design.md, lop.css}     (Task 11, 13)
design-system/themes/{giay-am,nhung-toi,poster-dac}.json  (Task 9, 10, 11)
pipeline/build_html.py          (sửa, Task 4)
pipeline/orchestrator.py        (sửa, Task 4, 15)
gates/{run.mjs, gates.mjs, gates_song.mjs}              (sửa, Task 5, 6)
scripts/nghiem-thu-exemplars.mjs                        (Task 7)
tests/consistency/phong_cach.test.mjs                   (Task 1, 2, 3, 5)
tests/smoke/phong_cach_build.test.mjs                   (Task 4)
tests/fixtures/phong-cach/{do,xanh}/...                 (Task 1)
examples/tom-tat-dieu-hanh-mau/                         (Task 12)
examples/poster-nganh-mau/                              (Task 13)
examples/deal-pack-mau/                                 (Task 14)
research/12-style-directions/                           (Track R, song song)
```

Thứ tự cứng (rút từ phản biện kimi): Task 1-8 là móng và harvest thep-xanh; Task 9-11 chủ đề màu; Task 12-14 exemplar theo độ khó tăng dần (giay-am sáng pdf, poster-dac sáng song, nhung-toi tối cuối vì cần luật khoá mới đã xong ở Task 6); Task 15-16 nghi thức và hoàn tất. Track R chạy song song bất kỳ lúc nào, không chặn ai.

---

### Task 1: Schema phong-cach + style thep-xanh + test đỏ xanh

**Files:**
- Create: `phong-cach/schema.mjs`
- Create: `phong-cach/thep-xanh/phong-cach.json`
- Create: `tests/fixtures/phong-cach/xanh/phong-cach.json`
- Create: `tests/fixtures/phong-cach/do-thieu-truong/phong-cach.json`
- Create: `tests/fixtures/phong-cach/do-mau-literal/phong-cach.json`
- Create: `tests/fixtures/phong-cach/do-toi-khong-gioi-han/phong-cach.json`
- Create: `tests/consistency/phong_cach.test.mjs`

**Interfaces:**
- Produces: `validatePhongCach(obj) -> { hopLe: boolean, loi: string[] }` từ `phong-cach/schema.mjs`; hằng `BAY_LOAI_AN_PHAM` (mảng 7 slug); hằng `RE_MAU_LITERAL` (regex bắt hex và hàm màu literal).
- Consumes: danh sách 7 loại ấn phẩm trong `SKILL.md` mục 1.B (đọc SKILL.md để chép đúng slug; nếu SKILL.md chưa có slug không dấu thì đặt tại đây và Task 8 đồng bộ ngược vào SKILL.md).

- [ ] **Bước 1: Viết `phong-cach/schema.mjs`**

```js
// Schema va validator cua phong-cach.json. Nguon su that duy nhat cua tang style.
// Khong dung ajv o day du co san: luat "cam mau literal" can regex tren MOI string,
// ajv khong lam duoc gon; validator tay ~60 dong, de doc, de them luat.

export const BAY_LOAI_AN_PHAM = [
  'ban-tin-thi-truong',
  'cap-nhat-kqkd',
  'bao-cao-khoi-tao-ma',
  'bao-cao-nganh',
  'deal-pack',
  'tom-tat-dieu-hanh',
  'ban-mau-ky-thuat',
];

// Bat hex (#abc, #aabbcc) va ham mau voi literal ben trong. var() duoc phep.
export const RE_MAU_LITERAL =
  /#[0-9a-fA-F]{3,8}\b|(?:rgb|rgba|hsl|hsla|oklch|lab|lch|color|color-mix)\s*\(/;

const TRANG_THAI_HOP_LE = ['chinh-thuc', 'vuon-uom'];

export function validatePhongCach(obj, { tenThuMuc = null, danhSachChuDe = [] } = {}) {
  const loi = [];
  const bat = (dk, msg) => { if (!dk) loi.push(msg); };

  bat(typeof obj.slug === 'string' && /^[a-z0-9-]+$/.test(obj.slug), 'slug phai la chuoi khong dau, chi a-z0-9-');
  if (tenThuMuc) bat(obj.slug === tenThuMuc, `slug ${obj.slug} phai trung ten thu muc ${tenThuMuc}`);
  bat(typeof obj.tagline === 'string' && obj.tagline.length >= 10, 'tagline phai co, toi thieu 10 ky tu');
  bat(Array.isArray(obj.mood) && obj.mood.length >= 1, 'mood phai la mang co it nhat 1 phan tu');
  bat(['cao', 'trung-cao', 'trung', 'thap'].includes(obj.formality), 'formality khong hop le');
  bat(['cao', 'trung', 'thap'].includes(obj.density), 'density khong hop le');
  for (const k of ['best_for', 'avoid_for']) {
    bat(Array.isArray(obj[k]), `${k} phai la mang`);
    for (const v of obj[k] || []) {
      bat(BAY_LOAI_AN_PHAM.includes(v), `${k} chua slug la: ${v}`);
    }
  }
  bat(typeof obj.chu_de_mac_dinh === 'string', 'chu_de_mac_dinh phai co');
  if (danhSachChuDe.length) {
    bat(danhSachChuDe.includes(obj.chu_de_mac_dinh),
      `chu_de_mac_dinh ${obj.chu_de_mac_dinh} khong co trong design-system/themes/`);
    if (obj.chu_de_dan_xuat != null) {
      bat(danhSachChuDe.includes(obj.chu_de_dan_xuat),
        `chu_de_dan_xuat ${obj.chu_de_dan_xuat} khong co trong design-system/themes/`);
    }
  }
  bat(Array.isArray(obj.gioi_han_loai_hinh), 'gioi_han_loai_hinh phai la mang, rong cung duoc');
  bat(obj.font && typeof obj.font.kit === 'string', 'font.kit phai co');
  bat(obj.token_override && typeof obj.token_override === 'object', 'token_override phai la object, rong cung duoc');
  for (const [k, v] of Object.entries(obj.token_override || {})) {
    bat(k.startsWith('--'), `token_override khoa ${k} phai bat dau bang --`);
    bat(!RE_MAU_LITERAL.test(String(v)),
      `token_override[${k}] chua mau literal, chi duoc var() hoac literal phi mau: ${v}`);
  }
  bat(typeof obj.chart_palette === 'string', 'chart_palette phai co');
  bat(TRANG_THAI_HOP_LE.includes(obj.trang_thai), 'trang_thai chi nhan chinh-thuc hoac vuon-uom');
  if (obj.trang_thai === 'chinh-thuc') {
    bat(typeof obj.exemplar === 'string' && obj.exemplar.startsWith('examples/'),
      'chinh-thuc thi exemplar phai tro vao examples/');
  }
  return { hopLe: loi.length === 0, loi };
}

// Luat rieng cho style co chu de mac dinh TOI: bat buoc cam matplotlib.
// Goi RIENG vi can biet paper cua chu de; ham nhan san co toi hay khong.
export function validateGioiHanChoChuDeToi(obj, chuDeLaToi) {
  if (!chuDeLaToi) return { hopLe: true, loi: [] };
  const ok = (obj.gioi_han_loai_hinh || []).includes('matplotlib');
  return {
    hopLe: ok,
    loi: ok ? [] : [`style ${obj.slug} co chu de toi thi gioi_han_loai_hinh phai chua "matplotlib"`],
  };
}
```

- [ ] **Bước 2: Viết `phong-cach/thep-xanh/phong-cach.json`**

```json
{
  "slug": "thep-xanh",
  "tagline": "Blue editorial nghiêm, giọng báo cáo tổ chức, tin ở mật độ lập luận",
  "mood": ["nghiem-tuc", "to-chuc", "lanh"],
  "formality": "cao",
  "density": "cao",
  "best_for": ["bao-cao-nganh", "bao-cao-khoi-tao-ma", "cap-nhat-kqkd", "ban-tin-thi-truong"],
  "avoid_for": ["tom-tat-dieu-hanh"],
  "chu_de_mac_dinh": "sang-lanh",
  "chu_de_dan_xuat": "toi-lanh",
  "gioi_han_loai_hinh": [],
  "font": {
    "kit": "mac-dinh",
    "hien_thi": "Spectral",
    "van_ban": "Spectral",
    "so_va_nhan": "IBM Plex Mono"
  },
  "token_override": {},
  "chart_palette": "sang-lanh",
  "exemplar": "examples/van-tai-bien",
  "trang_thai": "vuon-uom"
}
```

Ghi chú: `trang_thai` để `vuon-uom` cho tới Task 7 khi nghiem-thu.json được máy sinh; `avoid_for` chứa tom-tat-dieu-hanh vì loại đó sẽ thuộc giay-am, chỉnh lại được sau khi có nhiều style. Font kit `mac-dinh` nghĩa là dùng nguyên `fonts-embedded.css` hiện tại, build không thay gì.

- [ ] **Bước 3: Viết fixtures đỏ xanh**

`tests/fixtures/phong-cach/xanh/phong-cach.json`: chép nguyên nội dung Bước 2 nhưng `"slug": "xanh"`.

`tests/fixtures/phong-cach/do-thieu-truong/phong-cach.json`: chép bản xanh, `"slug": "do-thieu-truong"`, XOÁ khoá `chart_palette`.

`tests/fixtures/phong-cach/do-mau-literal/phong-cach.json`: chép bản xanh, `"slug": "do-mau-literal"`, đổi `token_override` thành `{ "--accent": "#FF0000" }`.

`tests/fixtures/phong-cach/do-toi-khong-gioi-han/phong-cach.json`: chép bản xanh, `"slug": "do-toi-khong-gioi-han"`, `"chu_de_mac_dinh": "toi-lanh"`, `gioi_han_loai_hinh: []`.

- [ ] **Bước 4: Viết test và chạy cho FAIL trước**

`tests/consistency/phong_cach.test.mjs` (phần 1, các phần sau nối thêm ở Task 2, 3, 5):

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validatePhongCach, validateGioiHanChoChuDeToi, BAY_LOAI_AN_PHAM, RE_MAU_LITERAL } from '../../phong-cach/schema.mjs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PC = path.join(REPO, 'phong-cach');
const FX = path.join(REPO, 'tests', 'fixtures', 'phong-cach');

function docJson(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }
function danhSachChuDe() {
  return fs.readdirSync(path.join(REPO, 'design-system', 'themes'))
    .filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, ''));
}
function chuDeLaToi(ten) {
  // Chu de toi = paper co do sang thap. Doc truc tiep tu nguon.
  const t = docJson(path.join(REPO, 'design-system', 'themes', `${ten}.json`));
  const hex = t.mau.paper.replace('#', '');
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16));
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) < 96;
}
function cacStyle() {
  return fs.readdirSync(PC, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'fixtures')
    .map((d) => d.name);
}

test('moi phong-cach.json qua schema', () => {
  const themes = danhSachChuDe();
  for (const slug of cacStyle()) {
    const obj = docJson(path.join(PC, slug, 'phong-cach.json'));
    const kq = validatePhongCach(obj, { tenThuMuc: slug, danhSachChuDe: themes });
    assert.deepEqual(kq.loi, [], `style ${slug}: ${kq.loi.join('; ')}`);
    const kq2 = validateGioiHanChoChuDeToi(obj, chuDeLaToi(obj.chu_de_mac_dinh));
    assert.deepEqual(kq2.loi, [], `style ${slug}: ${kq2.loi.join('; ')}`);
  }
});

test('fixture xanh PASS, ba fixture do FAIL dung cho', () => {
  const themes = danhSachChuDe();
  const xanh = docJson(path.join(FX, 'xanh', 'phong-cach.json'));
  assert.equal(validatePhongCach(xanh, { tenThuMuc: 'xanh', danhSachChuDe: themes }).hopLe, true);

  const thieu = docJson(path.join(FX, 'do-thieu-truong', 'phong-cach.json'));
  const kqThieu = validatePhongCach(thieu, { tenThuMuc: 'do-thieu-truong', danhSachChuDe: themes });
  assert.equal(kqThieu.hopLe, false);
  assert.ok(kqThieu.loi.some((l) => l.includes('chart_palette')), kqThieu.loi.join('; '));

  const mau = docJson(path.join(FX, 'do-mau-literal', 'phong-cach.json'));
  const kqMau = validatePhongCach(mau, { tenThuMuc: 'do-mau-literal', danhSachChuDe: themes });
  assert.equal(kqMau.hopLe, false);
  assert.ok(kqMau.loi.some((l) => l.includes('mau literal')), kqMau.loi.join('; '));

  const toi = docJson(path.join(FX, 'do-toi-khong-gioi-han', 'phong-cach.json'));
  const kqToi = validateGioiHanChoChuDeToi(toi, true);
  assert.equal(kqToi.hopLe, false);
});

test('RE_MAU_LITERAL khong bat var() va literal phi mau', () => {
  assert.equal(RE_MAU_LITERAL.test('var(--space-6)'), false);
  assert.equal(RE_MAU_LITERAL.test('2px'), false);
  assert.equal(RE_MAU_LITERAL.test('#2251FF'), true);
  assert.equal(RE_MAU_LITERAL.test('rgb(1, 2, 3)'), true);
  assert.equal(RE_MAU_LITERAL.test('color-mix(in srgb, red, blue)'), true);
});

test('BAY_LOAI_AN_PHAM co dung 7 slug khong dau', () => {
  assert.equal(BAY_LOAI_AN_PHAM.length, 7);
  for (const s of BAY_LOAI_AN_PHAM) assert.match(s, /^[a-z0-9-]+$/);
});
```

Chạy TRƯỚC khi tạo schema.mjs để thấy đỏ: `node --test tests/consistency/phong_cach.test.mjs`. Expected: FAIL vì module chưa tồn tại. Sau khi tạo đủ file ở Bước 1-3, chạy lại. Expected: PASS toàn bộ.

- [ ] **Bước 5: Chạy `npm test` toàn suite, xác nhận không đỏ test cũ, rồi commit**

```bash
git add phong-cach/ tests/fixtures/phong-cach/ tests/consistency/phong_cach.test.mjs
git commit -m "Tang phong-cach: schema, style thep-xanh, test do xanh"
```

---

### Task 2: sinh-index.mjs và INDEX.json bản sinh

**Files:**
- Create: `phong-cach/sinh-index.mjs`
- Create: `phong-cach/INDEX.json` (bản sinh đầu tiên)
- Modify: `tests/consistency/phong_cach.test.mjs` (nối test drift)

**Interfaces:**
- Produces: `node phong-cach/sinh-index.mjs` ghi INDEX.json; `node phong-cach/sinh-index.mjs --kiem` exit 1 nếu INDEX trên đĩa lệch bản tính lại; export `tinhIndex(repoRoot) -> object` để test gọi thẳng.
- Consumes: `phong-cach/*/phong-cach.json` (Task 1), `examples/*/nghiem-thu.json` (Task 5 sinh, trước đó chưa có thì entry bị hạ về vuon-uom).

- [ ] **Bước 1: Viết `phong-cach/sinh-index.mjs`**

```js
#!/usr/bin/env node
// Sinh INDEX.json tu cac phong-cach.json. INDEX la BAN SINH, cam sua tay.
// Cung ky luat voi design-system/generate-tokens.mjs: mot nguon, mot generator,
// mot test drift. --kiem chi so sanh, khong ghi.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validatePhongCach } from './schema.mjs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PC = path.join(REPO, 'phong-cach');

export function tinhIndex(repoRoot = REPO) {
  const pcDir = path.join(repoRoot, 'phong-cach');
  const danhSach = [];
  const themes = fs.readdirSync(path.join(repoRoot, 'design-system', 'themes'))
    .filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, ''));
  const slugs = fs.readdirSync(pcDir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
    .map((d) => d.name).sort();
  for (const slug of slugs) {
    const duongDan = path.join(pcDir, slug, 'phong-cach.json');
    if (!fs.existsSync(duongDan)) continue;
    const obj = JSON.parse(fs.readFileSync(duongDan, 'utf8'));
    const kq = validatePhongCach(obj, { tenThuMuc: slug, danhSachChuDe: themes });
    if (!kq.hopLe) throw new Error(`phong-cach/${slug} khong qua schema: ${kq.loi.join('; ')}`);

    // trang_thai chinh-thuc phai co nghiem-thu.json hop le; thieu thi HA CAP,
    // khong loi: dang giua arc thi style dang dung o vuon-uom la trang thai that.
    let trangThai = obj.trang_thai;
    let lanDaChungMinh = [];
    if (obj.exemplar) {
      const ntPath = path.join(repoRoot, obj.exemplar, 'nghiem-thu.json');
      if (fs.existsSync(ntPath)) {
        const nt = JSON.parse(fs.readFileSync(ntPath, 'utf8'));
        const coFail = (nt.gate || []).some((g) => g.ket_qua === 'FAIL');
        if (!coFail && nt.lan) lanDaChungMinh = [nt.lan];
      }
    }
    if (trangThai === 'chinh-thuc' && lanDaChungMinh.length === 0) trangThai = 'vuon-uom';

    danhSach.push({
      slug: obj.slug,
      tagline: obj.tagline,
      mood: obj.mood,
      formality: obj.formality,
      density: obj.density,
      best_for: obj.best_for,
      avoid_for: obj.avoid_for,
      chu_de_mac_dinh: obj.chu_de_mac_dinh,
      trang_thai: trangThai,
      exemplar: obj.exemplar ?? null,
      lan_da_chung_minh: lanDaChungMinh,
    });
  }
  return { phien_ban: 2, sinh_boi: 'phong-cach/sinh-index.mjs', danh_sach: danhSach };
}

const laMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (laMain) {
  const ra = JSON.stringify(tinhIndex(), null, 2) + '\n';
  const dich = path.join(PC, 'INDEX.json');
  if (process.argv.includes('--kiem')) {
    const cu = fs.existsSync(dich) ? fs.readFileSync(dich, 'utf8') : '';
    if (cu !== ra) {
      console.error('INDEX.json lech ban tinh lai. Chay: node phong-cach/sinh-index.mjs');
      process.exit(1);
    }
    console.log('INDEX.json khop nguon.');
  } else {
    fs.writeFileSync(dich, ra);
    console.log(`Da ghi ${dich} (${tinhIndex().danh_sach.length} style)`);
  }
}
```

- [ ] **Bước 2: Sinh INDEX lần đầu và nối test drift**

Chạy `node phong-cach/sinh-index.mjs`. Kiểm bằng mắt: một entry thep-xanh, `trang_thai: "vuon-uom"` (vì nghiem-thu.json chưa tồn tại, đúng hành vi hạ cấp), `lan_da_chung_minh: []`.

Nối vào `tests/consistency/phong_cach.test.mjs`:

```js
test('INDEX.json la ban sinh, khop nguon', async () => {
  const { tinhIndex } = await import('../../phong-cach/sinh-index.mjs');
  const tren_dia = docJson(path.join(PC, 'INDEX.json'));
  assert.deepEqual(tren_dia, tinhIndex(REPO), 'INDEX.json lech: chay node phong-cach/sinh-index.mjs');
});

test('entry chinh-thuc phai co lan_da_chung_minh', () => {
  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (e.trang_thai === 'chinh-thuc') {
      assert.ok(e.lan_da_chung_minh.length >= 1, `${e.slug} chinh-thuc ma khong co lan chung minh`);
      assert.ok(e.exemplar, `${e.slug} chinh-thuc ma khong co exemplar`);
    }
  }
});
```

- [ ] **Bước 3: Chạy test, PASS, commit**

```bash
node --test tests/consistency/phong_cach.test.mjs   # PASS
git add phong-cach/sinh-index.mjs phong-cach/INDEX.json tests/consistency/phong_cach.test.mjs
git commit -m "INDEX phong-cach la ban sinh, co test drift va luat ha cap"
```

---

### Task 3: Quét màu literal và contract lop.css

**Files:**
- Create: `phong-cach/thep-xanh/lop.css` (rỗng có scope, làm mẫu contract)
- Modify: `tests/consistency/phong_cach.test.mjs` (nối test contract)

**Interfaces:**
- Produces: quy ước lop.css mà Task 9-14 phải theo: mọi rule nằm dưới `[data-phong-cach="<slug>"]`, không màu literal, style có exemplar pdf-so không dùng thuộc tính trong `CAM_PDF`.
- Consumes: `RE_MAU_LITERAL` từ schema.mjs (Task 1).

- [ ] **Bước 1: Viết `phong-cach/thep-xanh/lop.css`**

```css
/* lop.css cua thep-xanh: RONG co chu y. thep-xanh la giong hien trang cua repo,
   moi override o day se lam no lech chinh no. Scope de san lam mau contract. */
[data-phong-cach="thep-xanh"] {
}
```

- [ ] **Bước 2: Nối test contract vào phong_cach.test.mjs**

```js
const CAM_PDF = ['aspect-ratio', 'writing-mode', 'backdrop-filter', 'filter:'];

test('lop.css theo contract: scope dung slug, khong mau literal', () => {
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'lop.css');
    if (!fs.existsSync(p)) continue;
    const css = fs.readFileSync(p, 'utf8');
    // Bo comment truoc khi quet
    const sach = css.replace(/\/\*[\s\S]*?\*\//g, '');
    assert.equal(RE_MAU_LITERAL.test(sach), false, `${slug}/lop.css chua mau literal`);
    // Moi selector ngoai cung phai mang scope [data-phong-cach="slug"]
    const selectors = [...sach.matchAll(/(^|\})\s*([^@{}]+)\{/g)].map((m) => m[2].trim()).filter(Boolean);
    for (const sel of selectors) {
      assert.ok(sel.includes(`[data-phong-cach="${slug}"]`),
        `${slug}/lop.css selector khong scope: ${sel}`);
    }
  }
});

test('style co exemplar lan pdf-so: lop.css khong dung thuoc tinh WeasyPrint bo qua', () => {
  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (!e.lan_da_chung_minh.includes('pdf-so')) continue;
    const p = path.join(PC, e.slug, 'lop.css');
    if (!fs.existsSync(p)) continue;
    const sach = fs.readFileSync(p, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
    for (const cam of CAM_PDF) {
      assert.ok(!sach.includes(cam), `${e.slug}/lop.css dung ${cam}, WeasyPrint bo qua hoac pha`);
    }
  }
});

test('design.md khong lap hex', () => {
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'design.md');
    if (!fs.existsSync(p)) continue;
    const md = fs.readFileSync(p, 'utf8');
    assert.equal(/#[0-9a-fA-F]{6}\b/.test(md), false, `${slug}/design.md chua hex, mau chi noi bang ten token`);
  }
});
```

- [ ] **Bước 3: Chạy test PASS, commit**

```bash
node --test tests/consistency/phong_cach.test.mjs
git add phong-cach/thep-xanh/lop.css tests/consistency/phong_cach.test.mjs
git commit -m "Contract lop.css: scope theo slug, cam mau literal, lint pdf-safe"
```

---

### Task 4: build_html.py đọc phong-cach, alias chủ đề, orchestrator chặn loại hình

**Files:**
- Create: `phong-cach/alias.json`
- Modify: `pipeline/build_html.py` (quanh dòng 71-97, 862-918, 920-935)
- Modify: `pipeline/orchestrator.py` (bước [1/6] HÌNH)
- Modify: `examples/van-tai-bien/noi-dung.md` và `examples/mau-phase2/noi-dung.md` (backfill front-matter)
- Create: `tests/smoke/phong_cach_build.test.mjs`
- Create: `tests/fixtures/phong-cach/bao-cao-thieu-khoa/noi-dung.md` + `so-nguon.json`
- Create: `tests/fixtures/phong-cach/bao-cao-vi-pham-loai-hinh/{noi-dung.md, so-nguon.json, hinh/gia.py}`

**Interfaces:**
- Consumes: `phong-cach/<slug>/phong-cach.json` (Task 1), `lop.css` (Task 3).
- Produces: front-matter bắt buộc `phong-cach: <slug>`; hàm Python `doc_phong_cach(meta: dict) -> dict` trong build_html.py; thẻ html thêm `data-phong-cach="<slug>"` và `<meta name="phong-cach" content="<slug>">` + `<meta name="chu-de-khoa" content="<data-theme đã resolve>">` trong head (Task 6 gate đọc hai meta này); alias map dùng chung ở `phong-cach/alias.json`.

- [ ] **Bước 1: Viết `phong-cach/alias.json`**

```json
{
  "_doc": "Anh xa ten chu de sang gia tri data-theme legacy. sang-lanh va toi-lanh ra doi TRUOC he phong-cach voi gia tri light/dark ghi o 41 cho; alias giu bit-compat cho thep-xanh. Chu de moi khong co alias: data-theme dung ten chu de.",
  "sang-lanh": "light",
  "toi-lanh": "dark"
}
```

- [ ] **Bước 2: Sửa `pipeline/build_html.py`**

Thêm sau khối `CHU_DE_MAC_DINH` (quanh dòng 81):

```python
PHONG_CACH_DIR = REPO / "phong-cach"
_ALIAS_CHU_DE = json.loads((PHONG_CACH_DIR / "alias.json").read_text(encoding="utf-8"))


def doc_phong_cach(meta: dict) -> dict:
    """Doc va kiem phong-cach tu front-matter. Fail-fast: vang khoa la dung ngay,
    khong co default im lang (spec v2 muc 3, dong thuan 3/3 worker phan bien)."""
    slug = meta.get("phong-cach")
    if not slug:
        raise LoiDung(
            "front-matter thieu khoa `phong-cach`. An pham moi thi chay nghi thuc chon huong:\n"
            "  python3 pipeline/orchestrator.py <bao-cao>/noi-dung.md --nghi-thuc-huong\n"
            "roi ghi `phong-cach: <slug>` vao front-matter."
        )
    duong_dan = PHONG_CACH_DIR / slug / "phong-cach.json"
    if not duong_dan.exists():
        co_san = sorted(p.name for p in PHONG_CACH_DIR.iterdir() if (p / "phong-cach.json").exists())
        raise LoiDung(f"phong-cach `{slug}` khong ton tai. Co san: {', '.join(co_san)}")
    pc = json.loads(duong_dan.read_text(encoding="utf-8"))
    if pc.get("slug") != slug:
        raise LoiDung(f"phong-cach/{slug}/phong-cach.json khai slug `{pc.get('slug')}`, lech ten thu muc")
    return pc


def data_theme_cua(pc: dict) -> str:
    """Gia tri data-theme sau alias: chu de cu giu ten legacy de thep-xanh
    khong doi mot byte; chu de moi dung thang ten."""
    chu_de = pc["chu_de_mac_dinh"]
    return _ALIAS_CHU_DE.get(chu_de, chu_de)


def khoi_token_override(pc: dict) -> str:
    """Sinh block CSS cho token_override. Dat SAU tokens.css, TRUOC lop.css."""
    if not pc.get("token_override"):
        return ""
    dong = "\n".join(f"  {k}: {v};" for k, v in pc["token_override"].items())
    return f'/* token_override cua phong-cach {pc["slug"]} */\n[data-phong-cach="{pc["slug"]}"] {{\n{dong}\n}}\n'
```

Sửa `lap_trang` (dòng 862): thêm tham số `phong_cach: dict | None = None`, và:

1. Chuỗi css: sau khi đọc 4 file gốc, nếu `phong_cach` có thì nối thêm `khoi_token_override(phong_cach)` rồi nội dung `phong-cach/<slug>/lop.css` (đọc bằng `read_text`, thiếu file thì bỏ qua vì lop.css rỗng là hợp lệ). LƯU Ý thứ tự: fonts, tokens.css, token_override, components.css, report.css, lop.css là SAI so với spec mục 3.1 (token_override phải trước components); đúng thứ tự spec: fonts, tokens.css, KHỐI TOKEN_OVERRIDE, components.css, report.css, LOP.CSS.
2. Thẻ html: `<html lang="vi" data-theme="{chu_de}" data-phong-cach="{slug}">` khi có phong_cach.
3. Head thêm hai meta ngay sau viewport khi có phong_cach:
   `<meta name="phong-cach" content="{slug}">` và `<meta name="chu-de-khoa" content="{chu_de}">`.

Sửa `dung()` (dòng 911): sau `tach_front_matter`, gọi `pc = doc_phong_cach(meta)`, tính `chu_de = data_theme_cua(pc)` (tham số `chu_de` cũ của `dung()` giữ làm override tay khi khác None, phục vụ trang nội bộ toi-lanh), truyền `phong_cach=pc` xuống `lap_trang`.

- [ ] **Bước 3: Backfill hai ấn phẩm cũ**

Thêm dòng `phong-cach: thep-xanh` vào front-matter của `examples/van-tai-bien/noi-dung.md` và `examples/mau-phase2/noi-dung.md`, ngay sau dòng `tieu_de`.

- [ ] **Bước 4: Chặn loại hình trong orchestrator**

Trong `pipeline/orchestrator.py`, bước [1/6] HÌNH: trước khi chạy `hinh/*.py`, đọc front-matter (dùng `tach_front_matter` import từ build_html) và `doc_phong_cach`; nếu `"matplotlib" in pc.get("gioi_han_loai_hinh", [])` và tồn tại bất kỳ `hinh/*.py` thì in lỗi rõ và `sys.exit(1)`:

```python
if "matplotlib" in pc.get("gioi_han_loai_hinh", []) and list(thu_muc_hinh.glob("*.py")):
    print(f"DUNG: phong-cach `{pc['slug']}` cam matplotlib (gioi_han_loai_hinh), "
          f"ma hinh/ co script .py. Doi hinh sang preset ECharts hoac minh hoa SVG.")
    sys.exit(1)
```

- [ ] **Bước 5: Fixtures và test smoke**

`tests/fixtures/phong-cach/bao-cao-thieu-khoa/noi-dung.md`: front-matter đủ `tieu_de`, `so_nguon: so-nguon.json` nhưng KHÔNG có `phong-cach`; thân một đoạn văn. `so-nguon.json`: `{"nguon": {}, "gia_tri": {}}` (nếu schema sổ nguồn tối thiểu khác, chép từ examples/mau-phase2/so-nguon.json rồi rút gọn về hợp lệ tối thiểu).

`tests/fixtures/phong-cach/bao-cao-vi-pham-loai-hinh/`: như trên nhưng có `phong-cach: thep-xanh` TẠM (Task 10 đổi sang nhung-toi khi style đó tồn tại; tạm thời test này dùng một style giả `tests/fixtures` không được, nên: tạo fixture style `do-cam-matplotlib` trong `tests/fixtures/phong-cach/` và cho orchestrator nhận đường dẫn style qua tham số môi trường KHÔNG làm; ĐƠN GIẢN HOÁ: test vi phạm loại hình chỉ bật từ Task 10 khi nhung-toi có thật, đánh dấu `test.skip` với ghi chú "cho den Task 10" và Task 10 gỡ skip).

`tests/smoke/phong_cach_build.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

test('build dung khi front-matter thieu khoa phong-cach, thong bao co huong dan', () => {
  const kq = spawnSync('python3', [
    '-c',
    [
      'import sys; sys.path.insert(0, "pipeline")',
      'import build_html as b',
      'meta, than = b.tach_front_matter(open("tests/fixtures/phong-cach/bao-cao-thieu-khoa/noi-dung.md").read())',
      'b.doc_phong_cach(meta)',
    ].join('\n'),
  ], { cwd: REPO, encoding: 'utf8' });
  assert.notEqual(kq.status, 0);
  assert.ok(kq.stderr.includes('nghi-thuc-huong'), kq.stderr);
});

test('doc_phong_cach tra ve config thep-xanh khi khoa hop le', () => {
  const kq = spawnSync('python3', [
    '-c',
    [
      'import sys; sys.path.insert(0, "pipeline")',
      'import build_html as b',
      'pc = b.doc_phong_cach({"phong-cach": "thep-xanh"})',
      'print(pc["chu_de_mac_dinh"], b.data_theme_cua(pc))',
    ].join('\n'),
  ], { cwd: REPO, encoding: 'utf8' });
  assert.equal(kq.status, 0, kq.stderr);
  assert.equal(kq.stdout.trim(), 'sang-lanh light');
});
```

- [ ] **Bước 6: Kiểm tương thích ngược bằng bản dựng thật**

```bash
python3 pipeline/orchestrator.py examples/van-tai-bien/noi-dung.md --lan=html-song
node gates/run.mjs examples/van-tai-bien/ra/noi-dung-gui-di.html --lan=html-song
```

Expected: gate y hệt trước arc (8 PASS 0 FAIL 1 SKIP). Rồi mở file kiểm bằng grep: thẻ html có `data-theme="light" data-phong-cach="thep-xanh"`, head có 2 meta mới. Vì thep-xanh có token_override rỗng và lop.css rỗng, PHẦN CSS không đổi; khác biệt duy nhất so với bản trước arc là attribute và 2 meta, đó là khác biệt CHỦ Ý đã ghi trong spec (bản v2 mục 8 nói trùng byte PHẦN NỘI DUNG; attribute mới là hạ tầng, không phải nội dung).

- [ ] **Bước 7: `npm test` toàn suite xanh, commit**

```bash
git add phong-cach/alias.json pipeline/build_html.py pipeline/orchestrator.py \
  examples/van-tai-bien/noi-dung.md examples/mau-phase2/noi-dung.md \
  tests/smoke/phong_cach_build.test.mjs tests/fixtures/phong-cach/
git commit -m "build_html doc phong-cach bat buoc, alias chu de, chan loai hinh o orchestrator"
```

---

### Task 5: gates/run.mjs sinh nghiem-thu.json, registry tên gate

**Files:**
- Modify: `gates/gates.mjs` (thêm export `TEN_GATES_PDF`)
- Modify: `gates/gates_song.mjs` (thêm export `TEN_GATES_SONG`)
- Modify: `gates/run.mjs` (cờ `--ghi-nghiem-thu=` và `--lenh-tai-tao=`)
- Modify: `tests/consistency/phong_cach.test.mjs` (nối test đối chiếu registry)

**Interfaces:**
- Produces: `node gates/run.mjs <html> [pdf] --lan=<lan> --ghi-nghiem-thu=<path> [--lenh-tai-tao="<cmd>"]` ghi JSON đúng schema spec mục 6 (các khoá: sinh_boi, ngay, sha, lenh_tai_tao, lan, phien_ban_bo_gate, gate[]); `TEN_GATES_PDF`, `TEN_GATES_SONG` là mảng tên gate đúng thứ tự chạy.
- Consumes: `inKetQuaVaThoat` hiện có; kết quả `ketQua = [{ten, trang_thai, ly_do[]}]`.

- [ ] **Bước 1: Export registry tên gate ở hai file gate**

Trong `gates/gates.mjs` và `gates_song.mjs`, ngay cạnh nơi định nghĩa danh sách gate chạy (đọc hàm `chayTatCa` / `chayTatCaSong` để tìm mảng gate), thêm export mảng tên đúng thứ tự, ví dụ ở gates_song.mjs:

```js
export const TEN_GATES_SONG = [
  'OFFLINE', 'JS-SILENT-FAIL', 'REDUCED-MOTION', 'KEYBOARD-PATH',
  'CONTRAST-ALL-THEMES', 'SIZE-BUDGET', 'NO-JS-CONTENT', 'RESPONSIVE-WIDTH', 'THEME-MATCH',
];
```

QUAN TRỌNG: chép tên từ CODE THẬT của hai file, không chép từ plan này; nếu tên trong code khác (ví dụ có tiền tố số), registry phải theo code. Thêm một assert trong chayTatCa/chayTatCaSong (hoặc test) rằng tập tên kết quả trả về đúng bằng registry, để registry không bao giờ trôi khỏi hành vi:

```js
// cuoi chayTatCaSong, truoc return:
const ten = ketQua.map((g) => g.ten);
if (JSON.stringify(ten) !== JSON.stringify(TEN_GATES_SONG)) {
  throw new Error(`Registry TEN_GATES_SONG lech ket qua that: ${ten.join(', ')}`);
}
```

- [ ] **Bước 2: Cờ ghi nghiệm thu trong run.mjs**

Trong `inKetQuaVaThoat` nhận thêm tham số `{lan, ghiNghiemThu, lenhTaiTao}`; trước `process.exit`, nếu `ghiNghiemThu`:

```js
import { execSync } from 'node:child_process';
import { TEN_GATES_PDF } from './gates.mjs';
import { TEN_GATES_SONG } from './gates_song.mjs';

function ghiNghiemThuJson(duongDan, ketQua, lan, lenhTaiTao) {
  const registry = lan === 'html-song' ? TEN_GATES_SONG : TEN_GATES_PDF;
  const sha = execSync('git rev-parse --short HEAD', { encoding: 'utf8' }).trim();
  const ho_so = {
    sinh_boi: 'gates/run.mjs --ghi-nghiem-thu',
    ngay: new Date().toISOString().slice(0, 10),
    sha,
    lenh_tai_tao: lenhTaiTao || `node gates/run.mjs ${process.argv.slice(2).filter((a) => !a.startsWith('--ghi-nghiem-thu')).join(' ')}`,
    lan,
    phien_ban_bo_gate: `${lan === 'html-song' ? 'song' : 'pdf'}-${registry.length}`,
    gate: ketQua.map((g) => {
      const muc = { ten: g.ten, ket_qua: g.trang_thai === 'WARN' ? 'PASS' : g.trang_thai };
      if (g.trang_thai === 'SKIP') muc.ly_do = g.ly_do.join('; ') || 'khong ghi ly do';
      if (g.trang_thai === 'WARN') muc.canh_bao = g.ly_do.join('; ');
      return muc;
    }),
  };
  fs.writeFileSync(duongDan, JSON.stringify(ho_so, null, 2) + '\n');
  console.log(`Da ghi nghiem thu: ${duongDan}`);
}
```

Parse cờ cạnh chỗ parse `--lan=`: `const ghiNT = (args.find((a) => a.startsWith('--ghi-nghiem-thu=')) || '').split('=')[1] || null;` và tương tự `--lenh-tai-tao=` (dùng `slice` sau dấu bằng đầu tiên vì lệnh chứa dấu bằng: `const ltIdx = args.findIndex((a) => a.startsWith('--lenh-tai-tao=')); const lenhTaiTao = ltIdx >= 0 ? args[ltIdx].slice('--lenh-tai-tao='.length) : null;`).

- [ ] **Bước 3: Nối test đối chiếu registry vào phong_cach.test.mjs**

```js
test('nghiem-thu.json cua exemplar khop registry gate hien hanh', async () => {
  const { TEN_GATES_PDF } = await import('../../gates/gates.mjs');
  const { TEN_GATES_SONG } = await import('../../gates/gates_song.mjs');
  const idx = docJson(path.join(PC, 'INDEX.json'));
  for (const e of idx.danh_sach) {
    if (e.trang_thai !== 'chinh-thuc') continue;
    const nt = docJson(path.join(REPO, e.exemplar, 'nghiem-thu.json'));
    const registry = nt.lan === 'html-song' ? TEN_GATES_SONG : TEN_GATES_PDF;
    assert.deepEqual(nt.gate.map((g) => g.ten), registry,
      `${e.slug}: tap gate trong nghiem-thu lech registry ${nt.lan}; chay lai npm run nghiem-thu`);
    for (const g of nt.gate) {
      assert.notEqual(g.ket_qua, 'FAIL', `${e.slug}: gate ${g.ten} FAIL trong nghiem-thu`);
      if (g.ket_qua === 'SKIP') assert.ok(g.ly_do, `${e.slug}: gate ${g.ten} SKIP khong ly do`);
    }
  }
});
```

- [ ] **Bước 4: Chạy thử cờ mới trên van-tai-bien, KHÔNG commit file sinh thử**

```bash
node gates/run.mjs examples/van-tai-bien/ra/noi-dung-gui-di.html --lan=html-song \
  --ghi-nghiem-thu=/tmp/nt-thu.json
cat /tmp/nt-thu.json   # kiem bang mat: du khoa, SKIP co ly_do
npm test
git add gates/ tests/consistency/phong_cach.test.mjs
git commit -m "gates/run.mjs sinh nghiem-thu.json, registry ten gate hai lan"
```

---

### Task 6: Gate KHOA-CHU-DE ở hai làn

**Files:**
- Modify: `gates/gates.mjs` (gate mới cuối danh sách, registry thành 11)
- Modify: `gates/gates_song.mjs` (gate mới cuối danh sách, registry thành 10)
- Create: `gates/fixtures/khoa-chu-de-xanh.html`, `gates/fixtures/khoa-chu-de-do-lech.html`, `gates/fixtures/khoa-chu-de-do-thieu.html`
- Modify: `tests/consistency/gate_do_xanh.test.mjs` và `gate_do_xanh_song.test.mjs` (case mới)

**Interfaces:**
- Consumes: hai meta trong head do Task 4 sinh (`phong-cach`, `chu-de-khoa`), `phong-cach/alias.json`, `phong-cach/<slug>/phong-cach.json`.
- Produces: gate `KHOA-CHU-DE` trong cả hai registry; hành vi: PASS khi (a) thẻ html có `data-theme` tường minh, (b) meta `phong-cach` tồn tại và style có thật, (c) `data-theme` == alias(`chu_de_mac_dinh` của style) == meta `chu-de-khoa`. SKIP kèm lý do khi file KHÔNG có meta `phong-cach` (trang dựng trước tầng style, ví dụ fixture cũ của gate khác). FAIL khi có meta mà lệch hoặc data-theme vắng.

- [ ] **Bước 1: Viết gate (logic dùng chung, đặt trong gates.mjs và import sang gates_song.mjs)**

```js
export function gateKhoaChuDe(html, repoRoot) {
  const ly_do = [];
  const themeAttr = (html.match(/<html[^>]*\bdata-theme="([^"]*)"/) || [])[1];
  const metaPC = (html.match(/<meta name="phong-cach" content="([^"]*)"/) || [])[1];
  const metaKhoa = (html.match(/<meta name="chu-de-khoa" content="([^"]*)"/) || [])[1];
  if (!metaPC) {
    return { ten: 'KHOA-CHU-DE', trang_thai: 'SKIP',
      ly_do: ['trang khong khai meta phong-cach, dung truoc tang style; gate khong chung minh duoc gi'] };
  }
  const pcPath = path.join(repoRoot, 'phong-cach', metaPC, 'phong-cach.json');
  if (!fs.existsSync(pcPath)) {
    return { ten: 'KHOA-CHU-DE', trang_thai: 'FAIL', ly_do: [`meta khai phong-cach ${metaPC} khong ton tai trong repo`] };
  }
  const pc = JSON.parse(fs.readFileSync(pcPath, 'utf8'));
  const alias = JSON.parse(fs.readFileSync(path.join(repoRoot, 'phong-cach', 'alias.json'), 'utf8'));
  const mong_doi = alias[pc.chu_de_mac_dinh] ?? pc.chu_de_mac_dinh;
  if (!themeAttr) ly_do.push('the html khong co data-theme tuong minh');
  else if (themeAttr !== mong_doi) ly_do.push(`data-theme="${themeAttr}" lech chu de cua style: mong doi "${mong_doi}"`);
  if (metaKhoa !== mong_doi) ly_do.push(`meta chu-de-khoa="${metaKhoa}" lech "${mong_doi}"`);
  return { ten: 'KHOA-CHU-DE', trang_thai: ly_do.length ? 'FAIL' : 'PASS', ly_do };
}
```

Nối vào cuối danh sách gate của `chayTatCa` và `chayTatCaSong`, cập nhật `TEN_GATES_PDF` (11 tên) và `TEN_GATES_SONG` (10 tên). Assert registry ở Task 5 Bước 1 sẽ tự bắt nếu quên.

- [ ] **Bước 2: Ba fixture**

`khoa-chu-de-xanh.html`: trang tối thiểu có `<html lang="vi" data-theme="light" data-phong-cach="thep-xanh">`, hai meta khớp (`phong-cach=thep-xanh`, `chu-de-khoa=light`).
`khoa-chu-de-do-lech.html`: giống hệt nhưng `data-theme="dark"`.
`khoa-chu-de-do-thieu.html`: có meta phong-cach nhưng thẻ html KHÔNG có data-theme.

- [ ] **Bước 3: Case đỏ xanh trong hai test gate hiện có, theo đúng pattern các case sẵn trong `gate_do_xanh.test.mjs` (đọc file để chép pattern gọi gate đơn lẻ). Chạy `node --test tests/consistency/gate_do_xanh.test.mjs tests/consistency/gate_do_xanh_song.test.mjs`. Expected: PASS, trong đó case đỏ chứng minh FAIL thật.**

- [ ] **Bước 4: Chạy lại gate trên van-tai-bien: giờ phải 9 PASS 0 FAIL 1 SKIP (thêm KHOA-CHU-DE PASS nhờ meta Task 4). `npm test` xanh. Commit.**

```bash
git commit -am "Gate KHOA-CHU-DE hai lan, fixture do xanh, registry 11 va 10"
```

---

### Task 7: Harvest thep-xanh: design.md, nghiem-thu máy sinh, INDEX chinh-thuc, npm run nghiem-thu

**Files:**
- Create: `phong-cach/thep-xanh/design.md`
- Create: `examples/van-tai-bien/nghiem-thu.json` (máy sinh, không viết tay)
- Create: `scripts/nghiem-thu-exemplars.mjs`
- Modify: `package.json` (script `"nghiem-thu"`)
- Modify: `phong-cach/thep-xanh/phong-cach.json` (`trang_thai` lên `chinh-thuc`)
- Modify: `phong-cach/INDEX.json` (sinh lại)
- Modify: `tests/consistency/phong_cach.test.mjs` (nối test tham chiếu tài sản trong design.md)

**Interfaces:**
- Consumes: cờ `--ghi-nghiem-thu` (Task 5), orchestrator (Task 4).
- Produces: mẫu design.md 7 phần cho Task 9-14 noi theo; `npm run nghiem-thu` tái nghiệm thu mọi exemplar chinh-thuc.

- [ ] **Bước 1: Viết `phong-cach/thep-xanh/design.md` theo đúng 7 phần spec mục 7.** Nội dung harvest từ hiện trạng: khí chất (blue editorial tổ chức, tin ở mật độ lập luận, người nhận thấy một định chế đang nói); nguồn màu (chủ đề `sang-lanh`, accent dùng cho đường nhấn và link, `pos`/`neg` chỉ trong chart và bảng, mọi màu nói bằng TÊN token); chữ (Spectral display và văn bản, IBM Plex Mono cho số và nhãn, thang chữ theo tokens.css hiện hành, không lệch doctrine 03); blueprint 7 loại ấn phẩm DẠNG BẢNG, mỗi hàng ghi component và preset bằng backtick slug lấy từ `catalog/INDEX.json` (người viết PHẢI mở catalog để chép slug thật, ví dụ `13-line-annotated`, `14-bar-ranking`; không bịa slug); motion làn song (reveal theo cuộn nhẹ, không animate số liệu, easing mặc định của mount-live); anti-pattern (tối đa 10 dòng: cấm gradient text, cấm card lồng card, cấm emoji icon, cấm accent làm màu chữ dài...); Known Gaps (chưa có bằng chứng làn pdf-so cho style này dù hạ tầng pdf là mặc định repo; điều kiện gỡ: chạy nghiệm thu một ấn phẩm pdf-so mặc thep-xanh).

- [ ] **Bước 2: Nối test tham chiếu tài sản (spec mục 6.7) vào phong_cach.test.mjs**

```js
test('design.md: tai san nhac bang backtick slug phai ton tai', () => {
  const catalog = docJson(path.join(REPO, 'catalog', 'INDEX.json'));
  const coThat = new Set(
    (Array.isArray(catalog) ? catalog : catalog.tai_san || catalog.danh_sach || [])
      .map((t) => t.slug || t.ma || t.id).filter(Boolean),
  );
  // Chi soat cac backtick co dang slug tai san (bat dau bang so hoac chua dau -)
  for (const slug of cacStyle()) {
    const p = path.join(PC, slug, 'design.md');
    if (!fs.existsSync(p)) continue;
    const md = fs.readFileSync(p, 'utf8');
    const refs = [...md.matchAll(/`([0-9][0-9a-z-]+)`/g)].map((m) => m[1]);
    for (const r of refs) {
      assert.ok(coThat.has(r), `${slug}/design.md nhac tai san khong ton tai: ${r}`);
    }
  }
});
```

LƯU Ý: đọc `catalog/INDEX.json` thật trước để biết hình dạng (mảng hay object, khoá slug tên gì) rồi chỉnh dòng lấy `coThat` cho khớp; assert thêm `coThat.size > 50` để bảo đảm parse đúng chứ không rỗng giả.

- [ ] **Bước 3: Viết `scripts/nghiem-thu-exemplars.mjs`**

```js
#!/usr/bin/env node
// Tai nghiem thu MOI exemplar chinh-thuc: chay lai orchestrator + gate, ghi de
// nghiem-thu.json. Ngoai npm test (cham); chay truoc merge lon va sau khi doi
// gate, token, font.
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const idx = JSON.parse(fs.readFileSync(path.join(REPO, 'phong-cach', 'INDEX.json'), 'utf8'));
// Duyet tu phong-cach.json (nguon) chu khong tu INDEX (INDEX ha cap khi thieu
// nghiem-thu, ma muc dich cua script nay chinh la sinh nghiem-thu).
const pcDir = path.join(REPO, 'phong-cach');
let loi = 0;
for (const slug of fs.readdirSync(pcDir)) {
  const f = path.join(pcDir, slug, 'phong-cach.json');
  if (!fs.existsSync(f)) continue;
  const pc = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (pc.trang_thai !== 'chinh-thuc' || !pc.exemplar) continue;
  const baoCao = path.join(REPO, pc.exemplar);
  const lan = fs.existsSync(path.join(baoCao, 'nghiem-thu.json'))
    ? JSON.parse(fs.readFileSync(path.join(baoCao, 'nghiem-thu.json'), 'utf8')).lan
    : 'html-song';
  const lenhOrch = `python3 pipeline/orchestrator.py ${pc.exemplar}/noi-dung.md --lan=${lan}`;
  console.log(`\n=== ${slug} (${lan}) ===\n$ ${lenhOrch}`);
  try {
    execSync(lenhOrch, { cwd: REPO, stdio: 'inherit' });
    const ten = path.basename(fs.readdirSync(path.join(baoCao, 'ra')).find((x) => x.endsWith('-gui-di.html')) || 'noi-dung-gui-di.html', '.html');
    const html = path.join(baoCao, 'ra', `${ten}.html`);
    const pdf = path.join(baoCao, 'ra', `${ten}.pdf`);
    const viTri = lan === 'html-song' ? `"${html}" --lan=html-song` : `"${html}" "${pdf}" --che-do=gui-di`;
    execSync(
      `node gates/run.mjs ${viTri} --ghi-nghiem-thu="${path.join(baoCao, 'nghiem-thu.json')}" --lenh-tai-tao="${lenhOrch}"`,
      { cwd: REPO, stdio: 'inherit' },
    );
  } catch (e) {
    loi += 1;
    console.error(`FAIL: ${slug}`);
  }
}
execSync('node phong-cach/sinh-index.mjs', { cwd: REPO, stdio: 'inherit' });
process.exit(loi ? 1 : 0);
```

Thêm vào package.json scripts: `"nghiem-thu": "node scripts/nghiem-thu-exemplars.mjs"`.

- [ ] **Bước 4: Nâng thep-xanh lên chinh-thuc và chạy trọn vòng**

```bash
# sua trang_thai trong phong-cach/thep-xanh/phong-cach.json thanh "chinh-thuc"
npm run nghiem-thu
node phong-cach/sinh-index.mjs --kiem   # INDEX da duoc script sinh lai
npm test
```

Expected: nghiem-thu.json xuất hiện ở examples/van-tai-bien/ với 10 gate làn song (9 cũ + KHOA-CHU-DE), 0 FAIL; INDEX entry thep-xanh `trang_thai: "chinh-thuc"`, `lan_da_chung_minh: ["html-song"]`; toàn suite xanh, gồm test đối chiếu registry (Task 5) giờ chạy trên dữ liệu thật.

- [ ] **Bước 5: Commit**

```bash
git add phong-cach/thep-xanh/ examples/van-tai-bien/nghiem-thu.json scripts/nghiem-thu-exemplars.mjs package.json phong-cach/INDEX.json tests/consistency/phong_cach.test.mjs
git commit -m "thep-xanh chinh-thuc: design.md harvest, nghiem-thu may sinh, npm run nghiem-thu"
```

---

### Task 8: Cập nhật luật: CLAUDE.md, doctrine/06, SKILL.md, README tầng

**Files:**
- Modify: `CLAUDE.md` (mục luật cứng khoá sáng)
- Modify: `doctrine/06-chu-de-toi.md` (mục 1, khi nào dùng)
- Modify: `SKILL.md` (thêm bước chọn phong cách trong định tuyến)
- Create: `phong-cach/README.md`

**Interfaces:**
- Consumes: mọi thứ Task 1-7 đã dựng.
- Produces: văn bản luật khớp hành vi code; SKILL.md có bước: đọc `phong-cach/INDEX.json`, lọc theo loại ấn phẩm và làn (`best_for`, `avoid_for`, `lan_da_chung_minh`), chỉ chọn entry `chinh-thuc`; ấn phẩm mới chưa chốt style thì chạy nghi thức (lệnh ở Task 15).

- [ ] **Bước 1: CLAUDE.md, thay dòng luật cứng `File giao khách phải khoá sáng...` bằng:**

```
- File giao khách phải KHOÁ chủ đề tường minh: `data-theme` trên thẻ html phải khớp
  `chu_de_mac_dinh` của phong cách trong front-matter (gate KHOA-CHU-DE canh cả hai
  làn). Chủ đề sáng vẫn là mặc định của mọi style trừ style khai bảng tối; style
  bảng tối bắt buộc khai `gioi_han_loai_hinh` chứa matplotlib, build dừng khi vi
  phạm. Điều kiện hết hiệu lực của luật "phải là light" cũ: một phong cách tự mang
  bảng màu đủ cho MỌI loại hình nó dùng thì được khoá tối.
```

- [ ] **Bước 2: doctrine/06 mục 1 thêm đoạn về nhung-toi (chủ đề tối làm BỘ MẶT MẶC ĐỊNH có khoá của một style là hợp lệ từ 2026-08; khác với "để máy khách quyết" vốn vẫn cấm). SKILL.md thêm bước chọn style ngay trước bước chọn hình. `phong-cach/README.md` ghi: luật exemplar, luật INDEX bản sinh, contract lop.css, cấm đọc design.md hàng loạt, lệnh sinh INDEX và npm run nghiem-thu.**

- [ ] **Bước 3: Chạy `node --test tests/consistency/skill_khong_lac_hau.test.mjs` (test này canh SKILL.md khớp thực tế, đọc nó nếu đỏ để biết phải khai gì thêm). `npm test` xanh. Commit: `"Luat khoa chu de tong quat, SKILL chon phong cach, README tang"`.**

---

### Task 9, 10, 11: Ba chủ đề màu mới (giay-am, nhung-toi, poster-dac)

Ba task cùng khuôn, mỗi task một chủ đề, LÀM TUẦN TỰ để mỗi lần chạy generator chỉ diff một chủ đề. Khuôn chung:

**Files (mỗi task):**
- Create: `design-system/themes/<ten>.json`
- Modify (bản sinh): `design-system/tokens.css`, `design-system/tokens.py`, `charts/echarts/theme.mjs` (qua generator, không sửa tay)
- Create (Task 9/10/11 lần lượt): `phong-cach/{giay-am,nhung-toi,poster-dac}/phong-cach.json` + `lop.css` (scope rỗng như Task 3)

**Interfaces:**
- Produces: chủ đề mới trong `PALETTES` (theme.mjs) và `THEMES` (tokens.py), khối `[data-theme="<ten>"]` trong tokens.css; style tương ứng ở trạng thái `vuon-uom`.
- Consumes: `generate-tokens.mjs` hiện có; cấu trúc JSON chép khuôn từ `sang-lanh.json` (đủ `_doc`, `chu_de`, `dung_cho`, `mau` 21 khoá, `ilus` 9 bậc).

- [ ] **Bước 1 (mỗi task): viết themes JSON với bảng màu khởi điểm dưới đây, GIỮ ĐỦ 21 khoá `mau` và 9 bậc `ilus` đúng tên khoá như sang-lanh.json.** Dải `ilus` là dải neutral CỐ ĐỊNH theo `illustrations/grammar.md`: chủ đề sáng chép nguyên của sang-lanh (bậc 1 tối nhất), chủ đề tối chép nguyên của toi-lanh (đảo bậc). KHÔNG chế dải ilus riêng.

Bảng khởi điểm `giay-am` (nền giấy ấm, accent cam đất):

```
paper #FAF6EE   paper-hi #F3EDE0   paper-hair #EBE3D3   paper-elev #F3EDE0
ink #2B2118     ink-md #55483A     ink-lo #6B5D4E       ink-faint #A89A88
line #DCD2BF    line-lo #EBE3D3
accent #A64B15  accent-hi #7E3810  accent-soft #D89B72
pos #1E7A46     neg #B3383E        neg-soft #E0A9AC     warn #8A6A0F
on-ink #FAF6EE  on-ink-md #D8CCB9  on-ink-lo #B3A48E    on-ink-line #4A3D30
```

Bảng khởi điểm `nhung-toi` (navy than sâu, vàng đồng):

```
paper #10131C   paper-hi #171B27   paper-hair #1E2432   paper-elev #161C2B
ink #EDE7DA     ink-md #C4BBA8     ink-lo #968D7B       ink-faint #5F5949
line #2A3040    line-lo #1C2230
accent #D4AF37  accent-hi #E8C766  accent-soft #8A7326
pos #4FC08D     neg #E4707F        neg-soft #6E323A     warn #E0B54C
on-ink #10131C  on-ink-md #3E4658  on-ink-lo #667082    on-ink-line #C3CBD9
```

Bảng khởi điểm `poster-dac` (trắng tuyệt đối, đỏ son báo chí):

```
paper #FFFFFF   paper-hi #F4F4F5   paper-hair #E9E9EB   paper-elev #F4F4F5
ink #0A0A0B     ink-md #3F3F46     ink-lo #62626B       ink-faint #A1A1AA
line #D4D4D8    line-lo #E9E9EB
accent #C0392B  accent-hi #8F2A20  accent-soft #E8938B
pos #157F3D     neg #C22F4E        neg-soft #E4A1AF     warn #9A6B00
on-ink #FFFFFF  on-ink-md #C9C9CE  on-ink-lo #98989F    on-ink-line #2E2E33
```

- [ ] **Bước 2 (mỗi task): kiểm contrast bằng script, CHỈNH GIÁ TRỊ tới khi đạt rồi mới ghi vào JSON.** Ngưỡng theo chuẩn đã ghi trong themes JSON hiện có: `ink`, `ink-md`, `ink-lo` trên `paper` phải >= 4,5; `line` và `accent` trên `paper` phải >= 3,0; `on-ink` trên `ink` >= 4,5. Script kiểm dùng một dòng node (không tạo file mới, WCAG relative luminance):

```bash
node -e '
const L = (h) => { const c = [0,2,4].map((i)=>parseInt(h.slice(1+i,3+i),16)/255).map((v)=>v<=0.03928?v/12.92:((v+0.055)/1.055)**2.4); return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; };
const ct = (a,b) => { const [x,y]=[L(a),L(b)].sort((p,q)=>q-p); return ((x+0.05)/(y+0.05)).toFixed(2); };
const t = require("./design-system/themes/giay-am.json").mau;
for (const k of ["ink","ink-md","ink-lo"]) console.log(k, ct(t[k], t.paper), ">=4.5?");
for (const k of ["line","accent"]) console.log(k, ct(t[k], t.paper), ">=3.0?");
console.log("on-ink/ink", ct(t["on-ink"], t.ink), ">=4.5?");
'
```

Giá trị nào hụt ngưỡng thì dịch về phía mực (tối hơn trên nền sáng, sáng hơn trên nền tối) từng nấc 8-12 đơn vị kênh màu, chạy lại script, ghi giá trị CHỐT vào JSON kèm tỷ lệ đo được vào `_doc` (noi gương toi-lanh.json).

- [ ] **Bước 3 (mỗi task): chạy generator và test drift**

```bash
node design-system/generate-tokens.mjs
node design-system/generate-tokens.mjs --kiem
npm test   # theme_tokens_drift, chart_theme phai xanh
```

- [ ] **Bước 4 (mỗi task): viết phong-cach.json cho style tương ứng** (khuôn Task 1 Bước 2, đổi các trường): giay-am `best_for: ["tom-tat-dieu-hanh"]`, `chart_palette: "giay-am"`, font kit `giay-am` (Task 12 dựng, tạm khai `"kit": "mac-dinh"` cho tới đó); nhung-toi `best_for: ["deal-pack"]`, `gioi_han_loai_hinh: ["matplotlib"]`, `chu_de_mac_dinh: "nhung-toi"`; poster-dac `best_for: ["bao-cao-nganh", "ban-tin-thi-truong"]`, `density: "cao"`. Cả ba `trang_thai: "vuon-uom"`, `exemplar` trỏ sẵn thư mục exemplar sẽ dựng (Task 12-14). Sinh lại INDEX, npm test, commit từng task một:

```bash
node phong-cach/sinh-index.mjs && npm test
git commit -am "Chu de <ten>: themes JSON qua generator, style vuon-uom"
```

Task 10 thêm một việc: gỡ `test.skip` của test vi phạm loại hình (Task 4 Bước 5), fixture `bao-cao-vi-pham-loai-hinh` đổi front-matter sang `phong-cach: nhung-toi`, test ép orchestrator exit khác 0 với thông báo chứa `gioi_han_loai_hinh`.

---

### Task 12: Font kit + exemplar giay-am (làn pdf-so)

**Files:**
- Modify: `design-system/fonts/build-fonts.py` (thêm họ font kit giay-am)
- Create: `design-system/fonts/fonts-giay-am.css` (hoặc theo pattern build-fonts.py sinh ra; ĐỌC file đó trước, theo cơ chế sẵn có)
- Modify: `pipeline/build_html.py` (font kit khác `mac-dinh` thì thay file css font khi ráp)
- Create: `phong-cach/giay-am/design.md` (7 phần, khuôn Task 7)
- Create: `examples/tom-tat-dieu-hanh-mau/{noi-dung.md, so-nguon.json, hinh/}`
- Create (máy sinh): `examples/tom-tat-dieu-hanh-mau/nghiem-thu.json`

**Interfaces:**
- Consumes: quy trình build-fonts.py + extract-ttf.py, cờ nghiệm thu (Task 5), chủ đề giay-am (Task 9).
- Produces: giay-am `chinh-thuc` với `lan_da_chung_minh: ["pdf-so"]`.

- [ ] **Bước 1: Font kit.** Đọc `design-system/fonts/build-fonts.py` để theo cơ chế sẵn có. Họ font: Fraunces (hiển thị), Source Serif 4 (văn bản), IBM Plex Mono (số, dùng lại kit sẵn). KIỂM PHỦ DẤU TRƯỚC KHI NHÚNG, cả hai họ mới:

```bash
python3 -c "
from fontTools.ttLib import TTFont
f = TTFont('<duong-dan-ttf-tai-ve>')
cmap = f.getBestCmap()
mau = 'ạằẵểịỡộừữựđĐ'
thieu = [c for c in mau if ord(c) not in cmap]
print('THIEU:', thieu if thieu else 'khong, du dau tieng Viet')
"
```

Họ nào thiếu glyph thì DỪNG và chọn họ thay thế cùng khí chất (ứng viên dự phòng: Lora thay Fraunces, Noto Serif thay Source Serif 4 nhưng nhớ gate FONT-PDF đỏ khi thấy Noto, nên dự phòng thứ hai là Source Serif 4 static). Trích ttf cho matplotlib bằng `python3 design-system/fonts/extract-ttf.py`, kiểm `findfont` theo đúng ghi chú CLAUDE.md (bẫy SemiBold nameID).

- [ ] **Bước 2: build_html.py nhận font kit.** Trong `lap_trang`, file font css: `"design-system/fonts/fonts-embedded.css"` khi kit là `mac-dinh`, ngược lại `f"design-system/fonts/fonts-{kit}.css"`; thiếu file thì LoiDung nói chạy build-fonts.

- [ ] **Bước 3: design.md giay-am** theo khuôn 7 phần; blueprint tập trung loại `tom-tat-dieu-hanh` và `thu-nha-dau-tu`; Known Gaps: chưa chứng minh làn html-song.

- [ ] **Bước 4: Exemplar `examples/tom-tat-dieu-hanh-mau/`.** Tóm tắt điều hành 2 trang: chủ đề hư cấu "Quỹ hạ tầng cảng XYZ, quý II/2026". Front-matter: `tieu_de`, `kicker: Tóm tắt điều hành, bản mẫu phong cách giay-am`, `dek` khai số minh hoạ, `phong-cach: giay-am`, `so_nguon: so-nguon.json`. Cấu trúc theo memory feedback exec-brief action-first: mở bằng verdict 3 câu, bảng mốc tín hiệu hành động (component bảng của repo), 1 chart matplotlib EIR (chọn từ catalog nhóm EIR sau khi đọc `catalog/CATALOG.md`, ưu tiên dạng bar hoặc bullet trả lời "đang đứng đâu so với ngưỡng"), 1 kpi-grid, đoạn rủi ro kèm kill-switch. so-nguon.json: 8 mã giá trị, tất cả bậc `T4_internal_estimate` hoặc `T5_derived`, ngày lấy 2026-08-10, ghi chú "số minh hoạ". Con số mock: NAV 1.850 tỷ đồng, IRR gộp 14,2%, tỷ lệ giải ngân 68%, DSCR 1,45x, còn lại tự đặt nhất quán.

- [ ] **Bước 5: Chạy trọn vòng pdf-so và nghiệm thu**

```bash
python3 pipeline/orchestrator.py examples/tom-tat-dieu-hanh-mau/noi-dung.md
node gates/run.mjs examples/tom-tat-dieu-hanh-mau/ra/noi-dung-gui-di.html \
  examples/tom-tat-dieu-hanh-mau/ra/noi-dung-gui-di.pdf --che-do=gui-di \
  --ghi-nghiem-thu=examples/tom-tat-dieu-hanh-mau/nghiem-thu.json \
  --lenh-tai-tao="python3 pipeline/orchestrator.py examples/tom-tat-dieu-hanh-mau/noi-dung.md"
```

Expected: 11 gate pdf 0 FAIL (FONT-PDF thấy Fraunces và Source Serif thật trong PDF, DIACRITICS 0 synthetic trên ký tự có dấu, KHOA-CHU-DE khớp giay-am). Đỏ gate nào sửa gate đó xong chạy lại; KHÔNG nới gate.

- [ ] **Bước 6: Nâng `trang_thai: "chinh-thuc"`, `node phong-cach/sinh-index.mjs`, `npm test`, mở PDF nhìn bằng mắt trang 1-2 (soi dấu tiếng Việt trên headline theo memory font-linux), commit.**

```bash
git commit -am "giay-am chinh-thuc: font kit Fraunces/Source Serif, exemplar tom tat dieu hanh pdf-so"
```

---

### Task 13: Font kit + exemplar poster-dac (làn html-song)

Khuôn y Task 12, các điểm khác:

- Font kit `poster-dac`: Archivo (hiển thị, có Black cho headline poster), IBM Plex Sans (văn bản), IBM Plex Mono (số, sẵn có). Kiểm phủ dấu như Task 12 Bước 1; dự phòng cho Archivo là Be Vietnam Pro (chắc chắn đủ dấu).
- `phong-cach/poster-dac/design.md`: blueprint tập trung `bao-cao-nganh` mật độ cao; anti-pattern: cấm khoảng trắng trang trí quá 25% viewport, mọi chart PHẢI có annotation sự kiện hoặc ngưỡng (đó là lý do tồn tại của style).
- Exemplar `examples/poster-nganh-mau/`: deep-dive ngành điện 4 section, 5 hình: 4 chart-song (chọn preset từ catalog theo câu hỏi: xếp hạng công suất, đường giá kèm mốc sự kiện, cơ cấu 100%, phân phối; đọc catalog trước, chép slug thật) + 1 minh hoạ ngành có bake callout. so-nguon.json 12 mã, toàn số minh hoạ. Mục tiêu stress: mỗi section 2 hình kề nhau, bảng 8 cột, đây là bài thử PAGEBREAK (không áp làn song) và RESPONSIVE-WIDTH + SIZE-BUDGET (5 hình sống một trang).
- Vòng nghiệm thu: `--lan=html-song`, kỳ vọng 10 gate song 0 FAIL; chú ý SIZE-BUDGET với 4 chart sống (bundle 786,8KB + hình tĩnh; nếu vượt trần thì giảm còn 3 chart sống 1 chart tĩnh, ghi quyết định vào design.md Known Gaps, KHÔNG nâng trần).
- Commit: `"poster-dac chinh-thuc: exemplar deep-dive nganh dien lan song"`.

---

### Task 14: Exemplar nhung-toi (làn html-song, chủ đề tối có khoá)

Khuôn y Task 12, các điểm khác:

- Font kit `nhung-toi`: Cormorant Garamond (hiển thị luxury), Source Serif 4 (văn bản, dùng chung kit giay-am nếu build-fonts cho phép tái dùng họ đã tải), IBM Plex Mono. Kiểm phủ dấu; dự phòng hiển thị: Playfair Display.
- `examples/deal-pack-mau/`: deal pack chào vốn hư cấu "Chuỗi trung tâm dữ liệu DC-Nova, vòng Series B 45 triệu USD" (mọi tên và số đều hư cấu, dek khai rõ; tinh thần cấu trúc mượn BondSample: điều khoản, use of proceeds, waterfall trả nợ, rủi ro). 4 hình: 3 chart-song + 1 minh hoạ SVG trung tâm dữ liệu từ `illustrations/` (nếu chưa có minh hoạ ngành phù hợp thì dùng minh hoạ cấu trúc vốn, chọn từ catalog). TUYỆT ĐỐI không hinh/*.py: orchestrator sẽ tự chặn nhờ Task 4 Bước 4, và đó chính là bài test sống của cơ chế chặn.
- KHOA-CHU-DE kỳ vọng: `data-theme="nhung-toi"` (không alias). CONTRAST-ALL-THEMES đo trên chủ đề khoá nhung-toi. THEME-MATCH kiểm nền chart khớp nền trang tối.
- design.md Known Gaps bắt buộc: cấm matplotlib (đã ép bằng schema), chưa có đường pdf-so (PDF nền tối in tốn mực, chưa nghiệm thu), giới hạn mount một lần của chart sống khi đổi chủ đề động.
- Commit: `"nhung-toi chinh-thuc: exemplar deal pack hu cau, chu de toi co khoa"`.

---

### Task 15: Nghi thức 3 bìa 3 phong cách (CK2 mở rộng)

**Files:**
- Modify: `pipeline/orchestrator.py` (cờ `--nghi-thuc-huong`, hàm CK2 mở rộng quanh dòng 151-183)
- Create: `tests/smoke/nghi_thuc_huong.test.mjs`

**Interfaces:**
- Consumes: `dung()` với tham số phong_cach override (thêm ở bước 1), INDEX.json với 4 entry chinh-thuc.
- Produces: `python3 pipeline/orchestrator.py <bao-cao>/noi-dung.md --nghi-thuc-huong [--lan=...]` chạy ĐƯỢC khi front-matter chưa có `phong-cach:` (đây là đường duy nhất hợp lệ cho ấn phẩm chưa chốt style), dựng bìa + section đầu tiên bằng 3 style ứng viên vào `ra/nghi-thuc/{slug}.html`, in bảng ứng viên và đường dẫn, KHÔNG hỏi y/n.

- [ ] **Bước 1: build_html.py cho phép override style:** `dung()` thêm tham số `phong_cach_override: str | None = None`; khi có, bỏ qua khoá front-matter (kể cả khi vắng) và dùng slug này. `LoiDung` vắng khoá chỉ ném khi không có override.

- [ ] **Bước 2: orchestrator:** argparse thêm `--nghi-thuc-huong` (store_true). Khi bật: đọc INDEX.json, lọc ứng viên: `trang_thai == "chinh-thuc"`, làn của lệnh nằm trong `lan_da_chung_minh`, loại ấn phẩm suy từ front-matter `phan_loai` nếu khớp được slug 7 loại thì ưu tiên entry có nó trong `best_for` và loại entry có nó trong `avoid_for`; lấy tối đa 3 (thiếu thì lấy theo thứ tự INDEX). Với mỗi ứng viên: cắt thân tới hết section `##` đầu tiên, gọi `dung(..., phong_cach_override=slug)` ghi `ra/nghi-thuc/{slug}.html`. In:

```
NGHI THUC CHON HUONG, 3 ung vien:
  1. thep-xanh    ra/nghi-thuc/thep-xanh.html
  2. giay-am      ra/nghi-thuc/giay-am.html
  3. poster-dac   ra/nghi-thuc/poster-dac.html
Chon xong, ghi `phong-cach: <slug>` vao front-matter roi chay lai orchestrator.
```

- [ ] **Bước 3: test smoke:** copy fixture `bao-cao-thieu-khoa` sang thư mục tạm, chạy orchestrator `--nghi-thuc-huong --lan=html-song` bằng spawnSync, assert exit 0, ra/nghi-thuc/ có >= 2 file html, mỗi file có `data-phong-cach` đúng slug tên file. Chạy, PASS, `npm test` xanh, commit: `"Nghi thuc 3 bia 3 phong cach: co CLI, artifact, khong y/n"`.

---

### Task 16: Khoá arc: tái nghiệm thu toàn bộ, memory repo, catalog xem trước

- [ ] **Bước 1:** `npm run nghiem-thu` chạy cả 4 exemplar từ đầu, 0 FAIL; `node phong-cach/sinh-index.mjs --kiem` sạch; `npm test` toàn suite xanh.
- [ ] **Bước 2:** Chụp 4 exemplar bằng playwright-core qua `scripts/lib/chromium.mjs` (mỗi bản 2 ảnh: bìa + section giữa) vào `catalog/xem-truoc/phong-cach/`, mở NHÌN BẰNG MẮT cả 8 ảnh soi dấu tiếng Việt và lệch bố cục (hai memory: font-linux, soi ảnh chụp sớm hơn animation thì chờ 1500ms).
- [ ] **Bước 3:** Cập nhật `memory.md` của repo: tầng phong-cách là gì, 4 style, lệnh nghi thức, luật exemplar, các bẫy đã cắn trong arc (ghi lúc này khi còn tươi).
- [ ] **Bước 4:** Commit chốt: `"Khoa arc phong-cach: 4 style chinh-thuc, 4 exemplar, xem truoc catalog"`. KHÔNG merge, KHÔNG push; báo operator nghiệm thu.

---

### Track R (song song, không chặn Task nào): research/12-style-directions

Không phải task code; giao cho 2 agent nền chạy bất kỳ lúc nào sau Task 1.

- Agent R1 (local): đọc `~/.claude/skills/huashu-design/references/design-styles.md` (40 style), `~/.claude/plugins/cache/frontend-slides/.../bold-template-pack/` (34 template, đọc selection-index.json + 5 design.md tiêu biểu), `~/.agents/skills/html-ppt/assets/themes/`. Đầu ra: `research/12-style-directions/01-kho-style-cong-dong.md`: bảng mọi style ứng viên với cột: tên, khí chất, khả thi với gate repo (font nhúng được, không blur, không gradient text), loại ấn phẩm nó phủ.
- Agent R2 (web): khảo ngôn ngữ đồ hoạ FT, Economist, Bloomberg, giải Red Dot annual report, và 5 báo cáo CTCK VN (SSI, HSC, VCSC, VND, TCBS) qua ảnh public. Đầu ra: `research/12-style-directions/02-mat-bang-va-khoang-trong.md`.
- Tổng hợp (sau khi hai bài về): `research/12-style-directions/03-shortlist.md` xếp hạng theo 3 tiêu chí spec mục 9; top 2 viết thành thư mục style `vuon-uom` (chỉ phong-cach.json + design.md, KHÔNG exemplar, không vào catalog chính thức).
- Ràng buộc: file research không em-dash; mọi nhận định về style cộng đồng phải kèm đường dẫn file nguồn cục bộ.

---

## Self-review đã chạy

1. Phủ spec: mục 1-9 spec đều có task (mục 2 Task 1-3, mục 3 Task 4, mục 3.1 Task 3, mục 4 Task 6+8, mục 5 Task 15, mục 6 Task 5+7, mục 7 Task 7 mẫu + 12-14, mục 8 Task 9-14, mục 9 Track R). Mục 10 rủi ro gắn trong từng task liên quan. Mục 11 ngoài phạm vi: không task nào đụng.
2. Placeholder: các chỗ "đọc file X trước rồi theo pattern" là chủ ý với file chưa đọc trong phiên plan (build-fonts.py, gate_do_xanh.test.mjs pattern), kèm tiêu chí chấp nhận đo được; không có TBD.
3. Nhất quán tên: `doc_phong_cach`, `data_theme_cua`, `khoi_token_override`, `validatePhongCach`, `tinhIndex`, `TEN_GATES_PDF/SONG`, `gateKhoaChuDe`, cờ `--ghi-nghiem-thu`, `--lenh-tai-tao`, `--nghi-thuc-huong` dùng thống nhất xuyên task.
