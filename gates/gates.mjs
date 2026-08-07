/**
 * gates.mjs, muoi gate nghiem thu truoc khi giao file. Moi gate la mot ham THUAN
 * nhan cung mot goi du lieu va tra ve { ten, trang_thai, ly_do[] }.
 *
 * Tach khoi `run.mjs` de bo test goi thang duoc tung gate voi fixture do va fixture
 * xanh, khong phai spawn tien trinh. Do la dieu kien de kiem duoc dieu quan trong
 * nhat: MOT GATE PHAI CHUNG MINH NO PHAN BIET DUOC HAI TRANG THAI truoc khi no co
 * quyen bao xanh. Repo nay da co ba gate xanh vi phep do rong, ca ba deu "chay dung"
 * va deu vo dung.
 *
 * Trang thai: 'PASS' | 'WARN' | 'FAIL' | 'SKIP'. Chi FAIL moi chan giao file. SKIP
 * bat buoc kem ly do, khong duoc dung SKIP de giau mot phep do khong lam duoc.
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { kiemTraXml } from './lib/xml.mjs';

const THU_MUC = path.dirname(fileURLToPath(import.meta.url));

// --------------------------------------------------------------------------- //
// Tien ich dung chung
// --------------------------------------------------------------------------- //
export function boTrang(s) {
  return String(s).replace(/\s+/g, '');
}

/** Van ban hien thi cua HTML: bo script, style, va the. */
export function textHienThi(html) {
  return html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Tach tung khoi <svg>...</svg> inline trong HTML, kem ma hinh cha neu co. */
export function tachSvg(html) {
  const ra = [];
  const re = /<figure class="hinh" id="([^"]+)"[\s\S]*?(<svg[\s\S]*?<\/svg>)[\s\S]*?<\/figure>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    ra.push({ maHinh: m[1], svg: m[2] });
  }
  // SVG nam ngoai figure (vi du logo) van phai hop le XML, gom them.
  const conLai = html.replace(re, ' ');
  const re2 = /<svg[\s\S]*?<\/svg>/gi;
  let m2;
  while ((m2 = re2.exec(conLai)) !== null) {
    ra.push({ maHinh: null, svg: m2[0] });
  }
  return ra;
}

function ghi(ten, trang_thai, ly_do) {
  return { ten, trang_thai, ly_do: ly_do || [] };
}

// --------------------------------------------------------------------------- //
// Gate 1, FONT-HTML
// --------------------------------------------------------------------------- //
const FONT_WINDOWS_AN_TOAN = [
  'segoe ui', 'times new roman', 'arial', 'calibri', 'cambria',
  'georgia', 'consolas', 'courier new', 'tahoma', 'verdana',
];

