"""
Opvia Deep Analysis - 9 Cover Variants
Each cover: full A4 page, page-break-after: always.

Usage:
    from covers import cover_styles, cover_macro_hero, cover_quick_take, ...

    css = build_css(...) + viz_styles() + cover_styles()
    cover_html = cover_macro_hero(eyebrow=..., title=..., ...)
    body = cover_html + main_content + ...
"""
from __future__ import annotations
from html import escape


def cover_styles() -> str:
    """Shared CSS cho all 9 cover variants."""
    return r"""
/* ============ COVER SHARED STYLES ============ */
.cover-v {
  height: 297mm; width: 100%;
  padding: 24mm 24mm 18mm 24mm;
  page-break-after: always;
  position: relative;
  display: flex; flex-direction: column;
}

/* ---------- COVER 1: MACRO HERO (current default, kept for reference) ---------- */
/* Existing .cover-deep handles this - reuse it */

/* ---------- COVER 2: QUICK TAKE ---------- */
.cover-quick-take {
  background: #FAF7F0; color: #003153;
}
.cover-quick-take .qt-header {
  display: flex; justify-content: space-between;
  align-items: baseline; padding-bottom: 6mm;
  border-bottom: 0.5px solid rgba(74,111,165,0.2);
  margin-bottom: 18mm;
}
.cover-quick-take .qt-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 9pt; font-weight: 700;
  letter-spacing: 0.18em; color: #003153;
}
.cover-quick-take .qt-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: #6B6760;
}
.cover-quick-take .qt-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 6mm;
}
.cover-quick-take h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 30pt;
  line-height: 1.1; letter-spacing: -0.005em;
  color: #003153; margin-bottom: 6mm;
  max-width: 150mm;
}
.cover-quick-take .qt-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; font-size: 12pt;
  line-height: 1.55; color: #4A6FA5;
  font-style: italic; margin-bottom: 14mm;
  max-width: 140mm;
  border-left: 2px solid #B5A642;
  padding-left: 6mm;
}
.cover-quick-take .qt-takeaway {
  background: #003153; color: #FAF7F0;
  padding: 8mm 9mm;
  margin-bottom: 12mm;
}
.cover-quick-take .qt-takeaway-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
  margin-bottom: 3mm;
}
.cover-quick-take .qt-takeaway-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 13pt; font-weight: 500;
  line-height: 1.4;
}
.cover-quick-take .qt-footer {
  margin-top: auto;
  display: flex; gap: 14mm;
  padding-top: 6mm;
  border-top: 0.5px solid rgba(74,111,165,0.2);
}
.cover-quick-take .qt-footer-item {
  font-family: 'Inter', 'InterVN', sans-serif;
}
.cover-quick-take .qt-footer-label {
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; color: #B5A642;
  margin-bottom: 1mm; text-transform: uppercase;
}
.cover-quick-take .qt-footer-value {
  font-size: 9pt; font-weight: 600; color: #003153;
}

/* ---------- COVER 3: SECTOR BRIEF ---------- */
.cover-sector-brief {
  background: #FAF7F0; color: #003153;
}
.cover-sector-brief .sb-header {
  display: flex; justify-content: space-between;
  padding-bottom: 6mm;
  border-bottom: 1px solid #003153;
  margin-bottom: 14mm;
}
.cover-sector-brief .sb-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #003153;
}
.cover-sector-brief .sb-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: #6B6760;
}
.cover-sector-brief .sb-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 5mm;
}
.cover-sector-brief h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 28pt;
  line-height: 1.1;
  color: #003153; margin-bottom: 8mm;
  max-width: 140mm;
}
.cover-sector-brief .sb-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; font-size: 11pt;
  font-style: italic; color: #4A6FA5;
  line-height: 1.55; margin-bottom: 12mm;
  max-width: 145mm;
}
.cover-sector-brief .sb-entities-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 4mm;
  padding-bottom: 2mm;
  border-bottom: 0.5px solid rgba(181,166,66,0.4);
}
.cover-sector-brief .sb-entity {
  display: grid; grid-template-columns: 24mm 1fr 18mm;
  gap: 6mm; padding: 4mm 0;
  border-bottom: 0.4px solid rgba(74,111,165,0.18);
  align-items: baseline;
}
.cover-sector-brief .sb-entity-ticker {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 11pt; font-weight: 700;
  color: #003153;
}
.cover-sector-brief .sb-entity-take {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10pt; font-weight: 450;
  line-height: 1.4; color: #2B2B2B;
}
.cover-sector-brief .sb-entity-direction {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  text-align: right;
  letter-spacing: 0.06em;
}
.cover-sector-brief .sb-entity-direction.up { color: #2E7D52; }
.cover-sector-brief .sb-entity-direction.down { color: #C0392B; }
.cover-sector-brief .sb-entity-direction.neutral { color: #6B6760; }

/* ---------- COVER 4: POLICY WATCH ---------- */
.cover-policy-watch {
  background: #000d18; color: #FAF7F0;
}
.cover-policy-watch .pw-header {
  display: flex; justify-content: space-between;
  align-items: baseline;
  padding-bottom: 4mm;
  border-bottom: 1px solid rgba(181,166,66,0.4);
  margin-bottom: 14mm;
}
.cover-policy-watch .pw-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
}
.cover-policy-watch .pw-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: rgba(250,247,240,0.6);
}
.cover-policy-watch .pw-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 5mm;
}
.cover-policy-watch h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 32pt;
  line-height: 1.05;
  color: #FAF7F0; margin-bottom: 6mm;
  max-width: 145mm;
}
.cover-policy-watch .pw-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; font-size: 11pt;
  font-style: italic; color: rgba(250,247,240,0.85);
  line-height: 1.55; margin-bottom: 12mm;
  max-width: 145mm;
  padding-left: 6mm;
  border-left: 2px solid #B5A642;
}
.cover-policy-watch .pw-timeline-title {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; color: #B5A642;
  margin-bottom: 6mm; text-transform: uppercase;
}
.cover-policy-watch .pw-timeline {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 4mm;
  margin-bottom: 8mm;
}
.cover-policy-watch .pw-event {
  padding: 4mm;
  background: rgba(74,111,165,0.18);
  border-top: 2px solid #B5A642;
}
.cover-policy-watch .pw-event.current {
  border-top-color: #C0392B;
  background: rgba(192,57,43,0.15);
}
.cover-policy-watch .pw-event-date {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; font-weight: 700;
  color: #B5A642; margin-bottom: 2mm;
}
.cover-policy-watch .pw-event-name {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8.5pt; font-weight: 600;
  color: #FAF7F0;
  line-height: 1.35;
}
.cover-policy-watch .pw-scenarios {
  margin-top: auto;
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 5mm;
  padding-top: 6mm;
  border-top: 0.5px solid rgba(181,166,66,0.3);
}
.cover-policy-watch .pw-scenario {
  text-align: center;
}
.cover-policy-watch .pw-scenario-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; color: rgba(250,247,240,0.7);
  margin-bottom: 1mm; text-transform: uppercase;
}
.cover-policy-watch .pw-scenario-prob {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 22pt; font-weight: 700;
  color: #B5A642; line-height: 1;
}
.cover-policy-watch .pw-scenario-name {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 9pt; font-weight: 500;
  font-style: italic;
  color: rgba(250,247,240,0.85);
  margin-top: 1mm;
}

/* ---------- COVER 5: EARNINGS BRIEF ---------- */
.cover-earnings {
  background: #FAF7F0; color: #003153;
}
.cover-earnings .eb-header {
  display: flex; justify-content: space-between;
  padding-bottom: 4mm;
  border-bottom: 1px solid #003153;
  margin-bottom: 12mm;
}
.cover-earnings .eb-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #003153;
}
.cover-earnings .eb-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: #6B6760;
}
.cover-earnings .eb-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 4mm;
}
.cover-earnings .eb-ticker-row {
  display: flex; align-items: baseline; gap: 5mm;
  margin-bottom: 4mm;
}
.cover-earnings .eb-ticker {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 30pt; font-weight: 700;
  color: #003153; line-height: 1;
}
.cover-earnings .eb-period {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 14pt; font-weight: 500;
  font-style: italic; color: #4A6FA5;
}
.cover-earnings h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 600; font-size: 22pt;
  line-height: 1.15; color: #003153;
  margin-bottom: 4mm; max-width: 140mm;
}
.cover-earnings .eb-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; font-size: 10.5pt;
  font-style: italic; color: #4A6FA5;
  line-height: 1.5; margin-bottom: 10mm;
  max-width: 140mm;
}
.cover-earnings .eb-metrics {
  display: grid; grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 4mm; margin-bottom: 8mm;
}
.cover-earnings .eb-metric {
  background: #FFFFFF;
  padding: 5mm;
  border-top: 3px solid #B5A642;
}
.cover-earnings .eb-metric-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: #6B6760; margin-bottom: 2mm;
}
.cover-earnings .eb-metric-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 18pt; font-weight: 700;
  color: #003153; line-height: 1;
  margin-bottom: 1mm;
}
.cover-earnings .eb-metric-delta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; font-weight: 700;
}
.cover-earnings .eb-metric-delta.up { color: #2E7D52; }
.cover-earnings .eb-metric-delta.down { color: #C0392B; }
.cover-earnings .eb-metric-delta.flat { color: #6B6760; }
.cover-earnings .eb-takeaway {
  margin-top: auto;
  padding: 6mm 7mm;
  background: #003153;
  color: #FAF7F0;
}
.cover-earnings .eb-takeaway-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
  margin-bottom: 2mm; text-transform: uppercase;
}
.cover-earnings .eb-takeaway-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 500;
  font-style: italic; line-height: 1.5;
}

/* ---------- COVER 6: THEMATIC MACRO ---------- */
.cover-thematic {
  background: #FAF7F0; color: #003153;
}
.cover-thematic .tm-header {
  display: flex; justify-content: space-between;
  padding-bottom: 4mm;
  border-bottom: 0.5px solid rgba(74,111,165,0.3);
  margin-bottom: 12mm;
}
.cover-thematic .tm-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #003153;
}
.cover-thematic .tm-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: #6B6760;
}
.cover-thematic .tm-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 4mm;
}
.cover-thematic h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 30pt;
  line-height: 1.1; letter-spacing: -0.005em;
  color: #003153; margin-bottom: 6mm;
  max-width: 145mm;
}
.cover-thematic .tm-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; font-size: 11.5pt;
  font-style: italic; color: #4A6FA5;
  line-height: 1.55; margin-bottom: 8mm;
  max-width: 145mm;
}
.cover-thematic .tm-chart-wrap {
  background: #003153;
  padding: 8mm 6mm 6mm 6mm;
  margin-bottom: 8mm;
}
.cover-thematic .tm-chart-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; color: #B5A642;
  margin-bottom: 4mm; text-transform: uppercase;
}
.cover-thematic .tm-chart-svg {
  display: block; width: 100%; height: auto;
}
.cover-thematic .tm-chart-caption {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 7.5pt; color: rgba(250,247,240,0.7);
  margin-top: 3mm;
  display: flex; justify-content: space-between;
}
.cover-thematic .tm-stats {
  margin-top: auto;
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 5mm;
  padding-top: 5mm;
  border-top: 0.5px solid rgba(74,111,165,0.2);
}
.cover-thematic .tm-stat {
  text-align: center;
}
.cover-thematic .tm-stat-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 18pt; font-weight: 700;
  color: #003153; line-height: 1;
  margin-bottom: 1mm;
}
.cover-thematic .tm-stat-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: #6B6760;
}

/* ---------- COVER 7: ALERT/FLASH ---------- */
.cover-alert {
  background: #FAF7F0; color: #003153;
}
.cover-alert .al-banner {
  background: #C0392B; color: #FAF7F0;
  margin: -24mm -24mm 12mm -24mm;
  padding: 8mm 24mm;
  display: flex; justify-content: space-between;
  align-items: center;
}
.cover-alert .al-banner-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 11pt; font-weight: 700;
  letter-spacing: 0.32em;
}
.cover-alert .al-banner-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 600;
}
.cover-alert .al-eyebrow {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: #C0392B; margin-bottom: 5mm;
}
.cover-alert h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 32pt;
  line-height: 1.05; color: #003153;
  margin-bottom: 8mm; max-width: 145mm;
}
.cover-alert .al-stat {
  display: flex; align-items: baseline; gap: 6mm;
  padding: 6mm 0;
  border-top: 2px solid #C0392B;
  border-bottom: 2px solid #C0392B;
  margin-bottom: 12mm;
}
.cover-alert .al-stat-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 50pt; font-weight: 700;
  color: #C0392B; line-height: 1;
  letter-spacing: -0.02em;
}
.cover-alert .al-stat-label {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 500;
  font-style: italic; color: #003153;
  line-height: 1.45; max-width: 80mm;
}
.cover-alert .al-summary-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
  margin-bottom: 3mm; text-transform: uppercase;
}
.cover-alert .al-summary {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 450;
  line-height: 1.55; color: #2B2B2B;
  margin-bottom: 8mm;
}
.cover-alert .al-actions {
  margin-top: auto;
  padding: 5mm 6mm;
  background: #003153; color: #FAF7F0;
  border-left: 4px solid #C0392B;
}
.cover-alert .al-actions-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7.5pt; font-weight: 700;
  letter-spacing: 0.16em; color: #B5A642;
  margin-bottom: 2mm; text-transform: uppercase;
}
.cover-alert .al-actions-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 10pt; font-weight: 500;
  line-height: 1.5;
}

/* ---------- COVER 8: YEAR-END REVIEW ---------- */
.cover-yearend {
  background: #000d18; color: #FAF7F0;
}
.cover-yearend .ye-header {
  display: flex; justify-content: space-between;
  padding-bottom: 4mm;
  border-bottom: 1px solid #B5A642;
  margin-bottom: 12mm;
}
.cover-yearend .ye-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
}
.cover-yearend .ye-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: rgba(250,247,240,0.6);
}
.cover-yearend .ye-year {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 700; font-size: 96pt;
  line-height: 1; letter-spacing: -0.04em;
  color: #B5A642; margin-bottom: 2mm;
}
.cover-yearend h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 600; font-size: 22pt;
  line-height: 1.15; color: #FAF7F0;
  margin-bottom: 6mm; max-width: 140mm;
}
.cover-yearend .ye-dek {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 500; font-size: 11pt;
  font-style: italic; color: rgba(250,247,240,0.82);
  line-height: 1.55; margin-bottom: 10mm;
  max-width: 140mm;
}
.cover-yearend .ye-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 4mm; margin-bottom: 8mm;
}
.cover-yearend .ye-stat {
  background: rgba(74,111,165,0.2);
  padding: 5mm 6mm;
  border-top: 2px solid #B5A642;
}
.cover-yearend .ye-stat-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: #B5A642; margin-bottom: 2mm;
}
.cover-yearend .ye-stat-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 16pt; font-weight: 700;
  color: #FAF7F0; line-height: 1;
  margin-bottom: 1mm;
}
.cover-yearend .ye-stat-context {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 8pt; font-weight: 450;
  font-style: italic; color: rgba(250,247,240,0.7);
  line-height: 1.4;
}
.cover-yearend .ye-themes {
  margin-top: auto;
}
.cover-yearend .ye-themes-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
  margin-bottom: 4mm; text-transform: uppercase;
  padding-bottom: 2mm;
  border-bottom: 0.5px solid rgba(181,166,66,0.4);
}
.cover-yearend .ye-theme {
  display: grid; grid-template-columns: 14mm 1fr;
  gap: 4mm; padding: 2mm 0;
  font-size: 9pt;
}
.cover-yearend .ye-theme-num {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 700; color: #B5A642;
}
.cover-yearend .ye-theme-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; line-height: 1.5;
  color: rgba(250,247,240,0.92);
}

/* ---------- COVER 9: PITCH DECK ---------- */
.cover-pitch {
  background: #FAF7F0; color: #003153;
}
.cover-pitch .pd-header {
  display: flex; justify-content: space-between;
  padding-bottom: 4mm;
  border-bottom: 1px solid #003153;
  margin-bottom: 14mm;
}
.cover-pitch .pd-brand {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 10pt; font-weight: 700;
  letter-spacing: 0.18em; color: #003153;
}
.cover-pitch .pd-meta {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 8pt; color: #6B6760;
}
.cover-pitch .pd-recommendation {
  display: grid; grid-template-columns: 50mm 1fr;
  gap: 8mm; margin-bottom: 10mm;
  padding: 6mm; background: #FFFFFF;
  border-left: 6px solid;
}
.cover-pitch .pd-recommendation.buy { border-left-color: #2E7D52; }
.cover-pitch .pd-recommendation.sell { border-left-color: #C0392B; }
.cover-pitch .pd-recommendation.hold { border-left-color: #B5A642; }
.cover-pitch .pd-rec-action {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 24pt; font-weight: 700;
  letter-spacing: 0.06em;
  text-align: center;
}
.cover-pitch .pd-recommendation.buy .pd-rec-action { color: #2E7D52; }
.cover-pitch .pd-recommendation.sell .pd-rec-action { color: #C0392B; }
.cover-pitch .pd-recommendation.hold .pd-rec-action { color: #B5A642; }
.cover-pitch .pd-rec-target {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 14pt; font-weight: 700;
  color: #003153; text-align: center;
  margin-top: 1mm;
}
.cover-pitch .pd-rec-upside {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 600;
  text-align: center; color: #6B6760;
  margin-top: 1mm;
}
.cover-pitch .pd-rec-thesis {
  font-family: 'PFD', 'PFDVN', serif;
  font-size: 11pt; font-weight: 500;
  font-style: italic; line-height: 1.5;
  color: #003153;
}
.cover-pitch h1 {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 600; font-size: 22pt;
  line-height: 1.15; color: #003153;
  margin-bottom: 8mm; max-width: 145mm;
}
.cover-pitch .pd-thesis-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 8pt; font-weight: 700;
  letter-spacing: 0.18em; color: #B5A642;
  margin-bottom: 4mm; text-transform: uppercase;
}
.cover-pitch .pd-bullet {
  display: grid; grid-template-columns: 5mm 1fr;
  gap: 3mm; padding: 3mm 0;
  font-size: 10pt;
  border-bottom: 0.4px solid rgba(74,111,165,0.15);
}
.cover-pitch .pd-bullet-mark {
  font-family: 'JBM', 'JBMVN', monospace;
  font-weight: 700; color: #B5A642;
}
.cover-pitch .pd-bullet-text {
  font-family: 'PFD', 'PFDVN', serif;
  font-weight: 450; line-height: 1.5;
  color: #2B2B2B;
}
.cover-pitch .pd-footer {
  margin-top: auto;
  padding-top: 5mm;
  border-top: 0.5px solid rgba(74,111,165,0.2);
  display: flex; justify-content: space-between;
}
.cover-pitch .pd-footer-item .pd-footer-label {
  font-family: 'Inter', 'InterVN', sans-serif;
  font-size: 7pt; font-weight: 700;
  letter-spacing: 0.14em; color: #B5A642;
  text-transform: uppercase; margin-bottom: 1mm;
}
.cover-pitch .pd-footer-item .pd-footer-value {
  font-family: 'JBM', 'JBMVN', monospace;
  font-size: 9pt; font-weight: 600; color: #003153;
}
"""


