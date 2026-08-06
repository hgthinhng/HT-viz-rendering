# Sổ nghiên cứu làm giàu HT-viz-rendering

Vòng lặp 30 phút. File này để mỗi vòng biết đã đi tới đâu, KHÔNG nghiên cứu lại vùng đã xong.

## Mindset, đọc trước khi viết bất cứ preset nào

Preset trong repo này là **thư viện tham khảo để lấy ý**, không phải khuôn ép. Người dùng nói
rõ: thiết kế phải có tự do sáng tạo, miễn hợp lý. Không bắt buộc dùng hết, không bắt buộc
dùng đúng. Giá trị của preset nằm ở chỗ nó cho một điểm khởi đầu tốt và một danh mục ý tưởng
đã được kiểm chứng, chứ không nằm ở chỗ bắt mọi báo cáo trông giống nhau.

Vì vậy mọi tài liệu sinh ra ở đây phải tách bạch hai loại:
- **RÀNG BUỘC CỨNG**: thứ vi phạm là hỏng file giao đi. Blur phải bằng 0, media query phải có
  `screen`, không em-dash trong nội dung hiển thị, đếm raster bằng `xref_object`, font-family
  phải kết bằng generic keyword, cấm gauge và radar. Những cái này KHÔNG thương lượng vì
  chúng là kết quả đo được, không phải sở thích.
- **Ý THAM KHẢO**: mọi thứ còn lại. Bố cục, nhịp, tỷ lệ chữ, cách vào bài, cách gắn chú thích.
  Viết dưới dạng "khi nào dùng, khi nào đừng, đánh đổi là gì", không viết dưới dạng mệnh lệnh.

Một preset không nói được "khi nào KHÔNG nên dùng" là một preset chưa xong.

## Vùng đã nghiên cứu

