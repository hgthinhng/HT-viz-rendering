# Tầng "wow": cái gì làm người đọc dừng lại

Mũi nghiên cứu này trả lời một câu duy nhất: cái gì làm một tài liệu tài chính khiến người ta
phải dừng lại và trầm trồ, và cái đó tái lập được đến đâu trong khuôn khổ in ấn cứng của repo
này (blur 0, không gauge/radar, bảng màu hẹp, dấu tiếng Việt).

**Đọc trước:** đây là thư viện để lấy ý, không phải khuôn ép. Mỗi mục dưới đây viết dưới dạng
canh bạc: đặt cược gì, thắng thì được gì, thua thì hỏng ra sao. Không có thủ pháp nào ở đây là
bắt buộc.

---

## 0. Một phát hiện đo được, không phải ý kiến: font Spectral hiện tại LỖI khi in dấu tiếng Việt

Trước khi bàn thẩm mỹ, phải nói phát hiện kỹ thuật này vì nó phá vỡ mọi kế hoạch "chữ to là hình
ảnh" nếu không né được. Repo dùng `design-system/fonts/fonts-embedded.css`, khai mỗi weight của
Spectral thành **hai khối `@font-face` trùng family/weight/style, chỉ khác `unicode-range`**
(một subset "vietnamese" phủ U+1EA0-1EF9 v.v., một subset "latin" phủ U+0000-00FF) - đúng kiểu
Google Fonts hay dùng để trình duyệt chỉ tải subset cần. Tôi test bằng WeasyPrint 69.0 (engine
PDF thật của repo, không phải Chromium) qua 4 file test độc lập cộng 1 file thật đã có sẵn trong
repo (`samples/report-exec-brief-action-first.html`, không phải do tôi tạo):

- Text qua `fonts-embedded.css`, mọi cỡ từ 17px (thân bài) tới 200px, mọi weight 400/600/700:
  chữ ra SAI HOÀN TOÀN kiểu lộn glyph, không phải mất dấu. "tưởng ổn nghệ kể" ra "tj í ng æn
  nght kv". File thật `report-exec-brief-action-first.html` render ra "TÓM TẮT ĐIỀU HÀNH" thành
  "TÓM T.T ĐI»U HÀNH" - không đọc được một câu nào đúng trên cả trang.
- Cùng câu chữ, `font-family: serif` (mặc định hệ thống, không dùng Spectral): ĐÚNG.
- Cùng câu chữ, `font-family: 'Noto Serif'` hoặc `'DejaVu Serif'` (một file duy nhất, KHÔNG
  chia `unicode-range`): ĐÚNG ở mọi cỡ đã test.

Kết luận: WeasyPrint không xử lý đúng việc chọn subset theo `unicode-range` khi có nhiều
`@font-face` trùng descriptor. Bug này **tàng hình khi QC bằng mắt trên trình duyệt** (Chromium
xử lý `unicode-range` đúng chuẩn) và chỉ lộ ra khi mở PDF thật xuất từ WeasyPrint - đúng loại
lỗi mà memory.md của repo gọi là "lọt lưới vì đo bằng phép đo mà kết quả có thể sai". Đã báo
việc này cho main qua SendMessage kèm ảnh chụp; **năm mẫu HTML của tôi ở mục dưới CỐ Ý không
dùng `fonts-embedded.css`**, dùng thẳng font-stack hệ thống có fallback Noto Serif/Georgia để
không tái sinh lỗi trong khi chờ vá gốc.

Hệ quả cho nghiên cứu "typography như hình ảnh" ở mục 3: bất kỳ thủ pháp phóng to chữ Việt nào
CHỈ có giá trị nếu pipeline in xuất đúng dấu trước đã. Đẹp trên bản nháp trình duyệt không phải
bằng chứng.

---

## 1. Trang mở đầu: cái gì khiến người ta muốn lật tiếp

