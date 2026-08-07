#!/usr/bin/env python3
"""viz_eir_stats.py, Editorial Institutional Research *statistics & markets* components
for CFA study notes. Extends viz_eir.py with 7 quant/technical archetypes.

Static matplotlib PNGs (Agg) that embed into the note .docx like the existing figures.
Same design language (FT / Bloomberg / Goldman / Morningstar / Economist), same editorial
chrome (kicker / serif headline / subtitle / source line), same spec.json contract as the
core note-pipeline-viz renderer, so a note may mix core + EIR + EIR-stats in one spec.

Editorial meta keys live inside params: title, kicker, subtitle, source, asof, rating,
firm. They render as furniture; data keys drive the plot.

Components (COMPONENTS keys):
  correlation_matrix · distribution · tornado · spc_control_chart · seasonality ·
  candlestick · spread_ladder

Usage:
  python3 viz_eir_stats.py --out-dir OUT [--only NAME] [--dpi 170]   # showcase render
  python3 viz_eir_stats.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_eir_stats.py --list
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
    draw_masthead, draw_source, save, _badge, tint, shade,
)
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.collections import LineCollection

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved


# --------------------------------------------------------- shared helpers (verbatim
# from viz_eir.py so a spec routed here behaves identically) -----------------------
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
    elif yf == "bps":
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g} bps"))


# ---- local helpers specific to this module --------------------------------------
def _legend_row(fig, entries, y=0.085, x0=0.045):
    """Bottom legend row (swatch/line + label), the FT/Bloomberg tell. entries =
    list of (kind, color, label): kind in {'sq','line','dash'}."""
    setup_fonts()
    x = x0
    for kind, color, label in entries:
        if kind == "sq":
            fig.add_artist(Rectangle((x, y - 0.006), 0.016, 0.02, transform=fig.transFigure,
                                     facecolor=color, edgecolor="none", zorder=5))
            tx = x + 0.024
        elif kind == "dash":
            fig.add_artist(mlines.Line2D([x, x + 0.028], [y + 0.004, y + 0.004],
                                         transform=fig.transFigure, color=color, lw=2.4,
                                         ls=(0, (4, 3)), zorder=5))
            tx = x + 0.036
        else:  # line
            fig.add_artist(mlines.Line2D([x, x + 0.028], [y + 0.004, y + 0.004],
                                         transform=fig.transFigure, color=color, lw=2.6,
                                         zorder=5))
            tx = x + 0.036
        t = fig.text(tx, y + 0.004, label, transform=fig.transFigure, fontsize=8.4,
                     color=INK, family=SANS, ha="left", va="center")
        # advance x by an estimate of rendered width (chars * per-char in fig fraction)
        x = tx + 0.0092 * len(label) + 0.028
    return y


def _smooth(x, y, k=14):
    """Catmull-Rom spline resample (numpy-only; scipy not available in sandbox).
    Returns densified (xs, ys) passing through every control point."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    if n < 3:
        return x, y
    xs, ys = [], []
    xp = np.concatenate(([x[0]], x, [x[-1]]))
    yp = np.concatenate(([y[0]], y, [y[-1]]))
    for i in range(1, n):
        p0, p1, p2, p3 = (np.array([xp[i - 1 + d], yp[i - 1 + d]]) for d in range(4))
        t = np.linspace(0, 1, k, endpoint=(i == n - 1))
        for tt in t:
            a = 0.5 * ((2 * p1) + (-p0 + p2) * tt +
                       (2 * p0 - 5 * p1 + 4 * p2 - p3) * tt ** 2 +
                       (-p0 + 3 * p1 - 3 * p2 + p3) * tt ** 3)
            xs.append(a[0]); ys.append(a[1])
    return np.array(xs), np.array(ys)


