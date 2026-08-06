# -*- coding: utf-8 -*-
"""
Thực nghiệm mổ xẻ opvia-data-viz + opvia-deepanalysis-polish.
Chủ đề mẫu: "Sửa Thông tư 22/2019 và tác động dây chuyền tới nhóm vận tải biển
niêm yết" (ngân hàng VN + vận tải biển VN, tiếng Việt có dấu đầy đủ).
"""
import os
import sys

LAB = "/tmp/claude-1000/-home-hgthinhng/28783fef-7078-47d7-af0a-c84d36f8435e/scratchpad/lab-opvia"
DATAVIZ = os.path.join(LAB, "opvia-data-viz")
POLISH = os.path.join(LAB, "opvia-deepanalysis-polish")

sys.path.insert(0, DATAVIZ)
sys.path.insert(0, POLISH)

import viz
import viz_wave8 as w8
import viz_wave9 as w9
import viz_wave10 as w10
import validators
import render as polish_render

components_rendered = []
errors = []

def safe_call(name, fn, *args, **kwargs):
    try:
        html = fn(*args, **kwargs)
        components_rendered.append(name)
        print(f"OK   {name:28s} -> {len(html):6d} ky tu HTML")
        return html
    except Exception as e:
        errors.append((name, repr(e)))
        print(f"FAIL {name:28s} -> {e!r}")
        return f"<!-- LOI render {name}: {e!r} -->"


# ---------------------------------------------------------------------------
# 1. cover_deep_page -- HTML thu cong theo DUNG class CSS that trong render.py
#    (khong dung literal class trong catalog/cover_deep_page.md vi da lech)
# ---------------------------------------------------------------------------
cover_html = """
<section class="cover-deep">
  <div class="cover-masthead">
    <div class="masthead-rule-top"></div>
    <div class="masthead-brand">OPVIA ACADEMY</div>
    <div class="masthead-rule-mid"></div>
    <div class="masthead-meta">
      <span class="meta-left">Ngân hàng &amp; Vận tải biển</span>
      <span class="meta-right">Số tháng 8 · 2026</span>
    </div>
  </div>
  <h1>Sửa Thông tư 22 và cơn khát vốn của đội tàu Việt Nam</h1>
  <p class="cover-subtitle">Ai được vay rẻ hơn để đóng tàu, ai bị siết lại?</p>
  <p class="cover-dek">
    Khi LDR hệ thống chạm 111,9% và NHNN cân nhắc nới trần SFL cho nhóm vận tải biển,
    ba doanh nghiệp niêm yết HAH, VOS, PVT đứng trước ngã ba: được bơm vốn giá rẻ để
    thay đội tàu cũ, hay tiếp tục vay ngoại tệ đắt đỏ từ ngân hàng nước ngoài.
  </p>
  <div class="cover-hero-stat">
    <div class="cover-hero-num">111,9%</div>
    <div class="cover-hero-cap">
      <div class="cover-hero-label">TỶ LỆ LDR HỆ THỐNG · 30/6/2026</div>
      <div class="cover-hero-desc">Vượt xa trần quy chế 85% - tín hiệu hệ thống đang căng, room tín dụng tàu biển bị bóp nghẹt.</div>
    </div>
  </div>
  <div class="cover-takeaways">
    <div class="cover-takeaways-label">TRONG BÀI NÀY</div>
    <ul>
      <li><strong>Tái phân phối, không phải nới lỏng.</strong> Sửa Thông tư 22 chỉnh quy tắc kỹ thuật, không bơm thêm tiền vào hệ thống.</li>
      <li><strong>Ba mã vận tải biển chịu tác động trái chiều.</strong> PVT hưởng lợi rõ nhất, VOS rủi ro tái cấp vốn cao nhất.</li>
      <li><strong>Cửa sổ chính sách hẹp, chỉ 2 quý.</strong> Sau Q1/2027 áp lực tỷ giá có thể đảo ngược toàn bộ lợi thế.</li>
    </ul>
  </div>
  <div class="cover-bottom-rule"></div>
  <div class="cover-meta-strip">
    <div class="meta-block"><strong>BIÊN SOẠN</strong>OPVIA ACADEMY</div>
    <div class="meta-block"><strong>ĐỌC TRONG</strong>12 PHÚT</div>
    <div class="meta-block"><strong>PHÁT HÀNH</strong>06/08/2026</div>
  </div>
</section>
"""
components_rendered.append("cover_deep_page (thu cong, class that)")

