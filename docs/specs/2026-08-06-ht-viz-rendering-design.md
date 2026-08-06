# HT-viz-rendering: thiết kế hệ thống

Ngày chốt: 2026-08-06
Trạng thái: thiết kế đã duyệt, chờ viết kế hoạch thi công

## 1. Vấn đề

Operator cần sinh báo cáo và phân tích tài chính tiếng Việt đạt chất lượng xuất bản: thiết kế đẹp ở mức ấn phẩm chuyên nghiệp, có chart tài chính đúng chuẩn, và có minh hoạ ngành neo được số liệu vào từng bộ phận vật thể. Hiện trạng là nhiều bộ skill rời rạc, mỗi bộ giải quyết một phần, không bộ nào phủ hết, và một số bộ đã hỏng âm thầm mà không ai biết.

Đích đến: một repo duy nhất, mọi thứ trong đó chạy được, dùng lại được cho mọi báo cáo về sau.

## 2. Phạm vi

Trong phạm vi:
- Tầng trình bày: từ nội dung đã chốt và số liệu đã verify, sinh ra HTML self-contained và PDF in được
- Ba nhóm hình: chart số liệu, component kể chuyện, minh hoạ ngành
- Tầng tư duy: quyết định thiết kế thế nào cho đúng bài này, không chỉ vẽ ra sao
- Nghiệm thu tự động trước khi giao file

Ngoài phạm vi:
- Phân tích tài chính và viết luận điểm. Đó là việc của các skill phân tích đã có
- Nạp số liệu tự động từ BCTC hoặc XBRL
- Kiểm chứng tính đúng của số liệu. Repo này chỉ ép mỗi số phải mang nguồn, không tự xác minh nguồn

## 3. Quyết định đã chốt

| Hạng mục | Quyết định | Lý do |
|---|---|---|
| Đầu ra chính | HTML self-contained và PDF | Anh gửi khách hai dạng này. HTML khi cần tương tác hoặc đẩy lên web, PDF khi cần bản trơn để in và forward |
| Engine PDF | WeasyPrint | Đã verify trên báo cáo thật 9 trang: 0 object ảnh raster. Chromium cùng file tạo 1 ảnh JPEG ẩn trong Tiling Pattern mà `get_images()` không thấy |
| Nền tảng | Nâng cấp StockLPT, không xây mới | StockLPT là superset của Opvia. Lõi vẽ và render đã verify chạy thật, thẩm mỹ đạt tầm ấn phẩm tài chính. Bốn trụ thiếu là lớp mới cần viết thêm, không phải sửa lỗi lớp cũ |
| Chart engine | Chia theo định dạng giao | matplotlib EIR cho PDF tĩnh vì đã có sẵn 48 component đúng chuẩn. ECharts SSR cho HTML tương tác vì matplotlib không bao giờ có hover và tooltip |
| Minh hoạ ngành | SVG viết tay | Không kho SVG mở nào có minh hoạ máy móc công trình đủ chi tiết. Ảnh AI đẹp hơn nhưng không neo được số liệu vào bộ phận, không sửa được, phải trả phí mỗi lần sinh |
| Nhánh PPTX | Vá 2 bug rồi dùng | Text và bảng editable thật. Chart và minh hoạ chấp nhận là ảnh tĩnh |
| Gauge và radar | Cấm | Gauge gợi ý độ chính xác không có thật. Radar có các trục không độc lập nên diện tích hình vô nghĩa |
| Nhận diện | Một lõi cố định, accent đổi theo ngành | Giữ được brand mà vẫn có vị riêng từng bài |
| Vận hành | Ba checkpoint | CK1 chốt kịch bản kể chuyện, CK2 chọn một trong ba bản preview dựng bằng nội dung thật, CK3 duyệt bản đầy đủ trước khi xuất |
| Vị trí | `~/HT-viz-rendering/`, symlink vào `~/.claude/skills/` | Sửa repo là skill đổi ngay |
| Công khai | Riêng tư | Được dùng thoải mái code mượn và ví dụ có số liệu thật |

