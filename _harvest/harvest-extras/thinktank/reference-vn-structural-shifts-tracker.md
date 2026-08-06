---
title: "Theo dõi Chuyển dịch Cấu trúc Việt Nam 2025–2026"
module_type: "reference"
file_name: "reference-vn-structural-shifts-tracker.md"
purpose: "STANDALONE living document ghi nhận chuyển đổi cấu trúc VN. Dùng để tránh evidence contamination và điều chỉnh time series."
primary_triggers:
  - "chuyển dịch cấu trúc"
  - "structural shift"
  - "structural break"
  - "regime shift"
  - "data history"
  - "policy change"
when_to_use:
  - "Trước time series analysis — kiểm tra structural break."
  - "Khi regime shift alert triggered."
  - "Trong pre-mortem: thesis có implicit assumption về shift không?"
when_not_to_use:
  - "Không thay thế real-time data retrieval."
  - "Không dùng để dự báo."
update_frequency: "Hàng tuần kiểm tra status; hàng quý review."
version: "v1.0 (Wave 6 — Lane 4)"
date: "2026-04-19"
next_review: "2026-07-19"
---

# Theo dõi Chuyển dịch Cấu trúc Việt Nam 2025–2026

> **Nguyên tắc:** Không ghi nhận structural break → pseudo-precision từ data không còn đại diện.
> **Status:** `PLANNED` → `IN-PROGRESS` → `EFFECTIVE` → `MATURE` → `ARCHIVED`
> **Modules:** equity-vn | macro-vn | fx | fixed-income | commodities | cross-asset

---

## I. REGULATORY SHIFTS

### R1. Luật Chứng khoán sửa đổi 2024–2025

| Mục | Nội dung |
|---|---|
| **Shift** | Sửa đổi Luật CK — margin, short-selling, FOL, securities firm licensing |
| **Status** | `EFFECTIVE` — Đã thông qua, triển khai nghị định từng phần |
| **Effective** | Q1–Q2/2025 (từng phần); toàn bộ 2025–2026 |
| **Data impact** | Pre-2025 data về margin, short-selling, FOL không còn đại diện. Liquidity metrics cần adjust. |
| **Monitor** | (1) Short-selling volume hàng ngày; (2) Margin outstanding/GDP; (3) Securities firm được cấp phép margin; (4) Settlement cycle (T+2→T+1/T+0) |
| **Modules** | equity-vn, macro-vn, fx, cross-asset |

### R2. Nới room ngoại (FOL) theo ngành

| Mục | Nội dung |
|---|---|
| **Shift** | FOL relaxation theo lộ trình ngành |
| **Status** | `IN-PROGRESS` — Đang thực hiện từng bước |
| **Effective** | 2024–2026 (ngân hàng 30→49%; một số ngành 50→100%) |
| **Data impact** | Foreign ownership ratio pre-2024 không so sánh trực tiếp được. FII flow cần normalize theo room mới. |
| **Monitor** | (1) FOL utilization rate theo ngành; (2) FII net buy/sell theo sector; (3) Premium/discount mã full-room vs sector median |
| **Modules** | equity-vn, fx |

### R3. Basel III / Tier-1 capital timeline

| Mục | Nội dung |
|---|---|
| **Shift** | Basel III implementation cho ngân hàng VN |
| **Status** | `IN-PROGRESS` — Lộ trình 2024–2028 |
| **Effective** | 2024 (phase-in); CAR nâng dần đến 2028 |
| **Data impact** | **CRITICAL BREAK.** NPL, CAR, ROE pre-2024 không so sánh trực tiếp do định nghĩa vốn, trích lập, RWA thay đổi. |
| **Monitor** | (1) CAR by bank (VCB, CTG, BID, TCB, VPB); (2) CET1 ratio; (3) Credit growth YoY vs CAR trend; (4) RWA density; (5) LLR coverage |
| **Modules** | macro-vn, fixed-income, liquidity-systems, equity-vn (banking) |

### R4. Lộ trình IFRS cho DN niêm yết

