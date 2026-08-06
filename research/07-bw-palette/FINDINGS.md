# Bảng màu cho biểu đồ nhiều chuỗi: an toàn in đen trắng và mù màu

Vòng 2, mũi nghiên cứu riêng cho bài toán màu. Đã đọc `research/03-chart-doctrine/FINDINGS.md`
mục 7 trước khi viết tài liệu này (vòng 1 đã đặt đúng hướng: dùng độ sáng thay vì chỉ hue, dùng
hoạ tiết làm mã hoá kép, và đã phát hiện `accent`/`negative` gần trùng xám). Tài liệu này đào sâu
hơn: đo chính xác bao nhiêu, sinh thêm màu theo quy tắc nào, và ngưỡng số chuỗi nào thì màu hết
tác dụng.

**Công cụ**: toàn bộ phép đo trong tài liệu này chạy bằng một bộ công thức tự viết
(`colormath.py`, không dùng thư viện màu chuyên dụng) gồm: WCAG 2.x relative luminance, tỷ số
tương phản, công thức xám của CSS Filter Effects Level 1, CIE 1976 Lab/LCH, delta-E76, và mô
phỏng mù màu theo ma trận Machado/Oliveira/Fernandes 2009 (severity 1.0, áp trên linear RGB).
Đã tự kiểm từng công thức bằng dữ liệu biết trước (trắng/đen bất biến, tương phản trắng/đen ra
đúng 21.0, đỏ/lục thật sự sụp gần nhau dưới deuteranopia trong khi xanh dương/cam vẫn tách xa)
trước khi dùng để ra khuyến nghị. Toàn bộ script nằm ở
`/tmp/claude-1000/-home-hgthinhng/aa9d41ed-d682-4f03-95aa-1c545671303a/scratchpad/` (colormath.py,
derive.py, derive2.py) vì phạm vi ghi của phiên này giới hạn ở `research/` và `samples/`.

## 0. Hai bẫy render phải biết trước khi tin bất kỳ mẫu nào trong repo

Trước khi có được số liệu đáng tin, phải sửa 2 lỗi phát hiện được ngay trên chính mẫu đầu tiên
đang viết (và xác nhận chúng có ở ít nhất 8 file khác trong `samples/` từ vòng 1):

