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

Fix round 3 (bug lộn glyph tiếng Việt trong WeasyPrint, ví dụ "nghệ" ra
"nght"): bản trước sinh HAI khối @font-face cho MỖI tổ hợp
(family, style, weight), một cho subset latin và một cho subset vietnamese,
đúng cách Google Fonts phục vụ qua mạng để trình duyệt chỉ tải subset cần
dùng. Nhưng font ở đây đã NHÚNG BASE64 ngay trong file, không tải qua mạng,
nên unicode-range không tiết kiệm được gì mà chỉ còn tác hại: WeasyPrint
không chọn đúng subset khi nhiều @font-face trùng family/style/weight, dẫn
tới lộn glyph (không phải tofu, không phải lỗi font-family tên trần) ngay ở
TẦNG TEXT của PDF. Sửa bằng cách sinh ĐÚNG MỘT @font-face cho mỗi tổ hợp,
phủ cả latin lẫn vietnamese trong một subset, bỏ hẳn unicode-range.

Cách gộp subset đã chọn: KHÔNG merge hai file .woff2 tách sẵn của Google
(rủi ro glyph ID/cmap không tương thích giữa hai lần subset độc lập), mà
dùng fontTools.subset để tạo một subset duy nhất từ font gốc:
  1. Gọi Google Fonts CSS API bằng UA trình duyệt hiện đại như cũ, CHỈ để
     đọc unicode-range của hai subset latin/vietnamese (Google có thể đổi
     phạm vi này giữa các version font, nên đọc động thay vì hard-code).
  2. Gọi lại CHÍNH API đó bằng USER-AGENT CŨ (trình duyệt không hiểu
     unicode-range/woff2, ví dụ Firefox 3.6). Với UA này Google trả về
     ĐÚNG MỘT @font-face cho mỗi tổ hợp, không tách subset, định dạng woff,
     và font phủ toàn bộ Unicode font hỗ trợ (đã verify bằng tay: font
     Spectral 400 tải theo cách này có sẵn cả U+1EC7 'ệ' lẫn latin cơ bản).
     Đây là "font gốc" dùng để subset.
  3. Dùng fontTools.subset.Subsetter với tập unicode = HỢP của hai
     unicode-range đọc được ở bước 1, chạy trên font gốc ở bước 2, xuất
     woff2. Giữ layout_features=["*"] để không mất kerning/GSUB.
Kết quả: tổng số glyph giữ lại vẫn là hợp latin+vietnamese như cũ, chỉ khác
là NẰM TRONG MỘT FILE thay vì hai. Dung lượng từng tổ hợp dao động khác
nhau tuỳ font (không đồng nhất): đo tay tại round 3 cho một tổ hợp duy nhất
(Spectral 400 normal, chênh dưới 2%) rồi suy rộng "gần như y hệt" cho cả
file là SAI, IBM Plex Sans lệch tới -40% (subset vietnamese cũ của riêng
IBM Plex Sans vốn nặng bất thường trong dữ liệu Google, không phải lỗi ở
đây). Đừng suy luận đúng/sai bằng cách so kích thước byte; xem
tests/consistency/fonts_test.py::test_moi_to_hop_khong_mat_codepoint_so_voi_font_goc
để có phép kiểm trực tiếp trên nội dung glyph (cmap) thay vì suy từ kích
thước.

Chạy lại khi cần đổi bộ trọng số (weight) hoặc thêm font:
    python3 build-fonts.py

