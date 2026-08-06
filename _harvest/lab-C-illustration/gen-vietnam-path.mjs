// gen-vietnam-path.mjs — sinh path SVG THẬT cho bản đồ Việt Nam từ dữ liệu
// biên giới thật (world-atlas, backed by Natural Earth), thay cho cách
// tay-gõ toạ độ đã bị bác bỏ (đọc ra "amip", không ra chữ S).
import * as topojson from "topojson-client";
import * as topoSimplify from "topojson-simplify";
import * as d3geo from "d3-geo";
import fs from "node:fs";
import path from "node:path";

const DIR = path.resolve(new URL(".", import.meta.url).pathname);
const PIPELINE_LAB = path.resolve(DIR, "../pipeline-lab");

let topo = JSON.parse(fs.readFileSync(path.join(PIPELINE_LAB, "node_modules/world-atlas/countries-50m.json"), "utf8"));

// Đơn giản hoá THẬT bằng topojson-simplify (Visvalingam's area) thay vì vẽ
// tay lại — giữ đúng hình dạng biên giới thật, chỉ bỏ bớt điểm ít quan
// trọng thị giác. minWeight chọn qua thử-sai: đủ nhỏ để giữ nét "chữ S",
// đủ lớn để không còn 555 điểm (quá dày cho 1 icon).
const SIMPLIFY_WEIGHT = process.env.SIMPLIFY_WEIGHT ? Number(process.env.SIMPLIFY_WEIGHT) : 0.0000012;
topo = topoSimplify.presimplify(topo);
topo = topoSimplify.simplify(topo, SIMPLIFY_WEIGHT);

const geoms = topo.objects.countries.geometries;
const vnGeom = geoms.find((g) => g.id === "704");
if (!vnGeom) throw new Error("Không tìm thấy Việt Nam (id=704) trong world-atlas");

const vnFeature = topojson.feature(topo, vnGeom);
console.log("Kiểu geometry:", vnFeature.geometry.type);
console.log("Số ring (đường viền con, gồm cả đảo):", vnFeature.geometry.type === "MultiPolygon" ? vnFeature.geometry.coordinates.length : 1);

// Đếm tổng điểm trước khi đơn giản hoá, để biết mật độ gốc
function countPoints(geom) {
  let n = 0;
  const rings = geom.type === "MultiPolygon" ? geom.coordinates.flat() : geom.coordinates;
  rings.forEach((r) => (n += r.length));
  return n;
}
console.log("Tổng điểm gốc (50m):", countPoints(vnFeature.geometry));

// Chỉ giữ phần lục địa lớn nhất (bỏ các đảo nhỏ rời rạc như Phú Quốc, Hoàng
// Sa/Trường Sa dạng chấm) để hình đọc gọn như 1 khối "chữ S" duy nhất, đúng
// tinh thần "đơn giản hoá" — nếu cần giữ đảo, bỏ bước lọc này.
let mainGeom = vnFeature.geometry;
if (mainGeom.type === "MultiPolygon") {
  const polys = mainGeom.coordinates;
  const areaOf = (poly) => {
    const ring = poly[0];
    let a = 0;
    for (let i = 0; i < ring.length - 1; i++) a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
    return Math.abs(a / 2);
  };
  const sorted = polys.map((p, i) => ({ i, area: areaOf(p) })).sort((a, b) => b.area - a.area);
  console.log("Số polygon con:", polys.length, "— top 5 diện tích (độ^2, xấp xỉ):", sorted.slice(0, 5).map((s) => s.area.toFixed(2)));
  mainGeom = { type: "Polygon", coordinates: polys[sorted[0].i] };
}
console.log("Điểm sau khi chỉ giữ lục địa chính:", countPoints(mainGeom));

const W = 400, H = 700;
const projection = d3geo.geoMercator().fitExtent([[24, 24], [W - 24, H - 24]], mainGeom);
const pathGen = d3geo.geoPath(projection);
const d = pathGen(mainGeom);

fs.writeFileSync(path.join(DIR, "vietnam-path-raw.txt"), d);
console.log("\nĐã ghi vietnam-path-raw.txt, độ dài chuỗi path:", d.length, "ký tự");

// Toạ độ vài mốc để đặt marker thành phố (Hà Nội, Đà Nẵng, TP.HCM) — project
// qua CÙNG 1 phép chiếu để khớp với path vừa sinh.
const CITIES = {
  "Hà Nội": [105.8342, 21.0278],
  "Đà Nẵng": [108.2208, 16.0544],
  "TP.HCM": [106.6297, 10.8231],
};
for (const [name, lonlat] of Object.entries(CITIES)) {
  const [x, y] = projection(lonlat);
  console.log(name, "->", x.toFixed(1), y.toFixed(1));
}
