#!/usr/bin/env node
// validator.mjs, kiem tra evidence ledger nhung trong file HTML.
// Usage: node validator.mjs <file.html>
//
// Ledger phai duoc nhung dang:
//   <script type="application/json" id="evidence-ledger"> {...} </script>
// Body phai gan so hien thi bang: <span data-evid="v_xxx">16,0 ty USD</span>
//
// Kiem tra:
//  1. Structural: ledger khop schema/evidence-ledger.schema.json (Ajv, draft 2020-12).
//  2. Orphan value -> source: moi value.source_id phai ton tai trong sources[].
//  3. Orphan source -> value (chieu nguoc): moi source phai duoc >=1 value tham chieu.
//  4. Tier drift: value.tier phai khop dung sources[value.source_id].tier.
//  5. Future date: retrieved_date (value) va published_date (source) khong duoc o tuong lai
//     so voi ngay chay that cua may (process real clock, khong phai ngay hu cau trong noi dung).
//  6. Unit consistency: trong cung 1 chart_id, moi value.unit phai giong het nhau.
//  7. HTML <-> ledger binding: moi data-evid trong body phai tro ve 1 value.id co that (dangling);
//     text hien thi cua the do phai khop value.display (neu ledger co khai display) (mismatch);
//     value co "display" nhung khong bao gio duoc data-evid nao tham chieu -> WARN (declared nhung khong hien).
//
// Exit code: 0 = khong co ERROR (WARN van duoc phep), 1 = co >=1 ERROR, 2 = loi doc file/parse.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function fail(msg) {
  console.error("LOI: " + msg);
  process.exit(2);
}

const file = process.argv[2];
if (!file) fail("usage: node validator.mjs <file.html>");
if (!fs.existsSync(file)) fail(`khong tim thay file: ${file}`);

const html = fs.readFileSync(file, "utf-8");

