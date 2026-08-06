---
title: "Futures Curve Mechanics — Contango, Backwardation, Roll Yield, Term Structure Signals"
module_type: "domain"
file_name: "domain-commodities-futures-curve.md"
purpose: "Codify cơ chế định giá futures curve cho commodities: contango vs backwardation, roll yield, cách đọc term structure để suy luận về tồn kho và cầu, và cách sử dụng CFTC Commitment of Traders (COT) report để phân biệt positioning commercial vs speculative."
primary_triggers:
  - "contango backwardation"
  - "futures curve commodity"
  - "roll yield"
  - "term structure commodity"
  - "CFTC COT report"
  - "commercial net short speculative net long"
  - "inventory demand signal futures"
  - "curve steepening flattening commodity"
when_to_use:
  - "Khi phân tích cấu trúc giá futures của oil, gold, copper, coffee, hoặc bất kỳ commodity có futures market."
  - "Khi đánh giá cost-of-carry cho commodity ETFs, index funds, hoặc passive commodity exposure."
  - "Khi đọc CFTC COT để xác định liệu giá hiện tại được đẩy bởi commercial hedging hay speculative flow."
  - "Khi phân tích tồn kho toàn cầu (WTI crude, copper LME, coffee ICE) qua lens của curve shape."
when_not_to_use:
  - "Không dùng để dự báo giá spot — term structure là lens diagnostic, không phải predictive model."
  - "Không dùng cho commodities không có futures market sâu (ví dụ: gạo VN, cao su SVR spot)."
  - "Không thay thế phân tích cung-cầu cơ bản — curve là biểu hiện, không phải nguyên nhân."
related_modules:
  - "domain-commodities-soft.md"
  - "domain-commodities-vn-impact.md"
  - "domain-cross-asset-correlation-regimes.md"
  - "framework-regime-v11.md"
  - "reference-vn-data-sources.md"
authoritative_citations:
  - "Working, H. (1949) — Theory of the Price of Storage."
  - "Brennan, M. J. (1958) — The Supply of Storage."
  - "CFTC Commitment of Traders Report — methodology and weekly release."
  - "Gorton, G. and Rouwenhorst, K. G. (2006) — Facts and Fantasies about Commodity Futures."
  - "Till, H. and Eagleeye, J. (2017) — Commodity Trading Advisors."
output_owner: "workflow-deep-dive.md khi phân tích commodity futures hoặc ETF/commodity index exposure; workflow-cross-asset-linkage.md khi curve shape là một transmission channel."
---

# Futures Curve Mechanics — Contango, Backwardation, và Term Structure

**Mục đích:** Cung cấp khung operational để đọc futures curve như một biến số độc lập: shape (contango/backwardation) nói gì về tồn kho và cầu, roll yield ảnh hưởng thế nào đến returns, và positioning data (CFTC COT) phân biệt động lực giá.

**Trạng thái:** [FRAMEWORK — Áp dụng cho mọi commodity futures market]

---

## 1. CONTANGO VS BACKWARDATION — ĐỊNH NGHĨA VÀ CƠ CHẾ

### 1.1. Định nghĩa

| Trạng thái | Định nghĩa | Curve shape | Điều kiện thị trường |
|:---|:---|:---|:---|
| **Contango** | Futures giá > Spot giá; giá các tháng xa hơn cao hơn tháng gần | Upward sloping | Dồi dào (abundant inventory), cost-of-carry dương, thị trường không lo lắng về cung ngắn hạn |
| **Backwardation** | Futures giá < Spot giá; giá các thám xa hơn thấp hơn tháng gần | Downward sloping | Khan hiếm (scarcity), convenience yield cao, thị trường sẵn sàng trả premium cho giao ngay |
| **Flat** | Futures giá ≈ Spot giá qua các tenor | Horizontal | Chuyển tiếp giữa hai trạng thái, hoặc thị trường không có thông tin rõ ràng |

### 1.2. Cơ chế cost-of-carry

