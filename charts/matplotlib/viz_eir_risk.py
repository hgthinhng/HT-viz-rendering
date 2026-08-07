#!/usr/bin/env python3
"""viz_eir_risk.py, ba component rui ro / phan phoi MOI cho thu vien EIR matplotlib.

Cung khuon 6 file viz_eir*.py hien co (kicker/tieu de serif/subtitle/source line,
cung hop dong spec.json qua --spec/--out-dir/--only/--dpi/--list). Dat trong file
RIENG (khong sua bat ky file viz_eir*.py nao dang co) de khong giam chan len cac
tac vu khac dang sua sau file do trong cung phien lam viec.

Components (COMPONENTS keys):
  drawdown          -> c_drawdown          vung % sut giam tu dinh gan nhat theo thoi gian
  calendar_heatmap  -> c_calendar_heatmap  luoi ngay kieu GitHub contributions
  ecdf              -> c_ecdf              duong bac thang phan phoi tich luy thuc nghiem

Editorial meta keys nam trong params: title, kicker, subtitle, source, asof, rating,
firm. Chung render thanh khung trang tri; cac key con lai dieu khien do thi.

Ca ba component deu la VECTOR THUAN cho lan pdf-so: khong dung imshow/pcolormesh/
contourf, khong dat rasterized=True o bat ky Artist nao. Luoi mau cua
calendar_heatmap ve tung o bang Rectangle va thanh chu giai ve bang axvspan, dung
cach da kiem chung o c_correlation_matrix (viz_eir_stats.py) va c_sensitivity_grid
(viz_eir.py): hai component do tung dung imshow, bi doi vi imshow nhung mot anh
BITMAP vao SVG va gate RASTER cua repo doi 0 anh trong ban PDF giao di.

Usage:
  python3 viz_eir_risk.py --spec spec.json --out-dir OUT [--only ID] [--dpi 200]
  python3 viz_eir_risk.py --list
Exit code = number of failed figures (0 = all rendered).
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _eir_style as S
from _eir_style import (
    PAPER, PAPER_HI, NAVY, INK, MUTED, FAINT, GRID, TEAL, BRICK, GOLD, INDIGO,
    setup_fonts, palette, tone_color, fmt_value, despine, eir_fig,
    draw_masthead, draw_source, save, _badge, tint, shade,
)
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap, Normalize

setup_fonts()
SANS, SERIF, MONO = S.SANS, S.SERIF, S.MONO   # bound AFTER setup so they are resolved


# --------------------------------------------------------------- shared helpers
# Sao chep tu viz_eir_stats.py / viz_eir_panels.py de giu dung khuon thi giac. Khong
# import truc tiep tu hai file do duoc: ca hai deu nam ngoai pham vi duoc phep sua
# trong tac vu nay, va mot module moi phu thuoc nguoc vao module dang bi khoa se
# lam file nay vo tinh vo hieu neu ben kia doi ten ham noi bo cua no.
def _meta(p, accent):
    m = {k: p.get(k) for k in ("kicker", "title", "subtitle", "source", "asof",
                               "rating", "firm")}
    m["accent"] = accent
    return m


def _vn(txt):
    """Doi dau thap phan tu dau cham sang dau phay kieu Viet Nam
    (1,234.5 -> 1.234,5). Chi ap dung cho chuoi DA dinh dang so (qua fmt_value),
    khong dung cho chuoi tuy y. Cung logic voi _vn() cua viz_eir_panels.py."""
    if txt is None:
        return txt
    s = str(txt)
    if "." in s and "," in s:          # dang Anh co nhom nghin: 1,234.56
        s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    elif "." in s:                     # thap phan don gian: 3.40
        s = s.replace(".", ",")
    return s


def _fv(v, kind="num", currency="$", dp=None):
    """fmt_value() roi doi dau thap phan sang kieu Viet Nam."""
    return _vn(fmt_value(v, kind, currency, dp))


def _legend_row(fig, entries, y=0.075, x0=0.045):
    """Hang chu giai duoi cung (o mau/duong + nhan). entries = list (kind, color, label)
    voi kind trong {'sq', 'line', 'dash'}."""
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
        fig.text(tx, y + 0.004, label, transform=fig.transFigure, fontsize=8.4,
                 color=INK, family=SANS, ha="left", va="center")
        x = tx + 0.0092 * len(label) + 0.028
    return y


def _thin_ticks(n, max_ticks=9):
    """Chi so cac diem duoc gan nhan tren truc x khi n qua lon de hien het, tranh
    nhan de len nhau. Luon giu diem dau va diem cuoi."""
    if n <= max_ticks:
        return list(range(n))
    step = max(1, round(n / max_ticks))
    idx = list(range(0, n, step))
    if idx[-1] != n - 1:
        idx.append(n - 1)
    return idx


# ================================================================== 1. drawdown
def c_drawdown(p, accent):
    """Sụt giảm từ đỉnh (drawdown), phần trăm mất giá tính từ đỉnh gần nhất theo
    thời gian.

    Trả lời: "Danh mục này đã từng lỗ sâu nhất bao nhiêu, và mất bao lâu để về lại
    đỉnh cũ?" Vùng tô dưới trục 0 là mức sụt giảm so với đỉnh CAO NHẤT tính đến
    từng thời điểm (không phải so với kỳ liền trước), điểm sụt sâu nhất được đánh
    dấu kèm phần trăm, và một chú thích riêng ghi số kỳ đã mất để giá trị vượt lại
    đỉnh cũ, hoặc nói rõ CHƯA HỒI PHỤC nếu chuỗi kết thúc khi còn dưới đỉnh.

    Dữ liệu cần: dates là nhãn thời gian tăng dần, values là NAV hoặc giá trị tài
    sản CÙNG ĐƠN VỊ tại mỗi mốc (không phải lợi suất phần trăm đã tính sẵn từng kỳ,
    vì drawdown cần biết đỉnh tuyệt đối chứ không đọc lại được từ chuỗi % rời rạc).
    Tuỳ chọn period_label đặt tên đơn vị kỳ trong câu chú thích hồi phục (mặc định
    "phiên").

    KHÔNG dùng khi values có dưới hai mươi quan sát, vì khi đó đường sụt giảm chỉ
    còn vài bậc thang rời rạc, không đủ để đọc ra hình dạng phục hồi; dùng
    before_after (viz_eir_panels.py) cho so sánh hai mốc đơn.
    """
    dates = list(p["dates"]); values = np.array(p["values"], float)
    n = len(values)
    if n < 2 or len(dates) != n:
        raise ValueError("drawdown can it nhat 2 quan sat, dates va values cung do dai")
    period_label = p.get("period_label", "phiên")

    running_peak = np.maximum.accumulate(values)
    dd = (values / running_peak - 1.0) * 100.0

    trough_i = int(np.argmin(dd))
    peak_level = running_peak[trough_i]
    # chi so CUOI CUNG truoc/tai trough ma chinh chuoi dat dung muc dinh do: peak_level
    # duoc lay TU values (qua maximum.accumulate) chu khong tinh lai doc lap, nen so
    # sanh bang tuyet doi o day la an toan, khac han loai so sanh float "kinh te tuong
    # duong" ma schema.py canh bao trong co_co().
    peak_i = int(np.where(values[: trough_i + 1] == peak_level)[0][-1])

    recovered_i = None
    for j in range(trough_i + 1, n):
        if values[j] >= peak_level:
            recovered_i = j
            break

    xs = np.arange(n)
    fig, ax = eir_fig(_meta(p, accent), figsize=(8.2, 4.8), rect=(0.09, 0.20, 0.86, 0.52))
    despine(ax, keep=("left", "bottom"), grid_axis="y")

    # dai "duoi nuoc": tu dinh toi luc hoi phuc (hoac het chuoi neu chua hoi phuc)
    end_i = recovered_i if recovered_i is not None else n - 1
    ax.axvspan(xs[peak_i], xs[end_i], color=GOLD, alpha=0.07, lw=0, zorder=1)

    ax.fill_between(xs, dd, 0, color=BRICK, alpha=0.22, lw=0, zorder=2)
    ax.plot(xs, dd, color=BRICK, lw=2.0, zorder=3)
    ax.axhline(0, color=INK, lw=1.0, zorder=3)

    ax.scatter([xs[trough_i]], [dd[trough_i]], s=80, color=BRICK, zorder=5,
               edgecolor=PAPER, linewidth=1.4)
    ax.annotate(f"Sụt sâu nhất {_fv(dd[trough_i], 'pct', dp=1)}",
                (xs[trough_i], dd[trough_i]), color=BRICK, fontsize=9.6,
                fontweight="bold", family=SANS, ha="center", va="top",
                xytext=(0, -10), textcoords="offset points")

    if recovered_i is not None:
        duration = recovered_i - peak_i
        ax.scatter([xs[recovered_i]], [dd[recovered_i]], s=46, color=NAVY, zorder=5,
                   edgecolor=PAPER, linewidth=1.0)
        ax.annotate(f"Về lại đỉnh cũ sau {duration} {period_label}",
                    (xs[recovered_i], 0), color=NAVY, fontsize=8.8, fontweight="bold",
                    family=SANS, ha="center", va="bottom", xytext=(0, 6),
                    textcoords="offset points")
    else:
        duration = n - 1 - peak_i
        ax.annotate(f"Chưa về lại đỉnh cũ sau {duration} {period_label} (đến hết chuỗi)",
                    (xs[-1], dd[-1]), color=MUTED, fontsize=8.6, style="italic",
                    family=SANS, ha="right", va="top", xytext=(-2, -4),
                    textcoords="offset points")

    tick_idx = _thin_ticks(n)
    ax.set_xticks(tick_idx)
    if n > 12:
        ax.set_xticklabels([dates[i] for i in tick_idx], fontsize=8.4, color=INK,
                           rotation=30, ha="right", rotation_mode="anchor")
    else:
        ax.set_xticklabels([dates[i] for i in tick_idx], fontsize=8.8, color=INK)
    ax.set_xlim(-0.5, n - 0.5)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fv(v, "pct", dp=0)))
    ax.margins(y=0.16)
    if p.get("x_label"):
        ax.set_xlabel(p["x_label"], fontsize=9.5, color=INK)

    _legend_row(fig, [
        ("sq", tint(BRICK, 0.30), "Mức sụt giảm so với đỉnh gần nhất"),
        ("sq", BRICK, "Điểm sụt sâu nhất"),
        ("sq", tint(GOLD, 0.24), "Giai đoạn dưới nước (đỉnh cũ tới lúc hồi phục)"),
    ], y=0.075)
    return fig


# ============================================================ 2. calendar_heatmap
_THANG_VN = ["Th1", "Th2", "Th3", "Th4", "Th5", "Th6", "Th7", "Th8", "Th9", "Th10",
             "Th11", "Th12"]
# Thu 2 (Mon) .. Chu nhat (Sun), dung nhan rut gon kieu lich Viet Nam
_THU_VN = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]


def c_calendar_heatmap(p, accent):
    """Lưới ngày kiểu GitHub contributions, một ô cho mỗi ngày.

    Trả lời: "Giá trị hằng ngày phân bố ra sao qua một tới hai năm, và ngày nào bất
    thường?" Mỗi cột là một tuần, mỗi hàng là một thứ trong tuần; màu ô mã hoá giá
    trị của ngày đó, viền vàng đánh dấu ngày lệch hơn ba độ lệch chuẩn so với trung
    bình cả chuỗi.

    Dữ liệu cần: dates là danh sách ngày ISO (YYYY-MM-DD), values là một giá trị số
    cho mỗi ngày, cùng độ dài với dates. Ngày không xuất hiện trong dates để trống
    (không vẽ ô), không gộp vào 0. Tuỳ chọn value_label mô tả đơn vị giá trị cho
    thanh chú giải.

    KHÔNG dùng khi chuỗi dưới tám tuần dữ liệu (56 ngày), vì lưới lúc đó chỉ còn vài
    cột, không đủ để mắt nhận ra nhịp lặp lại theo tuần; dùng spc_control_chart
    (viz_eir_stats.py) cho chuỗi ngắn cần phát hiện điểm vượt ngưỡng.
    """
    dates_raw = list(p["dates"]); values_raw = list(map(float, p["values"]))
    if len(dates_raw) != len(values_raw):
        raise ValueError("dates va values phai cung do dai")
    pairs = sorted(zip((dt.date.fromisoformat(s) for s in dates_raw), values_raw),
                   key=lambda pv: pv[0])
    dates = [d for d, _ in pairs]; values = [v for _, v in pairs]

    anchor = dates[0] - dt.timedelta(days=dates[0].weekday())  # Thu 2 dau tien
    week_of, date_of, week_first_date = {}, {}, {}
    for d, v in zip(dates, values):
        wi = (d - anchor).days // 7
        dow = d.weekday()  # 0=T2 .. 6=CN
        week_of[(wi, dow)] = v
        date_of[(wi, dow)] = d
        if wi not in week_first_date or d < week_first_date[wi]:
            week_first_date[wi] = d
    n_weeks = max(week_first_date) + 1

    vals_arr = np.array(list(week_of.values()), float)
    vmin, vmax = float(vals_arr.min()), float(vals_arr.max())
    diverging = vmin < 0 < vmax
    if diverging:
        vabs = max(abs(vmin), abs(vmax)) or 1.0
        norm = Normalize(-vabs, vabs)
        cmap = LinearSegmentedColormap.from_list(
            "eir_cal_div", [BRICK, tint(BRICK, 0.32), PAPER_HI, tint(TEAL, 0.28), TEAL])
    else:
        norm = Normalize(vmin, vmax if vmax > vmin else vmin + 1.0)
        base_hi = accent or TEAL
        cmap = LinearSegmentedColormap.from_list(
            "eir_cal_seq", [PAPER_HI, tint(base_hi, 0.55), base_hi])

    mean_v = float(vals_arr.mean()); std_v = float(vals_arr.std())
    outliers = {}
    if std_v > 0:
        for k, v in week_of.items():
            z = (v - mean_v) / std_v
            if abs(z) > 3.0:
                outliers[k] = z

    # Chieu cao khung phai bam theo SO HANG THAT, khong khai cung.
    #
    # Luoi lich dung `set_aspect("equal")` de o ngay vuong, dung tinh than lich
    # kieu GitHub. Nhung aspect equal cong voi mot rect cao co dinh thi matplotlib
    # tu CO khung lai cho dung ty le roi CAN GIUA phan con lai, nen phan thua bien
    # thanh khoang trang chet o tren va duoi luoi. Voi 15 thang, luoi rong khoang
    # 65 cot va cao 5 hang, tuc ty le trren 13 tren 1: khung vuong chi cao chua toi
    # mot inch trong khi rect cu danh cho no 1,84 inch. Hai phan ba la khoang trong.
    #
    # Hau qua that, khong phai chuyen tham my: khi hinh nay thu ve kho mot cot cua
    # bao cao, o ngay nho toi muc khong doc duoc mau, ma doc mau chinh la toan bo
    # gia tri cua loai chart nay.
    # Tinh bang INCH tuyet doi, khong bang ty le. Lan dau toi sua bang ty le va
    # nen hong: masthead va chu giai deu can mot chieu cao CO DINH tinh bang inch,
    # nen khi tong chieu cao co lai thi phan danh cho chung co theo va chung de len
    # nhau. Ba khoan duoi day cong lai dung bang chieu cao khung.
    # Hai con so nay do bang mat qua ba vong render, khong phai chon bua. Vong dau
    # dat chan 1,01 inch va chu giai de len nhan cua thanh mau, vi ban goc dat rect
    # bottom o 1,01 nhung khung THAT bi aspect equal can giua nen day khung nam cao
    # hon nhieu, tuc chan trang thuc te rong hon con so trong rect.
    CAO_MASTHEAD = 1.55   # kicker, tieu de, phu de, duong ke
    CAO_CHAN = 1.48       # thanh mau, nhan thanh mau, hai dong chu giai, dong nguon
    RONG_FIG = 8.6
    RONG_TRUC = RONG_FIG * 0.92

    so_hang = len({dow for (_, dow) in week_of}) or 7
    # O ngay vuong nen chieu cao luoi suy ra tu chieu rong: mot o rong bang
    # RONG_TRUC / so_cot, va luoi cao bang so_hang o cong le tren duoi.
    cao_luoi = RONG_TRUC * (so_hang + 1.2) / max(n_weeks, 1)
    cao_fig = CAO_MASTHEAD + cao_luoi + CAO_CHAN
    fig, ax = eir_fig(_meta(p, accent), figsize=(RONG_FIG, cao_fig),
                      rect=(0.055, CAO_CHAN / cao_fig, 0.92, cao_luoi / cao_fig))
    ax.set_facecolor(PAPER)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)

    cell = 0.82
    for (wi, dow), v in week_of.items():
        is_out = (wi, dow) in outliers
        ax.add_patch(Rectangle((wi - cell / 2, (6 - dow) - cell / 2), cell, cell,
                               facecolor=cmap(norm(v)),
                               edgecolor=GOLD if is_out else PAPER,
                               linewidth=1.8 if is_out else 0.7,
                               zorder=3 if is_out else 2))
    ax.set_xlim(-0.7, n_weeks - 0.3)
    # Chi ve nhung hang CO du lieu. Ban cu khai cung `set_ylim(-0.6, 6.6)` tuc bay
    # hang, va khai cung nhan `CN` o hang 6. Du lieu chung khoan chi co T2 toi T6,
    # nen nhan CN tro toi mot hang RONG nam duoi day luoi: no dang gan nhan cho mot
    # thu khong ton tai, va nguoi doc se tuong con mot hang chua ve.
    dow_co = sorted({dow for (_, dow) in week_of})
    y_tren = 6 - dow_co[0]
    y_duoi = 6 - dow_co[-1]
    ax.set_ylim(y_duoi - 0.6, y_tren + 0.6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    # Hien nhan cach mot hang de chu khong de nhau, va CHI trong so hang co that.
    NHAN_THU = {0: "T2", 1: "T3", 2: "T4", 3: "T5", 4: "T6", 5: "T7", 6: "CN"}
    hien = dow_co[1::2] or dow_co
    ax.set_yticks([6 - i for i in hien])
    ax.set_yticklabels([NHAN_THU[i] for i in hien], fontsize=7.8, color=MUTED,
                       family=MONO)

    # nhan thang phia tren luoi, bo qua neu qua gan nhan truoc do (kho hep <=1 nam
    # thi cach toi thieu 2 cot, kho rong hon 1 nam thi can toi thieu 4 cot vi moi cot
    # rat hep khi co tren khoang 60 tuan).
    min_gap = 2 if n_weeks <= 60 else 4
    prev_month, last_label_wi = None, -99
    for wi in sorted(week_first_date):
        m = week_first_date[wi].month
        if m != prev_month:
            if wi - last_label_wi >= min_gap:
                ax.annotate(_THANG_VN[m - 1], (wi, 6.85), fontsize=7.6, color=MUTED,
                            family=SANS, ha="left", va="bottom", annotation_clip=False)
                last_label_wi = wi
            prev_month = m

    # danh dau ngay bat thuong nhat bang mot chu thich co mui ten, chi 1 lan de
    # khong roi luoi; cac o bat thuong khac da co vien vang tu vong lap tren.
    if outliers:
        worst_key = max(outliers, key=lambda k: abs(outliers[k]))
        wi, dow = worst_key
        v = week_of[worst_key]; d = date_of[worst_key]
        y_cell = 6 - dow
        va = "bottom" if y_cell <= 3 else "top"
        dy = 16 if va == "bottom" else -16
        ax.annotate(f"{d.isoformat()}\n{_fv(v, dp=2)}", (wi, y_cell), color=GOLD,
                    fontsize=8, fontweight="bold", family=SANS, ha="center", va=va,
                    xytext=(0, dy), textcoords="offset points",
                    arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.1), zorder=6,
                    annotation_clip=False)

    # thanh chu giai gradient: ve bang axvspan tung lat mong, KHONG dung imshow (xem
    # docstring module va CLAUDE.md ve luat vector).
    cax = fig.add_axes([0.055, 0.135, 0.30, 0.018])
    steps = np.linspace(norm.vmin, norm.vmax, 161)
    for k in range(len(steps) - 1):
        cax.axvspan(steps[k], steps[k + 1],
                    color=cmap(norm((steps[k] + steps[k + 1]) / 2)), linewidth=0)
    cax.set_xlim(norm.vmin, norm.vmax); cax.set_ylim(0, 1)
    cax.set_yticks([]); cax.set_xticks([norm.vmin, norm.vmax])
    cax.set_xticklabels([_fv(norm.vmin, dp=1), _fv(norm.vmax, dp=1)], fontsize=7.4,
                        color=MUTED, family=MONO)
    cax.tick_params(length=0)
    for sp in cax.spines.values():
        sp.set_color(GRID); sp.set_linewidth(0.6)
    fig.text(0.055, 0.163, p.get("value_label", "Giá trị mỗi ô"), fontsize=7.8,
             color=MUTED, family=SANS, ha="left")

    _legend_row(fig, [
        ("sq", GRID, "Ô trống: ngày không có dữ liệu"),
        ("sq", tint(GOLD, 0.20), "Viền vàng: bất thường (lệch hơn ba độ lệch chuẩn)"),
    ], y=0.070)
    return fig


# ======================================================================= 3. ecdf
def c_ecdf(p, accent):
    """Đường bậc thang phân phối tích luỹ thực nghiệm (ECDF), không cần chia bin.

    Trả lời: "Một mã đang nằm ở phân vị bao nhiêu so với toàn ngành?" Trục dọc là
    phần trăm quan sát có giá trị nhỏ hơn hoặc bằng trục hoành, đọc trực tiếp mà
    không phải tự chọn bề rộng bin như histogram. Điểm locate (nếu có) được dóng
    bằng đường đứt nét kèm phân vị đọc thẳng ra được.

    Dữ liệu cần: values là một chuỗi giá trị (toàn ngành, toàn rổ so sánh). Tuỳ
    chọn locate là một giá trị cần định vị (ví dụ chỉ tiêu của một mã cụ thể) cùng
    locate_label đặt tên, và x_label cho trục hoành.

    KHÔNG dùng khi mẫu dưới hai mươi quan sát, vì mỗi bậc thang khi đó nhảy hơn năm
    phần trăm phân vị và phóng đại một điểm dữ liệu đơn lẻ thành một bước ngoặt của
    cả đường; dùng distribution (viz_eir_stats.py) khi cần nhìn HÌNH DẠNG mật độ
    thay vì định vị chính xác một điểm.
    """
    vals = np.sort(np.array(p["values"], float))
    n = len(vals)
    if n < 2:
        raise ValueError("ecdf can it nhat 2 quan sat")
    y = np.arange(1, n + 1) / n * 100.0

    fig, ax = eir_fig(_meta(p, accent), figsize=(7.8, 4.8), rect=(0.10, 0.185, 0.83, 0.55))
    despine(ax, keep=("left", "bottom"), grid_axis="y")

    pad = (vals[-1] - vals[0]) * 0.08 or 1.0
    x0, x1 = vals[0] - pad, vals[-1] + pad
    ax.set_xlim(x0, x1); ax.set_ylim(0, 100)

    for q, lab in ((25, "P25"), (50, "P50 (trung vị)"), (75, "P75")):
        ax.axhline(q, color=GRID, lw=0.8, ls=(0, (1, 2)), zorder=1)
        ax.annotate(lab, (x1, q), color=MUTED, fontsize=7.4, family=MONO, ha="right",
                    va="bottom", xytext=(0, 2), textcoords="offset points",
                    annotation_clip=False)

    ax.hlines(0, x0, vals[0], color=NAVY, lw=2.2, zorder=3)
    ax.step(vals, y, where="post", color=NAVY, lw=2.2, zorder=3)
    ax.hlines(100, vals[-1], x1, color=NAVY, lw=2.2, zorder=3)
    if n <= 60:
        ax.scatter(vals, y, s=16, color=NAVY, zorder=4, edgecolor=PAPER, linewidth=0.5)

    locate = p.get("locate")
    pct = None
    if locate is not None:
        lv = float(locate)
        pct = float(np.searchsorted(vals, lv, side="right")) / n * 100.0
        ax.axvline(lv, ymin=0, ymax=pct / 100.0, color=BRICK, ls=(0, (5, 2)), lw=1.8,
                   zorder=5)
        ax.axhline(pct, xmin=(lv - x0) / (x1 - x0), xmax=1.0, color=BRICK,
                   ls=(0, (5, 2)), lw=1.8, zorder=5)
        ax.scatter([lv], [pct], s=90, color=BRICK, zorder=6, edgecolor=PAPER,
                   linewidth=1.4)
        label = p.get("locate_label", "Điểm cần định vị")
        med = float(np.median(vals))
        ax.annotate(f"{label}\nPhân vị {_fv(pct, dp=0)}", (lv, pct), color=BRICK,
                    fontsize=9.4, fontweight="bold", family=SANS,
                    ha="left" if lv < med else "right",
                    va="bottom" if pct < 88 else "top",
                    xytext=(8 if lv < med else -8, 8), textcoords="offset points")

    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: _fv(v, p.get("x_format", "num"),
                                           p.get("currency", "$"), p.get("dp"))))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _fv(v, "pct", dp=0)))
    ax.set_xlabel(p.get("x_label", "Giá trị"), fontsize=9.5, color=INK)
    ax.set_ylabel("Phân vị tích luỹ", fontsize=9.5, color=INK)

    entries = [("line", NAVY, f"Phân phối toàn mẫu (n = {n})")]
    if pct is not None:
        entries.append(("sq", BRICK,
                        f"{p.get('locate_label', 'Điểm cần định vị')}: phân vị {_fv(pct, dp=0)}"))
    _legend_row(fig, entries, y=0.075)
    return fig


COMPONENTS = {
    "drawdown": c_drawdown,
    "calendar_heatmap": c_calendar_heatmap,
    "ecdf": c_ecdf,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec"); ap.add_argument("--out-dir")
    ap.add_argument("--only", default=None); ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    setup_fonts()
    if args.list:
        print("EIR-risk components:", ", ".join(sorted(COMPONENTS))); return 0
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
            sys.stderr.write(f"WARN unknown EIR-risk component '{comp}' (id={fid})\n")
            fail += 1; continue
        try:
            fig = fn(fs.get("params", {}), (fs.get("params", {}).get("accent") or accent))
            out = os.path.join(args.out_dir, f"{module}_{fid}.png")
            save(fig, out, dpi=args.dpi); print(f"RENDERED {out}"); ok += 1
        except Exception as e:
            import traceback; traceback.print_exc()
            sys.stderr.write(f"FAIL id={fid} component={comp}: {e}\n"); fail += 1
    print(f"viz_eir_risk: {ok} rendered, {fail} failed")
    return fail


if __name__ == "__main__":
    sys.exit(main())
