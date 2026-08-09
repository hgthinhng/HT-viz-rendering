#!/usr/bin/env node
// anh-moc.mjs, chup anh moc cua preset chart va so pixel voi ban dang co.
//
// LOP LOI NO CHAN, va vi sao khong gate nao hien co chan duoc:
//
// Bo gate cua repo doc CAU TRUC (parse XML, dem net ve, doc tang text cua PDF, do bbox
// so voi viewBox). Ca bo do mu voi mot lop loi: hinh van dung cau truc nhung NHIN da
// khac di. Doi mot hang so padding, doi thang mau, sua mot ham layout, sua mot dinh dang
// so, tat ca deu co the lam hinh xau di ma khong phep do nao doi mau.
//
// Phep do o day la visual regression: chup lai, so tung pixel voi anh moc luu trong
// repo. No khong biet the nao la DEP, no chi biet the nao la KHAC. Do dung la thu can:
// mot thay doi thi giac ngoai y muon se hien ra thanh mot con so.
//
// GIOI HAN, noi thang: no chi bat duoc thay doi so voi moc, nen mot hinh xau NGAY TU
// DAU thi no khong bao gi ca, va no khong thay duoc gi trong mot an pham moi chua co
// moc. Hai lop loi do thuoc ve gate chu tran viewBox va gate nhan chong, xem
// `tests/consistency/chu_khong_tran_viewbox.test.mjs`.
//
//   node scripts/anh-moc.mjs              so sanh, in bang, exit 1 neu lech
//   node scripts/anh-moc.mjs --cap-nhat   ghi de anh moc bang ban hien tai
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { launchChromium } from './lib/chromium.mjs';
import { PRESETS } from '../charts/echarts/registry.mjs';
import { renderStatic } from '../charts/echarts/render-static.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const THU_MUC_MOC = path.join(GOC, 'gates', 'fixtures', 'anh-moc');
const CSS_FONT = path.join(GOC, 'design-system', 'fonts', 'fonts-embedded.css');

/** Sau preset lam mau dai dien, khong phai ca 18.
 *
 * Chon theo LOAI SERIES chu khong theo thu tu, de moi duong ve chinh cua ECharts deu co
 * mot dai dien: custom (waterfall), sankey, heatmap, line cong graphic (line-annotated),
 * bar (bar-ranking), va heatmap dang luoi so (sensitivity-grid). Chup ca 18 thi them
 * 12 file PNG vao mot repo public de doi lay do phu gan nhu khong tang. */
export const MUC_TIEU = [
  { ten: '01-waterfall', rong: 700, cao: 400 },
  { ten: '02-sankey', rong: 760, cao: 400 },
  { ten: '08-heatmap', rong: 760, cao: 300 },
  { ten: '13-line-annotated', rong: 700, cao: 400 },
  { ten: '14-bar-ranking', rong: 700, cao: 420 },
  { ten: '18-sensitivity-grid', rong: 700, cao: 420 },
];

/** Pixel coi la KHAC khi mot kenh lech qua nguong nay.
 *
 * 12 tren 255 chu khong phai 0: vien chu chong rang khac nhau vai don vi giua hai lan
 * raster ma mat khong phan biet duoc, va mot gate do 0 se do vi ly do khong ai sua duoc. */
const NGUONG_KENH = 12;
/** Ty le pixel khac toi da truoc khi coi la LECH.
 *
 * 0,05% chu khong phai 0,3%, va con so nay den tu MUTATION chu khong tu cam giac. Ban
 * dau dat 0,3% cho an toan; mutation doi mot nhan tu `120` sang `120,00` chi lam 0,242%
 * pixel khac nen LOT QUA, tuc gate xanh trong khi hinh da doi that. Do lai tinh tat
 * dinh: chup cung mot preset hai lan lien tiep cho dung 0,000% khac, nghia la bien an
 * toan can chua chong rang gan nhu bang khong. 0,05% cua 700x400 la khoang 140 pixel,
 * van rong gap nhieu lan nhieu do va van bat duoc mutation tren. */
const NGUONG_TY_LE = 0.0005;

function trangChua(svg, rong, cao) {
  const css = readFileSync(CSS_FONT, 'utf8');
  return `<!doctype html><html lang="vi" data-theme="light"><head><meta charset="utf-8">
<style>${css}
html,body{margin:0;padding:0;background:#FFFFFF}
#khung{width:${rong}px;height:${cao}px}
#khung svg{display:block;width:100%;height:100%}</style></head>
<body><div id="khung">${svg}</div></body></html>`;
}

