---
title: "Soft Commodities — Nông sản Xuất khẩu Việt Nam: Gạo, Cà phê, Cao su, Điều"
module_type: "domain"
file_name: "domain-commodities-soft.md"
purpose: "Phân tích chuyên sâu về 4 nhóm nông sản xuất khẩu cốt lõi của Việt Nam: gạo (ĐBSCL), cà phê (Tây Nguyên), cao su, điều. Tập trung vào chu kỳ thu hoạch (seasonality), rủi ro thờii tiết (El Niño/La Niña), cơ chế định giá FOB/CIF, và đóng góp vào thu ngân sách / kim ngạch xuất khẩu."
primary_triggers:
  - "nông sản xuất khẩu Việt Nam"
  - "giá gạo thế giới"
  - "giá cà phê arabica robusta"
  - "mùa vụ thu hoạch cà phê"
  - "El Niño ảnh hưởng nông sản"
  - "FOB CIF gạo"
  - "xuất khẩu cao su điều"
  - "seasonality nông sản"
when_to_use:
  - "Khi phân tích kim ngạch xuất khẩu nông sản VN và rủi ro biến động giá."
  - "Khi đánh giá tác động của El Niño/La Niña lên sản lượng và giá nội địa."
  - "Khi cần hiểu chu kỳ thu hoạch để dự báo áp lực giá hoặc thu ngân sách theo quý."
  - "Khi phân tích margin của doanh nghiệp xuất khẩu nông sản (VNM, TNG, HAG, etc.)."
when_not_to_use:
  - "Không dùng để dự báo giá nông sản cụ thể (spot price prediction) — chỉ cung cấp structural lens."
  - "Không dùng cho phân tích nông sản nhập khẩu (ngô, đậu tương, lúa mì) — thuộc domain khác."
  - "Không thay thế dữ liệu thờii tiết real-time từ NCHMF."
related_modules:
  - "domain-commodities-vn-impact.md"
  - "domain-commodities-futures-curve.md"
  - "macro-vn-transmission-channels.md"
  - "reference-vn-data-sources.md"
  - "domain-cross-asset-correlation-regimes.md"
authoritative_citations:
  - "Bộ NN&PTNT — Cục Trồng trọt, Cục Chế biến và Phát triển thị trường nông sản."
  - "Tổng cục Hải quan — Trade statistics theo HS code (gạo 1006, cà phê 0901, cao su 4001, điều 0801)."
  - "GSO — CPI food component, PPI agriculture."
  - "ICO (International Coffee Organization), FAO, USDA World Agricultural Supply and Demand Estimates (WASDE)."
  - "NOAA Climate Prediction Center — ENSO status."
  - "Vietnam Food Association (VFA), Vietnam Coffee-Cocoa Association (Vicofa)."
output_owner: "workflow-deep-dive.md khi phân tích sector nông sản hoặc xuất khẩu VN; workflow-daily-brief.md khi có biến động giá nông sản đáng kể."
---

# Soft Commodities — Nông sản Xuất khẩu Việt Nam

**Mục đích:** Codify cơ cấu, chu kỳ, và rủi ro của 4 nhóm nông sản xuất khẩu chủ lực. Nông sản chiếm ~12–15% tổng kim ngạch xuất khẩu VN (2024) và là biến số quan trọng cho CPI food component (~40% basket), thu nhập nông thôn, và thu ngân sách địa phương.

**Trạng thái:** [STRUCTURAL — Cập nhật số liệu theo mùa vụ]

---

## 1. TỔNG QUAN: 4 TRỤ CỘT XUẤT KHẨU NÔNG SẢN

### 1.1. Đóng góp kim ngạch (ước tính 2024–2025)

| Mặt hàng | Kim ngạch XK (~USD tỷ/năm) | Thị phần global | Vùng sản xuất chính | Độ tập trung xuất khẩu |
|:---|:---:|:---:|:---|:---|
| **Gạo** | 4.5–5.0 | #3 (sau Ấn Độ, Thái Lan) | ĐBSCL (Long An, An Giang, Đồng Tháp, Kiên Giang) | Cao — top 5 doanh nghiệp chiếm ~40% |
| **Cà phê** | 4.0–5.0 | #2 robusta (sau Brazil) | Tây Nguyên (Đắk Lắk, Lâm Đồng, Gia Lai, Đắk Nông) | Trung bình — ~150 doanh nghiệp rang xay |
| **Cao su** | 2.5–3.0 | #3 (sau Thái Lan, Indonesia) | Đông Nam Bộ, Tây Nguyên (Bình Phước, Đồng Nai) | Thấp — nhiều nông hộ nhỏ |
| **Điều** | 3.0–3.5 | #1 (chiếm ~80% thế giới) | Đông Nam Bộ, Tây Nguyên (Bình Phước, Đồng Nai) | Cao — top 10 doanh nghiệp chiếm ~60% |

