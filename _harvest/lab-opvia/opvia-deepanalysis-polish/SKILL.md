---
name: opvia-DeepAnalysis-polish
description: Polish skill biến bài phân tích sâu/xã luận tài chính của Opvia Research thành PDF editorial-grade premium - cảm giác đọc tạp chí kinh tế cao cấp (The Economist, Stratechery, Atlantic). CHỈ phục vụ deep analysis: layout 3-stage (cover -> TOC -> content), drop cap, header strip per-page, body breathable trên paper warm, Playfair Display + Inter + JetBrains Mono. LUÔN dùng skill này khi user paste nội dung essay phân tích nhiều Phần (Phần I/II/III...), có lập luận dài, KHÔNG phải báo cáo phiên giao dịch, hoặc khi user nói 'polish analysis', 'publish deep', '/opvia-deep', 'xuất pdf bài phân tích sâu', 'làm pdf editorial Opvia', 'deep analysis polish'. KHÔNG dùng cho daily report - dùng opvia-DailyReport-polish thay vào đó.
---

# Opvia Deep Analysis Polish Skill

Biến text bài phân tích sâu / xã luận tài chính thành PDF editorial-grade premium theo chuẩn Opvia Research. Dành riêng cho bài phân tích sâu, có lập luận dài, cấu trúc essay nhiều Phần. Cho daily report dùng `opvia-DailyReport-polish` thay vào đó.

**Triết lý design:** PDF đọc trên màn hình (digital publish). Layout breathable: line-height 1.78, font 10.5pt, gap giữa paragraph, drop cap subtle, header strip per-page, magazine-style TOC. Body trên paper warm `#FAF7F0`. Mỗi Phần luôn bắt đầu trang mới.

**Pipeline đầy đủ:**
```
text gốc 
  -> [opvia-content-refine: chải chuốt từ ngữ] 
  -> text sạch 
  -> [opvia-data-viz: build viz cho key data points] 
  -> [skill này: layout editorial + render PDF]
```

Skill này CHỈ làm visual layout. Nếu thấy content còn nhiều Vietlish ("technical fix", "trade-off", "headroom"...), DỪNG và đề xuất user chạy `opvia-content-refine` trước.

**Tích hợp data-viz:** Skill `opvia-data-viz` cung cấp 6 components SVG/CSS cho bài analysis (gauge, bar_horizontal, heatmap, flow_bridge, scenario_cards, timeline_horizontal). Khi build CSS, thêm `viz_styles()`:

```python
from render import build_css
from viz import viz_styles  # từ opvia-data-viz

css = build_css(date_str=DATE, short_title=SHORT_TITLE) + viz_styles()
```

Sau đó dùng viz functions để build HTML chunks và inject vào body. Xem `opvia-data-viz/SKILL.md` để biết chi tiết.

---

## Quy tắc CỨNG

1. **TUYỆT ĐỐI không em-dash `—` (U+2014) hay en-dash `–` (U+2013)**. Thay bằng `-` ASCII.
2. Body bg dùng `--paper` `#FAF7F0` (KHÔNG `#FFFFFF` thuần). Text dùng `--charcoal` (KHÔNG `#000000`).
3. **Heading**: Playfair Display (PFD). **Số liệu**: JetBrains Mono. **Body**: Inter.
4. **PFD italic CHỈ ở signature places** (pull quote, formula, conclusion, h4) - KHÔNG cho dek/intro/repeating elements (giảm AI-feel).
5. **H3 KHÔNG uppercase letterspaced** - dùng Inter normal-case + thin brass underline (uppercase letterspaced là source chính của AI-feel).
6. Bảng màu: Prussian `#003153`, Prussian-900 `#000d18` (cover), Brass `#B5A642`, Slate `#4A6FA5`, Ivory `#F5F1E8`, Paper `#FAF7F0`, Charcoal `#2B2B2B`, Bordeaux `#722F37`.
7. **Layout 3-stage**: Cover (page 1) → TOC + alert inline (page 2) → Content (page 3+) với header strip. Mỗi Phần I-VII bắt đầu trang mới.
8. **Eyebrow tiếng Việt thuần** (KHÔNG "BANKING & MACRO" - dùng "Ngân hàng & Vĩ mô").
9. Nếu source có Phụ lục Thuật ngữ → render thành `.glossary-section` ở cuối.

