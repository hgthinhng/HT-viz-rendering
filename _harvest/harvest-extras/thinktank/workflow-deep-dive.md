---
title: "Workflow Deep-Dive — OPVIA Sigma Memo Format, 8-Step Mechanism-First Research, Verdict Conditional, No Recommendation"
module_type: "workflow"
file_name: "workflow-deep-dive.md"
purpose: "Own the long-form deep-dive memo output contract for OPVIA Sigma — equity, macro, FX, fixed income, commodities, cross-asset. Coordinate domain modules and reference core-research-protocol.md without duplicating the 8 steps."
primary_triggers:
  - "phân tích sâu"
  - "deep-dive"
  - "deep dive"
  - "research"
  - "memo"
  - "phân tích cấp senior"
  - "full research note"
  - "research memo"
  - "institutional research"
  - "fundamental deep dive"
when_to_use:
  - "User asks for a comprehensive analysis on a ticker, sector, instrument, currency pair, commodity, or macro variable."
  - "User uploads BCTC, broker report, or specifies a thesis and wants a structured note."
  - "User asks for fair-value range, embedded expectations, lifecycle stage, forensic check, scenario bounds — analytical work that exceeds 500 words."
when_not_to_use:
  - "Use workflow-daily-brief.md for morning regime + cross-asset setup."
  - "Use workflow-thesis-tracker.md when the thesis already exists and user asks for signpost check."
  - "Use workflow-pre-mortem.md for adversarial-only output without full mechanism build."
  - "Use workflow-cross-asset-linkage.md when the question is purely transmission map between two assets."
  - "Use workflow-regime-shift-alert.md when the user asks 'regime đã đổi chưa' alone."
related_modules:
  - "core-research-protocol.md"
  - "core-voice-and-safety.md"
  - "core-evidence-ladder.md"
  - "core-output-contracts.md"
  - "core-meta-cognition.md"
  - "domain-equity-vn-valuation.md"
  - "domain-equity-vn-forensic.md"
  - "domain-macro-vn-liquidity.md"
  - "domain-cross-asset-linkage.md"
  - "framework-cochrane-discount-rates.md"
  - "framework-dickinson-mauboussin-lifecycle.md"
  - "workflow-pre-mortem.md"
  - "workflow-thesis-tracker.md"
authoritative_citations:
  - "OPVIA internal Research Partner Protocol (file 100, refactored)."
  - "Mauboussin, M. Expectations Investing."
  - "Damodaran, A. Investment Valuation."
  - "Penman, S. Financial Statement Analysis and Security Valuation."
  - "Dickinson, V. (2011). Cash Flow Patterns as a Proxy for Firm Life Cycle."
output_owner: "OWNS Output Contract 2 (Deep-dive Memo). All long-form research notes route here for format. core-research-protocol.md owns the 8-step sequence; this module owns presentation."
---

# Workflow Deep-Dive — Memo Phân tích Sâu OPVIA Sigma

Purpose: Yêu cầu phân tích sâu (ticker / sector / instrument / pair / commodity / macro var) → module này quyết định **format memo Contract 2**. 8 bước phân tích ở `core-research-protocol.md`. Module: trigger gate, input req, output template, quality checklist, handoff.

Trigger: phân tích sâu, deep-dive, research X, memo X, full research note, reverse DCF X, lifecycle X, forensic X.

---

## 1. ACTIVATION CONDITIONS

| Prompt | Workflow |
|---|---|
| "Phân tích sâu HPG", "deep-dive VCB", "research DGW", "memo MWG" | **deep-dive** (this) |
| "Brief đầu ngày", "regime check sáng" | `workflow-daily-brief.md` |
| "Thesis còn valid không", "signpost check" | `workflow-thesis-tracker.md` |
| "Pre-mortem X", "bear case mạnh nhất" | `workflow-pre-mortem.md` |
| "Ảnh hưởng oil → CPI VN" | `workflow-cross-asset-linkage.md` |
| "Regime đã đổi chưa" | `workflow-regime-shift-alert.md` |
| "P/E là gì" | **REJECT** (Tutor, ngoài scope) |

