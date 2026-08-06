"""
StockLPT Publish Orchestrator (LLM-driven)
========================================

Single entry point cho pipeline xuất bản StockLPT.

Triết lý 2 tầng:
- Judgement (LLM = Opus chạy skill này): đọc content, classify archetype,
  decide polish_target, decide refine_action, build viz_plan với params + sequence.
- Execution (Python = file này): nhận decision dict, build HTML, inject viz,
  apply CSS từ polish skill, render qua WeasyPrint.

Code KHÔNG còn detect/recommend bằng regex - LLM làm việc đó.
File này chỉ thực thi quyết định, validate, render.

Usage:
    from orchestrator import publish

    decision = {
        "archetype": "banking_regulatory",
        "polish_target": "deep",
        "refine_action": "suggest",
        "viz_plan": [
            {
                "component": "gauge",
                "module": "viz",
                "wave": "1-3",
                "position": "open_phan_1",
                "params": {
                    "value": 111.9, "max_val": 120, "threshold": 85,
                    "label": "LDR hệ thống", "danger_above": True,
                },
            },
            # ... thêm viz khác
        ],
        "title": "Đề xuất sửa đổi Thông tư 22",
        "date_str": "29/04/2026",
    }

    pdf_path, plan = publish(content, decision, output_dir="/path/to/outputs")
"""
from __future__ import annotations
import importlib
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Literal


# ============================================================
# SKILL PATH RESOLUTION
# ============================================================

def _find_skills_base() -> str:
    """Locate skill base directory chứa các skill folders StockLPT."""
    candidates = [
        "/mnt/skills/user",
        os.path.expanduser("~/skills/user"),
        os.path.expanduser("~/.claude/skills"),
        "/home/claude/full_skill_update",
        # Cowork mode skills-plugin path (Windows mount)
        os.path.expanduser(
            "~/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin"
        ),
    ]
    # Explicit override (highest priority)
    env_base = os.environ.get("STOCKLPT_SKILLS_BASE")
    if env_base:
        candidates.insert(0, env_base)
    # Also try walking up from this file location
    here = Path(__file__).resolve().parent
    for parent in [here.parent, here.parent.parent]:
        candidates.insert(0, str(parent))

    for c in candidates:
        p = Path(c)
        if p.is_dir() and (p / "stocklpt-data-viz").is_dir():
            return str(p)

    raise RuntimeError(
        "Cannot find skill base directory. Tried: " + ", ".join(candidates)
    )


SKILLS_BASE = _find_skills_base()
DATA_VIZ_PATH = os.path.join(SKILLS_BASE, "stocklpt-data-viz")
DEEP_POLISH_PATH = os.path.join(SKILLS_BASE, "stocklpt-deepanalysis-polish")
DAILY_POLISH_PATH = os.path.join(SKILLS_BASE, "stocklpt-dailyreport-polish")

# Add to sys.path để import được data-viz module ngay
if DATA_VIZ_PATH not in sys.path:
    sys.path.insert(0, DATA_VIZ_PATH)


# ============================================================
# STOCKLPT BRAND (native)
# ============================================================
# Brand layer sống trong stocklpt-data-viz/_brand.py. Orchestrator chỉ cần
# set brand (env live) TRƯỚC khi execute_plan → render_pdf remap HTML cuối.
try:
    from _brand import (  # noqa: E402
        current_brand, set_brand, list_brands, get_brand,
    )
    BRANDS = set(list_brands())
    _BRAND_ENGINE = True
except Exception:  # pragma: no cover - fallback nếu engine vắng mặt
    BRANDS = {"stocklpt", "stocklpt"}
    _BRAND_ENGINE = False

    def set_brand(key: str):  # type: ignore
        os.environ["STOCKLPT_BRAND"] = (key or "stocklpt").strip().lower()

    def current_brand():  # type: ignore
        class _Stub:
            key = os.environ.get("STOCKLPT_BRAND", "stocklpt").strip().lower() or "stocklpt"
            display_name = "StockLPT" if key == "stocklpt" else key.title()
            filename_prefix = "STOCKLPT" if key == "stocklpt" else key.upper()
        return _Stub()

    def get_brand(key: str):  # type: ignore
        return current_brand()


# ============================================================
# ALLOWED VALUES
# ============================================================

ARCHETYPES = {
    "banking_regulatory", "macro_monetary", "sector_deep_dive",
    "equity_single_stock", "fixed_income", "fx_currency",
    "commodities", "esg", "ma_corporate_action", "earnings_review",
    "daily_report",
}

