# Ranh giới wow thật và wow rẻ tiền

Tài liệu chống AI-slop cho tầng "wow". Mỗi hàng là một cặp: cùng một Ý ĐỊNH thiết kế, một phiên
bản ĐẮT (giữ ý định, thi công có kỷ luật) và một phiên bản RẺ (giữ hình thức bề mặt, bỏ kỷ luật
bên dưới). Cột cuối là cách phân biệt bằng mắt trong 3 giây, không cần đọc nội dung.

Đối chiếu với luật đã chốt của người dùng: cấm bo tròn lớn cộng border-left màu, cấm kết luận
cách ngôn, cấm bịa social proof, cấm em-dash. Bảng dưới đây mở rộng danh sách này sang đúng vùng
"wow layer".

| # | Ý định thiết kế | Phiên bản ĐẮT | Phiên bản RẺ (AI-slop) | Phân biệt trong 3 giây |
|---|---|---|---|---|
| 1 | Làm nổi một con số quan trọng | Cỡ chữ áp đảo, đứng một mình, một câu ngữ cảnh duy nhất bên dưới, không khung | "Stat card" bo tròn 12px, icon mũi tên/ngôi sao, border-left màu accent, nền đổ màu nhạt | Che icon và khung lại: nếu con số vẫn đứng vững một mình thì đắt; nếu trông trống trải ngay là rẻ, vì sức nặng đến từ trang trí chứ không phải từ chính con số |
| 2 | Tạo độ nổi / phân lớp | `box-shadow` offset cứng blur 0 (xem tokens.css `--shadow-1/2/3`), hoặc text-shadow hai lớp kiểu letterpress | `box-shadow` có blur, hoặc gradient nền giả ánh sáng, hoặc `filter: drop-shadow()` | Nhìn viền bóng: viền sắc nét tuyệt đối là đắt (và là YÊU CẦU BẮT BUỘC của repo); viền mờ dần là rẻ VÀ VI PHẠM ràng buộc in |
| 3 | Dùng khoảng trắng lớn ở bìa/trang mở | Khoảng trắng có đúng hai điểm neo (một câu, một số), mắt phải di chuyển có chủ đích giữa chúng | Khoảng trắng bao quanh logo và tiêu đề căn giữa, không có gì khác vì "trông tối giản" | Che phần chữ, chỉ nhìn bố cục: nếu vẫn đoán được có một điểm nhấn lệch tâm là đắt; nếu đối xứng tuyệt đối và trống là rẻ |
| 4 | Phá nhịp giữa các trang đều đặn | 2-3 lần trong cả tài liệu, đúng chỗ có tin quan trọng nhất, đổi hẳn tỷ lệ thông tin (một trang = một ý) | Mọi trang chương đều "phá nhịp" giống nhau (cùng một mẫu nền màu, cùng một icon lớn) | Đếm số lần lặp lại đúng một mẫu phá nhịp: lặp lại quá 3 lần là nó đã thành khuôn mẫu, hết là "phá nhịp" |
| 5 | Trang ngăn chương | Tên chương + một câu định vị + 1-2 số neo THẬT sẽ xuất hiện lại trong chương | Tên chương to đùng giữa trang trắng, không số, không câu, chỉ có số thứ tự La Mã trang trí | Hỏi: "đọc xong trang ngăn có biết chương này sẽ nói gì không?" Biết là đắt, không biết là rẻ |
| 6 | Chữ tiếng Việt phóng to làm hình ảnh | Đã verify render đúng dấu trong PDF thật (WeasyPrint), ưu tiên số hoặc từ ít dấu chồng, có đệm dòng đo bằng ảnh thật | Phóng to bất kỳ từ nào cho "hoành tráng", chỉ xem trên trình duyệt rồi kết luận xong | Mở đúng file PDF xuất ra (không phải xem trên Chrome) và đọc to: nếu đọc trôi là đắt, nếu phải đoán chữ là rẻ và có thể đang dính bug font (xem FINDINGS.md mục 0) |
| 7 | Tiết chế / màu sắc hẹp | Một accent duy nhất dùng nhất quán, còn lại là kỷ luật căn lề/khoảng cách tuyệt đối để bù | Một accent duy nhất nhưng căn lề lệch, khoảng cách dòng không đều, font khác nhau giữa các bảng | Đo khoảng cách giữa hai khối bất kỳ bằng mắt so với khối khác: đều nhau là đắt (tiết chế có chủ đích), lệch là rẻ (thiếu ngân sách nguỵ trang thành tối giản) |
| 8 | Dữ liệu "nhân bản hoá" (data humanism kiểu Giorgia Lupi) | Con số luôn đi kèm NGỮ CẢNH so sánh cụ thể (so với năm trước, so với ngưỡng), giọng văn thật của repo (xem vn-humanizer register) | Thêm hoạ tiết "vẽ tay" giả (SVG path lượn sóng) phủ lên số liệu tài chính nghiêm túc để trông "ấm áp, con người" | Đọc câu văn quanh con số: có phép so sánh cụ thể là đắt; chỉ có hình trang trí không liên quan đến số là rẻ, và với báo cáo tài chính, hoạ tiết "vẽ tay" giả còn làm mất uy tín vì sai giọng thể loại |
| 9 | Thay thế tương tác digital (scroll/hover) trong bản in | Chuỗi small-multiples xếp cạnh nhau, chú thích neo bằng leader line vào đúng điểm | Vẽ mũi tên "vệt chuyển động" hoặc bóng mờ giả lia chuột, hoặc để trống ghi "xem bản online để tương tác" | Nếu thủ pháp thay thế vẫn mang thông tin thật (số, nhãn, thứ tự) là đắt; nếu chỉ là trang trí gợi nhớ hiệu ứng động mà không thêm thông tin là rẻ |
| 10 | Kết luận / câu chốt của một trang wow | Câu chốt có SỐ hoặc HÀNH ĐỘNG cụ thể, dưới 22 từ | Câu chốt kiểu cách ngôn ẩn dụ ("con số là ngôn ngữ của sự thật", "dữ liệu không biết nói dối") | Thử rút câu chốt ra khỏi ngữ cảnh: nếu vẫn mang thông tin cụ thể (số/hành động) là đắt; nếu nghe hay nhưng áp dụng cho bất kỳ báo cáo nào cũng đúng là rẻ (đặc điểm của cách ngôn AI-slop) |

## Bốn dấu hiệu gộp, dùng khi không chắc

Nếu một trang "wow" có từ hai dấu hiệu sau trở lên, khả năng cao là rẻ tiền dù từng chi tiết
riêng lẻ trông ổn:

1. **Trang trí không neo được vào một con số hoặc câu cụ thể nào** trên chính trang đó.
2. **Xoá yếu tố đó đi, thông điệp mạnh hơn** chứ không yếu hơn (xem quy tắc tổng kết trong
   FINDINGS.md).
3. **Đổi ngành/đổi công ty mà toàn bộ trang dùng lại nguyên xi được**, không cần sửa gì ngoài số
   liệu - dấu hiệu nó là khuôn trang trí, không phải phân tích cho case cụ thể (cùng nguyên tắc
   đã áp dụng cho minh hoạ SVG trong `illustrations/grammar.md`).
4. **Chỉ đứng vững khi xem trên màn hình**, hỏng hoặc mất tác dụng khi in ra giấy trắng đen hoặc
   photocopy lại.
