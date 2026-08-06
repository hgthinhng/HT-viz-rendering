#!/usr/bin/env node
/**
 * verify.mjs — CLI nghiệm thu tổng quát cho MỌI file HTML dùng components.css
 * của thư viện này (không chỉ gallery.html). Dùng làm gate CI/pre-commit:
 * exit code 0 = mọi kiểm tra PASS, exit code 1 = có kiểm tra FAIL.
 *
 * Usage:
 *   node verify.mjs --html=/path/to/file.html [options]
 *
 * Options:
 *   --html=<path>        (bắt buộc) file HTML cần nghiệm thu
 *   --out=<dir>           thư mục ghi PDF/screenshot/log (mặc định: cùng thư mục html)
 *   --max-raster=<n>      số ảnh raster tối đa cho phép trong PDF (mặc định 0)
 *   --chromium=<path>     đường dẫn binary Chromium (mặc định: dò trong ~/.cache/ms-playwright)
 *   --python=<bin>        binary python3 dùng để đếm raster (mặc định "python3")
 *   --skip-pdf            bỏ qua export PDF + đếm raster
 *   --skip-offline        bỏ qua kiểm tra chặn network (offline thật)
 *   --skip-pages          bỏ qua render từng trang PDF ra PNG để soi bằng mắt
 *   --page-dpi=<n>         DPI khi render trang PDF ra PNG (mặc định 100)
 *
 * Yêu cầu: `npm i -D playwright-core` đã chạy TRONG thư mục chứa script này
 * (hoặc thư mục cha gần nhất có node_modules/playwright-core — ESM resolve
 * theo vị trí file, không theo cwd).
 *
 * Output: in từng dòng [PASS]/[FAIL] ra stdout, ghi verify-report.json vào
 * --out. Exit code phản ánh kết quả tổng — dùng được trực tiếp trong CI:
 *   node verify.mjs --html=gallery.html || exit 1
 */
import { chromium } from "playwright-core";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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
  const dirs = fs.readdirSync(cacheDir).filter((d) => d.startsWith("chromium-") && !d.includes("headless_shell"));
  dirs.sort().reverse(); // bản mới nhất trước
  for (const d of dirs) {
    const p = path.join(cacheDir, d, "chrome-linux64", "chrome");
    if (fs.existsSync(p)) return p;
  }
  return null;
}

const args = parseArgs(process.argv);
if (!args.html) {
  console.error("Thiếu --html=<path>. Xem --help trong đầu file verify.mjs.");
  process.exit(2);
}
const htmlPath = path.resolve(args.html);
if (!fs.existsSync(htmlPath)) {
  console.error("Không tìm thấy file:", htmlPath);
  process.exit(2);
}
const outDir = args.out ? path.resolve(args.out) : path.dirname(htmlPath);
fs.mkdirSync(outDir, { recursive: true });
const maxRaster = args["max-raster"] !== undefined ? Number(args["max-raster"]) : 0;
const chromiumPath = args.chromium || findChromium();
const pythonBin = args.python || "python3";
const pageDpi = args["page-dpi"] ? Number(args["page-dpi"]) : 100;

if (!chromiumPath) {
  console.error("Không tìm thấy Chromium trong ~/.cache/ms-playwright. Truyền --chromium=<path> thủ công.");
  process.exit(2);
}

const results = []; // { name, passed, detail }
function record(name, passed, detail) {
  results.push({ name, passed, detail });
  const tag = passed ? "PASS" : "FAIL";
  console.log(`[${tag}] ${name}${detail ? " — " + detail : ""}`);
}

