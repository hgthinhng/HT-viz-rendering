"""
viz_daily.py - Bộ component visual cho BÁO CÁO PHIÊN (daily) StockLPT.
=====================================================================
First-class viz components, dùng qua viz_plan như mọi component khác (cả daily
lẫn deep). Palette StockLPT native, self-contained <style>, WeasyPrint-safe (HTML+CSS).

Component:
  stat_cards   - dải thẻ KPI phiên (VN-Index, thanh khoản, khối ngoại...)
  price_table  - bảng giá Mã/Giá/%/GTGD với ticker-badge + màu tăng/giảm
  money_flow   - thanh diverging mua/bán ròng (khối ngoại, tự doanh, tổ chức...)
  daily_alert  - callout cảnh báo (đột biến khối lượng, mã nóng)
"""
from __future__ import annotations
from html import escape

# StockLPT native palette
_INK = "#2A1A4A"; _ACCENT = "#16633C"; _UP = "#21B36A"; _DOWN = "#E13453"
_GOLD = "#C8972E"; _PAPER = "#F4F6F9"; _MUTED = "#645B76"; _TEXT = "#221A34"
_SANS = "'Inter','InterVN',sans-serif"; _SERIF = "'PFD','PFDVN',serif"; _MONO = "'JBM','JBMVN',monospace"


def _vnnum(x, d=0):
    if x is None or x == "":
        return ""
    try:
        s = f"{float(x):,.{d}f}"
        return s.replace(",", "§").replace(".", ",").replace("§", ".")
    except (TypeError, ValueError):
        return str(x)


def _tone_of(v):
    try:
        return "up" if float(v) > 0 else ("down" if float(v) < 0 else "flat")
    except (TypeError, ValueError):
        return "flat"


# ----------------------------------------------------------------- stat_cards
def stat_cards(cards: list, title: str = "") -> str:
    """cards: list {value,label,delta?,tone?}. tone: up|down|flat (màu delta)."""
    tc = {"up": _UP, "down": _DOWN, "flat": _MUTED}
    cells = ""
    for c in cards:
        col = tc.get(c.get("tone", "flat"), _MUTED)
        delta = c.get("delta", "")
        d = f'<div class="vd-sc-d" style="color:{col};">{escape(str(delta))}</div>' if delta else ""
        cells += (
            '<div class="vd-sc">'
            f'<div class="vd-sc-v">{escape(str(c.get("value", "")))}</div>{d}'
            f'<div class="vd-sc-l">{escape(c.get("label", ""))}</div></div>'
        )
    head = f'<div class="vd-h">{escape(title)}</div>' if title else ""
    return (
        "<style>"
        ".vd-cards{display:flex;gap:4mm;margin:6mm 0;}"
        ".vd-sc{flex:1;background:#FAFBFD;border:0.7px solid rgba(42,26,74,0.14);border-top:2.5px solid " + _INK + ";"
        "border-radius:3px;padding:5mm 5mm 4.5mm;}"
        ".vd-sc-v{font-family:" + _MONO + ";font-size:18pt;font-weight:600;color:" + _INK + ";line-height:1;}"
        ".vd-sc-d{font-family:" + _MONO + ";font-size:9.5pt;font-weight:600;margin-top:1.5mm;}"
        ".vd-sc-l{font-size:8pt;letter-spacing:0.08em;text-transform:uppercase;color:" + _MUTED + ";margin-top:2mm;line-height:1.3;}"
        ".vd-h{font-family:" + _SERIF + ";font-size:12pt;font-weight:700;color:" + _INK + ";margin:0 0 3mm;}"
        "</style>"
        f'{head}<div class="vd-cards">{cells}</div>'
    )


