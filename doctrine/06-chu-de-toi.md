# Chủ đề tối

Từ 09-08 repo có hai chủ đề: `sang-lanh` (mặc định) và `toi-lanh`. File này nói cách nó
hoạt động, khi nào dùng, và ba chỗ đã cắn trong lúc dựng.

---

## 1. Khi nào dùng, khi nào không

**Dùng** cho làn `html-song` khi người đọc mở trên màn hình và có thể ở môi trường thiếu sáng.

**Không dùng** cho bản gửi ra ngoài mà ta không kiểm soát được môi trường mở. Mặc định của
bản giao khách vẫn là khoá sáng, và lý do không phải kỹ thuật nữa mà là thói quen đọc: một
báo cáo tài chính nền tối vẫn là thứ lạ với phần lớn người nhận, và lạ ở chỗ không cần thiết
thì chỉ tạo nghi ngờ.

**Không dùng** cho làn `pdf-so` trừ khi biết chắc người đọc không in. PDF nền tối in ra vừa
tốn mực vừa đọc kém.

## 2. Cách nó hoạt động: bốn đường, cùng một nguồn

Nguồn duy nhất là `design-system/themes/*.json`. Chạy `node design-system/generate-tokens.mjs`
sinh ra ba đích: `tokens.css`, `tokens.py`, `charts/echarts/theme.mjs`.

Từ đó, bốn loại nội dung đổi màu theo bốn cách khác nhau:

| Loại | Cách đổi màu |
|---|---|
| Chữ và khối trong trang | dùng thẳng `var(--token)` trong CSS |
| Minh hoạ SVG | đã dùng `var(--ilus-1..9)`, trình duyệt lo phần còn lại |
| Chart TĨNH (ECharts và matplotlib) | hậu xử lý chuỗi SVG, đổi hex thành `var(--token, #hex-cũ)` |
| Chart SỐNG (ECharts mount lúc chạy) | đọc giá trị thật của biến CSS qua `getComputedStyle` rồi truyền vào option |

Hai đường cuối tồn tại vì cùng một lý do: ECharts và matplotlib đều ghi hex THẲNG vào SVG,
không biến CSS nào chạy ở đó.

## 3. Dải chín bậc của minh hoạ ĐẢO NGƯỢC, không ánh xạ một đối một

Đây là ràng buộc đã biết từ trước và nó vẫn đúng: **một mã màu trong minh hoạ đóng nhiều vai
cùng lúc**, ví dụ vừa là nền trời vừa là thân kim loại. Ánh xạ một đối một từ chủ đề sáng
sang chủ đề tối không tách được hai vai đó.

Thứ giữ được qua hai chủ đề là THỨ TỰ BẬC, không phải giá trị. Bậc 1 ở chủ đề sáng là tối
nhất; ở chủ đề tối, bậc 1 là sáng nhất. Hình vẫn đọc được vì tương quan đậm nhạt giữa các bộ
phận không đổi.

Hệ quả: nếu một hình cần tách hai vai của cùng một bậc, phải tách ở TỪNG HÌNH bằng cách dùng
hai bậc khác nhau, không tách bằng cách thêm token.

## 4. Nhóm token "trên nền mực"

Trang bìa dùng `background: var(--ink)` để đảo màu so với thân bài. Ở chủ đề tối, `--ink` là
màu SÁNG, nên bìa thành nền sáng, và đó là hành vi đúng: bìa luôn tương phản với thân.

Nhưng chữ trên bìa thì không tự đảo theo. Trước 09-08, `.bia-dek` và `.bia-meta` viết cứng ba
mã màu sáng, nên ở chủ đề tối chúng thành chữ nhạt trên nền sáng, gần như không đọc được.

Nhóm `--on-ink`, `--on-ink-md`, `--on-ink-lo`, `--on-ink-line` sinh ra cho đúng chỗ này: màu
của chữ đặt trên khối tô bằng `var(--ink)`. Ở chủ đề tối chúng đảo vai thành màu tối.

Phía Python đã có hằng `ON_INK` từ lâu mà phía CSS thì không. Đó là kiểu lệch chỉ lộ ra khi
thêm chủ đề thứ hai.

## 5. Ba chỗ đã cắn, ghi lại để không lặp

**Chart sống mount TRƯỚC khi chủ đề đổi thì giữ màu cũ.** Nó đọc `getComputedStyle` đúng một
lần lúc mount. Với chủ đề khai sẵn trong HTML thì không sao. Nhưng nếu sau này làm nút đổi
chủ đề động, phải mount lại chart hoặc gọi `setOption` với bảng màu mới; hiện chưa có cơ chế
đó và đây là giới hạn đã biết.

**`_veSauLayout` chạy SAU khi thay màu.** Nhãn vẽ bằng `graphic` trong bước hậu layout không
nằm trong option gốc, nên lần đầu nối chủ đề, bốn nhãn của một chart vẫn giữ màu chủ đề sáng
trong khi cả phần còn lại đã đổi. Kết quả của `_veSauLayout` cũng phải đi qua phép đổi màu.

**Đường sinh SVG qua Chromium đi vòng qua `renderStatic`.** `renderStatic` bọc hex thành
`var()`, nhưng `sinh-svg-preset.mjs` render bằng trình duyệt rồi lấy `outerHTML`, nên nó trả
về hex thô và chart tĩnh mất khả năng đổi chủ đề. Hồi quy này im lặng vì hình vẫn đúng màu ở
chủ đề sáng.

## 6. Kiểm bằng gì

Phép đo đúng là mở trang ở cả hai chủ đề rồi ĐỌC MÀU THẬT bằng `getComputedStyle`, không nhìn
ảnh chụp. Ba thứ phải kiểm:

1. Nền trang đổi.
2. Nền chart đổi theo nền trang, tức không còn ô trắng nổi giữa trang tối.
3. Chữ trong chart đổi, gồm cả nhãn vẽ bằng `graphic`.

Gate 9 `THEME-MATCH` của làn `html-song` đã đo lớp 1 và lớp 2 của việc này.
