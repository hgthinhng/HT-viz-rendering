---
name: opvia-publish
description: Orchestrator skill - pipeline xuất bản end-to-end cho mọi nội dung Opvia. LLM (Opus đang chạy skill này) đọc content, classify archetype (banking_regulatory, macro_monetary, sector_deep_dive, equity, fixed_income, fx, commodities, esg, ma, earnings, daily_report), decide pipeline (refine? viz? polish target?), rồi call orchestrator.py execute. Code Python chạy được programmatically (build_plan, execute_plan, render_pdf). Coordinate 4 child skills (opvia-content-refine, opvia-data-viz catalog 33+ component, opvia-DeepAnalysis-polish, opvia-DailyReport-polish). LUÔN dùng skill này khi user muốn pipeline đầy đủ end-to-end thay vì gọi từng skill riêng, hoặc khi user nói '/publish', 'opvia publish', 'xuất bản bài Opvia', 'biến thành PDF Opvia hoàn chỉnh', 'polish full pipeline', 'make Opvia PDF'. KHÔNG dùng khi user chỉ muốn 1 bước cụ thể (chỉ refine, chỉ build chart, chỉ polish layout đã có) - dùng child skill tương ứng.
---

# Opvia Publish - Orchestrator Skill

Skill điều phối pipeline xuất bản Opvia end-to-end. Triết lý 2 tầng:

- **Judgement tầng LLM (Opus)**: đọc content, phân loại archetype, quyết định pipeline. Đây là chỗ tôi (LLM) làm.
- **Execution tầng Python (`orchestrator.py`)**: nhận decision dict từ tôi, call đúng child skills, render PDF.

`orchestrator.py` không còn detect/recommend bằng regex - LLM làm việc đó. Code chỉ thực thi quyết định, validate, render.

---

## Workflow

```
1. RECEIVE: nhận content từ user.
2. JUDGE: tôi (LLM) đọc content, decide:
   - archetype: banking_regulatory | macro_monetary | sector_deep_dive |
                equity_single_stock | fixed_income | fx_currency | commodities |
                esg | ma_corporate_action | earnings_review | daily_report
   - polish_target: "deep" | "daily"
   - refine_action: "skip" | "suggest" | "strong_suggest" (xem có nhiều Vietlish không)
   - viz_plan: list[dict] - components + sequence + params
3. PLAN: build PipelinePlan từ decision dict.
4. CONFIRM: show plan cho user (skip nếu skip_confirm=True).
5. EXECUTE: call orchestrator.execute_plan() để build HTML + render PDF.
6. DELIVER: PDF + plan summary.
```

---

## Judgement guide cho LLM

### Step 1 - Classify archetype

Đọc content, identify dạng bài. Cụ thể tham khảo:

| Archetype | Signals điển hình |
|---|---|
| `banking_regulatory` | "Thông tư", "LDR", "NSFR", "SFL", "CAR", regulatory threshold, bank tickers |
| `macro_monetary` | GDP, CPI, FX, "lãi suất chính sách", Fed, SBV, monetary cycle |
| `sector_deep_dive` | "ngành thép/bán lẻ/BĐS/...", peer comparison, sector rotation |
| `equity_single_stock` | 1 ticker focal, valuation, catalyst, target price |
| `fixed_income` | yield, spread, TPCP, duration, credit rating |
| `fx_currency` | USD/VND, DXY, REER, intervention, cross rate |
| `commodities` | dầu/vàng/nông sản, futures curve, contango, inventory |
| `esg` | ESG score, scope emissions, materiality, sustainability |
| `ma_corporate_action` | acquirer/target, premium, synergy, accretion-dilution |
| `earnings_review` | quarterly results, beat/miss, segment, guidance |
| `daily_report` | "phiên", "VN-Index", "khối ngoại mua/bán ròng", "thanh khoản", section 01/02/03 |

Đọc `archetypes/<name>/README.md` của child skill `opvia-data-viz` để xem chart families + composition pattern.

