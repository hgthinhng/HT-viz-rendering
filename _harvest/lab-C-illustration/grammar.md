# NGỮ PHÁP VẼ MINH HOẠ NGÀNH BẰNG SVG THUẦN (LLM tự viết tay, không công cụ vẽ)
Rút ra từ: so sánh annotated-ship.html (bản cũ, ~15 primitive, phẳng, "đồ chơi")
với reference-kimi.html khối P17 (con tàu bằng chứng, ~45 primitive) và P18
(cán cân phán quyết). Áp dụng cho 11 minh hoạ trong illustrations/.

## 1. HỆ TOẠ ĐỘ CHUẨN
- Luôn dùng viewBox, KHÔNG dựa vào width/height cố định để scale (để nhúng
  PPTX/PDF ở mọi kích thước mà không vỡ nét).
- Hai khung chuẩn:
    Ngang (vật thể nằm ngang: tàu, nhà máy, giàn khoan, bản đồ, phễu, cán cân):
        viewBox="0 0 800 500"  (tỷ lệ 8:5)
    Đứng (vật thể cao: tháp căn hộ+cần cẩu, cột điện+turbine):
        viewBox="0 0 500 640"  (tỷ lệ ~5:6.4)
- Lề an toàn: chừa >=5% viewBox mọi cạnh (ví dụ khung 800x500 thì không vẽ gì
  ngoài x=[24,776] / y=[24,476]) — chỗ này dành cho leader-line của lớp chú
  thích và để PDF/PPT crop không cắt mất chi tiết.
- Đường nền chuẩn (neo trọng lượng thị giác, vật thể không "lửng lơ"):
    Cảnh trên mặt đất: mặt đất tại y = 0.86*H (H=500 -> y=430).
    Cảnh trên mặt nước: mực nước tại y = 0.72*H (H=500 -> y=360) — mực nước
    cao hơn mặt đất vì thân tàu ngập nước ăn sâu xuống dưới đường này.

## 2. PHÂN RÃ THÀNH NHÓM <g> CÓ TÊN NGỮ NGHĨA
- Cấu trúc bắt buộc: <svg role="img"><title>...</title><desc>...</desc>
  <g class="scene">...toàn bộ hình...</g></svg>
- Không bao giờ để shape trần ở cấp cao nhất — mọi cụm >=2 shape đều bọc
  trong <g class="ten-bo-phan-that"> (đặt tên tiếng Anh kebab-case theo bộ
  phận thật: "hull", "containers", "bridge", "funnel", "waterline",
  "smokestack", "conveyor", "vault-door"...). Lý do: (a) lớp chú thích cần
  neo (anchor) vào toạ độ có ý nghĩa, dễ tra cứu lại; (b) LLM lượt sau sửa
  hình chỉ cần tìm đúng <g>, không phải đếm lại toàn bộ path.
- Thứ tự vẽ = thứ tự chiều sâu vật lý, từ xa tới gần:
  nền/trời -> mặt đất hoặc mặt nước -> khối thân chính -> chi tiết nhô ra
  (ống khói, cần cẩu, ăng-ten) -> (lớp chú thích do module riêng chèn sau
  cùng, xem mục 8).

## 3. NGƯỠNG SỐ LƯỢNG SHAPE NGUYÊN THUỶ (khi nào sơ sài, khi nào rối)
- SƠ SÀI (dưới ngưỡng): < 20 primitive cho vật thể chính. Triệu chứng: khối
  màu phẳng đơn sắc, không có chi tiết bề mặt, không có nhịp lặp lại (vd:
  tàu chỉ có 1 hàng container). Đây đúng là lỗi của annotated-ship.html bản
  cũ trong lab.
- VÙNG AN TOÀN: 25-45 primitive cho vật thể chính + 10-20 cho môi trường
  (mặt đất/nước/trời) = tổng 35-65. Đây là vùng P17 (tàu tham chiếu) đang
  đứng.
