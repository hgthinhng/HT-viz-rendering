// 01-cau-gia-thanh.mjs, cau noi tu gia ban mot tan xi mang toi loi nhuan mot tan.
//
// Day la CHART CUA BAO CAO, khong phai preset cua thu vien. Preset trong
// charts/echarts/ la y tham khao; bao cao chep lay bo cuc roi thay du lieu that cua
// minh. Cach nay giu duoc mot dieu quan trong: du lieu cua bao cao nam trong thu muc
// bao cao, doc duoc, sua duoc, khong an trong mot preset dung chung.
//
// Moi so o day la so MINH HOA, xem examples/mau-phase2/so-nguon.json.
import * as echarts from 'echarts';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { baseOption, valueAxis, categoryAxis, PALETTE, TYPOGRAPHY } from '../../../charts/echarts/theme.mjs';
import { fmtNumber } from '../../../charts/echarts/fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi } from '../../../charts/echarts/schema.mjs';

const KY = { type: 'nam', year: 2025, end: '2025-12-31' };

const series = {
  unit: 'nghin_dong_tan',
  source: { tier: 'uoc-tinh', label: 'Số minh hoạ cho mẫu kỹ thuật' },
  as_of: '2026-08-01',
  direction: 'cao_tot',
  kind: 'luy_ke_ky',
  // Waterfall khong phai chuoi thoi gian: moi hang la mot HANG MUC trong cung mot ky,
  // nen `entity` mang ten hang muc con `period` giong nhau o moi hang.
  rows: [
    { value: 1180, entity: { code: 'Giá bán' }, period: KY },
    { value: -342, entity: { code: 'Than' }, period: KY },
    { value: -196, entity: { code: 'Điện' }, period: KY },
    { value: -274, entity: { code: 'Nguyên liệu' }, period: KY },
    { value: -220, entity: { code: 'Chi phí khác' }, period: KY },
    { value: 148, entity: { code: 'Lợi nhuận' }, period: KY },
  ],
};
validateSeries(series);
const decimals = soThapPhan(series);
const donVi = nhanDonVi(series.unit);

// Nhan truc lay tu `entity.code`, tuc rut gon o TANG DU LIEU chu khong boc dong o
// tang hien thi. Ban dau dung ten day du ("Khau hao, nhan cong, ban hang") thi ECharts
// tu an bot nhan cho khoi chong nhau, va tren ban PDF chi con hai nhan dau cuoi. Ten
// day du cua tung hang muc nam trong chu thich hinh, la cho co du cho.
const hangMuc = series.rows.map((r) => r.entity.code);
const giaTri = series.rows.map((r) => r.value);
// Moc tuyet doi la hang dau va hang cuoi; giua la cac khoan tru dan.
const laMoc = giaTri.map((_, i) => i === 0 || i === giaTri.length - 1);

// Tang do dem cua waterfall: chieu cao khoi trong suot ben duoi moi cot.
const dem = [];
const duong = [];
const am = [];
let chay = 0;
giaTri.forEach((v, i) => {
  if (laMoc[i]) {
    dem.push(0);
    duong.push(i === 0 ? v : chay);
    am.push('-');
    chay = i === 0 ? v : chay;
  } else if (v >= 0) {
    dem.push(chay);
    duong.push(v);
    am.push('-');
    chay += v;
  } else {
    chay += v;
    dem.push(chay);
    duong.push('-');
    am.push(-v);
  }
});

const W = 760;
const H = 430;
const chart = echarts.init(null, null, { renderer: 'svg', ssr: true, width: W, height: H });

chart.setOption({
  ...baseOption({
    title: 'Điện và than nuốt gần một nửa giá bán mỗi tấn',
    subtitle: `Cầu nối từ giá bán tới lợi nhuận trước thuế, ${donVi}, năm 2025`,
    width: W,
    height: H,
  }),
  // interval 0 ep hien DU sau nhan. ECharts mac dinh an bot nhan khi nghi chung
  // chong nhau, va tren ban PDF dau tien chi con ba tren sau nhan, khong bao loi.
  xAxis: categoryAxis(hangMuc, { axisLabel: { interval: 0 } }),
  // KHONG khai `name` cho truc gia tri: ten truc duoc dat o dinh truc, dung cho ma
  // `title.subtext` dang chiem, nen hai chuoi de len nhau. Da nhin tan mat o ban dau.
  // Don vi thuoc ve phu de, khong lap lai o ten truc.
  yAxis: valueAxis({}),
  // Chuoi "Dem" la khoi trong suot de day cot len dung cao do, khong phai du lieu.
  // No khong duoc xuat hien trong chu giai.
  legend: { data: ['Mốc và khoản cộng', 'Khoản trừ'] },
  series: [
    {
      name: 'Đệm',
      type: 'bar',
      stack: 'tong',
      itemStyle: { borderColor: 'transparent', color: 'transparent' },
      emphasis: { itemStyle: { borderColor: 'transparent', color: 'transparent' } },
      data: dem,
      silent: true,
    },
    {
      name: 'Mốc và khoản cộng',
      type: 'bar',
      stack: 'tong',
      barWidth: 46,
      itemStyle: {
        color: (p) => (laMoc[p.dataIndex] ? PALETTE.accent : PALETTE.accentSoft),
      },
      data: duong,
      label: {
        show: true,
        position: 'top',
        formatter: (p) => fmtNumber(p.value, { decimals }),
        ...TYPOGRAPHY.dataLabel,
      },
    },
    {
      name: 'Khoản trừ',
      type: 'bar',
      stack: 'tong',
      barWidth: 46,
      itemStyle: { color: PALETTE.negative },
      data: am,
      label: {
        show: true,
        position: 'bottom',
        formatter: (p) => '-' + fmtNumber(p.value, { decimals }),
        ...TYPOGRAPHY.dataLabel,
      },
    },
  ],
});

const svg = chart.renderToSVGString();
const raDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)));
fs.writeFileSync(path.join(raDir, 'ra-01-cau-gia-thanh.svg'), svg);
console.log('01-cau-gia-thanh: OK,', svg.length, 'bytes');

chart.dispose();
process.exit(0);
