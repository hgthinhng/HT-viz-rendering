# Tổng hợp vòng 3: ráp 13 khối thành một báo cáo liền mạch 14 trang

Vòng này KHÔNG khảo sát nguồn mới. Việc chính là dựng `samples/BAO-CAO-LIEN-MACH.html`,
một báo cáo ngành hư cấu (Vận tải container nội Á) 14 trang A4, bằng cách CHỌN LỌC có chủ đích
các thủ pháp đã kiểm chứng ở bốn vòng trước, rồi đọc tuần tự để bắt những vấn đề mà không mẫu
đơn lẻ nào từng có cơ hội bộc lộ. Đây là hồ sơ giá trị chính; file HTML là bằng chứng thực
nghiệm cho hồ sơ này.

**Vũ trụ hư cấu**: tiếp nối đúng công ty và bốn công ty cùng ngành đã dùng ở
`samples/wow-*.html` và `samples/report-*.html` (CTCP Vận tải Biển Á Châu, CTCP Hàng hải Đông
Dương, CTCP Vận tải Sông Hậu, CTCP Container Miền Trung, CTCP Logistics Bắc Vịnh), tái dùng
nguyên số liệu P&L và định giá đã có ở `report-dense-data-table.html` và chỉ số cước ở
`report-exhibit-institutional.html`. Lý do: một tài liệu THẬT không bịa lại vũ trụ mỗi lần viết,
nó tiếp nối. Việc số liệu khớp giữa 6 file khác nhau trong `samples/` là bằng chứng "tổng hợp"
chứ không phải "ghép ngẫu nhiên".

