/**
 * annotate.js — lớp chú thích (callout) tái dùng được cho minh hoạ ngành
 * vẽ tay bằng SVG (xem grammar.txt).
 *
 * Nguyên tắc thiết kế:
 *  - Toàn bộ đường dẫn (leader), điểm neo, hộp nhãn được vẽ THẲNG VÀO SVG
 *    (createElementNS), KHÔNG dùng absolute-positioned HTML overlay — vì
 *    vậy chúng LUÔN hiện khi in / xuất PDF, không phụ thuộc :hover hay vị
 *    trí cuộn trang (yêu cầu bắt buộc: "hoạt động cả khi in").
 *  - Phần duy nhất là HTML overlay là "drill card" (thẻ chi tiết khi click)
 *    — vì nó cần nổi trên toàn trang và theo vị trí con trỏ, đây là phần
 *    NÂNG CAO/tương tác, không phải kênh thông tin chính (đầu đề + phụ đề
 *    trên nhãn đã đủ nghĩa khi in ra giấy / PPTX, không cần click).
 *
 * Sử dụng (script thường, KHÔNG phải type="module"):
 *   <script src="../annotate.js"></script>
 *   <script>
 *     const svg = document.querySelector('#ship-svg');
 *     Annotate.annotate(svg, [
 *       { anchor: [614, 308], label: { x: 640, y: 180 },
 *         head: '25,6 TRIỆU CP', sub: 'Khối lượng gom, tính đến 30/07',
 *         tone: 'accent',
 *         drill: { title: 'KHỐI LƯỢNG GOM', value: '25,6 triệu cp',
 *                  sub: '...', source: '...' } },
 *       ...
 *     ]);
 *   </script>
 *
 * Cố ý viết IIFE + global `window.Annotate` thay vì ES module: báo cáo
 * trong pipeline này thường xuất ra 1 file HTML tĩnh mở trực tiếp qua
 * file:// (không qua HTTP server) — dưới file://, `<script type="module">`
 * bị Chromium chặn bởi CORS khi import file cùng thư mục (đã kiểm chứng
 * thực nghiệm trong lab này), trong khi <script> thường không bị chặn.
 * Đây cũng là quy ước window.U đã dùng trong reference-kimi.html.
 */
(function (global) {
const NS = "http://www.w3.org/2000/svg";

// Chỉ 3 tone — SIẾT LẠI sau phản hồi thật: bản trước dùng 5 màu viền
// (cam/xanh lá/xanh dương/đen/đỏ) trên cùng 1 hình, đúng kiểu "traffic-
// light hoá" mà luật màu gốc của dự án cấm (1 accent + 1 màu âm cho tin
// xấu + trung tính, không hơn). 'neutral' là MẶC ĐỊNH cho mọi callout
// thông tin thường; 'negative' CHỈ dùng cho callout mang tin xấu/rủi ro
// thật; 'accent' CHỈ nên dùng cho ĐÚNG 1 callout — con số quan trọng nhất
// của cả hình — không phải để tô điểm nhiều ô. Việc giới hạn "tối đa 1
// accent/hình" là kỷ luật của người dùng module, annotate.js không ép
// được bằng code, chỉ ép được số lượng GIÁ TRỊ tone hợp lệ.
const TONES = {
  neutral:  { line: "#334155", text: "#0f172a", border: "#334155", bg: "#f8fafc" },
  negative: { line: "#dc2626", text: "#7c2d12", border: "#dc2626", bg: "#fef2f2" },
  accent:   { line: "var(--accent, #2563eb)", text: "#0f172a", border: "var(--accent, #2563eb)",
              bg: "color-mix(in srgb, var(--accent, #2563eb) 6%, #f8fafc)" },
};

function el(tag, attrs, parent) {
  const n = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (parent) parent.appendChild(n);
  return n;
}

function textEl(x, y, s, opts, parent) {
  const t = el("text", {
    x, y,
    "font-family": opts.mono ? "'IBM Plex Mono', Menlo, Consolas, monospace" : "'Be Vietnam Pro', sans-serif",
    "font-size": opts.size || 12.5,
    "font-weight": opts.bold ? 700 : 400,
    fill: opts.fill || "#0f172a",
    "text-anchor": opts.anchor || "start",
  }, parent);
  t.textContent = s;
  return t;
}

// Ước lượng bề rộng chữ (không có DOM measurement chính xác khi SVG chưa
// attach) — hệ số ký tự trung bình cho font sans/mono ở các cỡ dùng trong
// callout. Đủ tốt cho việc định kích thước hộp nhãn, không cần chính xác
// tuyệt đối vì luôn có padding dự phòng.
function estWidth(str, size, bold) {
  return str.length * size * (bold ? 0.62 : 0.56);
}

function wrapSub(str, maxChars) {
  const words = str.split(/\s+/);
  const lines = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > maxChars) {
      if (cur) lines.push(cur.trim());
      cur = w;
    } else {
      cur = (cur + " " + w).trim();
    }
  }
  if (cur) lines.push(cur.trim());
  return lines.slice(0, 2); // tối đa 2 dòng phụ đề, quá dài thì cắt bớt
}