// ---- 1. trich ledger JSON tu the <script type="application/json" id="evidence-ledger"> ----
const ledgerMatch = html.match(
  /<script[^>]*\bid=["']evidence-ledger["'][^>]*>([\s\S]*?)<\/script>/i
);
if (!ledgerMatch) fail("khong tim thay <script id=\"evidence-ledger\"> trong file");

let ledger;
try {
  ledger = JSON.parse(ledgerMatch[1]);
} catch (e) {
  fail("evidence-ledger khong phai JSON hop le: " + e.message);
}

const schema = JSON.parse(
  fs.readFileSync(path.join(__dirname, "schema/evidence-ledger.schema.json"), "utf-8")
);

const ajv = new Ajv2020({ allErrors: true, strict: false });
addFormats(ajv);
const validateSchema = ajv.compile(schema);

const errors = [];
const warnings = [];

const schemaOk = validateSchema(ledger);
if (!schemaOk) {
  for (const e of validateSchema.errors) {
    errors.push(`[schema] ${e.instancePath || "(root)"} ${e.message}`);
  }
}

// Neu vo schema nghiem trong (thieu sources/values) thi dung som, khong co gi de doi chieu.
if (!ledger || !Array.isArray(ledger.sources) || !Array.isArray(ledger.values)) {
  printReport(file, errors, warnings, { sources: 0, values: 0 });
  process.exit(errors.length ? 1 : 0);
}

// ---- 2/3/4/5/6: doi chieu logic tren du lieu da parse duoc, du schema loi tung phan ----
const sourceById = new Map();
for (const s of ledger.sources) {
  if (!s || typeof s.id !== "string") continue;
  if (sourceById.has(s.id)) errors.push(`[source-dup] id nguon lap: ${s.id}`);
  sourceById.set(s.id, s);
}

const referenced = new Set();
const parseLooseDate = (d) => {
  if (typeof d !== "string") return null;
  const parts = d.split("-");
  const y = parseInt(parts[0], 10);
  const m = parts[1] ? parseInt(parts[1], 10) - 1 : 0;
  const day = parts[2] ? parseInt(parts[2], 10) : 1;
  if (Number.isNaN(y)) return null;
  return new Date(Date.UTC(y, m, day));
};
const NOW = new Date(); // dong ho that cua may chay validator, khong phai ngay hu cau trong noi dung

// 5b. published_date cua source khong duoc o tuong lai
for (const s of ledger.sources) {
  if (!s) continue;
  const pd = parseLooseDate(s.published_date);
  if (pd && pd.getTime() > NOW.getTime()) {
    errors.push(`[future-date] source ${s.id}: published_date=${s.published_date} sau ngay chay validator (${NOW.toISOString().slice(0, 10)})`);
  }
  if (s.sensitivity === "internal_only" && !s.public_label) {
    errors.push(`[missing-label] source ${s.id}: sensitivity=internal_only nhung thieu public_label (khong export duoc ban gui di)`);
  }
}

// group theo chart_id de kiem don vi
const unitByChart = new Map();

for (const v of ledger.values) {
  if (!v || typeof v.id !== "string") continue;

  // 2. orphan value -> source
  if (!v.source_id || !sourceById.has(v.source_id)) {
    errors.push(`[orphan-value] value ${v.id}: source_id="${v.source_id}" khong ton tai trong sources[]`);
  } else {
    referenced.add(v.source_id);
    const src = sourceById.get(v.source_id);
    // 4. tier drift
    if (v.tier && src.tier && v.tier !== src.tier) {
      errors.push(`[tier-drift] value ${v.id}: tier="${v.tier}" khac voi source ${v.source_id}.tier="${src.tier}"`);
    }
  }

  // 5a. retrieved_date tuong lai
  const rd = parseLooseDate(v.retrieved_date);
  if (rd && rd.getTime() > NOW.getTime()) {
    errors.push(`[future-date] value ${v.id}: retrieved_date=${v.retrieved_date} sau ngay chay validator (${NOW.toISOString().slice(0, 10)})`);
  }

  // 6. gom nhom don vi theo chart_id
  if (v.chart_id) {
    if (!unitByChart.has(v.chart_id)) unitByChart.set(v.chart_id, []);
    unitByChart.get(v.chart_id).push({ id: v.id, unit: v.unit });
  }
}

// 3. orphan source (chieu nguoc): dang ky nhung khong ai dung
for (const s of ledger.sources) {
  if (!s || !s.id) continue;
  if (!referenced.has(s.id)) {
    warnings.push(`[orphan-source] source ${s.id} duoc dang ky nhung khong co value nao tham chieu (nguon "mo coi chieu nguoc")`);
  }
}

// 6. don vi khong nhat quan trong cung chart
for (const [chartId, entries] of unitByChart) {
  const units = new Set(entries.map((e) => e.unit));
  if (units.size > 1) {
    errors.push(
      `[unit-mismatch] chart_id="${chartId}" co nhieu don vi khac nhau: ` +
        entries.map((e) => `${e.id}=${e.unit}`).join(", ")
    );
  }
}

// ---- 7. doi chieu voi phan hien thi trong HTML (data-evid="...") ----
const bodyMatch = html.split(/<\/script>/i).join("</script>\n"); // giu nguyen, chi de an toan split
const evidTagRe = /data-evid=["']([^"']+)["'][^>]*>([^<]*)</g;
const seenInBody = new Set();
let m;
// Loai bo noi dung script/style truoc khi quet de tranh dinh nham vao chinh JSON ledger.
const htmlNoScripts = html
  .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
  .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ");
while ((m = evidTagRe.exec(htmlNoScripts)) !== null) {
  const [, evidId, text] = m;
  seenInBody.add(evidId);
  const v = ledger.values.find((x) => x && x.id === evidId);
  if (!v) {
    errors.push(`[dangling-evid] HTML co data-evid="${evidId}" nhung khong co value nao trong ledger mang id nay`);
    continue;
  }
  if (typeof v.display === "string") {
    const shown = text.trim();
    if (shown !== v.display.trim()) {
      errors.push(
        `[display-mismatch] data-evid="${evidId}": HTML hien "${shown}" nhung ledger.display="${v.display}"`
      );
    }
  }
}
for (const v of ledger.values) {
  if (v && v.id && !seenInBody.has(v.id)) {
    warnings.push(`[unused-value] value ${v.id} khai bao trong ledger nhung khong co data-evid nao trong HTML hien no ra`);
  }
}

function printReport(fileArg, errs, warns, counts) {
  console.log("=".repeat(70));
  console.log("EVIDENCE LEDGER VALIDATOR -", fileArg);
  console.log("=".repeat(70));
  console.log(`sources: ${counts.sources ?? ledger.sources.length}  values: ${counts.values ?? ledger.values.length}`);
  console.log(`ngay chay (dong ho that): ${NOW.toISOString().slice(0, 10)}`);
  console.log("-".repeat(70));
  if (errs.length === 0) {
    console.log("ERRORS: 0");
  } else {
    console.log(`ERRORS: ${errs.length}`);
    errs.forEach((e) => console.log("  ✗ " + e));
  }
  console.log("-".repeat(70));
  if (warns.length === 0) {
    console.log("WARNINGS: 0");
  } else {
    console.log(`WARNINGS: ${warns.length}`);
    warns.forEach((w) => console.log("  ! " + w));
  }
  console.log("=".repeat(70));
  console.log(errs.length ? "KET QUA: FAIL" : "KET QUA: PASS");
}

printReport(file, errors, warnings, { sources: ledger.sources.length, values: ledger.values.length });
process.exit(errors.length ? 1 : 0);