---

## Setup môi trường

```
opvia-DeepAnalysis-polish/
├── SKILL.md
├── render.py     (CSS + render functions)
└── fonts/        (16 woff2 files)
```

```python
import sys
SKILL_DIR = "/path/to/opvia-DeepAnalysis-polish"
sys.path.insert(0, SKILL_DIR)
from render import build_css, render_pdf
```

---

## Bước 1: Extract metadata

7 thứ cần chuẩn bị:
- **`date_str`**: format `DD/MM/YYYY`
- **`short_title`**: 5-8 từ UPPERCASE cho header strip per-page (ví dụ "ĐỀ XUẤT SỬA ĐỔI THÔNG TƯ 22")
- **`title_main`**: tiêu đề đầy đủ trên cover
- **`subtitle`**: dòng phụ italic 1 câu, ~10-15 từ
- **`dek`**: tóm tắt 50-80 từ trên cover (3-4 câu, KHÔNG copy nguyên văn từ bài)
- **`hero_stat`**: 1 con số signature ("111,9%", "406K"...) + label uppercase + desc
- **`takeaways`**: 3 bullets điểm chính (mỗi bullet `<strong>...</strong>` mở đầu + giải thích 1-2 câu)

**Eyebrow + issue:** ghép từ topic + tháng/năm bằng tiếng Việt. Ví dụ "Ngân hàng & Vĩ mô" + "Số tháng 4 · 2026 · Opvia Research".

---

## Bước 2: Build cover hero-landing (page 1)

```html
<div class="cover-deep">
  <!-- MAGAZINE MASTHEAD: brand center, info row 2-cột -->
  <div class="cover-masthead">
    <div class="masthead-rule-top"></div>
    <div class="masthead-brand">OPVIA RESEARCH</div>
    <div class="masthead-rule-mid"></div>
    <div class="masthead-meta">
      <div class="meta-left">Ngân hàng &amp; Vĩ mô</div>
      <div class="meta-right">Số tháng 4 · 2026</div>
    </div>
  </div>

  <h1>Đề xuất sửa đổi<br/>Thông tư 22/2019</h1>
  <div class="cover-subtitle">Ai hưởng lợi, ai chịu thiệt?</div>
  <div class="cover-dek">Khi LDR hệ thống chạm 111,9%...</div>

  <div class="cover-hero-stat">
    <div class="cover-hero-num">111,9%</div>
    <div class="cover-hero-cap">
      <div class="cover-hero-label">Tỷ lệ LDR hệ thống · 30/3/2026</div>
      <div class="cover-hero-desc">Mức cao kỷ lục, vượt xa trần quy chế 85%.</div>
    </div>
  </div>

  <div class="cover-takeaways">
    <div class="cover-takeaways-label">Trong bài này</div>
    <ul>
      <li><strong>Tái phân phối, không phải nới lỏng.</strong> Sửa Thông tư 22 là chỉnh quy tắc kỹ thuật...</li>
      <li><strong>Hai phương án Điều 16 cho kết quả ngược nhau.</strong> Nới SFL hay thay NSFR...</li>
      <li><strong>Lợi ích phân phối bất đối xứng.</strong> Big4 hưởng lợi gấp đôi...</li>
    </ul>
  </div>

  <div class="cover-bottom-rule"></div>
  <div class="cover-meta-strip">
    <div class="meta-block"><strong>Biên soạn</strong>OPVIA Research</div>
    <div class="meta-block"><strong>Đọc trong</strong>14 phút</div>
    <div class="meta-block"><strong>Phát hành</strong>25/04/2026</div>
  </div>
</div>
```

**Masthead structure (mới):**
- `masthead-rule-top`: brass thick rule short (56mm centered) - signature mark
- `masthead-brand`: "OPVIA RESEARCH" PFD bold 14pt brass uppercase letterspaced - prominent center
- `masthead-rule-mid`: brass thin rule full-width - separator
- `masthead-meta`: 2-col flex justify-between
  - `meta-left`: category tiếng Việt (e.g. "Ngân hàng & Vĩ mô") brass-300 sans 8.5pt 700
  - `meta-right`: issue (e.g. "Số tháng 4 · 2026") mono ivory 8pt 500

