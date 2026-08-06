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
import importlib.util
import os
import warnings
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.lines as mlines

# ----------------------------------------------------------------- design tokens
# Nguon mau CHUAN cua ca he thong la design-system/tokens.py (Task 2), khong phai
# mot bang mau rieng cua EIR. Ban cu khai mot bang mau GIAY NGA AM tach biet
# (PAPER "#FFFEF8" mau kem am, NAVY "#1F2D4D" ...) trong khi toan bo phan con lai
# cua repo da chot TRANG LANH (xung dot da duoc phan xu, xem CLAUDE.md). De
# nguyen nghia la 48 component EIR ra tong giay kem trong khi phan con lai dung
# nen trang lanh, dung bay "PACKAGE tu nhan la tu du" ma CLAUDE.md canh bao.
#
# Nap tokens.py bang duong dan tuyet doi tinh tu __file__ (KHONG dung duong dan
# tuong doi theo cwd, vi viz_super.py duoc goi tu nhieu thu muc lam viec khac
# nhau). _eir_style.py nam o charts/matplotlib/, tokens.py nam o design-system/,
# hai thu muc anh em duoi goc repo (parents[2] tinh tu file nay).
_TOKENS_PATH = Path(__file__).resolve().parents[2] / "design-system" / "tokens.py"
_tok_spec = importlib.util.spec_from_file_location("_ht_viz_design_tokens", _TOKENS_PATH)
_tok_mod = importlib.util.module_from_spec(_tok_spec)
_tok_spec.loader.exec_module(_tok_mod)
COLORS = _tok_mod.COLORS

# Anh xa TEN hang mau cu (giu nguyen ten de moi component khong phai sua dong
# nao) sang GIA TRI moi lay tu token chuan. Da doc code truoc khi anh xa, khong
# doan mo:
#   NAVY (~76 cho dung, ~93% la color=/ec= van ban hoac duong vien; chi ~7 cho
#         la fc=/bg= nen chip/badge) va INK (~104 cho, chu du lieu/tick pho
#         bien nhat trong toan bo 48 component) deu la "muc nhan manh manh
#         nhat" trong tai lieu goc ("navy ink/structure" - chinh docstring cu
#         goi NAVY la mot dang ink). Gop ve chung COLORS["ink"]: phan cap tieu
#         de/chip (nhan manh) voi chu thuong da duoc chinh bang CO CHU + DAM
#         (fontsize/fontweight), khong chi rieng minh mau, nen gop khong lam
#         mat phan cap thi giac. Tuong phan tren nen trang moi: ~17:1 (rat an
#         toan, con cao hon ban cu tren nen kem).
#   MUTED (~86 cho, phu de/dong nguon/tick mo, VAN LA CHU doc duoc, co luc rat
#         nho 7.6pt) ve COLORS["ink_md"]: tuong phan ~7.56:1, an toan hon ban cu
#         (~5.3:1 tren nen kem truoc day).
#   FAINT (~19 cho, CHI to duong tham chieu dut net / marker / cham legend,
#         KHONG BAO GIO to chu doc duoc - da xac nhan rieng trong _legend() cua
#         viz_eir_diagram.py: tham so mau chi len marker, nhan chu luon fix
#         cung mau INK) ve COLORS["ink_lo"]: du nhin thay ro nhu mot duong/cham,
#         khong can dat nguong tuong phan van ban (~3.1:1, khong dung de doc
#         chu nen khong pham WCAG text-contrast).
#   GRID (hairline gridline/duong ke phan cach, decorative thuan tuy) ve
#         COLORS["line"], dung vai tro no duoc thiet ke cho.
#   TEAL/BRICK/GOLD/INDIGO (chuoi mau valence + categorical dung trong
#         palette() cho da-series) ve pos/neg/warn/accent_hi theo dung nhom mau
#         (xanh la/do/vang/xanh duong), giu nguyen kha nang phan biet chuoi mau.
PAPER = COLORS["paper"]
NAVY = COLORS["ink"]
INK = COLORS["ink"]
MUTED = COLORS["ink_md"]
FAINT = COLORS["ink_lo"]
GRID = COLORS["line"]
TEAL = COLORS["pos"]
BRICK = COLORS["neg"]
GOLD = COLORS["warn"]
INDIGO = COLORS["accent_hi"]
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

    Repo cam fallback im lang (xem CLAUDE.md). Neu mot candidate co duong dan
    ma khong ton tai, canh bao ro font nao, duong dan nao, va no dang bi bo
    qua (roi tiep tuc xet candidate ke tiep trong danh sach) - moi truong khac
    thieu font Liberation ma khong ai biet chinh la kich ban bug ban dau
    (hardcode sai ten thu muc font) tai dien.
    """
    names = []
    for name, path in candidates:
        if path and os.path.exists(path):
            fm.fontManager.addfont(path)
            names.append(name)
        elif path is None:
            names.append(name)
        else:
            warnings.warn(
                f"_eir_style: khong tim thay font '{name}' tai '{path}', "
                "bo qua candidate nay va roi xuong candidate ke tiep. Neu day "
                "la moi truong thieu font Liberation, tieng Viet co the mat "
                "dau khi roi ve DejaVu."
            )
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
