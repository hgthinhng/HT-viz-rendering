#!/usr/bin/env node
// guard-source-leak.mjs, chan ro nguon khi xuat ban "external" (gui khach).
// Ap dung bang quy doi tu memory feedback_no_source_disclosure_in_artifacts.md:
//   - cam cac tu chi kenh tin / co quan gan van ban chua cong bo / ten rieng mang luoi.
//   - cam cite/org THAT cua nguon sensitivity=internal_only lo ra ngoai khi mode=external
//     (dau hieu la nhan public_label khong duoc dung, hoac dung sai cho).
//
// Usage: node guard-source-leak.mjs <file.html> [--mode=external|internal]
// Mac dinh mode=external (ban gui di la truong hop phai kiem nghiem ngat nhat).
// Exit 0 = sach, 1 = co ro ri.

import fs from "node:fs";

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith("--"));
const modeArg = args.find((a) => a.startsWith("--mode="));
const mode = modeArg ? modeArg.split("=")[1] : "external";

if (!file || !fs.existsSync(file)) {
  console.error("usage: node guard-source-leak.mjs <file.html> [--mode=external|internal]");
  process.exit(2);
}

const html = fs.readFileSync(file, "utf-8");

// ---- banned phrases (nguyen van tu memory, khong duoc xuat hien trong BAT KY artifact nao) ----
const BANNED_PHRASES = [
  "công an", "đóng dấu", "tận mắt", "tin nhắn", "rò rỉ", "bộ sậu",
  "TUYỆT MẬT", "cuộc gọi", "thấy trên máy", "bị can", "phong toả", "kê biên",
  "hộp đen", "im lặng là chi phí"
];
// ten rieng kieu "anh LV" / "chị NT", chu thuong + 1-3 chu hoa lien tiep
const NAME_IN_NETWORK_RE = /\b(anh|chị|em)\s+[A-ZĐ]{1,3}\b/g;

function stripTagsKeepScriptForLedger(rawHtml) {
  // giu lai script de con parse ledger, nhung bo phan hien thi (text) khoi vong quet banned-phrase
  const noStyle = rawHtml.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ");
  const noScript = noStyle.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ");
  return noScript.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

const visibleText = stripTagsKeepScriptForLedger(html);

const hits = [];

for (const phrase of BANNED_PHRASES) {
  const re = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
  if (re.test(visibleText)) {
    hits.push(`[banned-phrase] xuat hien cum tu cam: "${phrase}"`);
  }
}
let nm;
NAME_IN_NETWORK_RE.lastIndex = 0;
while ((nm = NAME_IN_NETWORK_RE.exec(visibleText)) !== null) {
  hits.push(`[network-name] nghi la ten rieng viet tat trong mang luoi: "${nm[0]}"`);
}

// ---- doi chieu voi ledger: source sensitivity=internal_only khong duoc lo cite/org that khi mode=external ----
const ledgerMatch = html.match(
  /<script[^>]*\bid=["']evidence-ledger["'][^>]*>([\s\S]*?)<\/script>/i
);
let ledger = null;
if (ledgerMatch) {
  try {
    ledger = JSON.parse(ledgerMatch[1]);
  } catch {
    hits.push("[ledger-parse] evidence-ledger khong parse duoc, khong doi chieu duoc sensitivity");
  }
}

if (ledger && mode === "external") {
  for (const s of ledger.sources || []) {
    if (s.sensitivity !== "internal_only") continue;
    for (const field of ["org", "cite"]) {
      const raw = s[field];
      if (raw && visibleText.includes(raw)) {
        hits.push(
          `[internal-cite-leak] source ${s.id} (internal_only): chuoi that "${field}"="${raw}" xuat hien nguyen van trong ban external, phai thay bang public_label`
        );
      }
    }
  }
}

console.log("=".repeat(70));
console.log(`GUARD SOURCE-LEAK, ${file} (mode=${mode})`);
console.log("=".repeat(70));
if (hits.length === 0) {
  console.log("KET QUA: PASS, khong phat hien ro ri");
} else {
  console.log(`KET QUA: FAIL, ${hits.length} diem ro ri`);
  hits.forEach((h) => console.log("  ✗ " + h));
}
console.log("=".repeat(70));
process.exit(hits.length ? 1 : 0);
