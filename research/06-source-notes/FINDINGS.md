# Hệ thống chú nguồn và ghi chú cuối trang cho tài liệu tài chính

Vòng 2, vùng "Hệ thống chú nguồn và ghi chú cuối trang". Đọc `research/RESEARCH-LEDGER.md` mục
mindset trước khi dùng file này: mọi thủ pháp dưới đây là Ý THAM KHẢO, không phải khuôn ép.

Vòng 1 (`research/01-editorial/FINDINGS.md` mục 5) đã làm sidenote kiểu Tufte, pull-quote, và
neo số bằng màu tiết chế. File này KHÔNG lặp lại phần đó, mà đào sâu bốn hướng vòng 1 chưa chạm:
kỷ luật ghi nguồn của định chế phát hành số liệu vĩ mô, ma trận quyết định footnote/sidenote/
endnote (kèm phản biện chính Tufte), quy ước phân biệt thực tế với dự phóng bằng thị giác, và
ghi chú giả định mô hình định giá. Căng thẳng lộ nguồn được tách thành file riêng
`SOURCE-DISCLOSURE.md` vì nó là công cụ dùng hằng ngày, không phải một phát hiện đọc một lần.

---

## 1. Kỷ luật ghi nguồn của định chế phát hành số liệu vĩ mô

### 1.1 Ngày chốt số liệu đặt một lần ở đầu tài liệu, không lặp ở từng con số

Nguồn: IMF, "Assumptions and Data Conventions", World Economic Outlook — xác nhận qua tóm
tắt tìm kiếm (bản PDF gốc trả 403 khi fetch trực tiếp, không trích nguyên văn được, chỉ dùng nội
dung đã xác nhận qua nhiều kết quả tìm kiếm độc lập khớp nhau): mỗi kỳ WEO có một câu quy ước cố
định dạng "estimates and projections are based on statistical information available through
[ngày]", và với dữ liệu riêng từng nền kinh tế, người đọc được dẫn sang "date of last data
update" trong cơ sở dữ liệu trực tuyến thay vì nhắc lại ngày đó ở mọi bảng.

Thủ pháp: một câu chốt ngày duy nhất ở đầu tài liệu hoặc đầu mỗi bảng lớn, áp dụng cho toàn
bộ số liệu bên dưới, thay vì gắn "(cập nhật 06/08/2026)" vào sau từng con số riêng lẻ.

Tại sao hiệu quả: gắn ngày vào từng số làm trang rối và tạo ảo giác "mỗi số một độ tin cậy
khác nhau" trong khi thực ra cả bảng cùng một lần chốt dữ liệu. Một câu chốt ở đầu vừa đủ thông
tin để người đọc tính được độ trễ, vừa không phá nhịp đọc từng dòng.

Chuyển sang bối cảnh này: đặt ngay dưới tiêu đề báo cáo hoặc dưới mỗi bảng lớn một dòng
dạng "Số liệu chốt tới hết [ngày], các mốc sau đó là dự báo" bằng font mono, cỡ chữ chú thích,
màu ink nhạt. Nếu một bảng có vài con số chốt muộn hơn cả bảng (ví dụ một dòng cập
nhật realtime hơn), đánh dấu riêng dòng đó bằng ký hiệu hậu tố (xem 1.2), không viết lại cả câu
chốt ngày.

Khi nào ĐỪNG dùng: báo cáo có nhiều bảng với ngày chốt thực sự khác nhau đáng kể (ví dụ một
bảng dùng số liệu quý trước, bảng khác dùng số liệu tháng này) thì câu chốt ngày phải đặt riêng
cho từng bảng, gộp chung thành một câu ở đầu tài liệu sẽ đánh lừa người đọc về độ mới của bảng
cũ hơn.

### 1.2 Ký hiệu hậu tố một chữ cái thay vì nhắc lại chữ đầy đủ

Nguồn: World Bank, "Global Economic Prospects" — xác nhận qua tìm kiếm: quy ước dùng hậu tố
"e" (estimate) và "f" (forecast) đặt ngay sau con số hoặc ở đầu cột, thay vì viết "ước tính" hay
"dự báo" đầy đủ trong từng ô.

Thủ pháp: một chữ cái hậu tố nhỏ, thường đặt superscript hoặc trong ngoặc đơn nhỏ ngay sau
con số, giải nghĩa một lần ở chú thích cuối bảng ("e = ước tính", "d = dự báo").

