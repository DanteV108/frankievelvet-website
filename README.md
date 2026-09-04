# Frankievelvet and the Tendertones — the official archive

A ten-page static site. No framework, no dependencies, no build step needed to
*host* it — upload the folder and it works. Tested down to 390px wide.

```
index.html          Home
history.html        1991–2026
band.html           Current line-up and every member since 1991
discography.html    14 studio records, 6 live, 4 compilations, 22 singles (#singles)
listen.html         Audio player
press.html          Reviews and three interviews (#interviews)
tour.html           Dates and the residency record
gallery.html        Photographs
contact.html        Bookings and stage requirements (#requirements)
404.html            Not found

assets/styles.css   One stylesheet, sectioned and commented
assets/site.js      Audio player, image lightbox, discography filter
assets/img/         40 graded archival plates
assets/audio/       MP3s for the listening room

src/*.body.html     Page bodies (see "Editing" below)
tools/build.py      Wraps the bodies in the shared masthead/nav/footer
tools/*.py          The image-processing scripts, kept for re-runs
LORE.md             Continuity bible — names, dates, who joined when
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
