---
title: "Commodity → VN CPI + PPI Passthrough — Tác động Ngành, Elasticity, và Kênh Truyền Dẫn"
module_type: "domain"
file_name: "domain-commodities-vn-impact.md"
purpose: "Quantify và codify kênh truyền dẫn từ biến động giá commodity toàn cầu vào nền kinh tế Việt Nam: CPI (tiêu dùng), PPI (sản xuất), và margin theo ngành. Tập trung vào các commodity có impact lớn nhất: oil, steel, coffee, rice, gas, và phân bón."
primary_triggers:
  - "commodity ảnh hưởng CPI VN"
  - "giá dầu tăng ảnh hưởng gì"
  - "PPI passthrough"
  - "transport margin squeeze"
  - "steel price construction delay"
  - "coffee tax MOF"
  - "lạm phát nhập khẩu"
  - "giá xăng ảnh hưởng CPI"
  - "commodity shock Vietnam"
when_to_use:
  - "Khi phân tích tác động của biến động giá oil/steel/gas lên lạm phát VN hoặc margin doanh nghiệp."
  - "Khi đánh giá fiscal windfall từ xuất khẩu nông sản (thuế xuất khẩu, thuế thu nhập doanh nghiệp)."
  - "Khi làm bounds analysis: 'Oil tăng 20% thì CPI VN tăng bao nhiêu?'"
  - "Khi phân tích cross-asset linkage giữa commodity và VN equity / rates / FX."
when_not_to_use:
  - "Không dùng để dự báo CPI/PPI tuyệt đối — chỉ cung cấp elasticity estimates và kênh truyền dẫn."
  - "Không dùng khi dữ liệu commodity không rõ ràng hoặc trong giai đoạn structural break (cần kiểm tra vn-structural-shifts-tracker)."
  - "Không thay thế phân tích chính sách tiền tệ NHNN — commodity là supply shock, NHNN policy là demand management."
related_modules:
  - "domain-commodities-soft.md"
  - "domain-commodities-futures-curve.md"
  - "macro-vn-transmission-channels.md"
  - "macro-vn-monetary-policy-nhnn.md"
  - "reference-vn-data-sources.md"
  - "domain-cross-asset-linkage-matrix-vn.md"
authoritative_citations:
  - "GSO — CPI (11 nhóm hàng), PPI (3 ngành công nghiệp chính)."
  - "MOF — Thu ngân sách theo loại thuế, thuế xuất khẩu nông sản."
  - "Bộ Công Thương — Giá xăng dầu điều hành (kỳ điều chỉnh 10 ngày)."
  - "IMF Working Papers — pass-through coefficients for emerging markets."
  - "World Bank Commodity Markets Outlook."
  - "VEPR — Báo cáo thường niên kinh tế vĩ mô (elasticity estimates VN)."
output_owner: "workflow-cross-asset-linkage.md khi user hỏi 'ảnh hưởng X đến Y'; workflow-deep-dive.md khi phân tích sector-specific margin; workflow-daily-brief.md khi có commodity shock overnight."
---

# Commodity → VN CPI + PPI Passthrough

**Mục đích:** Codify kênh truyền dẫn từ commodity prices vào nền kinh tế VN với độ chi tiết operational: elasticity ước tính, lag structure, sector-specific impact, và fiscal implications. Dùng để trả lờii "Oil tăng 20% thì gì xảy ra?" một cách có cấu trúc.

**Trạng thái:** [STRUCTURAL — Elasticity estimates dựa trên data 2018–2024, cần review khi có structural break.]

---

## 1. TỔNG QUAN: PASSTROUGH MECHANISM

### 1.1. CPI Basket VN — Commodity exposure

