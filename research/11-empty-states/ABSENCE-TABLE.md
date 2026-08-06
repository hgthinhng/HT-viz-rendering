# Bảng ký hiệu sáu loại vắng mặt

Tài liệu dùng hàng ngày, đọc `FINDINGS.md` mục 1 để có quá trình khảo sát và lý do chọn từng ký
hiệu (IMF, World Bank, BIS, Eurostat, UN, OECD, comps ngân hàng đầu tư). File này chỉ giữ bảng
tra và câu chú thích mẫu.

**Ràng buộc nền của cả bảng**: không dùng em-dash (U+2014) hay en-dash (U+2013) cho bất kỳ ký hiệu nào
(khác quy ước UN/nhiều BCTC phương Tây vốn dùng en-dash cho "đúng bằng không" - repo này cấm
tuyệt đối, xem lý do ở `FINDINGS.md` mục 1.3). Mọi ký hiệu dưới đây dùng ASCII thường
(chấm, hyphen-minus, tilde) hoặc một glyph phổ quát (†) đã verify render đúng qua WeasyPrint
69.0 + trích xuất text bằng pymupdf.

## Bảng chính

| # | Ký hiệu | Nghĩa | Khi nào dùng | Khi nào ĐỪNG dùng | Đọc được khi in đen trắng/photocopy? |
|---|---|---|---|---|---|
| 1 | `0` (chữ số thường, không đổi màu/kiểu chữ so với số khác trong cột) | Đúng bằng không - đây LÀ một phép đo, giá trị của nó bằng không | Khoản mục có phát sinh nhưng tất toán về đúng không (dư nợ cuối kỳ sau khi trả hết, cổ tức tạm ứng quý không chi trả) | Đừng dùng cho giá trị THỰC RA khác không nhưng dưới ngưỡng làm tròn của cột - đó là hàng 2, gộp hai cái báo sai độ chính xác phép đo | Có, tự đọc được ngay vì là số bình thường, không cần tra chú thích |
| 2 | `0~` (số 0, hoặc số 0 kèm đúng số chữ số thập phân của cột, cộng dấu tilde ASCII ngay sau) | Khác không thật, nhưng dưới ngưỡng làm tròn hiển thị của cột | Cột tiền tỷ đồng mà giá trị gốc chỉ vài trăm triệu, cột phần trăm mà giá trị gốc dưới 0,05 | Đừng dùng tràn lan nếu PHẦN LỚN ô trong cột đều rơi vào trường hợp này - lúc đó đổi đơn vị cột (tỷ sang triệu) thay vì đánh dấu từng ô | Có, dấu tilde không phải em/en dash, không nhầm với số âm hay khoảng vùng |
| 3 | `.` (một dấu chấm, căn giữa ô, màu ink-faint) | Không áp dụng cho ngành/loại hình/giai đoạn này - một sự thật CẤU TRÚC | Chỉ tiêu ngân hàng (NPL, CASA, LDR) đặt cạnh doanh nghiệp phi ngân hàng trong cùng bảng; giai đoạn trước ngày niêm yết trong bảng so sánh chuỗi thời gian | Đừng dùng khi thực ra doanh nghiệp CÓ thể công bố nhưng chọn không công bố - đó là hàng 4, nhầm hai cái này là lỗi phổ biến nhất khi áp bảng vào thực tế | Cần một lần chú giải để phân biệt với hàng 4 (đếm 1 chấm so với 2 chấm), nhưng bản thân dấu chấm đơn lẻ rất khó nhầm với ký tự khác |
| 4 | `..` (hai dấu chấm liền nhau, cùng màu/cỡ với hàng 3) | Doanh nghiệp không công bố chỉ tiêu này - một LỰA CHỌN công bố, không phải sự thật cấu trúc | Biên lợi nhuận theo mảng khi doanh nghiệp không tách báo cáo bộ phận, dư nợ trái phiếu khi không thuyết minh chi tiết | Đừng cố thêm một mức thứ ba bằng ba dấu chấm "..." để phân biệt tinh hơn - đếm chấm chỉ còn đáng tin tới 2 mức khi in nhỏ hoặc photocopy nhiều lần, mức thứ ba phải đổi hẳn ký tự khác (xem hàng 6) | Cần chú giải một lần; đếm 2 chấm so với 1 chấm vẫn ổn định khi in, KHÔNG mở rộng thêm mức thứ ba bằng cách đếm |
| 5a | Chấm tròn hồng nhạt (khoen rỗng, vẽ bằng `<div>` hoặc `<span>` có khai `display:inline-block` tường minh - xem bẫy kỹ thuật ở `FINDINGS.md` mục 0) + hậu tố "chưa tới kỳ", màu ink-lo, không viền | Kỳ báo cáo chưa kết thúc, hoặc đã kết thúc nhưng còn trong hạn công bố (20/30 ngày theo Thông tư 96/2020/TT-BTC) | Doanh nghiệp mới niêm yết trong quý hiện tại, hoặc đang trong cửa sổ chờ hợp lệ | Đừng dùng cho doanh nghiệp đã quá hạn công bố thật - đó là hàng 5b, dùng chung ký hiệu này sẽ che giấu một tín hiệu quy trình thật cần chú ý | Có, hình khoen tròn tự đọc được là "đang mở/chờ", chữ "chưa tới kỳ" xác nhận thêm |
| 5b | Cùng khoen tròn hồng nhạt, NHƯNG đặt trong ô/thẻ có VIỀN ĐẶC màu `--warn` (vàng đồng), hậu tố "quá hạn" in đậm | Đã vượt mốc 20/30/45/60 ngày theo Thông tư 96/2020/TT-BTC mà chưa công bố | Chỉ dùng khi đã vượt hạn một khoảng đủ rõ (khuyến nghị từ 5 ngày trở lên) để loại trừ sai số hành chính/lệch múi giờ nộp hồ sơ | Đừng dùng viền `--neg` (đỏ) hay dấu chấm than - quá hạn là tín hiệu QUY TRÌNH cần theo dõi, chưa phải kết luận xấu đã xác nhận về kết quả kinh doanh, xem `FINDINGS.md` mục 5.3 | Viền đặc vẫn nổi rõ khi in đen trắng (khác biệt hình dạng viền, không chỉ màu); nếu ảnh mất màu hoàn toàn, viền liền nét vẫn phân biệt được với ô không viền của hàng 5a |
| 6 | `†` (dagger, màu ink-lo, đặt trong ô có viền hairline màu ink-lo trung tính - không phải màu warn) | Nhóm biên soạn báo cáo CHƯA THU THẬP ĐƯỢC, dữ liệu có tồn tại ngoài đời nhưng chưa lấy vào bài - lỗi/thiếu sót của người làm báo cáo, không phải của nguồn | Dữ liệu chắc chắn có công bố công khai nhưng đội biên soạn chưa kịp đối chiếu tới hạn chốt báo cáo | Đừng dùng cho trường hợp thực ra doanh nghiệp không công bố (đó là hàng 4) - dùng nhầm sẽ đổ lỗi sai đối tượng, và đừng dùng dấu "*" vì ký hiệu đó đã có nghĩa khác trong repo (đánh dấu tên doanh nghiệp/mã minh hoạ hư cấu, xem `samples/source-neo-so-van-xuoi.html`) | Cần chú giải một lần; dagger là ký tự phổ quát trong xuất bản (thứ hai sau dấu hoa thị), đã verify render đúng qua WeasyPrint 69.0 bằng trích xuất text |

