# Phase 2: pipeline HTML sang PDF và bộ gate

Ngày viết: 2026-08-07
Trạng thái: ĐÓNG 2026-08-07, nghiệm thu chạy thật
Tiền đề: Phase 1 đóng, thư viện mở rộng xong. Đọc `memory.md` trước.

## Vì sao phase này tồn tại

Repo có 18 preset ECharts, 50 component matplotlib, 29 component HTML, 11 minh hoạ SVG. Không
thứ nào trong số đó từng đi trọn đường tới file PDF giao đi rồi bị kiểm. Hệ quả đã đo được: bug
12 chart xuất SVG không hợp lệ XML sống trọn một phase, PDF ra 0 nét vẽ mà mọi gate vẫn xanh.

Ba probe chạy trước khi viết plan này, kết quả bằng số:

| Probe | Đo gì | Kết quả |
|---|---|---|
| P1 | Nhúng SVG vào WeasyPrint bằng 4 cách (inline, data URI, file ref, object) | Cả 4 đều sống: 19 nét vẽ, 0 ảnh raster, nhãn chart nằm trong tầng text |
| P2 | WeasyPrint có giải được woff2 base64 không | CÓ. Nhúng đúng `Spectral`, `IBM-Plex-Mono` dạng Type0 subset |
| P2b | Bỏ `@font-face` đi thì sao | Rơi về `Noto-Serif` + `Liberation-Mono`, mà tầng text VẪN đúng: 0 synthetic, 0 FFFD, dấu tiếng Việt đọc ra chuẩn |
| P3 | Minh hoạ `example-vertical-axis-ship.html` qua WeasyPrint | 42 nét vẽ nhưng chỉ 197 ký tự text. **Cả 7 callout biến mất** |

P2b là phát hiện nặng nhất: gate dấu tiếng Việt hiện tại đo tầng text, mà tầng text KHÔNG phân
biệt được file dùng font đúng với file rơi về font Linux. Đây đúng là bẫy
`feedback_font_linux_khong_dung_cho_file_gui_di`, và bộ gate hiện tại mù với nó.

P3 là bug lớp thứ tư cùng họ với ba lớp đã biết: trình duyệt đúng, engine đích hỏng, không ai
biết. `annotate.js` dựng callout bằng JavaScript lúc chạy; WeasyPrint không chạy JS nên bảy con
số neo vào bảy bộ phận con tàu, tức toàn bộ giá trị của minh hoạ, không có mặt trong PDF.

## Quyết định đã chốt với operator

| Hạng mục | Chốt | Ghi chú |
|---|---|---|
| Đầu vào pipeline | Markdown + front-matter + `ledger.json` | Đường dùng lại được cho mọi báo cáo sau |
| Ba checkpoint | Ghi artifact rồi dừng, KHÔNG hỏi y/n trên terminal | Chạy được trong batch và trong test tự động |
| Nghiệm thu | Một báo cáo mẫu 4 tới 6 trang, nội dung thật cỡ nhỏ | Không lấn sang báo cáo vận tải biển của Phase 4 |
| PPTX | NGOÀI phạm vi lần này | Operator giao đúng "HTML sang PDF" |

## Quyết định kỹ thuật rút từ probe

1. **Nhúng chart bằng inline `<svg>`**, không dùng data URI. Cả hai đều self-contained, nhưng
   inline nhẹ hơn khoảng một phần ba (base64 phình 33%) và mở được bằng mắt lúc gỡ lỗi. Cái giá
   phải trả là xung đột `id` khi nhiều SVG cùng trang, nên bước nhúng phải đặt tiền tố `id` theo
   từng hình.
2. **Minh hoạ phải được bake trước khi vào PDF.** Mở bằng Chromium qua `scripts/lib/chromium.mjs`,
   để `annotate.js` chạy xong, lấy `outerHTML` của SVG đã có callout, ghi ra file SVG tĩnh. Đây là
   bước bắt buộc, không phải tuỳ chọn.
3. **Gate font phải đọc PDF, không chỉ đọc CSS.** Liệt kê `BaseFont` thật trong PDF và FAIL khi
   thấy họ fallback hệ thống (Noto, Liberation, DejaVu, FreeSerif). Đây là gate duy nhất phân biệt
   được hai trạng thái mà P2b vừa chứng minh là tầng text không phân biệt nổi.
4. **Không thêm dependency markdown.** Port bộ dựng markdown của StockLPT
   (`_build_body_from_markdown`) rồi mở rộng directive. Giữ repo chạy offline và kiểm soát được
   class CSS sinh ra, vì luật repo là catalog phải khớp CSS thật.

## Kiến trúc

