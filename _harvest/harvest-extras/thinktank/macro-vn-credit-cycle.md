---
title: "Macro VN Credit Cycle — Chu Kỳ Tín Dụng Việt Nam 2018-2026: Dữ liệu Thực, Động lực Ngân hàng Quốc doanh, và Hệ thống Cảnh báo"
module_type: "domain"
file_name: "macro-vn-credit-cycle.md"
purpose: "Phân tích chu kỳ tín dụng Việt Nam 2018-2026 với dữ liệu thực, framework 4 pha chu kỳ, đặc thù room tín dụng + BĐS + TPDN, và phân hóa hành vi giữa ngân hàng quốc doanh (VCB, CTG, BID) và ngân hàng tư nhân (JSB)."
primary_triggers:
  - "chu kỳ tín dụng Việt Nam"
  - "room tín dụng NHNN"
  - "nợ xấu ngân hàng VN"
  - "LDR ngân hàng"
  - "tín dụng BĐS"
  - "tái cơ cấu nợ Thông tư 01"
  - "SOE bank vs private bank"
  - "Basel III CAR VN"
when_to_use:
  - "Khi phân tích vị trí hiện tại của nền kinh tế VN trong chu kỳ tín dụng và đánh giá rủi ro hệ thống."
  - "Khi so sánh khẩu vị rủi ro và khả năng tăng trưởng tín dụng giữa các nhóm ngân hàng (Big 4 vs JSB)."
  - "Khi đánh giá tác động của chính sách room tín dụng, Thông tư 01/2020, hoặc Basel III lên ngành ngân hàng."
when_not_to_use:
  - "Không dùng để dự báo giá cổ phiếu ngân hàng riêng lẻ — cần kết hợp với equity-vn/financial-modeling.md."
  - "Không dùng cho phân tích thị trường trái phiếu doanh nghiệp chi tiết — xem fixed-income/credit-spreads-vn.md."
related_modules:
  - "macro-vn-monetary-policy-nhnn.md"
  - "macro-vn-liquidity-systems.md"
  - "framework-thakor-yu-2024.md"
  - "framework-kashyap-stein-bank-lending.md"
  - "framework-regime-v11.md"
  - "fixed-income/credit-spreads-vn.md"
  - "equity-vn/bank-sector-deep-dive.md"
authoritative_citations:
  - "NHNN Thống kê Ngân hàng Hàng tháng (sbv.gov.vn)"
  - "FiinTrade Bank Sector Dashboard (fiintrade.vn)"
  - "VEPR Quarterly Banking Monitor (vepr.org.vn)"
  - "IMF Article IV Vietnam (2023-2024)"
  - "World Bank Vietnam Macro Poverty Outlook (2024-2025)"
  - "Vietcap Banking Sector Reports (vcsc.com.vn)"
  - "ACBS Strategy & Macro Research (acbs.com.vn)"
output_owner: "workflow-deep-dive.md khi ngườii dùng hỏi về chu kỳ tín dụng; workflow-daily-brief.md khi có dữ liệu tín dụng mới từ NHNN."
---

# Chu Kỳ Tín Dụng Việt Nam 2018-2026: Dữ liệu Thực, Động lực Ngân hàng Quốc doanh, và Hệ thống Cảnh báo

**Mục đích:** Cung cấp khung phân tích chu kỳ tín dụng Việt Nam (credit cycle) dựa trên dữ liệu thực 2018-2026, với emphasis đặc biệt vào vai trò của nhóm ngân hàng quốc doanh (VCB, CTG, BID — chiếm ~45% tài sản toàn ngành) và cơ chế điều tiết đặc thù (room tín dụng, Thông tư 01, Basel III).

**Trạng thái:** [DỮ LIỆU THỰC TẾ 2018-2024 | DỰ BÁO 2025-2026 | CẬP NHẬT THEO NHNN MONTHLY]

**Ngôn ngữ:** Tiếng Việt chính, thuật ngữ chuyên môn giữ nguyên tiếng Anh

---

## 1. Framework Chu Kỳ Tín Dụng — 4 Pha

Chu kỳ tín dụng Việt Nam tuân theo framework chu kỳ tín dụng kinh điển (Borio, BIS 2014; Minsky, 1986) nhưng bị biến dạng bởi cơ chế room tín dụng hành chính và vai trò chủ đạo của ngân hàng quốc doanh. Dưới đây là 4 pha chu kỳ được điều chỉnh cho bối cảnh Việt Nam.

### Ma trận Pha Chu kỳ × Đặc trưng Việt Nam

| Đặc trưng | Early Cycle (Phục hồi) | Mid Cycle (Mở rộng) | Late Cycle (Quá nhiệt) | Contraction (Deleveraging) |
|---|---|---|---|---|
| **Tăng trưởng tín dụng YoY** | <10%, đang tăng tốc từ đáy | 12-16%, momentum tăng | >16% hoặc >15% nhưng momentum giảm | <10%, thậm chí gần 0% |
| **Credit demand thực** | Yếu, DN thận trọng đầu tư | Mạnh lên, đầu tư mở rộng | Đầu cơ chiếm tỷ trọng cao (BĐS, margin CK) | Sụt giảm, DN không vay mới |
| **LDR hệ thống** | Thấp (~75-80%), dư thanh khoản | Tăng dần (~80-85%) | Tiến gần/trên 85% (trần NHNN khuyến nghị) | Giảm do tiền gửi chảy vào nhanh hơn cho vay |
| **NPL báo cáo** | Cao (từ chu kỳ trước), đang đỉnh | Bắt đầu giảm, "bức tranh đẹp lên" | Thấp nhất chu kỳ, nhưng NPL ẩn tích lũy | Tăng rõ rệt, Thông tư 01 hết hiệu lực |
| **Spread cho vay - huy động** | Rộng (rủi ro cao, thanh khoản dồi dào nhưng không ai vay) | Thu hẹp dần (cạnh tranh gay gắt) | Thu hẹp mạnh, thậm chí âm ở một số phân khúc | Giãn ra trở lại (rủi ro được định giá lại) |
| **BĐS tín dụng** | Đóng băng, thanh khoản kém | Phục hồi, giao dịch tăng | Sốt nóng, đầu cơ margin, phát hành TPDN ồ ạt | Đóng băng, nợ xấu BĐS tăng, TPDN vỡ nợ |
| **NHNN stance** | Nới lỏng, room mở rộng, lãi suất giảm | Trung tính, room tăng dần | Bắt đầu signal siết (room chậm lại, lãi suất tăng) | Thắt chặt hoặc nới lỏng nhưng không hiệu quả |
| **Basel III CAR pressure** | Thấp (dư vốn, chưa cần tăng vốn) | Vừa phải | Bắt đầu hiện (tăng trưởng nhanh ăn vào CAR) | Cao (NPL tăng → RWA tăng → CAR giảm) |
| **SOE bank behavior** | Được giao room cao, cho vay chính sách (ưu đãi lãi suất) | Tăng trưởng tín dụng chậm hơn JSB do quy trình rườm rà | Bị hạn chế room trước, "phanh sớm" theo chỉ đạo | Được ưu tiên recapitalization, mua nợ xấu từ JSB |
| **Private JSB behavior** | Thận trọng, tích lũy thanh khoản | Tăng trưởng nhanh hơn SOE, cạnh tranh lãi suất | Đẩy mạnh tín dụng tiêu dùng, BĐS, margin | NPL tăng nhanh hơn SOE, bị siết room mạnh |

