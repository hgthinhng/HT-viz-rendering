---
title: "Workflow — Regime Shift Alert (OPVIA Sigma)"
module_type: "workflow"
file_name: "workflow-regime-shift-alert.md"
owns_contract: "Output Contract 6 — Regime Shift Alert (≤ 1 page, banner + variables triggered + new regime + immediate implications)"
primary_triggers:
  - "regime shift"
  - "regime changed"
  - "regime alert"
  - "shift cảnh báo"
  - "auto-flag from daily-brief"
  - "R3 → R4"
  - "R4 → R5"
  - "R5 → R1"
when_to_use:
  - "Khi Daily Brief auto-flag mục 5 (Regime Shift Alert early warning) triggered."
  - "Khi user hỏi trực tiếp 'regime có shift không', 'alert regime', 'có phải đang chuyển regime'."
  - "Khi monitoring indicator breach threshold trong framework-regime-v11 Rule A/B/C/D."
when_not_to_use:
  - "Không dùng cho regime classification lần đầu — redirect sang framework-regime-v11 standalone."
  - "Không dùng cho step-function shock (chiến tranh, đại dịch) — Rule D veto suspend framework, dùng scenario riêng."
  - "Không dùng cho intra-regime drift (VD: R2 stable nhưng variables drift) — chỉ fire khi shift criteria met."
related_modules:
  - "framework-regime-v11.md"
  - "workflow-daily-brief.md"
  - "workflow-cross-asset-linkage.md"
  - "workflow-deep-dive.md"
  - "workflow-pre-mortem.md"
  - "workflow-thesis-tracker.md"
status: "v1.0 — Phase 2 Wave 5 Lane 1. Owns Output Contract 6."
---

# Workflow — Regime Shift Alert (OPVIA Sigma)

> **Owner:** Output Contract 6 (Regime Shift Alert, ≤ 1 page).
> **Phiên bản:** v1.0 — Phase 2.
> **Ngày chốt:** 2026-04-19.
> **Người dùng:** OPVIA analyst (firm project OPVIA Research & Advisory).
> **Vị trí:** `workflow-regime-shift-alert.md`. Cặp đôi với `framework-regime-v11.md` (shift criteria) + `workflow-daily-brief.md` (auto-flag handoff).

---

## 1. RAG HEADER — Khi nào kích hoạt

### 1.1 Trigger keywords (2 path)

**Path A — Analyst direct trigger:**
- `"regime shift"`, `"regime changed"`, `"regime alert"`, `"có phải đang chuyển regime"`.
- `"R3 sang R4?"`, `"R5 turn R1 chưa?"`, `"shift cảnh báo"`.

**Path B — Auto-flag handoff từ Daily Brief:**
- Daily Brief §5 auto-flag `⚠ REGIME SHIFT ALERT` triggered với conditions trong framework-regime-v11 §6.3.
- Analyst follow-up từ Daily Brief alert: "chạy alert đầy đủ", "full alert".

### 1.2 Critical clarification — Claude Project limitation

**Workflow này KHÔNG tự fire.** Claude Project CANNOT auto-trigger workflow based on external data streams. Alert chỉ generate khi:

1. **Analyst explicit ask** — analyst paste data + prompt "check regime shift" hoặc tương đương (Path A).
2. **Daily Brief detect shift trong input data** — khi analyst chạy Daily Brief, nếu DB-1/DB-2 chứa data breach shift criteria per framework-regime-v11, Daily Brief §5 auto-flag early warning + suggest handoff; analyst quyết định có chạy full Contract 6 alert không (Path B).
3. **Không có background daemon, không có cron, không có push notification.** Hệ thống là prompt-driven.

Hệ quả: analyst phải **proactive paste data** hoặc **run Daily Brief thường xuyên** để shift được detect. Nếu analyst skip 1 tuần không chạy Daily Brief → alert có thể miss.

### 1.3 Workflow ownership

- **Workflow này OWN Output Contract 6.** Không workflow khác được generate full Shift Alert format.
- **Anchor dependency bắt buộc:** `framework-regime-v11.md` §6 (Rule A/B/C/D transition rules).
- **Handoff source:** `workflow-daily-brief.md` §5 (early-warning flag → full alert escalation).

