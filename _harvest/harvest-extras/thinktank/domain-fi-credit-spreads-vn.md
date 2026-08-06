---
title: "Domain FI Credit Spreads VN — Corporate Bond Spread Việt Nam, Investment Grade vs High Yield, BĐS Bond Crisis 2022-2024, Restructuring Impact, Default Rate vs NPL Divergence"
module_type: "domain"
file_name: "domain-fi-credit-spreads-vn.md"
purpose: "Phân tích spread trái phiếu doanh nghiệp Việt Nam, phân biệt investment grade và high yield, đánh giá tác động của khủng hoảng trái phiếu BĐS 2022-2024 lên risk pricing, và phân tích sự phân kỳ giữa tỷ lệ vỡ nợ trái phiếu thực tế và nợ xấu ngân hàng báo cáo."
primary_triggers:
  - "credit spread trái phiếu doanh nghiệp VN"
  - "TPDN spread"
  - "corporate bond Vietnam"
  - "trái phiếu BĐS vỡ nợ"
  - "default rate TPDN"
  - "investment grade high yield VN"
  - "restructuring trái phiếu"
  - "TPDN vs NPL divergence"
  - "risk pricing corporate bond VN"
when_to_use:
  - "Khi định giá hoặc so sánh spread trái phiếu doanh nghiệp Việt Nam với benchmark TPCP."
  - "Khi đánh giá rủi ro tín dụng của một doanh nghiệp phát hành trái phiếu hoặc một ngành cụ thể (BĐS, ngân hàng, năng lượng)."
  - "Khi theo dõi tiến trình tái cơ cấu nợ trái phiếu sau khủng hoảng 2022-2024."
when_not_to_use:
  - "Không dùng để dự báo giá trái phiếu riêng lẻ mà không có thông tin issuer-specific."
  - "Không dùng cho phân tích cấu trúc lãi suất TPCP — xem domain-fi-yield-curve-vn.md."
related_modules:
  - "framework-thakor-yu-2024.md"
  - "macro-vn-credit-cycle.md"
  - "domain-fi-yield-curve-vn.md"
  - "domain-fi-duration-convexity.md"
  - "macro-vn-monetary-policy-nhnn.md"
authoritative_citations:
  - "VBMA — Vietnam Bond Market Association"
  - "FiinTrade — Corporate Bond Data & Default Tracker"
  - "Vietcap Fixed Income & Credit Research (vcsc.com.vn)"
  - "ACBS Credit Strategy (acbs.com.vn)"
  - "MBS Bond Market Report (mbs.com.vn)"
  - "SSI Research — Corporate Bond Monitor"
  - "NHNN — Thống kê Tín dụng và Nợ xấu"
  - "MOF — Thông tư 16/2021/TT-NHNN, Thông tư 08/2022/TT-NHNN"
output_owner: "workflow-deep-dive.md khi phân tích issuer hoặc sector credit; workflow-daily-brief.md khi có sự kiện default/restructuring mới."
---

# Domain FI Credit Spreads VN — Spread Trái phiếu Doanh nghiệp Việt Nam / TPDN Credit Risk Pricing

Purpose: Cung cấp lens phân tích credit spread và rủi ro tín dụng của thị trường trái phiếu doanh nghiệp Việt Nam (TPDN), với emphasis đặc biệt vào giai đoạn khủng hoảng 2022-2024, cơ chế restructuring, và sự phân kỳ giữa default rate thực tế của TPDN và nợ xấu ngân hàng (NPL) báo cáo. Module này dùng dữ liệu thực tế từ VBMA, NHNN, và báo cáo broker.

Trigger keywords: credit spread TPDN, trái phiếu doanh nghiệp VN, investment grade Vietnam, high yield Vietnam, TPDN BĐS, default rate, restructuring, extend and pretend, TPDN spread widening, NPL divergence, risk pricing.

---

## 1. Cấu trúc Thị trường TPDN và Phân khúc Credit

### 1.1. Quy mô và Cấu trúc Phát hành

Thị trường TPDN Việt Nam tăng trưởng nhanh giai đoạn 2019-2021 nhưng sụp đổ sau khủng hoảng BĐS 2022. Quy mô thị trường hiện tại (2025-2026) ước tính khoảng **1.800.000-2.200.000 tỷ VND** dư nợ lưu hành, giảm từ đỉnh ~2.800.000 tỷ VND năm 2021.

