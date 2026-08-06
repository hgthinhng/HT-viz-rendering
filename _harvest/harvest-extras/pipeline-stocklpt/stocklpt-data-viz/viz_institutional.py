"""
viz_institutional.py - Bộ component "Editorial Institutional Research" cho StockLPT.
=====================================================================================
Ngôn ngữ thiết kế: Goldman Sachs Equity Research + Bloomberg Intelligence + FT Weekend
+ Morningstar brief. NGUYÊN TẮC (chống AI-slop):
  - Hairline rule, KHÔNG card bo góc / KHÔNG nền tô / KHÔNG viền-trái.
  - Typography-first: tiêu đề serif, số liệu mono, nhãn small-caps.
  - Màu tiết chế: ink tím huyền là near-black; màu CHỈ dùng cho dữ liệu (tăng/giảm).
  - Grid dày đặc, mạch lạc; khoảng trắng có kỷ luật.

Component: research_masthead, data_strip, exec_brief, section_rule
Palette StockLPT native, self-contained <style>, WeasyPrint-safe.
"""
from __future__ import annotations
from html import escape

_INK = "#2A1A4A"; _ACCENT = "#16633C"; _UP = "#21B36A"; _DOWN = "#E13453"
_GOLD = "#C8972E"; _MUTED = "#645B76"; _TEXT = "#221A34"; _PAPER = "#F4F6F9"
_RULE = "rgba(42,26,74,0.16)"; _RULE2 = "rgba(42,26,74,0.30)"
_SANS = "'Inter','InterVN',sans-serif"; _SERIF = "'PFD','PFDVN',serif"; _MONO = "'JBM','JBMVN',monospace"


def _vn(x, d=0):
    if x is None or x == "":
        return ""
    try:
        return f"{float(x):,.{d}f}".replace(",", "§").replace(".", ",").replace("§", ".")
    except (TypeError, ValueError):
        return str(x)


# ------------------------------------------------------------- research_masthead
def research_masthead(title: str, kind: str = "MARKET VIEW", firm: str = "STOCKLPT RESEARCH",
                      date: str = "", subtitle: str = "", rating: str = "") -> str:
    """Masthead note nghiên cứu: eyebrow firm/kind, tiêu đề serif, ngày, rule đậm."""
    rt = f'<span class="im-rt">{escape(rating)}</span>' if rating else ""
    sub = f'<div class="im-sub">{escape(subtitle)}</div>' if subtitle else ""
    return (
        "<style>"
        "@page :first { @top-center{content:none;border:none;} }"
        ".im-mh{margin:0 0 7mm;font-family:" + _SANS + ";border-top:2px solid " + _INK + ";padding-top:3mm;}"
        ".im-eye{display:flex;justify-content:space-between;font-size:8pt;letter-spacing:0.16em;text-transform:uppercase;}"
        ".im-firm{color:" + _ACCENT + ";font-weight:700;}"
        ".im-kind{color:" + _MUTED + ";}"
        ".im-trow{display:flex;justify-content:space-between;align-items:flex-end;margin-top:5mm;"
        "border-bottom:1.5px solid " + _INK + ";padding-bottom:3mm;}"
        ".im-title{font-family:" + _SERIF + ";font-size:25pt;font-weight:700;line-height:1.05;color:" + _INK + ";letter-spacing:-0.01em;max-width:150mm;}"
        ".im-date{font-family:" + _MONO + ";font-size:9pt;color:" + _MUTED + ";white-space:nowrap;padding-bottom:1mm;}"
        ".im-sub{font-family:" + _SERIF + ";font-style:italic;font-size:12pt;color:" + _MUTED + ";margin-top:2.5mm;}"
        ".im-rt{display:inline-block;font-family:" + _SANS + ";font-size:8.5pt;font-weight:700;letter-spacing:0.06em;"
        "color:#F4F6F9;background:" + _INK + ";padding:1.6mm 3.5mm;margin-left:4mm;vertical-align:middle;}"
        "</style>"
        '<div class="im-mh">'
        f'<div class="im-eye"><span class="im-firm">{escape(firm)}</span><span class="im-kind">{escape(kind)}</span></div>'
        f'<div class="im-trow"><div class="im-title">{escape(title)}{rt}</div>'
        f'<div class="im-date">{escape(date)}</div></div>{sub}</div>'
    )


