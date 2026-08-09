# Tầng phong-cách: thư viện hướng nghệ thuật có exemplar

Ngày: 2026-08-09. Trạng thái: v2 sau phản biện 3 worker, chờ implementation plan.
Quyết định operator đã chốt: đủ 4 style + 4 exemplar trong arc này; nhung-toi dùng bảng
tối làm bộ mặt mặc định có khoá; nghi thức 3 bìa chỉ áp cho ấn phẩm mới; mở thêm luồng
deep research để tìm style thứ 5 trở đi.

Lịch sử bản: v1 commit 79e55d0. v2 hấp thụ phản biện broadcast (agy, codex, kimi),
danh sách sửa đổi ở mục 12.

## 0. Vấn đề

Repo có 116 tài sản hình nhưng gần như một giọng thẩm mỹ duy nhất (blue editorial của
sang-lanh). Độ đa dạng đang nằm ở tầng "vẽ hình gì", trong khi cái quyết định khí chất
một ấn phẩm là tầng hướng nghệ thuật: màu, font, nhịp khối, cách vào bài, tính cách
motion. Điều tra ngày 09-08 trên ba skill cộng đồng (huashu-design 40 style,
frontend-slides 34 template, html-ppt 36 theme) cho hai bài học ngược chiều:

- huashu-design và frontend-slides đẹp nhờ THƯ VIỆN HƯỚNG NGHỆ THUẬT có kỷ luật,
  không phải nhờ số lượng chart.
- frontend-slides có 34 spec sâu nhưng 0 bản render mẫu, nghĩa là chưa template nào
  được chứng minh. Đúng bài học sẵn có của repo: gate chưa chạy trên ấn phẩm thật là
  gate chưa được kiểm.

Tầng phong-cách sinh ra để lấy cái hay thứ nhất mà không lặp cái dở thứ hai.

## 1. Khái niệm

- `chu-de` (đã có, giữ nguyên): bảng MÀU, nguồn duy nhất ở `design-system/themes/*.json`,
  sinh ba đích qua `generate-tokens.mjs`.
- `phong-cach` (mới): bản khai báo GHÉP đứng trên chủ đề. Một phong cách gồm: chủ đề màu
  mặc định (bắt buộc) và chủ đề dẫn xuất (tuỳ chọn), font kit, override token khối và
  nhịp, một lớp CSS component. Khí chất chart và tính cách motion là NỘI DUNG THIẾT KẾ,
  sống trong design.md của style, không nằm trong schema JSON (xem mục 2.2).
- Hai trục độc lập: thep-xanh có sang-lanh làm mặc định và toi-lanh cho trang nội bộ;
  nhung-toi có bảng tối làm mặc định và không cần bản dẫn xuất.

Phương án kiến trúc đã chọn: tầng compose (phương án A). Hai phương án bị loại:
phình themes JSON thành style object (generator phình, ma trận style nhân chủ đề rối);
kiểu frontend-slides mỗi style một design.md tự đủ để model tự ráp CSS (không nguồn
duy nhất, trôi fidelity, chính là điểm yếu đã điều tra ra).

## 2. Cấu trúc thư mục và hệ chọn hai tầng

```
phong-cach/
  INDEX.json          SINH TỰ ĐỘNG từ các phong-cach.json, cấm sửa tay
  sinh-index.mjs      script sinh INDEX, chạy lại sau mỗi lần sửa phong-cach.json
  README.md           luật của tầng, gồm luật exemplar
  thep-xanh/
    phong-cach.json   nguồn sự thật DUY NHẤT của style: khai báo ghép + metadata chọn
    design.md         spec đầy đủ, chỉ đọc sau khi chốt style
    lop.css           override component, đắp sau report.css, theo contract mục 3.1
  giay-am/
  nhung-toi/
  poster-dac/
```

Hai tầng thay vì ba: INDEX nhẹ để lọc và shortlist, design.md chỉ nạp khi đã chốt.
`preview.md` của bản v1 đã cắt (đồng thuận 2/3 worker): với quy mô dưới 10 style,
tagline cộng mood cộng best_for trong INDEX là đủ để chọn, thêm một file trung gian
chỉ thêm một nơi để trôi. Cấm đọc design.md hàng loạt, ghi rõ trong README của tầng.

