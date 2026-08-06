# Domain: VND NDF Mechanics

> **RAG Status:** Green | **Priority:** P0 (Critical)
> **Domain:** FX (Foreign Exchange)
> **Related Frameworks:** framework-rey-global-financial-cycle, framework-diebold-yilmaz-spillover
> **Last Updated:** 2026-04-19

## 1. TỔNG QUAN (OVERVIEW)

VND NDF (Non-Deliverable Forward) là một công cụ phái sinh ngoại hối cho phép các nhà đầu tư offshore phòng ngừa rủi ro hoặc đầu cơ trên biến động của VND mà không cần sở hữu thực tế đồng tiền này. Do Việt Nam duy trì các biện pháp kiểm soát vốn (capital controls), NDF trở thành thị trường quan trọng nhất để quan sát kỳ vọng "thực" của thị trường quốc tế về VND.

---

## 2. CẤU TRÚC THỊ TRƯỜNG (MARKET STRUCTURE)

- **Địa điểm giao dịch:** Chủ yếu tại Singapore, Hong Kong và London.
- **Cơ chế thanh toán:** Không có việc chuyển giao USD và VND thực tế. Vào ngày đáo hạn, hai bên sẽ thanh toán mức chênh lệch giữa tỷ giá thỏa thuận (strike price) và tỷ giá Spot thực tế bằng USD.
- **Đối tượng tham gia:** Các ngân hàng đầu tư quốc tế, các quỹ phòng hộ (hedge funds), và các tập đoàn đa quốc gia có dòng tiền tại VN nhưng bị hạn chế bởi hạn ngạch forward onshore.

---

## 3. NDF VS. ONSHORE FORWARD: TÍN HIỆU TỪ CHÊNH LỆCH

Đây là phần cốt lõi của phân tích FX tại Việt Nam (Kimi P0):

### 3.1. Phản ánh kỳ vọng (True Market Sentiment)
- Thị trường Onshore (trong nước) bị kiểm soát chặt chẽ bởi NHNN qua tỷ giá trung tâm và biên độ giao dịch.
- Thị trường NDF (offshore) phản ánh cung cầu tự do hơn. Khi NDF giao dịch ở mức giá cao hơn đáng kể so với Spot và Onshore Forward (NDF Premium), thị trường đang kỳ vọng VND sẽ mất giá mạnh trong tương lai.

### 3.2. Chỉ báo hiệu quả kiểm soát vốn (Capital Control Effectiveness)
- **NDF Spread (NDF - Onshore):** Nếu spread này nới rộng, nó cho thấy các biện pháp kiểm soát vốn của NHNN đang ngăn chặn hiệu quả việc truyền dẫn áp lực từ bên ngoài vào thị trường nội địa, nhưng đồng thời cũng tạo ra sự mất cân bằng tiềm tàng.
- **Arbitrage Opportunity:** Khi spread đủ lớn, các thực thể có hiện diện ở cả hai thị trường sẽ tìm cách arbitrage (mặc dù khó khăn do quy định), điều này cuối cùng sẽ gây áp lực ngược lại lên thị trường Onshore.

---

## 4. CÁC GIAI ĐOẠN DIVERGENCE LỊCH SỬ

- **Giai đoạn stress thanh khoản USD (2022, 2024):** NDF thường chạy trước Spot từ 2-4 tuần. Khi NDF 1M hoặc 3M bắt đầu tăng vọt, đó là tín hiệu sớm cho thấy NHNN có thể sắp phải điều chỉnh tỷ giá trung tâm hoặc bán USD can thiệp.
- **Giai đoạn ổn định:** NDF và Onshore Forward có xu hướng hội tụ.

---

## 5. CÁCH SỬ DỤNG TRONG NGHIÊN CỨU (OPERATIONALIZATION)

1. **Theo dõi Forward Points:** Quan sát đường cong NDF (NDF Curve) từ 1M đến 12M để xác định "điểm gãy" kỳ vọng của thị trường.
2. **So sánh với lãi suất liên ngân hàng (VND Interest Rate):** NDF Premium thường phản ánh chênh lệch lãi suất (Interest Rate Differential). Nếu NDF tăng mạnh vượt xa mức chênh lệch lãi suất, đó là biểu hiện của rủi ro mất giá (Devaluation Risk).
3. **Signpost cho Intervention:** Khi NDF Spread vượt qua ngưỡng lịch sử (ví dụ > 500-700 pips), khả năng NHNN can thiệp mạnh tay là rất cao.

---

## 6. CROSS-REFERENCES

- **framework-rey-global-financial-cycle:** NDF là kênh truyền dẫn chính của Global Financial Cycle vào VND.
- **domain-fx-intervention-history:** Cách NHNN phản ứng khi NDF tạo áp lực lên tỷ giá trong nước.
- **domain-macro-vn-balance-of-payments:** NDF phản ánh áp lực lên cán cân thanh toán trước khi số liệu chính thức được công bố.
