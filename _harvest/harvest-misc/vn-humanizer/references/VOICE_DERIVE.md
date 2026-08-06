> [vn-humanizer reference — load khi SKILL.md trỏ tới. File dài: đọc mục lục/heading trước, nhảy tới mục cần.]

# VNH-5 — Distill Voice Profile từ văn mẫu (mode "learn-my-voice")

Research web, 2026-07-09. Bốn câu hỏi: (1) stylometry features nào transfer sang mimicry, (2) best practices few-shot style mimicry, (3) quy trình N bài mẫu → hồ sơ giọng (chữ ký vs tic), (4) validate bằng blind test.

---

## 1. Stylometry / authorship attribution: features nhận dạng tác giả — và cái nào BẮT CHƯỚC được

### 1.1 Bảng feature kinh điển (taxonomy từ literature AA)

| Nhóm | Feature cụ thể | Độ tin cậy nhận dạng |
|---|---|---|
| **Function words** | tần suất mạo từ, giới từ, liên từ, đại từ, trợ động từ (top 150–300 most-frequent words, z-score — Burrows' Delta) | **Cao nhất** — dùng vô thức, ổn định bất kể chủ đề; vector 200–300 MFW cho kết quả chính xác nhất |
| **Lexical richness** | type-token ratio, hapax legomena, Yule's K, MTLD; phân bố độ dài từ | Cao, nhưng nhạy với độ dài văn bản |
| **Câu & nhịp** | mean/variance độ dài câu (burstiness), độ phức tạp cú pháp, subordination | Cao |
| **Punctuation habits** | tỉ lệ dấu phẩy, ưa semicolon/dash/ngoặc đơn, tần suất chấm than | Trung–cao, rất "cá nhân" |
| **Character n-grams** | 2–4 grams ký tự (bắt hình thái từ, chính tả, dấu câu cùng lúc) | Cao nhất trong ML-based AA |
| **Cú pháp & POS** | POS n-grams, cấu trúc MỞ ĐẦU CÂU ưa dùng, grammatical sequences | Cao |
| **Discourse markers** | liên kết diễn ngôn ưa dùng ("tuy nhiên", "nói cách khác", "thực ra"), cách chuyển ý | Trung–cao, dễ quan sát |
| **Structural** | độ dài đoạn, cách xuống dòng, heading/list habits, chào–ký (email) | Trung |
| **Readability** | Flesch-Kincaid, Gunning Fog | Thấp–trung, chỉ dùng làm nền |

Nguồn: survey stylometry (lexical/syntactic/function-word/vocabulary-richness/POS là bộ chuẩn), Burrows' Delta (so z-score tần suất MFW; cùng tác giả → khoảng cách Delta nhỏ).

### 1.2 Cái nào TRANSFER sang việc bắt chước — chia 3 lớp

Nguyên tắc: **feature "nhận dạng tốt nhất" (function words, char n-grams) lại là feature KHÓ ra lệnh nhất** — không thể bảo model "dùng 'của' ở tần suất 2,3%". Chúng chỉ truyền được **ngầm qua ví dụ (in-context)**, và đo được để **validate**.

- **Lớp A — ra lệnh được (rule bank)**: nhịp câu (dài/ngắn xen kẽ, variance), punctuation habits, discourse markers ưa dùng, kiểu mở đầu câu/đoạn, cụm chữ ký, cách nêu ví dụ, cách cảnh báo, persona/stance, format habits (bảng, bold, song ngữ term-first). → Viết thành quy tắc tường minh.
- **Lớp B — chỉ truyền qua ví dụ (quote bank / few-shot)**: texture function words, char n-gram, cú pháp tinh vi, "hơi thở" tổng thể. Nghiên cứu gọi đây là *implicit style* — "subtle and implicit, making it difficult to specify through prompts" (Catch Me If You Can, EMNLP 2025 Findings). → Phải kèm văn mẫu nguyên bản.
- **Lớp C — chỉ dùng để VALIDATE, không nên bắt chước**: lỗi chính tả đặc trưng, quirk Unicode, thói quen xấu. → Đo để so, lọc khi sinh.

**Hệ quả thiết kế**: hồ sơ giọng bắt buộc là **hybrid = rule bank (lớp A) + quote bank (lớp B) + metric baseline (đo A+B+C để chấm điểm output)**.

---

## 2. Best practices few-shot style mimicry

### 2.1 Bao nhiêu sample là đủ?

- **2–5 sample đã kích hoạt được mimicry mạnh**; lợi ích giảm dần sau ~3–5 shot (PromptHub + tổng hợp research).
- Benchmark lớn nhất hiện có (Catch Me If You Can — 400+ tác giả thật, >40.000 generation/model, 4 domain): **5-shot > 0-shot nhất quán ở mọi model**, nhưng **tăng thêm demonstration KHÔNG giải quyết được style ngầm** — LLM bắt chước tốt format có cấu trúc (news, email), **vẫn trượt với giọng informal/ngầm (blog, forum)**. Tức: thêm sample có trần; phần thiếu phải bù bằng rule bank + vòng lặp sửa.
- Về phía distill (đọc để rút hồ sơ): càng nhiều càng tốt — 10k–30k+ từ để thống kê n-gram/nhịp câu ổn định (Delta cần văn bản đủ dài); nhưng phần **đính kèm vào prompt** chỉ cần 3–7 trích đoạn chọn lọc.

### 2.2 Chọn sample thế nào: cùng thể loại hay đa dạng?

Kết luận từ ICL research: 3 thứ quyết định là **input distribution, output space, và FORMAT của demonstration** — ~70% lợi ích của demo đến từ "format regulation" chứ không phải nội dung. Suy ra cho mimicry:

- **Register/thể loại: PHẢI TRÙNG với output đích.** Muốn viết study note → sample là study note, không phải email hay post mạng xã hội. (Catch Me If You Can cũng cho thấy khả năng imitate phụ thuộc mạnh vào domain.)
- **Chủ đề/nội dung: NÊN ĐA DẠNG** trong cùng register — để model học "cách viết" chứ không chép "cái được viết" (tránh content leakage; các style-embedding papers như StyleDistance/Wegmann-Nguyen đều nhấn mạnh phải tách style khỏi content).
- Chọn đoạn có **mật độ chữ ký cao nhưng sạch tic** (biên tập trích đoạn trước khi đưa vào quote bank — được phép sửa!).

### 2.3 Quote bank vs rule bank → HYBRID, và trick mạnh nhất: cặp pseudo-parallel

- **Rule bank đơn thuần** → pastiche chung chung ("viết thân thiện, dí dỏm" ai áp cũng ra giống nhau).
- **Quote bank đơn thuần** → bắt chước bề mặt + caricature (xem 2.5) + lẫn nội dung cũ.
- **STYLL (Patel, Andrews, Callison-Burch — baseline mạnh nhất cho low-resource authorship style transfer, thuần in-context, không train)** làm cả hai + một bước thứ ba:
  1. Sinh **style descriptors** từ văn mẫu (rule bank tự động);
  2. Tạo **cặp pseudo-parallel**: paraphrase trung tính hoá văn mẫu → đặt cạnh bản gốc. Cặp "bản phẳng → bản có giọng" **cô lập đúng phần style** và chỉ cho model thấy chính xác delta cần thêm;
  3. Few-shot với các cặp đó + text nguồn cần chuyển giọng.
- Practical guides (CyberArk, Towards AI, Nina Panickssery) hội tụ cùng công thức: (a) nhờ LLM mô tả style thật chi tiết, "chỉ nói về style, cấm nói về chủ đề" → đưa vào system prompt; (b) đính kèm sample; (c) một số guide thêm bước "neutralize" văn gốc thành flat text để làm cặp đối chiếu — chính là pseudo-parallel.

### 2.4 Negative examples có giúp không?

- **Lệnh cấm trần ("ĐỪNG viết X") yếu**: hiệu ứng "pink elephant" — negative instruction dễ bị bỏ qua hoặc phản tác dụng, model scale lên càng tệ; token generation là positive-selection nên lệnh dương tính (viết Y thay vì X) mạnh hơn.
- **Negative CÓ tác dụng khi**: (a) đi theo **cặp tương phản** bad→good (contrastive in-context learning có paper riêng); (b) số lượng ÍT, tuyệt đối, cho hard ban (kill-list tic); (c) mỗi lệnh cấm kèm ngay **replacement dương tính**.
- Format khuyến nghị đã được ngành content-design chuẩn hoá: **"this-but-not-that"** của Mailchimp ("We are smart **but not** academic") — mỗi trục giọng có cực dương và cực cấm dán liền nhau.

### 2.5 Rủi ro đặc thù: CARICATURE (máy tự sinh tic mới)

Nghiên cứu imitation văn học (GPT-4o, Digital Scholarship in the Humanities) cho thấy LLM bắt chước tốt lớp bề mặt nhưng lệch ở lớp sâu — và trong thực hành, model **khuếch đại các item nổi bật nhất**: cụm chữ ký xuất hiện 1 lần/2.000 từ trong văn gốc sẽ bị nhét vào mỗi đoạn. Chữ ký lạm phát = tic. (Đây đúng là bài học de-cringe 2027: humanizer skill tái sinh tic.) **Phòng ngừa: mọi chữ ký trong rule bank phải kèm NGÂN SÁCH TẦN SUẤT** ("≤1 lần/1.000 từ", "tối đa 2 lần/note") + validator đếm lại sau khi sinh.

---

## 3. Quy trình chuẩn hoá: N bài mẫu → HỒ SƠ GIỌNG

### Bước 0 — Corpus prep
Gom 10–30k+ từ **cùng register với output đích**; bỏ boilerplate (heading template, LOS list); tách đoạn.

### Bước 1 — Pass ĐỊNH LƯỢNG (máy đếm, không cần LLM)
- Nhịp: mean/σ độ dài câu, độ dài đoạn, tỉ lệ câu hỏi/câu cảm.
- Punctuation rates (phẩy, gạch ngang, ngoặc, hai chấm...).
- **N-gram 2–5 lặp bất thường** so với corpus nền → danh sách ứng viên "cụm lặp" (chưa phán là chữ ký hay tic).
- Function-word profile + lexical richness → **chỉ để làm baseline validate**, không đưa vào prompt.

### Bước 2 — Pass ĐỊNH TÍNH (LLM/người đọc)
Prompt kiểu CyberArk: "Mô tả cực kỳ chi tiết linguistic style, vocabulary, tone... **cấm nói về chủ đề bài viết**." Rút: persona/stance, moves tu từ (cách vào bài, cách nêu ví dụ, cách cảnh báo, cách chốt), miền ẩn dụ, kiểu hài, thói quen song ngữ/format.

### Bước 3 — TRIAGE mọi item lặp vào 3 rổ (checklist mục 4 dưới)
- **CHỮ KÝ** → giữ, kèm frequency budget.
- **TIC** → kill-list, kèm replacement dương tính.
- **TRUNG TÍNH** → bỏ, để model tự do.

### Bước 4 — Lắp HỒ SƠ GIỌNG (1 file, thứ tự ưu tiên)
1. **Identity paragraph** (3–5 câu: ai đang nói, với ai, thái độ gì).
2. **Rule bank**: 10–15 quy tắc DƯƠNG TÍNH lớp-A, mỗi rule 1 ví dụ minh hoạ 1 dòng.
3. **Bảng chữ ký**: cụm/move + khi nào dùng + **ngân sách tần suất**.
4. **Kill-list**: ≤10 hard ban, format this-but-not-that (cấm X → thay bằng Y).
5. **Quote bank**: 3–7 trích đoạn (register trùng, chủ đề đa dạng, ĐÃ BIÊN TẬP SẠCH TIC).
6. **2–3 cặp pseudo-parallel** (bản trung tính → bản có giọng) — trick STYLL, đáng giá nhất trên mỗi token.
7. **Metric baseline** (số liệu bước 1) — để validator dùng, KHÔNG nạp vào prompt sinh.

### Bước 5 — Nén cho vừa prompt budget; ưu tiên: cặp pseudo-parallel > kill-list > rule bank > quote bank dài.

---

## 4. CHỮ KÝ vs TIC — tiêu chí phân biệt

Nền tảng từ giới editing: tic = "words, phrases, or patterns you unconsciously repeat" — tương đương "um/like" khi nói; vô hình với tác giả, lồ lộ với độc giả; tai bắt lặp tốt hơn mắt. Nhưng "chỉ khi biết mình đang làm gì một cách vô thức, bạn mới dùng được tic — và voice — một cách CHỦ ĐÍCH" (Hughes): cùng một cụm có thể là tic ở tần suất này và là chữ ký ở tần suất khác. **Ranh giới là chủ đích + kiểm soát tần suất + giá trị cho người đọc**, không phải bản thân cụm từ.

Checklist 6 câu (điểm ≥4 = chữ ký; ≤2 = tic; giữa = trung tính, theo dõi thêm):
1. **Có mang nghĩa/chức năng không?** Bỏ đi bài có mất gì không? (Mất → chữ ký. Không mất → tic/filler.)
2. **Có chủ đích không?** Tác giả đọc lại có nhận ra và BẢO VỆ nó không? (Bảo vệ → chữ ký.)
3. **Tần suất có kiểm soát không?** Xuất hiện đúng ngữ cảnh hẹp (chỉ khi cảnh báo, chỉ khi chốt) hay rải vô tội vạ?
4. **Độc giả phản ứng thế nào ở lần gặp thứ 5?** Thấy "đúng chất" hay thấy ngán? (Ngán → tic.)
5. **Có thay được bằng từ khác mà không đổi giọng không?** (Thay được dễ dàng → trung tính/tic.)
6. **Ở văn người khác cùng thể loại có phổ biến không?** (Ai cũng viết vậy → trung tính, không phải chữ ký.)

---

## 5. VALIDATE hồ sơ giọng

### 5.1 Tự động (chạy mỗi lần sinh)
- **Authorship verification làm giám khảo**: chấm output bằng authorship-embedding/AV model (cách Catch-Me-If-You-Can và STYLL đo: attribution + verification + style matching + AI-detection thành ensemble). Bản thủ công tương đương: Delta distance giữa output và corpus gốc phải nhỏ hơn với corpus "giọng AI mặc định".
- **So metric baseline** (bước 1): phân bố độ dài câu, σ (burstiness — văn AI thường thiếu variance), punctuation rates trong dung sai ±.
- **Tic counter**: kill-list = 0 lần; mỗi chữ ký ≤ budget. (Tự động hoá bằng find/replace — đúng lời khuyên giới editing.)

### 5.2 Blind test người thật — thiết kế cho đúng
Bằng chứng nền: người đọc phân biệt AI/người **chỉ nhỉnh hơn ăn may** (57% với AI-text, 64% với human-text; chấm essay mù: không khác biệt điểm có ý nghĩa thống kê, nhận diện tác giả "marginally better than random"). Suy ra: hỏi kiểu yes/no 1 mẫu là vô nghĩa thống kê — phải **forced-choice, nhiều trial**:

1. **Lineup test (người lạ đã đọc văn gốc)**: đưa 3 đoạn — 2 thật 1 giả (hoặc ngược) — "đoạn nào KHÔNG phải tác giả viết?" ≥6 trials. Người chọn đúng ~1/3 (ngang ăn may) → mimicry ĐẠT.
2. **Owner test (chính chủ)**: tác giả tự đọc lineup. Chính chủ không tách được văn mình khỏi văn máy một cách tin cậy → đạt cấp cao nhất. Chính chủ tách được ngay → hỏi "nhờ dấu hiệu nào?" → dấu hiệu đó thành rule mới (vòng lặp).
3. **Annoyance test (bắt tic)**: cho người đọc 2–3 trang liền (không phải đoạn ngắn — tic chỉ lộ ở độ dài), gạch mọi chỗ "thấy lặp/thấy giả". Tai người là tic-detector tốt nhất.
4. **Recognition test (giọng có ĐẶC TRƯNG không, không chỉ "không giả")**: đưa output cho người quen văn tác giả, hỏi mở "ai viết?" hoặc chấm 1–5 "giống giọng X". Đạt "không phân biệt được" mà điểm recognition thấp → hồ sơ mới lọc được tic chứ chưa giữ được chữ ký → tăng cường bảng chữ ký.

Vòng lặp: fail dạng nào → sửa đúng khối đó (fail lineup → thêm cặp pseudo-parallel; fail annoyance → siết budget/kill-list; fail recognition → thêm chữ ký + move tu từ).

---

## SOURCES

Stylometry / AA features:
- Stylometry Analysis of Multi-authored Documents (arXiv 2401.06752) — taxonomy features: https://arxiv.org/html/2401.06752v1
- Stylometric Features for Multiple Authorship Attribution (Harvard DASH): https://dash.harvard.edu/bitstreams/134f7996-6b3b-4d93-a9cc-f45669ab351c/download
- Testing Burrows's Delta (Hoover; Cornell mirror): https://mimno.infosci.cornell.edu/info3350/readings/delta.pdf
- Improving Authorship Attribution: Optimizing Burrows' Delta (JQL): https://www.tandfonline.com/doi/abs/10.1080/09296174.2011.533591
- Boosting word frequencies in authorship attribution (arXiv 2211.01289): https://arxiv.org/pdf/2211.01289
- Authorship Attribution Using Stylometry and ML (ResearchGate): https://www.researchgate.net/publication/283862723_Authorship_Attribution_Using_Stylometry_and_Machine_Learning_Techniques

Few-shot mimicry / style transfer:
- Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate Implicit Writing Styles (EMNLP 2025 Findings): https://arxiv.org/abs/2509.14543 / https://aclanthology.org/2025.findings-emnlp.532.pdf
- Low-Resource Authorship Style Transfer (STYLL; Patel, Andrews, Callison-Burch): https://arxiv.org/abs/2212.08986
- How Well Do LLMs Imitate Human Writing Style? (arXiv 2509.24930): https://arxiv.org/pdf/2509.24930
- Using Prompts to Guide LLMs in Imitating a Real Person's Language Style (arXiv 2410.03848): https://arxiv.org/html/2410.03848v1
- TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings: https://arxiv.org/pdf/2406.15586
- Steering LLMs with Register Analysis for Arbitrary Style Transfer (arXiv 2505.00679): https://arxiv.org/pdf/2505.00679
- The Few Shot Prompting Guide (PromptHub): https://www.prompthub.us/blog/the-few-shot-prompting-guide
- A Guide to Mimicking and Blending Writing Styles with AI (CyberArk Engineering): https://medium.com/cyberark-engineering/a-guide-to-mimicking-and-blending-writing-styles-with-ai-ce541044c004
- How To Make LLMs Write Stylishly (Towards AI): https://pub.towardsai.net/how-to-make-llms-write-stylishly-6691be12b970
- How to make an LLM write like someone else (Nina Panickssery): https://blog.ninapanickssery.com/p/how-to-make-an-llm-write-like-someone
- Teach LLMs to mimic your style (Relevance AI): https://relevanceai.com/docs/example-use-cases/few-shot-prompting

Negative examples / contrastive:
- The Pink Elephant Problem: Why "Don't Do That" Fails with LLMs: https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis
- Why Positive Prompts Outperform Negative Ones (Gadlet): https://gadlet.com/posts/negative-prompting/
- Customizing LM Responses with Contrastive In-Context Learning (arXiv 2401.17390): https://arxiv.org/pdf/2401.17390

ICL demonstration selection / format:
- In-Context Learning with Iterative Demonstration Selection (arXiv 2310.09881): https://arxiv.org/abs/2310.09881
- Diverse Demonstrations Improve In-context Compositional Generalization (arXiv 2212.06800): https://arxiv.org/pdf/2212.06800
- In-Context Learning, In Context (The Gradient — input distribution/output space/format): https://thegradient.pub/in-context-learning-in-context/

Style measurement / content-independence:
- Does It Capture STEL? (Wegmann & Nguyen, EMNLP 2021): https://aclanthology.org/2021.emnlp-main.569/
- Same Author or Just Same Topic? Content-Independent Style Representations: https://aclanthology.org/2022.repl4nlp-1.26/
- StyleDistance: Stronger Content-Independent Style Embeddings (NAACL 2025): https://aclanthology.org/2025.naacl-long.436.pdf
- Learning Interpretable Style Embeddings via Prompting LLMs (LISA): https://arxiv.org/pdf/2305.12696

Signature vs tic (craft/editing):
- Voice, Tics, and Understanding (A. Hughes): https://ahugheswriter.com/voice-tics-and-understanding/
- How to Find and Fix Your Writing Tics (Deb Murphy): https://medium.com/@MurphyFreelance/how-to-find-and-fix-your-writing-tics-before-they-make-you-sound-amateur-da38cd927ec2
- How to cure 22 annoying and repetitive writing tics (Josh Bernoff): https://bernoff.com/blog/how-to-cure-22-annoying-and-repetitive-writing-tics
- Writing Tics: Definition, Examples (James Field): https://www.james-field.com/blog/writing-tics-definition-examples-and-how-to-spot-yours-before-they-drive-readers-mad
- Voice and Tone (Mailchimp Content Style Guide — "this but not that"): https://styleguide.mailchimp.com/voice-and-tone/
- 7 Steps for Establishing Voice and Tone Guidelines (Mailchimp): https://mailchimp.com/resources/establish-your-voice-and-tone/

Validation / human blind tests:
- Beyond the surface: stylometric analysis of GPT-4o's literary style imitation (DSH, Oxford): https://academic.oup.com/dsh/article/40/2/587/8118784
- Evaluating AI and human authorship quality in physics essays (IOPscience — blind marking, ID ~chance): https://iopscience.iop.org/article/10.1088/1361-6404/ad669d
- Do humans identify AI-generated text better than machines? (ScienceDirect — 57%/64%): https://www.sciencedirect.com/science/article/pii/S1477388025000131
- Everyone prefers human writers, including AI (arXiv 2510.08831 — attribution bias): https://arxiv.org/html/2510.08831v1
