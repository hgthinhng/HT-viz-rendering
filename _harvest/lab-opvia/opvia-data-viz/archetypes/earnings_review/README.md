# Earnings Review Analysis

Bài review quarterly earnings: beat/miss, segment, guidance change.

## Đặc trưng nội dung
- Actual vs consensus vs prior year.
- Segment breakdown.
- Margin trend.
- Guidance update.
- Stock reaction.

## Chart families thường dùng

**Headline:**
- `stat_dashboard` 4-6 KPI summary (Revenue / EPS / Margin / ROE).
- `data_hero` EPS surprise %.

**Beat/miss:**
- `waterfall` actual vs consensus walk.
- `bar_horizontal` segment beat/miss.
- `quadrant_scatter` revenue surprise vs EPS surprise (peer).

**Segment:**
- `bar_horizontal` segment revenue/profit.
- `heatmap` segment x metric matrix.
- `treemap` (future) segment proportional.

**Margin trend:**
- `line_with_annotations` margin Q-on-Q với annotations.
- `slopegraph` segment margin Q-1 vs Q.

**Guidance:**
- `before_after_comparison` old guidance vs new.
- `scenario_cards` next quarter scenarios.

**Reaction:**
- `line_with_annotations` stock price intraday + after-hours.

**Cuối:**
- `executive_summary_box`.

## Composition pattern

Mở: headline KPI dashboard + EPS surprise hero.
Mid: segment breakdown + margin trend.
Cuối: guidance update + outlook.

Total ~6-9 viz cho bài 6-10 trang earnings review (gọn hơn deep analysis).
