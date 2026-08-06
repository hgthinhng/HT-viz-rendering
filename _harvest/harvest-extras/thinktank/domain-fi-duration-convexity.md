---
title: "Domain FI Duration Convexity — Macaulay Duration, Modified Duration, Convexity, Key Rate Duration, Bank Treasury ALM, Insurance ALM, Convexity Hedging"
module_type: "domain"
file_name: "domain-fi-duration-convexity.md"
purpose: "Hướng dẫn kỹ thuật về duration và convexity trong quản lý danh mục trái phiếu Việt Nam, bao gồm duration targeting cho khối treasury ngân hàng và bảo hiểm, key rate duration để phân rã rủi ro yield curve, và chiến lược convexity hedging trong các giai đoạn đường cong biến dạng."
primary_triggers:
  - "duration trái phiếu"
  - "modified duration"
  - "convexity hedging"
  - "key rate duration"
  - "duration gap ALM"
  - "bank treasury duration targeting"
  - "insurance ALM duration mismatch"
  - "DV01 VN bond"
  - "steepening flattening hedge"
when_to_use:
  - "Khi đo lường độ nhạy của danh mục trái phiếu với thay đổi lãi suất và thiết kế chiến lược hedge."
  - "Khi phân tích ALM của ngân hàng hoặc bảo hiểm: duration gap, reinvestment risk, và funding mismatch."
  - "Khi đánh giá tác động của yield curve shift (parallel, steepening, flattening, butterfly) lên portfolio."
when_not_to_use:
  - "Không dùng để pricing trái phiếu doanh nghiệp có embedded option (callable, putable) — cần effective duration và OAS model."
  - "Không dùng cho phân tích credit risk — xem domain-fi-credit-spreads-vn.md."
related_modules:
  - "framework-thakor-yu-2024.md"
  - "macro-vn-credit-cycle.md"
  - "domain-fi-yield-curve-vn.md"
  - "domain-fi-ldr-and-bank-funding.md"
  - "domain-fi-credit-spreads-vn.md"
authoritative_citations:
  - "Fabozzi, F. J. Bond Markets, Analysis, and Strategies."
  - "Tuckman, B., & Serrat, A. Fixed Income Securities: Tools for Today's Markets."
  - "Hull, J. C. Options, Futures, and Other Derivatives."
  - "CFA Institute — Fixed Income Portfolio Management."
output_owner: "workflow-deep-dive.md khi phân tích ALM hoặc bond portfolio risk; workflow-daily-brief.md không dùng module này."
---

# Domain FI Duration & Convexity — Quản Lý Rủi ro Lãi suất Trái phiếu VN / Duration Targeting & Convexity Hedging

Purpose: Cung cấp bộ công cụ kỹ thuật (technical toolkit) để đo lường và quản lý rủi ro lãi suất cho danh mục trái phiếu tại Việt Nam. Module tập trung vào ứng dụng thực tiễn cho hai nhóm chủ thể chính: khối treasury ngân hàng thương mại và khối đầu tư bảo hiểm nhân thọ, với dữ liệu và case study từ thị trường TPCP/TPDN Việt Nam.

Trigger keywords: duration, modified duration, Macaulay duration, convexity, key rate duration, DV01, duration gap, ALM ngân hàng, ALM bảo hiểm, duration targeting, convexity hedging, steepening, flattening, parallel shift, yield curve twist.

---

## 1. Foundation: Macaulay, Modified Duration, và Convexity

### 1.1. Macaulay Duration (DMac)

Macaulay duration đo **thờii gian có trọng số trung bình** để nhận lại dòng tiền của trái phiếu:

$$D_{Mac} = \frac{\sum_{t=1}^{n} t \cdot \frac{C}{(1+y)^t} + n \cdot \frac{F}{(1+y)^n}}{P}$$

Trong đó: C = coupon, F = face value, y = yield to maturity, P = giá hiện tại, n = số kỳ còn lại.

