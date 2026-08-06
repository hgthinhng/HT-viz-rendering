# Lộ trình 3 giai đoạn × 6 hạng mục đầu tư

`KHỐI 04 · SWIMLANE ROADMAP (MOSCOW)`

## Mô tả / khi nào dùng

Trả lời: "Việc gì làm khi nào, ưu tiên ra sao, theo hạng mục nào?" Đầu vào: cột = giai đoạn (tên, khung thời gian, KPI mục tiêu), hàng = hạng mục, thẻ = {giai đoạn, hạng mục, ưu tiên MoSCoW, mô tả}. KHÔNG dùng khi chỉ có 1 giai đoạn (dùng step-chain) hoặc khi số hạng mục >8 (bảng sẽ quá rối, tách 2 swimlane).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="swimlane-wrap">
    <div class="swimlane">
      <div class="sl-corner">HẠNG MỤC ＼ GIAI ĐOẠN</div>
      <div class="sl-colhead now">
        <div class="sl-phase">GIAI ĐOẠN 1 · 0–12 THÁNG</div>
        <div class="sl-phase-name">Ổn định vận hành</div>
        <div class="sl-phase-kpi">Mục tiêu: biên EBITDA về lại 20%, giảm nợ ngắn hạn 15%</div>
      </div>
      <div class="sl-colhead">
        <div class="sl-phase">GIAI ĐOẠN 2 · 12–30 THÁNG</div>
        <div class="sl-phase-name">Trẻ hóa đội tàu</div>
        <div class="sl-phase-kpi">Mục tiêu: tuổi tàu bình quân xuống 11 năm</div>
      </div>
      <div class="sl-colhead">
        <div class="sl-phase">GIAI ĐOẠN 3 · 30 THÁNG +</div>
        <div class="sl-phase-name">Mở rộng &amp; khử carbon</div>
        <div class="sl-phase-kpi">Mục tiêu: 30% đội tàu tương thích nhiên liệu thay thế</div>
      </div>

      <div class="sl-rowlabel"><span class="id">FLEET</span><span class="nm">Đội tàu &amp; khai thác</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Tối ưu tuyến, giảm thời gian chờ cảng bình quân 18%</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Đóng mới 2 tàu hàng rời 38.000 DWT tiết kiệm nhiên liệu</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Thanh lý 4 tàu &gt;20 năm tuổi, tái đầu tư vòng 2</div></div>

      <div class="sl-rowlabel"><span class="id">FUEL</span><span class="nm">Nhiên liệu &amp; khí thải</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Ký hợp đồng phòng vệ giá dầu FO/VLSFO 6 tháng</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Lắp scrubber cho 6 tàu tuyến quốc tế</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="could">Thử nghiệm methanol/ammonia trên 1 tàu mẫu</div></div>

      <div class="sl-rowlabel"><span class="id">FIN</span><span class="nm">Tài chính &amp; vốn</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Tái cơ cấu khoản vay đóng tàu, kéo dài kỳ hạn</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Phát hành trái phiếu xanh tài trợ đóng tàu mới</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="could">Đánh giá niêm yết bổ sung / tăng vốn cổ phần</div></div>

      <div class="sl-rowlabel"><span class="id">CREW</span><span class="nm">Thuyền viên &amp; nhân lực</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Chương trình giữ chân sỹ quan boong/máy cấp cao</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="could">Hợp tác trường hàng hải đào tạo theo đơn đặt hàng</div></div>
      <div class="sl-cell"></div>

      <div class="sl-rowlabel"><span class="id">DIG</span><span class="nm">Số hóa vận hành</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Triển khai hệ thống theo dõi hải trình thời gian thực</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Tích hợp dữ liệu tiêu hao nhiên liệu tự động (noon report số)</div></div>
      <div class="sl-cell"></div>

      <div class="sl-rowlabel"><span class="id">ESG</span><span class="nm">ESG &amp; báo cáo phát thải</span></div>
      <div class="sl-cell"><div class="sl-card" data-prio="could">Công bố báo cáo phát thải theo chuẩn IMO DCS</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="should">Đạt xếp hạng CII nhóm C trở lên cho 80% đội tàu</div></div>
      <div class="sl-cell"><div class="sl-card" data-prio="must">Đạt xếp hạng CII nhóm B trở lên toàn đội tàu</div></div>
    </div>
  </div>
  <div class="sl-legend">
    <span class="must"><i></i>MUST</span><span class="should"><i></i>SHOULD</span><span class="could"><i></i>COULD</span>
  </div>
```