INDEX.json là BẢN SINH: `sinh-index.mjs` gom metadata từ các `phong-cach.json` cộng
kết quả đọc `nghiem-thu.json` của exemplar. Test drift ép INDEX khớp nguồn, cùng kiểu
kỷ luật với `generate-tokens.mjs`. Hết đường trùng nguồn sự thật giữa hai file.

### 2.1 Schema phong-cach.json (nguồn duy nhất, ví dụ đầy đủ)

```json
{
  "slug": "giay-am",
  "tagline": "Giấy kem ấm, serif chất văn, accent cam đất, giọng thư gửi người thật",
  "mood": ["am", "van-chuong", "gan-gui"],
  "formality": "trung-cao",
  "density": "trung",
  "best_for": ["tom-tat-dieu-hanh", "thu-nha-dau-tu"],
  "avoid_for": ["deep-dive-mat-do-cao"],
  "chu_de_mac_dinh": "giay-am",
  "chu_de_dan_xuat": null,
  "gioi_han_loai_hinh": [],
  "font": {
    "kit": "giay-am",
    "hien_thi": "Fraunces",
    "van_ban": "Source Serif 4",
    "so_va_nhan": "IBM Plex Mono"
  },
  "token_override": {
    "--radius-khoi": "2px",
    "--space-nhip-doan": "var(--space-6)"
  },
  "chart_palette": "giay-am",
  "exemplar": "examples/tom-tat-dieu-hanh-mau",
  "trang_thai": "vuon-uom"
}
```

Ghi chú schema, mỗi dòng một luật có lý do:

- `best_for`, `avoid_for` lấy từ đúng bộ 7 loại ấn phẩm trong SKILL.md, slug không
  dấu, test ép khớp từ vựng.
- `gioi_han_loai_hinh`: mảng loại hình bị CẤM trong style này. Style có
  `chu_de_mac_dinh` là chủ đề tối BẮT BUỘC khai `["matplotlib"]` trở lên, test ép
  (phản biện kimi: điều kiện hết hiệu lực của luật khoá phải có gate ép, không chỉ
  ghi lại). `build_html.py` gặp directive dùng loại hình bị cấm thì DỪNG build.
- `token_override`: cơ chế tiêu thụ tường minh: `build_html.py` sinh một block
  `<style data-token-phong-cach>` đặt SAU tokens.css và TRƯỚC lop.css. Giá trị chỉ
  được là `var()` reference hoặc literal PHI MÀU; cấm hex, `rgb()`, `hsl()`,
  `oklch()`, `color-mix()` với literal (phản biện codex: đường lách luật một nguồn
  hex). Test quét cả token_override lẫn lop.css lẫn design.md.
- KHÔNG có khối `motion` và `khi_chat` trong JSON (đồng thuận 3/3: dữ liệu chết,
  không consumer nào trong pipeline). Hai thứ đó là hướng dẫn thiết kế, sống trong
  design.md mục 5 và 4; thời lượng motion nếu style cần thì khai thẳng biến CSS
  trong lop.css.
- `trang_thai` và `exemplar` nằm ở đây để INDEX sinh được toàn phần; `sinh-index.mjs`
  hạ cấp `chinh-thuc` xuống `vuon-uom` trong INDEX nếu nghiem-thu.json thiếu hoặc
  không hợp lệ, và ghi thêm trường dẫn xuất `lan_da_chung_minh` (mục 6).

### 2.2 INDEX.json sinh ra (ví dụ đầy đủ một entry)

```json
{
  "phien_ban": 2,
  "sinh_boi": "phong-cach/sinh-index.mjs",
  "danh_sach": [
    {
      "slug": "thep-xanh",
      "tagline": "Blue editorial nghiêm, giọng báo cáo tổ chức, tin ở mật độ lập luận",
      "mood": ["nghiem-tuc", "to-chuc", "lanh"],
      "formality": "cao",
      "density": "cao",
      "best_for": ["bao-cao-nganh", "bao-cao-khoi-tao-ma", "cap-nhat-kqkd"],
      "avoid_for": ["thu-nha-dau-tu-giong-am"],
      "chu_de_mac_dinh": "sang-lanh",
      "trang_thai": "chinh-thuc",
      "exemplar": "examples/van-tai-bien",
      "lan_da_chung_minh": ["html-song"]
    }
  ]
}
```

