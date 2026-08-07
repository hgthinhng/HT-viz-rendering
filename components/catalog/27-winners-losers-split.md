# Ai hưởng lợi, ai chịu thiệt khi trần SFL được nới

`KHỐI 27 · DẢI THẮNG THUA`

## Mô tả / khi nào dùng

Trả lời: "Khi biến số hoặc chính sách này đổi, ai được và ai mất?" Một dòng mô tả biến đổi ở trên, hai cột liệt kê thực thể hưởng lợi và chịu thiệt ở dưới, mỗi thực thể kèm đúng một câu lý do. KHÔNG dùng khi chỉ có MỘT thực thể chuyển trạng thái theo thời gian (không phải nhiều thực thể chia phe cùng lúc): dùng `14-before-after`. KHÔNG dùng khi cần so sánh nhiều tiêu chí cùng lúc giữa các phương án loại trừ nhau: dùng `13-options-comparison-table`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="winlose">
  <div class="wl-event">
    <div class="wl-event-label">Biến số thay đổi</div>
    <div class="wl-event-text">Trần tỷ lệ nguồn vốn ngắn hạn cho vay trung dài hạn (SFL) nâng từ 30% lên 35%, dự kiến hiệu lực đầu 2027.</div>
  </div>
  <div class="wl-split">
    <div class="wl-side wl-win">
      <div class="wl-side-label">Hưởng lợi</div>
      <div class="wl-entity">
        <div class="wl-entity-name">Ngân hàng có SFL sát trần cũ (nhóm VPB, TCB)</div>
        <div class="wl-entity-why">Có thêm dư địa giải ngân trung dài hạn ngay quý đầu hiệu lực, không phải cơ cấu lại danh mục hay huy động vốn dài hạn gấp.</div>
      </div>
      <div class="wl-entity">
        <div class="wl-entity-name">Chủ đầu tư bất động sản đã đủ pháp lý, đang chờ vốn</div>
        <div class="wl-entity-why">Room tín dụng trung dài hạn nới ra đúng lúc, rút ngắn thời gian chờ giải ngân dự án.</div>
      </div>
    </div>
    <div class="wl-side wl-lose">
      <div class="wl-side-label">Chịu thiệt</div>
      <div class="wl-entity">
        <div class="wl-entity-name">Nhóm ngân hàng còn nhiều dư địa SFL (khối quốc doanh)</div>
        <div class="wl-entity-why">Không hưởng lợi biên tương ứng vì đã có sẵn dư địa, trong khi lãi suất cho vay trung dài hạn cạnh tranh hơn do đối thủ cùng được nới room.</div>
      </div>
      <div class="wl-entity">
        <div class="wl-entity-name">Người gửi tiết kiệm kỳ hạn ngắn</div>
        <div class="wl-entity-why">Ngân hàng bớt áp lực đảm bảo tỷ lệ SFL nên giảm ưu đãi lãi suất huy động ngắn hạn, lãi suất tiền gửi dưới 6 tháng có thể đi ngang hoặc giảm nhẹ.</div>
      </div>
    </div>
  </div>
</div>
```
