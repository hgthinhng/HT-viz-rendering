// probe-svg-fonttype.mjs — mo 2 SVG (fonttype=path vs none) trong CHROMIUM THAT
// (khong phai matplotlib tu render lai) de xem may-khach (khong co Lato/NotoSansMono/
// DejaVuSansMono) co "tu sua" duoc tofu bug hay khong, khi trinh duyet phai tu chon
// font thay the cho font-family khai bao trong SVG.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';

const DIR = '/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/exp-matplotlib-svg';

const browser = await chromium.launch({
  executablePath: '/home/hgthinhng/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });

for (const name of ['exec_dashboard_path', 'exec_dashboard_none']) {
  const svgPath = path.join(DIR, `${name}.svg`);
  const svg = fs.readFileSync(svgPath, 'utf8');
  await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await page.waitForTimeout(200);
  const shot = path.join(DIR, `browser-render-${name}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  console.log('rendered', shot);

  // doc lai text content thuc su cua node <text> chua "chiet khau" qua DOM (khong qua regex)
  const textCheck = await page.evaluate(() => {
    const nodes = [...document.querySelectorAll('text')];
    const hit = nodes.find((n) => n.textContent.includes('chi') && n.textContent.toLowerCase().includes('u'));
    return nodes.map((n) => n.textContent).filter((t) => /chiết|Số liệu|Nguồn/.test(t));
  });
  console.log(name, '-> DOM text content:', JSON.stringify(textCheck));
}

await browser.close();