`lan_da_chung_minh` đọc từ trường `lan` của nghiem-thu.json (phản biện kimi: mỗi
exemplar chỉ chứng minh một làn; SKILL không được chọn style cho làn chưa có bằng
chứng). Một style muốn chứng minh làn thứ hai thì exemplar thứ hai hoặc chạy lại
orchestrator với làn thứ hai trên cùng exemplar, sinh nghiem-thu bổ sung.

## 3. Đấu nối pipeline

- Front-matter `noi-dung.md` BẮT BUỘC có khoá `phong-cach: <slug>`. Vắng khoá thì
  build DỪNG với thông báo chỉ cách chạy nghi thức chọn hướng (mục 5). Không có
  default im lặng (đồng thuận 3/3: default im lặng cộng nhận diện ấn phẩm mới bằng
  vắng khoá là mâu thuẫn tự thân). Hai ấn phẩm hiện có backfill ngay trong arc:
  `examples/mau-phase2` và `examples/van-tai-bien` thêm dòng `phong-cach: thep-xanh`.
- `build_html.py` đọc `phong-cach.json` của style được khai rồi làm năm việc:
  1. khoá `data-theme` theo `chu_de_mac_dinh` của style (xem mục 4),
  2. gắn `data-phong-cach="<slug>"` lên thẻ html để lop.css scope vào,
  3. nhúng font kit tương ứng thay cho kit mặc định,
  4. sinh block token_override rồi đắp `lop.css` theo thứ tự cascade ở mục 3.1,
  5. truyền `chart_palette` cho bước sinh hình, và DỪNG nếu gặp loại hình nằm trong
     `gioi_han_loai_hinh`.
- Chart ECharts lấy palette qua registry `PALETTES` theo tên chủ đề trong
  `charts/echarts/theme.mjs`. Chart matplotlib lấy qua `THEMES` trong `tokens.py`.
  ĐƯỜNG ỐNG có sẵn nhưng DỮ LIỆU thì chưa: PALETTES và THEMES hiện chỉ có sang-lanh
  và toi-lanh (kimi đã kiểm tận file). Thêm ba chủ đề mới là BƯỚC LỚN RIÊNG của arc:
  ba file JSON mới, chạy generator, kiểm contrast từng chủ đề theo đúng chuẩn WCAG đã
  ghi trong themes JSON hiện có, không phải việc đấu nối vặt.
- Gate FONT-HTML, FONT-PDF, DIACRITICS đo trên file dựng ra nên tự áp cho mọi style.
  Gate khoá chủ đề sửa theo mục 4.

### 3.1 Contract của lop.css

Phản biện codex: đắp CSS tự do sau report.css là mở cửa cho style phá component và
lách luật màu mà gate không thấy. Contract bốn điều, có test:

1. Mọi selector trong lop.css phải nằm dưới scope `[data-phong-cach="<slug>"]` của
   chính style đó. Cấm selector trần.
2. Cấm hex và hàm màu literal; màu chỉ qua `var(--token)`. Cùng phép quét với
   token_override.
3. Thứ tự cascade cố định và được test: tokens.css, rồi block token_override, rồi
   components.css và report.css, rồi lop.css. Lop.css thắng là CHỦ Ý; thứ nó không
   được phép làm là định nghĩa lại giá trị token màu (điều 2 chặn).
4. Style có exemplar làn pdf-so: lop.css phải qua lint WeasyPrint-safe, cấm các thuộc
   tính đã biết WeasyPrint bỏ qua hoặc phá (danh sách trong CLAUDE.md: aspect-ratio,
   overflow trên table, writing-mode, cộng blur và backdrop-filter vốn cấm toàn cục).
   Style cần CSS màn hình riêng cho làn song thì tách phần đó vào media screen.

## 4. Luật khoá chủ đề tổng quát hoá

Luật cũ: file giao khách phải khai `data-theme="light"`. Lý do gốc ghi trong CLAUDE.md:
chart matplotlib và minh hoạ chỉ có bảng sáng, cộng WeasyPrint vứt khối
prefers-color-scheme.

