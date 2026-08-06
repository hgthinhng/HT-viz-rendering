---
title: "Domain Equity VN Financial Modeling — 3-Statement Model, Forecast Drivers, Working Capital, CapEx, Debt Schedule, Integrity Checks"
module_type: "domain"
file_name: "domain-equity-vn-financial-modeling.md"
purpose: "Build and audit Vietnamese listed-equity financial models using linked P&L, balance sheet, cash flow, forecast drivers, and must-pass integrity checks."
primary_triggers:
  - "mô hình tài chính"
  - "financial model"
  - "3-statement"
  - "P&L forecast"
  - "balance sheet forecast"
  - "dự phóng tài chính"
  - "dự phóng dòng tiền"
  - "CapEx schedule"
  - "debt schedule"
when_to_use:
  - "When the user asks to build, audit, or explain a 3-statement model for a Vietnamese listed company."
  - "When a valuation, reverse DCF, SOTP, or scenario analysis needs explicit forecast drivers and cash-flow outputs."
  - "When checking whether P&L growth, balance-sheet funding, and cash flow are internally consistent."
when_not_to_use:
  - "Do not use for pure accounting-forensic screening without a forecast; use domain-equity-vn-forensic-accounting.md."
  - "Do not use for standalone valuation conclusions; pair with domain-equity-vn-valuation-advanced.md."
  - "Do not issue buy/sell/hold, target price, or trade-timing output."
related_modules:
  - "workflow-deep-dive.md"
  - "domain-equity-vn-valuation-advanced.md"
  - "domain-equity-vn-forensic-accounting.md"
  - "domain-equity-vn-industry-guides.md"
  - "core-evidence-ladder.md"
authoritative_citations:
  - "Penman, S. Financial Statement Analysis and Security Valuation."
  - "Damodaran, A. Investment Valuation."
  - "Mauboussin, M. Expectations Investing."
  - "VAS — Vietnamese Accounting Standards, Ministry of Finance."
output_owner: "Financial-modeling lens only; workflow-deep-dive.md owns the final deep-dive output contract and forecast table placement."
---

# Domain Equity VN Financial Modeling — Mô hình tài chính 3 báo cáo

Purpose: Chuẩn hóa cách xây và kiểm tra **mô hình tài chính** cho cổ phiếu Việt Nam: P&L forecast, balance sheet forecast, cash flow forecast, working capital, CapEx, debt schedule, equity forecast, và integrity checks. Module này tạo đầu vào cho valuation, reverse DCF, scenario bounds và forensic stress test; không đưa khuyến nghị mua/bán/nắm giữ.

Trigger keywords: mô hình tài chính, financial model, 3-statement, P&L forecast, balance sheet forecast, cash flow forecast, DSO, DIO, DPO, NWC, CapEx schedule, debt schedule, covenant headroom, EBITDA, D&A, WACC.

Use with: `workflow-deep-dive.md`, `domain-equity-vn-valuation-advanced.md`, `domain-equity-vn-forensic-accounting.md`, `domain-equity-vn-industry-guides.md`.

---

## 1. 3-Statement Modeling Integrity — luật liên kết P&L → BS → CF

Mô hình 3 báo cáo chỉ đáng tin khi P&L, balance sheet và cash flow statement nói cùng một câu chuyện kinh tế. Nếu một báo cáo tăng trưởng đẹp nhưng hai báo cáo còn lại không tài trợ được tăng trưởng đó, mô hình đang có lỗi.

Luật liên kết tối thiểu:

