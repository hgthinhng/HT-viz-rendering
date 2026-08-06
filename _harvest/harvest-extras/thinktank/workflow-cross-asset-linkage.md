---
title: "Workflow — Cross-asset Linkage Analysis (OPVIA Sigma)"
module_type: "workflow"
file_name: "workflow-cross-asset-linkage.md"
owns_contract: "Output Contract 3 — Linkage Analysis (1-2 pages, linkage matrix + scenario table + monitoring indicators)"
primary_triggers:
  - "linkage"
  - "ảnh hưởng X tới Y"
  - "cross-asset"
  - "FX-equity correlation"
  - "rate cycle equity"
  - "oil CPI VN passthrough"
  - "USD/VND tới VN-Index"
  - "DXY spillover VN"
when_to_use:
  - "Khi user hỏi 'ảnh hưởng của A tới B', 'A move thì B như thế nào', 'correlation A-B'."
  - "Khi user hỏi passthrough commodity → CPI VN, hoặc FX → rates, hoặc rates → equity."
  - "Khi Daily Brief auto-flag handoff mục 7 (Section 6 risk flag cross-asset)."
when_not_to_use:
  - "Không dùng cho single-name analysis — redirect sang workflow-deep-dive."
  - "Không dùng cho regime classification — redirect sang framework-regime-v11 + workflow-regime-shift-alert."
  - "Không dùng để dự báo giá — output là linkage diagnostic + scenario bounds, không point forecast."
related_modules:
  - "framework-regime-v11.md"
  - "domain-macro-vn-transmission-channels.md"
  - "domain-fx-usd-vnd-dynamics.md"
  - "domain-commodities-vn-impact.md"
  - "domain-cross-asset-correlation-regimes.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
  - "workflow-daily-brief.md"
  - "workflow-regime-shift-alert.md"
status: "v1.0 — Phase 2 Wave 5 Lane 1. Owns Output Contract 3."
---

# Workflow — Cross-asset Linkage (OPVIA Sigma)

> **Owner:** Output Contract 3 (Linkage Analysis, 1-2 pages, table-heavy).
> **Phiên bản:** v1.0 — Phase 2.
> **Ngày chốt:** 2026-04-19.
> **Người dùng:** OPVIA analyst (firm project OPVIA Research & Advisory).
> **Vị trí:** `workflow-cross-asset-linkage.md`. Cặp đôi với `framework-regime-v11.md`, `domain-cross-asset-linkage-matrix-vn.md`, `domain-macro-vn-transmission-channels.md`.

---

## 1. RAG HEADER — Khi nào kích hoạt

### 1.1 Trigger keywords

- Trực tiếp: `"linkage"`, `"cross-asset"`, `"correlation X-Y"`, `"passthrough"`, `"spillover"`, `"transmission"`.
- Gián tiếp (biến thể Việt): `"ảnh hưởng X tới Y"`, `"X move thì Y như thế nào"`, `"X sẽ tác động Y bao nhiêu"`, `"kênh nào truyền dẫn X sang Y"`.
- Cặp phổ biến: `oil → CPI VN`, `DXY → USD/VND`, `UST 10Y → VN bond yield`, `USD/VND → VN-Index`, `gold → VNI`, `Brent → GAS/PLX/PVS`, `credit growth → BĐS`, `FII flow → VN-Index`.

### 1.2 Workflow ownership

- **Workflow này OWN Output Contract 3.** Không workflow khác được generate Linkage Matrix format.
- **Anchor dependency bắt buộc:** `framework-regime-v11.md` — mọi linkage strength assessment phải regime-conditional (linkage strength khác nhau ở R1 vs R3 vs R4).
- **Domain dependency theo cặp asset:** load domain module của asset A + asset B. VD: `oil → CPI VN` load `domain-commodities-vn-impact.md` + `domain-macro-vn-transmission-channels.md`.

### 1.3 Composition rule

