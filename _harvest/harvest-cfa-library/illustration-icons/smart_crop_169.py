# -*- coding: utf-8 -*-
"""
Smart-crop ảnh vuông (Nano Banana) về banner 16:9 cho header module CFA.
Logic:
  1. Dò màu nền (mẫu 4 góc) → tìm bounding box của subject (pixel khác nền).
  2. Nếu subject lọt dải cao H*9/16 → crop dải 16:9 ôm trọn subject (ưu tiên giữ tâm subject).
  3. Nếu subject cao quá → KHÔNG cắt; nới canvas 2 bên bằng màu nền → đủ 16:9.
Usage:  python smart_crop_169.py <folder>   (mặc định: folder "raw" cạnh script)
Output: <folder>/../out_169/<tên file>_169.png
"""
import sys, os
from PIL import Image
import numpy as np

def bg_color(a):
    corners = np.vstack([a[:8, :8].reshape(-1, a.shape[2]),
                         a[:8, -8:].reshape(-1, a.shape[2]),
                         a[-8:, :8].reshape(-1, a.shape[2]),
                         a[-8:, -8:].reshape(-1, a.shape[2])])
    return np.median(corners, axis=0)

def subject_bbox(a, bg, tol=18):
    diff = np.abs(a.astype(int) - bg.astype(int)).sum(axis=2)
    mask = diff > tol
    ys, xs = np.where(mask)
    if len(ys) == 0: return None
    return ys.min(), ys.max(), xs.min(), xs.max()

def process(path, outdir):
    im = Image.open(path).convert("RGB")
    a = np.array(im)
    H, W = a.shape[:2]
    target_h = int(round(W * 9 / 16))
    bg = bg_color(a)
    bb = subject_bbox(a, bg)
    if bb is None:
        y0 = (H - target_h) // 2
        out = im.crop((0, y0, W, y0 + target_h))
    else:
        ymin, ymax, _, _ = bb
        sub_h = ymax - ymin + 1
        if sub_h <= target_h * 0.96:            # crop được: dải ôm subject
            cy = (ymin + ymax) // 2
            y0 = max(0, min(H - target_h, cy - target_h // 2))
            # nếu dải vẫn chém subject, ép về phía chứa subject
            if ymin < y0: y0 = ymin
            if ymax > y0 + target_h: y0 = ymax - target_h
            y0 = max(0, min(H - target_h, y0))
            out = im.crop((0, y0, W, y0 + target_h))
        else:                                    # subject quá cao: nới ngang
            new_w = int(round(H * 16 / 9))
            canvas = Image.new("RGB", (new_w, H), tuple(int(c) for c in bg))
            canvas.paste(im, ((new_w - W) // 2, 0))
            out = canvas
    name = os.path.splitext(os.path.basename(path))[0]
    outp = os.path.join(outdir, name + "_169.png")
    out.save(outp)
    print(f"{os.path.basename(path)} -> {out.size[0]}x{out.size[1]}  ({outp})")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "raw")
    outdir = os.path.join(os.path.dirname(src.rstrip("/\\")), "out_169")
    os.makedirs(outdir, exist_ok=True)
    files = [f for f in sorted(os.listdir(src)) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    if not files: print("Không có ảnh trong", src); sys.exit(1)
    for f in files: process(os.path.join(src, f), outdir)
