#!/usr/bin/env node
/**
 * measure-density.mjs — công cụ ĐO (không phải gate PASS/FAIL) mật độ ký tự
 * tiếng Việt và độ an toàn dấu chồng cho MỘT font/cỡ chữ/line-height bất kỳ.
 * Dùng khi đổi font hoặc đổi thang chữ, để có số thật thay vì đoán.
 *
 * Usage:
 *   node measure-density.mjs --html=<path> [--font="Spectral"] [--size=17]
 *     [--line-height=1.7] [--weight=400] [--max-width=65ch]
 *
 * File --html PHẢI đã load đúng font cần đo (qua fonts-embedded.css hoặc CDN)
 * — script tự mở file đó bằng Chromium rồi đo trong context của nó, không
 * đo trên trang trống (trang trống làm font không được trigger tải, xem
 * README mục "bẫy canvas font chưa tải").
 *
 * In ra: ký tự/dòng thật (Range API), và ink-height thật (Canvas
 * measureText.actualBoundingBoxAscent/Descent) so với line-box khai báo —
 * KHÔNG dùng getBoundingClientRect().height để kết luận "an toàn dấu chồng",
 * số đó luôn khớp line-height theo định nghĩa CSS bất kể chữ có bị cắt hay
 * không (bẫy phương pháp luận đã tự bắt được, xem README).
 */
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";
import { fileURLToPath } from "node:url";

function parseArgs(argv) {
  const out = {};
  for (const a of argv.slice(2)) {
    const m = a.match(/^--([^=]+)(?:=(.*))?$/);
    if (m) out[m[1]] = m[2] === undefined ? true : m[2];
  }
  return out;
}
function findChromium() {
  const cacheDir = path.join(os.homedir(), ".cache", "ms-playwright");
  if (!fs.existsSync(cacheDir)) return null;
  const dirs = fs.readdirSync(cacheDir).filter((d) => d.startsWith("chromium-") && !d.includes("headless_shell")).sort().reverse();
  for (const d of dirs) {
    const p = path.join(cacheDir, d, "chrome-linux64", "chrome");
    if (fs.existsSync(p)) return p;
  }
  return null;
}

const args = parseArgs(process.argv);
if (!args.html) {
  console.error('Thiếu --html=<path>. Ví dụ: node measure-density.mjs --html=../gallery.html --font=Spectral --size=17 --line-height=1.7');
  process.exit(2);
}
const htmlPath = path.resolve(args.html);
const font = args.font || "Spectral";
const size = Number(args.size || 17);
const lineHeight = Number(args["line-height"] || 1.7);
const weight = Number(args.weight || 400);
const maxWidth = args["max-width"] || "65ch";
const chromiumPath = args.chromium || findChromium();

const WORST_DIACRITIC = "ường ệ ẫ ữ ỗ ộ ẫu tưởng nghiêng ưỡng Ộ Ễ Ữ";
const SAMPLES = [
  "Doanh thu tang truong on dinh trong ba quy lien tiep nho toi uu tuyen khai thac chinh.",
  "Doanh thu tăng trưởng ổn định trong ba quý liên tiếp nhờ tối ưu tuyến khai thác chính.",
  "Đội tàu vẫn chịu áp lực nhượng bộ ngưỡng nợ vay, được ưởng ứng ước lượng ổn thỏa hơn dự kiến ban đầu.",
];

async function main() {
  if (!chromiumPath) { console.error("Không tìm thấy Chromium, truyền --chromium=<path>."); process.exit(2); }
  const browser = await chromium.launch({ executablePath: chromiumPath, headless: true });
  const page = await browser.newPage();
  await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);

  const result = await page.evaluate(({ font, size, lineHeight, weight, maxWidth, samples, worst }) => {
    function charsPerLine(text, ff, sz, lh, mw) {
      const div = document.createElement("div");
      div.style.cssText = `position:absolute;left:-9999px;top:0;visibility:hidden;max-width:${mw};font-family:'${ff}',Georgia,serif;font-size:${sz}px;line-height:${lh};white-space:normal;overflow-wrap:break-word;`;
      div.textContent = text;
      document.body.appendChild(div);
      const range = document.createRange();
      const node = div.firstChild;
      let firstLineBreak = text.length, lastTop = null;
      for (let i = 0; i < text.length; i++) {
        range.setStart(node, i); range.setEnd(node, i + 1);
        const rect = range.getBoundingClientRect();
        if (lastTop === null) lastTop = rect.top;
        else if (rect.top > lastTop + 1) { firstLineBreak = i; break; }
      }
      const widthPx = div.getBoundingClientRect().width;
      document.body.removeChild(div);
      return { firstLineBreak, textLength: text.length, widthPx };
    }
    function inkMetrics(text, ff, sz, wt) {
      const c = document.createElement("canvas");
      const ctx = c.getContext("2d");
      ctx.font = `${wt} ${sz}px ${ff}`;
      const m = ctx.measureText(text);
      return {
        ascent: +m.actualBoundingBoxAscent.toFixed(2),
        descent: +m.actualBoundingBoxDescent.toFixed(2),
        inkHeight: +(m.actualBoundingBoxAscent + m.actualBoundingBoxDescent).toFixed(2),
      };
    }
    const perSample = samples.map((s) => charsPerLine(s, font, size, lineHeight, maxWidth));
    const ink = inkMetrics(worst, font, size, weight);
    const lineBox = size * lineHeight;
    return { perSample, ink, lineBox, marginPx: +(lineBox - ink.inkHeight).toFixed(2) };
  }, { font, size, lineHeight, weight, maxWidth, samples: SAMPLES, worst: WORST_DIACRITIC });

  await browser.close();

  console.log(`Font: ${font} @ ${size}px, weight ${weight}, line-height ${lineHeight}, max-width ${maxWidth}`);
  console.log("Ký tự/dòng đo được (Range API, 3 mẫu tiếng Việt):");
  result.perSample.forEach((s, i) => console.log(`  mẫu ${i + 1}: ${s.firstLineBreak} ký tự/dòng đầu (tổng ${s.textLength} ký tự, khổ ${s.widthPx.toFixed(0)}px)`));
  console.log(`Ink-height dấu chồng nặng nhất (Canvas measureText): ${result.ink.inkHeight}px`);
  console.log(`Line-box khai báo: ${result.lineBox}px → dư ${result.marginPx}px ${result.marginPx >= 0 ? "(AN TOÀN)" : "(RỦI RO CẮT DẤU)"}`);

  fs.writeFileSync(
    path.join(path.dirname(htmlPath), "density-measurement.json"),
    JSON.stringify({ font, size, lineHeight, weight, maxWidth, ...result }, null, 2)
  );
}

main().catch((e) => { console.error(e); process.exit(2); });