**Ý nghĩa tại VN:** Do TPCP phát hành coupon cố định (thường 6 tháng/lần), DMac của TPCP 10Y với coupon 5% và yield 3.5% vào khoảng **8.2-8.5 năm**. Điều này có nghĩa nếu yield tăng 100bps, giá trái phiếu giảm xấp xỉ **8.2-8.5%** (trước khi điều chỉnh convexity).

### 1.2. Modified Duration (DMod)

Modified duration đo độ nhạy giá với thay đổi yield:

$$D_{Mod} = \frac{D_{Mac}}{1 + y}$$

Với yield hàng năm, DMod ≈ DMac / (1+y). Khi yield thấp (~3%), DMod gần DMac. Khi yield cao (~5.5%), DMod thấp hơn DMac khoảng 5%.

**Đơn vị tại VN:** $\Delta P \approx -D_{Mod} \cdot \Delta y \cdot P$

Ví dụ: TPCP 10Y, P = 100, DMod = 8.0, yield tăng 50bps:
$\Delta P \approx -8.0 \times 0.005 \times 100 = -4.0$ (giá giảm ~4%).

### 1.3. DV01 (Dollar Value of 01)

DV01 đo thay đổi giá trị danh mục khi yield thay đổi 1 basis point (0.01%):

$$DV01 = D_{Mod} \times P \times 0.0001$$

**Ví dụ thực tế VN:** Một ngân hàng nắm giữ 2.000 tỷ VND TPCP 10Y với DMod = 8.0:
- DV01 portfolio ≈ 2.000 tỷ × 8.0 × 0.0001 = **1,6 tỷ VND/bp**.
- Nếu yield 10Y tăng 25bps trong một ngày, portfolio mất ~40 tỷ VND mark-to-market.
- Để hedge 50% rủi ro, treasury cần bán khống (nếu có công cụ) hoặc giảm duration xuống còn 4.0.

### 1.4. Convexity (C)

Convexity đo độ cong của quan hệ giá-yield, cung cấp điều chỉnh chính xác hơn cho biến động yield lớn:

$$\Delta P \approx -D_{Mod} \cdot \Delta y \cdot P + \frac{1}{2} C \cdot (\Delta y)^2 \cdot P$$

TPCP có convexity dương — khi yield biến động lớn, tác động bất lợi bị giảm nhẹ và tác động có lợi được tăng cường. Với TPCP 10Y coupon 5%, convexity vào khoảng **70-80**.

**Hàm ý:** Trong giai đoạn Q4/2022 khi yield 10Y tăng ~150bps, portfolio TPCP của ngân hàng chịu lỗ mark-to-market lớn. Nhưng nếu ngân hàng giữ đến đáo hạn (hold-to-maturity), convexity không quan trọng — chỉ có duration/reinvestment risk quan trọng.

---

## 2. Key Rate Duration — Phân rã Rủi ro Yield Curve

### 2.1. Khái niệm và Ứng dụng

Key rate duration (KRD) phân rã duration tổng thể thành độ nhạy với từng điểm mốc (key rate) trên yield curve:

$$D_{total} = \sum_{i} KRD_i$$

Với thị trường TPCP VN, các key rate thực dụng là: 1Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y.

### 2.2. KRD cho Danh mục Ngân hàng Thương mại

Giả định một ngân hàng có danh mục TPCP như sau:

| Mã TPCP | Kỳ hạn còn lại | Giá trị (tỷ VND) | Weight | KRD | Contribution |
|---|---|---|---|---|---|
| TPCP 2Y | 1.5Y | 500 | 10% | 1.4 | 0.14 |
| TPCP 5Y | 4.5Y | 1.500 | 30% | 4.1 | 1.23 |
| TPCP 10Y | 9.5Y | 2.500 | 50% | 7.8 | 3.90 |
| TPCP 15Y | 14.0Y | 500 | 10% | 10.2 | 1.02 |
| **Tổng** | | **5.000** | **100%** | | **6.29** |

**Phân tích:** Portfolio có duration tổng ~6.3 năm. Tuy nhiên, rủi ro tập trung ở 10Y (contribution 3.90/6.29 = 62%). Nếu 10Y yield tăng 50bps trong khi 5Y giữ nguyên (bear flattening), portfolio mất nhiều hơn so với dự báo từ parallel shift.

