#!/usr/bin/env node
// Requires Playwright and a local Chromium/Chrome. No existing browser is used.
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const mathjaxPath = process.env.MATHJAX_PATH || path.join(root, 'notes/assets/mathjax-3.2.2/es5/tex-chtml.js');
const books = {
  quant: { title: '量化面试通用题解手册', file: 'quant-interview-handbook.pdf',
    sources: Array.from({ length: 44 }, (_, i) => `notes/quant-interview-question-bank/chapters/${String(i + 1).padStart(3, '0')}.html`) },
  'quant-52': { title: '量化面试 52 道题：完整推导与面试方法', file: 'quant-interview-52.pdf', sources: ['notes/tech-analysis/xiaohongshu-quant-interview-question-bank.html'] },
  'quant-61': { title: '量化面试 61 道同类题：方法迁移', file: 'quant-interview-61.pdf', sources: ['notes/tech-analysis/xiaohongshu-quant-interview-practice-expansion.html'] },
  leetcode: { title: 'LeetCode Hot 100 分类精讲', file: 'leetcode-hot-100.pdf', sources: ['notes/leetcode-hot-100/index.html'] },
  probability: { title: '量化面试：概率论与数理统计', file: 'quant-probability-statistics.pdf', sources: ['notes/quant-foundations/probability-statistics.html'] },
  ml: { title: '量化面试：机器学习理论', file: 'quant-machine-learning.pdf', sources: ['notes/quant-foundations/machine-learning.html'] },
};

const printCSS = `
@page { size: A4; margin: 17mm 15mm 18mm; }
html, body.notes-shell-page { background: #fff !important; color: #202020; font-size: 10.5pt; line-height: 1.65; }
.notes-sitebar, .sidebar, .mobile-tools, .chapter-nav, .anchor-link, .no-print, .filters, .search-box, .back-to-top { display: none !important; }
.layout, main, main.content { display: block !important; width: 100% !important; max-width: none !important; margin: 0 !important; padding: 0 !important; }
.book-cover { break-after: page; padding-top: 36mm; }
.book-cover h1 { font-size: 30pt; line-height: 1.3; }
.pdf-contents { break-after: page; position: static; width: 100%; height: auto; }
.pdf-contents ol { padding-left: 1.5em; }
.pdf-contents li { margin: 3pt 0; }
.book-chapter + .book-chapter { break-before: page; }
.book-chapter, .chapter, .chapter-page, section, article, .qa, .problem, .worked-example, .solution, .derivation, .proof-detail, .supplement { height: auto !important; max-height: none !important; overflow: visible !important; break-inside: auto !important; box-shadow: none !important; }
.chapter-page { padding: 0 !important; border: 0 !important; }
header, footer { width: 100% !important; max-width: none !important; padding: 8pt 0; }
h1 { font-size: 24pt; } h2 { font-size: 19pt; } h3 { font-size: 14pt; } h4 { font-size: 11.5pt; }
h1, h2, h3, h4, h5, summary { break-after: avoid; scroll-margin: 0; }
p, li { orphans: 2; widows: 2; }
pre { font-size: 8pt; line-height: 1.45; background: #f6f6f6 !important; color: #111 !important; padding: 9pt; white-space: pre-wrap !important; overflow: visible !important; break-inside: auto; }
pre code { white-space: pre-wrap !important; overflow-wrap: anywhere !important; color: inherit !important; font-size: inherit !important; }
code { overflow-wrap: anywhere; }
.table-wrap, .table-container, .math-display, .formula, .equation, mjx-container { overflow: visible !important; max-width: 100% !important; }
table { min-width: 0 !important; width: 100% !important; table-layout: auto; font-size: 8.5pt; }
thead { display: table-header-group; } tr { break-inside: avoid; }
th, td { padding: 5pt; overflow-wrap: anywhere; }
img, svg { max-width: 100%; height: auto; break-inside: avoid; }
a { color: #323232; text-decoration: none; }
.stats, .study-lanes, .concept-grid, .grid-2, .grid-3 { display: block !important; }
.stats > *, .study-lanes > *, .concept-grid > *, .grid-2 > *, .grid-3 > * { margin-bottom: 8pt; }
`;

