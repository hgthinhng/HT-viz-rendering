#!/usr/bin/env python3
"""02-bien-loi-nhuan.py — khoang cach bien loi nhuan giua cac doanh nghiep trong nganh.

Chart cua BAO CAO, dung component `dumbbell` cua thu vien EIR. Xuat .svg chu khong
phai .png: `save()` tu ep `svg.fonttype='none'` khi duoi la .svg, nen chu van la
<text> that trong ban PDF, doc duoc, chon duoc, va khong bien thanh anh raster.

Ten doanh nghiep de la DN A toi DN F chu khong dung ma chung khoan that. So trong
file nay la so minh hoa; gan so minh hoa vao mot ma that la tao ra mot khang dinh
sai ve mot doanh nghiep co that.
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(GOC / "charts/matplotlib"))
sys.path.insert(0, str(GOC / "design-system"))

import _eir_style as S  # noqa: E402
from tokens import COLORS  # noqa: E402
from viz_super import COMPONENTS  # noqa: E402

S.setup_fonts()

# Accent phai lay tu token cua repo, KHONG dung S.TEAL. Thu vien EIR mang accent teal
# rieng cua no; bao cao dung teal thi chart matplotlib va chart ECharts trong cung mot
# trang ra hai he mau khac nhau. Da nhin tan mat tren ban PDF dau tien cua Phase 2:
# cham xanh teal o trang 4 canh cot xanh #2251FF o trang 2.
ACCENT = COLORS["accent"]

THAM_SO = {
    "kicker": "So sánh doanh nghiệp",
    "title": "Khoảng cách biên lợi nhuận giữa nhóm dẫn đầu và nhóm cuối rộng gấp bốn lần",
    "subtitle": "Biên lợi nhuận trước thuế theo doanh nghiệp, %",
    "source": "Số minh hoạ cho mẫu kỹ thuật",
    "asof": "31/12/2025",
    "categories": ["DN A", "DN B", "DN C", "DN D", "DN E", "DN F"],
    "before": [15.1, 12.4, 10.8, 8.2, 6.9, 5.4],
    "after": [18.6, 13.9, 11.2, 7.4, 5.8, 4.2],
    "left_name": "2024",
    "right_name": "2025",
    "sort": "after",
    "y_format": "pct",
    "dp": 1,
}


def main() -> int:
    ve = COMPONENTS["dumbbell"]
    fig = ve(THAM_SO, ACCENT)
    ra = Path(__file__).resolve().parent / "ra-02-bien-loi-nhuan.svg"
    S.save(fig, str(ra))
    print(f"02-bien-loi-nhuan: OK, {ra.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
