# AI TELLS TIẾNG VIỆT — bảng tra de-AI tổng quát (v2 general, 2026-07-09)

> Chưng cất từ 7 luồng research (Wikipedia WP:AISIGNS, paper Idiosyncrasies in LLMs ICML-2025, PNAS Reinhart 2025, GPTZero perplexity/burstiness, ViDetect + VietBinoculars cho tiếng Việt, Brands Vietnam thực nghiệm, corpus 245 tic đã quét khỏi 97 notes 2027). Bản full có nguồn: `Premium CFA/Xu Ly Notes L1 new/research_ai_tells_2026-07-09/`.
> **Cách dùng:** sửa theo MẬT ĐỘ, không diệt tuyệt đối — "được/việc/các/tuy nhiên" đều hợp lệ ở liều người thật. Tell là dấu hiệu, không phải tội danh.

## TIER 1 — LEXICAL: cụm phải quét (grep được)

**Mở bài AI (xoá, vào thẳng việc/số):** "Trong bối cảnh … (phát triển không ngừng)", "Trong thế giới/kỷ nguyên số/thời đại số", "Chào mừng bạn đến với", "Hãy cùng (tìm hiểu/khám phá)", "Dưới đây là…".
**Chuyển đoạn máy móc (cắt 60–70%, nối bằng nhân quả/lặp từ khoá):** "Hơn nữa", "Bên cạnh đó", "Thêm vào đó", "Ngoài ra" lặp dày; "Đáng chú ý là".
**Kết thừa (cắt thẳng; nếu chốt thì chốt bằng cái CHƯA nói):** "Tóm lại", "Nhìn chung", "Như vậy ta thấy", "Kết luận là", kết lạc quan mơ hồ.
**Editorializing / thổi phồng:** "đóng vai trò quan trọng/then chốt", "là minh chứng cho", "đánh dấu bước ngoặt", "mở ra kỷ nguyên", "nâng tầm", "tận dụng/khai thác sức mạnh", "đi sâu vào" (delve), "toàn diện", "vượt trội", "đột phá", "hành trình", "bức tranh toàn cảnh".
**Khuôn song song (tối đa 1/bài):** "không chỉ A mà còn B", "không phải A mà là B", "tưởng chừng… nhưng…".
**Hedging rỗng:** "Điều quan trọng cần lưu ý là", "có thể nói rằng", "phần nào", "Điều đáng lưu ý là", "cần lưu ý rằng" lặp.
**Chat-frame lọt vào văn bản:** "dựa trên thông tin bạn cung cấp", "Để tôi phân tích", "Hy vọng bài viết giúp bạn".
**Nhiệt tình rỗng:** "Thật thú vị!", "đầy hấp dẫn", "Câu hỏi rất hay".

## TIER 2 — CẤU TRÚC & NHỊP (đọc mới thấy, nguy hiểm hơn Tier 1)

1. **Low burstiness** — câu 20–30 từ đều tăm tắp (std-dev độ dài câu người 0.65–0.85, AI <0.30). FIX: câu ngắn 4–6 từ đấm sau chuỗi câu dài, đặt đúng chỗ kết luận/twist.
2. **Rule-of-three** — liệt kê 3 items cân xứng mọi nơi. FIX: đổi số item 1/2/4, làm vế lệch độ dài.
3. **Đoạn đều nhau + mở-thân-kết đồng hồ cát.** FIX: cho phép đoạn 1 câu cạnh đoạn 8 câu.
4. **Scaffolding "Thứ nhất/Thứ hai/Thứ ba"** cứng. FIX: chỉ đánh số khi cần đếm thật.
5. **Hedging cân xứng** — mỗi ưu điểm kèm đúng một "Tuy nhiên". FIX: cho trọng số, nói mặt nào nặng hơn và vì sao.
6. **Colon-title "X: Y"** đều cả mục lục. FIX: luân phiên heading dạng claim / câu hỏi thật / cụm trần.
7. **Câu hỏi tu từ nhồi đều.** QUOTA: ~1/section, hỏi thật + trả lời ngay.
8. **Tự hỏi tự trả lời kiểu Claude** ("Vậy điều này nghĩa là gì? Nó có nghĩa là…"). FIX: nói thẳng.