| Mục | Nội dung |
|---|---|
| **Shift** | VAS → IFRS migration |
| **Status** | `IN-PROGRESS` — Tier 1 bắt đầu 2025 |
| **Effective** | 2025 (tier 1: ngân hàng + big corp); 2026–2028 (mở rộng) |
| **Data impact** | **CRITICAL BREAK.** BCTC pre/post-IFRS không so sánh trực tiếp. ROE, D/E, P/B, revenue recognition (BĐS) bị break. |
| **Monitor** | (1) Danh sách DN đã chuyển IFRS; (2) Báo cáo song song VAS vs IFRS; (3) Impact on equity/book value |
| **Modules** | equity-vn, vas-ifrs-bridges |

### R5. Luật Đất đai sửa đổi 2024

| Mục | Nội dung |
|---|---|
| **Shift** | Bảng giá đất, thuế, chuyển đổi mục đích sử dụng |
| **Status** | `EFFECTIVE` — Hiệu lực 01/08/2024 |
| **Data impact** | Land cost pre-2024 cần adjust. NAV dự án BĐS thay đổi step-function. |
| **Monitor** | (1) Bảng giá đất mới theo tỉnh/thành; (2) Số dự án được cấp phép; (3) Thủ tục chuyển đổi đất NN → đô thị; (4) Giá đấu thầu đất |
| **Modules** | equity-vn (BĐS), macro-vn |

### R6. Luật Nhà ở / Kinh doanh BĐS sửa đổi

| Mục | Nội dung |
|---|---|
| **Shift** | Cơ chế bán nhà trên giấy, escrow, bảo lãnh ngân hàng |
| **Status** | `EFFECTIVE` — Triển khai 2024–2025 |
| **Data impact** | Doanh thu BĐS ghi nhận chậm hơn. Dòng tiền pre-sales khác biệt. Nợ xấu BĐS thay đổi cấu trúc. |
| **Monitor** | (1) Số dự án được phép bán; (2) Tỷ lệ dự án có bảo lãnh NH; (3) Doanh thu quarterly vs presales; (4) Nợ xấu BĐS NH |
| **Modules** | equity-vn (BĐS), macro-vn, fixed-income |

### R7. Khung xử lý nợ xấu mới

| Mục | Nội dung |
|---|---|
| **Shift** | Thay thế Nghị quyết 42/2017/QH14 bằng cơ chế mới |
| **Status** | `PLANNED` — Đang xây dựng |
| **Effective** | Dự kiến 2025–2026 |
| **Data impact** | NPL, LLR, credit cost pre/post-framework khác biệt do cơ chế bán nợ, VAMC, trích lập thay đổi. |
| **Monitor** | (1) NPL reported vs NPL sold to VAMC; (2) LLR coverage; (3) Credit cost / average loans; (4) NPL bán ra thị trường |
| **Modules** | macro-vn, fixed-income, credit-cycle-vn |

### R8. FATF grey list exit

| Mục | Nội dung |
|---|---|
| **Shift** | VN rút khỏi FATF grey list |
| **Status** | `IN-PROGRESS` |
| **Effective** | 2024–2025 |
| **Data impact** | Compliance cost ngân hàng, fintech. Capital control có thể chặt hơn trong quá trình. |
| **Monitor** | (1) FATF evaluation reports; (2) VASP được cấp phép; (3) Quy định KYC/AML mới; (4) Cross-border remittance friction |
| **Modules** | fx, macro-vn |

### R9. Thay đổi chính sách thuế

| Mục | Nội dung |
|---|---|
| **Shift** | VAT 8% (đã hết hiệu lực); TNDN ưu đãi FDI đang xem xét |
| **Status** | `IN-PROGRESS` — Ad-hoc |
| **Effective** | 2023–2025 |
| **Data impact** | Fiscal revenue bị "noise" từ chính sách tạm thờii. Không so sánh YoY thu ngân sách mà không adjust. |
| **Monitor** | (1) Thu ngân sách từng loại thuế (monthly); (2) Effective tax rate theo ngành; (3) Chính sách thuế mới QH thông qua |
| **Modules** | fiscal-policy-vn, macro-vn, equity-vn |

### R10. Green taxonomy / Sustainable finance

