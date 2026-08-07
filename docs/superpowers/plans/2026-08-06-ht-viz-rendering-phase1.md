# HT-viz-rendering Phase 1: Nền tảng và tài sản

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng repo `~/HT-viz-rendering` thành một hệ thống chạy được từ máy sạch, với design system hợp nhất và ba nhóm hình (chart, component, minh hoạ) đã đổ vào đúng chỗ và verify được bằng một lệnh.

**Architecture:** Repo hybrid Node và Python. Một `package.json` và một `requirements.txt` ở gốc khai báo mọi phụ thuộc. Design system là nguồn chân lý duy nhất, tồn tại hai bản song song (CSS cho HTML, Python cho pipeline WeasyPrint) và có test ép hai bản luôn khớp nhau. Ba nhóm hình mỗi nhóm một thư mục tự chứa, mỗi nhóm có script verify riêng trả exit code, và một smoke test tổng gọi cả ba.

**Tech Stack:** Node 24 với `node --test` built-in, Python 3.12 với `pytest`, `playwright-core` cộng Chromium cache có sẵn, `weasyprint`, `pymupdf`, `echarts`, `matplotlib`, `d3-geo`, `topojson-client`, `topojson-simplify`.

## Global Constraints

Sao chép nguyên văn từ spec, mọi task đều phải tuân:

- **Token màu lõi**: `--ink #051C2C`, `--ink-md #42566A`, `--ink-lo #8595A6`, `--line #DBE2EA`, `--paper #FFFFFF`, `--paper-hi #F7F9FC`, `--accent #2251FF`, `--accent-hi #1233B8`, `--accent-soft #7D9BFF`, `--warn #B07A10`, `--pos #008A6D`, `--neg #C22F4E`
- **Font**: `Spectral` cho mọi vai trò chữ, `IBM Plex Mono` cho số liệu và nhãn kỹ thuật, `IBM Plex Sans` chỉ cho ô bảng và nhãn nhỏ khi bảng quá dày
- **Shadow**: chỉ offset cứng, blur-radius phải bằng 0. Cấm `box-shadow` có blur
- **Cấm tuyệt đối trong CSS**: `filter: blur()`, `backdrop-filter`, border rgba-alpha đè lên background gradient
- **Media query co giãn màn hình** phải viết `@media screen and (max-width: ...)`, không được thiếu `screen`
- **Cấm gauge và radar** trong mọi danh mục chart
- **Màu mã hoá theo chiều** (tăng/giảm), không theo tốt/xấu. Nhưng nhận định so sánh (không phải delta thời gian) thì để trung tính hoặc dùng màu âm nếu bất lợi, không tô màu dương
- **Đếm ảnh raster trong PDF** phải dùng `doc.xref_object` quét toàn bộ xref, cấm dùng `get_images` vì nó bỏ sót ảnh trong Tiling Pattern
- **Không em-dash và en-dash** trong mọi nội dung hiển thị
- **Chromium** dùng `playwright-core` với `executablePath` trỏ `~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`, không dùng MCP Playwright
- Mọi script verify phải trả **exit code**: 0 là PASS, khác 0 là FAIL

---

## File Structure

```
HT-viz-rendering/
├── package.json                 phụ thuộc Node, script npm
├── requirements.txt             phụ thuộc Python
├── design-system/
│   ├── tokens.css               nguồn chân lý màu, font, spacing, radius, shadow
│   ├── tokens.py                bản Python sinh từ tokens.css
│   └── fonts/fonts-embedded.css font base64 subset latin + vietnamese
├── components/                  nhóm B, 22 component
│   ├── components.css
│   ├── components.js
│   ├── gallery.html
│   └── catalog/                 24 file spec
├── illustrations/               nhóm C, 11 SVG
│   ├── svg/
│   ├── annotate.js
│   ├── annotate.css
│   └── catalog/
├── charts/
│   ├── echarts/                 12 chart SSR, theme.mjs, fmt.mjs
│   └── matplotlib/              48 component EIR đã vá font
├── scripts/
│   ├── verify-components.mjs    gọi được độc lập
│   ├── verify-illustrations.mjs
│   ├── verify-charts.mjs
│   └── count_raster.py
└── tests/
    ├── smoke/                   test chạy được từ máy sạch
    └── consistency/             test chống catalog drift và token drift
```

---

## Task 1: Khung repo và lệnh cài đặt duy nhất

Nền tảng cho mọi task sau. Hiện tại hai PACKAGE trong `_harvest/` không chạy được vì thiếu `node_modules`, đã kiểm chứng bằng `ERR_MODULE_NOT_FOUND: playwright-core`, exit 1.

**Files:**
- Create: `package.json`
- Create: `requirements.txt`
- Create: `tests/smoke/deps.test.mjs`
- Create: `tests/smoke/deps_test.py`

**Interfaces:**
- Consumes: không có, đây là task đầu
- Produces: `npm run verify` chạy mọi verify script Node. `npm test` chạy `node --test tests/`. Thư mục `node_modules/` ở gốc repo cho mọi script Node import trực tiếp, không qua symlink.

- [ ] **Step 1: Viết test kiểm mọi phụ thuộc Node import được**

Tạo `tests/smoke/deps.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';

const REQUIRED = [
  'playwright-core',
  'echarts',
  'd3-geo',
  'topojson-client',
  'topojson-simplify',
];

for (const pkg of REQUIRED) {
  test(`import duoc goi ${pkg}`, async () => {
    const mod = await import(pkg);
    assert.ok(mod, `${pkg} import ve undefined`);
  });
}

test('Chromium cache ton tai va chay duoc', async () => {
  const { chromium } = await import('playwright-core');
  const exe = `${process.env.HOME}/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`;
  const browser = await chromium.launch({ executablePath: exe });
  const version = browser.version();
  await browser.close();
  assert.match(version, /^\d+\./, `version bat thuong: ${version}`);
});
```

- [ ] **Step 2: Chạy test để xác nhận nó fail**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/deps.test.mjs`
Expected: FAIL với `ERR_MODULE_NOT_FOUND` cho `playwright-core`

- [ ] **Step 3: Tạo package.json**

Tạo `package.json`:

```json
{
  "name": "ht-viz-rendering",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "Sinh bao cao tai chinh tieng Viet chat luong xuat ban: HTML self-contained va PDF in duoc",
  "scripts": {
    "test": "node --test tests/",
    "verify": "node scripts/verify-components.mjs && node scripts/verify-illustrations.mjs && node scripts/verify-charts.mjs",
    "verify:components": "node scripts/verify-components.mjs",
    "verify:illustrations": "node scripts/verify-illustrations.mjs",
    "verify:charts": "node scripts/verify-charts.mjs"
  },
  "dependencies": {
    "playwright-core": "^1.49.0",
    "echarts": "^6.1.0",
    "d3-geo": "^3.1.1",
    "topojson-client": "^3.1.0",
    "topojson-simplify": "^3.0.3",
    "world-atlas": "^3.0.0"
  },
  "engines": {
    "node": ">=22"
  }
}
```

- [ ] **Step 4: Cài đặt và chạy lại test Node**

Run: `cd ~/HT-viz-rendering && npm install && node --test tests/smoke/deps.test.mjs`
Expected: PASS cả 6 test. Nếu Chromium test fail vì đường dẫn khác, chạy `ls ~/.cache/ms-playwright/` để lấy tên thư mục đúng rồi sửa hằng số trong test.

- [ ] **Step 5: Viết test kiểm phụ thuộc Python**

Tạo `tests/smoke/deps_test.py`:

```python
import importlib
import pytest

REQUIRED = ["weasyprint", "fitz", "matplotlib", "fontTools"]


