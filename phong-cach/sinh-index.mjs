#!/usr/bin/env node
// Sinh INDEX.json tu cac phong-cach.json. INDEX la BAN SINH, cam sua tay.
// Cung ky luat voi design-system/generate-tokens.mjs: mot nguon, mot generator,
// mot test drift. --kiem chi so sanh, khong ghi.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validatePhongCach } from './schema.mjs';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PC = path.join(REPO, 'phong-cach');

export function tinhIndex(repoRoot = REPO) {
  const pcDir = path.join(repoRoot, 'phong-cach');
  const danhSach = [];
  const themes = fs.readdirSync(path.join(repoRoot, 'design-system', 'themes'))
    .filter((f) => f.endsWith('.json')).map((f) => f.replace(/\.json$/, ''));
  const slugs = fs.readdirSync(pcDir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
    .map((d) => d.name).sort();
  for (const slug of slugs) {
    const duongDan = path.join(pcDir, slug, 'phong-cach.json');
    if (!fs.existsSync(duongDan)) continue;
    const obj = JSON.parse(fs.readFileSync(duongDan, 'utf8'));
    const kq = validatePhongCach(obj, { tenThuMuc: slug, danhSachChuDe: themes });
    if (!kq.hopLe) throw new Error(`phong-cach/${slug} khong qua schema: ${kq.loi.join('; ')}`);

    // trang_thai chinh-thuc phai co nghiem-thu.json hop le; thieu thi HA CAP,
    // khong loi: dang giua arc thi style dang dung o vuon-uom la trang thai that.
    let trangThai = obj.trang_thai;
    let lanDaChungMinh = [];
    if (obj.exemplar) {
      const ntPath = path.join(repoRoot, obj.exemplar, 'nghiem-thu.json');
      if (fs.existsSync(ntPath)) {
        const nt = JSON.parse(fs.readFileSync(ntPath, 'utf8'));
        const coFail = (nt.gate || []).some((g) => g.ket_qua === 'FAIL');
        if (!coFail && nt.lan) lanDaChungMinh = [nt.lan];
      }
    }
    if (trangThai === 'chinh-thuc' && lanDaChungMinh.length === 0) trangThai = 'vuon-uom';

    danhSach.push({
      slug: obj.slug,
      tagline: obj.tagline,
      mood: obj.mood,
      formality: obj.formality,
      density: obj.density,
      best_for: obj.best_for,
      avoid_for: obj.avoid_for,
      chu_de_mac_dinh: obj.chu_de_mac_dinh,
      trang_thai: trangThai,
      exemplar: obj.exemplar ?? null,
      lan_da_chung_minh: lanDaChungMinh,
    });
  }
  return { phien_ban: 2, sinh_boi: 'phong-cach/sinh-index.mjs', danh_sach: danhSach };
}

const laMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (laMain) {
  const ra = JSON.stringify(tinhIndex(), null, 2) + '\n';
  const dich = path.join(PC, 'INDEX.json');
  if (process.argv.includes('--kiem')) {
    const cu = fs.existsSync(dich) ? fs.readFileSync(dich, 'utf8') : '';
    if (cu !== ra) {
      console.error('INDEX.json lech ban tinh lai. Chay: node phong-cach/sinh-index.mjs');
      process.exit(1);
    }
    console.log('INDEX.json khop nguon.');
  } else {
    fs.writeFileSync(dich, ra);
    console.log(`Da ghi ${dich} (${tinhIndex().danh_sach.length} style)`);
  }
}
