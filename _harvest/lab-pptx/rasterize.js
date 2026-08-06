// Screenshot just the <svg id="chart"> element to a standalone PNG,
// to test the documented workaround (rasterize SVG -> <img>).
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve('svg-source.html'));
  const el = await page.$('#chart');
  await el.screenshot({ path: 'chart-rasterized.png' });
  await browser.close();
  console.log('done');
})();