### 1.1 Early Cycle (Recovery)
- **Credit demand:** Yếu. Doanh nghiệp vừa trải qua giai đoạn suy thoái, bảng cân đối kém, không có động lực vay mới.
- **Ngân hàng:** Ngồi trên thanh khoản dồi dào (LDR thấp), nhưng khẩu vị rủi ro thấp. Tiêu chuẩn cho vay (credit standard) chặt.
- **NPL:** Vẫn ở mức cao từ chu kỳ trước — đây là "hangover" mà hệ thống phải xử lý trước khi tín dụng thực sự phục hồi.
- **SOE bank:** Được NHNN ưu tiên giao room cao để "kéo" tín dụng vào nền kinh tế. Cho vay chính sách (lãi suất ưu đãi cho SOE, nông nghiệp, doanh nghiệp nhỏ) tăng mạnh.
- **Private JSB:** Thận trọng hơn, tập trung vào tiền gửi và trái phiếu chính phủ (TPCP). Một số JSB nhỏ bị siết room vì CAR thấp.

### 1.2 Mid Cycle (Expansion)
- **Credit demand:** Phục hồi rõ rệt. Doanh nghiệp mở rộng sản xuất, đầu tư mới.
- **Ngân hàng:** Tín dụng tăng trưởng nhanh, spread bắt đầu nén lại do cạnh tranh.
- **NPL:** Bắt đầu giảm — nhưng đây là "bẫy": NPL giảm không phải vì chất lượng tài sản thực sự cải thiện, mà vì tăng trưởng tín dụng nhanh làm phân tán (dilute) tỷ lệ NPL.
- **SOE bank:** Tăng trưởng chậm hơn JSB do quy trình phê duyệt phức tạp và ràng buộc cho vay chính sách. Tuy nhiên, chi phí huy động thấp hơn (thương hiệu + mạng lưới) giúp biên lợi nhuận ổn định.
- **Private JSB:** Tăng trưởng tín dụng nhanh hơn SOE, đặc biệt ở phân khúc tiêu dùng và BĐS. Một số JSB (TCB, VPB, MBB) có thể tăng trưởng 20-25% YoY trong giai đoạn này.

### 1.3 Late Cycle (Overheating)
- **Credit demand:** Bao gồm cả nhu cầu thực và đầu cơ. Tín dụng BĐS và margin chứng khoán tăng vọt.
- **Ngân hàng:** Tín dụng tăng nhanh hơn tiền gửi → LDR tiến gần trần. Spread nén mạnh.
- **NPL:** Ở mức thấp nhất chu kỳ — đây là điểm nguy hiểm nhất vì NPL ẩn (nhóm 2 + tái cơ cấu) đang tích lũy.
- **SOE bank:** NHNN bắt đầu hạn chế room sớm hơn đối với SOE bank để kiểm soát hệ thống. Tuy nhiên, vì SOE bank có CAR cao hơn trung bình, họ vẫn có room để tăng trưởng.
- **Private JSB:** Tiếp tục đẩy mạnh tín dụng để giành thị phần, đôi khi "vượt room" bằng cách mua trái phiếu doanh nghiệp (TPDN) hoặc cho vay qua công ty con.

### 1.4 Contraction (Deleveraging)
- **Credit demand:** Sụt giảm. Doanh nghiệp cắt giảm đầu tư, hộ gia đình giảm vay tiêu dùng.
- **Ngân hàng:** Tăng trưởng tín dụng chậm lại đáng kể, thanh khoản căng thẳng do tiền gửi chảy ra (hoặc không vào nhanh bằng cho vay).
- **NPL:** Tăng rõ rệt. Thông tư 01/2020 hết hiệu lực (hoặc gia hạn) → NPL ẩn phải lộ ra.
- **SOE bank:** Được NHNN ưu tiên trong các gói hỗ trợ. Có thể được bơm vốn nhà nước (recapitalization) hoặc mua nợ xấu từ JSB nhỏ để ổn định hệ thống.
- **Private JSB:** Chịu áp lực mạnh hơn. NPL tăng nhanh hơn, CAR giảm, bị siết room mạnh. JSB nhỏ/yếu có nguy cơ bị sáp nhập.

---

## 2. Đặc thù Chu kỳ Tín dụng Việt Nam

### 2.1 Cơ chế Room Tín dụng (Credit Room)

Room tín dụng là công cụ điều tiết đặc thù của NHNN, không có ở hầu hết các nền kinh tế thị trường phát triển. Đây là biến số then chốt làm biến dạng chu kỳ tín dụng tự nhiên.

| Đặc điểm | Chi tiết |
|---|---|
| **Cơ chế phân bổ** | Hàng năm, NHNN giao chỉ tiêu tăng trưởng tín dụng cho từng NHTM dựa trên: (1) xếp hạng CAMELS, (2) CAR, (3) chất lượng tài sản, (4) nhu cầu chính sách |
| **Tỷ lệ tăng trưởng tín dụng mục tiêu toàn hệ thống** | Thường 14-16%/năm; 2020 giảm xuống ~10%; 2021-2022 tăng lại ~14%; 2023-2024 ~14-15% |
| **Tính ràng buộc** | Nếu bank đạt room sớm → phải dừng cho vay mới hoặc mua TPCP (không tính vào room theo một số quy định) |
| **Tính linh hoạt** | NHNN có thể điều chỉnh room giữa năm (thường vào Q2-Q3). Năm 2024, NHNN giao room ngay từ đầu năm thay vì chia đợt |
| **Impact lên chu kỳ** | Làm chu kỳ tín dụng "bị cắt ngang" — khi room hết, tín dụng đột ngột chững lại dù nhu cầu vẫn còn |

**Ma trận Phân bổ Room Tín dụng: SOE Bank vs Private JSB**

