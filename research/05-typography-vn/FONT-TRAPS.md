# Danh mục bẫy chuỗi công cụ font cho tiếng Việt

Mỗi bẫy dưới đây đã được **tái hiện thật** bằng WeasyPrint 69.0 + PyMuPDF (đọc tầng
text) + fontTools (đọc cmap/GSUB) + playwright-core/Chromium (đo pixel), không phải
suy diễn từ tài liệu. Script tái hiện nằm trong phiên nghiên cứu này, có thể chạy lại
theo hướng dẫn ở cuối mỗi mục.

Quy ước mức độ tin cậy: **ĐÃ KIỂM CHỨNG** = đo trực tiếp, có số liệu. **ĐÃ KIỂM, LOẠI
TRỪ** = nghi ngờ hợp lý nhưng đo xong không tái hiện được, ghi lại để khỏi tốn công đo
lại. **CHƯA ĐO SÂU** = có cơ sở lý thuyết nhưng phiên này chưa đủ thời gian đo bằng số.

---

## Bẫy #1: hai khối `@font-face` trùng family/style/weight do tách subset kiểu web (ĐÃ SỬA ở round 3, ghi lại để không tái phạm)

**Triệu chứng**: đọc tầng text PDF ra sai ký tự tại đúng vị trí có dấu tiếng Việt.
`nghệ` → `nght`, `liệu` → `litu`, glyph của `ệ` (U+1EC7) hiển thị/trích xuất thành
glyph của `t`. Không phải tofu, không phải lỗi tên font sai: chữ vẫn "có nghĩa nhìn
như chữ", chỉ sai.

**Cơ chế**: Google Fonts phục vụ font qua mạng bằng NHIỀU khối `@font-face` cùng
`font-family`/`font-style`/`font-weight` nhưng khác `unicode-range` (một khối cho
subset `latin`, một khối cho subset `vietnamese`), để trình duyệt chỉ tải subset cần
dùng. Khi nhúng font bằng base64 thẳng vào một file offline, `unicode-range` không
còn tác dụng tiết kiệm băng thông, nhưng nếu vẫn giữ nguyên cấu trúc "hai khối trùng
tên", **WeasyPrint (Pango/HarfBuzz) không chọn đúng subset theo `unicode-range`** -
tra cmap của subset A vào bảng glyph đã nạp từ subset B, ra lộn glyph. Trình duyệt xử
lý đúng (đây là lý do nghiệm thu bằng mắt trên Chromium mù với lỗi này).

**Cách tái hiện**: sinh CSS có 2 khối `@font-face` cùng tên/style/weight, một khối
base64 subset A, một khối base64 subset B (khác cmap), unicode-range đặt bất kỳ giá
trị nào; `weasyprint.HTML(...).write_pdf(...)` rồi đọc lại bằng `fitz`.

**Cách phát hiện tự động**: đếm số khối `@font-face` cho mỗi tổ hợp
`(font-family, font-style, font-weight)` trong file CSS cuối cùng sẽ nhúng. Số khối
phải luôn bằng 1. Script `extract_fonts.py` trong phiên nghiên cứu này làm đúng việc
đó (parse toàn bộ `@font-face{...}` bằng regex, đếm theo khóa 3 phần, cảnh báo nếu
khóa nào có hơn 1 khối).

**Cách sửa (đã áp dụng, xem `design-system/fonts/build-fonts.py`)**: dùng
`fontTools.subset.Subsetter` gộp union unicode-range của các subset cần giữ thành
MỘT bộ glyph duy nhất, xuất ra ĐÚNG MỘT `@font-face` cho mỗi tổ hợp, bỏ hẳn thuộc
tính `unicode-range`. Đã xác nhận lại trong phiên này: file
`design-system/fonts/fonts-embedded.css` hiện tại có đúng 12 khối `@font-face` cho
12 tổ hợp (family,style,weight), không khối nào trùng.

---

## Bẫy #2: chuẩn hoá Unicode NFD làm dấu nổi lệch vị trí: gốc rễ là khoảng trống trong bảng subset của Google Fonts

