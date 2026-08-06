---
title: "Domain Cross-Asset Risk-On / Risk-Off — RORO Indicators, Asset Behavior per Regime, VN-Specific Calibration"
module_type: "domain"
file_name: "domain-cross-asset-risk-on-off.md"
purpose: "Codify cách OPVIA đọc chế độ risk-on / risk-off (RORO) đa tài sản: bộ indicator global + VN-specific, hành vi điển hình của từng asset class theo regime, và cách calibrate RORO cho thị trường VN non-trẻ với cấu trúc đặc thù (FOL, capital control mềm, retail dominance)."
primary_triggers:
  - "risk-on risk-off"
  - "RORO indicator"
  - "risk appetite"
  - "khẩu vị rủi ro"
  - "risk-on regime"
  - "risk-off VN"
  - "flight to quality trigger"
  - "VIX VN proxy"
  - "RORO score"
when_to_use:
  - "Khi xác định 'thị trường đang risk-on hay risk-off' cho daily brief."
  - "Khi cần anchor asset allocation analysis vào risk regime."
  - "Khi phân tích FII flow vào/ra VN, định vị VND, và corporate bond spread."
  - "Khi cross-check regime classification của framework-regime-v11 bằng RORO score."
when_not_to_use:
  - "Không dùng làm signal trade — RORO là lens diagnostic."
  - "Không dùng đơn biến: VIX thấp không đủ kết luận risk-on nếu DXY tăng và oil giảm."
  - "Không dùng cho tài sản có liquidity kém (penny VN, corporate bond inactive)."
related_modules:
  - "framework-regime-v11.md"
  - "domain-cross-asset-correlation-regimes.md"
  - "domain-cross-asset-flight-to-quality.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
  - "workflow-cross-asset-linkage.md"
  - "domain-fx-usd-vnd.md"
  - "macro-vn-credit-cycle.md"
authoritative_citations:
  - "Bekaert, G., Hoerova, M., and Lo Duca, M. Risk, Uncertainty and Monetary Policy (2013)."
  - "Rey, H. Dilemma not Trilemma: Global Financial Cycle and Monetary Policy Independence (2015)."
  - "Adrian, T. and Shin, H. S. Liquidity and Leverage (2010)."
  - "Forbes, K. and Warnock, F. Capital Flow Waves (2012)."
output_owner: "Analytical lens only; pair với workflow-daily-brief.md hoặc workflow-cross-asset-linkage.md cho output contract."
---

# Domain Cross-Asset Risk-On / Risk-Off — Khẩu vị rủi ro đa tài sản

Purpose: Đo lường và phân loại risk appetite của thị trường toàn cầu + VN theo một score tổng hợp. RORO là **lens trung gian** giữa regime classification (framework-regime-v11) và asset-specific analysis (domain-equity-vn, domain-fx, domain-fi). Khi RORO chuyển state, gần như mọi asset đều reprice — biết sớm RORO shift là lợi thế tốc độ lớn nhất trong cross-asset research.

Trigger keywords: risk-on, risk-off, RORO score, khẩu vị rủi ro, VIX, DXY breadth, EM sell-off, FII flow VN, corporate bond spread, gold bid, USD bid.

---

## 1. KHÁI NIỆM — RORO LÀ GÌ, KHÔNG LÀ GÌ

### 1.1 Định nghĩa operational

RORO không phải binary on/off. Nó là một **spectrum** từ `Risk-On mạnh` đến `Risk-Off mạnh`, với các state trung gian: `Risk-On drift`, `Neutral`, `Risk-Off drift`, `Panic`.

| RORO State | Điểm số tổng hợp (0-100) | Đặc điểm |
|---|---|---|
| Risk-On mạnh | 75-100 | VIX <15, DXY yếu, credit spread tight, gold bid yếu, EM inflow |
| Risk-On drift | 60-75 | Multiple tín hiệu risk-on nhưng chưa đồng pha |
| Neutral | 40-60 | Mixed signals, không có xu hướng rõ |
| Risk-Off drift | 25-40 | USD bid, credit spread widening, EM outflow khởi đầu |
| Risk-Off mạnh | 10-25 | VIX >25, DXY mạnh, EM sell-off, FII rút |
| Panic | 0-10 | "Correlation goes to 1", margin call cascade, central bank intervention |

