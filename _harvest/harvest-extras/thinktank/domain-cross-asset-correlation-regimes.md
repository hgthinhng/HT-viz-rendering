---
title: "Domain Cross-Asset Correlation Regimes — Stable vs Regime-Shift Correlation, Rolling-Window, Breakpoint Detection"
module_type: "domain"
file_name: "domain-cross-asset-correlation-regimes.md"
purpose: "Cung cấp khung phân tích correlation đa tài sản theo regime: khi nào correlation ổn định, khi nào nó phá vỡ, cách tính rolling-window (30d/90d/252d), và phương pháp breakpoint detection (CUSUM, Bai-Perron) áp dụng cho VN equity, USD/VND, rates, oil, DXY, gold, CNY."
primary_triggers:
  - "correlation regime"
  - "rolling correlation"
  - "correlation breakdown"
  - "correlation phá vỡ"
  - "regime shift correlation"
  - "ma trận tương quan đa tài sản"
  - "cross-asset correlation VN"
  - "breakpoint detection"
  - "dynamic conditional correlation"
when_to_use:
  - "Khi phân tích 'VN-Index có còn correlate với DXY như cũ không'."
  - "Khi đánh giá risk của portfolio multi-asset dựa trên correlation giả định."
  - "Khi xác định regime shift: correlation cấu trúc thay đổi hay chỉ nhiễu ngắn hạn."
  - "Khi anchor phân tích cross-asset vào framework-regime-v11 thông qua correlation state."
when_not_to_use:
  - "Không dùng làm signal mua/bán — correlation chỉ là lens diagnostic."
  - "Không dùng cho tài sản có data quality kém (<1 năm lịch sử hoặc liquidity gap lớn)."
  - "Không dùng thay thế factor analysis khi câu hỏi là nguyên nhân gốc."
related_modules:
  - "framework-regime-v11.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
  - "domain-cross-asset-risk-on-off.md"
  - "domain-cross-asset-transmission-channels.md"
  - "workflow-cross-asset-linkage.md"
  - "macro-vn-transmission-channels.md"
authoritative_citations:
  - "Engle, R. F. Dynamic Conditional Correlation (2002)."
  - "Bai, J. and Perron, P. Computation and Analysis of Multiple Structural Change Models (2003)."
  - "Forbes, K. J. and Rigobon, R. No Contagion, Only Interdependence (2002)."
  - "Longin, F. and Solnik, B. Extreme Correlation of International Equity Markets (2001)."
output_owner: "Analytical lens only; workflow-cross-asset-linkage.md owns output contract khi cần delivery."
---

# Domain Cross-Asset Correlation Regimes — Chế độ tương quan đa tài sản

Purpose: Codify cách OPVIA Sigma đọc correlation đa tài sản như một biến số động, không phải hằng số. Correlation giữa VN-Index và các biến global (DXY, oil, gold, CNY, US 10Y real yield) thay đổi theo regime, và việc dùng correlation trung bình lịch sử cho mọi period là sai lầm phân tích nghiêm trọng nhất trong cross-asset research.

Trigger keywords: rolling correlation, DCC-GARCH, correlation regime, correlation breakdown, structural break, Bai-Perron, CUSUM, cross-asset VN, correlation phá vỡ, tương quan động.

---

## 1. NGUYÊN TẮC CỐT LÕI — CORRELATION KHÔNG BAO GIỜ LÀ HẰNG SỐ

### 1.1 Ba trạng thái correlation

