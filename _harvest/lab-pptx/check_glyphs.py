from fontTools.ttLib import TTFont

# Chars requested by team-lead (stacked-diacritic Vietnamese), plus a
# few extra structurally-distinct ones for good measure.
test_chars = "ừộẫợữểỗ"
extra_chars = "đĐưƯơƠ"  # base Vietnamese-specific letters (not stacking, but VN-exclusive)
all_chars = test_chars + extra_chars

fonts = [
    "fraunces", "ebgaramond", "inter", "jetbrainsmono", "bevietnampro",
    "newsreader", "ibmplexsans", "spectral", "ibmplexmono", "sourceserif4",
]

print(f"{'font':14s} | " + " ".join(all_chars) + "  | missing")
print("-" * 70)
for name in fonts:
    path = f"{name}.ttf"
    try:
        tt = TTFont(path, fontNumber=0, lazy=True)
        cmap = tt.getBestCmap()
        row = []
        missing = []
        for ch in all_chars:
            cp = ord(ch)
            ok = cp in cmap
            row.append("Y" if ok else ".")
            if not ok:
                missing.append(f"{ch}(U+{cp:04X})")
        print(f"{name:14s} | " + "  ".join(row) + "  | " + (",".join(missing) if missing else "NONE"))
    except Exception as e:
        print(f"{name:14s} | ERROR: {e}")
