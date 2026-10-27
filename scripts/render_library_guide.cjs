#!/usr/bin/env node
// No user browser session is accessed.
const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(path.resolve(process.argv[2])).href);
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: process.argv[3], format: 'A4', printBackground: true,
      preferCSSPageSize: true, tagged: true, outline: true });
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
