import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('PALETTE cua chart khop token loi', async () => {
  const { PALETTE } = await import(path.join(ROOT, 'charts/echarts/theme.mjs'));
  const expected = {
    accent: '#2251FF',
    accentHi: '#1233B8',
    accentSoft: '#7D9BFF',
    negative: '#C22F4E',
    positive: '#008A6D',
    warn: '#B07A10',
    ink: '#051C2C',
    inkMd: '#42566A',
    inkLo: '#8595A6',
    line: '#DBE2EA',
    paper: '#FFFFFF',
  };
  for (const [k, v] of Object.entries(expected)) {
    assert.ok(k in PALETTE, `PALETTE thieu khoa ${k}`);
    assert.equal(PALETTE[k].toUpperCase(), v, `PALETTE.${k} lech: ${PALETTE[k]} mong doi ${v}`);
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