# ================================================================ 1. correlation
def c_correlation_matrix(p, accent):
    """Ma trận tương quan, quan hệ từng cặp trong một rổ.

    Trả lời: "Cặp nào đi cùng nhau, cặp nào ngược nhau, và rổ này thật sự phân tán
    hay chỉ phân tán trên danh nghĩa?"

    Dữ liệu cần: labels, values là ma trận vuông đối xứng. Tuỳ chọn short_labels cho
    nhãn trục khi tên dài.

    KHÔNG dùng khi cửa sổ tính tương quan ngắn hơn khoảng ba mươi quan sát, vì hệ số
    khi đó dao động mạnh tới mức bảng đổi màu chỉ vì đổi kỳ tính. Và nhớ rằng tương
    quan trong giai đoạn bình thường không nói gì về tương quan lúc thị trường vỡ, là
    đúng lúc người đọc cần nó nhất.
    """
    labels = list(p["labels"]); n = len(labels)
    raw = np.array(p["values"], float)
    # accept full matrix or lower-tri (fill symmetric); force diagonal = 1.0
    M = np.array(raw, float)
    if M.shape != (n, n):
        raise ValueError("values must be n x n")
    for i in range(n):
        for j in range(i + 1, n):
            if np.isnan(M[i, j]) or M[i, j] == 0 and M[j, i] != 0:
                M[i, j] = M[j, i]
    np.fill_diagonal(M, 1.0)
    short = p.get("short_labels", labels)

    fig, ax = eir_fig(_meta(p, accent), figsize=(7.8, 7.4),
                      rect=(0.235, 0.175, 0.735, 0.50))
    ax.set_facecolor(PAPER)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    # 5-stop diverging: am(BRICK) -> tint(BRICK) -> trung tam trung tinh(PAPER)
    # -> tint(TEAL) -> duong(TEAL). Ca 5 diem deu dan xuat tu token that.
    cmap = LinearSegmentedColormap.from_list(
        "eir_corr", [BRICK, tint(BRICK, 0.32), PAPER, tint(TEAL, 0.28), TEAL])
    norm = Normalize(-1, 1)
    diag_fc = GRID  # xam lanh trung tinh cho o tu tuong quan tren duong cheo

    for i in range(n):
        for j in range(n):
            if j > i:
                continue  # mask upper triangle, never draw it
            v = M[i, j]
            if i == j:
                fc = diag_fc; txt_col = NAVY
            else:
                fc = cmap(norm(v))
                txt_col = PAPER if abs(v) >= 0.55 else INK
            ax.add_patch(Rectangle((j - 0.47, (n - 1 - i) - 0.47), 0.94, 0.94,
                                   facecolor=fc, edgecolor=PAPER, linewidth=2.2, zorder=2))
            ax.text(j, (n - 1 - i), _cfmt(v), ha="center", va="center", fontsize=10.5,
                    family=MONO, color=txt_col, fontweight="bold" if i == j else "normal",
                    zorder=3)
    ax.set_xlim(-0.6, n - 0.4); ax.set_ylim(-0.6, n - 0.4)
    ax.set_aspect("equal")
    # column labels along the top (rotated), row labels on the left
    ax.set_xticks(range(n))
    ax.xaxis.set_ticks_position("top")
    ax.set_xticklabels(short, fontsize=9, color=MUTED, rotation=32, ha="left",
                       rotation_mode="anchor")
    ax.set_yticks([n - 1 - i for i in range(n)])
    ax.set_yticklabels(labels, fontsize=9.2, color=INK)

    # small diverging legend strip under the matrix
    cax = fig.add_axes([0.235, 0.135, 0.30, 0.018])
    # Thanh chu giai ve bang 200 dai mong chu KHONG dung imshow: imshow nhung mot anh
    # bitmap vao SVG, va gate RASTER cua repo doi 0 anh trong ban PDF giao di.
    _canh = np.linspace(-1, 1, 201)
    for _k in range(len(_canh) - 1):
        cax.axvspan(_canh[_k], _canh[_k + 1],
                    color=cmap(norm((_canh[_k] + _canh[_k + 1]) / 2)), linewidth=0)
    cax.set_xlim(-1, 1); cax.set_ylim(0, 1)
    cax.set_yticks([]); cax.set_xticks([-1, 0, 1])
    cax.set_xticklabels([_cfmt(-1.0), _cfmt(0.0), _cfmt(1.0)], fontsize=7.6, color=MUTED,
                        family=MONO)
    cax.tick_params(length=0)
    for sp in cax.spines.values():
        sp.set_color(GRID); sp.set_linewidth(0.6)
    fig.text(0.235, 0.163, "Tương quan âm", fontsize=7.8, color=BRICK, style="italic",
             family=SANS, ha="left")
    fig.text(0.535, 0.163, "Tương quan dương", fontsize=7.8, color=TEAL, style="italic",
             family=SANS, ha="right")

    _legend_row(fig, [("sq", TEAL, "Tương quan dương (cùng chiều)"),
                      ("sq", BRICK, "Tương quan âm (ngược chiều)"),
                      ("sq", diag_fc, "Đường chéo: tự tương quan (1,00)")], y=0.065)
    return fig


def _cfmt(v):
    """Correlation coefficient in Vietnamese comma-decimal, 2 dp, signed."""
    s = f"{v:.2f}".replace(".", ",")
    return s