**Nguồn:** Kinfolk magazine (white-space teardown, [Visual Journal Craft](https://visualjournalcraft.com/article/white-space-in-design)); nguyên tắc cover annual report ([JDJ Creative](https://jdjcreative.co.uk/report-cover-design-ideas/), [Ethical Agency](https://ethical-agency.com/how-to-create-stand-out-annual-report-cover-designs-2024/)); Pentagram Flatiron 23rd Street Partnership annual report ([Pentagram](https://www.pentagram.com/news/flatiron-23rd-street-partnership-2013-annual-report)).

**Quan sát:** Kinfolk không đặt ảnh giữa trang, mà đặt ảnh góc trên phải và một khối chữ góc dưới
trái, buộc mắt phải DI CHUYỂN qua khoảng trắng giữa hai điểm neo - khoảng trắng chủ động, không
phải khoảng trắng "chưa xong việc". Margin của Kinfolk lớn bất thường so với tạp chí cùng giá.
Pentagram cho Flatiron 23rd Street Partnership dùng một ảnh chụp từ trên cao duy nhất, tràn trang,
không chữ chen vào - bìa TRẢ LỜI một câu hỏi thị giác duy nhất, không cố nhồi thông điệp.

**Canh bạc:** bìa report tài chính thường bị hiểu là "logo + tên + ngày", đặc trưng bằng cách
lấp đầy để trông "đầy đủ thông tin". Đặt cược ngược lại: một con số hoặc một câu duy nhất, cỡ
chữ áp đảo, xung quanh là khoảng trắng thật (không phải margin mặc định của template) - khiến
trang trông như đã BIẾT trước điều gì đó quan trọng, mời người đọc xác minh bằng cách lật vào.

**Thắng:** người nhận cầm bản in lên, đọc một dòng, và tò mò đủ để không đặt xuống. Với báo cáo
gửi khách hàng tổ chức, đây là khác biệt giữa "một trong hai mươi báo cáo tuần này" và "cái này
đọc trước".

**Thua:** nếu khoảng trắng không có gì neo (không số, không câu đủ sắc), nó đọc thành "hết
mực" hoặc "lỗi layout" - đặc biệt nguy hiểm khi photocopy lại bản in, khoảng trắng lớn có thể
trông như trang trắng bị bỏ sót.

**Dấu hiệu rẻ tiền:** dùng khoảng trắng lớn nhưng KHÔNG có gì đáng để mắt dừng lại trong đó -
tức là bắt chước hình thức Kinfolk mà không có nội dung xứng đáng với sự tĩnh lặng đó. Whitespace
là phần thưởng cho một câu đã được chọn lọc kỹ, không phải cách che giấu việc chưa viết được câu
đó.

---

## 2. Khoảnh khắc phá nhịp: 40 trang đều đặn thì phá ở đâu

**Nguồn:** Wired magazine layout ([John Henley/Medium](https://john-henley.medium.com/wired-magazine-structure-system-form-41d7264b9b25)); Bloomberg Businessweek dưới thời Richard Turley ([Creative Bloq](https://www.creativebloq.com/inspiration/bloomberg-businessweek-a-masterclass-in-magazine-design-1233765), [Creative Review](https://www.creativereview.co.uk/bloomberg-businessweek-redesign/)).

**Quan sát:** Wired dùng lưới 10 cột nghiêm ngặt CHÍNH XÁC để có chỗ phá nó - pull quote tràn
cột, ảnh tràn lề, không ngại "vi phạm" lưới khi có lý do. Bloomberg Businessweek dưới Turley
được mô tả là "một lớp hỗn loạn phủ lên trên một khung lưới chính xác" - hỗn loạn đó không ngẫu
nhiên, nó luôn PHỤC VỤ kể chuyện (chữ bị cắt, phóng to, xoay) chứ không trang trí thuần.

**Canh bạc:** một báo cáo dài mà mọi trang đều "ngoan" (cùng layout, cùng cỡ chữ, cùng nhịp) thì
đến trang 15 người đọc đã lướt chứ không đọc. Chèn 1 trang tràn lề (một minh hoạ chiếm trọn
trang, một con số khổng lồ, một bảng xoay ngang) ở đúng chỗ có tin quan trọng nhất - đặt cược
rằng SỰ GIÁN ĐOẠN THỊ GIÁC == tín hiệu "dừng lại, cái này khác" cho não người đọc đang lướt.

**Thắng:** người đọc nhớ ĐÚNG trang có tin quan trọng nhất, vì mắt bị buộc dừng ở đó. Đây là kỹ
thuật rẻ tiền nhất về công sức, đắt nhất về hiệu quả trong toàn bộ nghiên cứu này.

**Thua:** nếu phá nhịp ở một trang không có gì đặc biệt (chỉ vì "cho đẹp"), lần phá nhịp THẬT sự
sau đó mất tác dụng - não người đọc đã học được là trang lạ không có nghĩa gì. Ngân sách phá
nhịp trong một báo cáo 20-40 trang: tối đa 2-3 lần, đúng nghĩa "hiếm mới đáng chú ý".

**Dấu hiệu rẻ tiền:** phá nhịp ở TẤT CẢ các trang chương (biến "phá nhịp" thành khuôn mẫu lặp
lại), hoặc phá nhịp bằng cách đổi màu nền/thêm hoạ tiết trang trí thay vì đổi tỷ lệ thông tin
thật.

---

## 3. Typography như hình ảnh, và bẫy dấu tiếng Việt

**Nguồn:** Bloomberg Businessweek typographic illustration ([Fonts In Use](https://fontsinuse.com/uses/2360/bloomberg-businessweek-nov-5-11-2012-1), [Commercial Type](https://commercialtype.com/custom/bloomberg_businessweek)); vietnamesetypography.com (mục Diacritical Details, Design Challenges - truy cập bị chặn 403 khi WebFetch, ghi nhận qua kết quả tìm kiếm); phát hiện thực nghiệm của chính tôi ở mục 0.

**Quan sát:** Bloomberg Businessweek dùng Neue Haas Grotesk không chỉ để đọc mà để "cắt, kéo
giãn, biến thành minh hoạ" - chữ cái to đến mức người đọc nhận diện HÌNH TRƯỚC KHI đọc nghĩa.
Về tiếng Việt: theo vietnamesetypography.com, dấu thanh và dấu phụ của tiếng Việt XẾP CHỒNG lên
nhau (ví dụ ề, ổ - dấu mũ cộng dấu thanh), và với type hiển thị (display type), việc thiết kế
dấu "có thể phóng khoáng và thực nghiệm hơn" so với type đọc văn bản - nghĩa là chính ngành thiết
kế chữ Việt cũng coi cỡ lớn là một bài toán RIÊNG, không suy ra được từ cỡ đọc thường.

**Canh bạc kép, phải tách hai lớp:**

*Lớp kỹ thuật (đã đo, không phải phỏng đoán):* xem mục 0. Phóng to CHỮ tiếng Việt (không phải
chữ số) là canh bạc có xác suất hỏng cao hơn phóng to chữ số, vì (a) rủi ro font vỡ dấu như mục
0, và (b) ở cỡ cực lớn (trên khoảng 120-150px theo quan sát riêng, chưa có ngưỡng chuẩn hoá từ
nguồn ngoài), dấu mũ + dấu thanh xếp chồng có thể chạm vào dòng trên nếu line-height không đủ,
kể cả khi font render đúng.

*Lớp thẩm mỹ:* chữ SỐ (0-9, %, đơn vị) không có vấn đề dấu - đây là lý do thực dụng để ưu tiên
SỐ làm nhân vật chính của "typography như hình ảnh" trong repo tiếng Việt, thay vì một TỪ tiếng
Việt phóng to hết cỡ trang. Nếu bắt buộc phải phóng to một từ tiếng Việt, chọn từ ÍT dấu chồng
nhất có thể mà vẫn đúng nghĩa (ưu tiên từ có dấu sắc/huyền đơn thay vì dấu mũ + thanh kép như
"nghệ", "tưởng"), và luôn cộng thêm đệm phía trên dòng bằng khoảng đúng bằng chiều cao ước tính
của dấu (không suy diễn, đo bằng ảnh PDF thật xuất ra, đúng tinh thần "đo mực chữ" đã có trong
memory.md).

**Thắng:** một con số hoặc một từ ngắn phóng to đến mức chiếm cả tầm nhìn tạo hiệu ứng thị giác
ngay lập tức, không cần đọc câu xung quanh mới hiểu "quan trọng".

**Thua:** dấu bị cắt ở mép trên dòng (đọc được nhưng trông cẩu thả), hoặc tệ hơn, dính bug mục 0
và chữ ra sai hoàn toàn - với chữ CỠ NHỎ người đọc còn đoán được ý qua ngữ cảnh, với chữ phóng to
làm hình ảnh, một glyph sai là cả trang hỏng vì không có gì để đoán bù.

**Dấu hiệu rẻ tiền:** phóng to chữ tiếng Việt chỉ để "cho hoành tráng" mà không kiểm tra render
thật trong PDF xuất ra bằng WeasyPrint - xem đẹp trên trình duyệt rồi kết luận xong là chính xác
loại lỗi bị bắt ở mục 0.

---

## 4. Trang ngăn chương: vừa nghỉ mắt vừa tải thông tin

**Nguồn:** Wired feature divider ("chia bằng lề, cột rộng hơn hẳn" - [Riya Bobde/Medium](https://rbobde.medium.com/analyzing-wired-magazine-1f5665fefe7c)); nguyên tắc chapter opener sách ([The Book Designer](https://www.thebookdesigner.com/book-design-chapter-openers-part-openers/)).

**Quan sát:** trang ngăn chương tốt nhất trong xuất bản KHÔNG trắng trơn (lãng phí một trang) và
KHÔNG nhồi nhét (thì không còn là chỗ nghỉ mắt nữa). Wired dùng lề rộng bất thường và cột văn bản
hẹp hơn ở trang mở chương - tín hiệu "chậm lại" bằng NHỊP ĐỌC, không phải bằng để trống.

**Canh bạc:** biến trang ngăn chương thành "trang tóm tắt trước" - tên chương, một câu định vị
(không phải mục lục chi tiết), và 1-2 con số neo cho cả chương sắp tới. Đặt cược người đọc sẽ
nhớ RÕ tên chương và số neo đó hơn nếu nó đứng một mình trên một trang, so với nếu nhét chung vào
đầu trang nội dung.

**Thắng:** người đọc lướt nhanh, dùng các trang ngăn chương như một dạng "mục lục mở rộng" để
quyết định đọc kỹ chương nào - hành vi thật của người đọc báo cáo dài, họ hiếm khi đọc tuyến
tính.

**Thua:** nếu số neo trên trang ngăn không xuất hiện lại nhất quán trong chương (không được nhắc
lại khi nó xuất hiện thật), trang ngăn trở thành lời hứa suông, gây mất niềm tin vào phần còn lại
của tài liệu.

**Dấu hiệu rẻ tiền:** trang ngăn chỉ có số thứ tự và tên chương to đùng không có nội dung, đúng
kiểu "trang đệm PowerPoint" - chiếm diện tích in mà không trả lại giá trị đọc.

---

## 5. Một con số kể một câu chuyện, không phải KPI dashboard

**Nguồn:** Nicholas Felton / Feltron Annual Report ([99% Invisible](https://99percentinvisible.org/episode/episode-31-the-feltron-annual-report/), [MoMA](https://www.moma.org/collection/works/145531)); Giorgia Lupi, "Data Humanism" ([Medium](https://medium.com/@giorgialupi/data-humanism-the-revolution-will-be-visualized-31486a30dbfb)); ví dụ Zopa annual report ("không tường chữ, không insight bị chôn, chỉ có số liệu tự nói" - tìm thấy qua DesignRush/Visme, không truy cập được bản gốc để trích dẫn trực tiếp).

**Quan sát:** Felton không bao giờ trình bày một con số trần trụi - mỗi số trong Feltron Annual
Report đi kèm NGỮ CẢNH đo lường tỉ mỉ (không phải "đã đi 40 chuyến bay" mà là so với năm trước,
so với tổng số ngày, so với một mốc cá nhân). Giorgia Lupi gọi triết lý ngược lại của
"data humanism" là phản đối cách trình bày dữ liệu như thể nó tự đủ nghĩa mà không cần con người
đứng sau nó.

**Canh bạc:** một trang chỉ có MỘT con số, cỡ chữ áp đảo, với đúng MỘT câu ngữ cảnh ở dưới (so
sánh, xu hướng, hoặc ngưỡng) - không nhãn phụ, không icon trang trí, không đồng hồ đo. Đặt cược
rằng việc TƯỚC BỎ mọi con số khác trên trang buộc người đọc phải dừng ở con số CÒN LẠI đủ lâu để
nhớ nó, thay vì lướt qua một dashboard 6 con số cùng lúc và không nhớ số nào.

**Thắng:** con số đó trở thành thứ người đọc kể lại cho người khác ("báo cáo nói X đồng"), tức là
đã thắng ở tầng ghi nhớ, không chỉ tầng thông tin.

**Thua:** nếu con số không thực sự là con số quan trọng nhất của cả tài liệu (chọn sai con số để
tôn vinh), trang này biến thành phông chữ to vô nghĩa - người đọc nhớ ĐƯỢC con số nhưng nhớ SAI
trọng tâm của báo cáo.

**Dấu hiệu rẻ tiền:** con số to kèm icon (mũi tên, đồng hồ, ngôi sao) và box bo tròn xung quanh -
đúng công thức "stat card" của dashboard SaaS giá rẻ. Con số kể chuyện thật không cần khung, không
cần icon; sức nặng đến từ CỠ CHỮ và KHOẢNG TRẮNG xung quanh, không phải từ trang trí phụ trợ.

---

## 6. Sự tiết chế đắt tiền, và ranh giới với sự nhạt nhẽo

**Nguồn:** nguyên tắc thiết kế xa xỉ tối giản ([Letterhend Studio](https://www.letterhend.com/blog/knowledge/why-do-luxury-brands-choose-minimalist-fonts-the-secret-behind-visual-luxury/), [Kate Male](https://www.katemale.com/blog/luxury-branding-blind-spots/)); Pentagram cho Lloyd's of London ("thiết kế gọn khiến nó có thẩm quyền và dễ dùng... để sự thật đứng ở trung tâm" - [Pentagram](https://www.pentagram.com/work/lloyds-of-london) qua kết quả tìm kiếm, chưa fetch được trang gốc); Kinfolk (đã dẫn ở mục 1).

**Đây là câu hỏi quan trọng nhất của mũi nghiên cứu này.** Câu trả lời rút ra được từ đối chiếu
ba nguồn: **tiết chế đắt tiền = restraint có cấu trúc thay thế cho trang trí đã bị bỏ đi. Nhạt
nhẽo = restraint không có gì thay thế.**

Nguồn về thương hiệu xa xỉ nói thẳng: "một thương hiệu trông phẳng lặng khi nó bỏ chi tiết bề mặt
MÀ KHÔNG thay bằng cấu trúc, ý nghĩa, hoặc chủ đích" - restraint không tự nó là giá trị, nó chỉ
có giá trị khi thứ còn lại (bố cục, tỷ lệ, thứ tự đọc) được làm kỹ đến mức không cần trang trí để
che. Lloyd's of London theo Pentagram dùng bảng màu gần như đen-xám, chỉ một điểm nhấn cam - họ
không "làm ít hơn", họ CHUYỂN công sức từ trang trí sang HỆ THỐNG (thứ bậc chữ, căn lề số liệu,
nhất quán tuyệt đối).

**Canh bạc:** bỏ mọi yếu tố không phục vụ trực tiếp việc đọc (không border trang trí, không icon
minh hoạ cho vui, không màu thứ ba ngoài ink/accent), NHƯNG bù lại bằng kỷ luật tuyệt đối ở những
gì còn lại: căn lề số liệu chính xác đến từng cột, khoảng cách dòng nhất quán tuyệt đối, một hệ
thống cỡ chữ có tỷ lệ rõ ràng (repo đã chọn 1.333). Đặt cược rằng người đọc CẢM NHẬN được kỷ luật
đó dù không gọi tên được nó, và diễn giải cảm nhận đó thành "đáng tin, chuyên nghiệp".

**Thắng:** tài liệu trông như được làm bởi một tổ chức tự tin vào nội dung của mình, không cần
gồng lên bằng thị giác. Đây chính xác là hiệu ứng "quiet luxury" mà thương hiệu xa xỉ nhắm tới.

**Thua:** nếu kỷ luật ở phần còn lại KHÔNG đủ (căn lề lệch 2px, khoảng cách dòng không đều, một
bảng dùng font khác bảng kia), tiết chế không còn đọc là "chủ đích", nó đọc là "thiếu ngân sách"
hoặc "làm vội". Tiết chế chỉ đắt khi đi kèm bằng chứng nó là LỰA CHỌN, không phải THIẾU SÓT.

**Dấu hiệu nhận biết trong 3 giây:** nhìn vào lề trang và khoảng cách giữa các khối. Nếu chúng
đều bằng nhau tuyệt đối và bằng bội số của một đơn vị cơ sở (bằng mắt cũng nhận ra được sự lặp
lại có hệ thống), đó là tiết chế có chủ đích. Nếu khoảng trắng chỉ đơn giản là "còn dư chỗ", đó
là nhạt nhẽo.

---

## 7. Cái gì không chuyển được sang bản in, và thủ pháp thay thế

**Nguồn:** tổng hợp về scrollytelling ([Harvard Open Data Project](https://www.hodp.org/blog/scrollytelling/), [Shorthand](https://shorthand.com/the-craft/scrollytelling-examples/index.html)); Malofiej Awards doctrine về infographic báo chí in ([Wikipedia/Malofiej Awards](https://en.wikipedia.org/wiki/Malofiej_Awards), [SND-E](https://www.snd-e.com/en/malofiej/premios/2010)); Accurat studio, chuyển dữ liệu thành kể chuyện trên báo in ([Eye on Design/AIGA](https://eyeondesign.aiga.org/accurats-perfectly-imperfect-approach-to-data-visualization/)).

| Không chuyển được sang in | Vì sao | Thủ pháp in đạt HIỆU QUẢ TƯƠNG ĐƯƠNG |
|---|---|---|
| Scroll để lộ dần từng lớp dữ liệu (scrollytelling) | Không có "thời gian" trên giấy, mọi thứ hiện cùng lúc | Chuỗi hình nhỏ liên tiếp (small multiples) xếp ngang một dải trên cùng một trang, mắt tự "scroll" bằng cách đọc trái sang phải; đúng kỹ thuật báo chí in cổ điển mà Malofiej vẫn trao giải hàng năm cho thể loại tin breaking news |
| Hover để xem chú thích/tooltip | Không có sự kiện chuột trên giấy | Chú thích neo THẲNG vào đúng điểm trên hình bằng đường dẫn mảnh (leader line) và số thứ tự, đặt ngay cạnh thay vì ẩn đi - đây là ngôn ngữ chuẩn của infographic báo chí Malofiej, không phải giải pháp thay thế tạm bợ |
| Chuyển động nhấn mạnh (số đếm chạy, biểu đồ animate khi vào khung nhìn) | Giấy tĩnh tuyệt đối | Dùng TRỌNG LƯỢNG chữ và MÀU ink để dẫn mắt theo đúng thứ tự animation lẽ ra sẽ chạy - ví dụ nếu bản digital sẽ animate số tăng dần từ 0, bản in đặt số cuối to nhất kèm số gốc nhỏ hơn ngay cạnh với dấu mũi tên tĩnh, nói được "từ đâu đến đâu" trong một khung nhìn |
| Zoom/pan trên bản đồ hoặc biểu đồ lớn | Không có tương tác phóng to | Cắt sẵn 2-3 mức chi tiết (toàn cảnh + cận cảnh) đặt cạnh nhau trên cùng trang, đúng kỹ thuật "detail callout" báo in đã dùng từ trước khi có web |
| Dữ liệu cập nhật real-time | Bản in là ảnh chụp một thời điểm | Ghi rõ mốc thời gian chốt dữ liệu NGAY TRÊN hình (không phải ở footer), biến "tĩnh" thành một đặc điểm minh bạch thay vì một hạn chế phải giấu |

**Nhận định chung:** phần lớn hiệu ứng tương tác không mất giá trị khi in, chúng chỉ cần được
DỊCH sang một cơ chế thị giác tĩnh tương đương - đây chính xác là nghề mà infographic báo chí in
(Malofiej) đã làm hàng chục năm trước khi web tồn tại. Rủi ro thật không phải "không làm được",
mà là cố NHÁI hiệu ứng động bằng hình tĩnh (ví dụ vẽ mũi tên "loang" giả chuyển động) - cái đó rơi
vào đúng vùng AI-slop, xem ANTI-SLOP.md.

---

## 8. Tạo độ nổi không dùng blur, và một giới hạn còn nặng hơn: shadow không tồn tại

**Nguồn ban đầu (đã SAI một phần, xem sửa lại ngay dưới):** kỹ thuật letterpress/emboss bằng
`text-shadow` hai lớp ([Smashing Magazine](https://www.smashingmagazine.com/2012/07/letterpress-effect-fireworks-css/));
kỹ thuật xếp lớp box-shadow và inset shadow ([CSS-Tricks](https://css-tricks.com/getting-deep-into-shadows/)).

**ĐÍNH CHÍNH, kiểm bằng so ảnh mức byte (PNG xuất từ WeasyPrint qua cùng một trang, chỉ đổi
đúng một khai báo CSS mỗi lần, so `bytes` Python trực tiếp, không so bằng mắt):**
`box-shadow` và `text-shadow` **không tồn tại trong WeasyPrint 69.0 dưới bất kỳ cú pháp nào**,
kể cả offset cứng blur=0. Bốn phép so ảnh độc lập, mỗi phép giữ nguyên mọi thứ trừ đúng một
thuộc tính:

| Phép so | Biến thể A | Biến thể B | Kết quả |
|---|---|---|---|
| 1 | không có `box-shadow` | `box-shadow: 6px 6px 0 #C22F4E` | ảnh PNG giống hệt byte-for-byte |
| 2 | `box-shadow` màu hex | `box-shadow` màu `rgba(R,G,B,A)` dấu phẩy | giống hệt (cả hai đều = không có shadow) |
| 3 | `box-shadow` dấu phẩy | `box-shadow` màu `rgba(R G B / A)` khoảng trắng | giống hệt |
| 4 | `box-shadow` blur=0 | `box-shadow` blur=4px | giống hệt |
| 5 | không `text-shadow` | `text-shadow` hai lớp (công thức letterpress bên dưới) | giống hệt |
| 6 | `border-bottom` thường | thêm `box-shadow: inset 0 0 0 999px rgba(...)` ("veil") | giống hệt |

Ban đầu tôi kết luận SAI rằng cú pháp `rgba(R,G,B,A)` dấu phẩy "sửa" được vấn đề trong khi cú
pháp `rgba(R G B / A)` mới là thủ phạm, dựa trên so sánh BẰNG MẮT một ảnh chụp thu nhỏ. Team
lead phân xử lại bằng so ảnh mức byte và chỉ ra: cả hai cú pháp đều cho ảnh giống hệt bản
KHÔNG có shadow, tức là chính `box-shadow` (và `text-shadow`) không được WeasyPrint 69.0 vẽ ra
bất kỳ điểm ảnh nào, không liên quan tới cú pháp màu. Tôi tái hiện lại đúng phương pháp của họ
và xác nhận: kết luận của họ đúng, kết luận ban đầu của tôi sai. Bài học ghi vào phần "Luật
chung" cuối hồ sơ: **so một hiệu ứng thị giác phải so ảnh ở mức byte, không so bằng mắt** - một
viền `border` 1px và một shadow offset cứng blur=0 trông gần như nhau trên ảnh chụp thu nhỏ, mắt
không phân biệt được, byte thì phân biệt được ngay.

Quan sát về cú pháp `rgba(R G B / A)` bị bỏ qua khi dùng cho `color`/`background` THƯỜNG (không
liên quan `box-shadow`) thì **vẫn đúng, đã kiểm lại độc lập bằng đúng phương pháp so byte** (xem
mục 9), chỉ là nó không phải nguyên nhân của việc thiếu shadow - đó là hai lỗi khác nhau của
cùng một engine, tình cờ bị tôi gộp nhầm làm một trong bản nháp đầu.

**8.1 Hệ quả cho toàn bộ token shadow của repo.** `--shadow-1/2/3/hairline` trong `tokens.css`,
dù viết đúng cú pháp gì, đều KHÔNG render ra bất kỳ hiệu ứng gì trong PDF thật xuất từ
WeasyPrint. Bất kỳ component nào trong `components/` đang dựa vào các biến này để tạo cảm giác
"khối nổi" hiện đang render PHẲNG TUYỆT ĐỐI trên giấy, dù nhìn "có bóng" khi mở bằng Chromium.
Đây là khoảng cách kiểm chứng kinh điển: xem đẹp trên trình duyệt không phải bằng chứng cho PDF
thật, đúng tinh thần "verify output not just runs" đã có trong memory chung của người dùng.

**8.2 Vậy tạo độ nổi bằng gì, đã kiểm chứng render ra điểm ảnh thật.** Ba kỹ thuật dưới đây đều
đã so ảnh byte-level, xác nhận CÓ tạo ra khác biệt điểm ảnh thật so với bản không dùng:

- **Khối trùng lệch vị trí (offset duplicate).** Hai phần tử thật, không phải một phần tử có
  shadow: một khối/chữ nền tô màu nhạt (ví dụ `--line` hoặc `--paper-hi`) đặt `position: absolute`
  lệch 4-6px bằng `transform: translate()`, một khối/chữ chính đặt đè lên trên bằng `z-index`.
  Cả `transform` lẫn `background`/`color` đều đã xác nhận render đúng trong WeasyPrint (khác
  `box-shadow`). Hiệu ứng thị giác cuối cùng gần giống "letterpress" định làm ở 8 cũ, nhưng dựng
  từ hai phần tử THẬT thay vì một shadow ảo. Dùng được cho cả số liệu hero (chữ trùng lệch, màu
  nhạt phía sau) lẫn thẻ/chip (khối trùng lệch phía sau). Canh bạc: cần đúng 2 phần tử đồng bộ
  kích thước và font, sai lệch dù 1px cũng lộ ngay vì đây là hai lớp thật chứ không phải một hiệu
  ứng tự động. Thua: nếu nội dung động (độ dài số liệu thay đổi), phải đảm bảo cả hai lớp cùng
  cập nhật, dễ lệch khi sinh tự động từ template.
- **Border đặc thay cho shadow.** `border: 1px/2px solid var(--ink)` quanh một khối là cách rẻ
  nhất để phân định ranh giới khi không có shadow - không tạo cảm giác "nổi" thật nhưng tạo cảm
  giác "được đóng khung có chủ đích", khác hẳn việc không viền gì. Đây chính là lý do palette
  của repo vốn đã nghiêng về hairline border thay vì soft shadow, và giờ có thêm bằng chứng kỹ
  thuật ủng hộ hướng đó thay vì chỉ là gu thẩm mỹ.
- **Background-color khối thay cho "veil".** Ý tưởng "tô nổi một dòng trong bảng dày đặc mà
  không thêm biến màu mới" (8.2 bản cũ, dùng inset shadow) giờ làm trực tiếp bằng
  `background-color` thật (ví dụ `color-mix()` giữa `--warn` và `--paper`, hoặc một biến `-soft`
  đã có sẵn trong token thay vì bịa alpha mới) - đơn giản hơn, và quan trọng là THẬT SỰ render.

---

## Tổng kết ranh giới wow thật và wow rẻ tiền

Xem bảng đối chiếu đầy đủ ở `ANTI-SLOP.md`. Nguyên tắc gốc rút ra từ toàn bộ nghiên cứu trên: **wow
thật luôn TƯỚC BỎ trước khi PHÓNG ĐẠI** (Felton tước còn một số, Kinfolk tước còn hai điểm neo,
Lloyd's of London tước còn một màu nhấn); **wow rẻ tiền luôn CỘNG THÊM để che một quyết định
chưa đủ mạnh** (thêm icon vì con số chưa đủ ấn tượng, thêm màu vì bố cục chưa đủ rõ, thêm bo
tròn/gradient vì không dám để phẳng). Kiểm tra nhanh một thiết kế: nếu xoá bớt một yếu tố mà
thông điệp mạnh HƠN, yếu tố đó là rẻ tiền; nếu xoá đi thông điệp yếu hơn, yếu tố đó xứng đáng ở
lại.

**Nguyên tắc đo lường bổ sung sau vòng này:** khi đo một hiệu ứng thị giác trong PDF xuất từ
WeasyPrint, so ảnh ở mức byte (`pixmap.tobytes() == pixmap.tobytes()` hoặc md5), đừng so bằng
mắt trên ảnh chụp thu nhỏ. Một viền cứng và một shadow offset cứng blur=0 trông gần như nhau ở
kích thước nhỏ; mắt thường bị đánh lừa, phép so byte thì không.

---

## 9. Cú pháp màu CSS Color 4 dạng khoảng trắng/gạch chéo bị WeasyPrint bỏ qua (đã kiểm lại, tách riêng khỏi chuyện shadow)

**Xác nhận lại bằng so ảnh mức byte, độc lập với mục 8:** `rgba(R G B / A)` (CSS Color Level 4,
khoảng trắng và dấu gạch chéo, cú pháp `tokens.css` đang dùng cho toàn bộ `--shadow-1/2/3/hairline`)
khi gán cho `color` hoặc `background` (KHÔNG liên quan `box-shadow`, đã tách bạch sau khi đính
chính ở mục 8) bị WeasyPrint 69.0 bỏ qua âm thầm, property rớt về giá trị kế thừa/trong suốt. So
ảnh PNG cho hai trang chỉ khác đúng một khai báo:

- `color: rgba(5,28,44,0.9)` (dấu phẩy) → chữ ra đúng màu xanh đậm.
- `color: rgba(5 28 44 / 0.9)` (khoảng trắng/gạch chéo) → chữ ra màu đen mặc định, coi như
  khai báo không tồn tại.
- `background: rgba(34,81,255,0.15)` (dấu phẩy) → nền có màu xanh nhạt rõ ràng.
- `background: rgba(34 81 255 / 0.15)` (khoảng trắng/gạch chéo) → nền trong suốt, coi như
  khai báo không tồn tại.

Đây là một lỗi THẬT và ĐỘC LẬP với chuyện `box-shadow` ở mục 8 - hai phát hiện khác nhau của
cùng một engine, không nên gộp làm một (lỗi tôi từng mắc ở bản nháp đầu). Vì `--shadow-1/2/3/hairline`
trong `tokens.css` đang viết bằng đúng cú pháp khoảng trắng/gạch chéo này (cố ý, để né phép tách
`val.split(",")` trong `tests/consistency/tokens_test.py`, xem comment trong chính file đó), nên
dù có sửa lại cú pháp màu, token shadow VẪN sẽ không tạo ra hiệu ứng gì trong PDF (vì lý do ở
mục 8: bản thân `box-shadow` không tồn tại trong WeasyPrint, bất kể cú pháp màu). Nhưng lỗi cú
pháp màu này có thể ảnh hưởng tới bất kỳ chỗ nào KHÁC trong repo lỡ dùng `rgba(... / ...)` cho
`color` hoặc `background` thường ngoài phạm vi shadow - đáng để bên phụ trách `design-system/`
grep toàn repo tìm các chỗ dùng cú pháp này ngoài shadow.

Việc sửa `tokens.css`/`tokens_test.py` nằm ngoài quyền ghi file của agent nghiên cứu này (chỉ
được ghi `research/` và `samples/`), đã báo qua SendMessage cho main.
