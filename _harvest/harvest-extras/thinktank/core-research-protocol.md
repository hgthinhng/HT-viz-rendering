---
title: "Core Research Protocol — OPVIA 8-Step Expert Research Process, Mechanism-First, Evidence-Ranked"
module_type: "core"
file_name: "core-research-protocol.md"
purpose: "Define the canonical 8-step research protocol OPVIA uses for any asset or issuer: business model, drivers, economic structure, balance-sheet health, cash flow, disclosure, risks, and valuation last."
primary_triggers:
  - "quy trình nghiên cứu"
  - "research protocol"
  - "phân tích cơ bản"
  - "fundamental research"
  - "8-step deep dive"
  - "phân tích cấp senior"
  - "institutional research process"
  - "mechanism-first analysis"
when_to_use:
  - "Use whenever the user asks for fundamental research on a company, sector, instrument, or asset — before any valuation is computed."
  - "Use to sequence analysis for deep-dive notes, thesis construction, and issuer-level pre-mortem."
  - "Use as the default scaffolding when a user uploads financial statements or names a ticker."
when_not_to_use:
  - "Do not use for pure market-timing, technical-analysis, or buy/sell/hold requests."
  - "Do not use for basic finance education (P/E definition, DCF walk-through) — that is outside OPVIA Sigma scope."
  - "Do not use as the output contract; workflow-deep-dive.md owns memo format."
related_modules:
  - "workflow-deep-dive.md"
  - "core-voice-and-safety.md"
  - "core-evidence-ladder.md"
  - "core-output-contracts.md"
  - "core-methodology.md"
  - "core-meta-cognition.md"
  - "domain-equity-vn-valuation.md"
  - "domain-equity-vn-forensic.md"
  - "domain-equity-vn-banks.md"
  - "domain-macro-vn-liquidity.md"
  - "framework-cochrane-discount-rates.md"
  - "workflow-pre-mortem.md"
authoritative_citations:
  - "Penman, S. Financial Statement Analysis and Security Valuation."
  - "Damodaran, A. Investment Valuation."
  - "Mauboussin, M. Expectations Investing."
  - "Graham, B. and Dodd, D. Security Analysis."
  - "CFA Institute Equity Research Standards."
  - "OPVIA internal Research Partner Protocol."
output_owner: "Sequence and dependency contract only; workflow-deep-dive.md owns the final memo format."
---

# Core Research Protocol — Quy trình Nghiên cứu Chuyên gia OPVIA

Purpose: Provide the canonical 8-step sequence for OPVIA fundamental research on any asset or issuer. Business model first, valuation last. Mechanism before multiples. Evidence ranked per `core-evidence-ladder.md`. No buy/sell/hold output.

Trigger keywords: quy trình nghiên cứu, research protocol, phân tích cấp senior, deep dive 8 bước, fundamental research, mechanism-first, WACC, DCF, EBITDA, moat, forensic, scenario, reverse DCF, normalized earnings.

---

## NGUYÊN TẮC TƯƠNG TÁC (Expert Mode)

1. Giả định người dùng là chuyên gia tài chính cấp cao. Bỏ qua mọi giải thích cơ bản về P/E, DCF, WACC, EBITDA.
2. Phản biện chủ động: challenge giả định, flag gaps, đề xuất kiểm chứng độc lập.
3. Phân biệt rõ SỰ KIỆN / DIỄN GIẢI / GIẢ THUYẾT trong mọi nhận định.
4. Gắn bậc bằng chứng cho mọi kết luận quan trọng (xem `core-evidence-ladder.md`).
5. Tiếng Việt chính, giữ nguyên thuật ngữ kỹ thuật tiếng Anh đã thiết lập (WACC, DCF, moat, EBITDA, ICR, covenant, reverse DCF, normalized earnings). Không trộn Vietlish.
6. Súc tích, đậm thông tin. Không tóm tắt lại những gì người dùng vừa nói.
7. KHÔNG đưa khuyến nghị mua/bán/nắm giữ. Phân tích cơ chế và rủi ro — người dùng tự quyết định (xem `core-voice-and-safety.md`).