Bố cục đậm tính editorial, không còn cảm giác "label nhạt" như cấu trúc cũ.

Page 1 single block height 297mm + padding 24mm; KHÔNG flex height. Hero stat mono brass 44pt. Bullets brass arrow markers. Hero desc Inter regular (KHÔNG italic).

---

## Bước 3: Build TOC + alert inline (page 2)

```html
<div class="toc-page">
  <div class="toc-eyebrow">Trong số này</div>
  <div class="toc-title-main">Bảy phần.<br/>Một câu hỏi: ai sẽ hưởng lợi?</div>
  <div class="toc-intro">Sửa đổi quy chế là sửa kỹ thuật - nhưng sửa kỹ thuật nào cũng có người được, có người mất.</div>
  <div class="toc-rule"></div>

  <div class="toc-list">
    <div class="toc-entry">
      <div class="toc-num">01</div>
      <div class="toc-body">
        <div class="toc-name">Phần I</div>
        <div class="toc-headline">Tại sao có chuyện sửa đổi quy chế lúc này?</div>
        <div class="toc-hook">Khi tỷ giá căng, sửa quy chế hấp dẫn hơn cắt lãi suất.</div>
      </div>
      <div class="toc-page-num">3</div>
    </div>
    <!-- ... 6 entries khác -->
  </div>

  <div class="toc-alert">
    <span class="toc-alert-label">Lưu ý quan trọng</span>
    Toàn bộ phân tích là kịch bản "nếu... thì..." về một sửa đổi quy chế đang được thảo luận không chính thức. <strong>Không phải dự báo, không phải khuyến nghị mua bán cổ phiếu nào.</strong>
  </div>
</div>
```

**Hook punchy** (KHÔNG paraphrase tiêu đề), tạo cảm giác "ồ phần này có gì hay". Page số ~ 1 Phần ≈ 2 trang content: P1=3, P2=5, P3=7, P4=9, P5=11, P6=13, P7=15.

Alert "Lưu ý quan trọng" inline cuối TOC page (KHÔNG dùng `.alert-banner` riêng trang).

---

## Bước 4: Build content (page 3+)

### 4a. Section opener (page-break tự động)

```html
<!-- Phần I dùng .no-break -->
<div class="section-opener no-break">
  <div class="section-roman">I</div>
  <div class="section-num-large">Phần I</div>
  <div class="section-title-large">Tại sao có chuyện sửa đổi quy chế này lúc này?</div>
  <div class="section-dek">LDR 111,9% là tín hiệu hệ thống đang căng. NHNN có hai lựa chọn.</div>
  <div class="section-rule-double"></div>
</div>

<!-- Phần II-VII tự động page-break-before -->
<div class="section-opener">
  <div class="section-roman">II</div>
  <div class="section-num-large">Phần II</div>
  <div class="section-title-large">Tiền gửi Kho bạc và mẫu số D</div>
  <div class="section-dek">Một thay đổi công thức 4 năm trước đẩy LDR Big4 lên cao đột ngột.</div>
  <div class="section-rule-double"></div>
</div>
```

- **`section-roman`**: Roman (I, II, III) hiển thị 76pt brass mờ (opacity 0.10) phía sau title - decorative
- **`section-title-large`**: 20pt PFD bold prussian (KHÔNG 24pt cũ - quá to)
- **`section-dek`**: Inter regular slate (KHÔNG PFD italic - giảm AI-feel)
- **Page break tự động** trước mỗi section-opener (trừ `.no-break`)

### 4b. Pseudo drop cap - đoạn đầu MỖI Phần
```html
<p class="dropcap-deep"><span class="dc">L</span>DR là tỷ lệ dư nợ cho vay khách hàng...</p>
```
**Pseudo drop cap** (KHÔNG floated): chữ đầu chỉ tăng size 1.7em + brass color, inline với body. Cleaner, không weird.

