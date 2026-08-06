import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EIR = ROOT / "charts" / "matplotlib"

_HEX_RE = re.compile(r'"#[0-9A-Fa-f]{6}"')

# File duoc PHEP giu dinh nghia mau: day la nguon token DUY NHAT cho toan bo
# thu vien EIR, noi vao design-system/tokens.py (F2), va la noi dat cac ham
# dan xuat tint()/shade() (F6). Moi file khac phai dung ten hang so import tu
# day (PAPER, INK, TEAL, ...) hoac goi tint()/shade(), khong duoc tu che hex.
_ALLOWED_FILES = {"_eir_style.py"}

# File duoc MIEN TAM THOI, khong phai vi hex cua no hop le ve mat thiet ke, ma
# vi ban than FILE nay dang treo cho controller quyet dinh giu hay xoa (F6).
# viz_render_py.py tu nhan trong docstring cua chinh no la thuoc mot pipeline
# KHAC ("note-pipeline-viz"), KHONG import _eir_style, va khong file/test/
# script nao trong repo nay goi no (da grep xac nhan: chi co dong tu-tham-chieu
# va mot dong comment trong viz_super.py TRO SANG duong dan
# note-pipeline-viz/scripts/viz_render_py.py, thu muc do khong ton tai trong
# repo nay). No nhieu kha nang la san pham con sot cua lenh `cp -r` Step 3 chep
# nguyen thu muc harvest, khong phai thanh vien that su cua thu vien EIR. Neu
# controller quyet giu no lai trong charts/matplotlib/, phai xu ly 17 hex tran
# cua no va go mien nay.
_ORPHAN_FILES_PENDING_DECISION = {"viz_render_py.py"}


def test_khong_file_eir_nao_hardcode_hex_tran():
    """Bang mau GIAY NGA AM da bi bac (ba nguon doc lap hoi tu vao TRANG LANH,
    xem CLAUDE.md) tung ro ri qua 37 hex tran hardcode rai rac ngoai
    _eir_style.py (F6: TINT/CARD_BG cua viz_eir_panels.py, node fill cua
    viz_eir_diagram.py, colormap cua viz_eir.py/viz_eir_stats.py, v.v.). Test
    nay quet MOI file .py trong charts/matplotlib/ (tru danh sach trang tuong
    minh o tren) tim chuoi hex hardcode dang "#RRGGBB" va FAIL neu con, chi
    dung ten file:dong de lan sau ai cham vao biet ngay hong o dau."""
    offenders = []
    for f in sorted(EIR.glob("*.py")):
        if f.name in _ALLOWED_FILES or f.name in _ORPHAN_FILES_PENDING_DECISION:
            continue
        src = f.read_text(encoding="utf-8")
        for i, line in enumerate(src.splitlines(), start=1):
            if _HEX_RE.search(line):
                offenders.append(f"{f.name}:{i}: {line.strip()}")
    assert not offenders, (
        "Con hex tran hardcode ngoai _eir_style.py. Moi mau phai di qua token "
        "trong design-system/tokens.py: dung truc tiep ten hang so da import "
        "(PAPER, INK, TEAL, BRICK, GOLD, INDIGO, MUTED, FAINT, GRID, PAPER_HI) "
        "hoac dan xuat qua tint()/shade() trong _eir_style.py, khong duoc tu "
        "che them hex moi. Cac dong vi pham:\n" + "\n".join(offenders)
    )


def test_danh_sach_trang_khong_rong_bi_lang_quen():
    """Bao ve chinh danh sach trang: neu ai do xoa/doi ten
    _ORPHAN_FILES_PENDING_DECISION ma khong go het hex trong viz_render_py.py
    truoc, test tren se tu FAIL dung cho (khong can test rieng). Test nay chi
    dam bao danh sach trang khong am tham phinh to thanh mot regex rong lach
    luat: moi file trong do phai duoc liet ke TUONG MINH bang ten, khong dung
    wildcard/regex."""
    assert _ALLOWED_FILES == {"_eir_style.py"}
    assert _ORPHAN_FILES_PENDING_DECISION == {"viz_render_py.py"}
