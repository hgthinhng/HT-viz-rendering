---
title: "Framework Regime v1.1 — OPVIA Joint Global-VN Multi-Asset Regime Classification"
module_type: "framework"
file_name: "framework-regime-v11.md"
purpose: "Codify khung phân loại regime đa tài sản v1.1 của OPVIA — 5 regime joint global-VN với 21 biến observable, 4 quy tắc transition, mapping vận hành vào domain module và output framing. Khung in-house, dùng làm trục anchor cho mọi research multi-asset của OPVIA Sigma."
primary_triggers:
  - "OPVIA regime"
  - "regime framework v1.1"
  - "regime hiện tại"
  - "regime shift"
  - "phân loại regime VN"
  - "joint global-VN regime"
  - "RORO indicator VN"
  - "tightening stress"
  - "deleveraging regime"
when_to_use:
  - "Khi user hỏi 'regime hiện tại là gì', 'có regime shift không', hoặc cần classify một period lịch sử."
  - "Khi cần anchor một deep-dive (equity, FX, FI, commodity) vào bối cảnh regime."
  - "Khi build daily brief, regime block là item bắt buộc."
  - "Khi cần xác định module domain nào nên kích hoạt đầu tiên cho phân tích."
when_not_to_use:
  - "Không dùng để dự báo giá hoặc đưa khuyến nghị mua/bán."
  - "Không dùng cho step-function shock (chiến tranh, đại dịch, cấm vận) — các shock này có scenario riêng theo Rule D Veto, không thuộc regime thông thường."
  - "Không dùng làm khung valuation độc lập — phải pair với domain-equity-vn-valuation.md hoặc framework valuation phù hợp."
related_modules:
  - "domain-macro-vn-liquidity.md"
  - "domain-fx-usd-vnd.md"
  - "domain-cross-asset-linkage.md"
  - "domain-equity-vn-valuation.md"
  - "domain-equity-vn-forensic-accounting.md"
  - "framework-thakor-yu-2024.md"
  - "framework-kashyap-stein-bank-lending.md"
  - "framework-geanakoplos-leverage-cycle.md"
  - "framework-dickinson-mauboussin.md"
  - "workflow-daily-brief.md"
  - "workflow-regime-shift-alert.md"
  - "core-voice-and-safety.md"
authoritative_citations:
  - "OPVIA in-house Regime Framework v1.1 (OPVIA, 2025-2026)."
  - "Borio, C. The financial cycle and macroeconomics."
  - "Brunnermeier, M. K. and Pedersen, L. H. Funding liquidity and market liquidity."
  - "Geanakoplos, J. The leverage cycle."
  - "Mundell-Fleming open-economy trilemma literature."
output_owner: "Analytical framework only; never owns final output format. Output framing được xác định bởi workflow-daily-brief.md, workflow-deep-dive.md, hoặc workflow-regime-shift-alert.md."
status: "v1.1 DRAFT — codified from Wave 2 E1 strawman; AWAITING OPVIA REVIEW for thresholds + open questions in §11."
---

# Framework Regime v1.1 — OPVIA Joint Global-VN Multi-Asset Regime Classification

Purpose: Cung cấp trục anchor regime cho toàn bộ hệ thống OPVIA Sigma. Khung phân loại 5 regime joint global-VN, kết hợp 3 layer biến số (Global / VN Macro / Cross-asset) với 4 quy tắc transition (Breach / Persistence / Cross-validation / Veto). Khung này là **diagnostic**, không phải predictive — mục tiêu là **classify hiện trạng** và **detect shift**, không dự báo giá.

Trigger keywords: regime VN, regime framework, joint regime, OPVIA regime v1.1, regime shift, RORO, tightening stress, deleveraging, recovery cycle, late cycle.

---

## 1. Authors & Source

- **Tác giả khung:** OPVIA — OPVIA Research & Advisory.
- **Phiên bản:** v1.1, codified ngày 2026-04-19 từ Wave 2 E1 reverse-engineering strawman (Kimi CLI).
- **Tiền thân:** 4-regime taxonomy trong `125-macro-micro.md` (Phục hồi / Tăng trưởng / Đỉnh / Suy thoái) — mở rộng thành 5 regime để tách biệt "đỉnh chu kỳ overheating chưa stress" với "siết chặt ép buộc + capital flight".
- **Tham chiếu học thuật:** Borio (financial cycle), Brunnermeier-Pedersen (funding/market liquidity), Geanakoplos (leverage cycle), Mundell-Fleming (open-economy trilemma).
- **Trạng thái:** DRAFT v1.1 — các threshold đang chờ OPVIA calibrate trong Sprint 0 session #1 (xem §11).
- **Bậc bằng chứng:** [Bậc 3 — Bằng chứng sơ bộ] / [Q2 — Có cơ sở]. Mọi regime call dùng khung này phải gắn shelf life rõ ràng theo Safety Policy Rule 5.

---

## 2. Core Thesis

OPVIA phân loại bối cảnh thị trường thành **5 regime joint global-VN**. Mỗi regime là một **tổ hợp ổn định** của:

1. **Macro forcing toàn cầu** (Fed stance + DXY + UST + commodity cycle),
2. **Cross-asset behavior** (correlation, RORO, leadership, volatility), và
3. **VN-specific overlay** (NHNN action, credit cycle VN, VND dynamics, capital account VN).

**Bốn nguyên tắc nền:**

- **Joint, không độc lập.** VN là EM nhỏ, open economy với trilemma constraint thực thi → không thể tách regime VN khỏi DXY + Fed + UST. Mọi regime call phải đồng thời check global anchor + VN-specific overlay.
- **Pattern, không single trigger.** Regime được định nghĩa bằng **pattern đồng thời** của ≥3 biến qua ≥2 layer, không phải 1 biến trigger. Chống lại confirmation bias do single indicator.
- **Probabilistic, không binary.** Regime call là phán đoán xác suất, không phải sự thật binary. Dùng qualitative confidence (low/medium/high), không pseudo-precision %.
- **Shelf life rõ ràng.** Regime call có shelf life **1-2 tuần trong volatile regime** (R3, R4) và **2-4 tuần trong stable regime** (R2, R5). Hết shelf life phải re-evaluate, không carry-over passive.

