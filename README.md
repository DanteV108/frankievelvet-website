# Frankievelvet and the Tendertones — the official archive

A nine-page static site. No framework, no dependencies, no build step needed to
*host* it — upload the folder and it works. Tested down to 390px wide.

```
index.html          Front page
history.html        The Legend, 1991–2026 (+ #santa-fe, #charter)
band.html           Current line-up and the Roll of Honour
discography.html    14 studio albums, 6 live, 4 compilations, 22 singles
listen.html         The listening room (audio player)
press.html          Reviews and three long interviews (#interviews)
tour.html           Engagement diary and residency record
gallery.html        The photographic archive
society.html        The fan club (#bulletin, #bookings)

assets/styles.css   One stylesheet, sectioned and commented
assets/site.js      Audio player, image lightbox, discography filter
assets/img/         40 graded archival plates
assets/audio/       MP3s for the listening room

src/*.body.html     Page bodies (see "Editing" below)
tools/build.py      Wraps the bodies in the shared masthead/nav/footer
tools/*.py          The image-processing scripts, kept for re-runs
LORE.md             Continuity bible — names, dates, running jokes
```

## Editing

The masthead, navigation and footer are shared, so they live in `tools/build.py`
rather than being pasted into nine files. Page content lives in `src/`.

```bash
# edit src/history.body.html, then:
python3 tools/build.py
```

That regenerates the nine `.html` files at the root. Each `src/*.body.html`
starts with two comments that become the `<title>` and meta description:

```html
<!-- title: … -->
<!-- desc: … -->
```

If you'd rather not have a build step, the generated `.html` files are perfectly
ordinary and can be edited directly — just don't run `build.py` afterwards or it
will overwrite them.

## Adding audio

Drop an MP3 into `assets/audio/` and point a track at it in
`src/listen.body.html`:

```html
<button class="trk" data-title="Song Title" data-src="assets/audio/file.mp3">
```

A track with no `data-src` shows "Not yet digitised — reel held at Preston,"
which is why the other seven titles are listed but silent. Currently loaded:
`the-tendertone-swing.mp3` (3:00).

## Adding images

`tools/process_photos.py` handles the two real St Andrews scans;
`tools/select_frames.py` and `select_frames_b.py` pull individual frames out of
the generated contact sheets and crop them. All three share the archival grade in
`tools/archival.py` — shadow lift, warm shift, desaturation, vignette, grain.
Run `tools/split_grids.py` first (it re-creates `work/frames/` from the sheets in
your `group shots` folder), then add a row to the `PICKS` list in either selector
and re-run that script.

New photographs go in `assets/img/` and into `gallery.html` as a `figure.plate`;
copy any existing one. `data-zoom` on the figure enables the lightbox.

## Fonts

Bodoni Moda, EB Garamond, Archivo Narrow and Special Elite, loaded from Google
Fonts with real fallbacks (Georgia / Arial / Courier). If you'd rather self-host,
replace the `<link>` in `tools/build.py`.

## A note on the two real photographs

`band-hero.jpg`, `band-full-1994.jpg`, `frankie-portrait.jpg`,
`guitar-detail.jpg`, `percussion-detail.jpg`, `velvettes.jpg`,
`st-andrews-full.jpg`, `st-andrews-wide.jpg`, `room-detail.jpg` and
`guitar-stage-right.jpg` are all derived from your two original scans. Everything
else is derived from the generated sheets. Originals were not modified.

## Deploying

The site is entirely static — HTML, CSS, one JS file, images and audio. Anything
that serves files will serve it.

**GitHub Pages** (same pattern as `daniel-green-portfolio`):

```bash
gh repo create frankievelvet --public --source=. --remote=origin --push
# then: Settings → Pages → Deploy from branch → main → / (root)
```

`.nojekyll` is present so Pages serves the folder as-is rather than running it
through Jekyll. `robots.txt` and `sitemap.xml` assume
`https://dantev108.github.io/frankievelvet/` — change the base URL in both if the
site lands on its own domain, and add a `CNAME` file containing that domain.

**Anywhere else** (Netlify, Render, a plain host): publish directory is the repo
root, no build command. If you'd rather not ship the sources, exclude `src/`,
`tools/`, `LORE.md` and `README.md` — the ten `.html` files and `assets/` are the
whole site.

**Locally:**

```bash
python3 -m http.server 8000
```

Opening `index.html` straight off disk works too, though the audio player is
happier over HTTP.
