# Nhất quán số liệu giữa các exhibit của CÙNG một mô hình

Vòng 5, vùng "chưa ai từng đặt 2 exhibit của CÙNG một mô hình cạnh nhau để bắt lỗi số liệu tự
mâu thuẫn" - phát hiện của mũi tổng hợp (`research/08-synthesis/FINDINGS.md` mục 3.5), ghi ở
`research/RESEARCH-LEDGER.md` dòng "Trung bình, phát hiện mới từ vòng 3 tổng hợp". Mười vùng
khác đã xong, file này không lặp lại.

Đọc mục mindset đầu `RESEARCH-LEDGER.md` trước: preset là thư viện lấy ý, không phải khuôn ép.
Nhưng vùng này nghiêng về RÀNG BUỘC CỨNG hơn các vùng khác, vì nhất quán số liệu là chuyện
ĐÚNG/SAI đo được bằng số, không phải chuyện gu thẩm mỹ - một exhibit lệch số với chính nó ở
trang khác không có phiên bản "vẫn chấp nhận được vì đó là lựa chọn thiết kế".

---

## 1. Danh mục các cặp exhibit hay tự mâu thuẫn

Điểm chung của cả 4 cặp dưới đây: chúng chia sẻ MỘT tập biến đầu vào nhưng được VẼ ĐỘC LẬP bởi
quy trình/người khác nhau (một cái là chart SVG tay vẽ, một cái là bảng số, một cái là văn xuôi
tóm tắt), nên không có cơ chế nào tự động bắt buộc chúng đồng bộ khi một trong hai bị sửa.

### 1.1 Football field vs. lưới độ nhạy 2 chiều (worked example đầy đủ của file này)

**Biến chia sẻ**: WACC, tăng trưởng dài hạn (g), FCFF chuẩn hoá, nợ ròng, số cổ phiếu lưu hành.
Football field vẽ dải DCF là MỘT trong nhiều dải phương pháp; lưới độ nhạy vẽ TOÀN BỘ ma trận
WACC×g. Dải DCF trên football field, nếu đúng, phải bằng đúng MIN/MAX của ma trận đó.

**Mâu thuẫn thường xuất hiện ở đâu**: người vẽ football field ước lượng dải "trông hợp lý" quanh
kịch bản cơ sở (ví dụ +-15% quanh giá trị trung tâm) thay vì tính lại từ 2 góc cực của lưới độ
nhạy thật. Vì cả hai con số đều "nghe hợp lý" đứng riêng, sai lệch chỉ lộ ra khi đặt cạnh nhau và
trừ trực tiếp. Đây đúng là cơ chế bắt được ở `research/08-synthesis/FINDINGS.md` mục 3.5 (dải
19.200-24.600 viết tay so với 19.050-24.750 tính từ lưới) và được TÁI HIỆN CÓ CHỦ Ý trong
`samples/cross-dcf-mau-thuan.html` của vòng này (17,5-28,5 ghi trên hình so với 18,6-30,0 tính từ
lưới, lệch 1,1 và 1,5 nghìn đồng, đủ nhỏ để trông như làm tròn).

### 1.2 Bảng dòng tiền vs. biểu đồ waterfall

**Biến chia sẻ**: từng dòng mục (doanh thu, giá vốn, chi phí bán hàng, EBITDA, khấu hao, EBIT,
thuế, lãi vay, lợi nhuận ròng) và các mốc cộng dồn giữa chúng. Waterfall là hình ảnh hoá TRỰC
TIẾP của đúng dãy số trong bảng, không phải một cách tính khác.

**Mâu thuẫn thường xuất hiện ở đâu**: hai lỗi hay gặp nhất trong nghiệp vụ dựng waterfall (i) dấu
của cột: một khoản chi phí phải vẽ ÂM (giảm cột) nhưng bảng ghi số dương kèm chú thích "trừ", khi
chuyển sang waterfall người vẽ quên đảo dấu; (ii) mốc cộng dồn: cột "EBITDA" trên waterfall phải
đứng ở ĐÚNG độ cao bằng tổng luỹ kế tới thời điểm đó, nhưng nếu bảng nguồn được cập nhật một dòng
(ví dụ sửa lại chi phí bán hàng) mà waterfall không dựng lại từ đầu, cột mốc sẽ "treo lơ lửng"
sai độ cao trong khi các cột linh kiện xung quanh vẫn đúng riêng lẻ.

### 1.3 Bảng comps vs. biểu đồ định giá tương đối

