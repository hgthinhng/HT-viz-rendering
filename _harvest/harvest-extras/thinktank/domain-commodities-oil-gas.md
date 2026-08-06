---
title: "Domain Commodities Oil Gas — Oil Market Structure, WTI Brent Spread, OPEC Dynamics, Geopolitical Premium, Iran-US War 2025-2026, Strait of Hormuz Risk, Vietnam CPI Passthrough"
module_type: "domain"
file_name: "domain-commodities-oil-gas.md"
purpose: "Phân tích cấu trúc thị trường dầu mỏ toàn cầu, động lực OPEC+, rủi ro địa chính trị cấp chiến tranh (Iran-US, eo biển Hormuz), và kênh truyền dẫn vào kinh tế Việt Nam qua CPI, ngành dầu khí niêm yết (PVS, PVD, GAS), và chi phí vận tải biển."
primary_triggers:
  - "phân tích dầu thô"
  - "giá dầu Brent WTI"
  - "OPEC production cut"
  - "Iran US war oil"
  - "Strait of Hormuz risk"
  - "dầu khí Việt Nam"
  - "CPI passthrough dầu"
  - "PVS PVD GAS"
  - "shipping freight oil"
when_to_use:
  - "Khi phân tích giá dầu thô, spread Brent-WTI, hoặc động lực cung-cầu toàn cầu."
  - "Khi đánh giá rủi ro địa chính trị khu vực Trung Đông và tác động đến giá dầu, bảo hiểm vận tải, freight cost."
  - "Khi phân tích ngành dầu khí Việt Nam (upstream, downstream, dịch vụ) và tác động của giá dầu đến lạm phát VN."
when_not_to_use:
  - "Không dùng để dự báo giá dầu cụ thể tại thờii điểm X — chỉ dùng cho scenario bounds và regime classification."
  - "Không dùng để khuyến nghị mua/bán cổ phiếu dầu khí cụ thể — cần kết hợp với domain-equity-vn-industry-guides.md và workflow-deep-dive.md."
related_modules:
  - "framework-regime-v11.md"
  - "workflow-cross-asset-linkage.md"
  - "domain-equity-vn-industry-guides.md"
  - "domain-commodities-commodity-vn-impact.md"
  - "reference-vn-data-sources.md"
authoritative_citations:
  - "EIA Short-Term Energy Outlook (monthly)."
  - "OPEC Monthly Oil Market Report (MOMR)."
  - "IEA Oil Market Report (monthly)."
  - "ClipperData / Vortexa tanker tracking."
  - "GSO Vietnam CPI reports; MOF fuel price stabilization fund data."
output_owner: "workflow-deep-dive.md khi phân tích sâu dầu khí; workflow-daily-brief.md khi cập nhật giá dầu overnight; workflow-cross-asset-linkage.md khi phân tích transmission từ oil sang CPI VN hoặc equity VN."
---

# Domain Commodities Oil Gas — Cấu trúc Thị trường Dầu mỏ / Địa chính trị / Tác động Việt Nam

Purpose: Cung cấp lens phân tích thị trường dầu mỏ toàn cầu và kênh truyền dẫn vào Việt Nam. Bao gồm: cấu trúc giá (WTI vs Brent), động lực OPEC+, rủi ro địa chính trị cấp chiến tranh (Iran-US 2025-2026, Hormuz), freight/shipping premium, và passthrough vào CPI + ngành dầu khí niêm yết VN (PVS, PVD, GAS). Triggers: giá dầu, Brent, WTI, OPEC, Hormuz, Iran, dầu khí VN, CPI xăng dầu.

---

## 1. Cấu trúc Thị trường Dầu thô: WTI vs Brent vs Dubai/Oman

### 1.1. Đặc điểm từng benchmark
| Benchmark | Địa lý | API / Sulfur | Đối tượng sử dụng chính |
|---|---|---|---|
| **WTI** | Cushing, Oklahoma (US inland) | Light sweet (~39.6°API, 0.24% S) | US domestic pricing, WTI-linked contracts |
| **Brent** | North Sea (UK/Norway offshore) | Light sweet (~38°API, 0.37% S) | Global pricing, ~80% thế giới |
| **Dubai/Oman** | UAE/Oman | Medium sour (~31°API, ~2% S) | Châu Á, đặc biệt VN nhập khẩu chủ yếu |

**[SỰ KIỆN]** Từ 2020-2026, WTI từng rơi vào vùng âm (tháng 4/2020, -USD 37/thùng) do Cushing đầy bể và thiếu khả năng xuất khẩu. Brent không bao giờ âm vì là waterborne và dễ vận chuyển hơn.

