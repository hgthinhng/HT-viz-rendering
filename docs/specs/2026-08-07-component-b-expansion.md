# Mở rộng nhóm B: 5 component kể chuyện còn thiếu, đặc tả thi công

Ngày chốt: 2026-08-07
Trạng thái: đặc tả, chưa viết code. Đánh số tiếp KHỐI 25 đến 29, sau 24 spec hiện có trong `components/catalog/`.
Phạm vi: 5 component do `research/13-chart-component-gap/FINDINGS.md` xác định là lỗ hổng nhóm B (component kể chuyện HTML, không phải chart). Đã đối chiếu giọng và cấu trúc với 24 spec hiện có (đọc kỹ `11-exec-qa.md`, `13-options-comparison-table.md`, `24-bonus-key-point-callout.md`), luật cứng trong `CLAUDE.md`, và biến trong `design-system/tokens.css`.

---

## 0. Kiểm tra trùng lặp trước khi thêm mới

Không có component nào trong 5 cái trùng chức năng thật với 24 spec hiện có, nhưng 4 cái cận kề đủ gần để phải chỉ rõ ranh giới ngay trong chính spec (đã viết vào mục "KHÔNG dùng" của từng file bên dưới):

- **Hộp tóm tắt điều hành (KHỐI 25)** gần `11-exec-qa` (hỏi-đáp tự do) và `24-bonus-key-point-callout` (một câu kết) nhưng KHÔNG trùng: đây là 4 ô CỐ ĐỊNH Luận điểm/Chất xúc tác/Rủi ro/Hành động, đặt cuối bài, đúng như FINDINGS đã lập luận (10/10 loại báo cáo cần, đang thủng nhất). Không đề xuất mở rộng 2 cái kia vì hình dạng 4-ô-cố-định khác hẳn cấu trúc danh sách câu hỏi lẫn cấu trúc một-câu-kết.
- **Dải thắng thua (KHỐI 27)** gần `14-before-after` (một thực thể đổi trạng thái theo thời gian) nhưng khác: nhiều thực thể chia phe cùng lúc trước MỘT biến đổi, không phải một thực thể qua hai thời điểm.
- **Ngã ba chính sách (KHỐI 28)** gần `16-process-step-chain` (chuỗi tuần tự) và Thẻ kịch bản mới (KHỐI 26, 3 nhánh có xác suất) nhưng khác: đúng 2 nhánh, có điểm rẽ chung, không bắt buộc trục xác suất.
- **Dải tự sự (KHỐI 29)** gần nhất với `07-pull-quote`, `09-note-box`, `24-bonus-key-point-callout` (đều là đoạn văn đóng khung/nổi bật). Cân nhắc kỹ có nên mở rộng cái nào trong 3 cái đó thay vì thêm mới: KHÔNG nên, vì cả 3 đều có một vai trò CHỨC NĂNG rõ (trích dẫn thật có người nói / cảnh báo-giả định-điều kiện huỷ / một câu kết tự đúc kết), còn dải tự sự là văn xuôi TRUNG TÍNH của chính tác giả, không đóng khung, không claim gì đặc biệt, mục đích duy nhất là giữ mạch đọc giữa hai exhibit. Nhét vào note-box hay key-point sẽ ép nó "đóng vai" một trong ba chức năng đó, sai bản chất.
- **Thẻ kịch bản (KHỐI 26)** không trùng `06-quad-2x2-positioning` (đó là 2D probability x impact liên tục, đây là danh sách rời rạc 3 kịch bản có tên, có xác suất và điều kiện kích hoạt).

---

## 1. Ghi chú thiết kế bổ sung theo phản hồi broadcast 4 mô hình ngoài

Hai cảnh báo dưới đây đến từ broadcast 4 mô hình ngoài (team lead chạy riêng, không thuộc phạm vi đọc ban đầu của đặc tả này). Đã đối chiếu với bản thiết kế gốc, tìm ra 4 chỗ thật sự rơi vào cảnh báo thứ nhất, và đã sửa cả 4. Cảnh báo thứ hai chỉ áp cho KHỐI 25 nên xử lý riêng ở mục 1.2.

### 1.1 Nền xám nhạt tạo khối: đổi sang bỏ nền hoặc viền trái đậm

Cảnh báo: mực laser in trên nền xám ra bẩn, nên dùng viền trái đậm thay thế thay vì tô nền tạo khối.

**Đối chiếu**: bản thiết kế gốc dùng `background: var(--paper-hi)` (giá trị `#F7F9FC`, tương đương một lớp phủ xám khoảng 2% so với giấy trắng) ở 4 chỗ: `.es-head` (thanh đầu hộp tóm tắt điều hành, KHỐI 25), `.scn-card[data-tone="base"]` (toàn bộ nền thẻ kịch bản Cơ sở, KHỐI 26), `.wl-event` (thanh mô tả biến đổi, KHỐI 27), `.pf-root` (hộp điểm rẽ, KHỐI 28).

**Có rơi vào cảnh báo không, và xử lý ra sao cho từng chỗ**:

- `.es-head`, `.wl-event`, `.pf-root`: đây là 3 thanh ngang, đã có `border-bottom: 1.4px solid var(--ink)` phân tách rõ, nền chỉ là trang trí thêm không cần thiết. **Đã bỏ hẳn khai báo `background`** ở cả 3 chỗ, giữ nguyên border-bottom. Đây là cách sửa ăn toàn, không cần viền trái vì viền trái không hợp lý về mặt bố cục cho một thanh ngang căn giữa hoặc trải hết chiều rộng.
- `.scn-card[data-tone="base"]`: đây mới đúng là trường hợp "tô nền tạo khối" theo đúng nghĩa cảnh báo nhắm tới (phủ toàn bộ diện tích thẻ, không phải một dải mỏng). **Đã bỏ `background`, thêm `border-left: 3px solid var(--ink)`** để giữ độ nổi bật của thẻ Cơ sở so với 2 thẻ Tiêu cực/Tích cực bên cạnh. Kỹ thuật này lấy nguyên từ `legal-quote` đã có sẵn trong `components.css` dòng 303 (`border-left: 3px solid var(--ink)` cộng `background: var(--paper-hi)`), chỉ khác là bỏ luôn phần nền, giữ lại phần viền.