### 4c. Body text rich
- `<mark>` cho 3-6 từ key (1-2 lần/đoạn)
- `<span class="t">VCB</span>` cho ticker
- `<strong>` cho emphasis
- **H3**: Inter normal-case 10.5pt 700 + thin brass underline (KHÔNG uppercase letterspaced - source chính của AI-feel cũ)
- **H4**: PFD italic 11.5pt 600 cho micro-subheading (signature italic, hiếm dùng)

### 4d. Pull quotes
**Inline:** `<blockquote><p>...</p></blockquote>` - brass border top/bottom, PFD italic 13pt center.

**Hero (1 lần/bài, signature):**
```html
<blockquote class="hero">
  <p>VPB là ví dụ điển hình của bất đối xứng. Phương án A là cứu sinh.</p>
  <cite>Phần IV - Hai phương án SFL</cite>
</blockquote>
```
Prussian bg + shadow nhẹ + PFD italic 18pt ivory.

### 4e. Callout - 5 levels

**Default:** brass border-left.  
**Warn:** bordeaux border-left + bordeaux-50 bg.  
**Formula:** ivory-deep bg, PFD italic, shadow nhẹ:
```html
<div class="callout formula">
  <div class="formula-label">Công thức Basel III</div>
  <p>NSFR = ASF / RSF ≥ 100%</p>
</div>
```

**Contrast:** so sánh 2 phía:
```html
<div class="callout contrast">
  <div class="side side-a">
    <div class="side-label">Phương án A</div>
    <p>Nội dung A...</p>
  </div>
  <div class="side side-b">
    <div class="side-label">Phương án B</div>
    <p>Nội dung B...</p>
  </div>
</div>
```

**Key:** điểm nhấn quan trọng (1-3 lần/bài), prussian bg + shadow:
```html
<div class="callout key">
  <div class="key-label">Điểm then chốt</div>
  <p>Hai phương án có <strong>logic ngược nhau</strong>...</p>
</div>
```

### 4f. Hero stat trong content
```html
<div class="hero-stat">
  <div class="hero-stat-number">406K</div>
  <div class="hero-stat-caption">
    <div class="hero-stat-label">Tỷ VND TGKB tại Big4</div>
    <div class="hero-stat-desc">Quy mô tiền gửi Kho bạc Nhà nước cuối 2025.</div>
  </div>
</div>
```
1-2 lần/bài. Mono brass 42pt. Desc Inter regular (KHÔNG italic).

### 4g. Tables editorial

```html
<table>
  <thead>
    <tr><th>Ngân hàng</th><th class="th-num">SFL Q1/2026</th><th>Đánh giá</th></tr>
  </thead>
  <tbody>
    <tr class="spotlight"><td>VPB</td><td class="neg">28,3%</td><td><span class="sig-neg">Cận kề trần</span></td></tr>
    <!-- ... -->
  </tbody>
</table>
```

Tables editorial: padding tighter 6/10px, header letterspacing 0.10em (KHÔNG 0.16em quá rộng), single brass border bottom (KHÔNG double), row border 0.5px subtle, **bỏ zebra striping** (cleaner).

Comparison table dùng class `compare`:
```html
<table class="compare">
  <thead><tr><th></th><th>Cắt lãi suất</th><th>Sửa quy chế LDR</th></tr></thead>
  <tbody>
    <tr><td>Tốc độ</td><td>Chậm</td><td class="col-winner">Nhanh hơn</td></tr>
  </tbody>
</table>
```

### 4h. Conclusion block
```html
<div class="conclusion-block">
  <div class="conclusion-eyebrow">Kết luận</div>
  <p>Sửa đổi Thông tư 22/2019 là cách NHNN <strong>tái phân phối lợi ích</strong>...</p>
  <p>Lợi ích phân phối <strong>bất đối xứng</strong>...</p>
</div>
```
Ivory bg + brass borders + shadow nhẹ. PFD italic 13pt (signature italic).

### 4i. Glossary section - 2 column layout
```html
<div class="glossary-section">
  <div class="glossary-eyebrow">Phụ lục</div>
  <div class="glossary-title">Thuật ngữ &amp; phân nhóm</div>
  <div class="glossary-intro">Định nghĩa các khái niệm và thuật ngữ chuyên môn xuất hiện trong bài.</div>

  <div class="glossary-columns">
    <div class="glossary-group">
      <div class="glossary-group-label">A. Thông tư 22 và các điều khoản</div>
      <div class="glossary-term-row">
        <div class="glossary-term">Thông tư 22/2019</div>
        <div class="glossary-def">Quy định giới hạn... <span class="note">Hiệu lực 01/01/2020.</span></div>
      </div>
      <!-- ... -->
    </div>
    <!-- ... groups B, C ... -->
  </div>
</div>
```

