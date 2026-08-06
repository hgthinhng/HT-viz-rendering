---
title: "Domain Equity VN Valuation Advanced — Reverse DCF, SOTP, Real Options, ROIC"
module_type: "domain"
file_name: "domain-equity-vn-valuation-advanced.md"
purpose: "Advanced valuation for Vietnamese listed equities."
primary_triggers: ["định giá nâng cao cổ phiếu Việt Nam", "VN equity advanced valuation", "reverse DCF", "SOTP", "real options", "ROIC", "scenario bounds"]
when_to_use: ["Advanced valuation, embedded expectations, conglomerate valuation, moat-linked ROIC, or scenario fair value.", "Use when DCF, P/E, P/B, or EV/EBITDA alone is insufficient."]
when_not_to_use: ["Do not use for timing, technical analysis, target price, or buy/sell/hold."]
related_modules: ["domain-equity-vn-valuation.md", "domain-equity-vn-moat-analysis.md", "domain-equity-vn-forensic.md", "workflow-deep-dive.md", "core-voice-and-safety.md"]
authoritative_citations: ["Mauboussin/Rappaport, Expectations Investing.", "Damodaran, Investment Valuation.", "Penman, Financial Statement Analysis and Security Valuation."]
output_owner: "Valuation lens only."
---

# Domain Equity VN Valuation Advanced — Định giá nâng cao cổ phiếu Việt Nam

Purpose: Áp dụng Reverse DCF, SOTP, Real Options, ROIC decomposition, và Scenario Bounds Analysis cho cổ phiếu niêm yết Việt Nam khi P/E, P/B, EV/EBITDA hay DCF tuyến tính không đủ. Output luôn là **fair value range**, không phải target price, và không có buy/sell/hold.

Trigger keywords: định giá nâng cao, VN equity valuation, reverse DCF, SOTP, NAV, real options, ROIC, DuPont, scenario bounds, WACC.

Use with: `domain-equity-vn-valuation.md`, `domain-equity-vn-moat-analysis.md`, `domain-equity-vn-forensic.md`, `workflow-deep-dive.md`.

Safety note: **Output = fair value range, NOT target price. No buy/sell/hold.**

## Nguyên tắc chung

Định giá nâng cao làm rõ thị trường đang giả định gì, giá trị nằm ở đâu, phần nào là optionality, ROIC có bền không, và downside/upside có cân xứng không. Mọi kết quả phải là khoảng giá trị. Tại Việt Nam, kiểm tra VAS vs IFRS, cấu trúc tập đoàn, giao dịch liên quan, và dữ liệu phân khúc trước khi định lượng.

## 1. Reverse DCF — giải mã kỳ vọng thị trường

**Khi áp dụng:** Dùng khi P/E, EV/EBITDA hoặc P/B lệch mạnh so với lịch sử/peer; khi doanh nghiệp tăng trưởng cao như FPT; khi ngành chu kỳ như HPG có earnings hiện tại không đại diện; hoặc khi cần biết giá hiện tại đang nhúng giả định nào. Cần giá thị trường, số cổ phiếu, nợ ròng, FCF/NOPAT chuẩn hóa, WACC range, và terminal growth.

**Cách làm:**
1. Bắt đầu từ enterprise value/equity value hiện tại.
2. Chuẩn hóa FCF: loại lãi/lỗ một lần, điều chỉnh working capital bất thường, capex duy trì so với capex mở rộng.
3. Chọn WACC range hợp lý, ví dụ 10-13% cho doanh nghiệp phi tài chính tùy leverage, cyclicality, FX, và country risk.
4. Tính ngược tăng trưởng doanh thu, margin, reinvestment rate, ROIC và terminal growth cần có để biện minh giá hiện tại.
5. So sánh giả định với lịch sử, peer, quy mô thị trường, và moat evidence.
6. Chỉ ra "assumption breakpoint": biến nào sai sẽ làm fair value dịch chuyển mạnh nhất.

**Pitfalls VN:** VAS có thể làm FCF nhiễu do capitalized cost, lãi tiền gửi, cổ tức công ty con/liên kết, hoặc chuyển nhượng tài sản. Với tập đoàn, reverse DCF trên consolidated earnings có thể che mảng phá hủy giá trị. Giao dịch liên quan có thể làm margin hiện tại không phản ánh kinh tế thật.

**Output format:**

| Variable | Bear | Base | Stretch | Evidence |
|---|---:|---:|---:|---|
| Revenue CAGR 5 năm | x% | x% | x% | TAM, backlog, market share |
| EBIT margin | x% | x% | x% | Lịch sử, peer, input cost |
| ROIC terminal | x% | x% | x% | Moat/persistence |
| Fair value read-through | x-y VND/cp | x-y VND/cp | x-y VND/cp | Không phải target price |

