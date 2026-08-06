# EIR Component Catalog (48 total: viz_eir 21 + stats/diagram/panels/kpi 27) — core module `viz_eir.py`

Render: `python3 scripts/viz_eir.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]`
· list: `--list`. Spec contract is identical to the core renderer; a note may mix core +
EIR components in one `spec.json`. Every component accepts the furniture keys
`title, kicker, subtitle, source, asof, rating, firm` and `accent` (overrides theme), plus
`y_format` ∈ `num|pct|cur|x|bps`, `currency`, `dp` where numeric labels apply.

## Advisor — pick by the analytical job (data shape → component)

| The job you're teaching | Component(s) | Notes |
|---|---|---|
| Before → after, or A vs B, across categories | `dumbbell` | the GAP is the point; cleaner than paired bars |
| Rank magnitudes (leaner than bars) | `lollipop` | drop-in upgrade over a plain bar for contribution/attribution |
| Signed values around zero (beat/miss, active return) | `diverging_bar` | teal + / brick − |
| Point estimate + interval / range across rows | `range_dot` | forecast ranges, 52-week range, CI/forest |
| Rank changes over time | `bump` | rating migration, sector-weight re-ranking |
| Forecast with widening uncertainty | `fan` | Monte-Carlo, inflation/rate forecast, retirement wealth |
| A *difference* is the subject (spread/basis) | `spread` | 10Y−2Y, credit spread, ROIC−WACC |
| Compare series of different scale | `index100` | total-return rebased to 100 |
| X–Y relationship *moving over time* | `connected_scatter` | Phillips curve, rates vs inflation path |
| Compare distributions (spread/skew) | `boxplot` | return dispersion across asset classes/funds |
| Concentration / inequality | `lorenz` | portfolio-weight concentration, Gini, credit-loss curve |
| One KPI vs a target and qualitative bands | `bullet` | coverage vs covenant, funded ratio (better than a gauge) |
| Triangulate many valuation methods vs price | `football_field` | the iconic sell-side valuation chart |
| Refinancing "wall" by year | `maturity_ladder` | debt maturities, optionally stacked by instrument |
| Multiple vs a driver + best-fit | `comps_scatter` | EV/EBITDA vs growth, PEG-style relative value |
| Share × size in one view (segmentation) | `marimekko` | revenue by region × product |
| 2-variable sensitivity (conditional-format grid) | `sensitivity_grid` | DCF: WACC × g → value, base case boxed |
| Dense peer comparison "monitor" | `cond_table` | comps table, cells shaded best→worst per column |
| One-line KPI header snapshot | `kpi_strip` | ROE / margin / D-E / coverage with ▲▼ |
| The one framing number | `hero_stat` | WACC, fair-value gap |
| One-page executive summary | `exec_dashboard` | Morningstar/Bloomberg composite (the showpiece) |

> Parsimony still rules: this table helps you pick the *right* chart when the data already
> calls for a visual — it is not a checklist to fill. See `EIR_DESIGN.md`.

## Params reference (data keys per component)

**comparison / ranking**
- `dumbbell` — `categories[], before[], after[], left_name, right_name, sort('after'|'delta')`
- `lollipop` — `categories[], values[], sort(bool|'asc'), highlight`
- `diverging_bar` — `categories[], values[](signed), sort(bool)`
- `range_dot` — `rows[{label, point, lo, hi}], ref, ref_label, show_values`
- `bump` — `periods[], entities{name:[ranks]}, highlight[names]`

**time / trend**
- `fan` — `hist_x[], hist_y[], fcast_x[], median[], bands[{lo[],hi[],label}], split_label`
- `spread` — `x[], series_a{name,values}, series_b{name,values}` **or** `diff{name,values}`
- `index100` — `x[], series[{name,values}], rebase(bool,default true), base(100)`
- `connected_scatter` — `points[{x,y,label}] (time order), x_label, y_label`

**distribution**
- `boxplot` — `groups[{name, data[]}]`
- `lorenz` — `values[], x_label, y_label` (Gini auto-computed & badged)

**KPI vs target**
- `bullet` — `rows[{label, actual, target, bands[3 upper limits]}]`

**sell-side archetypes**
- `football_field` — `methods[{name, low, high}], current, target`
- `maturity_ladder` — `years[], series[{name, values[]}]` (1+ = stacked by instrument)
- `comps_scatter` — `points[{x,y,label,highlight}], x_label, y_label, fit(bool)`

**part-to-whole / tables**
- `marimekko` — `columns[{name, size}], segments[], data[[seg×col values]]` (per-column renormalised)
- `sensitivity_grid` — `row_label, col_label, rows[], cols[], values[][], base[ri,ci], diverging(bool)`
- `cond_table` — `columns[](first=label), rows[[label, v1, …]], higher_better[bool per col], fmt_cols[kind per col]`

**editorial**
- `kpi_strip` — `items[{label, value, delta, tone(up|down|flat)}]`
- `hero_stat` — `value, label, delta, tone, context`
- `exec_dashboard` — `kpis[], trend{title,x,series[]}, rank{title,categories,values,fmt}, panel_left{kind,…}, panel_right{kind,…}` (mini `kind` ∈ bars|diverging|dumbbell|donut; every region optional)

## Deliberate omissions (critical calls, not gaps)

- **Radar / spider** — matplotlib radar needs a custom projection, the polygon frame
  misaligns, and area encodes as radius² (perceptually dishonest). For multi-metric
  company/factor comparisons use `bump`, `dumbbell`, or a small-multiples bar grid instead.
