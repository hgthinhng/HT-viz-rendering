# `capsule_verdict` - trang hero magazine 1 verdict + mega-number duotone

**Wave:** 1-3  
**Output:** HTML+CSS (full-page, `page-break-after:always`)  
**Render:** `from viz import capsule_verdict`

---

## Khi nào dùng

- Mở/đóng bài deep dive doanh nghiệp bằng 1 trang verdict signature: ticker + lập trường + 1 mega-number rủi ro.
- Cần "tờ bìa quan điểm" gói gọn nguyên luận điểm thành 1 con số đắt (VIX=34, P/E=28x, nợ/EBITDA=4,1x).
- Verdict card mở Phần định giá hoặc trang chốt khuyến nghị (Mua/Giữ/Bán) với 3 metric phụ + 1 tín hiệu theo dõi.

---

## Khi nào KHÔNG dùng

- Chỉ có 1 ratio quy chiếu trần, không phải verdict cả doanh nghiệp - dùng `gauge` (atomic, không chiếm cả trang).
- Cần nhồi 4-6 KPI ngang nhau - dùng `dashboard_grid` (Wave 10) hoặc `stat_dashboard` (Wave 1).
- Mega-number không phải verdict (chỉ là 1 stat trong dòng prose) - dùng `data_hero` hoặc `infographic_panel`.
- Bài daily report - component này quá nặng, chiếm trọn 1 trang A4; daily dùng `dashboard_grid`.

---

## Pair với (composition pattern)

- `scenario_outlook`: trang sau capsule liệt kê bull/base/bear chống lưng cho verdict.
- `marginalia`: chú thích methodology cách tính mega-number bên lề trang kế.
- `back_cover_cta`: capsule mở bài → nội dung → `back_cover_cta` đóng, đối xứng visual.

---

## Params

```python
capsule_verdict(
    ticker: str,            # mã / nhãn lớn góc trái (vd "VN30 · VIX")
    meta: str,              # dòng meta nhỏ cạnh ticker (vd "Ngân hàng · HOSE")
    stance_label: str,      # nhãn lập trường, fill bằng stance_hex (vd "THẬN TRỌNG")
    stance_hex: str,        # màu nền chip lập trường (vd "#C8972E")
    risk_label: str,        # chip rủi ro viền (vd "Rủi ro: Cao")
    mega_value,             # con số hero khổng lồ (str/number, vd "34,2")
    mega_unit: str,         # đơn vị bám sau mega (vd "pts", "x", "%")
    stat_lead: str,         # caption nhỏ phía trên main, cạnh mega
    stat_main: str,         # caption chính cạnh mega - CHO PHÉP HTML (không escape)
    stat_sub: str,          # caption phụ phía dưới main
    thesis: str,            # 1 câu luận điểm dưới lockup
    metrics: list[dict],    # tile phụ: [{"value", "label", "note"}]
    signal: str,            # 1 dòng "Tín hiệu theo dõi" ở block cuối
    mega_accent: str = "#c8972e",  # MÀU MEGA-NUMBER (duotone) - xem polarity bên dưới
    kicker: str = "StockLPT Research · Quan điểm doanh nghiệp",  # eyebrow trên lockup
)
```

Ghi rõ:
- Tất cả param trước `mega_accent` đều **bắt buộc**. `metrics` nên đúng 3 phần tử (layout cân nhất); 2-4 vẫn render.
- `mega_accent` là điểm nhấn duotone của con số hero - **chọn theo polarity rủi ro**, không phải mặc định.
- `stat_main` **không bị escape** (cho phép `<em>`, `<strong>`); mọi field còn lại được escape an toàn.

---

## Code template

```python
from viz import capsule_verdict

html = capsule_verdict(
    ticker="VN30 · VIX",
    meta="Đo lường nỗi sợ thị trường · HOSE",
    stance_label="THẬN TRỌNG",
    stance_hex="#C8972E",
    risk_label="Rủi ro: Cao",
    mega_value="34,2",
    mega_unit="pts",
    stat_lead="Chỉ số biến động ngụ ý",
    stat_main="Vùng <em>căng thẳng</em> — trên ngưỡng 30 lần đầu kể từ Q3",
    stat_sub="Trung bình 10 năm: 18,4 pts",
    thesis="VIX phá 30 đồng nghĩa thị trường định giá lại rủi ro đuôi; pha de-risking thường kéo 4–6 tuần.",
    metrics=[
        {"value": "+86%", "label": "vs TB 10 năm", "note": "18,4 → 34,2"},
        {"value": "4–6 tuần", "label": "độ dài pha de-risk", "note": "trung vị lịch sử"},
        {"value": "-7,3%", "label": "VN-Index từ đỉnh", "note": "drawdown đang chạy"},
    ],
    signal="Theo dõi VIX về dưới 25 làm mốc xác nhận risk-on quay lại.",
    mega_accent="#C0392B",  # đỏ: con số rủi ro CAO
)

# Inject vào body (đây là 1 TRANG độc lập)
body += html
```