| Tiêu chí | SOE Bank (VCB, CTG, BID, Agribank) | Private JSB (TCB, VPB, MBB, ACB, v.v.) |
|---|---|---|
| **Room cơ bản (% tài sản)** | Thường được giao room cao hơn tỷ lệ thị phần do vai trò "neo" chính sách | Room phụ thuộc hoàn toàn vào CAR, xếp hạng CAMELS, và NPL |
| **Ưu tiên chính sách** | Được ưu tiên khi NHNN muốn "kéo" tín dụng vào nền kinh tế (giai đoạn phục hồi) | Không có ưu tiên chính sách; phải cạnh tranh dựa trên hiệu quả |
| **Hành vi khi room cạn** | Tiếp tục cho vay chính sách (không tính hoặc tính một phần vào room) | Dừng cho vay mới hoặc chuyển sang kênh khác (TPDN, cho vay liên kết) |
| **CAR buffer trước Basel III** | VCB ~11-12%, CTG ~9-10%, BID ~9-10% [DỮ LIỆU THIẾU chi tiết quarterly]; cao hơn trung bình JSB | Biến động lớn: TCB ~11%, VPB ~9%, MBB ~10%, ACB ~10-11% [DỮ LIỆU THIẾU] |
| **Khả năng hấp thụ Basel III** | Cao — vốn nhà nước đứng sau, dễ recapitalization | Trung bình-thấp — cần phát hành cổ phiếu, trái phiếu chuyển đổi, hoặc giảm tăng trưởng |

### 2.2 Thị trường Trái phiếu Doanh nghiệp (TPDN) — Kênh Tín dụng Thay thế

TPDN Việt Nam trong giai đoạn 2020-2022 hoạt động như một "ersatz credit" (tín dụng thay thế) — cho phép DN (đặc biệt BĐS) vay vốn ngoài hệ thống ngân hàng, nhưng thực chất vẫn phụ thuộc vào bảo lãnh ngân hàng và nguồn vốn từ chính các NHTM.

| Chỉ tiêu | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|
| **Tổng phát hành TPDN (tỷ VND)** | ~400.000 | ~600.000 | ~300.000 [DỮ LIỆU THIẾU chính xác] | ~100.000 | ~80.000 [DỮ LIỆU THIẾU] |
| **TPDN / Tín dụng ngân hàng** | ~7% | ~15-20% | ~10% | ~3-4% | ~3% |
| **Tỷ trọng BĐS trong TPDN** | ~60% | ~70% | ~65% | ~50% (nhưng nợ cũ chiếm lớn) | [DỮ LIỆU THIẾU] |
| **Lãi suất TPDN trung bình** | 8-10% | 10-13% | 12-15% | Default/Restructuring | 10-12% (phát hành mới ít) |
| **Nợ xấu TPDN (ước tính)** | <2% | <3% | ~15-20% | ~25-30% | ~20% [DỮ LIỆU THIẾU] |

**Case Study:** TPDN BĐS 2021-2022 là minh chứng điển hình cho "shadow credit cycle" — tín dụng tăng nhanh qua kênh phi ngân hàng, không bị room tín dụng kiểm soát, dẫn đến bong bóng và vỡ sau đó. Khi NHNN siết TPDN (Thông tư 16/2021, Thông tư 08/2022), dòng vốn đột ngột khô cạn, BĐS đóng băng, và NPL ngân hàng tăng (do nhiều TPDN có bảo lãnh ngân hàng).

### 2.3 Tín dụng Bất động sản (BĐS) — Hệ thống Collateral

BĐS không chỉ là một ngành nhận tín dụng — nó là **hệ thống tài sản đảm bảo (collateral)** cho toàn bộ nền kinh tế. Đây là đặc thù then chốt làm cho chu kỳ tín dụng Việt Nam nhạy cảm với BĐS hơn hầu hết các EM khác.

| Kênh tín dụng BĐS | Tỷ trọng ước tính | Chi tiết |
|---|---|---|
| **Tín dụng trực tiếp cho BĐS (NHNN công bố)** | ~20-22% tổng tín dụng | Cho vay dự án, cho vay mua nhà, cho vay đầu tư BĐS |
| **Tín dụng gián tiếp qua TPDN có bảo lãnh NH** | ~5-8% | TPDN BĐS có bảo lãnh thanh toán từ NH |
| **Tín dụng sử dụng BĐS làm collateral** | ~25-30% | Cho vay sản xuất kinh doanh, cho vay tiêu dùng, cho vay cá nhân dùng sổ đỏ thế chấp |
| **Tổng exposure lên BĐS (direct + indirect)** | **~50-60% tổng tín dụng** | Ước tính của Vietcap, ACBS. NHNN công bố số liệu thấp hơn do định nghĩa hẹp |
| **Tín dụng margin chứng khoán (liên quan BĐS)** | ~2-3% | Tăng mạnh 2020-2021 khi VN-Index tăng nóng; giảm 2022-2023 |

**Ma trận Pha Chu kỳ × Tín dụng BĐS**

| Pha | Tín dụng BĐS trực tiếp | Giá BĐS | NPL BĐS | TPDN BĐS | Hành vi NH |
|---|---|---|---|---|---|
| Early Cycle | Đóng băng, giảm | Giảm 10-20% từ đỉnh | Cao (từ chu kỳ trước) | Ít phát hành | Thận trọng, siết appraisal |
| Mid Cycle | Phục hồi, tăng 10-15% | Ổn định, tăng nhẹ | Giảm | Phát hành tăng | Nới lỏng dần |
| Late Cycle | Tăng nóng >20% | Tăng nhanh, đầu cơ | Thấp nhất (bị che) | Bùng nổ phát hành | Bắt đầu signal siết |
| Contraction | Giảm mạnh | Giảm 20-30% | Tăng vọt | Vỡ nợ, tái cơ cấu | Siết chặt, xử lý nợ xấu |

---

## 3. Dữ liệu Thực: Lộ trình Chu kỳ Tín dụng Việt Nam 2018-2026

### Tóm tắt Số liệu Tín dụng Hàng năm

| Năm | Tăng trưởng tín dụng YoY (NHNN) | LDR hệ thống | NPL báo cáo (NHNN) | NPL điều chỉnh (Vietcap/ACBS ước tính) | Refinancing Rate (cuối năm) | VND mất giá vs USD | Regime |
|---|---|---|---|---|---|---|---|
| **2018** | ~14.5% | ~82% | ~1.9% | ~3.5-4.5% | 6.25% | ~2.0% | Late Cycle |
| **2019** | ~12.5% | ~80% | ~1.6% | ~3.0-4.0% | 6.0% | ~1.5% | Deceleration |
| **2020** | ~9.1% | ~76% | ~1.7% | ~4.0-5.5% (gồm Thông tư 01) | 4.0% | ~0.2% | COVID Shock |
| **2021** | ~13.5% | ~80% | ~1.5% | ~5.0-6.5% (gồm TT01 + TPDN) | 4.0% | ~1.8% | Stimulus Rebound |
| **2022** | ~14.2% | ~85% | ~1.9% | ~6.0-8.0% | 6.0% | ~4.5% | Crisis + Restructuring |
| **2023** | ~13.5-14.0% | ~83% | ~2.2% | ~6.5-8.5% | 4.5% | ~2.8% | Selective Tightening |
| **2024** | ~15.0% [DỮ LIỆU THIẾU chính xác cuối năm] | ~84% | ~2.0-2.3% | ~5.5-7.5% | 4.5% | ~2.5% | Recovery |
| **2025 (Dự báo)** | ~14-15% | ~85% | ~2.0-2.5% | ~5.0-7.0% | 4.0-4.5% | ~2.0-3.0% | Expansion |
| **2026 (Outlook)** | ~14% | ~85-87% | ~2.5-3.0% | ~5.0-6.5% | 4.5% | ~2.0-3.0% | Late Cycle / Basel III |

