// Render the fixed-page visual overview HTML to PDF (+ optional PNG previews for QA).
// Usage: node render-overview.mjs overview/overview.html out.pdf [--shots dir] [--title "..."]
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const { PDFDocument } = require('pdf-lib');

const [, , src, out, ...rest] = process.argv;
const shotsIdx = rest.indexOf('--shots');
const shots = shotsIdx >= 0 ? rest[shotsIdx + 1] : null;
const titleIdx = rest.indexOf('--title');
const title = titleIdx >= 0 ? rest[titleIdx + 1] : 'Bawaba — Visual Design Overview';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto('file://' + path.resolve(src), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);

// Overflow check: any .page whose content overflows its box.
const overflow = await page.evaluate(() => {
  const res = [];
  document.querySelectorAll('.page').forEach((p, i) => {
    const pr = p.getBoundingClientRect();
    let maxBottom = 0;
    p.querySelectorAll('*').forEach((el) => {
      if (el.closest('.page-foot') || el.classList.contains('pattern') || el.classList.contains('band')) return;
      const r = el.getBoundingClientRect();
      if (r.height > 0) maxBottom = Math.max(maxBottom, r.bottom - pr.top);
    });
    const limit = pr.height - 17 * 3.78; // bottom padding area (footer zone)
    if (maxBottom > limit + 2) res.push({ page: i + 1, over_px: Math.round(maxBottom - limit), id: p.id || '' });
  });
  return res;
});

const pdfBuf = await page.pdf({ format: 'A4', printBackground: true, preferCSSPageSize: true, tagged: true });
const doc = await PDFDocument.load(pdfBuf);
doc.setTitle(title);
doc.setAuthor('Bawaba project');
fs.writeFileSync(out, await doc.save());

if (shots) {
  fs.mkdirSync(shots, { recursive: true });
  const n = await page.evaluate(() => document.querySelectorAll('.page').length);
  await page.emulateMedia({ media: 'print' });
  for (let i = 0; i < n; i++) {
    const el = (await page.$$('.page'))[i];
    await el.screenshot({ path: path.join(shots, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
}
await browser.close();
console.log(JSON.stringify({ out, pages: doc.getPageCount(), overflow, errors }, null, 1));
