# Kho style cộng đồng: chưng cất ứng viên cho phong cách báo cáo tài chính tiếng Việt

Ngày khảo sát: 2026-08-10. Mục tiêu: tìm hướng nghệ thuật thứ 5 trở đi cho repo
HT-viz-rendering, đứng cạnh 4 style đã có: `thep-xanh` (blue editorial, nghiêm túc,
tổ chức, lạnh, xem `/home/hgthinhng/HT-viz-rendering/phong-cach/thep-xanh/phong-cach.json`),
`giay-am` (giấy kem ấm, serif, accent cam đất, giọng thư gửi người thật), `nhung-toi`
(nền tối, navy vàng đồng, dark luxury) và `poster-dac` (data poster trắng đỏ mật độ cao).
Bốn style này được nêu trong `/home/hgthinhng/HT-viz-rendering/docs/specs/2026-08-09-tang-phong-cach-design.md`.

Ràng buộc kỹ thuật bắt buộc khi đánh giá khả thi: font phải nhúng được và có bản Việt
hoá đủ dấu tổ hợp (không chỉ Latin Extended mà phải phủ cả các dấu chồng như ệ, ữ, ẫ),
cấm blur và backdrop-filter, cấm gradient text (chữ tô bằng gradient qua
background-clip), bảng màu phải quy về token JSON một nguồn sự thật, và ấn phẩm phải
sống được ở cả hai làn xuất bản: html-song (HTML tự đủ, có tương tác) và pdf-so (PDF
đọc màn hình qua WeasyPrint). Với các mảng trang trí dùng gradient NỀN (không phải
gradient chữ), tôi ghi chú rủi ro riêng cho làn pdf-so vì repo có tiền lệ gradient-alpha
bị nướng bitmap khi in qua Chromium (không áp dụng trực tiếp cho WeasyPrint nhưng cùng
họ rủi ro raster).

Ba nguồn đã đọc:
1. `/home/hgthinhng/.claude/skills/huashu-design/references/design-styles.md` (40 style, đọc trọn)
2. `/home/hgthinhng/.claude/plugins/cache/frontend-slides/frontend-slides/2.1.0/skills/frontend-slides/bold-template-pack/selection-index.json` (34 template, đọc trọn) và 5 file `design.md` tiêu biểu đọc kỹ: `biennale-yellow`, `monochrome`, `cobalt-grid`, `vellum`, `signal`
3. `/home/hgthinhng/.agents/skills/html-ppt/assets/themes/` (36 file token CSS, đọc lướt tên và soi biến `--accent`/`--font-*` của toàn bộ 36 file)

7 loại ấn phẩm tài chính dùng để gắn nhãn phù hợp: bản tin thị trường, cập nhật KQKD,
báo cáo khởi tạo mã, báo cáo ngành, deal pack, tóm tắt điều hành, bản mẫu kỹ thuật.

---

## A. Từ huashu-design (design-styles.md)

