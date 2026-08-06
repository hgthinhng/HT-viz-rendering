"""
viz_charts.py - StockLPT quantitative chart family (Wave 12, 2026-06).
=====================================================================

Bổ sung CHART ĐỊNH LƯỢNG THẬT (matplotlib) cho engine viz - thứ mà bộ component
inline SVG/HTML cũ không làm tốt: time-series nhiều điểm, ranking, diverging,
waterfall, scatter, grouped/stacked bar.

Nguyên tắc (theo create-viz + note-pipeline viz_render_py):
  - spines top/right bỏ, grid y rất nhạt, bar bắt đầu từ 0.
  - direct labeling thay legend khi ít series.
  - màu = thông tin: up = emerald, down = đỏ, chrome/neutral = accent (forest),
    structure = ink (violet). Nền giấy hoà vào trang.
  - title nêu INSIGHT (do caller truyền), không phải tên metric trống.
  - 200 dpi, số định dạng kiểu VN (1.234,5 / 12,3%).

Tích hợp:
  - Mỗi component là 1 function top-level -> orchestrator import động và gọi
    func(**params), nhận lại 1 chuỗi HTML <figure><img base64></figure>.
  - Tự THEME theo brand đang active: lấy palette bằng cách remap các hex nguồn
    StockLPT qua current_brand().remap -> brand nào cũng đúng màu.
  - matplotlib import LAZY trong từng function -> import module này rẻ và an toàn
    kể cả khi môi trường chưa có matplotlib (chỉ khi render chart mới cần).

Public components:
    chart_line, chart_diverging, chart_bar_h, chart_waterfall,
    chart_bar_grouped, chart_scatter
Style:
    chart_styles()  -> CSS cho <figure class="lpt-chart">
"""
from __future__ import annotations

import os
import io
import base64

_FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_MPL_FONTS_LOADED = False

# Font family names (đã ship TTF trong fonts/)
BODY = "Be Vietnam Pro"
MONO = "IBM Plex Mono"
SERIF = "Spectral"


# ============================================================
# THEME (brand-aware): remap hex nguồn StockLPT -> brand đang active
# ============================================================
def _theme() -> dict:
    try:
        from _brand import current_brand
        r = current_brand().remap
    except Exception:
        def r(s):  # no brand -> StockLPT source colors
            return s
    return {
        "paper":  r("#F4F6F9"),   # nền giấy (StockLPT -> #F4F6F9)
        "ink":    r("#2A1A4A"),   # structure (-> tím huyền #2A1A4A)
        "muted":  r("#8E87A0"),   # axis/label phụ (-> #8E87A0)
        "grid":   r("#DEE4EC"),   # lưới (-> #DEE4EC)
        "accent": r("#16633C"),   # chrome thương hiệu (-> forest #16633C)
        "up":     r("#21B36A"),   # tăng / inflow (-> emerald #21B36A)
        "down":   r("#E13453"),   # giảm / outflow (-> red #E13453)
        "slate":  r("#514B78"),   # neutral data (-> grey-violet)
    }


def _ensure_mpl():
    """Lazy import matplotlib + đăng ký font 1 lần. Trả về (plt, FuncFormatter)."""
    global _MPL_FONTS_LOADED
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import font_manager as fm
    if not _MPL_FONTS_LOADED:
        import glob
        for ttf in glob.glob(os.path.join(_FONTS_DIR, "*.ttf")):
            try:
                fm.fontManager.addfont(ttf)
            except Exception:
                pass
        _MPL_FONTS_LOADED = True
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    th = _theme()
    plt.rcParams.update({
        "font.family": BODY,
        "figure.facecolor": th["paper"],
        "axes.facecolor": th["paper"],
        "savefig.facecolor": th["paper"],
        "text.color": th["ink"],
        "axes.labelcolor": th["ink"],
        "xtick.color": th["muted"],
        "ytick.color": th["muted"],
        "axes.edgecolor": th["muted"],
        "axes.grid": False,
    })
    return plt, FuncFormatter


def _vn(v, decimals=0):
    s = f"{v:,.{decimals}f}"
    return s.replace(",", "\u00a0").replace(".", ",").replace("\u00a0", ".")


def _fmt(kind="num", currency="", suffix=""):
    def f(v, _=None):
        if kind == "pct":
            return _vn(v, 1) + "%"
        if kind == "cur":
            return f"{currency}{_vn(v, 0)}"
        return _vn(v, 0) + suffix
    return f


