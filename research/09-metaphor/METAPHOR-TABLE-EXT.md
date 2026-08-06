# BẢNG TRA ẨN DỤ MỞ RỘNG — VÒNG 09, NGOÀI 11 HÌNH HIỆN CÓ

Bảng này KHÔNG thay thế `illustrations/metaphor-table.md` (file gốc không được sửa trong vòng
này). Đây là phần MỞ RỘNG: các ngành/luận điểm CHƯA có dòng nào trong bảng gốc, hoặc có dòng
văn bản trong bảng gốc nhưng CHƯA có file SVG tương ứng trong `illustrations/svg/`.

Mỗi dòng đã chạy đủ BA BÀI TỰ KIỂM của `illustrations/grammar.md` và ghi KẾT QUẢ TỪNG BÀI, không
nói chung chung "đã kiểm". Ba bài, nhắc lại cho tiện tra:

1. **Che chữ**: xoá hết `<title>`/`<desc>`/nhãn, nhìn silhouette còn đọc ra biến cấu trúc không.
2. **Đổi ngành**: đổi nhãn sang ngành khác, hình có còn "chạy" (đọc đúng nghĩa) không. Nếu có
   thì đó là trang trí.
3. **Chart giả**: hình có vô tình chứa gauge, radar, pie/donut nhiều lát, trục cắt cụt, hay
   dual-axis tự scale không (xem `research/03-chart-doctrine/FINDINGS.md` muc 3).

## Phần A — 3 ngành đã dựng SVG mẫu đầy đủ (xem `samples/metaphor-*.html`)

### 1. Dệt may / may mặc xuất khẩu

**Vật thể**: nhà máy may xuất khẩu, nhìn mở mặt trước, từ kho cuộn vải tới cửa xuất hàng.
**File**: `research/09-metaphor/svg/textile-garment-factory.svg`, demo `samples/metaphor-det-may.html`.

| Bộ phận | Biến neo |
|---|---|
| Chiều cao chồng cuộn vải ở kho đầu vào | Tồn kho nguyên vật liệu / tỷ lệ NVL trên giá vốn |
| Số trạm may "sáng" so với "tắt" trên dây chuyền (module lặp 6 lần, biến thiên màu) | Công suất sử dụng dây chuyền |
| Tỷ lệ màu kiện hàng ở khu đóng gói (đậm = FOB, xám = CMT) | Cơ cấu doanh thu theo phương thức FOB/CMT |
| Xe tải đang xếp + khối nét đứt phía sau (quy ước "chờ/dự kiến" đã dùng trong thư viện gốc) | Đơn hàng tồn đọng (backlog) chờ giao |

- **Bài 1 (che chữ)**: ĐẠT. 4 vùng đọc được từ silhouette: chồng hình viên thuốc tròn đầu = cuộn
  vải, dãy trụ nhỏ đều có đầu kim = dây chuyền với 1 điểm khác màu, khối hộp 2 tông xen kẽ = kiện
  hàng phân loại, xe + 2 khung nét đứt = hàng đợi.
- **Bài 2 (đổi ngành)**: ĐẠT. Cuộn vải có đầu xoáy trôn ốc không đổi được thành cuộn giấy/thép
  mà giữ nguyên nghĩa; nhãn FOB/CMT là thuật ngữ CHỈ tồn tại ở gia công xuất khẩu dệt may.
- **Bài 3 (chart giả)**: ĐẠT. Không gauge/radar/pie. Trạng thái tram may mã hoá bằng màu + vị trí
  cố định (họ bullet-chart), không phải góc quay.
- **Khi nào KHÔNG dùng**: doanh nghiệp CMT thuần không có đơn FOB (mất 1/4 biến); nganh sợi/dệt
  thượng nguồn (trước công đoạn vải cuộn thành phẩm).

### 2. Thuỷ sản chế biến xuất khẩu (chuỗi lạnh)

**Vật thể**: nhà máy chế biến thuỷ sản đông lạnh, từ sân tiếp nhận nguyên liệu tới container lạnh
chờ xuất.
**File**: `research/09-metaphor/svg/seafood-coldchain-plant.svg`, demo `samples/metaphor-thuy-san.html`.

| Bộ phận | Biến neo |
|---|---|
| Chiều cao chồng khay/kết ướp đá ở sân tiếp nhận | Sản lượng nguyên liệu thu mua (nuôi trồng/đánh bắt) |
| Số bàn phi lê "sáng" so "tắt" trên dây chuyền | Công suất chế biến sử dụng |
| Mức xếp hàng đông lạnh nhìn qua cửa kho mở (thang mã hoá bằng VỊ TRÍ, không phải kim đồng hồ) | Tồn kho thành phẩm đông lạnh (số ngày tồn kho) |
| Số container lạnh (reefer, có suốn kẻ sườn + khối máy làm mát riêng) + màu nhãn trên đỉnh | Cơ cấu doanh thu xuất khẩu theo thị trường |