**Vai trò trong OPVIA Sigma:** Regime không phải output cuối — là **anchor context** để các module domain (equity, FX, FI, commodity) chọn đúng valuation approach, đúng red flag focus, đúng module activation. Mỗi deep-dive bắt đầu bằng câu "Regime hiện tại là gì?" trước khi đi vào single-name analysis.

---

## 3. Key Variables / Mechanisms — 3-Layer Variable System

Regime được định nghĩa bằng **21 biến observable** chia thành 3 layer. Mỗi biến có ngưỡng theo regime (xem §5 ma trận chi tiết).

### 3.1 Global Layer (6 biến) — Anchor toàn cầu

| # | Biến | Vai trò | Source |
|---|---|---|---|
| G1 | **DXY trend** (level + 50dma slope) | Anchor chính cho EM FX, đặc biệt VND | ICE / Bloomberg |
| G2 | **UST 10Y level + direction** (3M change) | Anchor cost of capital toàn cầu, EM rates anchor | FRED / Treasury.gov |
| G3 | **Fed stance** (cut / hold / hawkish / hiking) | Forward driver cho DXY + UST | FOMC dot plot, statements |
| G4 | **Oil Brent** (level + 3M change) | Driver inflation toàn cầu, sensitivity đặc biệt với VN (net importer) | EIA / Brent futures |
| G5 | **Gold real yield** (gold price vs UST 10Y real) | Proxy cho stress + USD strength | Bloomberg / WGC |
| G6 | **EM risk appetite** (EM equity ETF flow + EM CDS spread) | Proxy capital flow EM, leading indicator outflow VN | EPFR / CDX |

**Mechanism note:** G1-G3 là cluster (DXY ≈ f(Fed, UST diff)). Khi G3 shift (Fed pivot), thường G1-G2 follow trong 1-3 tháng. G4 là exogenous driver (geopolitics, OPEC) → có thể độc lập với G1-G3. G5-G6 là confirming variables, không leading.

### 3.2 VN Macro Layer (9 biến) — VN-specific overlay

| # | Biến | Vai trò | Source |
|---|---|---|---|
| V1 | **NHNN OMO net** (weekly net inject/withdraw) | Tín hiệu chính sách tiền tệ VN realtime | NHNN daily |
| V2 | **VND vs DXY** (q/q + yoy + intervention proxy) | Rate differential + capital flow + intervention | SBV reference rate |
| V3 | **Credit growth YoY** (vs SBV target) | Chu kỳ tín dụng VN | NHNN monthly |
| V4 | **Real interest rate** (lãi suất cho vay 10Y - CPI yoy) | Tightness thực tế | NHNN + GSO |
| V5 | **CPI yoy** (headline + core) | Pressure tiền tệ NHNN | GSO monthly |
| V6 | **IIP** (Industrial Production Index, yoy 3M ma) | Activity proxy realtime | GSO monthly |
| V7 | **Trade balance** (3M rolling, $bn) | BoP + driver VND | Vietnam Customs |
| V8 | **FDI disbursement** (YTD $bn vs prior year) | Capital account stability | MPI quarterly |
| V9 | **Capital account net** (BoP financial account) | FII flow + FDI + debt flow | SBV BoP quarterly |

**Mechanism note:** V1-V2 là realtime (daily/weekly) — leading. V3-V5 là monthly với 1-2 tháng lag. V6-V9 là quarterly với 2-3 tháng lag — confirming, không leading. Khi V1-V2 shift trước V3-V9 → early warning. Khi V1-V2 confirm V3-V9 → regime shift xác nhận.

### 3.3 Cross-Asset Behavior Layer (6 biến) — Market microstructure

| # | Biến | Vai trò | Source |
|---|---|---|---|
| C1 | **VN-Index beta to MSCI EM** (60d rolling) | Mức độ co-move với EM cycle | Bloomberg / Reuters |
| C2 | **Bond-equity correlation VN** (60d, VNI vs VN10Y) | Stable regime indicator (âm = risk-on, dương = stress) | HOSE + bond data |
| C3 | **VN-Index vs VCB ratio** (60d) | Bank sector leadership — VCB lead = recovery, VCB lag = stress | HOSE |
| C4 | **RORO ratio** (cyclical vs defensive sector ratio, 60d) | Risk-on / risk-off internal rotation | HOSE sector indices |
| C5 | **Volatility regime** (VNI 30d realized vol) | Regime classifier (low/mid/high vol) | HOSE |
| C6 | **Foreign net buy** (5d rolling, $mn) | FII positioning realtime | HOSE/HNX foreign data |

**Mechanism note:** C1-C2 là regime classifier dài hạn (slow-moving). C3-C4 là rotation indicator (medium speed). C5-C6 là realtime stress indicator (fast). C2 là biến quan trọng nhất — bond-equity correlation đổi dấu là **definitive signal** của regime shift global, nhưng ở VN có thể không đổi dấu rõ rệt do bond market shallow (xem critique §8.3).

---

## 4. 5-Regime Taxonomy

Mã quy ước: **R1 → R2 → R3 → R4 → R5 → R1** là sequence "chuẩn" của một full cycle. Trong thực tế, transition có thể skip (R2 → R4 trong sudden stop), nhưng R4 → R1 trực tiếp **rất hiếm** (thường phải qua R5).

| Mã | Tên VN | Tên EN | Bản chất 1 dòng |
|---|---|---|---|
| **R1** | Phục hồi / Nới lỏng có hiệu quả | Recovery / Risk-on / Easing | Risk-on + Easing + Growth inflection từ đáy |
| **R2** | Tăng trưởng bền vững | Steady Growth / Goldilocks / Mid-cycle | Risk-on + Policy neutral + Stable expansion |
| **R3** | Đỉnh chu kỳ / Quá nhiệt | Late Cycle / Overheating | Risk-on fading + Tightening signals + Inflation rising |
| **R4** | Siết chặt / Stress | Tightening Stress / Risk-off / Capital Flight | Risk-off + Active tightening + FX pressure + Forced deleveraging |
| **R5** | Deleveraging / Đáy chu kỳ | Deleveraging / Post-stress repair / Bottom | Risk-off + Easing nhưng không hiệu quả + Balance sheet repair |