Tại sao hiệu quả: bảng tài chính có hàng chục tới hàng trăm ô, viết "ước tính" hay "dự báo"
đầy đủ trong mỗi ô làm bảng đặc chữ và khó dò theo cột số. Một ký tự hậu tố giữ được tín hiệu
"đây là số suy ra chứ không phải số đo được" mà gần như không tốn diện tích.

Chuyển sang bối cảnh này: dùng hậu tố tiếng Việt viết tắt, ví dụ "d" cho dự báo, đặt trong
font mono cỡ nhỏ hơn số chính khoảng 2pt để không lẫn với số. Tránh trùng với "e" (dễ đọc
nhầm exponent trong ngữ cảnh tài chính có ký hiệu khoa học), và tránh trùng chữ cái đã dùng làm
đơn vị ("tr" cho tỷ, "%"). Xem mẫu source-bang-thuc-te-du-phong.html.

Khi nào ĐỪNG dùng: bảng chỉ có 1-2 ô là số dự báo trong khi phần còn lại là số thực tế thì
ký hiệu hậu tố lặp lại 1-2 lần trông vụn vặt hơn là ghi thẳng "(dự báo)" cạnh đúng ô đó. Ký hiệu
hậu tố chỉ đáng dùng khi số dự báo xuất hiện đủ nhiều lần để việc giải nghĩa một lần ở chú thích
thực sự tiết kiệm được diện tích.

### 1.3 Dòng nguồn liệt kê nhiều nguồn cộng "tính toán của [đơn vị]" cho số đã qua xử lý

Nguồn: BIS, "Annual Economic Report" — xác nhận qua tìm kiếm, mẫu câu điển hình dạng
"Sources: International Labour Organization; IMF; OECD; Bloomberg; Consensus Economics;
Datastream; BIS calculations".

Thủ pháp: một dòng nguồn liệt kê tất cả nguồn dữ liệu thô đã dùng, kết thúc bằng "[tên đơn
vị] calculations" nếu số liệu hiển thị đã qua xử lý (tính tỷ lệ, quy đổi chỉ số, gộp trung bình)
chứ không phải số thô lấy nguyên từ một nguồn.

Tại sao hiệu quả: phân tách rõ "lấy dữ liệu từ đâu" và "tính ra số này bằng cách nào" là hai
câu hỏi khác nhau của người đọc định chế. Gộp chung thành một dòng "Nguồn: X" khi thực ra đã qua
xử lý sẽ khiến người đọc tưởng nhầm số hiển thị là số thô của X.

Chuyển sang bối cảnh này: đây chính là cơ chế giải căng thẳng lộ nguồn nội bộ, xem
SOURCE-DISCLOSURE.md. Với số liệu công khai (Tổng cục Thống kê, NHNN, báo cáo IR doanh
nghiệp), liệt kê nguyên tên. Với số đã qua mô hình/ước tính riêng, đóng bằng cụm trung tính
"ước tính của [đơn vị phát hành báo cáo]" thay vì tên hệ thống hay quy trình nội bộ cụ thể.

Khi nào ĐỪNG dùng: đừng liệt kê một chuỗi nguồn dài chỉ để trông có vẻ nghiêm túc nếu thực
ra chỉ dùng một nguồn duy nhất, liệt kê thừa nguồn không dùng tới là một dạng nguỵ tạo uy tín.

---

## 2. Footnote, sidenote, endnote: ma trận quyết định

Vòng 1 đã dựng sidenote kiểu Tufte (research/01-editorial/FINDINGS.md mục 5.1,
samples/editorial-tufte-sidenote-margin.html). Phần dưới đây bổ sung: phản biện chính lập
luận của Tufte, so sánh với footnote/endnote cổ điển, và một ma trận chọn theo tình huống thay
vì chọn theo gu thẩm mỹ.

### 2.1 Ba cơ chế, ba đánh đổi đo được

Nguồn: Fonts.com, "Footnotes and Endnotes"; Gwern, "Sidenotes In Web Design"
(gwern.net/sidenote); Tufte, "Sidenotes or footnotes or what?"
(edwardtufte.com/notebook/sidenotes-or-footnotes-or-what).

