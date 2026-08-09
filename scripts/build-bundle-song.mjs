#!/usr/bin/env node
// build-bundle-song.mjs, sinh bundle JavaScript nhung vao an pham lan `html-song`.
//
// Ra: charts/echarts/ra-song/bundle-song.js, mot file IIFE gan `window.HTViz`.
// File ra da gitignore: no sinh lai duoc tu nguon trong khoang mot giay, va commit mot
// file 700KB sinh tu dong vao repo la cach nhanh nhat de no troi khoi nguon.
//
// Vi sao can mot buoc build o mot repo von khong co bundler: an pham lan `html-song` la
// MOT file mo bang `file://`, ma 18 preset lai la 18 module ESM import lan nhau. Trinh
// duyet khong fetch duoc module anh em qua `file://`, nen phai gom truoc. Bundler cung
// la thu duy nhat lam duoc tree-shaking that: xem `echarts-song.mjs`.
import { build } from 'esbuild';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { mkdirSync, statSync } from 'node:fs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const GOC = path.resolve(HERE, '..');
const VAO = path.join(GOC, 'charts', 'echarts', 'song-entry.mjs');
const THU_MUC_RA = path.join(GOC, 'charts', 'echarts', 'ra-song');
export const DUONG_BUNDLE = path.join(THU_MUC_RA, 'bundle-song.js');

/** Tran dung luong. Ban day du cua ECharts la 1,1MB va ca diem cua buoc nay la khong
 * keo ban do; 900KB cho ca ECharts da rut gon cong 18 preset la con so du rong de khong
 * bao dong gia, nhung van do ngay khi ai do lo import lai `echarts` day du o dau do. */
const TRAN_BYTE = 900 * 1024;

export async function dungBundle({ im = false } = {}) {
  mkdirSync(THU_MUC_RA, { recursive: true });
  const ket_qua = await build({
    entryPoints: [VAO],
    outfile: DUONG_BUNDLE,
    bundle: true,
    // ESM chu khong phai IIFE, va day la mot rang buoc CHAT chu khong phai khau vi:
    // nhanh CLI cua ca 18 preset dung `await import('node:fs')` o cap cao nhat cua
    // module, ma esbuild khong dung duoc top-level await trong IIFE. Doi lai, trang
    // phai nhung bang `<script type="module">`. Inline module KHONG phat sinh request
    // nao nen van chay qua `file://`, tuc rang buoc "mot file tu du" khong bi vi pham.
    format: 'esm',
    platform: 'browser',
    // `node:fs` chi bi cham toi trong nhanh CLI, ma nhanh do gac sau
    // `typeof process !== 'undefined'` nen trong trinh duyet khong bao gio chay toi.
    // De external la giu nguyen loi goi import() do trong ban ra, khong phai xoa no.
    // `./render-static.mjs` cung phai external, va day la cho DE MAT NHAT cua ca buoc
    // nay: no chi bi goi trong nhanh CLI bang `await import()`, nhung esbuild van keo
    // ca module dong vao bundle, ma module do import `echarts` DAY DU. Khong external
    // thi bundle ra 1.197KB tuc con nang hon ban day du, va tat ca cong tree-shaking
    // thanh cong coc. Tran dung luong ben duoi sinh ra chinh de bat ca nay.
    external: ['node:fs', './render-static.mjs'],
    minify: true,
    target: ['chrome110', 'firefox110', 'safari16'],
    charset: 'utf8',
    legalComments: 'none',
    logLevel: im ? 'silent' : 'info',
    metafile: true,
  });
  const size = statSync(DUONG_BUNDLE).size;
  if (size > TRAN_BYTE) {
    throw new Error(
      `bundle-song.js nang ${(size / 1024).toFixed(1)}KB, vuot tran ${(TRAN_BYTE / 1024).toFixed(0)}KB. ` +
        'Nhieu kha nang mot module vua import `echarts` day du thay vi `echarts-song.mjs`.',
    );
  }
  return { size, metafile: ket_qua.metafile };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const { size } = await dungBundle();
  console.log(`bundle-song.js: ${(size / 1024).toFixed(1)}KB (tran ${(TRAN_BYTE / 1024).toFixed(0)}KB)`);
  process.exit(0);
}
