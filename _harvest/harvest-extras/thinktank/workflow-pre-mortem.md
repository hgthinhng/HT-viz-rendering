---
title: "Workflow Pre-Mortem — OPVIA Sigma Adversarial Dialogue Protocol, Contract 5 Owner, 6-Step Bear-Case Stress Test"
module_type: "workflow"
file_name: "workflow-pre-mortem.md"
purpose: "Own Output Contract 5 (Pre-mortem Memo) for OPVIA Sigma. Khi analyst có thesis đang mở hoặc đang cân nhắc, module này chạy 6-step adversarial dialogue: restate → identify assumptions → attack → construct counter-thesis → common ground → decisive observable. Mục tiêu: làm analyst uncomfortable ở đúng chỗ họ lười phản biện. Không soft, không dung hòa, không recommend mua/bán."
primary_triggers:
  - "pre-mortem"
  - "phản biện thesis"
  - "yết kháng"
  - "yết kháng thesis"
  - "stress test thesis"
  - "bear case"
  - "bear case mạnh nhất"
  - "counter-thesis"
  - "adversarial"
  - "steelman phản biện"
  - "thesis có thể sai chỗ nào"
when_to_use:
  - "User có thesis explicit (tự viết hoặc import từ deep-dive memo) + muốn kiểm tra điểm gãy trước khi position hoặc trước khi commit thêm."
  - "User nói 'tôi đang nghĩ X, phản biện cho tôi' — thesis đã formed nhưng chưa stress-tested."
  - "Sau deep-dive memo có §14 Scenario hoặc §16 Meta-cognition gợi ý bear case mạnh — handoff sang pre-mortem để format bear case đầy đủ."
  - "Regime shift vừa triggered → re-evaluate các thesis đang mở qua adversarial lens (handoff từ workflow-regime-shift-alert)."
  - "Consensus thị trường quá đồng thuận với thesis của analyst → trigger defensive pre-mortem."
when_not_to_use:
  - "Không dùng khi chưa có thesis rõ — thay bằng workflow-deep-dive.md để build thesis trước."
  - "Không dùng làm substitute cho forensic check — forensic thuộc domain-equity-vn-forensic-accounting.md."
  - "Không dùng khi user chỉ hỏi 'thesis còn valid không' mà không muốn full adversarial — dùng workflow-thesis-tracker.md."
  - "Không dùng khi user hỏi linkage cross-asset thuần — dùng workflow-cross-asset-linkage.md."
related_modules:
  - "core-research-protocol.md"
  - "core-voice-and-safety.md"
  - "core-meta-cognition.md"
  - "core-evidence-ladder.md"
  - "core-output-contracts.md"
  - "workflow-deep-dive.md"
  - "workflow-thesis-tracker.md"
  - "workflow-regime-shift-alert.md"
  - "framework-regime-v11.md"
  - "framework-dickinson-mauboussin-lifecycle.md"
  - "framework-thakor-yu-2024.md"
  - "framework-geanakoplos-leverage-cycle.md"
  - "framework-minsky-financial-instability.md"
  - "domain-equity-vn-forensic-accounting.md"
  - "domain-macro-vn-liquidity.md"
  - "domain-cross-asset-linkage.md"
authoritative_citations:
  - "Klein, G. (2007). Performing a Project Premortem. Harvard Business Review."
  - "Kahneman, D. Thinking, Fast and Slow — premortem technique."
  - "Tetlock, P. Superforecasting — devil's advocate discipline."
  - "Mauboussin, M. Expectations Investing — market-implied assumptions."
  - "OPVIA internal Research Partner Protocol (file 100) + core-meta-cognition.md 6-question foundation."
output_owner: "OWNS Output Contract 5 (Pre-mortem Memo, 1-3 pages). Adversarial memo — tone không soft, không đi tới khuyến nghị. Memo kết thúc bằng decisive observable + thesis-breaker condition."
status: "v1.0 — Phase 3 Wave 6 Lane 1. Locked với 6-step protocol, 10-assumption taxonomy, 8-item quality checklist. Calibration thresholds chờ analyst edit sau Sprint 0 session #1 theo framework-regime-v11.md §11."
---

# Workflow Pre-Mortem — Adversarial Dialogue cho Thesis OPVIA Sigma

Purpose: Analyst có thesis đang mở → module này chạy **6-step adversarial memo** để tìm điểm gãy trước khi position. Không phải forensic, không phải thesis-tracker, không phải scenario analysis thông thường. Pre-mortem là **giả định thesis đã thất bại**, rồi reverse-engineer nguyên nhân. Output Contract 5: 1-3 trang, adversarial, kết thúc bằng decisive observable 30/60/90 ngày.

Trigger: pre-mortem, phản biện thesis, yết kháng, bear case mạnh nhất, steelman phản biện, counter-thesis, stress test thesis, thesis có thể sai chỗ nào, thesis của tôi là X — phản biện đi.

---

## 1. RAG HEADER — Khi nào kích hoạt

### 1.1 Activation matrix