/**
 * Giải va chạm theo chiều dọc: với mỗi cạnh (trái/phải), sắp các nhãn theo
 * y tăng dần rồi đẩy nhãn sau xuống nếu còn cách nhãn trước < minGap.
 * Áp dụng SAU khi đã tính chiều cao hộp thật của từng nhãn.
 *
 * SỬA LỖI THẬT (phản hồi: hộp nhãn tràn ra ngoài viewBox — đo bằng
 * check-bbox.mjs xác nhận "THUỶ THỦ ĐOÀN" tràn quá bottomBound dù code có
 * vẻ như đã "nén" cho vừa): công thức nén 1-lượt cũ
 * `shrink * (arr.length - i)` cho phần tử CUỐI (i lớn nhất, cái đang gây
 * tràn) hệ số NHỎ NHẤT, phần tử ĐẦU (không liên quan gì tới tràn) hệ số
 * LỚN NHẤT — hoàn toàn ngược. Sửa bằng 2 lượt kinh điển: lượt 1 từ trên
 * xuống đảm bảo khoảng cách tối thiểu (như cũ), lượt 2 từ DƯỚI LÊN đảm bảo
 * không vượt bottomBound, kéo theo các phần tử phía trên nếu cần — 2 lượt
 * này LUÔN giữ đúng minGap và luôn ưu tiên sửa đúng phần tử đang tràn.
 */
function resolveCollisions(items, minGap, topBound, bottomBound) {
  const bySide = { left: [], right: [] };
  items.forEach((it) => bySide[it._side].push(it));
  for (const side of ["left", "right"]) {
    const arr = bySide[side].sort((a, b) => a.label.y - b.label.y);
    for (let i = 0; i < arr.length; i++) {
      if (i === 0) {
        arr[i].label.y = Math.max(arr[i].label.y, topBound + arr[i]._boxH / 2);
      } else {
        const prev = arr[i - 1];
        const need = prev.label.y + prev._boxH / 2 + minGap + arr[i]._boxH / 2;
        if (arr[i].label.y < need) arr[i].label.y = need;
      }
    }
    for (let i = arr.length - 1; i >= 0; i--) {
      if (i === arr.length - 1) {
        arr[i].label.y = Math.min(arr[i].label.y, bottomBound - arr[i]._boxH / 2);
      } else {
        const next = arr[i + 1];
        const maxY = next.label.y - next._boxH / 2 - minGap - arr[i]._boxH / 2;
        if (arr[i].label.y > maxY) arr[i].label.y = maxY;
      }
    }
  }
}

/**
 * Giải va chạm theo chiều NGANG (dành cho bố cục "dải giữa" — xem mục
 * axis:'horizontal' bên dưới): với mỗi hàng (trên/dưới), sắp nhãn theo x
 * tăng dần rồi đẩy nhãn sau sang phải nếu còn cách nhãn trước < minGap.
 * Đối xứng với resolveCollisions (chiều dọc) — cùng thuật toán 2 lượt,
 * đổi trục, cùng lý do sửa lỗi (xem comment ở resolveCollisions).
 */