## 4. Design token lõi

Ba nguồn độc lập hội tụ cùng một họ màu, đây là bằng chứng mạnh nhất thu được:

1. `reference-kimi.html`, bản operator tự đánh giá cao nhất, dùng ink `#051C2C` và accent `#2251FF`
2. `huashu-design/references/design-styles.md`, mục Two-Font Consulting, dùng đúng `#051C2C` là màu McKinsey deep-blue
3. `GIÁO TRÌNH Mindset thiết kế.txt` dòng 88, ghi đúng cả hai: `#051c2c` và `#2251ff`

Ba nguồn không ai chép ai. Token lõi neo theo đó.

```
--ink        #051C2C   text chính, nền trang bìa
--ink-md     #42566A   phụ đề, đoạn văn phụ
--ink-lo     #8595A6   chú thích, nhãn trục, dòng nguồn
--line       #DBE2EA   hairline phân cách
--paper      #FFFFFF   nền trang
--paper-hi   #F7F9FC   nền panel và card
--accent     #2251FF   số trung tâm, nhấn mạnh chính
--accent-soft #7D9BFF  chuỗi phụ trong chart
--accent-warm #B07A10  badge nguồn, nhấn ấm, dùng tiết chế
--positive   #008A6D   tăng trưởng, dùng cực tiết chế
--negative   #C22F4E   giảm, rủi ro, thiếu
```

Font: `Spectral` cho mọi vai trò chữ, `IBM Plex Mono` cho số liệu và nhãn kỹ thuật. Đã kiểm bằng fontTools `getBestCmap`: cả hai đủ glyph tiếng Việt, kể cả `ừ ộ ẫ ợ ữ ể ỗ đ Đ ư Ư ơ Ơ`. Đã kiểm bằng render thật ở ba điều kiện khắc nghiệt (body 17px line-height 1.5, display 44px line-height 1.15, chữ hoa có dấu 36px): không vỡ, không đụng dấu.

Bổ sung một phương án sans `IBM Plex Sans` chỉ dùng cho ô bảng và nhãn nhỏ khi bảng số liệu quá dày, không dùng cho tiêu đề hay thân bài.

Thang chữ tỉ lệ 1.333. Spacing 8 bậc trên lưới 4px. Radius nhỏ gần phẳng: 2, 3, 6px. Cố ý không dùng bo tròn lớn vì bo tròn lớn cộng border-left màu là dấu hiệu AI-slop, và vì báo cáo tài chính mật độ cao khác landing page.

**Shadow dùng offset cứng, blur bằng 0.** Đây là kết quả một thí nghiệm tách ba biến thể độc lập, đo bằng `doc.xref_object`:

| Biến thể | Kết quả |
|---|---|
| `2px 2px 0 rgba(...)` offset cứng, blur 0 | 0 ảnh raster |
| `0 6px 20px rgba(...)` có blur | 1 ảnh raster |
| Hai lớp offset cứng chồng nhau | 0 ảnh raster |

Kết luận: không phải cứ có `box-shadow` là bị nướng bitmap, **chỉ blur-radius lớn hơn 0 mới bị**. Vì vậy shadow con dấu (`2px 2px 0` cộng một lớp ngược chiều) là ngôn ngữ độ nổi duy nhất của toàn hệ. Cách này giải quyết vấn đề ngay từ token nên không phải override `box-shadow: none` cho từng component, và ít chỗ để sót hơn.

Đo thật bằng Range API: cột prose 65ch ở 17px Spectral cho 67 tới 70 ký tự mỗi dòng. **Dấu tiếng Việt chỉ làm giảm 4% ký tự mỗi dòng** so với văn bản không dấu, không cần cộng buffer line-height kiểu CJK. Tiếng Việt viết cách từ nên dấu chỉ cộng chiều cao, không cộng chiều rộng.

## 5. Kiến trúc

