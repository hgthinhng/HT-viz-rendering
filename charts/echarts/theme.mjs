// theme.mjs: Theme ECharts CANONICAL cho toàn bộ chart báo cáo tài chính VN.
//
// BẢNG MÀU (chốt theo design-system/tokens.css; CẤM traffic-light):
//   - Màu mang nghĩa DIRECTION (tăng/giảm), KHÔNG mang nghĩa VALENCE (tốt/xấu).
//     Vd: nợ vay GIẢM là tin tốt nhưng vẫn tô màu ÂM (đỏ) vì đó là một khoản
//     giảm trong biểu đồ cầu nối, người đọc suy ra "tốt/xấu" từ NGỮ CẢNH
//     (nhãn + chú thích), không suy từ màu. Đây là cách FT/Economist tránh
//     traffic-light hoá: xanh lá=tốt/đỏ=xấu chỉ đúng một nửa thời gian trong
//     tài chính (chi phí giảm=tốt nhưng doanh thu giảm=xấu, cùng là "giảm").
//   - Bang mau chot theo design-system/tokens.css. Ba nguon doc lap hoi tu cung
//     bo nay: reference-kimi.html, huashu-design design-styles.md muc Two-Font
//     Consulting (McKinsey deep-blue), va giao trinh thiet ke dong 88.
//
// TYPOGRAPHY: PHAI ket thuc bang generic keyword. Khai bao mot ten font tran
// khien trinh duyet thay glyph theo tung ky tu va lam roi dau tieng Viet
// ("So lieu" thanh "So^' lieu", dau sac tach roi troi noi), loi tinh vi hon
// tofu nen de lot QC. SVG co the duoc mo doc lap, khong co font nhung cua
// trang, nen fallback la bat buoc chu khong phai de phong.

export const PALETTE = {
  accent: '#2251FF',
  accentHi: '#1233B8',
  accentSoft: '#7D9BFF',
  negative: '#C22F4E',
  positive: '#008A6D',
  warn: '#B07A10',
  ink: '#051C2C',
  inkMd: '#42566A',
  inkLo: '#8595A6',
  line: '#DBE2EA',
  paper: '#FFFFFF',
};

export const FONT_STACK = '"Spectral", Georgia, "Times New Roman", serif';
export const FONT_STACK_MONO = '"IBM Plex Mono", Consolas, "Courier New", monospace';

export const TYPOGRAPHY = {
  title: { fontSize: 15, fontWeight: 'bold', fontFamily: FONT_STACK, color: PALETTE.ink },
  subtitle: { fontSize: 12, fontFamily: FONT_STACK, color: PALETTE.inkMd },
  axisLabel: { fontSize: 11, fontFamily: FONT_STACK_MONO, color: PALETTE.inkMd },
  axisName: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.inkLo },
  legend: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.inkMd },
  dataLabel: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.ink },
  source: { fontSize: 10, fontFamily: FONT_STACK, color: PALETTE.inkLo },
};

/** Base option áp cho MỌI chart, spread rồi override phần series/axis riêng. */
export function baseOption({ title, subtitle, width = 700, height = 400 } = {}) {
  return {
    backgroundColor: PALETTE.paper,
    textStyle: { fontFamily: FONT_STACK },
    title: {
      text: title || '',
      subtext: subtitle || '',
      left: 'left',
      top: 8,
      left: 16,
      textStyle: TYPOGRAPHY.title,
      subtextStyle: TYPOGRAPHY.subtitle,
    },
    grid: {
      left: 56,
      right: 24,
      top: subtitle ? 68 : 52,
      bottom: 60,
      containLabel: true,
    },
    legend: {
      bottom: 8,
      icon: 'roundRect',
      itemWidth: 12,
      itemHeight: 8,
      textStyle: TYPOGRAPHY.legend,
    },
    color: [PALETTE.accent, PALETTE.negative, PALETTE.inkLo, PALETTE.ink],
  };
}

/** Trục giá trị chuẩn: gridline mảnh 1px solid, KHÔNG bao giờ dashed, bắt đầu từ 0 cho bar/column. */
export function valueAxis(opts = {}) {
  const { name, min, startAtZero = true, axisLabelFormatter } = opts;
  return {
    type: 'value',
    name,
    nameTextStyle: TYPOGRAPHY.axisName,
    min: startAtZero ? 0 : min,
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { ...TYPOGRAPHY.axisLabel, formatter: axisLabelFormatter },
    splitLine: { lineStyle: { color: PALETTE.line, width: 1, type: 'solid' } },
  };
}

/** Trục hạng mục chuẩn: chỉ một đường trục dưới cùng, không gridline dọc mặc định. */
export function categoryAxis(data, opts = {}) {
  return {
    type: 'category',
    data,
    axisLine: { lineStyle: { color: PALETTE.inkMd } },
    axisTick: { show: false },
    axisLabel: { ...TYPOGRAPHY.axisLabel, ...(opts.axisLabel || {}) },
    splitLine: { show: false },
  };
}

export const tooltipDefault = {
  trigger: 'axis',
  textStyle: { fontFamily: FONT_STACK, fontSize: 12 },
  axisPointer: { type: 'shadow' },
};

export function sourceGraphic(text, { width = 700, height = 400 } = {}) {
  return {
    type: 'text',
    left: 16,
    top: height - 20,
    style: { text, font: `10px ${FONT_STACK}`, fill: PALETTE.inkLo },
    silent: true,
  };
}