**Một mâu thuẫn cần nói thẳng, không giấu**: `13-options-comparison-table.md` (đã đọc kỹ trước khi viết đặc tả này) ghi nguyên văn "Cột khuyến nghị được tô nền nhẹ (không dùng viền trái màu để tránh dấu hiệu 'AI slop')", tức lựa chọn NGƯỢC với khuyến nghị của broadcast 4 mô hình ở đúng trục quyết định này. Đối chiếu kỹ hơn thì đây không phải mâu thuẫn thật: quy ước "AI slop" mà tokens.css cấm (dòng 167-173, khối comment "Radius scale") là **viền trái MÀU THƯƠNG HIỆU cộng bo tròn lớn** (ví dụ viền trái xanh accent, bo góc 12-13px, đúng kiểu thẻ SaaS dashboard), không phải viền trái nói chung. `legal-quote` đã dùng viền trái màu `--ink` (mực đen trung tính, không phải accent) từ trước, và hệ thống vẫn giữ góc gần vuông xuyên suốt (radius-2 = 3px). Border-left ở `.scn-card[data-tone="base"]` dùng đúng `var(--ink)`, không dùng `var(--accent)`, và không đổi bán kính góc, nên không rơi vào đúng combo bị cấm. Ghi lại rõ ràng ở đây để người thi công không phải tự suy luận lại nếu sau này có ai hỏi "sao chỗ này dùng viền trái mà chỗ kia lại cấm".

### 1.2 Giới hạn cứng độ dài nội dung mỗi ô, riêng cho KHỐI 25

Cảnh báo: hộp dài quá nửa trang bị đẩy NGUYÊN khối sang trang sau (vì `.exec-summary` khai `break-inside: avoid`), để lại khoảng trắng lớn ở cuối trang trước. Đây đúng là lớp lỗi mà `research/08-synthesis/FINDINGS.md` mục 3.1 đã ghi nhận thật ("Tràn trang vô hình khi ráp nhiều khối lại, dù mỗi khối 'trông vừa 1 trang'"): một khối trông ổn khi xem riêng lẻ chỉ lộ ra vấn đề khi ráp vào một tài liệu có ngân sách trang thật.

**Tính toán cụ thể**: `@page` trong CLAUDE.md khai `margin: 16mm 14mm`, A4 cao 297mm, vậy vùng nội dung cao 297 - 2×16 = 265mm. Nửa trang ≈ 132mm. Với layout 2 cột của `.exec-summary` (mỗi cột rộng khoảng 85mm ở khổ A4 trừ margin), một ô văn xuôi (Luận điểm/Hành động) giữ dưới khoảng 3 câu (tương đương 4-5 dòng ở cột đó) và một ô danh sách (Chất xúc tác/Rủi ro) giữ tối đa 3 mục, mỗi mục tối đa khoảng 2 dòng, thì tổng chiều cao cả khối (thanh đầu + 2 hàng ô) rơi vào khoảng 90-100mm, có dư biên an toàn dưới ngưỡng nửa trang 132mm. Vượt quá các mốc này (ví dụ một ô văn xuôi kéo dài 6-7 dòng) là dấu hiệu cần cắt bớt nội dung trước khi merge, không phải để mặc rồi hy vọng WeasyPrint tự lo.

**Đã tự kiểm lại ví dụ HTML của chính KHỐI 25** (mục 2.3 bên dưới) theo đúng giới hạn này và cắt gọn 2 câu dài nhất ở ô Luận điểm và 2 mục dài nhất ở ô Chất xúc tác/Rủi ro so với bản nháp ban đầu để làm mẫu tuân thủ đúng ngay từ đầu, không chỉ ghi luật suông.

---

## 2. KHỐI 25 · TÓM TẮT ĐIỀU HÀNH BỐN Ô

File đề xuất: `components/catalog/25-exec-summary-quad.md`

### 2.1 File catalog