| Dòng | Luật liên kết | Lỗi thường gặp |
|---|---|---|
| Revenue → Receivables | Phải thu = Revenue × DSO / 365 | Revenue tăng nhưng DSO không đổi vô căn cứ khi khách hàng yếu đi |
| COGS → Inventory | Tồn kho = COGS × DIO / 365 | Sản xuất chu kỳ nhưng tồn kho không phản ứng với giá nguyên liệu |
| COGS → Payables | Phải trả NCC = COGS × DPO / 365 | DPO tăng để làm đẹp CFO nhưng không có sức mặc cả với NCC |
| CapEx → PP&E | PP&E cuối kỳ = PP&E đầu kỳ + CapEx − D&A ± thanh lý | Khấu hao lấy % doanh thu thay vì từ tài sản |
| Debt → Interest | Interest expense = average debt × interest rate | Lãi vay giảm dù nợ tăng |
| Net income → Equity | Equity cuối kỳ = equity đầu kỳ + LNST − dividends ± share issuance/buyback ± OCI | Quên cổ tức hoặc lợi ích cổ đông thiểu số |
| Cash flow → Cash | Cash cuối kỳ = cash đầu kỳ + CFO + CFI + CFF | BS cân nhờ plug ở cash hoặc debt mà không giải thích |

Điểm dễ tạo circular reference là interest expense và cash. Cách thực dụng: dùng nợ bình quân đầu/cuối kỳ nếu mô hình cho phép iteration; nếu không, dùng nợ đầu kỳ cho interest và ghi chú sai số. Không dùng "cash plug" để ép balance sheet cân; plug hợp lệ phải là chính sách tài trợ rõ: vay quay vòng, phát hành vốn, hoặc cash sweep.

## 2. Revenue Forecast Drivers — driver doanh thu theo ngành

Revenue forecast phải đi từ cơ chế ngành, không dùng CAGR lịch sử máy móc. Tách ít nhất 3 lớp: market demand, company volume/share, pricing/mix.

| Ngành | Driver chính | Công thức gợi ý | Điểm kiểm tra |
|---|---|---|---|
| Ngân hàng | Loan growth, NIM, fee income | NII = average earning assets × NIM; LNST phụ thuộc credit cost | Không dùng 3-statement công nghiệp; cần model bảng cân đối ngân hàng |
| Bán lẻ | Số cửa hàng, SSS, doanh thu/cửa hàng mới | Revenue = store count × sales/store; tách SSS và new stores | Cửa hàng mới thường ramp-up 6-24 tháng; lease obligation có thể off-BS dưới VAS |
| Thép | Volume × ASP; tách HRC/rebar/export | Revenue = sản lượng × ASP theo sản phẩm | Giá thép, quặng sắt, than cốc, utilization và tồn kho tạo đòn bẩy lớn |
| BĐS | Backlog, presales, bàn giao | Revenue = diện tích bàn giao × ASP × tỷ lệ sở hữu | Cash thu trước có thể đi trước revenue; inventory không dùng DIO thường |
| Cảng/logistics | Throughput, tariff, utilization | Revenue = TEU/tons × fee + dịch vụ phụ trợ | Capacity bottleneck và concession duration quan trọng hơn CAGR |
| Hàng tiêu dùng | Volume, ASP, channel mix | Revenue = volume × net ASP | Trade promotion có thể làm gross-to-net revenue nhiễu |
| Chứng khoán | ADTV, market share, margin loan book | Revenue = brokerage + margin interest + IB + prop trading | Prop trading làm earnings biến động, không nên tuyến tính hóa |

Với ngành chu kỳ, base case nên dùng mid-cycle volume, ASP và margin. Với operating leverage cao, phải tách volume và price: tăng do volume kéo theo working capital và CapEx; tăng do price làm margin và NWC biến động nhanh hơn.

## 3. Cost Forecast — variable, fixed, SG&A và D&A

Chi phí cần phân loại theo hành vi kinh tế:

| Nhóm chi phí | Cách forecast | Ví dụ |
|---|---|---|
| Variable cost | Theo volume hoặc % revenue/COGS unit cost | Nguyên liệu thép, hàng mua bán lẻ, bao bì |
| Fixed cost | Theo inflation, công suất, hợp đồng | Lương quản lý nhà máy, khấu hao, thuê kho |
| Semi-variable | Base cost + biến phí theo volume | Điện, logistics, bảo trì |
| SG&A | % revenue, per-store, headcount hoặc inflation | Bán hàng, marketing, quản lý, lương văn phòng |
| D&A | Từ PP&E schedule, không từ % revenue | Khấu hao tài sản hiện hữu + CapEx mới |

