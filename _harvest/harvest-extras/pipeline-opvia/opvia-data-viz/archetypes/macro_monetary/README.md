# Macro & Monetary Analysis

Bài về vĩ mô tiền tệ: GDP, CPI, FX, lãi suất chính sách, money supply.

## Đặc trưng nội dung
- Time series 8-24 quý/tháng dữ liệu.
- Multi-metric co-plot (GDP + CPI + FX + Rate).
- Forecast với uncertainty band.
- Regime shifts (COVID, war, monetary cycle).
- Cross-country comparison.

## Chart families thường dùng

**Mở bài:**
- `infographic_panel` Wave 10 hero stat macro.
- `narrative_strip` Wave 10 4-panel snapshot (GDP/CPI/FX/Rate).

**Time series core:**
- `line_with_annotations` Wave 8 với 2-4 annotations regime shifts.
- `compass_callout` wrap line chart bằng editorial caption.
- `small_multiples_grid` Wave 8 cho cross-country / cross-period.

**Phân phối & comparison:**
- `dot_plot_distribution` cross-country comparison (CPI 30 nước).
- `quadrant_scatter` Phillips curve, Taylor rule scatter.

**Mechanism:**
- `flow_bridge` cho transmission mechanism (Fed cut → DXY → VND → CPI).
- `sankey_mini` cho money flow.

**Forecast:**
- `scenario_cards` base/bull/bear với explicit probability.
- `path_progression` Wave 9 cho expected policy timeline.

**Cuối bài:**
- `executive_summary_box` 4-quadrant thesis.

## Composition pattern điển hình

Mở: `narrative_strip` 4-metric snapshot.
Mid: `line_with_annotations` cho mỗi metric chính + `marginalia` methodology.
Mechanism: `flow_bridge` transmission.
Forecast: `scenario_cards` + `path_progression`.

Cẩn thận: macro analysis dễ trở thành "data dumping". Mỗi chart phải có takeaway rõ.

## Notes
- Ratio < 1% nên dùng bps không phải %.
- FX rate dùng monospace JetBrains Mono.
