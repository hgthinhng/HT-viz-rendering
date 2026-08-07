#!/usr/bin/env python3
"""viz_super.py — unified dispatcher for the super-viz-factory (48 EIR components).

Merges the COMPONENTS registries of all EIR modules behind ONE spec.json runner, so a
CFA note can request any institutional/editorial figure — chart, diagram, panel, KPI —
through a single call and the same spec contract used by the core note-pipeline-viz
renderer.

Core primitives (bar_grouped, line, waterfall, scatter, heatmap, donut, slope, tree,
payoff, bar_h, bar_stacked) are NOT in this repo. They lived in viz_render_py.py, which
carried the warm palette (#FFFEF8 paper, #1F1F1F ink) that this repo rejected in favour
of the cold one (#051C2C ink, #2251FF accent), and was deleted after Phase 1 as dead
code. The nearest institutional equivalents inside the 48 components below are
comparison (grouped bars), index100 (indexed lines), flow_bridge (waterfall),
comps_scatter and connected_scatter (scatter), correlation_matrix (heatmap), and
distribution. If a genuine primitive is needed, port it from
_harvest/harvest-cfa-skillchain/viz-engine/viz_render_py.py onto the cold palette in
design-system/tokens.py rather than reviving the old file as-is.

Modules merged:
  viz_eir          21  comparison/rank/time/distribution/sell-side/part-to-whole/editorial
  viz_eir_stats     7  correlation_matrix, distribution(VaR), tornado, spc_control_chart,
                       seasonality, candlestick, spread_ladder
  viz_eir_diagram   8  decision_tree, flowchart, network_graph, mechanism_flow, flow_bridge,
                       sankey, timeline, lattice
  viz_eir_panels    7  executive_summary, scenario_cards, swot, comparison, dupont,
                       before_after, status_strip
  viz_eir_kpi       5  kpi_card_with_sparkline, sparkline_row, annotated_narrative,
                       anomaly_callout, stat_dashboard

Usage:
  python3 viz_super.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_super.py --list
"""
from __future__ import annotations
import argparse, importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _eir_style as S
from _eir_style import TEAL, save

_MODULES = ["viz_eir", "viz_eir_stats", "viz_eir_diagram", "viz_eir_panels", "viz_eir_kpi"]

COMPONENTS = {}
_SOURCE = {}
for _m in _MODULES:
    mod = importlib.import_module(_m)
    for k, fn in mod.COMPONENTS.items():
        if k in COMPONENTS:
            sys.stderr.write(f"WARN duplicate component '{k}' ({_m} vs {_SOURCE[k]}); {_m} wins\n")
        COMPONENTS[k] = fn
        _SOURCE[k] = _m


def render_spec(spec_path, out_dir, only=None, dpi=200):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    module = spec.get("module", "MOD")
    accent = (spec.get("theme") or {}).get("accent", TEAL)
    os.makedirs(out_dir, exist_ok=True)
    ok = fail = 0
    for fs in spec.get("figures", []):
        fid, comp = fs.get("id"), fs.get("component")
        if only and fid != only:
            continue
        fn = COMPONENTS.get(comp)
        if fn is None:
            sys.stderr.write(f"WARN unknown component '{comp}' (id={fid}). If it is a core "
                             f"primitive (bar_grouped/line/waterfall/...), this repo does not "
                             f"ship one. Closest here: comparison, index100, flow_bridge, "
                             f"comps_scatter, correlation_matrix, distribution.\n")
            fail += 1
            continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=dpi)
            print(f"RENDERED {out}  [{_SOURCE[comp]}]")
            ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n")
            fail += 1
    print(f"viz_super: {ok} rendered, {fail} failed  (of {len(COMPONENTS)} components available)")
    return fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--out-dir", default=".")
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    S.setup_fonts()
    if a.list:
        for m in _MODULES:
            keys = sorted(k for k in COMPONENTS if _SOURCE[k] == m)
            print(f"{m:18s} ({len(keys)}): {', '.join(keys)}")
        print(f"TOTAL: {len(COMPONENTS)} EIR components")
        return 0
    if not a.spec:
        ap.error("--spec required (or use --list)")
    return render_spec(a.spec, a.out_dir, a.only, a.dpi)


if __name__ == "__main__":
    sys.exit(main())
