/**
 * catalog_khop_nguon.test.mjs, muc luc thu vien phai khop ma nguon.
 *
 * `catalog/CATALOG.md` va `catalog/INDEX.json` la thu Claude doc o phien sau de biet thu
 * vien co gi. Mot muc luc troi khoi ma nguon con te hon khong co muc luc: no van doc tron
 * tru, van dung dinh dang, va no dan sai duong. Ba rang buoc duoi day giu no khop:
 *
 *   1. Chay lai bo sinh phai ra dung noi dung dang nam tren dia.
 *   2. Moi tai san tren dia deu co trong muc luc, khong sot cai nao.
 *   3. Khong muc nao thieu mo ta. Day la rang buoc ve NOI DUNG chu khong ve dinh dang:
 *      mot muc luc du 108 dong ma mot nua ghi "CHUA CO MO TA" thi khong tra loi duoc
 *      cau hoi ma no sinh ra de tra loi.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const doc = (p) => JSON.parse(readFileSync(path.join(GOC, p), 'utf-8'));

test('muc luc khop ma nguon, chay lai bo sinh khong ra khac', () => {
  // `--kiem` khong ghi de, chi so sanh. Exit khac 0 nghia la da troi.
  execFileSync('python3', [path.join(GOC, 'scripts/sinh_catalog.py'), '--kiem'], {
    cwd: GOC, stdio: 'pipe',
  });
});

test('moi tai san tren dia deu co trong muc luc', () => {
  const ml = doc('catalog/INDEX.json');
  const co = new Map();
  for (const m of ml.muc) {
    if (!co.has(m.nhom)) co.set(m.nhom, new Set());
    co.get(m.nhom).add(m.ma);
  }

  const tren_dia = {
    'chart-echarts': readdirSync(path.join(GOC, 'charts/echarts'))
      .filter((f) => /^\d\d-.*\.mjs$/.test(f)).map((f) => f.replace('.mjs', '')),
    component: readdirSync(path.join(GOC, 'components/catalog'))
      .filter((f) => f.endsWith('.md')).map((f) => f.replace('.md', '')),
    'minh-hoa': readdirSync(path.join(GOC, 'illustrations/svg'))
      .filter((f) => f.endsWith('.svg')).map((f) => f.replace('.svg', '')),
  };

  for (const [nhom, ds] of Object.entries(tren_dia)) {
    assert.ok(ds.length > 0, `khong quet duoc tai san nao cho nhom ${nhom}, phep do rong`);
    const thieu = ds.filter((x) => !co.get(nhom)?.has(x));
    assert.deepEqual(thieu, [], `nhom ${nhom} co tai san khong nam trong muc luc: ${thieu}`);
  }
});

test('so component matplotlib trong muc luc khop so ham c_ trong ma nguon', () => {
  const ml = doc('catalog/INDEX.json');
  const trong_muc_luc = ml.muc.filter((m) => m.nhom === 'chart-matplotlib').length;
  const dem = execFileSync('python3', ['-c', `
import ast, pathlib
so = 0
for f in pathlib.Path('charts/matplotlib').glob('viz_eir*.py'):
    for n in ast.walk(ast.parse(f.read_text(encoding='utf-8'))):
        if isinstance(n, ast.FunctionDef) and n.name.startswith('c_'):
            so += 1
print(so)
`], { cwd: GOC, encoding: 'utf-8' }).trim();
  assert.equal(trong_muc_luc, Number(dem));
});

test('KHONG muc nao thieu mo ta', () => {
  const ml = doc('catalog/INDEX.json');
  assert.deepEqual(
    ml.thieu_mo_ta, [],
    'cac tai san sau chua co mo ta. Viet o NGUON (docstring, comment dau file, muc ' +
      '"Mo ta / khi nao dung", hoac <desc> cua SVG) roi chay lai scripts/sinh_catalog.py:\n  ' +
      ml.thieu_mo_ta.join(', ')
  );
});

test('moi duong dan xem truoc trong muc luc deu tro toi file co that', () => {
  // Mot muc luc tro toi file khong ton tai se lam contact sheet hien o trong, va o
  // trong bi doc thanh "hinh nay hong".
  const ml = doc('catalog/INDEX.json');
  const hong = ml.muc
    .filter((m) => m.xem_truoc && m.xem_truoc.endsWith('.svg'))
    .filter((m) => !existsSync(path.join(GOC, m.xem_truoc)))
    .map((m) => `${m.ma} -> ${m.xem_truoc}`);
  assert.deepEqual(hong, [], `xem truoc tro toi file khong co: ${hong.join(', ')}`);
});

test('muc luc va contact sheet deu nam trong git, khong phai artifact bi bo quen', () => {
  const trong_git = execFileSync('git', ['ls-files', 'catalog'], { cwd: GOC, encoding: 'utf-8' })
    .split('\n').filter(Boolean);
  for (const f of ['catalog/INDEX.json', 'catalog/CATALOG.md']) {
    assert.ok(trong_git.includes(f), `${f} chua duoc commit, phien sau se khong thay muc luc`);
  }
});
