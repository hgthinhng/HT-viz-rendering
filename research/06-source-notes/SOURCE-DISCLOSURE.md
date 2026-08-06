# Bảng quy đổi: gắn số vào nguồn kiểm chứng được, không lộ kênh nội bộ

Tài liệu dùng hằng ngày, không phải phát hiện đọc một lần. Đọc `FINDINGS.md` mục 1.3 trước để
hiểu cơ chế gốc (dòng "Nguồn:" của định chế phân tách "lấy dữ liệu từ đâu" và "tính ra bằng
cách nào"). File này áp cơ chế đó vào đúng căng thẳng của repo: luật đã chốt là số neo phải gắn
định danh và cấp nguồn, luật khác đã chốt là không khai nguồn trong artifact (xem memory
`feedback_no_source_disclosure_in_artifacts`, viết cho tình huống thông tin nhạy về tố tụng/
văn bản chưa công bố). Bảng dưới đây tổng quát hoá nguyên tắc đó sang tình huống PHỔ BIẾN HƠN
NHIỀU của repo này: báo cáo ngành/cổ phiếu thông thường, nơi căng thẳng không phải "tin nội bộ
nhạy cảm" mà là "nguồn dữ liệu thương mại, mô hình riêng, và số liệu tự tổng hợp".

## Nguyên tắc phân xử khi hai luật va nhau

Số nêu ra phải kèm mã đang giữ và nguồn công bố/dự báo (luật neo số) không có nghĩa là phải nêu
TÊN CHÍNH XÁC của kênh nội bộ đã dùng để lấy hoặc tính ra con số đó (luật không lộ nguồn). Hai
luật giải được đồng thời vì "nguồn" mà người đọc cần không phải là "chúng tôi lấy dữ liệu này từ
đâu trong hệ thống của mình", mà là "con số này thuộc loại nào" (đã công bố chính thức, hay ước
tính, hay tổng hợp) và "ai chịu trách nhiệm cho con số đó nếu sai" (chính doanh nghiệp, một cơ
quan công khai, hay đơn vị phát hành báo cáo). Trả lời đúng hai câu đó là đủ để người đọc kiểm
chứng và chiết khấu độ tin cậy, không cần biết tên hệ thống, tên công cụ, hay đường dây quan hệ
đã dùng để lấy được số.

## Bảng quy đổi

| Loại nguồn nội bộ | Cách diễn đạt ở bản giao đi | Vì sao vẫn kiểm chứng được |
|---|---|---|
| Số liệu công ty tự công bố (BCTC kiểm toán, báo cáo IR, tài liệu họp ĐHCĐ, thông cáo báo chí) | Nêu thẳng tên tài liệu và ngày công bố: "theo BCTC hợp nhất quý 2/2026, công bố 20/07/2026" | Đây là nguồn công khai đã sẵn kiểm được, chính công ty là bên chịu trách nhiệm cho số liệu, nêu thẳng tên không tạo rủi ro gì và còn TĂNG độ tin cậy |
| Số liệu cơ quan nhà nước/định chế quốc tế công khai (Tổng cục Thống kê, NHNN, UBCKNN, IMF, World Bank, sở giao dịch) | Nêu thẳng tên cơ quan và kỳ công bố: "theo Tổng cục Thống kê, số liệu tháng 6/2026" | Cùng lý do trên, đây là nguồn công khai chuẩn của ngành, không phải kênh nội bộ |
| Dữ liệu thương mại trả phí (nhà cung cấp dữ liệu thị trường, dữ liệu tổng hợp giá/khối lượng) | "Dữ liệu thị trường tổng hợp, chốt tới hết [ngày]" - không nêu tên nhà cung cấp cụ thể trừ khi điều khoản sử dụng của chính nhà cung cấp đó cho phép và yêu cầu ghi credit | Người đọc biết đây là dữ liệu giao dịch thật (không phải số tự nghĩ ra), có ngày chốt để đối chiếu với các nguồn công khai khác nếu muốn kiểm tra chéo; việc không nêu tên thương hiệu cụ thể không làm giảm khả năng kiểm chứng vì bản thân dữ liệu giá/khối lượng đã có thể đối chiếu qua sở giao dịch |
| Mô hình định giá, ước tính, hoặc kết quả backtest/calibration tự làm | "Ước tính của [đơn vị phát hành báo cáo]", kèm hộp giả định (xem mẫu `source-khoi-gia-dinh-dinh-gia.html`) nêu rõ input và logic ở mức người ngoài đọc hiểu được | Không giả vờ đây là số đo được: gắn nhãn "ước tính của bên phát hành" đã đúng bản chất, và hộp giả định cho người đọc đủ thông tin để TỰ TÁI TẠO logic, đây là dạng kiểm chứng mạnh hơn cả nêu tên nguồn |
| Tổng hợp nhiều nguồn công khai bằng công cụ nội bộ (thu thập tin tức, quét báo cáo công khai) | "Tổng hợp từ các nguồn công bố công khai" + liệt kê LOẠI nguồn đã dùng (báo chí trong nước, thông cáo doanh nghiệp, báo cáo cơ quan quản lý) | Liệt kê loại nguồn đủ để người đọc biết phạm vi tin cậy, không cần biết tên công cụ/pipeline dùng để thu thập, công cụ chỉ là phương tiện, không phải nguồn |
| Trao đổi riêng với ban lãnh đạo/IR không có xác nhận công khai đi kèm | Không đưa số đó vào artifact. Nếu thông tin thật sự trọng yếu, tìm xác nhận qua kênh công khai tương đương (biên bản ĐHCĐ, công bố thông tin) rồi trích theo dòng nguồn công khai đó; không có xác nhận thì bỏ hẳn con số | Đây là ranh giới cứng, không phải quy đổi câu chữ: một con số không kiểm chứng độc lập được thì không có cách diễn đạt nào làm nó kiểm chứng được, xử lý bằng cách bỏ, không phải bằng cách nói giảm |
| Vị thế/giao dịch của một bên cụ thể mà báo cáo biết được qua quan hệ riêng | Không đưa vào, trừ khi chính bên đó là chủ thể công bố công khai (báo cáo sở hữu theo quy định). Nếu cần nhắc, dùng khung "theo dữ liệu giao dịch công khai trên sàn ngày X" | Số liệu giao dịch công khai trên sàn tự nó đã kiểm chứng được qua chính sở giao dịch, không cần nhắc quan hệ riêng nào để có được thông tin đó |
| Tên hệ thống/pipeline/dự án nội bộ dùng để xử lý số liệu | Không nêu tên. Nếu bắt buộc phải mô tả có xử lý, dùng "quy trình tổng hợp dữ liệu nội bộ" chung chung, phần lớn trường hợp bỏ hẳn không cần nhắc | Tên hệ thống không mang thông tin kiểm chứng nào cho người đọc bên ngoài, chỉ mang rủi ro lộ cấu trúc vận hành, bỏ đi không mất giá trị phân tích |
| Kênh truyền thông riêng tư (nhóm chat, diễn đàn nội bộ, hội thảo mời riêng) | Không trích trực tiếp. Tìm nguồn công khai tương đương để dẫn thay thế; không có thì bỏ | Cùng nguyên tắc với dòng "trao đổi riêng ban lãnh đạo": không kiểm chứng độc lập được thì không đưa vào, đúng tinh thần verifiability của báo chí (nguồn giấu tên chỉ dùng khi có thể đối chiếu qua nguồn khác) |

