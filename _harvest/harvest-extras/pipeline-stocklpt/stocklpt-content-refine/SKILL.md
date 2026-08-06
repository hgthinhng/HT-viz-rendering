---
name: stocklpt-content-refine
description: "Editor skill chải chuốt ngôn ngữ và làm sạch văn phong cho bài phân tích/báo cáo StockLPT trước khi polish thành PDF. Xử lý duy nhất NGỮ NGHĨA (Vietlish, từ vay mượn, AI-style filler, câu dài lan man, hedge overuse), không động đến CSS/HTML/visual. Hỗ trợ 3 mức (light/standard/heavy) tùy density Vietlish. LUÔN dùng skill này khi user paste text Vietlish hoặc AI-generated và muốn cleaner version, hoặc khi user nói 'refine', 'chải chuốt', 'làm sạch văn phong', 'rewrite cho ra tiếng Việt thuần', 'tinh chỉnh từ vựng', '/stocklpt-refine', '/stocklpt-refine'. Pipeline: text gốc → [stocklpt-content-refine] → text sạch → [stocklpt-dailyreport-polish hoặc stocklpt-deepanalysis-polish] → PDF. KHÔNG dùng cho text đã sạch của analyst nội bộ, text gốc tiếng Anh, hoặc khi user chỉ muốn polish visual ngay."
---

# StockLPT Content Refine Skill

Skill này chải chuốt **NGỮ NGHĨA** của bài phân tích/báo cáo StockLPT trước khi đem polish thành PDF. Chỉ liên quan đến từ vựng, văn phong, cách diễn đạt - KHÔNG liên quan đến CSS/HTML/render.

**Pipeline:** text gốc → refine (nội dung) → polish (visual) → PDF

> **Độc lập trình bày:** skill này chỉ chạm NGỮ NGHĨA, độc lập với palette và wordmark StockLPT. Brand (palette/wordmark) được quyết ở bước polish/render, không liên quan tới refine. Không cần biết brand nào khi chải chuốt text.

---

## Khi nào dùng skill này?

**Dùng khi:**
- User paste text bài analysis/daily report do Claude hoặc AI khác tạo ra
- Text có nhiều từ tiếng Anh không cần thiết (Vietlish): "technical fix", "trade-off", "headroom"...
- Văn phong AI-style: lạm dụng "thực sự", "vô cùng"; câu dài lê thê; redundancy
- User muốn output sẵn sàng publish

**KHÔNG dùng khi:**
- Content do người StockLPT (analyst) viết - thường đã sạch
- User chỉ muốn polish visual ngay
- Text gốc bằng tiếng Anh

---

## 3 Mức refine (Wave 1)

User có thể chọn mức cụ thể. Mặc định: **standard** (level 2).

### Level 1 - Light (giữ 95% nguyên bản)

**Áp dụng:** content đã ổn, chỉ cần dọn vài từ vay mượn rõ ràng.

**Quy tắc:**
- ✅ Paraphrase Vietlish hiển nhiên ("technical fix" → "sửa kỹ thuật")
- ✅ Sửa số: dấu phẩy decimal, dấu chấm thousands
- ❌ KHÔNG động đến cấu trúc câu
- ❌ KHÔNG cắt filler ("thực sự", "vô cùng")
- ❌ KHÔNG restructure đoạn

**Trigger:** `/stocklpt-refine level=1` hoặc user nói "nhẹ thôi"

### Level 2 - Standard (mặc định)

**Áp dụng:** AI-generated content thông thường.

**Quy tắc:**
- ✅ Tất cả của Level 1
- ✅ Cắt filler intensifiers ("thực sự là", "vô cùng" overuse)
- ✅ Cắt câu >40 từ thành 2 câu ngắn
- ✅ Sửa mở đầu yếu ("trong bối cảnh hiện nay" → cắt)
- ✅ Sửa câu kết yếu ("tóm lại có thể nói rằng" → cắt + rewrite)
- ✅ Giảm hedge overuse ("có thể là, có lẽ" cluster → giảm)
- ❌ KHÔNG restructure đoạn lớn
- ❌ KHÔNG đổi giọng tổng thể

**Trigger:** `/stocklpt-refine` hoặc default

### Level 3 - Heavy (rewrite mạnh)

**Áp dụng:** content quá AI hoặc quá hành chính.

**Quy tắc:**
- ✅ Tất cả của Level 2
- ✅ Restructure đoạn dài lan man
- ✅ Đổi giọng từ formal-bureaucratic sang editorial-direct
- ✅ Cắt redundant explanations ("X (tức là Y)" khi Y đã rõ)
- ✅ Áp dụng StockLPT voice rules
- ✅ Vary bullet phrasing
- ✅ Vary transitions

