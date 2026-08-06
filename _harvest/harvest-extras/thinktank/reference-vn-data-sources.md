---
title: "Reference VN Data Sources — Vietnam Macro, Equity, FX, Rates, Official and Commercial Data"
module_type: "reference"
file_name: "reference-vn-data-sources.md"
purpose: "List preferred data sources, source hierarchy, and cross-check rules for Vietnam-biased multi-asset research. Use to resolve source conflicts and assign trust tiers."
primary_triggers:
  - "nguồn dữ liệu"
  - "data source"
  - "FiinTrade"
  - "NHNN"
  - "broker research"
  - "dữ liệu Việt Nam"
  - "macro data Vietnam"
  - "Tổng cục Thống kê"
  - "HOSE"
  - "Customs"
when_to_use:
  - "When the user asks where data should come from or which source to trust."
  - "When a research output needs source hierarchy, data-quality caveats, or conflict resolution."
  - "When building a daily brief or deep-dive and need to cite primary vs secondary sources."
when_not_to_use:
  - "Do not use as a substitute for live data retrieval; it defines source preference, not current values."
  - "Do not use to generate structural-shift analysis — that belongs in shift-tracker files."
related_modules:
  - "workflow-daily-brief.md"
  - "workflow-deep-dive.md"
  - "core-evidence-ladder.md"
  - "domain-macro-vn-liquidity.md"
  - "domain-fx-usd-vnd.md"
  - "domain-equity-vn-valuation.md"
  - "reference-visual-artifact-policy.md"
authoritative_citations:
  - "State Bank of Vietnam."
  - "General Statistics Office of Vietnam."
  - "Ministry of Finance of Vietnam."
  - "HOSE and HNX official disclosures."
  - "Vietnam Customs."
  - "World Bank and IMF data portals."
  - "FiinGroup / FiinTrade."
output_owner: "Reference support only; does not own analysis."
---

# Reference VN Data Sources — Nguồn Dữ liệu Việt Nam

Purpose: Establish source hierarchy for OPVIA Sigma research. Official Vietnamese sources first where reliable, exchange data for market structure, commercial providers for equity deep-dives, broker research for primary intelligence, and global anchors for cross-asset context.

Trigger keywords: nguồn dữ liệu, data source, FiinTrade, NHNN, GSO, Tổng cục Thống kê, HOSE, HNX, Customs, IMF, World Bank, FRED, broker research, Vietcap, ACBS, macro data Vietnam.

---

## A. Nguồn Chính thức — Chính phủ & Regulator

> Tier S = primary source không tranh cãi. Tier A = đáng tin nhưng có limitation known.

| Nguồn | URL pattern | Dữ liệu core | Tần suất | Độ trễ | Định dạng | Trust |
|---|---|---|---|---|---|---|
| **NHNN (SBV)** | `sbv.gov.vn` | Policy rates, OMO (volume, rate, tenor), M2, tăng trưởng tín dụng, dự trữ ngoại hối, can thiệp FX (thông cáo định tính) | Policy: ad-hoc. OMO: daily 8h30. Thống kê: monthly (ngày 20–25) | OMO: T+0. Thống kê: T+20–25. FX reserves: quarterly, T+45–60 | PDF, Excel, web table | **Tier S** — số liệu chính thức. FX intervention không minh bạch → infer từ spot + forward premium |
| **GSO** | `gso.gov.vn` | CPI (11 nhóm), PPI (3 ngành), GDP (ngành/chi tiêu/địa phương), IIP, bán lẻ, FDI (đăng ký + giải ngân), XNK, lao động | CPI: monthly (ngày 29). GDP: quarterly (T+45). IIP/FDI/bán lẻ: monthly | T+20–30 (monthly); T+45 (GDP quarterly) | PDF, Excel, web table | **Tier S** — primary source. CPI basket weights không công bố chi tiết; GDP revision history ít transparent |
| **MOF** | `mof.gov.vn` | Thực hiện ngân sách (thu, chi, bội chi), nợ công (nội địa + ngoại tệ), lịch phát hành TPCP, thuế (VAT, TNDN, TNCN) | Ngân sách: monthly (T+25). Nợ công: quarterly/annual | T+25–45. Nợ công chi tiết: T+90 | PDF, Excel | **Tier S** (ngân sách); **Tier A** (nợ công — nợ ẩn SOE và local government guarantees không công bố đầy đủ) |
| **MoIT** | `moit.gov.vn` | Sản lượng công nghiệp chủ yếu, điện sản xuất/tiêu thụ, XNK theo mặt hàng | Monthly | T+20–30 | PDF, web | **Tier A** — hữu ích sector-specific, less rigorous than GSO |
| **Customs** | `customs.gov.vn` | Trade balance chi tiết theo HS code, đối tác quốc gia, cửa khẩu. FOB/CIF breakdown | Monthly (T+15–20, nhanh hơn GSO) | T+15–20 | Excel, PDF | **Tier S** (trade volume); **Tier B** (partner breakdown — mirror stats với TQ thường mismatch 15–20%) |

