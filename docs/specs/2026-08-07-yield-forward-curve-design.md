# Đường cong lãi suất và đường cong giá kỳ hạn: đặc tả thi công

Ngày chốt: 2026-08-07
Trạng thái: đặc tả, chưa viết code. Repo hiện KHÔNG có chart nào trong hai họ này ở cả matplotlib (`charts/matplotlib/`) lẫn ECharts (`charts/echarts/`), đã xác nhận bằng tìm kiếm trực tiếp trong hai thư mục.

Phạm vi: họ A (đường cong lãi suất và biến thể: theo thời điểm, chênh lệch kỳ hạn 2s10s, butterfly, z-spread, đường cong tín dụng theo hạng) và họ B (đường cong giá kỳ hạn: contango/backwardation, dịch chuyển qua thời gian, roll yield). Đây là chart nền cho báo cáo trái phiếu, chính sách tiền tệ, và hàng hoá, nên đặc tả này ưu tiên tính DÙNG LẠI ĐƯỢC cho nhiều bài viết hơn là tối ưu cho một bài cụ thể.

---

## 0. Bảng quyết định (đọc lướt)

| Câu hỏi | Quyết định | Vì sao (chi tiết ở mục tương ứng) |
|---|---|---|
| Trục kỳ hạn | Trục HẠNG MỤC (category, cách đều theo thứ tự), KHÔNG dùng trục tuyến tính theo năm | Tuyến tính theo năm nén hết vùng 1Y-10Y (vùng có tín hiệu chính sách) vào 1/3 bề rộng, dồn 2/3 còn lại cho vùng 15Y-30Y gần như không đọc. Xem §1 |
| Trục giá trị (trục y) | KHÔNG bắt đầu từ 0, tự co theo khoảng dữ liệu | Ràng buộc "trục không từ 0" trong `CHART-SELECTION.md` là luật cho BAR (độ dài mã hoá độ lớn), không áp cho LINE (vị trí đã mã hoá giá trị). `c_spread`, `c_index100`, `c_fan` sẵn có trong `viz_eir.py` cũng không zero-anchor. Zero-anchor một trục lợi suất 2-6% sẽ nén phẳng đúng cái hình dạng chart cần cho thấy |
| Nhiều thời điểm chồng nhau | Tối đa 3 đường/1 chart, phân biệt bằng ĐỘ ĐẬM NÉT + KIỂU NÉT (liền/đứt/chấm), không chỉ bằng màu | Sống được khi in đen trắng, xem §2 |
| Đảo ngược đường cong | Tô đoạn cong bị đảo ngược bằng `negative`, kèm badge số bps; chênh lệch kỳ hạn (2s10s) vẽ THÊM một chart riêng dạng diff/spread theo thời gian, tái dùng `c_spread` sẵn có | Đây là 1 trong 2 trường hợp hợp lệ để dùng màu valence theo đúng luật đã ghi trong `theme.mjs`: "dùng negative nếu một bên BẤT LỢI trong phép so sánh đó". Đảo ngược = cảnh báo suy thoái, không phải delta trung tính. Xem §3 |
| Butterfly | Vẽ DÂY CUNG tham chiếu nối 2 cánh trên chính chart hình dạng đường cong, cộng 1 chart giá trị theo thời gian dùng LẠI khung `spread` nhưng TẮT tô màu theo dấu | Dấu của butterfly không mang nghĩa phổ quát tốt/xấu như 2s10s, tô teal/brick sẽ là traffic-light giả. Xem §3.3 |
| Contango/backwardation | Đường giá kỳ hạn + 1 đường ngang tham chiếu giá giao ngay + badge chữ trung tính (không tô màu valence) | Contango không phải lúc nào cũng "xấu"; đọc bằng ĐỘ DỐC so với đường spot, không phải bằng màu. Xem §4 |
| Z-spread thật, đường cong tín dụng theo hạng thật | KHÔNG làm cho VN, thay bằng 2 biến thể rút gọn có căn cứ dữ liệu | VN không có benchmark liên tục để giải Z-spread lặp, không có hệ xếp hạng tín nhiệm chuẩn. Xem §6 |
| Kỳ hạn thưa dữ liệu | 3 cấp: chấm đặc/nét liền (quan sát được) · chấm rỗng/nét đứt (ước tính dealer) · bỏ hẳn điểm (không tồn tại trong kỳ đó) | Xem §5 |
| Engine | matplotlib: module mới `viz_eir_curves.py`, đăng ký vào `_MODULES` trong `viz_super.py:42`. ECharts: 3 file mới `13-yield-curve.mjs`, `14-term-spread.mjs`, `15-futures-curve.mjs` | Xem §7, §8 |

---

## 1. Trục kỳ hạn: câu hỏi quan trọng nhất

### 1.1 Ba phương án và phép đo méo hình dạng

Kỳ hạn TPCP không cách đều: 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y (VN hầu như không có 1M/3M/6M ở lớp trái phiếu chính phủ giao dịch thứ cấp, xem §5). Có 3 cách đặt trục hoành:

**(a) Tuyến tính theo năm thực** (1, 2, 3, 5, 7, 10, 15, 20 đặt đúng vị trí số học). Đúng về mặt toán học nhưng gây méo ngược: nếu khổ chart rộng 700px, đoạn 1Y-10Y (vùng có toàn bộ tín hiệu chính sách tiền tệ, chu kỳ tín dụng, on-the-run/off-the-run theo `domain-fi-yield-curve-vn.md`) chỉ chiếm ~1/3 bề rộng, còn đoạn 10Y-20Y (vùng thanh khoản thấp nhất, theo bảng thanh khoản trong domain doc chỉ có bảo hiểm nhân thọ mua giữ đến đáo hạn) chiếm 1/3 còn lại một cách không tương xứng với tầm quan trọng phân tích.

