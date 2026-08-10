/**
 * phong_cach_build.test.mjs, build_html.py phai doc phong-cach bat buoc tu front-matter.
 *
 * Goi qua `python3 -c` voi sys.path.insert thay vi import truc tiep tu Node: build_html.py
 * chi dung thu vien chuan (argparse, html, json, re, xml.parsers.expat), nen sys.path.insert
 * chay dung khong can doi sang PYTHONPATH env, da kiem truc tiep truoc khi viet file nay.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

test('build dung khi front-matter thieu khoa phong-cach, thong bao co huong dan', () => {
  const kq = spawnSync('python3', [
    '-c',
    [
      'import sys; sys.path.insert(0, "pipeline")',
      'import build_html as b',
      'meta, than = b.tach_front_matter(open("tests/fixtures/phong-cach/bao-cao-thieu-khoa/noi-dung.md").read())',
      'b.doc_phong_cach(meta)',
    ].join('\n'),
  ], { cwd: REPO, encoding: 'utf8' });
  assert.notEqual(kq.status, 0);
  assert.ok(kq.stderr.includes('nghi-thuc-huong'), kq.stderr);
});

test('doc_phong_cach tra ve config thep-xanh khi khoa hop le', () => {
  const kq = spawnSync('python3', [
    '-c',
    [
      'import sys; sys.path.insert(0, "pipeline")',
      'import build_html as b',
      'pc = b.doc_phong_cach({"phong-cach": "thep-xanh"})',
      'print(pc["chu_de_mac_dinh"], b.data_theme_cua(pc))',
    ].join('\n'),
  ], { cwd: REPO, encoding: 'utf8' });
  assert.equal(kq.status, 0, kq.stderr);
  assert.equal(kq.stdout.trim(), 'sang-lanh light');
});

// Fixture tests/fixtures/phong-cach/bao-cao-vi-pham-loai-hinh/ khai `phong-cach: thep-xanh`
// TAM vi thep-xanh khong khai gioi_han_loai_hinh nen chan chua bat duoc that. Doi sang
// style thuc su cam matplotlib (nhung-toi, chu de mac dinh toi) khi Task 10 dung style do,
// roi go skip nay va them assert orchestrator exit != 0 kem thong diep "cam matplotlib".
test.skip('orchestrator DUNG khi phong-cach cam matplotlib nhung hinh/ con script .py (cho den Task 10)', () => {
  assert.fail('chua co style chinh thuc cam matplotlib de kiem, xem ghi chu o tren');
});
