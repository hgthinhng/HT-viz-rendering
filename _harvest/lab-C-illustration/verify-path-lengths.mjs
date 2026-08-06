// verify-path-lengths.mjs — đo thật tỷ lệ (độ dài route / khoảng cách
// thẳng) của từng leader-line trong ship-annotated-demo.html, in ra bảng
// để đối chiếu với ràng buộc "không vượt 1.6x" — không chỉ tin vào chứng
// minh toán học (Manhattan <= sqrt(2) x thẳng), đo bằng số thật lấy trực
// tiếp từ DOM đã render.
import { chromium } from "playwright-core";
import path from "node:path";

const CHROME_PATH = "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const DIR = path.resolve(new URL(".", import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto("file://" + path.join(DIR, "demo", "ship-annotated-demo.html"), { waitUntil: "networkidle" });

const rows = await page.evaluate(() => {
  return [...document.querySelectorAll("#ship-svg g.annotations .callout")].map((g) => {
    const head = g.querySelector("text").textContent;
    const pathEl = g.querySelector("path");
    const total = pathEl.getTotalLength();
    const anchorCircle = g.querySelector("circle");
    const ax = +anchorCircle.getAttribute("cx"), ay = +anchorCircle.getAttribute("cy");
    // điểm cuối path = điểm bám vào nhãn
    const end = pathEl.getPointAtLength(total);
    const straight = Math.hypot(end.x - ax, end.y - ay);
    return { head, routeLen: total, straight, ratio: total / straight };
  });
});

console.log("Head".padEnd(22), "Route".padStart(8), "Straight".padStart(10), "Ratio".padStart(8));
for (const r of rows) {
  console.log(r.head.padEnd(22), r.routeLen.toFixed(1).padStart(8), r.straight.toFixed(1).padStart(10), (r.ratio.toFixed(3) + "x").padStart(8));
}
const maxRatio = Math.max(...rows.map((r) => r.ratio));
console.log("\nRatio lớn nhất:", maxRatio.toFixed(3) + "x", "— ngưỡng cho phép: 1.6x —", maxRatio <= 1.6 ? "ĐẠT" : "VI PHẠM");

await browser.close();