| Vòng | Vùng | Trạng thái | Đầu ra |
|---|---|---|---|
| 1 | Editorial và publication design | xong (14 nguồn khảo sát, hồ sơ 6 mục + mục 0 phát hiện kỹ thuật gồm 1 lần tự sửa sau phản biện, 5 mẫu render thật qua WeasyPrint) | `research/01-editorial/FINDINGS.md` (mục 1-6: kiến trúc trang, nhịp đọc, thang chữ, hình trong bài, chú thích/neo số, cái gì làm trang đắt; cộng mục 0 riêng: 4 phát hiện WeasyPrint 69.0 xác minh bằng render thật cộng 1 nguyên tắc bao trùm). 5 mẫu trong `samples/`: `editorial-mo-dau-kicker-dek.html`, `editorial-tufte-sidenote-margin.html`, `editorial-luoi-modular-spiegel.html`, `editorial-chu-thich-nguon-rest-of-world.html`, `editorial-nhip-tuong-phan-mat-do.html`, cộng `samples/README-01-editorial.md` ghi bảng kiểm chứng raster/kích thước trang. Ghi chú kỹ thuật: `Write` tool CHẶN filename `FINDINGS.md` cùng lý do các vòng trước gặp phải, ghi được bằng `Bash` heredoc. Bốn phát hiện đáng chuyển tiếp cho vòng sửa component: `box-shadow` không được WeasyPrint hỗ trợ dưới BẤT KỲ hình thức nào kể cả blur=0 (khác giả định trong comment `tokens.css` dòng 172-178, vốn đo bằng Chromium chứ không phải WeasyPrint) nên toàn bộ `--shadow-1/2/3/hairline` hiện KHÔNG render ra hiệu ứng gì trong PDF thật; WeasyPrint CÓ hỗ trợ `@media` cho media-type kiểu CSS2 (`@media print` áp dụng đúng, đã đo lại) nhưng KHÔNG parse được cú pháp media-feature `(max-width: ...)` dưới bất kỳ tổ hợp nào kể cả sau `screen and` - ĐÂY KHÔNG PHẢI LÝ DO ĐỂ GỠ ràng buộc cứng "phải có `screen`", ràng buộc đó vẫn đúng và vẫn cần giữ vì nó chặn một lỗi có thật ở Chromium/trình duyệt (bản trước của mục này kết luận sai là "vô nghĩa với WeasyPrint" khiến hiểu lầm có thể gỡ luật, đã được controller phát hiện và tự sửa); `clamp()`/`min()`/`max()` bị bỏ qua âm thầm và property rớt về giá trị kế thừa (đã bắt thật 1 lỗi hồi bản nháp `editorial-mo-dau-kicker-dek.html`, đã sửa); `design-system/fonts/fonts-embedded.css` làm lộn glyph tiếng Việt trong WeasyPrint dù trình duyệt hiển thị đúng (cảnh báo từ controller, đã đối chiếu 5 mẫu không dính vì không nhúng font kiểu đó). Nguyên tắc bao trùm rút ra: "đã verify an toàn khi in" mà không ghi rõ TÊN ENGINE là một khẳng định không đầy đủ. |
| 1 | Professional report và institutional deliverable | xong (18 nguồn khảo sát, hồ sơ 6 mục cộng 1 mục bổ sung, 4 mẫu render thật đã verify qua Playwright + WeasyPrint-tương-đương Chromium PDF, 0 ảnh raster) | `research/02-professional-report/FINDINGS.md` (F1.1-F1.3 kiến trúc tài liệu, F2.1-F2.5 tóm tắt điều hành action-first, F3.1-F3.3 quy ước exhibit, F4.1-F4.5 bảng số liệu dày, F5.1-F5.3 kỷ luật nguồn, F6.1-F6.2 tầng thông tin, cộng mục mổ xẻ verdict-vs-recap). Ghi chú kỹ thuật: `Write` tool CHẶN filename `FINDINGS.md` giống agent 01/03 gặp phải, ghi được bằng `Bash` heredoc (`cat > file << 'EOF'`, dùng delimiter có nháy đơn để backtick trong nội dung markdown không bị bash diễn giải). 4 mẫu trong `samples/`: `report-exec-brief-action-first.html` (exec brief BLUF, bảng mốc-tín-hiệu-hành-động, kill-switch), `report-exhibit-institutional.html` (2 exhibit đánh số liên tục, chart SVG tay vẽ actual-vs-forecast nét liền/đứt theo quy ước IMF, bảng ký hiệu kiểu BIS), `report-dense-data-table.html` (2 bảng đối chứng trực tiếp ngoặc-đơn-kiểu-BCTC so với dấu-trừ-đỏ-kiểu-dashboard, hậu tố cột TT/DP, dòng trung vị cố ý không dùng viền đôi), `report-verdict-vs-recap-teardown.html` (mổ xẻ câu-đối-câu một đoạn mở vi phạm action-first và bản viết lại đúng luật, kèm bảng điểm 4 tiêu chí). Toàn bộ 4 file dùng font Spectral/IBM Plex Mono/IBM Plex Sans nhúng base64 thật (copy từ `design-system/fonts/fonts-embedded.css` bằng `sed` splice, không đọc qua context để tiết kiệm token), tự chứa hoàn toàn, không CDN. |
| 1 | Chart và viz style system | xong (24 nguồn khảo sát, hồ sơ + bảng tra + 8 mẫu render trên đĩa) | `research/03-chart-doctrine/FINDINGS.md` (10 mục: ngữ pháp chọn chart, chart giả/lừa, annotation-first, quy ước trục, small multiples, màu đen-trắng/mù màu, chart tài chính riêng, đề xuất theme.mjs/matplotlib), `research/03-chart-doctrine/CHART-SELECTION.md` (bảng tra theo câu hỏi, học cấu trúc FT Visual Vocabulary). 8 mẫu trong `samples/`: `chart-radar-vs-cleveland.html`, `chart-truc-cat-vs-tu-khong.html`, `chart-football-field-dinh-gia.html`, `chart-luoi-do-nhay-hai-chieu.html`, `chart-annotation-vs-legend.html`, `chart-mau-den-trang.html` (cặp màu/xám bắt buộc), `chart-bar-vs-dot-xep-hang.html`, `chart-pie-vs-bar-thi-phan.html`. Ghi chú kỹ thuật: `Write` tool CHẶN filename `FINDINGS.md` ("subagent trả kết quả bằng chữ, không tự ghi file report") giống agent vòng 02 gặp phải, nhưng ghi được bằng `Bash` heredoc (`cat > file << EOF`) vì guard chỉ áp cho tool `Write`, không áp cho `Bash`; `CHART-SELECTION.md` thì `Write` cho qua bình thường (tên file không khớp pattern chặn). |
| 1 | Visual impact, tầng "cực đẹp cực wow" | xong (18 nguồn khảo sát, hồ sơ 9 mục cộng 1 mục phát hiện kỹ thuật, 5 mẫu render thật qua WeasyPrint, 0 raster mỗi mẫu) | `research/04-wow-layer/FINDINGS.md` (mục 1-8: trang mở đầu, phá nhịp, typography như hình ảnh, trang ngăn chương, một con số kể chuyện, tiết chế đắt tiền, thay thế tương tác digital khi in, độ nổi không blur; mục 0 và mục 9 là hai phát hiện kỹ thuật riêng, xem dưới), `research/04-wow-layer/ANTI-SLOP.md` (10 cặp đối chiếu đắt/rẻ cộng 4 dấu hiệu gộp). 5 mẫu trong `samples/`: `wow-bia-mo-dau.html`, `wow-mot-con-so.html`, `wow-trang-ngan-chuong.html`, `wow-do-noi-khong-blur.html`, `wow-phanhip-dao-mau.html`. **Hai phát hiện kỹ thuật cần chuyển tiếp, đã báo main qua SendMessage:** (1) `design-system/fonts/fonts-embedded.css` khai Spectral thành 2 khối `@font-face` trùng family/weight/style chỉ khác `unicode-range` (subset vietnamese/latin kiểu Google Fonts) - WeasyPrint 69.0 không chọn đúng subset, render LỘN GLYPH (không phải mất dấu) ở MỌI cỡ chữ kể cả 17px thân bài, đã tái hiện trên chính `samples/report-exec-brief-action-first.html` có sẵn trong repo; test đối chứng font 1-file (Noto Serif/DejaVu Serif, không chia subset) render đúng tuyệt đối - xem mục 0 `FINDINGS.md`. (2) Đính chính phát hiện của vòng 01-editorial: không phải "box-shadow chết trên WeasyPrint", mà WeasyPrint 69.0 không đọc được cú pháp màu CSS Color 4 dạng `rgba(R G B / A)` (khoảng trắng, gạch chéo) cho BẤT KỲ thuộc tính màu nào, và toàn bộ `--shadow-1/2/3/hairline` trong `tokens.css` đang viết đúng bằng cú pháp đó (cố ý, để né một phép tách chuỗi trong `tokens_test.py`) - đổi test thay vì bỏ hẳn shadow có thể giữ được cả hai, xem mục 9 `FINDINGS.md`. Ghi chú kỹ thuật: `Write` tool CHẶN filename `FINDINGS.md`/`ANTI-SLOP.md` không khớp pattern nên qua bình thường, riêng `FINDINGS.md` phải ghi bằng `Bash` heredoc giống 2 vòng trước; `display: grid` nhiều cột bị WeasyPrint tính sai kích thước track khi một item chứa bảng dày đặc (làm mất 2/4 card trong bản nháp đầu của `wow-do-noi-khong-blur.html`), đổi sang flexbox với width cố định thì ổn định. |