| Prompt analyst | Workflow |
|---|---|
| "Pre-mortem thesis HPG", "phản biện thesis X", "yết kháng", "bear case mạnh nhất", "stress test X" | **pre-mortem** (this) |
| "Phân tích sâu X" (chưa có thesis explicit) | `workflow-deep-dive.md` trước → pre-mortem sau |
| "Thesis X còn valid không", "signpost check" | `workflow-thesis-tracker.md` |
| "Ảnh hưởng X tới Y" (không phải thesis) | `workflow-cross-asset-linkage.md` |
| "Brief đầu ngày" | `workflow-daily-brief.md` |
| "Regime đã đổi chưa" | `workflow-regime-shift-alert.md` |
| "Có nên mua X không" | **REJECT** (khuyến nghị — Safety Policy Rule 2) → redirect sang pre-mortem với framing "giúp tôi thấy điểm gãy" |

### 1.2 Ownership

- **OWN Output Contract 5** (Pre-mortem Memo). Không workflow khác được tạo adversarial memo theo format này.
- **Domain dependency:** tùy thesis — equity VN thì pull `domain-equity-vn-forensic-accounting.md` + `domain-equity-vn-valuation-advanced.md`; macro thì pull `domain-macro-vn-liquidity.md`; cross-asset thì pull `domain-cross-asset-linkage.md`; FX thì pull `domain-fx-usd-vnd-dynamics.md`.
- **Framework anchor bắt buộc:** `core-meta-cognition.md` (6 câu hỏi foundation) + `framework-regime-v11.md` (regime context của thesis).

### 1.3 Composition rule

Pre-mortem **không tự generate thesis mới**. Nếu analyst không cung cấp thesis rõ → hỏi 1 câu: "Thesis chốt lại 1 câu là gì? Ví dụ: 'HPG hưởng lợi từ China stimulus 2026 → biên gộp lên 17% → giá fair 32k.'" Không soft — không chấp nhận thesis dạng "tôi thích HPG".

Pre-mortem **không đi thêm deep-dive**. Nếu thesis thiếu foundation analytical (chưa có drivers, chưa có valuation range) → handoff sang `workflow-deep-dive.md` trước, pre-mortem chạy sau.

---

## 2. INPUT PROTOCOL

### 2.1 Required input

| Input | Bắt buộc | Default nếu thiếu |
|---|---|---|
| **Thesis 1 câu** (subject + driver + mechanism + outcome) | YES | Hỏi lại, không guess |
| **Timeframe** (30/60/90/180 ngày) | NO | Default 90 ngày cho equity, 30-60 cho macro/FX, 180 cho structural |
| **Regime context** (R1-R5 theo framework-regime-v11.md) | NO | Tự classify từ data hiện tại, flag `[REGIME ASSUMED]` |
| **Position context** (đã position / chưa / đang cân nhắc) | NO | Không cần biết — pre-mortem không thay đổi output theo position |
| **Consensus context** (broker/market đồng thuận với thesis không) | NO | Ưu tiên check nếu có — consensus mạnh = pre-mortem càng gắt |

**Data gap protocol:** Thesis mơ hồ ("X tốt") → reject, hỏi format chuẩn. Thesis thiếu mechanism ("HPG sẽ lên") → reject, hỏi driver. Thesis thiếu outcome ("HPG hưởng lợi") → reject, hỏi metric quantifiable (biên gộp X%, giá Y, ROE Z%).

### 2.2 Thesis format chuẩn (analyst paste vào)

```
Subject: [ticker / asset / pair / macro variable]
Driver: [1 câu — cơ chế kinh tế trung tâm]
Mechanism: [2-3 câu — làm sao driver truyền dẫn vào outcome]
Outcome: [metric cụ thể + timeframe: biên gộp 17% Q4 2026, giá fair 32k trong 12 tháng, USD/VND < 24,800 trong 6 tháng]
Confidence analyst self-rate: [low/medium/high — qualitative]
Regime assumed: [R1-R5 theo framework v1.1]
```

Ví dụ hợp lệ: "HPG hưởng lợi từ China stimulus 2026 → iron ore demand tăng → HRC TSR spread mở rộng → biên gộp HPG lên 17% Q4 2026 (hiện 12.5%) → fair value 32k VND / 12 tháng. Confidence medium. Regime assumed R2 steady growth VN."

Ví dụ reject: "HPG tốt", "tôi thích HPG vì tăng trưởng", "HPG cyclical recovery" (thiếu outcome quantifiable).

---

## 3. EXECUTION PROTOCOL — 6 Steps Adversarial

6 bước chạy tuần tự, không skip, không trộn order. Mỗi bước có output standalone — memo render đủ 6 section cố định.

### Step 1 — RESTATE (hệ thống restate thesis bằng từ ngữ riêng)

**Mục tiêu:** Force clarity. Nếu không restate được thesis trong 2-3 câu mạch lạc → thesis có ambiguity ẩn, pre-mortem dừng ở đây, ask analyst clarify.

**Technique:**
- Bỏ hedging words của analyst ("có vẻ", "có thể", "kỳ vọng") → restate thành claim mạnh hơn analyst vừa nói.
- Expose causal chain: "Analyst đang nói A → B → C → D. Mỗi mắt xích phải giữ. Nếu B gãy thì C, D không cứu được."
- Identify implicit quantification: analyst nói "biên gộp lên" — lên bao nhiêu, trong bao lâu? Force số cụ thể.

**Output:** 1 paragraph (≤ 100 từ) restate thesis, kết thúc bằng câu "Nếu restate này sai, analyst sửa trước khi tôi phản biện."

**Red flag tại Step 1:**
- `[GIẢ ĐỊNH ẨN]` nếu phát hiện assumption analyst chưa nói ra (VD: "China stimulus 2026" → implicit assume stimulus effective, mechanism vào VN steel).
- `[NHẬN ĐỊNH CHỦ QUAN]` nếu thesis dựa chủ yếu vào narrative chưa có evidence.