**Lưu ý OPVIA:** NHNN FX intervention không công bố real-time size — proxy bằng spot USD/VND biến động bất thường, forward premium đột biến, delta reserves QoQ. So sánh với ước tính broker (Vietcap, ACBS). GSO CPI food component (~40% basket) — cross-check bằng giá trực tiếp từ chợ đầu mối. PPI thường lag CPI 1–2 tháng. FDI "đăng ký" khác xa "giải ngân" — chỉ dùng giải ngân cho analysis. MOF nợ công ~36–38% GDP theo công bố, nhưng nợ ẩn (bảo lãnh SOE, nợ địa phương, trái phiếu BĐS có bảo lãnh ngầm) lớn hơn — dùng VEPR/World Bank estimates để cross-check. Customs là leading indicator cho GDP quarterly; mirror stats với Trung Quốc thường chênh 15–20%.

---

## B. Sở Giao dịch / Cơ sở hạ tầng Thị trường

| Nguồn | URL pattern | Dữ liệu core | Tần suất | Định dạng | Trust | Chi phí |
|---|---|---|---|---|---|---|
| **HOSE** | `hsx.vn` | Giá, KLGD, market cap, VN-Index, VN30, foreign buy/sell daily | T+0 (EOD) | Web, Excel | **Tier S** | Free |
| **HNX** | `hnx.vn` | Giá, KLGD, HNX-Index, UPCOM, trái phiếu chính phủ giao dịch | T+0 | Web, Excel | **Tier S** | Free |
| **UPCOM** | Qua HNX | Giá, KLGD, foreign flow, động thái chuyển sàn lên HOSE/HNX | T+0 | Web | **Tier S** | Free |
| **VSDC** | `vsd.vn` | Số lượng tài khoản NHĐT (mở mới, tổng), NI lưu ký, FOL theo mã | Monthly | PDF, Excel | **Tier S** | Free |
| **VBMA** | `vbma.org.vn` | Bond market: issuance, secondary volume, yield curve ước tính, reference price | Daily/Weekly | Excel, web | **Tier A** | Free (members) |

**Caveat thị trường chứng khoán VN:** Foreign ownership ratio trên HOSE/HNX tính theo room (FOL), không phải free-float. Một số mã FOL full nhưng vẫn có giao dịch ngoại qua Covered Warrant, ETF, hoặc nắm giữ gián tiếp. FII trade data EOD nhưng không phân rã theo broker hay quốc gia. Bond market không có benchmark 10Y liên tục như UST — VBMA làm anchor nhưng cần cross-check với bid/ask từ broker.

---

## C. Nhà cung cấp Dữ liệu Thương mại

| Nguồn | Phạm vi | Chi phí (ước tính) | API | Đánh giá OPVIA |
|---|---|---|---|---|
| **FiinTrade** | Dữ liệu CK VN toàn diện: giá EOD + intraday (Pro), BCTC (quý, năm, 10Y+), ratios, ownership, corporate actions, dividends, EPS consensus | ~15–30 triệu VND/năm | Có (REST API, Enterprise) | **Tier 1 — core source.** SSOT cho equity data nếu OPVIA đã đăng ký. BCTC chuẩn hóa tốt nhưng VAS → cần điều chỉnh thủ công khi so sánh quốc tế |
| **FiinPro** | Screening, so sánh đa công ty, phân tích ngành, corporate governance, ESG score VN | ~40–80 triệu VND/năm | Có | **Tier 1** — nếu OPVIA có access. Dữ liệu ngành và governance hữu ích cho moat analysis. ESG score VN còn non-trẻ, dùng thận trọng |
| **Vietstock** | Tin tức thờii sự + dữ liệu cơ bản miễn phí (giá, BCTC 5 năm, ratios). Báo cáo phân tích miễn phí từ broker | Free / Premium (~3–5 triệu/năm) | Không | **Tier B** — tin tức nhanh, data cơ bản đủ dùng. BCTC không chi tiết bằng Fiin |
| **CafeF** | Tin tức tài chính nhanh nhất VN, dữ liệu giá cơ bản, foreign flow | Free | Không | **Tier B — news source.** Tốc độ cập nhật nhanh nhất. Quality control kém, tin sai/chưa verify thường xuyên. Không dùng làm primary source cho số liệu |
| **FireAnt** | Dữ liệu chứng khoán, BCTC, so sánh, báo cáo ngành | Free / Premium | Có (gói trả phí) | **Tier B+** — Giao diện tốt, data đầy đủ ở mức intermediate. Dùng nếu FiinTrade không available |
| **StockBiz** | Charting, screening, dữ liệu lịch sử giá, BCTC | Free / Premium nhẹ | Không | **Tier C** — dùng cho chart nhanh hoặc screen cơ bản. Không đủ deep cho institutional analysis |

