# Thiết kế báo cáo chuyên nghiệp và ấn phẩm định chế

Vòng nghiên cứu 02, phục vụ `HT-viz-rendering`. Đây là **thư viện tham khảo để lấy ý**, không phải
khuôn ép, đọc mindset ở `research/RESEARCH-LEDGER.md` trước khi áp bất cứ mục nào dưới đây.
Mỗi phát hiện tách bạch: nguồn, thủ pháp, tại sao hiệu quả, chuyển sang báo cáo tài chính
tiếng Việt thành gì, và khi nào KHÔNG nên dùng.

Repo đã có sẵn một số cấu kiện làm đúng tinh thần định chế (xem `components/catalog/`):
`20-source-badge-k-anchor.md` (badge 4 tier nguồn), `12-hairline-data-table.md` (bảng hairline),
`11-exec-qa.md` (khối hỏi-đáp điều hành). Hồ sơ này KHÔNG lặp lại các mục đó, nó bổ sung lớp
nằm NGOÀI những gì đã cataloged: kiến trúc toàn tài liệu, kỷ luật tiêu đề/headline, quy ước ký
hiệu ở tầng bảng/biểu, và ranh giới "khi nào hỏng".

---

## 1. Kiến trúc tài liệu

### F1.1, Front matter nặng ký hơn tỷ trọng trang của nó
**Nguồn**: World Bank, Global Economic Prospects (bán niên, tháng 1 và tháng 6), cấu trúc
Chương 1 Global outlook, Chương 2 Regional outlook, cộng chương phân tích chuyên đề.
https://thedocs.worldbank.org/en/doc/7ce50b5aa95bef66048680bba9926ec8-0050012026/original/GEP-Jan-2026.pdf
(chỉ đọc được mục lục/cấu trúc qua kết quả tìm kiếm, bản PDF đầy đủ không trích xuất được text
qua WebFetch, ghi nhận, không bịa nội dung bên trong).
**Thủ pháp**: Chương 1 (outlook toàn cầu) luôn đứng đầu và nhận tỷ trọng biên tập cao nhất dù
Chương 2 (khu vực) mới là phần dài nhất về số trang. Phần khu vực đóng vai trò tra cứu (depth),
phần toàn cầu đóng vai trò định hướng (narrative).
**Tại sao hiệu quả**: người đọc bận rộn chỉ cần Chương 1 để có lập trường; người cần số liệu khu
vực cụ thể tra thẳng vào Chương 2 mà không phải đọc tuần tự.
**Chuyển sang báo cáo tài chính VN**: báo cáo ngành/công ty nên mở bằng 1 trang "quan điểm chung"
(giống Chương 1) trước khi vào phần theo từng mảng kinh doanh/công ty con, không đảo ngược thứ
tự này dù phần chi tiết dài hơn nhiều lần.
**Khi nào KHÔNG nên dùng**: báo cáo ngắn (dưới khoảng 8 trang, một công ty một luận điểm) không
cần tách "outlook chung" và "chi tiết khu vực" thành hai tầng riêng, tầng hoá khi chỉ có một đối
tượng phân tích là thừa cấu trúc, làm báo cáo trông cồng kềnh hơn nội dung thật.

### F1.2, Phần tóm tắt là phần được đọc nhiều nhất, và cũng dễ bị lạm dụng nhất
**Nguồn**: giới thiệu về mục "Prospectus Summary" trong hồ sơ S-1 (IPO), tổng hợp từ FloQast,
IPOHub, geminIQ. https://www.floqast.com/blog/mastering-s-1-filing-requirements-in-your-pre-ipo-journey/
https://www.geminiq.com/blog/what-is-s-1
**Thủ pháp**: mục tóm tắt đầu hồ sơ IPO là phần "được đọc rộng nhất, nhiều khi là phần DUY NHẤT
nhà đầu tư đọc", nhưng đồng thời được mô tả thẳng là "phần được đánh bóng nhất và ít giá trị
phân tích nhất, vì số liệu được chọn lọc để phục vụ một câu chuyện."
**Tại sao hiệu quả (và tại sao nguy hiểm)**: đặt thông tin quan trọng nhất lên đầu là đúng
nguyên lý (xem BLUF ở mục 2), nhưng khi tổ chức phát hành tự chọn số để đưa lên đầu, nguyên lý
đúng bị lợi dụng thành công cụ PR. Đây là ví dụ mẫu KIẾN TRÚC đúng nhưng NỘI DUNG sai mục đích.
**Chuyển sang báo cáo tài chính VN**: học kiến trúc (đặt cái quan trọng nhất lên đầu), nhưng
gắn kỷ luật chọn số ngược lại, trang đầu phải chứa cả số bất lợi lẫn số có lợi nếu cả hai đều
trọng yếu cho quyết định, không chỉ chọn số làm đẹp câu chuyện.
**Khi nào KHÔNG nên dùng**: đừng lấy mục tóm tắt S-1 làm khuôn mẫu để bắt chước GIỌNG, giọng đó
là giọng bán hàng, ngược hoàn toàn với luật "cấm giọng dạy đời" theo hướng khác nhưng cùng họ
lỗi, thiên vị có chủ đích. Dùng nó như bài học phản diện, không phải hình mẫu.