### 1.2. Brent-WTI Spread — Ý nghĩa phân tích
Spread Brent-WTI phản ánh:
- **Cung US (Permian shale):** Khi US xuất khẩu crude tăng (lift of export ban 2015 + infrastructure buildout 2018-2023), spread thu hẹp.
- **Logistics constraint:** Cushing bottleneck → spread widen.
- **Quality differential:** Nhu cầu sour crude từ châu Á tăng → Dubai premium, Brent-WTI decouple khỏi historical range.

| Giai đoạn | Brent-WTI spread trung bình | Driver chính |
|---|---|---|
| 2020 | USD 2-4 | Cung US dồi dào, demand sụt COVID |
| 2021-2022 | USD 1-3 | Shale phục hồi chậm, US SPR release |
| 2023 | USD 4-6 | EU embargo Nga + price cap, redirect Urals |
| 2024-2025 | USD 3-5 | OPEC+ hold back supply, US production plateau |
| 2026 (YTD) | USD 4-7 | Iran tension + Hormuz risk premium |

**[DIỄN GIẢI]** Spread > USD 5 thường báo hiệu rủi ro logistics hoặc khan hiếm sour crude ở châu Á. VN nhập Dubai/Oman nên theo dõi Brent-Dubai spread chặt hơn WTI.

---

## 2. OPEC+ Dynamics: Cơ chế Cung và Spare Capacity

### 2.1. OPEC+ production framework
OPEC+ (OPEC 13 thành viên + 10 đồng minh led by Nga) kiểm soát ~40% sản lượng dầu toàn cầu và ~85% spare capacity có thể khai thác trong 30 ngày.

**[SỰ KIỆN]** Các đợt cắt giảm sản lượng chính 2022-2026:
- Tháng 10/2022: -2 triệu thùng/ngày (mbd)
- Tháng 4/2023: -1.66 mbd (chủ yếu voluntary cut từ Saudi, Nga, Iraq)
- Tháng 11/2023: -2.2 mbd extended đến Q2/2024
- Tháng 6/2024: Một số nước (Saudi, Nga, UAE) voluntary cut extended
- 2025-2026: Saudi duy trì ~9 mbd (dưới capacity ~12 mbd); Nga sản lượng ~9.1 mbd bất chấp sanctions

### 2.2. Spare capacity — biến số then chốt
| Quốc gia | Capacity thực tế | Sản lượng hiện tại | Spare capacity ước tính |
|---|---|---|---|
| Saudi Arabia | ~12.0 mbd | ~9.0 mbd | ~3.0 mbd |
| UAE | ~4.2 mbd | ~3.0 mbd | ~1.2 mbd |
| Iraq | ~4.8 mbd | ~4.2 mbd | ~0.6 mbd |
| Kuwait | ~2.8 mbd | ~2.5 mbd | ~0.3 mbd |
| **Tổng OPEC core** | | | **~5.0 mbd** |

**[DIỄN GIẢI]** Spare capacity ~5 mbd là tuyến phòng thủ cuối cùng chống supply shock. Nếu Hormuz bị đóng hoặc Iran output (~3.2 mbd) bị loại hoàn toàn, spare capacity có thể bù đắp nhưng để lại hệ thống không có buffer — tương tự khủng hoảng 1973/1979.

### 2.3. Compliance và "cheating"
[GIẢ THUYẾT] OPEC+ compliance thường < 100% trong giai đoạn giá cao. Iraq, UAE thường vượt quota. Nga báo cáo sản lượng thấp hơn thực tế do shadow fleet vận chuyển. Đây là yếu tố làm giảm hiệu quả của production cut trên paper.

---

## 3. Geopolitical Premium: Chiến tranh Iran-US 2025-2026 & Eo biển Hormuz

### 3.1. Bối cảnh chiến tranh Iran-US
**[SỰ KIỆN]** Từ cuối 2025, xung đột quân sự giữa Iran và Mỹ + đồng minh leo thang. Các mốc:
- Tấn công cơ sở hạt nhân / quân sự Iran bằng không kích và tên lửa hành trình.
- Iran đáp trả bằng tên lửa đạn đạo nhắm vào căn cứ Mỹ ở Iraq, Syria, và tàu chiến ở vịnh Ba Tư.
- Hezbollah / Houthis mở rộng tấn công shipping ở Biển Đỏ và eo biển Hormuz.