Yêu cầu: có mạng lúc CHẠY SCRIPT (không phải lúc xem file .html kết quả).
"""
import re, os, base64, urllib.request

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "font-cache")
LEGACY_DIR = os.path.join(CACHE, "legacy-src")
WOFF2_DIR = os.path.join(CACHE, "woff2-merged")
UA_MODERN = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
# UA co, khong hieu unicode-range/woff2 -> Google tra ve DUNG MOT @font-face
# cho moi to hop (family, style, weight), khong tach subset. Day la "font
# goc" dung de subset lai, xem doan giai thich o docstring dau file.
UA_LEGACY = "Mozilla/5.0 (Windows NT 5.1; rv:1.9.2.20) Gecko/20110803 Firefox/3.6.20"

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


def _fetch_css(ua):
    req = urllib.request.Request(GOOGLE_CSS_URL, headers={"User-Agent": ua})
    return urllib.request.urlopen(req, timeout=20).read().decode("utf-8")


def _parse_unicode_ranges(modern_css):
    """Doc unicode-range cua hai subset latin/vietnamese cho MOI to hop
    (family, style, weight), tra ve dict {(fam, style, weight): set(codepoint)}.
    """
    blocks = re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", modern_css)
    keep = [b for b in blocks if b[0] in KEEP_SUBSETS]
    print(f"Doc CSS hien dai: tong {len(blocks)} block, giu {len(keep)} block subset {KEEP_SUBSETS}.")

    def parse_range(s):
        out = set()
        for part in s.split(","):
            part = part.strip()
            if not part.startswith("U+"):
                continue
            part = part[2:]
            if "-" in part:
                a, b = part.split("-")
                out.update(range(int(a, 16), int(b, 16) + 1))
            else:
                out.add(int(part, 16))
        return out

    ranges = {}
    for subset_name, block in keep:
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        urange = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
        key = (fam, style, weight)
        ranges.setdefault(key, set()).update(parse_range(urange))
    return ranges


def _parse_legacy_sources(legacy_css):
    """Doc URL font GOC (khong tach subset) cho moi to hop tu CSS UA cu.
    Tra ve dict {(fam, style, weight): url}.

    Fix round 4 (G1): ban truoc gan `sources[key] = url` truc tiep trong
    vong lap, nen neu Google doi hanh vi va tra ve NHIEU HON MOT khoi cho
    cung mot to hop o nhanh UA cu, dict se AM THAM ghi de va chi giu URL
    cuoi cung, mot fallback im lang dung nghia CLAUDE.md cam, chi o dang
    an. Hau qua neu xay ra: script lay nham mot font goc THIEU (chi latin
    hoac chi vietnamese), fontTools.subset lai IM LANG bo qua nhung
    codepoint font goc khong co, tai sinh dung loi lon glyph ban dau ma
    khong co gi bao dong. Sua bang cach DEM so khoi cho moi to hop va assert
    dung bang 1 truoc khi tra ve.
    """
    blocks = re.findall(r"@font-face\s*\{([^}]+)\}", legacy_css)
    counts = {}
    sources = {}
    for block in blocks:
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        url = re.search(r"url\(([^)]+)\)\s*format", block).group(1)
        key = (fam, style, weight)
        counts[key] = counts.get(key, 0) + 1
        sources[key] = url
    trung = {k: v for k, v in counts.items() if v != 1}
    assert not trung, (
        f"UA cu (khong hieu unicode-range) tra ve KHAC 1 khoi @font-face cho "
        f"cac to hop sau: {trung}. Neu Google da doi hanh vi nhanh UA cu "
        f"(vi du quay lai tach subset ngay ca voi UA co), lay dai URL cuoi "
        f"cung mot cach am tham se tai sinh dung bug lon glyph ma round 3 "
        f"vua sua. Kiem tra lai noi dung CSS UA cu that (bien legacy_css) "
        f"truoc khi tiep tuc."
    )
    return sources


def sort_key(key):
    fam, style, weight = key
    return (ORDER_FAM.index(fam) if fam in ORDER_FAM else 99, int(weight), style)


def main():
    os.makedirs(LEGACY_DIR, exist_ok=True)
    os.makedirs(WOFF2_DIR, exist_ok=True)

    modern_css = _fetch_css(UA_MODERN)
    open(os.path.join(CACHE, "fonts-modern.css"), "w", encoding="utf-8").write(modern_css)
    ranges = _parse_unicode_ranges(modern_css)

    legacy_css = _fetch_css(UA_LEGACY)
    open(os.path.join(CACHE, "fonts-legacy.css"), "w", encoding="utf-8").write(legacy_css)
    sources = _parse_legacy_sources(legacy_css)

    keys = sorted(ranges.keys(), key=sort_key)
    missing = [k for k in keys if k not in sources]
    assert not missing, f"khong tim thay font goc (UA cu) cho: {missing}"
    print(f"Can gop {len(keys)} to hop (family, style, weight).")

    out = [
        "/* ═══════════════════════════════════════════════════════════════════════",
        "   FONT EMBED OFFLINE: base64, subset latin+vietnamese hop nhat trong MOT",
        "   @font-face cho moi (family, style, weight), KHONG dung unicode-range.",
        "   Fix round 3: ban truoc tach 2 khoi/to hop (latin + vietnamese, kieu",
        "   Google Fonts phuc vu qua mang) lam WeasyPrint lon glyph vi khong chon",
        "   dung subset khi nhung @font-face trung ten. Font da nhung base64 san",
        "   nen tach subset khong tiet kiem duoc gi, chi con tac hai. Xem docstring",
        "   dau build-fonts.py de biet cach gop.",
        "   Sinh tu dong boi build-fonts.py, DUNG sua tay file nay, sua script roi",
        "   chay lai. Nguon: Google Fonts, tai qua UA Chrome that + UA Firefox cu.",
        "   ═══════════════════════════════════════════════════════════════════════ */",
    ]
    total = 0
    for key in keys:
        fam, style, weight = key
        safe_fam = fam.replace(" ", "-")
        legacy_path = os.path.join(LEGACY_DIR, f"{safe_fam}-{weight}-{style}.src")
        if not os.path.exists(legacy_path):
            req = urllib.request.Request(sources[key], headers={"User-Agent": UA_LEGACY})
            data = urllib.request.urlopen(req, timeout=20).read()
            open(legacy_path, "wb").write(data)

        woff2_path = os.path.join(WOFF2_DIR, f"{safe_fam}-{weight}-{style}.woff2")
        if not os.path.exists(woff2_path):
            font = TTFont(legacy_path)
            options = ft_subset.Options()
            options.flavor = "woff2"
            options.layout_features = ["*"]
            subsetter = ft_subset.Subsetter(options=options)
            subsetter.populate(unicodes=sorted(ranges[key]))
            subsetter.subset(font)
            font.save(woff2_path)

        # Fix round 4 (G1, lop phong ve thu hai): fontTools.subset IM LANG
        # bo qua codepoint font goc khong co, khong bao gio bao loi. Tu kiem
        # lai: cmap cua ket qua phai phu het phan giao giua tap unicode ky
        # vong va cmap CUA CHINH font goc (khong doi hoi nhung gi font goc
        # von khong co, chi bat truong hop subsetting lam RON THEM du lieu
        # font goc da co). Chay cho ca nhanh vua sinh lan nhanh dung cache.
        goc_cmap = set(TTFont(legacy_path).getBestCmap().keys())
        ket_qua_cmap = set(TTFont(woff2_path).getBestCmap().keys())
        ky_vong_that = ranges[key] & goc_cmap
        thieu = sorted(ky_vong_that - ket_qua_cmap)
        assert not thieu, (
            f"To hop {key}: font sau khi subset THIEU {len(thieu)} codepoint "
            f"ma CA tap ky vong (latin+vietnamese doc dong tu CSS hien dai) "
            f"LAN font goc da tai ve deu co, vi du "
            f"{[hex(c) for c in thieu[:10]]}. Xoa {woff2_path} roi chay lai "
            f"de subset lai tu dau."
        )

        data = open(woff2_path, "rb").read()
        b64 = base64.b64encode(data).decode("ascii")
        total += len(b64)
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )

    out_path = os.path.join(HERE, "fonts-embedded.css")
    open(out_path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"Đã ghi {out_path}: {len(keys)} @font-face, ~{total/1024:.0f}KB base64.")


if __name__ == "__main__":
    main()