**(b) Trục hạng mục** (category, mỗi kỳ hạn cách đều nhau bất kể khoảng năm thực). Đây là quy ước mà hầu hết chart lợi suất xuất bản (FT, Bloomberg IYC, trang lãi suất của FRED) đang dùng. Cái giá phải trả: độ dốc hình học giữa 2 điểm không còn tỷ lệ với bps/năm thật.

Đo cụ thể bằng ví dụ số (dùng đúng khung dao động trong `domain-fi-yield-curve-vn.md` §1.2, không phải số đóng cửa 1 ngày thật):

- Đoạn 1Y (2,85%) sang 2Y (2,95%): chênh 10bps trong 1 năm thực → độ dốc thật **10 bps/năm**.
- Đoạn 15Y (3,70%) sang 20Y giả định (3,85%): chênh 15bps trong 5 năm thực → độ dốc thật **3 bps/năm**.

Trên trục hạng mục, hai đoạn này được vẽ với **bề rộng ngang bằng nhau** (mỗi đoạn = 1 khoảng cách hạng mục), nên đoạn 15Y-20Y (thực chất thoải hơn 3 lần) sẽ trông dốc gần tương đương đoạn 1Y-2Y nếu delta lợi suất hiển thị tương đương. Đây chính là méo hình dạng cần cảnh báo.

**(c) Trục log theo năm.** Trung dung giữa (a) và (b): giãn vùng ngắn hạn hơn (a) nhưng không đều tuyệt đối như (b).

### 1.2 Quyết định: trục hạng mục là mặc định, không dùng log, không dùng tuyến tính

Chọn **(b) trục hạng mục** làm mặc định cho cả hai họ chart, vì ba lý do cộng dồn:

1. **Độ phân giải thị giác đi đúng chỗ có thông tin.** Với TPCP VN, vùng 1Y-10Y là vùng phân tích chính (chu kỳ tín dụng, phản ứng NHNN, on-the-run rotation), vùng 15Y-30Y gần như chỉ có 1 nhóm mua (bảo hiểm nhân thọ) và thanh khoản rất thấp theo chính domain doc. Trục hạng mục cho vùng có tín hiệu nhiều không gian ngang hơn hẳn so với trục tuyến tính.
2. **Đây là quy ước người đọc đã quen.** Báo cáo broker VN (Vietcap, ACBS, SSI) khi vẽ đường cong lợi suất đều dùng nhãn kỳ hạn rời rạc cách đều, không dùng trục năm liên tục. Đổi quy ước sẽ làm người đọc mất thời gian giải mã thay vì đọc ngay hình dạng.
3. **Trục log là chi phí học thêm không cần thiết cho VN.** Trục log hợp lý khi 1 chart phải trải dài từ qua đêm/1 tuần (thị trường tiền tệ) tới 30 năm (trái phiếu), như một số chart lãi suất toàn cầu kết hợp OMO + bond. VN không có điểm kỳ hạn ngắn thanh khoản đủ để cần việc đó (xem §5: kỳ hạn ngắn nhất có ý nghĩa phân tích ở TPCP VN là 1Y). Thêm trục log vào một curve chỉ trải 1Y-20Y là thêm độ khó đọc không đổi lại được gì.

**Ràng buộc đi kèm quyết định này (bắt buộc, không phải khuyến nghị):**

- KHÔNG BAO GIỜ dùng slope trên chart để so sánh bps/năm giữa hai đoạn có khoảng năm thực khác nhau. Mọi chart theo họ này phải đi kèm bảng số liệu (hairline data table, xem `components/catalog/12-hairline-data-table.md`) để người đọc lấy con số thật nếu cần tính toán, không được suy ra từ mắt nhìn hình học.
- KHÔNG chồng 2 đường cong có TẬP HỢP kỳ hạn báo cáo khác nhau lên cùng 1 trục hạng mục (ví dụ 1 đường có 8 điểm, đường kia chỉ có 5 điểm) mà không xử lý union kỳ hạn trước. Nếu không, vị trí hạng mục thứ 3 của đường A và đường B có thể ứng với 2 kỳ hạn thực khác nhau, làm sai lệch so sánh trực tiếp. Cách xử lý: hợp nhất tập kỳ hạn của tất cả các snapshot đưa vào cùng 1 chart, kỳ hạn nào 1 snapshot không có dữ liệu thì bỏ điểm đó (không nội suy ngầm), xem §5.

---

## 2. Nhiều thời điểm chồng nhau, đọc được khi in đen trắng

Trần tối đa 3 đường/1 chart (hôm nay, 1 tháng trước, 1 năm trước là bộ ba chuẩn cho báo cáo định kỳ). Quá 3 đường chuyển sang small multiples (`07-small-multiples.mjs` đã có sẵn khung dùng lại được, mỗi ô 1 thời điểm, trục y đồng bộ).

Phân biệt 3 đường bằng **3 tầng, không chỉ dựa vào màu** vì màu không sống được khi in đen trắng hoặc photocopy:

| Thời điểm | Độ đậm nét | Kiểu nét | Marker | Sắc độ (nếu có màu) |
|---|---|---|---|---|
| Hôm nay | Đậm nhất (2,4-2,8pt) | Liền | Đặc, kích thước lớn nhất | `accent` nguyên bản |
| 1 tháng trước | Trung bình (1,8pt) | Đứt vừa `(0, (5, 2))` | Đặc, nhỏ hơn | `accent` pha nhạt ~35% về `paper` (dùng `tint(accent, 0.65)` phía matplotlib, hoặc `PALETTE.accentSoft` có sẵn phía ECharts) |
| 1 năm trước | Mảnh nhất (1,4pt) | Chấm `(0, (1, 2))` | Rỗng (hollow) | `inkLo`/`FAINT`, không dùng accent nữa |

