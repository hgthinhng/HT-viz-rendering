# Banking Regulatory Analysis

Bài về quy định ngân hàng, thay đổi Thông tư, NSFR/LDR/SFL/CAR, capital adequacy.

## Đặc trưng nội dung
- 1 ratio quy chiếu trần (LDR=85%, SFL=30%, NSFR=100%).
- 8-15 NHTM với metric đó.
- Có before/after policy change.
- Causal chain: policy → mechanism → bank impact → systemic effect.
- 2-3 phương án (Phương án A vs B kiểu StockLPT signature).
- Winners vs losers theo nhóm (Big4 vs tư nhân lớn vs nhóm C).
- Scenario discussion với probability.

## Chart families thường dùng

**Phần I - Tại sao có chuyện này:**
- `gauge` cho ratio signature (LDR=111,9% trần=85%) - hero stat mở Phần.
- `chart_dropcap` Wave 9 wrap gauge với drop cap T/M/V.
- `flow_bridge` explain why ratio đạt mức đó.

**Phần II - Đánh giá tình huống chi tiết:**
- `dot_plot_distribution` Wave 8 cho 12+ banks với threshold visible.
- `bar_horizontal` cho subset 5-6 bank focal.
- `heatmap` matrix bank × dimension impact.

**Phần III - Phương án A vs B:**
- `comparison_cards` summary 2 phương án.
- `policy_fork` decision factors matrix.
- `slopegraph` Wave 8 cho before/after policy theo n>=4 bank.

**Phần IV - Cuộc chơi phân phối:**
- `winners_losers_split` cột đối xứng.
- `heatmap` matrix detail.
- `before_after_comparison` cho 1-2 bank điển hình.

**Phần V-VI - Mechanism + Side effects:**
- `flow_bridge` cho counterintuitive chain (policy A → side effect Z).
- `mechanism_breakdown` 3-stage horizontal.
- `sankey_mini` Wave 8 cho capital flow change.

**Phần VII - Kịch bản + Action:**
- `scenario_cards` 3 outcomes với probability.
- `scenario_matrix` 2D Probability x Impact.
- `timeline_horizontal` hoặc `path_progression` Wave 9 lộ trình.
- `executive_summary_box` cuối bài (Thesis/Catalyst/Risk/Action).

## Composition pattern điển hình

Mở bài: `chart_dropcap(initial_letter="T", chart_html=gauge_html, ...)` (Phần I).
Giữa bài: alternation gauge → bar/dot → heatmap → flow_bridge → comparison.
Cuối bài: scenarios → timeline → executive_summary_box.

Total ~10-13 viz cho bài 15-20 trang.

## Examples gold-standard
- "Đề xuất sửa đổi Thông tư 22" - 7 Phần, 12 viz, hero stat 111,9%.
