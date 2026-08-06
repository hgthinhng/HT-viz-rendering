#!/bin/bash
# ============================================================================
# make_note.sh — LỆNH CHUẨN DUY NHẤT để build 1 CFA study note (.docx)
# Render path: engine + OMML (design ấm "textbook" + công thức Word edit được)
#
# Dùng:
#   ./make_note.sh <markup.md> <out.docx> "<Subject>" <module_num> "<Module name>" [LEVEL]
# Ví dụ:
#   ./make_note.sh work_QM_M1/QM_M1.markup.md "QM_M1.docx" "Quantitative Methods" 1 "Rates and Returns" I
#
# Màu accent tự động theo Subject (map 10 môn CFA trong engine). LEVEL = I|II|III (mặc định I).
# Đặt QC=1 để xuất thêm PDF + ảnh 4 trang đầu cạnh docx (tự kiểm tra nhanh).
# ============================================================================
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ENG="$HERE/scripts/render_engine.py"

MARKUP="$1"; OUT="$2"; SUBJECT="$3"; MNUM="$4"; MNAME="$5"; LEVEL="${6:-I}"
[ -z "$MNAME" ] && { echo "Usage: make_note.sh <markup> <out.docx> <Subject> <module_num> <Module name> [LEVEL]"; exit 1; }
command -v pandoc >/dev/null || { echo "ERROR: cần pandoc (cho công thức OMML)"; exit 1; }

# absolute output path
case "$OUT" in /*) ;; *) OUT="$(pwd)/$OUT";; esac
MDIR="$(cd "$(dirname "$MARKUP")" && pwd)"; MFILE="$(basename "$MARKUP")"
TMP="$(mktemp -d)"

# engine chạy từ thư mục markup để figures/ resolve đúng
( cd "$MDIR" && python3 "$ENG" "$MFILE" "$TMP/out" \
    --subject "$SUBJECT" --module-num "$MNUM" --module-name "$MNAME" \
    --level "$LEVEL" --font-stack B >/dev/null )

# zip unpacked OOXML -> docx
( cd "$TMP/out" && zip -r -X -q "$OUT" '[Content_Types].xml' _rels word )
echo "OK -> $OUT"

# verify OMML present
NF=$(cd "$TMP/out" && grep -o '<m:oMath>' word/document.xml | wc -l)
echo "   công thức OMML edit được: $NF"

# optional QC
if [ "$QC" = "1" ] && command -v libreoffice >/dev/null; then
  libreoffice --headless --convert-to pdf --outdir "$TMP" "$OUT" >/dev/null 2>&1 || true
  PDF="$TMP/$(basename "$OUT" .docx).pdf"
  if [ -f "$PDF" ]; then
    QCDIR="$(dirname "$OUT")/_qc_$(basename "$OUT" .docx)"; mkdir -p "$QCDIR"
    pdftoppm -png -r 130 -f 1 -l 4 "$PDF" "$QCDIR/p" >/dev/null 2>&1 || true
    echo "   QC ảnh: $QCDIR"
  fi
fi
rm -rf "$TMP"
