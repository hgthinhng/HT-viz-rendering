> [vn-humanizer reference — load khi SKILL.md trỏ tới. File dài: đọc mục lục/heading trước, nhảy tới mục cần.]

# VNH-1 — BẢN ĐỒ THỂ LOẠI (REGISTER MAP) VĂN VIẾT TIẾNG VIỆT CHO HUMANIZER ENGINE

Ngày lập: 2026-07-09. Phương pháp: web search EN+VN (giáo trình phong cách học, guide báo chí/SEO/email/brand-voice VN, tài liệu AI-detection EN+VN) + suy luận chuyên môn. Mỗi khối claim được đánh dấu **[SOURCED n]** (có nguồn, số trỏ về mục SOURCES cuối file) hoặc **[INFERRED]** (suy luận từ thực hành/quan sát, chưa có nguồn trực tiếp — cần treat như hypothesis có độ tin trung bình).

## 0. NGUYÊN LÝ CỐT LÕI: "AI-TELL LÀ TƯƠNG ĐỐI THEO REGISTER"

- Phong cách học tiếng Việt (Đinh Trọng Lạc – Nguyễn Thái Hòa, "Phong cách học tiếng Việt", 1994/2001) chia văn bản thành các **phong cách chức năng**: hành chính – công vụ, khoa học, báo chí – chính luận, sinh hoạt (khẩu ngữ), và ngôn ngữ nghệ thuật. Mỗi phong cách có chuẩn riêng về từ vựng, cú pháp, kết cấu. **[SOURCED 1,2,3]**
- Hệ quả cho humanizer: **một cụm từ/cấu trúc chỉ là "AI-tell" khi nó xuất hiện SAI phong cách**, hoặc khi nó xuất hiện ĐỀU TĂM TẮP bất kể phong cách. "Tóm lại" cuối luận văn = chuẩn mực; "Tóm lại" cuối caption bán hàng = chết. "Kính gửi" đầu email = bắt buộc; "Kính gửi" đầu blog tản văn = lố. **[INFERRED, nhất quán với 1,3,26]**
- AI (đặc biệt model chưa tinh chỉnh giọng) có **một register mặc định**: essay trung tính – lịch sự – đối xứng (mở–3 ý–kết), tránh viết tắt, tránh khẩu ngữ. Khi được yêu cầu viết register khác, nó "kéo" văn bản về register mặc định này → lỗi đặc trưng từng register ở mục 3. **[SOURCED 26,27,28,29 cho đặc điểm register mặc định; INFERRED cho cơ chế "kéo về"]**
- Vậy engine cần 3 lớp: (a) nhận diện register của văn bản (mục 4); (b) tra bảng chuẩn register đó (mục 2); (c) chỉ flag những gì lệch chuẩn CỦA register đó + các universal tell (mục 3.0).

## 1. NỀN LÝ THUYẾT → 8 REGISTER THỰC DỤNG

Mapping từ 5 phong cách chức năng giáo trình sang 8 register mà engine gặp trong thực tế:

| # | Register thực dụng | Gốc phong cách chức năng | Chức năng giao tiếp |
|---|---|---|---|
| R1 | Báo chí: tin + bài phân tích/bình luận | Báo chí – chính luận | Thông tin sự kiện / thuyết phục bằng lý lẽ |
| R2 | Học thuật / luận văn | Khoa học | Chứng minh, khái quát, khách quan |
| R3 | Content marketing / SEO | Báo chí lai quảng cáo | Kéo traffic + chuyển đổi |
| R4 | Mạng xã hội (FB post/caption) | Sinh hoạt (khẩu ngữ viết) | Tương tác, cảm xúc, bán hàng nhanh |
| R5 | Email công sở VN | Hành chính lai sinh hoạt | Trao đổi việc, giữ thể diện tôn ti |
| R6 | Báo cáo doanh nghiệp / tài chính | Hành chính – công vụ + khoa học | Trình cấp trên/cổ đông, số liệu |
| R7 | Blog cá nhân / tản văn | Nghệ thuật + sinh hoạt | Bộc lộ cái tôi, dư âm |
| R8 | Kỹ thuật / hướng dẫn | Khoa học ứng dụng | Làm theo được ngay |

Phong cách báo chí chuẩn giáo trình: 3 đặc trưng **tính thông tin sự kiện – tính ngắn gọn – tính hấp dẫn**; từ toàn dân, đa phong cách; câu rõ, khuôn cú pháp nhất định; bố cục logic dễ tiếp thu. **[SOURCED 3,4]**
Phong cách khoa học: **khái quát – logic – khách quan**, thuật ngữ chuyên môn, hạn chế ngôi thứ nhất. **[SOURCED 7,8]**
Phong cách hành chính – công vụ: **khuôn mẫu cao – minh xác (mỗi từ một nghĩa, không tu từ) – nghiêm túc khách quan**, ưa từ Hán-Việt trang trọng, kết cấu 3 phần cố định. **[SOURCED 24,25]**

## 2. HỒ SƠ TỪNG REGISTER

Chú thích thang "mật độ trang trọng" (formality): 1 = khẩu ngữ thuần → 5 = nghi thức hành chính. Thang này do tôi đặt **[INFERRED]**, các mô tả bên trong có đánh dấu nguồn riêng.

---
### R1a. BÁO CHÍ — TIN (news)