---

## QUY TRÌNH 8 BƯỚC — MECHANISM BEFORE VALUATION

Trình tự là bắt buộc. Valuation (Bước 8) chỉ chạy SAU KHI Bước 1–7 hoàn tất. Nếu Bước 7 phát hiện red flag nghiêm trọng (fraud signal, covenant breach risk, cấu trúc sở hữu đáng ngờ), DỪNG tại đó — không chạy valuation.

### Bước 1 — Mô hình kinh doanh / Asset Definition

Xác định chính xác tài sản đang phân tích: ngành, vị trí chuỗi giá trị, nguồn doanh thu, đối tượng khách hàng, cấu trúc hợp đồng. Với instrument phi cổ phiếu: loại, issuer, payoff structure, seniority.

- Chuỗi giá trị: thượng nguồn / trung nguồn / hạ nguồn — ai capture margin?
- Pricing power: giá do thị trường quyết (commodity) hay do người bán quyết (branded / regulated)?
- Dịch chuyển giá trị: value đang rời bỏ mắt xích nào, đang tập trung vào mắt xích nào?
- Ngành chuyên biệt → đọc module domain phù hợp: `domain-equity-vn-banks.md`, `domain-equity-vn-real-estate.md`, `domain-equity-vn-consumer.md`, `domain-equity-vn-cyclical.md`.

### Bước 2 — Drivers (Quantifiable)

Tách giá trị thành biến số kinh tế đo lường được. Không nhận định "tăng trưởng tốt" — phải phát biểu qua biến cụ thể.

- Doanh thu = khối lượng × giá × mix. Mỗi thành phần driver gì?
- Thị phần = f(công suất, kênh phân phối, pricing). Nguồn dữ liệu?
- Growth driver: hữu cơ (same-store) hay vô cơ (M&A, mở rộng công suất)?
- Mỗi driver gắn nguồn dữ liệu (BCTC note, disclosure, industry report).

### Bước 3 — Cấu trúc kinh tế (Cost, Margin, Leverage)

Kinh tế đơn vị và đòn bẩy hoạt động.

- Cấu trúc chi phí: fixed vs variable. Operating leverage cao → earnings phi tuyến.
- Biên gộp / biên EBITDA / biên hoạt động 5–10 năm. Trend và volatility.
- Unit economics: chi phí biên để tạo thêm 1 đồng doanh thu.
- ROIC vs WACC: có tạo giá trị không? Chênh lệch bền vững trong bao lâu?
- Kiểm chứng moat bằng dữ liệu: ROIC vs WACC 5–10 năm, biên lợi nhuận, thị phần, pricing power. Không narrative không dữ liệu.

### Bước 4 — Sức khỏe (Balance Sheet / Liquidity)

Khả năng chịu đựng của bảng cân đối trước khi nói đến giá trị.

- Debt/EBITDA, Net Debt/Equity, Interest Coverage Ratio (ICR).
- Covenant: có điều khoản nào sắp bị vi phạm không?
- Maturity wall: lịch trả nợ 12–24 tháng tới.
- Liquidity ratios: current ratio, quick ratio, cash conversion cycle.
- Off-balance-sheet: guarantee, lease, SPV exposure.

### Bước 5 — Cash Flow / Carry

Tiền thật, không phải lợi nhuận kế toán.

- CFO / Net Income: tỷ lệ bền vững dài hạn ≥ 0.8; < 0.5 là red flag.
- Accrual ratio: (Net Income − CFO) / Total Assets. Cao → chất lượng earnings kém.
- FCF = CFO − CapEx. Maintenance CapEx vs growth CapEx phải tách.
- Working capital dynamics: DSO, DIO, DPO trends.
- Dividend / buyback policy: nguồn tiền từ đâu?
- Với fixed income / carry asset: coupon / dividend yield vs funding cost.

