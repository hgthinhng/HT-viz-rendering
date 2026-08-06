# Harvest — Premium CFA design/viz assets (2026-08-06)

Nguồn thật KHÔNG nằm ở `_library` (chỉ là output PNG rỗng ruột) mà ở:
`L2 xử lý notes/_CLAUDE_MEMORY/from_XuLyNotes_moi/` (token + docx render engine)
và `Module Icons/` (illustration prompt system + 97 banner AI-gen).

## design-tokens/
- `tokens.css` — CSS custom properties canonical, 2 mode Light/Dark, nguồn chân lý màu.
- `theme.md`, `brand-style.md`, `brand-consolidated-light-dark.md` — tài liệu nghiên cứu/consolidate
  toàn bộ palette qua 3 dự án (CFA Notes, StoiX Read, StoiX exam-ops).
- `brand_theme_preview.html` — trang demo mở được, có 2 thẻ editorial mock Light/Dark, type specimen,
  token swatch. Copy nhanh nhất để xem "chất" theme.
- `PROMPT_*.md` — prompt gốc dùng để sinh 3 file .md ở trên (tái dùng cho việc audit theme khác).

## render-engine/
- `render_engine.py` (3443 dòng) + `render_engine_extras.py` — engine Python sinh thẳng OOXML (.docx),
  KHÔNG phải HTML/CSS. Chứa toàn bộ logic component: box callout (KEY/EXAMPLE/WARN/NOTE/PURPLE),
  formula card màu-biến, data cards, diagram primitives (timeline/hub/flow/tree2x2/payoff + extras:
  matrix2x3/pyramid/cycle/comparison/gauge), table điểm chẵn-lẻ, cover, TOC, glossary, pull-quote style
  cho BOX_KEY. Giá trị lớn nhất là LOGIC/PATTERN thiết kế (đọc để port ý tưởng sang HTML), không phải
  code chạy được thẳng cho web.

## pipeline-docs/
- `note-pipeline-viz.SKILL.md`, `note-pipeline.SKILL.md`, `DEPLOY_VIZ.md` — mô tả kiến trúc pipeline
  ghi chú CFA: advisor chọn loại figure, marker `[VIZ:]`/`[FIGURE:]`, engine "viz-factory" render qua
  PowerShell + headless Chrome (ECharts cho candlestick/OHLC, Mermaid cho flowchart/decision tree,
  custom HTML/CSS cho card/table/DuPont/SWOT/heatmap) rồi chụp PNG nhúng vào .docx.
  QUAN TRỌNG: bản thân folder engine "viz-factory" / "cfa-viz-factory" đã KHÔNG còn trên đĩa (đã tìm
  toàn bộ Desktop + `.claude/skills`, không thấy `catalog/`, `engine/build_spec.ps1`,
  `references/VIZ_ADVISOR.md`). Chỉ còn tài liệu mô tả kiến trúc + 46 ảnh output.

## viz-samples/
- `gallery.html` + 46 PNG — output đã render của viz-factory (mất source). Đây là bằng chứng hình ảnh
  duy nhất còn lại cho phong cách chart: kicker cam-nâu viết hoa, tiêu đề Indigo/Fraunces-serif, gạch
  chân vàng, nền giấy ngà `#FAFAF7`-ish, caption "Hình N.M.x · Minh họa CFA Level II" xanh đậm + ý chữ
  nghiêng xám. 46 loại: xem tên file (waterfall, dupont, sankey_mini, heatmap, kpi_card_with_sparkline,
  echarts (candlestick), mermaid (flowchart), swot, table, tornado, football_field, fan_chart...).

## illustration-icons/
- `MOTIF_TABLE.md` — bảng đầy đủ 97 scene-motif (1 dòng/module CFA L1, đủ 10 subject) + prompt template
  chuẩn dùng cho Nano Banana Pro (AI image gen), kèm palette cố định (cream `#F5EFE2`, navy `#16283F`,
  teal `#2F7E7A`, gold `#C9A227`) và constraint bố cục (central-band, full-bleed, cấm khung/panel).
  Đây là tài sản sáng tạo quý nhất trong toàn bộ thư viện — một "thư viện ẩn dụ hình ảnh" cho từng khái
  niệm tài chính, có thể tái dùng nguyên ý tưởng cho báo cáo ngành/công ty (ví dụ: DuPont = cân,
  callable bond = bập bênh giá/lợi suất, securitization = phễu gộp-cắt lát...).
- `ALL_97_contact_sheet.png` — bản xem nhanh cả 97 icon cùng lúc.
- `raw-sample/`, `out_169-sample/` — 5 ảnh mẫu (raw vuông AI-gen + 1 bản đã crop 16:9) để xem chất lượng
  thật. Toàn bộ 97×2 ảnh gốc (raw + out_169) nặng ~40-50MB, không copy hết, chỉ lấy mẫu.
  LƯU Ý: đây là ảnh raster do AI sinh (Nano Banana Pro), KHÔNG phải SVG vẽ tay, không có file vector
  editable — không thể chỉnh sửa lại ngoài việc generate lại bằng đúng prompt template.
