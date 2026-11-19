const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require('playwright');

const site = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3]);

async function main() {
  await fs.mkdir(output, { recursive: true });
  const server = http.createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      let filename = path.resolve(site, `.${pathname}`);
      if (filename !== site && !filename.startsWith(`${site}${path.sep}`)) {
        response.writeHead(403).end();
        return;
      }
      let metadata;
      try { metadata = await fs.stat(filename); } catch {
        filename += '.html';
        metadata = await fs.stat(filename);
      }
      if (metadata.isDirectory()) filename = path.join(filename, 'index.html');
      const actual = await fs.realpath(filename);
      assert.ok(actual.startsWith(`${site}${path.sep}`));
      const mime = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript',
        '.css': 'text/css', '.png': 'image/png', '.ico': 'image/x-icon', '.svg': 'image/svg+xml' };
      response.writeHead(200, { 'content-type': mime[path.extname(filename)] || 'application/octet-stream' });
      response.end(await fs.readFile(filename));
    } catch {
      response.writeHead(404).end();
    }
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  let browser;
  const results = [];
  try {
    browser = await chromium.launch({ headless: true });
    for (const width of [1440, 390, 320]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const localFailures = [];
      page.on('response', response => {
        if (response.url().startsWith('http://127.0.0.1:') && response.status() >= 400) {
          localFailures.push(response.url());
        }
      });
      await page.route('**/*', route => {
        if (route.request().url().startsWith('http://127.0.0.1:')) return route.continue();
        return route.fulfill({ status: 204, body: '' });
      });
      const origin = `http://127.0.0.1:${server.address().port}`;
      await page.goto(origin, { waitUntil: 'load' });
      await page.evaluate(async () => {
        await window.MathJax.startup.promise;
        await document.fonts.ready;
      });
      const initial = await page.evaluate(() => ({ jquery: window.jQuery.fn.jquery,
        width: innerWidth, documentWidth: document.documentElement.scrollWidth,
        links: [...document.querySelectorAll('#site-nav li a')].map(anchor => anchor.textContent),
        hidden: document.querySelectorAll('#site-nav .hidden-links li').length }));
      assert.equal(initial.jquery, '3.7.1');
      assert.ok(initial.documentWidth <= width + 1, JSON.stringify(initial));
      if (initial.hidden) {
        await page.locator('#site-nav button').click();
        assert.equal(await page.locator('#site-nav .hidden-links').isVisible(), true);
        await page.locator('#site-nav button').click();
      }
      await page.screenshot({ path: path.join(output, `homepage-${width}.png`) });
      const restored = await page.evaluate(() => {
        const nav = document.querySelector('#site-nav');
        nav.style.minWidth = '0';
        nav.style.width = '0';
        updateNav();
        const emptyWidth = document.querySelectorAll('#site-nav .visible-links li').length;
        updateNav();
        nav.style.width = '2000px';
        for (let iteration = 0; iteration < 10; iteration += 1) updateNav();
        const links = [...document.querySelectorAll('#site-nav .visible-links li a')].map(anchor => anchor.textContent);
        nav.style.removeProperty('width');
        nav.style.removeProperty('min-width');
        updateNav();
        return { emptyWidth, links };
      });
      assert.equal(restored.emptyWidth, 0);
      assert.deepEqual(restored.links, initial.links);
      await page.evaluate(async () => {
        const fixture = document.createElement('div');
        fixture.id = 'math-regression';
        fixture.textContent = 'Inline \\(x^2\\) and \\[\\frac{1}{2}\\] and \\begin{equation}a=b\\end{equation}';
        document.querySelector('.page__content').prepend(fixture);
        await window.MathJax.typesetPromise([fixture]);
      });
      const formula = await page.evaluate(() => ({
        containers: document.querySelectorAll('#math-regression mjx-container').length,
        errors: document.querySelectorAll('#math-regression [data-mjx-error], #math-regression mjx-merror').length,
        tags: window.MathJax.config.tex.tags
      }));
      assert.equal(formula.containers, 3);
      assert.equal(formula.errors, 0);
      assert.equal(formula.tags, 'all');
      await page.screenshot({ path: path.join(output, `formulas-${width}.png`) });
      await page.goto(`${origin}/publication/2023-12-19-paper-title-number-2`, { waitUntil: 'load' });
      assert.match(await page.locator('body').innerText(), /Exploring the Factual Consistency/);
      assert.equal(errors.length, 0, errors.join('\n'));
      assert.deepEqual(localFailures, []);
      results.push({ ...initial, formulas: formula, restoredOrder: true, browserErrors: errors, localFailures });
      await page.close();
    }
    await fs.writeFile(path.join(output, 'verification.json'), JSON.stringify({
      result: 'passed', externalResources: 'stubbed; not an external availability audit', results
    }, null, 2));
    console.log(JSON.stringify({ result: 'passed', scenarios: results.length, results }, null, 2));
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
