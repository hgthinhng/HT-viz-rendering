/**
 * schema.mjs - Lop schema du lieu dung chung cho MOI chart cua repo.
 *
 * VI SAO CO FILE NAY: sap them 6 preset ECharts, 5 component HTML va 3 chart duong
 * cong. Neu moi preset tu dinh nghia don vi, ky bao cao, gia tri thieu va nguon thi
 * them N chart la them N cho de ban HTML lech ban PDF. Da co tien le trong repo: font
 * lech, mau lech, va gan nhat la 12 chart xuat SVG khong hop le XML lam ban PDF mat
 * sach chart ma khong ai biet suot ca mot phase.
 *
 * BAN NAY LA KET QUA PHAN BIEN cua ba mo hinh ngoai tren cung mot cau hoi. Nhung cho
 * ban nhap ban dau bi bac, ghi lai de nguoi sau khong khoi phuc lai:
 *
 *  - Ban nhap bat entity.code phai VIET HOA KHONG DAU. Bi bac 2 tren 3 voi ly le manh:
 *    ma chung khoan thi dep, nhung phan khuc kinh doanh va ten chinh sach khong co ma
 *    tu nhien, va ep "Ban le" thanh "BAN LE" tren truc trong cau tha va bat nguoi doc
 *    dich nguoc. Cao dau la thu thuat HIEN THI khi truc thieu cho, khong phai dac tinh
 *    cua du lieu. Ban nay chi doi code NGAN, giu nguyen dau tieng Viet.
 *  - Ban nhap dat unit va source o TUNG HANG. Bi bac 2 tren 3: chinh ham validate
 *    "khong tron don vi" da to giac rang don vi la thuoc tinh cua LUOT XEP HANG chu
 *    khong phai cua hang. Ban nay dua unit, source, decimals, direction, kind len cap
 *    SERIES.
 *  - De xuat them truong display_value (chuoi da dinh dang san) bi BAC, du ly le chong
 *    lech HTML va PDF la dung. Ly do bac: no tuoc quyen dinh dang cua engine va nhan
 *    doi du lieu. Thay bang decimals o cap series cong bo fixture vang ep hai phia
 *    dinh dang giong nhau, dat cung muc tieu ma khong phinh du lieu.
 *
 * File tu vung: charts/schema.vocab.json, CA HAI ngon ngu doc chung.
 * Ban Python tuong duong: charts/matplotlib/schema.py, phai giu CUNG TEN TRUONG.
 * Chong troi dat giua hai ban: charts/fixtures/, ca hai validator chay cung bo ca.
 */
// Nap tu vung bang IMPORT ATTRIBUTE chu khong bang `fs.readFileSync`. Ban cu doc file
// luc chay, nen file nay nem loi ngay khi bi import trong trinh duyet, va do la ly do
// bon preset 15-18 chua mount song duoc suot Phase 4. Import attribute giai quyet ca
// hai dau ma KHONG nhan doi tu vung: Node doc thang file JSON, con esbuild inline noi
// dung file vao bundle lan `html-song`. `schema.vocab.json` van la nguon duy nhat, ban
// Python `schema.py` van doc dung file do.
import VOCAB_JSON from '../schema.vocab.json' with { type: 'json' };

export const VOCAB = VOCAB_JSON;
export const SCHEMA_VERSION = VOCAB.schema_version;

/** Ma loi ON DINH. Fixture vang doi chieu bang MA nay chu khong bang cau chu tieng
 * Viet, de sua loi nhan khong lam do test o phia ben kia. */
export const ERR = Object.freeze({
  THIEU_UNIT: 'THIEU_UNIT',
  UNIT_LA: 'UNIT_LA',
  THIEU_SOURCE: 'THIEU_SOURCE',
  TIER_LA: 'TIER_LA',
  DIRECTION_LA: 'DIRECTION_LA',
  KIND_LA: 'KIND_LA',
  ROLE_LA: 'ROLE_LA',
  STATUS_LA: 'STATUS_LA',
  THIEU_CODE: 'THIEU_CODE',
  CODE_QUA_DAI: 'CODE_QUA_DAI',
  VALUE_SAI_KIEU: 'VALUE_SAI_KIEU',
  VALUE_PHAI_NULL: 'VALUE_PHAI_NULL',
  VALUE_KHONG_DUOC_NULL: 'VALUE_KHONG_DUOC_NULL',
  PERIOD_TYPE_LA: 'PERIOD_TYPE_LA',
  THIEU_PERIOD_END: 'THIEU_PERIOD_END',
  PERIOD_END_SAI_DINH_DANG: 'PERIOD_END_SAI_DINH_DANG',
  THIEU_QUY: 'THIEU_QUY',
  QUY_NGOAI_PHAM_VI: 'QUY_NGOAI_PHAM_VI',
  THIEU_NAM: 'THIEU_NAM',
  DECIMALS_SAI: 'DECIMALS_SAI',
  CHI_SO_NGOAI_PHAM_VI: 'CHI_SO_NGOAI_PHAM_VI',
  DO_TIN_CAY_LA: 'DO_TIN_CAY_LA',
  DO_TIN_CAY_SAI_CAP: 'DO_TIN_CAY_SAI_CAP',
});

