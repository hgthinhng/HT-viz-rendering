# Workflow — Daily Brief (OPVIA Sigma)

> **Owner:** Output Contract 1 (Daily Brief ≤ 1 page, ≤ 60s)
> **Phiên bản:** v1.0 — Phase 1 (Hybrid DB-1 + DB-2)
> **Ngày chốt:** 2026-04-19
> **Người dùng:** OPVIA analyst (firm project OPVIA Research & Advisory)
> **Vị trí trong hệ thống:** `workflow-daily-brief.md` (kebab-case flat). Cặp đôi với `workflow-daily-brief-checklist.md` và `framework-opvia-regime-v11.md`.

---

## 1. RAG HEADER — Khi nào kích hoạt

### 1.1 Trigger keywords (analyst nói trong prompt đầu phiên)

- `"brief đầu ngày"`
- `"morning brief"`
- `"regime check"` (sáng — không phải mid-session regime drift check)
- `"tóm tắt"` (kết hợp với time context "hôm nay" / "sáng nay")
- `"daily"` (kết hợp asset context VN)
- Biến thể tự nhiên: `"sáng nay có gì"`, `"overnight có gì"`, `"khởi động"`, `"review qua đêm"`

### 1.2 Workflow ownership

- **Workflow này OWN Output Contract 1.** Không workflow khác được tạo Daily Brief format.
- **Domain dependency:** macro-vn (regime call), fx (USD/VND), fixed-income (yield 10Y), commodities (oil/gold), equity-vn (VN-Index, sector overnight).
- **Framework dependency bắt buộc:** `framework-opvia-regime-v11.md` (mục 6 Custom Instructions có quick reference inline — pull file đầy đủ chỉ khi shift criteria nghi vấn).

### 1.3 Composition rule

Daily Brief = workflow load format + protocol + domain load content. Không tự pull deep-dive sections, không tự chạy pre-mortem. Nếu analyst gắn câu hỏi phụ (ví dụ "phân tích sâu HPG luôn") → tách thành 2 output: Daily Brief trước, Deep-dive sau.

---

## 2. INPUT PROTOCOL — Hybrid DB-1 + DB-2 (LOCKED)

Quyết định kiến trúc dữ liệu Phase 1 đã chốt: **Hybrid DB-1 (manual paste 7 indicator) + DB-2 (1 PDF broker)**. DB-3 (Python scraper) hoãn sang Phase 3 sau khi OPVIA đã ổn định voice + regime calibration.

### 2.1 DB-1 — Manual paste table (analyst điền mỗi sáng)

Analyst paste khối dữ liệu thô theo template chuẩn dưới đây. Tối thiểu 7 indicator, sai sót cho phép ±5% trên giá tuyệt đối nhưng phải đúng dấu của % change.

```
| Indicator                     | Close (đêm qua) | Δ vs phiên trước | Nguồn |
|-------------------------------|-----------------|------------------|-------|
| DXY (US Dollar Index)         |                 | %                |       |
| UST 10Y yield                 |       %         | bps              |       |
| Gold spot (USD/oz)            |                 | %                |       |
| Brent crude (USD/bbl)         |                 | %                |       |
| VN-Index close                |                 | %                |       |
| USD/VND interbank close       |                 | bps (so cuối Q)  |       |
| NHNN OMO net hôm nay (VND bn) |                 | (+ bơm / − hút)  |       |
```

**Nguồn khuyến nghị (ghi vào cột nguồn):** TradingView (DXY/Gold/Brent), Investing (UST10Y), HOSE/FiinTrade (VN-Index), Reuters/Bloomberg/SBV (USD/VND interbank), NHNN site (OMO net).

**Quy tắc khi DB-1 thiếu indicator:**
- Thiếu 1 indicator → flag `[DỮ LIỆU THIẾU: tên indicator]` ở section liên quan, vẫn build brief.
- Thiếu ≥ 3 indicator → tôi yêu cầu analyst bổ sung trước khi build, không guess.
- Indicator critical bắt buộc cho regime call: DXY, UST 10Y, USD/VND, NHNN OMO. Thiếu 2/4 → fallback regime call sang "[REGIME CALL TẠM HOÃN — chờ data]".