**Nghiệm thu cuối cùng** (script 3 phép, `weasyprint` 69.0 thật + `pymupdf`):
`trang: 14, svg: 7, drawing_total: 377, raster xref (quét toàn bộ, không dùng get_images): 0,
em-dash: 0, en-dash: 0`. Cả 14 trang đã mở ảnh render (`dpi=110`) và xem tận mắt, hai vòng lặp
sửa lỗi dựa trên ảnh, không dựa trên số liệu text/drawing (xem mục "vấn đề chỉ lộ ra khi đọc
tuần tự" bên dưới, cả ba lỗi thật đều KHÔNG lộ qua đếm SVG/text, chỉ lộ qua nhìn ảnh).

---

## 1. Bảng "lấy gì từ đâu"

| # | Thủ pháp | Lấy từ | Vì sao lấy |
|---|---|---|---|
| 1 | Bốn lớp vào bài: kicker, headline, dek, nut graf | `01-editorial/FINDINGS.md` mục 1.1, `editorial-mo-dau-kicker-dek.html` | Trang thân bài cần đọc lướt được trong 20 giây; action-title bắt buộc theo F2.3 |
| 2 | Lưới 1 cột cho bìa/ngăn chương, khác lưới thân bài | mục 1.2 | Báo cáo 14 trang đủ dài để "trả phí" tín hiệu chuyển cảnh này |
| 3 | Drop cap `::first-letter`, đúng 1 lần | mục 2.3, `editorial-tufte-sidenote-margin.html` | Dùng đúng khuyến nghị "mỗi phần lớn 1 lần"; chọn từ mở đầu bằng phụ âm ("Ngành") để né rủi ro dấu tiếng Việt bị cắt khi phóng to 3,6 lần |
| 4 | Kicker mono, headline/dek serif | mục 2.4, token đã chốt | Tuân token có sẵn, không quyết định lại |
| 5 | Số hero phá thang chữ, đúng 1 lần mỗi trang thiết kế | mục 3.2, `wow-mot-con-so.html` | Trang bìa và trang một-con-số |
| 6 | Section divider trọn trang cho ranh giới Phần lớn ĐẦU TIÊN | `02-professional-report/FINDINGS.md` F1.3, `wow-trang-ngan-chuong.html` | 14 trang đủ dài để trả phí 1 lần; KHÔNG lặp lại lần 2, xem mục 2 |
| 7 | BLUF/Minto, verdict-first, cấm recap | F2.1, F2.2, `report-exec-brief-action-first.html` | Luật đã chốt của operator (`feedback_exec_brief_action_first_no_recap`), có gốc học thuật |
| 8 | Action title cho mọi H2 | F2.3 | Mọi tiêu đề mục là một khẳng định có số |
| 9 | Đánh số Hình/Bảng liên tục toàn tài liệu | F3.1, `report-exhibit-institutional.html` | Hình 1 đến 5, Bảng 1 đến 2, không số nào lặp |
| 10 | Đường liền = thực tế, nét đứt = dự phóng, vạch chốt | F3.2 | Hình 1 |
| 11 | Bảng ký hiệu dùng chung, đặt Ở MỘT NƠI duy nhất | F3.3, cải tiến so với `report-exhibit-institutional.html` | Xem phát hiện tuần tự số 4 |
| 12 | Số căn phải/tabular; ngoặc đơn cho bảng trích BCTC, dấu trừ đỏ cho bảng dashboard, không trộn 2 kiểu trong 1 bảng | F4.1, F4.2, `report-dense-data-table.html` | Bảng 1 (comps, dashboard) và Bảng 2 (P&L, trích BCTC) dùng đúng 2 quy ước khác nhau, có annot giải thích |
| 13 | Hậu tố cột TT/DP | F4.5 | Mọi cột năm trong Bảng 1, Bảng 2 |
| 14 | Gạch ngang cho số 0 thật | F4.3 | Dòng "Thu nhập khác, ròng" năm 2024 |
| 15 | Dòng tổng viền đơn trên/đôi dưới đậm; dòng trung vị KHÔNG viền đôi | F4.4 | Bảng 2 (Lợi nhuận sau thuế) so với Bảng 1 (Trung vị ngành) |
| 16 | Ngày chốt số liệu tách khỏi ngày biên soạn, áp dụng MỌI trang | F5.1 | Xem phát hiện tuần tự số 6 |
| 17 | Giả định neo tại đúng con số nó chi phối, hộp giả định 2 lớp | F5.2, `source-khoi-gia-dinh-dinh-gia.html` | Hình 5 và `.assume-box` liền kề |
| 18 | Bảng quy đổi nguồn, không lộ kênh nội bộ | `06-source-notes/SOURCE-DISCLOSURE.md` | Trang Nguồn và phương pháp, không nêu tên nhà cung cấp/hệ thống nào |
| 19 | Small multiples cùng trục | `01-editorial` mục 4.2, `03-chart-doctrine` | Hình 3, lộ ra phân hoá 3 tuyến mà 1 biểu đồ gộp sẽ che mất |
| 20 | Football field, thị trường trước nội tại sau | `03-chart-doctrine/CHART-SELECTION.md`, `chart-football-field-dinh-gia.html` | Hình 4 |
| 21 | Lưới độ nhạy 2 chiều, thang 1 hue liên tục | `chart-luoi-do-nhay-hai-chieu.html` | Hình 5, né thang diverging 2-hue gợi ý sai một ngưỡng tốt/xấu ở giữa bảng |
| 22 | Bar sắp giảm dần thay pie cho cơ cấu chi phí 5 hạng mục | Bảng phụ "khi nào là chart giả" trong `CHART-SELECTION.md` | Hình 2 |
| 23 | Trang một-con-số, không khung/icon | `04-wow-layer/FINDINGS.md` mục 5, `wow-mot-con-so.html` | Trang 6 |
| 24 | Khoảnh khắc phá nhịp bằng đảo màu, đúng 1 lần | mục 2, `wow-phanhip-dao-mau.html` | Trang 9; chọn từ "Dư cung" (không dấu thanh) thay vì tái dùng "Rủi ro" |
| 25 | Kỹ thuật "khối nổi" bằng 2 phần tử lệch vị trí, không `box-shadow` | mục 8, `wow-do-noi-khong-blur.html` | Mọi hero number trong 14 trang |
| 26 | Vũ trụ hư cấu và số liệu P&L/comps gốc | toàn bộ `report-*.html`, `wow-*.html` | Giữ số khớp giữa file tổng hợp và mẫu gốc |

## 2. Bảng "cố ý bỏ gì"

| # | Thủ pháp bỏ | Nguồn | Vì sao bỏ |
|---|---|---|---|
| 1 | Sidenote lề kiểu Tufte (float phải + margin âm) | `01-editorial` mục 2.3, `editorial-tufte-sidenote-margin.html` | Vòng 2 tự bắt lỗi round-trip PDF thật: `pymupdf get_text()` mặc định xáo trộn thứ tự khối nội dung floated khi container vừa `float` vừa `flex`, phải verify bằng `get_text("words")` sắp toạ độ mới thấy đúng. Kỹ thuật này CHƯA được verify lại theo đúng phương pháp đó ở bất kỳ mẫu nào (kể cả bản gốc). Với một file 14 trang cần verify nhanh trong ngân sách vòng này, tôi chọn không mang theo một kỹ thuật còn cảnh báo mở, dùng khối nguồn/caption tĩnh cuối exhibit thay cho footnote lề. |
| 2 | Mô-típ đồ hoạ lặp lại xuyên suốt kiểu MIT Technology Review | `01-editorial` mục 1.4 | Chính hồ sơ gốc viết rõ: "giá trị nằm ở việc lặp lại xuyên suốt NHIỀU báo cáo", một tài liệu đơn lẻ không có cơ hội chứng minh mô-típ đã quen mắt độc giả. Phát minh một mô-típ mới rồi chỉ dùng đúng 1 lần trong 1 file là làm ngược khuyến nghị của chính nguồn. |
| 3 | Optical sizing hai bản vẽ (Financier Display/Text) | `01-editorial` mục 3.1 | `tokens.css` đã CHỐT hợp nhất `--font-display`/`--font-serif` thành một font-stack Spectral. Đây là quyết định của operator, không phải khoảng trống cần lấp. |
| 4 | Trang ngăn chương trọn khổ LẦN THỨ HAI, cho ranh giới Phần 02 | `02-professional-report` F1.3, `wow-trang-ngan-chuong.html` | Phát hiện khi đọc tuần tự: dùng đúng 1 kiểu trang ngăn 2 lần liên tiếp trong một tài liệu 14 trang tự nó biến thành khuôn mẫu (đúng tinh thần ANTI-SLOP #4: lặp lại một mẫu phá nhịp quá nhiều lần là hết tác dụng; ở quy mô 14 trang ngưỡng "quá nhiều" còn thấp hơn tài liệu dài). Phần 02 dùng một marker nhẹ dạng dòng chữ mono kèm gạch chân đậm (`.part-mark`) thay vì trọn trang, tạo bất đối xứng có chủ đích giữa hai lần chuyển phần. |
| 5 | Pull-quote hư cấu từ lãnh đạo công ty | `editorial-tufte-sidenote-margin.html` (đã tự dán nhãn "phát biểu hư cấu") | Báo cáo NGÀNH so sánh 5 công ty; trích lời "lãnh đạo" của đúng 1 trong 5 công ty đó, dù đã dán nhãn hư cấu, đọc dễ như ưu ái ngầm công ty đó. Nối với luật đã chốt "cấm bịa social proof", rủi ro đọc nhầm cao hơn giá trị minh hoạ thêm. |
| 6 | Gauge, radar | Luật cứng | Không cân nhắc lại, cấm tuyệt đối. |
| 7 | Pie hoặc donut cho cơ cấu chi phí 5 hạng mục | `03-chart-doctrine` | Trên 3 đến 4 lát là chuyển sang bar ngang theo đúng bảng tra; Hình 2 dùng bar sắp giảm dần. |
| 8 | Dual-axis line cộng column | `03-chart-doctrine/FINDINGS.md` mục 3 | Thay bằng small multiples dọc cùng trục (Hình 3), tránh chọn 2 thang tuỳ ý tạo tương quan giả. |
| 9 | CSS `float: footnote` (Generated Content for Paged Media) | `06-source-notes`, ghi nhận "hỗ trợ chưa đủ ổn định" | Dùng khối nguồn tĩnh cuối mỗi exhibit thay chân trang tự động chưa kiểm chứng chắc trên WeasyPrint 69.0. |
| 10 | `clamp()`/`min()`/`max()` cho bất kỳ `font-size` nào, kể cả trên trang bìa | `01-editorial` mục 0.3 | Xem cảnh báo riêng ở mục 4 bên dưới: chính `report-exec-brief-action-first.html` hiện tại VẪN còn dùng `clamp()` cho `h1.verdict`, vi phạm đúng phát hiện mà hồ sơ 01-editorial đã cảnh báo. Bản tổng hợp này dùng `rem` cố định cho mọi cỡ chữ, không có ngoại lệ. |
| 11 | Chữ hoa toàn phần, tracking rộng cho headline lớn | `typo-tieu-de-lon-dau-chong.html`, `typo-tracking-va-kerning.html` | Không có trang nào trong 14 trang cần headline hoa toàn phần cỡ lớn; giữ Sentence case cho action title dễ đọc hơn khi mật độ chữ trong trang cao. |

## 3. Vấn đề CHỈ LỘ RA khi đọc tuần tự (phần cốt lõi)

### 3.1 Tràn trang vô hình khi ráp nhiều khối lại, dù mỗi khối "trông vừa 1 trang"

**Phát hiện ở đâu**: trang 2 (Tóm tắt điều hành) và trang 5 đến 6 (Phần 1B). **Bằng cách nào**:
lần render đầu tiên ra 15 trang vật lý thay vì 13 khối `.page` dự kiến; mở ảnh từng trang thấy
trang 2 dừng đột ngột ở dòng "BA CÂU HỘI ĐỒNG..." rồi 3 khối hỏi-đáp trôi hết sang một trang thứ
ba gần như trắng, và Hình 3 (small multiples) trôi hết sang một trang riêng gần trắng phía dưới
Hình 2. **Vì sao chỉ lộ ở đây**: cả `report-exec-brief-action-first.html` VÀ 3 mẫu report khác
của vòng 02 đã TỰ tràn thành 2 trang vật lý mỗi file (xem "Phụ lục kỹ thuật" cuối
`02-professional-report/FINDINGS.md`), nhưng vì mỗi file đó ĐÃ ĐƯỢC CHẤP NHẬN là "2 trang" ngay
từ đầu, không ai coi đó là lỗi cần sửa. Khi tôi ráp đúng NỘI DUNG TƯƠNG TỰ vào một tài liệu 14
trang có ngân sách trang cố định, phần tràn không còn là "thêm 1 trang vô hại" mà làm lệch nhịp
tổng thể và để lại khoảng trắng xấu. Không mẫu đơn lẻ nào có động lực phát hiện việc này vì
không có "ngân sách trang" để vi phạm. **Sửa ra sao**: siết khoảng cách toàn cục (padding
`.page-flow` từ 20mm/16mm xuống 16mm/12mm, margin `.kicker-bar`/`.exhibit`/`p.dek` giảm 22 đến
24 phần trăm), viết súc tích hơn ở tóm tắt điều hành (rút câu văn, giảm padding bảng/killbox/qa),
và giảm `margin-top` giữa Hình 2 và Hình 3 từ 24px xuống 10px. Kết quả: tóm tắt điều hành gọn
lại đúng 1 trang; Phần 1B vẫn tách 2 trang nhưng mỗi trang giờ dùng đủ không gian, không còn
trắng bất thường. Tổng tài liệu giảm từ 15 xuống 14 trang vật lý.

### 3.2 Kỹ thuật "khối nổi" (behind/front lệch vị trí) an toàn với SỐ, vỡ với CỤM TỪ có khoảng trắng

**Đây là phát hiện quan trọng nhất của vòng này.** Ba mẫu gốc dùng kỹ thuật 2 phần tử lệch vị
trí (`position:absolute` cho bản mờ phía sau, `position:relative` cho bản chính phía trước,
cùng nằm trong một `display:inline-block; position:relative`) đều CHỈ thử với một TOKEN ĐƠN
không khoảng trắng: `"150"` (`wow-trang-ngan-chuong.html`), `"18%"` (`wow-bia-mo-dau.html`,
`wow-mot-con-so.html`), `"+30%"` (`wow-mot-con-so.html`). Khi tôi tự chọn hero-word cho trang
phá nhịp riêng của mình là một CỤM TỪ CÓ KHOẢNG TRẮNG, `"Dư cung"`, WeasyPrint tính sai độ rộng
containing-block cho phần tử `position:absolute` bên trong wrapper `inline-block`, khiến bản
"đằng sau" tự ngắt dòng thành `"Dư"` rồi `"cung"` dù bản "đằng trước" (in-flow) không ngắt dòng
nào cả. Dòng "cung" bị ngắt rơi xuống thấp, đè thẳng lên đoạn dek phía dưới, làm cả đoạn văn
không đọc được.

**Phát hiện bằng cách nào**: không có cách nào bắt được lỗi này qua đếm SVG hay đối chiếu tầng
text (chữ vẫn trích ra đúng, `get_text()` vẫn đọc được "Dư cung" và "cung" riêng biệt, không có
lỗi font/glyph). Lỗi CHỈ lộ ra khi mở ảnh PNG render thật và nhìn bằng mắt, đúng lý do phép thứ
ba của bộ nghiệm thu (mở từng ảnh trang) được đánh dấu "quan trọng nhất" cho mũi nghiên cứu này.

**Sửa ra sao**: thêm `white-space:nowrap` cho cả 3 cặp behind/front dùng trong toàn tài liệu
(`.num-behind/.num-front` ở trang bìa, `.num-behind2/.num-front2` ở trang một-con-số,
`.inv-behind/.inv-front` ở trang đảo màu), kể cả 2 cặp đầu vốn dùng token đơn không dính lỗi,
để phòng ngừa nếu sau này ai đó đổi số thành chữ. Đây là một lỗ hổng có thật trong CHÍNH catalog
kỹ thuật của vòng 04-wow-layer (`wow-do-noi-khong-blur.html`), không lộ ra ở đó vì mẫu catalog
chưa từng thử với dữ liệu dạng chữ nhiều từ, chỉ lộ khi có người áp dụng kỹ thuật đó cho một loại
nội dung khác trong bối cảnh một tài liệu thật.

### 3.3 Nhãn hai đầu dải chồng lên nhau khi dải hẹp, dù đúng quy ước của mẫu gốc

**Phát hiện ở đâu**: Hình 4 (football field), dải P/E ngành trung vị chỉ rộng 1.300 đồng trên
tổng trục 8.000 đồng. **Vì sao chỉ lộ ở đây**: `chart-football-field-dinh-gia.html` (vòng 03)
đặt nhãn giá trị NGAY BÊN TRONG hai đầu mỗi dải, và mọi dải minh hoạ trong mẫu đó đều đủ rộng
nên hai nhãn không bao giờ chạm nhau. Quy ước "đặt nhãn bên trong 2 đầu dải" chỉ vỡ khi có một
dải THẬT SỰ hẹp, và mẫu gốc (dữ liệu demo lý tưởng hoá) không có động lực tạo ra một dải hẹp như
vậy. Khi tôi tự tính dải P/E hẹp cho dữ liệu thật của tài liệu này, hai nhãn "19.800" và "21.100"
chồng lên nhau đọc thành `"19.80@1.100"` không đọc được. **Sửa ra sao**: chuyển toàn bộ 3 dải
sang đặt nhãn NGOÀI hai đầu dải (neo trái ra bên trái điểm bắt đầu, neo phải ra bên phải điểm kết
thúc) thay vì bên trong, cách này an toàn bất kể độ rộng dải, áp dụng nhất quán cho cả 3 dải dù
chỉ 1 dải bị lỗi thật.

### 3.4 "Bảng ký hiệu dùng chung" chỉ thật sự đúng nghĩa khi có NHIỀU exhibit trải qua NHIỀU trang để đặt nó vào một nơi

**Phát hiện ở đâu**: khi quyết định đặt "Bảng ký hiệu" (TT/DP/.../-) ở đâu trong tài liệu 14
trang có 5 Hình và 2 Bảng. **Vì sao chỉ lộ ở đây**: `report-exhibit-institutional.html` (vòng 02)
đặt khối "Bảng ký hiệu dùng chung cho mọi hình và bảng trong tài liệu" NGAY TRÊN CHÍNH trang chứa
2 exhibit đó, vì mẫu đó chỉ có đúng 1 trang để minh hoạ khái niệm. Nhưng đọc kỹ chính văn bản quy
tắc F3.3 mà hồ sơ đó viết ra ("một trang quy ước NGẮN, đặt riêng... người đọc chỉ cần học một bộ
ký hiệu MỘT LẦN cho cả tài liệu dài hàng chục bảng, thay vì đọc lại chú thích ở mỗi bảng"), việc
lặp bảng ký hiệu ngay trên trang exhibit của chính nó mâu thuẫn với chính lý do tồn tại của quy
tắc. Vấn đề này không thể lộ ra từ một mẫu 1 trang, vì không có "mỗi bảng" nào khác để so sánh.
**Sửa ra sao**: dồn toàn bộ bảng ký hiệu về đúng MỘT trang cố định (trang 11, Nguồn và phương
pháp); 5 Hình và 2 Bảng còn lại trong tài liệu chỉ dùng ký hiệu (`TT`, `DP`, dấu gạch ngang) mà
không lặp lại chú giải, đúng tinh thần F3.3 hơn cả mẫu gốc sinh ra quy tắc đó.

### 3.5 Hai exhibit cùng một mô hình định giá tự mâu thuẫn số liệu nếu không đối chiếu bằng tay

**Phát hiện ở đâu**: Hình 4 (football field) và Hình 5 (lưới độ nhạy WACC×g) là hai cách nhìn
khác nhau của CÙNG một mô hình DCF, đặt ở hai trang liền kề. **Vì sao chỉ lộ ở đây**: khi viết
nháp đầu tiên, tôi gán dải DCF ở Hình 4 (19.200 đến 24.600 đồng) độc lập với việc tính bảng độ
nhạy ở Hình 5, không có phép nào bắt buộc hai con số phải khớp. Khi tính đúng bảng Hình 5 (giao
của WACC 10 đến 12 phần trăm và g 1,5 đến 2,5 phần trăm) thì dải thật là 19.050 đến 24.750 đồng,
lệch với con số đã viết ở Hình 4. Không mẫu đơn lẻ nào của vòng 02/03 từng đặt 2 exhibit của
CÙNG một mô hình sát nhau, nên phép đối chiếu chéo này chưa từng được yêu cầu ở đâu trước đây.
**Sửa ra sao**: tính lại Hình 4 đúng theo 4 ô góc của lưới Hình 5 (làm tròn 19.050 thành 19.100,
24.750 thành 24.700), ghi rõ trong caption Hình 4 khoảng WACC/g dùng để lấy dải, giúp người đọc
tự đối chiếu được với bảng Hình 5.

### 3.6 F5.1 (tách ngày chốt số liệu khỏi ngày biên soạn) đã kiểm chứng ở vòng 02 nhưng chưa từng áp dụng lại ở vòng 04

**Phát hiện ở đâu**: khi viết colophon cho cả 14 trang. **Vì sao chỉ lộ ở đây**: 4 mẫu
`wow-*.html` (vòng 04, viết độc lập với vòng 02) đều chỉ ghi MỘT ngày duy nhất
(`"Dữ liệu chốt 2026-08-01"`), không tách ngày chốt số liệu khỏi ngày biên soạn theo đúng F5.1
mà CHÍNH vòng 02 đã kiểm chứng và viết thành quy tắc trước đó. Đây không phải lỗi của vòng 04
(agent đó không có nhiệm vụ đọc chéo hồ sơ vòng 02), nhưng là bằng chứng cụ thể rằng một nguyên
tắc đã kiểm chứng ở một vòng không tự động lan sang vòng khác nếu không ai chủ động tổng hợp lại.
Chỉ lộ ra khi đọc CẢ HAI hồ sơ và so sánh cách hành xử THẬT trên mẫu, không lộ nếu chỉ đọc riêng
từng hồ sơ hoặc chỉ đọc phần "phát hiện" mà không xem lại chính mẫu đã render. **Sửa ra sao**:
áp dụng đúng F5.1 xuyên suốt cả 14 trang, mọi colophon đều ghi cả hai mốc tách bạch:
"Dữ liệu chốt 2026-03-31 · Biên soạn 2026-08-01".

### 3.7 Cảnh báo phụ, ngoài phạm vi sửa của vòng này: mẫu gốc vẫn còn `clamp()`

Không phải phát hiện "chỉ lộ ra khi đọc tuần tự" theo đúng nghĩa hẹp, nhưng đáng ghi lại vì tìm
thấy trong lúc đọc lại mã nguồn `report-exec-brief-action-first.html` để lấy cấu trúc `@page`:
dòng `h1.verdict{ font-size:clamp(1.55rem, 1.1rem + 1.6vw, 2.15rem); ... }` VẪN còn tồn tại
trong file này, vi phạm đúng phát hiện 0.3 mà `01-editorial/FINDINGS.md` đã cảnh báo từ vòng 1
("`clamp()` bị WeasyPrint bỏ qua ÂM THẦM, property rớt về giá trị kế thừa"). File đó thuộc vòng
02 và nằm ngoài phạm vi ghi của agent này (luật phạm vi chỉ cho sửa `research/` và tạo file mới
trong `samples/`, không cho sửa mẫu đã có), nên KHÔNG tự sửa, chỉ ghi nhận ở đây để vòng dọn dẹp
sau xử lý. Bản tổng hợp `BAO-CAO-LIEN-MACH.html` không kế thừa lỗi này, dùng `rem` cố định cho
mọi cỡ chữ.

---

## 4. Nhận định về nhịp

**Khoảnh khắc phá nhịp dùng trong tài liệu**: đúng 2 lần, hai kỹ thuật khác nhau. Trang 6 (một
con số, kỹ thuật "yên tĩnh": số lớn đứng một mình, không đảo màu) đóng Phần 01; trang 9 (đảo màu
"Dư cung", kỹ thuật "ồn ào": nền tối, chữ sáng, 3 điều kiện) đặt giữa Phần 02 đúng chỗ có tin
rủi ro nặng nhất. Hai kỹ thuật khác hẳn nhau nên không đọc như lặp lại, dù cùng thuộc nhóm "phá
nhịp". **Đánh giá hiệu quả**: cả hai đặt đúng chỗ nội dung xứng đáng với sự gián đoạn (đóng một
phần lớn; công bố điều kiện đảo ngược khuyến nghị), không dùng để trang trí. **Bao nhiêu lần là
quá nhiều**: với một tài liệu 14 trang, 2 lần là ngưỡng trên hợp lý; ANTI-SLOP.md của vòng 04 nói
"quá 3 lần trong CẢ TÀI LIỆU" cho tài liệu dài hơn, nhưng phát hiện 3.4 (mục 2 trong bảng "cố ý
bỏ") cho thấy ngay cả LẶP LẠI CÙNG MỘT LOẠI trang phụ (trang ngăn chương trọn khổ) 2 lần trong 14
trang cũng đã đủ để cảm nhận thành khuôn mẫu. Kết luận thực nghiệm cho quy mô báo cáo cỡ vừa
(12 đến 16 trang): ngưỡng an toàn là mỗi LOẠI trang phá nhịp/trang thiết kế đặc biệt chỉ nên xuất
hiện ĐÚNG 1 LẦN, trừ khi hai lần đó dùng kỹ thuật thị giác khác hẳn nhau.

**Bất nhất về khoảng trắng cuối trang, ranh giới mỏng cần vòng sau cân nhắc**: sau khi sửa hết
lỗi tràn trang, 4 trong 6 trang của Phần 02 (Hình 4, Hình 5, Bảng 1 so sánh định giá, trang Nguồn
và phương pháp) đều kết thúc sớm, để lại 40 đến 60 phần trăm khoảng trắng cuối trang. Từng trang
riêng lẻ ĐÚNG luật "đừng nhồi nhét giả tạo" (không có gì để thêm mà không loãng nội dung), nhưng
xếp 4 trang như vậy liên tiếp, chỉ ngắt bởi 1 trang đảo màu ở giữa, bắt đầu đọc như "hết nội
dung" hơn là "khoảng trắng có chủ đích" kiểu trang bìa/trang một-con-số. Ranh giới giữa hai trạng
thái này CHỈ lộ ra khi xếp đủ nhiều trang cạnh nhau để so sánh; một mẫu đơn lẻ (như các mẫu gốc
của vòng 02/03, luôn tự đứng một mình) không đủ ngữ cảnh để phân biệt. Tôi giữ nguyên (không ép
layout đầy giả tạo), nhưng gợi ý vòng sau: nếu quy mô báo cáo tăng lên, nên gộp bớt số exhibit
độc lập trong một phần định giá, hoặc thêm 1 đoạn phân tích ngắn mỗi trang để lấp khoảng trắng
bằng NỘI DUNG thật thay vì bằng cách nới `padding`.

---

## 5. Mọi bất nhất tìm thấy giữa các mẫu, đo bằng `grep` trên toàn `samples/`

| Điểm bất nhất | Bằng chứng | Xử lý trong bản tổng hợp |
|---|---|---|
| Tên class cho dòng chú nguồn dưới chart/bảng, ít nhất 5 tên khác nhau cho cùng một vai trò | `class="source"` (8 file chart/palette), `class="source-line"` (4 file editorial/source), `class="src-line"` (2 file report), `class="foot-legend"` (2 dòng report-dense-data-table.html), `class="source-block"`/`class="cutoff-banner"` (source-dong-nguon-dinh-che.html) | Bản tổng hợp dùng ĐÚNG MỘT tên xuyên suốt 14 trang: `p.src-line` cho dòng nguồn dưới mỗi exhibit, `.cutoff-banner` riêng cho banner chốt ngày (vai trò khác, xuất hiện đúng 2 nơi: trang 11 và trang 13) |
| Thang chữ không tham chiếu chung một hệ token | 5 mẫu `wow-*.html` mỗi file tự khai `font-size` bằng px rời rạc (11px, 12px, 13px, 15px, 17px, 18px cho các vai trò kicker/label/dek khác nhau), KHÔNG file nào import biến `--fs-caption/--fs-small/--fs-body/--fs-dek/--fs-h3/--fs-h2/--fs-h1` dù các biến này đã có sẵn trong `design-system/tokens.css` | Bản tổng hợp khai 7 biến `--fs-*` một lần ở đầu file và dùng lại cho MỌI vai trò chữ ở cả 14 trang, chỉ có hero number (phá thang có chủ đích) đặt px trực tiếp |
| `--fs-body` trôi giữa 0,98rem, 1rem, 1,02rem giữa các mẫu 01-editorial/06-source-notes | `editorial-tufte-sidenote-margin.html` dùng 1,02rem; `source-footnote-sidenote-endnote.html` dùng 0,98rem; 7 file còn lại dùng 1rem | Bản tổng hợp chốt `--fs-body: 1rem`, không có ngoại lệ |
| Đánh số Hình/Bảng "liên tục toàn tài liệu" (F3.1) chưa từng được kiểm bằng một tài liệu thật nhiều trang | `report-exhibit-institutional.html` chỉ có "Hình 1, Hình 2" trên 1 trang; `editorial-chu-thich-nguon-rest-of-world.html` dùng "Hình 4" rồi "Hình 2" (thứ tự ngược, vì đó là demo cơ chế tham chiếu chéo, không phải một tài liệu thật) | Bản tổng hợp là phép thử THẬT đầu tiên cho F3.1 trên quy mô nhiều trang: Hình 1 đến 5 và Bảng 1 đến 2 chạy đúng thứ tự xuyên suốt, không số nào lặp hay đảo. Đây là một xác nhận tích cực, không phải một lỗi. |
| Chú thích căn cứ "đã kiểm tra an toàn khi in" không phải lúc nào cũng khớp engine WeasyPrint | Xem mục 3.7 ở trên (`clamp()` còn sót trong `report-exec-brief-action-first.html`) | Ghi nhận, không tự sửa file ngoài phạm vi |

---

## 6. Đầu ra và phạm vi

- `samples/BAO-CAO-LIEN-MACH.html`: 14 trang A4, tự chứa, không CDN, không build step, mở bằng
  trình duyệt là chạy. Không `git add`, không `git commit`, đúng luật phạm vi.
- Không sửa `design-system/`, `components/`, `illustrations/`, `charts/`, `scripts/`, `tests/`.
