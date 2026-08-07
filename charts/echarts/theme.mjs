// theme.mjs: Theme ECharts CANONICAL cho toàn bộ chart báo cáo tài chính VN.
//
// BẢNG MÀU (chốt theo design-system/tokens.css; CẤM traffic-light):
//   - Với DELTA THEO THỜI GIAN (một đại lượng đổi giữa 2 mốc, vd cầu nối P&L):
//     màu mang nghĩa CHIỀU (tăng/giảm), KHÔNG mang nghĩa VALENCE (tốt/xấu).
//     Vd: nợ vay GIẢM là tin tốt nhưng vẫn tô màu ÂM (đỏ) vì đó là một khoản
//     giảm; người đọc suy ra "tốt/xấu" từ NGỮ CẢNH (nhãn + chú thích), không
//     suy từ màu. Đây là cách FT/Economist tránh traffic-light hoá: xanh
//     lá=tốt/đỏ=xấu chỉ đúng một nửa thời gian trong tài chính (chi phí giảm=
//     tốt nhưng doanh thu giảm=xấu, cùng là "giảm").
//   - Với NHẬN ĐỊNH SO SÁNH (không phải delta thời gian, vd cơ cấu vốn, kịch
//     bản bi quan/lạc quan): để TRUNG TÍNH, hoặc dùng negative nếu một bên
//     BẤT LỢI trong phép so sánh đó. TUYỆT ĐỐI không tô "màu dương" (accent
//     hay positive) cho bên có lợi, đó chính là traffic-light trá hình dưới
//     tên "chỉ là tô màu chủ đạo". negative CHỈ dùng cho giảm/rủi ro/cảnh báo/
//     bất lợi, không dùng cho hạng mục trung tính khác (kể cả khi nó rơi vào
//     đúng vị trí trong mảng color[] mặc định của baseOption()).
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

// Ten font boc bang NHAY DON, khong phai nhay kep. Day khong phai chuyen thau my:
// ECharts nhung nguyen font stack nay vao thuoc tinh style="..." cua the <text> trong
// SVG. Nhay kep long trong nhay kep lam SVG KHONG CON LA XML HOP LE, va hau qua da do
// duoc: WeasyPrint bo qua toan bo file, PDF ra 0 net ve, chart bien mat sach.
// Da do ca hai chieu tren cung mot file: ban nhay kep cho 0 drawing, ban nhay don cho
// 24 drawing va chu WACC doc duoc trong tang text cua PDF.
// Trinh duyet van hien dung ca hai kieu vi HTML parser de tinh hon XML parser, nen loi
// nay khong bao gio lo ra neu chi xem ban HTML.
// Van giu dung luat CLAUDE.md: list ket thuc bang generic keyword.
export const FONT_STACK = "'Spectral', Georgia, 'Times New Roman', serif";
export const FONT_STACK_MONO = "'IBM Plex Mono', Consolas, 'Courier New', monospace";

/** Tron hai mau hex theo ty le t (0=hexA, 1=hexB). Dung de dan xuat sac do tu
 * PALETTE thay vi hardcode hex moi trong file chart. */
export function mixHex(hexA, hexB, t) {
  const parse = (h) => {
    const s = h.replace('#', '');
    return [0, 2, 4].map((i) => parseInt(s.slice(i, i + 2), 16));
  };
  const [ar, ag, ab] = parse(hexA);
  const [br, bg, bb] = parse(hexB);
  const lerp = (a, b) => Math.round(a + (b - a) * t);
  return '#' + [lerp(ar, br), lerp(ag, bg), lerp(ab, bb)]
    .map((v) => v.toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase();
}

// Ba sac xam LANH cho dai ngu canh (vd bullet chart), PHAI cung ho voi
// ink/inkLo/line chu khong duoc la xam-be am (ban thao giay nga da bi bac bo,
// ba nguon doc lap hoi tu ve trang lanh). Dan xuat bang cach tron PALETTE.paper
// voi PALETTE.inkLo theo 3 ty le tang dan; KHONG hardcode hex moi o file chart.
PALETTE.bandLo = mixHex(PALETTE.paper, PALETTE.inkLo, 0.15);
PALETTE.bandMid = mixHex(PALETTE.paper, PALETTE.inkLo, 0.3);
PALETTE.bandHi = mixHex(PALETTE.paper, PALETTE.inkLo, 0.45);

/** Thang mau lien tuc N bac, MOT hue duy nhat, tu gan-paper toi mau dich.
 *
 * Dung cho truong DO LON lien tuc (vd luoi do nhay WACC x g), noi chi co
 * "thap den cao" chu KHONG co hai cuc am duong. Dung thang hai hue o day la
 * ngam gan nghia tot/xau cho mot dai von khong co nghia do, tuc traffic-light
 * tra hinh.
 *
 * Bac dau khong bat dau tu 0 ma tu 0,12: mot o gan nhu trang tren nen trang
 * khong doc duoc la mot o hay hai o, va khi in den trang thi mat han. Bac cuoi
 * la mau dich nguyen ban.
 *
 * KHONG dung cho delta hay so sanh co ben loi ben hai; nhung ca do da co
 * PALETTE.accent va PALETTE.negative. */
export function sequentialScale(hex = PALETTE.accent, steps = 5) {
  if (steps < 2) throw new Error('sequentialScale: can it nhat 2 bac');
  return Array.from({ length: steps }, (_, i) =>
    mixHex(PALETTE.paper, hex, 0.12 + (i / (steps - 1)) * 0.88),
  );
}

export const TYPOGRAPHY = {
  title: { fontSize: 15, fontWeight: 'bold', fontFamily: FONT_STACK, color: PALETTE.ink },
  subtitle: { fontSize: 12, fontFamily: FONT_STACK, color: PALETTE.inkMd },
  axisLabel: { fontSize: 11, fontFamily: FONT_STACK_MONO, color: PALETTE.inkMd },
  axisName: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.inkLo },
  legend: { fontSize: 11, fontFamily: FONT_STACK, color: PALETTE.inkMd },
  dataLabel: { fontSize: 11, fontFamily: FONT_STACK_MONO, color: PALETTE.ink },
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