---

## Examples

### Example 1: Verdict rủi ro cao (VIX-style) — mega đỏ

```python
capsule_verdict(
    ticker="VN30 · VIX",
    meta="Đo lường nỗi sợ thị trường · HOSE",
    stance_label="THẬN TRỌNG",
    stance_hex="#C8972E",
    risk_label="Rủi ro: Cao",
    mega_value="34,2", mega_unit="pts",
    stat_lead="Chỉ số biến động ngụ ý",
    stat_main="Vùng <em>căng thẳng</em>",
    stat_sub="Trung bình 10 năm: 18,4 pts",
    thesis="VIX phá 30 — thị trường định giá lại rủi ro đuôi.",
    metrics=[{"value": "+86%", "label": "vs TB 10 năm", "note": "18,4 → 34,2"}],
    signal="VIX về dưới 25 = risk-on quay lại.",
    mega_accent="#C0392B",
)
```

Output: trang full A4, ticker khổng lồ góc trên, chip "THẬN TRỌNG" nền gold + chip "Rủi ro: Cao" viền, mega-number `34,2` đỏ duotone giữa trang, 1 thesis, hàng tile metric, block "Tín hiệu theo dõi" cuối trang.

### Example 2: Verdict định giá căng (P/E) — mega gold cảnh báo

```python
capsule_verdict(
    ticker="FPT",
    meta="Công nghệ · HOSE",
    stance_label="GIỮ",
    stance_hex="#645B76",
    risk_label="Rủi ro định giá: Trung bình–Cao",
    mega_value="28,4", mega_unit="x",
    stat_lead="P/E forward 2026",
    stat_main="Giao dịch ở <strong>+1,5 độ lệch chuẩn</strong> trên trung bình 5 năm",
    stat_sub="Trung bình 5 năm: 19,1x",
    thesis="Tăng trưởng EPS 20% đã phản ánh phần lớn vào giá; dư địa re-rating mỏng.",
    metrics=[
        {"value": "19,1x", "label": "P/E TB 5 năm", "note": "vùng tham chiếu"},
        {"value": "20%", "label": "CAGR EPS kỳ vọng", "note": "2025–2027"},
        {"value": "1,4x", "label": "PEG", "note": "không còn rẻ"},
    ],
    signal="Chiết khấu về dưới 24x mở lại điểm vào hấp dẫn.",
    mega_accent="#C8972E",  # gold caution: đắt nhưng chưa nguy hiểm
)
```

Output: cùng layout, mega `28,4x` tô gold cảnh báo (không phải xanh — đây là con số "đắt").

(2-3 example là đủ.)

---

## Failure modes

- **`mega_accent` để xanh (#16633C) cho 1 con số rủi ro**: xanh = tích cực trong palette StockLPT, đọc giả hiểu ngược. Con số rủi ro/đắt → gold `#C8972E` (cảnh báo) hoặc đỏ `#C0392B` (nguy hiểm); chỉ dùng xanh khi mega thật sự là tin tốt (vd ROE cao, biên LN nở).
- **`metrics` rỗng hoặc >4 phần tử**: hàng tile vỡ cân. Giữ đúng 3 (2-4 chấp nhận được).
- **`stat_main` chèn HTML lỗi/không đóng thẻ**: vì field này KHÔNG escape, thẻ hở sẽ phá layout cả trang. Chỉ dùng `<em>`/`<strong>` đóng đúng cặp; nội dung do người nhập kiểm soát.
- **Nhồi 2 capsule liên tiếp**: mỗi capsule là 1 trang (`page-break-after:always`) → ra 2 trang trắng nhiều khoảng. Dùng tối đa 1-2 lần/bài (mở + chốt).

---

## Notes

- **Full-page**: section bọc `.cv-page{page-break-after:always}` — luôn ngắt sang trang mới sau capsule. Đây là 1 TRANG, không phải 1 block giữa prose.
- **Duotone**: chỉ riêng mega-number nhận `mega_accent`; phần còn lại giữ ink `#2A1A4A`. Đây là điểm nhấn duy nhất của trang — chọn màu có chủ đích.
- **Polarity màu (palette StockLPT)**: ink `#2A1A4A`, gold cảnh báo `#C8972E`, mint `#16633C` (tích cực), đỏ nguy hiểm `#C0392B`. Mega rủi ro → gold/đỏ; mega tin tốt → mint.
- **Brand remap**: hex ở đây là source space; khi brand `stocklpt` active, `_brand.py` remap palette + wordmark ở bước `render_pdf` — không truyền brand vào component.
- 4 block phân bố đều theo chiều dọc trang (head / hero lockup / metrics / signal); font hero dùng family lockup khổ lớn, caption phụ dùng serif PFD.