### 2.3. Twist Scenarios và KRD

| Loại Shift | Mô tả | Tác động lên Portfolio Ví dụ |
|---|---|---|
| **Parallel shift up** | Tất cả key rate tăng 50bps | $\Delta P = -6.29 \times 0.005 \times 5.000 \approx -157$ tỷ VND |
| **Bear steepening** | 2Y +25bps, 10Y +75bps | $\Delta P$ lớn hơn parallel (do KRD 10Y cao) |
| **Bear flattening** | 2Y +75bps, 10Y +25bps | $\Delta P$ nhỏ hơn parallel (nhưng short end mất nhiều % hơn) |
| **Bull steepening** | 2Y -50bps, 10Y -10bps | KRD 2Y tác động mạnh. Tốt cho ALM ngắn hạn, xấu cho reinvestment long |
| **Bull flattening** | 2Y -10bps, 10Y -50bps | Tốt nhất cho portfolio dài hạn. KRD 10Y tạo lợi nhuận lớn |

---

## 3. Duration Targeting cho Bank Treasury ALM

### 3.1. Vai trò Treasury Desk trong Ngân hàng VN

Theo phân tích trong framework-thakor-yu-2024.md và macro-vn-credit-cycle.md, khối treasury của ngân hàng VN không chỉ là "profit center" mà còn là **liquidity manager** và **regulatory compliance unit**. Quyết định duration targeting của treasury phụ thuộc vào:

1. **LDR (Loan-to-Deposit Ratio):** LDR cao → cần giữ tài sản ngắn hạn, thanh khoản cao → duration target thấp.
2. **LCR (Liquidity Coverage Ratio):** TPCP là HQLA Level 1. Khi LCR bị ép, treasury mua TPCP ngắn hạn (1-3Y) dù yield thấp.
3. **Room tín dụng:** Hết room → chuyển sang mua TPCP (không tính hoặc tính ít vào room) → tăng cầu TPCP, treasury phải quyết định kỳ hạn.
4. **NIM pressure:** Khi lãi suất huy động tăng nhanh hơn cho vay, treasury có thể chấp nhận duration dài hơn để lock yield cao hơn cost of funds.

### 3.2. Ma trận Duration Target theo Regime

| Regime | LDR | LCR | Room Tín dụng | Duration Target Khuyến nghị | Kỳ hạn Ưu tiên |
|---|---|---|---|---|---|
| **Easing / Dư thanh khoản** | <80% | >120% | Còn nhiều | 3-5 năm | 5Y, 7Y |
| **Mid cycle / Cân bằng** | 80-85% | 110-120% | Vừa đủ | 2-4 năm | 3Y, 5Y |
| **Late cycle / Căng** | >85% | 100-110% | Cạn | 1-3 năm | 2Y, 3Y |
| **Stress / Crisis** | Biến động | <100% | Không quan trọng | <1 năm hoặc hold-to-maturity | Tín phiếu, OMO, 1Y TPCP |

**[DIỄN GIẢI]:** Duration target không phải quyết định độc lập về đầu tư mà là hệ quả của constraint ALM. Treasury desk của VCB trong Q4/2022 (LDR ~85%, LCR bị ép sau SCB crisis) phải giảm duration xuống <2 năm và tăng holdings tín phiếu NHNN thay vì TPCP 10Y.

### 3.3. Duration Gap và Net Interest Income (NII) vs Economic Value

Ngân hàng VN phải cân nhắc hai loại rủi ro lãi suất:

1. **Earnings perspective (NII):** Thay đổi lãi suất ảnh hưởng đến thu nhập lãi thuần trong 1-2 năm tới. Nếu tài sản tái cấp vốn nhanh hơn nguồn vốn (positive gap), lãi suất tăng → NII tăng.
2. **Economic value perspective:** Thay đổi lãi suất ảnh hưởng đến giá trị hiện tại của toàn bộ tài sản và nợ phải trả. Duration gap = D(assets) - D(liabilities) × (Liabilities/Assets).