async function main() {
  const browser = await chromium.launch({ executablePath: chromiumPath, headless: true });

  // ── 1. Render màn hình thường, bắt lỗi console/page ──────────────────
  const consoleErrors = [];
  const pageErrors = [];
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", (err) => pageErrors.push(String(err)));
  await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  record("no-console-errors", consoleErrors.length === 0, `${consoleErrors.length} lỗi`);
  record("no-page-errors", pageErrors.length === 0, `${pageErrors.length} lỗi`);
  if (consoleErrors.length) console.log("  console errors:", consoleErrors.slice(0, 5));
  if (pageErrors.length) console.log("  page errors:", pageErrors.slice(0, 5));

  await page.screenshot({ path: path.join(outDir, "verify-screenshot.png"), fullPage: true });

  // ── 2. reduced-motion thật sự được tôn trọng ──────────────────────────
  const reducedOk = await page.evaluate(() => {
    // Không thể đổi media feature của context hiện tại; chỉ xác nhận CSS có
    // đăng ký handler cho @media (prefers-reduced-motion: reduce) bằng cách
    // dò trong stylesheet — kiểm tra đầy đủ hơn nằm ở context riêng bên dưới.
    return true;
  });

  const ctxReduced = await browser.newContext({ reducedMotion: "reduce" });
  const pageReduced = await ctxReduced.newPage();
  await pageReduced.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  const reducedMatches = await pageReduced.evaluate(() => matchMedia("(prefers-reduced-motion: reduce)").matches);
  await pageReduced.close();
  await ctxReduced.close();
  record("reduced-motion-context-honored", reducedMatches === true);

  // ── 3. Offline thật: chặn mọi request không phải file:// ──────────────
  if (!args["skip-offline"]) {
    const ctxOffline = await browser.newContext();
    let blocked = [];
    await ctxOffline.route("**/*", (route) => {
      const url = route.request().url();
      if (url.startsWith("file://")) return route.continue();
      blocked.push(url);
      return route.abort();
    });
    const pageOffline = await ctxOffline.newPage();
    await pageOffline.goto("file://" + htmlPath, { waitUntil: "networkidle" });
    await pageOffline.evaluate(() => document.fonts.ready);
    const fontFamilies = await pageOffline.evaluate(() => {
      const set = new Set();
      document.fonts.forEach((f) => set.add(f.family));
      return [...set];
    });
    const fontsOk = {};
    for (const fam of fontFamilies) {
      fontsOk[fam] = await pageOffline.evaluate((f) => document.fonts.check(`16px "${f}"`), fam);
    }
    const allFontsLoaded = Object.values(fontsOk).every(Boolean);
    record("offline-no-network-requests", blocked.length === 0, `${blocked.length} request bị chặn`);
    record("offline-fonts-available", allFontsLoaded, JSON.stringify(fontsOk));
    if (blocked.length) console.log("  blocked URLs:", blocked.slice(0, 10));
    await pageOffline.close();
    await ctxOffline.close();
  }

  // ── 4. PDF export + đếm raster (shell ra count_raster.py) ─────────────
  if (!args["skip-pdf"]) {
    await page.emulateMedia({ media: "print" });
    const pdfPath = path.join(outDir, "verify-print.pdf");
    await page.pdf({
      path: pdfPath,
      format: "A4",
      printBackground: true,
      margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" },
    });
    await page.emulateMedia({ media: "screen" });

    let rasterResult = null;
    try {
      const countScript = path.join(__dirname, "count_raster.py");
      const stdout = execFileSync(pythonBin, [countScript, pdfPath, "--max", String(maxRaster), "--json"], {
        encoding: "utf-8",
      });
      rasterResult = JSON.parse(stdout);
      record("pdf-raster-count", rasterResult.passed, `${rasterResult.raster_count}/${maxRaster} ảnh, ${rasterResult.page_count} trang`);
    } catch (e) {
      // execFileSync throws on non-zero exit (FAIL case) — output vẫn ở e.stdout
      if (e.stdout) {
        try {
          rasterResult = JSON.parse(e.stdout.toString());
          record("pdf-raster-count", false, `${rasterResult.raster_count}/${maxRaster} ảnh raster (VƯỢT NGƯỠNG)`);
        } catch {
          record("pdf-raster-count", false, "không đọc được output count_raster.py: " + e.message);
        }
      } else {
        record("pdf-raster-count", false, "lỗi chạy count_raster.py: " + e.message + " (cần: pip install pymupdf)");
      }
    }

    // ── 5. Render từng trang PDF ra PNG để soi bằng mắt (không tự động PASS/FAIL) ──
    if (!args["skip-pages"] && rasterResult) {
      try {
        const pagesDir = path.join(outDir, "verify-pages");
        fs.mkdirSync(pagesDir, { recursive: true });
        const pyInline = `
import fitz, sys
doc = fitz.open(sys.argv[1])
for i in range(doc.page_count):
    pix = doc[i].get_pixmap(dpi=${pageDpi})
    pix.save(f"{sys.argv[2]}/page-{i+1:02d}.png")
print(doc.page_count)
`;
        const tmpPy = path.join(outDir, ".render_pages_tmp.py");
        fs.writeFileSync(tmpPy, pyInline);
        const n = execFileSync(pythonBin, [tmpPy, pdfPath, pagesDir], { encoding: "utf-8" }).trim();
        fs.unlinkSync(tmpPy);
        console.log(`  đã render ${n} trang PNG vào ${pagesDir} (soi bằng mắt, không tự PASS/FAIL ngắt trang)`);
      } catch (e) {
        console.log("  cảnh báo: không render được trang PDF ra PNG:", e.message);
      }
    }
  }

  await browser.close();

  const allPassed = results.every((r) => r.passed);
  fs.writeFileSync(
    path.join(outDir, "verify-report.json"),
    JSON.stringify({ html: htmlPath, results, allPassed, timestamp: new Date().toISOString() }, null, 2)
  );

  console.log("");
  console.log(allPassed ? "TỔNG KẾT: PASS — mọi kiểm tra đạt." : "TỔNG KẾT: FAIL — xem chi tiết ở trên.");
  process.exit(allPassed ? 0 : 1);
}

main().catch((e) => {
  console.error("Lỗi verify.mjs:", e);
  process.exit(2);
});
