---
title: "Reference Visual Artifact Policy — OPVIA Sigma Design Bible, Chart Types, SVG Rules, Export Conventions"
module_type: "reference"
file_name: "reference-visual-artifact-policy.md"
purpose: "Define when and how OPVIA Sigma generates visual artifacts. Specifies the OPVIA Design Bible palette, canonical visual patterns, typography rules, and file naming conventions for research outputs."
primary_triggers:
  - "visual artifact"
  - "chart"
  - "diagram"
  - "SVG"
  - "Design Bible"
  - "OPVIA palette"
  - "màu sắc biểu đồ"
  - "trực quan hoá"
  - "bảng màu"
when_to_use:
  - "When generating any chart, diagram, or visual artifact in OPVIA research outputs."
  - "When deciding between visual artifact and markdown table for data presentation."
  - "When formatting a daily brief, deep-dive memo, or linkage analysis with visual elements."
when_not_to_use:
  - "Do not use to replace analytical reasoning with decorative visuals."
  - "Do not use to generate 3D charts, pie charts, or gimmicky visualizations."
related_modules:
  - "reference-vn-data-sources.md"
  - "workflow-daily-brief.md"
  - "workflow-deep-dive.md"
  - "workflow-cross-asset-linkage.md"
  - "core-output-contracts.md"
authoritative_citations:
  - "OPVIA Design Bible — Prussian Blue / Aged Brass / Slate Blue / Bordeaux palette."
  - "Focus_Brief.md Appendix — Visual artifact standards for institutional research."
output_owner: "Format reference only; does not own analytical conclusions."
---

# Reference Visual Artifact Policy — Chính sách Trực quan hoá OPVIA Sigma

Purpose: Standardize every visual artifact produced by OPVIA Sigma. Think-tank institutional cần **nhất quán, đọc được, truyền tải mechanism rõ ràng**.

Trigger keywords: visual artifact, chart, diagram, SVG, Design Bible, OPVIA palette, màu sắc biểu đồ, trực quan hoá, bảng màu, DuPont, linkage matrix, regime signature.

---

## 1. OPVIA Design Bible — Bảng màu Chuẩn

> Dùng nhất quán xuyên suốt. Không thêm màu ngoài danh sách. Tối đa 4 chuỗi dữ liệu trên chart. Không gradient. Prussian Blue + Aged Brass là cặp primary mặc định cho line chart 2 series. Bordeaux chỉ dùng cho điểm cần flag.

| Vai trò | Tên | Hex | Dùng cho |
|---|---|---|---|
| **Primary** | Prussian Blue | `#003366` | Tiêu đề, đường chính line chart, header table, primary bars |
| **Accent** | Aged Brass | `#8B7355` | Highlight quan trọng, đường thứ hai, annotation markers |
| **Secondary** | Slate Blue | `#6B7B8C` | Dữ liệu phụ, grid lines, nhãn trục, border nhẹ |
| **Emphasis** | Bordeaux | `#722F37` | Cảnh báo, điểm đột biến, bear-case scenarios, negative divergence |
| **Positive** | Deep Forest | `#2D5A3D` | Tích cực, bull-case, upside signal (dùng hạn chế) |
| **Neutral background** | Off-White | `#F5F5F0` | Nền chart, background artifact |
| **Neutral text** | Charcoal | `#2C2C2C` | Body text, nhãn trục, chú thích |
| **Light grid** | Silver | `#D1D5DB` | Grid lines, divider, viền table |

---

## 2. Typography

- **Font chính:** System sans-serif hoặc Google Fonts: **Inter**, **Noto Sans Vietnamese**, **Roboto**. Ưu tiên font hỗ trợ tiếng Việt đầy đủ.
- **Font size tối thiểu:** Legend/label **11px**, table cell **12px**, axis label **11px**, tiêu đề chart **14–16px bold**.
- **Font trong SVG:** Khai báo `font-family` trong SVG. Không dùng font hiếm.
- **Số liệu trong table:** Căn phải. Đơn vị trong header, không lặp lại trong cell.
- **Tỷ lệ:** Width:height ≈ **16:9** hoặc **4:3**. Không vuông trừ heatmap/matrix.

---

## 3. Chart Types Được Phép & Cấm

### ✅ Được phép

| Loại chart | Khi nào dùng | Giới hạn |
|---|---|---|
| **Line chart** | Xu hướng theo thờii gian, so sánh 2–3 series | Max 4 lines. Dùng dash pattern phân biệt. |
| **Bar chart** | So sánh, ranking | Max 12 bars. Sắp xếp descending. |
| **Grouped / Stacked bar** | So sánh multi-category; cơ cấu phần trăm | Max 3 groups × 4 categories. Không stacked nếu < 5%. |
| **Heatmap** | Sensitivity analysis, correlation matrix, DCF (WACC × g) | Color scale: Prussian Blue (thấp) → Off-White (giữa) → Bordeaux (cao). |
| **Scatter plot** | So sánh 2 biến, outlier detection | Kèm trendline nếu correlation. Label outlier rõ ràng. |
| **Sankey diagram** | Dòng tiền/vốn, transmission channels | Max 5–7 nodes. |

### ❌ Cấm tuyệt đối

**Pie / Donut** (góc cạnh khó so sánh → dùng bar), **3D chart** (distort tỷ lệ), **Radar / Spider** (trục không independent → gây hiểu nhầm), **Gauge / Speedometer** (pseudo-precision), **Word cloud** (không truyền tải quantitative information).

