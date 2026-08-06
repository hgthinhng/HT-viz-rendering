---
title: "Framework Borio Financial Cycle — Credit, Asset Prices, Medium-Term Boom-Bust, Vietnam Financial Cycle"
module_type: "framework"
file_name: "framework-borio-financial-cycle.md"
purpose: "Codify Claudio Borio's financial-cycle framework for Vietnam credit, property, banking, rates, and boom-bust regime analysis."
priority: "P1 / Kimi P1"
rag_status: "GREEN - academic framework codified; requires updated credit, property, bank, and rates data for live classification."
primary_triggers:
  - "Borio financial cycle"
  - "financial cycle vs business cycle"
  - "credit and asset prices"
  - "medium-term cycle"
  - "15-20 year cycle"
  - "Vietnam credit boom bust"
  - "financial cycle Vietnam"
when_to_use:
  - "Separate financial-cycle phases from ordinary GDP/business-cycle fluctuations."
  - "Analyze credit plus asset-price booms, busts, balance-sheet repair, and policy constraints."
  - "Classify Vietnam episodes such as 2008-2013 bust, 2014-2021 boom, and 2022+ correction."
when_not_to_use:
  - "Do not use as a high-frequency recession nowcast."
  - "Do not force a 15-20 year periodicity on short or structurally broken Vietnam data."
related_modules:
  - "domain-macro-vn-credit-cycle.md"
  - "domain-macro-vn-liquidity-systems.md"
  - "domain-macro-vn-regime-framework-v11.md"
  - "domain-fi-vn-yield-curve.md"
  - "framework-minsky-1986.md"
  - "framework-allen-gale-2000.md"
  - "framework-thakor-yu-2024.md"
authoritative_citations:
  - "Borio, C. (2014). The financial cycle and macroeconomics: What have we learnt? Journal of Banking & Finance, 45, 182-198. Also BIS Working Papers No. 395, 2012. https://www.bis.org/publ/work395.htm"
  - "Drehmann, M., Borio, C., & Tsatsaronis, K. (2012). Characterising the financial cycle: don't lose sight of the medium term! BIS Working Papers No. 380. https://www.bis.org/publ/work380.htm"
output_owner: "Analytical framework only; pair with OPVIA Regime v1.1 and Vietnam credit/property datasets for final output."
---

# Framework Borio Financial Cycle — Credit + Asset Prices

Purpose: Dùng lens Claudio Borio để tách **financial cycle** khỏi **business cycle**. Với Việt Nam, framework này đọc 2008-2013 bust, 2014-2021 boom và 2022+ correction như chu kỳ tín dụng, BĐS, collateral và bảng cân đối.

## 1. Authors & Source

**Claudio Borio (BIS, 2012/2014).** "The financial cycle and macroeconomics: What have we learnt?" BIS Working Papers No. 395, sau đó đăng trên *Journal of Banking & Finance* 45, 182-198.

Framework liên quan mật thiết tới **Drehmann, Borio and Tsatsaronis (2012)**, "Characterising the financial cycle: don't lose sight of the medium term!" BIS Working Papers No. 380. Nhánh BIS này nhấn mạnh rằng chu kỳ tài chính thường dài hơn chu kỳ kinh doanh, biên độ lớn hơn, và là nguồn gốc chính của các cuộc khủng hoảng ngân hàng.

## 2. Core thesis

Borio cho rằng macro truyền thống quá tập trung vào business cycle: GDP, output gap, lạm phát và thất nghiệp trong horizon vài quý đến vài năm. Nhưng rủi ro khủng hoảng tài chính tích tụ trong **financial cycle** dài hơn, đo bằng **credit** và **asset prices**, đặc biệt là BĐS. Financial cycle có thể kéo dài khoảng 15-20 năm ở nhiều nền kinh tế phát triển. Khi đi lên, tín dụng tăng, collateral tốt hơn, perceived risk giảm, ngân hàng nới chuẩn và leverage tiếp tục tăng. Khi đảo chiều, collateral giảm, borrower và ngân hàng repair balance sheet, tín dụng chậm lại, và kinh tế có thể yếu lâu dù policy rate đã giảm.

Điểm quan trọng cho OPVIA: financial cycle có thể **không trùng pha** với business cycle. GDP có thể vẫn tăng ổn trong late financial boom, khiến nhà phân tích đánh giá rủi ro quá thấp. Ngược lại, sau bust, GDP có thể hồi phục kỹ thuật nhưng tín dụng, BĐS, ngân hàng và risk appetite vẫn đang trong giai đoạn balance-sheet repair. Với Việt Nam, nơi ngân hàng là kênh tín dụng chính và BĐS là collateral system lớn, financial cycle thường giải thích regime tốt hơn chỉ số business cycle ngắn hạn.

