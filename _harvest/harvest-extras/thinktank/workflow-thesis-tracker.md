---
title: "Workflow Thesis Tracker — OPVIA Sigma Signpost Monitoring, Contract 4 Owner, Diagnostic Status Classification"
module_type: "workflow"
file_name: "workflow-thesis-tracker.md"
purpose: "Own Output Contract 4 (Thesis Tracker). Khi analyst đã có thesis mở + signpost đã định nghĩa, module này check trạng thái hiện tại vs threshold, phân loại ON-TRACK / WATCHING / TRIGGERED / BROKEN, flag red alert nếu triggered/broken, đề xuất re-evaluation. Diagnostic tool — không soft, không recommend, không dự đoán giá."
primary_triggers:
  - "thesis tracker"
  - "track thesis"
  - "signpost check"
  - "thesis còn valid không"
  - "regime check thesis"
  - "tracker update"
  - "signpost update"
  - "thesis status"
  - "check thesis"
when_to_use:
  - "Analyst đã có thesis opened + signpost variables được định nghĩa lúc opening (từ pre-mortem §6 hoặc deep-dive §14)."
  - "Periodic check: daily brief Section 4 reference tracker; weekly full update; monthly comprehensive review."
  - "Event-driven check: regime shift detected / data release impact signpost / earnings release / policy announcement."
  - "Pre-position check: analyst muốn refresh status trước khi add/reduce position."
when_not_to_use:
  - "Chưa có thesis — dùng workflow-deep-dive.md trước để build thesis."
  - "Chưa có signpost explicit — dùng workflow-pre-mortem.md §6 để define decisive observable trước."
  - "Muốn stress-test thesis gốc — dùng workflow-pre-mortem.md."
  - "Muốn linkage cross-asset thuần — dùng workflow-cross-asset-linkage.md."
related_modules:
  - "core-voice-and-safety.md"
  - "core-evidence-ladder.md"
  - "core-output-contracts.md"
  - "workflow-pre-mortem.md"
  - "workflow-deep-dive.md"
  - "workflow-daily-brief.md"
  - "workflow-regime-shift-alert.md"
  - "framework-regime-v11.md"
  - "domain-macro-vn-liquidity.md"
  - "domain-cross-asset-linkage.md"
  - "reference-vn-data-sources.md"
authoritative_citations:
  - "OPVIA internal thesis-tracking discipline + decision journal."
  - "Tetlock, P. Superforecasting — calibration and update discipline."
  - "Mauboussin, M. Expectations Investing — expectations update."
  - "Kahneman, D. Thinking, Fast and Slow — pre-commitment + feedback loop."
output_owner: "OWNS Output Contract 4 (Thesis Tracker). Format: table-heavy (Variable | Threshold | Current | Status | Last Update) + alert section + action implications. Diagnostic tone, verdict-first on status change, no recommendation."
status: "v1.0 — Phase 3 Wave 6 Lane 1. Locked với 4-status taxonomy (ON-TRACK / WATCHING / TRIGGERED / BROKEN), 5-step protocol, tracker table schema. Threshold calibration chờ analyst edit per thesis (không phải framework-wide)."
---

# Workflow Thesis Tracker — Signpost Monitoring OPVIA Sigma

Purpose: Thesis mở + signpost đã định nghĩa → module này kiểm tra **trạng thái hiện tại vs threshold**, phân loại status, flag nếu triggered/broken, đề xuất action implication (re-evaluate, NOT khuyến nghị). Output Contract 4: table-only, diagnostic tone. Tracker là **bộ đếm đồng hồ**, không phải re-analysis — nếu analyst muốn phản biện lại thesis, handoff sang pre-mortem.

Trigger: thesis tracker, track thesis, signpost check, thesis còn valid không, tracker update, thesis status, check thesis, regime check thesis.

---

## 1. RAG HEADER — Khi nào kích hoạt

### 1.1 Activation matrix

