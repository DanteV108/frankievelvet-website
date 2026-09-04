#!/usr/bin/env python3
"""Crop the chosen individual frames out of the sheets, grade them, name them."""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archival import grade, save

WORK = "/home/claude/frankievelvet/work/frames"
OUT = "/home/claude/frankievelvet/assets/img"

# frame -> (output name, crop l/t/r/b as fractions, target width)
PICKS = [
    ("06-r1c3", "band-quintet.jpg",        (0.00, 0.00, 1.00, 0.90), 1100),
    ("06-r1c2", "frankie-standing.jpg",    (0.00, 0.00, 1.00, 1.00), 1000),
    ("06-r2c3", "frankie-close.jpg",       (0.00, 0.00, 1.00, 1.00), 1000),
    ("06-r3c1", "nino-sax.jpg",            (0.00, 0.00, 1.00, 1.00), 1000),
    ("06-r3c3", "velvette-black.jpg",      (0.00, 0.00, 1.00, 1.00), 1000),
    ("06-r2c1", "velvette-front.jpg",      (0.00, 0.00, 1.00, 0.96), 1000),
    ("07-r2c1", "the-duet.jpg",            (0.00, 0.00, 1.00, 0.80), 1000),
    ("07-r2c2", "front-line.jpg",          (0.00, 0.00, 1.00, 0.80), 1100),
    ("07-r3c1", "double-bass.jpg",         (0.00, 0.00, 0.96, 0.90), 1100),
    ("07-r1c2", "velvettes-pair.jpg",      (0.00, 0.00, 1.00, 0.92), 1000),
    ("13-r2c2", "sax-and-guitar.jpg",      (0.00, 0.00, 1.00, 1.00), 1100),
    ("13-r1c1", "the-room.jpg",            (0.00, 0.00, 1.00, 1.00), 1400),
    ("13-r3c1", "floral-singer.jpg",       (0.00, 0.00, 1.00, 0.86), 1100),
    ("13-r3c2", "velvette-close.jpg",      (0.00, 0.00, 1.00, 1.00), 1000),
    ("04-r2c1", "keys-and-horn.jpg",       (0.00, 0.00, 1.00, 0.96), 1100),
    ("04-r2c2", "two-shot.jpg",            (0.00, 0.00, 1.00, 1.00), 1000),
    ("04-r3c1", "full-band-keys.jpg",      (0.00, 0.00, 1.00, 0.90), 1100),
    ("04-r1c1", "band-wide-1997.jpg",      (0.00, 0.00, 1.00, 0.94), 1100),
]

for frame, name, (l, t, r, b), width in PICKS:
    src = os.path.join(WORK, frame + ".png")
    im = Image.open(src).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))

    # these frames are small; upscale before grading so the grain sits on top
    scale = max(1.0, width / im.width)
    if scale > 1.0:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)

    g = grade(im, lift=0.062, warmth=1.02, sat=0.9, gamma=0.80, vig=0.30, grain=6)
    save(g, name, width, quality=86)

print("selected", len(PICKS), "frames")