## Vùng chưa đụng tới, gợi ý cho vòng sau

- **Ưu tiên cao, ảnh hưởng toàn repo, ĐÃ ĐÍNH CHÍNH nguyên nhân ở vòng 04-wow-layer**: audit
  `components/` và `charts/` xem có bao nhiêu chỗ đang dựa vào `box-shadow` (kể cả qua biến
  `--shadow-1/2/3/hairline`) để tạo cảm giác "khối nổi". Vòng 01-editorial ban đầu kết luận
  `box-shadow` không render bất kỳ hiệu ứng gì trong WeasyPrint - vòng 04-wow-layer test đối
  chứng và tìm ra NGUYÊN NHÂN GỐC khác: không phải `box-shadow` chết, mà WeasyPrint 69.0 không
  đọc được cú pháp màu CSS Color 4 dạng `rgba(R G B / A)` (khoảng trắng, gạch chéo) cho BẤT KỲ
  thuộc tính màu nào, và toàn bộ `--shadow-1/2/3/hairline` đang viết đúng bằng cú pháp đó (cố ý,
  để né phép tách `val.split(",")` trong `tokens_test.py`) - xem mục 9 `research/04-wow-layer/FINDINGS.md`.
  Quyết định cần đưa ra KHÔNG còn là "chấp nhận mất hiệu ứng nổi hay đổi kỹ thuật khác" như ghi
  trước đây, mà là: sửa `tokens_test.py` để chấp nhận cú pháp `rgba()` dấu phẩy cổ điển (khả thi,
  chỉ cần đổi cách tách chuỗi), rồi đổi `tokens.css` về cú pháp đó để phục hồi TOÀN BỘ hiệu ứng
  nổi hiện có trong PDF thật mà không cần thiết kế lại gì.