### 3.1 2018: Đỉnh Chu kỳ Trước (Late Cycle)
- **Bối cảnh:** Kinh tế tăng trưởng tốt (~7.0% GDP), FDI cao, xuất khẩu mạnh.
- **Tín dụng:** Tăng ~14.5% YoY, tiến gần trần room. LDR ~82%.
- **BĐS:** Sôi động, đặc biệt ở TP.HCM và Hà Nội. Tín dụng BĐS trực tiếp ~20% tổng tín dụng.
- **NPL:** Báo cáo thấp (~1.9%) nhưng NPL thực (gồm nhóm 2 + tái cơ cấu) ước tính cao hơn đáng kể.
- **SOE bank:** VCB, CTG, BID tăng trưởng chậm hơn JSB do đã tiến gần trần CAR và bị hạn chế room sớm.
- **JSB:** TCB, VPB, MBB tăng trưởng nhanh, đặc biệt ở tín dụng tiêu dùng và BĐS.

### 3.2 2019: Giảm Tốc (Deceleration)
- **Tín dụng:** Chậm lại còn ~12.5% YoY. NHNN giữ room chặt để kiểm soát rủi ro.
- **BĐS:** Bắt đầu chững lại. Một số dự án bị đình trệ do vướng pháp lý.
- **NPL:** Bắt đầu tăng nhẹ nhưng bị che bởi Thông tư 19/2016 (cho phép tái cơ cấu nợ).
- **SOE bank:** VCB tiếp tục tăng trưởng ổn định (~15% [DỮ LIỆU THIẾU chính xác]); CTG và BID chậm hơn do vướng quá trình cổ phần hóa và xử lý nợ xấu.
- **JSB:** Tăng trưởng phân hóa — JSB có chiến lược tốt (TCB, ACB) tiếp tục tăng trưởng, JSB yếu bị siết room.

### 3.3 2020: Cú Sốc COVID-19 + Thông tư 01 (Restructuring)
- **Tín dụng:** Tăng chậm nhất trong nhiều năm (~9.1%) do nhu cầu vay sụt giảm.
- **Thông tư 01/2020/TT-NHNN:** Cho phép ngân hàng tái cơ cấu nợ, giữ nguyên nhóm nợ cho các khoản vay bị ảnh hưởng COVID. Đây là "forbearance" quy mô lớn — NPL báo cáo được giữ thấp nhân tạo.
- **Thanh khoản:** NHNN giảm lãi suất điều hành mạnh (từ 6.0% xuống 4.0%), bơm thanh khoản qua OMO.
- **SOE bank:** Được giao nhiệm vụ cho vay ưu đãi lãi suất hỗ trợ doanh nghiệp (gói 16.000 tỷ VND và các gói khác). VCB, BID là đầu mối chính.
- **JSB:** Thận trọng hơn, tập trung vào cho vay ngắn hạn và tín dụng tiêu dùng thiết yếu.

**[DỮ LIỆU THIẾU]:** Số liệu chính xác về giá trị nợ được tái cơ cấu theo Thông tư 01 không được NHNN công bố chi tiết hàng quý. Ước tính của broker: ~300.000-500.000 tỷ VND tại đỉnh.

### 3.4 2021: Phục hồi Kích thích + BĐS Sôi sục
- **Tín dụng:** Tăng tốc trở lại ~13.5%. Room tín dụng được nới rộng.
- **BĐS:** Sốt nóng. Giá đất tăng 20-50% ở nhiều khu vực. Tín dụng BĐS và TPDN BĐS bùng nổ.
- **Chứng khoán:** VN-Index tăng từ ~1.000 lên ~1.500 điểm. Margin balance tăng vọt (~200.000 tỷ VND [DỮ LIỆU THIẾU chính xác]).
- **TPDN:** Phát hành kỷ lục (~600.000 tỷ VND). Lãi suất TPDN BĐS lên 12-15%.
- **SOE bank:** Tăng trưởng chậm hơn JSB. VCB tăng ~13-15%, CTG và BID ~10-12% [DỮ LIỆU THIẾU]. Tập trung cho vay lớn cho SOE và dự án hạ tầng.
- **JSB:** TCB, VPB, MBB tăng trưởng 20-30%. Tín dụng tiêu dùng, BĐS, và margin là động lực chính.

### 3.5 2022: Khủng hoảng TPDN + BĐS Tái cơ cấu
- **Sự kiện SCB (Tháng 10/2022):** Sụp đổ niềm tin vào TPDN BĐS, rút tiền hàng loạt tại SCB tạo ra cuộc khủng hoảng thanh khoản.
- **Tín dụng:** Tăng ~14.2% nhưng phân bổ không đều — H1 tăng nhanh, H2 chậm lại đáng kể sau sự cố SCB.
- **NHNN:** Tăng lãi suất điều hành 200bps (Tháng 9-10/2022), bán dự trữ ngoại hối can thiệp tỷ giá.
- **BĐS:** Đóng băng. Nhiều DN BĐS vỡ nợ (Novaland, Sunshine, v.v.). TPDN BĐS vỡ nợ hàng loạt.
- **SOE bank:** VCB, CTG, BID vẫn duy trì tăng trưởng dương. Được bơm thanh khoản từ NHNN. Mua TPDN BĐS distress (hoặc cho vay cứu trợ) theo chỉ đạo.
- **JSB:** Một số JSB bị ảnh hưởng nặng do exposure TPDN BĐS cao. LDR căng thẳng, chi phí huy động tăng.

### 3.6 2023: Siết Chọn lọc + Nén Biên Lợi nhuận
- **Tín dụng:** Tăng ~13.5-14.0%. NHNN áp dụng chính sách "siết chọn lọc" — room tín dụng có nhưng ưu tiên cho sản xuất, hạn chế BĐS.
- **NPL:** Báo cáo tăng nhẹ (~2.2%) nhưng NPL thực (gồm nhóm 2 + tái cơ cấu) ở mức cao.
- **Biên lợi nhuận:** Nén mạnh do (1) lãi suất huy động tăng nhanh hơn cho vay, (2) trích lập dự phòng tăng.
- **SOE bank:** VCB duy trì ROE cao nhất nhóm (~22-23% [DỮ LIỆU THIẾU]); CTG và BID cải thiện dần. CAR được bổ sung qua phát hành cổ phiếu (CTG, BID).
- **JSB:** Phân hóa mạnh. TCB, ACB, MBB giữ vững; VPB, MSB chịu áp lực. JSB nhỏ (PGBank, Kienlongbank, v.v.) bị siết room hoặc sáp nhập.

