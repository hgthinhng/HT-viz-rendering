/* ═══════════════════════════════════════════════════════════════════════
   components.js, hành vi tối thiểu cho thư viện component kể chuyện.
   Nguyên tắc: mọi hành vi ở đây là TĂNG CƯỜNG (progressive enhancement).
   Nếu JS tắt hoặc khi in, mỗi component phải vẫn đọc được (xem CSS
   .no-js / @media print trong components.css).
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  // JS chạy được ⇒ bỏ lớp giả định "không JS" trên <html>
  document.documentElement.classList.remove("no-js");

  var REDUCE = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 1. Drill-card: bấm vào cụm .drillable để bung/thu .drill-panel kế bên ── */
  function initDrillables() {
    document.querySelectorAll(".drillable").forEach(function (el) {
      var panel = el.parentElement.querySelector(".drill-panel");
      if (!panel) return;
      var id = panel.id || ("drill-" + Math.random().toString(36).slice(2, 9));
      panel.id = id;
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "0");
      el.setAttribute("aria-expanded", "false");
      el.setAttribute("aria-controls", id);
      function toggle() {
        var open = panel.classList.toggle("open");
        el.setAttribute("aria-expanded", open ? "true" : "false");
      }
      el.addEventListener("click", toggle);
      el.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); toggle(); }
      });
    });
  }

  /* ── 2. Wall-chart timeline: thuật toán xếp lớp chống chồng nhãn ──────────
     Kỹ thuật vay mượn có kiểm chứng từ reference-kimi.html (thuật toán
     "greedy layering": mỗi mốc thử đặt ở lane thấp nhất còn trống quanh vị
     trí năm của nó; nếu chồng lấn lane hiện tại, đẩy sang lane cao hơn).
     Khác biệt so với bản gốc: đo bằng offsetWidth thật của DOM (2 lượt:
     dựng ẩn rồi đo), không ước lượng theo số ký tự × hệ số, chính xác hơn
     với font Spectral biến thiên độ rộng theo từng chữ cái có dấu.       */
  function buildWallChart(root, data) {
    var y0 = data.y0, y1 = data.y1;
    var pct = function (yr) { return (yr - y0) / (y1 - y0); };

    var erasEl = root.querySelector(".wc-eras");
    var ticksEl = root.querySelector(".wc-ticks");
    var layer = root.querySelector(".wc-plaque-layer");
    var fallback = root.querySelector(".wc-fallback-list");
    if (!erasEl || !layer) return;

    // Band các "kỷ nguyên"
    erasEl.innerHTML = "";
    data.eras.forEach(function (e) {
      var d = document.createElement("div");
      d.className = "wc-era" + (e.now ? " now" : "");
      d.style.flexBasis = ((pct(e.b) - pct(e.a)) * 100) + "%";
      d.textContent = e.label;
      erasEl.appendChild(d);
    });

    // Vạch năm
    ticksEl.innerHTML = "";
    ticksEl.style.position = "relative";
    for (var yr = Math.ceil(y0 / 4) * 4; yr <= y1; yr += 4) {
      var t = document.createElement("span");
      t.style.cssText = "position:absolute;top:2px;font-family:var(--font-mono);font-size:9px;color:var(--ink-lo);transform:translateX(-50%);";
      t.style.left = (pct(yr) * 100) + "%";
      t.textContent = yr;
      ticksEl.appendChild(t);
    }

    // Plaques, lượt 1: dựng ẩn để đo offsetWidth thật
    layer.innerHTML = "";
    layer.style.position = "relative";
    var containerW = layer.clientWidth || root.clientWidth || 880;
    var rowH = 58;

    // Lưu ý accessibility: khối .wc-axis-wrap cha mang aria-hidden="true" (xem
    // gallery.html), bản trực quan này chỉ dành cho mắt nhìn, KHÔNG gắn
    // tabindex/role tương tác ở đây (phần tử focusable bên trong nhánh
    // aria-hidden là lỗi a11y, screen reader "thấy" ô trống nhưng không đọc
    // được nội dung). Nội dung đọc được thật nằm ở .wc-fallback-list.
    var built = data.events.map(function (e) {
      var el = document.createElement("div");
      el.className = "wc-plaque";
      el.dataset.cls = e.cls || "base";
      el.innerHTML = '<span class="wc-y">' + e.y + "</span><br><span class=\"wc-t\">" + e.t + "</span>";
      el.style.visibility = "hidden";
      el.style.left = "0px";
      layer.appendChild(el);
      return { e: e, el: el };
    });
    built.forEach(function (b) { b.w = b.el.offsetWidth; });

    // Lượt 2: thuật toán greedy layering theo px thật
    var laneEnds = [];
    built.forEach(function (b) {
      var cx = pct(b.e.y) * containerW;
      var lx = Math.max(2, Math.min(cx - b.w / 2, containerW - b.w - 2));
      var lane = 0;
      while (lane < 8 && laneEnds[lane] !== undefined && lx < laneEnds[lane] + 8) lane++;
      laneEnds[lane] = lx + b.w;
      b.lane = lane;
      b.lx = lx;
      b.cx = cx;
    });
    var maxLane = built.reduce(function (m, b) { return Math.max(m, b.lane); }, 0);
    var layerH = (maxLane + 1) * rowH + 6;
    layer.style.height = layerH + "px";

    built.forEach(function (b) {
      var top = layerH - (b.lane + 1) * rowH;
      b.el.style.left = b.lx + "px";
      b.el.style.top = top + "px";
      b.el.style.visibility = "visible";

      var stem = document.createElement("div");
      stem.className = "wc-stem";
      stem.style.left = b.cx + "px";
      stem.style.bottom = "0px";
      stem.style.height = (layerH - (top + b.el.offsetHeight)) + "px";
      stem.setAttribute("aria-hidden", "true");
      layer.appendChild(stem);
    });

    // Fallback: danh sách phẳng, hiển thị khi in hoặc khi JS tắt (đảm bảo
    // không có mốc nào "biến mất" khỏi bản in dù thuật toán layer có chạy hay không).
    if (fallback) {
      var ol = document.createElement("ol");
      ol.className = "toc-milestone";
      data.events.forEach(function (e, i) {
        var li = document.createElement("li");
        li.dataset.status = e.cls === "risk" ? "cho" : (e.cls === "now" ? "live" : "done");
        li.innerHTML =
          '<span class="toc-title">' + e.y + " · " + e.t +
          "<small>" + (e.d || "") + '</small></span><span class="toc-mark">' +
          (e.cls === "risk" ? "SIẾT" : e.cls === "now" ? "MỞ" : "NỀN") + "</span>";
        ol.appendChild(li);
      });
      fallback.innerHTML = "";
      fallback.appendChild(ol);
    }
  }

  /* ── 3. Khởi chạy khi DOM sẵn sàng + tái tính khi resize (responsive) ──── */
  function boot() {
    initDrillables();
    var wc = document.getElementById("wallchart-shipping");
    if (wc && window.WALLCHART_DATA) {
      buildWallChart(wc, window.WALLCHART_DATA);
      if (!REDUCE && "ResizeObserver" in window) {
        var ro = new ResizeObserver(function () {
          buildWallChart(wc, window.WALLCHART_DATA);
        });
        ro.observe(wc);
      } else {
        window.addEventListener("resize", function () { buildWallChart(wc, window.WALLCHART_DATA); });
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  // Trước khi in: đảm bảo layout wall-chart đã tính đúng theo bề rộng trang in.
  window.addEventListener("beforeprint", function () {
    var wc = document.getElementById("wallchart-shipping");
    if (wc && window.WALLCHART_DATA) buildWallChart(wc, window.WALLCHART_DATA);
  });
})();
