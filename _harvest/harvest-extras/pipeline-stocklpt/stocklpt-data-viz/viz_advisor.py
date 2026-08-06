"""
StockLPT Data Viz - viz_advisor (DEPRECATED)
==========================================

DEPRECATED. Module cu voi 22 regex heuristics da duoc scrap.

Reason: LLM (Opus) chay skill nay LA advisor. Doc content truc tiep + decide
component thong qua catalog/INDEX.md + archetypes/ folder. Regex preprocessor
khong con gia tri them.

Migration:
    # OLD (deprecated)
    from viz_advisor import analyze, recommend, explain

    # NEW
    # LLM doc catalog/INDEX.md + archetypes/<name>/README.md tu pick component
    # Render qua viz / viz_wave8 / viz_wave9 / viz_wave10
    # Validate qua validators.validate_html(html_body)
"""
from __future__ import annotations
import warnings


_DEPRECATION_MSG = (
    "viz_advisor module deprecated. LLM (Opus) chay skill nay la advisor - "
    "doc catalog/INDEX.md + archetypes/<name>/README.md de pick component."
)


def analyze(content, *args, **kwargs):
    warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    raise NotImplementedError(
        "viz_advisor.analyze() removed. LLM doc content truc tiep - "
        "xem catalog/INDEX.md."
    )


def recommend(shape, *args, **kwargs):
    warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    raise NotImplementedError(
        "viz_advisor.recommend() removed. LLM skim catalog/INDEX.md + "
        "deep-read spec - xem SKILL.md section Workflow."
    )


def explain(content, *args, **kwargs):
    warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
    raise NotImplementedError(
        "viz_advisor.explain() removed. LLM doc content + catalog truc tiep."
    )


# Re-export validators de legacy code import duoc
try:
    from validators import (
        is_valid_ticker, get_ticker_sector, extract_tickers,
        format_vn_number,
        validate_no_em_dash, validate_palette,
        validate_vn_numbers, validate_font_whitelist, validate_html,
        BANK_TICKERS, STOCK_TICKERS, ALL_TICKERS,
    )
except ImportError:
    pass


__all__ = [
    "analyze", "recommend", "explain",
    "is_valid_ticker", "get_ticker_sector", "extract_tickers",
    "format_vn_number",
    "validate_no_em_dash", "validate_palette",
    "validate_vn_numbers", "validate_font_whitelist", "validate_html",
    "BANK_TICKERS", "STOCK_TICKERS", "ALL_TICKERS",
]
