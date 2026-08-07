// fmt.mjs: Bộ định dạng số tiếng Việt CANONICAL cho báo cáo tài chính.
//
// QUYẾT ĐỊNH ĐÃ CHỐT (không phải "tuỳ chọn ngang nhau"):
//   - Phân cách hàng nghìn = DẤU CHẤM "."; phân cách thập phân = DẤU PHẨY ",".
//     Ví dụ: 1.234.567,89  (KHÔNG dùng 1,234,567.89 kiểu Anh-Mỹ).
//     Lý do: (1) đối tượng đọc là người Việt trong nước, khớp locale vi-VN và
//     Windows VN mà file sẽ mở trên đó; (2) rủi ro đọc nhầm "1,234" thành
//     "1 phẩy 234" ở người đọc chỉ quen chuẩn Việt là lỗi hiểu-sai số tiền thật,
//     không phải lỗi thẩm mỹ, với báo cáo tài chính đây là rủi ro không chấp
//     nhận được. Nếu cần bản song ngữ/quốc tế, gọi fmt* với locale:'en' để lật
//     sang kiểu Anh-Mỹ, KHÔNG trộn hai kiểu trong cùng một tài liệu.
//   - Đơn vị rút gọn: nghìn (10^3, hiếm dùng riêng) / tr = triệu (10^6) /
//     tỷ (10^9) / nghìn tỷ (10^12). KHÔNG dùng "tỷ tỷ" hay "triệu tỷ".
//   - %: KHÔNG có khoảng trắng trước "%" (khớp báo chí & CTCK Việt Nam:
//     "tăng 12,5%", không phải "12,5 %").
//   - Bội số (x lần): dạng gọn "15,2x" cho bảng/biểu đồ (khớp quy ước P/E, P/B
//     quốc tế mà dân tài chính VN cũng dùng); dạng văn xuôi "15,2 lần" khi viết
//     câu hoàn chỉnh. Hai dạng khác nhau, không phải lỗi.
//   - Kỳ báo cáo: nhãn gọn trên biểu đồ = "Q{n}/{YYYY}" (vd Q3/2026); trong câu
//     văn xuôi = "quý {n}/{YYYY}". KHÔNG dùng kiểu Mỹ rút gọn "3Q26" vì đây là
//     báo cáo tiếng Việt, "3Q26" không phải quy ước người đọc VN quen.
//   - Làm tròn nhãn trên biểu đồ về tối đa 3 chữ số có nghĩa (FT/Economist
//     style: không hiển thị "1.234,5678 tỷ" trên trục, chỉ "1.230 tỷ" hoặc
//     "1,23 nghìn tỷ").
//   - Số âm: dấu trừ "-" đứng ngay trước số, không dùng ngoặc đơn kế toán
//     kiểu Anh-Mỹ (123) trừ khi bảng đó là bảng kế toán thuần tuý theo yêu cầu
//     khách hàng.

const GROUP_VN = '.';
const DECIMAL_VN = ',';
const GROUP_EN = ',';
const DECIMAL_EN = '.';

function sign(n) {
  return n < 0 ? '-' : '';
}

/** Làm tròn tới N chữ số có nghĩa (không phải N chữ số thập phân). */
export function roundSigFig(value, sigFigs = 3) {
  if (value === 0 || !isFinite(value)) return 0;
  const d = Math.ceil(Math.log10(Math.abs(value)));
  const power = sigFigs - d;
  const factor = Math.pow(10, power);
  return Math.round(value * factor) / factor;
}

/**
 * Định dạng số thô theo locale vi-VN (mặc định) hoặc en.
 * fmtNumber(1234567.89) -> "1.234.567,89"
 * fmtNumber(1234.5, {decimals:1}) -> "1.234,5"
 */
