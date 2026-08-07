# Nhóm A (chart) và nhóm B (component) còn thiếu gì, xếp theo nhu cầu đo được

Câu hỏi: thư viện chart và component hiện có đủ dựng một báo cáo tài chính hoàn chỉnh chưa, và
nếu bổ sung thì bổ sung cái gì trước.

Khác với `03-chart-doctrine/CHART-SELECTION.md` (bảng tra chọn chart theo câu hỏi người đọc, có
ghi chỗ "chưa có" nhưng không xếp hạng), hồ sơ này trả lời câu **thứ tự làm**, và xếp hạng bằng
số chứ không bằng cảm tính.

## Phương pháp và nguồn

Bốn nguồn nội bộ, một nguồn ngoài:

1. `_harvest/lab-opvia/.../archetypes/` gồm 10 loại báo cáo, mỗi loại có README liệt kê chart
   family cần dùng. Đếm một chart xuất hiện ở bao nhiêu trên 10 loại thì ra **nhu cầu**.
2. `charts/echarts/` 12 preset và `charts/matplotlib/` 48 component EIR: ra **phủ**.
3. `components/catalog/` 24 spec: phủ nhóm B.
4. `_harvest/harvest-extras/thinktank/` 66 file domain: kiểm chéo nhu cầu bằng tần suất nhắc
   trong nội dung phân tích thật.
5. Web, để xác nhận chuẩn ngành sell-side không lệch với hai nguồn trên.

Giới hạn phải nói trước: nguồn 1 là bộ tài liệu của một hệ khác được harvest về, nó phản ánh
thực hành sell-side nói chung chứ không phải quy ước riêng của repo này. Dùng nó để **xếp thứ
tự**, không dùng để ép danh mục.

## Hiện trạng bằng số

| Tầng | Số lượng | Ghi chú |
|---|---|---|
| A1 chart ECharts, cho HTML tương tác | 12 preset | waterfall, sankey, bullet, dumbbell, slope, tornado, small-multiples, heatmap, candlestick, treemap, stacked-100, area-stack |
| A2 chart matplotlib EIR, cho PDF tĩnh | 48 component | phủ rộng, gồm cả nhóm kể chuyện như executive_summary, scenario_cards |
| B component kể chuyện HTML | 24 spec | |

Đối chiếu hai engine của nhóm A: **43 trong 48 loại của matplotlib không có bản ECharts**, và 7
loại của ECharts không có bản matplotlib.

## Phát hiện 1: lỗ hổng không nằm ở "ít chart", nằm ở LỆCH ENGINE

Đây là phát hiện chính, và nó đảo ngược ấn tượng ban đầu.

Đếm nhu cầu trên 10 loại báo cáo rồi đối chiếu phủ:

| Nhu cầu | Số loại báo cáo cần | PDF (matplotlib) | HTML (ECharts) |
|---|---|---|---|
| Hộp tóm tắt điều hành | 10/10 | có | không |
| Thẻ kịch bản | 8/10 | có | **không** |
| Line có chú thích | 8/10 | có | **không** |
| Bar ngang xếp hạng | 7/10 | có | **không** |
| Slopegraph | 7/10 | **không** | có |
| Sơ đồ cơ chế | 7/10 | có | **không** |
| Scatter phần tư | 7/10 | có | **không** |
| Sankey | 6/10 | có | có |
| Cầu nối dòng | 6/10 | có | có |
| Dòng thời gian tiến trình | 6/10 | có | **không** |
| Waterfall | 6/10 | gần đúng | có |
| Dot plot phân phối | 5/10 | có | **không** |
| Small multiples | 5/10 | **không** | có |

Đọc bảng theo cột: bản PDF phủ gần hết, bản HTML thủng đúng ở những dòng trên cùng, tức những
thứ dùng nhiều nhất. Trong khi đó ECharts lại có sẵn treemap (2/10) và candlestick (1/10), là
những loại ít dùng hơn hẳn.

Nói cách khác, 12 preset ECharts hiện tại **không phải một tập con hợp lý của 48 component
matplotlib**, mà là một tập chọn theo độ thú vị kỹ thuật. Cái rẻ nhất để làm (line, bar ngang,
scatter) lại là cái thiếu.

## Phát hiện 2: hai loại chart tài chính chuyên biệt vắng ở CẢ HAI engine

`yield curve` và `forward curve` (đường cong lãi suất, đường cong giá kỳ hạn) không có ở
matplotlib, không có ở ECharts, và không có dòng nào trong `CHART-SELECTION.md`.

Chúng không phải nhu cầu tưởng tượng: trong 66 file domain của ThinkTank, `yield curve` được
nhắc **50 lần** và `contango` **25 lần**, và có hẳn hai file dày dành riêng cho chúng
(`domain-fi-yield-curve-vn.md` 16KB, `domain-commodities-futures-curve.md` 14KB). Tức nội dung
phân tích đã có sẵn trong kho, chỉ thiếu cách vẽ.

Với thị trường Việt Nam, đường cong lãi suất còn là chart nền của mọi báo cáo trái phiếu và
mọi bài về chính sách tiền tệ.