| Trạng thái | Đặc điểm | Ví dụ VN |
|---|---|---|
| **Stable regime** | Correlation ổn định trong một range hẹp (±0.1) qua 6-12 tháng | VN-Index vs US 10Y nominal yield trong giai đoạn Fed hold 2024 Q2-Q3: rolling 90d corr ~-0.15 ổn định |
| **Drift regime** | Correlation trôi dần theo hướng có ý nghĩa (>0.2 trong 3-6 tháng) | USD/VND vs CNY: correlation tăng từ 0.3 (2022) lên 0.6 (2024) khi CNY yếu đi và trade linkage tăng |
| **Rupture regime** | Correlation đổi dấu hoặc nhảy >0.4 trong <1 tháng | VN-Index vs gold: từ -0.2 (risk-on bình thường) sang +0.3 (Q1-2026 khi cả hai cùng tăng do geopolitical premium + liquidity rẻ) |

Quy tắc phân tích: **luôn nêu rõ correlation đang ở state nào**, dùng window nào để đo, và điều kiện nào làm nó phá vỡ.

### 1.2 Tại sao correlation thay đổi

| Driver | Cơ chế | Impact lên correlation |
|---|---|---|
| Regime shift global | Fed pivot, USD cycle turn, China stimulus | Correlation cross-border reset |
| Liquidity shock | Funding stress, margin call | "Correlation goes to 1" — mọi risk asset sell cùng lúc |
| Structural break VN | FOL change, Basel III, short-selling | Correlation VN vs EM peers reset |
| Sector composition | Weight banks/BĐS thay đổi | VN-Index vs rates correlation tăng |
| Narrative shift | Gold = safe haven vs gold = inflation hedge | Gold vs real yield decouple |

---

## 2. METHODOLOGY — ROLLING WINDOW

### 2.1 Lựa chọn window

| Window | Use case | Ưu | Nhược |
|---|---|---|---|
| **30d** | Tactical, detect rupture | Phản ứng nhanh với regime shift | Nhiễu cao, false signal |
| **90d (quarterly)** | **Primary OPVIA default** | Cân bằng signal/noise | Lag 1-1.5 tháng với rupture |
| **252d (yearly)** | Strategic, baseline correlation | Ổn định, loại nhiễu | Miss regime shift trong năm |
| **3y / 5y** | Long-run structural | So sánh vs "normal" | Che giấu structural break |

Quy tắc OPVIA: **báo cáo song song 30d và 90d**. Khi 30d và 90d lệch nhau >0.3 → signal regime shift đang diễn ra, cần deep-dive.

### 2.2 Pearson vs Spearman vs Kendall

- **Pearson** (linear): Default cho returns daily, ổn định khi distribution gần normal.
- **Spearman** (rank): Robust với outlier, tốt cho period có tail event.
- **Kendall tau**: Ổn định nhất nhưng computational cost cao.

OPVIA default: Pearson trên log returns. Khi có shock event (chiến tranh, default corporate lớn) → bổ sung Spearman để cross-check.

### 2.3 DCC-GARCH (Dynamic Conditional Correlation)

Khi cần correlation **có điều kiện vào volatility state**: dùng DCC-GARCH của Engle (2002). Model này giả định correlation thay đổi theo thời gian và có thể jump khi volatility tăng. Dùng DCC khi:
- Cần backtest hedge ratio động.
- Cần tách "baseline correlation" vs "crisis correlation".
- Khi phân tích contagion (Forbes-Rigobon: phân biệt contagion vs interdependence).

Không dùng DCC cho daily brief — chi phí tính toán không justified.

---

## 3. BREAKPOINT DETECTION

### 3.1 CUSUM (Cumulative Sum)

CUSUM test trên rolling correlation: phát hiện khi mean correlation thay đổi đáng kể so với reference period. Ngưỡng: CUSUM statistic > 1.36 (95%) cho signal preliminary; > 1.63 (99%) cho confirmation.

Use case VN: detect khi VN-Index vs DXY correlation chuyển từ weakly negative (-0.15) sang moderately negative (-0.40) → signal DXY đang dominate flow regime.

### 3.2 Bai-Perron multiple breakpoint

Khi nghi ngờ có nhiều regime shift trong một period dài: dùng Bai-Perron để tìm **multiple structural breaks**. Ưu: không cần giả định số breakpoint trước. Nhược: đòi hỏi data >500 quan sát để stable.

