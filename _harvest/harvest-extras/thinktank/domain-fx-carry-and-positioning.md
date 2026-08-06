---
title: "Domain FX Carry and Positioning — VND Carry Context, Offshore Basis, FII Flows, Capital Controls"
module_type: "domain"
file_name: "domain-fx-carry-and-positioning.md"
purpose: "Analyze the risk-reward of holding VND versus USD and monitor market positioning signals from FIIs and offshore markets."
primary_triggers:
  - "VND carry trade"
  - "chênh lệch lãi suất VND USD"
  - "positioning indicators VN"
  - "FII net buy sell FX impact"
  - "offshore swap demand"
when_to_use:
  - "The user wants to evaluate if VND is attractive for 'search for yield' or if positioning suggests an imminent reversal."
when_not_to_use:
  - "Do not use for individual retail FX trading strategies."
related_modules:
  - "domain-fx-usd-vnd-dynamics.md"
  - "domain-macro-vn-liquidity-systems.md"
  - "framework-rey-global-financial-cycle.md"
authoritative_citations:
  - "Brunnermeier, M. K., et al. (2009). Carry Trades and Currency Crashes."
  - "FiinTrade Custom FII Reports."
  - "BIS Quarterly Review - EM Capital Flows."
output_owner: "workflow-deep-dive.md"
---

# Domain FX Carry and Positioning — Carry và Vị thế thị trường

## 1. Định nghĩa "Carry" trong ngữ cảnh Việt Nam
Thông thường, **Carry Trade** là chiến lược vay đồng tiền lãi suất thấp (như JPY) để đầu tư vào đồng tiền lãi suất cao (như BRL). Tuy nhiên, VND không phải là một đồng tiền carry trade tự do do:
- **Capital Controls**: Việt Nam kiểm soát dòng vốn chặt chẽ. Việc chuyển đổi VND ra ngoại tệ cho mục đích tài chính thuần túy bị hạn chế.
- **Devaluation Risk**: Lịch sử mất giá định kỳ của VND làm xói mòn lợi suất lãi suất.
- **Lãi suất thực (Real Yield)**: Phải xem xét lãi suất VND sau khi trừ lạm phát so với USD lãi suất thực.

Trong bối cảnh VN, "Carry" thường được hiểu là việc các NHTM hoặc các quỹ FII tận dụng chênh lệch lãi suất liên ngân hàng (Interbank) hoặc lãi suất trái phiếu chính phủ để tối ưu hóa lợi nhuận trong ngắn hạn.

## 2. Các chỉ báo Vị thế (Positioning Indicators)

### 2.1. Dòng vốn FII (Foreign Institutional Investment)
Khối ngoại (FII) là nhóm nhạy cảm nhất với tỷ giá.
- **Tương quan Nghịch**: Khi kỳ vọng VND mất giá tăng cao, khối ngoại có xu hướng bán ròng cổ phiếu để rút vốn về USD, tạo thêm áp lực cung FX.
- **FII Net Buy/Sell**: Việc theo dõi dòng vốn ròng hàng ngày/hàng tuần trên sàn HOSE là một proxy (đại diện) quan trọng cho tâm lý tỷ giá của dòng tiền thông minh.

### 2.2. Nhu cầu Swap Offshore (Offshore Swap Demand / Basis)
Thị trường Swap USD/VND phản ánh chi phí vay USD bằng cách thế chấp VND.
- **Swap Basis**: Khi nhu cầu USD tăng cao hoặc thanh khoản USD Onshore cạn kiệt, chi phí Swap sẽ tăng vọt. Sự phân kỳ giữa lãi suất Swap và lãi suất liên ngân hàng VND là dấu hiệu của "liquidity squeeze" (thắt chặt thanh khoản).
- **NDF Premium**: Chênh lệch giữa tỷ giá NDF 1-month và Spot phản ánh "embedded devaluation expectation" (kỳ vọng mất giá ngầm định).

