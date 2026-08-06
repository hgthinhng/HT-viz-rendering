# HT-viz-rendering: bàn giao cho phiên mới

Đọc file này trước tiên. Nó cho biết đang ở đâu và làm gì tiếp.

## Việc tiếp theo, làm ngay

Thi công **Phase 1** theo `docs/superpowers/plans/2026-08-06-ht-viz-rendering-phase1.md` bằng skill `superpowers:subagent-driven-development`. Kế hoạch có 8 task, 64 step, mỗi step đã có code thật và lệnh thật, không có chỗ trống nào cần đoán.

Bắt đầu từ Task 1. Không nhảy cóc, vì Task 1 dựng `package.json` mà mọi task sau đều cần.

## Repo này là gì

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF in được, có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG neo được số liệu vào từng bộ phận vật thể.

Thiết kế đầy đủ ở `docs/specs/2026-08-06-ht-viz-rendering-design.md`, 15 mục. Đọc mục 3 (bảng quyết định đã chốt) và mục 5 (kiến trúc) trước khi động vào code.

## Bối cảnh: mọi thứ trong repo đến từ đâu

Phiên trước dùng 13 subagent khảo sát và thí nghiệm. Kết quả nằm ở `_harvest/`, 860 file, đã commit. Đây là khu tạm, Phase 1 sẽ dỡ dần vào đúng chỗ.

| Thư mục trong `_harvest/` | Nội dung |
|---|---|
| `lab-B-components/PACKAGE/` | 22 component kể chuyện, 24 file catalog, font nhúng base64, script verify. Đã render PDF 16 trang, 0 ảnh raster |
| `lab-C-illustration/PACKAGE/` | 11 minh hoạ ngành SVG, lớp annotation, ngữ pháp vẽ, bảng tra ẩn dụ, prompt vẽ hình mới |
| `lab-A-charts/` | 12 chart ECharts chạy thật, theme, hàm định dạng số tiếng Việt đã test 25/25 |
| `harvest-cfa-skillchain/viz-engine/` | 48 component matplotlib EIR institutional, kèm `EIR_DESIGN.md` |
| `harvest-extras/pipeline-stocklpt/` | Pipeline HTML sang PDF hoàn chỉnh, football_field, sensitivity_grid, adapter FiinQuant |
| `harvest-extras/thinktank/` | 6 hợp đồng đầu ra, nhãn sự kiện/diễn giải/giả thuyết, 12 acceptance test |
| `harvest-misc/vn-humanizer/` | Register R6 dành riêng cho báo cáo tài chính, `lint_vi.py` chạy được |
| `harvest-misc/typst-render/` | Phương án PDF dự phòng, verify vector tuyệt đối nhưng chưa chọn |
| `lab-gate/`, `lab-evidence/` | 6 gate nghiệm thu và evidence ledger, dùng ở Phase 2 |
| `harvest-mindset/` | Giáo trình thiết kế, nguồn cho `doctrine/06-mindset.md` ở Phase 3 |
| `reference-kimi.html` | Báo cáo tham chiếu 815 KB, điểm neo cho token màu |

## Bảy điều đã đo được, đừng làm lại

1. **Chỉ `box-shadow` có blur mới bị nướng bitmap khi in.** Offset cứng blur 0 an toàn tuyệt đối. Đo bằng ba biến thể độc lập.
2. **`@media (max-width: Npx)` thiếu `screen` tự kích hoạt khi in**, vì vùng in A4 chỉ 688 tới 717px sau margin.
3. **Bug rớt dấu tiếng Việt không do engine** mà do khai `font-family` bằng một tên trần thay vì list kết thúc generic keyword. Lỗi ra dạng "Sô´liệu" chứ không phải ô vuông nên rất dễ lọt QC.
4. **Đo dấu tiếng Việt phải dùng mực chữ qua Canvas `measureText()`**. So `getBoundingClientRect().height` với `fontSize × lineHeight` là tautology, không bao giờ phát hiện được lỗi.
5. **Dấu tiếng Việt chỉ giảm 4% ký tự mỗi dòng**, không cần buffer line-height kiểu CJK.
6. **`echarts.init` với `ssr:true` không tự thoát process.** Mọi script chart phải kết bằng `chart.dispose(); process.exit(0);`.
7. **Đếm ảnh trong PDF phải dùng `doc.xref_object`**, `get_images()` bỏ sót ảnh trong Tiling Pattern.

## Ba cái bẫy đã gặp thật, đừng lặp lại

- **Catalog drift**: bộ Opvia có file catalog mô tả HTML dùng class không tồn tại trong CSS. Trang vẫn chạy nhưng suy biến âm thầm. Task 7 của Phase 1 sinh ra để chống đúng bệnh này.
- **PACKAGE tự nhận là tự đủ**: cả hai PACKAGE chạy được ở thư mục gốc của chúng nhưng `ERR_MODULE_NOT_FOUND` khi copy sang chỗ khác. Task 1 vá.
- **Verify script chọn class không tồn tại**: `annotate.js` không gắn class nào cho path và rect, nên script verify sẽ báo PASS mà chưa kiểm gì. Task 4 Step 4 vá.

## Ba xung đột đã phân xử, đừng mở lại

- **Bảng màu**: chốt trắng lạnh (`#051C2C` ink, `#2251FF` accent) chứ không phải giấy ngà ấm. Ba nguồn độc lập hội tụ: `reference-kimi.html`, thư viện style McKinsey, và giáo trình thiết kế dòng 88.
- **Gauge và radar**: cấm. Gauge gợi ý độ chính xác không có thật, radar có trục không độc lập nên diện tích vô nghĩa.
- **Engine PDF**: WeasyPrint, không phải Chromium. Chromium tạo ảnh JPEG ẩn trong Tiling Pattern.

## Các phase sau

Viết plan riêng khi phase trước nghiệm thu xong. Phase 2 pipeline và gate. Phase 3 doctrine và preset. Phase 4 báo cáo mẫu vận tải biển. Scope chi tiết ở cuối file plan Phase 1.

## Nghiệm thu Phase 1

Bốn lệnh này phải chạy sạch từ một shell mới:

```bash
cd ~/HT-viz-rendering
npm install && pip install --break-system-packages -r requirements.txt
npm test
npm run verify
python3 -m pytest tests/ -v
```
