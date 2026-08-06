#!/usr/bin/env python3
"""
build-fonts.py — tải bộ font CHỐT (Spectral + IBM Plex Mono + IBM Plex Sans,
lấy nguyên từ reference-kimi.html) từ Google Fonts, giữ lại đúng 2
unicode-range (latin + vietnamese; bỏ latin-ext vì đó là phạm vi Trung/Đông
Âu không cần cho nội dung tiếng Việt thuần — cắt khoảng 57% dung lượng font
so với giữ cả 3 subset), base64 hoá, và sinh fonts-embedded.css để nhúng
thẳng vào HTML — chạy được OFFLINE, không phụ thuộc CDN Google Fonts lúc gửi
khách.

Lịch sử đổi bộ font (đừng ngạc nhiên nếu thấy git history có Fraunces/EB
Garamond/Inter/JetBrains Mono — đó là bản 2 "hoà theo tokens.css StoiX", đã
BỊ THAY vì tokens.css phục vụ CFA study notes, khác thể loại report tài
chính. Bản 3 chốt lại theo reference-kimi.html — 3 nguồn độc lập hội tụ cùng
bộ Spectral/IBM Plex, xem components.css đầu file).

Chạy lại khi cần đổi bộ trọng số (weight) hoặc thêm font:
    python3 build-fonts.py

Yêu cầu: có mạng lúc CHẠY SCRIPT (không phải lúc xem file .html kết quả).
"""
import re, os, base64, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "font-cache")
WOFF2_DIR = os.path.join(CACHE, "woff2")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Đổi ở đây nếu cần thêm/bớt trọng số. Giữ tối thiểu — mỗi trọng số x2 subset x ~10-110KB.
# Spectral: 400/500/600/700 + 400/600 italic (dek, pull-quote, note-box đều
# dùng italic). IBM Plex Mono: 400/500/600/700 (số liệu + mọi nhãn kỹ thuật/
# trạng thái). IBM Plex Sans: 400/600 (CHỈ ô bảng dữ liệu dày đặc — vai trò
# hẹp, xem components.css khối 1 + khối 4/5/12/13).
FAMILY_QUERY = (
    "family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600"
    "&family=IBM+Plex+Mono:wght@400;500;600;700"
    "&family=IBM+Plex+Sans:wght@400;600"
)
GOOGLE_CSS_URL = f"https://fonts.googleapis.com/css2?{FAMILY_QUERY}&display=swap"
KEEP_SUBSETS = ("latin", "vietnamese")  # bỏ latin-ext/cyrillic*/greek*
ORDER_FAM = ["Spectral", "IBM Plex Mono", "IBM Plex Sans"]


def main():
    os.makedirs(WOFF2_DIR, exist_ok=True)
    css_path = os.path.join(CACHE, "fonts.css")
    req = urllib.request.Request(GOOGLE_CSS_URL, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    open(css_path, "w", encoding="utf-8").write(css)

    blocks = re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css)
    keep = [b for b in blocks if b[0] in KEEP_SUBSETS]
    print(f"Tổng {len(blocks)} block trong CSS gốc, giữ {len(keep)} block (subset {KEEP_SUBSETS}).")

    def sort_key(b):
        fam = re.search(r"font-family:\s*'([^']+)'", b[1]).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", b[1]).group(1)
        style = re.search(r"font-style:\s*(\w+)", b[1]).group(1)
        return (ORDER_FAM.index(fam) if fam in ORDER_FAM else 99, weight, style)

    keep.sort(key=sort_key)

    out = [
        "/* ═══════════════════════════════════════════════════════════════════════",
        "   FONT EMBED OFFLINE — base64, subset latin+vietnamese (bỏ latin-ext).",
        "   Sinh tự động bởi build-fonts.py — ĐỪNG sửa tay file này, sửa script rồi",
        "   chạy lại. Nguồn: Google Fonts, tải qua UA Chrome thật.",
        "   ═══════════════════════════════════════════════════════════════════════ */",
    ]
    total = 0
    for subset, block in keep:
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        unicode_range = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
        url = re.search(r"url\(([^)]+)\)\s*format", block).group(1)
        safe_fam = fam.replace(" ", "-")
        fname = os.path.join(WOFF2_DIR, f"{safe_fam}-{weight}-{style}-{subset}.woff2")
        if not os.path.exists(fname):
            r = urllib.request.Request(url, headers={"User-Agent": UA})
            data = urllib.request.urlopen(r, timeout=20).read()
            open(fname, "wb").write(data)
        data = open(fname, "rb").read()
        b64 = base64.b64encode(data).decode("ascii")
        total += len(b64)
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"unicode-range:{unicode_range};}}"
        )

    out_path = os.path.join(HERE, "fonts-embedded.css")
    open(out_path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"Đã ghi {out_path} — {len(keep)} @font-face, ~{total/1024:.0f}KB base64.")


if __name__ == "__main__":
    main()
