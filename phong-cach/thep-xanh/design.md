# thep-xanh: design.md

Harvest từ hiện trạng repo, không sáng tác mới. Giọng này đã sống trong
`design-system/tokens.css`, `pipeline/report.css` và exemplar
`examples/van-tai-bien` từ trước khi tầng phong-cách tồn tại; file này chỉ đặt
tên cho những gì đã chạy thật.

## 1. Khí chất và mood

Thep-xanh là giọng biên tập xanh lạnh của một định chế đang nói, không phải
giọng cá nhân. Người nhận tin ở mật độ lập luận và ở cách mỗi khẳng định gắn
liền một con số có nguồn, không tin ở trang trí. Ba từ đúng cảm giác khi mở
một ấn phẩm mang giọng này: nghiêm túc, có tổ chức, và lạnh theo nghĩa tiết
chế màu chứ không phải xa cách.

## 2. Nguồn màu

Chủ đề mặc định là `sang-lanh`, chủ đề dẫn xuất tối là `toi-lanh` khi ấn
phẩm cần bản màn hình tối; thep-xanh không tự pha thêm bảng nào khác ngoài
hai chủ đề đó. `--accent` chỉ đứng ở đường nhấn, kicker và liên kết, không
bao giờ làm nền một khối lớn. `--pos` và `--neg` mang ngữ nghĩa tốt/xấu,
sống trong chart, bảng so sánh, và các component trạng thái đã duyệt (nguồn
xét duyệt đầy đủ nằm trong comment gốc của `tokens.css`, không chép lại
danh sách ở đây vì sẽ trôi); cấm dùng hai token này làm màu trang trí hay
màu nhấn tuỳ hứng ngoài phạm vi ngữ nghĩa đó. `--ink` mang toàn bộ trọng
lượng chữ thân bài, `--ink-md` và `--ink-lo` hạ bậc cho chú thích và nhãn kỹ
thuật, không hạ thấp hơn mức đã sửa để giữ tương phản. Nền dùng `--paper`
cho thân trang, `--paper-hi` cho khối cần tách nhẹ; không dùng `--paper-elev`
để giả độ nổi, vì repo đã cấm shadow có blur và độ nổi ở giọng này đến từ
viền và khoảng trắng thật, không đến từ đổ bóng.

## 3. Chữ

Cặp chữ là `--font-display`/`--font-serif` (Spectral) cho tiêu đề và thân
bài, `--font-mono` (IBM Plex Mono) cho toàn bộ số liệu và nhãn kỹ thuật,
đúng vai trò đã khai trong `tokens.css`. Thang cỡ chữ dùng nguyên
`--fs-caption` tới `--fs-h1` của `tokens.css`, tỉ lệ 1,333; thep-xanh không
chỉnh lại thang này. `--font-sans` (IBM Plex Sans) chỉ mở cho bảng dữ liệu
dày cần chữ đặc hơn serif, cùng phạm vi hẹp đã ghi trong `tokens.css`,
thep-xanh không mở rộng vai trò đó sang tiêu đề hay thân bài. Không quy tắc
nào của `doctrine/03-viet-chu.md` bị lệch; giọng này tuân thủ nguyên, kể cả
luật câu chốt dưới hai mươi hai từ mang số hoặc hành động.

## 4. Blueprint theo 7 loại ấn phẩm

Văn xuôi dưới bảng chỉ giải thích lý do, không lặp lại nội dung bảng.

