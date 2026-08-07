# Phản biện từ bốn mô hình ngoài về thứ tự mở rộng thư viện chart

Bốn worker nhận **cùng một prompt đầy đủ**, không chia góc, đúng luật broadcast. Bốn trên bốn
trả về nội dung dùng được. Sổ hiệu chuẩn: `bcast-0026`.

## Kết quả quan trọng nhất: 4/4 bác thứ tự ưu tiên của vòng 13

Vòng 13 xếp "vá lệch engine" lên đầu vì đó là lỗ hổng lớn nhất đếm được (43 trên 48 loại chưa
có bản ECharts). Cả bốn mô hình đều bác, và lý lẽ hội tụ:

> Lỗ hổng lớn nhất về SỐ LƯỢNG không phải lỗ hổng lớn nhất về GIÁ TRỊ.

Kimi nói thẳng nhất, và kiểm được: trong 43 loại chưa port, phần lớn là **đồ hoạ sơ đồ chứ
không phải chart dữ liệu** (`decision_tree`, `flowchart`, `maturity_ladder`, `mechanism_flow`,
`network_graph`, `swot`, `scenario_cards`, `cond_table`). Sơ đồ thì không có gì để hover hay
zoom, nên port sang bản tương tác là bỏ công vô ích. Con số 43 vì thế là một phép đếm gây hiểu
lầm chính người viết ra nó.

Đối chiếu thứ tự đề xuất:

| Vị trí | codex | agy | kimi | grok |
|---|---|---|---|---|
| 1 | Schema dữ liệu chung hai engine | Hộp tóm tắt điều hành | Hộp tóm tắt điều hành | Hộp tóm tắt điều hành |
| 2 | Line có chú thích | Bar ngang xếp hạng | Đường cong lãi suất | Bốn chart xương sống chung schema |
| 3 | Họ đường cong kỳ hạn | Line có chú thích | Vá lệch engine, chỉ 4 loại | Đường cong lãi suất |
| 4 | Bar ngang xếp hạng | Cleveland dot plot | Cleveland dot plot | Cleveland dot plot cộng ngữ pháp so sánh |
| 5 | Hộp tóm tắt điều hành và scatter phần tư | Đường cong lãi suất | Calendar heatmap và surprise chart | Catalyst timeline có độ lớn |

Đọc theo hàng: **hộp tóm tắt điều hành đứng đầu ở 3 trên 4**, và codex tuy xếp nó thứ 5 vẫn
viết rõ "nếu chỉ được chọn một trong hai thì chọn hộp tóm tắt điều hành trước". Tức thực chất
4/4 coi đây là việc số một.

Bất đồng thật sự chỉ còn một: **codex muốn làm schema dữ liệu dùng chung trước mọi thứ khác**,
ba mô hình kia bắt tay vào component ngay. Lý lẽ của codex đáng nghe và không mâu thuẫn với ba
mô hình kia: nếu mỗi preset tự định nghĩa đơn vị, kỳ báo cáo, giá trị thiếu, ngưỡng và nguồn,
thì thêm năm chart là thêm năm chỗ để bản HTML và bản PDF lệch nhau. Grok nói cùng ý bằng câu
khác: "schema trước preset, một schema dùng cho cả hai engine rẻ hơn 43 wrapper".

## Đề xuất bỏ hoặc gộp, xếp theo số phiếu

Đây là phần đắt nhất của broadcast, vì nó động tới thứ đang có chứ không phải thứ chưa có.

| Đề xuất | Ai nêu | Lý lẽ |
|---|---|---|
| Bỏ hoặc gộp `candlestick` | agy, kimi | Nến Nhật phục vụ phân tích kỹ thuật ngắn hạn, không nằm trong 10 loại báo cáo trừ hàng hoá và ngoại hối, mà ở đó thường cần giá đóng cửa hơn |
| Hạ vai trò `treemap` | kimi, codex | Chỉ hợp cơ cấu một tầng; hai tầng trở lên người đọc mất khả năng so sánh diện tích |
| Bỏ `executive_summary` và `swot` khỏi tầng matplotlib | agy | Matplotlib là công cụ vẽ đồ thị toán học, dùng nó kết xuất đoạn văn tiếng Việt dài là sai kiến trúc; khối văn bản thuộc tầng HTML |
| Bỏ `marimekko` | agy | Ép người đọc so sánh diện tích hai chiều cùng lúc, cùng đúng cái lý do repo đã cấm radar |
| Gộp `lollipop` với `range_dot` | agy | Lollipop chỉ là cột mảnh gắn chấm, không cho góc nhìn mới |
| Gộp `spread`, `spread_ladder`, `football_field` | kimi | Cùng họ biểu diễn khoảng giá trị, nên là một component với chế độ hiển thị khác nhau |
| Gộp `stat_dashboard`, `exec_dashboard`, `hero_stat` | kimi | Cùng là lưới chỉ số, khác mỗi kích thước thẻ |
| Đóng băng `decision_tree`, `network_graph`, `mechanism_flow`, `flowchart` | kimi | Đồ hoạ sơ đồ, ứng viên hàng đầu cho "trông chuyên nghiệp nhưng nói rất ít" |
| Siết `lorenz`, `spc_control_chart`, `fan` | kimi | Dễ bị dùng để trang trí tính học thuật, hoặc dễ bị đọc nhầm giới hạn kiểm soát thành giới hạn dự báo |

