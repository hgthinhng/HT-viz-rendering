// verify.mjs — kiểm tra SVG xuất ra là vector THẬT, không phải ảnh raster nhúng.
import fs from 'node:fs';

export function verifySvg(path) {
  const svg = fs.readFileSync(path, 'utf8');
  const count = (re) => (svg.match(re) || []).length;
  const report = {
    file: path,
    bytes: Buffer.byteLength(svg, 'utf8'),
    hasImageTag: /<image[\s>]/i.test(svg),
    hasForeignObject: /<foreignObject/i.test(svg),
    hasBase64: /base64,/i.test(svg),
    paths: count(/<path[\s>]/g),
    rects: count(/<rect[\s>]/g),
    texts: count(/<text[\s>]/g),
    circles: count(/<circle[\s>]/g),
    polylines: count(/<polyline[\s>]/g) + count(/<polygon[\s>]/g),
    isValidXml: svg.trim().startsWith('<svg') && svg.trim().endsWith('</svg>'),
  };
  report.totalElements = report.paths + report.rects + report.texts + report.circles + report.polylines;
  report.clean = !report.hasImageTag && !report.hasForeignObject && !report.hasBase64 && report.isValidXml && report.totalElements > 0;
  return report;
}

export function printReport(r) {
  const status = r.clean ? 'SACH (vector, khong <image>)' : 'CANH BAO';
  console.log(
    `[${status}] ${r.file} | ${r.bytes}B | path=${r.paths} rect=${r.rects} text=${r.texts} circle=${r.circles} poly=${r.polylines} | total=${r.totalElements} | <image>=${r.hasImageTag} base64=${r.hasBase64}`
  );
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const files = process.argv.slice(2);
  let allClean = true;
  for (const f of files) {
    const r = verifySvg(f);
    printReport(r);
    if (!r.clean) allClean = false;
  }
  console.log(allClean ? '\n=== TAT CA SVG SACH ===' : '\n=== CO SVG LOI ===');
  process.exit(allClean ? 0 : 1);
}