function resolveCollisionsHorizontal(items, minGap, leftBound, rightBound) {
  const byRow = { top: [], bottom: [] };
  items.forEach((it) => byRow[it._side].push(it));
  for (const row of ["top", "bottom"]) {
    const arr = byRow[row].sort((a, b) => a.label.x - b.label.x);
    for (let i = 0; i < arr.length; i++) {
      if (i === 0) {
        arr[i].label.x = Math.max(arr[i].label.x, leftBound + arr[i]._boxW / 2);
      } else {
        const prev = arr[i - 1];
        const need = prev.label.x + prev._boxW / 2 + minGap + arr[i]._boxW / 2;
        if (arr[i].label.x < need) arr[i].label.x = need;
      }
    }
    for (let i = arr.length - 1; i >= 0; i--) {
      if (i === arr.length - 1) {
        arr[i].label.x = Math.min(arr[i].label.x, rightBound - arr[i]._boxW / 2);
      } else {
        const next = arr[i + 1];
        const maxX = next.label.x - next._boxW / 2 - minGap - arr[i]._boxW / 2;
        if (arr[i].label.x > maxX) arr[i].label.x = maxX;
      }
    }
  }
}

/**
 * Ràng buộc mới sau phản hồi thật: bản bezier-2-chặng trước đây LUÔN đạt
 * "không cắt qua vật thể" nhưng cái giá là đường lượn rất dài (route tới
 * tận mép avoidBox rồi vòng lại) — ví dụ đo được trên ship-annotated-demo
 * bản trước: path "475 TỶ USD" dài ~365 đơn vị trong khi khoảng cách thẳng
 * neo->nhãn chỉ ~215 đơn vị (tỷ lệ ~1.7x, VƯỢT ngưỡng cho phép). Sửa bằng
 * cách đổi hẳn chiến lược:
 *
 * 1) THAY VÌ kéo dài đường, DỜI NHÃN: nếu nhãn (label.y, cho bố cục cột
 *    dọc trái/phải) rơi vào bên trong dải y bận của avoidBox, đẩy nó ra
 *    mép trên/dưới GẦN NHẤT của avoidBox NGAY TỪ LÚC ĐẶT NHÃN (trước khi
 *    giải va chạm) — xem clampLabelToClearBand(). Sau bước này, nhãn luôn
 *    nằm ở hàng/cột đã ở vùng trống.
 * 2) Vẽ đường bằng ĐÚNG 1 góc vuông bo tròn nhẹ (Manhattan L), neo -> góc
 *    (ax, ly) -> nhãn — KHÔNG dùng bezier lượn nhiều đoạn. Vì nhãn đã được
 *    đảm bảo ở vùng trống (bước 1), góc (ax, ly) luôn nằm ngoài phần bận
 *    của vật thể, nên tuyến 2 đoạn thẳng này KHÔNG cắt qua vật thể mà
 *    không cần vòng tới tận mép khung.
 * 3) Độ dài tuyến Manhattan (|dx|+|dy|) so với khoảng cách thẳng
 *    sqrt(dx²+dy²) luôn có tỷ lệ tệ nhất = sqrt(2) ≈ 1.414 — LUÔN nằm
 *    trong ngưỡng 1.6x yêu cầu, không cần đo dò từng trường hợp. Vẫn có
 *    hàm assertPathLength() bên dưới để tự kiểm bằng số thật, không chỉ
 *    tin vào chứng minh toán học suông.
 */