Không đề xuất nào đạt 3/4 phiếu, nên theo luật consolidate thì **không cái nào là bắt buộc**.
Nhưng hai cái đáng nhận dù chỉ một phiếu, vì lý lẽ tự đứng được:

- Bỏ `executive_summary` và `swot` khỏi matplotlib. Đây không phải chuyện khẩu vị: repo vừa
  phải nhúng font riêng cho matplotlib để chữ tiếng Việt không mất dấu, và càng ít văn bản dài
  đi qua đường đó thì càng ít bề mặt hỏng.
- Bỏ `marimekko`. Nếu giữ nó trong khi cấm radar thì lệnh cấm mất tính nhất quán, và một lệnh
  cấm không nhất quán sẽ bị người dùng thư viện coi thường.

## Cạm bẫy thi công đáng giữ, gom từ cả bốn

**Trục kỳ hạn của đường cong lãi suất: đa số ngoài SAI, đã phân xử ngược lại.** Ba mô hình độc
lập cùng cảnh báo rằng trục hạng mục bóp méo hình học, vì 1 tháng tới 3 tháng và 5 năm tới 10
năm sẽ chiếm cùng một khoảng ngang, nên phải quy về dải số học theo số tháng. Xét như một
nguyên tắc chung thì họ đúng.

Nhưng khảo sát nội bộ trên dữ liệu thị trường Việt Nam kết luận ngược, và kết luận đó thắng.
Lý do là ngữ cảnh mà ba mô hình ngoài không có: **trái phiếu chính phủ Việt Nam gần như không
có kỳ hạn 1 tháng, 3 tháng, 6 tháng ở thị trường thứ cấp**. Dải thật chỉ từ 1 năm tới 20 năm.
Phép méo mà ba mô hình cảnh báo lớn nhất đúng ở đoạn cực ngắn, mà đoạn đó không tồn tại ở đây.
Đổi lại, trục tuyến tính sẽ dồn toàn bộ vùng 1 tới 10 năm, nơi chứa mọi tín hiệu chính sách
tiền tệ và chu kỳ tín dụng, vào một phần ba bề rộng chart, nhường hai phần ba còn lại cho vùng
15 tới 20 năm vốn chỉ có một nhóm mua và thanh khoản rất thấp.

Thêm hai căn cứ: đây là quy ước mà FT, Bloomberg và FRED đang dùng khi xuất bản đường cong lợi
suất, và cũng là cách các báo cáo môi giới Việt Nam đang vẽ. Đổi quy ước sẽ bắt người đọc giải
mã thay vì đọc ngay hình dạng.

Quyết định: **dùng trục hạng mục**, kèm ràng buộc bắt buộc mà khảo sát nội bộ tự đặt ra: không
được đọc độ dốc trên chart như số điểm cơ bản trên năm, và luôn kèm bảng số liệu. Ghi lại bất
đồng này ở đây vì nó là ví dụ tốt cho lần sau: bốn mô hình ngoài rất mạnh về nguyên tắc chung
nhưng không biết dải kỳ hạn thật của thị trường Việt Nam, nên phiếu của chúng nhẹ hơn một khảo
sát đọc thẳng tài liệu thị trường.

Kimi vẫn đúng ở một điểm liên quan, và điểm đó được nhận: đừng nối spline mượt qua các điểm kỳ
hạn rời rạc, vì đó là bịa dữ liệu ở khoảng giữa. Nối thẳng và chấm rõ từng điểm kỳ hạn thật.

