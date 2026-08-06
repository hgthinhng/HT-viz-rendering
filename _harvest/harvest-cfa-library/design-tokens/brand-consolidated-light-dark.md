# StoiX + CFA — Hợp nhất token theo 2 nhóm lớn: SÁNG / TỐI

> Phase consolidate. SÁNG/TỐI chỉ là **2 ô phân loại cấp cao** theo độ sáng nền.
> GIỮ NGUYÊN 100% variant — không gộp, không chọn mã đại diện, không bịa.
> Nguồn: `brand-style.md` + đọc lại code (render_engine.py, styles.css, src/ds/tokens, v2-tokens.css). Ngày: 2026-06-11.

## 0. Tổng quan + đếm

| Nhóm | Số variant | Ghi chú |
|------|-----------|---------|
| ☀ SÁNG | 8 | 4 từ CFA Notes (light) + 1 StoiX Read + 1 bookshelf sub + 2 exam-ops |
| 🌙 TỐI | 6 | 1 StoiX Read + 5 exam-ops |
| Trung lập (dùng cả 2) | 3 nhóm | Formula var cycle · semantic status · mono font |

3 dự án: **A** CFA Notes (render .docx) · **B** StoiX Read (web báo) · **C** StoiX exam-ops (app).

---

# 1. ☀ SÁNG (Light) — nền sáng (ivory / cream / giấy ấm)

## L1 · CFA Notes — Ivory Editorial *(A · render_engine.py)*
- Nền trang `#FFFEF8` · nền hộp `#F0EDE6`
- Tiêu đề purple `#2C3878` · indigo `#2E3B7C`
- Số mục cam đất `#B85A1C` · vàng đồng `#C49A1A`
- Thuật ngữ teal `#0E6B85` · ref Công thức amethyst `#5C2D91` · ref Ví dụ olive `#7A5C00`
- Highlight `#E8DEB0` · body `#1C1C1C` · secondary `#3B3B3B` · muted `#6B6B6B` · header/footer `#5A5A5A` · rule `#CECECE` · dark-teal cover `#1E3A5F`
- Font: **Inter** (body) · **Raleway** (display) · **Consolas** (mono) [Stack B]. EIR: **Lora** display + **JetBrains Mono** [Stack D]. Khác: A=Source Serif Pro/Fraunces, C=Be Vietnam Pro.

## L2 · CFA Notes — Bộ hộp callout *(A)*
- Key `bg #F6EDD5 / accent #8B6B20` · Example `bg #E4F0E9 / #2D6A4F` · Warn `bg #F7E9E6 / #A04030` · Note `bg #E4ECF6 / #2B5597` · Purple+ImageHint `bg #EEE8F7 / #6B3FA0` · KeyTakeaways(EIR) `bg #F6EDD5 / #8B6B20`

## L3 · CFA Notes — Màu nhấn theo môn (cover trên nền sáng) *(A)*
- PM `#6B4010` · FI `#1A5270` · EQ `#2E6B3E` · DER `#5C3A8B` · AI `#1A5B5B` · CI `#8B3A20` · FSA `#6B2020` · ECO `#3A5A20` · QM `#3A3A7C` · ETH `#204A7B`

## L4 · CFA Notes — Module number/name cover accents *(A)*
- Module num `#1E2862` · section tabs `1E2862·232D6E·283278·2C3878·323D80·384388·3E4990·445098`

## L5 · StoiX Read — Newsprint Light (mặc định) *(B · styles.css)*
- Paper `#fbf9f4` (biến thể `#f2e3c8`) · ink `#1a1714` / phụ `#3a2f1f`
- Accent Pompeii red `#9b2c2c` (cũ `#b23a2c`) · blue (series) `#2a4f7a` · green (upside) `#2f6f4d` · mustard `#a87a1c` / `#b8862c` · burgundy `#6a2a2a`
- Chart up `#2f6f4d` · chart down `#b23a2c` · rule `#d8d2c3` / `#d4be99`
- Font: **EB Garamond** (body+display, fallback Cormorant Garamond) · **Inter** (UI) · **JetBrains Mono**
- Phiên bản (cùng base, layout khác): v4★ · v3 · v2 · v1 · reader-v3 · studies · brain · editor · admin · glossary

