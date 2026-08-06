---
name: vn-humanizer
description: >
  Humanizer tiếng Việt tổng quát — biến văn "đúng nhưng máy" thành văn người thật, cho MỌI thể loại
  (báo chí, học thuật, marketing, social, email công sở, báo cáo tài chính, blog, tài liệu kỹ thuật).
  4 chế độ: humanize văn có sẵn · co-write từ đầu · audit/chấm điểm độ-người · learn-my-voice (distill
  giọng riêng từ văn mẫu của user thành profile cắm-rút). LUÔN dùng skill này khi user nói: "humanize",
  "làm bớt AI / bớt máy", "viết lại cho tự nhiên", "văn này nghe AI quá", "check xem có giống AI không",
  "chấm độ người", "học giọng tôi", "viết theo giọng của tôi/của X", "đổi giọng sang...", "de-AI",
  "văn Việt tự nhiên" — kể cả khi họ chỉ than "đọc cứng quá / sượng quá / giả trân" về một đoạn tiếng Việt.
  Không giới hạn chủ đề: skill tự phát hiện register + ngữ cảnh + quan hệ người viết-người đọc trước khi sửa.
---

# vn-humanizer — humanizer tiếng Việt tổng quát

> Nâng cấp tổng quát hoá từ note-pipeline-humanizer (CFA). Nền: 12 luồng research 2026-07-09
> (WP:AISIGNS, ICML-2025 Idiosyncrasies, PNAS Reinhart, Burrows's Delta, DIPPER/TH-Bench,
> phong cách học Đinh Trọng Lạc, ngữ dụng xưng hô Cao Xuân Hạo school, corpus 245 tic thực chiến).
> Archive research đầy đủ: `Premium CFA/Xu Ly Notes L1 new/research_ai_tells_2026-07-09/`.

## Triết lý (đọc trước khi làm bất cứ gì)

1. **Tell là TƯƠNG ĐỐI theo register.** "Tóm lại" bắt buộc trong kết luận học thuật, chết trong caption.
   "Kính gửi" chuẩn email, sai mọi nơi khác. → Không có kill-list phổ quát; chỉ có (cụm, register→verdict).
2. **Ba tầng tách bạch:** (a) universal de-AI (nhịp, cấu trúc, hedging) — mọi ngôn ngữ;
   (b) tầng tiếng Việt (calque, xưng hô, trợ từ, phương ngữ); (c) tầng VOICE — profile cắm-rút,
   kill-list của một người là DỮ LIỆU của profile người đó, không phải luật của skill.
3. **Đo thay vì cấm:** mật độ so với baseline của register (logic z-score), không hard-ban.
4. **No-new-tic:** humanizer không được đẻ mannerism mới. >3 hiệu ứng "người" nhìn thấy trên một trang
   = đang diễn. Mọi chữ ký giọng có NGÂN SÁCH tần suất.
5. **Detector chỉ là còi báo khói.** Không bao giờ tối ưu để lách máy detect — tối ưu cho người đọc.
6. **Cơ chế lỗi gốc của AI = bị kéo về "register mặc định essay"** (mở–3 ý–kết, lịch sự trung tính đều đều).
   Vì vậy lỗi nặng nhất luôn nằm ở KHUÔN MỞ/KẾT lệch chuẩn register — soi trước tiên.

## BƯỚC 0 — DETECTION (bắt buộc, trước mọi mode)

Xác định 5 thứ từ text/yêu cầu (suy không ra → HỎI user, tối đa 3 câu):
1. **Register** (8 loại — đọc `references/REGISTER_MAP.md`): tín hiệu cấu trúc ("Kính gửi"/hashtag/
   bước đánh số/trích dẫn) mạnh nhất → xưng hô → thống kê câu. Lai không rõ → chỉ áp tell universal.
2. **Chủ đề/domain** → quyết định xử lý thuật ngữ (tài chính: bilingual term-first; đời thường: thuần Việt).
3. **Quan hệ người viết → người đọc** → chọn CẶP xưng hô (đọc `references/XUNG_HO.md`) — chọn sai cặp
   thì mọi thứ khác vô nghĩa; nhất quán 100% cả bài.
4. **Mục đích** (dạy / thuyết phục / thông báo / giải trí) → chọn move tu từ.
5. **Vùng miền + tuổi độc giả** (nếu liên quan) → lexicon (đọc `references/LEXICON.md`); mặc định
   trung tính, nhất quán một hệ, KHÔNG tự chèn slang.

## 4 CHẾ ĐỘ

### Mode A — HUMANIZE văn có sẵn (mặc định khi user đưa text)
1. Bước 0 → chọn bộ luật + baseline.
2. Chạy `scripts/lint_vi.py <file> --register <R>` (hoặc quét tay theo `references/AI_TELLS_VI.md`
   Tier 1) → danh sách hit.
3. Sửa MINIMAL-DIFF: giữ nghĩa/số/term/trích dẫn nguyên vẹn; chỉ thay đoạn khác nhau. Ưu tiên:
   khuôn mở/kết lệch register → xưng hô sai cặp → Tier 1 lexical → Vietlish calque → nhịp
   (chỉ khi được phép sửa sâu).
4. Whitelist bất khả xâm phạm: set-phrase chuẩn mực ngành, trích dẫn, văn bản pháp lý, tên nút/lệnh
   trong tài liệu kỹ thuật, keyword SEO chủ đích. Test "earned vs orphan" cho metaphor: được nuôi
   bằng hình ảnh dựng trước thì GIỮ.