- **Kết cấu chuẩn**: Tít → sapo (chapeau, lời dẫn) → thân theo **kim tự tháp ngược** (quan trọng nhất lên đầu, cắt được từ dưới lên). Sapo trả lời ai–cái gì–khi nào–ở đâu–vì sao, KHÔNG lặp lại tít, không tóm hết bài (để người đọc còn đọc tiếp). **[SOURCED 4,5,6]**
- **Mở chuẩn**: vào thẳng sự kiện, thường mở bằng trạng ngữ thời gian/địa điểm: "Ngày 8/7, tại Hà Nội, ...", "Sáng 9/7, Công an tỉnh X cho biết...". **[SOURCED 4,6 cho nguyên tắc; INFERRED cho khuôn câu cụ thể]**
- **Kết chuẩn**: tin thuần KHÔNG có đoạn kết luận. Bài kết bằng chi tiết phụ, bối cảnh, hoặc câu trích của nhân vật — vì kim tự tháp ngược cho phép biên tập cắt đuôi. **[INFERRED từ logic kim tự tháp ngược, SOURCED 6 gián tiếp]**
- **Trang trọng**: 3/5. Khách quan, không "tôi". Nguồn dẫn qua "theo ông X", "trao đổi với phóng viên", chức danh + họ tên đầy đủ lần đầu.
- **Câu/đoạn**: câu ngắn–vừa (15–25 từ), đoạn 1–3 câu. **[SOURCED 3 "tính ngắn gọn"; con số INFERRED]**
- **Cụm HỢP LỆ riêng** (tell ở register khác): "Theo đó,", "Được biết,", "Liên quan đến vụ việc,", "trao đổi với PV", "thông tin từ...", "trước đó,". Các khuôn này là "khuôn mẫu cú pháp" hợp chuẩn báo chí. **[SOURCED 3; danh sách cụ thể INFERRED]**

### R1b. BÁO CHÍ — PHÂN TÍCH / BÌNH LUẬN

- **Kết cấu chuẩn**: "tam đoạn luận" báo chí: **luận đề → luận cứ → luận điểm**; nguyên tắc 5C+1N (Chủ đề, Chính kiến, Chính xác, Công bằng, Công tâm, Nhân văn) — bài bình luận PHẢI có chính kiến rõ. **[SOURCED 32,33]**
- **Mở chuẩn**: hook nêu nghịch lý/con số gây sốc/câu hỏi thời sự; được phép giọng cá nhân hơn tin.
- **Kết chuẩn**: chốt chính kiến, hoặc câu hỏi mở / trích dẫn đắt. "Tóm lại" chấp nhận được nhưng bị coi là non tay; cây bút giỏi kết bằng hình ảnh hoặc câu ngắn sắc. **[INFERRED]**
- **Trang trọng**: 3/5. "Tôi"/"chúng ta" dùng hạn chế, hợp lệ.
- **Câu**: dài ngắn xen kẽ có chủ đích; câu hỏi tu từ hợp lệ (khác R1a).

---
### R2. HỌC THUẬT / LUẬN VĂN

- **Chuẩn cốt lõi**: chính xác – rõ ràng – khách quan; trình bày luận cứ, phân tích, chứng minh, "tránh thể hiện tình cảm yêu ghét với đối tượng nghiên cứu"; tránh ngôi thứ nhất trừ khi cần; mọi luận điểm có trích dẫn/số liệu. **[SOURCED 7,8]**
- **Mở chuẩn**: dẫn nhập theo phễu: bối cảnh → tổng quan nghiên cứu trước → khoảng trống → mục tiêu + câu hỏi nghiên cứu. Khuôn "Trong những năm gần đây, ... đã trở thành vấn đề được quan tâm" là khuôn HỢP LỆ ở đây (dù mòn). **[SOURCED 8 cho cấu trúc; INFERRED cho khuôn câu]**
- **Kết chuẩn**: "Tóm lại"/"Kết luận" + tóm tắt kết quả + hạn chế nghiên cứu + hướng tiếp theo + khuyến nghị. Đây là register DUY NHẤT mà kết-tóm-tắt-đầy-đủ là bắt buộc. **[SOURCED 7,8,34]**
- **Trang trọng**: 4/5. Hán-Việt dày ("khảo sát", "tiến hành", "đề xuất"), danh hoá nhiều ("việc áp dụng...", "sự suy giảm...").
- **Câu**: dài, đa mệnh đề, câu bị động hợp lệ; đoạn 4–8 câu.
- **Cụm HỢP LỆ riêng**: "Nghiên cứu này nhằm...", "Kết quả cho thấy...", "Trên cơ sở đó,", "Có thể thấy rằng,", "Tóm lại,", "(Nguyễn, 2020)", "có ý nghĩa thống kê". Tất cả đều thành tell nếu rơi vào caption/email/blog.

---
### R3. CONTENT MARKETING / SEO

- **Kết cấu chuẩn (đã thành công nghiệp hoá)**: Title ≤ ~60 ký tự chứa keyword → mở bài (sapo) chứa keyword chính 1–2 lần ngay các câu đầu, nêu giá trị bài viết → H2/H3 chứa keyword phụ → mật độ keyword ~1–3% rải tự nhiên → kết bài 80–150 từ: tóm tắt + nhắc thương hiệu + call-to-action, có chứa keyword. Bài dài 1.500–2.000+ từ để cạnh tranh hạng. **[SOURCED 14,15,16]**
- **Mở chuẩn**: nêu pain point người đọc + hứa lợi ích: "Bạn đang loay hoay với X? Bài viết này sẽ...". Cụm "Trong bài viết này" HỢP LỆ ở R3 — nhưng là tell nếu xuất hiện ở R1/R4/R7. **[SOURCED 14 cho nguyên tắc; INFERRED cho tính register-relative]**
- **Kết chuẩn**: "Hy vọng bài viết đã giúp bạn...", CTA "liên hệ ngay/để lại bình luận". Là formula hợp lệ nhưng ĐÃ BÃO HOÀ — humanizer nên giữ chức năng, thay lời. **[SOURCED 14,15 cho formula; INFERRED cho khuyến nghị]**
- **Trang trọng**: 2.5/5. Xưng "bạn"; brand tự xưng tên riêng hoặc "chúng tôi". **[SOURCED 30,31]**
- **Câu**: vừa (12–20 từ), đoạn 2–4 câu để dễ đọc mobile; bullet + bảng hợp lệ.
- **Cụm HỢP LỆ riêng**: "Cùng tìm hiểu nhé", "Xem thêm:", "Lưu ngay", CTA trực tiếp, keyword lặp nguyên văn (ở register khác lặp nguyên cụm dài = vụng; ở SEO là kỹ thuật).

