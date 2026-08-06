---
title: "Fixed Income EM Rates Context — UST 10Y Anchor, Term Premium, EM Spread Compression Cycles, and US Real Yield Transmission"
module_type: "domain"
file_name: "domain-fi-em-rates-context.md"
purpose: "Provide the global rates anchor framework for Vietnam fixed income analysis: UST 10Y as the risk-free baseline, term premium dynamics, EM rate spread compression/expansion cycles, and transmission mechanisms from US real yields into Vietnam TPCP yields and VND rates."
primary_triggers:
  - "UST 10Y yield"
  - "term premium"
  - "EM rates spread"
  - "US real yield"
  - "TPCP yield vs UST"
  - "spread compression"
  - "Fed policy transmission Vietnam"
  - "VN bond yield anchor"
when_to_use:
  - "When analyzing why Vietnam TPCP yields move in sync with or diverge from UST 10Y."
  - "When assessing the fair value spread of Vietnam rates over UST in different Fed regimes."
  - "When forecasting direction of VN bond yields based on US macro data (CPI, payrolls, Fed dots)."
  - "When evaluating carry attractiveness of Vietnam TPCP for foreign investors relative to other EM."
when_not_to_use:
  - "Do not use as a standalone domestic supply-demand model — pair with domain-fi-bond-supply-demand.md."
  - "Do not apply mechanically without checking Vietnam-specific liquidity stress or SBV intervention."
  - "Not a substitute for FX analysis of VND carry — see domain-fx-usd-vnd.md."
related_modules:
  - "domain-fi-bond-supply-demand.md"
  - "domain-fi-bank-treasury-alm.md"
  - "domain-fi-ldr-bank-funding.md"
  - "macro-vn-monetary-policy-nhnn.md"
  - "macro-vn-transmission-channels.md"
  - "framework-regime-v11.md"
authoritative_citations:
  - "FRED: UST 10Y, TIPS 10Y real yield, term premium estimates (ACM, Kim-Wright)"
  - "IMF Global Financial Stability Report (GFSR) — EM rates chapter"
  - "BIS Quarterly Review: international banking flows and bond market spillovers"
  - "JP Morgan GBI-EM Global Diversified Index metrics"
  - "NHNN monthly statistics: TPCP yield curve, foreign holdings"
  - "VBMA bond market reports"
output_owner: "workflow-deep-dive.md when user asks about VN rates fair value or UST transmission; workflow-daily-brief.md when UST 10Y moves >10bps."
---

# EM Rates Context — UST 10Y Anchor và Truyền dẫn vào Thị trường VN

**Mục đích:** Xác định giá trị mốc (anchor) toàn cầu cho lãi suất VN: UST 10Y, term premium, chu kỳ nén/giãn spread EM, và kênh truyền dẫn từ US real yield vào TPCP.

**Trạng thái:** [DỮ LIỆU THỰC TẾ 2020-2026 | FRAMEWORK | CẬP NHẬT THEO FED MEETING VÀ NHNN MONTHLY]

---

## 1. UST 10Y làm Neo (Anchor) cho EM Rates

### 1.1. Tại sao UST 10Y quyết định lãi suất VN?

Dù VN không phải thành viên JPM GBI-EM GD (do capital control và non-deliverability), lãi suất TPCP vẫn chịu ảnh hưởng gián tiếp mạnh từ UST 10Y qua 3 kênh:

1. **Kênh tâm lý (sentiment channel):** UST 10Y tăng nhanh → FII rút khỏi EM bond → áp lực lên TPCP secondary market, đặc biệt khi VBMA reference yield bị đẩy lên.
2. **Kênh carry differential:** Khi UST 10Y tăng, spread TPCP 10Y − UST 10Y thu hẹp → TPCP kém hấp dẫn hơn với nhà đầu tư ngoại đo lường bằng USD-hedged yield.
3. **Kênh NHNN phản ứng:** UST 10Y tăng kéo theo DXY mạnh lên → NHNN có xu hướng giữ lãi suất điều hành cao hơn để bảo vệ VND → TPCP primary yield không thể giảm độc lập.

