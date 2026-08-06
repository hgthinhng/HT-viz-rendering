# Hồ sơ nghiên cứu: Hệ thống style biểu đồ của toà soạn và tổ chức data viz hàng đầu

Phạm vi: khảo sát FT Visual Vocabulary, The Economist, BBC, Reuters Graphics, Datawrapper,
Observable Plot, Vega-Lite, Urban Institute, CFPB, Tufte, và quy ước biểu đồ tài chính
(sell-side/Bloomberg), rồi chắt lọc thành thứ dùng được cho `charts/echarts/` và
`charts/matplotlib/` của repo này.

## 0. Đọc trước khi dùng bất cứ ý nào dưới đây

Tài liệu này là **thư viện tham khảo để lấy ý, không phải khuôn ép**. Mọi mục đều được viết
kèm "khi nào KHÔNG nên dùng" — nếu bạn thấy một mục chỉ toàn mệnh lệnh mà không có phần đó,
đó là lỗi của tài liệu này, không phải luật.

Hai loại việc khác nhau:
- **RÀNG BUỘC CỨNG của repo** (đã liệt kê đủ trong `CLAUDE.md` gốc, không nhắc lại ở đây):
  cấm gauge/radar, màu theo chiều không theo valence, shadow blur=0, media query có `screen`,
  cấm em-dash, font-family kết thúc generic keyword, `chart.dispose(); process.exit(0);`,
  định dạng số tiếng Việt. Những cái này áp dụng bất kể nguồn nào nói khác.
- **Ý tham khảo** (toàn bộ nội dung bên dưới): lấy ý, đổi ý, bỏ ý tuỳ ngữ cảnh báo cáo.

### 0.1 Cảnh báo kỹ thuật phát sinh trong lúc nghiên cứu: đừng nhúng `fonts-embedded.css`

Phát hiện của Task 2 trong Phase 1, ghi lại ở đây vì nhãn chart là chỗ dày dấu tiếng Việt nhất
và cũng là chỗ ít ai soi kỹ nhất khi nghiệm thu. `design-system/fonts/fonts-embedded.css`
(tại thời điểm viết tài liệu này) khai 24 khối `@font-face` cho 12 tổ hợp (family, style,
weight), mỗi tổ hợp 2 lần chỉ khác `unicode-range` (subset vietnamese và subset latin).
WeasyPrint 69.0 KHÔNG chọn đúng subset theo `unicode-range` khi trùng family/weight/style, nên
chữ tiếng Việt bị LỘN GLYPH ở tầng text của PDF (ví dụ đã tái hiện: "nghệ" ra "nght", "liệu" ra
"litu"). Nguy hiểm nhất: **trình duyệt (Chromium) xử lý `unicode-range` ĐÚNG, WeasyPrint thì
không** — nghiệm thu bằng cách mở file trong Chromium sẽ thấy bình thường và bug lọt qua hoàn
toàn, chỉ lộ ra khi mở PDF thật và đọc lại tầng text so với chuỗi gốc.

Áp dụng cho mọi mẫu trong `research/` và `samples/`: KHÔNG nạp `design-system/fonts/fonts-
embedded.css`, KHÔNG copy khối `@font-face` 2-subset đó vào file mẫu. Toàn bộ 8 mẫu chart
trong `samples/` của tài liệu này chỉ dùng font stack có fallback lấy nguyên từ
`design-system/tokens.css` (`"Spectral", "Noto Serif", Georgia, "Times New Roman", serif` và
`"IBM Plex Mono", "Noto Sans Mono", Menlo, Consolas, "Liberation Mono", monospace`), không
nhúng font riêng — đã kiểm lại bằng grep, không file nào tham chiếu `fonts-embedded.css` hay
`@font-face`. Bài học chung cho tài liệu này: **nghiệm thu bản in bằng cách xem trên trình
duyệt là không đủ**, phải mở PDF thật và đọc lại tầng text.

## 1. Nguồn đã khảo sát (24 lượt WebSearch/WebFetch)

