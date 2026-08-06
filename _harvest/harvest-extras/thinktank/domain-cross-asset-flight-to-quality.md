---
title: "Domain Cross-Asset Flight-to-Quality — FTQ Patterns, Leading Indicators, VN-Specific Safe Haven (Gold, USD Cash, TPCP)"
module_type: "domain"
file_name: "domain-cross-asset-flight-to-quality.md"
purpose: "Codify pattern flight-to-quality (FTQ) trong stress event: asset nào được bid, asset nào bị sell, leading indicator của FTQ, và đặc điểm riêng của FTQ Việt Nam nơi vàng miếng, USD cash cá nhân, và TPCP là safe haven chính thay vì UST hay JPY."
primary_triggers:
  - "flight to quality"
  - "flight to safety"
  - "safe haven VN"
  - "FTQ pattern"
  - "vàng như safe haven"
  - "USD cash retail VN"
  - "TPCP safe haven"
  - "stress event asset"
  - "panic flow"
when_to_use:
  - "Khi đánh giá stress event và xác định asset nào sẽ được bid, sell."
  - "Khi phân tích retail behavior VN trong panic: vàng miếng, USD cá nhân, tiết kiệm."
  - "Khi detect leading indicator FTQ để pre-position analysis."
  - "Khi cross-check RORO Panic state bằng FTQ pattern."
when_not_to_use:
  - "Không dùng trong regime risk-on bình thường — FTQ chỉ bật khi stress đủ lớn."
  - "Không dùng làm signal mua vàng / USD — đây là lens diagnostic."
  - "Không nhầm FTQ với flight-to-liquidity (khác nhau: FTQ seeks credit quality; FTL seeks liquidity)."
related_modules:
  - "domain-cross-asset-risk-on-off.md"
  - "domain-cross-asset-correlation-regimes.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
  - "framework-regime-v11.md"
  - "workflow-cross-asset-linkage.md"
  - "domain-fx-usd-vnd.md"
  - "macro-vn-credit-cycle.md"
  - "macro-vn-monetary-policy-nhnn.md"
authoritative_citations:
  - "Longstaff, F. A. The Flight-to-Liquidity Premium in U.S. Treasury Bond Prices (2004)."
  - "Vayanos, D. Flight to Quality, Flight to Liquidity, and the Pricing of Risk (2004)."
  - "Beber, A., Brandt, M. W., and Kavajecz, K. A. Flight-to-Quality or Flight-to-Liquidity? (2009)."
  - "Baur, D. G. and Lucey, B. M. Is Gold a Hedge or a Safe Haven? (2010)."
output_owner: "Analytical lens only; pair với workflow-cross-asset-linkage.md hoặc workflow-regime-shift-alert.md."
---

# Domain Cross-Asset Flight-to-Quality — Chế độ tháo chạy về an toàn

Purpose: Nhận diện và phân tích flight-to-quality (FTQ) events — khi capital flee từ risk asset sang safe haven. FTQ khác flight-to-liquidity (FTL): FTQ tìm credit quality (gold, UST, TPCP của quốc gia low risk); FTL tìm market liquidity (USD cash, on-the-run UST, deep market). Ở VN, FTQ có pattern riêng do cấu trúc tài sản retail và capital control mềm.

Trigger keywords: flight to quality, flight to safety, safe haven, vàng miếng SJC, USD cash cá nhân, TPCP VN, panic asset, stress event, retail defensive behavior.

---

## 1. KHÁI NIỆM — FTQ vs FTL

### 1.1 Phân biệt

| Khái niệm | Định nghĩa | Asset được bid | Ví dụ event |
|---|---|---|---|
| **Flight-to-Quality** | Capital chuyển từ risky credit sang high-quality credit | Gold, UST, AAA sovereign, blue-chip currency | 2008, 2020 COVID Q1 |
| **Flight-to-Liquidity** | Capital chuyển từ illiquid sang liquid asset, không quan trọng quality | USD cash, on-the-run UST, deep FX pair | 2008 Q4 (Lehman aftermath) |
| **Flight-to-Safety** (umbrella) | Combined FTQ + FTL | Cả hai | Mọi panic event |

Ở VN, trong stress lớn thường cả 2 diễn ra đồng thời với tín hiệu rõ:
- FTQ signal: vàng miếng SJC premium vs world gold tăng, TPCP yield giảm.
- FTL signal: USD cash cá nhân bid (premium vs official rate tăng), interbank ON rate spike.

### 1.2 Tại sao FTQ ở VN khác developed markets