# ---------------------------------------------------------------------------
# 2. data_hero
# ---------------------------------------------------------------------------
data_hero_html = safe_call(
    "data_hero", viz.data_hero,
    eyebrow="ĐIỂM NHẤN CHÍNH SÁCH",
    mega_value="111,9",
    mega_unit="%",
    mega_label="LDR hệ thống ngân hàng Q2/2026, vượt trần 85% quy định",
    sub_stats=[
        {"value": "35%", "label": "Trần SFL hiện hành"},
        {"value": "+8 đp", "label": "Đề xuất nới cho tàu biển"},
    ],
    story="Room tín dụng đóng tàu mới bị bó hẹp do hệ thống ngân hàng đã sát trần thanh khoản.",
)

# ---------------------------------------------------------------------------
# 3. gauge
# ---------------------------------------------------------------------------
gauge_html = safe_call(
    "gauge", viz.gauge,
    value=111.9, max_val=130, threshold=85,
    label="TỶ LỆ LDR HỆ THỐNG NGÂN HÀNG",
    description="Vượt xa trần quy chế 85%, tín hiệu hệ thống đang căng thanh khoản.",
    danger_above=85,
    annotations=[{"target": "value", "text": "Vượt trần 26,9 điểm", "position": "right"}],
)

# ---------------------------------------------------------------------------
# 4. bar_horizontal
# ---------------------------------------------------------------------------
bar_html = safe_call(
    "bar_horizontal", viz.bar_horizontal,
    items=[
        {"label": "VPB", "value": 28.3, "warn": True, "note": "Sát trần SFL"},
        {"label": "PVT", "value": 19.5, "positive": True, "note": "Room còn rộng"},
        {"label": "HAH", "value": 24.1, "note": "Trung bình ngành"},
        {"label": "VOS", "value": 31.8, "danger": True, "note": "Vượt trần đề xuất"},
        {"label": "GMD", "value": 22.0},
    ],
    threshold=30, threshold_label="Trần SFL đề xuất",
    title="Tỷ lệ SFL (Short-term Funding for Long-term lending) theo mã",
    subtitle="Dữ liệu minh hoạ Q2/2026, đơn vị %",
)

# ---------------------------------------------------------------------------
# 5. heatmap
# ---------------------------------------------------------------------------
heatmap_html = safe_call(
    "heatmap", viz.heatmap,
    rows=["PVT", "HAH", "VOS", "Big4 (bình quân)"],
    cols=["LDR Q1/2026", "LDR Q2/2026", "Delta (đp)"],
    cells=[
        [{"text": "92,0%", "color": "neutral"}, {"text": "94,5%", "color": "pos"}, {"text": "+2,5", "color": "pos"}],
        [{"text": "88,0%", "color": "neutral"}, {"text": "89,5%", "color": "neutral"}, {"text": "+1,5", "color": "neutral"}],
        [{"text": "101,0%", "color": "neg"}, {"text": "108,2%", "color": "neg-strong"}, {"text": "+7,2", "color": "neg-strong"}],
        [{"text": "108,5%", "color": "neg"}, {"text": "111,9%", "color": "neg-strongest"}, {"text": "+3,4", "color": "neg"}],
    ],
    title="Ai hưởng lợi, ai chịu thiệt: LDR theo mã vận tải biển",
    subtitle="So sánh trước/sau đề xuất sửa Thông tư 22",
)

# ---------------------------------------------------------------------------
# 6. waterfall
# ---------------------------------------------------------------------------
waterfall_html = safe_call(
    "waterfall", viz.waterfall,
    title="Cầu nối chi phí vốn vay đóng tàu PVT, trước và sau đề xuất",
    start={"label": "Chi phí vốn hiện hành", "value": 8.5},
    steps=[
        {"label": "Nới trần SFL +8đp", "value": -0.9},
        {"label": "Tỷ giá USD/VND tăng", "value": 0.4},
        {"label": "Phí bảo lãnh tín dụng xuất khẩu", "value": 0.2},
    ],
    end={"label": "Chi phí vốn dự kiến", "value": 8.2},
    value_format="{:.1f}%",
    subtitle="Đơn vị: %/năm, minh hoạ",
)

# ---------------------------------------------------------------------------
# 7. risk_radar
# ---------------------------------------------------------------------------
risk_radar_html = safe_call(
    "risk_radar", viz.risk_radar,
    title="Hồ sơ rủi ro VOS so với mục tiêu ngành",
    dimensions=[
        {"label": "Rủi ro thanh khoản", "current": 0.85, "target": 0.5},
        {"label": "Rủi ro tỷ giá", "current": 0.7, "target": 0.4},
        {"label": "Rủi ro tái cấp vốn", "current": 0.9, "target": 0.45},
        {"label": "Rủi ro giá cước", "current": 0.6, "target": 0.5},
        {"label": "Rủi ro đội tàu già", "current": 0.75, "target": 0.35},
    ],
)