| Prompt analyst | Workflow |
|---|---|
| "Tracker update", "signpost check HPG", "thesis GMD còn valid không", "check thesis X" | **thesis-tracker** (this) |
| "Pre-mortem X", "bear case", "phản biện" | `workflow-pre-mortem.md` |
| "Phân tích sâu X" | `workflow-deep-dive.md` |
| "Brief đầu ngày" | `workflow-daily-brief.md` (Section 4 có mini tracker) |
| "Regime đã đổi chưa" | `workflow-regime-shift-alert.md` |
| "Có nên giữ / bán / thêm X không" | **REJECT** (khuyến nghị — Safety Rule 2) → redirect "Tôi check status signpost, analyst quyết định position" |

### 1.2 Ownership

- **OWN Output Contract 4** (Thesis Tracker). Daily brief Section 4 có **compressed reference** tới tracker — chỉ trạng thái summary, không full table. Full tracker render qua workflow này.
- **Domain dependency:** tùy thesis — equity VN, macro-vn, FX, commodity. Tracker không load deep framework, chỉ pull **data latest** từ domain source (`reference-vn-data-sources.md`).
- **Framework anchor:** `framework-regime-v11.md` (regime tại thời điểm open thesis vs hiện tại — nếu shift, impact status).

### 1.3 Composition rule

Tracker **không re-build thesis**. Thesis + signpost phải được định nghĩa trước khi tracker chạy:
- Signpost từ `workflow-pre-mortem.md` §6 (3 decisive observable 30/60/90), HOẶC
- Signpost từ `workflow-deep-dive.md` §1 (thesis-breakers 30/60/90), HOẶC
- Signpost analyst paste manual (format mục 2.2 dưới).

Nếu không có signpost → reject, hỏi analyst: "Thesis này có signpost gì khi mở? Nếu chưa define → chạy pre-mortem trước." Không tự bịa signpost.

Tracker **không dự đoán**. Không extrapolate signpost direction ("variable đang trend X → sắp breach"). Chỉ check **current vs threshold**. Forward-looking logic thuộc pre-mortem hoặc deep-dive.

---

## 2. INPUT PROTOCOL

### 2.1 Required input

| Input | Bắt buộc | Default |
|---|---|---|
| **Thesis 1 câu** (refresh restate) | YES | Hỏi lại nếu chưa có context |
| **Signpost list** (3-10 variables với threshold) | YES | Reject nếu chưa define |
| **Ngày open thesis** | YES | Từ audit trail pre-mortem/deep-dive |
| **Regime lúc open** | YES | Từ audit trail; nếu miss → flag `[REGIME CONTEXT MISSING]` |
| **Current data per signpost** | YES | Analyst paste manual hoặc tôi pull qua daily brief latest |
| **Last tracker update date** | NO | Nếu có → diff vs lần trước; nếu first-run → baseline |

### 2.2 Signpost format chuẩn (analyst paste khi opening thesis hoặc import từ pre-mortem §6)

```
Thesis: [1 câu]
Opened: YYYY-MM-DD | Regime lúc open: [R1-R5]
Expected outcome: [metric + timeframe]

Signposts:
| # | Variable | Data source | Threshold ON-TRACK | Threshold TRIGGERED | Threshold BROKEN | Check frequency |
|---|---|---|---|---|---|---|
| 1 | [var 1] | [source] | [range] | [single threshold] | [single threshold] | [daily/weekly/monthly] |
| 2 | ...
```

**Example (from pre-mortem HPG §6):**

```
Thesis: HPG hưởng lợi từ China stimulus 2026 → biên gộp lên 17% Q4 2026 → fair 32k
Opened: 2026-04-19 | Regime: R2 Steady Growth
Expected: biên gộp 17% Q4 2026

Signposts:
| # | Variable | Source | ON-TRACK | TRIGGERED | BROKEN | Freq |
| 1 | HRC-iron ore spread | Bloomberg/SGX | > 80 USD/tấn 3 tuần liên tiếp | 60-80 USD/tấn range | < 60 USD/tấn 3 tuần | weekly |
| 2 | HPG DQ2 utilization | HPG earnings call | ≥ 60% Q2 2026 | 45-60% Q2 | ≤ 45% Q2 + Q3-Q4 delay language | quarterly |
| 3 | VN construction steel sales YoY | VSA monthly | ≥ +8% Aug-Sep | -3% to +8% | < -3% Aug-Sep | monthly |
| 4 | Regime still R2 | framework-regime-v11 | R2 confirmed | shift probability > medium | shifted to R3 or R4 | daily brief reference |
| 5 | USD/VND interbank | SBV | < 25,500 | 25,500-25,800 | > 25,800 sustained 5 phiên | daily |
```