| Nhóm hàng CPI | Trọng số (~%) | Commodity-linked? | Kênh truyền dẫn |
|:---|:---:|:---:|:---|
| **Lương thực, thực phẩm** | ~33–36 | Cao | Gạo, thịt lợn (feed cost), dầu ăn (cọ/dầu đậu nành), đường |
| **Nhà ở và vật liệu xây dựng** | ~10–12 | Trung bình | Thép, xi măng, gạch, sand (giá vận chuyển) |
| **Giao thông** | ~9–10 | Rất cao | Xăng, dầu diesel, dầu nhờn — điều hành giá 10 ngày/lần |
| **Điện, nước, gas** | ~4–5 | Cao | LNG, than đá, gas LPG (giá thế giới) |
| **May mặc, giày dép** | ~3–4 | Trung bình | Cotton, polyester (dầu mỏ derivative) |
| **Y tế, giáo dục, dịch vụ khác** | ~30–35 | Thấp | Ít nhạy cảm trực tiếp với commodity |

> **DIỄN GIẢI:** ~55–60% basket CPI VN có nhạy cảm trực tiếp hoặc gián tiếp với commodity prices. Đây là lý do VN có pass-through tương đối cao so với developed markets (nơi dịch vụ chiếm >70% basket).

### 1.2. Lag structure tổng quát

| Giai đoạn | Lag | Cơ chế |
|:---|:---:|:---|
| **Immediate (0–2 tuần)** | 0–0.5 tháng | Giá xăng dầu điều hành (10 ngày), gas LPG |
| **Short-term (1–3 tháng)** | 1–3 tháng | Giá thép, xi măng, phân bón, thức ăn chăn nuôi |
| **Medium-term (3–6 tháng)** | 3–6 tháng | Giá lương thực (gạo), thịt lợn (chu kỳ 4–6 tháng), dầu ăn |
| **Long-term (6–12 tháng)** | 6–12 tháng | Giá nhà ở (vật liệu xây dựng + đất), dịch vụ vận chuyển (contract adjustment) |

---

## 2. OIL — KÊNH TRUYỀN DẪN MẠNH NHẤT

### 2.1. Oil → CPI passthrough

| Kênh | Elasticity (ước tính) | Lag | Mô tả |
|:---|:---:|:---:|:---|
| **Xăng dầu trực tiếp** | 0.25–0.35 | 0–0.5 tháng | Mỗi 10% giá Brent tăng → CPI giao thông tăng 2.5–3.5%. Quỹ bình ổn giá xăng dầu làm trơn nhưng không loại bỏ hoàn toàn |
| **Vận chuyển hàng hóa** | 0.08–0.12 | 1–3 tháng | Freight cost, logistics — tác động lên giá hàng hóa nói chung |
| **Nhựa, hóa chất, phân bón** | 0.05–0.08 | 1–3 tháng | Dầu mỏ là input cho petrochemicals, phân bón ure |
| **Điện (nhiệt điện)** | 0.03–0.05 | 3–6 tháng | Than đá và LNG — oil-gas price linkage |

> **SỰ KIỆN:** Giá Brent tăng từ $78 (tháng 6/2024) lên $95 (tháng 9/2024, +22%). CPI giao thông VN tăng 8.5% trong cùng giai đoạn, góp phần đẩy CPI tổng thể từ 3.5% lên 4.3%. Quỹ bình ổn giá xăng dầu đã sử dụng ~3,000–4,000 tỷ VND để trơn giá, nhưng không ngăn được passthrough hoàn toàn.

### 2.2. Oil → Sector-specific: Transport margin squeeze

| Ngành | Impact | Cơ chế | Mitigation |
|:---|:---:|:---|:---|
| **Vận tải đường bộ (VNS, GMD, HAH)** | âm | Diesel chiếm 30–40% cost structure; không pass-through 100% cho khách hàng do cạnh tranh | Fuel surcharge (phụ phí xăng dầu) nhưng adjustment lag 1–2 tháng |
| **Hàng không (VJC)** | âm | Jet fuel ~25–35% operating cost; hedging jet fuel phức tạp và đắt | Fuel hedge (nếu có), phụ phí nhiên liệu |
| **Vận tải biển (GMD, HAH, PVT)** | âm/trung tính | Bunker fuel tăng → cost tăng, nhưng freight rates có thể tăng theo nếu supply tight | Fuel adjustment clause trong charter contract |
| **E-commerce / giao hàng (J&T, GHN, Lazada)** | âm | Last-mile delivery phụ thuộc xăng; không thể tăng phí ngay lập tức | Tăng phí giao hàng, optimize route |

