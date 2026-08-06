# Bảng màu đề xuất cho 4, 6, 8 chuỗi

Đơn vị: GrayCSS trên thang 0-255 (công thức CSS Filter Effects Level 1, áp trực tiếp lên sRGB đã
nén gamma, đã tự kiểm khớp Chromium thật sai số tối đa 0.49/255: xem FINDINGS.md mục 1). ΔE dùng
CIE76 (Euclidean trong Lab). Ba cột ΔE mù màu là kết quả sau khi áp ma trận Machado/Oliveira/
Fernandes 2009 (severity 1.0) rồi đo lại ΔE76 giữa 2 màu đã mô phỏng.

**An toàn bản in**: cả 3 bảng dưới đây AN TOÀN CHO BẢN IN (ΔGrayCSS nhỏ nhất toàn bảng ≥ 15, xem
ngưỡng thực dụng ở FINDINGS.md mục 1). Bảng N=8 cần hoạ tiết bổ sung cho 1 cặp (xem ghi chú dưới
bảng đó) để an toàn cho NÉT MẢNH (đường line chart) chứ không chỉ mảng lớn (thanh, cột).

## Quy tắc dẫn xuất (áp dụng chung cho cả 3 bảng)

1. Bắt đầu từ token có sẵn trong `tokens.css`, ưu tiên dùng hết trước khi sinh màu mới (đúng tinh
   thần "bảng hẹp là chủ ý" của repo). 5 token `ink`, `accent-hi`, `accent`, `ink-lo`, `line` đã đủ
   an toàn cho N=4 và N=5 mà không cần thêm màu nào.
2. Khi cần thêm màu (N=6, 7, 8), dùng thuật toán tham lam (greedy) trong không gian CIE LCH: mỗi
   màu mới được chọn để tối đa hoá `min(ΔGrayCSS, 1.3 × ΔE-mù-màu-tệ-nhất-trong-3-dạng)` so với MỌI
   màu đã có trong bảng (không chỉ màu liền kề dự kiến, vì thứ tự trong chú giải có thể đảo).
3. Hue của màu mới bị giới hạn trong **cung an toàn**: loại bỏ không chỉ góc hue chính xác của
   `pos`/`neg`/`warn`, mà cả vùng lân cận theo TÊN màu cảm nhận (loại dải đỏ 330-50°, cam/vàng
   50-95°, xanh lá/ngọc 95-190° trên thang hue CIE Lab): vì độc giả báo cáo tài chính gán nghĩa
   "xanh lá = tốt, đỏ/cam = xấu/cảnh báo" theo TÊN màu, không theo góc hue chính xác.
4. Sắp xếp toàn bộ N màu theo GrayCSS TĂNG DẦN một lần duy nhất, rồi gán cho hạng mục theo thứ tự
   ưu tiên của bài toán (hạng mục lớn nhất/quan trọng nhất trước). Xem quy tắc đầy đủ ở FINDINGS.md
   mục 7.
5. Mọi mảng dùng màu ở nửa sáng (GrayCSS > 180) phải có viền `ink` (đề xuất 0.5-0.8px), không thì
   biến mất khi giáp nền giấy trắng.
6. Nếu ΔGrayCSS giữa 2 màu liền kề (sau khi sắp ở bước 4) dưới 20, thêm hoạ tiết (`<pattern>` gạch
   chéo hoặc chấm bi, không dùng gradient/filter) cho ít nhất 1 trong 2 màu đó.

## Bảng N=4: an toàn tuyệt đối, không cần màu mới

Dùng nguyên token có sẵn, không sinh màu mới. Hợp mọi loại dữ liệu (có thứ tự lẫn định danh) vì có
đủ hue lệch nhau (navy, xanh dương đậm, xanh dương điện, xám-trắng).

| Màu | Hex | L* | GrayCSS (0-255) | Nguồn gốc |
|---|---|---|---|---|
| `ink` | `#051C2C` | 9.4 | 24.3 | token gốc tokens.css |
| `accent-hi` | `#1233B8` | 29.3 | 53.6 | token gốc tokens.css |
| `accent` | `#2251FF` | 43.4 | 83.6 | token gốc tokens.css |
| `line` | `#DBE2EA` | 89.6 | 225.1 | token gốc tokens.css |

