---
title: "Master Manifest — OPVIA Sigma Knowledge File Index"
module_type: "reference"
file_name: "master-manifest.md"
purpose: "Table of contents và navigation index cho toàn bộ knowledge base OPVIA Sigma. Claude load file này đầu tiên khi confused về routing."
primary_triggers:
  - "manifest"
  - "index"
  - "mục lục"
  - "danh sách file"
  - "routing"
  - "knowledge base"
version: "v1.0 (Wave 6 — Lane 4)"
date: "2026-04-19"
---

# Master Manifest — OPVIA Sigma Knowledge File Index

> **Cách dùng:** File này là bản đồ điều hướng. Tìm trigger keyword trong bảng → xác định file cần load → đọc file đó.
> **Convention:** `{skill}/SKILL.md` = entry point mỗi domain/workflow. `core/` files luôn load khi root skill active.

---

## LAYER 1: CORE (Always Loaded)

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `SKILL.md` (root) | Orchestrator điều phối toàn bộ hệ thống, routing, identity | "OPVIA Sigma", "bắt đầu", "tổng quan", bất kỳ câu hỏi chưa rõ domain |
| `core/00-mission-and-voice.md` | Mission, identity, peer-analyst voice | "voice", "tone", "mission", "style" |
| `core/01-router.md` | Logic chọn sub-skill: equity/macro/fx/commodities/fi/cross-asset | "route", "chọn module", "load domain" |
| `core/02-research-protocol.md` | Research protocol 8 bước (Tutor) và 15 bước (Expert) | "research protocol", "8 bước", "deep-dive protocol" |
| `core/03-methodology.md` | Bậc bằng chứng, cờ đỏ phương pháp | "methodology", "bậc bằng chứng", "evidence ladder" |
| `core/04-meta-cognition.md` | 6 câu hỏi tự phản biện | "meta-cognition", "tự phản biện", "bias check" |
| `core/05-output-contracts.md` | 6 output formats chuẩn | "output format", "contract", "template" |
| `core/06-safety-policy.md` | 70/30 rule, no-recommend, no-prediction, VAS/IFRS | "safety", "policy", "70/30", "không khuyến nghị" |

---

## LAYER 2: DOMAINS (Lazy Load)

### equity-vn

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/equity-vn/SKILL.md` | Entry point equity VN | "cổ phiếu VN", "phân tích {ticker}", "sector {X}", "HPG", "VCB" |
| `domains/equity-vn/industry-guides.md` | Hướng dẫn ngành VN 2026 | "ngành", "industry guide", "sector analysis" |
| `domains/equity-vn/valuation-advanced.md` | Reverse DCF, SOTP, real options | "định giá", "valuation", "reverse DCF", "SOTP" |
| `domains/equity-vn/financial-modeling.md` | 3-statement modeling | "model", "forecast", "3 statement", "BCTC dự phóng" |
| `domains/equity-vn/forensic-accounting.md` | Beneish, Piotroski, accrual | "forensic", "Beneish", "Piotroski", "red flags" |
| `domains/equity-vn/moat-analysis.md` | ROIC persistence, competitive advantage | "moat", "lợi thế cạnh tranh", "ROIC" |
| `domains/equity-vn/vas-ifrs-bridges.md` | So sánh VAS và IFRS | "VAS", "IFRS", "chuẩn mực kế toán" |
| `domains/equity-vn/red-flags.md` | Red flags VN-specific | "red flags", "cờ đỏ", "warning signs" |

### macro-vn

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/macro-vn/SKILL.md` | Entry point macro VN | "vĩ mô", "macro VN", "NHNN", "chính sách tiền tệ" |
| `domains/macro-vn/monetary-policy-nhnn.md` | Công cụ NHNN, policy reaction function | "NHNN", "OMO", "refinancing rate", "SBV" |
| `domains/macro-vn/transmission-channels.md` | 4 kênh truyền dẫn VN | "kênh truyền dẫn", "transmission", "monetary transmission" |
| `domains/macro-vn/credit-cycle-vn.md` | Phase identification, LDR, NPL leading | "chu kỳ tín dụng", "credit cycle", "LDR", "NPL" |
| `domains/macro-vn/liquidity-systems.md` | Thakor-Yu + Kashyap-Stein + Brunnermeier-Pedersen cho VN | "thanh khoản", "liquidity", "funding squeeze" |
| `domains/macro-vn/balance-of-payments.md` | Current account, capital account, FX reserves | "cán cân thanh toán", "BoP", "capital flow" |
| `domains/macro-vn/fiscal-policy-vn.md` | Nợ công, fiscal space, đầu tư công | "tài khóa", "fiscal", "nợ công", "ngân sách" |
| `domains/macro-vn/regime-framework-v11.md` | Codify Regime Framework v1.1 | "Regime v1.1", "regime framework", "phân loại chế độ" |

