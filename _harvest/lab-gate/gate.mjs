#!/usr/bin/env node
// gate.mjs — bo gate nghiem thu truoc khi giao file cho khach.
// Usage: node gate.mjs <file.html> <file.pdf>
//
// 6 gate:
//   1. FONT       — HTML dung font co tren Windows, hoac nhung base64 + unicode-range tieng Viet.
//   2. RASTER     — dem /Subtype /Image qua xref (pymupdf), khong dung get_images (bo sot Tiling Pattern).
//   3. DIACRITICS — so sanh mat do dau tieng Viet giua HTML nguon va PDF da render + FFFD + ky tu "synthetic".
//   4. STYLE      — cam em-dash/en-dash, cam ket luan cach ngon, cam AI-slop, bat tieng Anh lac trong nhan.
//   5. PAGEBREAK  — CSS co bao ve ngat trang khong (proxy) + hinh hoc: panel bi cat dung bien trang (that).
//   6. SOURCE-LEAK— noi mach 1: chay guard-source-leak.mjs (banned phrase + internal cite leak).
//
// In bang PASS/FAIL/WARN kem ly do. Exit 1 neu co >=1 FAIL cung.

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EVIDENCE_DIR = path.join(__dirname, "..", "lab-evidence");

const [, , htmlFile, pdfFile] = process.argv;
if (!htmlFile || !pdfFile) {
  console.error("usage: node gate.mjs <file.html> <file.pdf>");
  process.exit(2);
}
if (!fs.existsSync(htmlFile)) { console.error("khong tim thay HTML:", htmlFile); process.exit(2); }
if (!fs.existsSync(pdfFile)) { console.error("khong tim thay PDF:", pdfFile); process.exit(2); }

const html = fs.readFileSync(htmlFile, "utf-8");
const results = []; // { name, status: PASS|FAIL|WARN, reasons: [] }

function record(name, status, reasons) {
  results.push({ name, status, reasons: reasons || [] });
}