## 3. Key variables / mechanisms

**Credit-to-GDP gap:** biến lõi trong truyền thống BIS. Tín dụng tăng nhanh hơn GDP trong thời gian dài là dấu hiệu leverage hệ thống đang tích tụ.

**Real credit growth:** tăng trưởng tín dụng sau khi trừ lạm phát. Useful hơn nominal credit khi CPI biến động.

**Property prices / land liquidity:** asset-price leg quan trọng nhất ở Việt Nam. Không chỉ giá niêm yết, cần xem thanh khoản giao dịch, absorption rate, pháp lý dự án, presales và discount thực.

**Equity and bond risk appetite:** VN-Index multiple, margin lending, corporate bond spread, issuance volume và default/restructuring là chỉ báo bổ trợ.

**Bank balance-sheet health:** NPL, restructured loans, LLR, LDR, CAR/Tier-1, deposit growth, credit allocation theo sector. Đây là kênh truyền từ financial cycle sang real economy.

**Debt-service burden:** lãi vay cộng gốc đến hạn so với income/cash flow. Financial bust thường kéo dài khi debt-service burden cao dù rate giảm.

**Policy stance versus financial stance:** policy rate thấp không có nghĩa financial condition nới lỏng nếu ngân hàng đang capital-tight, borrower mất collateral, hoặc bond market đóng cửa.

**Risk perception and procyclicality:** trong boom, default thấp làm rủi ro nhìn có vẻ thấp; trong bust, realized loss tăng làm hệ thống phòng thủ quá mức.

## 4. When to apply

Apply khi câu hỏi liên quan tới chu kỳ tín dụng, BĐS, ngân hàng, trái phiếu doanh nghiệp, hoặc định giá cross-asset trung hạn. Nếu cần phân biệt "business-cycle slowdown" với "financial-cycle deleveraging", Borio nên được load.

Dùng khi có các tín hiệu lệch pha: GDP tăng nhưng tín dụng và BĐS nóng bất thường; CPI thấp nhưng asset inflation cao; policy easing nhưng credit không chạy; equity hồi phục nhưng bond/property vẫn stress; hoặc lãi suất giảm nhưng borrower vẫn không vay vì balance sheet yếu.

Không dùng Borio như một model timing ngắn hạn. Framework này không nói tháng nào thị trường đảo chiều. Nó giúp xác định nền móng rủi ro, regime trung hạn và lý do một cú sốc nhỏ có thể gây hậu quả lớn nếu xảy ra ở cuối financial boom.

## 5. How to apply (operationalized)

**Step 1: Build financial-cycle dashboard.** Gom credit-to-GDP, real credit growth, credit impulse, property liquidity/price proxy, corporate bond issuance/spread/default, bank LDR/NPL/restructured loan, VN-Index valuation, margin lending và policy rate.

**Step 2: Separate business-cycle indicators.** Đặt GDP, PMI, retail sales, export growth, CPI, unemployment và industrial production ở panel riêng. Mục tiêu là không để GDP growth che khuất leverage cycle.

**Step 3: Classify phase.** Dùng bốn pha thực dụng: early repair, expansion, late boom, correction/deleveraging. Expansion có credit và asset price cùng tăng nhưng debt-service chưa căng. Late boom có credit quality giảm, asset price phụ thuộc rollover, risk premium thấp. Correction có credit slowdown, asset illiquidity, default/restructuring và bank caution.

**Step 4: Test credit-asset feedback.** Hỏi giá tài sản tăng có đang làm collateral tốt hơn và cho phép vay thêm không. Nếu có, financial cycle đang tự khuếch đại. Khi asset price giảm, cùng cơ chế đó sẽ đảo chiều.

**Step 5: Overlay policy reaction.** Ở Việt Nam, NHNN có room tín dụng, OMO, lãi suất điều hành, tỷ giá, quy định trái phiếu và cơ cấu nợ. Phân tích policy phải hỏi công cụ nào tác động vào liquidity, công cụ nào tác động vào solvency, và công cụ nào chỉ kéo dài thời gian repair.