COGS không nên forecast một dòng duy nhất nếu biên gộp là driver valuation. Với thép, tách giá quặng/than/phế liệu, yield và inventory lag. Với bán lẻ, tách gross margin theo mix hàng hóa và shrinkage. Với ngân hàng, dùng CIR cho chi phí hoạt động; credit cost là biến riêng.

D&A phải chảy từ CapEx schedule. Quy ước đơn giản: tài sản cũ khấu hao theo run-rate hiện tại; CapEx mới dùng half-year convention trong năm đưa vào sử dụng, sau đó full-year theo đời hữu ích. Nếu có xây dựng cơ bản dở dang lớn, cần timeline chuyển từ CIP sang PP&E.

## 4. Working Capital Forecast — DSO, DIO, DPO và chuẩn ngành VN

NWC forecast là nơi nhiều mô hình đẹp trên P&L nhưng vỡ trên cash flow. Dùng công thức nhất quán:

```text
DSO = Phải thu khách hàng bình quân / Doanh thu × 365
DIO = Hàng tồn kho bình quân / COGS × 365
DPO = Phải trả người bán bình quân / COGS × 365
CCC = DSO + DIO − DPO
```

Chuẩn VN nên là range theo ngành, lấy từ lịch sử công ty, peer và thuyết minh:

| Ngành | DSO | DIO | DPO | Ghi chú |
|---|---:|---:|---:|---|
| Bán lẻ hiện đại | 5-25 ngày | 45-90 ngày | 45-120 ngày | Thu tiền nhanh, chiếm dụng NCC; DPO cao chỉ bền nếu scale mạnh |
| Thép/sản xuất chu kỳ | 30-75 ngày | 60-120 ngày | 30-90 ngày | Giá nguyên liệu làm giá trị tồn kho biến động mạnh |
| Hàng tiêu dùng | 20-60 ngày | 45-100 ngày | 30-80 ngày | Distributor financing và trade terms cần đọc thuyết minh |
| Xây dựng | 60-180 ngày | Không chuẩn | 60-150 ngày | Phải thu nghiệm thu và giữ lại bảo hành làm DSO cao |
| BĐS | Không dùng chuẩn | Inventory dự án nhiều năm | Phải trả nhà thầu | Người mua trả trước là driver riêng |
| Cảng/logistics | 25-60 ngày | Thấp | 20-60 ngày | Tồn kho không trọng yếu |

Không giả định DSO giảm chỉ để tăng CFO. Nếu DSO/DIO/DPO đổi hướng so với lịch sử, cần nguyên nhân: khách hàng, chính sách tín dụng, bargaining power, chuyển kênh, hay điều kiện ngành. Trong bear case, thường phải cho DSO tăng, DIO tăng và DPO bị giới hạn.

## 5. CapEx Schedule — growth vs maintenance và D&A convention

CapEx phải tách **maintenance CapEx** và **growth CapEx**. Maintenance CapEx giữ công suất hiện hữu, thường neo vào D&A, tuổi tài sản, hoặc sản lượng duy trì. Growth CapEx phải có dự án, tổng vốn, tiến độ giải ngân, thời điểm vận hành và revenue ramp-up.

Output schedule tối thiểu:

| Năm | Opening PP&E | Maintenance CapEx | Growth CapEx | Disposal | D&A | Closing PP&E | CIP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Y+1 | x | x | x | x | x | x | x |

Luật kiểm tra: growth CapEx không được tạo full revenue ngay nếu dự án chưa vận hành. Nhà máy thép, điện, cảng, bán lẻ mở chuỗi đều có J-curve: tiền ra trước, utilization tăng dần. Với BĐS, CapEx nằm trong inventory dự án thay vì PP&E; với ngân hàng, CapEx vật chất thường không phải driver chính.

## 6. Debt Schedule — cash sweep, amortization, covenant headroom

