---
title: "Core Methodology — OPVIA Evidence Hierarchy, Red Flags, Six Analysis Modes, Confidence Calibration"
module_type: "core"
file_name: "core-methodology.md"
purpose: "Define OPVIA methodology discipline for financial research: source hierarchy, sloppy-analysis red flags, six analytical modes, and qualitative confidence calibration."
primary_triggers:
  - "phương pháp luận nghiên cứu"
  - "methodology"
  - "evidence hierarchy"
  - "methodology red flags"
  - "selection bias"
  - "scenario analysis"
  - "stress test"
  - "confidence calibration"
when_to_use:
  - "Use whenever a research output needs evidence ranking, methodological caveats, or confidence calibration."
  - "Use to audit whether a thesis, model, or market narrative is analytically sound."
when_not_to_use:
  - "Do not use as a standalone valuation model or domain-specific framework."
  - "Do not use to replace workflow-deep-dive.md or core-research-protocol.md."
related_modules:
  - "core-research-protocol.md"
  - "core-meta-cognition.md"
  - "core-evidence-ladder.md"
  - "workflow-deep-dive.md"
  - "workflow-pre-mortem.md"
  - "framework-dickinson-mauboussin.md"
  - "framework-*"
authoritative_citations:
  - "CFA Institute research and ethics standards."
  - "Mauboussin, M. Expectations Investing and judgment calibration work."
  - "Penman, S. Financial Statement Analysis and Security Valuation."
  - "OPVIA internal Research Partner Protocol."
output_owner: "Methodology discipline only; final output format is owned by the relevant workflow module."
---

# Core Methodology — Phương pháp luận nghiên cứu OPVIA

Purpose: Chuẩn hóa cách OPVIA đánh giá chất lượng bằng chứng, phát hiện lỗi phương pháp luận, chọn mode phân tích phù hợp, và hiệu chuẩn mức tự tin trong research output. Trigger keywords: evidence hierarchy, bậc bằng chứng, methodology red flags, selection bias, survivorship bias, hindsight bias, cherry-picking, straw man, quantitative analysis, scenario analysis, stress test, bounds, calibration.

Module này vận hành cùng `core-research-protocol.md`: protocol quyết định trình tự nghiên cứu, methodology quyết định tiêu chuẩn chất lượng của từng nhận định. Khi kết luận quan trọng không qua được tiêu chuẩn nguồn, cơ chế, hoặc kiểm tra phản chứng, phải hạ mức tự tin hoặc ghi rõ gap thay vì lấp bằng narrative.

---

## 1. Evidence Hierarchy — Bậc bằng chứng

Mọi nhận định quan trọng phải gắn chất lượng nguồn. Không phải mọi dữ liệu đều có cùng quyền lực giải thích. OPVIA dùng thứ tự ưu tiên sau:

1. **Primary-source / nguồn gốc trực tiếp**: báo cáo tài chính, thuyết minh BCTC, nghị quyết, prospectus, filing, dữ liệu chính thức từ sở giao dịch, ngân hàng trung ương, cơ quan thống kê, văn bản pháp lý. Đây là bậc mạnh nhất cho sự kiện đã công bố, nhưng vẫn cần đọc điều khoản, phạm vi hợp nhất, chuẩn kế toán, và thay đổi chính sách ghi nhận.
2. **Peer-reviewed / nghiên cứu học thuật đã phản biện**: dùng cho cơ chế tổng quát, base rate, hành vi thị trường, hoặc framework đã kiểm định. Không tự động áp dụng vào một công ty nếu bối cảnh thị trường, chu kỳ, hoặc cấu trúc ngành khác biệt.
3. **Broker research / sell-side hoặc institutional research**: hữu ích để lấy giả định thị trường, peer set, dữ liệu ngành, và điểm tranh luận. Phải kiểm tra xung đột lợi ích, phương pháp dự báo, và mức phụ thuộc vào management guidance.
4. **News / truyền thông tài chính**: phù hợp để nhận diện sự kiện, timeline, sentiment, và thay đổi chính sách. Không dùng một mình để kết luận về intrinsic value, fraud, moat, hoặc năng lực quản trị.
5. **Rumor / tin đồn, social media, anecdote**: chỉ là tín hiệu cần kiểm chứng. Không đưa vào verdict trừ khi ghi rõ là unverified signal và nêu kế hoạch xác minh.

Nguyên tắc xử lý mâu thuẫn: ưu tiên bậc cao hơn; nếu cùng bậc, ưu tiên nguồn gần dữ kiện gốc hơn, mới hơn, có phương pháp rõ hơn, và có cơ chế kinh tế thuyết phục hơn. Nếu vẫn mâu thuẫn, nêu cả hai phía và đánh dấu `TRANH LUẬN ĐANG MỞ`.

---

## 2. Methodology Red Flags — Dấu hiệu phân tích cẩu thả

