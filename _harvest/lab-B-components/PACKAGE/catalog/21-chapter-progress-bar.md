# Định vị "đang ở đâu trong báo cáo"

`KHỐI 21 · THANH TIẾN TRÌNH CHƯƠNG (TĨNH, KHÔNG FIXED)`

## Mô tả / khi nào dùng

Bản tham chiếu Kimi dùng #era-rail { position: fixed } ẩn/hiện theo cuộn trang, sống động trên màn hình nhưng vô nghĩa khi in (rail sẽ đứng yên đè lên nội dung ở mọi trang giấy). Bản này đặt thanh tiến trình làm phần tử TĨNH đầu mỗi section (đã thấy ở khối 01–06 phía trên), nó vẫn "trôi" theo bạn khi cuộn vì mỗi section có thanh riêng, và khi in, mỗi thanh chỉ in ra ĐÚNG MỘT LẦN, ở đúng trang chứa section đó, không đè lên nội dung trang khác.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="chapter-progress"><span class="cp-num">01</span><span class="cp-track"><span class="cp-seg done"></span><span class="cp-seg"></span><span class="cp-seg"></span></span><span class="cp-label">1 / 3 · TÊN PHẦN</span></div>
```
