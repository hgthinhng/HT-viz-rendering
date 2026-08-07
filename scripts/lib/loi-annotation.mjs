/**
 * loi-annotation.mjs, quyet dinh mot loi JavaScript co phai loi cua LOP ANNOTATION
 * hay khong.
 *
 * Tach rieng khoi `verify-illustrations.mjs` vi file do chay top-level va mo Chromium
 * ngay khi import, nen khong test truc tiep duoc. Phep phan loai thi phai test duoc:
 * no quyet dinh quy loi cho ai, va quy nhan sai chu the loi la kieu bao cao te nhat.
 *
 * ## Vi sao khong con dung `/\bannotate\b/i` tren ca khoi stack
 *
 * Phia network da so basename CHINH XAC tu lau: mot request hong toi
 * `annotated-source-badge.png` khong bi tinh la loi cua `annotate.js`. Phia pageerror
 * thi van quet chuoi con theo ranh gioi tu, va `\bannotate\b` khop CA nhung thu khong
 * lien quan, vi dau gach noi va dau cham deu la ranh gioi tu:
 *
 *   "at f (file:///.../annotate-demo.js:3:1)"     -> khop, nhung day la file khac
 *   "at f (file:///.../annotated-source.js:3:1)"  -> KHONG khop (chu con), dung
 *   "TypeError: annotate is not a function"       -> khop, va day la bien cua ai cung duoc
 *
 * Ban nay lam dung cai phia network dang lam: trich duong dan file tu tung frame cua
 * stack roi so BASENAME voi danh sach tai nguyen annotation. Cong them mot duong rieng
 * cho `Annotate` viet hoa, la ten global that cua thu vien: loi
 * "ReferenceError: Annotate is not defined" phat sinh ngay trong the <script> cua trang
 * nen stack tro toi file .html, khong tro toi annotate.js, va do dung la ca can bat.
 */

export const TEN_TAI_NGUYEN_ANNOTATION = ['annotate.js', 'annotate.css'];

/** Basename cua mot URL hoac duong dan, da bo query va hash. */
export function basename(url) {
  return String(url).split(/[\\/]/).pop().split(/[?#]/)[0];
}

/** URL nay co tro dung mot tai nguyen cua lop annotation khong. */
export function laTaiNguyenAnnotation(url) {
  return TEN_TAI_NGUYEN_ANNOTATION.includes(basename(url));
}

// Duong dan file trong mot frame stack. Bat ca dang `file:///...` lan duong dan tuyet
// doi tran, dung lai truoc so dong va so cot.
const RE_FRAME = /(?:file:\/\/)?\/[^\s():]*\.(?:js|mjs|cjs)/g;

// Ten global THAT cua thu vien, viet hoa chu A. Dung `Annotate` chu khong dung
// `annotate` thuong: chu thuong la ten ham noi bo ma bat ky file nao cung co the dat.
const RE_DINH_DANH_GLOBAL = /\bAnnotate\b/;

/**
 * Trich basename cua moi file .js xuat hien trong stack.
 * @param {string} full message cong stack
 */
export function fileTrongStack(full) {
  return [...String(full).matchAll(RE_FRAME)].map((m) => basename(m[0]));
}

/**
 * Loi nay co phai cua lop annotation khong, va vi sao.
 * @returns {{lienQuan: boolean, lyDo: string}}
 */
export function phanLoaiLoi(full) {
  const s = String(full);
  const files = fileTrongStack(s);
  const khop = files.filter((f) => TEN_TAI_NGUYEN_ANNOTATION.includes(f));
  if (khop.length) {
    return { lienQuan: true, lyDo: `stack co frame trong ${[...new Set(khop)].join(', ')}` };
  }
  if (RE_DINH_DANH_GLOBAL.test(s)) {
    return { lienQuan: true, lyDo: 'loi nhac ten global Annotate' };
  }
  return {
    lienQuan: false,
    lyDo: files.length
      ? `stack chi tro toi ${[...new Set(files)].join(', ')}, khong file nao thuoc lop annotation`
      : 'khong co frame nao tro toi file cua lop annotation',
  };
}