- **Standalone gauge/dial** — lots of ink for one number with no context. `bullet` is the
  strictly-better KPI-vs-target substitute and is included.
- **Sparkline-in-table** — high fiddliness for moderate value; `cond_table` covers the
  dense-comparison need. Candidate for a later pass if a real note demands it.

---

# Super-viz-factory additions (27) — modules stats · diagram · panels · kpi

Rendered through the same `spec.json` contract via the unified dispatcher
`scripts/viz_super.py` (merges all 48 EIR components; `--list` to enumerate). Core
primitives still render via `note-pipeline-viz/scripts/viz_render_py.py`.

## Advisor — additional data-shape → component

| The job you're teaching | Component | Module |
|---|---|---|
| Pairwise correlation across many series | `correlation_matrix` | stats |
| A distribution + its VaR / CVaR tail | `distribution` | stats |
| Which assumption swings value most | `tornado` | stats |
| Is a monitored metric in control? | `spc_control_chart` | stats |
| Seasonal pattern (mean + range) | `seasonality` | stats |
| OHLC price action | `candlestick` | stats |
| Credit spread by rating bucket | `spread_ladder` | stats |
| Decision under uncertainty (EV rollback) | `decision_tree` | diagram |
| A yes/no procedure | `flowchart` | diagram |
| Layered structure (pool→SPV→tranches) | `network_graph` | diagram |
| Input → process → output mechanism | `mechanism_flow` | diagram |
| Cause → effect chain to one result | `flow_bridge` | diagram |
| Sources → uses flows (width ∝ value) | `sankey` | diagram |
| A dated milestone roadmap | `timeline` | diagram |
| Binomial option-pricing lattice | `lattice` | diagram |
| 2×2 themed takeaway brief | `executive_summary` | panels |
| Bear / base / bull with probabilities | `scenario_cards` | panels |
| Strengths/Weaknesses/Opps/Threats | `swot` | panels |
| Two instruments/approaches side-by-side | `comparison` | panels |
| Multiplicative decomposition (ROE=…) | `dupont` | panels |
| One metric, two-state transition + delta | `before_after` | panels |
| Covenant/compliance pass-warn-breach | `status_strip` | panels |
| KPI cells with mini trends | `kpi_card_with_sparkline` | kpi |
| Many metrics compactly, inline sparkline | `sparkline_row` | kpi |
| Commentary where the numbers must pop | `annotated_narrative` | kpi |
| Flag + explain one spike/anomaly | `anomaly_callout` | kpi |
| Big-stat header w/ mini spark or bars | `stat_dashboard` | kpi |

## Params reference (additions)

**stats**
- `correlation_matrix` — `labels[], values[][]` (full or lower-tri; upper masked), `short_labels[]`
- `distribution` — `mean, sd, var_pct(0.05)` or `data[]`; `y_format, currency, x_label`
- `tornado` — `base, rows[{label, low, high}], base_label, x_label, y_format`
- `spc_control_chart` — `x[], values[], center, ucl, lcl` (±3σ auto if omitted), `series_name, y_format`
- `seasonality` — `periods[], mean[], lo[], hi[], peak_label, trough_label, y_format`
- `candlestick` — `rows[{label,o,h,l,c}], y_label, y_format`
- `spread_ladder` — `ratings[], spreads_bps[], ref, ref_label, highlight`

**diagram**
- `decision_tree` — `tree{label, kind:decision|chance|leaf, prob, value/ev, tone, optimal, children[]}, layer_labels[]`
- `flowchart` — `nodes[{id,kind:start|process|decision|terminal,label,x,y,w,h,tone}], edges[{from,to,from_side,label}]`
- `network_graph` — `layers[[{id,label,tone,w}]], edges[{from,to,label}]`
- `mechanism_flow` — `stages[{tone:input|process|output, kicker, title, bullets[], footer}]`
- `flow_bridge` — `steps[{text, sub, tone:up|down|result}]`
- `sankey` — `sources[{name,value,color}], targets[{name,value}], flows[{src,dst,value}], src_header, dst_header, currency`
- `timeline` — `milestones[{date, title, caption, done}]`
- `lattice` — `levels[[values]], up_factor, down_factor, up_prob, x_labels[]`

**panels**
- `executive_summary` — `quadrants[{title, tone, body, headline}]` (len 4), `emphasize`
- `scenario_cards` — `cards[{name, prob, value, tone, bullets[], emphasize, badge}], value_label`
- `swot` — `strengths[], weaknesses[], opportunities[], threats[]` (3-4 each), `labels`
- `comparison` — `left{title, items[{text, sub}]}, right{...}, left_tone, right_tone`
- `dupont` — `result{label, value}, factors[{label, value, sub, fmt}]`
- `before_after` — `left{value,label}, right{value,label}, delta, tone, caption, pct_change`
- `status_strip` — `rows[{metric, value, threshold, status}], status_colors, status_labels`

**kpi**
- `kpi_card_with_sparkline` — `cards[{label, value, delta, tone, spark[], caption}], ncols`
- `sparkline_row` — `rows[{label, spark[], value, tone, status}]`
- `annotated_narrative` — `runs[[text, tone|None, bold]]` (tone up|down|emphasis|None), `fontsize, line_h`
- `anomaly_callout` — `x[], values[], anomaly_index, note{kicker, headline, body, dx, dy, negative}, y_format`
- `stat_dashboard` — `stats[{label, value, delta, tone, caption, spark[]|bars[]}], per_row`
