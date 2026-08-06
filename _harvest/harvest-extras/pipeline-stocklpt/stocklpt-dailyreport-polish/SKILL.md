---
name: stocklpt-dailyreport-polish
description: "Polish skill biến nội dung tổng hợp phiên giao dịch hằng ngày của StockLPT Advisory thành PDF chuyên nghiệp theo StockLPT Design Bible. CHỈ phục vụ daily report: stat cards, bảng giá Mã/Giá/%/GTGD, mã cảnh báo khối lượng, callout cảnh báo, theme Advisory. LUÔN dùng skill này khi user paste khối văn bản tổng hợp phiên giao dịch (có 'phiên', 'VN-Index', section đánh số 01/02/03, bảng cổ phiếu Mã/Giá/%) và muốn xuất PDF, hoặc khi user nói 'polish daily', 'publish daily', '/stocklpt-daily', 'làm pdf báo cáo phiên', 'xuất pdf daily StockLPT'. KHÔNG dùng cho bài phân tích sâu/xã luận/deep dive nhiều Phần - dùng stocklpt-deepanalysis-polish thay vào đó."
---

# StockLPT Daily Report Polish Skill

Biến text tổng hợp phiên giao dịch hằng ngày của StockLPT Advisory thành PDF chuyên nghiệp theo chuẩn StockLPT Design Bible. Skill này CHỈ phục vụ daily report (information density: stat cards, bảng giá, mã cảnh báo). Cho bài phân tích sâu/xã luận dùng `stocklpt-deepanalysis-polish`.

---

## Quy tắc CỨNG (đọc trước khi làm gì)

1. **TUYỆT ĐỐI không dùng em-dash `—` (U+2014) hay en-dash `–` (U+2013)**. Thay bằng `-` ASCII. QC tự động fail nếu phát hiện.
2. Không dùng `#FFFFFF` thuần làm nền. Không dùng `#000000` làm text.
3. Heading dùng Spectral (serif). Số liệu dùng IBM Plex Mono. Body dùng Inter.
4. Bảng màu: Indigo `#2A1A4A`, Accent `#16633C`, Slate `#514B78`, Ivory `#EBEFF4`, Charcoal `#221A34`. Bordeaux `#7A1F35` chỉ cho rủi ro nghiêm trọng.
5. **Dùng module `render.py` đi kèm skill** để có CSS đúng và font setup chuẩn. Không tự viết lại CSS.
6. **Thương hiệu StockLPT:** bảng màu + wordmark "STOCKLPT ADVISORY" ở mục 4 là palette native (ink tím huyền, accent deep forest, giấy off-white mát), áp thẳng khi render. Không cần truyền brand.
6. Schema bảng phải khớp với loại dữ liệu thực sự có. KHÔNG bịa cột bằng `-` cho dữ liệu không tồn tại (ví dụ bảng cảnh báo khối lượng chỉ cần Mã/GTGD/Ghi chú, không cần Giá/Phiên).

---

## Workflow

```
Input text -> Extract metadata -> Build HTML body -> Call render.render_pdf
```

---

## Bước 1: Setup môi trường

Skill folder structure:
```
stocklpt-dailyreport-polish/
├── SKILL.md       (file này)
├── render.py      (module CSS + render functions)
└── fonts/         (16 woff2 files cần thiết)
```

Khi dùng skill, copy folder vào working dir và import module:

```python
import sys
SKILL_DIR = "/path/to/stocklpt-dailyreport-polish"  # path thực tế khi run
sys.path.insert(0, SKILL_DIR)
from render import build_css, render_pdf, qc_check
```

---

## Bước 2: Extract metadata

Parse từ text input:
- **Ngày**: pattern `DD/MM/YYYY` trong text
- **Tiêu đề**: thường là "Tổng hợp phiên DD/MM/YYYY"
- **Sub-brand**: luôn là `ADVISORY` cho daily report

---

## Bước 3: Phân tích nội dung và đánh dấu emphasis

### 3a. "Thông điệp chính" -> `.callout.key` (BẮT BUỘC)
Đoạn tổng kết quan trọng nhất, thường ở cuối báo cáo. 1 lần duy nhất, gần cuối.

### 3b. Inline mark -> `<mark>`
Wrap cụm từ/số liệu quan trọng nhất. Quy tắc:
- 3-6 từ, KHÔNG wrap toàn câu
- Tối đa 1-2 mark mỗi đoạn
- Wrap những thứ như: "phá vỡ vùng tích lũy", "chỉ 35%", "đảo chiều 2 bậc"

### 3c. Cấp độ callout
- `.callout.key`: Thông điệp chính (Indigo background, ivory text)
- `.callout.warn`: Cảnh báo rủi ro, "cắt lỗ" (Bordeaux border)
- `.callout`: Default, ghi chú thêm (Accent border)