### 4.1 R1 — Recovery / Easing / Growth-positive

- **Defining signature:** Fed cut + DXY giảm dưới 102 + UST 10Y giảm dưới 3.5% + NHNN bơm OMO net + credit growth tăng tốc từ đáy + VN-Index outperform MSCI EM + bond-equity correlation âm.
- **Typical duration:** 6-12 tháng (full recovery cycle).
- **Entry conditions:** Từ R5 — credit growth chạm đáy và bắt đầu accelerate, NHNN cut rate, margin balance bottom + bắt đầu rise, foreign net buy turn positive sau đợt outflow kéo dài.
- **Exit conditions:** Sang R2 khi credit growth ổn định 12-15% và CPI ổn định 2-3.5%; sang R3 nếu credit overshoot >15% nhanh và CPI bắt đầu vượt 3.5%.
- **Historical VN examples:** Q2-Q4 2020 (post-COVID, Fed 0%, DXY <92); Q1-Q2 2023 (post-2022 stress, Fed pause signaled, NHNN giảm OMO rate); 2014 (post-2011-13 deleveraging, NHNN nới rate, BĐS hồi từ đáy).

### 4.2 R2 — Steady Growth / Goldilocks / Mid-cycle

- **Defining signature:** Fed hold + DXY range 102-105 + UST 10Y range 3.5-4.5% + NHNN neutral + credit growth 12-15% + CPI 2-3.5% + VN-Index inline với EM + sector rotation broad + low realized vol.
- **Typical duration:** 12-24 tháng (longest regime trong cycle).
- **Entry conditions:** Từ R1 khi growth + credit ổn định trong 2-3 quý liên tiếp, không có overshoot signal.
- **Exit conditions:** Sang R3 khi CPI vượt 3.5% và credit growth >15% với momentum giảm; sang R4 trực tiếp (rare) nếu external shock (DXY surge >108 trong <2 tuần).
- **Historical VN examples:** 2015-2017 (Yellen hike chậm, DXY range, EM inflow, CPI thấp, credit 15-18%); 2024 ước lượng (Fed hold, credit 12-15%, CPI 2-4%).

### 4.3 R3 — Late Cycle / Overheating

- **Defining signature:** Fed hawkish pivot signaled + DXY firming 105-108 + UST 10Y rising 4.5-5.0% + NHNN signal siết (room BĐS, refinancing rate hike signaled) + credit growth >15% momentum giảm + CPI 3.5-5% + VN-Index inline-to-underperform + bond-equity correlation chuyển dương + sector rotation defensive.
- **Typical duration:** 3-9 tháng (relatively short — tightens into R4 hoặc gentle rotate về R2).
- **Entry conditions:** Từ R2 khi CPI breach 3.5% và credit growth momentum giảm trong 2-3 tháng liên tiếp, NHNN signal hawkish.
- **Exit conditions:** Sang R4 khi DXY >108 + UST >5% + NHNN active tighten + VND mất giá >2.5%; soft landing về R2 nếu Fed pivot dovish + commodity cool xuống.
- **Historical VN examples:** 2021 H2 (Fed "transitory" rhetoric, credit >14%, CPI tăng, NHNN signal siết room BĐS); 2018 Q1-Q3 (Fed hike + DXY firming, NHNN signal siết).

### 4.4 R4 — Tightening Stress / Capital Flight / Risk-off

- **Defining signature:** Fed hiking aggressively (>75bps/qtr) + DXY surge >108 + UST 10Y spike >5% + NHNN tăng lãi suất điều hành + VND mất giá >2.5% + intervention mạnh + credit growth <10% + CPI >5% + VN-Index crash + bond-equity correlation dương mạnh + corp bond freeze + foreign net sell sustained + forced selling margin.
- **Typical duration:** 3-9 tháng (intense, không kéo dài — tightens into R5 hoặc Fed pivot vào R1).
- **Entry conditions:** Từ R3 khi DXY breach 108 + UST breach 5% + NHNN buộc intervention FX; từ R2 trực tiếp nếu sudden stop / external shock.
- **Exit conditions:** Sang R5 khi forced deleveraging xong (margin balance reset thấp, NPL recognition) + Fed pivot pause/cut signaled; sang R1 trực tiếp **rất hiếm** (thường phải qua R5).
- **Historical VN examples:** Q1 2020 (COVID crash, DXY spike, Fed emergency cut, margin cascade — short R4 stress event 6 tuần); Mar-Dec 2022 (Fed 425bps hike, DXY 114, UST >4%, VN-Index -40% peak-to-trough, corp bond freeze); 2011 (post-GFC EM inflation scare, NHNN tăng rate mạnh, NPL ngân hàng tăng).

### 4.5 R5 — Deleveraging / Post-stress Repair / Bottom

- **Defining signature:** DXY volatile peak rồi giảm + UST 10Y collapse <3.5% (safe haven flight) + Fed cut into recession + NHNN inject OMO trở lại nhưng credit không tăng + credit growth ~0% hoặc âm + CPI <2% (demand collapse) hoặc stagflation >5% + NPL recognition ongoing + VN-Index sideways low + thanh khoản thấp + corp bond issuance freeze + margin balance very low.
- **Typical duration:** 6-18 tháng (longest stress regime — balance sheet repair là slow process).
- **Entry conditions:** Từ R4 khi forced selling exhausted + NHNN buộc nới + NPL recognition bắt đầu open; sang trực tiếp từ R3 nếu policy tightening dẫn đến credit freeze nhanh (rare).
- **Exit conditions:** Sang R1 khi credit growth bắt đầu accelerate từ đáy + NHNN OMO net inject ổn định + margin balance bottom + foreign net buy turn positive + PMI bounce >50 — yêu cầu **persistence 10 phiên** vì R5→R1 dễ có dead cat bounce.
- **Historical VN examples:** 2012-2013 (post-2011 stress, NHNN nới nhưng credit không tăng, NPL cao, VAMC thành lập, BĐS đóng băng, "chứng khoán chết"); H2 2022 - Q1 2023 (post-2022 stress, corp bond freeze, BĐS đóng băng — R5 ngắn vì Fed pivot nhanh).

