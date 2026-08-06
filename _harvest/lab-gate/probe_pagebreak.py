import fitz, sys

doc = fitz.open(sys.argv[1] if len(sys.argv) > 1 else "reference-kimi.pdf")
EPS_EDGE = 1.5   # pt tolerance to "touches top/bottom edge"
EPS_X = 3.0      # pt tolerance on left/right alignment
EPS_COLOR = 0.02 # tolerance per channel

def close(a, b, eps):
    return abs(a - b) <= eps

def color_close(c1, c2, eps=EPS_COLOR):
    if c1 is None or c2 is None:
        return c1 == c2
    return all(abs(a - b) <= eps for a, b in zip(c1, c2))

hits = []
page_h = doc[0].rect.height
per_page = []
for i in range(doc.page_count):
    pg = doc[i]
    h = pg.rect.height
    draws = pg.get_drawings()
    rects = []
    for d in draws:
        fill = d.get("fill")
        rect = d.get("rect")
        if fill is None or rect is None:
            continue
        if rect.width < 20 or rect.height < 4:
            continue  # skip hairlines/dividers, keep panel-sized fills
        if rect.width >= pg.rect.width * 0.95 and rect.height >= pg.rect.height * 0.95:
            continue  # skip full-page background fill (not a content card)
        rects.append((rect, fill))
    per_page.append((h, rects))

for i in range(doc.page_count - 1):
    h, rects = per_page[i]
    h2, rects2 = per_page[i + 1]
    bottom_touch = [(r, f) for r, f in rects if close(r.y1, h, EPS_EDGE)]
    top_touch = [(r, f) for r, f in rects2 if close(r.y0, 0, EPS_EDGE)]
    for r1, f1 in bottom_touch:
        for r2, f2 in top_touch:
            if close(r1.x0, r2.x0, EPS_X) and close(r1.x1, r2.x1, EPS_X) and color_close(f1, f2):
                hits.append((i + 1, i + 2, r1, r2, f1))

print(f"pages={doc.page_count}")
for h in hits:
    print("SLICE pageA=%d pageB=%d rectA=%s rectB=%s fill=%s" % h)
print("total_hits", len(hits))
