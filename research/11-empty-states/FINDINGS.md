# Trạng thái rỗng và trạng thái thiếu dữ liệu trong báo cáo tài chính

Vòng 4, vùng "Trạng thái rỗng và trạng thái thiếu dữ liệu". Đọc `research/RESEARCH-LEDGER.md`
mục mindset trước khi dùng file này: mọi thủ pháp dưới đây là Ý THAM KHẢO, không phải khuôn ép,
trừ mục 0 (phát hiện kỹ thuật, là ràng buộc đo được). Chín vùng trước đã làm editorial,
professional report, chart doctrine, wow layer, typography VN, chú nguồn, bảng màu đen trắng,
minh hoạ ngành, và ba mảng chưa gắn tên riêng khác - file này KHÔNG lặp lại phần "thực tế và
dự phóng" đã có ở `research/06-source-notes/FINDINGS.md` mục 4, dù hai chủ đề liền kề nhau và
va chạm trực tiếp ở mục 3 dưới đây.

Người dùng có một luật đã chốt liên quan trực tiếp: số neo phải gắn định danh và cấp nguồn, và
phải phân biệt số CÔNG BỐ với số DỰ BÁO (`feedback_neo_so_phai_gan_dinh_danh_va_nguon`,
`feedback_no_source_disclosure_in_artifacts`). Vùng này là mặt còn lại của cùng đồng xu: khi
KHÔNG có số thì nói thế nào cho trung thực.

---

## 0. Phát hiện kỹ thuật: `<span>` làm flex item với `border-radius:50%` bị WeasyPrint vẽ thêm
   một đuôi nhọn, chưa vòng nào ghi nhận

Bắt được khi tự nghiệm thu `samples/empty-trang-thai-rong-toan-phan.html`: chuỗi bốn chấm tròn
đếm được (●●○○) render ra bốn hình quả bóng bay có đuôi nhọn phía dưới, không phải hình tròn.
Đúng tinh thần "so ảnh mức byte, đừng so bằng mắt" đã ghi ở đầu `RESEARCH-LEDGER.md`: phát hiện
này chỉ lộ ra khi MỞ ẢNH thật ở độ phân giải cao (300-400dpi), một bài kiểm text-round-trip
không bắt được vì không có chữ nào sai.

**Cô lập nguyên nhân bằng 12 biến thể tối giản** (giữ trong `/tmp` lúc làm việc, không đưa vào
repo vì là file chẩn đoán chứ không phải mẫu tham khảo): thử lần lượt bỏ từng yếu tố nghi ngờ -
flex lồng nhau, `min-width:0`, đơn vị `mm` cho trang, phần tử `<p>` đứng trước, font Spectral so
với sans-serif, có/không khối `.empty-card` bọc ngoài. TẤT CẢ các biến thể trên vẫn lỗi. Chỉ một
thay đổi duy nhất sửa được: đổi phần tử vẽ chấm từ `<span>` (mặc định `display:inline`) sang
`<div>`, HOẶC giữ nguyên `<span>` nhưng khai tường minh `display:inline-block` trên chính class
đó trước khi nó trở thành flex item.

**Kết luận**: WeasyPrint 69.0 blockify một `<span>` bên trong `display:flex` để làm flex item,
nhưng khi phần tử đó còn mang `border-radius:50%`, việc blockify không "tẩy sạch" hộp inline gốc
trước khi vẽ đường viền bo tròn - kết quả là một góc bị kéo dài thành đuôi nhọn thay vì khép kín
thành cung tròn. Lỗi không xuất hiện nếu phần tử đã LÀ block/inline-block NGAY TỪ ĐẦU (không cần
đợi flex blockify).

**Cách sửa, xác nhận lại bằng render thật**: khai tường minh `display: inline-block;` (hoặc dùng
hẳn `<div>`) trên MỌI class dùng làm chấm tròn/step-dot/status-dot là flex item, đừng dựa vào
flex tự blockify một `<span>` trần. Đã sửa `samples/empty-trang-thai-rong-toan-phan.html`
(thêm dòng `display: inline-block;` vào `.step-dot`, xem comment tại chỗ) và verify lại bằng
crop ảnh 400dpi: bốn chấm tròn tuyệt đối, không còn đuôi.