---

## 5. Regime Variable Matrix (Master Reference)

### 5.1 Global Layer thresholds

| Biến | R1 Recovery | R2 Steady | R3 Late Cycle | R4 Stress | R5 Deleveraging |
|---|---|---|---|---|---|
| **G1 DXY trend** | Yếu, <102 | Range 102-105 | Firming 105-108 | Surge >108 | Volatile / peak rồi giảm |
| **G2 UST 10Y** | Giảm <3.5% | Range 3.5-4.5% | Tăng 4.5-5.0% | Spike >5.0% | Collapse <3.5% (safe haven) |
| **G3 Fed stance** | Cut / pause | Neutral / data-dependent | Hawkish pivot signaled | Hiking >75bps/qtr | Cut into recession |
| **G4 Oil Brent** | Stable $65-75 | Range $70-85 | Rising $85-100+ | Volatile >$100 hoặc <$60 | Crash <$60 hoặc supply shock |
| **G5 Gold real yield** | Gold up, real yield down | Range | Gold range, real yield rising | Gold up flight, real yield volatile | Gold up safe haven, real yield collapse |
| **G6 EM risk appetite** | Inflow trở lại | Ổn định | Outflow nhẹ bắt đầu | Outflow mạnh / sudden stop | Outflow chậm lại nhưng FDI freeze |

### 5.2 VN Macro Layer thresholds

| Biến | R1 Recovery | R2 Steady | R3 Late Cycle | R4 Stress | R5 Deleveraging |
|---|---|---|---|---|---|
| **V1 NHNN OMO net** | Net inject mạnh | Cân bằng | Net withdraw nhẹ | Net withdraw mạnh | Net inject lại (ineffective) |
| **V2 VND vs DXY** | Ổn / tăng nhẹ | Mất giá 0.5-1.5% q/q | Mất giá 1.5-2.5% q/q | Mất giá >2.5% q/q + intervention | Mất giá nhanh / siết kiểm soát |
| **V3 Credit growth YoY** | <12% accelerating | 12-15% | >15% momentum giảm | <10% | ~0% hoặc âm |
| **V4 Real rate (lend - CPI)** | Giảm / âm nhẹ | 2-4% | 4-6% | >6% siết thực | Âm sâu hoặc không có ý nghĩa |
| **V5 CPI yoy** | <2% hoặc giảm | 2-3.5% | 3.5-5% | >5% | <2% (demand collapse) hoặc >5% (stagflation) |
| **V6 IIP yoy 3M ma** | Bounce từ <0 → >0 | 6-10% | 10%+ momentum giảm | <3% | <0% sustained |
| **V7 Trade balance** | Surplus phục hồi | Surplus ổn | Surplus narrow | Deficit hoặc shock | Volatile theo demand collapse |
| **V8 FDI disbursement** | Tăng yoy | Ổn yoy | Ổn nhưng new commitment slow | Slowdown rõ | Freeze new commitment |
| **V9 Capital account** | Inflow positive | Balance | Slight outflow | Sustained outflow | Outflow slow but no inflow |

### 5.3 Cross-Asset Layer thresholds

| Biến | R1 Recovery | R2 Steady | R3 Late Cycle | R4 Stress | R5 Deleveraging |
|---|---|---|---|---|---|
| **C1 VNI beta MSCI EM** | High positive (1.0+) | Moderate (0.6-0.9) | Decoupling slight | High again (crash co-move) | Low — VN-specific |
| **C2 Bond-equity corr** | Âm / thấp | Âm hoặc gần 0 | Chuyển dương | Dương mạnh | Dương mạnh →1 |
| **C3 VNI vs VCB ratio** | VCB lead — ratio rising | Stable | VCB lag bắt đầu | VCB crash hardest | VCB sideways low |
| **C4 RORO ratio** | Cyclical lead | Broad | Defensive rotate | Defensive lead mạnh | Defensive grind |
| **C5 Volatility regime** | Low-mid (15-20%) | Low (12-18%) | Mid rising (18-25%) | High (>30%) | Mid (20-25%) |
| **C6 Foreign net buy** | Net buy sustained | Balanced | Net sell start | Net sell heavy | Net sell slow / balanced |

---

## 6. Transition Rules — A / B / C / D

Regime shift là **pattern-based decision**, không phải single-variable trigger. Áp dụng cùng lúc 4 rule.

### 6.1 Rule A — Breach Threshold (số biến vi phạm ngưỡng)

| Layer | Min breach để **cân nhắc** shift | Min breach để **xác nhận** shift |
|---|---|---|
| Global (6 biến) | 2/6 | 3/6 |
| VN Macro (9 biến) | 3/9 | 4/9 |
| Cross-asset (6 biến) | 2/6 | 3/6 |

- Shift được **cân nhắc** khi đạt minimum ở **2/3 layer**.
- Shift được **xác nhận** khi đạt minimum ở **2/3 layer** + Rule B (persistence) + Rule C (cross-validation).

### 6.2 Rule B — Persistence (bền vững theo thời gian)

| Loại transition | Persistence yêu cầu |
|---|---|
| Shift R1↔R2, R2↔R3 (gentle, slow-moving) | **5 phiên giao dịch** liên tiếp ở regime mới |
| Shift R3↔R4, R4↔R5 (jumpy, stress regime) | **3 phiên** (vì regime stress có tính fast và whipsaw) |
| Shift R4/R5 → R1/R2 (recovery khó xác nhận) | **10 phiên** (false start risk cao, dead cat bounce) |