**Biến chia sẻ**: multiple (P/E, EV/EBITDA) và giá trị suy ra cho công ty mục tiêu từ multiple
trung vị/trung bình của nhóm so sánh. Bảng liệt kê từng công ty comp; biểu đồ thường chỉ vẽ
target company cộng dải trung vị-tứ phân vị của nhóm.

**Mâu thuẫn thường xuất hiện ở đâu**: nhóm comps trong bảng và nhóm dùng để tính dải trên biểu đồ
lệch nhau vì một lý do rất phổ biến - bảng liệt kê TOÀN BỘ nhóm so sánh ban đầu (kể cả outlier),
nhưng biểu đồ dùng nhóm đã LOẠI outlier để dải trông "gọn" hơn, và quyết định loại outlier đó
không được ghi lại ở cả hai nơi. Người đọc đối chiếu multiple trung vị trên biểu đồ với chính
bảng liệt kê sẽ tính ra một trung vị khác, vì tập hợp nguồn đã âm thầm khác nhau.

### 1.4 Tóm tắt điều hành vs. thân bài

**Biến chia sẻ**: bất kỳ con số nào được nhắc lại từ thân bài lên trang tóm tắt (định giá mục
tiêu, hạn mức đề xuất, tăng trưởng doanh thu dự phóng). Đây là cặp DỄ MẤT ĐỒNG BỘ NHẤT trong thực
tế vì tóm tắt điều hành thường được viết/sửa SAU CÙNG và SAU CÙNG NHẤT trong quy trình soạn báo
cáo, đúng lúc ít thời gian đối chiếu lại nhất.

**Mâu thuẫn thường xuất hiện ở đâu**: thân bài được cập nhật một vòng review cuối (ví dụ WACC đổi
từ 11,0% xuống 10,5% sau khi có ý kiến phản biện) nhưng con số hệ luỵ ở trang tóm tắt (định giá
mục tiêu) không được tính lại, vì tóm tắt điều hành nằm ở ĐẦU tài liệu còn bản sửa nằm ở GIỮA,
người sửa dễ quên cuộn lên đầu. `feedback_exec_brief_action_first_no_recap.md` (memory dự án) đã
ghi nhận nguyên tắc "tóm tắt = action-first, không recap"; cặp này bổ sung thêm một lý do KỸ
THUẬT cho nguyên tắc đó: recap càng nhiều số, bề mặt có thể lệch càng lớn.

---

## 2. Nguồn duy nhất của sự thật: cách các bên khác bảo đảm exhibit đồng bộ

### 2.1 Governance mô hình sell-side: định nghĩa - nguồn - đối chiếu, không phải một công cụ

Khảo sát qua tổng hợp tìm kiếm (Onetribe Advisory, "Single Source of Truth in Finance"; FD
Capital, "Building a Single Source of Truth in Modern Finance"): giới tài chính doanh nghiệp coi
"nguồn duy nhất của sự thật" là một KẾT QUẢ QUẢN TRỊ (governance outcome) - một tập định nghĩa,
nguồn, và công thức được thống nhất - chứ không phải một hệ thống hay công cụ cụ thể. Thực hành
cụ thể hay được nhắc: chọn ra một nhóm nhỏ con số hay lặp lại nhiều nơi nhất (ví dụ 5 con số xuất
hiện trong mọi board pack), rồi với mỗi con số: định nghĩa nó là gì, nguồn nó lấy từ đâu, và nhịp
đối chiếu lại là gì. Khảo sát cũng ghi nhận một con số đáng chú ý: tổ chức tài chính trung bình
duy trì 3-5 "nguồn sự thật" cạnh tranh nhau cho cùng một dữ liệu - tức là bài toán "hai exhibit
lệch nhau" không phải hiếm gặp hay đặc thù của báo cáo tự soạn, mà là tình trạng phổ biến ngay cả
ở tổ chức có quy trình.

**Chuyển sang bối cảnh này**: 5 con số neo nhiều exhibit nhất trong một báo cáo định giá (WACC,
g dài hạn, FCFF chuẩn hoá, nợ ròng, số cổ phiếu lưu hành cho mô hình DCF) nên có đúng MỘT nơi
định nghĩa - khối `dcf-assumptions` trong 3 mẫu của vòng này là cách làm cụ thể cho HTML tĩnh,
không có Excel để liên kết ô.

### 2.2 IMF World Economic Outlook: một cơ sở dữ liệu cho một kỳ xuất bản, đánh số chương.hình