---
### R4. MẠNG XÃ HỘI (FB POST / CAPTION)

- **Kết cấu chuẩn**: công thức AIDA (Attention–Interest–Desire–Action) hoặc PAS (Problem–Agitation–Solution); **hook nằm ở 1–2 dòng đầu** (trước nút "Xem thêm"); caption ngắn gọn; 2–5 hashtag; emoji; kể chuyện mini. **[SOURCED 12,13]**
- **Mở chuẩn**: câu giật/câu hỏi/tình huống đời thường, thường KHÔNG đủ chủ-vị: "Hết cứu.", "Ai còn thức không?", "3 đêm mất ngủ chỉ vì...".  **[SOURCED 12,13 cho nguyên tắc hook; khuôn câu INFERRED]**
- **Kết chuẩn**: CTA tương tác ("Cmt 'GIÁ' để nhận báo giá", "Tag đứa bạn hay trễ deadline") hoặc punchline bỏ lửng. TUYỆT ĐỐI không "Tóm lại", không đoạn tổng kết.
- **Trang trọng**: 1/5. Xưng "mình/tụi mình/em/nhà X", gọi khách "bạn/nàng/các mom/cả nhà". Ví dụ chuẩn ngành: Baemin "Tụi mình xử lý, bạn chỉ việc ngồi chill"; Tiki xưng "Tiki – bạn", câu ngắn, nhiều emoji. **[SOURCED 30]**
- **Câu**: rất ngắn (3–12 từ), ngắt dòng thay dấu câu, dòng trống giữa các ý.
- **Cụm HỢP LỆ riêng** (tell nặng ở mọi register trang trọng): viết tắt "ib", "sll", "freeship", "sale sập sàn", teencode nhẹ, CAPS LOCK nhấn mạnh, emoji giữa câu, "nhé/nha/nghen" cuối câu.

---
### R5. EMAIL CÔNG SỞ VN

- **Kết cấu chuẩn**: Subject nêu thẳng việc → chào: **"Kính gửi + ông/bà/anh/chị + tên,"** (đối tác, cấp trên, lần đầu) hoặc "Dear anh/chị X" / "Em chào anh/chị" (nội bộ, đã quen) → mở: xưng danh + mục đích ngay câu đầu → thân: từng việc rõ ràng, deadline → kết: "Trân trọng," / "Trân trọng cảm ơn." + chữ ký đầy đủ. Tránh viết tắt chat ("bn", "mk", "đk"), tuyệt đối không "này", "ê". **[SOURCED 9,10,11]**
- **Mở chuẩn thân bài**: "Em là A, phòng B. Em viết email này để..." / "Liên quan đến hợp đồng X, tôi xin xác nhận...". Đi thẳng việc trong 1–2 câu. **[SOURCED 9,10]**
- **Kết chuẩn**: nêu hành động mong đợi + hạn ("Nhờ anh phản hồi giúp em trước 17h thứ Sáu.") rồi mới "Trân trọng,". **[SOURCED 9; khuôn câu INFERRED]**
- **Trang trọng**: 3.5–4.5/5 tuỳ quan hệ; đặc thù VN là **tôn ti xưng hô em/anh/chị theo tuổi–chức**, không có "you" trung tính — đây là điểm AI hay hỏng nhất. **[INFERRED, nền tảng văn hoá]**
- **Câu**: ngắn–vừa; email tốt < 150 từ; bullet khi ≥3 đầu việc.
- **Cụm HỢP LỆ riêng**: "Kính gửi", "Trân trọng", "Em xin phép...", "nhờ anh/chị hỗ trợ", "Em cảm ơn anh/chị ạ", "ạ" cuối câu (với cấp trên). Toàn bộ nhóm này là tell nếu lọt sang R3/R4/R7.

---
### R6. BÁO CÁO DOANH NGHIỆP / TÀI CHÍNH

