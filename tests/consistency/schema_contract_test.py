"""Phia Python cua hop dong schema.

Ban Node doi xung o tests/consistency/schema_contract.test.mjs, CHAY CUNG MOT FILE
FIXTURE (charts/fixtures/schema-cases.json). Khi mot ben doi luat ma ben kia quen, mot
trong hai bo test do ngay.

Doi chieu bang MA LOI chu khong bang cau chu tieng Viet.
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "charts" / "matplotlib"))

from schema import (  # noqa: E402
    ERR,
    LoiSchema,
    SCHEMA_VERSION,
    VOCAB,
    cach_ve,
    co_co,
    so_thap_phan,
    validate_period,
    validate_row,
    validate_series,
)

with (ROOT / "charts" / "fixtures" / "schema-cases.json").open(encoding="utf-8") as f:
    FIXTURE = json.load(f)

CHAY = {
    "series": validate_series,
    "row": lambda d: validate_row(d, 0),
    "period": validate_period,
}


def test_moi_ca_trong_fixture_vang_cho_dung_ket_qua():
    hong = []
    for ca in FIXTURE["cases"]:
        chay = CHAY.get(ca["loai"])
        assert chay is not None, f'ca "{ca["ten"]}" co loai "{ca["loai"]}" khong ai xu ly'
        if ca["mong_doi"] == "pass":
            try:
                chay(ca["du_lieu"])
            except LoiSchema as e:
                hong.append(f'"{ca["ten"]}": mong doi PASS nhung nem {e.ma}')
        else:
            da_nem = None
            try:
                chay(ca["du_lieu"])
            except LoiSchema as e:
                da_nem = e.ma
            if da_nem is None:
                hong.append(f'"{ca["ten"]}": mong doi FAIL voi {ca["ma_loi"]} nhung PASS')
            elif da_nem != ca["ma_loi"]:
                hong.append(f'"{ca["ten"]}": mong doi {ca["ma_loi"]} nhung nem {da_nem}')
    assert not hong, f"{len(hong)} ca lech hop dong:\n" + "\n".join(hong)


def test_bo_ca_phu_het_ma_loi_da_khai():
    ma_duoc_kiem = {c["ma_loi"] for c in FIXTURE["cases"] if c.get("ma_loi")}
    # Hai ma nay khong den tu du lieu dau vao ma tu loi lap trinh trong preset.
    mien_tru = {"VALUE_SAI_KIEU", "CHI_SO_NGOAI_PHAM_VI"}
    tat_ca = {v for k, v in vars(ERR).items() if not k.startswith("_") and isinstance(v, str)}
    thieu = sorted(tat_ca - ma_duoc_kiem - mien_tru)
    assert not thieu, (
        f"cac ma loi sau chua co ca fixture nao kiem: {', '.join(thieu)}. "
        "Them ca vao charts/fixtures/schema-cases.json"
    )


def test_ma_loi_hai_ban_trung_khop():
    """Kiem doi xung: moi ma ben Python phai co ben Node va nguoc lai.

    Doc thang file schema.mjs bang van ban thay vi chay Node, de test nay khong phu
    thuoc vao viec co Node trong moi truong chay pytest.
    """
    mjs = (ROOT / "charts" / "echarts" / "schema.mjs").read_text(encoding="utf-8")
    py_ma = {v for k, v in vars(ERR).items() if not k.startswith("_") and isinstance(v, str)}
    thieu_ben_node = sorted(m for m in py_ma if f"{m}: '{m}'" not in mjs)
    assert not thieu_ben_node, (
        f"ma loi co ben Python nhung khong thay ben Node: {', '.join(thieu_ben_node)}"
    )


def test_so_thap_phan_lay_tu_tu_vung():
    assert so_thap_phan({"unit": "ty_dong"}) == 0
    assert so_thap_phan({"unit": "phan_tram"}) == 1
    assert so_thap_phan({"unit": "phan_tram", "decimals": 2}) == 2


def test_cach_ve_phan_biet_du_ba_loai_gia_tri_thieu():
    dau_hieu = [
        cach_ve("chua_cong_bo")["danh_dau_truc"],
        cach_ve("khong_ton_tai")["danh_dau_truc"],
        cach_ve("loai_bat_thuong")["danh_dau_truc"],
    ]
    assert len(set(map(str, dau_hieu))) == 3, (
        f"ba trang thai thieu phai co ba dau hieu khac nhau, dang la {dau_hieu}"
    )
    assert cach_ve("co_that")["noi_duong"] is True


def test_co_tinh_tu_chi_so_nguyen():
    la_base = co_co(2, 5)
    assert la_base(2) is True
    assert la_base(3) is False
    with pytest.raises(LoiSchema) as e1:
        co_co(5, 5)
    assert e1.value.ma == ERR.CHI_SO_NGOAI_PHAM_VI
    with pytest.raises(LoiSchema) as e2:
        co_co(True, 5)  # bool la subclass cua int, phai bi chan tuong minh
    assert e2.value.ma == ERR.CHI_SO_NGOAI_PHAM_VI


def test_tu_vung_va_phien_ban():
    assert SCHEMA_VERSION.count(".") == 2
    assert len(VOCAB["unit"]) >= 8
    for ten, mo in VOCAB["unit"].items():
        assert isinstance(mo["decimals"], int), f"don vi {ten} thieu decimals mac dinh"
        assert mo["nhan"], f"don vi {ten} thieu nhan hien thi"