POLISH_TARGETS = {"deep", "daily"}

REFINE_ACTIONS = {"skip", "suggest", "strong_suggest"}

VIZ_MODULES = {"viz", "viz_wave8", "viz_wave9", "viz_wave10", "viz_charts", "viz_daily", "viz_institutional"}


# ============================================================
# PIPELINE PLAN DATACLASS
# ============================================================

@dataclass
class PipelinePlan:
    archetype: str
    polish_target: Literal["deep", "daily"]
    refine_action: Literal["skip", "suggest", "strong_suggest"]
    viz_plan: list[dict] = field(default_factory=list)
    cover: dict = field(default_factory=dict)         # cover metadata (xem catalog/cover_deep_page.md)
    back_cover: dict = field(default_factory=dict)    # back cover CTA metadata (xem catalog/back_cover_cta.md)
    title: str = ""
    short_title: str = ""
    date_str: str = ""
    output_dir: str = ""
    word_count: int = 0
    output_filename: str = ""
    brand: str = "stocklpt"                              # brand cố định: StockLPT

    def summary(self) -> str:
        """Human-readable plan."""
        try:
            brand_label = get_brand(self.brand).display_name
        except Exception:
            brand_label = self.brand
        lines = [
            "=" * 60,
            "STOCKLPT PUBLISH - PIPELINE PLAN",
            "=" * 60,
            "",
            f"BRAND: {brand_label} ({self.brand})",
            f"ARCHETYPE: {self.archetype}",
            f"POLISH TARGET: {self.polish_target}",
            f"WORD COUNT: {self.word_count:,}",
            f"REFINE ACTION: {self.refine_action}",
            "",
        ]

        if self.viz_plan:
            lines.append(f"VIZ PLAN ({len(self.viz_plan)} components):")
            for i, v in enumerate(self.viz_plan, 1):
                pos = v.get("position", "")
                annotation = v.get("annotation", "")
                lines.append(
                    f"  {i:2d}. {v['component']:<28} ({v['module']}) "
                    f"@ {pos[:20]:<20} {annotation[:40]}"
                )
            lines.append("")

        lines.append(f"TITLE: {self.title}")
        lines.append(f"DATE: {self.date_str}")
        lines.append(f"OUTPUT: {self.output_filename}")
        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


# ============================================================
# DECISION VALIDATION
# ============================================================

def _validate_decision(decision: dict) -> None:
    """Raise ValueError nếu decision dict thiếu field hoặc value không hợp lệ."""
    required = {"archetype", "polish_target", "refine_action"}
    missing = required - set(decision.keys())
    if missing:
        raise ValueError(f"decision dict thiếu field: {missing}")

    if decision["archetype"] not in ARCHETYPES:
        raise ValueError(
            f"archetype '{decision['archetype']}' không hợp lệ. "
            f"Allowed: {sorted(ARCHETYPES)}"
        )
    if decision["polish_target"] not in POLISH_TARGETS:
        raise ValueError(
            f"polish_target '{decision['polish_target']}' không hợp lệ. "
            f"Allowed: {sorted(POLISH_TARGETS)}"
        )
    if decision["refine_action"] not in REFINE_ACTIONS:
        raise ValueError(
            f"refine_action '{decision['refine_action']}' không hợp lệ. "
            f"Allowed: {sorted(REFINE_ACTIONS)}"
        )

    # brand (optional, default 'stocklpt')
    brand = decision.get("brand", "stocklpt")
    if brand not in BRANDS:
        raise ValueError(
            f"brand '{brand}' không hợp lệ. Allowed: {sorted(BRANDS)}"
        )

    # Sanity: daily_report archetype phải đi với polish_target=daily
    if decision["archetype"] == "daily_report" and decision["polish_target"] != "daily":
        raise ValueError(
            "archetype='daily_report' phải đi với polish_target='daily'."
        )

    # viz_plan validation
    for i, v in enumerate(decision.get("viz_plan", [])):
        if "component" not in v or "module" not in v:
            raise ValueError(f"viz_plan[{i}] thiếu 'component' hoặc 'module'.")
        if v["module"] not in VIZ_MODULES:
            raise ValueError(
                f"viz_plan[{i}].module '{v['module']}' không hợp lệ. "
                f"Allowed: {sorted(VIZ_MODULES)}"
            )


# ============================================================
# HELPERS
# ============================================================

