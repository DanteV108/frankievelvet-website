"""Shared archival image treatment."""
#!/usr/bin/env python3
"""Turn the two St Andrews Pub scans into a set of archival plates for the site."""
import os, math
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops

SRC = "/mnt/user-data/uploads/Frankie Velvet"
OUT = "/home/claude/frankievelvet/assets/img"
os.makedirs(OUT, exist_ok=True)

def trim_scanner_border(im, tol=26):
    """Drop the near-white scanner margin and any near-black lid band."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    step = max(1, w // 400)

    def row_is_margin(y):
        vals = [px[x, y] for x in range(0, w, step)]
        light = sum(1 for v in vals if v > 232) / len(vals)
        dark = sum(1 for v in vals if v < 14) / len(vals)
        return light > 0.82 or dark > 0.92

    def col_is_margin(x):
        vals = [px[x, y] for y in range(0, h, step)]
        light = sum(1 for v in vals if v > 232) / len(vals)
        dark = sum(1 for v in vals if v < 14) / len(vals)
        return light > 0.82 or dark > 0.92

    top = 0
    while top < h // 4 and row_is_margin(top):
        top += 1
    bot = h - 1
    while bot > 3 * h // 4 and row_is_margin(bot):
        bot -= 1
    left = 0
    while left < w // 4 and col_is_margin(left):
        left += 1
    right = w - 1
    while right > 3 * w // 4 and col_is_margin(right):
        right -= 1
    pad = int(w * 0.004)
    return im.crop((left + pad, top + pad, right - pad, bot - pad))


def grade(im, lift=0.075, warmth=1.02, sat=0.88, gamma=0.76, vig=0.32, grain=7):
    """Faded-archive grade: open the shadows, warm it, pull the saturation, vignette, grain."""
    im = im.convert("RGB")

    # gamma lift so the very dark pub interior reads
    lut = [min(255, int(255 * ((i / 255) ** gamma))) for i in range(256)]
    im = im.point(lut * 3)

    # gentle per-channel autocontrast keeps the reds from clipping
    im = ImageOps.autocontrast(im, cutoff=(0.4, 0.6))

    # shadow lift, weighted so the blacks go warm brown rather than green
    L = lift * 255
    r, g, b = im.split()
    r = r.point(lambda i: min(255, int(i * (1.03 * warmth) + L * 1.00)))
    g = g.point(lambda i: min(255, int(i * 0.985 + L * 0.78)))
    b = b.point(lambda i: min(255, int(i * (0.930 / warmth) + L * 0.58)))
    im = Image.merge("RGB", (r, g, b))

    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(1.06)

    # vignette
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    mpx = mask.load()
    cx, cy = w / 2, h / 2
    mx = math.hypot(cx, cy)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / mx
            v = int(255 * max(0.0, 1 - vig * (d ** 2.4)))
            mpx[x, y] = v
            if x + 1 < w: mpx[x + 1, y] = v
            if y + 1 < h:
                mpx[x, y + 1] = v
                if x + 1 < w: mpx[x + 1, y + 1] = v
    mask = mask.filter(ImageFilter.GaussianBlur(w / 60))
    black = Image.new("RGB", (w, h), (26, 18, 14))
    im = Image.composite(im, black, mask)

    # film grain
    if grain:
        import random
        n = Image.effect_noise((w, h), grain).convert("L")
        n = n.point(lambda i: 128 + (i - 128) * 0.55)
        im = ImageChops.overlay(im, Image.merge("RGB", (n, n, n)))
        im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(0.4)), 0.25)

    return im


def save(im, name, width, quality=84):
    im = im.copy()
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=58, threshold=3))
    path = os.path.join(OUT, name)
    im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    print(f"  {name:38s} {im.width}x{im.height}  {os.path.getsize(path)//1024}kb")


def frac(im, l, t, r, b):
    w, h = im.size
    return im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))