## Loại thứ bảy, ngoài bảng chính, xử lý bằng câu văn tại chỗ

Vắng mặt vì một CHỈ SỐ PHÁI SINH (P/E trượt bốn quý, biên EBITDA luỹ kế mười hai tháng...) chưa
đủ số kỳ liên tục để tính, dù từng kỳ input đã công bố đầy đủ đúng hạn. Không có ký hiệu riêng
trong bảng chính vì tần suất thấp và bối cảnh luôn cần giải thích dài hơn một ký hiệu cho phép -
xử lý bằng chuỗi chấm đếm được (ví dụ ●●○○ cho "2/4 quý đã có") cộng một câu giải thích đầy đủ.
Xem lý do đầy đủ và ví dụ tại `FINDINGS.md` mục 1.4 và `samples/empty-trang-thai-rong-toan-phan.html`.
Nếu một loại báo cáo cụ thể (ví dụ chuyên trang doanh nghiệp mới niêm yết) gặp tình huống này
thường xuyên, cân nhắc chính thức hoá thành ký hiệu riêng - đến lúc đó chưa cần.

## Nguyên tắc phân bổ trọng lượng thị giác: tần suất và rủi ro quyết định độ terse

Không phải ngẫu nhiên hàng 1-4 chỉ dùng ký tự thuần (số hoặc dấu chấm, không viền, không màu
cảnh báo) còn hàng 5b-6 dùng thêm viền: hàng 1-4 là những trạng thái TẦN SUẤT CAO (xuất hiện
nhiều ô mỗi bảng) và RỦI RO THẤP nếu bị lướt qua (không áp dụng/không công bố là sự thật tĩnh,
không đổi theo thời gian đọc), nên ký hiệu phải TỐI GIẢN để không làm đặc bảng. Hàng 5b và 6 là
TẦN SUẤT THẤP nhưng RỦI RO CAO nếu bị lướt qua (một cái là tín hiệu cần theo dõi về doanh nghiệp,
một cái là lời thú nhận về chính báo cáo), nên được phép "tốn" thêm diện tích viền để không bị bỏ
sót. Khi thiết kế thêm ký hiệu mới ngoài bảng này, giữ đúng nguyên tắc: tần suất cao ép terse,
rủi ro cao ép nổi bật, đừng đảo ngược.

## Câu chú thích mẫu, đặt một lần dưới mỗi bảng dùng bộ ký hiệu này

```
0 đúng bằng không · 0~ khác không nhưng dưới ngưỡng làm tròn của cột ·
. không áp dụng cho loại hình này · .. doanh nghiệp không công bố chỉ tiêu này ·
○ chưa tới kỳ kỳ báo cáo chưa kết thúc hoặc còn trong hạn 20 ngày (30 ngày nếu là công ty mẹ) ·
○ quá hạn đã qua hạn công bố theo Thông tư 96/2020/TT-BTC mà chưa có số ·
† nhóm biên soạn chưa thu thập được, không phải doanh nghiệp không công bố
```

Xem bản render thật của câu chú thích này trong `samples/empty-bang-sau-loai-vang-mat.html`.

## Đối chiếu nhanh với sáu câu hỏi gốc

| Câu hỏi gốc | Trả lời bằng hàng nào |
|---|---|
| Doanh nghiệp không công bố chỉ tiêu này | Hàng 4 (`..`) |
| Chỉ tiêu không áp dụng cho ngành/loại hình này | Hàng 3 (`.`) |
| Bằng đúng số không | Hàng 1 (`0`) |
| Quá nhỏ nên làm tròn về không | Hàng 2 (`0~`) |
| Chưa tới kỳ báo cáo | Hàng 5a (khoen tròn, không viền) |
| Ta chưa lấy được dữ liệu | Hàng 6 (`†`) |
| (thêm, không có trong sáu câu gốc) Đã tới kỳ mà chưa công bố | Hàng 5b (khoen tròn, viền `--warn`) |
