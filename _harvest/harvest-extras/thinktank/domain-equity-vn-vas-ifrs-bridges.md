---
title: "Domain Equity VN VAS-IFRS Bridges — VAS vs IFRS Reconciliation, Accounting Standard Gaps, Vietnam Listed Equity Financial Statement Adjustment"
module_type: "domain"
file_name: "domain-equity-vn-vas-ifrs-bridges.md"
purpose: "Bridge Vietnamese Accounting Standards (VAS) to IFRS for equity analysis of Vietnamese listed companies. Maps reconciliation items, quantifies distortion magnitudes, flags VAS-only report risks, and tracks IFRS adoption timeline 2025-2030."
primary_triggers:
  - "VAS"
  - "IFRS"
  - "chênh lệch chuẩn mực"
  - "accounting standard reconciliation"
  - "VAS IFRS bridge"
  - "điều chỉnh BCTC VAS sang IFRS"
  - "so sánh VAS và IFRS"
  - "IFRS adoption Vietnam"
  - "lộ trình IFRS Việt Nam"
  - "BCTC song song VAS IFRS"
  - "revenue recognition VAS vs IFRS 15"
  - "expected credit loss VN banks"
  - "IFRS 16 lease Vietnam"
  - "goodwill impairment VAS"
when_to_use:
  - "When comparing Vietnamese companies to regional or global peers that report under IFRS."
  - "When adjusting VAS financials for DCF, multiples, or credit analysis."
  - "When analyzing banks, real estate, airlines, retailers, or any lease-heavy sector in Vietnam."
  - "When screening for hidden liabilities, asset undervaluation, or earnings-quality distortions caused by standard gaps."
when_not_to_use:
  - "Do not use as a standalone valuation module; pair with domain-equity-vn-valuation-advanced.md."
  - "Do not use for forensic detection alone; pair with domain-equity-vn-forensic-accounting.md."
  - "Do not replace auditor IFRS conversion work; this is an analytical bridge, not an audit opinion."
related_modules:
  - "domain-equity-vn-forensic-accounting.md"
  - "domain-equity-vn-valuation-advanced.md"
  - "domain-equity-vn-industry-guides.md"
  - "workflow-deep-dive.md"
  - "core-evidence-ladder.md"
authoritative_citations:
  - "MoF Circular 01/2020/TT-BTC — Vietnam IFRS adoption roadmap."
  - "VAS — Vietnamese Accounting Standards, Ministry of Finance."
  - "IFRS — International Financial Reporting Standards, IASB."
  - "Penman, S. Financial Statement Analysis and Security Valuation."
output_owner: "VAS/IFRS reconciliation lens only; workflow-deep-dive.md owns full company deep-dive format."
---

# Domain Equity VN VAS-IFRS Bridges — Điều chỉnh chuẩn mực VAS → IFRS / VAS IFRS Reconciliation

Purpose: Map từng khoản mục BCTC từ VAS sang IFRS, đo lường độ méo, và cung cấp checklist điều chỉnh khi phân tích doanh nghiệp niêm yết Việt Nam. Dùng khi so sánh cross-border, định giá, hoặc đánh giá chất lượng BCTC.

Trigger keywords: VAS, IFRS, chênh lệch chuẩn mực, accounting standard reconciliation, VAS IFRS bridge, điều chỉnh BCTC, IFRS adoption Vietnam, lộ trình IFRS, revenue recognition, goodwill impairment, ECL, IFRS 16, CTA, deferred tax, BCTC song song.

Use when: so sánh DN VN với peer quốc tế; điều chỉnh số liệu VAS trước khi chạy DCF/multiples; phân tích ngân hàng, BĐS, hàng không, bán lẻ. Do not use when: cần kết luận forensic chi tiết (dùng domain-equity-vn-forensic-accounting.md) hoặc valuation standalone (dùng domain-equity-vn-valuation-advanced.md).

---

## 1. Tổng quan VAS vs IFRS

**VAS** (Vietnamese Accounting Standards) do Bộ Tài chính ban hành, hiện là chuẩn mực bắt buộc cho hầu hết doanh nghiệp Việt Nam. **IFRS** (International Financial Reporting Standards) do IASB ban hành, áp dụng tại 140+ quốc gia.