> **DIỄN GIẢI:** Ngành vận tải VN có đặc thù: (a) cạnh tranh gay gắt, (b) nhiều doanh nghiệp nhỏ không có pricing power, (c) fuel surcharge adjustment chậm. Kết quả: oil tăng nhanh = margin squeeze ngắn hạn (2–4 tháng) trước khi cost được pass-through.

---

## 3. STEEL — KÊNH XÂY DỰNG VÀ TÀI SẢN CỐ ĐỊNH

### 3.1. Steel → PPI và CPI nhà ở

| Chỉ tiêu | Elasticity (ước tính) | Lag | Ghi chú |
|:---|:---:|:---:|:---|
| **PPI ngành sản xuất kim loại** | 0.6–0.8 | 1–2 tháng | Thép là input chiếm ~60% giá thành sản phẩm kim loại |
| **PPI ngành xây dựng** | 0.4–0.5 | 2–3 tháng | Thép + xi măng chiếm ~30–40% giá thành công trình |
| **CPI nhà ở và vật liệu xây dựng** | 0.15–0.25 | 6–12 tháng | Giá nhà ở adjustment chậm do contract và tâm lý |

### 3.2. Steel → Construction delay dynamics

| Scenario | Giá HRC/CRS tăng | Phản ứng ngành xây dựng | Phản ứng BĐS |
|:---|:---|:---|:---|
| **Tăng <10%** | Ngắn hạn | Contractor chịu margin squeeze nếu đã ký fixed-price contract | Ít tác động |
| **Tăng 10–25%** | Trung hạn | Contractor đàm phán lại giá, hoặc delay dự án để chờ giá hạ | CĐT review feasibility, một số dự án nhỏ bị hoãn |
| **Tăng >25%** | Dài hạn | Delay phổ biến, chuyển sang vật liệu thay thế (bê tông đúc sẵn, thép nhập khẩu giá rẻ hơn) | CĐT tăng giá bán (presale), hoặc freeze dự án |

> **SỰ KIỆN:** Giá thép HRC nội địa tăng ~35% trong 2021 (sau COVID supply shock + China output cuts). Nhiều dự án BĐS tại TP.HCM và Hà Nội bị delay 3–6 tháng do contractor không thể chịu margin và CĐT không muốn tăng giá trong bối cảnh thanh khoản yếu. Đây là ví dụ điển hình của "steel → construction delay → BĐS supply slowdown → giá nhà tăng chậm hơn dự kiến".

### 3.3. Steel → Equity impact (VN)

| Cổ phiếu | Direction | Cơ chế | Timing |
|:---|:---:|:---|:---|
| **HPG** | + | Nhà sản xuất thép — giá tăng > cost tăng (quặng sắt, than) → margin mở rộng | 1–2 quý |
| **HSG, NKG** | + | Tương tự HPG nhưng nhỏ hơn, nhạy cảm hơn với giá HRC | 1–2 quý |
| **DXG, NVL, KDH** | −/trung tính | Cost input tăng → margin giảm hoặc delay dự án | 2–4 quý |
| **Coteccons (CTD)** | − | EPC contractor — fixed-price contract bị margin squeeze nếu steel tăng sau khi ký hợp đồng | Ngay lập tức đến 1 quý |

---

## 4. COFFEE — FISCAL WINDFALL VÀ THU NHẬP NÔNG THÔN

### 4.1. Coffee → MOF tax revenue