# ---------------------------------------------------------------------------
# 8. line_with_annotations (wave8) - chi so cuoc van tai
# ---------------------------------------------------------------------------
line_html = safe_call(
    "line_with_annotations", w8.line_with_annotations,
    series=[{
        "name": "Chỉ số cước tàu hàng rời (BDI, quy đổi)",
        "color": "#003153",
        "data": [
            ("T1/25", 1450), ("T4/25", 1620), ("T7/25", 1980),
            ("T10/25", 2340), ("T1/26", 2100), ("T4/26", 2510), ("T7/26", 2780),
        ],
    }],
    annotations=[
        {"x_index": 3, "text": "Đỉnh mùa cao điểm Q4/2025", "anchor": "above"},
        {"x_index": 6, "text": "Kỳ vọng đề xuất TT22 thông qua", "anchor": "above"},
    ],
    title="Chỉ số cước vận tải hàng rời và kỳ vọng chính sách",
    y_label="Điểm chỉ số", y_unit="",
)

# ---------------------------------------------------------------------------
# 9. sankey_mini (wave8) - dong von
# ---------------------------------------------------------------------------
sankey_html = safe_call(
    "sankey_mini", w8.sankey_mini,
    sources=[
        {"id": "tien_gui", "label": "Tiền gửi <12 tháng", "color": "#003153"},
        {"id": "von_nn", "label": "Vốn vay nước ngoài", "color": "#4A6FA5"},
    ],
    targets=[
        {"id": "dong_tau", "label": "Tín dụng đóng tàu", "color": "#B5A642"},
        {"id": "khac", "label": "Lĩnh vực khác", "color": "#722F37"},
    ],
    flows=[
        {"source": "tien_gui", "target": "dong_tau", "value": 320},
        {"source": "tien_gui", "target": "khac", "value": 480},
        {"source": "von_nn", "target": "dong_tau", "value": 150},
        {"source": "von_nn", "target": "khac", "value": 90},
    ],
    title="Dòng vốn tín dụng đóng tàu, minh hoạ",
    unit="tỷ VND",
)

# ---------------------------------------------------------------------------
# 10. quadrant_scatter (wave8)
# ---------------------------------------------------------------------------
scatter_html = safe_call(
    "quadrant_scatter", w8.quadrant_scatter,
    points=[
        {"label": "PVT", "x": 1.3, "y": 15.2, "color": "#2E7D52"},
        {"label": "HAH", "x": 1.8, "y": 11.4, "color": "#4A6FA5"},
        {"label": "VOS", "x": 0.9, "y": 3.1, "color": "#C0392B"},
        {"label": "GMD", "x": 2.4, "y": 18.6, "color": "#B5A642"},
    ],
    x_label="P/B (x)", y_label="ROE (%)",
    quadrants={"tl": "Đắt nhưng yếu", "tr": "Sweet spot", "bl": "Rẻ và yếu", "br": "Rẻ và hiệu quả"},
    title="Định giá và hiệu quả nhóm vận tải biển niêm yết",
)

# ---------------------------------------------------------------------------
# 11. slopegraph (wave8)
# ---------------------------------------------------------------------------
slope_html = safe_call(
    "slopegraph", w8.slopegraph,
    items=[
        {"label": "PVT", "before": 88.0, "after": 92.5, "highlight": True},
        {"label": "HAH", "before": 90.0, "after": 91.0},
        {"label": "VOS", "before": 108.5, "after": 111.9, "highlight": True},
        {"label": "GMD", "before": 85.0, "after": 86.5},
    ],
    label_before="LDR trước đề xuất", label_after="LDR sau đề xuất",
    title="Xếp hạng lại LDR sau khi sửa Thông tư 22",
    unit="%",
)

# ---------------------------------------------------------------------------
# 12. dot_plot_distribution (wave8)
# ---------------------------------------------------------------------------
dotplot_html = safe_call(
    "dot_plot_distribution", w8.dot_plot_distribution,
    items=[
        {"label": "PVT", "value": 19.5},
        {"label": "HAH", "value": 24.1},
        {"label": "GMD", "value": 22.0},
        {"label": "VOS", "value": 31.8, "highlight": True, "annotate": "Vượt trần"},
        {"label": "VTO", "value": 26.4},
        {"label": "VSC", "value": 23.0},
    ],
    threshold=30, threshold_label="Trần SFL đề xuất",
    title="Phân phối tỷ lệ SFL nhóm vận tải biển",
    x_unit="%",
)

