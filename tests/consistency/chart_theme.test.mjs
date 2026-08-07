import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

// Doc ky vong TU design-system/themes/sang-lanh.json, KHONG hardcode hex trong than
// test. Truoc ban nay, ky vong nam ngay trong dict `expected` viet tay ben duoi: thu
// canh gac (test) la mot BAN SAO cua thu bi canh (theme.mjs), nen sua mot gia tri o
// theme.mjs se khong lam test nay do. Nguon that duy nhat la file JSON, sinh ra ca
// tokens.css lan theme.mjs bang design-system/generate-tokens.mjs.
//
// PALETTE (hand-maintained, dang la ban dung THAT trong moi preset chart) dat ten
// "negative"/"positive" thay vi "neg"/"pos" cua JSON; ban do KHONG phai bang gia tri
// nen giu nguyen o day, khong phai mot ban sao cua gia tri mau.
const TEN_MAP_JSON_SANG_PALETTE = {
  accent: 'accent',
  'accent-hi': 'accentHi',
  'accent-soft': 'accentSoft',
  neg: 'negative',
  pos: 'positive',
  warn: 'warn',
  ink: 'ink',
  'ink-md': 'inkMd',
  'ink-lo': 'inkLo',
  line: 'line',
  paper: 'paper',
};

function kyVongTuChuDeMacDinh() {
  const du = JSON.parse(
    readFileSync(path.join(ROOT, 'design-system/themes/sang-lanh.json'), 'utf8'),
  );
  const ra = {};
  for (const [tenJson, tenPalette] of Object.entries(TEN_MAP_JSON_SANG_PALETTE)) {
    ra[tenPalette] = du.mau[tenJson];
  }
  return ra;
}

test('PALETTE cua chart khop token loi', async () => {
  const { PALETTE } = await import(path.join(ROOT, 'charts/echarts/theme.mjs'));
  const expected = kyVongTuChuDeMacDinh();
  for (const [k, v] of Object.entries(expected)) {
    assert.ok(k in PALETTE, `PALETTE thieu khoa ${k}`);
    assert.equal(PALETTE[k].toUpperCase(), v.toUpperCase(), `PALETTE.${k} lech: ${PALETTE[k]} mong doi ${v} (theo design-system/themes/sang-lanh.json)`);
  }
});

test('font stack co Spectral va ket thuc bang generic keyword', async () => {
  const { FONT_STACK, FONT_STACK_MONO } = await import(path.join(ROOT, 'charts/echarts/theme.mjs'));
  assert.match(FONT_STACK, /Spectral/, 'FONT_STACK khong co Spectral');
  assert.match(FONT_STACK, /(serif|sans-serif)\s*$/, 'FONT_STACK khong ket thuc bang generic keyword, se roi dau tieng Viet');
  assert.match(FONT_STACK_MONO, /IBM Plex Mono/, 'FONT_STACK_MONO khong co IBM Plex Mono');
  assert.match(FONT_STACK_MONO, /monospace\s*$/, 'FONT_STACK_MONO khong ket thuc bang monospace');
});

test('khong file chart nao con hex cu', () => {
  const dir = path.join(ROOT, 'charts/echarts');
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.mjs'))) {
    const s = readFileSync(path.join(dir, f), 'utf8');
    for (const old of ['#2a78d6', '#dc2626', '#3c3c41', '#9a9992', '#dbdee4', 'Calibri']) {
      assert.doesNotMatch(
        s,
        new RegExp(old, 'i'),
        `${f} con gia tri cu "${old}", phai dung token loi`,
      );
    }
  }
});

test('khong chart nao la gauge hoac radar', () => {
  const dir = path.join(ROOT, 'charts/echarts');
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.mjs'))) {
    const s = readFileSync(path.join(dir, f), 'utf8');
    assert.doesNotMatch(s, /type\s*:\s*['"]gauge['"]/, `${f} dung series gauge, da bi cam`);
    assert.doesNotMatch(s, /type\s*:\s*['"]radar['"]/, `${f} dung series radar, da bi cam`);
  }
});

// F1 fix round 1: chan hardcode hex/ten mau CSS tran o BAT KY file chart nao
// ngoai theme.mjs. theme.mjs la nguon chan ly duy nhat cho mau (PALETTE) nen
// duoc mien; moi file chart khac PHAI tham chieu PALETTE.<khoa>, khong duoc
// tu bien hex hay ten mau tran (kể cả trung tinh nhu '#fff'), vi mot gia tri
// sot lai se lech am tham khi PALETTE doi ma khong test nao bat duoc.
test('khong file chart nao hardcode hex hoac ten mau CSS tran ngoai theme.mjs', () => {
  const dir = path.join(ROOT, 'charts/echarts');
  const hexPattern = /#[0-9a-fA-F]{3,8}\b/;
  const namedColorPattern = /\b(?:color|fill|stroke|background(?:Color)?|stop-color|borderColor)\s*:\s*['"]?(white|black|red|green|blue|yellow|gray|grey|orange|purple|pink|cyan|magenta|brown)\b/i;
  for (const f of readdirSync(dir).filter((x) => x.endsWith('.mjs') && x !== 'theme.mjs')) {
    const s = readFileSync(path.join(dir, f), 'utf8');
    assert.doesNotMatch(s, hexPattern, `${f} hardcode hex, phai lay tu PALETTE trong theme.mjs`);
    assert.doesNotMatch(s, namedColorPattern, `${f} dung ten mau CSS tran, phai lay tu PALETTE trong theme.mjs`);
  }
});
