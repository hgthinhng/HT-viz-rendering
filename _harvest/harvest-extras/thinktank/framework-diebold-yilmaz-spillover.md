---
title: "Framework Diebold-Yilmaz 2012 — Spillover Index, Volatility Connectedness, Forecast-Error Variance Decomposition"
module_type: "framework"
file_name: "framework-diebold-yilmaz-spillover.md"
purpose: "Codify Diebold-Yilmaz spillover và connectedness framework cho nhận diện nguồn shock cross-asset, đặc biệt VN equity, VN rates, VND, DXY, oil, CNY. Kimi P0."
primary_triggers:
  - "Diebold Yilmaz spillover"
  - "spillover index"
  - "volatility connectedness"
  - "forecast error variance decomposition"
  - "cross asset network"
  - "shock source identification"
  - "VN equity rates VND DXY oil CNY"
when_to_use:
  - "Định lượng connectedness giữa asset classes và xác định net transmitters versus net receivers."
  - "Phân tích một biến động VN là shock nội địa hay shock nhập khẩu từ global/regional factors."
  - "Xây dựng cross-asset linkage table cho regime monitoring."
when_not_to_use:
  - "Không dùng khi data frequency, liquidity, hoặc history quá yếu để hỗ trợ VAR estimation."
  - "Không coi connectedness là structural causality nếu thiếu diễn giải kinh tế."
related_modules:
  - "macro-vn-transmission-channels.md"
  - "framework-rey-global-financial-cycle.md"
  - "framework-brunnermeier-pedersen-2009.md"
  - "framework-regime-v11.md"
authoritative_citations:
  - "Diebold, F. X., & Yilmaz, K. (2012). Better to give than to receive: Predictive directional measurement of volatility spillovers. International Journal of Forecasting, 28(1), 57-66."
  - "Diebold, F. X., & Yilmaz, K. (2009). Measuring financial asset return and volatility spillovers, with application to global equity markets. Economic Journal, 119(534), 158-171."
  - "Diebold, F. X., & Yilmaz, K. (2014). On the network topology of variance decompositions: Measuring the connectedness of financial firms. Journal of Econometrics, 182(1), 119-134."
output_owner: "Analytical framework only; pair với cross-asset linkage, FX, rates, commodities, và regime modules cho output cuối."
---

# Framework Diebold-Yilmaz 2012 — Spillover Index & Connectedness

Purpose: Áp dụng Diebold-Yilmaz spillover index cho phân tích cross-asset Việt Nam. Giá trị chính là định lượng biến nào đang truyền shock, biến nào đang nhận shock, và connectedness có tăng vào regime stress hay không. Trigger keywords: spillover index, volatility connectedness, FEVD, VAR, shock source, net transmitter, VN equity, VN rates, VND, DXY, oil, CNY.

## 1. Authors & Source

**Francis X. Diebold and Kamil Yilmaz (2012).** "Better to give than to receive: Predictive directional measurement of volatility spillovers." *International Journal of Forecasting*, 28(1), 57-66.

Nguồn liên quan: **Diebold and Yilmaz (2009)** về return/volatility spillovers giữa equity markets toàn cầu; **Diebold and Yilmaz (2014)** về network topology của variance decompositions.

Trong OPVIA, "Diebold-Yilmaz" là connectedness framework dựa trên **forecast-error variance decomposition**, không phải correlation table thông thường. Output phải chỉ ra total connectedness, directional spillovers, net transmitter, net receiver và time variation.

## 2. Core thesis

Thị trường tài chính kết nối với nhau qua return shocks, volatility shocks, funding constraints, kỳ vọng và portfolio rebalancing. Correlation chỉ cho biết hai chuỗi có đi cùng nhau không; nó không cho biết bao nhiêu phần uncertainty của một biến đến từ shock của biến khác, và cũng không cho biết node nào đang truyền stress. Diebold-Yilmaz đưa ra cách đo vận hành được bằng variance decomposition từ vector autoregression.

Framework ước tính tỷ trọng forecast-error variance của từng biến được giải thích bởi shock của chính nó và shock từ các biến còn lại. Tổng các phần ngoài đường chéo tạo thành **total spillover index**, tức mức connectedness toàn hệ thống. Directional measures cho biết một node truyền bao nhiêu shock sang các node khác và nhận bao nhiêu shock từ hệ thống. Net spillover xác định node là transmitter hay receiver. Rolling estimation cho biết connectedness thay đổi qua thời gian, thường tăng mạnh khi regime stress xuất hiện.

Với Việt Nam, đây là Kimi P0 vì cross-asset analysis thường phải trả lời: VN equity, VN rates hay USD/VND đang bị kéo bởi yếu tố nội địa, hay bị nhập khẩu từ DXY, US yields, oil, CNY, VIX và regional risk? Một linkage matrix định tính là cần thiết nhưng chưa đủ. Diebold-Yilmaz biến matrix thành monitoring discipline. Mục tiêu không phải pseudo-precision; mục tiêu là giảm narrative overfitting. Nếu data nói DXY và CNY đang truyền phần lớn shock, memo không được giải thích USD/VND chỉ bằng câu chuyện local credit policy.

