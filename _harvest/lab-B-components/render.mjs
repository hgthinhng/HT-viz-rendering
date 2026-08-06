// Nghiệm thu thật: render gallery.html bằng playwright-core + chromium cache,
// chụp screenshot, xuất PDF, và đo mật độ ký tự tiếng Việt thật trên trang.
import { chromium } from "playwright-core";
import path from "node:path";
import { fileURLToPath } from "node:url";
import fs from "node:fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, "gallery.html");
const outDir = __dirname;

const consoleErrors = [];
const pageErrors = [];

async function main() {
  const browser = await chromium.launch({
    executablePath: "/home/hgthinhng/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome",
    headless: true,
  });

  // ── 1. Màn hình thường (screen media) ────────────────────────────────
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });
  page.on("pageerror", (err) => pageErrors.push(String(err)));

  await page.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300); // đảm bảo ResizeObserver/JS layout đã chạy xong

  await page.screenshot({ path: path.join(outDir, "screenshot-full.png"), fullPage: true });

  // Crop vài component trọng điểm để soi bằng mắt
  const crops = [
    ["c01-statgrid", "crop-01-statgrid.png"],
    ["c02-gate", "crop-02-gate-ladder.png"],
    ["c03-wallchart", "crop-03-wallchart.png"],
    ["c04-swimlane", "crop-04-swimlane.png"],
    ["c06-quad", "crop-06-quad2x2.png"],
    ["c09-notebox", "crop-09-notebox.png"],
    ["c23-termmag", "crop-23-termmag-diacritics.png"],
    ["c24-keypoint", "crop-24-keypoint.png"],
  ];
  for (const [id, file] of crops) {
    const el = await page.$("#" + id);
    if (el) await el.screenshot({ path: path.join(outDir, file) });
  }

  // ── 2. Đo mật độ ký tự tiếng Việt thật (Spectral 17px, max-width 65ch) ──
  const density = await page.evaluate(() => {
    function measure(text) {
      const div = document.createElement("div");
      div.style.cssText =
        "position:absolute;left:-9999px;top:0;visibility:hidden;max-width:65ch;" +
        "font-family:'EB Garamond',Georgia,serif;font-size:17px;line-height:1.7;" +
        "white-space:normal;overflow-wrap:break-word;";
      div.textContent = text;
      document.body.appendChild(div);
      const range = document.createRange();
      const node = div.firstChild;
      let firstLineBreak = text.length;
      let lastTop = null;
      for (let i = 0; i < text.length; i++) {
        range.setStart(node, i);
        range.setEnd(node, i + 1);
        const rect = range.getBoundingClientRect();
        if (lastTop === null) lastTop = rect.top;
        else if (rect.top > lastTop + 1) { firstLineBreak = i; break; }
      }
      const lineHeightPx = 17 * 1.7;
      const totalLines = Math.round(div.scrollHeight / lineHeightPx);
      const widthPx = div.getBoundingClientRect().width;
      document.body.removeChild(div);
      return { firstLineBreak, totalLines, textLength: text.length, widthPx };
    }
    const samples = {
      "khong_dau_it": "Doanh thu tang truong on dinh trong ba quy lien tiep nho toi uu tuyen khai thac chinh.",
      "co_dau_thuong": "Doanh thu tăng trưởng ổn định trong ba quý liên tiếp nhờ tối ưu tuyến khai thác chính.",
      "dau_chong_day": "Đội tàu vẫn chịu áp lực nhượng bộ ngưỡng nợ vay, được ưởng ứng ước lượng ổn thỏa hơn dự kiến ban đầu.",
      "cau_dai_thuc_te": "Chi phí nhiên liệu đã vượt chi phí thuyền viên để trở thành khoản mục lớn nhất trong giá vốn khai thác đội tàu năm nay.",
    };
    const out = {};
    for (const [k, v] of Object.entries(samples)) out[k] = measure(v);
    return out;
  });

  // ── 3. Kiểm tra chiều cao dòng có đủ cho dấu chồng (ừ ệ ẫ ữ ỗ ộ) ────────
  const diacriticCheck = await page.evaluate(() => {
    function check(text, fontSize, lineHeight, fontFamily) {
      const div = document.createElement("div");
      div.style.cssText =
        `position:absolute;left:-9999px;top:0;visibility:hidden;` +
        `font-family:${fontFamily};font-size:${fontSize}px;line-height:${lineHeight};` +
        `white-space:nowrap;`;
      div.textContent = text;
      document.body.appendChild(div);
      const rect = div.getBoundingClientRect();
      const expectedLineBox = fontSize * lineHeight;
      document.body.removeChild(div);
      return { renderedHeight: rect.height, expectedLineBox, overflowRisk: rect.height > expectedLineBox + 0.5 };
    }
    return {
      body_17_lh1_7_ebgaramond: check("ường ệ ẫ ữ ỗ ộ ẫu tưởng nghiêng ưỡng", 17, 1.7, "'EB Garamond',Georgia,serif"),
      h2_30_lh1_32_fraunces: check("Lộ trình mở rộng đội tàu, khử carbon và tưởng ứng ràng buộc mới", 30.2, 1.32, "'Fraunces',Georgia,serif"),
      h3_23_lh1_32_fraunces: check("Ba câu hỏi thường gặp về ràng buộc pháp lý", 22.7, 1.32, "'Fraunces',Georgia,serif"),
      h1_44_lh1_32_fraunces: check("Định vị dòng tiền tự do và ràng buộc pháp lý ngành hàng hải", 44, 1.32, "'Fraunces',Georgia,serif"),
      label_11_mono: check("BIÊN LỢI NHUẬN ƯỚC TÍNH", 11, 1.6, "'JetBrains Mono',monospace"),
      label_11_sans: check("BIÊN LỢI NHUẬN ƯỚC TÍNH", 11, 1.6, "'Inter',sans-serif"),
    };
  });

  // ── 3b. Đo ink-height THẬT bằng Canvas measureText (khác diacriticCheck ở
  // trên: getBoundingClientRect().height của 1 div luôn = fontSize*lineHeight
  // theo định nghĩa CSS, không phản ánh mực chữ có thật sự tràn ra ngoài hộp
  // dòng hay không — đó là phép đo dàn trang, không phải phép đo mực chữ.
  // actualBoundingBoxAscent/Descent của Canvas 2D mới là mực chữ thật, đo
  // độc lập với line-height khai báo. Trang gallery.html đã tự tải đủ các
  // family/weight qua nội dung thật nên phép đo này không bị lỗi "font chưa
  // tải" như lần thử đầu trên trang trống.
  const inkMetrics = await page.evaluate(() => {
    function ink(text, fontSize, weight, fontFamily) {
      const c = document.createElement("canvas");
      const ctx = c.getContext("2d");
      ctx.font = `${weight} ${fontSize}px ${fontFamily}`;
      const m = ctx.measureText(text);
      return {
        ascent: Math.round(m.actualBoundingBoxAscent * 100) / 100,
        descent: Math.round(m.actualBoundingBoxDescent * 100) / 100,
        inkHeight: Math.round((m.actualBoundingBoxAscent + m.actualBoundingBoxDescent) * 100) / 100,
      };
    }
    const worst = "ường ệ ẫ ữ ỗ ộ ẫu tưởng nghiêng ưỡng Ộ Ễ Ữ";
    const rows = [
      ["ebgaramond_body_400_17px", worst, 17, 400, "'EB Garamond'"],
      ["fraunces_h2_600_30px", "Lộ trình khử carbon", 30.2, 600, "Fraunces"],
      ["fraunces_h1_600_44px", "Định vị dòng tiền tự do", 44, 600, "Fraunces"],
    ];
    const out = {};
    rows.forEach(([label, text, sz, wt, ff]) => { out[label] = ink(text, sz, wt, ff); });
    return out;
  });
  // So khớp inkHeight với line-box thật (fontSize*lineHeight của CSS system)
  // để có kết luận "còn dư bao nhiêu px" thay vì chỉ true/false.
  const inkVsLineBox = {
    ebgaramond_body: { ...inkMetrics.ebgaramond_body_400_17px, lineBox: 17 * 1.7, marginPx: +(17 * 1.7 - inkMetrics.ebgaramond_body_400_17px.inkHeight).toFixed(2) },
    fraunces_h2: { ...inkMetrics.fraunces_h2_600_30px, lineBox: 30.2 * 1.32, marginPx: +(30.2 * 1.32 - inkMetrics.fraunces_h2_600_30px.inkHeight).toFixed(2) },
    fraunces_h1: { ...inkMetrics.fraunces_h1_600_44px, lineBox: 44 * 1.32, marginPx: +(44 * 1.32 - inkMetrics.fraunces_h1_600_44px.inkHeight).toFixed(2) },
  };

  fs.writeFileSync(
    path.join(outDir, "density-report.json"),
    JSON.stringify({ density, diacriticCheck, inkVsLineBox }, null, 2)
  );

  // ── 4. Kiểm tra reduced-motion (context riêng) ──────────────────────────
  const ctxReduced = await browser.newContext({ reducedMotion: "reduce", viewport: { width: 1280, height: 900 } });
  const pageReduced = await ctxReduced.newPage();
  await pageReduced.goto("file://" + htmlPath, { waitUntil: "networkidle" });
  await pageReduced.evaluate(() => document.fonts.ready);
  const reducedMotionMatches = await pageReduced.evaluate(() => matchMedia("(prefers-reduced-motion: reduce)").matches);
  await pageReduced.close();
  await ctxReduced.close();

  // ── 5. Xuất PDF (bản in) ─────────────────────────────────────────────
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: path.join(outDir, "gallery-print.pdf"),
    format: "A4",
    printBackground: true,
    margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" },
  });
  await page.emulateMedia({ media: "screen" });

  await browser.close();

  fs.writeFileSync(
    path.join(outDir, "render-log.json"),
    JSON.stringify({ consoleErrors, pageErrors, reducedMotionMatches }, null, 2)
  );

  console.log("DONE");
  console.log("consoleErrors:", consoleErrors.length, consoleErrors);
  console.log("pageErrors:", pageErrors.length, pageErrors);
  console.log("reducedMotionMatches:", reducedMotionMatches);
}

main().catch((e) => { console.error(e); process.exit(1); });
