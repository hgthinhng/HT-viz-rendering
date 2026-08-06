#!/usr/bin/env python3
"""_eir_style.py - shared style core for the Editorial Institutional Research (EIR)
viz library (matplotlib/Agg, static PNG for CFA note .docx).

Design doctrine (FT Visual Vocabulary + Bloomberg Intelligence + Goldman/sell-side +
Morningstar brief + The Economist):
  1. TITLE = the finding, not the topic; muted subtitle carries metric + units.
  2. COLOR = meaning, never decoration: navy ink/structure, teal up/positive,
     brick down/negative, gold target/neutral/annotation; everything else grey.
  3. TABULAR (mono) numerals so data aligns.
  4. Direct labels over legends; hairline gridlines; bars from zero; no 3D / rounded
     cards / drop shadows (reads as "AI slop").
  5. Source + "as of" line, always, bottom-left, muted.
Tokens match the note design system (cream paper #FFFEF8) and the core renderer, so a
single spec.json may mix core + EIR components.
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.lines as mlines

# ----------------------------------------------------------------- design tokens
PAPER = "#FFFEF8"; NAVY = "#1F2D4D"; INK = "#1F1F1F"; MUTED = "#6B6B6B"
FAINT = "#9A9488"; GRID = "#E8E5DE"; TEAL = "#2E6B5E"; BRICK = "#B23A2E"
GOLD = "#C08A2E"; INDIGO = "#2C3878"
TONE = {"up": TEAL, "down": BRICK, "flat": MUTED, "neutral": GOLD,
        "pos": TEAL, "neg": BRICK, None: MUTED}

_FONTS_READY = False
SANS = "DejaVu Sans"; SERIF = "DejaVu Serif"; MONO = "DejaVu Sans Mono"

_VN_TEST = "ếấố"  # e-circumflex-acute, a-circumflex-acute, o-circumflex-acute


def _covers(path, chars):
    try:
        from fontTools.ttLib import TTFont
        cmap = TTFont(path).getBestCmap()
        return all(ord(c) in cmap for c in chars)
    except Exception:
        return None  # cannot verify -> trust caller ordering


def _register_pick(paths, need=""):
    """addfont every existing path; return the family name of the first that exists
    (and, if `need` given and verifiable, covers those chars). Deterministic: resolves
    by FILE, not by fontManager name-set matching, so registration can't silently miss."""
    chosen = None
    for p in paths:
        if not os.path.exists(p):
            continue
        try:
            fm.fontManager.addfont(p)
            name = fm.FontProperties(fname=p).get_name()
        except Exception:
            continue
        if chosen is None:
            if need:
                ok = _covers(p, need)
                if ok is False:
                    continue
            chosen = name
    return chosen


def setup_fonts():
    """Lato (sans) + DejaVu Serif (headlines) + a VN-capable mono (Noto Sans Mono /
    Liberation Mono; NOT DejaVu Mono, which drops VN stacked diacritics)."""
    global _FONTS_READY, SANS, SERIF, MONO
    if _FONTS_READY:
        return SANS, SERIF, MONO
    sans = ["/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
            "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
            "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"]
    serif = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
    mono = ["/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf"]
    SANS = _register_pick(sans, _VN_TEST) or "DejaVu Sans"
    SERIF = _register_pick(serif) or "DejaVu Serif"
    MONO = _register_pick(mono, _VN_TEST) or "DejaVu Sans Mono"
    plt.rcParams.update({
        "font.family": SANS, "font.size": 10,
        "axes.edgecolor": "#BBBBBB", "axes.linewidth": 0.8,
        "figure.facecolor": PAPER, "savefig.facecolor": PAPER, "axes.facecolor": PAPER,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": MUTED, "ytick.color": MUTED,
    })
    _FONTS_READY = True
    return SANS, SERIF, MONO


def palette(accent=None):
    base = [accent or TEAL, GOLD, INDIGO, BRICK, "#5C6B73", "#7A5C00"]
    seen, out = set(), []
    for c in base:
        cl = str(c).lower()
        if cl not in seen:
            seen.add(cl); out.append(c)
    return out


def tone_color(tone, accent=None):
    if tone in ("up", "pos"):
        return accent or TEAL
    return TONE.get(tone, MUTED)


