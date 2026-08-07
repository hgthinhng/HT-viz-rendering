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
 *   --html=<path>        file HTML cần nghiệm thu (mặc định: components/gallery.html tính từ gốc repo)
 *   --out=<dir>           thư mục ghi PDF/screenshot/log (mặc định: cùng thư mục html)
 *   --max-raster=<n>      số ảnh raster tối đa cho phép trong PDF (mặc định 0)
 *   --chromium=<path>     đường dẫn binary Chromium (mặc định: bản playwright-core tự trỏ tới,
 *                         xem scripts/lib/chromium.mjs)
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
import path from "node:path";
import fs from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { kiemTraChromium, launchChromium } from "./lib/chromium.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEFAULT_HTML = path.join(ROOT, 'components', 'gallery.html');

function parseArgs(argv) {
  const out = {};
  for (const a of argv.slice(2)) {
    const m = a.match(/^--([^=]+)(?:=(.*))?$/);
    if (m) out[m[1]] = m[2] === undefined ? true : m[2];
  }
  return out;
}

const args = parseArgs(process.argv);
const htmlPath = path.resolve(args.html || DEFAULT_HTML);
if (!fs.existsSync(htmlPath)) {
  console.error("Không tìm thấy file:", htmlPath);
  process.exit(2);
}
const outDir = args.out ? path.resolve(args.out) : path.dirname(htmlPath);
fs.mkdirSync(outDir, { recursive: true });
const maxRaster = args["max-raster"] !== undefined ? Number(args["max-raster"]) : 0;
const pythonBin = args.python || "python3";
const pageDpi = args["page-dpi"] ? Number(args["page-dpi"]) : 100;

const kiemChromium = kiemTraChromium(args.chromium);
if (!kiemChromium.ok) {
  console.error(kiemChromium.message);
  process.exit(2);
}
const chromiumPath = kiemChromium.path;

const results = []; // { name, passed, detail }
function record(name, passed, detail) {
  results.push({ name, passed, detail });
  const tag = passed ? "PASS" : "FAIL";
  console.log(`[${tag}] ${name}${detail ? " - " + detail : ""}`);
}