def _clean(ax, th, left=True, bottom=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s, on in (("left", left), ("bottom", bottom)):
        if on:
            ax.spines[s].set_color(th["muted"])
            ax.spines[s].set_linewidth(0.8)
        else:
            ax.spines[s].set_visible(False)


def _wrap(fig, plt, title=None, caption=None):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    ttl = f'<div class="lpt-chart-title">{title}</div>' if title else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="lpt-chart">{ttl}'
            f'<img src="data:image/png;base64,{b64}" />{cap}</figure>')


# ============================================================
# COMPONENTS
# ============================================================
def chart_line(series, x_labels=None, title=None, caption=None,
               markers=None, ref=None, ref_label=None, up=True,
               y_format="num", currency="", height=2.95, **_):
    """Line/time-series. series: list[float]. markers: list[[index,'nhãn','top'|'bottom']].
    ref: giá trị đường tham chiếu (vd giá mở cửa). up=True -> emerald, False -> đỏ."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    color = th["up"] if up else th["down"]
    y = list(series)
    x = list(range(len(y)))
    fig, ax = plt.subplots(figsize=(7.4, height), dpi=200)
    _clean(ax, th, bottom=bool(x_labels))
    if ref is not None:
        ax.axhline(ref, color=th["muted"], lw=0.9, ls=(0, (4, 3)), alpha=0.7, zorder=1)
        if ref_label:
            ax.text(x[-1], ref, "  " + ref_label, va="center", ha="left",
                    fontsize=7.5, color=th["muted"], fontfamily=BODY)
    ax.fill_between(x, y, min(y), color=color, alpha=0.10, zorder=1)
    ax.plot(x, y, color=color, lw=2.4, solid_capstyle="round", zorder=3)
    for mk in (markers or []):
        i, lab, va = mk[0], mk[1], (mk[2] if len(mk) > 2 else "bottom")
        ax.scatter([x[i]], [y[i]], s=34, color=th["ink"], zorder=4)
        dy = 3 if va == "bottom" else -3
        ax.annotate(lab, (x[i], y[i]), xytext=(0, dy), textcoords="offset points",
                    ha="center", va=va, fontsize=8, color=th["ink"],
                    fontfamily=MONO, fontweight="medium")
    span = (max(y) - min(y)) or 1
    ax.set_ylim(min(y) - span * 0.12, max(y) + span * 0.16)
    ax.set_xlim(-0.4, len(y) - 0.6 + (1.8 if markers else 0.4))
    if x_labels:
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, fontsize=8, fontfamily=BODY)
    else:
        ax.set_xticks([])
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt(y_format, currency)))
    for t in ax.get_yticklabels():
        t.set_fontfamily(MONO)
        t.set_fontsize(8)
    ax.grid(axis="y", color=th["grid"], lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


def chart_diverging(items, title=None, caption=None, unit="", currency="",
                    y_format="num", height=None, **_):
    """Diverging horizontal bar (vd dòng tiền ròng): items=[{'name','value'}].
    value > 0 -> emerald, < 0 -> đỏ. Tự sort tăng dần (dương trên cùng)."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    data = sorted(items, key=lambda d: d["value"])
    names = [d["name"] for d in data]
    vals = [d["value"] for d in data]
    colors = [th["up"] if v >= 0 else th["down"] for v in vals]
    h = height or max(2.4, 0.42 * len(data) + 0.6)
    fig, ax = plt.subplots(figsize=(7.4, h), dpi=200)
    _clean(ax, th, left=False, bottom=False)
    yidx = list(range(len(names)))
    ax.barh(yidx, vals, color=colors, height=0.66, zorder=3)
    ax.axvline(0, color=th["ink"], lw=1.0, zorder=4)
    ax.set_yticks(yidx)
    ax.set_yticklabels(names, fontsize=9.5, fontfamily=MONO,
                       fontweight="medium", color=th["ink"])
    f = _fmt(y_format, currency, (" " + unit) if unit else "")
    for i, v in zip(yidx, vals):
        off = 3 if v >= 0 else -3
        ha = "left" if v >= 0 else "right"
        sign = "+" if v >= 0 else ""
        ax.annotate(sign + f(v), (v, i), xytext=(off, 0), textcoords="offset points",
                    va="center", ha=ha, fontsize=8.5, fontfamily=MONO,
                    color=(th["up"] if v >= 0 else th["down"]), fontweight="bold")
    ax.set_xticks([])
    ax.tick_params(left=False)
    m = max(abs(min(vals)), abs(max(vals))) or 1
    ax.set_xlim(-m * 1.34, m * 1.34)
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


