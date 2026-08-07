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

## Kiểm tra hệ thống còn sống

```bash
npm test                 # smoke test và consistency test
npm run verify           # verify cả ba nhóm hình
python3 -m pytest tests/ -v
```

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `design-system/` | Token màu, font, spacing. Nguồn chân lý là `tokens.css` |
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