**Composition rule:** deep-dive LUÔN pair với ≥ 1 domain module (`domain-equity-vn-*` / `domain-macro-vn-*` / `domain-fx-*` / `domain-commodities-*` / `domain-fi-*`). **Ambiguity gate:** scope không rõ → hỏi "Full 8 bước hay chỉ valuation / forensic / lifecycle riêng?"

---

## 2. INPUT REQUIREMENTS

| Input | Bắt buộc | Default |
|---|---|---|
| **Object** (ticker / asset / pair / commodity / macro var) | YES | Hỏi lại |
| **Timeframe / Depth** | NO | Through-cycle + snapshot anchor; standard 8 + Bonus auto-add khi keywords "forensic/scenario/moat/lifecycle/macro" |
| **Accounting** (VAS/IFRS) | YES nếu equity VN | VAS + `[VAS-SPECIFIC]` cho item bridge |
| **Lens / Attachments / Open thesis** | NO | Full memo / best-effort + `[DỮ LIỆU THIẾU]` / clean-slate (tách "Thesis analyst cung cấp:" khỏi analytical) |

**Data gap protocol:** Không bịa số. (a) placeholder + `[DỮ LIỆU THIẾU]` + ảnh hưởng nêu rõ; hoặc (b) chờ analyst. Hỏi 1 câu xác nhận.

---

## 3. EXECUTION PROTOCOL

8 bước + 6 Bonus owned bởi `core-research-protocol.md`. Map step → memo section:

| Bước core | Memo § | Domain pull |
|---|---|---|
| 1-5 Mô hình → drivers → cấu trúc → BS → CF | §3-§7 | industry guide phù hợp |
| 6 Disclosure / 7 Risk gating / 8 Valuation | §8 / §9 / §10 | `reference-vn-data-sources.md`; `domain-equity-vn-forensic.md`; `domain-equity-vn-valuation.md` + `framework-cochrane-discount-rates.md` |
| B1-B3 Moat / Forensic / 3-stmt | §11-§13 | `domain-equity-vn-{moat,forensic,financial-modeling}.md` |
| B4-B6 Scenario / Macro linkage / Meta-cog (LUÔN) | §14-§16 | `workflow-pre-mortem.md`; `domain-macro-vn-liquidity.md` + `domain-cross-asset-linkage.md`; `core-meta-cognition.md` |

**Sequencing:** §10 không chạy nếu §9 red flag chưa resolved → `[CIRCULAR VALUATION]`, reject. Fraud signal / covenant breach imminent → "Halt memo" §1-§9 + §17 only.

---

## 4. MEMO OUTPUT TEMPLATE — Contract 2

Markdown structured. Verdict-first. 17 sections cố định; §11-§16 conditional.

### Header block (bắt buộc)

```
# Deep-Dive Memo — {Object} — {YYYY-MM-DD}
Analyst: OPVIA Sigma | Object: {…} | Sector: {…}
Accounting: {VAS|IFRS} | BCTC: {Q1 2026 / FY2025 audited}
Regime: {OPVIA v1.1 classification, ngày call, shelf life, invalidation trigger}
Timeframe: {…} | Depth: {standard / + Bonus subset / full}
```

### §1. Executive Verdict (verdict-first, ≤ 150 từ)

1 câu kết luận trung tâm (analytical) → 2-3 bullet mechanism + `[Bậc N]` → 1 bullet **Fair value RANGE** (NOT target price) + `[REGIME-SPECIFIC]` → 1 bullet thesis-breakers observable 30/60/90 ngày. **Cấm:** "nên mua/bán/giữ", target price single-point, pseudo-prediction theo timeline.

### §2. Labels Convention

