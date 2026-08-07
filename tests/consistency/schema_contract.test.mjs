// Phia Node cua hop dong schema. Ban Python doi xung o
// tests/consistency/schema_contract_test.py, CHAY CUNG MOT FILE FIXTURE.
//
// Y do: phan lon thu troi dat giua hai ban schema la tu vung va luat ngu nghia. Tu
// vung da tach ra charts/schema.vocab.json nen ca hai cung doc. Luat ngu nghia van
// phai viet tay hai lan, va cach chong troi duy nhat that su hieu qua la bat ca hai
// chay cung mot bo ca, moi ca ghi ro phai pass hay fail va fail voi ma nao.
//
// Doi chieu bang MA LOI chu khong bang cau chu tieng Viet: sua loi nhan cho de hieu
// hon la viec tot, va no khong duoc lam do test o phia ben kia.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import {
  validateSeries,
  validateRow,
  validatePeriod,
  SCHEMA_VERSION,
  VOCAB,
  soThapPhan,
  cachVe,
  coCo,
  ERR,
} from '../../charts/echarts/schema.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const FIXTURE = JSON.parse(
  readFileSync(path.join(ROOT, 'charts/fixtures/schema-cases.json'), 'utf8'),
);

const CHAY = {
  series: (d) => validateSeries(d),
  row: (d) => validateRow(d, 0),
  period: (d) => validatePeriod(d),
};

test('moi ca trong fixture vang cho dung ket qua mong doi', () => {
  const hong = [];
  for (const ca of FIXTURE.cases) {
    const chay = CHAY[ca.loai];
    assert.ok(chay, `ca "${ca.ten}" co loai "${ca.loai}" khong ai xu ly`);
    if (ca.mong_doi === 'pass') {
      try {
        chay(ca.du_lieu);
      } catch (e) {
        hong.push(`"${ca.ten}": mong doi PASS nhung nem ${e.ma || e.message}`);
      }
    } else {
      let daNem = null;
      try {
        chay(ca.du_lieu);
      } catch (e) {
        daNem = e.ma;
      }
      if (daNem === null) hong.push(`"${ca.ten}": mong doi FAIL voi ${ca.ma_loi} nhung PASS`);
      else if (daNem !== ca.ma_loi) hong.push(`"${ca.ten}": mong doi ${ca.ma_loi} nhung nem ${daNem}`);
    }
  }
  assert.deepEqual(hong, [], `${hong.length} ca lech hop dong:\n${hong.join('\n')}`);
});

test('bo ca phu het cac ma loi da khai, khong de ma nao khong duoc kiem', () => {
  const maDuocKiem = new Set(FIXTURE.cases.filter((c) => c.ma_loi).map((c) => c.ma_loi));
  // Hai ma duoi day khong den tu du lieu dau vao ma tu loi lap trinh trong preset, nen
  // khong co ca fixture: VALUE_SAI_KIEU la ma du phong, CHI_SO_NGOAI_PHAM_VI do coCo()
  // nem khi preset truyen chi so sai.
  const MIEN_TRU = new Set(['VALUE_SAI_KIEU', 'CHI_SO_NGOAI_PHAM_VI']);
  const thieu = Object.values(ERR).filter((m) => !maDuocKiem.has(m) && !MIEN_TRU.has(m));
  assert.deepEqual(
    thieu,
    [],
    `cac ma loi sau chua co ca fixture nao kiem: ${thieu.join(', ')}. Them ca vao charts/fixtures/schema-cases.json`,
  );
});

test('so chu so thap phan lay tu tu vung khi series khong khai', () => {
  assert.equal(soThapPhan({ unit: 'ty_dong' }), 0);
  assert.equal(soThapPhan({ unit: 'phan_tram' }), 1);
  assert.equal(soThapPhan({ unit: 'phan_tram', decimals: 2 }), 2, 'khai tuong minh phai thang tu vung');
});

test('cach ve phan biet du ba loai gia tri thieu', () => {
  const chuaCongBo = cachVe('chua_cong_bo');
  const khongTonTai = cachVe('khong_ton_tai');
  const daLoai = cachVe('loai_bat_thuong');
  // Ca ba deu khong ve diem, nhung phai KHAC NHAU o dau hieu tren truc, neu khong thi
  // gop chung lam mot con hon la giu ba ten goi tao cam giac phan biet ma khong phan biet.
  const dauHieu = [chuaCongBo, khongTonTai, daLoai].map((c) => c.danh_dau_truc);
  assert.equal(new Set(dauHieu).size, 3, `ba trang thai thieu phai co ba dau hieu khac nhau, dang la ${JSON.stringify(dauHieu)}`);
  assert.equal(cachVe('co_that').noi_duong, true);
});

test('co tinh tu chi so nguyen, khong so sanh so thuc', () => {
  const laBase = coCo(2, 5);
  assert.equal(laBase(2), true);
  assert.equal(laBase(3), false);
  assert.throws(() => coCo(5, 5), /CHI_SO_NGOAI_PHAM_VI/, 'chi so bang do dai mang phai bi chan');
  assert.throws(() => coCo(1.5, 5), /CHI_SO_NGOAI_PHAM_VI/, 'chi so thuc phai bi chan');
});

test('tu vung va phien ban doc duoc tu file dung chung', () => {
  assert.match(SCHEMA_VERSION, /^\d+\.\d+\.\d+$/);
  assert.ok(Object.keys(VOCAB.unit).length >= 8, 'tu vung don vi qua ngheo');
  for (const [ten, mo] of Object.entries(VOCAB.unit)) {
    assert.ok(Number.isInteger(mo.decimals), `don vi ${ten} thieu decimals mac dinh`);
    assert.ok(mo.nhan && mo.nhan.length > 0, `don vi ${ten} thieu nhan hien thi`);
  }
});