> **DIỄN GIẢI:** Tổng 4 mặt hàng ~14–17 tỷ USD/năm, tương đương 8–10% tổng kim ngạch xuất khẩu VN. Biến động giá 10% trên 4 mặt hàng này = ±1.4–1.7 tỷ USD kim ngạch, tác động trực tiếp lên cán cân thương mại và dự trữ ngoại hối.

---

## 2. GẠO — ĐBSCL VÀ CƠ CHẾ GIÁ

### 2.1. Cơ cấu vụ mùa và seasonality

| Vụ | Thờii gian thu hoạch | Sản lượng (triệu tấn) | Đặc điểm chất lượng | Áp lực giá |
|:---|:---|:---:|:---|:---|
| **Đông Xuân** | Tháng 1–3 | ~10–11 | Chất lượng cao nhất, hạt dài, độ ẩm thấp | Xuống thấp do cung dồi dào |
| **Hè Thu** | Tháng 5–8 | ~8–9 | Chất lượng trung bình | Trung bình |
| **Thu Đông** | Tháng 9–12 | ~6–7 | Chất lượng thấp nhất, ảnh hưởng mưa bão | Có thể tăng nếu thiệt hại |

> **SỰ KIỆN:** VN xuất khẩu ~7.5–8 triệu tấn gạo/năm (2023–2024), tăng từ mức 6 triệu tấn trung bình giai đoạn 2018–2022 nhờ nới lỏng hạn ngạch và tăng năng suất giống lúa mới.

### 2.2. FOB vs CIF — Cơ chế định giá

| Điều khoản | Ai chịu chi phí vận chuyển | Ai chịu rủi ro | Phổ biến với | Impact margin |
|:---|:---|:---|:---|:---|
| **FOB** (Free On Board) | Ngưới mua (importer) | Chuyển giao tại cảng xuất khẩu (Cát Lái, Cái Mép) | Giao dịch bulk với Philippines, Indonesia, châu Phi | Xuất khẩu VN nhận giá FOB thấp hơn CIF ~8–12% nhưng không chịu freight risk |
| **CIF** (Cost, Insurance, Freight) | Ngưới bán (exporter VN) | Chuyển giao tại cảng đích | Giao dịch với Trung Đông, châu Âu (yêu cầu logistics door-to-door) | Margin bị squeeze khi freight tăng; cần hedge freight hoặc điều chỉnh giá theo BDI/SCFI |

> **DIỄN GIẢI:** Phần lớn gạo VN xuất theo FOB. Khi container rates tăng (như 2021–2022), buyer chịu phần lớn áp lực → demand không giảm mạnh. Ngược lại, nếu VN bán CIF, margin xuất khẩu sẽ biến động theo freight cycle.

---

## 3. CÀ PHÊ TÂY NGUYÊN — ARABICA VS ROBUSTA

### 3.1. Cơ cấu giống và vùng trồng

| Chỉ tiêu | Arabica | Robusta | Ghi chú |
|:---|:---|:---|:---|
| **Tỷ lệ diện tích VN** | ~5–7% | ~93–95% | VN là nước sản xuất robusta lớn nhất thế giới |
| **Vùng trồng chính** | Lâm Đồng (cao nguyên Di Linh, Bảo Lộc) | Đắk Lắk, Gia Lai, Đắk Nông | Arabica cần độ cao >1,000m, nhiệt độ thấp hơn |
| **Giá benchmark** | ICE Arabica (cents/lb, NY) | ICE Robusta (USD/tấn, London) | Robusta VN thường discount nhẹ so với London do chất lượng biến động |
| **Premium/Discount** | Premium so với robusta ~50–100% | Baseline | Spread Arabica-Robusta là tín hiệu substitution demand |
| **Đối tượng mua chính** | Specialty roasters (EU, Mỹ, Nhật) | Instant coffee, espresso blend (EU, Nga, Đông Nam Á) | Nestlé, JDE Peet’s, Kraft Heinz là buyer lớn |

### 3.2. Chu kỳ thu hoạch và seasonality giá