| Cặp | ΔGrayCSS | Contrast ratio | ΔE76 | ΔE protanopia | ΔE deuteranopia | ΔE tritanopia |
|---|---|---|---|---|---|---|
| ink/accent-hi | 29.3 | 1.81 | 75.7 | 61.5 | 65.8 | 29.4 |
| ink/accent | 59.3 | 3.05 | 97.9 | 80.7 | 87.9 | 45.6 |
| ink/line | 200.8 | 13.30 | 80.7 | 79.9 | 81.0 | 79.9 |
| accent-hi/accent | 30.0 | 1.68 | 23.7 | 20.5 | 23.1 | 16.7 |
| accent-hi/line | 171.5 | 7.34 | 99.7 | 84.0 | 91.4 | 58.6 |
| accent/line | 141.5 | 4.36 | 108.6 | 87.5 | 99.2 | 48.4 |

**ΔGrayCSS nhỏ nhất toàn bảng: 29.3.** Không cần hoạ tiết. An toàn cho cả bản in và bản màn hình,
cho cả mảng lớn lẫn nét mảnh (mọi cặp đều trên ngưỡng 20 của nét mảnh).

**Biến thể valence-punchier** (nếu chấp nhận mượn tạm `warn`, KHÔNG dùng nếu trang có chart valence
khác gần đó): `ink`, `accent`, `warn`, `line`: min ΔGrayCSS = 42.3, min ΔE mù màu = 45.6, số đẹp
hơn nhưng đổi lấy rủi ro ngữ nghĩa.

## Bảng N=6: mở rộng tối thiểu 1 màu mới, vẫn không cần hoạ tiết

Thêm `accent-sky` (màu mới, sinh trong cung an toàn) vào bộ N=4. Đo được: thêm màu này KHÔNG làm
giảm ΔGrayCSS nhỏ nhất so với N=4/N=5 (vẫn giữ 29.3): đây là bằng chứng số cho việc mở rộng có
kiểm soát không nhất thiết phải đánh đổi an toàn.

| Màu | Hex | L* | GrayCSS (0-255) | Nguồn gốc |
|---|---|---|---|---|
| `ink` | `#051C2C` | 9.4 | 24.3 | token gốc tokens.css |
| `accent-hi` | `#1233B8` | 29.3 | 53.6 | token gốc tokens.css |
| `accent` | `#2251FF` | 43.4 | 83.6 | token gốc tokens.css |
| `ink-lo` | `#8595A6` | 61.0 | 146.8 | token gốc tokens.css |
| `accent-sky` | `#82C0FF` | 75.9 | 183.4 | mới, greedy CIE LCH, cung an toàn |
| `line` | `#DBE2EA` | 89.6 | 225.1 | token gốc tokens.css |

| Cặp | ΔGrayCSS | Contrast ratio | ΔE76 | ΔE protanopia | ΔE deuteranopia | ΔE tritanopia |
|---|---|---|---|---|---|---|
| ink/accent-hi | 29.3 | 1.81 | 75.7 | 61.5 | 65.8 | 29.4 |
| ink/accent | 59.3 | 3.05 | 97.9 | 80.7 | 87.9 | 45.6 |
| ink/ink-lo | 122.6 | 5.66 | 51.7 | 51.4 | 51.9 | 51.0 |
| ink/accent-sky | 159.1 | 9.04 | 70.6 | 71.1 | 70.1 | 70.9 |
| ink/line | 200.8 | 13.30 | 80.7 | 79.9 | 81.0 | 79.9 |
| accent-hi/accent | 30.0 | 1.68 | 23.7 | 20.5 | 23.1 | 16.7 |
| accent-hi/ink-lo | 93.2 | 3.12 | 81.3 | 63.9 | 71.2 | 30.9 |
| accent-hi/accent-sky | 129.8 | 4.99 | 73.2 | 56.2 | 57.6 | 46.6 |
| accent-hi/line | 171.5 | 7.34 | 99.7 | 84.0 | 91.4 | 58.6 |
| accent/ink-lo | 63.3 | 1.86 | 95.3 | 73.2 | 84.4 | 25.6 |
| accent/accent-sky | 99.8 | 2.96 | 80.7 | 57.3 | 63.0 | 32.7 |
| accent/line | 141.5 | 4.36 | 108.6 | 87.5 | 99.2 | 48.4 |
| ink-lo/accent-sky | 36.5 | 1.60 | 30.3 | 28.5 | 31.6 | 30.4 |
| ink-lo/line | 78.3 | 2.35 | 29.3 | 28.7 | 29.4 | 29.3 |
| accent-sky/line | 41.7 | 1.47 | 35.3 | 31.2 | 38.0 | 35.1 |

