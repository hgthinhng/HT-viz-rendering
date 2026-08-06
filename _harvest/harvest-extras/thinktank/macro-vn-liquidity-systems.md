---
title: "Macro VN Liquidity Systems — Hệ thống Thanh khoản Ngân hàng Việt Nam: Tích hợp Thakor-Yu + Kashyap-Stein + Brunnermeier-Pedersen"
module_type: "domain"
file_name: "macro-vn-liquidity-systems.md"
purpose: "Khung phân tích tích hợp (P0) về hệ thống thanh khoản Việt Nam, áp dụng ba framework học thuật cốt lõi cho dòng chảy thanh khoản từ NHNN qua NHTM đến nền kinh tế, phân biệt nguồn vốn bán buôn và bán lẻ, và chênh lệch tiếp cận giữa ngân hàng quốc doanh và cổ phần."
primary_triggers:
  - "thanh khoản hệ thống ngân hàng VN"
  - "liquidity systems Vietnam"
  - "interbank VN"
  - "wholesale funding VN"
  - "LDR thanh khoản"
  - "repo TPCP"
  - "SOE bank vs JSB liquidity"
  - "Brunnermeier Pedersen Vietnam"
when_to_use:
  - "Khi phân tích stress thanh khoản, khủng hoảng thanh khoản liên ngân hàng, hoặc rủi ro funding squeeze tại VN."
  - "Khi đánh giá khả năng truyền dẫn chính sách tiền tệ qua kênh thanh khoản."
  - "Khi so sánh vị thế thanh khoản và chi phí vốn giữa SOE bank và private JSB."
when_not_to_use:
  - "Không dùng để dự báo lãi suất cho vay cụ thể từng ngân hàng."
  - "Không dùng cho phân tích thanh khoản doanh nghiệp phi ngân hàng trừ khi có liên kết với hệ thống NHTM."
related_modules:
  - "macro-vn-monetary-policy-nhnn.md"
  - "macro-vn-credit-cycle.md"
  - "macro-vn-transmission-channels.md"
  - "framework-thakor-yu-2024.md"
  - "framework-kashyap-stein-2000.md"
  - "framework-brunnermeier-pedersen-2009.md"
  - "framework-rey-global-financial-cycle.md"
  - "domain-fx-usd-vnd-dynamics.md"
authoritative_citations:
  - "Thakor, A. V., & Yu, E. G. (2024). Funding liquidity creation by banks. Journal of Financial Stability, 73, 101295."
  - "Kashyap, A. K., & Stein, J. C. (2000). What do a million observations on banks say about the transmission of monetary policy? American Economic Review, 90(3), 407-428."
  - "Brunnermeier, M. K., & Pedersen, L. H. (2009). Market liquidity and funding liquidity. Review of Financial Studies, 22(6), 2201-2238."
  - "Báo cáo Thống kê Ngân hàng NHNN (2020-2025)."
  - "IMF Article IV Vietnam (2023-2024)."
output_owner: "workflow-deep-dive.md khi ngườii dùng hỏi về thanh khoản hệ thống; workflow-daily-brief.md khi có biến động OMO/interbank."
---

# Hệ thống Thanh khoản Ngân hàng Việt Nam — Khung Tích hợp P0

**Mục đích:** Tổng hợp ba framework học thuật cốt lõi — **Thakor-Yu (2024)** về bank capital & funding liquidity creation, **Kashyap-Stein (2000)** về bank lending channel, và **Brunnermeier-Pedersen (2009)** về funding-market liquidity spiral — áp dụng cho hệ thống ngân hàng Việt Nam. Module này mô tả dòng chảy thanh khoản từ NHNN → NHTM → nền kinh tế, phân rã nguồn vốn bán buôn (wholesale) và bán lẻ (retail), và phân tích chênh lệch tiếp cận thanh khoản giữa ngân hàng quốc doanh (SOE) và ngân hàng cổ phần (JSB).

**Trạng thái:** [DỮ LIỆU THỰC TẾ 2020-2025 | DỰ BÁO 2025-2026]

---

## 1. Tổng quan Hệ thống Thanh khoản Việt Nam

