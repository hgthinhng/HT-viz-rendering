#import "cfa_warm.typ": *
#show: conf.with(level: "I")

= Phân tích tài chính doanh nghiệp
#gloss[Kiểm thử render Typst — dấu tiếng Việt, bảng số liệu, biểu đồ SVG]

Đây là bài kiểm thử khả năng xuất PDF chất lượng in bằng Typst, tập trung vào ba rủi ro thường gặp
khi làm báo cáo tài chính tiếng Việt: dấu thanh điệu bị vỡ, bảng số liệu căn lề sai, và biểu đồ bị
nướng thành ảnh bitmap thay vì giữ vector. Câu kiểm tra đủ dấu: "Nguyễn Văn Ánh, Trần Thị Ngọc Diễm,
Đặng Xuân Trường — dòng tiền chiết khấu, tỷ suất sinh lời, lãi suất phi rủi ro, đòn bẩy tài chính."

== Bảng kết quả kinh doanh

#cfatable(
  ([Chỉ tiêu], [2023], [2024], [2025], [Tăng trưởng]),
  (
    ([Doanh thu thuần (tỷ đồng)], [1.050], [1.180], [1.340], [+13,6%]),
    ([Lợi nhuận gộp (tỷ đồng)], [410], [468], [545], [+16,5%]),
    ([Lợi nhuận ròng (tỷ đồng)], [132], [151], [176], [+16,6%]),
    ([Biên lợi nhuận ròng], [12,6%], [12,8%], [13,1%], [+0,3 đpt]),
  ),
  caption: [Kết quả kinh doanh hợp nhất 2023 -- 2025],
)

#callout(kind: "key")[
  Biên lợi nhuận ròng cải thiện liên tục 3 năm, từ 12,6% lên 13,1% — chủ yếu nhờ #term[operating leverage][đòn bẩy hoạt động] khi doanh thu tăng nhanh hơn chi phí cố định.
]

== Công thức định giá

Tốc độ tăng trưởng kép hàng năm của doanh thu:

#align(center)[$ "CAGR" = (V_"cuối" / V_"đầu")^(1/n) - 1 $]

#text(9pt, fill: mute)[#text(fill: teal, weight:"bold")[$V$] = giá trị  ·  #text(fill: teal, weight:"bold")[$n$] = số năm]

Áp vào số liệu 2021--2025: $"CAGR" = (1340 / 820)^(1/4) - 1 approx 13.06%$.

== Biểu đồ doanh thu và lợi nhuận

#figure(image("chart.svg", width: 92%), caption: [Doanh thu và lợi nhuận ròng, 2021 -- 2025 (nguồn: BCTC hợp nhất đã kiểm toán)])

#callout(kind: "warn")[
  Số liệu 2025 là ước tính sơ bộ theo báo cáo quản trị nội bộ, chưa qua kiểm toán độc lập.
]