| Kênh thu | Elasticity với giá cà phê | Lag | Cơ chế |
|:---|:---:|:---:|:---|
| **Thuế xuất khẩu** | 0.8–1.0 | 1–3 tháng | Tính theo giá FOB tại thờii điểm xuất khẩu; giá tăng 20% = thuế xuất khẩu tăng ~20% |
| **Thuế TNDN doanh nghiệp rang xay/xuất khẩu** | 0.6–0.8 | 3–6 tháng (quý sau) | Profit tăng theo giá (nếu đã mua nguyên liệu trước ở giá thấp) |
| **Thuế TNCN nông dân** | 0.3–0.5 | 6–12 tháng (năm sau) | Thu nhập nông dân tăng, nhưng nhiều hộ nhỏ dưới ngưỡng chịu thuế |
| **Thuế GTGT chuỗi** | 0.5–0.7 | 1–6 tháng | Doanh thu chuỗi cung ứng tăng theo giá |

> **DIỄN GIẢI:** Giá cà phê robusta London tăng từ $1,800/tấn (2023) lên $3,200–3,500/tấn (2024–2025, +75–95%). Ước tính thu ngân sách từ kênh cà phê (thuế XK + TNDN + GTGT) tăng 1.5–2.5 nghìn tỷ VND/năm. Đây là "fiscal windfall" không bền vững — phụ thuộc hoàn toàn vào giá thế giới.

### 4.2. Coffee → Thu nhập nông thôn và tiêu dùng

| Kênh | Impact | Lag | Ghi chú |
|:---|:---:|:---:|:---|
| **Thu nhập hộ nông dân cà phê** | +++ | Ngay (bán tại vườn) | ~600,000 hộ nông dân Tây Nguyên, thu nhập tăng 30–50% trong 2024 |
| **Tiêu dùng địa phương (Đắk Lắk, Lâm Đồng)** | + | 1–3 tháng | Hiệu ứng thu nhập → bán lẻ, xe máy, xây nhà |
| **Giá đất vùng cà phê** | + | 6–12 tháng | Đất trồng cà phê tăng giá theo thu nhập kỳ vọng |
| **CPI food Đắk Lắk, Lâm Đồng** | + | 1–3 tháng | Tiêu dùng địa phương tăng đẩy giá dịch vụ và lương thực nội địa |

> **GIẢ THUYẾT:** Nếu giá cà phê duy trì >$3,000/tấn trong 2 năm liên tiếp, có thể xuất hiện: (a) diện tích trồng cà phê mở rộng bất hợp lý → oversupply 3–4 năm sau, (b) chuyển đổi từ arabica sang robusta do spread thu hẹp, (c) tăng đầu tư vào chế biến sâu nhưng rủi ro giá giảm trước khi hoàn vốn.

---

## 5. ELASTICITY ESTIMATES — MA TRẬN TỔNG HỢP

### 5.1. Commodity → CPI/PPI VN (Elasticity ước tính)

> **SỰ KIỆN:** Các con số dưới đây là estimates tổng hợp từ VEPR, WB, IMF working papers, và regression đơn giản trên data GSO 2018–2024. Confidence: Medium. Khi sử dụng, phải nêu rõ "estimate, không phải calibrated model."

| Commodity | Biến động giá | CPI tổng thể | CPI nhóm trực tiếp | PPI sản xuất | Lag chính | Confidence |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Brent crude (+10%)** | +10% | +0.35–0.50% | Giao thông: +3.0–3.5% | +0.6–0.9% | 0–1 tháng | High |
| **Steel HRC (+10%)** | +10% | +0.08–0.12% | Nhà ở: +0.5–0.8% | +0.8–1.2% | 2–3 tháng | Medium |
| **Gas LPG (+10%)** | +10% | +0.06–0.08% | Điện/nước/gas: +1.5–2.0% | +0.2–0.3% | 0–0.5 tháng | High |
| **Rice export price (+10%)** | +10% | +0.15–0.25% | Lương thực: +0.8–1.2% | +0.1–0.2% | 3–6 tháng | Medium |
| **Coffee London (+10%)** | +10% | +0.02–0.04% | Giải khát: +0.3–0.5% | +0.05–0.1% | 1–3 tháng | Low-Medium |
| **Ure/phân bón (+10%)** | +10% | +0.05–0.08% | Lương thực (gián tiếp): +0.3–0.5% | +0.4–0.6% | 1–3 tháng | Medium |
| **LNG (+10%)** | +10% | +0.04–0.06% | Điện: +0.5–0.8% | +0.3–0.5% | 3–6 tháng | Medium |

