// preset_qua_schema.test.mjs, ep dung mot cau da nam trong CLAUDE.md tu lau:
// "Moi chart phai di qua lop schema dung chung".
//
// Cau do tung SAI ve thuc te. Dem ngay 09-08: chi 6 tren 18 preset goi `validateSeries`,
// muoi hai cai con lai nhan du lieu tho va khong co cach nao biet don vi cua chinh dai
// luong chung ve. Do la ly do GOC cua lop loi `5.640.000%`: preset khong duoc cho biet
// don vi thi no doan, va doan thi co luc doan sai.
//
// Mot luat khong ai kiem thi khong phai luat, no la mot cau van. Test nay bien cau van
// do thanh luat.
//
// Ba phep do, moi phep chan mot duong lach:
//   1. Quet ma nguon: preset co goi `validateSeries` khong.
//   2. Do HANH VI: bo `unit` khoi MAC_DINH thi `option()` PHAI nem loi. Phep do 1 mot
//      minh lach duoc bang cach import ham roi khong goi.
//   3. Bo `source` cung phai nem loi: don vi va nguon la hai rang buoc doc lap, va nguon
//      moi la thu cho phep mot con so tren hinh truy nguoc duoc.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PRESETS } from '../../charts/echarts/registry.mjs';

const GOC = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const THU_MUC = path.join(GOC, 'charts', 'echarts');

/** Preset khai meta o CAP HANG chu khong o cap series, kem ly do.
 *
 * `03-bullet` la N chi tieu doc lap xep canh nhau, va chung khong nhat thiet cung don vi:
 * ban demo co ba chi tieu tinh bang ty dong va mot tinh bang lan. Ep ca bon vao mot
 * `series.unit` la khai bao noi doi, vi chinh `validateSeries` da chot "khong tron don vi
 * trong mot series". No validate TUNG hang thay vi mot khoi series. */
const META_O_CAP_HANG = {
  '03-bullet': 'N chi tieu doc lap, moi hang mot don vi rieng',
};

/** Preset khai meta duoi khoa `meta` thay vi `series`, kem ly do.
 *
 * Ba preset nay dung `series` lam mot bien CUC BO ben trong `option()`: chung tu dung
 * `rows` tu du lieu tho roi ghep voi meta. Nen meta di vao qua khoa `meta`, con `series`
 * la thu chung dung ra. `15-quadrant-scatter` co HAI khoi meta vi hai truc do hai dai
 * luong khac nhau, va do khong pha luat "khong tron don vi trong mot series": day la hai
 * series rieng. */
const META_DUOI_KHOA_META = {
  '15-quadrant-scatter': ['pb', 'roe'],
  '16-dot-distribution': null,
  '18-sensitivity-grid': null,
};

/** Lay cac khoi meta cua mot preset, du no khai duoi khoa nao. */
function cacKhoiMeta(ten, macDinh) {
  if (ten in META_DUOI_KHOA_META) {
    const nhanh = META_DUOI_KHOA_META[ten];
    return nhanh ? nhanh.map((k) => macDinh.meta && macDinh.meta[k]) : [macDinh.meta];
  }
  return [macDinh.series];
}

/** Tra ve ban MAC_DINH da lam hong mot truong meta, du preset khai duoi khoa nao. */
function lamHongMeta(ten, macDinh, truong) {
  if (ten in META_DUOI_KHOA_META) {
    const nhanh = META_DUOI_KHOA_META[ten];
    if (!nhanh) return { ...macDinh, meta: { ...macDinh.meta, [truong]: undefined } };
    const meta = { ...macDinh.meta };
    for (const k of nhanh) meta[k] = { ...meta[k], [truong]: undefined };
    return { ...macDinh, meta };
  }
  return { ...macDinh, series: { ...macDinh.series, [truong]: undefined } };
}