Linkage analysis = anchor regime + map channels + regime-conditional strength + bounds + breakers + VN overlay. Không tự dự báo giá. Không tự khuyến nghị hedge. Chỉ diagnostic + scenario bounds.

---

## 2. SIX-STEP LINKAGE PROTOCOL

Mọi linkage analysis follow đúng 6 bước theo thứ tự. Không skip, không đảo. Empty step render `[KHÔNG ÁP DỤNG — lý do]` thay vì im lặng.

### Step 1 — A→B Identification

- **Input:** Analyst chỉ rõ asset/variable A (driver) và B (impact target). Nếu analyst chỉ nói "ảnh hưởng X" mà không rõ target → tôi ask back 1 câu để clarify, không tự assume.
- **Output:** 1 dòng fact statement: `A = [định nghĩa cụ thể, unit, source]. B = [định nghĩa cụ thể, unit, source]. Direction: A → B (A drives B, không reversal trong scope).`
- **Regime anchor:** Call regime hiện tại (pull từ Daily Brief hoặc framework-regime-v11 nếu regime call đã stale > shelf life). Verdict: `Regime hiện tại: Rx (ngày Y, shelf life Z).`
- **Scope statement:** Time horizon cho linkage analysis (default: 1-3 tháng forward). Scope rộng hơn → flag "structural linkage, multi-regime", scope ngắn hơn → flag "tactical linkage, cần monitor real-time".

### Step 2 — Map Transmission Channels (3-5 channels)

- Liệt kê **3-5 channels phổ biến** mà A có thể truyền dẫn sang B. Channel = mechanism cụ thể, không vague.
- Mỗi channel: `Channel name | Mechanism 1-dòng | Lag ước lượng | Historical precedent`.
- **Cấm vague channel** kiểu "sentiment channel" không có mechanism. Mỗi channel phải có causal chain rõ.
- **VN-specific channels ưu tiên:** NHNN reaction function, VAS accounting treatment (BCTC hiệu ứng), sector structure VN (tỷ trọng ngành trong VN-Index), CPI basket VN (weight xăng dầu, thực phẩm).

### Step 3 — Strength Assessment (regime-conditional)

- Mỗi channel được đánh giá strength theo regime hiện tại — **qualitative** (mạnh / trung bình / yếu), không pseudo-precision %.
- Format: `Channel | Strength R1 | Strength R2 | Strength R3 | Strength R4 | Strength R5 | Strength hiện tại`.
- **Regime-dependency là nguyên tắc cốt lõi:** Linkage strength ≠ hằng số. Cùng 1 channel có thể strong ở R4 (stress) và weak ở R2 (goldilocks).
- Nếu empirical data VN không đủ dài để test cross-regime → flag `[LIMITED VN HISTORY — cross-regime assumption rely on global analog]`.

### Step 4 — Bounds Analysis (A move X → B move bao nhiêu)

- Format table: `Scenario A move | B move range qualitative | B move range quantitative (khi có basis) | Điều kiện trigger`.
- **3 scenario chuẩn:** Base (A move in expected range), Stress (A move >2σ), Tail (A move >3σ hoặc structural break).
- Range phải **wide**, không pseudo-precise. VD: "Oil +$20 → CPI VN +0.3-0.7% trong 3-6 tháng" (không phải "+0.5%").
- Nếu A và B có **multicollinearity cao** với biến thứ ba (Z) → flag `[MULTICOLLINEAR — A không drive B độc lập, Z chia sẻ variance]` + không probability-weighted.

### Step 5 — Channel Breakers (khi nào correlation gãy)

- **Channel breaker** = điều kiện mà channel ngừng hoạt động hoặc đảo chiều. Phải identify ít nhất 2 breaker cho mỗi channel chính.
- Breaker phổ biến: regime shift (R2→R4 có thể đổi dấu correlation), policy intervention (NHNN FX intervention), supply shock (OPEC+ cut), fiscal response (giảm thuế xăng dầu), capital controls, step-function shock (Rule D veto).
- Format: `Breaker condition | Channel affected | Historical precedent (nếu có)`.
- **Purpose:** Khi monitoring indicator breach breaker condition → linkage analysis needs re-run.