- **Bài 1**: ĐẠT. Khối tường dày với "cửa sổ" xếp tầng chứa hàng bên trong đọc được ngay là kho
  lạnh; container có suốn sườn + khối nhô 1 đầu đọc được là thiết bị lạnh, khác hẳn container khô.
- **Bài 2**: ĐẠT. Container lạnh KHÔNG đổi được thành container khô của `logistics-container-ship.svg`
  mà giữ nguyên nghĩa (suốn sườn + khối máy lạnh là chi tiết vật lý thật riêng của reefer).
- **Bài 3**: ĐẠT, có 1 quyết định thiết kế đáng ghi lại: bản nháp đầu dự định gắn nhiệt kế tường
  cho kho lạnh, đã BỎ vì một đồng hồ tương tự (kim/vạch chia độ) dễ trượt thành dạng gauge bị cấm
  dù hình dạng khác (thang dọc thay vì mặt tròn); thay bằng mức xếp hàng trong khung cửa, an toàn
  tuyệt đối với luật cấm gauge.
- **Khi nào KHÔNG dùng**: doanh nghiệp chỉ nuôi trồng/đánh bắt không tự chế biến (mất 2/4 biến);
  doanh nghiệp chỉ bán nội địa (mất biến thị trường xuất khẩu); nganh khai thác xa bờ (khâu trước
  cả sân tiếp nhận trong hình này).

### 3. Bảo hiểm (cơ chế dự phòng nghiệp vụ)

**Vật thể**: hệ 2 bể chứa nối ống, mô phỏng cơ chế phí bảo hiểm gộp vào, dự phòng nghiệp vụ, chi
bồi thường, và nhượng tái bảo hiểm.
**File**: `research/09-metaphor/svg/insurance-reserve-tank.svg`, demo `samples/metaphor-bao-hiem.html`.

| Bộ phận | Biến neo |
|---|---|
| Ống dẫn lớn + van bánh xe ở góc trên trái, chảy vào đỉnh bể chính | Phí bảo hiểm gốc thu được (gross written premium) |
| Chiều cao chất lỏng trong bể chính | Dự phòng nghiệp vụ (net technical reserves) hiện có |
| Ống xả đáy bể chính, chảy xuống bể hứng | Chi trả bồi thường (claims paid) / tỷ lệ bồi thường |
| Ống tràn nghiêng nối sang bể phụ nhỏ hơn + mức nước riêng của bể phụ | Tỷ lệ nhượng tái bảo hiểm (ceded reinsurance ratio) |
| Cọc tiền nhỏ rót thêm vào bể chính từ ống phụ trên đỉnh | Thu nhập đầu tư trên quỹ dự phòng |

- **Bài 1**: ĐẠT. Đọc được ngay là sơ đồ công nghiệp bể-ống chuẩn (vào/trữ/tràn/ra) không cần chữ.
- **Bài 2**: ĐẠT NHƯNG CÓ GIỚI HẠN THẬT (xem chi tiết trong `samples/metaphor-bao-hiem.html` mục
  bài 2, không rút gọn ở đây để tránh nói chung chung): bản thân hình dạng "2 bể nối ống tràn"
  cũng mô tả được cơ chế hợp vốn ngân hàng (tiền gửi vào, cho vay ra, syndication sang ngân hàng
  khác) nếu đổi nhãn — đây là rủi ro thật, không phải hình học miễn nhiễm tuyệt đối với phép đổi
  ngành. Cái CỨU được bài kiểm là 2 chi tiết gắn chặt vào đối tượng: (a) "dự phòng nghiệp vụ" vốn
  LÀ thuật ngữ kế toán bảo hiểm mượn hình ảnh hồ chứa, không phải ẩn dụ tự nghĩ ra; (b) cơ chế
  "1 công ty chuyển giao rủi ro cho MỘT CÔNG TY KHÁC" qua hợp đồng nhượng tái là đặc thù bảo hiểm.
  Kết luận thực dụng: DÙNG ĐƯỢC nhưng LUÔN kèm nhãn chữ rõ ràng, không nên thả hình trần không chú
  thích như 2 mẫu logistics/dệt may/thuỷ sản.
- **Bài 3**: ĐẠT. Mức dự phòng mã hoá bằng vị trí mực nước trên trục thẳng (bullet-chart), không
  phải góc kim.
- **Khi nào KHÔNG dùng**: công ty giữ lại gần hết rủi ro, không mua tái bảo hiểm đáng kể (bể phụ
  gần như rỗng, mất 1/5 biến); bảo hiểm nhân thọ có sản phẩm liên kết đầu tư (cơ cấu dự phòng thật
  phức tạp hơn nhiều lớp, 1 bể đơn là đơn giản hoá quá mức); người đọc chưa quen thuật ngữ kỹ
  thuật bảo hiểm (hình dựa vào nhãn chữ để tách khỏi cơ chế tank+pipe chung chung, xem bài 2).