| Tên gốc + nguồn | Khí chất | Khả thi với ràng buộc repo | Loại ấn phẩm phủ |
|---|---|---|---|
| **Dark Editorial** (Brittany Chiang dev portfolio), design-styles.md dòng 136-141 | Nền navy/hải quân sẫm `#0A192F` + chữ xám phiến đá + một accent xanh lục huỳnh quang duy nhất `#64FFDA`, sidebar cố định, nhãn mục lục dạng số `01/02` | Font Inter + JetBrains Mono đều có bản Việt đủ dấu. Không blur, không gradient, không shadow. Layout sidebar cố định là CSS thuần, an toàn cho html-song; với pdf-so cần bỏ sidebar sticky vì PDF không có viewport cuộn | báo cáo khởi tạo mã, bản mẫu kỹ thuật |
| **Kenya Hara White Gallery** (Cosmos/Aesop), dòng 202-207 | Nền gần trắng `#FAFAFA` + chữ đen `#0A0A0A`, masonry ảnh, độ tĩnh lặng kiểu phòng trưng bày | Font hệ thống/Inter đủ dấu Việt. Không blur, không gradient. Điểm yếu lớn nhất là hiệu ứng cuộn mượt Lenis/GSAP không dịch được sang CSS thuần, phải hạ cấp còn transition cơ bản | deal pack, tóm tắt điều hành |
| **Utility-First Colorful Docs** (Tailwind CSS Docs), dòng 164-169 | Nền trắng, dải hero xanh sky/cyan, thẻ tài liệu phân loại bằng dải màu cầu vồng (hồng/tím/lục/cam) theo nhóm chức năng | Inter + JetBrains Mono đủ dấu Việt. Không blur, không gradient text (chỉ gradient nền hero, chấp nhận được). Bố cục 3 cột thuần CSS Grid, đã có tiền lệ WeasyPrint chạy được Grid trong repo (`research/10-weasyprint-audit/FINDINGS.md` xác nhận `minmax()` không nằm trong danh sách lỗi) | bản mẫu kỹ thuật, báo cáo ngành (khi cần phân loại nhiều mã theo tag) |
| **Terminal-Core Soft-Futurism** (Cursor/Anysphere), dòng 171-176 | Than đen `#0B0D14` + chữ trắng ấm, mono là vai chính, khối lập phương đẳng cự 2.5D | JetBrains Mono/Geist Mono đủ dấu Việt. Không blur trên nền chính (chỉ có box-shadow phát sáng nhẹ, chấp nhận được nếu bỏ blur). Khối 3D đẳng cự dựng bằng CSS transform thuần, không cần WebGL | báo cáo khởi tạo mã (mã công nghệ/deep-tech), bản mẫu kỹ thuật |
| **Two-Font Consulting / Bower** (McKinsey 2019 rebrand), dòng 287-292 | Navy đậm `#051C2C`-tầm + trắng, một accent xanh lục kiểu BCG `#00805A`, tiêu đề action-title (câu khẳng định chứ không phải cụm danh từ), serif đối lập sans | Playfair Display/Fraunces (serif) + Inter (sans) đều đủ dấu Việt. Không blur, không gradient. **Cảnh báo trùng lặp**: tông navy này rất gần `thep-xanh` (chart_palette sang-lanh, accent `#2251FF`, ink `#051C2C`) - nếu chọn, phải phân biệt bằng cặp serif/sans tương phản và action-title, không chỉ đổi tông xanh | báo cáo ngành, báo cáo khởi tạo mã (nếu tách đủ khỏi thep-xanh) |
| **Diagram-Driven Isotype** (Salesforce, Otto Neurath), dòng 294-299 | Xanh doanh nghiệp, lưới icon hoá năng lực, mũi tên luồng ngang thay lời kể | Inter/IBM Plex Sans đủ dấu Việt. Mũi tên dựng bằng SVG marker hoặc clip-path thuần CSS, không cần ảnh | báo cáo ngành (giải thích chuỗi giá trị/mô hình vận hành) |
| **Diagrammatic Minimalism / Golden Circle** (Simon Sinek), dòng 301-306 | Nền trắng/nhạt + đen + một accent, một hình học mẹ duy nhất (vòng tròn đồng tâm/tam giác) chuyên chở toàn bộ khái niệm | Manrope/Jost đủ dấu Việt (Manrope chắc chắn; Jost cần kiểm dấu tổ hợp ở trọng lượng mảnh). Hình học dựng bằng border-radius/clip-path thuần | báo cáo khởi tạo mã (giải thích khung định giá/luận điểm bằng một hình duy nhất) |
| **Assertion-Evidence / Tufte** (Michael Alley, Edward Tufte), dòng 318-323 | Trắng/xám nhạt + đen + một accent tiết chế, tiêu đề là CÂU trọn vẹn chứ không phải cụm từ, một biểu đồ độc chiếm dưới tiêu đề, chú thích gắn thẳng vào điểm dữ liệu | Source Serif/Lora (tiêu đề) + Inter (thân) đều đủ dấu Việt. Zero chartjunk khớp thẳng với ECharts option() đã tách khỏi render trong repo | bản mẫu kỹ thuật, báo cáo khởi tạo mã |
| **Institutional Swiss Minimal** (Sequoia 10-page, Airbnb seed deck), dòng 325-330 | Trắng + đen xám + một accent (san hô Airbnb hoặc xanh trung tính), 3 cột đối xứng Problem/Solution, ma trận 2x2 | Inter/Helvetica Now đủ dấu Việt. Ma trận 2x2 và 3 cột đối xứng là CSS Grid/Flexbox thuần | deal pack, tóm tắt điều hành |
| **Editorial Longform** (Stripe Annual Letter, Amazon 6-page memo), dòng 332-337 | Kem/trắng ngà `#FBFAF8` + mực đậm + một accent điểm nhấn (tím Stripe), nhịp đọc ấn phẩm với thẻ dữ liệu chèn giữa dòng văn xuôi | Newsreader/Source Serif (thân) + Inter đều đủ dấu Việt. Thẻ dữ liệu inline dựng bằng float/inline-block thuần | tóm tắt điều hành, báo cáo ngành (dạng thư thường niên) |
| **Dense Research Report / Meeker style** (Mary Meeker, CB Insights, McKinsey Global Institute), dòng 346-351 | Trắng + một accent xanh sáng bậc thang `#0066FF`, gần như không chừa khoảng trắng, tiêu đề là câu kết luận, market map dạng lưới logo, chú thích nguồn cực nhỏ | Inter + IBM Plex Sans đủ dấu Việt. **Gần cùng địa hạt với poster-dac** (poster-dac trắng đỏ mật độ cao) nhưng khác giọng: đây là "tiêu đề = câu kết luận" và "market map logo" chứ không phải mật độ thị giác thuần; có thể là biến thể đáng làm riêng nếu accent đổi màu và cấu trúc tiêu đề khác hẳn | bản tin thị trường, báo cáo ngành |
| **All-Text Manifesto / Netflix-Amazon memo**, dòng 353-358 | Trắng hoặc đen thuần + một accent duy nhất (đỏ Netflix chỉ để nhấn), một trang một luận điểm, ZERO bullet ZERO biểu đồ, văn xuôi thẳng thắn kiểu memo văn hoá doanh nghiệp | Newsreader/Source Serif hoặc Inter đều đủ dấu Việt, đây là hệ hình dễ nhúng nhất trong toàn bộ khảo sát vì không có thành phần đồ hoạ nào ngoài chữ | tóm tắt điều hành (khớp gần như tuyệt đối với định nghĩa exec-summary) |
| **Sparkline Narrative / Duarte Resonate**, dòng 308-313 | Nền tối hoặc trắng + một accent cam bước ngoặt, một đường dao động SVG chạy xuyên hết chiều ngang slide, điểm chú thích gắn trên đường | Inter đủ dấu Việt. Đường sóng dựng bằng SVG path bezier thuần, có sẵn tiền lệ ECharts trong repo để tái dùng dữ liệu | bản tin thị trường, cập nhật KQKD (kể chuyện biến động theo thời gian) |
| **Neo-Swiss Billboard Editorial**, dòng 214-219 | Trắng hoặc gần đen + một accent bão hoà cao duy nhất, số khổng lồ chiếm nửa slide với tabular-nums, chia cột trái phải đối chiếu | Inter/Geist + Geist Mono (số) đủ dấu Việt. Số khổng lồ dựng bằng clamp() thuần | cập nhật KQKD (trang số liệu đầu bài, headline số) |
| **Bento Grid** (Apple Keynote/Stripe annual report chỉ số), dòng 273-278 | Nền kem/gần đen + accent thương hiệu, lưới thẻ không đều cao mỗi thẻ một luận điểm/sparkline | Inter/Geist đủ dấu Việt. `grid-template-areas` dựng lưới không đều là CSS thuần, không phụ thuộc JS | cập nhật KQKD (tổng hợp nhanh nhiều chỉ số), bản tin thị trường |