Footnote cuối trang: mắt phải rời văn bản, tìm chân trang, đọc, quay lại tìm đúng chỗ vừa
dừng, nhưng chi phí dàn trang thấp vì layout engine tự tính chỗ ngắt trang. Thắng khi chú thích
ngắn (dưới hai dòng), xuất hiện thưa (dưới ba tới bốn lần mỗi trang), và trang đã có bố cục một
cột cố định như bảng số liệu.

Sidenote lề phải: gần như không rời văn bản, chỉ liếc ngang, nhưng chi phí dàn trang cao vì
cần cột lề đủ rộng. Gwern ghi nhận sidenote "không giữ được trên khổ paperback hay điện thoại",
và mật độ cao thì các sidenote chồng lên nhau vì CSS tĩnh không tự dàn lại. Thắng khi đoạn văn
xuôi phân tích có một tới bốn chú thích rời rạc, khổ trang đủ rộng từ A4 trở lên, đúng thể loại
báo cáo của repo này.

Endnote cuối tài liệu: mắt phải lật hẳn sang phần khác của tài liệu, chi phí đọc cao nhất,
nhưng chi phí dàn trang thấp nhất vì không ảnh hưởng layout trang đang đọc. Thắng khi chú thích
dài (giải thích phương pháp luận, công thức, nguồn dữ liệu chi tiết nhiều dòng) mà nếu đặt chân
trang sẽ đẩy hết nội dung trang xuống.

Ba cơ chế không cạnh tranh nhau để chọn cái đẹp nhất, chúng phục vụ ba độ dài chú thích khác
nhau. Một báo cáo tốt thường dùng cả ba trong cùng tài liệu: sidenote cho ghi chú ngắn bên văn
xuôi phân tích, footnote cho chú giải một dòng ngay dưới bảng số liệu, endnote cho phụ lục
phương pháp luận định giá dài.

### 2.2 Phản biện chính lập luận của Tufte

Nguồn: Tufte, "Sidenotes or footnotes or what?" (trang thảo luận công khai, có phần bình
luận của người đọc); Gwern, "Sidenotes In Web Design".

Tufte lập luận sidenote tốt hơn vì mắt chỉ cần liếc khoé mắt thay vì nhảy trang. Nhưng chính
trang thảo luận của Tufte ghi nhận phản biện: người bình luận Alex Merz cho rằng đọc sidenote
"là một kỹ năng phải luyện", tức không miễn phí như Tufte ngụ ý, người đọc lần đầu gặp sidenote
dày đặc vẫn mất nhịp để học cách quét mắt đúng cách. Gwern bổ sung hai phản biện thực nghiệm:
sidenote tĩnh kiểu Tufte-CSS gặp khó khi số lượng chú thích nhiều hoặc chú thích dài, xảy ra
chồng lấp không tránh được; nhiều trang web bắt chước Tufte nhưng lại bắt người đọc bấm để mở
rộng sidenote, tự triệt tiêu chính lợi thế không cần thao tác mà Tufte đề cao, lúc đó sidenote
thu gọn còn tệ hơn một link tới endnote thông thường.

Chuyển sang bối cảnh này: giữ đúng khuyến nghị đã có ở vòng 1 (sidenote cho một tới bốn ghi
chú mỗi trang, khổ A4 trở lên), nhưng bổ sung hai ràng buộc cứng hơn từ phản biện trên: sidenote
trong tài liệu tĩnh (PDF/HTML in) không được phép yêu cầu click để mở, nếu nội dung dài tới mức
phải thu gọn thì đó là dấu hiệu nó thuộc về endnote chứ không phải sidenote; không dùng sidenote
cho báo cáo mà độc giả mục tiêu đọc trên điện thoại là chính (bản tin ngắn, tóm tắt gửi Zalo),
nhóm này nên dùng neo số trong prose (mục 3) hoặc footnote thay vì sidenote.

