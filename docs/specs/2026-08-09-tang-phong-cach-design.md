# Tầng phong-cách: thư viện hướng nghệ thuật có exemplar

Ngày: 2026-08-09. Trạng thái: đã duyệt hướng, chờ implementation plan.
Quyết định operator đã chốt: đủ 4 style + 4 exemplar trong arc này; nhung-toi dùng bảng
tối làm bộ mặt mặc định có khoá; nghi thức 3 bìa chỉ áp cho ấn phẩm mới; mở thêm luồng
deep research để tìm style thứ 5 trở đi.

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
  nhịp, một lớp CSS component, khí chất chart, tính cách motion cho làn html-song.
- Hai trục độc lập: thep-xanh có sang-lanh làm mặc định và toi-lanh cho trang nội bộ;
  nhung-toi có bảng tối làm mặc định và không cần bản dẫn xuất.

Phương án kiến trúc đã chọn: tầng compose (phương án A). Hai phương án bị loại:
phình themes JSON thành style object (generator phình, ma trận style nhân chủ đề rối);
kiểu frontend-slides mỗi style một design.md tự đủ để model tự ráp CSS (không nguồn
duy nhất, trôi fidelity, chính là điểm yếu đã điều tra ra).

## 2. Cấu trúc thư mục và hệ chọn ba tầng

```
phong-cach/
  INDEX.json          tầng 1: metadata chọn style, đọc mọi lúc
  README.md           luật của tầng, gồm luật exemplar
  thep-xanh/
    phong-cach.json   khai báo ghép
    preview.md        tầng 2: thẻ chọn ngắn, đọc khi shortlist
    design.md         tầng 3: spec đầy đủ, chỉ đọc sau khi chốt style
    lop.css           override component, đắp sau report.css
  giay-am/
  nhung-toi/
  poster-dac/
```

Progressive disclosure học từ frontend-slides: INDEX nhẹ để lọc, preview để so trong
shortlist, design.md chỉ nạp khi đã chốt. Cấm đọc design.md hàng loạt, ghi rõ trong
README của tầng.

### 2.1 Schema INDEX.json (ví dụ đầy đủ, không rút gọn)

```json
{
  "phien_ban": 1,
  "danh_sach": [
    {
      "slug": "thep-xanh",
      "tagline": "Blue editorial nghiêm, giọng báo cáo tổ chức, tin ở mật độ lập luận",
      "mood": ["nghiem-tuc", "to-chuc", "lanh"],
      "formality": "cao",
      "density": "cao",
      "chu_de_mac_dinh": "sang-lanh",
      "chu_de_dan_xuat": "toi-lanh",
      "best_for": ["bao-cao-nganh", "bao-cao-khoi-tao-ma", "cap-nhat-kqkd"],
      "avoid_for": ["thu-nha-dau-tu-giong-am"],
      "trang_thai": "chinh-thuc",
      "exemplar": "examples/van-tai-bien"
    },
    {
      "slug": "giay-am",
      "tagline": "Giấy kem ấm, serif chất văn, accent cam đất, giọng thư gửi người thật",
      "mood": ["am", "van-chuong", "gan-gui"],
      "formality": "trung-cao",
      "density": "trung",
      "chu_de_mac_dinh": "giay-am",
      "chu_de_dan_xuat": null,
      "best_for": ["tom-tat-dieu-hanh", "thu-nha-dau-tu"],
      "avoid_for": ["deep-dive-mat-do-cao"],
      "trang_thai": "vuon-uom",
      "exemplar": null
    }
  ]
}
```

Hai trạng thái: `chinh-thuc` (được SKILL chọn) và `vuon-uom` (đang dựng, cấm chọn).
Giá trị `best_for` và `avoid_for` lấy từ đúng bộ 7 loại ấn phẩm trong SKILL.md, viết
slug không dấu, test sẽ ép khớp từ vựng.

### 2.2 Schema phong-cach.json (ví dụ đầy đủ)

