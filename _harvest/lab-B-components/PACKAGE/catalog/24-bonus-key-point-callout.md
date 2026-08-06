# Một câu kết luận, không khung hộp nặng

`KHỐI PHỤ 2 · ĐIỂM MẤU CHỐT (KEY-POINT CALLOUT)`

## Mô tả / khi nào dùng

Kỹ thuật vay mượn từ render_engine.py (pipeline CFA Notes dạng DOCX), tái tô màu theo bộ token chốt (gold/copper của reference-kimi.html) thay vì indigo gốc. Trả lời: "Nếu người đọc chỉ nhớ một câu của mục này, câu đó là gì?" Không tính vào 22 component chính, xem lý giải nguồn và ranh giới với assertion-evidence trong CSS.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div class="key-point">
    <div class="kp-rule top"></div>
    <div class="kp-label">Điểm mấu chốt</div>
    <p class="kp-text">Đội tàu đang lãi ở cấp vận hành nhưng lỗ ở cấp chu kỳ nhiên liệu. <b>Khóa giá nhiên liệu 2 quý tới quan trọng hơn</b> mọi quyết định đầu tư tàu mới trong ngắn hạn.</p>
    <div class="kp-rule bottom"></div>
  </div>
```