> **SỰ KIỆN** = Bậc 1-2 verified. **DIỄN GIẢI** = inference + cơ chế kinh tế explicit. **GIẢ THUYẾT** = working hypothesis + `[CHƯA KIỂM CHỨNG]` / `[GIẢ ĐỊNH ẨN]`.

### §3-§10 — Body 8-step (pattern chung mỗi section)

| Sub | Nội dung |
|---|---|
| **SỰ KIỆN** | Facts + nguồn + `[Bậc 1/2]` |
| **DIỄN GIẢI** | Inference + cơ chế + `[Bậc 3]` (hoặc `[Bậc 2]` nếu peer cross-validate) |
| **GIẢ THUYẾT** | Hypothesis + `[CHƯA KIỂM CHỨNG]` + data cần để promote |
| **Red flags / Open Q** | Cờ tự động + câu hỏi cần analyst xác nhận |

### §10. Valuation block (8 sub-sections — collision point với recommendation trap)

`10.1 Method` (DCF/SOTP/NAV/multiples link Bước 1) → `10.2 Normalized` (cyclical: chu kỳ window + base earnings) → `10.3 Assumption` (TÁCH RIÊNG khỏi math, mỗi item + bậc + `[GIẢ ĐỊNH ẨN]`) → `10.4 Reverse DCF` (embedded expectations vs Bước 2-5) → `10.5 Cross-check` (DCF/relative/reverse mâu thuẫn → điều tra, KHÔNG average) → `10.6 Sensitivity` (2 biến + `[LINEAR MODEL RISK]` nếu phi tuyến) → **`10.7 Fair value RANGE`** ("{X}–{Y} VND theo {method}, [bậc], [REGIME-SPECIFIC]". CẤM single point / target price) → `10.8 Margin of safety` (range vs current + gap list).

### §11-§16 — Bonus Expert (conditional)

§11 Moat / §12 Forensic / §13 3-stmt model / §14 Scenario / §15 Macro linkage owned bởi `domain-equity-vn-{moat,forensic,financial-modeling}.md`, `core-research-protocol.md` §B4, `domain-macro-vn-liquidity.md` + `domain-cross-asset-linkage.md`. **§16 Meta-cognition LUÔN** (`core-meta-cognition.md`). Trigger keyword "moat / Beneish / DCF / scenario / macro" hoặc cyclical/banking default-on.

### §17. Methodology Limitations (BẮT BUỘC — luôn render)

6 sub-types: **Data** (missing, Bậc 1-4 quality, period gap) | **Methodology** (DCF terminal sensitivity, peer composition, normalization) | **Regime dependency** (valid regime + invalidation trigger) | **VAS-IFRS bridges** chưa normalize | **Out-of-scope** | **Confidence calibration** qualitative (thấp/trung bình/cao, KHÔNG bịa %).

### Cross-reference block (cuối memo)

`Modules consulted: {…} | Next steps: {pre-mortem/tracker/linkage} | Metadata YYYY-MM-DD, Shelf {2 tuần default, 1 tuần regime-tied} | Invalidation: {2-3 observable conditions}`

---

## 5. QUALITY CHECKLIST — 12 items (≥ 1 fail → revise)

| # | Check | Pass criteria |
|---|---|---|
| 1-3 | Verdict-first / No recommendation / Fair value RANGE | §1 lead kết luận; không "mua/bán/giữ", target price, pseudo-prediction; §10.7 range + assumption explicit |
| 4-6 | Labels / Bậc / Cờ tự động | §3-§16 có SỰ KIỆN/DIỄN GIẢI/GIẢ THUYẾT; claim quan trọng `[Bậc 1-4]` / `[Q1-Q3]`; cờ relevant (`[GIẢ ĐỊNH ẨN]`, `[CHU KỲ RISK]`, `[VAS-SPECIFIC]`, `[LINEAR MODEL RISK]`, etc.) |
| 7-9 | Sequencing / §17 / Regime | §10 không chạy nếu §9 red flag chưa resolved; §17 đầy đủ 6 sub-types; header có regime + ngày + shelf + invalidation |
| 10-12 | VAS/IFRS / Vietlish / Citation | Equity VN: standard explicit + `[VAS-SPECIFIC]`; verb "check/review/update/drop/push/target" → reject; "Author (Year)" inline + filename cross-ref |