def fmt_value(v, kind="num", currency="$", dp=None):
    if v is None or v == "":
        return ""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if kind == "pct":
        return f"{f:,.{1 if dp is None else dp}f}%".replace(".0%", "%")
    if kind == "bps":
        return f"{f:,.0f} bps"
    if kind == "x":
        return f"{f:,.{1 if dp is None else dp}f}x"
    if kind == "cur":
        a = abs(f)
        if a >= 1e9: return f"{currency}{f/1e9:,.1f}B"
        if a >= 1e6: return f"{currency}{f/1e6:,.1f}M"
        if a >= 1e4: return f"{currency}{f/1e3:,.1f}K"
        return f"{currency}{f:,.2f}" if f != int(f) else f"{currency}{f:,.0f}"
    if dp is not None:
        return f"{f:,.{dp}f}"
    return f"{f:,.0f}" if f == int(f) else f"{f:,.2f}"


def despine(ax, keep=("left", "bottom"), grid_axis="y"):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)
    for side in keep:
        ax.spines[side].set_color("#BBBBBB"); ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    if grid_axis in ("y", "both"):
        ax.yaxis.grid(True, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    else:
        ax.yaxis.grid(False)
    if grid_axis in ("x", "both"):
        ax.xaxis.grid(True, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    else:
        ax.xaxis.grid(False)


def draw_masthead(fig, meta, top=0.965):
    setup_fonts()
    accent = meta.get("accent") or TEAL
    x0, x1 = 0.035, 0.965
    fig.add_artist(mlines.Line2D([x0, x1], [top, top], color=NAVY, lw=2.6,
                                 transform=fig.transFigure))
    y = top - 0.055
    if meta.get("kicker"):
        fig.text(x0, y, meta["kicker"].upper(), transform=fig.transFigure, fontsize=8,
                 color=accent, fontweight="bold", family=SANS, ha="left", va="top")
        y -= 0.052
    if meta.get("title"):
        fig.text(x0, y, meta["title"], transform=fig.transFigure, fontsize=15.5,
                 color=NAVY, fontweight="bold", family=SERIF, ha="left", va="top")
        y -= 0.070
    if meta.get("subtitle"):
        fig.text(x0, y, meta["subtitle"], transform=fig.transFigure, fontsize=10,
                 color=MUTED, style="italic", family=SANS, ha="left", va="top")
        y -= 0.062
    if meta.get("rating"):
        _badge(fig, x1, top - 0.060, meta["rating"], ha="right", bg=NAVY, fg=PAPER)
    rule_y = max(y + 0.015, top - 0.22)
    fig.add_artist(mlines.Line2D([x0, x1], [rule_y, rule_y], color=GRID, lw=1.0,
                                 transform=fig.transFigure))
    return rule_y


def draw_source(fig, meta, bottom=0.028):
    setup_fonts()
    x0, x1 = 0.035, 0.965
    fig.add_artist(mlines.Line2D([x0, x1], [bottom + 0.052, bottom + 0.052],
                                 color=GRID, lw=0.9, transform=fig.transFigure))
    bits = []
    if meta.get("source"):
        bits.append(f"Nguồn: {meta['source']}")
    if meta.get("asof"):
        bits.append(f"Số liệu tại {meta['asof']}")
    txt = "  ·  ".join(bits) if bits else "Nguồn: minh họa của tác giả"
    fig.text(x0, bottom, txt, transform=fig.transFigure, fontsize=7.6, color=MUTED,
             family=MONO, ha="left", va="bottom")
    if meta.get("firm"):
        fig.text(x1, bottom, meta["firm"].upper(), transform=fig.transFigure,
                 fontsize=7.6, color=MUTED, family=SANS, ha="right", va="bottom",
                 fontweight="bold")


def _badge(fig, x, y, text, ha="left", bg=NAVY, fg=PAPER, ax=None):
    target = ax if ax is not None else fig
    t = target.text(x, y, f" {text} ", ha=ha, va="center", fontsize=8.5, color=fg,
                    family=SANS, fontweight="bold",
                    transform=(ax.transAxes if ax is not None else fig.transFigure),
                    bbox=dict(boxstyle="square,pad=0.35", fc=bg, ec="none"))
    return t


def eir_fig(meta, figsize=(7.4, 4.7), rect=(0.115, 0.17, 0.83, 0.60)):
    setup_fonts()
    fig = plt.figure(figsize=figsize, facecolor=PAPER)
    rule_y = draw_masthead(fig, meta)
    draw_source(fig, meta)
    left, bottom, w, h = rect
    # keep the plot axes clearly below the masthead closing rule so top ticks,
    # column headers and near-top data never collide with the subtitle band
    max_top = rule_y - 0.035
    if bottom + h > max_top:
        h = max(0.30, max_top - bottom)
    ax = fig.add_axes([left, bottom, w, h], facecolor=PAPER)
    return fig, ax


def save(fig, path, dpi=200):
    fig.savefig(path, dpi=dpi, facecolor=PAPER, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


setup_fonts()