## Phát hiện 3: một nhu cầu 4/10 đang bị luật cứng chặn, chưa có phương án thay chính thức

`risk_radar` xuất hiện ở 4 trên 10 loại báo cáo, nhưng repo **cấm radar** (trục không độc lập
nên diện tích vô nghĩa) và **cấm gauge**. Lệnh cấm đúng và không nên gỡ.

Vấn đề là cấm mà không chỉ đường thay thì người dùng thư viện sẽ tự chế. Repo đã nghiên cứu sẵn
lời giải ở `research/03-chart-doctrine` và mẫu `samples/chart-radar-vs-cleveland.html`, nhưng
lời giải đó chưa được nâng thành preset có tên trong `charts/`.

Đề xuất chốt thành quy ước: **hồ sơ rủi ro nhiều tiêu chí vẽ bằng Cleveland dot plot xếp hạng**,
mỗi tiêu chí một hàng, thang điểm chung, mốc tham chiếu là một vạch dọc.

## Phát hiện 4: nhóm B thủng đúng chỗ dùng nhiều nhất

Hộp tóm tắt điều hành là thứ **10 trên 10** loại báo cáo đều cần, tức thành phần phổ quát nhất
trong toàn bộ khảo sát. Nhóm B hiện có `11-exec-qa` (bốn câu hỏi hội đồng quản trị) và
`24-key-point-callout` (một câu kết luận), cả hai đều gần nhưng không phải cùng một thứ: cái
đang thiếu là khối bốn ô cố định Luận điểm / Chất xúc tác / Rủi ro / Hành động, đặt cuối bài.

Thẻ kịch bản (8/10) có bản matplotlib nhưng không có bản HTML, trong khi đây là thành phần
người đọc hay bấm vào nhất ở bản tương tác.

Ba thứ nhỏ hơn cũng vắng: dải thắng thua (winners/losers split), ngã ba chính sách (policy
fork), và dải tự sự chen giữa chart (narrative strip).

## Việc nên làm, xếp theo thứ tự

**P0, làm trước, vì rẻ và chặn nhiều báo cáo nhất.** Bốn preset ECharts, mỗi cái dựng được từ
nền `theme.mjs` sẵn có, không cần thư viện mới:

| Preset | Nhu cầu | Dựng từ |
|---|---|---|
| `13-line-annotated.mjs` | 8/10 | `12-area-stack.mjs` bỏ phần stack, thêm lớp `markPoint`/`markLine` |
| `14-bar-ranking.mjs` | 7/10 | `06-tornado.mjs` giữ một phía, sắp giảm dần, có biến thể dot plot |
| `15-quadrant-scatter.mjs` | 7/10 | `04-dumbbell.mjs` phần scatter, thêm hai đường chia phần tư |
| `16-dot-distribution.mjs` | 5/10 | như trên, thêm jitter và vạch trung vị |

Cộng hai chart chuẩn ngành mà chính ledger đã ghi là còn nợ, hiện mới có mẫu HTML vẽ tay:
football field và lưới độ nhạy hai chiều.

**P1, làm sau, giá trị cao nhưng tốn công hơn.**

- Đường cong lãi suất và đường cong giá kỳ hạn, cả hai engine. Cần quy ước riêng cho trục kỳ
  hạn (không đều nhau: 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y) và cho việc vẽ nhiều thời điểm chồng nhau.
- Thẻ kịch bản bản HTML, và hộp tóm tắt điều hành cho nhóm B.
- Preset dot plot rủi ro, thay cho radar bị cấm.

**P2, để sau cùng.** Bù đối xứng cho matplotlib: slopegraph, small multiples, treemap. Ba cái
này matplotlib đang thiếu nhưng bản ECharts đã có, nên bản PDF vẫn dựng được bằng cách khác.

## Việc KHÔNG nên làm

- Đừng gỡ lệnh cấm pie, donut nhiều lát, gauge, radar để "phủ cho đủ" danh mục của nguồn
  harvest. Nguồn đó liệt kê cả `gauge` và `risk_radar`, repo cố ý không theo.
- Đừng thêm preset chỉ vì matplotlib có mà ECharts chưa. Bảng nhu cầu ở trên cho thấy nhiều
  loại chỉ cần một engine, ví dụ dòng thời gian và sơ đồ cơ chế hợp bản in tĩnh hơn.
- Đừng chép bảng màu của nguồn harvest. Bộ Opvia dùng Prussian Blue `#003366` và Aged Brass
  `#8B7355`, khác hệ trắng lạnh `#051C2C` cộng `#2251FF` mà repo đã phân xử bằng ba nguồn độc
  lập. Lấy cấu trúc, bỏ màu.

## Nguồn ngoài

- [Football Field Valuation Chart guide](https://ctacquisitions.com/football-field-valuation-chart-guide/)
- [Equity Research Report format và thành phần](https://www.wallstreetprep.com/knowledge/sample-equity-research-report/)
- [Equity Research Report, CFI](https://corporatefinanceinstitute.com/resources/valuation/equity-research-report/)
