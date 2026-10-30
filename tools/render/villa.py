"""Scene 1 — modern villa with infinity pool at sunset (hero, desktop + mobile crops, pool angle)."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "desktop"
PREVIEW = "--preview" in sys.argv

sc = reset(seed=11)

# ---- materials
trav = mat_paving("paving")
coping = mat_varied("travertine", (0.74, 0.67, 0.56), (0.83, 0.77, 0.67), rough=0.75, scale=3.5, bump=0.08)
plaster = mat_varied("plaster", (0.86, 0.84, 0.80), (0.90, 0.88, 0.85), rough=0.85, scale=6, bump=0.02)
concrete = mat_varied("concrete", (0.70, 0.69, 0.66), (0.78, 0.77, 0.74), rough=0.8, scale=5, bump=0.04)
stonewall = mat_varied("stonewall", (0.36, 0.32, 0.27), (0.55, 0.49, 0.41), rough=0.85, scale=2.2, bump=0.45, detail=10)
cliff = mat_varied("cliff", (0.22, 0.19, 0.15), (0.34, 0.30, 0.24), rough=0.95, scale=0.15, bump=0.6, detail=10)
wood = mat_wood("cladding", dark=(0.16, 0.08, 0.035), light=(0.36, 0.20, 0.09), axis="Z", rough=0.55)
woodfloor = mat_wood("floor", dark=(0.30, 0.18, 0.09), light=(0.50, 0.33, 0.18), axis="X", rough=0.4, coat=0.2)
metal = mat("frame", (0.035, 0.035, 0.038), 0.35, 1.0)
bronze = mat("bronze", (0.50, 0.37, 0.22), 0.32, 1.0)
glass = mat_glass("glass", tint=(0.86, 0.92, 0.92))
tile = mat_varied("pooltile", (0.40, 0.66, 0.68), (0.48, 0.74, 0.75), rough=0.35, scale=8, bump=0.02)
water = mat_water("water", tint=(0.72, 0.92, 0.93), wave_scale=1.4, strength=0.08)
sea = mat_sea("sea", color=(0.012, 0.04, 0.06))
haze_far = mat("haze_far", (0.05, 0.05, 0.065), 1.0)
haze_mid = mat_varied("haze_mid", (0.10, 0.12, 0.10), (0.15, 0.17, 0.13), rough=1.0, scale=0.02, bump=0.0)
fabric = mat("sofa", (0.78, 0.74, 0.67), 0.95, sheen=0.5)
dark = mat("darkfab", (0.10, 0.09, 0.08), 0.9)
warm = mat_emit("warmstrip", (1.0, 0.70, 0.42), 14.0)
warm_soft = mat_emit("warmceil", (1.0, 0.76, 0.52), 0.9)
bollard_light = mat_emit("bollard", (1.0, 0.72, 0.45), 30.0)

# ---- site: terrace platform on a cliff above the sea
box(-16, -16, -40, 34, 26, -0.3, cliff, name="cliff")
box(-16, -16, -0.3, 34, -9, 0, trav, 0.01, "deckA")
box(-16, -3, -0.3, 34, 26, 0, trav, 0.01, "deckB")
box(12, -9, -0.3, 34, -3, 0, trav, 0.01, "deckD")
box(-16, -9, -0.3, -10.2, -3, -0.12, trav, 0.01, "deckC")  # lowered infinity edge
# pool basin
box(-10.2, -9, -1.6, 12, -3, -1.4, tile, name="poolfloor")
box(-10.2, -9.2, -1.6, 12, -9, -0.02, tile, name="pw1")
box(-10.2, -3, -1.6, 12, -2.8, -0.02, tile, name="pw2")
box(11.8, -9, -1.6, 12, -3, -0.02, tile, name="pw3")
box(-10.4, -9, -1.6, -10.2, -3, -0.14, tile, name="pw4")
plane(-10.35, -9, 12, -3, -0.075, water, "water")
# underwater pool lights
for x in (-6, 0, 6):
    box(x - 0.15, -3.02, -0.7, x + 0.15, -3.0, -0.55, mat_emit("poollight", (0.9, 0.95, 1.0), 25.0), name="pl")

# glass balustrade along the sea edge
vplane((-15.9, -16), (-15.9, 26), 0, 1.05, glass, "balustrade")
box(-15.95, -16, 1.0, -15.85, 26, 1.05, metal, name="rail")
vplane((-16, -15.9), (34, -15.9), 0, 1.05, glass, "balustrade2")

# sea and distant shore
plane(-4000, -4000, 4000, 4000, -36, sea, "sea")
for (x, y, sx, sy, sz) in [(-2600, 2900, 900, 420, 75), (-1300, 3400, 800, 380, 105), (-200, 3800, 700, 300, 80),
                            (-3600, 1700, 700, 500, 60)]:
    sphere((x, y, -36), (sx, sy, sz), haze_far, sub=4, name="farhill")
# wooded hill rising behind the villa
for (x, y, sx, sy, sz) in [(900, 2600, 900, 400, 70), (1900, 2300, 700, 350, 95)]:
    sphere((x, y, -36), (sx, sy, sz), haze_far, sub=4, name="farhill2")

# ---- villa: ground floor (glass pavilion)
box(-1.2, 0.0, 0.0, 0.0, 12.5, 3.35, stonewall, 0.02, "stonewall")       # feature wall
box(22.0, 2.0, 0.0, 22.4, 12.5, 3.3, plaster, 0.01, "wallR")
box(0.0, 12.0, 0.0, 22.0, 12.4, 3.3, plaster, name="wallBack")
box(0.0, 2.0, 0.0, 22.0, 12.0, 0.12, woodfloor, name="intfloor")
# glazing + mullions
vplane((0.0, 2.0), (22.0, 2.0), 0.12, 3.3, glass, "glazing")
for i in range(0, 10):
    x = i * 2.44
    box(x - 0.03, 1.96, 0.12, x + 0.03, 2.06, 3.3, metal, name="mullion")
box(0.0, 1.96, 3.22, 22.0, 2.06, 3.32, metal, name="transom")
# slab + soffit lights
box(-1.4, 1.0, 3.3, 23.2, 12.6, 3.75, concrete, 0.02, "slab1")
box(-0.6, 1.25, 3.29, 22.6, 1.32, 3.3, warm, name="soffitstrip")

# interior: back wall timber, sofa, island, pendants
box(0.2, 11.9, 0.12, 21.8, 12.0, 3.3, wood, name="woodwall")
box(4.5, 6.0, 0.12, 10.5, 7.0, 0.55, fabric, 0.06, "sofa")
box(4.5, 7.0, 0.12, 10.5, 7.5, 0.95, fabric, 0.06, "sofaback")
box(6.2, 4.4, 0.12, 8.8, 5.4, 0.42, mat_marble("marble"), 0.01, "ctable")
box(3.5, 4.0, 0.12, 11.5, 7.8, 0.13, mat("rug", (0.55, 0.50, 0.44), 1.0), name="rug")
box(13.5, 7.5, 0.12, 18.5, 8.6, 1.0, mat_marble("marble"), 0.01, "island")
box(13.5, 7.5, 0.12, 18.5, 8.6, 0.1, bronze, name="kick")
for x in (14.6, 16.0, 17.4):
    cyl(x, 8.05, 2.2, 3.3, 0.004, metal, 6, "wire")
    sphere((x, 8.05, 2.15), (0.16, 0.16, 0.16), mat_emit("pendant", (1.0, 0.74, 0.48), 18.0), sub=3, name="pendant")
box(0.2, 2.2, 3.22, 21.8, 11.8, 3.3, warm_soft, name="ceilglow")
for x in (3, 8, 13, 18):
    area((x, 7, 3.15), 2.0, 140, (1.0, 0.74, 0.50), name="int")
# floor lamp / art
box(19.5, 11.7, 1.0, 21.0, 11.85, 2.6, mat("art", (0.62, 0.48, 0.32), 0.8), name="art")

# ---- upper volume (cantilever with ribbon window)
X0, X1, Y0, Y1, Z0, Z1 = -4.5, 15.0, 3.0, 11.6, 3.75, 7.05
box(X0 + 0.9, Y0, Z0 + 0.12, X1 - 0.6, Y0 + 0.35, 4.45, plaster, 0.0, "uf_low")
box(X0 + 0.9, Y0, 6.35, X1 - 0.6, Y0 + 0.35, Z1, plaster, 0.0, "uf_high")
box(X0, Y0, Z0, X0 + 0.9, Y1, Z1, plaster, 0.0, "uf_endL")
box(X1 - 0.6, Y0, Z0, X1, Y1, Z1, plaster, 0.0, "uf_endR")
box(X0 + 0.9, Y1 - 0.3, Z0 + 0.12, X1 - 0.6, Y1, Z1, plaster, name="uf_back")
box(X0 + 0.9, Y0 + 0.35, Z0, X1 - 0.6, Y1 - 0.3, Z0 + 0.12, concrete, name="uf_floor")
box(X0 - 0.15, Y0 - 0.15, Z1, X1 + 0.15, Y1 + 0.15, Z1 + 0.22, concrete, 0.01, "roof1")
vplane((X0 + 0.9, Y0 + 0.5), (X1 - 0.6, Y0 + 0.5), 4.45, 6.35, glass, "ribbon")
for i in range(1, 7):
    x = X0 + 0.9 + i * (X1 - X0 - 1.5) / 7
    box(x - 0.025, Y0 + 0.47, 4.45, x + 0.025, Y0 + 0.55, 6.35, metal, name="rm")
box(X0 + 0.9, Y0 + 0.6, 6.25, X1 - 0.6, Y1 - 0.3, 6.35, warm_soft, name="ufceil")
box(X0 + 1.0, Y1 - 0.5, Z0, X1 - 0.7, Y1 - 0.3, 6.3, wood, name="ufwood")
for x in (-1, 4, 9, 13):
    area((x, 7, 6.2), 1.8, 90, (1.0, 0.74, 0.50), name="int2")
box(0, 8.5, 3.87, 5, 10.5, 4.4, fabric, 0.05, "bed")

# ---- secondary timber volume
TX0, TX1 = 15.6, 22.4
box(TX0, 4.5, 3.75, TX1, 12.4, 6.3, concrete, name="tv_core")
for i in range(0, int((TX1 - TX0) / 0.16)):
    x = TX0 + i * 0.16
    box(x, 4.3, 3.8, x + 0.09, 4.45, 6.25, wood, name="slat")
for i in range(0, int((12.4 - 4.5) / 0.16)):
    y = 4.5 + i * 0.16
    box(TX1 + 0.05, y, 3.8, TX1 + 0.2, y + 0.09, 6.25, wood, name="slat")
box(TX0 - 0.1, 4.2, 6.3, TX1 + 0.3, 12.5, 6.48, concrete, 0.01, "roof2")

# ---- landscape
for i, (x, y, h) in enumerate([(-3, 16, 10.5), (1.5, 18.5, 12.0), (5, 15.5, 9.0), (24.5, 15.5, 11.0),
                                (27.5, 18, 12.5), (31, 14.5, 9.5)]):
    cypress(x, y, 0, h, 0.75 + random.random() * 0.15, seed=i + 1)
round_tree(29, 3, 0, 5.5, 2.2)

for x in range(24, 33, 2):
    shrub(x + random.random(), -1.5 + random.random(), 0, 0.6 + random.random() * 0.3)

# planters
box(23.4, -2.6, 0, 33.6, -0.6, 0.45, concrete, 0.02, "planter")
# loungers between pool and house
for x in (-2.0, 0.4, 2.8):
    lounger(x, -0.9, rot=math.radians(180))
box(-7.5, -1.5, 0, -6.9, -0.9, 0.55, metal, 0.02, "sidetable")
# garden bollards
for x in (-8, -4, 14, 18):
    box(x - 0.08, -2.4, 0, x + 0.08, -2.24, 0.6, metal, name="bollard")
    box(x - 0.06, -2.43, 0.42, x + 0.06, -2.41, 0.55, bollard_light, name="bl")

# ---- light: golden hour from south-west, sky behind camera-left
import os
LIGHT = os.environ.get("LIGHT", "golden")
if LIGHT == "golden":
    sun(1.8, 188, strength=5.0, color=(1.0, 0.52, 0.26), angle=0.8)
    sky(1.8, 262, strength=0.22, air=1.6, aerosol=2.5, ozone=1.6)
else:  # blue hour: sun just below the horizon over the sea, villa lit by sky + interiors
    sky(-1.2, 282, strength=float(os.environ.get("SKYS", "0.9")), air=1.2, aerosol=1.6, ozone=1.4)
    sc.view_settings.exposure = float(os.environ.get("EXPO", "0.0"))

if SHOT == "desktop":
    camera((-12.5, -13.8, 1.6), (-6.8, -3.2, 1.6), lens=24, shift_y=0.1)
    W, H = (2160, 1215)
elif SHOT == "mobile":
    camera((-4.5, -14.8, 1.35), (1.5, -3.8, 1.35), lens=20, shift_y=0.1)
    W, H = (1080, 1620)
else:  # pool angle, low to the water, looking along the infinity edge to the sea
    camera((13.6, -7.4, 0.95), (2.0, -4.6, 0.95), lens=22, shift_y=0.12)
    W, H = (1600, 1067)

out = f"/home/claude/render/out/villa_{SHOT}{'_prev' if PREVIEW else ''}.png"
if PREVIEW:
    render(out, W, H, samples=12, pct=25)
else:
    render(out, W, H, samples=int(os.environ.get("SPP", "40")))
print("WROTE", out)