## Phần B — Ngành còn trống, mới dừng ở đề xuất bằng chữ (chưa dựng SVG trong vòng này)

| Ngành | Vật thể ẩn dụ | Bộ phận neo (≥4) | Bài 1 | Bài 2 | Bài 3 | Khi nào KHÔNG dùng |
|---|---|---|---|---|---|---|
| Chứng khoán / môi giới | Bàn giao dịch nhiều làn với cầu dao ngắt mạch (circuit breaker) ở giữa | (1) Chiều cao 4 làn tách biệt = 4 mảng doanh thu (môi giới/margin/tự doanh/IB); (2) vị trí cần gạt cầu dao (đóng/mở) = biên độ dao động đang bị chạm trần/sàn thật; (3) đồng hồ đếm khối lượng dạng cột (không phải kim) ở mỗi làn = giá trị giao dịch từng mảng; (4) dây nối làn "margin" tới 1 khối tài sản thế chấp riêng = dư nợ cho vay ký quỹ | ĐẠT — silhouette 4 làn + 1 cầu dao trung tâm đọc được là bảng điều khiển nhiều nhánh | ĐẠT có điều kiện — cầu dao ngắt mạch khi chạm biên độ ±7%/HOSE là quy định RIÊNG của sàn chứng khoán VN, không đổi được sang ngành khác mà giữ nghĩa "ngắt giao dịch theo biên độ"; nhưng silhouette "bảng điều khiển 4 làn" một mình thì trung tính, PHẢI giữ chi tiết cầu dao mới qua được bài này | ĐẠT nếu dùng cột/thanh cho khối lượng, THẤT BẠI nếu vẽ thành kim đồng hồ (dễ trượt thành gauge) | Công ty chứng khoán không có mảng tự doanh/IB đáng kể (chỉ còn 2-3 làn); báo cáo về Sở giao dịch (HOSE/HNX) chứ không phải 1 công ty chứng khoán cụ thể |
| Cao su tự nhiên | Vườn cao su theo lô tuổi cây + nhà máy sơ chế mủ (dây chuyền cán tờ/ly tâm) | (1) Số hàng cây theo lô, màu theo nhóm tuổi (kiến thiết cơ bản/khai thác/thanh lý) = cơ cấu diện tích theo tuổi vườn; (2) chiều cao chồng tờ mủ/khối mủ đã sơ chế = sản lượng mủ khai thác; (3) bồn ly tâm/cán tờ hoạt động hay không = công suất sơ chế; (4) xe bồn/thùng chở mủ tươi chờ nhập = tồn đọng thu mua | ĐẠT — hàng cây theo lô + nhà xưởng sơ chế đọc được là vườn công nghiệp | ĐẠT — cơ cấu tuổi vườn (kiến thiết cơ bản/khai thác/thanh lý) là thuật ngữ và chu kỳ sinh học riêng của cây cao su, không áp được cho ngành khác | ĐẠT, không gauge/pie | Doanh nghiệp cao su đã chuyển hẳn sang chế biến sâu (găng tay/nệm), không còn vườn cây trực canh — cần an dụ nhà máy cao su kỹ thuật riêng |
| Phân bón | Nhà máy tổng hợp NPK dạng tháp phối trộn + kho chứa rời (silo) theo loại phân | (1) Tỷ lệ 3 màu hạt trong tháp phối trộn (N xanh lá/P đỏ/K tím theo quy ước bao bì thật của ngành) = cơ cấu công thức NPK; (2) chiều cao silo mỗi loại phân = tồn kho theo chủng loại; (3) đường ống dẫn khí amoniac/khí gas đầu vào có van = chi phí nguyên liệu đầu vào (khí/than); (4) băng chuyền đóng bao ra cảng = sản lượng tiêu thụ | ĐẠT — tháp phối trộn 3 màu hạt + hàng silo đọc được là nhà máy hoá chất/phân bón | ĐẠT — mã màu N-P-K theo quy ước bao bì phân bón thật là đặc thù ngành, không tồn tại ở hoá chất công nghiệp khác | ĐẠT | Doanh nghiệp chỉ phân phối, không tự sản xuất (mất nhà máy, chỉ còn kho + logistics) |
| Hoá chất công nghiệp (xút, PVC...) | Cụm tháp phản ứng + bể điện phân (dạng công nghiệp thật của xút-clo) | (1) Số ngăn điện phân hoạt động/tổng số ngăn = công suất huy động; (2) 2 đường ống ra tách màu (clo vàng nhạt, xút trong) = tỷ trọng sản phẩm đồng hành; (3) áp kế... KHÔNG dùng kim, dùng cột đo áp dạng ống chữ U = áp suất vận hành; (4) bồn chứa thành phẩm theo loại = tồn kho theo sản phẩm | ĐẠT nếu vẽ đúng dạng bể điện phân nhiều ngăn (đặc trưng công nghệ chlor-alkali), THẤT BẠI nếu vẽ chung chung "nhà máy hoá chất" mù mờ | ĐẠT — bể điện phân nhiều ngăn với 2 đường ống ra khác màu là đặc trưng công nghệ xút-clo, không lẫn với nhà máy hoá chất khác | ĐẠT nếu dùng ống chữ U thay kim đồng hồ | Hoá chất chuyên ngành khác (sơn, chất tẩy rửa) có quy trình khác hẳn điện phân, cần vật thể riêng |
| Hàng không / vận tải hành khách | Thân máy bay cắt ngang theo hạng ghế (đã có trong `metaphor-table.md` dòng 21, CHƯA có SVG) | (1) Diện tích khoang thương gia so khoang phổ thông = cơ cấu doanh thu theo hạng ghế; (2) số ghế trống (màu nhạt) so ghế có khách (màu đậm) = hệ số lấp đầy (load factor); (3) khoang bụng chở hàng = doanh thu vận tải hàng hoá đi kèm; (4) số động cơ + kích thước = loại tàu bay/chi phí vận hành theo đội bay | ĐẠT — cutaway thân máy bay đọc được ngay là ngành hàng không | ĐẠT — bố trí hạng ghế + khoang bụng hàng là cấu trúc doanh thu ĐẶC THÙ hàng không, không map sang ngành khác | ĐẠT nếu hệ số lấp đầy vẽ bằng tỷ lệ diện tích/số ghế, THẤT BẠI nếu vẽ thành gauge "load factor" | Hãng bay chở hàng thuần (cargo airline), không có cấu trúc hạng ghế hành khách |
| Cảng biển / hạ tầng logistics | Cần cẩu giàn (gantry crane) trên ray + bãi container xếp so le (đã có trong `metaphor-table.md` dòng 2, CHƯA có SVG, KHÁC với tàu của logistics-container-ship.svg) | (1) Số cần cẩu đang hoạt động (cần vươn xuống bốc dỡ) so với đứng yên = công suất xử lý huy động; (2) chiều cao chồng container trên bãi theo khu vực = tồn bãi/tắc nghẽn; (3) tàu cập cảng (chỉ vẽ 1 phần mũi tàu ở rìa khung, không phải cả con tàu) = số cầu tàu đang khai thác; (4) đường ray cần cẩu dài bao nhiêu nhịp = quy mô bến cảng | ĐẠT — cần cẩu giàn trên ray là silhouette đặc trưng không lẫn vào đâu (khác hẳn cần cẩu tháp xây dựng hay cần cẩu tàu) | ĐẠT — cần cẩu giàn cụ thể (khung chữ A, ray chạy dọc cầu tàu) là thiết bị RIÊNG của cảng container, không dùng được cho kho bãi thường | ĐẠT | Cảng chuyên hàng rời/dầu khí (không dùng cẩu giàn container) |
| Khu công nghiệp / bất động sản KCN | Sơ đồ mặt bằng KCN nhìn từ trên xuống dạng ô lưới, mỗi ô là 1 lô đất | (1) Tỷ lệ ô đã tô đặc (đã cho thuê) so ô để trống (viền nét đứt) = tỷ lệ lấp đầy; (2) độ đậm màu mỗi ô theo ngành thuê (điện tử/dệt may/logistics) = cơ cấu khách thuê theo ngành; (3) đường giao thông nội khu + khoảng cách tới trục quốc lộ vẽ ở rìa = lợi thế vị trí; (4) khu xử lý nước thải tập trung ở góc = hạ tầng tiện ích đi kèm giá thuê | ĐẠT — lưới ô lô đất nhìn từ trên là silhouette bản đồ quy hoạch, không lẫn với nhà máy đơn lẻ | ĐẠT có điều kiện — bản thân "lưới ô đất nhìn từ trên, ô đặc/ô rỗng" khá gần với bài toán lấp đầy chung (có thể lẫn với "tỷ lệ lấp đầy văn phòng cho thuê"); CẦN giữ chi tiết khu xử lý nước thải tập trung + đường nội khu để khoá riêng vào KCN, nếu bỏ 2 chi tiết đó hình trượt về ẩn dụ bất động sản thương mại nói chung | ĐẠT nếu tỷ lệ lấp đầy vẽ bằng số ô, THẤT BẠI nếu rút gọn thành 1 con số kèm pie | KCN mới giải phóng mặt bằng, chưa có khách thuê nào (toàn bộ ô đều rỗng, hình chưa có gì để kể) |
| Xây lắp / nhà thầu EPC | Công trường với giàn giáo bọc quanh khung thép nhà xưởng đang dựng, cần trục bánh xích | (1) Số tầng khung thép đã dựng so với thiết kế tổng = % hoàn thành hợp đồng (progress billing); (2) chiều dài giàn giáo đã che phủ = khối lượng thi công đã nghiệm thu; (3) số công nhân/tổ đội quy ước bằng khối mũ bảo hộ nhỏ xếp hàng = nguồn lực huy động; (4) biển hiệu dự án ở cổng công trường = tên/quy mô hợp đồng đang thực hiện | ĐẠT — giàn giáo + khung thép dở dang đọc được ngay là công trường xây dựng | ĐẠT — cấu trúc "% hoàn thành theo tầng khung thép" gắn với phương pháp ghi nhận doanh thu progress billing đặc thù ngành xây lắp, không map trực tiếp sang sản xuất (dù CÓ độ gần với real-estate-apartment-crane.svg đã có, cần phân biệt rõ: BĐS là NGƯỜI MUA NHÀ, xây lắp là NHÀ THẦU ghi nhận doanh thu hợp đồng) | ĐẠT | Nhà thầu chuyên hạ tầng ngầm (đường ống, cống) không có silhouette khung thép nổi trên mặt đất |
| Thép (khác cấu trúc chung của manufacturing-factory-smokestack.svg) | Lò cao (blast furnace) + dây chuyền cán nóng/cán nguội ra cuộn thép | (1) Chiều cao mức liệu trong lò cao (quặng+than cốc) = tồn kho nguyên liệu đầu vào; (2) tia lửa/màu đỏ cam ở miệng lò = đang vận hành/công suất lò; (3) số cuộn thép cán ra xếp ở cuối dây chuyền, đường kính cuộn khác nhau = sản lượng theo loại sản phẩm (thép cuộn cán nóng/cán nguội); (4) ống khói thu hồi khí lò (khác ống khói thường, có bầu thu hồi) = mức độ tận dụng khí đồng hành/hiệu suất năng lượng | ĐẠT nếu vẽ đúng lò cao dạng bầu phình + dây chuyền cán cuộn (khác hẳn silhouette nhà xưởng mái răng cưa chung chung đã có) | ĐẠT — lò cao dạng bầu + cuộn thép cán là silhouette CHỈ CÓ ở luyện kim, không lẫn với nhà máy cơ khí/dệt may | ĐẠT | Nhà máy thép xây dựng (chỉ cán, không luyện từ quặng) — chỉ nên vẽ phần dây chuyền cán, bỏ lò cao |
| Bán lẻ hiện đại (chuỗi siêu thị, khác quầy đơn lẻ đã có) | Sơ đồ 1 dãy phố với nhiều biển hiệu cùng 1 thương hiệu lặp lại, có xe tải logistics nội bộ nối kho trung tâm | (1) Số biển hiệu "sáng" (đang hoạt động) so với biển hiệu viền nét đứt (đang mở mới/dự kiến) = tốc độ mở rộng chuỗi (net new stores); (2) kích thước mỗi cửa hàng khác nhau theo mô hình (mini/supermarket/đại siêu thị) = cơ cấu doanh thu theo mô hình cửa hàng; (3) kho trung tâm + số xe tải toả ra = hiệu quả logistics/số điểm bán phủ được; (4) 1 cửa hàng vẽ to hơn có gạch chéo = cửa hàng đóng cửa (đóng góp âm) | ĐẠT — dãy cửa hàng lặp lại cùng 1 hình dạng biển hiệu đọc được ngay là chuỗi bán lẻ, khác hẳn 1 cửa hàng đơn lẻ | ĐẠT — đây là ĐIỂM KHÁC BIỆT thật với `retail-storefront-cart.svg` hiện có (1 cửa hàng, đo giỏ hàng) — hình mới đo QUY MÔ MẠNG LƯỚI, một luận điểm hoàn toàn khác không thể thay bằng hình cũ | ĐẠT | Nhà bán lẻ chỉ có 1-2 cửa hàng flagship, chưa phải chuỗi (dùng lại `retail-storefront-cart.svg` đủ) |
| Công nghệ / phần mềm (SaaS, nền tảng số) | Trung tâm dữ liệu (data center) dạng dãy tủ rack server + đường mạng phân nhánh ra nhiều thiết bị đầu cuối | (1) Số đèn LED "xanh" (đang chạy) so "đỏ"/tắt trên tủ rack = tỷ lệ uptime/công suất hạ tầng sử dụng; (2) độ dày nhánh mạng toả ra nhiều thiết bị đầu cuối (điện thoại/laptop icon nhỏ) = số người dùng hoạt động (MAU/DAU); (3) khối lưu trữ (ổ đĩa xếp chồng) tăng dần = dữ liệu người dùng tích luỹ; (4) đường ống làm mát trung tâm dữ liệu = chi phí vận hành hạ tầng (một biến chi phí đặc trưng ngành mà công ty truyền thống không có) | ĐẠT nếu vẽ chi tiết đủ đặc trưng (tủ rack + đèn LED trạng thái + hệ làm mát), THẤT BẠI nếu chỉ vẽ "hộp máy tính" chung chung | CẢNH BÁO, chỉ ĐẠT MỘT PHẦN — nhánh mạng toả ra nhiều thiết bị VỀ BẢN CHẤT HÌNH HỌC giống hệt sơ đồ mạng lưới phân phối của viễn thông (dòng bên dưới) hoặc mạng lưới điện; cái giữ được tính riêng là CHI TIẾT HỆ LÀM MÁT TRUNG TÂM DỮ LIỆU (đặc trưng chi phí vận hành ngành phần mềm/cloud, ngành khác không có) — nếu bỏ chi tiết này, ẩn dụ tụt xuống mức trang trí dùng chung. Đây chính xác là lỗ hổng của dòng 23 trong `metaphor-table.md` gốc (bánh răng ăn khớp cho "công nghệ/nền tảng số") — xem mục cảnh báo riêng bên dưới | ĐẠT nếu dùng đèn LED nhị phân xanh/đỏ, không phải gauge % | Công ty phần mềm thuần B2B enterprise không vận hành hạ tầng cloud riêng (thuê ngoài AWS/Azure hoàn toàn) — data center không phải tài sản của họ, ẩn dụ mất đi ý nghĩa "vốn đầu tư hạ tầng" |
| Y tế (bệnh viện/chuỗi phòng khám) | Mặt cắt toà nhà bệnh viện nhiều tầng theo khoa (cấp cứu/nội trú/khám ngoại trú) | (1) Số giường bệnh đã có bệnh nhân (đậm màu) so giường trống (viền nhạt) mỗi tầng = công suất giường bệnh sử dụng theo khoa; (2) chiều dài hàng người chờ ở khoa khám ngoại trú = lưu lượng bệnh nhân ngoại trú; (3) xe cứu thương ở cổng cấp cứu = tần suất ca cấp cứu; (4) khu dược/xét nghiệm riêng biệt ở tầng trệt = doanh thu phi giường bệnh (dược, xét nghiệm, chẩn đoán hình ảnh) | ĐẠT — cutaway bệnh viện nhiều tầng theo khoa đọc được ngay | ĐẠT — cơ cấu doanh thu "giường bệnh vs dược/xét nghiệm" là đặc thù mô hình kinh doanh y tế, không map sang khách sạn (dù silhouette toà nhà nhiều tầng bên ngoài có nét giống, PHẢI giữ chi tiết xe cứu thương + khoa cấp cứu để phân biệt) | ĐẠT | Phòng khám chuyên khoa nhỏ không có giường nội trú (chỉ còn biến khu khám ngoại trú) |
| Giáo dục (trung tâm đào tạo/edtech có cơ sở vật lý) | Toà nhà trường học nhiều tầng lớp học + khối ký túc xá (nếu có) | (1) Số phòng học "đầy" (có học viên, đậm màu) so "trống" mỗi tầng = tỷ lệ lấp đầy lớp học; (2) chiều cao khối ký túc xá riêng = mảng doanh thu nội trú đi kèm; (3) sân/khu thể thao ở góc = chi phí tiện ích không sinh doanh thu trực tiếp; (4) số tầng mới đang xây thêm (nét đứt, giống cần cẩu real-estate) = kế hoạch mở rộng công suất | ĐẠT | ĐẠT có điều kiện — cấu trúc "toà nhà nhiều tầng phòng, đầy/trống" gần giống hệt cấu trúc y tế và khách sạn bên dưới; CẦN giữ chi tiết bảng đen/bàn ghế lớp học ở mỗi cửa sổ để phân biệt khỏi phòng bệnh viện hay phòng khách sạn — nếu chỉ vẽ khối cửa sổ trơn thì đây là 1 trong 3 ẩn dụ CÙNG HÌNH DẠNG dùng chung, cần callout rất rõ mới cứu được | ĐẠT | Edtech thuần online không có cơ sở vật lý — cần ẩn dụ khác (màn hình/thiết bị đầu cuối) |
| Du lịch / khách sạn | Toà nhà khách sạn nhiều tầng phòng + khu hồ bơi/sảnh ở khối thấp phía trước | (1) Số phòng "có khách" (đậm màu, rèm kéo) so "trống" (nhạt màu) = công suất phòng (occupancy rate); (2) độ dài hàng cờ quốc gia nhỏ cắm ở sảnh = cơ cấu khách theo quốc tịch; (3) khối nhà hàng/hồ bơi riêng ở khối thấp = doanh thu ngoài phòng (F&B, dịch vụ); (4) giá trung bình gợi ý bằng độ sang trọng vật liệu mặt tiền (kính lớn vs gạch) = phân khúc ADR (average daily rate) | ĐẠT | ĐẠT có điều kiện — CÙNG rủi ro trùng hình dạng với y tế/giáo dục ở trên (toà nhà nhiều phòng đầy/trống); chi tiết cứu bài là RÈM CỬA SỔ (khách sạn) khác giường bệnh (y tế) khác bàn học (giáo dục) — PHẢI vẽ đủ chi tiết phân biệt, nếu không đây là nhóm 3 ẩn dụ "hộp cửa sổ nhiều tầng" cùng công thức, chỉ khác nhãn | ĐẠT | Khách sạn theo mô hình quản lý nhượng quyền không sở hữu bất động sản (doanh thu là phí quản lý, không phải phòng) |
| Nông nghiệp công nghệ cao | Nhà kính (greenhouse) có hệ thống tưới nhỏ giọt + cảm biến, xếp theo luống | (1) Số luống cây "xanh tốt" (đậm) so "mới trồng" (nhạt) = tiến độ vụ mùa/tỷ lệ diện tích đang thu hoạch; (2) đường ống tưới nhỏ giọt chạy dọc luống, có van chia nhánh = mức độ tự động hoá (khác hẳn nông nghiệp truyền thống không có ống); (3) tấm pin năng lượng mặt trời trên mái nhà kính = chi phí vận hành thấp hơn nhờ tự chủ năng lượng; (4) xe tải lạnh chờ ở cửa = sản lượng xuất bán theo vụ | ĐẠT — nhà kính có mái vòm + luống ống tưới là silhouette khác hẳn ruộng lộ thiên | ĐẠT — hệ tưới nhỏ giọt tự động + nhà kính kiểm soát khí hậu là đặc trưng CÔNG NGHỆ CAO, phân biệt rõ với nông nghiệp truyền thống (ruộng/ao đã có trong bảng gốc dòng 18) | ĐẠT | Trồng trọt công nghệ cao nhưng ngoài trời (tưới nhỏ giọt trên đồng, không nhà kính) — bỏ mái vòm, giữ ống tưới |
| Logistics kho lạnh (dịch vụ 3PL, khác nhà máy tự có kho ở mục thuỷ sản) | Trung tâm kho lạnh cho thuê nhiều buồng nhiệt độ khác nhau, xe nâng ra vào | (1) Số buồng kho đang cho thuê (đậm) so còn trống (nhạt), MỖI buồng có nhãn nhiệt độ khác nhau (đông sâu/mát/khô) = tỷ lệ lấp đầy theo phân khúc nhiệt độ; (2) số xe nâng đang hoạt động ở sân bốc dỡ = tần suất luân chuyển hàng (thấp = khách thuê lưu kho dài ngày, cao = trung chuyển nhanh); (3) mái có dàn lạnh công suất lớn ở nhiều cụm = quy mô đầu tư hạ tầng; (4) khách thuê khác nhau đánh dấu bằng màu nhãn khác nhau trên cùng 1 buồng = mức độ đa dạng khách hàng (rủi ro tập trung) | ĐẠT nếu vẽ đủ nhiều buồng NHIỆT ĐỘ KHÁC NHAU rõ rệt (khác nhà máy thuỷ sản chỉ có 1 kho lạnh phục vụ chính mình) | ĐẠT — mô hình "cho khách thuê nhiều buồng, đa dạng khách hàng" là đặc thù DỊCH VỤ 3PL, khác hẳn nhà máy thuỷ sản tự dùng kho lạnh của chính mình (điểm phân biệt phải giữ: có NHIỀU NHÃN KHÁCH HÀNG khác nhau trên các buồng, không phải 1 chủ sở hữu duy nhất) | ĐẠT | Doanh nghiệp tự vận hành kho lạnh cho chính sản phẩm của mình (dùng ẩn dụ thuỷ sản/nhà máy ở Phần A thay vì hình này) |

