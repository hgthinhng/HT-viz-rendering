---
title: "Framework Thakor-Yu 2024 — Bank Capital, Funding Liquidity Creation, Basel III, Vietnam Credit Transmission"
module_type: "framework"
file_name: "framework-thakor-yu-2024.md"
purpose: "Codify the Thakor-Yu bank capital and funding liquidity creation framework for Vietnam banking, Basel III Tier-1 pressure, state-owned bank behavior, and credit-cycle analysis."
primary_triggers:
  - "Thakor Yu 2024"
  - "bank capital and liquidity"
  - "funding liquidity creation"
  - "Basel III Tier-1"
  - "LCR LDR RWA"
  - "ngan hang quoc doanh"
  - "chu ky tin dung Viet Nam"
when_to_use:
  - "Analyze bank lending capacity under capital or liquidity pressure."
  - "Assess Basel III transition, Tier-1 buffer tightness, LCR/LDR constraints, and state-owned bank credit behavior."
  - "Connect bank balance-sheet constraints to Vietnam macro liquidity and equity-bank sector views."
when_not_to_use:
  - "Do not use as a stand-alone bank valuation model."
  - "Do not apply mechanically to non-bank credit, shadow banking, finance companies, or bond-market credit without adapting funding structure."
related_modules:
  - "domain-macro-vn-liquidity.md"
  - "domain-macro-vn-credit-cycle.md"
  - "domain-fi-vn-ldr-and-bank-funding.md"
  - "framework-kashyap-stein-2000.md"
  - "framework-brunnermeier-pedersen-2009.md"
authoritative_citations:
  - "Thakor, A. V., & Yu, E. G. (2024). Funding liquidity creation by banks. Journal of Financial Stability, 73, 101295. https://doi.org/10.1016/j.jfs.2024.101295"
  - "Thakor, A. V., & Yu, E. G. (2023). Funding Liquidity Creation by Banks. Federal Reserve Bank of Philadelphia Working Paper No. 23-02."
output_owner: "Analytical framework only; pair with macro-vn liquidity, bank-sector deep-dive, or fixed-income funding modules for final output."
---

# Framework Thakor-Yu 2024 — Bank Capital & Funding Liquidity Creation

Purpose: Apply the Thakor-Yu lens to Vietnam banking: capital is not only a solvency buffer but also a condition for sustained liquidity creation and credit supply. Trigger keywords: Basel III, Tier-1, CAR, LCR, LDR, RWA growth, funding liquidity creation, state-owned banks, VN credit cycle.

## 1. Authors & Source

**Anjan V. Thakor and Edison G. Yu (2024).** "Funding liquidity creation by banks." *Journal of Financial Stability*, 73, Article 101295. DOI: 10.1016/j.jfs.2024.101295. Working paper version: Federal Reserve Bank of Philadelphia Working Paper No. 23-02, 2023.

Note for OPVIA retrieval: prompt shorthand may call this "Bank Capital and Liquidity" and may refer to "Fenghua Yu"; public bibliographic metadata for the 2024 journal article lists **Edison G. Yu** as co-author. The operational framework below follows the requested OPVIA interpretation: capital and liquidity are complements, not substitutes, in bank credit creation.

## 2. Core thesis

Thakor-Yu đảo ngược trực giác đơn giản rằng ngân hàng chỉ cho vay khi có sẵn tiền gửi hoặc thanh khoản dư thừa. Trong framework này, ngân hàng tạo **funding liquidity** thông qua hoạt động cho vay: loan creates deposit, và private money creation giúp nền kinh tế tài trợ dự án thực vượt quá lượng cash endowment ban đầu. Điểm quan trọng cho OPVIA là **bank capital và liquidity không phải substitutes mà là complements**. Equity buffer cao hơn giúp ngân hàng chịu rủi ro tín dụng, giữ tài sản kém thanh khoản, duy trì niềm tin của depositor/wholesale funder, và tiếp tục tạo tín dụng ngay cả khi cash deposits không tăng. Vì vậy, trong stress regime, câu hỏi không chỉ là "ngân hàng còn thanh khoản không?" mà là "capital buffer có đủ để biến thanh khoản thành lending capacity không?". Với Việt Nam, điều này đặc biệt quan trọng khi Basel III, Tier-1 quality, RWA growth, room tín dụng, LDR và hành vi ngân hàng quốc doanh cùng quyết định độ bền của lending channel.

## 3. Key variables / mechanisms

**Tier-1 capital ratio / CET1 proxy:** biến lõi để đo khả năng hấp thụ lỗ và năng lực mở rộng RWA. Trong VN, cần phân biệt CAR công bố theo Basel II, chất lượng vốn cấp 1, vốn nhà nước bổ sung, retained earnings, và khả năng phát hành riêng lẻ.

