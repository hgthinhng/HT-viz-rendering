#!/usr/bin/env node
/**
 * run.mjs — chay ca bo gate roi in bang. Exit 1 neu co bat ky FAIL cung nao.
 *
 * Usage:
 *   node gates/run.mjs <file.html> <file.pdf> [--che-do=noi-bo|gui-di] [--cho-phep-anh=N]
 *
 * Che do doi hai thu: ban `gui-di` khong nhung so nguon nen gate LEDGER SKIP co ly do,
 * va guard ro ri nguon chay o muc ngat nhat. Ban `noi-bo` thi nguoc lai.
 */
import fs from 'node:fs';
import { chayTatCa } from './gates.mjs';

const args = process.argv.slice(2);
const viTri = args.filter((a) => !a.startsWith('--'));
const [duongDanHtml, duongDanPdf] = viTri;
const cheDo = (args.find((a) => a.startsWith('--che-do=')) || '--che-do=noi-bo').split('=')[1];
const choPhepAnh = Number((args.find((a) => a.startsWith('--cho-phep-anh=')) || '--cho-phep-anh=0').split('=')[1]);

if (!duongDanHtml || !duongDanPdf) {
  console.error('usage: node gates/run.mjs <file.html> <file.pdf> [--che-do=noi-bo|gui-di] [--cho-phep-anh=N]');
  process.exit(2);
}
for (const f of [duongDanHtml, duongDanPdf]) {
  if (!fs.existsSync(f)) {
    console.error('khong tim thay file:', f);
    process.exit(2);
  }
}

const ketQua = chayTatCa({ duongDanHtml, duongDanPdf, cheDo, choPhepAnh });

const NGANG = '='.repeat(78);
console.log(NGANG);
console.log(`BO GATE NGHIEM THU  ${duongDanHtml}  +  ${duongDanPdf}   (che do ${cheDo})`);
console.log(NGANG);

let coFail = false;
const dem = { PASS: 0, WARN: 0, FAIL: 0, SKIP: 0 };
for (const g of ketQua) {
  dem[g.trang_thai] = (dem[g.trang_thai] || 0) + 1;
  if (g.trang_thai === 'FAIL') coFail = true;
  console.log(`[${g.trang_thai.padEnd(4)}] ${g.ten}`);
  for (const l of g.ly_do) console.log(`         - ${l}`);
}
console.log(NGANG);
console.log(`TONG: ${dem.PASS} PASS, ${dem.WARN} WARN, ${dem.FAIL} FAIL, ${dem.SKIP} SKIP`);
console.log(coFail ? 'KET QUA: FAIL, khong duoc giao file' : 'KET QUA: PASS (van doc ky phan WARN truoc khi giao)');
process.exit(coFail ? 1 : 0);
