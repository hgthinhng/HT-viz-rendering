# StoiX — Brand Style Catalog (khai báo / thống kê hiện trạng)

> Mức độ: **CATALOG / INVENTORY** — chỉ liệt kê và đối chiếu các theme/phiên bản đang tồn tại ở 3 dự án.
> CHƯA consolidate. Bước hợp nhất thành 1 bộ brand thống nhất sẽ làm ở vòng sau.
> Ngày probe: 2026-06-11. Nguồn: đọc trực tiếp file thiết kế trong từng repo (không bịa giá trị).

---

## 0. Bản đồ tổng quan

| # | Dự án | Loại | Tên/định danh brand | Nơi định nghĩa thiết kế |
|---|-------|------|---------------------|--------------------------|
| A | CFA Study Notes (`XuLyNotes moi`) | Note .docx | Hệ render note CFA L2 | `render_engine.py` (palette C, FONT_STACKS, SUBJECT_COLORS) |
| B | Web Tin tuc | Web tĩnh (báo) | **StoiX Read** — "Web làm báo cho HT" | `styles.css` (base) + `styles-v3/v4.css`, `index-v4.html` |
| C | exam-ops | App Next/React (CFA prep) | **StoiX Design System (S2)** + Brand Book v2.1 "The Ledger Doctrine" | `src/ds/tokens/*` + `src/styles/*` |

**Sợi chỉ chung:** giấy ấm + mực sẫm + vàng antique + một sắc đỏ nhấn (Pompeii / pen red), chữ serif làm display, kèm biến thể nền tối "Platinum Noir". Hai dự án web (B, C) dùng chung tên brand **StoiX**. Bộ note CFA (A) là một hệ editorial song song, độc lập về token.

---

## A. CFA Study Notes — hệ render .docx

Nguồn chân lý: `note-pipeline-render/scripts/render_engine.py`.

### A.1 Typography (font stacks)
| Stack | Tên | Body | Display | Mono / Math |
|-------|-----|------|---------|-------------|
| **B** (mặc định) | Modern Hybrid | Inter | Raleway | Consolas |
| **D** (EIR mới) | Editorial Institutional Research | Inter | Lora (serif) | JetBrains Mono |
| A | Editorial Textbook | Source Serif Pro | Fraunces | Source Code Pro |
| C | Vietnamese-Optimized | Be Vietnam Pro | Be Vietnam Pro | Source Code Pro |

### A.2 Màu cốt lõi
| Vai trò | Hex | Vai trò | Hex |
|---------|-----|---------|-----|
| Nền trang (giấy ngà) | `#FFFEF8` | Nền hộp chung | `#F0EDE6` |
| Tiêu đề (section purple) | `#2C3878` | Indigo | `#2E3B7C` |
| Số mục (cam đất) | `#B85A1C` | Vàng đồng (kẻ) | `#C49A1A` |
| Thuật ngữ (teal) | `#0E6B85` | Highlight | `#E8DEB0` |
| Tham chiếu Công thức (amethyst) | `#5C2D91` | Tham chiếu Ví dụ (olive) | `#7A5C00` |
| Chữ body | `#1C1C1C` | Chữ mờ | `#6B6B6B` |

### A.3 Hộp callout (nền / accent)
| Hộp | Nền | Accent |
|-----|-----|--------|
| ĐIỂM MẤU CHỐT (Key) | `#F6EDD5` | `#8B6B20` |
| VÍ DỤ MINH HỌA | `#E4F0E9` | `#2D6A4F` |
| LƯU Ý QUAN TRỌNG | `#F7E9E6` | `#A04030` |
| GHI CHÚ BỔ SUNG | `#E4ECF6` | `#2B5597` |
| GỢI Ý HÌNH / AI PROMPT | `#EEE8F7` | `#6B3FA0` |
| KEY TAKEAWAYS (EIR) | `#F6EDD5` | `#8B6B20` |

### A.4 Màu biến công thức (vòng 8 màu)
`#B83030` · `#2B5597` · `#2D6A4F` · `#7B3FA0` · `#A07820` · `#1A7A7A` · `#A04030` · `#5B3FA0`