test('moi preset ECharts deu goi validateSeries', () => {
  const thieu = [];
  for (const ten of Object.keys(PRESETS)) {
    const nguon = fs.readFileSync(path.join(THU_MUC, `${ten}.mjs`), 'utf8');
    if (!nguon.includes('validateSeries(')) thieu.push(ten);
  }
  assert.deepEqual(
    thieu,
    [],
    `preset sau chua di qua lop schema: ${thieu.join(', ')}. Them khoi \`series\` vao ` +
      'MAC_DINH va goi validateSeries(series) o dau option().',
  );
});

test('moi preset khai du unit va source trong MAC_DINH', () => {
  const thieu = [];
  for (const [ten, preset] of Object.entries(PRESETS)) {
    if (META_O_CAP_HANG[ten]) {
      const hang = preset.MAC_DINH.rows || [];
      const xau = hang.filter((r) => !r.unit || !r.source);
      if (xau.length) thieu.push(`${ten}: ${xau.length} hang thieu unit hoac source`);
      continue;
    }
    for (const s of cacKhoiMeta(ten, preset.MAC_DINH)) {
      if (!s) thieu.push(`${ten}: MAC_DINH khong co khoi meta`);
      else if (!s.unit) thieu.push(`${ten}: meta thieu unit`);
      else if (!s.source || !s.source.tier) thieu.push(`${ten}: meta thieu source.tier`);
    }
  }
  assert.deepEqual(thieu, [], thieu.join(' | '));
});

test('bo unit thi option() nem loi, do bang hanh vi chu khong doc ma nguon', () => {
  const imLang = [];
  for (const [ten, preset] of Object.entries(PRESETS)) {
    if (META_O_CAP_HANG[ten]) continue;
    const hong = lamHongMeta(ten, preset.MAC_DINH, 'unit');
    let nem = false;
    try {
      preset.option(hong);
    } catch {
      nem = true;
    }
    if (!nem) imLang.push(ten);
  }
  assert.deepEqual(
    imLang,
    [],
    `preset sau IM LANG khi thieu unit: ${imLang.join(', ')}. Chung co the dang import ` +
      'validateSeries ma khong goi, hoac goi nham doi tuong.',
  );
});

test('bo source thi option() cung nem loi', () => {
  const imLang = [];
  for (const [ten, preset] of Object.entries(PRESETS)) {
    if (META_O_CAP_HANG[ten]) continue;
    const hong = lamHongMeta(ten, preset.MAC_DINH, 'source');
    let nem = false;
    try {
      preset.option(hong);
    } catch {
      nem = true;
    }
    if (!nem) imLang.push(ten);
  }
  assert.deepEqual(imLang, [], `preset sau IM LANG khi thieu source: ${imLang.join(', ')}`);
});

/** Goi MOI ham dinh dang tim thay trong mot option, tra ve mang chuoi ket qua.
 *
 * Duyet de quy vi formatter nam rai rac: `axisLabel.formatter`, `label.formatter`,
 * `tooltip.formatter`, `valueFormatter`. Muc dich la co mot DAU VAN TAY cua cach preset
 * hien thi so, de so hai dau van tay ung voi hai don vi khac nhau. */