Lý do xếp theo thứ tự "càng xa hiện tại càng mảnh, càng đứt, càng rỗng, càng nhạt": đây là 4 kênh tương phản đều SỐNG được qua chuyển đổi sang thang xám (độ đậm nét và độ đặc/rỗng của marker là hình học, không phải màu), trong khi nếu chỉ tách 3 đường bằng 3 hue khác nhau thì khi in đen trắng chúng suy biến về cùng 1 mức xám và không phân biệt được nữa.

Nhãn trực tiếp cuối đường (theo đúng lối `c_index100`/`04-dumbbell.mjs` đã dùng trong repo, không dùng legend box), đặt ở đầu phải chart, có thể đặt lệch dọc nếu 2 đường gần chạm nhau ở điểm cuối.

Marker rỗng còn có vai trò kép: nó cũng là ký hiệu "kỳ hạn thưa dữ liệu, ước tính" ở §5. Khi cả hai điều kiện trùng nhau (ví dụ điểm 1 năm trước ở kỳ hạn 20Y vừa là đường cũ vừa là kỳ hạn thưa), không cần chồng thêm ký hiệu, marker rỗng đã tự nhiên đúng cho cả 2 lý do.

---

## 3. Đảo ngược đường cong, chênh lệch kỳ hạn (2s10s), và butterfly

### 3.1 Trên chính chart hình dạng đường cong

Khi một đoạn nối 2 kỳ hạn liền kề có độ dốc âm (kỳ hạn dài hơn nhưng lợi suất thấp hơn), tô đoạn đó bằng `negative` thay vì màu đường bình thường, và gắn badge nhỏ dạng "▼ đảo ngược 2Y-10Y: -18bps" neo cạnh đoạn đó (dùng lại `_badge()` đã có trong `_eir_style.py`, nền `NAVY`/`ink`, không dùng nền đỏ để badge không cạnh tranh với đoạn line đã tô đỏ).

Đây là 1 trong 2 trường hợp được phép dùng cặp màu valence `positive`/`negative` theo đúng chữ trong `charts/echarts/theme.mjs`: *"để TRUNG TÍNH, hoặc dùng negative nếu một bên BẤT LỢI trong phép so sánh đó"*. Đảo ngược đường cong là tín hiệu cảnh báo suy thoái/thắt chặt được thừa nhận rộng rãi trong phân tích vĩ mô, không phải một delta trung tính kiểu "tăng/giảm theo thời gian" mà theme.mjs cấm gán valence, nên gán `negative` ở đây đúng luật chứ không phải ngoại lệ phá luật.

**Không** tô cả 1 vùng area dưới đoạn đảo ngược (dễ nhầm với ngữ nghĩa "area chart = tích luỹ" đã dùng cho stacked/area khác trong repo). Chỉ tô đoạn LINE và marker.

### 3.2 Chart riêng: chênh lệch kỳ hạn theo thời gian (2s10s)

Term spread (ví dụ 10Y-2Y) là một scalar mỗi ngày, cần một chart THEO THỜI GIAN riêng biệt, không lồng vào chart hình dạng đường cong. Đây chính là use case của component `spread` đã có sẵn trong `charts/matplotlib/viz_eir.py::c_spread` (nhánh `if p.get("diff")`), tô `TEAL` phía trên 0, `BRICK` phía dưới 0, đường 0 vẽ đậm làm ngưỡng đảo ngược. **Dùng lại nguyên component này cho 2s10s, không viết hàm mới ở matplotlib.**

Phía ECharts hiện chưa có tương đương; đặc tả ở §8.2 (`14-term-spread.mjs`).

### 3.3 Butterfly: vì sao KHÔNG dùng chung ngữ nghĩa màu với 2s10s

Butterfly = 2 × lợi suất bụng − lợi suất cánh ngắn − lợi suất cánh dài (ví dụ 2 × 5Y − 2Y − 10Y). Khác 2s10s ở một điểm quan trọng: dấu của butterfly KHÔNG mang nghĩa phổ quát tốt/xấu như dấu của term spread (âm = đảo ngược = cảnh báo suy thoái). Một butterfly dương hay âm đều có thể là trạng thái bình thường tuỳ hình dạng đường cong hiện tại; gán `TEAL`/`BRICK` theo dấu ở đây sẽ là traffic-light giả đúng như cảnh báo trong chính comment của `theme.mjs`.

Quyết định: butterfly dùng **2 cách trình bày**, cả hai đều KHÔNG tô theo dấu:

1. **Trên chart hình dạng đường cong**: vẽ 1 dây cung tham chiếu (đường thẳng mảnh, nét đứt, màu `FAINT`/`inkLo`) nối trực tiếp 2 điểm cánh (ví dụ 2Y và 10Y). Khoảng cách thị giác giữa điểm bụng thật (5Y) và dây cung đó CHÍNH LÀ độ phồng butterfly, người đọc thấy ngay tại vị trí nào trên đường cong mà không cần đọc số trước.
2. **Chart giá trị theo thời gian**: dùng lại khung `spread` nhưng thêm cờ mới `zero_is_signal: false` để tắt tô teal/brick theo dấu, khi đó chỉ vẽ 1 đường `accent` liền, không area fill theo dấu (giữ area fill nhẹ 1 màu nếu muốn, nhưng không chia 2 màu qua trục 0).

