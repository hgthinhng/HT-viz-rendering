# Ranh giới đắt và rẻ

Chưng cất từ `research/04-wow-layer/ANTI-SLOP.md`, cập nhật cho hai làn xuất bản. Bản gốc viết
khi repo còn tiền đề in giấy, nên nhiều dòng của nó nói về WeasyPrint và photocopy; những dòng
đó giữ nguyên giá trị cho làn `pdf-so` nhưng không còn là ràng buộc chung.

Mỗi hàng là một cặp: cùng một Ý ĐỊNH, một bản đắt và một bản rẻ. Cột cuối là cách phân biệt
trong ba giây mà không cần đọc nội dung.

Danh sách gọn hơn cho phần cấu trúc và con chữ nằm ở `SKILL.md` mục 8.

---

## 1. Thị giác

| Ý định | Bản đắt | Bản rẻ | Phân biệt trong ba giây |
|---|---|---|---|
| Làm nổi một con số | Cỡ chữ áp đảo, đứng một mình, một câu ngữ cảnh bên dưới, không khung | Thẻ số bo tròn, icon mũi tên, viền trái màu, nền đổ nhạt | Che icon và khung: con số vẫn đứng vững là đắt, trông trống trải ngay là rẻ vì sức nặng đến từ trang trí |
| Tạo độ nổi và phân lớp | Hai phần tử thật lệch nhau, hoặc viền đặc, hoặc khối màu nền | Đổ bóng mờ, gradient giả ánh sáng | Phóng to 300%: thấy hai lớp hình học thật là đắt, thấy vệt mờ là rẻ |
| Khoảng trắng lớn ở trang mở | Khoảng trắng có đúng hai điểm neo, mắt di chuyển có chủ đích giữa chúng | Logo và tiêu đề căn giữa, xung quanh trống vì "trông tối giản" | Che chữ, chỉ nhìn bố cục: còn đoán được điểm nhấn lệch tâm là đắt, đối xứng tuyệt đối và trống là rẻ |
| Phá nhịp | Hai tới ba lần trong cả tài liệu, đúng chỗ có tin quan trọng nhất, đổi hẳn tỷ lệ thông tin | Mọi trang chương đều phá nhịp theo cùng một mẫu | Đếm số lần lặp một mẫu: quá ba lần là nó đã thành nền |
| Trang ngăn chương | Tên chương, một câu định vị, một tới hai số thật sẽ xuất hiện lại trong chương | Tên chương to giữa trang trắng, số La Mã trang trí | Hỏi: đọc xong có biết chương này sẽ nói gì không |
| Chữ phóng to làm hình ảnh | Đã kiểm dấu bằng ảnh chụp thật, ưu tiên số hoặc từ ít dấu chồng | Phóng to bất kỳ từ nào cho hoành tráng, chỉ xem trên máy người viết | Mở đúng file sẽ giao và đọc to: đọc trôi là đắt, phải đoán chữ là rẻ |
| Tiết chế màu | Một accent duy nhất, phần còn lại bù bằng kỷ luật căn lề tuyệt đối | Một accent duy nhất nhưng căn lề lệch, khoảng cách dòng không đều | Đo khoảng cách giữa hai khối bất kỳ: đều là tiết chế có chủ đích, lệch là thiếu ngân sách nguỵ trang thành tối giản |
| Nhân bản hoá dữ liệu | Con số luôn kèm ngữ cảnh so sánh cụ thể | Hoạ tiết vẽ tay giả phủ lên số liệu tài chính | Đọc câu quanh con số: có phép so sánh là đắt, chỉ có hình trang trí là rẻ và còn sai giọng thể loại |

## 2. Riêng làn `html-song`

Làn này được phép animation và tương tác, và đó là chỗ dễ rẻ tiền nhất trong toàn bộ repo.

| Ý định | Bản đắt | Bản rẻ | Phân biệt trong ba giây |
|---|---|---|---|
| Dùng chuyển động để dẫn mắt | Chuyển động xảy ra MỘT lần khi phần tử vào khung nhìn, dưới 300ms, và nói một điều: thứ tự đọc | Mọi khối đều trôi lên khi cuộn tới, hiệu ứng lặp vô hạn, phần tử nảy | Cuộn xuống rồi cuộn lên lại: nếu mọi thứ diễn lại từ đầu thì chuyển động là trang trí |
| Tương tác để đào sâu | Hover hoặc bấm mở ra số liệu KHÔNG có chỗ nào khác trên trang | Tooltip hiện lại đúng con số đã in ngay cạnh đó | Tắt JavaScript: nếu mất thông tin thật là đắt, nếu chỉ mất hiệu ứng là tương tác thừa |
| Chart sống thay chart tĩnh | Chart sống cho phép lọc, so sánh, hoặc xem nhiều tầng dữ liệu | Chart sống hiển thị đúng thứ một ảnh tĩnh hiển thị, chỉ thêm animation lúc vào | Hỏi: người đọc LÀM được gì với chart này mà với ảnh thì không |
| Chủ đề tối | Bảng màu tối được thiết kế riêng, chart và minh hoạ đều có bản theo nền | Đảo màu nền trang, chart giữ nguyên nền trắng | Cuộn qua một chart: nếu có ô trắng nổi giữa trang tối thì chưa làm xong |

## 3. Bốn dấu hiệu gộp

Một trang có từ hai dấu hiệu sau trở lên thì gần như chắc là rẻ, dù từng chi tiết trông ổn:

1. **Trang trí không neo được vào một con số hoặc câu cụ thể** trên chính trang đó.
2. **Xoá yếu tố đó đi thì thông điệp MẠNH LÊN**, không yếu đi.
3. **Đổi ngành, đổi công ty mà cả trang dùng lại nguyên xi được** chỉ bằng cách thay số. Đó là
   khuôn trang trí, không phải phân tích cho case cụ thể.
4. **Chỉ đứng vững ở một môi trường**: hỏng khi in đen trắng với làn `pdf-so`, hoặc mất sạch
   thông tin khi tắt JavaScript với làn `html-song`.

## 4. Phép thử cuối, dùng khi vẫn phân vân

Đưa trang cho một người không biết gì về ngành và hỏi đúng một câu: **"Trang này bảo bạn điều
gì?"**

Trả lời được bằng một câu có số là đắt. Trả lời "nó nói về tình hình ngành X" là rẻ, vì đó là
nhắc lại tiêu đề chứ không phải nhận được thông tin.
