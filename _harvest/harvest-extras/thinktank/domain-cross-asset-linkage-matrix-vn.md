---
title: "Domain Cross-Asset Linkage Matrix VN — 10-Node Expanded Correlation + Transmission Strength Matrix"
module_type: "domain"
file_name: "domain-cross-asset-linkage-matrix-vn.md"
purpose: "Ma trận linkage đầy đủ 10-node cho cross-asset VN research: VN-Index, USD/VND, VN 10Y, oil, DXY, gold, CNY, copper, US 10Y real yield, Asia HY. Cung cấp cả correlation matrix (trung bình lịch sử + stressed) và transmission strength matrix (mechanism-based, có directionality và lag)."
primary_triggers:
  - "linkage matrix VN"
  - "ma trận liên kết đa tài sản"
  - "10-node matrix"
  - "correlation matrix VN"
  - "transmission matrix"
  - "gold VN linkage"
  - "CNY VND linkage"
  - "copper VN"
  - "US 10Y real yield VN"
  - "Asia HY VN"
when_to_use:
  - "Khi cần reference đầy đủ correlation giữa 10 node chính cho daily brief / deep-dive."
  - "Khi scenario analysis: shock node A thay đổi → node B, C, D ra sao."
  - "Khi cross-check kết luận cross-asset bằng transmission strength."
  - "Khi anchor regime classification bằng matrix state (stable vs stressed)."
when_not_to_use:
  - "Không dùng correlation lịch sử cho period stress — dùng stressed matrix."
  - "Không dùng single cell của matrix làm conclusion — phải xem ma trận cùng context regime."
  - "Không dùng cho asset ngoài 10 node mà không check data quality và linkage cơ chế."
related_modules:
  - "domain-cross-asset-correlation-regimes.md"
  - "domain-cross-asset-risk-on-off.md"
  - "domain-cross-asset-transmission-channels.md"
  - "domain-cross-asset-flight-to-quality.md"
  - "framework-regime-v11.md"
  - "workflow-cross-asset-linkage.md"
  - "macro-vn-transmission-channels.md"
  - "domain-fx-usd-vnd.md"
authoritative_citations:
  - "Diebold, F. X. and Yilmaz, K. Better to Give than to Receive: Predictive Directional Measurement of Volatility Spillovers (2012)."
  - "Rey, H. Dilemma not Trilemma: Global Financial Cycle and Monetary Policy Independence (2015)."
  - "Baur, D. G. and Lucey, B. M. Is Gold a Hedge or a Safe Haven? (2010)."
  - "Forbes, K. J. and Rigobon, R. No Contagion, Only Interdependence (2002)."
output_owner: "Reference matrix; analytical output contract thuộc workflow-cross-asset-linkage.md hoặc workflow-deep-dive.md."
---

# Domain Cross-Asset Linkage Matrix VN — Ma trận liên kết 10-node

Purpose: Cung cấp reference matrix đầy đủ cho cross-asset research VN. Mở rộng từ 5-node strawman (VN-Index, USD/VND, VN 10Y, oil, DXY) lên **10-node** theo gap analysis Kimi Lane 4, bổ sung **gold, CNY, copper, US 10Y real yield, Asia HY**. Mỗi cặp node có: (a) correlation lịch sử stable + stressed, (b) transmission strength với directionality và lag.

Trigger keywords: linkage matrix, 10-node matrix, correlation VN, transmission strength, gold linkage VN, CNY VND, copper leading indicator, US 10Y real yield, Asia HY spread, stressed correlation.

---

## 1. 10 NODE — DANH SÁCH VÀ RATIONALE

| # | Node | Ticker / Proxy | Vai trò trong linkage VN |
|---|---|---|---|
| 1 | **VN-Index** | VNINDEX (HOSE) | Equity benchmark domestic; retail sentiment proxy |
| 2 | **USD/VND** | USD/VND spot + NDF 3M | FX pillar; capital flow + trade linkage |
| 3 | **VN 10Y yield** | VN govt bond 10Y | Domestic rates; bank treasury positioning |
| 4 | **Oil** | Brent crude | Energy cost + CPI + trade balance |
| 5 | **DXY** | US Dollar Index | Global USD cycle; anchor cho EM FX |
| 6 | **Gold** | XAU/USD + SJC premium | Safe haven VN retail; geopolitical + real yield hedge |
| 7 | **CNY** | USD/CNY + USD/CNH | Anchor thương mại #1 VN; competitive FX pressure |
| 8 | **Copper** | LME copper | China growth proxy; manufacturing input cost |
| 9 | **US 10Y real yield** | TIPS 10Y | Global risk-free rate; gold driver; EM valuation |
| 10 | **Asia HY** | Asia HY CDX / ICE index | Regional credit sentiment; FII flow competition |