Ví dụ: Với FPT, Reverse DCF nên tách kỳ vọng tăng trưởng IT services toàn cầu, biên offshore, và ROIC bền vững. Nếu giá đòi hỏi tăng trưởng hai chữ số kéo dài nhưng headcount, thị trường Nhật/Mỹ, hoặc pricing power không ủng hộ, gắn cờ kỳ vọng nhúng quá căng.

## 2. Sum-of-the-parts — SOTP cho conglomerate/holding

**Khi áp dụng:** Dùng cho doanh nghiệp đa ngành, holding, hoặc công ty có nhiều mảng khác nhau: bất động sản, bán lẻ, sản xuất, tài chính, cảng/logistics, công ty con niêm yết. Cần doanh thu, EBIT/EBITDA, tài sản, nợ, sở hữu, lợi ích cổ đông thiểu số, và dữ liệu phân khúc.

**Cách làm:**
1. Tách legal entities và economic segments. Không mặc định phân khúc kế toán là phân khúc kinh tế.
2. Chọn phương pháp riêng cho từng mảng: DCF cho mảng ổn định, EV/EBITDA cho logistics/cảng, P/B hoặc excess return cho ngân hàng, NAV cho bất động sản, market value cho công ty con niêm yết.
3. Điều chỉnh sở hữu thực tế: tỷ lệ nắm giữ, minority interest, preferred claims, intercompany debt.
4. Trừ net debt cấp holding và nghĩa vụ ngoài bảng cân đối nếu có.
5. Áp dụng holding company discount khi có chiết khấu quản trị, thanh khoản, thuế, hoặc capital allocation kém; ở VN thường kiểm tra 10-30%, không gán máy móc.
6. Đối chiếu với market cap để xác định phần thị trường đang trả cho "stub".

**Pitfalls VN:** Đất ghi theo giá gốc dưới VAS làm book value thấp hơn economic value, nhưng NAV dễ bị thổi phồng nếu chưa trừ thuế, chi phí pháp lý, thời gian triển khai và rủi ro pháp lý. Công ty liên kết có thể ghi theo equity method nhưng cash upstream hạn chế. Giao dịch nội bộ có thể làm EBITDA bị double count.

**Output format:**

| Segment | Method | Own. | Gross range | Adjustments | Equity value |
|---|---|---:|---:|---|---:|
| Mảng A | DCF/Multiple/NAV | x% | x-y | Debt/tax/minority | x-y |
| Holding net debt | Net debt | 100% | n/a | Trừ | (x-y) |
| Holding discount | Discount | n/a | n/a | 10-30% | (x-y) |
| Fair value range |  |  |  |  | x-y VND/cp |

Ví dụ: Với GMD, SOTP nên tách cảng nước sâu, cảng nội địa, logistics, và liên doanh. Cảng có concession, tariff và utilization khác logistics thuần; một EV/EBITDA chung sẽ làm mất nuance về quality và duration của cash flow.

## 3. Real Options — giá trị quyền chọn chiến lược

**Khi áp dụng:** Dùng khi giá trị đến từ quyền có thể làm nhưng chưa bắt buộc làm: mở rộng công suất, phát triển quỹ đất, launch sản phẩm mới, M&A, chuyển đổi công nghệ, hoặc dừng dự án.

**Cách làm:**
1. Xác định option cụ thể: growth option, abandonment option, deferral option, switching option, flexibility premium.
2. Tách value of existing assets khỏi option value; không cộng option lên DCF đã bao gồm cùng tăng trưởng.
3. Xác định trigger: giá bán, utilization, giấy phép, capex cost, demand threshold, WACC giảm.
4. Ước lượng payoff range, chi phí exercise, thời hạn, và xác suất điều kiện xảy ra.
5. Dùng scenario tree/decision tree; chỉ dùng Black-Scholes nếu input có ý nghĩa kinh tế.
6. Haircut mạnh nếu option phụ thuộc phê duyệt pháp lý, vốn vay, hoặc execution ngoài năng lực đã chứng minh.

**Pitfalls VN:** Quyền sử dụng đất, giấy phép, room tín dụng, thủ tục môi trường, PPA, hoặc hạn ngạch có thể là ràng buộc thực. Related-party capex có thể chuyển value từ cổ đông thiểu số sang bên liên quan. VAS không phản ánh đầy đủ fair value của option, nhưng cũng không cho phép gán option value tùy ý.

**Output format:**

| Option | Trigger | Cost | Payoff range | Condition | Value |
|---|---|---:|---:|---|---:|
| Growth option | Utilization > x% | x | x-y | Điều kiện rõ | x-y |
| Abandonment option | ROIC < WACC | Exit cost x | Loss avoided x-y | Điều kiện rõ | x-y |
| Fair value including options |  |  |  |  | x-y VND/cp |

## 4. ROIC Decomposition — DuPont mở rộng và persistence