**Lý do:** Theo nguyên tắc phi dừng (105-methodology), dữ liệu lịch sử có thể không đại diện. Recovery regime đặc biệt dễ false start — nhiều bounce 1-2 tuần rồi rollover. 10-phiên rule chống lại confirmation bias bullish sớm.

**Quy ước thay thế (alternative — OPVIA calibrate):** Có thể dùng **weekly close** thay cho trading day, hoặc **rolling 2-week average** của biến macro để smooth noise. Default dùng trading day.

### 6.3 Rule C — Cross-Validation (kiểm chứng chéo asset class)

Trước khi officially call regime shift, cần ≥2 lớp tài sản xác nhận theo các pattern dưới:

| Layer 1 xác nhận | Layer 2 xác nhận | Ví dụ transition |
|---|---|---|
| FX (VND depreciation breach) | Rates (VN bond yield spike) | R3→R4 |
| Rates (UST 10Y collapse) | Equity (VN-Index ≥10% drawdown) | R3→R5 (shock) |
| Macro (credit growth re-accelerate) | Equity (margin balance rising + cyclical rotation) | R5→R1 |
| Commodity (oil crash) | FX (DXY spike) | R2→R4 nhanh (supply shock reverse) |
| Macro (NHNN OMO net inject sustained) | Credit (corp bond issuance reopen) | R5→R1 confirm |

### 6.4 Rule D — Veto Conditions (dấu hiệu loại trừ tức thì)

Một số tín hiệu **veto** regime call ngay lập tức, bất kể các biến khác:

| Veto signal | Ý nghĩa | Action |
|---|---|---|
| NHNN can thiệp FX đột biến (>$5bn/tuần) | R2/R3 call bị hủy | Buộc xem xét R4 |
| Lãi suất liên ngân hàng VN spike >2x base (vd: 3% → >6%) | R1/R2 call bị hủy | Buộc xem xét R4/R5 |
| Forced selling margin cascade (>20% margin accounts hit trigger) | Bất kể macro | Coi như R5 stress event tức thì |
| Step-function shock (chiến tranh, đại dịch, cấm vận, policy regime change) | Không thuộc regime thông thường | Suspend regime framework, dùng scenario riêng (xem `125-macro-micro.md` Phần 6.4) |
| Analyst override (OPVIA flag structural break) | Có domain knowledge ngoài model | Khung tạm hold, awaiting re-calibration |

---

## 7. Operational Use — Mapping vào hệ thống OPVIA Sigma

Mỗi regime có 3 mapping operational: (i) module domain nào kích hoạt đầu tiên, (ii) output framing nào dùng, (iii) signpost nào theo dõi cho shift kế tiếp.

### 7.1 Module Activation Priority by Regime

| Regime | Module kích hoạt đầu tiên | Module thứ hai | Module hạ ưu tiên |
|---|---|---|---|
| **R1** | `domain-macro-vn-credit-cycle.md` + `domain-equity-vn-valuation-advanced.md` | `domain-cross-asset-correlation-regimes.md` | `domain-fx-carry-and-positioning.md` (chưa cần) |
| **R2** | `domain-equity-vn-moat-analysis.md` + `domain-equity-vn-financial-modeling.md` | `domain-macro-vn-monetary-policy-nhnn.md` (theo dõi pivot) | `domain-fi-em-rates-context.md` (chỉ reference) |
| **R3** | `domain-macro-vn-monetary-policy-nhnn.md` + `domain-cross-asset-risk-on-off.md` | `domain-equity-vn-forensic-accounting.md` (check earnings quality) | `domain-equity-vn-valuation-advanced.md` (P/E trap risk) |
| **R4** | `domain-fx-usd-vnd-dynamics.md` + `domain-macro-vn-liquidity-systems.md` | `domain-fi-credit-spreads-vn.md` + `domain-cross-asset-flight-to-quality.md` | `domain-equity-vn-financial-modeling.md` (earnings unreliable) |
| **R5** | `domain-macro-vn-liquidity-systems.md` + `domain-macro-vn-credit-cycle.md` | `domain-equity-vn-forensic-accounting.md` (survival check) + `domain-fx-intervention-history.md` | `domain-equity-vn-valuation-advanced.md` (normalize earnings impossible) |

### 7.2 Output Framing by Regime

| Regime | Framing chính | Tone narrative | Valuation approach |
|---|---|---|---|
| **R1** | Growth-tilt, cyclical overweight, earnings inflection | "Tìm early cycle winners" | Forward P/E justified, DCF với earnings ramp |
| **R2** | Quality growth, sector rotation, stock picking | "Grind with quality" | Normalized multiples, DCF base case |
| **R3** | Defensive rotation, earnings quality check, de-risk | "Late cycle — don't chase" | Reverse DCF check embedded expectations, stress test |
| **R4** | Capital preservation, FX hedge, liquidity focus | "Survive first" | **Không valuation** — chỉ balance sheet strength + covenant check |
| **R5** | Contrarian positioning, distressed screening, survival | "Prepare for turn, not yet" | Forward-looking từ đáy (không TTM), scenario bounds wide |

**Lưu ý Safety Policy Rule 2:** Output framing không phải khuyến nghị. "Growth-tilt" nghĩa là **nếu** OPVIA quyết định position trong R1, framework gợi ý nên focus vào growth/cyclical — không phải hệ thống recommend OPVIA mua growth.

### 7.3 Signpost Variables to Monitor for Next Shift

| Hiện tại | Signpost cần theo dõi | Shift tiềm năng |
|---|---|---|
| **R1** | Credit growth có chững lại trước khi đạt 15%? NHNN OMO có chuyển withdraw? CPI bắt đầu vượt 3%? | R1 → R2 hoặc R1 → R3 (nếu overheat) |
| **R2** | CPI vượt 4%? Fed pivot hawkish signal? VND bắt đầu mất giá nhanh >1%/quý? | R2 → R3 |
| **R3** | DXY >108? UST 10Y >5%? NHNN can thiệp FX? Margin balance peak rồi giảm? | R3 → R4 |
| **R4** | DXY peak rồi giảm? Fed signal pause/cut? NHNN bơm OMO trở lại? Forced selling exhausted? | R4 → R5 hoặc R4 → R1 (rare — usually qua R5) |
| **R5** | Credit growth chạm đáy và flat? Margin balance tăng nhẹ? PMI bounce >50? Foreign net buy turn positive? | R5 → R1 |