# ================================================================ 2. distribution
def c_distribution(p, accent):
    """Phân phối một chuỗi, kèm trung bình, độ lệch chuẩn và ngưỡng đuôi.

    Trả lời: "Chuỗi này phân bố ra sao, đuôi trái dày cỡ nào, và ngưỡng tổn thất nằm
    ở đâu?"

    Dữ liệu cần: data là chuỗi quan sát thật, cộng x_label. Tuỳ chọn mean, sd,
    var_pct để vẽ vạch ngưỡng.

    KHÔNG dùng khi mẫu quá ngắn để hình dạng có nghĩa, và đừng vẽ vạch độ lệch chuẩn
    lên một phân phối lệch rõ, vì độ lệch chuẩn khi đó mô tả sai chính cái đuôi mà
    người đọc đang quan tâm.
    """
    mean = float(p.get("mean", 0.0)); sd = float(p.get("sd", 1.0))
    var_pct = float(p.get("var_pct", 0.05))
    yf = p.get("y_format", "pct")

    data = p.get("data")
    if data:  # KDE via gaussian sum (numpy only)
        d = np.array(data, float)
        lo, hi = d.min() - 3 * d.std(), d.max() + 3 * d.std()
        xs = np.linspace(lo, hi, 600)
        bw = 1.06 * d.std() * len(d) ** (-1 / 5.0)
        pdf = np.mean([np.exp(-0.5 * ((xs - v) / bw) ** 2) for v in d], axis=0)
        pdf /= (bw * np.sqrt(2 * np.pi))
        mean = float(d.mean())
        # empirical VaR quantile
        var_x = float(np.quantile(d, var_pct))
        cvar_x = float(d[d <= var_x].mean()) if np.any(d <= var_x) else var_x
    else:
        xs = np.linspace(mean - 4 * sd, mean + 4 * sd, 600)
        pdf = np.exp(-0.5 * ((xs - mean) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        # normal quantile via inverse-erf (numpy only, no scipy)
        z = _norm_ppf(var_pct)
        var_x = mean + z * sd
        # CVaR of a normal: mean - sd * phi(z)/alpha
        phi = np.exp(-0.5 * z ** 2) / np.sqrt(2 * np.pi)
        cvar_x = mean - sd * (phi / var_pct)

    fig, ax = eir_fig(_meta(p, accent), figsize=(8.0, 5.0),
                      rect=(0.075, 0.185, 0.885, 0.55))
    despine(ax, keep=("bottom",), grid_axis="")
    ax.set_yticks([])

    # full pdf faint fill
    ax.fill_between(xs, pdf, color=GRID, alpha=0.9, lw=0, zorder=1)
    # left VaR tail (light brick), CVaR sub-tail (darker brick)
    ax.fill_between(xs, pdf, where=(xs <= var_x), color=BRICK, alpha=0.14, lw=0, zorder=2)
    ax.fill_between(xs, pdf, where=(xs <= cvar_x), color=BRICK, alpha=0.30, lw=0, zorder=2)
    ax.plot(xs, pdf, color=NAVY, lw=2.4, zorder=4)

    ymax = pdf.max()
    ax.set_ylim(0, ymax * 1.30)
    # mean line (gold dotted)
    ax.axvline(mean, color=GOLD, ls=":", lw=1.8, zorder=3)
    ax.annotate(f"Trung bình {_pf(mean, yf, p)}", (mean, ymax * 1.15), color=GOLD,
                fontsize=9.5, ha="left", va="bottom", style="italic", family=SANS,
                fontweight="bold", xytext=(5, 0), textcoords="offset points")
    # VaR & CVaR threshold lines
    a = f"{100*(1-var_pct):.0f}%"
    # CVaR = duoi rui ro cuc doan hon VaR nen dung ban DAM hon cua BRICK (shade),
    # khong phai mot hex mau-do-tham rieng khong lien quan toi token.
    cvar_col = shade(BRICK, 0.45)
    for xv, lab, val, col, ylab, side, dx in [
            (cvar_x, f"CVaR {a}", cvar_x, cvar_col, ymax * 1.02, "right", -5),
            (var_x, f"VaR {a}", var_x, BRICK, ymax * 0.80, "left", 5)]:
        ax.axvline(xv, color=col, ls=(0, (5, 2)), lw=1.6, zorder=3)
        ax.plot([xv], [0], marker="o", ms=6, color=col, zorder=5)
        ax.annotate(f"{lab}\n{_pf(val, yf, p)}", (xv, ylab), color=col,
                    fontsize=9.2, ha=side, va="top", fontweight="bold", family=SANS,
                    xytext=(dx, 0), textcoords="offset points")
    _axis_fmt(ax, p, "x")
    ax.set_xlabel(p.get("x_label", "Lợi suất danh mục (năm)"), fontsize=9.5, color=INK)

    _legend_row(fig, [
        ("line", NAVY, "Mật độ lợi suất"),
        # swatch dai dien dung boi mau: khop voi alpha=0.30 cua fill CVaR ben tren.
        ("sq", tint(BRICK, 0.30), "Vùng đuôi tổn thất"),
        ("dash", BRICK, f"VaR {100*(1-var_pct):.0f}% (ngưỡng)"),
        ("dash", cvar_col, f"CVaR {100*(1-var_pct):.0f}% (đuôi)")], y=0.075)
    return fig


def _norm_ppf(q):
    """Inverse standard-normal CDF (Acklam's rational approximation; numpy only)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if q < plow:
        r = np.sqrt(-2 * np.log(q))
        return (((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / \
               ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    if q > phigh:
        r = np.sqrt(-2 * np.log(1 - q))
        return -(((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / \
                ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    r = q - 0.5; s = r * r
    return (((((a[0]*s+a[1])*s+a[2])*s+a[3])*s+a[4])*s+a[5])*r / \
           (((((b[0]*s+b[1])*s+b[2])*s+b[3])*s+b[4])*s+1)


def _pf(v, yf, p):
    """format a distribution x-value by y_format (default percent, 1dp)."""
    if yf == "pct":
        return f"{v:,.1f}%"
    if yf == "cur":
        return fmt_value(v, "cur", p.get("currency", "$"))
    return fmt_value(v, yf, p.get("currency", "$"), p.get("dp"))


# ==================================================================== 3. tornado
def c_tornado(p, accent):
    """Tornado, biến nào lay chuyển kết quả mạnh nhất.

    Trả lời: "Trong các giả định, biến nào đáng tranh luận nhất?" Xếp theo biên độ
    giảm dần nên biến quan trọng nhất luôn nằm trên cùng.

    Dữ liệu cần: rows dạng {variable, low, high}, base là kết quả kịch bản cơ sở,
    cộng base_label, low_name, high_name, x_label.

    KHÔNG dùng khi khoảng thay đổi của mỗi biến không được chọn nhất quán, vì khi đó
    thứ tự thanh chỉ phản ánh việc ai nới khoảng rộng hơn chứ không phản ánh độ nhạy
    thật.
    """
    base = float(p["base"]); rows = p["rows"]
    # sort by |high - low| descending → biggest swing on top
    rows = sorted(rows, key=lambda r: abs(float(r["high"]) - float(r["low"])),
                  reverse=True)
    n = len(rows)
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.0, max(3.4, 0.62 * n + 2.4)),
                      rect=(0.32, 0.20, 0.61, 0.50))
    despine(ax, keep=("bottom",), grid_axis="x")
    y = np.arange(n)[::-1]  # first row at top

    for yi, r in zip(y, rows):
        lo = float(r["low"]); hi = float(r["high"])
        left = min(lo, hi); right = max(lo, hi)
        # brick side = below base, teal side = above base
        ax.barh(yi, base - left, left=left, height=0.56, color=BRICK, zorder=2)
        ax.barh(yi, right - base, left=base, height=0.56, color=TEAL, zorder=2)
        lo_col = BRICK if lo <= base else TEAL
        hi_col = TEAL if hi >= base else BRICK
        ax.annotate(_fmt(p, lo), (left, yi), va="center", ha="right", fontsize=9.2,
                    color=lo_col, fontweight="bold", xytext=(-6, 0),
                    textcoords="offset points")
        ax.annotate(_fmt(p, hi), (right, yi), va="center", ha="left", fontsize=9.2,
                    color=hi_col, fontweight="bold", xytext=(6, 0),
                    textcoords="offset points")

    ax.set_yticks(y); ax.set_yticklabels([r["label"] for r in rows], fontsize=9.4,
                                         color=INK)
    ax.set_ylim(-0.6, n - 0.2)
    # base line + top label
    ax.axvline(base, color=GOLD, lw=1.8, zorder=4)
    ax.plot([base], [n - 0.62], marker="o", ms=6, color=GOLD, zorder=5, clip_on=False)
    ax.annotate(f"{p.get('base_label', 'Giá trị cơ sở')} {_fmt(p, base)}",
                (base, n - 0.55), color=GOLD, fontsize=9.2, fontweight="bold",
                ha="center", va="bottom", family=SANS, annotation_clip=False)
    span = (max(float(r["high"]) for r in rows) - min(float(r["low"]) for r in rows))
    ax.set_xlim(min(float(r["low"]) for r in rows) - span * 0.16,
                max(float(r["high"]) for r in rows) + span * 0.12)
    _axis_fmt(ax, p, "x")
    if p.get("x_label"):
        ax.set_xlabel(p["x_label"], fontsize=9.5, color=INK)

    _legend_row(fig, [("sq", BRICK, p.get("low_name", "Kịch bản bất lợi (giá trị thấp)")),
                      ("sq", TEAL, p.get("high_name", "Kịch bản thuận lợi (giá trị cao)")),
                      ("line", GOLD, p.get("base_label", "Giá trị cơ sở"))], y=0.075)
    return fig


# =========================================================== 4. spc_control_chart
def c_spc_control_chart(p, accent):
    """Biểu đồ kiểm soát, chuỗi so với dải kiểm soát.

    Trả lời: "Biến động này nằm trong dao động thường lệ hay đã vượt ngưỡng?" Ba
    đường tâm, trên và dưới biến câu hỏi cảm tính thành một phép so ngưỡng.

    Dữ liệu cần: x, values, center, ucl, lcl cộng các nhãn tương ứng.

    KHÔNG dùng khi ngưỡng được đặt sau khi đã nhìn dữ liệu, vì khi đó mọi điểm vượt
    ngưỡng đều là điều hiển nhiên chứ không phải phát hiện.
    """
    x = p["x"]; vals = np.array(p["values"], float)
    numeric = all(isinstance(v, (int, float)) for v in x)
    xs = np.array(x, float) if numeric else np.arange(len(x))
    center = float(p["center"]) if p.get("center") is not None else float(vals.mean())
    if p.get("ucl") is not None and p.get("lcl") is not None:
        ucl = float(p["ucl"]); lcl = float(p["lcl"])
    else:
        sd = float(vals.std(ddof=1)); ucl = center + 3 * sd; lcl = center - 3 * sd
    line_col = accent if accent not in (TEAL,) else INDIGO  # SPC monitored series = indigo/navy-blue

    fig, ax = eir_fig(_meta(p, accent), figsize=(8.2, 5.0),
                      rect=(0.085, 0.185, 0.80, 0.52))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    # faint in-control band
    ax.axhspan(lcl, ucl, color=GRID, alpha=0.7, zorder=0)
    # centerline + control limits
    ax.axhline(center, color=line_col, lw=1.6, zorder=2)
    ax.axhline(ucl, color=GOLD, ls=(0, (5, 3)), lw=1.6, zorder=2)
    ax.axhline(lcl, color=GOLD, ls=(0, (5, 3)), lw=1.6, zorder=2)
    # series
    ax.plot(xs, vals, color=line_col, lw=2.0, zorder=3)
    ooc = (vals > ucl) | (vals < lcl)
    ax.scatter(xs[~ooc], vals[~ooc], s=42, color=line_col, zorder=4,
               edgecolor=PAPER, linewidth=1.0)
    ax.scatter(xs[ooc], vals[ooc], s=70, color=BRICK, zorder=5,
               edgecolor=PAPER, linewidth=1.2)
    for xi, vi in zip(xs[ooc], vals[ooc]):
        ax.annotate(_fmt(p, vi), (xi, vi), color=BRICK, fontsize=9.2, fontweight="bold",
                    ha="center", va="bottom" if vi > center else "top",
                    xytext=(0, 8 if vi > center else -8), textcoords="offset points")

    # right-edge labels for the three reference lines
    xr = xs[-1] + (xs[-1] - xs[0]) * 0.015
    for yv, lab in [(ucl, p.get("ucl_label", "Giới hạn trên")),
                    (center, p.get("center_label", "Mục tiêu")),
                    (lcl, p.get("lcl_label", "Giới hạn dưới"))]:
        col = line_col if yv == center else GOLD
        ax.annotate(f"{lab}\n{_fmt(p, yv)}", (xr, yv), color=col, fontsize=8.6,
                    va="center", ha="left", style="italic", family=SANS, fontweight="bold",
                    annotation_clip=False, xytext=(2, 0), textcoords="offset points")

    # headroom above the highest point so the note + peak label never collide
    ytop = max(ucl, float(vals.max()))
    ybot = min(lcl, float(vals.min()))
    yr = ytop - ybot
    ax.set_ylim(ybot - yr * 0.10, ytop + yr * 0.24)
    nooc = int(ooc.sum())
    if nooc:
        ax.annotate(p.get("note", f"Có {nooc} kỳ vượt giới hạn kiểm soát (ngoài tầm kiểm soát)."),
                    (0.015, 0.985), xycoords="axes fraction", fontsize=8.6, color=GOLD,
                    style="italic", family=SANS, ha="left", va="top")
    if not numeric:
        ax.set_xticks(xs); ax.set_xticklabels(x, fontsize=8.8, color=INK)
    ax.set_xlim(xs[0] - 0.4, xs[-1] + 0.4)
    _axis_fmt(ax, p, "y")
    if p.get("x_label"):
        ax.set_xlabel(p["x_label"], fontsize=9.5, color=INK)

    _legend_row(fig, [("line", line_col, p.get("series_name", "Chuỗi theo dõi")),
                      ("line", line_col, p.get("center_label", "Đường tâm (centerline)")),
                      ("dash", GOLD, "Giới hạn kiểm soát trên / dưới (UCL / LCL)"),
                      ("sq", BRICK, "Kỳ ngoài tầm kiểm soát")], y=0.075)
    return fig


# ================================================================= 5. seasonality
def c_seasonality(p, accent):
    """Hình mùa vụ, dải cao thấp theo kỳ trong năm.

    Trả lời: "Kỳ nào trong năm thường mạnh, kỳ nào thường yếu, và biên độ mùa vụ rộng
    cỡ nào?"

    Dữ liệu cần: periods, mean, hi, lo cùng đơn vị, cộng unit_label. Tuỳ chọn
    peak_label, trough_label để đặt tên đỉnh đáy.

    KHÔNG dùng khi lịch sử dưới ba chu kỳ đầy đủ, vì ba năm không đủ tách mùa vụ khỏi
    xu hướng, và hình sẽ khẳng định một quy luật lặp lại chưa hề được chứng minh.
    """
    periods = list(p["periods"]); n = len(periods)
    mean = np.array(p["mean"], float); lo = np.array(p["lo"], float)
    hi = np.array(p["hi"], float)
    x = np.arange(n)
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.2, 5.2),
                      rect=(0.095, 0.175, 0.86, 0.52))
    despine(ax, keep=("left", "bottom"), grid_axis="y")

    line_col = BRICK  # seasonal mean drawn in the warm hero colour (matches reference)
    xs_s, mean_s = _smooth(x, mean)
    _, lo_s = _smooth(x, lo)
    _, hi_s = _smooth(x, hi)
    # range band: teal-ish for the upper (toward hi), grey for lower, two soft fills
    ax.fill_between(xs_s, mean_s, hi_s, color=GOLD, alpha=0.16, lw=0, zorder=1)
    ax.fill_between(xs_s, lo_s, mean_s, color=INDIGO, alpha=0.10, lw=0, zorder=1)
    ax.plot(xs_s, hi_s, color=GOLD, lw=1.0, alpha=0.55, zorder=2)
    ax.plot(xs_s, lo_s, color=INDIGO, lw=1.0, alpha=0.45, zorder=2)
    ax.plot(xs_s, mean_s, color=line_col, lw=2.8, zorder=4)
    ax.scatter(x, mean, s=26, color=line_col, zorder=5, edgecolor=PAPER, linewidth=0.8)

    peak_i = int(np.argmax(mean)); trough_i = int(np.argmin(mean))
    ax.scatter([x[peak_i]], [mean[peak_i]], s=95, color=TEAL, zorder=6,
               edgecolor=PAPER, linewidth=1.4)
    ax.scatter([x[trough_i]], [mean[trough_i]], s=95, color=BRICK, zorder=6,
               edgecolor=PAPER, linewidth=1.4)
    ax.annotate(f"{p.get('peak_label', 'Đỉnh mùa')}\n{_fmt(p, mean[peak_i])}",
                (x[peak_i], mean[peak_i]), color=TEAL, fontsize=9.0, fontweight="bold",
                ha="left" if peak_i < n / 2 else "right", va="bottom",
                xytext=(6 if peak_i < n / 2 else -6, 8), textcoords="offset points")
    ax.annotate(f"{p.get('trough_label', 'Đáy mùa')}\n{_fmt(p, mean[trough_i])}",
                (x[trough_i], mean[trough_i]), color=BRICK, fontsize=9.0, fontweight="bold",
                ha="left" if trough_i < n / 2 else "right", va="top",
                xytext=(6 if trough_i < n / 2 else -6, -8), textcoords="offset points")

    ax.set_xticks(x); ax.set_xticklabels(periods, fontsize=8.8, color=INK)
    ax.set_xlim(-0.4, n - 0.6)
    _lo_all = min(lo.min(), lo_s.min()); _hi_all = max(hi.max(), hi_s.max())
    _rng = _hi_all - _lo_all
    ax.set_ylim(_lo_all - _rng * 0.05, _hi_all + _rng * 0.10)
    _axis_fmt(ax, p, "y")
    if p.get("unit_label"):  # unit shown top-left above the y axis (FT convention)
        ax.annotate(p["unit_label"], (0.0, 1.025), xycoords="axes fraction", fontsize=8.8,
                    color=MUTED, family=SANS, ha="left", va="bottom")

    # swatch dai dien cho dai GOLD/INDIGO alpha-blend ben tren (xem fill_between
    # o tren: GOLD alpha=0.16 nua tren, INDIGO alpha=0.10 nua duoi) - lay tint
    # cua GOLD lam dai dien vi no chiem phan lon an tuong thi giac cua dai.
    _legend_row(fig, [("line", line_col, p.get("mean_name", "Giá trị trung bình theo kỳ")),
                      ("sq", tint(GOLD, 0.18), "Khoảng dao động (thấp nhất tới cao nhất)"),
                      ("sq", TEAL, p.get("peak_label", "Đỉnh mùa")),
                      ("sq", BRICK, p.get("trough_label", "Đáy mùa"))], y=0.075)
    return fig


# ================================================================= 6. candlestick
def c_candlestick(p, accent):
    """Nến giá, mở cao thấp đóng theo từng kỳ.

    Trả lời: "Trong từng kỳ, giá đi tới đâu và đóng ở đâu so với mở?" Bóng nến giữ
    lại biên độ trong kỳ mà đường giá đóng cửa vứt mất.

    Dữ liệu cần: rows dạng {label, open, high, low, close}, cộng y_label và tên hai
    chiều tăng giảm.

    KHÔNG dùng quá khoảng sáu mươi kỳ trên một khổ giấy, vì thân nến mỏng dưới một
    điểm ảnh thì bóng và thân nhập làm một.
    """
    rows = p["rows"]; n = len(rows)
    x = np.arange(n)
    o = np.array([float(r["o"]) for r in rows]); h = np.array([float(r["h"]) for r in rows])
    l = np.array([float(r["l"]) for r in rows]); c = np.array([float(r["c"]) for r in rows])
    up = c >= o
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.4, 5.0),
                      rect=(0.085, 0.155, 0.88, 0.58))
    despine(ax, keep=("left", "bottom"), grid_axis="y")
    w = 0.6
    for xi, oi, hi_, li, ci, u in zip(x, o, h, l, c, up):
        col = TEAL if u else BRICK
        # wick: thin vline high→low
        ax.vlines(xi, li, hi_, color=col, lw=1.3, zorder=2)
        # body: bar from min(o,c) with height |c-o|
        bottom = min(oi, ci); height = abs(ci - oi)
        if height < (h.max() - l.min()) * 0.004:  # doji → hairline
            ax.hlines(oi, xi - w / 2, xi + w / 2, color=col, lw=1.6, zorder=3)
        else:
            ax.add_patch(Rectangle((xi - w / 2, bottom), w, height, facecolor=col,
                                   edgecolor=col, linewidth=0.8, zorder=3))
    ax.set_xticks(x)
    ax.set_xticklabels([r["label"] for r in rows], fontsize=8.8, color=INK)
    ax.set_xlim(-0.7, n - 0.3)
    pad = (h.max() - l.min()) * 0.08
    ax.set_ylim(l.min() - pad, h.max() + pad)
    _axis_fmt(ax, p, "y")
    if p.get("y_label"):
        ax.set_ylabel(p["y_label"], fontsize=9.5, color=INK)

    _legend_row(fig, [("sq", TEAL, p.get("up_name", "Phiên tăng (đóng ≥ mở)")),
                      ("sq", BRICK, p.get("down_name", "Phiên giảm (đóng < mở)"))],
                y=0.075)
    return fig


# =============================================================== 7. spread_ladder
def c_spread_ladder(p, accent):
    """Thang chênh lệch tín dụng theo hạng.

    Trả lời: "Chênh lệch tín dụng giãn ra bao nhiêu khi tụt một bậc xếp hạng, và bậc
    nào là bậc gãy?"

    Dữ liệu cần: ratings, spreads_bps, cộng x_label. Tuỳ chọn ref là mốc tham chiếu,
    highlight để nhấn một bậc.

    KHÔNG dùng khi các bậc lấy từ những thị trường hoặc kỳ hạn khác nhau, vì thang
    khi đó trộn hai đường cong vào một và bậc gãy hiện ra chỉ là dấu vết của việc
    trộn.
    """
    ratings = list(p["ratings"]); spreads = list(map(float, p["spreads_bps"]))
    ref = p.get("ref"); n = len(ratings)
    hl = p.get("highlight")  # e.g. "BBB" investment/speculative boundary
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.4, max(3.6, 0.56 * n + 2.4)),
                      rect=(0.135, 0.185, 0.80, 0.55))
    despine(ax, keep=("left", "bottom"), grid_axis="x")
    y = np.arange(n)[::-1]  # AAA at top
    for yi, rt, sp in zip(y, ratings, spreads):
        is_hl = (hl is not None and rt == hl)
        col = BRICK if is_hl else NAVY
        ax.barh(yi, sp, height=0.62, color=col, zorder=2,
                edgecolor="none")
        ax.annotate(f"{sp:,.0f} bps", (sp, yi), va="center", ha="left", fontsize=9.4,
                    color=col if is_hl else NAVY, fontweight="bold",
                    xytext=(7, 0), textcoords="offset points")
    ax.set_yticks(y)
    ax.set_yticklabels(ratings, fontsize=9.6, color=INK,
                       fontweight="bold")
    # bold the highlighted tick label
    if hl is not None:
        for lab in ax.get_yticklabels():
            lab.set_fontweight("bold")
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xlim(0, max(spreads) * 1.16)
    if ref is not None:
        rx = float(ref)
        ax.axvline(rx, color=GOLD, ls=(0, (5, 3)), lw=1.6, zorder=4)
        ax.annotate(f"{p.get('ref_label', 'Trung bình danh mục')} {rx:,.0f} bps",
                    (rx, n - 0.5), color=GOLD, fontsize=9.0, fontweight="bold",
                    ha="center", va="bottom", style="italic", family=SANS)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g} bps"))
    ax.set_xlabel(p.get("x_label", "Chênh lệch tín dụng so với chính phủ (bps)"),
                  fontsize=9.5, color=INK)

    entries = [("sq", NAVY, p.get("bar_name", "Hạng tín nhiệm"))]
    if hl is not None:
        entries.append(("sq", BRICK, p.get("highlight_name",
                                            "Ranh giới đầu tư / đầu cơ (BBB)")))
    if ref is not None:
        entries.append(("dash", GOLD, f"{p.get('ref_label', 'Trung bình danh mục')} "
                                      f"{float(ref):,.0f} bps"))
    _legend_row(fig, entries, y=0.075)
    return fig


COMPONENTS = {
    "correlation_matrix": c_correlation_matrix,
    "distribution": c_distribution,
    "tornado": c_tornado,
    "spc_control_chart": c_spc_control_chart,
    "seasonality": c_seasonality,
    "candlestick": c_candlestick,
    "spread_ladder": c_spread_ladder,
}


# ============================================================ built-in showcase data
_SHOWCASE = {
    "correlation_matrix": {
        "kicker": "Portfolio Management · Phân bổ tài sản",
        "title": "Ma trận tương quan lợi suất giữa năm lớp tài sản",
        "subtitle": "Hệ số tương quan lợi suất hằng tháng theo cặp lớp tài sản, giai đoạn "
                    "mười năm. Tương quan càng thấp (ô nhạt) thì lợi ích đa dạng hóa càng lớn.",
        "source": "Bloomberg, tính toán của tác giả", "asof": "T12/2025",
        "labels": ["Cổ phiếu phát triển", "Cổ phiếu mới nổi", "Trái phiếu chính phủ",
                   "Trái phiếu doanh nghiệp", "Hàng hóa"],
        "short_labels": ["CP phát triển", "CP mới nổi", "TP chính phủ", "TP doanh nghiệp",
                         "Hàng hóa"],
        "values": [
            [1.00, 0.00, 0.00, 0.00, 0.00],
            [0.74, 1.00, 0.00, 0.00, 0.00],
            [-0.18, -0.22, 1.00, 0.00, 0.00],
            [0.42, 0.38, 0.56, 1.00, 0.00],
            [0.31, 0.45, -0.09, 0.21, 1.00]],
    },
    "distribution": {
        "kicker": "Quản trị rủi ro",
        "title": "Phân phối lợi suất danh mục và giá trị chịu rủi ro (VaR)",
        "subtitle": "Lợi suất năm của danh mục giả định phân phối chuẩn với kỳ vọng 8,0% "
                    "và độ lệch chuẩn 15,0%. VaR 95% và CVaR 95% định lượng tổn thất ở đuôi trái.",
        "source": "minh họa của tác giả", "asof": "T12/2025",
        "mean": 8.0, "sd": 15.0, "var_pct": 0.05, "y_format": "pct",
        "x_label": "Lợi suất danh mục (năm)",
    },
    "tornado": {
        "kicker": "Equity · Định giá · Phân tích độ nhạy",
        "title": "Độ nhạy của giá trị nội tại theo các giả định chính",
        "subtitle": "Mỗi thanh thể hiện khoảng dao động của giá trị nội tại mỗi cổ phiếu khi "
                    "một biến đầu vào thay đổi quanh kịch bản cơ sở, các biến còn lại giữ nguyên.",
        "source": "mô hình DCF của tác giả", "asof": "T12/2025",
        "y_format": "cur", "currency": "$", "base": 58.4,
        "x_label": "Giá trị nội tại mỗi cổ phiếu (USD)",
        "rows": [
            {"label": "WACC (chi phí vốn bình quân)", "low": 41.6, "high": 78.9},
            {"label": "Tăng trưởng dài hạn", "low": 47.2, "high": 71.5},
            {"label": "Biên lợi nhuận hoạt động", "low": 50.3, "high": 67.1},
            {"label": "Vòng quay tài sản", "low": 53.8, "high": 63.0}],
    },
    "spc_control_chart": {
        "kicker": "Quản lý danh mục · Kiểm soát rủi ro chủ động",
        "title": "Theo dõi sai số (tracking error) so với giới hạn kiểm soát",
        "subtitle": "Sai số theo dõi hằng tháng của một quỹ cổ phiếu chủ động được giám sát "
                    "bằng biểu đồ kiểm soát thống kê: đường tâm 3,00%, dải kiểm soát 1,50%-4,50%.",
        "source": "báo cáo quỹ, tính toán của tác giả", "asof": "T12/2025",
        "y_format": "pct", "center": 3.0, "ucl": 4.5, "lcl": 1.5,
        "x_label": "Kỳ quan sát (16 tháng gần nhất)",
        "x": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12",
              "T13", "T14", "T15", "T16"],
        "values": [2.9, 3.1, 2.7, 3.4, 3.0, 2.6, 3.3, 4.8, 4.1, 3.6, 2.8, 3.2, 1.4, 2.5,
                   3.0, 3.7],
        "series_name": "Sai số theo dõi hằng tháng",
        "center_label": "Mục tiêu",
    },
    "seasonality": {
        "kicker": "Hàng hóa",
        "title": "Tính mùa vụ của giá khí thiên nhiên Henry Hub",
        "subtitle": "Giá khí thiên nhiên có xu hướng đạt đỉnh vào mùa đông khi nhu cầu sưởi "
                    "ấm tăng cao và chạm đáy vào cuối xuân. Vùng tô thể hiện khoảng từ thấp nhất tới cao nhất.",
        "source": "EIA, tính toán của tác giả", "asof": "2015-2025",
        "y_format": "num", "dp": 2, "unit_label": "USD/MMBtu",
        "periods": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"],
        "mean": [3.85, 3.60, 3.18, 2.74, 2.58, 2.71, 2.93, 3.02, 2.88, 3.05, 3.42, 3.78],
        "lo": [2.90, 2.75, 2.45, 2.10, 1.95, 2.05, 2.30, 2.35, 2.15, 2.40, 2.70, 2.82],
        "hi": [5.05, 4.70, 4.05, 3.55, 3.30, 3.55, 3.85, 3.88, 3.70, 4.00, 4.55, 5.00],
        "peak_label": "Đỉnh mùa", "trough_label": "Đáy mùa",
    },
    "candlestick": {
        "kicker": "Equity · Phân tích kỹ thuật",
        "title": "Biểu đồ nến giá cổ phiếu (OHLC)",
        "subtitle": "Mười hai phiên giao dịch với giá mở, đóng, cao, thấp. Nến xanh là phiên "
                    "tăng (đóng ≥ mở), nến đỏ là phiên giảm (đóng < mở).",
        "source": "HOSE, dữ liệu minh họa", "asof": "T12/2025",
        "y_format": "num", "dp": 1, "y_label": "Giá đóng cửa (nghìn VND)",
        "rows": [
            {"label": "P1", "o": 100.0, "h": 109.5, "l": 98.0, "c": 108.0},
            {"label": "P2", "o": 107.8, "h": 111.6, "l": 104.2, "c": 106.9},
            {"label": "P3", "o": 106.0, "h": 113.8, "l": 105.2, "c": 112.0},
            {"label": "P4", "o": 111.9, "h": 114.8, "l": 107.1, "c": 109.9},
            {"label": "P5", "o": 109.0, "h": 117.8, "l": 108.1, "c": 116.0},
            {"label": "P6", "o": 116.0, "h": 122.6, "l": 114.0, "c": 118.8},
            {"label": "P7", "o": 121.1, "h": 124.0, "l": 116.2, "c": 119.4},
            {"label": "P8", "o": 118.2, "h": 126.7, "l": 117.3, "c": 125.0},
            {"label": "P9", "o": 124.7, "h": 129.1, "l": 121.2, "c": 123.6},
            {"label": "P10", "o": 123.2, "h": 131.7, "l": 122.4, "c": 130.0},
            {"label": "P11", "o": 130.0, "h": 133.9, "l": 126.1, "c": 128.6},
            {"label": "P12", "o": 128.0, "h": 137.9, "l": 127.3, "c": 135.0}],
    },
    "spread_ladder": {
        "kicker": "Fixed Income · Phân tích tín dụng",
        "title": "Chênh lệch tín dụng theo hạng tín nhiệm",
        "subtitle": "Phần bù lợi suất (G-spread) so với trái phiếu chính phủ của trái phiếu "
                    "doanh nghiệp kỳ hạn 5 năm, xếp theo hạng tín nhiệm. Chênh lệch nới rộng dần "
                    "khi hạ hạng, phản ánh rủi ro vỡ nợ và thanh khoản gia tăng.",
        "source": "Bloomberg, tính toán của tác giả", "asof": "T12/2025",
        "ratings": ["AAA", "AA", "A", "BBB", "BB", "B"],
        "spreads_bps": [38, 62, 98, 165, 312, 528],
        "ref": 145, "ref_label": "Trung bình danh mục",
        "highlight": "BBB", "highlight_name": "Ranh giới đầu tư / đầu cơ (BBB)",
        "bar_name": "Hạng tín nhiệm",
    },
}


def _run_showcase(out_dir, only, dpi):
    os.makedirs(out_dir, exist_ok=True)
    ok = fail = 0
    for name, params in _SHOWCASE.items():
        if only and name != only:
            continue
        fn = COMPONENTS[name]
        try:
            accent = params.get("accent") or TEAL
            fig = fn(params, accent)
            out = os.path.join(out_dir, f"{name}.png")
            save(fig, out, dpi=dpi)
            print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL {name}: {e}\n"); fail += 1
    print(f"viz_eir_stats showcase: {ok} rendered, {fail} failed")
    return fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--out-dir",
        default="/sessions/jolly-confident-hopper/mnt/outputs/note-pipeline-viz-library/gallery/super/stats")
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=170)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR-stats components:", ", ".join(sorted(COMPONENTS))); return 0
    if not args.spec:  # showcase mode (default)
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
            sys.stderr.write(f"WARN unknown EIR-stats component '{comp}' (id={fid})\n")
            fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(args.out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir_stats: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
