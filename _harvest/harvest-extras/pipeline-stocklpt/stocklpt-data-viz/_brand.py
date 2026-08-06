"""
StockLPT Brand - native palette (Swiss didactic).
=================================================
Tông trầm-sang: ink tím huyền (#2A1A4A) cho structure/heading/text, accent deep
mint/forest (#16633C) cho nhận diện, positive emerald (#21B36A) cho tăng điểm,
negative đỏ (#E13453) cho giảm, giấy off-white mát (#F4F6F9).

Đây là single brand, palette đã ở không gian StockLPT gốc nên `remap()` là
identity. Giữ nguyên API cũ (current_brand / set_brand / get_brand / ...) để các
module render/validator import không phải đổi.

Chọn brand:
    - Mặc định và duy nhất: StockLPT.
    - Env `STOCKLPT_BRAND` chỉ còn để tương thích ngược (mọi giá trị -> stocklpt).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

# Palette hợp lệ của StockLPT (cho validators).
STOCKLPT_PALETTE_LOWER = frozenset(h.lower() for h in {
    # structure / ink (tím huyền)
    "#2A1A4A", "#1D1238", "#130B24", "#E8E5EF", "#C2BBD4", "#221545", "#352558",
    # accent / identity (deep forest)
    "#16633C", "#3C8C5E", "#C5E3D0", "#E8F3EC", "#0E4429", "#2C7A4E",
    # slate (grey-violet)
    "#514B78", "#847FA3",
    # surfaces (off-white mát)
    "#F4F6F9", "#EBEFF4", "#DDE4EC", "#FAFBFD", "#EDF0F5", "#E2E8F0", "#D2DAE5",
    # ink / text
    "#221A34", "#151022", "#645B76", "#8E87A0",
    # positive (emerald)
    "#21B36A", "#ABE5C6", "#E4F7ED", "#E8F7EF",
    # negative (red)
    "#E13453", "#F2B0BC", "#FCEAEC",
    # severe warning (crimson)
    "#7A1F35", "#FBE8EC", "#99283F", "#531526",
    # grid
    "#DEE4EC",
    # caution accent (gold) - hero/capsule stat
    "#C8972E", "#D8A948",
})


@dataclass(frozen=True)
class Brand:
    """StockLPT identity. remap() là identity vì palette đã native."""
    key: str = "stocklpt"
    display_name: str = "StockLPT"
    wordmark: str = "STOCKLPT"
    research_mark: str = "STOCKLPT RESEARCH"
    advisory_mark: str = "STOCKLPT ADVISORY"
    filename_prefix: str = "STOCKLPT"
    tagline: str = "Phân tích Thị trường & Cổ phiếu"
    hex_map: dict = field(default_factory=dict)   # identity
    rgba_map: dict = field(default_factory=dict)  # identity
    palette: frozenset = STOCKLPT_PALETTE_LOWER

    @property
    def is_default(self) -> bool:
        return True

    def remap(self, text: str) -> str:
        # Palette đã ở không gian StockLPT -> không cần đổi gì.
        return text

    def palette_allowed(self) -> frozenset:
        return self.palette


_BRAND = Brand()
_BRANDS: dict[str, Brand] = {"stocklpt": _BRAND}
_DEFAULT = "stocklpt"


def get_brand_name() -> str:
    return "stocklpt"


def current_brand() -> Brand:
    return _BRAND


def set_brand(key: str | None = None) -> Brand:
    """Tương thích ngược: chỉ có 1 brand. Đồng bộ env cho process con."""
    if key:
        os.environ["STOCKLPT_BRAND"] = "stocklpt"
    return _BRAND


def list_brands() -> list[str]:
    return ["stocklpt"]


def get_brand(key: str | None = None) -> Brand:
    return _BRAND


if __name__ == "__main__":
    b = current_brand()
    assert b.wordmark == "STOCKLPT" and b.filename_prefix == "STOCKLPT"
    sample = "color:#2A1A4A; fill:#16633C; STOCKLPT RESEARCH"
    assert b.remap(sample) == sample, "remap phải là identity"
    assert "#2a1a4a" in b.palette and "#16633c" in b.palette and "#21b36a" in b.palette
    print("_brand.py (StockLPT native) OK -", list_brands())