### 1.1. Sơ đồ Dòng chảy Thanh khoản (Liquidity Flow Map)

Hệ thống thanh khoản Việt Nam vận hành theo hình thái **hub-and-spoke** với NHNN là trung tâm:

```
NHNN (Hub)
  │←→ Dự trữ bắt buộc (RRR)
  │←→ OMO / Tín phiếu NHNN (Repo/Reverse Repo)
  │←→ Tái cấp vốn / Tái chiết khấu
  │←→ Can thiệp FX (mua/bán USD)
  ↓
NHTM (Spokes) — Phân thành:
  ├── Big 4 SOE (VCB, BID, CTG, Agribank): ~45-50% tài sản
  ├── Large Private JSB (TCB, MBB, ACB, VPB): ~25-30% tài sản
  ├── Mid-tier JSB: ~10-15% tài sản
  ├── Small JSB & Foreign Banks: ~10-15% tài sản
  ↓
Nền kinh tế thực:
  ├── Cho vay sản xuất kinh doanh
  ├── Cho vay BĐS (trực tiếp + gián tiếp qua collateral)
  ├── Cho vay tiêu dùng
  └── TPCP / Trái phiếu doanh nghiệp
```

**Nhận định cốt lõi:** Việt Nam là **bank-based economy** với tín dụng ngân hàng ~120-130% GDP. Do đó, thanh khoản hệ thống ngân hàng không chỉ là vấn đề ngành ngân hàng mà là **huyết mạch của toàn bộ nền kinh tế**. Khi funding liquidity của NHTM bị thắt chặt, tác động lan tỏa nhanh hơn và mạnh hơn so với các nền kinh tế dựa trên thị trường vốn.

### 1.2. Phân loại Thanh khoản theo Brunnermeier-Pedersen

Brunnermeier-Pedersen (2009) phân biệt hai loại thanh khoản:

| Loại thanh khoản | Định nghĩa | Ứng dụng VN | Chỉ báo chính |
|---|---|---|---|
| **Funding liquidity** | Khả năng ngân hàng huy động vốn (ngắn hạn và dài hạn) để tài trợ tài sản | Tiền gửi khách hàng, vay liên ngân hàng, phát hành giấy tờ có giá | LDR, deposit growth, interbank rate, CD issuance |
| **Market liquidity** | Khả năng mua/bán tài sản trên thị trường mà không làm biến động giá mạnh | Thanh khoản TPCP, TPDN, cổ phiếu niêm yết, BĐS | Bid-ask spread TPCP, trading volume, repo depth |

**Vòng xoáy thanh khoản (Liquidity Spiral) — Framework cốt lõi:** Khi funding liquidity suy yếu, ngân hàng phải bán tài sản → áp lực bán làm market liquidity giảm → giá tài sản giảm → giá trị collateral giảm → khả năng vay thế chấp giảm → funding liquidity suy yếu hơn. Đây là cơ chế **self-amplifying** đã xuất hiện trong khủng hoảng SCB tháng 10/2022.

---

## 2. Framework Tích hợp Ba Lớp

### 2.1. Lớp 1: Thakor-Yu (2024) — Capital-Liquidity Complementarity

Thakor-Yu đảo ngược trực giác thông thường: **ngân hàng không chỉ cho vay khi có sẵn thanh khoản mà còn tạo ra thanh khoản thông qua cho vay**. Loan creates deposit. Điểm then chốt cho VN: **vốn chủ sở hữu (capital) và thanh khoản là complements, không phải substitutes**.

**Áp dụng cho VN:**
- Khi Basel III siết Tier-1, ngân hàng có capital buffer mỏng không thể mở rộng tín dụng dù có dư thanh khoản từ OMO.
- SOE bank có implicit sovereign support nên deposit franchise mạnh hơn → funding liquidity creation capacity cao hơn JSB cùng quy mô.
- **Proxy VN:** Tăng trưởng tín dụng trừ tăng trưởng tiền gửi khách hàng, điều chỉnh interbank và OMO.

### 2.2. Lớp 2: Kashyap-Stein (2000) — Bank Lending Channel