export function fmtNumber(value, opts = {}) {
  const { decimals = null, locale = 'vi', sigFig = null } = opts;
  if (value === null || value === undefined || Number.isNaN(value)) return '-';
  let v = value;
  if (sigFig) v = roundSigFig(v, sigFig);
  const groupSep = locale === 'en' ? GROUP_EN : GROUP_VN;
  const decSep = locale === 'en' ? DECIMAL_EN : DECIMAL_VN;
  const abs = Math.abs(v);
  const fixed = decimals === null ? String(abs) : abs.toFixed(decimals);
  let [intPart, decPart] = fixed.split('.');
  // loại bỏ .0 dư khi decimals không ép cứng
  if (decimals === null && decPart === '0') decPart = undefined;
  intPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, groupSep);
  return sign(v) + intPart + (decPart ? decSep + decPart : '');
}

/**
 * Rút gọn đơn vị VN tự động: nghìn / tr / tỷ / nghìn tỷ.
 * baseUnit: đơn vị của value đầu vào: 'dong' (mặc định) hoặc 'ty' (đã tính bằng tỷ).
 */
export function fmtCompact(value, opts = {}) {
  const { decimals, baseUnit = 'dong', locale = 'vi' } = opts;
  if (value === null || value === undefined || Number.isNaN(value)) return '-';
  // quy hết về đơn vị "đồng" để chọn bậc thống nhất
  const multiplier = baseUnit === 'ty' ? 1e9 : baseUnit === 'trieu' ? 1e6 : 1;
  const dong = value * multiplier;
  const abs = Math.abs(dong);
  let unit, div;
  if (abs >= 1e12) { unit = 'nghìn tỷ'; div = 1e12; }
  else if (abs >= 1e9) { unit = 'tỷ'; div = 1e9; }
  else if (abs >= 1e6) { unit = 'tr'; div = 1e6; }
  else if (abs >= 1e3) { unit = 'nghìn'; div = 1e3; }
  else { unit = 'đồng'; div = 1; }
  // đồng lẻ không có phần thập phân trừ khi caller ép rõ decimals
  const effDecimals = decimals !== undefined ? decimals : (div === 1 ? 0 : 1);
  const num = fmtNumber(dong / div, { decimals: effDecimals, locale });
  return `${num} ${unit}`;
}

/** fmtPercent(12.5) -> "12,5%"; fmtPercent(-3.456, {decimals:2}) -> "-3,46%" */
export function fmtPercent(value, opts = {}) {
  const { decimals = 1, locale = 'vi', showPlus = false } = opts;
  if (value === null || value === undefined || Number.isNaN(value)) return '-';
  const s = fmtNumber(value, { decimals, locale });
  const prefix = showPlus && value > 0 ? '+' : '';
  return `${prefix}${s}%`;
}

/** fmtMultiple(15.234) -> "15,2x" (bảng/trục); {prose:true} -> "15,2 lần" (văn xuôi) */
export function fmtMultiple(value, opts = {}) {
  const { decimals = 1, locale = 'vi', prose = false } = opts;
  if (value === null || value === undefined || Number.isNaN(value)) return '-';
  const s = fmtNumber(value, { decimals, locale });
  return prose ? `${s} lần` : `${s}x`;
}

/** fmtDelta(-45, {unit:'tỷ'}) -> "-45,0 tỷ"; dấu +/- luôn hiện tường minh */
export function fmtDelta(value, opts = {}) {
  const { decimals = 1, unit = '', locale = 'vi' } = opts;
  if (value === null || value === undefined || Number.isNaN(value)) return '-';
  const prefix = value > 0 ? '+' : '';
  const s = fmtNumber(value, { decimals, locale });
  return unit ? `${prefix}${s} ${unit}` : `${prefix}${s}`;
}

/** fmtQuarter(3, 2026) -> "Q3/2026"; {prose:true} -> "quý 3/2026" */
export function fmtQuarter(q, year, opts = {}) {
  const { prose = false } = opts;
  return prose ? `quý ${q}/${year}` : `Q${q}/${year}`;
}

/** fmtAxisLabel: dùng cho nhãn trục, ép về ≤3 chữ số có nghĩa + đơn vị rút gọn */
export function fmtAxisLabel(value, opts = {}) {
  return fmtCompact(value, { ...opts, decimals: opts.decimals ?? 0 });
}