---

## 8. Limitations & Critique — 7 Self-Critiques

Khung v1.1 này là **strawman codified**, có các giới hạn đã được flag:

### 8.1 Threshold calibration TBD — chờ OPVIA team edit

Tất cả threshold (DXY >108, UST >5%, credit growth <10%, VND mất giá >2.5%) là **best guess** dựa trên public memory + reverse-engineering. OPVIA có thể có internal threshold khác. **Hành động:** OPVIA calibrate threshold trong Sprint 0 session #1; khung này version v1.1-draft → v1.1-final sau calibration.

### 8.2 Asymmetric transitions chưa formalize

Một số transition là **rất hiếm** hoặc **không thể**:
- R4 → R1 trực tiếp: hầu như không xảy ra mà không qua R5 (cần forced deleveraging trước recovery thực sự).
- R1 → R3 skip R2: có thể xảy ra trong overshooting easing (VD: 2010 sau 2009 stimulus) — chưa được ghi nhận trong khung.
- R5 → R3 skip R1: gần như không thể.

**Hành động:** Khung cần thêm transition matrix với probability qualitative (high/mid/low/very low/impossible) cho mỗi cặp transition.

### 8.3 Regime overlap zones — boundary fuzziness

Trong thực tế, các regime không có boundary sharp. Có **transition zones** kéo dài 2-6 tuần khi pattern không clear (ví dụ: Q1 2018 — borderline R2/R3). Rule A breach threshold có thể fail trong overlap zones, dẫn đến "regime indeterminate" call.

**Hành động:** Cần workflow riêng (`workflow-regime-shift-alert.md`) handle overlap zones — output "regime indeterminate, watching X variables" thay vì force binary.

### 8.4 VN-specific calibration gap — bond market shallow

Cross-asset Layer (đặc biệt C2 bond-equity correlation) giả định VN bond market có depth tương đương US/EU. Thực tế:
- Bond market VN kém sâu, thanh khoản thấp → bond yield có thể không phản ứng "đúng" như UST.
- 90% NĐT cá nhân → khi panic, bán cả cổ phiếu lẫn trái phiếu (flight to cash, không phải flight to quality) → correlation luôn dương ở stress events.

**Hành động:** Có thể cần thay C2 bond-equity bằng **equity-FX correlation** hoặc **equity-margin correlation** ở VN context.

### 8.5 Persistence rule cứng — 5 phiên có thể không phù hợp

5 phiên cho R1↔R2 có thể quá dài (miss early shift) hoặc quá ngắn (whipsaw). Alternatives chưa thử:
- Weekly close thay vì trading day.
- Rolling 2-week average của biến macro.
- "3/5 biến phải breach **và** NHNN có hành động cụ thể."

**Hành động:** Backtest empirical với 5 historical periods (2008, 2011, 2015, 2018, 2020, 2022) để xác định persistence optimal.

### 8.6 Thiếu biến "agent behavior" (behavioral layer)

Khung hiện tại thiên về **price-based** (giá DXY, UST, VNI) hơn **behavioral**:
- Không có biến **khẩu vị rủi ro NHTM** (LDR, credit standard tightening/loosening surveys).
- Không có biến **positioning của NĐT tổ chức nước ngoài** (FII flow detail, fund positioning).
- Không có biến **tâm lý tiêu dùng** (consumer confidence index VN).
- Không có biến **margin standards** của các CTCK lớn.

**Hành động:** Phase 2 có thể bổ sung **Behavioral Layer (Layer 4)** với 4-5 biến hành vi.

### 8.7 Step-function shock chưa operationalize đầy đủ

Rule D có nói "step-function shock → suspend regime framework", nhưng chưa định nghĩa:
- **Khi nào** shock đủ lớn để suspend? (threshold cho size of shock)
- **Transition back** từ shock scenario về regime framework như thế nào?
- Có **emergency regime** R0 riêng cho geopolitical stress kéo dài (như Ukraine 2022)?

**Hành động:** Pair với `workflow-regime-shift-alert.md` để define "shock suspend protocol" cụ thể.

---

## 9. Linked Frameworks — Theoretical Anchors

Khung Regime v1.1 không phải standalone — nó tích hợp các framework học thuật theo từng regime:

| Framework | Khi nào active | Vai trò |
|---|---|---|
| **Thakor & Yu (2024)** — Bank capital & liquidity creation | R3, R4 (tightening + stress) | Phân tích bank capital adequacy + liquidity creation collapse trong stress regime. Pair với `domain-macro-vn-liquidity.md`. |
| **Kashyap & Stein (2000)** — Bank lending channel | R3, R4 (tightening transmission) | Tách "large bank lending" vs "small bank lending" để xem credit channel ai bị hit trước khi NHNN siết. |
| **Brunnermeier & Pedersen (2009)** — Funding & market liquidity | R4, R5 (stress + deleveraging) | Funding liquidity vs market liquidity feedback loop — explain forced selling cascade. |
| **Geanakoplos (2010)** — Leverage cycle | R3 → R4 → R5 (full down-cycle) | Margin balance + collateral haircut → mechanism của forced deleveraging trong R4 và slow repair trong R5. |
| **Borio (financial cycle)** — Medium-term financial cycle | R1 ↔ R5 (long arc) | Khung 8-15 năm financial cycle, hỗ trợ identify đâu trong long-cycle hiện tại. |
| **Mundell-Fleming + Trilemma** — Open economy constraint | R3, R4 (FX pressure regime) | VN trilemma: ưu tiên FX + rate → buộc capital controls. Explain limit của NHNN response trong R4. |
| **Minsky (financial instability)** — Hedge → speculative → Ponzi | R2 → R3 (overheat build-up) | Identify Ponzi finance buildup trong credit boom — leading indicator R3 → R4. |
| **Dickinson (2011) / Mauboussin** — Corporate lifecycle | All regimes (single-name layer) | Lifecycle stage interaction với regime — VD: growth-stage company hit hardest trong R4 vì cash burn. |