Cờ `zero_is_signal` mặc định `true` (giữ nguyên hành vi hiện tại của `c_spread`, không phá bất kỳ `spec.json` nào đang gọi component này), chỉ đặt `false` khi vẽ butterfly hoặc bất kỳ spread nào không có ngưỡng 0 mang nghĩa cảnh báo.

---

## 4. Contango và backwardation: đọc chiều dốc ngay không cần thuật ngữ

Theo `domain-commodities-futures-curve.md` §1: contango = giá hợp đồng xa hơn cao hơn giá giao ngay (dốc lên), backwardation = ngược lại (dốc xuống). Ba lớp giúp người đọc không cần nhớ thuật ngữ:

1. **Đường tham chiếu ngang tại giá giao ngay** (spot), vẽ nét đứt mảnh màu `inkLo`, xuyên suốt chiều rộng chart. Đường cong futures nằm HẲN TRÊN đường này ở mọi điểm là contango rõ ràng, nằm HẲN DƯỚI là backwardation rõ ràng, cắt qua là hỗn hợp (gần front-month backwardation, xa hơn chuyển contango, hoặc ngược lại, một hình dạng có thật và đáng ghi chú riêng).
2. **Badge chữ trung tính** (nền `NAVY`, không phải `positive`/`negative`) ghi thẳng "CONTANGO" hoặc "BACKWARDATION" neo gần đoạn đường rõ nhất, dùng lại `_badge()`. Không tô màu valence cho badge này: contango không phải lúc nào cũng bất lợi (nó phản ánh tồn kho dồi dào, một trạng thái thị trường bình thường), backwardation không phải lúc nào cũng có lợi. Gán xanh/đỏ ở đây sẽ đúng là kiểu traffic-light mà `theme.mjs` cấm cho "nhận định so sánh không phải delta thời gian".
3. **Chú thích roll yield** dưới badge, 1 dòng: dấu và độ lớn suy trực tiếp từ hình dạng curve theo đúng cơ chế trong `domain-commodities-futures-curve.md` §2 (contango → roll âm, backwardation → roll dương). Ví dụ: "Roll yield ước tính khoảng -2,1%/năm nếu nắm giữ hợp đồng gần liên tục."

### 4.1 Dịch chuyển đường cong futures qua thời gian

Dùng lại đúng khung đa-thời-điểm ở §2 (đậm nét/kiểu nét/marker phân tầng theo thời gian), điểm khác biệt duy nhất so với yield curve: trục hoành ở đây là tháng hợp đồng (M1, M2, ..., M12), vốn CÁCH ĐỀU tương đối trong thời gian thực (mỗi hợp đồng cách nhau ~1 tháng lịch), nên trục hạng mục ở đây không tạo ra méo hình dạng đáng kể như ở yield curve, đây gần như "miễn phí" chứ không phải một đánh đổi. Ngoại lệ: nếu chuỗi hợp đồng bỏ qua một số tháng (không có open interest, thường gặp ở hợp đồng năm xa với hàng hoá mỏng thanh khoản như cà phê Robusta ICE), áp đúng quy tắc kỳ hạn thưa ở §5 (chấm rỗng, đoạn nối đứt nét) cho các tháng đó thay vì nối liền ngầm định như thể có báo giá thật.

### 4.2 VN không có thị trường futures nội địa: phạm vi áp dụng thực tế

Theo `domain-commodities-futures-curve.md` §5.1, VN không có futures market nội địa sâu. Chart họ B trong báo cáo VN dùng để trực quan hoá đường cong hàng hoá QUỐC TẾ có ảnh hưởng tới doanh nghiệp VN qua kênh giá đầu vào/margin (WTI, Brent cho GAS/PVD/PVS/BSR; vàng cho PNJ; cà phê Robusta ICE cho margin xuất khẩu HAG), không áp dụng cho một "đường cong hàng hoá nội địa VN" vì đối tượng đó không tồn tại. Ghi rõ điều này trong `asof`/`source` của mọi chart họ B khi dùng cho báo cáo VN, tránh người đọc hiểu nhầm đây là dữ liệu giao dịch trong nước.

---

## 5. Dữ liệu Việt Nam: nguồn, kỳ hạn thanh khoản, xử lý kỳ hạn thưa

### 5.1 Nguồn

Theo `reference-vn-data-sources.md` mục B và `domain-fi-yield-curve-vn.md`:

| Nguồn | Vai trò cho chart họ A | Tier |
|---|---|---|
| VBMA (`vbma.org.vn`) | Ước tính đường cong lợi suất, khối lượng giao dịch thứ cấp | Tier A |
| HNX (`hnx.vn`) | Giá/khối lượng giao dịch TPCP thực tế theo mã | Tier S (cho market structure) |
| Vietcap/ACBS/SSI Fixed Income Research | Synthetic 10Y yield, spread TPDN, ước tính khi benchmark rotate | Tier A/S theo bảng broker |
| NHNN | Lãi suất điều hành, OMO, làm đường tham chiếu chính sách nếu cần overlay | Tier S |
| FRED | UST yield để làm neo toàn cầu khi so sánh spread VN-Mỹ | Tier S |

Với chart họ B khi dùng dữ liệu hàng hoá quốc tế: Investing.com cho giá thời gian thực (Tier B, chấp nhận được cho hình minh hoạ nhưng không dùng làm số chốt báo cáo), FRED cho WTI/Brent lịch sử (Tier S), CFTC COT report cho positioning nếu cần phân tích chiều sâu (không có tương đương VN, xem `domain-commodities-futures-curve.md` §4, chỉ áp dụng khi phân tích thị trường quốc tế chứ không phải VN).

### 5.2 Kỳ hạn thực sự có thanh khoản (theo `domain-fi-yield-curve-vn.md` §1.1)