---

## 2. TRIGGER CONDITIONS — Shift criteria (locked per framework-regime-v11)

Full Contract 6 alert chỉ fire khi **đồng thời** 4 rule đạt (không phải OR, mà AND — tránh false alert). Nếu chỉ 1-2 rule đạt → Daily Brief early-warning flag là đủ, không full alert.

### 2.1 Rule A — Breach Threshold (multi-layer)

| Layer | Breach minimum để cân nhắc | Breach minimum để confirm full alert |
|---|---|---|
| Global (6 biến) | 2/6 | **3/6** |
| VN Macro (9 biến) | 3/9 | **4/9** |
| Cross-asset (6 biến) | 2/6 | **3/6** |

**Full alert cần đạt confirm minimum ở ≥ 2/3 layer.** Dưới ngưỡng → early warning only, không Contract 6 alert.

### 2.2 Rule B — Persistence

| Loại transition | Persistence tối thiểu trước khi fire alert |
|---|---|
| R1↔R2, R2↔R3 (gentle) | **5 phiên giao dịch** ở regime mới |
| R3↔R4, R4↔R5 (jumpy stress) | **3 phiên** |
| R4/R5 → R1/R2 (recovery — false start risk) | **10 phiên** |

Persistence đếm từ phiên đầu tiên breach. Whipsaw (breach rồi revert trong persistence window) → reset counter.

### 2.3 Rule C — Cross-Validation (≥2 asset class xác nhận)

Check pattern table trong framework-regime-v11 §6.3. Ví dụ:
- R3→R4 requires: FX breach (VND depreciation > threshold) + Rates breach (bond yield spike).
- R5→R1 requires: Macro confirm (credit re-accelerate) + Equity confirm (margin + cyclical rotation).

Chỉ 1 layer xác nhận → chưa đủ, alert downgrade thành "watching" thay vì "confirmed".

### 2.4 Rule D — Veto Conditions

**Veto triggers fire alert IMMEDIATELY, bất kể Rule A/B/C chưa đạt:**

| Veto signal | Action |
|---|---|
| NHNN can thiệp FX >$5bn/tuần | Auto-fire alert, shift về R4/R5 cân nhắc |
| Liên ngân hàng VN spike >2x base (VD 3%→>6%) | Auto-fire alert, shift về R4/R5 |
| Forced margin cascade (>20% margin accounts hit trigger) | Auto-fire alert, coi như R4/R5 stress event |
| Step-function shock (chiến tranh, cấm vận, phong tỏa, emergency policy) | Auto-fire alert, **suspend framework thông thường**, shift sang scenario riêng |
| Analyst override (analyst flag structural break) | Fire "alert pending re-calibration" |

---

## 3. ALERT OUTPUT FORMAT — Contract 6 Hard Rules

**≤ 1 page, ≤ 700 từ**. Banner-first, table-heavy, no prose paragraphs.

### 3.1 Standard alert template