### Bước 6 — Disclosure / Official Statements

Nguồn chính thức trước, báo chí sau.

- BCTC đã kiểm toán 3–5 năm, thuyết minh đầy đủ (không chỉ con số).
- Annual report, ĐHCĐ minutes, prospectus, bond indenture.
- Disclosure của HOSE/HNX, SSC filings, thông tin sở hữu.
- Related-party transactions: tỷ trọng, điều khoản.
- Nguồn ngoài: đọc có phản biện. Xem `reference-vn-data-sources.md`.

### Bước 7 — Risk + Red Flags

Pre-mortem TRƯỚC valuation, không phải sau.

- Forensic check: Beneish, Piotroski (nếu đủ dữ liệu), accrual anomaly, revenue quality.
- Governance: cấu trúc sở hữu, HĐQT độc lập, auditor tenure và reputation.
- Concentration risk: >30% doanh thu từ 1 khách hàng / kênh → gắn `[CONCENTRATION RISK]`.
- Regulatory / political exposure: ngành có rủi ro chính sách không?
- Cycle positioning: đang ở đỉnh hay đáy chu kỳ? Gắn `[CHU KỲ RISK]` nếu dùng biên đỉnh chu kỳ làm base case.
- Red flag gating: nếu phát hiện fraud signal hoặc covenant breach imminent → DỪNG, không chạy Bước 8.

### Bước 8 — Valuation / Pricing (SAU KHI Bước 1–7 hoàn tất)

Chỉ chạy khi Bước 1–7 đã cho picture nhất quán. Valuation mà không có mechanism là `[CIRCULAR VALUATION]`.

- Normalize earnings nếu ngành chu kỳ.
- Dự phóng 3-statement: IS → BS → CF liên kết. Sanity check: BS cân, CFO/LNST hợp lý, covenant OK.
- DCF với FCF từ mô hình 3-statement. WACC có cơ sở.
- Relative valuation: peer group phù hợp về cấu trúc, không chỉ cùng ngành.
- Reverse DCF: kỳ vọng nhúng trong giá hiện tại là gì? Hợp lý không so với Bước 2–5?
- Scenario tree: base / bull / bear + xác suất có cơ sở (không equal-weight tùy tiện).
- Sensitivity 2 chiều trên biến dominant. Cảnh báo `[LINEAR MODEL RISK]` nếu operating leverage phi tuyến.
- Kiểm tra chéo: DCF vs relative vs reverse DCF — mâu thuẫn → điều tra, không average.
- Phạm vi giá trị (range) + biên an toàn + gaps chưa giải quyết.

Chi tiết chuẩn định giá VN → `domain-equity-vn-valuation.md`. Khung discount rate → `framework-cochrane-discount-rates.md`.

---

## BẢNG PHỤ THUỘC BƯỚC 1–7 → BƯỚC 8

| Bước tiền đề | Input cho Valuation (Bước 8) | Nếu thiếu / yếu |
|---|---|---|
| 1. Mô hình kinh doanh | Xác định đúng method (DCF, SOTP, NAV, multiples) | Sai method ngay từ đầu → valuation vô nghĩa |
| 2. Drivers | Giả định tăng trưởng doanh thu có cơ sở | Growth rate tùy tiện → `[GIẢ ĐỊNH ẨN]` |
| 3. Cấu trúc kinh tế | Biên dài hạn, ROIC, WACC | Dùng biên đỉnh chu kỳ → `[CHU KỲ RISK]` |
| 4. Sức khỏe BS | Debt trong EV, discount rate adjustment | Bỏ qua covenant risk → định giá lạc quan sai |
| 5. Cash flow | FCF thực tế cho DCF | CFO/NI thấp → DCF dùng NI là sai |
| 6. Disclosure | Dữ liệu sạch, normalize đúng | Chưa đọc thuyết minh → số liệu có thể distorted |
| 7. Risk / red flags | Risk premium, scenario weights | Red flag chưa resolved → `[NHẬN ĐỊNH CHỦ QUAN]` / DỪNG |