### Step 6 — VN-specific Overlay

- Mọi channel từ global → VN phải check 3 layer VN overlay:
  - **Policy layer:** NHNN reaction function (thường lag 1-3 tháng sau Fed), MOF fiscal tools (giảm thuế, price ceiling), NHNN FX intervention threshold (>$5bn/tuần per framework-regime-v11 Rule D).
  - **Structural layer:** CPI basket weight VN (xăng dầu ~9%, thực phẩm ~34%), VN-Index sector composition (banks ~30%, BĐS ~15%, industrials ~12%), tỷ trọng FII trong free-float HOSE (~18-22%).
  - **Market microstructure:** Bond market shallow (C2 correlation unreliable — xem framework-regime-v11 §8.4), 90% NĐT cá nhân → flight-to-cash thay vì flight-to-quality, margin cascade risk trong stress.
- Output 1 paragraph: `VN overlay khiến channel X [mạnh hơn / yếu hơn / lagged / quirked] so với global analog do [lý do cụ thể].`

---

## 3. OUTPUT FORMAT — Contract 3 Hard Rules

### Rule L1 — Length cap

- **Target:** 800-1500 từ tiếng Việt (1-2 pages).
- **Hard cap:** 1500 từ. Vượt → compress Step 5 Breaker narrative trước, giữ nguyên Step 2-3-4.

### Rule L2 — Table-heavy

- **Tối thiểu 3 table:** (i) Linkage Matrix (Step 2-3), (ii) Scenario Table (Step 4), (iii) Monitoring Indicators (xem §4).
- Không prose paragraphs >3 câu. Mọi assessment nén vào table cells.

### Rule L3 — Regime-conditional mandatory

- Mỗi linkage claim phải gắn regime context: "Trong R3, channel X mạnh" thay vì "Channel X mạnh".
- Regime call phải có ngày + shelf life.

### Rule L4 — No point forecast

- Cấm câu kiểu "CPI VN sẽ đạt 4.2% vào tháng 8".
- Thay bằng range + điều kiện: "Nếu Brent sustained >$90 trong 3 tháng, CPI VN có thể vào range 3.8-4.5% với passthrough assumption β=0.08-0.12".
- Qualitative probability only (low / medium / high), không bịa số %.

### Rule L5 — Voice + safety scan

- Vietlish scan, soft-tone scan, pseudo-precision scan (theo Custom Instructions §3.1-3.3).
- No recommendation leak ("nên hedge VND", "khuyến nghị short oil").
- Label SỰ KIỆN / DIỄN GIẢI / GIẢ THUYẾT cho mọi multi-paragraph claim.

---

## 4. MONITORING INDICATORS — Required output

Cuối mọi linkage output, có section **Monitoring Indicators** (table-form) gồm:

| Indicator | Current value | Threshold trigger | Breaker condition | Re-run linkage khi |
|---|---|---|---|---|
| [Biến driver A] | [hiện tại] | [level breach] | [channel breaker] | [điều kiện] |
| [Biến impact B] | [hiện tại] | [level breach] | [channel breaker] | [điều kiện] |
| [Biến confounding Z] | [hiện tại] | [level breach] | [multicollinearity flag] | [điều kiện] |
| [Policy proxy — NHNN OMO, Fed, MOF] | [hiện tại] | [policy response threshold] | [Rule D veto] | [điều kiện] |

Mục đích: Analyst tự track post-hoc. Khi 1/4 threshold breach → re-run linkage, không giữ analysis stale.

---

## 5. WORKED EXAMPLE — Oil → CPI VN Passthrough

### 5.1 Setup giả dụ

Analyst asked: "Ảnh hưởng của Brent tới CPI VN nếu oil duy trì $95-100 trong 6 tháng tới. Regime hiện tại R3."