def chart_bar_h(items, title=None, caption=None, highlight=None,
                y_format="num", currency="", unit="", height=None, **_):
    """Ranking ngang: items=[{'name','value'}] (đã hoặc chưa sort -> tự sort giảm dần).
    highlight: tên item tô màu emerald (nổi bật), còn lại màu accent (forest)."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    data = sorted(items, key=lambda d: d["value"])  # nhỏ dưới -> lớn trên cùng khi barh
    names = [d["name"] for d in data]
    vals = [d["value"] for d in data]
    colors = [th["up"] if (highlight and d["name"] == highlight) else th["accent"]
              for d in data]
    h = height or max(2.4, 0.42 * len(data) + 0.6)
    fig, ax = plt.subplots(figsize=(7.4, h), dpi=200)
    _clean(ax, th, left=False, bottom=False)
    yidx = list(range(len(names)))
    ax.barh(yidx, vals, color=colors, height=0.66, zorder=3)
    ax.set_yticks(yidx)
    ax.set_yticklabels(names, fontsize=9.5, fontfamily=MONO, color=th["ink"])
    f = _fmt(y_format, currency, (" " + unit) if unit else "")
    for i, v in zip(yidx, vals):
        ax.annotate(f(v), (v, i), xytext=(4, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=8.5, fontfamily=MONO,
                    color=th["ink"], fontweight="medium")
    ax.set_xticks([])
    ax.tick_params(left=False)
    ax.set_xlim(0, max(vals) * 1.18)
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


def chart_waterfall(steps, title=None, caption=None, y_format="num",
                    currency="", height=3.0, **_):
    """Waterfall phân rã: steps=[{'name','value','kind'}], kind in
    {'start','delta','total'}. delta + -> emerald, - -> đỏ; start/total -> ink."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    names = [s["name"] for s in steps]
    fig, ax = plt.subplots(figsize=(7.4, height), dpi=200)
    _clean(ax, th)
    run = 0.0
    f = _fmt(y_format, currency)
    for i, s in enumerate(steps):
        kind = s.get("kind", "delta")
        v = s["value"]
        if kind in ("start", "total"):
            bottom, hgt, col = 0, v, th["ink"]
            run = v
        else:
            bottom = run if v >= 0 else run + v
            hgt = abs(v)
            col = th["up"] if v >= 0 else th["down"]
            run = run + v
        ax.bar(i, hgt, bottom=bottom, color=col, width=0.62, zorder=3)
        top = bottom + hgt
        ax.annotate((("+" if v >= 0 and kind == "delta" else "") + f(v)),
                    (i, top), xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, fontfamily=MONO,
                    color=th["ink"], fontweight="medium")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontsize=8.5, fontfamily=BODY, color=th["ink"])
    ax.yaxis.set_major_formatter(FuncFormatter(f))
    for t in ax.get_yticklabels():
        t.set_fontfamily(MONO); t.set_fontsize(8)
    ax.grid(axis="y", color=th["grid"], lw=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color=th["muted"], lw=0.8)
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