| Chỉ tiêu | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 Ước tính |
|---|---|---|---|---|---|---|
| **Tổng phát hành (tỷ VND)** | ~400.000 | ~600.000 | ~300.000 | ~100.000 | ~80.000 | ~100.000 |
| **Dư nợ lưu hành (tỷ VND)** | ~1.800.000 | ~2.400.000 | ~2.600.000 | ~2.200.000 | ~2.000.000 | ~1.900.000 |
| **Tỷ trọng BĐS** | ~60% | ~70% | ~65% | ~55% | ~50% | ~45% |
| **Lãi suất phát hành TB** | 8-10% | 10-13% | 12-15% | 10-14% | 9-12% | 8-11% |
| **Giá trị giao dịch thứ cấp** | Thấp | Trung bình | Giảm mạnh | Rất thấp | Thấp | Phục hồi nhẹ |

**[DỮ LIỆU THIẾU]:** VBMA công bố dữ liệu phát hành nhưng không có chuỗi thờii gian liên tục về dư nợ theo ngành và chất lượng tín dụng. Số liệu trên là tổng hợp từ báo cáo broker (Vietcap, ACBS, SSI) và có thể chênh lệch ±10-15%.

### 1.2. Phân khúc Credit: Investment Grade vs High Yield

Tại VN không có hệ thống xếp hạng tín nhiệm (credit rating) phát triển như S&P/Moody's/Fitch. Tuy nhiên, thị trường tự phân loại theo:

| Tiêu chí | Investment Grade (IG) Ước tính | High Yield (HY) / Speculative |
|---|---|---|
| **Issuer type** | Ngân hàng (VBSP, VB), SOE lớn (EVN, PVN, Viettel), Tập đoàn nhà nước | BĐS tư nhân (Novaland, Sunshine, FLC, v.v.), DN SME |
| **Bảo lãnh** | Thường có bảo lãnh thanh toán từ ngân hàng lớn hoặc SOE parent | Không có hoặc bảo lãnh từ ngân hàng nhỏ/yếu |
| **Lãi suất phát hành (2024)** | 6.5-8.5% | 10-14% (nếu phát hành được) |
| **Spread vs TPCP 5Y** | 150-300bps | 500-1.500bps (nếu có giao dịch) |
| **Khối lượng phát hành 2024** | Chiếm ~70% tổng phát hành mới | Chiếm ~30%, chủ yếu tái cấu trúc |
| **Thanh khoản thứ cấp** | Có, nhưng hạn chế | Gần như không có (frozen market) |

**[DIỄN GIẢI]:** Phân loại IG/HY tại VN không chính thức. Ngay cả TPDN của DN BĐS lớn như Novaland trước 2022 cũng được xem là "gần IG" do thương hiệu và tài sản đảm bảo. Sự sụp đổ niềm tin năm 2022 cho thấy phân loại này không đáng tin.

---

## 2. Credit Spread Dynamics và Pricing

### 2.1. Công thức Spread và Thành phần

Yield TPDN = Yield TPCP cùng kỳ hạn + Credit Spread

Credit Spread = Default Risk Premium + Liquidity Premium + Recovery Risk Premium + Market Sentiment Premium

Tại VN, do thiếu CDS market và thị trường thứ cấp mỏng, spread thường được ước tính từ:
1. Lãi suất phát hành sơ cấp so với TPCP cùng kỳ hạn.
2. Giá thứ cấp (nếu có giao dịch) so với par.
3. Broker estimate dựa trên comparable issuance.

### 2.2. Lộ Trình Spread Trung bình 2020-2026

| Thờii điểm | TPCP 5Y Yield (%) | TPDN IG Spread (bps) | TPDN HY Spread (bps) | Bối cảnh |
|---|---|---|---|---|
| **Q1/2020** | ~2.8% | ~200-250 | ~400-500 | Pre-COVID, spread ổn định |
| **H2/2020-H1/2021** | ~2.5-3.0% | ~250-350 | ~500-700 | COVID recovery, TPDN bùng nổ |
| **H2/2021** | ~3.0-3.5% | ~300-400 | ~600-900 | Sốt TPDN BĐS, spread nén do cầu mạnh |
| **H1/2022** | ~3.8-4.5% | ~400-600 | ~800-1.200 | Bắt đầu stress, SCB crisis |
| **H2/2022** | ~4.5-5.0% | ~600-900 | ~1.500-3.000+ | Khủng hoảng thanh khoản, spread giãn vỡ |
| **H1/2023** | ~4.0-4.5% | ~500-700 | ~1.200-2.500 | Restructuring ồ ạt, thị trường đóng băng |
| **H2/2023** | ~3.5-4.0% | ~400-600 | ~1.000-2.000 | Phục hồi chọn lọc, IG phát hành trở lại |
| **2024** | ~3.0-3.5% | ~350-500 | ~800-1.500 | IG normalizing, HY vẫn frozen |
| **2025 (Dự báo)** | ~3.0-3.3% | ~300-450 | ~700-1.200 | IG tiếp tục thu hẹp, HY phục hồi chậm |