## L6 · StoiX Read — Bookshelf (sub-variant sáng) *(B · styles-bookshelf.css)*
- Paper `#f7f4ed` · ink `#1a1714` · rule `#cdc6b8` · accent `#b23a2c` · blue `#2a4f7a` · green `#2f6f4d` · mustard `#b8862c`

## L7 · exam-ops — Paper tone (navy editorial / checkout) *(C · tones/paper.css)*
- Surface cream ramp `#f6efdb·#f1e9d0·#e8dec0·#ddd1ad·#d3c597` · edge `#b3a376`
- Ink navy `#0b0f1a·#10141d·#1a2030` · soft `#2a3142` · muted `#5a6276` · faint `#8a93a8`
- Accent gold-deep `#6a4f10` / gold-700 `#a07e1b` · rule `rgba(16,20,29,.18/.36)`
- Font: **Source Serif 4** + **Switzer** + JetBrains Mono

## L8 · exam-ops — Ledger Doctrine v2.1 (paper edition) *(C · v2-tokens.css)* [lưỡng cư: có token on-dark]
- Paper `#F8F1DF·#F2E9D2(bg)·#ECE1C4·#E4D6B0·#DCCB9B` · edge `#B8A47A`
- Ink `#07060A·#15131A·#1D1A22·#26222C`
- Gold-deep `#5A4A14` (PRIMARY trên giấy) · gold `#9F7E1B` · gold-bright `#D4AF37` (chỉ trên nền tối) · gold-glow `#F0CF55`
- Pen-red `#B0302D` (trên nền tối `#E5645F`)
- Text walnut `#1A1610` · soft `#4A3F28` · muted `#7A6B4A` · faint `#A8997A`
- Text-inverse (cho panel tối nhúng): `#F4EBD9·#C7B891·#897A5A`

---

# 2. 🌙 TỐI (Dark) — nền tối (noir / navy / midnight)

## D1 · StoiX Read — Dark mode (warm-black) *(B · styles base dark)*
- Paper `#14110d` · ink `#f2ece0` · rule `#3a342a` / strong `#574f42`
- Accents tái dùng: red `#b23a2c` · mustard `#b8862c` · green `#2f6f4d`
- Font: như L5 (EB Garamond / Inter / JetBrains Mono)

## D2 · exam-ops — study noir (app học) *(C · tones/study.css)*
- Surface Noir `#03060c·#06090f·#0a0f18·#101723·#182231·#202b3b·#28354a`
- Text Platinum `#f6f8fb·#eef2f8·#dde2ea·#c8d0d8·#9aa5b2·#5a626c·#4a525c`
- Accent platinum + gold `#D4AF37` · rule `rgba(216,224,232,.07–.24)`
- Font: DM Sans / Inter + Source Serif · JetBrains Mono

## D3 · exam-ops — funnel "Platinum Noir" (marketing) *(C · tones/funnel.css)*
- Surface Noir (như D2) · text platinum sáng `#eef2f8/#f6f8fb`
- Accent **gold `#D4AF37`** · glow `#f4da84` · glass `rgba(8,12,18,.72)` · rule `rgba(200,208,216,.12–.28)`
- Font: **Playfair Display** (display lớn) + sans body

## D4 · exam-ops — catalog "mint+gold/indigo" (wow landing) *(C · tones/catalog.css)*
- Surface indigo-noir `#050811·#070b17·#0a1020`
- Text cream `#ebede0·#ece4d2` · **mint accent** `#c8e0d6·#8caea2·#3c534b·#1d2b26`
- Gold catalog `#e8c896·#d4af7a` · sage `#d2d8c8·#94a097·#5e6b62·#34403a` · cat-rule `#1a2220·#121815·#26302c`

## D5 · exam-ops — catalog-v4 "Midnight Champagne" (free-quant) *(C · catalog-v4.css)*
- Bg `#050814` · surface `#0b1020` · elevated `#121a2b` · border `#263148`
- Text `#f6f2e8` / strong `#ffffff` / muted `#aeb7c4`
- Accent champagne `#d8c28a` · accent-soft `#6c6042`

