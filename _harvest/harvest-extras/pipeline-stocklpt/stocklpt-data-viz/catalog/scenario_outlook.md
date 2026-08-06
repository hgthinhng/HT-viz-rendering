# `scenario_outlook` - bull/base/bear cổ phiếu, editorial phẳng (trigger/implication)

**Wave:** 1-3  
**Output:** HTML+CSS  
**Render:** `from viz import scenario_outlook`

---

## Khi nào dùng

- Kịch bản **cổ phiếu/định giá**: bull / base / bear với xác suất, mỗi cột có điều kiện kích hoạt + hệ quả EPS/định giá.
- Cuối bài deep dive doanh nghiệp, chốt 3 đường đi của thị giá theo từng giả định tăng trưởng.
- Khung kịch bản trung lập (không có "bên thắng / bên thua") — chỉ điều gì kích hoạt và hệ quả lên giá trị.

---

## Khi nào KHÔNG dùng

- **Kịch bản M&A / chính sách phân phối lợi ích** (ai hưởng lợi, ai chịu thiệt) - dùng `scenario_cards` (giữ field winners/losers cũ).
- Kịch bản có cả probability + impact 2 chiều - dùng `scenario_matrix` (2D P×I).
- Chỉ 2 nhánh quyết định - dùng `comparison_cards` hoặc `policy_fork`.
- >4 kịch bản - lưới quá hẹp, ép về 3 chính (up/flat/down).

---

## Thay thế `scenario_cards` cho equity

`scenario_outlook` **thay thế** `scenario_cards` kiểu cũ (vốn dựng theo khuôn M&A) khi đối tượng là **một cổ phiếu**:

| | `scenario_cards` (cũ, M&A) | `scenario_outlook` (mới, equity) |
|---|---|---|
| Khung tư duy | Phân phối lợi ích | Định giá cổ phiếu |
| Field đặc thù | winners / losers | **trigger / implication** (trung lập) |
| Tông | "bên thắng vs bên thua" | editorial phẳng, không phe |
| Polarity | theo phe | up / flat / down |

Dùng `scenario_outlook` cho bull/base/bear cổ phiếu; giữ `scenario_cards` cho kịch bản thương vụ/chính sách.

---

## Pair với (composition pattern)

- `capsule_verdict`: trang verdict mở đầu → `scenario_outlook` chống lưng bằng 3 đường đi.
- `quadrant_scatter`: định vị peer (P/B × ROE) rồi `scenario_outlook` cho mã trọng tâm.
- `marginalia`: chú thích giả định EPS/định giá từng kịch bản bên lề.

---

## Params

```python
scenario_outlook(
    scenarios: list[dict],  # mỗi dict 1 cột, xem shape bên dưới
    title: str = "",        # tiêu đề serif phía trên lưới (optional)
    subtitle: str = "",     # phụ đề xám dưới title (optional)
)

# shape mỗi scenario:
# {
#   "name": str,           # tên kịch bản (vd "Bull")
#   "tone": str,           # 'up' (xanh) | 'flat' (xám) | 'down' (đỏ)
#   "prob": str | number,  # xác suất hiển thị (vd "45%")
#   "thesis": str,         # 1 câu luận điểm
#   "trigger": str,        # "Điều kiện kích hoạt"
#   "implication": str,    # "Hệ quả EPS / định giá"
# }
```

Ghi rõ:
- `scenarios` bắt buộc; lý tưởng đúng 3 cột (bull/base/bear). `title`/`subtitle` optional.
- `tone` ngoài {`up`,`flat`,`down`} sẽ fallback về `flat` (xám). Rule màu: thanh `so-rule` + `prob` tô theo tone (up=`#21B36A`, down=`#E13453`, flat=`#645B76`).
- `prob` tự do (string/number) — engine in nguyên, **không** tự kiểm tổng = 100%.

---

## Code template