**Dữ liệu thực tế (proxy):** TPCP 10Y VN dao động trong khoảng 2.8-3.5% (2023-2024), trong khi UST 10Y dao động 3.8-4.5%. Spread trung bình ~80-150bps, thấp hơn nhiều so với Indonesia (~350bps) hay Philippines (~250bps) do VN bond market ít liquid và FII tham gia hạn chế. Spread này không phản ánh "country risk premium" đúng nghĩa mà phản ánh cả **capital control premium** và **liquidity premium**.

### 1.2. Term Premium — Yếu tố bị bỏ quên

Term premium (phần thặng dư lãi suất dài hạn bù đắp cho rủi ro nắm giữ trái phiếu dài kỳ hạn) ở UST đã trở lại dương từ 2022 sau chu kỳ âm dài 2010-2021.

| Giai đoạn | ACM Term Premium (UST 10Y) | Ý nghĩa cho EM |
|---|---|---|
| 2019-2021 | −0.5% đến 0% | QE nén term premium → EM có "free carry", dòng vốn vào EM bond mạnh |
| 2022-2023 | 0.5% đến 1.2% | QT + Fed hiking → term premium bùng nổ → EM bị bán tháo |
| 2024-2025 | 0.3% đến 0.8% | Terminal rate uncertainty → term premium volatile |
| 2026 (scenario) | 0.5% đến 1.0% | Nếu Iran-US war kéo dài → safe-haven demand UST nhưng supply tăng → term premium ambiguous |

**Ứng dụng VN:** Khi US term premium tăng, TPCP 10Y VN khó giảm dù lạm phát VN ổn định. Ngược lại, nếu term premium giảm (Fed cut nhanh), TPCP có room giảm theo nhưng bị hạn chế bởi **floor của lãi suất huy động VND** (competition với bank deposit).

---

## 2. Chu Kỳ Nén/Giãn Spread EM (EM Rate Spread Compression Cycles)

### 2.1. Framework 4 pha chu kỳ spread EM

| Pha | Đặc trưng | UST 10Y | EM Spread | Dòng vốn FII EM | Tác động VN |
|---|---|---|---|---|---|
| **Compression rộng** | Fed pause/cut, risk-on | Giảm hoặc stable | Thu hẹp mạnh (>50bps) | Inflow mạnh | TPCP yield giảm theo, dù supply domestic |
| **Compression chật** | Late cycle, carry hunt | Stable | Thu hẹp nhẹ (<20bps) | Inflow chọn lọc | Chỉ TPCP short-mid tenor hưởng lợi |
| **Expansion nhanh** | Fed hawkish surprise, DXY spike | Tăng nhanh | Giãn >50bps | Outflow mạnh | TPCP yield tăng, nhà băng bán TPCP để giữ thanh khoản |
| **Expansion chậm** | Structural repricing | Drift higher | Giãn dần | Rotation sang HY/local | VN ít ảnh hưởng nếu FII exposure thấp |

### 2.2. VN trong bối cảnh EM peer comparison

VN không nằm trong GBI-EM GD nên **không bị forced selling từ benchmark-driven outflow**. Đây là điểm khác biệt quan trọng so với Indonesia, Malaysia, Thái Lan. Tuy nhiên, VN vẫn chịu:

- **Regional sentiment spillover:** Khi Asia HY bond (Indonesia, Philippines) bị bán tháo, VBMA reference yield thường điều chỉnh lên 5-10bps dù không có giao dịch thực.
- **Cross-asset correlation:** FII equity outflow khỏi VN thường đi kèm với giảm exposure fixed income (nếu có), tạo áp lực lên cả hai market.
- **NHNN signaling effect:** Spread TPCP 10Y − UST 10Y dưới 50bps được xem là "danger zone" cho nhà băng nội địa vì khuyến khích mua TPCP thay vì cho vay → NHNN có thể can thiệp gián tiếp qua OMO hoặc room tín dụng.