**[DỮ LIỆU THIẾU]:** Spread HY không có báo giá liên tục. Số liệu trên dựa trên lãi suất phát hành sơ cấp (nếu có) và ước tính recovery value từ broker. Trong giai đoạn 2022-2023, nhiều TPDN HY không có giao dịch — spread là "indicative" hoặc "theoretical".

---

## 3. Khủng hoảng Trái phiếu BĐS 2022-2024: Case Study Spread Widening

### 3.1. Timeline và Cơ chế Sụp đổ

Giai đoạn 2022-2024 là stress test lớn nhất của thị trường TPDN VN. Spread không chỉ widening mà thị trường thứ cấp gần như biến mất (frozen market).

| Giai đoạn | Sự kiện Chính | Tác động lên Spread |
|---|---|---|
| **T10/2021-T3/2022** | NHNN siết TPDN qua Thông tư 16/2021 | Phát hành mới giảm, lãi suất tăng nhẹ |
| **T4-T8/2022** | Nhiều DN BĐS chậm thanh toán coupon | Spread HY bắt đầu giãn từ ~800bps lên ~1.200bps |
| **T9/2022** | Fed tăng lãi suất mạnh, VND áp lực | Tất cả TPDN chịu áp lực, FII rút vốn |
| **T10/2022** | **Sự cố SCB** — Rút tiền hàng loạt | Thanh khoản toàn hệ thống đóng băng. TPDN HY không ai mua |
| **T11/2022-T3/2023** | Novaland, Sunshine, FLC, các DN BĐS lớn vỡ nợ hoặc cầu cứu | Spread HY vỡ mức 2.000-3.000bps. Giá thứ cấp <50 par |
| **T4-T12/2023** | **Restructuring ồ ạt** — Gia hạn, đổi nợ, chuyển đổi thành cổ phiếu | Spread không còn ý nghĩa do không có giao dịch. "Extend and pretend" |
| **2024** | Một số DN BĐS phục hồi (phát hành mới nhỏ) | IG spread thu hẹp về ~350-500bps. HY vẫn frozen |

### 3.2. Case Study: Novaland TPDN

Novaland (NVL) — issuer BĐS lớn nhất trước khủng hoảng:

| Chỉ tiêu | Trước 2022 | 2022-2024 |
|---|---|---|
| **Lãi suất phát hành** | 10.5-12.0% | Không phát hành mới, default/restructuring |
| **Giá thứ cấp** | ~95-100 par | ~20-50 par (OTC indicative, không có giao dịch thực) |
| **Coupon** | Đúng hạn | Ngừng thanh toán, gia hạn, chuyển đổi cổ phiếu |
| **Bảo lãnh NH** | Có (một số) | Vi phạm, litigation, thương lượng |

**[DỮ LIỆU THIẾU]:** Giá OTC indicative, không có độ tin cậy cao.

### 3.3. Tác động lên Ngân hàng — Kênh Truyền Nhiễm

Khủng hoảng TPDN không chỉ giới hạn ở thị trường trái phiếu. Nhiều TPDN BĐS có **bảo lãnh thanh toán từ ngân hàng** hoặc được mua bởi chính các NHTM:

| Kênh truyền nhiễm | Mô tả | Quy mô Ước tính |
|---|---|---|
| **Bảo lãnh phát hành** | Ngân hàng bảo lãnh thanh toán gốc/lãi TPDN | ~200.000-400.000 tỷ VND [DỮ LIỆU THIẾU] |
| **Mua TPDN đầu tư** | Ngân hàng nắm giữ TPDN trong danh mục đầu tư | ~150.000-300.000 tỷ VND [DỮ LIỆU THIẾU] |
| **Cho vay BĐS gián tiếp** | Cho vay dự án BĐS liên quan đến DN phát hành TPDN | ~300.000-500.000 tỷ VND |
| **Collateral overlap** | BĐS làm tài sản đảm bảo cho cả TPDN và vay NH | Không có số liệu tổng hợp |