Ví dụ áp dụng: phân tích USD/VND vs CNY correlation 2015-2026 sẽ tìm được 3-4 breakpoints (2015 CNY devaluation, 2018 trade war, 2022 Fed tightening, 2024 China stimulus).

### 3.3 Quandt-Andrews unknown breakpoint

Khi chỉ nghi ngờ **một** breakpoint nhưng không biết khi nào: Quandt-Andrews sup-Wald test. Đơn giản hơn Bai-Perron, phù hợp cho quick check trong research note.

---

## 4. BA PATTERN CORRELATION CRITICAL CHO VN

### 4.1 "Correlation goes to 1" trong stress

Trong regime **Tightening Stress** hoặc **Deleveraging** (xem framework-regime-v11.md), correlation giữa các risk asset tăng mạnh về 1. VN-Index, corporate bonds, BĐS, VND — tất cả sell cùng lúc. Gold và USD cash là 2 outlier duy nhất.

**Hàm ý**: diversification fails khi cần nhất. Portfolio "đa dạng hóa" dựa trên correlation trung bình sẽ drawdown nặng hơn kỳ vọng.

### 4.2 Asymmetric correlation (Longin-Solnik 2001)

Correlation khi market down **lớn hơn** correlation khi market up. Đặc biệt đúng cho:
- VN-Index vs MSCI EM: up-corr ~0.35, down-corr ~0.65.
- USD/VND vs USD/CNY: up-corr ~0.4, down-corr ~0.75 (CNY yếu pull VND yếu mạnh hơn CNY mạnh pull VND mạnh).

Dùng exceedance correlation (Longin-Solnik) để đo chính xác.

### 4.3 Decoupling period

Khi một biến đi ngược correlation history: đây là tín hiệu **structural break** hoặc **narrative shift** quan trọng. Ví dụ:
- Gold vs US real yield: correlation dài hạn -0.5, nhưng 2024-2026 → gần 0 (geopolitical premium override).
- VN-Index vs oil: từ +0.15 (producer-importer mix) sang -0.2 (oil như inflation tax) khi CPI gần trần.

---

## 5. QUY TRÌNH ÁP DỤNG TRONG RESEARCH

1. **Chọn window**: 30d + 90d song song.
2. **Đo correlation** giữa cặp biến quan tâm trên full history + recent window.
3. **So sánh** recent vs full: nếu lệch >0.3 → flag regime shift.
4. **Breakpoint test** (CUSUM cho preliminary, Bai-Perron cho deep-dive).
5. **Phân biệt** correlation drift vs rupture vs noise.
6. **Liên kết với regime**: correlation state hiện tại thuộc regime nào (framework-regime-v11.md §regime classification).
7. **Nêu rõ fact vs inference**: "correlation 90d -0.35" là fact; "regime shift đang diễn ra" là inference cần trigger xác nhận.

---

## 6. CẢNH BÁO — ĐIỀU KHÔNG ĐƯỢC LÀM

- Không kết luận causation từ correlation. Correlation bằng 0.7 không có nghĩa biến A drive biến B.
- Không dùng correlation trung bình lịch sử cho period stress — dùng stressed correlation matrix.
- Không ignore non-stationarity. Correlation rolling-90d thay đổi qua thời gian là bình thường, không phải sai methodology.
- Không dùng correlation daily khi có data gap (holiday mismatch VN vs global) mà không xử lý lag.

---

## 7. CROSS-REFERENCES

- Regime classification: **framework-regime-v11.md**
- Ma trận linkage 10-node: **domain-cross-asset-linkage-matrix-vn.md**
- RORO indicators: **domain-cross-asset-risk-on-off.md**
- Transmission channels: **domain-cross-asset-transmission-channels.md**
- Workflow output: **workflow-cross-asset-linkage.md**
- VN transmission mechanism: **macro-vn-transmission-channels.md**