| Giai đoạn | Tháng | Diễn biến giá nội địa | Diễn biến giá thế giới |
|:---|:---|:---|:---|
| **Thu hoạch chính** | Tháng 10–Tháng 3 | Cung tăng → giá nội địa giảm 10–20% so với off-season | London/NY có thể giảm nếu dự báo vụ mùa tốt |
| **Off-season** | Tháng 4–Tháng 9 | Cung giảm → giá tăng, nông dân bán dự trữ | Giá thế giới thường tăng nếu Brazil/Colombia có vấn đề |
| **Peak rủi ro thờii tiết** | Tháng 1–Tháng 3 (nở hoa) | Nếu mưa lớn/sương muối → mất mùa → giá nội địa tăng mạnh | Không correlate hoàn toàn — London phản ứng chậm hơn 2–4 tuần |

> **SỰ KIỆN:** Vụ thu hoạch cà phê VN 2023–2024 bị giảm sản lượng ~15–20% do hạn hán kéo dài ở Tây Nguyên (El Niño), đẩy giá nội địa lên mức cao nhất 10 năm. Tuy nhiên, giá London tăng ít hơn do Brazil bù đắp cung robusta.

---

## 4. CAO SU & ĐIỀU — CHU KỲ VÀ CƠ CHẾ

### 4.1. Cao su — Tính chu kỳ và tồn kho Trung Quốc

| Chỉ tiêu | Chi tiết |
|:---|:---|
| **Mùa cạo mủ** | Tháng 5–Tháng 11 (mùa mưa cạo được nhiều nhất) |
| **Mùa đông ngừng cạo** | Tháng 12–Tháng 4 — cây nghỉ, sản lượng giảm 30–40% |
| **Benchmark giá** | SICOM (Singapore), TOCOM (Tokyo), SHFE (Thượng Hải) |
| **Driver chính** | Tồn kho cao su Trung Quốc (SRB — State Reserve Bureau), nhu cầu lốp xe từ ngành ô tô |
| **Đặc thù VN** | ~70% cao su VN xuất khẩu dạng SVR (Standard Vietnamese Rubber), không phải RSS (dùng cho lốp cao cấp) → giá discount so với RSS3 |

> **DIỄN GIẢI:** Cao su VN bị ảnh hưởng mạnh bởi chu kỳ ô tô Trung Quốc và chính sách tồn kho Nhà nước TQ. Khi TQ tăng mua SRB, giá cao su tăng; khi TQ xả kho, giá giảm bất chấp nhu cầu thực.

### 4.2. Điều — Độc quyền và rủi ro chuỗi cung ứng

| Chỉ tiêu | Chi tiết |
|:---|:---|
| **Mùa thu hoạch** | Tháng 2–Tháng 5 (chính vụ), Tháng 8–Tháng 10 (vụ phụ) |
| **Vị thế VN** | #1 toàn cầu, nhưng ~90% xuất khẩu là hạt điều nhân chưa chế biến sâu |
| **Rủi ro chuỗi cung ứng** | Phụ thuộc nguyên liệu thô từ Tây Phi (Bờ Biển Ngà, Ghana, Nigeria) ~30–40% tổng nguyên liệu |
| **Margin squeeze** | Khi giá nguyên liệu Tây Phi tăng + freight tăng → margin chế biến VN giảm; ngược lại, nếu VN thu mua được giá thấp + giá xuất khẩu cao → margin bùng nổ |

> **GIẢ THUYẾT:** Nếu các nước Tây Phi tăng chế biến nội địa (như chính sách của Bờ Biển Ngà 2023–2025), nguồn cung nguyên liệu thô cho VN có thể giảm 20–30% trong 5 năm, buộc VN phải: (a) tăng diện tích trồng điều nội địa, hoặc (b) chuyển sang chế biến sâu (điều lụa, snack) để giữ margin.

---

## 5. RỦI RO THỜII TIẾT — EL NIÑO / LA NIÑA

### 5.1. ENSO Impact Matrix cho nông sản VN