### Step 2 — IDENTIFY IMPLICIT ASSUMPTIONS (≥ 5 giả định ẩn)

**Mục tiêu:** Mọi thesis đều build trên giả định ẩn. Pre-mortem phải list tối thiểu **5 assumption** analyst chưa nói ra nhưng thesis collapse nếu assumption sai.

**10-assumption taxonomy (check each, list relevant):**

| # | Loại assumption | Câu hỏi kiểm tra |
|---|---|---|
| A1 | **Macro regime stability** | Thesis giả định regime nào? Regime đó có shelf life bao lâu? Nếu shift sang regime X thì thesis còn không? |
| A2 | **Data quality** | Thesis dựa trên data Bậc 1-2 hay Bậc 3-4? Có peer cross-validation không? |
| A3 | **Mechanism strength** | Cơ chế driver → outcome là strong (empirical) hay weak (narrative)? Base rate historical bao nhiêu? |
| A4 | **Consensus vs contrarian** | Market đã price in chưa? Nếu consensus → upside đã gone; nếu contrarian → tại sao mình thấy đúng mà market sai? |
| A5 | **Counterparty/execution** | Thesis có require công ty/NHNN/Fed hành động cụ thể? Xác suất hành động đó xảy ra on-time? |
| A6 | **Lifecycle stage** | Company ở stage nào (Dickinson-Mauboussin)? Stage đó typical có driver analyst đang claim không? |
| A7 | **Competitive moat** | Thesis giả định pricing power / cost advantage. Moat sustainable không? Có erosion signal chưa? |
| A8 | **Liquidity / leverage** | Thesis giả định funding liquidity bình thường. Nếu stress (R4) thì thesis ra sao? |
| A9 | **Forward vs normalized** | Thesis dùng forward earnings / normalized earnings? Normalization window có representative không? |
| A10 | **Anchoring** | Thesis có anchor vào historical multiple / narrative cũ / giá quá khứ không? Anchor đó còn valid regime hiện tại? |

**Output:** Table 5-10 rows, cột `# | Assumption | Tại sao ẩn | Bậc bằng chứng | Cờ tự động`. Tối thiểu 5 row, không nén dưới 5. Assumption nào analyst đã explicitly nói ra → không đưa vào (pre-mortem chỉ track ẩn).

**Quality gate:** Nếu < 5 assumption phát hiện được → thesis có thể quá đơn giản hoặc hệ thống đang miss. Re-examine: có phải thesis thực ra là tautology hoặc trivial không?

### Step 3 — ATTACK EACH ASSUMPTION (devil's advocate, historical analog hoặc framework)

**Mục tiêu:** Mỗi assumption từ Step 2 bị attack bằng **1 trong 4 vũ khí**:

1. **Historical analog** — period lịch sử mà assumption tương tự đã fail. VD: "Giả định China stimulus effective" → attack bằng 2015-2016 China stimulus (RRR cut + infrastructure) → iron ore bounce ngắn 6 tháng rồi rollover, HPG biên gộp không break out sustained.
2. **Academic framework** — framework từ `frameworks/*` chỉ ra assumption weak. VD: Minsky (financial instability) → credit-driven cyclical recovery có tendency overshoot → assumption "biên gộp 17% sustained" có Ponzi-phase risk.
3. **Base rate** — empirical probability của assumption. VD: "HRC ramp on-time VN" — base rate 40% (per OPVIA internal data steel capex). Thesis giả định 100% on-time → bị discount bởi base rate.
4. **Counter-data** — data hiện tại contradict assumption. VD: analyst giả định "demand RE VN recovery 2026" → data: trade real estate Q1 2026 YoY -18%, banks room BĐS capped → contradict.

**Output:** Cho mỗi assumption (5-10 row), render 1 paragraph (≤ 80 từ) attack + cite vũ khí nào dùng (analog / framework / base rate / counter-data) + bậc bằng chứng của attack.

**Tone rule:** Adversarial, không soft. Forbidden phrases:
- "Có thể thesis đúng nếu..." → replace: "Thesis giả định X. Nếu X sai, thesis gãy ở điểm Y."
- "Tuy nhiên cũng cần lưu ý..." → remove, không cần hedging.
- "Tất nhiên assumption này có lý..." → remove, không validate assumption analyst mà pre-mortem đang attack.

### Step 4 — CONSTRUCT COUNTER-THESIS (bear case mạnh nhất)

**Mục tiêu:** Viết thesis ngược lại, steelman (mạnh nhất có thể), không strawman (không attack version yếu).

**Technique:**
- Counter-thesis phải có cùng structure như thesis gốc: subject + driver + mechanism + outcome + timeframe.
- Mechanism của counter-thesis phải là **cơ chế kinh tế explicit**, không narrative chung ("kinh tế xấu").
- Outcome của counter-thesis phải quantifiable, opposite với thesis gốc. VD: Thesis "biên gộp 17% Q4 2026" → Counter "biên gộp retest 10-11% Q4 2026".
- Counter-thesis ưu tiên dùng **3 assumption strongest-attacked từ Step 3** làm foundation. Không cherry-pick weak assumption.

