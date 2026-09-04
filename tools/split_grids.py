#!/usr/bin/env python3
"""Split the contact-sheet grids into individual frames."""
import os, glob
from PIL import Image

SRC = "/mnt/user-data/uploads/group shots"
WORK = "/home/claude/frankievelvet/work/frames"
os.makedirs(WORK, exist_ok=True)


def bands(is_gutter, n, min_len):
    """Return (start, end) runs of non-gutter indices."""
    out, start = [], None
    for i in range(n):
        if not is_gutter(i):
            if start is None:
                start = i
        else:
            if start is not None and i - start >= min_len:
                out.append((start, i))
            start = None
    if start is not None and n - start >= min_len:
        out.append((start, n))
    return out


def split(path, tag):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    g = im.convert("L")
    px = g.load()

    def col_gutter(x):
        vals = [px[x, y] for y in range(0, h, 3)]
        light = sum(1 for v in vals if v > 232) / len(vals)
        dark = sum(1 for v in vals if v < 12) / len(vals)
        return light > 0.55 or dark > 0.97

    def row_gutter(y):
        vals = [px[x, y] for x in range(0, w, 3)]
        light = sum(1 for v in vals if v > 232) / len(vals)
        dark = sum(1 for v in vals if v < 12) / len(vals)
        return light > 0.55 or dark > 0.97

    cols = bands(col_gutter, w, int(w * 0.12))
    rows = bands(row_gutter, h, int(h * 0.12))
    print(f"{tag}: {len(cols)} cols x {len(rows)} rows -> {len(cols)*len(rows)} frames")

    n = 0
    for ri, (y0, y1) in enumerate(rows):
        for ci, (x0, x1) in enumerate(cols):
            pad = 3
            fr = im.crop((x0 + pad, y0 + pad, x1 - pad, y1 - pad))
            if fr.width < 120 or fr.height < 120:
                continue
            n += 1
            fr.save(os.path.join(WORK, f"{tag}-r{ri+1}c{ci+1}.png"))
    return n


total = 0
for p in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    tag = p.split("T01_33_")[-1].replace(".png", "")
    total += split(p, tag)
print("frames:", total)

# contact sheet for review
files = sorted(glob.glob(os.path.join(WORK, "*.png")))
cols, cell = 6, 320
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell, rows * (cell + 22)), (245, 240, 230))
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f)
    im.thumbnail((cell - 8, cell - 8), Image.LANCZOS)
    x = (i % cols) * cell + (cell - im.width) // 2
    y = (i // cols) * (cell + 22) + 4
    sheet.paste(im, (x, y))
    d.text(((i % cols) * cell + 6, (i // cols) * (cell + 22) + cell - 2),
           os.path.basename(f).replace(".png", ""), fill=(60, 40, 30))
sheet.save("/home/claude/frankievelvet/work/contact-sheet.png")
print("sheet:", sheet.size)