## B. Từ bold-template-pack (frontend-slides)

| Tên gốc + nguồn | Khí chất | Khả thi với ràng buộc repo | Loại ấn phẩm phủ |
|---|---|---|---|
| **Cobalt Grid**, `bold-template-pack/templates/cobalt-grid/design.md` | Giấy kem ấm `#F0EBDE` + mực cobalt điện `#1F2BE0` duy nhất, lưới giấy kẻ ô vĩnh viễn phía sau mọi slide (10% opacity), cột nhiễu pixel-glitch và mảnh QR trang trí, Newsreader serif + Hanken Grotesk + DM Mono | Ba font đều có bản Việt trên Google Fonts, cần kiểm dấu tổ hợp cho DM Mono. Không blur, không gradient chữ (lưới nền dùng `repeating-linear-gradient` không alpha cao, rủi ro raster PDF thấp nhưng vẫn nên test làn pdf-so trước khi chốt vì repo có tiền lệ gradient bị nướng bitmap). Không dùng bo góc, dễ nhúng | báo cáo ngành, bản tin thị trường (đúng giọng "trend report" hai màu risograph) |
| **Monochrome / Ivory Ledger**, `bold-template-pack/templates/monochrome/design.md` | Giấy kem `#FAFADF` + mực đen duy nhất, KHÔNG có accent màu nào, Jost siêu mảnh (trọng lượng 200) làm tiêu đề + Lora chữ nghiêng cho trích dẫn + JetBrains Mono cho nhãn | Lora và JetBrains Mono đủ dấu Việt; Jost ở trọng lượng 200 cần kiểm riêng vì nét siêu mảnh dễ vỡ dấu tổ hợp tiếng Việt khi render nhỏ. Không blur, không gradient, bo góc duy nhất 16px cho thẻ | báo cáo khởi tạo mã, deal pack (khắc khổ tuyệt đối tạo cảm giác nghiêm cẩn) |
| **Blue Professional**, selection-index.json dòng 95-117 | Giấy kem + accent cobalt điện, chuyên nghiệp hiện đại, điềm tĩnh | Không đọc design.md đầy đủ (chỉ metadata), font chưa xác định cụ thể. **Trùng lặp cao với thep-xanh** vì cùng họ xanh-trên-nền-sáng; đáng cân nhắc CHỈ nếu nền kem thay cho nền trắng tạo đủ khác biệt | báo cáo ngành, cập nhật KQKD (nếu tách đủ khỏi thep-xanh) |
| **Editorial Forest**, selection-index.json dòng 315-338 | Xanh rừng + hồng bụi + kem ấm, Source Serif 4, tâm trạng khai báo rõ là "quarterly review" | Source Serif 4 đủ dấu Việt. Không blur, không gradient theo mô tả metadata (cần đọc design.md đầy đủ trước khi triển khai thật để xác nhận không có hiệu ứng ẩn) | cập nhật KQKD (tên gọi mood khớp thẳng use case) |
| **Signal**, `bold-template-pack/templates/signal/design.md` | Nền đôi luân phiên: navy sâu `#1C2644` và kem ấm `#F0ECE3`, một accent vàng đồng cổ điển `#C8A870` duy nhất, chữ nghiêng giữa câu tô vàng làm điểm nhấn ("Signal moment"), lưới 80px gần như vô hình phủ mọi slide tối | Source Serif 4 + DM Sans + IBM Plex Mono đều đủ dấu Việt. **Trùng lặp rất cao với nhung-toi** (navy + vàng đồng/brass là đúng công thức nhung-toi đã có) - KHÔNG nên làm style riêng, nhưng đáng mượn 2 kỹ thuật cụ thể cho nhung-toi: (a) cơ chế nền đôi navy/kem luân phiên giữa các trang thay vì toàn bài một nền tối, (b) chữ nghiêng giữa câu đổi màu accent làm cơ chế nhấn mạnh thay vì chỉ đổi độ đậm | (không đề xuất làm style mới, ghi nhận như kỹ thuật vay mượn cho nhung-toi) |
| **Vellum**, `bold-template-pack/templates/vellum/design.md` | Nền navy periwinkle đơn sắc `#2A3870` xuyên suốt (không có nền phụ, không đảo màu), chữ vàng chartreuse ấm `#E8D85C`, tiêu đề nghiêng Cormorant Garamond ở MỌI cỡ, "pin-note" mono màu xanh mòng két đóng vai chú thích ghim ở góc dưới trái mỗi trang, hoàn toàn tĩnh (không chuyển động) | Cormorant Garamond + DM Sans + Courier Prime, hai font đầu đủ dấu Việt, Courier Prime cần kiểm dấu tổ hợp. Không blur, không gradient. **Gần nhung-toi về việc dùng nền navy** nhưng khác hẳn về giọng: Vellum là luận văn tĩnh lặng độc thoại (một màu, không đảo, chữ nghiêng làm mặc định) còn nhung-toi là dark luxury có đối trọng vàng đồng kim loại; đủ khác để cân nhắc làm style riêng nếu repo cần một giọng "bài luận ghim tường" | tóm tắt điều hành (giọng luận văn tĩnh lặng, khác hẳn all-text-manifesto ở chỗ có nền màu và tiêu đề nghiêng thay vì trắng đen thuần) |
| **Studio**, selection-index.json dòng 807-831 | Nền đen + chữ vàng điện áp cao, tương phản cực đại | Font chưa xác định cụ thể (chỉ metadata). Nền đen + vàng điện có thể đọc quá "hãng sáng tạo/thời trang" cho ngữ cảnh tài chính Việt, độ nghiêm túc thấp | rủi ro thấp cho tài chính, có thể phù hợp cho trang bìa chiến dịch nội bộ, không đề xuất làm style báo cáo chính |
| **Stencil & Tablet**, selection-index.json dòng 782-806 | Giấy xương + tiêu đề cắt khuôn stencil + bảng màu đất 6 tông, cảm giác lưu trữ/khảo cổ | Font chưa xác định cụ thể. Tiêu đề stencil-cut là hiệu ứng cắt chữ phức tạp, khó tái tạo thuần CSS mà không mất bản sắc, rủi ro độ trung thực thấp khi nhúng | không ưu tiên cho báo cáo tài chính, giọng quá "viện bảo tàng" |