```json
{
  "slug": "giay-am",
  "chu_de_mac_dinh": "giay-am",
  "chu_de_dan_xuat": null,
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
  "chart": {
    "palette": "giay-am",
    "khi_chat": "duong-net-thanh, luoi-nhat, nhan-serif"
  },
  "motion": {
    "tinh_cach": "cham-va-am",
    "thoi_luong_goc_ms": 600
  }
}
```

Luật cứng của schema: KHÔNG chứa mã hex nào. Hex chỉ sống trong
`design-system/themes/*.json`. Font kit trỏ vào `design-system/fonts/` theo đúng quy
trình nhúng woff2 và trích ttf hiện có.

## 3. Đấu nối pipeline

- Front-matter `noi-dung.md` thêm khoá `phong-cach: <slug>`. Vắng khoá thì mặc định
  `thep-xanh`, mọi ấn phẩm cũ dựng lại ra kết quả cũ, không phá gì.
- `build_html.py` đọc `phong-cach.json` của style được chọn rồi làm bốn việc:
  1. khoá `data-theme` theo `chu_de_mac_dinh` của style (xem mục 4),
  2. nhúng font kit tương ứng thay cho kit mặc định,
  3. đắp `lop.css` SAU `report.css` trong cùng bản dựng tự đủ,
  4. truyền tên palette chart cho bước sinh hình.
- Chart ECharts lấy palette qua registry `PALETTES` theo tên chủ đề trong
  `charts/echarts/theme.mjs` (đã có sẵn từ 09-08). Chart matplotlib lấy qua `THEMES`
  trong `tokens.py`. Không thêm đường truyền màu mới nào.
- Gate không cần sửa cho việc đấu nối: FONT-HTML, FONT-PDF, DIACRITICS, THEME-MATCH
  đo trên file dựng ra nên tự áp cho mọi style. Chỗ duy nhất phải sửa gate là mục 4.

## 4. Luật khoá sáng tổng quát hoá

Luật cũ: file giao khách phải khai `data-theme="light"`. Lý do gốc ghi trong CLAUDE.md:
chart matplotlib và minh hoạ chỉ có bảng sáng, cộng WeasyPrint vứt khối
prefers-color-scheme.

Luật mới: file giao khách phải KHOÁ MỘT CHỦ ĐỀ TƯỜNG MINH bằng `data-theme` trên thẻ
html, không để máy khách quyết. Chủ đề bị khoá là `chu_de_mac_dinh` của phong cách.
Với thep-xanh, giay-am, poster-dac thì đó vẫn là chủ đề sáng, hành vi y như cũ. Với
nhung-toi, bộ mặt mặc định là bảng tối và bị khoá đúng như vậy: người đọc nào cũng
thấy đúng một bộ mặt.

Điều kiện hết hiệu lực của luật cũ, ghi lại theo đúng kỷ luật của repo: luật "phải là
light" hết lý do khi một phong cách tự mang bảng màu đủ cho MỌI loại hình nó dùng.
Nhung-toi đáp ứng bằng cách giới hạn loại hình (mục 8), không phải bằng cách vá bảng
màu cho toàn hệ.

Việc phải sửa kèm: mục luật cứng trong CLAUDE.md, doctrine/06-chu-de-toi.md, và gate
khoá chủ đề trong verify-components.mjs đổi phép đo từ "phải là light" sang "phải khai
tường minh và khớp chu_de_mac_dinh của phong cách trong front-matter".

## 5. Nghi thức 3 bìa 3 phong cách

Học từ cổng cứng của huashu-design nhưng thu phạm vi để chịu được chi phí định kỳ:

- Chỉ áp cho ấn phẩm MỚI, nhận diện bằng front-matter chưa có khoá `phong-cach:`.
- Checkpoint CK2 của orchestrator (hiện dựng 3 bìa cùng một giọng) mở rộng thành: dựng
  bìa cộng MỘT section mẫu bằng 3 style ứng viên, lọc từ INDEX theo loại ấn phẩm và
  formality. Ghi artifact ra thư mục, in đường dẫn, không hỏi y/n trên terminal, đúng
  quy ước checkpoint hiện hành.
