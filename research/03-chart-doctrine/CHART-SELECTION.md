# Bảng tra chọn chart cho báo cáo tài chính Việt Nam

Đây là ý tham khảo, không phải khuôn ép (xem `FINDINGS.md` §0). Cấu trúc học theo FT Visual
Vocabulary: mỗi hàng bắt đầu bằng CÂU HỎI người đọc đang hỏi, không phải bằng loại dữ liệu.
Mở rộng thêm 3 nhóm đặc thù tài chính mà FT không tách riêng (cầu nối tuần tự, định giá tổng
hợp, độ nhạy).

Cột "Engine trong repo": tên file `.mjs` trong `charts/echarts/` nếu đã có sẵn, `matplotlib`
nếu hợp tầng `charts/matplotlib/viz_eir*.py` hơn, hoặc "chưa có, xem mẫu ..." trỏ tới file HTML
minh hoạ trong `samples/`.

## Deviation — lệch bao nhiêu so với 1 mốc cố định

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Từng khoản mục lệch bao nhiêu so với kế hoạch/kỳ trước, dấu +/- quan trọng? | Diverging bar | Bar 2 phía trục 0, sắp theo độ lệch | Trộn màu valence vào màu chiều (xem luật màu ở CLAUDE.md) | Chưa có sẵn `.mjs` riêng, dựng từ `valueAxis` + 2 series bar giống `01-waterfall.mjs` |
| So YoY/QoQ hàng loạt chỉ tiêu cùng lúc? | Diverging stacked bar | Xếp chồng phần tăng/giảm | Trục không đối xứng quanh 0 làm khó so 2 phía | Tương tự trên, mở rộng `12-area-stack.mjs` |

## Correlation — hai đại lượng quan hệ thế nào

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| P/E và tăng trưởng lợi nhuận của các mã có tương quan không? | Scatterplot | Bubble (thêm chiều thứ 3 = vốn hoá) | Quá nhiều điểm gây chồng lấp, cần jitter hoặc lọc | Chưa có, ECharts `scatter` cơ bản, kế thừa `theme.mjs` |
| Giá cổ phiếu và khối lượng cùng lúc? | Line + Column (2 trục) | | Dual-axis dễ tạo tương quan giả khi tự động chọn thang (xem `FINDINGS.md` §3) | `09-candlestick.mjs` (đã có khối lượng dưới nến) |
| Ma trận tương quan nhiều cặp biến? | XY heatmap | | Thang màu diverging quá gắt gây đọc nhầm mức | `08-heatmap.mjs` |

## Ranking — vị trí trong danh sách quan trọng hơn giá trị tuyệt đối

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Xếp hạng 10-15 ngân hàng theo NIM/ROE? | Ordered bar hoặc Cleveland dot plot | Dot plot khi cần giảm mực in (nhiều hạng mục, khổ hẹp) | Không sắp theo giá trị, để mặc định theo alphabet | Chưa có, xem mẫu `chart-cleveland-dot-xep-hang.html` |
| So 2 mốc thời gian cho cùng danh sách xếp hạng (đầu kỳ vs cuối kỳ)? | Dumbbell / slope | Dumbbell khi 2 điểm rời rạc, slope khi nhấn mạnh xu hướng | Quá nhiều hạng mục làm các đường chồng chéo (>10-12 dòng) | `04-dumbbell.mjs`, `05-slope.mjs` |

## Distribution — giá trị phân bố ra sao

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| P/E toàn ngành phân bố thế nào, có ngoại lệ không? | Boxplot / dot strip | Violin nếu cần thấy hình dạng phân bố chi tiết | Boxplot che mất số lượng mẫu nhỏ (n thấp mà vẫn vẽ như phân bố đầy đủ) | Chưa có, ưu tiên matplotlib cho boxplot tĩnh |
| Phân bố tuổi nợ xấu / kỳ hạn trái phiếu? | Histogram | | Chọn bin-width tuỳ tiện làm méo hình dạng phân bố | matplotlib |

## Change over time — xu hướng theo thời gian

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Doanh thu/lợi nhuận qua các quý? | Line hoặc column | Column khi số kỳ ít (<12), line khi số kỳ nhiều | Trộn line và bar 2 trục y không cẩn thận (xem dual-axis ở `FINDINGS.md`) | Nền tảng có sẵn trong `theme.mjs::valueAxis/categoryAxis` |
| Giá cổ phiếu theo phiên? | Candlestick | Kèm khối lượng dưới, đường MA overlay | Dựa 100% vào màu xanh/đỏ mà không có mã hoá phụ (xem §8 FINDINGS) | `09-candlestick.mjs` |
| Dự phóng có dải bất định (upside/downside)? | Fan chart | Dải càng xa càng loang rộng | Không phân biệt được đâu là dữ liệu thực, đâu là dự phóng nếu không đổi kiểu nét | Chưa có, mở rộng từ `12-area-stack.mjs` với `lineStyle.type: 'dashed'` cho đoạn dự phóng |
| So nhiều chỉ tiêu cùng xu hướng nhưng thang khác nhau? | Small multiples | Lưới 6-9 ô, trục đồng bộ trong từng nhóm cùng đơn vị | Quên đồng bộ trục giữa các ô (xem §6 FINDINGS) | `07-small-multiples.mjs` |