# ---------------------------------------------------------------------------
# 13. path_progression (wave9)
# ---------------------------------------------------------------------------
path_html = safe_call(
    "path_progression", w9.path_progression,
    milestones=[
        {"label": "Dự thảo nội bộ NHNN", "caption": "T4/2026", "marker": "completed"},
        {"label": "Lấy ý kiến hiệp hội chủ tàu", "caption": "T6/2026", "marker": "completed"},
        {"label": "Trình Chính phủ", "caption": "T9/2026", "marker": "current", "highlight": True},
        {"label": "Ban hành chính thức", "caption": "Q1/2027", "marker": "future"},
    ],
    title="Lộ trình sửa đổi Thông tư 22 cho nhóm vận tải biển",
)

# ---------------------------------------------------------------------------
# 14. dashboard_grid (wave10)
# ---------------------------------------------------------------------------
dashboard_html = safe_call(
    "dashboard_grid", w10.dashboard_grid,
    cells=[
        {"kpi": "2.780", "label": "CHỈ SỐ CƯỚC BDI", "delta": "+10,7%", "delta_type": "up",
         "spark_data": [2100, 2200, 2350, 2510, 2780], "context": "Tăng 4 phiên liên tiếp."},
        {"kpi": "111,9%", "label": "LDR HỆ THỐNG", "delta": "+3,4 đp", "delta_type": "up",
         "spark_data": [105, 107, 108.5, 110, 111.9], "context": "Vượt trần quy định 85%.", "highlight": True},
        {"kpi": "8,2%", "label": "CHI PHÍ VỐN PVT", "delta": "-0,3 đp", "delta_type": "down",
         "spark_data": [8.5, 8.4, 8.3, 8.25, 8.2], "context": "Giảm nhờ đề xuất nới SFL."},
        {"kpi": "31,8%", "label": "SFL VOS", "delta": "+1,8 đp", "delta_type": "up",
         "spark_data": [28, 29, 30.2, 31.0, 31.8], "context": "Vượt trần đề xuất 30%."},
    ],
    title="Bảng chỉ số nhanh: ngân hàng và vận tải biển",
    cols=2,
)

# ---------------------------------------------------------------------------
# 15. infographic_panel (wave10)
# ---------------------------------------------------------------------------
infographic_html = safe_call(
    "infographic_panel", w10.infographic_panel,
    hero_value="406", hero_unit="nghìn tỷ VND",
    hero_label="DƯ NỢ TÍN DỤNG ĐÓNG TÀU TOÀN HỆ THỐNG",
    hero_caption="Ước tính dư nợ tín dụng dành cho đóng mới và cải tạo đội tàu biển Việt Nam, cuối Q2/2026.",
    facts=[
        {"value": "+18%", "label": "so với Q4/2025", "detail": "Tăng trưởng chủ yếu từ nhóm PVT, HAH."},
        {"value": "3", "label": "mã niêm yết chính", "detail": "PVT, HAH, VOS."},
        {"value": "35%", "label": "trần SFL hiện hành", "detail": "Đề xuất nới lên 43% cho nhóm tàu biển."},
        {"value": "Q1/2027", "label": "mốc ban hành dự kiến", "detail": "Có thể trễ nếu Quốc hội yêu cầu đánh giá lại."},
    ],
    title="Bức tranh tín dụng đóng tàu",
)

# ---------------------------------------------------------------------------
# 16. back_cover_cta -- HTML thu cong theo DUNG class CSS that (.contact-page...)
# ---------------------------------------------------------------------------
back_cover_html = """
<section class="contact-page">
  <div class="contact-eyebrow">THAM KHẢO &amp; LIÊN HỆ</div>
  <h2 class="contact-title">Đọc thêm cùng OPVIA</h2>
  <p class="contact-intro">
    Phân tích này nằm trong chuỗi nghiên cứu chuyên sâu về ngân hàng và vận tải biển
    của OPVIA Academy. Để đào sâu hơn từng góc nhìn, hãy liên hệ trực tiếp với đội ngũ.
  </p>
  <div class="contact-cta">
    <div class="cta-eyebrow">LIÊN HỆ ĐỘI NGŨ OPVIA</div>
    <div class="cta-title">Đọc thêm phân tích chuyên sâu hoặc đặt lịch tư vấn 1-1</div>
    <div class="cta-text">OPVIA Academy phát hành báo cáo định kỳ về ngân hàng, vĩ mô và vận tải biển.</div>
    <div class="cta-grid">
      <div class="cta-item"><div class="cta-label">EMAIL</div><div class="cta-value">contact@opvia.vn</div></div>
      <div class="cta-item"><div class="cta-label">WEBSITE</div><div class="cta-value">opvia.vn/research</div></div>
      <div class="cta-item"><div class="cta-label">ĐẶT LỊCH</div><div class="cta-value">opvia.vn/book</div></div>
    </div>
  </div>
  <div class="contact-section">
    <div class="glossary-eyebrow">NGUỒN</div>
    <p>Số liệu minh hoạ cho mục đích thực nghiệm mổ xẻ kỹ thuật, không phải số liệu thật.</p>
  </div>
  <div class="disclaimer-card">
    <div class="disclaimer-label">MIỄN TRỪ TRÁCH NHIỆM</div>
    <p>Toàn bộ phân tích và số liệu trong tài liệu này chỉ mang tính minh hoạ kỹ thuật,
    không phải khuyến nghị đầu tư.</p>
  </div>
  <div class="contact-signature">OPVIA ACADEMY · MỤC ĐÍCH GIÁO DỤC · © 2026</div>
</section>
"""
components_rendered.append("back_cover_cta (thu cong, class that)")


