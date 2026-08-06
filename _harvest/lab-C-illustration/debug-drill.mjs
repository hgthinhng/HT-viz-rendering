import { chromium } from "playwright-core";
import path from "node:path";

const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = path.resolve(new URL(".", import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage({ viewport: { width: 1200, height: 950 } });
await page.goto("file://" + path.join(DIR, "demo", "ship-annotated-demo.html"), { waitUntil: "networkidle" });

// click the first callout group (18-25% OPEX) and check the drill card populates
await page.evaluate(() => {
  const g = document.querySelectorAll("#ship-svg g.annotations .callout")[0];
  const evt = new MouseEvent("click", { clientX: 300, clientY: 200, bubbles: true });
  g.dispatchEvent(evt);
});
await page.waitForTimeout(150);
const drillText = await page.evaluate(() => {
  const card = document.getElementById("annotate-drill-card");
  return card ? { hidden: card.hidden, text: card.textContent } : null;
});
console.log("drill after click 1:", JSON.stringify(drillText));

// click outside -> should hide
await page.mouse.click(1100, 900);
await page.waitForTimeout(150);
const hiddenAfterOutside = await page.evaluate(() => document.getElementById("annotate-drill-card").hidden);
console.log("hidden after outside click:", hiddenAfterOutside);

await page.screenshot({ path: path.join(DIR, "png", "drill-test.png") });
await browser.close();