### 2.3. Trạng thái ngoại tệ của Hệ thống Ngân hàng
NHNN quy định trạng thái ngoại tệ ròng của các NHTM không được vượt quá +/- 20% vốn tự có.
- **Long USD Position**: Khi các NHTM duy trì trạng thái dương (Long) ở mức cao, điều đó cho thấy họ kỳ vọng tỷ giá sẽ tăng hoặc đang tích trữ cho nhu cầu thanh toán của khách hàng.
- **Short VND Position**: Ngược lại, việc găm giữ USD làm giảm nguồn cung cho thị trường giao ngay, buộc NHNN phải can thiệp.

## 3. Chênh lệch lãi suất Thực (Real Interest Rate Differential) 2020-2026

Dưới đây là bảng so sánh lợi suất thực (Lãi suất 12 tháng - Inflation) của VND so với USD.

| Năm | VND Real Yield (%) | USD Real Yield (%) | Spread (VND-USD) | Tác động lên Carry |
|---|---|---|---|---|
| 2020 | +2.5 | -0.5 | +3.0 | VND hấp dẫn, dòng vốn FII ổn định. |
| 2021 | +3.0 | -5.0 | +8.0 | Spread kỷ lục do lạm phát US vọt lên. DXY vẫn yếu. |
| 2022 | +2.0 | -2.0 | +4.0 | US Real Yield tăng nhanh, thu hẹp spread. VND mất giá mạnh cuối năm. |
| 2023 | +1.5 | +1.5 | 0.0 | Carry VND biến mất. Áp lực tỷ giá thường trực. |
| 2024 | +0.5 | +2.0 | -1.5 | Spread âm. FII bán ròng liên tục (>2 tỷ USD trên sàn chứng khoán). |
| 2025-2026 | +1.0 | +1.0 | 0.0 | Trạng thái cân bằng mới. Carry không còn là động lực chính, thay bằng "Safety search". |

## 4. Rào cản Kiểm soát Vốn (Capital Controls Limits)
Việt Nam áp dụng Nghị định 70/2014/NĐ-CP và các thông tư hướng dẫn về quản lý ngoại hối:
- **Dòng tiền vãng lai**: Tương đối tự do cho mục đích nhập khẩu, du lịch (có hạn mức), học tập.
- **Dòng tiền vốn**: Kiểm soát chặt chẽ việc vay trả nợ nước ngoài của doanh nghiệp (phải đăng ký với NHNN). Việc thoái vốn của nhà đầu tư nước ngoài (FII) được thực hiện qua tài khoản vốn đầu tư gián tiếp (IICA).
- **Ảnh hưởng đến FX**: Các rào cản này ngăn chặn các cuộc tấn công đầu cơ quy mô lớn kiểu Soros nhưng cũng làm giảm tính thanh khoản và khả năng tự cân bằng của tỷ giá.

## 5. Phân tích Chu kỳ Vị thế (Positioning Cycles)

### Phase 1: Risk-On (Search for Yield)
- FII mua ròng cổ phiếu và trái phiếu VND.
- Swap Basis hẹp.
- NDF giao dịch thấp hơn hoặc bằng Spot.
- **Hành động**: NHNN mua ngoại tệ tăng dự trữ.

### Phase 2: Risk-Off (Deleverage/Hedging)
- FII bán ròng.
- Doanh nghiệp tăng cường mua USD Forward để phòng vệ.
- Swap Basis giãn rộng (USD đắt đỏ).
- NDF Premium tăng cao.
- **Hành động**: NHNN phát hành T-Bills nâng lãi suất hoặc bán USD.

## 6. Liên kết Framework (Linkage Matrix)
- **Rey Global Financial Cycle**: Khi chu kỳ tài chính toàn cầu thắt chặt, vị thế của các EM (như VN) chuyển từ "Carry Search" sang "Capital Preservation".
- **Borio Financial Cycle**: Sự gia tăng nợ bằng ngoại tệ của doanh nghiệp trong giai đoạn lãi suất USD thấp tạo ra rủi ro hệ thống khi vị thế đảo ngược.

---
**Cross-references:**
- Xem `domain-fx-usd-vnd-dynamics.md` để hiểu các biến số vĩ mô ảnh hưởng đến vị thế.
- Xem `domain-macro-vn-liquidity-systems.md` để hiểu sâu về thanh khoản hệ thống ngân hàng.
- Xem `framework-rey-global-financial-cycle.md` để áp dụng lens lý thuyết toàn cầu về dòng vốn.
