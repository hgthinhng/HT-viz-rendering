---
title: "Fixed Income Bond Supply Demand — VN TPCP Issuance Calendar, Buyer Behavior, Seasonality, and Redemption Dynamics"
module_type: "domain"
file_name: "domain-fi-bond-supply-demand.md"
purpose: "Analyze the supply-demand mechanics of Vietnam government bond market (TPCP): MOF issuance calendar, demand breakdown by investor type (banks, insurance, retail, FII), seasonality patterns, and the interaction between new issuance and redemption schedule."
primary_triggers:
  - "TPCP issuance calendar"
  - "bond supply demand Vietnam"
  - "MOF bond auction"
  - "NHTM mua TPCP"
  - "insurance bond demand"
  - "retail bond investors"
  - "FII bond holding Vietnam"
  - "bond redemption Vietnam"
  - "seasonality TPCP"
when_to_use:
  - "When forecasting TPCP yield direction based on known issuance pipeline and redemption schedule."
  - "When analyzing why a specific TPCP auction failed or was oversubscribed."
  - "When assessing the crowding-out effect of fiscal deficit financing on bank lending capacity."
  - "When evaluating the absorption capacity of the domestic bond market for new supply."
when_not_to_use:
  - "Not for corporate bond (TPDN) supply-demand — see fixed-income/credit-spreads-vn.md."
  - "Not a substitute for understanding why banks buy bonds — see domain-fi-bank-treasury-alm.md for ALM motivation."
  - "Do not use for FX-linked bond or foreign-currency denominated government paper."
related_modules:
  - "domain-fi-bank-treasury-alm.md"
  - "domain-fi-ldr-bank-funding.md"
  - "domain-fi-em-rates-context.md"
  - "macro-vn-credit-cycle.md"
  - "framework-thakor-yu-2024.md"
  - "reference-vn-data-sources.md"
authoritative_citations:
  - "MOF Bond Issuance Calendar (mof.gov.vn — quarterly/annual plan)"
  - "NHNN Statistics: bond market outstanding, ownership by sector"
  - "VBMA Bond Market Report (monthly/quarterly)"
  - "KB Vietnam Securities: Bond Market Strategy"
  - "Vietcap Fixed Income Research"
  - "HNX Bond Market data (hnx.vn)"
output_owner: "workflow-deep-dive.md when user asks about TPCP auction results or issuance pipeline; workflow-daily-brief.md around MOF auction weeks."
---

# Bond Supply Demand — Thị trường TPCP Việt Nam: Cung, Cầu, và Mùa vụ

**Mục đích:** Phân rã cơ chế cung-cầu TPCP: lịch phát hành Bộ Tài chính, cấu trúc nhóm mua, tính mùa vụ, và tương tác giữa phát hành mới với đáo hạn.

**Trạng thái:** [DỮ LIỆU THỰC TẾ 2022-2026 | FRAMEWORK | CẬP NHẬT THEO MOF AUCTION CALENDAR]

---

## 1. Cung — Phía Phát hành TPCP

### 1.1. Cơ chế Phát hành và Lịch đấu thầu

Bộ Tài chính (MOF) phát hành TPCP qua đấu thầu định kỳ tại HNX (Hanoi Stock Exchange), với Kho bạc Nhà nước (KBNN) làm đơn vị tổ chức. Cấu trúc phát hành:

- **Kỳ hạn chuẩn:** 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y.
- **Tần suất đấu thầu:** Thường xuyên nhất là 5Y, 10Y, 15Y; 2Y-3Y ít hơn; 20Y-30Y thưa.
- **Phương thức:** Đấu thầu lãi suất (yield-based auction) — nhà đầu tư nộp bid yield, MOF chấp nhận các bid thấp nhất cho đến khi đủ khối lượng.

**Dữ liệu proxy:** Tổng dư nợ TPCP nội tệ ~2,800-3,000 nghìn tỷ VND (2024-2025, tương đương ~25-28% GDP). Tốc độ tăng dư nợ bình quân ~15-18%/năm, cao hơn GDP growth — indicator của fiscal deficit financing pressure.

### 1.2. Mùa vụ Phát hành (Issuance Seasonality)