### 3.2. Strait of Hormuz — chokepoint then chốt
- **20% sản lượng dầu toàn cầu** (~21 triệu thùng/ngày) qua Hormuz.
- **LNG từ Qatar** (~30% LNG toàn cầu) cũng qua Hormuz.
- **Width:** Chỉ ~21 hải lý (đường đi thực tế ~2 hải lý mỗi chiều).

| Scenario | Xác suất định tính | Tác động giá dầu ước tính | Thờii gian duy trì |
|---|---|---|---|
| Tấn công rải rác vào tàu chở dầu (Houstyle) | Medium | +USD 10-20 | 2-4 tuần |
| Iran phong tỏa một phần Hormuz | Low-Medium | +USD 30-50 | 1-3 tháng |
| Phong tỏa toàn bộ + US/Iran leo thang toàn diện | Low | +USD 50-100+ | 3-12 tháng |
| Tấn công cơ sở sản xuất Saudi (Abqaiq-style) | Low | +USD 20-40 | 1-6 tháng |

**[DIỄN GIẢI]** Geopolitical premium được pricing vào futures curve qua:
1. **Backwardation sâu:** Giá near-month cao hơn far-month do lo ngại khan hiếm ngắn hạn.
2. **Options skew:** Call option (mua) ở strike cao đắt hơn put (bán) đáng kể — implied vol asymmetry.
3. **Bảo hiểm vận tải (war risk insurance):** Tăng 5-10x qua Hormuz. Có thể đẩy chi phí vận chuyển từ USD 2-3/thùng lên USD 10-15/thùng.

### 3.3. Petrodollar fragmentation risk
[GIẢ THUYẾT] Nếu Saudi/UAE bắt đầu chấp nhận thanh toán dầu bằng CNY hoặc BRICS currency, demand USD reserve giảm → DXY biến động không theo pattern cũ. VND neo vào USD basket cũng chịu ảnh hưởng gián tiếp. Xem thêm trong framework-regime-v11.md về FX regime shift.

---

## 4. Tác động Việt Nam: Ngành Dầu khí Niêm yết và CPI Passthrough

### 4.1. Ngành dầu khí VN — Upstream, Downstream, Dịch vụ
| Nhóm | Tickers | Driver chính từ giá dầu | Nhạy cảm với giá dầu |
|---|---|---|---|
| **Upstream (E&P)** | GAS, PVS (một phần) | Giá condensate, natural gas, royalty | Cao — revenue linked to commodity price |
| **Dịch vụ (Services)** | PVS, PVD | Capex E&P toàn cầu, dayrate giàn khoan | Trung bình-Cao — lag 6-12 tháng |
| **Downstream (Refining)** | BSR, PLX | GRM (gross refining margin), crack spread | Trung bình — margin > price level |

**[DIỄN GIẢI]**
- **GAS (PV Gas):** Kinh doanh chủ yếu khí đốt và condensate. Giá khí thường được điều chỉnh theo cơ chế nhà nước (chậm hơn giá thế giới). Condensate tracking dầu thô với lag. Khi giá dầu tăng do supply shock (Hormuz), GAS hưởng lợi từ condensate nhưng bị hạn chế bởi pricing power khí đốt yếu.
- **PVS (PetroVietnam Technical Services):** Dịch vụ giàn khoan, EPCI, logistics. Dayrate giàn khoan tăng khi giá dầu > USD 70-80 duy trì 6 tháng+. Order book và utilization rate quan trọng hơn spot oil price.
- **PVD (PV Drilling):** Pure-play drilling. Dayrate semi-sub / jackup là leading indicator. Capex cycle toàn cầu (đặc biệt offshore Vietnam, Malaysia, Indonesia) quyết định demand.

### 4.2. CPI Passthrough — Kênh truyền dẫn vào lạm phát VN
**[SỰ KIỆN]** Xăng dầu chiếm ~3.5-4.0% rổ CPI Việt Nam (GSO) nhưng tác động gián tiếp qua vận tải, logistics, điện lớn hơn nhiều.

| Kênh | Trọng số ước tính | Lag | Elasticity ước tính |
|---|---|---|---|
| Xăng dầu trực tiếp (transport fuel) | ~3.7% CPI | 0-1 tháng | 1.0 (tương đối trực tiếp) |
| Vận tải hành khách/hàng hóa | ~8-10% CPI | 1-2 tháng | 0.3-0.5 |
| Điện (nhiệt điện dầu/khí) | ~4-5% CPI | 1-3 tháng | 0.2-0.4 |
| Logistics / supply chain | ~5-8% CPI | 2-4 tháng | 0.2-0.3 |
| **Tổng tác động gián tiếp ước tính** | **~15-20% CPI basket** | | |

