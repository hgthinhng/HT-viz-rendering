# Chọn hình theo câu hỏi

Chưng cất từ `research/03-chart-doctrine/`. Bản gốc có 24 nguồn khảo sát và phần phản biện;
đọc nó khi cần lý lẽ, đọc file này khi cần quyết định.

**File này KHÔNG liệt kê tên file preset.** Danh sách hình nào đã có là thứ đổi mỗi đợt, và mọi
bản chép tay của nó đều trôi: bảng gốc trong `research/` đến nay vẫn ghi "chưa có" cho boxplot
và fan chart, cả hai đã có từ lâu. Phần bền là ánh xạ từ câu hỏi sang HỌ HÌNH; phần biến động
tra ở `catalog/CATALOG.md`, thứ sinh tự động từ mã nguồn nên không lạc hậu được.

---

## 1. Luật gốc: đi từ câu hỏi, không đi từ dữ liệu

Sai lầm mặc định là nhìn dữ liệu rồi chọn hình quen tay. Đúng thứ tự là: viết ra câu hỏi người
đọc đang hỏi ở đúng chỗ đó, rồi mới tìm họ hình trả lời được câu hỏi ấy.

Không viết được câu hỏi thì hình đó không cần tồn tại. Đây cũng là phép thử cắt bớt hình nhanh
nhất khi ấn phẩm quá dày.

## 2. Tám nhóm câu hỏi

| Câu hỏi | Họ hình | Bẫy của nhóm này |
|---|---|---|
| Lệch bao nhiêu so với một mốc cố định | thanh hai phía trục 0, thanh phân kỳ xếp chồng | trục không đối xứng quanh 0 làm hai phía không so được |
| Hai đại lượng quan hệ thế nào | scatter, scatter bong bóng, ma trận tương quan | nhiều điểm chồng nhau; hai trục tung tạo tương quan giả |
| Vị trí trong danh sách quan trọng hơn giá trị | thanh xếp hạng, dumbbell, slope | sắp theo bảng chữ cái thay vì theo giá trị |
| Giá trị phân bố ra sao | dot strip, raincloud, ridgeline, hộp, histogram | hộp giấu cỡ mẫu nhỏ và giấu phân phối hai đỉnh; bin-width tuỳ tiện làm méo hình dạng |
| Xu hướng theo thời gian | đường có chú thích sự kiện, cột, nến, fan chart | không phân biệt số thực tế với số dự phóng |
| Một tổng thể phân rã thành các phần | thanh 100%, treemap, waffle | tròn và donut quá 3 lát; thứ tự xếp chồng đảo giữa các cột |
| So sánh độ lớn | thanh, bullet so với mục tiêu | trục không bắt đầu từ 0 với biểu đồ thanh |
| Khối lượng dịch chuyển giữa các trạng thái | sankey, alluvial | nhầm hai loại, xem mục 4 |

## 3. Ba nhóm đặc thù tài chính

Chuẩn phương Tây không tách riêng ba nhóm này, nhưng báo cáo tài chính dùng liên tục:

| Nhóm | Câu hỏi | Họ hình |
|---|---|---|
| Cầu nối tuần tự | một tổng số bị phân rã bởi các khoản cộng trừ theo thứ tự | waterfall |
| Định giá tổng hợp | nhiều phương pháp định giá cho ra vùng giá trị nào | football field |
| Độ nhạy | biến nào tác động mạnh nhất, hai biến cùng đổi thì sao | tornado một biến, lưới hai biến |

## 4. Hai cặp hay bị nhầm

**Sankey so với alluvial.** Sankey theo dõi MỘT đại lượng bảo toàn chảy qua các công đoạn khác
nhau: tiền, khối lượng, năng lượng. Alluvial theo dõi MỘT TẬP THỰC THỂ cố định bị phân loại lại
qua các mốc: cùng nhóm doanh nghiệp được xếp lại hạng qua ba năm. Ở sankey, tổng vào bằng tổng
ra vì đó là cùng một dòng. Ở alluvial, tổng mỗi mốc bằng nhau vì đó là cùng một tập được đếm
lại. Nhầm hai cái là nhầm bản chất đại lượng, không phải nhầm hình.

**Raincloud so với ridgeline.** Raincloud so vài nhóm KHÔNG có thứ tự. Ridgeline so nhiều kỳ CÓ
thứ tự và cố ý cho các hàng chồng lấn để mắt bắt được chuyển động của đỉnh. Dùng ridgeline cho
ba nhóm không thứ tự thì chồng lấn thành nhiễu chứ không thành thông tin.

## 5. Danh sách đen, có lý do

**Gauge.** Lãng phí diện tích cho một con số và mã hoá bằng góc, thứ mắt người đọc kém. Dùng
bullet: nó so thực tế với mục tiêu trên nền dải định tính, trong một phần diện tích.

**Radar.** Diện tích hình méo theo THỨ TỰ đặt trục, nên cùng một bộ số cho hai hình khác nhau
tuỳ người vẽ sắp trục thế nào. Dùng bảng khi cần đọc số, small multiples khi cần so hình dạng.

**Tròn và donut quá ba lát.** Mắt ước lượng góc kém hơn hẳn so chiều dài. Dùng thanh 100% khi
cần so nhiều kỳ, waffle khi cần người đọc nhớ con số.

**Hai trục tung trên một chart.** Thang của mỗi trục chọn được tuỳ ý, nên hình tạo ra tương quan
mà dữ liệu không có. Dùng hai chart xếp chồng chung trục thời gian.

**Chart 3D cho dữ liệu 2D.** Phối cảnh làm cột sau trông nhỏ hơn cột trước cùng giá trị.

## 6. Chú giải thẳng lên hình

Đặt nhãn ngay cạnh đường hoặc cột thay vì làm bảng chú giải riêng, bất cứ khi nào chỗ cho phép.
Bảng chú giải bắt mắt nhảy qua lại giữa hai vùng để đối chiếu màu, và mỗi lần nhảy là một cơ hội
đọc nhầm.

Chú giải riêng vẫn hơn khi: quá năm chuỗi, hoặc các chuỗi đan nhau dày tới mức không còn chỗ đặt
nhãn mà không chồng.

## 7. Số thực tế và số dự phóng phải khác nhau về NÉT

Phân biệt bằng nét liền so với nét đứt, hoặc bằng vùng nền, không phân biệt bằng riêng màu. Màu
mất khi in đen trắng và khoảng 8% nam giới không phân biệt được một số cặp màu.

Cùng nguyên tắc cho khoảng đứt dữ liệu: ba cách vẽ cho ba thông điệp khác nhau, và chọn nhầm là
nói sai. Xem `research/11-empty-states/ABSENCE-TABLE.md`.

## 8. Đọc mục lục trước khi dựng hình mới

`catalog/CATALOG.md` ghi từng tài sản kèm câu hỏi nó trả lời và khi nào đừng dùng nó. Đọc mục
lục mất hai phút và thường tìm ra thứ đã có. Dựng một hình mới trong khi thư viện đã có hình trả
lời đúng câu hỏi đó là thêm một chỗ để hai bản trôi khỏi nhau.

Khi thật sự cần hình mới, quy ước dựng nằm ở `CLAUDE.md` mục "Khi thêm chart".
