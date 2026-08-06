# `cover_deep_page` - trang bìa signature deep analysis

**Wave:** Page template (không phải atomic component)
**Output:** Full-page HTML+CSS, render qua opvia-DeepAnalysis-polish
**Render:** Inject HTML structure dưới đây vào body, polish skill có CSS sẵn cho `.cover-deep` class.

---

## Khi nào dùng

- LUÔN LUÔN cho bài deep analysis, mọi archetype trừ daily_report.
- Page 1 của PDF, full-bleed Prussian-900 background.
- Có hero stat signature (1 con số định-bài) làm anchor visual.

---

## Khi nào KHÔNG dùng

- Daily report - dùng header gọn của opvia-DailyReport-polish thay.
- Bài < 8 trang - cover quá nặng cho format ngắn, dùng `data_hero` inline.
- Không có 1 con số signature rõ - cover sẽ thiếu visual anchor.

---

## Pair với

- `back_cover_cta` ở page cuối - đối xứng mở/đóng bài.
- TOC + section openers ở giữa.

---

## Anatomy của cover

```
┌───────────────────────────────────────────┐
│            ─── ─── ─── (brass dashes)     │
│              OPVIA ACADEMY                │
│                                           │
│  NGÂN HÀNG & VĨ MÔ        SỐ THÁNG 4·2026 │  <- eyebrow row (sub-brand + issue)
│                                           │
│                                           │
│  Đề xuất sửa đổi                          │  <- TITLE: PFD italic ivory ~52pt
│  Thông tư 22/2019                         │     (2-3 line, line-height 1.05)
│                                           │
│  Ai hưởng lợi, ai chịu thiệt?             │  <- SUBTITLE: PFD italic brass ~22pt
│                                           │
│  Khi LDR hệ thống chạm 111,9% và tỷ giá   │
│  VND đang căng kịch trần, NHNN đối mặt    │  <- DEK: Inter ivory, 4-5 lines
│  lựa chọn khó: cắt lãi suất hay sửa quy   │     ~14pt, line-height 1.6
│  chế. Đề xuất sửa Thông tư 22 là...       │
│                                           │
│  ──────────────                            │
│                                           │
│  111,9%  TỶ LỆ LDR HỆ THỐNG · 30/3/2026   │  <- HERO STAT: mega number
│          Mức cao kỷ lục, vượt xa trần       │     JetBrains Mono brass ~96pt
│          quy chế 85% - tín hiệu hệ thống    │     + label uppercase brass
│          đang căng.                         │     + description ivory
│                                           │
│  TRONG BÀI NÀY                            │  <- eyebrow brass uppercase
│  ▸ Tái phân phối, không phải nới lỏng.    │     + 3 takeaways
│    Sửa Thông tư 22 là chỉnh quy tắc...    │     bold lead + giải thích
│  ▸ Hai phương án Điều 16...               │
│  ▸ Lợi ích phân phối bất đối xứng...      │
│                                           │
│  ──────────────                            │
│                                           │
│  BIÊN SOẠN     ĐỌC TRONG    PHÁT HÀNH     │  <- footer 3-col
│  OPVIA ACADEMY  14 PHÚT     25/04/2026    │     uppercase brass labels
│                                           │     + ivory values
└───────────────────────────────────────────┘
```

---

## Params (từ decision dict)

```python
cover_meta = {
    "sub_brand": "Ngân hàng & Vĩ mô",        # eyebrow trái
    "issue": "Số tháng 4 · 2026",             # eyebrow phải
    "title": "Đề xuất sửa đổi Thông tư 22/2019",
    "subtitle": "Ai hưởng lợi, ai chịu thiệt?",  # PFD italic brass
    "dek": "Khi LDR hệ thống chạm 111,9% ...",   # 50-80 từ, 4-5 line
    "hero_number": "111,9%",                  # mega stat
    "hero_label": "TỶ LỆ LDR HỆ THỐNG · 30/3/2026",
    "hero_desc": "Mức cao kỷ lục, vượt xa trần quy chế 85% - tín hiệu hệ thống đang căng.",
    "takeaways": [                            # 3 bullets, mỗi cái có lead bold + giải thích
        {"lead": "Tái phân phối, không phải nới lỏng.",
         "detail": "Sửa Thông tư 22 là chỉnh quy tắc kỹ thuật để hệ thống không bị 'đo' tệ trên giấy - không phải nới lỏng tiền tệ thực sự."},
        {"lead": "Hai phương án Điều 16 cho kết quả ngược nhau.",
         "detail": "Nới SFL 35% hay thay NSFR - cùng mục đích nhưng VPB có thể là người sống hoặc chết tùy chọn nào."},
        {"lead": "Lợi ích phân phối bất đối xứng.",
         "detail": "Big4 và một số tư nhân lớn hưởng lợi gấp đôi. Ngân hàng nhỏ Nhóm C thiệt 12-24 nghìn tỷ mỗi năm."},
    ],
    "author": "OPVIA Academy",
    "read_time_min": 14,
    "publish_date": "25/04/2026",
}
```

