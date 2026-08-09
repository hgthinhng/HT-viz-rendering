// 18-sensitivity-grid.mjs, Lưới độ nhạy 2 chiều: 2 biến cùng tác động lên 1 kết quả
// Dùng khi: 2 biến giả định thay đổi ĐỒNG THỜI (vd WACC x tăng trưởng dài hạn), kết quả
// là 1 ma trận N x M, cần đánh dấu riêng 1 ô "base case". Khác 06-tornado (1 biến/lúc,
// dùng khi chỉ cần 1 biến độ nhạy) và khác 08-heatmap (ma trận DIVERGING categorical có
// cực âm/dương, không có khái niệm base case) -- ở đây là magnitude field LIÊN TỤC 1 hue,
// chỉ có "thấp/cao", không có "âm/dương".
// KHÔNG dùng khi: 1 biến độ nhạy (dùng 06-tornado, gọn hơn); ma trận >6x6-7x7 (quá dày để
// dò mắt); 2 biến không độc lập trong mô hình (kết quả interaction giả tạo).
// Dữ liệu cần: series schema dùng chung (charts/echarts/schema.mjs) -- mỗi ô ma trận là 1
// hàng {entity:{code}, value}, unit/source ở cấp series. waccRows/gCols là 2 trục input,
// KHÔNG phải entity của series (chúng không có giá trị kết quả riêng, chỉ là chỉ số hàng/
// cột), nên đứng ngoài schema.
// Bẫy: (1) dùng thang diverging 2 hue thay vì 1 hue liên tục -> đây là magnitude field,
// không phải delta/so sánh, tô 2 hue sẽ ngầm gán "tốt/xấu" sai cho 1 đại lượng không có
// cực; (2) đổi màu NỀN ô base case thay vì chỉ đổi VIỀN -> phá tính liên tục của thang màu
// (nếu đổi nền, ô base case đọc như 1 outlier chứ không phải 1 điểm tham chiếu trong cùng
// thang đo); (3) quên set màu chữ theo độ đậm ô -> chữ đen trên nền accent đậm nhất không
// đọc được; (4) so sánh value===matrix[baseRow][baseCol] để tìm ô base -> nguồn lỗi im
// lặng nếu 2 ô trùng giá trị, PHẢI dùng coCo() theo CHỈ SỐ NGUYÊN.
import { baseOption, PALETTE, TYPOGRAPHY, FONT_STACK_MONO, sequentialScale } from './theme.mjs';
import { fmtNumber, fmtPercent } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi, coCo, epDonVi } from './schema.mjs';

const W = 700, H = 460;
const GRID = { left: 76, right: 24, top: 96, bottom: 84 };
const STEPS = 5;

export const MAC_DINH = {
  waccRows: [9.0, 9.5, 10.0, 10.5, 11.0], // %, trục hàng
  gCols: [2.0, 2.5, 3.0, 3.5, 4.0], // %, trục cột (tăng trưởng dài hạn)
  matrix: [
    [940, 965, 995, 1030, 1075],
    [890, 910, 935, 965, 1000],
    [800, 822, 850, 880, 915],
    [735, 752, 772, 795, 822],
    [680, 693, 708, 725, 745],
  ], // giá trị doanh nghiệp, tỷ đồng, minh hoạ (khớp base case 850 của 06-tornado.mjs để nhất quán bối cảnh minh hoạ, không phải trùng hợp số thật)
  baseRow: 2, baseCol: 2, // WACC 10,0% / g 3,0% = 850, base case CỦA MÔ HÌNH, không suy từ giá trị
  // Khoi meta BAT BUOC: don vi va nguon cua GIA TRI trong luoi.
  meta: {
    unit: 'ty_dong',
    source: { tier: 'uoc-tinh', label: 'Mô hình DCF nội bộ, minh hoạ' },
    as_of: '2026-08-07',
  },
};

/** Tra ve OBJECT OPTION thuan, cong 1 truong noi bo `_veSauLayout(chart)` cho khung base
 * case -- can toa do PIXEL THAT cua tam o (qua chart.convertToPixel() tren truc category)
 * sau khi truc da layout. Xem render-static.mjs de biet co che chung voi 13/17. */
