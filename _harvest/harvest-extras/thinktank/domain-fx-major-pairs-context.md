# Domain: Major FX Pairs & VND Context

> **RAG Status:** Green | **Priority:** P1
> **Domain:** FX (Foreign Exchange)
> **Related Frameworks:** framework-rey-global-financial-cycle, framework-diebold-yilmaz-spillover
> **Last Updated:** 2026-04-19

## 1. TỔNG QUAN (OVERVIEW)

Trong hệ thống tỷ giá của Việt Nam, VND không biến động hoàn toàn tự do mà được quản lý dựa trên một rổ tiền tệ (basket-pegged). Tuy nhiên, trọng số của các đồng tiền trong rổ không được công bố minh bạch. Module này phân tích các đồng tiền chính (Major Pairs) và cách biến động của chúng truyền dẫn vào tỷ giá USD/VND.

**Key Insight:** Trong khi DXY là thước đo sức mạnh toàn cầu của USD, thì **CNY (Nhân dân tệ)** mới là mỏ neo (anchor) thực tế quan trọng nhất đối với tính cạnh tranh thương mại và ổn định tỷ giá của Việt Nam.

---

## 2. DXY DYNAMICS: CÁI NEO TOÀN CẦU

Chỉ số DXY (USD Index) đo lường sức mạnh của USD so với rổ 6 đồng tiền mạnh (EUR, JPY, GBP, CAD, SEK, CHF).

- **Cơ chế truyền dẫn:** Khi DXY tăng mạnh, áp lực lên các đồng tiền EM (Emerging Markets) là tất yếu. NHNN thường phải đối mặt với áp lực mất giá VND để duy trì tính cạnh tranh của xuất khẩu và ngăn chặn chảy máu ngoại tệ.
- **DXY và Tâm lý thị trường:** DXY thường được dùng làm chỉ báo RORO (Risk-on/Risk-off). DXY tăng = Risk-off = Áp lực bán VND.

---

## 3. EUR & JPY: CÁC BIẾN SỐ PHỤ TRỢ

- **EUR/USD:** Cặp tiền có trọng số lớn nhất trong DXY. Biến động của EUR phản ánh sức khỏe kinh tế Châu Âu - thị trường xuất khẩu lớn của VN. EUR yếu có thể làm giảm sức mua đối với hàng hóa VN.
- **USD/JPY:** Quan trọng đối với dòng vốn FDI và ODA từ Nhật Bản. Sự mất giá mạnh của JPY (như giai đoạn 2024-2025) tạo ra áp lực deflationary cho hàng nhập khẩu từ Nhật nhưng lại gây khó khăn cho các doanh nghiệp VN có nợ bằng JPY.

---

## 4. CNY/USD: MỎ NEO CHIẾN LƯỢC (PRIMARY ANCHOR) - KIMI P0

Kimi P0 nhấn mạnh rằng **CNY là biến số quan trọng nhất** cần theo dõi khi phân tích VND do các yếu tố sau:

### 4.1. Liên kết thương mại (Trade Linkage)
- Việt Nam nhập siêu lớn từ Trung Quốc (~30% tổng kim hạch nhập khẩu). Hầu hết nguyên liệu đầu vào cho ngành sản xuất/gia công của VN đến từ TQ.
- Nếu CNY mất giá so với USD mà VND vẫn giữ giá, hàng hóa VN sẽ trở nên đắt đỏ hơn so với hàng TQ, gây rủi ro mất thị phần xuất khẩu và gia tăng nhập siêu.

### 4.2. Chuỗi cung ứng (Supply Chain Linkage)
- Mô hình "China + 1" khiến VN và TQ trở thành các mắt xích bổ trợ trong chuỗi cung ứng toàn cầu. Sự đồng bộ giữa VND và CNY giúp ổn định chi phí sản xuất cho các tập đoàn đa quốc gia (MNEs).

### 4.3. Rủi ro phá giá cạnh tranh (Competitive Devaluation)
- Lịch sử cho thấy NHNN thường có xu hướng "nhìn" theo biến động của CNY để điều chỉnh tỷ giá trung tâm. Khi CNY/USD vượt qua các ngưỡng tâm lý (ví dụ 7.2 hoặc 7.3), áp lực lên USD/VND sẽ tăng vọt ngay lập tức.

---

## 5. CƠ CHẾ TRUYỀN DẪN (TRANSMISSION MECHANISM)

Công thức tư duy: **VND Movement ≈ α(DXY) + β(CNY) + γ(Internal Flows)**

- **Kịch bản 1: DXY tăng, CNY giảm (Bearish cho VND):** Đây là kịch bản "double-hit". VND chịu áp lực kép từ sức mạnh USD toàn cầu và áp lực cạnh tranh từ TQ. NHNN thường phải can thiệp bằng dự trữ ngoại hối hoặc nâng tỷ giá trung tâm.
- **Kịch bản 2: DXY tăng, CNY ổn định (Mixed):** VND có thể mất giá nhẹ nhưng mức độ căng thẳng thấp hơn nhờ mỏ neo CNY giữ vững tâm lý khu vực.
- **Kịch bản 3: CNY mất giá mạnh bất kể DXY (Critical):** Nguy cơ shock tỷ giá tại VN rất cao. Thị trường sẽ kỳ vọng VND phải phá giá theo để bảo vệ biên lợi nhuận xuất khẩu.

---

## 6. CROSS-REFERENCES

- **framework-rey-global-financial-cycle:** Giải thích tại sao DXY chi phối dòng vốn vào EM bất kể chính sách nội địa.
- **framework-diebold-yilmaz-spillover:** Đo lường mức độ shock từ CNY lan tỏa sang VND so với các đồng tiền khác trong khu vực (THB, IDR).
- **domain-fx-ndf-mechanics:** Cách thị trường NDF phản ánh kỳ vọng về sự dịch chuyển này trước khi thị trường Spot phản ứng.