- Operator chọn một, ghi `phong-cach:` vào front-matter. Các kỳ sau của cùng ấn phẩm
  giữ style, bỏ qua nghi thức.
- Ấn phẩm định kỳ đổi style là quyết định tay, không có đường tự động.

## 6. Luật exemplar, phiên bản đo được

Nguyên tắc: spec không có exemplar thì style chưa tồn tại trong catalog.

- Style chỉ được `trang_thai: "chinh-thuc"` khi có `examples/<exemplar>/` mà
  front-matter của nó tham chiếu đúng slug style, và có `nghiem-thu.json` commit ở GỐC
  thư mục ấn phẩm. Không đặt trong `ra/` vì `ra/` đã gitignore.
- `nghiem-thu.json` ghi: ngày chạy, git sha lúc chạy, lệnh tái tạo nguyên văn, kết quả
  từng gate. Ví dụ đầy đủ:

```json
{
  "ngay": "2026-08-09",
  "sha": "cd69e3f",
  "lenh_tai_tao": "python3 pipeline/orchestrator.py examples/van-tai-bien/noi-dung.md --lan=html-song",
  "lan": "html-song",
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

- Test mới `tests/consistency/phong_cach.test.mjs` ép: INDEX đúng schema và đúng từ
  vựng 7 loại ấn phẩm; entry chinh-thuc có exemplar tồn tại, front-matter khớp slug,
  nghiem-thu.json hợp lệ và không có gate FAIL; SKIP phải kèm ly_do; entry vuon-uom
  không có exemplar thì không sao nhưng cấm SKILL chọn. Test có cặp fixture đỏ xanh
  theo đúng luật gate của repo.
- Giới hạn nói thẳng: nghiem-thu.json là BẢN GHI tại một sha, không phải bằng chứng
  sống. Tái kiểm bằng cách chạy lại lệnh trong `lenh_tai_tao`. Test consistency chỉ ép
  tính hợp lệ của bản ghi, không chạy lại orchestrator trong npm test để giữ suite
  nhanh.

## 7. Spec format design.md của từng style

Các phần bắt buộc, theo thứ tự:

1. Khí chất và mood: ấn phẩm mặc giọng này thì người nhận cảm thấy gì, ba câu.
2. Nguồn màu: chỉ TÊN chủ đề và tên token, cấm lặp hex. Nói quan hệ vai trò
   (accent dùng cho gì, pos neg dùng ở đâu) chứ không nói giá trị.
3. Chữ: cặp font, thang chữ, quan hệ với thang mặc định, quy tắc riêng nếu lệch
   doctrine/03-viet-chu.md. Không lặp quy tắc tiếng Việt chung.
4. Blueprint theo 7 loại ấn phẩm: mỗi loại nói bố cục vào bài, component nào trong
   `components/` hợp giọng, preset chart nào trong `charts/` hợp khí chất, cái nào
   TRÁNH. Đây là chỗ map tài sản sẵn có vào style, không vẽ lại tài sản.
5. Motion (làn html-song): tính cách, thời lượng gốc, easing, cái gì không bao giờ
   animate.
6. Anti-pattern riêng của style: tối đa 10 dòng, mỗi dòng một thứ cấm và một câu lý do.
7. Known Gaps: giới hạn thành thật, kèm điều kiện gỡ. Học trực tiếp từ frontend-slides
   và khớp bài học "gate đòi bằng chứng tạo động cơ bịa bằng chứng": cho spec được nói
   thật về chỗ nó chưa chứng minh.

## 8. Bốn style và bốn exemplar của arc này

| Style | Khí chất | Chủ đề màu | Exemplar | Làn |
|---|---|---|---|---|
| thep-xanh | blue editorial tổ chức, hiện trạng | sang-lanh, dẫn xuất toi-lanh | van-tai-bien, đã 8 PASS 0 FAIL 1 SKIP | html-song |
| giay-am | giấy kem ấm, serif chất văn, accent cam đất | giay-am (mới) | tóm tắt điều hành, số mock khai rõ | pdf-so |
| nhung-toi | navy than sâu, accent vàng đồng, deal pack | nhung-toi (mới, tối mặc định) | deal pack chào vốn hư cấu | html-song |
| poster-dac | mật độ cao kiểu poster dữ liệu, chữ hiển thị lớn | poster-dac (mới) | deep-dive ngành mật độ cao | html-song |

Ràng buộc thi công theo style:

- thep-xanh: harvest giọng hiện tại thành design.md, thêm front-matter và
  nghiem-thu.json cho van-tai-bien. Không đổi một giá trị thị giác nào.
- giay-am: exemplar đi làn pdf-so vì tóm tắt điều hành là loại hay bị chuyển tiếp
  nhất; ăn trọn 10 gate làn pdf, gồm FONT-PDF với font kit mới.
- nhung-toi: exemplar CHỈ dùng ECharts và minh hoạ SVG (hai loại đã đổi màu qua var),
  TRÁNH matplotlib EIR cho tới khi có bảng tối cho nó. Ghi thành Known Gap trong
  design.md của style.
- poster-dac: chọn deep-dive mật độ cao làm exemplar một cách cố ý, vì style này dễ
  đụng PAGEBREAK và RESPONSIVE-WIDTH nhất; exemplar phải chứng minh đúng chỗ khó.

Số liệu trong ba exemplar mới đều là số minh hoạ dựng để nghiệm thu đường ống, khai rõ
ngay đầu ấn phẩm theo tiền lệ van-tai-bien, không mượn số công bố của tổ chức thật.

## 9. Deep research style thứ 5 trở đi

Lập `research/12-style-directions/` theo đúng quan hệ research sang doctrine của repo:

- Khảo nguồn local: 40 style của huashu-design, 34 template của frontend-slides,
  catalog html-ppt, đã nằm sẵn trên máy.
- Khảo web: giải thưởng thiết kế annual report, ngôn ngữ đồ hoạ FT, Economist,
  Bloomberg, deck ngân hàng đầu tư.
- Soi mặt bằng báo cáo CTCK Việt Nam để định vị khác biệt.
- Đầu ra: shortlist xếp hạng theo ba tiêu chí: khác biệt thật với 4 style đã có, khả
  thi với hệ gate hiện hành, phủ được loại ấn phẩm đang thiếu giọng. Ứng viên tốt vào
  INDEX ở trạng thái vuon-uom, chờ arc sau dựng exemplar.

## 10. Rủi ro chính và cách trả

| Rủi ro | Cách trả |
|---|---|
| Font kit mới cho 3 style: nhúng woff2, trích ttf, phủ dấu tiếng Việt | đi đúng quy trình extract-ttf.py hiện có; gate FONT-HTML, FONT-PDF, DIACRITICS đã canh sẵn; nhớ bẫy IBM Plex SemiBold đổi nameID |
| Bảng tối nhung-toi cho chart tĩnh | chỉ dùng đường var() đã có; THEME-MATCH canh; cấm matplotlib trong exemplar |
| poster-dac tràn trang, tràn khung hẹp | chính exemplar được chọn để thử; PAGEBREAK và RESPONSIVE-WIDTH là tiêu chí nghiệm thu số một của style này |
| design.md lặp hex rồi trôi so với themes JSON | luật cấm hex trong phong-cach.json và design.md, soát khi review; nguồn hex duy nhất vẫn là themes JSON |
| Tầng mới làm SKILL.md phình | SKILL chỉ thêm một bước định tuyến đọc INDEX; nội dung sâu nằm ở design.md từng style, nạp theo nhu cầu |

## 11. Ngoài phạm vi arc này

- Không rename sang-lanh, toi-lanh (41 chỗ dùng, đổi tên không mua được gì).
- Không làm nút đổi chủ đề động trong trang (giới hạn mount một lần đã ghi ở
  doctrine/06, giữ nguyên).
- Không làm bảng tối cho matplotlib EIR.
- Không làm làn slide trình chiếu; nếu tương lai cần, cân nhắc mượn runtime
  presenter-mode của html-ppt, đã ghi nhận trong điều tra 09-08.
- Không dựng exemplar cho style vườn ươm ra từ luồng research.
