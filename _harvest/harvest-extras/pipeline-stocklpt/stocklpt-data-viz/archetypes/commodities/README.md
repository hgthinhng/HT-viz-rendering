# Commodities Analysis

Bài về hàng hóa: dầu, vàng, nông sản, kim loại.

## Đặc trưng nội dung
- Spot price + futures curve (contango/backwardation).
- Seasonality patterns.
- Inventory levels.
- Supply-demand fundamentals.

## Chart families thường dùng

**Price history:**
- `line_with_annotations` cho spot price với key events.
- `small_multiples_grid` cho seasonality (cùng month qua nhiều năm).

**Futures curve:**
- `line_with_annotations` futures curve M+1 đến M+12 (contango shape).
- `slopegraph` curve shift before/after.
- (Tương lai: dedicated `contango_curve` component).

**Inventory:**
- `line_with_annotations` cho inventory level vs 5Y average band.
- `dot_plot_distribution` regional inventory comparison.

**Supply-demand:**
- `waterfall` net change breakdown.
- `sankey_mini` flow producer → consumer.
- `mechanism_breakdown` supply chain.

**Forecast:**
- `scenario_cards`.
- `executive_summary_box`.

## Composition pattern

Mở: price chart + futures curve snapshot.
Mid: fundamentals (inventory, supply-demand).
Cuối: scenarios + trading recommendation.

## Notes
- Đơn vị quan trọng: USD/bbl, USD/oz, USD/MT, ...
- Seasonality cần normalized scale.