> **DIỄN GIẢI:** Futures price = Spot price + Cost-of-carry − Convenience yield.
> - **Cost-of-carry** = Lưu kho + Bảo hiểm + Chi phí tài chính (lãi vay) − Lợi tức (dividend, cho commodity thường = 0).
> - **Convenience yield** = Giá trị "có hàng trong tay" — khả năng đáp ứng đơn hàng đột xuất, tránh downtime sản xuất.

| Khi... | Cost-of-carry vs Convenience yield | Curve shape |
|:---|:---|:---:|
| Inventory dồi dào, không lo thiếu hàng | Cost-of-carry > Convenience yield | **Contango** |
| Inventory thấp, lo ngại đứt gãy cung | Convenience yield > Cost-of-carry | **Backwardation** |
| Inventory trung bình, kỳ vọng ổn định | Cost-of-carry ≈ Convenience yield | **Flat** |

> **SỰ KIỆN:** WTI crude tháng 4/2020 (COVID-19) — spot giá âm (-$37/bl) trong khi futures tháng 6 vẫn ~$20/bl. Đây là contango cực đoan do: (a) kho chứa Cushing đầy, (b) cost-of-carry → vô cực vì không còn chỗ chứa, (c) convenience yield = 0 do không ai cần dầu ngay.

---

## 2. ROLL YIELD — TÁC ĐỘNG LÊN RETURNS

### 2.1. Định nghĩa và dấu

Roll yield = Lợi nhuận/thua lỗ từ việc "roll" hợp đồng futures từ tháng gần đến tháng xa trước khi đáo hạn.

| Trạng thái curve | Roll yield | Impact holder long futures | Ví dụ |
|:---|:---:|:---|:---|
| **Contango** | Âm (negative roll) | Long futures mất tiền khi roll — bán tháng gần thấp, mua tháng xa cao | USO (WTI ETF) 2009–2014: contango sâu, tracking error âm 5–10%/năm so với spot |
| **Backwardation** | Dương (positive roll) | Long futures kiếm tiền khi roll — bán tháng gần cao, mua tháng xa thấp | WTI 2022 (sau xung đột Nga-Ukraine): backwardation mạnh, long futures outperform spot |
| **Flat** | ≈ 0 | Không có lợi thế/thiệt hại từ roll | — |

### 2.2. Roll yield trong commodity index investing

| Index / Vehicle | Hành vi roll | Độ nhạy với roll yield | Ghi chú |
|:---|:---|:---:|:---|
| **S&P GSCI** | Roll hàng tháng theo predetermined schedule | Cao — front-month heavy | Outperform trong backwardation, underperform trong contango sâu |
| **Bloomberg Commodity Index (BCOM)** | Roll 5-business-day window, 2nd-month biased | Trung bình | Ít nhạy cảm với front-month volatility hơn GSCI |
| **Single-commodity ETFs (USO, GLD)** | USO: roll monthly; GLD: không roll (physical-backed) | USO: cao; GLD: 0 | GLD không có roll risk vì nắm giữ vàng vật chất |
| **Commodity mutual funds VN** | Không có — VN chưa có futures market cho retail | N/A | Nhà đầu tư VN tiếp cận commodity qua equity proxy (DPM, GAS, HAG) hoặc offshore ETFs |

> **DIỄN GIẢI:** Roll yield là lý do tại sao "mua commodity futures để hedge lạm phát" là một proposition kém hiệu quả trong contango market. Nếu analyst đang xem xét exposure commodity qua futures-based ETF, phải kiểm tra curve shape trước — contango sâu có thể ăn mất 5–10% returns/năm ngay cả khi spot price đi ngang.

---

## 3. TERM STRUCTURE SIGNALS — ĐỌC TỒN KHO VÀ CẦU

### 3.1. Các dạng curve và ý nghĩa

| Curve shape | Ý nghĩa về inventory | Ý nghĩa về demand | Regime điển hình |
|:---|:---|:---|:---|
| **Steep contango (front thấp, back cao)** | Inventory rất cao, warehouse đầy | Demand yếu hoặc dự kiến phục hồi chậm | Recession, post-demand-shock (COVID 2020 Q2) |
| **Mild contango (slope nhẹ)** | Inventory trung bình-cao | Demand ổn định | Normal growth, supply ổn định |
| **Flat** | Inventory cân bằng | Demand = Supply ở mọi horizon | Transition hoặc uncertainty |
| **Mild backwardation (slope nhẹ âm)** | Inventory trung bình-thấp | Demand vượt supply nhẹ | Early cycle recovery |
| **Steep backwardation (front cao, back thấp)** | Inventory rất thấp, shortage | Demand mạnh hoặc supply disruption | War, sanction, crop failure |

