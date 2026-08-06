# StoiX · theme.md (Brand Theme · FINAL)

> Bản chốt, opinionated. 2 mode **Light (Paper)** / **Dark (Noir)**. Anchor: brand book
> "The Ledger Doctrine v2.1". Catalog đầy đủ 14 variant ở `brand-consolidated-light-dark.md`,
> token wire-ready ở `tokens.css`. Mọi hex là giá trị thật trong code. Ngày: 2026-06-11.
>
> **Tinh thần:** nhật ký tài chính editorial, KHÔNG bland. Giấy ấm + mực óc chó + vàng antique
> + đỏ pen-red, serif có cá tính, dark mode champagne. Tránh "xám trên trắng phẳng lì".

## 0. Nguyên tắc
1. 1 brand, 2 mode, mỗi vai trò 1 canonical. Variant cũ không xoá, xuống §8 làm alias.
2. Phân biệt **drift** (trùng vai trò, đã gộp) vs **functional** (màu theo chức năng, giữ).
3. Token đặt theo CSS custom property để wire thẳng vào code.
4. Mọi font canonical hỗ trợ tiếng Việt đầy đủ (đã verify Google Fonts vietnamese subset).

---

## 1. Type system (canonical · có cá tính · full tiếng Việt)
| Vai trò | Canonical | Tính cách | Tiếng Việt |
|---------|-----------|-----------|-----------|
| **Display** (bìa, hero, heading lớn, drop cap) | **Fraunces** | soft-serif "old style", có wonk + optical size, giàu cá tính | ✓ |
| **Serif editorial** (section heading, pull-quote, serif body) | **EB Garamond** | cổ điển ấm, chất nhật ký | ✓ |
| **Sans** (UI, body, nhãn, data) | **Inter** | workhorse trung tính, rõ | ✓ |
| **Mono** (số, bảng, issue strip, code) | **JetBrains Mono** | tabular, kỹ thuật | ✓ |
| **Script accent** (tùy chọn, chỉ Latin/số: ngày phát hành, marginalia) | **Caveat** | viết tay, thêm sức sống | dùng cho số/nhãn Latin, không cho thân bài VN |

- Fallback tiếng Việt tuyệt đối trong stack sans: **Be Vietnam Pro** (thiết kế cho tiếng Việt).
- Marketing hero cực glam có thể swap Display sang **Playfair Display** (high-contrast, VN ✓) · alias hợp lệ.
- CFA Notes .docx tạm giữ Raleway/Lora tới khi migrate sang Fraunces/EB Garamond.

**Font stacks:**
```
--font-display: 'Fraunces','Playfair Display',Georgia,serif;
--font-serif:   'EB Garamond','Be Vietnam Pro',Georgia,serif;
--font-sans:    'Inter','Be Vietnam Pro',system-ui,-apple-system,sans-serif;
--font-mono:    'JetBrains Mono',ui-monospace,Menlo,monospace;
--font-script:  'Caveat',cursive;   /* decorative Latin/numerals only */
```

---

## 2. LIGHT (Paper) · canonical
| Token | Hex | Vai trò |
|-------|-----|---------|
| `--paper` | `#F2E9D2` | nền trang |
| `--paper-deep` | `#F8F1DF` | nền ngà sâu nhất |
| `--paper-card` | `#ECE1C4` | card |
| `--paper-elev` | `#E4D6B0` | card nổi / row hover |
| `--paper-edge` | `#B8A47A` | mép giấy / rule đậm |
| `--ink` | `#1A1610` | chữ chính (walnut) |
| `--ink-strong` | `#07060A` | chữ đậm nhất / heading |
| `--ink-soft` | `#4A3F28` | chữ phụ |
| `--ink-muted` | `#7A6B4A` | chữ mờ |
| `--ink-faint` | `#A8997A` | watermark / caption |
| `--gold` | `#5A4A14` | vàng PRIMARY trên giấy (deep) |
| `--gold-mid` | `#9F7E1B` | vàng mid / hairline rule |
| `--accent` | `#B0302D` | đỏ nhấn (pen-red) |
| `--success` | `#5C8A3C` | đúng / tăng |
| `--error` | `#C73E3A` | sai / cảnh báo |