Xác nhận qua truy cập trực tiếp `imf.org` (khác với vòng 06-source-notes trước đó gặp lỗi 403 khi
tải PDF WEO gốc, lần này fetch qua kết quả tìm kiếm thành công): mỗi kỳ WEO (tháng 4 hoặc tháng
10) công bố một cơ sở dữ liệu WEO đúng kỳ đó, và MỌI hình/bảng trong ấn phẩm của kỳ đó đọc từ
CÙNG cơ sở dữ liệu này - không có chuyện Chương 1 dùng một bản snapshot còn Phụ lục Thống kê dùng
bản khác của cùng kỳ xuất bản. Hình được đánh số dạng "chương.số hình" (ví dụ "Figure 1.17",
"Figure 1.2" đều thuộc Chương 1), và khi cần chi tiết hơn, hình trong chương chính tự trỏ chéo
sang Phụ lục Thống kê CỦA CHÍNH KỲ ĐÓ (ví dụ ghi chú "See Box A2 of the WEO Statistical Appendix"
đọc được trong các số phát hành gần đây) - không bao giờ trỏ mơ hồ kiểu "xem phụ lục" mà không
ghi rõ đang nói tới Phụ lục nào của kỳ nào.

**Chuyển sang bối cảnh này**: quy ước "Hình 1"/"Hình 2" đánh số liên tục đã có sẵn trong
`samples/report-exhibit-institutional.html` (vòng 02) được 3 mẫu của vòng này tái sử dụng nguyên
vẹn, cộng thêm việc mỗi hình tự ghi rõ đang nói về mô hình/kỳ số liệu nào (khối "Neo chéo" mục 4
dưới đây), đúng tinh thần "không trỏ mơ hồ" của quy ước IMF.

### 2.3 SEC Regulation S-K: cross-reference phải nêu rõ vị trí, và số liệu phải nhất quán xuyên tài liệu

Xác nhận qua tổng hợp tìm kiếm về Reg S-K/Form and Content of Prospectuses (17 CFR Part 230):
quy định cáo bạch Mỹ yêu cầu (i) mọi trình bày lại số liệu ở nơi khác trong tài liệu phải NHẤT
QUÁN với báo cáo tài chính/thông tin phi tài chính đã công bố trong cùng tài liệu, và (ii) khi
dẫn chiếu sang phần khác (ví dụ mục Risk Factors), phải nêu RÕ VỊ TRÍ kèm số trang, và cross-
reference đó phải được làm nổi bật bằng kiểu chữ riêng (không chìm vào văn bản thường) - không để
người đọc tự đoán hai chỗ có cùng nguồn hay không.

**Chuyển sang bối cảnh này**: khối `.xref` ("Neo chéo &rarr; Hình X") trong 3 mẫu dùng đúng hai
kỷ luật này - nêu rõ hình đích (không chỉ nói "xem phụ lục" chung chung), và được làm nổi bằng
nền màu + viền trái đậm để không chìm vào caption thường.

---

## 3. Kỹ thuật phát hiện tự động

### 3.1 Nhúng data-* trên con số nguồn, đối chiếu bằng script (kỹ thuật thực dụng nhất, xem CONSISTENCY-CHECK.md)

Đây là kỹ thuật dùng trong cả 3 mẫu của vòng này và là kỹ thuật GIÁ TRỊ NHẤT trong 3 hướng được
khảo sát, vì hai lý do: (a) không cần thay đổi CÁCH VẼ hình (SVG tay vẽ vẫn giữ nguyên, chỉ thêm
thuộc tính `data-*` vào phần tử đã có sẵn), và (b) chạy được trên CHÍNH file HTML output cuối
cùng, không phải trên một bước trung gian có thể lệch khỏi output thật. Cơ chế: mỗi con số hiển
thị mang theo NGUỒN của nó (WACC, g dùng để tính ra nó) dưới dạng thuộc tính máy đọc được; một
khối `<script type="application/json" class="dcf-assumptions">` duy nhất khai công thức và tham
số; script Python tính lại độc lập từ khối JSON đó và so với số đã ghi trên từng phần tử, báo
FAIL kèm số liệu cụ thể nếu lệch quá dung sai làm tròn hiển thị. Chi tiết đầy đủ, script chạy
được, và cách mở rộng: xem `CONSISTENCY-CHECK.md`.

