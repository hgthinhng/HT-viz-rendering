#!/usr/bin/env node
/**
 * generate-tokens.mjs, mot nguon su that DUY NHAT cho bang mau chu de.
 *
 *     node design-system/generate-tokens.mjs            # ghi ba dich
 *     node design-system/generate-tokens.mjs --kiem      # khong ghi, chi bao co lech khong (exit 1 neu lech)
 *
 * ## Van de no giai
 *
 * Bang mau cua repo tung ton tai duoi dang chuoi hex VIET TAY o NAM noi: tokens.css
 * (khoi :root dau tien, ban that), tokens.py, charts/echarts/theme.mjs, cong THEM hai
 * noi la TEST tu hardcode ky vong ngay trong than test (tokens_test.py, chart_theme.
 * test.mjs). Nghia la thu canh gac lai la mot ban sao cua thu bi canh: sua mot gia tri
 * o tokens.css khong lam test do, vi test dang so voi chinh no viet tay o cho khac.
 *
 * File nay dao nguoc huong di: design-system/themes/*.json la nguon that, ba dich con
 * lai SINH RA tu do. tokens_test.py va chart_theme.test.mjs sau khi sua doc ky vong
 * TRUC TIEP tu file JSON, khong con hardcode hex trong than test nua.
 *
 * ## Co che "khoi quan ly"
 *
 * Moi file dich (tokens.css, tokens.py, theme.mjs) van la file HAND-MAINTAINED cho
 * phan con lai (mac dinh khong ten, ham, comment giai thich...). Generator chi duoc
 * dung MOT vung duy nhat trong moi file, bao boc bang hai marker:
 *
 *     /* THEME-TOKENS:BAT-DAU *\/  ...  /* THEME-TOKENS:KET-THUC *\/    (CSS)
 *     # THEME-TOKENS:BAT-DAU     ...  # THEME-TOKENS:KET-THUC          (Python)
 *     // THEME-TOKENS:BAT-DAU    ...  // THEME-TOKENS:KET-THUC         (JS)
 *
 * Lan dau chay (marker chua ton tai), script noi them CA khoi (header giai thich +
 * marker + than) vao cuoi file. Tu lan sau, script CHI thay phan NAM GIUA hai marker,
 * khong dung vao bat ky dong nao khac trong file, nen phan hand-maintained an toan.
 *
 * ## Rang buoc: KHONG doi mot gia tri mau nao
 *
 * File JSON dau tien (sang-lanh.json) trich NGUYEN VAN gia tri dang co trong tokens.css
 * khoi :root dau tien, khong go lai tu tri nho. Khoi CSS sinh ra dung selector moi
 * [data-theme="sang-lanh"], KHONG dung vao khoi :root mac dinh dang co san, nen mau
 * render cua moi trang hien tai KHONG doi (chua trang nao khai data-theme="sang-lanh").
 * Day la buoc DUNG CO CHE, chua bat mau moi hay chu de toi nao.
 */
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const THU_MUC_NAY = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(THU_MUC_NAY, '..');
export const THU_MUC_CHU_DE = path.join(THU_MUC_NAY, 'themes');

// Khoa "mau" va "ilus" ma MOI file JSON chu de phai co dung, khong thua khong thieu.
// Day la schema. Doi schema thi sua o day TRUOC, roi moi sua tung file JSON.
export const KHOA_MAU_CHUAN = [
  'paper', 'paper-hi', 'paper-hair', 'paper-elev',
  'ink', 'ink-md', 'ink-lo', 'ink-faint',
  'line', 'line-lo',
  'accent', 'accent-hi', 'accent-soft',
  'pos', 'neg', 'neg-soft',
  'warn',
];
// Dai ket cau CHIN bac, dam nhat la 1 nhat nhat la 9. Ban dau schema nay khai bon
// ten (toi/vua/sang/panel) lay tu illustrations/grammar.md muc 4, nhung dem that
// tren 11 file trong illustrations/svg/ thi chung dung CHIN bac: grammar.md va tai
// san da troi khoi nhau tu truoc. Bon ten cu roi vao bac 2, 4, 6, 8.
export const KHOA_ILUS_CHUAN = ['1', '2', '3', '4', '5', '6', '7', '8', '9'];

