#!/usr/bin/env python3
"""viz_eir_kpi.py, EIR KPI / SPARKLINE / ANNOTATION devices for CFA study notes.

Dense dashboard cells with mini trends, plus annotated narrative devices. Static
matplotlib PNGs (Agg), cream paper, editorial-institutional-research design language
(FT / Bloomberg / Goldman / Morningstar / The Economist) on the warm CFA palette.

Shares the chrome and tokens of viz_eir.py (kicker / serif headline / subtitle / source
line), honours the subject accent, reads the SAME spec.json contract, so a note may mix
core + EIR + these devices in one spec.

Editorial meta keys live inside params: title, kicker, subtitle, source, asof, rating,
firm. Data keys drive the device.

Components:
  kpi_card_with_sparkline, grid of KPI cards (big number + delta + sparkline beneath).
  sparkline_row, compact table: label | inline sparkline | value | status.
  annotated_narrative, editorial prose with inline colour+bold number runs.
  anomaly_callout, single time series with one boxed callout on an anomaly.
  stat_dashboard, dashboard header of big-stat cells, each with a mini spark/bar.

Usage:
  python3 viz_eir_kpi.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_eir_kpi.py --out-dir OUT        # renders the built-in _SHOWCASE
  python3 viz_eir_kpi.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _eir_style as S
from _eir_style import (
    PAPER, PAPER_HI, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge,
)
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle, FancyBboxPatch

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved

# 4th narrative tone: neutral/"trung tinh" (distinct from GOLD annotation). Dan
# xuat truc tiep = MUTED (COLORS["ink_md"]): gia tri cu la mot mau xam-xanh gan
# nhu trung voi MUTED va cung mang y nghia "lam ban dong dieu" giong nhau.
STEEL = MUTED


# --------------------------------------------------------------------- helpers
def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


def _delta_arrow(tone):
    # ▲▼ exist in Noto mono; • for flat. Never use glyphs Lato lacks (e.g. ▮).
    return {"up": "▲", "down": "▼", "flat": "•", "pos": "▲", "neg": "▼"}.get(tone, "")


def _spark(ax, vals, accent, fill=True, dot=True, minmax=False, lw=2.0,
           baseline=True, dotcolor=None):
    """Draw a bare sparkline into a dedicated axes: no spines, no ticks. Navy line,
    optional light fill to the series-minimum baseline, dotted baseline hairline,
    end-dot at the last point, optional min/max markers. ax.margins keeps headroom."""
    ax.axis("off")
    v = np.asarray(vals, dtype=float)
    n = len(v)
    if n == 0:
        return
    x = np.arange(n)
    lo = float(v.min())
    if fill and n > 1:
        ax.fill_between(x, v, lo, color=GRID, alpha=0.85, linewidth=0, zorder=1)
    if baseline and n > 1:
        ax.plot([0, n - 1], [lo, lo], color=FAINT, lw=0.8, ls=(0, (2, 2)), zorder=2)
    ax.plot(x, v, color=NAVY, lw=lw, solid_capstyle="round",
            solid_joinstyle="round", zorder=3)
    if minmax and n > 1:
        imax = int(v.argmax()); imin = int(v.argmin())
        ax.scatter([imax], [v[imax]], s=16, color=TEAL, zorder=4)
        ax.scatter([imin], [v[imin]], s=16, color=BRICK, zorder=4)
    if dot:
        ax.scatter([n - 1], [v[-1]], s=34, color=(dotcolor or GOLD),
                   zorder=5, edgecolors=PAPER, linewidths=0.8)
    pad = (v.max() - lo) or 1.0
    ax.set_xlim(-0.6, n - 1 + 0.9)
    ax.set_ylim(lo - pad * 0.18, v.max() + pad * 0.30)


def _sparkline_legend(fig, y=0.10, accent=None,
                      up_lbl="Diễn biến thuận lợi", down_lbl="Diễn biến bất lợi"):
    """Bottom legend row used by the sparkline devices: line swatch + end-dot + up/down."""
    setup_fonts()
    x = 0.045
    items = [("line", NAVY, "Xu hướng trong kỳ"),
             ("dot", GOLD, "Giá trị mới nhất"),
             ("sq", TEAL, up_lbl),
             ("sq", BRICK, down_lbl)]
    for kind, col, lbl in items:
        if kind == "line":
            fig.add_artist(mlines.Line2D([x, x + 0.028], [y, y], color=col, lw=2.4,
                                         solid_capstyle="round", transform=fig.transFigure))
            xs = x + 0.036
        elif kind == "dot":
            fig.add_artist(mlines.Line2D([x + 0.012], [y], marker="o", ms=6.5, color=col,
                                         mec=PAPER, mew=0.8, transform=fig.transFigure))
            xs = x + 0.030
        else:
            fig.add_artist(Rectangle((x, y - 0.011), 0.017, 0.022, facecolor=col,
                                     edgecolor="none", transform=fig.transFigure))
            xs = x + 0.026
        fig.text(xs, y, lbl, fontsize=8.5, color=INK, family=SANS, ha="left", va="center")
        x = xs + 0.011 * len(lbl) + 0.028


# ================================================================== 1. KPI CARDS
def c_kpi_card_with_sparkline(p, accent):
    """Grid of KPI cards; each = label + big MONO value + delta (▲▼) + sparkline beneath
    + a small italic caption. Flat cream cells with a GOLD left accent bar and hairline
    frame (no shadow / no rounding)."""
    from matplotlib.gridspec import GridSpec
    cards = p["cards"]
    n = len(cards)
    ncol = int(p.get("ncols", 2 if n > 3 else n))
    ncol = max(1, min(ncol, n))
    nrow = (n + ncol - 1) // ncol
    fig = plt.figure(figsize=(min(11.0, 4.9 * ncol + 1.2), 2.15 * nrow + 2.5),
                     facecolor=PAPER)
    m = _meta(p, accent)
    m.setdefault("firm", "CFA STUDY NOTE")
    draw_masthead(fig, m, top=0.965)
    draw_source(fig, m)
    _sparkline_legend(fig, y=0.075, accent=accent)
    setup_fonts()
    gs = GridSpec(nrow, ncol, figure=fig, left=0.045, right=0.965, top=0.70,
                  bottom=0.135, hspace=0.30, wspace=0.10)
    for i, card in enumerate(cards):
        r, c = divmod(i, ncol)
        cell = fig.add_subplot(gs[r, c]); cell.axis("off")
        cell.set_xlim(0, 1); cell.set_ylim(0, 1)
        # flat cell ground + hairline frame + GOLD accent spine on the left
        cell.add_patch(Rectangle((0.012, 0.03), 0.976, 0.94, facecolor=PAPER_HI,
                                 edgecolor=GRID, linewidth=1.0, zorder=1))
        cell.add_patch(Rectangle((0.012, 0.03), 0.012, 0.94, facecolor=GOLD,
                                 edgecolor="none", zorder=2))
        pad = 0.055
        cell.text(pad, 0.90, card.get("label", "").upper(), fontsize=9.5, color=MUTED,
                  family=SANS, fontweight="bold", ha="left", va="top", zorder=3)
        cell.text(pad, 0.68, str(card.get("value", "")), fontsize=22, color=NAVY,
                  family=MONO, fontweight="bold", ha="left", va="center", zorder=3)
        d = card.get("delta")
        if d:
            tone = card.get("tone", "flat")
            cell.text(pad, 0.475, f"{_delta_arrow(tone)} {d}", fontsize=11.5,
                      color=tone_color(tone, accent), family=MONO, fontweight="bold",
                      ha="left", va="center", zorder=3)
        # sparkline strip pinned to the lower band of the cell (axes-fraction inset)
        spark = card.get("spark") or []
        if spark:
            pos = cell.get_position()
            sx = pos.x0 + pos.width * (pad + 0.02)
            sw = pos.width * 0.90
            sy = pos.y0 + pos.height * 0.135
            sh = pos.height * 0.24
            sax = fig.add_axes([sx, sy, sw, sh])
            _spark(sax, spark, accent, fill=True, dot=True, lw=2.0)
        cap = card.get("caption")
        if cap:
            cell.text(pad, 0.075, cap, fontsize=8.6, color=MUTED, family=SANS,
                      style="italic", ha="left", va="center", zorder=3)
    return fig


# ============================================================== 2. SPARKLINE ROW
def c_sparkline_row(p, accent):
    """Compact table: one row per metric = label | inline sparkline | value (MONO) |
    status word (tăng/giảm/đi ngang, tone-coloured) + delta arrow. Hairline dividers
    between rows; merges the sparkline_row + inline_sparkline_text ideas into one row."""
    rows = p["rows"]
    n = len(rows)
    fig = plt.figure(figsize=(9.6, 1.15 * n + 2.7), facecolor=PAPER)
    m = _meta(p, accent)
    m.setdefault("firm", "CFA STUDY NOTE")
    draw_masthead(fig, m, top=0.965)
    draw_source(fig, m)
    _sparkline_legend(fig, y=0.070, accent=accent,
                      up_lbl="Tăng so với đầu kỳ", down_lbl="Giảm so với đầu kỳ")
    setup_fonts()
    top = 0.66
    bot = 0.135
    band = (top - bot) / n
    # column geometry (figure fraction)
    x_label = 0.048
    x_spark0, x_spark1 = 0.365, 0.605
    x_value = 0.760           # right edge of the MONO value (ha="right")
    x_status = 0.790          # left edge of status arrow + word
    fig.add_artist(mlines.Line2D([0.045, 0.965], [top, top], color=GRID, lw=0.9,
                                 transform=fig.transFigure))
    for i, row in enumerate(rows):
        yc = top - band * (i + 0.5)
        # row divider (below each row)
        fig.add_artist(mlines.Line2D([0.045, 0.965], [top - band * (i + 1),
                       top - band * (i + 1)], color=GRID, lw=0.9,
                       transform=fig.transFigure))
        fig.text(x_label, yc, row.get("label", ""), fontsize=11, color=INK,
                 family=SANS, ha="left", va="center")
        tone = row.get("tone", "flat")
        # inline sparkline axes for this row (end-dot uniform GOLD per the legend)
        sh = band * 0.62
        sax = fig.add_axes([x_spark0, yc - sh / 2, x_spark1 - x_spark0, sh])
        _spark(sax, row.get("spark") or [], accent, fill=True, dot=True, lw=1.9,
               dotcolor=GOLD)
        fig.text(x_value, yc, str(row.get("value", "")), fontsize=13, color=NAVY,
                 family=MONO, fontweight="bold", ha="right", va="center")
        status = row.get("status") or {"up": "tăng", "down": "giảm",
                                        "flat": "đi ngang"}.get(tone, "")
        col = tone_color(tone, accent) if tone in ("up", "down", "pos", "neg") else STEEL
        # arrow glyph in MONO (Noto has ▲▼; Lato does not -> would tofu); word in SANS
        arr = _delta_arrow(tone)
        if arr:
            fig.text(x_status, yc, arr, fontsize=10.5, color=col, family=MONO,
                     fontweight="bold", ha="left", va="center")
        fig.text(x_status + 0.022, yc, status, fontsize=11, color=col, family=SANS,
                 fontweight="bold", ha="left", va="center")
    return fig


# ============================================================ 3. ANNOTATED NARRATIVE
def _tone_run_color(tone, accent):
    if tone in ("up", "pos"):
        return TEAL
    if tone in ("down", "neg"):
        return BRICK
    if tone in ("emph", "highlight"):
        return INDIGO
    if tone in ("neutral", "flat"):
        return STEEL
    return None


def c_annotated_narrative(p, accent):
    """Editorial commentary panel: a title + a paragraph where KEY NUMBER runs are
    emphasised inline (bold + tone colour, teal up, brick down, indigo emphasis, steel
    neutral). Runs are laid out line-by-line with a running x cursor (advance by an
    estimated width), wrapping at the right margin; a gold left-bar frames the block and
    a 4-item legend sits beneath."""
    runs = p["runs"]                      # list of [text, tone|None, bold]
    fig = plt.figure(figsize=(9.8, float(p.get("height", 5.4))), facecolor=PAPER)
    m = _meta(p, accent)
    draw_masthead(fig, m, top=0.965)
    draw_source(fig, m)
    setup_fonts()

    # --- text block geometry (figure fraction) --------------------------------
    x_left = 0.075
    x_right = 0.955
    y_top = float(p.get("y_top", 0.62))
    line_h = float(p.get("line_h", 0.072))
    base_fs = float(p.get("fontsize", 14.5))
    # per-character width factor (figure-fraction per char per pt), tuned by render.
    # bold/number runs read slightly wider; measured widths in mpl are unreliable so we
    # estimate and wrap on the estimate, then verify visually.
    fig_w_in = fig.get_size_inches()[0]
    dpi_ref = 100.0
    # width of one character ~ fontsize*0.52 pt -> inches -> figure fraction
    def _run_width(text, bold):
        k = 0.556 if bold else 0.512
        w_pt = base_fs * k * len(text)
        return (w_pt / 72.0) / fig_w_in

    space_w = _run_width(" ", False)
    x = x_left
    y = y_top
    max_x = x_right
    for text, tone, bold in runs:
        # normalise a run into word-tokens so we can wrap between words; keep the run's
        # leading/trailing spaces as explicit gaps.
        col = _tone_run_color(tone, accent) or INK
        weight = "bold" if (bold or tone) else "normal"
        # split but retain spacing behaviour: number runs are usually a single token
        tokens = text.split(" ")
        for ti, tok in enumerate(tokens):
            if tok == "":
                # represents a space between tokens / leading-trailing space
                x += space_w
                if x > max_x:
                    x = x_left; y -= line_h
                continue
            w = _run_width(tok, bold or bool(tone))
            if x + w > max_x and x > x_left + 1e-6:
                x = x_left
                y -= line_h
            fig.text(x, y, tok, fontsize=base_fs, color=col, family=SANS,
                     fontweight=weight, ha="left", va="baseline",
                     transform=fig.transFigure)
            x += w
            if ti != len(tokens) - 1:
                x += space_w
                if x > max_x:
                    x = x_left; y -= line_h
        # a single trailing space so adjacent runs don't collide
        x += space_w
        if x > max_x:
            x = x_left; y -= line_h

    # --- gold left accent bar spanning the used text height -------------------
    y_bot = y - line_h * 0.4
    fig.add_artist(mlines.Line2D([x_left - 0.020, x_left - 0.020],
                                 [y_top + line_h * 0.55, y_bot], color=GOLD, lw=3.4,
                                 solid_capstyle="round", transform=fig.transFigure))

    # --- legend ---------------------------------------------------------------
    leg_y = max(y_bot - line_h * 1.1, 0.115)
    fig.add_artist(mlines.Line2D([0.045, 0.965], [leg_y + line_h * 0.55,
                   leg_y + line_h * 0.55], color=GRID, lw=0.9, transform=fig.transFigure))
    lx = x_left - 0.020
    for col, lbl in [(TEAL, "Tích cực"), (BRICK, "Tiêu cực"),
                     (INDIGO, "Nhấn mạnh"), (STEEL, "Trung tính")]:
        fig.add_artist(Rectangle((lx, leg_y - 0.010), 0.016, 0.020, facecolor=col,
                                 edgecolor="none", transform=fig.transFigure))
        fig.text(lx + 0.024, leg_y, lbl, fontsize=9.5, color=INK, family=SANS,
                 fontweight="bold", ha="left", va="center")
        lx += 0.024 + 0.0115 * len(lbl) + 0.030
    return fig


# ============================================================== 4. ANOMALY CALLOUT
def c_anomaly_callout(p, accent):
    """Single time series with ONE annotated callout: a compact boxed note (kicker + bold
    head + wrapped body) with a short connector pointing at an anomaly point that is marked
    with a hollow ring + solid core (BRICK for a negative event, GOLD otherwise) and a
    dotted drop-line to the axis. Body text is wrapped to a fixed char budget so the box
    stays a tidy vertical card (never a page-wide flat strip)."""
    import textwrap
    x = p["x"]
    vals = list(map(float, p["values"]))
    ai = int(p["anomaly_index"])
    note = p.get("note", {})
    m = _meta(p, accent)
    fig, ax = eir_fig(m, figsize=(9.4, 6.0), rect=(0.11, 0.16, 0.83, 0.56))
    setup_fonts()
    xs = np.arange(len(x))
    line_col = p.get("line_color", STEEL)   # keep the series calm; the anomaly carries colour
    ax.plot(xs, vals, color=line_col, lw=2.4, solid_capstyle="round", zorder=3)
    ax.scatter(xs, vals, s=16, color=line_col, zorder=4)
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=9)
    yf = p.get("y_format")
    if yf == "bps":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}bps"))
    elif yf == "pct":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}%"))
    if p.get("xlabel"):
        ax.set_xlabel(p["xlabel"], fontsize=9, color=MUTED)
    ax.margins(x=0.02)
    y0, y1 = ax.get_ylim()
    span = y1 - y0

    amark = BRICK if note.get("negative", True) else GOLD
    # dotted drop line from the anomaly point down to the axis, then the ring + core
    ax.plot([ai, ai], [y0, vals[ai]], color=amark, lw=1.4, ls=(0, (2, 2)), zorder=2)
    ax.scatter([ai], [vals[ai]], s=190, facecolors="none", edgecolors=amark,
               linewidths=1.8, zorder=5)                       # hollow ring
    ax.scatter([ai], [vals[ai]], s=48, color=amark, zorder=6)  # solid core

    # ---- compose the box as ONE multi-line block (kicker / head / wrapped body) -------
    kick = note.get("kicker", "ĐỘT BIẾN").upper()
    head = note.get("headline", f"{x[ai]}: {fmt_value(vals[ai], yf or 'num')}")
    body = note.get("body", "")
    wrap = int(note.get("wrap", 30))
    body_lines = textwrap.wrap(body, wrap) if body else []

    # anchor the box to a side of the spike, in DATA coords; default = to the left & below
    dx = float(note.get("dx", -3.4))
    dy = float(note.get("dy", -0.30))       # fraction of span below the point
    bx = ai + dx
    by = vals[ai] + dy * span
    # keep the box fully inside the axes horizontally
    bx = max(xs[0] + 0.2, min(bx, xs[-1] - 0.2))

    # kicker (small accent caps) sits just above the head, inside the box top padding
    box_text = head + ("\n" + "\n".join(body_lines) if body_lines else "")
    # draw the body/head block with a boxed background; head rendered bold separately on top
    txt = ax.annotate(
        "\n".join(body_lines) if body_lines else " ",
        xy=(ai, vals[ai]), xytext=(bx, by), textcoords="data",
        fontsize=10.5, color=INK, family=SANS, ha="left", va="top", linespacing=1.25,
        bbox=dict(boxstyle="round,pad=0.7", fc=PAPER, ec=amark, lw=1.5),
        arrowprops=dict(arrowstyle="-", color=amark, lw=1.4, shrinkA=6, shrinkB=8,
                        connectionstyle="arc3,rad=0.12"),
        zorder=7, annotation_clip=False,
    )
    # place kicker + bold head ABOVE the body block, offset upward in points so they never
    # overlap the wrapped body (which starts at the anchor and flows down).
    ax.annotate(kick, xy=(bx, by), textcoords="offset points", xytext=(2, 34),
                fontsize=8, color=amark, family=SANS, fontweight="bold",
                ha="left", va="bottom", zorder=9, annotation_clip=False)
    ax.annotate(head, xy=(bx, by), textcoords="offset points", xytext=(2, 16),
                fontsize=11, color=NAVY, family=MONO, fontweight="bold",
                ha="left", va="bottom", zorder=9, annotation_clip=False)

    # direct series label at the tail
    ax.annotate(f" {p.get('series_name', 'Chuỗi thời gian')}", (xs[-1], vals[-1]),
                color=line_col, fontsize=9, va="center", fontweight="bold", zorder=4)
    return fig


def c_stat_dashboard(p, accent):
    """KPI dashboard header: 3-4 big-stat cells (label + big MONO value + delta + italic
    caption) separated by vertical hairlines, EACH carrying a tiny spark or bar strip.
    Richer sibling of kpi_strip; supports a 2-row option via `rows`."""
    stats = p["stats"]
    n = len(stats)
    per_row = int(p.get("per_row", n if n <= 4 else (n + 1) // 2))
    per_row = max(1, min(per_row, n))
    nrow = (n + per_row - 1) // per_row
    fig = plt.figure(figsize=(min(12.0, 3.15 * per_row + 0.8), 1.95 * nrow + 2.4),
                     facecolor=PAPER)
    m = _meta(p, accent)
    m.setdefault("firm", "CFA STUDY NOTE")
    draw_masthead(fig, m, top=0.965)
    draw_source(fig, m)
    setup_fonts()
    top = 0.66
    bot = 0.085
    row_h = (top - bot) / nrow
    left, right = 0.045, 0.965
    span = right - left
    # top hairline over the stat band
    fig.add_artist(mlines.Line2D([left, right], [top, top], color=GRID, lw=0.9,
                                 transform=fig.transFigure))
    for i, st in enumerate(stats):
        r, c = divmod(i, per_row)
        cw = span / per_row
        cx = left + c * cw
        cyt = top - r * row_h
        cyb = cyt - row_h
        # vertical hairline before each cell except the first in a row
        if c > 0:
            fig.add_artist(mlines.Line2D([cx, cx], [cyb + row_h * 0.10,
                           cyt - row_h * 0.06], color=GRID, lw=0.9,
                           transform=fig.transFigure))
        # bottom hairline under each row
        fig.add_artist(mlines.Line2D([left, right], [cyb, cyb], color=GRID, lw=0.9,
                       transform=fig.transFigure))
        pad = 0.028
        tx = cx + pad
        fig.text(tx, cyt - row_h * 0.14, st.get("label", "").upper(), fontsize=9.5,
                 color=MUTED, family=SANS, fontweight="bold", ha="left", va="top")
        fig.text(tx, cyt - row_h * 0.42, str(st.get("value", "")), fontsize=21,
                 color=NAVY, family=MONO, fontweight="bold", ha="left", va="center")
        d = st.get("delta")
        if d:
            tone = st.get("tone", "flat")
            fig.text(tx, cyt - row_h * 0.62, f"{_delta_arrow(tone)} {d}", fontsize=10.5,
                     color=tone_color(tone, accent), family=MONO, fontweight="bold",
                     ha="left", va="center")
        cap = st.get("caption")
        if cap:
            fig.text(tx, cyt - row_h * 0.75, cap, fontsize=8.6, color=MUTED,
                     family=SANS, style="italic", ha="left", va="center")
        # mini spark or bar strip pinned to the bottom of the cell
        spark = st.get("spark") or []
        bars = st.get("bars") or []
        sx = tx
        sw = cw - pad - 0.02
        sy = cyb + row_h * 0.10
        sh = row_h * 0.20
        if spark:
            sax = fig.add_axes([sx, sy, sw, sh])
            _spark(sax, spark, accent, fill=True, dot=True, lw=1.8,
                   dotcolor=tone_color(st.get("tone", "flat"), accent))
        elif bars:
            sax = fig.add_axes([sx, sy, sw, sh]); sax.axis("off")
            bv = np.asarray(bars, float)
            bx = np.arange(len(bv))
            col = tone_color(st.get("tone", "flat"), accent)
            sax.bar(bx, bv, width=0.72, color=col, zorder=3)
            sax.set_xlim(-0.6, len(bv) - 0.4)
            sax.set_ylim(0, bv.max() * 1.18 if bv.max() else 1)
    return fig


# --------------------------------------------------------------------- registry
COMPONENTS = {
    "kpi_card_with_sparkline": c_kpi_card_with_sparkline,
    "sparkline_row": c_sparkline_row,
    "annotated_narrative": c_annotated_narrative,
    "anomaly_callout": c_anomaly_callout,
    "stat_dashboard": c_stat_dashboard,
}


# --------------------------------------------------------------------- showcase
_SHOWCASE = {
    "module": "SUPER-KPI",
    "theme": {"accent": TEAL},
    "figures": [
        {"id": "kpi_card_with_sparkline", "component": "kpi_card_with_sparkline", "params": {
            "kicker": "Portfolio Management · Module 6 · Bảng điều khiển quỹ",
            "title": "Bốn chỉ số hiệu quả then chốt của quỹ đầu tư",
            "subtitle": "Mỗi ô gộp một con số lớn, sparkline tám kỳ và mũi tên thay đổi",
            "firm": "CFA Study Note", "source": "minh họa của tác giả", "asof": "Q3/2026",
            "ncols": 2,
            "cards": [
                {"label": "Giá trị tài sản ròng (NAV)", "value": "1.284,6", "delta": "+3,6%",
                 "tone": "up", "caption": "triệu USD, so với kỳ trước",
                 "spark": [1150, 1162, 1158, 1171, 1180, 1205, 1240, 1284.6]},
                {"label": "Lợi nhuận lũy kế từ đầu năm", "value": "12,4%", "delta": "+1,9đpt",
                 "tone": "up", "caption": "vượt chỉ số tham chiếu 2,1 đpt",
                 "spark": [7.1, 8.0, 8.4, 9.1, 9.9, 10.5, 11.6, 12.4]},
                {"label": "Hệ số Sharpe (12 tháng trượt)", "value": "1,42", "delta": "+0,04",
                 "tone": "up", "caption": "lợi nhuận điều chỉnh rủi ro cải thiện",
                 "spark": [1.30, 1.31, 1.33, 1.34, 1.36, 1.39, 1.41, 1.42]},
                {"label": "Sụt giảm tối đa (Max Drawdown)", "value": "-8,3%", "delta": "+0,60đpt",
                 "tone": "up", "caption": "thu hẹp so với đáy trước",
                 "spark": [-11.2, -10.8, -10.5, -10.9, -9.7, -9.1, -8.6, -8.3]},
            ],
        }},
        {"id": "sparkline_row", "component": "sparkline_row", "params": {
            "kicker": "Economics · Module 2 · Chỉ số vĩ mô",
            "title": "Bảng theo dõi xu hướng bốn chỉ số kinh tế vĩ mô then chốt",
            "subtitle": "Mỗi dòng nén tám quý dữ liệu thành một sparkline",
            "firm": "CFA Study Note", "source": "minh họa của tác giả", "asof": "Q2/2026",
            "rows": [
                {"label": "Tăng trưởng GDP thực (yoy)", "value": "3,2%", "tone": "up",
                 "status": "+1,1%", "spark": [2.1, 2.3, 2.6, 3.0, 3.4, 3.2, 3.0, 3.2]},
                {"label": "Lạm phát CPI (yoy)", "value": "4,7%", "tone": "down",
                 "status": "-1,7%", "spark": [6.4, 6.1, 5.8, 5.5, 5.2, 5.0, 4.8, 4.7]},
                {"label": "Lãi suất chính sách", "value": "5,25%", "tone": "up",
                 "status": "+1,75%", "spark": [3.5, 3.75, 4.25, 4.75, 5.0, 5.25, 5.25, 5.25]},
                {"label": "Tỷ lệ thất nghiệp", "value": "4,1%", "tone": "flat",
                 "status": "đi ngang", "spark": [3.9, 3.8, 3.9, 4.0, 4.0, 4.1, 4.0, 4.1]},
            ],
        }},
        {"id": "annotated_narrative", "component": "annotated_narrative", "params": {
            "kicker": "Phân tích báo cáo tài chính",
            "title": "Bình luận kết quả kinh doanh quý",
            "subtitle": "Các con số then chốt được tô màu theo cực tính",
            "firm": "CFA Study Note", "source": "minh họa của tác giả", "asof": "Q3/2026",
            "runs": [
                ["Doanh thu hợp nhất quý 3 đạt", None, False],
                ["2.480 tỷ đồng", "up", True], [", tăng", None, False],
                ["12,6%", "up", True], ["so với cùng kỳ và", None, False],
                ["vượt 3,2%", "up", True], ["so với dự báo của giới phân tích, nhờ biên lợi nhuận gộp mở rộng lên", None, False],
                ["34,8%.", "up", True], ["Tuy nhiên, chi phí tài chính tăng vọt khiến lợi nhuận ròng chỉ đạt", None, False],
                ["318 tỷ đồng", "down", True], [", giảm", None, False],
                ["7,4%", "down", True], ["so với cùng kỳ và", None, False],
                ["hụt 5,1%", "down", True], ["so với kỳ vọng đồng thuận. Ban điều hành duy trì hướng dẫn cả năm với tăng trưởng doanh thu", None, False],
                ["10% đến 12%", "emph", True], [", song hạ dự phóng biên lợi nhuận ròng về vùng", None, False],
                ["12,5%", "emph", True], ["do áp lực lãi vay còn kéo dài.", None, False],
            ],
        }},
        {"id": "anomaly_callout", "component": "anomaly_callout", "params": {
            "kicker": "Thu nhập cố định",
            "title": "Đột biến chênh lệch tín dụng hạng đầu tư",
            "subtitle": "Chênh lệch lợi suất trái phiếu doanh nghiệp hạng đầu tư, bps",
            "firm": "CFA Study Note", "source": "minh họa của tác giả", "asof": "2026",
            "y_format": "bps", "xlabel": "Tháng", "series_name": "Chênh lệch hạng đầu tư (IG)",
            "x": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"],
            "values": [118, 122, 125, 121, 128, 245, 235, 180, 158, 146, 138, 132],
            "anomaly_index": 5,
            "note": {"kicker": "Đột biến", "headline": "T6:  245bps", "negative": True,
                     "dx": -3.4, "dy": -0.30,
                     "body": "Cú sốc thanh khoản khiến nhà đầu tư bán tháo, chênh lệch nới rộng gần gấp đôi chỉ trong một kỳ rồi nhanh chóng thu hẹp."},
        }},
        {"id": "stat_dashboard", "component": "stat_dashboard", "params": {
            "kicker": "Economics · Module 2 · §3.1",
            "title": "Bảng chỉ số vĩ mô: bốn trụ cột chính sách",
            "subtitle": "Ảnh chụp nhanh các chỉ số kinh tế then chốt, kèm sparkline xu hướng",
            "firm": "CFA Study Note", "source": "minh họa của tác giả", "asof": "Q2/2026",
            "per_row": 4,
            "stats": [
                {"label": "Tăng trưởng GDP thực", "value": "3,2%", "delta": "0,40đpt",
                 "tone": "up", "caption": "so với quý trước",
                 "spark": [2.4, 2.6, 2.9, 3.0, 3.1, 3.2]},
                {"label": "Lạm phát CPI (yoy)", "value": "4,7%", "delta": "0,30đpt",
                 "tone": "down", "caption": "đang hạ nhiệt",
                 "spark": [5.6, 5.4, 5.2, 5.0, 4.8, 4.7]},
                {"label": "Lãi suất chính sách", "value": "5,25%", "delta": "0,25đpt",
                 "tone": "up", "caption": "thắt chặt",
                 "bars": [4.0, 4.25, 4.75, 5.0, 5.25]},
                {"label": "Tỷ giá USD/VND", "value": "24.850", "delta": "1,8%",
                 "tone": "up", "caption": "VND mất giá",
                 "spark": [24200, 24350, 24450, 24600, 24750, 24850]},
            ],
        }},
    ],
}


def _render_spec(spec, out_dir, only=None, dpi=200):
    module = spec.get("module", "MOD")
    accent = (spec.get("theme") or {}).get("accent", TEAL)
    os.makedirs(out_dir, exist_ok=True)
    ok = fail = 0
    for fs in spec.get("figures", []):
        fid = fs.get("id"); comp = fs.get("component")
        if only and fid != only:
            continue
        fn = COMPONENTS.get(comp)
        if fn is None:
            sys.stderr.write(f"WARN unknown component '{comp}' (id={fid})\n"); fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir_kpi: {ok} rendered, {fail} failed")
    return fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=None)
    ap.add_argument("--out-dir",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "gallery", "super", "kpi"))
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=170)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR-KPI components:", ", ".join(sorted(COMPONENTS))); return 0
    if args.spec:
        with open(args.spec, encoding="utf-8") as f:
            spec = json.load(f)
    else:
        spec = _SHOWCASE
    return _render_spec(spec, args.out_dir, only=args.only, dpi=args.dpi)


if __name__ == "__main__":
    sys.exit(main())