### 5.1 Hai tầng

Tầng 1 là engine dùng chung: design system, kernel, ba nhóm hình, pipeline render, gate nghiệm thu.

Tầng 2 là preset theo loại báo cáo. Mỗi preset chỉ định nghĩa kịch bản kể chuyện mặc định, bộ hình hay dùng, accent ngành. Toàn bộ dựng hình gọi xuống tầng 1.

### 5.2 Luồng chạy

```
Nội dung đã chốt + ledger số liệu (mỗi số kèm nguồn, ngày, bậc bằng chứng)
        │
   [CK1] Kịch bản kể chuyện: mỗi section một câu hỏi, hình gì trả lời
        │
   [CK2] Ba bản preview hero và section đầu bằng nội dung THẬT, chọn một
        │
   Dựng HTML: token + kernel dùng chung
        ├─ chart tĩnh    → matplotlib EIR, xuất SVG, fonttype none
        ├─ chart tương tác → ECharts SSR, renderer SVG
        ├─ minh hoạ      → SVG viết tay + lớp annotation
        └─ component     → 22 khối HTML/CSS
        │
   Lint trước render: chặn filter blur, backdrop-filter, border alpha đè gradient,
                      box-shadow blur khi in, media query thiếu `screen`
        │
   [CK3] Duyệt bản đầy đủ
        │
   Xuất ─┬─ HTML self-contained (font base64 kèm unicode-range)
         ├─ PDF (WeasyPrint)
         └─ PPTX (html2pptx đã vá, chart rasterize trước)
        │
   Sáu gate nghiệm thu, FAIL là không được giao
```

### 5.3 Cấu trúc repo

```
HT-viz-rendering/
├── README.md                cổng vào cho người
├── SKILL.md                 cổng vào cho Claude, CHỈ định tuyến
├── CLAUDE.md                quy ước làm việc trong repo
│
├── doctrine/                tầng tư duy
│   ├── 00-design-read.md    đọc brief trước khi vẽ
│   ├── 01-narrative.md      kịch bản kể chuyện, 6 hợp đồng đầu ra
│   ├── 02-evidence.md       nhãn sự kiện/diễn giải/giả thuyết, 5 bậc bằng chứng
│   ├── 03-chart-doctrine.md 25 quy tắc kiểm được, 5 luật EIR
│   ├── 04-anti-slop.md      vn-humanizer R6, luật văn phong
│   ├── 05-metaphor.md       bảng tra ẩn dụ, semantic-site principle
│   └── 06-mindset.md        chắt lọc từ giáo trình
│
├── design-system/
│   ├── tokens.css           token lõi
│   ├── tokens.py            bản Python cho pipeline WeasyPrint
│   ├── typography.md        thang chữ đã đo bằng tiếng Việt
│   ├── industry-accents.json  8 preset accent ngành
│   └── fonts/               Spectral + IBM Plex Mono, woff2 subset VN
│
├── components/              nhóm B
│   ├── components.css
│   ├── components.js
│   ├── gallery.html         demo sống, mở ra xem hết 22 khối
│   └── catalog/             22 spec, mỗi khối dùng khi nào
│
├── charts/                  nhóm A
│   ├── echarts/             12 chart SSR, theme.mjs, fmt.mjs
│   ├── matplotlib/          48 component EIR đã vá font
│   └── catalog/             18 loại, dùng khi nào, bẫy gì
│
├── illustrations/           nhóm C
│   ├── svg/                 11 hình, tăng dần
│   ├── annotate.js, annotate.css
│   ├── grammar.md           ngữ pháp vẽ
│   ├── metaphor-table.md
│   └── prompt-template.md   để vẽ hình mới
│
├── pipeline/
│   ├── render_html.py
│   ├── render_pdf.py        WeasyPrint
│   ├── render_pptx.mjs      html2pptx đã vá 2 bug
│   └── orchestrator.py      điều phối, 3 checkpoint thật
│
├── gates/
│   ├── gate.mjs             6 gate nghiệm thu
│   ├── validators.py        đã sửa false positive
│   ├── evidence-validator.mjs
│   ├── guard-source-leak.mjs
│   └── lint_vi.py           văn phong R6
│
├── presets/                 tầng 2, bốn preset xây trước
│   ├── bao-cao-nganh/       kế thừa archetype sector_deep_dive
│   ├── bao-cao-co-phieu/    kế thừa equity_single_stock + earnings_review
│   ├── ban-tin-thi-truong/  kế thừa daily_report + macro_monetary
│   ├── deal-pack/           mới, không có archetype tương ứng
│   └── _inherited/          6 archetype còn lại giữ nguyên để dùng khi cần:
│                            banking_regulatory, commodities, esg,
│                            fixed_income, fx_currency, ma_corporate_action
│
├── examples/
│   └── vantaibien-2026/     một báo cáo hoàn chỉnh làm bản chuẩn
│
└── tests/smoke/             một lệnh, verify pipeline còn sống
```