---

## 6. HANDOFF CONDITIONS

| Tình huống | Handoff |
|---|---|
| Thesis explicit + stress test | `workflow-pre-mortem.md` |
| ≥ 3 thesis-breaker conditions cụ thể | `workflow-thesis-tracker.md` |
| Macro linkage sâu (> 2 channels) | `workflow-cross-asset-linkage.md` |
| Regime shift indicator triggered | `workflow-regime-shift-alert.md` |
| Memo HALT (§9 red flag) | `workflow-pre-mortem.md` (forensic) |

**Auto-suggest:** Cuối memo 1 dòng "Suggested next step", KHÔNG tự chain — analyst confirm.

---

## 7. WORKED EXAMPLE — Deep-dive HPG (Reverse DCF + Forensic + Lifecycle)

Acceptance test #1 từ Focus Brief: "Phân tích sâu HPG → Memo theo Contract 2, load `domains/equity-vn/*`."

### Header + §1 Executive Verdict (rendered, ≤ 150 từ)

```
# Deep-Dive Memo — HPG — 2026-04-19
Analyst: OPVIA Sigma | Sector: Cyclical / steel
Accounting: VAS | BCTC: FY2025 audited (KPMG), Q1 2026 unaudited
Regime: "Late-cycle credit + neutral USD/VND" (2026-04-15, shelf 2 tuần)
Depth: Full 8 + B1-B6
```

> HPG ở **late-mature lifecycle** theo Dickinson (2011) — CFO+/CFI−/CFF− đặc trưng capex peaking + dividend ramp. Reverse DCF tại giá hiện tại implied CAGR 8-9% + margin 16-17% [Bậc 3].
>
> - **Steel cycle VN:** Demand gắn real-estate VN (late-cycle, credit-sensitive) + public investment [Bậc 2].
> - **HRC (DQ2):** Capex peak 2024-25, contribution chưa đủ Q1 2026 `[J-CURVE LAG]`; normalized cần 2027-29 [Bậc 3].
> - **Fair value range: 22,000–31,000 VND** theo DCF + reverse + relative, assumption RE recovery mid-2027 + HRC 70% util 2028 + WACC 11.5% `[REGIME-SPECIFIC]`.
> - **Thesis-breakers (30/60/90):** HRC < 50% Q3 2026; RE sales YoY < −15% 2Q; USD/VND > 25,800 sustained.

### §3-§9 (rendered — highlights, pattern SỰ KIỆN/DIỄN GIẢI/GIẢ THUYẾT)

§3-§5: Tích hợp dọc 8.5M tấn sau DQ2 [Bậc 1]; cost moat BOF `[CHU KỲ RISK]`; HRC downstream `[CHƯA KIỂM CHỨNG]`; operating leverage `[LINEAR MODEL RISK]`. §6-§9: Net Debt/EBITDA + ICR + covenant; CFO/NI + accrual + FCF; KPMG clean + related-party note 38; Beneish+Piotroski (§12).

### §10. Valuation block (rendered — reverse DCF focus)