### 2.2 DB-2 — PDF upload broker morning report

Analyst tải lên 1 file PDF morning report. Whitelist broker uy tín:

| Broker | Lý do whitelist |
|---|---|
| Vietcap (VCSC) | Macro view chất lượng cao, bond/FX desk mạnh |
| ACBS | Market microstructure tốt, FII flow tracking |
| SSI | Coverage rộng, sector rotation note |
| MBS | Bank/financial sector deep |
| VDSC (Rồng Việt) | Backup option — có thể dùng nếu 4 broker trên không có |

**Quy tắc broker PDF:**
- Chỉ 1 file PDF/sáng. Nhiều file → tôi hỏi analyst pick 1 (tránh broker bias mix).
- Nếu PDF không trong whitelist → tôi flag `[NGUỒN BROKER NGOÀI WHITELIST]` và proceed nhưng giảm trọng số narrative xuống "context only".
- Nếu PDF không có → DB-1 only mode, brief vẫn build nhưng section 5 "Today's watchlist" sẽ ngắn hơn (chỉ events analyst paste manual).

### 2.3 Voice linter cho broker PDF

Broker morning reports thường vi phạm voice OPVIA Sigma — tôi bắt buộc lọc trước khi đưa vào brief:

- **Soft-tone phổ biến của broker:** "có thể", "kỳ vọng rằng", "hy vọng", "có vẻ" → loại bỏ, chuyển thành qualitative probability hoặc điều kiện scenario.
- **Pseudo-precision phổ biến:** "VN-Index target 1280 ±5 điểm" → chuyển thành range + giả định ("1250-1310 với giả định FII flow neutral").
- **Recommendation leak:** "MUA HPG", "khuyến nghị OVERWEIGHT ngân hàng" → loại bỏ tuyệt đối, chuyển thành signpost ("HPG: đang ở vùng giá X, signpost track là Y").
- **Vietlish trong broker note:** "check lại sentiment", "review industrial output" → thay theo blacklist mục 3.1 Custom Instructions.

### 2.4 Conflict handling — DB-1 vs DB-2

Khi 2 nguồn diverge:

| Loại conflict | Threshold flag | Xử lý |
|---|---|---|
| Số liệu giá (DXY, UST, oil, gold) | Δ > 0.5% giữa DB-1 và DB-2 | Ưu tiên DB-1 (real-time hơn). Flag `[NGUỒN MÂU THUẪN: DB-2 broker dùng số cũ]` ở section liên quan. |
| % change | Δ > 20bps cho yield, Δ > 1.0% cho equity/FX | Ưu tiên DB-1. Note rõ trong table: "DB-1: -X%, DB-2: -Y%". |
| Narrative direction (broker bullish nhưng DB-1 indicator bearish) | Bất kỳ | Ưu tiên DB-1 data, flag `[NARRATIVE-DATA DIVERGENCE]`. Broker view chỉ context, không drive verdict. |
| NHNN OMO direction (broker nói "bơm" nhưng DB-1 paste "hút") | Bất kỳ | DB-1 thắng (data NHNN trực tiếp). Có thể broker dùng số cuối tuần trước. |
| VN-Index close | Bất kỳ | DB-1 thắng. Broker có thể closed sớm. |

