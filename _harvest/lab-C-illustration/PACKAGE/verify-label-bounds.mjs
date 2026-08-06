// verify-label-bounds.mjs — đo THẬT bounding box của từng hộp nhãn callout
// so với viewBox của SVG, phát hiện tràn khung. KHÔNG có trong yêu cầu gốc
// nhưng thêm vào vì cùng triết lý với verify-path-lengths.mjs: đo bằng số
// thật lấy từ DOM đã render, không chỉ nhìn ảnh — chính cách đo này (so
// x/y/width/height của <rect> với viewBox.baseVal) là cách đã bắt được lỗi
// tràn khung thật trong ship-annotated-demo (hộp "THUỶ THỦ ĐOÀN" từng có
// bottom=516.5 trên viewBox cao 520 — chỉ còn 3.5px, bị cắt bởi
// overflow:hidden mặc định của SVG root, nhìn như tràn khung dù về số học
// chưa âm).
//
// CHẠY:
//   node verify-label-bounds.mjs <file.html> [id-svg=first] [margin=8]
// Thoát code 1 nếu có hộp nào tràn khung HOẶC vi phạm margin an toàn.
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";

const CHROME_PATH = process.env.CHROME_PATH || "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome";

const htmlArg = process.argv[2];
const svgIdArg = process.argv[3];
const margin = process.argv[4] ? Number(process.argv[4]) : 8;
if (!htmlArg) {
  console.error("Cách dùng: node verify-label-bounds.mjs <file.html> [id-svg] [margin=8]");
  process.exit(2);
}
const htmlPath = path.resolve(htmlArg);
if (!fs.existsSync(htmlPath)) { console.error("Không tìm thấy file:", htmlPath); process.exit(2); }
if (!fs.existsSync(CHROME_PATH)) { console.error("Không tìm thấy Chromium tại:", CHROME_PATH); process.exit(2); }

const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true });
const page = await browser.newPage();
await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });

const result = await page.evaluate((svgId) => {
  const svg = svgId ? document.getElementById(svgId) : document.querySelector("svg");
  const vb = svg.viewBox.baseVal;
  const boxes = [...svg.querySelectorAll("g.annotations .callout")].map((g) => {
    const rect = g.querySelector("rect"); // hộp nhãn = rect đầu tiên trong g
    const head = g.querySelector("text")?.textContent || "(không có head)";
    const x = +rect.getAttribute("x"), y = +rect.getAttribute("y");
    const w = +rect.getAttribute("width"), h = +rect.getAttribute("height");
    return { head, x, y, right: x + w, bottom: y + h };
  });
  return { viewBox: { width: vb.width, height: vb.height }, boxes };
}, svgIdArg);

if (result.boxes.length === 0) {
  console.error("Không tìm thấy callout nào — đã gọi Annotate.annotate() chưa? svg id đúng chưa?");
  await browser.close();
  process.exit(2);
}

console.log("viewBox:", JSON.stringify(result.viewBox), `(margin an toàn = ${margin}px)`);
let anyBad = false;
for (const b of result.boxes) {
  const bad = b.x < margin || b.y < margin || b.right > result.viewBox.width - margin || b.bottom > result.viewBox.height - margin;
  if (bad) anyBad = true;
  console.log((bad ? "TRÀN  " : "OK    ") + b.head.padEnd(24), `x=${b.x.toFixed(1)} y=${b.y.toFixed(1)} right=${b.right.toFixed(1)} bottom=${b.bottom.toFixed(1)}`);
}
console.log("\nKết quả:", anyBad ? "CÓ HỘP TRÀN/CHẠM LỀ AN TOÀN" : "TẤT CẢ HỘP NẰM TRỌN TRONG VIEWBOX");

await browser.close();
process.exit(anyBad ? 1 : 0);