def chart_bar_grouped(categories, series, title=None, caption=None,
                      y_format="num", currency="", highlight=None, height=3.0, **_):
    """Grouped bar: categories=[...]; series=[{'name','values':[...]}].
    <=2 series direct-label; màu accent + slate + up. highlight: tên series tô emerald."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    palette = [th["accent"], th["slate"], th["up"], th["down"]]
    n = len(series)
    idx = list(range(len(categories)))
    w = 0.8 / max(n, 1)
    fig, ax = plt.subplots(figsize=(7.4, height), dpi=200)
    _clean(ax, th)
    for si, s in enumerate(series):
        col = th["up"] if (highlight and s["name"] == highlight) else palette[si % len(palette)]
        xs = [i + (si - (n - 1) / 2) * w for i in idx]
        ax.bar(xs, s["values"], width=w * 0.92, color=col, zorder=3, label=s["name"])
    ax.set_xticks(idx)
    ax.set_xticklabels(categories, fontsize=8.5, fontfamily=BODY, color=th["ink"])
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt(y_format, currency)))
    for t in ax.get_yticklabels():
        t.set_fontfamily(MONO); t.set_fontsize(8)
    ax.grid(axis="y", color=th["grid"], lw=0.8)
    ax.set_axisbelow(True)
    leg = ax.legend(frameon=False, fontsize=8, loc="upper right", ncol=min(n, 3))
    for txt in leg.get_texts():
        txt.set_fontfamily(BODY); txt.set_color(th["ink"])
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


def chart_scatter(points, title=None, caption=None, x_label=None, y_label=None,
                  x_format="num", y_format="num", quadrant=False, height=3.4, **_):
    """Scatter: points=[{'x','y','label'(opt),'up'(opt bool)}].
    quadrant=True vẽ đường chia trung vị. up=True -> emerald, False -> đỏ, None -> accent."""
    plt, FuncFormatter = _ensure_mpl()
    th = _theme()
    fig, ax = plt.subplots(figsize=(7.4, height), dpi=200)
    _clean(ax, th)
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    for p in points:
        up = p.get("up", None)
        col = th["accent"] if up is None else (th["up"] if up else th["down"])
        ax.scatter([p["x"]], [p["y"]], s=70, color=col, alpha=0.85,
                   edgecolor=th["paper"], linewidth=1.0, zorder=3)
        if p.get("label"):
            ax.annotate(p["label"], (p["x"], p["y"]), xytext=(5, 4),
                        textcoords="offset points", fontsize=8, fontfamily=MONO,
                        color=th["ink"])
    if quadrant and xs and ys:
        import statistics as st
        ax.axvline(st.median(xs), color=th["muted"], lw=0.8, ls=(0, (4, 3)), alpha=0.7)
        ax.axhline(st.median(ys), color=th["muted"], lw=0.8, ls=(0, (4, 3)), alpha=0.7)
    if x_label:
        ax.set_xlabel(x_label, fontsize=9, fontfamily=BODY, color=th["ink"])
    if y_label:
        ax.set_ylabel(y_label, fontsize=9, fontfamily=BODY, color=th["ink"])
    ax.xaxis.set_major_formatter(FuncFormatter(_fmt(x_format)))
    ax.yaxis.set_major_formatter(FuncFormatter(_fmt(y_format)))
    for t in (ax.get_xticklabels() + ax.get_yticklabels()):
        t.set_fontfamily(MONO); t.set_fontsize(8)
    ax.grid(True, color=th["grid"], lw=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.6)
    return _wrap(fig, plt, title, caption)


# ============================================================
# STYLES (wired vào _build_css của orchestrator)
# ============================================================
def chart_styles() -> str:
    return """
.lpt-chart { margin: 6mm 0; page-break-inside: avoid; }
.lpt-chart img { width: 100%; display: block; border-radius: 5px; }
.lpt-chart .lpt-chart-title { font-family: 'Inter','InterVN',sans-serif; font-size: 8.5pt; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--indigo); margin-bottom: 3mm; }
.lpt-chart figcaption { font-family: 'Inter','InterVN',sans-serif; font-size: 8pt; color: var(--text-secondary); margin-top: 3mm; line-height: 1.5; }
"""


# ============================================================
# SMOKE TEST
# ============================================================
if __name__ == "__main__":
    os.environ.setdefault("STOCKLPT_BRAND", "stocklpt")
    n = 0
    n += len(chart_line([10, 12, 9, 14, 13], markers=[[0, "A", "bottom"], [3, "B", "top"]],
                        ref=10, ref_label="ref", title="Line", caption="cap"))
    n += len(chart_diverging([{"name": "X", "value": 5}, {"name": "Y", "value": -3}],
                             title="Diverging", unit="tỷ"))
    n += len(chart_bar_h([{"name": "P", "value": 8}, {"name": "Q", "value": 3}],
                         highlight="P", title="Rank"))
    n += len(chart_waterfall([{"name": "Đầu", "value": 100, "kind": "start"},
                              {"name": "Δ1", "value": 20, "kind": "delta"},
                              {"name": "Δ2", "value": -15, "kind": "delta"},
                              {"name": "Cuối", "value": 105, "kind": "total"}], title="WF"))
    n += len(chart_bar_grouped(["Q1", "Q2"], [{"name": "A", "values": [3, 5]},
                                              {"name": "B", "values": [4, 2]}], title="Grp"))
    n += len(chart_scatter([{"x": 1, "y": 2, "label": "a", "up": True},
                            {"x": 3, "y": 1, "label": "b", "up": False}], quadrant=True, title="Sc"))
    print("viz_charts smoke OK, total html chars:", n)
    print("styles len:", len(chart_styles()))
