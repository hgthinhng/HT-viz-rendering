# Thang ràng buộc pháp lý & kỹ thuật, xếp theo độ cứng

`KHỐI 02 · GATE LADDER`

## Mô tả / khi nào dùng

Trả lời: "Ràng buộc nào doanh nghiệp không thể đàm phán, ràng buộc nào có đường vòng?" Đầu vào: tên ràng buộc, cơ sở pháp lý, điểm cứng /10, có đường vòng hay không, mô tả đường vòng. KHÔNG dùng khi chỉ có 1-2 ràng buộc (dùng note-box cảnh báo) hoặc khi ràng buộc không thể xếp hạng độ cứng khách quan.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="gate-ladder">
    <div class="gate-row">
      <div class="gate-idx">01</div>
      <div class="gate-sq solid" aria-hidden="true"></div>
      <div><div class="gate-name">MARPOL Annex&nbsp;VI · trần lưu huỳnh 0,5%</div><div class="gate-basis">IMO 2020 · Reg. 14</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 10 trên 10">
        <span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span>
        <span class="gate-num">10/10</span>
      </div>
      <div class="gate-bypass none">KHÔNG CÓ ĐƯỜNG VÒNG</div>
    </div>
    <div class="gate-row">
      <div class="gate-idx">02</div>
      <div class="gate-sq" aria-hidden="true"></div>
      <div><div class="gate-name">IMO CII · chỉ số cường độ carbon</div><div class="gate-basis">MEPC.352(78), hiệu lực 2023</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 8 trên 10">
        <span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell"></span><span class="gate-cell"></span>
        <span class="gate-num">8/10</span>
      </div>
      <div class="gate-bypass">Mua tín chỉ carbon bù trừ hạng D/E liên tiếp</div>
    </div>
    <div class="gate-row">
      <div class="gate-idx">03</div>
      <div class="gate-sq" aria-hidden="true"></div>
      <div><div class="gate-name">Đăng kiểm tàu biển định kỳ</div><div class="gate-basis">Nghị định 171/2024/NĐ-CP</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 6 trên 10">
        <span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span>
        <span class="gate-num">6/10</span>
      </div>
      <div class="gate-bypass">Đăng kiểm nước ngoài (RINA/ClassNK) song song</div>
    </div>
    <div class="gate-row">
      <div class="gate-idx">04</div>
      <div class="gate-sq" aria-hidden="true"></div>
      <div><div class="gate-name">Quy định treo cờ &amp; thuế thuyền viên</div><div class="gate-basis">Luật Hàng hải VN 2015, sửa đổi</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 5 trên 10">
        <span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span>
        <span class="gate-num">5/10</span>
      </div>
      <div class="gate-bypass">Treo cờ mở (Panama/Marshall) cho tàu tuyến quốc tế</div>
    </div>
    <div class="gate-row">
      <div class="gate-idx">05</div>
      <div class="gate-sq solid" aria-hidden="true"></div>
      <div><div class="gate-name">SOLAS · an toàn sinh mạng trên biển</div><div class="gate-basis">Công ước SOLAS 1974, sửa đổi 2020</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 9 trên 10">
        <span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell on hot"></span><span class="gate-cell"></span>
        <span class="gate-num">9/10</span>
      </div>
      <div class="gate-bypass none">KHÔNG CÓ ĐƯỜNG VÒNG</div>
    </div>
    <div class="gate-row">
      <div class="gate-idx">06</div>
      <div class="gate-sq" aria-hidden="true"></div>
      <div><div class="gate-name">Phí neo đậu &amp; hoa tiêu cảng địa phương</div><div class="gate-basis">Biểu phí cảng vụ hàng hải, theo năm</div></div>
      <div class="gate-score" role="img" aria-label="Điểm cứng 3 trên 10">
        <span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell on"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span><span class="gate-cell"></span>
        <span class="gate-num">3/10</span>
      </div>
      <div class="gate-bypass">Đàm phán hợp đồng khung nhiều chuyến, chọn cảng cạnh tranh phí</div>
    </div>
  </div>
  <p class="gate-legend">Ô RỖNG = CÓ ĐƯỜNG VÒNG · Ô ĐẶC BÊN TRÁI = RÀNG BUỘC TUYỆT ĐỐI · Ô ĐỎ TRONG THANG ĐIỂM = VÙNG KHÓ ĐÀM PHÁN (≥8/10)</p>
```
