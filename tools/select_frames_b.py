#!/usr/bin/env python3
"""Second selection: the wider, better-lit venue frames that break up the pub set."""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archival import grade, save

WORK = "/home/claude/frankievelvet/work/frames"

# These frames are already bright and colourful, so the grade is much gentler
# than the one used on the dark pub scans — just a fade, a warm shift and grain.
PICKS = [
    ("50-r1c1", "mural-front-line.jpg",  (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r1c2", "club-tables.jpg",       (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r1c3", "coloured-lights.jpg",   (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r1c4", "skyline-room.jpg",      (0.00, 0.00, 1.00, 1.00), 1300),
    ("50-r2c1", "sax-singer-guitar.jpg", (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r2c2", "blue-set.jpg",          (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r2c3", "from-the-stage.jpg",    (0.00, 0.00, 1.00, 1.00), 1300),
    ("50-r2c4", "crowd-close.jpg",       (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r3c1", "big-crowd.jpg",         (0.00, 0.00, 1.00, 1.00), 1300),
    ("50-r3c2", "guitarist-portrait.jpg",(0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r3c3", "the-bar.jpg",           (0.00, 0.00, 1.00, 1.00), 1200),
    ("50-r3c4", "the-big-room.jpg",      (0.00, 0.00, 1.00, 1.00), 1300),
]

for frame, name, (l, t, r, b), width in PICKS:
    im = Image.open(os.path.join(WORK, frame + ".png")).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * l), int(h * t), int(w * r), int(h * b)))
    scale = max(1.0, width / im.width)
    if scale > 1.0:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    g = grade(im, lift=0.045, warmth=1.015, sat=0.84, gamma=0.94, vig=0.26, grain=6)
    save(g, name, width, quality=86)

print("selected", len(PICKS), "venue frames")