**Khi áp dụng:** Dùng khi valuation phụ thuộc vào moat, premium multiple, hoặc terminal ROIC cao hơn WACC. Quan trọng với công ty chất lượng cao như FPT/VCB hoặc ngành chu kỳ như HPG, nơi ROIC hiện tại có thể bị bóp bởi chu kỳ.

**Cách làm:**
1. Tính ROIC = NOPAT / invested capital, dùng average invested capital.
2. Phân rã: ROIC = EBIT margin sau thuế x invested capital turnover. Khi cần, tách gross margin, SG&A intensity, working capital intensity, fixed asset turnover.
3. So sánh 5-10 năm với WACC, median ngành, và chu kỳ ngành.
4. Kiểm tra persistence: spread ROIC-WACC có bền, mở rộng, hay thu hẹp.
5. Liên kết với moat evidence: pricing power, switching cost, cost advantage, scale efficiency, regulation.
6. Dùng ROIC để kiểm tra terminal value: không cho phép terminal ROIC cao nếu không có moat kiểm chứng.

**Pitfalls VN:** Invested capital theo VAS có thể thấp giả tạo vì đất/tài sản ghi giá gốc, làm ROIC cao giả; capex dở dang lớn có thể làm ROIC thấp tạm thời. Với ngân hàng như VCB, không dùng ROIC công nghiệp; dùng ROE/P/B, cost of equity, NIM, CIR, credit cost, CASA, asset quality. Với tập đoàn, consolidated ROIC che mảng tốt và xấu.

**Output format:**

| Driver | 5Y | Current | Normalized | Low/Base/High | Evidence |
|---|---:|---:|---:|---:|---|
| EBIT margin | x-y% | x% | x% | x/x/x | Pricing/cost |
| Capital turnover | x-y | x | x | x/x/x | Utilization |
| ROIC | x-y% | x% | x% | x/x/x | Moat persistence |
| ROIC-WACC spread | x-y pp | x pp | x pp | x/x/x | Value creation |

## 5. Scenario Bounds Analysis — low/base/high với asymmetric pricing

**Khi áp dụng:** Dùng cho mọi output cuối cùng, đặc biệt khi biến số tương quan mạnh: giá thép, sản lượng, lãi suất, tỷ giá, credit cost, backlog, utilization. Đây là lớp thay thế point estimate.

**Cách làm:**
1. Chọn 3 kịch bản: Low, Base, High. Không dùng nhãn cảm tính nếu không định nghĩa cơ chế.
2. Mỗi kịch bản phải có driver chính, cơ chế, xác suất nếu có cơ sở, và fair value range.
3. Gắn tương quan biến: trong suy thoái, volume giảm có thể đi cùng giá giảm, WACC tăng, working capital xấu đi.
4. Kiểm tra asymmetry: downside có nhanh hơn upside không, debt covenant có làm equity convex không, capex committed có làm FCF âm không.
5. Không trung bình hóa máy móc. Nếu xác suất chưa hiệu chuẩn, trình bày range và signposts thay vì expected value.

**Pitfalls VN:** Earnings trailing tại đỉnh chu kỳ làm P/E rẻ giả; tại đáy chu kỳ làm P/E đắt giả. VAS có thể trì hoãn lỗ dự phòng hoặc lợi nhuận chuyển nhượng. Dữ liệu segment và backlog đôi khi thiếu kiểm toán. Với HPG, scenario phải tách sản lượng thép, spread HRC/rebar, giá quặng/than, utilization của Dung Quất, và working capital; revenue +/-10% tuyến tính là không đủ.

**Output format:**

| Scenario | Mechanism | Assumptions | Fair value range | Asymmetry | Signposts |
|---|---|---|---:|---|---|
| Low | Cơ chế bất lợi | Giá/volume/WACC/ROIC | x-y VND/cp | Downside path | Dữ liệu cần theo dõi |
| Base | Cơ chế trung tâm | Giá/volume/WACC/ROIC | x-y VND/cp | Balance | Dữ liệu cần theo dõi |
| High | Cơ chế thuận lợi | Giá/volume/WACC/ROIC | x-y VND/cp | Upside path | Dữ liệu cần theo dõi |

## Cross-Reference Block

Use `domain-equity-vn-valuation.md` để chuẩn hóa earnings, DCF, P/E, EV/EBITDA, P/B và WACC. Use `domain-equity-vn-moat-analysis.md` khi terminal ROIC hoặc premium multiple dựa vào moat. Use `domain-equity-vn-forensic.md` khi có lợi nhuận bất thường, giao dịch liên quan, capitalized cost, hoặc cash flow không khớp earnings. Use `domain-equity-vn-banks.md` cho ngân hàng; không ép ROIC công nghiệp vào VCB, TCB, MBB. Use `workflow-deep-dive.md` cho full note.

Final output contract: kết luận bằng **fair value range**, confidence level, dominant variables, accounting/data caveats, and signposts. Không đưa target price. Không đưa buy/sell/hold.