| Loại ấn phẩm | Bố cục vào bài | Component hợp giọng | Preset chart hợp | TRÁNH |
|---|---|---|---|---|
| Bản tin thị trường | Mở thẳng bằng số kèm mốc so sánh, không trang bìa riêng, một kicker mono ở đầu | `20-source-badge-k-anchor`, `29-narrative-strip` | `13-line-annotated`, `09-candlestick` | `17-football-field`, `18-sensitivity-grid`: quá nặng cho một tin trong ngày |
| Cập nhật kết quả kinh doanh | Trang mở là câu verdict có số, theo sau là bảng KPI rồi mới tới chi tiết từng khoản mục | `01-kpi-stat-grid`, `14-before-after` | `01-waterfall`, `04-dumbbell` | `23-waffle`: đơn giản hoá quá tay cho mật độ số cao của loại này |
| Báo cáo khởi tạo một mã | Đủ ba tầng định hướng, bằng chứng, phản biện; đóng bằng mục nêu điều kiện làm luận điểm sai | `10-assertion-evidence`, `17-methodology-box`, `15-ranked-risk-block` | `17-football-field`, `18-sensitivity-grid`, `06-tornado` | Dùng `26-scenario-cards` một mình không kèm methodology: kết luận valuation thiếu đường tính |
| Báo cáo ngành | Câu hỏi mở đầu mỗi mục, minh hoạ ngành đặt gần đoạn nêu ràng buộc vật lý của ngành | `29-narrative-strip`, `12-hairline-data-table` | `13-line-annotated`, `14-bar-ranking`, `07-small-multiples` | `21-upset`, `22-alluvial`: thừa phức tạp trừ khi câu hỏi đúng là tập hợp chồng lấn |
| Deal pack, bản chào vốn | Trang đầu là bảng phương án so theo ngưỡng, không mở bằng bối cảnh ngành | `13-options-comparison-table`, `26-scenario-cards` | `17-football-field`, `18-sensitivity-grid` | Lặp `24-bonus-key-point-callout` nhiều lần thay lập luận: thep-xanh giữ mật độ, không rút thành khẩu hiệu |
| Tóm tắt điều hành | Không hợp: MUC_CAM_KET 9 trên khung ba phần cực ngắn đòi giọng dứt khoát hơn mật độ lập luận của thep-xanh cho phép | Nếu bắt buộc, chỉ `25-exec-summary-quad` đặt cuối, không dùng làm toàn bộ ấn phẩm | Tối đa một `03-bullet`, không thêm chart phân tích | Dùng thep-xanh cho toàn bộ tóm tắt điều hành: mật độ lập luận kéo dài đúng thứ loại này cần cắt ngắn |
| Bản mẫu kỹ thuật, số minh hoạ | Không cần đóng khung nặng, khai rõ ngay đầu bài rằng số liệu là số dựng để nghiệm thu, đúng tiền lệ exemplar | `20-source-badge-k-anchor` | Bất kỳ preset đang cần nghiệm thu đường ống | Bịa giọng nghiêm trang cho số minh hoạ như thể đó là số công bố thật |

Ba hàng đầu và hàng báo cáo ngành khớp `best_for` khai trong
`phong-cach.json`; hàng tóm tắt điều hành khớp `avoid_for`. Hai hàng còn
lại, deal pack và bản mẫu kỹ thuật, chưa có exemplar thật chạy qua nghiệm
thu, xem mục 7.

## 5. Motion cho làn html-song

Thep-xanh hiện KHÔNG có motion ở tầng trang: không `@keyframes` reveal theo
cuộn nào trong `report.css` hay `components.css`, không `IntersectionObserver`
nào gắn vào exemplar đã dựng. Đây là chủ ý của giọng tổ chức tĩnh, không
phải một chỗ còn thiếu: một ấn phẩm mang giọng này đọc đúng y hệt nhau dù
cuộn nhanh hay cuộn chậm.

Motion duy nhất đang chạy thật nằm ở tầng chart, không phải tầng trang.
Chart sống mount qua `mount-live.mjs` GIỮ animation mặc định của ECharts,
đúng comment nguồn của chính file đó: đây là năng lực riêng của làn
html-song mà làn pdf-so không có, vì đường SSR (`render-static.mjs`) bắt
buộc `animation: false` theo luật CLAUDE.md để tránh lỗi marker bị kéo về
gốc toạ độ. Nói cách khác, chart SỐNG có animation nội tại của ECharts,
chart TĨNH thì không, và thep-xanh không thêm hành vi nào ngoài hai mặc
định đó.