**Step 6: Derive cross-asset implications.** Trong late boom, equity cyclicals và BĐS có thể outperform nhưng fragility tăng. Trong correction, VN rates có thể giảm ở front-end nhưng credit spread rộng, bank lending chọn lọc, USD/VND nhạy với outflow, và equity multiple bị nén nếu earnings bị debt overhang.

**Step 7: State confidence and data gaps.** Vì data BĐS Việt Nam thiếu chuẩn, phải ghi rõ proxy dùng: presales, bank exposure, transaction reports, auction data hoặc brokerage data.

## 6. Limitations & critique

Chu kỳ 15-20 năm là quan sát medium-term ở nhiều nước, không phải định luật vật lý. Việt Nam có structural breaks lớn: WTO accession, thay đổi room tín dụng, tái cấu trúc ngân hàng sau 2011, phát triển trái phiếu doanh nghiệp, COVID, và siết pháp lý BĐS. Không nên ép data Việt Nam vào chu kỳ cố định.

Data BĐS và nợ xấu Việt Nam hạn chế. Giá niêm yết có thể lệch giá giao dịch; nợ tái cơ cấu có thể che stress; trái phiếu private placement thiếu minh bạch. Vì vậy phải dùng nhiều proxy và flag confidence.

Borio cũng có thể làm nhà phân tích quá thận trọng trong một nền kinh tế catch-up. Credit-to-GDP tăng có thể phản ánh financial deepening thật. Cần phân biệt tín dụng sản xuất, hạ tầng, FDI supply chain với tín dụng speculative vào đất và rollover.

Cuối cùng, business cycle vẫn quan trọng. Export shock, oil shock, fiscal impulse hoặc FDI relocation có thể tạo biến động ngắn hạn mạnh. Borio không thay thế macro nowcast; nó là lớp medium-term balance-sheet risk.

## 7. Linked frameworks

**Minsky (1986):** Minsky phân loại cấu trúc tài trợ hedge/speculative/Ponzi; Borio đặt quá trình đó vào chu kỳ tín dụng và asset price toàn hệ thống.

**Allen-Gale (2000):** Allen-Gale giải thích agency và credit expansion trong bubble; Borio giải thích vì sao bubble đó thuộc financial cycle dài hơn business cycle.

**Thakor-Yu (2024):** dùng để đi từ financial-cycle diagnosis xuống năng lực tạo tín dụng của ngân hàng khi capital/liquidity bị bó.

**Geanakoplos (2010):** bổ sung leverage và haircut channel, đặc biệt khi collateral là BĐS hoặc cổ phiếu.

**OPVIA Regime v1.1:** Borio là input quan trọng cho regime classification: liquidity easing, credit expansion, FX-defense, deleveraging, hoặc balance-sheet repair.

## 8. OPVIA usage examples

**Case A: Việt Nam 2008-2013 bust.** Giai đoạn trước 2008, tín dụng tăng rất nhanh, asset prices nóng, lạm phát cao và hệ thống ngân hàng mở rộng mạnh. Sau cú sốc 2008 và giai đoạn thắt chặt 2011, Việt Nam bước vào bust/balance-sheet repair: BĐS đóng băng, nợ xấu ngân hàng lộ ra, VAMC ra đời, tăng trưởng tín dụng chậm lại và risk appetite suy yếu. Business cycle có những quý hồi phục, nhưng financial cycle vẫn ở pha repair vì collateral yếu, bank balance sheet căng và borrower deleveraging. Borio giúp giải thích vì sao nới lỏng chính sách không lập tức tạo boom mới.

**Case B: 2014-2021 boom và 2022+ correction.** Từ sau tái cấu trúc ngân hàng, tín dụng và BĐS dần hồi phục, lãi suất giảm, niềm tin tăng, trái phiếu doanh nghiệp phát triển và equity multiple mở rộng. Đây là expansion chuyển sang late boom khi corporate bond và property funding tăng nhanh hơn cash-flow capacity ở một số nhóm. Năm 2022, Fed hiking, áp lực tỷ giá, siết trái phiếu, xử lý sai phạm và room tín dụng tạo trigger cho correction. Theo Borio, 2022+ không chỉ là business-cycle slowdown; đó là điều chỉnh của financial cycle: bond refinancing đóng, BĐS mất thanh khoản, ngân hàng thận trọng hơn, và policy phải cân bằng giữa hỗ trợ tăng trưởng, ổn định tỷ giá và repair bảng cân đối.

---
*OPVIA internal framework module. Research use only; no buy/sell/hold recommendation.*