### F1.3, Section divider là chi phí trang, chỉ trả khi tài liệu đủ dài
**Nguồn**: quy ước thiết kế annual report, "section divider là một double-page spread ở đầu mỗi
phần, giống trang tiêu đề chương"; heading/bảng/caption phải "dự đoán được" xuyên suốt để người
đọc không phải học lại layout ở mỗi phần. Tổng hợp Venngage, Zapier, Redokun.
https://venngage.com/blog/annual-report-format/ và https://redokun.com/blog/annual-report-design
**Thủ pháp**: trang ngăn chương tốn ít nhất nửa đến một trang A4 không chứa nội dung phân tích,
đổi lại người đọc luôn biết đang ở chương nào chỉ bằng cách lật nhanh gáy tài liệu.
**Tại sao hiệu quả**: trong tài liệu 40-100 trang, "định vị được mình đang ở đâu" là chi phí nhận
thức lớn hơn một trang giấy trắng.
**Chuyển sang báo cáo tài chính VN**: repo đã có mẫu nhẹ hơn cho việc này, `sec-no` cộng `op-num`
(số chương lớn góc phải) trong `_harvest/reference-kimi.html`, không cần cả trang trắng riêng.
Đây là lựa chọn ĐÚNG cho báo cáo cỡ vừa (10-30 trang), giữ tín hiệu định vị nhưng không trả phí
cả trang.
**Khi nào KHÔNG nên dùng**: trang ngăn chương toàn trang (kiểu double-page spread thật) chỉ đáng
dùng cho tài liệu multi-chương dài (báo cáo thường niên, sách trắng ngành), với một note ngắn
1 trang hay exec brief 4-6 trang, dùng nó là lãng phí không gian in.

---

## 2. Tóm tắt điều hành, hành động trước, không được lùi

