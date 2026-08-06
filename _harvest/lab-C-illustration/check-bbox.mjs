import { chromium } from "playwright-core";
import path from "node:path";

const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-C-illustration";
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto("file://" + path.join(DIR, "demo", "ship-annotated-demo.html"), { waitUntil: "networkidle" });

const result = await page.evaluate(() => {
  const svg = document.getElementById("ship-svg");
  const vb = svg.viewBox.baseVal;
  const boxes = [...document.querySelectorAll("#ship-svg g.annotations .callout")].map((g) => {
    const rect = g.querySelector("rect"); // hộp nhãn = rect đầu tiên trong g (không phải accent bar)
    const head = g.querySelector("text").textContent;
    const x = +rect.getAttribute("x"), y = +rect.getAttribute("y");
    const w = +rect.getAttribute("width"), h = +rect.getAttribute("height");
    return { head, x, y, w, h, right: x + w, bottom: y + h,
      overflowLeft: x < 0, overflowRight: x + w > vb.width,
      overflowTop: y < 0, overflowBottom: y + h > vb.height };
  });
  return { viewBox: { width: vb.width, height: vb.height }, boxes };
});
console.log("viewBox:", JSON.stringify(result.viewBox));
for (const b of result.boxes) {
  const bad = b.overflowLeft || b.overflowRight || b.overflowTop || b.overflowBottom;
  console.log((bad ? "TRÀN  " : "OK    ") + b.head.padEnd(22), `x=${b.x.toFixed(1)} y=${b.y.toFixed(1)} right=${b.right.toFixed(1)} bottom=${b.bottom.toFixed(1)}`);
}
await browser.close();
