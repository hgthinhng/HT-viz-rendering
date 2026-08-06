#!/usr/bin/env python3
"""viz_render_py.py - Pass B fallback renderer for note-pipeline-viz.

Pure-Python (matplotlib) renderer so the pipeline can produce data figures inside the
Linux sandbox without viz-factory (PowerShell + headless Chrome). Reads the same
spec.json contract, writes <out>/<MODULE>_<id>.png per figure, 200 dpi, styled to the
note design system and the create-viz principles: declutter (no top/right spines,
light y-grid only), bars start at zero, direct labeling over legends when few series,
colorblind-safe palette anchored on the subject accent, no 3D, no dual axes.

Spec contract:
{
  "module": "EQ_M3",
  "theme":  {"accent": "#2E6B3E"},
  "figures": [
    {"id": "1.2.a", "component": "bar_grouped", "caption": "...", "params": {...}}
  ]
}

Components: bar_grouped, bar_stacked, bar_h, line, payoff, waterfall, scatter,
heatmap, donut, slope.

Usage:
  python3 viz_render_py.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]

Exit code = number of failed figures (0 = all rendered).
"""
import argparse, json, os, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PAPER = "#FFFEF8"
INK = "#1F1F1F"
MUTED = "#666666"
GRID = "#E8E5DE"
SPINE = "#BBBBBB"
DOWN_RED = "#C00000"
INDIGO = "#2C3878"

def palette(accent):
    """Design-system palette: subject accent first, then fixed identity colors.
    Distinct in hue and lightness (colorblind-considerate)."""
    base = [accent, "#B85A1C", "#2C3878", "#7A5C00", "#5C2D91", "#666666"]
    # dedupe while preserving order (accent may equal a fixed color)
    seen, out = set(), []
    for c in base:
        cl = c.lower()
        if cl not in seen:
            seen.add(cl)
            out.append(c)
    return out

def fmt_value(v, kind="num", currency="$"):
    if v is None:
        return ""
    if kind == "pct":
        return f"{v:,.1f}%".replace(".0%", "%")
    if kind == "cur":
        a = abs(v)
        if a >= 1e9: return f"{currency}{v/1e9:,.1f}B"
        if a >= 1e6: return f"{currency}{v/1e6:,.1f}M"
        if a >= 1e4: return f"{currency}{v/1e3:,.1f}K"
        # Small currency values: keep 2 decimals when they carry information
        # (pedagogical data like $102.81 must not collapse to $103)
        return f"{currency}{v:,.2f}" if not a_int(v) else f"{currency}{v:,.0f}"
    if a_int(v):
        return f"{v:,.0f}"
    return f"{v:,.2f}"

def a_int(v):
    try:
        return float(v) == int(float(v))
    except (TypeError, ValueError):
        return False

def new_fig(figsize=(7.0, 4.2)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=PAPER)
    ax.set_facecolor(PAPER)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SPINE)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    return fig, ax

def style_labels(ax, p):
    if p.get("x_label"):
        ax.set_xlabel(p["x_label"], fontsize=10, color=INK)
    if p.get("y_label"):
        ax.set_ylabel(p["y_label"], fontsize=10, color=INK)
    if p.get("title"):
        ax.set_title(p["title"], fontsize=12, fontweight="bold", color=INK, loc="left", pad=10)

def maybe_pct_axis(ax, p):
    yf = p.get("y_format")
    if yf == "pct":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}%"))
    elif yf == "cur":
        cur = p.get("currency", "$")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_value(v, "cur", cur)))

# ---------------------------------------------------------------- components

def c_bar_grouped(p, colors):
    cats = p["categories"]; series = p["series"]
    n, k = len(cats), len(series)
    fig, ax = new_fig()
    width = min(0.8 / k, 0.35)
    x = np.arange(n)
    hl = p.get("highlight")
    for si, s in enumerate(series):
        offs = (si - (k - 1) / 2) * width
        cols = []
        for ci in range(n):
            base_col = colors[si % len(colors)]
            if hl is not None and (cats[ci] == hl or ci == hl) and k == 1:
                cols.append(colors[1 % len(colors)])
            else:
                cols.append(base_col)
        bars = ax.bar(x + offs, s["values"], width * 0.92, label=s.get("name", ""), color=cols)
        if n * k <= 10:
            for b, v in zip(bars, s["values"]):
                ax.annotate(fmt_value(v, p.get("y_format", "num"), p.get("currency", "$")),
                            (b.get_x() + b.get_width() / 2, b.get_height()),
                            ha="center", va="bottom", fontsize=8.5, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=9, color=INK)
    ax.set_ylim(bottom=0)  # bars start at zero (accuracy rule)
    if k > 1:
        ax.legend(frameon=False, fontsize=9, loc="best")
    style_labels(ax, p); maybe_pct_axis(ax, p)
    return fig

