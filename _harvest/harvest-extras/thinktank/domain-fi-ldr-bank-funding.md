---
title: "Fixed Income LDR & Bank Funding — Loan-to-Deposit Ratio Mechanics, Regulatory Cap, Squeeze Cycles, and Interbank Stress Signals"
module_type: "domain"
file_name: "domain-fi-ldr-bank-funding.md"
purpose: "Explain the mechanics of Loan-to-Deposit Ratio (LDR) in Vietnam banking: regulatory cap at 85%, historical squeeze cycles (especially 2022-2023), interbank market behavior as a funding stress signal, and integration with Thakor-Yu liquidity creation framework."
primary_triggers:
  - "LDR Vietnam"
  - "loan to deposit ratio"
  - "LDR cap 85%"
  - "interbank rate VN"
  - "bank funding stress"
  - "liquidity squeeze 2022"
  - "deposit competition"
  - "SBV LDR regulation"
  - "bank funding gap"
when_to_use:
  - "When analyzing whether banks have room to expand lending or are forced to slow credit growth."
  - "When interbank rates spike abnormally and need interpretation in funding stress context."
  - "When assessing the structural liquidity position of Vietnam banking system vs individual banks."
  - "When connecting LDR dynamics to TPCP demand (high LDR = less bond buying)."
when_not_to_use:
  - "Not for foreign bank branch analysis — they operate under different liquidity rules."
  - "Not a substitute for full ALM duration gap analysis — see domain-fi-bank-treasury-alm.md."
  - "Do not use LDR alone to predict bank stock prices — pair with equity-vn/financial-modeling.md."
related_modules:
  - "domain-fi-bank-treasury-alm.md"
  - "domain-fi-bond-supply-demand.md"
  - "macro-vn-credit-cycle.md"
  - "macro-vn-monetary-policy-nhnn.md"
  - "framework-thakor-yu-2024.md"
  - "framework-kashyap-stein-2000.md"
authoritative_citations:
  - "NHNN Thông tư 19/2016/TT-NHNN (sửa đổi bởi Thông tư 22/2019) về LDR ceiling"
  - "NHNN Thống kê Ngân hàng Hàng tháng"
  - "FiinTrade Bank Sector Dashboard"
  - "VEPR Quarterly Banking Monitor"
  - "IMF Article IV Vietnam (2023-2024): banking sector assessment"
  - "Vietcap / ACBS Banking Sector Strategy"
output_owner: "workflow-deep-dive.md when user asks about bank liquidity or LDR; workflow-daily-brief.md when interbank rate moves >50bps intraday."
---

# LDR & Bank Funding — Cơ chế Tỷ lệ Cho vay/Tiền gửi và Tín hiệu Căng thẳng Thanh khoản

**Mục đích:** Phân tích cơ chế LDR, giới hạn pháp lý 85%, chu kỳ squeeze 2022-2023, và vai trò của thị trường liên ngân hàng (interbank) như chỉ báo stress. Tích hợp với framework Thakor-Yu.

**Trạng thái:** [DỮ LIỆU THỰC TẾ 2020-2026 | FRAMEWORK | CẬP NHẬT THEO NHNN MONTHLY]

---

## 1. Cơ chế LDR — Định nghĩa và Quy định

### 1.1. Định nghĩa và Công thức Pháp lý

Theo Thông tư 19/2016/TT-NHNN (sửa đổi, bổ sung bởi Thông tư 22/2019):

> **LDR = Tổng dư nợ cho vay khách hàng / Tổng tiền gửi khách hàng**

- **Giới hạn:** LDR **không được vượt quá 85%** đối với NHTM Việt Nam.
- **Điều chỉnh:** NHNN có thể nới hoặc siết giới hạn tùy theo điều kiện kinh tế vĩ mô (ví dụ: nới lên 90% trong giai đoạn COVID-19 rồi thu hẹp lại).
- **Scope:** Không tính tiền gửi của các TCTD khác (interbank deposit) vào mẫu số → buộc ngân hàng phải huy động từ dân cư và DN thực.

### 1.2. LDR là Chỉ báo gì?

LDR không chỉ là tuân thủ pháp lý. Nó phản ánh:

1. **Funding structure health:** LDR thấp (~70%) = hệ thống có "chất béo" (fat), dư tiền gửi so với cho vay → room tăng trưởng tín dụng dồi dào.
2. **Funding stress:** LDR cao (>80%) = tiền gửi không đủ tài trợ cho vay → ngân hàng phải vay liên ngân hàng, phát hành giấy tờ có giá, hoặc cạnh tranh lãi suất huy động.
3. **Credit impulse:** Khi LDR toàn hệ thống tăng nhanh từ 75% lên 83% trong 6 tháng → credit growth sắp chạm ceiling → NHNN có thể nới room hoặc hệ thống tự chậm lại.

