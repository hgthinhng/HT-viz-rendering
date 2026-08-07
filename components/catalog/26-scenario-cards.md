# Ba kịch bản sửa đổi Thông tư 22 về trần SFL

`KHỐI 26 · THẺ KỊCH BẢN`

## Mô tả / khi nào dùng

Trả lời: "Có mấy kịch bản chính, xác suất mỗi cái bao nhiêu, và điều gì kích hoạt nó?" Đúng 3 thẻ Tiêu cực / Cơ sở / Tích cực, mỗi thẻ có xác suất, một giá trị neo (giá mục tiêu hoặc con số kết quả), và một điều kiện kích hoạt cụ thể. Xác suất ba thẻ nên cộng đúng 100%, sai số làm tròn cho phép trong khoảng 1 điểm phần trăm. KHÔNG dùng quá 3 kịch bản mỗi khối: xác suất khó cộng đúng 100% và người đọc khó giữ hơn 3 nhánh trong đầu khi quét ngang. KHÔNG dùng khi cần cả trục xác suất lẫn trục mức độ ảnh hưởng cùng lúc trên một mặt phẳng liên tục: chuyển sang `06-quad-2x2-positioning`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="scenario-cards">
  <div class="scn-card" data-tone="bear">
    <div class="scn-head">
      <div class="scn-name">Tiêu cực</div>
      <div class="scn-prob"><span class="scn-prob-num">20</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">24.500<small>đ/cp</small></div>
    <p class="scn-headline">Phương án B thay thế được chọn: giữ nguyên trần SFL 30%, đổi bằng room NSFR riêng cho bất động sản.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Chính phủ ưu tiên kiểm soát rủi ro hệ thống hơn tăng trưởng tín dụng, quyết định trước kỳ họp Quốc hội cuối năm.</div>
  </div>
  <div class="scn-card" data-tone="base">
    <div class="scn-head">
      <div class="scn-name">Cơ sở</div>
      <div class="scn-prob"><span class="scn-prob-num">50</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">29.000<small>đ/cp</small></div>
    <p class="scn-headline">Phương án A thông qua đúng dự thảo: nâng trần SFL từ 30% lên 35%, hiệu lực đầu 2027.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Dự thảo hiện hành giữ nguyên qua vòng lấy ý kiến, không có sửa đổi lớn từ Ngân hàng Nhà nước.</div>
  </div>
  <div class="scn-card" data-tone="bull">
    <div class="scn-head">
      <div class="scn-name">Tích cực</div>
      <div class="scn-prob"><span class="scn-prob-num">30</span><span class="scn-prob-unit">%</span></div>
    </div>
    <div class="scn-value">34.000<small>đ/cp</small></div>
    <p class="scn-headline">Phương án A thông qua kèm gói nới lỏng tiền tệ, lãi suất điều hành giảm thêm 50 điểm cơ bản.</p>
    <div class="scn-trigger"><span class="scn-trigger-label">Kích hoạt khi</span>Lạm phát duy trì dưới 3,5% cho phép nới đồng thời cả room tín dụng lẫn lãi suất.</div>
  </div>
</div>
```