## Phần C — Cảnh báo về 1 dòng trong bảng gốc `illustrations/metaphor-table.md`

**KHÔNG SỬA file gốc** (ngoài phạm vi cho phép của vòng này), chỉ ghi nhận để vòng sau cân nhắc:
dòng 23 "Công nghệ / nền tảng số (platform) → Bánh răng nhiều cỡ ăn khớp nhau" tự nó đã liệt kê lý
do "bánh răng lớn quay chậm kéo bánh răng nhỏ quay nhanh = network effect", nhưng khi áp đúng bài
tự kiểm 2 (đổi ngành) của chính `grammar.md`: cơ chế "tỷ lệ truyền động lớn kéo nhỏ" mô tả được
BẤT KỲ hệ thống có đòn bẩy/tỷ lệ nào (tổ chức, dây chuyền cơ khí ở NGÀNH SẢN XUẤT đã có sẵn trong
thư viện, thậm chí cơ cấu vốn tài chính) — không có chi tiết vật lý nào trong "2 bánh răng ăn khớp"
là ĐỘC QUYỀN của công nghệ/nền tảng số. Đây đúng loại ẩn dụ mà mục "Nguyên tắc khi nào KHÔNG nên
dùng" ở cuối chính file gốc đã cảnh báo (mục "chỉ để trang trí"), nhưng dòng 23 của chính bảng đó
lại chưa tự áp dụng triệt để nguyên tắc này cho chính nó. Đề xuất thay thế trong Phần B ở trên
(trung tâm dữ liệu với đèn LED trạng thái + hệ làm mát) là một ứng viên, kèm đúng giới hạn thật của
nó (xem dòng "Công nghệ / phần mềm" ở bảng trên, đã tự nhận CẢNH BÁO chỉ đạt một phần).

