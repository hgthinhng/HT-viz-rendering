# Chart đặc thù thị trường Việt Nam mà chuẩn sell-side phương Tây bỏ sót

Góc này chưa nguồn nào trong repo phủ. Bảng tra `03-chart-doctrine/CHART-SELECTION.md` dựng theo
FT Visual Vocabulary, còn 48 component matplotlib là bộ institutional phương Tây. Cả hai đều
không có chỗ cho những thứ mà một nhà phân tích Việt Nam xem đầu tiên mỗi sáng.

Mỗi mục dưới đây đã kiểm nguồn dữ liệu thật. Chỗ nào không có nguồn thì ghi rõ là không có.

## Tám ứng viên, kèm khả dụng dữ liệu

### A. Khối ngoại mua bán ròng theo phiên, kèm luỹ kế

Đây là chỉ số nhà đầu tư Việt Nam xem trước nhất, và nó **không tồn tại như một chỉ số hàng
ngày** trong template báo cáo Mỹ hay Âu, nơi dòng vốn ngoại là chuyện quý chứ không phải chuyện
phiên.

Dữ liệu hạng S, HOSE và HNX công bố cuối phiên miễn phí, tần suất T+0.

Cách vẽ: cột mỗi phiên (dương là mua ròng, âm là bán ròng) cộng đường luỹ kế trên trục phụ.
Đây là **trường hợp hai trục HỢP LỆ**, vì hai chuỗi khác loại phép đo, khác hẳn cái bẫy hai
trục tạo tương quan giả mà hồ sơ vòng 03 cảnh báo. Phải ghi rõ điều này trong catalog để người
sau không tưởng đây là ngoại lệ tuỳ tiện.

Bẫy riêng: giá trị mua bán ròng công bố thường lẫn cả giao dịch thoả thuận. Một thương vụ
chuyển nhượng chiến lược có thể chiếm phần lớn "mua ròng" của cả phiên mà không phải dòng tiền
thị trường thật. Luôn tách lớp khớp lệnh và thoả thuận, xem mục E.

### B. Room ngoại còn lại theo mã và theo ngành

Gắn thẳng với chất xúc tác lớn nhất mà chính tài liệu domain của repo đã nêu: nâng hạng thị
trường và dòng vốn thụ động đi kèm.

Dữ liệu hạng S và hạng 1: bảng giá HOSE và HNX hiển thị room còn lại theo thời gian thực, VSDC
công bố tỷ lệ sở hữu nước ngoài theo tháng.

Cách vẽ: bullet chart mỗi mã một hàng (đã dùng bao nhiêu, còn lại bao nhiêu, trần là bao nhiêu),
dựng thẳng từ `03-bullet.mjs` sẵn có, **không cần preset mới**. Đáng chú ý: đây chính là loại
dữ liệu hay bị vẽ thành gauge nhất, vì nó là một mức trên một trần. Chốt bullet để chặn trước.

### C. Cơ cấu sở hữu nhà nước và cổ đông lớn

Dữ liệu ad hoc theo sự kiện chứ không phải chuỗi thời gian đều: cổ đông từ 5% trở lên phải công
bố khi thay đổi qua ngưỡng 1%. Đây là điểm yếu về tần suất, phải nói rõ khi dùng.

Cách vẽ: cột chồng 100% một cột, dùng `11-stacked-100.mjs` sẵn có.

### D. Thanh khoản theo rổ VN30 và theo nhóm vốn hoá

Tính lại được từ dữ liệu cuối phiên cộng rổ VN30 công khai, tần suất ngày. Trả lời đúng câu hỏi
mà môi giới Việt Nam hỏi hằng tuần: dòng tiền đang luân chuyển đi đâu.

Cách vẽ: vùng chồng theo thời gian cho tỷ trọng ba nhóm, dùng `12-area-stack.mjs`.

### E. Giá trị thoả thuận so với khớp lệnh

Hai sàn tách riêng hai loại này trên bảng giá cuối phiên, miễn phí, tần suất ngày.

Cách vẽ: cột chồng hai phần mỗi phiên, hoặc đường tỷ lệ thoả thuận trên tổng để bắt đột biến.
Đột biến thường là dấu hiệu chuyển nhượng nội bộ chứ không phải cầu thị trường thật.

### F. Biến động phiên định kỳ mở cửa và đóng cửa

**Yếu nhất trong danh sách, và lý do đáng ghi.** Giá dự kiến hiển thị theo thời gian thực trong
15 phút mỗi phiên định kỳ, nhưng **không có nguồn lưu trữ lịch sử công khai đáng tin** cho giá
dự kiến đó. Muốn có thì phải tự thu theo thời gian thực. Repo không được giả định có sẵn dữ liệu.

Nếu có dữ liệu thì đây không phải chart mới mà là một lớp chú thích trên chart giá trong ngày,
và nhãn phải ghi rõ "giá dự kiến, chưa khớp". Điều này khớp với một bài học đã có trong sổ:
phiên định kỳ có giá hiển thị nhưng khối lượng luỹ kế bằng 0, từng làm báo sai vùng mua.