Ba nguyên tắc của cấu trúc này:

**SKILL.md chỉ định tuyến.** Không nhồi nội dung. Nói "việc này đọc `doctrine/03`, việc kia đọc `charts/catalog/waterfall.md`".

**Mọi thứ trong repo đều chạy được.** Không có tài liệu suông.

**Có smoke test, và đây là bài học đắt.** Bộ Opvia có `catalog/cover_deep_page.md` mô tả HTML dùng các class không tồn tại trong CSS thật. Trang bìa vẫn chạy nhưng suy biến âm thầm: mất layout hai cột, mất đường brass, bullet lặp đôi. Không ai phát hiện vì không ai chạy thử. Smoke test phải kiểm: catalog nói gì thì code làm được đúng thế.

## 6. Nhóm A: chart số liệu

18 loại đã chốt. 12 loại đã có code ECharts chạy thật và verify SVG sạch. 48 component matplotlib EIR đã có sẵn.

Chia engine theo định dạng giao, không theo loại chart:
- PDF tĩnh dùng matplotlib EIR, xuất SVG với `svg.fonttype='none'`
- HTML tương tác dùng ECharts SSR renderer SVG

Ba bẫy phải ghi vào doctrine:

**Bẫy font, đây là gốc rễ lỗi rớt dấu tiếng Việt.** Không phải do engine nào. Nguyên nhân là cách khai báo `font-family`: một tên trần thay vì chuỗi fallback kết thúc bằng từ khoá generic. Khai trần thì trình duyệt thay glyph theo từng ký tự, ra lỗi tinh vi hơn tofu: "Số liệu" thành "Sô´liệu", dấu sắc tách rời trôi nổi, nhìn thoáng tưởng đúng nên dễ lọt QC. Fix: luôn khai `family=[tên_thật, dự_phòng, 'monospace']` dạng list kết thúc generic. `_eir_style.py` còn một bug đường dẫn: hardcode `liberation2` trong khi thư mục thật là `liberation`.

**ECharts SSR không tự thoát process.** Hai socket handle treo, `dispose()` không giải phóng. Mọi script phải kết bằng `chart.dispose(); process.exit(0);` nếu không sẽ treo vô thời hạn trong pipeline batch.

**Bẫy màu theo chiều chứ không theo tốt xấu.** `_eir_style.py` có `TONE` map `up` bằng `pos` và `down` bằng `neg`. Sai: chi phí giảm là tin tốt nhưng vẫn là giảm. Caller phải tự map tốt xấu tại điểm gọi, không suy ra từ dấu số.

Định dạng số tiếng Việt đã chốt và test 25 trên 25: dấu chấm là hàng nghìn, dấu phẩy là thập phân. Đơn vị nghìn, triệu, tỷ, nghìn tỷ. Phần trăm không khoảng trắng. Bội số dùng `15,2x` trong bảng và `15,2 lần` trong văn xuôi. Kỳ dùng `Q3/2026` cho nhãn và `quý 3/2026` cho văn xuôi, không dùng `3Q26`.

