// 13-line-annotated.mjs, Line có chú thích sự kiện: xu hướng 1 chỉ tiêu + vì sao đổi hướng
// Dùng khi: một chỉ tiêu đổi hướng rõ rệt tại vài thời điểm, người đọc cần biết SỰ KIỆN
// nào giải thích bước ngoặt, không chỉ thấy đường lên/xuống. Nhu cầu 8/10 loại báo cáo
// (research/13-chart-component-gap/FINDINGS.md) nhưng chưa có bản ECharts.
// Dữ liệu cần: series schema dùng chung (charts/echarts/schema.mjs), 1 chuỗi rows
// {value, period} qua N kỳ, cộng tối đa 4-5 sự kiện {index,label} RIÊNG, không đi qua
// validateSeries() vì đó là annotation tự do, không phải quan sát.
// Bẫy thường gặp: (1) nhồi quá 5 sự kiện -> nhãn chồng không gỡ được, tách sang bảng
// dòng thời gian riêng; (2) tô màu sự kiện theo tốt/xấu (traffic-light) -> CHỦ Ý dùng
// 1 màu ink trung tính cho MỌI sự kiện, người đọc tự suy từ độ dốc đường và nội dung
// nhãn; (3) dưới 4 điểm dữ liệu thì đường không đủ dài để thấy xu hướng.
// RÀNG BUỘC CỨNG (xem CLAUDE.md "Tên font trong chart phải bọc bằng nháy ĐƠN"): mọi
// font trong graphic PHẢI lấy từ FONT_STACK/TYPOGRAPHY của theme.mjs, không gõ lại chuỗi
// font mới -- nháy kép lồng nháy kép từng làm SVG không phải XML hợp lệ, WeasyPrint bỏ
// qua cả file mà không báo lỗi.
import { baseOption, PALETTE, FONT_STACK, TYPOGRAPHY, tooltipDefault } from './theme.mjs';
import { fmtCompact, fmtQuarter, wrapLabel } from './fmt.mjs';
import { validateSeries, soThapPhan, nhanDonVi } from './schema.mjs';
import { renderStatic } from './render-static.mjs';

const W = 720, H = 420;

// Dữ liệu theo schema dùng chung: unit/source/decimals/direction/kind ở CẤP SERIES,
// không ở từng hàng (xem charts/echarts/schema.mjs). entity không cần cho chuỗi đơn.
export const MAC_DINH = {
  series: {
    unit: 'ty_dong',
    source: { tier: 'uoc-tinh', label: 'Minh hoạ, không phải số thật' },
    as_of: '2026-08-07',
    direction: 'cao_tot', // doanh thu cao hơn là tốt hơn
    kind: 'luy_ke_ky', // phát sinh trong kỳ, cộng dồn được
    rows: [
      { value: 180, period: { type: 'quy', q: 1, year: 2025, end: '2025-03-31' } },
      { value: 195, period: { type: 'quy', q: 2, year: 2025, end: '2025-06-30' } },
      { value: 172, period: { type: 'quy', q: 3, year: 2025, end: '2025-09-30' } },
      { value: 210, period: { type: 'quy', q: 4, year: 2025, end: '2025-12-31' } },
      { value: 225, period: { type: 'quy', q: 1, year: 2026, end: '2026-03-31' } },
      { value: 198, period: { type: 'quy', q: 2, year: 2026, end: '2026-06-30' } },
      { value: 240, period: { type: 'quy', q: 3, year: 2026, end: '2026-09-30' } },
      { value: 265, period: { type: 'quy', q: 4, year: 2026, end: '2026-12-31' } },
    ],
  },
  // index trỏ vào đúng vị trí trong series.rows (0-based).
  events: [
    { index: 2, label: 'Đứt gãy chuỗi cung ứng nguyên liệu nhập khẩu' },
    { index: 4, label: 'Ký hợp đồng phân phối độc quyền khu vực miền Trung' },
    { index: 5, label: 'Đối thủ mới gia nhập, cạnh tranh giá bán lẻ' },
    { index: 7, label: 'Ra mắt dòng sản phẩm cao cấp, biên lợi nhuận cao hơn' },
  ],
};

/** Tra ve OBJECT OPTION thuan, cong 1 truong noi bo `_veSauLayout(chart)` -- lop chu
 * thich su kien can TOA DO PIXEL THAT sau khi truc da layout (chart.convertToPixel()),
 * nen KHONG the tinh tay bang cong thuc tuyen tinh don gian nhu 17-football-field.mjs
 * (truc y o day KHONG khai max, ECharts tu chon "nice extent" theo thuat toan noi bo --
 * tu tinh lai dung y thuat toan do la viec RUI RO CAO, de lech mot don vi la sai vi tri
 * moi nhan su kien). `_veSauLayout` duoc renderStatic()/mountLive() goi SAU setOption
 * dau tien, dua tren MOT chart instance THAT (do render-static.mjs/mount-live.mjs tao,
 * option() o day khong tu goi echarts.init()). Xem render-static.mjs de biet co che. */