- RỐI (vượt ngưỡng): > 80 primitive (không tính chữ/chú thích), HOẶC bất kỳ
  hoạ tiết lặp nào có > 15 phần tử giống hệt nhau không biến thiên. Triệu
  chứng: nhiễu thị giác, mắt không còn phân biệt được "cái gì quan trọng".
- Luật đo bằng "thời gian đọc": người xem phải nhận ra ĐÂY LÀ CÁI GÌ (tàu,
  nhà máy...) trong <1 giây chỉ từ silhouette + 2-3 chi tiết đặc trưng, và
  tìm được đúng bộ phận sau một callout trong <2 giây kế tiếp. Nếu không đạt
  vế 1 -> thiếu chi tiết đặc trưng, thêm. Nếu không đạt vế 2 -> đang rối, gộp
  hoặc đơn giản hoá hoạ tiết lặp.
- Luật lặp lại: hoạ tiết lặp là ĐỐI TƯỢNG RỜI CÓ THỂ TRỞ THÀNH ĐÍCH CALLOUT
  RIÊNG (cửa sổ, răng bánh răng, cánh turbine, chân giàn khoan) dùng 3-7 lần
  LẶP CÓ BIẾN THIÊN NHẸ (đổi màu, đổi chiều cao, đổi offset) — đọc là "nhiều"
  mà không cần đúng số thật, tránh cảm giác lưới wireframe đều tăm tắp.
  NGOẠI LỆ "khối kết cấu" (container xếp trên tàu, gạch trên tường, cửa sổ
  toà nhà cao tầng): khi hoạ tiết lặp chỉ đóng vai trò TẠO CHẤT LIỆU/MẢNG
  KHỐI cho mắt đọc thành "đầy hàng"/"nhiều tầng" chứ KHÔNG có ý định làm
  từng cái thành đích callout riêng, được lặp nhiều hơn 7 (thực tế 12-30
  vẫn ổn) MIỄN LÀ cả cụm nằm gọn trong 1 <g> ngữ nghĩa duy nhất (vd
  class="containers") và có biến thiên màu/chiều cao để tránh lưới đều.

