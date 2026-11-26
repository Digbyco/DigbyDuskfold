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

- `data-copy="approved"`: the founder's approved copy.
- `data-copy="proposed"`: copy awaiting the founder's approval (listed in `docs/copy-for-approval.md`, made by `python3 tools/copy-sheet.py`). On approval, change it to `data-copy="approved"`.
- `data-draft`, `data-missing`, `data-interim` and `[OUTSTANDING: …]` are older interim markers; none remain.

`tools/check.py --release` fails while any proposed or interim content remains, so nothing unapproved can be published.

## Brand artwork

`src/brand/` holds the Digby master logo, wordmark and publisher's mark, lifted from the brand board as transparent PNGs in green and ivory, plus the board's app icon (favicon source) and the approved Duskfold mark (SVG). When the official logo files arrive, replace the PNGs with the same names and rebuild; cache-busting addresses make visitors receive the new files at once.

## App Store availability (one setting)

`src/site-config.json` holds Duskfold's App Store status and listing URL. Before launch every App Store spot shows "Coming soon to the App Store" (no inactive buttons). At launch: set `available_on_app_store` to `true`, add the listing URL and Apple's official badge as `src/brand/app-store-badge.svg`, and rebuild. The build refuses a missing badge or a URL that is not an App Store listing. The spots are the homepage Duskfold feature, the top and bottom of the Duskfold page, and the products card.

## Caching

Every asset address carries a content fingerprint (`?v=…`), added by the build, so changed files are fetched at once even though `.htaccess` lets browsers cache assets. Pages themselves are never cached.

## Adding a product later

Add `src/pages/products/<name>/index.html`, a card on `src/pages/products/index.html`, and, when there
is more than one product, point the "Our Products" navigation link in `src/layout.html` to `/products/`.