---

## D. Nghiên cứu Broker — Primary Intelligence

> Broker research ở VN là nguồn intelligence quan trọng vì: access management không công khai, ước tính dữ liệu NHNN, sector coverage sâu. Conflict of interest (IB, market making) là thực tế — cần discount.

### Tiering & Đánh giá

| Broker | Tier | Sector mạnh nhất | Tần suất | Trust | Điểm mạnh | Điểm yếu / Bias |
|---|---|---|---|---|---|---|
| **Vietcap (VCSC)** | **S** | Macro, Ngân hàng, BĐS KCN, Tiêu dùng | Weekly (macro), ad-hoc | ★★★★☆ | Macro call nhanh, data NHNN ước tính chất lượng cao | IB relationship → hold/sell hiếm gặp |
| **ACBS** | **S** | Ngân hàng, Chứng khoán, BĐS | Weekly (wrap), monthly (strategy) | ★★★★☆ | Balanced. Macro view conservative, phù hợp để "anchor" kỳ vọng | Coverage mid-cap hẹp hơn Vietcap |
| **SSI Research** | **S** | Ngân hàng, BĐS KCN, Logistics | Weekly (SSI Update), monthly | ★★★★☆ | Broker lớn nhất VN, coverage rộng nhất, flow data nội bộ tốt | Đôi khi generic do coverage quá rộng |
| **MBS** | **A** | Ngân hàng, Bán lẻ, Logistics | Weekly, daily commentary | ★★★★☆ | Research quality ổn định, derivatives commentary hữu ích | Macro call trung bình, ít scenario analysis |
| **VDSC** | **A** | Ngân hàng, BĐS, Dầu khí | Weekly | ★★★★☆ | Coverage rộng, định giá chặt | Macro call chậm 1–2 tuần so với Vietcap |
| **Mirae Asset** | **A** | Ngân hàng, Tiêu dùng, Công nghệ | Daily/Weekly | ★★★★☆ | FII perspective mạnh, flow analysis tốt | Bias bullish về FII inflow, ít bear-case detail |
| **HSC** | **A** | Ngân hàng, Bán lẻ, Tiêu dùng | Weekly | ★★★★☆ | Longest track record, methodology chuẩn, company-level chặt | Macro call trung bình |
| **BSC (BIDV Securities)** | **B** | Ngân hàng, SOE, Vĩ mô | Weekly | ★★★☆☆ | Data SOE và ngân hàng quốc doanh tốt | State-linked → macro view đôi khi "chính thức" quá mức |
| **BVSC** | **B** | Ngân hàng, Tiện ích, BĐS | Weekly | ★★★★☆ | Balanced, ít hype, quality control tốt | Coverage hẹp, ít ad-hoc deep-dive |

**Tier 2 — Specialist:** RongViet (BĐS dân dụng), KBSV (mid-cap, UPCOM), PSI (Maritime, Logistics, Hàng không), VNDirect (retail-focused — không dùng cho institutional thesis).

### Quy tắc Cross-check Broker Research

| Cặp so sánh | Câu hỏi cross-check |
|---|---|
| **Vietcap vs ACBS** | Vietcap macro thường bullish hơn ACBS. Nếu cả hai đồng thuận về rate cut/tightening → signal mạnh. Nếu split → xem lại assumptions về NHNN reaction function |
| **MBS vs HSC** | Cả hai đều conservative về ngân hàng. Nếu cả hai đồng thuận NPL sẽ tăng → trust cao. Nếu một bảo "NPL đã peak" → flag đỏ |
| **BSC vs Broker tư nhân** | BSC đôi khi phản ánh "view chính thức." So sánh với Vietcap/Mirae để tìm divergence giữa state view và market view |
| **Consensus EPS vs giá** | Nếu consensus EPS tăng 20%+ trong 3 tháng nhưng giá đi ngang → market không tin consensus |
| **Target price spread** | Spread TP cao nhất/thấp nhất > 40% → uncertainty cao, không dùng TP làm anchor |

