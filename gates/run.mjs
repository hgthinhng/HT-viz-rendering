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
 *
 * Co --ghi-nghiem-thu=<path> (ca hai lan): ghi ket qua thanh nghiem-thu.json MAY
 * SINH dung schema spec muc 6, dung de dua mot exemplar len trang thai chinh-thuc.
 * Co --lenh-tai-tao="<cmd>" di kem de ghi de lenh tai tao mac dinh (vi lenh chua dau
 * bang va khoang trang nen phai parse bang slice, khong dung split('=')).
 */
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { chayTatCa, TEN_GATES_PDF } from './gates.mjs';
import { chayTatCaSong, TEN_GATES_SONG } from './gates_song.mjs';

const NGANG = '='.repeat(78);

/**
 * Ghi bang chung MAY SINH ra dia, khong phai bang chung viet tay. Registry ten
 * gate lay tu chinh gates.mjs / gates_song.mjs (xem TEN_GATES_PDF/TEN_GATES_SONG),
 * nen phien_ban_bo_gate troi theo so gate that ngay khi co gate moi.
 *
 * WARN duoc anh xa thanh PASS kem truong canh_bao: WARN khong chan giao file,
 * nen nghiem-thu.json coi no la dat nhung khong duoc giau canh bao.
 */
function ghiNghiemThuJson(duongDan, ketQua, lan, lenhTaiTao) {
  const registry = lan === 'html-song' ? TEN_GATES_SONG : TEN_GATES_PDF;
  const sha = execSync('git rev-parse --short HEAD', { encoding: 'utf8' }).trim();
  const ho_so = {
    sinh_boi: 'gates/run.mjs --ghi-nghiem-thu',
    ngay: new Date().toISOString().slice(0, 10),
    sha,
    lenh_tai_tao: lenhTaiTao || `node gates/run.mjs ${process.argv.slice(2).filter((a) => !a.startsWith('--ghi-nghiem-thu')).join(' ')}`,
    lan,
    phien_ban_bo_gate: `${lan === 'html-song' ? 'song' : 'pdf'}-${registry.length}`,
    gate: ketQua.map((g) => {
      const muc = { ten: g.ten, ket_qua: g.trang_thai === 'WARN' ? 'PASS' : g.trang_thai };
      if (g.trang_thai === 'SKIP') muc.ly_do = g.ly_do.join('; ') || 'khong ghi ly do';
      if (g.trang_thai === 'WARN') muc.canh_bao = g.ly_do.join('; ');
      return muc;
    }),
  };
  fs.writeFileSync(duongDan, JSON.stringify(ho_so, null, 2) + '\n');
  console.log(`Da ghi nghiem thu: ${duongDan}`);
}

function inKetQuaVaThoat(ketQua, { lan, ghiNghiemThu, lenhTaiTao } = {}) {
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
  if (ghiNghiemThu) ghiNghiemThuJson(ghiNghiemThu, ketQua, lan, lenhTaiTao);
  process.exit(coFail ? 1 : 0);
}

const args = process.argv.slice(2);
const viTri = args.filter((a) => !a.startsWith('--'));
const lan = (args.find((a) => a.startsWith('--lan=')) || '--lan=pdf-so').split('=')[1];
const ghiNT = (args.find((a) => a.startsWith('--ghi-nghiem-thu=')) || '').split('=')[1] || null;
const ltIdx = args.findIndex((a) => a.startsWith('--lenh-tai-tao='));
const lenhTaiTao = ltIdx >= 0 ? args[ltIdx].slice('--lenh-tai-tao='.length) : null;

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
  inKetQuaVaThoat(ketQua, { lan, ghiNghiemThu: ghiNT, lenhTaiTao });
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
  inKetQuaVaThoat(ketQua, { lan, ghiNghiemThu: ghiNT, lenhTaiTao });
}