**Rule cho signpost:**
- Minimum 3 signpost per thesis (nếu < 3 → quá ít axis, tracker không meaningful → reject, ask analyst add).
- Maximum 10 signpost (nếu > 10 → quá phân tán, force analyst prioritize top 5-7).
- Mỗi signpost phải có **threshold explicit**, không "cao/thấp". Nếu analyst cung cấp threshold mơ hồ → reject, ask cụ thể.
- Signpost phải **independent** (không phải output của chính thesis — tránh tautology giống Step 6 pre-mortem).

---

## 3. EXECUTION PROTOCOL — 5 Steps

### Step 1 — LOAD THESIS + SIGNPOSTS

- Load thesis từ context (current conversation) hoặc từ user paste (format §2.2).
- Verify 3-10 signpost với threshold explicit.
- Verify regime context (lúc open + hiện tại).
- Flag missing input → reject với request cụ thể. Không proceed với partial data.

**Red flag tại Step 1:**
- `[AUDIT TRAIL MISSING]` — nếu không tìm thấy pre-mortem / deep-dive gốc → chỉ có thesis 1 câu + signpost, không có reasoning foundation. Tracker vẫn chạy nhưng flag "limited context".
- `[REGIME CONTEXT MISSING]` — nếu không biết regime lúc open → impact variable 4 dưới (regime-tied signpost).

### Step 2 — LIST SIGNPOST VARIABLES + PULL CURRENT

- Render signpost list từ Step 1.
- Pull current value per signpost từ:
  - Realtime data: analyst paste manual (DB-1 daily brief source).
  - Weekly data: analyst paste hoặc broker PDF (DB-2).
  - Monthly data: VSA, GSO, SBV, NHNN latest release (flag `[DỮ LIỆU THIẾU]` nếu lag > 1 tháng).
  - Quarterly data: earnings filing, BoP quarterly (flag nếu chưa release).
- Nếu > 50% signpost missing current data → tracker run partial + flag `[TRACKER PARTIAL — data gap mạnh]`.

### Step 3 — CHECK CURRENT VS THRESHOLD + CLASSIFY STATUS

4-status taxonomy (hard rule):

| Status | Condition | Color code | Action implication |
|---|---|---|---|
| **ON-TRACK** | Current nằm trong ON-TRACK range của signpost (thesis-supporting) | Green | Không action, continue monitoring |
| **WATCHING** | Current nằm trong neutral zone (giữa ON-TRACK và TRIGGERED thresholds) | Yellow | Tăng frequency monitoring; alert nếu direction worsening |
| **TRIGGERED** | Current đã breach TRIGGERED threshold (but chưa breach BROKEN) | Orange | Flag red; đề xuất re-evaluation; handoff pre-mortem nếu ≥ 2 signpost triggered |
| **BROKEN** | Current đã breach BROKEN threshold | Red | Thesis invalidated per original logic; force re-evaluation; handoff pre-mortem mandatory |

**Classification rule per signpost:**

```
IF current ≤ threshold_broken (hoặc ≥ threshold_broken tùy direction):
    status = BROKEN
ELIF current ≤ threshold_triggered (hoặc ≥ tùy direction):
    status = TRIGGERED
ELIF current nằm trong ON-TRACK range:
    status = ON-TRACK
ELSE:
    status = WATCHING  # neutral zone
```

**Direction rule:** Một số signpost "bad when higher" (USD/VND cao = pressure), một số "bad when lower" (biên gộp thấp = pressure). Tracker check direction explicit, không assume. Nếu analyst cung cấp threshold không rõ direction → reject, ask clarify.

### Step 4 — AGGREGATE THESIS STATUS + RED FLAG

Sau khi classify per-signpost, aggregate thesis-level status:

| Thesis-level status | Condition aggregate |
|---|---|
| **ON-TRACK (thesis)** | ≥ 80% signpost ON-TRACK + 0 TRIGGERED + 0 BROKEN |
| **WATCHING (thesis)** | ≥ 1 signpost WATCHING (neutral) + 0 TRIGGERED + 0 BROKEN |
| **TRIGGERED (thesis)** | ≥ 1 signpost TRIGGERED + 0 BROKEN. Subsidiary rule: nếu ≥ 2 signpost TRIGGERED → mandatory handoff pre-mortem. |
| **BROKEN (thesis)** | ≥ 1 signpost BROKEN (single BROKEN is enough — BROKEN là thesis-killer) |

**Red flag section (render nếu thesis status = TRIGGERED hoặc BROKEN):**

```
### ⚠ RED FLAG — Thesis {status}
Triggered by: [signpost(s) triggered/broken + values]
Days from open: [N days]
Regime context: [regime stability since open — còn R2 hay đã shift?]
Action implication (NOT recommendation):
- Re-evaluate thesis qua workflow-pre-mortem.md (Contract 5) để check counter-thesis strength
- Verify signpost threshold calibration (threshold có quá tight hoặc quá loose không?)
- Check related thesis (nếu analyst có thesis khác dùng cùng signpost) — có domino risk không
```

**Rule cứng:** Red flag KHÔNG chứa "bán", "giảm position", "exit". Chỉ action implication analytical.

### Step 5 — UPDATE REGIME CLASSIFICATION (nếu thay đổi)

- Check regime hiện tại vs regime lúc open thesis (framework-regime-v11.md).
- Nếu regime vẫn same → 1 dòng confirmation.
- Nếu regime shifted → append section "REGIME CHANGE IMPACT":

```
### Regime change since open
Open regime: [Rx — ngày]
Current regime: [Ry — ngày]
Shift confirmed by: [variables per framework-regime-v11.md §6.3 Rule C cross-validation]
Impact on thesis: [thesis logic regime-specific không? Module activation priority thay đổi không per §7.1?]
```

**Rule:** Regime shift trong life của thesis là **automatic signpost #∞** — dù analyst không explicitly list regime là signpost. Nếu shift R2 → R3 → R4 trong thesis period → auto flag TRIGGERED cho thesis (regime-dependent thesis không stable qua shift).

---

## 4. OUTPUT TEMPLATE — Contract 4

Table-heavy. Verdict-first (1-dòng status thesis aggregate). Length 500-1200 từ tiếng Việt (gọn hơn pre-mortem, ngắn hơn deep-dive).

### Header

```
# Thesis Tracker — {Thesis subject} — {YYYY-MM-DD} (Update #{N})
Analyst: OPVIA Sigma | Workflow: workflow-thesis-tracker.md
Thesis owner: OPVIA analyst | Opened: {YYYY-MM-DD} | Days held: {N days}
Regime at open: {Rx} | Regime now: {Ry} | Regime stability: {same / shifted}
Last update: {YYYY-MM-DD} (delta since last: {N days})
```

### §1. THESIS STATUS VERDICT (1-dòng)

```
**Status:** {ON-TRACK / WATCHING / TRIGGERED / BROKEN} (as of {YYYY-MM-DD}).
```

Nếu TRIGGERED hoặc BROKEN → bold + 1 dòng "Triggered by: {signpost + value}". Không soft.

### §2. THESIS RESTATE (≤ 50 từ, compressed)

1 câu thesis gốc + 1 câu expected outcome. Nếu deviation từ thesis gốc trước đó → flag `[THESIS REVISED]`.

### §3. SIGNPOST TRACKER TABLE (core output)

Bảng chính theo Output Contract 4 schema:

| # | Variable | Threshold (ON / TRG / BRK) | Current | Status | Last Update | Δ vs last update |
|---|---|---|---|---|---|---|
| 1 | [var 1] | ON > 80 / TRG 60-80 / BRK < 60 | 72 USD/tấn | **WATCHING** | 2026-04-19 | -5 USD/tấn |
| 2 | ... |

