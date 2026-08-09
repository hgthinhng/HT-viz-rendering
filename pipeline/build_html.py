#!/usr/bin/env python3
"""build_html.py, tu markdown va so nguon, dung ra MOT file HTML tu du.

Cach dung:
    python3 pipeline/build_html.py <noi-dung.md> <ra.html> [--che-do=noi-bo|gui-di]

Dau ra la mot file duy nhat: font nhung base64, CSS nhung thang, chart va minh hoa
nhung inline. Khong mot tham chieu nao ra ngoai file. Do la dieu kien de WeasyPrint
render duoc ma khong phu thuoc may dang chay, va de file gui khach mo duoc o may
khong co gi.

## Hai che do xuat, va vi sao khong duoc gop

`noi-bo`  nhung nguyen so nguon vao `<script id="evidence-ledger">`, danh muc nguon
          hien ten to chuc va trich dan day du. Day la ban de kiem, validator ledger
          chay tren ban nay.
`gui-di`  KHONG nhung so nguon, va nguon `internal_only` chi hien `public_label`.
          Nhung so nguon vao ban gui khach la tu dua ten co quan va kenh tin ra ngoai
          trong mot the script ma nguoi doc khong thay nhung `Ctrl+U` thi thay.

## Bon thu tac gia viet trong file markdown

1. Front-matter giua hai dong `---`, dang `khoa: gia tri`.
2. Markdown thuong: tieu de, doan, danh sach, bang, trich dan, duong ke.
3. Directive mot dong, mo bang `::: `:
       ::: chart src=... id=... chu="..." nguon=K1
       ::: minh-hoa src=... id=... chu="..." nguon=K2
       ::: ngat-trang
4. Con so co nguon, viet `{{ma_so}}` trong cau van. No tra ve so nguon, in ra chuoi
   `display`, va gan `data-evid` de gate doi chieu duoc. Ma khong co trong so nguon
   thi bao loi NGAY luc dung, khong im lang bo qua: mot con so khong nguon trong ban
   PDF da gui di thi khong goi lai duoc.

## Ba cho de sai, deu co ly do cu the

**Nhung SVG phai doi tien to `id`.** Nhieu SVG tren cung mot trang ma trung `id` thi
`url(#grad)` cua hinh sau tro nham vao dinh nghia cua hinh truoc. Trinh duyet chon
cai dau tien, nen loi hien ra la "hinh thu hai mat mau" chu khong phai loi ro rang.

**SVG phai parse duoc XML truoc khi nhung.** Neu khong, WeasyPrint bo qua CA FILE
va PDF ra 0 net ve, khong bao loi gi. Kiem o day de chet som, ngay luc dung.

**Minh hoa co callout phai bake truoc.** `annotate.js` ve callout bang JavaScript luc
chay; WeasyPrint khong chay JS. Nhung thang file HTML minh hoa vao day thi PDF mat
sach callout. Dung `pipeline/bake_svg.mjs` truoc, roi tro `src` toi file SVG da bake.
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import sys
import xml.parsers.expat
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# LAN xuat ban. Truc nay TRUC GIAO voi truc `che_do` (noi-bo / gui-di): `che_do`
# quyet dinh AI DUOC DOC gi, `lan` quyet dinh THU GIAO DI LA GI.
#
#   pdf-so    PDF doc tren MAN HINH. Tinh hoan toan, vi WeasyPrint khong chay JS.
#             Giu nguong 0 anh raster: ba ly do trong render_pdf.py (nang file, vo
#             net khi phong to, mat kha nang chon chu) deu con dung tren man hinh,
#             va man hinh con bi pinch-zoom nen raster lo ra NHIEU hon giay.
#   html-song HTML tu du mo bang trinh duyet. Duoc animation, tuong tac, raster.
#
# Mac dinh la `pdf-so` de moi loi goi cu giu nguyen hanh vi hom nay.
LAN_MAC_DINH = "pdf-so"
CAC_LAN = ("pdf-so", "html-song")

# Chu de mau. Truoc day chuoi `data-theme="light"` ghi CUNG trong f-string cua
# lap_trang(), khong nhan tham so, nen khong ai doi duoc ma khong sua ma nguon.
#
# Nay la tham so, nhung mac dinh VAN la `light`, va do la co y: bang mau toi da
# co san trong tokens.css, NHUNG chart matplotlib, chart ECharts va 11 minh hoa
# SVG deu chi co ban sang. Bat chu de toi truoc khi tra xong khoan no do la tu
# tao ra dung cai loi da do duoc: trang nen #0A1420 ma chart van nen trang. Go
# hardcode va bat dark mode la HAI viec, day moi la viec thu nhat.
CHU_DE_MAC_DINH = "light"

# Chuoi HIEN THI cho nguoi doc, nen phai co day du dau tieng Viet. Comment va ten bien
# trong repo viet khong dau, nhung do la ma nguon chu khong phai thu in ra giay.
BAC_BANG_CHUNG = {
    "T1_official": "T1 công bố chính thức",
    "T2_audited": "T2 báo cáo kiểm toán",
    "T3_broker": "T3 nghiên cứu thị trường",
    "T4_internal_estimate": "T4 ước tính nội bộ",
    "T5_derived": "T5 suy diễn",
}


class LoiDung(Exception):
    """Loi lam dung dut o giua. Fail-fast la co y: mot bao cao dung nua voi cho
    trong khong nguon con te hon mot lenh bao loi."""


# --------------------------------------------------------------------------- #
# Front-matter
# --------------------------------------------------------------------------- #
def tach_front_matter(van_ban: str) -> tuple[dict, str]:
    """Tra ve (meta, phan than). Front-matter la khoi giua hai dong `---` o dau file."""
    if not van_ban.startswith("---"):
        return {}, van_ban
    dong = van_ban.split("\n")
    ket = None
    for i in range(1, len(dong)):
        if dong[i].strip() == "---":
            ket = i
            break
    if ket is None:
        raise LoiDung("front-matter mo bang --- nhung khong co dong --- dong lai")

    meta: dict = {}
    for so, d in enumerate(dong[1:ket], start=2):
        if not d.strip() or d.lstrip().startswith("#"):
            continue
        if ":" not in d:
            raise LoiDung(f"front-matter dong {so} khong co dau hai cham: {d!r}")
        khoa, gia_tri = d.split(":", 1)
        gia_tri = gia_tri.strip()
        if gia_tri.startswith("[") and gia_tri.endswith("]"):
            meta[khoa.strip()] = [x.strip() for x in gia_tri[1:-1].split(",") if x.strip()]
        else:
            meta[khoa.strip()] = gia_tri.strip('"').strip("'")
    return meta, "\n".join(dong[ket + 1:])


# --------------------------------------------------------------------------- #
# SVG
# --------------------------------------------------------------------------- #
def kiem_xml(noi_dung: str) -> str:
    """Chuoi rong neu la XML hop le, chuoi loi neu khong.

    Tu tay dung expat voi entity handler tu choi moi entity, giong het ban Node o
    `gates/lib/xml.mjs`: expat khong tai external DTD, va handler duoi day cat luon
    nhanh internal entity. Dau vao la SVG do chinh repo sinh ra nen be mat tan cong
    bang 0; neu sau nay nhan SVG tu nguon NGOAI thi phai doi sang defusedxml.
    """
    p = xml.parsers.expat.ParserCreate()

    def tu_choi_entity(*a, **k):
        raise xml.parsers.expat.ExpatError("tu choi entity")

    p.EntityDeclHandler = tu_choi_entity
    p.ExternalEntityRefHandler = lambda *a: False
    try:
        p.Parse(noi_dung.encode("utf-8"), True)
        return ""
    except xml.parsers.expat.ExpatError as e:
        return str(e)


def doi_tien_to_id(svg: str, tien_to: str) -> str:
    """Doi moi `id` va moi tham chieu toi `id` sang co tien to rieng cua hinh."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    if not ids:
        return svg
    for cu in sorted(ids, key=len, reverse=True):
        moi = f"{tien_to}-{cu}"
        cu_esc = re.escape(cu)
        svg = re.sub(rf'\bid="{cu_esc}"', f'id="{moi}"', svg)
        svg = re.sub(rf"url\(#{cu_esc}\)", f"url(#{moi})", svg)
        svg = re.sub(rf'((?:xlink:)?href)="#{cu_esc}"', rf'\1="#{moi}"', svg)
        svg = re.sub(rf'\bbegin="{cu_esc}\.', f'begin="{moi}.', svg)
    return svg