**Output:** 1 section với:
- Counter-thesis 1 câu (tương đương format Step 2.2)
- Causal chain 3-5 mắt xích
- Outcome quantifiable + timeframe
- Bậc bằng chứng của counter-thesis (thường là `[Bậc 2-3]` — nếu counter-thesis có evidence mạnh hơn thesis gốc, analyst nên reconsider thesis gốc luôn)

**Quality gate:** Nếu counter-thesis yếu (không quantifiable, không mechanism, không timeframe) → Step 3 attack chưa đủ gắt → quay lại Step 3 redo. Counter-thesis yếu là sign hệ thống đang soft.

### Step 5 — IDENTIFY COMMON GROUND (điều cả thesis và counter phải đồng ý)

**Mục tiêu:** Dù conflict, thesis và counter đều có **common ground** — facts, constraints, hoặc observable cả hai phải chấp nhận. Common ground là nơi analyst không lose nếu sai — là "known knowns" của tình huống.

**Technique:**
- List 3-5 items cả thesis và counter đều phải admit. VD với HPG/China stimulus:
  - Cả hai đồng ý: China property sector stress từ 2021 chưa hết.
  - Cả hai đồng ý: HPG biên gộp hiện ~12.5% (Bậc 1).
  - Cả hai đồng ý: HRC DQ2 chưa reach normalized utilization.
  - Cả hai đồng ý: USD/VND pressure từ DXY hiện đang active.
- Items này là **anchor cho thesis-tracker sau pre-mortem** — analyst không cần re-debate, chỉ cần track variable quanh items này.

**Output:** Bullet list 3-5 items, mỗi item 1 dòng + bậc bằng chứng `[Bậc 1-2]`.

**Tại sao quan trọng:** Common ground là nền tảng cho Step 6 (decisive observable). Nếu không có common ground → thesis và counter đang nói về 2 realities khác nhau, pre-mortem không meaningful, handoff sang deep-dive để align facts trước.

### Step 6 — PROPOSE DECISIVE OBSERVABLE (30/60/90 ngày)

**Mục tiêu:** Đề xuất **observable cụ thể** mà nếu xảy ra sẽ **phân biệt dứt khoát** thesis vs counter trong 30/60/90 ngày. Decisive = single observable, không ambiguous, có data source rõ.

**Criteria cho decisive observable:**

| Criterion | Pass condition |
|---|---|
| **Observable** | Có data source cụ thể (FiinTrade, NHNN, GSO, HOSE, broker) |
| **Discriminating** | Nếu observable đi hướng A → thesis confirmed. Nếu hướng B → counter confirmed. Không có hướng C "neutral". |
| **Timeframe-bounded** | 30/60/90 ngày. Không "sometime in 2027". |
| **Threshold explicit** | Số cụ thể, không "cao/thấp". VD: "HRC spread > 80 USD/tấn" chứ không "HRC spread cao". |
| **Independent** | Không phải output của chính thesis (tránh tautology). VD: không dùng "HPG price" để confirm thesis HPG — phải dùng upstream variable như HRC spread, iron ore, RE VN sales. |

**Output:** Table cố định 3 row:

| Horizon | Observable | Data source | Threshold confirm thesis | Threshold confirm counter | Neutral zone |
|---|---|---|---|---|---|
| 30 ngày | [variable 1] | [source] | [số cụ thể] | [số cụ thể] | [range] |
| 60 ngày | [variable 2] | [source] | [số cụ thể] | [số cụ thể] | [range] |
| 90 ngày | [variable 3] | [source] | [số cụ thể] | [số cụ thể] | [range] |

**Rule:** 3 horizon phải dùng **3 variable khác nhau** (không cùng variable check 3 lần). 30 ngày ưu tiên leading indicator (realtime data), 60 ngày confirming (monthly data), 90 ngày structural (quarterly earnings / BoP).

**Handoff:** Cuối Step 6, 1 dòng "Handoff: Import 3 observable này vào `workflow-thesis-tracker.md` (Contract 4) để track liên tục. Pre-mortem dừng ở đây, không duplicate tracker logic."

---

## 4. OUTPUT TEMPLATE — Contract 5

Markdown structured. 6 section cố định + header + footer. Length 1-3 pages (500-1500 từ tiếng Việt).

### Header block (bắt buộc)

```
# Pre-Mortem Memo — {Thesis subject} — {YYYY-MM-DD}
Analyst: OPVIA Sigma | Workflow: workflow-pre-mortem.md
Thesis owner: OPVIA analyst | Confidence analyst self-rate: {low/med/high}
Regime assumed: {R1-R5 per framework-regime-v11.md, ngày, shelf life}
Timeframe: {30/60/90 / structural}
Consensus context: {consensus bullish / bearish / mixed} — nếu có check broker
```

### §1. THESIS RESTATE (Step 1)

1 paragraph (≤ 100 từ). Kết thúc: "Nếu restate này sai, analyst sửa trước khi tôi phản biện." Cờ `[GIẢ ĐỊNH ẨN]` / `[NHẬN ĐỊNH CHỦ QUAN]` nếu applicable.

### §2. IMPLICIT ASSUMPTIONS (Step 2)

Table 5-10 rows:

| # | Assumption (analyst chưa nói ra) | Loại (A1-A10) | Bậc | Cờ |
|---|---|---|---|---|
| 1 | [1 câu] | A1 Macro / A6 Lifecycle / ... | [Bậc 3] | `[GIẢ ĐỊNH ẨN]` |

### §3. ATTACK MỖI ASSUMPTION (Step 3)

