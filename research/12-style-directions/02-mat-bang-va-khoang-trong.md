# Mặt bằng ngôn ngữ đồ hoạ xuất bản tài chính và khoảng trống phong cách

Bối cảnh: repo đã có 4 style (blue editorial, giấy kem ấm, navy vàng đồng luxury, data poster trắng đỏ). Mục tiêu của file này là khảo ngôn ngữ đồ hoạ của các nhà xuất bản tài chính lớn, xu hướng giải thưởng thiết kế, và mặt bằng báo cáo công ty chứng khoán Việt Nam, rồi chỉ ra khoảng trống mà người đọc tài chính Việt Nam sẽ thấy vừa mới vừa đáng tin.

## 1. Ngôn ngữ đồ hoạ của các nhà xuất bản tài chính lớn

### Financial Times

FT có hai tài liệu công khai đáng chú ý: UI style guide và graphics style guide (chart-doctor), cả hai nằm trên GitHub của Financial-Times. Điểm nhận dạng mạnh nhất là nền hồng cá chua (FT Pink, một sắc salmon nhạt), được dùng xuyên suốt từ báo giấy đến web và đồ hoạ. Vì nền đã tối hơn màu trắng, mọi màu trên nền phải tối hơn nền đồ hoạ một lần nữa, khiến FT phải tự định nghĩa lại cả bảng màu: xám thường không hợp trên nền hồng nên họ chọn một sắc xám ngả be (beige-gray) cho dữ liệu không nổi bật hoặc dữ liệu thiếu. Đây là một ràng buộc màu hiếm thấy: một nền màu (không phải trắng/đen) làm gốc cho toàn bộ hệ thống màu, khá khác với 4 style hiện có trong repo (đều nền sáng trung tính hoặc trắng).

Về nguyên tắc làm biểu đồ, FT có bộ "Visual Vocabulary" (chart-doctor/visual-vocabulary), phân loại hơn 40 loại biểu đồ theo 9 mục đích kể chuyện: deviation, correlation, ranking, distribution, change over time, magnitude, part-to-whole, spatial, flow. Trong biểu đồ, FT chủ trương nhóm dữ liệu không quan trọng bằng tông màu trung tính và dành một màu nổi bật, tương phản cho dữ liệu cần thu hút sự chú ý, nói cách khác, thiết kế biểu đồ là dẫn dắt mắt người đọc qua một mạch kể chuyện, không phải tô màu mọi chuỗi số liệu.
Nguồn: https://github.com/Financial-Times/graphics-style-guide, https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary, https://www.datawrapper.de/blog/colors-for-data-vis-style-guides

### The Economist