# ------------------------------------------------------------------- data_strip
def data_strip(items: list) -> str:
    """Dải KPI kiểu Bloomberg: số mono, nhãn small-caps, vạch dọc hairline, KHÔNG card."""
    tc = {"up": _UP, "down": _DOWN, "flat": _MUTED}
    cells = ""
    for it in items:
        col = tc.get(it.get("tone", "flat"), _MUTED)
        delta = it.get("delta", "")
        d = f'<div class="im-ds-d" style="color:{col};">{escape(str(delta))}</div>' if delta else ""
        cells += (
            '<div class="im-ds-c">'
            f'<div class="im-ds-l">{escape(it.get("label", ""))}</div>'
            f'<div class="im-ds-v">{escape(str(it.get("value", "")))}</div>{d}</div>'
        )
    return (
        "<style>"
        ".im-ds{display:flex;border-top:1px solid " + _INK + ";border-bottom:1px solid " + _INK + ";margin:0 0 7mm;}"
        ".im-ds-c{flex:1;padding:4mm 5mm 4mm 0;margin-right:5mm;border-right:0.6px solid " + _RULE + ";}"
        ".im-ds-c:last-child{border-right:none;margin-right:0;}"
        ".im-ds-l{font-family:" + _SANS + ";font-size:7.6pt;letter-spacing:0.1em;text-transform:uppercase;color:" + _MUTED + ";}"
        ".im-ds-v{font-family:" + _MONO + ";font-size:17pt;font-weight:600;color:" + _INK + ";line-height:1;margin-top:2.5mm;}"
        ".im-ds-d{font-family:" + _MONO + ";font-size:9pt;font-weight:600;margin-top:1.5mm;}"
        "</style>"
        f'<div class="im-ds">{cells}</div>'
    )


