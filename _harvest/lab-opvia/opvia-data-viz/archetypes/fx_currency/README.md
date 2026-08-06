# FX & Currency Analysis

Bài về tỷ giá: DXY, USD/VND, cross rates, REER, intervention.

## Đặc trưng nội dung
- Time series rate với volatility.
- Cross rate matrix.
- Carry trade context (rate differential).
- Central bank intervention timeline.
- Real effective exchange rate.

## Chart families thường dùng

**Rate history:**
- `line_with_annotations` Wave 8 cho USD/VND với SBV intervention pivots.
- `small_multiples_grid` cho cross rates (USD/VND, EUR/VND, JPY/VND, CNY/VND).

**Differential & carry:**
- `quadrant_scatter` vol vs rate differential.
- `slopegraph` carry trade profitability before/after.

**REER:**
- `line_with_annotations` REER với equilibrium band.
- `bar_horizontal` REER deviation by trading partner.

**Mechanism:**
- `flow_bridge` Fed cut → DXY → VND → CPI transmission.
- `mechanism_breakdown` SBV policy reaction function.

**Intervention:**
- `timeline_horizontal` intervention events với size annotations.
- `path_progression` Wave 9 expected SBV policy path.

**Forecast:**
- `scenario_cards` base/strong USD/weak USD.
- `executive_summary_box`.

## Composition pattern

Mở: USD/VND chart + DXY trend.
Mid: cross rates + driver analysis.
Cuối: forecast + position recommendation.
