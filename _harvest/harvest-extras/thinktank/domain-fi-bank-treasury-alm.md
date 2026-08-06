---
title: "Fixed Income Bank Treasury & ALM — NHTM Treasury Desk Behavior, Duration Gap, TPCP Buy/Sell Decisions, NIM vs Capital Gain, SOE vs JSB Differential"
module_type: "domain"
file_name: "domain-fi-bank-treasury-alm.md"
purpose: "Codify the behavior of Vietnam commercial bank treasury desks (khối ALM/treasury) as the dominant force shaping TPCP yield curve: duration gap management, the decision framework for buying vs selling government bonds, NIM vs capital gain trade-off, and structural differences between state-owned banks (SOE) and joint-stock banks (JSB). This is the P0 missing module identified in Lane 4 gap analysis."
primary_triggers:
  - "bank treasury Vietnam"
  - "ALM ngân hàng"
  - "duration gap"
  - "TPCP buy sell decision"
  - "NIM vs capital gain"
  - "SOE bank vs JSB treasury"
  - "yield curve shape Vietnam"
  - "treasury desk behavior"
  - "bank bond portfolio"
  - "HTM AFS HQLA"
when_to_use:
  - "When explaining why the TPCP yield curve has a particular shape (steepening, flattening, inversion risk)."
  - "When analyzing bank quarterly results and need to decompose NIM vs treasury capital gain contribution."
  - "When forecasting TPCP demand shocks based on regulatory changes (Basel III, CAR, LCR)."
  - "When comparing bond portfolio strategy between Big 4 and JSB."
  - "When stress-testing bank profitability under rising yield scenario (capital loss on AFS/HTM)."
when_not_to_use:
  - "Not for non-bank institutional investors (insurance, securities firms) — see domain-fi-bond-supply-demand.md for insurance behavior."
  - "Not for micro-level trade execution or market making mechanics — VN bond market lacks continuous market making."
  - "Do not use as a bank equity valuation model — pair with equity-vn/financial-modeling.md."
related_modules:
  - "domain-fi-bond-supply-demand.md"
  - "domain-fi-ldr-bank-funding.md"
  - "domain-fi-em-rates-context.md"
  - "macro-vn-credit-cycle.md"
  - "macro-vn-monetary-policy-nhnn.md"
  - "framework-thakor-yu-2024.md"
  - "framework-kashyap-stein-2000.md"
  - "framework-regime-v11.md"
authoritative_citations:
  - "NHNN Thông tư 41/2016/TT-NHNN (sửa đổi) về quản lý rủi ro thanh khoản và ALM"
  - "NHNN Thông tư 22/2019/TT-NHNN về giới hạn LDR và an toàn hoạt động ngân hàng"
  - "Basel III: Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio (NSFR) — State Bank implementation roadmap"
  - "BCTC hợp nhất các NHTM niêm yết: VCB, CTG, BID, TCB, MB, ACB, VPB"
  - "FiinTrade Bank Sector: bond portfolio breakdown, HTM/AFS split"
  - "VBMA Bond Market Report: ownership structure and turnover"
  - "IMF Article IV Vietnam (2023-2024): banking sector ALM assessment"
output_owner: "workflow-deep-dive.md when user asks about yield curve drivers, bank treasury strategy, or ALM stress; workflow-daily-brief.md when TPCP yield curve shifts >5bps across tenors."
---

# Bank Treasury & ALM — Hành vi Khối Treasury NHTM và Tác động lên Yield Curve TPCP

**Mục đích:** Giải mã hành vi khối treasury/ALM của ngân hàng VN — market maker thực sự của TPCP — qua quản lý duration gap, quyết định mua/bán, đánh đổi NIM và capital gain, và phân hóa giữa SOE bank và JSB. **Module P0 — thiếu trong hệ thống = không hiểu yield curve.**

**Trạng thái:** [FRAMEWORK + DỮ LIỆU THỰC TẾ 2022-2026 | CẬP NHẬT THEO BCTC QUÝ VÀ NHNN MONTHLY]

---

## 1. Vai trò Khối Treasury trong Hệ thống NHTM VN

### 1.1. Treasury Desk làm gì?

Khối treasury (hoặc ALM — Asset-Liability Management) của NHTM VN có 3 chức năng chính:

1. **Quản lý thanh khoản (Liquidity management):** Đảm bảo ngân hàng có đủ tiền mặt để đáp ứng rút tiền của khách hàng và nghĩa vụ thanh toán. Tools: dự báo cash flow, interbank borrowing/lending, OMO repo với NHNN.
2. **Quản lý rủi ro lãi suất (Interest rate risk / Duration gap):** Điều chỉnh cấu trúc kỳ hạn tài sản và nợ phải trả để hạn chế tổn thất khi lãi suất thay đổi. Tools: mua/bán TPCP để điều chỉnh duration, interest rate swaps (còn hạn chế ở VN).
3. **Tối ưu hóa thu nhập (Income optimization):** Quyết định phân bổ vốn dư thừa giữa cho vay (loan book), TPCP (bond portfolio), và interbank lending.

