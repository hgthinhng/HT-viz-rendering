"""
Opvia Publish Orchestrator (LLM-driven)
========================================

Single entry point cho pipeline xuất bản Opvia.

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
    """Locate skill base directory chứa các skill folders Opvia."""
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
    # Also try walking up from this file location
    here = Path(__file__).resolve().parent
    for parent in [here.parent, here.parent.parent]:
        candidates.insert(0, str(parent))

    for c in candidates:
        p = Path(c)
        if p.is_dir() and (p / "opvia-data-viz").is_dir():
            return str(p)

    raise RuntimeError(
        "Cannot find skill base directory. Tried: " + ", ".join(candidates)
    )


SKILLS_BASE = _find_skills_base()
DATA_VIZ_PATH = os.path.join(SKILLS_BASE, "opvia-data-viz")
DEEP_POLISH_PATH = os.path.join(SKILLS_BASE, "opvia-deepanalysis-polish")
DAILY_POLISH_PATH = os.path.join(SKILLS_BASE, "opvia-dailyreport-polish")

# Add to sys.path để import được data-viz module ngay
if DATA_VIZ_PATH not in sys.path:
    sys.path.insert(0, DATA_VIZ_PATH)


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

VIZ_MODULES = {"viz", "viz_wave8", "viz_wave9", "viz_wave10"}


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
    date_str: str = ""
    output_dir: str = ""
    word_count: int = 0
    output_filename: str = ""

    def summary(self) -> str:
        """Human-readable plan."""
        lines = [
            "=" * 60,
            "OPVIA PUBLISH - PIPELINE PLAN",
            "=" * 60,
            "",
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
    return "OPVIA_REPORT"


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

    title = decision.get("title") or _extract_title(content)
    date_str = decision.get("date_str") or _today_str()
    word_count = len(content.split())

    # Generate filename từ title + today date
    slug = _slugify(title)
    today_iso = date.today().strftime("%Y%m%d")
    filename = f"OPVIA_{slug}_{today_iso}.pdf"
    output_path = os.path.join(output_dir, filename)

    return PipelinePlan(
        archetype=decision["archetype"],
        polish_target=decision["polish_target"],
        refine_action=decision["refine_action"],
        viz_plan=decision.get("viz_plan", []),
        cover=decision.get("cover", {}),
        back_cover=decision.get("back_cover", {}),
        title=title,
        date_str=date_str,
        output_dir=output_dir,
        word_count=word_count,
        output_filename=output_path,
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

def _build_body_from_markdown(content: str) -> str:
    """
    Convert markdown content thành HTML body cơ bản.
    Headings -> h1/h2/h3, list bullets -> ul/li, paragraphs -> p.
    Bold **text** -> <strong>.
    """
    lines = content.strip().split("\n")
    html_parts = []
    in_list = False

    for line in lines:
        line_stripped = line.strip()
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
            short_title=_slugify(plan.title, 30),
        )

    # Add viz styles - tất cả waves (cheap, prevents missing-style bugs)
    style_imports = [
        ("viz", "viz_styles"),
        ("viz_wave8", "wave8_styles"),
        ("viz_wave9", "wave9_styles"),
        ("viz_wave10", "wave10_styles"),
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
    css = _build_css(plan)

    viz_html_by_position = _render_viz_from_plan(plan.viz_plan) if plan.viz_plan else {}

    body = _build_body_from_markdown(content)
    if viz_html_by_position:
        body = _inject_viz_placeholders(body, viz_html_by_position)

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
        description="Opvia Publish Orchestrator (LLM-driven)"
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

    args = parser.parse_args()

    content = Path(args.input_file).read_text(encoding="utf-8")
    decision = json.loads(Path(args.decision_file).read_text(encoding="utf-8"))

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