---

## 3. US Real Yield Transmission — Kênh Truyền dẫn Mạnh nhất

### 3.1. Real yield = Nominal − Breakeven Inflation

US 10Y real yield (TIPS) là biến số toàn cầu quyết định giá của mọi tài sản real (gold, commodities, EM equity, EM bond). Transmission vào VN:

**Kênh trực tiếp (nhỏ):**
- FII nắm giữ TPCP quy đổi sang USD real yield: nếu TIPS tăng từ 1.5% lên 2.5%, TPCP 10Y nominal 3.2% (USD-hedged ~3.5%) trở nên kém hấp dẫn hơn.

**Kênh gián tiếp (lớn):**
- TIPS tăng → DXY mạnh lên → NHNN phòng thủ VND bằng cách giữ lãi suất điều hành → deposit rate floor không giảm → TPCP primary yield bị kẹt ở mức cao.
- TIPS tăng → global risk-off → VN equity P/E compression → wealth effect giảm → credit demand yếu → nhà băng dư tiền mua TPCP → paradox: TPCP yield có thể giảm do domestic demand mạnh dù US real yield tăng.

### 3.2. Regime-dependent transmission

| Regime | US Real Yield | Transmission vào VN TPCP | Confidence |
|---|---|---|---|
| Fed easing, real yield giảm | <1.0% | TPCP yield giảm theo, nhưng floor là deposit rate (~6-7% VND) | Cao |
| Fed neutral, real yield stable | 1.0-1.5% | TPCP yield sideway, spread EM stable | Trung bình |
| Fed hawkish, real yield tăng | >1.5% | TPCP yield tăng hoặc không giảm; NHNN giữ chặt | Cao |
| Geopolitical shock (UST safe-haven) | Ambiguous | TPCP decouple: nếu DXY spike + VND stress → TPCP yield tăng; nếu global recession fear → flight to quality into TPCP → yield giảm | Thấp — cần scenario analysis |

---

## 4. Dữ liệu Thực tế và Proxy cho VN

| Biến số | Nguồn | Tần suất | Ghi chú |
|---|---|---|---|
| UST 10Y nominal | FRED | Real-time | Anchor toàn cầu |
| US 10Y TIPS real yield | FRED | Real-time | Driver global risk-free real rate |
| ACM term premium | NY Fed | Monthly | Estimate, không quan sát trực tiếp |
| TPCP 2Y/5Y/10Y yield | VBMA, NHNN | Daily/Weekly | Không có benchmark on-the-run liên tục như UST |
| FII bond holding | NHNN, VBMA | Monthly | ~3-5% TPCP outstanding, nhỏ nhưng biên quan trọng |
| Cross-country spread | Bloomberg, broker research | Daily | So sánh VN vs ID, PH, TH, MY |

**[DỮ LIỆU THIẾU]:** VN không có TIPS market → không có market-implied real yield nội địa. Phải proxy bằng TPCP nominal − CPI YoY, nhưng CPI lag và smoothed → real yield ước tính có độ trễ 1-2 tháng.

---

## 5. Cross-references và Ứng dụng Phân tích

- **domain-fi-bond-supply-demand.md:** Supply TPCP tăng mạnh trong giai đoạn UST yield giảm có thể bù đắp nhau → yield sideway.
- **domain-fi-bank-treasury-alm.md:** Quyết định mua/bán TPCP của khối treasury phụ thuộc vào kỳ vọng UST direction + duration gap target.
- **macro-vn-monetary-policy-nhnn.md:** NHNN điều chỉnh OMO rate và room tín dụng để phản ứng với UST/Fed — không phải mechanical tracking.
- **framework-regime-v11.md:** Regime classification phải gắn UST 10Y level, slope (2s10s), và real yield như 3 biến đầu vào.

---

*Module: domain-fi-em-rates-context.md | Wave 5 Lane 8 | OPVIA Sigma*