/** Do dai toi da cua entity.code. Khong ep viet hoa, khong ep bo dau, chi ep NGAN.
 * 24 ky tu du cho "Bat dong san KCN" ma van chan duoc viec do nguyen ten phap nhan
 * day du vao truc. Nhan dai hon thi dung wrapLabel() cua fmt.mjs hoac rut gon o tang
 * du lieu, tuy nguoi nhap quyet dinh, schema khong quyet ho. */
export const MAX_CODE_LEN = 24;

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

class LoiSchema extends Error {
  constructor(ma, chiTiet) {
    super(`${ma}: ${chiTiet}`);
    this.name = 'LoiSchema';
    this.ma = ma;
  }
}
export { LoiSchema };

function trongTuVung(nhom, gia_tri) {
  return Object.prototype.hasOwnProperty.call(VOCAB[nhom], gia_tri);
}

/**
 * Kiem MOT series (mot luot xep hang, mot duong, mot bo diem cung don vi).
 *
 * Hinh dang:
 *   {
 *     unit: 'phan_tram',
 *     source: { tier: 'cong-bo', label: 'BCTC quy 2/2026' },
 *     as_of: '2026-08-07',
 *     direction: 'cao_tot',     // tuy chon, mac dinh trung_tinh
 *     kind: 'ty_le',            // tuy chon, mac dinh luy_ke_ky
 *     decimals: 1,              // tuy chon, mac dinh lay theo unit trong tu vung
 *     rows: [ ... ]
 *   }
 *
 * Nem LoiSchema ngay lan vi pham dau tien. Fail-fast luc build tot hon canh bao im
 * lang, vi mot chart sai don vi trong ban PDF khong the goi lai duoc.
 */
export function validateSeries(series) {
  if (!series || typeof series !== 'object') {
    throw new LoiSchema(ERR.THIEU_UNIT, 'series khong phai doi tuong');
  }
  if (!series.unit) throw new LoiSchema(ERR.THIEU_UNIT, 'series thieu unit');
  if (!trongTuVung('unit', series.unit)) {
    throw new LoiSchema(
      ERR.UNIT_LA,
      `"${series.unit}" khong nam trong tu vung. Them vao charts/schema.vocab.json truoc, dung tu che chuoi moi trong preset`,
    );
  }
  if (!series.source || !series.source.tier) {
    throw new LoiSchema(ERR.THIEU_SOURCE, 'series thieu source.tier');
  }
  if (!trongTuVung('source_tier', series.source.tier)) {
    throw new LoiSchema(ERR.TIER_LA, `tier "${series.source.tier}" khong nam trong tu vung`);
  }
  if (series.direction !== undefined && !trongTuVung('direction', series.direction)) {
    throw new LoiSchema(ERR.DIRECTION_LA, `direction "${series.direction}" khong nam trong tu vung`);
  }
  if (series.kind !== undefined && !trongTuVung('kind', series.kind)) {
    throw new LoiSchema(ERR.KIND_LA, `kind "${series.kind}" khong nam trong tu vung`);
  }
  if (series.decimals !== undefined) {
    if (!Number.isInteger(series.decimals) || series.decimals < 0 || series.decimals > 6) {
      throw new LoiSchema(ERR.DECIMALS_SAI, `decimals phai la so nguyen 0 toi 6, dang la ${series.decimals}`);
    }
  }
  // `do_tin_cay` thuoc cap DIEM, khong thuoc cap series. Chan tuong minh o day chu khong
  // im lang bo qua: dat nham cap thi ca duong cong se mang mot do tin cay duy nhat, va do
  // dung la thu ma truong nay sinh ra de tranh.
  if (series.do_tin_cay !== undefined) {
    throw new LoiSchema(
      ERR.DO_TIN_CAY_SAI_CAP,
      'do_tin_cay thuoc cap TUNG DIEM chu khong phai cap series. Bac cua ca series la source.tier',
    );
  }
  const rows = series.rows || [];
  rows.forEach((r, i) => validateRow(r, i));
  return true;
}