# ---------------------------------------------------------------- price_table
def price_table(rows: list, title: str = "", subtitle: str = "") -> str:
    """rows: list {ma, gia, pct, gtgd?, note?}. pct số (vd 1.2 = +1,2%); màu theo dấu.
    Ticker-badge tô theo chiều tăng/giảm."""
    badge_c = {"up": _UP, "down": _DOWN, "flat": _MUTED}
    trs = ""
    for r in rows:
        tone = r.get("tone") or _tone_of(r.get("pct"))
        bc = badge_c.get(tone, _MUTED)
        pct = r.get("pct")
        pct_s = ""
        if pct not in (None, ""):
            sign = "+" if (isinstance(pct, (int, float)) and pct > 0) else ""
            pct_s = f'{sign}{_vnnum(pct, 1)}%' if isinstance(pct, (int, float)) else str(pct)
        gtgd = r.get("gtgd", "")
        trs += (
            "<tr>"
            f'<td><span class="vd-badge" style="background:{bc};">{escape(str(r.get("ma", "")))}</span></td>'
            f'<td class="vd-num">{escape(_vnnum(r.get("gia"), 0) if isinstance(r.get("gia"), (int, float)) else str(r.get("gia", "")))}</td>'
            f'<td class="vd-num" style="color:{bc};font-weight:600;">{escape(pct_s)}</td>'
            f'<td class="vd-num vd-mut">{escape(_vnnum(gtgd, 0) if isinstance(gtgd, (int, float)) else str(gtgd))}</td>'
            f'<td class="vd-note">{escape(r.get("note", ""))}</td>'
            "</tr>"
        )
    head = f'<div class="vd-h">{escape(title)}</div>' if title else ""
    sub = f'<div class="vd-sub">{escape(subtitle)}</div>' if subtitle else ""
    return (
        "<style>"
        ".vd-pt{width:100%;border-collapse:collapse;margin:3mm 0 6mm;font-family:" + _SANS + ";}"
        ".vd-pt th{font-size:7.6pt;letter-spacing:0.08em;text-transform:uppercase;color:" + _MUTED + ";"
        "text-align:right;padding:0 0 2.5mm;border-bottom:1px solid rgba(42,26,74,0.2);}"
        ".vd-pt th:first-child,.vd-pt td:first-child{text-align:left;}"
        ".vd-pt th:last-child,.vd-pt td.vd-note{text-align:left;}"
        ".vd-pt td{padding:3mm 0;border-bottom:0.5px solid rgba(42,26,74,0.1);font-size:10pt;color:" + _TEXT + ";text-align:right;}"
        ".vd-num{font-family:" + _MONO + ";}"
        ".vd-mut{color:" + _MUTED + ";}"
        ".vd-pt td:nth-child(4),.vd-pt th:nth-child(4){padding-right:8mm;white-space:nowrap;}"
        ".vd-note{font-size:9pt;color:" + _MUTED + ";padding-left:2mm;}"
        ".vd-badge{display:inline-block;font-family:" + _MONO + ";font-size:9pt;font-weight:700;color:#F4F6F9;"
        "padding:1.2mm 3mm;border-radius:3px;letter-spacing:0.02em;}"
        ".vd-h{font-family:" + _SERIF + ";font-size:12pt;font-weight:700;color:" + _INK + ";margin:0;}"
        ".vd-sub{font-size:9pt;color:" + _MUTED + ";margin-top:1mm;}"
        "</style>"
        f'{head}{sub}<table class="vd-pt"><thead><tr>'
        '<th>Mã</th><th>Giá</th><th>%</th><th>GTGD (tỷ)</th><th>Ghi chú</th>'
        f'</tr></thead><tbody>{trs}</tbody></table>'
    )


# ----------------------------------------------------------------- money_flow
def money_flow(flows: list, title: str = "", subtitle: str = "", unit: str = "tỷ") -> str:
    """flows: list {label, value} (value +/- = mua/bán ròng). Thanh diverging từ tâm."""
    vals = [abs(float(f.get("value", 0) or 0)) for f in flows]
    mx = max(vals) if vals else 1
    rows = ""
    for f in flows:
        v = float(f.get("value", 0) or 0)
        w = (abs(v) / mx * 50) if mx else 0     # % nửa chiều rộng
        pos = v >= 0
        col = _UP if pos else _DOWN
        sign = "+" if pos else ""
        bar = (
            f'<div class="vd-mf-bar" style="{"left:50%" if pos else f"right:50%"};width:{w:.1f}%;background:{col};"></div>'
        )
        rows += (
            '<div class="vd-mf-row">'
            f'<div class="vd-mf-l">{escape(f.get("label", ""))}</div>'
            f'<div class="vd-mf-track"><div class="vd-mf-mid"></div>{bar}</div>'
            f'<div class="vd-mf-v" style="color:{col};">{sign}{_vnnum(v, 0)}</div>'
            '</div>'
        )
    head = f'<div class="vd-h">{escape(title)}</div>' if title else ""
    sub = f'<div class="vd-sub">{escape(subtitle)} (đơn vị: {escape(unit)}; xanh = mua ròng, đỏ = bán ròng)</div>'
    return (
        "<style>"
        ".vd-mf{margin:4mm 0 6mm;font-family:" + _SANS + ";}"
        ".vd-mf-row{display:flex;align-items:center;gap:4mm;padding:2mm 0;}"
        ".vd-mf-l{width:36mm;font-size:9.5pt;color:" + _TEXT + ";}"
        ".vd-mf-track{position:relative;flex:1;height:9px;background:rgba(42,26,74,0.05);border-radius:2px;}"
        ".vd-mf-mid{position:absolute;left:50%;top:-2px;bottom:-2px;width:1px;background:rgba(42,26,74,0.3);}"
        ".vd-mf-bar{position:absolute;top:0;bottom:0;border-radius:2px;}"
        ".vd-mf-v{width:22mm;text-align:right;font-family:" + _MONO + ";font-size:9.5pt;font-weight:600;}"
        ".vd-h{font-family:" + _SERIF + ";font-size:12pt;font-weight:700;color:" + _INK + ";margin:0;}"
        ".vd-sub{font-size:8.5pt;color:" + _MUTED + ";margin:1mm 0 2mm;}"
        "</style>"
        f'{head}{sub}<div class="vd-mf">{rows}</div>'
    )