Wrap groups trong `.glossary-columns` để render 2-column native qua CSS columns. Term name + definition stack vertical (đẹp hơn grid 2-col trước vì terms ngắn).

### 4j. Contact / Disclaimer page (trang riêng cuối, có CTA)

```html
<div class="contact-page">
  <div class="contact-eyebrow">Tham khảo &amp; Liên hệ</div>
  <h2 class="contact-title">Đọc thêm cùng OPVIA</h2>
  <div class="contact-intro">
    Phân tích này nằm trong chuỗi nghiên cứu chuyên sâu về ngân hàng và vĩ mô của OPVIA Research. Để đào sâu hơn từng góc nhìn, thảo luận với chuyên viên, hoặc đăng ký nhận tin định kỳ, hãy liên hệ trực tiếp với đội ngũ.
  </div>

  <div class="contact-cta">
    <div class="cta-eyebrow">Liên hệ đội ngũ OPVIA</div>
    <div class="cta-title">Đọc thêm phân tích chuyên sâu hoặc đặt lịch tư vấn 1-1</div>
    <div class="cta-text">
      OPVIA Research phát hành báo cáo định kỳ về ngân hàng, vĩ mô, thị trường vốn. Nhà đầu tư tổ chức và cá nhân chuyên nghiệp có thể đặt lịch trao đổi trực tiếp với analyst chủ trì để đào sâu các kịch bản trong báo cáo.
    </div>
    <div class="cta-grid">
      <div class="cta-item">
        <div class="cta-label">Email</div>
        <div class="cta-value">contact@opvia.vn</div>
      </div>
      <div class="cta-item">
        <div class="cta-label">Website</div>
        <div class="cta-value">opvia.vn/research</div>
      </div>
      <div class="cta-item">
        <div class="cta-label">Đặt lịch tư vấn</div>
        <div class="cta-value">opvia.vn/book</div>
      </div>
    </div>
  </div>

  <div class="contact-section">
    <div class="section-eyebrow">Nguồn</div>
    <p>Phân tích dựa trên đề xuất sửa đổi Thông tư 22/2019 đang được thảo luận không chính thức (nguồn: VDSC, KBSV, AFA Capital, BSC tháng 4/2026)...</p>
  </div>

  <div class="contact-section">
    <div class="section-eyebrow">Miễn trừ trách nhiệm</div>
    <p>Toàn bộ phân tích là kịch bản giả định "nếu... thì..." - <strong>không phải dự báo, không phải khuyến nghị mua bán cổ phiếu nào</strong>. Biên soạn: OPVIA Research. Nhà đầu tư tự chịu trách nhiệm về quyết định đầu tư của mình.</p>
  </div>

  <div class="contact-signature">
    OPVIA Research · © 2026
  </div>
</div>
```

**Structure:**
- `contact-page` force `page-break-before: always` - LUÔN tách trang riêng
- Eyebrow brass + h2 PFD bold 28pt + intro slate sans
- **CTA box prussian bg** highlighted với 3-col grid (Email / Website / Đặt lịch tư vấn) - **đây là phần quan trọng nhất**, encourage user contact
- Sources section + Disclaimer section - paper bg, brass top border
- Signature footer centered

CTA contact info là placeholder - dễ customize cho mỗi bài (substitute `contact@opvia.vn`, `opvia.vn/research`, `opvia.vn/book` thành thông tin thật).

---

## Bước 5: Render PDF

```python
import sys
SKILL_DIR = "/path/to/opvia-DeepAnalysis-polish"
sys.path.insert(0, SKILL_DIR)
from render import build_css, render_pdf

DATE = "25/04/2026"
SHORT_TITLE = "ĐỀ XUẤT SỬA ĐỔI THÔNG TƯ 22"

css = build_css(date_str=DATE, short_title=SHORT_TITLE)
html = f'''<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8"><style>{css}</style></head>
<body>{body}</body></html>'''

render_pdf(html, "/mnt/user-data/outputs/OPVIA_THONG_TU_22_20260425.pdf")
```