## 4. QUY TẮC PHỐI MÀU — 1 accent, N cấp sáng tối, KHÔNG gradient phức tạp
- Bảng màu cố định mỗi hình: 1 "ink" (near-black, #0f172a) cho viền/khối tối,
  1 "paper" (nền, thường để trong suốt hoặc #f8fafc), 1 "accent" theo ngành
  (xem bảng ẩn dụ), và một dải neutral xám CỐ ĐỊNH dùng cho phần "kết cấu"
  (thép/bê tông) bất kể accent ngành là gì:
      #1e293b (kết cấu tối) / #475569 (kết cấu vừa) /
      #94a3b8 (kết cấu sáng) / #e2e8f0 (panel/kính nhạt)
- KHÔNG BAO GIỜ dùng quá 4-5 hue riêng biệt trong 1 hình (1 accent + 1 màu
  cảnh báo đỏ dùng dè xẻn + 2-3 neutral + nền). Nhiều hue hơn -> trông như
  poster trẻ em.
- Tạo cảm giác khối KHÔNG DÙNG GRADIENT: dùng "flat 2-tone shading" — mặt
  hướng sáng (thường là mặt trên/trái) = accent gốc, mặt khuất (mặt
  dưới/phải, hoặc mặt bên) = accent làm tối đi ~18-20% (trộn thêm đen), hoặc
  ngược lại làm sáng lên ~20-25% (trộn thêm trắng) cho mặt được ánh sáng
  chiếu trực tiếp. Công thức áp dụng cho MỌI khối hộp/trụ có 2 mặt nhìn
  thấy được (thân tàu, thân nhà máy, mái, cabin) — không tự do tuỳ hứng.
- Viền mọi shape bằng nét 1-1.5px màu ink, opacity ~0.85 (không phải 1.0
  tuyệt đối, để không quá gắt) — chính đường viền này làm hình phẳng đọc
  như "sơ đồ kỹ thuật" thay vì "hình dán clipart".
- Biến màu qua CSS custom property: phần fill chính (đại diện ngành) đặt
  fill="var(--accent, #2563eb)" ở cấp <g> cao nhất của khối "hero" — đổi 1
  biến CSS là đổi tông màu toàn hình theo ngành khác nhau trong cùng báo cáo,
  không phải sửa từng shape.
- BẢNG MÀU "EDITORIAL" THAY THẾ (tuỳ chọn, đã kiểm chứng tương thích): nếu
  báo cáo cần cảm giác "tạp chí biên tập" nhất quán xuyên suốt nhiều minh
  hoạ (thay vì mỗi ngành 1 accent bão hoà rời rạc), dùng bộ 4 màu mượn từ
  kho 97 motif CFA (harvest-cfa-library/illustration-icons/MOTIF_TABLE.md):
  nền cream #F5EFE2, ink thay bằng navy #16283F, dải neutral đổi thành
  #16283F/#2F4A63/#6B8299/(nền cream), accent mặc định gợi ý teal #2F7E7A
  hoặc gold #C9A227. Đã test đổi màu logistics-container-ship.svg sang bộ này
  (xem bản test riêng trong quá trình phát triển, không kèm trong gói này — chỉ đổi 4 mã màu neutral/nền/accent mặc định của logistics-container-ship.svg) — hoà
  hợp tốt, KHÔNG xung đột với cơ chế --accent hiện có (chỉ đổi dải neutral +
  nền + accent mặc định, cơ chế swap accent theo ngành vẫn nguyên vẹn).
  Giới hạn thật: bộ màu gốc của họ đi kèm gradient nhẹ/grain/soft-shadow
  raster mà SVG phẳng không tái tạo được nếu giữ đúng luật "không gradient/
  không filter" — dùng bộ màu này cho SVG chỉ lấy được ĐÚNG 4 mã màu, không
  lấy được chất liệu bề mặt, xem mục "SVG vs raster" trong báo cáo gửi kèm.

## 5. QUY TẮC TỶ LỆ — để con tàu ra con tàu, không ra con giày
- Luật "module tham chiếu": chọn đơn vị lặp lại nhỏ nhất, dễ nhận ra nhất
  của vật thể (1 container, 1 ô cửa sổ, 1 nhịp gạch, 1 cánh turbine) làm
  MODULE, rồi suy mọi kích thước khác ra bằng bội số của module đó thay vì
  áng chừng bằng mắt. Ví dụ: module container = 60x40 -> thân tàu dài
  12-14 module, cabin cao 2.5 module. Đây là cách kỹ sư đóng tàu/kiến trúc
  thật sự lên tỷ lệ, và là đòn bẩy lớn nhất để tránh "trông sai sai": con
  người rất nhạy với tỷ lệ nhưng module hoá biến việc đó thành công thức
  thay vì cảm tính.
- Luật "silhouette trước": chặn khối silhouette NGOÀI CÙNG trước (đường bao
  thân tàu, khối nhà, chân giàn khoan) đúng tỷ lệ cuối cùng, RỒI mới thêm
  chi tiết. Nếu silhouette rỗng thu nhỏ về 100px mà không đọc ra "đây là
  tàu/nhà máy/tháp" thì thêm chi tiết sau cũng không cứu được — phải vẽ lại
  silhouette.
- Neo tỷ lệ thật (không áng chừng, chép thẳng vào code):
    Tàu: dài:cao(thân) ~ 6:1 đến 8:1
    Ống khói công nghiệp: cao:đường kính ~ 8:1 đến 10:1
    Tháp căn hộ: cao:rộng ~ 3:1 đến 5:1
    Cần cẩu tháp: cần ngang (jib) : chiều cao cột hiện rõ trên khung hình ~
      0.4-0.6:1 (jib thường DÀI hơn về số tuyệt đối nhưng cột luôn cao hơn
      hẳn nếu tính từ mặt đất — tỷ lệ trên tính TRÊN khung hình đã crop,
      không phải toàn bộ cột thật ngoài đời)
    Turbine gió: cột (chiều cao trục) : ĐƯỜNG KÍNH cánh quạt ~ 1:1 đến
      1.3:1 (tức cột : BÁN KÍNH cánh quạt ~ 2:1 đến 2.6:1 — bản nháp đầu
      tiên ghi nhầm thành cột:bán kính = 1.3:1, dựng thử ra cánh quạt to
      gần chạm mép khung, đã sửa lại đúng theo tỷ lệ turbine thật)

## 6. VIẾT PATH BEZIER CHO ĐƯỜNG CONG (thân tàu/mái vòm/ống khói/khói) MÀ KHÔNG CẦN CÔNG CỤ VẼ
- Đường cong THÂN TÀU (lồi, phình rồi thu vào mũi/lái): 1 cubic bezier mỗi
  bên, điểm điều khiển 1 kéo GẦN NGANG từ góc đầu (~35% chiều dài đoạn),
  điểm điều khiển 2 kéo GẦN DỌC vào điểm cuối (~15% chiều dài đoạn). Chính
  sự BẤT ĐỐI XỨNG này (control đầu nằm ngang, control cuối nằm dọc) làm
  đường cong đọc ra "thân tàu" chứ không phải quả trứng đối xứng.
- Đường cong "TRÒN CƠ KHÍ" (bồn chứa, mái vòm, bánh xe, ống): dùng arc `A rx
  ry ...` thay vì bezier tay — arc đảm bảo độ cong hằng số, bezier tay
  không đảm bảo trừ khi canh tangent rất kỹ. Quy tắc: NẾU đường cong phải
  "tròn đều cơ khí" -> dùng A. NẾU đường cong phải "mềm mại hữu cơ" (thân
  tàu, đồi, sóng, khói) -> dùng cubic C theo công thức trên.
- Đường cong LẶP (sóng nước, khói cuộn): bắt đầu bằng `Q` rồi nối chuỗi
  bằng `T` (quadratic tiếp tuyến mượt), đảo dấu độ lệch y mỗi đoạn:
  `M x0 y0 Q x0+w/2 y0-h x0+w y0 T x0+2w y0 T x0+3w y0` — đảm bảo lặp mượt
  hình sin chỉ với 2 số cần chỉnh (w=chu kỳ, h=biên độ), không phải canh
  tangent thủ công từng khớp nối.
- Quy tắc chung cho control point: khoảng cách control-point tới anchor xấp
  xỉ 0.45 x bán kính cong mong muốn; KHÔNG đặt control point vượt quá
  anchor điểm đối diện (gây tự cắt/vòng lặp) — kiểm tra nhanh: control
  point x/y có nằm giữa 2 anchor hay không, nếu cố tình vượt thì không quá
  20%.

## 7. CẤM TUYỆT ĐỐI VÀ LÝ DO
- CẤM <filter> (feGaussianBlur, feDropShadow, feColorMatrix...): (a) Chromium
  print-to-PDF RASTER HOÁ mọi vùng có filter đang hoạt động ở độ phân giải
  in, làm phình file và mất nét/mất khả năng search chữ (đã kiểm chứng thực
  nghiệm ngay trong lab này: case6-filterblur.html bị bẫy raster-hoá); (b)
  PowerPoint import SVG (kể cả qua đường LibreOffice/soffice) hoặc âm thầm
  bỏ filter hoặc raster hoá, KHÔNG BAO GIỜ giữ đúng filter vector; (c) filter
  render khác nhau tinh vi giữa Chromium/Skia/LibreOffice nên bản preview
  không phải bản sẽ xuất ra thật.
- CẤM gradient nhiều điểm dừng (>2 stop), và NÊN TRÁNH gradient hoàn toàn
  (dùng flat 2-tone shading ở mục 4 thay thế): gradient >~3 stop (a) thường
  bị python-pptx/LibreOffice gộp về 1 bitmap tile phẳng khi convert sang
  PPTX/EMF, (b) là nguồn lỗi kinh điển "đẹp trên Chrome, sai/vằn trên
  PowerPoint", (c) gần như không tạo khác biệt thị giác so với flat 2-tone
  ở kích thước in/nhỏ (<200px) — "ánh sáng lướt" của gradient vô hình ở cỡ
  đó nhưng cạnh 2-tone rõ ràng lại chính là cái tạo cảm giác khối.
- CẤM clipPath lồng nhau (clipPath tham chiếu clipPath khác, hoặc clipPath
  áp cho 1 group có >5 con): PowerPoint import clipPath không nhất quán —
  clip lồng thường render ra TRẮNG XOÁ HOÀN TOÀN thay vì suy biến nhẹ nhàng.
  Nếu cần cắt hình, ưu tiên vẽ THẲNG hình dạng đã-cắt-sẵn bằng path literal
  thay vì dùng clipPath.
- CẤM <mask>: cùng lý do PPTX-compat như clipPath, còn nặng hơn — mask phụ
  thuộc phép toán kênh luminance mà renderer ngoài trình duyệt (LibreOffice,
  bộ convert EMF của python-pptx) thường tính sai, ra kết quả đen kịt hoặc
  vô hình hoàn toàn.
- CẤM nhúng ảnh raster (<image> base64 hay src ngoài) bên trong minh hoạ
  "vector": phá vỡ toàn bộ lý do dùng cách này (scale vô hạn, file nhẹ, đổi
  màu theo brand) và tái tạo lại đúng vấn đề raster-phình-file mà cách này
  sinh ra để tránh.
- CẤM quá 2 cỡ chữ / 1 font-family trong nhãn chữ gắn trực tiếp vào minh
  hoạ — chữ trộn vào hình phải trông như ký hiệu kỹ thuật, không phải
  poster; để LỚP CHÚ THÍCH (module riêng, mục 8) làm chủ phân cấp chữ.
- GIỚI HẠN stroke-dasharray: tối đa 2 ý nghĩa mỗi hình (vd: nét liền = đã
  xác nhận, nét đứt = dự phóng/kế hoạch) — quá 2 kiểu nét đứt là không đọc
  được ở cỡ in.

## 8. KHUNG BẮT BUỘC MỖI FILE SVG
<svg viewBox="0 0 W H" role="img" style="--accent:#HEXCODE">
  <title>Tên ngắn tiếng Việt</title>
  <desc>Mô tả 1-2 câu tiếng Việt: vật thể là gì, dùng minh hoạ luận điểm gì</desc>
  <g class="scene">...</g>
</svg>
- Lớp chú thích (callout) KHÔNG nằm trong file .svg gốc — được module
  annotate.js chèn runtime vào 1 bản SVG đã nhúng vào trang HTML, để tách
  bạch "hình" (tái dùng nhiều báo cáo) khỏi "số liệu chú thích" (đổi mỗi
  báo cáo). File .svg trong illustrations/ vì vậy LUÔN sạch, không có callout, để làm
  thư viện gốc.

## 9. BÀI HỌC RÚT RA TỪ CHÍNH LAB NÀY (thất bại thật -> sửa thật, xem examples/example-vertical-axis-ship.html + annotate.js để đối chiếu code)
- <script type="module"> KHÔNG chạy được khi mở file HTML trực tiếp qua
  file:// (Chromium chặn CORS khi import module cùng thư mục) — mọi báo
  cáo trong pipeline này mở qua file://, không qua HTTP server, nên
  annotate.js PHẢI viết dạng IIFE + `window.Annotate` (giống quy ước
  `window.U` đã dùng trong reference-kimi.html), nạp bằng `<script src>`
  thường, không phải type="module".
- Leader-line nối thẳng 1 cubic bezier từ neo tới nhãn CHỈ an toàn khi vật
  thể thưa. Với vật thể dày đặc theo chiều dọc gần hết khung hình (con
  tàu), thử đầu ép leader đi theo "chữ L cong" bezier-2-chặng qua vùng
  trống phía trên/dưới bbox vật thể ĐẠT được "không cắt vật thể" nhưng vẫn
  SAI ở tiêu chí khác: đường quá dài/quá vòng (đo được 1 case dài 1.7x
  khoảng cách thẳng, vượt ngưỡng 1.6x chấp nhận được — xem mục dưới). Sửa
  đúng bằng cách đổi chiến lược: DỜI NHÃN ra vùng trống trước (không đụng
  đường dẫn), rồi chỉ cần 1 GÓC VUÔNG BO TRÒN NHẸ (Manhattan L, không phải
  bezier nhiều đoạn) nối neo->góc->nhãn — về mặt hình học, tuyến Manhattan
  luôn có tỷ lệ tệ nhất = √2≈1.414 so với đường thẳng, tự động nằm trong
  ngưỡng bất kỳ ≥1.414 mà không cần dò từng trường hợp. Quyết định thoát
  lên/xuống của bước "dời nhãn" vẫn phải dựa vào vị trí NHÃN (không phải vị
  trí neo như thuật toán đường dẫn) — 2 bài toán khác nhau: đường dẫn thoát
  nhanh nhất TỪ NEO, nhãn thì tìm chỗ trống GẦN NHÃN nhất.
- RÀNG BUỘC ĐỘ DÀI ĐƯỜNG DẪN: leader-line không được dài quá 1.6x khoảng
  cách thẳng neo->nhãn — nếu thuật toán né vật thể không tìm được tuyến
  thoả mãn, SỬA VỊ TRÍ NHÃN, đừng kéo dài đường. Tự kiểm bằng số đo thật
  (không chỉ tin chứng minh toán học): dùng `path.getTotalLength()` +
  điểm đầu/cuối so với khoảng cách thẳng — xem verify-path-lengths.mjs,
  kết quả đo thật trên examples/example-vertical-axis-ship.html: 7/7 callout trong khoảng
  1.15x-1.40x, dưới ngưỡng 1.6x.
- LUẬT MÀU CHO LỚP CHÚ THÍCH PHẢI CÙNG KỶ LUẬT VỚI LUẬT MÀU CỦA HÌNH GỐC
  (mục 4): bản đầu annotate.js có 5 tone (neutral/accent/good/warn/bad) ->
  7 callout dùng hết 5 màu viền khác nhau trên CÙNG 1 hình, đúng kiểu
  "traffic-light hoá" mà mục 4 đã cấm cho SVG gốc nhưng quên áp cho lớp
  chú thích. Đã rút gọn `tone` còn 3 giá trị: 'neutral' (mặc định),
  'negative' (CHỈ tin xấu/rủi ro), 'accent' (kỷ luật dùng: CHỈ 1 callout
  mỗi hình — con số quan trọng nhất). Module không ép được số lượng
  'accent' bằng code, đây là kỷ luật của người GỌI module, phải tự kiểm
  bằng mắt trước khi giao.
- Hai hình ghép bằng 2 shape riêng (fill khác nhau cho 2 phần) mà đường
  ranh giới KHÔNG THEO ĐÚNG ĐƯỜNG BAO của phần liền kề sẽ trông như "2
  khối rời nhau" dù kỹ thuật vẫn là 1 path duy nhất cho outline — case
  thật: dải sáng 2-tone của thân tàu (logistics-container-ship.svg) dùng 1 RECT
  cắt cụt đúng chỗ mũi tàu bắt đầu bo cong lên, tạo đường ranh dọc giả ở
  mũi khiến mũi trông như 1 miếng vá tối tách rời khỏi thân. Sửa: dải sáng
  phải là 1 PATH đi theo ĐÚNG contour của outline (kể cả đoạn cong), không
  phải hình chữ nhật cắt ngang tuỳ tiện — áp dụng cho MỌI khối 2-tone có
  cạnh cong (không chỉ tàu): tính giao điểm của đường cắt 2-tone với outline
  cong, đừng lấy rect thẳng đè lên.
- Bản đồ quốc gia/vùng địa lý: tay-gõ toạ độ TỪ TRÍ NHỚ đã bị bác bỏ dứt
  khoát (bản v1 và v2 đều không ra "chữ S", v2 sửa tay vẫn bị chê "phình
  sai/răng cưa bất thường"). ĐÃ THAY BẰNG QUY TRÌNH THẬT và xác nhận hiệu
  quả rõ rệt: `npm i d3-geo topojson-client topojson-simplify world-atlas`
  -> lấy geometry Việt Nam (id="704") từ world-atlas countries-50m.json ->
  `topojson-simplify` (Visvalingam's area) giảm 613 điểm gốc còn ~72 điểm
  (đã thử 118/72/50, chọn 72 — xem examples/vietnam-simplification-comparison.html) -> chỉ giữ
  polygon lục địa lớn nhất (bỏ đảo rời) -> `d3-geo.geoMercator().fitExtent`
  + `geoPath()` sinh path thật. Script tái dùng: gen-vietnam-path.mjs. Kết
  quả: nhận ra ngay "chữ S Việt Nam" — eo mảnh, đồng bằng sông Cửu Long có
  ngón tay đặc trưng, biên giới Tây Bắc lởm chởm đúng thật, thay vì "khối
  amip" của bản tay-gõ. BÀI HỌC: với BẤT KỲ hình học có sẵn dữ liệu chuẩn
  công khai (biên giới hành chính, đường bờ biển, mạng lưới giao thông),
  LUÔN ưu tiên lấy dữ liệu thật + script sinh path, KHÔNG tay-gõ toạ độ dù
  có vẻ "chỉ cần đơn giản hoá" — trí nhớ hình học của LLM không đủ chính
  xác cho việc này, ngay cả sau khi tự phê và sửa lần 2.
- CÔNG THỨC "NÉN CHO VỪA KHUNG" 1 LƯỢT LÀ BẪY: hàm resolveCollisions ban
  đầu có bước "nếu tràn cạnh dưới thì nén đều" dùng công thức
  `shrink * (arr.length - i)` — nhìn qua tưởng hợp lý nhưng hệ số bị NGƯỢC:
  phần tử CUỐI (đang gây tràn) nhận hệ số NHỎ NHẤT, phần tử ĐẦU (không
  liên quan) nhận hệ số LỚN NHẤT. Kết quả đo thật: hộp cuối cùng vẫn tràn
  16.5px dù code "trông như" đã xử lý — chỉ phát hiện được bằng cách ĐO
  bounding box thật (x/y/width/height của rect so với viewBox), không phải
  đọc code hay nhìn ảnh ở độ phân giải thường (chênh 16.5/520 quá nhỏ để
  mắt thường bắt được ở ảnh full-page). Sửa bằng thuật toán 2 lượt kinh
  điển: lượt 1 từ trên xuống đảm bảo khoảng cách tối thiểu, lượt 2 từ DƯỚI
  LÊN kẹp không vượt biên dưới — tự nhiên đúng vì lượt 2 luôn sửa ĐÚNG
  phần tử đang tràn trước (duyệt từ cuối). BÀI HỌC CHUNG: bất kỳ "công
  thức nén/co giãn tỷ lệ theo chỉ số i" nào cũng phải tự hỏi "hệ số có TĂNG
  đúng chiều với mức độ liên quan của phần tử i tới vấn đề đang sửa
  không" — rất dễ viết ra công thức đúng chiều tăng/giảm nhưng SAI chiều
  ưu tiên.
- CHỮ ĐÈ LÊN ĐƯỜNG VIỀN CÙNG MÀU: nhãn thành phố trên bản đồ (chữ màu ink
  #0f172a) bị đường viền coastline (cũng #0f172a) cắt ngang khi vị trí đặt
  tình cờ trùng — vì cả hai dùng chung 1 màu nên không có gì phân tách thị
  giác. Sửa bằng "halo": `stroke="#ffffff" stroke-width="4"
  paint-order="stroke"` trên chính thẻ `<text>` — vẽ viền trắng QUANH chữ
  TRƯỚC rồi mới tô chữ đè lên (paint-order="stroke" đảo thứ tự vẽ mặc định
  của SVG, vốn tô fill trước stroke sau). Áp dụng bất kỳ khi nào text có
  thể chồng lên hoạ tiết CÙNG TÔNG MÀU của chính minh hoạ (không chỉ bản
  đồ) — halo trắng giả định nền trang sáng màu, đổi màu halo nếu nhúng vào
  nền tối.