```python
from viz import scenario_outlook

html = scenario_outlook(
    scenarios=[
        {
            "name": "Bull", "tone": "up", "prob": "30%",
            "thesis": "Biên gộp hồi về 38% khi giá đầu vào hạ; sản lượng vượt kế hoạch 8%.",
            "trigger": "Giá HRC < 540 USD/tấn + tỷ giá ổn định dưới 25.500.",
            "implication": "EPS 2026 +22% lên 4.850đ; định giá fair 12,5x → giá mục tiêu 60.000đ.",
        },
        {
            "name": "Base", "tone": "flat", "prob": "50%",
            "thesis": "Sản lượng đi ngang, biên gộp giữ 34%; không có cú hích lẫn cú sốc.",
            "trigger": "Vĩ mô không đổi, đầu tư công giải ngân đúng tiến độ trung bình.",
            "implication": "EPS 2026 +9% lên 4.330đ; P/E 10x → giá mục tiêu 43.000đ.",
        },
        {
            "name": "Bear", "tone": "down", "prob": "20%",
            "thesis": "Cầu xây dựng yếu, biên gộp co về 30%; chi phí tài chính bào mòn lợi nhuận.",
            "trigger": "Giá HRC > 620 USD/tấn HOẶC tín dụng BĐS siết thêm.",
            "implication": "EPS 2026 -6% còn 3.730đ; de-rating về 8x → giá mục tiêu 30.000đ.",
        },
    ],
    title="Ba kịch bản thị giá HPG 2026",
    subtitle="Xác suất do StockLPT Research gán · cập nhật Q2/2026",
)

# Inject vào body
body += html
```

---

## Examples

### Example 1: Bull / Base / Bear cổ phiếu (đầy đủ)

Như Code template trên — 3 cột, thanh màu trên đầu (xanh/xám/đỏ), xác suất tô cùng màu, mỗi cột 2 hàng "Điều kiện kích hoạt" + "Hệ quả EPS / định giá".

Output: lưới 3 cột flex đều, rule màu phía trên mỗi cột, tên kịch bản serif + prob monospace cùng tông, thesis, rồi 2 hàng nhãn uppercase nhỏ.

### Example 2: 2 kịch bản (binary), bỏ title

```python
scenario_outlook(
    scenarios=[
        {"name": "Tái cấp phép", "tone": "up", "prob": "65%",
         "thesis": "Giấy phép khai thác gia hạn 10 năm.",
         "trigger": "Hồ sơ phê duyệt trước Q4/2026.",
         "implication": "EPS giữ 3.100đ, định giá fair 11x."},
        {"name": "Treo cấp phép", "tone": "down", "prob": "35%",
         "thesis": "Khai thác tạm dừng chờ rà soát.",
         "trigger": "Chậm phê duyệt qua 2027.",
         "implication": "EPS -40% còn 1.860đ, de-rating về 7x."},
    ],
)
```

Output: lưới 2 cột (không title/subtitle), vẫn cân vì `flex:1`.

(2-3 example là đủ.)

---

## Failure modes

- **Dùng nhầm cho kịch bản M&A** (cần winners/losers): `scenario_outlook` không có 2 field đó. Chuyển sang `scenario_cards`.
- **`tone` sai chính tả** (vd "bull", "positive"): không khớp {up/flat/down} → fallback xám, mất tín hiệu màu. Dùng đúng `'up'|'flat'|'down'`.
- **>4 cột**: mỗi cột co hẹp, chữ tiếng Việt xuống dòng vỡ. Ép về 3 kịch bản chính.
- **`prob` tổng ≠ 100%**: engine không cảnh báo; tự kiểm cho hợp lý trước khi truyền (bull+base+bear nên = 100%).

---

## Notes

- **Editorial phẳng**: cố ý không có khung "thắng/thua" — đây là khác biệt với `scenario_cards`. Field trung lập `trigger` (Điều kiện kích hoạt) + `implication` (Hệ quả EPS / định giá).
- Nhãn 2 hàng cố định trong code: "Điều kiện kích hoạt" và "Hệ quả EPS / định giá" — phù hợp khung định giá cổ phiếu.
- **Polarity màu**: up=`#21B36A`, down=`#E13453`, flat=`#645B76`. Brand remap palette ở `render_pdf` — hex là source space, không truyền brand vào component.
- `page-break-inside:avoid` — cả lưới giữ trên 1 trang; tên kịch bản dùng serif PFD, prob dùng JetBrains Mono.