**Giới hạn thật đã gặp khi dựng**: kỹ thuật này chỉ bắt được sai lệch nếu người viết THẬT SỰ gắn
đúng thuộc tính `data-*` khớp với hình vẽ - nếu ai đó sửa con số hiển thị (text) mà quên sửa luôn
thuộc tính `data-price` đi kèm, script sẽ so hai con số ĐÃ SAI GIỐNG NHAU và báo PASS giả. Đây
không phải lỗ hổng lý thuyết: chính lúc dựng `samples/cross-dcf-khac-biet-co-chu-y.html`, một bản
nháp trung gian đổi số hiển thị "25,3" nhưng quên đổi `data-price` tương ứng đã từng lọt qua đúng
kiểu PASS giả này trước khi bị bắt lại bằng cách đối chiếu ảnh render với bảng số tính tay - tức
là kỹ thuật này cần đi kèm ÍT NHẤT một lần verify bằng mắt trên ảnh render thật, không thay thế
hoàn toàn bước đó, chỉ giảm số lần cần làm.

### 3.2 Sinh cả hai hình từ một file JSON giả định duy nhất (mạnh hơn nhưng tốn hơn)

Thay vì nhúng `data-*` sau khi vẽ tay, cách làm chặt hơn là để MỘT script (ví dụ một hàm trong
`charts/echarts/`) đọc file JSON giả định và SINH RA cả football field lẫn lưới độ nhạy, đảm bảo
nhất quán bằng cấu trúc chứ không phải bằng việc nhớ đối chiếu thủ công. Đây là hướng ĐÚNG cho
sản xuất thật (khi football field/lưới độ nhạy được code hoá thành `.mjs` theo đề xuất còn treo ở
`research/03-chart-doctrine/FINDINGS.md` mục 9), nhưng KHÔNG áp dụng được cho các mẫu HTML tay vẽ
hiện có của repo (03-chart-doctrine, 08-synthesis) vì chúng không đi qua build step nào. Ghi nhận
làm hướng kế tiếp, không dựng lại ở vòng này vì đụng tới `charts/`, ngoài phạm vi ghi file của
agent nghiên cứu.

### 3.3 Trích số từ tầng text PDF rồi đối chiếu chéo (dùng khi không có data-*, ví dụ audit tài liệu cũ)

Khi không thể sửa lại HTML nguồn (ví dụ đang audit một PDF đã xuất bản, hoặc file HTML của một
vòng trước không có `data-*`), vẫn có thể bắt lỗi loại này bằng cách trích văn bản từng trang qua
`page.get_text()` (pymupdf), dùng regex bắt các mẫu số có đơn vị đi kèm gần nhãn hình (ví dụ số
liền trước/sau chữ "nghìn đồng", "tỷ đồng"), rồi so nhóm số trích từ 2 exhibit nghi ngờ liên quan.
Kỹ thuật này YẾU HƠN 3.1 vì (a) không biết CHẮC hai số trích ra có thật sự cùng một mô hình hay
chỉ tình cờ giống nhãn số, cần người kiểm tra lại bằng mắt trước khi kết luận, và (b) phụ thuộc
định dạng số nhất quán (dấu phẩy thập phân, đơn vị) xuyên toàn tài liệu để regex bắt đúng - nhưng
là lựa chọn DUY NHẤT khi không kiểm soát được HTML nguồn để nhúng `data-*` trước.

---

## 4. Ghi chú neo chéo

Quy ước dùng trong cả 3 mẫu: khối `.xref` đặt NGAY DƯỚI mỗi exhibit (không gộp chung một chỗ ở
cuối tài liệu), mở đầu bằng **"Neo chéo &rarr; Hình X"** in đậm màu accent, nêu rõ: (a) hình đích
cụ thể (không nói "xem phụ lục" chung chung, theo đúng kỷ luật SEC ở mục 2.3), (b) QUAN HỆ SỐ HỌC
cụ thể giữa hai exhibit (ví dụ "= min/max của lưới", không chỉ nói "liên quan tới nhau"), và (c)
với mẫu có script kiểm, tên thuộc tính `data-method` đang dùng để người đọc kỹ thuật tự tra được
cơ chế kiểm.

**Khi nào KHÔNG cần khối xref riêng**: báo cáo chỉ có 1 exhibit cho mỗi mô hình (không có gì để
neo chéo tới), hoặc hai exhibit đã đứng đủ gần nhau trên cùng một trang/cùng tầm mắt để người đọc
tự đối chiếu ngay không cần chỉ dẫn bằng lời (ví dụ bảng số và biểu đồ minh hoạ ngay chính bảng đó
trong cùng một khối, không phải hai trang cách nhau).