// ---------------------------------------------------------------------
// GATE 1 — FONT
// ---------------------------------------------------------------------
(function gateFont() {
  const WINDOWS_SAFE = [
    "segoe ui", "times new roman", "arial", "calibri", "cambria",
    "georgia", "consolas", "courier new", "tahoma", "verdana"
  ];
  const reasons = [];
  let status = "PASS";

  // 1a. thu thap @font-face: ten -> { hasDataUri, unicodeRanges: [] }
  const faceRe = /@font-face\s*{([^}]*)}/gis;
  const faces = new Map();
  let fm;
  while ((fm = faceRe.exec(html)) !== null) {
    const block = fm[1];
    const nameMatch = block.match(/font-family:\s*["']?([^;"'\n]+)["']?\s*;/i);
    if (!nameMatch) continue;
    const name = nameMatch[1].trim().toLowerCase();
    const hasDataUri = /src:\s*url\(data:font\//i.test(block);
    const urMatch = block.match(/unicode-range:\s*([^;]+);/i);
    const ranges = urMatch ? urMatch[1].split(",").map((s) => s.trim()) : [];
    if (!faces.has(name)) faces.set(name, { hasDataUri: false, ranges: [] });
    const entry = faces.get(name);
    entry.hasDataUri = entry.hasDataUri || hasDataUri;
    entry.ranges.push(...ranges);
  }

  // Vietnamese phai co it nhat 1 range phu combining-mark/tone-mark hoac khoi tien-compose U+1EA0-1EF9
  function coversVietnamese(ranges) {
    return ranges.some((r) => {
      const rr = r.toUpperCase();
      if (rr.includes("1EA0") || rr.includes("1EF")) return true; // khoi tien-compose co dau
      if (/U\+030[0139]/.test(rr)) return true; // combining tone marks: grave/acute/tilde/dot-below
      return false;
    });
  }

  // 1b. thu thap moi khai bao font-family dung trong selector thuong (khong phai @font-face)
  const bodyCss = html.replace(faceRe, " ");
  const usageRe = /font-family:\s*([^;]+);/gi;
  const stacksSeen = new Set();
  let um;
  while ((um = usageRe.exec(bodyCss)) !== null) {
    stacksSeen.add(um[1].trim());
  }

  const badStacks = [];
  for (const stack of stacksSeen) {
    // var(--x) khong xet truc tiep o day (se resolve qua khai bao --sans/--mono/--serif ben duoi)
    if (/^var\(/i.test(stack)) continue;
    const first = stack.split(",")[0].trim().replace(/^["']|["']$/g, "").toLowerCase();
    if (WINDOWS_SAFE.includes(first)) continue;
    if (faces.has(first)) {
      const f = faces.get(first);
      if (f.hasDataUri && coversVietnamese(f.ranges)) continue; // embedded + phu dau tieng Viet -> OK
      badStacks.push({ stack, reason: !f.hasDataUri ? "khong nhung base64 (@font-face khong co data: URI)" : "unicode-range khong thay ro phu dau tieng Viet" });
      continue;
    }
    badStacks.push({ stack, reason: "khong phai font Windows chuan, khong co @font-face nhung kem theo" });
  }

  // 1c. resolve bien --sans/--mono/--serif neu co, ap lai check tren gia tri thuc
  const varDefRe = /--(sans|mono|serif):\s*([^;]+);/gi;
  let vm;
  while ((vm = varDefRe.exec(html)) !== null) {
    const stack = vm[2].trim();
    const first = stack.split(",")[0].trim().replace(/^["']|["']$/g, "").toLowerCase();
    if (WINDOWS_SAFE.includes(first)) continue;
    if (faces.has(first)) {
      const f = faces.get(first);
      if (f.hasDataUri && coversVietnamese(f.ranges)) continue;
      badStacks.push({ stack: `--${vm[1]}: ${stack}`, reason: !f.hasDataUri ? "khong nhung base64" : "unicode-range khong phu dau tieng Viet" });
    } else {
      badStacks.push({ stack: `--${vm[1]}: ${stack}`, reason: "font dau tien khong Windows-safe va khong duoc @font-face nhung" });
    }
  }

  // 1d. cam ho Liberation/Noto khong nhung (fallback he thong tren Linux, vo dung tren Windows)
  const banList = ["liberation", "noto"];
  for (const [name, f] of faces) {
    if (banList.some((b) => name.includes(b)) && !f.hasDataUri) {
      badStacks.push({ stack: name, reason: "font ho Liberation/Noto nhung KHONG nhung base64 — se fallback vo dung tren Windows" });
    }
  }

  if (faces.size === 0 && stacksSeen.size === 0) {
    status = "WARN";
    reasons.push("khong tim thay khai bao font-family nao, khong kiem duoc");
  } else if (badStacks.length > 0) {
    status = "FAIL";
    for (const b of badStacks) reasons.push(`stack "${b.stack}": ${b.reason}`);
  } else {
    reasons.push(`${faces.size} @font-face nhung base64 + Windows-safe fallback, ${stacksSeen.size} stack dung trong CSS deu OK`);
  }
  record("1. FONT", status, reasons);
})();

// ---------------------------------------------------------------------
// GATE 2 & 3 & 5b — can PDF, goi pdf_checks.py mot lan
// ---------------------------------------------------------------------
let pdfData = null;
try {
  const out = execFileSync("python3", [path.join(__dirname, "pdf_checks.py"), pdfFile], {
    maxBuffer: 1024 * 1024 * 64,
  });
  pdfData = JSON.parse(out.toString());
} catch (e) {
  record("2. RASTER", "FAIL", ["khong chay duoc pdf_checks.py: " + e.message]);
  record("3. DIACRITICS", "FAIL", ["khong chay duoc pdf_checks.py: " + e.message]);
  record("5. PAGEBREAK", "FAIL", ["khong chay duoc pdf_checks.py: " + e.message]);
}

if (pdfData) {
  // GATE 2 — RASTER
  (function gateRaster() {
    const r = pdfData.raster;
    const reasons = [];
    let status = "PASS";
    const BYTES_PER_PAGE_WARN = 150 * 1024;
    const BYTES_PER_PAGE_FAIL = 300 * 1024;
    const IMAGE_OBJ_FAIL = 30;
    const BIG_PANEL_FAIL = 1; // >=1 anh full-panel (>500k px) la dau hieu blur/gradient-alpha bi nuong bitmap

    reasons.push(`${r.image_objects} object /Subtype /Image (xref scan) trong ${pdfData.pages} trang; ${pdfData.bytes_per_page.toFixed(0)} bytes/trang; file ${(pdfData.file_size_bytes / 1e6).toFixed(2)}MB`);

    if (r.big_panel_images.length >= BIG_PANEL_FAIL) {
      status = "FAIL";
      reasons.push(`${r.big_panel_images.length} anh full-panel (>500.000px) — dau hieu blur/backdrop-filter/gradient-alpha bi Chromium nuong thanh bitmap. Vi du: ${r.big_panel_images.slice(0, 3).map((i) => `${i.w}x${i.h}`).join(", ")}`);
    }
    if (r.image_objects > IMAGE_OBJ_FAIL) {
      status = "FAIL";
      reasons.push(`so object anh (${r.image_objects}) vuot nguong ${IMAGE_OBJ_FAIL}`);
    }
    if (pdfData.bytes_per_page > BYTES_PER_PAGE_FAIL) {
      status = "FAIL";
      reasons.push(`bytes/trang (${(pdfData.bytes_per_page/1024).toFixed(0)}KB) vuot nguong FAIL ${(BYTES_PER_PAGE_FAIL/1024).toFixed(0)}KB`);
    } else if (pdfData.bytes_per_page > BYTES_PER_PAGE_WARN && status === "PASS") {
      status = "WARN";
      reasons.push(`bytes/trang (${(pdfData.bytes_per_page/1024).toFixed(0)}KB) vuot nguong WARN ${(BYTES_PER_PAGE_WARN/1024).toFixed(0)}KB`);
    }
    record("2. RASTER", status, reasons);
  })();

  // GATE 3 — DIACRITICS
  (function gateDiacritics() {
    const d = pdfData.diacritics;
    const reasons = [];
    let status = "PASS";

    // dem dau tieng Viet trong HTML nguon (loai script/style/tag)
    const textOnly = html
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ");
    const VIET_RE = /[ăâêôơưđẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐạảãàáăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/g;
    const htmlVietCount = (textOnly.match(VIET_RE) || []).length;

    reasons.push(`dau tieng Viet: HTML nguon (text tinh) = ${htmlVietCount}, PDF da render = ${d.viet_diacritic_total}`);

    if (d.fffd_count > 0) {
      status = "FAIL";
      reasons.push(`co ${d.fffd_count} ky tu U+FFFD (glyph mat hoan toan) trong PDF`);
    }
    if (d.viet_diacritic_synthetic > 0) {
      status = "FAIL";
      reasons.push(`${d.viet_diacritic_synthetic} ky tu co dau bi MuPDF danh dau "synthetic" (khong chac chan glyph dung) — nghi ngo vo dau`);
    }
    // canh bao neu PDF co dau it hon dang ke so voi HTML tinh — luu y: PDF thuong >= HTML tinh
    // vi mot phan noi dung duoc JS render (vd danh sach nguon) khong nam trong text tinh cua HTML.
    if (htmlVietCount > 0 && d.viet_diacritic_total < htmlVietCount * 0.9) {
      status = status === "PASS" ? "WARN" : status;
      reasons.push(`PDF co it dau tieng Viet hon HTML tinh ~${(100 * (1 - d.viet_diacritic_total / htmlVietCount)).toFixed(0)}% — kiem tra xem co noi dung bi rung khi render khong`);
    }
    reasons.push(
      "GIOI HAN: day la kiem tra tang van ban (text-extraction), khong bat duoc truong hop " +
      "ToUnicode van dung ma glyph outline trong font subset bi thay bang .notdef (tofu) khi hien thi. " +
      "Theo memory feedback_font_linux_khong_dung_cho_file_gui_di: buoc xac nhan cuoi cung BAT BUOC la " +
      "mo bang trinh duyet that, chup man hinh, phong to soi ừ ộ ẫ ợ ữ ể ỗ — gate nay KHONG thay the buoc do " +
      "(sandbox khong co tesseract/pytesseract de OCR that)."
    );
    record("3. DIACRITICS", status, reasons);
  })();

  // GATE 5 — PAGEBREAK
  (function gatePagebreak() {
    const reasons = [];
    let status = "PASS";
    const cssBlocks = (html.match(/<style\b[^>]*>([\s\S]*?)<\/style>/gi) || []).join("\n");
    const hasBreakInside = /break-inside\s*:\s*avoid/i.test(cssBlocks);
    const hasPageBreakInside = /page-break-inside\s*:\s*avoid/i.test(cssBlocks);
    const hasMediaPrint = /@media\s+print/i.test(cssBlocks);

    if (!hasBreakInside && !hasPageBreakInside) {
      status = "WARN";
      reasons.push("HTML khong co bat ky rule break-inside/page-break-inside:avoid nao — khong co co che bao ve, moi lan reflow lai co the sinh cat trang moi");
    } else {
      reasons.push("HTML co khai bao break-inside/page-break-inside:avoid");
    }
    if (!hasMediaPrint) {
      reasons.push("khong co @media print rieng (khong bat buoc, nhung thieu thi kho kiem soat margin/kich thuoc trang khi in)");
    }

    const pb = pdfData.pagebreak;
    if (pb.total_hits > 0) {
      status = "FAIL";
      reasons.push(`PHAT HIEN THAT: ${pb.total_hits} panel/card bi cat dung bien trang (hinh chu nhat cung mau, cung toa do trai/phai, mep duoi trang N = mep tren trang N+1): ${JSON.stringify(pb.sliced_panel_hits.slice(0, 5))}`);
    } else {
      reasons.push("kiem hinh hoc tren PDF that: 0 panel bi cat dung bien trang trong lan render nay");
      if (status === "WARN") {
        reasons.push("LUU Y: 0 hit hien tai co the la MAY RUI cua lan reflow nay, khong phai do thiet ke — vi khong co CSS bao ve, sua noi dung/kich thuoc font sau nay co the lam panel lech qua trang ma khong ai canh bao");
      }
    }
    record("5. PAGEBREAK", status, reasons);
  })();
}

// ---------------------------------------------------------------------
// GATE 4 — STYLE (em-dash, aphorism, AI-slop, English jargon)
// ---------------------------------------------------------------------
(function gateStyle() {
  const reasons = [];
  let status = "PASS";
  const textOnly = html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ");

  const emEn = textOnly.match(/[—–]/g);
  if (emEn && emEn.length > 0) {
    status = "FAIL";
    reasons.push(`${emEn.length} em-dash/en-dash trong noi dung hien thi (cam theo feedback_no_em_dash_no_slop_humanizer)`);
  }

  const slopTerms = [
    "Điều đáng chú ý", "Không thể phủ nhận", "Tóm lại", "Đáng chú ý",
    "Trong bối cảnh", "Hơn nữa,", "Bên cạnh đó,"
  ];
  const slopHits = slopTerms.filter((t) => textOnly.includes(t));
  if (slopHits.length > 0) {
    status = "FAIL";
    reasons.push(`AI-slop: ${slopHits.join(" | ")}`);
  }

  const aph1 = textOnly.match(/không [^.]{0,40} bằng [^.]{0,45}, chỉ/g);
  const aph2 = textOnly.match(/nhất cũng là [^.]{0,30} nhất/g);
  if ((aph1 && aph1.length) || (aph2 && aph2.length)) {
    status = "FAIL";
    reasons.push(`cau ket luan kieu cach ngon: ${[...(aph1 || []), ...(aph2 || [])].join(" || ")}`);
  }

  const jargon = ["VERDICT", "ROE", "KPI", "review", "timeline", "matrix", "scenario", "insight", "framework"];
  const jargonHits = [];
  for (const j of jargon) {
    const re = new RegExp(`\\b${j}\\b`, "g");
    const n = (textOnly.match(re) || []).length;
    if (n > 0) jargonHits.push(`${j}×${n}`);
  }
  if (jargonHits.length > 0) {
    status = status === "PASS" ? "WARN" : status;
    reasons.push(`tieng Anh lac trong nhan (khong tu dong FAIL, can soi tay xem co phai nhan trang dau khong): ${jargonHits.join(", ")}`);
  }

  if (reasons.length === 0) reasons.push("khong phat hien em-dash / AI-slop / cach ngon / jargon lac");
  record("4. STYLE", status, reasons);
})();

// ---------------------------------------------------------------------
// GATE 6 — SOURCE-LEAK (noi mach 1)
// ---------------------------------------------------------------------
(function gateSourceLeak() {
  const reasons = [];
  let status = "PASS";
  try {
    execFileSync("node", [path.join(EVIDENCE_DIR, "guard-source-leak.mjs"), htmlFile, "--mode=external"], {
      stdio: "pipe",
    });
    reasons.push("guard-source-leak: PASS (xem chi tiet lenh rieng neu can log day du)");
  } catch (e) {
    status = "FAIL";
    const out = (e.stdout ? e.stdout.toString() : "") + (e.stderr ? e.stderr.toString() : "");
    const lines = out.split("\n").filter((l) => l.includes("✗"));
    reasons.push(...(lines.length ? lines.map((l) => l.trim()) : ["guard-source-leak FAIL (xem output goc)"]));
  }
  record("6. SOURCE-LEAK", status, reasons);
})();

// ---------------------------------------------------------------------
// In bang tong ket
// ---------------------------------------------------------------------
console.log("=".repeat(78));
console.log(`GATE SUITE — ${htmlFile} + ${pdfFile}`);
console.log("=".repeat(78));
let hardFail = false;
for (const r of results) {
  const icon = r.status === "PASS" ? "PASS" : r.status === "WARN" ? "WARN" : "FAIL";
  if (r.status === "FAIL") hardFail = true;
  console.log(`[${icon}] ${r.name}`);
  for (const reason of r.reasons) console.log(`       - ${reason}`);
}
console.log("=".repeat(78));
console.log(hardFail ? "TONG KET: FAIL — khong duoc ship" : "TONG KET: PASS (co the co WARN can soi tay)");
process.exit(hardFail ? 1 : 0);