export function gateFontHtml({ html }) {
  const ly_do = [];
  const reFace = /@font-face\s*{([^}]*)}/gis;
  const face = new Map();
  let m;
  while ((m = reFace.exec(html)) !== null) {
    const khoi = m[1];
    const ten = khoi.match(/font-family:\s*["']?([^;"'\n]+)["']?\s*;/i);
    if (!ten) continue;
    const ma = ten[1].trim().toLowerCase();
    const coDataUri = /src:\s*url\(data:(font|application)\//i.test(khoi);
    const ur = khoi.match(/unicode-range:\s*([^;]+);/i);
    const dai = ur ? ur[1].split(',').map((s) => s.trim()) : [];
    if (!face.has(ma)) face.set(ma, { coDataUri: false, dai: [] });
    const e = face.get(ma);
    e.coDataUri = e.coDataUri || coDataUri;
    e.dai.push(...dai);
  }

  // Font khong khai unicode-range thi phu TOAN BO bang chu, ke ca khoi co dau. Chi khi
  // co khai unicode-range moi phai kiem no co phu khoi tien-compose tieng Viet khong.
  function phuTiengViet(dai) {
    if (dai.length === 0) return true;
    return dai.some((r) => {
      const rr = r.toUpperCase();
      if (rr.includes('1EA0') || rr.includes('1EF')) return true;
      if (/U\+030[0139]/.test(rr)) return true;
      return false;
    });
  }

  const cssThan = html.replace(reFace, ' ');
  const stack = new Set();
  const reDung = /font-family:\s*([^;}]+)/gi;
  let d;
  while ((d = reDung.exec(cssThan)) !== null) stack.add(d[1].trim());

  const xau = [];
  for (const s of stack) {
    if (/^var\(/i.test(s)) continue;
    const dau = s.split(',')[0].trim().replace(/^["']|["']$/g, '').toLowerCase();
    if (FONT_WINDOWS_AN_TOAN.includes(dau)) continue;
    if (face.has(dau)) {
      const f = face.get(dau);
      if (f.coDataUri && phuTiengViet(f.dai)) continue;
      xau.push(`stack "${s}": ${!f.coDataUri ? 'khong nhung base64' : 'unicode-range khong phu dau tieng Viet'}`);
      continue;
    }
    xau.push(`stack "${s}": khong phai font Windows chuan va khong co @font-face nhung kem`);
  }

  if (face.size === 0 && stack.size === 0) {
    return ghi('1. FONT-HTML', 'WARN', ['khong tim thay khai bao font nao, khong kiem duoc gi']);
  }
  if (xau.length) return ghi('1. FONT-HTML', 'FAIL', xau);
  ly_do.push(`${face.size} @font-face nhung base64, ${stack.size} stack dung trong CSS deu hop le`);
  return ghi('1. FONT-HTML', 'PASS', ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 2, FONT-PDF
// --------------------------------------------------------------------------- //
// Ho font he thong Linux. Chung xuat hien trong PDF nghia la trang da am tham roi ve
// font cua may dang render, va file gui di se khac han file da duyet.
const HO_FONT_HE_THONG = /noto|liberation|dejavu|freeserif|freesans|nimbus|urw|c059|d050/i;

export function gateFontPdf({ pdf }) {
  const ho = Object.keys(pdf.font.ho_font);
  if (ho.length === 0) {
    return ghi('2. FONT-PDF', 'FAIL', ['PDF khong nhung font nao, khong the doc duoc dung tren may khac']);
  }
  const heThong = ho.filter((t) => HO_FONT_HE_THONG.test(t));
  const khongNhung = ho.filter((t) => !pdf.font.ho_font[t].nhung);

  const ly_do = [`font trong PDF: ${ho.join(', ')}`];
  let trang_thai = 'PASS';
  if (heThong.length) {
    trang_thai = 'FAIL';
    ly_do.push(
      `${heThong.length} font he thong Linux lot vao PDF: ${heThong.join(', ')}. Trang da roi ve ` +
      `font cua may dang render. LUU Y: tang text van doc dung trong ca nay, nen gate dau tieng Viet ` +
      `KHONG bat duoc. Da do bang so: cung mot trang, ban co @font-face cho Spectral, ban bo @font-face ` +
      `cho Noto-Serif, ca hai deu 0 FFFD va 0 ky tu synthetic.`
    );
  }
  if (khongNhung.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${khongNhung.length} font duoc tham chieu nhung KHONG nhung: ${khongNhung.join(', ')}`);
  }
  return ghi('2. FONT-PDF', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 3, RASTER
// --------------------------------------------------------------------------- //
export function gateRaster({ pdf, choPhepAnh = 0 }) {
  const r = pdf.raster;
  const ly_do = [
    `${r.so_object} object /Subtype /Image trong ${pdf.so_trang} trang, ` +
    `${(pdf.byte_moi_trang / 1024).toFixed(0)}KB moi trang, file ${(pdf.kich_thuoc_byte / 1e6).toFixed(2)}MB`,
  ];
  let trang_thai = 'PASS';
  if (r.so_object > choPhepAnh) {
    trang_thai = 'FAIL';
    ly_do.push(
      `so anh raster (${r.so_object}) vuot muc cho phep ${choPhepAnh}. Voi WeasyPrint va chart SVG ` +
      `thi muc dung phai la 0; anh chup that neu co phai khai tuong minh qua --cho-phep-anh`
    );
  }
  if (r.anh_toan_panel.length) {
    trang_thai = 'FAIL';
    const vd = r.anh_toan_panel.slice(0, 3).map((a) => `${a.w}x${a.h}`).join(', ');
    ly_do.push(`${r.anh_toan_panel.length} anh full-panel tren 500.000px (${vd}), dau hieu mot khoi bi nuong bitmap`);
  }
  return ghi('3. RASTER', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 4, DIACRITICS
// --------------------------------------------------------------------------- //
const RE_DAU_VIET = /[ăâêôơưđẠẢÃÀÁĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐạảãàáăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/g;

export function gateDau({ html, pdf }) {
  const d = pdf.dau;
  const ly_do = [];
  let trang_thai = 'PASS';

  const soHtml = (textHienThi(html).match(RE_DAU_VIET) || []).length;
  ly_do.push(`ky tu co dau: HTML nguon ${soHtml}, PDF da render ${d.dau_tong}`);

  if (d.fffd > 0) {
    trang_thai = 'FAIL';
    ly_do.push(`${d.fffd} ky tu U+FFFD trong PDF, glyph mat hoan toan`);
  }
  if (d.dau_synthetic > 0) {
    trang_thai = 'FAIL';
    ly_do.push(`${d.dau_synthetic} ky tu CO DAU bi MuPDF danh dau synthetic, nghi ngo vo dau`);
  }
  if (soHtml > 0 && d.dau_tong < soHtml * 0.9) {
    if (trang_thai === 'PASS') trang_thai = 'WARN';
    const hut = (100 * (1 - d.dau_tong / soHtml)).toFixed(0);
    ly_do.push(`PDF it dau hon HTML khoang ${hut}%, kiem xem co noi dung bi rung khi render khong`);
  }
  ly_do.push(
    `bo qua ${d.synthetic_khoang_trang} dau CACH bi danh synthetic: font subset khong nhung glyph ` +
    `khoang trang nen MuPDF tu tong hop, day la binh thuong. Dem ca thi gate do vinh vien.`
  );
  ly_do.push(
    'GIOI HAN: day la phep do tang van ban. No khong bat duoc truong hop ToUnicode dung ma glyph ' +
    'outline bi thay bang .notdef, va no KHONG bat duoc font sai. Gate 2 FONT-PDF moi bat font sai.'
  );
  return ghi('4. DIACRITICS', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 5, CHART-SONG
// --------------------------------------------------------------------------- //
/**
 * Gate quan trong nhat cua ca bo, sinh ra tu bug da song tron mot phase: 12 chart xuat
 * SVG khong hop le XML, WeasyPrint bo qua ca file, PDF ra 0 net ve, va moi gate cu van
 * xanh vi chung chi DEM chuoi chu khong PARSE.
 *
 * Hai tang, va tang hai moi la tang that:
 *   1. Moi SVG inline phai parse duoc XML.
 *   2. Moi hinh phai DE LAI DAU VET trong PDF: lay nhung chuoi chu dai nhat trong SVG
 *      roi doi chieu voi tang text cua PDF. SVG bi bo qua thi nhung chuoi do bien mat.
 *      Doi chieu sau khi bo het khoang trang, vi trich text tu PDF nuot khoang trang
 *      giua cac glyph sat nhau.
 */
export function gateChartSong({ html, pdf }) {
  const hinh = tachSvg(html);
  const ly_do = [];
  let trang_thai = 'PASS';

  if (hinh.length === 0) {
    return ghi('5. CHART-SONG', 'SKIP', ['trang khong co SVG inline nao, khong co gi de kiem']);
  }

  for (const { maHinh, svg } of hinh) {
    const nhan = maHinh || '(svg ngoai figure)';
    const loi = kiemTraXml(svg);
    if (loi) {
      trang_thai = 'FAIL';
      ly_do.push(`${nhan}: KHONG phai XML hop le (${loi}). WeasyPrint se bo qua ca file, PDF mat sach hinh`);
      continue;
    }
    const chu = [...svg.matchAll(/<text[^>]*>([\s\S]*?)<\/text>/gi)]
      .map((m) => m[1].replace(/<[^>]+>/g, '').trim())
      .filter((s) => s.length >= 4)
      .sort((a, b) => b.length - a.length)
      .slice(0, 3);
    if (chu.length === 0) {
      ly_do.push(`${nhan}: khong co chuoi chu nao du dai de doi chieu, chi kiem duoc XML`);
      continue;
    }
    const mat = chu.filter((s) => !pdf.text_bo_trang.includes(boTrang(s)));
    if (mat.length === chu.length) {
      trang_thai = 'FAIL';
      ly_do.push(
        `${nhan}: khong mot chuoi chu nao cua hinh co mat trong tang text cua PDF ` +
        `(vi du "${chu[0]}"). Hinh nay khong den duoc ban in`
      );
    } else if (mat.length) {
      if (trang_thai === 'PASS') trang_thai = 'WARN';
      ly_do.push(`${nhan}: thieu ${mat.length} tren ${chu.length} chuoi doi chieu, vi du "${mat[0]}"`);
    }
  }

  if (trang_thai === 'PASS') {
    ly_do.unshift(`${hinh.length} hinh: XML hop le va deu de lai chu trong tang text cua PDF`);
  }
  return ghi('5. CHART-SONG', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 6, CALLOUT-BAKED
// --------------------------------------------------------------------------- //
/**
 * WeasyPrint khong chay JavaScript. Mot trang dua vao `annotate.js` de ve callout luc
 * chay thi ban HTML dep con ban PDF mat sach lop chu thich. Da do that: minh hoa con
 * tau qua WeasyPrint cho 42 net ve va 197 ky tu text, 0 tren 7 callout; ban da bake cho
 * 74 net ve va du 7 callout.
 *
 * Gate chan hai dau: trang giao di khong duoc con tham chieu toi annotate.js, va lop
 * `g.annotations` neu co thi phai co chu that ben trong.
 */
export function gateCalloutBaked({ html }) {
  const ly_do = [];
  let trang_thai = 'PASS';

  if (/<script[^>]+annotate\.js/i.test(html) || /Annotate\s*\.\s*annotate\s*\(/.test(html)) {
    trang_thai = 'FAIL';
    ly_do.push(
      'trang con goi annotate.js luc chay. WeasyPrint khong chay JavaScript nen moi callout se ' +
      'vang mat khoi PDF. Bake truoc bang `node pipeline/bake_svg.mjs` roi nhung file SVG tinh'
    );
  }

  const lop = [...html.matchAll(/<g[^>]*class="annotations"[^>]*>([\s\S]*?)<\/g>\s*<\/svg>/gi)];
  if (lop.length === 0) {
    if (trang_thai === 'PASS') {
      return ghi('6. CALLOUT-BAKED', 'SKIP', ['trang khong co lop chu thich nao, khong co gi de kiem']);
    }
  } else {
    for (const [i, l] of lop.entries()) {
      const soChu = (l[1].match(/<text/gi) || []).length;
      if (soChu === 0) {
        trang_thai = 'FAIL';
        ly_do.push(`lop chu thich thu ${i + 1} khong co the <text> nao, callout rong`);
      }
    }
    if (trang_thai === 'PASS') {
      ly_do.push(`${lop.length} lop chu thich da bake, deu co chu that ben trong`);
    }
  }
  return ghi('6. CALLOUT-BAKED', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 7, STYLE
// --------------------------------------------------------------------------- //
const CUM_AI_SLOP = [
  'Điều đáng chú ý', 'Không thể phủ nhận', 'Tóm lại', 'Trong bối cảnh',
  'Hơn nữa,', 'Bên cạnh đó,', 'Nhìn chung,', 'Có thể thấy rằng',
];

export function gateVanPhong({ html }) {
  const ly_do = [];
  let trang_thai = 'PASS';
  const text = textHienThi(html);

  // Escape unicode, KHONG viet ky tu truc tiep. Mot dot don gach ngang hang loat
  // da tung doi ky tu ngay trong regex nay thanh [--], tuc chi con khop dau gach
  // noi thuong: gate bao FAIL cho moi noi dung binh thuong va khong con bat em-dash.
  const gach = text.match(/[\u2014\u2013]/g);
  if (gach && gach.length) {
    trang_thai = 'FAIL';
    ly_do.push(`${gach.length} em-dash hoac en-dash trong noi dung hien thi`);
  }

  const slop = CUM_AI_SLOP.filter((t) => text.includes(t));
  if (slop.length) {
    trang_thai = 'FAIL';
    ly_do.push(`cum tu AI-slop: ${slop.join(' | ')}`);
  }

  // Cau ket kieu cach ngon: "khong phai X ma la Y", "khong ... bang ..., chi ..."
  const cn1 = text.match(/không [^.]{0,40} bằng [^.]{0,45}, chỉ/g);
  const cn2 = text.match(/nhất cũng là [^.]{0,30} nhất/g);
  if ((cn1 && cn1.length) || (cn2 && cn2.length)) {
    trang_thai = 'FAIL';
    ly_do.push(`cau ket luan kieu cach ngon: ${[...(cn1 || []), ...(cn2 || [])].join(' || ')}`);
  }

  if (trang_thai === 'PASS') ly_do.push('khong thay em-dash, AI-slop hay cau ket cach ngon');
  return ghi('7. STYLE', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 8, PAGEBREAK
// --------------------------------------------------------------------------- //
export function gateNgatTrang({ html, pdf }) {
  const ly_do = [];
  let trang_thai = 'PASS';
  const css = (html.match(/<style\b[^>]*>([\s\S]*?)<\/style>/gi) || []).join('\n');
  const coBreak = /break-inside\s*:\s*avoid/i.test(css) || /page-break-inside\s*:\s*avoid/i.test(css);

  if (!coBreak) {
    trang_thai = 'WARN';
    ly_do.push('CSS khong co rule break-inside avoid nao, khong co co che bao ve khoi bi cat doi');
  } else {
    ly_do.push('CSS co khai break-inside avoid');
  }

  const nt = pdf.ngat_trang;
  if (nt.so_lan > 0) {
    trang_thai = 'FAIL';
    ly_do.push(`${nt.so_lan} the bi cat dung tai bien trang: ${JSON.stringify(nt.the_bi_cat.slice(0, 3))}`);
  } else {
    ly_do.push('hinh hoc tren PDF that: 0 the bi cat tai bien trang trong lan render nay');
    if (!coBreak) {
      ly_do.push(
        'LUU Y: 0 truong hop o lan nay co the la may rui cua lan reflow nay chu khong phai do thiet ke, ' +
        'vi khong co CSS bao ve thi doi noi dung sau nay co the sinh cat trang moi ma khong ai canh bao'
      );
    }
  }
  return ghi('8. PAGEBREAK', trang_thai, ly_do);
}

// --------------------------------------------------------------------------- //
// Gate 9, SOURCE-LEAK
// --------------------------------------------------------------------------- //
export function gateRoRiNguon({ duongDanHtml, cheDo = 'gui-di' }) {
  const ly_do = [];
  try {
    execFileSync('node', [path.join(THU_MUC, 'guard-source-leak.mjs'), duongDanHtml, `--mode=${cheDo === 'noi-bo' ? 'internal' : 'external'}`], {
      stdio: 'pipe',
    });
    ly_do.push(`guard-source-leak: sach (che do ${cheDo})`);
    return ghi('9. SOURCE-LEAK', 'PASS', ly_do);
  } catch (e) {
    const ra = (e.stdout ? e.stdout.toString() : '') + (e.stderr ? e.stderr.toString() : '');
    const dong = ra.split('\n').filter((l) => l.includes('x ') || l.includes('✗'));
    return ghi('9. SOURCE-LEAK', 'FAIL', dong.length ? dong.map((l) => l.trim()) : [ra.trim() || 'guard-source-leak FAIL']);
  }
}

// --------------------------------------------------------------------------- //
// Gate 10, LEDGER
// --------------------------------------------------------------------------- //
export function gateSoNguon({ html, duongDanHtml, cheDo = 'noi-bo' }) {
  if (!/<script[^>]*\bid=["']evidence-ledger["']/i.test(html)) {
    if (cheDo === 'gui-di') {
      return ghi('10. LEDGER', 'SKIP', [
        'ban gui di co y KHONG nhung so nguon, nen khong co gi de doi chieu o day. ' +
        'So nguon duoc kiem tren ban noi bo dung tu mot nguon noi dung',
      ]);
    }
    return ghi('10. LEDGER', 'FAIL', ['ban noi bo phai nhung <script id="evidence-ledger"> nhung khong thay']);
  }
  try {
    const ra = execFileSync('node', [path.join(THU_MUC, 'evidence-validator.mjs'), duongDanHtml], {
      stdio: 'pipe',
    }).toString();
    const canh = ra.split('\n').filter((l) => l.trim().startsWith('!')).map((l) => l.trim());
    return ghi('10. LEDGER', canh.length ? 'WARN' : 'PASS', canh.length ? canh : ['so nguon hop le, 0 loi']);
  } catch (e) {
    const ra = (e.stdout ? e.stdout.toString() : '') + (e.stderr ? e.stderr.toString() : '');
    const loi = ra.split('\n').filter((l) => l.trim().startsWith('✗')).map((l) => l.trim());
    return ghi('10. LEDGER', 'FAIL', loi.length ? loi : [ra.trim() || 'evidence-validator FAIL']);
  }
}

// --------------------------------------------------------------------------- //
// Chay ca bo
// --------------------------------------------------------------------------- //
export function docPdf(duongDanPdf) {
  const ra = execFileSync('python3', [path.join(THU_MUC, 'pdf_checks.py'), duongDanPdf], {
    maxBuffer: 1024 * 1024 * 128,
  });
  return JSON.parse(ra.toString());
}

export function chayTatCa({ duongDanHtml, duongDanPdf, cheDo = 'noi-bo', choPhepAnh = 0 }) {
  const html = fs.readFileSync(duongDanHtml, 'utf-8');
  const pdf = docPdf(duongDanPdf);
  const goi = { html, pdf, duongDanHtml, cheDo, choPhepAnh };
  return [
    gateFontHtml(goi),
    gateFontPdf(goi),
    gateRaster(goi),
    gateDau(goi),
    gateChartSong(goi),
    gateCalloutBaked(goi),
    gateVanPhong(goi),
    gateNgatTrang(goi),
    gateRoRiNguon(goi),
    gateSoNguon(goi),
  ];
}