### fx

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/fx/SKILL.md` | Entry point FX | "FX", "ngoại tệ", "tỷ giá", "USD/VND", "forex" |
| `domains/fx/usd-vnd-dynamics.md` | Drivers: rate differential, BoP, intervention | "USD/VND", "tỷ giá USD", "VND depreciation" |
| `domains/fx/intervention-history.md` | Lịch sử can thiệp NHNN | "can thiệp", "intervention", "NHNN mua bán USD" |
| `domains/fx/carry-and-positioning.md` | Carry trade VND, positioning | "carry", "carry trade", "NDF premium", "forward" |
| `domains/fx/major-pairs-context.md` | DXY, EUR, JPY, CNY anchor | "DXY", "EUR/USD", "CNY", "USD Index" |
| `domains/fx/em-fx-frameworks.md` | Trilemma, Mundell-Fleming, capital surges | "EM FX", "trilemma", "sudden stop" |

### commodities

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/commodities/SKILL.md` | Entry point commodities | "commodity", "hàng hóa", "oil", "gold", "dầu", "vàng" |
| `domains/commodities/oil-and-gas.md` | Oil market, OPEC, geopolitical premiums | "oil", "dầu", "Brent", "WTI", "OPEC" |
| `domains/commodities/gold-and-precious.md` | Gold drivers: real rates, USD, geopolitics | "gold", "vàng", "XAU", "precious metals" |
| `domains/commodities/base-metals.md` | Copper, aluminum, steel — China demand | "copper", "nhôm", "thép", "base metals" |
| `domains/commodities/soft-commodities.md` | Rice, coffee, rubber — VN exports | "gạo", "cà phê", "cao su", "soft commodities" |
| `domains/commodities/futures-curve-mechanics.md` | Contango/backwardation, roll yield | "contango", "backwardation", "futures curve" |
| `domains/commodities/commodity-vn-impact.md` | Passthrough vào CPI/PPI VN | "passthrough", "ảnh hưởng hàng hóa", "CPI", "PPI" |