Debt schedule nối financing need với P&L và balance sheet. Cấu trúc chuẩn:

| Dòng | Nội dung |
|---|---|
| Opening debt | Nợ ngắn hạn + dài hạn đầu kỳ |
| Mandatory amortization | Trả nợ theo lịch hợp đồng |
| New borrowings | Vay mới để tài trợ CapEx/NWC/refinance |
| Optional repayment / cash sweep | Dùng cash dư sau minimum cash để trả nợ |
| Closing debt | Opening + new borrowings − repayments |
| Average debt | Dùng tính interest expense |
| Interest rate | Tách fixed/floating nếu có dữ liệu |
| Interest expense | Average debt × rate, sau điều chỉnh vốn hóa nếu phù hợp |

Covenant headroom cần được tính trong base và bear case: Net debt/EBITDA, Interest Coverage, D/E, Current Ratio, minimum cash, và nghĩa vụ nợ đến hạn 12 tháng. Với doanh nghiệp VN vay ngắn hạn quay vòng lớn, rủi ro không chỉ là leverage mà là rollover. Cash sweep chỉ hợp lý nếu công ty không có minimum cash operating need, không bị restriction ở công ty con, và không phải giữ vốn cho working capital mùa vụ.

## 7. Equity Forecast — dividends, issuance, treasury

Equity forecast liên kết LNST với vốn chủ sở hữu và số cổ phiếu:

```text
Retained earnings cuối kỳ = Retained earnings đầu kỳ + LNST thuộc cổ đông mẹ − cổ tức
Total equity cuối kỳ = equity đầu kỳ + LNST − dividends + issuance − buyback ± OCI/reserves ± minority interest movement
EPS = LNST thuộc cổ đông mẹ / weighted average shares
```

Cổ tức tiền mặt phải đi qua CFF và giảm cash. Cổ tức cổ phiếu làm tăng số cổ phiếu nhưng không tạo tiền. ESOP, convertible bond, warrant và private placement cần tính fully diluted shares nếu ảnh hưởng valuation. Với tập đoàn có minority interest lớn, không dùng consolidated net income cho EPS; dùng LNST thuộc cổ đông công ty mẹ.

## 8. Cash Flow Build — indirect method theo chuẩn VN

Cash flow forecast theo indirect method:

```text
CFO = LNST + D&A + non-cash expenses − non-cash gains
      − ΔReceivables − ΔInventory + ΔPayables ± ΔOther working capital

CFI = −CapEx ± proceeds from disposals − financial investments + divestment proceeds

CFF = new debt − debt repayment − cash dividends + share issuance − buyback

Ending cash = beginning cash + CFO + CFI + CFF
```

FCF cho valuation cần nhất quán với cấu trúc vốn. FCFF = `EBIT × (1 − tax) + D&A − CapEx − ΔNWC`; FCFE = `CFO − CapEx + net borrowing`. Khi leverage thay đổi lớn, FCFF thường sạch hơn cho DCF vì tách operating value khỏi financing.

## 9. Integrity Checks — 10 kiểm tra bắt buộc

| # | Check | Must-pass logic |
|---:|---|---|
| 1 | Balance sheet balances | Total assets = liabilities + equity từng năm; sai lệch phải bằng 0 hoặc rounding immaterial |
| 2 | Cash tie-out | Ending cash trên BS = beginning cash + CFO + CFI + CFF |
| 3 | PP&E roll-forward | Closing PP&E = opening PP&E + CapEx − D&A ± disposal/reclass |
| 4 | Equity roll-forward | Closing equity khớp LNST, dividends, issuance, buyback, OCI/reserves, minority interest |
| 5 | Debt roll-forward | Closing debt khớp opening debt + borrowings − repayments; interest tính từ average debt |
| 6 | NWC bridge | ΔReceivables, ΔInventory, ΔPayables trên CFS khớp BS |
| 7 | Tax rate reasonableness | Effective tax rate gần statutory rate hoặc có lý do: ưu đãi thuế, lỗ chuyển tiếp, thu nhập miễn thuế |
| 8 | Leverage ratio logic | Net debt/EBITDA, D/E, Interest Coverage di chuyển cùng debt, EBITDA và interest |
| 9 | Margin reasonableness | Gross margin, EBITDA margin, EBIT margin có cơ chế hỗ trợ, nhất là khi vượt lịch sử/peer |
| 10 | Funding sufficiency | Cash không âm; nếu âm phải có financing plan, không dùng plug mơ hồ |

