# Typography tiếng Việt: dấu chồng ở cỡ chữ lớn, kerning tiêu đề, độ trung thực khi in

Vòng 2. Vùng: dấu chồng cỡ chữ lớn, kerning/tracking tiêu đề, chữ hoa toàn phần,
danh mục bẫy font, và độ phủ font cho tiếng Việt. Bẫy font tách riêng vào
`FONT-TRAPS.md` (tài liệu giá trị nhất của phiên này). File này gom các phép đo
tạo hình (headroom, va chạm, tracking) và độ phủ ký tự.

Công cụ dùng thật, không suy đoán: `weasyprint` 69.0 + `pymupdf` (round-trip text
layer), `fontTools` (đọc cmap/GSUB thật từ chính font nhúng của repo, trích ra từ
`design-system/fonts/fonts-embedded.css`), `playwright-core` + Chromium
(`~/.cache/ms-playwright/chromium-1228`, `deviceScaleFactor: 2`) để chụp pixel thật
rồi quét bằng `numpy`/`PIL`. Mọi phép đo dùng font Spectral 700 (font tiêu đề chốt
của repo) trừ khi ghi chú khác. Script gốc lưu trong scratchpad phiên làm việc, mọi
số liệu dưới đây có thể chạy lại bằng đúng quy trình mô tả ở từng mục.

**Nguyên tắc đo, đọc trước khi dùng lại các con số này**: mọi headroom/khoảng cách
đo bằng cách render ra ảnh rồi QUÉT PIXEL tìm hàng/cột đầu tiên có mực (ngưỡng xám
< 250/255), KHÔNG so `getBoundingClientRect()` với `fontSize × lineHeight` - phép so
đó là tautology, không bao giờ phát hiện được gì vì cả hai vế đều suy từ cùng công
thức CSS.

---

## 0. Bẫy `unicode-range` đã biết: đã sửa, đã xác nhận lại

`design-system/fonts/fonts-embedded.css` từng khai 2 khối `@font-face` cho mỗi tổ
hợp (family, style, weight) kiểu Google Fonts phục vụ qua mạng, khiến WeasyPrint tra
sai cmap và lộn glyph (`nghệ`→`nght`). Đã xác nhận lại trong phiên này bằng cách
trích 12 khối `@font-face` từ chính file hiện tại: **đúng 1 khối cho mỗi tổ hợp,
không khối nào trùng** - round 3 đã sửa đúng. Chi tiết cơ chế, cách tái hiện, cách
phát hiện tự động: xem `FONT-TRAPS.md` bẫy #1.

---

## 1. Headroom cho dấu chồng ở cỡ chữ lớn - đo bằng pixel-scan, không suy diễn

**Phép đo**: dựng hàng 12 ký tự Spectral 700 cỡ 160px, căn `align-items: baseline`
trong một flexbox (baseline layout của trình duyệt dùng metric thật của font, không
phải con số tôi tự đặt), chụp bằng Chromium `deviceScaleFactor: 2`, dùng toạ độ
`getBoundingClientRect()` CHỈ để biết cột X của từng ký tự (không dùng để đo chiều
cao), rồi quét PIXEL theo cột đó để tìm hàng đầu tiên có mực. So hàng-đầu-có-mực của
ký tự có dấu với ký tự trần (O, A, E, Ơ) cùng cột baseline.

**Kết quả** (device px ở dsf=2, font-size 160px = 320 device px):

| Cặp | Chênh hàng-trên-cùng | % font-size | Diễn giải |
|---|---|---|---|
| O → Ô | +61px | 19,1% | dấu mũ một tầng |
| O → Ộ | +61px | 19,1% | mũ + nặng: nặng ở DƯỚI nên không cộng thêm phía trên |
| A → Â | +63px | 19,7% | dấu mũ một tầng |
| **A → Ẫ** | **+115px** | **35,9%** | **mũ + ngã, cả hai cùng ở TRÊN: hai tầng thật, XẤU NHẤT** |
| E → Ê | +64px | 20,0% | dấu mũ một tầng |
| E → Ệ | +64px | 20,0% | mũ + nặng: nặng ở dưới |
| Ơ → Ớ | +35px | 10,9% | móc + sắc, móc nằm NGANG không xếp tầng dọc |
| Ơ → Ỡ | +31px | 9,7% | móc + ngã, tương tự |

