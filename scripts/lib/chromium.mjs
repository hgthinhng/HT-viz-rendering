/**
 * Nguon chan ly DUY NHAT cho chuyen "dung binary Chromium nao".
 *
 * Truoc ban nay repo co HAI cach chon binary chay song song:
 *   - verify-components.mjs tu doc ~/.cache/ms-playwright, loc thu muc
 *     "chromium-*", sort() roi reverse() lay ban moi nhat.
 *   - verify-illustrations.mjs va tests/smoke/deps.test.mjs hardcode
 *     "chromium-1228".
 * Hau qua: `npm run verify` nghiem thu bang HAI binary khac nhau trong cung
 * mot lan chay, va tren may sach (chi co ban Chromium moi) thi nhanh hardcode
 * chet ngay voi ENOENT.
 *
 * Ca hai cach deu sai theo mot kieu: chung doan xem playwright-core CAN ban
 * nao. playwright-core BIET dieu do, no co ham executablePath() tra ve dung
 * ban khop voi phien ban thu vien dang cai. Lay tu do thi khong the lech.
 *
 * Ghi chu ve sort(): cach cu con mot bay nua. sort() la so sanh CHUOI, nen
 * "chromium-999" > "chromium-1000" (ky tu '9' > '1'). Chua can vi Playwright
 * dang o moc 1200, nhung day la mot cach chon sai am tham. Ban nay khong con
 * sort nen bay do bien mat luon.
 */
import { chromium } from 'playwright-core';
import fs from 'node:fs';

const HUONG_DAN_CAI = 'Chua co Chromium. Chay: npm run setup:browser';

/**
 * Tra ve duong dan binary Chromium se dung.
 * @param {string} [explicit] duong dan nguoi dung truyen tay (--chromium=...)
 */
export function chromiumExecutablePath(explicit) {
  if (explicit) return explicit;
  return chromium.executablePath();
}

/**
 * Kiem tra binary co that tren dia khong. Tra ve { ok, path, message }.
 * Tach rieng khoi launch de goi duoc trong test ma khong phai mo browser.
 */
export function kiemTraChromium(explicit) {
  let p;
  try {
    p = chromiumExecutablePath(explicit);
  } catch (e) {
    return { ok: false, path: null, message: `${HUONG_DAN_CAI} (${e.message})` };
  }
  if (!p || !fs.existsSync(p)) {
    return {
      ok: false,
      path: p,
      message: explicit
        ? `Khong tim thay Chromium tai duong dan truyen tay: ${p}`
        : `${HUONG_DAN_CAI}\n  (playwright-core tro toi ${p}, file khong ton tai)`,
    };
  }
  return { ok: true, path: p, message: '' };
}

/**
 * Mo Chromium. Neu thieu binary thi bao loi kem lenh cai, khong de ENOENT
 * tho cua Node bay ra ngoai, vi thong diep goc ("spawn ENOENT") khong noi
 * cho nguoi chay biet phai lam gi.
 *
 * @param {object} [opts]
 * @param {string} [opts.executablePath] duong dan truyen tay
 * @param {(msg: string) => never} [opts.onMissing] xu ly khi thieu binary
 *        (mac dinh: in stderr roi process.exit(2))
 */
export async function launchChromium(opts = {}) {
  const { executablePath, onMissing, ...rest } = opts;
  const kiem = kiemTraChromium(executablePath);
  if (!kiem.ok) {
    if (onMissing) return onMissing(kiem.message);
    console.error(kiem.message);
    process.exit(2);
  }
  return chromium.launch({ executablePath: kiem.path, headless: true, ...rest });
}