Monetary policy truyền qua **supply of loans**, không chỉ **demand for loans**. Ngân hàng nhỏ và kém thanh khoản co lending mạnh hơn khi policy tighten.

**Áp dụng cho VN:**
- NHNN không chỉ tác động qua giá (lãi suất) mà còn qua **quantity ceiling (room tín dụng)** — biến VN-specific mà Kashyap-Stein gốc không có.
- Big 4 SOE có liquid asset buffer cao (TPCP, SBV bills, deposit base ổn định) → lending channel yếu hơn → duy trì lending khi policy tighten.
- Small JSB có liquid asset ratio thấp, deposit franchise yếu → lending channel mạnh → bị squeeze đầu tiên.

### 2.3. Lớp 3: Brunnermeier-Pedersen (2009) — Liquidity Spiral

Mối liên hệ hai chiều giữa funding liquidity và market liquidity, với **margin requirement** và **collateral haircut** là kênh amplification.

**Áp dụng cho VN:**
- Thị trường repo TPCP VN còn non trẻ nhưng đang phát triển nhanh. Repo rate deviation từ OMO rate = tín hiệu stress.
- Khi NHNN hút thanh khoản qua tín phiếu (như Q3/2022 và Q2/2024), funding cost tăng → bank bán TPCP → bond yield tăng → giá trị collateral giảm → repo capacity giảm → vòng xoáy.
- **Case study SCB 10/2022:** Rút tiền hàng loạt → funding liquidity sụp đổ → bank bán TPCN và tài sản → market liquidity giảm → spread TPDN tăng vọt → các ngân hàng khác cũng bị ảnh hưởng.

### 2.4. Ma trận Tích hợp Ba Framework

| Biến số / Tình huống | Thakor-Yu | Kashyap-Stein | Brunnermeier-Pedersen |
|---|---|---|---|
| **Basel III siết Tier-1** | Capital buffer mỏng → giảm khả năng tạo funding liquidity | Không trực tiếp | Không trực tiếp |
| **NHNN tăng lãi suất + hút tín phiếu** | Liquidity creation cost tăng | Small/illiquid banks co lending mạnh nhất | Funding liquidity ↓ → market liquidity ↓ → spiral |
| **SCB-style bank run** | Deposit outflow làm mất funding base | Lending channel tắc ở affected bank | Funding ↓↓↓ → fire sale → market freeze |
| **NHNN bơm OMO + nới room** | Tăng khả năng liquidity creation | Large/SOE banks deploy trước | Funding ↑ → market ↑ nhưng asymmetric |
| **BĐS collateral giảm giá** | RWA tăng → capital ăn mòn | Balance sheet channel yếu đi | Collateral haircut tăng → repo ↓ → spiral |

---

## 3. Nguồn Vốn Bán buôn (Wholesale Funding)

### 3.1. Thị trường Liên ngân hàng (Interbank Market)

Thị trường liên ngân hàng VN là **kênh điều tiết thanh khoản ngắn hạn chính**, nhưng độ sâu hạn chế và tính phân hóa cao.

| Chỉ tiêu | Dữ liệu thực tế | Ghi chú |
|---|---|---|
| **Lãi suất qua đêm (ON)** | 0.1% - 8.0% (biên độ cực đại 2020-2025) | Bình thường 0.1-1.0%; stress 5-8% (10/2022) |
| **Lãi suất 1 tuần** | Thường cao hơn ON 20-50bps | Phản ánh kỳ vọng thanh khoản ngắn hạn |
| **Lãi suất 1 tháng** | Theo sát lãi suất tín phiếu NHNN | Less volatile, nhưng ít giao dịch |
| **Khối lượng giao dịch** | [DỮ LIỆU THIẾU công khai chi tiết] | NHNN không công bố daily volume |
| **Tính phân hóa** | Big 4 và large JSB là lender; small JSB là borrower | Spread borrower-lender có thể 100-300bps trong stress |

**VN-specific quirk:** Thị trường liên ngân hàng VN không có **secured interbank lending** phổ biến. Hầu hết là vay không có tài sản đảm bảo (unsecured), dựa trên quan hệ và uy tín. Điều này làm cho small JSB dễ bị **funding rationing** khi có tin đồn về sức khỏe.

