---
title: "Domain Commodities Gold Precious — Gold Drivers, Real Yield Regime, USD, Central Bank Buying, Geopolitical Hedge, Vietnam Retail Demand ~40 tonnes/year"
module_type: "domain"
file_name: "domain-commodities-gold-precious.md"
purpose: "Phân tích động lực giá vàng toàn cầu với trọng tâm real yield regime (OPVIA P0), central bank buying kỷ lục 2023-2026, geopolitical hedge premium, và thị trường vàng bán lẻ Việt Nam (~40 tấn/năm). Không khuyến nghị mua/bán."
primary_triggers:
  - "giá vàng"
  - "gold price drivers"
  - "real yield gold"
  - "central bank gold buying"
  - "geopolitical hedge gold"
  - "vàng Việt Nam"
  - "SJC gold"
  - "gold decouple real yield"
  - "gold safe haven"
when_to_use:
  - "Khi phân tích giá vàng, động lực cung-cầu, và vai trò safe haven trong portfolio đa-asset."
  - "Khi đánh giá gold-real yield correlation và điều kiện decouple (geopolitical premium dominance)."
  - "Khi phân tích thị trường vàng bán lẻ Việt Nam, chênh lệch SJC-world, và tác động đến tâm lý nhà đầu tư VN."
when_not_to_use:
  - "Không dùng để dự báo giá vàng cụ thể tại thờii điểm X — chỉ dùng cho regime classification và scenario bounds."
  - "Không dùng để khuyến nghị mua/bán vàng hoặc cổ phiếu ngành vàng."
related_modules:
  - "framework-regime-v11.md"
  - "workflow-cross-asset-linkage.md"
  - "domain-equity-vn-industry-guides.md"
  - "domain-fx-usd-vnd-dynamics.md"
  - "reference-vn-data-sources.md"
authoritative_citations:
  - "World Gold Council (WGC) — Gold Demand Trends (quarterly)."
  - "IMF International Financial Statistics — central bank gold reserves."
  - "Fed Funds Rate, US 10Y TIPS yield (FRED)."
  - "LBMA Gold Price AM/PM fixings."
  - "NHNN / SJC / DOJI gold price data Vietnam."
output_owner: "workflow-deep-dive.md khi phân tích sâu vàng; workflow-cross-asset-linkage.md khi phân tích gold-FX-equity linkage; workflow-daily-brief.md cho gold price update overnight."
---

# Domain Commodities Gold Precious — Động lực Giá Vàng / Real Yield Regime / Thị trường VN

Purpose: Cung cấp lens phân tích vàng toàn cầu và Việt Nam. Trọng tâm: real yield regime (framework nội bộ OPVIA P0), central bank buying kỷ lục, geopolitical hedge premium, gold-USD decoupling dynamics, và thị trường bán lẻ VN (SJC, DOJI, nhu cầu ~40 tấn/năm). Triggers: giá vàng, gold drivers, real yield, SJC, central bank gold, safe haven, gold decouple.

---

## 1. Gold — Real Yield Regime (OPVIA P0 Framework)

### 1.1. Mối quan hệ vàng — real yield: Lý thuyết và Thực nghiệm
Vàng là tài sản không trả coupon/dividend, không có cash flow. Opportunity cost của việc nắm giữ vàng là **real yield** (lợi suất thực tế trên trái phiếu chính phủ lạm phát bảo vệ, thường dùng US 10Y TIPS yield).

**[SỰ KIỆN]** Tương quan âm giữa gold và US 10Y real yield đã được kiểm chứng mạnh 2003-2023 (correlation ~ -0.7 đến -0.8). Tuy nhiên, từ 2022-2026, correlation suy yếu đáng kể do central bank buying và geopolitical premium.

| Giai đoạn | US 10Y Real Yield | Giá Vàng (USD/oz) | Regime | Correlation strength |
|---|---|---|---|---|
| 2020 (COVID crash) | -1.0% → -0.5% | 1,500 → 2,070 | Real yield âm sâu | Mạnh (-0.8) |
| 2021-2022 (Fed hawkish) | -0.5% → +1.9% | 2,070 → 1,620 | Real yield dương cao | Mạnh (-0.75) |
| 2023 (Fed pause) | +1.9% → +1.5% | 1,620 → 2,080 | Real yield giảm nhẹ | Trung bình (-0.5) |
| 2024 | +1.5% → +2.0% | 2,080 → 2,630 | Real yield tăng, gold tăng | Yếu / Gãy (~0.0) |
| 2025-2026 (YTD) | +1.8% → +2.2% | 2,630 → 3,000+ | Real yield cao, gold cao hơn | Gãy / Dương nhẹ |

