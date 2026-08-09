# Bảng số dày

Chưng cất từ `research/02-professional-report` mục 4 và `research/11-empty-states`. Bảng là
thứ người đọc báo cáo tài chính dùng nhiều nhất và cũng là thứ hay bị làm ẩu nhất, vì nó trông
như chỉ cần đổ dữ liệu vào.

---

## 1. Khi nào bảng thắng chart

Bảng thắng khi người đọc cần **tra một giá trị cụ thể**, cần **so nhiều chỉ tiêu cùng lúc cho
cùng một đối tượng**, hoặc khi con số phải chép lại được vào mô hình của họ.

Chart thắng khi câu hỏi là về **hình dạng**: xu hướng, phân phối, tương quan, thứ hạng.

Phép thử nhanh: nếu người đọc sẽ dùng ngón tay dò theo hàng, đó là bảng. Nếu họ sẽ nhìn một
cái rồi gật đầu, đó là chart.

Với `MAT_DO_SO` từ 7 trở lên, phần lớn nội dung là bảng, và điều đó bình thường.

## 2. Căn chỉnh: ba luật, không có ngoại lệ thứ tư

1. **Cột số căn PHẢI**, và căn theo dấu thập phân nếu phần lẻ dài ngắn khác nhau. Đây là thứ
   cho phép mắt so độ lớn theo cột dọc, thao tác người đọc bảng tài chính làm nhiều nhất.
2. **Cột nhãn căn TRÁI.**
3. **Không căn giữa cột số.** Căn giữa phá hoàn toàn khả năng so theo cột.

Ngoại lệ hợp lệ duy nhất: cột chứa giá trị định tính, ví dụ hạng tín nhiệm hoặc mức đánh giá
cao trung bình thấp. Cột đó căn trái hoặc căn giữa đều được. Đừng ép cả bảng dùng một kiểu căn
chỉ vì phần lớn cột là số.

Số dùng font đẳng chiều rộng (`tabular-nums`), nếu không thì chữ số hàng đơn vị không thẳng
hàng dù đã căn phải.

## 3. Số âm: chọn một trường phái và giữ nguyên

| Trường phái | Ký hiệu | Dùng khi |
|---|---|---|
| Kế toán | ngoặc đơn, ví dụ (1.250) | báo cáo tài chính, bảng cần kiểm tổng bằng mắt, bản có thể in đen trắng |
| Phân tích | dấu trừ kèm màu | bản đọc trên màn hình, cần tín hiệu nhanh |

Ngoặc đơn không phụ thuộc màu nên vẫn đúng khi in đen trắng và với người mù màu. Dấu trừ kèm
màu nhanh hơn nhưng mất tác dụng khi photocopy.

**Trộn hai trường phái trong một tài liệu là lỗi.** Chọn theo thể loại rồi giữ nguyên tới cuối.

Dấu âm dùng dấu gạch nối ASCII, không dùng dấu trừ toán học. Lý do và số đo ở `CLAUDE.md`.

## 4. Quy ước số Việt Nam

- Dấu phẩy là dấu thập phân, dấu chấm phân cách hàng nghìn: `1.240,5`.
- Đơn vị ghi ở **tiêu đề cột**, không lặp ở từng ô. Ô chỉ chứa số.
- Trong văn xuôi thì ngược lại: viết đơn vị bằng chữ ngay cạnh số.
- Chép số từ nguồn tiếng Anh là chỗ hay lẫn hai quy ước nhất. Kiểm lại toàn bảng sau khi chép.

## 5. Ô trống: bốn loại vắng mặt, bốn ký hiệu

Để trống cả bốn là xoá thông tin. Bốn loại và cách đọc:

| Loại | Nghĩa |
|---|---|
| Chưa tới kỳ | kỳ báo cáo chưa kết thúc |
| Đã tới kỳ, chưa công bố | kỳ đã kết thúc mà số chưa ra |
| Không áp dụng | chỉ tiêu này không tồn tại với đối tượng này |
| Bị loại | có số nhưng loại vì bất thường, và phải nói loại vì sao |

Bảng ký hiệu đầy đủ ở `research/11-empty-states/ABSENCE-TABLE.md`. Đặt một câu chú thích duy
nhất dưới bảng giải nghĩa bộ ký hiệu, không giải nghĩa lặp ở từng bảng.

## 6. Ngưỡng bỏ bảng

Khi bảng thiếu quá nhiều ô, nó không còn là bảng mà là một tấm lưới rỗng có vài số rải rác. Lúc
đó chuyển sang câu văn: nói ra ba số có thật và nói thẳng phần còn lại chưa có.

Ngưỡng thực dụng: quá một phần ba số ô trống thì cân nhắc bỏ bảng. Đây là ngưỡng suy luận thiết
kế, chưa qua đo thực nghiệm, và nói ra để không ai tưởng nó là con số khoa học.

## 7. Hàng tổng

- Hàng tổng phải **khác biệt về nét**, không chỉ khác về đậm nhạt: một đường kẻ trên hàng tổng.
- Tổng phải **cộng đúng**, kể cả khi từng hàng đã làm tròn. Nếu tổng làm tròn không khớp tổng
  các hàng đã làm tròn, ghi chú một dòng thay vì sửa số cho khớp.
- Bảng không có ý nghĩa cộng dồn thì **đừng có hàng tổng**. Tổng của một cột tỷ lệ phần trăm
  giữa các đối tượng khác nhau là một con số vô nghĩa.

## 8. Nhất quán với chart

Bảng và chart của cùng một mô hình phải khớp. Cặp hay tự mâu thuẫn nhất: bảng tóm tắt so với
chart chi tiết, và tổng trong bảng so với tổng nêu trong văn xuôi.

Cách chắc chắn: sinh cả hai từ MỘT nguồn dữ liệu. Gõ lại số vào bảng là tạo ra một bản thứ hai
để trôi. Xem `research/12-cross-exhibit/FINDINGS.md`.