**Trigger:** `/stocklpt-refine level=3` hoặc user nói "rewrite mạnh", "StockLPT voice"

### Decision tree khi user không specify

```
Vietlish density 0-2 từ → Level 1
Vietlish density 3-7 từ → Level 2 (default)
Vietlish density 8+ từ HOẶC nhiều AI tells → Level 3
```

---

## Bước 1: Vietlish Dictionary (200+ entries)

### A. Macro economics

| Vietlish | Tiếng Việt |
|---|---|
| monetary easing | nới lỏng tiền tệ |
| monetary tightening | thắt chặt tiền tệ |
| monetary policy stance | lập trường chính sách tiền tệ |
| fiscal stimulus | kích thích tài khóa |
| fiscal headroom | dư địa tài khóa |
| soft landing | hạ cánh mềm |
| hard landing | hạ cánh cứng |
| supply shock | cú sốc cung |
| demand-pull inflation | lạm phát do cầu kéo |
| cost-push inflation | lạm phát do chi phí đẩy |
| output gap | khoảng cách sản lượng |
| potential GDP | GDP tiềm năng |
| trade deficit | thâm hụt thương mại |
| current account | tài khoản vãng lai |
| capital flow | dòng vốn |

### B. Banking technical

| Vietlish | Tiếng Việt |
|---|---|
| asset quality | chất lượng tài sản |
| loan loss provision | trích lập dự phòng rủi ro |
| write-off | xử lý/xóa nợ |
| restructured loans | nợ tái cơ cấu |
| credit cycle | chu kỳ tín dụng |
| deposit franchise | nền tảng huy động |
| fee income | thu nhập từ phí |
| wholesale funding | vốn liên ngân hàng |
| funding cost | chi phí vốn |
| interest income | thu nhập lãi |
| net interest income | thu nhập lãi thuần |
| operating leverage | đòn bẩy hoạt động |
| cost-to-income ratio | tỷ lệ chi phí/thu nhập (CIR) |
| credit growth | tăng trưởng tín dụng |
| credit penetration | mức độ thâm nhập tín dụng |
| balance sheet | bảng cân đối kế toán |
| balance sheet expansion | mở rộng bảng cân đối |
| capital ratio | tỷ lệ an toàn vốn |
| capital adequacy | đủ vốn |
| credit risk | rủi ro tín dụng |
| liquidity risk | rủi ro thanh khoản |
| concentration risk | rủi ro tập trung |
| risk-weighted assets | tài sản có rủi ro (giữ RWA) |
| tier 1 capital | vốn cấp 1 |
| tier 2 capital | vốn cấp 2 |
| credit exposure | dư nợ |
| deposit beta | giữ "deposit beta" (technical) |
| loan beta | giữ "loan beta" (technical) |
| cost of funds | chi phí vốn |
| net interest margin | giữ NIM (technical) |

### C. Market microstructure

| Vietlish | Tiếng Việt |
|---|---|
| order flow | dòng lệnh |
| market depth | độ sâu thị trường |
| price discovery | khám phá giá |
| flash crash | sụp tức thời |
| cooling-off period | giai đoạn hạ nhiệt |
| circuit breaker | ngắt mạch giao dịch |
| bid-ask spread | chênh lệch giá mua-bán |
| market impact | tác động thị trường |
| dark pool | giữ |
| high-frequency trading | giao dịch tần số cao (HFT) |

### D. Behavioral / sentiment

| Vietlish | Tiếng Việt |
|---|---|
| risk-on | ưa rủi ro |
| risk-off | ngại rủi ro |
| fear & greed | giữ |
| FOMO | giữ |
| capitulation | đầu hàng |
| panic selling | bán tháo hoảng loạn |
| dead cat bounce | phục hồi giả |
| buy the dip | mua đáy |
| overbought | quá mua |
| oversold | quá bán |

### E. Regulatory

| Vietlish | Tiếng Việt |
|---|---|
| macroprudential | an toàn vĩ mô |
| stress test | kiểm tra sức chịu đựng |
| capital adequacy | đủ vốn |
| leverage ratio | tỷ lệ đòn bẩy |
| SIFI | giữ |
| too-big-to-fail | quá lớn để sụp đổ |
| moral hazard | rủi ro đạo đức |
| systemic risk | rủi ro hệ thống |
| compliance | tuân thủ |
| regulatory framework | khung pháp lý |
| regulatory capital | vốn pháp định |
| Basel III | giữ |
| IFRS | giữ |
| forbearance | khoan nhượng |

### F. Corporate finance