| Nguồn | Loại | Truy cập được | Dùng cho mục |
|---|---|---|---|
| [FT Visual Vocabulary / chart-doctor README](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md) | Github, fetch trực tiếp | Có | §2 |
| [FT chart-doctor repo](https://github.com/Financial-Times/chart-doctor) | Github | Có (gián tiếp qua search) | §2 |
| [The Economist style — AECharts Medium](https://medium.com/@aecharts/how-to-create-the-economist-style-charts-f2052ba6d6d3) | Bài viết phân tích | Có (qua tóm tắt search) | §3, §4 |
| [Economist visual style guide — Fountn](https://fountn.design/resource/the-economist-visual-style-guide/) | Tổng hợp | Có (qua search) | §4 |
| [BBC `rcookbook`](https://bbc.github.io/rcookbook/) | Tài liệu chính thức | Có (qua search) | §4, §6 |
| [Reuters Graphics — Colors](https://reuters-graphics.github.io/style/colors/) | Fetch trực tiếp | Có | §6 |
| [Reuters Graphics — awesome-charts](https://github.com/reuters-graphics/awesome-charts) | Github | Có (qua search) | §2 |
| [Datawrapper — colorblindness part 1](https://www.datawrapper.de/blog/colorblindness-part1) | Blog | Có (qua search) | §6 |
| [Datawrapper — colorblindness part 2](https://www.datawrapper.de/blog/colorblindness-part2) | Fetch trực tiếp | Có | §6 |
| [Datawrapper — colorblind check tool](https://www.datawrapper.de/blog/colorblind-check) | Blog | Có (qua search) | §6 |
| [Datawrapper — annotations trong bar/range/dot chart](https://www.datawrapper.de/blog/annotations-in-bar-charts) | Blog | Có (qua search) | §3 |
| [Datawrapper — color keys](https://www.datawrapper.de/blog/color-keys-for-data-visualizations) | Blog | Có (qua search) | §3, §6 |
| [Datawrapper — grids vs data labels](https://data.europa.eu/apps/data-visualisation-guide/grids-versus-data-labels-in-bar-charts) | Tổng hợp lại nội dung Datawrapper | Có (qua search) | §4 |
| [Urban Institute Data Viz Style Guide](https://urbaninstitute.github.io/graphics-styleguide/) | Fetch trực tiếp | Có | §4, §6 |
| [CFPB design manual — bài của Amy Cesal](https://www.amycesal.com/cfpb-design-manual-data-visualization) | Bài viết của tác giả gốc | Có (qua search, không fetch được trang CFPB chính thức vì đã archive) | §4 |
| [Tufte — nguyên lý data-ink (tổng hợp EDAV)](https://jtr13.github.io/cc19/tuftes-principles-of-data-ink.html) | Tài liệu học thuật | Có (qua search) | §2, §5 |
| [Wall Street Prep — Football Field](https://www.wallstreetprep.com/knowledge/football-field-valuation-real-example-excel-template/) | Tài liệu nghiệp vụ IB | Có (qua search) | §7 |
| [Macabacus — Football Field build](https://macabacus.com/blog/build-football-field-chart-excel) | Tài liệu nghiệp vụ IB | Có (qua search) | §7 |
| [Observable — avoid radar charts](https://observablehq.com/blog/avoid-radar-charts) | Bài kỹ thuật | Có (qua search) | §3 |
| [Highcharts — radar chart explained](https://www.highcharts.com/blog/tutorials/radar-chart-explained-when-they-work-when-they-fail-and-how-to-use-them-right/) | Blog nhà cung cấp thư viện | Có (qua search) | §3 |
| [Stephanie Evergreen — gauge diagram](https://stephanieevergreen.com/gauge-diagram/) | Bài chuyên gia dataviz | Có (qua search) | §3 |
| [Perceptual Edge — Bullet Graph Design Spec (Stephen Few, PDF)](https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf) | Tài liệu gốc | Có (qua search) | §7 |
| [Michael Correll — Truncating the Y-Axis (arXiv)](https://arxiv.org/pdf/1907.02035) | Bài nghiên cứu | Có (qua search) | §3, §5 |
| [QuantHub — Avoid Truncated Axes](https://www.quanthub.com/common-chart-design-pitfalls-truncated-axes/) | Bài hướng dẫn | Có (qua search) | §5 |
| [Flourish — dual-axis charts](https://flourish.studio/blog/dual-axis-charts/) | Blog nhà cung cấp thư viện | Có (qua search) | §3 |
| [Data-to-viz — vấn đề pie chart](https://www.data-to-viz.com/caveat/pie.html) | Tài liệu tham khảo dataviz | Có (qua search) | §3 |
| [Observable — sự thật về pie chart](https://observablehq.com/blog/truth-about-pie-charts) | Bài kỹ thuật | Có (qua search) | §3 |
| [Solomon Messing — Cleveland và Tufte về small multiples](https://solomonmg.github.io/post/visualization-series-insight-from-cleveland-and-tufte-on-plotting-numeric-data-by-groups/) | Bài tổng hợp học thuật | Có (qua search) | §5 |
| [Observable Plot Github](https://github.com/observablehq/plot) | Github | Có (qua search) | §2 |
| [Vega-Lite chính thức](https://vega.github.io/vega-lite/) | Trang chính thức | Có (qua search) | §2 |
| [ibinterviewquestions — tornado/football field chart DCF](https://ibinterviewquestions.com/guides/valuation-investment-banking/football-field-chart-how-bankers-synthesize-valuation) | Tài liệu nghiệp vụ | Có (qua search) | §7 |

Không truy cập được trực tiếp (chỉ có qua bản tóm tắt của công cụ tìm kiếm, không fetch được
trang gốc): trang CFPB Design System chính thức (`cfpb.github.io/design-system`) đã đổi cấu
trúc, bài viết của Amy Cesal (người trực tiếp làm guide đó) dùng thay thế đủ tin cậy. Ghi nhận
và đi tiếp, không bịa nội dung không kiểm chứng được.

## 2. Ngữ pháp chọn loại chart: học đúng cấu trúc FT Visual Vocabulary rồi mở rộng cho VN

**Nguồn**: [FT Visual Vocabulary README](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md).

### Thủ pháp gốc

FT không phân loại chart theo *loại dữ liệu* (số, chuỗi thời gian, phần trăm...) mà theo
**câu hỏi người đọc đang hỏi**. Chín nhóm câu hỏi, mỗi nhóm có 4 đến 9 biến thể chart cụ thể:

1. **Deviation** — "đại lượng này lệch bao nhiêu so với một mốc cố định?" (diverging bar,
   spine chart, surplus/deficit filled line)
2. **Correlation** — "hai biến này quan hệ với nhau thế nào?" (scatterplot, line+column,
   connected scatterplot, bubble, XY heatmap)
3. **Ranking** — "vị trí trong danh sách xếp hạng quan trọng hơn giá trị tuyệt đối" (ordered
   bar, dot strip plot, slope, lollipop)
4. **Distribution** — "giá trị phân bố ra sao và tần suất thế nào?" (histogram, boxplot,
   violin, population pyramid, dot plot)
5. **Change over time** — "xu hướng thay đổi theo thời gian" (line, column, stock price,
   area, fan chart cho dự phóng, calendar heatmap)
6. **Part-to-whole** — "một tổng thể bị phân rã thành các phần thế nào?" (stacked column,
   pie, donut, treemap, waterfall)
7. **Magnitude** — "so sánh độ lớn" (column/bar, proportional symbol, isotype)
8. **Spatial** — "chỉ dùng khi vị trí địa lý chính xác hoặc mô hình không gian quan trọng
   hơn giá trị" (choropleth, flow map, cartogram)
9. **Flow** — "thể hiện khối lượng/cường độ dịch chuyển giữa các trạng thái" (sankey,
   waterfall, chord, network)

Điểm mấu chốt trong cách viết của FT: mỗi nhóm mở đầu bằng một **câu hỏi**, không phải một
**định nghĩa dữ liệu**. Đây là lý do bảng tra hoạt động tốt: người dùng thực tế (nhà báo,
nhà phân tích) nghĩ bằng câu hỏi ("số này so kỳ trước ra sao?"), không nghĩ bằng cấu trúc
bảng dữ liệu.

### Chuyển sang bối cảnh tài chính Việt Nam

Bảng đầy đủ nằm ở `CHART-SELECTION.md`. Điểm mở rộng quan trọng nhất: tài chính doanh nghiệp/
định giá có một nhóm câu hỏi FT không có sẵn vị trí rõ ràng — **"một con số bị phân rã bởi cấu
phần cộng/trừ CÓ TRẬT TỰ, và trật tự đó mang ý nghĩa nghiệp vụ"** (cầu nối P&L, cầu nối vốn chủ
sở hữu, phân rã ROE theo Dupont). FT xếp waterfall vào cả "part-to-whole" và "flow" — đúng về
mặt hình học nhưng không giúp người mới chọn nhanh. Ở bảng tra của repo này, waterfall được
tách thành nhóm riêng **"Cầu nối / phân rã tuần tự"** vì đây là loại chart xuất hiện nhiều nhất
trong báo cáo tài chính VN (phân tích biến động lợi nhuận theo quý, theo cấu phần chi phí).

**Khi nào KHÔNG áp dụng ngữ pháp này**: khi báo cáo cần một hình ẩn dụ minh hoạ (xem
`illustrations/grammar.md`) chứ không phải một biểu đồ số liệu — ngữ pháp chọn chart không áp
dụng cho minh hoạ ngành.

## 3. Chart giả và chart lừa: cơ chế đo được, không phải ý kiến

Gauge và radar đã bị cấm cứng. Dưới đây là cơ chế cụ thể của từng cái, cộng thêm ba loại khác
đáng liệt kê thêm vào danh sách đen tham khảo (không phải cấm cứng, nhưng nên tránh trong ngữ
cảnh báo cáo tài chính xuất bản).

### Radar/spider chart — tại sao diện tích nói dối

**Nguồn**: [Observable — avoid radar charts](https://observablehq.com/blog/avoid-radar-charts),
[Highcharts — radar chart explained](https://www.highcharts.com/blog/tutorials/radar-chart-explained-when-they-work-when-they-fail-and-how-to-use-them-right/).

Cơ chế: diện tích đa giác trong radar tăng theo **bình phương** giá trị trên mỗi trục (diện
tích tam giác = 1/2·a·b·sin(theta), nhân dồn qua N trục), trong khi giá trị thật chỉ tăng
tuyến tính. Người đọc nhìn "diện tích lớn hơn" và suy ra "tốt hơn nhiều hơn thực tế". Thêm
vào đó, các trục toả ra từ tâm không có đường cơ sở chung (contrast với trục x/y chung của
bar/line), nên so sánh giữa hai trục không liền kề đòi hỏi đếm vòng tròn đồng tâm — việc não
người làm kém. Cuối cùng, **hình dạng đa giác phụ thuộc vào THỨ TỰ xếp trục**: đổi thứ tự 5
chỉ số tài chính quanh vòng tròn ra hình dạng khác hẳn dù dữ liệu không đổi — chứng minh trực
quan trong mẫu `chart-radar-vs-cleveland.html`.

**Chuyển sang bối cảnh này**: dùng small multiples của bar/dot-strip (mỗi chỉ số 1 ô nhỏ, cùng
thang), hoặc bullet chart nếu có mục tiêu rõ ràng cho từng chỉ số.

### Gauge — chiếm diện tích lớn cho 1 số, đọc góc kém

**Nguồn**: [Stephanie Evergreen — gauge diagram](https://stephanieevergreen.com/gauge-diagram/),
Perceptual Edge/Stephen Few (nguồn gốc phát minh bullet chart để thay gauge).

Cơ chế: Cleveland (1984) đã đo thực nghiệm con người đọc SAI góc/độ dài cung tốt hơn nhiều so
với đọc SAI vị trí trên trục thẳng. Gauge mã hoá giá trị bằng góc kim đồng hồ — đúng loại mã
hoá kém chính xác nhất theo thang bậc của Cleveland — trong khi chiếm không gian ngang một cột
số liệu đầy đủ ngữ cảnh (target, dải định tính, xu hướng). Bullet chart (Stephen Few, 2005,
[bản spec gốc](https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf)) giải
quyết đúng vấn đề gauge cố giải quyết (so KPI với mục tiêu) trong 1/5 không gian, dùng trục
thẳng thay vì góc. Repo đã có `charts/echarts/03-bullet.mjs` đúng tinh thần này.

### Pie/donut nhiều lát — con người đọc góc kém, không phải "chỉ là gu"

**Nguồn**: [Data-to-viz — vấn đề pie chart](https://www.data-to-viz.com/caveat/pie.html),
[Observable — sự thật về pie chart](https://observablehq.com/blog/truth-about-pie-charts).

Cơ chế: con người có xu hướng **overestimate góc tù, underestimate góc nhọn**, và sai số này
tăng theo số lát. Vấn đề thứ hai ít được nhắc: khi 2 lát có kích thước gần bằng nhau, mắt không
phân biệt được lát nào lớn hơn (bar giải quyết bằng cách đưa mọi giá trị về 1 trục chung, dễ so
hơn hẳn). Đây KHÔNG phải ràng buộc cứng của repo (pie không nằm trong danh sách cấm ở
`CLAUDE.md`), nhưng nên áp dụng ngưỡng thực dụng: **≤3 lát và mục đích là "một phần chiếm áp
đảo phần còn lại" thì pie/donut còn chấp nhận được**; từ 4 lát trở lên, hoặc khi cần so sánh
chính xác giữa các lát, chuyển sang bar ngang xếp theo giá trị giảm dần. Xem mẫu
`chart-pie-vs-bar-thi-phan.html`.

### Trục bar/column bị cắt cụt — bar mã hoá bằng ĐỘ DÀI, cắt trục phá vỡ mã hoá đó

**Nguồn**: [Michael Correll — Truncating the Y-Axis (arXiv, Tableau Research)](https://arxiv.org/pdf/1907.02035),
[QuantHub — Avoid Truncated Axes](https://www.quanthub.com/common-chart-design-pitfalls-truncated-axes/),
Urban Institute style guide.

Cơ chế: bar/column mã hoá giá trị bằng **chiều dài từ 0**. Cắt trục (bắt đầu từ 890 thay vì 0)
làm chiều dài thanh không còn tỷ lệ thuận với giá trị — một chênh lệch 2% bị vẽ trông như 200%.
Đây là lý do "trục bar phải từ 0" là **ràng buộc cứng của ngành**, không riêng repo này (Urban
Institute, FT, Economist đều thống nhất). Correll (nghiên cứu Tableau) chỉ ra thêm: line chart
KHÔNG bắt buộc từ 0 vì line mã hoá bằng **độ dốc/vị trí tương đối**, không phải độ dài tuyệt
đối từ gốc — cắt trục line để phóng đại biến động nhỏ là hợp lệ NẾU trục được đánh dấu rõ ràng
(ký hiệu gãy trục hoặc dải màu nhạt đánh dấu vùng bị cắt) và mục đích là thấy biến động ngắn
hạn (ví dụ lợi suất TPCP dao động trong biên độ hẹp). Xem chứng minh trực quan trong mẫu
`chart-truc-cat-vs-tu-khong.html`.

**Khi nào ĐƯỢC cắt trục**: line/scatter khi biến động thực sự nhỏ so với mức nền và mục đích rõ
ràng là "biến động ngắn hạn", LUÔN đánh dấu điểm gãy. **Khi nào TUYỆT ĐỐI không**: bất kỳ bar,
column, hay diện tích nào — đây trùng với ràng buộc "trục bắt đầu từ 0 cho bar/column" đã có
sẵn trong `theme.mjs` (`valueAxis({ startAtZero: true })` mặc định).

### Dual-axis chart — tương quan giả bằng cách chọn thang tuỳ ý

**Nguồn**: [Flourish — dual-axis charts](https://flourish.studio/blog/dual-axis-charts/),
[PolicyViz — avoiding the dual axis chart](https://policyviz.com/2022/10/06/avoiding-the-dual-axis-chart/).

Cơ chế: khi 2 chuỗi dùng 2 trục y độc lập, người vẽ có thể **chọn khoảng trục tuỳ ý** để 2
đường trông "khớp nhau" hoàn hảo, tạo cảm giác tương quan mạnh dù dữ liệu thật yếu hoặc không
liên quan. Vấn đề nặng hơn khi 2 đường CẮT NHAU — điểm cắt của 2 trục khác nhau không có ý
nghĩa gì cả (không phải "hai đại lượng bằng nhau tại đó") nhưng mắt người tự động đọc điểm cắt
như một sự kiện quan trọng. **Đây không phải ràng buộc cứng của repo**, nhưng đáng đưa vào danh
sách cần thận trọng: nếu buộc phải dùng 2 trục (ví dụ giá cổ phiếu và khối lượng giao dịch),
neo trục phụ theo quy tắc rõ ràng (ví dụ trục khối lượng luôn bắt đầu từ 0 và có chiều cao tối
đa 30% khung hình, không share cùng vùng vẽ với trục giá) thay vì để phần mềm tự động chọn
khoảng.

## 4. Annotation-first: chú giải thẳng lên hình, khi nào legend vẫn hơn

**Nguồn**: [Economist style — tổng hợp AECharts](https://medium.com/@aecharts/how-to-create-the-economist-style-charts-f2052ba6d6d3),
[Datawrapper — annotations trong bar/range/dot chart](https://www.datawrapper.de/blog/annotations-in-bar-charts),
[Datawrapper — color keys](https://www.datawrapper.de/blog/color-keys-for-data-visualizations),
BBC `rcookbook`.

### Thủ pháp

The Economist và BBC đều ưu tiên **nhãn trực tiếp** (data label đặt ngay cạnh điểm cuối đường,
hoặc trên đầu cột) thay vì legend tách rời phía dưới. Cơ chế hiệu quả: legend buộc mắt phải làm
2 việc tách rời — (1) đọc màu ở legend, (2) tìm lại đúng màu đó trên hình — mỗi lần "tra cứu
chéo" này tốn thời gian phản ứng đo được. Nhãn trực tiếp gộp 2 việc thành 1: tên chuỗi nằm ngay
tại điểm dữ liệu, mắt không cần rời khỏi vùng đang đọc.

BBC `rcookbook` và Datawrapper đều khuyến nghị cụ thể: gridline chỉ giữ NGANG (không dọc), bỏ
tick trục y, để nhãn trục y nằm ngay TRÊN gridline chính thay vì bên ngoài khung — giảm số
đường kẻ mà không giảm khả năng đọc giá trị.

### Chuyển sang bối cảnh này

Repo đã áp dụng đúng tinh thần một phần: `theme.mjs` có `categoryAxis` không gridline dọc,
`valueAxis` chỉ gridline ngang solid. Phần CHƯA áp dụng đủ: hầu hết chart trong `charts/echarts/`
vẫn dùng `legend: { bottom: 8, ... }` mặc định trong `baseOption()` thay vì nhãn trực tiếp —
điều này ĐÚNG khi có >4-5 chuỗi (xem `12-area-stack.mjs`, nhãn trực tiếp cho 5+ dải sẽ chồng
chéo), nhưng với chart 2-3 chuỗi (`05-slope.mjs`, `04-dumbbell.mjs`) nên cân nhắc thêm nhãn cuối
đường thay vì chỉ legend.

**Khi nào legend vẫn thắng annotation-first**:
1. Trên 5-6 chuỗi cùng lúc trên 1 mặt phẳng — nhãn trực tiếp sẽ chồng chéo không gỡ được.
2. Small multiples nhiều ô — đặt legend 1 lần dùng chung cho cả lưới hiệu quả hơn lặp lại nhãn
   trong từng ô nhỏ.
3. Khi người đọc cần TRA CỨU LẶP LẠI nhiều lần qua nhiều lần xem (dashboard tương tác) — legend
   cố định là điểm neo ổn định hơn nhãn di chuyển theo dữ liệu.

Mẫu chứng minh trực quan cả 2 tình huống: `chart-annotation-vs-legend.html`.

## 5. Quy ước trục và nhãn

**Nguồn**: Urban Institute style guide, Correll (Truncating Y-Axis), Solomon Messing (Cleveland
& Tufte).

- **Trục bắt đầu từ 0**: bắt buộc cho bar/column/area (đã là ràng buộc cứng ngành, khớp
  `theme.mjs`). Line/scatter được miễn nếu mục đích là biến động ngắn hạn VÀ đánh dấu rõ điểm
  gãy trục.
- **Làm tròn nhãn trục**: cả FT và Economist đều làm tròn nhãn trục về số ít chữ số có nghĩa
  (không hiển thị "1.234,5678 tỷ" trên trục) — khớp đúng cơ chế `fmtAxisLabel`/`roundSigFig`
  đã có trong `fmt.mjs`.
- **Đơn vị đặt ở đâu**: Economist/FT đặt đơn vị trong SUBTITLE (dòng phụ đề ngay dưới tiêu đề),
  không lặp lại đơn vị ở từng nhãn trục — giảm nhiễu thị giác lặp. `theme.mjs::baseOption`
  đã đúng cấu trúc này (`subtitle` riêng, `title` là phát hiện).
- **Gridline**: chỉ ngang, mảnh (~1px), KHÔNG BAO GIỜ dashed cho gridline giá trị (Economist,
  BBC đồng thuận) — khớp `valueAxis()` hiện tại.
- **Số lượng series đa chuỗi trước khi cần tách chart**: Urban Institute khuyến nghị **dưới 7
  hạng mục** cho 1 chart categorical; quá 5 nên cân nhắc gộp nhóm phụ thành "khác" hoặc tách
  thành small multiples.

## 6. Small multiples: khi nào thắng 1 chart gộp

**Nguồn**: [Solomon Messing — Cleveland và Tufte](https://solomonmg.github.io/post/visualization-series-insight-from-cleveland-and-tufte-on-plotting-numeric-data-by-groups/),
[visualizing.org — small multiples](https://www.visualizing.org/small-multiples).

Thuật ngữ có 2 gốc độc lập: Tufte gọi "small multiple" (1990), Cleveland/Becker ở Bell Labs
gọi "trellis plot" cùng thời điểm — hai nhóm hội tụ về cùng kết luận từ hai hướng khác nhau,
đáng tin cậy hơn 1 nguồn đơn lẻ.

**Khi nào thắng 1 chart gộp**: khi 1 chart overlay có >5-6 chuỗi thành "mì Ý" (spaghetti lines)
không phân biệt được đường nào là đường nào. Small multiples tách mỗi chuỗi ra 1 ô, GIỮ NGUYÊN
trục/thang giữa các ô để mắt phát hiện khác biệt bằng cách so hình dạng, không cần đọc từng số.

**Giới hạn số ô**: nguồn nhất trí "trên khoảng 20 ô thì mỗi ô quá nhỏ để đọc". Với khổ báo cáo
A4 in được (không phải màn hình cuộn vô hạn), ngưỡng thực dụng của repo này nên chặt hơn:
**6-9 ô cho khổ nửa trang, tối đa 12 ô cho khổ toàn trang ngang** — đã đúng theo cấu trúc của
`07-small-multiples.mjs` hiện có (kiểm tra: file này dùng lưới 6 ô).

**Cách đồng bộ thang**: TẤT CẢ ô phải dùng chung `min`/`max` trục y (không để mỗi ô tự động co
giãn theo dữ liệu riêng) — nếu không, hình dạng giữa các ô không còn so sánh được, phản tác
dụng của kỹ thuật này. Đây là bẫy phổ biến nhất khi implement bằng thư viện tự động scale.

**Khi nào KHÔNG dùng**: khi mục đích là "vẽ 1 con số nổi bật nhất, không phải so sánh nhiều
thực thể" — small multiples là kỹ thuật cho việc SO SÁNH, dùng sai mục đích sẽ pha loãng con số
đáng chú ý ra thành 9 ô ngang hàng.

## 7. Màu cho chuỗi nhiều thành phần: đen trắng và mù màu

**Nguồn**: [Datawrapper — colorblindness part 1](https://www.datawrapper.de/blog/colorblindness-part1),
[Datawrapper — colorblindness part 2](https://www.datawrapper.de/blog/colorblindness-part2),
Reuters Graphics colors, Urban Institute style guide.

### Thủ pháp

Datawrapper liệt kê phối màu CẦN TRÁNH cho người mù màu đỏ-lục (dạng phổ biến nhất, ~8% nam
giới): đỏ + lục + nâu; hồng + ngọc lam + xám; tím + xanh dương. **Xanh dương là hue an toàn
nhất**; cặp xanh dương + cam/đỏ hoạt động tốt qua hầu hết dạng mù màu. Nhưng phát hiện quan
trọng hơn: **hơn nửa khuyến nghị của Datawrapper KHÔNG liên quan đến việc chọn hue** — mà là
(1) nhãn trực tiếp thay legend màu, (2) hình dạng/texture/nét đứt khác nhau để mã hoá kép,
(3) "get it right in black & white" — tức là **kiểm tra bằng độ SÁNG (lightness) khác nhau đủ
rõ giữa các chuỗi**, vì mù màu về bản chất là mất khả năng phân biệt HUE nhưng vẫn phân biệt
được LIGHTNESS.

### Chuyển sang bối cảnh này

Bảng màu hiện tại của repo (`PALETTE` trong `theme.mjs`) đã đi đúng hướng: `accent` (#2251FF)
và `negative` (#C22F4E) là cặp xanh dương/đỏ-gạch — đúng dạng "an toàn cho đa số mù màu" mà
Datawrapper khuyến nghị, KHÔNG PHẢI ngẫu nhiên trùng hợp mà là hệ quả của nguyên tắc "màu theo
chiều tăng giảm" vốn đã chọn đúng 2 hue tương phản mạnh. Cái còn thiếu: chuỗi categorical có
>2 thành phần (ví dụ cơ cấu dư nợ theo 5 ngành trong `12-area-stack.mjs`) hiện dựa vào
`color: [PALETTE.accent, PALETTE.negative, PALETTE.inkLo, PALETTE.ink]` — 4 màu này KHÔNG đủ
phân biệt khi in đen trắng vì `inkLo` và `ink` gần giống nhau về hue (cùng dải xanh navy) mà
chỉ khác độ sáng, trong khi `accent` khi khử màu có độ xám tương đương `negative` (2 màu bão
hoà cao thường quy về độ xám gần nhau khi desaturate). **Khuyến nghị cụ thể**: với chart có ≥3
chuỗi categorical cần phân biệt cả ở bản in đen trắng, bổ sung mã hoá kép bằng
`itemStyle.borderType` (nét liền/đứt/chấm) hoặc pattern lấp đầy, KHÔNG chỉ dựa vào hex màu.
Chứng minh thực nghiệm (không chỉ khẳng định suông) trong mẫu `chart-mau-den-trang.html`: cùng
1 bộ dữ liệu render 2 lần, 1 lần màu và 1 lần `filter: grayscale(1)`, đặt cạnh nhau.

**Khi nào KHÔNG cần lo đen trắng**: báo cáo chỉ phát hành bản HTML/PDF màn hình, không bao giờ
in — nhưng vì repo này định vị "HTML self-contained VÀ PDF in được", mặc định nên coi bản in
đen trắng là kịch bản PHẢI qua được, không phải edge case.

## 8. Chart cho bối cảnh tài chính riêng

### Đã có trong repo, không cần làm lại — chỉ ghi nhận khớp doctrine

- **Waterfall** (`01-waterfall.mjs`): đúng quy ước sell-side (subtotal khác màu delta, trục từ
  0). Khớp doctrine FT "part-to-whole/flow".
- **Bullet** (`03-bullet.mjs`): đúng spec gốc Stephen Few — dải định tính bằng ĐỘ SÁNG của 1
  hue (không phải nhiều hue), target là VẠCH không phải thanh. Đây chính là điều
  [bản spec gốc](https://www.perceptualedge.com/articles/misc/Bullet_Graph_Design_Spec.pdf)
  yêu cầu, repo đã làm đúng.
- **Tornado** (`06-tornado.mjs`): đúng quy ước sắp theo biên độ giảm dần ("hình phễu"), và đã tự
  ghi chú đúng bẫy màu valence mà `ibinterviewquestions.com` cũng cảnh báo (đừng lẫn "kịch bản
  lạc quan" với "màu dương = tốt").
- **Candlestick** (`09-candlestick.mjs`): với thị trường VN, đỏ=giảm/xanh=tăng là chuẩn đang
  dùng (khớp HOSE/HNX thực tế), giữ nguyên, nhưng nên đảm bảo có thêm mã hoá không-màu (ví dụ
  viền nét đứt cho nến giảm) nếu chart này cần in đen trắng — cần kiểm tra riêng vì nghiên cứu
  quốc tế ghi nhận quy ước đỏ/xanh KHÔNG thống nhất toàn cầu (một số thị trường Đông Á đảo
  ngược), nên KHÔNG dựa 100% vào màu khi chart phải tự thân đủ nghĩa (đọc bằng vị trí thân nến
  so với bấc, không chỉ màu).

### Chưa có trong repo, nên thêm

- **Football field (dải định giá)**: chart chuẩn sell-side để tổng hợp nhiều phương pháp định
  giá (DCF, EV/EBITDA comps, giao dịch tiền lệ, biên độ 52 tuần) thành các thanh ngang dạng
  dải min-max, cộng 1 vạch dọc = giá thị trường hiện tại.
  [Nguồn: Wall Street Prep](https://www.wallstreetprep.com/knowledge/football-field-valuation-real-example-excel-template/),
  [Macabacus](https://macabacus.com/blog/build-football-field-chart-excel). Sức mạnh của chart
  này nằm ở **vùng hội tụ** (nơi nhiều dải chồng lên nhau = độ tin cậy cao nhất của định giá) —
  đây là annotation-first tự nhiên (đánh dấu vùng hội tụ bằng dải nền, không cần legend vì mỗi
  thanh đã có nhãn phương pháp ngay cạnh). Chưa có `.mjs` nào trong repo làm loại này — đề xuất
  vào `theme.mjs` (xem mục 9). Mẫu: `chart-football-field-dinh-gia.html`.
- **Lưới độ nhạy 2 chiều (2-way sensitivity grid)**: khác tornado (tornado là 1 biến/1 trục),
  lưới độ nhạy là bảng nhiệt N×M cho 2 biến đồng thời (ví dụ WACC × tăng trưởng dài hạn ra
  giá trị doanh nghiệp) — chuẩn phổ biến trong phụ lục mô hình DCF. Repo có `08-heatmap.mjs`
  nhưng đó là heatmap categorical (ma trận tương quan/hoạt động), khác về mục đích và cách đọc
  (lưới độ nhạy LUÔN có 1 ô "base case" cần đánh dấu viền riêng, heatmap thường thì không). Mẫu:
  `chart-luoi-do-nhay-hai-chieu.html`.

## 9. Đề xuất cụ thể cho `theme.mjs` (ECharts) và tầng matplotlib

### Nên vào `theme.mjs` làm preset mới

1. **`footballFieldSeries()` helper**: thanh ngang dạng `custom series` vẽ dải [low, high] +
   nhãn phương pháp bên trái + giá trị 2 đầu ngay trên dải (annotation-first, không legend).
   Lý do vào ECharts chứ không phải matplotlib: các báo cáo định giá trong repo hiện xuất bản
   dạng HTML tương tác trước, PDF sau — và dải hội tụ hưởng lợi từ tooltip hover khi xem màn
   hình.
2. **Sensitivity grid heat table**: mở rộng `PALETTE.bandLo/Mid/Hi` (đã có, dùng cho bullet)
   thành thang liên tục 5-7 bậc cùng 1 hue (không diverging 2 hue, giữ đúng "không traffic-
   light" dù đây là magnitude field chứ không phải delta/so sánh) + cơ chế đánh dấu 1 ô base
   case bằng viền `ink` dày hơn thay vì đổi màu ô.
3. **`directLabelSeries` helper cho slope/dumbbell**: nhãn tên chuỗi ngay tại điểm cuối đường,
   dùng thay `legend` mặc định khi số chuỗi ≤4 — hiện `baseOption()` luôn bật `legend`, nên
   tách thành 2 lựa chọn rõ ràng (`withLegend: true/false`) thay vì ngầm định luôn có legend.

### Nên ở tầng matplotlib (`_eir_style.py` / `viz_eir*.py`)

1. **Bản PDF tĩnh của football field**: dùng `barh` với `xerr` không hợp (football field không
   phải error bar đối xứng quanh 1 điểm, mà là dải min-max bất đối xứng) — cần 1 hàm
   `draw_range_bar(ax, low, high, y, label)` riêng, vẽ bằng `Rectangle` ngang. Đặt ở matplotlib
   vì football field trong PDF gửi khách (research note tĩnh) phổ biến hơn bản tương tác.
2. **Sensitivity grid dạng bảng số + tô nền**: PDF/DOCX cần bảng có SỐ THẬT trong từng ô (không
   chỉ màu), nên đây hợp với `viz_eir_stats.py` (đã có hạ tầng vẽ bảng số) hơn là ECharts
   heatmap thuần hiển thị màu.

### Chỉ hợp bản màn hình, KHÔNG đưa vào PDF tĩnh

1. **Hover tooltip trên vùng hội tụ football field**: giá trị gia tăng của tooltip (xem chi
   tiết từng phương pháp khi rê chuột) biến mất hoàn toàn trên giấy — bản PDF PHẢI tự thân đủ
   thông tin (nhãn trực tiếp toàn bộ), không được dựa vào tương tác để bù thông tin thiếu.
2. **Bất kỳ khuyến nghị "disable legend, dùng hover để phân biệt màu" nào** (một số ví dụ
   Datawrapper dùng hover làm phương án phân biệt màu bổ sung) — bản in không có hover, nên nếu
   dùng cách này cho bản màn hình thì bản PDF của CÙNG chart phải tự động chuyển về nhãn trực
   tiếp, không được là 1 chart chỉ đọc được trên màn hình.

## 10. Tổng kết: cái gì là RÀNG BUỘC, cái gì là Ý THAM KHẢO trong tài liệu này

Toàn bộ nội dung §2 đến §9 là ý tham khảo. Không mục nào ở trên tạo thêm ràng buộc cứng mới
ngoài danh sách đã có ở `CLAUDE.md`. Cụ thể:
- Ngữ pháp chọn chart (§2): gợi ý điểm khởi đầu, không cấm chọn ngược lại nếu ngữ cảnh cần.
- Danh sách đen mở rộng (§3, pie/dual-axis): KHÔNG cấm cứng như gauge/radar — là khuyến nghị có
  ngưỡng cụ thể ("≤3 lát"), người viết báo cáo được quyền vượt ngưỡng nếu có lý do.
- Mọi con số ngưỡng (số ô small multiples, số chuỗi trước khi tách chart...) là **kinh nghiệm
  đúc kết từ nguồn**, không phải luật vật lý — điều chỉnh theo khổ giấy/độ phức tạp thật của
  từng báo cáo.
