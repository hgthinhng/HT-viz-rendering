"""Token thiết kế, bản Python cho pipeline WeasyPrint.

Nguồn chân lý duy nhất là tokens.css. File này phải luôn khớp, có test ép
(tests/consistency/tokens_test.py). Sửa một bên mà quên bên kia thì test
fail.

Fix round 1: tokens.css có hai khối :root cùng specificity (khối đầu do
Task 2 thêm, khối sau bắt nguồn từ components.css). Khối sau luôn thắng
trong cascade nên SPACING và SHADOW["s1"] dưới đây lấy giá trị của khối
sau (bản người dùng đã phân xử giữ), không phải giá trị ban đầu của khối
đầu.
"""

COLORS = {
    "ink": "#051C2C",
    "ink_md": "#42566A",
    "ink_lo": "#8595A6",
    "line": "#DBE2EA",
    "paper": "#FFFFFF",
    "paper_hi": "#F7F9FC",
    "accent": "#2251FF",
    "accent_hi": "#1233B8",
    "accent_soft": "#7D9BFF",
    "warn": "#B07A10",
    "pos": "#008A6D",
    "neg": "#C22F4E",
}

# Fix round 2: FONTS lech that voi tokens.css (thieu nhanh Noto Serif/Noto
# Sans, "sans" co them Arial ma CSS khong co). Da sua khop nguyen van voi
# --font-serif / --font-sans / --font-mono trong tokens.css (khoi :root thu
# hai). Moi list van ket thuc bang generic keyword: serif, monospace,
# sans-serif.
FONTS = {
    "serif": '"Spectral", "Noto Serif", Georgia, "Times New Roman", serif',
    "mono": '"IBM Plex Mono", "Noto Sans Mono", Menlo, Consolas, "Liberation Mono", monospace',
    "sans": '"IBM Plex Sans", "Noto Sans", -apple-system, "Segoe UI", sans-serif',
}

SPACING = [4, 8, 12, 16, 20, 28, 40, 56]

RADIUS = {"r0": 0, "r1": 2, "r2": 3, "r3": 6}

# Cu phap rgba(R G B / A) (CSS Color 4, khong dau phay trong ngoac): giu
# nguyen tri so mau/alpha nhung tranh dau phay lam hong phep tach
# val.split(",") theo lop shadow trong tokens_test.py. Da verify parse duoc
# bang tinycss2 va render duoc bang WeasyPrint 69.0 cai trong repo.
# s1 va hairline lay tu khoi :root thu hai (ban thang) trong tokens.css.
SHADOW = {
    "s1": "2px 2px 0px rgba(5 28 44 / 0.12), -1px -1px 0px rgba(255 255 255 / 0.6)",
    "s2": "2px 2px 0px rgba(5 28 44 / 0.08), -1px -1px 0px rgba(5 28 44 / 0.04)",
    "s3": "3px 3px 0px rgba(5 28 44 / 0.10), -1px -1px 0px rgba(5 28 44 / 0.05)",
    "none": "0px 0px 0px rgba(0 0 0 / 0)",
    "hairline": "0px 1px 0px rgba(5 28 44 / 0.35)",
}