### Step 2 - Pick polish_target

- `daily_report` archetype → `polish_target = "daily"` (opvia-DailyReport-polish)
- Mọi archetype khác → `polish_target = "deep"` (opvia-DeepAnalysis-polish)

### Step 3 - Decide refine_action

Đọc content, đếm Vietlish (từ vay mượn AI-style không cần thiết).

Red flags điển hình: "force", "leverage", "compression", "headroom", "trade-off", "stakeholder", "outlook", "momentum", "consolidation", "breakout", "overcome", "address", "navigate", "robust", "compelling", "significant", "underscore", "highlight" (động từ).

Whitelist (KHÔNG count - thuật ngữ chuyên môn): LDR, NSFR, CASA, Big4, Basel, NIM, P/E, P/B, EPS, bps, M&A, IPO, FDI, TPCP, TPDN, SFL, TT2, TGKB, Fed, DXY, CPI, GDP, FX, ROE, ROA, EBITDA, WACC, NPV, IRR.

Rules:
- 0-2 từ red flag → `refine_action = "skip"`
- 3-7 từ → `refine_action = "suggest"` (đề xuất user chạy refine trước)
- 8+ từ → `refine_action = "strong_suggest"`

### Step 3.5 - Cover + CTA metadata (bắt buộc)

Mọi bài publish-ready phải có cover (page 1) + back cover CTA (page cuối). LLM extract metadata từ content + provide cho polish skill render template.

**Cover metadata:**

```python
"cover": {
    "sub_brand": "Ngân hàng & Vĩ mô",            # eyebrow trái
    "issue": "Số tháng 4 · 2026",                 # eyebrow phải
    "title": "Đề xuất sửa đổi Thông tư 22/2019",  # 8-12 từ ngắn gọn
    "subtitle": "Ai hưởng lợi, ai chịu thiệt?",
    "dek": "Khi LDR hệ thống chạm 111,9%...",     # 50-80 từ
    "hero_number": "111,9%",                      # mega stat signature
    "hero_label": "TỶ LỆ LDR HỆ THỐNG · 30/3/2026",
    "hero_desc": "Mức cao kỷ lục, vượt xa trần quy chế 85%...",
    "takeaways": [
        {"lead": "Tái phân phối, không phải nới lỏng.",
         "detail": "Sửa Thông tư 22 là chỉnh quy tắc kỹ thuật..."},
        {"lead": "Hai phương án Điều 16 cho kết quả ngược nhau.",
         "detail": "Nới SFL 35% hay thay NSFR..."},
        {"lead": "Lợi ích phân phối bất đối xứng.",
         "detail": "Big4 hưởng lợi gấp đôi. Nhóm C thiệt 12-24 nghìn tỷ..."},
    ],
    "author": "OPVIA Academy",
    "read_time_min": 14,
    "publish_date": "25/04/2026",
}
```

**Back cover CTA metadata:**

```python
"back_cover": {
    # Per-bài (LLM fill từ content)
    "sources": "Phân tích dựa trên đề xuất sửa đổi Thông tư 22/2019...",
    "title_short": "ĐỀ XUẤT SỬA ĐỔI THÔNG TƯ 22",   # uppercase footer

    # Default Opvia (polish skill hardcode, LLM không cần fill):
    # cta_eyebrow, cta_title, cta_body, contact_email, contact_website,
    # contact_book, disclaimer
}
```

Daily report skip `cover` (header gọn polish skill đủ), vẫn cần `back_cover` compact (gộp source + disclaimer thành footer 6-8 dòng).

Xem catalog spec: `opvia-data-viz/catalog/cover_deep_page.md`, `opvia-data-viz/catalog/back_cover_cta.md`.

### Step 4 - Build viz_plan

Skim `catalog/INDEX.md` của opvia-data-viz, shortlist 5-10 component matching content. Deep-read 5-10 spec. Compose sequence theo composition pattern của archetype tương ứng.

