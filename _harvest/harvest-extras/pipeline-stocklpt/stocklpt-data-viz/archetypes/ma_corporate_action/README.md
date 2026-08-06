# M&A & Corporate Action Analysis

Bài về deal M&A, premium, accretion-dilution, integration.

## Đặc trưng nội dung
- 2 entities (acquirer + target).
- Premium calculation.
- Synergy estimation.
- Pro-forma financials.
- Deal timeline.

## Chart families thường dùng

**Deal overview:**
- `data_hero` deal value hero.
- `comparison_cards` acquirer vs target snapshot.

**Premium:**
- `waterfall` premium breakdown (cash + stock + earnout).
- `bar_horizontal` premium vs precedent transactions.

**Synergy:**
- `waterfall` synergy walk Year 1 → Year 5.
- `mechanism_breakdown` revenue synergy + cost synergy.

**Pro-forma:**
- `before_after_comparison` standalone vs pro-forma key metrics.
- `slopegraph` peer ranking before/after deal.

**Capital flow:**
- `sankey_mini` consideration flow (cash + shares to target shareholders).

**Timeline:**
- `timeline_horizontal` deal milestones (announce → due dilig → close → integrate).
- `path_progression` Wave 9 integration phases.

**Risk:**
- `scenario_matrix` integration risk Probability x Impact.
- `risk_radar` deal risk multi-dim.

**Cuối:**
- `executive_summary_box`.

## Composition pattern

Mở: deal hero + comparison cards.
Mid: premium + synergy.
Cuối: timeline + risk + action.
