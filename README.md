# HT-viz-rendering

Sinh báo cáo và phân tích tài chính tiếng Việt chất lượng xuất bản: HTML self-contained và PDF in được.

## Cài đặt

```bash
npm install
pip install --break-system-packages -r requirements.txt
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