**Triệu chứng**: văn bản tiếng Việt ở dạng NFD (chữ cái nền + các dấu kết hợp rời,
thay vì ký tự tổ hợp sẵn NFC) render ra dấu nổi lệch vị trí, trông như dấu "rớt" sang
phải/trên chữ thay vì nằm giữa. Ví dụ đã chụp thật: câu
`"Nghệ thuật ước lượng giá trị hợp lý ở ngưỡng ổn định."` ở dạng NFD render bằng
Spectral 700 nhúng + fallback `serif` (khớp Noto Serif qua `fc-match`) cho ra
`ngưỡng` → mất hẳn hình mũ, còn lại dấu ngã trôi nổi; `ở` → dấu hỏi tách rời thành
một dấu phẩy lửng lơ phía trên bên phải chữ `o` thay vì nằm giữa. Diff pixel đo được:
8.932/396.960 pixel khác nhau (2,25%) trong vùng crop 2 dòng so với bản NFC cùng nội
dung, cùng font, cùng cỡ chữ.

**Cơ chế, đã truy tới tận gốc**:

1. Chuẩn hoá NFD phân rã mỗi ký tự tiếng Việt có dấu thành chữ cái nền + tối đa 2
   dấu kết hợp. Ví dụ `ế` (U+1EBF) → `e` (U+0065) + U+0302 (mũ) + U+0301 (sắc); `ở`
   (U+1EDF) → `o` (U+006F) + U+031B (móc) + U+0309 (hỏi). Đã xác nhận bằng
   `unicodedata.normalize('NFD', ...)` cho 7 chữ mẫu, tất cả đều phân rã đúng 3
   codepoint.
2. Font nhúng của repo (Spectral, IBM Plex Mono, IBM Plex Sans: đọc cmap thật bằng
   fontTools từ chính file `fonts-embedded.css`) phủ **134/134 ký tự tiếng Việt tổ
   hợp sẵn (NFC)**, nhưng **THIẾU đúng 3 mã kết hợp cấu trúc**: U+0302 (mũ), U+0306
   (trăng), U+031B (móc). 5 dấu thanh điệu (huyền/sắc/ngã/hỏi/nặng, U+0300/0301/0303/
   0309/0323) thì CÓ ĐỦ.
3. **Đã truy ngược tới Google Fonts để tìm NGUYÊN NHÂN, không dừng ở "font thiếu"**:
   gọi trực tiếp `https://fonts.googleapis.com/css2?family=Spectral:wght@700` bằng
   UA Chrome thật, đọc `unicode-range` của cả 5 subset Google công bố cho Spectral
   (`cyrillic-ext`, `cyrillic`, `vietnamese`, `latin-ext`, `latin`). **Không subset
   nào trong 5 subset đó liệt kê U+0302, U+0306, hay U+031B**: kể cả `vietnamese`
   (subset tưởng như "đương nhiên phải có đủ dấu Việt") lẫn `latin-ext` (subset đã bị
   `build-fonts.py` loại bỏ có chủ đích để giảm 57% dung lượng). Ba mã này rơi vào
   đúng khoảng trống giữa 5 khai báo subset của Google.
4. Gọi lại API đó bằng UA Firefox 3.6 cũ (không hiểu `unicode-range`, Google trả về
   ĐÚNG MỘT file font gốc chưa tách subset, 878 glyph). Tải file gốc này về, đọc cmap
   bằng fontTools: **font gốc CÓ ĐỦ cả U+0302, U+0306, U+031B**. Kết luận chắc chắn:
   đây không phải giới hạn thiết kế của bản thân chữ Spectral: glyph tồn tại sẵn
   trong font, chỉ là **không được gắn nhãn vào bất kỳ subset nào trong 5 subset
   Google công bố**, nên khi `build-fonts.py` subset lại bằng union unicode-range
   của các subset ĐƯỢC GIỮ (`latin` + `vietnamese`), ba mã này bị loại theo, dù bản
   thân chúng "miễn phí" (đã có sẵn trong font gốc, không cần tải thêm gì).