| Vietlish | Tiếng Việt |
|---|---|
| M&A | giữ |
| due diligence | thẩm định |
| earn-out | giữ |
| synergy | hiệp lực |
| dilution | pha loãng |
| accretive | tăng EPS |
| covenant | cam kết |
| burn rate | giữ |
| runway | đường băng |
| term sheet | giữ |
| valuation | định giá |
| EV/EBITDA | giữ |
| free cash flow | dòng tiền tự do |
| working capital | vốn lưu động |
| capex | đầu tư cơ bản |

### G. AI-pattern Vietlish (rất phổ biến)

| AI viết | Tiếng Việt thuần |
|---|---|
| technical fix | sửa kỹ thuật |
| trade-off | đánh đổi |
| headroom | dư địa |
| compression | nén / thắt chặt |
| outlook | triển vọng |
| momentum | đà |
| consolidation | tích lũy |
| breakout | bứt phá |
| pioneer | tiên phong |
| peer | đồng nghiệp/cùng nhóm |
| delay | trì hoãn |
| stakeholder | bên liên quan |
| exposure | mức độ tiếp xúc |
| mechanics | cơ chế |
| FX | tỷ giá (context VND/USD) |
| hedge | phòng vệ |
| hedging | phòng vệ rủi ro |
| arbitrage | giữ |
| insight | hiểu biết |
| narrative | câu chuyện |
| backdrop | bối cảnh |
| upside | mặt tích cực |
| downside | mặt tiêu cực |
| guidance | định hướng |
| visibility | tầm nhìn |
| catalyst | chất xúc tác |
| trigger | kích hoạt |
| pivot | xoay trục |
| sentiment | tâm lý |
| floor | sàn |
| ceiling | trần |
| barrier | rào cản |
| ramp-up | tăng cường |
| roll-out | triển khai |

### H. AI verb patterns (cắt nếu redundant)

| AI viết | Tiếng Việt |
|---|---|
| thực hiện việc + V | (cắt, dùng động từ trực tiếp) |
| tiến hành + V | (cắt nếu redundant) |
| đem lại | mang lại / cắt |
| thực sự là | (cắt) |
| có thể nói rằng | (cắt) |
| nhìn chung | (giữ tối đa 1 lần/đoạn) |
| đặc biệt là | (vary, không lặp) |
| có sự gia tăng | tăng |
| tăng tích cực | tăng |
| ghi nhận sự + N | (cắt "sự") |
| tạo ra ảnh hưởng | tác động |
| dẫn tới | dẫn đến |
| từ đó | (thay "qua đó" hoặc cắt) |
| như vậy | (giữ tối đa 1 lần/đoạn) |
| tuy nhiên | (mix với "Nhưng" / "Trong khi đó") |

### I. Vietnam-specific patterns

| AI viết | Việt nói |
|---|---|
| chú ý đến việc | chú ý |
| xem xét lại | xem lại |
| đánh giá cao | (cắt nếu chỉ là filler) |
| được biết đến với | nổi tiếng với |
| trong những năm gần đây | gần đây / vài năm qua |
| trong tương lai gần | sắp tới |
| với mục đích | để |
| nhằm mục đích | để |
| đối với việc | với |
| trên cơ sở | dựa trên / theo |
| trong khuôn khổ | trong / theo |
| có vai trò quan trọng | quan trọng |
| đóng vai trò | (thường cắt được) |
| theo đó | (cắt, dùng "do đó" / "vì vậy") |
| do đó cần | nên / cần |

### J. Compound English-Vietnamese mix (TỆ NHẤT)

| AI mix | Tiếng Việt |
|---|---|
| force chúng ta | buộc chúng ta |
| build perspective | xây dựng góc nhìn |
| romantic hóa | lãng mạn hóa |
| optimize hóa | tối ưu hóa |
| confront vấn đề | đối mặt vấn đề |
| navigate qua | điều hướng qua |
| leverage để | dùng / tận dụng để |
| address vấn đề | giải quyết vấn đề |
| highlight rằng | nhấn mạnh rằng |
| validate giả thuyết | xác nhận giả thuyết |

### K. Smart context rules (15 từ context-dependent)

Cùng từ tiếng Anh, dịch khác tùy context:

| Từ | Context A | Context B |
|---|---|---|
| spread | "bid-ask spread" → "chênh lệch giá" | "credit spread" → giữ |
| leverage | "leverage ratio" → "tỷ lệ đòn bẩy" | "use leverage" → "dùng đòn bẩy" |
| exposure | "FX exposure" → "rủi ro tỷ giá" | "loan exposure" → "dư nợ" |
| position | "long position" → giữ | "fiscal position" → "tình hình tài khóa" |
| flow | "money flow" → "dòng tiền" | "order flow" → "dòng lệnh" |
| premium | "risk premium" → giữ | "premium product" → "cao cấp" |
| discount | "discount rate" → "tỷ lệ chiết khấu" | "discount to NAV" → giữ |
| margin | "NIM" → giữ | "operating margin" → "biên lợi nhuận" |
| capital | "tier 1 capital" → "vốn cấp 1" | "human capital" → "nguồn nhân lực" |
| stock | "stock price" → "giá cổ phiếu" | "stock-flow" → "tồn-lưu" |
| bond | "government bond" → "TPCP" | (giữ tên cụ thể) |
| yield | "bond yield" → "lợi suất" | "yield curve" → "đường cong lợi suất" |
| rate | "interest rate" → "lãi suất" | "exchange rate" → "tỷ giá" |
| liquidity | "market liquidity" → "thanh khoản thị trường" | "liquidity buffer" → "đệm thanh khoản" |
| benchmark | "benchmark rate" → "lãi suất tham chiếu" | "vs peers" → "so với nhóm cùng" |

---

## Bước 2: Whitelist - thuật ngữ KHÔNG paraphrase

Đây là technical terms đã thiết lập trong giới chuyên môn VN. Skill **KHÔNG** động đến.

**Banking & finance:**
LDR, NSFR, ASF, RSF, CASA, NIM, ROE, ROA, ROIC, NPL, CIR, P/E, P/B, EV, EBITDA, EPS, M&A, IPO, REIT, ETF, NAV, AUM

**Regulatory VN:**
TT22, TT26, TT41, TT39, TGKB, TT2, M3, Big4, Tier-1, Tier-2, Tier-3, JSB, SOCB, Basel I/II/III, IFRS, IAS, SBV, NHNN, BTC, MBKT, UBCKNN, HOSE, HNX, UPCoM

**Markets:**
TPCP, TPDN, GTGD, FX, USD/VND, EUR/VND, JPY/VND, DXY, Brent, WTI, VND, USD

**Securities:**
TCBS, VPBankS, SSI, HSC, VNDirect, VPS, KIS, Mirae

**Macro indicators:**
GDP, CPI, PPI, PMI, M2, FDI, FII, BOP

**Trading:**
HFT, dark pool, market making, arbitrage, hedge, long, short, calls, puts, futures, swap, repo, reverse repo

---

## Bước 3: AI-style detector + remover (30+ patterns)

### A. Mở đầu trống rỗng (cắt)

- ❌ "Trong bối cảnh hiện nay,..."
- ❌ "Có thể thấy rằng,..."
- ❌ "Một trong những điều quan trọng cần lưu ý là..."
- ❌ "Để hiểu rõ hơn về vấn đề này,..."
- ❌ "Trước hết, chúng ta cần..."
- ❌ "Cần phải nhận thấy rằng..."
- ❌ "Đầu tiên, phải nói rằng..."

**Fix:** cắt câu mở đầu, đi thẳng vào nội dung.

### B. Câu kết yếu (rewrite)

- ❌ "Tóm lại, có thể nói rằng..."
- ❌ "Như vậy, chúng ta thấy rằng..."
- ❌ "Để kết luận,..."
- ❌ "Có thể khẳng định rằng..."

**Fix:** thay bằng marker phrase StockLPT ("Đây là", "Thực ra", "Đáng chú ý là").

### C. Filler intensifiers (cắt nếu overuse)

- ❌ "thực sự là" (luôn cắt)
- ❌ "vô cùng" (giảm 80%)
- ❌ "hết sức" (giảm 80%)
- ❌ "cực kỳ" (giảm 80%)
- ❌ "rất rất" (luôn cắt)
- ❌ "tất nhiên là"
- ❌ "đương nhiên rằng"

### D. Hedge lạm dụng

- "có thể là, có lẽ" cluster trong 1 đoạn → giảm xuống 1 lần/đoạn
- "dường như" overuse → giảm
- "nhìn chung" >1 lần/đoạn → cắt còn 1
- "trong nhiều trường hợp" overuse

### E. Redundant explanations

- "X (tức là Y)" khi Y đã rõ từ context
- "X, hay nói cách khác, Y" overuse
- "X, được hiểu là Y" (cắt phần định nghĩa nếu redundant)

### F. Bullet structure AI-style

AI hay viết bullet đầy đủ subject-verb-object đều nhau. Editor viết bullet phrasing variable.

