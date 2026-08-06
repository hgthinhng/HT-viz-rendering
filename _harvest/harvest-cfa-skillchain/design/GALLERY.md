# VIZ FACTORY — GALLERY (95 khuôn CFA: 68 data-chart + 27 diagram)

*Render:* `python3 scripts/viz_render.py <template> out.png`  ·  *liệt kê:* `--list`  ·  *đổi số:* `--params key=val`
Khớp design ấm (navy/teal/gold/giấy kem, Lato), Cowork-fit (matplotlib, KHÔNG PowerShell/Chrome).
**18 engine** — data: curve_xy·distribution·payoff·tree·timeline·regression·prob_tree·bars·ladder · diagram: flowchart·venn2·matrix2x2·pyramid·cycle·compare·concentric·hflow·spokes
Visual conceptual quá sức matplotlib → `templates/AI_IMAGE_PROMPTS.md` (20 prompt FULL ENGLISH tự gen).


## Derivatives (16)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `bear_spread` | payoff | Bear put spread | DV_M08 | gallery/bear_spread.png |
| `bull_spread` | payoff | Bull call spread | DV_M08 | gallery/bull_spread.png |
| `butterfly` | payoff | Long butterfly | DV_M08 | gallery/butterfly.png |
| `clearing_novation` | hflow | Clearinghouse/novation | DV_M01 | gallery/clearing_novation.png |
| `collar` | payoff | Collar | DV_M03 | gallery/collar.png |
| `covered_call` | payoff | Covered call | DV_M03 | gallery/covered_call.png |
| `margin_call_ladder` | ladder | Margin & call | DV_M06 | gallery/margin_call_ladder.png |
| `otc_vs_etd` | compare | OTC vs ETD | DV_M01 | gallery/otc_vs_etd.png |
| `payoff_forward` | payoff | Forward payoff | DV_M02 | gallery/payoff_forward.png |
| `payoff_long_call` | payoff | Long call | DV_M02 | gallery/payoff_long_call.png |
| `payoff_long_put` | payoff | Long put | DV_M02 | gallery/payoff_long_put.png |
| `payoff_short_call` | payoff | Short call | DV_M02 | gallery/payoff_short_call.png |
| `payoff_short_put` | payoff | Short put | DV_M02 | gallery/payoff_short_put.png |
| `protective_put` | payoff | Protective put | DV_M03 | gallery/protective_put.png |
| `straddle` | payoff | Long straddle | DV_M08 | gallery/straddle.png |
| `swap_as_fra` | hflow | Swap = chuỗi FRA | DV_M07 | gallery/swap_as_fra.png |

## Fixed Income (8)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `bond_taxonomy` | tree | Phân loại trái phiếu | FI_M01 | gallery/bond_taxonomy.png |
| `convexity_curve` | curve_xy | Giá–yield + duration + convexity | FI_M11-12 | gallery/convexity_curve.png |
| `coupon_pull_to_par` | curve_xy | Pull to par | FI_M06 | gallery/coupon_pull_to_par.png |
| `credit_rating_scale` | ladder | Thang xếp hạng | FI_M14 | gallery/credit_rating_scale.png |
| `credit_spread_curve` | curve_xy | Đường cong spread | FI_M14 | gallery/credit_spread_curve.png |
| `reinvestment_crossover` | curve_xy | Price/reinvestment = MacDur | FI_M10 | gallery/reinvestment_crossover.png |
| `securitization_flow` | hflow | Chứng khoán hoá | FI_M17 | gallery/securitization_flow.png |
| `yield_curve` | curve_xy | Spot/Par/Forward term structure | FI_M09 | gallery/yield_curve.png |