const RE_HEX = /^#[0-9a-fA-F]{6}$/;

// Doi ten khoa rieng cho ban JS: theme.mjs hien dang dung "negative"/"positive" (khong
// phai "neg"/"pos") trong PALETTE hand-maintained, va chart_theme.test.mjs da kiem dung
// hai ten do. Chi doi CHINH XAC hai khoa nay, moi khoa con lai chuyen kebab-case sang
// camelCase theo cong thuc thang, khong doi ten nghia.
const JS_DOI_TEN = { neg: 'negative', pos: 'positive' };

function sangCamelCase(kebab) {
  return kebab.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());
}

function khoaJs(kebab) {
  return JS_DOI_TEN[kebab] ?? sangCamelCase(kebab);
}

function khoaPy(kebab) {
  return kebab.replace(/-/g, '_');
}

/** Doc va kiem tra schema cua MOT file chu de. Tra ve mang loi (rong = hop le). */
function kiemTraSchema(id, du) {
  const loi = [];
  if (du.chu_de !== id) {
    loi.push(`truong "chu_de" (${JSON.stringify(du.chu_de)}) phai bang ten file "${id}"`);
  }
  if (typeof du.dung_cho !== 'string' || du.dung_cho.trim() === '') {
    loi.push('thieu truong "dung_cho" hoac de rong');
  }
  for (const [ten_khoi, khoa_chuan] of [['mau', KHOA_MAU_CHUAN], ['ilus', KHOA_ILUS_CHUAN]]) {
    const khoi = du[ten_khoi];
    if (typeof khoi !== 'object' || khoi === null || Array.isArray(khoi)) {
      loi.push(`thieu khoi "${ten_khoi}"`);
      continue;
    }
    const khoaThua = Object.keys(khoi).filter((k) => !khoa_chuan.includes(k));
    const khoaThieu = khoa_chuan.filter((k) => !(k in khoi));
    if (khoaThua.length) loi.push(`"${ten_khoi}" co khoa la, khong nam trong schema: ${khoaThua.join(', ')}`);
    if (khoaThieu.length) loi.push(`"${ten_khoi}" thieu khoa: ${khoaThieu.join(', ')}`);
    for (const [k, v] of Object.entries(khoi)) {
      if (typeof v !== 'string' || !RE_HEX.test(v)) {
        loi.push(`${ten_khoi}.${k} khong phai hex 6 so hop le: ${JSON.stringify(v)}`);
      }
    }
  }
  return loi;
}

/**
 * Doc TAT CA file design-system/themes/*.json, kiem schema, tra ve mang
 * [{ id, duongDan, du }] sap theo TEN FILE (deterministic, khong phu thuoc thu tu he
 * dieu hanh liet ke thu muc). Fail-fast: mot file sai schema thi throw ngay, khong
 * am tham bo qua, vi mot chu de sai se sinh ra tokens sai ma khong ai biet.
 */
export function docTatCaChuDe() {
  if (!existsSync(THU_MUC_CHU_DE)) {
    throw new Error(`khong tim thay thu muc chu de: ${THU_MUC_CHU_DE}`);
  }
  const files = readdirSync(THU_MUC_CHU_DE).filter((f) => f.endsWith('.json')).sort();
  if (files.length === 0) {
    throw new Error(`${THU_MUC_CHU_DE} khong co file *.json nao`);
  }
  const ra = [];
  for (const f of files) {
    const id = f.replace(/\.json$/, '');
    const duongDan = path.join(THU_MUC_CHU_DE, f);
    const du = JSON.parse(readFileSync(duongDan, 'utf8'));
    const loi = kiemTraSchema(id, du);
    if (loi.length) {
      throw new Error(`${f} sai schema:\n  - ${loi.join('\n  - ')}`);
    }
    ra.push({ id, duongDan, du });
  }
  return ra;
}