function dauVanTay(opt) {
  const ra = [];
  const daTham = new Set();
  const duyet = (nut) => {
    if (!nut || typeof nut !== 'object' || daTham.has(nut)) return;
    daTham.add(nut);
    for (const [khoa, gt] of Object.entries(nut)) {
      if (typeof gt === 'function' && /formatter/i.test(khoa)) {
        for (const mau of [1200000, 42.5]) {
          try {
            ra.push(String(gt(mau)));
          } catch {
            try {
              ra.push(String(gt({ value: mau, data: [0, 0, mau], dataIndex: 0 })));
            } catch {
              /* formatter doi hinh dang khac, bo qua: cac formatter con lai van du lam dau van tay */
            }
          }
        }
      } else if (typeof gt === 'object') {
        duyet(gt);
      }
    }
  };
  duyet(opt);

  // Nhan ve bang `graphic` trong `_veSauLayout` KHONG nam trong bat ky formatter nao, nen
  // duyet cay option mot minh se bo sot chung. Bo sot o day khong vo hai: `05-slope` ve
  // toan bo nhan hai dau bang graphic, nen thieu buoc nay thi dau van tay cua no rong va
  // phep do ket luan nham la no khong phan ung voi don vi.
  //
  // `_veSauLayout` chi dung ba thu cua chart instance, nen mot chart GIA la du. Tra ve toa
  // do tuyen tinh chu khong tra so ngau nhien: dau van tay phai tat dinh.
  if (typeof opt._veSauLayout === 'function') {
    const chartGia = {
      getWidth: () => 700,
      getHeight: () => 400,
      convertToPixel: (_, [x, y]) => [100 + Number(x) * 3, 300 - Number(y) * 3],
      getOption: () => ({}),
    };
    try {
      const gr = opt._veSauLayout(chartGia) || [];
      for (const g of [gr].flat(3)) {
        if (g && g.style && typeof g.style.text === 'string') ra.push(g.style.text);
      }
    } catch {
      /* preset can nhieu hon mot chart gia; cac formatter o tren van la dau van tay */
    }
  }
  return ra;
}

test('preset dong cung don vi phai TU CHOI don vi khac, do bang hanh vi', () => {
  // Phep do nay tung SAI, va cach no sai dang ghi lai vi no la mot bay chung:
  //
  // Ban dau no bo qua preset nao KHONG chua chuoi `epDonVi(` trong ma nguon, voi ly le
  // "preset do nhan don vi tu do". Tuc test TU MIEN TRU dung cai no can kiem: go
  // `epDonVi` khoi mot preset la no ngung kiem preset do, va mutation xac nhan dieu do
  // (go epDonVi khoi 09-candlestick thi test van xanh).
  //
  // Ban nay khong doc ma nguon nua. Voi moi preset, doi don vi sang mot don vi khac han
  // roi hoi: hoac no NEM LOI (da khai epDonVi, that tha), hoac cach hien thi so PHAI doi
  // theo (don vi tu do that). Neu khong nem loi ma cach hien thi y nguyen thi khai bao la
  // noi doi, va do la thu duy nhat bi tinh la sai.
  const noiDoi = [];
  for (const [ten, preset] of Object.entries(PRESETS)) {
    if (META_O_CAP_HANG[ten]) continue;
    const goc = dauVanTay(preset.option(preset.MAC_DINH));
    const doi = ten in META_DUOI_KHOA_META
      ? { ...preset.MAC_DINH, meta: doiUnitTrongMeta(preset.MAC_DINH.meta, META_DUOI_KHOA_META[ten], 'usd_oz') }
      : { ...preset.MAC_DINH, series: { ...preset.MAC_DINH.series, unit: 'usd_oz' } };
    let sau = null;
    try {
      sau = dauVanTay(preset.option(doi));
    } catch {
      continue; // nem loi la hanh vi DUNG cua preset dong cung don vi
    }
    if (JSON.stringify(goc) === JSON.stringify(sau)) {
      noiDoi.push(`${ten}: nhan unit=usd_oz ma cach hien thi so khong doi mot chut nao`);
    }
  }
  assert.deepEqual(
    noiDoi,
    [],
    `${noiDoi.join(' | ')}. Preset dong cung don vi phai goi epDonVi(series, [...]) de tu ` +
      'choi thang, thay vi nhan roi ve ra mot nhan sai su that.',
  );
});

/** Doi `unit` trong mot khoi meta, du no phang hay chia nhanh theo truc. */
function doiUnitTrongMeta(meta, nhanh, unit) {
  if (!nhanh) return { ...meta, unit };
  const ra = { ...meta };
  for (const k of nhanh) ra[k] = { ...ra[k], unit };
  return ra;
}