Nếu 6 check đầu fail, mô hình chưa đủ điều kiện dùng cho valuation. Nếu check 7-10 fail, có thể dùng để stress-test nhưng phải gắn caveat và sensitivity.

## 10. VN-Specific Modeling Quirks

**VAS translation reserve:** Chênh lệch tỷ giá do chuyển đổi báo cáo tài chính của đơn vị nước ngoài hoặc khoản mục tiền tệ có thể đi qua equity/reserve thay vì P&L tùy bản chất. Với công ty có doanh thu USD hoặc công ty con nước ngoài, tách FX operating impact khỏi translation reserve. Không đưa translation gain/loss vào recurring EBITDA.

**Revaluation surplus handling:** VAS nhìn chung theo giá gốc và hạn chế đánh giá lại tài sản. Nếu thấy revaluation surplus hoặc quỹ đánh giá lại tài sản lớn, phải đọc thuyết minh: tài sản nào, cơ sở định giá, đơn vị thẩm định, có được phân phối hay không. Không dùng surplus này như cash-flow value trừ khi có cơ chế monetization.

**Related-party consolidation gotchas:** Giao dịch nội bộ phải loại trừ khi hợp nhất, nhưng RPT với công ty liên kết, cổ đông lớn hoặc bên chưa hợp nhất có thể làm revenue, margin và receivables méo. Tách doanh thu/chi phí/phải thu RPT nếu trọng yếu, kiểm tra DSO RPT và giá giao dịch. Với sở hữu chéo, tránh double count trong SOTP và NAV.

**SOE quasi-mandate on lending:** Với ngân hàng quốc doanh hoặc có vai trò chính sách, loan growth, NIM, credit allocation và forbearance có thể chịu mục tiêu vĩ mô. Banking model không chỉ tối đa hóa ROE; cần stress NIM, quota tín dụng, nợ tái cơ cấu và credit cost theo chu kỳ chính sách.

**Group holding company NAV vs consolidated:** Holding company có thể có NAV cao nhưng cash upstream hạn chế do dividend policy ở công ty con, minority interest, nợ cấp holding, thuế chuyển nhượng, và tài sản chưa niêm yết thanh khoản thấp. Khi model tập đoàn, tách consolidated operating model khỏi holding NAV bridge.

## 11. Worked Mini-Example — 3-year skeleton cho VN steel mill kiểu HPG

Ví dụ chỉ là khung cơ chế, không phải forecast thực tế cho HPG.

**Assumptions:**

| Driver | Y0 | Y+1 | Y+2 | Y+3 |
|---|---:|---:|---:|---:|
| Steel volume, mn tons | 8.0 | 8.6 | 9.2 | 9.8 |
| ASP, VND mn/ton | 15.0 | 14.5 | 15.2 | 15.8 |
| Revenue, VND tn | 120.0 | 124.7 | 139.8 | 154.8 |
| Raw material cost / ton | 11.2 | 10.9 | 11.2 | 11.5 |
| Gross margin | 18.0% | 19.0% | 19.5% | 20.0% |
| SG&A / revenue | 3.0% | 3.1% | 3.0% | 2.9% |
| D&A, VND tn | 8.0 | 9.0 | 10.5 | 12.0 |
| CapEx, VND tn | 18.0 | 25.0 | 22.0 | 12.0 |
| DSO / DIO / DPO | 35/90/55 | 38/95/55 | 36/90/58 | 35/85/60 |

**P&L skeleton:**