## Part-to-whole — một tổng thể phân rã thành các phần

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Cơ cấu vốn/tài sản tại 1 thời điểm, ≤3-4 phần? | Stacked bar 100% (1 cột) hoặc donut nhỏ | Donut chỉ khi ≤3 lát (xem §3 FINDINGS) | Vẽ pie/donut cho >4 lát | `11-stacked-100.mjs` cho 1-nhiều kỳ, pie/donut KHÔNG có sẵn (cố ý, xem danh sách đen) |
| Cơ cấu thay đổi qua nhiều kỳ? | Stacked column hoặc 100% stacked column | | Thứ tự xếp chồng đảo lộn giữa các cột làm khó so 1 dải qua thời gian | `11-stacked-100.mjs`, `12-area-stack.mjs` |
| Phân cấp lồng nhau (ngành > tiểu ngành > mã)? | Treemap | | Diện tích quá nhỏ mất nhãn, quá nhiều cấp gây rối | `10-treemap.mjs` |

## Magnitude — so sánh độ lớn

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| So quy mô tài sản giữa các ngân hàng? | Column/bar đơn giản | Paired bar nếu so 2 kỳ | Trục không từ 0 (ràng buộc cứng, xem `valueAxis`) | Nền tảng `theme.mjs` |
| KPI thực tế so mục tiêu, có dải định tính? | Bullet chart | | Vẽ target bằng bar chồng thay vì 1 vạch | `03-bullet.mjs` |

## Flow — khối lượng dịch chuyển giữa các trạng thái

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Dòng vốn di chuyển giữa các danh mục/phân khúc? | Sankey | | Quá nhiều nút làm luồng chồng chéo không đọc được | `02-sankey.mjs` |

## Nhóm đặc thù tài chính (mở rộng ngoài 9 nhóm FT)

| Câu hỏi | Chart phù hợp | Biến thể | Bẫy thường gặp | Engine trong repo |
|---|---|---|---|---|
| Một tổng bị phân rã bởi các khoản cộng/trừ CÓ TRẬT TỰ nghiệp vụ (DThu → LNST)? | Waterfall (cầu nối) | Cầu nối vốn CSH, cầu nối EBITDA→FCF | Quên tô khác màu cho subtotal (điểm đầu/cuối) với delta giữa | `01-waterfall.mjs` |
| Tổng hợp nhiều phương pháp định giá thành 1 kết luận? | Football field | Kèm vạch giá thị trường hiện tại, dải vùng hội tụ | Sắp xếp ngẫu nhiên các phương pháp thay vì theo logic (thường: thị trường trước, nội tại sau) | Chưa có, xem mẫu `chart-football-field-dinh-gia.html`; đề xuất vào `theme.mjs` (xem FINDINGS §9) |
| Biến nào tác động mạnh nhất lên 1 kết quả khi thay đổi TỪNG biến 1? | Tornado | Sắp theo biên độ giảm dần | Không neo rõ base case, hoặc tô "lạc quan" bằng màu dương (traffic-light trá hình) | `06-tornado.mjs` |
| 2 biến cùng tác động đồng thời lên 1 kết quả (ví dụ WACC × g)? | Lưới độ nhạy 2 chiều | Bảng nhiệt N×M, base case viền riêng | Dùng thang diverging 2 hue gắt thay vì 1 hue liên tục nhạt-đậm | Chưa có, xem mẫu `chart-luoi-do-nhay-hai-chieu.html` |
| Đóng nến tăng/giảm theo phiên với đủ chi tiết OHLC? | Candlestick | | Không kiểm tra High là max, Low là min của 4 giá (dữ liệu lỗi vẽ ra bấc lộn ngược) | `09-candlestick.mjs` |

## Bẫy khi giao file: nhúng font sai làm lộn glyph tiếng Việt trong PDF

