# Lưới thẻ số liệu tổng quan

`KHỐI 01 · KPI STAT GRID`

## Mô tả / khi nào dùng

Trả lời câu hỏi: "Bức tranh tổng thể trong 5-6 con số là gì?" Đầu vào: nhãn, giá trị lớn, đơn vị phụ, xu hướng có dấu, mô tả ngắn, badge nguồn. KHÔNG dùng khi chỉ có 1-2 số (dùng assertion-evidence) hoặc khi các số cần so sánh trực tiếp cạnh nhau theo hàng (dùng bảng hairline).

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="statgrid">
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Quy mô đội tàu</span></div>
      <div class="sg-value">23<small> chiếc</small></div>
      <div class="sg-foot"><span class="sg-trend up">▲ +3</span><span class="sg-sub">so với 2023</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="noi-bo"><i class="tier-dot"></i>Sổ đăng ký đội tàu, 2026-06</span></div>
    </div>
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Tổng trọng tải</span></div>
      <div class="sg-value">612.400<small> DWT</small></div>
      <div class="sg-foot"><span class="sg-trend up">▲ +9,8%</span><span class="sg-sub">theo năm</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="noi-bo"><i class="tier-dot"></i>Sổ đăng ký đội tàu, 2026-06</span></div>
    </div>
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Doanh thu 2025</span></div>
      <div class="sg-value">4.180<small> tỷ đồng</small></div>
      <div class="sg-foot"><span class="sg-trend up">▲ +12,4%</span><span class="sg-sub">svck 2024</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="cong-bo"><i class="tier-dot"></i>BCTC kiểm toán FY2025</span></div>
    </div>
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Biên EBITDA</span></div>
      <div class="sg-value">18,7<small>%</small></div>
      <div class="sg-foot"><span class="sg-trend down">▼ −2,1 đ.%</span><span class="sg-sub">áp lực nhiên liệu</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="cong-bo"><i class="tier-dot"></i>BCTC kiểm toán FY2025</span></div>
    </div>
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Nợ vay / Vốn CSH</span></div>
      <div class="sg-value">1,42<small>×</small></div>
      <div class="sg-foot"><span class="sg-trend down">▼ từ 1,58×</span><span class="sg-sub">tái cơ cấu nợ 2024</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="cong-bo"><i class="tier-dot"></i>BCTC kiểm toán FY2025</span></div>
    </div>
    <div class="sg-card">
      <div class="sg-top"><span class="sg-label">Tuổi tàu bình quân</span></div>
      <div class="sg-value">14,2<small> năm</small></div>
      <div class="sg-foot"><span class="sg-trend up">▲ già hơn TB ngành</span><span class="sg-sub">TB ngành ~11,8 năm</span></div>
      <div class="sg-foot"><span class="src-badge" data-tier="uoc-tinh"><i class="tier-dot"></i>Clarksons Research, ước tính</span></div>
    </div>
  </div>
```
