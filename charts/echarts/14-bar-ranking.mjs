// 14-bar-ranking.mjs, Bar ngang xếp hạng + biến thể Cleveland dot cho khổ hẹp
// Dùng khi: xếp hạng N hạng mục theo 1 chỉ tiêu, vị trí quan trọng hơn giá trị tuyệt đối.
// KHÔNG dùng khi: so 2 mốc thời gian (04-dumbbell/05-slope); mục đích là cơ cấu %
// (11-stacked-100); >15-18 hạng mục (lọc top-N + "khác").
// Dữ liệu cần: series schema dùng chung (charts/echarts/schema.mjs), rows là
// {entity:{code,name}, value}[]. RÀNG BUỘC CỨNG: mọi hàng trong 1 lượt xếp hạng phải
// CÙNG 1 unit -- validateSeries() ép ở runtime (đơn vị nằm ở cấp series nên tự động
// đồng nhất, không cần kiểm tay), xếp hạng khác đơn vị vô nghĩa như radar (CLAUDE.md
// cấm radar). RÀNG BUỘC CỨNG THỨ HAI: nhãn trục = entity.code, rút gọn Ở TẦNG DỮ LIỆU
// lúc nhập (schema.mjs ép tối đa 24 ký tự, giữ dấu tiếng Việt, KHÔNG ép viết hoa không
// dấu -- "Bán lẻ" hợp lệ y như "VCB"). entity.name đầy đủ CHỈ ở tooltip + 1 dòng chú
// giải dưới chart, không dùng wrapLabel()/truncate cho nhãn TRÊN TRỤC vì thuật toán
// chống-đè-nhãn của ECharts hoạt động kém với chuỗi dài có dấu tiếng Việt.
// Bẫy khác: (1) không sort giảm dần; (2) trục giá trị không từ 0 (ràng buộc cứng cho CẢ
// HAI biến thể: dot vẫn vẽ đường nối 0->value, tức vẫn mã hoá bằng ĐỘ DÀI như bar, không
// phải scatter thuần vị trí); (3) quên yAxis.inverse:true -- ECharts mặc định đặt
// categories[0] ở ĐÁY, nếu thiếu dòng này hạng 1 sẽ rơi xuống đáy thay vì đỉnh (đã xác
// nhận và vá đúng lớp bug này ở 04-dumbbell.mjs/06-tornado.mjs).
//
// PRESET NAY XUAT HAI BIEN THE tu 1 nguon du lieu (bar ngang kho rong / Cleveland dot
// kho hep), khac 17 preset con lai chi xuat 1 SVG. Tham so hoa bang `params.bienThe`
// ('bar' | 'dot', mac dinh 'bar' qua MAC_DINH.bienThe) thay vi 2 ham option() rieng, vi
// hop dong "1 preset = 1 cap {option, MAC_DINH}" cua registry.mjs khong co cho cho preset
// da-bien-the. CLI tail goi option() HAI LAN voi bienThe khac nhau de giu nguyen ca hai
// file ra out-14-bar-ranking.svg va out-14-bar-ranking-dot.svg nhu truoc khi tach.
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK, tooltipDefault } from './theme.mjs';
import { fmtPercent } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi } from './schema.mjs';
import { renderStatic } from './render-static.mjs';

// % biên lợi nhuận gộp minh hoạ theo phân khúc, KHÔNG phải số thật. entity.code là
// tên rút gọn NGẮN, giữ dấu tiếng Việt (không phải mã tự chế viết hoa không dấu) --
// tránh dùng "TCTD" cho "tài chính tiêu dùng" vì đó là viết tắt chuẩn của "tổ chức tín
// dụng" trong tiếng Việt tài chính, dùng lại sẽ gây hiểu nhầm.
export const MAC_DINH = {
  series: {
    unit: 'phan_tram',
    source: { tier: 'uoc-tinh', label: 'Minh hoạ theo phân khúc, không phải số thật' },
    as_of: '2026-08-07',
    direction: 'cao_tot',
    kind: 'ty_le',
    rows: [
      { entity: { code: 'NLTT', name: 'Năng lượng tái tạo' }, value: 33.0 },
      { entity: { code: 'CNTT', name: 'Công nghệ thông tin' }, value: 24.6 },
      { entity: { code: 'Dược & YT', name: 'Dược phẩm & bán lẻ y tế' }, value: 21.3 },
      { entity: { code: 'Bán lẻ', name: 'Bán lẻ tiêu dùng nhanh' }, value: 18.7 },
      { entity: { code: 'VLXD', name: 'Vật liệu xây dựng' }, value: 15.4 },
      { entity: { code: 'TC tiêu dùng', name: 'Tài chính tiêu dùng' }, value: 13.9 },
      { entity: { code: 'BĐS KCN', name: 'Bất động sản khu công nghiệp' }, value: 12.1 },
      { entity: { code: 'Logistics', name: 'Logistics & vận tải biển' }, value: 9.8 },
    ],
  },
  bienThe: 'bar', // 'bar' | 'dot'
};

