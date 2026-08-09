// skill_khong_lac_hau.test.mjs, chan mot benh da xay ra that va song rat lau.
//
// `SKILL.md` la cua vao cua ca repo, va no tung noi SAI ve chinh repo suot hai phase:
// ghi "108 tai san" khi thuc te 116, ghi "muoi gate" khi da co them chin gate lan song,
// tro toi mot thu muc vi du duy nhat trong khi da co hai, va hen "bay file doctrine se
// toi o Phase 3" trong khi Phase 3 da qua tu lau.
//
// Khong phep do nao bat duoc, vi tai lieu khong chay. Ba phep do duoi day bien nhung
// khang dinh KIEM DUOC trong SKILL.md thanh thu co the do:
//   1. Moi duong dan SKILL.md tro toi phai ton tai that.
//   2. Con so tai san phai khop `catalog/CATALOG.md`, thu von sinh tu ma nguon.
//   3. Khong con loi hen ve mot phase da qua.
//
// Nhung khang dinh KHONG kiem duoc (doctrine, cach quyet dinh) thi khong gate nao thay
// nguoi doc duoc, va test nay khong gia vo lam duoc dieu do.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const SKILL = fs.readFileSync(path.join(GOC, 'SKILL.md'), 'utf8');

test('moi duong dan SKILL.md tro toi deu ton tai', () => {
  // Bat duong dan trong backtick, dang `thu-muc/file.ext` hoac `thu-muc/`.
  const ma = [...SKILL.matchAll(/`([a-z0-9][\w./-]*\/[\w./-]*)`/gi)].map((m) => m[1]);
  const boQua = (d) =>
    d.startsWith('<') || // chuoi thay the trong vi du lenh
    d.includes('*') ||
    d.startsWith('@media') ||
    /^(node|npm|python3)\b/.test(d);
  const thieu = [...new Set(ma)]
    .filter((d) => !boQua(d))
    .filter((d) => !fs.existsSync(path.join(GOC, d.replace(/\/$/, ''))));
  assert.deepEqual(
    thieu,
    [],
    `SKILL.md tro toi duong dan khong ton tai: ${thieu.join(', ')}. Tai lieu la cua vao ` +
      'cua repo, tro sai la dan nguoi doc vao ngo cut.',
  );

  // Chong REGEX HONG, giu lai tu ban cu trong tests/smoke/entrypoint.test.mjs. Ban dau
  // tien cua phep do nay mo bang [a-z] nen bo qua moi duong dan bat dau bang chu hoa,
  // tuc bo qua dung hai file quan trong nhat ma SKILL.md tro toi. Gate xanh suot mot
  // phase ma chua tung cham vao chung. Doi chieu voi hai ten cu the la cach re nhat de
  // biet regex con bat duoc gi.
  const batDuoc = [...SKILL.matchAll(/`([A-Za-z][\w./-]+\.(?:md|css|py|mjs|js|json|html))`/g)].map(
    (m) => m[1],
  );
  for (const phai of ['CLAUDE.md', 'catalog/CATALOG.md']) {
    assert.ok(
      batDuoc.includes(phai),
      `regex khong bat duoc "${phai}" du SKILL.md co tro toi. Bat duoc: ${batDuoc.join(', ')}`,
    );
  }
});

test('so tai san trong SKILL.md khop muc luc sinh tu ma nguon', () => {
  const cat = fs.readFileSync(path.join(GOC, 'catalog', 'CATALOG.md'), 'utf8');
  const m = cat.match(
    /Tổng (\d+) tài sản: (\d+) chart-echarts, (\d+) chart-matplotlib, (\d+) component, (\d+) minh-hoa/,
  );
  assert.ok(m, 'khong doc duoc dong tong ket trong catalog/CATALOG.md');
  const [, tong, echarts, mpl, comp, minhHoa] = m;

  const lech = [];
  if (!SKILL.includes(`${tong} tài sản`)) lech.push(`tong: catalog noi ${tong}`);
  if (!SKILL.includes(`${echarts} chart ECharts`)) lech.push(`chart ECharts: catalog noi ${echarts}`);
  if (!SKILL.includes(`${mpl} component matplotlib`)) lech.push(`matplotlib: catalog noi ${mpl}`);
  if (!SKILL.includes(`${comp} component kể chuyện`)) lech.push(`component: catalog noi ${comp}`);
  if (!SKILL.includes(`${minhHoa} minh hoạ ngành`)) lech.push(`minh hoa: catalog noi ${minhHoa}`);

  assert.deepEqual(
    lech,
    [],
    `SKILL.md lech so voi muc luc: ${lech.join(' | ')}. Muc luc sinh tu ma nguon nen no ` +
      'dung; sua SKILL.md cho khop, dung sua nguoc lai.',
  );
});

test('SKILL.md khong con hen ve mot phase da qua', () => {
  const hen = [];
  // "se toi o Phase N" la mot loi hen, va loi hen trong tai lieu cua vao thi khong ai
  // quay lai kiem. Bat moi bien the.
  for (const mau of [/sẽ tới ở Phase/i, /Chưa có ở Phase/i, /sẽ có ở Phase/i, /Phase \d+ sẽ/i]) {
    const m = SKILL.match(mau);
    if (m) hen.push(m[0]);
  }
  assert.deepEqual(
    hen,
    [],
    `SKILL.md con loi hen ve phase: ${hen.join(', ')}. Hoac lam roi thi sua tai lieu, hoac ` +
      'chua lam thi noi thang la CHUA CO va khong hen moc.',
  );
});