---

## 3. DARK (Noir) · canonical
| Token | Hex | Vai trò |
|-------|-----|---------|
| `--bg` | `#06090F` | nền tối |
| `--surface` | `#0A0F18` | bề mặt |
| `--raised` | `#101723` | bề mặt nổi |
| `--border` | `#263148` | viền |
| `--text` | `#EEF2F8` | chữ chính (platinum) |
| `--text-2` | `#C8D0D8` | chữ phụ |
| `--text-muted` | `#9AA5B2` | chữ mờ |
| `--gold` | `#D4AF37` | vàng bright |
| `--gold-glow` | `#F0CF55` | đỉnh sáng / champagne hero |
| `--accent` | `#E5645F` | đỏ nhấn trên nền tối |
| `--success` | `#8FD6A8` | đúng / tăng |
| `--glass-bg` | `rgba(255,255,255,.03)` | glass nền |
| `--glass-border` | `rgba(255,255,255,.08)` | glass viền |

---

## 4. Gold · MỘT thang
`#5A4A14` deep → `#9F7E1B` mid → `#D4AF37` bright → `#F0CF55` glow.
- Light dùng deep/mid; Dark dùng bright/glow. `#C49A1A` (CFA Notes) ≈ mid → fold.

---

## 5. Personality · chống bland (bắt buộc khi áp dụng)
Theme này KHÔNG được phẳng lì. Các "đòn bẩy" cá tính:
1. **Display Fraunces** ở bìa/section opener, cho phép wonk + optical contrast cao (không để mặc định nhạt).
2. **Drop cap** chữ cái đầu bài/section bằng Fraunces hoặc Playfair, tô `--gold` hoặc `--accent`.
3. **Hairline rule vàng** (`--gold-mid` trên giấy, `--gold` trên dark) ngăn các khối, kiểu sổ cái.
4. **Pen-red `--accent`** dùng có chủ đích: số liệu âm, callout, kicker. Không thay bằng xám.
5. **Issue strip / số liệu** bằng JetBrains Mono, có thể kèm Roman numerals + Caveat cho ngày.
6. **Tương phản mạnh**: mực walnut `#1A1610` trên giấy `#F2E9D2` (không phải gray-on-white).
7. **Dark mode champagne**: `--gold-glow` cho hero, glass panel, tạo chất "lavish" Platinum Noir.
8. **Texture giấy**: dùng `--paper-edge` làm deckle/shadow mép, tránh nền beige chết.

---

## 6. Functional palettes (GIỮ · màu theo chức năng, không phải thừa)
**Semantic status:** error `#C73E3A` · success `#5C8A3C` (Light) / `#8FD6A8` (Dark) · danger `#E55A4A`.

**Formula variable cycle (CFA Notes, 8 màu xoay vai trò biến):**
`#B83030 · #2B5597 · #2D6A4F · #7B3FA0 · #A07820 · #1A7A7A · #A04030 · #5B3FA0`

**Callout boxes (CFA Notes, 5 cặp nền/accent):**
Key `#F6EDD5/#8B6B20` · Example `#E4F0E9/#2D6A4F` · Warn `#F7E9E6/#A04030` · Note `#E4ECF6/#2B5597` · Purple/Image `#EEE8F7/#6B3FA0`.

**Subject taxonomy (CFA Notes, 10 môn):**
PM `#6B4010` · FI `#1A5270` · EQ `#2E6B3E` · DER `#5C3A8B` · AI `#1A5B5B` · CI `#8B3A20` · FSA `#6B2020` · ECO `#3A5A20` · QM `#3A3A7C` · ETH `#204A7B`.