Khi nào ĐỪNG dùng cả ba: nếu một con số chỉ cần một vế ngữ cảnh ngắn (ví dụ "18,4%, cao nhất
bốn quý gần nhất"), đừng phong nó thành chú thích riêng ở bất kỳ cơ chế nào, viết thẳng vào câu
văn xuôi là đủ. Chú thích chỉ đáng có khi thông tin đi kèm không thể nói gọn trong chính câu văn
mà không làm câu dài quá.

---

## 3. Neo số trong văn xuôi: đánh dấu để tra được mà không vỡ nhịp đọc

Nguồn: đối chiếu quy ước ký hiệu hậu tố của định chế (mục 1.2) với nguyên tắc trực tiếp,
không rời câu văn mà vòng 1 đã rút ra từ Economist chart style guide (research/01-editorial/
FINDINGS.md mục 5.3); bổ sung quy ước thứ tự ký hiệu chú thích cổ điển (dấu sao, dagger,
double-dagger), xác nhận qua nhiều nguồn kiểu-sách hội tụ (Fonts.com, PrintWiki, các hướng dẫn
văn phong khoa học).

Vấn đề cụ thể: một câu văn xuôi tài chính thường có hai tới bốn con số cùng lúc, nhưng không
phải số nào cũng cần tra nguồn, số đã nêu nguồn ở câu trước, số chỉ là phép cộng từ hai số khác
trong cùng đoạn, và số thực sự cần tra (vì lấy từ báo cáo bên ngoài, hoặc là số dự phóng riêng)
nên có ba mức đánh dấu khác nhau, không phải một mức đánh dấu cho mọi số.

Ba cấp neo, xếp từ nhẹ nhất tới nặng nhất:

Cấp một, không đánh dấu gì: số suy ra được ngay từ số liệu đã nêu trong cùng đoạn (ví dụ đã
nói doanh thu và giá vốn, biên lợi nhuận gộp là phép trừ, không cần neo riêng).

Cấp hai, gạch chân chấm mờ (underline dotted, màu ink nhạt, không dùng màu xanh kiểu
hyperlink web vì tài liệu này không phải trang web): tín hiệu "số này có nguồn cụ thể, xem chú
thích cuối bảng/cuối trang gần nhất" mà không cần một ký hiệu riêng chen vào giữa câu, giữ nhịp
đọc gần như nguyên vẹn.

Cấp ba, ký hiệu hậu tố nhỏ trong font mono (số thứ tự hoặc chữ cái, xem mục 1.2 và 2.2): dùng
khi số đó là số dự phóng hoặc số nội bộ cần phân biệt rõ với số đã công bố, tín hiệu mạnh hơn
gạch chân vì người đọc phải biết đây không phải số đo được, là số suy ra.

Tại sao ba cấp hiệu quả hơn một cấp: nếu mọi số neo giống nhau, người đọc mất khả năng phân
biệt "số này cần tra kỹ vì là dự phóng" với "số này chỉ cần biết nó có nguồn nhưng không quan
trọng bằng". Ba cấp giữ đúng nguyên lý đã có ở vòng 1 (mục 5.3: chỉ nhấn một tới hai số quan
trọng nhất đoạn) nhưng áp dụng cho việc neo nguồn thay vì nhấn luận điểm, đây là hai trục độc
lập, một số có thể vừa được nhấn màu vì là luận điểm chính, vừa mang ký hiệu hậu tố vì là số dự
phóng.

Quy ước thứ tự ký hiệu khi một đoạn có nhiều chú thích không dùng số thứ tự: dùng thứ tự cổ
điển dấu sao, dagger, double-dagger cho tối đa ba chú thích trong cùng một khối văn bản/bảng nhỏ
độc lập (ví dụ dưới một hộp giả định định giá), vượt quá ba thì chuyển sang số thứ tự
superscript, vì lặp ký hiệu (hai dấu sao, hai dagger) bắt đầu khó phân biệt bằng mắt thường ở cỡ
chữ nhỏ.

Chuyển sang bối cảnh này: xem mẫu source-neo-so-van-xuoi.html, trình bày song song ba cấp
trên cùng một đoạn văn thật để so sánh trực tiếp.

Khi nào ĐỪNG dùng: đừng áp cả ba cấp cho một bảng dày đặc số liệu (bảng đã có ký hiệu hậu tố
theo cột/theo dòng ở mục 1.2 là đủ, thêm gạch chân chấm cho từng ô sẽ chồng hai hệ thống đánh
dấu lên nhau và gây nhiễu thị giác nặng hơn là giúp ích).

---

## 4. Phân biệt thực tế với dự phóng bằng thị giác, còn rõ khi in đen trắng

