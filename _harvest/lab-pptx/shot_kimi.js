const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
  await page.goto('file://' + '/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/reference-kimi.html');
  await page.waitForTimeout(700);
  await page.screenshot({ path: 'kimi-render-check.png' });
  await browser.close();
})();
