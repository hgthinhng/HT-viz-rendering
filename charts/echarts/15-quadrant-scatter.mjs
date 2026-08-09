// 15-quadrant-scatter.mjs, Scatter chia 4 phần tư: định vị nhóm so sánh trên 2 tiêu chí
// Dùng khi: cần thấy nhóm so sánh (ngân hàng, doanh nghiệp cùng ngành) phân bố thế nào
// trên 2 tiêu chí ĐỘC LẬP cùng lúc (vd P/B vs ROE), chia bởi đường trung vị thành 4 vùng
// đọc được bằng câu chữ, không chỉ bằng toạ độ.
// KHÔNG dùng khi: 2 trục tương quan mạnh (phần tư vô nghĩa); <5 điểm; cần bubble 3D.
//
// LƯU Ý VỀ SCHEMA THẬT (charts/echarts/schema.mjs) khác bản nháp trong đặc tả
// docs/specs/2026-08-07-echarts-preset-expansion.md mục 00 ở BA điểm, bản này làm theo
// schema THẬT đang chạy trong repo:
//   1) unit/source nằm ở CẤP SERIES (không phải từng hàng) -- xem validateSeries() bên
//      dưới, chính hàm đó tố giác unit là thuộc tính của LƯỢT XẾP HẠNG chứ không phải
//      của từng hàng.
//   2) entity.code KHÔNG bị ép viết hoa không dấu, chỉ ép NGẮN (tối đa MAX_CODE_LEN=24 ký
//      tự). Ở đây dùng mã chứng khoán thật (VCB, TCB...) vì đó đúng là entity.code chuẩn
//      hoá tự nhiên của thực thể này, không phải vì bị ép viết hoa.
//   3) số thập phân hiển thị lấy từ soThapPhan(series), không tự chọn số rời rạc trong
//      từng lời gọi fmtMultiple()/fmtPercent().
//
// 2 trục CỐ Ý khác đơn vị (P/B = "lần", ROE = "%") nên dựng HAI series riêng, mỗi series
// đúng MỘT unit -- KHÔNG vi phạm ràng buộc "cùng đơn vị" của 14-bar-ranking, ràng buộc đó
// chỉ áp cho xếp hạng chung 1 trục, không áp cho 2 trục độc lập của quadrant chart (đúng
// bản chất chart này).
//
// Đường chia phần tư = TRUNG VỊ của CHÍNH tập P/B và ROE đang vẽ, tính trong code (doctrine
// repo "baseline phải rút trong nhóm"), không hardcode mốc "trung bình ngành" từ nguồn khác.
//
// role 'chinh'/'so_sanh' đánh dấu ngân hàng đang phân tích (VCB, chỉ số 0) so với 8 mã còn
// lại trong nhóm so sánh, đánh dấu bằng coCo() theo CHỈ SỐ NGUYÊN chứ không so sánh giá
// trị -- đúng công dụng coCo() được viết ra: "trọng tâm bài viết" là quyết định của người
// viết báo cáo, không phải kết quả suy ra từ dữ liệu.
//
// Bẫy thường gặp: (1) tô nền góc "tốt" bằng accent -> traffic-light trá hình, CHỦ Ý không
// tô nền quadrant nào, chỉ ghi chú chữ trung tính; (2) nhãn entity.code chồng nhau khi 2
// điểm gần -> dùng labelLayout.moveOverlap (rút gọn code đã quyết Ở TẦNG DỮ LIỆU lúc nhập,
// không xử lý ở tầng hiển thị); (3) ép trục từ 0 -> scatter mã hoá VỊ TRÍ không phải ĐỘ
// DÀI, được miễn luật "từ 0" (tiền lệ đã có ở 09-candlestick.mjs cho trục giá OHLC).
import { baseOption, TYPOGRAPHY, PALETTE, FONT_STACK } from './theme.mjs';
import { fmtMultiple, fmtPercent, wrapLabel } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi, coCo, epDonVi } from './schema.mjs';

const W = 680, H = 660;