**Quy tắc vàng:** Không bao giờ dùng 1 broker report làm primary basis cho thesis. "Buy" rating ở VN chiếm > 70% → normalize bằng cách đọc "conviction level" thay vì label. Ưu tiên báo cáo có sensitivity table và scenario analysis.

---

## E. Neo Toàn cầu (Global Anchors)

### E1. Nếu OPVIA có quyền truy cập

| Nguồn | Dữ liệu core | Chi phí | Trust |
|---|---|---|---|
| **Bloomberg Terminal** | VN equity, FX (USD/VND spot + NDF), rates (UST, VN government bond), commodities futures, broker report aggregator | ~24,000 USD/năm | **Tier S** |
| **Refinitiv / LSEG** | Tương tự Bloomberg, Eikon cheaper | ~18,000–22,000 USD/năm | **Tier S** |

### E2. Nguồn Miễn phí

| Nguồn | URL | Dữ liệu core | Tần suất | Trust |
|---|---|---|---|---|
| **FRED** | `fred.stlouisfed.org` | UST yields, DXY, Fed funds, real yield (TIPS), unemployment, inflation breakeven | Daily/Weekly | **Tier S** |
| **TradingEconomics** | `tradingeconomics.com/vietnam` | Tổng hợp macro VN: GDP, CPI, PPI, trade, interest rate, unemployment. Cross-country | Monthly | **Tier B** (aggregate, không primary) |
| **Investing.com** | `investing.com` | Futures oil, gold, copper, DXY, major FX, VN-Index futures | Real-time (delayed 15ph) | **Tier B** (price data ok, analysis generic) |
| **BIS** | `bis.org` | Global liquidity, FX turnover survey, credit-to-GDP gaps, property price index (có VN!) | Quarterly/Annual | **Tier S** (global); **Tier A** (VN property, có lag) |
| **IMF DataPortal** | `data.imf.org` | BoP, GDP, inflation, fiscal, debt — cross-country. Article IV VN (annual) | Annual/Quarterly | **Tier S** |
| **World Bank** | `data.worldbank.org` | GDP, poverty, infrastructure, remittance estimates | Annual | **Tier S** |
| **UST Department** | `home.treasury.gov` | UST issuance, yield data, TIC capital flows | Daily | **Tier S** |

### E3. Dataset Cụ thể cần Monitor

| Dataset | Nguồn chính | Tần suất | Mục đích cho VN |
|---|---|---|---|
| **UST 10Y yield** | FRED | Daily | Anchor VN TPCP 10Y spread, global risk-free rate, EM equity multiple |
| **UST 10Y real yield (TIPS)** | FRED | Daily | Driver gold price, EM equity risk premium |
| **DXY** | FRED / Investing.com | Daily | VND neo vào USD basket → DXY strength = pressure on VND spot |
| **CNY/USD** | Investing.com / Bloomberg | Daily | ~30% trade linkage, FDI source, competitive devaluation risk |
| **WTI / Brent futures** | Investing.com / FRED | Real-time | Passthrough CPI VN (xăng dầu ~5–7% basket), logistics cost |
| **Gold spot (XAU/USD)** | Investing.com | Real-time | Safe haven VN, wealth store (~40 tấn/năm retail demand) |

---

## F. Học thuật / Think-tank

| Tổ chức | URL | Đóng góp cho VN analysis | Trust |
|---|---|---|---|
| **VEPR** | `vepr.org.vn` | Quarterly macro report chất lượng cao. GDP forecast độc lập. Policy recommendations thực tế. | **Tier A+** — nguồn học thuật VN trust nhất |
| **NCIF** | `ncif.org.vn` | Nghiên cứu tài chính công, nợ công, thị trường vốn. Đánh giá độc lập về fiscal space | **Tier A** |
| **CIEM** | `ciem.org.vn` | Policy-oriented, view Chính phủ nhưng analysis kỹ thuật tốt về CPTPP/EVFTA/RCEP | **Tier A** |
| **BIS** | `bis.org` | Global financial cycle, credit gap, property price. Claudio Borio papers = framework #1 cho financial cycle analysis | **Tier S** (global context) |
| **IMF** | `imf.org` | Article IV VN (annual), WEO (Apr/Oct). BoP, fiscal, debt chuẩn quốc tế | **Tier S** (cross-country comparison) |
| **World Bank** | `worldbank.org` | Vietnam Macro Poverty Outlook, remittance estimates, infrastructure reports | **Tier S** |
| **ADB** | `adb.org` | Asian Development Outlook, bond market reports cho VN. Conservative forecasts, useful for stress testing | **Tier A** |
| **IIF** | `iif.com` | Capital flow tracker cho EM, including VN. Flow data theo tuần/tháng | **Tier A** (membership required) |

