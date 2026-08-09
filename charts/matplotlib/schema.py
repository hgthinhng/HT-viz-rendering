"""schema.py - ban Python cua lop schema du lieu chart.

PHAI giu CUNG TEN TRUONG va CUNG MA LOI voi charts/echarts/schema.mjs. Hai file cung
doc mot tu vung (charts/schema.vocab.json) va cung chay mot bo fixture vang
(charts/fixtures/schema-cases.json), nen khi mot ben doi luat ma ben kia quen thi test
do ngay.

Vi sao khong sinh ma tu dong tu mot dinh nghia chung: voi vai tram dong schema, duong
ong sinh ma ton cong bao tri hon chinh schema, va khi no hong thi nguoi phai sua la
nguoi khong hieu no. Ba mo hinh ngoai deu khuyen cung mot huong: tu vung tach ra file
du lieu, luat viet tay hai lan, va khoa hai ban bang fixture chung.

Vi sao khong dung JSON Schema chuan: no dien ta tot cau truc (kieu, enum, bat buoc)
nhung dien ta rat te luat lien-hang, vi du "co phai tinh tu chi so nguyen" hay "ba
trang thai thieu deu phai de value la null". Phan de troi dat nhat van phai viet tay
hai lan, doi lai them mot phu thuoc thu vien o moi phia.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_HERE = Path(__file__).resolve().parent
VOCAB_PATH = _HERE.parent / "schema.vocab.json"

with VOCAB_PATH.open(encoding="utf-8") as f:
    VOCAB = json.load(f)

SCHEMA_VERSION = VOCAB["schema_version"]

#: Do dai toi da cua entity.code. Khong ep viet hoa, khong ep bo dau, chi ep NGAN.
#: Xem ly do day du trong schema.mjs: ep viet hoa khong dau lam hong du lieu that,
#: vi phan khuc kinh doanh va ten chinh sach khong co ma tu nhien.
MAX_CODE_LEN = 24

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ERR:
    """Ma loi ON DINH, doi chieu bang ma chu khong bang cau chu tieng Viet."""

    THIEU_UNIT = "THIEU_UNIT"
    UNIT_LA = "UNIT_LA"
    THIEU_SOURCE = "THIEU_SOURCE"
    TIER_LA = "TIER_LA"
    DIRECTION_LA = "DIRECTION_LA"
    KIND_LA = "KIND_LA"
    ROLE_LA = "ROLE_LA"
    STATUS_LA = "STATUS_LA"
    THIEU_CODE = "THIEU_CODE"
    CODE_QUA_DAI = "CODE_QUA_DAI"
    VALUE_SAI_KIEU = "VALUE_SAI_KIEU"
    VALUE_PHAI_NULL = "VALUE_PHAI_NULL"
    VALUE_KHONG_DUOC_NULL = "VALUE_KHONG_DUOC_NULL"
    PERIOD_TYPE_LA = "PERIOD_TYPE_LA"
    THIEU_PERIOD_END = "THIEU_PERIOD_END"
    PERIOD_END_SAI_DINH_DANG = "PERIOD_END_SAI_DINH_DANG"
    THIEU_QUY = "THIEU_QUY"
    QUY_NGOAI_PHAM_VI = "QUY_NGOAI_PHAM_VI"
    THIEU_NAM = "THIEU_NAM"
    DECIMALS_SAI = "DECIMALS_SAI"
    CHI_SO_NGOAI_PHAM_VI = "CHI_SO_NGOAI_PHAM_VI"
    DO_TIN_CAY_LA = "DO_TIN_CAY_LA"
    DO_TIN_CAY_SAI_CAP = "DO_TIN_CAY_SAI_CAP"


class LoiSchema(Exception):
    """Loi vi pham schema, mang theo ma on dinh o thuoc tinh `ma`."""

    def __init__(self, ma: str, chi_tiet: str):
        super().__init__(f"{ma}: {chi_tiet}")
        self.ma = ma


def _trong_tu_vung(nhom: str, gia_tri) -> bool:
    return gia_tri in VOCAB[nhom]


def validate_series(series) -> bool:
    """Kiem MOT series: mot luot xep hang, mot duong, mot bo diem cung don vi.

    Don vi, nguon, so chu so thap phan, chieu tot xau va loai so lieu deu o cap SERIES
    chu khong o tung hang. Chinh ham kiem "khong tron don vi" da to giac dieu do: neu
    tron don vi trong mot luot xep hang la loi, thi don vi la thuoc tinh cua luot xep
    hang chu khong phai cua hang.
    """
    if not isinstance(series, dict):
        raise LoiSchema(ERR.THIEU_UNIT, "series khong phai doi tuong")
    if not series.get("unit"):
        raise LoiSchema(ERR.THIEU_UNIT, "series thieu unit")
    if not _trong_tu_vung("unit", series["unit"]):
        raise LoiSchema(
            ERR.UNIT_LA,
            f'"{series["unit"]}" khong nam trong tu vung. Them vao charts/schema.vocab.json '
            "truoc, dung tu che chuoi moi trong preset",
        )
    source = series.get("source") or {}
    if not source.get("tier"):
        raise LoiSchema(ERR.THIEU_SOURCE, "series thieu source.tier")
    if not _trong_tu_vung("source_tier", source["tier"]):
        raise LoiSchema(ERR.TIER_LA, f'tier "{source["tier"]}" khong nam trong tu vung')

    if "direction" in series and not _trong_tu_vung("direction", series["direction"]):
        raise LoiSchema(ERR.DIRECTION_LA, f'direction "{series["direction"]}" khong nam trong tu vung')
    if "kind" in series and not _trong_tu_vung("kind", series["kind"]):
        raise LoiSchema(ERR.KIND_LA, f'kind "{series["kind"]}" khong nam trong tu vung')
    if "decimals" in series:
        d = series["decimals"]
        if not isinstance(d, int) or isinstance(d, bool) or d < 0 or d > 6:
            raise LoiSchema(ERR.DECIMALS_SAI, f"decimals phai la so nguyen 0 toi 6, dang la {d}")
    # `do_tin_cay` thuoc cap DIEM, khong thuoc cap series. Chan tuong minh chu khong im
    # lang bo qua: dat nham cap thi ca duong cong mang mot do tin cay duy nhat, dung thu
    # ma truong nay sinh ra de tranh.
    if "do_tin_cay" in series:
        raise LoiSchema(
            ERR.DO_TIN_CAY_SAI_CAP,
            "do_tin_cay thuoc cap TUNG DIEM chu khong phai cap series. "
            "Bac cua ca series la source.tier",
        )

    for i, row in enumerate(series.get("rows") or []):
        validate_row(row, i)
    return True


def ep_don_vi(series, duoc_phep):
    """Ban Python cua epDonVi() ben JS. Giu CUNG ma loi UNIT_LA.

    Xem chu thich day du o charts/echarts/schema.mjs. Tom tat: mot preset dong cung don vi
    trong ham dinh dang thi phai noi thang no lam duoc gi, thay vi khai `unit` roi phot lo.
    """
    if series.get("unit") not in duoc_phep:
        raise LoiSchema(
            ERR["UNIT_LA"],
            f'preset nay chi ve dung duoc don vi {", ".join(duoc_phep)}, '
            f'nhan duoc "{series.get("unit")}"',
        )
    return True


def validate_row(row, chi_so: int = 0) -> bool:
    """Kiem MOT hang quan sat."""
    o = f"hang #{chi_so}"
    if not isinstance(row, dict):
        raise LoiSchema(ERR.THIEU_CODE, f"{o} khong phai doi tuong")

    if "entity" in row:
        entity = row["entity"] or {}
        if not entity.get("code"):
            raise LoiSchema(ERR.THIEU_CODE, f"{o} co entity nhung thieu entity.code")
        if len(str(entity["code"])) > MAX_CODE_LEN:
            raise LoiSchema(
                ERR.CODE_QUA_DAI,
                f"{o} entity.code dai {len(str(entity['code']))} ky tu, toi da {MAX_CODE_LEN}. "
                "Rut gon o tang du lieu, dung de nhan dai len truc",
            )

    status = row.get("status", "co_that")
    if not _trong_tu_vung("status", status):
        raise LoiSchema(ERR.STATUS_LA, f'{o} status "{status}" khong nam trong tu vung')

    value = row.get("value")
    if status == "co_that":
        # bool la subclass cua int trong Python, phai loai tuong minh, neu khong
        # True se lot qua nhu so 1 va tao ra mot diem du lieu vo nghia.
        hop_le = isinstance(value, (int, float)) and not isinstance(value, bool)
        if hop_le:
            hop_le = value == value and value not in (float("inf"), float("-inf"))
        if not hop_le:
            raise LoiSchema(
                ERR.VALUE_KHONG_DUOC_NULL,
                f"{o} status co_that thi value phai la so huu han, dang la {value!r}",
            )
    elif value is not None:
        # Ba trang thai thieu deu phai de value la null. Neu de so cu o do, mot ngay
        # nao do co nguoi loc theo value thay vi theo status va so bi loai se song lai.
        raise LoiSchema(
            ERR.VALUE_PHAI_NULL,
            f'{o} status "{status}" thi value phai la null, dang giu {value!r}',
        )

    if "role" in row and not _trong_tu_vung("role", row["role"]):
        raise LoiSchema(ERR.ROLE_LA, f'{o} role "{row["role"]}" khong nam trong tu vung')

    # `do_tin_cay` la do tin cay cua CHINH DIEM NAY, khac han `source.tier` la bac cua ca
    # series. Ho duong cong can no: mot duong lai suat that tron ca ky han thanh khoan cao
    # (quan sat truc tiep) lan ky han thua (dealer bao gia hoac noi suy), trong khi ca
    # duong van la MOT nguon o cap series. Truoc khi co truong nay, viz_eir_curves.py phai
    # tai dung `source_tier` o cap diem, va khi do doc mot diem thi khong biet no dang noi
    # ve nguon cua ca duong hay ve chinh no.
    if "do_tin_cay" in row and not _trong_tu_vung("do_tin_cay", row["do_tin_cay"]):
        hop_le = ", ".join(VOCAB["do_tin_cay"])
        raise LoiSchema(
            ERR.DO_TIN_CAY_LA,
            f'{o} do_tin_cay "{row["do_tin_cay"]}" khong nam trong tu vung ({hop_le})',
        )
    if "period" in row:
        validate_period(row["period"], o)
    return True


def validate_period(period, o: str = "period") -> bool:
    """Ky bao cao. BAT BUOC co `end` dang ISO, khong chi co quy va nam.

    Ly do: doanh nghiep Viet Nam co nam tai chinh lech (ket thuc 30/6 hoac 31/3 ton tai
    that), nen "Quy 1" cua hai doanh nghiep co the khong trung nhau. Truc thoi gian chi
    ghi "Q1" thi bang so sanh nganh sai ma khong ai phat hien.
    """
    if not isinstance(period, dict) or not _trong_tu_vung("period_type", period.get("type")):
        loai = period.get("type") if isinstance(period, dict) else None
        raise LoiSchema(ERR.PERIOD_TYPE_LA, f'{o} period.type "{loai}" khong nam trong tu vung')
    if not period.get("end"):
        raise LoiSchema(ERR.THIEU_PERIOD_END, f"{o} thieu period.end dang YYYY-MM-DD")
    if not _ISO_DATE.match(period["end"]):
        raise LoiSchema(
            ERR.PERIOD_END_SAI_DINH_DANG, f'{o} period.end "{period["end"]}" phai dang YYYY-MM-DD'
        )
    if period["type"] == "quy":
        if "q" not in period:
            raise LoiSchema(ERR.THIEU_QUY, f"{o} period.type quy thi phai co q")
        q = period["q"]
        if not isinstance(q, int) or isinstance(q, bool) or q < 1 or q > 4:
            raise LoiSchema(ERR.QUY_NGOAI_PHAM_VI, f"{o} q phai la so nguyen 1 toi 4, dang la {q}")
    if period["type"] in ("quy", "nam"):
        year = period.get("year")
        if not isinstance(year, int) or isinstance(year, bool):
            raise LoiSchema(ERR.THIEU_NAM, f"{o} thieu year dang so nguyen")
    return True


def co_co(chi_so_can_danh_dau: int, tong_so_hang: int):
    """Co tinh tu CHI SO NGUYEN, khong so sanh gia tri so thuc.

    So sanh float de tim base case hay ngoai le la nguon loi im lang: hai gia tri bang
    nhau ve mat kinh te van khac nhau o chu so thu muoi lam.
    """
    if (
        not isinstance(chi_so_can_danh_dau, int)
        or isinstance(chi_so_can_danh_dau, bool)
        or chi_so_can_danh_dau < 0
        or chi_so_can_danh_dau >= tong_so_hang
    ):
        raise LoiSchema(
            ERR.CHI_SO_NGOAI_PHAM_VI,
            f"chi so {chi_so_can_danh_dau} nam ngoai pham vi 0 toi {tong_so_hang - 1}",
        )
    return lambda i: i == chi_so_can_danh_dau


def so_thap_phan(series) -> int:
    """So chu so thap phan cho mot series.

    CA HAI engine phai goi ham nay thay vi tu chon, neu khong ban HTML hien 15,45% con
    ban PDF hien 15,5%. Do la dung loai lech ma lop schema sinh ra de ngan.
    """
    if "decimals" in series:
        return series["decimals"]
    return VOCAB["unit"][series["unit"]]["decimals"]


def cach_ve(status: str | None = None) -> dict:
    """Cach ve ung voi tung trang thai, mo ta thuan du lieu, khong phu thuoc engine."""
    s = status or "co_that"
    if not _trong_tu_vung("status", s):
        raise LoiSchema(ERR.STATUS_LA, f'status "{s}" khong nam trong tu vung')
    return {
        "co_that": {"ve_diem": True, "noi_duong": True, "danh_dau_truc": None},
        "chua_cong_bo": {"ve_diem": False, "noi_duong": False, "danh_dau_truc": "chua_cong_bo"},
        "khong_ton_tai": {"ve_diem": False, "noi_duong": False, "danh_dau_truc": None},
        "loai_bat_thuong": {"ve_diem": False, "noi_duong": False, "danh_dau_truc": "da_loai"},
    }[s]


def nhan_don_vi(unit: str) -> str:
    """Nhan don vi de in duoi truc hoac trong tieu de phu."""
    if not _trong_tu_vung("unit", unit):
        raise LoiSchema(ERR.UNIT_LA, f'unit "{unit}" khong nam trong tu vung')
    return VOCAB["unit"][unit]["nhan"]