Bỏ trục kép khỏi danh mục. Thay bằng chỉ số hoá về gốc 100 với một trục.

## 7. Nhóm B: component kể chuyện

22 component đã dựng và verify: PDF 16 trang, 0 object ảnh raster.

Bảy bẫy print-safe mới phát hiện, tất cả bằng cách render PDF thật rồi soi từng trang:

1. `box-shadow` có blur bị Chromium nướng thành bitmap kể cả khi không đụng `filter`. Đo được 12 object ảnh từ 6 thẻ. Fix: `box-shadow: none` trong `@media print`
2. `@media (max-width: Npx)` không giới hạn `screen` **tự kích hoạt khi in**, vì vùng in A4 chỉ khoảng 688 tới 717px sau margin, hẹp hơn hầu hết breakpoint mobile. Fix: mọi breakpoint phải viết `@media screen and (max-width: ...)`
3. `overflow-x: auto` cộng `min-width` cố định cắt mất cột ngoài trang khi in
4. Component tra DOM bằng `root.querySelector` phải nằm đúng bên trong root, nếu không sẽ rỗng im lặng
5. Flex item không có `break-inside: avoid` bị cắt đôi giữa hai trang
6. `white-space: nowrap` trên badge tràn ra ngoài thẻ hẹp
7. Grid con nhiều hơn số cột khai báo khi `::before` counter tự chiếm một cột

**Cách đo dấu tiếng Việt phải dùng mực chữ, không dùng hộp dòng.** Phép đo sai là so `getBoundingClientRect().height` với `fontSize × lineHeight`: hai số này theo định nghĩa CSS luôn bằng nhau khi không có `overflow: hidden`, nên kết quả "an toàn" không bao giờ có thể trả về "không an toàn". Phép đo đúng dùng Canvas `measureText().actualBoundingBoxAscent` và `actualBoundingBoxDescent`, đọc mực chữ thật, độc lập với line-height khai báo. Phải đo sau khi trang đã tải font, nếu không Canvas dùng font chưa tải và cho số sai.

Về accessibility, sửa đúng cách chứ không máy móc: **không gắn `role="img"` lên container HTML thật** vì sẽ che mất text bên trong khỏi cây accessibility, tệ hơn cả không làm gì. Cách đúng: đánh dấu bản trực quan phức tạp `aria-hidden="true"` rồi cung cấp bản thay thế thật, là danh sách phẳng hoặc bảng dữ liệu ẩn.

## 8. Nhóm C: minh hoạ ngành

Đây là phần không mua được ở đâu. Đã khảo sát 12 repo và mọi kho SVG mở: không nơi nào có cơ chế sinh minh hoạ theo chủ đề ngành.

**Nguyên lý cốt lõi là semantic-site principle**, trích từ giáo trình dòng 25-26:

> Con số phải treo vào bộ phận của vật thể mà trong thực tế nó thực sự làm chức năng đo lường đó. Con số không nằm trên tàu, con số là bộ phận của tàu. Số không có chỗ ngồi ngữ nghĩa thì không treo bừa, đưa về prose.

Ví dụ đúng: mớn nước là kim ngạch, hầm máy là chi phí vận hành, cờ hiệu là quốc tịch đăng ký. Ví dụ sai: một hộp số đặt cạnh con tàu.

**Định nghĩa chart giả, đo được**: một hình phải mã hoá ít nhất 2 biến cấu trúc ngoài chữ, chọn trong số lượng, thời gian, dòng chảy, xác suất, tô-pô, đơn vị vật lý. Dưới ngưỡng đó thì giáng xuống prose hoặc bảng. Luật này tự động bao trùm gauge và radar mà không cần liệt kê tên.