/** Ep mot preset CHI nhan nhung don vi ma no ve dung duoc.
 *
 * Sinh ra tu mot the kho xu: nhieu preset dong cung don vi ngay trong ham dinh dang, vi
 * du waterfall goi `fmtCompact(v, { baseUnit: 'ty' })`. Sau khi bat moi preset phai khai
 * `series.unit`, ta co hai lua chon te va mot lua chon dung:
 *   - Khai `unit` roi phot lo no khi dinh dang: khai bao NOI DOI, va no im lang. Doi
 *     `unit` sang `teu` thi nhan van ra "tỷ", khong ai bao gi.
 *   - Viet lai moi preset cho nhan duoc moi don vi: dung ve nguyen tac nhung doi dien mao
 *     cua nhung preset von chi sinh ra cho mot dai luong duy nhat.
 *   - LUA CHON NAY: preset noi thang no lam duoc gi. Truyen don vi ngoai danh sach thi
 *     no bao loi ngay luc build thay vi ve ra mot nhan sai.
 *
 * @param {object} series khoi meta da qua validateSeries()
 * @param {string[]} duocPhep danh sach ma don vi preset ve dung duoc
 */
export function epDonVi(series, duocPhep) {
  if (!duocPhep.includes(series.unit)) {
    throw new LoiSchema(
      ERR.UNIT_LA,
      `preset nay chi ve dung duoc don vi ${duocPhep.join(', ')}, nhan duoc "${series.unit}". ` +
        'Dinh dang so cua no gan chat voi dai luong, doi unit ma khong doi ham dinh dang ' +
        'se cho mot nhan sai su that.',
    );
  }
  return true;
}

/** Kiem MOT hang quan sat. Goi rieng duoc khi khong co bao boc series. */
export function validateRow(row, chiSo = 0) {
  const o = `hang #${chiSo}`;
  if (!row || typeof row !== 'object') throw new LoiSchema(ERR.THIEU_CODE, `${o} khong phai doi tuong`);

  if (row.entity !== undefined) {
    if (!row.entity || !row.entity.code) {
      throw new LoiSchema(ERR.THIEU_CODE, `${o} co entity nhung thieu entity.code`);
    }
    if (String(row.entity.code).length > MAX_CODE_LEN) {
      throw new LoiSchema(
        ERR.CODE_QUA_DAI,
        `${o} entity.code dai ${row.entity.code.length} ky tu, toi da ${MAX_CODE_LEN}. Rut gon o tang du lieu, dung de nhan dai len truc`,
      );
    }
  }

  const status = row.status === undefined ? 'co_that' : row.status;
  if (!trongTuVung('status', status)) {
    throw new LoiSchema(ERR.STATUS_LA, `${o} status "${status}" khong nam trong tu vung`);
  }
  if (status === 'co_that') {
    if (typeof row.value !== 'number' || !Number.isFinite(row.value)) {
      throw new LoiSchema(
        ERR.VALUE_KHONG_DUOC_NULL,
        `${o} status co_that thi value phai la so huu han, dang la ${JSON.stringify(row.value)}`,
      );
    }
  } else if (row.value !== null && row.value !== undefined) {
    // Ba trang thai thieu deu phai de value la null. Neu de so cu o do, mot ngay nao
    // do co nguoi loc theo value thay vi theo status va so bi loai se song lai.
    throw new LoiSchema(
      ERR.VALUE_PHAI_NULL,
      `${o} status "${status}" thi value phai la null, dang giu ${JSON.stringify(row.value)}`,
    );
  }

  if (row.role !== undefined && !trongTuVung('role', row.role)) {
    throw new LoiSchema(ERR.ROLE_LA, `${o} role "${row.role}" khong nam trong tu vung`);
  }

  // `do_tin_cay` la do tin cay cua CHINH DIEM NAY, khac han `source.tier` la bac cua ca
  // series. Ho duong cong can no: mot duong lai suat that tron ca ky han thanh khoan cao
  // (quan sat truc tiep) lan ky han thua (dealer bao gia hoac noi suy), trong khi ca
  // duong van la MOT nguon o cap series. Truoc khi co truong nay, viz_eir_curves.py phai
  // tai dung `source_tier` o cap diem, va khi do doc mot diem thi khong biet no dang noi
  // ve nguon cua ca duong hay ve chinh no.
  if (row.do_tin_cay !== undefined && !trongTuVung('do_tin_cay', row.do_tin_cay)) {
    throw new LoiSchema(
      ERR.DO_TIN_CAY_LA,
      `${o} do_tin_cay "${row.do_tin_cay}" khong nam trong tu vung (${Object.keys(VOCAB.do_tin_cay).join(', ')})`,
    );
  }

  if (row.period !== undefined) validatePeriod(row.period, o);
  return true;
}