async function chup(browser, muc) {
  const preset = PRESETS[muc.ten];
  if (!preset) throw new Error(`khong co preset ${muc.ten}`);
  const svg = renderStatic(preset.option, preset.MAC_DINH, { width: muc.rong, height: muc.cao });
  const page = await browser.newPage({
    viewport: { width: muc.rong + 20, height: muc.cao + 20 },
    deviceScaleFactor: 1,
  });
  await page.setContent(trangChua(svg, muc.rong, muc.cao), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const anh = await page.locator('#khung').screenshot({ type: 'png' });
  await page.close();
  return anh;
}

/** So hai PNG bang canvas TRONG trinh duyet.
 *
 * Node khong co bo giai ma PNG san, va them mot thu vien chi de doc pixel la them mot
 * phu thuoc cho mot viec ma Chromium dang mo san lam duoc. */
async function soPixel(browser, pngA, pngB) {
  const page = await browser.newPage();
  await page.setContent('<!doctype html><meta charset="utf-8"><body></body>');
  const ra = await page.evaluate(
    async ([a, b, nguong]) => {
      const nap = (base64) =>
        new Promise((res, rej) => {
          const im = new Image();
          im.onload = () => res(im);
          im.onerror = rej;
          im.src = 'data:image/png;base64,' + base64;
        });
      const [ia, ib] = await Promise.all([nap(a), nap(b)]);
      if (ia.width !== ib.width || ia.height !== ib.height) {
        return { kichThuocLech: `${ia.width}x${ia.height} so voi ${ib.width}x${ib.height}` };
      }
      const ve = (im) => {
        const c = document.createElement('canvas');
        c.width = im.width;
        c.height = im.height;
        c.getContext('2d').drawImage(im, 0, 0);
        return c.getContext('2d').getImageData(0, 0, im.width, im.height).data;
      };
      const da = ve(ia);
      const db = ve(ib);
      let khac = 0;
      for (let i = 0; i < da.length; i += 4) {
        const d = Math.max(
          Math.abs(da[i] - db[i]),
          Math.abs(da[i + 1] - db[i + 1]),
          Math.abs(da[i + 2] - db[i + 2]),
        );
        if (d > nguong) khac++;
      }
      const tong = da.length / 4;
      return { khac, tong, tyLe: khac / tong };
    },
    [pngA.toString('base64'), pngB.toString('base64'), NGUONG_KENH],
  );
  await page.close();
  return ra;
}

/** Chay ca bo. Tra ve mang ket qua, khong tu in va khong tu thoat, de test dung lai. */
export async function doAnhMoc({ capNhat = false } = {}) {
  mkdirSync(THU_MUC_MOC, { recursive: true });
  const browser = await launchChromium();
  const ra = [];
  try {
    for (const muc of MUC_TIEU) {
      const duong = path.join(THU_MUC_MOC, `${muc.ten}.png`);
      const hienTai = await chup(browser, muc);
      if (capNhat || !existsSync(duong)) {
        writeFileSync(duong, hienTai);
        ra.push({ ten: muc.ten, trangThai: capNhat ? 'DA-GHI' : 'MOI', bytes: hienTai.length });
        continue;
      }
      const moc = readFileSync(duong);
      const d = await soPixel(browser, moc, hienTai);
      if (d.kichThuocLech) {
        ra.push({ ten: muc.ten, trangThai: 'LECH', ly_do: `kich thuoc khac: ${d.kichThuocLech}` });
      } else if (d.tyLe > NGUONG_TY_LE) {
        ra.push({
          ten: muc.ten,
          trangThai: 'LECH',
          tyLe: d.tyLe,
          ly_do: `${d.khac} tren ${d.tong} pixel khac (${(d.tyLe * 100).toFixed(3)}%), tren nguong ${(NGUONG_TY_LE * 100).toFixed(3)}%`,
        });
      } else {
        ra.push({ ten: muc.ten, trangThai: 'KHOP', tyLe: d.tyLe });
      }
    }
  } finally {
    await browser.close();
  }
  return ra;
}

/** Chup CUNG mot preset hai lan roi so, de do chinh do TAT DINH cua phep do.
 *
 * Mot gate visual regression khong tat dinh la mot gate do ngau nhien, va no se bi tat
 * sau vai lan do oan. Ham nay cho phep test khang dinh dieu do bang so thay vi bang
 * niem tin. */
export async function doTinhTatDinh(tenPreset) {
  const muc = MUC_TIEU.find((m) => m.ten === tenPreset) || MUC_TIEU[0];
  const browser = await launchChromium();
  try {
    const a = await chup(browser, muc);
    const b = await chup(browser, muc);
    return await soPixel(browser, a, b);
  } finally {
    await browser.close();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const capNhat = process.argv.includes('--cap-nhat');
  const ket = await doAnhMoc({ capNhat });
  let hong = 0;
  for (const r of ket) {
    if (r.trangThai === 'LECH') hong++;
    const them = r.ly_do ? `  ${r.ly_do}` : r.tyLe !== undefined ? `  (${(r.tyLe * 100).toFixed(3)}% pixel khac)` : '';
    console.log(`[${r.trangThai}] ${r.ten}${them}`);
  }
  if (hong) {
    console.log(`\n${hong} hinh lech so voi anh moc. Neu doi la CO Y, xem lai anh roi chay:`);
    console.log('  node scripts/anh-moc.mjs --cap-nhat');
  }
  process.exit(hong ? 1 : 0);
}