### 1.2. Regime Classification: Khi nào gold follow real yield, khi nào decouple
**[DIỄN GIẢI]** OPVIA chia gold-real yield relationship thành 3 regime:

| Regime | Điều kiện | Gold behavior | Dominant driver |
|---|---|---|---|
| **Regime A: Real Yield Dominant** | Real yield biến động > 50bps, geopolitical calm | Gold follow real yield (inverse) | Opportunity cost |
| **Regime B: Mixed** | Real yield ổn định, có geopolitical noise | Gold sideway-tăng nhẹ, correlation yếu | Cân bằng nhiều yếu tố |
| **Regime C: Geopolitical Premium Dominant** | Chiến tranh / sanctions / de-dollarization | Gold decouple khỏi real yield, tăng độc lập | Safe haven + central bank demand |

**[SỰ KIỆN]** 2024-2026 đang ở Regime C: US 10Y real yield ở mức cao (~2.0%) nhưng gold vẫn phá đỉnh lịch sử. Lý do:
1. Central bank buying kỷ lục (xem mục 2).
2. De-dollarization narrative + BRICS reserve diversification.
3. Chiến tranh Iran-US + xung đột Đông Âu + căng thẳng Đài Loan.
4. Fiscal dominance ở US: deficit ~6-7% GDP làm real yield "high but not trusted."

### 1.3. Operationalization: Cách dùng framework trong phân tích
Khi phân tích gold, luôn hỏi:
1. Real yield đang ở đâu? Trend là gì? (FRED TIPS 10Y)
2. Geopolitical premium có đang dominate không? (VIX, oil spike, news flow)
3. Central bank net buying > 1,000 tấn/năm không? (WGC data)
4. Nếu cả 2 và 3 đúng → real yield model underpredicts gold price → dùng scenario bounds thay vì point estimate.

---

## 2. Central Bank Gold Buying: Dữ liệu 2023-2026

### 2.1. Dữ liệu thực tế
**[SỰ KIỆN]** 2022-2024 là 3 năm central bank buying cao nhất lịch sử (kể từ khi có dữ liệu đáng tin cậy 1950):

| Năm | Central bank net buying (tấn) | % của demand toàn cầu |
|---|---|---|
| 2021 | 463 | ~10% |
| 2022 | 1,082 | ~24% |
| 2023 | 1,037 | ~24% |
| 2024 (ước tính) | ~1,050 | ~23% |
| 2025-2026 (YTD) | ~800+ annualized | ~22% |

### 2.2. Các ngân hàng trung ương mua nhiều nhất
| Quốc gia | Tích lũy 2022-2026 (tấn ước tính) | Động cơ chính |
|---|---|---|
| **Trung Quốc (PBOC)** | ~300-350 | De-dollarization, diversify from UST, CNY internationalization |
| **Ba Lan** | ~130 | Geopolitical hedge (Ukraine border), EU skepticism |
| **Singapore** | ~75 | Reserve diversification, wealth fund logic |
| **Thổ Nhĩ Kỳ** | ~150 | Lạm phát cao, lira devaluation, domestic demand + official |
| **Ấn Độ** | ~80 | Tradition + RBI diversification |
| **Nga (pre-2022)** | N/A | Đã tích lũy từ trước, bị đóng băng USD/EUR reserve |
| **Các nước khác** | ~400+ | Bandwagon effect, fear of sanctions |

**[DIỄN GIẢI]** Central bank buying khác retail/ETF ở chỗ: (a) không bán khi giá giảm (sticky demand), (b) không sensitive với real yield ngắn hạn, (c) thường mua physical và rút khỏi hệ thống LBMA/COMEX → giảm "free float" gold available cho thị trường tư nhân.

### 2.3. "Unreported buying" — yếu tố bị đánh giá thấp
[GIẢ THUYẾT] WGC data chỉ bao gồm reported buying. Nhiều analyst ước tính rằng Trung Quốc và một số nước BRICS mua qua proxy (sovereign wealth funds, state-owned banks) không báo cáo vào IMF. Nếu đúng, central bank demand có thể cao hơn 20-30% so với số liệu chính thức.