RE_KHOI_STYLE = re.compile(r"<style([^>]*)>(.*?)</style>", re.S)


def gioi_han_style_svg(svg: str, ma_hinh: str) -> str:
    """Bo hep pham vi moi rule CSS ben trong SVG vao dung hinh do.

    matplotlib xuat kem `<style>*{stroke-linejoin: round; stroke-linecap: butt}</style>`.
    Khi SVG nam trong file .svg rieng thi `*` chi cham toi chinh no. Khi SVG duoc nhung
    INLINE vao trang HTML thi `*` cham toi MOI phan tu cua ca trang, va mot bao cao co
    sau hinh matplotlib se co sau rule toan cuc chong len nhau. Day la kieu tac dung phu
    khong ai truy ra, vi trieu chung nam o cho khac hoan toan voi nguyen nhan.

    Cach chua: gan tien to `#<ma_hinh>` vao truoc moi selector. Hinh nam trong
    `<figure id="<ma_hinh>">` nen tien to nay bo hep dung pham vi.
    """

    def bo_hep(m: re.Match) -> str:
        thuoc_tinh, than = m.group(1), m.group(2)
        ra = []
        for phan in re.split(r"(?<=\})", than):
            if "{" not in phan:
                ra.append(phan)
                continue
            selector, con_lai = phan.split("{", 1)
            if selector.strip().startswith("@"):
                ra.append(phan)
                continue
            moi = ", ".join(f"#{ma_hinh} {s.strip()}" for s in selector.split(",") if s.strip())
            ra.append(f"{moi}{{{con_lai}")
        return f"<style{thuoc_tinh}>{''.join(ra)}</style>"

    return RE_KHOI_STYLE.sub(bo_hep, svg)


# Ban Python cua `bocMauChuDe()` trong charts/echarts/hex-token.mjs. Giu CUNG bang khoa.
#
# VI SAO CAN CA BAN PYTHON: ban JS chi chay tren duong ECharts. Chart matplotlib sinh tu
# `hinh/*.py` cua bao cao va di thang vao `nap_svg()` duoi dang hex tho, nen chung KHONG
# doi mau theo chu de nguoi doc chon. Do duoc: mot SVG matplotlib mau co 60 hex tho, trong
# do 7 tren 8 gia tri khac nhau thuoc dung bang mau cua repo.
#
# Du phong LUON bang hex cu, vi file .svg con duoc mo doc lap ngoai trang HTML khai bien.
TOKEN_CSS_PY = {
    "accent": "--accent",
    "accent_hi": "--accent-hi",
    "accent_soft": "--accent-soft",
    "neg": "--neg",
    "pos": "--pos",
    "warn": "--warn",
    "ink": "--ink",
    "ink_md": "--ink-md",
    "ink_lo": "--ink-lo",
    "line": "--line",
    "paper": "--paper",
}


