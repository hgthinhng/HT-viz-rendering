// Schema va validator cua phong-cach.json. Nguon su that duy nhat cua tang style.
// Khong dung ajv o day du co san: luat "cam mau literal" can regex tren MOI string,
// ajv khong lam duoc gon; validator tay ~60 dong, de doc, de them luat.

export const BAY_LOAI_AN_PHAM = [
  'ban-tin-thi-truong',
  'cap-nhat-kqkd',
  'bao-cao-khoi-tao-ma',
  'bao-cao-nganh',
  'deal-pack',
  'tom-tat-dieu-hanh',
  'ban-mau-ky-thuat',
];

// Bat hex (#abc, #aabbcc) va ham mau voi literal ben trong. var() duoc phep.
export const RE_MAU_LITERAL =
  /#[0-9a-fA-F]{3,8}\b|(?:rgb|rgba|hsl|hsla|oklch|lab|lch|color|color-mix)\s*\(/;

const TRANG_THAI_HOP_LE = ['chinh-thuc', 'vuon-uom'];

export function validatePhongCach(obj, { tenThuMuc = null, danhSachChuDe = [] } = {}) {
  const loi = [];
  const bat = (dk, msg) => { if (!dk) loi.push(msg); };

  bat(typeof obj.slug === 'string' && /^[a-z0-9-]+$/.test(obj.slug), 'slug phai la chuoi khong dau, chi a-z0-9-');
  if (tenThuMuc) bat(obj.slug === tenThuMuc, `slug ${obj.slug} phai trung ten thu muc ${tenThuMuc}`);
  bat(typeof obj.tagline === 'string' && obj.tagline.length >= 10, 'tagline phai co, toi thieu 10 ky tu');
  bat(Array.isArray(obj.mood) && obj.mood.length >= 1, 'mood phai la mang co it nhat 1 phan tu');
  bat(['cao', 'trung-cao', 'trung', 'thap'].includes(obj.formality), 'formality khong hop le');
  bat(['cao', 'trung', 'thap'].includes(obj.density), 'density khong hop le');
  for (const k of ['best_for', 'avoid_for']) {
    bat(Array.isArray(obj[k]), `${k} phai la mang`);
    for (const v of obj[k] || []) {
      bat(BAY_LOAI_AN_PHAM.includes(v), `${k} chua slug la: ${v}`);
    }
  }
  bat(typeof obj.chu_de_mac_dinh === 'string', 'chu_de_mac_dinh phai co');
  if (danhSachChuDe.length) {
    bat(danhSachChuDe.includes(obj.chu_de_mac_dinh),
      `chu_de_mac_dinh ${obj.chu_de_mac_dinh} khong co trong design-system/themes/`);
    if (obj.chu_de_dan_xuat != null) {
      bat(danhSachChuDe.includes(obj.chu_de_dan_xuat),
        `chu_de_dan_xuat ${obj.chu_de_dan_xuat} khong co trong design-system/themes/`);
    }
  }
  bat(Array.isArray(obj.gioi_han_loai_hinh), 'gioi_han_loai_hinh phai la mang, rong cung duoc');
  bat(obj.font && typeof obj.font.kit === 'string', 'font.kit phai co');
  bat(obj.token_override && typeof obj.token_override === 'object', 'token_override phai la object, rong cung duoc');
  for (const [k, v] of Object.entries(obj.token_override || {})) {
    bat(k.startsWith('--'), `token_override khoa ${k} phai bat dau bang --`);
    bat(!RE_MAU_LITERAL.test(String(v)),
      `token_override[${k}] chua mau literal, chi duoc var() hoac literal phi mau: ${v}`);
  }
  bat(typeof obj.chart_palette === 'string', 'chart_palette phai co');
  bat(TRANG_THAI_HOP_LE.includes(obj.trang_thai), 'trang_thai chi nhan chinh-thuc hoac vuon-uom');
  if (obj.trang_thai === 'chinh-thuc') {
    bat(typeof obj.exemplar === 'string' && obj.exemplar.startsWith('examples/'),
      'chinh-thuc thi exemplar phai tro vao examples/');
  }
  return { hopLe: loi.length === 0, loi };
}

// Luat rieng cho style co chu de mac dinh TOI: bat buoc cam matplotlib.
// Goi RIENG vi can biet paper cua chu de; ham nhan san co toi hay khong.
export function validateGioiHanChoChuDeToi(obj, chuDeLaToi) {
  if (!chuDeLaToi) return { hopLe: true, loi: [] };
  const ok = (obj.gioi_han_loai_hinh || []).includes('matplotlib');
  return {
    hopLe: ok,
    loi: ok ? [] : [`style ${obj.slug} co chu de toi thi gioi_han_loai_hinh phai chua "matplotlib"`],
  };
}