### 3.7 2024: Room Tín dụng Vẫn Ràng buộc, JSB Bị Ép
- **Tín dụng:** Tăng ~15.0% [DỮ LIỆU THIẾU chính xác cuối năm], vượt mục tiêu NHNN. Tuy nhiên, tăng trưởng chủ yếu đến từ H1.
- **Room tín dụng:** NHNN giao room ngay từ đầu năm thay vì chia đợt. Một số JSB hết room sớm (Q3).
- **NPL:** Báo cáo ~2.0-2.3% nhưng NPL thực vẫn cao do nhiều khoản nợ TPDN/BĐS đang trong giai đoạn tái cơ cấu.
- **SOE bank:** VCB tiếp tục dẫn đầu về quy mô và hiệu quả. BID và CTG cải thiện CAR sau phát hành cổ phiếu.
- **JSB:** JSB có room vẫn tăng trưởng nhanh; JSB hết room phải chuyển sang bán trái phiếu chính phủ hoặc tăng huy động.

### 3.8 2025-2026: Phục hồi + Áp lực Basel III
- **Dự báo tín dụng:** ~14-15% (2025), ~14% (2026). Tăng trưởng chậm lại so với tiềm năng do room tín dụng và Basel III.
- **Basel III:** Lộ trình áp dụng 2024-2028. CAR yêu cầu tăng, Tier-1 chất lượng cao hơn. Điều này hạn chế khả năng tăng trưởng tín dụng của nhóm JSB có CAR thấp.
- **SOE bank:** VCB, BID, CTG có lợi thế do CAR cao hơn và khả năng recapitalization từ nhà nước. Sẽ tiếp tục chiếm thị phần lớn.
- **JSB:** Phân hóa sâu hơn. JSB lớn (TCB, MBB, ACB, VPB) cần tăng vốn để đáp ứng Basel III. JSB nhỏ có nguy cơ bị sáp nhập.

---

## 4. Chỉ báo Credit/Deposit Divergence — Khi Nào Báo Đỏ

Khi tín dụng tăng nhanh hơn tiền gửi (credit-deposit divergence), hệ thống ngân hàng phải tìm nguồn vốn thay thế — thường là liên ngân hàng, TPDN, hoặc vay ngoại tệ. Đây là tín hiệu cảnh báo sớm cho Late Cycle.

### Ma trận Cảnh báo Credit-Deposit Divergence

| Mức độ divergence | Định nghĩa | Hàm ý | Hành động của NHNN | Ví dụ lịch sử |
|---|---|---|---|---|
| **Xanh** | Credit growth ≈ Deposit growth (±2%) | Cân bằng | Trung tính | 2019, Q1-Q2 2024 |
| **Vàng** | Credit growth > Deposit growth 2-4% | LDR tăng, áp lực thanh khoản nhẹ | Theo dõi, có thể siết room | 2021 H2 |
| **Cam** | Credit growth > Deposit growth 4-6% | Thanh khoản căng, lãi suất huy động tăng | Siết room, tăng OMO rate | 2022 H1 |
| **Đỏ** | Credit growth > Deposit growth >6% hoặc credit tăng trong khi deposit giảm | Khủng hoảng thanh khoản tiềm ẩn | Can thiệp mạnh, bơm thanh khoản, có thể tăng lãi suất điều hành | Q4/2022 (SCB crisis) |

**Các chỉ báo bổ sung khi divergence xảy ra:**
1. **Lãi suất liên ngân hàng (interbank rate):** Tăng vọt trên lãi suất điều hành → stress thanh khoản.
2. **Lãi suất huy động kỳ hạn dài (>12 tháng):** Tăng nhanh hơn huy động ngắn hạn → bank đang "cố" giữ vốn.
3. **Mua/bán TPCP của NH:** Nếu NH bán TPCP → cần tiền mặt; nếu mua → dư tiền.
4. **Nợ vay ngoại tệ của NH:** Tăng đột biến → đang vay quốc tế bù đắp thiếu hụt VND.

---

## 5. Chỉ báo Dẫn trước NPL (NPL Leading Indicators)

NPL báo cáo của NHNN là **con số trễ (lagging)** — nó phản ánh tình trạng tín dụng 6-12 tháng trước. Để dự báo NPL sớm hơn, cần theo dõi các chỉ báo dẫn trước:

### 5.1 Nhóm Nợ Quá hạn 91-180 ngày (Overdue loans 91-180 days)
- **Logic:** Khoản vay quá hạn 90 ngày thường sẽ chuyển thành nợ xấu (nhóm 3-5) trong 1-2 quý tới.
- **Dữ liệu:** NHNN không công bố chi tiết theo nhóm quá hạn. FiinTrade và broker report (Vietcap, ACBS) có ước tính riêng cho từng ngân hàng.
- **Theo dõi:** So sánh tốc độ tăng overdue 91-180d / tổng tín dụng giữa các quý.

### 5.2 Nợ Tái cơ cấu (Restructured Loans)
- **Logic:** Nợ tái cơ cấu là NPL "bị giấu" — DN không đủ khả năng trả đúng hạn nhưng được ngân hàng giãn thở. Khi tái cơ cấu hết hiệu lực, một tỷ lệ lớn sẽ chuyển thành NPL.
- **Thông tư 01/2020:** Cho phép tái cơ cấu nợ mà không chuyển nhóm nợ. Số liệu chính xác không công bố, nhưng ước tính của broker: ~10-15% tổng tín dụng tại đỉnh 2021-2022.
- **Thông tư 02/2023:** Gia hạn cơ chế tái cơ cấu đến hết 2023. Hiện tại (2024-2025), các khoản nợ tái cơ cấu đang dần hết hạn.

### 5.3 Nợ Nhóm 2 (Special Mention Loans)
- **Logic:** Nhóm 2 là nợ quá hạn 10-90 ngày. Tỷ lệ chuyển từ nhóm 2 lên nhóm 3-5 thường 30-50% trong 12 tháng.
- **Dữ liệu:** NHNN công bố theo bảng cân đối ngân hàng hàng quý. Tuy nhiên, cần cross-check với báo cáo tài chính riêng lẻ của từng ngân hàng trên FiinTrade.

### Ma trận Chỉ báo NPL Dẫn trước × Khung Thờii gian