**ΔGrayCSS nhỏ nhất toàn bảng: 29.3.** Không cần hoạ tiết. An toàn cho cả mảng lớn và nét mảnh
(mọi cặp trên ngưỡng 20).

## Bảng N=8: an toàn cho mảng lớn, cần hoạ tiết cho 1 cặp nếu dùng nét mảnh

Thêm `accent-plum` và `accent-cyan` (2 màu mới, cùng thuật toán) vào bộ N=6. Đây là ngưỡng nơi
việc mở rộng bắt đầu có chi phí: ΔGrayCSS nhỏ nhất giảm từ 29.3 xuống 18.7.

| Màu | Hex | L* | GrayCSS (0-255) | Nguồn gốc |
|---|---|---|---|---|
| `ink` | `#051C2C` | 9.4 | 24.3 | token gốc tokens.css |
| `accent-hi` | `#1233B8` | 29.3 | 53.6 | token gốc tokens.css |
| `accent` | `#2251FF` | 43.4 | 83.6 | token gốc tokens.css |
| `accent-plum` | `#9162BD` | 50.0 | 114.6 | mới, greedy CIE LCH, cung an toàn |
| `ink-lo` | `#8595A6` | 61.0 | 146.8 | token gốc tokens.css |
| `accent-sky` | `#82C0FF` | 75.9 | 183.4 | mới, greedy CIE LCH, cung an toàn |
| `accent-cyan` | `#64E3FF` | 84.4 | 202.0 | mới, greedy CIE LCH, cung an toàn |
| `line` | `#DBE2EA` | 89.6 | 225.1 | token gốc tokens.css |

