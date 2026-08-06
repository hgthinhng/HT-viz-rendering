---
title: "Domain Cross-Asset Transmission Channels — 5 Kênh Truyền Dẫn Đa Tài Sản (Rates, FX, Commodity-CPI, Global Risk, Credit Spread)"
module_type: "domain"
file_name: "domain-cross-asset-transmission-channels.md"
purpose: "Mở rộng §1.4 và §2 của 135-economic-analysis thành 5 kênh truyền dẫn cross-asset cụ thể: rates→equity, FX→equity, commodity→CPI→equity, global risk→EM, credit spread→equity. Mỗi kênh có cơ chế, độ trễ, điều kiện kích hoạt, và VN-specific friction."
primary_triggers:
  - "cross-asset transmission"
  - "kênh truyền dẫn đa tài sản"
  - "rates equity channel"
  - "FX equity channel"
  - "commodity CPI equity"
  - "global risk EM transmission"
  - "credit spread equity"
  - "cross-asset channel VN"
  - "second-order effect"
when_to_use:
  - "Khi phân tích một shock ở tài sản A ảnh hưởng đến tài sản B qua cơ chế nào, độ trễ bao lâu."
  - "Khi build scenario: 'nếu Fed cut 50bp, VN-Index phản ứng ra sao' — phải đi qua các kênh."
  - "Khi đánh giá second-order và third-order effect của một event."
  - "Khi cross-check Diebold-Yilmaz spillover bằng mechanism analysis."
when_not_to_use:
  - "Không dùng cho correlation analysis thuần — đây là mechanism, không phải statistical."
  - "Không dùng cho single-asset deep-dive (dùng domain-equity-vn hoặc domain-fx-usd-vnd)."
  - "Không dùng thay thế framework-regime-v11 — transmission channel vận hành trong regime, không override regime."
related_modules:
  - "framework-regime-v11.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
  - "domain-cross-asset-correlation-regimes.md"
  - "domain-cross-asset-risk-on-off.md"
  - "macro-vn-transmission-channels.md"
  - "workflow-cross-asset-linkage.md"
  - "domain-fx-usd-vnd.md"
authoritative_citations:
  - "Mishkin, F. S. The Transmission Mechanism and the Role of Asset Prices in Monetary Policy (2001)."
  - "Rey, H. Dilemma not Trilemma: Global Financial Cycle and Monetary Policy Independence (2015)."
  - "Diebold, F. X. and Yilmaz, K. Better to Give than to Receive: Predictive Directional Measurement of Volatility Spillovers (2012)."
  - "Bekaert, G., Hoerova, M., and Lo Duca, M. Risk, Uncertainty and Monetary Policy (2013)."
output_owner: "Analytical lens only; output contract thuộc workflow-cross-asset-linkage.md hoặc workflow-deep-dive.md."
---

# Domain Cross-Asset Transmission Channels — Kênh truyền dẫn đa tài sản

Purpose: Cung cấp 5 kênh truyền dẫn cross-asset làm backbone cho mọi phân tích "shock ở A ảnh hưởng đến B như thế nào". Mở rộng Khung Phân tích 7 tầng của 135-economic-analysis (đặc biệt Tầng 4 — Kênh truyền dẫn) thành framework vận hành cụ thể cho VN 2026.

Trigger keywords: cross-asset transmission, kênh truyền dẫn đa tài sản, rates to equity, FX to equity, commodity CPI, global risk transmission, credit spread equity, second-order effect, third-order effect.

---

## 1. NGUYÊN TẮC CHUNG

Mỗi transmission channel có 4 thuộc tính bắt buộc:

| Thuộc tính | Ý nghĩa | Ví dụ |
|---|---|---|
| **Cơ chế** | Chuỗi nhân quả cụ thể | Fed cut → UST yield giảm → DXY yếu → USD/VND áp lực giảm → FII inflow VN → VN-Index bid |
| **Độ trễ** | Thời gian từ shock A → B | Rates → FX: 1-5 ngày; FX → equity: 1-3 tuần; FX → CPI: 1-2 quý |
| **Điều kiện kích hoạt** | Regime / state cần để channel mạnh | Rates→FX channel mạnh khi global cycle synchronized, yếu khi decoupling |
| **VN-specific friction** | Cái gì làm channel yếu ở VN | Capital control, FOL, retail dominance, SBV intervention |

Quy tắc: **luôn nêu đủ 4 thuộc tính** khi invoke một channel. Không kết luận "Fed cut → VN tăng" mà không đi qua chuỗi cụ thể.

---

## 2. KÊNH 1 — RATES → EQUITY

### 2.1 Cơ chế

Chuỗi nhân quả từ global rates (US 10Y, US 10Y real yield) đến VN equity:

```
US 10Y yield ↓ → DXY ↓ → USD/VND áp lực ↓ → FII flow VN ↑ →
                    → US equity multiple ↑ (global beta) →
                    → EM equity beta ↑ → VN-Index multiple ↑
US 10Y real yield ↓ → Gold bid → VN retail wealth effect (gold tích trữ)
US 10Y real yield ↓ → EM discount rate ↓ → VN equity DCF multiple ↑
```

