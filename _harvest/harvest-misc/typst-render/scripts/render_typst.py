#!/usr/bin/env python3
"""Compile Typst -> PDF (warm-design CFA). Usage: render_typst.py <in.typ> <out.pdf> [--png]
Tự set root = thư mục chứa file .typ (để import cfa_warm.typ cạnh nó), font /usr/share/fonts."""
import sys, os, subprocess
try: import typst
except ImportError:
    subprocess.run([sys.executable,"-m","pip","install","typst","--break-system-packages","-q"]); import typst
inp=os.path.abspath(sys.argv[1]); out=os.path.abspath(sys.argv[2])
typst.compile(inp, output=out, root=os.path.dirname(inp) or "/", font_paths=["/usr/share/fonts"])
print("PDF:", out)
if "--png" in sys.argv:
    base=os.path.splitext(out)[0]
    subprocess.run(["pdftoppm","-png","-r","150",out,base])
    print("PNG preview:", base+"-1.png")