Phần lớn DN niêm yết HOSE/HNX vẫn lập BCTC theo VAS. Một số tập đoàn lớn và ngân hàng đã công bố BCTC IFRS song song. Chênh lệch giữa hai chuẩn mực tạo độ méo đáng kể trong ROA, ROE, D/E, P/B, EBITDA, và lợi nhuận — đặc biệt ở ngành bất động sản, ngân hàng, bán lẻ, và hàng không.

**Lộ trình áp dụng IFRS:** Theo Thông tư 01/2020/TT-BTC:
- **2025:** Ngân hàng thương mại nhà nước và một số TMCP lớn chạy pilot IFRS.
- **2028:** Tất cả doanh nghiệp niêm yết trên HOSE/HNX bắt buộc chuyển sang IFRS.
- **2030:** Toàn bộ doanh nghiệp có quy mô lớn và DNNN phải áp dụng IFRS.

Giai đoạn 2026-2027 là "preparation window": DN cần xây dựng hệ thống dữ liệu, đào tạo kế toán, và chạy song song để đảm bảo số liệu so sánh khi chính thức chuyển đổi.

---

## 2. Bảng cầu nối VAS → IFRS — Key Reconciliation Areas

### 2.1 Revenue Recognition / Ghi nhận doanh thu

| Tiêu chí | VAS | IFRS (IFRS 15) |
|---|---|---|
| Nguyên tắc | Chuyển rủi ro và lợi ích | Chuyển quyền kiểm soát — 5-step model |
| Hợp đồng đa thành phần | Hướng dẫn hạn chế | Tách riêng từng performance obligation |
| BĐS bán trước | Ghi nhận sớm hơn (bàn giao pháp lý) | Chậm hơn (control transfer) |

**Điều chỉnh:** Doanh thu BĐS theo VAS thường "đẹp hơn" thực tế. Cần đọc thuyết minh chính sách DT, đối chiếu tiến độ thực tế dự án, và tính lại revenue theo percentage-of-completion hoặc control transfer nếu có dữ liệu.

### 2.2 Inventory / Hàng tồn kho

| Tiêu chí | VAS (VAS 07) | IFRS (IAS 2) |
|---|---|---|
| Phương pháp | FIFO hoặc weighted average | FIFO hoặc weighted average |
| LIFO | Không phổ biến | **Cấm hoàn toàn** |
| Đánh giá cuối kỳ | Giá gốc hoặc NRV — thấp hơn | Tương tự, hướng dẫn NRV chi tiết hơn |

**Điều chỉnh:** Hai chuẩn gần như tương đồng. Rủi ro chính là trì hoãn ghi nhận dự phòng giảm giá hoặc thay đổi phương pháp tính giá để làm mượt lợi nhuận.

### 2.3 PP&E / Tài sản cố định hữu hình

| Tiêu chí | VAS | IFRS (IAS 16) |
|---|---|---|
| Mô hình | **Chỉ giá gốc trừ khấu hao** | Giá gốc **hoặc revaluation model** |
| Đánh giá lại đất đai | Không cho phép | Cho phép; chênh lệch ghi vào OCI |

**Điều chỉnh:** DN VN có đất đai mua từ lâu thường ghi giá trị sổ sách thấp hơn thị trường nhiều lần → ROA, ROE bị "đẹp hóa" và P/B thô méo. Dùng NAV điều chỉnh thay vì book value VAS.

### 2.4 Investment Property / Bất động sản đầu tư

| Tiêu chí | VAS | IFRS (IAS 40) |
|---|---|---|
| Mô hình | Giá gốc trừ khấu hao | **Cost model hoặc fair value model** |
| Fair value changes | Không ghi nhận | Ghi vào P&L (fair value model) |

**Điều chỉnh:** VAS không phản ánh giá trị thị trường BĐS đầu tư. P/B và ROE bị méo nếu DN nắm giữ nhiều BĐS cho thuê.

### 2.5 Intangibles + Goodwill / Tài sản vô hình và Lợi thế thương mại

| Tiêu chí | VAS | IFRS (IFRS 3 / IAS 36) |
|---|---|---|
| Goodwill | **Khấu hao đều tối đa 10 năm** | **Không khấu hao**; annual impairment test |
| Intangibles không xác định đờị hữu ích | Không có khái niệm rõ ràng | Không khấu hao; impairment test hàng năm |

