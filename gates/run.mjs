#!/usr/bin/env node
/**
 * run.mjs, chay ca bo gate roi in bang. Exit 1 neu co bat ky FAIL cung nao.
 *
 * Usage (lan pdf-so, mac dinh, giu nguyen hanh vi cu):
 *   node gates/run.mjs <file.html> <file.pdf> [--che-do=noi-bo|gui-di] [--cho-phep-anh=N]
 *
 * Usage (lan html-song, chin gate moi trong gates_song.mjs):
 *   node gates/run.mjs <file.html> --lan=html-song
 *
 * Che do doi hai thu (chi lan pdf-so): ban `gui-di` khong nhung so nguon nen gate
 * LEDGER SKIP co ly do, va guard ro ri nguon chay o muc ngat nhat. Ban `noi-bo`
 * thi nguoc lai.
 *
 * Lan html-song KHONG can file PDF: dac ta cu doi ca hai duong dan nen lan nay
 * khong chay duoc tren nhanh mac dinh, day la ly do co --lan rieng.
 */
import fs from 'node:fs';
import path from 'node:path';
import { chayTatCa } from './gates.mjs';
import { chayTatCaSong } from './gates_song.mjs';

const NGANG = '='.repeat(78);

function inKetQuaVaThoat(ketQua) {
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
}

const args = process.argv.slice(2);
const viTri = args.filter((a) => !a.startsWith('--'));
const lan = (args.find((a) => a.startsWith('--lan=')) || '--lan=pdf-so').split('=')[1];

if (lan === 'html-song') {
  const [duongDanHtml] = viTri;
  if (!duongDanHtml) {
    console.error('usage: node gates/run.mjs <file.html> --lan=html-song');
    process.exit(2);
  }
  if (!fs.existsSync(duongDanHtml)) {
    console.error('khong tim thay file:', duongDanHtml);
    process.exit(2);
  }

  const ketQua = await chayTatCaSong({ duongDanHtml: path.resolve(duongDanHtml) });

  console.log(NGANG);
  console.log(`BO GATE NGHIEM THU (lan html-song)  ${duongDanHtml}`);
  console.log(NGANG);
  inKetQuaVaThoat(ketQua);
} else {
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

  console.log(NGANG);
  console.log(`BO GATE NGHIEM THU  ${duongDanHtml}  +  ${duongDanPdf}   (che do ${cheDo})`);
  console.log(NGANG);
  inKetQuaVaThoat(ketQua);
}