### 5.2 Output linkage analysis (minh họa Contract 3)

---

**Regime anchor:** R3 — Đỉnh chu kỳ / Quá nhiệt (call 2026-04-19, shelf life 1-2 tuần, invalidate nếu DXY <103 hoặc UST 10Y <4.3% sustained 5 phiên).

**Scope:** Brent (ICE, USD/bbl, 3-month rolling average) → CPI VN headline (GSO, yoy). Horizon 3-6 tháng forward. Direction: Brent drives CPI VN passthrough; reverse ignored (VN không phải swing producer).

#### Linkage Matrix — 4 channels

| # | Channel | Mechanism 1-dòng | Lag | Historical precedent |
|---|---|---|---|---|
| 1 | **Direct fuel passthrough** | Brent → giá xăng dầu retail VN (xăng A95, diesel) → CPI weight xăng dầu ~9.4% | 2-6 tuần (điều chỉnh 7-10 ngày/lần theo NĐ 95/2021) | 2022 H1 Brent $110 → CPI xăng +60% yoy |
| 2 | **Logistics passthrough** | Xăng/diesel → cước vận tải → giá thực phẩm + hàng tiêu dùng → CPI basket thực phẩm (~34%) + consumer goods | 1-3 tháng | 2011 oil peak → CPI food +15-20% lag 2-3 tháng |
| 3 | **Electricity cost channel** | Oil/gas → EVN input cost (thermal ~30%) → điều chỉnh giá điện → CPI utilities (~3.5%) | 6-12 tháng (lag do MOF phê duyệt) | 2022-2023 EVN loss → 2024 tăng giá điện 2 lần |
| 4 | **NHNN reaction (feedback loop)** | Oil → CPI breach 4% → NHNN tightening signal → VND defense → import cost fbk | 2-4 tháng | 2018 H2 + 2022 H2 — NHNN tăng rate khi CPI breach |

#### Strength Assessment — Regime-conditional

| Channel | R1 | R2 | R3 hiện tại | R4 | R5 |
|---|---|---|---|---|---|
| 1 Fuel direct | Trung bình | Trung bình | **Mạnh** | Mạnh (nhưng bị cản bởi giảm thuế bảo vệ môi trường) | Yếu (demand collapse) |
| 2 Logistics | Yếu | Trung bình | **Trung bình** | Mạnh (cost push + FX) | Yếu |
| 3 Electricity | Yếu | Yếu | **Yếu-Trung bình** | Trung bình (MOF cho phép tăng giá để EVN survive) | Yếu |
| 4 NHNN feedback | — | — | **Mạnh** (NHNN signal siết) | Veto trigger | Ineffective |

DIỄN GIẢI: Trong R3 hiện tại, channel 1 (direct fuel) + channel 4 (NHNN feedback) là dominant. Channel 2 (logistics) lag 1-3 tháng, sẽ kick-in trong Q3 nếu oil sustained. Channel 3 (electricity) có policy gate → MOF quyết định timing, không market-driven.

#### Bounds Analysis — 3 scenarios

| Scenario | Brent 3M avg | CPI VN passthrough range | Điều kiện |
|---|---|---|---|
| **Base** | $85-95 | CPI yoy 3.8-4.3% (vs hiện 3.5%) | Channel 1+2 active, channel 3 không kick; NHNN hold rate |
| **Stress** | $95-110 sustained >3 tháng | CPI yoy 4.5-5.2% | Channel 1+2 full, channel 4 activate → NHNN tăng rate điều hành 50-100bps; R3→R4 transition probability **trung bình-cao** |
| **Tail** | >$110 + supply shock (Strait of Hormuz, Iran-US escalation) | CPI yoy 5.5-7%+ stagflation | Channel 1-2-3-4 đồng thời + step-function shock — **framework-regime-v11 Rule D veto triggered**, chuyển sang scenario riêng ngoài regime thông thường |