## Phần D — Ẩn dụ CẦN TRÁNH (mở rộng danh sách gợi ý của team lead)

| Ẩn dụ | Cơ chế vì sao vô giá trị |
|---|---|
| Bánh răng ăn khớp | Mô tả BẤT KỲ hệ thống có tỷ lệ truyền động/đòn bẩy nào (tổ chức, cơ khí, vốn) — không có chi tiết nào độc quyền cho 1 ngành. Xem Phần C: chính bảng gốc đang dùng cho "nền tảng số" nhưng không có gì ngăn dùng y hệt cho bất kỳ ngành nào khác. |
| Cầu thang bậc thang đi lên | Về bản chất là 1 bar chart bị nguỵ trang bằng phối cảnh 3D — mã hoá giá trị bằng chiều cao bậc giống hệt cột, nhưng phối cảnh xiên làm biến dạng cảm nhận độ cao (cùng cơ chế lừa mà trục bị cắt cụt hoặc pie 3D bị liệt vào danh sách đen ở `research/03-chart-doctrine/FINDINGS.md`), lại không thêm được thông tin nào so với 1 cột thường. |
| Con đường/lộ trình có cột mốc | Ẩn dụ "hành trình" áp được cho bất kỳ chuỗi sự kiện theo thời gian nào (lộ trình sản phẩm, lịch sử công ty, tiến trình bệnh) — bản thân con đường không mang cơ chế vật lý nào của một ngành cụ thể, chỉ là khung kể chuyện chung. |
| Đích ngắm / bia bắn cung | Ẩn dụ "đạt mục tiêu" phổ quát cho bất kỳ KPI nào ở bất kỳ chức năng nào (doanh số, chất lượng, ESG) — vòng tròn đồng tâm không neo được cơ chế vật lý riêng của ngành nào. |
| Ngọn núi có cờ trên đỉnh | Cùng họ với đích ngắm: "hành trình chinh phục mục tiêu" dùng được cho mọi câu chuyện tăng trưởng, độ cao núi là tuỳ ý vẽ, không ánh xạ được với một đại lượng thật nào của doanh nghiệp. |
| Chìa khoá mở ổ khoá | Ẩn dụ "giải pháp/mở khoá tiềm năng" phổ quát, dùng được cho quảng cáo bất kỳ sản phẩm/dịch vụ nào, không gắn với cơ chế ngành cụ thể. |
| Cầu nối 2 bờ sông | Ẩn dụ "kết nối/chuyển tiếp" phổ quát (nối thế hệ, nối công nghệ cũ-mới, nối 2 thị trường) — không có chi tiết vật lý ngành nào bắt buộc phải là 1 cây cầu. |
| Tên lửa phóng lên | Ẩn dụ tăng trưởng tăng tốc phổ biến trong pitch deck khởi nghiệp bất kể ngành nghề, không neo được biến cấu trúc nào ngoài "đường bay đi lên", tương đương 1 mũi tên chéo được vẽ cầu kỳ hơn. |
| Đồng hồ cát đếm ngược (dùng như biểu tượng "gấp rút" chung chung) | Chỉ hợp lệ khi neo vào MỘT mốc thời gian đếm ngược cụ thể có thật (ngày đáo hạn trái phiếu, ngày hết hạn bằng sáng chế); dùng như biểu tượng "khẩn cấp" trang trí chung chung thì không đọc ra được biến nào khi che chữ, thất bại ngay bài tự kiểm 1. |
| Cây non lớn dần kèm đồng xu làm lá/quả | Ẩn dụ "tăng trưởng giá trị theo thời gian" phổ quát cho tiết kiệm/đầu tư/doanh thu bất kỳ ngành nào; thường đi kèm gradient thân cây tô bóng, cũng dễ vi phạm luôn cả luật cấm gradient của `illustrations/grammar.md` mục 7. |
| La bàn chỉ hướng | Ẩn dụ "định hướng chiến lược" phổ quát, không gắn với cơ chế vật lý của bất kỳ ngành cụ thể nào (khác với la bàn thật trên bản đồ hàng hải, vốn CÓ nghĩa đen khi minh hoạ ngành logistics/hàng hải). |

## Nguồn tham khảo bên ngoài (chi tiết đầy đủ ở `FINDINGS.md` mục 3)

Edward Tufte (nguyên tắc "integrated evidence", data-ink, layering/separation), cutaway drawing
kỹ thuật (Wikipedia "Cutaway drawing"), The Pudding (visual essay do dữ liệu dẫn dắt cấu trúc, không
phải minh hoạ trang trí phủ lên sau), Reuters Graphics/GEOART (cutaway công nghiệp dầu khí trong ấn
phẩm thương mại).