**Điều chỉnh:** VAS làm EBIT giảm nhẹ đều đặn. IFRS giữ EBIT cao hơn nhưng rủi ro impairment đột ngột lớn. Khi so sánh cross-border, điều chỉnh goodwill amortization VAS về 0 để so sánh EBIT apple-to-apple.

### 2.6 Financial Instruments / Công cụ tài chính

| Tiêu chí | VAS | IFRS (IFRS 9) |
|---|---|---|
| Phân loại | Đơn giản: cho vay, HTM, AFS, FVTPL | Phức tạp: business model + SPPI test |
| Đo lường fair value | Hạn chế hơn | Rộng rãi hơn |
| Dự phòng tổn thất | **Incurred loss** | **Expected Credit Loss (ECL)** |

**Điều chỉnh (quan trọng với ngân hàng):** VAS trích lập khi nợ đã xấu. IFRS 9 yêu cầu ECL từ nhóm 1. Khi VN chuyển sang IFRS 9, ngân hàng có thể phải trích lập thêm 30-80% → giảm LNST và vốn CSH đột ngột.

### 2.7 Leases / Thuê tài sản

| Tiêu chí | VAS (VAS 06) | IFRS (IFRS 16) |
|---|---|---|
| Operating lease | **Không ghi nhận trên bảng cân đối** | **ROU asset + lease liability** |
| Ảnh hưởng BCĐKT | Tài sản thấp, nợ thấp | Tài sản cao, nợ cao |
| Ảnh hưởng KQKD | Chi phí thuê trong SG&A | Khấu hao + lãi lease |
| EBITDA | Thấp hơn thực tế | Cao hơn (chi phí thuê chuyển xuống dưới EBITDA) |

**Điều chỉnh:** DN bán lẻ, hàng không, logistics theo VAS có D/E thấp hơn thực tế. Khi chuyển IFRS 16, D/E tăng, EBITDA tăng, net income giảm nhẹ do front-loading lãi. Cần cộng nợ thuê ước tính từ cam kết thuê vào EV.

### 2.8 Consolidation Scope / Phạm vi hợp nhất

| Tiêu chí | VAS | IFRS (IFRS 10) |
|---|---|---|
| Định nghĩa kiểm soát | Quyền biểu quyết > 50% hoặc thống nhất ý chí | **Quyền, biến động returns, khả năng sử dụng quyền** |
| SPV / VIE | Hướng dẫn hạn chế | Consolidation theo control thực chất |

**Điều chỉnh:** Tập đoàn VN thường dùng SPV, công ty con gián tiếp để nắm quỹ đất. VAS có thể không hợp nhất nếu sở hữu trực tiếp thấp, trong khi IFRS 10 bắt buộc consolidation dựa trên control thực chất.

### 2.9 FX Translation / Chênh lệch tỷ giá

| Tiêu chí | VAS | IFRS (IAS 21) |
|---|---|---|
| Chênh lệch hợp nhất CTC nước ngoài | Ghi vào chi phí tài chính hoặc riêng trong vốn CSH | **CTA ghi vào OCI**, tích lũy riêng |
| Chuyển nhượng CTC nước ngoài | Có thể ghi vào P&L | **Recycle từ OCI sang P&L** |

**Điều chỉnh:** VAS không phân biệt rõ CTA. DN có hoạt động ở Lào, Campuchia, Myanmar có thể trộn lẫn chênh lệch tỷ giá với retained earnings. Cần tách riêng để đánh giá operating performance đúng.

### 2.10 Deferred Tax / Thuế thu nhập hoãn lại

| Tiêu chí | VAS (VAS 17) | IFRS (IAS 12) |
|---|---|---|
| Nhận diện DTA/DTL | Theo khung thuế VN | Rộng hơn: tất cả temporary differences |
| Phân loại | Đôi khi mơ hồ ngắn/dài hạn | Phân loại rõ theo recovery timing |

**Điều chỉnh:** VAS tuân thủ khung thuế VN nên deferred tax ít hơn IFRS. Phân loại mơ hồ có thể méo current ratio và D/E.

