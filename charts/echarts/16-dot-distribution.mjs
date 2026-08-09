// 16-dot-distribution.mjs, Dot strip phân phối: thay boxplot khi n nhỏ, không giấu cỡ mẫu
// Dùng khi: cần thấy HÌNH DẠNG phân phối 1 chỉ tiêu (vd P/E) của 1-3 nhóm nhỏ (n~5-25),
// và việc thấy TỪNG ĐIỂM (không phải chỉ quartile tóm tắt) quan trọng vì n nhỏ.
// KHÔNG dùng khi: n>30-40 (chồng điểm dù jitter -> histogram matplotlib); cần quartile
// chính xác bằng số (boxplot matplotlib); >3-4 nhóm (07-small-multiples).
//
// LƯU Ý VỀ SCHEMA THẬT (charts/echarts/schema.mjs), khác bản nháp trong đặc tả gốc ở BA
// điểm giống 15-quadrant-scatter.mjs (xem đầu file đó để biết lý do): unit/source nằm ở
// cấp series; entity.code không ép viết hoa không dấu; số thập phân lấy từ
// soThapPhan(series). Ở preset này từng điểm KHÔNG có entity.code riêng -- đúng bản chất
// "1 chấm = 1 mã ẩn danh" của thiết kế gốc (chỉ có tooltip theo NHÓM, không có tên thực thể
// nào cần giữ), entity là field TUỲ CHỌN trong schema nên bỏ hẳn không bịa mã giả cho từng
// điểm.
//
// Dữ liệu cần: nhóm {name, values:number[]}. Bẫy: (1) random jitter mỗi lần render ra ảnh
// khác nhau -> dùng công thức TẤT ĐỊNH theo chỉ số sau khi sort; (2) tô ngoại lệ bằng màu
// cảnh báo (traffic-light) -> mã hoá bằng HÌNH DẠNG (viền rỗng), không phải màu; (3) quên
// vạch trung vị mỗi strip -> mắt không có mốc neo để so 2 nhóm.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtMultiple } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi, coCo } from './schema.mjs';

export const MAC_DINH = {
  groupNames: ['Thép', 'Xi măng', 'VLXD khác'],
  groupValues: [
    [8.2, 9.1, 7.5, 10.3, 8.8, 22.4, 9.6, 8.0, 9.9],
    [6.5, 7.2, 6.8, 15.9, 7.0, 6.3, 7.4],
    [11.2, 12.5, 10.8, 13.1, 11.9, 12.0, 34.6, 11.5],
  ], // P/E minh hoạ theo phân ngành, KHÔNG phải số thật. 22.4/15.9/34.6 CỐ Ý là ngoại lệ để thử
  trongTamIndex: 0, // chỉ số nhóm đang phân tích trong bài ('Thép'); còn lại là nhóm so sánh
};

function tinhKichThuoc(params) {
  return { width: 700, height: 60 * params.groupNames.length + 200 };
}

function median(arr) {
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}
function quartile(arr, q) {
  const s = [...arr].sort((a, b) => a - b);
  const pos = (s.length - 1) * q;
  const lo = Math.floor(pos), hi = Math.ceil(pos);
  return s[lo] + (s[hi] - s[lo]) * (pos - lo);
}
function isOutlier(v, arr) {
  const q1 = quartile(arr, 0.25), q3 = quartile(arr, 0.75), iqr = q3 - q1;
  return v < q1 - 1.5 * iqr || v > q3 + 1.5 * iqr;
}
// jitter TẤT ĐỊNH theo chỉ số sau khi sort trong nhóm, KHÔNG Math.random -> SVG tái lập y
// hệt mỗi lần chạy. Gate verify-charts.mjs KHÔNG tự bắt được nếu ai sau này đổi sang
// random (nó không diff nội dung SVG giữa 2 lần chạy), phải tự nhớ giữ tất định.
function jitter(i, band) {
  const dau = i % 2 === 0 ? 1 : -1;
  const doLon = ((i % 4) + 1) / 4;
  return dau * doLon * band * 0.32;
}