**Ba bài tự kiểm trước khi ship**:
1. Che hết chữ. Không đọc ra được biến cấu trúc nào thì xoá ngay, không polish nữa
2. Đổi ngành. Hình còn dùng được nguyên thì nó là trang trí, không phải phân tích
3. Kiểm danh sách đen: reskin vật chứa nghĩa đen, chuỗi icon truyền sóng, cây quyết định bằng textbox, bảng tường số

**Ngữ pháp vắng mặt**, đưa vào token làm từ vựng thị giác cố định: rỗng cộng nét đứt là dự báo, hatch là ước tính, hatch đỏ cộng dấu hỏi là thiếu dữ liệu, đường không vẽ là thực thể đã chết. Lập trường kèm theo: vẽ cả khoảng trống, không nội suy, không giấu.

**Ngữ pháp vẽ**: viewBox 800x500 ngang hoặc 500x640 đứng, lề tối thiểu 5%, mặt đất ở 0.86 chiều cao, mặt nước ở 0.72. Ngưỡng shape: dưới 20 là sơ sài, 25 tới 45 cho vật thể chính, trên 80 là rối. Một accent qua biến CSS cộng dải neutral cố định, tô phẳng hai tông, không gradient. Cấm tuyệt đối filter, mask phức tạp, clipPath lồng nhau, gradient nhiều stop.

**Lớp annotation**: `tone` chỉ ba giá trị là neutral, negative, accent. Kỷ luật một callout accent mỗi hình. Đường dẫn dùng elbow vuông bo tròn, không bezier lượn, và độ dài không vượt 1,6 lần đường thẳng. Đã đo thật bằng `getTotalLength()`: dài nhất 1,398 lần. Hai mode bố cục không dùng chung được, phải chọn tường minh: nhãn cột dọc hai bên cho vật thể cao, nhãn hàng ngang trên dưới cho bố cục banner.

**Thứ tự giải va chạm nhãn** với ngưỡng đo thật: dời vị trí, so le tầng, xuống dòng theo từ, đo và cắt với serif tối thiểu 5,8px mỗi ký tự và mono 6px ở cỡ 10px. Đuôi cắt phải gỡ dấu phẩy, mạo từ, giới từ trước khi thêm dấu ba chấm. Bản đầy đủ luôn nằm trong drill-down. Chữ đè đường luôn dùng `paint-order: stroke` với halo giấy 3,5 tới 5px.

Bản đồ quốc gia phải sinh từ dữ liệu geo thật qua d3-geo, không tay gõ toạ độ. Nguồn world-atlas Natural Earth, lọc lấy polygon lục địa lớn nhất, đơn giản hoá Visvalingam còn khoảng 72 điểm, chiếu Mercator qua `fitExtent`. Bản tay gõ từ trí nhớ không ra được hình chữ S.

Mọi nhãn chữ đặt trên hình phải có halo, nếu không sẽ bị đường nét của hình cắt ngang chữ. Dùng `stroke` màu nền với `paint-order: stroke`.

**Ba việc phải verify bằng số, không bằng mắt**, vì cả ba đều có sai số quá nhỏ để mắt bắt được trên ảnh full-page:
1. Độ dài đường dẫn callout, đo bằng `path.getTotalLength()` từ DOM đã render
2. Hộp nhãn nằm trọn trong viewBox, đo bounding box thật của từng hộp
3. Chữ không đè lên nét hình

Một bug thật đã bắt được nhờ đo: hàm giải va chạm có bước nén cho vừa khung dùng hệ số ngược chiều, phần tử cuối đang gây tràn lại nhận hệ số nhỏ nhất. Hộp tràn 16,5px mà nhìn ảnh không thấy. Cách sửa đúng là thuật toán hai lượt, top-down đảm bảo khoảng cách tối thiểu rồi bottom-up kẹp không vượt biên, cộng một ràng buộc cứng ưu tiên thu hẹp bề rộng hộp trước khi dời vị trí.