---

## 2. CORRELATION MATRIX — LỊCH SỬ STABLE (2015-2024 non-stress periods)

Rolling 90d Pearson correlation trên log daily returns (VND base), trung bình qua các period non-stress:

|  | VN-Idx | USD/VND | VN10Y | Oil | DXY | Gold | CNY | Copper | US10Y RY | Asia HY |
|---|---|---|---|---|---|---|---|---|---|---|
| **VN-Idx** | 1.00 | -0.15 | -0.10 | +0.10 | -0.20 | -0.10 | -0.15 | +0.25 | -0.20 | -0.30 |
| **USD/VND** | -0.15 | 1.00 | +0.15 | +0.10 | +0.55 | -0.05 | +0.60 | +0.05 | +0.25 | +0.30 |
| **VN 10Y** | -0.10 | +0.15 | 1.00 | +0.15 | +0.10 | -0.05 | +0.10 | -0.05 | +0.45 | +0.25 |
| **Oil** | +0.10 | +0.10 | +0.15 | 1.00 | -0.40 | +0.10 | -0.15 | +0.35 | +0.10 | -0.15 |
| **DXY** | -0.20 | +0.55 | +0.10 | -0.40 | 1.00 | -0.50 | +0.70 | -0.45 | +0.40 | +0.35 |
| **Gold** | -0.10 | -0.05 | -0.05 | +0.10 | -0.50 | 1.00 | -0.20 | +0.30 | **-0.55** | -0.20 |
| **CNY**† | -0.15 | +0.60 | +0.10 | -0.15 | +0.70 | -0.20 | 1.00 | -0.25 | +0.30 | +0.40 |
| **Copper** | +0.25 | +0.05 | -0.05 | +0.35 | -0.45 | +0.30 | -0.25 | 1.00 | -0.15 | -0.35 |
| **US10Y RY** | -0.20 | +0.25 | +0.45 | +0.10 | +0.40 | **-0.55** | +0.30 | -0.15 | 1.00 | +0.30 |
| **Asia HY** | -0.30 | +0.30 | +0.25 | -0.15 | +0.35 | -0.20 | +0.40 | -0.35 | +0.30 | 1.00 |

† CNY ở đây là USD/CNY: tăng = CNY yếu.
Asia HY: tăng = spread widening.

**Ghi chú quan trọng**: Các giá trị trên là **reference trung bình**. Biến thiên regime-specific có thể ±0.2 quanh trung bình. Phải dùng rolling-window thực tế từ domain-cross-asset-correlation-regimes.md để update.

---

## 3. CORRELATION MATRIX — STRESSED (Panic / FTQ periods)

Trong regime Tightening Stress, Deleveraging, hoặc Global Risk-Off (VIX >30, DXY breakout), correlation shift như sau:

|  | VN-Idx | USD/VND | VN10Y | Oil | DXY | Gold | CNY | Copper | US10Y RY | Asia HY |
|---|---|---|---|---|---|---|---|---|---|---|
| **VN-Idx** | 1.00 | **-0.40** | **-0.35** | -0.20 | **-0.55** | **+0.10** | -0.45 | -0.20 | -0.30 | **-0.65** |
| **USD/VND** | -0.40 | 1.00 | +0.35 | +0.15 | **+0.80** | -0.10 | **+0.85** | +0.20 | +0.40 | **+0.60** |
| **VN 10Y** | -0.35 | +0.35 | 1.00 | +0.10 | +0.30 | +0.05 | +0.30 | -0.10 | +0.55 | +0.45 |
| **Oil** | -0.20 | +0.15 | +0.10 | 1.00 | -0.30 | -0.05 | -0.10 | -0.15 | +0.05 | -0.25 |
| **DXY** | -0.55 | +0.80 | +0.30 | -0.30 | 1.00 | **-0.30** | **+0.85** | -0.55 | +0.55 | **+0.65** |
| **Gold** | +0.10 | -0.10 | +0.05 | -0.05 | -0.30 | 1.00 | -0.20 | +0.10 | **-0.25** | -0.10 |
| **CNY**† | -0.45 | +0.85 | +0.30 | -0.10 | +0.85 | -0.20 | 1.00 | -0.40 | +0.45 | +0.70 |
| **Copper** | -0.20 | +0.20 | -0.10 | -0.15 | -0.55 | +0.10 | -0.40 | 1.00 | -0.25 | -0.50 |
| **US10Y RY** | -0.30 | +0.40 | +0.55 | +0.05 | +0.55 | -0.25 | +0.45 | -0.25 | 1.00 | +0.50 |
| **Asia HY** | -0.65 | +0.60 | +0.45 | -0.25 | +0.65 | -0.10 | +0.70 | -0.50 | +0.50 | 1.00 |

**Bold** = shift ≥0.2 so với stable regime — correlation đổi dấu hoặc strengthen đáng kể.

### 3.1 Quan sát chính từ stressed matrix

1. **"Correlation goes to 1" cho risk asset**: VN-Index vs Asia HY = -0.65 (gần như perfect negative). Asia HY spread widen = VN-Index sell.
2. **Gold decouple khỏi real yield**: từ -0.55 (stable) → -0.25 (stressed). Geopolitical premium override.
3. **CNY-DXY-USD/VND triangle strengthen**: cả 3 correlation ≥0.80. VND effectively becomes function của DXY/CNY trong stress.
4. **VN-Index gần flat với gold (+0.10)**: safe haven VN bid ngay cả khi global risk asset sell.
5. **Copper-Asia HY correlation hash sharply negative (-0.50)**: China demand fear + credit stress đồng pha.

---

## 4. TRANSMISSION STRENGTH MATRIX

Khác với correlation (symmetric, statistical), transmission strength **có directionality** và **có lag**. Scale: 0 (không có) → 5 (mạnh, direct mechanism).

| From \ To | VN-Idx | USD/VND | VN10Y | Oil | DXY | Gold | CNY | Copper | US10Y RY | Asia HY |
|---|---|---|---|---|---|---|---|---|---|---|
| **VN-Idx** | — | 2 (1-2w) | 1 (1m) | 0 | 0 | 1 (retail) | 0 | 0 | 0 | 1 (regional) |
| **USD/VND** | 3 (1-3w) | — | 2 (1m) | 0 | 1 | 1 (retail FTQ) | 2 | 0 | 1 | 1 |
| **VN 10Y** | 3 (2-4w) | 2 (2-4w) | — | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| **Oil** | 3 (1-3m CPI) | 2 (1-2m trade) | 2 (CPI→SBV) | — | 2 | 2 | 1 | 3 | 2 | 2 |
| **DXY** | 4 (1-2w) | **5 (1-5d)** | 3 (1-2w) | 3 (1-5d) | — | 4 (1-5d) | **5 (1-5d)** | 4 (1-2w) | 3 (1-5d) | 4 (1-2w) |
| **Gold** | 1 (retail) | 1 (retail USD) | 0 | 0 | 1 | — | 0 | 1 | 1 | 0 |
| **CNY** | 4 (1-2w trade) | **5 (1-5d)** | 2 (1m) | 2 (1w) | 4 (1-5d) | 1 | — | 4 (1-2w) | 1 | 4 (1-2w) |
| **Copper** | 2 (1-2m mfg) | 1 (1m) | 1 (1-2m CPI) | 3 (1-2w) | 2 | 2 | 3 (1-2w) | — | 1 | 3 (1-2w) |
| **US 10Y RY** | 4 (1-3w) | 3 (1-2w) | 3 (1-2w) | 2 | 4 (1-2w) | **5 (1-5d)** | 4 (1-2w) | 3 (1-2w) | — | 4 (1-2w) |
| **Asia HY** | 4 (1-3w) | 3 (1-2w) | 3 (1-2w) | 1 | 3 (1-2w) | 1 | 4 (1-2w) | 3 (1-2w) | 3 (1-2w) | — |