| Tháng | Đặc trưng Cung | Lý do |
|---|---|---|
| **Q1 (T1-T3)** | Cao điểm phát hành | Ngân sách cần vốn cho đầu năm, chi đầu tư công khởi động |
| **T4-T5** | Trung bình | Bù đắp thuế giảm sau Tết, nhưng chưa áp lực |
| **Q3 (T7-T9)** | Cao — peak thường T8-T9 | Thu ngân sách chậm giữa năm, chi đầu tư công đẩy mạnh |
| **Q4 (T10-T12)** | Biến động lớn | Phụ thuộc vào bội chi cả năm; nếu thu ngắn hụt → phát hành đột biến T11-T12 |

**Implication:** TPCP yield thường chịu áp lực tăng trong Q1 và Q3 do cung lớn. Ngược lại, Q2 thường là "sweet spot" cho yield giảm nếu cầu ổn định.

### 1.3. Đáo hạn và Tái cấp vốn (Redemption Wall)

Khoảng 15-20% dư nợ TPCP đáo hạn mỗi năm, tập trung ở kỳ hạn 2Y-5Y phát hành 2-3 năm trước. Lịch đáo hạn quan trọng vì:

- **Refinancing risk:** Nếu đáo hạn tập trung trong tháng có phát hành lớn → MOF phải huy động gấp đôi → yield auction tăng.
- **Rollover effect:** MOF thường phát hành kỳ hạn dài hơn để thay thế kỳ hạn ngắn → duration outstanding tăng dần → áp lực lên nhà băng phải mua dài hơn.

---

## 2. Cầu — Phân rã Nhóm Mua TPCP

### 2.1. NHTM (~60-70% dư nợ): Market Maker thực sự

Ngân hàng thương mại là chủ thể nắm giữ TPCP lớn nhất. Tuy nhiên, phải phân biệt:

- **Khối Treasury / ALM:** Mua TPCP để quản lý duration gap, đáp ứng CAR, và dự phòng thanh khoản (HQLA theo Basel III). Hành vi này ổn định, ít phụ thuộc yield.
- **Khối Kinh doanh:** Mua/bán TPCP để săn capital gain khi yield giảm, hoặc carry trade (borrow short, buy long). Hành vi này pro-cyclical — mua nhiều khi yield giảm (FOMO), bán tháo khi yield tăng.

**Chi tiết hành vi:**
- Big 4 (VCB, CTG, BID, Agribank) nắm giữ TPCP chủ yếu vì mục đích ALM + nhiệm vụ chính sách (hỗ trợ MOF). Khẩu vị rủi ro thấp, ưu tiên kỳ hạn 5Y-10Y.
- JSB (Techcombank, MB, ACB, VPBank) linh hoạt hơn: có thể chuyển động mạnh giữa TPCP và cho vay tùy theo NIM expectation và room tín dụng.

### 2.2. Bảo hiểm (~15-20%): Natural Buyer dài hạn

Công ty bảo hiểm nhân thọ (Dai-ichi Life, Prudential, Bảo Việt, Manulife) có liabilities dài hạn (hợp đồng bảo hiểm 10-20 năm) nên cần assets dài để match.

- **Khẩu vị:** Ưu tiên 10Y, 15Y, 20Y. Không bán tháo khi yield tăng ngắn hạn vì hold-to-maturity (HTM).
- **Constraint:** Premium growth (doanh thu phí bảo hiểm mới) quyết định dòng tiền mới đổ vào TPCP. Nếu premium growth chậm → demand giảm.
- **Dữ liệu:** Tổng tài sản ngành bảo hiểm ~800-900 nghìn tỷ VND (2024), trong đó TPCP chiếm ~40-50% danh mục đầu tư.

### 2.3. Nhà đầu tư Cá nhân (~5-10%): Retail Demand

- **Kênh:** Mua qua ngân hàng (phân phối TPCP sơ cấp) hoặc trái phiếu doanh nghiệp (TPDN) — TPCP ít phổ biến với retail hơn TPDN.
- **Đặc điểm:** Sensitive với lãi suất tiết kiệm. Nếu deposit rate 12 tháng > TPCP 5Y yield → retail rỗng.
- **2022-2023 anomaly:** Sau vụ TPDN vỡ nợ (Trung Nam, Tân Hoàng Minh, v.v.), một bộ phận retail chuyển sang TPCP như safe haven → demand tăng đột biến, đặc biệt ở kỳ hạn ngắn.