def c_bar_stacked(p, colors):
    cats = p["categories"]; series = p["series"]
    fig, ax = new_fig()
    x = np.arange(len(cats))
    bottom = np.zeros(len(cats))
    for si, s in enumerate(series):
        vals = np.array(s["values"], dtype=float)
        ax.bar(x, vals, 0.55, bottom=bottom, label=s.get("name", ""), color=colors[si % len(colors)])
        bottom += vals
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=9, color=INK)
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, fontsize=9, loc="best")
    style_labels(ax, p); maybe_pct_axis(ax, p)
    return fig

def c_bar_h(p, colors):
    cats = p["categories"]; vals = p["values"]
    fig, ax = new_fig(figsize=(7.0, max(2.6, 0.45 * len(cats) + 1.2)))
    ax.xaxis.grid(True, color=GRID, linewidth=0.6); ax.yaxis.grid(False)
    y = np.arange(len(cats))
    hl = p.get("highlight")
    cols = [colors[1] if (hl is not None and (c == hl or i == hl)) else colors[0]
            for i, c in enumerate(cats)]
    ax.barh(y, vals, 0.6, color=cols)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=9, color=INK)
    ax.invert_yaxis()
    ax.set_xlim(left=0)
    for yi, v in zip(y, vals):
        ax.annotate(" " + fmt_value(v, p.get("y_format", "num"), p.get("currency", "$")),
                    (v, yi), va="center", fontsize=8.5, color=INK)
    style_labels(ax, p)
    if p.get("y_format") == "pct":
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}%"))
    elif p.get("y_format") == "cur":
        cur = p.get("currency", "$")
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_value(v, "cur", cur)))
    return fig

def _line_like(p, colors, zero_line=False):
    x = p["x"]; series = p["series"]
    fig, ax = new_fig()
    numeric_x = all(isinstance(v, (int, float)) for v in x)
    xs = np.array(x, dtype=float) if numeric_x else np.arange(len(x))
    muted = p.get("muted", False)
    hl_name = p.get("highlight")
    for si, s in enumerate(series):
        if muted:
            _col = colors[0] if (hl_name and s.get("name") == hl_name) else "#C9BEB2"
            _lw = 2.6 if (hl_name and s.get("name") == hl_name) else 1.2
        else:
            _col, _lw = colors[si % len(colors)], 2.0
        ax.plot(xs, s["values"], color=_col, linewidth=_lw,
                marker="o" if len(x) <= 12 and not zero_line and not muted else None, markersize=3.5)
        # Direct labeling at the right end (create-viz: prefer over legends when few series)
        if not muted and len(series) <= 4 and s.get("name"):
            ax.annotate(" " + s["name"], (xs[-1], s["values"][-1]),
                        color=colors[si % len(colors)], fontsize=9, va="center", fontweight="bold")
    if len(series) > 4 and not muted:
        ax.legend([s.get("name", "") for s in series], frameon=False, fontsize=9)
    if not numeric_x:
        ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=9, color=INK)
    if zero_line:
        ax.axhline(0, color=INK, linewidth=1.0)
    style_labels(ax, p); maybe_pct_axis(ax, p)
    if len(series) <= 4:
        fig.subplots_adjust(right=0.82)
    return fig

def c_line(p, colors):
    return _line_like(p, colors, zero_line=False)

