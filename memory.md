# HT-viz-rendering: bàn giao cho phiên mới

Đọc file này trước tiên. Nó cho biết đang ở đâu và làm gì tiếp.

## 27-08: ấn phẩm html-song THẬT đầu tiên (PDR) lôi ra lỗi tiêu đề đóng cứng ở 4 preset

Ấn phẩm `bao-cao/pdr-2026-08-27/` (báo cáo cổ phiếu PDR từ engine HLPP + news engine, 5 chart
sống, 9 gate PASS, đã chép ra Desktop Windows) là bản html-song đầu tiên dùng số THẬT. Nó lộ
ra thứ bản mẫu vận tải biển không lộ vì bản mẫu vốn là số minh hoạ: preset 09, 07, 13, 14
ĐÓNG CỨNG tiêu đề và phụ đề trong `option()`, kể cả chuỗi "mã minh hoạ VNM" và "minh hoạ
FY2026, không phải số thật", nên hình giao khách in nguyên câu đó lên số thật. Vá tối thiểu:
cả bốn nay đọc `params.title ?? <mặc định cũ>` và `params.subtitle ?? ...`, cùng kiểu preset 11
đã làm từ đầu; MAC_DINH không đổi nên catalog và test giữ nguyên (`npm test` 197 pass).
Hai vá kèm: 13-line-annotated mở trục âm (`min: null` khi có giá trị âm, dòng tiền kinh doanh
âm 11 quý bị cắt sạch trước đó) và formatter trục thêm 1 chữ số khi mốc là nghìn tỷ lẻ (trước
đó in hai nhãn "-2 nghìn tỷ" liền nhau cho -1.500 và -2.000); 07-small-multiples nhãn ô lấy
quý cuối từ dữ liệu thay vì chuỗi "(Q4)" cứng. Bốn file preset đang SỬA CHƯA COMMIT.

**Nợ còn lại đo được trên ấn phẩm này:** (a) preset 07 với 3 cột ở khổ 680 làm nhãn ô cuối
tràn mép nếu tên dài, phải rút tên; (b) 11-stacked-100 chỉ có 3 màu, nhóm thứ tư trùng màu
nhóm một, phải gộp về 3 nhóm; (c) chưa có gate nào bắt "chuỗi minh hoạ" lọt vào hình của ấn
phẩm số thật, nên thêm gate quét `minh hoạ|không phải số thật` trong SVG của thư mục
`bao-cao/` là việc rẻ và đáng làm.

## Regression làn pdf-so bắt bằng mắt và vá 11-08: var() trong thuộc tính SVG làm chart ĐEN TRÙM

Ấn phẩm pdf-so ĐẦU TIÊN build sau 09-08 (bản trình TPB `bao-cao/tpb-congbo-chudong/`, gitignore
theo luật bao-cao) cho chart thành khối đen đặc 714x334pt trong PDF trong khi CẢ 10 GATE XANH.
Nguyên nhân: `boc_mau_chu_de` (thêm 09-08 cho làn html-song đổi chủ đề) bọc mọi hex thành
`fill="var(--token, #hex)"`; trình duyệt hiểu var() trong thuộc tính trình bày, WeasyPrint thì
không, giá trị coi là hỏng và fill rơi về mặc định SVG là ĐEN, rect nền 940x440 tô đen trùm hết.
Bản mẫu `examples/mau-phase2` không dính vì PDF của nó build 08-08, TRƯỚC commit đó, và chưa ai
build lại làn pdf-so từ ngày ấy. Vá tối thiểu: `render_pdf.py` thêm `nuong_var_trong_svg()`,
thay var bằng chính fallback CHỈ trong các đoạn `<svg>` của chuỗi HTML đưa cho WeasyPrint; file
`.html` giữ nguyên var() cho đổi chủ đề. Bảng bẫy WeasyPrint trong CLAUDE.md đã thêm dòng này.
`npm test` 197 pass 0 fail sau vá.

**NỢ GATE (việc kế tiếp khi mở repo):** chưa có gate nào nhìn MÀU của nét vẽ trong PDF nên lỗi
này chui qua cả 10 gate; nên thêm phép đo "không có fill đen diện tích lớn bất thường trong vùng
chart" hoặc so màu nét vẽ PDF với bảng màu style, kèm cặp fixture đỏ xanh theo đúng luật gate.
Hai bài học nhỏ cùng phiên: ECharts tự sinh legend từ `series.name` khi không khai `legend`
(lộ mã kỹ thuật `so_du` lên hình giao khách, phải `legend: {show:false}` khi chỉ một chuỗi);
tiêu đề TRONG hình lặp nguyên văn H2 của section là dòng rỗng, tiêu đề hình phải nói thêm ý
khác (áp luật 4.4 cho cả cấp tiêu đề, không riêng chú thích).

## Repo này PUBLIC trên GitHub, và điều đó đổi cách chứa file (09-08)

`gh repo view` trả `visibility: PUBLIC`. Bản ghi cũ trong repo và trong memory toàn cục đều
viết PRIVATE, cả hai đều SAI. Người dùng đã chốt giữ public, nên repo là thư viện mở và mọi
thứ nằm trong git đều là mặt tiền.

Hai thứ đã tách ra ngày 09-08, cả hai đều đã gitignore:

- **`bao-cao/`, ấn phẩm thật của khách.** Bốn commit chưa push mang bộ TPB VN30 gồm bản nội
  bộ, sổ nguồn và dữ liệu thô. Đã chuyển sang `~/tpb-buongmophong/an-pham-vn30-10kb/` và gỡ
  khỏi lịch sử bốn commit đó bằng `filter-branch` TRƯỚC khi push. Luật từ nay: bản giao cho
  một dự án sống trong repo của chính dự án đó. Repo này giữ `examples/` là mẫu chạy được,
  không giữ hàng giao đi.
- **`_harvest/`, 892 file và 57MB.** Gỡ khỏi git, giữ nguyên trên đĩa để còn đối chiếu. Lý do
  không phải dung lượng: mẫu `SHOWCASE_exec_dashboard.png` trong đó vẫn lỗi dấu tiếng Việt,
  nên người mở repo gặp bản HỎNG trước bản đúng. Cộng 203 file font phân phối lại.

Số file trong git rớt từ khoảng 1.194 xuống 302.

**Còn một việc chưa làm và nó đang gây hiểu nhầm thật.** Default branch trên GitHub vẫn là
`master`, đứng sau `feat/digital-only-buoc-1-2` **30 commit** và vẫn mang đủ 892 file
`_harvest/`. Người ngoài mở repo thấy bản trước cú bẻ lái: 108 tài sản, một làn in giấy, chưa
có 9 gate làn song. Một người xem ngoài đã review đúng bản đó và kết luận repo thiếu những thứ
nhánh làm việc đã có (ecdf, calendar heatmap, fan, bump đều đang có trong 111 tài sản).

## Làn `html-song` nay CHẠY THẬT, và bản mẫu đầu tiên đã có (09-08)

Handoff cũ ghi "hạ tầng đã đủ, chưa có trang nào dùng". Câu đó lạc quan. Tầng preset và
tầng gate đã sẵn, nhưng **tầng lắp ráp thì chưa tồn tại**: `build_html.py` có hằng
`CAC_LAN` mà làn A chỉ khác đúng một điểm là cho phép raster, không chỗ nào nhúng ECharts,
không directive đặt chart sống, `orchestrator.py` không có cờ `--lan`. Đợt này dựng nốt.

### Đường sống, bốn mảnh ghép

- `schema.mjs` bỏ `fs.readFileSync`, dùng import attribute JSON. Đây là thứ chặn preset
  15-18 mount sống suốt Phase 4. `schema.vocab.json` vẫn là nguồn duy nhất.
- Cả 18 preset chuyển `renderStatic` sang import ĐỘNG trong nhánh CLI. Import tĩnh kéo
  `render-static.mjs`, mà module đó kéo `echarts` đầy đủ: **đo được, bundle ra 1.197KB,
  tức còn nặng hơn bản đầy đủ**. Trần dung lượng trong `build-bundle-song.mjs` sinh ra
  chính để bắt ca này.
- `echarts-song.mjs`, cửa ECharts riêng, chỉ SVGRenderer. Đổi hướng so với ý ban đầu của
  `mount-live.mjs` là dùng canvas mặc định, lý do: gate THEME-MATCH quét thẻ `<svg>` nên
  chart canvas nằm NGOÀI tầm gate. Bundle 786,8KB, giảm 33%.
- `esbuild` vào devDependencies. Không phải để tiết kiệm 371KB, mà vì một ấn phẩm làn A
  là MỘT file mở bằng `file://` còn 18 preset là 18 module ESM import lẫn nhau.

### Nâng cấp dần, không phải thay thế

Chart sống KHÔNG đứng một mình. Mỗi khối mang SVG tĩnh nhúng sẵn, JS gỡ nó ra sau khi
mount xong. Bắt buộc chứ không phải để đẹp: gate 7 NO-JS-CONTENT đòi mọi chuỗi số hiện
khi JS bật phải hiện cả khi JS tắt, và tỷ lệ text tắt trên bật từ 85%. Chart sống thuần
làm gate đó đỏ chắc chắn.

**Và hai bản phải render bằng CÙNG một engine.** `sinh-svg-preset.mjs` render qua Chromium
chứ không SSR trên Node, vì ECharts chọn số khoảng chia của trục theo BỀ RỘNG CHỮ: cùng dữ
liệu, cùng khung 624x400, bản SSR ra nhãn lớn nhất 5.000.000 còn bản trình duyệt ra
6.000.000. Hai bản của cùng một hình hiện hai con số khác nhau tuỳ JavaScript có chạy hay
không.

### Bốn lỗi THẬT mà bản mẫu đầu tiên lôi ra

Không lỗi nào bắt được bằng test đơn vị, cả bốn chỉ lộ khi dựng một ấn phẩm hoàn chỉnh.

1. **`RE_DIRECTIVE` dùng `(\w+)=` mà `\w` không khớp dấu gạch ngang**, nên `du-lieu=...`
   bị đọc thành khoá `lieu`. Hậu quả đúng kiểu tệ nhất: chart sống im lặng rơi về dữ liệu
   demo của preset trong khi SVG tĩnh cạnh nó dùng dữ liệu thật. Nay `du-lieu` là BẮT BUỘC,
   không có đường lui về `MAC_DINH`.