const LEGEND_SEP = ' · ';
function chunkEntries(entries, maxCharsPerLine) {
  const lines = [];
  let cur = [];
  let curLen = 0;
  entries.forEach((entry) => {
    const addLen = entry.length + (cur.length ? LEGEND_SEP.length : 0);
    if (cur.length && curLen + addLen > maxCharsPerLine) {
      lines.push(cur.join(LEGEND_SEP));
      cur = [entry];
      curLen = entry.length;
    } else {
      cur.push(entry);
      curLen += addLen;
    }
  });
  if (cur.length) lines.push(cur.join(LEGEND_SEP));
  return lines;
}
function legendGraphic(lines, { left, top, lineHeight = 12, fontSize = 9 }) {
  return lines.map((line, li) => ({
    type: 'text', left, top: top + li * lineHeight,
    style: { text: line, font: `${fontSize}px ${FONT_STACK}`, fill: PALETTE.inkLo },
  }));
}

/** Kich thuoc canvas phu thuoc SO LUONG hang VA bien the (chu giai xuong dong khac nhau
 * giua kho rong/kho hep) -- CLI tail va option() dung CHUNG ham nay de khong lech nhau. */
export function kichThuoc(params) {
  const { series, bienThe = 'bar' } = params;
  const legendEntries = series.rows.map((r) => `${r.entity.code}=${r.entity.name}`);
  if (bienThe === 'dot') {
    const legendLines = chunkEntries(legendEntries, 40);
    return { width: 380, height: 400 + (legendLines.length * 12 + 8) };
  }
  const legendLines = chunkEntries(legendEntries, 92);
  return { width: 700, height: 380 + (legendLines.length * 12 + 8) };
}

