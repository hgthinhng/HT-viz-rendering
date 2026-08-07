---
name: HT-viz-rendering
description: Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản, xuất HTML self-contained và PDF in được. Có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG neo được số liệu vào từng bộ phận vật thể. Dùng khi cần làm báo cáo ngành, báo cáo cổ phiếu, bản tin thị trường, hoặc deal pack.
---

# HT-viz-rendering

File này chỉ ĐỊNH TUYẾN. Đọc phần liên quan tới việc đang làm, đừng đọc hết.

## Tầng doctrine (tư duy thiết kế)

Chưa có ở Phase 1. Bảy file tầng doctrine (đọc trước khi vẽ, chọn kịch bản kể chuyện, gắn nguồn,
chọn chart, viết chữ, vẽ minh hoạ, quyết định khó) sẽ tới ở Phase 3. Cho tới lúc đó, dùng mục
"Ý tham khảo" bên dưới và `CLAUDE.md` làm kim chỉ nam.

## Ràng buộc cứng, không có ngoại lệ

Đây là kết quả ĐO ĐƯỢC, vi phạm là hỏng file giao đi. Chi tiết và lý do ở `CLAUDE.md`.

- Shadow chỉ dùng offset cứng, blur phải bằng 0
- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải có `screen`
- Cấm gauge và radar
- Đếm ảnh raster bằng `doc.xref_object`, không dùng `get_images`
- Không em-dash và en-dash trong mọi nội dung hiển thị
- `font-family` phải là list kết thúc generic keyword, không dùng một tên trần
- `design-system/tokens.css` có hai khối `:root`, không khai một biến ở cả hai khối
- Shadow viết `rgba(R G B / A)`, không dùng dấu phẩy trong ngoặc màu
- File giao khách khai `<html lang="vi" data-theme="light">` để không đổi màu theo máy khách
- Font nhúng thẳng vào file, không trỏ đường dẫn tuyệt đối trên máy đang làm

## Làm một báo cáo: đường ống

Một báo cáo là một THƯ MỤC. Chép `examples/mau-phase2/` làm khung rồi thay nội dung.

```bash
python3 pipeline/orchestrator.py <thu-muc>/noi-dung.md
```

Chạy trọn: sinh hình, ghi kịch bản CK1, dựng ba bản bìa CK2, dựng HTML tự đủ cả bản nội
bộ lẫn bản gửi đi, xuất PDF, rồi chạy mười gate. Quy ước chi tiết ở `CLAUDE.md`.

Ba điều phải nhớ trước khi viết dòng đầu tiên:

- Minh hoạ có callout phải bake bằng `pipeline/bake_svg.mjs` trước, vì WeasyPrint không
  chạy JavaScript nên callout vẽ lúc chạy sẽ vắng mặt khỏi PDF.
- Mỗi số hiển thị viết `{{ma}}` và phải có mặt trong sổ nguồn của báo cáo, xem
  `examples/mau-phase2/so-nguon.json`, nếu không thì build dừng ngay.
- Bản gửi khách xuất bằng `--che-do=gui-di`, và nó KHÔNG mang sổ nguồn.

## Thư viện có gì: đọc mục lục TRƯỚC khi chọn hình

**`catalog/CATALOG.md`** liệt kê cả 108 tài sản của thư viện dưới một dạng duy nhất, mỗi
dòng ghi mã, hình đó trả lời câu hỏi gì, và khi nào đừng dùng nó. Đọc file này là biết
thư viện có gì, không phải mở bốn thư mục và đọc bốn khuôn mô tả khác nhau.

| File | Dùng khi |
|---|---|
| `catalog/CATALOG.md` | chọn hình cho một section. Đây là file nên đọc đầu tiên |
| `catalog/INDEX.json` | cần tra bằng máy: lọc theo nhóm, theo định dạng giao |
| `catalog/contact-sheet.pdf` | muốn NHÌN cả kho một lượt, 50 bản xem trước |

Mục lục sinh tự động từ chính mã nguồn. Sửa mô tả thì sửa ở nguồn (comment đầu file
preset, docstring component, mục `Mô tả / khi nào dùng` của catalog, hoặc `<desc>` của
SVG) rồi chạy `python3 scripts/sinh_catalog.py`. Có test ép mục lục khớp mã nguồn, nên
sửa một bên mà quên bên kia thì `npm test` đỏ.

## Theo thành phần

| Cần | Ở đâu |
|---|---|
| Màu, font, spacing, shadow | `design-system/tokens.css` |
| Component kể chuyện | `components/catalog/` rồi `components/gallery.html` |
| Chart tĩnh cho PDF | `charts/matplotlib/` |
| Chart tương tác cho HTML | `charts/echarts/` |
| Minh hoạ ngành | `illustrations/svg/` và `illustrations/grammar.md` |
| Đường ống và trang giấy | `pipeline/` |
| Mười gate nghiệm thu | `gates/` |
| Báo cáo mẫu chạy được | `examples/mau-phase2/` |

## Ý tham khảo, không phải khuôn ép

Component, preset, và minh hoạ trong repo là THƯ VIỆN THAM KHẢO ĐỂ LẤY Ý, không bắt buộc dùng
hết hay dùng đúng nguyên bản. Thiết kế có tự do sáng tạo, miễn hợp lý.

- Bố cục, nhịp, cách vào bài: xem thư mục `research/` để lấy hướng, đừng chép nguyên.
- Ví dụ báo cáo tham chiếu: xem thư mục `samples/`.
- Ngữ pháp vẽ minh hoạ ngành: `illustrations/grammar.md`.

## Trước khi giao file

Chạy `node gates/run.mjs <html> <pdf> --che-do=gui-di` trên đúng bản sắp gửi, và
`npm run verify` cho thư viện hình. FAIL là không được giao.
