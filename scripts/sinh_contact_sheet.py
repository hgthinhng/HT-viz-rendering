#!/usr/bin/env python3
"""sinh_contact_sheet.py, mot trang xem het kho hinh bang mat.

    python3 scripts/sinh_contact_sheet.py            # ghi catalog/contact-sheet.html
    python3 scripts/sinh_contact_sheet.py --pdf      # ghi them ban PDF

`catalog/CATALOG.md` tra loi cau hoi "hinh nao tra loi cau hoi nao", va do la thu Claude
doc. Trang nay tra loi cau hoi khac han: "kho co gi, trong ra sao", va do la thu NGUOI
can. Hai thu khong thay nhau duoc: doc mo ta mot chart dumbbell khong cho biet no chiem
bao nhieu chieu ngang tren giay, con nhin thumbnail thi khong biet khi nao dung no.

Chi nhung tai san CO SAN mot file SVG moi len duoc trang nay. Component ke chuyen la
HTML sang trong gallery, va phan lon component matplotlib chi ton tai duoi dang ham chua
render, nen chung duoc liet ke bang chu kem ly do vang mat. Khong dung o trong lam day
cho: mot contact sheet co o trong khong ghi chu se bi doc thanh "hinh nay hong".
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "catalog"


def nhung_svg(duong: Path, tien_to: str) -> str | None:
    """Doc SVG, doi tien to id, ep khung vua o. None neu file khong ton tai."""
    if not duong.exists():
        return None
    s = duong.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    for cu in sorted(set(re.findall(r'\bid="([^"]+)"', s)), key=len, reverse=True):
        moi = f"{tien_to}-{cu}"
        e = re.escape(cu)
        s = re.sub(rf'\bid="{e}"', f'id="{moi}"', s)
        s = re.sub(rf"url\(#{e}\)", f"url(#{moi})", s)
        s = re.sub(rf'((?:xlink:)?href)="#{e}"', rf'\1="#{moi}"', s)
    # Bo hep style trong SVG vao dung o cua no, neu khong selector `*` cua matplotlib
    # se cham toi ca trang.
    s = re.sub(
        r"<style([^>]*)>(.*?)</style>",
        lambda m: f"<style{m.group(1)}>"
        + "".join(
            (f"#{tien_to} {p.split('{', 1)[0].strip()}{{{p.split('{', 1)[1]}"
             if "{" in p and not p.strip().startswith("@") else p)
            for p in re.split(r"(?<=\})", m.group(2))
        )
        + "</style>",
        s,
        flags=re.S,
    )
    # Ep SVG co theo be ngang o chua, giu ty le.
    s = re.sub(r'<svg([^>]*?)\s(?:width|height)="[^"]*"', r"<svg\1", s, count=2)
    return s.strip()


def dung_trang() -> str:
    ml = json.loads((CATALOG / "INDEX.json").read_text(encoding="utf-8"))
    css = "\n".join(
        (REPO / p).read_text(encoding="utf-8")
        for p in ("design-system/fonts/fonts-embedded.css", "design-system/tokens.css")
    )

    o_html: list[str] = []
    khong_anh: dict[str, list[str]] = {}
    so_co_anh = 0

    for m in ml["muc"]:
        xt = m.get("xem_truoc")
        svg = None
        if xt and xt.endswith(".svg"):
            svg = nhung_svg(REPO / xt, f"xt-{m['nhom']}-{m['ma']}")
        if svg is None:
            khong_anh.setdefault(m["nhom"], []).append(m["ma"])
            continue
        so_co_anh += 1
        tra_loi = (m.get("tra_loi") or "").strip()
        if len(tra_loi) > 150:
            tra_loi = tra_loi[:150].rsplit(" ", 1)[0] + "..."
        o_html.append(
            f'<figure class="o" id="xt-{m["nhom"]}-{m["ma"]}">'
            f'<div class="khung">{svg}</div>'
            f'<figcaption><code>{m["ma"]}</code><span>{tra_loi}</span></figcaption>'
            f"</figure>"
        )

    LY_DO = {
        "chart-matplotlib": "chỉ tồn tại dưới dạng hàm chưa render. Chạy "
                            "<code>python3 charts/matplotlib/viz_super.py --spec ... </code> "
                            "với đuôi .svg để có bản xem trước.",
        "component": "là khối HTML, xem trực tiếp trong <code>components/gallery.html</code>.",
        "chart-echarts": "chưa sinh file <code>out-*.svg</code>. Chạy "
                         "<code>npm run verify:charts</code>.",
        "minh-hoa": "không đọc được file SVG.",
    }
    phan_thieu = ""
    if khong_anh:
        muc = "".join(
            f"<li><b>{nhom}</b> ({len(ds)}): {LY_DO.get(nhom, '')}<br>"
            f'<span class="ds">{", ".join(ds)}</span></li>'
            for nhom, ds in khong_anh.items()
        )
        phan_thieu = (
            '<section class="thieu"><h2>Không có bản xem trước</h2>'
            "<p>Liệt kê thẳng ở đây thay vì để ô trống, vì một ô trống không ghi chú "
            "sẽ bị đọc thành hình hỏng.</p>"
            f"<ul>{muc}</ul></section>"
        )

    return f"""<!DOCTYPE html>