2. **`14-bar-ranking` đóng cứng `fmtPercent` ở năm chỗ**, nên một lượt xếp hạng tính bằng
   TEU ra nhãn `5.640.000%` trên ấn phẩm thật. Sai sự thật chứ không phải xấu. Đã sửa để
   theo `series.unit`. **Nợ: 04, 05, 08, 15, 18 vẫn đóng cứng y hệt, chưa rà.** Với
   `11-stacked-100` thì đóng cứng là đúng vì nó luôn là tỷ trọng cộng 100%.
3. **`.bia` có margin âm theo `--space-7/6` nhưng breakpoint 700px đổi padding body sang
   `--space-5/4` mà không sửa margin.** Bìa rộng hơn body đúng phần chênh, tràn 12px ở
   360px. Lưu ý cách đọc gate 8: nó báo thủ phạm là thẻ `<g>` trong chart, vì nó liệt kê
   phần tử tràn CUỐI CÙNG chứ không phải phần tử GÂY tràn.
4. **`mountLive` chỉ gắn `data-theme` cho thẻ `<svg>` đầu tiên**, mà ECharts với SVGRenderer
   đặt HAI thẻ `<svg>` cạnh nhau. Gate THEME-MATCH duyệt từng thẻ nên đỏ đúng một nửa số
   chart. Cộng thêm: SVG TĨNH nhúng vào trang chưa từng có ai gắn `data-theme`, nay
   `khai_chu_de_svg()` trong `build_html.py` lo.

### Bản mẫu vận tải biển: 8 PASS, 0 FAIL, 1 SKIP

`examples/van-tai-bien/`, hai chart sống cộng một minh hoạ bake. Chạy bằng:

    python3 pipeline/orchestrator.py examples/van-tai-bien/noi-dung.md --lan=html-song

Gate 3 REDUCED-MOTION là SKIP chứ không phải PASS, và đó là hành vi đúng của nó: trang
không có phần tử nào chạy animation CSS ở chế độ thường (animation của chart là animation
JavaScript trong ECharts), nên gate tự khai là không chứng minh được nó phân biệt được hai
trạng thái. Nó thà SKIP còn hơn xanh giả.

### Ba phán quyết về LUẬT, và vì sao không phải là nới gate cho dễ

Hai gate đỏ ban đầu không phải lỗi của ấn phẩm mà là phép đo sai. Người dùng đã chốt cả ba.