**Đặc thù VN:** Hầu hết ngân hàng VN có **negative duration gap** (tài sản dài hạn hơn nguồn vốn) do cho vay trung-dài hạn và nguồn vốn chủ yếu là tiền gửi không kỳ hạn/ngắn hạn. Khi lãi suất tăng:
- NII có thể tăng (cho vay tái định giá nhanh hơn tiền gửi trong ngắn hạn).
- Economic value giảm (tài sản dài hạn mất giá nhiều hơn nguồn vốn ngắn hạn).

Theo Thakor-Yu (2024), khi capital buffer mỏng, economic value erosion có thể làm giảm Tier-1, tạo ra vòng xoáy hạn chế lending capacity — đây là lý do NHNN yêu cầu ngân hàng báo cáo interest rate risk trong bảng cân đối (IRRBB).

---

## 4. Duration Targeting cho Insurance ALM

### 4.1. Bảo hiểm Nhân thọ — Liability-Driven Investment (LDI)

Bảo hiểm nhân thọ VN (Bảo Việt, Prudential, Dai-ichi, AIA, Manulife) có nghĩa vụ dài hạn (liabilities) từ hợp đồng bảo hiểm với kỳ hạn 10-30 năm. Mục tiêu ALM là **duration match** giữa assets và liabilities.

| Chỉ tiêu | Giá trị Ước tính | Ghi chú |
|---|---|---|
| Duration liabilities (bảo hiểm nhân thọ) | 12-18 năm | Phụ thuộc vào mix sản phẩm: endowment, whole life, annuity |
| Duration assets trung bình | 8-12 năm | TPCP 10Y-15Y là chủ đạo, TPDN dài hạn, cổ phiếu |
| **Duration gap** | **-4 đến -6 năm** | Assets ngắn hơn liabilities → rủi ro reinvestment |
| Kỳ hạn TPCP ưa thích | 15Y, 20Y, 30Y | Thanh khoản kém, nên thường mua hold-to-maturity |

### 4.2. Reinvestment Risk và Guaranteed Rate

Nhiều hợp đồng bảo hiểm VN có **guaranteed interest rate** (tỷ lệ lãi đảm bảo) 3.5-5.0%/năm. Nếu yield TPCP giảm xuống dưới guaranteed rate, bảo hiểm phải:
1. Chấp nhận biên lợi nhuận âm (negative spread).
2. Tăng allocation vào TPDN/rủi ro cao hơn.
3. Giảm guaranteed rate cho hợp đồng mới (nhưng hợp đồng cũ vẫn ràng buộc).

**Case Study 2020-2021:** Khi TPCP 10Y giảm xuống ~2.8-3.0%, nhiều công ty bảo hiểm gặp áp lực reinvestment risk. Giải pháp phổ biến là mua TPCP 15Y-20Y (dù thanh khoản kém) hoặc tăng allocation cổ phiếu để tăng yield.

### 4.3. Cash Flow Matching và Immunization

Lý thuyết immunization: Nếu duration assets = duration liabilities và convexity assets > convexity liabilities, portfolio được "bảo vệ" khỏi parallel shift. Tuy nhiên:
- **Tại VN:** Khó thực hiện chính xác do thiếu TPCP kỳ hạn dài (>15Y) và cash flow liabilities không xác định chính xác (policyholder có quyền rút trước hạn, surrender risk).
- **BĐS và alternative assets:** Một số bảo hiểm tăng allocation BĐS để tăng yield, nhưng điều này tạo ra concentration risk và liquidity risk thay vì lãi suất risk.

---

## 5. Convexity Hedging trong Các Giai đoạn Yield Curve Biến dạng

### 5.1. Chiến lược Hedging theo Loại Twist