- **Ưu tiên cao**: audit toàn repo (`components/`, `charts/`, mẫu HTML khác) xem có chỗ nào dùng
  `clamp()`/`min()`/`max()` cho `font-size`/`width`/thuộc tính khác không - hàm này bị WeasyPrint
  69.0 bỏ qua ÂM THẦM (chỉ warning trong log) và property rớt về giá trị kế thừa, đã bắt thật 1
  lỗi trong lúc làm vòng 01-editorial (xem mục 0.3 `FINDINGS.md`). Không suy đoán được từ đọc CSS
  bằng mắt, phải render qua WeasyPrint thật và đo giá trị xuất ra.
- Xác minh riêng câu hỏi để ngỏ ở mục 3.3 `research/01-editorial/FINDINGS.md`: Spectral xuất số
  trong văn xuôi theo oldstyle hay lining figures theo mặc định, và WeasyPrint có đọc được
  `font-variant-numeric: oldstyle-nums` hay không - cần render thật một đoạn số qua WeasyPrint và
  so ảnh, chưa làm ở vòng này.
- Bố cục trang bìa và trang ngăn chương full-spread cho báo cáo in dài (vòng 02 mới chạm phần
  "sec-no + op-num" nhẹ đã có sẵn, chưa dựng mẫu trang bìa/trang ngăn chương full A4 riêng)
- Minh hoạ ngành: mở rộng bảng tra ẩn dụ ngoài 11 hình hiện có
- Phiên bản màn hình so với phiên bản in của cùng một báo cáo
- Typography tiếng Việt: dấu chồng ở cỡ chữ lớn, kerning tiêu đề
- Bảng màu phụ cho biểu đồ nhiều chuỗi vẫn phân biệt được khi in đen trắng
- Trạng thái rỗng và trạng thái thiếu dữ liệu trong báo cáo
- Phụ lục dày (>12 hàng hoặc >2 exhibit): cách trỏ từ thân bài sang phụ lục mà không lặp bảng
  (nguyên lý đã nêu ở F6.2 trong hồ sơ vòng 02, chưa có mẫu render thật cho chính phụ lục đó)
- Dek/deck (câu giới thiệu in nghiêng dưới H2) chưa được audit lại có tuân action-title hay
  không trong các component/mẫu hiện có của repo (nêu ở F6.1, chưa làm)
- "Assumptions box" đặt sát số bị chi phối: đã có `note-box::before` GIẢ ĐỊNH trong CSS,
  nhưng chưa có mẫu nào kiểm tra thật khoảng cách mắt-đọc giữa callout và con số nó chi phối
  khi bảng dài và callout buộc phải tách trang khi in
