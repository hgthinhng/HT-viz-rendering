# PROMPT MẪU, VẼ MINH HOẠ NGÀNH MỚI BẰNG SVG THUẦN

Dán nguyên khối trong phần "Prompt" dưới đây cho LLM (kể cả Claude ở phiên
khác), điền 4 chỗ `[NGÀNH]`, `[ẨN DỤ]`, `[MÀU ACCENT]`, `[GHI CHÚ RIÊNG]`
theo ngành cần vẽ. Đã tự test bằng chính prompt này (vẽ "nhà máy xi măng", xem `illustrations/manufacturing-cement-factory.svg`), PASS ngay vòng 1.

## Prompt (dán nguyên khối bên trong khung này)

> Bạn sẽ vẽ MỘT minh hoạ ngành bằng SVG thuần (không dùng thư viện icon,
> không dùng ảnh raster), theo đúng ngữ pháp sau. Đây không phải icon
> trang trí, đây là hình sẽ bị "mổ xẻ" bằng callout (chú thích số liệu
> neo vào từng bộ phận), nên PHẢI đủ chi tiết để có nhiều điểm neo có ý
> nghĩa.
>
> **NGÀNH CẦN VẼ**: [NGÀNH] (ví dụ: "nhà máy xi măng", "trang trại nuôi tôm")
> **ẨN DỤ VẬT LÝ DÙNG**: [ẨN DỤ] (vật thể cụ thể đại diện đúng cơ chế ngành
>, tra `metaphor-table.md` nếu chưa chắc; không dùng ẩn dụ chỉ để trang trí)
> **MÀU ACCENT MẶC ĐỊNH**: [MÀU ACCENT] (1 mã hex)
> **GHI CHÚ RIÊNG**: [GHI CHÚ RIÊNG] (đặc điểm bắt buộc phải có để ngành
> này không bị nhầm với ngành khác, ví dụ nhà máy xi măng PHẢI có lò nung
> quay (kiln) hình trụ nằm nghiêng, không chỉ ống khói)
>
> **QUY TẮC BẮT BUỘC (không thương lượng):**
>
> 1. **HỆ TOẠ ĐỘ**: `viewBox="0 0 800 500"` nếu vật thể nằm ngang,
>    `"0 0 500 640"` nếu vật thể cao/đứng. Không đặt width/height cố định
>    ngoài viewBox. Chừa lề ≥5% mỗi cạnh. Nếu hình dự kiến sẽ gắn callout ở
>    phiên sau, hãy RỘNG RÃI HƠN NỮA, chừa 20-25% viewBox mỗi bên trái/phải
>    làm khoảng trống cho hộp nhãn, đừng để silhouette chiếm hết chiều
>    ngang khung.
> 2. **SILHOUETTE TRƯỚC, CHI TIẾT SAU**: trước khi thêm bất kỳ chi tiết
>    nào, tự hỏi, nếu chỉ vẽ đường bao ngoài (không tô chi tiết bên trong)
>    và thu nhỏ về 100px, người xem có nhận ra ngay đây là [NGÀNH] không?
>    Nếu không, sửa lại tỷ lệ/khối trước khi vẽ tiếp. Dùng "module tham
>    chiếu" (đơn vị lặp nhỏ nhất, dễ nhận: 1 ô cửa sổ, 1 bao xi măng, 1 ao
>    nuôi) để suy mọi kích thước khác ra bằng bội số, không áng chừng bằng
>    mắt.
> 3. **PHÂN RÃ `<g>` CÓ TÊN**: mọi cụm ≥2 shape bọc trong
>    `<g class="ten-bo-phan">` đặt tên tiếng Anh kebab-case theo bộ phận
>    THẬT (không đặt "group1"). Thứ tự vẽ = xa tới gần: nền/trời → đất/nước
>    → khối thân chính → chi tiết nhô ra.
> 4. **NGƯỠNG SỐ LƯỢNG SHAPE**: 25-45 primitive cho vật thể chính + 10-20
>    cho môi trường (đất/nước/trời) = tổng 35-65. Hoạ tiết lặp mang tính
>    CHẤT LIỆU/MẢNG KHỐI (bao xi măng chất đống, cửa sổ toà nhà, ao nuôi
>    theo lô) được lặp nhiều hơn 7 nếu gộp trong 1 `<g>` duy nhất; hoạ tiết
>    có thể trở thành ĐÍCH CALLOUT RIÊNG (từng cái một) thì giới hạn 3-7
>    lần lặp có biến thiên màu/kích thước nhẹ.
> 5. **MÀU**: đúng 1 accent ([MÀU ACCENT]) + dải neutral CỐ ĐỊNH
>    `#1e293b`/`#475569`/`#94a3b8`/`#e2e8f0` cho phần "kết cấu" + tối đa 1
>    màu cảnh báo đỏ dùng dè xẻn. KHÔNG quá 4-5 hue riêng biệt toàn hình
>    (không tính neutral xám). Tạo khối bằng FLAT 2-TONE SHADING (mặt sáng
>    = tông gốc, mặt tối = tông gốc trộn thêm ~18-20% đen HOẶC mặt sáng =
>    tông gốc trộn thêm ~20-25% trắng), KHÔNG dùng gradient. Viền mọi
>    shape 1-1.5px màu ink (`#0f172a`) opacity ~0.85. Đặt fill chính của
>    khối "hero" qua `fill="var(--accent)"` ở cấp `<g>` cao nhất để đổi màu
>    bằng 1 biến CSS. Nếu 2 khối liền kề có màu khác nhau ở 1 đường viền
>    cong (vd hai-tông thân tàu qua mũi cong), đường ranh giới PHẢI đi
>    ĐÚNG THEO contour cong đó (tính giao điểm tham số), KHÔNG cắt bằng 1
>    hình chữ nhật thẳng, nếu không phần bị cắt cụt sẽ trông như "miếng
>    vá rời" thay vì liền khối (lỗi thật đã gặp, xem grammar.md mục 9).
> 6. **TỶ LỆ**: tỷ lệ dài:cao/cao:rộng phải khớp vật thể thật (tra trong
>    `grammar.md` mục 5 nếu vật thể tương tự đã có neo tỷ lệ, hoặc tự ước
>    lượng từ hiểu biết thật về vật thể, ĐỪNG áng chừng ngẫu nhiên).
> 7. **ĐƯỜNG CONG**: mái vòm/bồn tròn/bánh xe → dùng arc `A`. Đường hữu cơ
>    (thân tàu, đồi, sóng, khói, dây leo) → cubic `C` với control point đầu
>    gần-ngang (~35% chiều dài đoạn), control point cuối gần-dọc (~15%).
>    Khói/sóng lặp → `Q` nối chuỗi `T`, đảo dấu y mỗi đoạn.
> 8. **CẤM TUYỆT ĐỐI**: `<filter>` (mọi loại), gradient >2 stop (khuyến
>    khích KHÔNG gradient luôn), clipPath lồng nhau hoặc áp cho group >5
>    con, `<mask>`, ảnh raster nhúng (`<image>`), quá 2 cỡ chữ/1 font trong
>    nhãn gắn trực tiếp vào hình, quá 2 kiểu stroke-dasharray mỗi hình. Lý
>    do: raster hoá khi in PDF, không tương thích PowerPoint, xem
>    `grammar.md` mục 7.
> 9. **KHUNG FILE BẮT BUỘC**:
>    ```svg
>    <svg viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg" role="img"
>         style="--accent:#HEX">
>      <title>Tên ngắn tiếng Việt</title>
>      <desc>1-2 câu: vật thể là gì, minh hoạ luận điểm gì cho [NGÀNH]</desc>
>      <g class="scene">...</g>
>    </svg>
>    ```
>    KHÔNG chèn callout/số liệu vào file này, file phải "sạch" để tái
>    dùng nhiều báo cáo; số liệu gắn runtime bằng module `annotate.js`
>    riêng (xem README.md).
> 10. **TỰ KIỂM SAU KHI VẼ** (bắt buộc làm thật, không bỏ qua):
>     - Render ra PNG (playwright-core + Chromium cache, xem "Cách render"
>       trong README.md của gói này).
>     - Tự nhìn ảnh, trả lời thật: "Nhìn thu nhỏ, đây có phải [NGÀNH]
>       không, hay trông giống ngành khác/vật thể chung chung?" Nếu mơ hồ,
>       thêm ĐÚNG 1-2 chi tiết đặc trưng nhất của [GHI CHÚ RIÊNG] rồi
>       render lại, không thêm tràn lan nhiều chi tiết cùng lúc.
>     - Đếm nhanh xem có vi phạm mục 8 (cấm tuyệt đối) không.
>     - Nếu vật thể có texture lặp, kiểm ngưỡng "sơ sài/rối" ở mục 4.
>     - Báo cáo trung thực số vòng lặp đã sửa và hình còn điểm gì chưa ổn
>, KHÔNG khen lấy được.

## Ghi chú cho người điền prompt (không gửi phần này cho LLM vẽ)

- **Bản đồ quốc gia/vùng địa lý**: KHÔNG tay-gõ toạ độ đường biên từ trí
  nhớ, đã thử 2 lần và bị bác bỏ dứt khoát (đọc ra "khối amip", không ra
  hình dạng thật). Dùng `gen-vietnam-path.mjs` đi kèm gói này (hoặc viết
  script tương tự cho quốc gia khác, script đã tham số hoá qua biến môi
  trường `COUNTRY_ID`, xem comment đầu file) để lấy toạ độ THẬT từ
  world-atlas (Natural Earth) qua d3-geo + topojson-simplify, không tay-gõ
  trong bất kỳ trường hợp nào còn lựa chọn khác.
- **Cán cân/đòn bẩy** (ẩn dụ phán quyết): góc nghiêng LÀ dữ liệu, không cố
  định được trong file thư viện, phải tính lại theo công thức ghi trong
  comment đầu file `illustrations/universal-balance-scale.svg` mỗi lần
  dùng cho báo cáo khác (tilt góc khác → toạ độ 2 đầu đòn cân khác).