### 3.2. Giấy tờ có giá (Certificates of Deposit — CDs)

CD là công cụ huy động vốn bán buôn quan trọng của các JSB khi tiền gửi bán lẻ không đủ.

| Năm | Phát hành CD (tỷ VND, ước tính) | Lãi suất CD 6-12M | Bối cảnh |
|---|---|---|---|
| 2020 | ~50.000 | 4-6% | Thanh khoản dồi dào, CD ít phát hành |
| 2021 | ~80.000 | 5-7% | Tín dụng tăng nhanh, một số JSB bắt đầu phát hành CD |
| 2022 | ~150.000 [DỮ LIỆU THIẾU] | 8-11% | Stress thanh khoản, CD là cứu cánh cho JSB |
| 2023 | ~120.000 [DỮ LIỆU THIẾU] | 7-9% | Hạ nhiệt nhưng vẫn cao hơn 2021 |
| 2024 | ~100.000 [DỮ LIỆU THIẾU] | 6-8% | Thanh khoản cải thiện, lãi suất giảm |
| 2025 (Dự báo) | ~80-100.000 | 5.5-7.5% | Trạng thái bình thường hóa |

**Mối liên hệ với Kashyap-Stein:** JSB phụ thuộc CD nhiều hơn SOE bank → khi thanh khoản căng, JSB phải tăng lãi suất CD mạnh hơn → NIM bị nén → buộc phải giảm lending hoặc tăng spread cho vay.

### 3.3. Repo TPCP và Thị trường Repo

Thị trường repo VN đang phát triển nhưng còn sơ khai. Đây là kênh quan trọng để NHTM quản lý thanh khoản ngắn hạn và tạo collateralized funding.

| Chỉ tiêu | Trạng thái 2024-2025 |
|---|---|
| **Repo rate vs OMO rate** | Thường cao hơn OMO 20-50bps do rủi ro counterparty và illiquidity premium |
| **TPCP làm collateral chính** | Kỳ hạn 2Y, 5Y, 10Y TPCP được chấp nhận; 10Y thanh khoản kém hơn 2Y-5Y |
| **Haircut repo** | 5-15% tùy kỳ hạn TPCP và counterparty |
| **Thanh khoản repo** | Tập trung ở Big 4 và large JSB; small JSB khó tham gia |
| **Repo với NHNN** | Chủ yếu qua OMO repo (bơm thanh khoản) |

**Dấu hiệu stress:** Khi repo rate deviation từ OMO rate vượt 100bps, đây là tín hiệu funding liquidity stress — ngân hàng sẵn sàng trả premium cao để có vốn có collateral.

---

## 4. Nguồn Vốn Bán lẻ (Retail Funding)

### 4.1. Tiền gửi Khách hàng — Trụ cột Thanh khoản

Tiền gửi khách hàng chiếm **75-80% tổng nguồn vốn** của hệ thống ngân hàng VN, là nguồn vốn ổn định nhất.

| Năm | Tổng tiền gửi khách hàng (tỷ VND) | Tăng trưởng YoY | Tỷ trọng tiền gửi / Tổng nguồn vốn |
|---|---|---|---|
| 2020 | ~9.500.000 | ~10% | ~78% |
| 2021 | ~10.800.000 | ~14% | ~77% |
| 2022 | ~12.000.000 | ~11% | ~76% |
| 2023 | ~13.200.000 | ~10% | ~75% |
| 2024 | ~14.500.000 [DỮ LIỆU THIẾU] | ~10% | ~75% |
| 2025 (Dự báo) | ~16.000.000 | ~10% | ~74% |

**Cấu trúc tiền gửi theo kỳ hạn:**
- Không kỳ hạn (CASA): ~15-20% tổng tiền gửi — nguồn vốn rẻ và ổn định nhất.
- Dưới 12 tháng: ~55-60% — nhạy cảm với lãi suất.
- Trên 12 tháng: ~25-30% — ổn định hơn nhưng chi phí cao.

### 4.2. Phân hóa Tiền gửi: SOE Bank vs JSB

