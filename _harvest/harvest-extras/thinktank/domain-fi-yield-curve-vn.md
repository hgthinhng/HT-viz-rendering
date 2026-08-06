---
title: "Domain FI Yield Curve VN — Đường cong lãi suất Trái phiếu Chính phủ Việt Nam TPCP, Thanh khoản Theo Kỳ hạn, Benchmark Rotation, Dealer Network"
module_type: "domain"
file_name: "domain-fi-yield-curve-vn.md"
purpose: "Phân tích cấu trúc đường cong lãi suất TPCP Việt Nam, thanh khoản theo tenor, cơ chế benchmark rotation, chênh lệch on-the-run/off-the-run, và vai trò dealer network trong định giá yield curve."
primary_triggers:
  - "đường cong lãi suất TPCP"
  - "yield curve Vietnam"
  - "trái phiếu chính phủ 10Y"
  - "lãi suất TPCP 5 năm 10 năm"
  - "benchmark bond VN"
  - "on-the-run off-the-run"
  - "VN government bond yield"
when_to_use:
  - "Khi phân tích cấu trúc lãi suất TPCP, term spread, và độ dốc đường cong (steepening/flattening)."
  - "Khi đánh giá thanh khoản theo kỳ hạn và chọn benchmark để pricing corporate bond spread."
  - "Khi theo dõi hành vi mua/bán TPCP của khối treasury ngân hàng và bảo hiểm."
when_not_to_use:
  - "Không dùng để dự báo giá trái phiếu doanh nghiệp riêng lẻ — cần kết hợp với domain-fi-credit-spreads-vn.md."
  - "Không dùng cho phân tích repo, interbank collateral, hoặc ALM chi tiết — xem domain-fi-ldr-and-bank-funding.md."
related_modules:
  - "framework-thakor-yu-2024.md"
  - "macro-vn-credit-cycle.md"
  - "macro-vn-monetary-policy-nhnn.md"
  - "domain-fi-duration-convexity.md"
  - "domain-fi-credit-spreads-vn.md"
  - "domain-fi-ldr-and-bank-funding.md"
authoritative_citations:
  - "VBMA — Vietnam Bond Market Association (vbma.org.vn)"
  - "NHNN — Thống kê Thị trường Tài chính hàng tháng"
  - "FiinTrade — Government Bond Yield Tracker"
  - "MOF — Lịch phát hành TPCP hàng quý"
  - "Vietcap Fixed Income Strategy (vcsc.com.vn)"
  - "ACBS Macro & Rates Research (acbs.com.vn)"
output_owner: "workflow-deep-dive.md khi phân tích sâu về rates VN; workflow-daily-brief.md khi cập nhật yield close EOD."
---

# Domain FI Yield Curve VN — Đường Cong Lãi Suất TPCP Việt Nam / VN Government Bond Curve

Purpose: Cung cấp lens phân tích đường cong lãi suất trái phiếu chính phủ Việt Nam (TPCP) từ góc nhìn cấu trúc thị trường (market structure), thanh khoản theo tenor, benchmark rotation, và hành vi dealer. Module này dùng dữ liệu thực tế 2020-2026, tập trung vào đặc thù thị trường VN còn non trẻ: thiếu benchmark liên tục, thanh khoản phân mảnh, và vai trò định giá của primary dealer.

Trigger keywords: đường cong lãi suất TPCP, yield curve Vietnam, trái phiếu chính phủ 10Y, lãi suất TPCP 5 năm, benchmark bond, on-the-run off-the-run, VN government bond, term spread, steepening, flattening, primary dealer.

---

## 1. Cấu trúc Đường Cong TPCP Việt Nam

### 1.1. Phổ Kỳ hạn và Thanh khoản

Thị trường TPCP Việt Nam có phổ kỳ hạn từ 1 năm đến 30 năm, nhưng thanh khoản tập trung cực kỳ không đều:

| Kỳ hạn | Tình trạng Thanh khoản | Vai trò Benchmark | Ghi chú |
|---|---|---|---|
| **1Y, 2Y** | Thấp | Không có | Ít phát hành, chủ yếu đáp ứng nhu cầu ngắn hạn của NHNN và Bộ Tài chính |
| **3Y** | Trung bình-thấp | Phụ | Thanh khoản kém hơn 5Y, thường được dùng cho ALM ngắn hạn của bảo hiểm |
| **5Y** | **Cao** | **Benchmark phụ** | Kỳ hạn thanh khoản nhì toàn thị trường. Yield 5Y là anchor cho pricing TPDN ngắn hạn |
| **7Y** | Trung bình | Không chính thức | Thanh khoản kém hơn rõ rệt so với 5Y và 10Y |
| **10Y** | **Cao nhất** | **Benchmark chính** | Kỳ hạn quan trọng nhất. Yield 10Y TPCP = risk-free rate reference cho mọi tài sản VN |
| **15Y, 20Y, 30Y** | Rất thấp | Không có | Phát hành ít, nhu cầu chủ yếu từ bảo hiểm nhân thọ dài hạn. Bid-ask spread rộng |

**Đặc thù then chốt:** Thị trường TPCP VN không có benchmark 10Y liên tục (continuous benchmark) như UST 10Y. Mỗi đợt phát hành là một mã riêng biệt, với khối lượng lưu hành giảm dần theo thờii gian do NHNN mua lại (buyback) hoặc đáo hạn. Do đó, "10Y TPCP yield" thực chất là yield của **phiên bản phát hành gần nhất có kỳ hạn còn lại ~10Y** — đây là nguồn "noise" đáng kể trong so sánh chuỗi thờii gian.

### 1.2. Lộ Trình Yield 10Y TPCP Thực Tế 2020-2026

| Thờii điểm | Yield 10Y TPCP (%) | Bối cảnh Vĩ mô | Lãi suất Tái cấp vốn | Term Spread (10Y-2Y proxy) |
|---|---|---|---|---|
| **Q1/2020** | ~3.0% | Pre-COVID, thanh khoản dồi dào | 6.0% | ~50-70bps |
| **Q2-Q3/2020** | ~2.8-3.0% | COVID shock, NHNN giảm lãi suất mạnh, flight-to-quality | 4.0% | ~80-100bps |
| **Q4/2020-Q1/2021** | ~2.8-3.2% | Kỷ nguyên tiền rẻ, FII mua TPCP mạnh | 4.0% | ~100-120bps |
| **H2/2021** | ~3.0-3.5% | Phục hồi kinh tế, lạm phát lo ngại nhẹ | 4.0% | ~100bps |
| **H1/2022** | ~3.5-4.2% | Fed hawkish, DXY mạnh, VND áp lực | 4.0% → 5.0% | ~120-150bps |
| **Q3-Q4/2022** | ~4.5-5.5% | SCB crisis, NHNN tăng lãi suất 200bps, rút vốn ngoại | 6.0% | ~150-200bps |
| **Q1-Q2/2023** | ~4.0-4.8% | NHNN cắt giảm lãi suất 150bps, giảm áp lực | 4.5% | ~120-160bps |
| **H2/2023** | ~3.5-4.0% | Phục hồi TPCP, FII quay lại mua | 4.5% | ~100-130bps |
| **2024** | ~3.0-3.8% | Ổn định, thanh khoản OMO dồi dào, credit growth mạnh | 4.5% | ~80-120bps |
| **2025 (Dự báo)** | ~3.0-3.5% | Fed có thể cắt giảm, VND ổn định | 4.0-4.5% | ~80-110bps |
| **2026 (Outlook)** | ~3.2-3.8% | Bình thường hóa, Basel III tác động đến nhu cầu TPCP | 4.5% | ~90-120bps |

**[DỮ LIỆU THIẾU]:** Yield TPCP 10Y không có chuỗi thờii gian liên tục do benchmark rotation. Các broker (Vietcap, ACBS, MBS) tự xây dựng "synthetic 10Y yield" bằng cách nội suy giữa các phiên bản phát hành gần nhất. Số liệu trên là tổng hợp từ nhiều nguồn và có thể chênh lệch ±20-30bps giữa các nguồn.

---

## 2. Benchmark Rotation và On-the-Run / Off-the-Run

### 2.1. Cơ chế Benchmark Rotation ở VN