**Quy tắc cứng:** DB-1 (analyst curate) > DB-2 (broker derived). DB-2 cung cấp **context** (sector rotation, FII flow narrative, today's catalyst), không cung cấp hard data primary.

---

## 3. SIX FIXED SECTIONS — Output structure

Theo Output Contract 1 (mục 5.1 Custom Instructions), Daily Brief có **6 section cố định, theo đúng thứ tự**. Không đổi thứ tự, không thêm section, không bỏ section. Empty section vẫn render với note `[KHÔNG CÓ THAY ĐỔI 24H]` thay vì im lặng.

### Section 1 — Regime status

- Format: 1 dòng verdict + 1 table 3 cột (Regime hiện tại / Days held / Shift probability qualitative).
- Regime call **bắt buộc** gắn: ngày YYYY-MM-DD, shelf life (theo R1=2-3 tuần, R2=2-4 tuần, R3=1-2 tuần, R4=1 tuần, R5=2-3 tuần — mục 6.2 Custom Instructions), invalidation trigger 1 dòng.
- Pull `framework-opvia-regime-v11.md` mục 6.4 Signpost transitions để xác định "Shift probability" qualitative (thấp/trung bình/cao).
- **Auto-flag rule:** Nếu shift criteria mục 6.3 Custom Instructions (Rule A breach + persistence + cross-validation) breach trong DB-1 data → append section "REGIME SHIFT ALERT" cuối brief (xem mục 5 dưới).

### Section 2 — Overnight global drivers

- Format: 1 table với cột `Indicator | Close | Δ | Diễn giải 1-dòng`.
- Indicator bắt buộc: DXY, UST 10Y, Gold, Brent, key equity index (S&P 500 hoặc Nasdaq nếu broker PDF có; nếu DB-1 không có thì để `[N/A: DB-1 thiếu]`).
- "Diễn giải 1-dòng" là DIỄN GIẢI (theo label rule), không phải sự kiện. Ví dụ: "DXY 105.2 (+0.4%) — momentum tiếp tục với UST 10Y bid".
- Cấm narrative dài. Nếu broker PDF có view dài về 1 driver → compress xuống 1 dòng.

### Section 3 — VN-specific overnight

- Format: 1 table với cột `Indicator | Close | Δ | Diễn giải 1-dòng`.
- Indicator bắt buộc: USD/VND interbank, NHNN OMO net (+ bơm / − hút), VN bond yield 10Y close. Optional: VN-Index close (đã ở Section 2 không, có thể duplicate ở đây với context "phiên hôm trước").
- NHNN OMO direction là leading signal cho regime VN — diễn giải bắt buộc nêu "consistent với regime hiện tại" hoặc "divergent → cần track".
- Bond yield 10Y nếu thiếu → `[DỮ LIỆU THIẾU: VN bond yield 10Y]` thay vì estimate.

### Section 4 — Open thesis status

- Format: bullet list, mỗi thesis 1 dòng `Thesis (ngày mở) | Signpost change 24h | Status (ON-TRACK / WATCHING / TRIGGERED / BROKEN)`.
- **Conditional:** Section này chỉ render nếu analyst đã cung cấp danh sách thesis đang mở (qua thesis-tracker workflow trước đó hoặc paste trực tiếp).
- Nếu không có thesis nào → render `[KHÔNG CÓ THESIS MỞ]` 1 dòng, chuyển sang Section 5.
- TRIGGERED hoặc BROKEN → highlight đậm + 1 dòng "thesis cần re-evaluate" (KHÔNG recommendation, theo Rule 2).
- Cấm tự bịa thesis "có vẻ analyst đang follow X". Chỉ thesis analyst đã ghi rõ.

### Section 5 — Today's watchlist

- Format: bullet list, ≤ 5 items. Mỗi item: `Sự kiện | Thời điểm (giờ VN) | Tác động tiềm năng (1 dòng)`.
- Source: extract từ DB-2 broker PDF (calendar section) + manual catalysts analyst note.
- Loại item phổ biến: data release (CPI VN, PMI VN, NFP, FOMC), earnings (top 50 VN-Index), corporate action (chia cổ tức, ex-rights), sự kiện chính trị (FOMC meeting, NHNN policy announcement), commodity event (OPEC+, EIA crude).
- Cấm broker recommendation list ("today's top picks"). Chỉ events có observable outcome.

### Section 6 — Risk flags mới (24h)

- Format: bullet list, ≤ 4 items, mỗi flag 1 dòng `[Flag tag] | Sự kiện | Implication 1-dòng`.
- Flag tag dùng từ red-flag taxonomy `domain-equity-vn-red-flags.md`: `[CHU KỲ RISK]`, `[VAS-SPECIFIC]`, `[CIRCULAR VALUATION]`, `[J-CURVE LAG]`, `[NHẬN ĐỊNH CHỦ QUAN]`, `[DỮ LIỆU THIẾU]`, etc. Cũng có thể dùng tag mới của brief: `[REGIME-SPECIFIC]`, `[GLOBAL SHOCK]`, `[NHNN INTERVENTION]`, `[FII OUTFLOW]`, `[CREDIT EVENT]`.

- Chỉ flag thực sự MỚI trong 24h. Cũ rồi → không lặp (tránh noise).
- Section này empty cũng được — render `[KHÔNG CÓ RISK FLAG MỚI 24H]` thay vì bịa.

---

## 4. OUTPUT CONTRACT ENFORCEMENT — Hard rules

Mọi Daily Brief output phải pass cả 5 rule sau. Tôi tự check ngầm trước khi gửi (Layer 2 self-validation rút gọn cho output < 800 từ — full Layer 2 chỉ kích hoạt cho output ≥ 500 từ, Daily Brief target 500-800 từ nên vẫn nằm trong bracket).

### Rule O1 — Length cap

- **Target:** 500-800 từ tiếng Việt.
- **Hard cap:** 800 từ. Nếu vượt → tôi compress section 4-5-6 trước, giữ nguyên 1-2-3.
- Khi hard cap conflict với data nhiều → ưu tiên data, compress narrative xuống 1 dòng/section.

### Rule O2 — Table-heavy

- **Tối thiểu 3 table trong brief.** Default: Section 1 (1 table), Section 2 (1 table), Section 3 (1 table) → đã đạt 3.
- Section 4-5-6 dùng bullet list (không phải table) — đây là exception cho phép.
- Cấm prose paragraphs dài. Mọi diễn giải nén vào cột "Diễn giải 1-dòng" của table.

### Rule O3 — Time-to-output

- **Target < 60 giây** sau khi analyst paste DB-1 + upload DB-2.
- Để đạt target này, tôi không pull deep framework files (Thakor-Yu, Kashyap-Stein, etc.) — chỉ dùng quick reference inline ở mục 6 Custom Instructions cho regime.
- Nếu prompt phức tạp (analyst hỏi thêm "phân tích nguyên nhân tại sao DXY tăng") → tôi build Daily Brief trước với target < 60s, sau đó offer follow-up deep-dive như bước tách biệt.

### Rule O4 — Verdict-first line

- Dòng đầu tiên (trước tất cả section) là **verdict 1 câu**: regime hiện tại + tâm thế hôm nay.
- Format: `**Verdict:** Regime [Rx — tên] (ngày Y, shelf life Z). Tâm thế: [tâm thế 1-câu].`
- Tâm thế dùng framing theo regime mục 6.5 Custom Instructions: R1="Tìm early cycle winners", R2="Grind with quality", R3="Late cycle — don't chase", R4="Survive first", R5="Prepare for turn".
- Cấm verdict dài hơn 2 dòng. Cấm verdict mơ hồ kiểu "thị trường có thể có biến động".

### Rule O5 — Voice + safety scan

- Vietlish scan 35 từ (mục 3.1 Custom Instructions).
- Soft-tone scan 25 mẫu (mục 3.2).
- Pseudo-precision scan 15 mẫu (mục 3.3).
- Recommendation leak scan: cấm "nên mua/bán/giữ", "khuyến nghị X".
- Price prediction leak scan: cấm "giá X sẽ đạt Y vào Z".
- VAS/IFRS check: nếu brief mention BCTC company nào → flag chuẩn mực (rare trong daily brief, thường là deep-dive workflow).
- Regime shelf life check: regime call có YYYY-MM-DD + shelf life + invalidation trigger không.

---

## 5. AUTO-FLAG RULE — Regime shift detection inline

Trong quá trình build Daily Brief, nếu data DB-1 + DB-2 cho thấy shift criteria của `framework-opvia-regime-v11.md` (Rule A/B/C/D mục 6.3 Custom Instructions) bị breach → tôi **auto-append một section "REGIME SHIFT ALERT"** ở cuối brief (sau Section 6).

### 5.1 Khi nào auto-flag

| Điều kiện trigger | Hành động |
|---|---|
| **Rule D Veto:** NHNN can thiệp FX > $5bn/tuần (proxy: USD/VND interbank mất giá > 1.5% trong 1 phiên + NHNN OMO net inject mạnh) | Auto-flag — R2/R3 call bị veto, cân nhắc R4 |
| **Rule D Veto:** Liên ngân hàng VN spike > 2x base (proxy: VN bond yield 10Y +50bps trong 1 phiên + NHNN withdraw mạnh) | Auto-flag — R1/R2 bị veto, cân nhắc R4/R5 |
| **Rule A breach minimum:** ≥ 2/3 layer breach trong DB-1 data | Auto-flag với note "shift cân nhắc, chưa xác nhận — chờ persistence" |
| **Step-function shock:** broker PDF mention chiến tranh / phong tỏa / cấm vận / NHNN policy emergency | Auto-flag — chuyển sang scenario riêng ngoài regime thông thường |

### 5.2 Format alert section

```
---
## ⚠ REGIME SHIFT ALERT (auto-triggered)

**Triggered by:** [variable(s) breach + threshold]
**Current regime:** Rx (ngày Y)
**Potential shift target:** Ry
**Persistence required:** [3 / 5 / 10 phiên theo Rule B]
**Cross-validation needed:** [layer 2 nào cần xác nhận]
**Handoff:** Chạy `workflow-regime-shift-alert` (Output Contract 6) để full alert format. Daily Brief chỉ flag, không generate full alert.
```

### 5.3 Handoff to workflow-regime-shift-alert

- Daily Brief KHÔNG tự generate full Contract 6 alert. Chỉ flag + handoff.
- `workflow-regime-shift-alert.md` chưa được build trong Phase 1 (Phase 2 deliverable theo Roadmap Focus_Brief mục 11). Trong Phase 1, handoff = note placeholder + analyst proceed manually.
- Khi Phase 2 ship `workflow-regime-shift-alert.md`, sửa handoff line thành "Tự động chuyển sang Contract 6 alert".

---

## 6. QUALITY CHECKLIST — 8-item pre-output

Tôi pass checklist này ngầm trước khi gửi brief. Pass im lặng, không báo cáo. Fail → sửa trước khi output.

| # | Check | Tiêu chí pass |
|---|---|---|
| 1 | **Verdict-first line** | Dòng đầu tiên có format `**Verdict:** Regime [Rx] (ngày Y, shelf life Z). Tâm thế: ...` |
| 2 | **6 sections theo đúng thứ tự** | Section 1 → 6 hiện diện đầy đủ, không đổi thứ tự, empty section render placeholder |
| 3 | **Tối thiểu 3 table** | Section 1, 2, 3 đều có table |
| 4 | **Length 500-800 từ** | Đếm từ tiếng Việt, không vượt 800 |
| 5 | **Regime call complete** | Có YYYY-MM-DD + shelf life + invalidation trigger |
| 6 | **Voice scan pass** | Không Vietlish (35 từ), không soft-tone (25 mẫu), không pseudo-precision (15 mẫu) |
| 7 | **No recommendation/price prediction leak** | Không câu nào đọc giống "nên mua/bán" hoặc "giá X sẽ đạt Y" |
| 8 | **Conflict + data gap flagged** | DB-1 vs DB-2 conflict → `[NGUỒN MÂU THUẪN]`. Indicator missing → `[DỮ LIỆU THIẾU: tên]` |

---

## 7. HANDOFF CONDITIONS — Khi nào chuyển workflow khác

Daily Brief là entry point cho cả phiên. Cuối brief, tôi propose 1 next-step nếu data đáng track sâu hơn. Không tự kích hoạt — analyst quyết.

| Điều kiện trong brief | Next-step suggest |
|---|---|
| Section 1 có shift probability "cao" | "Chạy `workflow-regime-shift-alert` (Contract 6) để full alert?" |
| Section 4 có thesis chuyển TRIGGERED hoặc BROKEN | "Re-run `workflow-pre-mortem` (Contract 5) cho thesis Y?" hoặc "Update `workflow-thesis-tracker` (Contract 4)?" |
| Section 6 có flag `[CREDIT EVENT]` hoặc `[NHNN INTERVENTION]` | "Deep-dive `workflow-cross-asset-linkage` (Contract 3) cho impact channel?" |
| Section 5 có earnings VN top 50 release hôm nay | "Pre-emptive `workflow-deep-dive` (Contract 2) cho ticker X?" |
| Brief bình thường, không signal đặc biệt | Không suggest next-step. Brief stand-alone. |

---

## 8. WORKED EXAMPLE — Daily Brief với giả dụ data

### 8.1 Input giả dụ analyst paste

**DB-1 (manual paste):**

```
| Indicator                     | Close            | Δ        | Nguồn           |
|-------------------------------|------------------|----------|-----------------|
| DXY                           | 105.2            | +0.4%    | TradingView     |
| UST 10Y yield                 | 4.62%            | +6 bps   | Investing       |
| Gold spot                     | 2,378 USD/oz     | -0.3%    | TradingView     |
| Brent crude                   | 78.40 USD/bbl    | -0.8%    | TradingView     |
| VN-Index close                | 1,242.5          | -0.6%    | HOSE            |
| USD/VND interbank             | 25,420           | +35 bps q| SBV             |
| NHNN OMO net hôm nay          | +15,000 VND bn   | bơm ròng | NHNN site       |
```

**DB-2 (Vietcap morning report PDF):** Section macro nói "DXY mạnh tiếp tục pressure VND, NHNN bơm OMO duy trì thanh khoản, FII rút ròng phiên thứ 4 liên tiếp ~280 tỷ VND". Section market view: "VN-Index sideways quanh 1,235-1,260 với hỗ trợ MA50, top picks hôm nay: HPG, FPT" (recommendation line — sẽ bị strip).

### 8.2 Output Daily Brief (giả dụ — minh họa format)

---

**Verdict:** Regime **R3 — Đỉnh chu kỳ / Quá nhiệt** (call 2026-04-19, shelf life 1-2 tuần, invalidate nếu DXY < 103 hoặc UST 10Y < 4.3% trong 5 phiên). Tâm thế hôm nay: **"Late cycle — don't chase"**, defensive rotation, earnings quality check.

#### Section 1 — Regime status

| Regime | Days held | Shift probability |
|---|---|---|
| R3 (Late Cycle / Overheating) | 8 phiên (từ 2026-04-11) | **Trung bình → cao** đối với R3→R4 (DXY firming + USD/VND pressure đang xác nhận tiến gần Rule D veto thresholds) |

Signpost theo dõi: DXY > 108 (hiện 105.2), UST 10Y > 5.0% (hiện 4.62%), NHNN can thiệp FX > $5bn/tuần (chưa, OMO inject thuần là cushion thanh khoản chứ chưa phải defend FX).

#### Section 2 — Overnight global drivers

| Indicator | Close | Δ | Diễn giải 1-dòng |
|---|---|---|---|
| DXY | 105.2 | +0.4% | DIỄN GIẢI: momentum hawkish duy trì, gần ngưỡng veto R3→R4 nếu break 108 |
| UST 10Y | 4.62% | +6 bps | DIỄN GIẢI: bid yields tiếp tục, term premium expanding [Bậc 2] |
| Gold | 2,378 | -0.3% | DIỄN GIẢI: real rate up + USD strength → headwind |
| Brent | 78.40 | -0.8% | DIỄN GIẢI: demand concern weighing, chưa breach mức $75 stress |

#### Section 3 — VN-specific overnight

| Indicator | Close | Δ | Diễn giải 1-dòng |
|---|---|---|---|
| USD/VND interbank | 25,420 | +35 bps q/q | DIỄN GIẢI: VND mất giá tiếp, đã accumulate ~1.4% q/q — gần ngưỡng cảnh báo 1.5% (Rule D veto soft trigger) |
| NHNN OMO net | +15,000 VND bn | bơm ròng | DIỄN GIẢI: cushion thanh khoản nội tệ trong khi siết kênh FX — pattern điển hình R3 |
| VN bond yield 10Y | 3.42% | +4 bps | DIỄN GIẢI: kéo theo UST anchor, chưa stress nội địa |

#### Section 4 — Open thesis status

`[KHÔNG CÓ THESIS MỞ]` — analyst chưa paste danh sách thesis active. Setup `workflow-thesis-tracker` để start tracking nếu cần.

#### Section 5 — Today's watchlist

- **CPI Mỹ Tháng 4** | 19:30 VN | Kết quả > 3.4% → confirm UST tiếp tục bid → R3→R4 acceleration.
- **HPG báo cáo Q1** (sau giờ giao dịch VN) | 17:00 VN | Quan sát biên gộp + leverage ratio (theo `domain-equity-vn-forensic-accounting.md` — Beneish M-score nếu earnings beat lớn).
- **OPEC+ JMMC meeting** | 21:00 VN | Surprise cut/extend → oil reverse > $82 sẽ pressure CPI VN.
- **NHNN tỷ giá trung tâm sáng** | 09:00 VN | Theo dõi nếu nâng > 24,200 → tín hiệu intervention escalation.

#### Section 6 — Risk flags mới (24h)

- `[FII OUTFLOW]` | FII rút ròng phiên thứ 4 liên tiếp (~280 tỷ VND theo Vietcap) | Implication: confirm risk-off rotation R3, signpost track nếu phiên 5-6 tiếp tục → R3→R4 cross-validation layer 2.
- `[NHNN INTERVENTION]` | NHNN OMO inject +15,000 VND bn (lớn nhất 2 tuần) | Implication: defensive liquidity cushion — chưa phải full FX defend nhưng tăng tracking.

---

#### ⚠ REGIME SHIFT ALERT (chưa trigger — early warning only)

**Triggered by:** USD/VND mất giá tích lũy 1.4% q/q (gần ngưỡng veto 1.5%) + FII outflow phiên 4/4 + NHNN OMO inject pattern R3 → R4 transition.

**Current regime:** R3 (call 2026-04-11)
**Potential shift target:** R4 (Tightening Stress / Capital Flight)
**Persistence required:** 3 phiên theo Rule B (R3↔R4 jumpy regime).
**Cross-validation needed:** Layer 2 = VN bond yield 10Y spike > +20bps trong 1 phiên (hiện chỉ +4bps), HOẶC NHNN can thiệp FX > $5bn/tuần (chưa breach).
**Handoff:** Chưa cần generate Contract 6 alert đầy đủ. Tracking 2-3 phiên tiếp theo. Nếu USD/VND breach 25,500 (≈ 1.6% q/q) hoặc bond 10Y > 3.6% → kích hoạt `workflow-regime-shift-alert` full Contract 6.

---

**Suggested next-step:** Setup `workflow-thesis-tracker` cho top 3 holding nếu OPVIA có position — R3 late-cycle là phase rủi ro cao nhất cho thesis dùng forward P/E. Hoặc chạy `workflow-cross-asset-linkage` cho cặp USD/VND ↔ VN-Index nếu muốn quantify pressure channel.

---

### 8.3 Word count check

Brief mẫu ở mục 8.2: ~720 từ (trong target 500-800). 4 table (Section 1, 2, 3, hard cap pass), 0 Vietlish leak, 0 recommendation leak (đã strip Vietcap top picks line), 0 price prediction. Regime call có ngày 2026-04-19 + shelf life 1-2 tuần + invalidation trigger 1 dòng. Auto-flag alert section append đúng theo Rule D veto early-warning pattern.

---

## 9. EDGE CASES — Tình huống đặc biệt

| Tình huống | Xử lý |
|---|---|
| Analyst paste DB-1 nhưng không upload DB-2 | Build brief DB-1-only mode. Section 5 watchlist ngắn hơn (chỉ event analyst note manual). Note 1 dòng cuối: "DB-2 missing — broker context không có, brief chỉ rely DB-1 data primary." |
| Analyst upload 3 broker PDF cùng lúc | Hỏi 1 câu pick 1: "Pick 1 broker PDF chính (recommend: Vietcap macro hoặc ACBS market microstructure). 2 PDF còn lại → reference only nếu cần cross-check?" Không tự merge 3 broker (broker bias mix risk). |
| Cuối tuần / ngày nghỉ thị trường | Daily Brief vẫn build được nếu analyst paste data global (DXY, UST, oil, gold cuối tuần Mỹ). Section 3 VN sẽ là "[THỊ TRƯỜNG VN NGHỈ]". Section 5 watchlist focus event tuần tới. |
| DB-1 paste sai format (table vỡ) | Tôi reformat ngầm theo template mục 2.1 nếu data còn parse được. Nếu không parse được → ask analyst re-paste với template chuẩn. Không guess. |
| Broker PDF tiếng Anh (ví dụ Vietcap English version) | Build brief tiếng Việt như bình thường (voice rule), trích dẫn quote tiếng Anh nếu giữ nguyên ngữ là quan trọng (rare). |
| Step-function shock detected (war/sanction/lockdown) | Auto-flag mục 5.2 alert, đồng thời append note: "Regime framework thông thường suspended — chuyển sang scenario riêng theo `core-research-protocol.md` mục step-function shock handling. Daily Brief sẽ thay đổi structure cho ngày tiếp theo." |
| Regime call nghi vấn (analyst push back "tôi nghĩ R2 chứ không R3") | Tôi không lùi tự động. Verdict-first line giữ regime call original + 1 dòng "analyst có view R2; cần data Y, Z để cross-validate" cuối Section 1. Không soft. |

---

## 10. VERSION + MAINTENANCE

- **Locked Phase 1:** Hybrid DB-1 + DB-2 input protocol, 6 fixed sections, 8-item quality checklist, 5 hard rules O1-O5, 9 trigger keywords, broker whitelist 5.
- **Open for revise sau Sprint 1-2 testing:** Threshold conflict DB-1 vs DB-2 (0.5%/20bps có thể quá tight nếu noise nhiều); broker whitelist (mở rộng/co lại); auto-flag thresholds (USD/VND 1.5% q/q, bond 10Y +50bps có thể cần re-calibrate).
- **Phase 2 deliverable:** `workflow-regime-shift-alert.md` (Contract 6 full) — khi ship, sửa handoff line ở mục 5.3.
- **Phase 3 consideration:** Nếu OPVIA migrate sang DB-3 (Python scraper auto-paste), DB-1 manual paste section trở thành fallback. Output structure không đổi.

---

**Hết workflow-daily-brief.md v1.0 (Wave 4 Lane 2).**

Tác giả: Wave 4 Lane 2 (Native Opus Executor).
Reference: Focus_Brief.md §6 Workflow 1 + §9 Contract 1; wave2-d-toolkit.md PART 3 Hybrid DB-1+DB-2; wave2-a-custom-instructions.md §4.1 Contract 1; custom-instructions.md §5.1 (production-locked); wave2-e1-regime-v11-draft.md (5-regime taxonomy + transition rules).