**Đối chiếu ngược, một tin tốt**: quy ước `.swatch-dot`/`.dot-hollow` đã có sẵn từ vòng 2
(`samples/source-bang-thuc-te-du-phong.html`) và được dùng lại đúng cách ở
`samples/empty-bang-sau-loai-vang-mat.html` của vòng này KHÔNG dính lỗi, vì cả hai đều khai
`display: inline-block;` tường minh ngay trong định nghĩa class - tức thói quen cũ của repo đã
vô tình đúng, chỉ là chưa ai biết TẠI SAO nó phải viết vậy. Từ giờ đây là một quy tắc có lý do,
không phải một chi tiết ngẫu nhiên có thể bị xoá khi dọn code.

**Khi nào ĐỪNG áp dụng sai bài học này**: đừng suy rộng thành "mọi `<span>` trong flex đều lỗi"
- chỉ border-radius bo tròn mới lộ vấn đề (đã thử `.c-b` chấm tròn KHÔNG viền, TÔ ĐẶC, trong
cùng bối cảnh lỗi và nó vẫn tròn đúng ở lần thử đầu tiên vì không có cạnh viền để lộ đuôi thừa;
nhưng để an toàn tuyệt đối, quy tắc áp dụng chung vẫn nên là "mọi chấm tròn flex item đều khai
display tường minh", không cần nhớ ngoại lệ nào ăn may).

**Đề xuất vòng sau**: audit toàn bộ `components/`, `charts/`, và các `samples/*.html` khác xem
còn chỗ nào dùng `<span>` bo tròn làm flex/inline-flex item mà THIẾU khai `display` tường minh -
tìm bằng `grep -rn "border-radius: 50%"` rồi kiểm từng chỗ có `<span>` hay không, có
`display:inline-block`/`display:block` đứng trước hay không.

---

## 1. Bảng ký hiệu sáu loại vắng mặt: khảo sát quy ước định chế và lý do chọn từng ký hiệu

Bảng đầy đủ, dùng hàng ngày: `research/11-empty-states/ABSENCE-TABLE.md`. Mục này chỉ ghi lại
QUÁ TRÌNH khảo sát và LÝ DO loại bỏ các phương án khác, không lặp lại bảng.

### 1.1 Khảo sát: mỗi định chế chọn một cách khác nhau, không có chuẩn chung

- **IMF**, "World Economic Outlook Database, Assumptions and Data Conventions": dùng khoảng
  trống/"n/a" cho không có dữ liệu (xác nhận qua tổng hợp tìm kiếm, bản gốc không trích nguyên
  văn được).
  https://www.imf.org/en/publications/weo/weo-database/assumptions-and-data-conventions
- **World Bank**, World Development Indicators: `..` (hai dấu chấm) cho "không có dữ liệu".
  https://datahelpdesk.worldbank.org/knowledgebase/topics/19285-data-not-available
- **BIS**, "Conventions used in the BIS Quarterly Review" (xác nhận qua WebFetch toàn văn):
  `...` (ba chấm) = không có dữ liệu, `.` (một chấm) = không áp dụng, `e` = ước tính, gạch ngang
  kiểu phương Tây = "nil or negligible".
  https://www.bis.org/publ/qtrpdf/conventions.htm
- **Eurostat**, "Glossary: Flag": `:` = không có dữ liệu, cộng một bộ cờ chữ cái riêng
  (`e` ước tính, `p` sơ bộ, `b` đứt gãy chuỗi, `f` dự báo, `n` không đáng kể, `u` độ tin cậy
  thấp) đính kèm SAU giá trị chứ không thay giá trị.
  https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Flag
- **UN Statistical Yearbook**, "Symbols, abbreviations and conversion factors": PHÂN BIỆT RÕ
  "đúng bằng không" (dùng gạch ngang kiểu phương Tây) với "khác không nhưng dưới nửa đơn vị hiển
  thị cuối" (ký hiệu `<` riêng) - đây là định chế DUY NHẤT trong khảo sát này tách hai khái niệm
  mà nhiều bảng tài chính thông thường gộp làm một.
  http://data.un.org/_Docs/2015_Symbols,%20abbreviations%20and%20conversion%20factors.pdf
- **OECD**, Economic Outlook 1973, phụ lục thống kê: `..` không có dữ liệu, `0` cho nil/negligible
  (KHÔNG dùng gạch ngang cho số 0 như UN), `-` cho "irrelevant".
  https://www.oecd.org/content/dam/oecd/en/publications/reports/1973/07/oecd-economic-outlook-volume-1973-issue-1_g1g2369e/eco_outlook-v1973-1-en.pdf
- **Bảng comps ngân hàng đầu tư**: `NM` (not meaningful) khi EBITDA âm hoặc gần không làm
  multiple vô nghĩa, loại khỏi trung vị/trung bình của nhóm so sánh.
  https://www.lumovest.com/courses/valuation-multiples/lessons/not-meaningful-multiples/

### 1.2 Không định chế nào có đủ sáu mức, vì không định chế nào cần đủ sáu mức

Điểm mấu chốt rút ra: BIS/World Bank/OECD là NIÊN GIÁM VĨ MÔ, đối tượng đọc là nhà nghiên cứu
quen quy ước, và số ô trống trên mỗi trang rất lớn nên cần ký hiệu TỐI GIẢN (đếm chấm là đủ).
Báo cáo tài chính doanh nghiệp cho nhà đầu tư có ĐỘ RỦI RO NGỮ NGHĨA cao hơn nhiều lần: nhầm
"không áp dụng" thành "không công bố" có thể đổi thành kết luận "doanh nghiệp giấu số" hoàn toàn
sai. Vì vậy bảng ở `ABSENCE-TABLE.md` KHÔNG copy nguyên một định chế nào, mà lai ghép: mượn quy
ước đếm chấm của BIS cho hai mức tần suất cao/rủi ro thấp (không áp dụng, không công bố), mượn
nguyên tắc tách "bằng không" khỏi "dưới ngưỡng làm tròn" của UN nhưng đổi ký hiệu vì UN dùng gạch
ngang bị cấm trong repo này, và THÊM HẲN hai mức không định chế nào khảo sát có (chưa tới kỳ,
quá hạn) vì đây là vấn đề đặc thù của báo cáo DOANH NGHIỆP theo chu kỳ công bố, không phải vấn
đề của thống kê vĩ mô công bố theo lịch cố định.

### 1.3 Ràng buộc riêng của repo này làm mất đi quy ước phổ biến nhất

**Xung đột thật cần nói thẳng**: ký hiệu phổ biến nhất cho "đúng bằng không" trong xuất bản định
chế (UN, nhiều BCTC phương Tây) là gạch ngang en-dash (U+2013). Repo này CẤM en-dash tuyệt đối trong
mọi nội dung hiển thị. Đây không phải một lựa chọn có thể né bằng font khác - ký tự đó không
được xuất hiện. Giải pháp trong `ABSENCE-TABLE.md`: dùng chính chữ số "0" cho "đúng bằng không"
(giống OECD 1973, nhưng trong bối cảnh khác lý do khác - OECD dùng "0" vì họ ĐÃ dành gạch ngang
cho nghĩa khác "irrelevant", ở đây dùng "0" vì KHÔNG được dùng gạch ngang cho bất cứ nghĩa nào). Số
"0" có ưu điểm phụ: nó tự đọc được ngay không cần chú giải, vì nó LÀ một con số bình thường.

### 1.4 Một loại vắng mặt thứ bảy, nằm ngoài sáu loại gốc, ghi nhận trung thực thay vì ép vào

Trong lúc dựng `samples/empty-trang-thai-rong-toan-phan.html` gặp một tình huống không khớp
gọn vào sáu hàng: chỉ số P/E trượt bốn quý (TTM) của một doanh nghiệp mới niêm yết hai quý.
Từng quý ĐÃ công bố đầy đủ, đúng hạn - không phải "không công bố", không phải "chưa tới kỳ" (kỳ
đã qua), không phải "không áp dụng" (chỉ số này áp dụng được, chỉ là chưa đủ input). Đây là một
loại thứ bảy: **vắng mặt vì độ sâu lịch sử chưa đủ cho một PHÉP TÍNH PHÁI SINH cần nhiều kỳ liên
tục**, khác hẳn vắng mặt vì thiếu MỘT quan sát thô. Không ép vào bảng sáu hàng cho gọn, vì ép vào
sẽ làm sai một trong hai: hoặc nói "chưa tới kỳ" (sai, đã qua kỳ), hoặc nói "không áp dụng" (sai,
chỉ số áp dụng được về sau). Cách xử lý trong mẫu: chuỗi chấm đếm được ●●○○ cộng câu giải thích
đầy đủ, xem mục 5.3.

**Khi nào ĐỪNG dùng cách phân biệt sáu-cộng-một này**: nếu tần suất gặp loại thứ bảy này thấp
(dưới một lần mỗi vài báo cáo), đừng thêm nó vào bảng ký hiệu chính thức làm bảng dài thêm một
hàng ai cũng phải học - xử lý bằng câu văn tại chỗ như mẫu đã làm là đủ, chỉ nên "chính thức hoá"
thành ký hiệu riêng nếu một loại báo cáo cụ thể (ví dụ báo cáo doanh nghiệp mới niêm yết) gặp nó
thường xuyên.

---

## 2. Ngưỡng: khi nào bảng thiếu quá nhiều thì đừng vẽ bảng nữa

**Quy tắc đề xuất, có cơ chế chứ không phải một con số tuỳ ý**: một CỘT mất khả năng so sánh khi
trạng thái PHỔ BIẾN NHẤT của nó là "không có dữ liệu" thay vì "có số" - tức tỷ lệ trống của cột
đó (không tính "chưa tới kỳ" vì đó là tạm thời, sẽ tự lấp khi cập nhật kỳ sau) vượt quá 50%. Dưới
mức đó, người đọc quét dọc cột gặp Ô TRỐNG NHIỀU HƠN Ô CÓ SỐ - bảng lúc này chủ yếu truyền tải
"cái gì thiếu" chứ không còn truyền tải "các con số này so sánh ra sao" nữa, và cách trình bày
đúng cho "cái gì thiếu" là MỘT CÂU VĂN hoặc một bản đồ độ phủ, không phải một bảng số dày đặc ký
hiệu trống.

**Ngưỡng cho TOÀN BẢNG**: khi phần lớn cột đều vượt ngưỡng 50% trên, bảng không còn đúng vai trò
một lưới so sánh hai chiều nữa. Ví dụ đúng ngay từ đề bài của vòng này ("một bảng 8 cột mà 5 cột
trống"): 5/8 = 62,5% cột trống, tức 37,5% lấp đầy nếu tính đều - dưới ngưỡng 50%, xác nhận trực
giác ban đầu bằng số học thay vì chỉ bằng cảm tính. Đã dựng lại đúng ví dụ này bằng số liệu cụ
thể trong `samples/empty-bang-sau-loai-vang-mat.html` (mục "Ngưỡng"): một bảng trộn chỉ tiêu
ngân hàng với doanh nghiệp phi ngân hàng có 15/35 ô lấp đầy ≈ 43%, dưới ngưỡng.

**Cách thay thế, không phải một cách duy nhất**:
1. Tách cột theo NHÓM ÁP DỤNG ĐƯỢC, dồn phần còn lại thành MỘT CÂU liệt kê ngoại lệ đặt ngay
   dưới bảng (đã làm trong mẫu, "chỉ 1/5 doanh nghiệp là ngân hàng nên bốn chỉ tiêu ngân hàng
   không đưa vào bảng chung, số của doanh nghiệp đó: ...").
2. Đổi trục: từ bảng-theo-đối-tượng sang hồ sơ-văn-bản-ngắn-theo-từng-đối-tượng (dùng trong
   `samples/empty-trang-thai-rong-toan-phan.html`).
3. Đổi thành bản đồ độ phủ (coverage map): chỉ hiện CÓ/KHÔNG CÓ dữ liệu bằng hai tông màu/hoạ
   tiết, không hiện giá trị, làm bước đệm trước khi trình bày số liệu chi tiết ở phụ lục.

**Đối chiếu với thực hành thật**: FactSet Earnings Insight công bố bảng KPI mùa báo cáo ngay khi
mới khoảng 60% doanh nghiệp S&P 500 đã báo cáo (trên ngưỡng 50% của quy tắc này), không đợi đủ
100%, nhưng LUÔN kèm một dòng tỷ lệ phủ và khái niệm "blended" tách bạch số đã báo cáo thật khỏi
số ước tính cho phần chưa báo cáo - khớp với cách 1 ở trên (giữ bảng, thêm lớp chú thích tách
bạch) chứ không phải cách 2 hay 3, vì ở mức phủ 60% bảng vẫn còn giữ được vai trò so sánh.
https://insight.factset.com/sp-500-earnings-season-update-july-31-2026

**Khi nào ĐỪNG áp dụng máy móc ngưỡng 50%**: một cột có tỷ lệ trống 55% nhưng TOÀN BỘ phần trống
đó là "chưa tới kỳ" (sẽ tự lấp trong một, hai kỳ tới) không nên bị loại khỏi bảng chính - loại
trừ "chưa tới kỳ" khỏi phép tính tỷ lệ trống trước khi so ngưỡng, đúng như đã làm ở
`samples/empty-bang-sau-loai-vang-mat.html` (dòng độ phủ ghi rõ "không tính 1 doanh nghiệp chưa
tới kỳ").

---

## 3. Chart có khoảng đứt dữ liệu: ba cách vẽ, một cách trung thực nhất

Ba biến thể render thật trong `samples/empty-chart-dut-gay-du-lieu.html`, cùng một bộ số.

### 3.1 Nối liền qua khoảng trống là nói dối bằng hình

Datawrapper Academy, "How to deal with missing data in line charts": khuyến nghị GIỮ khoảng
trống thật khi "không thể giả định dữ liệu phát triển liền mạch giữa hai điểm", và cảnh báo nối
liền khoảng trống lớn "có thể chứa ngoại lệ mạnh, gây sai lệch trực quan hoá".
https://www.datawrapper.de/academy/patchy-data

Nối liền tự động (WeasyPrint/trình duyệt nội suy tuyến tính giữa hai điểm có thật) vẽ ra một
đường không dựa trên bất kỳ phép đo nào ở giữa - nguy hiểm hơn một ô trống trong bảng, vì bảng
trống ít nhất KHÔNG khẳng định gì, còn đường nối liền KHẲNG ĐỊNH một xu hướng cụ thể (ở đây:
tăng đều) mà không có bằng chứng nào chống lưng.

### 3.2 Nét đứt cho khoảng trống đụng độ trực tiếp với quy ước đã có của repo

**Đây là phát hiện quan trọng nhất của mục này, phải tách bạch rõ với vòng 2**: nét đứt trong
repo đã có nghĩa CỐ ĐỊNH là "số dự phóng của đơn vị phát hành" (xem
`research/06-source-notes/FINDINGS.md` mục 4 và `samples/source-bang-thuc-te-du-phong.html`).
Một khoảng đứt dữ liệu (ta không biết số thật vì không đo được) là một ý nghĩa KHÁC HẲN dự báo
(ta CÓ MỘT ước tính có phương pháp, chỉ là chưa thành sự thật). Dùng lại nét đứt cho khoảng đứt
sẽ đánh lừa đúng quy ước report vừa dựng ở vòng trước - người đọc quen "đường đứt nét = có ước
tính đằng sau" sẽ đọc nhầm một đoạn "không biết gì cả" thành "đây là dự báo của chúng tôi".

### 3.3 Trung thực nhất: ngắt đường thật, tô nhạt vùng, ghi nhãn - ba lớp độc lập

Liberty Street Economics (Ngân hàng Dự trữ Liên bang New York), "Seeing Through the Shutdown's
Missing Inflation Data": dùng nét liền cho số liệu thật, nét đứt cho dự báo, và RIÊNG MỘT DẢI
XÁM DỌC để đánh dấu giai đoạn hoàn toàn không có số liệu CPI/PCE do chính phủ đóng cửa - ba tín
hiệu thị giác cho ba ý nghĩa khác nhau, không gộp chung nét đứt.
https://libertystreeteconomics.newyorkfed.org/2026/02/seeing-through-the-shutdowns-missing-inflation-data/

Ba lớp tín hiệu độc lập trong mẫu đã dựng: (1) đường DỪNG HẲN, không có nét nào bắc qua vùng
thiếu; (2) nền vùng thiếu tô khác màu nền chart; (3) chữ giải thích ngắn nói rõ LÝ DO (đứt mạch
khảo sát, không phải "giá đứng yên" hay "giá bằng không"). Mất một lớp (ảnh in mờ không thấy nền
xám, hoặc cắt chữ vì chart nhỏ) vẫn còn hai lớp kia giữ đúng thông điệp.

**Khi nào ĐỪNG dùng cách này**:
- Khoảng trống chỉ MỘT điểm dữ liệu: tô cả vùng rộng phóng đại cảm giác "mất rất nhiều dữ liệu",
  dùng ký hiệu điểm rỗng tại đúng vị trí đó thay vì tô vùng.
- Vùng tô nhạt trùng màu với một khối chú thích khác (assumption box, callout) trong cùng trang:
  người đọc lẫn "vùng thiếu dữ liệu" với "đây là một ghi chú".
- Biểu đồ nhỏ dạng small multiples: nhãn chữ đầy đủ không đủ chỗ, giữ vùng tô nhạt, dời câu giải
  thích ra chú thích chung dưới cả nhóm biểu đồ.

---

## 4. So sánh hai đối tượng có độ dài chuỗi thời gian khác nhau

Rất hay gặp ở TTCK Việt Nam: doanh nghiệp niêm yết lâu năm so với doanh nghiệp mới IPO. Ba biến
thể trong `samples/empty-so-sanh-chuoi-dai-ngan.html`.

### 4.1 Bẫy chính: chỉ số hoá về một gốc xa hơn lịch sử thật của chuỗi ngắn

Ép chuỗi ngắn về cùng mốc gốc index với chuỗi dài đòi hỏi hoặc BỊA số trước khi doanh nghiệp tồn
tại trên sàn, hoặc (nhẹ tay hơn nhưng vẫn sai) giữ đường PHẲNG ở mốc gốc 100 trong toàn bộ giai
đoạn chưa niêm yết. Một đường phẳng dài đọc RA LÀ "không biến động", một phát biểu sai hoàn toàn
khác với "doanh nghiệp này chưa tồn tại trên sàn ở giai đoạn đó" - và về mặt thị giác, một đường
phẳng dài cạnh một đường dao động tạo ấn tượng ổn định mà doanh nghiệp mới chưa từng được kiểm
chứng qua thời gian đó.

Đây là cùng CƠ CHẾ lỗi với memory người dùng đã chốt "baseline phải rút TRONG nhóm"
(`feedback_baseline_must_be_drawn_inside_the_subgroup`) - ở đó là baseline thống kê rút từ quần
thể gộp làm phồng phương sai nhóm nhỏ, ở đây là mốc gốc index hoá rút từ lịch sử của chuỗi dài
hơn ép lên chuỗi ngắn. Cùng một bài học tổng quát: đơn vị đo lường (baseline, mốc gốc) phải luôn
đến từ ĐÚNG cái đang được đo, không mượn từ một tập lớn hơn bao trùm nó.

### 4.2 Hai cách thay thế, đánh đổi khác nhau - không có cách nào miễn phí

**Cách 1, thu hẹp về cửa sổ chung**: chỉ vẽ trong khoảng cả hai CÙNG tồn tại trên sàn. Mọi điểm
trên chart là so sánh công bằng, nhưng người đọc mất hoàn toàn bối cảnh dài hạn của doanh nghiệp
cũ. Đừng dùng nếu mục đích chính của trang là đánh giá ĐỘ BỀN dài hạn của doanh nghiệp cũ.

**Cách 2, hai khung trục X riêng cùng thang Y, vạch mốc sự kiện IPO**: giữ trọn lịch sử dài, chỉ
vẽ chuỗi ngắn từ đúng vạch mốc niêm yết. Vạch mốc dùng NÉT LIỀN MẢNH (không phải nét đứt, để
không đụng quy ước dự phóng của vòng 2; không phải vùng tô xám, để không đụng quy ước "khoảng
đứt dữ liệu" vừa dựng ở mục 3 CHÍNH TRONG VÒNG NÀY - ba ý nghĩa khác nhau, ba tín hiệu khác nhau,
không được phép trùng). Nhược điểm: mắt vẫn có xu hướng so ĐỘ DỐC hai đoạn dù trục X hai bên vạch
mốc phủ độ dài thời gian khác nhau - cần nói rõ trong lời văn đi kèm, không chỉ dựa vào hình.
Đừng dùng nếu báo cáo hướng tới so sánh ĐỊNH LƯỢNG chặt (hệ số tương quan, beta) giữa hai chuỗi.

### 4.3 Bảng số đi kèm: tái dùng đúng ký hiệu "không áp dụng", không phải "không công bố"

Giai đoạn trước ngày niêm yết trong bảng số liệu dùng ký hiệu "." (không áp dụng, hàng 3 của
`ABSENCE-TABLE.md`), KHÔNG dùng ".." (không công bố, hàng 4) - đây là một sự thật CẤU TRÚC
(doanh nghiệp chưa tồn tại công khai), không phải một lựa chọn công bố. Nhầm hai ký hiệu này ở
đúng tình huống so sánh chuỗi dài-ngắn là lỗi dễ gặp nhất khi áp bảng sáu hàng vào thực tế.

---

## 5. "Chưa tới kỳ" so với "đã tới kỳ mà chưa công bố": neo bằng luật thật, không neo bằng cảm giác

### 5.1 Mốc pháp lý cụ thể cho thị trường Việt Nam

Thông tư 96/2020/TT-BTC, Điều 14 (hướng dẫn công bố thông tin trên thị trường chứng khoán Việt
Nam, xác nhận qua WebFetch bản toàn văn, không suy diễn từ tóm tắt): công ty đại chúng quy mô
lớn phải công bố báo cáo tài chính QUÝ trong thời hạn **20 ngày** kể từ ngày kết thúc quý (**30
ngày** nếu là công ty mẹ hoặc có đơn vị kế toán trực thuộc); báo cáo tài chính BÁN NIÊN soát xét
trong **5 ngày** kể từ ngày tổ chức kiểm toán ký báo cáo soát xét nhưng không vượt quá **45
ngày** (**60 ngày** nếu là công ty mẹ/có đơn vị kế toán trực thuộc) kể từ ngày kết thúc kỳ.

Đây là mốc NEO ĐƯỢC, không phải một ước lượng cảm tính về "bao lâu thì gọi là trễ" - đúng tinh
thần luật đã chốt "số neo phải gắn định danh và nguồn". Ba trạng thái tách bạch theo đúng mốc
này: (a) kỳ báo cáo còn chưa kết thúc - trung tính tuyệt đối; (b) kỳ đã kết thúc, còn trong hạn
20/30/45/60 ngày - vẫn trung tính, đang chờ; (c) đã vượt hạn mà chưa có số - đây LÀ một tín hiệu.

### 5.2 Quá hạn công bố là một tín hiệu đủ phổ biến để cần cách trình bày riêng

VietnamPlus, "Firms ask for delay financial statements release": việc xin gia hạn công bố "xảy
ra hằng năm, hằng quý" ở TTCK Việt Nam, không phải trường hợp hiếm có thể gộp chung vào ô trống
thông thường.
https://en.vietnamplus.vn/firms-ask-for-delay-financial-statements-release-post167491.vnp

Vì đủ phổ biến, quá hạn công bố cần một Ô/THẺ RIÊNG ghi rõ: kỳ kết thúc, hạn công bố (kèm trích
dẫn điều khoản), ngày chốt báo cáo hiện tại, và số ngày đã quá hạn - xem thẻ "quá hạn" trong
`samples/empty-trang-thai-rong-toan-phan.html` và dòng "công bố quý này" viền vàng đồng trong
`samples/empty-bang-sau-loai-vang-mat.html`.

### 5.3 Màu sắc: quá hạn dùng `--warn`, không dùng `--neg`

Quyết định thiết kế quan trọng nhất của mục này: ô/thẻ quá hạn dùng viền `--warn` (vàng đồng),
KHÔNG dùng `--neg` (đỏ) hay dấu chấm than. Lý do: quá hạn công bố là một tín hiệu QUY TRÌNH cần
chú ý, chưa phải một kết luận xấu đã xác nhận về kết quả kinh doanh - dùng đỏ sẽ đánh đồng "trễ
nộp báo cáo" với "kết quả kinh doanh tệ", hai chuyện có tương quan thống kê (trễ công bố tương
quan với khả năng tin xấu cao hơn trung bình) nhưng KHÔNG phải quan hệ nhân quả chắc chắn cho
từng trường hợp cụ thể - dùng màu kết luận (`--neg`) cho một sự kiện mới chỉ là dấu hiệu cần theo
dõi sẽ khiến người đọc kết luận vội trước khi có báo cáo thật.

**Khi nào ĐỪNG dùng viền `--warn`**: mới quá hạn một, hai ngày do lệch múi giờ nộp hồ sơ hoặc độ
trễ xử lý hành chính của sàn - chỉ đánh dấu khi đã vượt mốc một khoảng đủ rõ (ví dụ quá 5 ngày
trở lên) để loại trừ sai số hành chính thông thường.

---

## 6. Ghi chú độ phủ dữ liệu: một dòng, không phải một rừng chú thích

**Nguyên tắc**: MỘT dòng mono, đặt ngay dưới bảng/thẻ, nói rõ bảng phủ bao nhiêu phần trăm mẫu
và LOẠI TRỪ RÕ những gì không tính vào mẫu số (ví dụ "chưa tới kỳ" không tính vào phần trăm
không công bố). Không lặp phần trăm phủ riêng cho từng ô, không đặt số chú thích lên từng con số
- đúng nguyên tắc đã có ở `research/06-source-notes/FINDINGS.md` mục 1.1 ("ngày chốt số liệu đặt
một lần ở đầu, không lặp ở từng con số"), áp dụng tương tự cho độ phủ.

**Khi độ phủ khác nhau ĐÁNG KỂ giữa các cột** (ví dụ một chỉ tiêu cũ có sẵn 100% mẫu, một chỉ
tiêu mới theo quy định gần đây chỉ có 60% mẫu): tách riêng phần trăm phủ theo TỪNG CỘT trong cùng
một dòng ghi chú, không gộp thành một con số trung bình vô nghĩa - xem dòng độ phủ trong
`samples/empty-bang-sau-loai-vang-mat.html` liệt kê ba mức phủ khác nhau cho ba cột khác nhau
trong cùng một câu.

**Đối chiếu thực hành**: FactSet Earnings Insight không đợi đủ 100% doanh nghiệp báo cáo mới
công bố, mà công bố ngay ở mức phủ một phần kèm dòng tỷ lệ phủ tường minh và khái niệm "blended"
tách bạch số thật khỏi số ước tính cho phần chưa báo cáo - một ví dụ thật về kỷ luật "nói rõ mẫu
là gì trước khi nói kết luận là gì", đúng cơ chế lỗi mà memory người dùng
`feedback_baseline_must_be_drawn_inside_the_subgroup` đã cảnh báo ở một bối cảnh khác (baseline
thống kê): kết luận rút ra từ một mẫu không đầy đủ phải nói rõ mẫu đó là gì, không ngầm định là
toàn bộ quần thể.
https://insight.factset.com/sp-500-earnings-season-update-july-31-2026

**Khi nào ĐỪNG cần dòng độ phủ riêng**: bảng có độ phủ 100% ở mọi cột (trường hợp phổ biến khi
báo cáo chỉ về MỘT doanh nghiệp, không phải so sánh nhiều doanh nghiệp) - lúc đó độ phủ là hiển
nhiên, thêm một dòng nói "phủ 100%" là thừa chữ không mang thông tin mới.

---

## Nguồn đã khảo sát, tổng hợp

- IMF, WEO Database, Assumptions and Data Conventions - https://www.imf.org/en/publications/weo/weo-database/assumptions-and-data-conventions
- World Bank, WDI, Data Not Available - https://datahelpdesk.worldbank.org/knowledgebase/topics/19285-data-not-available
- BIS, Conventions used in the BIS Quarterly Review - https://www.bis.org/publ/qtrpdf/conventions.htm
- Eurostat, Glossary: Flag - https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Flag
- UN Statistics Division, Symbols, abbreviations and conversion factors (2015) - http://data.un.org/_Docs/2015_Symbols,%20abbreviations%20and%20conversion%20factors.pdf
- OECD, Economic Outlook Volume 1973 Issue 1 - https://www.oecd.org/content/dam/oecd/en/publications/reports/1973/07/oecd-economic-outlook-volume-1973-issue-1_g1g2369e/eco_outlook-v1973-1-en.pdf
- Lumovest, Not-Meaningful Multiples - https://www.lumovest.com/courses/valuation-multiples/lessons/not-meaningful-multiples/
- Datawrapper Academy, How to deal with missing data in line charts - https://www.datawrapper.de/academy/patchy-data
- Liberty Street Economics (Ngân hàng Dự trữ Liên bang New York), Seeing Through the Shutdown's Missing Inflation Data - https://libertystreeteconomics.newyorkfed.org/2026/02/seeing-through-the-shutdowns-missing-inflation-data/
- FactSet Earnings Insight, S&P 500 Earnings Season Update (31/07/2026) - https://insight.factset.com/sp-500-earnings-season-update-july-31-2026
- Thông tư 96/2020/TT-BTC, Điều 14 - https://vanban.vcci.com.vn/thong-tu-962020tt-btc-huong-dan-cong-bo-thong-tin-tren-thi-truong-chung-khoan
- VietnamPlus, Firms ask for delay financial statements release - https://en.vietnamplus.vn/firms-ask-for-delay-financial-statements-release-post167491.vnp