---

## G. Phương pháp Cross-check khi Nguồn Xung đột

> Luật: Không bao giờ tin một nguồn duy nhất.

### Hierarchy Trust

```
Tier S (Primary):    NHNN, GSO, MOF, HOSE/HNX, VSDC, FRED, IMF, BIS, World Bank
    ↓ cross-check với
Tier A (Institutional broker): Vietcap, ACBS, SSI, MBS, VDSC, Mirae, HSC, BVSC
    ↓ cross-check với
Tier B (Commercial aggregate): FiinTrade, TradingEconomics, Investing.com, BSC
    ↓ cross-check với
Tier C (News/Tertiary): CafeF, Vietstock free tier, StockBiz
```

### Xử lý xung đột phổ biến

| Tình huống | Nguồn A | Nguồn B | Quyết định |
|---|---|---|---|
| GDP growth: GSO vs IMF | GSO | IMF | **Tin GSO cho historical; tin IMF cho forecast** (IMF less politically smoothed) |
| FX reserves: NHNN vs IMF IFS | NHNN | IMF | **Tin IMF IFS** — NHNN công bố gross reserves, IMF ước tính net sau swap và forward liabilities |
| Corporate EPS: FiinTrade vs Broker | FiinTrade | Broker | **Tin broker nếu report có model detail và sensitivity.** FiinTrade là mechanical aggregation, có thể miss one-off items |
| NPL ratio: NHNN vs Vietcap | NHNN (reported) | Vietcap (adjusted) | **Tin Vietcap adjusted** nếu họ công bố methodology. NHNN NPL là floor, không phải ceiling |
| UST 10Y: FRED vs Investing.com | FRED | Investing.com | **Tin FRED.** Investing.com có thể delay hoặc sai ticker |
| Trade balance: Customs vs GSO | Customs | GSO | **Tin Customs cho monthly (nhanh hơn).** GSO là revised quarterly, dùng cho annual reconciliation |

### Red flags cho nguồn không đáng tin

- Không công bố methodology.
- Revisions không có changelog.
- Data point outlier mà không có explanation trong press release.
- Broker report không có sensitivity table hoặc chỉ có single-point target price.
- CafeF/Vietstock đăng tin mà không ghi rõ nguồn.

---

## Tích hợp với Workflow Daily Brief

| Block | Nội dung | Nguồn chính | Nguồn phụ |
|---|---|---|---|
| **DB-1: Overnight & Regime** | UST, DXY, oil, gold, VN-Index close, OMO hôm qua | FRED (UST, DXY), Investing.com (oil, gold), HOSE/HNX (VN close), NHNN web (OMO) | TradingEconomics (cross-country), FiinTrade (consensus check) |
| **DB-2: Today's Watchlist** | Data release hôm nay, earnings, broker report mới, signpost cần check | GSO calendar (CPI, IIP), MOF calendar (ngân sách), FiinTrade (earnings calendar), Vietstock (broker report mới), VEPR/IMF (report release) | CafeF (speed check nếu có news break) |

**Quy tắc nhanh cho DB:** DB-1 ưu tiên real-time hoặc T+0 sources (FRED, HOSE, NHNN OMO). DB-2 ưu tiên calendar và scheduled releases (GSO, MOF, earnings calendar). Không bao giờ dùng CafeF làm nguồn duy nhất cho một claim trong DB. Nếu số liệu quan trọng chưa có từ Tier S → flag "data gap" và dùng Tier A estimate kèm disclaimer.

---

## Cross-references

- Phân tích sâu: `workflow-deep-dive.md`
- Brief hàng ngày: `workflow-daily-brief.md`
- Thang bậc bằng chứng: `core-evidence-ladder.md`
- Trực quan hoá: `reference-visual-artifact-policy.md`
- VAS → IFRS: `domain-equity-vn-vas-ifrs-bridges.md`
- Chu kỳ tín dụng: `framework-thakor-yu-2024.md`

---

> **Document Control**
> - Version: v1.0 (Wave 4 — Lane 11)
> - Ngày: 2026-04-19
> - Author: OPVIA Sigma Build Team
> - Approver: OPVIA
> - Related modules: workflow-daily-brief.md, workflow-deep-dive.md, core-evidence-ladder.md, domain-macro-vn-liquidity.md, domain-fx-usd-vnd.md
> - Source port: Wave 2 Lane E2 Part I (A–G)
