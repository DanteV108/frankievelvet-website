#!/usr/bin/env python3
"""
Assemble the site.

Each page body lives in src/<name>.body.html and is wrapped in the shared
masthead / navigation / footer defined below, producing a plain static
<name>.html at the project root. Nothing else is required to host the site —
run `python3 tools/build.py` after editing a body and upload the result.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

NAV = [
    ("index.html", "Home"),
    ("history.html", "History"),
    ("band.html", "The Band"),
    ("discography.html", "Discography"),
    ("listen.html", "Listen"),
    ("press.html", "Press"),
    ("tour.html", "Live"),
    ("gallery.html", "Photographs"),
    ("contact.html", "Contact"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@400;600;700"
         "&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900"
         "&family=EB+Garamond:ital,wght@0,400..700;1,400..700"
         "&family=Special+Elite&display=swap")

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'"
           "%3E%3Crect width='64' height='64' fill='%23f3ebdd'/%3E%3Ctext x='32' y='45' "
           "font-family='Georgia,serif' font-size='34' font-weight='700' text-anchor='middle' "
           "fill='%237c1f2b'%3EFV%3C/text%3E%3C/svg%3E")

# Visitor statistics. GoatCounter: no cookies, no personal data, so no consent
# banner is required. Register this code once at https://www.goatcounter.com/
# (it becomes <code>.goatcounter.com, where the dashboard lives).
# Set GOATCOUNTER = "" to strip analytics from the site entirely.
GOATCOUNTER = "frankievelvet"

ANALYTICS = (
    f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count"\n'
    f'        async src="https://gc.zgo.at/count.js"></script>\n'
) if GOATCOUNTER else ""


def head(title, desc):
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/band-hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
<link rel="icon" href="{FAVICON}">
{ANALYTICS}</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="masthead">
  <div class="wrap">
    <div class="masthead__top">
      <span>Established Melbourne, 1991</span>
      <span>Fridays &middot; The Emerald Room, Coburg</span>
    </div>
    <a class="masthead__name" href="index.html">
      <em>Continental Entertainment Since 1991</em>
      <strong>Frankievelvet</strong>
      <b>and the Tendertones</b>
    </a>
    <p class="masthead__motto">Tenderness, Nightly</p>
  </div>
  <nav class="nav" aria-label="Primary">
    <div class="wrap">
      <ul>
"""


def nav(page):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ""
        out.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(out)


FOOT = """      </ul>
    </div>
  </nav>
</header>

<main id="main">
__BODY__
</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <h4>The Band</h4>
        <ul>
          <li><a href="history.html">History</a></li>
          <li><a href="band.html">Members</a></li>
          <li><a href="gallery.html">Photographs</a></li>
          <li><a href="press.html">Press</a></li>
        </ul>
      </div>
      <div>
        <h4>The Music</h4>
        <ul>
          <li><a href="discography.html">Discography</a></li>
          <li><a href="listen.html">Listen</a></li>
          <li><a href="discography.html#singles">Singles</a></li>
        </ul>
      </div>
      <div>
        <h4>Live</h4>
        <ul>
          <li><a href="tour.html">Dates</a></li>
          <li>The Emerald Room, Coburg</li>
          <li>Fridays from 8.30</li>
        </ul>
      </div>
      <div>
        <h4>Enquiries</h4>
        <ul>
          <li><a href="contact.html">Bookings</a></li>
          <li><a href="contact.html#requirements">Stage requirements</a></li>
          <li>mail@frankievelvet.com.au</li>
        </ul>
      </div>
    </div>
    <div class="counter" hidden>
      <p class="counter__label">Patrons through the door</p>
      <div class="counter__digits" role="status" aria-live="polite"></div>
      <p class="counter__note">Counter installed 1998 &middot; maintained irregularly</p>
    </div>

    <div class="foot__base">
      <span>Frankievelvet and the Tendertones &middot; Melbourne</span>
      <span>&copy; 2026</span>
    </div>
  </div>
</footer>

<script src="assets/site.js"></script>
</body>
</html>
"""


def build():
    n = 0
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".body.html"):
            continue
        page = fn.replace(".body.html", ".html")
        raw = open(os.path.join(SRC, fn), encoding="utf-8").read()

        m = re.match(r"<!--\s*title:\s*(.*?)\s*-->\s*<!--\s*desc:\s*(.*?)\s*-->\s*",
                     raw, re.S)
        if not m:
            raise SystemExit(f"{fn}: missing title/desc comments at top of file")
        title, desc, body = m.group(1), m.group(2), raw[m.end():]

        html = head(title, desc) + nav(page) + FOOT.replace("__BODY__", body.rstrip())
        open(os.path.join(ROOT, page), "w", encoding="utf-8").write(html)
        print(f"  {page:22s} {len(html)//1024} kb")
        n += 1
    print(f"built {n} pages")


if __name__ == "__main__":
    build()