- **Chuẩn nền**: kế thừa phong cách hành chính – công vụ: **khuôn mẫu cao** (điền vào cấu trúc có sẵn), **minh xác** (không tu từ, không hàm ý, mỗi câu một ý), **nghiêm túc – khách quan**, ưa Hán-Việt trang trọng. Kết cấu 3 phần: phần đầu (nơi nhận "Kính gửi: Ban Giám đốc...", căn cứ), phần chính (mục đánh số La Mã/1./1.1.), phần cuối (kiến nghị, ký tên). **[SOURCED 24,25]**
- Báo cáo thường niên/tài chính: nội dung chuẩn hoá theo Thông tư (bảng CĐKT, KQKD, LCTT, thuyết minh); văn thuyết minh bám số liệu: doanh thu, lũy kế, % kế hoạch, so cùng kỳ. **[SOURCED 17,18]**
- **Mở chuẩn**: câu "căn cứ/thực hiện": "Căn cứ kế hoạch kinh doanh năm 2026...", "Thực hiện chỉ đạo của HĐQT tại...". Không hook, không câu hỏi. **[SOURCED 24 cho tính khuôn mẫu; khuôn câu INFERRED]**
- **Kết chuẩn**: mục "Kiến nghị/Đề xuất" + câu khoá "Trên đây là báo cáo..., kính trình Ban Giám đốc xem xét, phê duyệt." **[INFERRED từ mẫu công văn phổ biến; nhất quán 24,25]**
- **Trang trọng**: 5/5. Không ngôi cá nhân (cơ quan tự xưng "Công ty", "Phòng").
- **Câu**: câu dài đa mệnh đề chấp nhận, bị động + danh hoá dày ĐẶC TRƯNG hợp lệ ("việc triển khai... đã được hoàn thành") — thứ mà style guide phương Tây coi là xấu lại là chuẩn ở đây.
- **Cụm HỢP LỆ riêng**: "Căn cứ...", "Theo đó,", "lũy kế", "so với cùng kỳ", "đạt 87% kế hoạch", "nguyên nhân chủ yếu do", "Trên đây là...". Số liệu dày là bắt buộc, không phải trang trí.

---
### R7. BLOG CÁ NHÂN / TẢN VĂN

- **Chuẩn thể loại**: văn xuôi ngắn, hàm súc; **chấm phá**, không cần cốt truyện; điều cốt yếu là **giọng điệu, cốt cách cá nhân** và "bộc lộ trực tiếp tình cảm, ý nghĩ mang đậm bản sắc cá tính tác giả"; hình thức tự do, dài ngắn tuỳ ý. Blog cá nhân = hậu duệ số của tản văn (nhật ký, chuyến đi, trải nghiệm). **[SOURCED 19,20,21]**
- **Mở chuẩn**: vào thẳng một khoảnh khắc/chi tiết cụ thể, thường phi thời sự: "Sáng nay đứng chờ cà phê nhỏ giọt, tự dưng nhớ...". KHÔNG dẫn nhập bối cảnh xã hội kiểu "Trong cuộc sống hiện đại ngày nay". **[INFERRED từ đặc trưng chấm phá 19,20]**
- **Kết chuẩn**: dư âm — một câu ngắn, một hình ảnh, bỏ lửng; không tóm tắt, không bài học đạo lý lộ liễu. Kết "Qua đó ta thấy..." là tử huyệt. **[INFERRED]**
- **Trang trọng**: 1.5/5. Xưng "tôi/mình" tự nhiên; khẩu ngữ hợp lệ.
- **Câu**: dài ngắn xen kẽ MẠNH — một câu 40 từ rồi một câu 3 từ; câu cụt, câu đặc biệt hợp lệ và là dấu hiệu tay nghề.
- **Cụm HỢP LỆ riêng**: "tự dưng", "thật ra", "chẳng hiểu sao", "kiểu", "ừ thì", từ địa phương, chêm nhẹ tiếng Anh đời thường. Ngược lại thuật ngữ/danh hoá Hán-Việt dày ("việc tối ưu hoá trải nghiệm") là tell ở đây dù hợp lệ ở R2/R6.

---
### R8. KỸ THUẬT / HƯỚNG DẪN

- **Chuẩn cốt lõi**: văn phong **"câu mệnh lệnh", ngắn gọn, rõ ràng**, người phổ thông đọc là làm theo được; từ ngữ phổ thông, hạn chế từ nước ngoài không cần thiết, thuật ngữ chuyên môn phải được giải thích; đoạn dài thì tách thành gạch đầu dòng; in đậm/nghiêng để highlight. **[SOURCED 22,23]**
- **Mở chuẩn**: nêu mục tiêu + điều kiện tiên quyết trong 1–3 câu ("Bài này hướng dẫn cài X trên Windows 11. Yêu cầu: quyền admin."). Không kể lể.
- **Kết chuẩn**: kết quả mong đợi, mục "Lưu ý"/troubleshooting. "Chúc bạn thành công!" là kết quen thuộc hợp lệ của guide tiếng Việt. Không cần kết cảm xúc/tổng kết ý nghĩa. **[SOURCED 22,23 cho thân bài; nhận xét về câu kết INFERRED]**
- **Trang trọng**: 2.5/5, trung tính; xưng "bạn" hoặc không ngôi.
- **Câu**: mệnh lệnh ngắn "Nhấn **Save**. Chọn tab **Advanced**."; đánh số bước tuần tự.
- **Cụm HỢP LỆ riêng — QUAN TRỌNG cho engine**: **lặp từ nguyên văn là ĐÚNG** ("nút Cài đặt" phải luôn là "nút Cài đặt", không được thay bằng "phím thiết lập" cho đỡ lặp). Quy tắc chống-lặp-từ của các register văn chương KHÔNG áp dụng ở đây; humanizer mà "đa dạng hoá từ vựng" trong R8 là phá hỏng tài liệu. **[INFERRED từ nguyên tắc minh xác 22 + thực hành technical writing]**

## 3. DẤU HIỆU AI THEO TỪNG REGISTER

### 3.0. Universal tells (mọi register — flag luôn, không cần biết register)