// ------------------------- SELF TEST (>=15 case) -------------------------
/** Boc chuoi dai thanh nhieu dong theo ranh gioi TU, khong cat giua am tiet.
 *
 * Dung cho nhan truc va chu thich dai. Nguong tinh theo SO KY TU chu khong theo
 * pixel: font mono cua repo rong deu nen quy doi duoc, con font serif thi con so
 * nay la uoc luong, phai nhin anh that de chinh.
 *
 * LUU Y VE PHAM VI: day la loi thoat cho nhan KHONG co ma ngan tu nhien (ten
 * phan khuc kinh doanh, ten chinh sach). Voi thuc the CO ma ngan (ma chung
 * khoan, ma nganh) thi rut gon phai lam o TANG DU LIEU qua entity.code, khong
 * phai boc dong o tang hien thi. Boc dong tren truc lam lech chieu cao hang va
 * kho kiem soat khi so hang thay doi.
 */
export function wrapLabel(text, maxCharsPerLine = 16) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = '';
  for (const w of words) {
    const next = cur ? `${cur} ${w}` : w;
    if (next.length > maxCharsPerLine && cur) {
      lines.push(cur);
      cur = w;
    } else {
      cur = next;
    }
  }
  if (cur) lines.push(cur);
  return lines.length ? lines : [''];
}

export function runSelfTest() {
  const cases = [
    [() => fmtNumber(1234567.89, { decimals: 2 }), '1.234.567,89'],
    [() => fmtNumber(1234.5, { decimals: 1 }), '1.234,5'],
    [() => fmtNumber(-1234.5, { decimals: 1 }), '-1.234,5'],
    [() => fmtNumber(0, { decimals: 1 }), '0,0'],
    [() => fmtNumber(999), '999'],
    [() => fmtNumber(1000), '1.000'],
    [() => fmtNumber(1234567.89, { decimals: 2, locale: 'en' }), '1,234,567.89'],
    [() => fmtCompact(47_000_000_000), '47,0 tỷ'],
    [() => fmtCompact(1_230_000_000_000), '1,2 nghìn tỷ'],
    [() => fmtCompact(2_500_000), '2,5 tr'],
    [() => fmtCompact(120, { baseUnit: 'ty' }), '120,0 tỷ'],
    [() => fmtCompact(-45, { baseUnit: 'ty' }), '-45,0 tỷ'],
    [() => fmtCompact(500), '500 đồng'],
    [() => fmtPercent(12.5), '12,5%'],
    [() => fmtPercent(-3.456, { decimals: 2 }), '-3,46%'],
    [() => fmtPercent(8, { showPlus: true }), '+8,0%'],
    [() => fmtMultiple(15.234), '15,2x'],
    [() => fmtMultiple(15.234, { prose: true }), '15,2 lần'],
    [() => fmtDelta(-45, { unit: 'tỷ' }), '-45,0 tỷ'],
    [() => fmtDelta(45, { unit: 'tỷ' }), '+45,0 tỷ'],
    [() => fmtQuarter(3, 2026), 'Q3/2026'],
    [() => fmtQuarter(3, 2026, { prose: true }), 'quý 3/2026'],
    [() => roundSigFig(1234.5678, 3), 1230],
    [() => roundSigFig(0.012345, 3), 0.0123],
    [() => fmtNumber(null), '-'],
  ];
  let pass = 0;
  const results = [];
  cases.forEach(([fn, expected], i) => {
    const actual = fn();
    const ok = String(actual) === String(expected);
    if (ok) pass++;
    results.push({ i: i + 1, expected, actual, ok });
  });
  return { pass, total: cases.length, results };
}

// `typeof process !== 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi
// import trong trinh duyet: MOI preset ECharts import ham dinh dang tu day, nen neu
// nhanh nay tham chieu `process` khong dieu kien thi ca 18 preset deu khong mount song
// duoc trong DOM qua mount-live.mjs (lan html-song), du ban than tung preset da tach
// dung option()/render.
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { pass, total, results } = runSelfTest();
  results.forEach(r => {
    console.log(`${r.ok ? 'PASS' : 'FAIL'} #${r.i}: expected="${r.expected}" actual="${r.actual}"`);
  });
  console.log(`\n=== ${pass}/${total} PASS ===`);
  if (pass !== total) process.exit(1);
}