| Mục | Nội dung |
|---|---|
| **Shift** | Hệ thống phân loại dự án "xanh" |
| **Status** | `PLANNED` — Đang xây dựng, chưa bắt buộc |
| **Effective** | 2025–2027 (dự kiến) |
| **Data impact** | Cost of capital ngành carbon-intensive sẽ phân hóa. Pre-2025 data không reflect green premium/discount. |
| **Monitor** | (1) Green bond issuance VN; (2) Taxonomy publication; (3) Carbon disclosure rate DN niêm yết; (4) Chi phí vay xanh vs vay thường |
| **Modules** | fixed-income, equity-vn, commodities |

---

## II. MONETARY / MACRO SHIFTS

### M1. NHNN CBDC exploration

| Mục | Nội dung |
|---|---|
| **Shift** | Digital Dong pilot |
| **Status** | `PLANNED` — Pilot nội bộ |
| **Effective** | 2024–2027 (không timeline công khai) |
| **Data impact** | Nếu scale: OMO mechanics, M0 definition, velocity of money data history bị break. |
| **Monitor** | (1) Thông cáo NHNN về CBDC; (2) Pilot scope; (3) M2/M1 ratio; (4) Digital payment volume; (5) Cash-in-circulation growth |
| **Modules** | monetary-policy-nhnn, liquidity-systems, macro-vn |

### M2. Room tín dụng theo ngành

| Mục | Nội dung |
|---|---|
| **Shift** | Cơ chế điều hành tín dụng theo ngành của NHNN |
| **Status** | `MATURE` — Ad-hoc nhiều năm, 2023–2024 đặc biệt chặt |
| **Effective** | Ad-hoc, không quy tắc cứng |
| **Data impact** | Credit growth theo ngành bị thay đổi cấu trúc bởi administrative directive. Pre-2023 allocation data khác post-2023. |
| **Monitor** | (1) Room tín dụng từng NH; (2) Tín dụng BĐS / tổng tín dụng; (3) Trái phiếu DN phát hành mới; (4) NIM compression |
| **Modules** | monetary-policy-nhnn, credit-cycle-vn, macro-vn |

### M3. Tái cơ cấu trái phiếu doanh nghiệp & BĐS — "Maturity Wall"

| Mục | Nội dung |
|---|---|
| **Shift** | Corporate bond restructuring wave và real estate debt overhang |
| **Status** | `IN-PROGRESS` — Đỉnh đáo hạn 2024–Q2/2026 |
| **Effective** | 2023–Q2/2026 |
| **Data impact** | **CRITICAL BREAK.** Default rate, credit spread, NPL bị "contaminated" bởi extend-and-pretend. Reported NPL là floor. |
| **Monitor** | (1) Bond maturity wall (value đáo hạn theo tháng/quý); (2) Reported vs estimated real default; (3) NPL nhóm 2 + tái cơ cấu; (4) Giá trái phiếu BĐS thứ cấp |
| **Modules** | fixed-income, macro-vn, credit-cycle-vn, equity-vn (BĐS) |

### M4. MoF bond issuance shift

| Mục | Nội dung |
|---|---|
| **Shift** | TPCP chuyển sang dài hạn và benchmark-linked |
| **Status** | `IN-PROGRESS` |
| **Effective** | 2024–2026 |
| **Data impact** | Yield curve shape thay đổi. Bank ALM bị ảnh hưởng do shift short→long tenor. |
| **Monitor** | (1) Issuance calendar và tenor mix; (2) TPCP 10Y vs UST 10Y spread; (3) Bank holding by maturity; (4) Bid/cover ratio |
| **Modules** | fixed-income, macro-vn, liquidity-systems |

### M5. Phân bổ vốn đầu tư công 1 triệu tỷ VND

| Mục | Nội dung |
|---|---|
| **Shift** | Giải ngân vốn đầu tư công quy mô lớn |
| **Status** | `IN-PROGRESS` — Giai đoạn 2021–2025 và 2026–2030 |
| **Effective** | 2021–2030 |
| **Data impact** | Fiscal multiplier và GDP composition thay đổi. Input demand ở quy mô chưa từng có. Pre-2021 public investment ở scale khác. |
| **Monitor** | (1) Giải ngân vốn đầu tư công (monthly); (2) Số dự án khởi công; (3) Giải ngân/kế hoạch; (4) Nợ công do đầu tư công; (5) Giá xi măng, thép |
| **Modules** | fiscal-policy-vn, macro-vn, commodities, equity-vn (xây dựng) |