GIẢ THUYẾT: Passthrough coefficient β_oil→CPI (elasticity) ước 0.08-0.12 dựa trên 2011, 2018, 2022 VN analog. [Bậc 3 — Bằng chứng sơ bộ]. Wide range do (i) thuế BVMT xăng dầu MOF có thể adjust làm nonlinear passthrough, (ii) fx component (oil priced USD, VND mất giá trong R3 → double cost push).

#### Channel Breakers

| Breaker condition | Channel affected | Historical precedent |
|---|---|---|
| MOF giảm thuế bảo vệ môi trường xăng dầu (từ 4,000đ xuống 1,000-2,000đ) | Channel 1 direct fuel passthrough giảm 40-60% | 2022 H2: giảm từ 4,000 xuống 1,000đ → hiệu lực 6 tháng |
| Brent crash <$65 (demand collapse scenario R4/R5) | Channel 1+2 đảo chiều (disinflation) | 2015-2016 oil crash → CPI VN về 0-1% |
| NHNN tăng rate điều hành >100bps trong 1 quý | Channel 4 feedback full activate → aggregate demand compress → offset channel 1-2 | 2022 Q4 |
| EVN được phép tăng giá điện >8%/lần | Channel 3 spike + secondary passthrough | 2023 Q2 + Q4 |
| Step-function shock Strait of Hormuz close | **Rule D veto** — framework suspended, shift sang scenario geopolitical | 1973, 1979, 2019 (partial) |

#### VN Overlay

**Policy layer:** NHNN thường phản ứng CPI với lag 2-4 tháng (historical 2018, 2022). Khi CPI breach 4% → NHNN signal siết; breach 5% → buộc tăng rate điều hành. MOF có đòn bẩy thuế BVMT xăng dầu (công cụ nonlinear, politically-gated).

**Structural layer:** CPI basket VN nặng thực phẩm (~34%) hơn OECD (~15%) → channel 2 (logistics) VN mạnh hơn global analog. Xăng dầu weight ~9.4% → channel 1 direct medium. Electricity weight ~3.5% → channel 3 small but sticky.

**Market microstructure:** VN không có futures oil local → hedge phụ thuộc offshore; airlines (HVN, VJ) + steel (HPG — coke cost) + logistics (GMD, HAH) là equity sector bị hit trực tiếp. Shallow bond market → channel 4 NHNN feedback chủ yếu qua OMO + tín hiệu hành chính, không qua bond yield.

#### Monitoring Indicators

| Indicator | Current value | Threshold trigger | Breaker | Re-run linkage khi |
|---|---|---|---|---|
| Brent 3M rolling | $78 (2026-04-19) | >$95 sustained 3 tháng | Crash <$65 | Breach range Base |
| CPI VN yoy | 3.5% (Mar 2026 proxy) | >4.5% | MOF giảm thuế xăng | Breach trigger |
| USD/VND q/q | +1.4% (gần threshold Rule D) | >1.5% q/q + NHNN intervention | DXY peak + Fed pivot | Rule D veto condition |
| NHNN OMO net 5d avg | +10,000 VND bn (inject) | Chuyển withdraw >3 phiên | — | Channel 4 activate signal |
| Xăng A95 retail | 24,500 VND/lít | Breach 27,000 (lịch sử R3 peak) | Thuế BVMT giảm | Channel 1 intensity |

---

GIẢ THUYẾT / open questions: (i) β_oil→CPI có thể đã đổi sau 2022 structural (EVN pricing reform + MOF thuế xăng elasticity). [Bậc 3]. (ii) Kết quả scenario Tail phụ thuộc vào Iran-US escalation path — outside model, xử lý qua Rule D.

**Suggested next-step:** (i) Chạy `workflow-regime-shift-alert` nếu Brent breach $95 + CPI breach 4.2% đồng thời. (ii) `workflow-deep-dive` cho equity sector bị impact (HVN, VJ, HPG, GMD) với input linkage strength R3.