### 2.11 Employee Benefits / Lợi ích ngưởị lao động

| Tiêu chí | VAS | IFRS (IAS 19) |
|---|---|---|
| Trợ cấp thôi việc (severance) | Trích lập theo Luật Lao động; không actuarial đầy đủ | **Actuarial valuation** cho DBO |
| Remeasurements | Không có khái niệm rõ ràng | Ghi vào OCI, không recycle |

**Điều chỉnh:** DN nhiều lao động lâu năm (sản xuất, khai khoáng, viễn thông) có thể có nghĩa vụ trợ cấp lớn nhưng không đo lường actuarial theo VAS. IFRS yêu cầu present value DBO discounted bằng corporate bond yield → có thể tăng nợ và giảm vốn CSH.

---

## 3. Red Flags khi đọc BCTC VAS-only

| Red Flag | Vì sao nguy hiểm | Cách điều chỉnh |
|---|---|---|
| **Goodwill không kiểm tra impairment** | VAS khấu hao đều 10 năm → che giấu rủi ro M&A đắt; recoverable amount có thể thấp hơn carrying amount | Tự ước tính impairment: so sánh carrying amount với fair value hoặc value in use của cash-generating unit |
| **Doanh thu bên liên quan ẩn trong "thu nhập khác"** | Phân loại mơ hồ; lợi nhuận RPT không bền vững, giá non-arm's length | Phân rã thu nhập khác; kiểm tra chi tiết RPT; so sánh giá giao dịch với thị trường |
| **Revaluation surplus trong vốn CSH** | VAS hạn chế revaluation; nếu có thường do tái cơ cấu; cơ sở đánh giá có thể không độc lập | Đọc thuyết minh; xác minh đơn vị thẩm định độc lập |
| **CTA trộn lẫn với retained earnings** | Không tách CTA riêng → méo biên ròng | Phân tích riêng ảnh hưởng tỷ giá; dùng EBIT nguyên thủy nếu có segment data |
| **Deferred tax phân loại sai** | DTA/DTL ngắn/dài hạn không rõ → méo thanh khoản và đòn bẩy | Kiểm tra thuyết minh; tự phân loại lại theo recovery timing |
| **Thuê hoạt động lớn nhưng off-balance-sheet** | D/E thấp hơn thực tế; nợ tiềm tàng lớn | Cộng PV(cam kết thuê) vào EV và nợ |
| **Dự phòng tín dụng ngân hàng thấp bất thường** | Incurred loss vs ECL → nợ nhóm 2 chưa được trích lập đầy đủ | Theo dõi nợ nhóm 2/tổng dư nợ; ước tính ECL đơn giản từ LGD và PD ngành |

---

## 4. Lộ trình áp dụng IFRS tại Việt Nam (2026 cập nhật)

| Giai đoạn | Đối tượng | Năm áp dụng |
|---|---|---|
| Pilot ngân hàng | VCB, VietinBank, BIDV và một số TMCP lớn | **2025** |
| Tất cả ngân hàng TMCP niêm yết | NH quy mô lớn HOSE/HNX | **2026-2027** |
| Doanh nghiệp niêm yết (listed equity) | Tất cả công ty HOSE, HNX, UPCOM | **2028 (bắt buộc)** |
| DNNN & DN quy mô lớn | Tập đoàn, tổng công ty nhà nước | **2028-2029** |
| Toàn bộ DN lớn | Theo tiêu chí MoF | **2030** |

**Rủi ro lộ trình:** Chậm trễ do thiếu nhân lực IFRS, hệ thống IT chưa sẵn sàng, và khác biệt pháp lý giữa Luật Kế toán VN với IFRS. Các ngân hàng pilot 2025 có thể gặp "capital shock" khi ECL tăng đột biến.

---

## 5. Doanh nghiệp đã dual-report VAS + IFRS (early adopters)

Một số DN và ngân hàng lớn đã công bố BCTC IFRS song song hoặc chuyển hoàn toàn:

1. **VCB** (Vietcombank) — Pilot IFRS đầu tiên, song song từ 2024-2025.
2. **VIC** (Vingroup) — IFRS cho công ty mẹ và hợp nhất trong annual report.
3. **VHM** (VinHomes) — Thuyết minh điều chỉnh IFRS trong annual report.
4. **FPT** — Song song IFRS cho hoạt động toàn cầu.
5. **HPG** (Hòa Phát) — So sánh VAS/IFRS cho một số khoản mục trọng yếu.
6. **GAS** (PV Gas) — Chuẩn bị IFRS theo lộ trình DNNN.
7. **VNM** (Vinamilk) — IFRS cho công ty con nước ngoài.
8. **MWG** (Thế Giới Di Động) — IFRS 16 lease adjustments trong annual report.
9. **PNJ** (Phú Nhuận Jewelry) — Công bố thông tin điều chỉnh IFRS.
10. **GMD** (Gemadept) — Segment reporting gần IFRS format.
11. **VJC** (Vietjet) — Disclosure chi tiết cam kết thuê; chịu ảnh hưởng lớn IFRS 16.
12. **SSI** (SSI Securities) — Báo cáo theo IFRS cho hoạt động tài chính.
13. **VPB** (VPBank) — Chuẩn bị pilot IFRS 9.
14. **TCB** (Techcombank) — Công bố roadmap chuyển đổi IFRS.
15. **ACB** (Asia Commercial Bank) — Roadmap IFRS rõ ràng.

**Nguyên tắc:** Ưu tiên IFRS cho cross-border comparison. Với trend analysis nội bộ, dùng VAS + điều chỉnh thủ công nếu time series IFRS chưa đủ dài.

---

## 6. Tóm tắt ảnh hưởng lên chỉ số

| Khoản mục | VAS so với IFRS | Ảnh hưởng chỉ số |
|---|---|---|
| Tài sản (đất đai cũ, BĐS đầu tư) | Thấp hơn | ROA cao hơn, P/B thô sai lệch → dùng NAV adjusted |
| Nợ (operating lease) | Thấp hơn | D/E thấp hơn thực tế; cộng nợ thuê vào EV |
| Doanh thu BĐS bán trước | Có thể sớm hơn | DT/LN "đẹp hơn"; kiểm tra control transfer |
| Dự phòng tín dụng (NH) | Thấp hơn (incurred loss) | LNST cao hơn, rủi ro ẩn; theo dõi nợ nhóm 2 |
| Goodwill | Khấu hao đều 10 năm | EBIT ổn định hơn, không phản ánh impairment thực |
| EBITDA (lease-heavy) | Thấp hơn (chi phí thuê trong SG&A) | IFRS 16 làm EBITDA cao hơn; EV/EBITDA không so sánh trực tiếp VAS-IFRS |

---

## Cross-Reference Block / Khối tham chiếu chéo

**Module liên quan trực tiếp:**
- `domain-equity-vn-forensic-accounting.md` — Cờ đỏ VAS-specific, Beneish M-score điều chỉnh VAS noise, mẫu thao túng kế toán VN.
- `domain-equity-vn-valuation-advanced.md` — Reverse DCF, SOTP, NAV adjusted; yêu cầu điều chỉnh VAS → IFRS trước khi định lượng.
- `domain-equity-vn-industry-guides.md` — Điều chỉnh đặc thù ngành (NH: ECL, nợ nhóm 2; BĐS: vốn hóa lãi vay và revenue recognition; logistics: lease và concession).
- `workflow-deep-dive.md` — Định dạng output khi tích hợp VAS/IFRS bridge vào memo phân tích sâu.
- `core-evidence-ladder.md` — Mức độ bằng chứng cho mỗi điều chỉnh chuẩn mực.

**Mối quan hệ:**
- VAS/IFRS bridge + `domain-equity-vn-forensic-accounting.md` = phát hiện méo từ chuẩn mực và thao túng.
- VAS/IFRS bridge + `domain-equity-vn-valuation-advanced.md` = đầu vào sạch cho DCF, SOTP, và multiples.
- VAS/IFRS bridge + `domain-equity-vn-industry-guides.md` = điều chỉnh ngành chính xác.

---

> **END OF MODULE** — domain-equity-vn-vas-ifrs-bridges.md
>
> Last updated: 2026-04-19 | Wave 4 Lane 10 | Ported from FinMentor 70 | OPVIA Sigma format