Theo macro-vn-credit-cycle.md, tổng exposure lên BĐS (trực tiếp + gián tiếp) ước tính **~50-60% tổng tín dụng**. Khủng hoảng TPDN là một phần của khủng hoảng BĐS rộng hơn.

---

## 4. Restructuring Impact trên Risk Pricing

### 4.1. Các Hình thức Restructuring

| Hình thức | Tần suất | Tác động đến Creditor |
|---|---|---|
| **Gia hạn kỳ hạn** | Rất phổ biến | Reinvestment risk kéo dài |
| **Giảm coupon** | Phổ biến | Thu nhập giảm, có thể âm so với cost of funds |
| **Chuyển đổi cổ phiếu** | Trung bình | Haircut lớn do cổ phiếu giảm mạnh |
| **Trả góp (amortization)** | Ít | Giảm recovery risk |
| **Bảo lãnh thay thế** | Rất hiếm | Khó khả thi khi NH cũng bị stress |

### 4.2. "Extend and Pretend" — Hệ quả lên Risk Pricing

Creditor đồng ý gia hạn thay vì crystallize default vì: (1) BĐS giảm sâu — forced sale lỗ lớn, (2) không có thị trường bán distress, (3) áp lực chính trị.

**Tác động lên risk pricing:**
- **Spread báo cáo không phản ánh risk thực:** Gia hạn → spread ~500-800bps thay vì 2.000bps+, nhưng economic loss tương đương default.
- **Moral hazard:** DN có động lực over-issue trong chu kỳ sau.
- **Nợ xấu ngầm:** TPDN restructuring được xếp "performing" — hidden risk lớn.

---

## 5. Default Rate vs Reported NPL Divergence

### 5.1. Sự Phân kỳ Giữa Hai Chỉ báo

| Chỉ báo | Định nghĩa | Nguồn | Ước tính Hiện tại | Vấn đề |
|---|---|---|---|---|
| **NPL Ngân hàng (báo cáo)** | Nhóm 3-5 / Tổng tín dụng | NHNN | ~2.0-2.5% | Bị che bởi Thông tư 01, tái cơ cấu, và extend-and-pretend |
| **NPL điều chỉnh (broker estimate)** | Bao gồm nhóm 2 + tái cơ cấu + nợ xấu ngầm | Vietcap, ACBS | ~5.5-7.5% | Ước tính, không có ground truth |
| **TPDN default rate** | TPDN không thanh toán đúng hạn / Tổng dư nợ TPDN | VBMA + ước tính | ~15-25% (2022-2024) | Không có số liệu tổng hợp chính thức |
| **TPDN restructuring rate** | TPDN đang tái cơ cấu / Tổng dư nợ | VBMA + ước tính | ~20-30% (2023-2024) | Phần lớn chưa crystallize thành default |

**[DỮ LIỆU THIẾU]:** Không có cơ quan nào công bố default rate TPDN tổng hợp hàng quý. VBMA có số liệu phát hành nhưng không theo dõi default. Các số liệu trên là tổng hợp từ báo cáo broker và tin tức về các vụ default công khai.

### 5.2. Giải thích Sự Phân kỳ

Tại sao TPDN default rate (~15-25%) cao gấp 6-10 lần NPL ngân hàng (~2.0-2.5%)?

1. **Forbearance khác biệt:** NH có Thông tư 01/2020, Thông tư 02/2023 để tái cơ cấu và "giấu" NPL. TPDN không có cơ chế tương tự — hết tiền là default công khai.
2. **Sector concentration:** TPDN ~50-70% BĐS (ngành khủng hoảng nặng nhất). Tín dụng NH đa dạng hơn.
3. **Bảo lãnh NH:** Rủi ro TPDN chuyển sang NH qua bảo lãnh, nhưng khi kích hoạt thường xếp vào "cho vay" chứ không phải NPL ngay.
4. **Collateral quality:** TPDN BĐS dùng dự án chưa hoàn thành làm đảm bảo — giá giảm nhanh hơn BĐS hoàn thiện (collateral cho vay NH).
5. **Extend-and-pretend:** Cả hai bên đều áp dụng, nhưng TPDN cấu trúc đơn giản hơn nên khó che giấu hơn.

