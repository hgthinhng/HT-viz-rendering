const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.resolve('slide-test-nosvg.html'));
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.screenshot({ path: 'render-check.png' });
  await browser.close();
})();
