// probe-echarts-font.mjs — kiem tra CHEO: SVG cua chinh ECharts (nhom A) co bi
// cung 1 loai bug font-fallback nhu matplotlib khong, khi mo trong Chromium THAT
// (font "Calibri","Segoe UI" khong ton tai tren Linux sandbox nay -> browser phai
// tu roi xuong fallback, giong y het tinh huong _eir_style.py gap).
import { chromium } from 'playwright-core';
import fs from 'node:fs';

const svgPath = '/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/out-01-waterfall.svg';
const svg = fs.readFileSync(svgPath, 'utf8');

const browser = await chromium.launch({
  executablePath: '/home/hgthinhng/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 800, height: 500 } });
await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
await page.waitForTimeout(150);
await page.screenshot({ path: '/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-A-charts/exp-matplotlib-svg/browser-render-echarts-waterfall.png' });
const texts = await page.evaluate(() => [...document.querySelectorAll('text')].map((n) => n.textContent));
console.log('DOM text nodes:', JSON.stringify(texts));
await browser.close();