export function option(params) {
  const { series, bienThe = 'bar' } = params;
  validateSeries(series); // FAIL ngay nếu entity.code quá dài hoặc thiếu unit/source
  const rows = [...series.rows].sort((a, b) => b.value - a.value); // sort giảm dần: hạng 1 ở index 0
  const decimals = soThapPhan(series); // 1 cho 'phan_tram', không tự chọn ở đây
  const donVi = nhanDonVi(series.unit);

  // dòng chú giải "mã = tên", vì bản PDF không có hover -- annotation-first, không dựa
  // hover. Tổng chuỗi có thể vượt bề rộng canvas nên PHẢI gói dòng theo TỪNG CẶP mã=tên
  // nguyên vẹn (không cắt giữa một cặp), khác wrapLabel() của fmt.mjs vốn gói theo TỪ.
  const legendEntries = rows.map((r) => `${r.entity.code}=${r.entity.name}`);

  // axisDecimals/splitNumber CHỈ chi phối nhãn MỐC TRỤC (đọc thoáng ở khổ hẹp), không
  // đụng tới decimals của nhãn dữ liệu/tooltip -- cái đó luôn lấy từ soThapPhan(series)
  // theo đúng ràng buộc cứng, không tự chọn. Tiền lệ đã có ở 04-dumbbell.mjs (trục dùng
  // decimals:0 dù dữ liệu decimals:1).
  function buildValueAxis({ axisDecimals = decimals, splitNumber } = {}) {
    return {
      type: 'value', min: 0, splitNumber,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtPercent(v, { decimals: axisDecimals }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    };
  }

  const { width: W, height: H } = kichThuoc(params);

  if (bienThe === 'dot') {
    // --- Biến thể 2: Cleveland dot, khổ hẹp (vd cột phụ A4) ---
    const legendLines = chunkEntries(legendEntries, 40);
    const legendH = legendLines.length * 12 + 8;
    return {
      ...baseOption({ title: 'Xếp hạng biên lợi nhuận gộp', subtitle: `${donVi}, khổ hẹp`, width: W, height: H }),
      tooltip: { ...tooltipDefault, formatter: (p) => `${rows[p.dataIndex].entity.name}: ${fmtPercent(p.value, { decimals })}` },
      legend: { show: false },
      grid: { left: 96, right: 40, top: 60, bottom: 30 + legendH },
      // khổ hẹp 380px: full decimals + 8 mốc dính chữ liền nhau không đọc được (đã bắt
      // được bằng ảnh chụp) -- rút còn ~4 mốc, bỏ số thập phân trên NHÃN TRỤC.
      xAxis: buildValueAxis({ axisDecimals: 0, splitNumber: 3 }),
      yAxis: { type: 'category', data: rows.map((r) => r.entity.code), inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
      series: [
        {
          name: 'Đường nối', type: 'custom', z: 1, silent: true,
          renderItem: (itemParams, api) => {
            const y = api.coord([0, itemParams.dataIndex])[1];
            const x0 = api.coord([0, itemParams.dataIndex])[0];
            const x1 = api.coord([api.value(1), itemParams.dataIndex])[0];
            return { type: 'line', shape: { x1: x0, y1: y, x2: x1, y2: y }, style: { stroke: PALETTE.inkLo, lineWidth: 1.5 } };
          },
          data: rows.map((r) => [0, r.value]),
        },
        {
          name: 'Giá trị', type: 'scatter', symbolSize: 11, z: 3,
          itemStyle: { color: PALETTE.accent },
          data: rows.map((r) => r.value),
          label: { show: true, position: 'right', formatter: (p) => fmtPercent(p.value, { decimals }), ...TYPOGRAPHY.dataLabel },
        },
      ],
      graphic: legendGraphic(legendLines, { left: 16, top: H - legendH - 4 }),
    };
  }

  // --- Biến thể 1 (mac dinh): bar ngang, khổ rộng ---
  const legendLines = chunkEntries(legendEntries, 92);
  const legendH = legendLines.length * 12 + 8;
  return {
    ...baseOption({ title: 'Xếp hạng biên lợi nhuận gộp theo phân khúc', subtitle: `Đơn vị: ${donVi}, sắp giảm dần, minh hoạ FY2026, không phải số thật`, width: W, height: H }),
    tooltip: { ...tooltipDefault, formatter: (p) => `${rows[p.dataIndex].entity.name}: ${fmtPercent(p.value, { decimals })}` },
    legend: { show: false },
    grid: { left: 96, right: 50, top: 60, bottom: 40 + legendH },
    xAxis: buildValueAxis(),
    // index 0 (hạng 1) phải render ở ĐỈNH -> inverse:true, GIỮ NGUYÊN thứ tự mảng đã sort
    yAxis: { type: 'category', data: rows.map((r) => r.entity.code), inverse: true, axisLine: { show: false }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    series: [{
      type: 'bar', barWidth: 20, itemStyle: { color: PALETTE.accent, borderRadius: [0, 3, 3, 0] },
      data: rows.map((r) => r.value),
      label: { show: true, position: 'right', formatter: (p) => fmtPercent(p.value, { decimals }), ...TYPOGRAPHY.dataLabel },
    }],
    graphic: legendGraphic(legendLines, { left: 16, top: H - legendH - 4 }),
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo: preset nay sinh HAI file,
// dung nguyen ten cu (khong doi ten) de gate/catalog hien co khong vo. `typeof process
// !== 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const parBar = { ...MAC_DINH, bienThe: 'bar' };
  const parDot = { ...MAC_DINH, bienThe: 'dot' };

  const svgBar = renderStatic(option, parBar, kichThuoc(parBar));
  writeFileSync(new URL('./out-14-bar-ranking.svg', import.meta.url), svgBar);
  console.log('14-bar-ranking (bar): OK,', svgBar.length, 'bytes, <image>?', svgBar.includes('<image'));

  const svgDot = renderStatic(option, parDot, kichThuoc(parDot));
  writeFileSync(new URL('./out-14-bar-ranking-dot.svg', import.meta.url), svgDot);
  console.log('14-bar-ranking (dot): OK,', svgDot.length, 'bytes, <image>?', svgDot.includes('<image'));

  process.exit(0);
}