### A.5 Màu nhấn theo môn (trang bìa)
PM `#6B4010` · FI `#1A5270` · EQ `#2E6B3E` · DER `#5C3A8B` · AI `#1A5B5B` · CI `#8B3A20` · FSA `#6B2020` · ECO `#3A5A20` · QM `#3A3A7C` · ETH `#204A7B`

---

## B. StoiX Read (Web Tin tuc) — site báo editorial

Brand: **StoiX Read** · "Vol. II · Founded MMXXIV · Sài Gòn". Bản chốt build: `index-v4.html`.
Token gốc: `styles.css`; component: `styles-v3.css`; polish: `styles-v4.css`.

### B.1 Typography
| Vai trò | Token | Font |
|---------|-------|------|
| Body / Display | `--font-body` / `--font-display` | **EB Garamond** (fallback Cormorant Garamond), serif |
| UI | `--font-ui` | Inter |
| Mono | `--font-mono` | JetBrains Mono |
| Đã thử ở các version | — | Spectral, Source Serif 4, Fraunces, Be Vietnam Pro, Caveat |

### B.2 Palette (giấy báo ấm)
| Vai trò | Hex |
|---------|-----|
| Paper (light, mặc định) | `#fbf9f4` (biến thể `#f2e3c8`, bookshelf `#f7f4ed`) |
| Ink | `#1a1714` / phụ `#3a2f1f` |
| **Accent — Pompeii red** | `#9b2c2c` (trước đây `#b23a2c`) |
| Accent blue (series, longform) | `#2a4f7a` |
| Accent green (upside, growth) | `#2f6f4d` |
| Accent mustard (highlight, callout) | `#a87a1c` / `#b8862c` |
| Accent burgundy (archived) | `#6a2a2a` |
| Chart up / down | `#2f6f4d` / `#b23a2c` |
| Rule | `#d8d2c3` / `#d4be99` |
| **Dark mode** | paper `#14110d`, ink `#f2ece0` |

### B.3 Phiên bản / theme đang tồn tại
| Version / theme | File | Trạng thái |
|-----------------|------|------------|
| v4 (Landing chốt) | `index-v4.html` + `styles-v4.css` | ★ Bản cuối |
| v3 | `index-v3.html` + `styles-v3.css` | Component layer (vẫn dùng) |
| v2 | `index-v2.html` + `styles-home-v2.css` | Cũ, giữ so sánh |
| v1 | `index.html` + `styles.css` + `styles-home.css` | Base tokens |
| Reader | `reader.html` + `styles-reader-v3.css` | Trang đọc bài |
| Bookshelf | `bookshelf.html` + `styles-bookshelf.css` | Tủ sách |
| Studies | `studies.html` + `styles-studies.css` | Chuyên đề |
| Brain | `brainstorm*.html` + `styles-brain.css` | Idea maps |
| Editor / Admin | `styles-editor.css` / `styles-admin.css` | Hậu trường |
| Glossary | `glossary.html` | Thuật ngữ |

### B.4 Layout token
shell `1280px` · wide `1040px` · article `720px` · narrow `560px` · body text `1.28rem` / line-height `1.62`.

---

## C. StoiX exam-ops — Design System S2 (app CFA prep)

Brand: **StoiX Design System (S2)** — "one token source of truth, 2 surfaces (study + funnel)".
Kiến trúc 3 lớp: `primitives (--p-*)` → `semantic (--ds-*)` → `tones ([data-tone])`.
Ngoài ra có Brand Book v2.1 "The Ledger Doctrine" (`v2-tokens.css`).

### C.1 Typography (primitives)
| Token | Font | Dùng cho |
|-------|------|----------|
| `--p-font-spectral` | Spectral (fallback Source Serif 4) | serif display |
| `--p-font-source-serif` | Source Serif 4 (fallback Newsreader) | serif body |
| `--p-font-playfair` | Playfair Display | funnel display lớn |
| `--p-font-dmsans` | DM Sans (fallback Inter) | sans body |
| `--p-font-inter` | Inter | UI |
| `--p-font-switzer` | Switzer | paper tone sans |
| `--p-font-mono` | JetBrains Mono | mono |