---

## 5. Khi nào MÂU THUẪN LÀ ĐÚNG

Đây là phần dễ làm sai theo cả hai hướng, và cả hai đều có ví dụ thật dựng trong `samples/`:

**Sai hướng 1 - coi mọi khác biệt là lỗi**: ép hai exhibit hợp lệ khác nhau (dùng khác kịch bản,
khác ngày chốt số liệu, khác phương pháp) phải khớp số bằng mọi giá sẽ CHE GIẤU một khác biệt có
thật mà người đọc cần biết. Ví dụ: dải "house view" hẹp dùng để ra quyết định đầu tư và dải
"stress-test" rộng dùng để đo rủi ro đuôi PHẢI khác nhau - nếu ai đó chỉnh cho hai dải bằng nhau,
báo cáo mất đi chính công cụ phân biệt "khuyến nghị" với "kịch bản xấu nhất".

**Sai hướng 2 - dùng nhãn "khác biệt có chủ đích" để nguỵ trang lỗi thật**: chỉ ghi một câu giải
thích nghe hợp lý ("dải này dùng cho quyết định, dải kia dùng cho rủi ro") mà KHÔNG kiểm bằng số
xem dải hẹp có thật sự là tập con của dải rộng hay không, thì một lỗi tính sai vẫn trốn được sau
lớp vỏ ngôn từ đó - về hình thức trông giống hệt một khác biệt hợp lệ.

**Hai điều kiện bắt buộc để coi một khác biệt là hợp lệ**, minh hoạ đầy đủ trong
`samples/cross-dcf-khac-biet-co-chu-y.html`:

1. **Có nhãn rõ ràng ngay trên hình** nói khác biệt tồn tại và VÌ SAO (ví dụ "TÓM TẮT ĐIỀU HÀNH -
   DẢI KHUYẾN NGHỊ (HOUSE VIEW)" so với "PHỤ LỤC - LƯỚI STRESS-TEST ĐẦY ĐỦ"), để người đọc không
   cần suy đoán.
2. **Quan hệ giữa hai dải được TÍNH LẠI bằng số, không chỉ khẳng định bằng lời**: dải hẹp phải
   thật sự là tập con của dải rộng khi tính từ cùng một khối giả định - kiểm bằng thuộc tính
   `data-method="house-view-subset"` cộng script (mục 3.1), không dừng ở việc đọc câu giải thích
   thấy "nghe có lý".

Thiếu điều kiện 1: người đọc bình thường sẽ tưởng đây là mâu thuẫn giống hệt
`samples/cross-dcf-mau-thuan.html`, vì tự bản thân hai con số khác nhau không nói được lý do.
Thiếu điều kiện 2: đây thật ra LÀ lỗi, chỉ đang được nguỵ trang bằng ngôn ngữ "khác biệt có chủ
đích" - script trong `check_cross_exhibit.py` áp cả hai điều kiện cùng lúc (khớp đúng công thức
VÀ nằm trong phạm vi lưới đầy đủ), nên không thể PASS chỉ nhờ có nhãn đẹp.

---

## Nguồn khảo sát

- Wall Street Prep, "Football Field Valuation"; Macabacus, "Building a Football Field Chart in
  Excel" - đã dùng ở vòng 03-chart-doctrine, không khảo sát lại, chỉ kế thừa cho worked example.
- Onetribe Advisory, "Single Source of Truth in Finance"; FD Capital, "Building a Single Source
  of Truth in Modern Finance" - khảo sát qua tổng hợp tìm kiếm cho mục 2.1.
- IMF, World Economic Outlook (Chapter 1, các kỳ 2025-2026) và Statistical Appendix cùng kỳ -
  xác nhận qua truy cập trực tiếp `imf.org` cho quy ước đánh số hình và cross-reference ở mục 2.2.
- SEC, Regulation S-K / 17 CFR Part 230 (Form and Content of Prospectuses) - khảo sát qua tổng
  hợp tìm kiếm cho mục 2.3.
- `research/08-synthesis/FINDINGS.md` mục 3.5 - nguồn phát hiện gốc của toàn bộ vùng này, tái
  hiện có chủ ý trong `samples/cross-dcf-mau-thuan.html`.
- `research/06-source-notes/FINDINGS.md` mục 1.1 - quy ước IMF/World Bank/BIS về ngày chốt số
  liệu, kế thừa cho colophon 2 mốc (chốt số liệu/biên soạn) ở cả 3 mẫu.