### 5.3. Hàm Ý cho Phân tích Rủi ro Hệ thống

- **NPL ngân hàng là trailing indicator:** NPL báo cáo phản ánh tình trạng 12-18 tháng trước. TPDN default là leading indicator cho NPL ngân hàng sắp tới (qua kênh bảo lãnh và cho vay BĐS).
- **Nếu TPDN default rate giảm xuống <10%:** Tín hiệu phục hồi thị trường BĐS và tín dụng.
- **Nếu TPDN default rate vẫn >15% trong 2025-2026:** NPL ngân hàng thực tế cao hơn báo cáo. Rủi ro Basel III capital buffer bị ăn mòn.

---

## 6. Cross-References và Framework

| Framework / Module | Tác động đến Credit Spread VN | Vị trí Liên kết |
|---|---|---|
| **Thakor-Yu (2024)** | Capital constraint của ngân hàng ảnh hưởng khả năng bảo lãnh TPDN và mua TPDN distress. Bank treasury là buyer of last resort cho TPDN IG | `framework-thakor-yu-2024.md` |
| **Credit Cycle VN** | Giai đoạn late cycle → TPDN spread widening; giai đoạn contraction → default rate tăng. TPDN là "canary in the coal mine" | `macro-vn-credit-cycle.md` |
| **Yield Curve VN** | Spread = TPDN yield - TPCP benchmark. Thiếu benchmark liên tục làm spread noisy | `domain-fi-yield-curve-vn.md` |
| **Monetary Policy NHNN** | Lãi suất điều hành tác động đến cả TPCP và TPDN, nhưng TPDN HY nhạy hơn do funding risk cao | `macro-vn-monetary-policy-nhnn.md` |
| **Minsky (1986)** | TPDN BĐS 2020-2022 là case study hedge → speculative → Ponzi financing. Khủng hoảng Minsky điển hình | `framework-minsky-1986.md` |

---

## 7. Tự Phản biện và Giới hạn Dữ liệu

1. **SỰ KIỆN:** TPDN BĐS khủng hoảng 2022-2024 với default rate ước tính 15-25% và restructuring rate 20-30%.
2. **DIỄN GIẢI:** Đây là khủng hoảng tín dụng doanh nghiệp nghiêm trọng nhất của VN kể từ 2012. Tuy nhiên, thiếu dữ liệu minh bạch làm giảm khả năng đánh giá chính xác quy mô thiệt hại.
3. **GIẢ THUYẾT:** Nếu BĐS phục hồi thanh khoản (giao dịch tăng, giá ổn định) trong 2025-2026, TPDN HY có thể tái phát hành với spread ~600-800bps. Nếu BĐS tiếp tục đóng băng, default rate có thể tăng thêm do maturity wall 2025-2026. Điều kiện phân biệt: theo dõi giao dịch BĐS sơ cấp, giá TPDN HY thứ cấp, và NPL ngân hàng Q2-Q3/2025.

| Khoảng trống Dữ liệu | Mô tả | Tác động |
|---|---|---|
| **Default rate TPDN chính thức** | Không có cơ quan công bố | Phải dựa vào ước tính broker và tin tức |
| **Giá thứ cấp TPDN** | Không có sàn giao dịch tập trung | Spread HY là indicative, không tradable |
| **Bảo lãnh TPDN chi tiết** | Ngân hàng không công bố đầy đủ exposure bảo lãnh | Khó đánh giá contagion risk |
| **Restructuring terms** | Đa số là thương lượng riêng (private workout) | Không có dữ liệu tổng hợp về haircut rate, extension terms |
| **Collateral value BĐS** | Không có mark-to-market định kỳ | Recovery value là ước tính, có thể optimistic |

---

> **Document Control**
> - Version: v1.0 (Wave 5 — Lane 7)
> - Ngày: 2026-04-19
> - Author: OPVIA Build System
> - Next review: 2026-05-19
> - Related modules: framework-thakor-yu-2024.md, macro-vn-credit-cycle.md, domain-fi-yield-curve-vn.md, domain-fi-duration-convexity.md, macro-vn-monetary-policy-nhnn.md, framework-minsky-1986.md
> - Data sources: VBMA, NHNN, FiinTrade, Vietcap, ACBS, SSI, MBS, MOF