**Quy tắc compose:** Khi conflict giữa 2 framework (VD: Geanakoplos suggest R5 sẽ kéo dài, nhưng Borio suggest sắp turn), framework yêu cầu **flag conflict explicit**, không tự dung hòa. Để OPVIA quyết định weight.

---

## 10. OPVIA Usage Examples — 3 Worked Mappings

### 10.1 Example A — Q1 2020 COVID → R4 Stress Event (Short)

- **Setup pre-shock (Q4 2019):** R2 Steady Growth — Fed hold, DXY 97-98, credit growth 13%, CPI 3%.
- **Trigger (cuối Jan - Feb 2020):** COVID outbreak China → step-function shock per Rule D Veto. Suspend regime framework, dùng scenario "pandemic shock".
- **Mapping vào R4 (Mar 2020):** Sau 2-3 tuần, Rule D shock dissipate → reapply framework. Breach: G1 DXY spike 99 → 103, G2 UST 10Y crash 1.9% → 0.5%, G3 Fed emergency cut 150bps, V1 NHNN inject OMO mạnh, V3 credit growth freeze, C2 bond-equity corr → +1, C5 volatility >50%, C6 foreign net sell heavy. → **9/21 biến breach R4 threshold đồng thời** → R4 confirmed Mar 2020.
- **Module activation:** `domain-fx-usd-vnd-dynamics.md` + `domain-macro-vn-liquidity-systems.md` (per §7.1 R4 mapping).
- **Output framing:** "Survive first — capital preservation, balance sheet check" — **không valuation**.
- **Transition R4 → R1 (Q2 2020):** Rule D suspend bị thay bằng Rule A confirmation: Fed 0%, DXY giảm về 97 → 92, NHNN cut rate, credit growth turn positive, foreign flow stabilize. **5/21 biến confirm R1** + persistence 10 phiên (recovery rule) → R1 confirmed Jun 2020.
- **Lesson:** R4 stress event có thể **rất ngắn** (6-8 tuần) khi central bank response decisive. Không phải mọi R4 đều dẫn đến R5 deleveraging dài.

### 10.2 Example B — Q3 2022 Fed Hiking + DXY Surge → R3 → R4 Transition

- **Setup (Q1-Q2 2022):** R3 Late Cycle — Fed hawkish pivot post Mar 2022 hike, DXY 95 → 105, UST 10Y 1.5% → 3%, CPI VN 2% → 3.5%, credit growth 14% momentum giảm. **8/21 biến breach R3** confirmed.
- **R3 → R4 trigger (Aug-Oct 2022):** G1 DXY breach 108 → 114 (peak), G2 UST 10Y breach 4%, G3 Fed 75bps hike consecutively, V2 VND mất giá ~5% từ đầu năm, V1 NHNN buộc tăng lãi suất điều hành 200bps trong 1 tháng, C2 bond-equity correlation chuyển dương mạnh, C5 volatility VNI spike >40%, C6 foreign net sell heavy.
- **Confirmation per Rule A:** Global 4/6 + VN Macro 5/9 + Cross-asset 4/6 → đạt minimum 2/3 layer.
- **Rule B persistence:** 3 phiên (R3↔R4 jumpy rule) → met đầu Sep 2022.
- **Rule C cross-validation:** FX (VND breach) + Rates (VN bond yield spike từ 3% lên 5%) → confirmed.
- **Module activation:** `domain-fx-usd-vnd-dynamics.md` + `domain-macro-vn-liquidity-systems.md` + `domain-fi-credit-spreads-vn.md` (corp bond freeze).
- **Output framing:** "Survive first — FX hedge, liquidity focus" + flag corp bond market tail risk.
- **Lesson:** R3 → R4 transition **xác nhận chỉ trong 3 tuần** vì Rule B persistence cho stress regime ngắn (3 phiên). Real-time monitoring cần check daily trong R3 → R4 risk zone.

### 10.3 Example C — 2024 VN Recovery → R5 → R1 Transition

- **Setup (Q4 2022 - Q2 2023):** R5 Deleveraging — corp bond freeze, BĐS đóng băng, NHNN cut OMO rate 200bps nhưng credit growth ~0%, NPL recognition ongoing.
- **Early signpost (Q3 2023):** Credit growth chạm đáy 0% và flat 2 tháng, margin balance bottom + bắt đầu rise nhẹ, foreign net buy turn positive sustained 4 tuần.
- **R5 → R1 trigger (Q4 2023 - Q1 2024):** G3 Fed pause signaled (post Nov 2023 hold), G1 DXY giảm từ 107 → 102, G2 UST 10Y giảm từ 5% → 3.8%, V3 credit growth turn positive 8% YoY, V1 NHNN ổn định OMO inject net, C3 VCB lead recovery, C6 foreign net buy sustained.
- **Confirmation per Rule A:** Global 4/6 + VN Macro 4/9 + Cross-asset 3/6 → minimum 2/3 layer met.
- **Rule B persistence:** 10 phiên (recovery rule) — confirmed late Q1 2024 sau gần 1 quý watching.
- **Rule C cross-validation:** Macro (credit re-accelerate) + Equity (margin rising + cyclical sector — BĐS/NH lead) → confirmed.
- **Module activation:** `domain-macro-vn-credit-cycle.md` + `domain-equity-vn-valuation-advanced.md` (forward earnings ramp).
- **Output framing:** "Tìm early cycle winners — cyclical overweight, BĐS/NH/Steel".
- **Lesson:** Recovery confirmation **chậm có chủ đích** — 10 phiên persistence + 1 quý watching protect against false start. Q1-Q3 2023 có 2 false starts (bounce 2-3 tuần rồi rollover) bị rule này filter ra đúng.

---

## 11. Open Questions for OPVIA — AWAITING OPVIA REVIEW (Sprint 0 Session #1)