**Token `--ink-lo` hạ độ sáng, #8595A6 sang #66788C.** Giá trị cũ cho 3,07:1 trên nền giấy,
dưới ngưỡng WCAG 4,5:1, mà **41 chỗ** trong `report.css` và `components.css` dùng bậc mực
này làm màu CHỮ. Sửa `.v-nguon` thì `.hinh-nguon` lộ ra ngay, nên bệnh nằm ở token chứ
không ở rule. Bậc `dark` (#7E93A6 trên #0A1420) sẵn 5,83:1 nên giữ nguyên.

**Sửa màu phải sửa ở `design-system/themes/*.json` rồi chạy `node design-system/generate-tokens.mjs`.**
Đã mất một vòng vì sửa thẳng vào `tokens.css`. Nhưng generator KHÔNG lo hết: ba nơi là bản
CHÉP TAY nằm ngoài vùng marker và phải sửa kèm, `tokens.css` khối `:root` đầu, `tokens.py`
dict đầu, và `PALETTE` phẳng trong `charts/echarts/theme.mjs`. Chính `PALETTE` phẳng đó mới
là thứ mọi preset chart đọc, còn `PALETTES` sinh từ JSON là registry theo tên chủ đề.
`chart_theme.test.mjs` ép hai bên khớp nên quên là đỏ.

**Gate 5 chỉ đo chủ đề mà trang KHOÁ.** Trước đó gate lấy mọi chủ đề khai trong CSS rồi tự
bật từng cái lên. Trên một file giao khách, thứ đó vi phạm một luật cứng khác của repo là
khoá `data-theme="light"`: gate đang đo một trạng thái người đọc không bao giờ thấy rồi báo
FAIL vì trạng thái đó xấu. Nay đọc `data-theme` trên thẻ `<html>`; có khai thì đo đúng nó,
không khai thì đo cả danh sách như cũ. `contrast-do.html` đã bỏ `data-theme` khỏi thẻ
`<html>` cho khớp ngữ nghĩa, và có cặp mới `contrast-khoa-xanh.html` giống nó từng ký tự
trừ đúng chỗ khoá, để nhánh mới cũng có bằng chứng đỏ xanh.

**Gate 9 lớp 2 đổi từ đo NỀN sang đo MỰC.** Phép đo cũ so nền SVG với nền trang và đòi từ
3:1, nên một chart nền trắng trên trang nền trắng cho đúng 1:1 và bị FAIL, tức lớp 2 đỏ với
MỌI ấn phẩm đúng chuẩn thiết kế. Ý định của gate là bắt "SVG chìm vào nền", mà thứ nói lên
điều đó là nét vẽ chứ không phải nền. Nay lấy nét vẽ ĐẬM NHẤT trong SVG đối chiếu với nền
của chính nó. Lấy max chứ không lấy min: đường lưới và nhãn phụ vốn cố ý nhạt, đòi mọi nét
từ 3:1 là ép chart phải hết nhạt. Cả hai fixture cũ giữ nguyên và vẫn đỏ đúng lý do, vì
hình 2 của fixture đỏ có chữ #0F1B28 trên nền #0B1522.

Bài học chung, đáng nhớ hơn ba ca này: **một gate chưa từng chạy trên ấn phẩm thật là một
gate chưa được kiểm.** Chín gate làn song đều có cặp fixture đỏ xanh và đều đỏ được, nhưng
hai trong chín đo sai thứ, và fixture không thể lộ ra điều đó vì fixture do chính người
viết gate dựng theo đúng giả định của người viết gate.

## Phổ chart mở lên 23 preset, và hai gate thị giác mới (09-08)

### Năm preset tầng phân phối và tập hợp

`19-raincloud`, `20-ridgeline`, `21-upset`, `22-alluvial`, `23-waffle`. Thư viện lên
**116 tài sản** (23 chart ECharts, 53 component matplotlib, 29 component, 11 minh hoạ).

**Viết MỘT lần ở ECharts, không viết hai lần.** Đây là thứ đổi so với nợ "hai engine phải
đồng bộ tay" ghi trong các bản trước: từ khi `sinh-svg-preset.mjs` render qua Chromium,
một preset ECharts sinh được SVG tĩnh dùng thẳng cho làn `pdf-so`. Nợ đó thu hẹp còn đúng
53 component matplotlib đã có, không lớn thêm theo mỗi chart mới.

Mỗi preset chọn theo CÂU HỎI nó trả lời, không theo độ lạ mắt:

| Preset | Trả lời câu hỏi | Vì sao không dùng cái sẵn có |
|---|---|---|
| `19-raincloud` | phân phối một chỉ tiêu giữa 2-5 nhóm có hình dạng thế nào | boxplot giấu phân phối hai đỉnh: cùng trung vị và cùng quartile vẫn có thể là hai câu chuyện khác hẳn |
| `20-ridgeline` | phân phối DỊCH đi đâu qua 4-12 kỳ | raincloud không có trục thời gian, chồng lấn là tính năng chứ không phải lỗi bố cục |
| `21-upset` | từ 4 tập trở lên chồng lấn nhau ra sao | Venn bốn vòng KHÔNG vẽ được đủ 15 vùng giao, mọi bản Venn bốn tập đều bỏ sót vùng |
| `22-alluvial` | cùng một tập thực thể đổi nhóm ra sao qua các mốc | sankey là dòng chảy BẢO TOÀN qua công đoạn, alluvial là tập thực thể được phân loại LẠI; nhầm hai cái là nhầm bản chất đại lượng |
| `23-waffle` | một cơ cấu, đọc bằng cách ĐẾM ô | biểu đồ tròn bắt mắt ước lượng góc, việc mắt người làm kém nhất |

Ba điều đã đo và đáng nhớ khi viết tiếp preset dạng này:

- **Bandwidth Silverman hệ số 0,9 xoá mất phân phối hai đỉnh.** Nó tối ưu cho phân phối
  một đỉnh; với hai cụm nó nối hai bướu thành một cao nguyên phẳng, tức xoá đúng cái mà
  raincloud sinh ra để cho thấy. Đo trên nhóm demo hai cụm: 0,9 cho một khối gần phẳng,
  0,55 cho hai bướu tách rời.
- **Jitter phải TẤT ĐỊNH.** `Math.random()` làm mỗi lần render ra một ảnh khác nhau, phá
  hẳn visual regression và làm hai bản của cùng một báo cáo hiện hai hình.
- **Tên node của alluvial phải mang tiền tố mốc.** Trùng tên giữa các mốc thì ECharts gộp
  chúng làm một node, đồ thị có chu trình, và bố cục sankey vỡ hoàn toàn.

### Hai gate thị giác, và bốn lỗi chúng lôi ra ngay lần chạy đầu

Bộ gate cũ đọc CẤU TRÚC nên mù với lớp lỗi "hình đúng cấu trúc nhưng nhìn đã khác đi".

- **`scripts/anh-moc.mjs` cộng `anh_moc.test.mjs`**, visual regression cho sáu preset đại
  diện, ảnh mốc 200KB trong `gates/fixtures/anh-moc/`. So pixel bằng canvas TRONG trình
  duyệt nên không thêm thư viện giải mã PNG nào. Ngưỡng 0,05% đến từ mutation chứ không
  từ cảm giác: 0,3% ban đầu để lọt một mutation đổi nhãn `120` thành `120,00` (0,242%).
  Chụp cùng một preset hai lần cho đúng 0 pixel khác, và test khẳng định điều đó bằng số.
- **`nhan_khong_chong.test.mjs`** đo TUYỆT ĐỐI, không cần mốc: hai hộp chữ giao quá 40%
  diện tích hình nhỏ hơn là chồng.

Bốn lỗi thật, đều có sẵn trong thư viện và đều đi qua mọi gate cũ: `04-dumbbell` hai nhãn
cùng `position: top` ra `12,54,1%`; `03-bullet` grid.bottom 30px không đủ cho cả nhãn trục
lẫn chú giải ra `30ải tốt`; `06-tornado` nhãn giá trị gặp nhãn trục; `05-slope` nhãn hai
đầu chồng nhau, nay tự vẽ bằng graphic trong `_veSauLayout` và tách theo trục dọc.

Với `05-slope` đã cân và LOẠI hai đường sẵn có của ECharts: `hideOverlap` chạy thật nhưng
nó ẨN nhãn, tức xoá tên một ngân hàng khỏi biểu đồ so thị phần; `moveOverlap: 'shiftY'`
đúng ý định nhưng đo thật thì không dịch đủ, vẫn còn giao 40%.

## 23/23 preset qua schema, và một gate rỗng tinh vi bị lộ (09-08)

CLAUDE.md viết "mọi chart phải đi qua lớp schema dùng chung" từ Phase 1. Đếm thật thì chỉ
**6 trên 18** preset gọi `validateSeries`. Một luật không ai kiểm thì không phải luật, nó
là một câu văn, và câu văn đó đã sai suốt hai phase.

### Vì sao đây là nợ thật chứ không phải chuyện hình thức

Preset không đi qua schema thì không có `series.unit`, tức **không có cách nào biết đơn vị
của chính đại lượng nó vẽ**, nên nó đoán. Đó là gốc của lỗi `5.640.000%`. Sửa từng preset
như đợt trước là chữa triệu chứng.

### Ba hình dạng khai meta, cả ba đều có lý do

`validateSeries` hoá ra **không bắt buộc `rows`** (`series.rows || []`), nên nó áp được cho
mọi preset chỉ với `unit` và `source`. Không phải tách schema thành hai tầng như phương án
đầu tiên đã cân.

| Khai ở | Preset | Vì sao |
|---|---|---|
| `MAC_DINH.series` | 19 preset | mặc định |
| `MAC_DINH.meta` | 15, 16, 18 | chúng dùng `series` làm biến cục bộ để dựng `rows`; trùng tên thì module chết bằng SyntaxError, đã cắn thật ở 05 và 07 |
| từng hàng | 03-bullet | N chỉ tiêu độc lập, ba cái tỷ đồng và một cái lần. Ép cả bốn vào một `series.unit` là nói dối, vì chính `validateSeries` đã chốt "không trộn đơn vị trong một series" |

### `epDonVi`: cho preset nói thật về giới hạn của nó

Nhiều preset đóng cứng đơn vị trong hàm định dạng (`fmtCompact(v, { baseUnit: 'ty' })`).
Sau khi bắt mọi preset khai `unit`, có ba đường:

- Khai `unit` rồi phớt lờ khi định dạng: **khai báo nói dối**, và nó im lặng. Đổi `unit`
  sang `teu` thì nhãn vẫn ra "tỷ".
- Viết lại mọi preset cho nhận được mọi đơn vị: đúng nguyên tắc nhưng đổi diện mạo của
  những preset vốn sinh ra cho một đại lượng duy nhất.
- **Đường đã chọn:** preset nói thẳng nó làm được gì, `epDonVi(series, ['ty_dong'])`, và
  ném lỗi lúc build thay vì vẽ ra một nhãn sai sự thật.

### Gate rỗng tinh vi: validate chính hằng số mình bịa ra

`15-quadrant-scatter`, `16-dot-distribution`, `18-sensitivity-grid` **có** gọi
`validateSeries` từ trước, nhưng đối tượng chúng validate là một object `unit`/`source`
viết cứng ngay trong `option()`. Phép validate chạy thật, nhưng nó kiểm một hằng số do
chính preset bịa ra, nên **không bao giờ đỏ với dữ liệu người dùng truyền vào**: một báo
cáo thật có thể đưa vào bộ số không nguồn mà preset vẫn xanh.

Đây là biến thể nguy hiểm nhất của gate rỗng đã gặp: nó có một lời gọi validate thật, nên
đọc mã nguồn thấy đủ. Chỉ phép đo hành vi (bỏ `source` khỏi `MAC_DINH`, đòi `option()` phải
ném lỗi) mới lộ ra.

### Và chính test mới cũng dính một lỗ hổng cùng loại

Phép đo "preset đóng cứng đơn vị phải gọi `epDonVi`" bản đầu **bỏ qua preset nào không chứa
chuỗi `epDonVi` trong mã nguồn**, với lý lẽ "preset đó nhận đơn vị tự do". Tức test tự miễn
trừ đúng cái nó cần kiểm: gỡ `epDonVi` khỏi một preset là nó ngưng kiểm preset đó. Mutation
xác nhận, và bản sau không đọc mã nguồn nữa mà so DẤU VÂN TAY định dạng: đổi `unit` rồi hỏi
cách hiện số có đổi theo không. Dấu vân tay phải với cả nhãn vẽ bằng `graphic` trong
`_veSauLayout`, nếu không `05-slope` bị kết luận nhầm là nói dối.

### Nghiệm thu

Diện mạo **không đổi một pixel** trên cả sáu ảnh mốc, đúng mục tiêu của một đợt refactor.
Gate ảnh mốc dựng hôm trước chứng minh giá trị ngay ở lần dùng đầu tiên. `npm test` 175
pass, pytest 43 pass, ấn phẩm làn song vẫn 8 PASS.

Cộng hai việc nhỏ đóng cùng đợt: thêm `so_luong` vào từ vựng (upset và alluvial đếm số phần
tử, vocab chưa có đơn vị đếm), và **vạch base-case của `06-tornado` nay vẽ THẬT**. Vạch đó
từng được viết bằng `getOption()` rồi `setOption()` lại, cách đó không làm `markLine` hiện
ra trong SVG, nên một tính năng nhìn như có trong mã nhưng chưa bao giờ vẽ ra suốt hai
phase. Khai `markLine` thẳng trong option thì nó hiện.

## SKILL.md nay là DOCTRINE tự đủ, không còn là bảng chỉ đường (09-08)

Người dùng đối chiếu repo với skill `design-taste-frontend` và hỏi thiếu gì. Chẩn đoán:
`design-taste-frontend` là **doctrine tự đủ** dạy CÁCH QUYẾT ĐỊNH, một file chạy được trên
máy trắng. `SKILL.md` cũ là **bảng chỉ đường tới repo**, 4,3KB, và nó tự thú ngay dòng 12
rằng tầng doctrine "sẽ tới ở Phase 3". Phase 3 đã qua từ lâu.

### Phát hiện quan trọng nhất: doctrine ĐÃ CÓ, chỉ chưa được chưng cất

`research/` có 14 thư mục, khoảng 350KB, và trong đó đã nằm sẵn những thứ tưởng là thiếu:
`03-chart-doctrine/CHART-SELECTION.md` chính là cây quyết định chọn hình theo tám nhóm câu
hỏi; `04-wow-layer/ANTI-SLOP.md` chính là danh sách dấu hiệu máy làm, có cả cột "phân biệt
trong ba giây". Chúng chưa bao giờ được `SKILL.md` trỏ tới.

Nhưng research là **ảnh chụp một thời điểm**: bảng tra chọn hình đến nay vẫn ghi "chưa có"
cho boxplot và fan chart, cả hai đã có từ lâu. Đó là lý do doctrine mới KHÔNG chép danh sách
tài sản: phần bền là ánh xạ câu hỏi sang họ hình, phần biến động tra ở `catalog/CATALOG.md`
vốn sinh tự động từ mã nguồn.

### Đã dựng

`SKILL.md` 19,4KB tự đủ, cấu trúc: đọc đề bài và tuyên bố một dòng, ba núm, chọn làn, kiến
trúc ấn phẩm, chín chỉ thị sửa thiên lệch, chọn hình theo câu hỏi, kỷ luật bằng chứng, ràng
buộc cứng, dấu hiệu máy viết, kiểm trước khi giao.

**Ba núm, suy từ research chứ không đoán:** `DO_SAU`, `MAT_DO_SO`, `MUC_CAM_KET`, mỗi núm
1-10, kèm bảng preset cho bảy loại ấn phẩm. Ràng buộc nối chúng với bằng chứng: **mức cam kết
không được vượt bậc nguồn**, số ước tính nội bộ thì trần của `MUC_CAM_KET` là 6.

`doctrine/` bốn file thật: kể chuyện, chọn hình, viết chữ, anti-slop. Hai file đầu và file
viết chữ là mảnh CHƯA TỪNG CÓ; anti-slop là bản cập nhật cho hai làn. Ba bảng tra khác vẫn
sống ở `research/` và README nói rõ vì sao: chúng đã ở dạng thi hành được, chép sang chỉ tạo
thêm một bản để trôi.

### Luật "SKILL.md phải dưới 12KB" đã BỎ, ghi lại vì sao

Test cũ chặn SKILL.md quá 12KB với lý lẽ "mỗi lần gọi là nuốt hết", và nêu đích danh
`design-taste-frontend` làm phản ví dụ. Lý lẽ đó **đo chi phí sai**: nó chỉ đếm phần nạp tự
động mà bỏ qua phần phải đọc thêm. Bản 4,3KB cũ không tự đủ, agent phải mở tiếp `CLAUDE.md`
26KB và catalog 37KB, tổng thật vượt 60KB. Bản tự đủ 19,4KB rẻ hơn hẳn.

Người dùng chốt bỏ hẳn thay vì nới ngưỡng: độ dài là việc của người viết. Điều kiện đáng đặt
lại một ngưỡng, ghi trong chính file test: khi SKILL.md bắt đầu mang phần TRA CỨU thay vì
phần QUYẾT ĐỊNH. Lúc đó vấn đề không phải độ dài mà là sai tầng.

### Gate mới: `skill_khong_lac_hau.test.mjs`

`SKILL.md` từng nói sai về chính repo suốt hai phase (108 tài sản khi thực tế 116, "mười
gate" khi đã có thêm chín, hẹn một phase đã qua) và không phép đo nào bắt được vì tài liệu
không chạy. Ba phép đo mới: mọi đường dẫn phải tồn tại, số tài sản phải khớp catalog, không
còn lời hẹn về phase. Cả ba đã mutation. Những khẳng định KHÔNG kiểm được thì test nói thẳng
là không kiểm, không giả vờ.

## Chủ đề tối CHẠY THẬT, và tầng doctrine đóng trọn (09-08, đợt 3)

Hai món cuối trong sổ nợ đã đóng. Không còn mục nào trong danh sách "còn thiếu".

### Chủ đề tối: hạ tầng đã sẵn hơn tưởng, chỉ thiếu nối dây

Khảo sát trước khi làm cho thấy ba phần tư đường đã xong từ các đợt trước mà không ai biết:
minh hoạ SVG chỉ còn **1 hex hardcode** trên 39 (38 cái kia là fallback trong `var()`);
`hex-token.mjs` đã có sẵn cơ chế bọc hex thành `var(--token, #hex-cũ)`; `generate-tokens.mjs`
đã sinh `PALETTES` theo tên chủ đề nhưng **chưa ai dùng**. Đợt migrate 300 hex sang `var()`
ngày 07-08 chính là để chuẩn bị cho việc này.

Thêm `design-system/themes/toi-lanh.json`, chạy generator, và bốn đường đổi màu hoạt động:
CSS dùng thẳng `var()`, minh hoạ đã `var()`, chart tĩnh bọc chuỗi, chart sống đọc
`getComputedStyle`.

### Bốn chỗ đã cắn khi nối, cả bốn đều im lặng

1. **`sinh-svg-preset.mjs` đi vòng qua `renderStatic`** nên không được bọc màu. Đây là hồi quy
   do chính đợt đổi sang render bằng Chromium tạo ra, và nó im lặng vì hình vẫn đúng màu ở chủ
   đề sáng.
2. **Chart matplotlib chưa có đường bọc nào.** Phải viết bản Python của `bocMauChuDe`. Đo được:
   7 trên 8 giá trị hex khác nhau trong một SVG matplotlib thuộc đúng bảng màu, nên bọc được;
   cái thứ tám là `#BBBBBB` viết cứng trong `_eir_style.py`, nằm ngoài hệ token.
3. **`_veSauLayout` chạy SAU khi thay màu**, nên bốn nhãn của một chart giữ màu chủ đề sáng
   trong khi cả phần còn lại đã đổi.
4. **Nhóm token "trên nền mực" không tồn tại phía CSS.** `.bia-dek` và `.bia-meta` viết cứng ba
   mã màu sáng, nên ở chủ đề tối chúng thành chữ nhạt trên nền sáng. Phía Python đã có hằng
   `ON_INK` từ lâu; kiểu lệch này chỉ lộ khi thêm chủ đề thứ hai. Nay có
   `--on-ink`, `--on-ink-md`, `--on-ink-lo`, `--on-ink-line`.

### Giới hạn đã biết, ghi rõ

Chart sống đọc màu đúng MỘT LẦN lúc mount. Chủ đề khai sẵn trong HTML thì đúng; nếu sau này
làm nút đổi chủ đề động thì phải mount lại chart. Chưa có cơ chế đó.

### Dải chín bậc của minh hoạ ĐẢO NGƯỢC, không ánh xạ một đối một

Ràng buộc cũ vẫn đúng: một mã màu trong minh hoạ đóng nhiều vai cùng lúc. Thứ giữ được qua hai
chủ đề là THỨ TỰ BẬC, không phải giá trị. Bậc 1 ở chủ đề sáng là tối nhất, ở chủ đề tối là
sáng nhất.

### Tầng doctrine nay đủ sáu file

`01-ke-chuyen`, `02-chon-hinh`, `03-viet-chu`, `04-bang-so`, `05-anti-slop`, `06-chu-de-toi`.
Ba bảng tra khác vẫn sống ở `research/` và README nói rõ vì sao.

## ĐỌC MỤC NÀY TRƯỚC: tiền đề của repo đã đổi (07-08)

Repo được xây trên tiền đề **"PDF IN ĐƯỢC"**. Người dùng đã phán quyết tiền đề đó sai với thực
tế: không ai in bản giấy nữa. Giữ nó là tự bóp chính mình, vì nó loại oan trọn hai trường phái
mạnh nhất của nghiên cứu (narrative formats và motion idioms) chỉ vì WeasyPrint không chạy
JavaScript.

**Đích mới: DIGITAL ONLY, hai làn, người dùng chọn theo từng ấn phẩm.**

| Làn | Là gì | Được phép | Còn ràng buộc |
|---|---|---|---|
| `html-song` | HTML tự đủ mở bằng trình duyệt | animation, tương tác, scrollytelling, tooltip, hover, JavaScript lúc chạy, canvas, WebGL, blur, dark mode, responsive | một file tự đủ, chạy offline, không CDN ngoài, font nhúng |
| `pdf-so` | PDF đọc trên MÀN HÌNH, không phải để in | khổ ngang, màu RGB, siêu liên kết, bookmark, hết lo lề nhà in | tĩnh hoàn toàn, chữ chọn được trong tầng text |

**Engine PDF: người dùng đã chốt GIỮ WeasyPrint**, không đổi Chromium. Nên `bake_svg.mjs`,
gate 6, bảng ba thuộc tính WeasyPrint bỏ qua, và lệnh cấm `color-mix()` đều GIỮ NGUYÊN cho làn
`pdf-so`. Siêu liên kết và bookmark vẫn làm được qua `bookmark-level` mà WeasyPrint hỗ trợ sẵn.

**Bảng màu ĐÃ MỞ**: trắng lạnh nay là MẶC ĐỊNH, không còn là hằng số. Ràng buộc con giữ nguyên
độ cứng: một báo cáo chỉ MỘT bảng màu, báo cáo chọn TÊN bảng chứ không chọn hex, và mọi bảng
mới phải qua gate tương phản. Gate đó CHƯA CÓ, là việc mới đẻ ra từ quyết định này.

**Bốn luật KHÔNG được nới theo**, vì chúng không sinh ra từ in ấn: cấm gauge và radar (lý do
đúng sai phân tích) · cấm em-dash, en-dash, AI-slop, câu kết cách ngôn (văn phong) · font phải
nhúng (máy khách không có font) · mọi số phải có nguồn.

### Đã làm được gì cho cú bẻ lái (commit `e9a1336`)

Bước 1 và 2 XONG. Cả hai đều là GỠ ràng buộc, không thêm tính năng, nên mọi lời gọi cũ giữ
nguyên hành vi.

- `nap_svg()` nhận `cho_phep_raster`, `lap_trang()` nhận `chu_de`, `dung()` nhận `lan` và
  `chu_de`, CLI có `--lan` và `--chu-de`. Mặc định `pdf-so` và `light`.
- `catalog_drift.test.mjs` đổi từ `assert.equal(29)` sang SÀN, nên thêm component không còn làm
  `npm test` đỏ ở bước đếm.
- Luật `rgba(R G B / A)` GỠ HẲN. Luật `blur=0` giữ nhưng lý do đã đính chính.

### Đã làm XONG bước 3 và bước 5, cộng ba tài sản mới

**Bước 3 XONG**: `design-system/themes/sang-lanh.json` là nguồn sự thật duy nhất, cộng
`design-system/generate-tokens.mjs` sinh ra cả `tokens.css`, `tokens.py` và `theme.mjs` qua marker
`THEME-TOKENS:BAT-DAU/KET-THUC`, cộng `tests/consistency/theme_tokens_drift.test.mjs`. Quan trọng
nhất: **hai test tự hardcode kỳ vọng nay đọc từ JSON** (`tokens_test.py`, `chart_theme.test.mjs`),
tức đã xoá đúng cái lỗ "thứ canh gác là bản sao của thứ bị canh". Chưa thêm chủ đề tối, mới dựng
CƠ CHẾ. Bốn token `--ilus-toi/-vua/-sang/-panel` đã khai sẵn cho bước 4.

**Bước 5 XONG, và con số thật là 22 chứ không phải 29.** Ước lượng 29 đến từ một phép grep thô
đếm cả comment, docstring, khai hằng số và `facecolor=`/`fc=`/`edgecolor=`/`markerfacecolor=`.
Đọc từng ngữ cảnh thì đúng 22 chỗ là chữ hoặc glyph đặt trên khối màu đậm. `ON_INK` bằng đúng
`PAPER` hôm nay nên **31 trên 31 ảnh sinh ra khớp SHA256 tuyệt đối**, không đổi một pixel.
`viz_eir_kpi.py` không có chỗ nào thuộc nhóm này. Hai chỗ trong `viz_eir_diagram.py` là
`marker="*"` và ký hiệu `+`/`-`, không phải text thật nhưng đóng đúng vai glyph tương phản trên
node NAVY, nên xếp vào `ON_INK`; không xếp thì chúng biến mất trên nền tối y hệt chữ.

**Ba tài sản MỚI đầu tiên sau cú bẻ lái**, trong file riêng `charts/matplotlib/viz_eir_risk.py`:
`c_drawdown`, `c_calendar_heatmap`, `c_ecdf`. Kho lên **111 tài sản** (53 matplotlib). Cả ba là
vector thuần, 0 raster, đã nghiệm thu bằng cách render PDF thật rồi đếm bằng `doc.xref_object`.

**Bước 4 XONG, PHASE 3 ĐÓNG.** Đã di trú **300 vị trí** trên 11 SVG cộng `annotate.css` sang
`var(--ilus-N, #hex-cũ)`. Tầng minh hoạ lần đầu tiên đi qua cửa `design-system/tokens`.

Dải kết cấu mở từ 4 lên **9 bậc**. Khối `ilus` ban đầu trích từ `illustrations/grammar.md` mục 4
khai bốn bậc, nhưng đếm thật trên 11 file thì chúng dùng CHÍN bậc: **grammar.md và tài sản đã
trôi khỏi nhau từ trước**. Đánh số theo VỊ TRÍ (`--ilus-1` đậm nhất tới `--ilus-9` nhạt nhất) vì
chín bậc thì không còn tên nào gọi cho đúng mà không phải bịa.

Ánh xạ **một đối một, không gộp bậc**. Gộp chín về bốn sẽ đổi diện mạo 11 minh hoạ đang dùng
được, và đó là quyết định thiết kế chứ không phải việc dọn dẹp. **49 mã ngữ nghĩa giữ nguyên
hex**: chúng là accent ngành, thuộc trục khác với trục chủ đề.

Mọi `var()` có giá trị dự phòng bằng đúng hex cũ, vì các file `.svg` còn được mở ĐỘC LẬP ngoài
trang HTML. Thiếu dự phòng là hình mất sạch màu, và chỉ lộ ra ở đường mở độc lập.

### ECharts: một nguồn preset cho hai làn, XONG

`option(params)` tách hẳn khỏi render. Ba đường dùng chung một nguồn:
`render-static.mjs` (SSR, nơi DUY NHẤT ép `animation:false`, cộng hậu xử lý hex sang `var()`) ·
`mount-live.mjs` (mount trong DOM thật, GIỮ animation mặc định) · `registry.mjs` (18 mục).
`baseOption()` không còn tự khai `animation:false`, vì đó là luật của ĐƯỜNG SSR chứ không phải
của dữ liệu chart.

**Bẫy hex nướng vào SVG tĩnh đã chốt cách xử lý**: hậu xử lý trong `renderStatic()` đổi mọi hex
THUỘC BẢNG MÀU sang `var(--token, #hex-cũ)`. An toàn vì tập hex là TẬP ĐÓNG sinh từ `PALETTE`,
biết chính xác phải tìm gì. `hex-token.mjs` giữ bảng và hàm `demHexThoConLai()`, có gate riêng đã
kiểm đỏ được.

Nghiệm thu: 19 output (18 preset cộng biến thể `-dot`) khớp số nét vẽ TUYỆT ĐỐI với bản trước
refactor. Cộng bằng chứng điều kiện ĐỦ: nhúng SVG đã hậu xử lý vào trang có token giả, accent đo
được đổi từ `rgb(34, 81, 255)` sang `rgb(255, 106, 0)`, và ảnh chụp xác nhận TOÀN BỘ chart đổi
theo chứ không riêng một điểm.

### Bộ gate làn `html-song`, chín gate, XONG

`gates/gates_song.mjs` (file riêng, `gates/gates.mjs` giữ nguyên cho làn `pdf-so`), chín cặp
fixture trong `gates/fixtures/song/`, test ép đỏ xanh ở `tests/consistency/gate_do_xanh_song.test.mjs`.
`gates/run.mjs` thêm nhánh `--lan=html-song` nhận một mình file HTML; nhánh mặc định giữ nguyên
hành vi cũ. KHÔNG gate nào bị loại.

`THEME-MATCH` có hai lớp, và chúng bắt HAI BỆNH KHÁC NHAU chứ không dự phòng cho nhau: bệnh kinh
điển "chart trắng trên nền tối" cho tương phản RẤT CAO (18,5:1) nên lớp đo thực nghiệm không bắt
được, chỉ lớp khai báo bắt; lớp thực nghiệm bắt bệnh ngược lại là SVG chìm vào nền.

### Ba phát hiện phụ của đợt này

**`06-tornado.mjs` có một tính năng CHƯA BAO GIỜ vẽ ra.** Vạch base-case qua `chart.getOption()`
cộng gán lại cộng `setOption()` lần hai không hề hiện trên chart: đếm chuỗi "Base" trong SVG gốc
chỉ ra 1 lần, và đó là từ phụ đề. Đã GIỮ nguyên hành vi để đảm bảo không đổi diện mạo, ghi chú
trong mã, chưa sửa vì ngoài phạm vi.

**Cả 18 preset cộng `fmt.mjs` đọc `process.argv[1]` và import `node:fs` TĨNH ở đỉnh file**, nên
ném lỗi ngay khi bị import trong trình duyệt. Nghĩa là `mount-live.mjs` sẽ vô dụng cho toàn bộ
nếu không sửa. Đã vá bằng import động cộng `typeof process !== 'undefined'`, kiểm bằng mount thật
qua Chromium và xác nhận `chart.getOption().animation === 'auto'`, tức đường sống KHÔNG bị ép tắt.

**Giới hạn còn lại, đã khai không giấu**: preset 15, 16, 17, 18 vẫn CHƯA mount sống được, vì
`schema.mjs` dùng chung có `fs.readFileSync('schema.vocab.json')` không điều kiện ở đỉnh file.
Sửa nó cần thiết kế riêng vì file đó dùng chung với `schema.py`.

### Việc tiếp theo

- Gỡ nốt `schema.mjs` khỏi `fs` để 4 preset còn lại mount sống được.
- Sửa `06-tornado.mjs`: hoặc làm vạch base-case vẽ thật, hoặc bỏ hẳn mã chết.
- Dựng một ẤN PHẨM làn `html-song` thật đầu tiên. Hạ tầng đã đủ, chưa có trang nào dùng.
- Định nghĩa giá trị cho một chủ đề TỐI. Lúc đó mới đụng giới hạn đã biết: một mã hex trong minh
  hoạ có thể đóng NHIỀU vai (vừa là nền trời vừa là thân kim loại), và ánh xạ một đối một không
  tách hai vai đó ra được. Phải tách ở TỪNG HÌNH chứ không tách ở token.
- `_eir_style.py: draw_masthead()` chưa tự xuống dòng, phụ đề quá ~110 ký tự vẫn tràn lề phải.
- **Dấu âm trong chart matplotlib chưa ai chốt, và một chart đang dùng hai kiểu.** Đo được trên
  `catalog/xem-truoc/diverging_bar.svg`: tick trục ra `−2`, `−1` bằng U+2212, còn nhãn giá trị
  trong cùng hình đó ra `-2.0`, `-1.1` bằng dấu gạch nối ASCII. Nguyên nhân là `axes.unicode_minus`
  của matplotlib mặc định bật và repo chưa đặt lại ở đâu cả. Phải chọn một kiểu rồi ép bằng test.
  Kèm theo là một lỗ hổng đặc tả: `FINANCIAL_SYMBOLS` trong `build-fonts.py` liệt kê 13 codepoint
  và `KY_HIEU_TAI_CHINH_PHO_QUAT` trong `fonts_test.py` liệt kê 6, **không danh sách nào có
  0x2212**. Font subset hiện CÓ glyph đó, nhưng có nhờ dải `latin` của Google chứ không do ai
  yêu cầu, nên một lần đổi nguồn font là rớt mà không gate nào bắt. Thêm 0x2212 vào cả hai danh
  sách bất kể chọn kiểu dấu âm nào.
- SVG trong `catalog/xem-truoc/` chỉ khai `font-family` chứ không nhúng font. Trên máy không có
  IBM Plex, chúng rơi về font hệ thống và trông xấu hoặc ra ô vuông. Đó là ảnh xem trước nên
  chấp nhận được, nhưng phải biết trước khi ai đó báo "chart lỗi dấu" từ ảnh xem trước.

### Bẫy XML: `var()` bọc vào một hex nằm trong COMMENT làm hỏng CẢ FILE

Phép thay thế bằng regex đã bọc một mã hex nằm trong khối `<!-- -->` của
`geography-vietnam-map.svg`. Cú pháp custom property bắt đầu bằng hai dấu gạch ngang, mà **XML
cấm chuỗi con đó bên trong comment**, nên một dòng chú thích thuần tài liệu, không ảnh hưởng
render, biến thành lỗi làm hỏng cả file. Hỏng theo đúng kiểu nguy hiểm nhất của repo: WeasyPrint
bỏ qua CẢ FILE không báo lỗi, PDF ra 0 nét vẽ.

Bắt được vì quy trình bắt buộc chạy `kiemTraXml()` sau mỗi lần sửa. Nhìn mắt không thấy gì. Đã
trả lại hex thô tại đúng vị trí đó, và đó là ngoại lệ DUY NHẤT trong 11 file.

### Nghiệm thu di trú: điều kiện CẦN không phải điều kiện ĐỦ

Ba agent đều chứng minh ảnh KHÔNG ĐỔI khi mở độc lập, SHA256 khớp tuyệt đối 11/11. Đúng, nhưng
chưa đủ: **nếu bọc nhầm TÊN BIẾN thì ảnh độc lập vẫn y hệt**, vì dự phòng vẫn là hex cũ, và không
phép đo nào của họ bắt được.

Phép đo điều kiện ĐỦ: nhúng từng hình vào một trang CÓ khai `--ilus-*`, đảo ngược cả chín bậc
sang một dải màu khác hẳn, rồi xác nhận hình ĐỔI THEO. Kết quả 11/11. Cộng soi mắt một hình xác
nhận tách trục đúng: thân tàu, cabin, ống khói, vạch mớn nước theo dải mới, còn container và mặt
nước giữ nguyên vì chúng là màu ngữ nghĩa.

Bài học chung: khi một phép di trú có **giá trị dự phòng bằng đúng giá trị cũ**, mọi phép đo
"không có gì đổi" đều xanh kể cả khi việc di trú sai hoàn toàn. Phải có một phép đo ép hệ thống
THỂ HIỆN cái năng lực mới.

### Hai hệ màu song song, nợ có từ TRƯỚC cú bẻ lái, ĐÃ TRẢ 07-08

11 minh hoạ SVG dùng **345 hex viết cứng, và không một mã nào là `#051C2C` hay `#2251FF`**.
Chúng là bảng Tailwind (`#0f172a`, `#e2e8f0`, `#64748b`, `#2563eb`, `#f59e0b`, `#0d9488`). Tầng
minh hoạ **chưa bao giờ đi qua cửa `tokens`**, trong khi nhóm matplotlib đã bị ép đi qua bằng cả
một khối lập luận ở `_eir_style.py:29-52`. Chỉ `--accent` là di động, xuất hiện đúng 2 lần trong
89 dòng của `logistics-container-ship.svg`.

Chuyển 345 hex sang `var()` trả cả hai nợ một lượt. Sơn tay sang bảng tối thì trả một nợ và đẻ
thêm một nợ (22 file thay vì 11).

### Bẫy kiến trúc ECharts phải chốt TRƯỚC khi động vào `theme.mjs`

ECharts SSR ghi hex **thẳng** vào SVG tĩnh, không `var()` nào chạy lúc người đọc xem (kiểm được
trên `out-01-waterfall.svg`: 0 lần `var(--`, cả 8 mã hex đã bake thành chữ literal). Nên "chart
theo chủ đề người đọc chọn" KHÔNG làm được bằng CSS. Hai đường, chưa chọn: sinh N bản SVG mỗi
chart (chi phí nhân theo số chủ đề), hoặc hậu xử lý đổi hex thành `var()` (một bản duy nhất,
nhưng sót một hex là ra vệt màu lạc rất khó bắt bằng mắt, phải có gate đếm hex còn sót).

### Ba gate rỗng MỚI phát hiện, cộng vào ba cái của Phase 1

4. `gates/gates.mjs:261-264` gate 5 CHART-SONG: SVG không có chuỗi chữ dài từ 4 ký tự thì
   `continue` mà KHÔNG đổi `trang_thai`. Hình đó vẫn PASS, chỉ còn được che bởi phép kiểm yếu
   nhất là XML parse được.
5. Gate `khoa-sang-khong-doi-theo-may-khach` chỉ đọc `getComputedStyle(document.body)`, tức
   KHÔNG nhìn thấy chart hay minh hoạ, nên không có khả năng phát hiện đúng bệnh mà luật khoá
   sáng sinh ra để tránh.
6. `--shadow-*` blur bằng 0 canh một thứ WeasyPrint chưa bao giờ vẽ. Xem mục dưới.

### Một luật cấp hệ thống đã vô nghĩa suốt hai phase

`docs/specs/...design.md:79` chốt "shadow offset cứng là ngôn ngữ độ nổi DUY NHẤT của toàn hệ",
dựa trên phép đo chạy trên **Chromium in**. Nhưng engine chốt là **WeasyPrint**, và WeasyPrint
**không vẽ box-shadow bằng bất kỳ cú pháp nào**. Luật đó chưa bao giờ bảo vệ bản giao đi; nó chỉ
bó tay bản trình duyệt. Nó còn đẻ ra luật con `rgba(R G B / A)` tồn tại CHỈ để một dòng
`split(",")` trong test chạy đúng.

**Bài học cấp doctrine**: repo có gate ép mọi gate phải tự đỏ được, nhưng KHÔNG có gate nào hỏi
**"luật này còn lý do không"**. Mỗi luật cứng từ nay phải ghi LÝ DO và ĐIỀU KIỆN HẾT HIỆU LỰC
ngay cạnh nó.

### Ba khe hở tìm được khi dựng ba component mới

**`_eir_style.py: draw_masthead()` không tự xuống dòng.** Phụ đề dài quá khoảng 110 tới 120 ký
tự thì TRÀN QUA LỀ PHẢI. Đây là bệnh CÓ SẴN, tái hiện được trên component cũ `seasonality` chứ
không phải do component mới gây ra. Chưa sửa vì nằm ngoài phạm vi đợt đó. Trong lúc chưa sửa thì
giữ phụ đề dưới 95 ký tự.

**`viz_super.py: _MODULES` là danh sách viết cứng.** Thêm một module mới mà quên khai vào đó thì
component của nó biến mất khỏi `--list`, khỏi `scripts/sinh_xem_truoc.py`, và khỏi contact sheet,
TRONG KHI `sinh_catalog.py` vẫn liệt kê nó vì script đó quét FILE chứ không quét registry. Kết
quả là một component có mặt trong mục lục nhưng không có bản xem trước, và không lỗi nào báo
ngoài một dòng "bo qua" trên stderr. Đã vấp thật khi nạp `viz_eir_risk.py`. Docstring của
`viz_super.py` cũng đã trôi từ trước: ghi 48 component và liệt kê 5 module trong khi mã đã có 6.
Nay docstring không còn viết tay con số nào, chỉ trỏ tới `--list`.

**Bẫy soi ảnh NGƯỢC với bẫy đã ghi trong `CLAUDE.md`.** Luật cũ cảnh báo "soi ảnh toàn cảnh bị
thu nhỏ làm chi tiết nhỏ biến mất". Ca `c_calendar_heatmap` là chiều ngược lại: soi crop thì mọi
chi tiết đúng hết (ô outlier đúng màu, viền vàng đúng chỗ, nhãn tháng không đè nhau) nhưng BỐ CỤC
TỔNG THỂ sai, lưới chỉ chiếm một dải mỏng giữa khung và nhãn `CN` gán cho một hàng không tồn tại.
Phải soi CẢ HAI, và soi toàn cảnh TRƯỚC.

Một chi tiết kỹ thuật đáng nhớ từ ca đó: `set_aspect("equal")` cộng một `rect` cao cố định thì
matplotlib CO khung lại cho đúng tỷ lệ rồi CĂN GIỮA phần còn lại, nên phần thừa biến thành khoảng
trắng chết. Muốn khung lấp đầy thì phải tính chiều cao khung TỪ chiều rộng và số hàng, và tính
bằng INCH TUYỆT ĐỐI chứ không bằng tỷ lệ, vì masthead và chân trang cần chiều cao cố định; nén
theo tỷ lệ thì chúng co theo và đè lên nhau.

### Nợ nhỏ: SVG sinh ra không tái lập được

`hinh/ra-*.svg` được commit nhưng matplotlib nhúng `<dc:date>` và một `clip-path` id ngẫu nhiên,
nên mỗi lần chạy `npm run mau` là cây git bẩn thêm một file dù không có gì đổi thật. Chữa bằng
`svg.hashsalt` và tắt metadata.

## Đang ở đâu

**Phase 2 ĐÓNG.** Đường ống từ markdown ra PDF đã qua gate chạy được bằng một lệnh, và
mười gate đều đã chứng minh là đỏ được với fixture đỏ của chính chúng.

Nghiệm thu gần nhất, chạy thật chứ không chép lại:

| Lệnh | Kết quả |
|---|---|
| `npm test` | 109 pass, 0 fail |
| `npm run verify` | exit 0, mọi gate PASS và 2 SKIP có ghi rõ lý do |
| `python3 -m pytest tests/ -q` | 48 passed |
| `npm run mau` | 6 trang, 169 nét vẽ, 0 ảnh raster, 10 gate PASS ở bản nội bộ và 9 PASS 1 SKIP ở bản gửi đi |

Phase 1 đóng trước đó: 8 task review sạch, 50 commit, cộng đợt dọn và đợt mở rộng thư viện.

Hai SKIP là cố ý, không phải gate hỏng: `gallery.html` là trang nội bộ nên không khai
`data-theme="light"`, và `vietnam-simplification-comparison.html` không dùng lớp annotation.

Trong repo: 50 mẫu ở `samples/`, 14 hồ sơ ở `research/`, 29 catalog spec, 11 minh hoạ SVG,
18 preset chart ECharts, 50 component matplotlib EIR.

**Đợt mở rộng thư viện đã xong**, làm một lần cho lâu dài. Bốn thứ mới:

1. **Lớp schema dùng chung hai engine**: `charts/schema.vocab.json` (từ vựng, cả hai ngôn ngữ
   cùng đọc), `charts/echarts/schema.mjs`, `charts/matplotlib/schema.py`, và 28 ca hợp đồng ở
   `charts/fixtures/schema-cases.json` chạy ở CẢ HAI phía. Mọi preset mới phải đi qua lớp này.
   Quy ước đầy đủ trong `CLAUDE.md`.
2. **Sáu preset ECharts mới** 13 tới 18: line có chú thích, bar ngang xếp hạng kèm biến thể
   Cleveland dot, scatter chia phần tư, dot strip phân phối, football field, lưới độ nhạy.
3. **Năm component nhóm B** khối 25 tới 29: tóm tắt điều hành bốn ô, thẻ kịch bản, dải thắng
   thua, ngã ba chính sách, dải tự sự.
4. **Họ đường cong** cho matplotlib: `viz_eir_curves.py` với `c_yield_curve` và
   `c_futures_curve`, cộng cờ `zero_is_signal` thêm vào `c_spread`.

## Phase 2 đã dựng gì

Kế hoạch và lý do đầy đủ ở `docs/superpowers/plans/2026-08-07-phase2-pipeline-va-gate.md`.
Quy ước dùng hàng ngày ở `CLAUDE.md`. Tóm tắt để biết cái gì nằm đâu:

```
pipeline/
├── orchestrator.py   một lệnh chạy trọn sáu bước, ba checkpoint ghi artifact
├── build_html.py     markdown + sổ nguồn -> một file HTML tự đủ
├── render_pdf.py     WeasyPrint, và tự mở lại file kiểm ngay sau khi ghi
├── bake_svg.mjs      đóng băng callout của annotate.js thành SVG tĩnh
└── report.css        trang giấy: khổ, lề, chạy đầu chân trang, ba kiểu bìa

gates/
├── run.mjs           runner, in bảng, trả exit code
├── gates.mjs         mười gate, mỗi gate một hàm thuần để test gọi thẳng
├── pdf_checks.py     mọi phép đo trên PDF nhị phân, gọi một lần dùng chung
└── fixtures/         cặp đỏ và xanh cho từng gate

examples/mau-phase2/  báo cáo mẫu 6 trang, chạm cả hai engine chart và một minh hoạ
```

Một lệnh chạy hết: `npm run mau`.

## Bốn thứ Phase 2 tìm ra, đều đo được bằng số

1. **Callout của minh hoạ mất sạch trong PDF.** `annotate.js` vẽ bằng JavaScript lúc chạy,
   WeasyPrint không chạy JS. Bản gốc con tàu qua WeasyPrint cho 42 nét vẽ và 0 trên 7
   callout; bản đã bake cho 74 nét vẽ và đủ 7. Bug lớp thứ tư cùng họ với ba lớp cũ, đã
   sống trong repo suốt Phase 1.
2. **Tầng text không phân biệt được font đúng với font hệ thống.** Cùng một trang, bản có
   `@font-face` cho `Spectral`, bản bỏ `@font-face` cho `Noto-Serif`. Cả hai đều 0 FFFD,
   0 ký tự synthetic, tầng text đúng dấu y hệt. Gate 2 FONT-PDF sinh ra từ đây.
3. **Callout khai `'Be Vietnam Pro'`, một font repo không nhúng.** Mọi callout đang in
   bằng font hệ thống. Đã vá `annotate.js` sang `'IBM Plex Sans'`.
4. **Trục giá trị in `1,200` thay vì `1.200`.** Mặc định của ECharts, ảnh hưởng mọi preset
   không tự truyền formatter. Đã vá `valueAxis` trong `theme.mjs`.

## Ba cái bẫy của tầng trang giấy, đã cắn thật

- `string-set: content()` đặt lên `body` biến toàn bộ văn bản thành chuỗi chân trang, và
  WeasyPrint in nguyên khối đó tràn đè lên cả trang.
- `.bao-cao h1 { color: var(--ink) }` đè màu kế thừa từ `.bia`, cho ra chữ ink trên nền
  ink. Tiêu đề biến mất khỏi bìa mà vẫn nguyên trong tầng text.
- `name` của `valueAxis` đè lên `title.subtext` vì cả hai đóng ở đỉnh trục.

## Một việc nhỏ còn nợ, làm kèm lúc nào cũng được

- Bảng số liệu đi kèm đường cong là ràng buộc cứng của đặc tả nhưng thuộc tầng HTML, chart
  không tự lo được. Mọi báo cáo dùng `c_yield_curve` phải ghép thêm `12-hairline-data-table`.

Hai việc còn lại của mục này đã đóng ở đợt dọn 07-08: schema nay có trường `do_tin_cay` riêng
ở cấp điểm, và từ vựng có đủ `usd_thung` cùng `usd_oz` nên `c_futures_curve` không phải bỏ
phép kiểm đơn vị nữa.

## Chạy được từ máy sạch

```bash
cd ~/HT-viz-rendering
npm install
npm run setup:browser      # BUOC RIENG, playwright-core khong tu tai browser
pip install --break-system-packages -r requirements.txt
npm run verify && npm test && python3 -m pytest tests/ -v   # THU TU NAY QUAN TRONG
```

**`verify` phải chạy TRƯỚC `test`, không đảo được.** Thứ tự cũ ghi ngược và trên máy sạch thì
luôn đỏ. Nguyên nhân: `.gitignore:10` bỏ qua `charts/echarts/out-*.svg`, `git ls-files` cho 0
file, nhưng `catalog_khop_nguon.test.mjs` lại đòi mọi đường dẫn xem trước trong mục lục phải trỏ
tới file có thật. Chính `verify-charts.mjs` mới là thứ sinh ra các file đó, như một hiệu ứng phụ.
Hai agent độc lập cùng vấp lỗi này trong worktree sạch ngày 07-08, cả hai đều phải tự `git stash`
để chứng minh nó có sẵn ở HEAD chứ không phải do mình gây ra.

Đây đúng họ với những bẫy khác của repo: chạy trơn tru trên máy đã có sẵn artifact, chỉ hỏng ở
máy sạch, và không phép nghiệm thu nào của repo chạy từ máy sạch nên không ai thấy. Cách chữa
đúng hơn là cho test tự sinh artifact nó cần hoặc SKIP kèm lý do rõ, thay vì phụ thuộc thứ tự
lệnh trong tài liệu. Chưa làm.

Không cần cài font hệ thống: bản HTML nhúng base64 trong `design-system/fonts/fonts-embedded.css`,
chart matplotlib đọc `design-system/fonts/ttf/` (6 face, 404KB, đã commit). Sinh lại bằng
`python3 design-system/fonts/extract-ttf.py`, script này trích ngược từ chính file CSS kia nên
chạy offline. Phải có bản `.ttf` riêng vì matplotlib không đọc được woff2.

Mọi chỗ mở Chromium đều đi qua `scripts/lib/chromium.mjs`, tức hỏi thẳng `playwright-core` xem
bản nào khớp phiên bản thư viện. Trước đợt dọn, `verify-illustrations.mjs` và `deps.test.mjs`
hardcode `chromium-1228` còn `verify-components.mjs` tự dò bản mới nhất, nên `npm run verify`
nghiệm thu bằng hai binary khác nhau trong cùng một lần chạy, và trên máy sạch thì chết ENOENT.
Có gate trong `deps.test.mjs` chặn tái phạm: nó quét `scripts/` và `tests/` tìm đường dẫn cache
hardcode lẫn lời gọi `launch()` trực tiếp.

## Repo này là gì

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF
in được, có chart tài chính đúng chuẩn, component kể chuyện print-safe, và minh hoạ ngành SVG
neo được số liệu vào từng bộ phận vật thể.

Thiết kế đầy đủ ở `docs/specs/2026-08-06-ht-viz-rendering-design.md`, 15 mục. Đọc mục 3 (bảng
quyết định đã chốt) và mục 5 (kiến trúc) trước khi động vào code. Quy ước làm việc chi tiết ở
`CLAUDE.md`, cổng vào cho Claude là `SKILL.md`.

## Ba phán quyết của người dùng ở đợt dọn sau Phase 1

1. **`viz_render_py.py`: XOÁ.** Nó mang bảng màu giấy ngà ấm đã bị bác và không file nào import.
   Hệ quả phải biết: repo không còn 10 primitive lõi (bar_grouped, line, waterfall, scatter,
   heatmap, donut, slope, payoff, bar_h, bar_stacked) ở đường matplotlib. Tương đương gần nhất
   trong 48 component EIR là comparison, index100, flow_bridge, comps_scatter, correlation_matrix,
   distribution. Bản gốc vẫn nằm ở `_harvest/harvest-cfa-skillchain/viz-engine/viz_render_py.py`
   nếu cần port lại sang bảng màu lạnh.
2. **Hệ màu tối: GIỮ cho trang nội bộ, KHOÁ SÁNG cho file giao đi.** ĐÃ SỬA MỘT PHẦN ở cú bẻ lái
   07-08, đọc kỹ vì luật này có HAI TẦNG và chúng có số phận khác nhau.

   *Tầng quyết định*: đã mở. `data-theme` nay là tham số `--chu-de` chứ không còn ghi cứng trong
   f-string của `lap_trang()`.

   *Tầng nợ tài sản*: **VẪN NGUYÊN, và người dùng mở bảng màu KHÔNG trả hộ được.** Lý do đo được
   ban đầu là chart matplotlib và minh hoạ SVG chỉ có bảng màu sáng, nên máy khách đặt theme tối
   cho ra trang nền `#0A1420` mà chart vẫn nền trắng. Đó là sự thật về mã nguồn, không phải về
   khẩu vị. Vì vậy **mặc định vẫn là `light`** cho tới khi trả xong nợ ở Phase 3.

   Gate `khoa-sang-khong-doi-theo-may-khach` phải viết lại: nó chỉ đọc
   `getComputedStyle(document.body)` nên KHÔNG nhìn thấy chart hay minh hoạ, tức không có khả
   năng phát hiện đúng cái bệnh mà luật này sinh ra để tránh.
3. **`.q-dot`: vá cả hai lỗi cùng một rule.** Thêm `display: inline-block` cho hết méo, và thay
   `box-shadow` chết bằng `::before` vẽ vòng tròn thật.

## Ba thuộc tính CSS mà WeasyPrint bỏ qua

Khối ma trận 2x2 dính cả ba cùng lúc, tưởng là một lỗi bố cục hoá ra là ba lỗi độc lập. Bảng
đầy đủ ở `CLAUDE.md`, tóm tắt:

| Thuộc tính | WeasyPrint làm gì | Đã thay bằng |
|---|---|---|
| `aspect-ratio` | Bỏ qua, khối cao 0 | `height: 438px` |
| `overflow`/`clip` trên `<table>` | Bỏ qua, bảng vẫn in ra | Bọc trong `<div class="visually-hidden">` |
| `writing-mode` | Bỏ qua nhưng vẫn áp `transform` | `rotate(-90deg) translateX(-100%)` |
| SVG không hợp lệ XML | Bỏ qua CẢ FILE, im lặng | Tên font bọc nháy đơn trong `theme.mjs` |

**Bẫy nặng nhất tìm được, và nó sống sót trọn Phase 1**: cả 12 chart ECharts xuất ra SVG **không
phải XML hợp lệ**, vì `FONT_STACK` bọc bằng nháy kép rồi bị ECharts nhúng vào thuộc tính
`style="..."`. WeasyPrint bỏ qua cả file, PDF ra 0 nét vẽ, chart biến mất sạch. Trình duyệt vẫn
hiện đúng nên soi bản HTML không bao giờ thấy, và mọi gate cũ chỉ đếm chuỗi chứ không parse. Đã
vá `theme.mjs`, thêm gate parse XML vào `verify-charts.mjs`, kiểm là gate đỏ được khi phá ở nguồn.
Bài học chung: **một gate đếm được không thay được một gate PARSE**.

Cách tìm ra: dựng ca tối giản đã biết là đúng rồi thêm từng yếu tố. Bốn biến thể đầu (grid lồng
grid, absolute inset 0, left/top phần trăm, translate âm) đều ĐÚNG, nên nghi can ban đầu bị loại
hết. Yếu tố thứ năm mới làm vỡ. Bài học lặp lại lần thứ tư trong repo: đoán nguyên nhân theo
trực giác thì trật, cô lập từng yếu tố thì trúng.

Cả ba đều có test chặn tái phạm, và cả ba test đã được kiểm là ĐỎ ĐƯỢC khi tái tạo lỗi.

## Bảy điều đã đo được, đừng làm lại

1. **Chỉ `box-shadow` có blur mới bị nướng bitmap khi in.** Offset cứng blur 0 an toàn tuyệt đối.
   Đo bằng ba biến thể độc lập. Ngoài ra WeasyPrint không render box-shadow bằng bất kỳ cú pháp
   nào, nên bóng chỉ tồn tại trên trình duyệt.
2. **`@media (max-width: Npx)` thiếu `screen` tự kích hoạt khi in**, vì vùng in A4 chỉ 688 tới
   717px sau margin.
3. **Bug rớt dấu tiếng Việt không do engine** mà do khai `font-family` bằng một tên trần thay vì
   list kết thúc generic keyword. Lỗi ra dạng "Sô´liệu" chứ không phải ô vuông nên rất dễ lọt QC.
4. **Đo dấu tiếng Việt phải dùng mực chữ qua Canvas `measureText()`**. So
   `getBoundingClientRect().height` với `fontSize × lineHeight` là tautology, không bao giờ phát
   hiện được lỗi. Gate `offline-body-dung-font-nhung` dùng đúng phép này.
5. **Dấu tiếng Việt chỉ giảm 4% ký tự mỗi dòng**, không cần buffer line-height kiểu CJK.
6. **`echarts.init` với `ssr:true` không tự thoát process.** Mọi script chart phải kết bằng
   `chart.dispose(); process.exit(0);`.
7. **Đếm ảnh trong PDF phải dùng `doc.xref_object`**, `get_images()` bỏ sót ảnh trong Tiling Pattern.
8. **`color-mix()` không render trong WeasyPrint 69.0**, ra 0 fill. Viết `rgb(R G B / A)` thay thế.
9. **`outline` không bo theo `border-radius` trong WeasyPrint**: đặt outline lên một chấm tròn thì
   ra khung vuông. Đã thử và loại khi vá `.q-dot`.

## Bốn cái bẫy đã gặp thật, đừng lặp lại

- **Catalog drift**: bộ Opvia có file catalog mô tả HTML dùng class không tồn tại trong CSS. Trang
  vẫn chạy nhưng suy biến âm thầm. `tests/consistency/catalog_drift.test.mjs` chống đúng bệnh này.
- **PACKAGE tự nhận là tự đủ**: cả hai PACKAGE chạy được ở thư mục gốc của chúng nhưng
  `ERR_MODULE_NOT_FOUND` khi copy sang chỗ khác.
- **Verify script chọn class không tồn tại**: script verify báo PASS mà chưa kiểm gì.
- **Gate xanh vì phép đo rỗng**: ba ca đã gặp và đã vá ở đợt dọn. `reduced-motion` cũ chỉ hỏi
  Playwright xem Playwright có làm đúng việc của Playwright không, luôn true kể cả khi CSS không
  có dòng nào. `offline-fonts-available` cũ dùng `.every(Boolean)` trên mảng rỗng nên trang không
  khai font nào vẫn xanh. Regex quét `SKILL.md` mở bằng `[a-z]` nên chưa bao giờ kiểm `CLAUDE.md`
  và `README.md`. Cách chữa chung: mỗi gate phải chứng minh được nó PHÂN BIỆT ĐƯỢC hai trạng thái
  trước khi được quyền xanh, và phải tự đỏ được khi cố tình phá.

## Hai xung đột đã phân xử, đừng mở lại

- **Gauge và radar**: cấm. Gauge gợi ý độ chính xác không có thật, radar có trục không độc lập.
  Đây là lý do ĐÚNG SAI PHÂN TÍCH, không dính gì môi trường xuất bản, nên nó sống qua mọi tiền
  đề. Bảy mục trong nghiên cứu là radar cải trang và bị loại theo: `radviz`, `star-coordinates`,
  `dust-and-magnet`, `star-glyph`, `shape-coding`, `progress-ring`, `wind-rose`.
- **Engine PDF**: WeasyPrint, không phải Chromium. Chromium tạo ảnh JPEG ẩn trong Tiling Pattern.
  Đã cân lại một lần nữa ở cú bẻ lái 07-08 và người dùng CHỐT GIỮ.

**Bảng màu đã RỜI khỏi danh sách này.** Nó từng chốt trắng lạnh chứ không phải giấy ngà ấm, và ba
nguồn độc lập hội tụ ủng hộ nó vẫn là bằng chứng tốt. Nhưng ngày 07-08 người dùng chủ động mở:
trắng lạnh nay là MẶC ĐỊNH chứ không phải hằng số. Cái mất là quyền phủ quyết một bảng màu khác,
không phải cái mất về bằng chứng.

## Đợt dọn sổ nợ 07-08, và cái bẫy nó tự tạo ra

Năm món nợ đã đóng: em-dash trong tài liệu và comment, thư mục `charts/echarts/out/` rỗng,
`verify-illustrations.mjs` quy lỗi theo chuỗi con, ba nợ schema chart, bảng markdown thiếu
ô gộp và caption.

**Bài học đắt nhất của đợt này**: phép dọn gạch ngang hàng loạt đã đổi chính hai ký tự nằm
bên trong character class của hai gate chặn em-dash, biến chúng thành `/[--]/g`. Regex đó
chỉ còn khớp dấu gạch nối thường, tức gate báo FAIL cho mọi nội dung bình thường và không
còn bắt em-dash, mà vẫn chạy trơn tru không báo gì. **Một phép dọn hàng loạt có thể vô
hiệu hoá đúng cái gate canh nó.** Nay hai regex đó viết bằng escape unicode, và luật
em-dash chuyển thành tuyệt đối cho toàn repo chính, có gate riêng ở
`tests/consistency/em_dash_repo.test.mjs` miễn trừ đúng hai chỗ tường minh.

Ba việc khác đáng ghi: `verify-illustrations.mjs` nay trích đường dẫn từ từng frame stack
rồi so basename, đúng cách phía network vẫn làm, nên không còn quy oan cho lớp annotation
mọi lỗi phát sinh trong file tên kiểu `annotate-demo.js`. Schema chart có trường
`do_tin_cay` riêng ở cấp điểm, tách khỏi `source.tier` ở cấp series, cộng hai đơn vị
`usd_thung` và `usd_oz`. Bảng markdown hỗ trợ ô gộp cột và `<caption>`, và ở đây cũng có
một bẫy nhỏ: `strip("|")` của Python bỏ NHIỀU pipe liên tiếp, nên hàng kết thúc bằng ô gộp
bị mất một cột mà bảng vẫn hiện ra bình thường.

## Mục lục thư viện, để phiên sau không phải dò lại

`catalog/CATALOG.md` liệt kê cả 108 tài sản dưới một dạng, mỗi dòng ghi mã, trả lời câu
hỏi gì, và khi nào đừng dùng. `catalog/INDEX.json` là bản máy đọc. `catalog/contact-sheet.pdf`
là 50 bản xem trước để nhìn cả kho một lượt. Cả ba sinh tự động bằng
`scripts/sinh_catalog.py`, `scripts/sinh_xem_truoc.py` và `scripts/sinh_contact_sheet.py`,
có test ép khớp mã nguồn nên không trôi được.

Dựng chúng đòi lấp một lỗ hổng thật: **50 trên 50 component matplotlib không có mô tả nào
dùng được**, 28 cái không có lấy một dòng docstring. Nay cả 50 đều ghi rõ trả lời câu hỏi
gì, cần dữ liệu gì, và khi nào KHÔNG nên dùng.

Hai lỗi bắt được nhờ chính contact sheet, cả hai đều nằm sẵn trong thư viện từ trước:

- **`c_sensitivity_grid` và `c_correlation_matrix` dùng `imshow`**, tức nhúng một ảnh
  BITMAP vào SVG. Báo cáo nào dùng hai component đó đều sẽ vi phạm luật vector và bị gate
  RASTER chặn. Đo được: bản cũ cho một ảnh 1216x511 trong PDF. Đã thay bằng `Rectangle` và
  `axvspan`, nay 0 ảnh.
- **CSS Grid phân trang rất tệ trong WeasyPrint**: mỗi hàng grid bị đẩy sang một trang
  mới, 29 ô ra 9 trang với hai phần ba mỗi trang bỏ trống. `inline-block` phân trang bình
  thường. Kèm hai chi tiết nhỏ: ba ô `32,4% + 1,4%` cộng lại vượt 100% nên mỗi hàng chỉ
  chứa hai ô, và SVG không khai `width`/`height` thì không co theo ô mà giữ nguyên cỡ px
  của viewBox.

## Sổ nợ, chưa chặn ai

- Em-dash trong `_harvest/` giữ nguyên, đó là bản gốc để còn đối chiếu. Repo chính đã sạch
  tuyệt đối và có gate ép giữ vậy.

- `_harvest/` vẫn còn 57MB. Phase 2 đã dỡ `lab-gate/` và `lab-evidence/` vào `gates/`;
  `harvest-extras/pipeline-stocklpt/` chưa dỡ, chỉ mới đọc để tham khảo cách dựng markdown.
- Nhánh PPTX chưa làm. Operator chốt Phase 2 chỉ lo đường HTML sang PDF. Hai bug đã biết của
  `html2pptx.js` (SVG làm crash cả file, bảng mất trắng) vẫn nằm nguyên trong `_harvest/`.
- 18 preset ECharts vẫn là script hardcode dữ liệu demo, chưa có bề mặt gọi được với dữ liệu
  thật. Báo cáo hiện chép preset vào `hinh/` của mình rồi thay số, và cách đó đúng tinh thần
  "preset là ý tham khảo" nhưng chưa tiện. Cân nhắc ở Phase 3.
- Bảng markdown chưa hỗ trợ ô gộp HÀNG (`rowspan`), mới chỉ gộp cột. Chưa gặp bài cần tới.
- 29 trên 50 component matplotlib chưa có bản xem trước, vì chúng không có bộ tham số ví
  dụ trong `spec_showcase.json`. Contact sheet liệt kê tên chúng kèm lý do thay vì để ô
  trống. Thêm ví dụ cho chúng là việc còn lại.
- `c_sensitivity_grid` dùng bảng màu ấm `_cmap_warm()` trong khi repo đã chốt bảng màu
  lạnh. Chưa đụng vì nó nằm ngoài phạm vi đợt này.

## Các phase sau, ĐÃ ĐỊNH NGHĨA LẠI theo cú bẻ lái

Viết plan riêng khi phase trước nghiệm thu xong.

**Phase 3 nay là TRẢ NỢ NỀN, không phải xây tính năng.** Người dùng đã chốt thứ tự này. Chi tiết
ở mục đầu file. Tóm tắt: generator chủ đề từ JSON, migrate 345 hex minh hoạ, 29 chỗ `color=PAPER`
sang `ON_INK`. Xong ba việc đó thì mỗi chủ đề mới chỉ còn khoảng 5 file thay vì 17.

**Phase 4: dựng làn `html-song` cho chạy được.** Tách `option()` khỏi `render` trong ECharts để
một nguồn preset phục vụ cả hai làn, cộng bundle tree-shaken. Đã ĐO THẬT: bundle qua
`echarts/core` nặng 733KB thô so với 1,1MB của bản đầy đủ, giảm 371KB tức 33% trên mọi file làn
A, và nghiệm thu bằng render thật sankey 31/31, treemap 48/48, candlestick 49/49 nét vẽ, giống
hệt engine đầy đủ và trùng khớp file `.svg` đang commit. Danh sách đủ cho cả 18 preset: 8 Chart
(`bar/line/scatter/custom/heatmap/sankey/treemap/candlestick`), Component
(`grid/tooltip/title/legend/graphic/markLine/markPoint/markArea/visualMap`), Feature
`labelLayout`, chỉ `SVGRenderer`.

**Phase 5: bộ gate làn A.** Chín gate mới, mỗi cái đã có phép đo và mô tả fixture đỏ:
`OFFLINE-INTACT`, `JS-SILENT-FAIL`, `REDUCED-MOTION`, `KEYBOARD-PATH`, `CONTRAST-ALL-THEMES`,
`SIZE-BUDGET`, `NO-JS-CONTENT`, `RESPONSIVE-WIDTH`, `THEME-MATCH`. Đặc tả đầy đủ ở memory toàn
cục. Hai gate đã cân và LOẠI vì không dựng nổi fixture đỏ tất định: "mượt 60fps" và "trang phải
đẹp".

**Phase 6: báo cáo mẫu vận tải biển**, nghiệm thu bằng bộ gate của đúng làn nó chọn.

Mười gate cũ KHÔNG chết: cả mười sống nguyên cho làn `pdf-so`, chỉ `report.css` đổi khổ trang và
tầng 2 của gate 5 phải trỏ đúng cặp file. Cộng bốn gate mới chỉ digital PDF mới có:
`HYPERLINK-LIVE`, `BOOKMARK-OUTLINE`, `PAGE-RATIO`, `MIN-FONT-SCREEN`.
