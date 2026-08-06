#!/bin/bash
# markup (.markup.md) -> Typst -> PDF in cao cấp (design ấm). Usage: make_note_pdf.sh <markup> <out.pdf>
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$1"; OUT="$2"
case "$OUT" in /*) ;; *) OUT="$(pwd)/$OUT";; esac
python3 -c "import typst" 2>/dev/null || pip install typst --break-system-packages -q
TMP="$(mktemp -d)"; cp "$HERE/templates/cfa_warm.typ" "$TMP/"
python3 "$HERE/scripts/markup_to_typst.py" "$SRC" "$TMP/note.typ"
python3 -c "import typst; typst.compile('$TMP/note.typ', output='$OUT', root='/', font_paths=['/usr/share/fonts'])"
echo "PDF -> $OUT"; rm -rf "$TMP"
