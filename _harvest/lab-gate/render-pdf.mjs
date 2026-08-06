// render-pdf.mjs — HTML -> PDF via cached Chromium (playwright-core), print-to-pdf path.
// Usage: node render-pdf.mjs <input.html> <output.pdf>
// Recipe: memory reference_playwright_core_cached_chromium_wsl.md
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";

const [, , inFile, outFile] = process.argv;
if (!inFile || !outFile) {
  console.error("usage: node render-pdf.mjs <input.html> <output.pdf>");
  process.exit(2);
}

const CHROME_CANDIDATES = fs.readdirSync(
  path.join(process.env.HOME, ".cache/ms-playwright")
)
  .filter(d => d.startsWith("chromium-"))
  .map(d => path.join(process.env.HOME, ".cache/ms-playwright", d, "chrome-linux64/chrome"))
  .filter(p => fs.existsSync(p));

if (CHROME_CANDIDATES.length === 0) {
  console.error("Khong tim thay chromium binary trong ~/.cache/ms-playwright");
  process.exit(1);
}
const executablePath = CHROME_CANDIDATES[CHROME_CANDIDATES.length - 1];

const absIn = path.resolve(inFile);
const browser = await chromium.launch({ executablePath, headless: true });
const page = await browser.newPage();
await page.goto("file://" + absIn, { waitUntil: "networkidle" });
// để mọi IntersectionObserver / reveal chạy xong (reference-kimi.html có reveal on-scroll)
await page.evaluate(() => {
  document.querySelectorAll(".band .spread > *, footer .spread > *").forEach(el => {
    el.style.opacity = "1";
    el.style.transform = "none";
  });
});
await page.waitForTimeout(300);
await page.pdf({
  path: path.resolve(outFile),
  printBackground: true,
  format: "A4",
  margin: { top: "0", bottom: "0", left: "0", right: "0" }
});
await browser.close();
console.log("OK ->", outFile);
