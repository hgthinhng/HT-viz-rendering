"""
StockLPT Design Tokens - Single source of truth.
================================================

Centralized color hex codes, font stacks, và metrics. Mọi viz module
phải import từ đây thay vì hardcode hex.

Lý do: WeasyPrint SVG render không reliable với CSS class selectors,
nên SVG attributes phải dùng inline hex. Không có tokens → drift dần
giữa các files. Module này chấm dứt drift.
"""
from __future__ import annotations


class COLORS:
    """Single source of truth cho 20+ hex codes StockLPT."""

    # Indigo scale
    INDIGO = "#2A1A4A"
    INDIGO_50 = "#E8E5EF"
    INDIGO_100 = "#C2BBD4"
    INDIGO_700 = "#1D1238"
    INDIGO_900 = "#130B24"

    # Accent scale
    ACCENT = "#16633C"
    ACCENT_300 = "#3C8C5E"
    ACCENT_100 = "#C5E3D0"
    ACCENT_50 = "#E8F3EC"
    ACCENT_700 = "#0E4429"

    # Slate scale
    SLATE = "#514B78"
    SLATE_LIGHT = "#847FA3"

    # Surfaces
    IVORY = "#EBEFF4"
    IVORY_DEEP = "#DDE4EC"
    PAPER = "#F4F6F9"

    # Ink
    CHARCOAL = "#221A34"
    INK = "#151022"
    TEXT_SECONDARY = "#645B76"
    TEXT_MUTED = "#8E87A0"

    # Semantic
    BORDEAUX = "#7A1F35"
    BORDEAUX_50 = "#FBE8EC"
    POSITIVE = "#21B36A"
    POSITIVE_LIGHT = "#ABE5C6"
    POSITIVE_BG = "#E4F7ED"
    NEGATIVE = "#E13453"
    NEGATIVE_LIGHT = "#F2B0BC"
    NEGATIVE_BG = "#FCEAEC"

    # Grid / Axis
    GRID = "#DEE4EC"
    AXIS = "#8E87A0"

    # Caution accent (gold)
    GOLD = "#C8972E"
    GOLD_LIGHT = "#D8A948"


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