### F2.1, Nguyên lý Kim tự tháp Minto: khẳng định trước, lập luận sau
**Nguồn**: Barbara Minto, cựu McKinsey, "The Pyramid Principle" (1985, bản nâng cấp 1996).
Tổng hợp qua slideworks.io, betterup.com, Wikipedia.
https://slideworks.io/resources/the-pyramid-principle-mckinsey-toolbox-with-examples và
https://en.wikipedia.org/wiki/Barbara_Minto
**Thủ pháp**: "Bạn nghĩ từ dưới lên, nhưng trình bày từ trên xuống." Câu đầu tiên là MỘT khẳng
định trung tâm (governing thought), mọi đoạn sau chỉ tồn tại để bảo vệ khẳng định đó, nhóm theo
MECE (không chồng lấn, không bỏ sót).
**Tại sao hiệu quả**: người đọc nắm được kết luận trong câu đầu tiên có quyền dừng đọc bất cứ
lúc nào mà không mất thông tin quyết định, mọi đoạn sau là tùy chọn, không phải bắt buộc.
**Chuyển sang báo cáo tài chính VN**: câu mở đầu exec brief phải là VERDICT ("NÊN/KHÔNG NÊN X,
vì Y"), không phải bối cảnh ("Trong quý qua, ngành..."). Đây chính là luật "action-first, cấm
recap" người dùng đã chốt, Minto là nguồn gốc học thuật của chính luật đó.
**Khi nào KHÔNG nên dùng**: khi đối tượng đọc là kiểm toán viên hoặc cơ quan quản lý cần được
dẫn qua phương pháp luận TRƯỚC khi chấp nhận một kết luận (họ cần tự kiểm tra logic, không chỉ
nhận kết quả), trong thể loại "biên bản phương pháp luận" hoặc "workpaper", trình bày bằng chứng
trước kết luận mới đúng, vì mục đích là để người đọc tự verify, không phải để họ hành động nhanh.

### F2.2, BLUF: kết luận nằm ở câu đầu tiên, không phải đoạn cuối
**Nguồn**: BLUF (Bottom Line Up Front), gốc quân đội Mỹ, Army Regulation 25-50 (1988), tái
khẳng định bởi chỉ thị của Tướng James Mattis năm 2017 yêu cầu mọi bản tóm tắt mở bằng khuyến
nghị và giới hạn slide phụ trợ vào một phụ lục backup duy nhất.
https://en.wikipedia.org/wiki/BLUF_(communication) và https://www.animalz.co/blog/bottom-line-up-front
**Thủ pháp**: quy tắc cứng, câu đầu tiên của MỌI văn bản (memo, briefing, email) là kết luận,
không phải bối cảnh. Chi tiết hỗ trợ đẩy hết xuống dưới hoặc ra phụ lục.
**Tại sao hiệu quả**: tôn trọng thời gian người đọc; đảm bảo thông điệp chính không bị bỏ lỡ nếu
người đọc chỉ đọc một câu; buộc người viết phải làm rõ quan điểm TRƯỚC khi thêm chi tiết, nếu
không rõ quan điểm thì không viết được câu đầu.
**Chuyển sang báo cáo tài chính VN**: kỷ luật "một phụ lục backup duy nhất" của Mattis chuyển
thẳng thành cấu trúc "thân bài chỉ kết luận cộng số trang tham chiếu, chi tiết dồn vào phụ lục",
tránh việc thân bài vừa dài vừa loãng vì nhét cả bảng chi tiết vào giữa luận điểm.
**Khi nào KHÔNG nên dùng**: nội bộ giữa các nhà phân tích khi đang TRANH LUẬN một giả định (chưa
chốt quan điểm), ép viết kết luận trước khi có kết luận thật sẽ tạo cảm giác chắc chắn giả tạo.
BLUF dành cho giao tiếp MỘT CHIỀU đã chốt quan điểm, không dành cho biên bản thảo luận đang mở.

### F2.3, Tiêu đề hành động (action title): đọc mỗi tiêu đề là đọc hết lập luận
**Nguồn**: kỹ thuật "action title" trong slide McKinsey/MBB, tổng hợp qua slideworks.io,
slidescience.co. https://slideworks.io/resources/how-to-write-action-titles-like-mckinsey và
https://slidescience.co/action-titles/
**Thủ pháp**: tiêu đề mỗi trang/mục là MỘT câu khẳng định định lượng ("Doanh thu quý 3 tăng 18%,
toàn bộ đến từ khách doanh nghiệp lớn"), không phải nhãn chủ đề ("Doanh thu quý 3"). Nếu chép
toàn bộ tiêu đề trong tài liệu ra một chỗ, chúng phải đọc liền mạch như một đoạn văn kể hết câu
chuyện.
**Tại sao hiệu quả**: người lướt chỉ đọc tiêu đề vẫn nắm được kết luận; tiêu đề buộc tác giả phải
có MỘT ý mỗi mục, không thể viết tiêu đề hành động cho một mục chưa rõ "so what" là gì.
**Chuyển sang báo cáo tài chính VN**: đây là mẫu H2 trong `_harvest/reference-kimi.html` đã làm
đúng ("16 tỷ USD một năm, 71,8% đã không đi qua ngân hàng", không phải "Tổng quan kiều hối").
Phát hiện ở đây là làm RÕ quy tắc ẩn đằng sau lựa chọn đó để áp dụng nhất quán cho mọi tiêu đề
mới, kể cả tiêu đề exhibit (xem mục 3).
**Khi nào KHÔNG nên dùng**: với số liệu còn nhiều bất định hoặc câu hỏi thật sự CHƯA có câu trả
lời (một kịch bản rủi ro mở, một giả thuyết chưa kiểm chứng), ép một "khẳng định" lên dữ liệu
mơ hồ là nói dối bằng hình thức. Khi đó tiêu đề mô tả trung tính ("Ba kịch bản tỷ giá cho 2027")
trung thực hơn một tiêu đề hành động giả tạo. Cũng đừng dùng cho MỌI exhibit phụ lục, 40 exhibit
phụ lục đều mang tiêu đề hô khẩu hiệu sẽ gây mệt và mất tác dụng nhấn.

### F2.4, Assertion-Evidence: câu khẳng định 8-14 từ, bằng chứng thay cho gạch đầu dòng
**Nguồn**: Michael Alley, Penn State, mô hình "Assertion-Evidence" cho trình bày khoa học kỹ
thuật. http://writing.engr.psu.edu/2005_alley_neeley.pdf và
https://www.ibiology.org/professional-development/power-point-slide-design/
**Thủ pháp**: mỗi trang có đúng MỘT câu khẳng định làm tiêu đề (khuyến nghị 8-14 từ), được minh
chứng bằng hình/biểu đồ/bảng ngắn, KHÔNG bằng danh sách gạch đầu dòng, vì gạch đầu dòng không
thể hiện được quan hệ giữa các ý.
**Tại sao hiệu quả**: gạch đầu dòng liệt kê ý ngang hàng giả tạo (mục thứ ba trông "bằng cấp" với
mục đầu dù không liên quan mức độ); bằng chứng trực quan buộc tác giả thể hiện ĐÚNG quan hệ thật
(nhân quả, so sánh, xu hướng) thay vì che giấu nó sau dấu chấm đầu dòng.
**Chuyển sang báo cáo tài chính VN**: khi một mục có xu hướng dữ liệu thật (ví dụ margin co lại
qua 4 quý), ưu tiên một câu khẳng định cộng một chart nhỏ hơn là 4 bullet liệt kê số liệu rời
rạc, chart thể hiện được ĐỘ DỐC mà bullet không thể hiện được.
**Khi nào KHÔNG nên dùng**: khi các ý THẬT SỰ độc lập, không có quan hệ trục nào giữa chúng (ví
dụ danh sách điều kiện tiên quyết pháp lý, mỗi điều một chủ thể khác nhau), ép chúng vào một
chart hoặc một câu khẳng định duy nhất sẽ bóp méo; danh sách gạch đầu dòng lúc đó trung thực hơn.

### F2.5, Giọng thư cổ đông: BLUF không có nghĩa là khô khan
**Nguồn**: thư cổ đông Berkshire Hathaway, Warren Buffett, tổng hợp qua matthewgutierrezwrites.com
và D&O Diary. https://www.matthewgutierrezwrites.com/blog/warren-buffetts-writing-style-a-masterclass-in-clarity-wit-and-persuasion
**Thủ pháp**: thư luôn nêu quan điểm sớm, nhưng viết như đang trả lời câu hỏi của MỘT người cụ
thể (Buffett tự nhận là viết cho em gái Bertie), câu ngắn, không thuật ngữ ngành, số liệu luôn
đi kèm NGỮ CẢNH ("gấp X lần Y quen thuộc") thay vì trình bày trần trụi.
**Tại sao hiệu quả**: hầu hết thư CEO thất bại theo một trong hai hướng đối lập, sáo rỗng
("chúng tôi tự hào...") hoặc nhồi thuật ngữ để tỏ ra uyên bác. Giọng "giải thích cho một người cụ
thể" tránh được cả hai cực.
**Chuyển sang báo cáo tài chính VN**: verdict đầu trang không cần viết cộc lốc kiểu điện tín,
viết như đang trả lời thẳng câu hỏi "vậy tôi nên làm gì" của một người đọc cụ thể, miễn câu đầu
vẫn là kết luận. Hai điều không loại trừ nhau: action-first là VỊ TRÍ của kết luận, không phải
lệnh cấm giọng văn có ngữ cảnh.
**Khi nào KHÔNG nên dùng**: cho một bản ghi nhớ định giá cần tính phòng vệ cao (đưa ra hội đồng
quyết định, có thể bị kiểm tra ngược), giọng thân mật kiểu "thư gửi em gái" có thể đọc thành
thiếu nghiêm cẩn trong bối cảnh cần mọi câu đều chịu được chất vấn logic. Dùng giọng này cho thể
loại "thư/letter", không dùng cho thân bài phân tích kỹ thuật.

---

## 3. Quy ước exhibit

### F3.1, Đánh số Exhibit liên tục xuyên suốt tài liệu, không reset theo chương
**Nguồn**: quan sát thực tế cách McKinsey Global Institute đánh số ("Exhibit 11", "Exhibit 18")
kèm dòng "SOURCE:" bên dưới, qua kết quả tìm kiếm gián tiếp (không tìm được style guide chính
thức công khai, McKinsey không công bố sổ tay nội bộ, ghi nhận giới hạn này). Suy ra tiếp từ
quy ước phổ biến trong xuất bản học thuật/định chế (số hình liên tục toàn tài liệu để một số
tham chiếu về sau không bị trùng, ví dụ "xem Exhibit 4" vẫn đúng dù người đọc đang ở chương 3).
**Thủ pháp**: số thứ tự hình/bảng KHÔNG gắn với chương (không phải "Hình 2.3"), mà chạy 1, 2, 3
suốt tài liệu.
**Tại sao hiệu quả**: cho phép tham chiếu chéo ("xem Exhibit 4") ở bất kỳ đâu trong tài liệu mà
không cần nói kèm số chương, giảm một lớp thông tin người đọc phải giữ trong đầu.
**Chuyển sang báo cáo tài chính VN**: dùng "Hình 1, Hình 2" và "Bảng 1, Bảng 2" là hai chuỗi số
độc lập chạy suốt tài liệu (không trộn chung một chuỗi, vì hình và bảng phục vụ mục đích tra cứu
khác nhau). Mẫu render: samples/report-exhibit-institutional.html.
**Khi nào KHÔNG nên dùng**: báo cáo modular được thiết kế để đọc từng phần độc lập, không theo
thứ tự (ví dụ bộ slide rời cho từng buổi họp khác nhau), đánh số liên tục toàn "tài liệu mẹ" vô
nghĩa vì không có "tài liệu mẹ" thống nhất; khi đó đánh số theo từng phần độc lập hợp lý hơn.

### F3.2, Đường nét đứt là dự phóng, đường liền là thực tế đã có
**Nguồn**: quy ước biểu đồ IMF World Economic Outlook, "đường liền thể hiện số liệu thực tế mới
nhất; đường nét đứt thể hiện số dự báo mới nhất." Tổng hợp qua kết quả tìm kiếm về WEO forecast
tracker (bd-econ.com) và trang "Assumptions and Data Conventions" của IMF.
https://www.imf.org/en/publications/weo/weo-database/assumptions-and-data-conventions
**Thủ pháp**: MỘT quy ước hình học duy nhất (kiểu nét, liền hoặc đứt) mã hoá "đã xảy ra" so với
"dự phóng" trên cùng một trục thời gian, không cần chú thích màu riêng.
**Tại sao hiệu quả**: người đọc phân biệt "sự thật" và "giả định" ngay từ hình dạng đường, không
phải đọc chú thích trước, quan trọng nhất là KHÔNG THỂ nhầm vì mã hoá nằm trên chính đường dữ
liệu, không phải ở màu (màu có thể bị bỏ lỡ khi in đen trắng, nét đứt/liền thì không).
**Chuyển sang báo cáo tài chính VN**: mọi chart có trục thời gian vắt qua kỳ dự phóng (doanh thu
2024-2027 dự phóng chẳng hạn) nên dùng đúng quy ước này, nét liền tới kỳ có BCTC kiểm toán, nét
đứt từ đó trở đi, kèm một điểm đánh dấu (vạch dọc mảnh) tại ranh giới ghi rõ "Dữ liệu chốt đến
Q_/20__". Đây là lớp bổ sung Ở TRÊN hệ 4-tier badge nguồn đã có (badge nói NGUỒN, nét đường nói
THỜI ĐIỂM), hai hệ không thay thế nhau. Mẫu render: samples/report-exhibit-institutional.html, Hình 1.
**Khi nào KHÔNG nên dùng**: khi TOÀN BỘ chuỗi số trên chart đều là dự phóng (không có đoạn thực
tế nào để so sánh), lúc đó vẽ toàn bộ bằng nét đứt là thừa, chỉ cần một dòng ghi chú "Toàn bộ số
liệu là dự phóng" là đủ, không cần mã hoá hình học cho một biến duy nhất.

### F3.3, Bảng ký hiệu chuẩn hoá dùng chung cho mọi bảng và biểu trong tài liệu
**Nguồn**: "Conventions used in the BIS Quarterly Review", trang quy ước chính thức của Ngân
hàng Thanh toán Quốc tế. https://www.bis.org/publ/qtrpdf/conventions.htm
**Thủ pháp**: một trang quy ước NGẮN, đặt riêng, liệt kê ký hiệu dùng xuyên suốt: e là ước tính,
ba chấm là không có số liệu, dấu chấm là không áp dụng, gạch ngang là bằng không hoặc không đáng
kể, lhs/rhs là trục trái/phải, cộng dòng "chênh lệch tổng số do làm tròn." Mọi bảng trong toàn ấn
phẩm dùng ĐÚNG bộ ký hiệu này, không tự chế ký hiệu mới cho từng bảng.
**Tại sao hiệu quả**: người đọc chỉ cần học một bộ ký hiệu MỘT LẦN cho cả tài liệu dài hàng chục
bảng, thay vì đọc lại chú thích ở mỗi bảng, giảm tải nhận thức tuyến tính theo số bảng.
**Chuyển sang báo cáo tài chính VN**: đưa một "Bảng ký hiệu" ngắn (5-7 dòng) vào trang nguồn và
phương pháp, tương tự trang "Nguồn và phương pháp" đã có trong `_harvest/reference-kimi.html`,
nhưng bổ sung phần ký hiệu hình thức (TT là thực tế, DP là dự phóng, ba chấm là không có số liệu,
gạch ngang là bằng 0) mà bản đó hiện CHƯA có (bản đó mới có phân hạng nguồn theo tier màu, chưa
có ký hiệu số học). Mẫu render: samples/report-exhibit-institutional.html, khối "Bảng ký hiệu
dùng chung".
**Khi nào KHÔNG nên dùng**: báo cáo chỉ có 1-2 bảng/biểu, lập hẳn một trang ký hiệu cho tài liệu
ngắn là đầu tư thừa; khi đó ghi ký hiệu ngay dưới bảng đó (footnote tại chỗ) là đủ và nhanh hơn
cho người đọc.

---

## 4. Bảng số liệu dày

### F4.1, Số căn phải và căn theo dấu thập phân, nhãn căn trái
**Nguồn**: tổng hợp thực hành chuẩn từ CreativePro ("The Path to Beautiful Tables"), Excel
Campus, Tech Accounting Pro. https://creativepro.com/the-path-to-beautiful-tables-part-iii-working-with-numbers/
và https://www.excelcampus.com/tips-shortcuts/formatting-battles/
**Thủ pháp**: cột số luôn căn phải (hoặc căn theo vị trí dấu thập phân nếu số có phần lẻ khác
độ dài nhau); cột nhãn/tên hạng mục luôn căn trái. Không trộn căn giữa trong bảng số liệu.
**Tại sao hiệu quả**: căn phải giúp mắt so sánh ĐỘ LỚN theo cột dọc (chữ số hàng đơn vị luôn
thẳng hàng), đây là thao tác người đọc bảng tài chính làm nhiều nhất, căn giữa phá vỡ hoàn toàn
khả năng đó.
**Chuyển sang báo cáo tài chính VN**: đã đúng trong table.dt hiện có (class num cộng font mono
tabular-nums), phát hiện ở đây là xác nhận lựa chọn đã chốt bằng nguồn ngoài, không phải thay
đổi gì. Mẫu render: samples/report-dense-data-table.html.
**Khi nào KHÔNG nên dùng**: cột chứa khoảng giá trị dạng chữ ("Thấp/Trung bình/Cao", "AAA/BB")
không phải số thuần, căn trái hoặc căn giữa cho cột định tính đó vẫn đúng, đừng ép mọi cột trong
bảng dùng chung một kiểu căn chỉ vì phần lớn cột là số.

### F4.2, Hai trường phái ký hiệu số âm, chọn theo thể loại tài liệu
**Nguồn**: tổng hợp thực hành kế toán chuẩn (ngoặc đơn cho số âm) từ Tech Accounting Pro.
https://blog.techaccountingpro.com/p/opinionated-guide-on-financial-statement
**Thủ pháp**: trường phái kế toán/BCTC dùng NGOẶC ĐƠN cho số âm, ví dụ (1.250), vì ngoặc dễ
kiểm tra tổng bằng mắt hơn dấu trừ (dễ phân biệt số bị trừ với số cộng khi quét nhanh một cột).
Trường phái phân tích/dashboard hiện đại dùng dấu trừ kèm MÀU (thường đỏ) vì màu là tín hiệu
nhanh hơn với người đọc màn hình.
**Tại sao hiệu quả**: ngoặc đơn không phụ thuộc màu, vẫn đọc đúng khi in đen trắng hoặc với
người mù màu; dấu trừ cộng màu nhanh hơn nhưng mất tác dụng khi in thiếu mực màu hoặc photocopy.
**Chuyển sang báo cáo tài chính VN**: vì token màu neg (đỏ carmine) đã chốt trong hệ thống và
mọi bảng đều xuất PDF màu (không phải đen trắng), khuyến nghị dùng dấu trừ cộng màu neg làm mặc
định cho bảng phân tích/dashboard, NHƯNG với bảng trình bày dạng "trích BCTC" (đối chiếu số báo
cáo tài chính kiểm toán), giữ ngoặc đơn để đúng NGUYÊN VĂN cách trình bày trong báo cáo tài chính
gốc, tránh gây cảm giác "diễn giải lại" số liệu đã kiểm toán. Mẫu render đối chiếu trực tiếp cả
hai trường phái trên cùng một trang: samples/report-dense-data-table.html (Bảng 1 dùng ngoặc
đơn, Bảng 2 dùng dấu trừ đỏ).
**Khi nào KHÔNG nên dùng**: đừng trộn cả hai trong CÙNG một bảng (một cột dùng ngoặc, cột khác
dùng dấu trừ), không nhất quán còn tệ hơn chọn sai trường phái.

### F4.3, Số 0 hiển thị bằng gạch ngang, không hiển thị bằng chữ số 0
**Nguồn**: quy ước BIS Quarterly Review (F3.3), gạch ngang là "nil or negligible".
**Thủ pháp**: khi giá trị bằng không hoặc không đáng kể, ô hiển thị một gạch ngang canh giữa
chiều cao dòng, không hiển thị số 0.
**Tại sao hiệu quả**: mắt quét cột số nhanh hơn khi giá trị "không có gì đáng chú ý" có tín hiệu
thị giác khác hẳn (một vạch ngắn) so với các số có nghĩa, số 0 lẫn vào các số khác, gạch ngang
thì nhảy ra ngay.
**Chuyển sang báo cáo tài chính VN**: áp dụng cho bảng có nhiều ô bằng 0 thật (ví dụ ma trận công
ty con theo mảng kinh doanh, phần lớn ô là 0 vì công ty không hoạt động ở mảng đó). Mẫu render:
samples/report-dense-data-table.html, dòng "Thu nhập khác, ròng" năm 2024.
**Khi nào KHÔNG nên dùng**: khi con số 0 tự nó là một PHÁT HIỆN đáng chú ý (ví dụ "nợ vay ngoại
tệ bằng 0, giảm từ 40% năm trước", bằng không là tin tốt cần nhấn), lúc đó hiện số 0 thật cùng
định dạng nhấn (đậm, badge) mạnh hơn một gạch ngang vô hình, vì gạch ngang có nghĩa "không đáng
để ý" trong khi ở đây "bằng không" chính là điều đáng để ý nhất trong hàng.

### F4.4, Dòng tổng: một gạch trên, gạch đôi dưới, chữ đậm
**Nguồn**: quy ước định dạng bảng tài chính chuẩn, Excel Campus.
https://www.excelcampus.com/tips-shortcuts/formatting-battles/
**Thủ pháp**: dòng tổng/tổng cộng có một đường kẻ mảnh phía trên (ngăn với các dòng thành phần)
và một đường kẻ đôi phía dưới (đóng bảng), chữ số in đậm.
**Tại sao hiệu quả**: hai lớp kẻ khác nhau (đơn/đôi) mã hoá hai vai trò khác nhau của cùng một
đường kẻ ngang, "ranh giới trước phép cộng" và "kết thúc bảng", không cần chữ hay màu.
**Chuyển sang báo cáo tài chính VN**: table.dt hiện tại đã có dòng "Tổng / bình quân" in đậm
(xem components/catalog/12-hairline-data-table.md) nhưng dùng MỘT kiểu viền hairline đồng nhất
cho mọi dòng, chưa phân biệt viền trên dòng tổng với viền các dòng khác. Có thể tăng cường: viền
trên dòng tổng dày hơn (khoảng 1,5px thay vì hairline mảnh) mà không cần thêm màu, vẫn giữ tinh
thần "gần phẳng" của hệ token đã chốt. Mẫu render đầy đủ hai lớp viền: samples/report-dense-data-table.html,
dòng "Lợi nhuận sau thuế".
**Khi nào KHÔNG nên dùng**: bảng không có phép cộng dọc thật sự (ví dụ bảng so sánh định tính
giữa các công ty, dòng cuối chỉ là "trung vị ngành" chứ không phải tổng số học của các dòng trên),
gắn kẻ đôi kiểu "dòng tổng" cho một dòng KHÔNG phải tổng sẽ đánh lừa người đọc rằng đó là một
phép cộng, trong khi thực chất là một thống kê khác (trung vị, trung bình có trọng số). Xem đối
chứng trực tiếp trong samples/report-dense-data-table.html, dòng "Trung vị ngành" cố tình KHÔNG
dùng viền đôi.

### F4.5, Cột năm dự phóng phải tự gắn nhãn ngay trên tiêu đề cột
**Nguồn**: quan sát quy ước phổ biến trong báo cáo phân tích cổ phiếu bên bán (ví dụ cách trình
bày bảng comps với các cột năm kèm hậu tố A, E, E). Không tìm được một tài liệu style-guide công
khai duy nhất mô tả quy ước này (các nhà môi giới không công bố sổ tay định dạng nội bộ), ghi
nhận đây là suy luận từ việc quan sát cấu trúc bảng phổ biến trong ngành research bên bán, không
phải trích dẫn trực tiếp một nguồn có URL, cần đối chiếu thêm nếu áp dụng ở mức "luật".
**Thủ pháp**: hậu tố một chữ cái ngay sau năm trong tiêu đề cột, A cho actual đã có báo cáo,
E cho estimate ước tính bên ngoài, F cho forecast dự phóng mô hình nội bộ.
**Tại sao hiệu quả**: người skim bảng không cần đọc chú thích cuối trang để biết cột nào là số
thật, cột nào là số suy đoán, tín hiệu nằm NGAY TẠI ĐIỂM NHÌN (tiêu đề cột), không phải ở footer
cách đó nửa trang.
**Chuyển sang báo cáo tài chính VN**: dùng TT (thực tế) và DP (dự phóng) làm hậu tố tiếng Việt
thay vì mượn ký tự tiếng Anh, giữ đúng tinh thần "gắn ngay tại điểm nhìn" nhưng không lai tạp
ngôn ngữ trong nhãn cột. Đây là lớp bổ sung cụ thể cho hệ 4-tier badge đã có: badge tốt cho việc
gắn nguồn ở cấp Ô hoặc cấp KHỐI, hậu tố cột tốt cho việc gắn tính chất ở cấp CỘT khi cả một cột
(không phải một ô lẻ) cùng một tính chất. Mẫu render: cả hai bảng trong
samples/report-dense-data-table.html dùng hậu tố này ở tiêu đề cột.
**Khi nào KHÔNG nên dùng**: khi TOÀN BỘ các cột trong bảng cùng một tính chất (toàn bộ là số
thực tế, hoặc toàn bộ là dự phóng), gắn hậu tố lặp lại trên mọi cột là nhiễu thị giác vô ích,
một dòng ghi chú chung phía trên bảng là đủ.

---

## 5. Kỷ luật nguồn và ghi chú

### F5.1, Ngày chốt số liệu khác ngày phát hành, phải ghi cả hai
**Nguồn**: quy ước IMF WEO, báo cáo công bố định kỳ (tháng 1, 4, 7, 10) luôn có một ngày CHỐT dữ
liệu đầu vào cho các dự báo, tách biệt khỏi ngày phát hành ấn phẩm. Tổng hợp qua trang xuất bản
WEO. https://www.imf.org/en/Publications/WEO
**Thủ pháp**: hai mốc thời gian riêng biệt luôn xuất hiện: "dữ liệu tính đến ngày X" và "công bố
ngày Y", với X luôn sớm hơn Y một khoảng cố định (thời gian biên tập/kiểm chứng).
**Tại sao hiệu quả**: một dự báo "lỗi thời" không phải vì sai, mà vì người đọc tưởng nó phản ánh
tình hình ĐẾN NGÀY HỌ ĐANG ĐỌC, tách hai mốc ngăn hiểu lầm này ngay từ đầu.
**Chuyển sang báo cáo tài chính VN**: colophon cuối tài liệu (đã có mẫu trong
`_harvest/reference-kimi.html`: biên soạn một ngày, dữ liệu truy xuất một ngày khác) nên tách rõ
hai dòng thay vì gộp một câu, đặc biệt quan trọng khi ngày biên soạn và ngày chốt số liệu CÁCH XA
nhau (ví dụ báo cáo hoàn thiện sau 2 tuần rà soát trong khi số liệu đã chốt từ đầu).
**Khi nào KHÔNG nên dùng**: bản nháp nội bộ lưu hành trong ngày (không phải ấn phẩm chính thức),
tách hai mốc thời gian cho một tài liệu sống chưa đầy 24 giờ là hình thức thừa; một dòng
timestamp là đủ.

### F5.2, Giả định phải neo tại đúng con số nó chi phối, không dồn hết ra phụ lục
**Nguồn**: khớp với nguyên lý chung của tài liệu định giá định chế (DCF, financial model), giả
định chính luôn xuất hiện ở gần bảng/chart mà nó ảnh hưởng trực tiếp, phụ lục chỉ chứa phần mở
rộng đầy đủ. Xác nhận chéo với hệ thống đã có sẵn trong repo: note-box với nhãn GIẢ ĐỊNH trong
components/components.css đã hiện thực đúng nguyên lý này.
**Thủ pháp**: một callout ngắn (2-3 dòng) đặt NGAY DƯỚI con số bị chi phối, nói rõ giả định nào
tạo ra con số đó, không phải một danh sách giả định gộp chung ở cuối tài liệu tách rời khỏi số.
**Tại sao hiệu quả**: người đọc không phải nhảy qua lại giữa số liệu và phụ lục giả định để biết
"con số này có đáng tin không", khoảng cách đọc bằng 0.
**Chuyển sang báo cáo tài chính VN**: repo đã làm đúng phần khung; phát hiện bổ sung ở đây là quy
tắc VỊ TRÍ, callout giả định phải nằm trong tầm mắt của con số nó chi phối (cùng cột, ngay dưới
hoặc ngay bên phải), không đặt callout giả định ở đầu trang rồi số liệu ở cuối trang.
**Khi nào KHÔNG nên dùng**: khi MỘT giả định chi phối HÀNG CHỤC con số rải khắp tài liệu (ví dụ
tỷ giá USD/VND giả định dùng xuyên suốt mọi bảng), lặp lại callout đó ở mọi vị trí là nhiễu; khi
đó nêu MỘT LẦN ở đầu tài liệu rồi không lặp lại là đúng hơn nêu tại từng chỗ.

### F5.3, Phân biệt "nguồn dữ liệu" và "chủ thể diễn giải" là hai dòng khác nhau
**Nguồn**: đối chiếu văn bản của chính `_harvest/reference-kimi.html` (đã đọc trực tiếp source,
dòng khoảng 1073-1076): số liệu chính thống được ưu tiên tuyệt đối; ước tính thị trường thương
mại luôn gắn cờ; mọi con số suy rộng đánh dấu derived. Đây là bằng chứng NỘI BỘ (không phải
nguồn ngoài) nhưng đáng ghi vì khớp đúng tinh thần phân hạng bằng chứng của BIS/IMF (số chính
thức trước, ước tính bên ngoài sau, suy luận nội bộ đánh dấu riêng).
**Thủ pháp**: ba lớp tách bạch, một là số CÔNG BỐ có văn bản/BCTC xác nhận, hai là số BÊN THỨ BA
ước tính (broker, tổ chức nghiên cứu), ba là số DẪN XUẤT (tự tính từ hai lớp trên, ví dụ
TAM/SAM/SOM).
**Tại sao hiệu quả**: ba lớp phản ánh đúng ba mức độ RỦI RO SAI, số công bố gần như không sai
(trừ gian lận), số bên thứ ba có thể sai theo phương pháp luận của họ, số dẫn xuất cộng dồn cả
hai loại rủi ro trên cộng thêm rủi ro mô hình.
**Chuyển sang báo cáo tài chính VN**: hệ 4-tier đã có (CÔNG BỐ, ƯỚC TÍNH, DỰ BÁO, NỘI BỘ trong
components/catalog/20-source-badge-k-anchor.md) ĐÃ đúng tinh thần này. Không có phát hiện mới cần
thêm, ghi lại đây để XÁC NHẬN bằng nguồn ngoài rằng lựa chọn đã chốt khớp với thực hành BIS/IMF,
không phải để đề xuất thay đổi.
**Khi nào KHÔNG nên dùng**: (áp dụng cho chính hệ 4-tier) đừng gắn tier cho những câu chữ không
phải số liệu (nhận định chủ quan, mô tả bối cảnh định tính), hệ tier được thiết kế cho GIÁ TRỊ
ĐO ĐƯỢC, gắn nó vào câu văn diễn giải sẽ làm loãng tín hiệu của chính hệ thống.

---

## 6. Tầng thông tin, một trang phục vụ hai tốc độ đọc

### F6.1, Ba nguồn độc lập hội tụ cùng một nguyên lý: tiêu đề mang hết nghĩa, phần thân mang bằng chứng
Ba dòng bằng chứng riêng biệt cùng khẳng định một nguyên lý:
- McKinsey action title (F2.3): đọc riêng tiêu đề đã đủ hiểu toàn bộ lập luận.
- Assertion-Evidence (F2.4): tiêu đề là câu khẳng định, thân trang là bằng chứng minh hoạ.
- Nghiên cứu về "structural skim" (tổng hợp qua các nguồn hướng dẫn đọc nhanh tài liệu dài):
  người đọc lướt chỉ cần vài phút vì họ "không đọc để hiểu sâu, mà để dựng bản đồ", và bản đồ đó
  gần như hoàn toàn dựa vào tiêu đề cộng câu mở đoạn.
**Thủ pháp chung**: tách vai trò rõ ràng, TIÊU ĐỀ (cộng dek một câu) phục vụ người đọc 20 giây;
THÂN TRANG (chart, bảng, footnote) phục vụ người đọc 10 phút. Cả hai cùng tồn tại trên MỘT trang,
không phải hai bản tài liệu khác nhau.
**Tại sao hiệu quả**: đây là cách duy nhất một tài liệu vừa ngắn gọn vừa đầy đủ cùng lúc, ngắn
gọn ở TẦNG ĐỌC, đầy đủ ở TẦNG BẰNG CHỨNG, không phải đánh đổi giữa hai đầu.
**Chuyển sang báo cáo tài chính VN**: mẫu op-text cộng H2 cộng dek trong
`_harvest/reference-kimi.html` đã đúng cấu trúc này. Phát hiện bổ sung: dek (câu giới thiệu in
nghiêng dưới H2) nên chính nó cũng tuân luật action-title, hiện tại một số dek trong file tham
chiếu vẫn thiên mô tả bối cảnh hơn là khẳng định định lượng, có thể siết chặt hơn ở lượt viết nội
dung tiếp theo (xem gợi ý trong "vùng chưa đụng tới" ở RESEARCH-LEDGER.md). Mẫu render minh hoạ
cả hai tầng cùng lúc: samples/report-exec-brief-action-first.html.
**Khi nào KHÔNG nên dùng**: mục lục, phụ lục tra cứu thuần (bảng dữ liệu thô, glossary), những
phần này ĐÚNG RA không cần "dek khẳng định", vì bản chất chúng là tra cứu chứ không phải lập
luận; gắn một câu khẳng định giả tạo lên đầu bảng tra cứu là thừa và có thể gây hiểu lầm rằng bảng
đó có MỘT kết luận duy nhất trong khi nó phục vụ nhiều câu hỏi khác nhau.

### F6.2, Nguyên tắc "một phụ lục backup": không lặp lại chi tiết, chỉ trỏ tới nó
**Nguồn**: chỉ thị Mattis 2017 (F2.2), giới hạn tài liệu hỗ trợ vào MỘT phụ lục backup duy nhất
đằng sau bản tóm tắt kết luận. https://en.wikipedia.org/wiki/BLUF_(communication)
**Thủ pháp**: thân bài không lặp lại bảng chi tiết ở dạng thu nhỏ, thay vào đó, một câu trỏ (ví
dụ "xem Bảng A3 để đối chiếu đầy đủ 12 công ty cùng ngành") kèm số trang hoặc mã tham chiếu.
**Tại sao hiệu quả**: tránh tình trạng phổ biến trong báo cáo dài, cùng một bảng xuất hiện hai
lần (một bản rút gọn trong thân bài, một bản đầy đủ trong phụ lục) khiến người đọc không biết nên
tin bản nào khi hai bản KHÔNG khớp nhau do cập nhật lệch thời điểm.
**Chuyển sang báo cáo tài chính VN**: mọi bảng dày (trên 12 hàng, đã có quy tắc "không dùng
hairline table quá 12 hàng" trong components/catalog/12-hairline-data-table.md) nên tồn tại ĐÚNG
MỘT LẦN trong phụ lục, thân bài chỉ giữ một bảng rút gọn 3-5 hàng trọng yếu nhất cộng câu trỏ tới
bản đầy đủ, không phải bản tóm tắt của cùng một bảng. Mẫu render minh hoạ câu trỏ chéo giữa hai
file mẫu: samples/report-dense-data-table.html trỏ sang samples/report-exhibit-institutional.html.
**Khi nào KHÔNG nên dùng**: báo cáo một trang (exec brief độc lập, không có phụ lục đính kèm),
"trỏ tới phụ lục" vô nghĩa khi không có phụ lục; trong thể loại này mọi bằng chứng cần thiết phải
nằm ngay trên trang đó.

---

## Bổ sung: mổ xẻ trực tiếp một vi phạm thật với bản sửa

Yêu cầu nghiên cứu đòi hỏi tìm cả mẫu tuân thủ lẫn mẫu vi phạm luật action-first, cấm recap.
Không tìm được một văn bản định chế công khai nào tiện trích dẫn nguyên văn để mổ xẻ (rủi ro bản
quyền và rủi ro chỉ đích danh một tổ chức cụ thể), nên đã dựng một cặp đối chứng theo đúng MẪU
HÌNH phổ biến của thể loại "thư mời họp cổ đông" (mở bằng bối cảnh năm, đề xuất thật giấu ở đoạn
ba, kết luận bằng ẩn dụ) đối chiếu câu đối câu với bản viết lại theo BLUF và Minto, chú thích
ngay bên cạnh mỗi đoạn dẫn về đúng phát hiện F nào ở trên. Xem
samples/report-verdict-vs-recap-teardown.html.

---

## Nguồn không truy cập được (ghi nhận, không bịa nội dung)

- IMF WEO Executive Summary PDF (tháng 4/2026): trả về lỗi 403 Forbidden qua WebFetch. Không
  trích dẫn nội dung bên trong; các phát hiện IMF ở trên chỉ dựa vào phần tóm tắt hiển thị công
  khai qua kết quả tìm kiếm và trang "Assumptions and Data Conventions" (fetch được).
- World Bank Global Economic Prospects, tháng 1/2026, bản PDF đầy đủ: tải được nhưng nội dung là
  luồng nhị phân nén (FlateDecode), WebFetch không giải mã được text, chỉ dùng được cấu trúc
  chương mục lấy từ mô tả gián tiếp qua tìm kiếm, KHÔNG trích dẫn câu chữ bên trong.
- Trang chính thức McKinsey Global Institute và Goldman Sachs Global Investment Research: không
  có style guide công khai mô tả quy tắc exhibit/report nội bộ, mọi phát hiện về hai tổ chức này
  ở trên đến từ quan sát VÍ DỤ thực tế (slide/report được bên thứ ba đăng lại) hoặc suy luận từ
  thực hành phổ biến, đã ghi rõ trong từng mục, không trình bày như trích dẫn chính thức.
- stripe.com/annual-updates: trả về 404 tại thời điểm truy cập (đường dẫn có thể đã đổi cấu
  trúc). Không đưa phát hiện riêng về thiết kế thư Stripe vào hồ sơ này vì không xác minh được
  trực tiếp, bỏ khỏi phạm vi thay vì suy diễn.