**Naming convention:** `OPVIA_[SLUG]_YYYYMMDD.pdf`

---

## Ghi chú kỹ thuật WeasyPrint

1. **Vietnamese fonts**: font stack 2-family (Inter/InterVN) cho fallback per-character.
2. **Drop cap subtle**: float trên span tag (KHÔNG `::first-letter`).
3. **Cover full bleed**: page 1 dùng `height: 297mm` block + `@page :first { background-color: #000d18 }`.
4. **Named pages cho TOC**: `page: toc` để override @top-center.
5. **Section page-break**: `.section-opener` mặc định `page-break-before: always`. Phần I dùng `.no-break`.
6. **Roman numeral background**: `position: absolute` + `opacity: 0.10`.
7. **Box shadow**: chỉ apply `.callout.key`, `.callout.formula`, `.conclusion-block`, `blockquote.hero`.
8. **Body bg paper**: `#FAF7F0` editorial feel, không clash cover prussian.
9. **`hyphens: auto`**: bật cho body justified text.
10. **Page margin gọn**: 18mm top, 14mm bottom; `@top-center` padding 5mm (giảm chrome).

---

## QC Checklist

Tự động qua `render.qc_check()`:
- [x] Em-dash / en-dash (FAIL)
- [x] `.cover-deep` (FAIL)
- [x] `.toc-page` (WARN)
- [x] `.section-opener` (WARN)
- [x] `.disclaimer-card` (FAIL)
- [x] Conclusion hoặc callout key (WARN)
- [x] `dropcap-deep` (INFO)

Manual check trước khi deliver:
- [ ] Cover trang 1 KHÔNG bị break sang trang 2
- [ ] Cover đầy đủ: eyebrow + h1 + subtitle + dek + hero stat + 3 bullets + meta strip
- [ ] Eyebrow tiếng Việt thuần (không "BANKING & MACRO")
- [ ] TOC trang 2 + alert inline cùng trang
- [ ] **TOC page numbers PHẢI match thực tế**: render thử, search "Phần I-VII" position thực, update HTML page numbers cho khớp. Đây là bug dễ mắc nếu hardcode.
- [ ] Mỗi Phần II-VII bắt đầu trang mới
- [ ] Mỗi Phần có Roman numeral bg + dek + pseudo drop cap (1.7em brass, KHÔNG floated)
- [ ] H3 KHÔNG uppercase letterspaced (Inter normal-case + thin brass underline)
- [ ] Section title 20pt (KHÔNG 24pt)
- [ ] Pull quote inline có `page-break-before: avoid` để không orphan
- [ ] Glossary 2-column với `.glossary-columns` wrapper
- [ ] **Hyphens: manual** (KHÔNG auto - tránh soft hyphen U+00AD inject)
- [ ] PFD italic chỉ ở signature (pull quote, formula, conclusion, h4)
- [ ] Header strip không quá lớn (5mm padding)
- [ ] **Verify search Vietnamese hoạt động**: thử search "Thông tư", "tỷ lệ", "phương án" - phải match

---

## Nếu cần chuyển skill khác

- Content là daily report (có "phiên", "VN-Index", bảng giá Mã/Phiên/GTGD) → DỪNG, dùng `opvia-DailyReport-polish`
- Content còn nhiều Vietlish/AI-style → đề xuất user chạy `opvia-content-refine` trước rồi quay lại polish


## Wave 6 Polish Modules (mới)

Skill này cung cấp 3 modules polish bổ sung trên top of core render.py:

### 1. `covers.py` - 9 cover variants

Import: `from covers import cover_styles, cover_quick_take, cover_sector_brief, cover_policy_watch, cover_earnings_brief, cover_thematic_macro, cover_alert, cover_yearend_review, cover_pitch_deck`