---

## 2. Chu Kỳ Squeeze LDR 2022-2023: Case Study

### 2.1. Bối cảnh 2022: Tín dụng Bùng nổ sau COVID

- Năm 2022, tăng trưởng tín dụng VN đạt ~14-15% YoY, vượt xa tăng trưởng tiền gửi (~10-11%).
- Nguyên nhân: (1) DN phục hồi sau COVID vay mở rộng sản xuất; (2) BĐS tăng trưởng nóng; (3) NHNN nới room tín dụng sớm.
- Kết quả: LDR toàn ngành tăng từ ~78% (đầu 2022) lên ~85-87% (cuối 2022), vượt ceiling một số ngân hàng.

### 2.2. Squeeze 2022-Q2/2023: Triệu chứng và Hệ quả

| Triệu chứng | Cơ chế | Dữ liệu Proxy |
|---|---|---|
| **Lãi suất huy động tăng nhanh** | Cạnh tranh giành tiền gửi | Deposit rate 12 tháng từ 5.5% lên 8.5-9.5% (cuối 2022, đầu 2023) |
| **Interbank rate spike** | Vay liên ngân hàng bù đắp funding gap | O/N interbank từ 1.5% lên 4-5%, có ngày >6% |
| **TPCP demand giảm** | Không còn dư tiền mua trái phiếu | Một số auction T8-T12/2022 undersubscribed hoặc cut-off yield cao |
| **Room tín dụng cạn** | NHNN giữ room chặt để kiểm soát | Nhiều JSB hết room từ Q3/2022, phải chờ năm mới |
| **NIM compression** | Chi phí huy động tăng nhanh hơn cho vay | NIM một số JSB giảm 30-50bps 2022-2023 |

### 2.3. Giải pháp của NHNN và Ngân hàng

**NHNN:**
- Nới room tín dụng thêm 1.5-2% GDP trong Q4/2022 → nhưng không giải quyết root cause (thiếu tiền gửi).
- Giảm lãi suất điều hành từ Q2/2023 → truyền dẫn chậm do deposit rate sticky.

**Ngân hàng:**
- Big 4 (đặc biệt Agribank, BIDV) có LDR thấp hơn → tiếp tục cho vay, hút thị phần từ JSB.
- JSB buộc phải tăng lãi suất tiết kiệm, bán TPCP, hoặc chậm tăng trưởng tín dụng.
- Techcombank, MB, ACB tăng cường CASA (Current Account Savings Account) ratio để giảm chi phí funding.

---

## 3. Interbank Market — Chỉ báo Stress Thanh khoản

### 3.1. Cấu trúc Thị trường Liên ngân hàng VN

Thị trường liên ngân hàng VN là nơi các NHTM cho vay/ngược lại thanh khoản dư thừa/thiếu hụt qua đêm (O/N) và kỳ hạn (1W, 1M, 3M). Đặc điểm:

- **Chủ yếu O/N:** 80-90% giao dịch là qua đêm → thị trường ngắn hạn, không tạo được yield curve đáng tin.
- **Thanh khoản tập trung:** Top 5 ngân hàng (thường là Big 4 + 1-2 JSB lớn) là lender; JSB nhỏ và ngân hàng mới là borrower.
- **Collateral:** Không bắt buộc collateral cho O/N giữa các NHTM; dựa trên credit line song phương.

### 3.2. Interbank Rate là Tín hiệu gì?

| Mức O/N Interbank | Ý nghĩa | Khả năng LDR Stress | Hành động NHNN |
|---|---|---|---|
| <2.0% | Thanh khoản dồi dào | Thấp | Có thể hút tiền qua OMO phát hành |
| 2.0-3.5% | Bình thường | Trung bình | Theo dõi |
| 3.5-5.0% | Căng thẳng nhẹ — một số ngân hàng thiếu tiền | Cao ở JSB | OMO injection nếu kéo dài |
| >5.0% | Stress nghiêm trọng — funding gap hệ thống hoặc individual bank crisis | Rất cao | SLF, OMO emergency, hoặc can thiệp định tính |

