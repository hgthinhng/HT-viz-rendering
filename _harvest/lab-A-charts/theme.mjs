// theme.mjs — Theme ECharts CANONICAL cho toàn bộ chart báo cáo tài chính VN.
//
// BẢNG MÀU (chốt theo brief: 1 accent + 1 âm + 2-3 trung tính; CẤM traffic-light):
//   - Màu mang nghĩa DIRECTION (tăng/giảm), KHÔNG mang nghĩa VALENCE (tốt/xấu).
//     Vd: nợ vay GIẢM là tin tốt nhưng vẫn tô màu ÂM (đỏ) vì đó là một khoản
//     giảm trong biểu đồ cầu nối — người đọc suy ra "tốt/xấu" từ NGỮ CẢNH
//     (nhãn + chú thích), không suy từ màu. Đây là cách FT/Economist tránh
//     traffic-light hoá: xanh lá=tốt/đỏ=xấu chỉ đúng một nửa thời gian trong
//     tài chính (chi phí giảm=tốt nhưng doanh thu giảm=xấu, cùng là "giảm").
//   - accent   #2a78d6 (xanh dương) — series chính/số liệu kỳ hiện tại/tăng.
//   - negative #dc2626 (đỏ)         — giảm/rủi ro/cảnh báo. DUY NHẤT dùng đỏ
//                                     cho mục đích này, không dùng đỏ cho gì khác.
//   - neutralDark  #3c3c41 — subtotal/tổng/cột mốc, đường viền đậm.
//   - neutralMid   #9a9992 — series so sánh (kỳ trước/trung bình ngành), context.
//   - neutralLight #dbdee4 — gridline, trục, nền phụ.
//   Nguồn gốc: accent/negative lấy từ ramp đã qua validator CVD trong
//   references/palette.md (skill dataviz) — KHÔNG tự bịa hex.
//
// TYPOGRAPHY: font-family ưu tiên bộ font WINDOWS vì file HTML/PDF này sẽ mở
// trên máy khách (memory: "Font Linux không dùng cho file gửi đi" — Linux
// thường thiếu metric y hệt Windows, dấu tiếng Việt lệch/vỡ khi convert PDF).
// Không dùng fallback "sans-serif" của Linux (DejaVu Sans) làm mặc định.

export const PALETTE = {
  accent: '#2a78d6',
  accentDark: '#184f95',
  negative: '#dc2626',
  neutralDark: '#3c3c41',
  neutralMid: '#9a9992',
  neutralLight: '#dbdee4',
  surface: '#ffffff',
  textPrimary: '#0b0b0b',
  textSecondary: '#54555a',
  textMuted: '#898781',
  gridline: '#dbdee4',
  axisLine: '#54555a',
};

export const FONT_STACK = '"Calibri","Segoe UI",Arial,sans-serif';

export const TYPOGRAPHY = {
  title: { fontSize: 15, fontWeight: 'bold', fontFamily: FONT_STACK, color: PALETTE.textPrimary },
  subtitle: { fontSize: 12, fontFamily: FONT_STACK, color: PALETTE.textSecondary },
  axisLabel: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.textSecondary },
  axisName: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.textMuted },
  legend: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.textSecondary },
  dataLabel: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.textPrimary },
  source: { fontSize: 10, fontFamily: FONT_STACK, color: PALETTE.textMuted },
};

/** Base option áp cho MỌI chart — spread rồi override phần series/axis riêng. */
export function baseOption({ title, subtitle, width = 700, height = 400 } = {}) {
  return {
    backgroundColor: PALETTE.surface,
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
    color: [PALETTE.accent, PALETTE.negative, PALETTE.neutralMid, PALETTE.neutralDark],
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
    splitLine: { lineStyle: { color: PALETTE.gridline, width: 1, type: 'solid' } },
  };
}

/** Trục hạng mục chuẩn: chỉ một đường trục dưới cùng, không gridline dọc mặc định. */
export function categoryAxis(data, opts = {}) {
  return {
    type: 'category',
    data,
    axisLine: { lineStyle: { color: PALETTE.axisLine } },
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
    style: { text, font: `10px ${FONT_STACK}`, fill: PALETTE.textMuted },
    silent: true,
  };
}