### M6. Cấp phép ngân hàng số

| Mục | Nội dung |
|---|---|
| **Shift** | Neobank và digital banking partnership (Timo, Cake, v.v.) |
| **Status** | `EFFECTIVE` — Đã cấp dưới dạng hợp tác |
| **Effective** | 2023–2025 |
| **Data impact** | CASA ratio, chi phí huy động, CAC của NH truyền thống bị thay đổi cấu trúc. |
| **Monitor** | (1) CASA market share by bank; (2) Digital transaction volume; (3) CAC; (4) Deposit migration traditional→digital |
| **Modules** | macro-vn, liquidity-systems, equity-vn (ngân hàng) |

---

## III. REAL ECONOMY SHIFTS

### E1. Triển khai Quy hoạch Điện VIII (PDP8)

| Mục | Nội dung |
|---|---|
| **Shift** | Quy hoạch phát triển điện lực VIII — than → LNG + renewable |
| **Status** | `IN-PROGRESS` — Đã phê duyệt, đang giải phóng mặt bằng |
| **Effective** | 2024–2030 |
| **Data impact** | Cost of electricity, cơ cấu nguồn điện, CapEx ngành điện. Pre-2024 cost data không đại diện do LNG passthrough. |
| **Monitor** | (1) LNG import volume & price (JKM); (2) Renewable capacity additions; (3) PPA signed; (4) Giá điện bán lẻ (EVN); (5) Than nhập khẩu |
| **Modules** | commodities, equity-vn (utilities), macro-vn |

### E2. Samsung supply chain relocation — "Vietnam+1"

| Mục | Nội dung |
|---|---|
| **Shift** | FDI Hàn Quốc / Samsung diversification ra khỏi VN |
| **Status** | `IN-PROGRESS` — Structural |
| **Effective** | Từ 2023 |
| **Data impact** | FDI manufacturing, XK điện thoại/máy tính (HS 85xx) pre-2023 có trend khác post-2023. Không extrapolate FDI disbursement. |
| **Monitor** | (1) Samsung VN revenue và headcount; (2) FDI Hàn Quốc disbursement; (3) XK điện thoại/máy tính YoY; (4) New FDI India/Mexico/Indonesia vs VN |
| **Modules** | macro-vn, fx, cross-asset |

### E3. CPTPP / EVFTA / RCEP — Rules of Origin evolution

| Mục | Nội dung |
|---|---|
| **Shift** | Tariff phase-out và RoO compliance |
| **Status** | `EFFECTIVE` — EVFTA 2020; RCEP 2022; CPTPP 2019. Giảm thuế dần 2020–2030 |
| **Effective** | 2020–2030 |
| **Data impact** | Tariff pre-2020 không so sánh được. Export margin phụ thuộc RoO compliance. FDI into export sectors có động lực khác. |
| **Monitor** | (1) Effective tariff rate theo ngành; (2) Tỷ lệ XK hưởng ưu đãi FTA; (3) Số vụ bị từ chối C/O; (4) FDI vào ngành hưởng FTA |
| **Modules** | macro-vn, equity-vn (xuất khẩu) |

### E4. Năng lượng tái tạo — FIT thay đổi sang auction

| Mục | Nội dung |
|---|---|
| **Shift** | FIT giảm dần, chuyển sang đấu thầu |
| **Status** | `EFFECTIVE` |
| **Effective** | 2023–2025 |
| **Data impact** | IRR dự án điện mặt trờii/gió thay đổi. Dự án cũ FIT được bảo vệ, new pipeline margin compress. |
| **Monitor** | (1) FIT mới theo công nghệ; (2) Giá trúng thầu auction; (3) PPA terms (tenor, take-or-pay); (4) Grid connection queue |
| **Modules** | equity-vn (utilities), commodities, macro-vn |

### E5. Thu hút FDI từ Trung Quốc — "dịch chuyển" qua third country

