import { chromium } from "playwright-core";
import path from "node:path";
const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = path.resolve(new URL(".", import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto("file://" + path.join(DIR, "demo", "banner-topbottom-demo.html"), { waitUntil: "networkidle" });
const result = await page.evaluate(() => {
  const svg = document.getElementById("banner-svg");
  const vb = svg.viewBox.baseVal;
  const boxes = [...document.querySelectorAll("#banner-svg g.annotations .callout")].map((g) => {
    const rect = g.querySelector("rect");
    const head = g.querySelector("text").textContent;
    const x = +rect.getAttribute("x"), y = +rect.getAttribute("y");
    const w = +rect.getAttribute("width"), h = +rect.getAttribute("height");
    return { head, x, y, right: x + w, bottom: y + h };
  });
  return { viewBox: { width: vb.width, height: vb.height }, boxes };
});
console.log("viewBox:", JSON.stringify(result.viewBox));
for (const b of result.boxes) {
  const bad = b.x < 0 || b.y < 0 || b.right > result.viewBox.width || b.bottom > result.viewBox.height;
  console.log((bad ? "TRÀN  " : "OK    ") + b.head.padEnd(14), `x=${b.x.toFixed(1)} y=${b.y.toFixed(1)} right=${b.right.toFixed(1)} bottom=${b.bottom.toFixed(1)}`);
}
await browser.close();