### 1.2 RORO không phải regime

RORO là **một input** cho regime classification, không phải bản thân regime. Một period có thể Risk-On nhưng vẫn thuộc regime "Tightening Stress" (VN bị bao vây chính sách dù global risk-on). Ngược lại, Risk-Off global không nhất thiết đẩy VN vào regime Deleveraging nếu SBV đang bơm thanh khoản.

---

## 2. BỘ INDICATOR RORO — GLOBAL

### 2.1 Core RORO indicators (7 biến)

| # | Indicator | Ngưỡng Risk-On | Ngưỡng Risk-Off | Trọng số OPVIA |
|---|---|---|---|---|
| 1 | **VIX** (S&P 500 vol) | <15 | >25 | 0.20 |
| 2 | **MOVE index** (UST vol) | <90 | >130 | 0.10 |
| 3 | **DXY** level + momentum | yếu + DXY giảm | mạnh + DXY tăng | 0.15 |
| 4 | **US HY credit spread** (HYG) | <350bp | >550bp | 0.15 |
| 5 | **EM credit spread** (EMBI+) | <300bp | >500bp | 0.10 |
| 6 | **Copper / Gold ratio** | tăng | giảm | 0.10 |
| 7 | **10Y UST yield** (direction) | tăng mạnh = growth | giảm mạnh = flight | 0.10 |
| 8 | **EM equity breadth** (MSCI EM % above 200MA) | >70% | <30% | 0.10 |

Composite score = weighted sum, scale 0-100.

### 2.2 Second-tier indicators (cross-check)

- **CNY volatility** (USD/CNH implied): CNH vol tăng mạnh = risk-off Asia.
- **BDI (Baltic Dry Index)** direction: drop mạnh = demand shock risk-off.
- **Japanese yen** (USD/JPY): JPY strengthen = risk-off (unwind carry).
- **Bitcoin / tech stocks** (pure beta): collapse = liquidity stress.
- **Gold momentum**: gold bid tăng tốc = flight-to-quality (xem domain-cross-asset-flight-to-quality.md).

---

## 3. RORO CALIBRATION CHO VN

### 3.1 Tại sao VN cần calibration riêng

Thị trường VN có 3 đặc thù làm RORO global không đủ:

1. **Capital control mềm**: FII flow VN bị chi phối bởi FOL, margin rules, short-selling restriction — không phản ứng 1:1 với RORO global.
2. **Retail dominance** (~85% volume): tâm lý retail VN có thể decouple khỏi global risk sentiment trong short-term.
3. **Currency managed**: USD/VND không float tự do, NHNN có thể absorb shock → indicator FX không phản ánh ngay stress.

### 3.2 VN-specific RORO indicators (8 biến)

| # | Indicator | Risk-On VN | Risk-Off VN | Trọng số |
|---|---|---|---|---|
| 1 | **VN-Index breadth** (% above 50MA) | >60% | <30% | 0.15 |
| 2 | **Margin balance** (top 20 brokers) | tăng + accel | giảm + contract | 0.15 |
| 3 | **Foreign net buy/sell** (HOSE weekly) | net buy 3w+ | net sell 3w+ | 0.15 |
| 4 | **USD/VND premium** (NDF - spot) | <1% annualized | >3% annualized | 0.15 |
| 5 | **Corporate bond yield** (AAA 5Y) | tight spread | widen >100bp | 0.10 |
| 6 | **Gold/VND retail premium** | premium <3% | premium >7% | 0.10 |
| 7 | **VN-Index turnover/float** | >1% daily | <0.4% daily | 0.10 |
| 8 | **Interbank ON rate** vs SBV target | on target | >200bp above | 0.10 |

VN RORO composite = weighted sum, scale 0-100.

### 3.3 Quy tắc kết hợp Global + VN RORO