| Mục | Nội dung |
|---|---|
| **Shift** | FDI TQ tăng mạnh, thường qua Singapore/HK |
| **Status** | `IN-PROGRESS` — Tăng 2023–2025, đang bị scrutiny |
| **Effective** | 2023–ongoing |
| **Data impact** | FDI theo quốc gia không còn "sạch." FDI TQ có thể đi qua Singapore/HK. Historical by-country data không reflect new pattern. |
| **Monitor** | (1) FDI đăng ký theo quốc gia (Singapore/HK/Korea tăng đột biến); (2) Dự án bị từ chối vì an ninh; (3) M&A deal value by source |
| **Modules** | macro-vn, fx, cross-asset |

### E6. China+1 / Friend-shoring

| Mục | Nội dung |
|---|---|
| **Shift** | Dịch chuyển chuỗi cung ứng từ "lắp ráp giá rẻ" sang "component manufacturing" |
| **Status** | `IN-PROGRESS` — Structural |
| **Effective** | 2020–2030 |
| **Data impact** | FDI structure và export composition thay đổi. Pre-2020 FDI by sector không đại diện. |
| **Monitor** | (1) FDI theo ngành (manufacturing sub-sectors); (2) XK processing vs ordinary trade; (3) Local content ratio; (4) Component suppliers in VN |
| **Modules** | macro-vn, fx, cross-asset |

### E7. Luật Lao động sửa đổi / tăng lương tối thiểu

| Mục | Nội dung |
|---|---|
| **Shift** | Tăng lương tối thiểu vùng |
| **Status** | `EFFECTIVE` — Tăng ~6% từ 01/07/2024 |
| **Effective** | 01/07/2024 (mới nhất); thường xuyên |
| **Data impact** | Chi phí lao động, biên lợi nhuận ngành labor-intensive thay đổi cấu trúc. CPI có seasonal từ lương tối thiểu. |
| **Monitor** | (1) Lương tối thiểu vùng; (2) Tổng quỹ lương/GDP; (3) Unit labor cost; (4) FDI manufacturing wage vs Cambodia/Indonesia/India |
| **Modules** | macro-vn, equity-vn (manufacturing) |

### E8. Cổ phần hóa / tái cơ cấu DNNN (SOE reform)

| Mục | Nội dung |
|---|---|
| **Shift** | Cổ phần hóa và tái cơ cấu DNNN |
| **Status** | `IN-PROGRESS` — Chậm, ad-hoc |
| **Effective** | 2024–2030 (không timeline cứng) |
| **Data impact** | IPO pipeline, supply cổ phiếu mới. Pre-privatization data không đại diện cho post-privatization (efficiency, ROE, governance). |
| **Monitor** | (1) Danh sách SOE được phê duyệt cổ phần hóa; (2) Tiến độ IPO; (3) Valuation SOE assets; (4) Dividend to state budget |
| **Modules** | fiscal-policy-vn, equity-vn |

---

## IV. MARKET INFRASTRUCTURE SHIFTS

### I1. HOSE-HNX consolidation

| Mục | Nội dung |
|---|---|
| **Shift** | Sáp nhập HOSE và HNX |
| **Status** | `PLANNED` — Đang nghiên cứu |
| **Effective** | Dự kiến 2025–2027 |
| **Data impact** | Liquidity fragmentation giảm, benchmark restructuring, clearing upgrade. Pre-consolidation index data không comparable nếu methodology đổi. |
| **Monitor** | (1) Thông cáo chính thức; (2) Technology platform; (3) Index methodology; (4) Settlement cycle upgrade |
| **Modules** | equity-vn, cross-asset, macro-vn |

### I2. Nâng hạng thị trường chứng khoán (MSCI/FTSE EM)

| Mục | Nội dung |
|---|---|
| **Shift** | Upgrade từ Frontier lên EM chính thức |
| **Status** | `PLANNED` — Trì hoãn do T+2, short-selling, FX convertibility |
| **Effective** | Không xác định (review tháng 6 và 12 hàng năm) |
| **Data impact** | **CRITICAL IF TRIGGERED.** Passive inflow ~3–5 tỷ USD, holder base thay đổi vĩnh viễn. Pre-upgrade data không đại diện cho post-upgrade. |
| **Monitor** | (1) MSCI/FTSE review calendar; (2) Settlement cycle (T+2→T+1/T+0); (3) Short-selling framework; (4) Foreign access improvement |
| **Modules** | equity-vn, fx, cross-asset |