Một phân tích có vẻ hợp lý vẫn có thể sai vì lỗi chọn mẫu hoặc câu chuyện hóa dữ kiện. Các red flags sau phải được kiểm tra trước khi dùng kết luận:

- **Selection bias**: chỉ chọn quan sát thuận lợi cho thesis. Ví dụ: lấy 3 doanh nghiệp thắng cuộc để kết luận ngành có moat, nhưng bỏ qua nhóm thất bại hoặc bị delist.
- **Survivorship bias**: chỉ phân tích các công ty còn tồn tại nên đánh giá quá cao tỷ lệ duy trì ROIC, biên lợi nhuận, hoặc tăng trưởng.
- **Hindsight bias**: sau khi kết quả xảy ra, diễn giải như thể nó đã hiển nhiên từ trước. Red flag này làm backtest và case study trở nên quá sạch.
- **Cherry-picking**: chọn mốc thời gian, peer group, chỉ tiêu, hoặc năm cơ sở có lợi cho kết luận. Phải kiểm tra độ nhạy với mốc khác.
- **Straw man**: phản bác phiên bản yếu nhất của quan điểm đối lập. OPVIA yêu cầu trình bày strongest opposing case trước khi bác bỏ.
- **Extrapolation đỉnh/đáy chu kỳ**: dùng margin, volume, hoặc cost of capital ở trạng thái cực đoan làm base case.
- **Circular valuation**: dùng market price làm input rồi kết luận market price hợp lý. Valuation phải tách khỏi giá trước khi so sánh.

Khi gặp red flag, không nhất thiết loại bỏ toàn bộ phân tích. Việc đúng là hạ confidence, ghi rõ điều kiện, yêu cầu bổ sung kiểm chứng, hoặc chuyển kết luận thành hypothesis.

---

## 3. Six Modes Of Analysis — 6 mode phân tích

**Quantitative analysis** trả lời “con số nói gì?”. Dùng cho financial ratios, growth decomposition, margin bridge, ROIC/WACC, leverage, cash conversion, valuation sensitivity. Rủi ro chính là false precision: mô hình có nhiều chữ số nhưng giả định yếu.

**Qualitative analysis** trả lời “cơ chế kinh tế là gì?”. Dùng cho moat, governance, regulation, competitive dynamics, customer behavior, supply chain, disclosure quality. Định tính có quyền veto khi phát hiện rủi ro cấu trúc, nhưng không có quyền tạo thesis nếu định lượng không ủng hộ.

**Comparative analysis** trả lời “so với ai và so với lịch sử nào?”. Dùng peer set, cross-cycle comparison, local vs regional benchmark, company vs industry. Peer phải cùng business economics; cùng sàn niêm yết không đủ.

**Scenario analysis** trả lời “những trạng thái tương lai hợp lý là gì?”. Base case không phải dự báo duy nhất. Cần ít nhất downside, base, upside, kèm driver chính và điều kiện kích hoạt.

**Stress analysis** trả lời “điều gì xảy ra khi biến xấu đồng thời?”. Dùng cho lãi suất, FX, refinancing, commodity input, regulatory shock, demand collapse. Stress test ưu tiên bảng cân đối và liquidity trước valuation.

**Bounds analysis** trả lời “khoảng hợp lý nằm đâu?”. Khi uncertainty cao, không ép ra một điểm định giá. Dùng range, floor/ceiling logic, reverse DCF, và invalidation trigger để tránh pseudo-precision.

---

## 4. Confidence Calibration — Thang tự tin

OPVIA dùng thang định tính **low / medium / high**, không dùng phần trăm giả chính xác.

**High confidence**: nguồn primary hoặc peer-reviewed mạnh, nhiều nguồn độc lập xác nhận, cơ chế kinh tế rõ, kết luận chịu được sensitivity và phản chứng chính. Vẫn cần ghi validity window.

**Medium confidence**: bằng chứng hợp lý nhưng còn gap, phụ thuộc giả định chu kỳ, hoặc có mâu thuẫn chưa đủ lớn để phủ định. Đây là mức phổ biến nhất trong phân tích thị trường.

**Low confidence**: dữ liệu thiếu, nguồn yếu, mâu thuẫn lớn, regime mới, hoặc thesis phụ thuộc narrative. Low confidence không có nghĩa là sai; nghĩa là chưa đủ quyền lực để kết luận mạnh.

Quy tắc: confidence phải phản ánh chất lượng bằng chứng, không phản ánh mức hấp dẫn của câu chuyện hay mức đồng thuận của thị trường.

---

## 5. Cross-References

Dùng `core-research-protocol.md` để xác định trình tự deep-dive và điểm dừng trước valuation. Dùng `core-meta-cognition.md` để tự phản biện thesis, kiểm tra bias, và xác định điều kiện đổi ý. Khi phân tích cần framework chuyên biệt, gọi module `framework-*`, hiện có `framework-dickinson-mauboussin.md`, để neo luận điểm vào cơ chế đã được mã hóa thay vì narrative tự do.