/** Sinh THAN (khong marker) cho khoi CSS, mot [data-theme="id"] cho moi chu de. */
export function sinhThanCss(dsChuDe) {
  const khoi = dsChuDe.map(({ id, du }) => {
    const dongMau = KHOA_MAU_CHUAN.map((k) => `  --${k}: ${du.mau[k]};`).join('\n');
    const dongIlus = KHOA_ILUS_CHUAN.map((k) => `  --ilus-${k}: ${du.ilus[k]};`).join('\n');
    return `[data-theme="${id}"] {\n${dongMau}\n\n${dongIlus}\n}`;
  });
  return khoi.join('\n\n');
}

/** Sinh THAN (khong marker) cho dict THEMES trong tokens.py. */
export function sinhThanPy(dsChuDe) {
  const dong = ['THEMES = {'];
  for (const { id, du } of dsChuDe) {
    dong.push(`    "${id}": {`);
    dong.push('        "mau": {');
    for (const k of KHOA_MAU_CHUAN) dong.push(`            "${khoaPy(k)}": "${du.mau[k]}",`);
    dong.push('        },');
    dong.push('        "ilus": {');
    for (const k of KHOA_ILUS_CHUAN) dong.push(`            "${k}": "${du.ilus[k]}",`);
    dong.push('        },');
    dong.push('    },');
  }
  dong.push('}');
  return dong.join('\n');
}

/** Sinh THAN (khong marker) cho object PALETTES trong theme.mjs. */
export function sinhThanJs(dsChuDe) {
  const dong = ['export const PALETTES = {'];
  for (const { id, du } of dsChuDe) {
    dong.push(`  '${id}': {`);
    dong.push('    mau: {');
    for (const k of KHOA_MAU_CHUAN) dong.push(`      ${khoaJs(k)}: '${du.mau[k]}',`);
    dong.push('    },');
    dong.push('    ilus: {');
    for (const k of KHOA_ILUS_CHUAN) dong.push(`      ${k}: '${du.ilus[k]}',`);
    dong.push('    },');
    dong.push('  },');
  }
  dong.push('};');
  return dong.join('\n');
}

/**
 * Ghep THAN moi vao noi dung file HIEN CO. Neu hai marker da ton tai, chi thay phan
 * nam giua chung (giu nguyen moi thu khac trong file). Neu chua ton tai, noi them CA
 * khoi (header giai thich, do CAU_HINH_DICH cung cap, cong marker cong than) vao cuoi
 * file. Ham thuan tuy (khong doc/ghi dia), dung chung cho ca che do ghi va che do kiem.
 */
export function apDungKhoi(noiDungCu, moMarker, ketMarker, thanMoi, headerKhiChuaCo) {
  const iMo = noiDungCu.indexOf(moMarker);
  const iKet = noiDungCu.indexOf(ketMarker);
  if (iMo !== -1 && iKet !== -1 && iKet > iMo) {
    const truoc = noiDungCu.slice(0, iMo + moMarker.length);
    const sau = noiDungCu.slice(iKet);
    return `${truoc}\n${thanMoi}\n${sau}`;
  }
  const nenTang = noiDungCu.endsWith('\n') ? noiDungCu : `${noiDungCu}\n`;
  return `${nenTang}\n${headerKhiChuaCo}\n${moMarker}\n${thanMoi}\n${ketMarker}\n`;
}

const HEADER_CSS = `/* ============================================================================
   CHU DE MAU DAT TEN THEO FILE JSON

   Sinh tu design-system/themes/*.json bang design-system/generate-tokens.mjs. DUNG
   SUA TAY vung giua hai marker duoi day; sua gia tri o file JSON tuong ung roi chay:

       node design-system/generate-tokens.mjs
       node design-system/generate-tokens.mjs --kiem   (kiem lech, khong ghi)

   Test drift: tests/consistency/theme_tokens_drift.test.mjs.

   Day la co che CHU DE MAU DAT TEN (bao cao chon TEN bang, khong chon hex), TACH BIET
   voi khoa [data-theme="light"|"dark"] mode man hinh sang/toi da co san o phia tren.
   Hien tai chua trang nao khai data-theme="sang-lanh", nen khoi duoi day KHONG doi mau
   render cua bat ky trang dang chay nao.
   ============================================================================ */`;

