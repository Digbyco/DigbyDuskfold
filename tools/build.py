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

# Official Digby artwork, lifted from the brand board (src/brand/; see docs/website-report.md).
LOGO_SMALL = '<img class="logo-header" src="/assets/brand/digby-wordmark-green.png" width="148" height="29" alt="Digby" />'
LOGO_FOOTER = '<img class="logo-footer" src="/assets/brand/digby-master-logo-ivory.png" width="225" height="96" alt="Digby" />'
LOGO_HERO = '<img class="logo-master" src="/assets/brand/digby-master-logo-green.png" width="900" height="384" alt="Digby" />'
SEAL_GREEN = '<img class="seal" src="/assets/brand/digby-publishers-mark-green.png" width="402" height="405" alt="" loading="lazy" />'
SEAL_IVORY = '<img class="seal" src="/assets/brand/digby-publishers-mark-ivory.png" width="402" height="405" alt="" loading="lazy" />'

# The approved Duskfold mark (duskfold/assets/images/brand/duskfold-mark.svg, D-144).
DUSKFOLD_MARK = '<img class="dk-mark" src="/assets/brand/duskfold-mark.svg" width="64" height="64" alt="" />'


NAV_KEYS = ['home', 'products', 'about', 'contact']

# Duskfold's App Store availability, in one place (src/site-config.json).
CONFIG = __import__('json').loads((SRC / 'site-config.json').read_text())
APP_STORE_BADGE = SRC / 'brand' / 'app-store-badge.svg'
APP_STORE_URL_PATTERN = r'^https://apps\.apple\.com/[a-z]{2}/app/[a-z0-9-]+/id\d+(\?.*)?$'


def store_cta() -> str:
    """Before launch: the coming-soon status, with no inactive button. After: Apple's badge."""
    dk = CONFIG['duskfold']
    if not dk.get('available_on_app_store'):
        return '<p class="store-cta"><span class="status">Coming soon to the App Store</span></p>'
    url = dk.get('app_store_url', '')
    if not re.match(APP_STORE_URL_PATTERN, url):
        raise SystemExit('site-config.json: app_store_url must be the public App Store listing (https://apps.apple.com/…)')
    if not APP_STORE_BADGE.exists():
        raise SystemExit("Add Apple's official badge as src/brand/app-store-badge.svg before switching availability on")
    return (
        f'<p class="store-cta"><a class="store-badge" href="{url}">'
        '<img src="/assets/brand/app-store-badge.svg" width="160" height="54" alt="Download Duskfold on the App Store" /></a></p>'
    )


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
        'seal_green': SEAL_GREEN,
        'duskfold_store_cta': store_cta(),
        'dk_status': (
            'Available on the App Store'
            if CONFIG['duskfold'].get('available_on_app_store')
            else 'Coming soon to the App Store'
        ),
        'seal_ivory': SEAL_IVORY,
        'founder_figure': f'<div class="portrait-alt">{SEAL_IVORY}</div>',
        'today': date.today().strftime('%-d %B %Y'),
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
    from PIL import Image

    brand_out = SITE / 'assets' / 'brand'
    brand_out.mkdir(parents=True, exist_ok=True)
    for f in (SRC / 'brand').iterdir():
        if f.suffix in ('.png', '.svg') and not f.name.endswith('-source.png'):
            shutil.copy(f, brand_out / f.name)

    # Favicons from the brand board's Digby app icon.
    icon = Image.open(SRC / 'brand' / 'digby-app-icon-source.png').convert('RGB')
    icon.resize((180, 180), Image.LANCZOS).save(SITE / 'apple-touch-icon.png', optimize=True)
    icon.resize((48, 48), Image.LANCZOS).save(SITE / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    icon.resize((96, 96), Image.LANCZOS).save(SITE / 'favicon.png', optimize=True)

    # Sharing image (1200 x 630): the master logo on ivory.
    share = Image.new('RGBA', (1200, 630), (247, 244, 238, 255))
    logo = Image.open(SRC / 'brand' / 'digby-master-logo-green.png')
    logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)
    share.alpha_composite(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2 - 10))
    share.convert('RGB').save(SITE / 'assets' / 'img' / 'share.png', optimize=True)


def fingerprint() -> None:
    """Adds ?v=<content hash> to every asset address, so an updated file is never served stale."""
    import hashlib

    def version(path: str) -> str:
        f = SITE / path.lstrip('/')
        return hashlib.sha256(f.read_bytes()).hexdigest()[:10] if f.is_file() else ''

    def tag(m: re.Match) -> str:
        path = m.group(2)
        v = version(path)
        return f'{m.group(1)}{path}?v={v}' if v else m.group(0)

    pattern = r'((?:href|src)="|, |srcset=")(/(?:assets/[^"\s,?]+|favicon\.[a-z]+|apple-touch-icon\.png))'
    for page in SITE.rglob('*.html'):
        page.write_text(re.sub(pattern, tag, page.read_text()))
    css = SITE / 'assets' / 'site.css'
    css.write_text(re.sub(r"(url\(')(/assets/[^')?]+)", tag, css.read_text()))


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
    fingerprint()
    print(f'Built {len(pages) + 1} pages into {SITE}')
    if '--preview' in __import__('sys').argv:
        relative_copy(ROOT / 'preview')
        print(f'Folder preview (relative links) in {ROOT / "preview"}')


if __name__ == '__main__':
    main()