Cho mỗi row §2, render subsection ngắn:

```
### §3.X — Attack A{#} ({loại assumption})
Weapon: [historical analog / framework / base rate / counter-data]
Attack: [1 paragraph ≤ 80 từ — attack gắt, không soft]
Bậc: [Bậc X]
```

### §4. COUNTER-THESIS (Step 4)

```
### §4.1 Counter-thesis 1 câu
{subject + driver + mechanism + outcome + timeframe — opposite direction}

### §4.2 Causal chain
- Mắt xích 1: ...
- Mắt xích 2: ...
- Mắt xích 3: ...

### §4.3 Bậc counter-thesis
[Bậc 2-3]. Nếu counter ≥ Bậc thesis gốc → recommendation analyst reconsider thesis gốc.
```

### §5. COMMON GROUND (Step 5)

Bullet list 3-5 items + bậc bằng chứng từng item.

### §6. DECISIVE OBSERVABLE (Step 6)

Table 3 row (30/60/90 ngày) theo format §3.6 trên.

### §7. METHODOLOGY LIMITATIONS (bắt buộc — Output Contract common requirement)

3-4 bullet:
- **Data gap:** variable nào analyst chưa cung cấp / data Bậc 4 / estimated.
- **Regime dependency:** pre-mortem này valid trong regime X, nếu shift sang Y thì analysis thay đổi.
- **Confidence calibration:** counter-thesis self-rated `low/medium/high` qualitative — không bịa %.
- **Out-of-scope:** pre-mortem không check forensic (handoff `domain-equity-vn-forensic-accounting.md` nếu cần), không check valuation (handoff `workflow-deep-dive.md` §10).

### §8. HANDOFF + NEXT STEP

1 dòng: "Handoff → `workflow-thesis-tracker.md` với 3 observable §6. Re-run pre-mortem nếu: (a) assumption §2 mới emerge, (b) regime shift, (c) structural break trong common ground §5."

---

## 5. ANTI-PATTERNS — Reject ở quality gate

Pre-mortem là workflow dễ fail nhất vì đối kháng với bias tự nhiên (tìm evidence ủng hộ thesis). Danh sách anti-pattern dưới đây BẮT BUỘC pass scan trước khi output. ≥ 1 anti-pattern = revise.

| # | Anti-pattern | Ví dụ fail | Fix |
|---|---|---|---|
| 1 | **Soft language** — hedging thesis attacker | "Có thể assumption này không đúng" | "Assumption này sai nếu X — bằng chứng Y" |
| 2 | **Fake adversarial** — pretending to attack but conceding | "Thesis của analyst có rủi ro macro chung, nhưng base case vẫn OK" | Remove concession. State thesis-breaker cụ thể. |
| 3 | **Strawman counter-thesis** — attack weak version | Counter-thesis "HPG sẽ phá sản" khi thesis gốc chỉ nói biên gộp không đạt | Steelman: counter "biên gộp retest 10-11%" — cùng metric, opposite direction |
| 4 | **Generic assumptions** — không specific | "Assumption: macro VN ổn định" | "A1: Assumption NHNN không tăng OMO rate >100bps trong 6 tháng tới" |
| 5 | **Missing quantification** — thiếu số cụ thể | "Nếu demand giảm thì thesis gãy" | "Nếu HRC spread < 60 USD/tấn 3 tháng liên tiếp → thesis gãy" |
| 6 | **Recommendation leak** | "Không nên buy HPG ở giá này" | "Thesis-breaker: HRC spread < 60 → re-evaluate position (NOT recommend)" |
| 7 | **Price prediction** | "Giá HPG sẽ về 22k" | "Counter-thesis outcome: fair value range 20-24k theo scenario bear" |
| 8 | **Tautological observable** — check thesis bằng chính price | Observable: "HPG price < 24k" | Observable: upstream variable — "HRC spread < 60" |
| 9 | **Neutral zone too wide** — observable không discriminating | Threshold confirm thesis: HRC > 100. Counter: < 50. Neutral: 50-100 (quá wide) | Thesis: > 80. Counter: < 70. Neutral: 70-80 (narrow) |
| 10 | **Consensus collapse** — just parrot market consensus | Counter-thesis = broker bear case copy-paste | Build counter-thesis từ assumption attack §3, không import external bias |
| 11 | **< 5 assumption** | 3 assumption listed | Re-examine — thesis có quá simple hoặc hệ thống đang miss? Force tới 5+ |
| 12 | **Vietlish** | "Check lại momentum", "review driver" | Tiếng Việt: "Kiểm tra đà", "rà lại driver" |
| 13 | **Bậc bằng chứng missing** | Claim không có `[Bậc N]` | Add `[Bậc 1-4]` cho mọi claim factual |
| 14 | **Regime context missing** | Pre-mortem không reference regime | Header block phải có regime assumed + shelf life |

---

## 6. QUALITY CHECKLIST — 10 items pre-output

Pass all 10. Fail ≥ 1 → revise. Hệ thống self-check ngầm, không báo cáo.