### 3.2. Spread analysis — Leading indicator

| Spread | Cách tính | Ý nghĩa |
|:---|:---|:---|
| **First–Second Month Spread** | F1 − F2 | Liquidity tốt nhất, phản ứng nhanh với supply shock ngắn hạn |
| **First–Twelfth Month Spread** | F1 − F12 | Phản ánh kỳ vọng cân bằng cung-cầu 1 năm |
| **Calendar Spread (seasonal)** | Ví dụ: July corn − Dec corn | Phản ánh vụ mùa cụ thể (new crop vs old crop) |

> **SỰ KIỆN:** Coffee Arabica ICE (KC) tháng 12/2024 — F1-F6 spread chuyển từ contango $200/tấn (tháng 6) sang backwardation $150/tấn (tháng 12) khi Brazil báo cáo hạn hán nghiêm trọng ở Minas Gerais. Spread đảo chiều trước khi spot price tăng 25%, là tín hiệu sớm cho shortage.

### 3.3. Curve dynamics — Steepening vs Flattening

| Biến động | Định nghĩa | Diễn giải |
|:---|:---|:---|
| **Bear steepening** | Front giảm nhiều hơn back | Short-term supply dồi dào đột ngột hoặc demand collapse ngắn hạn |
| **Bull steepening** | Front tăng nhiều hơn back | Short-term supply shock hoặc demand surge ngắn hạn |
| **Bear flattening** | Back giảm nhiều hơn front | Kỳ vọng long-term supply tăng (new mine, new crop, shale expansion) |
| **Bull flattening** | Back tăng nhiều hơn front | Kỳ vọng long-term structural shortage (peak oil, reserve depletion) |

---

## 4. COMMERCIAL VS SPECULATIVE POSITIONING — CFTC COT REPORT

### 4.1. Cấu trúc CFTC COT

CFTC công bố hàng tuần (thứ Sáu, data đến thứ Ba) chia positioning thành 3 nhóm chính:

| Nhóm | Định nghĩa | Hành vi điển hình | Tín hiệu |
|:---|:---|:---|:---|
| **Commercial (Producer/Merchant)** | Doanh nghiệp có exposure vật chất (nông dân, mỏ, refinery) | Hedge: bán futures khi có hàng (short hedge), mua futures khi cần nguyên liệu (long hedge) | Net short = có hàng bán; Net long = cần mua. Commercial net short extremes = supply pressure thực |
| **Non-Commercial (Managed Money / Speculative)** | Quỹ hedge fund, CTA, speculative account | Theo đuổi momentum, trend-following, macro thesis | Net long extremes = greed, crowded long; Net short extremes = fear, capitulation |
| **Non-Reportable (Small traders)** | Position nhỏ hơn reporting threshold | Retail, noise | Ít predictive value |

### 4.2. Cách đọc COT như tín hiệu

| Tình huống | Commercial | Non-Commercial | Diễn giải | Confidence |
|:---|:---:|:---:|:---|:---:|
| **Bullish confirmation** | Net short giảm (covering) hoặc chuyển net long | Net long tăng | Cả hai phe đồng thuận giá tăng — nhưng cần cảnh giác crowded long | Medium |
| **Bullish divergence** | Net short giảm mạnh (smart money buying) | Net long giảm hoặc net short | Commercial — ngưới hiểu cơ bản nhất — đang mua vào khi spec bán | **High** |
| **Bearish confirmation** | Net short tăng (bán hedge mạnh) | Net short tăng | Đồng thuận giảm — thường khi supply dồi dào | Medium |
| **Bearish divergence** | Net short tăng (commercial bán) | Net long tăng (spec mua) | Spec đuổi theo rally nhưng "smart money" đang bán — warning sign | **High** |
| **Extreme positioning** | Commercial net short ở percentile 95%+ | Non-commercial net long ở percentile 95%+ | Market cực kỳ crowded — reversal risk cao, không phải entry mới | High (cho reversal) |

