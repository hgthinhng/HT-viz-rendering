#!/usr/bin/env python3
"""viz_eir.py, Editorial Institutional Research chart library for CFA study notes.

Static matplotlib PNGs (Agg) that embed into the note .docx like the existing figures.
Design language: FT Visual Vocabulary + Bloomberg Intelligence + Goldman/sell-side +
Morningstar brief + The Economist. Every component shares the editorial chrome (kicker /
serif headline / subtitle / source line), honours the subject accent, and reads the SAME
spec.json contract as the core note-pipeline-viz renderer, so a note may mix core + EIR.

Editorial meta keys live inside params: title, kicker, subtitle, source, asof, rating,
firm. They render as furniture; data keys drive the plot.

Usage:
  python3 viz_eir.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_eir.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _eir_style as S
from _eir_style import (
    PAPER, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge, tint,
)
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize, LinearSegmentedColormap

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved


def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


def _fmt(p, v):
    return fmt_value(v, p.get("y_format", "num"), p.get("currency", "$"), p.get("dp"))


def _axis_fmt(ax, p, which):
    yf = p.get("y_format")
    axis = ax.yaxis if which == "y" else ax.xaxis
    if yf == "pct":
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}%"))
    elif yf == "cur":
        cur = p.get("currency", "$")
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_value(v, "cur", cur)))
    elif yf == "x":
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}x"))


# ========================================================= comparison / ranking
def c_dumbbell(p, accent):
    """Dumbbell, độ dịch chuyển của nhiều hạng mục giữa hai mốc.

    Trả lời: "Từng hạng mục dịch chuyển bao nhiêu giữa hai mốc, và hạng mục nào dịch
    mạnh nhất?" Nhấn vào ĐỘ CHÊNH giữa hai đầu chứ không vào giá trị tuyệt đối, nên
    đọc nhanh hơn hai cột cạnh nhau.

    Dữ liệu cần: categories, before, after cùng một đơn vị. Tuỳ chọn left_name,
    right_name, sort ("after" hoặc "delta").

    KHÔNG dùng khi có hơn hai mốc thời gian (dùng index100 hoặc bump), hoặc khi thứ
    hạng quan trọng hơn độ chênh (dùng lollipop).
    """
    cats = list(p["categories"]); a = list(map(float, p["before"])); b = list(map(float, p["after"]))
    order = list(range(len(cats)))
    if p.get("sort") == "after":
        order = sorted(order, key=lambda i: b[i])
    elif p.get("sort") == "delta":
        order = sorted(order, key=lambda i: b[i] - a[i])
    cats = [cats[i] for i in order]; a = [a[i] for i in order]; b = [b[i] for i in order]
    n = len(cats)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.4, max(3.2, 0.52 * n + 2.0)),
                      rect=(0.30, 0.16, 0.63, 0.60))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n)
    lname, rname = p.get("left_name", "Trước"), p.get("right_name", "Sau")
    for yi, av, bv in zip(y, a, b):
        ax.hlines(yi, min(av, bv), max(av, bv), color=FAINT, lw=2.2, zorder=1)
    ax.scatter(a, y, s=95, color=MUTED, zorder=3, label=lname)
    ax.scatter(b, y, s=95, color=accent, zorder=3, label=rname)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=9, color=INK)
    ax.set_ylim(-0.6, n - 0.4)
    for yi, av, bv in [(y[-1], a[-1], b[-1]), (y[0], a[0], b[0])]:
        ax.annotate(_fmt(p, av), (av, yi), color=MUTED, fontsize=8.3,
                    ha="right" if av <= bv else "left", va="bottom",
                    xytext=(-4 if av <= bv else 4, 4), textcoords="offset points")
        ax.annotate(_fmt(p, bv), (bv, yi), color=accent, fontsize=8.3, fontweight="bold",
                    ha="left" if av <= bv else "right", va="bottom",
                    xytext=(4 if av <= bv else -4, 4), textcoords="offset points")
    ax.margins(x=0.14)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right", ncol=2,
              bbox_to_anchor=(1.0, 1.005), handletextpad=0.3, columnspacing=1.2)
    _axis_fmt(ax, p, "x")
    return fig


def c_lollipop(p, accent):
    """Lollipop, xếp hạng một chỉ tiêu theo hạng mục.

    Trả lời: "Hạng mục nào đóng góp nhiều nhất, và khoảng cách giữa chúng bao xa?"
    Chấm cuối cây kẹo đặt mắt đúng vào giá trị, nhẹ hơn cột đặc khi có nhiều hạng mục.

    Dữ liệu cần: categories, values cùng đơn vị. Tuỳ chọn highlight để nhấn một hạng
    mục, sort để xếp theo giá trị.

    KHÔNG dùng khi giá trị có cả âm lẫn dương và dấu là thông điệp chính (dùng
    diverging_bar), hoặc khi dưới bốn hạng mục vì câu văn xuôi gọn hơn.
    """
    cats = list(p["categories"]); vals = list(map(float, p["values"]))
    idx = list(range(len(cats))); s = p.get("sort", True)
    if s:
        idx = sorted(idx, key=lambda i: vals[i], reverse=(s != "asc"))
    cats = [cats[i] for i in idx]; vals = [vals[i] for i in idx]; n = len(cats)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.4, max(3.0, 0.46 * n + 2.0)),
                      rect=(0.30, 0.16, 0.63, 0.60))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n); hl = p.get("highlight")
    cols = [GOLD if (hl is not None and (c == hl or i == hl)) else accent
            for i, c in enumerate(cats)]
    ax.hlines(y, 0, vals, color=FAINT, lw=1.6, zorder=1)
    ax.scatter(vals, y, s=90, color=cols, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=9, color=INK)
    ax.invert_yaxis()
    _lo = min(0, min(vals)); _hi = max(0, max(vals)); _pad = ((_hi - _lo) or 1) * 0.17
    ax.set_xlim(_lo - _pad, _hi + _pad)
    for yi, v in zip(y, vals):
        if v < 0:
            ax.annotate(_fmt(p, v) + "  ", (v, yi), va="center", ha="right", fontsize=8.4, color=INK)
        else:
            ax.annotate("  " + _fmt(p, v), (v, yi), va="center", ha="left", fontsize=8.4, color=INK)
    _axis_fmt(ax, p, "x")
    return fig


def c_diverging_bar(p, accent):
    """Thanh phân kỳ hai chiều quanh mốc không.

    Trả lời: "Hạng mục nào vượt chuẩn, hạng mục nào thua chuẩn, và chênh bao nhiêu?"
    Mốc không là trục đối xứng nên dấu đọc được ngay mà không phải tra nhãn.

    Dữ liệu cần: categories, values có cả âm lẫn dương, cùng đơn vị. Tuỳ chọn sort,
    use_accent_up để chọn màu nào mang nghĩa dương.

    KHÔNG dùng khi mọi giá trị cùng dấu, vì khi đó trục không mất vai trò và hình
    suy biến thành lollipop nhưng tốn gấp đôi bề ngang.
    """
    cats = list(p["categories"]); vals = list(map(float, p["values"]))
    idx = list(range(len(cats)))
    if p.get("sort", True):
        idx = sorted(idx, key=lambda i: vals[i])
    cats = [cats[i] for i in idx]; vals = [vals[i] for i in idx]; n = len(cats)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.4, max(3.0, 0.46 * n + 2.0)),
                      rect=(0.30, 0.16, 0.63, 0.60))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n)
    up = accent if p.get("use_accent_up") else TEAL
    cols = [up if v >= 0 else BRICK for v in vals]
    ax.barh(y, vals, height=0.62, color=cols, zorder=2)
    ax.axvline(0, color=INK, lw=1.0, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=9, color=INK)
    ax.set_ylim(-0.6, n - 0.4)
    _dv = (max(vals) - min(vals)) or 1
    ax.set_xlim(min(0, min(vals)) - 0.17 * _dv, max(0, max(vals)) + 0.17 * _dv)
    pad = (max(vals) - min(vals) or 1) * 0.02
    for yi, v in zip(y, vals):
        ax.annotate((" " if v >= 0 else "") + _fmt(p, v),
                    (v + (pad if v >= 0 else -pad), yi), va="center",
                    ha="left" if v >= 0 else "right", fontsize=8.4, color=INK)
    _axis_fmt(ax, p, "x")
    return fig


def c_range_dot(p, accent):
    """Chấm trong khoảng, giá trị điểm đặt trong dải thấp tới cao.

    Trả lời: "Đồng thuận nằm ở đâu trong dải ước tính, và dải đó rộng hẹp ra sao?"
    Đường tham chiếu cắt ngang cho biết giá hiện tại nằm trong hay ngoài dải.

    Dữ liệu cần: rows dạng {label, low, high, point}. Tuỳ chọn ref và ref_label cho
    đường tham chiếu, show_values để in số ở hai đầu.

    KHÔNG dùng khi dải chỉ có hai đầu mà không có điểm giữa có nghĩa (dùng dumbbell),
    hoặc khi các dòng khác đơn vị nhau.
    """
    rows = p["rows"]; n = len(rows)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.4, max(3.0, 0.5 * n + 2.0)),
                      rect=(0.30, 0.16, 0.63, 0.60))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n)
    pts = [float(r["point"]) if r.get("point") is not None else (float(r["lo"]) + float(r["hi"])) / 2
           for r in rows]
    lo = [float(r["lo"]) for r in rows]; hi = [float(r["hi"]) for r in rows]
    xerr = np.array([[pt - l for pt, l in zip(pts, lo)], [h - pt for pt, h in zip(pts, hi)]])
    if p.get("ref") is not None:
        ax.axvline(float(p["ref"]), color=GOLD, ls=(0, (4, 3)), lw=1.2, zorder=1)
        if p.get("ref_label"):
            ax.annotate(p["ref_label"], (float(p["ref"]), n - 0.5), color=GOLD,
                        fontsize=8, ha="center", va="bottom")
    ax.errorbar(pts, y, xerr=xerr, fmt="o", color=accent, ecolor=FAINT, elinewidth=1.6,
                capsize=3.5, markersize=7, zorder=3, linestyle="none")
    ax.set_yticks(y); ax.set_yticklabels([r["label"] for r in rows], fontsize=9, color=INK)
    ax.set_ylim(-0.6, n - 0.4)
    if p.get("show_values", True):
        for yi, pt, l, h in zip(y, pts, lo, hi):
            ax.annotate(f"  {_fmt(p, pt)}  [{_fmt(p, l)}, {_fmt(p, h)}]", (h, yi),
                        va="center", fontsize=7.8, color=MUTED)
    _axis_fmt(ax, p, "x")
    return fig


def c_bump(p, accent):
    """Bump chart, đổi thứ hạng qua nhiều kỳ.

    Trả lời: "Thứ hạng đổi chỗ thế nào qua các kỳ, ai lên ai xuống?" Trục dọc là HẠNG
    chứ không phải giá trị, nên hai thực thể cách nhau một bậc trông như nhau dù giá
    trị chênh rất xa.

    Dữ liệu cần: periods, entities dạng {name, ranks} với ranks là số nguyên. Tuỳ
    chọn highlight để nhấn một đường.

    KHÔNG dùng khi độ lớn của khoảng cách mới là thông điệp, vì bump cố ý vứt bỏ nó.
    Quá tám thực thể thì đường rối thành búi, tách bảng hoặc chọn nhấn vài đường.
    """
    periods = p["periods"]; ent = p["entities"]
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, 4.8), rect=(0.10, 0.16, 0.80, 0.60))
    despine(ax, keep=(), grid_axis="")
    hl = set(p.get("highlight") or []); x = np.arange(len(periods)); cols = palette(accent)
    for i, (name, ranks) in enumerate(ent.items()):
        on = (not hl) or (name in hl)
        col = cols[i % len(cols)] if on else FAINT
        lw = 2.6 if (on and hl) else 2.0
        ax.plot(x, ranks, "o-", color=col, lw=lw, markersize=7, markerfacecolor=PAPER,
                markeredgecolor=col, markeredgewidth=1.8, zorder=3 if on else 1)
        if on:
            ax.annotate(f"{name}", (x[-1], ranks[-1]), color=col, fontsize=8.6,
                        va="center", ha="left", xytext=(10, 0), textcoords="offset points",
                        fontweight="bold" if hl else "normal")
            ax.annotate(f"{name}", (x[0], ranks[0]), color=col, fontsize=8.6,
                        va="center", ha="right", xytext=(-10, 0), textcoords="offset points")
    ax.set_yticks(range(1, max(max(r) for r in ent.values()) + 1)); ax.invert_yaxis()
    ax.set_xticks(x); ax.set_xticklabels(periods, fontsize=9, color=INK)
    ax.set_xlim(-0.9, len(periods) - 0.1 + 0.9)
    ax.set_ylabel("Thứ hạng", fontsize=9, color=MUTED)
    return fig


# ================================================================= time / trend
def c_fan(p, accent):
    """Biểu đồ quạt, dải bất định của dự báo mở rộng theo thời gian.

    Trả lời: "Dự báo trung tâm là bao nhiêu, và vùng bất định quanh nó rộng ra thế
    nào theo thời gian?" Dải tô nhạt dần ra ngoài đọc thẳng thành mức tin cậy.

    Dữ liệu cần: hist_x, hist_y cho phần thực tế; fcast_x, median và bands dạng danh
    sách {lo, hi} cho phần dự báo. Tuỳ chọn split_label đặt tên vạch chia.

    KHÔNG dùng khi các dải không đến từ một phân phối thật mà chỉ là ba kịch bản rời
    rạc, vì hình quạt khẳng định một liên tục xác suất không có thật (dùng
    scenario_cards).
    """
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, 4.6), rect=(0.10, 0.16, 0.83, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    hx, hy = p.get("hist_x", []), p.get("hist_y", [])
    fx, med = p["fcast_x"], p["median"]
    bands = sorted(p.get("bands", []), key=lambda bd: bd["hi"][0] - bd["lo"][0], reverse=True)
    nb = len(bands)
    for k, bd in enumerate(bands):
        alpha = 0.16 + 0.18 * (k / max(1, nb - 1)) if nb > 1 else 0.28
        ax.fill_between(fx, bd["lo"], bd["hi"], color=accent, alpha=alpha, lw=0, zorder=2)
    if hx:
        ax.plot(hx, hy, color=NAVY, lw=1.9, zorder=4)
    ax.plot(fx, med, color=accent, lw=1.9, ls=(0, (5, 2)), zorder=4)
    ax.axvline(fx[0], color=FAINT, lw=1.0, ls=(0, (2, 2)), zorder=1)
    ax.annotate(p.get("split_label", "Dự báo →"), (fx[0], ax.get_ylim()[1]), color=MUTED,
                fontsize=8, ha="left", va="top", xytext=(4, -2), textcoords="offset points")
    if bands:
        ax.annotate(f" {bands[0].get('label','')}", (fx[-1], bands[0]["hi"][-1]),
                    color=MUTED, fontsize=8, va="center")
    _axis_fmt(ax, p, "y")
    return fig


def c_spread(p, accent):
    """Hai chuỗi và chênh lệch giữa chúng.

    Trả lời: "Hai lãi suất hay hai giá đang giãn ra hay thu lại, và chênh lệch hiện
    ở đâu so với lịch sử?" Khung dưới vẽ riêng phần chênh nên không phải trừ bằng mắt.

    Dữ liệu cần: x, series_a, series_b cùng đơn vị, diff là chuỗi chênh lệch đã tính.
    Cờ zero_is_signal bật khi việc chênh lệch chạm không có nghĩa kinh tế, ví dụ đảo
    ngược đường cong lợi suất.

    KHÔNG dùng khi hai chuỗi khác đơn vị, vì phép trừ khi đó vô nghĩa dù chart vẫn vẽ
    ra được.
    """
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, 4.6), rect=(0.10, 0.16, 0.83, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    x = p["x"]
    numeric = all(isinstance(v, (int, float)) for v in x)
    xs = np.array(x, float) if numeric else np.arange(len(x))
    if p.get("diff"):
        d = p["diff"]["values"]
        # zero_is_signal=True (mac dinh, giu nguyen hanh vi cu, khong pha spec.json nao
        # dang goi component "spread"): nguong 0 mang nghia canh bao (vd dao nguoc 2s10s)
        # nen to TEAL/BRICK theo dau. Dat False cho butterfly hoac bat ky spread nao ma
        # dau khong mang nghia tot/xau pho quat (muc 3.3 cua docs/specs/2026-08-07-
        # yield-forward-curve-design.md) - khi do CHI dung 1 mau accent trung tinh, tranh
        # traffic-light gia.
        zero_is_signal = p["diff"].get("zero_is_signal", True)
        if zero_is_signal:
            ax.fill_between(xs, d, 0, where=[v >= 0 for v in d], color=TEAL, alpha=0.25, lw=0)
            ax.fill_between(xs, d, 0, where=[v < 0 for v in d], color=BRICK, alpha=0.25, lw=0)
        else:
            ax.fill_between(xs, d, 0, color=accent, alpha=0.14, lw=0)
        ax.plot(xs, d, color=NAVY, lw=2.0, zorder=3); ax.axhline(0, color=INK, lw=1.0)
        ax.annotate(" " + p["diff"].get("name", "Spread"), (xs[-1], d[-1]), color=NAVY,
                    fontsize=9, va="center", fontweight="bold")
    else:
        a, b = p["series_a"], p["series_b"]
        ax.fill_between(xs, a["values"], b["values"], color=accent, alpha=0.16, lw=0)
        ax.plot(xs, a["values"], color=accent, lw=2.0, zorder=3)
        ax.plot(xs, b["values"], color=MUTED, lw=2.0, zorder=3)
        _ae, _be = a["values"][-1], b["values"][-1]
        ax.annotate(" " + a.get("name", "A"), (xs[-1], _ae), color=accent, fontsize=9,
                    va="bottom" if _ae >= _be else "top", fontweight="bold")
        ax.annotate(" " + b.get("name", "B"), (xs[-1], _be), color=MUTED, fontsize=9,
                    va="top" if _ae >= _be else "bottom")
    if not numeric:
        ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=9, color=INK)
    _axis_fmt(ax, p, "y"); fig.subplots_adjust(right=0.86)
    return fig


def c_index100(p, accent):
    """Chỉ số hoá về gốc 100, so hiệu suất tương đối trên MỘT trục.

    Trả lời: "Từ cùng một điểm xuất phát, chuỗi nào chạy nhanh hơn?" Đây là cách repo
    thay cho trục kép: mọi chuỗi quy về 100 tại kỳ gốc nên so được trực tiếp.

    Dữ liệu cần: x, series dạng {name, values}. Tuỳ chọn base là chỉ số kỳ gốc,
    rebase để tự quy đổi.

    KHÔNG dùng khi mức tuyệt đối là thông điệp (một quỹ 100 tỷ và một quỹ 1 tỷ cùng
    tăng 20% sẽ trông y hệt nhau), hoặc khi kỳ gốc rơi vào một điểm dị thường vì mọi
    đường sau đó đều bị méo theo.
    """
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, 4.6), rect=(0.10, 0.16, 0.83, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    x = p["x"]; numeric = all(isinstance(v, (int, float)) for v in x)
    xs = np.array(x, float) if numeric else np.arange(len(x))
    base = p.get("base", 100); cols = palette(accent)
    for i, s in enumerate(p["series"]):
        v = np.array(s["values"], float)
        if p.get("rebase", True):
            v = v / v[0] * base
        ax.plot(xs, v, color=cols[i % len(cols)], lw=2.2, zorder=3)
        ax.annotate(f" {s['name']}", (xs[-1], v[-1]), color=cols[i % len(cols)],
                    fontsize=9, va="center", fontweight="bold")
    ax.axhline(base, color=FAINT, lw=1.0, ls=(0, (3, 3)))
    ax.margins(y=0.10)
    if not numeric:
        ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=9, color=INK)
    ax.set_ylabel(f"Chỉ số (gốc = {base})", fontsize=9, color=MUTED)
    fig.subplots_adjust(right=0.85)
    return fig


def c_connected_scatter(p, accent):
    """Scatter nối theo thời gian, quỹ đạo của hai biến qua các kỳ.

    Trả lời: "Quan hệ giữa hai biến di chuyển thế nào qua thời gian, có quay vòng hay
    đổi chế độ không?" Đường nối biến scatter tĩnh thành một quỹ đạo đọc được.

    Dữ liệu cần: points dạng {label, x, y} xếp theo thứ tự thời gian, cộng x_label và
    y_label.

    KHÔNG dùng khi các điểm không có thứ tự thời gian tự nhiên, vì khi đó đường nối
    là một khẳng định về trình tự mà dữ liệu không có (dùng comps_scatter).
    """
    pts = p["points"]
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.0, 5.0), rect=(0.13, 0.16, 0.80, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="both")
    xs = [q["x"] for q in pts]; ys = [q["y"] for q in pts]
    ax.plot(xs, ys, color=accent, lw=1.6, zorder=2, alpha=0.75)
    ax.scatter(xs, ys, s=42, color=accent, zorder=3, edgecolor=PAPER, linewidth=1)
    for q in pts:
        if q.get("label"):
            ax.annotate(q["label"], (q["x"], q["y"]), fontsize=8, color=INK,
                        xytext=(5, 4), textcoords="offset points")
    ax.scatter([xs[0]], [ys[0]], s=90, facecolor=PAPER, edgecolor=MUTED, linewidth=1.8, zorder=4)
    ax.scatter([xs[-1]], [ys[-1]], s=90, color=GOLD, zorder=4)
    if p.get("x_label"): ax.set_xlabel(p["x_label"], fontsize=9.5, color=INK)
    if p.get("y_label"): ax.set_ylabel(p["y_label"], fontsize=9.5, color=INK)
    return fig


# ================================================================= distribution
def c_boxplot(p, accent):
    """Hộp phân phối, so hình dạng phân phối giữa các nhóm.

    Trả lời: "Nhóm nào phân tán rộng hơn, và đuôi nằm ở đâu?" Hộp cho trung vị và tứ
    phân vị, râu cho vùng ngoài, nên đọc được cả tâm lẫn độ rộng.

    Dữ liệu cần: groups và boxes, mỗi box là một danh sách quan sát thật.

    KHÔNG dùng khi mỗi nhóm dưới khoảng mười quan sát, vì tứ phân vị của mẫu quá nhỏ
    là con số gợi ý độ chính xác không có thật (dùng dot strip hiện từng điểm).
    """
    groups = p["groups"]; n = len(groups)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.2, 4.6), rect=(0.12, 0.16, 0.81, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    data = [list(map(float, g["data"])) for g in groups]
    bp = ax.boxplot(data, vert=True, widths=0.55, patch_artist=True,
                    medianprops=dict(color=NAVY, lw=1.8),
                    whiskerprops=dict(color=MUTED, lw=1.2), capprops=dict(color=MUTED, lw=1.2),
                    flierprops=dict(marker="o", markersize=3, markerfacecolor=FAINT, markeredgecolor="none"))
    for patch in bp["boxes"]:
        patch.set_facecolor(accent); patch.set_alpha(0.28); patch.set_edgecolor(accent)
    ax.set_xticks(range(1, n + 1)); ax.set_xticklabels([g["name"] for g in groups], fontsize=9, color=INK)
    for i, d in enumerate(data, 1):
        med = float(np.median(d))
        ax.annotate(_fmt(p, med), (i + 0.32, med), va="center", fontsize=8, color=NAVY)
    _axis_fmt(ax, p, "y")
    return fig


def c_lorenz(p, accent):
    """Đường Lorenz, mức độ tập trung của một tổng.

    Trả lời: "Bao nhiêu phần trăm cấu phần chiếm bao nhiêu phần trăm tổng?" Khoảng
    cách từ đường chéo bình đẳng đọc thẳng thành mức tập trung.

    Dữ liệu cần: values là tỷ trọng hoặc giá trị của từng cấu phần, cộng x_label,
    y_label.

    KHÔNG dùng khi dưới khoảng mười cấu phần, vì đường gãy khúc thô và bảng tỷ trọng
    nói rõ hơn.
    """
    v = np.sort(np.array(p["values"], float)); cum = np.cumsum(v) / v.sum()
    cum = np.insert(cum, 0, 0); xs = np.linspace(0, 1, len(cum))
    gini = 1 - np.sum((cum[1:] + cum[:-1]) * np.diff(xs))
    fig, ax = eir_fig(_meta(p, accent), figsize=(6.4, 5.2), rect=(0.14, 0.16, 0.78, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="both")
    ax.plot([0, 1], [0, 1], color=FAINT, lw=1.3, ls=(0, (4, 3)))
    ax.plot(xs, cum, color=accent, lw=2.4, zorder=3)
    ax.fill_between(xs, cum, xs, color=accent, alpha=0.14)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel(p.get("x_label", "Tỷ lệ tích lũy của mẫu"), fontsize=9.5, color=INK)
    ax.set_ylabel(p.get("y_label", "Tỷ lệ tích lũy của giá trị"), fontsize=9.5, color=INK)
    b = _badge(fig, 0.0, 0.0, f"Gini = {gini:.2f}", ax=ax, bg=NAVY, fg=PAPER)
    b.set_position((0.06, 0.90))
    return fig


# =============================================================== KPI vs target
def c_bullet(p, accent):
    """Thanh bullet, thực tế so với mục tiêu trên nền dải định tính.

    Trả lời: "Chỉ tiêu này đã đạt ngưỡng chưa, và đang nằm ở vùng nào?" Thay cho gauge
    vốn bị repo cấm, và xếp được nhiều dòng thành một cột gọn.

    Dữ liệu cần: rows dạng {label, value, target, bands}. Dải nền dùng ba sắc độ xám
    của cùng một thang, không tô đỏ vàng xanh.

    KHÔNG dùng khi không có mục tiêu hoặc ngưỡng thật để so, vì khi đó vạch mục tiêu
    là một con số bịa nằm giữa hình.
    """
    rows = p["rows"]; n = len(rows)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.4, max(2.6, 0.85 * n + 1.8)),
                      rect=(0.28, 0.18, 0.66, 0.58))
    despine(ax, keep=("bottom",), grid_axis="x")
    # 3 bac nen bullet chart (kem/te/tot), dan xuat tu INK qua tint() thay vi
    # 3 hex kem/nau am rieng - giu trung tinh, lanh, dung sac cua token that.
    band_shades = [tint(INK, 0.06), tint(INK, 0.13), tint(INK, 0.22)]; maxend = 0
    for i, r in enumerate(rows):
        yc = n - 1 - i
        limits = r.get("bands") or [r["target"] * 0.8, r["target"], r["target"] * 1.25]
        prev = 0
        for j, lim in enumerate(limits):
            ax.barh(yc, lim - prev, left=prev, height=0.62, color=band_shades[min(j, 2)], zorder=1)
            prev = lim
        maxend = max(maxend, prev)
        ax.barh(yc, r["actual"], height=0.24, color=NAVY, zorder=3)
        ax.vlines(r["target"], yc - 0.28, yc + 0.28, color=GOLD, lw=2.6, zorder=4)
        ax.annotate(_fmt(p, r["actual"]), (r["actual"], yc), va="center", ha="left",
                    fontsize=8.4, color=INK, xytext=(4, 0), textcoords="offset points", zorder=5)
    ax.set_yticks(range(n)); ax.set_yticklabels([r["label"] for r in reversed(rows)], fontsize=9, color=INK)
    ax.set_ylim(-0.6, n - 0.4); ax.set_xlim(0, maxend * 1.12)
    _axis_fmt(ax, p, "x")
    handles = [Rectangle((0, 0), 1, 1, fc=NAVY), mlines.Line2D([0], [0], color=GOLD, lw=2.6),
               Rectangle((0, 0), 1, 1, fc=band_shades[1])]
    ax.legend(handles, ["Thực tế", "Mục tiêu", "Vùng chuẩn"], frameon=False, fontsize=8,
              loc="lower right", bbox_to_anchor=(1.0, 1.005), ncol=3, handlelength=1.3,
              columnspacing=1.2, handletextpad=0.4)
    return fig


# ============================================================ sell-side archetypes
def c_football_field(p, accent):
    """Football field, dải định giá theo từng phương pháp.

    Trả lời: "Các phương pháp định giá cho khoảng nào, chúng có hội tụ không, và giá
    hiện tại nằm ở đâu so với vùng hội tụ?"

    Dữ liệu cần: methods dạng {name, low, high}, current là giá hiện tại, target là
    vùng hoặc điểm mục tiêu.

    KHÔNG dùng khi chỉ có một phương pháp, vì cả giá trị của hình nằm ở chỗ so nhiều
    dải với nhau.
    """
    methods = p["methods"]; n = len(methods)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, max(3.0, 0.6 * n + 2.0)),
                      rect=(0.30, 0.17, 0.63, 0.58))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n)
    for yi, m in zip(y, reversed(methods)):
        lo, hi = float(m["low"]), float(m["high"])
        ax.barh(yi, hi - lo, left=lo, height=0.52, color=accent, alpha=0.55,
                edgecolor=accent, linewidth=1.0, zorder=2)
        ax.annotate(_fmt(p, lo), (lo, yi), va="center", ha="right", fontsize=7.8, color=MUTED,
                    xytext=(-3, 0), textcoords="offset points")
        ax.annotate(_fmt(p, hi), (hi, yi), va="center", ha="left", fontsize=7.8, color=MUTED,
                    xytext=(3, 0), textcoords="offset points")
    ax.set_yticks(y); ax.set_yticklabels([m["name"] for m in reversed(methods)], fontsize=9, color=INK)
    _lows = [float(m["low"]) for m in methods]; _highs = [float(m["high"]) for m in methods]
    _rng = (max(_highs) - min(_lows)) or 1
    ax.set_xlim(min(_lows) - 0.13 * _rng, max(_highs) + 0.11 * _rng)
    ax.set_ylim(-1.0, n - 0.4 + 0.4)
    if p.get("current") is not None:
        cx = float(p["current"]); ax.axvline(cx, color=NAVY, lw=1.8, zorder=4)
        ax.annotate(f"Giá hiện tại {_fmt(p, cx)}", (cx, n - 0.5), color=NAVY, fontsize=8.4,
                    fontweight="bold", ha="center", va="bottom")
    if p.get("target") is not None:
        tx = float(p["target"]); ax.axvline(tx, color=GOLD, lw=1.8, ls=(0, (4, 3)), zorder=4)
        ax.annotate(f"Mục tiêu {_fmt(p, tx)}", (tx, -0.5), color=GOLD, fontsize=8.4,
                    fontweight="bold", ha="center", va="top")
    _axis_fmt(ax, p, "x")
    return fig


def c_maturity_ladder(p, accent):
    """Thang đáo hạn, nghĩa vụ nợ dồn vào năm nào.

    Trả lời: "Áp lực tái tài trợ rơi vào năm nào, và có bức tường đáo hạn không?"

    Dữ liệu cần: years và series dạng {name, values} theo từng loại nợ.

    KHÔNG dùng khi kỳ hạn chưa chốt hoặc phần lớn nợ là hạn mức quay vòng, vì cột
    theo năm khẳng định một lịch trả nợ cứng mà thực tế không có.
    """
    years = p["years"]; series = p["series"]
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, 4.6), rect=(0.11, 0.17, 0.82, 0.58))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    x = np.arange(len(years)); cols = palette(accent); bottom = np.zeros(len(years))
    for i, s in enumerate(series):
        v = np.array(s["values"], float)
        ax.bar(x, v, 0.62, bottom=bottom, color=cols[i % len(cols)], label=s.get("name", ""), zorder=2)
        bottom += v
    ax.set_xticks(x); ax.set_xticklabels(years, fontsize=9, color=INK); ax.set_ylim(bottom=0)
    for xi, tot in zip(x, bottom):
        ax.annotate(_fmt(p, tot), (xi, tot), ha="center", va="bottom", fontsize=8.2, color=INK,
                    xytext=(0, 2), textcoords="offset points")
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=8.5, loc="upper right")
    _axis_fmt(ax, p, "y")
    return fig


def c_comps_scatter(p, accent):
    """Scatter so sánh cùng ngành, bội số theo một biến giải thích.

    Trả lời: "Bội số của doanh nghiệp này cao hay thấp so với mức mà tăng trưởng của
    nó giải thích được?" Đường hồi quy biến câu hỏi đắt hay rẻ thành khoảng cách tới
    đường.

    Dữ liệu cần: points dạng {label, x, y}, x_label, y_label. Tuỳ chọn fit để vẽ
    đường xu hướng.

    KHÔNG dùng khi dưới sáu điểm, vì đường hồi quy qua vài điểm là một khẳng định
    thống kê không đứng được.
    """
    pts = p["points"]
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.0, 5.0), rect=(0.13, 0.16, 0.80, 0.60))
    despine(ax, keep=("left", "bottom"), grid_axis="both")
    xs = np.array([q["x"] for q in pts], float); ys = np.array([q["y"] for q in pts], float)
    if p.get("fit", True) and len(pts) >= 3:
        b, a = np.polyfit(xs, ys, 1); xr = np.linspace(xs.min(), xs.max(), 50)
        ax.plot(xr, a + b * xr, color=FAINT, lw=1.4, ls=(0, (5, 3)), zorder=1)
        ss = 1 - np.sum((ys - (a + b * xs)) ** 2) / np.sum((ys - ys.mean()) ** 2)
        ax.annotate(f"R² = {ss:.2f}", (0.02, 0.96), xycoords="axes fraction",
                    fontsize=8.5, color=MUTED, va="top")
    for q in pts:
        hl = q.get("highlight")
        ax.scatter([q["x"]], [q["y"]], s=95 if hl else 55, color=GOLD if hl else accent,
                   zorder=4 if hl else 3, edgecolor=PAPER, linewidth=1)
        if q.get("label"):
            ax.annotate(q["label"], (q["x"], q["y"]), fontsize=8, color=NAVY if hl else INK,
                        fontweight="bold" if hl else "normal", xytext=(5, 4), textcoords="offset points")
    if p.get("x_label"): ax.set_xlabel(p["x_label"], fontsize=9.5, color=INK)
    if p.get("y_label"): ax.set_ylabel(p["y_label"], fontsize=9.5, color=INK)
    return fig


# ============================================================= part-to-whole
def c_marimekko(p, accent):
    """Marimekko, cơ cấu hai chiều với chiều rộng mang nghĩa.

    Trả lời: "Mỗi mảng lớn cỡ nào, và bên trong nó cơ cấu ra sao?" Chiều rộng cột là
    quy mô, chiều cao là tỷ trọng, nên đọc được cả hai chiều trong một hình.

    Dữ liệu cần: columns là các mảng lớn kèm quy mô, segments là các phân khúc, data
    là ma trận tỷ trọng.

    KHÔNG dùng quá sáu cột hoặc quá năm phân khúc, vì ô nhỏ mất nhãn và người đọc
    quay sang so diện tích, thứ mắt người ước lượng rất tệ.
    """
    cols = p["columns"]; segs = p["segments"]; data = np.array(p["data"], float)
    widths = np.array([c["size"] for c in cols], float); widths = widths / widths.sum() * 100.0
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.8, 5.0), rect=(0.09, 0.17, 0.84, 0.58))
    despine(ax, keep=(), grid_axis=""); seg_cols = palette(accent); x_left = 0.0
    for j, c in enumerate(cols):
        w = widths[j]; col_vals = data[:, j]; shares = col_vals / col_vals.sum() * 100.0; bottom = 0.0
        for i, h in enumerate(shares):
            ax.bar(x_left, h, width=w, bottom=bottom, align="edge", color=seg_cols[i % len(seg_cols)],
                   edgecolor=PAPER, linewidth=1.2, zorder=2)
            if h >= 8 and w >= 7:
                ax.text(x_left + w / 2, bottom + h / 2, f"{h:.0f}%", ha="center", va="center",
                        fontsize=7.6, color=PAPER, fontweight="bold")
            bottom += h
        ax.text(x_left + w / 2, 101.5, c["name"], ha="center", va="bottom", fontsize=8.4, color=INK)
        ax.text(x_left + w / 2, -3, f"{w:.0f}%", ha="center", va="top", fontsize=7.6, color=MUTED)
        x_left += w
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_xticks([]); ax.set_yticks([])
    handles = [Rectangle((0, 0), 1, 1, color=seg_cols[i % len(seg_cols)]) for i in range(len(segs))]
    ax.legend(handles, segs, frameon=False, fontsize=8.3, ncol=min(len(segs), 4),
              loc="lower center", bbox_to_anchor=(0.5, -0.16), handlelength=1.1)
    return fig


def _cmap_warm():
    # 4-stop tu nhat den day: hai diem dau la tint(GOLD) o hai muc do dam khac
    # nhau (khong phai hex kem/nau am rieng), roi toi GOLD nguyen ban, roi TEAL.
    return LinearSegmentedColormap.from_list(
        "eir_seq", [tint(GOLD, 0.06), tint(GOLD, 0.35), GOLD, TEAL])


def c_sensitivity_grid(p, accent):
    """Lưới độ nhạy hai biến, giá trị đầu ra theo hai giả định.

    Trả lời: "Kết quả đổi bao nhiêu khi hai giả định then chốt cùng đổi, và vùng nào
    đưa kết quả qua ngưỡng?"

    Dữ liệu cần: rows, cols là hai trục giả định, values là ma trận kết quả, base là
    ô kịch bản cơ sở. Tuỳ chọn diverging khi thang màu cần hai chiều quanh một mốc.

    KHÔNG dùng khi hai biến không độc lập với nhau, vì lưới ngầm khẳng định mọi tổ
    hợp đều xảy ra được, kể cả tổ hợp mâu thuẫn về kinh tế.
    """
    rows = p["rows"]; cols = p["cols"]; vals = np.array(p["values"], float)
    fig, ax = eir_fig(_meta(p, accent), figsize=(7.6, max(3.0, 0.5 * len(rows) + 2.4)),
                      rect=(0.14, 0.13, 0.80, 0.60))
    ax.set_facecolor(PAPER); diverge = p.get("diverging", False)
    if diverge:
        norm = Normalize(vals.min(), vals.max())
        cmap = LinearSegmentedColormap.from_list("eir_div", [BRICK, PAPER, TEAL])
    else:
        norm = Normalize(vals.min(), vals.max()); cmap = _cmap_warm()
    # Ve tung o bang Rectangle chu KHONG dung imshow. `imshow` xuat ra mot anh BITMAP
    # nhung trong SVG, va do la thu luat cung cua repo cam: ban in phai la vector, gate
    # RASTER dem `/Subtype /Image` phai bang 0. Da do bang so: ban imshow cho ra mot anh
    # 1216x511 trong PDF, ban Rectangle cho ra 0.
    for _i in range(vals.shape[0]):
        for _j in range(vals.shape[1]):
            ax.add_patch(Rectangle(
                (_j - 0.5, _i - 0.5), 1, 1,
                facecolor=cmap(norm(vals[_i, _j])), edgecolor="none", zorder=0,
            ))
    ax.set_xlim(-0.5, vals.shape[1] - 0.5)
    ax.set_ylim(vals.shape[0] - 0.5, -0.5)   # dao truc y de hang dau nam tren, nhu imshow
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=8.6, color=INK)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels(rows, fontsize=8.6, color=INK)
    ax.set_xlabel(p.get("col_label", ""), fontsize=9.5, color=NAVY, fontweight="bold")
    ax.set_ylabel(p.get("row_label", ""), fontsize=9.5, color=NAVY, fontweight="bold")
    ax.xaxis.set_label_position("top"); ax.xaxis.tick_top()
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    lo, hi = vals.min(), vals.max(); mid = (lo + hi) / 2
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = vals[i, j]
            ax.text(j, i, _fmt(p, v), ha="center", va="center", fontsize=8,
                    color=PAPER if (not diverge and v > mid) else INK)
    base = p.get("base")
    if base:
        ri, ci = base
        ax.add_patch(Rectangle((ci - 0.5, ri - 0.5), 1, 1, fill=False, edgecolor=NAVY,
                               linewidth=2.4, zorder=5))
    return fig


def c_cond_table(p, accent):
    """Bảng tô màu theo cột, so nhiều doanh nghiệp trên nhiều chỉ tiêu.

    Trả lời: "Trên toàn bảng, doanh nghiệp nào nổi bật ở chỉ tiêu nào?" Màu tô theo
    TỪNG CỘT nên so sánh luôn nằm trong cùng một đơn vị.

    Dữ liệu cần: columns, rows, higher_better cho biết cột nào cao là tốt, fmt_cols
    cho định dạng từng cột.

    KHÔNG dùng khi các dòng không so sánh được với nhau (khác ngành, khác quy mô kế
    toán), vì bảng tô màu biến một danh sách rời rạc thành một bảng xếp hạng giả.
    """
    columns = p["columns"]; rows = p["rows"]; ncol = len(columns); nnum = ncol - 1
    hb = p.get("higher_better", [True] * nnum); fmts = p.get("fmt_cols", ["num"] * nnum)
    fig = plt.figure(figsize=(min(9.0, 1.35 * ncol + 1.6), 0.5 * len(rows) + 2.2), facecolor=PAPER)
    draw_masthead(fig, _meta(p, accent)); draw_source(fig, _meta(p, accent))
    ax = fig.add_axes([0.03, 0.10, 0.94, 0.62]); ax.axis("off")
    numeric = np.array([[float(r[c + 1]) for c in range(nnum)] for r in rows], float)
    cell_colors = [["none"] * ncol for _ in rows]; cmap = _cmap_warm()
    for c in range(nnum):
        col = numeric[:, c]; rng = col.max() - col.min() or 1
        for r in range(len(rows)):
            t = (col[r] - col.min()) / rng
            if not hb[c]:
                t = 1 - t
            cell_colors[r][c + 1] = cmap(0.15 + 0.7 * t)
    text = [[r[0]] + [fmt_value(r[c + 1], fmts[c], p.get("currency", "$")) for c in range(nnum)]
            for r in rows]
    tbl = ax.table(cellText=text, colLabels=columns, cellColours=cell_colors, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(8.6); tbl.scale(1, 1.5)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(PAPER); cell.set_linewidth(1.2)
        if r == 0:
            cell.set_facecolor(NAVY); cell.get_text().set_color(PAPER); cell.get_text().set_fontweight("bold")
        elif c == 0:
            cell.get_text().set_ha("left"); cell.get_text().set_color(INK); cell.set_facecolor(PAPER)
        else:
            cell.get_text().set_family(MONO)
    return fig


# ==================================================================== editorial
def _delta_arrow(tone):
    return {"up": "▲", "down": "▼", "flat": "•"}.get(tone, "")


def c_kpi_strip(p, accent):
    """Dải KPI một dòng, ảnh chụp nhanh vài chỉ số.

    Trả lời: "Trong một dòng, tình hình đang thế nào?" Dùng mở đầu một trang hoặc
    đóng một mục, không dùng thay cho phân tích.

    Dữ liệu cần: items dạng {label, value, delta}.

    KHÔNG dùng quá sáu chỉ số, và không dùng khi các chỉ số cần so trực tiếp với nhau
    theo hàng (dùng cond_table).
    """
    items = p["items"]; n = len(items)
    fig = plt.figure(figsize=(min(9.5, 2.0 * n + 1.0), 2.7), facecolor=PAPER)
    m = _meta(p, accent)
    if any(m.get(k) for k in ("title", "kicker", "subtitle")):
        draw_masthead(fig, m, top=0.94); y0, yh = 0.12, 0.42
    else:
        y0, yh = 0.16, 0.62
    draw_source(fig, m); setup_fonts()
    for i, it in enumerate(items):
        x = 0.045 + i * (0.91 / n); w = 0.91 / n
        if i > 0:
            fig.add_artist(mlines.Line2D([x - 0.006, x - 0.006], [y0, y0 + yh], color=GRID,
                           lw=0.9, transform=fig.transFigure))
        fig.text(x + 0.01, y0 + yh, it.get("label", "").upper(), fontsize=8, color=MUTED,
                 family=SANS, ha="left", va="top", fontweight="bold")
        fig.text(x + 0.01, y0 + yh - 0.14, str(it.get("value", "")), fontsize=21, color=NAVY,
                 family=MONO, ha="left", va="top", fontweight="bold")
        d = it.get("delta")
        if d:
            tone = it.get("tone", "flat")
            fig.text(x + 0.01, y0 + 0.02, f"{_delta_arrow(tone)} {d}", fontsize=9.5,
                     color=tone_color(tone, accent), family=MONO, ha="left", va="bottom", fontweight="bold")
    return fig


def c_hero_stat(p, accent):
    """Một con số lớn, đặt giữa trang.

    Trả lời: "Nếu người đọc chỉ nhớ một con số của mục này thì đó là số nào?" Cỡ chữ
    lớn là cách nói rằng số này quan trọng hơn mọi số khác quanh nó.

    Dữ liệu cần: label, value, cộng tuỳ chọn delta, context, tone.

    KHÔNG dùng quá một lần mỗi mục, vì hai con số cùng cỡ lớn thì không con nào lớn
    nữa.
    """
    fig = plt.figure(figsize=(7.4, 3.0), facecolor=PAPER)
    m = _meta(p, accent); draw_masthead(fig, m, top=0.94); draw_source(fig, m); setup_fonts()
    fig.text(0.045, 0.46, str(p["value"]), fontsize=52, color=accent, family=MONO,
             fontweight="bold", ha="left", va="center")
    fig.text(0.50, 0.60, p.get("label", "").upper(), fontsize=10, color=MUTED, family=SANS,
             fontweight="bold", ha="left", va="center")
    if p.get("delta"):
        tone = p.get("tone", "flat")
        fig.text(0.50, 0.46, f"{_delta_arrow(tone)} {p['delta']}", fontsize=13,
                 color=tone_color(tone, accent), family=MONO, fontweight="bold", ha="left", va="center")
    if p.get("context"):
        fig.text(0.50, 0.32, p["context"], fontsize=9.5, color=INK, family=SANS, ha="left", va="center")
    return fig


def c_exec_dashboard(p, accent):
    """Bảng điều hành một trang, gộp KPI, xu hướng và xếp hạng.

    Trả lời: "Toàn cảnh của hồ sơ này trong một trang là gì?" Dùng làm trang mở của
    báo cáo dài, để người đọc vội vẫn nắm được khung.

    Dữ liệu cần: kpis, trend, rank.

    KHÔNG dùng cho báo cáo dưới sáu trang, vì khi đó nó lặp lại đúng thứ mà chính báo
    cáo sắp nói, và không dùng làm nơi chứa mọi số không biết đặt đâu.
    """
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(11.0, 7.2), facecolor=PAPER)
    m = _meta(p, accent); m.setdefault("firm", "CFA STUDY NOTE")
    draw_masthead(fig, m, top=0.965); draw_source(fig, m)
    gs = GridSpec(3, 4, figure=fig, left=0.06, right=0.955, top=0.72, bottom=0.11,
                  height_ratios=[0.8, 1.7, 1.4], hspace=0.55, wspace=0.42)
    cols = palette(accent)
    for i, it in enumerate(p.get("kpis", [])[:4]):
        ax = fig.add_subplot(gs[0, i]); ax.axis("off")
        ax.text(0, 1.0, it.get("label", "").upper(), fontsize=8, color=MUTED, family=SANS,
                fontweight="bold", va="top", transform=ax.transAxes)
        ax.text(0, 0.55, str(it.get("value", "")), fontsize=18, color=NAVY, family=MONO,
                fontweight="bold", va="center", transform=ax.transAxes)
        if it.get("delta"):
            tone = it.get("tone", "flat")
            ax.text(0, 0.06, f"{_delta_arrow(tone)} {it['delta']}", fontsize=9,
                    color=tone_color(tone, accent), family=MONO, fontweight="bold",
                    va="bottom", transform=ax.transAxes)
        if i > 0:
            ax.axvline(-0.08, color=GRID, lw=0.9)
    tr = p.get("trend")
    if tr:
        ax = fig.add_subplot(gs[1, 0:3]); despine(ax, keep=("left", "bottom"))
        x = tr["x"]; numeric = all(isinstance(v, (int, float)) for v in x)
        xs = np.array(x, float) if numeric else np.arange(len(x))
        for i, s in enumerate(tr["series"]):
            ax.plot(xs, s["values"], color=cols[i % len(cols)], lw=2.2)
            ax.annotate(f" {s.get('name','')}", (xs[-1], s["values"][-1]), color=cols[i % len(cols)],
                        fontsize=8.5, va="center", fontweight="bold")
        if not numeric:
            ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=8)
        ax.set_title(tr.get("title", ""), fontsize=9.5, color=NAVY, loc="left",
                     fontweight="bold", family=SANS); ax.tick_params(labelsize=8)
    rk = p.get("rank")
    if rk:
        ax = fig.add_subplot(gs[1, 3]); despine(ax, keep=("bottom",), grid_axis="x")
        cats = rk["categories"]; vals = list(map(float, rk["values"]))
        order = sorted(range(len(cats)), key=lambda i: vals[i])
        cats = [cats[i] for i in order]; vals = [vals[i] for i in order]; yy = np.arange(len(cats))
        ax.barh(yy, vals, color=accent, height=0.6)
        ax.set_yticks(yy); ax.set_yticklabels(cats, fontsize=7.6)
        ax.set_title(rk.get("title", ""), fontsize=9.5, color=NAVY, loc="left",
                     fontweight="bold", family=SANS); ax.tick_params(labelsize=7.6)
        for yi, v in zip(yy, vals):
            ax.annotate(" " + fmt_value(v, rk.get("fmt", "num")), (v, yi), va="center",
                        fontsize=7.4, color=INK)
    for span, key in [((2, slice(0, 2)), "panel_left"), ((2, slice(2, 4)), "panel_right")]:
        pan = p.get(key)
        if pan:
            _mini_panel(fig.add_subplot(gs[span[0], span[1]]), pan, accent, cols)
    return fig


def _mini_panel(ax, pan, accent, cols):
    kind = pan.get("kind", "bars")
    ax.set_title(pan.get("title", ""), fontsize=9.5, color=NAVY, loc="left",
                 fontweight="bold", family=SANS)
    if kind == "bars":
        despine(ax, keep=("left", "bottom"))
        cats = pan["categories"]; vals = list(map(float, pan["values"])); x = np.arange(len(cats))
        ax.bar(x, vals, 0.6, color=accent); ax.set_xticks(x)
        ax.set_xticklabels(cats, fontsize=7.6); ax.tick_params(labelsize=7.6)
        for xi, v in zip(x, vals):
            ax.annotate(fmt_value(v, pan.get("fmt", "num")), (xi, v), ha="center", va="bottom",
                        fontsize=7.2, color=INK)
    elif kind == "diverging":
        despine(ax, keep=("bottom",), grid_axis="x")
        cats = pan["categories"]; vals = list(map(float, pan["values"]))
        order = sorted(range(len(cats)), key=lambda i: vals[i])
        cats = [cats[i] for i in order]; vals = [vals[i] for i in order]; yy = np.arange(len(cats))
        ax.barh(yy, vals, color=[TEAL if v >= 0 else BRICK for v in vals], height=0.6)
        ax.axvline(0, color=INK, lw=0.9); ax.set_yticks(yy)
        ax.set_yticklabels(cats, fontsize=7.6); ax.tick_params(labelsize=7.6)
    elif kind == "dumbbell":
        despine(ax, keep=("bottom",), grid_axis="x")
        cats = pan["categories"]; a = list(map(float, pan["before"])); b = list(map(float, pan["after"]))
        yy = np.arange(len(cats))
        for yi, av, bv in zip(yy, a, b):
            ax.hlines(yi, min(av, bv), max(av, bv), color=FAINT, lw=2)
        ax.scatter(a, yy, s=45, color=MUTED, zorder=3); ax.scatter(b, yy, s=45, color=accent, zorder=3)
        ax.set_yticks(yy); ax.set_yticklabels(cats, fontsize=7.6); ax.tick_params(labelsize=7.6)
    elif kind == "donut":
        vals = pan["values"]; labels = pan.get("labels", [])
        w, _ = ax.pie(vals, startangle=90, counterclock=False,
                      colors=[cols[i % len(cols)] for i in range(len(vals))],
                      wedgeprops={"width": 0.42, "edgecolor": PAPER, "linewidth": 1.5})
        tot = sum(vals)
        for wi, lab, v in zip(w, labels, vals):
            ang = np.deg2rad((wi.theta1 + wi.theta2) / 2)
            ax.annotate(f"{lab} {100*v/tot:.0f}%", (0.85 * np.cos(ang), 0.85 * np.sin(ang)),
                        ha="center", va="center", fontsize=7, color=INK)


COMPONENTS = {
    "dumbbell": c_dumbbell, "lollipop": c_lollipop, "diverging_bar": c_diverging_bar,
    "range_dot": c_range_dot, "bump": c_bump, "fan": c_fan, "spread": c_spread,
    "index100": c_index100, "connected_scatter": c_connected_scatter, "boxplot": c_boxplot,
    "lorenz": c_lorenz, "bullet": c_bullet, "football_field": c_football_field,
    "maturity_ladder": c_maturity_ladder, "comps_scatter": c_comps_scatter,
    "marimekko": c_marimekko, "sensitivity_grid": c_sensitivity_grid, "cond_table": c_cond_table,
    "kpi_strip": c_kpi_strip, "hero_stat": c_hero_stat, "exec_dashboard": c_exec_dashboard,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--out-dir")
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR components:", ", ".join(sorted(COMPONENTS))); return 0
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
            sys.stderr.write(f"WARN unknown EIR component '{comp}' (id={fid})\n"); fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(args.out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