Hệ quả đo được: gate `3. REDUCED-MOTION` trong nghiệm thu của van-tai-bien
đang SKIP, không PASS, đúng vì trang không có phần tử nào animate ở tầng
CSS nên gate tự nhận nó chưa chứng minh được khả năng phân biệt hai trạng
thái. Nếu một bản sau của thep-xanh thêm motion tầng trang thật, gate đó
phải sống dậy thành PASS đo được chứ không phải giữ nguyên SKIP; điều kiện
này ghi trong mục 7.

## 6. Anti-pattern

1. Cấm gradient text ở tiêu đề: giọng biên tập không cần hiệu ứng thị giác để tỏ ra hiện đại.
2. Cấm card lồng card cho cùng một khối nội dung: thep-xanh phân lớp bằng viền và khoảng trắng, không bằng bóng đổ chồng lớp.
3. Cấm icon emoji thay cho nhãn chữ: trạng thái đã có mã màu và nhãn mono, thêm icon là trùng lặp không kiểm được.
4. Cấm dùng `--accent` làm màu chữ cho một đoạn dài quá một dòng: accent chỉ đứng ở điểm nhấn, kéo dài nó làm mất chính vai trò nhấn.
5. Cấm gauge và radar: luật cấp repo, nhắc lại vì blue editorial rất dễ bị đề xuất gauge cho KPI.
6. Cấm dùng `--pos`/`--neg` làm màu trang trí hay màu nhấn tuỳ hứng ngoài phạm vi ngữ nghĩa tốt/xấu đã duyệt: hai token này mang nghĩa, không mang thẩm mỹ.
7. Cấm mở bài bằng bối cảnh khi MUC_CAM_KET từ 7 trở lên: trang đầu phải là verdict có số, không phải recap.
8. Cấm hoạ tiết trang trí không neo vào một con số nào trên chính trang đó, theo bốn dấu hiệu gộp của anti-slop.
9. Cấm chuyển động lặp lại mỗi lần cuộn qua cuộn lại một khối đã hiện: hiệu ứng chỉ chạy một lần khi vào khung nhìn.
10. Cấm thẻ số bo tròn kèm icon mũi tên thay cho cỡ chữ áp đảo: cách làm nổi một con số của giọng này là cỡ chữ, không phải khung trang trí.

## 7. Known Gaps

Thep-xanh chưa có motion ở tầng trang, xem mục 5. Điều kiện gỡ nếu sau này
muốn thêm reveal theo cuộn: phần tử animate phải khiến gate
`3. REDUCED-MOTION` chuyển từ SKIP sang PASS đo được thật, không phải giữ
nguyên SKIP, vì SKIP hiện tại là gate tự nhận chưa có gì để phân biệt chứ
không phải một xác nhận an toàn.

Chưa có bằng chứng làn `pdf-so` cho thep-xanh, dù hạ tầng PDF vẫn là mặc
định của repo: mọi dòng trong file này về bản in màn hình là suy diễn từ
token dùng chung, chưa chạy qua mười gate `pdf-so` thật. Điều kiện gỡ: chạy
nghiệm thu một ấn phẩm mặc `thep-xanh` qua làn `pdf-so`, thêm `pdf-so` vào
`lan_da_chung_minh`, và sửa lại mục 4 nếu blueprint đổi theo giới hạn khổ
giấy A4.

Hai hàng của mục 4, báo cáo khởi tạo một mã và deal pack, chưa có exemplar
thật chạm tới; blueprint của chúng suy từ bảng preset ở `SKILL.md` mục 1.B
chứ chưa qua nghiệm thu. Điều kiện gỡ: dựng một exemplar cho một trong hai
loại và chạy `npm run nghiem-thu`.

Chủ đề dẫn xuất `toi-lanh` chưa có ấn phẩm nào của thep-xanh dùng thật, dù
đã khai trong `phong-cach.json`. Điều kiện gỡ: một exemplar mở
`chu_de_mac_dinh=toi-lanh` hoặc đổi chủ đề lúc dựng, rồi nghiệm thu qua gate
CONTRAST-ALL-THEMES của làn html-song.
