---
title: "Domain Equity VN Forensic Accounting — Beneish M-Score, Piotroski F-Score, Accrual Analysis, Red Flags, VAS/IFRS Reconciliation, Vietnam Listed Equity Quality"
module_type: "domain"
file_name: "domain-equity-vn-forensic-accounting.md"
purpose: "Merged forensic accounting framework and consolidated red-flag detector for Vietnamese listed equities. Applies Beneish, Piotroski, accrual analysis, working-capital pattern analysis, and VN-specific accounting manipulation patterns."
primary_triggers:
  - "forensic accounting Vietnam"
  - "Beneish M-score VN"
  - "Piotroski F-score"
  - "chất lượng lợi nhuận"
  - "cờ đỏ tài chính"
  - "red flags BCTC"
  - "accrual ratio"
  - "earnings quality"
  - "thao túng kế toán"
  - "VAS IFRS reconciliation"
  - "related party transactions VN"
  - "pledged shares"
  - "tunneling risk"
when_to_use:
  - "When analyzing financial-statement quality of any Vietnamese listed company."
  - "When screening for earnings manipulation, revenue recognition issues, or balance-sheet stress."
  - "When evaluating governance risk, ownership structure, or related-party exposure."
  - "When preparing the forensic lens of a deep-dive memo or pre-mortem."
when_not_to_use:
  - "Do not use as a standalone valuation module; pair with domain-equity-vn-valuation.md."
  - "Do not use to make buy/sell/hold recommendations; output is diagnostic, not advisory."
  - "Do not replace auditor work; this is an analytical screen, not an audit opinion."
related_modules:
  - "workflow-deep-dive.md"
  - "domain-equity-vn-valuation.md"
  - "domain-equity-vn-industry-guides.md"
  - "framework-regime-v11.md"
  - "core-evidence-ladder.md"
authoritative_citations:
  - "Beneish, M. D. 1999. The Detection of Earnings Manipulation."
  - "Piotroski, J. D. 2000. Value Investing: The Use of Historical Financial Statement Information."
  - "Penman, S. Financial Statement Analysis and Security Valuation."
  - "VAS — Vietnamese Accounting Standards, Ministry of Finance."
  - "IFRS — International Financial Reporting Standards, IASB."
output_owner: "Forensic-quality lens only; workflow-deep-dive.md owns full company deep-dive format and final output contract."
---

# Domain Equity VN Forensic Accounting — Forensic + Red Flags / Phân tích pháp lý kế toán & Cờ đỏ Việt Nam

Purpose: Apply OPVIA forensic discipline to Vietnamese listed equities. Screen for earnings manipulation, revenue-quality degradation, balance-sheet stress, governance red flags, and VAS-specific distortions. Output is diagnostic — severity-ranked flags with confidence levels.

Trigger keywords: forensic accounting, Beneish M-score, Piotroski F-score, accrual ratio, earnings quality, chất lượng lợi nhuận, cờ đỏ tài chính, red flags, thao túng kế toán, VAS IFRS, related party, pledged shares, tunneling, insider trading, working capital analysis, cash conversion cycle.

Use when: screening BCTC quality, building deep-dive red-flag sections, stress-testing governance, or evaluating pre-IPO / restructuring candidates. Do not use when: valuation alone (use domain-equity-vn-valuation.md) or trade timing.

---

## Section A: Forensic Scoring Models / Mô hình chấm điểm pháp lý

### A.1 Beneish M-Score

Mô hình 8 biến Beneish (1999) phát hiện xác suất thao túng lợi nhuận. **Ngưỡng: M-score > −1.78** → xác suất cao có manipulation.