## Portfolio Management (9)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `asset_class_tree` | tree | Phân lớp tài sản | PM_M03 | gallery/asset_class_tree.png |
| `behavioral_biases` | tree | Phân loại thiên lệch | PM_M05 | gallery/behavioral_biases.png |
| `cal_cml` | curve_xy | CAL/CML + danh mục tiếp tuyến | PM_M02 | gallery/cal_cml.png |
| `efficient_frontier` | curve_xy | Biên hiệu quả 2 tài sản + GMVP | PM_M01-02 | gallery/efficient_frontier.png |
| `indifference_curve` | curve_xy | Đường bàng quan risk-averse | PM_M04 | gallery/indifference_curve.png |
| `ips_process` | cycle | Quy trình IPS | PM_M04 | gallery/ips_process.png |
| `sharpe_comparison` | bars | So sánh Sharpe | PM_M01 | gallery/sharpe_comparison.png |
| `sml_capm` | curve_xy | SML/CAPM, over/undervalued | PM_M02 | gallery/sml_capm.png |
| `var_cvar` | distribution | VaR/CVaR đuôi trái | PM_M06 | gallery/var_cvar.png |

## Quantitative Methods (12)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `central_limit_theorem` | distribution | CLT | QM_M07 | gallery/central_limit_theorem.png |
| `confidence_interval` | distribution | Khoảng tin cậy 95% | QM_M07 | gallery/confidence_interval.png |
| `hypothesis_two_tailed` | distribution | Vùng bác bỏ 2-tail | QM_M08 | gallery/hypothesis_two_tailed.png |
| `kurtosis` | distribution | Kurtosis | QM_M03 | gallery/kurtosis.png |
| `normal_vs_lognormal` | distribution | Normal vs lognormal | QM_M06 | gallery/normal_vs_lognormal.png |
| `probability_tree` | prob_tree | Cây xác suất | QM_M04 | gallery/probability_tree.png |
| `regression_scatter_fit` | regression | Hồi quy scatter+fit | QM_M10 | gallery/regression_scatter_fit.png |
| `residual_hetero` | regression | Residual heteroskedastic | QM_M10 | gallery/residual_hetero.png |
| `residual_homo` | regression | Residual homoskedastic | QM_M10 | gallery/residual_homo.png |
| `sampling_distribution` | distribution | Sampling distribution | QM_M07 | gallery/sampling_distribution.png |
| `skewness` | distribution | Độ lệch | QM_M03 | gallery/skewness.png |
| `type_i_ii_error` | distribution | Type I/II error | QM_M08 | gallery/type_i_ii_error.png |

## Equity (11)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `ddm_timeline` | timeline | Timeline cổ tức DDM | EQ_M08 | gallery/ddm_timeline.png |
| `dividend_chronology` | timeline | Lịch trình cổ tức | EQ_M04 | gallery/dividend_chronology.png |
| `emh_forms` | concentric | Dạng hiệu quả EMH | EQ_M03 | gallery/emh_forms.png |
| `gordon_growth` | curve_xy | Gordon growth sensitivity | EQ_M08 | gallery/gordon_growth.png |
| `index_weighting` | bars | Trọng số chỉ số | EQ_M02 | gallery/index_weighting.png |
| `lifecycle_curve` | curve_xy | Vòng đời ngành | EQ_M06 | gallery/lifecycle_curve.png |
| `order_book` | bars | Order book | EQ_M01 | gallery/order_book.png |
| `pestle` | spokes | PESTLE | EQ_M06 | gallery/pestle.png |
| `porter_five_forces` | spokes | Porter 5 lực | EQ_M06 | gallery/porter_five_forces.png |
| `valuation_models_tree` | tree | Cây mô hình định giá | EQ_M08 | gallery/valuation_models_tree.png |
| `value_chain` | hflow | Porter value chain | EQ_M06 | gallery/value_chain.png |

## Economics (11)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `business_cycle` | curve_xy | Chu kỳ kinh tế | EC_M02 | gallery/business_cycle.png |
| `business_cycle_phases` | cycle | 4 pha chu kỳ | EC_M02 | gallery/business_cycle_phases.png |
| `cost_curves` | curve_xy | MC/ATC/AVC | EC_M01 | gallery/cost_curves.png |
| `fx_regimes` | ladder | Phổ chế độ tỷ giá | EC_M08 | gallery/fx_regimes.png |
| `laffer_curve` | curve_xy | Laffer thuế | EC_M03 | gallery/laffer_curve.png |
| `market_structures` | compare | 4 cấu trúc thị trường | EC_M01 | gallery/market_structures.png |
| `monetary_transmission` | hflow | Truyền dẫn tiền tệ | EC_M05 | gallery/monetary_transmission.png |
| `phillips_curve` | curve_xy | Phillips curve | EC_M03 | gallery/phillips_curve.png |
| `policy_mix` | matrix2x2 | Phối hợp chính sách 2x2 | EC_M04 | gallery/policy_mix.png |
| `supply_demand` | curve_xy | Cung-cầu cân bằng | EC_M01 | gallery/supply_demand.png |
| `trade_welfare` | curve_xy | Thặng dư thương mại | EC_M06 | gallery/trade_welfare.png |