Đây là kiến trúc ĐÃ DỰNG, không phải bản dự kiến. Hai chỗ khác bản nháp đầu, ghi lại lý do
ngay dưới sơ đồ.

```
<thu-muc-bao-cao>/noi-dung.md + so-nguon.json + hinh/
      │
      ├─ [1] sinh hình     chạy hinh/*.mjs và hinh/*.py, bake hinh/*.html qua Chromium
      │
      ├─ [2] CK1  ra/ck1-kich-ban.md          mỗi section một câu hỏi, hình nào trả lời
      │
      ├─ [3] CK2  ra/ck2-bia-{dac,hairline,vien-accent}.pdf   ba kiểu bìa, nội dung thật
      │
      ├─ [4] build_html.py   markdown + directive + sổ nguồn + token + font base64
      │                      -> một file HTML tự đủ, khoá sáng data-theme="light"
      │                      dựng CẢ HAI bản: noi-bo và gui-di
      │
      ├─ [5] CK3  render_pdf.py qua WeasyPrint, tự mở lại kiểm ngay sau khi ghi
      │
      └─ [6] gates/run.mjs   mười gate trên cả hai bản. FAIL là không được giao
```

Hai chỗ khác bản nháp:

**Không có `render_charts.mjs`.** Bản nháp định viết một lớp gọi 18 preset với dữ liệu thật,
nhưng preset hiện là script hardcode dữ liệu demo, và bọc chúng lại đòi refactor cả 18 file.
Cách đang dùng đúng tinh thần "preset là ý tham khảo, không phải khuôn ép" đã ghi trong
`CLAUDE.md`: báo cáo chép bố cục preset vào `hinh/` của mình rồi thay số thật, nên dữ liệu của
báo cáo nằm trong thư mục báo cáo chứ không ẩn trong một preset dùng chung. Bước 1 chạy mọi
script trong `hinh/`, không cần biết chúng gọi engine nào. Đổi lại, việc gói preset thành bề
mặt gọi được vẫn còn nợ, ghi trong sổ nợ của `memory.md`.

**CK2 là ba KIỂU BÌA, không phải ba bản preview tuỳ ý.** Ba biến thể sinh ra cho có thì không
giúp ai chọn. Ba kiểu bìa thật (`dac`, `hairline`, `vien-accent`) khai bằng `bia_kieu` trong
front-matter, dựng trên cùng nội dung thật, thì so được và chọn xong là dùng luôn.

```
pipeline/
├── orchestrator.py   nối trọn sáu bước, ba checkpoint ghi artifact
├── build_html.py     markdown + sổ nguồn -> HTML tự đủ
├── render_pdf.py     WeasyPrint, có kiểm PDF ngay sau khi ghi
├── bake_svg.mjs      đóng băng callout của annotate.js
└── report.css        trang giấy: khổ, lề, chạy đầu chân trang, ba kiểu bìa

gates/
├── run.mjs           runner, in bảng, trả exit code
├── gates.mjs         mười gate, mỗi gate một hàm thuần để test gọi thẳng
├── pdf_checks.py     mọi phép đo trên PDF nhị phân, gọi một lần dùng chung
├── lib/xml.mjs       phép kiểm XML, dùng chung với scripts/verify-charts.mjs
├── guard-source-leak.mjs, evidence-validator.mjs, schema/
└── fixtures/         cặp đỏ và xanh cho từng gate

examples/mau-phase2/  báo cáo mẫu 6 trang, nội dung thật cỡ nhỏ
```

Mười gate nằm trong MỘT file `gates.mjs` chứ không mỗi gate một file như bản nháp: mỗi gate
chỉ vài chục dòng, và chúng dùng chung một gói dữ liệu, nên tách file chỉ thêm mười dòng
import mà không thêm cách ly nào có thật.

## Mười gate

Bảy gate kế thừa từ `_harvest/lab-gate/` và `_harvest/lab-evidence/`, ba gate mới sinh từ probe. Bản nháp đầu ghi chín gate; gate LEDGER được tách riêng thay vì nhét vào gate SOURCE-LEAK, vì hai gate trả lời hai câu hỏi khác nhau. Mỗi gate phải có cặp fixture
đỏ và xanh chứng minh nó phân biệt được hai trạng thái, theo luật đã rút ở đợt dọn Phase 1.