**Kết luận, CHỐT**: có ĐÚNG một nhóm ký tự cần headroom gấp đôi nhóm còn lại - các
nguyên âm có dấu MŨ hoặc TRĂNG (â, ă, ê, ô) kết hợp với MỘT THANH ĐIỆU NẰM Ở TRÊN
(sắc, huyền, hỏi, ngã, không tính nặng vì nặng nằm dưới): Ấ Ầ Ẩ Ẫ, Ắ Ằ Ẳ Ẵ, Ế Ề Ể
Ễ, Ố Ồ Ổ Ỗ (và bản thường). Nhóm này cần khoảng **36% font-size** headroom (đo được
35,9%, nên dùng 38-40% để chừa biên an toàn đổi font). Mọi nhóm khác (chỉ mũ/trăng,
chỉ móc, móc+thanh điệu) chỉ cần khoảng **20% hoặc ít hơn**.

**Cơ chế vì sao móc (ơ, ư) không cộng dồn**: dấu móc (horn, U+031B) là phần mở rộng
NGANG gắn vào thân chữ o/u để tạo ơ/ư, không phải dấu xếp CHỒNG phía trên như mũ.
Thanh điệu của ớ/ờ/ở/ỡ/ợ vẫn nằm phía trên chữ cái, nhưng nó nằm trên đúng MỘT tầng
(thân chữ ơ), không có tầng trung gian kiểu mũ/trăng chen giữa. Đây là lý do bảng chữ
cái tiếng Việt CHỈ có 2 "họ" nguyên âm tạo dấu chồng hai tầng thật (â/ă/ê/ô + thanh
điệu trên), còn ơ/ư luôn dừng ở một tầng bất kể thanh điệu nào.

**Khi nào KHÔNG áp dụng**: số đo trên là cho Spectral 700 (weight đậm, dùng cho
tiêu đề). Một font có tỷ lệ cap-height/dấu khác (ví dụ font hiển thị chân phương với
dấu nhỏ hơn) có thể cần tỷ lệ khác - chạy lại đúng quy trình đo (script
`gen_html.py` + `shoot.mjs` + `analyze_exp1.py` trong phiên này) trước khi áp dụng
cho font khác. Ở cỡ chữ thân bài (17px, đã chốt ở nghiên cứu trước:
[[feedback_vietnamese_ink_metrics]]), phần trăm này quy ra dưới 1px, không đáng chừa
riêng.

---

## 2. Va chạm liên dòng khi line-height siết ở chữ hoa toàn phần

**Phép đo**: khối 2 dòng chữ hoa "TỶ SUẤT LỢI NHUẬN RÒNG ĐẠT / MỨC ẤN TƯỢNG TRONG
QUÝ" (cố ý chọn để dòng 1 kết thúc bằng dấu nặng kéo xuống, dòng 2 mở đầu bằng dấu
mũ+sắc kéo lên), Spectral 700, font-size 80px, quét PROFILE mực theo TỪNG HÀNG pixel
trên toàn bộ chiều rộng ảnh (không phải theo cột của một ký tự) - hợp lý vì trong một
dòng chữ hoa dài, các ký tự khác nhau lấp đầy các độ cao khác nhau nên "dải mực" của
cả dòng liền mạch, không có khe hở nội bộ; ranh giới dải chỉ xuất hiện GIỮA hai dòng.

**Kết quả, khoảng trắng đo được giữa dải mực của dòng 1 và dòng 2**:

| line-height | Khoảng trắng | % font-size (80px) |
|---|---|---|
| 1.0 | 2,5px CSS | ~3% |
| 1.05 | 5,0px CSS | ~6% |
| 1.1 | 5,0px CSS | ~6% |
| 1.15 | 5,0px CSS | ~6% |
| 1.2 | 5,0px + 1,5px CSS (tách thêm một dải vi mô là riêng dấu sắc phía trên Ấ) | ~8% |
| 1.3 | 5,0px + 9,5px CSS | ~18% |