## TIER 3 — VIETLISH CALQUE (model nghĩ tiếng Anh, viết tiếng Việt)

| Calque | Ví dụ AI | Sửa |
|---|---|---|
| Passive "được/bị + V + bởi" | "Danh mục được quản lý bởi X" | "X quản lý danh mục" / "do X quản lý" |
| Chuỗi "của" | "biến động của giá của cổ phiếu" | "biến động giá cổ phiếu" (≤1 "của"/danh ngữ) |
| Danh hoá "việc/sự" | "Việc sử dụng đòn bẩy làm tăng sự biến động" | "Dùng đòn bẩy thì dao động mạnh hơn" |
| "một" mạo từ | "là một công cụ quan trọng" | "là công cụ quan trọng" |
| "những/các" thừa | "các nhà đầu tư… các danh mục" | danh từ generic để trần |
| "Nó" mở câu (dummy it) | "Nó cũng làm méo mó…" | lặp danh từ / nối vế |
| "một cách + adj" (-ly) | "đánh giá một cách cẩn thận" | "đánh giá kỹ" |
| ", điều mà/điều này" (which) | "…, điều mà giúp…" | cắt câu, nối bằng "nên/vì" |
| Dấu Tây | em-dash — dày, semicolon, Oxford comma | phẩy/ngoặc/hai chấm; cắt câu |
| Thiếu trợ từ cuối câu | zero nhé/đấy/đâu/mà | 1–2 trợ từ/section, đúng chỗ dặn bẫy |
| Thiếu từ láy | "không rõ ràng", "rất không chắc chắn" | "lấp lửng", "bấp bênh", "mờ mịt" |

## TIER 4 — FORMATTING (tài liệu in/docx)

- **Bold-itis**: đậm tràn lan, đậm mọi lần term xuất hiện. CHUẨN: term đậm đúng LẦN ĐẦU + nhãn; nhấn mạnh bằng cú pháp, không bằng format.
- **Bullet khuôn "- Term: giải thích" 10 dòng đều** — tell list đặc trưng nhất. CHUẨN: prose là mặc định; bullet chỉ cho item đếm được.
- **Header spam** (mỗi 2 đoạn 1 heading hoán đổi được). CHUẨN: 1 heading = 1 đơn vị dạy thật, section KHÔNG đều nhau.
- **Emoji làm bullet/heading** → zero trong tài liệu in (semantic icon = hệ callout box).
- **Table-itis**: bảng 2 cột 3 dòng đáng lẽ là 1 câu. CHUẨN: bảng chỉ khi có ma trận so sánh thật.
- **Markdown residue trong docx** (`**`, `##`, `==`, `—----`) = tag leak, quét bắt buộc.
- **Zoom-out test 25%**: mọi trang cùng texture (heading-bullet-bold đều nhịp) = skeleton vẫn máy dù chữ đã sạch.

## TIER 5 — DOMAIN (ví dụ chuẩn hoá từ finance/giảng dạy — nguyên tắc áp được domain khác)

1. Người thật vào bài bằng CON SỐ/TÌNH HUỐNG/SAI LẦM cụ thể, không chào mừng.
2. Thuật ngữ: nói đủ 1 lần rồi NÓI TẮT (FRA, mock, khối ngoại, kéo trụ) — AI lặp đủ cụm dài.
3. DÁM CHẤM ĐIỂM có địa chỉ ("Qbank Kaplan giải thích sơ sài") — AI hedge tròn trịa.
4. Số lẻ dày ("mock 57.1%", "bán ròng hơn 3.000 tỷ") — AI định tính chung chung.
5. ⚠️ **VÍ DỤ BỊA là tell nguy hiểm nhất**: AI dựng case thương hiệu thật + sự kiện giả. LUẬT: case phải kiểm chứng được (mã + thời điểm) HOẶC đánh dấu ước lượng (~, "tầm").
6. Nhận định NEO THỜI GIAN (phiên/quý/năm) — văn AI phi thời gian.
7. Kết mục bằng hành động/bẫy/mẹo — không tổng kết lại ý vừa viết.

