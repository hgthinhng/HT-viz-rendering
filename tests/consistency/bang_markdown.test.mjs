/**
 * bang_markdown.test.mjs, bo dung bang cua build_html.py phai giu dung SO COT.
 *
 * Bang so lieu sai so cot la loi kho thay nhat trong ban in: trinh duyet va WeasyPrint
 * deu tu vá cho bang can doi, nen mot hang thieu mot o van hien ra "binh thuong", chi
 * la mot cot bi truot sang o ben canh. Nguoi doc thay so nam duoi sai tieu de cot ma
 * khong co dau hieu nao bao la co loi.
 *
 * Da dinh that khi lam o gop: `strip("|")` cua Python bo NHIEU pipe lien tiep o hai dau,
 * nen hang "| a ||| b ||" mat o rong cuoi va ra 4 cot trong khi tieu de co 5.
 */
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

const SO_NGUON = {
  version: '1.0',
  generated_date: '2026-08-07',
  sources: [
    { id: 'K1', org: 'Số minh hoạ', tier: 'T5_derived', sensitivity: 'public',
      published_date: '2026-08-01', cite: 'Số minh hoạ cho test' },
  ],
  values: [
    { id: 'v1', display: '9,8%', value: 9.8, unit: '%', period: '2025',
      source_id: 'K1', retrieved_date: '2026-08-01', tier: 'T5_derived', chart_id: 'c1' },
  ],
};

function dung(thanMd) {
  const tam = fs.mkdtempSync(path.join(os.tmpdir(), 'htviz-bang-'));
  fs.writeFileSync(path.join(tam, 'so-nguon.json'), JSON.stringify(SO_NGUON), 'utf-8');
  const md = `---\ntieu_de: Test bảng\nphong-cach: thep-xanh\nso_nguon: so-nguon.json\n---\n\n## Mục\n\n${thanMd}\n`;
  fs.writeFileSync(path.join(tam, 'noi-dung.md'), md, 'utf-8');
  const ra = path.join(tam, 'ra.html');
  execFileSync('python3', [path.join(GOC, 'pipeline/build_html.py'), path.join(tam, 'noi-dung.md'), ra], {
    cwd: GOC, stdio: 'pipe',
  });
  const html = fs.readFileSync(ra, 'utf-8');
  fs.rmSync(tam, { recursive: true, force: true });
  return html;
}

/** Tong so cot cua mot hang, cong ca colspan. */
function soCot(hangHtml) {
  return [...hangHtml.matchAll(/<t[hd][^>]*>/g)].reduce((tong, m) => {
    const sp = m[0].match(/colspan="(\d+)"/);
    return tong + (sp ? Number(sp[1]) : 1);
  }, 0);
}

test('bang phang giu dung so cot va danh dau cot so', () => {
  const html = dung(['| A | B | C |', '|---|---:|---|', '| x | 1 | y |'].join('\n'));
  const hang = html.match(/<tr>[\s\S]*?<\/tr>/g);
  assert.equal(soCot(hang[0]), 3);
  assert.equal(soCot(hang[1]), 3);
  assert.match(hang[0], /<th scope="col" class="num">B<\/th>/, 'cot can phai phai la cot so');
});

test('o gop giu dung TONG so cot, ke ca khi hang ket thuc bang o rong', () => {
  const html = dung(
    ['| A | B | C | D |', '|---|---:|---:|---|', '| gop ba o ||| d |', '| gop hai o cuoi | 1 ||| '].join('\n')
  );
  const hang = html.match(/<tr>[\s\S]*?<\/tr>/g);
  for (const [i, h] of hang.entries()) {
    assert.equal(soCot(h), 4, `hang ${i} phai co du 4 cot, dang co ${soCot(h)}`);
  }
  assert.match(hang[1], /colspan="3"/);
});

test('dong "Bang:" truoc bang tro thanh caption, ke ca khi cach mot dong trong', () => {
  const html = dung(['Bảng: Chú thích của bảng.', '', '| A | B |', '|---|---|', '| x | y |'].join('\n'));
  assert.match(html, /<caption>Chú thích của bảng\.<\/caption>/);
  assert.ok(!/<p>Bảng: /.test(html), 'dong caption khong duoc con lai duoi dang doan van');
});

test('dong "Bang:" KHONG dung truoc bang thi van la doan van binh thuong', () => {
  // Quy uoc khong duoc am tham nuot mat mot doan chi vi no mo dau bang chu "Bang:".
  const html = dung('Bảng: câu này không đứng trước bảng nào cả.');
  assert.match(html, /<p>Bảng: câu này không đứng trước bảng nào cả\.<\/p>/);
  assert.ok(!/<caption>/.test(html));
});

test('so trong bang van tra ve so nguon duoc', () => {
  const html = dung(['| A | B |', '|---|---:|', '| Toàn ngành | {{v1}} |'].join('\n'));
  assert.match(html, /data-evid="v1"/);
});
