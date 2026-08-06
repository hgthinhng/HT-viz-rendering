# Domain: EM FX Frameworks (VN Calibration)

> **RAG Status:** Green | **Priority:** P1
> **Domain:** FX (Foreign Exchange)
> **Related Frameworks:** framework-rey-global-financial-cycle, framework-mundell-fleming-trilemma
> **Last Updated:** 2026-04-19

## 1. TỔNG QUAN (OVERVIEW)

Phân tích tỷ giá tại các thị trường mới nổi (EM) như Việt Nam đòi hỏi các khung lý thuyết chuyên biệt, vượt ra ngoài các mô hình PPP (Purchasing Power Parity) cơ bản. Module này hệ thống hóa các framework quan trọng nhất để đánh giá sức mạnh đồng nội tệ và rủi ro khủng hoảng tỷ giá, được hiệu chỉnh (calibrate) cho bối cảnh Việt Nam.

---

## 2. TRILEMMA VS. DILEMMA: BỐI CẢNH CHÍNH SÁCH

### 2.1. Mundell-Fleming Trilemma (Bộ ba bất khả thi)
- Một quốc gia không thể đồng thời thực hiện ba mục tiêu: (1) Tỷ giá cố định, (2) Chính sách tiền tệ độc lập, (3) Tự do lưu chuyển vốn.
- **VN Calibration:** VN chọn (1) Tỷ giá ổn định (pegged-float) và (2) Chính sách tiền tệ độc lập. Do đó, VN phải thực hiện (3) Kiểm soát vốn (Capital Controls). Mọi nỗ lực nới lỏng kiểm soát vốn sẽ trực tiếp đe dọa sự ổn định tỷ giá nếu lãi suất không đồng bộ với thế giới.

### 2.2. Rey's Dilemma (Global Financial Cycle)
- Hélène Rey (2015) lập luận rằng đối với EM, Trilemma thực chất là Dilemma. Nếu dòng vốn toàn cầu (chi phối bởi Fed/DXY) được tự do, EM sẽ mất độc lập tiền tệ bất kể họ chọn chế độ tỷ giá nào.
- **VN Application:** Khi Fed thắt chặt, thanh khoản USD toàn cầu thu hẹp, VN buộc phải tăng lãi suất hoặc bán USD để giữ tỷ giá, dù kinh tế nội địa có thể đang cần nới lỏng.

---

## 3. DÒNG VỐN: SURGES & SUDDEN STOPS (CALVO)

- **Capital Flow Surges:** Khi dòng vốn (FDI, FII) đổ vào quá mạnh, gây áp lực tăng giá nội tệ và bong bóng tài sản.
- **Sudden Stops:** Khi dòng vốn đột ngột rút ra (thường do shock toàn cầu hoặc rủi ro địa chính trị).
- **Indicators cho VN:** Theo dõi số liệu FDI giải ngân hàng tháng và trạng thái mua/bán ròng của khối ngoại trên thị trường chứng khoán (proxy cho FII).

---

## 4. ĐÁNH GIÁ DỰ TRỮ NGOẠI HỐI (RESERVE ADEQUACY)

NHNN dùng dự trữ ngoại hối (FX Reserves) làm "tấm đệm" bảo vệ tỷ giá. Các tiêu chuẩn phổ biến:

- **Tháng nhập khẩu (Months of Imports):** Tiêu chuẩn tối thiểu là 3 tháng. Đây là chỉ số VN thường dùng nhất.
- **Greenspan-Guidotti Rule:** Dự trữ phải đủ cover 100% nợ nước ngoài ngắn hạn (đáo hạn trong 1 năm).
- **IMF ARA Metric (Assessing Reserve Adequacy):** Một công thức phức tạp hơn kết hợp cả xuất khẩu, nợ ngắn hạn, cung tiền M2 và các nghĩa vụ tài chính khác.
- **VN Context:** Trong các giai đoạn DXY mạnh, việc dự trữ ngoại hối giảm xuống gần ngưỡng 3 tháng nhập khẩu là một tín hiệu báo động đỏ (Red Flag) cho khả năng phá giá VND.

---

## 5. CHỈ BÁO CẢNH BÁO SỚM (EARLY-WARNING INDICATORS)

Dựa trên các mô hình khủng hoảng tiền tệ EM:

1. **Real Effective Exchange Rate (REER) Appreciation:** Nếu REER của VND tăng quá nhanh so với các đối tác thương mại, VND đang bị định giá cao quá mức (overvalued), tạo áp lực phá giá.
2. **Current Account Deficit:** Thâm hụt vãng lai kéo dài > 3-5% GDP.
3. **Credit-to-GDP Gap:** Tín dụng tăng trưởng quá nóng so với xu hướng dài hạn (gắn với rủi ro nợ xấu và rút vốn).
4. **M2/FX Reserves Ratio:** Tỷ lệ tiền mặt nội tệ so với dự trữ ngoại hối. Tỷ lệ này cao cho thấy khả năng bảo vệ tỷ giá yếu nếu người dân chuyển đổi hàng loạt từ nội tệ sang USD.

---

## 6. CROSS-REFERENCES

- **framework-rey-global-financial-cycle:** Nền tảng cho hiểu biết về Dilemma của EM.
- **domain-macro-vn-monetary-policy-nhnn:** Cách NHNN điều hành lãi suất trong khuôn khổ Trilemma.
- **domain-fx-major-pairs-context:** CNY là biến số bổ sung vào khung phân tích EM truyền thống cho VN.