const HEADER_PY = `# ==============================================================================
# CHU DE MAU DAT TEN THEO FILE JSON
#
# Sinh tu design-system/themes/*.json bang design-system/generate-tokens.mjs. DUNG SUA
# TAY vung giua hai marker duoi day; sua gia tri o file JSON tuong ung roi chay lai
# generator (xem lenh trong tokens.css). THEMES la dict MOI, tach biet voi COLORS o
# tren: COLORS la ban phang khop voi khoi :root mac dinh cua tokens.css (khong doi),
# THEMES la registry theo TEN chu de cho tuong lai chon bang bang ten.
# ==============================================================================`;

const HEADER_JS = `// ==============================================================================
// CHU DE MAU DAT TEN THEO FILE JSON
//
// Sinh tu design-system/themes/*.json bang design-system/generate-tokens.mjs. DUNG SUA
// TAY vung giua hai marker duoi day; sua gia tri o file JSON tuong ung roi chay lai
// generator. PALETTES la registry MOI theo TEN chu de, tach biet voi PALETTE o tren
// (PALETTE la ban phang hien dang dung that trong moi preset chart, khong doi).
// ==============================================================================`;

export const CAU_HINH_DICH = [
  {
    ten: 'design-system/tokens.css',
    duongDan: path.join(REPO, 'design-system', 'tokens.css'),
    moMarker: '/* THEME-TOKENS:BAT-DAU */',
    ketMarker: '/* THEME-TOKENS:KET-THUC */',
    sinhThan: sinhThanCss,
    header: HEADER_CSS,
  },
  {
    ten: 'design-system/tokens.py',
    duongDan: path.join(REPO, 'design-system', 'tokens.py'),
    moMarker: '# THEME-TOKENS:BAT-DAU',
    ketMarker: '# THEME-TOKENS:KET-THUC',
    sinhThan: sinhThanPy,
    header: HEADER_PY,
  },
  {
    ten: 'charts/echarts/theme.mjs',
    duongDan: path.join(REPO, 'charts', 'echarts', 'theme.mjs'),
    moMarker: '// THEME-TOKENS:BAT-DAU',
    ketMarker: '// THEME-TOKENS:KET-THUC',
    sinhThan: sinhThanJs,
    header: HEADER_JS,
  },
];

/** Tinh noi dung MOI cho mot muc trong CAU_HINH_DICH, khong ghi dia. */
export function tinhNoiDungMoi(muc, dsChuDe) {
  const noiDungCu = readFileSync(muc.duongDan, 'utf8');
  const than = muc.sinhThan(dsChuDe);
  const noiDungMoi = apDungKhoi(noiDungCu, muc.moMarker, muc.ketMarker, than, muc.header);
  return { noiDungCu, noiDungMoi };
}

function main() {
  const keKiem = process.argv.includes('--kiem');
  let dsChuDe;
  try {
    dsChuDe = docTatCaChuDe();
  } catch (err) {
    console.error(`chu de mau LOI: ${err.message}`);
    return 1;
  }

  if (keKiem) {
    const lech = [];
    for (const muc of CAU_HINH_DICH) {
      const { noiDungCu, noiDungMoi } = tinhNoiDungMoi(muc, dsChuDe);
      if (noiDungCu !== noiDungMoi) lech.push(muc.ten);
    }
    if (lech.length) {
      for (const t of lech) console.error(`token LECH: ${t} da troi khoi ma nguon design-system/themes/*.json`);
      console.error('Chay: node design-system/generate-tokens.mjs');
      return 1;
    }
    console.log(`token khop ma nguon (${dsChuDe.length} chu de: ${dsChuDe.map((c) => c.id).join(', ')})`);
    return 0;
  }

  for (const muc of CAU_HINH_DICH) {
    const { noiDungCu, noiDungMoi } = tinhNoiDungMoi(muc, dsChuDe);
    if (noiDungCu !== noiDungMoi) writeFileSync(muc.duongDan, noiDungMoi, 'utf8');
  }
  console.log(`token OK: ${dsChuDe.length} chu de (${dsChuDe.map((c) => c.id).join(', ')})`);
  for (const muc of CAU_HINH_DICH) console.log(`  ${muc.ten}`);
  return 0;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  process.exit(main());
}