# ---------------------------------------------------------------------------
# Lap rap HTML hoan chinh
# ---------------------------------------------------------------------------
body_content = f"""
{cover_html}

<section class="toc-page" style="display:none"><!-- bo qua TOC that trong thi nghiem nay --></section>

<div class="content" style="padding: 0 24mm;">
  <div class="section-opener">
    <div class="section-roman">I</div>
    <div class="section-eyebrow">TÍN DỤNG NGÂN HÀNG</div>
    <h2 class="section-title-large">Hệ thống đã sát trần thanh khoản</h2>
    <p class="section-dek">Áp lực LDR buộc NHNN phải chọn giữa nới quy chế hoặc siết tăng trưởng tín dụng.</p>
  </div>

  {data_hero_html}
  {gauge_html}
  {bar_html}
  {heatmap_html}

  <div class="section-opener">
    <div class="section-roman">II</div>
    <div class="section-eyebrow">TÁC ĐỘNG NGÀNH VẬN TẢI BIỂN</div>
    <h2 class="section-title-large">Ai được vay rẻ, ai bị siết lại</h2>
    <p class="section-dek">Ba mã niêm yết chính đối diện tác động trái chiều tuỳ hồ sơ tài chính.</p>
  </div>

  {waterfall_html}
  {risk_radar_html}
  {line_html}
  {sankey_html}
  {scatter_html}
  {slope_html}
  {dotplot_html}

  <div class="section-opener">
    <div class="section-roman">III</div>
    <div class="section-eyebrow">LỘ TRÌNH VÀ TÓM TẮT</div>
    <h2 class="section-title-large">Cửa sổ chính sách và các mốc cần theo dõi</h2>
  </div>

  {path_html}
  {dashboard_html}
  {infographic_html}

  <div class="disclaimer-card">
    <div class="disclaimer-label">MIỄN TRỪ TRÁCH NHIỆM (nội dung giữa bài)</div>
    <p>Đây là tài liệu thực nghiệm kỹ thuật, số liệu minh hoạ.</p>
  </div>
</div>

{back_cover_html}
"""

# CSS: build_full_css (core + polish) + tat ca 4 module viz styles
css = polish_render.build_full_css(date_str="06/08/2026", short_title="Thông tư 22 và vận tải biển")
css += viz.viz_styles()
css += w8.wave8_styles()
css += w9.wave9_styles()
css += w10.wave10_styles()

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Sửa Thông tư 22 và vận tải biển - OPVIA thực nghiệm</title>
<style>
{css}
</style>
</head>
<body>
{body_content}
</body>
</html>
"""

out_html = os.path.join(LAB, "output_report.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(full_html)

print()
print("================ TOM TAT ================")
print(f"So component thu goi: {len(components_rendered)}")
print(f"Thanh cong (safe_call): {len(components_rendered) - 2}")  # tru 2 cai thu cong
print(f"Loi: {len(errors)}")
for name, err in errors:
    print(f"  - {name}: {err}")
print(f"HTML da ghi: {out_html} ({len(full_html)} ky tu)")

# Validate qua validators.py that
val_errors = validators.validate_html(full_html)
print(f"\\nvalidators.validate_html() -> {len(val_errors)} issue")
for e in val_errors[:30]:
    print(f"  - {e}")

# QC check that cua polish skill
qc_issues = polish_render.qc_check(full_html)
print(f"\\nqc_check() (opvia-deepanalysis-polish) -> {len(qc_issues)} issue")
for i in qc_issues:
    print(f"  {i}")