async function exportBook(browser, key, book) {
  const page = await browser.newPage();
  page.setDefaultTimeout(120000);
  const docs = await Promise.all(book.sources.map(async source => ({
    html: await fs.readFile(path.join(root, source), 'utf8'),
    url: pathToFileURL(path.join(root, source)).href,
  })));
  // Retain the first page's stylesheet and MathJax configuration. Rebase all
  // resources and qualify IDs before joining chapters, including PDF TOC links.
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), 'interview-print-'));
  try {
    await page.goto('about:blank');
    const html = await page.evaluate(({ docs, title, printCSS, mathjaxURL, rootURL }) => {
      const parser = new DOMParser();
      const parsed = docs.map(({ html, url }, i) => {
        const doc = parser.parseFromString(html, 'text/html');
        const main = doc.querySelector('main');
        if (!main) throw new Error(`Missing main: ${url}`);
        // Later chapters can use a different MathJax delimiter configuration.
        // Normalize their dollar math before applying the first chapter's config.
        if (docs[i].html.includes("['$', '$']") || docs[i].html.includes('["$", "$"]')) {
          const walker = doc.createTreeWalker(main, NodeFilter.SHOW_TEXT);
          const nodes = [];
          while (walker.nextNode()) nodes.push(walker.currentNode);
          for (const node of nodes) {
            if (node.parentElement.closest('pre, code, script, style')) continue;
            node.textContent = node.textContent
              .replace(/(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$/g, '\\[$1\\]')
              .replace(/(?<![\\$])\$(?!\$)([^$]*?)(?<!\\)\$/g, '\\($1\\)');
          }
        }
        main.querySelectorAll('.chapter-nav, .anchor-link, .no-print, .no-results').forEach(el => el.remove());
        main.querySelectorAll('details').forEach(el => { el.open = true; });
        main.querySelectorAll('h2, h3').forEach((el, n) => { if (!el.id) el.id = `section-${n}`; });
        main.querySelectorAll('[id]').forEach(el => { el.id = `b${i}-${el.id}`; });
        main.querySelectorAll('[src], [href]').forEach(el => {
          for (const attr of ['src', 'href']) {
            const value = el.getAttribute(attr);
            if (!value) continue;
            if (attr === 'href' && value.startsWith('#')) el.setAttribute(attr, `#b${i}-${value.slice(1)}`);
            else el.setAttribute(attr, new URL(value, url).href);
          }
        });
        // Cross-chapter relative links become intra-document PDF destinations.
        main.querySelectorAll('a[href]').forEach(el => {
          if (el.getAttribute('href').startsWith('#')) return;
          const dest = new URL(el.getAttribute('href'), url);
          const match = docs.findIndex(d => d.url === dest.href.split('#')[0]);
          if (match >= 0) el.setAttribute('href', dest.hash ? `#b${match}-${dest.hash.slice(1)}` : `#book-${match}`);
          else if (dest.href.startsWith(rootURL)) el.setAttribute('href', 'https://ricardokevins.github.io/' + dest.href.slice(rootURL.length));
        });
        const heading = main.querySelector('h1, h2');
        return { text: heading ? heading.textContent : doc.title, html: main.innerHTML, id: `book-${i}` };
      });
      const first = parser.parseFromString(docs[0].html, 'text/html');
      first.querySelectorAll('link[href], script[src]').forEach(el => {
        const attr = el.tagName === 'LINK' ? 'href' : 'src';
        el.setAttribute(attr, new URL(el.getAttribute(attr), docs[0].url).href);
      });
      first.querySelectorAll('script[src]').forEach(el => {
        if (!/mathjax|tex-(?:chtml|svg)/i.test(el.src)) el.remove();
        else if (mathjaxURL) el.src = mathjaxURL;
      });
      first.title = title;
      first.querySelector('body').className = 'notes-shell-page';
      first.querySelector('body').innerHTML = '';
      const style = first.createElement('style'); style.textContent = printCSS; first.head.append(style);
      const main = first.createElement('main');
      const cover = first.createElement('header'); cover.className = 'book-cover';
      if (!parsed[0].html.includes('id="b0-top"')) cover.id = 'b0-top';
      const h1 = first.createElement('h1'); h1.textContent = title; cover.append(h1);
      const p = first.createElement('p'); p.textContent = '离线学习版 · 题型方法、逐步讲解与练习'; cover.append(p); main.append(cover);
      const toc = first.createElement('nav'); toc.className = 'pdf-contents';
      const h2 = first.createElement('h2'); h2.textContent = '目录'; toc.append(h2);
      const list = first.createElement('ol');
      const tocItems = parsed.length > 1 ? parsed.map(p => ({ id: p.id, text: p.text })) : [];
      if (parsed.length === 1) {
        const holder = first.createElement('div'); holder.innerHTML = parsed[0].html;
        holder.querySelectorAll('h2[id]').forEach(el => tocItems.push({ id: el.id, text: el.textContent }));
      }
      for (const item of tocItems) {
        const li = first.createElement('li'); const a = first.createElement('a');
        a.href = `#${item.id}`; a.textContent = item.text; li.append(a); list.append(li);
      }
      toc.append(list); if (tocItems.length) main.append(toc);
      for (const part of parsed) {
        const article = first.createElement('article'); article.className = 'book-chapter';
        article.id = part.id; article.innerHTML = part.html; main.append(article);
      }
      first.body.append(main);
      return '<!doctype html>\n' + first.documentElement.outerHTML;
    }, { docs, title: book.title, printCSS,
      mathjaxURL: pathToFileURL(path.resolve(mathjaxPath)).href,
      rootURL: pathToFileURL(root + path.sep).href });
    const temporaryHTML = path.join(temporary, 'book.html');
    await fs.writeFile(temporaryHTML, html);
    await page.goto(pathToFileURL(temporaryHTML).href, { waitUntil: 'load', timeout: 180000 });
    await page.evaluate(async () => {
      if (document.querySelector('script[src*="mathjax"],script[src*="tex-chtml"],script[src*="tex-svg"]')) {
        if (!window.MathJax?.startup?.promise) throw new Error('MathJax failed to load; refusing raw-TeX PDF');
        await window.MathJax.startup.promise;
      }
      await document.fonts.ready;
      await Promise.all([...document.images].map(img => img.decode()));
      if (document.querySelector('mjx-merror, [data-mjx-error]')) throw new Error('MathJax formula error');
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement.closest('pre, code, script, style, mjx-container') && /\\(?:frac|sqrt|sum|mathbb|begin|theta|alpha)\b/.test(node.textContent)) {
          throw new Error(`Unrendered formula: ${node.textContent.slice(0, 160)}`);
        }
      }
    });
    await page.emulateMedia({ media: 'print' });
    // Fit the rare wide display equation instead of clipping its right side.
    await page.evaluate(() => document.querySelectorAll('mjx-container[display="true"]').forEach(el => {
      const inner = el.querySelector('mjx-math, svg');
      if (inner && inner.getBoundingClientRect().width > el.clientWidth) {
        el.style.fontSize = `${Math.floor(100 * el.clientWidth / inner.getBoundingClientRect().width)}%`;
      }
    }));
    const output = path.join(root, 'notes/downloads', book.file);
    await fs.mkdir(path.dirname(output), { recursive: true });
    await page.pdf({ path: output, format: 'A4', printBackground: true, preferCSSPageSize: true,
      tagged: true, outline: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:9px;width:100%;text-align:center;color:#666"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
    const stats = await page.evaluate(() => ({ chapters: document.querySelectorAll('.book-chapter').length,
      formulas: document.querySelectorAll('mjx-container').length, characters: document.querySelector('main').innerText.length }));
    console.log(JSON.stringify({ book: key, output: path.relative(root, output), ...stats }));
  } finally {
    await page.close();
    await fs.rm(temporary, { recursive: true, force: true });
  }
}

(async () => {
  const selected = process.argv.slice(2);
  if (selected.some(key => !books[key])) throw new Error(`Choose from: ${Object.keys(books).join(', ')}`);
  const browser = await chromium.launch({ headless: true,
    ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  try { for (const key of selected.length ? selected : Object.keys(books)) await exportBook(browser, key, books[key]); }
  finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
