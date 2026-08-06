import { chromium } from 'playwright-core';
import path from 'node:path';

const CHROME_PATH = '/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome';
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });

for (const i of [1,2,3,4,5]) {
  const page = await browser.newPage();
  const htmlPath = path.resolve(`./cases/case${i}.html`);
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.resolve(`./cases/case${i}.pdf`),
    width: '1093px', height: '400px',
    printBackground: true,
    margin: { top: '0px', bottom: '0px', left: '0px', right: '0px' },
  });
  await page.close();
}
await browser.close();
console.log('done');
