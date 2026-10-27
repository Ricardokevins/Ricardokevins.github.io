#!/usr/bin/env node
// Requires Playwright, a local Chromium/Chrome, and Python 3 with pypdf.
// No existing browser is used; numbered contents are checked in two passes.
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const mathjaxPath = process.env.MATHJAX_PATH || path.join(root, 'notes/assets/mathjax-3.2.2/es5/tex-svg.js');
const { execFileSync } = require('node:child_process');
const books = require('./interview_books.json').books;
const studyHints = Object.fromEntries(Object.entries(books).map(([key, book]) => [key, book.studyHint]));

const printCSS = `
@page { size: A4; margin: 17mm 15mm 18mm; }
.notes-shell-page *, .notes-shell-page *::before, .notes-shell-page *::after {
  box-shadow: none !important; text-shadow: none !important;
  filter: none !important; backdrop-filter: none !important;
}
html, body.notes-shell-page, .notes-shell-page .chapter-page {
  background: #fff !important; background-image: none !important;
}
.notes-shell-page .visual-lead { box-shadow: none !important; background: white !important; }

html, body.notes-shell-page { background: #fff !important; color: #202020; font-size: 10.5pt; line-height: 1.65; }
.notes-sitebar, .sidebar, .mobile-tools, .chapter-nav, .anchor-link, .no-print, .filters, .search-box, .back-to-top { display: none !important; }
.layout, main, main.content { display: block !important; width: 100% !important; max-width: none !important; margin: 0 !important; padding: 0 !important; }
.book-cover { break-after: page; padding-top: 36mm; }
.book-cover h1 { font-size: 30pt; line-height: 1.3; }
.pdf-contents { break-after: page; position: static; width: 100%; height: auto; }
.pdf-contents ol { padding-left: 1.5em; }
.pdf-contents li { margin: 3pt 0; position: relative; padding-right: 35pt; }
.pdf-page-number { position: absolute; right: 0; top: 0; color: #555; font-variant-numeric: tabular-nums; }
.pdf-contents .toc-topic { margin-left: 1em; font-size: 9pt; }
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
.math-display, .formula, .equation { break-inside: avoid !important; }
mjx-container:not([display="true"]) { display: inline-block; vertical-align: middle; }
.notes-shell-page mjx-container { break-inside: avoid !important; page-break-inside: avoid !important; }
.notes-shell-page mjx-container * { max-width: none; }
.notes-shell-page mjx-container[jax="SVG"] > svg { height: revert; max-width: none; }
.study-priority { padding: 3pt 6pt; font-size: 9pt; background: #f4eee3; }
.priority-core { color: #792b19; background: #fff0df; }
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
    const html = await page.evaluate(({ docs, title, combined, replaceToc, detailToc, studyHint, printCSS, mathjaxURL, rootURL }) => {
      const parser = new DOMParser();
      // Short ASCII destinations avoid PDF Name-length warnings for long CJK IDs.
      const pdfId = (index, value) => {
        let hash = 2166136261;
        for (let n = 0; n < value.length; n++) hash = Math.imul(hash ^ value.charCodeAt(n), 16777619) >>> 0;
        return 'b' + index + '-a' + hash.toString(16);
      };
      const parsed = docs.map(({ html, url }, i) => {
        const doc = parser.parseFromString(html, 'text/html');
        const main = doc.querySelector('main');
        if (!main) throw new Error(`Missing main: ${url}`);
        if (replaceToc) main.querySelectorAll('nav.toc').forEach(el => el.remove());
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
        main.querySelectorAll('.worked-example').forEach((card, n) => {
          const first = card.querySelector(':scope > p');
          if (first && /^(例题|练习|第.{1,6}题)/.test(first.textContent.trim())) {
            const heading = doc.createElement('h4'); heading.innerHTML = first.innerHTML;
            heading.id = first.id || 'worked-question-' + n; first.replaceWith(heading);
          }
        });
        main.querySelectorAll('h2, h3, h4').forEach((el, n) => { if (!el.id) el.id = `section-${n}`; });
        const assignedIds = new Set();
        main.querySelectorAll('[id]').forEach(el => {
          const id = pdfId(i, el.id);
          if (assignedIds.has(id)) throw new Error('Duplicate PDF destination: ' + el.id);
          assignedIds.add(id); el.id = id;
        });
        main.querySelectorAll('[src], [href]').forEach(el => {
          for (const attr of ['src', 'href']) {
            const value = el.getAttribute(attr);
            if (!value) continue;
            if (attr === 'href' && value.startsWith('#')) el.setAttribute(attr, '#' + pdfId(i, decodeURIComponent(value.slice(1))));
            else el.setAttribute(attr, new URL(value, url).href);
          }
        });
        // Cross-chapter relative links become intra-document PDF destinations.
        main.querySelectorAll('a[href]').forEach(el => {
          if (el.getAttribute('href').startsWith('#')) return;
          const dest = new URL(el.getAttribute('href'), url);
          const match = docs.findIndex(d => d.url === dest.href.split('#')[0]);
          if (match >= 0) el.setAttribute('href', dest.hash ? '#' + pdfId(match, decodeURIComponent(dest.hash.slice(1))) : '#book-' + match);
          else if (dest.href.startsWith(rootURL)) el.setAttribute('href', 'https://ricardokevins.github.io/' + dest.href.slice(rootURL.length));
        });
        const heading = main.querySelector('h1, h2');
        return { text: docs.length > 1 ? doc.title.replace(/ - 量化面试通用题解手册$/, '') : heading ? heading.textContent : doc.title, html: main.innerHTML, id: `book-${i}` };
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
      // SVG outlines keep stretched brackets, radicals and fraction rules
      // together during Chromium's PDF pagination and do not depend on math fonts.
      const mathConfig = first.createElement('script');
      mathConfig.textContent = 'window.MathJax=window.MathJax||{};window.MathJax.svg={fontCache:"local"};';
      const mathScript = first.querySelector('script[src]');
      if (mathScript) mathScript.before(mathConfig);
      first.title = title;
      first.querySelector('body').className = 'notes-shell-page';
      first.querySelector('body').innerHTML = '';
      const style = first.createElement('style'); style.textContent = printCSS; first.head.append(style);
      const main = first.createElement('main');
      const cover = first.createElement('header'); cover.className = 'book-cover';
      const topId = pdfId(0, 'top');
      if (!parsed[0].html.includes('id="' + topId + '"')) cover.id = topId;
      const h1 = first.createElement('h1'); h1.textContent = title; cover.append(h1);
      const p = first.createElement('p'); p.textContent = '离线学习版 · 题型方法、逐步讲解与练习'; cover.append(p); main.append(cover);
      const aim = first.createElement('h2'); aim.textContent = '复习目标：量化笔试与面试'; cover.append(aim);
      const hint = first.createElement('p'); hint.textContent = studyHint; cover.append(hint);
      const toc = first.createElement('nav'); toc.className = 'pdf-contents';
      const h2 = first.createElement('h2'); h2.textContent = '目录'; toc.append(h2);
      const list = first.createElement('ol');
      const tocItems = [];
      if (parsed.length > 1) for (const part of parsed) {
        tocItems.push({ id: part.id, text: part.text });
        if (detailToc) {
          const holder = first.createElement('div'); holder.innerHTML = part.html;
          holder.querySelectorAll('h3[id]').forEach(el => tocItems.push({ id: el.id, text: el.textContent, topic: true }));
        }
      }
      if (parsed.length === 1) {
        const holder = first.createElement('div'); holder.innerHTML = parsed[0].html;
        holder.querySelectorAll('h2[id]').forEach(el => tocItems.push({ id: el.id, text: el.textContent }));
      }
      for (const item of tocItems) {
        const li = first.createElement('li'); const a = first.createElement('a');
        a.href = `#${item.id}`; a.textContent = item.text; li.append(a); if (item.topic) li.className = 'toc-topic'; list.append(li);
      }
      toc.append(list); if (tocItems.length) main.append(toc);
      for (const part of parsed) {
        const article = first.createElement('article'); article.className = 'book-chapter';
        article.id = part.id; article.innerHTML = part.html; main.append(article);
      }
      first.body.append(main);
      return '<!doctype html>\n' + first.documentElement.outerHTML;
    }, { docs, title: book.title, combined: key === 'complete', replaceToc: true, detailToc: ['regression', 'statistics'].includes(key), studyHint: studyHints[key], printCSS,
      mathjaxURL: pathToFileURL(path.resolve(mathjaxPath)).href,
      rootURL: pathToFileURL(root + path.sep).href });
    const temporaryHTML = path.join(temporary, 'book.html');
    await fs.writeFile(temporaryHTML, html);
    // A4 minus 15mm margins is 680 CSS pixels. Typeset and measure formulas at
    // the actual paper content width, rather than the default desktop viewport.
    await page.setViewportSize({ width: 680, height: 990 });
    await page.emulateMedia({ media: 'print' });
    await page.goto(pathToFileURL(temporaryHTML).href, { waitUntil: 'load', timeout: 180000 });
    await page.evaluate(async () => {
      if (document.querySelector('script[src*="mathjax"],script[src*="tex-chtml"],script[src*="tex-svg"]')) {
        if (!window.MathJax?.startup?.promise) throw new Error('MathJax failed to load; refusing raw-TeX PDF');
        await window.MathJax.startup.promise;
      }
      await document.fonts.ready;
      if ([...document.fonts].some(font => font.status === 'error')) throw new Error('A PDF font failed to load');
      await Promise.all([...document.images].map(img => img.decode()));
      if (document.querySelector('mjx-merror, [data-mjx-error], [data-mml-node="merror"]')) throw new Error('MathJax formula error');
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement.closest('pre, code, script, style, mjx-container') && /\\(?:frac|sqrt|sum|mathbb|begin|theta|alpha)\b/.test(node.textContent)) {
          throw new Error(`Unrendered formula: ${node.textContent.slice(0, 160)}`);
        }
        if (!node.parentElement.closest('pre, script, style, mjx-container') && /[_^]\{[^}]+\}/.test(node.textContent)) {
          throw new Error(`Bare mathematical subscript/superscript: ${node.textContent.slice(0, 160)}`);
        }
        if (node.parentElement.closest('code') && !node.parentElement.closest('pre') && /[∫∑Σ]|[_^]\{|\\(?:frac|sqrt|sum)\b/.test(node.textContent)) {
          throw new Error(`Mathematics placed in a code label: ${node.textContent.slice(0, 160)}`);
        }
      }
    });
    await page.emulateMedia({ media: 'print' });
    // Fit wide inline as well as display equations within their paper column.
    await page.evaluate(() => document.querySelectorAll('mjx-container').forEach(el => {
      const inner = el.querySelector('mjx-math, svg');
      if (inner?.tagName.toLowerCase() === 'svg') {
        inner.style.height = inner.getAttribute('height');
        inner.style.width = inner.getAttribute('width');
      }
      if (inner && el.clientWidth > 0 && inner.getBoundingClientRect().width > el.clientWidth) {
        el.style.fontSize = `${Math.floor(100 * el.clientWidth / inner.getBoundingClientRect().width)}%`;
      }
    }));
    await page.evaluate(async () => {
      await document.fonts.ready;
      for (const el of document.querySelectorAll('mjx-container')) {
        const inner = el.querySelector('mjx-math, svg');
        if (!inner) continue;
        const box = inner.getBoundingClientRect();
        const parent = el.getBoundingClientRect();
        if (box.width > parent.width + 2 || box.right > document.documentElement.clientWidth + 2 || box.left < -2) {
          throw new Error(`Formula exceeds paper column: ${el.textContent.slice(0, 100)}`);
        }
        if (parseFloat(getComputedStyle(el).fontSize) < 9) {
          throw new Error('Formula reduced below readable size; split its source equation');
        }
      }
    });
    const output = path.join(root, 'notes/downloads', book.file);
    await fs.mkdir(path.dirname(output), { recursive: true });
    const draftPDF = path.join(temporary, 'book.pdf');
    const pdfOptions = { path: draftPDF, format: 'A4', printBackground: true, preferCSSPageSize: true,
      tagged: true, outline: true, displayHeaderFooter: true,
      headerTemplate: '<span></span>', footerTemplate: '<div style="font-size:9px;width:100%;text-align:center;color:#666"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' };
    const hasDecoration = await page.evaluate(() => [...document.querySelectorAll('main *')].some(el => {
      const s = getComputedStyle(el); return s.boxShadow !== 'none' || s.filter !== 'none';
    }));
    if (hasDecoration) throw new Error('A screen shadow/filter survived PDF styles');
    await page.pdf(pdfOptions);
    const destinations = () => JSON.parse(execFileSync('python3',
      [path.join(root, 'scripts/pdf_destinations.py'), draftPDF], { encoding: 'utf8', maxBuffer: 5 * 1024 * 1024 }));
    const firstDestinations = destinations();
    await page.evaluate(data => {
      for (const a of document.querySelectorAll('.pdf-contents a')) {
        const id = decodeURIComponent(a.hash.slice(1));
        if (!data.destinations[id]) throw new Error('Missing PDF contents destination: ' + id);
        const label = document.createElement('span'); label.className = 'pdf-page-number';
        label.textContent = data.destinations[id]; a.parentElement.append(label);
      }
    }, firstDestinations);
    await page.pdf(pdfOptions);
    const finalDestinations = destinations();
    if (JSON.stringify(firstDestinations) !== JSON.stringify(finalDestinations)) {
      throw new Error('Page-number labels changed pagination; refusing unstable contents');
    }
    // Readers must never observe the first pass or a half-written second pass.
    const pendingPDF = output.replace(/\.pdf$/, '.pending.pdf');
    await fs.copyFile(draftPDF, pendingPDF);
    await fs.rename(pendingPDF, output);
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
  try { for (const key of selected.length ? selected : Object.keys(books).filter(key => !books[key].archive)) await exportBook(browser, key, books[key]); }
  finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