**Liquidity Coverage Ratio (LCR):** đo khả năng chịu liquidity stress ngắn hạn. LCR tốt nhưng capital mỏng không tự động tạo được tín dụng; ngân hàng có thể giữ HQLA để phòng thủ thay vì tăng lending.

**Loan-to-Deposit Ratio (LDR):** chỉ báo funding tightness. LDR cao làm tăng chi phí huy động, giảm room cho vay mới, và buộc ngân hàng cạnh tranh deposit rate.

**Risk-weighted assets (RWA) growth:** cầu nối giữa tăng trưởng tín dụng và tiêu hao vốn. Cùng một mức tăng loan, RWA tăng nhanh hơn nếu mix chuyển sang bất động sản, SME, consumer finance hoặc corporate có risk weight cao.

**Equity-to-asset ratio:** chỉ báo leverage thô. Useful khi so sánh cross-bank, nhưng phải điều chỉnh off-balance-sheet commitment, trái phiếu doanh nghiệp nắm giữ, và asset quality.

**Funding liquidity creation ratio:** theo tinh thần Thakor-Yu, quan sát phần deposit/loan expansion không được giải thích bởi cash deposit inflow. Với VN, proxy thực dụng là tăng trưởng tín dụng trừ tăng trưởng tiền gửi khách hàng, điều chỉnh interbank funding, giấy tờ có giá, và OMO liquidity.

**State-owned bank policy function:** VCB, BID, CTG, Agribank có thể duy trì lending khi private JSB co lại vì có implicit sovereign support, deposit franchise mạnh, và ưu tiên room tín dụng. Nhưng nếu Tier-1 bị bó, policy mandate cũng không loại bỏ constraint kế toán.

## 4. When to apply

Apply framework này khi phân tích **stress regime**, nhất là lúc hệ thống ngân hàng vừa chịu áp lực tỷ giá/lãi suất vừa phải duy trì tăng trưởng tín dụng. Đây là lens tốt cho bank-sector deep-dive khi câu hỏi là "ai còn khả năng cho vay?" hơn là "ai đang có NIM cao?".

Sử dụng trong **late-stage credit cycle**: tín dụng tăng nhanh, RWA phình, LDR tăng, deposit beta cao, còn capital raising chậm. Framework giúp phát hiện khi headline credit target vẫn còn nhưng balance-sheet capacity thực đã hẹp.

Dùng cho **Basel III transition** và policy analysis: Tier-1 pressure có thể làm credit supply phân hóa giữa SOE banks có hỗ trợ vốn, private top-tier banks có retained earnings mạnh, và small JSB phụ thuộc deposit/wholesale funding.

Không dùng framework này để kết luận trực tiếp về định giá cổ phiếu ngân hàng. Nó tạo ra lending-capacity diagnosis; valuation cần thêm NIM, fee income, credit cost, asset quality, governance, và market expectations.

## 5. How to apply (operationalized)

**Step 1: Build bank capital table.** Lập bảng theo từng ngân hàng: CAR, Tier-1/CET1 proxy, equity-to-asset, retained earnings capacity, planned capital raise, dividend payout, RWA density, NPL/LLR, và exposure tới real estate/corporate bond. Tách SOE banks, large private banks, mid-tier JSB, small JSB.

**Step 2: Identify buffer tightness.** So sánh capital ratio hiện tại với regulatory minimum, management buffer, và RWA growth implied bởi credit growth target. Nếu RWA growth 15% nhưng Tier-1 chỉ tăng 5-7%, capital buffer bị ăn mòn dù headline CAR chưa vi phạm.

**Step 3: Map liquidity constraint.** Đặt LCR/LDR/deposit growth cạnh capital table. Nếu LDR cao và deposit growth yếu, ngân hàng cần tăng deposit rate hoặc phát hành giấy tờ có giá. Nếu LCR cao nhưng Tier-1 mỏng, ngân hàng phòng thủ liquidity chứ không necessarily mở loan book.

**Step 4: Forecast lending capacity.** Ước tính loan growth feasible theo 3 constraint: capital, funding, và regulatory room. Lending capacity thực là minimum của ba constraint này, không phải con số room tín dụng được cấp.

**Step 5: Link to credit cycle stage.** Nếu nhiều ngân hàng đồng thời capital-tight và funding-tight, hệ thống chuyển sang late-cycle / deleveraging pressure. Nếu SOE banks còn buffer nhưng private JSB bị bó, credit allocation sẽ nghiêng về khách hàng lớn, SOE, infrastructure, export blue chips; SME và BĐS yếu hơn.

