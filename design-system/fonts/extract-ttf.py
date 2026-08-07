#!/usr/bin/env python3
"""extract-ttf.py - trich file .ttf cho matplotlib tu fonts-embedded.css.

VI SAO CAN FILE RIENG: matplotlib doc duoc ttf/otf/ttc, KHONG doc duoc woff2.
Ma toan bo font cua repo dang nam duoi dang woff2 base64 trong
fonts-embedded.css (dinh dang do dung cho HTML, dung cho). Nen duong chart
Python truoc day phai muon font HE THONG o /usr/share/fonts, tuc mot phu thuoc
ngoai repo: may nao thieu Liberation thi chart roi ve DejaVu va nhan tieng Viet
mat dau.

VI SAO TRICH NGUOC CHU KHONG TAI MOI: build-fonts.py tai tu Google Fonts qua
mang. Trich nguoc tu fonts-embedded.css thi chay duoc OFFLINE, va quan trong
hon la lay DUNG bo font da qua kiem chung cua repo (cung subset latin +
vietnamese, cung phien ban), nen ban chart va ban HTML khong the lech font.

Chay lai khi nao: sau khi build-fonts.py sinh lai fonts-embedded.css.

    python3 design-system/fonts/extract-ttf.py

File .ttf sinh ra CO commit vao repo (khac font-cache/ vốn bị git-ignore), vì
đó chính là điểm của việc này: để repo tự đủ, khong phai cai them font he thong.
"""
import base64
import pathlib
import re
import sys

from fontTools.ttLib import TTFont

THU_MUC = pathlib.Path(__file__).resolve().parent
CSS = THU_MUC / "fonts-embedded.css"
DICH = THU_MUC / "ttf"

# Chi trich nhung face matplotlib THAT SU dung, khong trich het 14 face, de
# repo khong phinh vi font khong ai mo toi. Doi chieu voi _SANS/_MONO/_SERIF
# trong charts/matplotlib/_eir_style.py: mot ban thuong va mot ban dam cho moi
# vai tro la du cho nhan, tieu de va so lieu tren chart.
CAN_TRICH = [
    ("IBM Plex Sans", "normal", 400),
    ("IBM Plex Sans", "normal", 600),
    ("IBM Plex Mono", "normal", 400),
    ("IBM Plex Mono", "normal", 600),
    ("Spectral", "normal", 400),
    ("Spectral", "normal", 700),
]


def ten_file(family, style, weight):
    return f"{family.replace(' ', '')}-{weight}{'' if style == 'normal' else '-' + style}.ttf"


def doc_cac_face(css_text):
    """Tra ve dict {(family, style, weight): bytes woff2}."""
    ra = {}
    for khoi in re.findall(r"@font-face\{(.*?)\}", css_text, re.S):
        fam = re.search(r"font-family:'([^']+)'", khoi)
        sty = re.search(r"font-style:([a-z]+)", khoi)
        wei = re.search(r"font-weight:(\d+)", khoi)
        src = re.search(r"base64,([A-Za-z0-9+/=]+)", khoi)
        if not (fam and sty and wei and src):
            continue
        ra[(fam.group(1), sty.group(1), int(wei.group(1)))] = base64.b64decode(src.group(1))
    return ra


def main():
    if not CSS.exists():
        print(f"khong thay {CSS}", file=sys.stderr)
        return 2
    cac_face = doc_cac_face(CSS.read_text(encoding="utf-8"))
    if not cac_face:
        print("khong doc duoc @font-face nao tu CSS", file=sys.stderr)
        return 2

    DICH.mkdir(exist_ok=True)
    thieu = [k for k in CAN_TRICH if k not in cac_face]
    if thieu:
        print(f"CSS khong co cac face sau: {thieu}", file=sys.stderr)
        return 1

    for khoa in CAN_TRICH:
        family, style, weight = khoa
        tam = DICH / "._tam.woff2"
        tam.write_bytes(cac_face[khoa])
        font = TTFont(tam)
        font.flavor = None  # bo nen woff2, ghi ra ttf tran
        ep_ten_ho(font, family, weight)
        dich = DICH / ten_file(family, style, weight)
        font.save(dich)
        font.close()
        tam.unlink()
        print(f"{dich.name}: {dich.stat().st_size // 1024} KB  (ho '{family}', weight {weight})")
    return 0


def ep_ten_ho(font, family, weight):
    """Ep nameID 1 va 16 ve DUNG ten ho, vd 'IBM Plex Sans'.

    Google Fonts dat ten ho cua ban 600 la 'IBM Plex Sans SemiBold', tuc mot
    HO KHAC chu khong phai mot cap dam cua 'IBM Plex Sans'. Trich nguyen xi thi
    matplotlib dang ky hai ho roi rac, va khi chart xin ban dam cua
    'IBM Plex Sans' no khong tim thay -> tu to gia (synthetic bold) hoac roi ve
    font khac. Da do that: fontManager liet ke 'IBM Plex Sans' va
    'IBM Plex Sans SemiBold' nhu hai dong doc lap.
    matplotlib chon face theo (ho, weight), nen chi can hai file CUNG TEN HO va
    khac usWeightClass la du. Giu nguyen usWeightClass, chi sua ten.
    Spectral khong dinh loi nay vi Google dat ca hai ban duoi cung ten 'Spectral'.
    """
    kieu = "Bold" if weight >= 600 else "Regular"
    for ban_ghi in font["name"].names:
        if ban_ghi.nameID == 1 or ban_ghi.nameID == 16:
            ban_ghi.string = family
        elif ban_ghi.nameID == 2 or ban_ghi.nameID == 17:
            ban_ghi.string = kieu
        elif ban_ghi.nameID == 4:  # ten day du
            ban_ghi.string = f"{family} {kieu}"


if __name__ == "__main__":
    raise SystemExit(main())
