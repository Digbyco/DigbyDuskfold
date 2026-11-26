# Digby House website

The static company website for Digby House Ltd (www.digbyhouse.co.uk). It is separate from the
Duskfold app: no database, no scripts, no connection to Duskfold's servers or AI, and no
third-party requests, cookies, analytics or tracking.

## Layout

- `src/layout.html`: the shared page frame (header, navigation, footer).
- `src/pages/`: one file per page; the folder structure is the site's address structure.
- `src/site.css`: all styling (Digby palette, self-hosted Newsreader and Inter fonts).
- `src/.htaccess`, `src/robots.txt`: server settings and search-engine instructions.
- `site/`: **the built website, ready to upload.** Built from `src/` by the build script. Fonts and
  app screenshots live in `site/assets/`.
- `tools/`: build, check and browser-test scripts; `tools/fonts/` holds the font sources for the
  generated images.
- `docs/website-report.md`: the consolidated report, open items and upload instructions.

## Commands

```
python3 tools/build.py              # build site/ (needs Python 3 and Pillow)
python3 tools/build.py --preview    # also build preview/: relative links, opens from a folder
python3 tools/check.py              # links, files, metadata, no external requests; lists interim content
python3 tools/check.py --release    # as above, and refuses while any interim content remains
node tools/browser-test.js <url> <screenshot-dir> <axe.min.js>   # screenshots, axe, keyboard, overflow
```

## Copy status and interim content

- `data-copy="proposed"`: copy awaiting the founder's approval (listed in `docs/copy-for-approval.md`, made by `python3 tools/copy-sheet.py`). On approval, change it to `data-copy="approved"`.
- `data-copy="board"`: copy taken from the Digby brand board.
- `data-draft`, `data-missing`, `data-interim` and `[OUTSTANDING: …]` are older interim markers; none remain.

`tools/check.py --release` fails while any proposed or interim content remains, so nothing unapproved can be published.

## Brand artwork

`src/brand/` holds the Digby master logo, wordmark and publisher's mark, lifted from the brand board as transparent PNGs in green and ivory, plus the board's app icon (favicon source) and the approved Duskfold mark (SVG). To use higher-resolution originals, replace the PNGs with the same names. To show the founder photograph on About, add `src/brand/founder-portrait.jpg`.

## Adding a product later

Add `src/pages/products/<name>/index.html`, a card on `src/pages/products/index.html`, and, when there
is more than one product, point the "Our Products" navigation link in `src/layout.html` to `/products/`.
