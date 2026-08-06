"""
Opvia Design Tokens - Single source of truth.
================================================

Centralized color hex codes, font stacks, và metrics. Mọi viz module
phải import từ đây thay vì hardcode hex.

Lý do: WeasyPrint SVG render không reliable với CSS class selectors,
nên SVG attributes phải dùng inline hex. Không có tokens → drift dần
giữa các files. Module này chấm dứt drift.
"""
from __future__ import annotations


class COLORS:
    """Single source of truth cho 20+ hex codes Opvia."""

    # Prussian scale
    PRUSSIAN = "#003153"
    PRUSSIAN_50 = "#E8F2F9"
    PRUSSIAN_100 = "#B3D1E6"
    PRUSSIAN_700 = "#001A2E"
    PRUSSIAN_900 = "#000d18"

    # Brass scale
    BRASS = "#B5A642"
    BRASS_300 = "#CCC46B"
    BRASS_100 = "#E8E2B8"
    BRASS_50 = "#F5F2DD"
    BRASS_700 = "#80762F"

    # Slate scale
    SLATE = "#4A6FA5"
    SLATE_LIGHT = "#7B96BD"

    # Surfaces
    IVORY = "#F5F1E8"
    IVORY_DEEP = "#EDE6D3"
    PAPER = "#FAF7F0"

    # Ink
    CHARCOAL = "#2B2B2B"
    INK = "#1A1A1A"
    TEXT_SECONDARY = "#6B6760"
    TEXT_MUTED = "#9A9688"

    # Semantic
    BORDEAUX = "#722F37"
    BORDEAUX_50 = "#F5ECED"
    POSITIVE = "#2E7D52"
    POSITIVE_LIGHT = "#A8C9B5"
    POSITIVE_BG = "#EDF7F1"
    NEGATIVE = "#C0392B"
    NEGATIVE_LIGHT = "#E8B4AC"
    NEGATIVE_BG = "#FBEEEC"

    # Grid / Axis
    GRID = "#E5E0D5"
    AXIS = "#9A9688"


class FONTS:
    """Font stack strings dùng inline trong SVG attributes."""
    SANS = "'Inter','InterVN',sans-serif"
    SERIF = "'PFD','PFDVN','Lora',Georgia,serif"
    MONO = "'JBM','JBMVN','IBM Plex Mono',monospace"


class METRICS:
    """Layout metrics - common values reused across components."""
    PAGE_WIDTH_PX = 720       # default chart container width
    PAGE_PAD_TOP = 28
    PAGE_PAD_BOT = 38
    PAGE_PAD_LEFT = 56
    PAGE_PAD_RIGHT = 32
    BORDER_RADIUS = 4
    LABEL_MIN_GAP = 11        # collision-resolve minimum spacing
