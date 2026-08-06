import { chromium } from "playwright-core";
import path from "node:path";

const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = path.resolve(new URL(".", import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
page.on("console", (msg) => console.log("CONSOLE:", msg.type(), msg.text()));
page.on("pageerror", (err) => console.log("PAGEERROR:", err.message));
await page.goto("file://" + path.join(DIR, "demo", "ship-annotated-demo.html"), { waitUntil: "networkidle" });
await page.waitForTimeout(300);
const info = await page.evaluate(() => {
  return [...document.querySelectorAll("#ship-svg g.annotations .callout")].map((g) => {
    const head = g.querySelector("text")?.textContent;
    const path = g.querySelector("path");
    const circle = g.querySelector("circle");
    return { head, d: path?.getAttribute("d"), anchor: [circle?.getAttribute("cx"), circle?.getAttribute("cy")] };
  });
});
console.log(JSON.stringify(info, null, 2));
await browser.close();
