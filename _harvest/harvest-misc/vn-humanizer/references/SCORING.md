> [vn-humanizer reference — load khi SKILL.md trỏ tới. File dài: đọc mục lục/heading trước, nhảy tới mục cần.]

# VNH-4 — Đo lường "độ người" của văn + rủi ro overfitting khi humanize

Research note (web research, 2026-07-09). Phạm vi: (1) stylometry metrics đo được bằng script cho tiếng Việt, (2) bài học từ văn học paraphrase-attack vs AI-detector, (3) 6 overfitting modes của style-rule system + cách phòng, (4) rubric chấm mù cho human reviewer, (5) thiết kế self-check loop.

**Kết luận 1 dòng:** Không tồn tại ngưỡng "human-ness" tuyệt đối đáng tin (nhất là cho tiếng Việt — lit gần như toàn English); cách đúng duy nhất là **đo khoảng cách tới baseline giọng thật của chính mình** (z-score vs corpus 102 module đã chuẩn hoá — đúng logic Burrows's Delta), dùng detector/tic-list chỉ làm tín hiệu phụ, và khoá vòng lặp bằng blind human review trên hold-out.

---

## Phần 1 — Stylometry features đo được bằng script cho tiếng Việt

### 1.0 Tiền đề bắt buộc: tokenization tiếng Việt

- Tiếng Việt là isolating language: whitespace tách **âm tiết**, không tách **từ**; ~85% word types là đa âm tiết, và 80%+ syllable types tự nó cũng là từ → mọi metric đếm "word" (TTR, MTLD, function-word freq) lệch nếu không word-segment ([arXiv 1709.06307](https://arxiv.org/pdf/1709.06307), [AAAI 2025 — Vietnamese words are not constructed from syllables](https://ojs.aaai.org/index.php/AAAI/article/view/34581)).
- Segmenter thực dụng: RDRSegmenter/VnCoreNLP (F1 ≈ 97.9%) hoặc UETSegmenter (F1 ≈ 98.8%) ([arXiv 1906.07662](https://arxiv.org/pdf/1906.07662)); underthesea là lựa chọn pip-friendly.
- **Quy tắc thực dụng:** nếu ngại dependency, tính mọi thứ trên syllable-token CŨNG ĐƯỢC — miễn là baseline và bản test đi qua **cùng một pipeline** (so sánh nội bộ, không so cross-study). Kết quả MTLD/TTR phụ thuộc tokenization/case-folding là limitation đã ghi nhận ([MetricGate MTLD docs](https://metricgate.com/docs/mtld-lexical-diversity/)).
- Note song ngữ CFA: strip trước khi đo — công thức/LaTeX/OMML, bảng, code block, tiêu đề, LOS, thuật ngữ tiếng Anh in-line (hoặc đếm riêng thành 1 kênh "EN-term density").

### 1.1 Bộ metric (xếp theo độ robust từ cao xuống thấp)

| # | Metric | Cách tính (script) | Robust? | Ngưỡng khởi điểm (PHẢI calibrate lại trên baseline riêng) |
|---|--------|--------------------|---------|------------------------------------------------------------|
| 1 | **Function-word distribution** (hư từ) | Tần suất /1k token của ~50–150 hư từ phổ biến nhất; so với baseline bằng Burrows's Delta (mean |z|) hoặc Jensen–Shannon divergence | **Cao nhất.** Chuẩn vàng authorship attribution từ Mosteller–Wallace; bền với thay đổi topic ([Function Word Adjacency Networks](https://arxiv.org/pdf/1406.4469), [Testing Burrows's Delta](https://academic.oup.com/dsh/article/19/4/453/943644)) | Flag khi Delta > mean+2SD của phân phối Delta nội-baseline (đo Delta giữa từng cặp note baseline để có phân phối "bình thường") |
| 2 | **Sentence-length CV** (burstiness câu) | Tách câu theo `.!?;\n`, đếm token/câu, CV = SD/mean; thêm % câu <8 token và % câu >40 token (đuôi phân phối) | **Cao.** LLM dồn cụm 10–30 token, human phân tán hơn, nhiều câu rất dài/rất ngắn hơn ([Muñoz-Ortiz et al. — Contrasting Linguistic Patterns](https://arxiv.org/pdf/2308.09067)); burstiness thấp là AI-signature lặp lại qua nhiều corpus ([StyloAI](https://arxiv.org/html/2405.10129v1)) | Heuristic từ lit English: CV < ~0.35 → nghi uniform-AI; human editorial thường 0.45–0.70. **Chỉ dùng làm điểm xuất phát**; ngưỡng thật = z vs 102 module |
| 3 | **Punctuation profile** | Đếm /1k token: `, . : ; — – … ( ) " ! ?` + % câu fragment (không động từ) | **Trung-cao.** Human dùng dash/ellipsis/fragment "kịch tính" hơn; em-dash là AI-tell nổi tiếng 2024–2025 — tần suất em-dash trong abstract khoa học **tăng hơn 2×** giai đoạn 2021–2025 ([Em Dash as a Site of Contest](https://www.researchgate.net/publication/398319038_The_Em_Dash_as_a_Site_of_Contest_Between_AI_Determinism_and_Human_Agency), [Nick Potkalitsky](https://nickpotkalitsky.substack.com/p/why-ai-cant-stop-using-em-dashes)) | Đo lệch từng dấu so baseline; chú ý em-dash, "…", và mật độ dấu hai chấm mở-danh-sách (markdown fingerprint — [The Last Fingerprint](https://arxiv.org/pdf/2603.27006)) |
| 4 | **Lexical diversity — MTLD/MATTR (KHÔNG dùng raw TTR)** | MTLD (factor threshold 0.72) hoặc MATTR (window 50–100 token) trên văn bản ≥100 token | **Trung.** Raw TTR nhạy độ dài văn bản (flaw kinh điển); MTLD ít bị ảnh hưởng độ dài nhất, MATTR là bản sửa windowed ([McCarthy & Jarvis qua MetricGate](https://metricgate.com/docs/mtld-lexical-diversity/), [ScienceDirect — text length effects](https://www.sciencedirect.com/science/article/abs/pii/S0346251X12000887)) | AI thường có lexical diversity thấp hơn human cùng thể loại; flag khi z < −1.5 vs baseline. Văn <100 token: bỏ, giá trị không ổn định |
| 5 | **Paragraph variance** | CV độ dài đoạn (token/đoạn); % đoạn 1 câu; % đoạn đúng 3–4 câu; nhịp heading/bullet | **Trung-thấp** (nhiễu cao, phụ thuộc format note). AI ra đoạn đều tăm tắp + nghiện bullet/heading do markdown training ([The Last Fingerprint](https://arxiv.org/pdf/2603.27006)) | So baseline; đặc biệt flag "mọi đoạn 3–4 câu" và "mọi section có đúng n bullet" |
| 6 | **Template/n-gram repetition** | Top 3–4-gram lặp /10k token; sentence-opener diversity (entropy của 2 token đầu câu); mật độ discourse marker ("tuy nhiên", "do đó", "ngoài ra", "bên cạnh đó", "nhìn chung", "tóm lại", "đáng chú ý") | **Trung** cho mục đích tic-hunting; đây chính là kênh phát hiện "excess vocabulary" kiểu delve ([Kobak et al. — Delving into ChatGPT usage](https://arxiv.org/html/2406.07016v1)) | Flag n-gram nào có tần suất > 3× baseline (density-relative, không hard-ban — xem Phần 3) |

**Starter list hư từ tiếng Việt** (mở rộng lên 100–150 từ tần suất cao nhất của chính baseline, đúng cách Burrows lấy 150 MFW): của, và, là, có, được, trong, cho, với, đã, đang, sẽ, các, những, một, này, đó, kia, khi, nếu, thì, mà, để, cũng, lại, rất, khá, hơn, nhất, vẫn, chỉ, từ, về, theo, như, nhưng, vì, do, nên, bởi, tại, giữa, sau, trước, cùng, đều, càng, tức, nghĩa, chính, ngay, luôn, từng, mỗi, mọi.

**Về "ngưỡng nào":** văn học không cho ngưỡng tuyệt đối chuyển giao được — các nghiên cứu cross-domain cho thấy feature phân biệt AI/human **đổi hẳn giữa dataset** ([Why AI-Generated Text Detection Fails](https://arxiv.org/html/2603.23146v2)). Cách đúng (và cũng là cách Burrows's Delta hoạt động): z-score từng metric so với mean/SD của baseline nội bộ; **|z| ≤ 1.5 pass, 1.5–2 review, > 2 flag**. PNAS 2025 xác nhận LLM instruction-tuned vẫn phân biệt được với human bằng grammatical/rhetorical style features — tức bộ feature trên có thật, nhưng magnitude là chuyện của từng corpus ([Do LLMs write like humans? — PNAS](https://www.pnas.org/doi/10.1073/pnas.2422455122)).

---

## Phần 2 — Bài học từ văn học humanization / paraphrase-attack

### 2.1 Detector rất dễ lách…

- **DIPPER** (Krishna et al., NeurIPS 2023): paraphraser 11B (T5-XXL) đánh sập hàng loạt detector — DetectGPT rơi từ 70.3% → **4.6%** detection @1%FPR; watermarking, GPTZero, OpenAI classifier đều thủng ([paper + repo](https://github.com/martiansideofthemoon/ai-detection-paraphrases), [NeurIPS poster](https://neurips.cc/virtual/2023/poster/71402)).
- **Sadasivan et al. — "Can AI-Generated Text be Reliably Detected?"**: recursive paraphrasing hạ watermark detection 99.3% → **9.7%**, DetectGPT AUROC 96.5 → 25.2; kèm **impossibility result**: khi LLM càng giỏi, total-variation distance giữa phân phối văn AI và văn người co lại → detector tốt nhất cũng tiệm cận random ([arXiv 2303.11156](https://arxiv.org/abs/2303.11156)).
- **Adversarial Paraphrasing** (NeurIPS 2025): paraphrase có detector dẫn đường, giảm trung bình **87.88% T@1%F** across detectors, transferable ([arXiv 2506.07001](https://arxiv.org/abs/2506.07001)).
- **RAID benchmark** (ACL 2024): 6M+ mẫu, 11 attack; homoglyph làm 5 detector rơi trung bình **40.6%**, synonym-swap làm metric-based detector rơi tới 36.1% ([arXiv 2405.07940](https://arxiv.org/html/2405.07940v1), [repo](https://github.com/liamdugan/raid)).

### 2.2 …nhưng "lách được detector" ≠ "đọc như người" — bằng chứng

1. **Attack thắng detector bằng cách phá chữ, không phải bằng cách viết hay hơn:** RAID attacks gồm homoglyph, zero-width space, misspelling, article deletion — máy mù nhưng người đọc thấy văn hỏng ngay ([RAID](https://arxiv.org/html/2405.07940v1)). DAMAGE ghi nhận adversarial tricks "come at the cost of readability or fidelity — missing articles, odd spellings… obviously flawed to a human reader" ([arXiv 2501.03437](https://arxiv.org/pdf/2501.03437)).
2. **Humanizer thương mại:** khảo sát 19 tool humanizer/paraphraser (DAMAGE) + các test độc lập: có tool qua mặt detector bằng cách làm văn "messy như bản nháp" — một mẫu được ghi nhận **97 lỗi ngữ pháp, content score 54/100** sau humanize; văn thành dài dòng, rối, thậm chí sai fact ([DAMAGE](https://arxiv.org/pdf/2501.03437), [Hastewire test](https://hastewire.com/blog/can-ai-humanizers-pass-detection-test-results-revealed-55-chars)).
3. **TH-Bench** (benchmark chuyên cho humanizing attacks): đánh giá theo 3 trục — evading effectiveness, text quality, computational overhead — và kết luận **không attack nào thắng cả 3 trục**; tradeoff là quy luật, không phải ngoại lệ ([arXiv 2503.08708](https://arxiv.org/pdf/2503.08708)).
4. **Chiều ngược lại cũng sai:** detector flag oan văn người — 7 detector flag trung bình **61.3%** bài TOEFL của người thật là AI (và ≥1 detector flag 97.8%!), vì perplexity thấp/từ vựng ít biến hoá; "polish từ vựng bằng ChatGPT" lại làm FPR rơi còn 11.6% ([Liang et al. — GPT detectors are biased](https://arxiv.org/abs/2304.02819)). Tức là: **điểm detector đo "độ lệch khỏi phông thống kê nó học", không đo "độ người"** — tối ưu theo nó chỉ dời văn sang một phông khác.
5. Ngay cả attack "sạch" nhất (Adversarial Paraphrasing, 87% mẫu được chấm 4–5/5) vẫn tự nhận "**mostly** a slight degradation in text quality" — chất lượng luôn trả giá, chỉ là ít hay nhiều ([arXiv 2506.07001](https://arxiv.org/abs/2506.07001)).

### 2.3 Hệ quả thiết kế cho pipeline humanize của mình

- **Không bao giờ dùng AI-detector score làm objective** (kể cả làm "điểm phụ để kéo xuống"). Objective đúng = khoảng cách stylometric tới baseline giọng thật + human blind rating.
- Detector nếu dùng, chỉ dùng như **smoke alarm một chiều**: điểm "AI 99%" trên đoạn dài → đáng nhìn lại; điểm "human" → không có nghĩa gì.
- **Giới hạn số vòng sửa**: recursive paraphrasing là cơ chế làm mất chất lượng dần đều (mỗi vòng xa bản gốc thêm) — cap 2 vòng patch/đoạn, minimal-diff (trùng bài học minimal-diff patcher nội bộ).

---

## Phần 3 — 6 overfitting modes của style-rule system + cách phòng

Bối cảnh nội bộ: kill-list decringe 2027 sinh từ chính corpus 2027; đã quan sát "humanizer skill sẽ TÁI SINH tic". Văn học bên ngoài xác nhận cả 6 mode dưới đây đều có tiền lệ.

**Mode 1 — Corpus-transfer false positive** (rule sinh từ corpus A áp lên corpus B). Rule "từ X = AI" chỉ đúng trong phân phối nó được sinh ra. Bằng chứng kinh điển: "delve" là từ **bình thường trong Nigerian/African business English** → người Nigeria bị buộc tội dùng AI oan hàng loạt ([Simon Willison](https://simonwillison.net/2024/Apr/18/delve/), [Times Higher Education](https://www.timeshighereducation.com/blog/policing-ai-use-counting-telltale-words-flawed-and-damaging)); detector học 1 corpus rơi 5–30 điểm AUROC khi đổi domain ([arXiv 2603.17522](https://arxiv.org/pdf/2603.17522)). Bản CFA: rule bắn nhầm **set-phrase thuật ngữ** ("đường cong lợi suất", "dòng tiền chiết khấu"), trích dẫn LOS/CFA Institute, ví dụ chuẩn hoá lặp lại có chủ đích.
   → *Phòng:* **whitelist** theo lớp: (a) thuật ngữ song ngữ + set-phrase tài chính, (b) trích dẫn/LOS/công thức — freeze hoàn toàn, (c) cụm chủ đích của giọng chuẩn (đã có trong VOICE_PROFILE). Rule mới chỉ được enable sau khi chạy thử trên hold-out văn người và FP-rate < ngưỡng (vd <1 hit oan/10k từ).

**Mode 2 — Mannerism rotation** (diệt tic cũ, sinh tic mới). Bằng chứng ở quy mô toàn ngành: sau khi "delve/intricate/meticulous" bị điểm mặt đầu 2024 (delve từng tăng 28×, meticulously +137%), tần suất chúng **giảm rõ rệt** trong bài đăng học thuật — nhưng phong cách AI không biến mất, nó dời sang marker khác (em-dash 2×, "not just X, it's Y", markdown-nghiện-bullet) ([Human-LLM Coevolution](https://arxiv.org/pdf/2502.09606), [Kobak et al.](https://arxiv.org/html/2406.07016v1), [Em-dash studies](https://www.researchgate.net/publication/398319038_The_Em_Dash_as_a_Site_of_Contest_Between_AI_Determinism_and_Human_Agency)). Kill-list tĩnh do đó **luôn trễ một nhịp**.
   → *Phòng:* tic-watchlist **tự cập nhật**: sau mỗi sweep, chạy lại "excess n-gram scan" (tần suất n-gram bản mới / baseline) — tic mới nổi sẽ tự lộ như delve đã lộ trong PubMed scan. Kill-list là output của scan, không phải input bất biến.

**Mode 3 — Over-sanitization / regression to the mean** (gọt quá tay ra văn vô hồn). Nghịch lý đo được: đuôi phân phối (câu cụt, câu rất dài, dash, fragment, từ đắt hiếm) chính là chỗ "chất người" nằm — human có burstiness cao, punctuation kịch tính hơn AI ([StyloAI](https://arxiv.org/html/2405.10129v1), [Contrasting Linguistic Patterns](https://arxiv.org/pdf/2308.09067)). Sanitize mọi thứ "lạ" = ép văn về mean = **làm văn GIỐNG AI HƠN theo chính stylometry**. Đây cũng là lý do TOEFL essays (từ vựng phẳng, an toàn) bị flag oan 61.3%.
   → *Phòng:* mọi rule diệt tic phải đi kèm **floor cho variance**: sau patch, sentence-length CV / punctuation entropy / MTLD không được giảm quá z=−0.5 so trước patch (no-regression gate ở Phần 5).

**Mode 4 — Goodhart / detector-objective hacking** (tối ưu để lách máy đo). Khi metric thành mục tiêu, hệ tìm nghiệm suy biến: homoglyph, misspelling, đảo chữ — thắng detector, thua người đọc (RAID/DAMAGE, Phần 2.2). Phiên bản nội bộ: nếu tự chấm bằng chính script scoring rồi patch cho tới khi "điểm đẹp", sẽ ra văn tối ưu-theo-script (vd nhét câu cụt vô nghĩa để kéo CV lên).
   → *Phòng:* tách **metric để chẩn đoán** khỏi **metric để nghiệm thu**. Script chỉ ra *chỗ nghi* (diagnostic); nghiệm thu cuối = blind human rubric (Phần 4) trên sample. Không bao giờ iterate quá 2 vòng trên cùng một metric.

**Mode 5 — Frequency-blind rule** (đếm tuyệt đối thay vì mật độ so baseline). Hard-ban một từ/cấu trúc mà văn người thật vẫn dùng (chỉ là ít hơn) tạo văn "có lỗ hổng" — thiếu hư từ chuyển ý ở chỗ đáng có cũng bất thường như thừa. Toàn bộ truyền thống authorship attribution (Burrows's Delta) đo bằng **z-score tần suất so reference corpus**, không đo bằng có/không ([Testing Burrows's Delta](https://academic.oup.com/dsh/article/19/4/453/943644)).
   → *Phòng:* **density-relative-to-baseline**: rule dạng "tần suất cụm X không quá k× baseline /10k từ" thay vì "cấm X". Chỉ hard-ban cụm baseline-frequency = 0 thật sự (tic thuần AI chưa từng xuất hiện trong 102 module).

**Mode 6 — Rule-interaction / pipeline drift** (nhiều pass sửa chồng, phân phối trôi dần không ai thấy). Mỗi pass (humanize → de-meta → decringe → org-refine) kéo phân phối một hướng nhỏ; qua nhiều pass, tổng drift lớn nhưng không pass nào "có lỗi". Tương tự in-domain overfitting của detector fine-tuned: mỗi bước khớp hơn với cái nó vừa thấy, tệ hơn với phần còn lại ([arXiv 2603.23146](https://arxiv.org/html/2603.23146v2)); kinh nghiệm nội bộ docx≠markup desync là một biến thể cơ học của mode này.
   → *Phòng:* **hold-out review**: giữ N note (5–10%) không đi qua pass mới, làm control; định kỳ so metric-profile nhóm sửa vs nhóm control vs baseline gốc; kèm blind A/B người đọc. Mọi pass mới phải chạy trên hold-out trước khi sweep toàn bộ.

**Tóm tắt 3 lớp phòng thủ:** (1) whitelist phân lớp + FP-test trước khi enable rule; (2) mọi ngưỡng là density-relative-to-baseline (z-score), có floor cho variance; (3) hold-out + blind human review làm nghiệm thu cuối, script chỉ chẩn đoán.

---

## Phần 4 — Rubric chấm "human-ness" cho human reviewer (blind)

### 4.1 Protocol (chống bias trước, rubric sau)

- **Blind + trộn mẫu:** mỗi phiên chấm trộn 3 loại đoạn (không nhãn): (a) văn người thật cùng thể loại (đoạn từ note chuẩn cũ / văn user tự viết), (b) văn AI chưa humanize, (c) văn đã humanize. Reviewer không biết tỷ lệ. Đây là chuẩn blind evaluation trong NLG human eval ([Automating Text Naturalness Evaluation](https://arxiv.org/pdf/2006.13268), [Galileo — human eval best practices](https://galileo.ai/blog/human-evaluation-metrics-ai)).
- **Đơn vị chấm:** đoạn 150–300 từ (đủ dài để thấy nhịp, đủ ngắn để chấm 20–30 đoạn/phiên), thứ tự random.
- **≥2 reviewer độc lập**, báo cáo agreement bằng quadratic-weighted Cohen's κ hoặc Gwet's AC2 (chuẩn cho Likert ordinal); κ < 0.4 → rubric mơ hồ, sửa rubric trước khi tin điểm.
- **Insight HUSE** (Hashimoto et al., NAACL 2019): human judgment một mình đo được *quality* nhưng mù với *diversity* (không bắt được văn na ná nhau hàng loạt); metric thống kê một mình thì ngược lại → **bắt buộc kết hợp cả hai**, đúng như loop Phần 5 ([arXiv 1904.02792](https://arxiv.org/abs/1904.02792)).

### 4.2 Rubric 7 tiêu chí (Likert 1–5, chấm từng tiêu chí rồi mới nhìn tổng)

| # | Tiêu chí | 5 điểm trông thế nào | 1 điểm trông thế nào |
|---|----------|----------------------|----------------------|
| 1 | **Nhịp câu** | Dài ngắn xen kẽ tự nhiên, có câu cụt đúng chỗ | Câu nào cũng 20–30 từ, đều như máy khâu |
| 2 | **Giọng & cam kết quan điểm** | Dám khẳng định, có thái độ, biết cái gì quan trọng hơn cái gì | Hedging tràn lan, "có thể", "thường", cân đối vô hồn hai chiều |
| 3 | **Cụ thể vs generic** | Con số thật, tên thật, ví dụ neo được | "Trong bối cảnh hiện nay", "đóng vai trò quan trọng", ví dụ generic thay được cho mọi chủ đề |
| 4 | **Chuyển ý** | Ý này mọc ra từ ý trước, nối hữu cơ | "Tuy nhiên… Ngoài ra… Bên cạnh đó… Tóm lại" xếp hàng như khung xương lộ ra ngoài |
| 5 | **Từ vựng** | Có từ "đắt" bất ngờ mà đúng; không cụm nào lặp đến phát chán | Tic lặp (bất kể tic gì), từ an toàn phẳng lì, không một lựa chọn từ nào gây ngạc nhiên |
| 6 | **Lỗi kiểu người vs lỗi kiểu máy** | Fragment chủ đích, phép so sánh hơi lệch nhưng sống — chấp nhận được | Sai kiểu máy: thừa từ nối, lặp nguyên mệnh đề, ví dụ tự mâu thuẫn, mượt nhưng rỗng |
| 7 | **Turing tổng** | "Đồng nghiệp tôi viết được đoạn này" — không lăn tăn | "Tôi cá đây là AI" trong 5 giây đầu |

Tiêu chí 1–6 bám đúng các trục stylometry Phần 1 (burstiness, epistemic stance, specificity, discourse markers, lexical choice) — các trục này được xác nhận là chỗ human/AI khác nhau có hệ thống ([PNAS](https://www.pnas.org/doi/10.1073/pnas.2422455122), [Contrasting Linguistic Patterns](https://arxiv.org/pdf/2308.09067)) — để human review và script scoring **đối chiếu được với nhau** từng trục.

### 4.3 Thêm 1 bài test A/B rẻ mà mạnh

Bài "guess the source": đưa reviewer cặp đoạn (1 thật + 1 humanized, cùng chủ đề), hỏi "cái nào do người viết?". **Pass bar: tỷ lệ đoán đúng ≤ 60%** (gần chance 50%). Đây chính là phép đo optimal-error-rate mà HUSE hình thức hoá.

**Pass bar tổng cho một note:** mean ≥ 4.0, không tiêu chí nào ≤ 2, A/B ≤ 60%, và κ giữa reviewer ≥ 0.4.

---

## Phần 5 — Self-check loop (thiết kế)

```
[0] FREEZE BASELINE (làm 1 lần, cập nhật theo quý)
    corpus = 102 module chuẩn (giọng đã duyệt)
    → tính mean/SD cho 6 metric Phần 1 (per-note và per-đoạn)
    → tính phân phối Burrows-Delta nội-baseline (cặp note với nhau)
    → xuất baseline.json  +  tách 5–10% note làm HOLD-OUT control (không sweep)

[1] DRAFT / HUMANIZE  (như pipeline hiện tại)

[2] SCRIPT SCORING (chẩn đoán, không phải nghiệm thu)
    z-profile 6 metric vs baseline.json
    |z| ≤ 1.5 pass · 1.5–2 review · > 2 flag  (flag ở mức ĐOẠN, không cả note)

[3] TIC-SCAN (excess n-gram)
    tần suất n-gram bản mới / baseline > 3× → candidate tic
    → lọc qua WHITELIST (thuật ngữ song ngữ / trích dẫn·LOS·công thức = freeze / cụm giọng chuẩn)
    → kill-list phiên này = candidates còn lại (kill-list là OUTPUT của scan)

[4] MINIMAL-DIFF PATCH — chỉ sửa đoạn bị flag, giữ nguyên phần còn lại
    MAX 2 vòng patch / đoạn (chống recursive-paraphrase decay)

[5] NO-REGRESSION GATE (re-score sau patch)
    không metric nào được xấu đi quá z = −0.5 so với TRƯỚC patch
    (đặc biệt: sentence-CV, MTLD, punctuation entropy không được giảm — chống over-sanitize)
    fail → revert đoạn đó, sửa tay hoặc chấp nhận flag

[6] BLIND HUMAN RUBRIC (định kỳ — mỗi ~10 note hoặc mỗi sweep mới)
    sample đoạn từ: nhóm vừa sửa + HOLD-OUT + baseline thật → chấm mù rubric Phần 4 + A/B
    pass bar: mean ≥ 4, A/B ≤ 60%, κ ≥ 0.4

[7] UPDATE WATCHLIST & RULES
    tic mới từ [3]/[6] → vào watchlist
    RULE MỚI chỉ được enable sau khi chạy trên HOLD-OUT văn người thật
    với FP-rate chấp nhận được (<1 hit oan / 10k từ)
    → quay lại [1] cho note kế tiếp
```

**4 nguyên tắc khoá loop:**
1. **Objective = distance-to-own-baseline, không phải detector score.** Detector (nếu chạy) chỉ là smoke alarm một chiều.
2. **Script chẩn đoán, người nghiệm thu.** Không iterate quá 2 vòng trên cùng metric (chống Goodhart, Mode 4).
3. **Mọi ngưỡng đều relative + có floor cho variance** (chống Mode 3, 5).
4. **Không rule nào sống sót nếu chưa qua hold-out FP-test** (chống Mode 1, 6); kill-list tái sinh từ scan mỗi sweep (chống Mode 2).

---

## SOURCES

**Paraphrase / humanization attacks & impossibility**
- Krishna et al. 2023, *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense* (DIPPER, NeurIPS) — https://github.com/martiansideofthemoon/ai-detection-paraphrases ; https://neurips.cc/virtual/2023/poster/71402
- Sadasivan et al., *Can AI-Generated Text be Reliably Detected?* — https://arxiv.org/abs/2303.11156
- *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text* (NeurIPS 2025) — https://arxiv.org/abs/2506.07001
- TH-Bench: *Evaluating Evading Attacks via Humanizing AI Text* — https://arxiv.org/pdf/2503.08708
- DAMAGE: *Detecting Adversarially Modified AI Generated Text* (khảo sát 19 humanizer) — https://arxiv.org/pdf/2501.03437
- RAID: *A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors* (ACL 2024) — https://arxiv.org/html/2405.07940v1 ; https://github.com/liamdugan/raid
- Humanizer quality tests (97 grammar errors case) — https://hastewire.com/blog/can-ai-humanizers-pass-detection-test-results-revealed-55-chars

**Detector unreliability / bias / overfitting**
- Liang et al., *GPT detectors are biased against non-native English writers* — https://arxiv.org/abs/2304.02819
- *Why AI-Generated Text Detection Fails: Evidence from Explainable AI* — https://arxiv.org/html/2603.23146v2
- *Detecting the Machine: benchmark across architectures, domains, adversarial conditions* — https://arxiv.org/pdf/2603.17522

**Stylometry human vs AI**
- Muñoz-Ortiz et al., *Contrasting Linguistic Patterns in Human and LLM-Generated News Text* — https://arxiv.org/pdf/2308.09067
- *Do LLMs write like humans? Variation in grammatical and rhetorical styles* (PNAS 2025) — https://www.pnas.org/doi/10.1073/pnas.2422455122
- StyloAI — https://arxiv.org/html/2405.10129v1
- *Stylometry recognizes human and LLM-generated texts in short samples* — https://arxiv.org/html/2507.00838v2
- *The Last Fingerprint: How Markdown Training Shapes LLM Prose* — https://arxiv.org/pdf/2603.27006

**Lexical tics & rotation ("delve" era)**
- Kobak et al., *Delving into ChatGPT usage in academic writing through excess vocabulary* — https://arxiv.org/html/2406.07016v1
- *Human-LLM Coevolution: Evidence from Academic Writing* (delve giảm sau khi bị điểm mặt) — https://arxiv.org/pdf/2502.09606
- FSU, *Why Does ChatGPT "Delve" So Much?* — https://news.fsu.edu/news/science-technology/2025/02/17/why-does-chatgpt-delve-so-much-fsu-researchers-begin-to-uncover-why-chatgpt-overuses-certain-words/
- Em-dash as AI tell — https://www.researchgate.net/publication/398319038_The_Em_Dash_as_a_Site_of_Contest_Between_AI_Determinism_and_Human_Agency ; https://nickpotkalitsky.substack.com/p/why-ai-cant-stop-using-em-dashes
- "Delve" & Nigerian English false accusations — https://simonwillison.net/2024/Apr/18/delve/ ; https://www.timeshighereducation.com/blog/policing-ai-use-counting-telltale-words-flawed-and-damaging

**Authorship attribution / baseline-relative measurement**
- Hoover, *Testing Burrows's Delta* — https://academic.oup.com/dsh/article/19/4/453/943644
- *Authorship Attribution through Function Word Adjacency Networks* — https://arxiv.org/pdf/1406.4469
- *A Stylometric Investigation of Linguistic Styles Based on a Vietnamese Corpus* — https://www.scirp.org/journal/paperinformation?paperid=113685

**Lexical diversity metrics**
- MTLD / MATTR docs & limitations — https://metricgate.com/docs/mtld-lexical-diversity/ ; https://metricgate.com/docs/mattr-moving-average-ttr/
- *Effects of text length on lexical diversity measures* — https://www.sciencedirect.com/science/article/abs/pii/S0346251X12000887

**Vietnamese NLP prerequisites**
- *Vietnamese Words Are Not Constructed from Syllables* (AAAI 2025) — https://ojs.aaai.org/index.php/AAAI/article/view/34581
- RDRSegmenter / UETSegmenter benchmarks — https://arxiv.org/pdf/1906.07662 ; https://arxiv.org/pdf/1709.06307

**Human evaluation**
- Hashimoto et al., HUSE: *Unifying Human and Statistical Evaluation for NLG* (NAACL 2019) — https://arxiv.org/abs/1904.02792
- *Automating Text Naturalness Evaluation of NLG Systems* — https://arxiv.org/pdf/2006.13268
- Human eval best practices (blind, Likert, κ/AC2) — https://galileo.ai/blog/human-evaluation-metrics-ai ; https://aclanthology.org/2024.acl-long.745/
