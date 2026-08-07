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


def nap_svg(duong_dan: Path, tien_to: str) -> str:
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
    if "<image" in svg or "base64" in svg:
        raise LoiDung(
            f"{duong_dan} co <image> hoac base64 nhung ben trong. Hinh trong bao cao "
            f"phai la vector thuan, neu khong ban PDF se mang anh raster."
        )
    return gioi_han_style_svg(doi_tien_to_id(svg.strip(), tien_to), tien_to)


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

    def __init__(self, du_lieu: dict, che_do: str):
        self.du_lieu = du_lieu
        self.che_do = che_do
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
        return (
            f'<span class="v" data-evid="{html_mod.escape(ma)}">{html_mod.escape(hien)}</span>'
            f'<span class="v-nguon">{html_mod.escape(v["source_id"])}</span>'
        )

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


RE_DIRECTIVE = re.compile(r'(\w+)=("([^"]*)"|\S+)')


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
    def __init__(self, so_nguon: SoNguon, goc: Path):
        self.so_nguon = so_nguon
        self.goc = goc
        self.so_hinh = 0
        self.so_h2 = 0

    def hinh(self, loai: str, tt: dict) -> str:
        src = tt.get("src")
        if not src:
            raise LoiDung(f"directive {loai} thieu src")
        duong = (self.goc / src) if not os.path.isabs(src) else Path(src)
        self.so_hinh += 1
        ma_hinh = tt.get("id") or f"hinh-{self.so_hinh}"
        svg = nap_svg(duong, ma_hinh)

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

    def directive(self, dong: str) -> str:
        loai, tt = doc_directive(dong)
        if loai in ("chart", "minh-hoa"):
            return self.hinh(loai, tt)
        if loai == "ngat-trang":
            return '<div class="ngat-trang"></div>'
        raise LoiDung(f"directive khong biet: {loai}")


def dung_than(van_ban: str, so_nguon: SoNguon, goc: Path) -> str:
    bo = BoDung(so_nguon, goc)
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

    return "\n".join(ra)


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


def lap_trang(meta: dict, than: str, so_nguon: SoNguon) -> str:
    css = "\n".join(
        (REPO / p).read_text(encoding="utf-8")
        for p in (
            "design-system/fonts/fonts-embedded.css",
            "design-system/tokens.css",
            "components/components.css",
            "pipeline/report.css",
        )
    )
    the_ledger = ""
    if so_nguon.che_do == "noi-bo":
        the_ledger = (
            '<script type="application/json" id="evidence-ledger">'
            + json.dumps(so_nguon.du_lieu, ensure_ascii=False)
            + "</script>"
        )
    tieu_de = html_mod.escape(meta.get("tieu_de", "Báo cáo"))
    return f"""<!DOCTYPE html>
<html lang="vi" data-theme="light">
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
</body>
</html>
"""


def dung(nguon_md: Path, ra_html: Path, che_do: str) -> Path:
    van_ban = nguon_md.read_text(encoding="utf-8")
    meta, than_md = tach_front_matter(van_ban)

    duong_ledger = meta.get("so_nguon") or meta.get("ledger")
    if not duong_ledger:
        raise LoiDung("front-matter thieu `so_nguon`, tro toi file JSON so nguon")
    p_ledger = nguon_md.parent / duong_ledger
    if not p_ledger.exists():
        raise LoiDung(f"khong tim thay so nguon: {p_ledger}")
    so_nguon = SoNguon(json.loads(p_ledger.read_text(encoding="utf-8")), che_do)

    than = dung_than(than_md, so_nguon, nguon_md.parent)
    trang = lap_trang(meta, than, so_nguon)

    ra_html.parent.mkdir(parents=True, exist_ok=True)
    ra_html.write_text(trang, encoding="utf-8")
    return ra_html


def main() -> int:
    ap = argparse.ArgumentParser(description="Dung HTML tu du tu markdown va so nguon")
    ap.add_argument("nguon", type=Path)
    ap.add_argument("ra", type=Path)
    ap.add_argument("--che-do", dest="che_do", default="noi-bo", choices=["noi-bo", "gui-di"])
    tham_so = ap.parse_args()

    try:
        duong = dung(tham_so.nguon, tham_so.ra, tham_so.che_do)
    except LoiDung as e:
        print(f"build_html FAIL: {e}", file=sys.stderr)
        return 1

    kich_thuoc = duong.stat().st_size
    print(f"build_html OK -> {duong} ({kich_thuoc / 1024:.0f}KB, che do {tham_so.che_do})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