```
---
## ⚠ REGIME SHIFT ALERT — [CONFIRMED / WATCHING / VETO-TRIGGERED]

**Alert timestamp:** YYYY-MM-DD HH:MM VN
**Previous regime:** Rx — [tên] (call ngày Z, held N phiên)
**New regime:** Ry — [tên]
**Shift type:** [Gentle / Stress / Recovery / Shock-driven]
**Confidence:** [Low / Medium / High] (qualitative)
**Shelf life:** [1 tuần / 2-3 tuần / 2-4 tuần] per Ry
**Invalidation trigger:** [1 dòng — biến nào reverse sẽ invalidate shift]

---

### Variables Triggered

| Layer | # Breach | Biến key | Threshold | Current |
|---|---|---|---|---|
| Global | x/6 | [G-code] | [per §5.1 framework] | [value] |
| VN Macro | y/9 | [V-code] | [per §5.2 framework] | [value] |
| Cross-asset | z/6 | [C-code] | [per §5.3 framework] | [value] |

**Rule A:** [passed / not passed — breakdown]
**Rule B persistence:** [met — N phiên / not met — waiting M more]
**Rule C cross-validation:** [met — 2+ layer confirm / not met]
**Rule D veto:** [none / triggered by X]

---

### New Regime Signature (Ry)

| Dimension | Expected behavior trong Ry |
|---|---|
| Module activation priority | [per framework §7.1 table] |
| Output framing | [per framework §7.2 — "Tìm early cycle winners" / "Grind with quality" / "Late cycle don't chase" / "Survive first" / "Prepare for turn"] |
| Valuation approach | [per framework §7.2] |
| Signpost next shift | [per framework §7.3 — biến monitor cho Ry → R?] |

---

### Immediate Implications (≤ 5 items)

- [Thesis impact]: Open thesis nào bị TRIGGERED hoặc BROKEN — list cụ thể.
- [Module re-prioritize]: Module domain nào phải re-activate (VD: R3→R4 load FX + liquidity + credit spreads, deprioritize valuation).
- [Monitoring intensify]: Biến nào cần daily tracking (not weekly) trong regime mới.
- [Workflow handoff]: Workflow nào nên chạy next (pre-mortem, thesis-tracker, cross-asset-linkage).
- [Data gap flagged]: Indicator nào missing cản trở confirm — analyst cần paste thêm.

---

### Escalation Path

1. **Nếu confirmed shift:** Analyst update regime anchor cho toàn bộ workflow sau (Daily Brief verdict-first line, Deep-dive regime anchor).
2. **Nếu watching only:** Tiếp tục monitor M phiên nữa, không update anchor.
3. **Nếu veto-triggered (Rule D):** Suspend framework, chuyển sang scenario riêng — note rõ "regime thông thường không apply".
4. **Nếu false alert (whipsaw):** Document trong post-mortem, calibrate threshold nếu lặp lại.
```

### 3.2 Hard rules

| # | Rule | Pass criteria |
|---|---|---|
| A1 | **Length** | ≤ 700 từ, ≤ 1 page |
| A2 | **Banner-first** | Dòng đầu `⚠ REGIME SHIFT ALERT — [status]` bắt buộc |
| A3 | **Variables triggered table** | Có breakdown 3-layer với # breach + key variables |
| A4 | **New regime signature** | Map sang framework-regime-v11 §7.1-§7.3 — không tự bịa framing |
| A5 | **Implications ≤ 5** | Bullet list ngắn, không prose dài |
| A6 | **Invalidation trigger** | 1 dòng cuối — biến nào reverse sẽ cancel shift |
| A7 | **Confidence qualitative** | Low/Medium/High — không pseudo-precision % |
| A8 | **No recommendation leak** | Cấm "nên short VND", "nên rotate defensive" — chỉ framing + signpost |

---

## 4. WORKED EXAMPLE — R3 → R4 Confirmed Alert

### 4.1 Setup giả dụ

Daily Brief 2026-04-26 auto-flag early warning (USD/VND breach 1.6% q/q + bond 10Y +25bps + FII outflow phiên 6/6). Analyst prompt: "chạy full alert".

### 4.2 Output (minh họa Contract 6)

---

## ⚠ REGIME SHIFT ALERT — CONFIRMED

**Alert timestamp:** 2026-04-26 09:00 VN
**Previous regime:** R3 — Đỉnh chu kỳ / Quá nhiệt (call 2026-04-11, held 11 phiên)
**New regime:** R4 — Siết chặt / Stress / Capital Flight
**Shift type:** Stress (jumpy)
**Confidence:** **Trung bình-cao** (Rule A-B-C met; 1 veto soft-trigger)
**Shelf life:** 1 tuần (R4 volatile regime per framework §2)
**Invalidation trigger:** DXY drop < 106 + Fed dovish pivot signaled trong 5 phiên → revert R3.

---

### Variables Triggered

| Layer | # Breach | Biến key | Threshold R4 | Current |
|---|---|---|---|---|
| Global | **3/6** | G1 DXY, G2 UST, G3 Fed | >108 / >5.0% / hiking | 108.4 / 5.08% / 75bps Q1 |
| VN Macro | **4/9** | V1 OMO, V2 VND, V3 Credit, V4 Real rate | withdraw mạnh / >2.5% q/q / <10% / >6% | Withdraw 8,000 bn / +2.7% q/q / 11% mom↓ / 5.8% |
| Cross-asset | **3/6** | C2 corr, C5 vol, C6 FII | +mạnh / >30% / net sell heavy | +0.68 / 32% / 7 phiên sell |

