"""Generates Nova Gayrimenkul logo SVGs (text converted to outlines) from the site's own OFL fonts.

Run: python3 tools/make_logo.py   → writes src/assets/brand/*.svg and public/favicon.svg
"""
import io, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FS = os.path.join(ROOT, "node_modules/@fontsource-variable")
OUT = os.path.join(ROOT, "src/assets/brand")
os.makedirs(OUT, exist_ok=True)

INK, PAPER, GOLD = "#101114", "#F5F1E8", "#B89B63"


def load(path, axes):
    f = TTFont(path)
    return instantiateVariableFont(f, axes, inplace=False)


def text_path(font, text, size, tracking=0.0):
    """Return (svg path d, width, ascent) for text at font-size `size` (px), tracking in em."""
    upm = font["head"].unitsPerEm
    scale = size / upm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    x = 0.0
    parts = []
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        # flip Y (font units are y-up)
        tp = TransformPen(pen, (scale, 0, 0, -scale, x, 0))
        gs[gname].draw(tp)
        parts.append(pen.getCommands())
        x += hmtx[gname][0] * scale + tracking * size
    width = x - tracking * size
    return " ".join(parts), width


bodoni = load(os.path.join(FS, "bodoni-moda/files/bodoni-moda-latin-opsz-normal.woff2"), {"opsz": 96, "wght": 500})
bodoni_ext = load(os.path.join(FS, "bodoni-moda/files/bodoni-moda-latin-ext-opsz-normal.woff2"), {"opsz": 96, "wght": 500})
jost = load(os.path.join(FS, "jost/files/jost-latin-wght-normal.woff2"), {"wght": 500})
jost_ext = load(os.path.join(FS, "jost/files/jost-latin-ext-wght-normal.woff2"), {"wght": 500})


def merged_text(main, ext, text, size, tracking):
    """Draw text picking glyphs from latin or latin-ext subset (for İ)."""
    upm = main["head"].unitsPerEm
    scale = size / upm
    x = 0.0
    parts = []
    for ch in text:
        for f in (main, ext):
            cm = f.getBestCmap()
            if ord(ch) in cm:
                g = cm[ord(ch)]
                gs = f.getGlyphSet()
                pen = SVGPathPen(gs)
                gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
                parts.append(pen.getCommands())
                x += f["hmtx"][g][0] * scale + tracking * size
                break
    return " ".join(parts), x - tracking * size


# --- monogram: Didone-style N (thin stems, thick diagonal) + four-point "nova" star
def monogram_paths(ox=0, oy=0, s=1.0, color=INK, star=GOLD):
    def P(pts):
        return "M" + " L".join(f"{ox + x * s:.2f},{oy + y * s:.2f}" for x, y in pts) + " Z"
    n = [
        P([(24, 22), (27.2, 22), (27.2, 78), (24, 78)]),                 # left hairline stem
        P([(24, 22), (39, 22), (76, 78), (61, 78)]),                     # thick diagonal
        P([(72.8, 22), (76, 22), (76, 78), (72.8, 73)]),                 # right hairline stem
        P([(16, 22), (35, 22), (35, 23.6), (16, 23.6)]),                 # top-left serif
        P([(65, 22), (84, 22), (84, 23.6), (65, 23.6)]),                 # top-right serif
        P([(16, 76.4), (35, 76.4), (35, 78), (16, 78)]),                 # bottom-left serif
    ]
    cx, cy, r, w = 86, 9, 7.5, 1.6
    st = P([(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r), (cx - w, cy + w), (cx - r, cy), (cx - w, cy - w)])
    return f'<path fill="{color}" d="{" ".join(n)}"/><path fill="{star}" d="{st}"/>'


def svg(w, h, body, title="Nova Gayrimenkul"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{body}</svg>\n")


def wordmark_group(x, y, color, sub_color, nova_size=46, sub_size=11.2):
    d1, w1 = text_path(bodoni, "NOVA", nova_size, tracking=0.16)
    d2, w2 = merged_text(jost, jost_ext, "GAYRİMENKUL", sub_size, tracking=0.42)
    # centre the subline under NOVA
    sx = x + (w1 - w2) / 2
    g = (f'<path fill="{color}" d="{d1}" transform="translate({x:.2f},{y:.2f})"/>'
         f'<path fill="{sub_color}" d="{d2}" transform="translate({sx:.2f},{y + sub_size * 2.1:.2f})"/>')
    return g, max(w1, w2)


for variant, fg, sub in (("dark", INK, "#5A5750"), ("light", PAPER, "#CFC7B6")):
    # horizontal lockup: monogram + wordmark
    mono = monogram_paths(0, 4, 0.62, fg, GOLD)
    wm, ww = wordmark_group(74, 44, fg, sub)
    rule = f'<rect x="64" y="10" width="0.9" height="56" fill="{GOLD}"/>'
    W = 74 + ww + 4
    open(os.path.join(OUT, f"logo-yatay-{variant}.svg"), "w").write(svg(W, 72, mono + rule + wm))
    # stacked wordmark only
    wm2, ww2 = wordmark_group(4, 48, fg, sub)
    open(os.path.join(OUT, f"logo-yazi-{variant}.svg"), "w").write(svg(ww2 + 8, 76, wm2))
    # monogram only
    open(os.path.join(OUT, f"monogram-{variant}.svg"), "w").write(svg(100, 100, monogram_paths(0, 0, 1.0, fg, GOLD), "Nova Gayrimenkul N monogramı"))

# favicon: monogram on ink tile
fav = f'<rect width="100" height="100" rx="14" fill="{INK}"/>' + monogram_paths(6, 8, 0.86, PAPER, GOLD)
open(os.path.join(ROOT, "public/favicon.svg"), "w").write(svg(100, 100, fav, "Nova Gayrimenkul"))
open(os.path.join(OUT, "favicon.svg"), "w").write(svg(100, 100, fav, "Nova Gayrimenkul"))
print("logo files written to", OUT)