Và qua VN domestic:
```
Fed dovish → SBV dư địa cắt lãi suất → VN 10Y yield ↓ → VN equity discount rate ↓
SBV cắt lãi suất → chi phí vốn DN ↓ → earnings forecast ↑ (lag 2-4 quý)
SBV cắt lãi suất → deposit rate ↓ → tiền từ tiết kiệm sang cổ phiếu
```

### 2.2 Độ trễ

| Sub-channel | Lag |
|---|---|
| UST → DXY | 1-3 ngày |
| DXY → USD/VND spot | 1-5 ngày (nếu SBV không can thiệp) |
| USD/VND → FII flow VN | 1-3 tuần |
| FII flow → VN-Index | 1-4 tuần |
| Fed → SBV policy response | 1-3 tháng |
| SBV rate → VN lending rate | 2-4 quý (xem macro-vn-transmission-channels.md) |

### 2.3 Điều kiện kích hoạt

- **Mạnh**: khi regime Synchronized Easing (Fed + SBV cùng cắt), RORO Risk-On.
- **Yếu**: khi Fed cut nhưng SBV không dư địa (VND stress, CPI gần trần).
- **Đảo chiều**: khi Fed cut nhưng là "bad news" (recession priced in) → VN equity có thể giảm dù rate giảm.

### 2.4 VN-specific friction

- FOL scarcity: FII có thể muốn mua nhưng FOL full ở VCB, FPT, MWG → premium scarcity.
- Margin rule: khi retail margin cao, rate cut không kích thích thêm mà trigger margin call nếu stress.
- Ownership ratio: blue-chip phần lớn sở hữu bởi tổ chức lớn → rate sensitivity khác SME.

---

## 3. KÊNH 2 — FX → EQUITY

### 3.1 Cơ chế

```
USD/VND ↑ (VND yếu) →
  Kênh A (exporter): doanh thu USD / chi phí VND → margin ↑ → equity exporter bid
  Kênh B (importer): chi phí USD / doanh thu VND → margin ↓ → equity importer pressure
  Kênh C (FII): VND yếu → FII fear further weakness → outflow → equity sell
  Kênh D (CPI): nếu VND yếu persistent → CPI ↑ → SBV tighten → equity discount rate ↑
```

### 3.2 Phân loại ngành theo FX sensitivity

| Ngành | FX sensitivity (VND yếu) | Mechanism |
|---|---|---|
| Thủy sản (VHC, MPC) | Positive | 70-80% doanh thu USD |
| Dệt may (TCM, GMC) | Positive | USD revenue, VND cost |
| Thép (HPG) | Mixed | Bán trong nước VND nhưng nguyên liệu USD |
| Điện (POW, PC1) | Negative | Nợ USD lớn |
| BĐS (VHM, NVL) | Negative | Nợ USD + retail affordability ↓ |
| Bán lẻ (MWG, PNJ) | Negative | CPI pressure → sức mua ↓ |
| Dầu khí (GAS, PVS) | Positive | USD revenue |

### 3.3 Độ trễ

- FX spot → exporter P&L: 1-2 quý (translation + hedging lag).
- FX → CPI: 2-4 quý (passthrough rate VN ~0.15-0.25 cho 1% VND depreciation).
- FX → SBV response: 2-6 tuần nếu cross threshold can thiệp.

### 3.4 VN-specific friction

- SBV band (±5%) → spot FX move bị cap → transmission qua NDF thay vì spot.
- Remittance (~USD 15-16 tỷ) và FDI disbursement làm damping factor cho VND pressure.
- Capital control mềm: foreign investor không thể hedge VND bằng FX forward dễ dàng → risk premium.

---

## 4. KÊNH 3 — COMMODITY → CPI → EQUITY

### 4.1 Cơ chế

```
Oil ↑ → VN CPI transport + food (~20% basket) ↑ →
  Kênh A: Real income ↓ → consumption ↓ → retail equity pressure
  Kênh B: PPI ↑ → manufacturing margin ↓
  Kênh C: SBV tighten if CPI >4% target → equity discount rate ↑
  Kênh D (nếu VN là net importer): trade deficit ↑ → FX pressure ↑
```

### 4.2 Commodity-CPI passthrough VN

| Commodity | CPI weight (VN basket) | Passthrough elasticity | Lag |
|---|---|---|---|
| Oil / gasoline | ~3.5% direct + indirect transport | 0.3-0.5 cho 10% oil move | 1-3 tháng |
| Rice | ~8% | 0.4-0.6 | 1-2 tháng |
| Pork | ~4% | 0.5-0.7 | 2-4 tháng (African Swine Fever lịch sử) |
| Coffee | ~0.5% | 0.2-0.3 | 1-2 tháng |
| Electricity / fuel | ~4% | Depends on EVN price adjustment (admin lag) | 3-12 tháng |
| Steel / construction | Indirect | 0.1-0.2 qua BĐS/infrastructure | 2-4 quý |