export const MAC_DINH = {
  entities: [
    { code: 'VCB', name: 'Ngân hàng TMCP Ngoại thương Việt Nam' },
    { code: 'TCB', name: 'Ngân hàng TMCP Kỹ thương Việt Nam' },
    { code: 'MBB', name: 'Ngân hàng TMCP Quân đội' },
    { code: 'ACB', name: 'Ngân hàng TMCP Á Châu' },
    { code: 'VPB', name: 'Ngân hàng TMCP Việt Nam Thịnh Vượng' },
    { code: 'STB', name: 'Ngân hàng TMCP Sài Gòn Thương Tín' },
    { code: 'HDB', name: 'Ngân hàng TMCP Phát triển TP.HCM' },
    { code: 'TPB', name: 'Ngân hàng TMCP Tiên Phong' },
    { code: 'VIB', name: 'Ngân hàng TMCP Quốc tế Việt Nam' },
  ], // 9 ngân hàng niêm yết thật, GIÁ TRỊ dưới đây minh hoạ, KHÔNG phải số thật
  pbValues: [2.8, 1.1, 1.0, 1.5, 1.0, 1.3, 1.4, 0.9, 1.6], // lần, cùng thứ tự entities
  roeValues: [19.8, 14.5, 20.1, 23.0, 11.2, 16.5, 21.5, 14.0, 22.0], // %, cùng thứ tự entities
  trongTamIndex: 0, // chỉ số entity đang phân tích trong bài (VCB); phần còn lại là nhóm so sánh
  // Khoi meta BAT BUOC. Hai truc, hai don vi, nen hai khoi.
  meta: {
    pb: {
      unit: 'lan',
      source: { tier: 'uoc-tinh', label: 'Minh hoạ, không phải số thật' },
      as_of: '2026-08-07',
      direction: 'trung_tinh', // định giá không có chiều tốt/xấu tự thân, phụ thuộc ROE đi kèm
      kind: 'ty_le',
      decimals: 1,
    },
    roe: {
      unit: 'phan_tram',
      source: { tier: 'uoc-tinh', label: 'Minh hoạ, không phải số thật' },
      as_of: '2026-08-07',
      direction: 'cao_tot',
      kind: 'ty_le',
      decimals: 1,
    },
  },
};

