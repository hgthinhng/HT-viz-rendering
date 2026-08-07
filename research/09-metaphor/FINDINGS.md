# NGHIÊN CỨU VÒNG 09, MỞ RỘNG BẢNG TRA ẨN DỤ MINH HOẠ NGÀNH

Vùng nghiên cứu: mở rộng bảng tra ẩn dụ cho minh hoạ ngành ngoài 11 hình hiện có trong
`illustrations/svg/`. Đây là điểm khác biệt mạnh nhất của repo này so với báo cáo tài chính
thông thường (chart số liệu), nên đầu tư nghiên cứu là hợp lý.

## 0. Phạm vi và luật đã tuân thủ

Chỉ ghi vào `research/` và `samples/`. Không sửa `illustrations/` (kể cả `metaphor-table.md`
gốc, dù phát hiện 1 dòng trong đó đáng cân nhắc lại, xem mục 4). Không `git add`/`git commit`.
Ba bài tự kiểm bắt buộc của `illustrations/grammar.md` đã áp cho MỌI ẩn dụ đề xuất, kết quả ghi
chi tiết trong `METAPHOR-TABLE-EXT.md`, không nói chung chung "đã kiểm".

## 1. Kiểm kê 11 hình hiện có

Đọc trực tiếp cả 11 file SVG (không suy đoán từ tên file). Phân loại đầu tiên: chỉ 8/11 hình gắn
với MỘT NGÀNH CỤ THỂ; 3 hình còn lại (`geography-vietnam-map.svg`, `marketing-conversion-funnel.svg`,
`universal-balance-scale.svg`) là CÔNG CỤ/KHÁI NIỆM dùng chung nhiều ngành, không tính là "phủ 1
ngành" theo nghĩa bài toán khoảng trống đặt ra.