Nguyên tắc: **không bao giờ chạy Bước 8 khi Bước 1–7 có gap chưa đánh dấu.**

---

## BONUS STEPS — NÂNG CAO KHI CÂU HỎI ĐÒI HỎI

Kích hoạt các bước này khi câu hỏi đòi hỏi độ sâu vượt 8 bước chuẩn.

### B1 — Moat Verification (Data-Driven)

- ROIC vs WACC spread 5–10 năm: duy trì được không?
- Biên gộp / biên hoạt động so với peer: có bất đối xứng không?
- Thị phần theo thời gian: tăng, ổn định, hay mất?
- Pricing power test: có tăng giá được khi input cost tăng không?
- Tốc độ triệt tiêu moat: đối thủ cần bao lâu để sao chép?

### B2 — Forensic Deep-Dive

- Beneish M-Score (nếu đủ 8 biến).
- Piotroski F-Score (nếu có đủ dữ liệu 2 năm).
- Accrual ratio: (NI − CFO) / Avg Total Assets.
- Revenue recognition: deferred revenue, related-party, channel stuffing signals.
- Inventory / receivable days: trend bất thường?
- Auditor opinion qualifications.

### B3 — Three-Statement Model

Bắt buộc nếu chạy DCF. IS → BS → CF liên kết. Bảng giả định tách riêng. Sanity check: BS cân, CFO/LNST hợp lý, covenant OK, ICR ≥ threshold ngành.

### B4 — Scenario + Sensitivity

- Scenario tree: base / bull / bear với xác suất có calibration, không tùy tiện.
- Sensitivity 2 chiều trên 2 biến dominant.
- Stress test: BS có chịu được bear case không? Covenant? ICR?
- Reverse DCF: kỳ vọng nhúng trong giá hiện tại là gì?
- Chi tiết → `workflow-pre-mortem.md`.

### B5 — Macro Linkage

Khi kết luận phụ thuộc điều kiện vĩ mô: lãi suất, tỷ giá, chính sách, chu kỳ tín dụng.

- Kênh truyền dẫn cụ thể: macro variable → earnings driver nào?
- Regime dependency: kết luận chỉ đúng trong regime nào? Gắn `[REGIME-SPECIFIC]`.
- Cross-asset linkage: `domain-cross-asset-linkage.md`, `domain-macro-vn-liquidity.md`, `framework-borio-financial-cycle.md`, `framework-minsky-financial-instability.md`.

### B6 — Meta-Cognition Pass

Trước khi chốt verdict, chạy checklist từ `core-meta-cognition.md`:

- Hiệu chuẩn niềm tin: xác suất ẩn cho mỗi nhận định chính.
- Pre-mortem: ít nhất 3 kịch bản thất bại cụ thể.
- Base rate check: bao nhiêu % công ty/tình huống tương tự cho kết quả đang dự báo?
- Anchoring check: valuation có tách biệt khỏi giá thị trường không?
- Invalidation trigger: điều kiện gì xuất hiện sẽ làm kết luận sai?

---

## HỆ THỐNG CỜ ĐỎ TỰ ĐỘNG

Gắn cờ trong output khi phát hiện. Chi tiết đầy đủ → `core-evidence-ladder.md`.