**Ghi chú trung thực về phép đo**: khoảng trắng KHÔNG tăng tuyến tính mượt theo
line-height (phẳng ở 5px CSS suốt từ 1.05 đến 1.15 rồi mới tăng tiếp) - nhiều khả
năng do bo tròn subpixel/hinting của Chromium khi phân bổ "half-leading" trên/dưới
mỗi dòng, không phải sai số đo. Kết luận rút ra vẫn vững: **line-height 1.0 để lại
biên chỉ 2,5px CSS (~3% font-size) - mỏng tới mức lệch 1 bậc trọng lượng font hoặc
lệch DPI khi in có thể làm hai dấu chạm nhau**; từ 1.15 trở lên biên ổn định quanh
5-14px CSS, an toàn hơn nhiều lần. KHÔNG suy diễn công thức tuyến tính từ bảng này để
nội suy line-height khác - đo lại ở đúng font-size định dùng.

**Khi nào KHÔNG áp dụng**: tiêu đề một dòng (không có vấn đề liên dòng). Tiêu đề chữ
thường (không hoa toàn phần) có biên độ dấu nhỏ hơn nhiều, ít rủi ro va chạm hơn ở
cùng line-height.

---

## 3. Chữ hoa toàn phần: nơi dấu hai tầng dễ vỡ nhất

Kết hợp trực tiếp mục 1 và mục 2: chữ hoa toàn phần vừa cần headroom lớn nhất (mục 1,
vì luôn có khả năng gặp Ấ/Ầ/Ẩ/Ẫ/Ắ/Ằ/Ẳ/Ẵ/Ế/Ề/Ể/Ễ/Ố/Ồ/Ổ/Ỗ dạng hoa), vừa nhạy với
line-height nhất khi xuống dòng (mục 2, vì bản thân chữ hoa đã cao gần hết dòng, dấu
chồng đẩy tiếp lên trên, còn ít dư địa hơn chữ thường). Khuyến nghị gộp: `padding-top`
riêng cho khối (không dùng line-height để tạo headroom phía trên vì line-height chia
đều hai phía, tốn gấp đôi khoảng cần) bằng 38-40% font-size, cộng `line-height` khối
tối thiểu 1.2 nếu có từ hai dòng trở lên.

---

## 4. Kerning và tracking cho tiêu đề có dấu

**Phép đo 1 - kerning có thật sự làm gì**: cụm "TRƯỢT GIÁ TRỊ" (Spectral 700, 140px),
so `font-kerning: normal` với `none` bằng WeasyPrint, diff pixel toàn ảnh: **0,497%**
khác nhau - kerning dịch chuyển glyph thật ở các cặp T-R/G-I, không phải hiệu ứng ảo.

**Phép đo 2 - ngưỡng va chạm khi siết tracking**: cùng cụm từ, đếm connected-component
(cụm mực liền mạch) trên ảnh render qua các mức `letter-spacing`:

| letter-spacing | Số cụm liền mạch | Khe hở nhỏ nhất |
|---|---|---|
| 0 (mặc định) | 10 | 0,5px CSS - đã gần chạm do kerning font tự nhiên (T-R) |
| -0.01em | 9 | 3,5px CSS |
| -0.02em | 9 | 2,0px CSS |
| -0.03em | 9 | 0,5px CSS - gần chạm thêm một điểm |
| **-0.04em** | **8** | (2 glyph đã GỘP MỰC thành 1 khối) |
| +0.02em | 10 | 4,0px CSS |
| +0.04em | 10 | 6,5px CSS |

**Kết luận**: với tiêu đề hoa có nguyên âm móc (Ơ, Ư), tracking âm bắt đầu gây gộp
mực thật (không chỉ "gần") ở khoảng **-0.03 đến -0.04em**. Vì tracking mặc định
(0em) ĐÃ gần chạm sẵn do kerning tự nhiên của font, mọi mức tracking âm chỉ khiến
tình huống XẤU HƠN từ một nền vốn đã mỏng, không phải từ một nền an toàn - không nên
nghĩ "còn dư địa để siết thêm một chút" chỉ vì hình chưa vỡ ở mắt thường tại cỡ chữ
hiển thị nhỏ.