| Global RORO | VN RORO | Kết luận |
|---|---|---|
| Risk-On mạnh | Risk-On mạnh | Regime Synchronized Risk-On — đồng pha, ít nhiễu |
| Risk-On mạnh | Neutral/Risk-Off | **Divergence** — VN có structural headwind (capital control, FOL full, credit tight). Cần deep-dive nguyên nhân |
| Risk-Off mạnh | Risk-On | **Anomaly**: retail euphoria độc lập. Dễ gãy đột ngột khi global stress transmit qua |
| Risk-Off mạnh | Risk-Off mạnh | Regime Synchronized Risk-Off — stress kép global + VN, highest risk |
| Neutral | Risk-Off drift | VN leading indicator — thường báo hiệu domestic credit issue trước khi global ảnh hưởng |

---

## 4. HÀNH VI ASSET CLASS THEO RORO

### 4.1 Matrix tổng hợp

| Asset | Risk-On mạnh | Risk-Off mạnh | Panic |
|---|---|---|---|
| **VN-Index** | Tăng, breadth rộng, retail inflow | Sell-off, concentrate blue-chip | Gap down, circuit breaker |
| **VND** (spot) | Stable / mạnh nhẹ | Yếu, SBV can thiệp | SBV bán reserve, NDF blow out |
| **VN 10Y yield** | Tăng nhẹ (growth pricing) | Tăng mạnh (stress premium) hoặc giảm (flight to TPCP domestic) | Ambiguous — phụ thuộc NHNN |
| **Gold** | Flat/weak | Bid | Strong bid, retail premium >7% |
| **Oil** | Bid (demand) | Weak (demand fear) | Crash hoặc spike (supply shock) |
| **DXY** | Weak | Strong | Very strong (safe haven) |
| **CNY** | Stable/strong | Weak | PBOC intervention |
| **Copper** | Strong | Weak | Collapse |
| **US 10Y real yield** | Rise | Fall (flight) | Whipsaw |
| **Asia HY spread** | Tight | Wide | Blow out |

### 4.2 "Correlation goes to 1" trong Panic

Trong panic, almost all risk asset giảm đồng thời. Chỉ có **USD cash, UST (sometimes), gold** là safe haven. VN retail thường không nhận ra panic global trong 1-2 tuần đầu do information lag — đây là window dangerous cho portfolio VN long-only.

---

## 5. QUY TRÌNH ÁP DỤNG — DAILY BRIEF

1. **Global RORO score**: tính từ 8 indicator core → scale 0-100.
2. **VN RORO score**: tính từ 8 indicator VN → scale 0-100.
3. **Divergence check**: |Global - VN| > 25 điểm → flag cho deep-dive.
4. **Map vào regime**: dùng framework-regime-v11.md §regime classification.
5. **Asset behavior table**: list expected vs actual — mismatch = signal.
6. **Signposts**: liệt kê 3-5 biến cần theo dõi để xác nhận/phủ định RORO state.

---

## 6. FAILURE MODES — KHI RORO SAI

- **2020 Q1 COVID**: RORO indicator global chậm 1-2 tuần so với panic thực. Gold ban đầu bán do margin call trước khi bid.
- **2022 Q1 Ukraine**: oil tăng nhưng VIX chưa đủ cao để trigger risk-off mạnh — geopolitical premium làm méo indicator.
- **2024 VN corporate bond crisis**: VN RORO Risk-Off rõ nhưng Global RORO Risk-On → divergence persistent 6 tháng. Ai dùng global RORO để anchor VN đã mis-time severely.

---

## 7. CROSS-REFERENCES

- Regime master: **framework-regime-v11.md**
- Correlation regime: **domain-cross-asset-correlation-regimes.md**
- Flight-to-quality: **domain-cross-asset-flight-to-quality.md**
- Linkage matrix: **domain-cross-asset-linkage-matrix-vn.md**
- VN transmission: **macro-vn-transmission-channels.md**
- FX detail: **domain-fx-usd-vnd.md**
- Credit cycle VN: **macro-vn-credit-cycle.md**
- Workflow: **workflow-cross-asset-linkage.md**
