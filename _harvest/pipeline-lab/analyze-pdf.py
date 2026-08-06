import sys
import fitz  # pymupdf

path = sys.argv[1]
doc = fitz.open(path)
print(f"=== {path} ===")
print(f"pages: {len(doc)}  file size: {doc.tobytes().__sizeof__() if False else ''}")
import os
print(f"file bytes on disk: {os.path.getsize(path)}")

total_img_bytes = 0
img_count = 0
for pno in range(len(doc)):
    page = doc[pno]
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        try:
            info = doc.extract_image(xref)
            sz = len(info["image"])
            w, h = info.get("width"), info.get("height")
        except Exception as e:
            sz = 0
            w = h = None
        total_img_bytes += sz
        img_count += 1
        print(f"  page {pno+1}: xref={xref} dims={w}x{h} bytes={sz}")

print(f"TOTAL raster images: {img_count}, total bytes: {total_img_bytes}")
