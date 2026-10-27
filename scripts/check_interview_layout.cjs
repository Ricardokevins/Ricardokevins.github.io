#!/usr/bin/env node
// Regression check: mobile books must expose the body outside the TOC scrollbox.
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const mathjaxPath = process.env.MATHJAX_PATH || path.join(root, 'notes/assets/mathjax-3.2.2/es5/tex-chtml.js');
const assert = (condition, message) => { if (!condition) throw new Error(message); };

(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  let checked = 0;
  const screenshots = process.env.SCREENSHOT_DIR;
  if (screenshots) await fs.mkdir(screenshots, { recursive: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true });
    page.setDefaultNavigationTimeout(120000);
    await page.route(/https:.*(?:mathjax@[^/]+|mathjax\/[^/]+)\/es5\//, async route => {
      const asset = route.request().url().split('/es5/')[1];
      const file = path.resolve(path.dirname(mathjaxPath), asset);
      assert(file.startsWith(path.dirname(mathjaxPath)), 'Invalid MathJax asset');
      await route.fulfill({ body: await fs.readFile(file), contentType: file.endsWith('.js') ? 'application/javascript' : 'font/woff', headers: { 'access-control-allow-origin': '*' } });
    });
    const inspect = async (source, width, screenshot = false) => {
      await page.setViewportSize({ width, height: 844 });
      const errors = [];
      const errorListener = err => errors.push(err.message);
      page.on('pageerror', errorListener);
      await page.goto(pathToFileURL(path.join(root, source)).href, { waitUntil: 'load' });
      await page.evaluate(async () => {
        if (document.querySelector('script[src*="mathjax"]') && !window.MathJax?.startup?.promise) throw new Error('MathJax did not load');
        if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
        await document.fonts.ready;
      });
      const state = await page.evaluate(() => {
        const main = document.querySelector('main');
        const sidebar = document.querySelector('.sidebar');
        const rect = main.getBoundingClientRect();
        return { width: innerWidth, documentWidth: document.documentElement.scrollWidth,
          mainWidth: rect.width, text: main.innerText.length,
          sidebarHeight: sidebar?.getBoundingClientRect().height,
          sidebarPosition: sidebar && getComputedStyle(sidebar).position,
          mathErrors: document.querySelectorAll('mjx-merror, [data-mjx-error]').length,
          brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src) };
      });
      assert(state.documentWidth <= width + 1, `${source} @${width}: page overflow ${state.documentWidth}`);
      assert(state.mainWidth > width * (width <= 980 ? .8 : .3), `${source}: body squeezed`);
      assert(state.text > 50, `${source}: missing body text`);
      assert(!state.mathErrors, `${source}: formula errors`);
      assert(!state.brokenImages.length, `${source}: broken images ${state.brokenImages}`);
      assert(!errors.length, `${source}: browser errors ${errors}`);
      const formulaScroll = await page.evaluate(() => {
        const el = [...document.querySelectorAll('mjx-container')].find(e => e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 2);
        if (!el) return true;
        el.scrollLeft = el.scrollWidth;
        const scrolls = el.scrollLeft > 0;
        el.scrollLeft = 0;
        return scrolls;
      });
      assert(formulaScroll, `${source}: wide formula is clipped instead of scrollable`);
      if (width <= 980 && state.sidebarHeight) {
        assert(state.sidebarPosition === 'static', `${source}: sticky mobile sidebar`);
        assert(state.sidebarHeight < 844, `${source}: mobile directory consumes entire screen`);
      }
      if (source.includes('quant-interview-question-bank/')) {
        const open = await page.locator('.book-directory').evaluate(el => el.open);
        assert(open === (width > 980), `${source}: wrong mobile directory state`);
      }
      await page.locator('main').evaluate(el => el.scrollIntoView({ block: 'start', behavior: 'instant' }));
      const reached = await page.locator('main').evaluate(el => {
        const r = el.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 70;
      });
      assert(reached, `${source}: body unreachable`);
      if (source === 'notes/leetcode-hot-100/index.html' && width === 390) {
        await page.locator('#problem-search').fill('416');
        assert(await page.locator('.problem:not([hidden])').count() === 1, 'Hot 100 search must find LC 416');
        await page.emulateMedia({ media: 'print' });
        const printed = await page.locator('.problem').evaluateAll(els => els.filter(el => getComputedStyle(el).display !== 'none').length);
        assert(printed === 100, 'Printing a filtered Hot 100 must retain all 100 solutions');
        await page.emulateMedia({ media: 'screen' });
        await page.locator('#show-all').click();
        assert(await page.locator('.problem:not([hidden])').count() === 100, 'Hot 100 clear search');
      }
      if (screenshots && screenshot) await page.screenshot({ path: path.join(screenshots, `${source.replaceAll('/', '_')}-${width}.png`) });
      page.off('pageerror', errorListener);
      checked++;
    };
    for (const bank of ['quant-interview-question-bank', 'math-interview-question-bank', 'llm-interview-question-bank']) {
      for (const width of [320, 390, 768, 980, 1440]) await inspect(`notes/${bank}/index.html`, width, width === 390);
    }
    for (const file of (await fs.readdir(path.join(root, 'notes/quant-interview-question-bank/chapters'))).filter(f => f.endsWith('.html'))) {
      await inspect(`notes/quant-interview-question-bank/chapters/${file}`, 390, file === '014.html');
    }
    for (const source of ['notes/math-interview-question-bank/chapters/001.html', 'notes/math-interview-question-bank/chapters/021.html',
      'notes/llm-interview-question-bank/chapters/020.html', 'notes/llm-interview-question-bank/chapters/091.html']) await inspect(source, 390);
    for (const source of ['notes/leetcode-hot-100/index.html', 'notes/quant-foundations/index.html',
      'notes/quant-foundations/math-prerequisites.html', 'notes/quant-foundations/probability-statistics.html', 'notes/quant-foundations/machine-learning.html', 'notes/quant-foundations/deep-learning.html', 'notes/interview-offline/index.html',
      'notes/tech-analysis/xiaohongshu-quant-interview-question-bank.html', 'notes/tech-analysis/xiaohongshu-quant-interview-practice-expansion.html']) {
      try { await fs.access(path.join(root, source)); } catch { continue; }
      for (const width of [320, 390, 768, 1440]) await inspect(source, width, width === 390);
    }
    console.log(JSON.stringify({ layoutChecks: checked, result: 'passed' }));
  } finally { await browser.close(); }
})().catch(err => { console.error(err); process.exitCode = 1; });