def c_payoff(p, colors):
    fig = _line_like(p, colors, zero_line=True)
    ax = fig.axes[0]
    for be in p.get("breakeven", []):
        ax.axvline(be, color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
        ax.annotate(f" BE = {be:g}", (be, ax.get_ylim()[1]), fontsize=8.5,
                    color=MUTED, va="top")
    return fig

def c_waterfall(p, colors):
    steps = p["steps"]
    labels = [s["label"] for s in steps]
    vals = [float(s["value"]) for s in steps]
    cum, run = [], 0.0
    for v in vals:
        cum.append(run); run += v
    total = run
    fig, ax = new_fig(figsize=(7.0, 4.4))
    x = np.arange(len(steps) + 1)
    accent = colors[0]
    for i, (b, v) in enumerate(zip(cum, vals)):
        col = accent if v >= 0 else DOWN_RED
        ax.bar(i, v, 0.6, bottom=b, color=col)
        ax.annotate(fmt_value(v, p.get("y_format", "num"), p.get("currency", "$")),
                    (i, b + v + (abs(total) * 0.01 if v >= 0 else -abs(total) * 0.04)),
                    ha="center", fontsize=8.5, color=INK)
        if i > 0:
            ax.plot([i - 1 + 0.3, i - 0.3], [cum[i], cum[i]], color=MUTED, linewidth=0.7)
    ax.bar(len(steps), total, 0.6, color=INDIGO)
    ax.annotate(fmt_value(total, p.get("y_format", "num"), p.get("currency", "$")),
                (len(steps), total), ha="center", va="bottom", fontsize=9, color=INK, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labels + [p.get("total_label", "Tổng")],
                                         fontsize=8.5, color=INK, rotation=p.get("rotate", 0))
    ax.axhline(0, color=INK, linewidth=0.9)
    # Explicit headroom: value labels above bars must never clip (margins() does not
    # account for annotation extents).
    _tops = [b + max(0.0, v) for b, v in zip(cum, vals)] + [max(0.0, total)]
    _bots = [b + min(0.0, v) for b, v in zip(cum, vals)] + [min(0.0, total), 0.0]
    _span = max(_tops) - min(_bots) or 1.0
    ax.set_ylim(min(_bots) - 0.06 * _span, max(_tops) + 0.12 * _span)
    style_labels(ax, p); maybe_pct_axis(ax, p)
    return fig

def c_scatter(p, colors):
    pts = p["points"]
    fig, ax = new_fig()
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    xs = [q["x"] for q in pts]; ys = [q["y"] for q in pts]
    ax.scatter(xs, ys, s=46, color=colors[0], zorder=3)
    for q in pts:
        if q.get("label"):
            ax.annotate(" " + q["label"], (q["x"], q["y"]), fontsize=8.5, color=INK, va="bottom")
    quad = p.get("quadrant")
    if quad:
        ax.axvline(quad["x"], color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
        ax.axhline(quad["y"], color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
    style_labels(ax, p)
    return fig

def c_heatmap(p, colors):
    rows, cols_, vals = p["rows"], p["cols"], np.array(p["values"], dtype=float)
    fig, ax = plt.subplots(figsize=(max(5.0, 1.0 * len(cols_) + 2), max(3.2, 0.55 * len(rows) + 1.4)),
                           facecolor=PAPER)
    ax.set_facecolor(PAPER)
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("cfa", ["#FFFFFF", colors[0]])
    im = ax.imshow(vals, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(cols_))); ax.set_xticklabels(cols_, fontsize=9, color=INK)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=9, color=INK)
    vmax, vmin = float(vals.max()), float(vals.min())
    thresh = (vmax + vmin) / 2
    for i in range(len(rows)):
        for j in range(len(cols_)):
            v = vals[i, j]
            ax.text(j, i, fmt_value(v, p.get("fmt", "num"), p.get("currency", "$")),
                    ha="center", va="center", fontsize=8.5,
                    color="white" if v > thresh else INK)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.tick_params(colors=MUTED, length=0)
    style_labels(ax, p)
    return fig

def c_donut(p, colors):
    labels, vals = p["labels"], p["values"]
    if len(labels) > 6:
        raise ValueError("donut > 6 slices: dùng bar_h thay (create-viz rule)")
    fig, ax = plt.subplots(figsize=(5.6, 4.0), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    wedges, _ = ax.pie(vals, startangle=90, counterclock=False,
                       colors=[colors[i % len(colors)] for i in range(len(vals))],
                       wedgeprops={"width": 0.42, "edgecolor": PAPER, "linewidth": 1.5})
    total = sum(vals)
    for w, lab, v in zip(wedges, labels, vals):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        r = 1.12
        ax.annotate(f"{lab}\n{fmt_value(100*v/total, 'pct')}",
                    (r * np.cos(ang), r * np.sin(ang)), ha="center", va="center",
                    fontsize=8.5, color=INK)
    return fig

def c_slope(p, colors):
    items = p["items"]
    fig, ax = new_fig(figsize=(6.0, 4.2))
    ax.yaxis.grid(False)
    for ii, it in enumerate(items):
        col = colors[ii % len(colors)]
        ax.plot([0, 1], [it["left"], it["right"]], color=col, linewidth=2.0, marker="o", markersize=4)
        ax.annotate(f'{it["name"]} {fmt_value(it["left"], p.get("y_format", "num"))} ',
                    (0, it["left"]), ha="right", va="center", fontsize=9, color=col)
        ax.annotate(f' {fmt_value(it["right"], p.get("y_format", "num"))}',
                    (1, it["right"]), ha="left", va="center", fontsize=9, color=col, fontweight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels([p.get("left_label", "Trước"), p.get("right_label", "Sau")], fontsize=10, color=INK)
    ax.set_xlim(-0.45, 1.45)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_yticks([])
    style_labels(ax, p)
    return fig

def c_tree(p, colors):
    """Binomial lattice: levels = [["4.000%"], ["6.886%","5.123%"], [...]] left->right.
    Node = circle + label; edges connect node (t,i) -> (t+1,i) and (t+1,i+1)."""
    levels = p["levels"]
    fig, ax = plt.subplots(figsize=(6.8, 4.4), facecolor=PAPER)
    ax.set_facecolor(PAPER); ax.axis("off")
    pos = {}
    for t, lv in enumerate(levels):
        n = len(lv)
        for i, val in enumerate(lv):
            y = (n - 1) / 2 - i
            pos[(t, i)] = (t, y)
    for t in range(len(levels) - 1):
        for i in range(len(levels[t])):
            for j in (i, i + 1):
                if j < len(levels[t + 1]):
                    x0, y0 = pos[(t, i)]; x1, y1 = pos[(t + 1, j)]
                    ax.plot([x0, x1], [y0, y1], color=SPINE, lw=1.1, zorder=1)
    hl = p.get("highlight_level")
    for (t, i), (x, y) in pos.items():
        col = colors[0] if (hl is None or t == hl) else "#9A8B8F"
        ax.scatter([x], [y], s=1450, color=PAPER, edgecolor=col, linewidth=2.0, zorder=2)
        ax.annotate(str(levels[t][i]), (x, y), ha="center", va="center",
                    fontsize=9.5, color=INK, fontweight="bold", zorder=3)
    xlabels = p.get("x_labels") or [f"Time {t}" for t in range(len(levels))]
    for t, lab in enumerate(xlabels[:len(levels)]):
        ax.annotate(lab, (t, -(max(len(l) for l in levels) - 1) / 2 - 0.75),
                    ha="center", fontsize=9, color=MUTED)
    ax.set_xlim(-0.5, len(levels) - 0.4)
    ax.set_ylim(-(max(len(l) for l in levels)) / 2 - 0.9, (max(len(l) for l in levels)) / 2 + 0.5)
    style_labels(ax, p)
    return fig

COMPONENTS = {
    "tree": c_tree,
    "bar_grouped": c_bar_grouped,
    "bar_stacked": c_bar_stacked,
    "bar_h": c_bar_h,
    "line": c_line,
    "payoff": c_payoff,
    "waterfall": c_waterfall,
    "scatter": c_scatter,
    "heatmap": c_heatmap,
    "donut": c_donut,
    "slope": c_slope,
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--only", default=None, help="Render only this figure id")
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    module = spec["module"]
    accent = (spec.get("theme") or {}).get("accent", "#2C3878")
    colors = palette(accent)
    os.makedirs(args.out_dir, exist_ok=True)

    ok, fail = 0, 0
    for fig_spec in spec.get("figures", []):
        fid = fig_spec.get("id")
        comp = fig_spec.get("component")
        if args.only and fid != args.only:
            continue
        fn = COMPONENTS.get(comp)
        if fn is None:
            sys.stderr.write(f"WARN: unknown component '{comp}' (id={fid}), skipped. "
                             f"Available: {sorted(COMPONENTS)}\n")
            fail += 1
            continue
        try:
            fig = fn(fig_spec.get("params", {}), colors)
            # bloomberg-viz chrome: thick top rule + source line (EIR layer)
            _p = fig_spec.get("params", {})
            if _p.get("chrome", True):
                import matplotlib.lines as _ml
                fig.add_artist(_ml.Line2D([0.005, 0.995], [0.995, 0.995],
                               color=INK, lw=3.0, transform=fig.transFigure))
            _src_txt = _p.get("source")
            if _src_txt:
                fig.text(0.005, -0.02, f"Nguồn: {_src_txt}", fontsize=8,
                         color=MUTED, style="italic", transform=fig.transFigure,
                         ha="left", va="top")
            out_png = os.path.join(args.out_dir, f"{module}_{fid}.png")
            fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight", facecolor=PAPER)
            plt.close(fig)
            print(f"RENDERED {out_png}")
            ok += 1
        except Exception as e:
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n")
            fail += 1
    print(f"viz_render_py: {ok} rendered, {fail} failed")
    return fail

if __name__ == "__main__":
    sys.exit(main())
