# Badge nguồn chuẩn hóa cho mọi số liệu

`KHỐI 20 · CHÚ GIẢI NGUỒN (K-ANCHOR BADGE)`

## Mô tả / khi nào dùng

Đây là component NỀN TẢNG mà mọi khối có số liệu khác (statgrid, bảng, note-box…) đều gọi lại; mỗi số liệu phải khai báo được {value, source, date, tier}. Bốn tier theo màu, phỏng theo quy tắc "4 nguồn" của bản Kimi tham chiếu nhưng đổi tên tiếng Việt: CÔNG BỐ (BCTC, văn bản pháp luật), ƯỚC TÍNH (bên thứ ba như Clarksons/VIMC), DỰ BÁO (mô hình nội bộ), NỘI BỘ (báo cáo vận hành chưa kiểm toán). KHÔNG dùng tier "công bố" cho số liệu chưa có văn bản/BCTC xác nhận. Cũng KHÔNG tự đặt tier ngoài đúng 4 giá trị `data-tier` mà `.src-badge` định nghĩa màu (cong-bo, uoc-tinh, du-bao, noi-bo): thêm hoặc gõ sai một giá trị khác sẽ khiến badge rơi về không màu, không có cảnh báo gì.

## HTML mẫu (copy trực tiếp từ gallery.html, chạy được ngay với components.css)

```html
<div style="display:flex; flex-wrap:wrap; gap:10px;">
    <span class="src-badge" data-tier="cong-bo"><i class="tier-dot"></i>CÔNG BỐ · BCTC kiểm toán FY2025 · 2026-03-28</span>
    <span class="src-badge" data-tier="uoc-tinh"><i class="tier-dot"></i>ƯỚC TÍNH · Clarksons Research · 2026-05</span>
    <span class="src-badge" data-tier="du-bao"><i class="tier-dot"></i>DỰ BÁO · Mô hình nội bộ v3.2 · 2026-06</span>
    <span class="src-badge" data-tier="noi-bo"><i class="tier-dot"></i>NỘI BỘ · Báo cáo vận hành · 2026-06-30</span>
  </div>
  <p style="font-size:12.5px; color:var(--ink-lo); margin-top:14px; max-width:60ch;">Mã dùng: <code class="mono">&lt;span class="src-badge" data-tier="cong-bo"&gt;&lt;i class="tier-dot"&gt;&lt;/i&gt;nhãn&lt;/span&gt;</code>. Giá trị <code class="mono">data-tier</code> nhận 1 trong 4: <code class="mono">cong-bo</code>, <code class="mono">uoc-tinh</code>, <code class="mono">du-bao</code>, <code class="mono">noi-bo</code>.</p>
```
