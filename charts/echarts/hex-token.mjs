// hex-token.mjs, hau xu ly mau cho SVG tinh: doi hex sang var(--ten-token, #hex-cu).
//
// VI SAO CAN FILE NAY: ECharts SSR ghi hex THANG vao SVG, khong var() nao chay luc
// nguoi doc xem (kiem duoc tren out-01-waterfall.svg truoc ban nay: 0 lan "var(--",
// moi hex da bake thanh chu literal). Chart tinh vi vay khong theo duoc chu de nguoi
// doc chon. Cach chua: hau xu ly chuoi SVG, doi MOI hex THUOC BANG MAU (PALETTE trong
// theme.mjs) thanh var(--ten-token, #hex-cu). Du phong LUON bang dung hex cu, vi file
// .svg con duoc mo DOC LAP ngoai trang HTML khai bien CSS -- thieu du phong la hinh
// mat sach mau, chi lo o duong mo doc lap.
//
// AN TOAN VI TAP HEX LA TAP DONG: TOKEN_CSS duoi day chi liet ke 11 khoa co MOT bien
// CSS duy nhat dai dien trong design-system/tokens.css (--accent, --accent-hi, ...).
// KHONG dong voi PALETTE.bandLo/bandMid/bandHi (dan xuat qua mixHex() trong theme.mjs,
// khong co bien CSS rieng trong tokens.css) hay mau dan xuat qua sequentialScale() --
// boc nhung mau do se phai bia ten bien CSS moi, vi pham luat "khong hardcode hex/ten
// bien moi ngoai theme.mjs". Nhung hex do CO CHU Y giu nguyen dang literal.
//
// Hex lay TU PALETTE luc chay, KHONG go tay chuoi hex nao trong file nay: test
// tests/consistency/chart_theme.test.mjs quet moi file .mjs trong charts/echarts/
// (tru theme.mjs) cam hardcode hex tran, va no quet ca file nay.
import { PALETTE } from './theme.mjs';

// Anh xa TEN THUOC TINH cua PALETTE sang TEN BIEN CSS trong design-system/tokens.css
// (xem khoi :root dau tien cua file do). Chu y --neg/--pos KHONG phai --negative/
// --positive: CSS dat ten ngan hon ten thuoc tinh JS cua PALETTE.
export const TOKEN_CSS = {
  accent: '--accent',
  accentHi: '--accent-hi',
  accentSoft: '--accent-soft',
  negative: '--neg',
  positive: '--pos',
  warn: '--warn',
  ink: '--ink',
  inkMd: '--ink-md',
  inkLo: '--ink-lo',
  line: '--line',
  paper: '--paper',
};

function thoatRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Mot vi tri khop hex duoc coi la "da boc" neu ngay truoc no la phan du phong cua
// mot loi goi var(--ten-bien, ) khac -- tranh long var() hai lan neu ham chay tren
// chinh dau ra cua no (idempotent), va la co so chung cho ca boc lan dem.
function daNamTrongVar(truoc) {
  return /var\(--[\w-]+,\s*$/.test(truoc);
}

/** Doi moi hex THUOC BANG MAU (xem TOKEN_CSS o tren) trong chuoi SVG thanh
 * var(--ten-token, #hex-cu). Hex KHONG thuoc bang mau (mau noi bo ECharts tu ve,
 * hoac mau dan xuat qua sequentialScale/mixHex) duoc GIU NGUYEN literal, co chu y. */
export function bocMauChuDe(svgText) {
  let ra = svgText;
  for (const [tenPalette, cssVar] of Object.entries(TOKEN_CSS)) {
    const hex = PALETTE[tenPalette];
    if (!hex) continue;
    const re = new RegExp(thoatRegex(hex), 'g');
    ra = ra.replace(re, (khop, viTri, chuoiGoc) => {
      const truoc = chuoiGoc.slice(Math.max(0, viTri - 40), viTri);
      if (daNamTrongVar(truoc)) return khop;
      return `var(${cssVar}, ${khop})`;
    });
  }
  return ra;
}

/** Dem so lan mot hex THUOC BANG MAU con nam TRAN (chua boc var()) trong chuoi SVG.
 * Dung lam gate hau-xu-ly: goi SAU bocMauChuDe() thi phai tra ve 0. Goi TRUOC
 * bocMauChuDe() tren mot SVG chua qua xu ly se tra ve > 0 (fixture do cua chinh gate
 * nay, xem tests/consistency/echarts_hex_residue_gate.test.mjs). */
export function demHexThoConLai(svgText) {
  let dem = 0;
  for (const tenPalette of Object.keys(TOKEN_CSS)) {
    const hex = PALETTE[tenPalette];
    if (!hex) continue;
    const re = new RegExp(thoatRegex(hex), 'g');
    let m;
    while ((m = re.exec(svgText))) {
      const truoc = svgText.slice(Math.max(0, m.index - 40), m.index);
      if (!daNamTrongVar(truoc)) dem += 1;
    }
  }
  return dem;
}