> **SỰ KIỆN:** WTI COT tuần 15/03/2022 — Non-commercial net long ở mức cao nhất 5 năm (percentile 98%) trong khi commercial net short cũng ở percentile 95%. Sau đó 4 tuần, giá WTI giảm 18% từ $123 về $101 khi spec bắt đầu profit-taking. Extreme positioning không dự báo thờii điểm reversal nhưng cảnh báo asymmetric risk.

### 4.3. COT — Limitations

| Limitation | Mô tả | Mitigation |
|:---|:---|:---|
| **Lag 3 ngày** | Data đến thứ Ba, công bố thứ Sáu | Dùng làm context, không làm trigger real-time |
| **Aggregation bias** | Commercial bao gồm cả swap dealer (goldman, jpm hedging cho clients) | Phân biệt "Producer/Merchant" vs "Swap Dealer" nếu có disaggregated COT |
| **Không phản ánh OTC** | Position qua OTC (forward, swap) không báo cáo CFTC | Dùng COT như proxy, không làm ground truth |
| **Regime-dependent** | Tín hiệu COT hoạt động khác trong trend mạnh vs range-bound | Kết hợp với curve shape và fundamental data |

---

## 5. ỨNG DỤNG CHO VN CONTEXT

### 5.1. VN không có futures market nội địa sâu — implications

| Điểm | Ý nghĩa |
|:---|:---|
| Không có VND-denominated commodity futures | Doanh nghiệp VN phải hedge qua offshore (ICE, NYMEX, LME) hoặc không hedge |
| FX risk thêm vào commodity risk | Mua futures USD-quoted + VND biến động = double exposure |
| Lack of price discovery nội địa | Giá nội địa (gạo, cà phê, cao su) phụ thuộc hoàn toàn vào giá thế giới + basis local |
| No roll yield for VN investors | NĐT VN không thể "earn roll yield" trực tiếp; phải qua offshore ETF hoặc equity proxy |

### 5.2. Equity proxies cho commodity exposure VN

| Commodity | Equity proxy VN | Futures curve relevance |
|:---|:---|:---|
| Oil / Gas | GAS, PVD, PVS, BSR | WTI/Brent curve shape ảnh hưởng revenue GAS (gas price linked to oil) |
| Gold | PNJ, SJC (không niêm yết) | Gold futures contango/backwardation ảnh hưởng margin PNJ (input cost) |
| Coffee | HAG (indirect), không có pure-play | ICE Robusta curve ảnh hưởng giá thu mua và margin xuất khẩu |
| Steel | HPG, HSG, NKG | Iron ore + HRC futures curve (SGX, SHFE) ảnh hưởng input cost |

> **DIỄN GIẢI:** Vì VN thiếu futures market nội địa, doanh nghiệp VN thường để exposure tự nhiên (natural hedge) hoặc dùng forward contract với ngân hàng. Điều này có nghĩa là: (a) margin biến động theo giá thế giới, (b) không có công cụ để lock giá dài hạn hiệu quả, (c) các công ty có dòng tiền USD tự nhiên (xuất khẩu) có lợi thế hedge ngầm.

---

## 6. CROSS-REFS VÀ TRIGGER WORKFLOW

| Khi ngưới dùng hỏi... | Load module... | Output contract |
|:---|:---|:---|
| "WTI đang contango hay backwardation? Ý nghĩa gì?" | Module này + `domain-commodities-vn-impact.md` | Deep-dive Memo |
| "COT report gold đang nói gì?" | Module này | Daily Brief / Linkage |
| "Mua USO có bị roll yield âm không?" | Module này + `framework-regime-v11.md` | Deep-dive Memo |
| "Giá cà phê futures tăng ảnh hưởng margin HAG?" | Module này + `domain-commodities-soft.md` | Linkage Analysis |

---

*Module version: 0.1.0 | Shelf life: 12 tháng (framework stable).*
*Cross-check với: CFTC COT (hàng tuần), ICE/NYMEX/LME curve data (hàng ngày), BCOM/GSCI roll schedules (hàng tháng).*