| VND tn | Y+1 | Y+2 | Y+3 |
|---|---:|---:|---:|
| Revenue | 124.7 | 139.8 | 154.8 |
| Gross profit | 23.7 | 27.3 | 31.0 |
| SG&A | (3.9) | (4.2) | (4.5) |
| EBITDA | 28.8 | 33.6 | 38.5 |
| D&A | (9.0) | (10.5) | (12.0) |
| EBIT | 19.8 | 23.1 | 26.5 |
| Interest expense | (3.2) | (3.8) | (3.6) |
| Tax @ 20% | (3.3) | (3.9) | (4.6) |
| LNST | 13.3 | 15.4 | 18.3 |

**Cash and funding read-through:**

| VND tn | Y+1 | Y+2 | Y+3 |
|---|---:|---:|---:|
| LNST + D&A | 22.3 | 25.9 | 30.3 |
| ΔNWC | (5.5) | (3.0) | (1.5) |
| CFO | 16.8 | 22.9 | 28.8 |
| CapEx | (25.0) | (22.0) | (12.0) |
| FCF before financing | (8.2) | 0.9 | 16.8 |
| Net debt change before dividends | +8.2 | (0.9) | (16.8) |

Interpretation: P&L cải thiện nhờ volume, ASP và margin hồi phục, nhưng Y+1 vẫn cần funding vì growth CapEx và inventory cycle. Nếu bear case cho ASP giảm 8%, DIO tăng 20 ngày và interest rate tăng 200 bps, cash need có thể tăng nhanh dù EBITDA vẫn dương. Đây là lý do mô hình thép phải stress cùng lúc price, volume, inventory và debt, không chỉ giảm revenue tuyến tính.

## 12. Output Format — dùng trong workflow-deep-dive.md

Khi tích hợp vào `workflow-deep-dive.md`, forecast table thuộc Step 2/3 của protocol: Step 2 xác định driver và cơ chế kinh doanh; Step 3 lượng hóa forecast và valuation input. Output tối thiểu:

| Section | Nội dung |
|---|---|
| Forecast driver table | Revenue, margin, working capital, CapEx, debt, tax, dividend assumptions |
| 3-statement summary | P&L, BS, CF 3-5 năm; chỉ giữ dòng trọng yếu |
| Integrity checklist | 8-10 checks với pass/fail và caveat |
| Scenario bridge | Base/low/high driver changes và impact lên EBITDA, FCF, leverage |
| Valuation handoff | FCFF/FCFE, normalized EBITDA, net debt, share count, WACC caveats |

Không trình bày mô hình như bài học kế toán. Trình bày như công cụ nghiên cứu: assumptions, mechanics, outputs, failure points, và signposts.

## 13. Cross-References

- `workflow-deep-dive.md` — owns full research note; đặt forecast table ở Step 2/3 và dùng integrity checks trước valuation.
- `domain-equity-vn-valuation-advanced.md` — nhận FCFF, EBITDA, WACC caveats, reverse DCF assumptions, SOTP/NAV bridge và scenario bounds từ mô hình.
- `domain-equity-vn-forensic-accounting.md` — dùng DSO/DIO/DPO, CFO/LNST, accrual ratio, RPT receivables và covenant stress để kiểm tra chất lượng lợi nhuận.
- `domain-equity-vn-industry-guides.md` — dùng để chọn driver ngành: banking, BĐS, thép, bán lẻ, cảng/logistics, điện, chứng khoán.
- `core-evidence-ladder.md` — phân cấp bằng chứng cho assumptions: filing audited, thuyết minh, management guidance, industry data, hoặc analyst judgment.

Final output contract: mô hình phải cân, cash tie-out phải khớp, assumptions phải giải thích được bằng cơ chế ngành, và mọi valuation input phải truy ngược được về P&L, BS và CF. Không đưa target price, buy/sell/hold, hoặc điểm vào/ra.

> END OF MODULE — domain-equity-vn-financial-modeling.md
>
> Last updated: 2026-04-19 | Wave 4 Lane 5 | Ported from FinMentor 112 | OPVIA Sigma format