Nguồn: quy ước phổ biến trong công cụ BI (SQLBI, "Showing actuals and forecasts in the same
chart with Power BI"; Peltier Tech, "Chart with Actual Solid Lines and Projected Dashed Lines");
storytellingwithdata.com, "when to use a dotted line"; đối chiếu ký hiệu hậu tố e/f của World
Bank (mục 1.2).

Thủ pháp theo ba loại thể hiện, một quy ước xuyên suốt cả ba:

Trong chart, đường/cột thực tế dùng nét liền, đường/cột dự phóng dùng nét đứt hoặc giảm độ
đặc (không giảm bằng độ trong suốt một mình, vì opacity một mình vẫn dựa vào màu và không phân
biệt được khi in đen trắng có độ tương phản thấp, kết hợp nét đứt là điều kiện cần).

Trong bảng, cột/dòng dự phóng dùng ký hiệu hậu tố (mục 1.2) cộng chữ nghiêng cho toàn bộ số
trong cột đó, chữ nghiêng là tín hiệu độc lập với màu, sống sót qua in đen trắng và cả photocopy
nhiều lần.

Trong văn xuôi, số dự phóng luôn có ký hiệu hậu tố (mục 1.2) đi kèm, không dựa vào màu sắc,
vì một câu văn nhấn màu cho số dự phóng dễ bị hiểu nhầm là nhấn luận điểm (mục 3) thay vì nhấn
trạng thái dự phóng, hai mục đích khác nhau không nên dùng chung một tín hiệu màu.

Tại sao hiệu quả: cả ba thủ pháp cùng một nguyên lý, dùng thuộc tính hình dạng (nét đứt, chữ
nghiêng, ký hiệu hậu tố) thay vì thuộc tính màu sắc làm tín hiệu phân biệt chính. Màu sắc là
kênh mã hoá yếu nhất khi in đen trắng, khi photocopy, hoặc với người đọc mù màu; hình dạng và
kiểu chữ sống sót qua mọi trường hợp đó. Đây cũng là lý do storytellingwithdata.com nhấn mạnh
nét đứt đã trở thành quy ước được công nhận rộng rãi, quy ước quen mắt tự nó là một dạng khả
năng tiếp cận, người đọc không cần đọc chú thích cũng đoán đúng ý nghĩa.

Chuyển sang bối cảnh này: xem mẫu source-bang-thuc-te-du-phong.html, kết hợp bảng (ký hiệu
hậu tố + chữ nghiêng) với biểu đồ mini SVG (nét liền/nét đứt) diễn giải cùng một chuỗi số liệu,
để chứng minh quy ước nhất quán xuyên suốt hai loại thể hiện.

Khi nào ĐỪNG dùng: đừng dùng chữ nghiêng cho toàn bộ một dòng nếu dòng đó có cả số thực tế
lẫn số dự phóng xen kẽ theo cột, lúc đó nghiêng phải áp theo từng ô, không áp theo dòng, nếu
không sẽ nghiêng nhầm cả số thực tế đứng cạnh số dự phóng. Cũng đừng dùng nét đứt cho đường
không phải dự báo (ví dụ đường trung bình động, đường mục tiêu) vì người đọc đã quen nét đứt là
dự phóng, dùng nét đứt cho ý nghĩa khác sẽ đánh lừa quy ước mà chính báo cáo này đang xây.

---

## 5. Ghi chú giả định của mô hình định giá

Nguồn: tổng hợp thực hành phổ biến trong tài liệu đào tạo định giá (Financial Edge Training,
Wall Street Mastermind, "DCF Sensitizing for Key Variables"/"DCF Sensitivity Analysis"), các
nguồn này mô tả thực hành chung của ngành, không phải văn bản gốc của một định chế cụ thể nên
được trích như thực hành phổ biến, không trích như tiêu chuẩn chính thức.

Thủ pháp hai lớp, tránh biến trang thành mê cung:

Lớp một, hộp giả định cô đọng: bốn tới sáu dòng, mỗi dòng là một giả định đầu vào (WACC,
tăng trưởng dài hạn, thuế suất, biên EBITDA dài hạn) với giá trị và một câu lý do ngắn tại sao
chọn giá trị đó, không giải thích cả công thức. Đây là thứ phần lớn người đọc chỉ cần liếc qua.

Lớp hai, bảng độ nhạy làm cơ chế tự kiểm: thay vì viết đoạn văn dài giải thích nếu WACC đổi
thì định giá đổi bao nhiêu, dùng một bảng lưới nhỏ (ví dụ năm hàng năm cột: hàng là WACC, cột là
tăng trưởng dài hạn, ô là định giá) để người đọc tự thấy độ nhạy mà không cần đọc thêm chữ. Tài
liệu đào tạo định giá gọi đây là cách làm hiện rõ trong một bảng duy nhất bao nhiêu phần bất
định của định giá đến từ đúng hai giả định đó.

Tại sao hiệu quả: câu hỏi thật của người đọc định giá không phải "giả định là gì" (đọc lướt
lớp một là đủ) mà là "nếu không tin giả định này thì kết quả lệch bao nhiêu", bảng độ nhạy trả
lời thẳng câu hỏi đó bằng chính cấu trúc bảng, không cần thêm một đoạn văn diễn giải dài. Đây là
lý do hai lớp không biến trang thành mê cung: lớp một là tra cứu nhanh, lớp hai là công cụ kiểm
chứng tự phục vụ, không có lớp thứ ba nào cần thêm.

Chuyển sang bối cảnh này: xem mẫu source-khoi-gia-dinh-dinh-gia.html. Bảng độ nhạy trình bày
bằng bảng HTML thường (không phải chart), vì đây là bảng tra cứu chính xác từng ô, không phải
minh hoạ xu hướng, dùng bảng giữ được số chính xác, dùng chart sẽ làm người đọc phải ước lượng
bằng mắt một con số đáng lẽ đọc thẳng được.

Khi nào ĐỪNG dùng bảng độ nhạy: nếu mô hình định giá chỉ nhạy với một biến (ví dụ chỉ WACC,
tăng trưởng dài hạn gần như cố định vì ngành bão hoà), một bảng lưới hai chiều là thừa, dùng một
dòng "định giá dao động từ X đến Y khi WACC đổi trong khoảng [a, b]" trong văn xuôi, ngắn gọn
hơn và không tạo cảm giác giả định thứ hai (tăng trưởng) quan trọng ngang giả định thứ nhất
trong khi thực ra không phải vậy.

---

## Kỹ thuật cân nhắc nhưng không đưa vào mẫu, ghi nhận để không ai thử lại

CSS Generated Content for Paged Media (float footnote): đây là cách đúng chuẩn nhất để tạo
chân trang tự động chảy theo layout engine, nhưng hỗ trợ của WeasyPrint cho thuộc tính này chưa
đủ ổn định để tin cậy trong repo yêu cầu round-trip PDF chính xác tuyệt đối. Các mẫu trong file
này mô phỏng chân trang bằng khối định vị cố định trong một khung trang có chiều cao xác định,
không dùng float footnote thật.

Sidenote JavaScript (sidenotes.js kiểu động): Gwern ghi nhận cách này giải quyết được vấn đề
chồng lấp khi mật độ cao, nhưng đòi hỏi JavaScript chạy để tính layout, trái với ràng buộc tự
chứa/không build step và không tin cậy khi xuất PDF tĩnh qua WeasyPrint (WeasyPrint không chạy
JavaScript).

## Nguồn đã thử nhưng không truy cập được đầy đủ, ghi nhận trung thực

IMF WEO "Statistical Appendix" và "Assumptions and Conventions" bản PDF gốc: imf.org trả về
HTTP 403 Forbidden khi fetch trực tiếp trong phiên này. Nội dung mục 1.1 dùng lại được nhờ tóm
tắt hội tụ từ nhiều kết quả tìm kiếm độc lập nhắc cùng một câu quy ước, nhưng không có trích
nguyên văn trực tiếp từ chính văn bản.

SSI Research và VNDIRECT: không tìm được bản PDF báo cáo phân tích cụ thể có thể đọc trực tiếp
quy ước ghi nguồn của họ qua tìm kiếm công khai trong phiên này (kết quả trả về là trang danh
mục sản phẩm, không phải nội dung báo cáo). Không dùng làm nguồn cho mục nào ở trên; toàn bộ suy
luận về ngữ cảnh Việt Nam trong file này là chuyển đổi của tôi từ các nguồn quốc tế đã đọc được,
không phải sao chép từ một báo cáo tiếng Việt thật.