- **Rule A:** PASSED — 3/6 + 4/9 + 3/6 met confirm minimum 2/3 layer.
- **Rule B persistence:** PASSED — 4 phiên liên tiếp (>3 phiên required cho R3↔R4).
- **Rule C cross-validation:** PASSED — FX (VND breach 2.5% q/q) + Rates (bond 10Y +25bps accumulate) + Cross-asset (C2 corr flip positive).
- **Rule D veto:** Soft-trigger — NHNN intervention FX ước $4.2bn/tuần (chưa breach $5bn threshold), watching daily.

---

### New Regime Signature (R4)

| Dimension | Expected trong R4 |
|---|---|
| Module priority | `domain-fx-usd-vnd-dynamics.md` + `domain-macro-vn-liquidity-systems.md` (1st); `domain-fi-credit-spreads-vn.md` + `domain-cross-asset-flight-to-quality.md` (2nd); deprioritize `valuation-advanced.md` |
| Output framing | **"Survive first"** — capital preservation, FX hedge, liquidity focus |
| Valuation approach | **Không valuation** — chỉ balance sheet strength + covenant check |
| Signpost next shift | R4→R5: forced selling exhausted + NHNN buộc nới + NPL recognition open. R4→R1 trực tiếp: very rare. |

---

### Immediate Implications

- **Thesis impact:** Open thesis nào dùng forward P/E assumption → flag TRIGGERED re-evaluate (valuation ngừng apply trong R4 per framework §7.2). Chạy `workflow-thesis-tracker` urgent.
- **Module re-prioritize:** FX + liquidity lên first; forensic (earnings reliability) lên second; valuation + moat analysis xuống không-priority.
- **Monitoring intensify:** V1 NHNN OMO daily (không weekly), V2 USD/VND interbank daily, C6 FII flow daily, G1 DXY 4H intraday trong rolling 5 phiên tới.
- **Workflow handoff:** (i) `workflow-pre-mortem` cho top 3 holding có leverage cao; (ii) `workflow-cross-asset-linkage` cho cặp USD/VND → VN-Index quantify pressure; (iii) `workflow-thesis-tracker` refresh toàn bộ thesis.
- **Data gap flagged:** Margin balance HOSE chưa có Apr data — analyst paste khi có để confirm cascade risk layer 3.

---

### Escalation Path

1. **Confirmed — update anchor:** Regime call từ hôm nay 2026-04-26 là **R4** cho toàn bộ workflow sau. Daily Brief verdict-first line dùng R4 thay R3.

2. **Rule D watching:** Nếu NHNN intervention >$5bn/tuần trong 2 tuần tới → Rule D veto full-trigger → escalate thành "Deep R4 / potential step-function".
3. **Post-mortem deferred:** Nếu R4 revert về R3 trong 5 phiên (whipsaw) → document trong maintenance log, re-calibrate Rule B persistence 3 phiên có thể quá ngắn.

---

### 4.3 Word count check

Example ~580 từ (trong cap 700). Banner-first. 3 tables (Variables, Signature, Implications-adjacent). Rule A-B-C-D breakdown rõ. Invalidation trigger 1 dòng. No recommendation leak. Framing theo framework §7.2 ("Survive first") không bịa.

---

## 5. ALERT VARIANTS — 3 status types

### 5.1 CONFIRMED (Rule A+B+C all met)

Template §3.1 full. Analyst update regime anchor. Module re-prioritize active.

### 5.2 WATCHING (Rule A met, B or C not yet)

- Banner: `⚠ REGIME SHIFT ALERT — WATCHING (not confirmed)`.
- Confidence: Low-Medium.
- Implications: "Không update anchor. Tiếp tục monitor M phiên nữa để Rule B/C met".
- Suggested next: Re-run alert sau M phiên với data mới.

### 5.3 VETO-TRIGGERED (Rule D fires, framework suspended)