# ----------------------------------------------------------------- daily_alert
def daily_alert(items: list, title: str = "Cảnh báo phiên") -> str:
    """items: list str HOẶC {ma, note}. Callout cảnh báo (đột biến KL, mã nóng)."""
    lis = ""
    for it in items:
        if isinstance(it, dict):
            lis += f'<li><span class="vd-al-ma">{escape(str(it.get("ma", "")))}</span>{escape(it.get("note", ""))}</li>'
        else:
            lis += f'<li>{escape(str(it))}</li>'
    return (
        "<style>"
        ".vd-al{border-top:2.5px solid " + _GOLD + ";background:rgba(200,151,46,0.07);border-radius:0 0 4px 4px;"
        "padding:4.5mm 6mm;margin:5mm 0;font-family:" + _SANS + ";page-break-inside:avoid;}"
        ".vd-al-h{font-size:8pt;letter-spacing:0.12em;text-transform:uppercase;color:" + _GOLD + ";font-weight:700;margin-bottom:2.5mm;}"
        ".vd-al ul{list-style:none;margin:0;padding:0;}"
        ".vd-al li{font-size:9.8pt;color:" + _TEXT + ";line-height:1.5;padding:1mm 0;}"
        ".vd-al-ma{font-family:" + _MONO + ";font-weight:700;color:" + _INK + ";margin-right:3mm;}"
        "</style>"
        f'<div class="vd-al"><div class="vd-al-h">{escape(title)}</div><ul>{lis}</ul></div>'
    )


def key_message(text: str, label: str = "Thông điệp chính") -> str:
    """Banner thông điệp chính (self-contained, cream trên ink; vẫn mang class callout.key cho QC daily)."""
    style = ("background:#2A1A4A;color:#EBEFF4;border-radius:4px;padding:5mm 6mm;margin:5mm 0;"
             "font-family:'Inter','InterVN',sans-serif;font-size:11pt;line-height:1.55;")
    return (f'<div class="callout key" style="{style}">'
            f'<b style="color:#C8972E;">{escape(label)}:</b> {escape(text)}</div>')


if __name__ == "__main__":
    import os
    os.environ.setdefault("STOCKLPT_BRAND", "stocklpt")
    a = stat_cards([{"value": "1.287,4", "label": "VN-Index", "delta": "+0,8%", "tone": "up"},
                    {"value": "21.450", "label": "GTGD (tỷ)", "delta": "+12%", "tone": "up"},
                    {"value": "-340", "label": "Khối ngoại (tỷ)", "delta": "Bán ròng", "tone": "down"}])
    b = price_table([{"ma": "HPG", "gia": 28000, "pct": 1.2, "gtgd": 540, "note": "KL gấp 2 lần TB"},
                     {"ma": "SSI", "gia": 30000, "pct": -0.5, "gtgd": 410}])
    c = money_flow([{"label": "Khối ngoại", "value": -340}, {"label": "Tự doanh", "value": 180},
                    {"label": "Tổ chức trong nước", "value": 90}])
    d = daily_alert([{"ma": "VIX", "note": "khối lượng gấp 3 lần bình quân 20 phiên"}, "Nhóm thép hút dòng tiền cuối phiên"])
    assert all(len(x) > 100 for x in (a, b, c, d))
    assert "vd-badge" in b and "vd-mf-bar" in c
    print("viz_daily smoke OK")
