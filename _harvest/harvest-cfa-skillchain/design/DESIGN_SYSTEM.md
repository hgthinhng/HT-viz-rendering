# Design System — Canonical Reference

(See PHASE2_DESIGN.md for full details. This is the at-a-glance reference.)

## Color Palette (functional roles)

| Role | Hex | Use |
|---|---|---|
| page_bg | `#FAFAF7` | Page background |
| body | `#1C1C1C` | Primary text |
| secondary | `#3B3B3B` | Definitions, descriptions |
| muted | `#6B6B6B` | Labels, captions, subtitles |
| indigo | `#2E3B7C` | Term emphasis, formula color |
| section_purple | `#2C3878` | Headings, titles |
| section_num_orange | `#B85A1C` | Section numbers only |
| gold | `#C49A1A` | Rules, borders, dividers |

## Box accent colors (left border + tinted bg)

| Box type | Accent | Background |
|---|---|---|
| BOX_KEY | `#8B6B20` (gold dark) | none (gold rules instead) |
| BOX_EXAMPLE | `#2D6A4F` (green) | `#E4F0E9` |
| BOX_WARN | `#A04030` (brick) | `#F7E9E6` |
| BOX_NOTE | `#2B5597` (steel blue) | `#E4ECF6` |
| BOX_PURPLE | `#6B3FA0` (rich purple) | none (annotation only) |

## Per-section accent gradient (Tầng G.1)

8 sections share a subtle gradient through indigo family:
1. `1E2862` (deepest)
2. `232D6E`
3. `283278`
4. `2C3878` (canonical)
5. `323D80`
6. `384388`
7. `3E4990`
8. `445098` (lightest)

## Subject accent colors (cover subject line)

See PHASE2_DESIGN.md for full table.

## Typography

| Element | Font | Size | Weight |
|---|---|---|---|
| Cover module name | Raleway | 22pt | Bold |
| Cover subject | Raleway | 17pt | Bold + letter-spacing 80 |
| Half-title | Raleway | 22pt | Italic + letter-spacing 20 |
| Section heading | Inter | 18pt | Bold |
| Subsection | Inter | 13pt | Bold |
| Body | Inter | 10pt | Regular |
| Margin | Inter | 8pt | Italic |
| Formula main | Consolas | 13pt | Bold |
| Formula legend | Consolas + Inter | 9pt | Mixed |
| Footnote | Inter | 7pt | Italic |

## Spacing (twips)

| Element | Before | After |
|---|---|---|
| Section heading | 240 | 40 |
| Subsection heading | 180 | 40 |
| Body paragraph | 50 | 50 |
| Box external | 120 | 120 |
| Box internal | 20 | 20 |
| Formula block | 120 | 60 |
| Table top spacer | 120 | 0 |

## Borders & rules

- Section heading bottom: 0.5pt purple (sz=4)
- Subsection left: 2pt gold (sz=16)
- Box left rule: 3pt accent color (sz=24)
- TABLE top/bottom: 1.5pt gold (sz=12)
- Pull-quote top/bottom: 0.75pt gold (sz=6)
- Formula gold rules: 0.5pt (sz=4)
- Hairline rules: 0.25pt (sz=2)

## Page

- Size: Letter 12240 × 15840
- Margins (print/both): top 1296, right 1080, bottom 1296, left 1440
- Margins (digital): symmetric 1296
- Header/footer distance: 600
- Header/footer suppressed on cover (titlePg flag)
- Line spacing: 1.25 (w:line=260)