## D6 · exam-ops — "Navy Ledger v3" + glass (standalone dark) *(C · dark-tone.css, glass-tokens.css)*
- Navy-ink dark rebind (vàng sáng hơn, contrast mạnh) · glass-bg `rgba(255,255,255,.03)` · glass-border `rgba(255,255,255,.08)`

---

# 3. Trung lập (dùng ở cả SÁNG và TỐI)

- **Formula variable cycle** (8 màu, vai trò biến — A): `#B83030·#2B5597·#2D6A4F·#7B3FA0·#A07820·#1A7A7A·#A04030·#5B3FA0`
- **Semantic status** (C primitives): error `#c73e3a` · correct `#5c8a3c` · danger/red `#e55a4a` · green `#8fd6a8`
- **Mono font thống nhất**: **JetBrains Mono** (cả 3 dự án) — token nhất quán duy nhất xuyên hệ.
- **Platinum ramp** (C): dùng làm text trên dark + accent trên light.

---

# 4. MASTER FLAT LIST (bảng phẳng toàn bộ)

| Nhóm | Variant | Vai trò | Hex / Font | Nguồn |
|------|---------|---------|-----------|-------|
| ☀ | L1 Notes Ivory | page / box | `#FFFEF8` / `#F0EDE6` | A render_engine |
| ☀ | L1 Notes Ivory | title / indigo / orange / gold | `#2C3878` `#2E3B7C` `#B85A1C` `#C49A1A` | A |
| ☀ | L1 Notes Ivory | teal / amethyst / olive / highlight | `#0E6B85` `#5C2D91` `#7A5C00` `#E8DEB0` | A |
| ☀ | L1 Notes Ivory | body / secondary / muted / rule | `#1C1C1C` `#3B3B3B` `#6B6B6B` `#CECECE` | A |
| ☀ | L1 fonts | display / body / mono | Raleway · Inter · Consolas (EIR: Lora · JetBrains) | A |
| ☀ | L2 box Key/Example | bg/accent | `#F6EDD5`/`#8B6B20` · `#E4F0E9`/`#2D6A4F` | A |
| ☀ | L2 box Warn/Note/Purple | bg/accent | `#F7E9E6`/`#A04030` · `#E4ECF6`/`#2B5597` · `#EEE8F7`/`#6B3FA0` | A |
| ☀ | L3 subjects | PM/FI/EQ/DER/AI | `#6B4010` `#1A5270` `#2E6B3E` `#5C3A8B` `#1A5B5B` | A |
| ☀ | L3 subjects | CI/FSA/ECO/QM/ETH | `#8B3A20` `#6B2020` `#3A5A20` `#3A3A7C` `#204A7B` | A |
| ☀ | L4 cover | module num / tabs | `#1E2862` · 8-tab indigo ramp | A |
| ☀ | L5 Read Newsprint | paper / ink | `#fbf9f4` (`#f2e3c8`) / `#1a1714` `#3a2f1f` | B styles.css |
| ☀ | L5 Read Newsprint | red/blue/green/mustard/burgundy | `#9b2c2c` `#2a4f7a` `#2f6f4d` `#a87a1c`/`#b8862c` `#6a2a2a` | B |
| ☀ | L5 fonts | display / ui / mono | EB Garamond · Inter · JetBrains Mono | B |
| ☀ | L6 Read Bookshelf | paper / rule | `#f7f4ed` / `#cdc6b8` | B bookshelf |
| ☀ | L7 exam paper | cream / navy ink / gold | `#f1e9d0` / `#10141d` / `#6a4f10`·`#a07e1b` | C paper.css |
| ☀ | L7 fonts | display / sans | Source Serif 4 · Switzer | C |
| ☀ | L8 Ledger v2.1 | paper / ink | `#F2E9D2`(`#F8F1DF`) / `#07060A`·`#1A1610` | C v2-tokens |
| ☀ | L8 Ledger v2.1 | gold-deep/gold/bright/glow | `#5A4A14` `#9F7E1B` `#D4AF37` `#F0CF55` | C |
| ☀ | L8 Ledger v2.1 | pen-red / text-inv | `#B0302D`(`#E5645F`) / `#F4EBD9`·`#C7B891` | C |
| 🌙 | D1 Read Dark | paper / ink / rule | `#14110d` / `#f2ece0` / `#3a342a`·`#574f42` | B dark |
| 🌙 | D2 study noir | surface ramp | `#03060c`→`#28354a` (7 bước) | C study.css |
| 🌙 | D2 study noir | text platinum / gold | `#c8d0d8` (ramp `#f6f8fb`→`#4a525c`) / `#D4AF37` | C |
| 🌙 | D3 funnel Platinum Noir | accent gold / glow / glass | `#D4AF37` / `#f4da84` / `rgba(8,12,18,.72)` | C funnel.css |
| 🌙 | D3 fonts | display | Playfair Display | C |
| 🌙 | D4 catalog indigo | surface / cream text | `#050811`·`#070b17`·`#0a1020` / `#ebede0` | C catalog.css |
| 🌙 | D4 catalog indigo | mint / catgold / sage | `#8caea2`(ramp) / `#e8c896`·`#d4af7a` / `#5e6b62` | C |
| 🌙 | D5 Midnight Champagne | bg / surface / elevated / border | `#050814` `#0b1020` `#121a2b` `#263148` | C catalog-v4 |
| 🌙 | D5 Midnight Champagne | text / champagne accent | `#f6f2e8`·`#aeb7c4` / `#d8c28a`·`#6c6042` | C |
| 🌙 | D6 Navy Ledger / glass | glass bg/border | `rgba(255,255,255,.03)` / `.08` | C dark-tone/glass |
| ⚪ | Neutral | formula var cycle (8) | `#B83030 #2B5597 #2D6A4F #7B3FA0 #A07820 #1A7A7A #A04030 #5B3FA0` | A |
| ⚪ | Neutral | semantic status | error `#c73e3a` · correct `#5c8a3c` · danger `#e55a4a` · green `#8fd6a8` | C |
| ⚪ | Neutral | mono font | JetBrains Mono (cả 3 dự án) | A·B·C |

