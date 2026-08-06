# EIR Design Doctrine — Editorial Institutional Research

Distilled from the **FT Visual Vocabulary**, **Bloomberg Intelligence**, **Goldman /
sell-side equity research**, **Morningstar** briefs, and **The Economist** chart style
guide. This is the "why" behind every component in `viz_eir.py`. Read it before adding
or tuning a chart so the whole library keeps reading as one research house.

## The five rules (encode these, not decoration)

1. **Title states the finding, not the topic.** A chart headline is an active sentence
   that says the takeaway ("Chênh lệch 10 năm trừ 2 năm thu hẹp về gần 0"), and the
   subtitle carries the metric + units ("Lợi suất trái phiếu chính phủ, %"). This single
   convention does more for the institutional feel than any chart-type choice. It also
   forces one message per figure — if you need two headlines, make two charts.

2. **Colour = meaning, never decoration.** One ink for structure, one hue for
   up/positive, one for down/negative, one for target/neutral/annotation. Everything else
   is grey. Rainbow categorical palettes are used *only* when the categories themselves
   are the message (e.g. marimekko segments).

   | Role | Token | Hex | Used for |
   |---|---|---|---|
   | Ink / structure | `NAVY` | `#1F2D4D` | headlines, axes, the "hero" neutral series |
   | Up / positive | `TEAL` | `#2E6B5E` | gains, beats, positive active return (or subject accent) |
   | Down / negative | `BRICK` | `#B23A2E` | losses, misses, deficits |
   | Target / neutral / annotation | `GOLD` | `#C08A2E` | targets, reference lines, the one highlighted point |
   | Paper | `PAPER` | `#FFFEF8` | cream ground — dissolves into the note page |
   | Context / muted | `MUTED` `#6B6B6B`, `FAINT` `#9A9488`, `GRID` `#E8E5DE` | secondary text, connectors, hairline grid |

   The subject accent from the note (`theme.accent`) overrides `TEAL` as the hero/positive
   colour where a hero series exists; the signed roles (up/down/target) stay fixed so a
   reader always decodes green = good, red = bad, gold = the number to watch.

3. **Tabular (mono) numerals.** Data labels, KPI values, and table cells use a monospace
   with Vietnamese coverage (Noto Sans Mono) so columns and figures align like a terminal.
   Prose/labels use Lato; headlines use a serif (DejaVu Serif) for the editorial voice.

4. **Declutter, direct-label, honest axes.** No top/right spines; hairline gridlines on
   one axis only; bars start at zero; label series/points in place instead of a legend
   whenever ≤4 series; no 3D, no decorative dual axes, **no rounded cards / drop shadows**
   (those read as generic "AI slop", the opposite of institutional).

5. **Source + "as of" line, always.** Bottom-left, muted mono: `Nguồn: … · Số liệu tại …`.
   The single most recognisable Bloomberg/FT tell, and good scholarship for a study note.

## The editorial chrome (furniture)

Every single-panel component is built through `eir_fig(meta, …)`, which draws, top to
bottom: a thick navy top rule → kicker (accent small-caps) → serif headline → muted
subtitle → optional rating badge (top-right) → the plot → a thin rule → the source line.
Multi-panel components (`exec_dashboard`, `kpi_strip`, `cond_table`) call
`draw_masthead` + `draw_source` directly. Pass furniture via params:
`title, kicker, subtitle, source, asof, rating, firm`.

## Parsimony (inherited from note-pipeline-viz, unchanged)

More chart *types* does **not** mean more charts. The library widens the vocabulary so
that when data naturally fits a dumbbell or a fan, you have the right tool — not so every
module fills a quota. Keep the existing discipline: **each visual must teach one thing;
if you have to bend the data to fit the chart, stop.** 2–5 figures for theory modules (5–9 for calculation-heavy ones, per note-pipeline-viz v3) remains the
norm; a table rendered well as `[TABLE]` needs no chart. Conceptual/metaphor visuals still
go to AI-image hints, not here.

## Vietnamese font note (correctness)

DejaVu Sans Mono — matplotlib's default mono — **drops Vietnamese stacked diacritics**
(ế, ấ, ố → tofu boxes). `_eir_style.setup_fonts()` therefore resolves mono to **Noto Sans
Mono** (or Liberation Mono), verified by glyph coverage, and Lato for sans. Never hardcode
`family="monospace"`; always use the resolved `S.MONO`.
