// verify-path-lengths.mjs — đo THẬT tỷ lệ (độ dài leader-line / khoảng
// cách thẳng neo->nhãn) trên 1 file HTML đã gọi Annotate.annotate(), đối
// chiếu với ràng buộc "không quá 1.6x khoảng cách thẳng". Không tin vào
// chứng minh toán học suông (Manhattan <= sqrt(2)x thẳng) — đo bằng
// path.getTotalLength() lấy trực tiếp từ DOM đã render qua Chromium thật.
//
// PHỤ THUỘC: npm install playwright-core (đã cài trong pipeline-lab của
// dự án gốc; nếu chạy nơi khác, cài lại + trỏ CHROME_PATH cho đúng máy).
//
// CHẠY:
//   node verify-path-lengths.mjs <đường-dẫn-file.html> [id-svg=first]
// Ví dụ:
//   node verify-path-lengths.mjs examples/example-vertical-axis-ship.html ship-svg
//   node verify-path-lengths.mjs examples/example-horizontal-axis-banner.html banner-svg
//
// Thoát code 1 nếu có bất kỳ leader nào vượt 1.6x (dùng được trong CI/gate).
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";

const CHROME_PATH = process.env.CHROME_PATH || "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";
const RATIO_LIMIT = 1.6;

const htmlArg = process.argv[2];
const svgIdArg = process.argv[3];
if (!htmlArg) {
  console.error("Cách dùng: node verify-path-lengths.mjs <file.html> [id-svg]");
  process.exit(2);
}
const htmlPath = path.resolve(htmlArg);
if (!fs.existsSync(htmlPath)) {
  console.error("Không tìm thấy file:", htmlPath);
  process.exit(2);
}
if (!fs.existsSync(CHROME_PATH)) {
  console.error("Không tìm thấy Chromium tại:", CHROME_PATH, "— đặt biến môi trường CHROME_PATH trỏ đúng chỗ (vd ~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome).");
  process.exit(2);
}

const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });

const rows = await page.evaluate((svgId) => {
  const svg = svgId ? document.getElementById(svgId) : document.querySelector("svg");
  return [...svg.querySelectorAll("g.annotations .callout")].map((g) => {
    const head = g.querySelector("text")?.textContent || "(không có head)";
    const pathEl = g.querySelector("path");
    const total = pathEl.getTotalLength();
    const anchorCircle = g.querySelector("circle");
    const ax = +anchorCircle.getAttribute("cx"), ay = +anchorCircle.getAttribute("cy");
    const end = pathEl.getPointAtLength(total);
    const straight = Math.hypot(end.x - ax, end.y - ay) || 1;
    return { head, routeLen: total, straight, ratio: total / straight };
  });
}, svgIdArg);

if (rows.length === 0) {
  console.error("Không tìm thấy callout nào (g.annotations .callout) — đã gọi Annotate.annotate() chưa? svg id đúng chưa?");
  await browser.close();
  process.exit(2);
}

console.log("Head".padEnd(24), "Route".padStart(8), "Straight".padStart(10), "Ratio".padStart(8));
let worst = 0;
for (const r of rows) {
  worst = Math.max(worst, r.ratio);
  console.log(r.head.padEnd(24), r.routeLen.toFixed(1).padStart(8), r.straight.toFixed(1).padStart(10), (r.ratio.toFixed(3) + "x").padStart(8));
}
console.log(`\nRatio lớn nhất: ${worst.toFixed(3)}x — ngưỡng cho phép: ${RATIO_LIMIT}x —`, worst <= RATIO_LIMIT ? "ĐẠT" : "VI PHẠM");

await browser.close();
process.exit(worst <= RATIO_LIMIT ? 0 : 1);
