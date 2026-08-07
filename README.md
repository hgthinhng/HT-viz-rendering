# HT-viz-rendering

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF in được.

## Cài đặt

Ba lệnh, chạy đúng thứ tự này từ một máy chưa có gì:

```bash
npm install
npm run setup:browser      # tai Chromium cho playwright-core, thieu buoc nay thi verify chet
pip install --break-system-packages -r requirements.txt
```

`npm run setup:browser` cần mạng và tải khoảng 170MB về `~/.cache/ms-playwright`. `playwright-core`
không tự tải browser lúc `npm install`, nên đây là bước riêng chứ không phải bước thừa. Mọi script
trong repo lấy đường dẫn binary từ `scripts/lib/chromium.mjs`, tức hỏi thẳng `playwright-core` bản
nào khớp phiên bản thư viện, nên không có chuyện hai script chạy hai bản Chromium khác nhau.

Không cần cài font hệ thống. Bản HTML nhúng font base64 trong `design-system/fonts/fonts-embedded.css`,
bản chart matplotlib đọc `design-system/fonts/ttf/` ngay trong repo. Cả hai là cùng một bộ Spectral,
IBM Plex Sans và IBM Plex Mono, và cả sáu file `.ttf` đã đo là phủ đủ 243 codepoint tiếng Việt.

## Máy mới, hoặc phiên Claude mới

Repo nằm ở `github.com/hgthinhng/HT-viz-rendering`, **private**. Trên một máy mới:

```bash
gh repo clone hgthinhng/HT-viz-rendering ~/HT-viz-rendering
cd ~/HT-viz-rendering
npm install
npm run setup:browser                                   # bước riêng, xem mục Cài đặt
pip install --break-system-packages -r requirements.txt
ln -sfn ~/HT-viz-rendering ~/.claude/skills/HT-viz-rendering
```

Dòng cuối là dòng làm Claude thấy được thư viện: nó trỏ `SKILL.md` vào thư mục skill, và
`SKILL.md` trỏ tiếp tới `catalog/CATALOG.md`. Từ đó một phiên mới đọc một file là biết thư
viện có gì mà không phải dò từng thư mục.

Vì repo private nên ảnh trong đó **không hotlink được**: `raw.githubusercontent.com` đòi
token, và bật GitHub Pages từ repo private trên tài khoản Pro sẽ publish site ra công
khai. Đó không phải hạn chế đáng tiếc mà là điều không cần tới: chart và minh hoạ được
nhúng thẳng vào file báo cáo, nên người nhận xem được kể cả khi offline, và kho hình chỉ
cần mở được trên máy đã clone.

## Thư viện có gì

```bash
catalog/CATALOG.md          108 tài sản, mỗi dòng: trả lời câu hỏi gì, khi nào đừng dùng
catalog/contact-sheet.pdf   50 bản xem trước, nhìn cả kho một lượt
```

Sinh lại sau khi thêm hình mới:

```bash
python3 scripts/sinh_xem_truoc.py      # render bản xem trước cho component matplotlib
python3 scripts/sinh_catalog.py        # dựng lại mục lục từ mã nguồn
python3 scripts/sinh_contact_sheet.py --pdf
```

Mô tả sửa ở NGUỒN chứ không sửa trong mục lục: comment đầu file preset, docstring
component, mục `Mô tả / khi nào dùng` của catalog, hoặc `<desc>` của SVG. Có test ép mục
lục khớp mã nguồn.

## Làm một báo cáo

Một báo cáo là một thư mục: `noi-dung.md` viết bằng markdown, `so-nguon.json` giữ nguồn cho
từng con số, `hinh/` chứa script sinh hình. Một lệnh chạy trọn từ đó ra PDF đã qua gate:

```bash
npm run mau              # chạy báo cáo mẫu trong examples/mau-phase2/
python3 pipeline/orchestrator.py <thu-muc>/noi-dung.md
```

Sáu bước: sinh hình, ghi kịch bản kể chuyện, dựng ba bản bìa để chọn, dựng HTML tự đủ cả bản
nội bộ lẫn bản gửi đi, xuất PDF bằng WeasyPrint, rồi chạy mười gate nghiệm thu. Chép
`examples/mau-phase2/` làm khung cho báo cáo mới.

Nghiệm thu riêng một cặp file bất kỳ:

```bash
node gates/run.mjs <file.html> <file.pdf> --che-do=gui-di
```

## Kiểm tra hệ thống còn sống

```bash
npm test                 # smoke test và consistency test
npm run verify           # verify cả ba nhóm hình
python3 -m pytest tests/ -v
```

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `pipeline/` | Đường ống từ markdown ra PDF, và CSS tầng trang giấy |
| `gates/` | Mười gate nghiệm thu, kèm cặp fixture đỏ và xanh cho từng gate |
| `examples/` | Báo cáo mẫu chạy được, dùng làm khung cho báo cáo mới |
| `design-system/` | Token màu, font, spacing. Nguồn chân lý là `tokens.css`. Font nhúng sẵn: `fonts/fonts-embedded.css` cho HTML, `fonts/ttf/` cho matplotlib |
| `components/` | Component kể chuyện, print-safe, kèm catalog spec |
| `charts/echarts/` | Chart cho HTML tương tác |
| `charts/matplotlib/` | Component EIR cho PDF tĩnh |
| `illustrations/` | Minh hoạ ngành SVG và lớp annotation |
| `scripts/` | Script verify, mỗi cái trả exit code |
| `tests/` | Smoke test và test chống drift |
| `research/`, `samples/` | Thư viện tham khảo để lấy ý, không phải khuôn ép |
| `_harvest/` | Khu tạm chứa tài sản gốc, sẽ dỡ dần |

## Dành cho Claude

Cổng vào để gọi skill này từ Claude là `SKILL.md`. Quy ước làm việc chi tiết ở `CLAUDE.md`.

## Thiết kế

Đọc `docs/specs/2026-08-06-ht-viz-rendering-design.md`.