| Yếu tố | Developed markets | VN |
|---|---|---|
| Safe haven chính | UST, JPY, gold, CHF | **Vàng miếng SJC, USD cash, TPCP VND** |
| Currency safe haven | USD, JPY, CHF | USD (retail cash), không phải JPY |
| Retail access | Mutual fund, ETF, bond | Vàng vật chất, USD cash, tiết kiệm ngân hàng |
| Central bank role | Provider of last resort cho UST | SBV can thiệp FX để bảo vệ VND |
| Information flow | Real-time, transparent | Lagged, narrative-driven |

---

## 2. VN-SPECIFIC SAFE HAVEN HIERARCHY

### 2.1 Thứ tự safe haven VN trong stress

| Cấp | Asset | Retail accessibility | Role |
|---|---|---|---|
| **1 (Primary)** | **Vàng miếng SJC** | Cao — mọi tiệm vàng | Store of value chống lạm phát + geopolitical |
| **2 (Primary)** | **USD cash cá nhân** | Trung bình — chợ đen + ngân hàng | Hedge VND devaluation |
| **3 (Secondary)** | **Tiết kiệm VND lớn (VCB, BID, CTG)** | Cao | Hedge credit risk tư nhân (SCB episode 2022) |
| **4 (Secondary)** | **TPCP VN (retail indirect qua fund)** | Thấp-trung | Institutional safe haven |
| **5 (Tertiary)** | **BĐS prime location (HCM Q1, Hà Nội Ba Đình)** | Thấp | Long-run store of value (illiquid) |
| **6 (Emerging)** | **USD savings qua USDT / crypto** | Trung | Emerging retail hedge (capital control bypass) |

### 2.2 Vàng miếng SJC — case study

Vàng miếng SJC là safe haven đặc trưng VN với đặc điểm:
- **Premium over world gold**: thường 3-7% trong normal time, có thể >15% trong panic (2022 peak ~20%).
- **Retail demand ~40 tấn/năm** (2023-2024).
- **NHNN độc quyền nhập khẩu vàng nguyên liệu** → tạo scarcity premium structural.
- **Leading indicator**: premium SJC widen >10% trước khi retail equity sell-off (lag ~2-4 tuần).

FTQ vào vàng ở VN thường có 2 wave:
- Wave 1 (informed): smart money + large retail, khởi đầu trước panic visible.
- Wave 2 (panic): mass retail, thường đỉnh sau peak panic 1-2 tuần → dấu hiệu FTQ gần kết thúc.

### 2.3 USD cash — case study

USD cash cá nhân VN có 2 channel:
- **Official**: nhận kiều hối, cất giữ (không được bán lại ngân hàng theo Nghị định).
- **Chợ đen / gray market**: buying/selling với premium vs official rate.

Premium chợ đen vs official rate là **leading indicator VND devaluation expectation**:
- <0.3%: neutral.
- 0.5-1%: mild stress.
- 1-3%: significant stress, SBV thường đã bắt đầu intervene.
- >3%: crisis level, thường kéo theo NHNN emergency measures.

---

## 3. LEADING INDICATOR FTQ

### 3.1 Global leading indicators (3-7 ngày trước FTQ peak)

| Indicator | Ngưỡng trigger | Cơ chế |
|---|---|---|
| **VIX term structure inversion** | VIX > VIX3M | Short-term vol > medium-term = panic |
| **MOVE index spike** | >150 từ baseline ~100 | UST vol = stress fixed income |
| **Copper/gold ratio** | Drop >10% trong 2 tuần | Growth fear + safe haven bid |
| **CDS spread** (sovereign + financial) | Widening >30% trong 1 tuần | Credit risk repricing |
| **USD funding spread** (FX swap basis) | Widening beyond -50bp | Dollar shortage global |
| **Repo market stress** (SOFR - IOER) | >20bp | Funding stress |

### 3.2 VN-specific leading indicators (1-3 tuần trước FTQ peak)

| Indicator | Ngưỡng trigger | Cơ chế |
|---|---|---|
| **SJC premium vs world gold** | >10% | Retail FTQ incipient |
| **USD chợ đen premium vs official** | >1% | VND devaluation expectation |
| **Interbank ON rate** vs SBV target | Spike >200bp | Bank funding stress |
| **Corporate bond yield AAA 5Y** widening | >100bp trong 1 tháng | Credit stress |
| **Net FII outflow HOSE** | 3 tuần liên tục + accelerating | FII pre-emption |
| **Margin balance brokers** contract | >10% drop trong 2 tuần | Domestic deleveraging |
| **VN-Index breadth** | % above 50MA <30% | Broad-based selling |

