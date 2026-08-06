#!/usr/bin/env python3
"""harness_fixed.py — CHUNG MINH fix cu the: chi sua 1 duong dan sai
(/liberation2/ -> /liberation/, dung font Liberation Mono CO SAN tren may),
KHONG can bundle font moi, roi render lai chinh 2 component da lay tofu
(exec_dashboard, tornado) va so sanh truoc/sau bang lai canh bao glyph.
"""
import sys, os, warnings, io
sys.path.insert(0, "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/harvest-cfa-skillchain/viz-engine")
OUT = "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/exp-matplotlib-svg"

import matplotlib
import matplotlib.font_manager as fm
import _eir_style as S

# ---- FIX: dung dung duong dan Liberation Mono THAT SU ton tai tren may nay ----
REAL_LIBERATION_MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
assert os.path.exists(REAL_LIBERATION_MONO), "font khong ton tai, fix sai gia thuyet"
fm.fontManager.addfont(REAL_LIBERATION_MONO)
S.MONO = fm.FontProperties(fname=REAL_LIBERATION_MONO).get_name()
S._FONTS_READY = True  # khoa lai de setup_fonts() ben trong khong ghi de S.MONO
print("PATCHED S.MONO ->", S.MONO)

import viz_eir as ve
import viz_eir_stats as ves
import json
from _eir_style import TEAL, save

with open(os.path.join(os.path.dirname(S.__file__), "spec_showcase.json"), encoding="utf-8") as f:
    spec = json.load(f)
fig_by_id = {fs["id"]: fs for fs in spec["figures"]}
exec_params = fig_by_id["exec_dashboard"]["params"]
tornado_params = ves._SHOWCASE["tornado"]

for name, fn, params in [("exec_dashboard", ve.c_exec_dashboard, exec_params),
                          ("tornado", ves.c_tornado, tornado_params)]:
    buf = io.StringIO()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        fig = fn(params, params.get("accent") or TEAL)
        path = os.path.join(OUT, f"{name}_FIXED.png")
        save(fig, path, dpi=200)
        missing_glyph_warnings = [str(x.message) for x in w if "missing from font" in str(x.message)]
    print(f"{name}: {len(missing_glyph_warnings)} canh bao 'missing glyph' (truoc fix >=5-6 moi bieu do)")
    print(f"  -> {path}")