export function option(params) {
  const { waccRows, gCols, matrix, baseRow, baseCol , meta} = params;

  // series schema dùng chung: mỗi ô ma trận là 1 hàng, unit/source/decimals ở cấp series
  // (đúng chỗ, không lặp lại trên từng ô). entity.code chỉ để thoả ràng buộc "mỗi hàng có 1
  // nhãn ngắn", không dùng để hiển thị (nhãn thật trên lưới là header WACC/g riêng).
    // Meta den tu `params.meta` chu khong con la hang so trong ma.
  //
  // Ban truoc dung `unit`/`source` viet cung ngay tai day roi goi validateSeries len
  // chinh no. Phep validate do chay that nhung doi tuong no kiem la mot hang so do
  // chinh preset bia ra, nen no khong bao gio do voi du lieu NGUOI DUNG truyen vao:
  // mot bao cao that co the dua vao mot bo so khong nguon ma preset van xanh. Do la
  // gate rong dung nghia, chi tinh vi hon vi co mot loi goi validate that.
  const series = { ...meta, rows: [] };
  waccRows.forEach((w, ri) => gCols.forEach((g, ci) => {
    series.rows.push({
      entity: { code: `WACC ${fmtPercent(w, { decimals: 1 })} / g ${fmtPercent(g, { decimals: 1 })}` },
      value: matrix[ri][ci],
    });
  }));
  validateSeries(series); // FAIL ngay nếu thiếu unit/source hoặc entity.code vượt 24 ký tự
  // Ham dinh dang cua preset nay gan chat voi don vi ty_dong, nen no TU CHOI don vi
  // khac thay vi nhan roi ve ra nhan sai. Xem epDonVi() trong schema.mjs.
  epDonVi(series, ['ty_dong']);
  const decimals = soThapPhan(series);
  const donVi = nhanDonVi(series.unit);

  // base case xác định bằng CHỈ SỐ NGUYÊN qua coCo() của schema, không so sánh giá trị số
  // thực -- 2 ô có thể trùng giá trị (vd làm tròn) mà vẫn khác ô, so sánh float là nguồn lỗi
  // im lặng. Gộp (ri,ci) thành 1 chỉ số phẳng để dùng chung tiện ích coCo() (vốn nhận 1
  // chỉ số nguyên trên 1 mảng phẳng).
  const totalCells = waccRows.length * gCols.length;
  const baseFlatIndex = baseRow * gCols.length + baseCol;
  const laOBaseCase = coCo(baseFlatIndex, totalCells);

  const flat = matrix.flat();
  const min = Math.min(...flat), max = Math.max(...flat);
  // thang màu RỜI RẠC 5 bậc, 1 hue duy nhất, dẫn xuất từ PALETTE.accent qua sequentialScale
  // (theme.mjs) -- KHÔNG tự tính hex trong file preset, KHÔNG dùng thang 2 cực xanh-đỏ vì
  // đây là 1 trường độ lớn liên tục (magnitude field), không có "âm/dương".
  const bandColors = sequentialScale(PALETTE.accent, STEPS);
  const bandOf = (v) => Math.min(STEPS - 1, Math.floor(((v - min) / (max - min)) * STEPS));
  const isDarkBand = (band) => band >= STEPS - 1; // chỉ bậc đậm nhất mới cần chữ trắng, khớp thực nghiệm ở mẫu HTML đã duyệt

  const data = [];
  waccRows.forEach((w, ri) => gCols.forEach((g, ci) => {
    const v = matrix[ri][ci];
    const band = bandOf(v);
    const flatIndex = ri * gCols.length + ci;
    const isBase = laOBaseCase(flatIndex);
    data.push({
      value: [ci, ri, v],
      // KHÔNG đánh dấu base case bằng itemStyle.borderColor/borderWidth ở đây -- series
      // heatmap vẽ từng ô theo thứ tự, 2 ô KỀ BÊN (phải, dưới) vẽ SAU nên đè mất 2 trong 4
      // cạnh viền của ô base case, viền chỉ còn hiện góc trên-trái thay vì cả khung (đã tự
      // bắt bằng ảnh chụp crop cao). Viền base case chuyển hẳn sang 1 rect graphic riêng vẽ
      // SAU CÙNG bên dưới (z cao hơn mọi ô), xem `_veSauLayout` phía dưới.
      itemStyle: { color: bandColors[band], borderColor: PALETTE.paper, borderWidth: 2 },
      label: { color: isDarkBand(band) ? PALETTE.paper : PALETTE.ink, fontWeight: isBase ? 'bold' : 'normal' },
    });
  }));

  return {
    ...baseOption({
      title: 'Lưới độ nhạy: giá trị doanh nghiệp theo WACC và tăng trưởng dài hạn',
      subtitle: `Đơn vị: ${donVi}, minh hoạ. Base case WACC ${fmtPercent(waccRows[baseRow], { decimals: 1 })} / g ${fmtPercent(gCols[baseCol], { decimals: 1 })} = ${fmtNumber(matrix[baseRow][baseCol], { decimals })} (viền đậm)`,
      width: W, height: H,
    }),
    tooltip: { position: 'top', formatter: (p) => `WACC ${fmtPercent(waccRows[p.data.value[1]], { decimals: 1 })}, g ${fmtPercent(gCols[p.data.value[0]], { decimals: 1 })}: ${fmtNumber(p.data.value[2], { decimals })} ${donVi}` },
    legend: { show: false },
    // ECharts BẮT BUỘC 1 component visualMap nhắm vào series heatmap mới chịu render, kể cả
    // khi mọi ô đã tự set itemStyle.color riêng -- không có nó thì ném "Heatmap must use with
    // visualMap" ngay ở bước render, đã tự kiểm bằng thực nghiệm. show:false vì màu THẬT lấy
    // từ itemStyle từng ô (băng rời rạc 5 bậc ở trên), không lấy từ thang màu của component
    // này -- itemStyle đặt trực tiếp trên data item luôn thắng thang màu suy ra từ visualMap.
    visualMap: { show: false, min, max, dimension: 2 },
    grid: GRID,
    xAxis: {
      type: 'category', data: gCols.map((g) => fmtPercent(g, { decimals: 1 })),
      name: 'Tăng trưởng dài hạn (g)', nameLocation: 'middle', nameGap: 30, nameTextStyle: TYPOGRAPHY.axisName,
      splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: PALETTE.ink, fontFamily: FONT_STACK_MONO, fontSize: 11, fontWeight: 'bold' },
    },
    yAxis: {
      type: 'category', data: waccRows.map((w) => fmtPercent(w, { decimals: 1 })),
      inverse: true, // hàng đầu mảng (WACC thấp nhất) nằm TRÊN CÙNG, khớp mẫu HTML đã duyệt
      // nameLocation mặc định 'end' đặt tên trục ở DƯỚI khi inverse:true (đã tự bắt bằng ảnh
      // chụp thật: "WACC" đè lên ngay chú giải thang màu "Thấp" ở chân chart) -- 'start' đặt
      // đúng lên phía TRÊN, ngay trên hàng đầu (WACC thấp nhất).
      name: 'WACC', nameLocation: 'start', nameGap: 20, nameTextStyle: TYPOGRAPHY.axisName,
      splitArea: { show: false }, axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: PALETTE.ink, fontFamily: FONT_STACK_MONO, fontSize: 11, fontWeight: 'bold' },
    },
    series: [{
      type: 'heatmap', data,
      label: { show: true, formatter: (p) => fmtNumber(p.data.value[2], { decimals }), fontSize: 12, fontFamily: FONT_STACK_MONO },
    }],
    // KHÔNG đặt graphic ở lần setOption đầu -- khung base case cần convertToPixel(), chỉ
    // dùng được SAU khi trục đã tồn tại. Gom hết graphic vào 1 mảng rồi set đúng 1 lần trong
    // `_veSauLayout`, chạy SAU setOption dau tien do renderStatic()/mountLive() thuc hien
    // (bai hoc tu preset 17: chart.getOption().graphic tra ve dang boc khac cau truc dua
    // vao, spread lai de noi them graphic lam ECharts am tham bo qua phan tu them sau).
    _veSauLayout(chart) {
      // khung base case: 1 rect graphic riêng, vẽ SAU series heatmap nên KHÔNG bị ô kề bên
      // đè mất cạnh (khác itemStyle.borderColor đặt trên chính ô, bị 2 ô vẽ sau đè mất 2/4
      // cạnh, đã tự bắt lỗi này bằng ảnh chụp crop cao). fill:none nên không đụng màu nền ô,
      // giữ đúng nguyên tắc "chỉ đánh dấu bằng viền, không đổi màu nền" -- đổi nền phá tính
      // liên tục của thang màu.
      //
      // Toạ độ: KHÔNG dùng convertToPixel([baseCol-0.5, baseRow-0.5]) để lấy trực tiếp 2 góc
      // ô -- đã tự thử và bắt bằng ảnh chụp crop cao: kết quả lệch nguyên NỬA Ô sang phải-dưới
      // so với ô "850" thật (category axis không nội suy nửa-chỉ-số như trục value). Cách
      // đúng đã verify bằng cách so với toạ độ <path> thật của chính ô đó trong SVG render:
      // lấy TÂM ô base case qua convertToPixel([baseCol, baseRow]) (số nguyên, luôn đúng vì
      // đó chính là chỉ số category), rồi lấy khoảng cách tâm-tới-tâm với ô kế bên để suy ra
      // bề rộng/cao 1 ô -- 2 tâm liền kề cách nhau ĐÚNG BẰNG 1 band width bất kể offset nội
      // bộ của HeatmapView.
      const [xCenter, yCenter] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [baseCol, baseRow]);
      const [xNextCol] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [baseCol + 1, baseRow]);
      const [, yNextRow] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [baseCol, baseRow + 1]);
      const cellW = Math.abs(xNextCol - xCenter);
      const cellH = Math.abs(yNextRow - yCenter);
      const baseBorderInset = 1.5; // co nhẹ vào trong nửa lineWidth để nét viền không tràn ra ngoài khung ô, tránh chồng lên gridline giữa các ô lân cận
      const baseRect = {
        x: xCenter - cellW / 2 + baseBorderInset,
        y: yCenter - cellH / 2 + baseBorderInset,
        width: cellW - baseBorderInset * 2,
        height: cellH - baseBorderInset * 2,
      };

      // legend thang màu tự vẽ (KHÔNG dùng component visualMap): 5 bậc rời rạc dễ dò "ô này
      // thuộc bậc nào" hơn gradient liên tục tinh vi ở lưới nhỏ, và tự vẽ cho toàn quyền set
      // màu chữ điều kiện theo ô mà không phải vật lộn với API màu điều kiện của visualMap.
      return [
        { type: 'text', left: 76, top: H - 34, style: { text: 'Thấp', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
        ...bandColors.map((c, i) => ({ type: 'rect', left: 116 + i * 40, top: H - 38, shape: { width: 34, height: 12 }, style: { fill: c } })),
        { type: 'text', left: 116 + STEPS * 40 + 6, top: H - 34, style: { text: 'Cao', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
        { type: 'text', left: 116 + STEPS * 40 + 50, top: H - 34, style: { text: '1 hue liên tục, không traffic-light', font: `10px ${FONT_STACK_MONO}`, fill: PALETTE.inkLo } },
        // z cao nhất trong toàn bộ graphic, và graphic vốn đã vẽ SAU series trong SSR -> khung
        // luôn nổi trên mọi ô, đủ cả 4 cạnh.
        { type: 'rect', z: 10, shape: baseRect, style: { fill: 'none', stroke: PALETTE.ink, lineWidth: 3 }, silent: true },
      ];
    },
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
  writeFileSync(new URL('./out-18-sensitivity-grid.svg', import.meta.url), svg);
  console.log('18-sensitivity-grid: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