export function option(params) {
  const { groupNames, groupValues, trongTamIndex } = params;
  const { width: W, height: H } = tinhKichThuoc(params);

  // nhóm tai trongTamIndex la nhom dang phan tich trong bai, con lai la nhom so sanh,
  // danh dau bang coCo() theo CHI SO NGUYEN chu khong so gia tri.
  const laTrongTam = coCo(trongTamIndex, groupNames.length);

  const series = {
    unit: 'lan',
    source: { tier: 'uoc-tinh', label: 'Minh hoạ, không phải số thật' },
    as_of: '2026-08-07',
    direction: 'trung_tinh', // P/E không có chiều tốt/xấu tự thân, phụ thuộc tăng trưởng đi kèm
    kind: 'ty_le',
    decimals: 1,
    rows: groupValues.flatMap((values, gi) => values.map((value) => ({
      value,
      role: laTrongTam(gi) ? 'chinh' : 'so_sanh',
    }))),
  };
  validateSeries(series); // FAIL ngay nếu unit/tier bịa hoặc role bịa
  const decimals = soThapPhan(series);

  const bandHeight = 60;
  const points = [];
  groupNames.forEach((name, gi) => {
    const values = groupValues[gi];
    const sorted = [...values].sort((a, b) => a - b);
    sorted.forEach((v, i) => {
      points.push({
        group: name, gi, value: v,
        y: gi + jitter(i, 0.42) / bandHeight,
        outlier: isOutlier(v, values),
        chinh: laTrongTam(gi),
      });
    });
  });

  return {
    ...baseOption({
      title: 'Phân phối P/E theo phân ngành',
      subtitle: `Đơn vị: ${nhanDonVi(series.unit)}. Mỗi chấm = 1 mã, vòng rỗng = ngoại lệ ngoài 1,5 lần IQR, minh hoạ`,
      width: W, height: H,
    }),
    tooltip: {
      // scatter toạ độ đã jitter, KHÔNG hợp với axisPointer shadow của tooltipDefault
      // (trigger:'axis' dành cho category axis đơn giản), nên khai riêng trigger:'item'.
      trigger: 'item',
      textStyle: { fontFamily: FONT_STACK, fontSize: 12 },
      // p.data.value là cặp [x,y] đã jitter (x = P/E thật, y = vị trí dọc trong dải), lấy
      // value[0] chứ không phải value nguyên khối, nếu không fmtMultiple() nhận mảng ra NaN.
      formatter: (p) => `${p.data.group}: ${fmtMultiple(p.data.value[0], { decimals })}${p.data.outlier ? ' (ngoại lệ)' : ''}`,
    },
    legend: { show: false },
    grid: { left: 100, right: 40, top: 70, bottom: 80 },
    xAxis: {
      type: 'value', min: 0,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtMultiple(v, { decimals }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    yAxis: {
      type: 'category', data: groupNames, inverse: true,
      axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel,
    },
    series: [
      {
        name: 'Trung vị', type: 'custom', z: 2, silent: true,
        renderItem: (itemParams, api) => {
          const gi = itemParams.dataIndex;
          const med = median(groupValues[gi]);
          const y = api.coord([0, gi])[1];
          const x = api.coord([med, gi])[0];
          // vạch median của nhóm trọng tâm dày hơn (3px so với 1.5px), cùng 1 màu ink,
          // phân biệt bằng ĐỘ DÀY chứ không phải màu cảnh báo.
          return { type: 'line', shape: { x1: x, y1: y - 20, x2: x, y2: y + 20 }, style: { stroke: PALETTE.ink, lineWidth: laTrongTam(gi) ? 3 : 1.5 } };
        },
        data: groupNames.map((_, i) => [0, i]),
      },
      {
        name: 'Mã bình thường', type: 'scatter', z: 3, symbolSize: 9,
        itemStyle: { color: PALETTE.accent, opacity: 0.85 },
        // ...p PHẢI đứng TRƯỚC value:[...]: p tự nó đã có field "value" (số P/E vô hướng
        // dùng để tính median/outlier), nếu spread ...p SAU thì nó đè mất value:[x,y] vừa
        // gán bằng lại số vô hướng, ECharts sẽ không vẽ đúng toạ độ 2 chiều. Đã bắt lỗi này
        // bằng thực nghiệm: bản đầu chỉ ra 3/20 điểm bình thường trên ảnh render thật.
        data: points.filter((p) => !p.outlier).map((p) => ({ ...p, value: [p.value, p.y] })),
      },
      {
        name: 'Ngoại lệ', type: 'scatter', z: 4, symbolSize: 11,
        // mã hoá HÌNH DẠNG (viền rỗng), không phải màu cảnh báo
        itemStyle: { color: PALETTE.paper, borderColor: PALETTE.ink, borderWidth: 2 },
        data: points.filter((p) => p.outlier).map((p) => ({ ...p, value: [p.value, p.y] })),
        label: { show: true, formatter: (p) => fmtMultiple(p.data.value[0], { decimals }), position: 'top', ...TYPOGRAPHY.dataLabel },
      },
    ],
    graphic: [
      { type: 'text', left: 16, top: H - 46, style: { text: '○ viền đậm = ngoại lệ (ngoài 1,5 lần IQR). Vạch median đậm hơn = Thép, nhóm đang phân tích, 2 nhóm còn lại là nhóm so sánh.', font: `9px ${FONT_STACK}`, fill: PALETTE.inkLo } },
    ],
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  // `render-static.mjs` keo ca goi ECharts vao, nen import TINH o dinh file lam
  // bundle lan `html-song` mat sach tree-shaking va keo ban day du 1,1MB. Import
  // DONG ngay trong nhanh CLI: duong tinh van chay y het, con trinh duyet khong
  // bao gio cham toi module nay.
  const { renderStatic } = await import('./render-static.mjs');
  const { writeFileSync } = await import('node:fs');
  const { width, height } = tinhKichThuoc(MAC_DINH);
  const svg = renderStatic(option, MAC_DINH, { width, height });
  writeFileSync(new URL('./out-16-dot-distribution.svg', import.meta.url), svg);
  console.log('16-dot-distribution: OK,', svg.length, 'bytes, image?', svg.includes('<image'));
  process.exit(0);
}
