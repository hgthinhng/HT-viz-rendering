#!/usr/bin/env python3
"""viz_eir_diagram.py — Editorial Institutional Research DIAGRAM library for CFA notes.

Node / box / flow diagrams hand-laid in matplotlib (Agg, static PNG) so they embed into
the Vietnamese CFA study-note .docx exactly like the charts in ``viz_eir.py``. Same
editorial chrome (kicker / serif headline / subtitle / source line via ``eir_fig``), same
warm CFA palette, same spec.json contract, so one spec may mix core + EIR chart + EIR
diagram components.

Design rules (anti "AI slop"): boxes are HAIRLINE navy outline on cream/pale-tint fill,
squared or lightly rounded corners, NO drop shadows, NO gradients; connectors are thin
(lw 1.0–1.3) muted/navy arrows; exactly ONE accent (GOLD or TEAL) marks the highlighted /
optimal path. Numbers use the VN-safe mono (S.MONO), labels use the VN-safe sans (S.SANS).

Components (COMPONENTS keys):
  decision_tree · flowchart · network_graph · mechanism_flow · flow_bridge · sankey ·
  timeline · lattice

Usage:
  python3 viz_eir_diagram.py --out-dir OUT [--only ID] [--dpi 170]
  python3 viz_eir_diagram.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _eir_style as S
from _eir_style import (
    PAPER, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge,
)
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved


# ------------------------------------------------------------------ shared meta
def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


# ---------------------------------------------------------------- small helpers
def _box(ax, cx, cy, w, h, *, fc=PAPER, ec=NAVY, lw=1.3, pad=0.012, z=3):
    """Hairline-outline rounded rectangle centred at (cx, cy). Returns the patch."""
    b = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle=f"round,pad=0,rounding_size={pad}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z, mutation_aspect=1)
    ax.add_patch(b)
    return b


def _sq(ax, cx, cy, w, h, *, fc=PAPER, ec=NAVY, lw=1.3, z=3):
    """Squared rectangle centred at (cx, cy)."""
    r = Rectangle((cx - w / 2, cy - h / 2), w, h, linewidth=lw, edgecolor=ec,
                  facecolor=fc, zorder=z)
    ax.add_patch(r)
    return r


def _text(ax, x, y, s, *, size=9.2, color=INK, family=None, weight="normal",
          style="normal", ha="center", va="center", z=6):
    return ax.text(x, y, s, fontsize=size, color=color, family=(family or SANS),
                   fontweight=weight, fontstyle=style, ha=ha, va=va, zorder=z)


def _arrow(ax, xy, xytext, *, color=MUTED, lw=1.1, style="-|>", z=2, mut=12, rad=0.0):
    cs = f"arc3,rad={rad}" if rad else None
    ax.annotate("", xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=mut,
                                connectionstyle=cs), zorder=z)


def _elbow(ax, x0, y0, x1, y1, *, color=MUTED, lw=1.15, z=2, head=False, split_frac=0.5):
    """Orthogonal L / Z connector parent(x0,y0) -> child(x1,y1); horizontal-first.
    A mid vertical riser at split_frac keeps a tidy right-angle tree look."""
    xm = x0 + (x1 - x0) * split_frac
    ax.plot([x0, xm], [y0, y0], color=color, lw=lw, zorder=z, solid_capstyle="round")
    ax.plot([xm, xm], [y0, y1], color=color, lw=lw, zorder=z, solid_capstyle="round")
    if head:
        _arrow(ax, (x1, y1), (xm, y1), color=color, lw=lw, z=z + 1)
    else:
        ax.plot([xm, x1], [y1, y1], color=color, lw=lw, zorder=z, solid_capstyle="round")


def _legend(fig, entries, *, y_fig=0.115, size=8.6):
    """Bottom legend row, CENTERED, in FIGURE coordinates so it clears the source
    chrome (source rule sits ~0.08 fig-fraction; keep y_fig above it).
    entries=[(label,color,marker)] · marker: 'sq' square · 'line' short line ·
    'circle' filled dot. Widths measured from the renderer for true centering."""
    setup_fonts()
    fig.canvas.draw()               # ensure a renderer exists for text measurement
    rend = fig.canvas.get_renderer()
    W = fig.get_figwidth() * fig.dpi
    sym_w = {"line": 0.030, "circle": 0.026, "sq": 0.024}   # symbol+gap, fig-fraction
    pad_after = 0.028                                        # gap after each label
    # measure each label width in fig-fraction
    items = []
    total = 0.0
    for lab, col, mk in entries:
        t = fig.text(0, -1, lab, fontsize=size, family=SANS)   # offscreen probe
        bb = t.get_window_extent(renderer=rend)
        lw = bb.width / W
        t.remove()
        w = sym_w.get(mk, 0.024) + lw + pad_after
        items.append((lab, col, mk, lw)); total += w
    total -= pad_after                      # no trailing pad on the last item
    cur = max(0.035, 0.5 - total / 2)       # centre the row
    for lab, col, mk, lw in items:
        if mk == "line":
            fig.add_artist(mlines.Line2D([cur, cur + 0.024], [y_fig, y_fig], color=col,
                           lw=3.0, transform=fig.transFigure, solid_capstyle="round"))
            tx = cur + 0.030
        elif mk == "circle":
            fig.add_artist(mlines.Line2D([cur + 0.010], [y_fig], marker="o", markersize=9,
                           color=col, transform=fig.transFigure, linestyle="none"))
            tx = cur + 0.024
        else:  # square swatch
            fig.patches.append(Rectangle((cur, y_fig - 0.010), 0.018, 0.020,
                               transform=fig.transFigure, facecolor=col, edgecolor="none"))
            tx = cur + 0.024
        fig.text(tx, y_fig, lab, transform=fig.transFigure, fontsize=size, color=INK,
                 family=SANS, ha="left", va="center")
        cur = tx + lw + pad_after


def _layer_headers(ax, xs, labels, y, *, color=MUTED):
    for x, lab in zip(xs, labels):
        ax.text(x, y, lab, ha="center", va="bottom", fontsize=8.8, color=color,
                family=SANS, fontweight="normal", zorder=5)


# ============================================================= 1. DECISION TREE
def c_decision_tree(p, accent):
    """Left->right decision-analysis tree: decision node (square) -> chance nodes
    (small squares) with branch probabilities -> outcome leaves with EV/value labels;
    optimal path highlighted in GOLD."""
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.2, 5.9),
                      rect=(0.03, 0.06, 0.94, 0.72))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)

    tree = p["tree"]
    up_c, dn_c = TEAL, BRICK
    opt_c = GOLD

    # collect leaves to lay them out on an even vertical grid
    leaves = []
    def _collect(node):
        ch = node.get("children") or []
        if not ch:
            leaves.append(node)
        for c in ch:
            _collect(c)
    _collect(tree)
    nlv = len(leaves)
    top, bot = 82, 20
    ys = np.linspace(top, bot, nlv) if nlv > 1 else [ (top + bot) / 2 ]
    for lf, yy in zip(leaves, ys):
        lf["_y"] = yy

    # x columns by depth
    def _depth(node):
        ch = node.get("children") or []
        return 0 if not ch else 1 + max(_depth(c) for c in ch)
    maxd = _depth(tree)
    xcols = np.linspace(8, 92, maxd + 1)

    # assign y to internal nodes = mean of children; x by depth
    def _place(node, d):
        node["_x"] = xcols[d]
        ch = node.get("children") or []
        if ch:
            for c in ch:
                _place(c, d + 1)
            node["_y"] = float(np.mean([c["_y"] for c in ch]))
    _place(tree, 0)

    opt_edges = set()  # (id(parent), id(child)) on optimal path
    def _mark_opt(node):
        ch = node.get("children") or []
        if not ch:
            return
        best = None
        for c in ch:
            if c.get("optimal"):
                best = c
        if best is not None:
            opt_edges.add((id(node), id(best)))
            _mark_opt(best)
        else:
            for c in ch:
                _mark_opt(c)
    _mark_opt(tree)

    # draw edges (orthogonal) parent->child
    def _draw_edges(node):
        ch = node.get("children") or []
        for c in ch:
            on = (id(node), id(c)) in opt_edges
            col = opt_c if on else FAINT
            lw = 2.6 if on else 1.4
            _elbow(ax, node["_x"], node["_y"], c["_x"], c["_y"], color=col, lw=lw,
                   z=(4 if on else 2))
            # probability label: sit on the CHILD horizontal segment (right of the
            # riser at split_frac=0.5), at the child's own y -> never on the riser.
            if c.get("prob") is not None:
                xm = node["_x"] + (c["_x"] - node["_x"]) * 0.5
                xlab = xm + (c["_x"] - xm) * 0.5
                _text(ax, xlab, c["_y"] + 3.0,
                      f"p = {c['prob']}".replace(".", ","), size=9.2, color=MUTED,
                      family=MONO, va="bottom")
            _draw_edges(c)
    _draw_edges(tree)

    # draw nodes
    def _draw_node(node):
        k = node.get("kind", "chance")
        x, y = node["_x"], node["_y"]
        label = node.get("label", "")
        if k == "decision":
            _sq(ax, x, y, 3.6, 6.2, fc=PAPER, ec=accent, lw=2.0, z=5)
            if label:
                _text(ax, x, y + 6.6, label, size=9.6, color=NAVY, weight="bold", va="bottom")
            if node.get("ev") is not None:
                _text(ax, x, y - 6.6, f"EV = {node['ev']}".replace(".", ","),
                      size=9.2, color=INK, family=MONO, va="top")
        elif k == "chance":
            _sq(ax, x, y, 3.4, 5.6, fc=PAPER, ec=NAVY, lw=1.8, z=5)
            if label:
                _text(ax, x, y + 6.2, label, size=9.6, color=NAVY, weight="bold", va="bottom")
            if node.get("ev") is not None:
                _text(ax, x, y - 6.2, f"EV* = {node['ev']}".replace(".", ","),
                      size=9.2, color=INK, family=MONO, va="top")
        else:  # leaf
            tone = node.get("tone")
            dot = up_c if tone == "up" else dn_c if tone == "down" else MUTED
            ax.scatter([x], [y], s=70, color=dot, zorder=6)
            if label:
                _text(ax, x + 2.4, y + 1.3, label, size=9.4, color=NAVY, weight="bold",
                      ha="left", va="bottom")
            if node.get("value") is not None:
                vc = up_c if tone == "up" else dn_c if tone == "down" else INK
                _text(ax, x + 2.4, y - 1.6, str(node["value"]).replace(".", ","),
                      size=9.6, color=vc, family=MONO, ha="left", va="top")
        for c in (node.get("children") or []):
            _draw_node(c)
    _draw_node(tree)

    # layer headers
    hdrs = p.get("layer_labels")
    if hdrs:
        _layer_headers(ax, xcols[:len(hdrs)], hdrs, 90, color=MUTED)

    _legend(fig, [
        ("Nút quyết định (lựa chọn)", accent, "sq"),
        ("Nút ngẫu nhiên (xác suất)", NAVY, "sq"),
        ("Kết cục dương", TEAL, "line"),
        ("Kết cục âm", BRICK, "line"),
    ], y_fig=0.115)
    return fig


# ================================================================= 2. FLOWCHART
def c_flowchart(p, accent):
    """Top->down flowchart: rounded process rectangles + a diamond decision with
    Yes/No branches to two outcome boxes."""
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.4, 6.6),
                      rect=(0.03, 0.05, 0.94, 0.74))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    nodes = p["nodes"]; edges = p["edges"]
    N = {}
    for nd in nodes:
        N[nd["id"]] = nd

    def _wrap(s, width):
        words = s.split(); lines = []; cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if len(t) > width and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
        return "\n".join(lines)

    # draw nodes
    handles = {}
    for nd in nodes:
        x, y = nd["x"], nd["y"]
        kind = nd.get("kind", "process")
        label = _wrap(nd["label"], nd.get("wrap", 18))
        if kind == "decision":
            w, h = nd.get("w", 34), nd.get("h", 26)
            dia = Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                          closed=True, facecolor="#F1EEE6", edgecolor=NAVY, lw=1.4, zorder=3)
            ax.add_patch(dia)
            _text(ax, x, y, label, size=9.4, color=INK)
        elif kind == "terminal":
            tone = nd.get("tone")
            ec = TEAL if tone == "up" else BRICK if tone == "down" else NAVY
            fc = "#EAF0EE" if tone == "up" else "#F6EAE8" if tone == "down" else "#F1EEE6"
            w, h = nd.get("w", 30), nd.get("h", 15)
            _box(ax, x, y, w, h, fc=fc, ec=ec, lw=1.5, pad=0.03, z=3)
            _text(ax, x, y, label, size=9.4, color=NAVY, weight="bold")
        else:  # process / start
            w, h = nd.get("w", 30), nd.get("h", 15)
            fc = "#EDEAE1" if kind == "start" else "#F1EEE6"
            _box(ax, x, y, w, h, fc=fc, ec=NAVY, lw=1.4, pad=0.03, z=3)
            _text(ax, x, y, label, size=9.4, color=INK,
                  weight="bold" if kind == "start" else "normal")
        nd["_w"] = nd.get("w", 34 if kind == "decision" else 30)
        nd["_h"] = nd.get("h", 26 if kind == "decision" else 15)

    def _anchor(nd, side):
        x, y = nd["x"], nd["y"]; w, h = nd["_w"], nd["_h"]
        if nd.get("kind") == "decision":
            if side == "bottom": return (x, y - h / 2)
            if side == "left":   return (x - w / 2, y)
            if side == "right":  return (x + w / 2, y)
            if side == "top":    return (x, y + h / 2)
        if side == "bottom": return (x, y - h / 2)
        if side == "top":    return (x, y + h / 2)
        if side == "left":   return (x - w / 2, y)
        if side == "right":  return (x + w / 2, y)
        return (x, y)

    for e in edges:
        a, b = N[e["from"]], N[e["to"]]
        sa = e.get("from_side", "bottom"); sb = e.get("to_side", "top")
        pa = _anchor(a, sa); pb = _anchor(b, sb)
        # orthogonal when horizontal offset present and going down
        if sa in ("left", "right"):
            # decision side branch: go out sideways, then down into target top
            midy = (pa[1] + pb[1]) / 2
            ax.plot([pa[0], pb[0]], [pa[1], pa[1]], color=MUTED, lw=1.15, zorder=1,
                    solid_capstyle="round")
            _arrow(ax, pb, (pb[0], pa[1]), color=MUTED, lw=1.15)
        else:
            _arrow(ax, pb, pa, color=MUTED, lw=1.2)
        if e.get("label"):
            lx = (pa[0] + pb[0]) / 2 + e.get("lx", 0)
            ly = (pa[1] + pb[1]) / 2 + e.get("ly", 0)
            _text(ax, lx, ly, e["label"], size=9.0, color=MUTED, family=SANS,
                  weight="bold")
    return fig


# ============================================================= 3. NETWORK GRAPH
def c_network_graph(p, accent):
    """Layered node-link structure (e.g. securitisation: pool -> SPV -> tranches):
    boxes on N layers connected by thin edges with optional edge labels."""
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.0, 5.9),
                      rect=(0.03, 0.05, 0.94, 0.74))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    layers = p["layers"]; edges = p.get("edges", [])
    nl = len(layers)
    ys = np.linspace(80, 18, nl)      # top layer high, cascade down
    pos = {}; boxw = p.get("box_w", 26); boxh = p.get("box_h", 12)
    for li, (layer, yy) in enumerate(zip(layers, ys)):
        m = len(layer)
        xs = np.linspace(20, 80, m) if m > 1 else [50]
        # single node centres; more nodes spread across width
        if m == 1:
            xs = [50]
        for nd, xx in zip(layer, xs):
            tone = nd.get("tone")
            ec = TEAL if tone == "up" else BRICK if tone == "down" else GOLD if tone == "hi" else NAVY
            fc = "#EAF0EE" if tone == "up" else "#F6EAE8" if tone == "down" else \
                 "#FBF3E2" if tone == "hi" else "#F1EEE6"
            _box(ax, xx, yy, nd.get("w", boxw), boxh, fc=fc, ec=ec, lw=1.4, pad=0.028)
            _text(ax, xx, yy, nd["label"], size=9.3, color=NAVY,
                  weight="bold" if tone else "normal")
            pos[nd["id"]] = (xx, yy, nd.get("w", boxw), boxh)

    for e in edges:
        (xa, ya, wa, ha) = pos[e["from"]]
        (xb, yb, wb, hb) = pos[e["to"]]
        pa = (xa, ya - ha / 2); pb = (xb, yb + hb / 2)
        _arrow(ax, pb, pa, color=MUTED, lw=1.15)
        if e.get("label"):
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]
            ang = np.degrees(np.arctan2(dy, dx))
            if ang < -90: ang += 180
            if ang > 90:  ang -= 180
            # nudge label off the line: perpendicular offset (n = (-dy, dx) normalised).
            L = (dx * dx + dy * dy) ** 0.5 or 1.0
            off = 3.2
            nx, ny = -dy / L * off, dx / L * off
            # for a (near-)vertical edge, push sideways; keep sign consistent (left)
            if abs(dx) < 1e-3:
                nx = -off; ny = 0.0
            ax.text(mx + nx, my + ny, e["label"], fontsize=8.4, color=MUTED,
                    family=SANS, ha="center", va="center", rotation=ang,
                    rotation_mode="anchor", zorder=5,
                    bbox=dict(boxstyle="square,pad=0.12", fc=PAPER, ec="none"))
    return fig


# ============================================================ 4. MECHANISM FLOW
def c_mechanism_flow(p, accent):
    """3 horizontal stage boxes (input -> process -> output): a colored header +
    bullet sub-points each, joined by GOLD chevron arrows."""
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.6, 5.7),
                      rect=(0.03, 0.06, 0.94, 0.72))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    stages = p["stages"]; n = len(stages)
    tone_map = {"input": INDIGO, "process": BRICK, "output": TEAL,
                "up": TEAL, "down": BRICK, "neutral": INDIGO}
    gap = 5.0
    total_w = 100.0
    bw = (total_w - gap * (n - 1) - 4) / n
    x0 = 2.0
    top, bottom = 86, 8
    head_h = 15
    for i, st in enumerate(stages):
        cx = x0 + i * (bw + gap) + bw / 2
        col = tone_map.get(st.get("tone", "neutral"), INDIGO)
        # body box (pale) with header on top
        body_top = top - head_h
        _box(ax, cx, (body_top + bottom) / 2, bw, body_top - bottom, fc="#FBFAF5",
             ec=GRID, lw=1.1, pad=0.012, z=2)
        # colored header (rounded top look via full box, squared feel)
        hb = FancyBboxPatch((cx - bw / 2, body_top), bw, head_h,
                            boxstyle="round,pad=0,rounding_size=0.015",
                            linewidth=0, facecolor=col, zorder=3)
        ax.add_patch(hb)
        if st.get("kicker"):
            _text(ax, cx, top - 3.6, st["kicker"].upper(), size=8.0, color=PAPER,
                  weight="bold", family=SANS, va="center")
        _text(ax, cx, body_top + head_h * 0.36, st["title"], size=11.0, color=PAPER,
              weight="bold", family=SERIF, va="center")
        # bullets
        bullets = st.get("bullets", [])
        by = body_top - 6
        for b in bullets:
            ax.scatter([cx - bw / 2 + 4], [by], s=26, marker="s", color=col, zorder=5)
            # wrap bullet text
            txt = _wrap_to(b, 22)
            _text(ax, cx - bw / 2 + 6.5, by, txt, size=9.0, color=INK, ha="left",
                  va="top")
            by -= 6.0 + 4.0 * txt.count("\n")
        if st.get("footer"):
            _text(ax, cx - bw / 2 + 4, bottom + 3.2, _wrap_to(st["footer"], 30),
                  size=8.4, color=MUTED, style="italic", ha="left", va="bottom")
        # chevron arrow to next
        if i < n - 1:
            ax_x = cx + bw / 2 + gap / 2
            ay = (top + bottom) / 2
            ax.annotate("", xy=(ax_x + 1.6, ay), xytext=(ax_x - 1.6, ay),
                        arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=3.4,
                                        mutation_scale=22, shrinkA=0, shrinkB=0),
                        zorder=6)

    _legend(fig, [(f"{st.get('kicker','')}: {st['title']}",
                   tone_map.get(st.get("tone", "neutral"), INDIGO), "sq")
                  for st in stages], y_fig=0.115, size=8.4)
    return fig


def _wrap_to(s, width):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return "\n".join(lines)


# =============================================================== 5. FLOW BRIDGE
def c_flow_bridge(p, accent):
    """Vertical causal chain: stacked step boxes each with a +/-/result direction node
    and a down-arrow to the next; final emphasized result box."""
    steps = p["steps"]; n = len(steps)
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.2, max(5.6, 1.2 * n + 2.8)),
                      rect=(0.03, 0.155, 0.94, 0.66))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    tone_c = {"up": TEAL, "down": BRICK, "result": NAVY}
    tone_sym = {"up": "+", "down": "\u2212"}   # +, minus-sign (result uses a drawn star)
    top, bot = 94, 4
    box_h = (top - bot) / n - 2.2
    node_x = 9.0
    box_x0 = 17.0
    box_x1 = 97.0
    box_cx = (box_x0 + box_x1) / 2
    box_w = box_x1 - box_x0
    ys = np.linspace(top - box_h / 2, bot + box_h / 2, n)
    for i, (st, yc) in enumerate(zip(steps, ys)):
        tone = st.get("tone", "up")
        col = tone_c.get(tone, TEAL)
        is_res = tone == "result"
        # box
        if is_res:
            _box(ax, box_cx, yc, box_w, box_h, fc=NAVY, ec=NAVY, lw=1.4, pad=0.01, z=3)
            # gold top rule
            ax.plot([box_x0 + 0.6, box_x1 - 0.6], [yc + box_h / 2 - 0.8,
                    yc + box_h / 2 - 0.8], color=GOLD, lw=2.6, zorder=5,
                    solid_capstyle="round")
            head_col, sub_col = PAPER, "#D8DEEC"
        else:
            _box(ax, box_cx, yc, box_w, box_h, fc="#EFEDE6", ec=GRID, lw=1.0, pad=0.01, z=2)
            # left accent bar
            ax.add_patch(Rectangle((box_x0, yc - box_h / 2), 0.9, box_h,
                         facecolor=col, edgecolor="none", zorder=4))
            head_col, sub_col = NAVY, MUTED
        # direction node on the left: scatter marker stays round in display space
        ax.scatter([node_x], [yc], s=340, color=col, zorder=5)
        if is_res:
            ax.scatter([node_x], [yc], s=190, marker="*", color=PAPER, zorder=6)
        else:
            _text(ax, node_x, yc, tone_sym.get(tone, "+"), size=14, color=PAPER,
                  weight="bold", family=SANS)
        # texts
        head = _wrap_to(st["text"], 46)
        _text(ax, box_x0 + 3.2, yc + box_h * 0.16, head, size=10.2, color=head_col,
              weight="bold", ha="left", va="center")
        if st.get("sub"):
            _text(ax, box_x0 + 3.2, yc - box_h * 0.28, _wrap_to(st["sub"], 54),
                  size=8.8, color=sub_col, ha="left", va="center")
        # arrow to next
        if i < n - 1:
            y_from = yc - box_h / 2
            y_to = ys[i + 1] + box_h / 2
            nxt_tone = steps[i + 1].get("tone", "up")
            _arrow(ax, (node_x, y_to), (node_x, y_from),
                   color=tone_c.get(nxt_tone, MUTED), lw=1.8, mut=15)

    _legend(fig, [
        ("Tác động làm tăng", TEAL, "sq"),
        ("Tác động làm giảm", BRICK, "sq"),
        ("Kết quả cuối cùng", NAVY, "sq"),
    ], y_fig=0.088, size=8.4)
    return fig


# ==================================================================== 6. SANKEY
def c_sankey(p, accent):
    """Flows from sources (left) to uses (right); tapered bands whose width is
    proportional to value. Simple bipartite."""
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.8, 6.7),
                      rect=(0.03, 0.135, 0.94, 0.66))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    sources = p["sources"]; targets = p["targets"]; flows = p["flows"]
    cols = palette(accent)
    src_col = {}
    for i, s in enumerate(sources):
        src_col[s["name"]] = s.get("color", cols[i % len(cols)])

    x_src, x_dst = 20.0, 80.0
    bar_w = 2.4
    top, bot = 90, 7
    gap = 8.4
    tot_src = sum(float(s["value"]) for s in sources)
    tot_dst = sum(float(t["value"]) for t in targets)
    scale = ((top - bot) - gap * (max(len(sources), len(targets)) - 1)) / max(tot_src, tot_dst)

    # place source bars top->down
    src_pos = {}; y = top
    for s in sources:
        h = float(s["value"]) * scale
        ax.add_patch(Rectangle((x_src - bar_w, y - h), bar_w, h,
                     facecolor=src_col[s["name"]], edgecolor="none", zorder=5))
        src_pos[s["name"]] = {"top": y, "bot": y - h, "cur": y, "h": h}
        cy = y - h / 2
        _text(ax, x_src - bar_w - 1.4, cy + 2.2, _wrap_to(s["name"], 18),
              size=9.0, color=INK, ha="right", va="bottom")
        _text(ax, x_src - bar_w - 1.4, cy - 2.2,
              fmt_value(s["value"], "cur", p.get("currency", "$")),
              size=9.4, color=src_col[s["name"]], family=MONO, weight="bold",
              ha="right", va="top")
        y -= h + gap

    dst_pos = {}; y = top
    for t in targets:
        h = float(t["value"]) * scale
        ax.add_patch(Rectangle((x_dst, y - h), bar_w, h,
                     facecolor=NAVY, edgecolor="none", zorder=5))
        dst_pos[t["name"]] = {"top": y, "bot": y - h, "cur": y, "h": h}
        cy = y - h / 2
        _text(ax, x_dst + bar_w + 1.4, cy + 2.2, _wrap_to(t["name"], 18),
              size=9.0, color=INK, ha="left", va="bottom")
        _text(ax, x_dst + bar_w + 1.4, cy - 2.2,
              fmt_value(t["value"], "cur", p.get("currency", "$")),
              size=9.4, color=NAVY, family=MONO, weight="bold", ha="left", va="top")
        y -= h + gap

    # bands
    for f in flows:
        s = src_pos[f["src"]]; t = dst_pos[f["dst"]]
        h = float(f["value"]) * scale
        y0a = s["cur"]; y0b = s["cur"] - h; s["cur"] -= h
        y1a = t["cur"]; y1b = t["cur"] - h; t["cur"] -= h
        col = src_col[f["src"]]
        xa, xb = x_src, x_dst
        # cubic bezier band (top edge and bottom edge)
        cx = (xa + xb) / 2
        verts = [
            (xa, y0a), (cx, y0a), (cx, y1a), (xb, y1a),      # top edge L->R
            (xb, y1b),                                        # down right
            (cx, y1b), (cx, y0b), (xa, y0b),                 # bottom edge R->L
            (xa, y0a),                                        # close
        ]
        codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
                 MplPath.LINETO,
                 MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
                 MplPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MplPath(verts, codes), facecolor=col, edgecolor="none",
                     alpha=0.42, zorder=2))

    _layer_headers(ax, [x_src - bar_w / 2, x_dst + bar_w / 2],
                   [p.get("src_header", "Nguồn"), p.get("dst_header", "Sử dụng")],
                   top + 2.2, color=NAVY)
    _legend(fig, [(s["name"], src_col[s["name"]], "sq") for s in sources]
                 + [(p.get("dst_legend", "Khoản sử dụng"), NAVY, "sq")], y_fig=0.085, size=8.3)
    return fig


# ================================================================== 7. TIMELINE
def c_timeline(p, accent):
    """Horizontal milestone timeline: a spine, dated markers alternating above/below
    with title + date; done (filled) vs pending (hollow)."""
    ms = p["milestones"]; n = len(ms)
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.6, 5.4),
                      rect=(0.03, 0.06, 0.94, 0.72))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    xs = np.linspace(8, 92, n)
    spine_y = 50
    # split spine: navy up to last done, grey after
    last_done = -1
    for i, m in enumerate(ms):
        if m.get("done"):
            last_done = i
    if last_done >= 0:
        ax.plot([xs[0], xs[last_done]], [spine_y, spine_y], color=NAVY, lw=3.0,
                zorder=2, solid_capstyle="round")
    seg_start = max(0, last_done)
    ax.plot([xs[seg_start], xs[-1]], [spine_y, spine_y], color=GRID, lw=3.0,
            zorder=1, solid_capstyle="round")

    def _check(cx, cy):
        """Crisp check mark via a scatter marker built from a Path (font-independent,
        aspect-proof: marker paths render in display space)."""
        from matplotlib.path import Path as _P
        verts = [(-0.5, 0.02), (-0.16, -0.4), (0.52, 0.46)]
        tick = _P(verts, [_P.MOVETO, _P.LINETO, _P.LINETO])
        ax.scatter([cx], [cy], marker=tick, s=150, facecolor="none",
                   edgecolors=PAPER, linewidths=1.8, zorder=7)

    for i, (m, x) in enumerate(zip(ms, xs)):
        above = (i % 2 == 0)
        done = m.get("done")
        sgn = 1 if above else -1
        va = "bottom" if above else "top"
        # marker
        if done:
            ax.scatter([x], [spine_y], s=330, color=NAVY, zorder=5)
            _check(x, spine_y)
        else:
            ax.scatter([x], [spine_y], s=330, facecolor=PAPER, edgecolor=NAVY,
                       linewidth=2.0, zorder=5)
            ax.scatter([x], [spine_y], s=26, color=NAVY, zorder=6)
        # dotted stem from marker toward the label block
        stem_end = spine_y + sgn * 9
        ax.plot([x, x], [spine_y + sgn * 4, stem_end], color=FAINT,
                lw=1.0, ls=(0, (2, 2)), zorder=2)
        # label block, ordered outward from the spine: caption (nearest) -> title ->
        # date (farthest), matching the reference reading order top-to-bottom for
        # 'above' markers (date highest) and bottom-to-top for 'below'.
        title = _wrap_to(m["title"], 16); tl = title.count("\n") + 1
        y_cap = spine_y + sgn * 11
        if m.get("caption"):
            _text(ax, x, y_cap, m["caption"], size=8.6, color=GOLD, style="italic", va=va)
            y_title = y_cap + sgn * 6.0
        else:
            y_title = y_cap
        _text(ax, x, y_title, title, size=9.6, color=NAVY, weight="bold", va=va)
        y_date = y_title + sgn * (6.5 * tl)
        _text(ax, x, y_date, str(m["date"]).replace(".", ","), size=9.2, color=NAVY,
              family=MONO, weight="bold", va=va)

    _legend(fig, [
        ("Đã hoàn thành", NAVY, "circle"),
        ("Sắp tới (chưa thực hiện)", FAINT, "circle"),
    ], y_fig=0.115, size=8.6)
    return fig


# =================================================================== 8. LATTICE
def c_lattice(p, accent):
    """Labeled binomial (recombining) lattice: nodes on a triangular grid, node values,
    up/down edges, optional up-prob label; terminal payoffs highlighted."""
    levels = p["levels"]; nL = len(levels)
    fig, ax = eir_fig(_meta(p, accent), figsize=(9.6, 6.3),
                      rect=(0.03, 0.155, 0.94, 0.63))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    xs = np.linspace(10, 90, nL)
    top, bot = 84, 24
    vstep = (top - bot) / max(1, (nL - 1))     # vertical spacing per rank
    # node positions: level t has t+1 nodes, centred
    pos = {}
    for t, col in enumerate(levels):
        m = len(col)
        cy = (top + bot) / 2
        # spread nodes symmetrically; node j (0=top)
        yy = [cy + (m - 1) / 2 * (vstep) - j * vstep for j in range(m)]
        for j, (v, y) in enumerate(zip(col, yy)):
            pos[(t, j)] = (xs[t], y, v)

    up_c, dn_c = TEAL, BRICK
    # edges: node (t,j) -> (t+1,j) [up] and (t+1,j+1) [down]
    for t in range(nL - 1):
        for j in range(len(levels[t])):
            xa, ya, _ = pos[(t, j)]
            xu, yu, _ = pos[(t + 1, j)]
            xd, yd, _ = pos[(t + 1, j + 1)]
            ax.plot([xa, xu], [ya, yu], color=up_c, lw=1.5, zorder=2,
                    solid_capstyle="round")
            ax.plot([xa, xd], [ya, yd], color=dn_c, lw=1.5, zorder=2,
                    solid_capstyle="round")

    # first up/down factor labels
    if p.get("up_factor") is not None or p.get("down_factor") is not None:
        xa, ya, _ = pos[(0, 0)]; xu, yu, _ = pos[(1, 0)]; xd, yd, _ = pos[(1, 1)]
        if p.get("up_factor") is not None:
            _text(ax, (xa + xu) / 2, (ya + yu) / 2 + 2.5,
                  f"u = {p['up_factor']}".replace(".", ","), size=9.2, color=GOLD,
                  style="italic", family=MONO, va="bottom")
        if p.get("down_factor") is not None:
            _text(ax, (xa + xd) / 2, (ya + yd) / 2 - 2.5,
                  f"d = {p['down_factor']}".replace(".", ","), size=9.2, color=GOLD,
                  style="italic", family=MONO, va="top")

    # nodes (draw after edges so boxes sit on top)
    bw, bh = 12.5, 6.0
    for t, col in enumerate(levels):
        m = len(col)
        for j, v in enumerate(col):
            x, y, val = pos[(t, j)]
            ec, lw = NAVY, 1.3
            if t == 0:
                ec, lw = BRICK, 1.8            # root highlighted
            elif t == nL - 1:
                ec = up_c if j == 0 else dn_c if j == m - 1 else NAVY
                lw = 1.7 if (j == 0 or j == m - 1) else 1.3
            _box(ax, x, y, bw, bh, fc=PAPER, ec=ec, lw=lw, pad=0.06, z=5)
            _text(ax, x, y, str(val).replace(".", ","), size=9.4, color=INK,
                  family=MONO, weight="bold")

    # time axis labels
    xlabs = p.get("x_labels") or [f"t = {i}" for i in range(nL)]
    for x, lab in zip(xs, xlabs):
        _text(ax, x, bot - 8, str(lab).replace(".", ","), size=9.0, color=MUTED,
              family=MONO, va="top")
    if p.get("x_axis_label"):
        _text(ax, 50, bot - 14, p["x_axis_label"], size=9.0, color=MUTED, va="top")

    # up-prob rule at top-right
    if p.get("up_prob") is not None:
        ax.plot([54, 92], [top + 4.0, top + 4.0], color=GOLD, lw=1.6, zorder=3)
        raw = str(p["up_prob"])
        pv = raw.replace(".", ",")
        try:
            q = 1 - float(raw.replace(",", ".")); qs = f"{q:.2f}".replace(".", ",")
        except Exception:
            qs = "1 - p"
        _text(ax, 92, top + 5.6,
              f"Xác suất trung lập rủi ro: p = {pv} → 1 - p = {qs}",
              size=9.2, color=INK, ha="right", va="bottom")

    _legend(fig, [
        ("Bước tăng (up)", TEAL, "line"),
        ("Bước giảm (down)", BRICK, "line"),
        ("Nút gốc / kết cục biên", BRICK, "sq"),
    ], y_fig=0.088, size=8.5)
    return fig


COMPONENTS = {
    "decision_tree": c_decision_tree,
    "flowchart": c_flowchart,
    "network_graph": c_network_graph,
    "mechanism_flow": c_mechanism_flow,
    "flow_bridge": c_flow_bridge,
    "sankey": c_sankey,
    "timeline": c_timeline,
    "lattice": c_lattice,
}


# ================================================================= showcase data
_SHOWCASE = {
    "decision_tree": {
        "kicker": "Corporate Finance · Quyền chọn thực · Module 4",
        "title": "Quyền chọn từ bỏ dự án: tiếp tục hay thanh lý sau năm đầu",
        "subtitle": ("Sau khi quan sát kết quả năm đầu, ban quản trị chọn tiếp tục vận "
                     "hành hoặc từ bỏ và thanh lý. Nút vuông là điểm quyết định, nút nhỏ "
                     "là điểm thị trường phân giải với xác suất. Giá trị là NPV (triệu USD)."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "layer_labels": ["Đầu tư ban đầu", "Kết quả năm 1", "Quyết định năm 1", ""],
        "tree": {
            "label": "Đầu tư dự án", "kind": "decision", "ev": "92,5",
            "children": [
                {"label": "Nhu cầu cao", "kind": "chance", "prob": "0,55", "ev": "142,0",
                 "optimal": True, "children": [
                     {"label": "Tiếp tục vận hành", "kind": "leaf", "value": "$142,0",
                      "tone": "up", "optimal": True},
                     {"label": "Từ bỏ và thanh lý", "kind": "leaf", "value": "$60,0",
                      "tone": "down"},
                 ]},
                {"label": "Nhu cầu thấp", "kind": "chance", "prob": "0,45", "ev": "32,0",
                 "children": [
                     {"label": "Tiếp tục vận hành", "kind": "leaf", "value": "-$48,0",
                      "tone": "down"},
                     {"label": "Từ bỏ và thanh lý", "kind": "leaf", "value": "$32,0",
                      "tone": "up", "optimal": True},
                 ]},
            ],
        },
    },
    "flowchart": {
        "kicker": "Fixed Income · Quyền chọn đính kèm · §3.3",
        "title": "Quyết định gọi mua trái phiếu có thể thu hồi",
        "subtitle": ("Khi lãi suất thị trường giảm, tổ chức phát hành so sánh giá trái "
                     "phiếu với giá gọi mua để quyết định thu hồi."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "nodes": [
            {"id": "s", "kind": "start", "label": "Lãi suất thị trường giảm",
             "x": 50, "y": 90, "w": 40, "h": 12},
            {"id": "d", "kind": "decision",
             "label": "Giá trái phiếu vượt giá gọi mua?", "x": 50, "y": 60,
             "w": 42, "h": 30, "wrap": 16},
            {"id": "y1", "kind": "process", "label": "Tổ chức phát hành thực hiện gọi mua",
             "x": 25, "y": 30, "w": 38, "h": 14, "wrap": 20},
            {"id": "n1", "kind": "process", "label": "Giữ trái phiếu đến đáo hạn",
             "x": 75, "y": 30, "w": 38, "h": 14, "wrap": 20},
            {"id": "y2", "kind": "terminal", "tone": "down",
             "label": "Nhà đầu tư đối mặt rủi ro tái đầu tư ở lãi suất thấp hơn",
             "x": 25, "y": 9, "w": 40, "h": 16, "wrap": 22},
            {"id": "n2", "kind": "terminal", "tone": "up",
             "label": "Dòng tiền coupon tiếp tục như cũ",
             "x": 75, "y": 9, "w": 40, "h": 16, "wrap": 22},
        ],
        "edges": [
            {"from": "s", "to": "d"},
            {"from": "d", "to": "y1", "from_side": "left", "label": "Có", "ly": 3},
            {"from": "d", "to": "n1", "from_side": "right", "label": "Không", "ly": 3},
            {"from": "y1", "to": "y2"},
            {"from": "n1", "to": "n2"},
        ],
    },
    "network_graph": {
        "kicker": "Fixed Income · Chứng khoán hóa · §6.1",
        "title": "Cấu trúc giao dịch chứng khoán hóa",
        "subtitle": ("Tài sản gốc được bán sang pháp nhân có mục đích đặc biệt (SPV), rồi "
                     "phân tầng thành các lớp ưu tiên thanh toán khác nhau."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "box_w": 30, "box_h": 12,
        "layers": [
            [{"id": "pool", "label": "Danh mục tài sản gốc", "w": 34}],
            [{"id": "spv", "label": "Pháp nhân SPV", "w": 30}],
            [{"id": "aaa", "label": "Lớp ưu tiên (AAA)", "tone": "up", "w": 26},
             {"id": "bbb", "label": "Lớp trung gian (BBB)", "tone": "hi", "w": 27},
             {"id": "eq", "label": "Lớp vốn cổ phần", "tone": "down", "w": 25}],
        ],
        "edges": [
            {"from": "pool", "to": "spv", "label": "Bán đứt"},
            {"from": "spv", "to": "aaa", "label": "Trả trước"},
            {"from": "spv", "to": "bbb", "label": "Ưu tiên giữa"},
            {"from": "spv", "to": "eq", "label": "Hấp thụ lỗ"},
        ],
    },
    "mechanism_flow": {
        "kicker": "Equity · Module 4 · §2.3",
        "title": "Cơ chế định giá chiết khấu dòng tiền (DCF)",
        "subtitle": ("Từ ba nhóm đầu vào cốt lõi, mô hình chiết khấu dòng tiền tự do về "
                     "hiện tại để cho ra giá trị nội tại mỗi cổ phiếu."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "stages": [
            {"tone": "input", "kicker": "Đầu vào", "title": "Dữ liệu đầu vào",
             "bullets": ["Dòng tiền tự do của hãng (FCFF) dự phóng 5 năm",
                         "Tốc độ tăng trưởng dài hạn g = 3,0%",
                         "Chi phí vốn bình quân WACC = 9,0%"],
             "footer": "Nguồn: báo cáo tài chính và giả định nhà phân tích"},
            {"tone": "process", "kicker": "Xử lý", "title": "Quá trình chiết khấu",
             "bullets": ["Chiết khấu từng dòng tiền về hiện tại theo WACC",
                         "Tính giá trị cuối kỳ bằng mô hình Gordon",
                         "Cộng dồn thành giá trị doanh nghiệp (EV)"],
             "footer": "Áp dụng công thức PV = CF / (1 + WACC)^t"},
            {"tone": "output", "kicker": "Đầu ra", "title": "Giá trị nội tại",
             "bullets": ["Trừ nợ ròng để ra giá trị vốn chủ sở hữu",
                         "Chia cho số cổ phiếu lưu hành",
                         "Giá trị nội tại ước tính 168 USD mỗi cổ phiếu"],
             "footer": "So sánh với giá thị trường để ra khuyến nghị"},
        ],
    },
    "flow_bridge": {
        "kicker": "Fixed Income · Cơ chế truyền dẫn lãi suất",
        "title": "Vì sao tăng lãi suất chính sách lại gây lỗ định giá trên trái phiếu",
        "subtitle": ("Chuỗi nhân quả từ quyết định của ngân hàng trung ương đến khoản lỗ "
                     "ghi nhận theo giá thị trường (mark-to-market) trên danh mục nắm giữ."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "steps": [
            {"tone": "up", "text": "Ngân hàng trung ương tăng lãi suất điều hành thêm 0,75 điểm phần trăm",
             "sub": "Phản ứng trước áp lực lạm phát; lãi suất ngắn hạn lập tức đi lên."},
            {"tone": "up", "text": "Lợi suất yêu cầu (tỷ lệ chiết khấu) trên toàn đường cong tăng lên",
             "sub": "Nhà đầu tư đòi hỏi lợi suất cao hơn cho mọi kỳ hạn để bù đắp."},
            {"tone": "down", "text": "Giá trái phiếu giảm do dòng tiền tương lai bị chiết khấu nặng hơn",
             "sub": "Quan hệ nghịch giữa giá và lợi suất: lợi suất tăng thì giá giảm."},
            {"tone": "result", "text": "Ghi nhận khoản lỗ định giá theo giá thị trường (MTM) trên danh mục",
             "sub": "Trái phiếu kỳ hạn dài, duration cao chịu mức sụt giá lớn nhất."},
        ],
    },
    "sankey": {
        "kicker": "Financial Reporting · Báo cáo lưu chuyển tiền tệ",
        "title": "Dòng tiền của doanh nghiệp: nguồn tạo ra so với cách phân bổ",
        "subtitle": ("Tiền tạo ra từ hoạt động kinh doanh và huy động nợ mới được phân bổ "
                     "cho chi tiêu vốn, cổ tức, mua lại cổ phiếu và trả nợ gốc. "
                     "Bề rộng mỗi dải tỷ lệ thuận với giá trị dòng tiền."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note", "currency": "$",
        "src_header": "Nguồn tiền", "dst_header": "Sử dụng tiền",
        "dst_legend": "Khoản sử dụng",
        "sources": [
            {"name": "Dòng tiền hoạt động (CFO)", "value": 720, "color": NAVY},
            {"name": "Huy động nợ mới", "value": 280, "color": BRICK},
            {"name": "Thanh lý tài sản", "value": 90, "color": TEAL},
        ],
        "targets": [
            {"name": "Chi tiêu vốn (CapEx)", "value": 480},
            {"name": "Cổ tức trả cho cổ đông", "value": 210},
            {"name": "Mua lại cổ phiếu quỹ", "value": 150},
            {"name": "Trả nợ gốc", "value": 160},
            {"name": "Tăng tiền mặt dự trữ", "value": 90},
        ],
        "flows": [
            {"src": "Dòng tiền hoạt động (CFO)", "dst": "Chi tiêu vốn (CapEx)", "value": 420},
            {"src": "Dòng tiền hoạt động (CFO)", "dst": "Cổ tức trả cho cổ đông", "value": 210},
            {"src": "Dòng tiền hoạt động (CFO)", "dst": "Mua lại cổ phiếu quỹ", "value": 90},
            {"src": "Huy động nợ mới", "dst": "Chi tiêu vốn (CapEx)", "value": 60},
            {"src": "Huy động nợ mới", "dst": "Mua lại cổ phiếu quỹ", "value": 60},
            {"src": "Huy động nợ mới", "dst": "Trả nợ gốc", "value": 160},
            {"src": "Thanh lý tài sản", "dst": "Tăng tiền mặt dự trữ", "value": 90},
        ],
    },
    "timeline": {
        "kicker": "Fixed Income · Quy định · §6.1",
        "title": "Lộ trình áp dụng chuẩn vốn Basel III",
        "subtitle": ("Năm giai đoạn triển khai khung vốn và thanh khoản. Các mốc đã hoàn "
                     "thành được tô đặc màu chàm; các mốc sắp tới để rỗng."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "milestones": [
            {"date": "Quý 1, 2023", "title": "Công bố khung quy định",
             "caption": "BIS ban hành", "done": True},
            {"date": "Quý 4, 2023", "title": "Áp dụng tỷ lệ vốn lõi",
             "caption": "CET1 ≥ 7%", "done": True},
            {"date": "Quý 2, 2024", "title": "Bổ sung đệm dự phòng",
             "caption": "Đệm phản chu kỳ", "done": True},
            {"date": "Quý 1, 2025", "title": "Tỷ lệ thanh khoản LCR",
             "caption": "LCR ≥ 100%", "done": False},
            {"date": "Quý 1, 2026", "title": "Tuân thủ đầy đủ",
             "caption": "Hiệu lực toàn phần", "done": False},
        ],
    },
    "lattice": {
        "kicker": "Derivatives · Module 3 · §2.1",
        "title": "Cây nhị thức tái hợp: định giá quyền chọn",
        "subtitle": ("Giá tài sản cơ sở tiến triển qua ba bước với hệ số tăng u và giảm d. "
                     "Cây tái hợp gộp các nhánh, nên bước t có t+1 nút thay vì 2^t."),
        "source": "Minh họa của tác giả", "asof": "CFA Level II",
        "firm": "CFA Study Note",
        "up_factor": "1,2", "down_factor": "0,833", "up_prob": "0,55",
        "x_axis_label": "Số bước thời gian",
        "x_labels": ["t = 0", "t = 1", "t = 2", "t = 3"],
        "levels": [
            ["$50,00"],
            ["$60,00", "$41,65"],
            ["$72,00", "$49,98", "$34,69"],
            ["$86,40", "$59,98", "$41,63", "$28,90"],
        ],
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir",
                    default=os.path.join(os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__))), "gallery", "super", "diagram"))
    ap.add_argument("--only", default=None)
    ap.add_argument("--dpi", type=int, default=170)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR diagram components:", ", ".join(sorted(COMPONENTS))); return 0
    os.makedirs(args.out_dir, exist_ok=True)
    ok = fail = 0
    for key, fn in COMPONENTS.items():
        if args.only and key != args.only:
            continue
        params = _SHOWCASE.get(key, {})
        accent = params.get("accent") or TEAL
        try:
            fig = fn(params, accent)
            out = os.path.join(args.out_dir, f"{key}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL {key}: {e}\n"); fail += 1
    print(f"viz_eir_diagram: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