**Sự kiện điển hình:** Tháng 10/2022, O/N interbank tăng vọt lên >6% trong 2-3 ngày do (1) NHNN giảm OMO injection, (2) một số JSB lớn hết room tín dụng nhưng vẫn cần tiền tài trợ cho vay đã cam kết. Sự kiện này buộc NHNN phải nới room và giảm lãi suất điều hành.

### 3.3. Tích hợp Thakor-Yu Framework

Theo Thakor-Yu (2024), **funding liquidity creation** không chỉ cần deposit mà còn cần capital buffer để depositor tin tưởng. Ứng dụng vào VN:

- Khi LDR tăng → ngân hàng cần "vay mượn" funding liquidity thay vì tạo ra từ deposit → chi phí tăng → NIM giảm.
- Nếu capital buffer (CAR, Tier-1) đủ cao, ngân hàng có thể vay interbank hoặc phát hành certificate of deposit (CD) với chi phí hợp lý. Nếu capital mỏng → counterparty risk premium tăng → interbank rate cho bank đó cao hơn thị trường.
- **Proxy Thakor-Yu cho VN:** Tăng trưởng tín dụng trừ tăng trưởng tiền gửi khách hàng = "funding gap". Nếu funding gap >5% trong 2 quý liên tiếp → LDR sẽ chạm ceiling → squeeze sắp xảy ra.

---

## 4. Phân hóa LDR: SOE Bank vs JSB

### 4.1. Big 4 + Agribank (SOE-dominated)

| Đặc điểm | Big 4 | Hệ quả LDR |
|---|---|---|
| Mạng lưới rộng, tiền gửi dân cư sâu | LDR thường 75-82% | Dư địa cho vay, ít stress |
| Nhiệm vụ chính sách | Cho vay ưu đãi lãi suất | LDR có thể cao hơn nhưng được "bảo hiểm" bởi tiền gửi ổn định |
| Vốn nhà nước | CAR cao, Tier-1 chất lượng | Khả năng hấp thụ funding shock tốt |
| Room tín dụng ưu tiên | Được NHNN phân bổ room trước | Ít khi bị "tắc" room |

### 4.2. Joint Stock Banks (JSB)

| Đặc điểm | JSB | Hệ quả LDR |
|---|---|---|
| Phụ thuộc deposit rate cạnh tranh | LDR 80-90%, một số vượt 85% | Dễ rơi vào squeeze |
| Wholesale funding (CD, interbank) | Tỷ trọng cao hơn Big 4 | Nhạy cảm với interbank rate spike |
| Tăng trưởng tín dụng nhanh | Muốn gain market share | Dễ vượt LDR cap nếu không kiểm soát huy động |
| CASA ratio cao (Techcombank, MB) | Giảm chi phí funding | LDR cao nhưng funding cost thấp → NIM vẫn ổn |

---

## 5. Dữ liệu Giám sát và Trigger List

| Indicator | Nguồn | Tần suất | Ngưỡng Cảnh báo |
|---|---|---|---|
| LDR toàn ngành | NHNN | Monthly | >83% (cảnh báo), >85% (critical) |
| LDR theo ngân hàng | FiinTrade, BCTC | Quarterly | >85% individual bank |
| Interbank O/N rate | NHNN | Daily | >4% sustained 3+ ngày |
| Interbank volume | NHNN | Daily | Giảm >30% — thị trường đóng băng |
| Deposit growth YoY | NHNN | Monthly | <Credit growth YoY — gap widening |
| CD issuance volume | HNX, VBMA | Monthly | Tăng đột biến = wholesale funding stress |
| Funding gap (credit − deposit growth) | Tính toán từ NHNN | Monthly | >5% 2 quý liên tiếp |

---

## 6. Cross-references

- **domain-fi-bank-treasury-alm.md:** LDR cao → treasury desk phải chọn giữa cho vay (NIM) và mua TPCP (HQLA + capital gain).
- **domain-fi-bond-supply-demand.md:** LDR squeeze = giảm demand TPCP từ NHTM, đặc biệt JSB.
- **macro-vn-credit-cycle.md:** LDR là leading indicator cho phase chuyển từ "mid cycle" sang "late cycle" hoặc "contraction."
- **framework-thakor-yu-2024.md:** Capital buffer và funding liquidity creation xác định khả năng một ngân hàng vượt qua LDR squeeze mà không bị liquidity crisis.
- **macro-vn-monetary-policy-nhnn.md:** NHNN điều chỉnh OMO rate và room tín dụng để quản lý LDR toàn hệ thống.

---

*Module: domain-fi-ldr-bank-funding.md | Wave 5 Lane 8 | OPVIA Sigma*