### 3d. Bảng - linh hoạt schema
- **Bảng giá**: 5 cột (Mã, Giá, Phiên, GTGD, Nhận xét)
- **Bảng cảnh báo khối lượng**: 3 cột (Mã, GTGD, Ghi chú) - KHÔNG cần Giá/Phiên
- **Bảng tín hiệu**: 3 cột (Mã, Tín hiệu, Ghi chú)
- **Spotlight row**: max 1 row mỗi bảng cho entry quan trọng nhất
- **Ticker badge**: cột Mã dùng `<span class="ticker-badge">VIC</span>`
- **"Mới" badge**: entry mới thêm `<span class="badge-new">Mới</span>` trong cột nhận xét

### 3e. Text styling
- **Tickers in-text**: `<span class="t">VIC</span>` (bold + navy)
- **Tín hiệu cột text**: `<span class="sig-pos">Tích lũy mạnh</span>` hoặc `sig-neg`
- **Numbers cột**: `<td class="num">86.700</td>`, `<td class="pos">+6,9%</td>`, `<td class="neg">-0,9%</td>`

---

## Bước 4: Template HTML

```html
<div class="cover-daily">
  <div class="top-accent"></div>
  <div class="brand-row">STOCKLPT ADVISORY</div>
  <h1>Tổng hợp phiên DD/MM/YYYY</h1>
  <!-- KHONG them date-display, KHONG them tags - title đã chứa ngày -->
</div>
<div class="path-strong"></div>

<div class="content">
  <!-- 4 STAT CARDS: number is the hero (22pt), unit small (13pt), context line below -->
  <div class="stat-bar">
    <div class="stat-card [neg-card|pos-card]">
      <div class="stat-label">Tên chỉ số</div>
      <div class="stat-value-wrap">
        <span class="stat-value">47</span><span class="stat-unit">%</span>
      </div>
      <div class="stat-context">↓ từ 50% hôm qua</div>
    </div>
    <!-- ... 3 cards khác -->
  </div>

  <!-- EXEC SUMMARY -->
  <div class="exec-summary">
    <div class="exec-label">Điểm chính phiên hôm nay</div>
    <ul>
      <li><span class="t">VIC</span> ...</li>
    </ul>
  </div>
  <div class="path"></div>

  <!-- SECTIONS -->
  <div class="section-header">
    <span class="section-num">01.</span>
    <span class="section-title">Bức tranh chung</span>
  </div>
  <p>Nội dung với <span class="t">CTD</span> và <mark>cụm quan trọng</mark>.</p>

  <h3>Tiêu đề con uppercase</h3>
  <table>
    <thead><tr><th>Mã</th><th class="th-num">Giá</th><th class="th-num">Phiên</th><th class="th-num">GTGD</th><th>Nhận xét</th></tr></thead>
    <tbody>
      <tr class="spotlight">
        <td><span class="ticker-badge">CTD</span></td>
        <td class="num">86.700</td>
        <td class="pos">+6,9%</td>
        <td class="num">67 tỷ</td>
        <td>Mạnh nhất phiên <span class="badge-new">Mới</span></td>
      </tr>
    </tbody>
  </table>

  <!-- CALLOUTS theo cấp độ -->
  <div class="callout"><p>Ghi chú thêm</p></div>
  <div class="callout warn"><p>Cảnh báo rủi ro</p></div>

  <!-- BẮT BUỘC: 1 callout key cho thông điệp chính -->
  <div class="callout key">
    <div class="key-label">Thông điệp chính</div>
    <p>Đoạn tổng kết quan trọng nhất với <strong>điểm key</strong>.</p>
  </div>

  <!-- DISCLAIMER CARD -->
  <div class="disclaimer-card">
    <div class="disclaimer-label">Tuyên bố miễn trừ trách nhiệm</div>
    <p>STOCKLPT Advisory biên soạn cho ngày DD/MM/YYYY... <strong>không phải khuyến nghị đầu tư</strong>...</p>
  </div>
</div>
```

---

## Bước 5: Render PDF

```python
import sys
SKILL_DIR = "/path/to/stocklpt-dailyreport-polish"
sys.path.insert(0, SKILL_DIR)
from render import build_css, render_pdf

DATE = "23/04/2026"

css = build_css(date_str=DATE)

body = """
<div class="cover-daily">...</div>
<div class="content">
  ... toàn bộ nội dung HTML ...
</div>
"""

html = f'''<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><style>{css}</style></head>
<body>{body}</body></html>'''

render_pdf(html, "/mnt/user-data/outputs/STOCKLPT_DAILY_20260423.pdf")
```

**Naming convention:** `STOCKLPT_DAILY_YYYYMMDD.pdf`

---

## Ghi chú kỹ thuật WeasyPrint

1. **Vietnamese fonts**: `unicode-range` không hoạt động đúng trong WeasyPrint. Phải tách 2 font-family riêng (Inter/InterVN) và dùng font stack `'Inter', 'InterVN', sans-serif`. CSS engine sẽ fallback per-character. `render.py` đã setup đúng.