## C. Từ html-ppt/assets/themes (36 file token CSS)

Nhóm này chỉ là bộ token accent + font (không phải hệ thống thiết kế đầy đủ như hai
nguồn trên), nên đánh giá tập trung vào việc token này có mở ra một khí chất tài chính
mới hay không, thay vì độ sâu component.

| Tên gốc + nguồn | Khí chất | Khả thi với ràng buộc repo | Loại ấn phẩm phủ |
|---|---|---|---|
| **engineering-whiteprint**, `assets/themes/engineering-whiteprint.css` | Navy `#0a1e46` + xanh lam `#1e5ac4` + đỏ nhấn `#c42a10`, hiển thị JetBrains Mono, giọng bản vẽ kỹ thuật/whiteprint | JetBrains Mono + Inter đều đủ dấu Việt. Không blur, không gradient trong biến đọc được. Tên gọi khớp thẳng loại ấn phẩm "bản mẫu kỹ thuật" | bản mẫu kỹ thuật (khớp tên gọi trực tiếp) |
| **blueprint**, `assets/themes/blueprint.css` | Chữ trắng/xanh cyan nhạt/cam trên nền tối kiểu bản vẽ kiến trúc, JetBrains Mono/IBM Plex Mono cho cả hiển thị lẫn thân | Hai mono đều đủ dấu Việt. Cùng địa hạt blueprint như engineering-whiteprint, chỉ nên chọn MỘT trong hai để tránh trùng | bản mẫu kỹ thuật (biến thể tối hơn engineering-whiteprint) |
| **academic-paper**, `assets/themes/academic-paper.css` | Navy `#1a3a7a` + đỏ tối `#8a1a1a`, hiển thị bằng Latin Modern Roman/Playfair Display | Playfair Display đủ dấu Việt, nhưng **Latin Modern Roman là font gắn với LaTeX/Computer Modern, không phải Google Fonts chuẩn và độ phủ dấu Việt không chắc chắn** - cần thay bằng Playfair Display hoặc Spectral (đã có sẵn trong repo) nếu chọn hướng này | báo cáo khởi tạo mã (giọng học thuật nghiêm cẩn) |
| **japanese-minimal**, `assets/themes/japanese-minimal.css` | Đỏ `#d93a2a` + vàng đồng nhạt `#c9a961`, Noto Serif SC tối giản kiểu Nhật | Cảnh báo quan trọng: Noto Serif SC là font tối ưu cho chữ Hán giản thể, KHÔNG phải giải pháp chính cho tiếng Việt - phải thay hiển thị chính bằng Spectral hoặc Playfair Display có dấu Việt đầy đủ, chỉ giữ Noto Serif SC làm fallback nếu có xen chữ Hán. Không blur, không gradient | deal pack, tóm tắt điều hành (tối giản có điểm vàng đồng, khác nhung-toi vì nền sáng chứ không tối) |
| **midcentury**, `assets/themes/midcentury.css` | Mù tạt `#d4902a` + xanh mòng két `#2a7a7f` + gạch nung `#c7502a`, ba tông ấm đối lập, hiển thị Playfair Display | Playfair Display + Inter đều đủ dấu Việt. Bảng ba màu ấm khác hẳn cam đất đơn sắc của giay-am, tạo được nhiều tính cách hơn mà vẫn giữ tông ấm | báo cáo ngành (khi cần nhiều tính cách hơn giay-am nhưng vẫn giữ hơi ấm) |
| **news-broadcast**, `assets/themes/news-broadcast.css` | Đỏ `#e11d2d` + đen + vàng `#ffd100`, hiển thị Oswald (chữ hẹp kiểu băng chạy tin) | Oswald có bản Việt đủ dấu. Không blur, không gradient. Tên gọi và bảng màu khớp thẳng giọng "tin nóng/ticker" | bản tin thị trường (khớp tên gọi trực tiếp, giọng ticker/breaking-news) |
| **sharp-mono**, `assets/themes/sharp-mono.css` | Đen tuyệt đối `#000000` + đỏ nhấn `#ff2200`, hiển thị Archivo Black cực đậm | Archivo Black đủ dấu Việt. **Gần địa hạt poster-dac** (cũng đen/đỏ độ tương phản cao) nhưng đậm hơn nhiều nhờ Archivo Black chiếm trọn không gian chữ, có thể là biến thể "hét to hơn" của poster-dac chứ không phải style độc lập | không ưu tiên làm style riêng, ghi nhận như biến thể của poster-dac |
| **swiss-grid**, `assets/themes/swiss-grid.css` | Đỏ `#d6001c` + đen + xám, Helvetica Neue | **Trùng lặp cao với poster-dac** (cùng công thức đỏ-đen-trắng độ tương phản cao kiểu Thuỵ Sĩ) | không đề xuất, trùng poster-dac |
| **corporate-clean**, `assets/themes/corporate-clean.css` | Navy `#0a2540` + xanh lam `#1d4ed8`, Inter | **Trùng lặp cao với thep-xanh** | không đề xuất, trùng thep-xanh |
| **editorial-serif**, `assets/themes/editorial-serif.css` | Nâu đỏ đất `#8a2a1c` + cam đất `#c97a4a`, Playfair Display | **Gần như chính là công thức giay-am** (serif + cam đất ấm) | không đề xuất, trùng giay-am |
| **glassmorphism**, `assets/themes/glassmorphism.css` | Xanh/tím nhạt trên nền kính mờ, hiệu ứng backdrop-filter | **Vi phạm trực tiếp luật cấm blur/backdrop-filter của repo** | loại bỏ hoàn toàn |
| terminal-green, cyberpunk-neon, vaporwave, y2k-chrome, retro-tv, dracula, nord, tokyo-night, rose-pine, catppuccin-mocha/latte, gruvbox-dark, solarized-light | Các theme dev-tool tối hoặc theme trang trí retro/Y2K | Font kỹ thuật đủ dấu Việt hầu hết, nhưng khí chất neon/retro/pastel không khớp đăng ký nghiêm túc của báo cáo tài chính Việt Nam theo 4 style đã có | không đề xuất cho báo cáo tài chính chính thống |