def _slugify(text: str, max_len: int = 40) -> str:
    """Slug VN-friendly cho filename."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").upper()
    return text[:max_len]


def _extract_title(content: str) -> str:
    """Extract title từ markdown heading hoặc first line."""
    lines = content.strip().split("\n")
    for line in lines[:10]:
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
        if line and len(line) > 10 and not line.startswith("---"):
            return line
    try:
        return f"{current_brand().filename_prefix}_REPORT"
    except Exception:
        return "STOCKLPT_REPORT"


def _today_str() -> str:
    return date.today().strftime("%d/%m/%Y")


# ============================================================
# BUILD PLAN
# ============================================================

def build_plan(
    content: str,
    decision: dict,
    output_dir: str = "/mnt/user-data/outputs",
) -> PipelinePlan:
    """
    Construct PipelinePlan từ LLM decision dict + content metadata.

    decision: dict với keys:
        - archetype (required)
        - polish_target (required)
        - refine_action (required)
        - viz_plan (optional, default [])
        - title (optional, sẽ extract từ content nếu thiếu)
        - date_str (optional, default today DD/MM/YYYY)
    """
    _validate_decision(decision)

    # Set active brand EARLY (env live) — phải xảy ra trước khi extract title
    # (title fallback brand-aware) và trước filename prefix. execute_plan sẽ
    # re-affirm từ plan.brand để render_pdf remap đúng brand.
    brand_key = decision.get("brand", "stocklpt")
    set_brand(brand_key)
    try:
        brand_prefix = current_brand().filename_prefix
    except Exception:
        brand_prefix = "STOCKLPT"

    title = decision.get("title") or _extract_title(content)
    short_title = decision.get("short_title") or title.split(" - ")[0].split(":")[0].strip()[:34]
    date_str = decision.get("date_str") or _today_str()
    word_count = len(content.split())

    # Generate filename từ title + today date (brand-prefixed)
    slug = _slugify(title)
    today_iso = date.today().strftime("%Y%m%d")
    filename = f"{brand_prefix}_{slug}_{today_iso}.pdf"
    output_path = os.path.join(output_dir, filename)

    return PipelinePlan(
        archetype=decision["archetype"],
        polish_target=decision["polish_target"],
        refine_action=decision["refine_action"],
        viz_plan=decision.get("viz_plan", []),
        cover=decision.get("cover", {}),
        back_cover=decision.get("back_cover", {}),
        title=title,
        short_title=short_title,
        date_str=date_str,
        output_dir=output_dir,
        word_count=word_count,
        output_filename=output_path,
        brand=brand_key,
    )


# ============================================================
# VIZ RENDER FROM PLAN
# ============================================================

def _render_viz_from_plan(viz_plan: list[dict]) -> dict[str, str]:
    """
    Loop viz_plan, dynamically import + call component function với params.
    Return dict {position: html_string} - LLM có thể inject vào content via
    placeholder syntax `<!-- viz:<position> -->`.

    Nếu position trùng nhau, append HTML.
    """
    rendered = {}
    for i, v in enumerate(viz_plan):
        module_name = v["module"]
        component = v["component"]
        params = v.get("params", {})
        position = v.get("position", f"viz_{i}")

        try:
            mod = importlib.import_module(module_name)
        except ImportError as e:
            raise RuntimeError(
                f"viz_plan[{i}] không import được module '{module_name}': {e}"
            )

        if not hasattr(mod, component):
            raise RuntimeError(
                f"viz_plan[{i}] module '{module_name}' không có function '{component}'."
            )

        func = getattr(mod, component)
        try:
            html = func(**params)
        except TypeError as e:
            raise RuntimeError(
                f"viz_plan[{i}] {component}(**params) lỗi signature: {e}"
            )

        if position in rendered:
            rendered[position] += "\n" + html
        else:
            rendered[position] = html
    return rendered


def _inject_viz_placeholders(body: str, viz_html: dict[str, str]) -> str:
    """
    Replace `<!-- viz:<position> -->` placeholder trong body với HTML rendered.
    Placeholder không match thì để nguyên (LLM có thể warn).
    Viz không có placeholder thì append cuối body.
    """
    used = set()
    pattern = re.compile(r"<!--\s*viz:([\w_-]+)\s*-->")

    def replace(m):
        pos = m.group(1)
        if pos in viz_html:
            used.add(pos)
            return viz_html[pos]
        return m.group(0)  # leave unmatched

    body = pattern.sub(replace, body)

    # Append unused viz cuối body
    unused = [pos for pos in viz_html if pos not in used]
    if unused:
        appended = "\n".join(viz_html[pos] for pos in unused)
        body += "\n<!-- auto-appended viz (no placeholder match) -->\n" + appended

    return body


# ============================================================
# BUILD BODY FROM MARKDOWN
# ============================================================

def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render_md_table(rows: list) -> str:
    """rows: list raw '| a | b |' (đã loại dòng phân cách |---|)."""
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    if not cells:
        return ""
    head, body = cells[0], cells[1:]
    thead = "".join(f"<th>{_esc(h)}</th>" for h in head)
    trows = "".join("<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<table class="lpt-table"><thead><tr>{thead}</tr></thead><tbody>{trows}</tbody></table>'


def _build_toc(content: str) -> str:
    """TOC tự sinh từ heading '## ' (chỉ khi >=3 mục)."""
    heads = [l.strip()[3:].strip() for l in content.split("\n") if l.strip().startswith("## ")]
    if len(heads) < 3:
        return ""
    items = "".join(
        f'<li><span class="toc-n">{i:02d}</span><span class="toc-t">{_esc(h)}</span></li>'
        for i, h in enumerate(heads, 1)
    )
    return (
        "<style>"
        ".lpt-toc{page-break-after:always;padding:8mm 0 0;}"
        ".lpt-toc .toc-h{font-family:'PFD','PFDVN',serif;font-size:22pt;color:#2A1A4A;font-weight:700;margin:0 0 9mm;border:none;}"
        ".lpt-toc ol{list-style:none;padding:0;margin:0;}"
        ".lpt-toc li{display:flex;align-items:baseline;gap:7mm;padding:4.2mm 0;border-top:0.6px solid rgba(42,26,74,0.14);}"
        ".lpt-toc li:last-child{border-bottom:0.6px solid rgba(42,26,74,0.14);}"
        ".lpt-toc .toc-n{font-family:'JBM','JBMVN',monospace;font-size:11pt;color:#16633C;font-weight:600;}"
        ".lpt-toc .toc-t{font-family:'PFD','PFDVN',serif;font-size:13pt;color:#221A34;}"
        "</style>"
        f'<section class="lpt-toc"><div class="toc-h">Mục lục</div><ol>{items}</ol></section>'
    )


def _build_cover(c: dict) -> str:
    """Cover trang 1 generic từ metadata plan.cover (editorial light, StockLPT native)."""
    if not c:
        return ""
    eyebrow = " · ".join(x for x in [c.get("sub_brand", ""), c.get("issue", "")] if x)
    foot = " · ".join(x for x in [c.get("author", ""), c.get("publish_date", "")] if x)
    hero = ""
    if c.get("hero_number"):
        hero = (
            f'<div class="cv2-hero"><div class="cv2-num">{_esc(c["hero_number"])}</div>'
            f'<div class="cv2-hl">{_esc(c.get("hero_label",""))}</div>'
            f'<div class="cv2-hd">{_esc(c.get("hero_desc",""))}</div></div>'
        )
    return (
        "<style>"
        "@page :first { margin:0; @top-center{content:none;border:none;} @bottom-left{content:none;border:none;} @bottom-right{content:none;border:none;} }"
        ".cv2{page-break-after:always;background:#F4F6F9;margin:0 -24mm;min-height:289mm;padding:30mm 26mm 22mm;"
        "display:flex;flex-direction:column;justify-content:space-between;font-family:'Inter','InterVN',sans-serif;}"
        ".cv2-eyebrow{font-size:8.5pt;letter-spacing:0.16em;text-transform:uppercase;color:#16633C;font-weight:600;"
        "border-bottom:1px solid rgba(42,26,74,0.18);padding-bottom:7mm;}"
        ".cv2-title{font-family:'PFD','PFDVN',serif;font-size:37pt;line-height:1.08;color:#2A1A4A;font-weight:700;margin:0 0 6mm;letter-spacing:-0.01em;}"
        ".cv2-sub{font-family:'PFD','PFDVN',serif;font-size:16pt;font-style:italic;color:#645B76;margin-bottom:9mm;}"
        ".cv2-dek{font-size:11.5pt;line-height:1.62;color:#221A34;max-width:150mm;}"
        ".cv2-hero{border-top:1px solid rgba(42,26,74,0.18);padding-top:9mm;}"
        ".cv2-num{font-family:'PFD','PFDVN',serif;font-size:52pt;line-height:0.9;color:#C8972E;font-weight:700;}"
        ".cv2-hl{font-size:8.5pt;letter-spacing:0.12em;text-transform:uppercase;color:#645B76;margin-top:3mm;}"
        ".cv2-hd{font-size:10.5pt;color:#221A34;margin-top:2mm;max-width:140mm;line-height:1.5;}"
        ".cv2-foot{font-size:9pt;letter-spacing:0.06em;color:#645B76;border-top:1px solid rgba(42,26,74,0.18);padding-top:6mm;}"
        "</style>"
        f'<section class="cv2"><div class="cv2-eyebrow">{_esc(eyebrow)}</div>'
        f'<div><div class="cv2-title">{_esc(c.get("title",""))}</div>'
        f'<div class="cv2-sub">{_esc(c.get("subtitle",""))}</div>'
        f'<div class="cv2-dek">{_esc(c.get("dek",""))}</div></div>'
        f'{hero}<div class="cv2-foot">{_esc(foot)}</div></section>'
    )


def _build_body_from_markdown(content: str) -> str:
    """
    Convert markdown content thành HTML body cơ bản.
    Headings -> h1/h2/h3, list bullets -> ul/li, paragraphs -> p.
    Bold **text** -> <strong>.
    """
    lines = content.strip().split("\n")
    html_parts = []
    in_list = False
    table_buf = []

    def _flush_table():
        if table_buf:
            html_parts.append(_render_md_table(table_buf))
            table_buf.clear()

    for line in lines:
        line_stripped = line.strip()
        # pipe-table rows
        if line_stripped.startswith("|") and line_stripped.endswith("|"):
            if set(line_stripped) <= set("|-: "):
                continue  # separator row |---|
            table_buf.append(line_stripped)
            continue
        _flush_table()
        if not line_stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        # Preserve viz placeholder comments
        if line_stripped.startswith("<!--") and line_stripped.endswith("-->"):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(line_stripped)
            continue

        if line_stripped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h3>{line_stripped[4:].strip()}</h3>")
        elif line_stripped.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{line_stripped[3:].strip()}</h2>")
        elif line_stripped.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{line_stripped[2:].strip()}</h1>")
        elif line_stripped.startswith("- ") or line_stripped.startswith("* "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{line_stripped[2:].strip()}</li>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            line_stripped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line_stripped)
            html_parts.append(f"<p>{line_stripped}</p>")

    if in_list:
        html_parts.append("</ul>")
    _flush_table()

    return "\n".join(html_parts)


# ============================================================
# EXECUTE PLAN
# ============================================================

def _setup_polish_path(polish_target: str) -> str:
    """Setup sys.path cho polish skill, reset cache giữa daily/deep."""
    if polish_target == "daily":
        polish_path = DAILY_POLISH_PATH
        other_path = DEEP_POLISH_PATH
    else:
        polish_path = DEEP_POLISH_PATH
        other_path = DAILY_POLISH_PATH

    # Remove other polish path nếu đang trong sys.path
    if other_path in sys.path:
        sys.path.remove(other_path)
    # Re-insert this polish path priority đầu
    if polish_path in sys.path:
        sys.path.remove(polish_path)
    sys.path.insert(0, polish_path)

    # Force re-import render module (cả 2 polish skill đều có module 'render')
    for mod_name in list(sys.modules.keys()):
        if mod_name in ("render", "covers", "section_openers", "extras"):
            del sys.modules[mod_name]

    return polish_path


def _build_css(plan: PipelinePlan) -> str:
    """Build full CSS chain: polish base + viz styles wave 1-10."""
    if plan.polish_target == "daily":
        from render import build_full_css   # noqa
        css = build_full_css(date_str=plan.date_str)
    else:
        from render import build_full_css   # noqa
        css = build_full_css(
            date_str=plan.date_str,
            short_title=(plan.short_title or plan.title),
        )

    # Add viz styles - tất cả waves (cheap, prevents missing-style bugs)
    style_imports = [
        ("viz", "viz_styles"),
        ("viz_wave8", "wave8_styles"),
        ("viz_wave9", "wave9_styles"),
        ("viz_wave10", "wave10_styles"),
        ("viz_charts", "chart_styles"),
    ]
    for module_name, fn_name in style_imports:
        try:
            mod = importlib.import_module(module_name)
            fn = getattr(mod, fn_name, None)
            if fn:
                css = css + "\n" + fn()
        except ImportError:
            pass

    return css


def execute_plan(plan: PipelinePlan, content: str) -> str:
    """
    Execute plan. Build HTML body, render qua appropriate polish skill, return PDF path.

    Pipeline:
    1. Setup polish path (daily vs deep) + reset module cache.
    2. Build CSS = polish base + all viz styles.
    3. Render viz components from plan.viz_plan.
    4. Build HTML body from content markdown + inject viz.
    5. Validate body via validators (no em-dash, palette, font, VN numbers).
    6. Wrap in full HTML doc + render PDF via WeasyPrint.
    """
    _setup_polish_path(plan.polish_target)
    # Re-affirm brand từ plan (env live) — đảm bảo validators (pre-remap) dùng
    # union allow-list đúng và render_pdf remap đúng brand kể cả khi execute_plan
    # được gọi trực tiếp (không qua build_plan).
    set_brand(plan.brand)
    css = _build_css(plan)

    viz_html_by_position = _render_viz_from_plan(plan.viz_plan) if plan.viz_plan else {}

    body = _build_body_from_markdown(content)
    if viz_html_by_position:
        body = _inject_viz_placeholders(body, viz_html_by_position)

    # Scaffolding tự động từ plan.cover:
    #  - cover.masthead / cover.exec  -> research_masthead + exec_brief (deep & daily)
    #  - cover thường (deep)          -> generic cover + TOC tự sinh
    header_html = ""
    if plan.cover:
        _mh = plan.cover.get("masthead"); _ex = plan.cover.get("exec")
        if _mh or _ex:
            _vi = importlib.import_module("viz_institutional")
            if _mh:
                header_html += _vi.research_masthead(**_mh)
            if _ex:
                header_html += _vi.exec_brief(**_ex)
        elif plan.polish_target == "deep":
            header_html += _build_cover(plan.cover) + _build_toc(content)
    body = header_html + body

    body_wrapped = '<div class="content">\n' + body + '\n</div>'

    try:
        from validators import validate_html
        errors = validate_html(body_wrapped)
        if errors:
            print("Validators flagged:")
            for e in errors[:10]:
                print(f"  - {e}")
    except ImportError:
        pass

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="vi">\n'
        '<head><meta charset="UTF-8"><style>'
        + css +
        '</style></head>\n'
        '<body>' + body_wrapped + '</body>\n'
        '</html>\n'
    )

    output_path = plan.output_filename
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    from render import render_pdf
    render_pdf(html, output_path, strict=False)

    return output_path


# ============================================================
# QUICK MODE
# ============================================================

def publish(
    content: str,
    decision: dict,
    output_dir: str = "/mnt/user-data/outputs",
    skip_confirm: bool = True,
):
    """Quick mode - 1 lenh tu content + decision sang PDF.

    Returns: (pdf_path, plan_used)
    """
    plan = build_plan(content, decision, output_dir=output_dir)

    if not skip_confirm:
        print(plan.summary())
        response = input("Proceed? [Y/n] ").strip().lower()
        if response and response != "y":
            raise RuntimeError("User aborted")

    pdf_path = execute_plan(plan, content)
    return pdf_path, plan


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="StockLPT Publish Orchestrator (LLM-driven)"
    )
    parser.add_argument("input_file", help="Path to content markdown/text file")
    parser.add_argument(
        "--decision-file",
        required=True,
        help="JSON file chua decision dict",
    )
    parser.add_argument(
        "--output-dir", default="/mnt/user-data/outputs",
        help="Output directory cho PDF",
    )
    parser.add_argument(
        "--plan-only", action="store_true",
        help="Build plan + print summary, khong render",
    )
    parser.add_argument(
        "--skip-confirm", action="store_true",
        help="Skip confirmation prompt",
    )
    parser.add_argument(
        "--brand", default=None,
        help="Brand cố định StockLPT (cờ giữ để tương thích).",
    )

    args = parser.parse_args()

    content = Path(args.input_file).read_text(encoding="utf-8")
    decision = json.loads(Path(args.decision_file).read_text(encoding="utf-8"))
    if args.brand:
        decision["brand"] = args.brand.strip().lower()

    if args.plan_only:
        plan = build_plan(content, decision, output_dir=args.output_dir)
        print(plan.summary())
    else:
        pdf_path, plan = publish(
            content,
            decision,
            output_dir=args.output_dir,
            skip_confirm=args.skip_confirm,
        )
        print(f"\nPDF rendered: {pdf_path}")
        print(plan.summary())