| Chỉ báo | Lead time trước NPL báo cáo | Nguồn dữ liệu | Độ tin cậy | Ghi chú |
|---|---|---|---|---|
| **Nợ quá hạn 91-180 ngày** | 1-2 quý | BCTC ngân hàng (FiinTrade) | Cao | Tín hiệu sớm nhất nhưng không phải NH nào cũng công bố rõ |
| **Nhóm 2 / Special mention** | 2-4 quý | BCTC ngân hàng + NHNN | Cao | Tín hiệu chuẩn; cần theo dõi trend chứ không chỉ level |
| **Nợ tái cơ cấu / Thông tư 01** | 3-6 quý (sau khi hết hiệu lực) | BCTC ngân hàng + ước tính broker | Trung bình | Số liệu không minh bạch; phụ thuộc vào chính sách gia hạn |
| **Lãi suất quá hạn trung bình** | 1-2 quý | BCTC ngân hàng | Trung bình | Indicator bị ảnh hưởng bởi chính sách tái cơ cấu |
| **Tỷ lệ bao phủ nợ xấu (LLR)** | Đồng thờii/trễ | BCTC ngân hàng | Cao | LLR giảm = bank đang "chạy" dự phòng để che NPL |
| **Giá trái phiếu BĐS thứ cấp** | 2-4 quý | VBMA, giao dịch OTC | Trung bình | Giá < 70 par = distress; < 50 par = default risk cao |
| **Thanh khoản BĐS (giao dịch sơ cấp)** | 2-4 quý | Sở Xây dựng, CBRE, JLL | Trung bình | Giao dịch giảm → DN BĐS không có tiền trả nợ |

---

## 6. Phân hóa Hành vi: SOE Bank vs Private JSB

### 6.1 Tổng quan Cấu trúc Ngành Ngân hàng Việt Nam

| Chỉ tiêu (2024 ước tính) | SOE Bank (VCB, CTG, BID, Agribank) | Private JSB | Nước ngoài (100% vốn) |
|---|---|---|---|
| **Thị phần tài sản** | ~45-50% | ~40-45% | ~8-10% |
| **Thị phần tín dụng** | ~45% | ~45% | ~8% |
| **Số lượng NH** | 4 | ~20 | ~9 |
| **Tỷ lệ NPL trung bình** | Thấp hơn JSB ~0.5-1.0% [DỮ LIỆU THIẾU] | Cao hơn SOE ~0.5-1.5% | Thấp nhất (rủi ro thấp, khách hàng FDI) |
| **ROE trung bình** | ~18-22% (VCB cao nhất) | ~15-20% (phân hóa lớn) | ~10-15% |
| **CASA ratio** | VCB cao (~30%+), CTG/BID thấp hơn | TCB cao (~35%+), ACB ~30%, các JSB khác thấp hơn | Cao (khách hàng doanh nghiệp) |

### 6.2 Phân bổ Room Tín dụng

| Khía cạnh | SOE Bank | Private JSB |
|---|---|---|
| **Cơ chế phân bổ** | Ưu tiên dựa trên vai trò chính sách + CAMELS | Hoàn toàn dựa trên CAMELS + CAR + NPL |
| **Độ ổn định room** | Cao — ít bị cắt giảm đột ngột | Thấp — có thể bị siết mạnh nếu NPL tăng hoặc CAR giảm |
| **Khả năng vượt room** | Khó — bị giám sát chặt | Có thể thông qua công ty con, liên kết |
| **Room dự trữ (buffer)** | Thường có do tăng trưởng chậm hơn JSB | Ít — JSB thường dùng hết room nhanh |
| **Ví dụ 2024** | VCB được giao room ~14-15%; BID, CTG tương tự | TCB, MBB, ACB được giao room ~14-16%; một số JSB nhỏ bị giới hạn ~10-12% |

### 6.3 Con Đường Tăng Vốn (Recapitalization) Trong Khủng hoảng

| Phương thức | SOE Bank | Private JSB |
|---|---|---|
| **Vốn nhà nước** | Trực tiếp bơm vốn qua Bộ Tài chính/SCIC. Ví dụ: BIDV nhận vốn nhà nước nhiều lần | Không có |
| **Phát hành cổ phiếu ra công chúng** | Có, nhưng bị ràng buộc quy trình (phải qua Thủ tướng nếu nhà nước giảm tỷ lệ sở hữu) | Chủ động hơn. TCB, MBB, ACB phát hành thường xuyên |
| **Phát hành trái phiếu chuyển đổi** | Ít phổ biến | Phổ biến hơn, đặc biệt JSB cần vốn nhanh |
| **Chia cổ tức bằng cổ phiếu** | Cả hai nhóm đều dùng | Cả hai nhóm đều dùng |
| **Tốc độ recapitalization** | Chậm (quy trình hành chính) | Nhanh hơn (quyết định ĐHĐCĐ) |
| **Khả năng chịu đựng stress** | Cao hơn do "đệm" nhà nước | Phụ thuộc vào chất lượng tài sản và khả năng huy động vốn |

### 6.4 Nhiệm vụ Cho vay Chính sách (Policy Loan Mandate)

| Nội dung | Chi tiết |
|---|---|
| **Vai trò của SOE bank** | VCB, BID, CTG (và Agribank) là công cụ chính sách của Chính phủ. Khi có gói kích thích hoặc gói cứu trợ, SOE bank phải thực thi |
| **Ví dụ gói COVID-19** | Gói 16.000 tỷ VND (lãi suất 0%) — VCB và BID là đầu mối phân phối chính |
| **Cho vay SOE lớn** | VCB, BID, CTG có tỷ lệ cho vay SOE/Nhà nước cao hơn JSB. Điều này vừa là rủi ro (hiệu quả SOE thấp) vừa là điểm tựa (không dễ default) |
| **Tác động lên chu kỳ** | Khi NHNN muốn kích thích, SOE bank được "bật" trước → tín dụng tăng nhanh hơn ở giai đoạn Early Cycle |
| **Tác động lên ROE** | Cho vay chính sách thường lãi suất thấp hơn thị trường → nén biên lợi nhuận. Tuy nhiên, SOE bank bù đắp bằng chi phí huy động thấp |

### 6.5 CAR Buffer Trước Basel III

| Bank | CAR 2023-2024 (ước tính) | CET1 Ratio (ước tính) | Đánh giá khả năng đáp ứng Basel III |
|---|---|---|---|
| **VCB** | ~11-12% | ~10-11% | **Rất tốt** — dư vốn, có thể tăng trưởng 15%+ mà không cần tăng vốn |
| **BID** | ~9-10% | ~8-9% | **Khá** — cần tăng vốn để đáp ứng Tier-1 chất lượng cao hơn |
| **CTG** | ~9-10% | ~8-9% | **Khá** — tương tự BID, đã phát hành cổ phiếu gần đây |
| **Agribank** | [DỮ LIỆU THIẾU] | [DỮ LIỆU THIẾU] | Chưa niêm yết, số liệu không minh bạch |
| **TCB** | ~11% | ~10% | **Tốt** — CAR cao, nhưng cần duy trì |
| **ACB** | ~10-11% | ~9-10% | **Tốt** — một trong những JSB có CAR tốt nhất |
| **MBB** | ~10% | ~9% | **Khá** — cần quản lý tăng trưởng |
| **VPB** | ~9% | ~8% | **Trung bình** — áp lực tăng vốn nếu tăng trưởng nhanh |
| **JSB nhỏ** | <9% | <8% | **Yếu** — có nguy cơ bị siết room, sáp nhập |

