#!/usr/bin/env python3
"""Turn the two St Andrews Pub scans into archival plates."""
import os
from PIL import Image, ImageOps
from archival import SRC, OUT, trim_scanner_border, grade, save, frac

print("photo scan 1 (the quartet)")
a = trim_scanner_border(Image.open(os.path.join(SRC, "photo scan 1.jpeg")))
print("  trimmed to", a.size)
ga = grade(a)
save(ga, "band-full-1994.jpg", 1800)
save(frac(ga, 0.02, 0.10, 0.86, 0.99), "band-hero.jpg", 2000, 86)
save(frac(ga, 0.30, 0.16, 0.56, 0.98), "frankie-portrait.jpg", 900)
save(frac(ga, 0.53, 0.22, 0.83, 0.90), "guitar-detail.jpg", 1100)
save(frac(ga, 0.05, 0.24, 0.30, 0.95), "percussion-detail.jpg", 900)
save(frac(ga, 0.26, 0.18, 0.62, 0.62), "frankie-mic-crop.jpg", 900)

print("St Andrews Pub (with the Velvettes)")
b = trim_scanner_border(Image.open(os.path.join(SRC, "St Andrews Pub.jpeg")))
print("  trimmed to", b.size)
gb = grade(b, vig=0.36, gamma=0.66, lift=0.085)
save(gb, "st-andrews-full.jpg", 1800)
save(frac(gb, 0.42, 0.16, 0.72, 0.86), "velvettes.jpg", 1000)
save(frac(gb, 0.66, 0.18, 0.95, 0.80), "guitar-stage-right.jpg", 1000)
save(frac(gb, 0.30, 0.22, 0.56, 0.90), "room-detail.jpg", 900)
save(frac(gb, 0.20, 0.10, 1.00, 0.95), "st-andrews-wide.jpg", 1800)

# a duotone plate for the masthead / ephemera use
print("duotone plate")
d = ImageOps.grayscale(frac(ga, 0.02, 0.10, 0.86, 0.99))
d = ImageOps.autocontrast(d, cutoff=2)
d = ImageOps.colorize(d, black="#2a1a12", mid="#8a5a2c", white="#f2e6d0")
save(d, "band-duotone.jpg", 1600)
print("done")
