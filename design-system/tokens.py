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
    # Xem ghi chu trong tokens.css: ha do sang cho dat WCAG 4,5:1 tren nen giay.
    "ink_lo": "#66788C",
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
# Fix chieu nguoc (dot don sau Phase 1): them "display". tokens.css co
# --font-display tu dau, tro CUNG mot stack voi --font-serif (giu hai bien de
# khoi phai sua moi selector da gan var(--font-display): h1-h3, sg-value,
# t-abbr). Ban Python truoc thieu han no, va khong test nao do, vi test cu chi
# di mot chieu Python -> CSS. Chart matplotlib ve tieu de bang vai tro
# "display" nen day la thieu that, khong phai bien trang tri.
FONTS = {
    "display": '"Spectral", "Noto Serif", Georgia, "Times New Roman", serif',
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

# ==============================================================================
# CHU DE MAU DAT TEN THEO FILE JSON
#
# Sinh tu design-system/themes/*.json bang design-system/generate-tokens.mjs. DUNG SUA
# TAY vung giua hai marker duoi day; sua gia tri o file JSON tuong ung roi chay lai
# generator (xem lenh trong tokens.css). THEMES la dict MOI, tach biet voi COLORS o
# tren: COLORS la ban phang khop voi khoi :root mac dinh cua tokens.css (khong doi),
# THEMES la registry theo TEN chu de cho tuong lai chon bang bang ten.
# ==============================================================================
# THEME-TOKENS:BAT-DAU
THEMES = {
    "sang-lanh": {
        "mau": {
            "paper": "#FFFFFF",
            "paper_hi": "#F7F9FC",
            "paper_hair": "#EEF1F6",
            "paper_elev": "#F7F9FC",
            "ink": "#051C2C",
            "ink_md": "#42566A",
            "ink_lo": "#66788C",
            "ink_faint": "#AAB8C4",
            "line": "#DBE2EA",
            "line_lo": "#EEF1F6",
            "accent": "#2251FF",
            "accent_hi": "#1233B8",
            "accent_soft": "#7D9BFF",
            "pos": "#008A6D",
            "neg": "#C22F4E",
            "neg_soft": "#E4A1AF",
            "warn": "#B07A10",
            "on_ink": "#FFFFFF",
            "on_ink_md": "#B7C4D1",
            "on_ink_lo": "#8595A6",
            "on_ink_line": "#223449",
        },
        "ilus": {
            "1": "#0f172a",
            "2": "#1e293b",
            "3": "#334155",
            "4": "#475569",
            "5": "#64748b",
            "6": "#94a3b8",
            "7": "#cbd5e1",
            "8": "#e2e8f0",
            "9": "#f8fafc",
        },
    },
    "toi-lanh": {
        "mau": {
            "paper": "#0A1420",
            "paper_hi": "#111E2E",
            "paper_hair": "#16263A",
            "paper_elev": "#152234",
            "ink": "#EAF0F6",
            "ink_md": "#B7C4D1",
            "ink_lo": "#8FA2B4",
            "ink_faint": "#5A6E80",
            "line": "#2A3B4F",
            "line_lo": "#1B2A3C",
            "accent": "#6E93FF",
            "accent_hi": "#9DB6FF",
            "accent_soft": "#3A5599",
            "pos": "#3FBFA0",
            "neg": "#F0748E",
            "neg_soft": "#7A3644",
            "warn": "#E0A83C",
            "on_ink": "#051C2C",
            "on_ink_md": "#42566A",
            "on_ink_lo": "#66788C",
            "on_ink_line": "#C3D0DC",
        },
        "ilus": {
            "1": "#f8fafc",
            "2": "#e2e8f0",
            "3": "#cbd5e1",
            "4": "#94a3b8",
            "5": "#64748b",
            "6": "#475569",
            "7": "#334155",
            "8": "#1e293b",
            "9": "#0f172a",
        },
    },
}
# THEME-TOKENS:KET-THUC