Nguồn VN: **[SOURCED 26,27]**; nguồn EN: **[SOURCED 28,29]**.
1. Cặp khuôn "không chỉ... mà còn...", "tưởng chừng... nhưng..." lặp nhiều lần.
2. Chuyển đoạn máy móc dày đặc: "Hơn nữa,", "Thêm vào đó,", "Bên cạnh đó," mở đầu đoạn liên tiếp.
3. Kết mọi bài bằng "Tóm lại,"/"Kết luận là..." bất kể thể loại (tell trừ R2/R6 — ở đó phải xét thêm tín hiệu khác).
4. Sáo rỗng doanh nghiệp: "tạo giá trị", "đồng bộ hoá mục tiêu", "nâng tầm", "tối ưu trải nghiệm".
5. Lặp một từ chức năng ("hỗ trợ") dày đặc không đảo từ.
6. Em dash (—) 2–3 lần trong đoạn ngắn ở văn VN (dấu này hiếm trong văn Việt tự nhiên).
7. Câu đều chằn chặn về độ dài; đoạn đều chằn chặn về cấu trúc; mở–3 ý–kết đối xứng ("Intro-Point-Point-Conclusion").
8. Không một lỗi nào + trơn tru vô hồn; phức tạp hoá ý đơn giản; đọc lướt thấy ổn, đọc kỹ thấy nông, ý trùng lặp.
9. Từ vựng hallmark EN lây sang VN khi dịch/song ngữ: "delve" → "đào sâu", "tapestry" → "bức tranh đa sắc", "testament" → "minh chứng cho", "trong bối cảnh..." mở bài vạn năng.
10. Tránh viết tắt/khẩu ngữ tuyệt đối, lịch sự trung tính quá mức so với ngữ cảnh ("lack of jaggedness" — thiếu độ xù xì của người thật). **[SOURCED 29]**

### 3.1. Tells THEO REGISTER (lỗi "kéo về register mặc định essay")

Toàn mục này: cơ chế chung **[SOURCED 26,28,29]**, biểu hiện cụ thể từng register **[INFERRED]** — đây là phần engine cần nhất nhưng cũng là phần cần validate bằng corpus thật.

| Register | AI viết SAI kiểu gì (register bị kéo về đâu) | Tell cụ thể cần flag |
|---|---|---|
| R1a Tin | Tin bị kéo thành essay/bình luận | Đoạn kết tổng kết đạo lý ("Sự việc là hồi chuông cảnh tỉnh..."); sapo lặp nguyên tít; "Trong bối cảnh..." mở tin; thiếu trạng ngữ thời gian–địa điểm câu đầu; không có nguồn dẫn "theo..." |
| R1b Phân tích | Bình luận không chính kiến (5C thiếu C2) | Cân bằng giả "một mặt... mặt khác..." rồi không chốt; kết "thời gian sẽ trả lời"; không có luận cứ số liệu mới, chỉ diễn giải lại |
| R2 Học thuật | Học thuật bị kéo thành blog/SEO | Xưng "bạn"; bullet thay lập luận; câu cảm thán; khẳng định to không trích dẫn; "Hy vọng bài viết giúp bạn"; hedging kép vô nghĩa ("có thể có khả năng") |
| R3 SEO | Content bị kéo thành essay vô chủ | Mọi H2 đều dạng câu hỏi; kết lặp nguyên văn mở; keyword rải đều tăm tắp đúng chu kỳ; không case/số/giá cụ thể VN; CTA chung chung "hãy liên hệ chúng tôi" không kênh |
| R4 Caption | Caption bị kéo thành blog/essay — **lỗi lộ nhất** | Mở "Trong cuộc sống hiện đại,..."; câu đủ chủ-vị chỉn chu 20+ từ liên tiếp; không ngắt dòng; emoji đặt cuối-mỗi-câu đều tăm tắp (hoặc không có); kết "Tóm lại"; hashtag dạng cụm dài #NhữngĐiềuCầnBiếtVềX; không CTA tương tác |
| R5 Email | Email bị kéo thành thư nghi thức dịch máy / essay | "Tôi hy vọng email này đến với bạn trong tình trạng tốt nhất" (dịch "I hope this email finds you well" — không tồn tại trong email Việt); gọi sếp bằng "bạn"; giải thích bối cảnh 2 đoạn mới vào việc; thiếu "Trân trọng"/chữ ký; "ạ" lúc có lúc không trong cùng thư |
| R6 Báo cáo | Báo cáo bị kéo thành bài PR/LinkedIn | Tính từ cảm xúc ("ấn tượng", "ngoạn mục") thay số; kết truyền cảm hứng ("cùng nhau bứt phá"); xưng "chúng ta/bạn"; thiếu căn cứ–kiến nghị; % không có kỳ so sánh |
| R7 Blog | Blog bị kéo thành essay nghị luận | Kết cấu mở–thân–kết lộ khung; mỗi đoạn một ý đều nhau; cảm xúc generic ("bình yên đến lạ", "chợt nhận ra rằng" lặp motif); không có chi tiết cảm giác riêng (mùi, âm thanh, tên phố thật); không câu cụt nào |
| R8 Hướng dẫn | Guide bị kéo thành bài SEO/essay | Dẫn nhập dài "Trong thời đại công nghệ 4.0..."; câu mệnh lệnh bị viết thành mô tả vòng ("Bạn có thể tiến hành việc nhấn vào nút..."); ĐỔI TỪ đồng nghĩa cho thuật ngữ/tên nút (phá minh xác); bước không đánh số; chèn đoạn "lợi ích của việc X" giữa các bước |

## 3.2. MA TRẬN CỤM TỪ × REGISTER (hợp lệ ✓ / trung tính ~ / tell ✗)

Toàn bảng: vị trí ✓ có nguồn theo mục 2; các ô ✗/~ là **[INFERRED]** từ nguyên lý tương đối mục 0.

