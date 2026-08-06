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

# Danh sach ung vien theo thu tu uu tien. Duong dan phai dung: thu muc that
# tren he la 'liberation' (KHONG them hau to so nhu ban cu tung hardcode sai)
# -> os.path.exists tra False -> roi tu do ve DejaVu -> mat dau tieng Viet).
_SANS_CANDIDATES = [
    ("Liberation Sans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ("DejaVu Sans", None),
]
_MONO_CANDIDATES = [
    ("Liberation Mono", "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    ("Noto Sans Mono", "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"),
    ("DejaVu Sans Mono", None),
]
# Serif dung cho tieu de lon (draw_masthead). Khong nam trong tuple tra ve cua
# setup_fonts() (interface la (sans_list, mono_list)) nhung van phai la LIST
# ket thuc generic keyword, khong duoc la mot ten tran, theo luat cung CLAUDE.md.
_SERIF_CANDIDATES = [
    ("DejaVu Serif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
]

SANS = ["DejaVu Sans", "sans-serif"]
SERIF = ["DejaVu Serif", "serif"]
MONO = ["DejaVu Sans Mono", "monospace"]


def _register(candidates):
    """Dang ky font vao cache cua matplotlib va tra ve list ten dung duoc.

    Chi dua ten suong khong du: matplotlib co cache font rieng, khong tu quet
    theo ten, phai goi addfont voi duong dan that truoc.
    """
    names = []
    for name, path in candidates:
        if path and os.path.exists(path):
            fm.fontManager.addfont(path)
            names.append(name)
        elif path is None:
            names.append(name)
    return names


def setup_fonts():
    """Tra ve (sans_list, mono_list), moi list KET THUC BANG GENERIC KEYWORD.

    Tra ve LIST chu khong phai chuoi ten tran. Khai mot ten tran khien trinh
    duyet thay glyph theo tung ky tu va lam roi dau tieng Viet: "So lieu"
    thanh "So^' lieu", dau sac tach roi troi noi. Loi nay tinh vi hon tofu
    o vuong nen rat de lot QC bang mat.

    Cung tien the dang ky va cap nhat global SERIF (list, khong tra ve trong
    tuple vi interface chi la 2 phan tu) de draw_masthead dung tieu de van
    tuan thu luat "font-family phai la list ket thuc generic keyword".
    """
    global _FONTS_READY, SANS, SERIF, MONO
    if _FONTS_READY:
        return SANS, MONO
    sans = _register(_SANS_CANDIDATES) + ["sans-serif"]
    mono = _register(_MONO_CANDIDATES) + ["monospace"]
    serif = _register(_SERIF_CANDIDATES) + ["serif"]
    SANS, SERIF, MONO = sans, serif, mono
    plt.rcParams.update({
        "font.family": SANS, "font.size": 10,
        "axes.edgecolor": "#BBBBBB", "axes.linewidth": 0.8,
        "figure.facecolor": PAPER, "savefig.facecolor": PAPER, "axes.facecolor": PAPER,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": MUTED, "ytick.color": MUTED,
    })
    _FONTS_READY = True
    return sans, mono


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
    """Xuat figure ra path. Neu duoi la .svg, ep svg.fonttype='none' de chu van la
    <text> that (co the search/select-copy, khong bien thanh path), phu hop luat
    cung cua repo la tranh anh raster khi in duoc."""
    if str(path).lower().endswith(".svg"):
        matplotlib.rcParams["svg.fonttype"] = "none"
    fig.savefig(path, dpi=dpi, facecolor=PAPER, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


setup_fonts()