Khác với UST có benchmark on-the-run được phát hành định kỳ (reopening), TPCP Việt Nam được phát hành theo lịch đấu thầu định kỳ của Kho bạc Nhà nước (thông qua MOF và Sở Giao dịch Chứng khoán Hà Nội — HNX). Mỗi đợt phát hành tạo ra một mã trái phiếu mới, và "benchmark" được thị trường tự chọn — thường là mã có khối lượng lưu hành lớn nhất và giao dịch gần nhất với kỳ hạn mục tiêu.

| Đặc điểm | UST (Mỹ) | TPCP (Việt Nam) |
|---|---|---|
| Phát hành benchmark | Định kỳ, reopening | Đấu thầu định kỳ, mã mới mỗi đợt |
| On-the-run | Rõ ràng: phiên bản phát hành gần nhất | Mờ nhạt: thị trường tự chọn mã thanh khoản nhất |
| Off-the-run discount | ~5-15bps | ~10-30bps (biến động lớn do thanh khoản kém) |
| Khối lượng lưu hành trung bình | Hàng trăm tỷ USD | 5.000-20.000 tỷ VND (~200-800 triệu USD) |
| Giao dịch thứ cấp | Rất sâu | Mỏng, chủ yếu OTC qua dealer |

### 2.2. Chênh lệch On-the-Run / Off-the-Run (OTR/OFR Gap)

Tại VN, chênh lệch OTR/OFR lớn hơn đáng kể so với thị trường phát triển do:

1. **Khối lượng lưu hành nhỏ:** Mỗi mã TPCP chỉ 5.000-20.000 tỷ VND. Khi một mã trở thành "cũ" (off-the-run), giao dịch gần như ngừng lại.
2. **Không có repo market sâu:** Khó vay/bán khống TPCP off-the-run để hedge, làm tăng illiquidity premium.
3. **Buy-and-hold behavior:** Ngân hàng và bảo hiểm mua TPCP để nắm giữ đến đáo hạn (hold-to-maturity), làm giảm thanh khoản thứ cấp.

**[DỮ LIỆU THỰC NGHIỆM]:** Trong giai đoạn 2022-2023, chênh lệch yield giữa TPCP on-the-run 10Y (phiên bản phát hành gần nhất) và off-the-run 10Y (phiên bản 1-2 năm trước) dao động **15-35bps**, so với ~5-10bps của UST trong cùng giai đoạn.

### 2.3. Hàm Ý cho Pricing và Risk Management

- **Pricing corporate bond spread:** Spread thường được tính so với TPCP on-the-run cùng kỳ hạn. Nếu benchmark đổi (rotation), spread có thể "nhảy" giả tạo do chuyển đổi benchmark chứ không phải do credit risk thay đổi.
- **Duration và DV01:** Khi benchmark rotate, modified duration của "10Y benchmark" thay đổi nhẹ (từ ~8.5 xuống ~7.8 nếu kỳ hạn còn lại giảm từ 10.5Y xuống 9.5Y). Điều này tạo ra "duration drift" trong portfolio tracking.
- **Index tracking:** Các chỉ số trái phiếu VN (VD: VBMA Bond Index) phải điều chỉnh benchmark holdings theo quy tắc rebalancing định kỳ, tạo ra flow predictable nhưng đôi khi disruptive.

---

## 3. Dealer Network và Market Making

### 3.1. Cấu trúc Primary Dealer tại VN

Thị trường TPCP VN hoạt động theo mô hình **dealer-centric**, không phải **order-driven exchange** như cổ phiếu. Primary Dealer (PD) được NHNN và MOF chỉ định, có nghĩa vụ tham gia đấu thầu phát hành sơ cấp và duy trì thanh khoản thứ cấp.