---

## 3. USD và Gold: Quan hệ Đối trọng và Ngoại lệ

### 3.1. DXY — Gold inverse: Khi nào đúng, khi nào sai
Truyền thống: DXY ↑ → gold ↓ (vì gold priced in USD). Tuy nhiên, 2022-2026 chứng kiến nhiều giai đoạn cả DXY và gold cùng tăng.

| Giai đoạn | DXY | Gold | Giải thích |
|---|---|---|---|
| Q3/2022 | 114 (đỉnh) | 1,620 (đáy) | Inverse hoàn hảo — Fed hawkish, real yield ↑ |
| Q1/2023 | 102 | 1,950 | Cùng tăng nhẹ — banking stress (SVB), flight to quality |
| Q4/2023 | 103 | 2,080 | Cùng tăng — Israel-Gaza, Fed pause |
| 2024 | 100-106 | 2,080-2,790 | Cùng tăng mạnh — de-dollarization + fiscal dominance |
| 2025-2026 | 103-108 | 2,790-3,000+ | Cùng tăng — Iran-US war, BRICS reserve shift |

**[DIỄN GIẢI]** Khi lý do tăng của DXY là **safe-haven flight** (không phải carry/rate differential), gold có thể tăng cùng. Đây là "fear correlation" thay vì "opportunity cost correlation."

### 3.2. Gold trong context VND
VND không freely convertible; thị trường vàng VN có cơ chế riêng. Tuy nhiên:
- Giá vàng SJC tracking giá thế giới với **spread thuế, phí, và premium địa phương**.
- Khi VND mất giá so với USD (hoặc kỳ vọng mất giá), nhu cầu vàng vật chất tăng.
- **Chênh lệch SJC — giá thế giới quy đổi** là proxy cho kỳ vọng VND devaluation + premium thanh khoản thị trường nội địa.

---

## 4. Geopolitical Hedge Premium: Khi Vàng "Bỏ qua" Real Yield

### 4.1. Cơ chế geopolitical premium
Geopolitical premium = phần giá vàng không được giải thích bởi real yield, USD, hoặc jewelry demand. Được đo lường bằng residual từ regression model (gold ~ real yield + DXY + ETF holdings + jewelry demand).

**[SỰ KIỆN]** Ước tính residual 2024-2026:
- Q1-Q2/2024: +USD 100-150/oz (Israel-Gaza, Red Sea)
- Q3-Q4/2024: +USD 200-300/oz (Ukraine escalation fears, US election uncertainty)
- 2025-2026: +USD 300-500/oz (Iran-US war direct, Hormuz risk, de-dollarization)

### 4.2. Historical analog: 1979-1980 vs 2025-2026
| | 1979-1980 | 2025-2026 |
|---|---|---|
| Real yield | -2% (cực thấp) | +2% (cao) |
| Geopolitical | Iran Revolution + Hostage Crisis | Iran-US war + Hormuz |
| Gold peak | USD 850/oz | USD 3,000+ |
| Driver chính | Real yield âm + geopolitical | Geopolitical + de-dollarization |
| Inflation | > 10% | 2-3% (US) |

**[DIỄN GIẢI]** Analog 1979-1980 chỉ giới hạn: lạm phát hiện tại thấp hơn nhiều. Tuy nhiên, **fiscal dominance** (deficit cao kéo dài) và **reserve diversification** là yếu tố mới không tồn tại 1980.

---

## 5. Thị trường Vàng Việt Nam: Bán lẻ và Chính sách

### 5.1. Quy mô và đặc thù
**[SỰ KIỆN]** Việt Nam tiêu thụ khoảng **35-45 tấn vàng/năm** (WGC 2023-2024 estimate), chủ yếu dưới dạng trang sức và vàng miếng SJC.

| Phân khúc | Tỷ trọng ước tính | Đặc điểm |
|---|---|---|
| Trang sức | ~55-60% | Demand seasonal (Tết, cưới hỏi), price-inelastic |
| Vàng miếng (SJC) | ~30-35% | Investment demand, sensitive với VND devaluation expectation |
| Công nghiệp / điện tử | ~5-8% | Electronics, dental — stable |
| Ngân hàng NHNN | ~2-3% | Dự trữ vàng chính thức ~80 tấn (rất thấp so với GDP) |