async function main() {
  const browser = await launchChromium({ executablePath: chromiumPath });

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

  // ── 2. reduced-motion thật sự tắt chuyển động của TRANG NÀY ───────────
  //
  // Bản trước gate này xanh mà không kiểm gì của trang: nó chỉ hỏi
  // matchMedia("(prefers-reduced-motion: reduce)") trong một context đã khai
  // reducedMotion:"reduce", tức hỏi Playwright xem Playwright có làm đúng
  // việc của Playwright không. Câu trả lời luôn true kể cả khi CSS của trang
  // không có một dòng @media prefers-reduced-motion nào. Biến reducedOk phía
  // trên còn tệ hơn: một hàm `return true` chưa từng được đọc.
  //
  // Bản này đếm SỐ PHẦN TỬ THẬT còn chuyển động, ở hai chế độ:
  //   thường  -> phải > 0, nếu bằng 0 thì trang không có gì để tắt và gate
  //              tự khai là chưa kiểm được gì (SKIP), không nhận PASS.
  //   reduce  -> phải bằng 0.
  // Vế "thường phải > 0" chính là cái chống tautology: nó ép phép đo phải
  // CHỨNG MINH ĐƯỢC nó phân biệt được hai chế độ trước khi được quyền xanh.
  const demChuyenDong = () => {
    const NGUONG_MS = 1; // 0.001ms cua rule reduce lam tron ve 0.001, duoi nguong
    const doMs = (v) =>
      v
        .split(",")
        .map((s) => s.trim())
        .reduce((max, s) => {
          const n = s.endsWith("ms") ? parseFloat(s) : parseFloat(s) * 1000;
          return Number.isFinite(n) && n > max ? n : max;
        }, 0);
    const dinhDanh = (el) => {
      const cls = (el.getAttribute("class") || "").trim().split(/\s+/).filter(Boolean).slice(0, 2);
      return el.tagName.toLowerCase() + (cls.length ? "." + cls.join(".") : "");
    };
    // Quét CẢ pseudo-element. Bản đầu của gate này chỉ đọc getComputedStyle(el)
    // và ra kết quả "trang không có chuyển động nào" trên chính gallery.html,
    // trong khi components.css:97 có `.sg-card::after { transition: opacity
    // .18s ease }`. Chuyển động của thư viện này nằm gần hết ở ::after (thanh
    // accent chạy ra khi hover), nên bỏ pseudo là bỏ đúng thứ cần đo.
    const co = [];
    for (const el of document.querySelectorAll("*")) {
      for (const pseudo of [null, "::before", "::after"]) {
        const cs = getComputedStyle(el, pseudo);
        const t = doMs(cs.transitionDuration || "0s");
        const a = doMs(cs.animationDuration || "0s");
        if (t > NGUONG_MS || a > NGUONG_MS) {
          co.push(`${dinhDanh(el)}${pseudo || ""} (transition ${t}ms, animation ${a}ms)`);
        }
      }
    }
    return co;
  };

  const dongThuong = await page.evaluate(demChuyenDong);

  const ctxReduced = await browser.newContext({ reducedMotion: "reduce" });
  const pageReduced = await ctxReduced.newPage();
  await pageReduced.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  await pageReduced.evaluate(() => document.fonts.ready);
  const dongReduce = await pageReduced.evaluate(demChuyenDong);
  await pageReduced.close();
  await ctxReduced.close();

  if (dongThuong.length === 0) {
    console.log(
      "[SKIP] reduced-motion-tat-chuyen-dong: trang khong co phan tu nao co transition/animation > 1ms " +
        "o che do thuong, nen khong the chung minh rule @media prefers-reduced-motion co tac dung. " +
        "Khong tinh la PASS.",
    );
  } else {
    record(
      "reduced-motion-tat-chuyen-dong",
      dongReduce.length === 0,
      `che do thuong ${dongThuong.length} phan tu co chuyen dong, che do reduce con ${dongReduce.length}`,
    );
    if (dongReduce.length) console.log("  con chuyen dong khi reduce:", dongReduce.slice(0, 5));
  }

  // ── 2b. Khoá sáng: file giao khách không được đổi màu theo máy người nhận ──
  //
  // Quyết định của người dùng (đợt dọn sau Phase 1): hệ màu tối được GIỮ cho
  // gallery và trang nội bộ, nhưng file giao đi phải khoá sáng. Lý do là thứ
  // đo được chứ không phải khẩu vị: chart matplotlib và minh hoạ SVG đang chỉ
  // có bảng màu sáng, nên một máy khách đặt theme tối sẽ cho trang nền tối mà
  // chart vẫn nền trắng. Khoá sáng cũng có nghĩa bản HTML và bản PDF trùng
  // nhau, vì WeasyPrint vốn vứt khối @media prefers-color-scheme.
  //
  // Cơ chế đã có sẵn trong CSS: mọi rule tối đều viết
  // `:root:not([data-theme="light"])`, nên chỉ cần thẻ <html data-theme="light">
  // là khoá. Gate này KIỂM chứ không tin: mở trang trong context colorScheme
  // "dark" rồi so màu nền và màu chữ với context "light". Trang khai khoá sáng
  // mà hai bên vẫn lệch nghĩa là còn rule tối lọt ra ngoài cơ chế :not().
  const doMau = async (colorScheme) => {
    const c = await browser.newContext({ colorScheme });
    const pg = await c.newPage();
    await pg.goto("file://" + htmlPath, { waitUntil: "networkidle" });
    await pg.evaluate(() => document.fonts.ready);
    const mau = await pg.evaluate(() => {
      const b = getComputedStyle(document.body);
      return {
        nen: b.backgroundColor,
        chu: b.color,
        khaiKhoaSang: document.documentElement.getAttribute("data-theme") === "light",
      };
    });
    await pg.close();
    await c.close();
    return mau;
  };
  const mauSang = await doMau("light");
  const mauToi = await doMau("dark");

  if (!mauSang.khaiKhoaSang) {
    console.log(
      '[SKIP] khoa-sang-khong-doi-theo-may-khach: trang khong khai <html data-theme="light">. ' +
        "Hop le cho trang noi bo (gallery, trang thu nghiem), NHUNG file giao khach thi phai khai, " +
        `hien tai nen doi ${mauSang.nen} sang ${mauToi.nen} khi may khach dat theme toi.`,
    );
  } else {
    const giongNhau = mauSang.nen === mauToi.nen && mauSang.chu === mauToi.chu;
    record(
      "khoa-sang-khong-doi-theo-may-khach",
      giongNhau,
      giongNhau
        ? `nen ${mauSang.nen}, chu ${mauSang.chu}, khong doi o ca hai che do`
        : `LECH: sang(nen ${mauSang.nen}, chu ${mauSang.chu}) vs toi(nen ${mauToi.nen}, chu ${mauToi.chu})`,
    );
  }

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
    // Bẫy every() trên mảng RỖNG: một trang không khai @font-face nào thì
    // fontFamilies = [] và Object.values({}).every(Boolean) === true, gate
    // xanh trong khi chưa kiểm một font nào. Đúng cái bệnh vacuous truth.
    // Với repo này, trang không nhúng font là LỖI THẬT chứ không phải ca
    // ngoại lệ: file giao đi phải tự đủ, không được mượn font máy khách.
    const soFace = fontFamilies.length;
    const allFontsLoaded = soFace > 0 && Object.values(fontsOk).every(Boolean);

    // Phép đo thứ hai, độc lập: MỰC CHỮ. document.fonts.check() chỉ nói font
    // đã sẵn sàng, nó không nói phần tử THẬT có dùng font đó không. Đo bề
    // rộng một chuỗi tiếng Việt có dấu bằng font của <body> rồi so với chính
    // chuỗi đó vẽ bằng một tên font chắc chắn không tồn tại: hai số bằng nhau
    // nghĩa là trang đang rơi về font mặc định trình duyệt.
    const mucChu = await pageOffline.evaluate(() => {
      const ff = getComputedStyle(document.body).fontFamily;
      const ctx2d = document.createElement("canvas").getContext("2d");
      const mau = "Sản lượng vận tải quý IV, tăng 12,4%";
      ctx2d.font = `16px ${ff}`;
      const wThat = ctx2d.measureText(mau).width;
      ctx2d.font = '16px "ht-viz-font-khong-ton-tai-9d3f"';
      const wMacDinh = ctx2d.measureText(mau).width;
      return { ff, wThat: Math.round(wThat * 100) / 100, wMacDinh: Math.round(wMacDinh * 100) / 100 };
    });
    const dungFontRieng = Math.abs(mucChu.wThat - mucChu.wMacDinh) > 0.5;

    record("offline-no-network-requests", blocked.length === 0, `${blocked.length} request bị chặn`);
    record(
      "offline-fonts-available",
      allFontsLoaded,
      soFace === 0
        ? "trang khong khai @font-face nao, khong the tu du khi giao di"
        : `${soFace} face: ${JSON.stringify(fontsOk)}`,
    );
    record(
      "offline-body-dung-font-nhung",
      dungFontRieng,
      `muc chu ${mucChu.wThat}px vs font mac dinh ${mucChu.wMacDinh}px (${mucChu.ff})`,
    );
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
  console.log(allPassed ? "TỔNG KẾT: PASS - mọi kiểm tra đạt." : "TỔNG KẾT: FAIL - xem chi tiết ở trên.");
  process.exit(allPassed ? 0 : 1);
}

main().catch((e) => {
  console.error("Lỗi verify.mjs:", e);
  process.exit(2);
});
