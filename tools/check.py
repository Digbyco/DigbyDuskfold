#!/usr/bin/env python3
"""Checks the built site in site/.

    python3 tools/check.py            # preview: report interim content, fail on real faults
    python3 tools/check.py --release  # publication: also fail while any interim content remains

Faults: broken internal links or images, resources loaded from other sites, pages without a
title, description, h1 or lang, images without alt text, scripts, a package over 100 MB.
Interim content (refused with --release): data-draft copy, data-missing assets, data-interim
logos and [OUTSTANDING: ...] notes.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE = Path(__file__).resolve().parent.parent / 'site'
LIMIT_MB = 100
# External links people may follow (never loaded by the page itself).
ALLOWED_EXTERNAL_LINKS = {'ico.org.uk'}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.resources: list[str] = []
        self.images_without_alt = 0
        self.h1 = 0
        self.scripts = 0
        self.lang = None
        self.title = ''
        self._in_title = False
        self.description = False
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'link' and a.get('href'):
            (self.links if a.get('rel') == 'canonical' else self.resources).append(a['href'])
        if tag == 'img':
            self.resources.append(a.get('src', ''))
            for part in (a.get('srcset') or '').split(','):
                if part.strip():
                    self.resources.append(part.strip().split()[0])
            if 'alt' not in a:
                self.images_without_alt += 1
        if tag == 'script':
            self.scripts += 1
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self._in_title = True
        if tag == 'meta' and a.get('name') == 'description' and a.get('content'):
            self.description = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def target(path: str) -> Path:
    p = SITE / path.lstrip('/')
    return p / 'index.html' if path.endswith('/') or p.is_dir() else p


def main() -> int:
    release = '--release' in sys.argv
    faults: list[str] = []
    interim: list[str] = []
    pages = sorted(SITE.rglob('*.html'))
    for page in pages:
        rel = '/' + str(page.relative_to(SITE))
        html = page.read_text()
        p = Page()
        p.feed(html)
        if p.lang != 'en-GB':
            faults.append(f'{rel}: html lang is not en-GB')
        if not p.title.strip():
            faults.append(f'{rel}: no title')
        if not p.description:
            faults.append(f'{rel}: no meta description')
        if p.h1 != 1:
            faults.append(f'{rel}: {p.h1} h1 headings (expected 1)')
        if p.images_without_alt:
            faults.append(f'{rel}: {p.images_without_alt} image(s) without alt')
        if p.scripts:
            faults.append(f'{rel}: contains a script')
        for href in p.links:
            u = urlparse(href)
            if u.scheme in ('mailto', 'tel'):
                continue
            if u.scheme in ('http', 'https'):
                host = u.netloc.removeprefix('www.')
                if host == 'digbyhouse.co.uk':
                    if not target(u.path or '/').exists():
                        faults.append(f'{rel}: canonical or link to missing page {href}')
                elif host not in ALLOWED_EXTERNAL_LINKS:
                    faults.append(f'{rel}: unexpected external link {href}')
                continue
            if href.startswith('#'):
                if href[1:] not in p.ids:
                    faults.append(f'{rel}: missing anchor {href}')
                continue
            if not target(u.path).exists():
                faults.append(f'{rel}: broken link {href}')
        for src in p.resources:
            u = urlparse(src)
            if u.scheme in ('http', 'https'):
                faults.append(f'{rel}: loads {src} from another site')
            elif not target(u.path).exists():
                faults.append(f'{rel}: missing file {src}')
        for kind, pattern in (
            ('draft copy', r'data-draft="([^"]+)"'),
            ('missing asset', r'data-missing="([^"]+)"'),
            ('interim logo', r'data-interim="([^"]+)"'),
            ('outstanding', r'\[OUTSTANDING: ([^\]]+)\]'),
        ):
            for m in re.findall(pattern, html):
                interim.append(f'{rel}: {kind}: {m}')

    css = (SITE / 'assets' / 'site.css').read_text()
    for url in re.findall(r'url\((["\']?)([^)"\']+)\1\)', css):
        if url[1].startswith('http') or (not url[1].startswith('data:') and not target(url[1]).exists()):
            faults.append(f'site.css: bad url {url[1]}')

    total = sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file())
    print(f'Pages: {len(pages)}; files: {sum(1 for f in SITE.rglob("*") if f.is_file())}; total size: {total / 1024:.0f} KB ({total / LIMIT_MB / 1024 / 1024 * 100:.2f}% of {LIMIT_MB} MB)')
    if total > LIMIT_MB * 1024 * 1024 * 0.5:
        faults.append('package is over half of the hosting allowance')

    print(f'\nInterim content ({len(interim)}):' if interim else '\nInterim content: none')
    for line in interim:
        print('  ' + line)
    print(f'\nFaults ({len(faults)}):' if faults else '\nFaults: none')
    for line in faults:
        print('  ' + line)
    if faults:
        return 1
    if release and interim:
        print('\nNot ready to publish: interim content remains (see above).')
        return 1
    print('\nRelease check passed.' if release else '\nPreview check passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
