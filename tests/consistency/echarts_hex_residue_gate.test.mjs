import { test } from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const DIR_ECHARTS = path.join(ROOT, 'charts/echarts');

// GATE moi: dem hex tho con sot trong SVG tinh SAU khi hau xu ly (charts/echarts/
// hex-token.mjs). Khong dat trong gates/ (mot agent khac dang lam thu muc do), nen song
// o day nhu mot test consistency ep dung dinh nghia trong charts/echarts/hex-token.mjs.
//
// Luat repo: "gate khong tu do duoc voi fixture do cua chinh no thi gate do chua ton
// tai." Ca hai fixture duoi day deu XAY TU PALETTE that (theme.mjs), khong go hex tay,
// vi day chinh la tap dong ma bocMauChuDe()/demHexThoConLai() thao tac.
//
// Bay XML da ghi trong memory.md (var() boc vao hex NAM TRONG COMMENT XML lam hong ca
// file, vi "--" bi cam trong comment XML) KHONG ap dung o day: da kiem thuc nghiem tren
// toan bo 18 SVG do 18 preset ECharts sinh ra, khong file nao co chuoi "<!--" (ECharts
// SSR khong xuat XML comment). Vi vay hex-token.mjs khong can logic ne comment XML nhu
// ban di tru minh hoa SVG tung can.

test('demHexThoConLai/bocMauChuDe: fixture DO phai bi bat (hex tran, chua boc var())', async () => {
  const { PALETTE } = await import(path.join(DIR_ECHARTS, 'theme.mjs'));
  const { demHexThoConLai, bocMauChuDe } = await import(path.join(DIR_ECHARTS, 'hex-token.mjs'));

  const hex = PALETTE.accent; // lay tu PALETTE that, khong go hex tay trong test
  const svgDo = `<svg><rect fill="${hex}"/><path stroke="${hex}"/></svg>`;

  const soDo = demHexThoConLai(svgDo);
  assert.ok(soDo > 0, `fixture DO phai co it nhat 1 hex tran chua boc, nhung demHexThoConLai tra ve ${soDo} -- gate nay chua ton tai neu no khong do duoc voi fixture do cua chinh no`);
  assert.equal(soDo, 2, 'fixture do co dung 2 lan xuat hien hex tran (rect + path)');
});

test('demHexThoConLai/bocMauChuDe: fixture XANH phai PASS (da boc var(--token, #hex))', async () => {
  const { PALETTE } = await import(path.join(DIR_ECHARTS, 'theme.mjs'));
  const { demHexThoConLai, bocMauChuDe } = await import(path.join(DIR_ECHARTS, 'hex-token.mjs'));

  const hex = PALETTE.accent;
  const svgDo = `<svg><rect fill="${hex}"/><path stroke="${hex}"/></svg>`;
  const svgXanh = bocMauChuDe(svgDo);

  const soXanh = demHexThoConLai(svgXanh);
  assert.equal(soXanh, 0, `sau bocMauChuDe(), khong duoc con hex tran nao thuoc bang mau, nhung con ${soXanh}`);

  // du phong PHAI bang dung hex cu -- file .svg con duoc mo doc lap ngoai trang HTML co
  // khai bien CSS, thieu du phong la hinh mat sach mau.
  assert.match(svgXanh, new RegExp(`var\\(--accent, ${hex}\\)`), 'var() phai giu du phong dung bang hex cu');
});

test('bocMauChuDe khong lam gi voi hex KHONG thuoc bang mau (mau dan xuat/noi bo ECharts)', async () => {
  const { bocMauChuDe, demHexThoConLai } = await import(path.join(DIR_ECHARTS, 'hex-token.mjs'));
  // #3c3c41 la mot mau noi bo ECharts tu ve (thay trong out-01-waterfall.svg thuc te,
  // khong nam trong PALETTE), phai giu nguyen literal, KHONG bi boc var() va KHONG bi
  // gate nay dem la "tan du" vi no chua bao gio thuoc tap can boc.
  const svg = '<svg><rect fill="#3c3c41"/></svg>';
  const ra = bocMauChuDe(svg);
  assert.equal(ra, svg, 'hex ngoai bang mau phai giu nguyen literal, khong bi dong den');
  assert.equal(demHexThoConLai(ra), 0, 'gate chi dem hex THUOC bang mau, khong duoc bao dong gia voi mau ngoai bang mau');
});

test('bocMauChuDe khong long var() hai lan neu chay tren chinh dau ra cua no (idempotent)', async () => {
  const { PALETTE } = await import(path.join(DIR_ECHARTS, 'theme.mjs'));
  const { bocMauChuDe, demHexThoConLai } = await import(path.join(DIR_ECHARTS, 'hex-token.mjs'));

  const hex = PALETTE.ink;
  const svgDo = `<svg><text fill="${hex}">so lieu</text></svg>`;
  const lanMot = bocMauChuDe(svgDo);
  const lanHai = bocMauChuDe(lanMot);
  assert.equal(lanHai, lanMot, 'chay bocMauChuDe lan thu hai tren dau ra cua chinh no khong duoc doi gi them');
  assert.equal(demHexThoConLai(lanHai), 0);
  assert.doesNotMatch(lanHai, /var\(--ink, var\(--ink,/, 'khong duoc long var() hai lan');
});

test('gate chay THAT tren mot preset da qua renderStatic(): phai bang 0', async () => {
  const { renderStatic } = await import(path.join(DIR_ECHARTS, 'render-static.mjs'));
  const { demHexThoConLai } = await import(path.join(DIR_ECHARTS, 'hex-token.mjs'));
  const { option, MAC_DINH } = await import(path.join(DIR_ECHARTS, '01-waterfall.mjs'));

  const svg = renderStatic(option, MAC_DINH, { width: 700, height: 400 });
  assert.ok(svg.includes('var(--'), 'SVG that qua renderStatic() phai co it nhat 1 var(--token, ...)');
  assert.equal(demHexThoConLai(svg), 0, 'SVG that qua renderStatic() khong duoc con hex tho thuoc bang mau');
});
