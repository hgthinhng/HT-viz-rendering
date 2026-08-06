# viz_charts - Chart định lượng (matplotlib) · Wave 12

> **Khác biệt với phần còn lại của catalog:** các component dưới đây render bằng
> **matplotlib → PNG base64** (không phải inline SVG/HTML). Dùng cho dữ liệu định
> lượng THẬT mà atom inline không vẽ tốt: time-series nhiều điểm, ranking, diverging,
> waterfall tính toán, scatter. Tự theme theo brand đang active (remap palette qua
> `_brand.py`): up = emerald, down = đỏ, chrome/neutral = forest accent, structure = ink.
> Font khớp report (Spectral / Be Vietnam Pro / IBM Plex Mono).

Module: `viz_charts` · Style fn: `chart_styles` (đã wire trong orchestrator `_build_css`).
Mỗi component trả về `<figure class="lpt-chart"><img base64></figure>` — gọi qua viz_plan
như mọi component khác.

## Khi nào dùng (parsimony: mỗi chart phải DẠY một điều, không trang trí)

| Data shape | Component |
|---|---|
| Xu hướng theo thời gian / đường trong phiên | `chart_line` |
| Dòng ròng mua/bán, chênh lệch +/- theo nhóm | `chart_diverging` |
| Xếp hạng giá trị (top GTGD, đóng góp điểm) | `chart_bar_h` |
| Phân rã (P&L bridge, điểm số cấu thành) | `chart_waterfall` |
| So sánh nhiều nhóm × nhiều kỳ | `chart_bar_grouped` |
| Tương quan 2 biến (P/B × ROE) | `chart_scatter` |

## Params

### chart_line
```
series: list[float]              # bắt buộc - chuỗi giá trị
x_labels: list[str] = None       # nhãn trục x (bỏ -> không hiện)
markers: [[index, "nhãn", "top"|"bottom"], ...]   # chấm + nhãn điểm (mono)
ref: float = None                # đường tham chiếu ngang (vd giá mở cửa)
ref_label: str = None            # nhãn cho đường ref
up: bool = True                  # True -> emerald, False -> đỏ
y_format: "num"|"pct"|"cur"      # định dạng trục y; currency="₫"/"$" khi "cur"
title, caption: str
```

### chart_diverging
```
items: [{"name": "VIC", "value": 114}, {"name": "FPT", "value": -112}, ...]  # bắt buộc
unit: str = ""                   # vd "tỷ" -> nhãn "+114 tỷ"
y_format, currency, title, caption
# value > 0 emerald, < 0 đỏ; tự sort; đường zero = ink.
```

### chart_bar_h
```
items: [{"name","value"}, ...]   # bắt buộc - tự sort
highlight: str = None            # tên item tô emerald nổi bật; còn lại forest
unit, y_format, currency, title, caption
```

### chart_waterfall
```
steps: [{"name","value","kind"}]  # kind in {"start","delta","total"}
# delta + -> emerald, - -> đỏ; start/total -> ink.
y_format, currency, title, caption
```

### chart_bar_grouped
```
categories: ["Q1","Q2",...]
series: [{"name","values":[...]}, ...]   # <=4 series
highlight: str = None            # tên series tô emerald
y_format, currency, title, caption
```

### chart_scatter
```
points: [{"x","y","label"(opt),"up"(opt bool)}, ...]
quadrant: bool = False           # vẽ đường trung vị chia 4 góc
x_label, y_label, x_format, y_format, title, caption
```

## Ví dụ viz_plan entry
```json
{
  "component": "chart_diverging",
  "module": "viz_charts",
  "position": "section-2",
  "params": {
    "items": [{"name":"VIC","value":114},{"name":"LPB","value":33},
              {"name":"CTG","value":-103},{"name":"FPT","value":-112}],
    "unit": "tỷ",
    "title": "Khối ngoại: gom Vingroup, xả ngân hàng & FPT",
    "caption": "Top giao dịch ròng khối ngoại HOSE. Ròng toàn sàn -611 tỷ."
  }
}
```

## Quy tắc
1. Số liệu trong params khớp prose từng chữ số. Title nêu INSIGHT, không phải tên metric trống.
2. Caption tiếng Việt, không em-dash. Nhãn chart dùng tiếng Việt (tránh ký tự Hy Lạp như Δ - một số font thân không có glyph).
3. Parsimony: chỉ thêm chart khi bảng/atom inline không truyền tải được. 2-4 chart/bài là đủ.
4. Không hardcode hex trong params - màu tự theo brand.
