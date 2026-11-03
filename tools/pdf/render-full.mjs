// Render a set of Markdown documents into one styled, bookmarked PDF.
// Usage: node render-full.mjs --out out.pdf --title "..." --subtitle "..." file1.md file2.md ...
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Marked } from 'marked';
import hljs from 'highlight.js';
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { PDFDocument } from 'pdf-lib';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = { out: 'out.pdf', title: 'Document', subtitle: '', version: '', date: '', files: [] };
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === '--out') opt.out = args[++i];
  else if (a === '--title') opt.title = args[++i];
  else if (a === '--subtitle') opt.subtitle = args[++i];
  else if (a === '--version') opt.version = args[++i];
  else if (a === '--date') opt.date = args[++i];
  else opt.files.push(a);
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = (s) => String(s).toLowerCase().replace(/<[^>]+>/g, '').replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s+/g, '-');

const chapters = [];
opt.files.forEach((file, idx) => {
  const md = fs.readFileSync(file, 'utf8');
  const prefix = `c${idx + 1}-`;
  const headings = [];
  const seen = new Map();
  const marked = new Marked({ gfm: true });
  marked.use({
    renderer: {
      heading({ tokens, depth }) {
        const text = this.parser.parseInline(tokens);
        let id = prefix + slug(text);
        const n = seen.get(id) || 0;
        seen.set(id, n + 1);
        if (n) id += `-${n}`;
        headings.push({ depth, text, id });
        return `<h${depth} id="${id}">${text}</h${depth}>\n`;
      },
      code({ text, lang }) {
        const l = (lang || '').trim().split(/\s+/)[0];
        if (l === 'mermaid') return `<figure class="diagram"><pre class="mmd-src">${esc(text)}</pre></figure>\n`;
        let html;
        try {
          html = l && hljs.getLanguage(l) ? hljs.highlight(text, { language: l }).value : esc(text);
        } catch { html = esc(text); }
        return `<pre class="code"><code class="hljs${l ? ' lang-' + esc(l) : ''}">${html}</code></pre>\n`;
      },
      link({ href, title, tokens }) {
        const text = this.parser.parseInline(tokens);
        // Intra-repo links to other markdown files -> plain text (they're all in this PDF)
        if (href && /\.md(#.*)?$/.test(href) && !/^https?:/.test(href)) return `<span class="xref">${text}</span>`;
        if (href && href.startsWith('#')) return `<a href="#${prefix}${href.slice(1)}">${text}</a>`;
        return `<a href="${esc(href)}"${title ? ` title="${esc(title)}"` : ''}>${text}</a>`;
      },
      table(token) {
        // default rendering, wrapped for styling
        let header = '<tr>' + token.header.map((c, i) => `<th${token.align[i] ? ` style="text-align:${token.align[i]}"` : ''}>${this.parser.parseInline(c.tokens)}</th>`).join('') + '</tr>';
        let body = token.rows.map((r) => '<tr>' + r.map((c, i) => `<td${token.align[i] ? ` style="text-align:${token.align[i]}"` : ''}>${this.parser.parseInline(c.tokens)}</td>`).join('') + '</tr>').join('\n');
        return `<div class="table-wrap"><table><thead>${header}</thead><tbody>${body}</tbody></table></div>\n`;
      },
    },
  });
  const html = marked.parse(md);
  const h1 = headings.find((h) => h.depth === 1);
  const clean = (t) => t.replace(/^\s*\d+\s*[—:–-]\s*/, '');
  if (h1) h1.text = clean(h1.text);
  chapters.push({ file, html, headings, title: h1 ? h1.text : path.basename(file), id: h1 ? h1.id : prefix + 'top' });
});

const fontCss = [
  '@fontsource/inter/400.css', '@fontsource/inter/500.css', '@fontsource/inter/600.css', '@fontsource/inter/700.css', '@fontsource/inter/800.css',
  '@fontsource/ibm-plex-sans-arabic/400.css', '@fontsource/ibm-plex-sans-arabic/500.css', '@fontsource/ibm-plex-sans-arabic/600.css', '@fontsource/ibm-plex-sans-arabic/700.css',
  '@fontsource/jetbrains-mono/400.css', '@fontsource/jetbrains-mono/600.css',
].map((p) => `<link rel="stylesheet" href="node_modules/${p}">`).join('\n');

const toc = chapters.map((c, i) => {
  const subs = c.headings.filter((h) => h.depth === 2).map((h) => `<li><a href="#${h.id}">${h.text}</a></li>`).join('');
  return `<li class="toc-ch"><a href="#${c.id}"><span class="toc-num">${String(i + 1).padStart(2, '0')}</span>${c.title}</a>${subs ? `<ol class="toc-sub">${subs}</ol>` : ''}</li>`;
}).join('\n');

const arch = `<svg class="arch" viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E0A458"/><stop offset="1" stop-color="#C9803A"/></linearGradient></defs>
  <path d="M20 240 V110 A80 80 0 0 1 180 110 V240" fill="none" stroke="url(#g)" stroke-width="14"/>
  <path d="M50 240 V118 A50 50 0 0 1 150 118 V240" fill="none" stroke="#7FB7BE" stroke-width="6" opacity=".9"/>
  <path d="M100 40 l10 18 h-20z" fill="#E0A458"/>
  <rect x="88" y="150" width="24" height="90" rx="4" fill="#7FB7BE" opacity=".35"/>
</svg>`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${esc(opt.title)}</title>
${fontCss}
<link rel="stylesheet" href="node_modules/highlight.js/styles/github.css">
<style>
:root{--ink:#16232A;--muted:#5B6B73;--brand:#0F4C5C;--brand-2:#1F6F7F;--accent:#E0A458;--sky:#7FB7BE;--line:#DCE3E5;--soft:#F3F6F6;--sand:#FBF6EE;}
@page{size:A4;margin:18mm 16mm 20mm 16mm;}
@page cover{margin:0;}
@page wide{size:A4 landscape;margin:14mm 14mm 18mm 14mm;}
figure.diagram.wide{page:wide;break-before:page;break-after:page;border:0;background:none;padding:0;margin:0}
figure.diagram.wide svg{max-height:160mm}
figure.diagram.wide .wide-caption{text-align:left;margin:0 0 4mm}
*{box-sizing:border-box}
html{font-size:10pt}
body{margin:0;color:var(--ink);font-family:Inter,"IBM Plex Sans Arabic",system-ui,sans-serif;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}
p,li,td,th,blockquote,figcaption{unicode-bidi:plaintext}
.cover{page:cover;height:297mm;width:210mm;position:relative;overflow:hidden;background:linear-gradient(160deg,#0B3A47 0%,#0F4C5C 55%,#145E6F 100%);color:#fff;break-after:page}
.cover .pattern{position:absolute;inset:0;opacity:.07;background-image:radial-gradient(circle at 1px 1px,#fff 1px,transparent 0);background-size:14px 14px}
.cover .arch{position:absolute;right:18mm;top:38mm;width:70mm}
.cover .inner{position:absolute;left:20mm;right:20mm;bottom:34mm}
.cover .kicker{letter-spacing:.18em;text-transform:uppercase;font-size:9pt;color:var(--accent);font-weight:600}
.cover h1{font-size:52pt;line-height:1;margin:6mm 0 2mm;font-weight:800;letter-spacing:-.02em;border:0;padding:0;color:#fff}
.cover .ar{font-family:"IBM Plex Sans Arabic";font-size:30pt;color:var(--sky);font-weight:600;margin:0 0 8mm}
.cover .sub{font-size:14pt;max-width:140mm;color:#E6F0F1;font-weight:400}
.cover .meta{margin-top:12mm;display:flex;gap:10mm;font-size:9pt;color:#BFD6D9}
.cover .meta b{display:block;color:#fff;font-weight:600;font-size:10pt}
.cover .band{position:absolute;left:0;right:0;bottom:0;height:10mm;background:var(--accent)}
.toc{break-after:page}
.toc h2{font-size:20pt;color:var(--brand);margin:0 0 6mm;border:0}
.toc ol{list-style:none;padding:0;margin:0}
.toc-ch{margin:0 0 4mm;break-inside:avoid}
.toc-ch>a{display:flex;align-items:baseline;gap:4mm;font-weight:700;font-size:12pt;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:1.5mm}
.toc-num{color:var(--accent);font-weight:800;min-width:9mm}
.toc-sub{columns:2;column-gap:8mm;margin:2mm 0 0 13mm!important;font-size:8.6pt}
.toc-sub li{break-inside:avoid;margin:0 0 .8mm}
.toc-sub a{color:var(--muted);text-decoration:none}
.chapter{break-before:page}
.chapter-head{background:linear-gradient(120deg,var(--brand),var(--brand-2));color:#fff;border-radius:3mm;padding:7mm 8mm;margin-bottom:6mm;position:relative;overflow:hidden}
.chapter-head .n{font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:700}
.chapter-head h1{color:#fff;border:0;margin:1mm 0 0;padding:0;font-size:22pt}
.chapter-head:after{content:"";position:absolute;right:-12mm;top:-12mm;width:48mm;height:48mm;border:5mm solid rgba(224,164,88,.35);border-radius:50%}
h1{font-size:20pt;color:var(--brand);margin:8mm 0 3mm;line-height:1.2}
h2{font-size:14.5pt;color:var(--brand);margin:8mm 0 2.5mm;padding-bottom:1.2mm;border-bottom:2px solid var(--accent);line-height:1.25;break-after:avoid}
h3{font-size:11.5pt;color:var(--ink);margin:6mm 0 2mm;break-after:avoid}
h4{font-size:10.2pt;color:var(--brand-2);margin:4.5mm 0 1.5mm;break-after:avoid}
h5,h6{font-size:9.6pt;margin:4mm 0 1mm;break-after:avoid}
p{margin:0 0 2.6mm}
a{color:var(--brand-2)}
ul,ol{margin:0 0 3mm;padding-left:6mm}
li{margin:0 0 1mm}
li>ul,li>ol{margin-top:1mm}
strong{color:#0d1b21}
hr{border:0;border-top:1px solid var(--line);margin:6mm 0}
blockquote{margin:0 0 3mm;padding:2.5mm 4mm;background:var(--sand);border-left:3px solid var(--accent);border-radius:0 2mm 2mm 0;color:#4a3a22}
blockquote p:last-child{margin:0}
code{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:8.3pt;background:var(--soft);padding:.2mm 1.1mm;border-radius:1mm;color:#0B4A57}
pre.code{background:#F7F9FA;border:1px solid var(--line);border-left:3px solid var(--brand-2);border-radius:2mm;padding:3mm 3.5mm;margin:0 0 3.5mm;white-space:pre-wrap;word-break:break-word;font-size:7.8pt;line-height:1.45}
pre.code code{background:none;padding:0;color:#24292e;font-size:inherit}
.table-wrap{margin:0 0 4mm}
table{border-collapse:collapse;width:100%;font-size:8.2pt;line-height:1.4}
thead{display:table-header-group}
tr{break-inside:avoid}
th{background:var(--brand);color:#fff;text-align:left;font-weight:600;padding:1.6mm 2mm;border:1px solid var(--brand)}
td{padding:1.4mm 2mm;border:1px solid var(--line);vertical-align:top;overflow-wrap:anywhere}
tbody tr:nth-child(even) td{background:#F8FAFA}
td code,th code{font-size:7.6pt;word-break:normal;overflow-wrap:anywhere}
th code{background:rgba(255,255,255,.15);color:#fff}
figure.diagram{margin:2mm 0 5mm;padding:4mm;border:1px solid var(--line);border-radius:2.5mm;background:#FCFDFD;break-inside:avoid;text-align:center}
figure.diagram svg{max-width:100%!important;height:auto;max-height:225mm}
.mermaid-error{font-size:7.5pt;color:#9a3412;text-align:left}
.xref{color:var(--brand-2);font-weight:600}
input[type=checkbox]{margin-right:1.5mm}
</style></head><body>
<!--COVER-START--><section class="cover"><div class="pattern"></div>${arch}
<div class="inner"><div class="kicker">Design document</div><h1>${esc(opt.title)}</h1><div class="ar">بوابة</div>
<div class="sub">${esc(opt.subtitle)}</div>
<div class="meta"><div><b>Version</b>${esc(opt.version)}</div><div><b>Date</b>${esc(opt.date)}</div><div><b>Status</b>Draft for review</div></div></div>
<div class="band"></div></section><!--COVER-END-->
<section class="toc"><h2>Contents</h2><ol>${toc}</ol></section>
${chapters.map((c, i) => {
  // Replace the chapter's first h1 with a styled head
  const body = c.html.replace(/<h1 id="([^"]+)">([\s\S]*?)<\/h1>/, (_m, id, t) => `<div class="chapter-head"><div class="n">Chapter ${String(i + 1).padStart(2, '0')}</div><h1 id="${id}">${t.replace(/^\s*\d+\s*[—:–-]\s*/, '')}</h1></div>`);
  return `<section class="chapter">${body}</section>`;
}).join('\n')}
<script src="node_modules/mermaid/dist/mermaid.min.js"></script>
</body></html>`;

const coverRe = /<!--COVER-START-->[\s\S]*<!--COVER-END-->/;
const coverHtml = html.replace(/<body>[\s\S]*<\/body>/, '<body>' + html.match(coverRe)[0] + '</body>');
const bodyHtml = html.replace(coverRe, '');
const base = path.join(HERE, path.basename(opt.out, '.pdf'));
fs.writeFileSync(base + '.cover.html', coverHtml);
fs.writeFileSync(base + '.body.html', bodyHtml);

const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', (e) => console.error('pageerror:', e.message));
await page.goto('file://' + base + '.body.html', { waitUntil: 'load' });
const report = await page.evaluate(async () => {
  const m = window.mermaid;
  m.initialize({
    startOnLoad: false, securityLevel: 'loose', theme: 'base',
    fontFamily: 'Inter, "IBM Plex Sans Arabic", sans-serif',
    themeVariables: {
      primaryColor: '#E8F2F3', primaryBorderColor: '#1F6F7F', primaryTextColor: '#16232A',
      secondaryColor: '#FBF1E2', tertiaryColor: '#F3F6F6', lineColor: '#5B6B73',
      clusterBkg: '#F6FAFA', clusterBorder: '#9FC3C8', fontSize: '13px',
      actorBkg: '#E8F2F3', actorBorder: '#1F6F7F', noteBkgColor: '#FBF1E2', noteBorderColor: '#E0A458',
    },
    flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
    sequence: { useMaxWidth: true, mirrorActors: false },
  });
  const nodes = [...document.querySelectorAll('pre.mmd-src')];
  let ok = 0; const failed = []; const layout = [];
  // Usable box (CSS px) inside the figure on a portrait / landscape A4 page.
  const PORT = { w: 630, h: 830 }, LAND = { w: 990, h: 600 };
  const dims = (svg) => {
    const mm = svg.match(/viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)"/);
    return mm ? { w: +mm[1], h: +mm[2] } : { w: 600, h: 400 };
  };
  const fit = (d, box) => Math.min(box.w / d.w, box.h / d.h, 1.25);
  let seq = 0;
  for (let i = 0; i < nodes.length; i++) {
    const el = nodes[i];
    const src = el.textContent;
    try {
      const cands = [src];
      if (/^\s*(flowchart|graph)\s+(LR|RL)\b/m.test(src)) cands.push(src.replace(/^(\s*(?:flowchart|graph)\s+)(LR|RL)\b/m, '$1TB'));
      else if (/^\s*(flowchart|graph)\s+(TB|TD|BT)\b/m.test(src)) cands.push(src.replace(/^(\s*(?:flowchart|graph)\s+)(TB|TD|BT)\b/m, '$1LR'));
      let best = null;
      for (const c of cands) {
        let out;
        try { out = await m.render('mmd' + (seq++), c); } catch (e) { if (c === src) throw e; else continue; }
        document.querySelectorAll('[id^="dmmd"]').forEach((n) => n.remove());
        const d = dims(out.svg);
        const sp = fit(d, PORT), sl = fit(d, LAND);
        const wide = sp < 0.62 && sl > sp * 1.25;
        const score = wide ? sl * 0.97 : sp; // slight preference for staying inline
        if (!best || score > best.score) best = { svg: out.svg, score, wide, d, swapped: c !== src };
      }
      const fig = el.closest('figure');
      if (best.wide && fig) {
        fig.classList.add('wide');
        // Pull an immediately preceding heading onto the landscape page so it isn't orphaned.
        const prev = fig.previousElementSibling;
        if (prev && /^H[2-5]$/.test(prev.tagName)) { prev.classList.add('wide-caption'); fig.prepend(prev); }
      }
      el.outerHTML = best.svg; ok++;
      layout.push({ i, w: Math.round(best.d.w), h: Math.round(best.d.h), wide: best.wide, swapped: best.swapped, scale: +best.score.toFixed(2) });
    } catch (e) {
      failed.push({ i, err: String(e && e.message || e).slice(0, 200), head: src.slice(0, 80) });
      const pre = document.createElement('pre'); pre.className = 'code'; pre.textContent = src;
      const note = document.createElement('div'); note.className = 'mermaid-error'; note.textContent = 'Diagram source (could not be rendered):';
      el.replaceWith(note, pre);
    }
    document.querySelectorAll('[id^="dmmd"]').forEach((n) => n.remove());
  }
  await document.fonts.ready;
  return { ok, failed, total: nodes.length, layout };
});
console.log(JSON.stringify(report, null, 1));

const footer = `<div style="width:100%;font-family:Arial,sans-serif;font-size:7pt;color:#7a8a90;padding:0 16mm;display:flex;justify-content:space-between;">
<span>${esc(opt.title)} · ${esc(opt.subtitle)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
const bodyPdf = await page.pdf({
  format: 'A4', printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: footer,
  outline: true, tagged: true,
});
const cpage = await browser.newPage();
await cpage.goto('file://' + base + '.cover.html', { waitUntil: 'load' });
await cpage.evaluate(() => document.fonts.ready);
const coverPdf = await cpage.pdf({ format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();

const doc = await PDFDocument.load(bodyPdf);
const cover = await PDFDocument.load(coverPdf);
const [cp] = await doc.copyPages(cover, [0]);
doc.insertPage(0, cp);
doc.setTitle(opt.title + (opt.subtitle ? ' — ' + opt.subtitle : ''));
doc.setAuthor('Bawaba project');
doc.setSubject(opt.subtitle);
fs.writeFileSync(opt.out, await doc.save());
console.log('wrote', opt.out, 'pages:', doc.getPageCount());