5. Đã kiểm tra IBM Plex Mono bằng đúng quy trình trên: **hệt Spectral**, cùng 5 dải
   unicode-range cho từng subset, cùng khoảng trống thiếu U+0302/0306/031B ở mọi
   subset. Đây là lỗ hổng **hệ thống trong siêu dữ liệu subset của Google Fonts**,
   không riêng một họ chữ: bất kỳ ai chỉ giữ subset `latin`+`vietnamese` (một tối ưu
   nghe rất hợp lý cho site thuần tiếng Việt) đều dính đúng lỗ hổng này.
6. Font hệ thống dùng làm fallback (Noto Serif, Noto Sans, DejaVu Serif/Sans,
   Liberation Serif/Sans/Mono: đã kiểm cả 6, đọc cmap trực tiếp) **đều có đủ cả 8
   dấu kết hợp**, không riêng 5 dấu thanh điệu. Đây là lý do khi Spectral (nhúng,
   luôn "có mặt" vì là `data:` URI không bao giờ bị coi là "vắng font") không tìm
   thấy glyph cho đúng 1 mã dấu trong một cụm, HarfBuzz/Pango mượn glyph đó từ font
   dự phòng kế tiếp trong danh sách: và **bảng neo GPOS mark-to-base giữa hai font
   khác nhau không khớp nhau**, nên dấu mượn nổi lệch vị trí thay vì đứng đúng chỗ.
7. **Điều kiện để bẫy lộ ra, quan trọng cho việc viết bài kiểm**: bẫy chỉ xuất hiện
   khi font CHÍNH có mặt (không bị thay thế nguyên `font-family`) nhưng THIẾU một số
   mã cụ thể: đúng kịch bản font nhúng base64. Nếu tên font chính không khớp font
   nào đã cài (ví dụ chỉ khai `font-family:"Spectral"` mà không nhúng font thật),
   fontconfig thay THẲNG cả family bằng một font khác đủ dấu (trên máy build của
   phiên này, `fc-match Spectral` trả về Noto Sans: đủ cả 8 dấu), và bẫy **không**
   tái hiện vì toàn bộ cụm được vẽ bằng một font duy nhất có GPOS nhất quán. Do đó
   một phép thử "font-stack không nhúng" sẽ cho kết quả ÂM TÍNH GIẢ: phải test với
   đúng font nhúng thật mới bắt được lỗi.
8. **Hệ quả phụ đã đo, đáng chú ý**: khi bẫy KHÔNG lộ ra (do rơi vào kịch bản #7,
   một font duy nhất đủ dấu render toàn bộ cụm), tầng TEXT của PDF (đọc qua
   `page.get_text()`) có thể bị HarfBuzz **tái tổ hợp NFD → NFC ngay trong lúc
   shaping**, trước khi ghi `ToUnicode` CMap: đối chiếu multiset ký tự xác nhận mỗi
   cụm [chữ nền + dấu rời] trong nguồn ánh xạ đúng 1-1 sang đúng 1 ký tự tổ hợp sẵn
   trong PDF, không mất, không sinh ký tự lạ. Ngược lại, khi bẫy CÓ lộ ra (kịch bản
   cross-font thật, xem thí nghiệm gốc trong mục Đo được bên dưới), tầng text GIỮ
   NGUYÊN chuỗi NFD 76 codepoint, không tái tổ hợp. Tức là: **hành vi của tầng text
   PDF với cùng một input NFD không cố định: nó phụ thuộc có bao nhiêu font tham
   gia vẽ cụm ký tự đó**. Không nên viết code coi "PDF luôn giữ nguyên NFD gốc" hay
   "PDF luôn tự sửa về NFC" là bất biến; phải chuẩn hoá NFC ở đầu vào, không dựa vào
   hành vi ngầm định của renderer.