## PROTOCOL DƯƠNG TÍNH (làm văn người — liều ≤1–2 lần/1.000 từ MỖI kỹ thuật)

1. Câu ngắn đấm sau chuỗi câu dài (đúng chỗ twist).
2. Quan điểm có gan + hedge CÓ ĐỊA CHỈ ("số này tôi ngờ — nhạy với giả định 2%").
3. Kể sự kiện đủ cụ thể để ý nghĩa TỰ toát — không dán nhãn "điều này cho thấy tầm quan trọng".
4. Chủ ngữ người + động từ mạnh (gỡ "việc/sự").
5. Chi tiết đắt: số, tên, ngày.
6. Câu hỏi Socratic hỏi thật trả lời ngay, ≤1/section.
7. Dẫn qua cái sai trước (cách ngây thơ → sai → vì sao → cách đúng).
8. Nhấn bằng cú pháp ("chính X mới là", đảo câu, câu cụt đứng riêng).
9. Trợ từ cuối câu 1–2/section — vũ khí riêng tiếng Việt.
10. Chuẩn Nguyễn Hiến Lê: pass cuối xoá hết trang trí; câu còn đứng vững thì giữ bản đã xoá.
⛔ KHÔNG giả typo (phá credibility). KHÔNG cố tỏ ra người thật — >3 hiệu ứng nhìn thấy/trang là bỏ bớt (cơ chế chống tái sinh tic kiểu "GHÉ TAI").

## LINT REGEX (quét cơ học trước khi giao)

```
(Trong bối cảnh|Trong thế giới|kỷ nguyên số|Hãy cùng|Chào mừng|Dưới đây là)
(không chỉ[^.]{0,60}mà còn|không phải[^.]{0,40}mà là)   # đếm; >1/bài = flag
(Điều quan trọng cần lưu ý|có thể nói rằng|Đáng chú ý là|cần lưu ý rằng)
(Tóm lại|Nhìn chung|Như vậy[,]? (ta|chúng ta) (thấy|có thể thấy))
(Hơn nữa|Bên cạnh đó|Thêm vào đó|Ngoài ra)               # đếm mật độ/1000 từ
(đóng vai trò (quan trọng|then chốt)|minh chứng cho|bước ngoặt|nâng tầm|đi sâu vào)
được [^.]{0,30} bởi                                        # passive+bởi
một cách [a-zà-ỹ]+                                         # -ly calque
, điều (mà|này)                                            # which-clause
\*\*|##|==|•                                               # markdown residue trong docx
std-dev độ dài câu < 0.4 → flag nhịp máy (đo bằng script)
```

## META
- Tell TRÔI theo version model (GPT-5.1 đã bớt em-dash; đa số evidence đo Claude 3.5) — tái research mỗi ~6 tháng.
- Tell sống sót qua dịch: khung câu Claude vẫn hiện trong tiếng Việt (ICML 2025, 97.1% attribution).
- Sửa từng chữ chưa đủ: "de-delved nhưng thought structure vẫn là model" — phải sửa cả NHỊP + LẬP TRƯỜNG + CHẤT LIỆU.


> Kill-list cá nhân (nếu có) nằm trong `profiles/<tên>.md`, KHÔNG nằm ở đây — tell phổ quát và tic cá nhân là hai tầng khác nhau.
> Verdict Tier 1 phải đối chiếu REGISTER_MAP trước khi áp (vd 'Tóm lại' hợp lệ ở học thuật).