**Format rule:**
- Cột "Threshold" compact format `ON {range} / TRG {value} / BRK {value}`.
- Cột "Current" hiển thị với unit + `[DỮ LIỆU THIẾU]` nếu missing.
- Cột "Status" bold, color code text (green/yellow/orange/red) qualitative trong ngoặc nếu render plain text.
- Cột "Δ vs last update" show direction + magnitude. Nếu first-run → "baseline".

### §4. REGIME CHECK (1-2 câu)

- Nếu regime same: "Regime R{x} tiếp tục (days held: N since open). Shelf life: {theo framework v1.1 §phụ lục}."
- Nếu regime shifted: render full section §3 Step 5 template.

### §5. RED FLAG ALERT (conditional — chỉ nếu TRIGGERED hoặc BROKEN)

Theo template §3 Step 4. Nếu thesis ON-TRACK hoặc WATCHING → skip section này, render 1 dòng "No red flag."

### §6. ACTION IMPLICATIONS (NOT recommendation)

3-4 bullet action implication analytical. Forbidden: "bán", "mua thêm", "exit", "khuyến nghị". Allowed:
- "Re-evaluate qua pre-mortem"
- "Verify threshold calibration"
- "Increase monitoring frequency signpost X từ weekly → daily"
- "Check related thesis Y có domino không"
- "Wait for data release Z trước khi next update"

### §7. NEXT UPDATE SCHEDULE

- Next scheduled update: {YYYY-MM-DD based on check frequency highest signpost}
- Event-driven triggers: {data release / earnings / policy event sẽ trigger ad-hoc update}
- If thesis BROKEN: "Tracker freeze — thesis đã invalidated, analyst quyết định close thesis hoặc re-open với revised version"

### §8. HANDOFF

1 dòng: "Handoff → {none / pre-mortem nếu TRIGGERED ≥ 2 / regime-shift-alert nếu regime changed / deep-dive nếu analyst muốn revise thesis foundation}"

---

## 5. ANTI-PATTERNS — Reject ở quality gate

| # | Anti-pattern | Fail example | Fix |
|---|---|---|---|
| 1 | **Recommendation leak** | "Analyst nên giảm position HPG" | "Re-evaluate qua pre-mortem" |
| 2 | **Soft status classification** | "Thesis vẫn OK dù signpost trigger" | Apply rule §3 Step 4 strict — TRIGGERED là TRIGGERED |
| 3 | **Threshold mơ hồ** | Current: "cao" | Current: "72 USD/tấn" — số cụ thể |
| 4 | **Forward extrapolation** | "Signpost đang trend xấu, sắp breach" | Chỉ check current vs threshold, không predict |
| 5 | **Missing regime check** | §4 skip | §4 mandatory — regime là signpost ngầm |
| 6 | **Signpost < 3** | Tracker 1-2 signpost | Reject, ask analyst add signpost (min 3) |
| 7 | **Tautological signpost** | Signpost = "HPG price" cho thesis HPG | Reject, ask upstream variable (HRC spread, DQ2 utilization) |
| 8 | **Data gap hidden** | Current: best-guess không flag | `[DỮ LIỆU THIẾU]` + impact rõ |
| 9 | **Vietlish** | "Check lại status thesis" | "Rà lại trạng thái thesis" |
| 10 | **Verdict buried** | Status thesis ở cuối memo | §1 Verdict-first, 1-dòng ngay sau header |

---

## 6. QUALITY CHECKLIST — 8 items pre-output

| # | Check | Pass criteria |
|---|---|---|
| 1 | **Verdict-first line** | §1 1-dòng status thesis ngay sau header |
| 2 | **8 sections đầy đủ** | §1-§8 (§5 conditional) |
| 3 | **Tracker table ≥ 3 row** | §3 table có ≥ 3 signpost với threshold + current + status |
| 4 | **Status classification strict** | Áp dụng rule §3 Step 3-4 không soft |
| 5 | **Regime check** | §4 render, nếu shift → full template |
| 6 | **Red flag conditional** | §5 render khi TRIGGERED/BROKEN, skip khi ON-TRACK/WATCHING |
| 7 | **No recommendation leak** | Scan "bán/mua/exit/khuyến nghị" — zero hit |
| 8 | **Data gap flagged** | Missing data → `[DỮ LIỆU THIẾU]` explicit, không hidden |

