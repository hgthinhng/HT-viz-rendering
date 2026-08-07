# Fixture đỏ và xanh

Mỗi gate trong `gates/gates.mjs` có một cặp fixture: một bản phải PASS và một bản phải
FAIL. Bộ test `tests/consistency/gate_do_xanh.test.mjs` chạy cả cặp và ép đúng hai kết
quả đó.

Lý do có thư mục này nằm trong lịch sử của chính repo. Đợt dọn sau Phase 1 tìm ra ba
gate xanh vì phép đo rỗng: một gate hỏi Playwright xem Playwright có làm đúng việc của
Playwright không, một gate dùng `.every(Boolean)` trên mảng rỗng, một gate có regex
chưa bao giờ khớp file nào. Cả ba đều chạy trơn tru và cả ba đều vô dụng.

Luật rút ra, áp cho mọi gate về sau: **một gate phải chứng minh nó phân biệt được hai
trạng thái trước khi nó có quyền báo xanh.** Fixture đỏ chính là bằng chứng đó. Gate nào
không đỏ được với fixture đỏ của chính nó thì gate đó chưa tồn tại.

## Cách fixture được dựng

Phần lớn fixture là dữ liệu tổng hợp trong file test, không phải file trên đĩa: gate là
hàm thuần nhận `{html, pdf}` nên dựng thẳng hai giá trị đó là đủ và chạy trong mili
giây. Chỉ hai gate cần file thật, vì chúng gọi tiến trình con đọc file:

| File | Dùng cho | Vai trò |
|---|---|---|
| `ledger-xanh.html` | gate 10 LEDGER | sổ nguồn hợp lệ, mọi giá trị trỏ về nguồn có thật |
| `ledger-do.html` | gate 10 LEDGER | trỏ tới nguồn không tồn tại, và lệch bậc bằng chứng |
| `nguon-xanh.html` | gate 9 SOURCE-LEAK | bản gửi đi sạch |
| `nguon-do.html` | gate 9 SOURCE-LEAK | lộ tên riêng viết tắt trong mạng lưới |

## Hai giới hạn, nói thẳng

Fixture tổng hợp kiểm được LOGIC của gate, không kiểm được rằng cấu trúc dữ liệu do
`pdf_checks.py` sinh ra vẫn khớp với thứ gate mong đợi. Ràng buộc đó do
`tests/smoke/pipeline_that.test.mjs` giữ: nó chạy trọn đường ống thật rồi chạy cả bộ
gate trên kết quả.

Gate 2 FONT-PDF có thêm một bằng chứng ngoài test, ghi lại ở đây vì nó là lý do gate
này ra đời: cùng một trang HTML, bản khai `@font-face` base64 cho ra `Spectral` và
`IBM-Plex-Mono` trong PDF, bản bỏ `@font-face` cho ra `Noto-Serif` và `Liberation-Mono`.
Cả hai bản đều 0 ký tự U+FFFD và 0 ký tự synthetic, tầng text đọc ra tiếng Việt đúng
dấu y hệt nhau. Nghĩa là mọi phép đo tầng text đều mù với ca này.