<html lang="vi" data-theme="light">
<head>
<meta charset="utf-8">
<title>Kho hình HT-viz, {so_co_anh} bản xem trước</title>
<style>
{css}
@page {{ size: A4 landscape; margin: 12mm; }}
body {{
  margin: 0; padding: 24px; background: var(--paper); color: var(--ink);
  font-family: var(--font-sans);
}}
h1 {{ font-family: var(--font-display); font-size: 26px; margin: 0 0 4px; }}
p.dan {{ color: var(--ink-md); font-size: 14px; margin: 0 0 24px; max-width: 90ch; }}
/* CO Y khong dung CSS Grid o day. WeasyPrint 69 phan trang grid rat te: moi HANG
   grid bi day sang mot trang moi, nen 29 o ra 9 trang voi hai phan ba moi trang bo
   trong. `inline-block` phan trang binh thuong va cho ra dung cai can: cac o chay
   tiep nhau, sang trang khi het cho. Da do bang so tren chinh trang nay. */
.luoi {{ font-size: 0; }}
.o {{
  display: inline-block; vertical-align: top; width: 31.2%; margin: 0 1.6% 16px 0;
  /* 31,2 x 3 cong 1,6 x 2 bang 96,8 phan tram. Ban truoc de 32,4 cong 1,4 nen ba o
     cong lai vuot 100 phan tram va moi hang chi chua duoc HAI o. */
  break-inside: avoid; border: 1px solid var(--line); background: var(--paper);
  font-size: 12px;
}}
.o:nth-child(3n) {{ margin-right: 0; }}
/* Khung CAO CO DINH cho moi thumbnail, va SVG duoc khai ca width lan height de
   `preserveAspectRatio` mac dinh tu thu nho hinh vua khung. De `height: auto` thi minh
   hoa nganh (viewBox 800x500, khong khai width/height) khong co theo o ma giu nguyen
   co px cua viewBox, va tu trang 5 tro di contact sheet chi con 2 o moi trang. Da dem
   bang so tren chinh file nay. Cung co cho moi o con la dieu contact sheet CAN: thumbnail
   khac co thi khong so duoc voi nhau. */
.khung {{
  height: 42mm; padding: 8px; background: var(--paper-hi);
  border-bottom: 1px solid var(--line);
}}
.khung svg {{ display: block; width: 100%; height: 100%; }}
figcaption {{ padding: 8px 10px; font-size: 11.5px; line-height: 1.45; color: var(--ink-md); }}
figcaption code {{
  display: block; font-family: var(--font-mono); font-size: 11px;
  color: var(--accent); margin-bottom: 3px;
}}
.thieu {{ margin-top: 32px; border-top: 2px solid var(--ink); padding-top: 16px; }}
.thieu h2 {{ font-family: var(--font-display); font-size: 18px; margin: 0 0 6px; }}
.thieu p {{ font-size: 13px; color: var(--ink-md); margin: 0 0 12px; }}
.thieu li {{ font-size: 13px; margin-bottom: 10px; }}
.thieu .ds {{ font-family: var(--font-mono); font-size: 11px; color: var(--ink-lo); }}
@media screen and (max-width: 900px) {{ .o {{ width: 100%; margin-right: 0; }} }}
</style>
</head>
<body>
<h1>Kho hình HT-viz</h1>
<p class="dan">{ml['tong']} tài sản trong thư viện, {so_co_anh} có bản xem trước ở đây.
Mã dưới mỗi hình là mã dùng trong mục lục <code>catalog/CATALOG.md</code>, nơi ghi đầy đủ
hình nào trả lời câu hỏi nào và khi nào đừng dùng.</p>
<div class="luoi">
{"".join(o_html)}
</div>
{phan_thieu}
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Trang xem het kho hinh bang mat")
    ap.add_argument("--pdf", action="store_true", help="xuat them ban PDF")
    t = ap.parse_args()

    if not (CATALOG / "INDEX.json").exists():
        print("chua co catalog/INDEX.json. Chay: python3 scripts/sinh_catalog.py", file=sys.stderr)
        return 1

    CATALOG.mkdir(parents=True, exist_ok=True)
    p = CATALOG / "contact-sheet.html"
    p.write_text(dung_trang(), encoding="utf-8")
    print(f"contact sheet OK -> {p} ({p.stat().st_size / 1024:.0f}KB)")

    if t.pdf:
        ra = p.with_suffix(".pdf")
        subprocess.run(
            [sys.executable, str(REPO / "pipeline/render_pdf.py"), str(p), str(ra)],
            cwd=str(REPO), check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
