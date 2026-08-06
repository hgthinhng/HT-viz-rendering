# `back_cover_cta` - trang kết bài CTA + nguồn + disclaimer

**Wave:** Page template
**Output:** Full-page HTML+CSS, render qua stocklpt-DeepAnalysis-polish hoặc stocklpt-DailyReport-polish
**Render:** Inject HTML structure dưới đây vào cuối body, polish skill có CSS sẵn cho `.back-cover-cta` class.

---

## Khi nào dùng

- LUÔN LUÔN cuối mọi bài StockLPT publish-ready (deep analysis + daily report).
- Page cuối, paper warm `#F4F6F9` background.
- Mời reader liên hệ để đào sâu / đặt lịch tư vấn / nhận tin định kỳ.
- Kèm nguồn (sources) + disclaimer hợp pháp.

---

## Khi nào KHÔNG dùng

- Nội bộ draft, chưa publish - skip để giảm noise khi review.
- Bài rất ngắn (< 3 trang) - CTA chiếm tỷ lệ quá lớn, dùng compact footer thay.

---

## Pair với

- `cover_deep_page` ở page 1 - đối xứng mở/đóng bài. Mỗi bài deep có cả 2.

---

## Anatomy của back cover

```
┌───────────────────────────────────────────┐
│  THAM KHẢO & LIÊN HỆ                      │  <- eyebrow accent uppercase
│                                           │
│  Đọc thêm cùng STOCKLPT                      │  <- title PFD italic charcoal ~32pt
│                                           │
│  Phân tích này nằm trong chuỗi nghiên     │
│  cứu chuyên sâu về ngân hàng và vĩ mô     │
│  của STOCKLPT Academy. Để đào sâu hơn từng   │  <- description Inter ~13pt
│  góc nhìn, thảo luận với chuyên viên,     │     line-height 1.65
│  hoặc đăng ký nhận tin định kỳ, hãy liên  │
│  hệ trực tiếp với đội ngũ.                │
│                                           │
│  ┌─────────────────────────────────────┐ │
│  │  LIÊN HỆ ĐỘI NGŨ STOCKLPT              │ │  <- DARK INDIGO BOX
│  │  (accent uppercase eyebrow)          │ │     bg #2A1A4A hoặc #130B24
│  │                                     │ │
│  │  Đọc thêm phân tích chuyên sâu      │ │  <- title PFD italic ivory ~22pt
│  │  hoặc đặt lịch tư vấn 1-1           │ │
│  │                                     │ │
│  │  STOCKLPT Academy phát hành báo cáo... │ │  <- body ivory smaller ~12pt
│  │                                     │ │
│  │  ─── ─── ───  (accent dashes)        │ │
│  │                                     │ │
│  │  EMAIL          WEBSITE     ĐẶT LỊCH │ │  <- 3-col contact grid
│  │  contact@...    stocklpt.vn/r  stocklpt.vn │ │     labels accent uppercase
│  │                             /book    │ │     values mono ivory
│  └─────────────────────────────────────┘ │
│                                           │
│  NGUỒN                                    │  <- eyebrow accent
│  Phân tích dựa trên đề xuất sửa đổi...    │  <- source citations
│                                           │     italic charcoal ~10pt
│                                           │
│  MIỄN TRỪ TRÁCH NHIỆM                     │  <- eyebrow accent
│  Toàn bộ phân tích là kịch bản giả định   │
│  "nếu... thì..." - không phải dự báo,     │  <- legal disclaimer
│  không phải khuyến nghị mua bán...        │     italic charcoal ~10pt
│                                           │
│  ──────────────────────────────────       │
│  STOCKLPT ACADEMY · MỤC ĐÍCH GIÁO DỤC ·      │  <- footer copyright
│  © 2026 STOCKLPT ACADEMY                     │     centered, accent uppercase ~9pt
└───────────────────────────────────────────┘
```

---

## Params (từ decision dict + skill defaults)

```python
back_cover_meta = {
    # CTA box content (có default StockLPT, override khi cần)
    "cta_eyebrow": "LIÊN HỆ ĐỘI NGŨ STOCKLPT",
    "cta_title": "Đọc thêm phân tích chuyên sâu hoặc đặt lịch tư vấn 1-1",
    "cta_body": "STOCKLPT Academy phát hành báo cáo định kỳ về ngân hàng, vĩ mô, thị trường vốn. Nhà đầu tư tổ chức và cá nhân chuyên nghiệp có thể đặt lịch trao đổi trực tiếp với analyst chủ trì để đào sâu các kịch bản trong báo cáo.",

    # Contact channels (lock - thuộc brand)
    "contact_email": "contact@stocklpt.vn",
    "contact_website": "stocklpt.vn/research",
    "contact_book": "stocklpt.vn/book",

    # Per-bài (LLM fill)
    "sources": "Phân tích dựa trên đề xuất sửa đổi Thông tư 22/2019 đang được thảo luận không chính thức (nguồn: VDSC, KBSV, AFA Capital, BSC tháng 4/2026). Chưa có dự thảo chính thức từ NHNN tại thời điểm viết. Số liệu BCTC ngân hàng cuối 2025 và Q1/2026 lấy từ công bố chính thức của các tổ chức tín dụng.",

    "disclaimer": (
        "Toàn bộ phân tích là kịch bản giả định 'nếu... thì...' - không phải dự báo, "
        "không phải khuyến nghị mua bán cổ phiếu nào. Biên soạn: STOCKLPT Academy. "
        "Mục đích giáo dục và thông tin chuyên môn. Nhà đầu tư tự chịu trách nhiệm "
        "về quyết định đầu tư của mình. STOCKLPT Academy không đảm bảo tính chính xác "
        "tuyệt đối và không chịu trách nhiệm về thiệt hại phát sinh từ việc sử dụng "
        "nội dung báo cáo này."
    ),

    # Footer
    "publish_date": "25/04/2026",
    "title_short": "ĐỀ XUẤT SỬA ĐỔI THÔNG TƯ 22",   # uppercase cho footer copyright
    "year": 2026,
}
```

