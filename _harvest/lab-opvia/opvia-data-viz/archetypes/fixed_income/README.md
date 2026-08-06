# Fixed Income Analysis

Bài về thị trường trái phiếu, lợi suất, credit spread, duration.

## Đặc trưng nội dung
- Yield curve shape (normal/inverted/flat).
- Spread movements (TPCP - corp bond).
- Duration & convexity profile.
- Issuance schedule, supply-demand.
- Credit migration matrix.

## Chart families thường dùng

**Yield curve:**
- `line_with_annotations` cho yield curve 1M-30Y với key tenors.
- `small_multiples_grid` Wave 8 cho yield curve theo tháng (rotation viewing).
- (Tương lai: dedicated `yield_curve` component sẽ tốt hơn).

**Spreads:**
- `line_with_annotations` cho time series spread.
- `heatmap` cho rating × tenor spread matrix.
- `slopegraph` Wave 8 spread before/after rating change.

**Duration profile:**
- `quadrant_scatter` duration vs yield.
- `bar_horizontal` duration ranking 10 issuers.

**Issuance:**
- `timeline_horizontal` issuance schedule.
- `waterfall` net issuance walk (gross issue - maturity).
- `sankey_mini` capital flow nhà đầu tư → issuer.

**Mechanism:**
- `flow_bridge` cho macro driver → yield (CPI → rate → curve shift).

**Cuối:**
- `scenario_cards` rate forecast scenarios.
- `executive_summary_box`.

## Composition pattern

Mở: yield curve hiện tại + spread snapshot.
Mid: history + driver mechanism.
Cuối: forecast scenarios + duration positioning.

## Notes
- bps formatting bắt buộc (không dùng % cho rate < 1%).
- Yield curve cần fixed scale tránh distort.