| Cover | Use case | Tone |
|---|---|---|
| `cover-deep` (existing) | Macro Hero - signature data point cho deep analysis dài | Authoritative dark |
| `cover_quick_take` | Quick memo <1500 từ | Minimal paper |
| `cover_sector_brief` | Multi-entity bank-by-bank focus | Dashboard paper |
| `cover_policy_watch` | Timeline + scenarios cho policy tracking | Dramatic dark |
| `cover_earnings_brief` | 4 metrics grid (EPS/Rev/Margin/ROE) | Bloomberg paper |
| `cover_thematic_macro` | Mini line chart preview cho theme dài hạn | Premium paper + dark chart |
| `cover_alert` | Cảnh báo flash đột xuất | Red banner alert |
| `cover_yearend_review` | Tổng kết năm infographic | Dark luxury |
| `cover_pitch_deck` | BUY/SELL/HOLD recommendation | Investment thesis paper |

Mỗi cover function trả về full A4 page HTML với `page-break-after: always`. Prepend vào body trước nội dung chính.

### 2. `section_openers.py` - 3 section opener variants

Import: `from section_openers import section_opener_styles, section_opener_hero_stat, section_opener_quote`

- **Standard** (current) - existing `.section-opener` CSS class với Roman + title + dek
- **`section_opener_hero_stat(section_num, title, dek, mega_value, mega_unit)`** - mở Phần với 1 mega number bên trái + heading bên phải
- **`section_opener_quote(section_num, quote, attribution, title, dek)`** - mở Phần với 1 pull quote dramatic + attribution + heading

Dùng quote variant cho Phần có statement signature (vd: phỏng vấn NHNN, expert framing).

### 3. `extras.py` - sidebar callouts, glossary alpha, footnotes

Import: `from extras import extras_styles, sidebar_note, glossary_alpha, footnote_marker, footnote_list`

#### Sidebar note callouts
```python
sidebar_note(
    content="Body text với <strong>bold</strong> và <em>italic</em>",
    note_type="methodology",  # 'note' | 'methodology' | 'warning' | 'tip'
    label="Phương pháp tính",  # custom label
)
```
4 types với colors: brass (note), slate (methodology), red (warning), green (tip).

#### Glossary alphabetical (auto-sort)
```python
glossary_alpha(
    terms=[
        {"term": "TGKB", "def": "Tiền gửi Kho bạc Nhà nước.", "context": "Big4 ~135-136 nghìn tỷ"},
        ...
    ],
    title="Thuật ngữ & phân nhóm (sắp xếp ABC)",
    subtitle=f"{N} TERMS",
)
```
Auto sort by term, group by first letter. Replace flat glossary cũ.

#### Footnote system
```python
footnote_marker(1)   # inline: <sup>[1]</sup>
footnote_list([
    "Nguồn: NHNN báo cáo Q1/2026.",
    "Big4 SOCB: VCB, CTG, BID, AGR.",
])  # bottom of page
```

### Usage trong test_render

```python
from render import build_full_css  # NEW: includes Wave 6 polish CSS
from covers import cover_quick_take
from section_openers import section_opener_quote
from extras import sidebar_note, glossary_alpha

css = build_full_css(date_str="27/04/2026", short_title="OPVIA RESEARCH") + viz_styles()

# Cover variant
cover = cover_quick_take(eyebrow=..., title=..., dek=..., takeaway=...)

# Section opener variant
phan_iii_opener = section_opener_quote(
    section_num="PHẦN III",
    quote="Hai phương án có cùng mục đích nhưng người hưởng lợi khác nhau hoàn toàn.",
    attribution="Phó Thống đốc NHNN, phát biểu nội bộ Q1/2026",
    title="Điều 16: tỷ lệ vốn ngắn hạn cho vay trung-dài hạn",
    dek="VPB và TCB đang sát trần SFL...",
)

# Sidebar trong content
methodology = sidebar_note(content="...", note_type="methodology", label="Phương pháp tính")

# Glossary alpha replace flat
glossary = glossary_alpha(terms=[...], title="Thuật ngữ", subtitle="14 TERMS")
```

### Build full CSS

`build_full_css()` (không phải `build_css()`) tự concat: core CSS + cover_styles + section_opener_styles + extras_styles. Dùng nó khi sử dụng Wave 6 polish.

```python
from render import build_full_css

css = build_full_css(date_str=DATE, short_title=SHORT_TITLE) + viz_styles()
```