---

## HTML template

```html
<section class="cover-deep">
  <div class="cover-masthead">
    <div class="cover-dashes">··· ··· ···</div>
    <div class="cover-brand">OPVIA ACADEMY</div>
  </div>

  <div class="cover-eyebrow-row">
    <span class="eyebrow-left">{sub_brand}</span>
    <span class="eyebrow-right">{issue}</span>
  </div>

  <h1 class="cover-title">{title}</h1>
  <p class="cover-subtitle">{subtitle}</p>
  <p class="cover-dek">{dek}</p>

  <div class="cover-rule"></div>

  <div class="cover-hero-stat">
    <div class="cover-hero-num">{hero_number}</div>
    <div class="cover-hero-meta">
      <div class="cover-hero-label">{hero_label}</div>
      <div class="cover-hero-desc">{hero_desc}</div>
    </div>
  </div>

  <div class="cover-takeaways">
    <div class="eyebrow">TRONG BÀI NÀY</div>
    <ul>
      {for t in takeaways:}
      <li><span class="arrow">▸</span> <strong>{t.lead}</strong> {t.detail}</li>
      {endfor}
    </ul>
  </div>

  <div class="cover-rule"></div>

  <footer class="cover-footer">
    <div><div class="label">BIÊN SOẠN</div><div class="value">{author}</div></div>
    <div><div class="label">ĐỌC TRONG</div><div class="value">{read_time_min} PHÚT</div></div>
    <div><div class="label">PHÁT HÀNH</div><div class="value">{publish_date}</div></div>
  </footer>
</section>
```

---

## Tokens

- Background: Prussian-900 `#000d18`
- Brass dashes: `#B5A642`, font-size 14pt, letter-spacing 0.4em
- Brand "OPVIA ACADEMY": Inter 700, ivory `#F5F1E8`, letter-spacing 0.25em, ~14pt
- Eyebrow: Inter 600, brass, uppercase, letter-spacing 0.18em, ~10pt
- Title: PFD italic, ivory, ~52pt, line-height 1.05
- Subtitle: PFD italic, brass, ~22pt
- Dek: Inter regular, ivory, ~14pt, line-height 1.6
- Hero number: JetBrains Mono, brass, ~96pt, font-weight 500
- Hero label: Inter 600, brass, uppercase, ~10pt
- Hero desc: Inter regular, ivory `#F5F1E8 95%`, ~12pt
- Takeaways arrow ▸: brass
- Footer label: Inter 600, brass, uppercase, ~10pt, letter-spacing 0.18em
- Footer value: Inter regular, ivory, ~12pt
- Cover rule: 1px brass, width ~25% page

---

## Failure modes

- **Title quá dài (>3 line)**: overflow vào dek area. Cô đọng tới ≤8 từ.
- **Dek > 80 từ**: page break. Ngắn lại 50-70 từ tối ưu.
- **takeaways không phải đúng 3**: layout asymmetric. Force 3 bullets.
- **hero_number > 6 chars**: scale down auto, nhưng có thể không signature như mong đợi. Pick number gọn (vd "111,9%" thay vì "111.900.000.000.000 VND").
- **Takeaway lead > 60 chars**: wrap nhiều dòng. Cô đọng punchline.

---

## Notes

- Cover phải có `page-break-after: always` để section I bắt đầu trang mới.
- Background full-bleed dùng `@page :first` rule trong CSS với `background-color`.
- WeasyPrint bug: `background` shorthand không reliable trên `@page`, dùng `background-color` riêng.
- 3 brass dashes trên cùng (`··· ··· ···`) là signature visual của Opvia - giữ nguyên trong tất cả cover deep.