---

### 5.3 Word count check (example)

Output example ~1,250 từ (trong target 800-1500). 5 tables. Regime call complete. Wide scenario bounds. No point forecast. NHNN reaction function overlay đầy đủ. VN CPI basket structural overlay applied.

---

## 6. QUALITY CHECKLIST — 9-item pre-output

Tôi pass checklist ngầm trước khi gửi. Fail → sửa trước output.

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Regime anchor** | Step 1 có regime call + ngày + shelf life + invalidation trigger |
| 2 | **6-step protocol** | Step 1-6 đầy đủ, đúng thứ tự, không skip |
| 3 | **Min 3 channels** | Step 2 có ≥3 channels với mechanism rõ |
| 4 | **Regime-conditional strength** | Step 3 có strength assessment cho ≥3 regime (không flat "strong" toàn cycle) |
| 5 | **Wide bounds** | Step 4 có range (min-max), không point forecast |
| 6 | **Min 2 breakers/channel chính** | Step 5 có breaker cụ thể, không vague |
| 7 | **VN overlay 3-layer** | Step 6 cover policy + structural + microstructure |
| 8 | **Monitoring indicators table** | §4 có ≥4 indicators với threshold + breaker |
| 9 | **Voice + safety scan** | No Vietlish, soft-tone, pseudo-precision, recommendation leak |

---

## 7. HANDOFF CONDITIONS

| Condition trong linkage output | Next-step suggest |
|---|---|
| Scenario Stress hoặc Tail hit R3→R4 transition | `workflow-regime-shift-alert` (Contract 6) |
| Channel breaker Rule D veto triggered | `workflow-regime-shift-alert` + escalation |
| Equity sector impact concrete (HPG, HVN, GMD etc.) | `workflow-deep-dive` (Contract 2) per ticker |
| FX channel dominant (USD/VND → Y) | Load `domain-fx-usd-vnd-dynamics.md` sâu hơn |
| Linkage stale > 2 tháng (monitoring breach) | Re-run linkage workflow với data mới |

---

## 8. EDGE CASES

| Tình huống | Xử lý |
|---|---|
| User hỏi bidirectional ("A ↔ B") | Tách thành 2 linkage runs: A→B và B→A, flag rõ mỗi hướng |
| A và B có multicollinearity cao với Z (VD: DXY, UST, Fed stance co-move) | Flag `[MULTICOLLINEAR — kiểm soát Z]` + dùng qualitative only, không point forecast |
| VN data không đủ dài để calibrate β | Flag `[LIMITED VN HISTORY]` + dùng global analog (EM proxy) với caveat |
| User yêu cầu "hedge recommendation" | Từ chối per Safety Rule 2, redirect sang "signpost + breaker identification" framing |
| Step-function shock đang active (chiến tranh, cấm vận) | Rule D veto invoked, linkage suspended, note "framework regime thông thường không apply trong shock window" |
| Cặp asset không phổ biến (VD: copper → PVB) | Build linkage-from-scratch với tối thiểu 2 channels + wide bounds + high uncertainty flag |

---

## 9. VERSION + MAINTENANCE

- **Locked Phase 2:** 6-step protocol, Contract 3 hard rules L1-L5, 9-item quality checklist.
- **Open for revise sau Sprint 1-2:** Passthrough coefficients (β_oil→CPI, β_DXY→VND) cần empirical update khi có data VN mới; breaker thresholds (oil $65/$95, USD/VND 1.5%) calibrate theo framework-regime-v11 §11 analyst review.
- **Phase 3 consideration:** Behavioral Layer overlay (FII positioning, broker survey) khi framework-regime-v11 Layer 4 ship.

---

**Hết workflow-cross-asset-linkage.md v1.0 (Wave 5 Lane 1).**

Reference: Focus_Brief.md §6 Workflow 3 + §9 Contract 3; framework-regime-v11.md §6-§7; workflow-daily-brief.md §7 handoff pattern.