### 1.2. Tại sao Treasury là Market Maker TPCP?

- NHTM nắm giữ **60-70% dư nợ TPCP** — không có nhóm nhà đầu tư nào lớn hơn.
- Giao dịch thứ cấp TPCP chủ yếu là **inter-dealer** (giữa các NHTM với nhau) hoặc **repo với NHNN**.
- Không có "dealer" chuyên nghiệp độc lập như primary dealer ở UST market. NHTM vừa là investor, vừa là market maker ngầm.

**Kết luận:** Shape của yield curve TPCP (steepness, level, hump) phản ánh **tổng hợp quyết định ALM của 20-25 khối treasury NHTM** chứ không phải expectation của "thị trường" theo nghĩa classical.

---

## 2. Duration Gap Management — Cốt lõi ALM

### 2.1. Định nghĩa và Tính toán

**Duration gap = Duration of assets − (Liabilities / Assets) × Duration of liabilities**

- Nếu duration gap **dương** (assets dài hơn liabilities): Khi lãi suất tăng → giá trị tài sản giảm nhiều hơn nợ phải trả → equity giảm.
- Nếu duration gap **âm** (assets ngắn hơn liabilities): Khi lãi suất giảm → giá trị tài sản tăng ít hơn nợ phải trả → opportunity cost.

**Proxy thực tế VN:**
- Hầu hết NHTM VN có **duration gap dương** vì:
  - Assets: Cho vay trung/dài hạn (BĐS, DN, SME) kỳ hạn 3-5 năm + TPCP 5Y-10Y.
  - Liabilities: Tiền gửi không kỳ hạn (CASA) và tiết kiệm ngắn hạn (<12 tháng) chiếm 70-80%.

### 2.2. Cách Treasury Điều chỉnh Duration Gap

| Hành động Treasury | Tác động Duration Gap | Điều kiện Kích hoạt | Tác động Yield Curve |
|---|---|---|---|
| **Mua TPCP dài hạn (10Y, 15Y)** | Tăng duration gap | Kỳ vọng lãi suất giảm, cần HQLA, hoặc insurance demand dài tăng | Long end yield giảm (flattening) |
| **Bán TPCP dài, mua ngắn (2Y, 3Y)** | Giảm duration gap | Kỳ vọng lãi suất tăng, hoặc Basel III LCR pressure | Long end yield tăng (steepening) |
| **Chuyển TPCP sang HTM từ AFS** | Giảm báo cáo P&L volatility | Yield tăng nhanh, unrealized loss lớn trên AFS | Giảm selling pressure (technical support) |
| **Mua TPCP ngắn thay cho interbank lending** | Giữ duration gap | Thanh khoản dồi dào nhưng không muốn tăng credit risk | Short end yield giảm |

---

## 3. Quyết định Mua/Bán TPCP — Framework Hành vi

### 3.1. Ma trận Quyết định Treasury

Khối treasury không chỉ nhìn yield. Họ nhìn tổng hợp 5 yếu tố:

| Yếu tố | Trọng số | Mua TPCP khi... | Bán TPCP khi... |
|---|---|---|---|
| **LDR / Funding position** | Cao | LDR thấp, dư tiền gửi, room tín dụng cạn | LDR cao, cần tiền cho vay, hoặc interbank stress |
| **Yield expectation** | Trung bình | Kỳ vọng yield giảm (capital gain) | Kỳ vọng yield tăng (capital loss) |
| **Regulatory requirement (HQLA, CAR)** | Cao | Cần HQLA cho LCR, hoặc RWA-efficient asset (TPCP risk weight = 0%) | Không cần thêm HQLA, hoặc cần giải phóng vốn cho cho vay |
| **NIM vs bond yield** | Trung bình | TPCP yield gần hoặc vượt lending rate risk-adjusted | Lending rate rõ ràng cao hơn TPCP yield |
| **NHNN signaling** | Trung bình | NHNN nới thanh khoản, OMO rate giảm | NHNN siết thanh khoản, hoặc can thiệp FX mạnh |

### 3.2. Regulatory Arbitrage — Tại sao TPCP hấp dẫn dù yield thấp?

TPCP có 3 đặc quyền pháp lý làm tăng giá trị "thực" vượt yield:

1. **Risk weight = 0%:** Theo Thông tư 22/2019, TPCP được áp risk weight 0% tính CAR → ngân hàng có thể nắm giữ lượng lớn mà không tiêu hao vốn. Cho vay BĐS risk weight 150%, SME 100% → TPCP rất RWA-efficient.
2. **HQLA (High Quality Liquid Asset):** TPCP là Level 1 HQLA theo Basel III LCR → nắm giữ TPCP cải thiện khả năng vượt LCR mà không cần giữ tiền mặt không sinh lờ.
3. **Collateral cho OMO/SLF:** TPCP được chấp nhận làm tài sản đảm bảo cho vay thanh khoản từ NHNN → tăng tính thanh khoản thực.

**Kết quả:** Ngay cả khi TPCP 10Y yield 3.0% thấp hơn lending rate 8-10%, treasury vẫn có thể mua vì lợi ích pháp lý + capital efficiency.

---

## 4. NIM vs Capital Gain Trade-off

### 4.1. Hai Nguồn Thu từ Bond Portfolio

| Nguồn | Đặc điểm | Kế toán | SOE bank bias | JSB bias |
|---|---|---|---|---|
| **Carry / NIM from bonds** | Coupon yield − funding cost | Thu nhập lãi thuần (NIM) | Ưu tiên — ổn định | Ưu tiên — nhưng nếu yield quá thấp thì không đủ |
| **Capital gain/loss** | Thay đổi giá trái phiếu do yield move | AFS: qua OCI; HTM: không ghi nhận unless sold | Ít quan tâm — HTM dominant | Quan tâm nhiều — AFS dominant, săn capital gain |

### 4.2. HTM vs AFS — Quyết định Chiến lược

- **HTM (Held-to-Maturity):** Ghi nhận theo amortized cost. Không phải đánh giá lại theo giá thị trường. Phù hợp khi treasury muốn "lock in" yield và tránh P&L volatility. Big 4 ưu tiên HTM.
- **AFS (Available-for-Sale):** Ghi nhận theo fair value. Unrealized gain/loss qua OCI (Other Comprehensive Income). Phù hợp khi treasury muốn linh hoạt bán khi cần. JSB dùng AFS nhiều hơn.

**Tác động lên thị trường:**
- Khi yield tăng nhanh (2022): JSB có AFS portfolio lớn → unrealized loss → báo lãi quý giảm hoặc OCI âm → buộc phải bán TPCP để cắt lỗ hoặc reclassify sang HTM. Selling pressure đẩy yield TPCP lên thêm → feedback loop.
- Big 4 ít bị ảnh hưởng vì HTM dominant → không bán → cung ổn định → yield tăng chậm hơn ở long end.

### 4.3. Scenario: Rising Yield Environment

| Giai đoạn | Treasury Response | Yield Curve Impact |
|---|---|---|
| Yield tăng chậm (10-20bps/quý) | JSB chuyển TPCP sang HTM (gọi là "HTM wall") | Long end yield tăng nhưng có ceiling technical |
| Yield tăng nhanh (>30bps/tháng) | JSB bán AFS TPCP, cắt lỗ | Long end yield tăng mạnh, curve steepen |
| Yield tăng + LDR squeeze | Cả SOE và JSB bán TPCP để giữ thanh khoản | Catastrophic — cả curve shift up |
| Yield giảm sau peak | JSB mua lại TPCP để săn capital gain | Rally mạnh ở long end, flattening |

---

## 5. SOE Bank vs JSB — Phân hóa Hành vi Treasury

### 5.1. Ngân hàng Quốc doanh (VCB, CTG, BID, Agribank)

| Đặc điểm Treasury | Biểu hiện |
|---|---|
| **Mục tiêu chính** | ALM stability, tuân thủ regulation, hỗ trợ chính sách MOF |
| **TPCP holding** | Lớn, stable, chủ yếu HTM, kỳ hạn 5Y-10Y |
| **Trading activity** | Thấp — không săn capital gain |
| **Phản ứng yield shock** | Chậm, passive. Không bán tháo. Đôi khi mua thêm khi MOF cần (nhiệm vụ chính sách) |
| **Duration gap** | Quản lý conservative, nhưng không tight hedge |

**Implication cho yield curve:** SOE bank là **stabilizer** — họ cung cấp "base demand" cho TPCP và không tạo selling pressure ngắn hạn.

### 5.2. Joint Stock Banks (Techcombank, MB, ACB, VPBank, HDBank)

| Đặc điểm Treasury | Biểu hiện |
|---|---|
| **Mục tiêu chính** | Tối ưu hóa tổng thu nhập (NIM + fee + treasury gain) |
| **TPCP holding** | Nhỏ hơn SOE, nhưng AFS tỷ trọng cao hơn |
| **Trading activity** | Cao — treasury desk có P&L target |
| **Phản ứng yield shock** | Nhanh, pro-cyclical. Bán khi yield tăng, mua khi yield giảm |
| **Duration gap** | Quản lý active, có thể dùng derivatives (nếu có) |

