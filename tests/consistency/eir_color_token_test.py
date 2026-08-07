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

# Danh sach mien tam thoi, gio RONG. Truoc day no chua viz_render_py.py, mot
# file mo coi cho quyet dinh giu hay xoa. Nguoi dung da quyet XOA (dot don sau
# Phase 1): file mang bang mau giay nga am da bi bac, khong file nao trong repo
# import no, va ban goc van con o
# _harvest/harvest-cfa-skillchain/viz-engine/viz_render_py.py neu can port lai
# 10 primitive loi sang bang mau lanh.
#
# Giu bien nay lai (rong) thay vi xoa han, vi no la CHO DAT dung nghia cho lan
# sau co file cho quyet dinh, va vi test ben duoi ep moi ten trong danh sach
# phai TON TAI THAT tren dia. Mot mien tru tro toi file da bien mat la mien tru
# chet: no khong con che gi, nhung doc vao thi tuong repo van con no.
_ORPHAN_FILES_PENDING_DECISION = set()


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
    """Bao ve chinh danh sach trang, hai chieu.

    Chieu 1 (da co tu truoc): danh sach khong duoc am tham phinh to thanh mot
    regex rong lach luat, moi file phai liet ke TUONG MINH bang ten.

    Chieu 2 (them o dot don sau Phase 1): moi ten trong danh sach phai TON TAI
    THAT trong charts/matplotlib/. Truoc do danh sach van giu ten
    viz_render_py.py sau khi file bi xoa, va khong phep kiem nao do duoc, vi ca
    hai test deu chi so bang voi mot hang so cung ghi trong chinh file test.
    """
    assert _ALLOWED_FILES == {"_eir_style.py"}
    assert _ORPHAN_FILES_PENDING_DECISION == set()

    co_that = {f.name for f in EIR.glob("*.py")}
    mien_tru_chet = (_ALLOWED_FILES | _ORPHAN_FILES_PENDING_DECISION) - co_that
    assert not mien_tru_chet, (
        f"danh sach trang tro toi file khong con ton tai: {sorted(mien_tru_chet)}. "
        "Xoa ten do khoi danh sach, dung de mien tru chet nam lai."
    )