**Nhãn tiếng Việt trong bar ngang và scatter.** Tên đầy đủ kiểu "Ngân hàng Thương mại Cổ phần
Ngoại thương Việt Nam" dài gấp ba nhãn tiếng Anh. agy đề xuất đặt nhãn nằm trên thanh thay vì
bên trái trục. Kimi đi xa hơn và đúng hơn: rút gọn phải làm ở **tầng dữ liệu** bằng mã chứng
khoán chuẩn hoá, không xử lý ở tầng hiển thị, vì thuật toán tránh đè nhãn của ECharts hoạt động
kém với chuỗi dài có dấu.

**Phân biệt hai kỳ đo khi in đen trắng.** agy và kimi cùng chỉ ra: mực `#051C2C` và nhấn
`#2251FF` in đen trắng ra hai mảng xám gần như nhau. Cách duy nhất chắc chắn là chấm đặc cho kỳ
hiện tại, chấm rỗng viền đậm cho kỳ trước.

**Xếp hạng đa tiêu chí khác đơn vị.** Kimi bắt được một cái bẫy tinh vi: nếu Cleveland dot plot
xếp hạng theo giá trị mà các tiêu chí khác đơn vị (một cái là phần trăm, một cái là điểm số),
thì ta vừa tạo ra đúng thứ vô nghĩa mà radar bị cấm vì nó. Phải chuẩn hoá về thang chung hoặc
chia nhóm theo đơn vị.

**Ngắt trang hộp tóm tắt điều hành.** Cả agy và kimi cảnh báo hộp dài nửa trang bị cắt ngang khi
in. Kimi thêm một chi tiết thực dụng: đừng dùng nền xám nhạt tạo khối vì mực laser trên nền xám
in ra bẩn, dùng viền trái đậm thay thế.

## Gợi ý mới, lọc theo mức đáng làm

Bốn mô hình đề xuất tổng cộng mười lăm thứ mới. Sau khi lọc trùng và lọc những cái repo đã có,
còn lại năm cái đáng cân nhắc:

| Đề xuất | Ai nêu | Đánh giá |
|---|---|---|
| Biểu đồ độ lệch kỳ vọng (thực tế so với dự báo đồng thuận) | kimi | Đáng làm, nhưng kèm ràng buộc bắt buộc, xem cảnh báo dưới |
| Bản đồ nhiệt mùa vụ theo tháng và năm | kimi | Đáng làm cho hàng hoá và vĩ mô, thang xám đơn sắc |
| Bảng số liệu phân cấp tài khoản | agy | Rất hợp báo cáo tài chính Việt Nam, phân cấp bằng lùi lề tĩnh chứ không bằng nền màu |
| Ma trận kỳ hạn và độ nhạy | codex | Thay thế tốt cho nhu cầu nhiều gauge, giữ được hai chiều độc lập |
| Dải bằng chứng theo luận điểm | codex | Thuộc tầng component, nối luận điểm với số liệu chứng minh |

Bốn thứ bị loại vì repo đã có: `connected_scatter` (agy đề xuất, đã có ở matplotlib), waterfall
có tổng phụ (kimi, đã có), index tái cơ sở 100 (kimi, đã có `index100`), scatter phần tư (codex,
đã nằm trong P0 vòng 13).

Hai thứ bị loại vì mâu thuẫn ràng buộc cứng: ridgeline (agy) chồng nhiều phân phối bán trong
suốt, mà WeasyPrint xử lý trộn màu in đè kém, chính agy cũng cảnh báo điều này trong phần bẫy
của mình; waffle (agy) là biến thể đếm ô của biểu đồ tròn, và với hơn năm hạng mục thì đúng vào
lý do repo cấm pie nhiều lát.

## Cảnh báo dữ liệu quan trọng nhất, từ kimi

Về biểu đồ độ lệch kỳ vọng:

> Ở Việt Nam, consensus cho nhiều doanh nghiệp là không tồn tại hoặc chỉ từ một nhà phân tích
> duy nhất, và trình bày một ước tính đơn lẻ như "kỳ vọng thị trường" là gây hiểu sai.

Đề xuất kèm theo đáng đưa thẳng thành luật của component: bắt buộc có trường nguồn kỳ vọng và
số lượng ước tính tham gia, và **từ chối vẽ** khi chỉ có một nguồn. Đây là kiểu ràng buộc mà
repo đã quen: gate phải thành thật về giới hạn của chính nó thay vì vẽ ra một con số trông có
vẻ chắc chắn.
