# Sector Deep Dive

Bài deep dive 1 ngành: thép, bán lẻ, BĐS, năng lượng, IT, banking sector overview.

## Đặc trưng nội dung
- 8-30 stocks trong ngành, thường top 10 focal.
- Sector economics: supply-demand dynamics, margin structure, value chain.
- Peer comparison metrics: P/B, P/E, ROE, growth.
- Sector rotation context (vs other sectors).

## Chart families thường dùng

**Sector overview:**
- `treemap` (nếu có - chưa trong catalog hiện tại) cho proportional weight.
- `ranking_ladder` ranking với delta vs prev period.
- `narrative_strip` Wave 10 4-metric snapshot ngành.

**Peer comparison:**
- `quadrant_scatter` Wave 8 cho 2D peer (P/B vs ROE).
- `dot_plot_distribution` Wave 8 cho metric distribution 30 stocks.
- `bar_horizontal` cho top 5-6 focal.

**Time series & history:**
- `line_with_annotations` cho sector index 5 năm với cycle annotations.
- `small_multiples_grid` Wave 8 cho key metric across 8-12 stocks.

**Value chain:**
- `mechanism_breakdown` Input → Process → Output (raw material → product → market).
- `sankey_mini` cho supply chain flow.
- `flow_bridge` cho margin walk.

**Catalysts & risks:**
- `scenario_cards` outlook scenarios.
- `risk_radar` multi-axis profile.

**Cuối:**
- `executive_summary_box` Thesis/Catalyst/Risk/Action cho ngành.

## Composition pattern điển hình

Mở: sector snapshot strip + peer scatter.
Mid: deep dive 2-3 stocks focal với gauge / data_hero.
Cuối: scenarios + action items.

Total ~8-12 viz cho bài 12-18 trang.