export function option(params) {
  const { entities, pbValues, roeValues, trongTamIndex , meta} = params;

  // entity tai trongTamIndex la ngan hang dang phan tich trong bai, con lai la nhom so sanh.
  const laTrongTam = coCo(trongTamIndex, entities.length);
  const vaiTro = (i) => (laTrongTam(i) ? 'chinh' : 'so_sanh');

  // Meta cua CA HAI truc den tu `params.meta` chu khong con la hang so trong ma.
  //
  // Ban truoc viet cung `unit`/`source` ngay tai day roi goi validateSeries len chinh no.
  // Phep validate do chay that nhung doi tuong no kiem la hang so do chinh preset bia ra,
  // nen no khong bao gio do voi du lieu NGUOI DUNG truyen vao. Gate rong dung nghia, chi
  // tinh vi hon vi co mot loi goi validate that.
  //
  // Preset nay co HAI don vi vi hai truc do hai dai luong khac nhau, nen meta cung phai
  // co hai khoi. Do khong pha luat "khong tron don vi trong mot series": day la HAI
  // series, moi cai mot don vi.
  const pbSeries = {
    ...meta.pb,
    rows: entities.map((e, i) => ({ entity: e, value: pbValues[i], role: vaiTro(i) })),
  };
  const roeSeries = {
    ...meta.roe,
    rows: entities.map((e, i) => ({ entity: e, value: roeValues[i], role: vaiTro(i) })),
  };
  validateSeries(pbSeries); // FAIL ngay nếu unit/tier bịa, entity.code quá dài, hoặc role bịa
  validateSeries(roeSeries);
  // Hai truc, hai don vi CO DINH: truc hoanh la boi so (P/B) va truc tung la phan tram
  // (ROE). Ham dinh dang cua tung truc gan chat voi don vi do, nen tu choi don vi khac
  // thay vi ve ra nhan sai.
  epDonVi(pbSeries, ['lan']);
  epDonVi(roeSeries, ['phan_tram']);

  const decimalsPb = soThapPhan(pbSeries);
  const decimalsRoe = soThapPhan(roeSeries);

  function median(arr) {
    const s = [...arr].sort((a, b) => a - b);
    const mid = Math.floor(s.length / 2);
    return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
  }
  const medPb = median(pbValues); // trung vị CỦA CHÍNH 9 mã đang vẽ, không lấy mốc ngoài
  const medRoe = median(roeValues);

  const rows = entities.map((e, i) => ({
    entity: e,
    pb: pbSeries.rows[i].value,
    roe: roeSeries.rows[i].value,
    role: vaiTro(i),
  }));

  const legendLine = rows.map((r) => `${r.entity.code}=${r.entity.name}`).join(' · ');

  return {
    ...baseOption({
      title: 'Định vị nhóm ngân hàng: P/B và ROE',
      subtitle: 'Trục chia = trung vị của chính 9 mã đang so sánh, không phải mốc ngoài',
      width: W, height: H,
    }),
    tooltip: {
      // 2 trục đều là value nên KHÔNG dùng tooltipDefault (trigger:'axis' + axisPointer
      // shadow dành cho category axis, không hợp với scatter 2 trục liên tục).
      trigger: 'item',
      textStyle: { fontFamily: FONT_STACK, fontSize: 12 },
      formatter: (p) => `${p.data.entity.name}<br/>P/B: ${fmtMultiple(p.data.pb, { decimals: decimalsPb })}<br/>ROE: ${fmtPercent(p.data.roe, { decimals: decimalsRoe })}`,
    },
    legend: { show: false },
    // top: 96 chứ không phải 70 -- đo trên ảnh render thật: yAxis.name "ROE (%)" nổi PHÍA
    // TRÊN mép grid (mặc định nameLocation:'end'), grid.top=70 làm nó đè lên dòng subtitle.
    grid: { left: 70, right: 40, top: 96, bottom: 150 },
    xAxis: {
      type: 'value', scale: true, name: `P/B (${nhanDonVi('lan')})`, nameTextStyle: TYPOGRAPHY.axisName,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtMultiple(v, { decimals: decimalsPb }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    yAxis: {
      type: 'value', scale: true, name: `ROE (${nhanDonVi('phan_tram')})`, nameTextStyle: TYPOGRAPHY.axisName,
      axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtPercent(v, { decimals: decimalsRoe }) },
      splitLine: { lineStyle: { color: PALETTE.line } },
    },
    series: [{
      type: 'scatter',
      data: rows.map((r) => ({
        ...r,
        value: [r.pb, r.roe],
        symbolSize: r.role === 'chinh' ? 16 : 11,
        itemStyle: {
          color: PALETTE.accent, // CÙNG 1 màu cho mọi điểm, không valence theo hạng mục
          borderColor: r.role === 'chinh' ? PALETTE.ink : PALETTE.paper,
          borderWidth: r.role === 'chinh' ? 2.5 : 1,
        },
      })),
      label: { show: true, formatter: (p) => p.data.entity.code, position: 'top', ...TYPOGRAPHY.dataLabel },
      labelLayout: { moveOverlap: 'shiftY' }, // chống chồng nhãn khi 2 mã gần nhau
      markLine: {
        silent: true, symbol: 'none',
        // dashed CHO PHÉP ở đây: markLine tham chiếu, không phải splitLine trục giá trị
        // (luật "không dashed" trong theme.mjs chỉ áp cho splitLine).
        lineStyle: { color: PALETTE.ink, type: 'dashed', width: 1 },
        label: { show: false },
        data: [{ xAxis: medPb }, { yAxis: medRoe }],
      },
    }],
    graphic: [
      { type: 'text', left: 76, top: 106, style: { text: 'Định giá thấp / Hiệu quả cao', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo } },
      // CHÚ Ý bug đã verify bằng thực nghiệm: left:(W-40) + style.textAlign:'right' KHÔNG
      // trừ đúng bề rộng chữ (ECharts đo bounding box theo neo textAlign:'left' mặc định rồi
      // mới đổi text-anchor, làm toạ độ x lệch ra ngoài canvas). Phải dùng thuộc tính
      // `right:` (khoảng cách từ MÉP PHẢI canvas) để neo phải đúng, không dùng `left` + toạ
      // độ tự trừ tay.
      { type: 'text', right: 40, top: 106, style: { text: 'Định giá cao / Hiệu quả cao', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo, textAlign: 'right' } },
      // top = H - 174 (không phải H - grid.bottom = H - 150) để chừa 24px giữa nhãn góc và
      // hàng nhãn trục X phía dưới, đã đo trên ảnh render thật: khoảng cách 8px trước đó làm
      // "Định giá thấp / Hiệu quả thấp" đè lên nhãn tick "10,0%".
      { type: 'text', left: 76, top: H - 174, style: { text: 'Định giá thấp / Hiệu quả thấp', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo } },
      { type: 'text', right: 40, top: H - 174, style: { text: 'Định giá cao / Hiệu quả thấp', font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo, textAlign: 'right' } },
      { type: 'text', left: 16, top: H - 118, style: { text: '● viền đậm = VCB, ngân hàng đang phân tích trong bài. ○ viền mảnh = nhóm so sánh.', font: `9px ${FONT_STACK}`, fill: PALETTE.inkLo } },
      ...wrapLabel(legendLine, 110).map((line, i) => ({
        type: 'text', left: 16, top: H - 100 + i * 13,
        style: { text: line, font: `9px ${FONT_STACK}`, fill: PALETTE.inkLo },
      })),
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
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-15-quadrant-scatter.svg', import.meta.url), svg);
  console.log('15-quadrant-scatter: OK,', svg.length, 'bytes, image?', svg.includes('<image'));
  process.exit(0);
}
