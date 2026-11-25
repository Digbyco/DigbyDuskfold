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

## Interim content

Until the founder supplies the brand board, the agreed copy and the portrait, the preview marks:

- `data-draft="…"`: interim copy (shown with a dashed orange outline);
- `data-missing="…"`: a missing asset (dashed blue outline);
- `data-interim="…"`: the interim typographic wordmark in the header and footer;
- `[OUTSTANDING: …]`: facts still to confirm.

`tools/check.py --release` fails while any of these remain, so the site cannot be published by mistake.

## Adding a product later

Add `src/pages/products/<name>/index.html`, a card on `src/pages/products/index.html`, and, when there
is more than one product, point the "Our Products" navigation link in `src/layout.html` to `/products/`.
