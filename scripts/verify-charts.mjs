#!/usr/bin/env node
// Render lai toan bo chart ECharts va kiem SVG sach.
// LUU Y: echarts.init voi ssr:true KHONG tu thoat process (2 socket handle
// treo, dispose() khong giai phong). Moi script chart phai ket bang
// chart.dispose(); process.exit(0); neu khong se treo vo thoi han.
import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
// Phep kiem XML nam o gates/lib/xml.mjs de gate cua Phase 2 va verify cua Phase 1
// dung CHUNG mot ban. Hai ban song song la cach de hai noi troi khac nhau.
import { kiemTraXml } from '../gates/lib/xml.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'charts/echarts');

let failed = 0;
const log = (ok, msg) => {
  console.log(`${ok ? '[PASS]' : '[FAIL]'} ${msg}`);
  if (!ok) failed += 1;
};

const charts = readdirSync(DIR)
  .filter((f) => /^\d\d-.*\.mjs$/.test(f))
  .sort();

for (const f of charts) {
  try {
    execFileSync('node', [path.join(DIR, f)], { cwd: DIR, timeout: 60000, stdio: 'pipe' });
  } catch (e) {
    log(false, `${f}: chay loi hoac treo -> ${e.message.split('\n')[0]}`);
    continue;
  }
  const svgName = 'out-' + f.replace('.mjs', '.svg');
  const svgPath = path.join(DIR, svgName);
  if (!existsSync(svgPath)) {
    log(false, `${f}: khong sinh ra ${svgName}`);
    continue;
  }
  const svg = readFileSync(svgPath, 'utf8');
  const problems = [];
  if (/<image/.test(svg)) problems.push('co <image>');
  if (/base64/.test(svg)) problems.push('co base64');
  if (!/Spectral|IBM Plex Mono/.test(svg)) problems.push('khong thay font chot');
  if (/#2a78d6|#dc2626|Calibri/i.test(svg)) problems.push('con gia tri mau/font cu');
  const els = (svg.match(/<(rect|path|text|line|circle|polygon)\b/g) || []).length;
  if (els < 10) problems.push(`chi ${els} phan tu, nghi ngo rong`);

  // Gate quan trong nhat cua file nay, va la gate suyt khong ai nghi ra: SVG phai la
  // XML HOP LE. Toan bo 12 chart tung KHONG hop le suot Phase 1 vi font stack boc bang
  // nhay kep bi ECharts nhung thang vao thuoc tinh style="..." cua the <text>, tao ra
  // nhay kep long trong nhay kep. Moi gate cu deu PASS vi chung chi dem chuoi va dem
  // phan tu, khong cai nao PARSE. Hau qua do duoc tren engine dich: WeasyPrint bo qua
  // ca file, PDF ra 0 net ve, chart bien mat sach ma khong bao loi.
  // Trinh duyet van hien dung vi HTML parser de tinh hon, nen soi bang mat tren ban
  // HTML khong bao gio phat hien duoc.
  const loiXml = kiemTraXml(svg);
  if (loiXml) problems.push(`KHONG phai XML hop le (${loiXml}), WeasyPrint se bo qua ca file`);

  // SVG tinh nhung vao bao cao KHONG duoc mang CSS animation. ECharts SSR mac dinh
  // xuat @keyframes cho moi marker, va keyframe cuoi la `transform: scale(n,n)`.
  // CSS transform THANG thuoc tinh XML, va keyframe do khong mang phan translate,
  // nen sau khi animation chay xong marker bi keo ve GOC TOA DO. Da nhin tan mat
  // tren out-04-dumbbell.svg truoc khi va: moi cham bien mat khoi vi tri dung, con
  // mot cham lac o goc tren trai.
  // Chi hong o ban HTML mo bang trinh duyet. Ban PDF khong dinh vi WeasyPrint khong
  // chay CSS animation, va do cung la ly do bug nay song sot ca mot phase: moi phep
  // nghiem thu cua repo hoac di qua PDF hoac di qua gate dem phan tu.
  // Cach chua: `animation: false` trong option, da dat san trong baseOption().
  if (/@keyframes|animation\s*:/.test(svg)) {
    problems.push('con CSS animation, marker se bi keo ve goc toa do khi mo bang trinh duyet');
  }
  log(problems.length === 0, `${svgName}: ${els} phan tu${problems.length ? ' -> ' + problems.join(', ') : ' sach'}`);
}

console.log(failed === 0 ? 'TAT CA PASS' : `${failed} GATE FAIL`);
process.exit(failed === 0 ? 0 : 1);