### 5.2. SJC Premium và Quản lý Nhà nước
**[SỰ KIỆN]** SJC (Tập đoàn Vàng bạc Đá quý Sài Gòn) từng là đơn vị độc quyền sản xuất vàng miếng được NHNN cấp phép. Từ 2024, NHNN mở rộng cấp phép cho thêm DOJI, PNJ, Bảo Tín Minh Châu.

**[DIỄN GIẢI]** SJC premium (chênh lệch giá SJC so với giá thế giới quy đổi) thường dao động:
- Bình thường: +USD 5-15/oz (~0.3-1.0%)
- Căng thẳng tỷ giá / VND devaluation fear: +USD 30-80/oz (2-5%)
- Siết nhập khẩu vàng / thanh khoản khan hiếm: +USD 100+/oz

[GIẢ THUYẾT] Premium cao kéo dài tạo áp lực buộc NHNN nhập khẩu thêm vàng hoặc nới lỏng quota. Nếu không, thị trường song song (grey market) phát triển.

### 5.3. Vàng như Safe Haven ở VN
Ở Việt Nam, vàng đóng vai trò:
1. **Hedge VND devaluation:** Khi USD/VND tăng hoặc kỳ vọng tăng, nhu cầu vàng tăng nhanh hơn lãi suất tiết kiệm.
2. **Wealth preservation:** Thay thế cho BĐS khi BĐS thanh khoản kém (2023-2025).
3. **Flight to quality cá nhân:** Trong stress episode (ngân hàng SCB 2022, trái phiếu doanh nghiệp 2023), ngườii dân đổ sang vàng.

Pair với **domain-equity-vn-industry-guides.md** (ngành Vàng / Bán lẻ) để xem PNJ, DOJI earnings sensitivity.

---

## 6. Cross-asset Linkage: Gold trong Ma trận VN

### 6.1. Transmission channels
| From | To | Channel | Strength |
|---|---|---|---|
| Gold ↑ | VND ↓ (expectation) | Wealth store shift, FX substitution | Medium-High |
| Gold ↑ | PNJ / DOJI revenue ↑ | Jewelry + bar sales | Medium |
| Gold ↑ | NHNN import bill ↑ | Vàng nhập khẩu → FX outflow | Medium |
| Real yield ↓ | Gold ↑ | Global opportunity cost | High (Regime A) |
| Real yield ↓ | VN rates ↓ (lag) | Fed cut → EM rates room | Medium |
| DXY ↑ + Gold ↑ | VND mixed | Safe-haven DXY but VND gold demand | Low-Medium |

### 6.2. Decisive observables
| Observable | Regime A (Real yield dominant) | Regime C (Geopolitical dominant) |
|---|---|---|
| Gold-real yield correlation | -0.6 to -0.8 | 0.0 to +0.3 |
| ETF flows | Strong predictive | Weak / outflows despite price rise |
| Central bank buying | < 800 tấn/năm | > 1,000 tấn/năm |
| Geopolitical news flow | Background noise | Front-page, oil spike > USD 10 |
| DXY-gold | Inverse | Positive correlation |

---

## 7. Monitoring Signposts

| Biến | Nguồn | Ngưỡng đáng chú ý |
|---|---|---|
| US 10Y TIPS yield | FRED | < 0% = gold bull; > 2.5% = headwind (nếu Regime A) |
| Central bank net buying (quarterly) | WGC Gold Demand Trends | > 300 tấn/quý = structural support |
| DXY | ICE / Bloomberg | > 110 = EM stress, nhưng gold có thể decouple |
| SJC premium vs world | SJC / DOJI / NHNN | > 3% = VND stress signal |
| VN gold import quota | NHNN / Customs | Cắt giảm = supply squeeze, premium ↑ |
| ETF holdings (GLD, IAU) | Bloomberg | Outflows + price rise = central bank/retail demand |
| Iran-US escalation | News flow / DoD statements | Direct strike = +USD 100-200/oz tail risk |

---

**Cross-ref:** **framework-regime-v11.md**, **workflow-cross-asset-linkage.md**, **domain-equity-vn-industry-guides.md** (ngành Vàng / Bán lẻ), **domain-fx-usd-vnd-dynamics.md**.

**Data gap:** Không có dữ liệu real-time về dự trữ vàng NHNN VN cập nhật hàng tháng. SJC premium chỉ có qua website bán lẻ, không có time-series điện tử chuẩn. Central bank "unreported buying" là ước tính, không có source độc lập xác nhận.
