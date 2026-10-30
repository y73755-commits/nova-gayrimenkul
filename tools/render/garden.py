"""Scene 2 — detached luxury house with garden and wide glass facade, afternoon light."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=5)

lawn = mat_varied("lawn", (0.035, 0.08, 0.018), (0.10, 0.17, 0.04), rough=0.95, scale=0.35, bump=0.9, detail=14)
paver = mat_varied("paver", (0.55, 0.52, 0.47), (0.64, 0.61, 0.56), rough=0.8, scale=5, bump=0.1)
stone = mat_paving("stoneclad", c1=(0.34, 0.31, 0.27), c2=(0.44, 0.40, 0.35), w=0.9, h=0.3, rough=0.85)
plaster = mat_varied("plaster", (0.88, 0.87, 0.84), (0.92, 0.91, 0.88), rough=0.85, scale=6, bump=0.02)
concrete = mat_varied("concrete", (0.72, 0.71, 0.68), (0.80, 0.79, 0.76), rough=0.8, scale=5, bump=0.03)
soffit = mat_wood("soffit", dark=(0.30, 0.17, 0.08), light=(0.52, 0.33, 0.17), axis="X", rough=0.55)
woodfloor = mat_wood("floor", dark=(0.32, 0.20, 0.10), light=(0.52, 0.35, 0.19), axis="X", rough=0.4)
metal = mat("frame", (0.03, 0.03, 0.032), 0.35, 1.0)
glass = mat_glass("glass", tint=(0.84, 0.90, 0.90))
fabric = mat("sofa", (0.80, 0.76, 0.69), 0.95, sheen=0.5)
hedge = mat_varied("hedge", (0.03, 0.08, 0.02), (0.07, 0.13, 0.04), rough=0.8, scale=12, bump=0.5)
warm = mat_emit("warmceil", (1.0, 0.80, 0.58), 0.5)
water = mat_water("water", tint=(0.62, 0.80, 0.82), wave_scale=3.0, strength=0.05)
pondfloor = mat("pondfloor", (0.30, 0.34, 0.33), 0.6)

# ground
plane(-300, -300, 300, 300, 0, lawn, "lawn")
# plinth & terrace
box(-6, -4.5, 0, 24, 10.5, 0.35, concrete, 0.01, "plinth")
box(-6, -4.6, 0.30, 24, -4.5, 0.35, metal, name="edge")
# steps
for i in range(3):
    box(7.5, -5.6 - i * 0.4 + 0.4, 0, 11.5, -4.5, 0.35 - i * 0.12, concrete, 0.01, "step")

# ground floor
box(-5.5, -0.2, 0.35, -1.0, 10, 3.6, stone, 0.02, "stonevol")
box(23.5, 0, 0.35, 24, 10, 3.4, plaster, name="wallR")
box(-1.0, 9.8, 0.35, 23.5, 10.0, 3.4, plaster, name="back")
box(-1.0, 0, 0.35, 23.5, 9.8, 0.42, woodfloor, name="floor")
vplane((-1.0, 0.0), (23.5, 0.0), 0.42, 3.35, glass, "glazing")
for i in range(0, 11):
    x = -1.0 + i * 2.45
    box(x - 0.03, -0.05, 0.42, x + 0.03, 0.05, 3.35, metal, name="mull")
box(-6.0, -2.6, 3.35, 24.5, 10.2, 3.8, concrete, 0.02, "canopy")
box(-5.9, -2.5, 3.30, 24.4, 0.0, 3.35, soffit, name="soffit")
box(-1, 0.3, 3.3, 23.5, 9.6, 3.35, warm, name="ceil")
# interior pieces seen through glass
box(3, 4, 0.42, 9, 5, 0.85, fabric, 0.06, "sofa")
box(3, 5, 0.42, 9, 5.5, 1.25, fabric, 0.06, "sofab")
box(13, 6, 0.42, 18, 7, 1.3, mat_marble("marble"), 0.01, "island")
box(0, 9.6, 0.42, 23, 9.7, 3.3, mat_wood("wall", dark=(0.25, 0.14, 0.07), light=(0.45, 0.28, 0.14), axis="Z"), name="woodwall")
for x in (4, 10, 16, 21):
    area((x, 5, 3.2), 2.0, 70, (1.0, 0.8, 0.6), name="int")

# upper floor
UX0, UX1 = 8.5, 24.0
box(UX0, 1.2, 3.8, UX1, 10.0, 7.0, plaster, 0.015, "upper")
box(UX0 - 0.2, 1.0, 7.0, UX1 + 0.2, 10.2, 7.3, concrete, 0.01, "roof")
# big recessed opening on the upper front
box(UX0 + 1.0, 1.15, 4.1, UX1 - 1.2, 1.25, 6.7, mat("recess", (0.02, 0.02, 0.02), 0.5), name="recessdark")
vplane((UX0 + 1.0, 1.1), (UX1 - 1.2, 1.1), 4.1, 6.7, glass, "upglass")
for i in range(1, 6):
    x = UX0 + 1.0 + i * (UX1 - UX0 - 2.2) / 6
    box(x - 0.025, 1.05, 4.1, x + 0.025, 1.15, 6.7, metal, name="um")
box(UX0 + 1.0, 1.25, 6.6, UX1 - 1.2, 9.8, 6.7, warm, name="upceil")
# glass balustrade on canopy (terrace)


# landscape
for i in range(14):
    x = 1 + i * 1.7
    box(x, -11.0, 0, x + 1.5, -10.2, 0.9, hedge, 0.08, "hedgebox")
box(-6.2, -8.7, 0, 2.7, -8.5, 0.4, concrete, 0.01, "rim1")
box(-6.2, -5.6, 0, 2.7, -5.4, 0.4, concrete, 0.01, "rim2")
box(-6.2, -8.5, 0, -6.0, -5.6, 0.4, concrete, 0.01, "rim3")
box(2.5, -8.5, 0, 2.7, -5.6, 0.4, concrete, 0.01, "rim4")
box(-6.0, -8.5, 0.0, 2.5, -5.6, 0.08, pondfloor, name="pondfloor")
plane(-6.0, -8.5, 2.5, -5.6, 0.34, water, "pond")
# foreground planting to frame the view
for i in range(9):
    shrub(-9.5 + random.random() * 3, -15 + random.random() * 4, 0, 0.3 + random.random() * 0.3)
for i in range(6):
    shrub(6 + random.random() * 6, -15.5 + random.random() * 2, 0, 0.35 + random.random() * 0.3)
# stepping stones path to the steps
for i in range(7):
    y = -22 + i * 2.4
    box(8.4, y, 0, 10.6, y + 1.1, 0.04, paver, 0.01, "stepstone")
for i, (x, y, h) in enumerate([(-9, 13, 10), (-6, 15, 12), (27, 13, 11), (30, 16, 13), (5, 16, 9), (15, 17, 11)]):
    cypress(x, y, 0, h, 0.8, seed=i + 3)
round_tree(-11, -3, 0, 5.5, 2.4, n=6)
round_tree(30, -6, 0, 6.0, 2.6, n=6)
for x, y in [(-3, -6.5), (-2, -7.8), (4, -7.5), (13, -7), (15, -6.4), (19, -7.2), (22, -6)]:
    shrub(x, y, 0.35 if -4.5 < y else 0, 0.55 + random.random() * 0.3)
for i in range(30):
    a = random.random() * math.tau
    shrub(-35 + random.random() * 90, 22 + random.random() * 25, 0, 2.0 + random.random() * 2.0)
for i in range(10):
    round_tree(-40 + i * 9 + random.random() * 4, 30 + random.random() * 10, 0, 7 + random.random() * 3, 3 + random.random(), n=6)

sun(32, 235, strength=3.6, color=(1.0, 0.90, 0.78), angle=1.0)
sky(32, 215, strength=0.30, air=0.9, aerosol=0.2, ozone=1.4, extra_tint=(0.80, 0.90, 1.0))
sc.view_settings.exposure = -0.45

camera((-6.5, -17.5, 1.55), (4.0, -3.0, 1.55), lens=24, shift_y=0.06)
out = f"/home/claude/render/out/garden_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "40")), pct=25 if PREVIEW else 100)
print("WROTE", out)