| Biến | Ký hiệu | Công thức (đơn giản) | Ý nghĩa pháp lý |
|------|---------|---------------------|-----------------|
| Days Sales in Receivables Index | DSRI | DSO năm nay / DSO năm trước | Phải thu khách hàng tăng bất thường — có thể "dồn" doanh thu cuối kỳ |
| Gross Margin Index | GMI | Biên gộp năm trước / biên gộp năm nay | Biên gộp suy giảm → áp lực thao túng tăng |
| Asset Quality Index | AQI | (1 − Tài sản ngắn hạn − TSCĐ) / Tổng tài sản, năm nay vs năm trước | Chất lượng tài sản giảm — chi phí vốn hóa bất thường |
| Sales Growth Index | SGI | Doanh thu năm nay / Doanh thu năm trước | Tăng trưởng DT cao → áp lực thao túng tăng |
| Depreciation Index | DEPI | Tỷ lệ khấu hao năm trước / năm nay | Kéo dài đờị hữu ích tài sản → giảm chi phí khấu hao |
| SG&A Index | SGAI | (SG&A/DT) năm nay / (SG&A/DT) năm trước | Chi phí bán hàng & quản lý bất thường |
| Leverage Index | LVGI | (Tổng nợ/Tổng TS) năm nay / năm trước | Đòn bẩy tài chính tăng |
| Total Accruals to Total Assets | TATA | Total Accruals / Tổng tài sản bình quân | Dồn tích cao — lợi nhuận không có tiền mặt đi kèm |

**Công thức tổng hợp (đơn giản hóa):**
```
M = −4.84 + 0.92×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI
    + 0.115×DEPI − 0.172×SGAI − 0.327×LVGI + 4.679×TATA
```

**VN adaptation notes:** Cần ít nhất 2 năm dữ liệu BCTC liên tục. VAS tạo noise ở **goodwill amortization** (khấu hao đều 10 năm, không impairment test hàng năm như IFRS) → ảnh hưởng DEPI và AQI. **TSCĐ không đánh giá lại theo VAS** (giá gốc) → AQI có thể méo. Dùng M-score như **screening tool**, không phải bằng chứng kết luận.

### A.2 Piotroski F-Score

9 tiêu chí nhị phân (đạt = 1 điểm), tổng 0–9. Đánh giá sức khỏe tài chính, kết hợp với Beneish để lọc chất lượng.

**Nhóm Sinh lợi — Profitability (4 điểm):**
1. ROA dương → +1
2. CFO (Operating Cash Flow) dương → +1
3. ROA tăng so với năm trước → +1
4. CFO > Net Income (LNST) → +1 (chất lượng lợi nhuận)

**Nhóm Đòn bẩy / Thanh khoản — Leverage & Liquidity (3 điểm):**
5. Nợ dài hạn / Tổng tài sản giảm so với năm trước → +1
6. Current Ratio tăng so với năm trước → +1
7. Không phát hành thêm cổ phiếu trong kỳ → +1

**Nhóm Hiệu quả — Efficiency (2 điểm):**
8. Gross Margin tăng so với năm trước → +1
9. Asset Turnover tăng so với năm trước → +1

**Diễn giải:**
- F ≥ 8: Sức khỏe tài chính mạnh, chất lượng cao.
- F = 5–7: Trung bình — cần phân tích chi tiết hơn.
- F ≤ 4: Yếu — rủi ro cao, đặc biệt nếu kết hợp với M-score > −1.78.

**Sector applicability:** Ngân hàng/bảo hiểm/chứng khoán — F-score gốc không phù hợp; dùng ROE, NPL, LDR thay thế. BĐS — điều chỉnh tiêu chí (5) do vốn hóa lãi vay. Sản xuất, bán lẻ, logistics — áp dụng trực tiếp.

### A.3 Accrual Ratio & Earnings Quality / Tỷ lệ dồn tích

**3 tầng kiểm tra:**

**Tầng 1 — CFO / Net Income:** CFO/LNST > 0.8 liên tục → tốt; 0.5–0.8 → điều tra; < 0.5 hoặc CFO âm khi LNST dương → 🔴.

**Tầng 2 — Accrual analysis:**
```
Total Accruals = Net Income − CFO
Accrual Ratio  = Total Accruals / Tổng tài sản bình quân
```
- Accrual ratio > 10% → lợi nhuận từ dồn tích, không phải tiền thật.
- Xu hướng tăng → chất lượng xấu đi.