**Lộ trình Basel III Việt Nam:**
- **2024-2025:** Áp dụng các quy định vốn nâng cao, tăng CAR tối thiểu dần.
- **2026-2028:** Hoàn thiện Tier-1 chất lượng cao (CET1), loại bỏ dần hybrid capital.
- **Hàm ý:** JSB có CAR thấp sẽ phải giảm tốc độ tăng trưởng tín dụng hoặc phát hành cổ phiếu. SOE bank có lợi thế cạnh tranh rõ rệt.

---

## 7. Nguồn Dữ liệu và Công cụ Theo dõi

### 7.1 Nguồn Chính thức

| Nguồn | URL | Dữ liệu core | Tần suất | Độ tin cậy |
|---|---|---|---|---|
| **NHNN Thống kê Ngân hàng** | `https://www.sbv.gov.vn/webcenter/portal/` → Thống kê | Tăng trưởng tín dụng, tiền gửi, LDR, NPL, M2, lãi suất | Hàng tháng (T+20-25 ngày) | **Tier S** |
| **GSO** | `https://www.gso.gov.vn/` | GDP, CPI, IIP, bán lẻ | Hàng tháng/quý | **Tier S** |
| **MOF** | `https://mof.gov.vn/` | Ngân sách, nợ công, phát hành TPCP | Hàng tháng/quý | **Tier S** |

### 7.2 Nền tảng Dữ liệu Thương mại

| Nguồn | URL/Ticker | Dữ liệu core | Chi phí | Độ tin cậy |
|---|---|---|---|---|
| **FiinTrade Bank Dashboard** | `fiintrade.vn` / Tickers: VCB, CTG, BID, TCB, VPB, MBB, ACB, MSB | BCTC quý, CAR, NPL, LDR, ROE, CASA, credit growth, deposit growth | ~15-30 triệu VND/năm | **Tier 1** |
| **FiinPro** | `fiingroup.vn` | Screening ngân hàng, so sánh đa công ty, phân tích ngành | ~40-80 triệu VND/năm | **Tier 1** |
| **Vietstock** | `vietstock.vn` | Tin tức ngân hàng, BCTC cơ bản, báo cáo broker | Free/Premium | **Tier B** |
| **FireAnt** | `fireant.vn` | Dữ liệu ngân hàng, so sánh, biểu đồ | Free/Premium | **Tier B+** |

### 7.3 Nghiên cứu Broker và Think-tank

| Nguồn | Ticker/Access | Đặc thù | Độ tin cậy |
|---|---|---|---|
| **Vietcap (VCSC)** | `vcsc.com.vn` | Macro + Ngân hàng mạnh nhất. Ước tính NPL điều chỉnh (adjusted NPL) chi tiết | **Tier 1** |
| **ACBS** | `acbs.com.vn` | Ngân hàng + Chiến lược. Conservative, phù hợp anchor kỳ vọng | **Tier 1** |
| **MBS** | `mbs.com.vn` | Ngân hàng, Derivatives. Commentary hữu ích | **Tier 1** |
| **SSI Research** | `ssi.com.vn` | Coverage rộng, data nội bộ tốt | **Tier 1** |
| **BSC (BIDV Securities)** | `bsc.com.vn` | Data SOE/ngân hàng quốc doanh tốt, nhưng bias "chính thức" | **Tier 1-** |
| **VEPR** | `vepr.org.vn` | Quarterly macro report, GDP forecast độc lập, banking monitor | **Tier A+** |
| **IMF Article IV** | `imf.org` | Đánh giá độc lập về NPL, CAR, fiscal space | **Tier S** |
| **World Bank** | `worldbank.org` | Vietnam Macro Poverty Outlook, credit gap, structural analysis | **Tier S** |

### 7.4 Checklist Theo dõi Chu kỳ Tín dụng (Monthly)

| STT | Chỉ số | Nguồn | Ngưỡng cảnh báo | Tần suất check |
|---|---|---|---|---|
| 1 | Tăng trưởng tín dụng YTD | NHNN | >16% hoặc <8% | Hàng tháng |
| 2 | Tăng trưởng tiền gửi YTD | NHNN | Divergence >4% so với tín dụng | Hàng tháng |
| 3 | LDR hệ thống | NHNN | >85% | Hàng tháng |
| 4 | NPL báo cáo | NHNN | >2.5% | Hàng tháng |
| 5 | Nhóm 2 / Special mention | BCTC ngân hàng (FiinTrade) | Tăng >20% QoQ | Hàng quý |
| 6 | NPL điều chỉnh (Vietcap) | Vietcap Reports | >7% | Hàng quý |
| 7 | Room tín dụng còn lại | NHNN + ACBS estimate | <20% room còn lại giữa năm | Hàng tháng |
| 8 | Tín dụng BĐS / Tổng tín dụng | NHNN | >25% | Hàng tháng |
| 9 | Lãi suất liên ngân hàng | NHNN | >1.5x refinancing rate | Hàng tuần |
| 10 | CAR theo bank | FiinTrade / BCTC | Tiến gần trần Basel III | Hàng quý |
| 11 | TPDN BĐS đáo hạn 12M | VBMA + FiinTrade | >100.000 tỷ VND đáo hạn | Hàng tháng |
| 12 | Giá TPDN BĐS thứ cấp | VBMA + OTC market | <70 par | Hàng tuần |

---

## 8. Cross-References và Framework Liên kết