Luật mới: file giao khách phải KHOÁ MỘT CHỦ ĐỀ TƯỜNG MINH bằng `data-theme` trên thẻ
html, và chủ đề bị khoá phải KHỚP `chu_de_mac_dinh` của phong cách khai trong
front-matter. Với thep-xanh, giay-am, poster-dac thì đó vẫn là chủ đề sáng, hành vi y
như cũ. Với nhung-toi, bộ mặt mặc định là bảng tối và bị khoá đúng như vậy: người đọc
nào cũng thấy đúng một bộ mặt.

Vị trí phép đo, sửa theo phản biện kimi (đã kiểm code thật): phép đo hiện nằm trong
`scripts/verify-components.mjs` và đo trên gallery, nơi KHÔNG có front-matter. Vậy:

- Gate mới "KHOA-CHU-DE" đặt ở tầng gate ấn phẩm: `gates/gates.mjs` (làn pdf-so) và
  `gates/gates_song.mjs` (làn html-song), so `data-theme` của file dựng ra với
  `chu_de_mac_dinh` của style trong front-matter. Có cặp fixture đỏ xanh.
- `verify-components.mjs` GIỮ NGUYÊN luật light cho gallery: gallery không phải ấn
  phẩm, không có front-matter, và bảng màu tối của gallery đã có đường kiểm riêng.

Điều kiện hết hiệu lực của luật cũ, nay có gate ép chứ không chỉ ghi lại: style có
chủ đề mặc định tối bắt buộc khai `gioi_han_loai_hinh` chứa ít nhất matplotlib, test
schema ép, build dừng khi vi phạm (mục 2.1).

Việc phải sửa kèm: mục luật cứng trong CLAUDE.md, doctrine/06-chu-de-toi.md.

## 5. Nghi thức 3 bìa 3 phong cách

Học từ cổng cứng của huashu-design nhưng thu phạm vi để chịu được chi phí định kỳ.
Kích hoạt TƯỜNG MINH, không suy diễn từ trạng thái front-matter (đồng thuận 3/3):

- Lệnh: `python3 pipeline/orchestrator.py <bao-cao>/noi-dung.md --nghi-thuc-huong`.
  Chạy khi khởi tạo ấn phẩm mới, hoặc bất cứ khi nào operator muốn xem lại hướng.
- Nghi thức dựng bìa cộng MỘT section mẫu bằng 3 style ứng viên: lọc entry
  `chinh-thuc` trong INDEX theo loại ấn phẩm (best_for, avoid_for), formality, và
  `lan_da_chung_minh` phải chứa làn của ấn phẩm. Ghi artifact ra thư mục, in đường
  dẫn, không hỏi y/n trên terminal, đúng quy ước checkpoint hiện hành.
- Operator chọn một, ghi `phong-cach:` vào front-matter. Từ đó build chạy thẳng.
- Build thường không có khoá `phong-cach:` thì DỪNG và chỉ sang lệnh nghi thức. Ấn
  phẩm cũ đã backfill nên không bao giờ rơi vào nhánh này.

## 6. Luật exemplar, phiên bản máy sinh

Nguyên tắc: spec không có exemplar thì style chưa tồn tại trong catalog.

- Style chỉ được `trang_thai: "chinh-thuc"` khi có `examples/<exemplar>/` mà
  front-matter tham chiếu đúng slug style, và có `nghiem-thu.json` hợp lệ ở GỐC thư
  mục ấn phẩm. Không đặt trong `ra/` vì `ra/` đã gitignore.
- `nghiem-thu.json` do MÁY SINH, không viết tay: `gates/run.mjs` thêm cờ
  `--ghi-nghiem-thu=<đường-dẫn>` ghi thẳng kết quả từng gate cộng ngày, git sha, lệnh
  tái tạo nguyên văn, làn. Sửa theo phản biện codex cộng bài học sẵn có của memory:
  gate đòi bằng chứng viết tay là tạo động cơ bịa bằng chứng; cho máy ghi thì hết
  chỗ bịa. Ví dụ đầy đủ:

```json
{
  "sinh_boi": "gates/run.mjs --ghi-nghiem-thu",
  "ngay": "2026-08-09",
  "sha": "cd69e3f",
  "lenh_tai_tao": "python3 pipeline/orchestrator.py examples/van-tai-bien/noi-dung.md --lan=html-song",
  "lan": "html-song",
  "phien_ban_bo_gate": "song-9",
  "gate": [
    { "ten": "OFFLINE", "ket_qua": "PASS" },
    { "ten": "JS-SILENT-FAIL", "ket_qua": "PASS" },
    { "ten": "REDUCED-MOTION", "ket_qua": "SKIP", "ly_do": "trang khong co animation CSS o che do thuong" },
    { "ten": "KEYBOARD-PATH", "ket_qua": "PASS" },
    { "ten": "CONTRAST-ALL-THEMES", "ket_qua": "PASS" },
    { "ten": "SIZE-BUDGET", "ket_qua": "PASS" },
    { "ten": "NO-JS-CONTENT", "ket_qua": "PASS" },
    { "ten": "RESPONSIVE-WIDTH", "ket_qua": "PASS" },
    { "ten": "THEME-MATCH", "ket_qua": "PASS" }
  ]
}
```

- Test mới `tests/consistency/phong_cach.test.mjs` ép:
  1. mọi phong-cach.json đúng schema, đúng từ vựng 7 loại ấn phẩm, chu_de trỏ theme
     có thật;
  2. INDEX.json khớp bản sinh lại từ nguồn (drift test);
  3. entry chinh-thuc: exemplar tồn tại, front-matter khớp slug, nghiem-thu.json hợp
     lệ, không gate FAIL, SKIP phải kèm ly_do;
  4. TẬP TÊN GATE trong nghiem-thu phải khớp registry gate hiện hành của làn đó
     (phản biện kimi cộng codex: thêm gate thứ 10 mà exemplar cũ vẫn xanh là lỗ
     hổng; trường phien_ban_bo_gate cộng phép so tập tên chặn nó, exemplar cũ tự đỏ
     và phải chạy lại nghiệm thu);
  5. token_override, lop.css, design.md không chứa hex và hàm màu literal;
  6. style chủ đề tối có gioi_han_loai_hinh hợp lệ;
  7. blueprint trong design.md: mọi tài sản nhắc tới bằng backtick slug phải tồn tại
     thật trong components/, charts/, illustrations/ (phản biện codex).
  Test có cặp fixture đỏ xanh theo đúng luật gate của repo.
- Smoke tái nghiệm thu, NGOÀI npm test để giữ suite nhanh: script
  `npm run nghiem-thu` chạy lại orchestrator cộng gate cho MỌI exemplar chinh-thuc
  rồi ghi đè nghiem-thu.json. Chạy trước mỗi lần merge nhánh lớn và mỗi lần đổi
  gate, token, font.
- Giới hạn nói thẳng: nghiem-thu.json vẫn là BẢN GHI tại một sha. Phép so tập gate
  làm nó tự đỏ khi bộ gate đổi, npm run nghiem-thu là đường tái tạo một lệnh.

## 7. Spec format design.md của từng style

Các phần bắt buộc, theo thứ tự:

1. Khí chất và mood: ấn phẩm mặc giọng này thì người nhận cảm thấy gì, ba câu.
2. Nguồn màu: chỉ TÊN chủ đề và tên token, cấm lặp hex (test mục 6 quét). Nói quan
   hệ vai trò chứ không nói giá trị.
3. Chữ: cặp font, thang chữ, quan hệ với thang mặc định, quy tắc riêng nếu lệch
   doctrine/03-viet-chu.md. Không lặp quy tắc tiếng Việt chung.
4. Blueprint theo 7 loại ấn phẩm: dạng bảng gọn, mỗi loại một hàng: bố cục vào bài,
   component hợp giọng, preset chart hợp khí chất, cái nào TRÁNH. Tài sản nhắc bằng
   backtick slug để test tham chiếu được (mục 6.7). Phần văn xuôi chỉ dành cho
   rationale, không lặp lại bảng (phản biện codex: blueprint 7 loại dạng prose là
   khối tài liệu phình không kiểm được).