# ============================================================
# COVER 1: Macro Hero (alias - existing cover-deep)
# ============================================================
# Skip - sử dụng existing .cover-deep CSS class trong render.py


# ============================================================
# COVER 2: Quick Take
# ============================================================
def cover_quick_take(
    eyebrow: str,
    title: str,
    dek: str,
    takeaway: str,
    issue: str = "",
    date: str = "",
    reading_time: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """Minimal 1-page memo cover. <1500 từ analysis behind."""
    return f"""
<div class="cover-v cover-quick-take">
  <div class="qt-header">
    <div class="qt-brand">{escape(author)}</div>
    <div class="qt-meta">{escape(issue)}</div>
  </div>
  <div class="qt-eyebrow">QUICK TAKE</div>
  <h1>{escape(title)}</h1>
  <div class="qt-dek">{escape(dek)}</div>
  <div class="qt-takeaway">
    <div class="qt-takeaway-label">Điểm chính</div>
    <div class="qt-takeaway-text">{escape(takeaway)}</div>
  </div>
  <div class="qt-footer">
    <div class="qt-footer-item">
      <div class="qt-footer-label">Phát hành</div>
      <div class="qt-footer-value">{escape(date)}</div>
    </div>
    <div class="qt-footer-item">
      <div class="qt-footer-label">Đọc trong</div>
      <div class="qt-footer-value">{escape(reading_time)}</div>
    </div>
    <div class="qt-footer-item">
      <div class="qt-footer-label">Eyebrow</div>
      <div class="qt-footer-value">{escape(eyebrow)}</div>
    </div>
  </div>
</div>
"""


# ============================================================
# COVER 3: Sector Brief
# ============================================================
def cover_sector_brief(
    eyebrow: str,
    title: str,
    dek: str,
    entities: list[dict],
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Multi-entity overview cover.

    entities: list of {
        "ticker": str,
        "take": str,             # 1-line opinion
        "direction": "up" | "down" | "neutral",
    }
    """
    direction_arrows = {"up": "↑ HƯỞNG LỢI", "down": "↓ CHỊU THIỆT", "neutral": "─ TRUNG TÍNH"}

    rows = []
    for e in entities:
        d = e.get("direction", "neutral")
        rows.append(f"""
        <div class="sb-entity">
          <div class="sb-entity-ticker">{escape(e.get("ticker", ""))}</div>
          <div class="sb-entity-take">{escape(e.get("take", ""))}</div>
          <div class="sb-entity-direction {d}">{direction_arrows.get(d, "─")}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-sector-brief">
  <div class="sb-header">
    <div class="sb-brand">{escape(author)}</div>
    <div class="sb-meta">{escape(issue)}</div>
  </div>
  <div class="sb-eyebrow">{escape(eyebrow)}</div>
  <h1>{escape(title)}</h1>
  <div class="sb-dek">{escape(dek)}</div>
  <div class="sb-entities-label">Đánh giá theo từng đơn vị</div>
  {''.join(rows)}
</div>
"""


# ============================================================
# COVER 4: Policy Watch
# ============================================================
def cover_policy_watch(
    eyebrow: str,
    title: str,
    dek: str,
    timeline: list[dict],
    scenarios: list[dict],
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Policy timeline + scenarios.

    timeline: list of {"date": str, "name": str, "current": bool (optional)}
    scenarios: list of {"label": str, "probability": str, "name": str}
    """
    timeline_html = []
    for ev in timeline:
        cls = "current" if ev.get("current") else ""
        timeline_html.append(f"""
        <div class="pw-event {cls}">
          <div class="pw-event-date">{escape(ev.get("date", ""))}</div>
          <div class="pw-event-name">{escape(ev.get("name", ""))}</div>
        </div>
        """)

    scenarios_html = []
    for sc in scenarios:
        scenarios_html.append(f"""
        <div class="pw-scenario">
          <div class="pw-scenario-label">{escape(sc.get("label", ""))}</div>
          <div class="pw-scenario-prob">{escape(sc.get("probability", ""))}</div>
          <div class="pw-scenario-name">{escape(sc.get("name", ""))}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-policy-watch">
  <div class="pw-header">
    <div class="pw-brand">{escape(author)}</div>
    <div class="pw-meta">{escape(issue)}</div>
  </div>
  <div class="pw-eyebrow">{escape(eyebrow)}</div>
  <h1>{escape(title)}</h1>
  <div class="pw-dek">{escape(dek)}</div>
  <div class="pw-timeline-title">Lịch trình dự kiến</div>
  <div class="pw-timeline">
    {''.join(timeline_html)}
  </div>
  <div class="pw-scenarios">
    {''.join(scenarios_html)}
  </div>
</div>
"""


# ============================================================
# COVER 5: Earnings Brief
# ============================================================
def cover_earnings_brief(
    ticker: str,
    period: str,
    title: str,
    dek: str,
    metrics: list[dict],
    takeaway: str,
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Earnings results cover - 4 metrics grid.

    metrics: list of 4 dicts (EPS, Rev, Margin, ROE typical):
        {"label": str, "value": str, "delta": str, "delta_type": "up"|"down"|"flat"}
    """
    metrics_html = []
    for m in metrics:
        dtype = m.get("delta_type", "flat")
        arrow = "↑" if dtype == "up" else ("↓" if dtype == "down" else "─")
        metrics_html.append(f"""
        <div class="eb-metric">
          <div class="eb-metric-label">{escape(m.get("label", ""))}</div>
          <div class="eb-metric-value">{escape(m.get("value", ""))}</div>
          <div class="eb-metric-delta {dtype}">{arrow} {escape(m.get("delta", ""))}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-earnings">
  <div class="eb-header">
    <div class="eb-brand">{escape(author)}</div>
    <div class="eb-meta">{escape(issue)}</div>
  </div>
  <div class="eb-eyebrow">EARNINGS BRIEF</div>
  <div class="eb-ticker-row">
    <div class="eb-ticker">{escape(ticker)}</div>
    <div class="eb-period">{escape(period)}</div>
  </div>
  <h1>{escape(title)}</h1>
  <div class="eb-dek">{escape(dek)}</div>
  <div class="eb-metrics">
    {''.join(metrics_html)}
  </div>
  <div class="eb-takeaway">
    <div class="eb-takeaway-label">Điểm then chốt</div>
    <div class="eb-takeaway-text">{escape(takeaway)}</div>
  </div>
</div>
"""


# ============================================================
# COVER 6: Thematic Macro
# ============================================================
def cover_thematic_macro(
    eyebrow: str,
    title: str,
    dek: str,
    chart_label: str,
    chart_data: list[float],
    chart_caption_left: str,
    chart_caption_right: str,
    stats: list[dict],
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Macro theme cover with mini line chart preview.

    chart_data: list of values for line chart preview (~12-24 points)
    stats: list of {"value": str, "label": str}
    """
    # Build line chart SVG
    if not chart_data or len(chart_data) < 2:
        chart_svg = ""
    else:
        v_min = min(chart_data)
        v_max = max(chart_data)
        v_range = v_max - v_min if v_max != v_min else 1
        n = len(chart_data)
        svg_w = 600
        svg_h = 100
        pad = 6
        cw = svg_w - 2 * pad
        ch = svg_h - 2 * pad

        points = []
        for i, v in enumerate(chart_data):
            x = pad + (i / (n - 1)) * cw
            y = pad + ch - ((v - v_min) / v_range) * ch
            points.append((x, y))

        path_d = f"M {points[0][0]:.1f} {points[0][1]:.1f}"
        for x, y in points[1:]:
            path_d += f" L {x:.1f} {y:.1f}"

        # Area fill
        area_d = path_d + f" L {points[-1][0]:.1f} {pad + ch} L {points[0][0]:.1f} {pad + ch} Z"

        chart_svg = f"""
        <svg class="tm-chart-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
          <path d="{area_d}" fill="#B5A642" fill-opacity="0.18"/>
          <path d="{path_d}" fill="none" stroke="#B5A642" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """

    stats_html = []
    for s in stats:
        stats_html.append(f"""
        <div class="tm-stat">
          <div class="tm-stat-value">{escape(s.get("value", ""))}</div>
          <div class="tm-stat-label">{escape(s.get("label", ""))}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-thematic">
  <div class="tm-header">
    <div class="tm-brand">{escape(author)}</div>
    <div class="tm-meta">{escape(issue)}</div>
  </div>
  <div class="tm-eyebrow">{escape(eyebrow)}</div>
  <h1>{escape(title)}</h1>
  <div class="tm-dek">{escape(dek)}</div>
  <div class="tm-chart-wrap">
    <div class="tm-chart-label">{escape(chart_label)}</div>
    {chart_svg}
    <div class="tm-chart-caption">
      <span>{escape(chart_caption_left)}</span>
      <span>{escape(chart_caption_right)}</span>
    </div>
  </div>
  <div class="tm-stats">
    {''.join(stats_html)}
  </div>
</div>
"""


# ============================================================
# COVER 7: Alert/Flash
# ============================================================
def cover_alert(
    title: str,
    stat_value: str,
    stat_label: str,
    summary: str,
    actions: str,
    eyebrow: str = "ALERT",
    timestamp: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """Quick alert cover - red banner + signature stat."""
    return f"""
<div class="cover-v cover-alert">
  <div class="al-banner">
    <div class="al-banner-label">CẢNH BÁO · FLASH</div>
    <div class="al-banner-meta">{escape(timestamp)}</div>
  </div>
  <div class="al-eyebrow">{escape(eyebrow)}</div>
  <h1>{escape(title)}</h1>
  <div class="al-stat">
    <div class="al-stat-value">{escape(stat_value)}</div>
    <div class="al-stat-label">{escape(stat_label)}</div>
  </div>
  <div class="al-summary-label">Tóm tắt</div>
  <div class="al-summary">{escape(summary)}</div>
  <div class="al-actions">
    <div class="al-actions-label">Hành động đề xuất</div>
    <div class="al-actions-text">{escape(actions)}</div>
  </div>
</div>
"""


# ============================================================
# COVER 8: Year-end Review
# ============================================================
def cover_yearend_review(
    year: str,
    title: str,
    dek: str,
    stats: list[dict],
    themes: list[str],
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Year-end infographic cover.

    stats: list of 3-6 dicts {"label": str, "value": str, "context": str}
    themes: list of top themes (3-5 strings)
    """
    stats_html = []
    for s in stats:
        stats_html.append(f"""
        <div class="ye-stat">
          <div class="ye-stat-label">{escape(s.get("label", ""))}</div>
          <div class="ye-stat-value">{escape(s.get("value", ""))}</div>
          <div class="ye-stat-context">{escape(s.get("context", ""))}</div>
        </div>
        """)

    themes_html = []
    for i, theme in enumerate(themes, 1):
        themes_html.append(f"""
        <div class="ye-theme">
          <div class="ye-theme-num">{i:02d}</div>
          <div class="ye-theme-text">{escape(theme)}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-yearend">
  <div class="ye-header">
    <div class="ye-brand">{escape(author)}</div>
    <div class="ye-meta">{escape(issue)}</div>
  </div>
  <div class="ye-year">{escape(year)}</div>
  <h1>{escape(title)}</h1>
  <div class="ye-dek">{escape(dek)}</div>
  <div class="ye-grid">
    {''.join(stats_html)}
  </div>
  <div class="ye-themes">
    <div class="ye-themes-label">Chủ đề chính trong năm</div>
    {''.join(themes_html)}
  </div>
</div>
"""


# ============================================================
# COVER 9: Pitch Deck
# ============================================================
def cover_pitch_deck(
    ticker: str,
    title: str,
    recommendation: str,  # "BUY" | "SELL" | "HOLD"
    target_price: str,
    upside: str,
    thesis: str,
    bullets: list[str],
    current_price: str = "",
    issue: str = "",
    author: str = "OPVIA RESEARCH",
) -> str:
    """
    Investment pitch cover with recommendation + target + thesis bullets.
    """
    rec_lower = recommendation.lower()

    bullets_html = []
    for i, b in enumerate(bullets, 1):
        bullets_html.append(f"""
        <div class="pd-bullet">
          <div class="pd-bullet-mark">{i:02d}</div>
          <div class="pd-bullet-text">{escape(b)}</div>
        </div>
        """)

    return f"""
<div class="cover-v cover-pitch">
  <div class="pd-header">
    <div class="pd-brand">{escape(author)}</div>
    <div class="pd-meta">{escape(issue)}</div>
  </div>
  <div class="pd-recommendation {rec_lower}">
    <div>
      <div class="pd-rec-action">{escape(recommendation.upper())}</div>
      <div class="pd-rec-target">{escape(target_price)}</div>
      <div class="pd-rec-upside">{escape(upside)}</div>
    </div>
    <div class="pd-rec-thesis">{escape(thesis)}</div>
  </div>
  <h1>{escape(title)}</h1>
  <div class="pd-thesis-label">Luận điểm chính</div>
  {''.join(bullets_html)}
  <div class="pd-footer">
    <div class="pd-footer-item">
      <div class="pd-footer-label">Ticker</div>
      <div class="pd-footer-value">{escape(ticker)}</div>
    </div>
    <div class="pd-footer-item">
      <div class="pd-footer-label">Giá hiện tại</div>
      <div class="pd-footer-value">{escape(current_price)}</div>
    </div>
    <div class="pd-footer-item">
      <div class="pd-footer-label">Target</div>
      <div class="pd-footer-value">{escape(target_price)}</div>
    </div>
  </div>
</div>
"""