## Corporate Issuers (8)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `breakeven_cvp` | curve_xy | Breakeven CVP | CI_M07 | gallery/breakeven_cvp.png |
| `capital_allocation_process` | cycle | Quy trình capital allocation | CI_M05 | gallery/capital_allocation_process.png |
| `cash_conversion_cycle` | cycle | CCC cycle | CI_M04 | gallery/cash_conversion_cycle.png |
| `cashflow_timeline` | timeline | Timeline dòng tiền NPV | CI_M05 | gallery/cashflow_timeline.png |
| `claim_priority_ladder` | ladder | Thứ tự ưu tiên thanh toán | CI_M02 | gallery/claim_priority_ladder.png |
| `npv_profile` | curve_xy | NPV profile + IRR | CI_M05 | gallery/npv_profile.png |
| `stakeholder_map` | spokes | Bản đồ stakeholder | CI_M02 | gallery/stakeholder_map.png |
| `wacc_vs_leverage` | curve_xy | WACC vs đòn bẩy | CI_M06 | gallery/wacc_vs_leverage.png |

## Financial Statement Analysis (9)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `accounting_cycle` | cycle | Chu trình kế toán | FSA_M01 | gallery/accounting_cycle.png |
| `common_size_is` | bars | Common-size IS | FSA_M02 | gallery/common_size_is.png |
| `dual_axis_rev_margin` | bars | Dual-axis doanh thu/biên | FSA_M11 | gallery/dual_axis_rev_margin.png |
| `dupont_3step` | tree | DuPont 3 bước | FSA_M11 | gallery/dupont_3step.png |
| `dupont_5step` | tree | DuPont 5 bước | FSA_M11 | gallery/dupont_5step.png |
| `fifo_lifo` | bars | FIFO vs LIFO | FSA_M06 | gallery/fifo_lifo.png |
| `fraud_triangle` | spokes | Fraud triangle | FSA_M10 | gallery/fraud_triangle.png |
| `ifrs_vs_usgaap` | compare | IFRS vs US GAAP | FSA_M01 | gallery/ifrs_vs_usgaap.png |
| `three_statement_linkage` | hflow | Liên kết 3 BCTC | FSA_M04 | gallery/three_statement_linkage.png |

## Alternative Investment (5)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `fair_value_hierarchy` | pyramid | Fair value hierarchy | AI_M01 | gallery/fair_value_hierarchy.png |
| `hedge_fund_strategies` | tree | Chiến lược hedge fund | AI_M06 | gallery/hedge_fund_strategies.png |
| `j_curve` | curve_xy | PE J-curve | AI_M03 | gallery/j_curve.png |
| `re_quadrants` | matrix2x2 | BĐS 4 góc | AI_M04 | gallery/re_quadrants.png |
| `term_structure` | curve_xy | Contango/backwardation | AI_M05 | gallery/term_structure.png |

## Ethics (6)

| Template | Engine | Dùng cho | Module | Ảnh |
|---|---|---|---|---|
| `conflicts_disclose` | flowchart | Xử lý xung đột lợi ích | ETH_M02 | gallery/conflicts_disclose.png |
| `eth_decision_framework` | flowchart | Khung quyết định đạo đức | ETH_M01 | gallery/eth_decision_framework.png |
| `eth_standards_map` | tree | 7 Standards map | ETH_M02 | gallery/eth_standards_map.png |
| `gips_structure` | pyramid | GIPS cấu trúc | ETH_M03 | gallery/gips_structure.png |
| `legal_vs_ethical` | venn2 | Venn legal vs ethical | ETH_M01 | gallery/legal_vs_ethical.png |
| `mosaic_vs_mnpi` | venn2 | Mosaic vs MNPI | ETH_M02 | gallery/mosaic_vs_mnpi.png |