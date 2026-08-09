// chart_dinh_dang.test.mjs, chan mot lop loi SAI SU THAT chu khong phai loi xau.
//
// `14-bar-ranking` tung dong cung `fmtPercent` o nam cho, nen mot luot xep hang tinh
// bang TEU ra nhan `5.640.000%` tren mot an pham that. Chart van chay, SVG van hop le
// XML, moi gate cu van xanh, va con so tren giay thi sai. Khong test don vi nao cua repo
// bat duoc, chi mot ban bao cao that moi lo ra.
//
// Hai phep do, va chung bat hai thu khac nhau:
//   1. Quet ma nguon: preset khong duoc dong cung `fmtPercent` tru danh sach mien tru
//      CO LY DO ghi ngay trong file nay.
//   2. Do HANH VI: goi `option()` that voi mot don vi khong phai phan tram roi doc nhan
//      truc. Phep do 1 mot minh la du de lach, chi can doi ten ham.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PRESETS } from '../../charts/echarts/registry.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const THU_MUC = path.join(GOC, 'charts', 'echarts');

/** Preset ma phan tram la BAN CHAT chu khong phai mot lua chon don vi.
 *
 * Danh sach nay khong phai cho mien tru cho tien. Moi dong phai tra loi duoc cau hoi:
 * dai luong ma preset nay ve co the la thu gi khac ngoai phan tram khong? Neu co thi no
 * khong thuoc ve day. */
const PHAN_TRAM_LA_BAN_CHAT = {
  '11-stacked-100': 'ty trong cua mot co cau, LUON cong bang 100%, do la dinh nghia cua preset',
  '15-quadrant-scatter': 'truc tung la ROE, truc hoanh la P/B dung fmtMultiple; ca hai truc co don vi CO DINH theo dinh nghia preset',
  '18-sensitivity-grid': 'hai truc la WACC va tang truong dai han, deu la phan tram theo dinh nghia; gia tri O luoi thi dung don vi rieng',
  '23-waffle': 'mot o la mot phan tram, tong dung 100 o; preset nay khong ve duoc dai luong nao khac',
};

test('preset khong dong cung fmtPercent, tru nhung preset phan tram la ban chat', () => {
  const pham = [];
  for (const ten of Object.keys(PRESETS)) {
    if (PHAN_TRAM_LA_BAN_CHAT[ten]) continue;
    const nguon = fs.readFileSync(path.join(THU_MUC, `${ten}.mjs`), 'utf8');
    // Bo dong comment truoc khi quet: mot file duoc phep NHAC den fmtPercent trong ghi chu.
    const ma = nguon
      .split('\n')
      .filter((d) => !d.trim().startsWith('//') && !d.trim().startsWith('*'))
      .join('\n');
    if (ma.includes('fmtPercent(')) pham.push(ten);
  }
  assert.deepEqual(
    pham,
    [],
    'preset sau dong cung fmtPercent nhung khong phai preset phan tram: ' +
      `${pham.join(', ')}. Dung dinhDangTheoDonVi(donVi) trong fmt.mjs, hoac neu phan tram ` +
      'that su la ban chat cua preset thi them vao PHAN_TRAM_LA_BAN_CHAT kem ly do.',
  );
});

/** Dat don vi cho MOT preset, theo dung duong ma preset do doc don vi.
 *
 * Hai duong ton tai song song, va do la mot NO chu khong phai thiet ke: chi 6 tren 18
 * preset goi `validateSeries()` nen chi 6 cai do co `series.unit`. Muoi hai cai con lai
 * nhan du lieu tho va phai nhan don vi qua `params.donVi`. CLAUDE.md viet "moi chart phai
 * di qua lop schema dung chung", cau do dung ve y dinh nhung sai ve thuc te.
 */
function datDonVi(macDinh, unit) {
  if (macDinh && macDinh.series && macDinh.series.unit) {
    return { ...macDinh, series: { ...macDinh.series, unit } };
  }
  return { ...macDinh, donVi: unit };
}

test('doi don vi thi nhan truc doi theo, do bang gia tri that chu khong doc ma nguon', () => {
  const hong = [];
  for (const [ten, preset] of Object.entries(PRESETS)) {
    if (PHAN_TRAM_LA_BAN_CHAT[ten]) continue;
    let opt;
    try {
      opt = preset.option(datDonVi(preset.MAC_DINH, 'teu'));
    } catch {
      continue; // preset khong nhan don vi theo duong nao, phep do 1 da lo phan con lai
    }
    const truc = [opt.xAxis, opt.yAxis].flat().filter(Boolean);
    for (const t of truc) {
      const f = t && t.axisLabel && t.axisLabel.formatter;
      if (typeof f !== 'function') continue;
      const ra = String(f(1200000));
      if (ra.includes('%')) hong.push(`${ten}: nhan truc ra "${ra}" du don vi la teu`);
    }
  }
  assert.deepEqual(hong, [], hong.join(' | '));
});

test('dinhDangTheoDonVi tra dung ham cho tung ma don vi trong tu vung', async () => {
  const { dinhDangTheoDonVi } = await import('../../charts/echarts/fmt.mjs');
  assert.equal(dinhDangTheoDonVi('phan_tram')(18.2, { decimals: 1 }), '18,2%');
  assert.equal(dinhDangTheoDonVi('lan')(1.5, { decimals: 1 }), '1,5x');
  assert.equal(dinhDangTheoDonVi('teu')(5640000, { decimals: 0 }), '5.640.000');
  assert.equal(dinhDangTheoDonVi('ty_dong')(1180, { decimals: 0 }), '1.180');
  // Khong truyen gi thi ve phan tram, de moi loi goi cu giu nguyen dien mao.
  assert.equal(dinhDangTheoDonVi(undefined)(18.2, { decimals: 1 }), '18,2%');
});