**Tầng 3 — Phân rã thành phần:** % doanh thu cốt lõi vs thu nhập khác; % lợi nhuận từ hoạt động kinh doanh vs tài chính vs một lần; % CFO từ hoạt động thực vs thay đổi vốn lưu động.

### A.4 Cash Conversion Cycle (CCC) & Working Capital Pattern / Chu kỳ chuyển đổi tiền mặt

```
CCC = DSO + DIO − DPO
DSO = (Phải thu KH bình quân / DT) × 365
DIO = (Tồn kho bình quân / COGS) × 365
DPO = (Phải trả NCC bình quân / COGS) × 365
```

**Pattern analysis:**
- **DSO tăng + DIO giảm:** Có thể "dồn" doanh thu cuối kỳ.
- **DSO giảm + DIO tăng:** Có thể tích hàng lỗi thờị — kiểm tra dự phòng giảm giá.
- **DPO tăng đột ngột:** Kéo dài công nợ NCC để cải thiện CFO tạm thờị.
- **CCC > ngành trung bình 30+ ngày:** Lỗ hổng vốn lưu động hoặc cấu trúc yếu.

---

## Section B: Red Flags Consolidated / Cờ đỏ tổng hợp

> Nguyên tắc: Cờ đỏ = dấu hiệu cảnh báo, **KHÔNG** nhất thiết là sai phạm. Mỗi cờ đỏ phải kèm (a) dấu hiệu, (b) ý nghĩa, (c) cần kiểm tra thêm gì.