**Khi nào cần siết, khi nào không**: siết tracking âm chỉ nên dùng khi tiêu đề TOÀN
là ký tự không có móc ngang (mũ/trăng/thanh điệu đều nằm trong biên dọc của glyph,
không thò ngang) - trong trường hợp đó biên an toàn rộng hơn nhiều. Có Ơ/Ư trong
tiêu đề: coi -0.02em là trần, ưu tiên giảm cỡ chữ thay vì siết thêm nếu cần vừa khổ.

**Phép đo 3 - ligature, đã kiểm và loại trừ cho bộ font hiện tại**: xem
`FONT-TRAPS.md` bẫy khả nghi #3. Tóm tắt: bật/tắt `font-variant-ligatures` không có
tác dụng thực vì glyph ligature đã bị cắt khỏi font subset của repo, không phải vì
an toàn theo thiết kế.

---

## 5. Độ phủ font cho tiếng Việt: Spectral, IBM Plex Mono, IBM Plex Sans

Đọc cmap THẬT bằng fontTools, trích trực tiếp từ 12 khối `@font-face` trong
`design-system/fonts/fonts-embedded.css` (không tải font riêng, dùng đúng byte sẽ
lên sản phẩm).

| Font | 134 ký tự VN tổ hợp sẵn (NFC) | 5 dấu thanh điệu kết hợp | 3 dấu cấu trúc (mũ/trăng/móc) kết hợp |
|---|---|---|---|
| Spectral (6 weight/style) | đủ 134/134 | đủ | **THIẾU cả 3** (U+0302, U+0306, U+031B) |
| IBM Plex Mono (4 weight) | đủ 134/134 | đủ | **THIẾU cả 3** |
| IBM Plex Sans (2 weight) | đủ 134/134 | đủ | **THIẾU cả 3** |
| Noto Serif (fallback `serif`, `fc-match` xác nhận) | đủ 134/134 | đủ | đủ cả 3 |
| Noto Sans, DejaVu Serif/Sans, Liberation Serif/Sans/Mono (đã kiểm thêm) | đủ 134/134 | đủ | đủ cả 3 |

**Điểm mấu chốt, xem `FONT-TRAPS.md` bẫy #2 để có chuỗi nhân quả đầy đủ**: ba dấu
cấu trúc bị thiếu không phải vì Spectral/Plex "không hỗ trợ" - font gốc (chưa subset)
tải trực tiếp từ Google có đủ cả 878 glyph bao gồm cả ba mã này. Chúng bị loại trong
lúc `build-fonts.py` subset lại theo union unicode-range của 2 subset Google gắn
nhãn (`latin` + `vietnamese`), và cả hai nhãn đó (kiểm tận API Google Fonts) đều
KHÔNG liệt kê ba mã này - một khoảng trống trong chính siêu dữ liệu subset của
Google, không phải giới hạn của font hay của repo. Với 134/134 ký tự tổ hợp sẵn
(NFC) luôn đủ, bẫy này CHỈ lộ ra khi văn bản đầu vào ở dạng NFD (xem `FONT-TRAPS.md`
bẫy #2 để biết khi nào gặp NFD ngoài đời và cách chặn ở đầu vào).

**Khi nào không cần lo**: nếu pipeline nạp dữ liệu đã chuẩn hoá NFC trước khi đưa vào
template (khuyến nghị chuẩn trong `FONT-TRAPS.md`), độ phủ 134/134 NFC là đủ dùng
100% bảng chữ cái tiếng Việt, không cần quan tâm 3 mã cấu trúc kia nữa.

---

## Liên kết

- Danh mục bẫy đầy đủ, có cách tái hiện/phát hiện/sửa cho từng bẫy: `FONT-TRAPS.md`.
- 5 file mẫu minh hoạ áp dụng trực tiếp các số đo trên: `samples/typo-*.html`.
- Số đo dấu tiếng Việt ở cỡ thân bài (17px, kết luận CHỐT, không lật lại):
  [[feedback_vietnamese_ink_metrics]] trong bộ nhớ dự án - nghiên cứu này KHÔNG đụng
  lại vùng đó, chỉ mở rộng sang cỡ tiêu đề lớn.