### G. Dư nợ ký quỹ toàn thị trường

Dữ liệu quý, tổng hợp từ báo cáo tài chính của các công ty chứng khoán niêm yết. Đây **là ước
tính tổng hợp, không phải số liệu công bố tập trung của cơ quan quản lý**, phải ghi rõ nguồn khi
vẽ.

Cách vẽ: cột theo quý, phủ chỉ số thị trường trên trục phụ để thấy quan hệ giữa chu kỳ ký quỹ
và pha nóng của thị trường. Khung lý thuyết **đã có sẵn** trong tài liệu chu kỳ tín dụng của
repo, chỉ cần nối dữ liệu, không tốn công nghiên cứu thêm.

### H. Lịch cổ tức và pha loãng do phát hành thêm

Tổng hợp từ công bố thông tin bắt buộc, có ngày giao dịch không hưởng quyền và mức chi trả.

Đây là hai nhu cầu tách biệt: một là dải lịch theo tuần (gần với lịch chất xúc tác hơn là chart
số liệu), hai là chart pha loãng dạng dumbbell trước và sau, hoặc waterfall cho phần trăm pha
loãng lên lợi nhuận mỗi cổ phần khi có phát hành thêm, quyền chọn nhân viên, hoặc chuyển đổi
trái phiếu.

## Nếu chỉ làm được ba

1. **Khối ngoại mua bán ròng theo phiên.** Phổ biến nhất trong thực hành hằng ngày, dữ liệu
   hạng S miễn phí theo ngày, không có thứ tương đương trong template phương Tây.
2. **Dư nợ ký quỹ theo quý.** Chi phí dựng thấp vì khung lý thuyết đã nằm sẵn trong kho, chỉ
   cần nối dữ liệu.
3. **Room ngoại còn lại.** Gắn với chất xúc tác nâng hạng mà chính tài liệu domain của repo đã
   đánh dấu, và dựng được ngay từ preset bullet sẵn có.

Điểm đáng chú ý về chi phí: **ba việc này gần như không cần preset mới**. Chúng dùng lại bullet,
cột chồng 100%, và vùng chồng đã có. Cái thiếu là quy ước dữ liệu và spec catalog, không phải
code vẽ.

## Quy ước số liệu Việt Nam ảnh hưởng tới trục và nhãn

- Đơn vị: tỷ đồng cho doanh nghiệp, nghìn tỷ đồng cho toàn thị trường. Đừng dùng triệu đồng cho
  số toàn thị trường vì trục sẽ dài vô lý.
- Dấu phân cách **ngược với tiếng Anh**: dấu phẩy là thập phân, dấu chấm là hàng nghìn. Đã kiểm
  code: `charts/echarts/fmt.mjs` xử lý đúng qua locale tiếng Việt. Đây là chỗ repo đã làm đúng
  sẵn. Nhưng mọi chart Việt Nam thêm mới **phải gọi qua `fmt.mjs`**, không được tự viết định
  dạng riêng.
- Mã chứng khoán ba ký tự viết hoa cố định, nhãn trục nên viết hoa cứng, ghi kèm sàn khi có
  nguy cơ trùng mã.
- Năm tài chính: đa số doanh nghiệp Việt Nam trùng năm dương lịch nhưng có ngoại lệ. Không được
  mặc định quý một là tháng 1 tới tháng 3 cho mọi doanh nghiệp khi vẽ trục quý.

## Bốn cạm bẫy dữ liệu mà chart phải phòng

1. **Giá sau chia tách và cổ tức.** Chuỗi giá dài phải dùng giá điều chỉnh, nếu không sẽ hiện
   một cú sụt giả đúng ngày giao dịch không hưởng quyền. Chart phủ nhiều mã phải chú thích rõ
   đang dùng giá gốc hay giá điều chỉnh.
2. **Giá phiên định kỳ là giá dự kiến.** Lọc theo khối lượng luỹ kế lớn hơn 0 trước khi coi là
   giá đã giao dịch thật.
3. **Chuỗi lịch sử ngắn của mã mới niêm yết.** Cần lối thoát rõ ràng kiểu "không đủ kỳ để vẽ xu
   hướng" thay vì nội suy hoặc để trống gây hiểu nhầm.
4. **Hợp nhất mẹ con và sở hữu chéo.** Cộng gộp cấp tập đoàn dễ đếm hai lần khi công ty con
   cũng niêm yết riêng.

## Chỗ không có nguồn, ghi rõ để không ai tưởng là đã kiểm

- Danh sách đầy đủ doanh nghiệp Việt Nam có năm tài chính lệch năm dương lịch.
- Nguồn lưu trữ lịch sử công khai cho giá dự kiến của phiên định kỳ mở cửa và đóng cửa.
