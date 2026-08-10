#!/usr/bin/env node
// Tai nghiem thu MOI exemplar chinh-thuc: chay lai orchestrator + gate, ghi de
// nghiem-thu.json. Ngoai npm test (cham); chay truoc merge lon va sau khi doi
// gate, token, font.
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
// Duyet tu phong-cach.json (nguon) chu khong tu INDEX (INDEX ha cap khi thieu
// nghiem-thu, ma muc dich cua script nay chinh la sinh nghiem-thu).
const pcDir = path.join(REPO, 'phong-cach');
let loi = 0;
let soChay = 0;

for (const slug of fs.readdirSync(pcDir)) {
  const f = path.join(pcDir, slug, 'phong-cach.json');
  if (!fs.existsSync(f)) continue;
  const pc = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (pc.trang_thai !== 'chinh-thuc' || !pc.exemplar) continue;
  soChay += 1;

  const baoCao = path.join(REPO, pc.exemplar);
  const lan = fs.existsSync(path.join(baoCao, 'nghiem-thu.json'))
    ? JSON.parse(fs.readFileSync(path.join(baoCao, 'nghiem-thu.json'), 'utf8')).lan
    : 'html-song';
  const lenhOrch = `python3 pipeline/orchestrator.py ${pc.exemplar}/noi-dung.md --lan=${lan}`;
  console.log(`\n=== ${slug} (${lan}) ===\n$ ${lenhOrch}`);
  try {
    execSync(lenhOrch, { cwd: REPO, stdio: 'inherit' });

    // orchestrator.py dat ten artifact theo `<stem-cua-noi-dung.md>-gui-di.html`.
    // Doc lai tu thu muc ra/ thay vi doan cung 'noi-dung-gui-di.html', vi mot
    // exemplar sau nay co the dat ten file nguon khac 'noi-dung.md'.
    const tenFile = fs.readdirSync(path.join(baoCao, 'ra')).find((x) => x.endsWith('-gui-di.html'));
    if (!tenFile) throw new Error(`khong tim thay *-gui-di.html trong ${baoCao}/ra sau khi dung`);
    const ten = path.basename(tenFile, '.html');
    const html = path.join(baoCao, 'ra', `${ten}.html`);
    const pdf = path.join(baoCao, 'ra', `${ten}.pdf`);
    // Lan html-song khong xuat PDF (xem orchestrator.py: buoc CK3 bo han o lan
    // nay), nen gates/run.mjs chi nhan mot minh file HTML voi --lan=html-song.
    const viTri = lan === 'html-song' ? `"${html}" --lan=html-song` : `"${html}" "${pdf}" --che-do=gui-di`;
    execSync(
      `node gates/run.mjs ${viTri} --ghi-nghiem-thu="${path.join(baoCao, 'nghiem-thu.json')}" --lenh-tai-tao="${lenhOrch}"`,
      { cwd: REPO, stdio: 'inherit' },
    );
  } catch (e) {
    loi += 1;
    console.error(`FAIL: ${slug}`);
    console.error(e.message);
  }
}

if (soChay === 0) {
  console.log('Khong co style nao o trang_thai chinh-thuc, khong co gi de nghiem thu.');
}

execSync('node phong-cach/sinh-index.mjs', { cwd: REPO, stdio: 'inherit' });
process.exit(loi ? 1 : 0);