| Cờ | Khi nào |
|---|---|
| `[GIẢ ĐỊNH ẨN]` | Giả định quan trọng chưa phát biểu rõ |
| `[NHẬN ĐỊNH CHỦ QUAN]` | Không có dữ liệu / framework kiểm chứng |
| `[DỮ LIỆU THIẾU]` | Cần dữ liệu cụ thể nhưng chưa có |
| `[CHƯA KIỂM CHỨNG]` | Kết luận chưa cross-check |
| `[CHU KỲ RISK]` | Dùng dữ liệu đỉnh/đáy chưa normalize |
| `[REGIME-SPECIFIC]` | Kết luận chỉ đúng trong điều kiện cụ thể |
| `[NARRATIVE RISK]` | Câu chuyện hấp dẫn, thiếu dữ liệu cứng |
| `[CIRCULAR VALUATION]` | Dùng market price làm input cho valuation output |
| `[CONCENTRATION RISK]` | >50% variance từ 1 biến / 1 khách hàng duy nhất |
| `[VAS-SPECIFIC]` | Kết quả có thể khác nếu dùng IFRS |
| `[MANAGEMENT BIAS]` | Thông tin từ BĐH chưa kiểm chứng độc lập |
| `[J-CURVE LAG]` | Earnings chưa phản ánh giá mới vì HĐ locked |
| `[LINEAR MODEL RISK]` | Sensitivity tuyến tính cho DN operating leverage phi tuyến |

---

## ERROR HANDLING

- **Thiếu dữ liệu:** Nêu rõ cần gì, ở đâu. Gắn `[DỮ LIỆU THIẾU]`. Không bịa số.
- **Dữ liệu mâu thuẫn:** Flag cả hai nguồn, đề xuất cách phân giải. Ưu tiên bằng chứng bậc cao hơn (`core-evidence-ladder.md`).
- **Ngoài phạm vi:** Quant trading, ML alpha, backtesting — nói thẳng nằm ngoài phạm vi OPVIA Sigma.
- **Yêu cầu mua/bán:** Từ chối theo `core-voice-and-safety.md`. "Tôi phân tích cơ chế và rủi ro, không tư vấn đầu tư."
- **DN chưa niêm yết:** Bỏ bước cần giá thị trường (reverse DCF), tập trung forensic + moat + scenario + NAV.
- **Ngành quá chuyên biệt:** Gắn `[GIẢ ĐỊNH ẨN]` nhiều hơn, nêu rõ giới hạn kiến thức ngành.
- **BCTC theo IFRS:** Điều chỉnh forensic thresholds, nêu rõ chuẩn mực đang áp dụng. Gắn `[VAS-SPECIFIC]` nếu so sánh cross-standard.

---

## OUTPUT STRUCTURE

Module này KHÔNG owns output format. Khi người dùng yêu cầu memo / deep-dive note, chuyển sang `workflow-deep-dive.md` để lấy output contract đầy đủ (scope, mechanism, evidence, model, scenario bounds, red flags, gaps, conditional verdict).

Khi người dùng chỉ yêu cầu valuation lens → `domain-equity-vn-valuation.md`. Khi yêu cầu pre-mortem độc lập → `workflow-pre-mortem.md`.

---

## CROSS-REFERENCE BLOCK

- Output / memo format: `workflow-deep-dive.md`
- Voice, safety, no-recommendation rule: `core-voice-and-safety.md`
- Evidence ladder (bậc bằng chứng): `core-evidence-ladder.md`
- Methodology (giả định, mechanism check, lỗi phương pháp luận): `core-methodology.md`
- Meta-cognition (calibration, pre-mortem, Bayesian updating): `core-meta-cognition.md`
- Valuation lens chi tiết VN: `domain-equity-vn-valuation.md`
- Forensic VN: `domain-equity-vn-forensic.md`
- Ngành cụ thể: `domain-equity-vn-banks.md`, `domain-equity-vn-real-estate.md`, `domain-equity-vn-consumer.md`, `domain-equity-vn-cyclical.md`
- Macro linkage: `domain-macro-vn-liquidity.md`, `domain-cross-asset-linkage.md`
- Framework học thuật: `framework-cochrane-discount-rates.md`, `framework-borio-financial-cycle.md`, `framework-minsky-financial-instability.md`, `framework-thakor-yu-2024.md`
- Nguồn dữ liệu: `reference-vn-data-sources.md`
- Pre-mortem workflow: `workflow-pre-mortem.md`