### fixed-income

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/fixed-income/SKILL.md` | Entry point fixed income | "fixed income", "trái phiếu", "yield", "bond", "TPCP" |
| `domains/fixed-income/yield-curve-vn.md` | Government bond curve VN | "yield curve", "đường cong lãi suất" |
| `domains/fixed-income/duration-convexity.md` | Duration management, convexity hedging | "duration", "convexity", "interest rate risk" |
| `domains/fixed-income/credit-spreads-vn.md` | Corporate bond spread VN | "credit spread", "trái phiếu doanh nghiệp" |
| `domains/fixed-income/em-rates-context.md` | UST anchor, term premium | "UST", "Treasury", "term premium", "EM spread" |
| `domains/fixed-income/bond-supply-demand.md` | Issuance calendar, demand sources | "issuance", "supply demand", "phát hành" |
| `domains/fixed-income/ldr-and-bank-funding.md` | LDR, funding squeeze | "LDR", "bank funding", "funding squeeze" |

### cross-asset

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `domains/cross-asset/SKILL.md` | Entry point cross-asset | "cross-asset", "linkage", "ảnh hưởng X tới Y", "correlation" |
| `domains/cross-asset/correlation-regimes.md` | Stable vs regime-shift correlation | "correlation", "regime correlation", "tương quan" |
| `domains/cross-asset/risk-on-off-classification.md` | RORO regime indicators | "risk on", "risk off", "RORO", "risk appetite" |
| `domains/cross-asset/transmission-channels-cross-asset.md` | Cross-asset transmission | "transmission cross-asset" |
| `domains/cross-asset/flight-to-quality-patterns.md` | Historical patterns, EM impacts | "flight to quality", "safe haven" |
| `domains/cross-asset/linkage-matrix-vn.md` | Ma trận VN equity↔USD/VND↔VN rates↔oil↔DXY | "linkage matrix", "ma trận liên kết" |

---

## LAYER 3: WORKFLOWS (Lazy Load)

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `workflows/daily-brief/SKILL.md` | Entry point daily brief | "brief đầu ngày", "regime check", "morning brief" |
| `workflows/daily-brief/template.md` | Format Daily Brief (6 sections) | "daily brief template" |
| `workflows/daily-brief/checklist.md` | 10 items must-cover | "daily brief checklist" |
| `workflows/deep-dive/SKILL.md` | Entry point deep-dive | "phân tích sâu", "deep-dive", "research X" |
| `workflows/deep-dive/8-step-protocol.md` | Protocol 8 bước | "8 bước", "deep-dive protocol" |
| `workflows/deep-dive/output-template.md` | Template deep-dive memo | "deep-dive template" |
| `workflows/pre-mortem/SKILL.md` | Entry point pre-mortem | "pre-mortem", "phản biện thesis", "yết kháng", "bear case" |
| `workflows/pre-mortem/adversarial-protocol.md` | 6-step adversarial dialogue | "adversarial", "devil's advocate" |
| `workflows/pre-mortem/failure-modes-checklist.md` | Failure modes by asset class | "failure modes", "rủi ro thesis" |
| `workflows/thesis-tracker/SKILL.md` | Entry point thesis tracking | "track thesis", "signpost check", "thesis còn valid không" |
| `workflows/thesis-tracker/tracker-format.md` | Tracker table format | "tracker format" |
| `workflows/thesis-tracker/trigger-conditions.md` | ON-TRACK/WATCHING/TRIGGERED/BROKEN thresholds | "trigger conditions" |
| `workflows/cross-asset-linkage/SKILL.md` | Entry point linkage | "linkage", "FX-equity correlation", "rate cycle equity" |
| `workflows/cross-asset-linkage/analysis-protocol.md` | Linkage protocol 6 bước | "linkage protocol" |
| `workflows/regime-shift-alert/SKILL.md` | Entry point regime shift alert | "regime shift", "cảnh báo chuyển đổi" |
| `workflows/regime-shift-alert/shift-criteria.md` | Auto-trigger criteria | "shift criteria" |

---

## LAYER 4: FRAMEWORKS (Load on Demand)

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `frameworks/README.md` | Index tất cả frameworks | "framework index", "học thuật" |
| `frameworks/thakor-yu-2024.md` | Bank capital & liquidity | "Thakor", "Yu", "bank capital" |
| `frameworks/kashyap-stein-2000.md` | Bank lending channel | "Kashyap", "Stein", "lending channel" |
| `frameworks/brunnermeier-pedersen-2009.md` | Funding & market liquidity | "Brunnermeier", "Pedersen", "liquidity spiral" |
| `frameworks/adrian-shin-2010.md` | Liquidity & leverage cycles | "Adrian", "Shin", "leverage cycle" |
| `frameworks/geanakoplos-2010.md` | Leverage cycle — margin | "Geanakoplos", "leverage", "margin" |
| `frameworks/minsky-1986.md` | Financial instability | "Minsky", "Ponzi financing" |
| `frameworks/allen-gale-2000.md` | Asset price bubbles | "Allen", "Gale", "bubble" |
| `frameworks/dickinson-mauboussin.md` | Corporate lifecycle | "Dickinson", "Mauboussin", "lifecycle" |
| `frameworks/opvia-regime-framework-v11.md` | OPVIA regime classification | "Regime v1.1", "OPVIA regime" |

---

## LAYER 5: REFERENCES (Load on Demand)

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `references/visual-artifact-policy.md` | Design bible: Prussian Blue, Aged Brass | "visual", "chart", "design", "màu sắc" |
| `references/vn-data-sources.md` | Source hierarchy, trust tiers, cross-check | "nguồn dữ liệu", "data source", "FiinTrade", "NHNN", "GSO" |
| `references/design-bible-opvia.md` | Palette, typography, layout | "design bible", "bảng màu", "palette" |
| `references/glossary-domain-specific.md` | Thuật ngữ chuyên sâu | "thuật ngữ", "glossary", "định nghĩa" |
| `references/vn-structural-shifts-tracker.md` | Living document structural shifts VN | "chuyển dịch cấu trúc", "structural shift", "structural break" |

---

## LAYER 6: PROMPTS (Load on Demand)

| Filename | Purpose | Trigger Keywords |
|---|---|---|
| `prompts/README.md` | Index prompt templates | "prompt index", "template prompt" |
| `prompts/daily-brief-prompt.md` | Template daily brief | "daily brief prompt" |
| `prompts/deep-dive-prompt.md` | Template deep-dive | "deep-dive prompt" |
| `prompts/pre-mortem-prompt.md` | Template pre-mortem | "pre-mortem prompt" |
| `prompts/thesis-tracker-prompt.md` | Template thesis tracker | "thesis tracker prompt" |
| `prompts/cross-asset-linkage-prompt.md` | Template linkage | "linkage prompt" |
| `prompts/external-company-template.md` | Template phân tích công ty ngoài | "external company", "template công ty" |

---

## QUICK-LOOKUP: INTENT → FILES

| User Intent | Files to Load |
|---|---|
| "Brief đầu ngày" | `workflows/daily-brief/SKILL.md` + `core/` + `references/vn-data-sources.md` |
| "Phân tích sâu HPG" | `domains/equity-vn/SKILL.md` + `workflows/deep-dive/SKILL.md` + `core/` |
| "USD/VND outlook" | `domains/fx/SKILL.md` + `domains/macro-vn/SKILL.md` + `core/` |
| "Oil ảnh hưởng CPI VN" | `domains/cross-asset/SKILL.md` + `domains/commodities/SKILL.md` + `core/` |
| "Pre-mortem thesis GMD" | `workflows/pre-mortem/SKILL.md` + `domains/equity-vn/SKILL.md` + `core/` |
| "Regime hiện tại" | `domains/macro-vn/regime-framework-v11.md` + `frameworks/opvia-regime-framework-v11.md` |
| "Track thesis X" | `workflows/thesis-tracker/SKILL.md` + `core/` |
| "Thế nào là Regime v1.1" | `frameworks/opvia-regime-framework-v11.md` + `references/glossary-domain-specific.md` |
| "Nguồn dữ liệu nào tin" | `references/vn-data-sources.md` |
| "Có chuyển dịch cấu trúc gì mới" | `references/vn-structural-shifts-tracker.md` |
| "Vẽ chart theo style OPVIA" | `references/visual-artifact-policy.md` + `references/design-bible-opvia.md` |

---

> **Document Control**
> - Version: v1.0 (Wave 6 — Lane 4)
> - Ngày: 2026-04-19
> - Files indexed: ~87
> - Related: Tất cả file trong index