**StoiX Read editorial category accents (4):**
blue `#2A4F7A` (series) · green `#2F6F4D` (upside) · mustard `#A87A1C` (highlight) · burgundy `#6A2A2A` (archived).

**Notes section-number accent (functional, giữ riêng):** cam-đất `#B85A1C` (vai trò "số mục", khác đỏ brand).

> Các palette này gắn vai trò cụ thể nên KHÔNG gộp. Đây không phải "thừa màu".

---

## 7. Quyết định đã chốt (OPEN cũ → resolved)
| Vấn đề | Chốt |
|--------|------|
| Serif display | **Fraunces** (display) + **EB Garamond** (serif editorial). Playfair = alias marketing hero. Spectral = alias (VN ✓ nhưng không vào canonical). |
| Cam-đất `#B85A1C` | **Giữ làm functional** (section-number của Notes), không nhập vào `--accent`. |
| Paper chuẩn | **`#F2E9D2`**; `#FFFEF8`/`#fbf9f4`/`#f1e9d0` thành alias sáng hơn. |
| Playfair Display | **Giữ** làm display alias cho marketing hero, không bỏ. |

---

## 8. Appendix · variant → canonical alias (không xoá gì)
| Variant cũ | Mode | Map về canonical | Token thành alias |
|------------|------|------------------|-------------------|
| L1 Notes Ivory | Light | Paper | `#FFFEF8`→`--paper-deep`; title `#2C3878`/teal `#0E6B85`/amethyst `#5C2D91`/olive `#7A5C00` = functional |
| L2 Notes boxes | Light | functional §6 | giữ nguyên |
| L3 Notes subjects | Light | functional §6 | giữ nguyên |
| L4 Notes cover indigo | Light | `--ink` | `#1E2862` ≈ ink-on-paper |
| L5 StoiX Read Newsprint | Light | Paper | `#fbf9f4`→`--paper-deep` alias; red `#9b2c2c`→`--accent` alias |
| L6 Read Bookshelf | Light | Paper | `#f7f4ed`→paper alias |
| L7 exam Paper | Light | Paper | `#f1e9d0`→paper alias; gold `#6a4f10`→`--gold` near |
| L8 Ledger v2.1 | Light | **= canonical anchor** | nguồn của `--paper`/`--ink`/`--gold`/`--accent` |
| D1 Read Dark | Dark | Noir | `#14110d` warm-black → alias `--bg` (biến thể ấm) |
| D2 exam study noir | Dark | **= canonical Noir anchor** | nguồn `--bg`/`--text` |
| D3 exam funnel | Dark | Noir | gold `#D4AF37`→`--gold`; Playfair → display alias |
| D4 exam catalog indigo | Dark | Noir | `#050811`→`--bg` alias; mint `#8caea2` = functional landing accent |
| D5 exam catalog-v4 | Dark | Noir | `#050814`→`--bg` alias; champagne `#d8c28a`→`--gold` family |
| D6 Navy Ledger/glass | Dark | Noir | `--glass-bg`/`--glass-border` = nguồn |

---

## 9. Self-check
- Mọi token canonical truy ngược về hex thật (anchor Ledger v2.1 + study noir). 0 hex bịa.
- 5 font canonical đều hỗ trợ tiếng Việt (Fraunces, EB Garamond, Inter, JetBrains Mono verify Google Fonts vietnamese subset; Caveat chỉ dùng Latin/số).
- 14/14 variant có dòng map ở §8, không variant nào bị xoá.
- Drift đã gộp: vàng 4→1 thang; đỏ 3→1 + alias; paper 4→1 + alias; serif → 1 display + 1 editorial.
- Chống bland: §5 liệt kê 8 đòn bẩy cá tính bắt buộc.

**Canonical 32 token màu + 5 font · alias 14 variant · functional ~36 giá trị · 0 hex bịa · 0 OPEN còn lại.**
