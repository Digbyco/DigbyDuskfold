const { chromium } = require('playwright');
const fs = require('fs');
const S = process.argv[2];
const rec = JSON.parse(fs.readFileSync(`${S}/recorded.json`, 'utf8'));
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
const now = Math.floor(Date.now() / 1000);
const uid = '0f0f0f0f-1111-4222-8333-444455556666';
const jwt = `${b64({ alg: 'HS256', typ: 'JWT' })}.${b64({ sub: uid, role: 'authenticated', aud: 'authenticated', exp: now + 86400, iat: now, is_anonymous: true })}.c2ln`;
const user = { id: uid, aud: 'authenticated', role: 'authenticated', is_anonymous: true, app_metadata: {}, user_metadata: {}, created_at: new Date().toISOString() };
const session = { access_token: jwt, token_type: 'bearer', expires_in: 86400, expires_at: now + 86400, refresh_token: 'local-refresh', user };
const safety = { level: 'ordinary', signals: [], classification: 'complete', blocks: [], allowReflection: true, ritual: 'continue' };
const json = (route, body, status = 200) => route.fulfill({ status, contentType: 'application/json', headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*' }, body: JSON.stringify(body) });
const HIDE = ['DEV', 'PROVISIONAL ARTWORK', 'PROVISIONAL SERIF'];
async function tidy(p) {
  await p.evaluate((HIDE) => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); const n = [];
    while (w.nextNode()) n.push(w.currentNode);
    for (const t of n) if (HIDE.includes(t.nodeValue.trim())) t.parentElement.style.visibility = 'hidden';
    for (const e of document.querySelectorAll('[aria-label]')) if (/^DEV|diagnostics/i.test(e.getAttribute('aria-label'))) e.style.visibility = 'hidden';
  }, HIDE);
}
const btns = async (p) => (await p.$$eval('[role=button],button,[role=radio],[role=checkbox]', (es) => es.map((e) => (e.getAttribute('aria-label') || e.innerText || '').trim().slice(0, 40)))).filter(Boolean).join(' | ');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 3 });
  const p = await ctx.newPage();
  await p.route('http://localhost:8787/**', async (route) => {
    const r = route.request(); const u = new URL(r.url());
    if (r.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*', 'access-control-allow-methods': '*' } });
    console.log('  ->', r.method(), u.pathname);
    if (u.pathname === '/auth/v1/signup' || u.pathname === '/auth/v1/token') return json(route, session);
    if (u.pathname === '/auth/v1/user') return json(route, user);
    if (u.pathname === '/functions/v1/ai-consent') { const body = JSON.parse(r.postData() || '{}'); return json(route, { status: 'granted', version: body.version, recorded_at: new Date().toISOString() }); }
    if (u.pathname === '/functions/v1/ai-unload') return json(route, { screen: { status: 'ok', level: 'ordinary', signals: [] }, safety, extraction: { status: 'ok', output: rec.extraction }, pass: 'local-pass-1' });
    if (u.pathname === '/functions/v1/ai-reflect') { await new Promise((r) => setTimeout(r, 300)); return json(route, { status: 'ok', output: rec.reflection, safety, pass: 'local-pass-2' }); }
    return json(route, { error: 'not_found' }, 404);
  });
  const step = async (name) => { await p.waitForTimeout(1200); console.log(`[${name}]`, (await p.evaluate(() => document.body.innerText)).replace(/\s+/g, ' ').slice(0, 140)); console.log('   buttons:', await btns(p)); };
  const click = async (re) => { await p.getByRole('button', { name: re }).first().click(); };
  await p.goto('http://localhost:8081/'); await step('start');
  fs.writeFileSync(`${S}/steps.txt`, '');
  globalThis.p = p; globalThis.click = click; globalThis.step = step; globalThis.tidy = tidy;
  const script = fs.readFileSync(`${S}/steps.js`, 'utf8');
  await eval(`(async () => { ${script} })()`);
  await b.close();
})();