| Chỉ tiêu | Big 4 SOE (VCB, BID, CTG, Agribank) | Large Private JSB (TCB, MBB, ACB) | Mid/Small JSB |
|---|---|---|---|
| **Thị phần tiền gửi** | ~50-55% | ~25-30% | ~15-20% |
| **CASA ratio** | VCB ~30%+, CTG/BID ~15-20% | TCB ~35%+, ACB ~30%, MBB ~20% | Thường <15% |
| **Deposit beta** | Thấp (khách hàng trung thành, trust premium) | Trung bình | Cao (phải cạnh tranh lãi suất) |
| **Chi phí huy động** | Thấp nhất hệ thống | Trung bình-thấp | Cao nhất |
| **Stickiness** | Rất cao — khó rút tiền hàng loạt | Cao | Trung bình-thấp |

**Hàm ý theo Thakor-Yu:** SOE bank có **deposit franchise premium** — khả năng huy động vốn ổn định với chi phí thấp hơn → funding liquidity creation capacity cao hơn → có thể duy trì lending khi JSB phải cắt giảm.

### 4.3. "Dollarization" và "Gold-ization" — Rủi ro Thay thế Thanh khoản

Mặc dù đã giảm so với thập kỷ trước, tâm lý chuyển sang USD và vàng khi bất ổn vẫn là rủi ro thanh khoản quan trọng.

- **Tiền gửi USD / Tổng tiền gửi:** ~8-10% (giảm từ ~20% năm 2010).
- **Vàng vật chất nắm giữ:** Ước tính ~400-500 tấn trong dân (~25-30 tỷ USD), tương đương ~25-30% GDP — kênh tích trữ wealth thay thế tiền gửi ngân hàng.
- **Khi stress:** Nếu VND mất giá nhanh hoặc có tin đồn phá giá, dòng chảy từ VND deposit sang USD cash và vàng có thể làm **thanh khoản VND bốc hơi** nhanh chóng.

---

## 5. SOE Bank vs JSB: Chênh lệch Tiếp cận Thanh khoản

### 5.1. Ma trận Tiếp cận Thanh khoản Toàn diện

| Kênh thanh khoản | SOE Bank (Big 4) | Private JSB | Lý do chênh lệch |
|---|---|---|---|
| **OMO / Repo NHNN** | Ưu tiên access | Access bình thường | Quan hệ với NHNN, vai trò điều tiết thị trường |
| **Vay liên ngân hàng** | Lender chính, spread thấp | Borrower, spread cao hơn | Uy tín, deposit base, implicit guarantee |
| **CD issuance** | Ít cần thiết | Phụ thuộc nhiều | Deposit franchise mạnh của SOE |
| **TPCP repo (private)** | Dễ dàng, haircut thấp | Khó hơn, haircut cao | Counterparty risk perception |
| **Vay ngoại tệ quốc tế** | Có sovereign-linked access | Phụ thuộc rating riêng | Implicit sovereign support |
| **NHNN emergency liquidity** | Ưu tiên tuyệt đối | Hạn chế, có điều kiện | "Too big to fail" + policy mandate |
| **Recapitalization** | Vốn nhà nước trực tiếp | Thị trường vốn riêng | Ownership structure |

### 5.2. Ví dụ Thực tế: Khủng hoảng Thanh khoản 10/2022

**Sự kiện:** Sụp đổ niềm tin vào SCB lan sang toàn hệ thống.

| Giai đoạn | SOE Bank | Private JSB | Hệ thống |
|---|---|---|---|
| **Tuần 1 (1-7/10)** | Không bị ảnh hưởng đáng kể | Một số JSB nhỏ bị rút tiền nhẹ | Interbank rate bình thường |
| **Tuần 2 (8-14/10)** | VCB/BID nhận bơm thanh khoản từ NHNN | JSB lớn bắt đầu căng thẳng; tăng lãi suất huy động | Interbank rate tăng lên 3-4% |
| **Tuần 3 (15-21/10)** | Tiếp tục cho vay chính sách theo chỉ đạo | JSB nhỏ gần như đóng băng cho vay mới; bán TPCP | Interbank rate 5-8% |
| **Tuần 4 (22-31/10)** | NHNN tăng lãi suất điều hành 100bps; SOE bank được yêu cầu hỗ trợ thanh khoản hệ thống | JSB phụ thuộc hoàn toàn vào NHNN; một số cần cơ cấu lại | Interbank rate đỉnh ~8-10%; tỷ giá chợ đen vượt 25.000 |