| Cụm / đặc điểm | R1a Tin | R1b Bình luận | R2 Học thuật | R3 SEO | R4 Caption | R5 Email | R6 Báo cáo | R7 Blog | R8 Guide |
|---|---|---|---|---|---|---|---|---|---|
| "Tóm lại," kết bài | ✗ | ~ | ✓ | ~ | ✗✗ | ✗ | ~ (mục Kết luận) | ✗ | ✗ |
| "Kính gửi..." | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| "Trân trọng," | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| "Trong bài viết này..." | ✗ | ~ | ✓ ("bài báo này") | ✓ | ✗ | ✗ | ✗ | ✗ | ~ |
| "Theo đó," / "Được biết," | ✓ | ✓ | ~ | ~ | ✗ | ~ | ✓ | ✗ | ~ |
| "Nghiên cứu này nhằm..." | ✗ | ~ | ✓ | ✗ | ✗ | ✗ | ~ | ✗ | ✗ |
| "Căn cứ...", "kính trình" | ✗ | ✗ | ✗ | ✗ | ✗ | ~ | ✓ | ✗ | ✗ |
| Xưng "bạn" với người đọc | ✗ | ~ | ✗ | ✓ | ✓ | ✗ (trừ ngang hàng thân) | ✗ | ✓ | ✓ |
| Xưng "mình/tụi mình" | ✗ | ✗ | ✗ | ~ | ✓ | ~ (nội bộ thân) | ✗ | ✓ | ~ |
| "Em xin phép... ạ" | ✗ | ✗ | ✗ | ✗ | ~ (bán hàng cho khách lớn tuổi) | ✓ | ~ | ✗ | ✗ |
| Emoji | ✗ | ✗ | ✗ | ~ (ít) | ✓ | ✗ (trừ nội bộ thân) | ✗ | ~ | ✗ |
| Hashtag | ✗ | ✗ | ✗ | ~ | ✓ | ✗ | ✗ | ~ | ✗ |
| Câu cụt / không đủ chủ-vị | ✗ | ~ (nhấn) | ✗ | ~ | ✓ | ✗ | ✗ | ✓ | ✓ (mệnh lệnh) |
| Câu bị động + danh hoá dày | ✗ | ✗ | ✓ | ✗ | ✗✗ | ~ | ✓ | ✗ | ✗ |
| Lặp nguyên văn 1 thuật ngữ | ~ | ~ | ✓ | ✓ (keyword) | ✗ | ~ | ✓ | ✗ | ✓✓ (bắt buộc) |
| Bullet/đánh số | ~ | ✗ | ~ | ✓ | ~ | ✓ (≥3 việc) | ✓ | ✗ | ✓✓ |
| Trích nguồn "(Nguyễn, 2020)" | ✗ ("theo ông X") | ~ | ✓ | ✗ (hyperlink) | ✗ | ✗ | ~ (phụ lục) | ✗ | ✗ |
| "Hy vọng bài viết giúp bạn" | ✗ | ✗ | ✗ | ✓ (mòn) | ✗ | ✗ | ✗ | ✗ | ~ |
| "Chúc bạn thành công!" | ✗ | ✗ | ✗ | ~ | ~ | ~ (kết thư nhẹ) | ✗ | ✗ | ✓ |
| Con số % + kỳ so sánh | ✓ | ✓ | ✓ | ~ | ~ | ~ | ✓✓ | ✗ | ~ |

Cách đọc cho engine: một cụm ✗✗ trong register đã nhận diện → flag nặng (điểm AI-tell cao). Cụm ✓ ở đúng register → KHÔNG flag kể cả khi nó nằm trong kill-list toàn cục. Kill-list toàn cục chỉ giữ các mục 3.0.

## 4. TỰ ĐỘNG NHẬN DIỆN REGISTER TỪ TEXT

Tiền lệ kỹ thuật: phân loại văn bản tiếng Việt theo chủ đề/thể loại bằng ML là bài toán chín (underthesea, corpus binhvq/news-corpus, các khảo sát mô hình phân loại văn bản tiếng Việt) — nhưng cho humanizer, rule-based scoring đủ dùng và giải thích được. **[SOURCED 35,36]** Toàn bộ heuristic dưới đây **[INFERRED]**, xây từ các đặc trưng ĐÃ SOURCED ở mục 2.

### 4.1. Tín hiệu cấu trúc bề mặt (mạnh nhất, check trước)
1. Dòng đầu có "Kính gửi" / cuối có "Trân trọng" + chữ ký → **R5** (nếu có "Căn cứ", số hiệu, "kính trình", mục La Mã → **R6**).
2. Quốc hiệu tiêu ngữ / "BÁO CÁO" in hoa / bảng số liệu + "lũy kế/cùng kỳ" → **R6**.
3. Hashtag, emoji ≥2, dòng ngắn <60 ký tự xuống dòng liên tục, tổng <300 từ → **R4**.
4. Bước đánh số + động từ mệnh lệnh đầu câu ("Nhấn", "Chọn", "Cài") + tên UI in đậm → **R8**.
5. H2/H3 nhiều + keyword lặp chu kỳ + CTA cuối + 800–2500 từ → **R3**.
6. Trích dẫn học thuật "(Tác giả, năm)" / "TÀI LIỆU THAM KHẢO" / "Nghiên cứu này" → **R2**.
7. Câu đầu có ngày tháng + địa danh + cơ quan; nguồn "theo ông/bà" → **R1a**; có chính kiến "tôi cho rằng", câu hỏi tu từ, luận cứ → **R1b**.
8. Xưng "tôi/mình" + chi tiết đời tư + không CTA bán hàng → **R7**.

### 4.2. Tín hiệu xưng hô (rất phân biệt trong tiếng Việt)
- em/anh/chị + "ạ" → R5 (hoặc R4 seller). "bạn" + brand tự xưng tên → R3. "mình/tụi mình/cả nhà" → R4/R7. "tôi" + cảm xúc → R7/R1b. Zero ngôi (toàn danh từ cơ quan) → R1a/R6. "chúng tôi" + số liệu → R2/R6.