### 3.3 Composite FTQ score (VN)

Weighted combination của 7 indicator trên → scale 0-100. Ngưỡng:
- 0-30: Normal (no FTQ).
- 30-50: Elevated risk.
- 50-70: FTQ active.
- 70-100: Full panic / crisis.

---

## 4. ASSET BEHAVIOR TRONG FTQ

### 4.1 Matrix FTQ behavior

| Asset | FTQ Early (score 30-50) | FTQ Active (50-70) | FTQ Panic (70+) |
|---|---|---|---|
| **VN-Index** | Choppy, breadth narrow | Sell-off blue-chip | Gap down, circuit breaker |
| **VND** | Mild weakness | SBV visible intervention | Hard floor defend, reserve burn |
| **VN TPCP 10Y** | Yield flat/down slightly | Yield down (FTQ bid) | Ambiguous (can yield up if USD bid domestic) |
| **Vàng SJC** | Premium widening | Premium >10% | Premium >15%, retail rush |
| **USD cash (chợ đen)** | Premium <1% | Premium 1-2% | Premium >3% |
| **Corporate bond** | Spread widen slowly | Spread widen fast | Market freeze |
| **BĐS** | Turnover drop | Price drop slight | Price drop significant, transaction freeze |
| **Deposit VCB/BID** | Stable | Inflow từ bank nhỏ | Large inflow, bank run nhỏ |

### 4.2 Sector rotation trong FTQ (VN equity)

| Sector | Early FTQ | Active FTQ | Panic |
|---|---|---|---|
| Banks (VCB, BID, CTG) | Mild sell | Moderate sell | Sell nhưng relative outperform |
| BĐS (VHM, NVL, KDH) | Sell | Strong sell | Crash |
| Retail (MWG, FRT) | Mild sell | Strong sell | Crash (discretionary) |
| Utilities (POW, GAS) | Flat | Relative outperform | Less drawdown |
| Staples (VNM, MSN) | Flat | Relative outperform | Defensive bid |
| Healthcare (DHG, IMP) | Flat | Outperform | Rare defensive bid |
| Tech (FPT) | Sell | Sell | Depends on USD cost/revenue mix |

---

## 5. FTQ UNWIND — KHI FTQ KẾT THÚC

### 5.1 Pattern unwind

FTQ unwind thường có 3 phase:
1. **Peak panic plateau** (1-2 tuần): safe haven asset bid đạt đỉnh nhưng không accelerate.
2. **Stabilization** (2-4 tuần): policy response (Fed liquidity, SBV OMO) absorb stress; safe haven premium shrink.
3. **Unwind / rotation** (4-12 tuần): risk asset recover, gold/USD cash bị sell, TPCP yield rebound.

### 5.2 Leading indicator unwind

- SJC premium shrink từ peak.
- Chợ đen USD premium giảm về <0.5%.
- FII net buy resume.
- Margin balance recover.
- Corporate bond spread tighten.

### 5.3 VN-specific unwind friction

- Retail gold buyer thường **không bán** sau panic — store of value long-run. Unwind chủ yếu từ smart money/institutional.
- USD cash unwind chậm vì lack of formal channel to sell.
- TPCP unwind driven by bank treasury behavior + NHNN OMO stance.

---

## 6. CẢNH BÁO — KHÔNG NHẦM LẪN

- **FTQ ≠ Risk-Off bình thường**: risk-off có thể xảy ra mà không có FTQ. FTQ cần stress đủ lớn để active safe haven bid.
- **Gold ≠ luôn safe haven**: gold có thể bị sell trong liquidity crunch đầu (margin call 2020 Q1). Chỉ sau wave 1 liquidation, gold mới bid.
- **VN TPCP ≠ UST**: TPCP VND có FX risk cho foreign investor, không phải global safe haven. Chỉ safe haven cho VN institution.
- **BĐS ≠ safe haven trong FTQ**: BĐS illiquid, transaction freeze. Store of value chỉ trong long-run, không phải trong stress.

---

## 7. CROSS-REFERENCES

- RORO state: **domain-cross-asset-risk-on-off.md**
- Correlation trong stress: **domain-cross-asset-correlation-regimes.md**
- Linkage matrix đầy đủ: **domain-cross-asset-linkage-matrix-vn.md**
- Regime anchor: **framework-regime-v11.md**
- FX / VND: **domain-fx-usd-vnd.md**
- VN credit cycle: **macro-vn-credit-cycle.md**
- SBV policy (FTQ unwind catalyst): **macro-vn-monetary-policy-nhnn.md**
- Workflow: **workflow-cross-asset-linkage.md**
