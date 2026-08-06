"""
fiinquant_adapter.py - map dữ liệu thị trường VN -> params viz StockLPT.
==========================================================================

GATE NĂNG LỰC (đọc trước khi dùng):
    Module này KHÔNG tự gọi FiinQuant. Việc kiểm tra tài khoản có MCP FiinQuant
    (paid) hay không là ở tầng AGENT/LLM, TRƯỚC khi dùng adapter:

      1. Agent kiểm tra có tool MCP FiinQuant không (dò tool registry / call test rẻ).
      2. NẾU CÓ  -> pull dữ liệu live, đưa dict thô vào các hàm dưới.
         NẾU KHÔNG -> nhận CÙNG shape dict đó từ input JSON thủ công của người dùng.

    Cả hai đường dùng chung adapter này, nên pipeline KHÔNG phụ thuộc cứng vào
    FiinQuant: thiếu MCP thì degrade gọn về nhập tay, không vỡ.

Các hàm trả về đúng shape mà component trong `stocklpt-data-viz` mong đợi
(capsule_verdict.metrics, quadrant_scatter.points, bar_horizontal.items, chart_line.series).
"""
from __future__ import annotations


# ------------------------------------------------------------------ helpers
def vnnum(x, decimals: int = 0) -> str:
    """Format số kiểu VN: dấu chấm phân tách nghìn, dấu phẩy thập phân.
    vnnum(41165, 0) -> '41.165' ; vnnum(1.92, 2) -> '1,92'."""
    if x is None:
        return "-"
    s = f"{float(x):,.{decimals}f}"          # 41,165.00 (en)
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def _pick(d: dict, *keys, default=None):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default


# ------------------------------------------------------ capsule metric rail
def snapshot_to_capsule_metrics(snap: dict) -> list[dict]:
    """snap: dict có thể chứa pe, pb, roe, eps, market_cap_ty, npat_ty, yoy...
    Trả list {value,label,note} cho capsule_verdict.metrics (bỏ field thiếu)."""
    out = []
    pe = _pick(snap, "pe", "PE")
    if pe is not None:
        out.append({"value": f"{vnnum(pe, 1)}x", "label": "P/E", "note": _pick(snap, "pe_note", default="")})
    pb = _pick(snap, "pb", "PB")
    if pb is not None:
        out.append({"value": f"{vnnum(pb, 2)}x", "label": "P/B", "note": _pick(snap, "pb_note", default="")})
    roe = _pick(snap, "roe", "ROE")
    if roe is not None:
        out.append({"value": f"{vnnum(roe, 1)}%", "label": _pick(snap, "roe_label", default="ROE"), "note": _pick(snap, "roe_note", default="")})
    npat = _pick(snap, "npat_ty", "lnst_ty", "npat")
    if npat is not None:
        out.append({"value": vnnum(npat, 0), "label": _pick(snap, "npat_label", default="LNST (tỷ)"), "note": _pick(snap, "npat_note", default="")})
    return out[:4]


# --------------------------------------------------- peer P/B vs ROE scatter
def peers_to_scatter(peers: list[dict], focus: str | None = None,
                     x_key: str = "roe", y_key: str = "pb",
                     focus_color: str = "#C8972E") -> list[dict]:
    """peers: list {ticker, roe, pb}. Trả points cho quadrant_scatter; mã `focus`
    được tô gold + size lớn (để 'lộ' trong nhóm)."""
    pts = []
    for p in peers:
        tk = _pick(p, "ticker", "label", "ma", default="")
        pt = {"x": _pick(p, x_key, default=0), "y": _pick(p, y_key, default=0), "label": tk}
        if focus and tk.upper() == focus.upper():
            pt["color"] = focus_color
            pt["size"] = 13
        pts.append(pt)
    return pts


# -------------------------------------------------------- annual / quarterly bar
def rows_to_bar(rows: list[dict], label_key: str = "label", value_key: str = "value",
                highlight_last_positive: bool = True) -> list[dict]:
    """rows: list {label, value}. Trả items cho bar_horizontal, có value_label VN.
    Mặc định mã/năm cuối được đánh dấu positive (điểm nhấn)."""
    items = []
    for i, r in enumerate(rows):
        v = _pick(r, value_key, default=0)
        it = {"label": str(_pick(r, label_key, default="")), "value": v,
              "value_label": _pick(r, "value_label", default=vnnum(v, 0))}
        if highlight_last_positive and i == len(rows) - 1:
            it["positive"] = True
        items.append(it)
    return items


# ----------------------------------------------------------- price -> series
def prices_to_series(prices: list, close_key: str = "close") -> list[float]:
    """prices: list số HOẶC list {close}. Trả list[float] cho chart_line.series."""
    out = []
    for p in prices:
        if isinstance(p, dict):
            c = _pick(p, close_key, "Close", default=None)
        else:
            c = p
        if c is not None:
            out.append(float(c))
    return out


if __name__ == "__main__":
    assert vnnum(41165, 0) == "41.165"
    assert vnnum(1.92, 2) == "1,92"
    m = snapshot_to_capsule_metrics({"pe": 5.55, "pb": 1.92, "roe": 28.9, "npat_ty": 5410})
    assert len(m) == 4 and m[0]["value"] == "5,5x" and m[1]["value"] == "1,92x", m
    s = peers_to_scatter([{"ticker": "VIX", "roe": 28.9, "pb": 1.92},
                          {"ticker": "SSI", "roe": 14.0, "pb": 1.69}], focus="VIX")
    assert s[0]["color"] == "#C8972E" and s[0]["size"] == 13, s
    b = rows_to_bar([{"label": "2024", "value": 663}, {"label": "2025", "value": 5410}])
    assert b[-1]["positive"] and b[-1]["value_label"] == "5.410", b
    assert prices_to_series([{"close": 16900}, 16800]) == [16900.0, 16800.0]
    print("fiinquant_adapter smoke OK")