| # | Gate | Kiểm gì | Nguồn |
|---|---|---|---|
| 1 | FONT-HTML | Font đầu stack Windows-safe hoặc nhúng base64 phủ dấu tiếng Việt | kế thừa |
| 2 | FONT-PDF | `BaseFont` thật trong PDF, FAIL nếu thấy Noto/Liberation/DejaVu/FreeSerif | **MỚI, từ P2b** |
| 3 | RASTER | Đếm `/Subtype /Image` qua `xref_object`, ngưỡng chỉnh lại cho WeasyPrint | kế thừa, chỉnh ngưỡng |
| 4 | DIACRITICS | FFFD, synthetic, mật độ dấu HTML so PDF | kế thừa |
| 5 | CHART-SONG | Mọi SVG phải parse được XML, và phải để lại nét vẽ trong PDF | **MỚI, từ bug 12 chart** |
| 6 | CALLOUT-BAKED | Nhãn callout khai trong nguồn phải có mặt trong tầng text của PDF | **MỚI, từ P3** |
| 7 | STYLE | Em-dash, en-dash, AI-slop, câu kết cách ngôn | kế thừa |
| 8 | PAGEBREAK | CSS bảo vệ, và hình học thật tìm panel bị cắt ngang biên trang | kế thừa |
| 9 | SOURCE-LEAK | Cụm từ cấm, tên riêng viết tắt, đối chiếu ledger ở chế độ external | kế thừa |
| 10 | LEDGER | Sổ nguồn hợp lệ: không mồ côi, không lệch bậc, không lệch đơn vị | kế thừa |

Gate 3 phải chỉnh ngưỡng: bộ cũ tuning cho Chromium với `IMAGE_OBJ_FAIL = 30`. WeasyPrint cộng
chart SVG cho 0 ảnh raster, nên ngưỡng đúng ở đây là 0, có một cửa cho ảnh chụp thật khai tường
minh trong front-matter.

## Các bước thi công

- [x] **B1. Bake minh hoạ.** `pipeline/bake_svg.mjs` mở HTML ví dụ bằng Chromium qua
      `scripts/lib/chromium.mjs`, chờ annotate chạy xong, lấy `outerHTML` SVG, ghi file tĩnh.
      Nghiệm thu: render bản bake qua WeasyPrint, đếm được đủ 7 callout trong tầng text, so với 0
      của bản gốc.

- [x] **B2. Dựng HTML.** `pipeline/build_html.py`: đọc front-matter, dựng markdown, xử lý ba
      directive `chart`, `minh-hoa`, `ngat-trang` cộng cú pháp `{{ma}}` cho số có nguồn, nhúng
      token và font base64, nhúng sổ nguồn vào `<script id="evidence-ledger">`, khai
      `data-theme="light"`. Directive `component` bỏ khỏi phạm vi: markdown vốn cho viết HTML
      thô, nên khối component chép thẳng từ `components/catalog/` vào bài là đủ và không đẻ
      thêm một lớp cú pháp phải bảo trì.

- [x] **B3. Xuất PDF.** `pipeline/render_pdf.py` gọi WeasyPrint, ghi xong thì mở lại đếm trang,
      đếm nét vẽ, đếm ảnh raster, và FAIL ngay nếu số trang bằng 0 hay nét vẽ bằng 0.

- [x] **B4. Mười gate.** Dời bảy gate cũ vào `gates/`, sửa theo luật repo, viết ba gate mới.
      Runner in bảng PASS, WARN, FAIL, SKIP và trả exit code.

- [x] **B5. Fixture đỏ và xanh.** Mỗi gate một cặp. Test tự động chạy cả cặp và ép: bản xanh phải
      PASS, bản đỏ phải FAIL. Một gate không đỏ được với fixture đỏ của chính nó là gate rỗng.

- [x] **B6. Orchestrator.** Nối chuỗi, ghi artifact ba checkpoint, chạy gate, trả exit code.

- [x] **B7. Báo cáo mẫu.** `examples/mau-phase2/`: 4 tới 6 trang, chạm cả hai engine chart, vài
      component, một minh hoạ có callout, ledger đủ nguồn gồm cả một nguồn `internal_only`.

- [x] **B8. Nghiệm thu end-to-end.** Một lệnh từ markdown ra PDF đã qua mười gate.

- [x] **B9. Bàn giao.** Cập nhật `CLAUDE.md`, `memory.md`, `SKILL.md`, `package.json`, commit.

## Nghiệm thu Phase 2

Phase 2 đóng khi cả năm điều sau đúng, chạy thật từ shell mới:

1. `python3 pipeline/orchestrator.py examples/mau-phase2/noi-dung.md` ra PDF, exit 0
2. `node gates/run.mjs <html> <pdf>` cho mười gate, không FAIL cứng
3. `npm test` và `pytest` vẫn xanh, cộng bộ test fixture đỏ và xanh của mười gate
4. Mỗi gate đã được kiểm là ĐỎ ĐƯỢC bằng fixture đỏ của chính nó
5. `npm run verify` vẫn exit 0