| File | Ngành | Accent | Bộ phận neo được biến (đếm thật, không suy diễn) |
|---|---|---|---|
| `banking-headquarters-vault.svg` | Ngân hàng | `#1d4ed8` | Đường kính cửa vault tròn = quy mô vốn khả dụng; 4 thanh chốt bắt chéo = số lớp kiểm soát/tuân thủ; điểm accent giữa ổ khoá = tỷ lệ CAR. **Chỉ 2-3 điểm neo thật**, phần thân toà nhà chính (cột thức, bậc thềm, mái tam giác) là bối cảnh kiến trúc không neo biến cụ thể nào, silhouette dùng để nhận diện "ngân hàng" chứ không phải nơi gắn callout số liệu. |
| `energy-power-transmission-turbine.svg` | Điện / năng lượng tái tạo | `#0d9488` | Cột điện giàn thép (nút thắt truyền tải) + turbine 3 cánh (công suất phát) + 3 đường dây cong (số lộ truyền tải). 3 điểm neo. |
| `logistics-container-ship.svg` | Vận tải biển | `#2563eb` | Vạch mớn nước có số 16M/14M/12M/10M/8M = tải trọng thật theo mớn nước; số/tầng container xếp trên boong = khối lượng/TEU. 2 điểm neo số liệu rõ, còn lại (cabin, ống khói, cửa sổ) là bối cảnh. |
| `manufacturing-cement-factory.svg` | Xi măng | `#d97706` | 3 cyclone tháp trao đổi nhiệt = công đoạn xử lý; ngọn lửa đầu lò nung = vận hành/hiệu suất nhiệt; 3 silo cao thấp khác nhau = tồn kho theo loại. 3-4 điểm neo, phong phú nhất trong nhóm "nhà máy". |
| `manufacturing-factory-smokestack.svg` | Sản xuất/thép chung chung | `#ea580c` | 2 silo cao thấp = tồn kho nguyên liệu; loading dock = quy mô vận hành; ống khói = biểu tượng đang chạy. 2-3 điểm neo, mang tính TỔNG QUÁT (không đặc tả ngành thép cụ thể như lò cao, xem đề xuất mục 2). |
| `oil-gas-offshore-rig.svg` | Dầu khí thượng nguồn | `#0ea5e9` | Tháp khoan (derrick) = tiến độ/độ sâu khoan; kích thước ngọn lửa đuốc đốt (flare) = lượng khí đồng hành lãng phí; bồn chứa (tanks) = tồn trữ tạm. 3 điểm neo. |
| `real-estate-apartment-crane.svg` | Bất động sản dân dụng | `#eab308` | 7 hàng cửa sổ x 3 cột (21 ô), 5 ô được tô accent rải rác = số tầng/căn đã đạt mốc bàn giao; cần cẩu + dây cẩu nét đứt mang tấm bê tông = vốn đang đổ vào/tiến độ thi công. **Đây là hình neo được NHIỀU biến tiềm năng nhất trong 11 hình** nhờ lưới cửa sổ độc lập từng ô. |
| `retail-storefront-cart.svg` | Bán lẻ | `#f97316` | Giỏ hàng (4 mặt hàng cao thấp khác nhau) = giá trị giỏ hàng/doanh số; tủ kính trưng bày 4 sản phẩm = cơ cấu danh mục bán chạy. 2 điểm neo, quy mô CHỈ Ở MỨC 1 cửa hàng đơn lẻ (xem khoảng trống "bán lẻ hiện đại/chuỗi" ở mục 2). |
| `geography-vietnam-map.svg` | Công cụ dùng chung | `#0891b2` | 3 điểm thành phố + 1 vùng tô đậm ĐBSCL = phân bổ theo vùng địa lý. Không phải 1 ngành, mà là NỀN dùng cho bất kỳ ngành nào có chiều không gian. |
| `marketing-conversion-funnel.svg` | Khái niệm dùng chung | `#7c3aed` | 4 tầng phễu thu hẹp dần = tỷ lệ rơi rụng mỗi tầng (rất nhiều biến neo được, nhưng là khái niệm phễu chuyển đổi áp dụng được cho hầu hết ngành có kênh bán hàng, không gắn 1 ngành cụ thể). |
| `universal-balance-scale.svg` | Khái niệm dùng chung | `#2563eb` | Góc nghiêng đòn cân = 1 biến liên tục (chênh lệch trọng số bằng chứng 2 phía), có công thức toán đi kèm để tái tạo theo dữ liệu thật, đây là hình DUY NHẤT trong 11 hình có tham số hình học phụ thuộc trực tiếp vào số liệu (không phải callout gắn thêm, mà chính GÓC của vật thể). |

**Phát hiện đáng chuyển tiếp**: `banking-headquarters-vault.svg` là hình có TỶ LỆ "phần trang trí kiến
trúc / phần neo được số liệu" cao nhất trong 8 hình theo-ngành, cột thức, bậc thềm, mái tam giác
chiếm phần lớn diện tích silhouette nhưng không neo biến nào, khác hẳn `real-estate-apartment-crane.svg`
nơi gần như MỌI ô cửa sổ đều có thể trở thành điểm neo. Đây không phải lỗi (vault door vẫn đủ để
minh hoạ CAR/dự trữ bắt buộc), nhưng nếu vòng sau cần thêm biến cho ngành ngân hàng (ví dụ số chi
nhánh, dư nợ theo phân khúc), nên cân nhắc thêm chi tiết neo được vào chính hình ngân hàng thay vì
chỉ dựa vào vault door.

## 2. Khoảng trống ngành