export function option(params) {
  const { series, events } = params;
  if (events.length > 5) throw new Error('13-line-annotated: qua 5 su kien, tach sang bang dong thoi gian (03-wall-chart-timeline)');
  validateSeries(series); // FAIL ngay nếu unit/source/period sai định dạng
  const decimals = soThapPhan(series); // 0 cho 'ty_dong', không tự chọn ở đây

  const categories = series.rows.map((r) => fmtQuarter(r.period.q, r.period.year));
  const values = series.rows.map((r) => r.value);
  const donVi = nhanDonVi(series.unit);

  return {
    ...baseOption({ title: 'Doanh thu thuần theo quý, có chú thích sự kiện', subtitle: `Đơn vị: ${donVi}, minh hoạ 2025-2026, không phải số thật`, width: W, height: H }),
    tooltip: { ...tooltipDefault, valueFormatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals }) },
    legend: { show: false },
    grid: { left: 60, right: 24, top: 108, bottom: 50 }, // top nới rộng để chừa chỗ nhãn sự kiện phía trên đường
    xAxis: { type: 'category', data: categories, boundaryGap: false, axisLine: { lineStyle: { color: PALETTE.inkMd } }, axisTick: { show: false }, axisLabel: TYPOGRAPHY.axisLabel },
    yAxis: { type: 'value', min: 0, axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: (v) => fmtCompact(v, { baseUnit: 'ty', decimals }) }, splitLine: { lineStyle: { color: PALETTE.line } } },
    series: [{
      name: 'Doanh thu thuần', type: 'line', data: values, symbol: 'circle', symbolSize: 6,
      lineStyle: { width: 2, color: PALETTE.accent }, itemStyle: { color: PALETTE.accent },
    }],
    // lớp chú thích: vẽ SAU khi có toạ độ pixel thật (convertToPixel hoạt động đúng ở chế
    // độ ssr:true). renderStatic()/mountLive() setOption lần 2 chỉ thêm `graphic`, KHÔNG
    // xoá series đã có.
    _veSauLayout(chart) {
      const graphics = [];
      events.forEach((ev, i) => {
        const [px, py] = chart.convertToPixel({ xAxisIndex: 0, yAxisIndex: 0 }, [ev.index, values[ev.index]]);
        const above = i % 2 === 0; // xen kẽ trên/dưới giảm chồng nhãn khi 2 sự kiện gần nhau
        const leaderLen = 34;
        const lines = wrapLabel(ev.label, 18);
        const labelTopStart = above ? py - leaderLen - lines.length * 13 : py + leaderLen + 4;
        // điểm gần mép trái/phải canvas thì khối nhãn (textAlign 'center') tràn ra ngoài --
        // kẹp vị trí NGANG của CHỮ vào biên an toàn, leader line/chấm tròn vẫn neo đúng điểm
        // dữ liệu thật (px). Đã thử đổi textAlign theo cạnh gần nhất trước đó nhưng ECharts
        // graphic text neo text-anchor="end" tại left+textWidth chứ không phải tại left khi
        // left là số + textAlign:'right', nên chữ bị đẩy CÀNG lệch ra ngoài canvas -- kẹp vị
        // trí thay vì đổi textAlign để né hẳn cách tính lệch đó.
        const edgeMargin = 90;
        const textLeft = Math.min(Math.max(px, edgeMargin), W - edgeMargin);
        graphics.push(
          { type: 'line', shape: { x1: px, y1: py, x2: px, y2: above ? py - leaderLen : py + leaderLen }, style: { stroke: PALETTE.inkMd, lineWidth: 1 }, silent: true },
          // TẤT CẢ điểm sự kiện dùng CÙNG 1 màu trung tính (ink), không phân tích cực/tiêu cực
          // -- đây là chú thích nguyên nhân, không phải delta có bên thắng-thua.
          { type: 'circle', shape: { cx: px, cy: py, r: 4 }, style: { fill: PALETTE.ink, stroke: PALETTE.paper, lineWidth: 1.5 }, silent: true },
          // toạ độ đặt TRONG style.x/y (khớp cách shape.x1/y1 của line/circle ở trên dùng
          // toạ độ pixel thô), KHÔNG dùng top-level left/top -- đã thực nghiệm thấy left/top
          // cấp graphic-item cho toạ độ lệch xa so với px thật khi phối hợp với textAlign,
          // trong khi style.x/y bám đúng convertToPixel().
          ...lines.map((line, li) => ({
            type: 'text', x: textLeft, y: labelTopStart + li * 13,
            style: { text: line, font: `11px ${FONT_STACK}`, fill: PALETTE.inkMd, textAlign: 'center' },
            silent: true,
          })),
        );
      });
      return graphics;
    },
  };
}

// Giu nguyen duong CLI de verify-charts.mjs va catalog khong vo. `typeof process !==
// 'undefined'` dung TRUOC de tranh ReferenceError khi file nay bi import trong trinh
// duyet (lan html-song qua mount-live.mjs); `node:fs` chuyen sang import DONG cung ly do
// (chi tiet: 01-waterfall.mjs).
if (typeof process !== 'undefined' && import.meta.url === `file://${process.argv[1]}`) {
  const { writeFileSync } = await import('node:fs');
  const svg = renderStatic(option, MAC_DINH, { width: W, height: H });
  writeFileSync(new URL('./out-13-line-annotated.svg', import.meta.url), svg);
  console.log('13-line-annotated: OK,', svg.length, 'bytes, <image>?', svg.includes('<image'));
  process.exit(0);
}
