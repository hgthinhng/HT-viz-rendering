# 27 năm khung pháp lý & công ước ngành hàng hải

`KHỐI 03 · WALL-CHART TIMELINE`

## Mô tả / khi nào dùng

Trả lời: "Chuỗi mốc lịch sử/pháp lý dẫn tới hiện tại là gì, và mốc nào gần nhau về thời gian mà không đè nhãn lên nhau?" Đầu vào: mảng {năm, tiêu đề, mô tả, phân loại}. Thuật toán xếp lớp (greedy layering, đo bằng offsetWidth thật) tự đẩy nhãn chồng nhau lên lane cao hơn. KHÔNG dùng khi <5 mốc (dùng danh sách thường) hoặc khi cần trục thời gian có tỷ lệ chính xác đến ngày (dùng chart thật).

## Phụ thuộc JS (khác các component còn lại — hầu hết là HTML/CSS thuần)

Cần `components.js` VÀ một biến toàn cục `window.WALLCHART_DATA = {y0, y1, eras:[{a,b,label,now}], events:[{y,cls,t,d}]}` định nghĩa TRƯỚC khi `components.js` chạy (đặt `<script>window.WALLCHART_DATA={...}</script>` ngay trước `<script src="components.js">`). Xem ví dụ đầy đủ trong `gallery.html` gốc (cuối file, trước thẻ `</body>`). Không có JS → container `.wc-axis-wrap` trống, chỉ `.wc-fallback-list` (danh sách phẳng, luôn có nội dung thật cho screen reader/in ấn) hiển thị — đây là hành vi progressive-enhancement CÓ CHỦ ĐÍCH, không phải lỗi.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="wallchart" id="wallchart-shipping">
    <div class="wc-axis-wrap" aria-hidden="true">
      <div class="wc-lanes"><div class="wc-plaque-layer"></div></div>
      <div class="wc-eras"></div>
      <div class="wc-ticks"></div>
    </div>
    <p class="wc-caption" aria-hidden="true">Ba khung xanh gần đây (Nghị định mở FDI cảng biển, IMO CII, EU ETS hàng hải) là áp lực và cơ hội song song; khung đỏ (MARPOL/SOLAS) là tuân thủ xuyên suốt không thể đàm phán.</p>
    <!-- Bản đọc được cho screen reader / in ấn / no-JS. PHẢI nằm TRONG cùng
         root #wallchart-shipping vì buildWallChart() tra cứu bằng
         root.querySelector(".wc-fallback-list"); đặt ngoài root là bug thật
         đã bắt được khi nghiệm thu PDF (danh sách rỗng, xem báo cáo). Luôn có
         trong DOM, ẩn kiểu sr-only khi bản trực quan đang hiển thị (xem
         components.css). Đây là cách khắc phục điểm yếu cụ thể của bản Kimi
         tham chiếu (chart SVG không có text thay thế, screen reader bỏ qua)
         mà KHÔNG dùng role="img": role="img" trên container HTML thật sẽ che
         luôn nội dung văn bản thật bên trong, phản tác dụng. -->
    <div class="wc-fallback-list"></div>
  </div>
```