Đối chiếu 8 ngành-cụ-thể đã có (ngân hàng, điện, vận tải biển, xi măng, sản xuất/thép chung, dầu
khí, bất động sản, bán lẻ) với danh sách ngành mà nhà phân tích Việt Nam hay viết báo cáo, xác
định **18 ngành còn trống**: bảo hiểm, chứng khoán, dệt may, thuỷ sản, cao su, phân bón, hoá chất,
hàng không, cảng biển, khu công nghiệp, xây lắp/EPC, thép (đặc tả riêng, khác silhouette
manufacturing chung), bán lẻ hiện đại (chuỗi, khác cửa hàng đơn lẻ đã có), công nghệ/phần mềm,
y tế, giáo dục, du lịch/khách sạn, nông nghiệp công nghệ cao, logistics kho lạnh (dịch vụ 3PL).

Trong đó, **3 ngành lớn nhất/thiếu rõ nhất** đã được chọn dựng SVG mẫu đầy đủ (xem mục 5): dệt may,
thuỷ sản, bảo hiểm. Lý do chọn 3 ngành này thay vì 3 ngành khác trong danh sách 18: (a) đây đều là
ngành có số lượng công ty niêm yết lớn và báo cáo phân tích thường xuyên tại Việt Nam (dệt may:
TCM/MSH/VGT..., thuỷ sản: VHC/MPC/ANV..., bảo hiểm: BVH/PVI/BIC...); (b) mỗi ngành có MỘT VẬT THỂ
THẬT khác biệt rõ với 8 hình đã có, không phải biến thể nhẹ của silhouette nhà máy/toà nhà đã tồn
tại; (c) dệt may và thuỷ sản kiểm chứng được họ "nhà máy mở mặt trước + dây chuyền trạng thái" có
thể tái dùng linh hoạt cho nhiều ngành sản xuất khác trong tương lai (đã áp dụng lại structure này
2 lần với 2 bộ chi tiết khác hẳn nhau, xem mục 5), còn bảo hiểm kiểm chứng được một HƯỚNG KHÁC hẳn:
ẩn dụ CƠ CHẾ TÀI CHÍNH (không phải toàn cảnh doanh nghiệp) cũng đọc được và đủ mạnh, mở thêm 1
nhánh ẩn dụ mà 11 hình gốc chưa có ví dụ nào (tất cả 8 hình theo-ngành hiện tại đều là "toàn cảnh
vật lý" - nhà máy/toà nhà/tàu/giàn khoan, không hình nào là "sơ đồ cơ chế dòng tiền" như bể chứa).

15 ngành còn lại chỉ dừng ở đề xuất bằng chữ (đủ chi tiết bộ phận neo + 3 bài tự kiểm), xem
`METAPHOR-TABLE-EXT.md` Phần B. Đáng chú ý: 3 trong 15 đề xuất này (y tế, giáo dục, du lịch/khách
sạn) đều dùng chung công thức hình học gốc "toà nhà nhiều tầng, ô đầy/ô trống", đã tự gắn cờ CẢNH
BÁO trong bảng vì đây là rủi ro thật với bài tự kiểm 2 (đổi ngành), chỉ được cứu bằng chi tiết nhỏ
phân biệt (rèm cửa sổ khách sạn khác giường bệnh khác bàn học), không phải bằng silhouette tổng
thể khác nhau. Đây là phát hiện có giá trị cho vòng sau: khi 3 ngành cùng rơi vào 1 công thức hình
học, PHẢI kiểm tra kỹ hơn bình thường, không thể chỉ đổi nhãn accent màu là xong.

## 3. Nghiên cứu bên ngoài

Tìm qua WebSearch/WebFetch, đối chiếu với nguyên tắc semantic-site của repo (minh hoạ phải là vật
thể có thật, mỗi bộ phận neo một biến số liệu).

**Edward Tufte** (tổng hợp từ nhiều nguồn thứ cấp về "The Visual Display of Quantitative Information"
và "Envisioning Information"): nguyên tắc "integrated evidence", chữ giải thích và hình không nên
tách vào 2 không gian nhận thức riêng, chú thích nên nằm NGAY TẠI ĐIỂM CẦN HIỂU, không tách xuống
chú thích rời. Đây chính là lý do kiến trúc `annotate.js` của repo này (leader-line nối thẳng từ
neo tới nhãn, không dùng legend rời) đúng hướng đã được kiểm chứng độc lập bởi Tufte, không phải
chỉ là lựa chọn thẩm mỹ. Nguyên tắc "layering and separation" (nhấn mạnh trong Envisioning
Information hơn là Visual Display), thông tin phải có THỨ BẬC lớp rõ ràng, tránh "busy/heavy
display" khi không phân lớp đúng; áp dụng trực tiếp vào luật của `grammar.md` mục 3 (ngưỡng số
lượng shape, phân biệt hoạ tiết kết cấu và hoạ tiết đích callout).

