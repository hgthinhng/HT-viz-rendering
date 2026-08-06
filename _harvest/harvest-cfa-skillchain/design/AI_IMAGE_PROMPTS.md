# AI-IMAGE PROMPT LIBRARY — visual khái niệm "quá sức matplotlib"
*Theo policy NỚI NHẸ: khi 1 visual đáng có nhưng là scene/ẩn dụ/conceptual (kho khuôn matplotlib không vẽ được) → KHÔNG ép; dùng prompt FULL ENGLISH dưới đây, tự gen bằng AI-Image-Generator (DALL·E/Midjourney/...) rồi chèn vào `[FIGURE]`.*

**Style chung (giữ nhất quán với note):** thêm vào cuối mọi prompt →
`Editorial line-art illustration, restrained dark-navy ink (#14213D) on warm cream (#FAFAF7) background, subtle teal (#1C5D72) and antique-gold (#9A7B3F) accents, minimalist, clean vector, generous whitespace, no text labels, no watermark.`

---

## Fixed Income
- **macaulay_balance_beam** (FI_M11 · Macaulay duration) — *"A physical balance beam / seesaw on a fulcrum; small money-bag weights placed at increasing distances along the beam representing bond cash flows over time; the fulcrum sits at the balance point labeling 'duration'."*
- **bond_as_zeros** (FI_M01) — *"One coupon bond visually 'unzipping' into a row of separate small zero-coupon strips, each a discrete slip, showing decomposition into individual cash flows."*
- **liquidity_frozen_vs_flowing** (FI_M03) — *"Split scene: left side water flowing freely through an open pipe (liquid market), right side the same pipe frozen solid (illiquid market)."*

## Derivatives
- **zero_sum_seesaw** (DV_M01) — *"A perfectly balanced seesaw; one side rising with a plus symbol, the other sinking with a minus symbol, equal magnitude — long gain equals short loss."*
- **hedger_vs_speculator** (DV_M03) — *"Two contrasting figures side by side: one holding a large protective umbrella over assets (hedger), one rolling dice on a small chart (speculator)."*

## Portfolio Management
- **core_satellite** (PM_M03) — *"A large central planet labeled as the index 'core', with several smaller satellites orbiting it representing active 'satellite' positions."*
- **diversification_baskets** (PM_M01) — *"Eggs distributed across several different baskets versus all eggs in one basket; minimalist, conveying spreading of risk."*
- **risk_return_mountain** (PM_M02) — *"A climber ascending a mountain; higher altitude marked with higher reward flags but steeper, riskier terrain — illustrating the risk-return trade-off."*

## Economics
- **central_bank_traffic** (EC_M05) — *"A central bank building personified as a traffic controller operating a stop/go signal that regulates flowing streams of money and goods."*
- **invisible_hand** (EC_M01) — *"A faint translucent hand gently guiding many small independent market actors into an orderly equilibrium pattern."*

## Equity
- **economic_moat** (EQ_M06) — *"A castle on a hill surrounded by a wide protective moat, symbolizing a company's durable competitive advantage."*
- **mr_market** (EQ_M03) — *"A single personified figure with a swinging mood — one face euphoric, one fearful — offering wildly different price tags, representing market sentiment."*
- **circle_of_competence** (EQ_M05) — *"Concentric circles; an investor standing confidently inside the small inner circle (what they truly understand) versus the vast unknown outside."*

## FSA
- **earnings_iceberg** (FSA_M10) — *"An iceberg: small reported earnings visible above the waterline, a much larger mass of accruals/quality issues hidden below — earnings quality."*
- **three_gears_statements** (FSA_M04) — *"Three interlocking gears labeled by shape as income statement, balance sheet, and cash-flow statement, turning together to show their linkage."*

## Alternative Investment
- **pe_distribution_waterfall** (AI_M02) — *"A literal multi-tier water cascade where water flows down tiers in sequence (return of capital → preferred return → catch-up → carry split), illustrating a PE distribution waterfall."*

## Quants
- **compounding_snowball** (QM_M02) — *"A small snowball rolling downhill growing exponentially larger, illustrating compound growth of money over time."*
- **fat_tail_black_swan** (QM_M03) — *"A single black swan gliding among many white swans, beside a bell curve whose tails are visibly thickened — rare extreme events / fat tails."*

## Ethics
- **profession_pillars** (ETH_M01) — *"A classical temple supported by sturdy pillars, each pillar embodying a professional virtue (integrity, competence, diligence), conveying the foundation of the profession."*
- **chinese_wall** (ETH_M02) — *"A solid wall cleanly separating two office departments, preventing information flow between them — information barrier."*

---
**Cách dùng trong pipeline:** humanizer/qc nhận diện visual conceptual → chèn `[BOX_NOTE]` ghi "🎨 AI-IMAGE: {tên} — prompt: {FULL ENGLISH + style chung}". User gen ảnh, lưu vào `figures/`, đổi sang `[FIGURE: figures/{tên}.png | caption]`.