**Đánh giá thật thà về giới hạn**: SVG viết tay thua ảnh AI về chất liệu bề mặt và độ phong phú chi tiết. Đó là cái giá có chủ đích của luật cấm gradient và filter để đổi lấy PDF không vỡ. Đổi lại, ảnh AI không neo được số liệu vào bộ phận, không sửa được, phải trả phí mỗi lần sinh. Quy tắc dùng: ảnh AI cho bìa chương và banner trang trí không cần callout, SVG tay cho mọi minh hoạ cần neo số liệu thật.

## 9. Truy nguồn số liệu

Mỗi giá trị hiển thị mang `{value, unit, period, source_id, retrieved_date, tier, note}`.

Năm bậc bằng chứng: T1 công bố chính thức, T2 báo cáo kiểm toán, T3 broker, T4 ước tính nội bộ có công thức, T5 suy diễn.

Trục thứ hai độc lập với bậc: `public` hoặc `internal_only`. Nguồn `internal_only` bắt buộc có `public_label`, là câu quy đổi đã duyệt. Schema ép bằng `if/then required`, thiếu là lỗi validate ngay.

Hai chế độ xuất: bản nội bộ hiện đủ nguồn, bản gửi đi chỉ hiện nhãn quy đổi cho nguồn `internal_only`. Nguồn `public` trích dẫn đầy đủ ở cả hai bản, đó không phải rò rỉ.

Validator đã chạy thật: file sạch PASS 0 lỗi, file bẩn FAIL 9 lỗi và 2 cảnh báo, bắt được orphan value, tier drift, ngày tương lai, lệch đơn vị trong cùng chart, dangling reference, lệch giữa text HTML và ledger.

## 10. Sáu gate nghiệm thu

Đã chạy thật. Trên `reference-kimi.html` cho kết quả FAIL đúng như mong đợi.

| Gate | Kiểm gì | Kết quả trên file Kimi |
|---|---|---|
| Font | Font đầu stack phải Windows-safe hoặc nhúng base64 kèm unicode-range phủ khối có dấu | PASS |
| Raster | Đếm `/Subtype /Image` qua `doc.xref_object`, không dùng `get_images` vì nó bỏ sót ảnh trong Tiling Pattern | FAIL: 53 object ảnh, 34 ảnh full-panel trên 500.000px |
| Dấu tiếng Việt | So mật độ ký tự có dấu giữa HTML và text trích từ PDF, đếm FFFD và cờ synthetic | PASS |
| Văn phong | Chặn em-dash và en-dash, chặn câu kết cách ngôn không có số, chặn cụm AI-slop | PASS |
| Ngắt trang | Hai lớp: có khai `break-inside: avoid` không, và hình học thật tìm panel bị cắt đúng ranh giới trang | WARN: không có khai báo nào |
| Rò rỉ nguồn | Cụm từ cấm, tên riêng viết tắt, đối chiếu ledger ở chế độ external | PASS |

Giới hạn thành thật: gate dấu tiếng Việt không có OCR vì máy không cài được tesseract offline. Nó bắt được lỗi encoding và glyph mất hẳn, nhưng không bắt được trường hợp ToUnicode đúng mà glyph outline bị thay bằng notdef. Vẫn cần soi tay bằng mắt cho bản gửi khách.

## 11. Bug phải vá trong tài sản kế thừa