| Nhóm Dealer | Vai trò | Đặc điểm |
|---|---|---|
| **Ngân hàng thương mại lớn** (VCB, BID, CTG, TCB, ACB, MBB) | Market maker chính | Chiếm ~70-80% giao dịch TPCP. Treasury desk quyết định bid/offer |
| **Ngân hàng nước ngoài** (StanChart, HSBC, Citi, Deutsche) | Cầu nối FII | Chủ yếu giao dịch cho khách hàng FII. Giúp price discovery theo chuẩn quốc tế |
| **Công ty chứng khoán lớn** (SSI, HCM, VND) | Dealer phụ | Tham gia đấu thầu, market making nhỏ hơn. Tập trung TPDN hơn TPCP |
| **Quỹ đầu tư / Bảo hiểm** (PVI, Bảo Việt, Prudential) | Price taker | Mua để nắm giữ, không market making |

### 3.2. Hành vi Treasury Desk và Bid-Ask Spread

Treasury desk của ngân hàng VN là ngườii quyết định giá TPCP thứ cấp. Hành vi của họ bị chi phối bởi:

1. **ALM constraint:** Nếu LDR cao, treasury có thể bán TPCP để giải phóng vốn. Nếu dư thanh khoản, họ mua TPCP để đầu tư ngắn hạn.
2. **Regulatory holding:** TPCP được tính là HQLA (High Quality Liquid Asset) trong LCR. Khi LCR bị ép, ngân hàng giữ TPCP dù yield không hấp dẫn.
3. **Room tín dụng:** Khi room cạn, ngân hàng chuyển sang mua TPCP (không tính vào room hoặc tính ít), làm tăng cầu TPCP và nén yield.

**Spread thực nghiệm (bid-ask):**
- TPCP on-the-run 5Y/10Y: **5-15bps** trong điều kiện bình thường.
- TPCP off-the-run hoặc kỳ hạn dài (>15Y): **20-50bps**.
- Trong stress (Q4/2022): Bid-ask 10Y có thể giãn ra **30-60bps** do dealer rút vốn.

---

## 4. Nguồn Cầu TPCP và Tác động lên Yield Curve

### 4.1. Ma trận Nguồn Cầu Theo Nhóm Đầu tư

| Nhóm | Tỷ trọng Danh mục Ước tính | Kỳ hạn Ưa thích | Động lực Chính |
|---|---|---|---|
| **Ngân hàng thương mại** | ~50-55% | 5Y, 10Y | ALM, LCR, room tín dụng thay thế |
| **Bảo hiểm nhân thọ** | ~15-20% | 10Y, 15Y, 20Y | Duration matching với nghĩa vụ dài hạn |
| **FII (quỹ ngoại)** | ~10-15% | 5Y, 10Y | Carry + FX appreciation + index inclusion |
| **Quỹ nội địa / ETFs trái phiếu** | ~5-8% | 5Y, 10Y | Tracking index, retail flow |
| **NHNN (mua lại)** | Biến động | Không cố định | Thanh lý nợ công, điều tiết thanh khoản |

### 4.2. Yield Curve và Chu kỳ Tín dụng

Yield curve TPCP không chỉ phản ánh kỳ vọng lãi suất mà còn phản ánh **tightness của bank funding** (xem framework-thakor-yu-2024.md và macro-vn-credit-cycle.md):

| Giai đoạn | Đặc điểm Yield Curve | Giải thích |
|---|---|---|
| **Easing / Early cycle** | Curve steepening, 10Y-2Y >120bps | Thanh khoản dồi dào, ngân hàng mua TPCP dài hạn để lock yield |
| **Mid cycle expansion** | Curve flattening dần, 10Y-2Y ~80-100bps | Tín dụng tăng, ngân hàng bán TPCP để giải phóng vốn cho cho vay |
| **Late cycle / Tightening** | Bear steepening hoặc inversion, 10Y-2Y volatile | NHNN tăng lãi suất, rủi ro vĩ mô tăng, FII rút vốn |
| **Contraction / Crisis** | Bull steepening, 10Y giảm nhanh hơn 2Y | Flight-to-quality, ngân hàng mua TPCP bất chấp yield thấp |

**Case Study Q4/2022:** Khi NHNN tăng lãi suất 200bps, yield 10Y TPCP tăng từ ~3.8% lên ~5.5% (bear steepening). Tuy nhiên, sau khi lãi suất điều hành ổn định, yield 10Y giảm nhanh hơn yield ngắn hạn do (1) flight-to-quality vào TPCP, (2) ngân hàng bị siết room chuyển sang mua TPCP, (3) kỳ vọng NHNN sẽ cắt giảm lãi suất trong 2023.