# -------------------------------------------------------------------- exec_brief
def exec_brief(thesis: str, stats: list = None, takeaways: list = None,
               rating: str = "", eyebrow: str = "Tóm tắt điều hành") -> str:
    """Brief điều hành kiểu Morningstar/GS: luận điểm serif + bảng số ruled + takeaways
    đánh số. Hairline, KHÔNG box. stats: [{label,value}]. takeaways: [{lead,detail}] hoặc [str]."""
    stats = stats or []; takeaways = takeaways or []
    srows = "".join(
        f'<div class="im-st-row"><span class="im-st-l">{escape(s.get("label", ""))}</span>'
        f'<span class="im-st-v">{escape(str(s.get("value", "")))}</span></div>' for s in stats
    )
    rt = f'<div class="im-eb-rt">{escape(rating)}</div>' if rating else ""
    tk = ""
    for i, t in enumerate(takeaways, 1):
        if isinstance(t, dict):
            tk += (f'<div class="im-tk"><span class="im-tk-n">{i:02d}</span>'
                   f'<span class="im-tk-b"><b>{escape(t.get("lead", ""))}</b> {escape(t.get("detail", ""))}</span></div>')
        else:
            tk += f'<div class="im-tk"><span class="im-tk-n">{i:02d}</span><span class="im-tk-b">{escape(str(t))}</span></div>'
    right = f'<div class="im-eb-r"><div class="im-st">{srows}</div></div>' if stats else ""
    return (
        "<style>"
        ".im-eb{margin:0 0 8mm;font-family:" + _SANS + ";border-top:1.5px solid " + _INK + ";padding-top:4mm;}"
        ".im-eb-eye{font-size:8pt;letter-spacing:0.14em;text-transform:uppercase;color:" + _ACCENT + ";font-weight:700;margin-bottom:4mm;}"
        ".im-eb-top{display:flex;gap:10mm;}"
        ".im-eb-l{flex:1.4;}"
        ".im-eb-rt{display:inline-block;font-size:8.5pt;font-weight:700;letter-spacing:0.06em;color:#F4F6F9;"
        "background:" + _INK + ";padding:1.4mm 3.5mm;margin-bottom:3mm;}"
        ".im-eb-thesis{font-family:" + _SERIF + ";font-size:15pt;line-height:1.5;color:" + _INK + ";}"
        ".im-eb-r{flex:1;border-left:0.6px solid " + _RULE + ";padding-left:8mm;}"
        ".im-st-row{display:flex;justify-content:space-between;align-items:baseline;padding:2.4mm 0;border-bottom:0.6px solid " + _RULE + ";}"
        ".im-st-row:first-child{border-top:0.6px solid " + _RULE + ";}"
        ".im-st-l{font-size:8.4pt;letter-spacing:0.06em;text-transform:uppercase;color:" + _MUTED + ";}"
        ".im-st-v{font-family:" + _MONO + ";font-size:11pt;font-weight:600;color:" + _INK + ";}"
        ".im-tks{margin-top:7mm;}"
        ".im-tk{display:flex;gap:5mm;padding:3.2mm 0;border-top:0.6px solid " + _RULE + ";}"
        ".im-tk:last-child{border-bottom:0.6px solid " + _RULE + ";}"
        ".im-tk-n{font-family:" + _MONO + ";font-size:10pt;font-weight:700;color:" + _GOLD + ";}"
        ".im-tk-b{font-size:10pt;line-height:1.5;color:" + _TEXT + ";}"
        ".im-tk-b b{color:" + _INK + ";font-weight:700;}"
        "</style>"
        '<div class="im-eb">'
        f'<div class="im-eb-eye">{escape(eyebrow)}</div>'
        f'<div class="im-eb-top"><div class="im-eb-l">{rt}<div class="im-eb-thesis">{escape(thesis)}</div></div>{right}</div>'
        f'<div class="im-tks">{tk}</div></div>'
    )


# ----------------------------------------------------------------- section_rule
def section_rule(num: str, title: str) -> str:
    """Tiêu đề mục kiểu research: số mono accent + tên serif + rule mảnh."""
    return (
        "<style>"
        ".im-sr{display:flex;align-items:baseline;gap:4mm;border-bottom:1px solid " + _INK + ";"
        "padding-bottom:2.5mm;margin:8mm 0 5mm;}"
        ".im-sr-n{font-family:" + _MONO + ";font-size:11pt;font-weight:700;color:" + _ACCENT + ";}"
        ".im-sr-t{font-family:" + _SERIF + ";font-size:15pt;font-weight:700;color:" + _INK + ";}"
        "</style>"
        f'<div class="im-sr"><span class="im-sr-n">{escape(num)}</span><span class="im-sr-t">{escape(title)}</span></div>'
    )


if __name__ == "__main__":
    import os
    os.environ.setdefault("STOCKLPT_BRAND", "stocklpt")
    a = research_masthead("Nhận định cuối phiên VN-Index", date="30/06/2026", rating="TRUNG LẬP",
                          subtitle="Thanh khoản cải thiện, khối ngoại vẫn bán ròng")
    b = data_strip([{"label": "VN-Index", "value": "1.287,4", "delta": "+0,8%", "tone": "up"},
                    {"label": "GTGD (tỷ)", "value": "21.450", "delta": "+12%", "tone": "up"},
                    {"label": "Khối ngoại", "value": "-340", "delta": "Bán ròng", "tone": "down"}])
    c = exec_brief("Thị trường giữ đà tăng nhẹ nhưng nội lực mỏng; dòng tiền nội đỡ giá trong khi khối ngoại bán ròng phiên thứ ba.",
                   stats=[{"label": "P/E VN-Index", "value": "13,8x"}, {"label": "Vùng hỗ trợ", "value": "1.260"}],
                   takeaways=[{"lead": "Thanh khoản cải thiện.", "detail": "GTGD +12%, tập trung thép và chứng khoán."},
                              {"lead": "Khối ngoại chưa quay lại.", "detail": "Bán ròng 340 tỷ, phiên thứ ba liên tiếp."}],
                   rating="QUAN ĐIỂM: TRUNG LẬP")
    d = section_rule("01", "Diễn biến kỹ thuật")
    assert all(len(x) > 150 for x in (a, b, c, d)) and "im-ds" in b and "im-tk" in c
    print("viz_institutional smoke OK")