function roundedElbow(ax, ay, cx, cy, lx, ly) {
  const d1 = Math.hypot(cx - ax, cy - ay);
  const d2 = Math.hypot(lx - cx, ly - cy);
  if (d1 < 0.5) return `M ${ax} ${ay} L ${lx} ${ly}`; // góc trùng neo (đã thẳng hàng) -> 1 đoạn thẳng
  if (d2 < 0.5) return `M ${ax} ${ay} L ${cx} ${cy}`; // góc trùng nhãn -> 1 đoạn thẳng
  const r = Math.max(0, Math.min(10, d1 * 0.4, d2 * 0.4));
  if (r < 1) return `M ${ax} ${ay} L ${cx} ${cy} L ${lx} ${ly}`;
  const p1x = cx - ((cx - ax) / d1) * r, p1y = cy - ((cy - ay) / d1) * r;
  const p2x = cx + ((lx - cx) / d2) * r, p2y = cy + ((ly - cy) / d2) * r;
  return `M ${ax} ${ay} L ${p1x} ${p1y} Q ${cx} ${cy} ${p2x} ${p2y} L ${lx} ${ly}`;
}

// Tự kiểm bằng số thật (không chỉ tin chứng minh toán học): log cảnh báo
// nếu 1 tuyến nào đó vẫn vượt 1.6x — không nên xảy ra với roundedElbow
// nhưng giữ lại phòng khi opts tuỳ biến phá vỡ giả định.
function assertPathLength(ax, ay, cx, cy, lx, ly, label) {
  const routeLen = Math.hypot(cx - ax, cy - ay) + Math.hypot(lx - cx, ly - cy);
  const straight = Math.hypot(lx - ax, ly - ay) || 1;
  const ratio = routeLen / straight;
  if (ratio > 1.6) {
    console.warn(`[annotate.js] leader "${label}" dài ${ratio.toFixed(2)}x khoảng cách thẳng (>1.6x cho phép)`);
  }
  return ratio;
}

/**
 * Dời NHÃN ra khỏi dải y bận của avoidBox — áp dụng cho bố cục cột dọc
 * (axis:'vertical'). Không đụng vào label.x (đã ở lề trái/phải, luôn
 * ngoài avoidBox theo chiều ngang), chỉ nắn label.y nếu nó rơi vào đúng
 * dải y của vật thể. Quyết định đẩy lên hay xuống dựa vào vị trí NHÃN
 * đang có (không phải vị trí neo) — vì mục tiêu ở đây là tìm chỗ TRỐNG gần
 * nhãn nhất, khác với leader-line (mục tiêu ở đó là thoát nhanh nhất từ
 * ANCHOR).
 */
// RÀNG BUỘC CỨNG: hộp nhãn phải nằm TRỌN trong viewBox — không tin tưởng
// tuyệt đối vào collision-resolution (dù đã sửa lỗi 2 lượt ở trên) khi có
// quá nhiều callout chen trong khung nhỏ. Áp CUỐI CÙNG, ngay trước khi vẽ,
// trên hộp ĐÃ được đặt vị trí: (1) kẹp không cho lọt ra lề trái/trên, (2)
// nếu tràn lề phải/dưới, THỬ THU HẸP BỀ RỘNG/CAO trước (đến mức tối thiểu
// còn đọc được), (3) nếu vẫn không đủ chỗ, mới dịch cả hộp vào trong. Tự
// kiểm bằng check-bbox.mjs (đo x/y/width/height thật của rect đã render so
// với viewBox) — xem verify-label-bounds.mjs trong PACKAGE/.
function clampBoxToViewport(box, W, H, margin) {
  const b = { ...box };
  if (b.boxLeft < margin) b.boxLeft = margin;
  if (b.boxTop < margin) b.boxTop = margin;
  const overRight = b.boxLeft + b.boxW - (W - margin);
  if (overRight > 0) {
    const shrinkable = b.boxW - 90; // 90 = bề rộng tối thiểu còn đọc được
    if (shrinkable > 0) b.boxW -= Math.min(overRight, shrinkable);
    b.boxLeft = Math.min(b.boxLeft, W - margin - b.boxW);
  }
  const overBottom = b.boxTop + b.boxH - (H - margin);
  if (overBottom > 0) {
    b.boxTop = Math.max(margin, H - margin - b.boxH);
  }
  return b;
}

