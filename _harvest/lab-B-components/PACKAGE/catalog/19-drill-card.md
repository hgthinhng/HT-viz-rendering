# Số liệu trong câu văn, bấm để xem gốc

`KHỐI 19 · THẺ TRUY NGUỒN (DRILL-CARD)`

## Mô tả / khi nào dùng

Trả lời: "Số này lấy từ đâu, tính thế nào?" Khác badge nguồn ở chỗ đây là tương tác click-to-reveal nhúng trong văn xuôi, không phải nhãn cố định cạnh biểu đồ. Bản gốc tham chiếu (Kimi) dùng position:fixed theo con trỏ chuột, KHÔNG print-safe. Bản này dùng panel bung ngay dưới dòng văn bản, và ép hiện toàn bộ khi in (xem CSS @media print) để không mất thông tin trên giấy. KHÔNG dùng quá 3-4 lần mỗi trang; quá nhiều điểm bấm làm rối văn bản.

## Phụ thuộc JS

Cần `components.js` (hàm `initDrillables()` tự chạy khi DOM sẵn sàng) để bấm `.drillable` bật/tắt `.drill-panel` liền kề trên màn hình. Không có JS, panel vẫn RENDER được (mặc định ẩn qua CSS) và luôn hiện đầy đủ khi in (`@media print { .drill-panel { display: block !important; } }`) — không mất thông tin trong bản in dù JS có chạy hay không.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<p style="max-width:65ch; font-size:15px; line-height:1.75;">
    Trong quý 2/2026, đội tàu ghi nhận hiệu suất khai thác bình quân
    <span class="drillable">90,1%</span>, cao hơn 2,4 điểm phần trăm so với cùng kỳ, chủ yếu nhờ giảm thời gian chờ cầu cảng tại khu vực Cái Mép, Thị Vải.
  </p>
  <div class="drill-panel">
    <div class="d-title">HIỆU SUẤT KHAI THÁC BÌNH QUÂN · Q2/2026</div>
    <div class="d-val">90,1%</div>
    <div>Tính bằng (số ngày tàu hoạt động thương mại) / (số ngày tàu sẵn sàng khai thác), bình quân theo trọng số DWT toàn đội tàu 23 chiếc.</div>
    <div class="src-badge" data-tier="noi-bo" style="margin-top:8px;"><i class="tier-dot"></i>Báo cáo vận hành nội bộ, chốt 2026-06-30</div>
  </div>
```