**Cách tái hiện đầy đủ** (script `nfc_nfd_test.py`, `cmap_coverage.py` trong phiên
nghiên cứu):
```python
import unicodedata as ud, weasyprint, fitz
s = "Nghệ thuật ước lượng giá trị hợp lý ở ngưỡng ổn định."
s_nfd = ud.normalize("NFD", s)   # 76 codepoint, so voi 53 cua ban NFC
# nhung ca hai vao HTML dung DUNG font Spectral 700 base64 that (khong dung generic fallback)
# render bang weasyprint, doc lai bang fitz, so sanh pixel + text layer
```

**Cách phát hiện tự động** (chèn ở bước nạp dữ liệu, KHÔNG ở bước render):
```python
import unicodedata as ud
assert text == ud.normalize("NFC", text), "van ban dau vao khong o dang NFC"
```

**Cách sửa, xếp theo chi phí**:
1. **Rẻ nhất, khuyến nghị**: chuẩn hoá `unicodedata.normalize('NFC', text)` tại điểm
   nạp dữ liệu (đọc file, nhận input, gọi API): chặn triệt để vì NFC hoá rồi thì
   không còn combining mark rời nào để thiếu glyph.
2. **Sửa tại nguồn font (bền hơn, nên làm song song)**: sửa `build-fonts.py` để khi
   gọi `Subsetter.populate(unicodes=...)`, hợp thêm tường minh khối
   `U+0300-0323` (Combining Diacritical Marks liên quan tiếng Việt) vào tập unicode
   cần giữ, KHÔNG chỉ dựa vào unicode-range mà Google gắn nhãn cho từng subset: vì
   đã chứng minh nhãn đó có khoảng trống. Chi phí gần như bằng 0 (glyph đã có sẵn
   trong font gốc, không cần tải thêm).
3. Nếu vẫn muốn dựa hoàn toàn vào nhãn subset của Google: giữ thêm subset
   `latin-ext`: nhưng đã chứng minh Ở MỤC 3 rằng `latin-ext` của Spectral CŨNG
   không liệt kê 3 mã này, nên cách này KHÔNG giải quyết được vấn đề, chỉ tốn thêm
   dung lượng vô ích. Đừng chọn hướng này.

---

## Bẫy khả nghi #3: `font-variant-ligatures`: ĐÃ KIỂM, LOẠI TRỪ cho bộ font hiện tại

**Giả thuyết ban đầu**: ligature `fi`/`fl` (dùng khi tiếng Việt chen từ vay mượn
tiếng Anh, ví dụ "profile") có thể tạo glyph ghép chèn sai vị trí dấu ở chữ liền kề,
hoặc làm hỏng `ToUnicode` CMap khi trích xuất text.

**Đã đo**: câu `"Hồ sơ tài chính và profile rủi ro của doanh nghiệp được cải
thiện."` render bằng Spectral 400 nhúng, so `font-variant-ligatures: common-ligatures`
(mặc định) với `none`. Kết quả: **0,006% pixel khác nhau** (nhiễu anti-alias, không
phải khác biệt thật), và tầng text trích xuất khớp input tuyệt đối ở CẢ HAI trường
hợp.

**Vì sao không tái hiện được, đã truy tới gốc**: Spectral có bảng GSUB với feature
`liga` (xác nhận bằng `fontTools`, liệt kê `FeatureList` của font nhúng), nhưng khi
liệt kê TOÀN BỘ tên glyph trong font (430 glyph), **không có glyph nào tên
`f_i`/`f_l`** kiểu ligature chuẩn: vì `fontTools.subset` khi cắt font cho repo này
đã loại các glyph ligature (không nằm trong closure trực tiếp của tập unicode cần
giữ theo cách subsetter xử lý ligature không bắt buộc). Tức là: `liga` bật/tắt không
có tác dụng thực với đúng bộ font đã subset của repo, không phải vì "an toàn theo
thiết kế" mà vì ligature đã bị cắt khỏi subset từ trước. Nếu sau này đổi cách gọi
`fontTools.subset` để CÓ giữ ligature (ví dụ vì cần ligature `ct`/`st` trang trí của
Spectral ở nơi khác), phải đo lại: kết luận "không tái hiện" ở đây gắn với bộ font
ĐANG CÓ, không phải kết luận vĩnh viễn về Spectral nói chung.