## 3. Key variables / mechanisms

**Forecast-error variance decomposition (FEVD):** object lõi. Với mỗi biến, FEVD đo share của forecast uncertainty đến từ shock của chính biến đó và từ các biến khác.

**Total spillover index:** tỷ lệ forecast-error variance toàn hệ thống đến từ cross-variable shocks thay vì own shocks. Giá trị cao nghĩa là connectedness cao và contagion risk lớn hơn.

**Directional spillover "to others":** lượng shock một node đóng góp vào uncertainty của các node khác. Cao nghĩa là shock transmitter.

**Directional spillover "from others":** lượng uncertainty của một node được giải thích bởi shock từ các node khác. Cao nghĩa là shock receiver.

**Net spillover:** "to others" trừ "from others". Dương là transmitter ròng; âm là receiver ròng.

**Pairwise spillover:** quan hệ directional giữa hai biến, ví dụ DXY -> USD/VND, oil -> VN rates, CNY -> VN equity.

**Rolling window:** estimation theo cửa sổ trượt để phát hiện regime shift. Connectedness trong calm regime có thể rất khác stress regime.

**Return versus volatility connectedness:** return spillover đo hướng giá; volatility spillover đo transmission của uncertainty. Với stress monitoring, volatility connectedness thường hữu ích hơn.

## 4. When to apply

Áp dụng cho **cross-asset linkage analysis**, nhất là khi nhiều narrative cùng hợp lý. Ví dụ: VN equity giảm, USD/VND tăng, oil spike, CNY yếu. Nguồn shock là Fed, dầu, Trung Quốc, local rates hay margin deleveraging? Diebold-Yilmaz cung cấp điểm bắt đầu có kỷ luật.

Dùng trong **regime transition**: Fed tightening, CNY devaluation pressure, oil shock, domestic bond stress, equity sell-off, liquidity squeeze. Connectedness tăng cho thấy các shock riêng lẻ có thể đang nhập thành một macro-financial shock.

Dùng để xây **monitoring dashboard**: VN equity, VN rates, USD/VND, DXY, oil, CNY, gold, US real yields, Asia credit spreads, foreign-flow proxies. Framework giúp xác định biến nào cần lên trang đầu Daily Brief.

Dùng cho **post-mortem và pre-mortem**. Sau shock, xác định đường truyền. Trước shock, hỏi node nào sẽ truyền nhanh nhất nếu bị stress.

Không dùng khi dữ liệu quá yếu. Một số yield VN có thanh khoản thấp; property prices tần suất thấp; corporate bond spread thiếu quan sát; USD/VND là tỷ giá quản lý. Input yếu sẽ tạo output có vẻ khoa học nhưng fragile.

## 5. How to apply (operationalized)

**Step 1: Define node set.** Network lõi cho VN:

| Node | Practical proxy |
|---|---|
| VN equity | VNINDEX return hoặc VN30 return |
| VN rates | thay đổi 2Y/5Y government bond yield, interbank O/N, hoặc deposit-rate proxy |
| VND | USD/VND spot return/change |
| DXY | Dollar index return |
| Oil | Brent return |
| CNY | USD/CNY hoặc proxy CFETS |

Expanded nodes: gold, US 10Y real yield, VIX, Asia HY spreads, copper, foreign equity flows.

**Step 2: Chọn transformation.** Dùng returns cho price series, yield changes cho rates, volatility nếu câu hỏi là stress transmission. Không trộn levels và returns nếu không có lý do rõ. Align holidays và xử lý stale prices.

**Step 3: Estimate VAR.** Chọn lag length bằng information criteria và judgment kinh tế. Với sample nhỏ, dùng parsimonious VAR hoặc shrinkage. Ghi rõ sample period, frequency, lag, forecast horizon.

**Step 4: Compute FEVD.** Ưu tiên generalized FEVD để giảm nhạy với thứ tự biến. Nếu dùng Cholesky ordering, phải công bố ordering và robustness.

**Step 5: Build spillover table.** Output cần FEVD matrix, total spillover index, directional "to", directional "from", và net spillover. Bảng phân rã quan trọng hơn một con số headline.

**Step 6: Run rolling windows.** Dùng 60, 120 hoặc 250 trading days tùy data quality. Mục tiêu là xem connectedness có tăng không và transmitter nào đổi vai.

**Step 7: Translate into OPVIA narrative.** Chỉ diễn giải sau table: transmitter hiện tại, receiver hiện tại, và điều kiện làm gãy interpretation. Ví dụ: "DXY là net transmitter; VN equity là receiver; confidence thấp nếu VN rates bị stale."

