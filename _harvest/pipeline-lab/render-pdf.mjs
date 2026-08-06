import { chromium } from 'playwright-core';
import path from 'node:path';

const CHROME_PATH = '/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome';

const htmlPath = path.resolve('./test-page.html');
const outPath = path.resolve('./out-playwright.pdf');

const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
// ensure webfont loaded
await page.evaluate(() => document.fonts.ready);
await page.pdf({
  path: outPath,
  width: '1093px',
  height: '900px',
  printBackground: true,
  margin: { top: '0px', bottom: '0px', left: '0px', right: '0px' },
});
await browser.close();
console.log('Wrote', outPath);
