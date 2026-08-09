---
name: HT-viz-rendering
description: Làm báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản. Đọc đề bài để suy ra loại ấn phẩm, độc giả và mức cam kết, rồi chọn làn xuất bản (`html-song` HTML tự đủ có tương tác, hoặc `pdf-so` PDF đọc trên màn hình), chọn hình theo câu hỏi người đọc đang hỏi, và giao file đã qua gate. Dùng khi cần báo cáo ngành, báo cáo cổ phiếu, bản tin thị trường, cập nhật kết quả kinh doanh, deal pack, hoặc tóm tắt điều hành.
---

# HT-viz-rendering: doctrine làm báo cáo tài chính

Tài liệu này dạy CÁCH QUYẾT ĐỊNH, không phải cách gọi lệnh. Nó dùng được cả khi không có repo
đi kèm: mọi mục đều đứng một mình. Khi có repo, các mục sẽ trỏ tới chỗ thi công cụ thể.

Sai lầm hay gặp nhất khi một mô hình làm báo cáo tài chính không phải là sai số liệu. Nó là
**nhảy thẳng vào định dạng mặc định**: ba gạch đầu dòng cho mọi mục, một bar chart cho mọi câu
hỏi, một câu kết "cần tiếp tục theo dõi". Tài liệu này tồn tại để chặn đúng phản xạ đó.

---

## 0. ĐỌC ĐỀ BÀI TRƯỚC KHI VIẾT DÒNG NÀO

### 0.A Sáu tín hiệu phải đọc

1. **Loại ấn phẩm.** Bản tin thị trường, cập nhật kết quả kinh doanh, báo cáo khởi tạo một mã,
   báo cáo ngành, deal pack, tóm tắt điều hành, bản mẫu kỹ thuật. Bảy loại này khác nhau ở
   ĐỘ SÂU và MỨC CAM KẾT nhiều hơn ở độ dài.
2. **Ai đọc, và đọc trong bao lâu.** Uỷ ban đầu tư đọc 20 giây rồi hỏi; nhà đầu tư cá nhân đọc
   một mạch 10 phút; chuyên viên thẩm định đọc kèm bảng tính mở bên cạnh. Người đọc chọn cấu
   trúc, không phải khẩu vị của người viết.
3. **Người đọc phải LÀM gì sau khi đọc.** Không làm gì (nắm tình hình), quyết định một việc
   (mua, bán, cấp hạn mức), hay mang đi thuyết phục người khác. Đây là tín hiệu mạnh nhất và
   hay bị bỏ qua nhất.
4. **Số liệu có nguồn tới đâu.** Số công bố chính thức, số ước tính nội bộ, hay số minh hoạ.
   Bậc nguồn thấp nhất trong bài quyết định mức cam kết cao nhất được phép.
5. **Ràng buộc phát hành.** Bản gửi ra ngoài hay bản nội bộ, có được lộ kênh dữ liệu không, có
   ràng buộc pháp lý nào về khuyến nghị đầu tư không.
6. **File sẽ mở ở đâu.** Trình duyệt trên máy tính, điện thoại, hay in ra dùng trong phòng họp.
   Đây là thứ chọn LÀN, xem mục 2.

### 0.B Tuyên bố một dòng trước khi bắt đầu

Trước khi dựng bất cứ thứ gì, nói một câu:

