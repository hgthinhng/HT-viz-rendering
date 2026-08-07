/**
 * loi_annotation.test.mjs, phep quy loi cho lop annotation phai phan biet duoc.
 *
 * Ban truoc quy loi bang mot phep quet chuoi con tren ca khoi stack:
 * `/\bannotate\b/i`. Vi dau gach noi va dau cham deu la ranh gioi tu, phep do coi
 * MOI loi phat sinh trong mot file ten kieu "annotate-demo.js" la loi cua lop
 * annotation. Repo cam quy nhan sai chu the loi, va mot bao cao chi sai cho thi con
 * ton thoi gian hon mot bao cao khong noi gi.
 *
 * Cac ca duoi day la ca THAT: chung la hinh dang stack ma Chromium sinh ra.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { phanLoaiLoi, fileTrongStack, laTaiNguyenAnnotation } from '../../scripts/lib/loi-annotation.mjs';

test('loi phat sinh TRONG annotate.js thi quy cho lop annotation', () => {
  const stack = [
    "TypeError: Cannot read properties of undefined (reading 'x')",
    '    at resolveCollisions (file:///home/x/illustrations/annotate.js:210:14)',
    '    at annotate (file:///home/x/illustrations/annotate.js:401:3)',
    '    at file:///home/x/illustrations/examples/vi-du.html:108:12',
  ].join('\n');
  const kq = phanLoaiLoi(stack);
  assert.equal(kq.lienQuan, true);
  assert.match(kq.lyDo, /annotate\.js/);
});

test('loi ReferenceError Annotate quy cho lop annotation du stack chi tro toi file HTML', () => {
  // Ca nay xay ra khi the <script src=annotate.js> khong nap duoc: loi phat sinh
  // ngay trong the <script> cua trang nen khong frame nao tro toi annotate.js.
  const stack = [
    'ReferenceError: Annotate is not defined',
    '    at file:///home/x/illustrations/examples/vi-du.html:108:3',
  ].join('\n');
  const kq = phanLoaiLoi(stack);
  assert.equal(kq.lienQuan, true);
  assert.match(kq.lyDo, /Annotate/);
});

test('loi trong mot file ten gan giong thi KHONG quy cho lop annotation', () => {
  // Day la ca ban cu quy oan: `\bannotate\b` khop "annotate-demo.js" vi dau gach
  // noi la ranh gioi tu.
  const stack = [
    "TypeError: Cannot read properties of undefined (reading 'y')",
    '    at ve (file:///home/x/demo/annotate-demo.js:12:5)',
    '    at file:///home/x/illustrations/examples/vi-du.html:40:1',
  ].join('\n');
  const kq = phanLoaiLoi(stack);
  assert.equal(kq.lienQuan, false, 'file khac ten thi khong duoc quy cho lop annotation');
  assert.match(kq.lyDo, /annotate-demo\.js/);
});

test('loi cua mot script hoan toan khac thi khong quy cho lop annotation', () => {
  const stack = [
    'TypeError: fetch failed',
    '    at doLuong (file:///home/x/illustrations/gen-vietnam-path.mjs:33:9)',
  ].join('\n');
  assert.equal(phanLoaiLoi(stack).lienQuan, false);
});

test('fileTrongStack tra ve basename cua moi frame', () => {
  const stack = '    at f (file:///a/b/annotate.js:1:1)\n    at g (/c/d/khac.mjs:2:2)';
  assert.deepEqual(fileTrongStack(stack), ['annotate.js', 'khac.mjs']);
});

test('laTaiNguyenAnnotation so basename chinh xac, khong dung chuoi con', () => {
  assert.equal(laTaiNguyenAnnotation('file:///x/annotate.js'), true);
  assert.equal(laTaiNguyenAnnotation('file:///x/annotate.css?v=2'), true);
  assert.equal(laTaiNguyenAnnotation('file:///x/annotated-source-badge.png'), false);
  assert.equal(laTaiNguyenAnnotation('file:///x/annotate-demo.js'), false);
});
