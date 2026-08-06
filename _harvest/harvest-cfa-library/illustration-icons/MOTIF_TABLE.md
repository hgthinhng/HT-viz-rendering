# Module Icons 2027 — Bảng motif banner (97 module)

Mục tiêu: mỗi module note L1 2027 có 1 banner 16:9, style editorial The Economist/Businessweek, **không chữ/số trong ảnh**. Bảng này cho sẵn *scene fragment* để ghép vào prompt Nano Banana Pro.

## Cách dùng (mechanical)

1. Lấy `SCENE` của module ở bảng dưới, ghép vào `[MOTIF]` trong template.
2. Generate trên Nano Banana Pro (ra ảnh vuông).
3. Tải ảnh về `raw\`, **đặt tên đúng bằng CODE module** (vd `QM_M1.png`, `FIX_M11.png`) → sau crop ra `QM_M1_169.png`, map thẳng về docx.
4. `python smart_crop_169.py` → `out_169\`.

### Template chuẩn (giữ nguyên, chỉ thay `[MOTIF]`)

> Premium editorial illustration in the style of The Economist and Bloomberg Businessweek covers. WIDE HORIZONTAL LANDSCAPE banner, 16:9. Scene: **[MOTIF]**. Style: flat vector shapes with subtle screenprint grain and soft offset shadows, mid-century modern finish, warm cream background (#F5EFE2), deep navy (#16283F), muted teal (#2F7E7A), warm gold (#C9A227). Calm negative space. Absolutely no text, no letters, no numbers, no watermark.
> Composition constraint: place all subjects within the central horizontal third of the frame, leaving the top and bottom areas as plain empty background; the entire canvas is ONE single continuous warm cream field filling every edge; do NOT enclose the artwork in any inner rectangle, panel, card, border, frame, or vignette, and do NOT lighten or tint the background inside any region.

*(FB2 constraint — chốt 2026-07-07 sau khi bản "central band + full-bleed" vẫn để lọt vài ảnh panel-khung. FB2 diệt hẳn defect.)*

### Nguyên tắc chống lặp (đã áp khi thiết kế bảng)

- Không dùng coin/sprout đại trà. `coin` chỉ ở QM_M1 (bản đã đạt).
- Motif "cân/balance" giới hạn 4 bài, mỗi bài render KHÁC nhau (cân 2 đĩa / bập bênh / đòn bẩy điểm tựa / dầm xếp rổ): FSA_M3, FIX_M6, FIX_M11, DER_M9.
- Motif "kính lúp" chỉ FSA_M1. Motif "toà nhà/issuer" phân biệt bằng loại nhà (skyline / tháp doanh nghiệp / toà chính phủ cột trụ / công ty tư nhân có cổng).
- Trong cùng subject, mỗi module một vật thể chủ đạo khác nhau (đặc biệt FIX 19 bài, DER 10 bài).

---

## QM — Quantitative Methods (11)

| CODE | Module | SCENE fragment (dán vào [MOTIF]) |
|---|---|---|
| QM_M1 | Returns of Financial Assets | ascending stack of coin-steps with a smooth growth line arcing up over them *(bản đã đạt — giữ)* |
| QM_M2 | Types of Financial Returns | a single beam of light passing through a prism, splitting into several diverging colored streams (return decomposed into types) |
| QM_M3 | Benchmarking Returns | two parallel arrow-tracks racing side by side, one measured against a marked reference ruler-bar |
| QM_M4 | Time Value of Money | an hourglass whose falling sand forms an upward compounding curve on the lower chamber |
| QM_M5 | Statistical Characteristics of Returns | a smooth bell-shaped hill of terrain with a central plumb-line and one longer asymmetric tail-slope |
| QM_M6 | Statistical Distributions | a shelf lined with vessels of different silhouettes (bell, skewed, spiked) — a gallery of distribution shapes |
| QM_M7 | Estimation & Hypothesis Testing | a magnifying lens over a few small sample-dots inferring a large faint population-cloud behind |
| QM_M8 | Return & Risk of a Portfolio | several separate asset-circles overlapping and merging into one calmer blended orbit |
| QM_M9 | Simulation of Asset Prices | many thin branching paths fanning out from a single origin point (Monte Carlo fan) |
| QM_M10 | Simple Linear Regression | a scatter cloud of dots on a clean grid with one confident best-fit line threading through |
| QM_M11 | Intro to Financial Data Science | structured and unstructured data-blocks flowing through pipes into a stylized circuit-brain node |

## ECO — Economics (9)

| CODE | Module | SCENE fragment |
|---|---|---|
| ECO_M0 | Foundations of Economics (Pre) | two intersecting arcs crossing like scissors at a single balance point (supply meets demand) |
| ECO_M1 | The Firm & Market Structures | a skyline spectrum from many tiny equal market-stalls rising to one dominant solitary tower |
| ECO_M2 | Understanding Business Cycles | a rolling sine-wave landscape of peaks and troughs with a sun rising over one crest, setting over the next |
| ECO_M3 | Fiscal Policy | a government building with two taps — one draining (tax), one pouring (spending) — into an economy basin |
| ECO_M4 | Monetary Policy | a central-bank building with one large control dial regulating a flowing stream of money/credit |
| ECO_M5 | Introduction to Geopolitics | chess pieces standing on a stylized globe with tension-lines drawn between nations |
| ECO_M6 | International Trade | two ports across water exchanging stacked cargo containers, arrows crossing a border line |
| ECO_M7 | Capital Flows & the FX Market | a river of currency flowing between two territories through an exchange gate/channel |
| ECO_M8 | Exchange Rate Calculations | two currency medallions as meshing gears of different sizes converting one into the other |

## CF — Corporate Finance (7)

| CODE | Module | SCENE fragment |
|---|---|---|
| CF_M1 | Organizational Forms & Ownership | three business structures of rising formality — a small tent, a paired lodge, a corporate tower |
| CF_M2 | Investors & Other Stakeholders | a central company hub with spokes radiating to distinct stakeholder figures around a wheel |
| CF_M3 | Corporate Governance | a boardroom table balanced by guardrails between an owner-side and a manager-side (checks and balances) |
| CF_M4 | Working Capital & Liquidity | a circular pipe-loop cycling short-term assets: inventory → receivables → cash → back |
| CF_M5 | Capital Investments & Allocation | a hand routing capital at a crossroads toward competing project-doors ranked by height |
| CF_M6 | Capital Structure | a building supported by columns split into debt-blocks and equity-blocks in its foundation |
| CF_M7 | Business Models | interlocking modular blueprint blocks meshing into one working machine (a business-model canvas of gears) |

## FSA — Financial Statement Analysis (13)

| CODE | Module | SCENE fragment |
|---|---|---|
| FSA_M0 | Foundations of Financial Reporting (Pre) | an open classical ledger resting on foundation stones (the reporting framework as bedrock) |
| FSA_M1 | Intro to Financial Statement Analysis | a magnifying glass held over a neat stack of the three financial statements |
| FSA_M2 | Analyzing Income Statements | a funnel: broad revenue pouring in the top, narrowing through expense filters to a small net-profit drop |
| FSA_M3 | Analyzing Balance Sheets | a two-pan scale perfectly level — assets on one pan, liabilities and equity on the other |
| FSA_M4 | Statements of Cash Flows I | three labeled pipes (operating, investing, financing) feeding one central cash reservoir |
| FSA_M5 | Statements of Cash Flows II | a stepped reconciliation bridge converting an accrual figure across a gap into a cash figure |
| FSA_M6 | Analysis of Inventories | crates on a conveyor entering one side and leaving the other (first-in-first-out flow of stock) |
| FSA_M7 | Analysis of Long-Term Assets | a heavy machine on a downward ramp of declining value (depreciation of a long-lived asset) |
| FSA_M8 | Long-Term Liabilities & Equity | a heavy anchor tethered to a structure by long taut cables (long-term obligations anchoring the firm) |
| FSA_M9 | Analysis of Income Taxes | two side-by-side calendars (book vs tax) with a highlighted timing-gap slice between them |
| FSA_M10 | Financial Reporting Quality | a document passing through a fine filter/sieve that catches small red-flag shapes |
| FSA_M11 | Financial Analysis Techniques | a cockpit dashboard of several ratio gauges and dials (analysis instrument panel) |
| FSA_M12 | Intro to Financial Statement Modeling | a spreadsheet grid extruding forward into projected future bars (model projecting ahead) |

## EQ — Equities (12)

| CODE | Module | SCENE fragment |
|---|---|---|
| EQ_M1 | Equity Instrument Features | a single ownership wedge lifting out of a whole company-pie, tied with a share ribbon |
| EQ_M2 | Jurisdictions, Classes & Voting | a ballot box receiving share-shaped ballots, with tiered share-class layers beside it |
| EQ_M3 | Equity Issuance & Trading | a launch pad sending shares up (issuance) feeding into a marketplace of exchanging hands (trading) |
| EQ_M4 | Sources of Equity Returns | a dividend-drop stream and a price-appreciation arrow merging into one total-return river |
| EQ_M5 | Introduction to Equity Valuation | an iceberg — a small price-tip above water, the larger intrinsic value submerged below |
| EQ_M6 | DCF & Growth Models | future cash-flow bars pulled back through a telescoping discount-tunnel into a present-value stack |
| EQ_M7 | Relative Value (Multiples) | several comparable company-vessels on a shelf measured against each other by one common ruler |
| EQ_M8 | Financial Statement Forecasting | a branching driver-tree (revenue → margins → drivers) growing forward into a projected value |
| EQ_M9 | Industry & Competitive Analysis | five directional arrows pressing inward on a central firm-hub (five competitive forces) |
| EQ_M10 | Company Analysis: Past/Present/Future | a triptych timeline of one company: a rear-view mirror, a present frame, a forward telescope |
| EQ_M11 | Equity Analyst Research Reports | an analyst's report page with a target-flag planted and a star-rating stamp (no letters) |
| EQ_M12 | CAPM, Market Model & Factor Models | a rising security-market-line with a beta-slope, fed by several factor-input dials |

## FIX — Fixed Income (19)

| CODE | Module | SCENE fragment |
|---|---|---|
| FIX_M1 | Fixed-Income Instrument Features | anatomy of a bond — a principal certificate with detachable coupon tabs and a maturity marker |
| FIX_M2 | Cash Flows & Types | a timeline with a row of small equal coupon-payments then one large principal balloon at the end |
| FIX_M3 | Issuance & Trading | a bond issued from a podium into a connected web of dealer desks (primary to OTC secondary) |
| FIX_M4 | Markets for Corporate Issuers | a corporate tower issuing tiered debt shelves by maturity (short paper up to long bonds) |
| FIX_M5 | Markets for Government Issuers | a classical columned treasury building emitting sovereign bond-notes from its vault |
| FIX_M6 | Bond Valuation: Prices & Yields | a rocker/see-saw showing the inverse relationship — a price-ball rises as a yield-ball drops |
| FIX_M7 | Yield & Spread (Fixed-Rate) | a base yield-bar with additional spread-layers stacked on top (yield build-up) |
| FIX_M8 | Yield & Spread (Floating-Rate) | a buoy floating up and down riding a reference-rate wave (periodic reset) |
| FIX_M9 | Term Structure: Spot/Par/Forward | a family of three distinct curves layered rising across a maturity axis |
| FIX_M10 | Interest Rate Risk & Return | a coiled spring (bond price) compressing under a descending rate-weight (price sensitivity) |
| FIX_M11 | Yield-Based Duration | cash-flow bars balanced on a plank resting at a single fulcrum-point (weighted-average timing) |
| FIX_M12 | Convexity & Portfolio Properties | a bowed convex curve arcing away from a straight tangent line, the curvature-gap highlighted |
| FIX_M13 | Curve-Based & Empirical Measures | a hand twisting and shifting a yield curve at separate key points (scenario reshaping) |
| FIX_M14 | Credit Risk | a taut chain with one visibly weakening/cracking link (probability of default) |
| FIX_M15 | Credit Analysis: Government Issuers | a classical government building resting on a tilting stability-platform under stress-test weights |
| FIX_M16 | Credit Analysis: Corporate Issuers | a corporate tower assessed against a rising credit rating-ladder gauge |
| FIX_M17 | Fixed-Income Securitization | many small loan-shapes funneled into a pool then sliced into stacked tranche-layers |
| FIX_M18 | Asset-Backed Security (ABS) | a bundle of diverse receivable-icons (auto, card, lease) wrapped as one security package |
| FIX_M19 | Mortgage-Backed Security (MBS) | a row of house-rooftops pooled into a security stack with a prepayment valve on the side |

## DER — Derivatives (10)

| CODE | Module | SCENE fragment |
|---|---|---|
| DER_M1 | Instrument & Market Features | a kite tethered by a taut string to a ground anchor (value derived from an underlying) |
| DER_M2 | Forward Commitment vs Contingent Claim | a fork splitting into a locked handshake (obligation) and an optional open door (right) |
| DER_M3 | Benefits, Risks & Uses | one instrument held two ways — as a protective shield (hedge) and as an amplifying lever (speculation) |
| DER_M4 | Arbitrage, Replication, Cost of Carry | two separate roads forking then converging to one identical price-endpoint (law of one price) |
| DER_M5 | Pricing/Valuation of Forwards | a price-flag locked and planted ahead on a future timeline point, with a carry-adjustment along the path |
| DER_M6 | Pricing/Valuation of Futures | a daily settlement staircase resetting each step, anchored to a central clearinghouse hub |
| DER_M7 | Interest Rate & Other Swaps | two counterparties exchanging a fixed-stream and a floating-stream across a bridge |
| DER_M8 | Pricing/Valuation of Options | an asymmetric hockey-stick payoff shape rising from a flat floor past a strike-point |
| DER_M9 | Option Replication / Put-Call Parity | a level beam holding two stacked baskets that balance (call+bond equals put+stock) |
| DER_M10 | One-Period Binomial Model | a single node splitting into an up-branch and a down-branch of a valuation lattice |

## PC — Portfolio Construction (6)

| CODE | Module | SCENE fragment |
|---|---|---|
| PC_M1 | Portfolio Risk & Return I | two assets combining into a bulging efficient-frontier arc on a risk-return plane |
| PC_M2 | Portfolio Risk & Return II | a capital-market-line tangent from a risk-free anchor-point up to a market-portfolio star |
| PC_M3 | Portfolio Management: Overview | a lifecycle loop around an investor — plan, execute, feedback — as a closed cycle |
| PC_M4 | Portfolio Planning & Construction | building blocks assembling onto an IPS blueprint scaffold (constraints and objectives) |
| PC_M5 | Behavioral Biases of Individuals | a head profile whose rational gears are warped by a tilted emotional distortion-lens |
| PC_M6 | Introduction to Risk Management | a risk-governance control panel with a shield and a downside-limiting governor dial |

## ALT — Alternative Investments (7)

| CODE | Module | SCENE fragment |
|---|---|---|
| ALT_M1 | Features, Methods & Structures | a fund-structure pyramid (general partner at apex, limited partners at base) holding varied alt-assets |
| ALT_M2 | Performance & Returns | a fee/return waterfall cascading over a hurdle-step before a carry split |
| ALT_M3 | Private Capital: Equity & Debt | a private unlisted company behind a gate fed by an equity-stream and a debt-stream |
| ALT_M4 | Real Estate & Infrastructure | a property skyline beside an infrastructure bridge and a utility tower |
| ALT_M5 | Natural Resources | a trio — a farmland field, an oil barrel, a stacked metal ingot (land, energy, metals) |
| ALT_M6 | Hedge Funds | a literal manicured garden-hedge shaped around a paired long-up and short-down arrow |
| ALT_M7 | Introduction to Digital Assets | linked cube-blocks forming a chain across a distributed network of glowing nodes |

## ETH — Ethics (3)

| CODE | Module | SCENE fragment |
|---|---|---|
| ETH_M1 | Ethics & Trust in the Profession | a keystone bridge of trust arching between an investor figure and the profession |
| ETH_M2 | Code of Ethics & Standards | the Code as engraved stone pillars/tablets with a guiding compass set before them |
| ETH_M3 | Ethics Application | a compass needle navigating a forked crossroads (applying the standards to a real dilemma) |

---

## Tổng kết phân bổ

- **97 module**: QM 11 · ECO 9 · COR 7 · FSA 13 · EQ 12 · FIX 19 · DER 10 · PFM 6 · ALT 7 · ETH 3.
- Memory ghi "~104" — thực đếm file docx là **97**. Chênh có thể do: (a) 10 cover cấp subject (dự tính sơn dầu, style khác — chưa nằm trong 97 này); (b) đếm ước lượng cũ. Cần xác nhận trước khi batch.