| Kỳ hạn | Thanh khoản | Xử lý trên chart |
|---|---|---|
| 5Y | Cao (benchmark phụ) | Chấm ĐẶC, đoạn nối 2 bên nét LIỀN |
| 10Y | Cao nhất (benchmark chính) | Chấm ĐẶC, nét LIỀN, có thể phóng to marker 1 bậc vì đây là điểm neo toàn hệ thống giá |
| 3Y, 7Y | Trung bình | Chấm ĐẶC nếu kỳ báo cáo có giá đóng cửa/broker quote đều đặn; chuyển RỖNG nếu kỳ đó không có báo giá liên tục |
| 1Y, 2Y | Thấp | Chấm RỖNG, đoạn nối 2 bên nét ĐỨT |
| 15Y, 20Y | Rất thấp (chủ yếu bảo hiểm nhân thọ giữ đến đáo hạn) | Chấm RỖNG, đoạn nối 2 bên nét ĐỨT |
| 30Y | Phát hành gần đây, dữ liệu lịch sử ngắn | BỎ HẲN điểm cho các kỳ báo cáo trước khi VN bắt đầu phát hành kỳ hạn này; không nội suy ngầm |
| 1M, 3M, 6M | Không tồn tại như 1 lớp tài sản TPCP giao dịch thứ cấp có ý nghĩa phân tích | Không đưa vào chart họ A cho VN (khác US, nơi T-bill 1M-6M là 1 phần chuẩn của yield curve) |

Quy tắc vẽ 3 cấp (đặc/liền, rỗng/đứt, bỏ) đã nêu ở bảng trên áp dụng thống nhất cho MỌI chart trong họ A khi dùng dữ liệu VN, không chỉ riêng chart hình dạng đường cong. Chú thích chuẩn đặt cuối chart (dòng nguồn, theo đúng khuôn `draw_source()`/`sourceGraphic()` đã có): "● quan sát được từ giá đóng cửa/broker quote · ○ ước tính dealer, thanh khoản thấp". Cách đặt tên 2 cấp này cố ý dùng lại đúng ngôn ngữ đã có trong `components/catalog/01-kpi-stat-grid.md` (`data-tier="cong-bo"` / `data-tier="uoc-tinh"`), để 1 báo cáo có cả bảng KPI và chart curve dùng chung 1 quy ước tier, không phải học 2 hệ ký hiệu khác nhau.

### 5.3 Benchmark rotation: không vẽ 1 đường 10Y liên tục như thể nó là 1 mã trái phiếu duy nhất

`domain-fi-yield-curve-vn.md` §2 nêu rõ: TPCP VN không có benchmark liên tục kiểu UST, "10Y" thực chất là mã phát hành gần nhất có kỳ hạn còn lại gần 10 năm, và các nguồn tự tính synthetic yield có thể lệch nhau ±20-30bps. Với chart THEO THỜI GIAN (term spread, butterfly value, hoặc bất kỳ chuỗi lợi suất theo ngày), không cần xử lý gì thêm trên chart (dữ liệu đầu vào coi là đã được lớp dữ liệu/broker xử lý rotation), nhưng PHẢI có dòng chú thích: "Chuỗi 10Y là mã đại diện gần nhất theo kỳ hạn còn lại, không phải 1 mã liên tục; các nguồn có thể lệch ±20-30bps quanh mốc benchmark rotation." Nếu cần so sánh trực tiếp ước tính giữa các broker (ví dụ khi 2 nguồn lệch nhau đáng kể), dùng component `range_dot` đã có sẵn trong `viz_eir.py` (điểm + khoảng lo/hi) làm chart PHỤ riêng, không trộn dải bất định đó vào chính đường cong chính (tránh nhầm ngữ nghĩa với fan chart dự báo vốn đã dùng dải mờ cho một khái niệm khác).

---

## 6. Biến thể KHÔNG đáng làm cho VN, và thay thế đề xuất

### 6.1 Z-spread thật: không khả thi, dùng "chênh lệch theo kỳ hạn khớp" thay thế

Z-spread đúng nghĩa (option-adjusted, giải lặp một mức dịch chuyển song song trên toàn bộ đường cong benchmark sao cho hiện giá dòng tiền trái phiếu khớp giá thị trường) đòi hỏi một đường cong benchmark LIÊN TỤC làm nền. `domain-fi-yield-curve-vn.md` §2.1 và §6 đã ghi rõ: VN không có benchmark liên tục, mỗi nguồn tự nội suy khác nhau, sai số ±20-30bps. Giải Z-spread trên nền dữ liệu này sẽ tạo ra độ chính xác giả (precision không có căn cứ), đúng loại rủi ro "gate đòi bằng chứng tạo động cơ bịa bằng chứng" cần tránh.

**Thay thế**: chênh lệch theo kỳ hạn khớp (tenor-matched spread) = lợi suất TPDN trừ lợi suất TPCP tại đúng kỳ hạn còn lại tương ứng (nội suy tuyến tính đơn giản giữa 2 điểm TPCP gần nhất nếu không trùng khớp), đúng công thức cơ bản đã nêu trong `domain-fi-credit-spreads-vn.md` §2.1 ("Yield TPDN = Yield TPCP cùng kỳ hạn + Credit Spread"). Vẽ bằng chính component `spread` (2 series a/b, không phải diff) đã có sẵn, `zero_is_signal: false`. Nhãn chart PHẢI ghi rõ "chênh lệch theo kỳ hạn khớp" chứ không được gọi là "Z-spread", để không nhận vơ độ chính xác mà phương pháp không có.

### 6.2 Đường cong tín dụng theo hạng: không khả thi, dùng đường cong theo nhóm phát hành thay thế