| ENSO Phase | Xác suất ảnh hưởng VN | Tác động Gạo (ĐBSCL) | Tác động Cà phê (Tây Nguyên) | Tác động Cao su | Tác động Điều |
|:---|:---:|:---|:---|:---|:---|
| **El Niño** | Cao | Hạn hán mùa khô (tháng 12–4), xâm nhập mặn sâu → giảm sản lượng Đông Xuân | Hạn hán, thiếu nước tưới → giảm năng suất cây non | Mùa khô kéo dài → cạo mủ được lâu hơn, nhưng cây stress nếu kéo dài >6 tháng | Giảm năng suất nếu hạn kéo dài quá tháng 3 |
| **La Niña** | Cao | Mưa lớn, lũ lụt ĐBSCL → thiệt hại Hè Thu và Thu Đông | Mưa nhiều → rủi ro nấm bệnh, nhưng nước tưới dồi dào | Mưa lớn → khó cạo mủ, sản lượng giảm | Mưa lớn thu hoạch khó khăn, hạt nứt |
| **Trung tính (Neutral)** | Baseline | Bình thường | Bình thường | Bình thường | Bình thường |

### 5.2. Lịch sử tác động

| Sự kiện | Năm | ENSO | Tác động |
|:---|:---:|:---:|:---|
| **Hạn hán ĐBSCL nghiêm trọng** | 2016 | El Niño mạnh | Xâm nhập mặn sâu 80–100km, mất 300,000 ha lúa, giá gạo nội địa tăng 20% |
| **Lũ lụt miền Trung/Tây Nguyên** | 2020 | La Niña | Mưa lũ lịch sử, thiệt hại cà phê ~10% sản lượng vùng trũng |
| **Hạn hán Tây Nguyên** | 2023–2024 | El Niño | Sản lượng cà phê giảm 15–20%, giá nội địa tăng 40% so với trung bình 5 năm |

> **DIỄN GIẢI:** ENSO là biến số cấu trúc (structural) chứ không phải nhiễu ngắn hạn. Một đợt El Niño mạnh có thể làm giảm tổng sản lượng nông sản VN 5–10%, tương đương thiệt hại 2–3 tỷ USD kim ngạch xuất khẩu và đẩy CPI food lên 1.5–2.5 điểm %.

---

## 6. FOB VS CIF — CƠ CHẾ VÀ RỦI RO

### 6.1. So sánh chi tiết cho nông sản VN

| Dimension | FOB (Phổ biến 70–80%) | CIF (Phổ biến 20–30%) |
|:---|:---|:---|
| **Giá nhận được** | Thấp hơn CIF ~8–12% | Cao hơn FOB, bao gồm freight + insurance |
| **Rủi ro logistics** | Ngưới mua chịu | Ngưới bán chịu |
| **Yêu cầu vốn lưu động** | Thấp — không cần trả trước freight | Cao — cần vốn để trả freight trước khi nhận tiền |
| **Yêu cầu năng lực** | Thấp — chỉ cần đưa hàng ra cảng | Cao — cần đối tác logistics quốc tế, khả năng hedge freight |
| **Phù hợp với** | Doanh nghiệp vừa và nhỏ, giao dịch châu Á ngắn | Doanh nghiệp lớn (Vinh Thanh Dat, Intimex, TNG), giao dịch châu Âu/Trung Đông |
| **Nhạy cảm với freight** | Không | Rất nhạy — freight tăng 50% có thể xóa sạch margin |

> **SỰ KIỆN:** Trong đợt freight tăng 2021–2022 (container rates tăng 5–10x), các doanh nghiệp xuất khẩu điều bán CIF chịu margin squeeze nghiêm trọng, trong khi các doanh nghiệp bán FOB (chủ yếu gạo) hưởng lợi từ việc buyer chịu phần lớn chi phí vận chuyển.

---

## 7. CROSS-REFS VÀ TRIGGER WORKFLOW

| Khi ngưới dùng hỏi... | Load module... | Output contract |
|:---|:---|:---|
| "Giá cà phê tăng ảnh hưởng CPI VN không?" | `domain-commodities-vn-impact.md` + module này | Linkage Analysis |
| "Futures cà phê đang contango hay backwardation?" | `domain-commodities-futures-curve.md` + module này | Deep-dive Memo |
| "El Niño 2024 ảnh hưởng gì đến xuất khẩu VN?" | Module này + `macro-vn-transmission-channels.md` | Daily Brief / Linkage |
| "Margin doanh nghiệp điều 2025 thế nào?" | Module này + `domain-equity-vn-industry-guides.md` | Deep-dive Memo |

---

*Module version: 0.1.0 | Shelf life: 6 tháng (cập nhật theo mùa vụ).*
*Cross-check với: USDA WASDE (tháng), ICO monthly report, NOAA ENSO diagnostic (hàng tuần).*