**Implication cho yield curve:** JSB là **volatile marginal trader** — họ tạo momentum cho yield moves và có thể amplify trend.

### 5.3. Tương tác Giữa Hai Nhóm — Tạo Shape Yield Curve

| Shape Yield Curve | Giải thích qua Hành vi Treasury |
|---|---|
| **Steepening (long end tăng nhiều hơn short end)** | JSB bán TPCP dài để giảm duration gap hoặc cắt lỗ AFS; SOE không đủ mua bù |
| **Flattening (long end giảm nhiều hơn)** | JSB mua TPCP dài săn capital gain; insurance demand dài hỗ trợ |
| **Parallel shift up** | Systemic stress: LDR squeeze + NHNN siết thanh khoản + expectation lãi suất tăng. Cả SOE và JSB đều giảm mua hoặc bán |
| **Hump (5Y cao nhất)** | Short end (<3Y) được hỗ trợ bởi OMO rate + ALM liquidity need; long end (>10Y) được hỗ trợ bởi insurance; 5Y "orphan" — không có natural buyer |

---

## 6. Tại sao ALM Behavior Drives Yield Curve Shape?

### 6.1. Tóm tắt Chuỗi Nhân quả

1. **Regulation (Basel III, LDR, HQLA)** → Xác định "mandatory demand" cho TPCP (đặc biệt short-mid tenor).
2. **LDR và Funding Position** → Xác định "discretionary demand" — có dư tiền để mua thêm không.
3. **Yield Expectation + Duration Gap Target** → Xác định kỳ hạn ưa thích: ngắn (an toàn) hay dài (capital gain).
4. **HTM/AFS Accounting Choice** → Xác định khả năng chịu đựng unrealized loss → quyết định bán hay giữ khi yield tăng.
5. **SOE vs JSB Split** → Xác định tính ổn định của demand: SOE = sticky, JSB = elastic.

**Kết quả cuối cùng:** Yield curve TPCP không phải "expectations hypothesis" thuần túy (lãi suất dài = trung bình lãi suất ngắn kỳ vọng + term premium). Nó là **tổng hợp của balance sheet constraints, regulatory arbitrage, và procyclical trading behavior của 20+ treasury desks.**

### 6.2. Indicator để Theo dõi ALM Stress

| Indicator | Ý nghĩa | Nguồn |
|---|---|---|
| AFS/HTM ratio trong BCTC ngân hàng | Càng cao = càng nhiều unrealized loss risk | BCTC hợp nhất, FiinTrade |
| Unrealized gain/loss on securities (OCI line) | Số liệu trực tiếp về treasury P&L health | BCTC, Notes |
| Bond portfolio yield vs funding cost spread | Carry attractiveness | Tính toán từ BCTC |
| TPCP 5Y-10Y yield change vs 2Y change | Slope change = duration gap adjustment signal | VBMA, NHNN |
| JSB vs SOE TPCP net purchase (quarterly) | Xác định ai đang marginal buyer/seller | VBMA, broker estimates |

---

## 7. Cross-references và Ứng dụng

- **domain-fi-bond-supply-demand.md:** Supply từ MOF cần được hấp thụ bởi treasury demand — nếu ALM stress thì auction có thể fail hoặc cut-off yield cao bất thường.
- **domain-fi-ldr-bank-funding.md:** LDR >85% → treasury không còn dư tiền mua TPCP → demand shock.
- **domain-fi-em-rates-context.md:** UST 10Y move tạo kỳ vọng yield VN — treasury điều chỉnh duration gap dựa trên kỳ vọng này.
- **framework-thakor-yu-2024:** Capital buffer quyết định khả năng treasury nắm giữ TPCP kém thanh khoản dài hạn; liquidity creation cần cả deposit growth và HQLA backing.
- **macro-vn-credit-cycle.md:** Khi credit cycle late-phase, LDR cao + NIM squeeze → treasury capital gain trở thành nguồn bù đắp quan trọng cho lợi nhuận ngân hàng → incentive săn capital gain tăng → pro-cyclical risk.
- **framework-regime-v11.md:** Regime shift từ "low volatility, falling yield" sang "rising yield, steepening curve" cần được nhận diện sớm qua hành vi treasury (bán AFS, chuyển HTM, giảm mua dài).

---

*Module: domain-fi-bank-treasury-alm.md | Wave 5 Lane 8 | OPVIA Sigma | **P0 — Kimi Build***