### 4.3. Tín hiệu thống kê
- Độ dài trung bình câu: R4 (<10 từ) < R8 < R1a ≈ R3 < R5 < R1b < R7 (phương sai lớn nhất) < R2 ≈ R6 (dài nhất).
- Tỷ lệ từ Hán-Việt/trang trọng ("tiến hành, triển khai, căn cứ, đề xuất"): R6 ≥ R2 > R5 > R1 > R3 ≈ R8 > R7 > R4.
- Mật độ số + %: R6 > R1a ≈ R2 > R3 > còn lại.
- Phương sai độ dài câu cao + câu cụt → R7/R4 người thật; phương sai thấp → hoặc R2/R6 hợp lệ, hoặc AI.

### 4.4. Thuật toán đề xuất
Score(register) = 3×(structural hits) + 2×(xưng hô hits) + 1×(keyword hits) + 1×(thống kê trong khoảng chuẩn). Lấy max; nếu top-2 chênh <20% → gắn nhãn lai (vd R3/R1b "advertorial") và chỉ áp universal tells + tells chung của cả hai. Văn bản <120 từ mặc định nghiêng R4/R5 trước khi xét khác.

## 5. KHUYẾN NGHỊ TÍCH HỢP VÀO HUMANIZER

1. **Detect register TRƯỚC khi chấm tell** — chạy 4.1→4.4; không có register thì chỉ được dùng danh sách 3.0.
2. **Kill-list phải là kill-list-có-điều-kiện**: lưu dạng (cụm, register→verdict) theo ma trận 3.2, không lưu cụm trần. ("Tóm lại" từng bị xoá oan ở văn bản học thuật nếu kill-list phẳng.)
3. **Không "đa dạng hoá từ vựng" ở R8 và keyword R3** — lặp là đúng chuẩn ở đó.
4. **Humanize = tăng jaggedness ĐÚNG CHỖ**: R7/R4 cần phương sai câu + câu cụt; R2/R6 tuyệt đối không chèn khẩu ngữ — humanize R6 nghĩa là siết số liệu + đúng khuôn, không phải thêm "chất người" kiểu blog.
5. **Mở/kết là điểm chấm nặng nhất**: mỗi register có khuôn mở/kết riêng (mục 2); lệch khuôn mở/kết là tín hiệu AI mạnh hơn mọi cụm từ giữa bài.
6. Validate các ô [INFERRED] bằng corpus thật (news-corpus cho R1, kho note/email nội bộ cho R5/R6) trước khi hard-code trọng số.

## SOURCES

Ghi chú: các URL đã truy cập/trích qua web search 2026-07-09. S = dùng làm căn cứ chính.

**Lý thuyết phong cách học (R-nền):**
1. (S) Nguyễn Thế Truyền, "Đề cương bài giảng Phong cách học tiếng Việt hiện đại" (nhắc nền Đinh Trọng Lạc) — http://www.hoalinhthoai.com/application/uploads/files/De%20cuong%20%20Giao%20trinh%20Phong%20cach%20hoc.pdf
2. (S) Đề cương Phong cách học tiếng Việt, ĐH Quy Nhơn — https://www.studocu.vn/vn/document/dai-hoc-quy-nhon/mot-so-van-de-phong-cach-hoc-tieng-viet/de-cuong-bai-giang-phong-cach-hoc-tieng-viet-mon-pch-1-tin-chi/127006473
3. (S) "Các phong cách chức năng ngôn ngữ trong văn bản" — https://loigiaihay.com/cac-phong-cach-chuc-nang-ngon-ngu-trong-van-ban-phan-1-c122a20059.html

**R1 Báo chí:**
4. (S) "Phong cách ngôn ngữ báo chí là gì? Đặc điểm" — https://luatminhkhue.vn/phong-cach-ngon-ngu-bao-chi.aspx
5. (S) "Khái luận về sapô" — https://123docz.com/trich-doan/781605-khai-luan-ve-sapo.htm
6. (S) "Sapo là gì? 7 cách tạo đoạn mở đầu hấp dẫn" — https://vietmoz.edu.vn/sapo-la-gi/
32. (S) "Nguyên tắc viết bài bình luận ngắn 5C+1N" — https://onecms.vn/nguyen-tac-viet-bai-binh-luan-ngan-tao-su-khac-biet-cho-bao-dien-tu-49703.html
33. "Kỹ năng viết tin, bài" (HV Nông nghiệp) — https://nxb.vnua.edu.vn/wp-content/uploads/2018/12/viet-tin.doc

**R2 Học thuật:**
7. (S) "Cách viết văn phong học thuật (academic writing)" — https://stefanassignment.com/blogs/news/cach-viet-van-phong-hoc-thuat-academic-writing-nhu-the-nao
8. (S) "Làm thế nào để viết tốt một luận văn khoa học" — Viện KT&KDQT, ĐH Ngoại thương — https://ktkdqt.ftu.edu.vn/lam-the-nao-de-viet-tot-mot-luan-van-khoa-hoc/
34. Quy định cấu trúc bài báo khoa học — https://jsrd.thanhdo.edu.vn/index.php/khpt/structure-and-presentation

**R5 Email:**
9. (S) "Cách viết email chuyên nghiệp" JobsGO — https://jobsgo.vn/blog/cach-viet-email-chuyen-nghiep/
10. (S) "Hướng dẫn cách viết email chuẩn và chuyên nghiệp" VBI — https://tuyendung.evbi.vn/tin-tuc/huong-dan-cach-viet-email-chuan-va-chuyen-nghiep.35a54d2d/vi
11. "Cách viết email chuyên nghiệp tại công ty" — https://vinahost.vn/cach-viet-email-chuyen-nghiep/