- Banner: `⚠ REGIME SHIFT ALERT — VETO-TRIGGERED (framework suspended)`.
- Shift type: Shock-driven.
- Note: "Regime thông thường không apply. Chuyển sang scenario riêng theo Focus_Brief step-function shock handling."
- Implications: Balance sheet + liquidity + capital controls priority.

---

## 6. ESCALATION PATH — Workflow integration

| Alert status | Immediate action | Workflow handoff |
|---|---|---|
| CONFIRMED | Update regime anchor. Re-prioritize modules. | `workflow-thesis-tracker` urgent + `workflow-pre-mortem` cho high-risk thesis |
| WATCHING | Keep R_old anchor, intensify monitoring | Re-run alert sau persistence window |
| VETO-TRIGGERED | Suspend framework, scenario mode | `workflow-cross-asset-linkage` với Rule D caveat + `workflow-deep-dive` defensive holdings |
| FALSE ALERT (post-hoc) | Document in maintenance log | Re-calibrate Rule B threshold nếu pattern lặp |

---

## 7. QUALITY CHECKLIST — 8-item pre-output

| # | Check | Pass |
|---|---|---|
| 1 | Banner-first line có status `[CONFIRMED / WATCHING / VETO-TRIGGERED]` | |
| 2 | Variables Triggered table có 3-layer breakdown + # breach | |
| 3 | Rule A/B/C/D status breakdown từng rule | |
| 4 | New Regime Signature map đúng framework-regime-v11 §7.1-§7.3 | |
| 5 | Implications ≤ 5 items, bullet list ngắn | |
| 6 | Invalidation trigger 1 dòng cụ thể | |
| 7 | Confidence qualitative (Low/Medium/High), không % | |
| 8 | Length ≤ 700 từ, ≤ 1 page | |

---

## 8. EDGE CASES

| Tình huống | Xử lý |
|---|---|
| User hỏi alert khi Rule A chỉ đạt 2/6 + 3/9 + 2/6 (cân nhắc minimum, chưa confirm) | Output WATCHING status, không CONFIRMED |
| 2 rule D veto cùng fire (VD: FX intervention + margin cascade) | Banner "VETO-TRIGGERED (multiple)", shift coi như R4/R5 simultaneously, escalate urgent |
| Shift từ R3 → R5 skip R4 (policy tightening → credit freeze nhanh) | Possible per framework §4, document rõ trong shift type "R3→R5 skip — rare" |
| Daily Brief auto-flag nhưng analyst không follow-up full alert | Early warning stand-alone OK, không force escalate. Analyst quyết flow. |
| Whipsaw: alert CONFIRMED hôm nay, regime revert trong 3 phiên | Document post-mortem, flag "Rule B persistence 3 phiên quá ngắn cho R3↔R4 jumpy — suggest 5 phiên calibration" |
| Step-function shock (chiến tranh Iran-US escalation) | Rule D veto fire, suspend framework, scenario mode. Alert note: "regime framework thông thường không apply" |
| Analyst push back: "tôi không nghĩ shift, đây chỉ là noise" | Không lùi tự động. Giữ alert với confidence mức đã call, thêm 1 dòng "analyst có view counter — cần data Y để invalidate" |

---

## 9. VERSION + MAINTENANCE

- **Locked Phase 2:** Trigger conditions Rule A/B/C/D per framework-regime-v11 §6, Contract 6 template §3.1, 3-status variants, escalation path.
- **Open for revise:** Persistence thresholds (3/5/10 phiên) chờ framework-regime-v11 §11 analyst calibration Sprint 0; Rule D veto thresholds (FX $5bn, liên ngân hàng 2x base) chờ empirical backtest.
- **Maintenance log:** Mọi false alert + whipsaw phải document cho Sprint retrospective → calibrate threshold nếu pattern lặp.

---

**Hết workflow-regime-shift-alert.md v1.0 (Wave 5 Lane 1).**

Reference: Focus_Brief.md §6 Workflow 5 + §9 Contract 6; framework-regime-v11.md §6 (Rule A/B/C/D) + §7 (operational mapping); workflow-daily-brief.md §5 (auto-flag handoff source).
