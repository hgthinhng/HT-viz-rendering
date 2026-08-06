#!/usr/bin/env python3
"""StockLPT data-viz smoke test.

Self-contained: sets brand env, wires sys.path to the skill root, imports the
core modules, then renders a handful of components to HTML and asserts that the
output is non-empty and brand-clean (no Opvia / Prussian leftovers).

Run from anywhere:  python3 smoke_test.py
"""

import os
import sys

# ---------------------------------------------------------------------------
# Environment must be set BEFORE importing the viz modules (brand + matplotlib).
# ---------------------------------------------------------------------------
os.environ["STOCKLPT_BRAND"] = "stocklpt"
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

# The skill package dir = parent of this tests/ folder.
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import _brand  # noqa: E402
import viz  # noqa: E402
import viz_wave8  # noqa: E402
import viz_charts  # noqa: E402
import validators  # noqa: E402

# ---------------------------------------------------------------------------
# 1. Brand resolves to StockLPT
# ---------------------------------------------------------------------------
brand = _brand.current_brand()
assert brand.display_name == "StockLPT", (
    f"expected display_name 'StockLPT', got {brand.display_name!r}"
)

# ---------------------------------------------------------------------------
# 2. Render components -> non-empty HTML strings
# ---------------------------------------------------------------------------
outputs = {}

outputs["capsule_verdict"] = viz.capsule_verdict(
    ticker="VN30 · VIX",
    meta="Đo lường nỗi sợ thị trường · HOSE",
    stance_label="THẬN TRỌNG",
    stance_hex="#C8972E",
    risk_label="Rủi ro: Cao",
    mega_value="34,2",
    mega_unit="pts",
    stat_lead="Chỉ số biến động ngụ ý",
    stat_main="Vùng <em>căng thẳng</em> — trên ngưỡng 30",
    stat_sub="Trung bình 10 năm: 18,4 pts",
    thesis="VIX phá 30 đồng nghĩa thị trường định giá lại rủi ro đuôi.",
    metrics=[
        {"value": "+86%", "label": "vs TB 10 năm", "note": "18,4 → 34,2"},
        {"value": "4–6 tuần", "label": "độ dài pha de-risk", "note": "trung vị"},
        {"value": "-7,3%", "label": "VN-Index từ đỉnh", "note": "drawdown"},
    ],
    signal="Theo dõi VIX về dưới 25 làm mốc xác nhận risk-on.",
    mega_accent="#C0392B",
)

outputs["scenario_outlook"] = viz.scenario_outlook(
    scenarios=[
        {"name": "Bull", "tone": "up", "prob": "30%",
         "thesis": "Biên gộp hồi về 38% khi giá đầu vào hạ.",
         "trigger": "Giá HRC < 540 USD/tấn.",
         "implication": "EPS 2026 +22%; giá mục tiêu 60.000đ."},
        {"name": "Base", "tone": "flat", "prob": "50%",
         "thesis": "Sản lượng đi ngang, biên gộp giữ 34%.",
         "trigger": "Vĩ mô không đổi.",
         "implication": "EPS 2026 +9%; giá mục tiêu 43.000đ."},
        {"name": "Bear", "tone": "down", "prob": "20%",
         "thesis": "Cầu xây dựng yếu, biên gộp co về 30%.",
         "trigger": "Giá HRC > 620 USD/tấn.",
         "implication": "EPS 2026 -6%; giá mục tiêu 30.000đ."},
    ],
    title="Ba kịch bản thị giá HPG 2026",
    subtitle="Xác suất do StockLPT Research gán",
)

outputs["bar_horizontal"] = viz.bar_horizontal(
    items=[
        {"label": "VCB", "value": 19.2, "positive": True},
        {"label": "TCB", "value": 16.1},
        {"label": "VPB", "value": 28.3, "danger": True},
        {"label": "MBB", "value": 22.0, "warn": True},
    ],
    threshold=25.0,
    threshold_label="Trần",
    title="ROE ngành ngân hàng",
    subtitle="Q1/2026",
)

outputs["quadrant_scatter"] = viz_wave8.quadrant_scatter(
    points=[
        {"label": "VCB", "x": 2.4, "y": 19.2, "color": "#2A1A4A"},
        {"label": "TCB", "x": 1.1, "y": 16.1, "color": "#16633C"},
        {"label": "VPB", "x": 1.3, "y": 14.0, "color": "#C8972E"},
        {"label": "MBB", "x": 1.0, "y": 22.0, "color": "#2A1A4A"},
    ],
    x_label="P/B (lần)",
    y_label="ROE (%)",
    quadrants={"tl": "Quá đắt", "tr": "Sweet spot", "bl": "Tránh", "br": "Cơ hội"},
    title="Định vị peer ngân hàng",
)

for name, html in outputs.items():
    assert isinstance(html, str), f"{name}: expected str, got {type(html).__name__}"
    assert html.strip(), f"{name}: returned empty string"

# ---------------------------------------------------------------------------
# 3. Brand-clean: no Opvia / Prussian / #003153 leftovers (case-insensitive)
# ---------------------------------------------------------------------------
FORBIDDEN = ["opvia", "prussian", "#003153"]
for name, html in outputs.items():
    low = html.lower()
    for token in FORBIDDEN:
        assert token not in low, f"{name}: forbidden token {token!r} found in output"

# Touch validators so a broken import surfaces here (kept light + version-agnostic).
assert validators is not None
assert viz_charts is not None

print("SMOKE OK")

# institutional + daily kit import smoke
import viz_institutional, viz_daily
assert hasattr(viz_institutional,'research_masthead') and hasattr(viz_daily,'price_table')
print('institutional+daily kit import OK')