### 2.4. Nhà đầu tư Nước ngoài (FII) (~3-5%): Marginal but Influential

- **Rào cản:** Capital control, non-deliverable VND, thiếu benchmark 10Y liên tục, và secondary market illiquid.
- **Dòng vốn thực tế:** Chủ yếu qua kênh ETF bond (ít) hoặc direct mandate của pension/sovereign wealth fund Hàn Quốc, Nhật Bản.
- **Tác động biên:** Dù nắm giữ nhỏ, FII là "smart money" signal. Nếu FII net buy TPCP liên tục 2-3 tháng → thường báo hiệu spread VN vs EM đã đủ hấp dẫn.

---

## 3. Cân bằng Cung-Cầu và Tín hiệu Thị trường

### 3.1. Tỷ lệ Trúng thầu (Bid-to-cover ratio)

| Bid-to-cover | Ý nghĩa | Tín hiệu Yield |
|---|---|---|
| >2.0x | Cầu mạnh, oversubscribed | Yield có xu hướng giảm sau auction |
| 1.2-2.0x | Cân bằng | Yield sideway |
| <1.2x | Cầu yếu, undersubscribed hoặc cut-off yield cao | Yield tăng áp lực |
| <1.0x | Failed auction (hiếm ở VN) | Cảnh báo nghiêm trọng về liquidity hoặc yield expectation mismatch |

**Lưu ý VN:** MOF có thể điều chỉnh khối lượng phát hành ngay trong phiên đấu thầu nếu cầu yếu → bid-to-cover ratio ít khi dưới 1.0x. Tuy nhiên, **cut-off yield** mới là tín hiệu quan trọng — nếu cut-off yield cao hơn secondary market 5-10bps → MOF chấp nhận financing cost cao hơn.

### 3.2. Seasonality Demand — Lịch sự kiện Nội địa

| Sự kiện | Tác động Demand | Lý do |
|---|---|---|
| Tháng 1 (sau Tết) | Cầu tăng | Tiền mặt từ tiêu dùng Tết chảy vào hệ thống ngân hàng → dư tiền mua TPCP |
| Tháng 4-5 | Cầu giảm nhẹ | DN bắt đầu vay mùa sản xuất, LDR tăng |
| Tháng 6 | Biến động | Quý 2 báo cáo tài chính, NHNN có thể điều chỉnh room tín dụng |
| Tháng 9-10 | Cầu tăng | Thu ngân sách cuối năm, NHNN thường nới thanh khoản |
| Tháng 12 | Cầu giảm | Ngân hàng giữ tiền mặt dự phòng năm mới, thanh khoản chặt |

---

## 4. Tương tác với Chính sách Tài khóa và Tiền tệ

### 4.1. Crowding-out Effect

Khi MOF phát hành TPCP lớn trong giai đoạn NHNN không nới thanh khoản:
- Nhà băng dùng tiền mua TPCP → giảm room cho vay → credit growth chậm lại.
- NHNN có thể đối trọng bằng OMO injection hoặc nới room tín dụng → nhưng nếu làm cả hai đồng thờ → lạm phát risk.

### 4.2. NHNN as Indirect Buyer

NHNN không mua TPCP trực tiếp (không có QE kiểu Fed), nhưng:
- **OMO collateral:** TPCP là tài sản đảm bảo chính cho OMO repo → nhà băng nắm giữ TPCP có khả năng vay thanh khoản từ NHNN tốt hơn.
- **Standing Lending Facility (SLF):** TPCP được chấp nhận làm collateral → tăng giá trị nắm giữ TPCP vượt ra ngoài yield.

---

## 5. Cross-references

- **domain-fi-bank-treasury-alm.md:** Hành vi mua TPCP của NHTM không chỉ là supply-demand mà còn là ALM optimization.
- **domain-fi-ldr-bank-funding.md:** LDR cao → giảm khả năng mua TPCP dù auction hấp dẫn.
- **macro-vn-credit-cycle.md:** TPCP issuance boom trong giai đoạn credit contraction (2023-2024) là crowding-out điển hình.
- **framework-thakor-yu-2024.md:** Bank capital và HQLA requirement quyết định "mandatory demand" cho TPCP bất kể yield.

---

*Module: domain-fi-bond-supply-demand.md | Wave 5 Lane 8 | OPVIA Sigma*
