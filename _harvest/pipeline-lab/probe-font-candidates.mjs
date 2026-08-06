// probe-font-candidates.mjs — tim font THAT SU CO SAN tren may nay co the thay the
// DejaVu Sans Mono de fix tofu bug, bang cach render THAT trong Chromium va chup anh.
import { chromium } from 'playwright-core';

const candidates = ['DejaVu Sans Mono', 'Liberation Mono', 'DejaVu Sans', 'Noto Sans', 'Be Vietnam Pro', 'JetBrains Mono', 'Ubuntu Mono'];
const testStrings = ['Số liệu tại 06/2026', 'chiết khấu 14%', 'ếấốồặữ'];

const html = `<html><body style="background:#FFFEF8;padding:20px">
${candidates.map((f) => `
  <div style="font-family:'${f}',monospace; font-size:22px; margin-bottom:10px; color:#1F1F1F;">
    <b>${f}:</b> ${testStrings.join('  |  ')}
  </div>`).join('')}
</body></html>`;

const browser = await chromium.launch({
  executablePath: '/home/hgthinhng/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 1500, height: 500 } });
await page.setContent(html);
await page.waitForTimeout(150);
await page.screenshot({ path: '/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/exp-matplotlib-svg/font-candidates.png' });
console.log('done');
await browser.close();