---

## 7. HANDOFF CONDITIONS

| Tình huống | Handoff |
|---|---|
| Thesis status = TRIGGERED với ≥ 2 signpost | `workflow-pre-mortem.md` mandatory — re-run bear case |
| Thesis status = BROKEN | `workflow-pre-mortem.md` + analyst quyết định close thesis hoặc re-open revised |
| Regime shifted since open | `workflow-regime-shift-alert.md` (Contract 6) |
| Signpost threshold cần calibrate lại (quá tight/loose) | Analyst revise signpost manual → tracker re-run với threshold mới, flag `[THRESHOLD REVISED]` |
| Multiple thesis cùng hit BROKEN | `workflow-pre-mortem.md` cross-thesis (emerging theme analysis) |
| ON-TRACK bình thường | No handoff. Next update scheduled. |

---

## 8. WORKED EXAMPLE — Tracker cho HPG / China stimulus thesis (5 signpost, 1 triggered + 1 broken)

Scenario: Thesis opened 2026-04-19 (cùng ngày pre-mortem memo). Tracker update 60 ngày sau (2026-06-18). Trong window này, đã có 2 earnings release, 1 regime check, FII outflow sustained, DXY breach 108.

### Header

```
# Thesis Tracker — HPG / China stimulus 2026 — 2026-06-18 (Update #2)
Analyst: OPVIA Sigma | Workflow: workflow-thesis-tracker.md
Thesis owner: OPVIA analyst | Opened: 2026-04-19 | Days held: 60
Regime at open: R2 Steady Growth | Regime now: R3 Late Cycle | Regime stability: **SHIFTED**
Last update: 2026-05-17 (Update #1, delta: 32 days)
```

### §1. Thesis Status Verdict

**Status: BROKEN (as of 2026-06-18).** Triggered by: (a) signpost #4 Regime R2 → R3 shift confirmed 2026-05-28; (b) signpost #3 VN construction steel sales YoY -5.2% breach BROKEN threshold.

### §2. Thesis Restate

Thesis gốc: HPG hưởng lợi từ China stimulus 2026 → biên gộp 17% Q4 2026 → fair value 32k VND / 12 tháng. Expected outcome: biên gộp 17% Q4 2026.

### §3. Signpost Tracker Table