def boc_mau_chu_de(svg: str) -> str:
    """Doi moi hex THUOC bang mau thanh `var(--token, #hex-cu)`.

    Bo qua hex da nam trong mot `var(...)` roi, nen ham nay chay lai tren dau ra cua chinh
    no khong doi gi them. Tinh chat do can thiet vi mot SVG co the di qua ca duong JS lan
    duong Python.
    """
    try:
        from tokens import COLORS  # design-system/tokens.py, da nam tren sys.path
    except ImportError:
        sys.path.insert(0, str(REPO / "design-system"))
        from tokens import COLORS

    for khoa, bien in TOKEN_CSS_PY.items():
        hexa = COLORS.get(khoa)
        if not hexa:
            continue
        mau = re.compile(rf"(?<!var\(){re.escape(hexa)}", re.IGNORECASE)

        def thay(m, bien=bien, hexa=hexa):
            truoc = svg_hien[max(0, m.start() - 60):m.start()]
            # Da boc roi thi de nguyen: dau hieu la mot `var(--x,` chua dong ngoac.
            if "var(--" in truoc and truoc.rfind("var(--") > truoc.rfind(")"):
                return m.group(0)
            return f"var({bien}, {hexa})"

        svg_hien = svg
        svg = mau.sub(thay, svg)
    return svg


RE_THE_SVG_MO = re.compile(r"<svg\b")


def khai_chu_de_svg(svg: str, chu_de: str) -> str:
    """Ghi `data-theme` len MOI the <svg> mo trong chuoi, tru the da co san.

    Gate 9 THEME-MATCH cua lan `html-song` duyet tung the <svg> tren trang va coi thieu
    `data-theme` la FAIL chu khong phai SKIP. Ly do gate lam vay hop ly: mot SVG khong
    khai gi thi khong co cach nao biet no da sinh theo dung chu de cua trang hay chua.
    Nhung khong ai gan thuoc tinh do cho SVG TINH nhung vao trang, nen truoc ban nay moi
    an pham lan song deu do gate 9 ngay tu hinh dau tien. Chart SONG thi da tu gan luc
    mount (xem mount-live.mjs), day la nua con lai cua cung mot viec.
    """
    if not chu_de:
        return svg
    ra = []
    vi_tri = 0
    for m in RE_THE_SVG_MO.finditer(svg):
        het_the = svg.find(">", m.end())
        if het_the == -1:
            break
        the = svg[m.start():het_the]
        ra.append(svg[vi_tri:m.start()])
        if "data-theme" in the:
            ra.append(the)
        else:
            ra.append(f'<svg data-theme="{html_mod.escape(chu_de)}"' + the[len("<svg"):])
        vi_tri = het_the
    ra.append(svg[vi_tri:])
    return "".join(ra)


def nap_svg(duong_dan: Path, tien_to: str, cho_phep_raster: bool = False) -> str:
    if not duong_dan.exists():
        raise LoiDung(f"khong tim thay file hinh: {duong_dan}")
    svg = duong_dan.read_text(encoding="utf-8")
    loi = kiem_xml(svg)
    if loi:
        raise LoiDung(
            f"{duong_dan} khong phai XML hop le ({loi}). WeasyPrint se bo qua CA FILE "
            f"va PDF ra 0 net ve ma khong bao loi. Sua o nguon sinh SVG."
        )
    # Bo khai bao XML va DOCTYPE: chung hop le trong file .svg roi nhung khong hop le
    # khi dat giua than mot trang HTML. Bo luon khoi metadata RDF cua matplotlib: no
    # khai namespace rieng, khong ai doc, va chi lam nang file.
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg)
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    # Chan raster o TANG DUNG, som hon gate 3 RASTER. Ly do phai chan o day chu
    # khong cho gate lo: gate doc file PDF da render xong, con day bat duoc ngay
    # lan hinh dau tien, kem ten file sai.
    #
    # Chan CO DIEU KIEN chu khong tuyet doi. Lan `pdf-so` giu nguyen nguong 0 vi
    # ba ly do trong render_pdf.py deu con dung tren man hinh: nang file, vo net
    # khi phong to, va mat kha nang chon chu. Lan `html-song` thi cho phep, va do
    # la mot quyet dinh ve TRAI NGHIEM chu khong phai mot lo hong ky thuat.
    if not cho_phep_raster and ("<image" in svg or "base64" in svg):
        raise LoiDung(
            f"{duong_dan} co <image> hoac base64 nhung ben trong. Hinh trong bao cao "
            f"phai la vector thuan, neu khong ban PDF se mang anh raster. "
            f"Lan html-song thi dung --lan=html-song de cho phep."
        )
    # Boc mau THEO CHU DE truoc khi tra ve. Chart matplotlib va mot so SVG khac di vao
    # day duoi dang hex tho; khong boc thi chung dung yen mot mau du trang doi chu de.
    # Ham idempotent nen SVG da boc san o duong ECharts khong bi long var() hai lan.
    return boc_mau_chu_de(gioi_han_style_svg(doi_tien_to_id(svg.strip(), tien_to), tien_to))


# --------------------------------------------------------------------------- #
# Markdown
# --------------------------------------------------------------------------- #
RE_DAM = re.compile(r"\*\*(.+?)\*\*")
RE_NGHIENG = re.compile(r"(?<![\*\w])\*([^\*\n]+?)\*(?!\*)")
RE_MA = re.compile(r"`([^`\n]+?)`")
RE_LIEN_KET = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_GIA_TRI = re.compile(r"\{\{([A-Za-z0-9_\-]+)\}\}")


def dung_inline(van_ban: str, so_nguon: "SoNguon") -> str:
    """Xu ly danh dau trong dong. HTML tho trong markdown duoc GIU NGUYEN, khong
    escape, dung quy uoc markdown von co: tac gia can chen mot khoi component thi
    viet thang HTML."""
    van_ban = RE_MA.sub(lambda m: f"<code>{html_mod.escape(m.group(1))}</code>", van_ban)
    van_ban = RE_DAM.sub(r"<strong>\1</strong>", van_ban)
    van_ban = RE_NGHIENG.sub(r"<em>\1</em>", van_ban)
    van_ban = RE_LIEN_KET.sub(r'<a href="\2">\1</a>', van_ban)
    van_ban = RE_GIA_TRI.sub(lambda m: so_nguon.the_gia_tri(m.group(1)), van_ban)
    return van_ban