### C.2 Tones (theme) — 5 tone chính
| Tone | Mô tả | Surface | Ink / Text | Accent |
|------|-------|---------|------------|--------|
| **study** | App học CFA: calm, dày, dễ đọc | Noir `#03060c`–`#28354a` | platinum `#c8d0d8` | platinum/gold |
| **funnel** | "Platinum Noir" marketing: sang, glass, type lớn | Noir | platinum sáng | **gold `#D4AF37`** |
| **catalog** | "Wow" landing: mint + gold trên indigo | Catalog-noir `#050811` | cream | **mint `#8caea2`** + catgold `#e8c896` |
| **paper** | LIGHT navy-editorial (checkout/refund) | cream `#f1e9d0` | navy ink `#10141d` | gold-deep `#6a4f10` (Source Serif 4 + Switzer) |
| **catalog-v4** | DARK "Midnight Champagne" (free-quant) | `#050814` | `#f6f2e8` | champagne `#d8c28a` |

### C.3 Ramp màu (primitives)
| Ramp | Dải |
|------|-----|
| Noir (xanh đen) | `#03060c` → `#06090f` → `#0a0f18` → `#101723` → `#182231` → `#202b3b` → `#28354a` |
| Platinum (neutral sáng) | `#f6f8fb` → `#eef2f8` → `#dde2ea` → `#c8d0d8` → `#9aa5b2` → `#5a626c` → `#4a525c` |
| Paper light (navy editorial) | `#f6efdb` → `#f1e9d0` → `#e8dec0` → `#ddd1ad` (edge `#b3a376`) |
| Cream + sage | cream `#ebede0`/`#ece4d2` · sage `#d2d8c8`→`#94a097`→`#5e6b62`→`#34403a` |
| Midnight Champagne | bg `#050814` · surface `#0b1020` · accent `#d8c28a` |
| Gold | `#d4af37` · glow `#f4da84` · catgold `#e8c896`/`#d4af7a` |
| Semantic | error `#c73e3a` · correct `#5c8a3c` · danger `#e55a4a` · green `#8fd6a8` |

### C.4 Brand Book v2.1 — "The Ledger Doctrine" (Paper edition · `v2-tokens.css`)
Bản brand chính thức nhất, đọc như nhật ký tài chính trên giấy:
| Nhóm | Token → Hex |
|------|-------------|
| Paper | `--paper-0 #F8F1DF` · `--paper-1 #F2E9D2` (bg) · `#ECE1C4` · `#E4D6B0` · `#DCCB9B` · edge `#B8A47A` |
| Ink | `--ink-0 #07060A` · `#15131A` · `#1D1A22` · `#26222C` |
| Gold | `--gold-deep #5A4A14` (PRIMARY trên giấy) · `--gold #9F7E1B` · `--gold-bright #D4AF37` (trên nền tối) · `--gold-glow #F0CF55` |
| Đỏ | `--pen-red #B0302D` · trên nền tối `#E5645F` |
| Text | `#1A1610` (mực óc chó) · soft `#4A3F28` · muted `#7A6B4A` · faint `#A8997A` |

### C.5 Theme standalone khác (trong `src/styles`)
`platinum-tone.css` · `dark-tone.css` ("Navy Ledger v3") · `glass-tokens.css` · `editorial.css` · `v2-tokens.css` (Ledger Doctrine) · `catalog-tone.css` · `catalog-v4-tokens.css` · `study-app-shell.css`.

---

## D. Quan sát nhanh (chưa phải consolidate)
1. **Vàng** là hằng số xuyên 3 dự án nhưng khác sắc: note `#C49A1A`, StoiX bright `#D4AF37`, paper deep `#5A4A14`/`#6a4f10`.
2. **Đỏ nhấn**: note dùng cam đất `#B85A1C`; StoiX dùng đỏ Pompeii/pen `#9b2c2c`/`#B0302D`.
3. **Giấy ấm + mực sẫm** là nền tảng chung; StoiX có thêm trục nền tối (Noir / Platinum Noir / Midnight Champagne).
4. **Mono** thống nhất: JetBrains Mono ở cả 3 (note EIR + StoiX Read + exam-ops).
5. **Serif display** mỗi nơi một họ: note Lora/Raleway · StoiX Read EB Garamond · exam-ops Spectral/Playfair/Source Serif 4. Đây là điểm cần cân nhắc khi hợp nhất sau.
