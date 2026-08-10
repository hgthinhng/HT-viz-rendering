#!/usr/bin/env python3
"""gia.py, fixture chart matplotlib danh cho test vi pham loai hinh cua tang phong-cach.

Ton tai DE bi CAM: fixture noi-dung.md canh no khai mot phong-cach co
gioi_han_loai_hinh chua "matplotlib" (Task 10, style nhung-toi), va orchestrator phai
DUNG truoc khi chay file .py nay. Khong duoc xoa chi vi no "khong dung toi" trong
lan chay binh thuong, no chinh la dieu kien de test chung minh gate that su chan.
"""
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(GOC / "charts/matplotlib"))
sys.path.insert(0, str(GOC / "design-system"))

import _eir_style as S  # noqa: E402
from tokens import COLORS  # noqa: E402
from viz_super import COMPONENTS  # noqa: E402

S.setup_fonts()

ACCENT = COLORS["accent"]

THAM_SO = {
    "kicker": "Fixture vi pham loai hinh",
    "title": "Chart nay khong duoc phep chay o phong-cach cam matplotlib",
    "subtitle": "Du lieu minh hoa cho test orchestrator",
    "source": "Fixture cho test",
    "asof": "10/08/2026",
    "categories": ["A", "B", "C"],
    "before": [10.0, 8.0, 6.0],
    "after": [12.0, 9.0, 5.0],
    "left_name": "Truoc",
    "right_name": "Sau",
    "sort": "after",
    "y_format": "pct",
    "dp": 1,
}


def main() -> int:
    ve = COMPONENTS["dumbbell"]
    fig = ve(THAM_SO, ACCENT)
    ra = Path(__file__).resolve().parent / "ra-gia.svg"
    S.save(fig, str(ra))
    print(f"gia: OK, {ra.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