---

## 5. Cross-Asset Linkage và Hàm Ý

### 5.1. TPCP là Anchor cho Toàn bộ Hệ thống Giá VN

TPCP yield đóng vai trò **risk-free rate reference** cho:
- **Corporate bond spread:** TPDN được pricing = TPCP cùng kỳ hạn + credit spread.
- **Bank loan pricing:** Lãi suất cho vay dài hạn của ngân hàng thường tham chiếu TPCP 5Y/10Y cộng margin.
- **Equity valuation:** WACC và cost of equity có thành phần risk-free rate lấy từ TPCP 10Y.
- **FX forward pricing:** Interest rate differential VND-USD một phần dựa trên TPCP yield vs UST yield.

### 5.2. UST Anchor và EM Spread

Dù TPCP là nội địa, yield vẫn chịu ảnh hưởng gián tiếp từ UST:
- **UST 10Y tăng →** FII có xu hướng giảm allocation vào EM bond, kể cả TPCP. Yield TPCP 10Y có thể tăng theo nhưng với lag và biên độ nhỏ hơn do capital control.
- **DXY mạnh →** VND bị áp lực, NHNN tăng lãi suất điều hành, đẩy TPCP yield lên.
- **Real yield UST cao →** Opportunity cost của holding TPCP tăng. Tuy nhiên, VN vẫn hấp dẫn FII do (1) FX appreciation kỳ vọng, (2) credit rating upgrade potential, (3) index inclusion (JPM GBI-EM).

---

## 6. Giới hạn Dữ liệu và Cảnh báo

| Khoảng trống | Mô tả | Tác động đến Phân tích |
|---|---|---|
| **Benchmark rotation** | Không có chuỗi 10Y liên tục. Mỗi nguồn tự tính synthetic yield khác nhau | Có thể chênh lệch ±20-30bps giữa các broker. Không nên so sánh chuỗi thờii gian quá chi tiết |
| **Bid-ask thực** | Thị trường OTC, không có central limit order book | Spread báo cáo có thể optimistic. Trong stress, thực tế spread rộng hơn đáng kể |
| **FII flow data** | Không có báo cáo real-time về FII mua/bán TPCP | Phải dựa vào proxy: net foreign inflow bond, FX reserve change, broker commentary |
| **Hold-to-maturity bias** | Ngân hàng + bảo hiểm giữ TPCP đến đáo hạn | Thanh khoản thứ cấp bị thổi phồng (overstated) trong báo cáo. Khối lượng giao dịch không phản ánh khả năng bán thực sự |
| **Repo market thiếu** | Không có repo TPCP chuẩn hóa | Khó short TPCP, khó hedge duration chính xác. Repo rate spread là tín hiệu stress nhưng không có dữ liệu minh bạch |

---

## 7. Tự Phản biện

1. **SỰ KIỆN:** Yield 10Y TPCP dao động ~2.8%-5.5% giai đoạn 2020-2026.
2. **DIỄN GIẢI:** Biên độ dao động lớn phản ánh thị trường non trẻ, nhạy cảm với chính sách NHNN và dòng vốn ngoại.
3. **GIẢ THUYẾT:** Nếu VN được nâng hạng trong JPM GBI-EM hoặc FTSE Russell EM bond index, cấu trúc nguồn cầu TPCP sẽ thay đổi đáng kể (FII tăng, yield nén, curve flatten). Tuy nhiên, điều kiện tiên quyết là cải thiện thanh khoản và benchmark continuity.

---

> **Document Control**
> - Version: v1.0 (Wave 5 — Lane 7)
> - Ngày: 2026-04-19
> - Author: OPVIA Build System
> - Next review: 2026-05-19
> - Related modules: framework-thakor-yu-2024.md, macro-vn-credit-cycle.md, macro-vn-monetary-policy-nhnn.md, domain-fi-duration-convexity.md, domain-fi-credit-spreads-vn.md
> - Data sources: VBMA, NHNN, FiinTrade, MOF, Vietcap, ACBS, HNX