---

## Top 5 đề cử

1. **Cobalt Grid** (`bold-template-pack/templates/cobalt-grid/design.md`) - hệ hai
   màu kem-cobalt với lưới giấy kẻ ô vĩnh viễn là một khí chất hoàn toàn chưa có trong
   4 style hiện tại (không trùng xanh của thep-xanh vì cobalt bão hoà cao hơn và có
   lưới nền làm nền tảng thị giác, không trùng poster-dac vì không phải đỏ-trắng mật
   độ cao mà là giọng "trend report" risograph điềm tĩnh hơn), khớp trực tiếp báo cáo
   ngành và bản tin thị trường.

2. **All-Text Manifesto / Netflix-Amazon memo** (design-styles.md dòng 353-358) - repo
   hiện chưa có một giọng "chữ thuần, không biểu đồ, một trang một luận điểm" nào, mà
   đây đúng là định nghĩa cấu trúc của tóm tắt điều hành; đồng thời đây là hệ hình rẻ
   nhất để nhúng vì không có thành phần đồ hoạ nào ngoài kiểu chữ và một accent.

3. **engineering-whiteprint** (`assets/themes/engineering-whiteprint.css`) - loại ấn
   phẩm "bản mẫu kỹ thuật" hiện chưa có style nào phủ trực tiếp trong 4 style đã có, và
   giọng bản vẽ kỹ thuật (navy/lam/đỏ nhấn, mono làm hiển thị) là một đăng ký thị giác
   rõ ràng khác biệt với cả bốn.

4. **Monochrome / Ivory Ledger** (`bold-template-pack/templates/monochrome/design.md`)
   - đây là style duy nhất trong toàn bộ khảo sát hoàn toàn không có accent màu nào,
   một sự khắc khổ mà cả 4 style hiện tại đều không chạm tới (thep-xanh có xanh,
   giay-am có cam, nhung-toi có vàng đồng, poster-dac có đỏ); khắc khổ này tự thân là
   tín hiệu nghiêm cẩn phù hợp báo cáo khởi tạo mã hoặc deal pack.

5. **Editorial Forest** (selection-index.json dòng 315-338) - tâm trạng khai báo ngay
   trong metadata nguồn là "quarterly review", khớp thẳng loại ấn phẩm cập nhật KQKD;
   bảng màu xanh rừng/hồng bụi/kem ấm chưa xuất hiện ở bất kỳ style nào trong 4 style
   hiện có, cần đọc design.md đầy đủ của template này (hiện chỉ có metadata) trước khi
   triển khai thật.
