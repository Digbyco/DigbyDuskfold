#!/usr/bin/env python3
"""Build the Digby House static website from src/ into site/.

No dependencies beyond Python 3 and Pillow (for the favicon and sharing image). The output is
plain HTML, CSS, fonts and images, suitable for OVHcloud's free 100 MB hosting.

    python3 tools/build.py
"""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'
SITE = ROOT / 'site'
ORIGIN = 'https://www.digbyhouse.co.uk'

# Interim wordmark until the master logo files are supplied (brief §3). Marked so the release
# check refuses to ship it.
LOGO_SMALL = '<span class="wordmark wordmark-small" data-interim="master logo">DIGBY</span>'
LOGO_FOOTER = '<span class="wordmark" data-interim="master logo">DIGBY</span>'
LOGO_HERO = (
    '<span data-missing="Digby master logo (brand board files)" aria-hidden="true">'
    '<span class="wordmark">DIGBY</span></span>'
)

# The Duskfold mark, as drawn in the app (src/components/scene/LogoMark.tsx), in its gold.
DUSKFOLD_MARK = """<svg class="dk-mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
  <defs><linearGradient id="dkfold" x1="0.3" y1="1" x2="1" y2="0.1"><stop offset="0" stop-color="#D9AE78" stop-opacity="0"/><stop offset="0.6" stop-color="#D9AE78" stop-opacity="0.12"/><stop offset="1" stop-color="#D9AE78" stop-opacity="0.55"/></linearGradient></defs>
  <path d="M38.4 41 L52.4 41 Q56.4 41 56.4 45 L56.4 58.1 Z" fill="url(#dkfold)"/>
  <path d="M30 6 A26.1 26.1 0 1 0 32.1 58.1 L53.4 58.1 Q56.4 58.1 56.4 55.1 L56.4 45 Q56.4 41 52.4 41 L38.4 41 A20.6 20.6 0 0 1 30 6 Z" fill="none" stroke="#D9AE78" stroke-width="1.4" stroke-linejoin="round"/>
  <path d="M38.4 41 L56 57.8" stroke="#D9AE78" stroke-width="1.4"/>
  <path d="M52.3 12.6 Q52.8 18.9 58.9 19.4 Q52.8 19.9 52.3 26.2 Q51.8 19.9 45.7 19.4 Q51.8 18.9 52.3 12.6 Z" fill="#D9AE78"/>
</svg>"""

NAV_KEYS = ['home', 'products', 'about', 'contact']


def front_matter(text: str) -> tuple[dict[str, str], str]:
    m = re.match(r'\s*<!--(.*?)-->\s*', text, re.S)
    if not m:
        raise SystemExit('missing front matter')
    meta = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(':')
        meta[key.strip()] = value.strip()
    return meta, text[m.end():]


def render(layout: str, meta: dict[str, str], body: str) -> str:
    values = {
        'title': meta['title'],
        'description': meta['description'],
        'path': meta['path'],
        'body_class': meta.get('body_class', ''),
        'content': body,
        'logo_small': LOGO_SMALL,
        'logo_footer': LOGO_FOOTER,
        'logo_hero': LOGO_HERO,
        'duskfold_mark': DUSKFOLD_MARK,
    }
    for key in NAV_KEYS:
        values[f'nav_{key}'] = ' aria-current="page"' if meta.get('nav') == key else ''
    out = layout
    # Two passes: page bodies may use the same placeholders as the layout.
    for _ in range(2):
        out = re.sub(r'\{\{(\w+)\}\}', lambda m: values.get(m.group(1), m.group(0)), out)
    if meta.get('noindex') == 'yes':
        out = out.replace('<meta name="viewport"', '<meta name="robots" content="noindex" />\n    <meta name="viewport"', 1)
    left = re.findall(r'\{\{\w+\}\}', out)
    if left:
        raise SystemExit(f'unfilled placeholders in {meta["path"]}: {left}')
    return out


