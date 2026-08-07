#!/usr/bin/env python3
"""sinh_xem_truoc.py, render ban xem truoc SVG cho component matplotlib.

    python3 scripts/sinh_xem_truoc.py

Component matplotlib chi ton tai duoi dang HAM, khong co file hinh nao nam san tren dia,
nen chung khong len duoc contact sheet. Script nay chay chung mot lan bang bo tham so vi
du trong `charts/matplotlib/spec_showcase.json` roi ghi ra `catalog/xem-truoc/*.svg`.

Xuat SVG chu khong phai PNG, va do khong phai chuyen so thich: contact sheet duoc render
tiep qua WeasyPrint, ma luat cung cua repo la ban in phai la vector, dem `/Subtype /Image`
phai bang 0. Mot thumbnail PNG se pha dung phep dem do.

Component nao khong co trong spec_showcase thi khong duoc render, va contact sheet liet ke
thang ten chung. Bia mot bo tham so vi du chi de co hinh se cho ra mot thumbnail khong
phan anh cach component do duoc dung that.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RA = REPO / "catalog/xem-truoc"

sys.path.insert(0, str(REPO / "charts/matplotlib"))
sys.path.insert(0, str(REPO / "design-system"))


def main() -> int:
    import _eir_style as S
    from tokens import COLORS
    from viz_super import COMPONENTS

    S.setup_fonts()
    accent = COLORS["accent"]

    spec = json.loads((REPO / "charts/matplotlib/spec_showcase.json").read_text(encoding="utf-8"))
    RA.mkdir(parents=True, exist_ok=True)

    ok = hong = 0
    for hinh in spec.get("figures", []):
        ten = hinh.get("component")
        ve = COMPONENTS.get(ten)
        if ve is None:
            print(f"  bo qua {ten}: khong co trong COMPONENTS", file=sys.stderr)
            hong += 1
            continue
        try:
            fig = ve(hinh.get("params", {}), accent)
            duong = RA / f"{ten}.svg"
            S.save(fig, str(duong))
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {ten}: {e}", file=sys.stderr)
            hong += 1

    print(f"xem truoc OK: {ok} component, {hong} hong -> {RA.relative_to(REPO)}/")
    return 1 if hong else 0


if __name__ == "__main__":
    raise SystemExit(main())