**Bẫy 1: `<svg width="100%" height="auto">` bị WeasyPrint 69.0 bỏ qua hoàn toàn.** Tự kiểm bằng
`weasyprint.HTML(...).write_pdf()` rồi `fitz` chụp lại trang: SVG với `width="100%"` (dù đặt trực
tiếp trên `<svg>` hay qua CSS `style="width:100%"`) render ra Ô TRỐNG trong PDF, không lỗi không
cảnh báo. Trình duyệt (Chromium) render đúng, nên lỗi này CHỈ lộ ra khi kiểm PDF thật, đúng kịch
bản rủi ro nêu trong yêu cầu nghiên cứu. Test tối thiểu tái lập: một `<svg viewBox="0 0 100 100"
width="100%">` cùng file với một `<svg width="200">` cố định, cùng file, chỉ cái thứ hai render.
Cách sửa an toàn: `<svg>` phải có `width`/`height` là SỐ PX CỐ ĐỊNH khớp `viewBox`; muốn co giãn
theo màn hình thì đặt CSS `svg { max-width: 100%; height: auto; }` trên chính `<svg>` (không đặt
`width="100%"` làm thuộc tính của `<svg>`). Grep nhanh `width="100%" height="auto"` trong
`samples/*.html` ra ít nhất 8 file khác từ vòng 1 (toàn bộ nhóm `chart-*.html` của
`research/03-chart-doctrine`) cùng dùng đúng pattern lỗi này -- khả năng cao các mẫu đó cũng render
rỗng khi ra PDF dù trông hoàn hảo trên trình duyệt, cần một lượt kiểm lại riêng (xem mục "Đề xuất
cho vòng sau"). Đây CHÍNH XÁC là loại lỗi mà nhiệm vụ nghiên cứu này đã cảnh báo trước: "đã có mẫu
của agent khác trông hoàn hảo trên trình duyệt nhưng vỡ nát khi ra PDF thật."

**Bẫy 2: `filter: grayscale(1)` không được WeasyPrint 69.0 thực thi.** Đây là kỹ thuật chính mẫu
`chart-mau-den-trang.html` (vòng 1) dùng để "chứng minh bằng thực nghiệm" chart vẫn đọc được sau
khi khử màu. Tự kiểm bằng cách xuất PDF rồi đọc lại giá trị pixel bằng PyMuPDF
(`page.get_pixmap()` rồi `Image.getpixel()`): panel được cho là "đã khử màu" có pixel Y HỆT panel
màu gốc (ví dụ một mảng accent-hi vẫn ra đúng RGB(17,51,184), không phải một sắc xám). Nghĩa là
kỹ thuật này chỉ đúng khi xem bằng trình duyệt (HTML/màn hình), không đúng cho chính pipeline in
PDF mà repo cam kết ("HTML self-contained VÀ PDF in được"). Vì bài kiểm bắt buộc của nhiệm vụ chỉ
yêu cầu so khớp CHỮ (text round-trip qua `fitz.get_text()`), lỗi loại này không bị bài kiểm đó bắt
được -- chữ vẫn khớp dù hình sai hoàn toàn. Cách sửa: không dựa vào CSS filter cho bất kỳ tuyên bố
thị giác nào cần đúng ở PDF; gán THẲNG giá trị xám đã tính trước (bằng đúng công thức CSS Filter
Effects, xem mục 1) làm `fill` của phiên bản "đã khử màu", độc lập với runtime filter của bất kỳ
renderer nào. Bốn mẫu HTML trong tài liệu này (trừ mẫu B) đều dùng cách sửa này, có thể kiểm lại
bằng `PIL.Image.getpixel()` sau khi xuất PDF: các trang kiểm ra `R == G == B` chính xác tại mọi
điểm dữ liệu.

**Bẫy 3 (nhỏ hơn, phát hiện khi dựng mẫu 3): CSS Grid mặc định kéo giãn (`justify-self: stretch`)
áp cả lên `<svg>` có aspect ratio nội tại.** Một `<svg width="170" height="320">` đặt làm item
trực tiếp của một `.grid` 2 cột sẽ bị kéo giãn theo chiều rộng cột rồi tính lại chiều cao theo tỉ
lệ, biến 170x320 thành ví dụ 300x564 và đè lên nội dung phía dưới. Đây không phải lỗi riêng của
WeasyPrint (đúng theo spec CSS Box Alignment, trình duyệt thật cũng làm vậy), nhưng dễ bị bỏ sót
vì nhìn ảnh chụp màn hình nhỏ không thấy ngay chỗ tràn. Sửa bằng `justify-self: start` trên chính
`<svg>` khi nó là item của `display:grid`.

## 1. Ngưỡng phân biệt khi chuyển sang thang xám

**Số đo**: dùng công thức CSS Filter Effects (`gray = 0.2126R + 0.7152G + 0.0722B` áp trực tiếp
lên giá trị sRGB đã nén gamma, KHÔNG tuyến tính hoá trước -- đây là công thức Chromium/Firefox
thực sự dùng khi render `filter: grayscale(1)`, và cũng là công thức gần với cách máy in/photocopy
thông thường quy đổi sang thang xám vì chúng cũng không tuyến tính hoá trước khi lấy độ chói).

Tự kiểm công thức khớp browser thật: dựng trang chứa 12 màu token gốc, áp `filter: grayscale(1)`
thật, chụp bằng `playwright-core` + Chromium (`~/.cache/ms-playwright/chromium-1228/`), đọc lại
pixel bằng PIL. Sai số lớn nhất giữa công thức và pixel Chromium render thật: **0.49/255** (thuần
làm tròn). Công thức dùng trong toàn bộ tài liệu này đã được xác nhận đúng bằng render thật, không
phải suy luận từ spec.

**Ngưỡng thực dụng** (đo bằng cách render 7 cặp màu ở các mức ΔGrayCSS mục tiêu 3/6/11/15/20/27/38,
mỗi cặp ở 2 cỡ mảng: mảng lớn 60x44px mô phỏng thanh/cột, và nét mảnh 3px mô phỏng đường line
chart, tự quan sát qua ảnh chụp Chromium thật trước khi chốt số -- xem mẫu
`samples/palette-nguong-phan-biet.html`):

| ΔGrayCSS (0-255) | Mảng lớn (thanh, cột, vùng tô) | Nét mảnh (đường, viền) |
|---|---|---|
| dưới 10 | Không phân biệt được | Không phân biệt được |
| 10-15 | Mờ nhạt, bắt đầu thấy | Vẫn khó |
| 15-20 | Rõ | Thấy được nhưng phải nhìn kỹ |
| từ 20 trở lên | Rõ | Rõ |

**Khuyến nghị số**: ΔGrayCSS từ 15 trở lên cho mảng lớn, ΔGrayCSS từ 20 trở lên cho nét mảnh. Dưới
10 luôn thất bại. Đối chiếu với chuẩn bản đồ học độc lập (Mendeley Data, "Calculation of the
CIELAB color coordinates and differences for map color legends": ΔE*ab từ 10 trở lên đảm bảo phân
biệt được, ΔE*ab từ 3.5 trở lên là "khác biệt rõ ràng" cho ứng dụng nhạy hơn) -- hai không gian đo
khác nhau (GrayCSS dùng sRGB gamma trực tiếp, ΔE dùng Lab đã tuyến tính hoá) nên không quy đổi
tuyến tính được, nhưng cả hai độc lập xác nhận: ngưỡng an toàn nằm ở mức 2 chữ số, không phải 1
chữ số.

## 2. Thứ tự dẫn xuất khi cần sinh thêm màu

So sánh 3 cách dẫn xuất 6 màu từ `accent` (#2251FF), đo bằng số thay vì chọn bằng mắt (script
`derive.py`, mẫu `samples/palette-dan-xuat-quy-tac.html`):

| Cách | Mô tả | ΔGrayCSS liền kề nhỏ nhất | Nhận xét |
|---|---|---|---|
| A | Tint: trộn tuyến tính với `paper` trong sRGB | 34 (đều) | An toàn xám tuyệt đối, chỉ 1 hue. Hợp dữ liệu CÓ THỨ TỰ. Không hợp định danh (không có tên riêng để nhớ). |
| B | Xoay hue, GIỮ NGUYÊN L* và C* | 0 | SAI cho in ấn: 2 màu xanh dương-ngọc khác hẳn nhau về hue lại đổ về đúng 1 ô xám. |
| D | Tham lam (greedy) trong CIE LCH, tối đa hoá đồng thời ΔGrayCSS và ΔE mù màu tệ nhất | 30 | Có nhiều hue thật (hợp định danh) mà vẫn an toàn in ấn và mù màu. |

Cách B là lỗi phổ biến nhất khi ai đó "thêm màu bằng cách xoay bánh xe màu" trực giác mà không
kiểm lại độ sáng -- vì mắt và máy in phân biệt màu chủ yếu qua ĐỘ SÁNG khi mất sắc độ (đúng như
vòng 1 đã trích Datawrapper: "get it right in black & white"), giữ nguyên L* nghĩa là giữ gần
nguyên độ xám bất kể xoay hue bao xa.

**Quy tắc dẫn xuất chính thức dùng cho PALETTE-TABLE.md (cách D)**: quét lưới ứng viên trong CIE
LCH, giới hạn hue trong CUNG AN TOÀN (loại bỏ hue của `pos`/`neg`/`warn` VÀ vùng lân cận theo TÊN
màu cảm nhận -- loại cả dải đỏ 330-50 độ, cam/vàng 50-95 độ, xanh lá/ngọc 95-190 độ, vì độc giả báo
cáo tài chính gán nghĩa "xanh lá = tốt, đỏ/cam = xấu/cảnh báo" theo TÊN màu chứ không theo góc hue
chính xác -- loại rộng hơn góc hue thật của 3 token đó). Chọn từng màu mới theo thuật toán tham lam
(greedy farthest-point): mỗi bước chọn ứng viên tối đa hoá `min(ΔGrayCSS, 1.3 x ΔE-mù-màu-tệ-nhất)`
so với mọi màu đã chọn. Bắt đầu từ chính `accent` (hoặc bộ 5 token có sẵn, xem mục 3) để bảng màu
mới vẫn nhận ra được là cùng hệ.

**Đánh đổi hue hẹp và hue rộng**: cung hẹp (60-80 độ) giữ màu trong họ xanh dương-tím sát với
`accent`, nhưng ép ΔGrayCSS tối thiểu ở N=8 xuống 15.8-21.2. Cung rộng hơn (140 độ, kéo dài tới gần
vùng hồng-magenta) cho số tốt hơn (ΔGrayCSS=22.4 ở N=8) nhưng bắt đầu trôi khỏi cảm giác "cùng hệ
navy/xanh dương" của repo. Khuyến nghị: ưu tiên tái dùng token có sẵn trước (mục 3), chỉ mở rộng
hue mới khi thật cần, đúng tinh thần "bảng hẹp là chủ ý" của repo.

## 3. Tái dùng 12 token có sẵn: tới đâu thì đủ, tới đâu thì vỡ

Trước khi sinh màu mới, đã brute-force toàn bộ tổ hợp con của 12 token trong `tokens.css` (loại
`paper`/`paper-hi` vì quá sáng để làm data-ink) để tìm tập con N=4/6/8 tốt nhất, đo bằng
`min(ΔGrayCSS, ΔE-mù-màu)` trên MỌI cặp (không chỉ cặp liền kề, vì thứ tự trong chú giải có thể
đảo):

| N | Tập tốt nhất (không đụng valence) | min ΔGrayCSS | Ghi chú |
|---|---|---|---|
| 4 | ink, ink-md, accent-soft, line | 58.9 | An toàn tuyệt đối, nhưng 1 hue (đơn sắc) |
| 5 | ink, accent-hi, accent, ink-lo, line | 29.3 | Vẫn 1 hue chính, an toàn |
| 6 | (không có tập nào an toàn) | 9.0 | VỠ: ink-md/accent-hi chỉ cách nhau 9.0 |
| 7 | (không có tập nào an toàn) | 0.4 | Vỡ hoàn toàn |

**Phát hiện cụ thể**: `ink-md` (#42566A) và `accent` (#2251FF) chỉ cách nhau 0.4 đơn vị GrayCSS
(83.2 so với 83.6 trên thang 0-255) -- gần như trùng tuyệt đối, dù 2 màu trông khác hẳn trên màn
hình (xám-xanh vs xanh dương điện). `ink-md` và `accent-hi` cách nhau 9.0. Đây là 2 cái bẫy ẩn cụ
thể: nếu ai đó ghép `ink-md` vào cùng 1 chart với `accent` hoặc `accent-hi` để làm 2 chuỗi khác
nhau, bản in đen trắng sẽ không phân biệt được, dù không ai nhận ra khi nhìn bản màu trên màn hình.

Nếu chấp nhận mượn tạm `pos`/`neg`/`warn` (rủi ro: đọc giả có thể hiểu nhầm valence), tập tốt nhất
ở N=6 là ink, accent-hi, neg, warn, accent-soft, line (min ΔGrayCSS=26.9) -- nhưng mượn CẢ `neg`
VÀ `warn` cùng lúc, rủi ro cao nếu trang có chart valence khác gần đó.

**Kết luận cho bộ khung dùng chính thức**: bắt đầu từ 5 token an toàn (ink, accent-hi, accent,
ink-lo, line), rồi mở rộng bằng thuật toán tham lam (mục 2) từng màu một. Đo được: thêm màu thứ 6
và thứ 7 theo cách này KHÔNG làm giảm ΔGrayCSS tối thiểu (vẫn giữ 29.3, y hệt N=5) -- chỉ tới màu
thứ 8 mới bắt đầu giảm xuống 18.7. Đây là bằng chứng số cho khuyến nghị ở PALETTE-TABLE.md: 4/6/7
chuỗi an toàn không cần thoả hiệp, 8 chuỗi cần mã hoá kép bổ sung.

## 4. Khi nào ĐỪNG dùng màu để phân biệt

Kéo dài thuật toán tham lam ở mục 2 tới N=12 để đo XU HƯỚNG suy giảm (script `derive2.py`):

| N | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|
| min ΔGrayCSS toàn bảng | 18.7 | 17.3 | 16.1 | 15.4 | 15.0 |
| min ΔE mù màu tệ nhất | 14.4 | 13.2 | 13.2 | 13.2 | 11.8 |

**Phát hiện quan trọng nhất của mục này**: về THUẦN SỐ, ngay cả ở N=12, thuật toán tham lam vẫn
giữ ΔGrayCSS trên ngưỡng tối thiểu 10 (chuẩn bản đồ học). Nghĩa là qua được ngưỡng số không có
nghĩa là dùng được trong thực tế -- đây là giới hạn thật của việc đo bằng ΔE/ΔGray từng cặp: phép
đo không nắm được việc não người phân loại màu theo HỌ MÀU (gestalt), không theo từng cặp riêng
lẻ. 4 màu sinh thêm ở N=9-12 (#0C5170, #2D6F8D, #2F8FFF, #84A9D2) đều đo được là khác nhau nhưng
đều là các sắc "xanh dương-xanh lam-xám" không có tên gọi riêng trong trí nhớ người đọc -- xem
minh hoạ thị giác ở `samples/palette-khong-dung-mau.html`.

Cộng thêm gánh nặng nhận thức của legend nhiều mục: Munzner (Visualization Analysis and Design)
khuyến nghị 6-12 màu categorical là khả thi về mặt tri giác thuần tuý, nhưng thực dụng 7-9 trước
khi hiệu quả legend giảm, 8 là ngưỡng hay được dẫn trong tài liệu ngành.

**Ngưỡng kết luận** (kết hợp cả 2 nguồn bằng chứng, số đo và nhận thức):

- Từ 6 chuỗi trở lên: luôn thử phương án không dùng màu song song với phương án màu (nhãn trực
  tiếp, tô đậm 1-2 chuỗi trọng tâm), đừng mặc định màu là kênh chính.
- Từ 8 trở lên: nếu vẫn dùng màu, bắt buộc mã hoá thứ 2 (hoạ tiết, nét đứt, nhãn trực tiếp) cho
  MỌI cặp có ΔGrayCSS dưới 20.
- Từ 10 trở lên: ưu tiên chuyển hẳn sang small multiples hoặc highlight-and-mute (tô đậm 1-2 chuỗi
  trọng tâm, phần còn lại dùng chung 1 màu trung tính), không cố nhồi thêm màu vào cùng một cung
  hue -- lúc này vấn đề không còn là toán học mà là con người không gán được TÊN cho từng màu
  trong trí nhớ.

**Khi nào 12 màu vẫn ổn**: khi các hạng mục đã có trật tự KHÔNG GIAN cố định trên chính hình (bản
đồ hành chính, lưới toạ độ) -- người đọc tra cứu bằng vị trí, màu chỉ là gia vị phụ chứ không phải
kênh mã hoá chính, nên ngưỡng phân biệt yêu cầu thấp hơn nhiều so với một dải màu tuyến tính/pie
chart nơi màu LÀ kênh chính.

## 5. Hoạ tiết và nét đứt: giải pháp cổ điển, dùng tiết chế

Ràng buộc cứng của repo cấm `<linearGradient>`/`<radialGradient>`/`<filter>`/`<clipPath>` lồng
nhau trong SVG (chúng bị raster hoá khi in) -- nhưng KHÔNG cấm `<pattern>`, nên hoạ tiết vẫn làm
được thuần vector. Đã dùng 2 dạng trong các mẫu: gạch chéo 45 độ (`<pattern>` chứa `<rect>` +
`<line>`) và chấm bi (`<pattern>` chứa `<rect>` + `<circle>`) -- cả hai đều là hình học thuần,
không gradient, không raster.

**Dùng tiết chế**: chỉ gắn hoạ tiết cho cặp có ΔGrayCSS dưới ngưỡng an toàn (dưới 20, xem mục 1),
không gắn tràn lan cho mọi chuỗi -- gắn hết sẽ phá vỡ tính sạch của trang (đúng lo ngại nêu trong
yêu cầu nghiên cứu) và làm mất tác dụng phân biệt của chính hoạ tiết (nếu 8/8 chuỗi đều có hoạ
tiết khác nhau, hoạ tiết trở thành kênh chính thay vì kênh dự phòng, và người đọc phải học 8 hoạ
tiết thay vì 8 màu -- không tiết kiệm được gánh nặng nhận thức nào). Trong mẫu 8 màu chính thức
(`palette-8-chuoi.html`), chỉ 2/8 chuỗi (cặp yếu nhất, ΔGrayCSS=18.7) có hoạ tiết; 6 chuỗi còn lại
dùng màu phẳng.

**Nét đứt cho đường line chart**: chưa dựng mẫu riêng (đường line 8 chuỗi có vấn đề khác -- xem
mục 7), nhưng nguyên lý giống hệt: chỉ gắn nét đứt cho cặp đường có ΔGrayCSS thấp, và ưu tiên độ
dài nét đứt khác nhau rõ rệt (không chỉ 2 mức liền-đứt mà 3 mức liền/đứt-thưa/đứt-dày) để còn phân
biệt được khi 2 đường đó CẮT NHAU trên biểu đồ (điểm cắt làm mất tác dụng của chênh lệch màu tại
đúng chỗ người đọc cần phân biệt nhất).

## 6. Mù màu: đo bằng mô phỏng thật, không chỉ khẳng định "an toàn"

Áp ma trận Machado/Oliveira/Fernandes 2009 (severity 1.0, tính trên linear RGB) cho cả 3 dạng phổ
biến. Đã tự kiểm ma trận bằng 2 phép thử đối chứng đã biết trước kết quả:

- Đỏ thuần (#FF0000) và lục thuần (#00CC00): ΔE76 bình thường = 154.1, sụp còn 10.2 dưới
  deuteranopia (mất gần hết khả năng phân biệt, đúng hiện tượng y học đã biết về cặp đỏ-lục).
- Xanh dương (#2251FF) và cam (#FF8800): ΔE76 bình thường = 166.6, vẫn giữ 147.8-168.2 dưới cả
  protanopia và deuteranopia (cặp "an toàn mù màu" kinh điển, đúng như tài liệu vòng 1 đã trích).

Áp lên bảng 8 màu chính thức (đầy đủ ở PALETTE-TABLE.md): cặp yếu nhất dưới mô phỏng vẫn là
accent-sky/accent-cyan (ΔE giảm còn 14.4 dưới deuteranopia) -- TRÙNG với cặp yếu nhất về ΔGrayCSS
(18.7). Đây không phải trùng hợp: cả 2 phép đo đều nhạy với việc 2 màu này quá gần nhau về độ sáng
VÀ cùng nằm trong 1 dải hue hẹp (xanh dương nhạt-lục lam), nên hoạ tiết gắn cho cặp này (đã làm ở
mục 5) giải quyết đúng cả 2 rủi ro cùng lúc, không phải bù ngẫu nhiên.

**Bảng lõi hiện tại** (ink, accent, accent-hi, accent-soft, warn, pos, neg) chịu được tới đâu:
cặp neg/pos (dùng cho valence tăng giảm) giữ ΔE76 bình thường = 98.8, nhưng sụp còn 18.7-21.1 dưới
protanopia/deuteranopia -- vẫn trên ngưỡng 10 nhưng không còn dư dả nhiều như nhìn bằng mắt thường
tưởng. Đây là lý do không nên đặt `neg` và `pos` cạnh nhau làm 2 vùng liền kề lớn khi có thể; nếu
bắt buộc, nên có mã hoá hướng bổ sung (mũi tên, dấu +/-) chứ không chỉ dựa màu.

## 7. Thứ tự gán màu

**Quy tắc rút ra** (áp dụng trong cả 2 mẫu 8 màu): sắp N màu theo GrayCSS TĂNG DẦN một lần duy
nhất, rồi gán cho các hạng mục theo đúng thứ tự ưu tiên của bài toán -- không phải theo thứ tự
bảng chữ cái hay ngẫu nhiên. Hai lý do bằng số:

1. Hai đầu mút của thang GrayCSS luôn có khoảng cách LỚN NHẤT có thể trong toàn bộ tập màu (ví dụ
   200.8 giữa ink và line trong bảng 8 màu) -- nên cặp quan trọng nhất khi so sánh nhanh (hạng mục
   lớn nhất/nổi bật nhất so với phần còn lại, hoặc "chủ thể báo cáo" so với các đối chiếu) nên
   luôn nhận 1 trong 2 màu đầu mút, không cần chọn tay mỗi lần.
2. Nếu bài toán có 1 "chủ thể" cố định (ví dụ công ty đang được phân tích, xuất hiện lặp lại ở
   nhiều exhibit trong cùng báo cáo) mà KHÔNG nhất thiết đứng đầu bảng xếp hạng, vẫn nên ưu tiên
   gán màu đậm nhất hệ (ink) cho đúng chủ thể đó thay vì theo thứ hạng -- vì vai trò của màu ở đây
   là "chủ thể dễ tìm nhất", không phải "xếp hạng dễ đọc nhất" (thứ hạng đã có sẵn qua vị trí/độ
   dài thanh và số ghi trực tiếp, không cần màu đảm nhiệm việc đó nữa).

## 8. Danh sách nguồn

- WCAG 2.x, relative luminance và tỷ số tương phản (Web Content Accessibility Guidelines)
- CSS Filter Effects Module Level 1 (W3C), công thức grayscale()
- CIE 1976 (L*, a*, b*) color space
- Machado, G.M., Oliveira, M.M., Fernandes, L.A.F. (2009), "A Physiologically-based Model for
  Simulation of Color Vision Deficiency", IEEE Transactions on Visualization and Computer
  Graphics 15(6)
- Mendeley Data, "Calculation of the CIELAB color coordinates and differences for map color
  legends" -- ngưỡng ΔE*ab từ 10 trở lên cho phân biệt bản đồ học
- Munzner, T., Visualization Analysis and Design -- khuyến nghị số màu categorical
- research/03-chart-doctrine/FINDINGS.md mục 7 (vòng 1, điểm khởi đầu của mũi nghiên cứu này)
- design-system/tokens.css (giá trị 12 token màu gốc của repo)

## 9. Đề xuất vùng cho vòng sau

- Ưu tiên cao: kiểm lại toàn bộ 8 mẫu chart của vòng 1 (chart-*.html trong samples/, thuộc
  research/03-chart-doctrine) bằng đúng phép weasyprint + fitz.get_pixmap() (không chỉ
  get_text()) đã dùng ở đây -- khả năng cao chúng render RỖNG vì cùng dùng
  width="100%" height="auto" trên svg. Đây là rủi ro cao nhất tìm được trong toàn bộ phiên làm
  việc, ảnh hưởng ngoài phạm vi mũi nghiên cứu màu.
- Đường line chart nhiều chuỗi (khác cột/mảng): ΔGrayCSS ngưỡng nét mảnh (mục 1) chưa được kiểm
  tại điểm 2 đường CẮT NHAU -- đây là tình huống thực tế hay gặp nhất và khó nhất cho phân biệt
  màu trên đường, chưa có mẫu render riêng.
- CIEDE2000 (ΔE00) chưa được cài đặt, tài liệu này chỉ dùng ΔE76 (Euclidean thuần trong Lab) vì
  đơn giản và minh bạch hơn, nhưng ΔE76 được biết là không đều trong vùng xanh dương (có thể phóng
  đại chênh lệch thật ở vùng hue này) -- nếu vòng sau cần độ chính xác cao hơn cho vùng hue khác
  (đỏ, vàng), nên cài CIEDE2000.