`domain-fi-credit-spreads-vn.md` §1.2 nói thẳng: "Tại VN không có hệ thống xếp hạng tín nhiệm (credit rating) phát triển như S&P/Moody's/Fitch." Một họ đường cong AAA/AA/A/BBB kiểu Mỹ không có dữ liệu nền để dựng.

**Thay thế**: đường cong theo NHÓM PHÁT HÀNH không chính thức mà chính domain doc dùng để phân loại: nhóm "gần IG" (ngân hàng, SOE lớn, có bảo lãnh thanh toán) và nhóm "gần HY" (BĐS tư nhân, không bảo lãnh hoặc bảo lãnh từ ngân hàng nhỏ). Vẽ như 2 đường trong 1 chart `spread` (2 series), có badge cảnh báo rõ ràng, ví dụ: "Phân nhóm không chính thức, thị trường tự phân loại theo loại tổ chức phát hành và bảo lãnh, KHÔNG phải xếp hạng tín nhiệm chuẩn hoá." Badge này bắt buộc, không tuỳ chọn, vì nếu thiếu, người đọc quen chart Mỹ sẽ mặc định đây là rating thật.

---

## 7. Đặc tả matplotlib

### 7.1 Module mới `charts/matplotlib/viz_eir_curves.py`

Theo đúng khuôn 5 module hiện có (`viz_eir.py`, `viz_eir_stats.py`, `viz_eir_diagram.py`, `viz_eir_panels.py`, `viz_eir_kpi.py`), mỗi module có 1 dict `COMPONENTS` export, mỗi hàm chữ ký `def c_xxx(p: dict, accent: str) -> Figure`. Đăng ký module mới vào `_MODULES` trong `charts/matplotlib/viz_super.py:42` (hiện là `_MODULES = ["viz_eir", "viz_eir_stats", "viz_eir_diagram", "viz_eir_panels", "viz_eir_kpi"]`, thêm `"viz_eir_curves"`).

Import dùng chung style core, đúng mẫu `viz_eir.py` dòng 22-32:

```python
import _eir_style as S
from _eir_style import (
    PAPER, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge, tint,
)
```

### 7.2 `c_yield_curve(p, accent)`

Vẽ chart hình dạng đường cong, tối đa 3 snapshot, trục hạng mục, kỳ hạn thưa xử lý theo §5, đảo ngược tô theo §3.1, butterfly tuỳ chọn theo §3.3.

```python
def c_yield_curve(p, accent):
    """
    p = {
      # meta chuẩn EIR: kicker, title, subtitle, source, asof, rating, firm
      "y_format": "pct", "dp": 2,           # 2 chữ số thập phân, không phải 1 mặc định
                                              # của fmt_value, vì chênh lệch 10bps giữa
                                              # các kỳ hạn liền kề sẽ biến mất ở 1 chữ số
      "snapshots": [
        {
          "name": "Hôm nay (07/08/2026)",
          "points": [
            {"tenor": "1Y",  "value": 2.85, "tier": "uoc_tinh"},
            {"tenor": "2Y",  "value": 2.95, "tier": "uoc_tinh"},
            {"tenor": "3Y",  "value": 3.05, "tier": "quan_sat"},
            {"tenor": "5Y",  "value": 3.25, "tier": "quan_sat"},
            {"tenor": "7Y",  "value": 3.35, "tier": "quan_sat"},
            {"tenor": "10Y", "value": 3.45, "tier": "quan_sat"},
            {"tenor": "15Y", "value": 3.70, "tier": "uoc_tinh"},
            {"tenor": "20Y", "value": 3.85, "tier": "uoc_tinh"}
          ]
        },
        {"name": "1 tháng trước (07/07/2026)", "points": [ ... ]},
        {"name": "1 năm trước (07/08/2025)",   "points": [ ... ]}
      ],
      # tuỳ chọn: tô đoạn đảo ngược + badge bps
      "inversions": [{"from": "2Y", "to": "10Y", "bps": -18}],
      # tuỳ chọn: dây cung tham chiếu butterfly
      "butterfly": {"wings": ["2Y", "10Y"], "belly": "5Y"}
    }
    """
```

Điểm khác biệt kỹ thuật so với các hàm `c_*` hiện có trong `viz_eir.py`:

- Trục x KHÔNG dùng `np.arange` đơn thuần như `c_index100`, mà dựng từ UNION các `tenor` xuất hiện ở bất kỳ snapshot nào (đã hợp nhất theo §1.2), giữ thứ tự kỳ hạn tăng dần cố định (`["1Y","2Y","3Y","5Y","7Y","10Y","15Y","20Y","30Y"]` là thứ tự chuẩn, không sort theo giá trị).
- KHÔNG gọi `ax.set_ylim(bottom=0)` ở bất kỳ đâu (khác các hàm cột trong `viz_eir.py`), để trục y tự co theo `ax.margins(y=...)` giữ đúng quyết định §1.2.
- Marker: `ax.scatter(..., facecolor=PAPER if tier=="uoc_tinh" else color, edgecolor=color)` để tạo hiệu ứng rỗng/đặc; đoạn nối dùng `ax.plot(..., linestyle=(0,(4,3)) if either endpoint tier=="uoc_tinh" else "-")`.
- Đảo ngược: lặp qua từng cặp điểm liền kề, nếu `value[i+1] < value[i]`, vẽ lại riêng đoạn đó bằng `ax.plot` màu `BRICK` đè lên trên (z-order cao hơn đường chính), gắn `_badge()` cạnh trung điểm đoạn.
- Butterfly: nếu có key `butterfly`, vẽ 1 `ax.plot` nét đứt màu `FAINT` nối thẳng 2 điểm cánh, không marker, z-order thấp hơn đường chính.