/**
 * Ky bao cao. BAT BUOC co `end` dang ISO, khong chi co quy va nam.
 *
 * Ly do: doanh nghiep Viet Nam co nam tai chinh lech (ket thuc 30/6 hoac 31/3 ton tai
 * that), nen "Quy 1" cua hai doanh nghiep co the khong trung nhau. Truc thoi gian chi
 * ghi "Q1" thi bang so sanh nganh sai ma khong ai phat hien. Ngoai ra chart duong cong
 * can sap xep tren truc thoi gian THAT, khong sap tren chuoi "Q1/24" duoc.
 */
export function validatePeriod(period, o = 'period') {
  if (!period || !trongTuVung('period_type', period.type)) {
    throw new LoiSchema(ERR.PERIOD_TYPE_LA, `${o} period.type "${period && period.type}" khong nam trong tu vung`);
  }
  if (!period.end) throw new LoiSchema(ERR.THIEU_PERIOD_END, `${o} thieu period.end dang YYYY-MM-DD`);
  if (!ISO_DATE.test(period.end)) {
    throw new LoiSchema(ERR.PERIOD_END_SAI_DINH_DANG, `${o} period.end "${period.end}" phai dang YYYY-MM-DD`);
  }
  if (period.type === 'quy') {
    if (period.q === undefined) throw new LoiSchema(ERR.THIEU_QUY, `${o} period.type quy thi phai co q`);
    if (!Number.isInteger(period.q) || period.q < 1 || period.q > 4) {
      throw new LoiSchema(ERR.QUY_NGOAI_PHAM_VI, `${o} q phai la so nguyen 1 toi 4, dang la ${period.q}`);
    }
  }
  if (period.type === 'quy' || period.type === 'nam') {
    if (!Number.isInteger(period.year)) throw new LoiSchema(ERR.THIEU_NAM, `${o} thieu year dang so nguyen`);
  }
  return true;
}

/** Cho tinh tu CHI SO NGUYEN, khong so sanh gia tri so thuc.
 * So sanh float de tim base case hay ngoai le la nguon loi im lang: hai gia tri bang
 * nhau ve mat kinh te van khac nhau o chu so thu muoi lam. */
export function coCo(chiSoCanDanhDau, tongSoHang) {
  if (!Number.isInteger(chiSoCanDanhDau) || chiSoCanDanhDau < 0 || chiSoCanDanhDau >= tongSoHang) {
    throw new LoiSchema(
      ERR.CHI_SO_NGOAI_PHAM_VI,
      `chi so ${chiSoCanDanhDau} nam ngoai pham vi 0 toi ${tongSoHang - 1}`,
    );
  }
  return (i) => i === chiSoCanDanhDau;
}

/** So chu so thap phan cho mot series: uu tien khai tuong minh, khong thi lay theo
 * don vi trong tu vung. Ca hai engine PHAI goi ham nay thay vi tu chon, neu khong ban
 * HTML hien 15,45% con ban PDF hien 15,5%. */
export function soThapPhan(series) {
  if (series.decimals !== undefined) return series.decimals;
  return VOCAB.unit[series.unit].decimals;
}

/** Cach ve ung voi tung trang thai. Tra ve mo ta thuan du lieu, khong phu thuoc engine,
 * de ban matplotlib va ban ECharts hanh xu giong nhau. */
export function cachVe(status) {
  const s = status || 'co_that';
  if (!trongTuVung('status', s)) throw new LoiSchema(ERR.STATUS_LA, `status "${s}" khong nam trong tu vung`);
  return {
    co_that: { ve_diem: true, noi_duong: true, danh_dau_truc: null },
    chua_cong_bo: { ve_diem: false, noi_duong: false, danh_dau_truc: 'chua_cong_bo' },
    khong_ton_tai: { ve_diem: false, noi_duong: false, danh_dau_truc: null },
    loai_bat_thuong: { ve_diem: false, noi_duong: false, danh_dau_truc: 'da_loai' },
  }[s];
}

/** Nhan don vi de in duoi truc hoac trong tieu de phu. */
export function nhanDonVi(unit) {
  if (!trongTuVung('unit', unit)) throw new LoiSchema(ERR.UNIT_LA, `unit "${unit}" khong nam trong tu vung`);
  return VOCAB.unit[unit].nhan;
}