class SoNguon:
    """So nguon da nap, cong cac phep tra cuu ma tang trinh bay can."""

    def __init__(self, du_lieu: dict, che_do: str, danh_dau: bool = True):
        self.du_lieu = du_lieu
        self.che_do = che_do
        # danh_dau=False: bo ky hieu nguon dang chi so tren canh tung con so.
        # data-evid VAN GIU nguyen tren the .v, nen so nguon van doi chieu duoc
        # va gate LEDGER van chay dung; danh muc nguon cuoi bao cao va dong
        # "Nguon:" duoi moi hinh cung khong doi. Chi bo mot lop nhieu thi giac
        # khi ca bao cao chi co mot nguon duy nhat, luc do ky hieu lap lai hai
        # muoi lan tren mot trang khong them thong tin nao.
        self.danh_dau = danh_dau
        self.nguon = {s["id"]: s for s in du_lieu.get("sources", [])}
        self.gia_tri = {v["id"]: v for v in du_lieu.get("values", [])}
        self.da_dung_nguon: set[str] = set()

    def the_gia_tri(self, ma: str) -> str:
        v = self.gia_tri.get(ma)
        if v is None:
            raise LoiDung(
                f"cau van tham chieu {{{{{ma}}}}} nhung so nguon khong co gia tri nao mang ma do. "
                f"Cac ma dang co: {', '.join(sorted(self.gia_tri)) or '(khong co)'}"
            )
        hien = v.get("display") or f"{v['value']} {v['unit']}"
        self.da_dung_nguon.add(v["source_id"])
        the_so = f'<span class="v" data-evid="{html_mod.escape(ma)}">{html_mod.escape(hien)}</span>'
        if not self.danh_dau:
            return the_so
        return the_so + f'<span class="v-nguon">{html_mod.escape(v["source_id"])}</span>'

    def nhan_nguon(self, ma: str) -> str:
        """Chuoi hien thi cho mot nguon, da ap quy tac che do xuat."""
        s = self.nguon.get(ma)
        if s is None:
            raise LoiDung(f"tham chieu nguon {ma} nhung so nguon khong co nguon nao mang ma do")
        self.da_dung_nguon.add(ma)
        if s.get("sensitivity") == "internal_only" and self.che_do == "gui-di":
            nhan = s.get("public_label")
            if not nhan:
                raise LoiDung(
                    f"nguon {ma} la internal_only nhung thieu public_label, khong xuat ban gui di duoc"
                )
            return nhan
        return s.get("org", ma)


def dung_bang(khoi: list[str], so_nguon: SoNguon, chu_thich: str = "") -> str:
    """Bang markdown dang pipe, co o gop cot va co caption.

    Cot nao co dau hai cham ben phai o dong can le thi la cot SO, duoc gan class `num`
    de an tabular-nums cua components.css.

    **O gop cot** viet bang mot o rong ngay sau o can gop, dung quy uoc quen thuoc cua
    markdown mo rong:

        | Nhóm      | 2025 | 2026 |
        |---|---:|---:|
        | Dẫn đầu ba doanh nghiệp || 18,6% |

    Hai dau gach dung lien tao mot o rong, va o truoc no nhan `colspan=2`. Khong tu che
    cu phap moi vi mot cu phap chi ton tai trong repo nay thi nguoi viet phai hoc rieng.

    **Caption** lay tu dong `Bảng: ...` dat ngay TRUOC bang. `<caption>` la the chuan cua
    HTML va trinh doc man hinh doc no truoc khi vao noi dung bang, khac han mot doan van
    dat gan do.
    """
    def bo_pipe_bien(d: str) -> str:
        """Bo DUNG mot dau pipe moi ben. `strip("|")` bo nhieu pipe lien tiep, nen mot
        hang ket thuc bang o gop dang "| a ||| b ||" bi mat o rong cuoi va ra thieu mot
        cot so voi dong tieu de."""
        d = d.strip()
        if d.startswith("|"):
            d = d[1:]
        if d.endswith("|"):
            d = d[:-1]
        return d

    dong = [bo_pipe_bien(d) for d in khoi]
    tieu_de = [c.strip() for c in dong[0].split("|")]
    can_le = [c.strip() for c in dong[1].split("|")]
    la_so = [c.endswith(":") and not c.startswith(":") for c in can_le]
    than = dong[2:]

    def o_va_colspan(cac_o: list[str]):
        """Gop moi o rong vao o dung truoc no. Tra ve [(noi_dung, colspan, chi_so_cot)]."""
        ra = []
        for i, c in enumerate(cac_o):
            if c == "" and ra:
                ra[-1][1] += 1
                continue
            ra.append([c, 1, i])
        return ra

    ra = ['<div class="table-wrap">', '<table class="dt">']
    if chu_thich:
        ra.append(f"<caption>{dung_inline(chu_thich, so_nguon)}</caption>")
    ra.append("<thead><tr>")
    for noi_dung, span, cot in o_va_colspan(tieu_de):
        lop = ' class="num"' if cot < len(la_so) and la_so[cot] else ""
        thuoc_tinh = f' colspan="{span}"' if span > 1 else ""
        ra.append(f'<th scope="col"{lop}{thuoc_tinh}>{dung_inline(noi_dung, so_nguon)}</th>')
    ra.append("</tr></thead><tbody>")
    for d in than:
        if not d.strip():
            continue
        ra.append("<tr>")
        for noi_dung, span, cot in o_va_colspan([c.strip() for c in d.split("|")]):
            lop = ' class="num"' if cot < len(la_so) and la_so[cot] else ""
            thuoc_tinh = f' colspan="{span}"' if span > 1 else ""
            ra.append(f"<td{lop}{thuoc_tinh}>{dung_inline(noi_dung, so_nguon)}</td>")
        ra.append("</tr>")
    ra.append("</tbody></table></div>")
    return "\n".join(ra)