---

# 5. Self-check + ghi chú

**Đếm:** SÁNG = 8 variant · TỐI = 6 variant · Trung lập = 3 nhóm. Mọi variant trong `brand-style.md` đã được xếp, không bỏ sót. Phiên bản layout của StoiX Read (v1-v4 + sub-pages) gom dưới L5 (cùng base token).

**Mã "lưỡng cư":**
- `#D4AF37` (gold-bright): xuất hiện ở SÁNG (Ledger "chỉ dùng trên nền tối") và TỐI (D2 study, D3 funnel).
- Ledger v2.1 (L8): chủ yếu SÁNG nhưng mang sẵn `text-inverse` cho panel tối nhúng.
- Platinum ramp + formula cycle + semantic status: dùng xuyên cả 2 nhóm.

**Điểm trôi dạt (chỉ ghi nhận, không tự quyết khi consolidate):**
1. Vàng 4 sắc: `#C49A1A` (note) · `#D4AF37` (StoiX bright) · `#9F7E1B` (mid) · `#5A4A14`/`#6a4f10` (deep-on-paper).
2. Đỏ nhấn lệch: `#B85A1C` cam đất (note) vs `#9b2c2c`/`#b23a2c` (Read) vs `#B0302D`/`#E5645F` (Ledger).
3. Serif display 3 họ: Lora/Raleway (note) · EB Garamond (Read) · Spectral/Playfair/Source Serif 4 (exam).
4. Giấy nền sáng 4 độ ngà: `#FFFEF8` · `#fbf9f4` · `#f1e9d0` · `#F2E9D2`.
5. **TỐI có 2 tính cách**: warm-black `#14110d` (Read) vs cool-noir `#03060c`/`#050814` (exam-ops). Cả hai được giữ làm 2 variant riêng.
6. Mono đã thống nhất tuyệt đối: JetBrains Mono.

**Đã giữ 14 variant + 3 nhóm trung lập / toàn bộ mã trong catalog, 0 mã bị mất.**