### 7.3 `c_futures_curve(p, accent)`

```python
def c_futures_curve(p, accent):
    """
    p = {
      "spot": 82.4, "spot_label": "Giá giao ngay",
      "contracts": [
        {"month": "M1 (09/2026)", "price": 83.1, "liquid": True},
        {"month": "M2 (10/2026)", "price": 83.6, "liquid": True},
        {"month": "M3 (11/2026)", "price": 84.0, "liquid": True},
        {"month": "M6 (02/2027)", "price": 85.1, "liquid": True},
        {"month": "M12 (08/2027)", "price": 86.4, "liquid": False}
      ],
      "y_format": "cur", "currency": "$",
      "roll_note": "Roll yield ước tính khoảng -2,1%/năm nếu nắm giữ hợp đồng gần liên tục"
    }
    """
```

Đường ngang spot: `ax.axhline(p["spot"], color=FAINT, lw=1.2, ls=(0,(4,3)))`. Badge trạng thái: so sánh giá trị trung bình các hợp đồng với spot, nếu toàn bộ cao hơn → badge "CONTANGO" nền `NAVY`; toàn bộ thấp hơn → "BACKWARDATION"; hỗn hợp → không gắn badge tự động, để tác giả báo cáo tự chú thích bằng tay (tránh gán nhãn sai khi hình dạng phức tạp). Hợp đồng `liquid: False` dùng đúng quy tắc marker rỗng/nét đứt như §5.

### 7.4 Term spread và butterfly theo thời gian: mở rộng `c_spread`, không viết hàm mới

Trong `viz_eir.py::c_spread` (dòng 225-251), nhánh `if p.get("diff")` hiện luôn tô `TEAL`/`BRICK` theo dấu. Thêm 1 tham số tuỳ chọn:

```python
zero_is_signal = p["diff"].get("zero_is_signal", True)
if zero_is_signal:
    ax.fill_between(xs, d, 0, where=[v >= 0 for v in d], color=TEAL, alpha=0.25, lw=0)
    ax.fill_between(xs, d, 0, where=[v < 0 for v in d], color=BRICK, alpha=0.25, lw=0)
else:
    ax.fill_between(xs, d, 0, color=accent, alpha=0.14, lw=0)
ax.plot(xs, d, color=NAVY, lw=2.0, zorder=3); ax.axhline(0, color=INK, lw=1.0)
```

Mặc định `True` giữ nguyên hành vi hiện tại, không phá `spec.json` nào đang gọi `component: "spread"`. Dùng `zero_is_signal: false` khi gọi cho butterfly.

---

## 8. Đặc tả ECharts

### 8.1 `charts/echarts/13-yield-curve.mjs`

Cấu trúc theo đúng khuôn `04-dumbbell.mjs`/`12-area-stack.mjs`: import `baseOption`, `TYPOGRAPHY`, `PALETTE`, `categoryAxis`, `valueAxis` từ `theme.mjs`, `fmtPercent` từ `fmt.mjs`.

```js
// 13-yield-curve.mjs: Đường cong lợi suất, 1 hoặc nhiều thời điểm chồng nhau
// Trục x là CATEGORY (kỳ hạn cách đều, không theo tỷ lệ năm thực, xem lý do
// trong docs/specs/2026-08-07-yield-forward-curve-design.md §1). Trục y
// KHÔNG bắt đầu từ 0 (khác valueAxis({startAtZero:true}) mặc định của các
// chart cột) vì đây là line chart, vị trí điểm đã mã hoá giá trị.

const tenorOrder = ['1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '15Y', '20Y', '30Y'];

const snapshots = [
  { name: 'Hôm nay (07/08/2026)', lineStyle: 'solid', points: {
      '1Y': { value: 2.85, tier: 'uoc_tinh' }, '2Y': { value: 2.95, tier: 'uoc_tinh' },
      '3Y': { value: 3.05, tier: 'quan_sat' }, '5Y': { value: 3.25, tier: 'quan_sat' },
      '7Y': { value: 3.35, tier: 'quan_sat' }, '10Y': { value: 3.45, tier: 'quan_sat' },
      '15Y': { value: 3.70, tier: 'uoc_tinh' }, '20Y': { value: 3.85, tier: 'uoc_tinh' },
  } },
  // ... snapshot 1 tháng trước, 1 năm trước, cùng cấu trúc
];

// hợp nhất tập kỳ hạn xuất hiện ở BẤT KỲ snapshot nào, giữ đúng thứ tự chuẩn
const categories = tenorOrder.filter((t) => snapshots.some((s) => t in s.points));

const styleByAge = [
  { lineWidth: 2.6, type: 'solid',           opacity: 1.0 },
  { lineWidth: 1.8, type: [5, 2],            opacity: 0.75 },
  { lineWidth: 1.4, type: [1, 2],            opacity: 0.55 },
];

const series = snapshots.map((snap, i) => ({
  name: snap.name, type: 'line', connectNulls: false,   // KHÔNG nối qua kỳ hạn thiếu (§5)
  lineStyle: { ...styleByAge[i], color: i === 0 ? PALETTE.accent : PALETTE.inkLo },
  data: categories.map((t) => {
    const p = snap.points[t];
    if (!p) return null;                                  // bỏ hẳn điểm, không nội suy (§5)
    return { value: p.value,
      symbol: p.tier === 'uoc_tinh' ? 'emptyCircle' : 'circle',   // rỗng = ước tính (§5)
      symbolSize: p.tier === 'uoc_tinh' ? 6 : 8 };
  }),
  endLabel: { show: true, formatter: () => snap.name, ...TYPOGRAPHY.dataLabel },
}));
```