| # | Check | Pass criteria |
|---|---|---|
| 1 | **6 sections đầy đủ** | §1-§6 render đủ, không skip |
| 2 | **§2 ≥ 5 assumption** | Table có tối thiểu 5 row |
| 3 | **§3 mỗi assumption attacked** | Không row nào missing attack; mỗi attack có weapon (analog/framework/base rate/counter-data) |
| 4 | **§4 counter-thesis quantifiable** | Counter có metric + timeframe + bậc |
| 5 | **§5 common ground 3-5 items** | Không empty, không > 5 |
| 6 | **§6 decisive observable 3 horizon** | Table 3 row 30/60/90; threshold explicit; independent variable (không tautology) |
| 7 | **§7 methodology limitations** | 3-4 bullet theo template |
| 8 | **Anti-pattern scan** | 14 anti-pattern §5 không match nào |
| 9 | **Tone adversarial** | Không soft language, không hedging, không concession |
| 10 | **Regime + Bậc + Cờ** | Header có regime; claim có bậc; flag applicable (`[GIẢ ĐỊNH ẨN]`, `[REGIME-SPECIFIC]`, etc.) |

---

## 7. HANDOFF CONDITIONS

| Tình huống trong pre-mortem | Handoff |
|---|---|
| Thesis thiếu foundation (chưa có driver / valuation range) | `workflow-deep-dive.md` trước |
| §6 decisive observable → analyst muốn track liên tục | `workflow-thesis-tracker.md` (Contract 4) |
| §3 attack bằng counter-data forensic (Beneish, accrual, covenant) | `domain-equity-vn-forensic-accounting.md` |
| Counter-thesis mechanism macro-wide | `domain-macro-vn-liquidity.md` + `domain-cross-asset-linkage.md` |
| Regime shift emerge trong §5 common ground | `workflow-regime-shift-alert.md` (Contract 6) |
| Analyst phản biện pre-mortem → thesis revised | Re-run pre-mortem với thesis v2 (không merge — pre-mortem cũ giữ làm audit trail) |

**Rule:** Pre-mortem không tự chain. Cuối memo 1 dòng "Next-step suggest" — analyst confirm mới chạy handoff.

---

## 8. WORKED EXAMPLE — Pre-mortem "HPG hưởng lợi từ China stimulus 2026"