@pytest.mark.parametrize("name", REQUIRED)
def test_import_duoc(name):
    mod = importlib.import_module(name)
    assert mod is not None, f"{name} import ve None"


def test_pymupdf_dem_duoc_xref():
    import fitz

    doc = fitz.open()
    doc.new_page()
    assert doc.xref_length() >= 1
    doc.close()


def test_matplotlib_backend_svg():
    import matplotlib

    matplotlib.use("svg")
    assert matplotlib.get_backend().lower() == "svg"
```

- [ ] **Step 6: Chạy test Python**

Run: `cd ~/HT-viz-rendering && python3 -m pytest tests/smoke/deps_test.py -v`
Expected: PASS. Nếu thiếu gói nào, cài bằng `pip install --break-system-packages <ten>` rồi chạy lại.

- [ ] **Step 7: Ghi requirements.txt từ những gì đang cài thật**

Run:
```bash
cd ~/HT-viz-rendering
python3 - <<'PY'
import importlib.metadata as md
names = ["weasyprint", "pymupdf", "matplotlib", "fonttools"]
lines = []
for n in names:
    try:
        lines.append(f"{n}>={md.version(n)}")
    except md.PackageNotFoundError:
        lines.append(f"# THIEU: {n}")
open("requirements.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
PY
```
Expected: in ra 4 dòng có số phiên bản thật, không dòng nào bắt đầu bằng `# THIEU`

- [ ] **Step 8: Commit**

```bash
cd ~/HT-viz-rendering
git add package.json package-lock.json requirements.txt tests/smoke/
git commit -m "Khung repo: package.json, requirements.txt, smoke test phu thuoc"
```

---

## Task 2: Design system hợp nhất, hai bản luôn khớp

Token phải tồn tại hai bản (CSS cho HTML, Python cho pipeline WeasyPrint) nhưng chỉ có một nguồn chân lý. Test ép hai bản khớp nhau, nếu ai sửa một bên mà quên bên kia thì test fail.

**Files:**
- Create: `design-system/tokens.css`
- Create: `design-system/tokens.py`
- Create: `design-system/fonts/fonts-embedded.css`
- Create: `tests/consistency/tokens_test.py`
- Source: `_harvest/lab-B-components/PACKAGE/components.css` (khối `:root`), `_harvest/lab-B-components/PACKAGE/fonts-embedded.css`

**Interfaces:**
- Consumes: `node_modules/` từ Task 1
- Produces: `design-system/tokens.py` export `COLORS` dict với 12 khoá màu, `FONTS` dict với 3 khoá, `SPACING` list 8 phần tử, `RADIUS` dict 4 khoá, `SHADOW` dict 4 khoá. `design-system/tokens.css` khai cùng bấy nhiêu biến CSS với cùng giá trị.

- [ ] **Step 1: Viết test ép hai bản token khớp nhau**

Tạo `tests/consistency/tokens_test.py`:

```python
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSS = ROOT / "design-system" / "tokens.css"


def parse_css_root():
    text = CSS.read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\}", text, re.S)
    assert block, "khong tim thay khoi :root trong tokens.css"
    out = {}
    for line in block.group(1).split("\n"):
        m = re.match(r"\s*--([a-z0-9-]+)\s*:\s*([^;]+);", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def test_css_co_du_12_mau():
    css = parse_css_root()
    expected = {
        "ink": "#051C2C",
        "ink-md": "#42566A",
        "ink-lo": "#8595A6",
        "line": "#DBE2EA",
        "paper": "#FFFFFF",
        "paper-hi": "#F7F9FC",
        "accent": "#2251FF",
        "accent-hi": "#1233B8",
        "accent-soft": "#7D9BFF",
        "warn": "#B07A10",
        "pos": "#008A6D",
        "neg": "#C22F4E",
    }
    for name, hexval in expected.items():
        assert name in css, f"thieu bien --{name} trong tokens.css"
        assert css[name].upper() == hexval.upper(), (
            f"--{name} lech: css={css[name]} mong doi={hexval}"
        )


def test_python_khop_css():
    import sys

    sys.path.insert(0, str(ROOT / "design-system"))
    import tokens

    css = parse_css_root()
    for name, hexval in tokens.COLORS.items():
        css_name = name.replace("_", "-")
        assert css_name in css, f"tokens.py co {name} nhung tokens.css khong co"
        assert css[css_name].upper() == hexval.upper(), (
            f"{name} lech giua hai ban: py={hexval} css={css[css_name]}"
        )


def test_shadow_khong_co_blur():
    css = parse_css_root()
    for name, val in css.items():
        if name.startswith("shadow"):
            parts = [p.strip() for p in val.split(",")]
            for p in parts:
                nums = re.findall(r"(-?\d+(?:\.\d+)?)px", p)
                assert len(nums) >= 3, f"--{name} thieu thanh phan: {p}"
                assert float(nums[2]) == 0.0, (
                    f"--{name} co blur={nums[2]}px, phai bang 0 (bay raster khi in)"
                )
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && python3 -m pytest tests/consistency/tokens_test.py -v`
Expected: FAIL vì `design-system/tokens.css` chưa tồn tại

- [ ] **Step 3: Trích khối token từ components.css sang tokens.css**

Run:
```bash
cd ~/HT-viz-rendering
mkdir -p design-system/fonts
python3 - <<'PY'
import re
from pathlib import Path
src = Path("_harvest/lab-B-components/PACKAGE/components.css").read_text(encoding="utf-8")
# lay tu dau file toi het khoi prefers-color-scheme (phan token)
end = src.find("/* ── 2.")
if end == -1:
    end = src.find("/* -- 2.")
assert end > 0, "khong tim thay ranh gioi cuoi khoi token"
Path("design-system/tokens.css").write_text(src[:end].rstrip() + "\n", encoding="utf-8")
print("da ghi", len(src[:end]), "ky tu")
PY
```
Expected: in ra số ký tự lớn hơn 2000

- [ ] **Step 4: Bổ sung thang spacing, radius, shadow vào tokens.css**

Thêm vào cuối khối `:root` trong `design-system/tokens.css`, ngay trước dòng `color-scheme`:

```css
  /* Spacing: lưới 4px, 8 bậc */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 32px;
  --space-8: 48px;

  /* Radius: nhỏ gần phẳng. Bo tròn lớn cộng border-left màu là dấu hiệu AI-slop */
  --radius-0: 0;
  --radius-1: 2px;
  --radius-2: 3px;
  --radius-3: 6px;

  /* Shadow con dấu: blur PHẢI bằng 0. Blur lớn hơn 0 bị Chromium nướng bitmap khi in.
     Đã đo: offset cứng cho 0 ảnh raster, có blur cho 1 ảnh raster. */
  --shadow-1: 2px 2px 0 rgba(5, 28, 44, 0.06);
  --shadow-2: 2px 2px 0 rgba(5, 28, 44, 0.08), -1px -1px 0 rgba(5, 28, 44, 0.04);
  --shadow-3: 3px 3px 0 rgba(5, 28, 44, 0.10), -1px -1px 0 rgba(5, 28, 44, 0.05);
  --shadow-none: 0 0 0 rgba(0, 0, 0, 0);
```

- [ ] **Step 5: Viết tokens.py sinh từ tokens.css**

Tạo `design-system/tokens.py`:

```python
"""Token thiet ke, ban Python cho pipeline WeasyPrint.

Nguon chan ly la tokens.css. File nay phai luon khop, co test ep
(tests/consistency/tokens_test.py). Sua mot ben ma quen ben kia thi test fail.
"""

COLORS = {
    "ink": "#051C2C",
    "ink_md": "#42566A",
    "ink_lo": "#8595A6",
    "line": "#DBE2EA",
    "paper": "#FFFFFF",
    "paper_hi": "#F7F9FC",
    "accent": "#2251FF",
    "accent_hi": "#1233B8",
    "accent_soft": "#7D9BFF",
    "warn": "#B07A10",
    "pos": "#008A6D",
    "neg": "#C22F4E",
}

FONTS = {
    "serif": '"Spectral", Georgia, "Times New Roman", serif',
    "mono": '"IBM Plex Mono", Consolas, "Courier New", monospace',
    "sans": '"IBM Plex Sans", "Segoe UI", Arial, sans-serif',
}

SPACING = [4, 8, 12, 16, 20, 24, 32, 48]

RADIUS = {"r0": 0, "r1": 2, "r2": 3, "r3": 6}

SHADOW = {
    "s1": "2px 2px 0 rgba(5, 28, 44, 0.06)",
    "s2": "2px 2px 0 rgba(5, 28, 44, 0.08), -1px -1px 0 rgba(5, 28, 44, 0.04)",
    "s3": "3px 3px 0 rgba(5, 28, 44, 0.10), -1px -1px 0 rgba(5, 28, 44, 0.05)",
    "none": "0 0 0 rgba(0, 0, 0, 0)",
}
```

- [ ] **Step 6: Chép font đã nhúng base64**

Run:
```bash
cd ~/HT-viz-rendering
cp _harvest/lab-B-components/PACKAGE/fonts-embedded.css design-system/fonts/
cp _harvest/lab-B-components/PACKAGE/build-fonts.py design-system/fonts/
ls -la design-system/fonts/
```
Expected: `fonts-embedded.css` khoảng 504 KB, `build-fonts.py` khoảng 5 KB

- [ ] **Step 7: Chạy lại test token**

Run: `cd ~/HT-viz-rendering && python3 -m pytest tests/consistency/tokens_test.py -v`
Expected: PASS cả 3 test

- [ ] **Step 8: Commit**

```bash
cd ~/HT-viz-rendering
git add design-system/ tests/consistency/
git commit -m "Design system hop nhat: tokens.css la nguon chan ly, tokens.py khop bang test"
```

---

## Task 3: Nhóm B, 22 component kể chuyện

**Files:**
- Create: `components/components.css`, `components/components.js`, `components/gallery.html`, `components/catalog/` (24 file)
- Create: `scripts/verify-components.mjs`
- Create: `scripts/count_raster.py`
- Source: `_harvest/lab-B-components/PACKAGE/`

**Interfaces:**
- Consumes: `design-system/tokens.css`, `design-system/fonts/fonts-embedded.css` từ Task 2
- Produces: `scripts/verify-components.mjs` nhận `--html=<path>` (mặc định `components/gallery.html`), chạy 6 kiểm tra, in `[PASS]` hoặc `[FAIL]` từng dòng, trả exit 0 khi tất cả PASS. `scripts/count_raster.py` nhận `<pdf-path> --max N`, in số object ảnh, trả exit 1 nếu vượt ngưỡng.

- [ ] **Step 1: Viết test smoke cho nhóm B**

Tạo `tests/smoke/components.test.mjs`:

```javascript
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
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/components.test.mjs`
Expected: FAIL với "thieu components/gallery.html"

- [ ] **Step 3: Chép tài sản nhóm B vào đúng chỗ**

Run:
```bash
cd ~/HT-viz-rendering
mkdir -p components/catalog scripts
cp _harvest/lab-B-components/PACKAGE/components.css components/
cp _harvest/lab-B-components/PACKAGE/components.js components/
cp _harvest/lab-B-components/PACKAGE/gallery.html components/
cp _harvest/lab-B-components/PACKAGE/catalog/*.md components/catalog/
cp _harvest/lab-B-components/PACKAGE/scripts/verify.mjs scripts/verify-components.mjs
cp _harvest/lab-B-components/PACKAGE/scripts/count_raster.py scripts/
ls components/catalog/ | wc -l
```
Expected: in ra `24`

- [ ] **Step 4: Gỡ khối token trùng khỏi components.css, trỏ sang design-system**

Run:
```bash
cd ~/HT-viz-rendering
python3 - <<'PY'
from pathlib import Path
p = Path("components/components.css")
src = p.read_text(encoding="utf-8")
end = src.find("/* ── 2.")
if end == -1:
    end = src.find("/* -- 2.")
assert end > 0, "khong tim thay ranh gioi cuoi khoi token"
header = (
    "/* Component ke chuyen. Token nam o design-system/tokens.css,\n"
    "   file nay KHONG duoc tu khai bao lai bien mau. */\n"
    '@import url("../design-system/tokens.css");\n\n'
)
p.write_text(header + src[end:], encoding="utf-8")
print("da cat", end, "ky tu token trung")
PY
```
Expected: in số ký tự đã cắt, lớn hơn 2000

- [ ] **Step 5: Sửa đường dẫn font trong gallery.html**

Run:
```bash
cd ~/HT-viz-rendering
python3 - <<'PY'
from pathlib import Path
p = Path("components/gallery.html")
s = p.read_text(encoding="utf-8")
s = s.replace('href="fonts-embedded.css"', 'href="../design-system/fonts/fonts-embedded.css"')
if 'design-system/tokens.css' not in s:
    s = s.replace(
        '<link rel="stylesheet" href="components.css">',
        '<link rel="stylesheet" href="../design-system/tokens.css">\n  <link rel="stylesheet" href="components.css">',
    )
p.write_text(s, encoding="utf-8")
print("ok")
PY
grep -c "design-system" components/gallery.html
```
Expected: in `ok` rồi in số lớn hơn hoặc bằng 2

- [ ] **Step 6: Sửa verify-components.mjs cho đường dẫn mặc định mới**

Trong `scripts/verify-components.mjs`, tìm chỗ đặt giá trị mặc định cho tham số `--html` và đổi thành đường dẫn tính từ gốc repo:

```javascript
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEFAULT_HTML = path.join(ROOT, 'components', 'gallery.html');
```

Rồi thay mọi chỗ dùng hằng số cũ bằng `DEFAULT_HTML`.

- [ ] **Step 7: Chạy verify thật**

Run: `cd ~/HT-viz-rendering && node scripts/verify-components.mjs; echo "exit=$?"`
Expected: mọi dòng `[PASS]`, `exit=0`. Nếu gate raster FAIL, mở PDF sinh ra rồi tìm `box-shadow` còn blur hoặc media query thiếu `screen`.

- [ ] **Step 8: Chạy lại test smoke**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/components.test.mjs`
Expected: PASS cả 4 test

- [ ] **Step 9: Commit**

```bash
cd ~/HT-viz-rendering
git add components/ scripts/verify-components.mjs scripts/count_raster.py tests/smoke/components.test.mjs
git commit -m "Nhom B: 22 component ke chuyen, token lay tu design-system, verify chay tu goc repo"
```

---

## Task 4: Nhóm C, 11 minh hoạ ngành và lớp annotation

**Files:**
- Create: `illustrations/svg/` (11 SVG), `illustrations/annotate.js`, `illustrations/annotate.css`, `illustrations/catalog/`
- Create: `illustrations/gen-vietnam-path.mjs`
- Create: `scripts/verify-illustrations.mjs`
- Source: `_harvest/lab-C-illustration/PACKAGE/`

**Interfaces:**
- Consumes: `node_modules/` từ Task 1 (cần `d3-geo`, `topojson-client`, `topojson-simplify`, `world-atlas`)
- Produces: `illustrations/annotate.js` expose `window.Annotate.annotate(svgEl, callouts, opts)` với `callouts` là mảng `{anchor: [x,y], label: {x,y}, head, sub, tone, drill}` và `tone` chỉ nhận `'neutral'`, `'negative'`, `'accent'`. `opts.axis` nhận `'vertical'` hoặc `'horizontal'`, không có tự nhận diện. `scripts/verify-illustrations.mjs` chạy hai kiểm tra hình học (độ dài đường dẫn dưới 1,6 lần, hộp nhãn nằm trọn viewBox) và trả exit code.

- [ ] **Step 1: Viết test smoke cho nhóm C**

Tạo `tests/smoke/illustrations.test.mjs`:

```javascript
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
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/illustrations.test.mjs`
Expected: FAIL vì `illustrations/svg` chưa tồn tại

- [ ] **Step 3: Chép tài sản nhóm C**

Run:
```bash
cd ~/HT-viz-rendering
mkdir -p illustrations/svg illustrations/catalog illustrations/examples
cp _harvest/lab-C-illustration/PACKAGE/illustrations/*.svg illustrations/svg/
cp _harvest/lab-C-illustration/PACKAGE/annotate.js illustrations/
cp _harvest/lab-C-illustration/PACKAGE/annotate.css illustrations/
cp _harvest/lab-C-illustration/PACKAGE/gen-vietnam-path.mjs illustrations/
cp _harvest/lab-C-illustration/PACKAGE/examples/*.html illustrations/examples/
ls illustrations/svg/ | wc -l
```
Expected: in `11`

- [ ] **Step 4: Gắn class cho đường dẫn và hộp nhãn để verify bám vào được**

Kiểm chứng cho thấy `annotate.js` tạo `<path>` và `<rect>` mà **không gắn class nào**, nên script verify không có gì để chọn. Sửa `illustrations/annotate.js` tại ba chỗ tạo element (khoảng dòng 451 tới 459), thêm thuộc tính `class`:

```javascript
// duong dan tu neo toi nhan
el("path", {
  class: "anno-leader",
  d,
  fill: "none",
  stroke: tone.line,
  "stroke-width": 1.3,
  "stroke-opacity": 0.85,
}, g);

// hop nhan
el("rect", {
  class: "anno-box",
  ...boxAttrs,
}, g);

// thanh accent ben canh hop
el("rect", { class: "anno-bar", ...accentBarAttrs, fill: tone.border }, g);
```

Giữ nguyên mọi thuộc tính cũ, chỉ thêm `class`. Đây không phải thay đổi thẩm mỹ mà là điều kiện để hình học kiểm được bằng máy.

- [ ] **Step 5: Gộp hai script verify của nhóm C thành một**

Tạo `scripts/verify-illustrations.mjs`:

```javascript
#!/usr/bin/env node
// Verify hinh hoc cho minh hoa nhom C. Hai kiem tra deu phai do bang so,
// vi sai so qua nho de mat bat duoc tren anh full-page.
import { chromium } from 'playwright-core';
import { readdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const EXE = `${process.env.HOME}/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`;
const MAX_RATIO = 1.6;
const MARGIN = 8;

let failed = 0;
const log = (ok, msg) => {
  console.log(`${ok ? '[PASS]' : '[FAIL]'} ${msg}`);
  if (!ok) failed += 1;
};

const browser = await chromium.launch({ executablePath: EXE });
const page = await browser.newPage();

const examples = readdirSync(path.join(ROOT, 'illustrations/examples')).filter((f) =>
  f.endsWith('.html'),
);

for (const file of examples) {
  const url = pathToFileURL(path.join(ROOT, 'illustrations/examples', file)).href;
  await page.goto(url, { waitUntil: 'networkidle' });

  const paths = await page.evaluate(() =>
    [...document.querySelectorAll('path.anno-leader')].map((p) => {
      const d = p.getAttribute('d') || '';
      const nums = d.match(/-?\d+(?:\.\d+)?/g) || [];
      const x1 = +nums[0];
      const y1 = +nums[1];
      const x2 = +nums[nums.length - 2];
      const y2 = +nums[nums.length - 1];
      return { len: p.getTotalLength(), straight: Math.hypot(x2 - x1, y2 - y1) };
    }),
  );
  if (paths.length === 0) {
    log(false, `${file}: khong tim thay path.anno-leader nao`);
  } else {
    const worst = Math.max(...paths.map((p) => p.len / Math.max(p.straight, 1)));
    log(worst <= MAX_RATIO, `${file}: ty le duong dan lon nhat ${worst.toFixed(3)}x (nguong ${MAX_RATIO}x)`);
  }

  const overflow = await page.evaluate((margin) => {
    const svg = document.querySelector('svg[viewBox]');
    if (!svg) return ['khong co svg[viewBox]'];
    const [, vw, vh] = svg.getAttribute('viewBox').split(/\s+/).map(Number);
    const bad = [];
    for (const r of svg.querySelectorAll('rect.anno-box')) {
      const x = +r.getAttribute('x');
      const y = +r.getAttribute('y');
      const w = +r.getAttribute('width');
      const h = +r.getAttribute('height');
      if (x < margin || y < margin || x + w > vw - margin || y + h > vh - margin) {
        bad.push(`hop tai (${x},${y}) ${w}x${h} tran khoi ${vw}x${vh}`);
      }
    }
    return bad;
  }, MARGIN);
  log(overflow.length === 0, `${file}: hop nhan trong viewBox (${overflow.length} loi)${overflow.length ? ' -> ' + overflow.join('; ') : ''}`);
}

await browser.close();
console.log(failed === 0 ? 'TAT CA PASS' : `${failed} GATE FAIL`);
process.exit(failed === 0 ? 0 : 1);
```

- [ ] **Step 6: Sửa đường dẫn tương đối trong file example**

Run:
```bash
cd ~/HT-viz-rendering
python3 - <<'PY'
from pathlib import Path
for p in Path("illustrations/examples").glob("*.html"):
    s = p.read_text(encoding="utf-8")
    s = s.replace('src="../annotate.js"', 'src="../annotate.js"')
    s = s.replace('href="../annotate.css"', 'href="../annotate.css"')
    s = s.replace('"illustrations/', '"../svg/')
    p.write_text(s, encoding="utf-8")
    print("sua", p.name)
PY
```
Expected: in tên 3 file

- [ ] **Step 7: Chạy verify thật**

Run: `cd ~/HT-viz-rendering && node scripts/verify-illustrations.mjs; echo "exit=$?"`
Expected: mọi dòng `[PASS]`, `exit=0`. Nếu class selector không khớp, mở `illustrations/annotate.js` tìm tên class thật cho đường dẫn và hộp nhãn rồi sửa hằng số trong script verify.

- [ ] **Step 8: Chạy lại test smoke**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/illustrations.test.mjs`
Expected: PASS cả 5 test

- [ ] **Step 9: Commit**

```bash
cd ~/HT-viz-rendering
git add illustrations/ scripts/verify-illustrations.mjs tests/smoke/illustrations.test.mjs
git commit -m "Nhom C: 11 minh hoa nganh, lop annotation, verify hinh hoc bang so do"
```

---

## Task 5: Nhóm A ECharts, hợp nhất bảng màu về token chốt

Nhóm A hiện dùng bảng màu khác hẳn: accent `#2a78d6`, negative `#dc2626`, font `"Calibri","Segoe UI",Arial,sans-serif`. Phải đổi về bộ chốt. Font stack cho SVG phải có fallback vì SVG có thể mở độc lập, không có font nhúng của trang.

**Files:**
- Create: `charts/echarts/` (12 file chart, `theme.mjs`, `fmt.mjs`)
- Modify: `charts/echarts/theme.mjs` (bảng màu và font stack)
- Create: `scripts/verify-charts.mjs`
- Source: `_harvest/lab-A-charts/`

**Interfaces:**
- Consumes: `design-system/tokens.py` từ Task 2 (để test đối chiếu), `node_modules/echarts` từ Task 1
- Produces: `charts/echarts/theme.mjs` export `PALETTE` với khoá `accent`, `accentHi`, `accentSoft`, `negative`, `positive`, `warn`, `ink`, `inkMd`, `inkLo`, `line`, `paper`; export `FONT_STACK` và `FONT_STACK_MONO`; export `baseOption()`, `valueAxis()`, `categoryAxis()`, `sourceGraphic()`. `charts/echarts/fmt.mjs` export `fmtNumber`, `fmtCompact`, `fmtPercent`, `fmtMultiple`, `fmtDelta`, `fmtQuarter`, `roundSigFig`, `fmtAxisLabel`.

- [ ] **Step 1: Viết test ép theme nhóm A khớp token lõi**

Tạo `tests/consistency/chart_theme.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('PALETTE cua chart khop token loi', async () => {
  const { PALETTE } = await import(path.join(ROOT, 'charts/echarts/theme.mjs'));
  const expected = {
    accent: '#2251FF',
    accentHi: '#1233B8',
    accentSoft: '#7D9BFF',
    negative: '#C22F4E',
    positive: '#008A6D',
    warn: '#B07A10',
    ink: '#051C2C',
    inkMd: '#42566A',
    inkLo: '#8595A6',
    line: '#DBE2EA',
    paper: '#FFFFFF',
  };
  for (const [k, v] of Object.entries(expected)) {
    assert.ok(k in PALETTE, `PALETTE thieu khoa ${k}`);
    assert.equal(PALETTE[k].toUpperCase(), v, `PALETTE.${k} lech: ${PALETTE[k]} mong doi ${v}`);
  }
});

test('font stack co Spectral va ket thuc bang generic keyword', async () => {
  const { FONT_STACK, FONT_STACK_MONO } = await import(path.join(ROOT, 'charts/echarts/theme.mjs'));
  assert.match(FONT_STACK, /Spectral/, 'FONT_STACK khong co Spectral');
  assert.match(FONT_STACK, /(serif|sans-serif)\s*$/, 'FONT_STACK khong ket thuc bang generic keyword, se roi dau tieng Viet');
  assert.match(FONT_STACK_MONO, /IBM Plex Mono/, 'FONT_STACK_MONO khong co IBM Plex Mono');
  assert.match(FONT_STACK_MONO, /monospace\s*$/, 'FONT_STACK_MONO khong ket thuc bang monospace');
});

test('khong file chart nao con hex cu', () => {
  const dir = path.join(ROOT, 'charts/echarts');
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.mjs'))) {
    const s = readFileSync(path.join(dir, f), 'utf8');
    for (const old of ['#2a78d6', '#dc2626', '#3c3c41', '#9a9992', '#dbdee4', 'Calibri']) {
      assert.doesNotMatch(
        s,
        new RegExp(old, 'i'),
        `${f} con gia tri cu "${old}", phai dung token loi`,
      );
    }
  }
});

test('khong chart nao la gauge hoac radar', () => {
  const dir = path.join(ROOT, 'charts/echarts');
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.mjs'))) {
    const s = readFileSync(path.join(dir, f), 'utf8');
    assert.doesNotMatch(s, /type\s*:\s*['"]gauge['"]/, `${f} dung series gauge, da bi cam`);
    assert.doesNotMatch(s, /type\s*:\s*['"]radar['"]/, `${f} dung series radar, da bi cam`);
  }
});
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && node --test tests/consistency/chart_theme.test.mjs`
Expected: FAIL vì `charts/echarts/theme.mjs` chưa tồn tại

- [ ] **Step 3: Chép tài sản nhóm A, không chép symlink node_modules**

Run:
```bash
cd ~/HT-viz-rendering
mkdir -p charts/echarts charts/echarts/out
cp _harvest/lab-A-charts/*.mjs charts/echarts/
rm -f charts/echarts/verify.mjs
ls charts/echarts/*.mjs | wc -l
test -L charts/echarts/node_modules && echo "CON SYMLINK, phai xoa" || echo "khong co symlink, dung"
```
Expected: in `14` (12 chart cộng theme cộng fmt), rồi in `khong co symlink, dung`

- [ ] **Step 4: Sửa bảng màu và font stack trong theme.mjs**

Trong `charts/echarts/theme.mjs`, thay khối `PALETTE`, `FONT_STACK` và thêm `FONT_STACK_MONO`:

```javascript
// Bang mau chot theo design-system/tokens.css. Ba nguon doc lap hoi tu cung
// bo nay: reference-kimi.html, huashu-design design-styles.md muc Two-Font
// Consulting (McKinsey deep-blue), va giao trinh thiet ke dong 88.
//
// Mau ma hoa theo CHIEU (tang/giam), khong theo TOT/XAU. Nhung nhan dinh
// so sanh (khong phai delta thoi gian) thi de trung tinh hoac dung mau am
// neu bat loi, KHONG to mau duong.
export const PALETTE = {
  accent: '#2251FF',
  accentHi: '#1233B8',
  accentSoft: '#7D9BFF',
  negative: '#C22F4E',
  positive: '#008A6D',
  warn: '#B07A10',
  ink: '#051C2C',
  inkMd: '#42566A',
  inkLo: '#8595A6',
  line: '#DBE2EA',
  paper: '#FFFFFF',
};

// PHAI ket thuc bang generic keyword. Khai bao mot ten font tran khien trinh
// duyet thay glyph theo tung ky tu va lam roi dau tieng Viet ("So lieu" thanh
// "So^' lieu", dau sac tach roi troi noi) - loi tinh vi hon tofu nen de lot QC.
export const FONT_STACK = '"Spectral", Georgia, "Times New Roman", serif';
export const FONT_STACK_MONO = '"IBM Plex Mono", Consolas, "Courier New", monospace';
```

Rồi sửa mọi tham chiếu tới khoá cũ: `PALETTE.accentDark` thành `PALETTE.accentHi`, `PALETTE.neutralDark` thành `PALETTE.ink`, `PALETTE.neutralMid` thành `PALETTE.inkLo`, `PALETTE.neutralLight` thành `PALETTE.line`, `PALETTE.surface` thành `PALETTE.paper`, `PALETTE.textPrimary` thành `PALETTE.ink`, `PALETTE.textSecondary` thành `PALETTE.inkMd`, `PALETTE.textMuted` thành `PALETTE.inkLo`, `PALETTE.gridline` thành `PALETTE.line`, `PALETTE.axisLine` thành `PALETTE.inkMd`.

Trong `TYPOGRAPHY`, đổi `fontFamily: FONT_STACK` thành `fontFamily: FONT_STACK_MONO` cho `axisLabel` (số liệu dùng mono).

- [ ] **Step 5: Viết verify-charts.mjs**

Tạo `scripts/verify-charts.mjs`:

```javascript
#!/usr/bin/env node
// Render lai toan bo chart ECharts va kiem SVG sach.
// LUU Y: echarts.init voi ssr:true KHONG tu thoat process (2 socket handle
// treo, dispose() khong giai phong). Moi script chart phai ket bang
// chart.dispose(); process.exit(0); neu khong se treo vo thoi han.
import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'charts/echarts');

let failed = 0;
const log = (ok, msg) => {
  console.log(`${ok ? '[PASS]' : '[FAIL]'} ${msg}`);
  if (!ok) failed += 1;
};

const charts = readdirSync(DIR)
  .filter((f) => /^\d\d-.*\.mjs$/.test(f))
  .sort();

for (const f of charts) {
  try {
    execFileSync('node', [path.join(DIR, f)], { cwd: DIR, timeout: 60000, stdio: 'pipe' });
  } catch (e) {
    log(false, `${f}: chay loi hoac treo -> ${e.message.split('\n')[0]}`);
    continue;
  }
  const svgName = 'out-' + f.replace('.mjs', '.svg');
  const svgPath = path.join(DIR, svgName);
  if (!existsSync(svgPath)) {
    log(false, `${f}: khong sinh ra ${svgName}`);
    continue;
  }
  const svg = readFileSync(svgPath, 'utf8');
  const problems = [];
  if (/<image/.test(svg)) problems.push('co <image>');
  if (/base64/.test(svg)) problems.push('co base64');
  if (!/Spectral|IBM Plex Mono/.test(svg)) problems.push('khong thay font chot');
  if (/#2a78d6|#dc2626|Calibri/i.test(svg)) problems.push('con gia tri mau/font cu');
  const els = (svg.match(/<(rect|path|text|line|circle|polygon)\b/g) || []).length;
  if (els < 10) problems.push(`chi ${els} phan tu, nghi ngo rong`);
  log(problems.length === 0, `${svgName}: ${els} phan tu${problems.length ? ' -> ' + problems.join(', ') : ' sach'}`);
}

console.log(failed === 0 ? 'TAT CA PASS' : `${failed} GATE FAIL`);
process.exit(failed === 0 ? 0 : 1);
```

- [ ] **Step 6: Chạy verify thật**

Run: `cd ~/HT-viz-rendering && node scripts/verify-charts.mjs; echo "exit=$?"`
Expected: 12 dòng `[PASS]`, `exit=0`. Nếu chart nào treo, mở file đó và thêm `chart.dispose(); process.exit(0);` vào cuối.

- [ ] **Step 7: Chạy lại test consistency**

Run: `cd ~/HT-viz-rendering && node --test tests/consistency/chart_theme.test.mjs`
Expected: PASS cả 4 test

- [ ] **Step 8: Commit**

```bash
cd ~/HT-viz-rendering
git add charts/echarts/ scripts/verify-charts.mjs tests/consistency/chart_theme.test.mjs
git commit -m "Nhom A ECharts: hop nhat bang mau ve token chot, font stack co generic keyword"
```

---

## Task 6: Nhóm A matplotlib EIR, vá bug font rớt dấu tiếng Việt

Bug đã tái hiện thật: `_eir_style.py` hardcode đường dẫn `liberation2` trong khi thư mục thật là `liberation`, và truyền `family` là một chuỗi tên trần thay vì list kết thúc bằng generic keyword. Hậu quả: rớt dấu tiếng Việt, "Số liệu" thành "S☐ liệu".

**Files:**
- Create: `charts/matplotlib/` (chép từ harvest)
- Modify: `charts/matplotlib/_eir_style.py`
- Create: `tests/consistency/eir_font_test.py`
- Source: `_harvest/harvest-cfa-skillchain/viz-engine/`

**Interfaces:**
- Consumes: `design-system/tokens.py` từ Task 2
- Produces: `charts/matplotlib/_eir_style.py` với hàm `setup_fonts()` trả về tuple `(sans_list, mono_list)` là hai list font kết thúc bằng generic keyword, và `save(fig, path)` xuất SVG với `svg.fonttype='none'`.

- [ ] **Step 1: Viết test bắt đúng bug font**

Tạo `tests/consistency/eir_font_test.py`:

```python
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EIR = ROOT / "charts" / "matplotlib"

VIET_TEST = "Số liệu tại 06/2026 · chiết khấu 14% · Nguồn: BCTC"


def test_khong_hardcode_liberation2():
    src = (EIR / "_eir_style.py").read_text(encoding="utf-8")
    assert "liberation2" not in src, (
        "con hardcode duong dan 'liberation2', thu muc that la 'liberation' "
        "-> os.path.exists tra False -> roi tu do ve DejaVu -> mat dau tieng Viet"
    )


def test_setup_fonts_tra_ve_list_ket_thuc_generic():
    sys.path.insert(0, str(EIR))
    import _eir_style

    sans, mono = _eir_style.setup_fonts()
    assert isinstance(sans, list), f"sans phai la list, dang la {type(sans)}"
    assert isinstance(mono, list), f"mono phai la list, dang la {type(mono)}"
    assert sans[-1] in ("sans-serif", "serif"), f"sans khong ket thuc generic: {sans}"
    assert mono[-1] == "monospace", f"mono khong ket thuc generic: {mono}"


def test_render_khong_canh_bao_thieu_glyph():
    script = f"""
import sys, warnings
sys.path.insert(0, {str(EIR)!r})
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
import _eir_style
sans, mono = _eir_style.setup_fonts()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.text(0.05, 0.5, {VIET_TEST!r}, fontfamily=sans, fontsize=12)
    ax.set_axis_off()
    fig.savefig("/dev/null", format="svg")
    plt.close(fig)
missing = [str(w.message) for w in caught if "missing from font" in str(w.message)]
print("MISSING:", len(missing))
for m in missing[:3]:
    print("  ", m)
"""
    out = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=120
    )
    assert "MISSING: 0" in out.stdout, (
        f"con canh bao thieu glyph -> se ra tofu:\n{out.stdout}\n{out.stderr}"
    )


def test_svg_giu_text_that_khong_bien_thanh_path():
    script = f"""
import sys
sys.path.insert(0, {str(EIR)!r})
import matplotlib
matplotlib.use("svg")
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
import _eir_style
sans, mono = _eir_style.setup_fonts()
fig, ax = plt.subplots(figsize=(6, 2))
ax.text(0.05, 0.5, {VIET_TEST!r}, fontfamily=sans, fontsize=12)
ax.set_axis_off()
fig.savefig("/tmp/eir_font_check.svg", format="svg")
plt.close(fig)
"""
    subprocess.run([sys.executable, "-c", script], check=True, timeout=120)
    svg = Path("/tmp/eir_font_check.svg").read_text(encoding="utf-8")
    assert "<text" in svg, "svg.fonttype khong phai 'none', chu da bien thanh path"
    assert "chiết khấu" in svg, "chu tieng Viet khong con nguyen ven trong SVG"
    assert "<image" not in svg, "SVG nhung anh raster"
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && python3 -m pytest tests/consistency/eir_font_test.py -v`
Expected: FAIL vì `charts/matplotlib` chưa tồn tại

- [ ] **Step 3: Chép engine EIR**

Run:
```bash
cd ~/HT-viz-rendering
mkdir -p charts/matplotlib
cp -r _harvest/harvest-cfa-skillchain/viz-engine/* charts/matplotlib/
ls charts/matplotlib/ | head -20
```
Expected: thấy `_eir_style.py` và các file `viz_eir*.py`

- [ ] **Step 4: Vá bug đường dẫn và bug font family**

Trong `charts/matplotlib/_eir_style.py`, thay hàm `setup_fonts` bằng:

```python
import os
from matplotlib import font_manager as fm

# Danh sach ung vien theo thu tu uu tien. Duong dan phai dung: thu muc that
# tren he la 'liberation', KHONG phai 'liberation2' (ban cu hardcode sai
# -> os.path.exists tra False -> roi tu do ve DejaVu -> mat dau tieng Viet).
_SANS_CANDIDATES = [
    ("Liberation Sans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ("DejaVu Sans", None),
]
_MONO_CANDIDATES = [
    ("Liberation Mono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ("Noto Sans Mono", "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"),
    ("DejaVu Sans Mono", None),
]


def _register(candidates):
    """Dang ky font vao cache cua matplotlib va tra ve list ten dung duoc.

    Chi dua ten suong khong du: matplotlib co cache font rieng, khong tu quet
    theo ten, phai goi addfont voi duong dan that truoc.
    """
    names = []
    for name, path in candidates:
        if path and os.path.exists(path):
            fm.fontManager.addfont(path)
            names.append(name)
        elif path is None:
            names.append(name)
    return names


def setup_fonts():
    """Tra ve (sans_list, mono_list), moi list KET THUC BANG GENERIC KEYWORD.

    Tra ve LIST chu khong phai chuoi ten tran. Khai mot ten tran khien trinh
    duyet thay glyph theo tung ky tu va lam roi dau tieng Viet: "So lieu"
    thanh "So^' lieu", dau sac tach roi troi noi. Loi nay tinh vi hon tofu
    o vuong nen rat de lot QC bang mat.
    """
    sans = _register(_SANS_CANDIDATES) + ["sans-serif"]
    mono = _register(_MONO_CANDIDATES) + ["monospace"]
    return sans, mono
```

Rồi tìm mọi chỗ trong file dùng biến `SANS` hoặc `MONO` dạng chuỗi và đổi sang gọi `setup_fonts()`.

- [ ] **Step 5: Chạy test font**

Run: `cd ~/HT-viz-rendering && python3 -m pytest tests/consistency/eir_font_test.py -v`
Expected: PASS cả 4 test. Nếu `test_render_khong_canh_bao_thieu_glyph` fail, chạy `fc-list | grep -i liberation` để xem đường dẫn thật rồi sửa hằng số.

- [ ] **Step 6: Render thử ba component khó nhất và tự soi ảnh**

Run:
```bash
cd ~/HT-viz-rendering/charts/matplotlib
python3 viz_super.py --list | head -5
python3 viz_super.py --spec examples/spec_showcase.json --out-dir /tmp/eir-check 2>&1 | tail -5
ls /tmp/eir-check/*.png | head -5
```
Expected: `--list` in ra danh sách component, render không có dòng `UserWarning: Glyph ... missing from font`

Mở ba ảnh bằng công cụ đọc ảnh và xác nhận bằng mắt: mọi chữ tiếng Việt hiển thị đủ dấu, không có ô vuông thay thế.

- [ ] **Step 7: Commit**

```bash
cd ~/HT-viz-rendering
git add charts/matplotlib/ tests/consistency/eir_font_test.py
git commit -m "Nhom A matplotlib: va bug duong dan liberation2 va bug font family chuoi tran"
```

---

## Task 7: Smoke test chống catalog drift

Bệnh đã gặp thật trong bộ Opvia: `catalog/cover_deep_page.md` mô tả HTML dùng các class không tồn tại trong CSS thật. Trang bìa vẫn chạy nhưng suy biến âm thầm, mất layout hai cột, mất đường phân cách, bullet lặp đôi. Không ai phát hiện vì không ai chạy thử.

**Files:**
- Create: `tests/consistency/catalog_drift.test.mjs`

**Interfaces:**
- Consumes: `components/catalog/` từ Task 3, `components/components.css` từ Task 3, `illustrations/catalog/` từ Task 4
- Produces: không, đây là test thuần

- [ ] **Step 1: Viết test đối chiếu catalog với CSS thật**

Tạo `tests/consistency/catalog_drift.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const CATALOG = path.join(ROOT, 'components/catalog');
const CSS = readFileSync(path.join(ROOT, 'components/components.css'), 'utf8');

// Moi class ma CSS that co dinh nghia
const definedClasses = new Set(
  [...CSS.matchAll(/\.([a-zA-Z][\w-]*)/g)].map((m) => m[1]),
);

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
    const bad = md.match(/[\u2014\u2013]/g) || [];
    assert.equal(bad.length, 0, `${file} co ${bad.length} em-dash hoac en-dash`);
  }
});
```

- [ ] **Step 2: Chạy test và ghi nhận kết quả thật**

Run: `cd ~/HT-viz-rendering && node --test tests/consistency/catalog_drift.test.mjs 2>&1 | tail -30`
Expected: có thể FAIL ở vài file. Đó là kết quả đúng nếu có drift thật.

- [ ] **Step 3: Sửa từng drift tìm được**

Với mỗi file catalog fail, mở file đó và `components/components.css`, đối chiếu tên class. Sửa file catalog cho khớp CSS thật, không sửa CSS cho khớp catalog, vì CSS là thứ đang chạy và đã được verify.

Nếu một class trong catalog thật sự cần mà CSS chưa có, đó là lỗi khác: ghi vào `docs/specs/` và xử lý riêng, đừng xoá khỏi catalog.

- [ ] **Step 4: Bổ sung mục "khi nào KHÔNG nên dùng" cho 5 file còn thiếu**

Kiểm chứng cho thấy chỉ 19 trên 24 file catalog có mục này. Năm file thiếu: `09-note-box.md`, `21-chapter-progress-bar.md`, `22-margin-dashboard-note.md`, `23-bonus-term-magazine.md`, `24-bonus-key-point-callout.md`.

Thêm vào mỗi file một mục với nội dung thật, không chung chung. Gợi ý nội dung, sửa lại nếu đọc component thấy khác:

```markdown
## KHÔNG dùng khi

- `09-note-box`: khi nội dung là một luận điểm chính của section. Note-box là ghi chú bên lề, đưa luận điểm chính vào đó là hạ cấp nó. Dùng assertion-evidence thay thế.
- `21-chapter-progress-bar`: khi báo cáo dưới 4 section. Thanh tiến trình với 2 tới 3 mốc không cho thêm thông tin gì mà chiếm chỗ.
- `22-margin-dashboard-note`: khi bản in là đầu ra chính. Ghi chú lề chuyển thành khối tĩnh khi in nên mất lợi thế theo dõi ngữ cảnh, lúc đó dùng note-box thường gọn hơn.
- `23-bonus-term-magazine`: khi thuật ngữ đã quen với người đọc mục tiêu. Giải nghĩa thứ ai cũng biết làm báo cáo nghe như tài liệu nhập môn.
- `24-bonus-key-point-callout`: khi trong một section đã có quá hai khối này. Đây là khối nhấn mạnh mạnh nhất trong bộ, dùng nhiều thì mất tác dụng nhấn.
```

- [ ] **Step 5: Chạy lại tới khi sạch**

Run: `cd ~/HT-viz-rendering && node --test tests/consistency/catalog_drift.test.mjs`
Expected: PASS toàn bộ

- [ ] **Step 6: Commit**

```bash
cd ~/HT-viz-rendering
git add tests/consistency/catalog_drift.test.mjs components/catalog/
git commit -m "Smoke test chong catalog drift: moi class trong vi du phai ton tai trong CSS that"
```

---

## Task 8: Cổng vào cho Claude và cho người

**Files:**
- Create: `SKILL.md`
- Create: `README.md`
- Create: `CLAUDE.md`
- Create: `tests/smoke/entrypoint.test.mjs`

**Interfaces:**
- Consumes: mọi thứ từ Task 1 tới 7
- Produces: `~/.claude/skills/HT-viz-rendering` là symlink trỏ tới repo, để Claude gọi được

- [ ] **Step 1: Viết test kiểm cổng vào**

Tạo `tests/smoke/entrypoint.test.mjs`:

```javascript
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
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/entrypoint.test.mjs`
Expected: FAIL vì `SKILL.md` chưa tồn tại

- [ ] **Step 3: Viết SKILL.md chỉ định tuyến**

Tạo `SKILL.md`:

```markdown
---
name: HT-viz-rendering
description: Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản, xuất HTML self-contained và PDF in được. Có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG neo được số liệu vào từng bộ phận vật thể. Dùng khi cần làm báo cáo ngành, báo cáo cổ phiếu, bản tin thị trường, hoặc deal pack.
---

# HT-viz-rendering

File này chỉ ĐỊNH TUYẾN. Đọc phần liên quan tới việc đang làm, đừng đọc hết.

## Trước khi vẽ bất cứ thứ gì

Đọc `doctrine/00-design-read.md`, rồi phát biểu một câu "đọc đề" trước khi sinh code.

## Theo việc

| Việc | Đọc |
|---|---|
| Chọn kịch bản kể chuyện cho báo cáo | `doctrine/01-narrative.md` |
| Gắn nguồn cho số liệu | `doctrine/02-evidence.md` |
| Chọn loại chart, tránh chart giả | `doctrine/03-chart-doctrine.md` |
| Viết chữ, tránh AI-slop | `doctrine/04-anti-slop.md` |
| Vẽ minh hoạ ngành | `doctrine/05-metaphor.md` rồi `illustrations/grammar.md` |
| Quyết định thiết kế khó | `doctrine/06-mindset.md` |

## Theo thành phần

| Cần | Ở đâu |
|---|---|
| Màu, font, spacing, shadow | `design-system/tokens.css` |
| Component kể chuyện | `components/catalog/` rồi `components/gallery.html` |
| Chart tĩnh cho PDF | `charts/matplotlib/` |
| Chart tương tác cho HTML | `charts/echarts/` |
| Minh hoạ ngành | `illustrations/svg/` và `illustrations/annotate.js` |

## Luật cứng, không có ngoại lệ

- Shadow chỉ dùng offset cứng, blur phải bằng 0
- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải có `screen`
- Cấm gauge và radar
- Đếm ảnh raster bằng `doc.xref_object`, không dùng `get_images`
- Không em-dash và en-dash

## Trước khi giao file

Chạy `npm run verify`. FAIL là không được giao.
```

- [ ] **Step 4: Viết README.md**

Tạo `README.md`:

```markdown
# HT-viz-rendering

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản.

## Cài đặt

```bash
npm install
pip install --break-system-packages -r requirements.txt
```

## Kiểm tra hệ thống còn sống

```bash
npm test                 # smoke test và consistency test
npm run verify           # verify cả ba nhóm hình
```

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `doctrine/` | Tầng tư duy: quyết định thiết kế thế nào cho đúng bài này |
| `design-system/` | Token màu, font, spacing. Nguồn chân lý là `tokens.css` |
| `components/` | 22 component kể chuyện, print-safe |
| `charts/echarts/` | 12 chart cho HTML tương tác |
| `charts/matplotlib/` | 48 component EIR cho PDF tĩnh |
| `illustrations/` | 11 minh hoạ ngành SVG và lớp annotation |
| `scripts/` | Script verify, mỗi cái trả exit code |
| `tests/` | Smoke test và test chống drift |
| `_harvest/` | Khu tạm chứa tài sản gốc, sẽ dỡ dần |

## Thiết kế

Đọc `docs/specs/2026-08-06-ht-viz-rendering-design.md`.
```

- [ ] **Step 5: Viết CLAUDE.md**

Tạo `CLAUDE.md`:

```markdown
# Quy ước làm việc trong repo này

## Trước khi sửa bất cứ gì

Chạy `npm test`. Nếu đang đỏ sẵn thì sửa cái đỏ trước, đừng chồng thêm.

## Khi thêm component mới

1. Thêm khối vào `components/gallery.html` và style vào `components/components.css`
2. Viết file spec trong `components/catalog/` nói rõ trả lời câu hỏi gì, đầu vào gì, **khi nào KHÔNG nên dùng**
3. Chạy `node --test tests/consistency/catalog_drift.test.mjs`. Test này ép mọi class trong ví dụ phải tồn tại thật trong CSS
4. Chạy `npm run verify:components`

## Khi sửa token

Sửa `design-system/tokens.css` trước, rồi sửa `design-system/tokens.py` cho khớp. Test `tests/consistency/tokens_test.py` sẽ bắt nếu quên một bên.

## Khi thêm chart

Bảng màu lấy từ `charts/echarts/theme.mjs`, không hardcode hex. Mọi script chart phải kết bằng `chart.dispose(); process.exit(0);` vì ECharts SSR không tự thoát process.

## Khi thêm minh hoạ

Đọc `illustrations/grammar.md` trước. Ba bài tự kiểm bắt buộc: che hết chữ mà không đọc ra biến cấu trúc thì xoá; đổi ngành mà hình vẫn dùng được nguyên thì đó là trang trí; kiểm danh sách đen.

## Không bao giờ

- Sửa CSS cho khớp catalog. Sửa catalog cho khớp CSS, vì CSS là thứ đang chạy
- Dùng `get_images()` để đếm ảnh trong PDF
- Tin một PACKAGE là tự đủ chỉ vì nó chạy được ở thư mục gốc của nó
```

- [ ] **Step 6: Chạy test cổng vào**

Run: `cd ~/HT-viz-rendering && node --test tests/smoke/entrypoint.test.mjs`
Expected: PASS cả 4 test. Nếu test đường dẫn fail, sửa `SKILL.md` bỏ tham chiếu tới file chưa tồn tại (các file `doctrine/` sẽ có ở Phase 3).

- [ ] **Step 7: Tạo symlink vào thư mục skills**

Run:
```bash
ln -sfn ~/HT-viz-rendering ~/.claude/skills/HT-viz-rendering
ls -la ~/.claude/skills/ | grep HT-viz
```
Expected: thấy symlink trỏ tới `/home/hgthinhng/HT-viz-rendering`

- [ ] **Step 8: Chạy toàn bộ test và verify một lần cuối**

Run:
```bash
cd ~/HT-viz-rendering
npm test 2>&1 | tail -20
npm run verify 2>&1 | tail -20
python3 -m pytest tests/ -v 2>&1 | tail -20
```
Expected: mọi test PASS, mọi verify exit 0

- [ ] **Step 9: Commit**

```bash
cd ~/HT-viz-rendering
git add SKILL.md README.md CLAUDE.md tests/smoke/entrypoint.test.mjs
git commit -m "Cong vao: SKILL.md dinh tuyen, README, CLAUDE.md quy uoc, symlink vao skills"
```

---

## Nghiệm thu Phase 1

Phase 1 xong khi cả bốn lệnh này chạy sạch từ một shell mới:

```bash
cd ~/HT-viz-rendering
npm install && pip install --break-system-packages -r requirements.txt
npm test
npm run verify
python3 -m pytest tests/ -v
```

Và khi mở `components/gallery.html` trong trình duyệt thấy đủ 22 component với token trắng lạnh, mở `illustrations/examples/example-vertical-axis-ship.html` thấy con tàu với 7 callout không tràn khung.

---

## Các phase tiếp theo

Phase 1 dừng ở "tài sản đã vào đúng chỗ và chạy được". Ba phase sau, mỗi phase một plan riêng, viết khi phase trước nghiệm thu xong:

**Phase 2: Pipeline và gate.** Dựng `pipeline/render_html.py`, `pipeline/render_pdf.py` dùng WeasyPrint, `pipeline/render_pptx.mjs` với `html2pptx.js` đã vá hai bug (SVG crash cả file, bảng mất trắng), `pipeline/orchestrator.py` với ba checkpoint thật. Nối sáu gate nghiệm thu và evidence ledger từ `_harvest/lab-gate/` và `_harvest/lab-evidence/`. Deliverable: từ một file nội dung ra được PDF đã qua gate.

**Phase 3: Doctrine và preset.** Viết bảy file `doctrine/`, chắt lọc từ `_harvest/harvest-mindset/`, `_harvest/harvest-extras/thinktank/`, `_harvest/harvest-misc/vn-humanizer/`, và `EIR_DESIGN.md`. Dựng bốn preset tầng 2. Deliverable: Claude ở phiên khác đọc `SKILL.md` là làm được báo cáo mà không cần hỏi lại.

**Phase 4: Báo cáo mẫu.** Làm trọn một báo cáo ngành vận tải biển, nghiệm thu bằng chính sáu gate của repo, đặt vào `examples/`. Deliverable: bản chuẩn để so mọi báo cáo về sau.