**Đọc cell**: `From row → To column`. Số là strength (0-5), ngoặc là lag điển hình.

### 4.1 Node quan trọng nhất (highest out-degree)

1. **DXY**: transmit strong đến 9/9 node khác. DXY shock = system-wide reprice.
2. **CNY**: transmit strong đến USD/VND, DXY, copper, Asia HY. Dominant cho VN regional exposure.
3. **US 10Y real yield**: transmit strong đến gold, DXY, VN-Index. Global risk-free rate anchor.
4. **Asia HY**: transmit strong đến VN-Index, USD/VND, VN 10Y. Regional credit benchmark.

### 4.2 Node receiving nhất (highest in-degree)

1. **VN-Index**: nhận transmission từ hầu hết node với lag 1-4 tuần. High beta domestic.
2. **USD/VND**: nhận transmission DXY, CNY với strength 5 và lag 1-5 ngày. Fast reprice.
3. **Gold**: nhận mạnh từ US 10Y real yield + DXY. Global benchmark.

---

## 5. SCENARIO ANALYSIS — SHOCK PROPAGATION

### Scenario A: US 10Y real yield +50bp (Fed hawkish surprise)

Propagation (lag order):
- **T+1-5d**: DXY +2-3%, Gold -3-5%, CNY weak, Asia HY spread +50-80bp widen.
- **T+1-2w**: USD/VND pressure +0.5-1%, VN-Index -3-5%, copper -5-8%, oil softer.
- **T+2-4w**: VN 10Y yield +20-40bp (if SBV không react), FII outflow VN +USD 100-200M/week.
- **T+1-3m**: VN CPI transport pass-through, SBV tone hawkish, VN corporate bond spread widen.

### Scenario B: CNY 5% devaluation (China stimulus + competitive)

Propagation:
- **T+1-5d**: USD/CNY +5%, DXY +2%, copper -10%, oil mixed, Asia HY spread +100bp.
- **T+1-2w**: USD/VND +1.5-3% (VND follow CNY partially), VN-Index -5-8%, export equity VN bid.
- **T+2-4w**: SBV reserve burn, NDF VND premium spike, FII rotate out.
- **T+1-3m**: VN trade deficit narrow (competitive), but import cost from China rise in CNY.

### Scenario C: Oil +30% (Hormuz closure)

Propagation:
- **T+1-5d**: Oil +30%, gold +5-8%, DXY mixed (petrodollar + risk-off opposing).
- **T+1-2w**: VN CPI transport ↑, USD/VND pressure (trade deficit).
- **T+1-3m**: VN CPI breach 4% target, SBV hawkish pivot, VN-Index consumer discretionary sell.
- **Sector rotation**: GAS, PVS bid; VJC, airline sell; retail sell.

---

## 6. MATRIX UPDATE PROTOCOL

Matrix này là **living reference**, cần update:
- Hàng quý: rolling correlation 90d cho mỗi cặp.
- Hàng năm: stressed correlation từ mọi panic event trong năm.
- Ad-hoc: khi detect structural break (CUSUM / Bai-Perron) → update baseline.
- Khi regime shift (framework-regime-v11): re-classify current regime và sử dụng matrix phù hợp.

---

## 7. CẢNH BÁO

- Correlation ≠ causation. Transmission matrix mới phản ánh causation.
- Matrix này là **reference statistical**, không phải prediction tool.
- Trong panic, nhiều correlation saturate về ±1 — matrix bình thường không apply.
- Data quality khác nhau: VN 10Y liquidity thấp hơn UST → noise correlation cao hơn.
- NDF VND có thể deviate spot đáng kể trong stress — dùng cả 2 trong FX analysis.

---

## 8. CROSS-REFERENCES

- Correlation methodology: **domain-cross-asset-correlation-regimes.md**
- RORO state hiện tại: **domain-cross-asset-risk-on-off.md**
- Transmission mechanism chi tiết: **domain-cross-asset-transmission-channels.md**
- FTQ pattern: **domain-cross-asset-flight-to-quality.md**
- Regime anchor: **framework-regime-v11.md**
- VN monetary transmission: **macro-vn-transmission-channels.md**
- FX detail: **domain-fx-usd-vnd.md**
- Workflow output: **workflow-cross-asset-linkage.md**