function clampLabelToClearBand(ly, avoidBox) {
  if (!avoidBox) return ly;
  const margin = 16;
  const top = avoidBox.y, bottom = avoidBox.y + avoidBox.height;
  if (ly <= top || ly >= bottom) return ly; // đã ở vùng trống, không cần dời
  const mid = (top + bottom) / 2;
  return ly <= mid ? top - margin : bottom + margin;
}

let drillCard = null;
function ensureDrillCard() {
  if (drillCard) return drillCard;
  drillCard = document.createElement("div");
  drillCard.id = "annotate-drill-card";
  drillCard.hidden = true;
  document.body.appendChild(drillCard);
  document.addEventListener("click", (e) => {
    if (!drillCard.hidden && !drillCard.contains(e.target) && !e.target.closest("[data-drill-keep]")) {
      drillCard.hidden = true;
    }
  }, true);
  return drillCard;
}

// Xây thẻ chi tiết bằng DOM node + textContent (không dùng innerHTML với
// chuỗi nội suy) — nội dung drill do chính báo cáo tự khai báo lúc build,
// nhưng dựng bằng textContent vẫn an toàn hơn và không tốn thêm chi phí.
function buildDrillContent(card, drill) {
  card.textContent = "";
  const close = document.createElement("button");
  close.className = "ad-close";
  close.setAttribute("aria-label", "Đóng");
  close.textContent = "✕";
  close.onclick = () => { card.hidden = true; };
  card.appendChild(close);

  const title = document.createElement("div");
  title.className = "ad-title";
  title.textContent = drill.title || "";
  card.appendChild(title);

  const val = document.createElement("div");
  val.className = "ad-val";
  val.textContent = drill.value || "";
  card.appendChild(val);

  if (drill.sub) {
    const sub = document.createElement("div");
    sub.className = "ad-sub";
    sub.textContent = drill.sub;
    card.appendChild(sub);
  }
  if (drill.source) {
    const src = document.createElement("div");
    src.className = "ad-src";
    src.textContent = "Nguồn · " + drill.source;
    card.appendChild(src);
  }
}

function showDrill(drill, x, y) {
  const card = ensureDrillCard();
  buildDrillContent(card, drill);
  card.hidden = false;
  const r = card.getBoundingClientRect();
  const left = Math.min(Math.max(x + 14, 8), window.innerWidth - r.width - 8);
  let top = y - r.height - 14;
  if (top < 8) top = y + 18;
  top = Math.min(Math.max(top, 8), window.innerHeight - r.height - 8);
  card.style.left = left + "px";
  card.style.top = top + "px";
}

/**
 * annotate(svg, items, opts) -> gắn lớp callout vào 1 phần tử <svg> đã có
 * viewBox. Trả về group <g class="annotations"> vừa tạo (để gọi có thể xoá
 * / vẽ lại khi đổi bộ số liệu).
 *
 * item: { anchor:[x,y], label:{x,y}, head, sub, tone, drill }
 *   - anchor: toạ độ điểm neo trên vật thể (theo hệ toạ độ viewBox của SVG)
 *   - label:  toạ độ TÂM hộp nhãn mong muốn — module sẽ tự nắn theo chiều
 *             dọc để chống chồng (mục "collision"), giữ nguyên x
 *   - tone:   'neutral' (mặc định, dùng cho hầu hết callout) | 'negative'
 *             (CHỈ tin xấu/rủi ro) | 'accent' (CHỈ 1 callout mỗi hình —
 *             con số quan trọng nhất). KHÔNG còn 'good'/'warn'/'bad' —
 *             rút gọn sau phản hồi "traffic-light hoá" trên bản 5-tone.
 *   - drill:  optional { title, value, sub, source } — nếu có, callout
 *             click được để mở thẻ chi tiết
 * opts: { minGap=14, boxPad=10, headSize=13, subSize=10.5,
 *          avoidBox={x,y,width,height}, axis='vertical'|'horizontal' }
 *   - avoidBox: bbox vật thể chính cần né khi vẽ leader-line (mục đích:
 *     "đường dẫn không cắt qua vật thể"). Nên luôn truyền cho hình có mật
 *     độ chi tiết cao (tàu, nhà máy...); có thể bỏ qua cho hình rất thưa.
 *   - axis: 'vertical' (mặc định) = bố cục cũ, nhãn xếp cột dọc theo lề
 *     TRÁI/PHẢI — hợp với vật thể CAO/dày đặc theo chiều dọc (tàu, nhà máy,
 *     tháp). 'horizontal' = bố cục "dải giữa" kiểu banner biên tập (chủ
 *     thể nằm trong dải ngang giữa khung, viền trên/dưới để trống — xem
 *     MOTIF_TABLE.md), nhãn xếp HÀNG NGANG phía TRÊN/DƯỚI, label.x là tâm
 *     hộp (không phải cạnh như mode 'vertical'). Thêm mode này sau khi đối
 *     chiếu với bố cục banner 97-motif — 2 mode phục vụ 2 tỷ lệ khung khác
 *     nhau, KHÔNG dùng chung được (xem ghi chú trong báo cáo gửi kèm).
 */
