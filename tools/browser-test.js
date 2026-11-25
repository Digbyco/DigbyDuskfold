// Browser tests for the built site (preview). Usage:
//   node tools/browser-test.js <base-url> <screenshot-dir> <path-to-axe.min.js>
const { chromium } = require('playwright');
const fs = require('fs');
const [base, outDir, axePath] = process.argv.slice(2);
const PAGES = ['/', '/products/', '/products/duskfold/', '/about/', '/contact/', '/privacy/', '/legal/', '/terms/', '/support/', '/404.html'];
const axe = fs.readFileSync(axePath, 'utf8');
(async () => {
  const b = await chromium.launch();
  const results = [];
  for (const [label, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }], ['narrow', { width: 360, height: 740 }]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    const external = new Set();
    const errors = [];
    p.on('request', (r) => { const u = new URL(r.url()); if (u.origin !== new URL(base).origin) external.add(u.origin); });
    p.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    p.on('pageerror', (e) => errors.push(String(e)));
    for (const path of PAGES) {
      const res = await p.goto(base + path, { waitUntil: 'networkidle' });
      const status = res.status();
      const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      const name = (path.replace(/\//g, '_').replace(/^_|_$/g, '') || 'home').replace('.html', '');
      if (label !== 'narrow') await p.screenshot({ path: `${outDir}/${label}-${name}.png`, fullPage: true });
      let violations = [];
      if (label === 'desktop' || label === 'mobile') {
        await p.addScriptTag({ content: axe });
        const r = await p.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] })).violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} node(s) — ${v.nodes.slice(0, 2).map((n) => n.target.join(' ')).join('; ')}`));
        violations = r;
      }
      let focus = null;
      if (label === 'desktop') {
        // Keyboard: Tab through the page; every focused element must show a visible outline.
        focus = await p.evaluate(() => null);
        const seen = [];
        await p.focus('body');
        for (let i = 0; i < 40; i++) {
          await p.keyboard.press('Tab');
          const f = await p.evaluate(() => {
            const e = document.activeElement; if (!e || e === document.body) return null;
            const s = getComputedStyle(e);
            const r = e.getBoundingClientRect();
            return { tag: e.tagName, text: (e.textContent || '').trim().slice(0, 30), outline: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0, visible: r.width > 0 && r.height > 0 };
          });
          if (!f) break;
          seen.push(f);
        }
        focus = { stops: seen.length, withoutOutline: seen.filter((f) => !f.outline || !f.visible).map((f) => `${f.tag} ${f.text}`) };
      }
      results.push({ view: label, path, status, overflow, violations, focus });
    }
    results.push({ view: label, external: [...external], errors });
    await ctx.close();
  }
  await b.close();
  console.log(JSON.stringify(results, null, 1));
})();