### B.1 Revenue Recognition Red Flags / Cờ đỏ ghi nhận doanh thu

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 1 | Doanh thu tăng đột biến không có lý do rõ ràng | 🔴 Nghiêm trọng | Ghi nhận sớm, dồn DT, hoặc giao dịch ảo | Thuyết minh chính sách DT; đối chiếu CFO |
| 2 | DT tăng nhưng CFO giảm hoặc không tăng tương ứng | 🔴 Nghiêm trọng | DT "trên giấy" — chưa thu tiền thật | Phải thu khách hàng; thay đổi vốn lưu động |
| 3 | Doanh thu tăng chủ yếu từ RPT | ⚠️ Cần theo dõi | Giá không phản ánh thị trường (non-arm's length) | Chi tiết RPT trong thuyết minh; so sánh giá thị trường |
| 4 | Thu nhập khác / Tổng DT > 15% | ⚠️ Cần theo dõi | Lợi nhuận từ bán tài sản — không bền vững | Chi tiết thu nhập khác; loại khỏi normalized earnings |
| 5 | Doanh thu Q4 chiếm > 40% cả năm | ⚠️ Cần theo dõi | Dồn DT cuối kỳ để đạt target | So sánh QoQ, YoY; kiểm tra hợp đồng |
| 6 | Thay đổi chính sách ghi nhận DT vào thờị điểm nhạy cảm (trước IPO, vay nợ lớn) | 🔴 Nghiêm trọng | "Làm đẹp" con số | Tác động lên LNST; so sánh ngành |
| 7 | Backlog giảm nhưng DT tăng | ⚠️ Cần theo dõi | Có thể ghi nhận DT trước nghĩa vụ | Kiểm tra hợp đồng và milestone |
| 8 | Top 3 khách hàng > 50% doanh thu | ⚠️ Cần theo dõi | Concentration risk; khách hàng lớn có thể là RPT | Công bố khách hàng lớn; rà soát quan hệ |
| 9 | DT hợp đồng dài hạn ghi nhận % hoàn thành, tiến độ không rõ | 🟡 Lưu ý | Rủi ro ước tính tiến độ sai | Báo cáo tiến độ độc lập; so sánh chi phí thực tế |
| 10 | Giá bán tăng nhưng sản lượng giảm, tổng DT vẫn tăng | 🟡 Lưu ý | Có thể chuyển giá nội bộ hoặc sản phẩm ảo | Phân tích cơ cấu sản phẩm; giá vs thị trường |

### B.2 Margin Pattern Red Flags / Cờ đỏ biên lợi nhuận

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 11 | Gross Margin giảm liên tục 3+ quý trong khi đối thủ ổn định | ⚠️ Cần theo dõi | Mất pricing power hoặc chi phí đầu vào tăng | So sánh với đối thủ; giá nguyên liệu thế giới |
| 12 | SG&A tăng nhanh hơn DT (> 5% chênh lệch) | ⚠️ Cần theo dõi | Chi phí vận hành mất kiểm soát | Chi tiết SG&A; so sánh headcount |
| 13 | Biên gộp cao bất thường so với ngành (> 1.5 std dev) | 🟡 Lưu ý | Có thể tốt (moat) hoặc xấu (kế toán) | Cross-check đối thủ; logic ngành; kiểm tra COGS |
| 14 | Net Margin tăng trong khi biên gộp giảm | 🔴 Nghiêm trọng | "Make-up" qua tài chính, thu nhập khác, hoặc giảm dự phòng | Phân rã LNST theo nguồn; kiểm tra chi phí tài chính âm |
| 15 | COGS giảm đột ngột không có lý do nguyên liệu hoặc công nghệ | ⚠️ Cần theo dõi | Có thể thay đổi phương pháp tính giá tồn kho hoặc vốn hóa chi phí | Thuyết minh chính sách kế toán; FIFO vs weighted average |

### B.3 Balance Sheet Red Flags / Cờ đỏ bảng cân đối kế toán

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 16 | Goodwill / Tổng TS > 15% và tăng nhanh | ⚠️ Cần theo dõi | Mua lại đắt; rủi ro impairment cao (đặc biệt IFRS) | Lịch sử M&A; giá mua vs fair value |
| 17 | Phải thu tăng nhanh hơn doanh thu (DSO tăng) | 🔴 Nghiêm trọng | Khách hàng trả chậm hoặc "dồn" DT cuối kỳ | Tuổi nợ; dự phòng nợ khó đòi; cơ cấu phải thu |
| 18 | Dự phòng nợ khó đòi giảm trong khi phải thu tăng | 🔴 Nghiêm trọng | "Làm đẹp" lợi nhuận bằng cách giảm dự phòng | Dự phòng / phải thu qua các năm; so sánh ngành |
| 19 | Tồn kho tăng nhanh hơn COGS (DIO tăng) | ⚠️ Cần theo dõi | Bán chậm, tồn kho lỗi thờị, hoặc tích hàng | Cơ cấu tồn kho: thành phẩm vs NVL vs dở dang |
| 20 | Dự phòng giảm giá tồn kho giảm khi tồn kho tăng mạnh | 🔴 Nghiêm trọng | Trì hoãn ghi nhận tổn thất | Dự phòng / tồn kho qua các kỳ; so sánh ngành |
| 21 | D/E > 2 (phi tài chính) hoặc tăng mạnh 1 năm | ⚠️ Cần theo dõi | Đòn bẩy tăng — rủi ro tái cấp vốn | Kỳ hạn nợ; lãi suất; covenant |
| 22 | Interest Coverage < 1.5x | 🔴 Nghiêm trọng | Lợi nhuận gần không đủ trả lãi | Kỳ hạn nợ đáo hạn; tái cấp vốn |
| 23 | Current Ratio < 1 | 🔴 Nghiêm trọng | Thanh khoản yếu — nợ ngắn hạn > tài sản ngắn hạn | Khoản vay sắp đáo hạn; dự phòng tín dụng |
| 24 | Tài sản thiếu thanh khoản (dở dang, đất chưa có sổ) chiếm tỷ trọng lớn | ⚠️ Cần theo dõi | Giá trị sổ sách không phản ánh thanh khoản | Pháp lý tài sản; tiến độ dự án; định giá độc lập |

### B.4 Related-Party Transaction Red Flags / Cờ đỏ giao dịch bên liên quan (VN-specific)

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 25 | DT > 20% từ bên liên quan | 🔴 Nghiêm trọng | Giá không phản ánh thị trường | Sơ đồ quan hệ; so sánh giá giao dịch độc lập |
| 26 | Phải thu từ bên liên quan tăng đột biến | 🔴 Nghiêm trọng | Chuyển tiền cho bên liên quan (tunneling) | Chi tiết RPT; mục đích phải thu |
| 27 | Sở hữu chéo: A sở hữu B, B sở hữu C, C mua hàng A | 🔴 Nghiêm trọng | Dòng tiền vòng, che giấu hiệu suất thực | Vẽ sơ đồ sở hữu; giao dịch ngược chiều |
| 28 | Cho vay nội bộ lãi suất bất thường | ⚠️ Cần theo dõi | Chuyển lợi nhuận hoặc rút tiền qua lãi vay | Hợp đồng vay; lãi suất so với thị trường |
| 29 | Phí quản lý công ty mẹ thu từ công ty con tăng nhanh | ⚠️ Cần theo dõi | Công cụ rút tiền (tunneling qua phí) | So sánh phí quản lý vs quy mô và ngành |
| 30 | Family-controlled group, nhiều công ty niêm yết và chưa niêm yết | ⚠️ Cần theo dõi | Rủi ro đối xử không công bằng giữa cổ đông | Quy chế quản trị; lịch sử giao dịch cổ đông lớn |

### B.5 Disclosure Red Flags / Cờ đỏ công bố thông tin

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 31 | Ý kiến kiểm toán không unqualified | 🔴 Nghiêm trọng | BCTC có vấn đề trọng yếu | Đọc kỹ qualification hoặc emphasis |
| 32 | Thay đổi công ty kiểm toán / KTV chính 2 năm liên tiếp | ⚠️ Cần theo dõi | Có thể do bất đồng kế toán | Lý do công bố; lịch sử kiểm toán |
| 33 | BCTC bị điều chỉnh / restatement | 🔴 Nghiêm trọng | Sai sót trọng yếu kỳ trước | Mức độ điều chỉnh; ảnh hưởng LNST và vốn CSH |
| 34 | Management letter có nội dung nghiêm trọng không công khai đầy đủ | ⚠️ Cần theo dõi | Kiểm toán viên phát hiện vấn đề nội kiểm soát | Yêu cầu công bố chi tiết qua IR |
| 35 | Thuyết minh BCTC thiếu chi tiết về RPT, chính sách kế toán, hoặc dự phòng | 🟡 Lưu ý | Giảm transparency; che giấu rủi ro | So sánh thuyết minh với đối thủ cùng ngành |

### B.6 Ownership & Governance Red Flags / Cờ đỏ sở hữu & quản trị

| # | Dấu hiệu | Mức | Ý nghĩa | Kiểm tra thêm |
|---|----------|-----|---------|---------------|
| 36 | Pledged shares > 30% vốn điều lệ | 🔴 Nghiêm trọng | Rủi ro margin call, ép bán, mất kiểm soát | Tỷ lệ thế chấp qua các quý; giá vs mức thế chấp |
| 37 | Pledged shares > 60% | 🔴 Nghiêm trọng | Rủi ro hệ thống — đợt giảm giá có thể gây mất kiểm soát | Thỏa thuận tín dụng; quyền kích hoạt của ngân hàng |
| 38 | Ban điều hành thay đổi nhanh (> 2 lần CEO/CFO trong 3 năm) | ⚠️ Cần theo dõi | Bất ổn chiến lược hoặc xung đột nội bộ | Lý do từ chức; chính sách kế toán có thay đổi |
| 39 | Insiders bán ròng liên tục 2+ quý | ⚠️ Cần theo dõi | Insider không tin tưởng triển vọng | Khối lượng và thờị điểm bán; so sánh ESOP |
| 40 | ESOP / Warrant / Convertible pha loãng EPS > 10% fully diluted | ⚠️ Cần theo dõi | Pha loãng cổ đông; động cơ phát hành không rõ | Vesting schedule; điều kiện chuyển đổi; mục đích vốn |
| 41 | Cổ đông lớn giảm sở hữu đáng kể không có lý do chiến lược | ⚠️ Cần theo dõi | Thoái vốn do lo ngại nội bộ | Lý do công bố; ngưởị mua vào |

---

## Section C: VN-Specific Forensic / Đặc thù pháp lý Việt Nam

### C.1 VAS Gotchas — Những "bẫy" kế toán VN

| Khoản mục | VAS xử lý như thế nào | Vì sao là vấn đề forensic | Cách điều chỉnh khi phân tích |
|-----------|----------------------|---------------------------|------------------------------|
| **TSCĐ / Đất đai** | Ghi theo giá gốc, **không được đánh giá lại** (revaluation) | Giá trị sổ sách thấp hơn thực tế nhiều lần → ROA, ROE bị "đẹp hóa" (mẫu số nhỏ) | Dùng NAV điều chỉnh; so sánh P/B với NAV thay vì book value thô |
| **Bất động sản đầu tư** | Giá gốc − khấu hao | Không phản ánh giá trị thị trường; P/B sai lệch | Điều chỉnh theo giá thị trường nếu có dữ liệu |
| **Goodwill** | Khấu hao đều tối đa 10 năm, **không impairment test hàng năm** | Lợi nhuận giảm đều nhẹ nhàng thay vì impairment đột ngột → che giấu rủi ro M&A | Tự tính impairment test đơn giản; so sánh giá trị thu hồi với carrying amount |
| **Thuê tài sản (operating lease)** | Không ghi nhận trên bảng cân đối | D/E thấp hơn thực tế; nợ tiềm tàng lớn | Ước tính nợ thuê và tài sản quyền sử dụng từ cam kết thuê |
| **Doanh thu BĐS bán trước** | Có thể ghi nhận **sớm hơn IFRS** | Doanh thu/lợi nhuận "đẹp hơn" thực tế; dễ bị dồn cuối kỳ | Đọc kỹ thuyết minh ghi nhận DT; so sánh với tiến độ thực tế dự án |
| **Dự phòng tín dụng (ngân hàng)** | Mô hình **tổn thất đã phát sinh** | Dự phòng thấp hơn IFRS 9 (ECL); rủi ro ẩn khi nợ chưa xấu nhưng có dấu hiệu | Theo dõi nợ nhóm 2; ước tính ECL đơn giản |
| **Thu nhập khác** | Phân loại đôi khi mơ hồ | Che giấu lợi nhuận một lần hoặc tài chính | Phân rã thu nhập khác; tách recurring vs one-off |
| **Dự phòng giảm giá tồn kho** | Theo giá gốc hoặc giá trị thuần có thể thực hiện | Không cho phép LIFO; nhưng vẫn có room để trì hoãn ghi nhận | So sánh tỷ lệ dự phòng với ngành; kiểm tra tuổi tồn kho |
| **Chênh lệch tỷ giá** | Ghi vào chi phí tài chính hoặc riêng | Méo biên ròng và dòng tiền | Phân tích riêng ảnh hưởng tỷ giá; dùng EBIT nguyên thủy |
| **Quỹ đánh giá lại tài sản / Revaluation reserve** | VAS hạn chế; chỉ áp dụng với một số trường hợp đặc biệt | Ít DN VN có revaluation reserve lớn; nếu có → cần kiểm tra cơ sở đánh giá | Đọc thuyết minh chi tiết; xác minh đơn vị thẩm định độc lập |

### C.2 IFRS Reconciliation — Khi dữ liệu IFRS có sẵn

Một số DN lớn (VIC, VHM, ngân hàng lớn) công bố BCTC IFRS song song VAS.

**Điều chỉnh trọng yếu:**
- **Tổng tài sản:** IFRS cao hơn do operating lease lên bảng + BĐS đầu tư đánh giá lại.
- **Nợ:** IFRS cao hơn do nợ thuê tài chính (IFRS 16) + ECL dự phòng sớm hơn.
- **Lợi nhuận:** BĐS thường thấp hơn (DT ghi nhận chậm), ngân hàng thấp hơn (ECL).
- **Goodwill:** IFRS không khấu hao → EBIT cao hơn nhưng rủi ro impairment đột ngột.

**Nguyên tắc:** Ưu tiên IFRS cho cross-border comparison; dùng VAS + điều chỉnh cho trend analysis nội bộ.

### C.3 Typical VN Accounting Manipulation Patterns / Các mẫu thao túng điển hình ở VN

| Mẫu thao túng | Cách nhận biết | Ngành hay gặp | Cách phát hiện |
|---------------|---------------|---------------|----------------|
| **Pre-IPO dressing** | LNST tăng đột biến 1–2 năm trước IPO; CFO không theo kịp; sau IPO lợi nhuận sụt | Tất cả ngành | So sánh 3 năm trước vs sau IPO; M-score trước IPO |
| **Earnings smoothing** | LNST biến động rất ít so với doanh thu; dự phòng tăng giảm đều đặn | Ngân hàng, bảo hiểm, bán lẻ | Kiểm tra biến động dự phòng; so sánh LNST với OCF |
| **RPT sales inflation** | DT tăng nhờ bán cho công ty con/liên kết; giá cao hơn thị trường; phải thu RPT tăng | Tập đoàn đa ngành, sản xuất | So sánh giá RPT vs độc lập; kiểm tra DSO khác biệt |
| **Capitalized interest engineering** | Lãi vay vốn hóa vào giá vốn dự án BĐS → LNST cao hơn thực; CFO giảm | Bất động sản, xây dựng | So sánh lãi vay vốn hóa / tổng lãi vay; kiểm tra dự án chưa bàn giao |
| **Debt covenant engineering** | Thay đổi chính sách kế toán để D/E hoặc Interest Coverage nằm trong covenant | Phi tài chính nợ vay lớn | Stress test: EBIT −20% → vi phạm covenant? |
| **Cross-holding circular flow** | Công ty A mua cổ phiếu B, B mua cổ phiếu C, C cho A vay — dòng tiền quay vòng | Tập đoàn gia đình, private conglomerate | Vẽ sơ đồ sở hữu; kiểm tra dòng tiền từ CFF và CFI |
| **Land value understatement + off-book** | Đất mua từ lâu, giá gốc rất thấp; không lên sổ đỏ hoặc sổ đỏ mang tên cá nhân | Bất động sản, nông nghiệp | Kiểm tra quỹ đất trong báo cáo thường niên; so sánh với giá thị trường |

### C.4 Case Examples — Ví dụ thực tế (đã ẩn danh)

**Case 1 — Real estate conglomerate with pledged shares > 60%:**
Tập đoàn BĐS niêm yết tại HOSE, cổ đông gia đình thế chấp > 60% cổ phần 2021–2023 để vay ngân hàng phục vụ dự án. Giá cổ phiếu giảm 40% trong 6 tháng → margin call → bán tài sản cắt lỗ, trầm trọng hóa đà giảm. **Bài học:** Pledged shares > 30% là 🔴; > 60% là rủi ro hệ thống.

**Case 2 — Pre-IPO earnings smoothing (consumer goods manufacturer):**
Công ty hàng tiêu dùng chuẩn bị IPO 2022. LNST tăng 35–42% 2 năm trước IPO, CFO chỉ tăng 5–8%. Sau IPO 12 tháng, LNST giảm 25%. Điều tra cho thấy công ty tăng dự phòng tồn kho trước IPO (làm LNST năm trước thấp), sau đó giảm dự phòng (làm LNST năm IPO cao), kéo dài công nợ khách hàng. **Bài học:** M-score > −1.2; CFO/LNST < 0.6 trước IPO là 🔴 mạnh.

**Case 3 — Related-party revenue inflation (family-controlled industrial group):**
Tập đoàn công nghiệp gia đình: công ty niêm yết A bán nguyên liệu cho công ty chưa niêm yết B giá cao hơn thị trường 15–20%; B bán thành phẩm lại cho công ty niêm yết C giá thấp hơn thị trường. Lợi nhuận "bơm" vào A và C, B âm thầm lỗ. Dòng tiền A và C không khớp lợi nhuận do phải thu từ B tăng. **Bài học:** RPT > 20% DT → vẽ sơ đồ dòng tiền; DSO RPT thường dài hơn DSO độc lập > 30 ngày.

---

## Section D: Output Pattern / Cách trình bày kết quả pháp lý

### D.1 Forensic Findings in Deep-Dive Memo

Khi tích hợp vào memo phân tích sâu (workflow-deep-dive.md):

```
## 5. FORENSIC & CHẤT LƯỢNG BCTC

### 5.1 Tổng quan chất lượng
- CFO/LNST 3 năm: [x, y, z]
- Accrual Ratio trend: [tăng/giảm/ổn định]
- Beneish M-score: [giá trị]
- Piotroski F-score: [giá trị]

### 5.2 Cờ đỏ
🔴 Nghiêm trọng: [Mô tả + số liệu]
⚠️ Cần theo dõi: [Mô tả + số liệu]
🟡 Lưu ý: [Mô tả + số liệu]

### 5.3 VAS/IFRS & Governance
- [Điều chỉnh chuẩn mực; sơ đồ sở hữu; pledged shares]

### 5.4 Kết luận forensic
- [Tổng hợp rủi ro; câu hỏi cần làm rõ]
```

### D.2 Severity Scale & Confidence Level

Mỗi cờ đỏ gán **2 thang điểm:**

**Severity:**
- 🔴 **Red:** Ảnh hưởng đến kết luận hoặc manipulation / stress nghiêm trọng.
- ⚠️ **Yellow:** Bất thường cần theo dõi. 3+ yellow cùng hướng → nâng lên composite Red.
- 🟢 **Green:** Đã kiểm tra, bình thường.

**Confidence:**
- **High:** Số liệu rõ ràng, cross-check đa nguồn.
- **Medium:** Cần thêm thông tin (thuyết minh, IR).
- **Low:** Nghi ngờ từ pattern, thiếu bằng chứng trực tiếp.

**Quy tắc nâng cấp:** 1 Red (High) → không bỏ qua; 3+ Yellow cùng hướng → composite Red; Red + Low → ghi rõ và đề xuất câu hỏi.

### D.3 Covenant Stress Test Template

```
| Kịch bản | EBIT giảm 20% | Trích lập dự phòng +50% | Lãi suất tăng 200bps |
|----------|---------------|------------------------|---------------------|
| Interest Coverage | [x.x]x | — | [x.x]x |
| D/E | [x.x]x | [x.x]x | [x.x]x |
| Current Ratio | [x.x]x | [x.x]x | [x.x]x |
| Covenant breach? | Yes / No | Yes / No | Yes / No |
```

---

## Cross-Reference Block / Khối tham chiếu chéo

**Module liên quan trực tiếp:**
- `workflow-deep-dive.md` — Định dạng output forensic trong memo phân tích sâu.
- `domain-equity-vn-valuation.md` — Forensic input cho normalized earnings; chất lượng kém → discount rate adjustment.
- `domain-equity-vn-industry-guides.md` — Cờ đỏ đặc thù ngành (NH: lãi dự thu, nợ nhóm 2; BĐS: vốn hóa lãi vay; logistics: dry-dock).
- `framework-regime-v11.md` — Stage-based vulnerability: regime tightening → covenant stress → default risk nhanh hơn.
- `core-evidence-ladder.md` — Mức độ bằng chứng yêu cầu cho mỗi cờ đỏ.

**Mối quan hệ:**
- Forensic + `domain-equity-vn-industry-guides.md` = bức tranh rủi ro đầy đủ.
- Forensic + `framework-regime-v11.md` = stress test theo chu kỳ.
- Forensic + `domain-equity-vn-valuation.md` = điều chỉnh valuation (accrual cao → normalized earnings thấp; governance red flags → discount rate premium).

---

> **END OF MODULE** — domain-equity-vn-forensic-accounting.md
> 
> Last updated: 2026-04-19 | Wave 3 Lane 6 | Merged from FinMentor 115 + 80 + VAS/IFRS 70 | OPVIA Sigma format