| # | Variable | Threshold (ON / TRG / BRK) | Current | Status | Last Update | Δ vs Update #1 |
|---|---|---|---|---|---|---|
| 1 | HRC-iron ore spread (global) | ON > 80 / TRG 60-80 / BRK < 60 (3 tuần) | 68 USD/tấn | **WATCHING** (neutral zone) | 2026-06-18 (weekly avg) | -4 USD/tấn (từ 72) |
| 2 | HPG DQ2 utilization (mgmt disclosure) | ON ≥ 60% Q2 / TRG 45-60% / BRK ≤ 45% + delay | 48% Q2 2026 (earnings 2026-05-25) | **TRIGGERED** | 2026-05-25 | vs baseline 40% (Update #1 placeholder) |
| 3 | VN construction steel sales YoY (VSA monthly) | ON ≥ +8% Aug-Sep / TRG -3% to +8% / BRK < -3% | -5.2% (May 2026 print, 2026-06-12) | **BROKEN** | 2026-06-12 | -7pp vs Update #1 (+1.8%) |
| 4 | Regime still R2 (framework v1.1) | ON R2 confirmed / TRG shift probability > medium / BRK shifted R3/R4 | R3 confirmed 2026-05-28 | **BROKEN** | 2026-05-28 | shift event |
| 5 | USD/VND interbank (SBV) | ON < 25,500 / TRG 25,500-25,800 / BRK > 25,800 sustained 5 phiên | 25,680 (2026-06-18) | **TRIGGERED** | 2026-06-18 | +260 bps vs Update #1 (25,420) |

### §4. Regime Check — SHIFTED

Regime open: R2 Steady Growth (call 2026-04-11).
Regime now: R3 Late Cycle / Overheating (call 2026-05-28, shelf life 1-2 tuần).
Shift confirmed by: DXY breach 108 (2026-05-15), UST 10Y 4.82%, NHNN signal siết room BĐS (2026-05-22), FII outflow phiên 14/30. Rule C cross-validation: FX (VND mất giá 2.1% q/q) + Macro (NHNN signal) + Cross-asset (bond-equity correlation chuyển dương) → 3-layer confirm.
Impact on thesis: Thesis HPG build trên giả định R2. Per framework-regime-v11.md §7.1, R3 module priority shift sang forensic + monetary policy (KHÔNG cyclical valuation). HPG (cyclical, P/E 8x forward) vulnerable tới de-rating multiple trong R3. Thesis logic regime-specific → signpost #4 BROKEN = thesis foundation collapse.

### §5. Red Flag Alert

**⚠ RED FLAG — Thesis BROKEN**
- Triggered by: Signpost #3 (VN steel sales YoY -5.2%) + Signpost #4 (Regime shift R2 → R3 confirmed). 1 BROKEN rule thỏa (BROKEN là thesis-killer single-signpost), 2 BROKEN càng mandatory.
- Days from open: 60 (thesis life chỉ 2 tháng — short thesis, cần audit tại sao miss early signal).
- Regime context: Shift R2 → R3 đã được dự báo trong pre-mortem §3.7 (assumption A7 attack — regime R2 persist giả định). Pre-mortem đã warn; tracker confirm execution.
- Action implication (NOT recommendation):
  - Re-evaluate thesis qua `workflow-pre-mortem.md` — run counter-thesis bây giờ là base case, thesis gốc là bear case đảo ngược.
  - Không tự "bán" — analyst quyết position. Tracker chỉ flag thesis foundation đã collapse.
  - Audit: tại sao pre-mortem §3.7 warn nhưng analyst vẫn hold? Learning cho decision journal.
  - Related thesis check: nếu analyst có thesis HSG/TVN (cùng cyclical steel) → khả năng domino BROKEN cao — re-check tracker cho thesis đó.

### §6. Action Implications

1. **Mandatory handoff `workflow-pre-mortem.md`** — re-run pre-mortem với regime R3 assumption. Counter-thesis từ pre-mortem #1 (§4) nay cần upgrade thành main case; thesis gốc cần downgrade hoặc close.
2. **Signpost threshold audit** — Signpost #1 (HRC spread) hiện WATCHING (68 USD/tấn neutral zone 60-80). Nếu HRC break < 60 trong 3 tuần tới → TRIGGERED. Raise check frequency từ weekly → every 3 days.
3. **Regime-tied thesis sweep** — Check tất cả thesis khác analyst đang hold: nếu thesis nào có signpost "R2 persist" assumption → apply domino check, potentially BROKEN.
4. **Freeze tracker, analyst quyết định next** — Tracker sẽ không tiếp tục update thesis này cho tới khi analyst: (a) close thesis formally, hoặc (b) re-open với revised thesis + signpost mới. Không drift passive.

### §7. Next Update Schedule

- Thesis status BROKEN → tracker freeze cho thesis gốc.
- Next tracker activity: analyst confirm action qua pre-mortem re-run.
- Nếu analyst re-open với thesis v2 (ví dụ "HPG value play post-regime shift") → tracker khởi động baseline mới với signpost revised.

### §8. Handoff

Handoff → `workflow-pre-mortem.md` (mandatory, thesis BROKEN) + `workflow-regime-shift-alert.md` (Contract 6 cho regime shift R2 → R3 impact).

---

### 8.2 Alternative scenario — cùng thesis, update sớm hơn (Update #1, 2026-05-17, 1 triggered mà chưa broken)

Để minh họa thesis ở status TRIGGERED (không BROKEN), render compressed:

**Status:** TRIGGERED (as of 2026-05-17).

| # | Variable | Current | Status |
|---|---|---|---|
| 1 | HRC spread | 72 USD/tấn | WATCHING |
| 2 | DQ2 util | 40% (management guide tại Q1 earnings 2026-04-28) | WATCHING (chưa reach Q2 report) |
| 3 | VN steel sales YoY | +1.8% (Apr 2026 print) | WATCHING |
| 4 | Regime R2 | R2 confirmed, shelf còn 1 tuần | WATCHING (shift probability trung bình-cao) |
| 5 | USD/VND | 25,620 | **TRIGGERED** (breach 25,500-25,800 range) |

**Red flag (TRIGGERED):** Signpost #5 USD/VND breach 25,500. Days from open: 28. Regime: R2 còn, shelf expiring 1 tuần — shift probability trung bình-cao. Action: increase frequency signpost #4 (regime) từ weekly reference → daily; verify pre-mortem §3.7 assumption A7 (regime R2 persist) có breach chưa — nếu shift confirm → thesis BROKEN (single signpost #4 đủ). Handoff: `workflow-regime-shift-alert.md` nếu shift confirm + `workflow-pre-mortem.md` nếu ≥ 2 signpost triggered.

---

## 9. EDGE CASES

| Tình huống | Xử lý |
|---|---|
| Analyst không cung cấp current data cho > 50% signpost | Render tracker partial + flag `[TRACKER PARTIAL — data gap mạnh]`. Reject classification for missing signpost (render "TBD"). |
| Signpost threshold analyst viết mơ hồ ("cao / thấp") | Reject. Ask analyst clarify số cụ thể trước khi tracker chạy. |
| Thesis status = BROKEN nhưng analyst muốn override ("tôi vẫn hold") | Tracker không lùi — render BROKEN theo rule. Flag `[ANALYST OVERRIDE NOTED]`. Analyst position là việc của analyst; tracker chỉ flag thesis foundation. |
| Signpost #N status conflict (analyst paste current khác với broker report) | Ưu tiên analyst paste (source curated). Flag `[NGUỒN MÂU THUẪN]` + note broker disagree. |
| Thesis không có pre-mortem backing (analyst skip pre-mortem) | Flag `[AUDIT TRAIL MISSING]`. Tracker vẫn chạy nhưng action implication mạnh hơn: "Recommend chạy pre-mortem trước khi add position". |
| Multiple thesis dùng cùng 1 signpost (VD: 3 thesis đều watch USD/VND) | Tracker chạy per thesis, nhưng section §6 action có note "cross-thesis impact detected — domino risk". |
| Regime shift nhưng signpost khác all ON-TRACK | Per rule §3 Step 5, regime shift auto-triggers signpost #∞ regime-level. Nếu thesis logic regime-dependent → BROKEN. Nếu regime-agnostic (rare) → TRIGGERED only. |
| Signpost breach threshold nhưng recovery trong window (VD: 1-2 ngày spike rồi về) | Rule: threshold phải breach SUSTAINED theo spec gốc (thường 3-5 ngày). Nếu không sustained → WATCHING thay vì TRIGGERED. |

---

## 10. VERSION + MAINTENANCE

- **Phase 3 locked:** 5-step protocol, 4-status taxonomy, 8-item quality checklist, tracker table schema, 10 anti-pattern scan.
- **Open for revise Sprint 1-2:** Aggregate rule (80% ON-TRACK threshold có thể strict quá — thesis với 10 signpost, 2 WATCHING sẽ fall vào WATCHING aggregate — calibrate sau). Persistence rule cho TRIGGERED (hiện không có — có thể thêm "TRIGGERED sustained 5 phiên mới count", tương tự regime framework Rule B).
- **Phase 4 consideration:** Auto-tracker daemon (chạy ngầm với DB-1 paste mỗi sáng, update tất cả active thesis); portfolio-level aggregation (nếu analyst có 5-10 thesis, view consolidated sức khỏe); signpost learning (empirical: signpost nào historically predictive nhất cho OPVIA thesis — recalibrate threshold dựa on hit rate).

---

**Hết workflow-thesis-tracker.md v1.0 (Wave 6 Lane 1 — Contract 4 owner).**

Tác giả: Wave 6 Lane 1 (Native Opus Executor).
Reference: Focus_Brief.md §6 Workflow 5 + §9 Contract 4; workflow-pre-mortem.md §6 (signpost import source); workflow-deep-dive.md §1 (thesis-breakers 30/60/90 import source); framework-regime-v11.md §6 transition rules + §7.1 module activation; core-meta-cognition.md (decision journal foundation); Tetlock Superforecasting (calibration update discipline).