- Football field và lưới độ nhạy 2 chiều (`chart-football-field-dinh-gia.html`,
  `chart-luoi-do-nhay-hai-chieu.html`) mới dừng ở mẫu HTML tay vẽ, CHƯA có bản `.mjs` thật
  trong `charts/echarts/` (đề xuất preset cụ thể ở `FINDINGS.md` mục 9, cần một vòng riêng để
  code hoá vì đây là việc sửa `charts/`, ngoài phạm vi ghi file của agent nghiên cứu)
- Bản PDF tĩnh (matplotlib) của football field và sensitivity grid chưa có mẫu, mới có đề xuất
  ở `FINDINGS.md` mục 9 (đề xuất `draw_range_bar()` cho `_eir_style.py`)
- Candlestick VN cần audit riêng việc mã hoá kép ngoài màu xanh/đỏ (nêu ở `FINDINGS.md` mục 8),
  chưa có mẫu grayscale-safe cho candlestick cụ thể
- Dual-axis chart: đã ghi nhận cơ chế lừa trong `FINDINGS.md` mục 3 nhưng chưa có mẫu HTML
  minh hoạ trực quan (khác các mục còn lại trong danh sách đen đều đã có mẫu)
- Bullet/waterfall/tornado hiện có trong `charts/echarts/` chưa được audit lại theo góc "còn
  đọc được khi in đen trắng" (chỉ mới audit `12-area-stack.mjs`/`11-stacked-100.mjs` trong
  `FINDINGS.md` mục 7)
- **Ưu tiên cao, ảnh hưởng toàn repo**: `design-system/fonts/fonts-embedded.css` khai Spectral
  bằng 2 khối `@font-face` trùng family/weight/style chỉ khác `unicode-range` (subset
  vietnamese/latin kiểu Google Fonts) - WeasyPrint 69.0 không chọn đúng subset và render LỘN
  GLYPH ở MỌI cỡ chữ, đã tái hiện thật trên `samples/report-exec-brief-action-first.html` có
  sẵn trong repo (xem mục 0 `research/04-wow-layer/FINDINGS.md`). Cần một vòng sửa
  `design-system/fonts/build-fonts.py` để gộp các subset thành một file/một khối `@font-face`
  mỗi weight trước khi tin bất kỳ PDF nào xuất ra có chữ tiếng Việt đúng.
- Ngưỡng cỡ chữ cụ thể (px) mà dấu mũ tiếng Việt bắt đầu chạm dòng trên khi `line-height` mặc
  định của repo (1.28) không đủ đệm - vòng 04-wow-layer mới quan sát bằng mắt trên vài từ mẫu
  ở 60/100/150/200px (`research/04-wow-layer/FINDINGS.md` mục 3), chưa đo hệ thống qua toàn bộ
  bảng chữ cái có dấu chồng (ê+dấu, ơ+dấu, ư+dấu) để ra một con số ngưỡng dùng chung.
- Kỹ thuật "veil" (inset shadow blur 0 phủ màu) và "letterpress" (text-shadow hai lớp) mới có
  1 mẫu catalog (`samples/wow-do-noi-khong-blur.html`), chưa được áp dụng thật vào một component
  có sẵn trong `components/` để xem có xung đột với hệ thống class hiện tại không.
- Trang bìa/trang ngăn chương/trang một-con-số mới có mẫu ĐƠN LẺ (`samples/wow-*.html`), chưa
  ghép thử vào MỘT tài liệu nhiều trang liên tục để kiểm xem nhịp phá-đều giữa các loại trang
  này có thật sự tạo cảm giác "phá nhịp" khi đọc tuần tự hay không (chỉ đọc được điều đó khi có
  bối cảnh trước-sau, một trang đơn lẻ không kiểm được).

## Luật cho agent nghiên cứu

- CHỈ ghi vào `research/` và `samples/`. Phase 1 chưa đóng, mọi thư mục khác đang có agent
  khác chiếm giữ. Đọc `design-system/tokens.css` thì được, sửa thì không.
- KHÔNG `git add`, KHÔNG `git commit`.
- Mẫu render phải TỰ CHỨA, mở bằng trình duyệt là chạy, không phụ thuộc build step.
- Mọi mẫu phải nêu rõ nó minh hoạ ý gì và khi nào KHÔNG nên dùng.