## Cụm từ NÊN TRÁNH vì vô tình lộ kênh

- "Theo nguồn tin nội bộ [tên doanh nghiệp]" - tự khai có đường dây riêng với đúng doanh nghiệp
  đang được phân tích, đây là rủi ro nặng nhất vì gắn trực tiếp vào một chủ thể có thể truy vết.
- "Dữ liệu lấy từ [tên hệ thống/tên nhà cung cấp cụ thể] mà chúng tôi đang thuê bao" - lộ cả
  quan hệ thương mại lẫn quy mô đầu tư hạ tầng dữ liệu, không cần thiết cho giá trị phân tích.
- "Theo trao đổi riêng với ban lãnh đạo" khi không kèm xác nhận công khai - biến một cuộc nói
  chuyện không kiểm chứng được thành có vẻ như một trích dẫn chính thức.
- "Theo file/mô hình nội bộ phòng phân tích" hoặc nêu thẳng tên dự án/pipeline - lộ cấu trúc vận
  hành mà không tăng thêm một chút độ tin cậy nào cho con số.
- "Một nhà đầu tư đang nắm giữ X% cho biết" khi chính bên viết báo cáo là nhà đầu tư đó - vừa lộ
  vị thế, vừa lộ động cơ, đọc được ngay là quảng cáo trá hình cho vị thế của mình.
- "Theo dữ liệu chúng tôi thu thập được từ [nhóm chat/diễn đàn cụ thể]" - lộ kênh riêng tư đã
  theo dõi, và thường không kiểm chứng độc lập được nên còn vi phạm cả nguyên tắc verifiability.
- Bất kỳ URL nội bộ, tên trường dữ liệu (field name), tên API endpoint, hay đường dẫn file dùng
  để truy vấn/tính ra con số - đây là chi tiết vận hành, không phải nguồn theo nghĩa người đọc
  cần, và có thể lộ thêm cấu trúc hệ thống nếu bị đọc kỹ.
- "Chúng tôi có thông tin sớm hơn thị trường" hoặc bất kỳ câu hàm ý biết trước ngày công bố của
  doanh nghiệp - đây là ranh giới đã chốt ở memory `feedback_no_source_disclosure_in_artifacts`,
  nhắc lại vì cùng họ lỗi: không phải lỗi phân tích, lỗi nằm ở câu khai nguồn không cần thiết.

## Liên hệ với FINDINGS.md

Cơ chế cột 2 trong bảng trên chính là áp dụng mục 1.3 (dòng "Nguồn:" kiểu BIS) vào từng loại
nguồn cụ thể của repo này: số công khai giữ nguyên tên, số đã qua xử lý đóng bằng "ước tính/tính
toán của [đơn vị phát hành]". Mẫu `source-bang-thuc-te-du-phong.html` và
`source-khoi-gia-dinh-dinh-gia.html` áp dụng trực tiếp cách quy đổi này trong dòng nguồn ở chân
bảng.