### 4.3 VN-specific friction

- Giá xăng admin (Bộ Công Thương điều chỉnh 15-ngày một lần) → smooth passthrough.
- EVN price adjustment politically constrained → lag 6-12 tháng cho điện.
- Rice export ban (nếu có) → decouple giá nội địa khỏi global.

---

## 5. KÊNH 4 — GLOBAL RISK → EM (→ VN)

### 5.1 Cơ chế (Rey Global Financial Cycle)

```
VIX ↑ / DXY ↑ / Global risk-off →
  Capital flow pull-back từ EM →
  EM FX depreciation →
  EM central bank tighten (defend FX) hoặc cut (defend growth) — dilemma →
  EM equity sell-off →
  VN (part of Asia EM) impact via: FII outflow, USD/VND pressure, global beta
```

Rey (2015) "Dilemma not Trilemma": EM không thể độc lập chính sách khi Global Financial Cycle turn. VN là một case — khi Fed tighten, SBV buộc phải tighten theo dù domestic condition không require.

### 5.2 Độ trễ

- VIX spike → EM equity: 1-5 ngày (high beta).
- VIX spike → EM FX: 1-10 ngày.
- EM FX stress → central bank response: 1-4 tuần.
- Global risk-off → VN FII outflow: 1-3 tuần.
- Global risk-off → VN domestic retail response: 3-8 tuần (information lag).

### 5.3 Differentiation factors

| Yếu tố | Làm VN less sensitive | Làm VN more sensitive |
|---|---|---|
| Current account | Surplus (pre-2025) | Deficit (cyclical) |
| FX reserve | >3 tháng nhập khẩu | <3 tháng |
| External debt | Thấp (~40% GDP) | Cao (post-SOE) |
| Capital control | Mềm but effective | Nếu bị phá vỡ |
| Trade linkage | Diversified | Concentrated (US risk) |

### 5.4 VN-specific friction

- Capital control mềm làm FII outflow bị chậm lại so với Indonesia, Philippines.
- Retail dominance → domestic bid có thể absorb FII sell short-term.
- SBV reserve ~USD 80-90 tỷ (2025) → đệm ~3-4 tháng nhập khẩu, đủ defend VND trong stress vừa.

---

## 6. KÊNH 5 — CREDIT SPREAD → EQUITY

### 6.1 Cơ chế

```
US HY spread ↑ → EM corporate funding cost ↑ →
VN corporate bond primary market stress →
Refinancing risk ↑ (BĐS, infrastructure) →
  Kênh A: Equity của DN có bond maturity wall ↓
  Kênh B: Bank equity ↓ (nợ xấu tiềm tàng)
  Kênh C: Discount rate ↑ chung cho EM → multiple contract
```

### 6.2 VN credit spread linkage

VN corporate bond spread có 3 layer:
1. **Global EM layer**: US HY + EMBI+ → benchmark cho EM corporate.
2. **Asia layer**: Asia HY (Indonesia, Philippines) → regional risk sentiment.
3. **VN domestic layer**: bond default rate, BĐS restructuring, bank exposure.

Spread widening ở bất kỳ layer nào transmit đến equity — nhưng speed và magnitude khác nhau.

### 6.3 Độ trễ

- US HY → Asia HY: 1-2 tuần.
- Asia HY → VN corporate bond yield: 2-6 tuần (thanh khoản thấp).
- VN corporate bond stress → equity của issuer: 1-3 tháng (thường visible qua margin call trước).

### 6.4 VN-specific friction

- Secondary market VN corporate bond thanh khoản thấp → spread widening thường lagged và discontinuous.
- "Extend and pretend" culture → spread không phản ánh real credit quality.
- Retail holder ~30% corporate bond → panic selling có thể trigger cascade nếu narrative shift.

---

## 7. QUY TRÌNH ÁP DỤNG TRONG RESEARCH

1. **Identify shock**: biến nào đang move bất thường?
2. **Map channels**: shock này transmit qua 1-5 channels nào?
3. **Lag analysis**: trạng thái hiện tại ở đâu trên timeline transmission?
4. **Friction check**: VN-specific friction nào đang active?
5. **Regime overlay**: channel này strong hay weak trong regime hiện tại (framework-regime-v11)?
6. **Second-order**: channel bật channel nào tiếp theo?
7. **Signposts**: biến cần theo dõi để confirm transmission đang diễn ra?

---

## 8. CROSS-REFERENCES

- Regime master: **framework-regime-v11.md**
- Linkage matrix chi tiết: **domain-cross-asset-linkage-matrix-vn.md**
- Correlation state: **domain-cross-asset-correlation-regimes.md**
- RORO state: **domain-cross-asset-risk-on-off.md**
- VN monetary transmission: **macro-vn-transmission-channels.md**
- FX detail: **domain-fx-usd-vnd.md**
- Workflow: **workflow-cross-asset-linkage.md**