**Default values lock vào polish skill** - LLM chỉ phải fill `sources`, `disclaimer` (per-bài), `publish_date`, `title_short`. Còn lại CTA box content + contact channels là StockLPT brand defaults.

---

## HTML template

```html
<section class="back-cover-cta page-break-before">
  <div class="eyebrow">THAM KHẢO &amp; LIÊN HỆ</div>

  <h2 class="back-title">Đọc thêm cùng STOCKLPT</h2>

  <p class="back-description">
    Phân tích này nằm trong chuỗi nghiên cứu chuyên sâu về ngân hàng và vĩ mô
    của STOCKLPT Academy. Để đào sâu hơn từng góc nhìn, thảo luận với chuyên viên,
    hoặc đăng ký nhận tin định kỳ, hãy liên hệ trực tiếp với đội ngũ.
  </p>

  <div class="cta-box">
    <div class="cta-eyebrow">{cta_eyebrow}</div>
    <h3 class="cta-title">{cta_title}</h3>
    <p class="cta-body">{cta_body}</p>

    <div class="cta-dashes">··· ··· ···</div>

    <div class="cta-contact-grid">
      <div>
        <div class="label">EMAIL</div>
        <div class="value">{contact_email}</div>
      </div>
      <div>
        <div class="label">WEBSITE</div>
        <div class="value">{contact_website}</div>
      </div>
      <div>
        <div class="label">ĐẶT LỊCH TƯ VẤN</div>
        <div class="value">{contact_book}</div>
      </div>
    </div>
  </div>

  <div class="back-section">
    <div class="eyebrow">NGUỒN</div>
    <p class="back-meta">{sources}</p>
  </div>

  <div class="back-section">
    <div class="eyebrow">MIỄN TRỪ TRÁCH NHIỆM</div>
    <p class="back-meta">{disclaimer}</p>
  </div>

  <div class="back-footer-rule"></div>
  <div class="back-footer">
    STOCKLPT ACADEMY · MỤC ĐÍCH GIÁO DỤC · © {year} STOCKLPT ACADEMY · {title_short} · {publish_date}
  </div>
</section>
```

---

## Tokens

- Page bg: paper `#F4F6F9`
- Eyebrow: Inter 600, accent `#16633C`, uppercase, letter-spacing 0.18em, ~10pt
- Back title "Đọc thêm cùng STOCKLPT": PFD italic, charcoal `#221A34`, ~32pt
- Description: Inter regular, charcoal, ~13pt, line-height 1.65
- CTA box: bg `#2A1A4A` (Indigo), padding ~28-32pt, border-radius 0 (flat editorial)
- CTA eyebrow trong box: Inter 600, accent, uppercase ~9pt, letter-spacing 0.2em
- CTA title: PFD italic, ivory `#EBEFF4`, ~22pt, line-height 1.25
- CTA body: Inter regular, ivory 90%, ~12pt
- CTA dashes: accent, font-size 12pt, letter-spacing 0.4em, centered
- Contact grid: 3 columns equal, gap ~24pt
- Contact label: Inter 600, accent, uppercase ~9pt
- Contact value: JetBrains Mono, ivory, ~11pt
- Source/disclaimer: italic, charcoal, ~10pt, line-height 1.5
- Footer rule: 1px accent full width
- Footer copyright: Inter 600, accent, uppercase ~9pt, letter-spacing 0.2em, centered

---

## Defaults locked trong polish skill

Để giảm boilerplate cho LLM, polish skill (stocklpt-DeepAnalysis-polish + stocklpt-DailyReport-polish) phải hardcode default cho các field brand-locked:

- `cta_eyebrow = "LIÊN HỆ ĐỘI NGŨ STOCKLPT"`
- `cta_title = "Đọc thêm phân tích chuyên sâu hoặc đặt lịch tư vấn 1-1"`
- `cta_body = "STOCKLPT Academy phát hành báo cáo định kỳ ..."` (default StockLPT copy)
- `contact_email = "contact@stocklpt.vn"`
- `contact_website = "stocklpt.vn/research"`
- `contact_book = "stocklpt.vn/book"`
- `disclaimer` (default StockLPT disclaimer copy)

LLM chỉ override khi user yêu cầu rõ (vd archetype khác có CTA khác, hoặc disclaimer cần custom).

---

## Failure modes

- **Thiếu disclaimer**: legal exposure. Validator phải fail nếu back_cover_cta không có `disclaimer` field.
- **CTA contact email/url sai**: brand damage. Validator nên check format `*@stocklpt.vn` và `stocklpt.vn/*`.
- **Sources rỗng**: bài không có citation. Warn (không fail) - một số daily report ngắn có thể không cần.
- **CTA box overflow vào page sau**: page break trong giữa box. Add `page-break-inside: avoid` cho `.cta-box`.

---

## Notes

- Daily report dùng version compact của back_cover (gộp source + disclaimer thành 1 footer 6-8 dòng). Deep analysis dùng full version như mô tả.
- 3 accent dashes (`··· ··· ···`) trong CTA box echo lại pattern cover - signature visual đối xứng.
- Footer copyright line cuối cần wrap "·" giữa segments để không break giữa "ĐỀ XUẤT" và "SỬA ĐỔI".