5. **Tối đa 2 vòng sửa** (vòng 3+ = recursive-paraphrase decay). Sau sửa: re-lint, so before/after;
   CV nhịp câu + đa dạng từ vựng KHÔNG được giảm (no-regression gate).
6. Báo cáo: gì đã sửa theo family, gì GIỮ và vì sao (nêu rõ các quyết định giữ có chủ đích).

### Mode B — CO-WRITE từ đầu
Bước 0 → nếu có voice profile (user chỉ định hoặc `profiles/` có sẵn) thì nạp; không có thì dùng
chuẩn register + PROTOCOL DƯƠNG TÍNH (AI_TELLS_VI.md, liều ≤1–2/1000 từ/kỹ thuật). Viết xong
tự chạy Mode C lên chính bản nháp, sửa 1 vòng.

### Mode C — AUDIT / chấm độ-người (không sửa)
Chạy lint + đọc tay theo 5 tier → report: (a) bảng hit theo family + mật độ/1000 từ so baseline
register; (b) 3 lỗi nặng nhất kèm ví dụ nguyên văn; (c) điểm 1–10 từng trục: nhịp / lập trường /
chất liệu cụ thể / xưng hô / lexicon; (d) khuyến nghị sửa hay viết lại. KHÔNG đụng text.

### Mode D — LEARN-MY-VOICE (distill giọng từ văn mẫu)
Đọc `references/VOICE_DERIVE.md` và làm đủ B0→B5: corpus cùng-register 10k+ từ → pass định lượng
(nhịp, punctuation, n-gram lặp) → pass định tính (persona, moves, miền ẩn dụ — cấm nói về chủ đề)
→ triage 3 rổ bằng checklist 6 câu CHỮ KÝ vs TIC → lắp profile (identity → rule dương tính →
chữ ký + ngân sách tần suất → kill-list ≤10 kèm replacement → quote bank 3–7 đã lọc tic →
2–3 cặp pseudo-parallel) → validate (tic counter = 0, chữ ký ≤ budget; đề nghị user blind-test).
Lưu thành `profiles/<tên>.md` theo template trong VOICE_DERIVE.md. **Cảnh báo caricature:** model
khuếch đại cụm nổi bật thành tic — mọi chữ ký PHẢI có budget, validator phải đếm.

## LUẬT ANTI-OVERFITTING (6 mode hỏng đã ghi nhận — SCORING.md có bằng chứng)

1. Corpus-transfer: rule sinh từ corpus này bắn nhầm set-phrase corpus khác → whitelist phân lớp
   + thử rule mới trên hold-out trước khi áp đại trà.
2. Mannerism rotation: diệt tic cũ đẻ tic mới → sau mỗi sweep, scan chính OUTPUT tìm cụm lặp mới.
3. Over-sanitization: gọt sạch đuôi phân phối → văn về mean → GIỐNG AI HƠN. Giữ độ gồ ghề tự nhiên.
4. Goodhart: không tối ưu theo detector score.
5. Frequency-blind: mọi rule là mật độ-tương-đối, không phải có/không.
6. Pipeline drift: nhiều pass kéo nhiều hướng → max 2 vòng + no-regression gate + hold-out 5–10%.

## Checklist trước khi giao (mọi mode có sửa/viết)
- [ ] Đúng khuôn mở/kết của register? Xưng hô đúng cặp + nhất quán 100%?
- [ ] Lint Tier 1 sạch theo verdict CỦA register này (không phải register khác)?
- [ ] Whitelist còn nguyên (set-phrase, trích dẫn, term, keyword, tên nút)?
- [ ] Nhịp: có câu ngắn đấm đúng chỗ? CV không giảm so bản gốc?
- [ ] Số/tên/ngày giữ nguyên từng ký tự? Ví dụ thực thể thật phải kiểm chứng được hoặc đánh dấu ~?
- [ ] Không tic mới? Chữ ký (nếu dùng profile) trong ngân sách? ≤3 hiệu ứng nhìn thấy/trang?
- [ ] Trợ từ cuối câu ≤1/câu, đúng sắc thái, đúng register (học thuật ≈ 0)?

## Files
- `references/AI_TELLS_VI.md` — 5 tier tells + protocol dương tính + lint regex (universal + VN)
- `references/REGISTER_MAP.md` — 8 register: chuẩn mở/kết, tell riêng, cụm hợp-lệ-riêng, cách detect
- `references/XUNG_HO.md` — bảng cặp xưng hô × quan hệ, trợ từ map sắc thái, pro-drop, làm mềm mệnh lệnh
- `references/LEXICON.md` — phương ngữ/thế hệ/Hán-Việt: tier ĐỎ-VÀNG-XANH + 4 câu kiểm
- `references/VOICE_DERIVE.md` — pipeline learn-my-voice B0→B5 + checklist chữ-ký-vs-tic + template profile
- `references/SCORING.md` — metric đo được, z-score protocol, 6 overfitting mode, self-check loop 7 bước
- `scripts/lint_vi.py` — lint chạy được: regex tier-1 theo register + nhịp câu CV + mật độ connector
- `profiles/cfa-teacher.md` — profile mẫu (giọng thầy CFA đã đi thi) — minh hoạ cấu trúc profile chuẩn