**Bài học theo Brunnermeier-Pedersen:** Funding liquidity stress ở một ngân hàng (SCB) đã lan sang market liquidity (TPCP, TPDN) và quay lại funding liquidity của các ngân hàng khác — đúng cơ chế **liquidity spiral**.

### 5.3. Basel III và Phân hóa Thanh khoản Tương lai

Basel III không chỉ siết capital mà còn siết **liquidity coverage ratio (LCR)** và **net stable funding ratio (NSFR)**.

| Yêu cầu | SOE Bank | Private JSB | Hàm ý |
|---|---|---|---|
| **LCR (HQLA / Net cash outflow 30 ngày)** | Dễ đáp ứng do nhiều TPCP, SBV bills, deposit stable | Khó hơn; cần tăng HQLA hoặc giảm short-term wholesale funding | JSB có thể phải giảm lending để tăng TPCP |
| **NSFR (Stable funding / Required stable funding)** | Dễ đáp ứng do deposit dài hạn ổn định | Khó hơn nếu phụ thuộc CD và interbank | JSB cần chuyển sang deposit dài hạn |
| **HQLA eligibility** | TPCP + SBV bills + deposit tại NHNN | Tương tự nhưng quy mô nhỏ hơn | SOE bank có lợi thế quy mô |

---

## 6. Chỉ báo Giám sát Thanh khoản Hệ thống (Dashboard)

### 6.1. Bảng Chỉ báo Cảnh báo Sớm

| Chỉ báo | Nguồn | Ngưỡng Xanh | Ngưỡng Vàng | Ngưỡng Đỏ | Tần suất |
|---|---|---|---|---|---|
| LDR hệ thống | NHNN | <80% | 80-85% | >85% | Tháng |
| Interbank ON rate / Refinancing rate | NHNN | <0.5x | 0.5-1.5x | >1.5x | Ngày |
| Tăng trưởng tiền gửi - Tăng trưởng tín dụng | NHNN | ±2% | 2-4% | >4% | Tháng |
| Outstanding tín phiếu NHNN | NHNN | <50.000 tỷ | 50-150.000 tỷ | >150.000 tỷ | Tuần |
| FX reserves / Nhập khẩu 3 tháng | NHNN + GSO | >3.5 tháng | 3-3.5 tháng | <3 tháng | Tháng |
| Repo rate - OMO rate | FiinTrade + NHNN | <30bps | 30-80bps | >80bps | Tuần |
| CD rate - Deposit rate trung bình | FiinTrade | <50bps | 50-150bps | >150bps | Tuần |
| TPCP yield 2Y (biến động 1 tháng) | FiinTrade | <30bps | 30-60bps | >60bps | Ngày |

### 6.2. Liquidity Regime Classification

Dựa trên OPVIA Regime v1.1, hệ thống thanh khoản VN có thể được phân loại:

| Regime | Đặc điểm | Chính sách NHNN | Hành vi NHTM | Hàm ý Cross-asset |
|---|---|---|---|---|
| **R1: Dồi dào (Abundant)** | ON <0.5%, LDR <78%, tín phiếu NHNN ít | Nới lỏng hoặc trung tính | Tăng lending, giảm lãi suất cho vay | Equity tích cực; bond yield giảm |
| **R2: Bình thường (Normal)** | ON 0.5-1.5%, LDR 78-83% | Trung tính | Lending bình thường, cạnh tranh vừa phải | Equity trung tính; bond stable |
| **R3: Căng thẳng (Tight)** | ON 1.5-4%, LDR 83-87%, tín phiếu tăng | Hút thanh khoản hoặc FX defense | Giảm lending, tăng huy động, bán TPCP | Equity tiêu cực; bond yield tăng; VND yếu |
| **R4: Stress (Crisis)** | ON >4%, LDR >87% hoặc giảm do deposit rút | Can thiệp mạnh, emergency liquidity | Fire sale, đóng băng cho vay mới | Equity sụt giảm mạnh; bond spread widen; flight to quality |
| **R5: Phục hồi (Recovery)** | ON giảm dần từ cao, LDR ổn định | Bơm thanh khoản, nới room | Thận trọng, tích lũy HQLA | Equity bottoming; bond rally |