Đảo ngược: dựng thêm 1 series `type: 'line'` chỉ chứa 2 điểm đoạn bị đảo ngược, `lineStyle.color: PALETTE.negative`, `z: 5` để đè lên trên, cộng 1 `graphic` text badge (theo mẫu `sourceGraphic` sẵn có) neo tại trung điểm.

Butterfly: 1 series phụ `type: 'line'`, 2 điểm là 2 cánh, `lineStyle: { type: 'dashed', color: PALETTE.inkLo, width: 1 }`, không `symbol`.

Trục y: dùng `valueAxis({ startAtZero: false, axisLabelFormatter: (v) => fmtPercent(v, {decimals: 2}) })`, tự co theo `min`/`max` mà ECharts tính (không ép `min: 0`).

### 8.2 `charts/echarts/14-term-spread.mjs`

Kỹ thuật tô màu theo dấu trong ECharts (không có sẵn kiểu `fill_between(where=...)` như matplotlib) dùng `visualMap` kiểu `piecewise`, áp theo GIÁ TRỊ của series, không phải theo index:

```js
// Kỹ thuật: 2 series area riêng (phần dương, phần âm), mỗi series đã lọc sẵn
// giá trị phía kia về null (connectNulls:false) để area không tô tràn qua 0.
const values = periods.map((_, i) => diffValues[i]);
const posSeries = values.map((v) => (v >= 0 ? v : null));
const negSeries = values.map((v) => (v < 0 ? v : null));

series: [
  { name: 'Dương', type: 'line', data: posSeries, connectNulls: false,
    lineStyle: { color: PALETTE.ink, width: 2 },
    areaStyle: zeroIsSignal ? { color: PALETTE.positive, opacity: 0.22 } : { color: PALETTE.accent, opacity: 0.14 },
    symbol: 'none' },
  { name: 'Âm', type: 'line', data: negSeries, connectNulls: false,
    lineStyle: { color: PALETTE.ink, width: 2 },
    areaStyle: zeroIsSignal ? { color: PALETTE.negative, opacity: 0.22 } : { color: PALETTE.accent, opacity: 0.14 },
    symbol: 'none' },
],
markLine: { silent: true, symbol: 'none',
  lineStyle: { color: PALETTE.ink, width: 1 },
  data: [{ yAxis: 0 }] },
```

`zeroIsSignal` là tham số hàm dựng chart (mirror đúng `zero_is_signal` bên matplotlib §7.4), mặc định `true` cho 2s10s, đặt `false` cho butterfly (khi đó cả 2 nhánh area dùng chung 1 màu `accent` nhạt, không phân biệt dương/âm bằng màu).

### 8.3 `charts/echarts/15-futures-curve.mjs`

Cấu trúc gần giống `13-yield-curve.mjs` nhưng trục x là category theo tháng hợp đồng (không cần hợp nhất union phức tạp vì tháng hợp đồng đã gần đều, xem §4.1), cộng:

```js
series: [
  { type: 'line', data: contractPrices, symbol: (v, p) => (p.data.liquid ? 'circle' : 'emptyCircle'),
    lineStyle: { color: PALETTE.accent, width: 2.4 } },
],
markLine: { silent: true, symbol: 'none',
  lineStyle: { color: PALETTE.inkLo, type: 'dashed', width: 1.2 },
  label: { formatter: 'Giá giao ngay', position: 'insideStartTop', ...TYPOGRAPHY.axisName },
  data: [{ yAxis: spotPrice }] },
],
graphic: [
  { type: 'text', left: 'center', top: 40,
    style: { text: shape === 'contango' ? 'CONTANGO' : 'BACKWARDATION',
             font: `bold 11px ${FONT_STACK}`, fill: PALETTE.paper },
    // vẽ kèm 1 rect nền NAVY phía sau text, không dùng positive/negative
  },
],
```

`shape` (`'contango' | 'backwardation' | null`) tính ở tầng dữ liệu (so sánh trung bình giá hợp đồng với spot), không tự động gắn badge nếu hỗn hợp, đúng quy tắc đã nêu ở §7.3.

---

## 9. Ràng buộc cứng đã tuân thủ (đối chiếu lại)

- Không đề xuất gauge hay radar ở bất kỳ đâu trong đặc tả này.
- Mọi màu tham chiếu đều lấy từ `PALETTE`/`COLORS` đã có trong `theme.mjs`/`tokens.py` (`accent`, `accentSoft`/`accent_soft` qua `tint()`, `ink`, `inkMd`, `inkLo`, `line`, `positive`, `negative`), không có hex mới nào được đề xuất.
- Toàn bộ nhãn ví dụ (badge, tên snapshot, ghi chú nguồn) không dùng em-dash/en-dash, chỉ dùng dấu phẩy, dấu hai chấm, hoặc xuống dòng.
- Nhãn tiếng Việt trong ví dụ có dấu đầy đủ; ký hiệu kỳ hạn (1Y, 2Y, ..., M1, M2, ...) giữ nguyên quy ước quốc tế mà chính báo cáo broker VN đang dùng (đã thấy trực tiếp trong `domain-fi-yield-curve-vn.md`: "Yield 10Y TPCP", "TPCP 5Y"), tương tự cách `fmt.mjs` cố ý giữ "Q3/2026" thay vì dịch hẳn sang tiếng Việt.
- Hai họ z-spread thật và đường cong tín dụng theo hạng thật đã nói thẳng là KHÔNG làm cho VN, kèm lý do dữ liệu cụ thể và phương án thay thế có căn cứ (§6), theo đúng yêu cầu không được im lặng bỏ qua.