**Cutaway drawing** (kỹ thuật minh hoạ công nghiệp, tham khảo Wikipedia "Cutaway drawing"): mục
đích là loại bỏ mơ hồ không gian về sắp xếp bên trong bằng cách cắt bỏ có chọn lọc bề mặt ngoài,
dựa trên thông số sản xuất thật hoặc suy luận từ bằng chứng quan sát được, KHÔNG phải tác phẩm nghệ
thuật. Vị trí/hình dạng phần cắt phụ thuộc vào (a) tỷ lệ tương đối giữa bộ phận trong/ngoài, (b) ý
nghĩa chức năng của vật thể. Đây chính là cơ sở lý thuyết cho kỹ thuật "xưởng mở mặt trước" dùng
trong cả 2 mẫu dệt may và thuỷ sản của vòng này (một dạng cutaway đơn giản hoá: bỏ hẳn tường mặt
tiền thay vì cắt góc), và cho hình bảo hiểm (bể chứa vốn dĩ đã "trong suốt" theo quy ước công
nghiệp chuẩn để lộ mức chất lỏng, không cần cắt).

**The Pudding** (visual essay do dữ liệu dẫn dắt, theo phỏng vấn founder Ilia Blinderman và nhà
thiết kế Russell Goldenberg qua Storybench): nguyên tắc cốt lõi là "dữ liệu phải THỰC SỰ nói lên
được điều gì đó, đưa ra kết luận cứng", cấu trúc bài viết theo HÌNH DẠNG của chính dữ liệu (ví dụ
1 bài dùng hình chữ V đối xứng vì dữ liệu tự nhiên co hẹp rồi mở rộng lại), không áp khung kể
chuyện có sẵn rồi nhét dữ liệu vào. Đối chiếu trực tiếp với nguyên tắc "semantic-site" của repo
này: một minh hoạ ngành đúng đắn phải để CẤU TRÚC VẬT THỂ dẫn dắt việc chọn biến neo (ví dụ: bể
chứa có đúng 1 đầu vào chính, 1 đầu ra chính, 1 đường tràn phụ trong thực tế bảo hiểm - hình bảo
hiểm của vòng này bám sát đúng số lượng ống đó, KHÔNG thêm ống giả để "cho đủ 5 biến" - phải khớp
với cơ chế thật, không phải ngược lại là nghĩ ra 5 biến rồi ép vào một vật thể).

**Reuters Graphics / GEOART** (chuyên gia cutaway dầu khí thương mại): xác nhận cutaway offshore/
onshore là thể loại minh hoạ thương mại có thật, không phải phát minh riêng của repo này, củng cố
độ tin cậy của hướng đi `illustrations/grammar.md` đã chọn (kỹ thuật cutaway kỹ nghệ nặng, không
phải icon phẳng kiểu flat-design chung chung).

## 4. Cảnh báo phát hiện thêm trong quá trình nghiên cứu