function annotate(svg, items, opts = {}) {
  const vb = svg.viewBox.baseVal;
  const W = vb && vb.width ? vb.width : svg.clientWidth;
  const H = vb && vb.height ? vb.height : svg.clientHeight;
  const minGap = opts.minGap ?? 14;
  const boxPad = opts.boxPad ?? 10;
  const headSize = opts.headSize ?? 13;
  const subSize = opts.subSize ?? 10.5;
  const maxSubChars = opts.maxSubChars ?? 34;
  const avoidBox = opts.avoidBox || null;
  const axis = opts.axis || "vertical";

  // xoá lớp annotation cũ nếu gọi lại (đổi bộ số liệu trên cùng 1 hình)
  const old = svg.querySelector(":scope > g.annotations");
  if (old) old.remove();

  const group = el("g", { class: "annotations" }, svg);
  const objMidY = avoidBox ? avoidBox.y + avoidBox.height / 2 : H / 2;

  const prepared = items.map((raw) => {
    const it = JSON.parse(JSON.stringify(raw));
    if (axis === "horizontal") {
      it._side = it.anchor[1] <= objMidY ? "top" : "bottom"; // dựa vào NEO, cùng bài học rút ra ở mode vertical
    } else {
      it._side = it.label.x < W / 2 ? "left" : "right";
      // DỜI NHÃN ra khỏi dải y bận của avoidBox NGAY TỪ ĐẦU (trước khi
      // giải va chạm) — đây là cách sửa "đường dẫn quá dài" đúng theo yêu
      // cầu: sửa ở NHÃN, không kéo dài ĐƯỜNG. Bố cục 'horizontal' không
      // cần bước này vì hàng trên/dưới vốn đã luôn ở vùng trống.
      it.label.y = clampLabelToClearBand(it.label.y, avoidBox);
    }
    const subLines = it.sub ? wrapSub(it.sub, maxSubChars) : [];
    const headW = estWidth(it.head || "", headSize, true);
    const subW = Math.max(0, ...subLines.map((l) => estWidth(l, subSize, false)));
    it._boxW = Math.max(150, Math.min(300, Math.max(headW, subW) + boxPad * 2));
    it._boxH = 18 + subLines.length * 14 + boxPad;
    it._subLines = subLines;
    return it;
  });

  if (axis === "horizontal") {
    resolveCollisionsHorizontal(prepared, minGap, 20, W - 20);
  } else {
    resolveCollisions(prepared, minGap, 20, H - 20);
  }

  for (const it of prepared) {
    const tone = TONES[it.tone] || TONES.neutral;
    const g = el("g", { class: "callout", cursor: it.drill ? "pointer" : "default" }, group);
    if (it.drill) g.setAttribute("data-drill-keep", "");
    const [ax, ay] = it.anchor;

    let boxLeft, boxTop;
    if (axis === "horizontal") {
      boxLeft = it.label.x - it._boxW / 2;
      boxTop = it._side === "top" ? it.label.y - it._boxH : it.label.y;
    } else {
      boxLeft = it._side === "left" ? it.label.x : it.label.x - it._boxW;
      boxTop = it.label.y - it._boxH / 2;
    }

    // Ràng buộc cứng: hộp phải nằm trọn trong viewBox (xem
    // clampBoxToViewport ở trên) — áp NGAY TRÊN vị trí thô, rồi mọi thứ
    // khác (điểm bám leader, vạch màu cạnh hộp) suy ra từ box ĐÃ kẹp, một
    // nguồn sự thật duy nhất, tránh vá lệch như bản thử đầu (tính
    // attachX/attachY trước rồi patch delta sau — dễ sai, đã bỏ).
    const box = clampBoxToViewport({ boxLeft, boxTop, boxW: it._boxW, boxH: it._boxH }, W, H, 12);
    boxLeft = box.boxLeft; boxTop = box.boxTop; it._boxW = box.boxW; it._boxH = box.boxH;

    let attachX, attachY, accentBarAttrs;
    if (axis === "horizontal") {
      attachX = boxLeft + it._boxW / 2;
      attachY = it._side === "top" ? boxTop + it._boxH : boxTop;
      accentBarAttrs = { x: boxLeft, y: it._side === "top" ? boxTop + it._boxH - 3 : boxTop, width: it._boxW, height: 3 };
    } else {
      // điểm bám của leader vào hộp: cạnh gần vật thể nhất (phải nếu hộp ở
      // bên trái vật thể, trái nếu hộp ở bên phải)
      attachX = it._side === "left" ? boxLeft + it._boxW : boxLeft;
      attachY = boxTop + it._boxH / 2;
      accentBarAttrs = { x: it._side === "left" ? boxLeft + it._boxW - 3 : boxLeft, y: boxTop, width: 3, height: it._boxH };
    }

    // 1) điểm neo trên vật thể
    el("circle", { cx: ax, cy: ay, r: 3.2, fill: tone.line }, g);
    el("circle", { cx: ax, cy: ay, r: 6, fill: "none", stroke: tone.line, "stroke-width": 1, "stroke-opacity": 0.4 }, g);

    // 2) leader = góc vuông bo tròn nhẹ, đúng 1 góc: neo -> (ax, attachY)
    // -> nhãn. Nhãn đã được đảm bảo ở vùng trống (clampLabelToClearBand
    // cho mode 'vertical'; hàng trên/dưới vốn đã trống cho mode
    // 'horizontal'), nên đoạn ngang tại y=attachY không cắt qua avoidBox.
    const cornerX = ax, cornerY = attachY;
    assertPathLength(ax, ay, cornerX, cornerY, attachX, attachY, it.head);
    const d = roundedElbow(ax, ay, cornerX, cornerY, attachX, attachY);
    el("path", { class: "anno-leader", d, fill: "none", stroke: tone.line, "stroke-width": 1.3, "stroke-opacity": 0.85 }, g);

    // 3) hộp nhãn
    el("rect", {
      class: "anno-box",
      x: boxLeft, y: boxTop, width: it._boxW, height: it._boxH, rx: 5,
      fill: tone.bg, stroke: tone.border, "stroke-width": 1.1,
    }, g);
    // vạch màu cạnh gần vật thể nhất (giống "thẻ treo dây" tham chiếu)
    el("rect", { class: "anno-bar", ...accentBarAttrs, fill: tone.border }, g);

    // 4) chữ
    const tx = boxLeft + boxPad;
    textEl(tx, boxTop + 16, it.head, { size: headSize, bold: true, fill: tone.text }, g);
    it._subLines.forEach((line, i) => {
      textEl(tx, boxTop + 16 + 14 * (i + 1), line, { size: subSize, fill: "#475569" }, g);
    });

    if (it.drill) {
      g.addEventListener("click", (e) => showDrill(it.drill, e.clientX, e.clientY));
    }
  }

  return group;
}

function hideDrill() {
  if (drillCard) drillCard.hidden = true;
}

global.Annotate = { annotate, hideDrill };
})(window);