The Economist có "Economist Style Guide" công khai với một màu đỏ đặc trưng gọi là Econ Red (#E3120B), dùng cho tiêu đề đầu trang và ô màu logo. Các màu phụ là đỏ nhạt (#FF6B6B, #FF9999) hoặc xám (#999999, #BBBBBB); nền là trắng, lưới ngang dày màu trắng trên nền xám nhạt. Font chữ là ITC Officina Sans; tiêu đề biểu đồ to đậm 18-22px màu đen, phụ đề bán đậm 9-11px. Điểm đặc trưng nhất của Economist không phải ở màu mà ở cấu trúc nội dung: tiêu đề biểu đồ luôn là một câu khẳng định ý chính bằng ngôn ngữ đơn giản (không phải tên trục), nhãn trục Y đặt bên phải thay vì bên trái, và một ô vuông đỏ đặc thay logo ở góc trên. Triết lý được phát biểu rõ: "tiêu đề là ngôi sao của mọi biểu đồ", nói thẳng insight, không mô tả dữ liệu.
Nguồn: https://fountn.design/resource/the-economist-visual-style-guide/, https://medium.com/@aecharts/how-to-create-the-economist-style-charts-f2052ba6d6d3

### Bloomberg

Không có một "style guide" công khai chi tiết như FT/Economist, nhưng ngôn ngữ thị giác của Bloomberg được định hình bởi hai thế giới song song: Bloomberg Terminal (nền đen/gần đen, chữ màu hoặc amber trên nền tối, font monospace, mật độ thông tin cực cao, không trang trí) và Bloomberg Graphics/Businessweek (đồ hoạ báo chí màu sắc rõ ràng, thường dùng một màu nhận diện mạnh trên nền trắng cho từng bài, phong cách "biz-editorial" chứ không phải terminal). Điểm đáng chú ý cho khảo sát này: mỹ học "terminal", nền tối, chữ mono, accent màu neon cho tăng/giảm, đang trở thành một trend riêng trong thiết kế dashboard tài chính 2025-2026 (xem mục 2), tách biệt hẳn với 4 style nền sáng hiện có trong repo.
Nguồn: https://www.bloomberg.com/graphics, https://www.bloomberg.com/ux/

### McKinsey và BCG

McKinsey dùng nguyên tắc "high contrast": bảng màu ít (2-3 màu chính cộng với các sắc xám), đối lập màu xanh lá đậm/xanh teal (khoảng #034641) với trắng và xám ấm (#9B9B9B), chữ đen trên nền trắng. Typography tương phản giữa một font có cá tính (Bower) và một font sạch, trung tính (Theinhardt); tránh in nghiêng, gạch chân, nhiều font, chỉ dùng đậm để nhấn mạnh. Đây là một công thức "sang trọng bằng sự tối giản" rõ ràng, khác với phong cách "nhiều chi tiết trang trí" thường thấy ở báo cáo consulting giá rẻ.

BCG gần đây làm mới nhận diện: một sắc xanh lá duy nhất, đậm và cường độ cao, đặt trên nền trắng thuần, tạo cảm giác tự tin và dễ nhận diện. Logo, font riêng, hệ thống màu bổ trợ và hệ thống xuất bản được làm đồng bộ để đạt tính nhất quán xuyên suốt. Cả McKinsey và BCG đều chọn hướng "ít màu, nhiều khoảng trắng, tương phản mạnh" thay vì "nhiều màu, nhiều biểu đồ chen đầy trang".
Nguồn: https://poesius.com/blog/consulting-slide-design-mckinsey-bcg-bain-guide, https://www.red-dot.org/project/mckinsey-company-40709, https://metadesign.com/en/work/bcg

## 2. Xu hướng giải thưởng thiết kế annual report 2024-2026

Các giải lớn (Red Dot Brands & Communication, ARC Awards, iF Design Award) không công bố một "bảng màu chuẩn" nhưng từ các bài tổng hợp xu hướng 2026 và các dự án đoạt giải có thể rút ra vài hướng rõ:

- Nền tảng: đang chuyển từ "báo cáo đẹp để trưng bày" sang "báo cáo đọc được thật", lưới bố cục cứng nhắc (rigid grid) đang được thay bằng typography "vượt khỏi lưới", ảnh chụp thoát khỏi khung dự đoán được, và chủ nghĩa tối giản được khẳng định lại bằng sự tự tin thay vì sự giản lược.
- Màu sắc: xu hướng nghiêng về các gam pastel tinh tế (neo-mint), tông màu bão hoà mạnh dùng làm accent, và bảng màu lấy cảm hứng từ thiên nhiên/đất. Pantone chọn Cloud Dancer (một màu trắng ngà trung tính, dịu hoà) làm Color of the Year 2026, báo hiệu xu hướng dùng một nền trung tính, ấm áp làm phông, rồi thả một vài màu accent bão hoà cao thay vì phủ đầy màu khắp trang.
- Với báo cáo thiên về ESG/bền vững: màu đất, gradient lấy cảm hứng từ thiên nhiên, ảnh chụp thực tế từ hiện trường thay vì ảnh stock.
- Về khả năng tiếp cận: các bài hướng dẫn 2026 nhấn mạnh typography dễ đọc, bảng màu tương phản cao, và cấu trúc điều hướng nội dung rõ ràng, tức là "đẹp" không còn được tách rời khỏi "dễ đọc/accessible".
- Một ví dụ giải Red Dot Grand Prix 2025 đáng chú ý là "Gewobag Online Annual and Sustainability Report", báo cáo thường niên dạng web tương tác (không còn là file tĩnh), phản ánh dịch chuyển chung sang báo cáo online-first có tính tương tác, phù hợp với hướng "html-song" mà repo đang theo.
Nguồn: https://www.blackboxdesign.com.au/designing-annual-reports-that-investors-actually-read-key-trends-for-2026/, https://ethicaldesign.co/annual-report-design-trends-for-2026/, https://www.red-dot.org/magazine/award-ceremony-bcd-25, https://sagedesigngroup.biz/the-2026-visual-trends-report-what-colors-fonts-and-styles-will-dominate-brand-identity/

## 3. Mặt bằng báo cáo công ty chứng khoán Việt Nam

Kiểm tra trực tiếp vài file PDF báo cáo phân tích công khai của các công ty chứng khoán (CTCK) lớn cho thấy một mô hình lặp lại khá rõ:

- Một báo cáo khởi tạo (initial report) của SHS về cổ phiếu TCB được làm bằng Canva, 29 trang khổ A4, nhiều lớp hình ảnh/mask, tức là được dựng bằng công cụ thiết kế slide/marketing phổ thông, không phải hệ thống xuất bản chuyên dụng. Kết quả thị giác gần với tài liệu marketing/slide thuyết trình hơn là ấn phẩm báo chí.
- Một báo cáo doanh nghiệp của Vietcap (VCI) dùng tổ hợp font mặc định của Microsoft Office: Calibri làm nội dung chính, Open Sans cho tiêu đề, Arial hỗ trợ, Times New Roman cho một số yếu tố, đặc trưng của file được soạn trên Word/Excel rồi xuất PDF, không có bộ nhận diện typography riêng.
- TCBS phát hành lại nguyên bản báo cáo của HSC (dán "Powered by FactSet, RMS Partners" ở đầu trang), cho thấy một phần không nhỏ báo cáo lưu hành trên thị trường là sản phẩm OEM/white-label giữa các CTCK, không phải thiết kế riêng cho từng thương hiệu.
- Điểm sáng duy nhất phá vỡ khuôn mẫu này là cuộc rebrand năm 2023 của VCSC thành Vietcap: logo tam giác xanh lá sáng (bright green), font FK Grotesk Neue, đặt làm mũi tên số mũ (exponent) tượng trưng cho tăng trưởng, lấy cảm hứng trực tiếp từ "màu xanh của bảng giá chứng khoán". Đây là nhận diện thương hiệu (logo/marketing), chưa thấy áp dụng đồng bộ vào chính các báo cáo phân tích (vẫn dùng Calibri/Open Sans như ví dụ trên).
- Một chi tiết văn hoá quan trọng cần lưu ý khi thiết kế cho độc giả Việt, đã kiểm chứng lại qua trang hướng dẫn đọc bảng giá của DNSE: quy ước màu trên bảng giá chứng khoán Việt Nam thực chất CÙNG CHIỀU với chuẩn quốc tế, xanh lá là TĂNG giá, đỏ là GIẢM giá, không hề đảo ngược. Điểm đặc thù thật sự không nằm ở chiều xanh/đỏ mà nằm ở việc bảng giá Việt Nam dùng một bộ NĂM màu chứ không phải hai: thêm vàng cho giá THAM CHIẾU (đóng cửa phiên trước, không đổi), tím cho giá TRẦN (mức cao nhất được phép khớp trong phiên), và xanh dương cho giá SÀN (mức thấp nhất được phép khớp trong phiên). Ba trạng thái tham chiếu/trần/sàn này không có tương đương trong hệ hai màu tăng/giảm (green/red) của FT, Economist hay Bloomberg, vì các sàn quốc tế mà các nhà xuất bản đó phục vụ không có biên độ dao động giá cứng theo phiên kiểu HOSE/HNX/UPCOM. Một khoảng trống phong cách thực sự dành riêng cho độc giả Việt Nam là mã hoá đủ bộ năm trạng thái này thành ngôn ngữ thiết kế nhất quán trong ấn phẩm, không chỉ dừng ở hai màu tăng/giảm mà các style nhập khẩu từ nước ngoài mặc định dùng.
Nguồn: https://www.dnse.com.vn/hoc/cac-mau-trong-bang-gia-chung-khoan

Nhìn chung, mặt bằng báo cáo phân tích CTCK Việt Nam hiện tại nằm trong một dải hẹp: nền trắng, bảng số dày đặc, font mặc định Office (Calibri/Arial/Times New Roman), bố cục kiểu slide Canva hoặc kiểu Word-xuất-PDF, ít hoặc không có hệ thống lưới/typography riêng, logo CTCK đặt góc trên nhưng không có ngôn ngữ màu/hình nhất quán xuyên tài liệu. Đây chính là khoảng trống lớn nhất: chưa có CTCK/nhà xuất bản tài chính Việt nào đang vận hành một hệ thống thị giác ở mức độ FT/Economist/McKinsey.
Nguồn: https://www.shs.com.vn/Sites/QuoteVN/SiteRoot/reportattach/20250805_114912_TCB%20Initial%20report.pdf, https://funan.com.vn/upload/media/LocalNews/16032026/VCI%20Company%20report%20-%20Vietcap%20Securities%20JSC%20(VCI)%20Final.pdf, https://www.tcbs.com.vn/documents/10181/757092/TCBS-Report-19-Aug-25-EN_byHSC.pdf, https://www.vietcap.com.vn/en/news/press-release-viet-capital-securities-joint-stock-company-officially-rebrands-to-vietcap-securities-joint-stock-company-hose-vci, https://www.brandcoat.net/case-study/vietcap

## Khoảng trống phong cách xếp hạng

1. **Nền màu tinh tế kiểu FT (không phải trắng, không phải kem ấm) làm nền cho báo cáo dài hạn.** Cả 4 style hiện có và toàn bộ mặt bằng CTCK Việt đều dùng nền trắng hoặc gần trắng; chưa ai dùng một nền màu chủ đạo (kiểu salmon FT) làm khung nhận diện riêng. Với độc giả Việt quen nhìn báo cáo trắng/xám, một nền màu tinh tế tạo cảm giác "đây là ấn phẩm có biên tập" ngay từ cái nhìn đầu, mà vẫn đủ trung tính để đọc lâu.

2. **Hệ thống năm màu của bảng giá Việt Nam (xanh lá tăng, đỏ giảm, vàng tham chiếu, tím trần, xanh dương sàn), mã hoá đủ cả ba trạng thái tham chiếu/trần/sàn thành ngôn ngữ thiết kế nhất quán, không chỉ dừng ở hai màu tăng/giảm.** Đây là khoảng trống rõ nhất và gần với độc giả nhất: hiện tại không CTCK nào mã hoá đồng bộ cả năm trạng thái này vào toàn bộ ấn phẩm (tiêu đề, callout, icon xu hướng) mà chỉ dùng hai màu tăng/giảm như các hệ thống quốc tế; trong khi phản xạ đọc bảng giá hằng ngày của người Việt đã quen nhận diện đủ năm trạng thái, một style tận dụng đúng bộ năm màu này (đặc biệt là trần/sàn, hai trạng thái mang tính kịch tính mà báo cáo phân tích thường phải nói tới) sẽ vừa quen mắt vừa khác biệt với mọi mẫu quốc tế nhập khẩu.

3. **Mỹ học "terminal": nền tối, chữ mono, accent neon cho tăng/giảm, áp dụng cho bản html-song tương tác.** Đây là xu hướng đang lên rõ trong dashboard tài chính quốc tế 2025-2026 nhưng chưa có mặt trong 4 style hiện có (đều nền sáng) và chưa thấy CTCK Việt nào dùng. Với độc giả trẻ, quen giao diện app giao dịch (nền tối, số nhảy màu), một bản báo cáo dạng "phiên bản terminal" sẽ cảm giác vừa chuyên nghiệp vừa bắt mắt theo đúng thói quen màn hình giao dịch hằng ngày.

4. **Công thức "ít màu, nhiều khoảng trắng, một màu nhận diện duy nhất thật đậm" kiểu McKinsey/BCG, thay vì bản trang dày số liệu kiểu Canva/Excel đang thống trị thị trường CTCK Việt.** Đây là khoảng trống dễ triển khai nhất vì không đòi hỏi một bảng màu lạ (chỉ cần kỷ luật biên tập và lưới), và tạo tương phản mạnh với cảm giác "báo cáo nội bộ xuất ra vội" mà phần lớn báo cáo CTCK đang mang.

5. **Bảng màu lấy cảm hứng từ chất liệu Việt (sơn mài, lụa), đất/vàng/nâu trung tính, đặt accent vàng lá/đỏ son trầm, cho các ấn phẩm mang tính "báo cáo thường niên/di sản doanh nghiệp" thay vì "báo cáo giao dịch nhanh".** Đây là khoảng trống xa nhất với mặt bằng hiện tại (không CTCK nào đang dùng hướng này) nhưng gần với xu hướng giải thưởng quốc tế 2026 (màu đất, chất liệu tự nhiên) và tạo bản sắc riêng biệt, khó bị nhầm với report ngoại quốc dịch lại.