5. Motion cho làn html-song: tính cách, easing, cái gì không bao giờ animate. Thời
   lượng khai bằng biến CSS trong lop.css nếu style cần.
6. Anti-pattern riêng của style: tối đa 10 dòng, mỗi dòng một thứ cấm và một câu lý do.
7. Known Gaps: giới hạn thành thật, kèm điều kiện gỡ. Style chủ đề tối bắt buộc có
   dòng về matplotlib và làn pdf-so.

## 8. Bốn style và bốn exemplar của arc này

| Style | Khí chất | Chủ đề màu | Exemplar | Làn chứng minh |
|---|---|---|---|---|
| thep-xanh | blue editorial tổ chức, hiện trạng | sang-lanh, dẫn xuất toi-lanh | van-tai-bien, đã 8 PASS 0 FAIL 1 SKIP | html-song |
| giay-am | giấy kem ấm, serif chất văn, accent cam đất | giay-am (mới) | tóm tắt điều hành, số mock khai rõ | pdf-so |
| nhung-toi | navy than sâu, accent vàng đồng, deal pack | nhung-toi (mới, tối mặc định) | deal pack chào vốn hư cấu | html-song |
| poster-dac | mật độ cao kiểu poster dữ liệu, chữ hiển thị lớn | poster-dac (mới) | deep-dive ngành mật độ cao | html-song |

Trạng thái cuối arc: cả bốn entry chinh-thuc trong INDEX. Trong lúc thi công, ba
style mới đứng ở vuon-uom; mọi ví dụ JSON trong spec này minh hoạ trạng thái GIỮA
arc, không phải trạng thái đích (làm rõ theo phản biện codex).

Ràng buộc thi công theo style:

- thep-xanh: harvest giọng hiện tại thành design.md, backfill front-matter, chạy
  `gates/run.mjs --ghi-nghiem-thu` trên van-tai-bien. Tiêu chí số một: bản dựng lại
  TRÙNG bản hiện tại từng byte của phần nội dung, chứng minh tầng compose không đổi
  hiện trạng.
- giay-am: exemplar đi làn pdf-so, ăn trọn 10 gate pdf với font kit mới. Quyết định
  tường minh theo phản biện kimi: nếu exemplar dùng chart matplotlib thì font kit
  giay-am PHẢI có bản ttf trích qua extract-ttf.py cho matplotlib, cùng bước với
  nhúng woff2, không để chart mang font kit cũ.
- nhung-toi: exemplar CHỈ dùng ECharts và minh hoạ SVG; `gioi_han_loai_hinh` chứa
  matplotlib, build dừng nếu vi phạm.
- poster-dac: chọn deep-dive mật độ cao làm exemplar một cách cố ý, vì style này dễ
  đụng PAGEBREAK và RESPONSIVE-WIDTH nhất; exemplar phải chứng minh đúng chỗ khó.

Số liệu trong ba exemplar mới đều là số minh hoạ dựng để nghiệm thu đường ống, khai rõ
ngay đầu ấn phẩm theo tiền lệ van-tai-bien, không mượn số công bố của tổ chức thật.

## 9. Deep research style thứ 5 trở đi

Track SONG SONG, không nằm trên đường găng của 4 style (làm rõ theo phản biện codex
và kimi; operator giữ quyết định mở luồng này trong arc):

- Lập `research/12-style-directions/` theo đúng quan hệ research sang doctrine.
- Khảo nguồn local: 40 style của huashu-design, 34 template của frontend-slides,
  catalog html-ppt, đã nằm sẵn trên máy.
- Khảo web: giải thưởng thiết kế annual report, ngôn ngữ đồ hoạ FT, Economist,
  Bloomberg, deck ngân hàng đầu tư.
- Soi mặt bằng báo cáo CTCK Việt Nam để định vị khác biệt.
- Đầu ra: shortlist xếp hạng theo ba tiêu chí: khác biệt thật với 4 style đã có, khả
  thi với hệ gate hiện hành, phủ được loại ấn phẩm đang thiếu giọng. Ứng viên tốt
  thành thư mục style ở trạng thái vuon-uom, chờ arc sau dựng exemplar.

## 10. Rủi ro chính và cách trả

