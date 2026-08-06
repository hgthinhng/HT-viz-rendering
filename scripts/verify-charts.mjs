#!/usr/bin/env node
// Render lai toan bo chart ECharts va kiem SVG sach.
// LUU Y: echarts.init voi ssr:true KHONG tu thoat process (2 socket handle
// treo, dispose() khong giai phong). Moi script chart phai ket bang
// chart.dispose(); process.exit(0); neu khong se treo vo thoi han.
import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

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
  log(problems.length === 0, `${svgName}: ${els} phan tu${problems.length ? ' -> ' + problems.join(', ') : ' sach'}`);
}

console.log(failed === 0 ? 'TAT CA PASS' : `${failed} GATE FAIL`);
process.exit(failed === 0 ? 0 : 1);