**[DIỄN GIẢI]** Quỹ Bình ổn Giá xăng dầu (BOG) của MOF hoạt động như buffer: khi giá dầu tăng đột biến, quỹ chi để giữ giá bán lẻ; khi giá giảm, quỹ thu. Tuy nhiên, nếu giá dầu > USD 100 kéo dài > 3 tháng, quỹ BOG cạn kiệt → passthrough trở nên gần như hoàn toàn.

### 4.3. Freight cost và Shipping — Kênh bị bỏ quên
**[SỰ KIỆN]** VN nhập khẩu ~90% năng lượng (xăng dầu, than, LNG). Chi phí vận tải biển (freight) là một phần giá landed cost.

| Chỉ số | Ý nghĩa | Tác động đến VN |
|---|---|---|
| BDI (Baltic Dry Index) | Chi phí vận tải hàng rỗi (bulk) | Than nhập khẩu, nguyên liệu thô |
| SCFI (Shanghai Containerized Freight Index) | Container rate | Hàng hóa nhập khẩu, biên lợi nhuận manufacturing |
| Dirty tanker rates (VLCC, Suezmax) | Chi phí vận chuyển dầu thô | Chi phí nhập khẩu dầu Dubai/Oman |
| War risk insurance | Phí bảo hiểm qua vùng nguy hiểm | Tăng vọt khi Hormuz bị đe dọa |

[GIẢ THUYẾT] Nếu Hormuz bị phong tỏa một phần, dirty tanker rate có thể tăng 200-300%. VN không có strategic petroleum reserve (SPR) đáng kể; inventory cover ~20-30 ngày. Đây là điểm yếu cấu trúc chưa được pricing đầy đủ trong equity market.

---

## 5. Cross-asset Linkage và Regime Classification

### 5.1. Oil trong ma trận cross-asset VN
Pair với **workflow-cross-asset-linkage.md** để phân tích:
- **Oil ↑ → CPI VN ↑ → NHNN tightening expectation → VN rates ↑ → VN equity pressure** (channel: monetary policy)
- **Oil ↑ → GAS/PVS/PVD revenue ↑ → VN-Index sector rotation** (channel: sector earnings)
- **Oil ↑ → Freight ↑ → HPG/steel margin pressure** (channel: input cost)
- **Oil ↑ → USD demand ↑ (import bill) → VND pressure** (channel: BoP / FX)

### 5.2. Regime classification (framework-regime-v11.md)
| Regime | Giá dầu | VN Impact |
|---|---|---|
| **Supply shock (Hormuz)** | > USD 100, backwardation sâu | CPI risk, NHNN hawkish, equity rotation sang dầu khí |
| **Demand destruction (recession)** | < USD 60, contango | Margin bán lẻ tốt, dầu khí earnings downcycle |
| **OPEC+ managed balance** | USD 75-90, flat curve | Baseline — dầu khí VN ổn định, BOG hoạt động |
| **Shale surge (US supply)** | < USD 70, WTI discount | Pressure lên OPEC, dayrate giàn khoan giảm |

---

## 6. Monitoring Signposts

| Biến | Nguồn | Ngưỡng đáng chú ý |
|---|---|---|
| Brent spot | ICE Futures | > USD 100 (supply shock); < USD 60 (demand destruction) |
| Brent-WTI spread | ICE / NYMEX | > USD 5 (logistics/Asia sour tightness) |
| OPEC spare capacity | EIA / IEA | < 2 mbd (system vulnerability) |
| Hormuz transit volume | Vortexa / ClipperData | Giảm > 20% = red flag |
| Tanker war risk premium | Platts / Braemar | > USD 10/thùng = major disruption |
| VN BOG fund balance | MOF / Petrolimex disclosures | < 1 tháng coverage = passthrough risk |
| PVD/PVS dayrate / utilization | Company disclosures | Utilization > 85% = upcycle confirmation |

---

**Cross-ref:** **framework-regime-v11.md**, **workflow-cross-asset-linkage.md**, **domain-equity-vn-industry-guides.md** (section Dầu Khí), **domain-commodities-commodity-vn-impact.md** (nếu tồn tại).

**Data gap:** Không có dữ liệu real-time về SPR VN (không công bố). BOG fund balance chỉ có qua báo cáo tài chính Petrolimex và thông cáo MOF không đều.