**Step 6: Translate into cross-asset implications.** Capital-tight banking system thường đồng nghĩa VN rates khó giảm sâu, USD/VND nhạy hơn với outflow, equity multiple của cyclical sectors bị nén, và bank stocks phân hóa theo capital quality.

## 6. Limitations & critique

**Regulatory arbitrage:** ngân hàng có thể tối ưu RWA bằng collateral, guarantee, loan classification, off-balance-sheet commitment hoặc chuyển rủi ro sang trái phiếu/ủy thác. Vì vậy RWA growth có thể thấp hơn risk growth thực.

**Non-bank credit:** VN credit cycle không chỉ nằm ở NHTM. Trái phiếu doanh nghiệp, finance companies, broker margin, supplier credit và shadow lending có thể bù hoặc khuếch đại banking constraint. Nếu chỉ nhìn bank balance sheet, framework sẽ underestimate total credit stress.

**Shadow banking and extend-and-pretend:** asset quality bị che bởi cơ cấu nợ, rollover trái phiếu, và real estate collateral chưa mark-to-market. Capital buffer công bố có thể overstated nếu credit cost bị trì hoãn.

**Policy dominance:** NHNN có room tín dụng, OMO, FX intervention, administrative guidance và moral suasion. Những công cụ này có thể làm lending response khác với thị trường phát triển. Framework vẫn useful, nhưng cần overlay policy reaction function.

**Deposit franchise heterogeneity:** SOE banks có deposit stickiness và trust premium lớn hơn private JSB. Một LDR giống nhau không có cùng meaning giữa VCB và một small JSB.

## 7. Linked frameworks

**Kashyap-Stein (2000) bank lending channel:** bổ sung transmission lens: khi monetary policy tighten, small/illiquid banks co lending mạnh hơn. Thakor-Yu giải thích vì sao capital buffer quyết định khả năng duy trì funding liquidity creation.

**Brunnermeier-Pedersen (2009) funding liquidity / market liquidity spiral:** dùng khi liquidity stress lan từ bank funding sang asset fire sale và market liquidity. Thakor-Yu là pre-stress balance-sheet capacity lens; Brunnermeier-Pedersen là stress amplification lens.

**Bernanke-Gertler financial accelerator:** nối bank credit constraint với borrower balance-sheet deterioration, collateral value, và investment decline.

**OPVIA Regime v1.1:** dùng để classify macro backdrop: easing liquidity, tight liquidity, FX-defense, or credit deleveraging regime.

## 8. OPVIA usage examples

**Case A: VCB 2024 Basel III transition.** VCB là case tốt để tách liquidity strength khỏi capital deployment capacity. Deposit franchise mạnh, CASA/retail trust cao, asset quality tốt và vai trò quốc doanh giúp VCB thường có funding advantage. Nhưng khi chuyển sang Basel III hoặc tiêu chuẩn Tier-1 chất lượng cao hơn, câu hỏi OPVIA không phải "VCB có thanh khoản không?" mà là "VCB có đủ Tier-1 buffer để tiếp tục tăng RWA trong khi vẫn giữ management buffer và policy role không?". Nếu VCB được ưu tiên room tín dụng, framework dự báo VCB có thể nhận phần lending share từ private JSB yếu hơn, nhất là khách hàng corporate chất lượng cao. Nhưng nếu capital raise bị chậm, VCB có incentive chọn lọc loan book, ưu tiên low-risk-weight, fee relationship, government-linked projects, và giữ HQLA thay vì tăng rủi ro balance sheet.

**Case B: Small JSB forced deleveraging scenario.** Một small joint-stock bank có LDR cao, deposit growth yếu, RWA density lớn do SME/BĐS, và Tier-1 buffer mỏng sẽ bị bó bởi cả funding và capital. Khi NHNN giữ chính sách thận trọng hoặc deposit competition tăng, ngân hàng này phải chọn: tăng deposit rate làm giảm NIM, bán tài sản thanh khoản, giảm loan growth, hoặc chuyển sang fee/rollover để tránh crystallize NPL. Theo Thakor-Yu, ngân hàng không chỉ thiếu "tiền để cho vay"; nó thiếu capital credibility để tạo funding liquidity mới. Kết quả là forced deleveraging xuất hiện trước khi CAR headline chạm sàn: giải ngân mới chậm, renewal khắt khe hơn, SME borrower bị squeeze, và credit cycle chuyển từ expansion sang rationing.

---
*OPVIA internal framework module. Research use only; no buy/sell/hold recommendation.*