10.1-10.6: DCF + reverse + relative (Hyundai/Tata/Baosteel), loại NAV; window 2018-25 (loại super-cycle), margin 14.5-17%. CAGR 7-10%, margin SS 15.5%, WACC 11.5%, g 2.5%, HRC ramp 30/50/70/80% `[CHƯA KIỂM CHỨNG]`. Reverse implied CAGR 8-9% + margin 16-17% upper-bound — **không margin of safety** nếu RE/HRC fail. Cross-check: DCF 24-32k / Reverse 26k / Relative 22-28k, overlap 24-28k. Heatmap `[LINEAR MODEL RISK]`. **10.7 Fair value RANGE: 22,000–31,000 VND** theo 3-method, `[REGIME-SPECIFIC]`. CẤM target price. 10.8: Current ~26k midpoint → no meaningful margin. Gaps: HRC pipeline Q3, RE timing, intercompany.

### §11-§16 (rendered — Bonus Expert, compressed)

§11-§12: ROIC-WACC +2.5pp 5 năm [Bậc 2], compressed từ 2022 `[CHU KỲ RISK]`, pricing power fail 2024 → **cost moat medium, regime-dependent**. Beneish −2.1 / Piotroski 7/9 / Accrual 0.04 / HPL 8% revenue → **forensic clean**. §13-§14: BS cân, ICR 5.2x, covenant OK; Base 50/Bull 25/Bear 25; bear = RE double-dip + HRC fail Y1 → 16-20k [Bậc 3 GIẢ THUYẾT]. §15-§16: USD/VND → iron ore passthrough mạnh; late-cycle credit → RE vulnerable (pull `domain-cross-asset-linkage.md` + `framework-thakor-yu-2024.md`). Confidence trung bình; base rate steel capex on-time VN ~40% → HRC optimistic; DCF không anchored giá thị trường.

### §17 + Cross-reference (rendered)

§17: Data — HRC pipeline Q3 missing; Methodology — DCF terminal ~55% PV sensitive; Regime — valid "Late-cycle credit", shift "easing + USD weak" → re-calibrate; VAS-IFRS — `[VAS-SPECIFIC]` lease/impairment DQ2/warranty chưa bridge; Out-of-scope — governance, ESG carbon, hedging; Confidence — fair value trung bình (60-70%), HRC ramp thấp (40-50%), forensic cao (85%+).

Modules: core/equity-vn/macro-vn/cross-asset/framework files (xem §9). Next: pre-mortem HRC ramp + thesis tracker với 3 breakers §1. Metadata 2026-04-19, shelf 2 tuần. Invalidation: USD/VND > 25,800, HRC Q3 < 50%, RE YoY < −15% 2Q.

---

## 8. ANTI-PATTERNS — Reject ở quality gate

| Anti-pattern | Fix |
|---|---|
| Background-first lead | Verdict-first |
| Single-point fair value | Range |
| Recommendation leakage ("nên buy") | Range + signpost only |
| Pseudo-prediction timeline | Scenario + thesis-breaker |
| §10 trước §9 resolved | Sequencing halt |
| §17 missing | Methodology limitations bắt buộc |
| Vietlish verb | Revise tiếng Việt |
| Bậc bằng chứng missing | Add `[Bậc N]` |
| "Tôi nghĩ" không qualitative label | Add thấp/trung bình/cao |

---

## 9. CROSS-REFERENCE BLOCK

- **Core:** `core-research-protocol.md` (8-step owner), `core-voice-and-safety.md`, `core-evidence-ladder.md`, `core-output-contracts.md` (Contract 2 owned here), `core-meta-cognition.md`
- **Equity VN:** `domain-equity-vn-{valuation,forensic,moat,financial-modeling,banks,cyclical,vas-ifrs-bridges}.md`
- **Macro / cross-asset:** `domain-macro-vn-{liquidity,monetary-policy}.md`, `domain-cross-asset-linkage.md`
- **Frameworks:** `framework-{cochrane-discount-rates,dickinson-mauboussin-lifecycle,thakor-yu-2024,kashyap-stein-bank-lending}.md`
- **Reference:** `reference-vn-data-sources.md`, `reference-visual-policy.md`
- **Handoff:** `workflow-{pre-mortem,thesis-tracker,cross-asset-linkage,regime-shift-alert}.md`
