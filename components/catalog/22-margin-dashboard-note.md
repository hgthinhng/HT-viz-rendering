# Rail ngữ cảnh đổi theo mục · bản print-safe

`KHỐI 22 · TÓM TẮT BÊN LỀ (MARGIN DASHBOARD NOTE)`

## Mô tả / khi nào dùng

Bản tham chiếu Kimi vẽ dashboard bên phải bằng <canvas> cố định toàn trang (position:fixed), đổi nội dung theo section đang cuộn qua IntersectionObserver, sinh động nhưng: (1) canvas không có text thật cho screen reader, (2) fixed vỡ hoàn toàn khi in. Bản này dùng <aside> thật với position:sticky chỉ trong phạm vi khối cha (không sticky toàn viewport), text thật nên đọc được, và tự chuyển thành khối tĩnh nằm dưới nội dung khi in hoặc màn hẹp. KHÔNG dùng khi bản in là đầu ra chính: ở `@media print`, `.margin-note` chuyển `position: static`, mất `border-left` và xếp thành một hàng flex nằm dưới nội dung, nên lợi thế theo dõi ngữ cảnh song song khi cuộn hoàn toàn biến mất trên giấy; lúc đó note-box đơn giản hơn cho cùng nội dung.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="with-margin-note">
    <div>
      <h3 style="font-size:18px; margin-bottom:10px;">Diễn giải: áp lực nhiên liệu quý 2/2026</h3>
      <p style="font-size:14.5px; line-height:1.75; color:var(--ink-md);">Giá VLSFO bình quân khu vực Singapore tăng từ 598 lên 641 USD/tấn trong quý, trong khi cước giao ngay tuyến nội Á chỉ tăng 6%. Khoảng cách giữa hai đường này giải thích phần lớn mức giảm biên EBITDA quý. Đội tàu container feeder, nhóm tiêu thụ nhiên liệu hiệu quả nhất, vẫn giữ được biên tốt hơn nhóm tàu hàng rời cũ.</p>
      <p style="font-size:14.5px; line-height:1.75; color:var(--ink-md);">Ban điều hành đã ký hợp đồng phòng vệ giá cho 65% nhu cầu nhiên liệu quý 3, giảm một phần độ nhạy cảm với biến động giá giao ngay trong giai đoạn còn lại của năm.</p>
    </div>
    <aside class="margin-note" aria-label="Tóm tắt số liệu chính của mục này">
      <div class="mn-h">SỐ CHÍNH · MỤC NÀY</div>
      <div class="mn-item"><div class="mn-val">641<span style="font-size:12px;font-weight:400;"> USD/t</span></div><div class="mn-key">Giá VLSFO bình quân Q2/2026</div></div>
      <div class="mn-item"><div class="mn-val">65%</div><div class="mn-key">Nhu cầu nhiên liệu Q3 đã phòng vệ giá</div></div>
      <div class="mn-item"><div class="mn-val">−2,1<span style="font-size:12px;font-weight:400;"> đ.%</span></div><div class="mn-key">Thay đổi biên EBITDA quý</div></div>
    </aside>
  </div>
```