`design-system/fonts/fonts-embedded.css` (tại thời điểm viết tài liệu này) đang có bug: 24 khối
`@font-face` cho 12 tổ hợp family/style/weight, mỗi tổ hợp khai 2 lần chỉ khác `unicode-range`
(subset vietnamese/latin). WeasyPrint không chọn đúng subset khi trùng family/weight/style, chữ
tiếng Việt bị lộn glyph ở tầng text PDF (đã tái hiện: "nghệ" ra "nght", "liệu" ra "litu").
Trình duyệt xử lý `unicode-range` đúng nên nghiệm thu bằng Chromium KHÔNG bắt được bug này,
chỉ lộ ra khi mở PDF thật và đọc lại tầng text. Nhãn chart là nơi dày dấu tiếng Việt và ít ai
soi kỹ nhất, nên đây là bẫy đặc biệt cần lưu ý khi chart xuất ra PDF (tầng matplotlib hoặc
ECharts SVG nhúng vào trang WeasyPrint render). Khắc phục: dùng font stack có fallback thật
(`"Spectral", "Noto Serif", Georgia, "Times New Roman", serif`), KHÔNG nhúng
`fonts-embedded.css` hay copy khối `@font-face` 2-subset đó vào bất kỳ mẫu/preset chart nào,
cho tới khi Task 2 gộp xong 2 subset thành 1 khối mỗi weight. Xem chi tiết
`FINDINGS.md` mục 0.1.

## Bẫy khi giao file: `<svg height="auto">` và `filter: grayscale()` rỗng/sai trong WeasyPrint

Hai bẫy im lặng tuyệt đối, không lỗi không cảnh báo, chỉ lộ ra khi mở đúng file PDF (không phải
xem trên Chromium) và đếm số vector vẽ được. Chi tiết đầy đủ, bảng số liệu trước/sau và bảng
quy đổi hex ở `FINDINGS.md` mục 0.2.

1. `<svg width="100%" height="auto" viewBox="...">` render RỖNG HOÀN TOÀN trên WeasyPrint 69.0
   (0 object vẽ được), dù `viewBox` vẫn khai đủ và file mở trên Chromium vẫn đẹp bình thường.
   Thủ phạm là `height="auto"` một mình nó đã đủ. Sửa: bỏ hẳn `height="auto"`, chỉ giữ
   `width="100%"` + `viewBox`; khống chế chiều cao (nếu cần) bằng CSS trên phần tử bao ngoài.
2. `filter: grayscale()` (và CSS `filter` nói chung) bị WeasyPrint bỏ qua hoàn toàn, không
   raster hoá sai, chỉ đơn giản không áp dụng: 1 SVG màu bọc `filter: grayscale(1)` hiện lên
   NGUYÊN MÀU trong PDF. Nguy hiểm hơn bẫy 1 vì chart vẫn "trông có nội dung" (số drawing vẫn
   cao bình thường), chỉ sai đúng cái mà mắt cần soi kỹ mới thấy. Sửa: không dùng `filter`,
   tính tay hex xám bằng công thức luminance BT.709 (`Y = 0,2126R + 0,7152G + 0,0722B`) và
   nhúng làm giá trị `fill`/`stroke` tĩnh.

Quy trình nghiệm thu bắt buộc cho mọi chart SVG cần ra PDF: (1) đếm object vẽ được bằng
`fitz`/PyMuPDF (`page.get_drawings()`) sau khi render qua `weasyprint`, vài đơn vị trong khi
SVG có nội dung phức tạp là dấu hiệu rỗng; (2) render ra PNG và tự mở ảnh nhìn tận mắt, vì đếm
drawing không bắt được trường hợp vẽ SAI (bẫy 2); (3) không bao giờ coi "đẹp trên Chromium" là
bằng chứng đủ cho bản sẽ đi qua WeasyPrint.

## Bảng phụ: khi câu hỏi trông giống 1 chart giả, chuyển sang chart nào

| Người yêu cầu muốn thấy | Chart họ hay đòi (đã bị cấm/nên tránh) | Chart thay thế đúng nghĩa | Vì sao thay thế tốt hơn |
|---|---|---|---|
| "Cho tôi 1 hình tổng quan sức khoẻ tài chính 5 chỉ số" | Radar/spider | Small multiples (5 ô bar nhỏ) hoặc bullet chart 5 hàng | Không có trục chung ảo, diện tích không nói dối (xem §3 FINDINGS) |
| "1 đồng hồ đo mức độ rủi ro" | Gauge | Bullet chart 1 hàng | Cùng thông tin, 1/5 không gian, đọc bằng vị trí không phải góc |
| "Cơ cấu doanh thu theo 6 mảng kinh doanh" | Pie/donut 6 lát | Bar ngang xếp theo giá trị giảm dần | Mắt so độ dài chính xác hơn so góc, đặc biệt khi 2 lát gần bằng nhau |
| "Giá cổ phiếu và tin tức cùng trục để thấy tương quan" | Dual-axis tự động scale | 2 chart xếp chồng cùng trục thời gian (small multiples dọc) | Tránh chọn thang tuỳ ý tạo tương quan giả (xem §3 FINDINGS) |