`viz_plan` là list[dict], mỗi dict:

```python
{
    "component": "gauge",           # tên function trong viz/viz_wave8/9/10
    "module": "viz",                # "viz" | "viz_wave8" | "viz_wave9" | "viz_wave10"
    "wave": "1-3",                  # hoặc "8" | "9" | "10"
    "position": "open_section_1",   # vị trí trong bài
    "params": {                     # kwargs cho component function
        "value": 111.9,
        "max_val": 120,
        "threshold": 85,
        "label": "LDR hệ thống",
        "danger_above": True,
    },
    "annotation": "Mega number mở Phần I",   # context cho execution layer
}
```

Frequency budget: bài deep ~10-15 viz, daily report ~1-3 viz. Composite (Wave 10) max 2-3 per bài.

---

## Cách dùng (3 modes)

### Mode A - Quick: 1 lệnh từ content sang PDF

```python
import sys
sys.path.insert(0, "/path/to/opvia-publish")
from orchestrator import publish

# LLM (tôi) decide trước, pass decision dict
decision = {
    "archetype": "banking_regulatory",
    "polish_target": "deep",
    "refine_action": "suggest",
    "viz_plan": [
        {"component": "gauge", "module": "viz", "wave": "1-3", "position": "open_phan_1", "params": {...}},
        {"component": "dot_plot_distribution", "module": "viz_wave8", "wave": "8", "position": "phan_2", "params": {...}},
        # ...
    ],
    "title": "Đề xuất sửa đổi Thông tư 22",
    "date_str": "29/04/2026",
}

content = open("noidung.md").read()
pdf_path, plan = publish(content, decision, output_dir="/path/to/outputs", skip_confirm=True)
print(f"PDF: {pdf_path}")
print(plan.summary())
```

### Mode B - Plan first: build plan trước, render sau

```python
from orchestrator import build_plan, execute_plan

plan = build_plan(content, decision, output_dir="/path/to/outputs")
print(plan.summary())   # show LLM decision + planned viz sequence

# User confirm, có thể adjust...
if user_confirms:
    pdf_path = execute_plan(plan, content)
```

### Mode C - Programmatic: dùng PipelinePlan dataclass trực tiếp

```python
from orchestrator import PipelinePlan, execute_plan

plan = PipelinePlan(
    archetype="banking_regulatory",
    polish_target="deep",
    refine_action="skip",
    viz_plan=[...],
    title="...",
    date_str="29/04/2026",
    output_dir="/path/to/outputs",
)
pdf_path = execute_plan(plan, content)
```

---

## Architecture - các functions chính

```python
@dataclass
class PipelinePlan:
    archetype: str              # "banking_regulatory" | "macro_monetary" | ... | "daily_report"
    polish_target: str          # "deep" | "daily"
    refine_action: str          # "skip" | "suggest" | "strong_suggest"
    viz_plan: list[dict]        # ordered list of viz components
    title: str
    date_str: str               # "DD/MM/YYYY"
    output_dir: str
    word_count: int = 0
    output_filename: str = ""

    def summary(self) -> str:   # human-readable plan

def build_plan(content: str, decision: dict, output_dir: str) -> PipelinePlan:
    """Construct PipelinePlan từ LLM decision dict + content metadata."""

def execute_plan(plan: PipelinePlan, content: str) -> str:
    """Build HTML body, inject viz, apply CSS từ polish_target, render PDF."""

def publish(content: str, decision: dict, output_dir: str,
            skip_confirm: bool = False) -> tuple[str, PipelinePlan]:
    """Quick mode: build_plan + (optional confirm) + execute_plan."""
```

---

## Patterns quan trọng

### Pattern 1: Module cache reset

Cả `opvia-DailyReport-polish` và `opvia-DeepAnalysis-polish` đều export module tên `render`. Switch giữa 2 pipelines phải reset cache:

```python
for mod_name in list(sys.modules.keys()