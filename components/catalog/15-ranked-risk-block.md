# Sáu rủi ro chính, xếp theo mức tác động ước tính

`KHỐI 15 · KHỐI RỦI RO CÓ XẾP HẠNG`

## Mô tả / khi nào dùng

Trả lời: "Rủi ro nào đáng lo nhất, theo thứ tự nào?" Đầu vào: tên rủi ro, mô tả ngắn, điểm tác động (0-10) hoặc mức {cao/trung bình/thấp}. KHÔNG dùng khi rủi ro cần thể hiện đồng thời xác suất VÀ tác động (khi đó dùng ma trận 2×2 rủi ro thay vì danh sách xếp hạng đơn trục).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="risk-rank">
    <div class="risk-row" data-sev="cao"><div class="rk-idx">01</div><div><div class="rk-name">Biến động giá nhiên liệu VLSFO/HSFO</div><div class="rk-desc">Chiếm 42% giá vốn khai thác, độ biến động 12 tháng gần nhất ~28%</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:92%;"></i></div><span class="rk-num">9,2</span></div></div>
    <div class="risk-row" data-sev="cao"><div class="rk-idx">02</div><div><div class="rk-name">Gián đoạn tuyến Biển Đỏ / Hồng Hải</div><div class="rk-desc">Kéo dài hải trình thay thế, tăng phí bảo hiểm chiến tranh cho tuyến liên quan</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:78%;"></i></div><span class="rk-num">7,8</span></div></div>
    <div class="risk-row" data-sev="trung-binh"><div class="rk-idx">03</div><div><div class="rk-name">Thiếu hụt sỹ quan boong/máy cấp cao</div><div class="rk-desc">Tỷ lệ nghỉ việc sỹ quan cấp cao 14%/năm, cao hơn mức an toàn vận hành</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:62%;"></i></div><span class="rk-num">6,2</span></div></div>
    <div class="risk-row" data-sev="trung-binh"><div class="rk-idx">04</div><div><div class="rk-name">Biến động cước giao ngay (spot rate)</div><div class="rk-desc">Chỉ 58% công suất được phủ hợp đồng dài hạn</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:58%;"></i></div><span class="rk-num">5,8</span></div></div>
    <div class="risk-row" data-sev="trung-binh"><div class="rk-idx">05</div><div><div class="rk-name">Rủi ro tỷ giá USD/VND trên nợ vay ngoại tệ</div><div class="rk-desc">68% dư nợ vay đóng tàu bằng USD, chưa phòng vệ hoàn toàn</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:51%;"></i></div><span class="rk-num">5,1</span></div></div>
    <div class="risk-row" data-sev="thap"><div class="rk-idx">06</div><div><div class="rk-name">Rủi ro lãi suất vay đóng tàu mới</div><div class="rk-desc">80% khoản vay đóng tàu mới đã chốt lãi suất cố định</div></div><div class="rk-meter"><div class="rk-bar"><i style="width:28%;"></i></div><span class="rk-num">2,8</span></div></div>
  </div>
```