| Framework | Tác giả | Ứng dụng trong Module này | Vị trí liên kết |
|---|---|---|---|
| **Bank Capital & Liquidity** | Thakor-Yu (2024) | Giải thích tại sao Basel III ảnh hưởng khác nhau giữa SOE bank (dễ recap) và JSB (phụ thuộc thị trường vốn) | `framework-thakor-yu-2024.md` |
| **Bank Lending Channel** | Kashyap-Stein (2000) | Room tín dụng của NHNN là "administrative lending channel" — cắt giảm/gia tăng room tác động khác nhau lên bank lớn vs bank nhỏ | `framework-kashyap-stein-2000.md` |
| **Financial Instability Hypothesis** | Minsky (1986) | Chu kỳ tín dụng VN 2020-2022 là case study điển hình: hedge financing → speculative financing (TPDN BĐS) → Ponzi (margin, đầu cơ) → bust | `framework-minsky-1986.md` |
| **Leverage Cycle** | Geanakoplos (2010) | BĐS VN là leverage cycle điển hình: giá BĐS tăng → collateral value tăng → vay được nhiều hơn → giá tăng tiếp → bust ngược lại | `framework-geanakoplos-2010.md` |
| **Global Financial Cycle** | Rey (2015) | Dòng vốn FDI/FII vào VN ảnh hưởng trực tiếp đến thanh khoản ngân hàng và khả năng tăng trưởng tín dụng | `framework-rey-global-financial-cycle.md` |
| **Regime Framework v1.1** | OPVIA | Chu kỳ tín dụng là input chính để xác định regime (R1-R5). Credit growth <10% + NPL tăng = R5; credit growth >15% + LDR cao = R3 | `framework-regime-v11.md` |
| **Monetary Policy NHNN** | OPVIA | Room tín dụng là công cụ chính sách tiền tệ #2 của NHNN (sau lãi suất). Hiểu credit cycle = hiểu 50% phản ứng của NHNN | `macro-vn-monetary-policy-nhnn.md` |
| **Transmission Channels** | OPVIA | Kênh tín dụng (credit channel) là kênh truyền dẫn mạnh nhất ở VN. Biến động tín dụng ảnh hưởng trực tiếp đến GDP, BĐS, và CK | `macro-vn-transmission-channels.md` |

---

## 9. Tự Phản biện và Giới hạn Dữ liệu

### 9.1 Dữ liệu Chưa Đầy đủ / Cần Cross-check

| Khoảng trống | Mô tả | Kế hoạch lấp đầy |
|---|---|---|
| **NPL thực vs báo cáo** | NHNN không công bố nhóm 2 theo thờii gian thực. NPL điều chỉnh của broker là ước tính | Dùng Vietcap + ACBS adjusted NPL; tự tính từ BCTC ngân hàng nếu cần |
| **Tái cơ cấu Thông tư 01** | Số liệu chính xác không công bố. Chỉ có ước tính | Theo dõi BCTC ngân hàng dòng "nợ tái cơ cấu"; ghi chú giả định |
| **Exposure BĐS gián tiếp** | NHNN chỉ công bố tín dụng trực tiếp BĐS (~20-22%). Exposure gián tiếp qua collateral không có số liệu chính thức | Dùng ước tính broker (~50-60% tổng tín dụng có liên quan BĐS); flag rõ là ước tính |
| **CAR theo Basel III** | VN đang trong lộ trình áp dụng. Số liệu CAR hiện tại vẫn dùng định nghĩa cũ (VAS) | Theo dõi thông báo NHNN về Basel III; điều chỉnh khi có số liệu CET1 chuẩn mới |
| **LDR chính xác theo tháng** | NHNN công bố LDR hàng tháng nhưng có độ trễ | Dùng số liệu NHNN chính thức; không dùng ước tính thay thế |
| **TPDN BĐS nợ xấu** | Không có số liệu tổng hợp chính thức. VBMA có số liệu phát hành nhưng không có default rate | Tổng hợp từ báo cáo broker + theo dõi các vụ default công khai |

### 9.2 Giả định Quan trọng

1. **SOE bank chiếm ~45% tài sản:** Con số này dựa trên ước tính của broker (Vietcap, ACBS) và không bao gồm Agribank (chưa niêm yết, số liệu không minh bạch). Nếu tính Agribank, tỷ lệ có thể lên ~50-55%.
2. **NPL điều chỉnh cao gấp 2-3x NPL báo cáo:** Đây là ước tính phổ biến của broker nhưng không phải ground truth. Mỗi ngân hàng có chất lượng tài sản khác nhau.
3. **Basel III timeline 2024-2028:** Dựa trên thông báo của NHNN. Có thể bị trì hoãn nếu kinh tế suy giảm.

---

## 10. Kết luận và Hàm ý Đầu tư

### 10.1 Vị trí Hiện tại (2025)
- **Pha chu kỳ:** Mid Cycle (Expansion) đang chuyển sang Late Cycle.
- **Tín dụng:** Tăng trưởng 14-15%, tiến gần trần room. LDR ~85%.
- **Rủi ro chính:** (1) Basel III làm phân hóa ngành ngân hàng mạnh hơn; (2) TPDN/BĐS tái cơ cấu chưa xong; (3) NPL ẩn từ Thông tư 01 đang dần lộ ra.

### 10.2 Hàm ý Đầu tư Theo Nhóm Ngân hàng

| Nhóm | Triển vọng | Lý do | Rủi ro |
|---|---|---|---|
| **SOE Bank (VCB, BID, CTG)** | **Tích cực** | CAR cao, dễ recap, được ưu tiên room, chi phí huy động thấp | Tăng trưởng chậm hơn JSB, cho vay chính sách nén biên |
| **JSB lớn (TCB, ACB, MBB)** | **Trung tính-tích cực** | Quản trị tốt, CAR khá, thị phần tăng | Cần tăng vốn để đáp ứng Basel III, cạnh tranh gay gắt |
| **JSB trung (VPB, MSB, HDB)** | **Trung tính** | Tăng trưởng nhanh nhưng CAR căng | NPL có thể tăng nhanh hơn nếu BĐS tiếp tục khó khăn |
| **JSB nhỏ / yếu** | **Tiêu cực** | CAR thấp, thị phầng giảm, bị siết room | Nguy cơ sáp nhập hoặc phá sản có kiểm soát |

### 10.3 Signpost Cần Theo dõi (6 tháng tới)

1. **Q1-Q2/2025:** Tăng trưởng tín dụng YTD có vượt 15% không? Nếu có → Late Cycle confirmed.
2. **Basel III timeline:** NHNN có công bố lộ trình cụ thể hơn không? CAR yêu cầu tăng bao nhiêu?
3. **NPL Q4/2024-Q1/2025:** NPL báo cáo có tăng vọt khi Thông tư 01 hết hiệu lực không?
4. **Room tín dụng 2025:** NHNN giao room như thế nào? SOE bank có được ưu tiên hơn không?
5. **TPDN BĐS đáo hạn 2025-2026:** Maturity wall lớn nhất vào thờii điểm nào? Có khả năng default hàng loạt không?

---

> **Document Control**
> - Version: v1.0 (Wave 4 — Lane 9)
> - Ngày: 2026-04-19
> - Author: Wave 4 Lane 9 (Kimi CLI)
> - Approver: OPVIA
> - Next review: 2026-05-19 (sau khi NHNN công bố thống kê ngân hàng tháng 4/2025)
> - Related modules: macro-vn-monetary-policy-nhnn.md, macro-vn-liquidity-systems.md, framework-thakor-yu-2024.md, framework-kashyap-stein-2000.md, framework-regime-v11.md, fixed-income/credit-spreads-vn.md
> - Data sources: NHNN (sbv.gov.vn), FiinTrade (fiintrade.vn), VEPR (vepr.org.vn), Vietcap (vcsc.com.vn), ACBS (acbs.com.vn), IMF Article IV Vietnam
