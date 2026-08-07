# Hai kịch bản sửa đổi Thông tư 22, một điểm rẽ

`KHỐI 28 · NGÃ BA CHÍNH SÁCH`

## Mô tả / khi nào dùng

Trả lời: "Chính sách này có mấy khả năng, và mỗi khả năng kéo theo hệ quả gì?" Một điểm rẽ chung ở trên, đúng hai nhánh loại trừ nhau ở dưới, mỗi nhánh có điều kiện rẽ (NẾU...) và một đoạn hệ quả. KHÔNG dùng khi có hơn 2 nhánh rẽ: chuyển sang `26-scenario-cards`, khối kịch bản xử lý được từ 3 nhánh trở lên kèm xác suất. KHÔNG dùng cho một chuỗi bước tuần tự không có điểm rẽ thật: dùng `16-process-step-chain`.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="policy-fork">
  <div class="pf-root">
    <div class="pf-root-label">Điểm rẽ</div>
    <div class="pf-root-text">Ngân hàng Nhà nước đang lấy ý kiến sửa đổi Thông tư 22/2023 về tỷ lệ SFL, dự kiến ban hành Quý 4/2026.</div>
  </div>
  <div class="pf-branches">
    <div class="pf-branch" data-branch="a">
      <div class="pf-branch-label">Nhánh A</div>
      <div class="pf-cond"><span class="pf-cond-tag">NẾU</span>Phương án A được thông qua nguyên trạng: nâng trần SFL từ 30% lên 35%</div>
      <div class="pf-outcome">
        <div class="pf-outcome-label">Hệ quả</div>
        <p>Nhóm ngân hàng tư nhân tầm trung có thêm khoảng 45.000 tỷ đồng dư địa cho vay trung dài hạn toàn ngành, tăng trưởng tín dụng quý đầu hiệu lực có thể vượt kế hoạch được giao 1 đến 2 điểm phần trăm.</p>
      </div>
    </div>
    <div class="pf-branch" data-branch="b">
      <div class="pf-branch-label">Nhánh B</div>
      <div class="pf-cond"><span class="pf-cond-tag">NẾU</span>Phương án B thay thế được chọn: giữ nguyên trần SFL, đổi bằng room NSFR riêng cho bất động sản</div>
      <div class="pf-outcome">
        <div class="pf-outcome-label">Hệ quả</div>
        <p>Ngân hàng có tỷ trọng CASA thấp chịu áp lực huy động vốn dài hạn tăng, chi phí vốn bình quân toàn ngành nhích thêm 15 đến 20 điểm cơ bản trong hai quý đầu áp dụng.</p>
      </div>
    </div>
  </div>
</div>
```