2. **Footer dính chùm**: KHÔNG dùng `position: running()` với element flex bên trong. Dùng `@bottom-left` / `@bottom-right` trực tiếp trong `@page`, inject date qua Python f-string.

3. **Top margin trang 2+**: Dùng `@page { margin: 16mm 0 16mm 0 }` + `@page :first { margin-top: 0 }`. Trang 1 cover bleed full top, trang sau có breathing room.

4. **Viewport units**: Không hỗ trợ `vh/vw`. Dùng `mm` hoặc `pt`.

---

## QC Checklist (tự động + manual)

`render.qc_check()` tự động kiểm tra:
- [x] Em-dash / en-dash
- [x] `.callout.key` bắt buộc
- [x] `.disclaimer-card` bắt buộc
- [x] Min ticker-badge count
- [x] No date-display redundancy

Manual check trước khi deliver:
- [ ] Cover gọn: chỉ brand-row + h1, không date riêng, không tags
- [ ] Stat cards: 4 cards, mỗi card có label + value + unit + context
- [ ] Số liệu: `.num` 10pt weight 600 ink color, `.pos`/`.neg` 10pt weight 700
- [ ] Tickers: `.t` (bold + navy) trong text, `.ticker-badge` trong bảng
- [ ] Bảng cảnh báo khối lượng: 3 cột, không bịa Giá/Phiên
- [ ] Spotlight row: 1 entry quan trọng nhất mỗi bảng
- [ ] "Mới" badge cho entry lần đầu
- [ ] Disclaimer card có label "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM" + padding rõ
- [ ] Footer 2 cột tách nhau (left: brand+date, right: số trang)

---

## Naming và output

```
/mnt/user-data/outputs/STOCKLPT_DAILY_YYYYMMDD.pdf
```

Sau khi render, gọi `present_files` để user download.


## Wave 7 Daily Report Enhancements (mới)

Skill này cung cấp 3 components nâng cấp cho daily report. Import từ `render.py`:

```python
from render import build_full_css, stat_card_pro, money_flow, daily_compare
```

`build_full_css()` (không phải `build_css()`) tự include Wave 7 styles.

### 1. `stat_card_pro` - stat card với delta arrow + inline sparkline

Thay thế stat cards cũ. Mỗi card có: label uppercase + value mono + delta arrow (▲/▼/─) + inline sparkline SVG bên phải + context italic.

```python
stat_card_pro(
    label="VN-INDEX",
    value="1.347,82",
    delta="+0,68% (+9,15)",
    delta_type="up",  # 'up' | 'down' | 'flat'
    spark_data=[1305, 1310, 1315, 1322, 1318, 1325, 1330, 1335, 1340, 1342, 1345, 1347],
    context="Phiên xanh thứ 4 liên tiếp. Khối ngoại mua ròng 285 tỷ.",
)
```

Sparkline color tự động: green (up), red (down), slate (flat). Dùng grid 2-col cho 4 cards thường.

### 2. `money_flow` - dòng vào vs dòng ra

2 columns side-by-side: DÒNG VÀO (green) vs DÒNG RA (red), mỗi side có total mono lớn + items list.

```python
money_flow(
    title="Khối ngoại - dòng tiền theo nhóm cổ phiếu",
    inflow_total="+1.245 tỷ",
    outflow_total="-960 tỷ",
    inflows=[
        {"name": "Ngân hàng (Big4)", "value": "+520 tỷ"},
        {"name": "VPB", "value": "+285 tỷ"},
        ...
    ],
    outflows=[
        {"name": "Thép (HPG)", "value": "-385 tỷ"},
        ...
    ],
)
```

### 3. `daily_compare` - bảng so sánh hôm nay vs hôm qua

4-column grid (chỉ số / hôm qua muted / hôm nay vivid / Δ delta arrow).

```python
daily_compare(
    title="So sánh phiên - chỉ số chính",
    today_label="HÔM NAY",
    yesterday_label="HÔM QUA",
    rows=[
        {"metric": "VN-Index điểm đóng cửa", "yesterday": "1.338,67", "today": "1.347,82", "delta": "+9,15", "delta_type": "up"},
        {"metric": "Thanh khoản HOSE (tỷ đ)", "yesterday": "24.400", "today": "22.450", "delta": "-1.950", "delta_type": "down"},
        ...
    ],
)
```

Delta arrows: ↑ up green, ↓ down red, → flat gray. Dùng để cho reader scan changes nhanh.

### Usage pattern

```python
from render import build_full_css, stat_card_pro, money_flow, daily_compare

css = build_full_css(date_str=DATE)

SC_VNINDEX = stat_card_pro(label="VN-INDEX", value="1.347,82", ...)
SC_USDVND = stat_card_pro(label="USD/VND", value="26.105", ...)
FLOW = money_flow(title="...", inflows=[...], outflows=[...])
COMPARE = daily_compare(title="...", rows=[...])

body = f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4mm;">
{SC_VNINDEX}
{SC_USDVND}
</div>

{FLOW}

{COMPARE}
"""
```
