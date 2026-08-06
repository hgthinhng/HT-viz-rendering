---
name: typst-render
description: Tạo PDF chất lượng IN (premium) từ Typst (.typ) trong sandbox — đẹp ngang LaTeX, nhanh ~10×, math native, KHỚP design ấm CFA (Lora/Lato, navy/teal/gold/giấy kem, callout, term song ngữ). LUÔN dùng khi user nói "xuất PDF đẹp", "typst", "premium PDF", "PDF chất lượng in", "render typst", hoặc cần đường PDF thứ hai ngoài docx. Có template warm tái dùng + cover + callout + term().
---

# typst-render

> Đường **PDF cao cấp** bổ trợ cho note-pipeline (ngoài docx-OMML). Typst = typesetting hiện đại: 1 binary, math native, layout dễ chỉnh hơn LaTeX. Đã khớp sẵn design ấm của note.

## Setup (1 lần / phiên)
```bash
pip install typst --break-system-packages   # binding Python; hoặc dùng binary `typst`
```
Fonts Lato + Lora đã có trong sandbox.

## Dùng nhanh
1. Viết nội dung `.typ`, đặt cạnh `templates/cfa_warm.typ` (hoặc copy template vào cùng thư mục).
2. Đầu file: `#import "cfa_warm.typ": *` rồi `#show: conf.with(level: "I")`.
3. Compile: `python3 scripts/render_typst.py noi_dung.typ out.pdf --png`.

## API template (`templates/cfa_warm.typ`)
- `#show: conf.with(level: "I")` — page giấy kem, footer số trang + gold rule, heading Lora teal/navy + gold rule dưới H1.
- `#cover(subject: "...", module: "...", vi: "...", level: "I")` — trang bìa editorial.
- `#callout(kind:"example"|"key"|"warn"|"note")[ ... ]` — box shading + thanh màu trái + nhãn gold (warn = "GHI CHÚ BỔ SUNG").
- `#term[English][gloss Việt]` — thuật ngữ song ngữ term-first (teal đậm + gloss).
- Math: cú pháp Typst native, vd `$ R_G = [product_(t=1)^T (1+R_t)]^(1/T) - 1 $`.

## Khi nào chọn typst vs docx-engine
- **docx-OMML** (note-pipeline-render): khi cần file Word EDIT được + chèn ảnh AI.
- **typst** (skill này): khi cần PDF chất lượng IN đẹp nhất / nhanh / 1 lệnh, không cần edit Word.
Cùng 1 design ấm → output nhất quán.

## Tích hợp note-pipeline (đường PDF thứ 2)
Cùng 1 `{module}.markup.md` (sau GATE VOICE) → 2 đầu ra:
- `note-pipeline-render/make_note.sh` → **.docx** (Word edit, OMML, chèn ảnh AI) — primary.
- `make_note_pdf.sh <markup> <out.pdf>` → **.pdf Typst** (in cao cấp, math native, khoá đẹp) — export.

`scripts/markup_to_typst.py` chuyển markup→.typ (dùng `cfa_warm.typ`); `scripts/l2t.py` chuyển LaTeX→Typst math. Map: SECTION→`=`, SUBSECTION→`==`, FORMULA→`$...$`, BOX_*→`#callout`, T:→`#term`, TABLE→`#cfatable`, FIGURE→`#image`, COVER→`#cover`, SECTION_OPEN→`#opener`, RECAP→`#callout key`.
Design KHỚP docx-engine (cùng palette/type). Đổi design phải sửa cả 2 (giữ 1 spec chung).