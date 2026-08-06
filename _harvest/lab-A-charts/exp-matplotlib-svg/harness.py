#!/usr/bin/env python3
"""harness.py — thi nghiem THAT: render 3 component EIR kho nhat (football_field,
tornado, exec_dashboard) sang CA PNG (baseline nhu cu) LAN SVG (khong doi backend,
chi doi duoi file — matplotlib tu chon SVG writer theo extension), voi CA 2 che do
svg.fonttype ('path' va 'none'), de do dac that thay vi suy luan.
"""
import sys, os, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/harvest-cfa-skillchain/viz-engine")
OUT = "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/exp-matplotlib-svg"
os.makedirs(OUT, exist_ok=True)

import matplotlib
import _eir_style as S
from _eir_style import TEAL, save
import viz_eir as ve
import viz_eir_stats as ves
import viz_eir_panels as vep

S.setup_fonts()
print("=== FONT RESOLUTION (may nay) ===")
print("SANS  =", S.SANS)
print("SERIF =", S.SERIF)
print("MONO  =", S.MONO)

# ---- lay params that tu chinh library (khong bia) ----
with open(os.path.join(os.path.dirname(S.__file__), "spec_showcase.json"), encoding="utf-8") as f:
    spec = json.load(f)
fig_by_id = {fs["id"]: fs for fs in spec["figures"]}
football_params = fig_by_id["football_field"]["params"]
exec_params = fig_by_id["exec_dashboard"]["params"]
tornado_params = ves._SHOWCASE["tornado"]

CASES = [
    ("football_field", ve.c_football_field, football_params),
    ("tornado", ves.c_tornado, tornado_params),
    ("exec_dashboard", ve.c_exec_dashboard, exec_params),
]

results = []


def render(name, fn, params, fmt, svg_fonttype=None, dpi=200):
    if svg_fonttype:
        matplotlib.rcParams["svg.fonttype"] = svg_fonttype
    fig = fn(params, params.get("accent") or TEAL)
    suffix = f"_{svg_fonttype}" if svg_fonttype else ""
    path = os.path.join(OUT, f"{name}{suffix}.{fmt}")
    t0 = time.time()
    save(fig, path, dpi=dpi)
    dt = time.time() - t0
    size = os.path.getsize(path)
    results.append({"name": name, "fmt": fmt, "svg_fonttype": svg_fonttype, "path": path,
                     "bytes": size, "seconds": round(dt, 3)})
    print(f"OK {name:16s} fmt={fmt:4s} fonttype={str(svg_fonttype):6s} "
          f"-> {size:>9,} bytes  ({dt:.2f}s)  {path}")


for name, fn, params in CASES:
    # 1) baseline PNG (nhu pipeline cu dang dung)
    render(name, fn, params, "png")
    # 2) SVG, fonttype='path' (mac dinh eir chua set, matplotlib default la 'path')
    render(name, fn, params, "svg", svg_fonttype="path")
    # 3) SVG, fonttype='none' (chu la <text> that)
    render(name, fn, params, "svg", svg_fonttype="none")

with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\n=== DONE, results.json written ===")