**R3/R4 Marketing & Social:**
12. (S) "Cách viết content Facebook hiệu quả" MISA AMIS — https://amis.misa.vn/126583/cach-viet-content-facebook/
13. (S) "Công thức viết content (AIDA, PAS...)" — https://www.huongnghiepaau.com/cong-thuc-viet-content
14. (S) "Cách viết bài chuẩn SEO + checklist" GTV SEO — https://gtvseo.com/cach-viet-bai-chuan-seo/
15. (S) "Viết bài chuẩn SEO: 7 bước, 34 checklist" SEONGON — https://seongon.com/blog/seo/viet-bai-chuan-seo.html
16. "Bài viết chuẩn SEO 2026" Advertising Vietnam — https://advertisingvietnam.com/article/bai-viet-chuan-seo-2026-dinh-nghia-checklist-10-muc-5-buoc-viet-len-top-google-p27482
30. (S) "Hiểu đúng về Brand Tone of Voice" (case Tiki, Baemin, xưng hô) — https://advertisingvietnam.com/hieu-dung-ve-brand-tone-of-voice-cach-thuong-hieu-the-hien-ban-sac-va-giao-tiep-ca-nhan-hoa-voi-nguoi-dung-muc-tieu-p21587
31. "Brand tone of voice là gì" OCD — https://ocd.vn/brand-tone-of-voice-giong-dieu-thuong-hieu-la-gi-cach-xay-dung-va-ung-dung-hieu-qua/

**R6 Báo cáo / hành chính:**
17. (S) "Báo cáo thường niên là gì? Cách lập" — https://ketoanleanh.edu.vn/kinh-nghiem-ke-toan/bao-cao-thuong-nien-la-gi.html
18. "Báo cáo thường niên" Wikipedia VN — https://vi.wikipedia.org/wiki/B%C3%A1o_c%C3%A1o_th%C6%B0%E1%BB%9Dng_ni%C3%AAn
24. (S) "Phong cách ngôn ngữ hành chính – công vụ" — https://www.studocu.vn/vn/document/truong-dai-hoc-can-tho/ky-thuat-va-phuong-phap-day-hoc-ky-thuat-giao-duc-tieu-hoc/19-phong-cach-ngon-ngu-hanh-chinh-cong-vu/93385610
25. (S) "Soạn bài Phong cách ngôn ngữ hành chính" — https://vuihoc.vn/tin/thpt-soan-bai-phong-cach-ngon-ngu-hanh-chinh-ngu-van-12-chi-tiet-1937.html

**R7 Tản văn / blog:**
19. (S) "Tản văn là gì? Đặc trưng" Văn học trẻ — https://forum.vanhoctre.com/threads/tan-van-la-gi-dac-trung-cua-tan-van-su-khac-va-giong-nhau-giua-tan-van-tu-su-ky-su-la-gi.1936/
20. (S) "Tản văn" Wikipedia VN — https://vi.wikipedia.org/wiki/T%E1%BA%A3n_v%C4%83n
21. "Tản văn là gì? Đặc điểm, phân loại, kỹ năng viết" — https://supperclean.vn/tan-van-la-gi/

**R8 Kỹ thuật:**
22. (S) "Kỹ năng soạn thảo văn bản" VBSP (văn phong mệnh lệnh, ngắn gọn) — https://vbsp.org.vn/wp-content/uploads/2016/02/B%C3%A0i-3.-K%E1%BB%B9-n%C4%83ng-so%E1%BA%A1n-th%E1%BA%A3o-v%C4%83n-b%E1%BA%A3n.doc
23. (S) "Mẹo nâng cao kỹ năng viết tài liệu kỹ thuật" Viblo — https://viblo.asia/p/mot-so-meo-hay-giup-nang-cao-ki-nang-viet-tai-lieu-ky-thuat-m68Z0VJj5kG

**AI-tells:**
26. (S) "Dấu hiệu nhận biết nội dung được viết bởi AI" BRANDS Vietnam Help — https://help.brandsvietnam.com/vi/article/dau-hieu-nhan-biet-noi-dung-duoc-viet-boi-ai-3zy07d/
27. (S) "Cách nhận biết bài viết có được viết bởi ChatGPT" SCTT — https://sctt.net.vn/cach-nhan-biet-bai-viet-co-duoc-viet-boi-chatgpt-hay-khong/
28. (S) "Wikipedia:Signs of AI writing" — https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
29. (S) "How to Spot AI Writing Tells: 17 Examples + AI Words Blacklist" — https://www.oliviacal.com/post/ai-writing-tells

**Phân loại văn bản tự động:**
35. "Phân loại văn bản tiếng Việt sử dụng machine learning" — https://nguyenvanhieu.vn/phan-loai-van-ban-tieng-viet/
36. "Khảo sát các mô hình phân loại văn bản tiếng Việt" — https://www.researchgate.net/publication/364422333_KHAO_SAT_CAC_MO_HINH_PHAN_LOAI_VAN_BAN_TIENG_VIET

**Giới hạn dữ liệu:** (a) chưa có khảo sát định lượng công bố về "AI viết sai register tiếng Việt" — mục 3.1 là khung suy luận cần validate; (b) các ngưỡng số (độ dài câu, formality score) ở mục 4.3 là ước lượng chuyên môn, chưa đo trên corpus; (c) nguồn giáo trình gốc (Đinh Trọng Lạc 1994) chỉ tiếp cận được qua đề cương/giáo trình thứ cấp, chưa đối chiếu bản in.