## 6. Limitations & critique

**Connectedness không phải structural causality.** FEVD đo predictive variance contribution, không chứng minh nguyên nhân kinh tế. Diễn giải phải gắn với mechanism.

**Data quality là constraint lớn ở Việt Nam.** Bond yields có thể illiquid, interbank rates phản ánh policy operation, USD/VND được quản lý, nhiều chuỗi có stale prints. Framework phải gắn data-quality label.

**Parameter instability thường xuyên.** Quan hệ đổi theo regime. Model estimate trên calm period có thể thất bại khi crisis; crisis window có thể overstate connectedness bình thường.

**Variable selection chi phối kết quả.** Bỏ CNY hoặc US real yields có thể làm DXY trông quá dominant; bỏ domestic rates có thể overstate equity-FX linkage. Node set phải khớp câu hỏi.

**High connectedness không luôn xấu.** Total index tăng có thể phản ánh global easing factor, không chỉ stress. Direction và macro context quyết định interpretation.

**Low frequency bỏ lỡ spillover nhanh.** Daily data có thể miss intraday FX intervention, offshore NDF và liquidity event đột ngột. Weekly data có thể smooth quá mức.

## 7. Linked frameworks

**Rey Global Financial Cycle:** Diebold-Yilmaz lượng hóa transmission mà Rey mô tả: Fed/DXY/VIX vào EM assets và policy constraints.

**Brunnermeier-Pedersen (2009):** dùng khi connectedness tăng vì funding liquidity và market liquidity khuếch đại nhau.

**Minsky (1986):** dùng khi connectedness spike làm lộ fragility tái cấp vốn trong credit markets.

**OPVIA Regime v1.1:** connectedness indicators nên feed vào regime classification: local regime, imported shock, global dollar squeeze, oil inflation shock, hoặc CNY-led regional stress.

**Kashyap-Stein (2000):** giúp diễn giải spillover từ rates/liquidity vào bank lending và equity.

## 8. OPVIA usage examples

**Case A: Network VN equity - VN rates - VND - DXY - oil - CNY.**  
SỰ KIỆN: Giả sử VN equity giảm, USD/VND tăng, VN rates nhích lên, oil tăng, DXY mạnh và CNY yếu. Memo định tính có thể chọn bất kỳ narrative nào theo prior của analyst: Fed, dầu, China hay local credit stress.

DIỄN GIẢI: Diebold-Yilmaz buộc tách correlation khỏi connectedness. Nếu rolling FEVD cho thấy DXY giải thích phần lớn forecast variance của USD/VND và VN equity, còn oil giải thích VN rates nhiều hơn equity, shock chính là global dollar tightening với inflation/rates channel phụ. Nếu CNY là net transmitter sang VND và VN equity, vấn đề là regional competitiveness và China risk, không chỉ Fed. Nếu VN rates truyền mạnh sang equity trong khi DXY yên, nguồn shock là local liquidity.

GIẢ THUYẾT: OPVIA output nên có table: transmitter = DXY/CNY; receiver = VN equity/VND; secondary = oil -> rates. Trigger theo dõi: total spillover index vượt rolling percentile band, cộng với DXY hoặc CNY chuyển thành net transmitter dương. Data gap: nếu VN government bond yields stale, dùng interbank O/N, deposit-rate proxy và T-bill yields để robustness check.

**Case B: Nhận diện nguồn shock trong oil spike.**  
SỰ KIỆN: Brent tăng mạnh vì geopolitical risk. VN equity yếu, USD/VND chịu áp lực, và inflation expectations tăng. Oil là narrative hiển nhiên, nhưng transmission có thể đi qua nhiều đường: import bill, CPI, Fed expectations, DXY hoặc risk-off.

DIỄN GIẢI: Spillover framework hỏi oil có trực tiếp truyền volatility sang VN assets không, hay oil làm tăng kỳ vọng lạm phát Mỹ, kéo US yields/DXY lên rồi mới đánh vào Việt Nam qua Global Financial Cycle. Nếu FEVD cho thấy oil -> VN rates cao nhưng oil -> VND thấp sau khi kiểm soát DXY, kênh chính là inflation/rates. Nếu DXY -> VND dominant, oil shock đã bị financialized qua USD. Nếu CNY cùng lúc thành transmitter, China demand và regional FX pressure có thể là kênh VN lớn hơn.

GIẢ THUYẾT: Cross-asset linkage memo không được viết "oil up equals VN down" nếu chưa chứng minh channel. Cấu trúc đúng là: shock source, transmission strength, receiver asset, confidence, data caveat. Thesis breaker: oil còn cao nhưng DXY yếu, CNY ổn và VN rates không tăng; khi đó equity impact nên được xem là sector-specific margin pressure hơn là broad macro contagion.

---
*OPVIA internal framework module. Research use only; no buy/sell/hold recommendation.*