**Cách đo lại khi cần**:
```python
from fontTools.ttLib import TTFont
f = TTFont("fonts-embedded-font.woff2")
ligs = [g for g in f.getGlyphOrder() if "_" in g or "fi" in g.lower() or "fl" in g.lower()]
```

---

## Bẫy khả nghi #4: `text-transform: uppercase` có làm hỏng dấu tiếng Việt không: ĐÃ KIỂM, LOẠI TRỪ

**Giả thuyết**: hoa hoá bằng CSS (`text-transform: uppercase`) là phép biến đổi ở
tầng render, có thể không map đúng chữ thường có dấu sang chữ hoa có dấu tương ứng
(ví dụ `ợ` → phải ra `Ợ`, không phải `O` trần hay giữ nguyên `ợ`), hoặc tầng text PDF
trích ra chữ THƯỜNG dù mắt thấy chữ HOA (vì transform chỉ đổi glyph hiển thị, không
đổi "text gốc").

**Đã đo**: trang `samples/typo-chu-hoa-toan-phan.html` dùng
`text-transform: uppercase` trên đoạn `"Trượt giá trị điều chỉnh"` (nguồn HTML viết
chữ thường). Round-trip WeasyPrint + PyMuPDF: multiset ký tự (đã casefold) giữa
nguồn và tầng text PDF khớp tuyệt đối 1118/1118: nghĩa là **tầng text PDF phản ánh
đúng dạng ĐÃ HOA HOÁ** (không phải giữ nguyên chữ thường gốc), và mọi ký tự có dấu
đều hoa hoá đúng cặp (`ợ`→`Ợ`, `ị`→`Ị`...), không rơi rớt dấu nào.

**Kết luận**: với WeasyPrint + font hiện dùng, `text-transform: uppercase` an toàn
cho tiếng Việt cả về hình lẫn về tầng text. Lưu ý điều này gắn với ENGINE (WeasyPrint/
Pango) đang dùng: một số renderer khác (ví dụ vài phiên bản wkhtmltopdf cũ) từng có
tiếng là xử lý uppercase transform theo bảng ASCII, bỏ qua ký tự ngoài Latin cơ bản;
không suy diễn kết luận này sang engine khác chưa đo.

---

## Hướng chưa đo sâu trong phiên này (đề xuất cho vòng sau)

- **Hinting/rendering khác nhau giữa engine in (WeasyPrint, không hint theo pixel vì
  xuất vector) và engine màn hình (Chromium, hint theo DPI thiết bị)**: có cơ sở lý
  thuyết vững (hai pipeline hoàn toàn khác nhau: WeasyPrint qua Pango/Cairo xuất
  glyph outline thẳng vào PDF, Chromium/Skia rasterize có hint theo subpixel), nhưng
  phiên này chưa đo bằng số cụ thể mức lệch hình học giữa hai đường xuất cho cùng một
  cụm dấu tiếng Việt. Cách đo đề xuất: xuất cùng một trang ra PDF bằng WeasyPrint VÀ
  bằng Chromium `page.pdf()`, render cả hai về PNG cùng DPI bằng PyMuPDF, so
  bounding-box mực của cùng ký tự.
- **`text-rendering: optimizeLegibility`**: về bản chất chỉ bật kerning + ligature
  (đã đo riêng cả hai ở trên), nhưng chưa đo trường hợp nó tương tác với
  `font-feature-settings` tùy chỉnh khác trong `components/`.
- **Font Latin Extended Additional coverage cho các họ chữ KHÁC** ngoài Spectral/IBM
  Plex đang dùng trong repo (ví dụ nếu tương lai đổi sang một serif hiển thị khác cho
  minh hoạ/illustration): quy trình kiểm đã có sẵn (`cmap_coverage.py`), chỉ cần
  chạy lại trên font mới.
