#!/usr/bin/env python3
"""viz_eir_panels.py, Editorial/Text-panel group for the EIR viz library.

Typography-first structured-text layouts drawn as static matplotlib PNGs (Agg) that
embed into CFA study-note .docx files. Design language: Editorial Institutional Research
(FT / Bloomberg / Goldman / Morningstar / The Economist) on the warm CFA palette.

These are TEXT panels, 2x2 quadrant briefs, scenario columns, SWOT, structured
comparisons, DuPont equation-of-cards, before/after hero transitions, covenant status
tables. The discipline is HAIRLINE rules + restrained colour + flat grounds with hairline
borders, NOT decorative floating cards or drop shadows.

Shares the editorial chrome (`draw_masthead` / `draw_source`) and the spec.json contract
of viz_eir.py, so a note may mix core + EIR + panels. Editorial meta keys live inside
params: title, kicker, subtitle, source, asof, rating, firm.

Usage:
  python3 viz_eir_panels.py --spec spec.json --out-dir OUT [--only ID] [--dpi 170]
  python3 viz_eir_panels.py --out-dir OUT            # render built-in _SHOWCASE
  python3 viz_eir_panels.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, json, os, sys, textwrap
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
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved

# tint grounds (flat, pale) used as quadrant/card backgrounds. Day chinh la cho
# gay ra nen KEM AM cua executive_summary/dupont (F6): 4 hang nay tung tu khai
# mot bang mau rieng ngoai tam voi cua _eir_style.py, khong nap tu
# design-system/tokens.py. Gio dan xuat tu token that: TINT/TINT2 la nen "the"
# ben ngoai (giong PAPER_HI, nen phu, hoi tach khoi trang chinh), CARD_BG la
# than the/card lop trong (giong PAPER, trang thuan de noi bat hon TINT bao
# quanh), CARD_EDGE la vien hairline (giong GRID).
TINT = PAPER_HI
TINT2 = PAPER_HI
CARD_BG = PAPER
CARD_EDGE = GRID


# --------------------------------------------------------------------- meta
def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


def _tone(t, accent=None):
    """Resolve a semantic tone name to a colour. Accepts explicit tone tokens plus a few
    editorial aliases used in text panels."""
    if t is None:
        return accent or TEAL
    key = str(t).lower()
    alias = {
        "strength": TEAL, "positive": TEAL, "good": TEAL, "pass": TEAL, "bull": TEAL,
        "weakness": BRICK, "negative": BRICK, "bad": BRICK, "fail": BRICK, "bear": BRICK,
        "opportunity": GOLD, "opp": GOLD, "highlight": GOLD, "warn": GOLD, "warning": GOLD,
        "threat": NAVY, "challenge": NAVY, "base": INDIGO, "info": INDIGO, "neutral": NAVY,
    }
    if key in alias:
        return alias[key]
    return tone_color(t, accent)


def _wrap(txt, width):
    """Wrap a Vietnamese string to `width` chars/line, honouring explicit newlines."""
    out = []
    for para in str(txt).split("\n"):
        if para == "":
            out.append("")
            continue
        out.extend(textwrap.wrap(para, width=width, break_long_words=False,
                                 break_on_hyphens=False) or [""])
    return out


def _vn(txt, vn=True):
    """Swap the decimal point to a comma for Vietnamese display (1,234.5 -> 1.234,5).
    Applied only to already-formatted numeric strings, and only when vn=True."""
    if not vn or txt is None:
        return txt
    s = str(txt)
    if "." in s and "," in s:          # US grouped: 1,234.56
        s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    elif "." in s:                     # plain decimal: 3.40
        s = s.replace(".", ",")
    return s


def _fv(v, kind="num", currency="$", dp=None, vn=True):
    """fmt_value + Vietnamese-decimal display. Keeps unit suffixes (x, %, bps) intact."""
    return _vn(fmt_value(v, kind, currency, dp), vn)


def _ground(ax, x, y, w, h, fc=TINT, ec=CARD_EDGE, lw=1.1, rounding=0.014, z=1):
    """Flat pale ground with a hairline border (NO shadow)."""
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z, mutation_aspect=1.0,
    )
    ax.add_patch(patch)
    return patch


def _header_bar(ax, x, yb_top, w, hb, col, rounding=0.012):
    """A filled colour header bar with a squared bottom so it sits flat on the card body."""
    ax.add_patch(FancyBboxPatch((x, yb_top - hb), w, hb,
                 boxstyle=f"round,pad=0,rounding_size={rounding}",
                 linewidth=0, facecolor=col, zorder=3))
    ax.add_patch(Rectangle((x, yb_top - hb), w, hb * 0.5, facecolor=col, ec="none", zorder=3))


def _overlay(fig, rect=(0.0, 0.0, 1.0, 1.0)):
    """A transparent axis spanning the whole figure so we can place cards/text in
    figure-fraction coords with clipping off."""
    ax = fig.add_axes(rect); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off"); ax.set_facecolor("none")
    return ax


def _content_top(fig, meta):
    """Where content starts: just below the masthead rule."""
    return draw_masthead(fig, meta, top=0.965)


# ------------------------------------------------------------- shared UI helpers
def _status_badge(ax, x, y, text, col):
    """Filled rounded pill with a leading dot, left-anchored at x (fig-fraction)."""
    w = 0.052 + 0.0135 * len(text)
    ax.add_patch(FancyBboxPatch((x, y - 0.026), w, 0.052,
                 boxstyle="round,pad=0,rounding_size=0.026",
                 linewidth=0, facecolor=col, zorder=5))
    ax.add_patch(Circle((x + 0.024, y), 0.007, facecolor=PAPER, ec="none", zorder=6))
    ax.text(x + 0.044, y, text, color=PAPER, family=SANS, fontsize=10.5, fontweight="bold",
            va="center", ha="left", zorder=6)


def _legend(ax, entries, y, x0=0.035, swatch=0.014, gap_after_text=0.028):
    """Editorial swatch legend along the bottom. entries=[(label, color)]."""
    x = x0
    for label, col in entries:
        if not label:
            continue
        ax.add_patch(Rectangle((x, y - swatch / 2), swatch, swatch, facecolor=col,
                               ec="none", zorder=5))
        ax.text(x + swatch + 0.008, y, label, color=INK, family=SANS, fontsize=10,
                va="center", ha="left", zorder=5)
        x += swatch + 0.008 + 0.0092 * len(label) + gap_after_text


# ========================================================= 1. executive_summary
def c_executive_summary(p, accent):
    """2x2 text-quadrant brief. Each quadrant = small colored heading + short serif
    sub-headline + 2-3 body lines; hairline cross-dividers inside one pale ground.
    params: quadrants=[{title, tone, body, headline?}] (len 4); emphasize? (0-3)."""
    quads = p["quadrants"][:4]
    while len(quads) < 4:
        quads.append({"title": "", "body": ""})
    fig = plt.figure(figsize=(9.8, 6.6), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.035, 0.965
    gy1 = rule_y - 0.035
    gy0 = 0.085
    _ground(ax, gx0, gy0, gx1 - gx0, gy1 - gy0, fc=TINT, ec=CARD_EDGE, lw=1.2)

    mx = (gx0 + gx1) / 2.0
    my = (gy0 + gy1) / 2.0
    pad = 0.028
    ax.add_line(mlines.Line2D([mx, mx], [gy0 + pad, gy1 - pad], color=CARD_EDGE, lw=1.0,
                              zorder=3))
    ax.add_line(mlines.Line2D([gx0 + pad, gx1 - pad], [my, my], color=CARD_EDGE, lw=1.0,
                              zorder=3))

    inpad = 0.030
    cells = [
        (gx0 + inpad, gy1 - inpad),   # top-left
        (mx + inpad,  gy1 - inpad),   # top-right
        (gx0 + inpad, my - inpad),    # bottom-left
        (mx + inpad,  my - inpad),    # bottom-right
    ]
    cell_w = (mx - gx0) - 2 * inpad
    body_chars = max(24, int(cell_w * 118))

    for (cx, cy), q in zip(cells, quads):
        col = _tone(q.get("tone"), accent)
        y = cy
        ax.add_line(mlines.Line2D([cx, cx + 0.028], [y + 0.006, y + 0.006], color=col,
                                  lw=3.4, zorder=4, solid_capstyle="butt"))
        y -= 0.020
        ax.text(cx, y, q.get("title", "").upper(), color=col, family=SANS, fontsize=10,
                fontweight="bold", va="top", ha="left", zorder=4)
        y -= 0.040
        hl = q.get("headline")
        if hl:
            for line in _wrap(hl, max(18, int(cell_w * 44))):
                ax.text(cx, y, line, color=NAVY, family=SERIF, fontsize=15, fontweight="bold",
                        va="top", ha="left", zorder=4)
                y -= 0.041
            y -= 0.006
        for line in _wrap(q.get("body", ""), body_chars):
            ax.text(cx, y, line, color=INK, family=SANS, fontsize=10.6, va="top", ha="left",
                    zorder=4)
            y -= 0.036

    emp = p.get("emphasize")
    if emp is not None and 0 <= emp < 4:
        ex = gx0 if emp in (0, 2) else mx
        eyt = gy1 if emp in (0, 1) else my
        eyb = my if emp in (0, 1) else gy0
        ecol = _tone(quads[emp].get("tone"), accent)
        ax.add_patch(FancyBboxPatch((ex + 0.012, eyb + 0.012),
                     (mx - gx0) - 0.024, (eyt - eyb) - 0.024,
                     boxstyle="round,pad=0,rounding_size=0.012",
                     linewidth=1.8, edgecolor=ecol, facecolor="none", zorder=5))
    return fig


# ============================================================= 2. scenario_cards
def c_scenario_cards(p, accent):
    """3 side-by-side scenario columns (bear / base / bull). Each: colored header bar,
    probability % (top), large outcome value, 2-4 bullets. Base column emphasized.
    params: cards=[{name, prob, value, tone, bullets[], emphasize?, badge?}]."""
    cards = p["cards"]
    n = len(cards)
    fig = plt.figure(figsize=(10.8, 6.8), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.035, 0.965
    top = rule_y - 0.030
    bot = 0.130
    gap = 0.022
    w = (gx1 - gx0 - (n - 1) * gap) / n
    hb = 0.056
    prob_fmt = p.get("prob_format", "pct")
    val_fmt = p.get("value_format", "cur")
    cur = p.get("currency", "$")
    vn = p.get("vn_decimal", True)
    body_chars = max(20, int(w * 108))

    for i, cd in enumerate(cards):
        x = gx0 + i * (w + gap)
        col = _tone(cd.get("tone"), accent)
        emph = cd.get("emphasize", False)
        _ground(ax, x, bot, w, top - bot, fc=CARD_BG, ec=CARD_EDGE,
                lw=1.6 if emph else 1.1, z=2)
        if emph:
            ax.add_patch(FancyBboxPatch((x, bot), w, top - bot,
                         boxstyle="round,pad=0,rounding_size=0.014",
                         linewidth=1.9, edgecolor=GOLD, facecolor="none", zorder=6))
        _header_bar(ax, x, top, w, hb, col)
        ax.text(x + w / 2, top - hb / 2, cd.get("name", ""), color=PAPER, family=SERIF,
                fontsize=15, fontweight="bold", ha="center", va="center", zorder=5)
        if emph and cd.get("badge"):
            _badge(fig, x + w - 0.010, top - hb / 2, cd["badge"], ha="right", bg=GOLD,
                   fg=PAPER, ax=ax)

        ix = x + 0.020
        y = top - hb - 0.052
        pv = _fv(cd.get("prob"), prob_fmt, vn=vn)
        ax.text(ix, y, pv, color=col, family=MONO, fontsize=27, fontweight="bold",
                va="center", ha="left", zorder=5)
        ax.text(x + w - 0.018, y, "xác suất", color=MUTED, family=MONO, fontsize=10,
                va="center", ha="right", zorder=5)
        y -= 0.058
        ax.add_line(mlines.Line2D([ix, x + w - 0.018], [y + 0.012, y + 0.012],
                    color=GRID, lw=0.9, zorder=4))
        ax.text(ix, y - 0.006, p.get("value_label", "Giá mục tiêu"), color=MUTED,
                family=MONO, fontsize=10.5, va="top", ha="left", zorder=5)
        y -= 0.040
        ax.text(ix, y, _fv(cd.get("value"), val_fmt, cur, vn=vn), color=NAVY, family=SERIF,
                fontsize=25, fontweight="bold", va="top", ha="left", zorder=5)
        y -= 0.070
        ax.add_line(mlines.Line2D([ix, x + w - 0.018], [y + 0.020, y + 0.020],
                    color=GRID, lw=0.9, zorder=4))
        for b in cd.get("bullets", [])[:4]:
            ax.add_patch(Rectangle((ix, y - 0.004), 0.009, 0.014, facecolor=col,
                                   ec="none", zorder=5))
            for line in _wrap(b, body_chars):
                ax.text(ix + 0.020, y, line, color=INK, family=SANS, fontsize=10.2,
                        va="top", ha="left", zorder=5)
                y -= 0.033
            y -= 0.012

    _legend(ax, [(cd.get("name", ""), _tone(cd.get("tone"), accent)) for cd in cards],
            y=0.075, x0=gx0)
    return fig


# ========================================================================= 3. swot
def c_swot(p, accent):
    """2x2 SWOT. Điểm mạnh (TEAL) / Điểm yếu (BRICK) / Cơ hội (GOLD) / Thách thức (NAVY).
    Each quadrant: filled colored header + bullet list; flat card grounds + hairline borders.
    params: strengths[], weaknesses[], opportunities[], threats[] (each 3-4 items)."""
    S_ = p.get("strengths", []); W = p.get("weaknesses", [])
    O = p.get("opportunities", []); T = p.get("threats", [])
    lbl = p.get("labels", {})
    quads = [
        (lbl.get("s", "Điểm mạnh"), TEAL, S_, "NỘI BỘ"),
        (lbl.get("w", "Điểm yếu"), BRICK, W, "NỘI BỘ"),
        (lbl.get("o", "Cơ hội"), GOLD, O, "BÊN NGOÀI"),
        (lbl.get("t", "Thách thức"), NAVY, T, "BÊN NGOÀI"),
    ]
    fig = plt.figure(figsize=(10.6, 9.2), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.060, 0.965
    top = rule_y - 0.028
    bot = 0.110
    gapx, gapy = 0.026, 0.034
    w = (gx1 - gx0 - gapx) / 2.0
    mid_y = (top + bot) / 2.0
    h = (top - bot - gapy) / 2.0
    hb = 0.046
    positions = [
        (gx0, mid_y + gapy / 2.0),                 # S top-left
        (gx0 + w + gapx, mid_y + gapy / 2.0),      # W top-right
        (gx0, bot),                                # O bottom-left
        (gx0 + w + gapx, bot),                     # T bottom-right
    ]
    body_chars = max(30, int(w * 100))

    # fit line-step so the busiest quadrant's bullets stay inside its ground
    top_head = 0.036      # gap header -> first bullet
    bul_gap = 0.009       # gap between bullets
    def _nlines(items):
        return sum(max(1, len(_wrap(it, body_chars))) for it in items[:4])
    max_bul = max(1, max(len(q[2][:4]) for q in quads))
    max_ln = max(1, max(_nlines(q[2]) for q in quads))
    avail_body = h - hb - top_head - 0.016
    step = (avail_body - bul_gap * (max_bul - 1)) / max_ln
    step = min(0.030, max(step, 0.022))

    for (x, yb), (title, col, items, side) in zip(positions, quads):
        _ground(ax, x, yb, w, h, fc=CARD_BG, ec=CARD_EDGE, lw=1.1, z=2)
        _header_bar(ax, x, yb + h, w, hb, col)
        ax.text(x + 0.020, yb + h - hb / 2, title, color=PAPER, family=SERIF, fontsize=15,
                fontweight="bold", ha="left", va="center", zorder=5)
        ax.text(x + w - 0.018, yb + h - hb / 2, side, color=PAPER, family=SANS, fontsize=8.5,
                fontweight="bold", ha="right", va="center", zorder=5, alpha=0.92)
        ix = x + 0.022
        y = yb + h - hb - top_head
        for it in items[:4]:
            ax.add_patch(Rectangle((ix, y - 0.004), 0.009, 0.013, facecolor=col, ec="none",
                                   zorder=5))
            for line in _wrap(it, body_chars):
                ax.text(ix + 0.020, y, line, color=INK, family=SANS, fontsize=10.2,
                        va="top", ha="left", zorder=5)
                y -= step
            y -= bul_gap

    # axis labels: internal/external (left), positive/negative (bottom)
    ax.text(gx0 - 0.032, mid_y + gapy / 2 + h / 2, "NỘI BỘ", color=MUTED, family=SANS,
            fontsize=8.5, fontweight="bold", rotation=90, ha="center", va="center")
    ax.text(gx0 - 0.032, bot + h / 2, "BÊN NGOÀI", color=MUTED, family=SANS, fontsize=8.5,
            fontweight="bold", rotation=90, ha="center", va="center")
    ax.text(gx0 + w / 2, bot - 0.010, "TÍCH CỰC", color=MUTED, family=SANS, fontsize=8.5,
            fontweight="bold", ha="center", va="top")
    ax.text(gx0 + w + gapx + w / 2, bot - 0.010, "TIÊU CỰC", color=MUTED, family=SANS,
            fontsize=8.5, fontweight="bold", ha="center", va="top")

    _legend(ax, [(q[0], q[1]) for q in quads], y=0.058, x0=gx0)
    return fig


# =================================================================== 4. comparison
def c_comparison(p, accent):
    """2-column structured comparison (A vs B). A header bar per column, aligned rows of
    attribute text (main line + optional italic sub), a center hairline + 'vs' badge.
    params: left={title, items[{text, sub?}]}, right={title, items[...]}."""
    L = p["left"]; R = p["right"]
    lcol = _tone(p.get("left_tone"), accent) if p.get("left_tone") else INDIGO
    rcol = _tone(p.get("right_tone"), accent) if p.get("right_tone") else BRICK
    fig = plt.figure(figsize=(10.8, 7.2), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.035, 0.965
    top = rule_y - 0.030
    bot = 0.120
    mx = (gx0 + gx1) / 2.0
    gutter = 0.055
    w = (mx - gx0) - gutter / 2.0
    hb = 0.058
    body_chars = max(24, int(w * 96))

    def _norm_items(items):
        out = []
        for it in items:
            if isinstance(it, dict):
                out.append((it.get("text", ""), it.get("sub")))
            else:
                out.append((str(it), None))
        return out

    for x, side, col in [(gx0, L, lcol), (mx + gutter / 2.0, R, rcol)]:
        _ground(ax, x, bot, w, top - bot, fc=CARD_BG, ec=CARD_EDGE, lw=1.1, z=2)
        _header_bar(ax, x, top, w, hb, col)
        ax.text(x + w / 2, top - hb / 2, side.get("title", ""), color=PAPER, family=SERIF,
                fontsize=15, fontweight="bold", ha="center", va="center", zorder=5)
        ix = x + 0.024
        y = top - hb - 0.050
        for txt, sub in _norm_items(side.get("items", [])):
            ax.text(ix, y, "›", color=col, family=SANS, fontsize=14, fontweight="bold",
                    va="top", ha="left", zorder=5)
            for line in _wrap(txt, body_chars):
                ax.text(ix + 0.022, y, line, color=INK, family=SANS, fontsize=10.8,
                        va="top", ha="left", zorder=5)
                y -= 0.034
            if sub:
                for line in _wrap(sub, body_chars):
                    ax.text(ix + 0.022, y, line, color=col, family=SANS, fontsize=9.6,
                            style="italic", va="top", ha="left", zorder=5)
                    y -= 0.030
            y -= 0.020

    ax.add_line(mlines.Line2D([mx, mx], [bot + 0.02, top - hb - 0.02], color=CARD_EDGE,
                lw=1.0, ls=(0, (3, 3)), zorder=2))
    ax.add_patch(Circle((mx, top - hb / 2), 0.028, facecolor=PAPER, edgecolor=GOLD,
                        linewidth=2.0, zorder=7))
    ax.text(mx, top - hb / 2, "vs", color=GOLD, family=SERIF, fontsize=13,
            fontstyle="italic", fontweight="bold", ha="center", va="center", zorder=8)

    _legend(ax, [(L.get("title", ""), lcol), (R.get("title", ""), rcol)], y=0.068, x0=gx0)
    return fig


# ======================================================================= 5. dupont
def c_dupont(p, accent):
    """Equation-of-cards decomposition: Result = A x B x C. Navy result card, flat pale
    factor cards each with a colored top rule; joined by = and x operators.
    params: result={label, value}, factors=[{label, value, sub, fmt?, dp?}]."""
    res = p["result"]; facs = p["factors"]
    fig = plt.figure(figsize=(11.2, 5.6), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.035, 0.965
    top = rule_y - 0.070
    bot = 0.155
    ch = top - bot
    cy = bot
    n = len(facs)
    op_w = 0.050
    total_ops = op_w * n
    avail = (gx1 - gx0) - total_ops
    res_w = avail * 0.24
    fac_w = (avail - res_w) / n
    fac_cols = ([_tone(c, accent) for c in p["factor_colors"]]
                if p.get("factor_colors") else palette(accent))

    x = gx0
    _ground(ax, x, cy, res_w, ch, fc=NAVY, ec=NAVY, lw=1.0, z=2)
    ax.add_line(mlines.Line2D([x + 0.012, x + res_w - 0.012], [cy + ch - 0.010,
                cy + ch - 0.010], color=GOLD, lw=3.2, zorder=4, solid_capstyle="butt"))
    ax.text(x + res_w / 2, cy + ch - 0.052, res.get("label", "").upper(), color=PAPER,
            family=SANS, fontsize=10.5, fontweight="bold", ha="center", va="top", zorder=5)
    vn = p.get("vn_decimal", True)
    ax.text(x + res_w / 2, cy + ch / 2 - 0.020, _fv(res.get("value"),
            p.get("result_format", "pct"), vn=vn), color=PAPER, family=SERIF, fontsize=30,
            fontweight="bold", ha="center", va="center", zorder=5)
    x += res_w

    ax.text(x + op_w / 2, cy + ch / 2, "=", color=MUTED, family=SERIF, fontsize=26,
            ha="center", va="center", zorder=5)
    x += op_w

    for i, fc in enumerate(facs):
        col = fac_cols[i % len(fac_cols)]
        _ground(ax, x, cy, fac_w, ch, fc=TINT2, ec=CARD_EDGE, lw=1.1, z=2)
        ax.add_line(mlines.Line2D([x + 0.012, x + fac_w - 0.012], [cy + ch - 0.010,
                    cy + ch - 0.010], color=col, lw=3.2, zorder=4, solid_capstyle="butt"))
        ax.text(x + fac_w / 2, cy + ch - 0.050, fc.get("label", ""), color=INK,
                family=SANS, fontsize=11, fontweight="bold", ha="center", va="top", zorder=5)
        ax.text(x + fac_w / 2, cy + ch / 2 + 0.010, _fv(fc.get("value"),
                fc.get("fmt", "num"), p.get("currency", "$"), fc.get("dp"), vn=vn), color=col,
                family=SERIF, fontsize=27, fontweight="bold", ha="center", va="center",
                zorder=5)
        sub = fc.get("sub")
        if sub:
            yy = cy + ch / 2 - 0.070
            for line in _wrap(sub, max(14, int(fac_w * 70))):
                ax.text(x + fac_w / 2, yy, line, color=MUTED, family=SANS, fontsize=9.5,
                        style="italic", ha="center", va="top", zorder=5)
                yy -= 0.036
        x += fac_w
        if i < n - 1:
            ax.text(x + op_w / 2, cy + ch / 2, "×", color=MUTED, family=SERIF, fontsize=22,
                    ha="center", va="center", zorder=5)
            x += op_w

    _legend(ax, [(res.get("label", ""), NAVY)] +
            [(fc.get("label", ""), fac_cols[i % len(fac_cols)])
             for i, fc in enumerate(facs)], y=0.085, x0=gx0)
    return fig


# ================================================================== 6. before_after
def c_before_after(p, accent):
    """2-state hero transition: big number (left) -> arrow with delta -> big number (right),
    centered metric title, caption line. params: left={value,label}, right={value,label},
    delta, tone, caption, metric?, pct_change?, unit?."""
    L = p["left"]; R = p["right"]
    tone = _tone(p.get("tone", "good"), accent)
    lcol = _tone(p.get("left_tone"), accent) if p.get("left_tone") else INDIGO
    fig = plt.figure(figsize=(10.8, 6.6), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.055, 0.945
    if p.get("metric"):
        mty = rule_y - 0.055
        ax.text(0.5, mty, p["metric"].upper(), color=NAVY, family=SANS, fontsize=12,
                fontweight="bold", ha="center", va="center", zorder=5)
        ax.add_line(mlines.Line2D([0.5 - 0.085, 0.5 + 0.085], [mty - 0.028, mty - 0.028],
                    color=GOLD, lw=2.4, zorder=5))

    cy_top = rule_y - 0.140
    cy_bot = 0.240
    cw = 0.300
    ch = cy_top - cy_bot
    lx = gx0
    rx = gx1 - cw
    vfmt = p.get("value_format", "num")
    cur = p.get("currency", "$")
    vn = p.get("vn_decimal", True)
    dp = p.get("dp")
    unit = (" " + p["unit"]) if p.get("unit") else ""

    def _hero_card(x, side, col):
        _ground(ax, x, cy_bot, cw, ch, fc=CARD_BG, ec=CARD_EDGE, lw=1.1, z=2)
        ax.add_line(mlines.Line2D([x + 0.010, x + cw - 0.010], [cy_bot + ch - 0.008,
                    cy_bot + ch - 0.008], color=col, lw=3.4, zorder=4, solid_capstyle="butt"))
        ax.text(x + cw / 2, cy_bot + ch - 0.048, side.get("label", "").upper(), color=MUTED,
                family=SANS, fontsize=10.5, fontweight="bold", ha="center", va="top", zorder=5)
        ax.text(x + cw / 2, cy_bot + ch / 2 - 0.030,
                _fv(side.get("value"), vfmt, cur, dp, vn=vn) + unit, color=col, family=SERIF,
                fontsize=34, fontweight="bold", ha="center", va="center", zorder=5)

    _hero_card(lx, L, lcol)
    _hero_card(rx, R, tone)

    midx = (lx + cw + rx) / 2.0
    arrow_y = cy_bot + ch / 2 - 0.02
    ax.annotate("", xy=(rx - 0.012, arrow_y), xytext=(lx + cw + 0.012, arrow_y),
                arrowprops=dict(arrowstyle="-|>", color=tone, lw=2.6, mutation_scale=22),
                zorder=4)
    _badge(fig, midx, arrow_y + 0.075, str(p.get("delta", "")), ha="center", bg=tone,
           fg=PAPER, ax=ax)
    if p.get("pct_change"):
        ax.text(midx, arrow_y - 0.050, p["pct_change"], color=tone, family=MONO,
                fontsize=12, fontweight="bold", ha="center", va="center", zorder=5)
        ax.text(midx, arrow_y - 0.085, p.get("pct_label", "thay đổi"), color=MUTED,
                family=MONO, fontsize=9.5, ha="center", va="center", zorder=5)

    if p.get("caption"):
        yy = cy_bot - 0.040
        for line in _wrap(p["caption"], 96):
            ax.text(0.5, yy, line, color=INK, family=SANS, fontsize=10.4, ha="center",
                    va="top", zorder=5)
            yy -= 0.030

    _legend(ax, [(p.get("legend_label", "Cải thiện"), tone)], y=0.062, x0=gx0)
    return fig


# =================================================================== 7. status_strip
def c_status_strip(p, accent):
    """Compliance/covenant table: rows of {metric, value, threshold, status}. Status = a
    colored badge Đạt (TEAL) / Cảnh báo (GOLD) / Vi phạm (BRICK). Aligned columns,
    hairline row rules, colored left-edge tabs. params: rows=[{metric, value, threshold,
    status, value_fmt?}]."""
    rows = p["rows"]
    n = len(rows)
    status_map = p.get("status_colors", {
        "pass": TEAL, "đạt": TEAL, "dat": TEAL,
        "warn": GOLD, "cảnh báo": GOLD, "canh bao": GOLD, "warning": GOLD,
        "fail": BRICK, "vi phạm": BRICK, "vi pham": BRICK, "breach": BRICK,
    })
    status_label = p.get("status_labels", {
        "pass": "Đạt", "warn": "Cảnh báo", "fail": "Vi phạm",
    })

    def _scol(s):
        return status_map.get(str(s).lower(), MUTED)

    def _slabel(s):
        return status_label.get(str(s).lower(), str(s))

    fig = plt.figure(figsize=(10.4, max(5.4, 2.4 + 0.62 * n + 1.6)), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    rule_y = _content_top(fig, m); draw_source(fig, m)
    ax = _overlay(fig)

    gx0, gx1 = 0.045, 0.965
    top = rule_y - 0.045
    bot = 0.115
    col_val_x = 0.700
    col_stat_x = 0.815
    hy = top
    ax.text(gx0 + 0.020, hy, p.get("col_metric", "HẠN MỨC / ĐIỀU KIỆN").upper(),
            color=MUTED, family=SANS, fontsize=9.5, fontweight="bold", va="center",
            ha="left", zorder=5)
    ax.text(col_val_x, hy, p.get("col_value", "GIÁ TRỊ").upper(), color=MUTED, family=SANS,
            fontsize=9.5, fontweight="bold", va="center", ha="right", zorder=5)
    ax.text(col_stat_x, hy, p.get("col_status", "TRẠNG THÁI").upper(), color=MUTED,
            family=SANS, fontsize=9.5, fontweight="bold", va="center", ha="left", zorder=5)
    ax.add_line(mlines.Line2D([gx0, gx1], [hy - 0.028, hy - 0.028], color=GOLD, lw=2.0,
                zorder=4))

    area_top = hy - 0.028
    step = (area_top - bot) / n
    vfmt = p.get("value_format", "x")
    cur = p.get("currency", "$")
    vn = p.get("vn_decimal", True)

    for i, r in enumerate(rows):
        rc = area_top - i * step
        cyc = rc - step / 2.0
        col = _scol(r.get("status"))
        ax.add_line(mlines.Line2D([gx0 + 0.002, gx0 + 0.002], [rc - step + 0.016,
                    rc - 0.016], color=col, lw=4.2, zorder=5, solid_capstyle="butt"))
        ax.text(gx0 + 0.024, cyc + 0.018, r.get("metric", ""), color=NAVY, family=SANS,
                fontsize=11.5, fontweight="bold", va="center", ha="left", zorder=5)
        if r.get("threshold"):
            ax.text(gx0 + 0.024, cyc - 0.020, r["threshold"], color=MUTED, family=SANS,
                    fontsize=9.6, style="italic", va="center", ha="left", zorder=5)
        ax.text(col_val_x, cyc, _fv(r.get("value"), r.get("value_fmt", vfmt), cur,
                r.get("value_dp"), vn=vn), color=col, family=MONO, fontsize=13,
                fontweight="bold", va="center", ha="right", zorder=5)
        _status_badge(ax, col_stat_x, cyc, _slabel(r.get("status")), col)
        ax.add_line(mlines.Line2D([gx0 + 0.024, gx1], [rc - step, rc - step],
                    color=GRID, lw=0.9, zorder=3))

    _legend(ax, [(_slabel(k) + suff, v) for k, v, suff in [
        ("pass", TEAL, " (trong hạn mức)"), ("warn", GOLD, " (gần ngưỡng)"),
        ("fail", BRICK, " (vượt ngưỡng)")]], y=0.060, x0=gx0)
    return fig


COMPONENTS = {
    "executive_summary": c_executive_summary,
    "scenario_cards": c_scenario_cards,
    "swot": c_swot,
    "comparison": c_comparison,
    "dupont": c_dupont,
    "before_after": c_before_after,
    "status_strip": c_status_strip,
}


# =========================================================================== showcase
_SHOWCASE = {
    "executive_summary": {
        "kicker": "Equity · Module 4 · Tổng kết",
        "title": "Bốn điểm cốt lõi của Module 4",
        "subtitle": "Bốn trụ cột cần nhớ trước khi sang phần bài tập: nền tảng định giá, "
                    "nguồn rủi ro, hàm ý chiến lược và cạm bẫy thường gặp.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "emphasize": 3,
        "quadrants": [
            {"title": "Định giá", "tone": "base",
             "headline": "Dòng tiền chiết khấu là gốc",
             "body": "Giá trị nội tại bằng hiện giá dòng tiền tự do tương lai; chất lượng "
                     "đầu vào WACC và tăng trưởng dài hạn quyết định độ tin cậy hơn cả mô hình."},
            {"title": "Rủi ro", "tone": "weakness",
             "headline": "Beta và phần bù chi phối",
             "body": "Suất chiết khấu nhạy với hệ số beta và phần bù rủi ro vốn cổ phần; "
                     "một thay đổi nhỏ ở WACC tạo dao động lớn trong giá mục tiêu."},
            {"title": "Chiến lược", "tone": "strength",
             "headline": "Đối chiếu chéo nhiều phương pháp",
             "body": "Kết hợp định giá tuyệt đối (DCF) với định giá tương đối (bội số) để "
                     "khoanh vùng giá hợp lý và kiểm tra tính nhất quán của giả định."},
            {"title": "Cạm bẫy", "tone": "opportunity",
             "headline": "Lạm dụng giá trị cuối kỳ",
             "body": "Giá trị cuối kỳ thường chiếm phần lớn định giá; tăng trưởng vĩnh viễn "
                     "vượt tốc độ tăng GDP danh nghĩa là lỗi kinh điển cần tránh."},
        ],
    },
    "scenario_cards": {
        "kicker": "Equity · Module 5 · §3.1",
        "title": "Phân tích kịch bản: giá mục tiêu 12 tháng",
        "subtitle": "Khung định giá theo ba kịch bản với xác suất gán cho từng trạng thái. "
                    "Giá kỳ vọng = 25%·142 + 50%·168 + 25%·205, lệch về phía tăng.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "value_label": "Giá mục tiêu", "prob_format": "pct", "value_format": "cur",
        "cards": [
            {"name": "Bi quan", "tone": "bear", "prob": 25, "value": 142,
             "bullets": ["Tăng trưởng doanh thu chậm còn 3%, biên gộp thu hẹp 180bp",
                         "WACC tăng lên 10,5% do phần bù rủi ro cao hơn",
                         "Bội số P/E mục tiêu giảm xuống 14 lần"]},
            {"name": "Cơ sở", "tone": "base", "prob": 50, "value": 168, "emphasize": True,
             "badge": "trọng tâm",
             "bullets": ["Doanh thu tăng 8%, biên gộp duy trì quanh 42%",
                         "WACC giữ ở 9,0%, tăng trưởng dài hạn 3,5%",
                         "Bội số P/E mục tiêu 17 lần, phù hợp trung bình ngành"]},
            {"name": "Lạc quan", "tone": "bull", "prob": 25, "value": 205,
             "bullets": ["Doanh thu tăng tốc 13% nhờ giành thị phần",
                         "Đòn bẩy hoạt động đẩy biên EBIT lên 28%",
                         "Tái định giá lên 20 lần khi tăng trưởng được xác nhận"]},
        ],
    },
    "swot": {
        "kicker": "Equity · Module 5 · §2.3",
        "title": "Phân tích SWOT: luận điểm đầu tư cổ phiếu",
        "subtitle": "Khung SWOT cho luận điểm mua dài hạn một nhà sản xuất thiết bị công "
                    "nghiệp. Trục dọc tách yếu tố nội bộ khỏi bên ngoài; trục ngang tách "
                    "tích cực khỏi tiêu cực.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "strengths": [
            "Biên gộp 47% và ROIC 18%, vượt trung vị ngành 600bp",
            "Bảng cân đối ròng tiền mặt, nợ ròng trên EBITDA âm 0,4 lần",
            "Thị phần dẫn đầu 32% ở phân khúc lõi với chi phí chuyển đổi cao",
            "Dòng tiền tự do chuyển đổi trên 90% lợi nhuận ròng",
        ],
        "weaknesses": [
            "Doanh thu tập trung: ba khách hàng lớn nhất chiếm 41%",
            "Chi tiêu vốn theo chu kỳ, độ nhạy đòn bẩy hoạt động cao",
            "Hiện diện tại thị trường mới nổi còn dưới 12% doanh thu",
            "Định giá cao: P/E kỳ vọng 24 lần so với trung bình 5 năm là 19 lần",
        ],
        "opportunities": [
            "Chu kỳ tự động hóa nhà máy mở rộng thị trường tiềm năng 9%/năm",
            "Mảng dịch vụ và phần mềm biên cao nâng doanh thu định kỳ",
            "Thương vụ thâu tóm bổ trợ nhờ bảng cân đối còn dư địa",
            "Quy định khí thải mới thúc đẩy nhu cầu thay thế thiết bị",
        ],
        "threats": [
            "Đối thủ chi phí thấp châu Á gây áp lực giảm giá bán",
            "Suy giảm vĩ mô làm hoãn đầu tư vốn của khách hàng công nghiệp",
            "Biến động giá đầu vào thép và chất bán dẫn nén biên lợi nhuận",
            "Rủi ro tỷ giá khi 58% doanh thu phát sinh bằng ngoại tệ",
        ],
    },
    "comparison": {
        "kicker": "Fixed Income · Module 2 · §3.1",
        "title": "Trái phiếu lãi suất cố định so với thả nổi",
        "subtitle": "So sánh hai cấu trúc trả lãi cốt lõi của thị trường thu nhập cố định. "
                    "Lựa chọn phụ thuộc kỳ vọng lãi suất và khẩu vị rủi ro lãi suất.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "left": {"title": "Trái phiếu lãi suất cố định", "items": [
            {"text": "Lãi suất coupon được ấn định cố định trong suốt vòng đời trái phiếu",
             "sub": "Dòng tiền danh nghĩa biết trước hoàn toàn"},
            {"text": "Giá nhạy cảm mạnh với biến động lãi suất thị trường",
             "sub": "Duration hiệu dụng cao"},
            {"text": "Hưởng lợi khi lãi suất giảm; chịu thiệt khi lãi suất tăng"},
            {"text": "Phù hợp khi nhà đầu tư dự báo lãi suất đi xuống hoặc đi ngang"},
        ]},
        "right": {"title": "Trái phiếu lãi suất thả nổi", "items": [
            {"text": "Coupon đặt lại định kỳ theo lãi suất tham chiếu cộng biên độ",
             "sub": "Ví dụ: SOFR + 120 điểm cơ bản"},
            {"text": "Giá ít nhạy cảm với lãi suất nhờ duration ngắn",
             "sub": "Duration gần bằng kỳ đặt lại coupon"},
            {"text": "Hưởng lợi khi lãi suất tăng; thu nhập điều chỉnh theo thị trường"},
            {"text": "Phù hợp khi nhà đầu tư dự báo lãi suất đi lên hoặc bất định"},
        ]},
    },
    "dupont": {
        "kicker": "Equity · Phân tích DuPont",
        "title": "Phân rã ROE theo DuPont ba nhân tố",
        "subtitle": "Suất sinh lời trên vốn chủ sở hữu (ROE) được tách thành biên lợi nhuận "
                    "ròng, vòng quay tài sản và đòn bẩy tài chính.",
        "asof": "FY2025", "source": "minh họa của tác giả",
        "result": {"label": "ROE", "value": 18.5}, "result_format": "pct",
        "factor_colors": ["opportunity", "strength", "base"],
        "factors": [
            {"label": "Biên lợi nhuận ròng", "value": 22, "fmt": "pct",
             "sub": "Lợi nhuận ròng / Doanh thu"},
            {"label": "Vòng quay tài sản", "value": 0.9, "fmt": "num", "dp": 1,
             "sub": "Doanh thu / Tổng tài sản"},
            {"label": "Đòn bẩy tài chính", "value": 0.93, "fmt": "num", "dp": 2,
             "sub": "Tổng tài sản / Vốn chủ sở hữu"},
        ],
    },
    "before_after": {
        "kicker": "Quản lý rủi ro lãi suất · Phòng hộ kỳ hạn · §5.3",
        "title": "Hợp đồng tương lai trái phiếu kéo thời lượng danh mục về mục tiêu",
        "subtitle": "Vị thế bán hợp đồng tương lai trái phiếu kho bạc làm giảm thời lượng "
                    "hiệu dụng của danh mục, đưa độ nhạy lãi suất về sát mức chuẩn.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "metric": "Thời lượng hiệu dụng danh mục",
        "value_format": "num", "unit": "năm", "dp": 1,
        "left": {"value": 7.2, "label": "Trước phòng hộ"},
        "right": {"value": 4.5, "label": "Sau phòng hộ"},
        "delta": "−2,7 năm", "pct_change": "−37,5%", "pct_label": "thay đổi",
        "tone": "good", "legend_label": "Cải thiện (chiều tốt: giảm)",
        "caption": "Bán khống hợp đồng tương lai giúp điều chỉnh duration mà không phải "
                   "bán trái phiếu cơ sở, giữ nguyên cấu trúc danh mục và tiết kiệm chi phí giao dịch.",
    },
    "status_strip": {
        "kicker": "Phân tích tín dụng",
        "title": "Bảng theo dõi tuân thủ điều khoản vay (covenant)",
        "subtitle": "Năm điều khoản tài chính chính trong hợp đồng vay hợp vốn, đối chiếu "
                    "giá trị thực tế cuối quý với ngưỡng cam kết.",
        "asof": "Q2 2026", "source": "minh họa của tác giả",
        "value_format": "x",
        "rows": [
            {"metric": "Nợ ròng trên EBITDA", "threshold": "Ngưỡng: tối đa 3,5x",
             "value": 3.40, "status": "warn", "value_dp": 2},
            {"metric": "Hệ số bao phủ lãi vay (EBIT/lãi vay)",
             "threshold": "Ngưỡng: tối thiểu 3,0x", "value": 4.80, "status": "pass",
             "value_dp": 2},
            {"metric": "Tỷ lệ nợ trên vốn chủ sở hữu", "threshold": "Ngưỡng: tối đa 1,50x",
             "value": 1.85, "status": "fail", "value_dp": 2},
            {"metric": "Hệ số thanh toán hiện hành", "threshold": "Ngưỡng: tối thiểu 1,20x",
             "value": 1.62, "status": "pass", "value_dp": 2},
            {"metric": "Biên EBITDA", "threshold": "Ngưỡng: tối thiểu 20,0%",
             "value": 18.5, "status": "warn", "value_fmt": "pct"},
        ],
    },
}


def _run_showcase(out_dir, only, dpi):
    os.makedirs(out_dir, exist_ok=True)
    ok = fail = 0
    for cid, params in _SHOWCASE.items():
        if only and cid != only:
            continue
        fn = COMPONENTS[cid]
        try:
            fig = fn(params, params.get("accent") or TEAL)
            out = os.path.join(out_dir, f"{cid}.png")
            save(fig, out, dpi=dpi)
            print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL {cid}: {e}\n"); fail += 1
    print(f"viz_eir_panels: {ok} rendered, {fail} failed")
    return fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--out-dir",
        default="/sessions/jolly-confident-hopper/mnt/outputs/note-pipeline-viz-library/"
                "gallery/super/panels")
    ap.add_argument("--only", default=None)
    ap.add_argument("--dpi", type=int, default=170)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR panel components:", ", ".join(sorted(COMPONENTS))); return 0
    if not args.spec:
        return _run_showcase(args.out_dir, args.only, args.dpi)
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    module = spec.get("module", "MOD")
    accent = (spec.get("theme") or {}).get("accent", TEAL)
    os.makedirs(args.out_dir, exist_ok=True)
    ok = fail = 0
    for fs in spec.get("figures", []):
        fid = fs.get("id"); comp = fs.get("component")
        if args.only and fid != args.only:
            continue
        fn = COMPONENTS.get(comp)
        if fn is None:
            sys.stderr.write(f"WARN unknown panel component '{comp}' (id={fid})\n")
            fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(args.out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir_panels: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
