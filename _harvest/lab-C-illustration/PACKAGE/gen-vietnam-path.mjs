// gen-vietnam-path.mjs — sinh path SVG THẬT cho bản đồ Việt Nam từ dữ liệu
// biên giới thật (world-atlas, backed by Natural Earth), thay cho cách
// tay-gõ toạ độ (đã thử và bị bác bỏ hai lần: bản tay-gõ đọc ra "khối
// amip", không ra chữ S — xem grammar.md mục 9).
//
// PHỤ THUỘC (cài 1 lần, đứng cạnh package.json bất kỳ có node_modules mà
// script này chạy từ trong hoặc dưới thư mục đó):
//   npm install d3-geo topojson-client topojson-simplify world-atlas
//
// CHẠY:
//   node gen-vietnam-path.mjs                    # mặc định SIMPLIFY_WEIGHT=0.05 (~72 điểm)
//   SIMPLIFY_WEIGHT=0.02 node gen-vietnam-path.mjs   # chi tiết hơn (~118 điểm)
//   SIMPLIFY_WEIGHT=0.1  node gen-vietnam-path.mjs   # đơn giản hơn (~50 điểm)
// Kết quả: in path "d" ra stdout + ghi vietnam-path-raw.txt cạnh script, và
// in toạ độ 3 mốc thành phố (Hà Nội/Đà Nẵng/TP.HCM) đã chiếu cùng hệ để
// dán trực tiếp vào <circle>/<text> trong SVG.
//
// TÁI SỬ DỤNG CHO QUỐC GIA/VÙNG KHÁC: đổi ID trong `geoms.find(g => g.id
// === "704")` sang mã ISO numeric của nước khác (vd Thái Lan = "764",
// Indonesia = "360" — tra trong node_modules/world-atlas/README.md hoặc
// http://www.opengeocode.org/cude.php), đổi W/H/toạ độ CITIES cho phù hợp.
import { createRequire } from "node:module";
import * as topojson from "topojson-client";
import * as topoSimplify from "topojson-simplify";
import * as d3geo from "d3-geo";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(import.meta.url);
const DIR = path.resolve(new URL(".", import.meta.url).pathname);

// require.resolve() tự đi tìm node_modules/world-atlas theo CHUẨN Node.js
// (leo dần thư mục cha từ vị trí script) — KHÔNG hardcode đường dẫn tương
// đối tới 1 thư mục anh em cụ thể như bản nháp đầu (lỗi nếu di chuyển
// script sang thư mục khác có độ sâu khác).
const worldAtlasPath = require.resolve("world-atlas/countries-50m.json");
let topo = JSON.parse(fs.readFileSync(worldAtlasPath, "utf8"));

// Đơn giản hoá THẬT bằng topojson-simplify (Visvalingam's area) thay vì vẽ
// tay lại — giữ đúng hình dạng biên giới thật, chỉ bỏ bớt điểm ít quan
// trọng thị giác.
const SIMPLIFY_WEIGHT = process.env.SIMPLIFY_WEIGHT ? Number(process.env.SIMPLIFY_WEIGHT) : 0.05;
topo = topoSimplify.presimplify(topo);
topo = topoSimplify.simplify(topo, SIMPLIFY_WEIGHT);

const COUNTRY_ID = process.env.COUNTRY_ID || "704"; // 704 = Việt Nam
const geoms = topo.objects.countries.geometries;
const countryGeom = geoms.find((g) => g.id === COUNTRY_ID);
if (!countryGeom) throw new Error(`Không tìm thấy quốc gia id=${COUNTRY_ID} trong world-atlas`);

const feature = topojson.feature(topo, countryGeom);
console.error("Kiểu geometry:", feature.geometry.type);

function countPoints(geom) {
  let n = 0;
  const rings = geom.type === "MultiPolygon" ? geom.coordinates.flat() : geom.coordinates;
  rings.forEach((r) => (n += r.length));
  return n;
}
console.error("Tổng điểm sau simplify:", countPoints(feature.geometry));

// Chỉ giữ phần lục địa lớn nhất (bỏ đảo rời) để hình đọc gọn như 1 khối
// duy nhất — bỏ bước lọc này (comment lại khối if) nếu ngành cần giữ đảo.
let mainGeom = feature.geometry;
if (mainGeom.type === "MultiPolygon") {
  const polys = mainGeom.coordinates;
  const areaOf = (poly) => {
    const ring = poly[0];
    let a = 0;
    for (let i = 0; i < ring.length - 1; i++) a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
    return Math.abs(a / 2);
  };
  const sorted = polys.map((p, i) => ({ i, area: areaOf(p) })).sort((a, b) => b.area - a.area);
  console.error("Số polygon con:", polys.length, "— giữ polygon lớn nhất");
  mainGeom = { type: "Polygon", coordinates: polys[sorted[0].i] };
}
console.error("Điểm sau khi chỉ giữ lục địa chính:", countPoints(mainGeom));

const W = Number(process.env.OUT_WIDTH) || 400;
const H = Number(process.env.OUT_HEIGHT) || 700;
const projection = d3geo.geoMercator().fitExtent([[24, 24], [W - 24, H - 24]], mainGeom);
const pathGen = d3geo.geoPath(projection);
const d = pathGen(mainGeom);

fs.writeFileSync(path.join(DIR, "vietnam-path-raw.txt"), d);
console.error("\nĐã ghi vietnam-path-raw.txt, độ dài chuỗi path:", d.length, "ký tự");
console.log(d); // stdout: chỉ path "d", tiện pipe vào file/script khác

const CITIES = {
  "Hà Nội": [105.8342, 21.0278],
  "Đà Nẵng": [108.2208, 16.0544],
  "TP.HCM": [106.6297, 10.8231],
};
console.error("\nToạ độ mốc (đã chiếu, dán thẳng vào <circle cx cy>):");
for (const [name, lonlat] of Object.entries(CITIES)) {
  const [x, y] = projection(lonlat);
  console.error(" ", name, "->", x.toFixed(1), y.toFixed(1));
}