> **"Đọc đề bài này là: `<loại ấn phẩm>` cho `<độc giả>`, để họ `<hành động>`, làn `<html-song
> hoặc pdf-so>`, ba núm `<độ sâu>/<mật độ số>/<mức cam kết>`."**

Ví dụ:

- *"Đọc đề bài này là: cập nhật kết quả quý cho uỷ ban đầu tư, để họ quyết định giữ hay giảm tỷ
  trọng, làn pdf-so, ba núm 5/8/6."*
- *"Đọc đề bài này là: báo cáo ngành cho nhà đầu tư cá nhân, để họ nắm bức tranh chứ chưa hành
  động, làn html-song, ba núm 7/5/4."*
- *"Đọc đề bài này là: deal pack cho bên cấp vốn, để họ ra quyết định cấp hạn mức, làn pdf-so,
  ba núm 8/7/9."*

Câu này không phải nghi thức. Nó buộc phải chốt độc giả và hành động TRƯỚC khi chọn hình, mà
đó chính là hai thứ quyết định mọi lựa chọn phía sau.

### 0.C Khi đề bài mơ hồ, hỏi ĐÚNG MỘT câu

Chỉ hỏi khi hai cách đọc dẫn tới hai ấn phẩm khác hẳn nhau. Ví dụ đáng hỏi: *"Bản này để nắm
tình hình hay để ra quyết định mua bán?"* Câu trả lời đổi mức cam kết từ 3 lên 8, tức đổi cả
cấu trúc.

Suy được từ ngữ cảnh thì đừng hỏi. Tuyên bố cách đọc rồi làm.

### 0.D Kỷ luật chống mặc định

Đừng mặc định: mở bài bằng bối cảnh vĩ mô, ba gạch đầu dòng cho mọi mục, một bar chart cho mọi
câu hỏi, bảng SWOT bốn ô, "rủi ro và cơ hội" cân bằng giả tạo, câu kết "cần tiếp tục theo dõi".
Đây là mặc định của mô hình, không phải lựa chọn của người viết.

---

## 1. BA NÚM

Ba biến số này được tham chiếu bằng đúng tên ở các mục sau. Đừng đặt tên khác.

### 1.A Định nghĩa

**`DO_SAU` (1-10)** đo độ sâu lập luận, không đo độ dài.

| Mức | Nghĩa |
|---|---|
| 1-3 | thuật lại chuyện đã xảy ra, không diễn giải nguyên nhân |
| 4-6 | có một tầng nguyên nhân, so với kỳ trước và với nhóm cùng ngành |
| 7-8 | có mô hình định lượng, kịch bản, và độ nhạy theo biến chính |
| 9-10 | có phản biện chính luận điểm của mình, nêu điều kiện làm luận điểm sai |

**`MAT_DO_SO` (1-10)** đo số con số trên một màn hình hoặc một trang.

| Mức | Nghĩa |
|---|---|
| 1-3 | vài số neo, phần lớn là chữ và hình |
| 4-6 | mỗi mục một bảng nhỏ hoặc một hình, số trong văn xuôi có neo nguồn |
| 7-8 | bảng dày nhiều cột, người đọc dò theo hàng |
| 9-10 | phụ lục dữ liệu, đọc bằng cách tra chứ không đọc tuần tự |

**`MUC_CAM_KET` (1-10)** đo mức độ bài viết dám bảo người đọc làm gì.

| Mức | Nghĩa |
|---|---|
| 1-3 | mô tả trung tính, không gợi ý hành động |
| 4-6 | nêu hàm ý, kèm điều kiện, không nói nên mua hay bán |
| 7-8 | khuyến nghị rõ kèm ngưỡng kích hoạt và điều kiện huỷ |
| 9-10 | lệnh hành động kèm mốc thời gian, ngưỡng, và kill-switch |

**Ràng buộc cứng nối MUC_CAM_KET với bằng chứng:** mức cam kết không được vượt bậc nguồn. Một
bài toàn số ước tính nội bộ mà ra lệnh mua bán ở mức 9 là bài sai, không phải bài mạnh dạn. Nếu
số liệu chỉ tới bậc ước tính, trần của `MUC_CAM_KET` là 6.

### 1.B Preset theo loại ấn phẩm

| Loại ấn phẩm | DO_SAU | MAT_DO_SO | MUC_CAM_KET |
|---|---|---|---|
| Bản tin thị trường (ngày, tuần) | 2 | 6 | 3 |
| Cập nhật kết quả kinh doanh | 5 | 8 | 6 |
| Báo cáo khởi tạo một mã | 9 | 7 | 8 |
| Báo cáo ngành | 7 | 5 | 4 |
| Deal pack, bản chào vốn | 8 | 7 | 9 |
| Tóm tắt điều hành | 3 | 4 | 9 |
| Bản mẫu kỹ thuật, số minh hoạ | 4 | 5 | 1 |

Lệch preset thì được, nhưng phải nói lý do trong câu tuyên bố ở 0.B.

### 1.C Ba núm lái cái gì

| Núm | Lái |
|---|---|
| `DO_SAU` | số section, có phụ lục hay không, chart mô tả hay chart phân tích (mục 5), có kịch bản và độ nhạy không, có mục phản biện không |
| `MAT_DO_SO` | bảng dày hay thưa, ngưỡng bỏ bảng chuyển sang câu văn, số neo trong văn xuôi, cỡ và số lượng hình mỗi màn |
| `MUC_CAM_KET` | giọng tiêu đề (khẳng định hay mô tả), có bảng tín hiệu và hành động không, có kill-switch không, độ chặt bắt buộc của nguồn |

---

## 2. CHỌN LÀN

Hai làn, chọn theo ĐỘC GIẢ MỞ FILE Ở ĐÂU, không chọn theo sở thích.

| | `html-song` | `pdf-so` |
|---|---|---|
| Là gì | một file HTML tự đủ, mở bằng trình duyệt | PDF đọc trên màn hình, không phải để in |
| Được phép | animation, tương tác, tooltip, hover, JavaScript lúc chạy, chủ đề tối, co giãn theo màn hình | khổ ngang, màu RGB, siêu liên kết, bookmark |
| Ràng buộc | một file duy nhất, chạy offline, không tham chiếu ra ngoài, font nhúng | tĩnh hoàn toàn, chữ phải chọn được trong tầng text |
| Chọn khi | người đọc mở trên máy tính và có thể khám phá; số liệu nhiều tầng cần tooltip | file bị chuyển tiếp qua email, cần đóng dấu bản, cần in dự phòng |

**Ràng buộc quyết định:** nếu file sẽ bị chuyển tiếp cho người thứ ba mà ta không kiểm soát môi
trường mở, chọn `pdf-so`. Một file HTML 1,4MB gửi qua email thường bị chặn hoặc bị mở bằng thứ
không phải trình duyệt.

**Không trộn hai làn trong một ấn phẩm.** Chart mount lúc chạy đưa vào đường xuất PDF sẽ vắng
mặt, vì engine PDF không chạy JavaScript.

---

## 3. KIẾN TRÚC MỘT ẤN PHẨM

Một ấn phẩm là một THƯ MỤC, không phải một file:

```
<ten-an-pham>/
├── noi-dung.md      front-matter, markdown, và directive đặt hình
├── so-nguon.json    mỗi số một nguồn, một bậc bằng chứng, một ngày lấy về
├── hinh/            script sinh hình, và file SVG chúng sinh ra
└── ra/              artifact, sinh lại được, không commit
```

Lý do tách sổ nguồn thành file riêng: một con số không nguồn trong bản đã gửi đi thì không gọi
lại được. Sổ nguồn tách rời cho phép kiểm số mà không phải đọc lại toàn bài.

**Hai chế độ xuất, không được gộp.** Bản nội bộ nhúng đủ sổ nguồn để kiểm; bản gửi đi KHÔNG
nhúng, và nguồn nội bộ chỉ hiện nhãn công khai. Nhúng sổ nguồn vào bản gửi khách là tự đưa tên
cơ quan và kênh tin ra ngoài trong một thẻ mà người đọc không thấy nhưng xem mã nguồn thì thấy.

---

## 4. CHỈ THỊ SỬA THIÊN LỆCH

Mỗi mục dưới đây sửa một phản xạ mặc định cụ thể.

### 4.1 Tiêu đề mang hết nghĩa, thân bài mang bằng chứng

Đọc riêng chuỗi tiêu đề phải hiểu được toàn bộ lập luận. Tiêu đề là câu KHẲNG ĐỊNH có số, không
phải nhãn chủ đề.

- Sai: "Tình hình biên lợi nhuận"
- Đúng: "Biên lợi nhuận giảm ba quý liên tiếp, do giá than chứ không do giá bán"

Một trang phục vụ hai tốc độ đọc cùng lúc: tiêu đề cộng câu dẫn phục vụ người đọc 20 giây, thân
trang phục vụ người đọc 10 phút. Không phải hai bản tài liệu, mà là hai tầng trên cùng một trang.

Ngoại lệ: mục lục, phụ lục tra cứu, bảng thuật ngữ. Gắn câu khẳng định lên một bảng tra cứu là
gợi ý sai rằng bảng đó có một kết luận duy nhất.

### 4.2 Kết luận đứng trước, không lùi xuống cuối

Với `MUC_CAM_KET` từ 7 trở lên, trang đầu là verdict cộng bảng mốc, tín hiệu, hành động, cộng
kill-switch. Cấm mở bài bằng recap bối cảnh. Người đọc cần quyết định đã biết bối cảnh rồi.

### 4.3 Mỗi hình trả lời đúng một câu hỏi, và câu hỏi đó viết ra được

Trước khi chọn loại hình, viết ra câu hỏi người đọc đang hỏi ở đúng chỗ đó. Không viết được câu
hỏi thì hình đó không cần tồn tại. Xem mục 5 để đi từ câu hỏi tới loại hình.

### 4.4 Chú thích hình nói thứ thân bài không nói

Chú thích lặp lại tiêu đề hình là chú thích rỗng. Nó phải thêm: cách đọc hình, một ngoại lệ đáng
chú ý, hoặc giới hạn của dữ liệu.

### 4.5 Số phải có ngữ cảnh so sánh

Một con số đứng một mình không mang thông tin. "Biên lợi nhuận 14,2%" chưa nói gì; "14,2%, thấp
nhất trong năm quý và dưới trung vị ngành 3,1 điểm phần trăm" mới nói. Với `DO_SAU` từ 4 trở
lên, mọi số neo trong văn xuôi phải có ít nhất một mốc so sánh.

### 4.6 Phân biệt thực tế với dự phóng bằng thị giác

Số đã xảy ra và số dự phóng không được trông giống nhau. Dùng khác biệt về nét (đường liền so
với đường đứt) hoặc vùng nền, không dùng riêng màu, vì màu mất khi in đen trắng và người mù màu
không đọc được.

### 4.7 Vắng mặt phải có ký hiệu riêng, không để trống

"Chưa tới kỳ", "đã tới kỳ mà chưa công bố", "không áp dụng", "bị loại vì bất thường" là bốn thứ
khác nhau. Để trống cả bốn là xoá thông tin. Với chart, ba cách vẽ khoảng đứt dữ liệu cho ba
thông điệp khác nhau: ngắt đường và chừa chỗ, ngắt hẳn, hay ngắt và đánh dấu trên trục.

### 4.8 Nhất quán số liệu giữa các hình

Hai hình của cùng một mô hình phải khớp nhau. Cặp hay tự mâu thuẫn: bảng tóm tắt so với chart
chi tiết, tổng của biểu đồ cơ cấu so với con số tổng trong văn xuôi, kỳ gốc của hai chart chỉ số
hoá. Sinh cả hai từ MỘT nguồn dữ liệu thay vì gõ lại.

Có trường hợp mâu thuẫn là ĐÚNG: hai hình dùng hai kỳ khác nhau hoặc hai phạm vi hợp nhất khác
nhau. Lúc đó phải nói ra ngay tại chỗ, đừng để người đọc tự phát hiện.

### 4.9 Trang trí phải neo được vào một con số

Bất kỳ yếu tố thị giác nào không neo được vào một con số hoặc một câu cụ thể trên chính trang đó
là trang trí. Phép thử: xoá nó đi, nếu thông điệp mạnh lên thì nó là trang trí.

---

## 5. CHỌN HÌNH THEO CÂU HỎI

Đi từ CÂU HỎI, không đi từ loại dữ liệu. Tám nhóm câu hỏi, mỗi nhóm có họ hình riêng:

| Câu hỏi người đọc đang hỏi | Họ hình |
|---|---|
| Lệch bao nhiêu so với một mốc cố định | thanh hai phía trục 0, thanh phân kỳ xếp chồng |
| Hai đại lượng quan hệ thế nào | scatter, scatter bong bóng, ma trận tương quan |
| Vị trí trong danh sách quan trọng hơn giá trị | thanh xếp hạng, dumbbell, slope |
| Giá trị phân bố ra sao | dot strip, raincloud, ridgeline, hộp |
| Xu hướng theo thời gian | đường có chú thích sự kiện, nến, vùng xếp chồng |
| Một tổng thể phân rã thành các phần | thanh 100%, treemap, waffle |
| So sánh độ lớn | thanh, bullet so với mục tiêu |
| Khối lượng dịch chuyển giữa các trạng thái | sankey (dòng bảo toàn), alluvial (tập được phân loại lại) |

Ba nhóm đặc thù tài chính mà bảng chuẩn phương Tây không tách riêng: **cầu nối tuần tự**
(waterfall, từ doanh thu tới lợi nhuận), **định giá tổng hợp** (football field, nhiều phương
pháp trên một trục), **độ nhạy** (tornado một biến, lưới hai biến).

Ba lỗi chọn hình hay gặp:

1. **Biểu đồ tròn cho cơ cấu.** Mắt người ước lượng góc kém. Dùng thanh 100% khi cần so nhiều
   kỳ, waffle khi cần người đọc nhớ con số.
2. **Hai trục tung trên một chart.** Nó tạo tương quan giả vì thang được chọn tuỳ tiện. Dùng hai
   chart xếp chồng chung trục thời gian.
3. **Gauge và radar.** Gauge lãng phí diện tích cho một con số và mã hoá bằng góc; radar làm
   diện tích méo theo thứ tự trục. Dùng bullet thay gauge, bảng hoặc small multiples thay radar.

Khi có repo: `catalog/CATALOG.md` liệt kê từng tài sản kèm câu hỏi nó trả lời và khi nào đừng
dùng; `research/03-chart-doctrine/CHART-SELECTION.md` là bảng tra đầy đủ tám nhóm trên.

---

## 6. KỶ LUẬT BẰNG CHỨNG

**Mọi số hiển thị phải truy được về một nguồn.** Không có ngoại lệ cho số minh hoạ: số minh hoạ
khai bậc "minh hoạ" và nói rõ trong câu dẫn, chứ không phải khỏi khai.

**Ba bậc nguồn**, và bậc thấp nhất trong bài chặn trần của `MUC_CAM_KET`:

| Bậc | Là gì |
|---|---|
| công bố | số đã công bố chính thức, tra lại được |
| ước tính | ước tính có phương pháp, ghi rõ giả định |
| nội bộ | tính toán nội bộ từ số công bố |

**Không lộ kênh trong file gửi đi.** Bản gửi ra ngoài quy đổi nguồn nội bộ sang nhãn công khai.
Viết mọi artifact như thể nó sẽ bị chuyển tiếp.

**Giả định của mô hình phải hiện diện cạnh kết quả**, không giấu trong phụ lục. Một con số định
giá không kèm giả định chiết khấu là một con số không kiểm được.

---

## 7. RÀNG BUỘC CỨNG

Đây là kết quả đo được, không phải khẩu vị. Vi phạm là hỏng file giao đi.

**Ở cả hai làn:**

- Cấm gauge và radar
- Không em-dash và en-dash ở bất kỳ đâu, kể cả chú thích mã nguồn
- Cấm câu kết kiểu cách ngôn: câu chốt phải có SỐ hoặc HÀNH ĐỘNG, dưới 22 từ
- Cấm bịa lời chứng thực, đánh giá, hay tên người
- Mọi số hiển thị phải có mã trong sổ nguồn, thiếu là dừng build
- `font-family` phải là danh sách kết thúc bằng generic keyword
- Font nhúng thẳng vào file, không trỏ đường dẫn tuyệt đối trên máy đang làm
- Dấu âm dùng dấu gạch nối ASCII, không dùng dấu trừ toán học

**Chỉ ở làn `pdf-so`:**

- Cấm `filter: blur()` và `backdrop-filter`
- Media query co giãn màn hình phải viết `@media screen and (max-width: ...)`, thiếu `screen`
  thì khối đó tự chạy khi in
- Ngưỡng ảnh raster bằng 0
- Chú thích của minh hoạ phải bake trước, vì engine PDF không chạy JavaScript
- Chart tắt animation, vì đường xuất SSR để lại keyframe kéo marker về gốc toạ độ

---

## 8. DẤU HIỆU BÁO CÁO DO MÁY VIẾT

Danh sách này là thứ hay bị vi phạm nhất. Mỗi dòng là một cặp: cùng ý định, một bản đắt và một
bản rẻ.

### 8.A Cấu trúc

| Ý định | Bản đắt | Bản rẻ |
|---|---|---|
| Trình bày nhiều luận điểm | Số luận điểm bằng đúng số luận điểm có thật, có mục một ý và mục bốn ý | Mọi mục đều đúng ba gạch đầu dòng |
| Cân bằng góc nhìn | Nêu rủi ro khi rủi ro có thật, kèm xác suất và ngưỡng | Mục nào cũng có "cơ hội" và "rủi ro" cân bằng giả tạo |
| Đóng một phần | Câu chốt mang số hoặc hành động | "Cần tiếp tục theo dõi", "thời gian sẽ trả lời" |
| Dẫn vào bài | Vào thẳng phát hiện | Mở bằng bối cảnh vĩ mô toàn cầu rồi thu hẹp dần |

### 8.B Con chữ

| Ý định | Bản đắt | Bản rẻ |
|---|---|---|
| Nhấn một ý | Đặt nó ở vị trí mạnh trong câu | "Đáng chú ý là", "Điều thú vị là", mở đầu mọi đoạn |
| Nói về bất định | Nêu khoảng và điều kiện | "Có thể", "dường như", "trong một số trường hợp" chồng lên nhau |
| Chuyển ý | Chuyển bằng nội dung | "Bên cạnh đó", "hơn nữa", "tuy nhiên" mở đầu ba đoạn liên tiếp |
| Tổng kết | Nói điều chưa nói ở trên | Nhắc lại y nguyên các tiêu đề đã có |

### 8.C Hình ảnh

Bảng đầy đủ cho tầng thị giác, gồm cả bẫy riêng của làn `html-song`, nằm ở
`doctrine/05-anti-slop.md`. Bốn dòng hay sai nhất:

| Ý định | Bản rẻ |
|---|---|
| Làm nổi một con số | thẻ số bo tròn, icon mũi tên, viền trái màu, nền đổ nhạt |
| Đa dạng hình | mọi hình đều là bar chart, đổi mỗi màu |
| Dùng chuyển động dẫn mắt | mọi khối đều trôi lên khi cuộn tới, hiệu ứng lặp vô hạn |
| Chart sống thay chart tĩnh | chart sống hiện đúng thứ ảnh tĩnh hiện, chỉ thêm animation lúc vào |

### 8.D Bốn dấu hiệu gộp

Một trang có từ hai dấu hiệu sau trở lên thì gần như chắc là rẻ, dù từng chi tiết trông ổn:

1. Trang trí không neo được vào con số hoặc câu nào trên chính trang đó.
2. Xoá yếu tố đó đi thì thông điệp MẠNH LÊN.
3. Đổi ngành, đổi công ty mà cả trang dùng lại nguyên xi được chỉ bằng cách thay số.
4. Chỉ đứng vững trên màn hình, mất tác dụng khi in đen trắng.

---

## 9. NGOÀI PHẠM VI

Tài liệu này không nói về: xây mô hình định giá (nó nói cách TRÌNH BÀY kết quả mô hình), thu
thập dữ liệu, tuân thủ pháp lý về khuyến nghị đầu tư, và thiết kế giao diện sản phẩm phần mềm.

---

## 10. KIỂM TRƯỚC KHI GIAO

Chạy hết, không bỏ ô nào. Một ô đỏ là chưa xong.

- [ ] Đã tuyên bố cách đọc đề bài (mục 0.B) chưa?
- [ ] Ba núm có giá trị rõ và suy được từ đề bài, không im lặng dùng mặc định?
- [ ] `MUC_CAM_KET` có vượt bậc nguồn thấp nhất trong bài không?
- [ ] Đọc riêng chuỗi tiêu đề có hiểu được toàn bộ lập luận không?
- [ ] Mỗi hình có viết ra được câu hỏi nó trả lời không?
- [ ] Có hình nào là bar chart chỉ vì mặc định không?
- [ ] Mọi số hiển thị có mã nguồn không?
- [ ] Bản gửi đi có lộ kênh nội bộ không?
- [ ] Hai hình của cùng một mô hình có khớp số không?
- [ ] Số thực tế và số dự phóng có phân biệt được khi in đen trắng không?
- [ ] Ô trống trong bảng có ký hiệu phân biệt bốn loại vắng mặt không?
- [ ] Không có em-dash và en-dash ở bất kỳ đâu?
- [ ] Câu chốt cuối mỗi phần có số hoặc hành động, dưới 22 từ?
- [ ] Đã đọc lại mục 8 và đối chiếu từng dòng chưa?

Khi có repo, chạy thêm phần máy kiểm được:

```bash
node gates/run.mjs <html> <pdf> --che-do=gui-di    # làn pdf-so, 10 gate
node gates/run.mjs <html> --lan=html-song           # làn html-song, 9 gate
npm run verify                                       # thư viện hình
```

---

## 11. KHI CÓ REPO: CHỖ THI CÔNG

| Cần | Ở đâu |
|---|---|
| Tra cứu sâu bốn mục doctrine | `doctrine/README.md` |
| Kiến trúc ấn phẩm, thứ tự phần, bộ khung theo mức cam kết | `doctrine/01-ke-chuyen.md` |
| Chọn hình theo câu hỏi, danh sách đen kèm lý do | `doctrine/02-chon-hinh.md` |
| Viết câu chủ đề, nói về bất định, viết chú thích hình | `doctrine/03-viet-chu.md` |
| Phân biệt bản đắt và bản rẻ trong ba giây | `doctrine/05-anti-slop.md` |
| Chọn hình cho một section | `catalog/CATALOG.md`, đọc đầu tiên |
| Nhìn cả kho một lượt | `catalog/contact-sheet.pdf` |
| Bảng tra chọn hình theo tám nhóm câu hỏi | `research/03-chart-doctrine/CHART-SELECTION.md` |
| Ranh giới đắt và rẻ ở tầng thị giác | `research/04-wow-layer/ANTI-SLOP.md` |
| Bảng màu cho 4, 6, 8 chuỗi, an toàn đen trắng và mù màu | `research/07-bw-palette/PALETTE-TABLE.md` |
| Ký hiệu sáu loại vắng mặt | `research/11-empty-states/ABSENCE-TABLE.md` |
| Quy đổi nguồn cho bản gửi đi | `research/06-source-notes/SOURCE-DISCLOSURE.md` |
| Ẩn dụ minh hoạ theo ngành | `research/09-metaphor/METAPHOR-TABLE-EXT.md` và `illustrations/grammar.md` |
| Chạy trọn đường ống | `python3 pipeline/orchestrator.py <thu-muc>/noi-dung.md [--lan=html-song]` |
| Ấn phẩm mẫu chạy được | `examples/mau-phase2/` cho `pdf-so`, `examples/van-tai-bien/` cho `html-song` |
| Quy ước kỹ thuật và lý do từng luật | `CLAUDE.md` |
| Đang ở đâu, làm gì tiếp | `memory.md` |

Thư viện hiện có 116 tài sản: 23 chart ECharts, 53 component matplotlib, 29 component kể chuyện,
11 minh hoạ ngành. Mục lục sinh tự động từ mã nguồn, có test ép hai bên khớp nhau.

**Component và preset là Ý THAM KHẢO, không phải khuôn ép.** Không bắt buộc dùng hết hay dùng
nguyên bản. Ràng buộc cứng ở mục 7 mới là thứ không thương lượng.
