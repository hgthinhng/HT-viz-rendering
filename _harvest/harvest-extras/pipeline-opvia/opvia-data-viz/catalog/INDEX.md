# Catalog Index - Opvia Data Viz

33 component spread Wave 1-10 + 2 page templates. **Skim trang này trước khi deep-read spec cụ thể.**

---

## Page templates (LUÔN dùng cho bài publish-ready)

| Template | One-liner | Bắt buộc cho |
|---|---|---|
| `cover_deep_page` | Trang bìa Prussian-900 với hero stat + 3 takeaways | Mọi deep analysis (trừ daily report) |
| `back_cover_cta` | Trang kết với CTA Prussian box + nguồn + disclaimer | Mọi bài publish-ready (deep + daily) |

Mở bài bằng `cover_deep_page`, kết bằng `back_cover_cta`. Đối xứng visual signature của Opvia.

---

## Wave 1-3 (HTML+CSS+SVG atomic) - `viz.py`

| Component | One-liner | Best for |
|---|---|---|
| `gauge` | Đồng hồ 1 ratio + threshold | LDR/NSFR/SFL với trần, mở Phần với signature stat |
| `bar_horizontal` | Bar chart ngang 3-6 entity + threshold | So sánh nhỏ với baseline, nhãn label dài tiếng Việt |
| `heatmap` | Ma trận cell màu pos/neg | Ai hưởng lợi ai chịu thiệt, sector × policy impact |
| `flow_bridge` | Chuỗi nhân quả vertical | Mechanism explanation A → B → Z, đặc biệt counterintuitive |
| `scenario_cards` | 3 kịch bản với probability | Cuối bài deep, base/bull/bear với % |
| `timeline_horizontal` | Timeline ngang milestones | Khung thời gian implementation, regulatory schedule |
| `waterfall` | Chuỗi changes A → B | P&L bridge, capital adequacy walk |
| `ranking_ladder` | Xếp hạng với delta arrows | Sector ranking vs prev period, bank size vs Q-1 |
| `comparison_cards` | Cards so sánh side-by-side | Phương án A vs B (rất Opvia signature) |
| `stat_dashboard` | 4-6 stats grid | Mở Phần overview, daily report header |
| `sparkline` | Mini chart inline trong prose | "VPB CASA giảm liên tục [sparkline]" trong câu |
| `distribution_dot_plot` | Dots trên axis (HTML version) | Sector outliers identification, n=8-15 |
| `policy_fork` | 2 phương án + decision factors matrix | Regulatory decision analysis với criteria matrix |
| `winners_losers_split` | Cột hưởng lợi vs chịu thiệt | Phần "Cuộc chơi phân phối" |
| `data_hero` | 1 trang dramatic 1 mega number | Signature page mở Phần với hero stat |
| `mechanism_breakdown` | Input → Process → Output | 3-stage causal flow |
| `before_after_comparison` | State A → State B với delta | n=2 entity hoặc 1 system trước-sau policy |
| `executive_summary_box` | 4-section dashboard cuối bài | Thay summary text với 4-quadrant takeaway |
| `scenario_matrix` | 2D Probability × Impact | Policy uncertainty mapping |
| `risk_radar` | Radar chart 5-7 axes | Entity profile multi-dimension (1 stock 5 risk axes) |

---

## Wave 8 (atomic SVG) - `viz_wave8.py`

| Component | One-liner | Best for |
|---|---|---|
| `line_with_annotations` | Time series 8-20 điểm có pivot points | Macro time series với 2-4 highlight events |
| `dot_plot_distribution` | Phân phối dots với quartile band (SVG) | n=10+ entity với threshold, show median + IQR |
| `small_multiples_grid` | Cùng metric × 4-12 entity × time | Tufte signature, polarity-aware coloring |
| `quadrant_scatter` | 2D scatter X-Y với 4-quadrant | Risk-return, P/B vs ROE peer mapping |
| `slopegraph` | Before/after với rerank visible | Policy impact n>=4 entity, đường đan chéo = signal rerank |
| `sankey_mini` | Capital flow Bezier 3-5 → 3-5 | Dòng vốn nguồn → đích, M&A flow |
| `compass_callout` | Wrapper bọc chart + caption sidebar | Editorial wrapper cho Wave 8 chart |

---

## Wave 9 (editorial signatures) - `viz_wave9.py`

| Component | One-liner | Best for |
|---|---|---|
| `marginalia` | Chú thích lề brass italic 75/22 | Methodology notes, definition tooltips, source |
| `chart_dropcap` | Mở Phần với chart hero + drop cap 32pt | Signature opening cho Phần long-form |
| `path_progression` | Process tracking 3-7 milestones | Implementation status (completed/current/future) |

---

## Wave 10 (composite layouts) - `viz_wave10.py`

| Component | One-liner | Best for |
|---|---|---|
| `dashboard_grid` | 2x2 grid 4 cells KPI + sparkline + delta | Daily report header, quarterly KPI overview |
| `narrative_strip` | 3-4 mini charts hàng ngang + caption | Economist-style multi-metric strip |
| `infographic_panel` | Dark Prussian panel hero 56pt + 4 facts | Cover signature, section opener art |

---

## Selection cheat (LLM dùng để shortlist trong 5 giây)

**Có 1 con số signature?** → `gauge` hoặc `data_hero` hoặc `infographic_panel`

**Có n entity (3-6)?** → `bar_horizontal` (+ threshold) hoặc `comparison_cards` (n=2-3) hoặc `ranking_ladder` (có delta)

**Có n entity (8-15)?** → `dot_plot_distribution` (Wave 8 SVG) hoặc `distribution_dot_plot` (Wave 1 HTML)

**Có time series?** → `line_with_annotations` (Wave 8) hoặc `sparkline` (inline)

**Có time series × multi entity?** → `small_multiples_grid` (Wave 8)

**Trước/sau (n>=4)?** → `slopegraph` (Wave 8)

**Trước/sau (n=2)?** → `before_after_comparison` (Wave 1-3)

**2D scatter X-Y?** → `quadrant_scatter` (Wave 8)

**Capital flow nguồn → đích?** → `sankey_mini` (Wave 8)

**Mechanism explanation?** → `flow_bridge` (vertical) hoặc `mechanism_breakdown` (3-stage horizontal)

**3 kịch bản với probability?** → `scenario_cards` (atomic) hoặc `scenario_matrix` (2D P×I)

**Hưởng lợi vs chịu thiệt?** → `winners_losers_split` (đối xứng) hoặc `heatmap` (matrix)

**Process timeline / milestones?** → `timeline_horizontal` (atomic) hoặc `path_progression` (Wave 9 với marker types)

**4-6 KPI grid?** → `stat_dashboard` (Wave 1) hoặc `dashboard_grid` (Wave 10 với sparkline)

**3-4 macro metric strip?** → `narrative_strip` (Wave 10)

**Cuối bài executive summary?** → `executive_summary_box` (4-section)

**Multi-dim profile (5-7 axes)?** → `risk_radar`

**Mở Phần dramatic?** → `chart_dropcap` (Wave 9) hoặc `data_hero` (Wave 1) hoặc `infographic_panel` (Wave 10)

**Methodology / source note?** → `marginalia` (Wave 9)

**Wrap Wave 8 chart bằng editorial caption?** → `compass_callout`

---

## Frequency budget cho bài deep 15-20 trang

- 2-3 atomic số (gauge, data