### 5.2. Bounds analysis — Scenario

| Scenario | Oil +30% | Steel +25% | Rice +20% | Combined impact CPI |
|:---|:---:|:---:|:---:|:---:|
| **Direct passthrough** | +1.1–1.5% | +0.2–0.3% | +0.3–0.5% | +1.6–2.3% |
| **With 2nd round effects** (wage, expectations) | +1.5–2.0% | +0.3–0.5% | +0.4–0.7% | +2.2–3.2% |
| **With policy response** (Quỹ bình ổn xăng, NHNN tighten) | +0.8–1.2% | +0.2–0.3% | +0.3–0.5% | +1.3–2.0% |

> **DIỄN GIẢI:** Combined commodity shock có thể đẩy CPI VN tăng 2–3 điểm % trong 6–12 tháng nếu không có can thiệp chính sách. Đây là lý do NHNN thường thắt chặt tiền tệ hoặc điều chỉnh tỷ giá khi oil tăng mạnh — không chỉ vì lạm phát trực tiếp mà vì expectations bị đẩy lên.

---

## 6. SECTOR-SPECIFIC IMPACT MATRIX

| Sector | Commodity risk chính | Direction | Lag | Ví dụ cổ phiếu |
|:---|:---|:---:|:---:|:---|
| **Vận tải đường bộ** | Diesel | âm | 0–2 tháng | VNS, ACL, VTO |
| **Vận tải biển** | Bunker fuel | âm | 0–1 tháng | GMD, HAH, PVT |
| **Hàng không** | Jet fuel | âm | 0–1 tháng | VJC |
| **Sản xuất thép** | Quặng sắt, than | dương (producer) | 1–2 quý | HPG, HSG, NKG |
| **Xây dựng / EPC** | Thép, xi măng, diesel | âm | 0–3 tháng | CTD, HBC, FEC |
| **BĐS** | Thép, xi măng | âm (cost) / dương (giá bán nếu pass) | 2–4 quý | NVL, DXG, KDH |
| **Chăn nuôi** | Ngô, đậu tương, thức ăn | âm | 1–2 tháng | HAG, DBC, MAS |
| **Xuất khẩu cà phê** | Robusta price | dương | 1–3 tháng | HAG (indirect) |
| **Xuất khẩu gạo** | Gạo 5% broken FOB | dương | 1–3 tháng | VFM, TNG, LTG |
| **Bán lẻ nội địa** | Xăng, logistics | âm | 1–2 tháng | MWG, FRT, PNJ |

---

## 7. CROSS-REFS VÀ TRIGGER WORKFLOW

| Khi ngưới dùng hỏi... | Load module... | Output contract |
|:---|:---|:---|
| "Oil tăng 20% thì CPI VN tăng bao nhiêu?" | Module này + `macro-vn-transmission-channels.md` | Linkage Analysis |
| "Margin HPG khi giá HRC tăng?" | Module này + `domain-equity-vn-industry-guides.md` | Deep-dive Memo |
| "Giá cà phê tăng ảnh hưởng thu ngân sách?" | Module này + `domain-commodities-soft.md` | Linkage Analysis |
| "Commodity shock overnight — brief đầu ngày?" | Module này + `workflow-daily-brief.md` | Daily Brief |
| "Passthrough giá dầu vào lãi suất NHNN?" | Module này + `macro-vn-monetary-policy-nhnn.md` | Cross-asset Linkage |

---

*Module version: 0.1.0 | Shelf life: 6 tháng (elasticity estimates cần review khi có structural break).*
*Cross-check với: GSO CPI/PPI (hàng tháng), MOF thu ngân sách (hàng tháng), Bộ Công Thương giá xăng dầu (10 ngày), VEPR macro report (hàng quý).*