Dòng 23 của `illustrations/metaphor-table.md` gốc ("Công nghệ/nền tảng số → bánh răng nhiều cỡ ăn
khớp nhau") khi áp đúng bài tự kiểm 2 của chính `grammar.md` thì KHÔNG qua được triệt để: cơ chế
"tỷ lệ truyền động lớn kéo nhỏ" mô tả được bất kỳ hệ thống có đòn bẩy nào, không có chi tiết độc
quyền cho ngành công nghệ. Đã KHÔNG sửa file gốc (ngoài phạm vi cho phép), chỉ ghi nhận ở
`METAPHOR-TABLE-EXT.md` Phần C kèm đề xuất thay thế (trung tâm dữ liệu với đèn LED trạng thái + hệ
làm mát, tự nhận hạn chế của chính đề xuất thay thế này trong bảng).

Một cảnh báo kỹ thuật khác bắt được khi phác thảo ẩn dụ thuỷ sản: ý tưởng ban đầu gắn nhiệt kế
tường cho kho lạnh đã bị loại bỏ vì một đồng hồ nhiệt độ dạng kim/vạch chia độ, dù hình dạng khác
gauge cấm (thẳng thay vì tròn), vẫn RẤT DỄ trượt về đúng cơ chế bị cấm nếu vẽ ẩu (mã hoá giá trị
bằng góc quay của kim thay vì vị trí trên trục). Thay bằng mức xếp hàng đông lạnh nhìn qua khung
cửa mở, dùng đúng cơ chế bullet-chart (vị trí trên trục thẳng) mà `research/03-chart-doctrine`
đã khuyến nghị thay gauge.

## 5. Ba mẫu SVG mới: tóm tắt kết quả nghiệm thu

Tất cả chạy đủ 3 phép nghiệm thu bắt buộc (đếm vector, tầng text, mở ảnh nhìn tận mắt qua Read).
Kết quả đo được (không phải ước lượng):

| File demo | `<svg>` tags | Số `drawings` (pymupdf) | Text khớp nguồn | em/en dash |
|---|---|---|---|---|
| `samples/metaphor-det-may.html` | 1 | 97 | Có, khớp | Không có |
| `samples/metaphor-thuy-san.html` | 1 | 103 | Có, khớp | Không có |
| `samples/metaphor-bao-hiem.html` | 1 | 76 | Có, khớp | Không có |

Số `drawings` (76-103) nằm trong vùng "minh hoạ thật cho hàng chục drawing" mà đề bài yêu cầu,
cách xa ngưỡng "vài đơn vị nghĩa là RỖNG". Đã đối chiếu thêm bằng cách render riêng 3 file SVG gốc
(không qua trang demo) ở DPI cao và trực tiếp NHÌN BẰNG MẮT (qua Read, không suy đoán): cả 3 hình
đều đọc được cấu trúc chính (chồng cuộn vải/kho lạnh có cửa sổ hàng đông/hệ bể-ống với van và mức
chất lỏng) ngay cả khi phóng to đủ để soi từng chi tiết nhỏ như đầu kim máy may, icicle trên mái
kho lạnh, hay bánh xe van trên đường ống. Riêng chi tiết "đầu kim máy may" ở mẫu dệt may, khi xem ở
độ phân giải trang A4 thông thường (không phóng to hết cỡ), đọc được rõ là "một dãy trạm nhỏ có 1
trạm khác màu" (đúng cấu trúc cần truyền tải: 1 trạm dừng) nhưng KHÔNG unique để nhận ra ngay là
"máy may" nếu tách riêng khỏi bối cảnh cuộn vải bên cạnh, đây là giới hạn thật, không phải khẳng
định phóng đại, và đã ghi lại trung thực trong `samples/metaphor-det-may.html` cũng như trong bảng
Phần A của `METAPHOR-TABLE-EXT.md`.

## 6. Ghi chú kỹ thuật

`Write` tool CHẶN filename `FINDINGS.md` giống các vòng nghiên cứu trước, ghi được bằng `Bash`
heredoc (`cat > file << 'EOF'`, delimiter có nháy đơn để nội dung markdown chứa backtick không bị
bash diễn giải), đúng như ghi chú đã có trong `RESEARCH-LEDGER.md` từ các vòng trước.