Render đầy đủ Contract 5 cho thesis demo (acceptance test #5 từ Focus_Brief §10).

### Header

```
# Pre-Mortem Memo — HPG / China stimulus 2026 thesis — 2026-04-19
Analyst: OPVIA Sigma | Workflow: workflow-pre-mortem.md
Thesis owner: OPVIA analyst | Confidence analyst self-rate: medium
Regime assumed: R2 Steady Growth VN (call 2026-04-11, shelf 2-3 tuần, invalidate nếu DXY > 108 hoặc USD/VND > 25,800)
Timeframe: 90 ngày (Q2-Q3 2026)
Consensus context: broker split — VCSC/SSI bullish HPG (HRC thesis), ACBS/MBS neutral; mainstream media bullish China stimulus narrative
```

### §1. Thesis Restate

Analyst đang claim: Gói stimulus Trung Quốc 2026 (RRR cut + infrastructure package) → iron ore demand Trung Quốc tăng → HRC-iron ore spread toàn cầu mở rộng → HPG, vì tích hợp dọc 8.5M tấn sau DQ2, capture full spread expansion → biên gộp 2026 nhảy từ 12.5% hiện tại lên 17% Q4 2026 → reverse DCF implied fair value 32k VND cho horizon 12 tháng. Causal chain: stimulus TQ → iron ore demand → HRC spread → HPG margin → HPG valuation. Nếu restate này sai, analyst sửa trước khi tôi phản biện. `[GIẢ ĐỊNH ẨN]`: stimulus effective + mechanism intact + HPG capture full, không leak sang peer.

### §2. Implicit Assumptions (9 items)

| # | Assumption (analyst chưa nói ra) | Loại | Bậc | Cờ |
|---|---|---|---|---|
| 1 | China stimulus 2026 thực sự pass + implement trong 6 tháng | A5 Counterparty | [Bậc 3] | `[GIẢ ĐỊNH ẨN]` |
| 2 | Stimulus TQ tập trung infrastructure (steel-intensive), không consumer | A3 Mechanism | [Bậc 3] | `[GIẢ ĐỊNH ẨN]` |
| 3 | Iron ore demand respond với stimulus lag ≤ 3 tháng (không 6-9 tháng như 2015-16) | A3 Mechanism | [Bậc 3] | `[NHẬN ĐỊNH CHỦ QUAN]` |
| 4 | HRC-iron ore spread correlate với iron ore level (không overshoot input cost) | A3 Mechanism | [Bậc 4] | `[CHƯA KIỂM CHỨNG]` |
| 5 | HPG biên gộp sensitivity tới HRC spread là linear (không non-linear) | A9 Forward/Normalized | [Bậc 4] | `[LINEAR MODEL RISK]` |
| 6 | DQ2 ramp on-time, reach 70% utilization Q4 2026 | A6 Lifecycle | [Bậc 3] | `[CHƯA KIỂM CHỨNG]` |
| 7 | Regime R2 persist 6-12 tháng (DXY < 108, USD/VND stable) | A1 Macro regime | [Bậc 3] | `[REGIME-SPECIFIC]` |
| 8 | RE VN recovery 2026 (demand nội địa steel) | A3 Mechanism + A1 Macro | [Bậc 3] | `[CHƯA KIỂM CHỨNG]` |
| 9 | Thesis chưa price in — consensus chưa bullish đủ | A4 Consensus | [Bậc 3] | `[GIẢ ĐỊNH ẨN]` |

### §3. Attack each assumption

**§3.1 — Attack A1 (China stimulus pass + implement timing)**
Weapon: Historical analog + base rate. 2015-2016 TQ stimulus (RRR cut, infrastructure push) — infrastructure package announced Q1 2016, actual steel demand inflection Q3 2016 (lag 6 tháng), iron ore rally ngắn từ Q2 2016 rồi rollover Q4 2016 khi TQ tightens lại. Base rate stimulus effective on-time ≤ 3 tháng: ~35% theo pattern 2008, 2012, 2015-16, 2020. Thesis timeframe 90 ngày giả định Q2-Q3 2026 inflection → đòi stimulus pass Q1 2026 + implement Q2 → too tight. [Bậc 2].

**§3.2 — Attack A2 (stimulus infra-heavy, không consumer)**
Weapon: Counter-data. TQ policy narrative 2025-2026 shift sang "common prosperity + consumption rebalance" thay vì "infrastructure push" legacy. Recent Politburo communique Dec 2025 mention "optimize infrastructure investment structure" — không phải "scale up". Nếu stimulus consumer-heavy (subsidy hàng tiêu dùng, tax cut hộ gia đình) → steel intensity elasticity thấp hơn 40-60% so với infrastructure stimulus. [Bậc 3].

**§3.3 — Attack A3 (iron ore demand lag ≤ 3 tháng)**
Weapon: Framework (Kashyap-Stein bank lending channel). Credit transmission vào TQ steel sector qua 3 lag: (1) policy → SOE bank lending (1-2 tháng), (2) bank lending → infrastructure project financing (2-4 tháng), (3) project financing → steel order (1-3 tháng). Total lag 4-9 tháng. Thesis 3-tháng lag inconsistent với transmission mechanism. [Bậc 2].

**§3.4 — Attack A4 (HRC spread correlate với iron ore level, không overshoot)**
Weapon: Historical analog. 2021 Q2-Q3: iron ore surge tới 220 USD/tấn, nhưng HRC spread COMPRESSED vì TQ steel mill buộc sản xuất để giữ market share trong cost squeeze (political mandate). HPG 2021 Q3 biên gộp giảm despite iron ore tăng. Assumption "spread expand proportional với iron ore" fail trong regime chính trị TQ. [Bậc 2].

**§3.5 — Attack A5 (HPG margin sensitivity linear)**
Weapon: Framework (operating leverage). HPG high fixed cost (nặng BOF + capital intensive DQ2), non-linear response: (a) spread expand 10 USD/tấn trong normal util → +1.2pp biên gộp; (b) spread expand 10 USD/tấn trong under-util (DQ2 2026 dự kiến 40-50%) → +0.4pp biên gộp vì fixed cost drag. Thesis linear model over-estimate margin uplift ~2x. [Bậc 3] `[LINEAR MODEL RISK]`.

**§3.6 — Attack A6 (DQ2 on-time ramp)**
Weapon: Base rate. OPVIA internal data steel capex VN on-time rate ~40% (HSG Phú Mỹ, POM Nghi Sơn, TVN). HPG DQ2 specifically: phase 1 commissioned 2024 Q4 with 2-tháng delay; phase 2 originally target Q2 2026, recent management call says "Q3-Q4 2026". Giả định 70% utilization Q4 2026 có base rate ≤ 40%. [Bậc 2].

**§3.7 — Attack A7 (Regime R2 persist)**
Weapon: Counter-data + framework (regime v1.1). USD/VND hiện 25,420 (accumulated 1.4% q/q, gần Rule D Veto threshold 1.5%). FII outflow phiên 4/4. Nếu DXY break 108 Q2 2026 → shift R3 → HPG (cyclical) hit first (per §7.1 framework-regime-v11.md module priority R3 = forensic + monetary policy focus, NOT cyclical valuation). Thesis giả định R2 persist 6-12 tháng có probability qualitative trung bình-thấp. [Bậc 3] `[REGIME-SPECIFIC]`.

**§3.8 — Attack A8 (RE VN recovery 2026)**
Weapon: Counter-data. BĐS VN Q1 2026 transaction volume YoY -18% (FiinTrade), primary sales price index -4% YoY, bank room BĐS capped (NHNN room), corp bond BĐS issuance freeze continue. Recovery signal chưa xuất hiện. Thesis "RE recovery 2026" có `[CHƯA KIỂM CHỨNG]`, timeline realistic có thể là H2 2027. [Bậc 2].

**§3.9 — Attack A9 (consensus chưa bullish)**
Weapon: Counter-data. VCSC target price HPG 28k (bullish), SSI 29k (bullish), Bloomberg consensus forward P/E 2026 implied margin 14-15% (đã price in partial thesis). Thesis giả định market chưa price in → fail: market đã price in ~50% của thesis. Upside gap từ 26k hiện tại → 32k = 23%, không 23% pure alpha. [Bậc 2].

### §4. Counter-Thesis

**§4.1 Counter-thesis 1 câu:** HPG biên gộp retest 10-11% Q4 2026 (thấp hơn 12.5% hiện tại), fair value bear range 18-22k VND horizon 12 tháng, do combination của (a) China stimulus consumer-heavy + lag 6-9 tháng > thesis timeframe, (b) DQ2 ramp chậm + fixed cost drag non-linear, (c) RE VN recovery lag sang H2 2027, (d) regime R2 → R3 shift Q2-Q3 2026 với DXY pressure.

**§4.2 Causal chain:**
- Mắt xích 1: China stimulus Q2 2026 implementation (xác suất on-time 35%) → iron ore demand inflection Q4 2026 thay vì Q2-Q3.
- Mắt xích 2: HRC spread không expand (TQ mill political squeeze repeat 2021) + DQ2 under-utilization → HPG biên gộp sideways 11-13%.
- Mắt xích 3: RE VN demand yếu + bank room BĐS capped → volume sản phẩm HPG (construction steel) không hỗ trợ operating leverage.
- Mắt xích 4: Regime shift R2 → R3 Q2-Q3 2026 → cyclical P/E de-rating multiple từ 8x về 5-6x forward.
- Mắt xích 5: Reverse DCF implied CAGR 8-9% sẽ miss → stock de-rate cả multiple và earnings.

**§4.3 Bậc counter-thesis:** [Bậc 2-3]. Counter-thesis evidence mạnh ngang thesis gốc — đặc biệt A3 (Kashyap-Stein mechanism) + A4 (2021 TQ analog) + A6 (DQ2 base rate) đều ở Bậc 2. Analyst nên reconsider confidence rating self-rated "medium" — counter-thesis có thể force xuống low-medium.

### §5. Common Ground

- Cả thesis và counter đồng ý: HPG biên gộp hiện 12.5% (Bậc 1, BCTC Q4 2025).
- Cả hai đồng ý: DQ2 chưa reach normalized utilization (hiện ~40%, target ≥70%, timing tranh cãi).
- Cả hai đồng ý: Iron ore price sensitivity là driver lớn nhất của margin HPG.
- Cả hai đồng ý: Regime R2 VN hiện đang active, shelf life 2-3 tuần theo framework v1.1.
- Cả hai đồng ý: RE VN chưa recovery theo data Q1 2026 (FiinTrade, NHNN room).

### §6. Decisive Observable (30/60/90)

| Horizon | Observable | Data source | Confirm thesis | Confirm counter | Neutral |
|---|---|---|---|---|---|
| 30 ngày | HRC-iron ore spread (global) | Bloomberg / SGX | > 80 USD/tấn 3 tuần liên tiếp | < 60 USD/tấn 3 tuần | 60-80 |
| 60 ngày | HPG DQ2 utilization (management disclosure Q2 2026 report) | HPG earnings call + FiinTrade | ≥ 60% util Q2 + commitment "70% Q4" | ≤ 45% util + delay Q3-Q4 language | 45-60% |
| 90 ngày | VN construction steel sales volume (Vietnam Steel Association monthly) | VSA | YoY growth ≥ +8% trong Aug-Sep 2026 | YoY < -3% trong Aug-Sep 2026 | -3% to +8% |

Handoff: Import 3 observable này vào `workflow-thesis-tracker.md` để track liên tục. Pre-mortem dừng ở đây.

### §7. Methodology Limitations

- **Data gap:** Internal HPG DQ2 ramp timeline giả định management call Q4 2025 (Bậc 3 — chưa audit). Actual throughput data chờ Q2 2026 filing.
- **Regime dependency:** Pre-mortem valid trong regime R2 (call 2026-04-11). Nếu shift R3 trong 2 tuần → counter-thesis margin of victory tăng đáng kể (framework-regime-v11.md §7.1 R3 module priority).
- **Confidence calibration:** Counter-thesis self-rated "medium" qualitative. Không đưa %.
- **Out-of-scope:** Pre-mortem không check forensic HPG (handoff `domain-equity-vn-forensic-accounting.md` nếu analyst muốn check Beneish / accrual); không valuation DCF mới (handoff `workflow-deep-dive.md` §10 nếu muốn revise fair value range).

### §8. Handoff + Next Step

Next-step suggest: (1) Import 3 observable §6 vào `workflow-thesis-tracker.md` để start tracking từ hôm nay. (2) Re-run pre-mortem Q3 2026 sau khi có HPG Q2 earnings (Aug 2026) — assumption A6 (DQ2 ramp) sẽ được data mới resolve. (3) Nếu regime shift R2 → R3 trong 30 ngày → tự động invalidate thesis gốc, run pre-mortem v2 với regime assumption mới.

---

## 9. VERSION + MAINTENANCE

- **Phase 3 locked:** 6-step protocol, 10-assumption taxonomy, 14 anti-pattern scan, 10-item quality checklist, 3-horizon observable rule.
- **Open for revise sau Sprint 1-2:** base rate quantification (hiện chủ yếu qualitative — sau khi backtest 5-10 thesis historical OPVIA có, có thể calibrate empirical base rate); persistence rule cho counter-thesis (hiện không có, có thể thêm "counter-thesis confirmed khi 2/3 observable breach threshold").
- **Phase 4 consideration:** Meta-pre-mortem — pre-mortem CỦA pre-mortem (kiểm tra hệ thống có đang anchor vào bear narrative không, confirmation bias inverse).

---

**Hết workflow-pre-mortem.md v1.0 (Wave 6 Lane 1 — Contract 5 owner).**

Tác giả: Wave 6 Lane 1 (Native Opus Executor).
Reference: Focus_Brief.md §6 Workflow 6 + §9 Contract 5; core-meta-cognition.md (6-question foundation); framework-regime-v11.md (regime context); workflow-deep-dive.md (sibling pattern — §14 Scenario handoff source); Klein (2007) premortem technique; Tetlock Superforecasting devil's advocate.