| Bug | Ở đâu | Sửa gì |
|---|---|---|
| SVG làm crash cả file PPTX | `html2pptx.js` dòng 757 | `el.className.includes()` gọi trên `SVGAnimatedString`. Dùng `el.classList` hoặc kiểm `typeof` trước |
| Bảng mất trắng 100% im lặng | `html2pptx.js` | Không có nhánh xử lý `<table>`. Thêm nhánh gọi `addTable()` có sẵn trong pptxgenjs |
| Rớt dấu tiếng Việt | `_eir_style.py` | Đường dẫn `liberation2` thừa số 2. Và phải đổi `family=chuỗi` thành `family=[list kết thúc generic]` |
| Catalog drift | `catalog/cover_deep_page.md`, `back_cover_cta.md` | HTML template dùng class không tồn tại trong CSS thật. Viết lại khớp CSS, và thêm smoke test chống tái diễn |
| Validator báo 26 lỗi giả | `validators.py` | Mở whitelist palette cho CSS variable thật, loại số trong style attribute khỏi kiểm định dạng, thêm validator overflow text |
| Gate bị tắt mặc định | `orchestrator.py` | `strict=False` và `skip_confirm=True`. Bật lên, thêm kiểm PDF sau khi ghi |
| Module chưa đấu nối | StockLPT | `viz_institutional.py` và `viz_daily.py` không được import, không có catalog, `_build_css()` không nạp CSS của chúng |
| Tài liệu sai sự thật | `opvia-data-viz/SKILL.md` | Ghi 19+ component (thật là 35) và viz_advisor 22 heuristic 94% (thật là đã scrap, mọi hàm raise NotImplementedError) |
| Font mồ côi | hai thư mục polish | 8 file woff2 không ai tham chiếu |

## 12. Tài sản thu hoạch

Đã kiểm chứng và copy về scratchpad, chờ đổ vào repo:

- 48 component matplotlib EIR cùng `EIR_DESIGN.md` với 5 luật rút từ FT, Bloomberg, Goldman, Morningstar, Economist
- 35 component HTML/SVG của Opvia cùng 10 archetype
- `viz_institutional.py` với football_field và sensitivity_grid, `viz_charts.py`, `fiinquant_adapter.py` của StockLPT
- 97 ẩn dụ hình ảnh tài chính trong `MOTIF_TABLE.md` kèm prompt template phong cách Economist
- `tokens.css` canonical đã verify font tiếng Việt
- `html2pptx.js` 1177 dòng, MIT
- `vn-humanizer` với register R6 dành riêng cho báo cáo doanh nghiệp, và `lint_vi.py` chạy được
- `typst-render` với `cfa_warm.typ` và `l2t.py`, giữ làm phương án PDF dự phòng
- ThinkTank với 6 hợp đồng đầu ra, nhãn sự kiện/diễn giải/giả thuyết, 12 acceptance test
- `validate_markup.py` 732 dòng với 39 mã lỗi, làm mẫu cho linter xác định

Một lưu ý về vn-humanizer: register R6 **miễn trừ** bị động và danh hoá, ngược với universal tells. Áp luật chung mù quáng vào báo cáo tài chính sẽ sửa sai.

## 13. Những gì để ngỏ

- Engine chart 46 loại của `cfa-viz-factory` đã mất khỏi đĩa. Chỉ còn 46 ảnh output làm tham chiếu style. Nếu operator còn bản sao ở đâu thì đưa vào, không thì dựng lại theo style DNA nhìn từ ảnh
- Typst đã verify tốt hơn về mặt vector tuyệt đối (0 trên 112 xref là ảnh) và có toán native, nhưng chưa chọn vì phải viết lại tầng trình bày. Giữ trong repo làm phương án dự phòng cho tài liệu nặng công thức
- Chưa test screen reader thật, chỉ kiểm DOM và ARIA tĩnh
- Bốn chart ECharts chưa có code và vẫn cần: scatter bubble, funnel, box plot, lollipop. Hai loại còn lại trong danh mục 18 đã bị loại có chủ đích là gauge (cấm) và trục kép (thay bằng chỉ số hoá về gốc 100)
- Ẩn dụ tảng băng chưa vẽ, để đợt mở rộng sau

## 14. Thứ tự thi công

Anh chọn đổ hết tài sản trước rồi mới nối pipeline.

1. Dựng khung repo và đổ toàn bộ tài sản thu hoạch vào đúng chỗ
2. Viết doctrine bảy file
3. Hợp nhất design system, vá bug font
4. Nối pipeline và ba checkpoint
5. Nối sáu gate
6. Viết smoke test
7. Làm một báo cáo vận tải biển hoàn chỉnh làm bản chuẩn, nghiệm thu bằng chính gate của repo