def images() -> None:
    from PIL import Image, ImageDraw, ImageFont

    fonts = SITE / 'assets' / 'fonts'
    serif_ttf = ROOT / 'tools' / 'fonts' / 'Newsreader_400Regular.ttf'
    italic_ttf = ROOT / 'tools' / 'fonts' / 'Newsreader_400Regular_Italic.ttf'
    forest, ivory = (33, 76, 61), (247, 244, 238)

    # Interim favicon: an ivory "D" on forest green, until the brand board's favicon is supplied.
    def monogram(size: int) -> Image.Image:
        im = Image.new('RGB', (size, size), forest)
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(str(serif_ttf), int(size * 0.72))
        box = d.textbbox((0, 0), 'D', font=f)
        d.text(((size - (box[2] - box[0])) / 2 - box[0], (size - (box[3] - box[1])) / 2 - box[1]), 'D', font=f, fill=ivory)
        return im

    monogram(180).save(SITE / 'apple-touch-icon.png', optimize=True)
    monogram(64).save(SITE / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    (SITE / 'favicon.svg').write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#214C3D"/>'
        '<text x="32" y="46" text-anchor="middle" font-family="Georgia, \'Times New Roman\', serif" font-size="42" fill="#F7F4EE">D</text></svg>\n'
    )

    # Interim sharing image (1200 x 630).
    im = Image.new('RGB', (1200, 630), ivory)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(str(serif_ttf), 150)
    word = 'D I G B Y'
    box = d.textbbox((0, 0), word, font=f)
    d.text(((1200 - (box[2] - box[0])) / 2 - box[0], 190), word, font=f, fill=forest)
    fi = ImageFont.truetype(str(italic_ttf), 44)
    tag = 'Thoughtfully made tools for everyday life.'
    box = d.textbbox((0, 0), tag, font=fi)
    d.text(((1200 - (box[2] - box[0])) / 2 - box[0], 420), tag, font=fi, fill=forest)
    d.rectangle((0, 600, 1200, 630), fill=forest)
    im.save(SITE / 'assets' / 'img' / 'share.png', optimize=True)
    assert fonts.exists()


def relative_copy(dest: Path) -> None:
    """A copy of site/ with relative links, for opening straight from a folder (founder preview)."""
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SITE, dest)
    for page in dest.rglob('*.html'):
        depth = len(page.relative_to(dest).parts) - 1
        up = '../' * depth

        def local(m: re.Match) -> str:
            path = m.group(2)
            if path.startswith('//'):
                return m.group(0)
            rel = up + path.lstrip('/')
            if rel == '' or rel.endswith('/'):
                rel += 'index.html'
            return f'{m.group(1)}{rel}'

        html = page.read_text()
        # Browsers refuse a crossorigin preload from a local folder; the font still loads via CSS.
        html = re.sub(r'\s*<link rel="preload"[^>]*>', '', html)
        html = re.sub(r'((?:href|src)=")(/[^"]*)', local, html)
        html = re.sub(r'(srcset="[^"]*")', lambda m: re.sub(r'(^|, |")(/assets)', lambda n: n.group(1) + up + 'assets', m.group(1)), html)
        page.write_text(html)
    css = dest / 'assets' / 'site.css'
    css.write_text(css.read_text().replace("url('/assets/fonts/", "url('fonts/"))


def main() -> None:
    layout = (SRC / 'layout.html').read_text()
    # Fresh output, keeping the prepared fonts and screenshots.
    for p in SITE.glob('*'):
        if p.name == 'assets':
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    (SITE / 'assets').mkdir(exist_ok=True)
    shutil.copy(SRC / 'site.css', SITE / 'assets' / 'site.css')
    for name in ('.htaccess', 'robots.txt'):
        shutil.copy(SRC / name, SITE / name)

    pages = []
    for page in sorted((SRC / 'pages').rglob('*.html')):
        meta, body = front_matter(page.read_text())
        rel = page.relative_to(SRC / 'pages')
        out = SITE / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(layout, meta, body))
        if meta.get('noindex') != 'yes':
            pages.append(meta['path'])

    today = date.today().isoformat()
    urls = '\n'.join(f'  <url><loc>{ORIGIN}{p}</loc><lastmod>{today}</lastmod></url>' for p in pages)
    (SITE / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '\n</urlset>\n'
    )
    images()
    print(f'Built {len(pages) + 1} pages into {SITE}')
    if '--preview' in __import__('sys').argv:
        relative_copy(ROOT / 'preview')
        print(f'Folder preview (relative links) in {ROOT / "preview"}')


if __name__ == '__main__':
    main()