### I3. Mở rộng thị trường phái sinh

| Mục | Nội dung |
|---|---|
| **Shift** | Stock options, bond futures, FX futures (ngoài VN30 futures hiện có) |
| **Status** | `PLANNED` — Đang nghiên cứu |
| **Effective** | 2025–2027 (dự kiến) |
| **Data impact** | Volatility surface, hedging cost, price discovery. Pre-derivatives volatility không comparable. |
| **Monitor** | (1) OI futures VN30; (2) Basis (futures-spot); (3) Put/call ratio (khi có options); (4) Implied volatility |
| **Modules** | equity-vn, cross-asset |

### I4. Bond market restructuring

| Mục | Nội dung |
|---|---|
| **Shift** | Tái cơ cấu thị trường trái phiếu thứ cấp VN |
| **Status** | `IN-PROGRESS` — VBMA xây dựng reference price, market maker framework |
| **Effective** | 2024–2026 |
| **Data impact** | Bond yield pre-restructuring không reflect true market clearing price do illiquidity. VBMA reference yield là estimate, không transaction-based. |
| **Monitor** | (1) Secondary trading volume; (2) Bid-ask spread by tenor; (3) Market maker participation; (4) VBMA reference vs broker quote |
| **Modules** | fixed-income, macro-vn |

---

## V. TOP-5 IMPACT SHIFTS (Summary)

| # | Shift | Data Impact | Key Monitor |
|---|---|---|---|
| T1 | Luật CK + FOL nới | P/E, foreign ownership, turnover pre-2025 cần footnote "pre-reform" | FOL utilization rate; margin outstanding/free-float |
| T2 | Basel III | CAR pre-2024 dùng định nghĩa vốn cũ. Không so sánh CAR 2023 vs 2025 | CET1 ratio; RWA density; credit growth vs CAR |
| T3 | Corp bond maturity wall | Reported NPL là floor; shadow NPL = nhóm 2 + tái cơ cấu + bond distress | Adjusted NPL; maturity wall 12M; secondary price <70 par |
| T4 | PDP8 | Giá điện pre-2024 không reflect LNG passthrough | LNG import price (JKM); PPA signed; EVN tariff |
| T5 | Samsung + Vietnam+1 | Export growth 2015–2023 driven by Samsung; extrapolate = overestimate GDP/FX | Samsung VN revenue/total exports; FDI Korea; HS 8517 XK YoY |

---

## VI. PROTOCOL CẬP NHẬT & SỬ DỤNG

### Quy trình cập nhật

| Tần suất | Hành động |
|---|---|
| **Hàng tuần** | Kiểm tra shift tracker — status đổi không? Cập nhật indicator values |
| **Hàng tháng** | Review indicator — shift nào đạt threshold TRIGGERED? |
| **Hàng quý** | Thêm shift mới. Chuyển shift hoàn thành sang archive |
| **Ad-hoc** | Văn bản pháp luật mới, Nghị định, Thông tư, sự kiện địa chính trị lớn |

### Cách dùng trong Workflow

| Workflow | Cách dùng |
|---|---|
| **Daily Brief** | Check shift đổi status gần đây → flag trong risk section |
| **Deep-dive Equity** | Structural break ảnh hưởng multiple/earnings? (Basel III→bank, PDP8→utilities, Luật Đất đai→BĐS) |
| **Cross-asset Linkage** | Shift nào affect correlation regime? |
| **Pre-mortem** | Thesis có implicit assumption "shift X không xảy ra" không? |
| **Regime Shift Alert** | ≥3 indicator đổi status cùng lúc → trigger structural re-evaluation |

### Checklist trước Time Series

- [ ] Có structural break trong analysis period không? (Kiểm tra tracker)
- [ ] Nếu có → đã adjust data hoặc segment analysis chưa?
- [ ] Broker estimate có sensitivity table không?
- [ ] Có data gap không? → flag rõ.

---

> **Document Control**
> - Version: v1.0 (Wave 6 — Lane 4)
> - Ngày: 2026-04-19
> - Next review: 2026-07-19
> - Entries: 30 (26 category + 4 top-impact)
> - Related: workflow-daily-brief.md, workflow-pre-mortem.md, workflow-regime-shift-alert.md