# ============================================================
# DEEP-RESEARCH ADDITIONS (institutional finance viz)
# football_field · sensitivity_grid · bullet_kpi · sparkline_table
# ============================================================

def football_field(methods: list, current=None, title: str = "", subtitle: str = "", unit: str = "") -> str:
    """Dải định giá đa phương pháp (DCF, so sánh, 52w...) trên cùng trục giá.
    methods: [{label, low, high, mid?}]. current: giá hiện tại (vạch gold). Inline fill (WeasyPrint-safe)."""
    lows = [float(m["low"]) for m in methods]; highs = [float(m["high"]) for m in methods]
    lo = min(lows); hi = max(highs)
    if current is not None:
        lo = min(lo, float(current)); hi = max(hi, float(current))
    span = (hi - lo) or 1; pad = span * 0.07; lo -= pad; hi += pad; span = hi - lo
    W, L, R, rowH, top = 660, 120, 556, 30, 38
    H = top + len(methods) * rowH + 14
    X = lambda v: L + (float(v) - lo) / span * (R - L)
    body = ""
    for i, m in enumerate(methods):
        y = top + i * rowH + rowH / 2
        x1, x2 = X(m["low"]), X(m["high"])
        body += (f'<text x="{L-9}" y="{y+3:.1f}" text-anchor="end" fill="{_TEXT}" font-family="{_SANS}" font-size="9.5">{escape(m["label"])}</text>'
                 f'<rect x="{x1:.1f}" y="{y-6:.1f}" width="{max(2,x2-x1):.1f}" height="12" rx="2" fill="rgba(22,99,60,0.26)" stroke="{_ACCENT}" stroke-width="0.8"/>')
        if m.get("mid") is not None:
            xm = X(m["mid"]); body += f'<line x1="{xm:.1f}" y1="{y-8:.1f}" x2="{xm:.1f}" y2="{y+8:.1f}" stroke="{_INK}" stroke-width="1.5"/>'
        body += f'<text x="{x2+6:.1f}" y="{y+3:.1f}" text-anchor="start" fill="{_MUTED}" font-family="{_MONO}" font-size="8">{_vn(m["low"],0)} - {_vn(m["high"],0)}</text>'
    cur = ""
    if current is not None:
        xc = X(current)
        cur = (f'<line x1="{xc:.1f}" y1="{top-7}" x2="{xc:.1f}" y2="{top+len(methods)*rowH:.1f}" stroke="{_GOLD}" stroke-width="1.5" stroke-dasharray="3 2"/>'
               f'<text x="{xc:.1f}" y="{top-10}" text-anchor="middle" fill="{_GOLD}" font-family="{_MONO}" font-size="8" font-weight="700">Giá hiện tại · {_vn(current,0)}</text>')
    head = section_rule_inline(title) if title else ""
    sub = f'<div style="font-family:{_SANS};font-size:9pt;color:{_MUTED};margin:0 0 2mm;">{escape(subtitle)}</div>' if subtitle else ""
    return (f'<div style="margin:2mm 0 7mm;">{head}{sub}'
            f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">{cur}{body}</svg></div>')


def sensitivity_grid(row_vals: list, col_vals: list, data: list, row_label: str = "", col_label: str = "",
                     title: str = "", subtitle: str = "", center=None, fmt: int = 0) -> str:
    """Bảng nhạy 2 biến (vd WACC × tăng trưởng -> giá mục tiêu). Cell tô heat diverging quanh center."""
    flat = [float(c) for r in data for c in r if c is not None]
    lo, hi = min(flat), max(flat); ctr = float(center) if center is not None else (lo + hi) / 2
    def bg(v):
        v = float(v)
        if v >= ctr:
            t = (v - ctr) / ((hi - ctr) or 1); return f"rgba(33,179,106,{0.06+0.34*t:.2f})"
        t = (ctr - v) / ((ctr - lo) or 1); return f"rgba(225,52,83,{0.06+0.34*t:.2f})"
    th = "".join(f"<th>{_vn(c,fmt)}</th>" for c in col_vals)
    rows = ""
    for i, rv in enumerate(row_vals):
        tds = "".join(f'<td style="background:{bg(data[i][j])};">{_vn(data[i][j],fmt)}</td>' for j in range(len(col_vals)))
        rows += f'<tr><th class="sg-rh">{_vn(rv,fmt)}</th>{tds}</tr>'
    head = f'{section_rule_inline(title)}' if title else ""
    sub = f'<div class="sg-sub">{escape(subtitle)}{(" · cột: "+escape(col_label)) if col_label else ""}{(" · hàng: "+escape(row_label)) if row_label else ""}</div>'
    return (
        "<style>"
        ".sg{border-collapse:collapse;margin:2mm 0 7mm;font-family:" + _MONO + ";width:100%;}"
        ".sg th{font-family:" + _SANS + ";font-size:8pt;letter-spacing:0.04em;color:" + _MUTED + ";font-weight:700;padding:2.5mm 3mm;border-bottom:1px solid " + _INK + ";text-align:center;}"
        ".sg .sg-rh{border-bottom:0.5px solid " + _RULE + ";border-right:1px solid " + _INK + ";color:" + _INK + ";}"
        ".sg td{font-size:9.5pt;color:" + _TEXT + ";text-align:center;padding:2.6mm 3mm;border-bottom:0.5px solid " + _RULE + ";font-weight:600;}"
        ".sg-sub{font-family:" + _SANS + ";font-size:8.5pt;color:" + _MUTED + ";margin:0 0 2mm;}"
        "</style>"
        f'{head}{sub}<table class="sg"><thead><tr><th></th>{th}</tr></thead><tbody>{rows}</tbody></table>'
    )


def bullet_kpi(items: list, title: str = "", subtitle: str = "") -> str:
    """Bullet chart (Stephen Few): thực tế vs mục tiêu. items: [{label,value,target?,max?,unit?,d?,tone?}]."""
    tc = {"up": _UP, "down": _DOWN, "flat": _ACCENT}
    rows = ""
    for it in items:
        mx = float(it.get("max") or (float(it["value"]) * 1.35) or 1) or 1
        val = float(it["value"]); vw = max(1, min(100, val / mx * 100))
        col = tc.get(it.get("tone", "flat"), _ACCENT)
        tick = ""
        if it.get("target") is not None:
            tw = min(100, float(it["target"]) / mx * 100); tick = f'<div class="bk-tick" style="left:{tw:.1f}%;"></div>'
        rows += (
            '<div class="bk-row">'
            f'<div class="bk-l">{escape(it["label"])}</div>'
            f'<div class="bk-track"><div class="bk-val" style="width:{vw:.1f}%;background:{col};"></div>{tick}</div>'
            f'<div class="bk-v">{_vn(val, it.get("d", 0))}{escape(it.get("unit", ""))}</div>'
            '</div>'
        )
    head = f'{section_rule_inline(title)}' if title else ""
    sub = f'<div class="bk-sub">{escape(subtitle)} (vạch = mục tiêu)</div>' if subtitle or True else ""
    return (
        "<style>"
        ".bk{margin:2mm 0 7mm;font-family:" + _SANS + ";}"
        ".bk-sub{font-size:8.5pt;color:" + _MUTED + ";margin:0 0 3mm;}"
        ".bk-row{display:flex;align-items:center;gap:4mm;padding:1.8mm 0;}"
        ".bk-l{width:42mm;font-size:9.5pt;color:" + _TEXT + ";}"
        ".bk-track{position:relative;flex:1;height:11px;background:rgba(42,26,74,0.07);}"
        ".bk-val{position:absolute;left:0;top:0;bottom:0;}"
        ".bk-tick{position:absolute;top:-3px;bottom:-3px;width:2px;background:" + _INK + ";}"
        ".bk-v{width:22mm;text-align:right;font-family:" + _MONO + ";font-size:10pt;font-weight:600;color:" + _INK + ";}"
        "</style>"
        f'{head}{sub}<div class="bk">{rows}</div>'
    )


def sparkline_table(rows: list, title: str = "", subtitle: str = "",
                    cols=("Chỉ tiêu", "Xu hướng", "Hiện tại", "Δ")) -> str:
    """Bảng có sparkline inline (mật độ kiểu Bloomberg). rows: [{label,series,value,delta?,tone?}]."""
    trs = ""
    for r in rows:
        s = [float(x) for x in r["series"]]
        mn, mx = min(s), max(s); rng = (mx - mn) or 1
        n = len(s)
        pts = " ".join(f"{(i/(n-1) if n > 1 else 0)*78+1:.1f},{17-((v-mn)/rng*15+1):.1f}" for i, v in enumerate(s))
        up = s[-1] >= s[0]; tone = r.get("tone") or ("up" if up else "down")
        col = {"up": _UP, "down": _DOWN, "flat": _MUTED}.get(tone, _MUTED)
        spark = (f'<svg viewBox="0 0 80 18" width="80" height="18" xmlns="http://www.w3.org/2000/svg">'
                 f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.4"/>'
                 f'<circle cx="{((n-1)/(n-1) if n>1 else 0)*78+1:.1f}" cy="{17-((s[-1]-mn)/rng*15+1):.1f}" r="1.7" fill="{col}"/></svg>')
        trs += (f'<tr><td class="sk-l">{escape(r["label"])}</td><td class="sk-sp">{spark}</td>'
                f'<td class="sk-v">{escape(str(r.get("value", "")))}</td>'
                f'<td class="sk-d" style="color:{col};">{escape(str(r.get("delta", "")))}</td></tr>')
    head = f'{section_rule_inline(title)}' if title else ""
    sub = f'<div class="sk-sub">{escape(subtitle)}</div>' if subtitle else ""
    th = "".join(f"<th>{escape(c)}</th>" for c in cols)
    return (
        "<style>"
        ".sk{width:100%;border-collapse:collapse;margin:2mm 0 7mm;font-family:" + _SANS + ";}"
        ".sk th{font-size:7.6pt;letter-spacing:0.08em;text-transform:uppercase;color:" + _MUTED + ";text-align:right;padding:0 0 2.5mm;border-bottom:1px solid " + _INK + ";}"
        ".sk th:first-child,.sk td.sk-l{text-align:left;}.sk th:nth-child(2),.sk td.sk-sp{text-align:center;}"
        ".sk td{padding:2.6mm 0;border-bottom:0.5px solid " + _RULE + ";font-size:10pt;color:" + _TEXT + ";text-align:right;vertical-align:middle;}"
        ".sk-l{font-size:9.5pt;}.sk-v{font-family:" + _MONO + ";font-weight:600;color:" + _INK + ";}"
        ".sk-d{font-family:" + _MONO + ";font-size:9pt;font-weight:600;}"
        ".sk-sub{font-size:8.5pt;color:" + _MUTED + ";margin:0 0 2mm;}"
        "</style>"
        f'{head}{sub}<table class="sk"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'
    )


def section_rule_inline(title: str) -> str:
    """Tiêu đề nhỏ cho chart (không số), dùng nội bộ các component trên."""
    return (f'<div style="font-family:{_SERIF};font-size:12pt;font-weight:700;color:{_INK};'
            f'border-bottom:1px solid {_INK};padding-bottom:2mm;margin:0 0 3mm;">{escape(title)}</div>')