---

## 7. Cross-References và Framework Liên kết

| Framework / Module | Tác giả / Nguồn | Vai trò trong Module này | File liên kết |
|---|---|---|---|
| **Bank Capital & Liquidity** | Thakor-Yu (2024) | Capital là điều kiện cần để duy trì funding liquidity creation | `framework-thakor-yu-2024.md` |
| **Bank Lending Channel** | Kashyap-Stein (2000) | Differential lending response khi thanh khoản thay đổi | `framework-kashyap-stein-2000.md` |
| **Funding/Market Liquidity Spiral** | Brunnermeier-Pedersen (2009) | Cơ chế self-amplification trong khủng hoảng thanh khoản | `framework-brunnermeier-pedersen-2009.md` |
| **Global Financial Cycle** | Rey (2015) | Dòng vốn FDI/FII ảnh hưởng thanh khoản VND và khả năng can thiệp FX của NHNN | `framework-rey-global-financial-cycle.md` |
| **Monetary Policy NHNN** | OPVIA | Công cụ điều tiết thanh khoản: OMO, RRR, tín phiếu, FX intervention | `macro-vn-monetary-policy-nhnn.md` |
| **Credit Cycle VN** | OPVIA | Vị trí chu kỳ tín dụng quyết định mức độ căng thẳng thanh khoản | `macro-vn-credit-cycle.md` |
| **FX USD/VND** | OPVIA | Áp lực tỷ giá là nguồn hút thanh khoản VND chính | `domain-fx-usd-vnd-dynamics.md` |
| **Transmission Channels** | OPVIA | Kênh thanh khoản là backbone của monetary transmission tại VN | `macro-vn-transmission-channels.md` |

---

## 8. Tự Phản biện và Giới hạn Dữ liệu

### 8.1. Dữ liệu Chưa Đầy đủ

| Khoảng trống | Mô tả | Tác động |
|---|---|---|
| Khối lượng interbank daily | NHNN không công bố | Khó đo lường chính xác mức độ stress |
| Repo market depth | Thiếu dữ liệu giao dịch repo chi tiết | Proxy bằng TPCP yield và OMO rate có thể không chính xác |
| CD issuance theo ngân hàng | Không có số liệu tổng hợp công khai | Phải dùng ước tính broker |
| HQLA chi tiết theo bank | Basel III LCR chưa công bố đầy đủ | Khó so sánh liquidity position chính xác giữa các NH |

### 8.2. Giả định Quan trọng

1. **Implicit guarantee cho SOE bank:** Giả định này chưa được Chính phủ xác nhận chính thức nhưng được thị trường pricing in. Nếu implicit guarantee bị loại bỏ, chênh lệch thanh khoản SOE-JSB sẽ thu hẹp hoặc đảo chiều.
2. **Deposit stickiness:** Giả định tiền gửi VN có stickiness cao dựa trên lịch sử. Tuy nhiên, SCB 2022 cho thấy bank run vẫn có thể xảy ra với tốc độ rất nhanh trong thờii đại số.
3. **Basel III timeline:** Lộ trình áp dụng LCR/NSFR có thể bị trì hoãn nếu kinh tế suy giảm.

---

> **Document Control**
> - Version: v1.0 (Wave 5 — Lane 11)
> - Ngày: 2026-04-19
> - Author: Wave 5 Lane 11 (Kimi CLI)
> - Approver: OPVIA
> - Next review: 2026-05-19
> - Word count: ~3.200 từ
> - Related modules: macro-vn-monetary-policy-nhnn.md, macro-vn-credit-cycle.md, macro-vn-transmission-channels.md, framework-thakor-yu-2024.md, framework-kashyap-stein-2000.md, framework-brunnermeier-pedersen-2009.md, framework-rey-global-financial-cycle.md, domain-fx-usd-vnd-dynamics.md