| Scenario | Diễn biến Yield Curve | Chiến lược Convexity Hedge | Công cụ Tại VN |
|---|---|---|---|
| **Bear steepening** | Long end tăng nhiều hơn short end | Giảm KRD dài hạn, tăng KRD ngắn hạn | Bán TPCP 10Y-15Y, mua TPCP 3Y-5Y |
| **Bear flattening** | Short end tăng nhiều hơn long end | Giảm KRD ngắn hạn, tăng KRD dài hạn | Bán TPCP 2Y-3Y, mua TPCP 10Y (nếu có khả năng) |
| **Bull steepening** | Short end giảm nhiều hơn long end | Tăng KRD ngắn hạn, lock short rate | Mua TPCP 2Y-3Y, giữ cash để tái đầu tư |
| **Bull flattening** | Long end giảm nhiều hơn short end | Tăng KRD dài hạn, tận dụng duration | Mua TPCP 10Y-15Y |

### 5.2. Case Study: Q4/2022 Bear Steepening

**Bối cảnh:** NHNN tăng lãi suất điều hành 200bps (Tháng 9-10/2022). TPCP 2Y yield tăng ~150bps, TPCP 10Y yield tăng ~200bps.

**Tác động lên các nhóm:**
- **Ngân hàng có duration dài (>5 năm):** Mark-to-market loss lớn. Ví dụ: portfolio 5.000 tỷ VND, DMod = 6.0, yield tăng 200bps → lỗ ~600 tỷ VND MTM.
- **Bảo hiểm nhân thọ:** Lỗ MTM trên TPCP 10Y-15Y, nhưng nếu hold-to-maturity thì không crystallize. Tuy nhiên, economic value trên báo cáo tài chính giảm.
- **Ngân hàng có duration ngắn (<2 năm):** Lỗ MTM nhỏ hơn. Nhưng khi lãi suất đỉnh, họ phải tái đầu tư ở yield cao → lợi thế về sau.

**Chiến lược convexity hedge hiệu quả:** Một treasury desk nào đã dự báo bear steepening và giảm KRD 10Y từ 60% xuống 30% trong Q3/2022 (bằng cách bán TPCP 10Y, mua TPCP 3Y) sẽ giảm thiệt hại MTM đáng kể. Tuy nhiên, tại VN việc "bán" TPCP 10Y không dễ do thị trường thứ cấp mỏng — thường phải bán cho dealer với discount lớn.

### 5.3. Giới hạn của Convexity Hedging tại VN

1. **Thiếu công cụ phái sinh:** Không có Treasury futures, IRS market không phát triển, không có options on TPCP. Hedge chủ yếu bằng cách điều chỉnh cash portfolio.
2. **Transaction cost cao:** Bid-ask spread TPCP off-the-run rộng. Rebalancing portfolio tạo ra cost đáng kể.
3. **Hold-to-maturity bias:** Nhiều institution không quan tâm MTM vì intend để hold. Convexity hedge chỉ quan trọng cho nhóm quản lý theo MTM (FII, quỹ đầu tư).
4. **Repo market hạn chế:** Khó borrow TPCP để short hedge hoặc tạo synthetic negative duration.

---

## 6. Tự Phản biện và Giới hạn

1. **SỰ KIỆN:** Duration và convexity là công cụ định lượng chuẩn cho fixed income risk management.
2. **DIỄN GIẢI:** Tại VN, ứng dụng bị hạn chế bởi thiếu công cụ phái sinh, thị trường thứ cấp mỏng, và hold-to-maturity behavior.
3. **GIẢ THUYẾT:** Nếu VN phát triển thị trường futures trái phiếu hoặc IRS chuẩn, duration management sẽ chuyển từ "cash-only rebalancing" sang "derivative overlay" — giảm transaction cost và tăng tốc độ điều chỉnh portfolio. Tuy nhiên, điều này cần ít nhất 3-5 năm phát triển thị trường.

---

> **Document Control**
> - Version: v1.0 (Wave 5 — Lane 7)
> - Ngày: 2026-04-19
> - Author: OPVIA Build System
> - Next review: 2026-05-19
> - Related modules: framework-thakor-yu-2024.md, macro-vn-credit-cycle.md, domain-fi-yield-curve-vn.md, domain-fi-ldr-and-bank-funding.md
> - Citations: Fabozzi Bond Markets, Tuckman Fixed Income Securities, CFA Institute