```markdown
# Đội tàu lãi vận hành, lỗ chu kỳ nhiên liệu

`KHỐI 25 · TÓM TẮT ĐIỀU HÀNH BỐN Ô`

## Mô tả / khi nào dùng

Trả lời: "Nếu người đọc chỉ đọc đúng một khối trước khi rời báo cáo, khối đó nói gì?" Bốn ô cố định Luận điểm / Chất xúc tác / Rủi ro / Hành động, luôn đặt CUỐI bài, đúng một lần. Giới hạn cứng để tránh đẩy nguyên khối sang trang sau (khối dùng `break-inside: avoid`): ô Luận điểm/Hành động tối đa khoảng 3 câu, ô Chất xúc tác/Rủi ro tối đa 3 mục mỗi ô. Khác `11-exec-qa` (nhiều cặp hỏi-đáp tự do, giọng người đọc hỏi) và `24-bonus-key-point-callout` (một câu kết tự đúc kết, không có cấu trúc con). KHÔNG dùng giữa bài hoặc lặp lại nhiều lần trong cùng báo cáo: đặt quá 1 lần biến nó thành `24-bonus-key-point-callout` rải rác nhiều điểm nhấn nhỏ thay vì một điểm chốt duy nhất ở cuối. KHÔNG dùng khi báo cáo không đủ nội dung lấp cả 4 ô: chuyển sang `11-exec-qa` dạng hỏi-đáp linh hoạt hơn, không ép khung 4 ô cố định.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="exec-summary">
  <div class="es-head">
    <div class="es-kicker">Tóm tắt điều hành</div>
    <div class="es-meta">Dữ liệu chốt 30/06/2026 · Biên soạn 05/08/2026</div>
  </div>
  <div class="es-grid">
    <div class="es-cell es-thesis">
      <div class="es-label">Luận điểm</div>
      <p class="es-text">Đội tàu vận hành ở biên lãi gộp 18 đến 20%, nhưng biên EBITDA co lại vì nhiên liệu tăng nhanh hơn giá cước. Định giá P/B 0,9 lần chưa phản ánh đội tàu trẻ hơn trung bình ngành 4 năm.</p>
    </div>
    <div class="es-cell es-catalyst">
      <div class="es-label">Chất xúc tác</div>
      <ul class="es-list">
        <li><span class="es-tag">Q4/2026</span>Đợt đóng tàu thứ hai bàn giao, thêm 2 tàu feeder, nâng công suất tuyến nội Á khoảng 12%.</li>
        <li><span class="es-tag">T3/2027</span>Hạn IMO CII giai đoạn 2 buộc 6 tàu trên 20 tuổi nâng cấp hoặc thanh lý.</li>
      </ul>
    </div>
    <div class="es-cell es-risk">
      <div class="es-label">Rủi ro</div>
      <ul class="es-list">
        <li><b>Biển Đỏ kéo dài.</b> Phí bảo hiểm chiến tranh tăng theo chu kỳ căng thẳng, ăn vào biên khai thác.</li>
        <li><b>Đội tàu già hoá cục bộ.</b> 6 tàu trên 20 tuổi chiếm 26% tổng DWT, chi phí bảo dưỡng tăng nhanh.</li>
      </ul>
    </div>
    <div class="es-cell es-action">
      <div class="es-label">Hành động</div>
      <p class="es-text">Tích luỹ dưới vùng 24.000 đồng một cổ phiếu, chốt lãi một phần quanh 30.000 đồng. Theo dõi tiến độ đóng tàu quý 4 và giá dầu FO 380 làm hai biến xác nhận luận điểm.</p>
    </div>
  </div>
</div>
```
```

### 2.2 CSS

Dán vào `components.css`, trước khối "26. ACCESSIBILITY", đặt tên phần "── 26. KHỐI 25 · TÓM TẮT ĐIỀU HÀNH BỐN Ô ───". **Đã bỏ `background` trên `.es-head` so với bản nháp đầu (xem mục 1.1)**, chỉ giữ `border-bottom`.

```css
.exec-summary { border: 1.4px solid var(--ink); margin: 40px 0; box-shadow: var(--shadow-1); break-inside: avoid; }
.es-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; flex-wrap: wrap; padding: 12px 20px; border-bottom: 1.4px solid var(--ink); }
.es-kicker { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
.es-meta { font-family: var(--font-mono); font-size: 9.5px; color: var(--ink-lo); }
.es-grid { display: grid; grid-template-columns: 1fr 1fr; }
.es-cell { padding: 18px 20px 16px; border-top: 1px solid var(--line); border-left: 1px solid var(--line); break-inside: avoid; }
.es-cell:nth-child(1), .es-cell:nth-child(2) { border-top: 0; }
.es-cell:nth-child(odd) { border-left: 0; }
.es-label { font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.es-label::before { content: ""; width: 14px; height: 2px; background: currentColor; }
.es-thesis .es-label { color: var(--accent-hi); }
.es-catalyst .es-label { color: var(--ink-md); }
.es-risk .es-label { color: var(--neg); }
.es-action .es-label { color: var(--warn); }
.es-text { font-size: 14px; line-height: 1.6; margin: 0; }
.es-list { margin: 0; padding: 0; list-style: none; }
.es-list li { font-size: 13px; line-height: 1.55; padding-left: 15px; position: relative; margin-bottom: 8px; }
.es-list li:last-child { margin-bottom: 0; }
.es-list li::before { content: "▸"; position: absolute; left: 0; top: 0; color: var(--ink-lo); font-size: 11px; }
.es-tag { display: inline-block; font-family: var(--font-mono); font-size: 9px; font-weight: 700; letter-spacing: .04em; color: var(--accent-hi); border: 1px solid var(--accent-soft); border-radius: var(--radius-1); padding: 0 4px; margin-right: 6px; vertical-align: 1px; }
@media screen and (max-width: 640px) {
  .es-grid { grid-template-columns: 1fr; }
  .es-cell { border-left: 0; border-top: 1px solid var(--line); }
  .es-cell:first-child { border-top: 0; }
}
```

### 2.3 Section gallery.html

```html
<section id="c25-execsummary" aria-labelledby="h-c25">
  <div class="sec-kicker">KHỐI 25 · TÓM TẮT ĐIỀU HÀNH BỐN Ô</div>
  <h2 class="sec-title" id="h-c25">Đội tàu lãi vận hành, lỗ chu kỳ nhiên liệu</h2>
  <p class="sec-note">Trả lời: "Nếu người đọc chỉ đọc đúng một khối trước khi rời báo cáo, khối đó nói gì?" Bốn ô cố định Luận điểm / Chất xúc tác / Rủi ro / Hành động, đặt cuối bài, đúng một lần. KHÔNG dùng giữa bài hoặc lặp lại nhiều lần: dùng <code>exec-qa</code> nếu cần nhiều cặp hỏi-đáp tự do hơn.</p>
  <!-- dán nguyên khối .exec-summary ở mục 2.1 -->
</section>
```

**Ngắt trang & đen trắng**: `.exec-summary` là một khối `break-inside: avoid`, tuân thủ giới hạn độ dài ở mục 1.2 để tránh bị đẩy nguyên khối sang trang sau. Bốn nhãn phân biệt bằng CHỮ (LUẬN ĐIỂM/CHẤT XÚC TÁC/RỦI RO/HÀNH ĐỘNG) chứ không chỉ bằng màu, nên mất màu khi in đen trắng vẫn đọc đúng vai trò từng ô.

---

## 3. KHỐI 26 · THẺ KỊCH BẢN

File đề xuất: `components/catalog/26-scenario-cards.md`

> **ĐÃ DUYỆT 07-08, không phải hỏi lại.** Người dùng cho phép dùng `var(--pos)` cho bản
> Tích cực. Ghi chú trong `design-system/tokens.css` đã sửa thành ba nơi được duyệt.
> Giữ nguyên phương án dự phòng bên dưới phòng khi sau này đổi ý.
>
> Ghi chú gốc lúc còn chờ: Thẻ kịch bản dùng `var(--pos)` cho viền trên và nhãn "Tích cực" (bull case). `design-system/tokens.css` dòng 30 ghi rõ `--pos` chỉ dùng CỰC TIẾT CHẾ, đúng 2 chỗ đã duyệt (statgrid trend up, risk thấp). Đây sẽ là nơi dùng thứ 3, cần operator xác nhận trước khi merge.
>
> Nếu operator TỪ CHỐI, chỉ cần đổi đúng 2 dòng sau trong CSS ở mục 3.2 (không cần đọc lại phần còn lại của đặc tả):
> - `.scn-card[data-tone="bull"] { border-top-color: var(--pos); }` → đổi `var(--pos)` thành `var(--accent)`
> - `.scn-card[data-tone="bull"] .scn-name { color: var(--pos); }` → đổi `var(--pos)` thành `var(--accent)`

### 3.1 File catalog

```markdown
# Ba kịch bản sửa đổi Thông tư 22 về trần SFL

`KHỐI 26 · THẺ KỊCH BẢN`

## Mô tả / khi nào dùng

Trả lời: "Có mấy kịch bản chính, xác suất mỗi cái bao nhiêu, và điều gì kích hoạt nó?" Đúng 3 thẻ Tiêu cực / Cơ sở / Tích cực, mỗi thẻ có xác suất, một giá trị neo (giá mục tiêu hoặc con số kết quả), và một điều kiện kích hoạt cụ thể. Xác suất ba thẻ nên cộng đúng 100%, sai số làm tròn cho phép trong khoảng 1 điểm phần trăm. KHÔNG dùng quá 3 kịch bản mỗi khối: xác suất khó cộng đúng 100% và người đọc khó giữ hơn 3 nhánh trong đầu khi quét ngang. KHÔNG dùng khi cần cả trục xác suất lẫn trục mức độ ảnh hưởng cùng lúc trên một mặt phẳng liên tục: chuyển sang `06-quad-2x2-positioning`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="scenario-cards">
  <div class="scn-card" data-tone="bear">
    <div class="scn-head">
      <div class="scn-name">Tiêu cực</div>
      <div class="scn-prob"><span class="scn-prob-num">20</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">24.500<small>đ/cp</small></div>
    <p class="scn-headline">Phương án B thay thế được chọn: giữ nguyên trần SFL 30%, đổi bằng room NSFR riêng cho bất động sản.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Chính phủ ưu tiên kiểm soát rủi ro hệ thống hơn tăng trưởng tín dụng, quyết định trước kỳ họp Quốc hội cuối năm.</div>
  </div>
  <div class="scn-card" data-tone="base">
    <div class="scn-head">
      <div class="scn-name">Cơ sở</div>
      <div class="scn-prob"><span class="scn-prob-num">50</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">29.000<small>đ/cp</small></div>
    <p class="scn-headline">Phương án A thông qua đúng dự thảo: nâng trần SFL từ 30% lên 35%, hiệu lực đầu 2027.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Dự thảo hiện hành giữ nguyên qua vòng lấy ý kiến, không có sửa đổi lớn từ Ngân hàng Nhà nước.</div>
  </div>
  <div class="scn-card" data-tone="bull">
    <div class="scn-head">
      <div class="scn-name">Tích cực</div>
      <div class="scn-prob"><span class="scn-prob-num">30</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">34.000<small>đ/cp</small></div>
    <p class="scn-headline">Phương án A thông qua kèm gói nới lỏng tiền tệ, lãi suất điều hành giảm thêm 50 điểm cơ bản.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Lạm phát duy trì dưới 3,5% cho phép nới đồng thời cả room tín dụng lẫn lãi suất.</div>
  </div>
</div>
```
```

### 3.2 CSS

```css
/* CHO DUYET: --pos dung cho data-tone="bull" la noi dung dung thu 3 ngoai 2 cho da duyet
   trong tokens.css (statgrid trend up, risk thap). Operator can xac nhan truoc khi merge,
   xem callout dau muc 3 trong file dac ta. Neu tu choi, doi 2 dong duoi day sang var(--accent). */
.scenario-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 32px 0; }
.scn-card { border: 1px solid var(--line); border-top: 3px solid var(--ink-lo); background: var(--paper); box-shadow: var(--shadow-1); padding: 16px 18px 14px; break-inside: avoid; }
.scn-card[data-tone="bear"] { border-top-color: var(--neg); }
.scn-card[data-tone="base"] { border-top-color: var(--ink); border-width: 1.4px; border-left: 3px solid var(--ink); }
.scn-card[data-tone="bull"] { border-top-color: var(--pos); }
.scn-head { display: flex; justify-content: space-between; align-items: baseline; }
.scn-name { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
.scn-card[data-tone="bear"] .scn-name { color: var(--neg); }
.scn-card[data-tone="bull"] .scn-name { color: var(--pos); }
.scn-prob { font-family: var(--font-mono); }
.scn-prob-num { font-weight: 700; font-size: 24px; }
.scn-prob-unit { font-size: 12px; color: var(--ink-lo); }
.scn-value { font-family: var(--font-mono); font-weight: 700; font-size: 19px; margin: 10px 0 8px; }
.scn-value small { font-size: 11px; font-weight: 400; color: var(--ink-md); margin-left: 3px; }
.scn-headline { font-size: 13px; line-height: 1.55; margin: 0 0 10px; }
.scn-trigger { font-size: 11.5px; color: var(--ink-md); line-height: 1.5; padding-top: 10px; border-top: 1px dashed var(--line); }
.scn-trigger-label { display: block; font-family: var(--font-mono); font-size: 9px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 3px; }
@media screen and (max-width: 700px) { .scenario-cards { grid-template-columns: 1fr; } }
```

### 3.3 Section gallery.html

```html
<section id="c26-scenario" aria-labelledby="h-c26">
  <div class="sec-kicker">KHỐI 26 · THẺ KỊCH BẢN</div>
  <h2 class="sec-title" id="h-c26">Ba kịch bản sửa đổi Thông tư 22 về trần SFL</h2>
  <p class="sec-note">Trả lời: "Có mấy kịch bản chính, xác suất bao nhiêu, điều gì kích hoạt nó?" Đúng 3 thẻ, xác suất nên cộng 100%. KHÔNG dùng quá 3 kịch bản mỗi khối; cần cả trục xác suất lẫn mức ảnh hưởng liên tục thì dùng <code>quad-2x2-positioning</code>.</p>
  <!-- dán nguyên khối .scenario-cards ở mục 3.1 -->
</section>
```

**Ngắt trang & đen trắng**: mỗi `.scn-card` là `break-inside: avoid`, cả hàng 3 thẻ có thể tràn sang trang sau nếu không đủ chỗ. Grid 3 cột auto-height theo thẻ cao nhất, nên headline giữ dưới khoảng 80 ký tự (đúng giới hạn `scenario_cards` gốc trong harvest) để 3 thẻ không lệch chiều cao quá nhiều. Đen trắng: thẻ Cơ sở tách biệt bằng viền dày 1,4px cộng viền trái 3px (khác biệt cấp xám rõ, không dựa vào nền màu), tên kịch bản luôn có chữ TIÊU CỰC/CƠ SỞ/TÍCH CỰC nên mất màu vẫn đọc đúng; nếu `--pos` bị từ chối và đổi sang `--accent`, độ tương phản đen trắng giữ nguyên vì cả hai token đều có cấp xám khác biệt rõ với `--neg`.

---

## 4. KHỐI 27 · DẢI THẮNG THUA

File đề xuất: `components/catalog/27-winners-losers-split.md`

### 4.1 File catalog

```markdown
# Ai hưởng lợi, ai chịu thiệt khi trần SFL được nới

`KHỐI 27 · DẢI THẮNG THUA`

## Mô tả / khi nào dùng

Trả lời: "Khi biến số hoặc chính sách này đổi, ai được và ai mất?" Một dòng mô tả biến đổi ở trên, hai cột liệt kê thực thể hưởng lợi và chịu thiệt ở dưới, mỗi thực thể kèm đúng một câu lý do. KHÔNG dùng khi chỉ có MỘT thực thể chuyển trạng thái theo thời gian (không phải nhiều thực thể chia phe cùng lúc): dùng `14-before-after`. KHÔNG dùng khi cần so sánh nhiều tiêu chí cùng lúc giữa các phương án loại trừ nhau: dùng `13-options-comparison-table`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="winlose">
  <div class="wl-event">
    <div class="wl-event-label">Biến số thay đổi</div>
    <div class="wl-event-text">Trần tỷ lệ nguồn vốn ngắn hạn cho vay trung dài hạn (SFL) nâng từ 30% lên 35%, dự kiến hiệu lực đầu 2027.</div>
  </div>
  <div class="wl-split">
    <div class="wl-side wl-win">
      <div class="wl-side-label">Hưởng lợi</div>
      <div class="wl-entity">
        <div class="wl-entity-name">Ngân hàng có SFL sát trần cũ (nhóm VPB, TCB)</div>
        <div class="wl-entity-why">Có thêm dư địa giải ngân trung dài hạn ngay quý đầu hiệu lực, không phải cơ cấu lại danh mục hay huy động vốn dài hạn gấp.</div>
      </div>
      <div class="wl-entity">
        <div class="wl-entity-name">Chủ đầu tư bất động sản đã đủ pháp lý, đang chờ vốn</div>
        <div class="wl-entity-why">Room tín dụng trung dài hạn nới ra đúng lúc, rút ngắn thời gian chờ giải ngân dự án.</div>
      </div>
    </div>
    <div class="wl-side wl-lose">
      <div class="wl-side-label">Chịu thiệt</div>
      <div class="wl-entity">
        <div class="wl-entity-name">Nhóm ngân hàng còn nhiều dư địa SFL (khối quốc doanh)</div>
        <div class="wl-entity-why">Không hưởng lợi biên tương ứng vì đã có sẵn dư địa, trong khi lãi suất cho vay trung dài hạn cạnh tranh hơn do đối thủ cùng được nới room.</div>
      </div>
      <div class="wl-entity">
        <div class="wl-entity-name">Người gửi tiết kiệm kỳ hạn ngắn</div>
        <div class="wl-entity-why">Ngân hàng bớt áp lực đảm bảo tỷ lệ SFL nên giảm ưu đãi lãi suất huy động ngắn hạn, lãi suất tiền gửi dưới 6 tháng có thể đi ngang hoặc giảm nhẹ.</div>
      </div>
    </div>
  </div>
</div>
```
```

### 4.2 CSS

**Đã bỏ `background` trên `.wl-event` so với bản nháp đầu (xem mục 1.1)**, chỉ giữ `border-bottom`.

```css
.winlose { border: 1px solid var(--line); margin: 32px 0; }
.wl-event { padding: 14px 20px; border-bottom: 1.4px solid var(--ink); }
.wl-event-label { font-family: var(--font-mono); font-size: 9.5px; letter-spacing: .16em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 6px; }
.wl-event-text { font-family: var(--font-serif); font-weight: 700; font-size: 15px; line-height: 1.4; }
.wl-split { display: grid; grid-template-columns: 1fr 1fr; }
.wl-side { padding: 16px 20px; }
.wl-win { border-right: 1px solid var(--line); }
.wl-side-label { font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }
.wl-win .wl-side-label { color: var(--accent-hi); }
.wl-lose .wl-side-label { color: var(--neg); }
.wl-win .wl-side-label::before { content: "▲"; font-size: 9px; }
.wl-lose .wl-side-label::before { content: "▼"; font-size: 9px; }
.wl-entity { padding: 10px 0; border-top: 1px solid var(--line-lo); break-inside: avoid; }
.wl-entity:first-of-type { border-top: 0; padding-top: 0; }
.wl-entity-name { font-weight: 700; font-size: 13.5px; margin-bottom: 3px; }
.wl-entity-why { font-size: 12px; color: var(--ink-md); line-height: 1.5; }
@media screen and (max-width: 640px) {
  .wl-split { grid-template-columns: 1fr; }
  .wl-win { border-right: 0; border-bottom: 1px solid var(--line); }
}
```

### 4.3 Section gallery.html

```html
<section id="c27-winlose" aria-labelledby="h-c27">
  <div class="sec-kicker">KHỐI 27 · DẢI THẮNG THUA</div>
  <h2 class="sec-title" id="h-c27">Ai hưởng lợi, ai chịu thiệt khi trần SFL được nới</h2>
  <p class="sec-note">Trả lời: "Khi biến số này đổi, ai được và ai mất?" KHÔNG dùng cho một thực thể duy nhất qua hai thời điểm (dùng <code>before-after</code>); KHÔNG dùng khi cần so sánh nhiều tiêu chí giữa các phương án (dùng <code>options-comparison-table</code>).</p>
  <!-- dán nguyên khối .winlose ở mục 4.1 -->
</section>
```

**Ngắt trang & đen trắng**: chỉ `.wl-entity` có `break-inside: avoid` (từng mục không bị cắt giữa), còn `.winlose`/`.wl-split` KHÔNG ép nguyên khối, cho phép danh sách dài chảy qua trang nếu cần, đúng quy ước "container được ngắt, thẻ con thì không" đã dùng cho statgrid/exec-qa-grid. Đen trắng: ▲/▼ phân biệt bằng HÌNH DẠNG tam giác chứ không chỉ màu, cộng nhãn chữ HƯỞNG LỢI/CHỊU THIỆT, nên đây là component an toàn nhất trong nhóm có dùng màu.

---

## 5. KHỐI 28 · NGÃ BA CHÍNH SÁCH

File đề xuất: `components/catalog/28-policy-fork.md`

### 5.1 File catalog

```markdown
# Hai kịch bản sửa đổi Thông tư 22, một điểm rẽ

`KHỐI 28 · NGÃ BA CHÍNH SÁCH`

## Mô tả / khi nào dùng

Trả lời: "Chính sách này có mấy khả năng, và mỗi khả năng kéo theo hệ quả gì?" Một điểm rẽ chung ở trên, đúng hai nhánh loại trừ nhau ở dưới, mỗi nhánh có điều kiện rẽ (NẾU...) và một đoạn hệ quả. KHÔNG dùng khi có hơn 2 nhánh rẽ: chuyển sang `26-scenario-cards`, khối kịch bản xử lý được từ 3 nhánh trở lên kèm xác suất. KHÔNG dùng cho một chuỗi bước tuần tự không có điểm rẽ thật: dùng `16-process-step-chain`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="policy-fork">
  <div class="pf-root">
    <div class="pf-root-label">Điểm rẽ</div>
    <div class="pf-root-text">Ngân hàng Nhà nước đang lấy ý kiến sửa đổi Thông tư 22/2023 về tỷ lệ SFL, dự kiến ban hành Quý 4/2026.</div>
  </div>
  <div class="pf-branches">
    <div class="pf-branch" data-branch="a">
      <div class="pf-branch-label">Nhánh A</div>
      <div class="pf-cond"><span class="pf-cond-tag">NẾU</span>Phương án A được thông qua nguyên trạng: nâng trần SFL từ 30% lên 35%</div>
      <div class="pf-outcome">
        <div class="pf-outcome-label">Hệ quả</div>
        <p>Nhóm ngân hàng tư nhân tầm trung có thêm khoảng 45.000 tỷ đồng dư địa cho vay trung dài hạn toàn ngành, tăng trưởng tín dụng quý đầu hiệu lực có thể vượt kế hoạch được giao 1 đến 2 điểm phần trăm.</p>
      </div>
    </div>
    <div class="pf-branch" data-branch="b">
      <div class="pf-branch-label">Nhánh B</div>
      <div class="pf-cond"><span class="pf-cond-tag">NẾU</span>Phương án B thay thế được chọn: giữ nguyên trần SFL, đổi bằng room NSFR riêng cho bất động sản</div>
      <div class="pf-outcome">
        <div class="pf-outcome-label">Hệ quả</div>
        <p>Ngân hàng có tỷ trọng CASA thấp chịu áp lực huy động vốn dài hạn tăng, chi phí vốn bình quân toàn ngành nhích thêm 15 đến 20 điểm cơ bản trong hai quý đầu áp dụng.</p>
      </div>
    </div>
  </div>
</div>
```
```

### 5.2 CSS

**Đã bỏ `background` trên `.pf-root` so với bản nháp đầu (xem mục 1.1)**, chỉ giữ `border-bottom`.

```css
.policy-fork { border: 1.4px solid var(--ink); margin: 36px 0; break-inside: avoid; }
.pf-root { border-bottom: 1.4px solid var(--ink); padding: 16px 20px; text-align: center; }
.pf-root-label { font-family: var(--font-mono); font-size: 9.5px; letter-spacing: .18em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 6px; }
.pf-root-text { font-family: var(--font-serif); font-weight: 700; font-size: 15px; line-height: 1.4; max-width: 52ch; margin: 0 auto; }
.pf-branches { display: grid; grid-template-columns: 1fr 1fr; }
.pf-branch { padding: 16px 20px 14px; break-inside: avoid; }
.pf-branch[data-branch="a"] { border-right: 1px solid var(--line); }
.pf-branch-label { font-family: var(--font-mono); font-size: 9px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 8px; }
.pf-cond { font-weight: 700; font-size: 14px; line-height: 1.4; margin-bottom: 10px; }
.pf-cond-tag { font-family: var(--font-mono); font-weight: 700; font-size: 10px; letter-spacing: .08em; color: var(--accent-hi); margin-right: 6px; }
.pf-outcome-label { font-family: var(--font-mono); font-size: 9px; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 4px; }
.pf-outcome p { font-size: 12.5px; color: var(--ink-md); line-height: 1.55; margin: 0; }
@media screen and (max-width: 640px) {
  .pf-branches { grid-template-columns: 1fr; }
  .pf-branch[data-branch="a"] { border-right: 0; border-bottom: 1px solid var(--line); }
}
```

### 5.3 Section gallery.html

```html
<section id="c28-policyfork" aria-labelledby="h-c28">
  <div class="sec-kicker">KHỐI 28 · NGÃ BA CHÍNH SÁCH</div>
  <h2 class="sec-title" id="h-c28">Hai kịch bản sửa đổi Thông tư 22, một điểm rẽ</h2>
  <p class="sec-note">Trả lời: "Chính sách này có mấy khả năng, mỗi khả năng kéo theo hệ quả gì?" KHÔNG dùng khi hơn 2 nhánh (dùng <code>scenario-cards</code>); KHÔNG dùng cho chuỗi bước tuần tự không có điểm rẽ thật (dùng <code>process-step-chain</code>).</p>
  <!-- dán nguyên khối .policy-fork ở mục 5.1 -->
</section>
```

**Ngắt trang & đen trắng**: `.policy-fork` (gốc + 2 nhánh) là một khối `break-inside: avoid` duy nhất, giống `.assertion-card`/`.method-box`, nếu quá dài thì đẩy nguyên khối sang trang sau. Không dùng đường nối/mũi tên vẽ tay (tránh đúng bẫy transform/writing-mode đã ghi trong CLAUDE.md ở khối ma trận 2x2); cảm giác "rẽ nhánh" tạo bằng một khung viền liền mạch (gốc trên, hai nhánh dưới chung khung), an toàn tuyệt đối với WeasyPrint vì chỉ dùng border, không transform. Đen trắng: hai nhánh không dùng màu phân biệt (cùng viền, cùng nền), chỉ phân biệt bằng chữ NHÁNH A/NHÁNH B và NẾU/Hệ quả, nên đây là component không phụ thuộc màu ngay từ thiết kế gốc.

---

## 6. KHỐI 29 · DẢI TỰ SỰ CHEN GIỮA CHART

File đề xuất: `components/catalog/29-narrative-strip.md`

### 6.1 File catalog

```markdown
# Nối biên EBITDA với cơ cấu tuyến khai thác

`KHỐI 29 · DẢI TỰ SỰ CHEN GIỮA CHART`

## Mô tả / khi nào dùng

Trả lời: "Đọc xong hình trên rồi, tại sao tôi cần xem tiếp hình dưới?" Một đoạn văn ngắn (1 đến 3 câu) của chính tác giả, không đóng khung, không quy về giả định/cảnh báo/trích dẫn, chỉ để giữ mạch đọc giữa hai exhibit liền kề. KHÔNG dùng cho câu trích dẫn có thật từ một người cụ thể: dùng `07-pull-quote`. KHÔNG dùng cho giả định, cảnh báo hoặc điều kiện huỷ cần đóng khung: dùng `09-note-box`. KHÔNG dùng cho một câu kết luận tự đúc kết muốn nổi bật giữa trang: dùng `24-bonus-key-point-callout`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<p class="narrative-strip">
  <span class="ns-link" aria-hidden="true">Hình 2 → Hình 3</span>
  Biên EBITDA cải thiện chủ yếu nhờ giá cước tăng ở ba tuyến nội Á, nhưng ba tuyến này chỉ chiếm 34% tổng công suất đội tàu. Cơ cấu tuyến khai thác dưới đây cho thấy vì sao mức cải thiện khó lặp lại đều ở quy mô toàn đội trong các quý tới.
</p>
```
```

### 6.2 CSS

```css
.narrative-strip { max-width: 62ch; margin: 26px auto; font-family: var(--font-serif); font-style: italic; font-size: 15px; line-height: 1.7; color: var(--ink-md); text-align: center; break-inside: avoid; }
.narrative-strip .ns-link { display: block; font-family: var(--font-mono); font-style: normal; font-size: 9.5px; letter-spacing: .12em; text-transform: uppercase; color: var(--ink-lo); margin-bottom: 8px; }
```

### 6.3 Section gallery.html

```html
<section id="c29-narrative" aria-labelledby="h-c29">
  <div class="sec-kicker">KHỐI 29 · DẢI TỰ SỰ CHEN GIỮA CHART</div>
  <h2 class="sec-title" id="h-c29">Nối biên EBITDA với cơ cấu tuyến khai thác</h2>
  <p class="sec-note">Trả lời: "Đọc xong hình trên rồi, tại sao tôi cần xem tiếp hình dưới?" KHÔNG dùng cho trích dẫn thật (dùng <code>pull-quote</code>), cảnh báo/giả định (dùng <code>note-box</code>), hoặc một câu kết muốn nổi bật (dùng <code>bonus-key-point-callout</code>).</p>
  <!-- dán nguyên khối .narrative-strip ở mục 6.1 -->
</section>
```

**Ngắt trang & đen trắng**: đoạn ngắn theo thiết kế (1 đến 3 câu) nên gần như không bao giờ đủ dài để tràn trang, `break-inside: avoid` chỉ là an toàn mặc định theo đúng thói quen của các khối văn bản ngắn khác trong file (`pull-quote` cũng làm vậy). Đây là component AN TOÀN NHẤT trong cả 5 cho bản in đen trắng vì hoàn toàn không dùng màu (chỉ `--ink-md`/`--ink-lo`, hai sắc xám trung tính có sẵn), phân biệt hoàn toàn bằng kiểu chữ (nghiêng, cỡ nhỏ hơn thân bài, căn giữa, cột hẹp) chứ không phải màu hay khung. Nhãn `ns-link` là tuỳ chọn, bỏ đi vẫn chạy được.

---

## 7. Việc còn lại cho người thi công

1. `tests/consistency/catalog_drift.test.mjs` dòng 163 assert đúng 24 file catalog, phải sửa thành 29 khi thêm 5 file trên.
2. Khối in ấn tổng hợp `components.css` dòng 568-570 (danh sách `break-inside: avoid`) nên thêm `.exec-summary, .scn-card, .wl-entity, .policy-fork` vào cho nhất quán với cách file đang làm (đã khai `break-inside: avoid` tại chính rule của từng khối rồi, đây chỉ là lớp phòng thủ kép mà file đã áp dụng cho toàn bộ 22 khối cũ, không phải bắt buộc kỹ thuật).
3. `.narrative-strip` không cần thêm vào danh sách đó vì đã có break-inside ở chính nó và nội dung luôn ngắn.
4. Xin operator duyệt việc dùng `--pos` cho thẻ kịch bản Tích cực (callout đầu mục 3) trước khi merge CSS khối 26.
5. Chạy `node --test tests/consistency/catalog_drift.test.mjs` và `npm run verify:components` sau khi dán đủ cả 3 phần (catalog .md, CSS, gallery.html) theo đúng quy trình 4 bước ghi trong CLAUDE.md mục "Khi thêm component".

Toàn bộ 5 CSS block chỉ dùng biến từ `design-system/tokens.css` (accent/accent-hi/accent-soft/neg/warn/ink/ink-md/ink-lo/line/line-lo/paper/font-mono/font-serif/space/radius/shadow-1), không hardcode hex nào, không dùng `filter: blur()`/`backdrop-filter`, không dùng `aspect-ratio`/`writing-mode`, mọi media query màn hình đều viết `@media screen and (max-width: ...)`, và không có em-dash/en-dash ở bất kỳ đâu.

---

## 8. Thứ tự thi công 5 khối

Broadcast 4 mô hình ngoài xếp hộp tóm tắt điều hành là việc số một trong toàn bộ kế hoạch mở rộng thư viện, CAO HƠN cả 4 preset chart P0 mà `research/13-chart-component-gap/FINDINGS.md` từng xếp trên cùng (line có chú thích, bar ngang xếp hạng, quadrant scatter, dot distribution). Đây là thông tin MỚI so với FINDINGS gốc (lúc đó xếp hộp tóm tắt điều hành ở P1, dưới cả nhóm chart P0), nên thứ tự dưới đây ĐÈ lên thứ tự cũ của FINDINGS cho riêng nhóm B, không đổi thứ tự của nhóm A (chart).

1. **KHỐI 25, tóm tắt điều hành bốn ô.** Ưu tiên tuyệt đối theo đúng consensus 4 mô hình, đồng thời khớp với chính lập luận gốc của FINDINGS (10/10 loại báo cáo cần, đang thủng nhất trong toàn bộ khảo sát nhóm B).
2. **KHỐI 26, thẻ kịch bản.** FINDINGS xếp 8/10 nhu cầu và gọi thẳng đây là "thành phần người đọc hay bấm vào nhất ở bản tương tác", chỉ đứng sau hộp tóm tắt điều hành về tần suất cần dùng.
3. **KHỐI 29, dải tự sự chen giữa chart.** Chi phí thực thi gần như bằng 0 (thuần CSS chữ, không cần biến thể màu, không cần data attribute), và áp dụng được ở HẦU HẾT báo cáo có từ 2 exhibit trở lên bất kể ngành, nên tỷ lệ giá trị trên công sức cao nhất trong 3 khối còn lại.
4. **KHỐI 27, dải thắng thua.** Áp dụng khi báo cáo có một biến số hoặc chính sách thay đổi ảnh hưởng nhiều thực thể, phổ biến ở báo cáo ngành và vĩ mô nhưng không phải mọi báo cáo đều có tình huống này.
5. **KHỐI 28, ngã ba chính sách.** Hẹp nhất trong 5 khối: chỉ dùng được khi có đúng một điểm rẽ quy định hoặc chính sách nhị phân đang chờ quyết định (ví dụ báo cáo ngân hàng, ngành chịu quản lý chặt). Làm sau cùng không phải vì kém giá trị, mà vì tần suất gặp đúng tình huống "2 nhánh loại trừ nhau" thấp hơn 4 khối kia.