| Rủi ro | Cách trả |
|---|---|
| Ba chủ đề màu mới nhân ba đích sinh cộng palette chart: khối việc lớn nhất arc | tách thành bước riêng trong plan; mỗi chủ đề qua generator, kiểm contrast theo chuẩn WCAG ghi trong themes JSON; CONTRAST-ALL-THEMES đo trên exemplar |
| Font kit mới cho 3 style: nhúng woff2, trích ttf, phủ dấu tiếng Việt | quy trình extract-ttf.py hiện có; gate FONT-HTML, FONT-PDF, DIACRITICS canh; bẫy IBM Plex SemiBold đổi nameID đã ghi trong CLAUDE.md |
| lop.css phá component hoặc lách luật màu | contract mục 3.1 cộng test quét; scope theo slug |
| Bảng tối nhung-toi cho chart tĩnh | chỉ dùng đường var() đã có; THEME-MATCH canh; gioi_han_loai_hinh chặn matplotlib từ build |
| poster-dac tràn trang, tràn khung hẹp | chính exemplar được chọn để thử; PAGEBREAK và RESPONSIVE-WIDTH là tiêu chí nghiệm thu số một |
| Bộ gate đổi làm nghiem-thu cũ thành bằng chứng mốc | phép so tập tên gate với registry theo làn làm exemplar cũ tự đỏ; npm run nghiem-thu tái tạo một lệnh |

## 11. Ngoài phạm vi arc này

- Không rename sang-lanh, toi-lanh (41 chỗ dùng, đổi tên không mua được gì).
- Không làm nút đổi chủ đề động trong trang.
- Không làm bảng tối cho matplotlib EIR.
- Không làm làn slide trình chiếu; nếu tương lai cần, cân nhắc mượn runtime
  presenter-mode của html-ppt, đã ghi nhận trong điều tra 09-08.
- Không dựng exemplar cho style vườn ươm ra từ luồng research.

## 12. Nhật ký phản biện v1 sang v2

Broadcast 09-08 tới ba worker (agy, codex, kimi), prompt giống hệt nhau. Phán quyết:
agy và kimi DUYET-CO-DIEU-KIEN, codex LAM-LAI. Sửa đổi đã hấp thụ:

1. Bỏ default im lặng thep-xanh; front-matter bắt buộc khai, backfill hai ấn phẩm cũ;
   nghi thức 3 bìa kích hoạt bằng cờ CLI (3/3 worker bắt cùng một mâu thuẫn).
2. INDEX.json thành bản sinh từ phong-cach.json, hết trùng nguồn (agy).
3. Cắt preview.md (agy, kimi).
4. Cắt motion và khi_chat khỏi schema JSON; token_override có cơ chế tiêu thụ và
   allowlist giá trị (3/3).
5. Contract lop.css bốn điều, gồm lint WeasyPrint-safe cho style làn pdf (agy, codex).
6. Gate khoá chủ đề đặt đúng tầng gates.mjs và gates_song.mjs, verify-components giữ
   nguyên cho gallery (kimi, đã kiểm code thật).
7. Thêm lan_da_chung_minh; SKILL và nghi thức chỉ chọn style cho làn có bằng chứng
   (kimi).
8. nghiem-thu.json máy sinh qua cờ mới của gates/run.mjs; phép so tập gate với
   registry; npm run nghiem-thu (codex, kimi).
9. Ghi nhận đúng cỡ khối việc ba chủ đề màu mới (kimi, đã kiểm PALETTES và THEMES
   chỉ có hai entry).
10. Blueprint dạng bảng, tài sản backtick slug có test tham chiếu (codex).
11. gioi_han_loai_hinh cho style tối, có test và build dừng (kimi).
12. Research ghi rõ là track song song không chặn đường găng (codex, kimi; giữ trong
    arc theo quyết định operator).

Phát hiện KHÔNG nhận và lý do: codex đề nghị manifest palette theo từng asset cộng
gate đối chiếu; với quy mô hiện tại, KHOA-CHU-DE cộng THEME-MATCH cộng gioi_han đã
phủ các đường lệch thật, manifest per-asset là hạ tầng thêm một tầng đồng bộ chưa trả
được giá; ghi lại đây để mở lại nếu xuất hiện ca lệch palette mà hai gate kia mù.