Các câu hỏi dưới đây **chỉ OPVIA có thể trả lời** — sẽ được resolve trong Sprint 0 session #1 và trigger v1.1-final calibration. **Trạng thái: AWAITING OPVIA REVIEW.**

1. **AWAITING OPVIA REVIEW — Số lượng regime:** OPVIA confirm 5 regime joint global-VN, hay muốn 4 (như `125-macro-micro.md` cũ) hoặc 6 (tách "Stagflation" thành regime riêng R6)?

2. **AWAITING OPVIA REVIEW — Threshold deal-breaker:** Trong 21 biến §3, biến nào là **deal-breaker** — nếu breach, các biến khác không còn quan trọng? (Hypothesis: V1 NHNN OMO action + V2 VND intervention.)

3. **AWAITING OPVIA REVIEW — Asymmetric transitions:** Confirm transition matrix proposed §8.2. Có transition nào **không thể** ngoài R4→R1 trực tiếp? (VD: R5→R3 skip R1?)

4. **AWAITING OPVIA REVIEW — DXY vs Fed stance:** OPVIA coi DXY (G1) là biến **độc lập** hay chỉ là hệ quả của Fed (G3) + UST diff (G2)? Có bao giờ DXY surge mà VN vẫn R2 không (decoupling)?

5. **AWAITING OPVIA REVIEW — NHNN reaction function:** Khi NHNN tăng lãi suất điều hành, đó là **proactive** (đi trước Fed) hay **reactive** (theo sau Fed)? Có delay trung bình bao lâu trong 2018, 2022?

6. **AWAITING OPVIA REVIEW — VND threshold critical:** Ngưỡng mất giá VND nào là **critical** cho regime call? 1.5%/quý? 2.5%/quý? 5%/năm? Hay ngưỡng intervention NHNN là quan trọng hơn?

7. **AWAITING OPVIA REVIEW — Credit growth target:** SBV thường đặt target credit hàng năm. Target đó có phải biến **regime-defining** không? Hay chỉ là noise (target thường bị miss)?

8. **AWAITING OPVIA REVIEW — NPL leading indicator:** Indicator nào để **dự báo** NPL trước khi NPL chính thức tăng? (Special mention loan? Restructured loan? Lãi suất quá hạn? Group 2 loans growth?)

9. **AWAITING OPVIA REVIEW — Equity-bond correlation VN:** OPVIA có thấy correlation C2 thực sự đổi dấu theo regime ở VN không? Hay VN thường **cả hai cùng rơi** (both risk assets, flight-to-cash) → correlation luôn dương? (Critique §8.4.)

10. **AWAITING OPVIA REVIEW — Shelf life regime call:** Confirm shelf life 1-2 tuần trong volatile regime (R3, R4) và 2-4 tuần trong stable regime (R2, R5)? Hay OPVIA có rule khác (VD: regime call chỉ đổi khi X biến breach lại)?

11. **AWAITING OPVIA REVIEW — Step-function shock protocol:** Geopolitical (Iran-US, eo biển), pandemic, cấm vận — OPVIA xử lý như **scenario ngoài regime** (`125-macro-micro.md` 6.4) hay muốn có **regime R0 emergency** riêng cho geopolitical stress kéo dài?

12. **AWAITING OPVIA REVIEW — Internal proprietary data:** OPVIA có internal data/indicator nào (proprietary positioning data, broker survey, nhóm ngành lead-lag, consumer confidence proprietary) cần reference trong khung này nhưng không có trong public data?

---

## Phụ lục — Ma trận tóm tắt 1 trang

| | R1 Recovery | R2 Steady | R3 Late Cycle | R4 Stress | R5 Deleveraging |
|---|---|---|---|---|---|
| **Global** | DXY↓ UST↓ Fed cut | DXY→ UST→ Fed hold | DXY↑ UST↑ Fed hawk | DXY↑↑ UST↑↑ Fed hike | DXY volatile UST↓ Fed cut into recession |
| **VN Macro** | NHNN inject, TD↑, CPI↓ | NHNN neutral, TD 12-15%, CPI 2-3.5% | NHNN signal tighten, TD>15% momentum↓, CPI↑ | NHNN tighten/FX defend, TD<10%, CPI high | NHNN inject ineffective, TD~0%, NPL↑ |
| **Cross-asset** | Eq-bond corr âm, VNI outperform, spread↓ | Eq-bond corr ~0, VNI inline, spread→ | Eq-bond corr turning +, rotation defensive, spread↑ | Eq-bond corr +, VNI crash, spread blowout | Eq-bond corr +, forced selling, issuance freeze |
| **Valuation** | Forward P/E justified | Normalized multiples | Reverse DCF, stress test | No valuation — BS only | Forward from bottom |
| **Sector tilt** | Cyclical, BĐS, NH | Broad, quality growth | Defensive, energy/materials last | Exporters, cash-rich | Distressed, survivors |
| **Module priority** | credit-cycle, valuation | moat, modeling | monetary-policy, forensic | FX, liquidity | liquidity, credit-cycle, forensic |
| **Shelf life** | 2-3 tuần | 2-4 tuần | 1-2 tuần | 1 tuần | 2-3 tuần (false bottom risk) |
| **Persistence rule** | 10 phiên (recovery) | 5 phiên | 5 phiên | 3 phiên | 3 phiên |

---

> **Status & Confidence:**
> - Phiên bản: v1.1-DRAFT
> - Codified: 2026-04-19 (Wave 4 Lane 3)
> - Source: Reverse-engineered from Wave 2 E1 strawman + Focus_Brief §7 template
> - Bậc bằng chứng: [Bậc 3 — Bằng chứng sơ bộ] / [Q2 — Có cơ sở]
> - **Hành động kế tiếp:** OPVIA team phản biện 12 câu hỏi §11 trong Sprint 0 session #1 → tinh chỉnh threshold + transition matrix + behavioral layer → version v1.1-FINAL.
> - **Quy ước sử dụng:** Mọi regime call dựa trên framework này phải gắn `[REGIME-SPECIFIC]` + ngày + shelf life rõ ràng theo Safety Policy Rule 5 trong `core-voice-and-safety.md`.