---

## 4. Định dạng Artifact

| Loại output | Định dạng ưu tiên |
|---|---|
| **Diagram / Sơ đồ** | **SVG** (Claude Artifact hoặc inline SVG) — Cấu trúc, mechanism, flow. |
| **Chart dữ liệu** | **Markdown table** cho đơn giản; **HTML/SVG chart** cho phức tạp — ≤ 12 data points → table. Trend hoặc multi-series → chart. |
| **Matrix / Heatmap** | **Markdown table với emoji/mã màu text** hoặc **HTML table** — Linkage matrix, correlation matrix, sensitivity table. |
| **Dashboard tóm tắt** | **Markdown table** với icon/status — Red-flag scan, tracker table, regime status. |

**Quy tắc kỹ thuật SVG:** ViewBox rõ ràng (`viewBox="0 0 800 450"`). Inline CSS — không external stylesheet. Font-family khai báo rõ. Stroke width tối thiểu 1.5px cho đường chính. Padding ít nhất 40px mỗi cạnh.

---

## 5. Ba Pattern Trực quan Canonical của OPVIA

### Pattern 1: DuPont Tree

Phân rã ROE thành 3–5 thành phần. SVG flowchart dạng cây từ trên xuống, max 3 tầng. Màu: Prussian Blue = gốc (ROE), Slate Blue = trung gian, Aged Brass = leaf nodes.

### Pattern 2: Linkage Matrix

Workflow cross-asset linkage — strength và direction của transmission channels. Heatmap table hoặc directed graph. Mỗi cell có label "direction + strength + regime condition". Màu: Prussian Blue = strong positive; Slate Blue = weak positive; Off-White = neutral; Aged Brass = weak negative; Bordeaux = strong negative.

### Pattern 3: Regime Signature Chart

Hiển thị current regime classification với 3–4 key indicator. Multi-panel small multiples hoặc combo chart (line + shaded region). Annotation đánh dấu ngày regime switch. Shelf life ghi chú dưới chart. Màu: mỗi regime = nền shaded nhẹ (Prussian Blue = A, Slate Blue = B, Aged Brass = C). Đường indicator = Charcoal hoặc Bordeaux nếu threshold bị vượt.

---

## 6. Quy tắc Quyết định: Visual vs Markdown Table

### Tạo Visual khi:

1. Có **≥ 8 data points** theo thờii gian → line chart.
2. So sánh **≥ 3 entities** trên cùng một metric → bar chart.
3. Cần thể hiện **relationship/correlation** giữa 2 biến → scatter plot.
4. Cần thể hiện **cấu trúc/cơ chế** (DuPont, transmission channel) → SVG diagram.
5. Dữ liệu có **pattern bất thường** (break, divergence, regime shift) cần nhìn bằng mắt.

### Chỉ dùng Markdown Table khi:

1. Dữ liệu **≤ 6 rows × 4 columns** và đơn giản.
2. Cần **tra cứu nhanh** giá trị chính xác (spot rate, ratio hiện tại).
3. Là **tracker table** với status icon (ON-TRACK / WATCHING / TRIGGERED / BROKEN).
4. Là **summary table** ở cuối memo — tóm tắt kết luận bằng số.

**Quy tắc vàng:** Nghi ngờ → dùng **table**. Table không bao giờ sai; chart dở có thể misleading. Chỉ dùng chart khi pattern cần nhìn thấy.

---

## 7. Quy ước Đặt tên & Xuất file Artifact

### Đặt tên file

```
{date}_{asset}_{type}_{descriptor}.{ext}
```

- `date`: `20260419` (YYYYMMDD)
- `asset`: `vn-index`, `usd-vnd`, `hpg`, `macro`, `cross-asset`
- `type`: `chart`, `diagram`, `matrix`, `heatmap`, `tree`
- `descriptor`: `dupont`, `linkage`, `regime`, `sensitivity`, `trend`
- `ext`: `svg` (diagram), `png` (chart raster), `md` (table embedded)

**Ví dụ:** `20260419_vn-index_chart_trend.svg`

### Xuất và lưu trữ

- Artifact sinh ra trong Claude conversation → analyst tự export nếu cần.
- Mọi artifact phải có **caption**: "Hình X — [mô tả ngắn] — Nguồn: [source] — Ngày: [date]".

---

## 8. Checklist Quality

Trước khi publish: palette đúng 4 màu chính + neutral; font ≥ 11px; tiếng Việt dấu rõ; không dùng chart type cấm; tiêu đề rõ; trục có nhãn và đơn vị; caption đi kèm (nguồn + ngày); max 5–7 chuỗi dữ liệu.

---

## Cross-references

- Nguồn dữ liệu: `reference-vn-data-sources.md`
- Daily Brief: `workflow-daily-brief.md`
- Deep-dive: `workflow-deep-dive.md`
- Linkage Analysis: `workflow-cross-asset-linkage.md`
- Output chung: `core-output-contracts.md`

---

> **Document Control**
> - Version: v1.0 (Wave 4 — Lane 11)
> - Ngày: 2026-04-19
> - Author: OPVIA Sigma Build Team
> - Approver: OPVIA
> - Related modules: reference-vn-data-sources.md, workflow-daily-brief.md, workflow-deep-dive.md, workflow-cross-asset-linkage.md, core-output-contracts.md
> - Source port: FinMentor 42-visual-artifact-policy.md + Focus_Brief Design Bible Appendix
