// render.mjs — render mọi file trong svg/*.svg (và demo/*.html) ra PNG để
// tự kiểm bằng mắt (Read tool đọc ảnh). Dùng Chromium cache sẵn có trong
// máy (playwright-core, không cần download lại — xem memory
// reference_playwright_core_cached_chromium_wsl).
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";

const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = path.resolve(new URL(".", import.meta.url).pathname);

const svgFiles = fs.readdirSync(path.join(DIR, "svg")).filter((f) => f.endsWith(".svg"));
const htmlFiles = fs.readdirSync(path.join(DIR, "demo")).filter((f) => f.endsWith(".html"));

const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });

async function renderSvgFile(svgName) {
  const svgPath = path.join(DIR, "svg", svgName);
  const svgContent = fs.readFileSync(svgPath, "utf8");
  const page = await browser.newPage({ viewport: { width: 1000, height: 800 } });
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face { font-family:'Be Vietnam Pro'; src:url('file:///home/hgthinhng/.fonts/BeVietnamPro-Regular.ttf'); font-weight:400; }
    @font-face { font-family:'Be Vietnam Pro'; src:url('file:///home/hgthinhng/.fonts/BeVietnamPro-SemiBold.ttf'); font-weight:600; }
    @font-face { font-family:'Be Vietnam Pro'; src:url('file:///home/hgthinhng/.fonts/BeVietnamPro-Bold.ttf'); font-weight:700; }
    *{margin:0;padding:0;box-sizing:border-box;}
    html,body{background:#ffffff;}
    body{width:900px;padding:24px;font-family:'Be Vietnam Pro',sans-serif;}
    svg{width:100%;height:auto;display:block;border:1px solid #e2e8f0;}
  </style></head><body>${svgContent}</body></html>`;
  await page.setContent(html, { waitUntil: "networkidle" });
  const outName = svgName.replace(/\.svg$/, ".png");
  await page.locator("body").screenshot({ path: path.join(DIR, "png", outName) });
  await page.close();
  console.log("rendered", outName);
}

async function renderHtmlFile(htmlName) {
  const htmlPath = path.join(DIR, "demo", htmlName);
  const page = await browser.newPage({ viewport: { width: 1000, height: 900 } });
  await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  const outName = htmlName.replace(/\.html$/, ".png");
  await page.screenshot({ path: path.join(DIR, "png", outName), fullPage: true });
  await page.close();
  console.log("rendered", outName);
}

for (const f of svgFiles) await renderSvgFile(f);
for (const f of htmlFiles) await renderHtmlFile(f);

await browser.close();
console.log("done:", svgFiles.length, "svg +", htmlFiles.length, "html");