| Cặp | ΔGrayCSS | Contrast ratio | ΔE76 | ΔE protanopia | ΔE deuteranopia | ΔE tritanopia |
|---|---|---|---|---|---|---|
| ink/accent-hi | 29.3 | 1.81 | 75.7 | 61.5 | 65.8 | 29.4 |
| ink/accent | 59.3 | 3.05 | 97.9 | 80.7 | 87.9 | 45.6 |
| ink/accent-plum | 90.3 | 3.88 | 62.7 | 50.5 | 48.9 | 47.6 |
| ink/ink-lo | 122.6 | 5.66 | 51.7 | 51.4 | 51.9 | 51.0 |
| ink/accent-sky | 159.1 | 9.04 | 70.6 | 71.1 | 70.1 | 70.9 |
| ink/accent-cyan | 177.8 | 11.56 | 79.8 | 77.6 | 74.3 | 83.7 |
| ink/line | 200.8 | 13.30 | 80.7 | 79.9 | 81.0 | 79.9 |
| accent-hi/accent | 30.0 | 1.68 | 23.7 | 20.5 | 23.1 | 16.7 |
| accent-hi/accent-plum | 61.0 | 2.14 | 37.6 | 29.3 | 42.7 | 33.7 |
| accent-hi/ink-lo | 93.2 | 3.12 | 81.3 | 63.9 | 71.2 | 30.9 |
| accent-hi/accent-sky | 129.8 | 4.99 | 73.2 | 56.2 | 57.6 | 46.6 |
| accent-hi/accent-cyan | 148.4 | 6.38 | 100.1 | 72.4 | 70.8 | 60.6 |
| accent-hi/line | 171.5 | 7.34 | 99.7 | 84.0 | 91.4 | 58.6 |
| accent/accent-plum | 31.0 | 1.27 | 50.5 | 39.0 | 55.9 | 36.2 |
| accent/ink-lo | 63.3 | 1.86 | 95.3 | 73.2 | 84.4 | 25.6 |
| accent/accent-sky | 99.8 | 2.96 | 80.7 | 57.3 | 63.0 | 32.7 |
| accent/accent-cyan | 118.5 | 3.79 | 108.5 | 74.2 | 76.7 | 47.1 |
| accent/line | 141.5 | 4.36 | 108.6 | 87.5 | 99.2 | 48.4 |
| accent-plum/ink-lo | 32.3 | 1.46 | 50.2 | 36.5 | 30.5 | 26.3 |
| accent-plum/accent-sky | 68.8 | 2.33 | 47.7 | 31.2 | 23.7 | 54.7 |
| accent-plum/accent-cyan | 87.5 | 2.98 | 74.5 | 46.4 | 33.8 | 69.6 |
| accent-plum/line | 110.5 | 3.43 | 65.5 | 57.2 | 52.3 | 43.5 |
| ink-lo/accent-sky | 36.5 | 1.60 | 30.3 | 28.5 | 31.6 | 30.4 |
| ink-lo/accent-cyan | 55.2 | 2.04 | 36.9 | 27.4 | 27.0 | 44.7 |
| ink-lo/line | 78.3 | 2.35 | 29.3 | 28.7 | 29.4 | 29.3 |
| **accent-sky/accent-cyan** | **18.7** | 1.28 | 28.6 | 17.4 | **14.4** | 15.4 |
| accent-sky/line | 41.7 | 1.47 | 35.3 | 31.2 | 38.0 | 35.1 |
| accent-cyan/line | 23.1 | 1.15 | 33.1 | 14.5 | 24.0 | 43.8 |

**ΔGrayCSS nhỏ nhất toàn bảng: 18.7** (cặp `accent-sky`/`accent-cyan`, cũng là cặp yếu nhất dưới mô
phỏng deuteranopia với ΔE=14.4). Cặp này nằm giữa 2 ngưỡng thực dụng (đủ cho mảng lớn ≥15, CHƯA đủ
dư dả cho nét mảnh ≥20): **bắt buộc gắn hoạ tiết** cho ít nhất 1 trong 2 màu nếu dùng làm đường
line chart cạnh nhau; nếu chỉ dùng làm mảng/thanh (như trong `samples/palette-8-chuoi.html` và
`samples/palette-mau-vs-thang-xam.html`), hoạ tiết là biện pháp an toàn thêm chứ không bắt buộc
tuyệt đối, nhưng cả 2 mẫu vẫn gắn để minh hoạ cách bù đúng chỗ toán học chỉ ra là yếu nhất.

**Chỉ hợp bản in nếu có hoạ tiết ở cặp trên; hợp bản màn hình ngay cả không có hoạ tiết** (màn hình
màu không gặp vấn đề GrayCSS, và ΔE76 bình thường của cặp đó vẫn là 28.6, đủ phân biệt với mắt
thường có màu).

## Trên N=8: xem FINDINGS.md mục 4

Kéo dài cùng thuật toán tới N=12 vẫn giữ ΔGrayCSS trên ngưỡng tối thiểu 10 (giảm dần đều 18.7 →
17.3 → 16.1 → 15.4 → 15.0), nhưng KHÔNG khuyến nghị dùng tới N=10-12 bằng màu thuần tuý: các màu
sinh thêm đều rơi vào cùng họ "xanh dương-xanh lam-xám" không có tên gọi riêng để nhớ, và gánh nặng
legend nhiều mục làm giảm hiệu quả đọc dù số đo vẫn qua ngưỡng. Xem `samples/palette-khong-dung-
mau.html` cho giải pháp thay thế (small multiples) và ngưỡng kết luận đầy đủ.
