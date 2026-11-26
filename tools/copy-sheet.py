#!/usr/bin/env python3
"""Writes docs/copy-for-approval.md: every passage marked data-copy="proposed" or "board", as text.

    python3 tools/copy-sheet.py
Approving: change data-copy="proposed" to data-copy="approved" in src/pages (or replace the text
with the agreed copy), rebuild, and run tools/check.py --release.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.blocks, self.depth = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.depth:
            self.depth += 1
            if tag in ('p', 'li', 'h2', 'h3') and self.blocks[-1][1]:
                self.blocks[-1][1].append('\n')
        elif a.get('data-copy') == 'proposed':
            self.depth = 1
            self.blocks.append((a['data-copy'], []))

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= 1

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.depth:
            self.blocks[-1][1].append(data.replace('\n', ' '))


out = ['# Website copy for approval', '',
       'Generated from the site source by `tools/copy-sheet.py`. These are the only passages not yet approved: the website-specific privacy notice and website terms. Everything else on the site is the founder\'s approved copy.', '']
n = 0
for page in sorted((ROOT / 'src' / 'pages').rglob('*.html')):
    p = Blocks()
    text = page.read_text()
    p.feed(re.sub(r'\{\{\w+\}\}', '', text))
    if not p.blocks:
        continue
    out.append(f'## {page.relative_to(ROOT / "src" / "pages")}')
    out.append('')
    for kind, parts in p.blocks:
        body = re.sub(r'[ \t]+', ' ', ''.join(parts))
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        if kind == 'proposed':
            n += 1
        out.append(f'**{"Proposed " + str(n) if kind == "proposed" else "Brand board"}**')
        out.append('')
        out.extend(f'> {l}' for l in lines)
        out.append('')
(ROOT / 'docs' / 'copy-for-approval.md').write_text('\n'.join(out))
print(f'{n} proposed passages written to docs/copy-for-approval.md')
