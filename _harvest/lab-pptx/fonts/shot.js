const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 } });
  await page.goto('file://' + path.resolve('glyph-render-check.html'));
  await page.waitForTimeout(500); // let @font-face load
  await page.screenshot({ path: 'glyph-render-check.png', fullPage: true });
  await browser.close();
})();
