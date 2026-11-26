const UNLOAD = "There was a message from the client saying they want the whole proposal restructured by Monday. That's my weekend gone, and we'd planned to see Tom's parents. Tom was lovely about it, but I could tell he was disappointed.";
const shot = async (name) => { await tidy(p); await p.screenshot({ path: `shots/${name}.png` }); await p.screenshot({ path: `shots/${name}-full.png`, fullPage: true }); };
await click(/Continue without signing in/i); await p.waitForTimeout(800);
await click(/^Begin$/i); await p.waitForTimeout(800);
await click(/^Continue/i); await p.waitForTimeout(1200);
await p.getByText(/I explicitly agree/).first().click(); await p.waitForTimeout(600);
await p.getByText('No', { exact: true }).first().click(); await p.waitForTimeout(600);
await click(/^Continue/i); await p.waitForTimeout(1500);
await click(/Begin tonight/i); await p.waitForTimeout(1500);
await p.locator('textarea').first().fill(UNLOAD); await p.locator('textarea').first().blur(); await p.evaluate(() => { const t = document.querySelector('textarea'); t.scrollTop = 0; }); await p.waitForTimeout(600);
await shot('1-unload');
await click(/^Continue$/i); await p.waitForTimeout(2500); await step('sort');
await shot('2-sort');
for (const r of await p.getByRole('radio', { name: /^Reflect first/ }).all()) { await r.click(); await p.waitForTimeout(300); }
await step('sorted');
await click(/Continue to reflect/i); await p.waitForTimeout(3500); await step('reflect');
await shot('3-reflect');
await click(/Continue to let it drift/i); await p.waitForTimeout(3000); await step('drift');
await shot('4-drift');

for (let i = 0; i < 6; i++) {
  const txt = await p.evaluate(() => document.body.innerText);
  if (/STEP 5 OF 5/.test(txt)) break;
  const c = p.getByRole('button', { name: /^Continue$/ });
  const n = await c.count(); if (!n) break;
  await c.last().click().catch(() => {}); await p.waitForTimeout(2500);
}
await step('rest');
await shot('5-rest');