**Detect:** Nếu 5+ bullets cùng pattern "[Subject] [Verb] [Object]" liên tiếp → flag.
**Fix:** vary phrasing - một bullet câu hoàn chỉnh, một bullet phrase ngắn, một bullet pair contrast.

### G. Transitions overused

- "Tuy nhiên" cùng đoạn 3+ lần → mix với "Nhưng" / "Trong khi đó" / "Song"
- "Bên cạnh đó" → "Còn" / "Ngoài ra" / cắt
- "Hơn nữa" → "Thêm vào đó" / cắt
- "Đồng thời" overuse → giảm
- "Mặt khác" overuse → mix

### H. Verb patterns AI overuse

- ❌ "thực hiện việc đánh giá" → "đánh giá"
- ❌ "tiến hành phân tích" → "phân tích"
- ❌ "có sự gia tăng đáng kể" → "tăng đáng kể"
- ❌ "ghi nhận sự thay đổi" → "thay đổi"
- ❌ "đem lại nhiều lợi ích" → "có nhiều lợi ích" hoặc cụ thể hóa

---

## Bước 4: StockLPT voice rules (cho Level 3)

### Voice DO

✅ **Có quan điểm rõ:** 
- "VPB là người sống chết tùy phương án nào" (assertion)
- "Sửa Thông tư 22 là technical fix tái phân phối, không phải nới lỏng tiền tệ"

✅ **Không hedge over:**
- "Big4 hưởng lợi" (không "Big4 có thể có khả năng hưởng lợi")
- "TPCP yield sẽ tăng 20-40 bps" (không "có thể có khả năng tăng nhẹ")

✅ **Metaphor để clarify:**
- "Phương án A là cứu sinh, phương án B là cú đánh"
- "VPB đảo cực giữa hai phương án"
- "Nhóm C đang trong cuộc đua lãi suất"

✅ **Câu ngắn rhythm:**
- 8-15 từ với câu key
- Mix câu ngắn (5-8 từ) với câu trung (15-20 từ)
- Avoid câu >35 từ

✅ **Marker phrases StockLPT:**
- "Đây là..." (assertion)
- "Thực ra..." (correction common belief)
- "Đáng chú ý là..." (highlight)
- "Khi đọc tin này hãy hỏi..." (call to action)
- "Không phải X, mà là Y..." (correction)

✅ **Concrete > abstract:**
- "Big4 unlock 80-100K tỷ dư địa cho vay" (cụ thể)
- thay vì "Big4 sẽ có thêm dư địa đáng kể" (vague)

### Voice DON'T

❌ **Hedge bureaucratic:**
- "Có thể nói rằng việc..." → cắt
- "Có khả năng có thể có" → cắt

❌ **Verbose corporate:**
- "Thực hiện việc đánh giá" → "đánh giá"

❌ **Vague:**
- "Đem lại nhiều lợi ích" → cụ thể "Big4 unlock 80-100K tỷ"

❌ **Filler:**
- "Trong bối cảnh phức tạp này..." → cắt

---

## Bước 5: Number formatting consistency

```
DECIMAL: dấu phẩy
- "111,9%" ✓ / "111.9%" ✗

THOUSANDS: dấu chấm
- "1.234.567 tỷ" ✓ / "1234567" ✗

UNITS:
- "tỷ VND" hoặc "tỷ" (preferred)
- "nghìn tỷ" cho >1000 tỷ
- "%" KHÔNG space ("85%" not "85 %")
- Range: "20-40 bps"

PERCENT POINTS:
- "+1pp" hoặc "+1 đp" → unify trong cùng bài
- Default: "đp"

CURRENCY:
- VND: "1,2 tỷ VND" hoặc "1.234 tỷ"
- USD: "$1,2M" hoặc "1,2 triệu USD"
```

---

## Output format

Trả về text refined sạch. Optional diff report nếu user yêu cầu.

---

## Edge cases

- Text gốc tiếng Anh → SKIP, return nguyên
- Text mixed VN-EN intentional (vd: code blocks) → refine cẩn thận, không động code
- Quote/citation EN → giữ nguyên trong dấu ngoặc kép
- Term StockLPT-specific user định nghĩa → tôn trọng

---

## Checklist trước khi output

- [ ] Vietlish density giảm xuống <5 từ/1000 từ
- [ ] Filler intensifiers giảm 80%
- [ ] Mở đầu/kết yếu rewrite hoặc cắt
- [ ] Number format consistent VN style
- [ ] Câu >40 từ split (cho Level 2+)
- [ ] Whitelist terms KHÔNG bị đụng đến
- [ ] (Level 3) Voice StockLPT áp dụng - assertion rõ, ít hedge
- [ ] Bullets variable phrasing
- [ ] Transitions vary