# `[\w-]` chu khong phai `\w`: `\w` KHONG khop dau gach ngang, nen `du-lieu=...` bi doc
# thanh khoa `lieu`. Da can that va can theo dung kieu te nhat: chart song im lang roi ve
# du lieu demo cua preset trong khi SVG tinh canh no dung du lieu that cua bao cao, tuc
# hai ban cua CUNG mot hinh noi hai dieu khac nhau ma khong ai bao gi. Ten directive cua
# repo von dung dau gach (`ngat-trang`, `chart-song`) nen ten thuoc tinh cung phai dung
# duoc.
RE_DIRECTIVE = re.compile(r'([\w-]+)=("([^"]*)"|\S+)')


def doc_directive(dong: str) -> tuple[str, dict]:
    phan = dong[3:].strip()
    if not phan:
        raise LoiDung("directive rong")
    loai = phan.split()[0]
    thuoc_tinh = {}
    for m in RE_DIRECTIVE.finditer(phan[len(loai):]):
        thuoc_tinh[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(2)
    return loai, thuoc_tinh


class BoDung:
    def __init__(
        self,
        so_nguon: SoNguon,
        goc: Path,
        lan: str = LAN_MAC_DINH,
        chu_de: str = CHU_DE_MAC_DINH,
    ):
        self.lan = lan
        self.chu_de = chu_de
        self.so_nguon = so_nguon
        self.goc = goc
        self.so_hinh = 0
        self.so_h2 = 0
        # Bat khi gap directive `chart-song`. Trang chi nhung bundle 787KB khi THAT SU
        # co chart song: mot ban lan html-song thuan chu va SVG tinh khong phai ganh no.
        self.co_chart_song = False

    def hinh(self, loai: str, tt: dict) -> str:
        src = tt.get("src")
        if not src:
            raise LoiDung(f"directive {loai} thieu src")
        duong = (self.goc / src) if not os.path.isabs(src) else Path(src)
        self.so_hinh += 1
        ma_hinh = tt.get("id") or f"hinh-{self.so_hinh}"
        svg = khai_chu_de_svg(
            nap_svg(duong, ma_hinh, cho_phep_raster=(self.lan == "html-song")), self.chu_de
        )

        chu = tt.get("chu", "")
        dong_nguon = ""
        if tt.get("nguon"):
            cac_ma = [x.strip() for x in tt["nguon"].split(",") if x.strip()]
            ten = ", ".join(self.so_nguon.nhan_nguon(m) for m in cac_ma)
            dong_nguon = f'<span class="hinh-nguon">Nguồn: {html_mod.escape(ten)}</span>'

        return (
            f'<figure class="hinh" id="{html_mod.escape(ma_hinh)}">\n'
            f'<div class="hinh-khung">{svg}</div>\n'
            f'<figcaption class="hinh-chu">'
            f'<span class="hinh-so">Hình {self.so_hinh}</span>'
            f"{dung_inline(chu, self.so_nguon)}{dong_nguon}</figcaption>\n"
            f"</figure>"
        )

    def chart_song(self, tt: dict) -> str:
        """Hinh CO HAI BAN trong cung mot khoi: SVG tinh nhung san, va chart ECharts
        song do bundle mount de len khi JavaScript chay.

        Chi lan `html-song` dung duoc. Lan `pdf-so` di qua WeasyPrint, ma WeasyPrint
        khong chay JavaScript, nen o do directive nay chi con lai ban tinh: dung thi
        khong sai gi ca nhung nguoi viet bao cao tuong minh dang dat mot hinh tuong tac
        vao ban PDF. Bao loi thang con hon de hieu nham do keo dai.

        Hai ban sinh tu CUNG mot file du lieu (`du-lieu=`) qua CUNG mot `option()`, nen
        so tren hai ban khong the lech. Xem `scripts/sinh-svg-preset.mjs`.
        """
        if self.lan != "html-song":
            raise LoiDung(
                "directive `chart-song` chi dung duoc o lan html-song. "
                f"Lan hien tai la `{self.lan}`, ma WeasyPrint khong chay JavaScript nen "
                "chart song se khong bao gio mount. Dung `::: chart` voi mot SVG tinh, "
                "hoac dung `--lan=html-song`."
            )
        preset = tt.get("preset")
        if not preset:
            raise LoiDung("directive chart-song thieu preset")
        src = tt.get("src")
        if not src:
            raise LoiDung(
                f"directive chart-song ({preset}) thieu src. `src` tro toi SVG tinh sinh "
                "san bang scripts/sinh-svg-preset.mjs, va no la thu nguoi tat JavaScript "
                "nhin thay, cung la thu giu gate NO-JS-CONTENT khong do."
            )
        self.so_hinh += 1
        ma_hinh = tt.get("id") or f"hinh-{self.so_hinh}"
        cao = tt.get("cao", "380")
        if not str(cao).isdigit():
            raise LoiDung(f"chart-song {ma_hinh}: `cao` phai la so pixel, dang la {cao!r}")

        duong_svg = (self.goc / src) if not os.path.isabs(src) else Path(src)
        svg = khai_chu_de_svg(nap_svg(duong_svg, ma_hinh, cho_phep_raster=True), self.chu_de)

        # `du-lieu` BAT BUOC, khong co duong lui ve MAC_DINH cua preset. Thieu no thi ban
        # song ve du lieu demo con ban tinh canh no ve du lieu that, va nguoi doc thay ban
        # nao la tuy vao JavaScript co chay hay khong. Da xay ra that mot lan, chinh o ban
        # mau nay, vi RE_DIRECTIVE khong doc noi khoa co dau gach.
        if not tt.get("du-lieu"):
            raise LoiDung(
                f"chart-song {ma_hinh} ({preset}) thieu `du-lieu`. Ban song va ban tinh phai "
                "sinh tu CUNG mot file du lieu, neu khong hai ban se noi hai dieu khac nhau."
            )
        khoi_du_lieu = ""
        if tt.get("du-lieu"):
            duong_dl = self.goc / tt["du-lieu"]
            if not duong_dl.exists():
                raise LoiDung(f"chart-song {ma_hinh}: khong thay file du lieu {duong_dl}")
            tho = duong_dl.read_text(encoding="utf-8")
            try:
                json.loads(tho)
            except json.JSONDecodeError as e:
                raise LoiDung(f"chart-song {ma_hinh}: du lieu khong phai JSON hop le, {e}") from e
            # `</script>` trong chuoi JSON se dong som the script va lam vo ca trang.
            an_toan = tho.replace("</", "<\\/")
            khoi_du_lieu = f'<script type="application/json">{an_toan}</script>'

        chu = tt.get("chu", "")
        dong_nguon = ""
        if tt.get("nguon"):
            cac_ma = [x.strip() for x in tt["nguon"].split(",") if x.strip()]
            ten = ", ".join(self.so_nguon.nhan_nguon(m) for m in cac_ma)
            dong_nguon = f'<span class="hinh-nguon">Nguồn: {html_mod.escape(ten)}</span>'

        self.co_chart_song = True
        return (
            f'<figure class="hinh" id="{html_mod.escape(ma_hinh)}">\n'
            f'<div class="hinh-khung chart-song" data-preset="{html_mod.escape(preset)}" '
            f'style="height:{cao}px">'
            f'<div data-svg-tinh>{svg}</div>{khoi_du_lieu}</div>\n'
            f'<figcaption class="hinh-chu">'
            f'<span class="hinh-so">Hình {self.so_hinh}</span>'
            f"{dung_inline(chu, self.so_nguon)}{dong_nguon}</figcaption>\n"
            f"</figure>"
        )

    def directive(self, dong: str) -> str:
        loai, tt = doc_directive(dong)
        if loai in ("chart", "minh-hoa"):
            return self.hinh(loai, tt)
        if loai == "chart-song":
            return self.chart_song(tt)
        if loai == "ngat-trang":
            return '<div class="ngat-trang"></div>'
        raise LoiDung(f"directive khong biet: {loai}")


def dung_than(
    van_ban: str,
    so_nguon: SoNguon,
    goc: Path,
    lan: str = LAN_MAC_DINH,
    chu_de: str = CHU_DE_MAC_DINH,
) -> tuple[str, bool]:
    """Tra ve (than_html, co_chart_song). Co ca co `co_chart_song` vi trang chi nen
    nhung bundle 787KB khi tren trang that su co chart song."""
    bo = BoDung(so_nguon, goc, lan, chu_de)
    ra: list[str] = []
    chu_thich_bang = ""
    dong = van_ban.split("\n")
    i = 0
    n = len(dong)

    while i < n:
        d = dong[i]
        thu = d.strip()

        if not thu:
            i += 1
            continue

        if thu.startswith("::: "):
            ra.append(bo.directive(thu))
            i += 1
            continue

        if thu.startswith("#"):
            cap = len(thu) - len(thu.lstrip("#"))
            chu = thu[cap:].strip()
            if cap == 2:
                bo.so_h2 += 1
                lop = ' class="dau-tien"' if bo.so_h2 == 1 else ""
                ra.append(f"<h2{lop}>{dung_inline(chu, so_nguon)}</h2>")
            else:
                ra.append(f"<h{cap}>{dung_inline(chu, so_nguon)}</h{cap}>")
            i += 1
            continue

        if thu in ("---", "***", "___"):
            ra.append("<hr>")
            i += 1
            continue

        # Dong "Bang: ..." dat ngay TRUOC mot bang thi tro thanh <caption> cua bang do.
        # Dat sau dong nay bat ky thu gi khac thi no quay ve la mot doan van binh thuong,
        # nen quy uoc khong the am tham nuot mat mot doan.
        ke_tiep = next((d for d in dong[i + 1:] if d.strip()), "")
        if thu.startswith("Bảng:") and "|" in ke_tiep:
            chu_thich_bang = thu[len("Bảng:"):].strip()
            i += 1
            continue

        # Bang pipe: dong hien tai va dong ke tiep deu co |, dong ke tiep la duong can le
        if "|" in thu and i + 1 < n and re.fullmatch(r"[\s|:\-]+", dong[i + 1].strip() or "x"):
            khoi = []
            while i < n and "|" in dong[i]:
                khoi.append(dong[i])
                i += 1
            if len(khoi) >= 2:
                ra.append(dung_bang(khoi, so_nguon, chu_thich_bang))
                chu_thich_bang = ""
                continue
            # khong phai bang that, tra lai de xu ly nhu doan
            i -= len(khoi)

        if thu.startswith(">"):
            khoi = []
            while i < n and dong[i].strip().startswith(">"):
                khoi.append(dong[i].strip().lstrip(">").strip())
                i += 1
            noi = " ".join(khoi)
            ra.append(f"<blockquote><p>{dung_inline(noi, so_nguon)}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", thu) or re.match(r"^\d+[.)]\s+", thu):
            co_thu_tu = bool(re.match(r"^\d+[.)]\s+", thu))
            the = "ol" if co_thu_tu else "ul"
            muc = []
            while i < n:
                t = dong[i].strip()
                if re.match(r"^[-*]\s+", t) or re.match(r"^\d+[.)]\s+", t):
                    muc.append(re.sub(r"^([-*]|\d+[.)])\s+", "", t))
                    i += 1
                elif t and muc:
                    muc[-1] += " " + t  # dong noi tiep cua muc truoc
                    i += 1
                else:
                    break
            ben_trong = "".join(f"<li>{dung_inline(m, so_nguon)}</li>" for m in muc)
            ra.append(f"<{the}>{ben_trong}</{the}>")
            continue

        # HTML tho: khoi bat dau bang the mo thi giu nguyen tron khoi
        if thu.startswith("<"):
            khoi = []
            while i < n and dong[i].strip():
                khoi.append(dong[i])
                i += 1
            ra.append("\n".join(khoi))
            continue

        # Doan van thuong
        khoi = []
        while i < n and dong[i].strip() and not dong[i].strip().startswith(("#", ">", "::: ", "<")):
            khoi.append(dong[i].strip())
            i += 1
        noi = " ".join(khoi)
        lop = ' class="lede"' if noi.startswith("__") else ""
        if lop:
            noi = noi.strip("_").strip()
        ra.append(f"<p{lop}>{dung_inline(noi, so_nguon)}</p>")

    return "\n".join(ra), bo.co_chart_song


# --------------------------------------------------------------------------- #
# Lap trang
# --------------------------------------------------------------------------- #
KIEU_BIA = {"dac": "", "hairline": " bia--hairline", "vien-accent": " bia--vien-accent"}


def dung_bia(meta: dict) -> str:
    if not meta.get("tieu_de"):
        raise LoiDung("front-matter thieu `tieu_de`")
    kieu = meta.get("bia_kieu", "dac")
    if kieu not in KIEU_BIA:
        raise LoiDung(f"bia_kieu={kieu!r} khong co. Chon mot trong: {', '.join(KIEU_BIA)}")
    phan_meta = []
    for khoa in ("ngay", "tac_gia", "phan_loai"):
        if meta.get(khoa):
            phan_meta.append(f"<span>{html_mod.escape(str(meta[khoa]))}</span>")
    kicker = (
        f'<p class="bia-kicker">{html_mod.escape(meta["kicker"])}</p>' if meta.get("kicker") else ""
    )
    dek = f'<p class="bia-dek">{html_mod.escape(meta["dek"])}</p>' if meta.get("dek") else ""
    return (
        f'<header class="bia{KIEU_BIA[kieu]}">{kicker}'
        f'<h1 class="bia-ten">{html_mod.escape(meta["tieu_de"])}</h1>'
        f'{dek}<div class="bia-meta">{"".join(phan_meta)}</div></header>'
    )


def dung_danh_muc_nguon(so_nguon: SoNguon) -> str:
    muc = []
    for ma, s in so_nguon.nguon.items():
        if ma not in so_nguon.da_dung_nguon:
            continue
        rieng = s.get("sensitivity") == "internal_only"
        if rieng and so_nguon.che_do == "gui-di":
            than = html_mod.escape(s["public_label"])
        else:
            than = html_mod.escape(s.get("cite", s.get("org", "")))
        bac = BAC_BANG_CHUNG.get(s.get("tier", ""), s.get("tier", ""))
        muc.append(
            f'<li><span class="nguon-ma">{html_mod.escape(ma)}</span>'
            f'<span class="nguon-than">{than}'
            f'<span class="nguon-bac">{html_mod.escape(bac)}</span></span></li>'
        )
    if not muc:
        return ""
    return (
        '<section class="nguon-muc"><h2>Nguồn số liệu</h2>'
        f'<ul class="nguon-danh-sach">{"".join(muc)}</ul></section>'
    )


# Kho trang ngang, bat bang front-matter `kho_trang: ngang`. Khoi nay DE dung ba
# thu va khong dung gi khac: kho giay, be rong khoi hinh va bang, be rong khung
# man hinh. Cot CHU giu nguyen 165mm co chu dich - be rong doc duoc khong doi
# theo kho giay, mot dong chu dai 265mm thi mat truot dong; phan doi ra cua kho
# ngang danh cho hinh va bang, la thu that su can be ngang.
CSS_KHO_NGANG = """
@page { size: A4 landscape; margin: 15mm 18mm 13mm 18mm; }
@page bia { margin: 0; }
/* KHONG dung column-count o lan pdf-so. Da thu va do duoc: WeasyPrint 69 chay
   van xuoi hai cot voi `column-span: all` cho tieu de va bang thi NUOT NOI
   DUNG - hai section cuoi bien mat khoi PDF va bang cut con mot phan, trong
   khi ban HTML van du. Gate DIACRITICS bat duoc bang so (PDF it hon HTML 24%
   ky tu co dau) nhung khong bao FAIL, nen loi nay du suc di thang ra file
   giao neu chi nhin ban HTML.
   Cach dung o day: MOT cot chu, rong hon kho doc mot chut, canh trai; phan
   doi ra cua kho ngang danh cho hinh va bang, la thu that su can be ngang. */
.bao-cao > * { max-width: 182mm; }
/* Can GIUA cot chu. Phai viet `body.bao-cao > *` chu khong phai `.bao-cao > *`:
   report.css khai `.bao-cao p { margin: ... }` voi do uu tien (0,1,1), cao hon
   `.bao-cao > *` (0,1,0), nen margin auto bi ghi de va cot chu van dinh le
   trai. Da nhin tan mat mot lan truoc khi tim ra. */
body.bao-cao > * { margin-left: auto; margin-right: auto; }
.bao-cao > .hinh,
.bao-cao > .table-wrap,
.bao-cao > figure,
.bia { max-width: 100%; }
.hinh { max-width: 100%; }
/* Bang nhieu cot o kho ngang: ha thang chu mot bac de 11 cot vao tron be
   ngang thay vi tu xuong dong trong o. */
.bao-cao table.dt { font-size: 0.82em; }
.bao-cao table.dt th,
.bao-cao table.dt td { padding-top: 3px; padding-bottom: 3px; }
/* Tieu de cot duoc XUONG DONG. components.css khai `table.dt th` la nowrap,
   hop ly cho bang it cot ten ngan, nhung o bang nhieu cot ten day du thi be
   rong toi thieu cua bang vuot qua kho giay va WeasyPrint CAT mat may cot
   cuoi, khong bao gi. Da nhin tan mat: cot "Hang von hoa" bien khoi trang.
   Cho xuong dong thi tieu de cao them mot dong, con toan bo bang vao tron. */
.bao-cao table.dt th { white-space: normal; }
@media screen { body.bao-cao { max-width: 297mm; } }
"""

KHO_TRANG_HOP_LE = ("doc", "ngang")


DUONG_BUNDLE_SONG = REPO / "charts" / "echarts" / "ra-song" / "bundle-song.js"


def khoi_script_song() -> str:
    """Bundle lan `html-song` nhung thang vao trang, cong loi goi mount.

    `<script type="module">` chu khong phai script thuong: bundle o dinh dang ESM vi
    nhanh CLI cua 18 preset dung top-level await (xem scripts/build-bundle-song.mjs).
    Module INLINE khong phat sinh request nao nen van chay qua `file://`.

    KHONG bọc `try/catch` quanh loi goi mount, va do la co y chu khong phai thieu sot.
    Gate 2 JS-SILENT-FAIL sinh ra de bat dung kieu loi bi nuot. Neu mount hong thi
    SVG tinh van con nguyen tren trang (song-entry.mjs chi go no RA sau khi mount xong),
    nen trang khong vo, ma loi van noi to du de gate nghe thay.
    """
    if not DUONG_BUNDLE_SONG.exists():
        raise LoiDung(
            f"lan html-song can bundle {DUONG_BUNDLE_SONG.relative_to(REPO)} nhung chua co. "
            "Chay: npm run bundle:song"
        )
    bundle = DUONG_BUNDLE_SONG.read_text(encoding="utf-8")
    return (
        '<script type="module">\n'
        + bundle
        + "\nwindow.HTViz.mountTatCa();\n"
        + "</script>"
    )


def lap_trang(
    meta: dict,
    than: str,
    so_nguon: SoNguon,
    chu_de: str = CHU_DE_MAC_DINH,
    khoi_script: str = "",
) -> str:
    css = "\n".join(
        (REPO / p).read_text(encoding="utf-8")
        for p in (
            "design-system/fonts/fonts-embedded.css",
            "design-system/tokens.css",
            "components/components.css",
            "pipeline/report.css",
        )
    )
    kho_trang = str(meta.get("kho_trang", "doc")).strip().lower()
    if kho_trang not in KHO_TRANG_HOP_LE:
        raise LoiDung(f"kho_trang khong biet: {kho_trang!r}. Chi nhan {KHO_TRANG_HOP_LE}")
    if kho_trang == "ngang":
        css += CSS_KHO_NGANG
    the_ledger = ""
    if so_nguon.che_do == "noi-bo":
        the_ledger = (
            '<script type="application/json" id="evidence-ledger">'
            + json.dumps(so_nguon.du_lieu, ensure_ascii=False)
            + "</script>"
        )
    tieu_de = html_mod.escape(meta.get("tieu_de", "Báo cáo"))
    return f"""<!DOCTYPE html>
<html lang="vi" data-theme="{html_mod.escape(chu_de)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{tieu_de}</title>
<style>
{css}
</style>
</head>
<body class="bao-cao">
{dung_bia(meta)}
{than}
{dung_danh_muc_nguon(so_nguon)}
{the_ledger}
{khoi_script}
</body>
</html>
"""


def dung(
    nguon_md: Path,
    ra_html: Path,
    che_do: str,
    lan: str = LAN_MAC_DINH,
    chu_de: str = CHU_DE_MAC_DINH,
) -> Path:
    van_ban = nguon_md.read_text(encoding="utf-8")
    meta, than_md = tach_front_matter(van_ban)

    duong_ledger = meta.get("so_nguon") or meta.get("ledger")
    if not duong_ledger:
        raise LoiDung("front-matter thieu `so_nguon`, tro toi file JSON so nguon")
    p_ledger = nguon_md.parent / duong_ledger
    if not p_ledger.exists():
        raise LoiDung(f"khong tim thay so nguon: {p_ledger}")
    danh_dau = str(meta.get("danh_dau_nguon", "co")).strip().lower()
    if danh_dau not in ("co", "khong"):
        raise LoiDung(f"danh_dau_nguon khong biet: {danh_dau!r}. Chi nhan 'co' hoac 'khong'")
    so_nguon = SoNguon(
        json.loads(p_ledger.read_text(encoding="utf-8")), che_do, danh_dau=(danh_dau == "co")
    )

    if lan not in CAC_LAN:
        raise LoiDung(f"lan khong biet: {lan}. Chi nhan mot trong {CAC_LAN}")

    than, co_chart_song = dung_than(than_md, so_nguon, nguon_md.parent, lan, chu_de)
    khoi_script = khoi_script_song() if co_chart_song else ""
    trang = lap_trang(meta, than, so_nguon, chu_de, khoi_script)

    ra_html.parent.mkdir(parents=True, exist_ok=True)
    ra_html.write_text(trang, encoding="utf-8")
    return ra_html


def main() -> int:
    ap = argparse.ArgumentParser(description="Dung HTML tu du tu markdown va so nguon")
    ap.add_argument("nguon", type=Path)
    ap.add_argument("ra", type=Path)
    ap.add_argument("--che-do", dest="che_do", default="noi-bo", choices=["noi-bo", "gui-di"])
    ap.add_argument("--lan", dest="lan", default=LAN_MAC_DINH, choices=list(CAC_LAN))
    ap.add_argument("--chu-de", dest="chu_de", default=CHU_DE_MAC_DINH)
    tham_so = ap.parse_args()

    try:
        duong = dung(tham_so.nguon, tham_so.ra, tham_so.che_do, tham_so.lan, tham_so.chu_de)
    except LoiDung as e:
        print(f"build_html FAIL: {e}", file=sys.stderr)
        return 1

    kich_thuoc = duong.stat().st_size
    print(
        f"build_html OK -> {duong} ({kich_thuoc / 1024:.0f}KB, "
        f"che do {tham_so.che_do}, lan {tham_so.lan}, chu de {tham_so.chu_de})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
