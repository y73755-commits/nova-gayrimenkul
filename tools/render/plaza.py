"""Scene 5 — contemporary office tower (plaza) at dusk."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=21)

paving = mat_paving("plazapaving", c1=(0.42, 0.40, 0.37), c2=(0.50, 0.48, 0.45), w=1.5, h=0.75, rough=0.45)
bronze = mat("bronze", (0.50, 0.37, 0.22), 0.3, 1.0)
dark = mat("darkmetal", (0.03, 0.03, 0.035), 0.3, 1.0)
stone = mat_varied("granite", (0.20, 0.19, 0.18), (0.28, 0.27, 0.26), rough=0.35, scale=8, bump=0.05)
facade = mat_windows("officewin", base=(0.03, 0.04, 0.05), lit=(1.0, 0.93, 0.80), strength=0.20, density=0.55, scale=(0.36, 0.36, 0.06), cell=(0.5, 0.5, 0.25), rough=0.08, glow=0.45)
facade2 = mat_windows("nbwin", base=(0.025, 0.03, 0.04), lit=(1.0, 0.82, 0.60), strength=0.14, density=0.4, scale=(0.4, 0.4, 0.075), cell=(0.5, 0.5, 0.25), rough=0.15, glow=0.3)
lobbyglow = mat_emit("lobby", (1.0, 0.82, 0.60), 4.0)
water = mat_water("water", tint=(0.20, 0.25, 0.28), wave_scale=4.0, strength=0.03)
glass = mat_glass("glass", tint=(0.80, 0.86, 0.88))
uplight = mat_emit("uplight", (1.0, 0.80, 0.55), 40.0)

plane(-2000, -2000, 2000, 2000, 0, mat("road", (0.05, 0.05, 0.055), 0.6), "ground")
box(-60, -80, 0, 60, 30, 0.15, paving, name="plaza")

# main tower: 36 x 26 m footprint, 132 m tall, glazed with bronze vertical fins
TX0, TX1, TY0, TY1, TH = -18, 18, 0, 26, 132
box(TX0, TY0, 9.0, TX1, TY1, TH, facade, name="tower")
# double-height lobby base
box(TX0 + 1.5, TY0 + 1.5, 0.15, TX1 - 1.5, TY1, 9.0, lobbyglow, name="lobbybox")
vplane((TX0, TY0), (TX1, TY0), 0.15, 9.0, glass, "lobbyglass")
for i in range(0, 13):
    x = TX0 + i * 3.0
    box(x - 0.08, TY0 - 0.15, 0.15, x + 0.08, TY0 + 0.05, 9.0, dark, name="lmull")
box(TX0 - 3, TY0 - 6, 8.6, TX1 + 3, TY0 + 1, 9.2, stone, 0.02, "canopy")
for x in range(int(TX0), int(TX1) + 1, 4):
    box(x - 0.3, TY0 - 5.8, 8.55, x + 0.3, TY0 - 5.6, 8.6, mat_emit("canopylight", (1.0, 0.8, 0.55), 10.0), name="cl")
# vertical fins on front + side faces
x = TX0
while x <= TX1 + 0.01:
    box(x - 0.09, TY0 - 0.9, 9.0, x + 0.09, TY0, TH, bronze, name="fin")
    x += 1.5
y = TY0
while y <= TY1 + 0.01:
    box(TX0 - 0.9, y - 0.09, 9.0, TX0, y + 0.09, TH, bronze, name="finS")
    y += 1.5
# slab edges every 4.2 m
z = 9.0
while z < TH:
    box(TX0 - 0.95, TY0 - 0.95, z - 0.12, TX1 + 0.1, TY0 - 0.85, z + 0.12, dark, name="slab")
    box(TX0 - 0.95, TY0 - 0.95, z - 0.12, TX0 - 0.85, TY1, z + 0.12, dark, name="slabS")
    z += 4.2
# crown
box(TX0 - 1.0, TY0 - 1.0, TH, TX1 + 1.0, TY1 + 1.0, TH + 6, bronze, name="crown")
box(TX0 - 0.6, TY0 - 0.6, TH + 0.5, TX1 + 0.6, TY1 + 0.6, TH + 5.5, mat_emit("crownglow", (1.0, 0.78, 0.5), 2.5), name="crownglow")

# neighbours
random.seed(4)
for (x0, y0, w, d, h) in [(-95, 40, 30, 30, 78), (45, 55, 34, 28, 96), (-150, 90, 40, 30, 60), (110, 110, 40, 40, 70),
                          (-60, 160, 36, 36, 110), (20, 220, 50, 40, 85), (-230, 60, 40, 40, 45), (180, 40, 30, 50, 52)]:
    box(x0, y0, 0, x0 + w, y0 + d, h, facade2, name="nb")

# reflecting pool leading to the entrance + trees with uplights
box(-5, -70, 0.15, 5, -12, 0.45, stone, 0.02, "poolrim")
plane(-4.6, -69.6, 4.6, -12.4, 0.40, water, "reflect")
for y in range(-66, -14, 8):
    for x in (-12, 12):
        box(x - 1.2, y - 1.2, 0.15, x + 1.2, y + 1.2, 0.6, stone, 0.02, "treebox")
        round_tree(x, y, 0.6, 6.0, 1.9, n=5)
        box(x - 0.2, y - 1.25, 0.6, x + 0.2, y - 1.21, 0.68, uplight, name="ul")
        area((x, y - 0.9, 0.9), 0.3, 120, (1.0, 0.78, 0.5), rot=(math.radians(-25), 0, 0), name="treeup")
# benches
for y in (-50, -30):
    for x in (-8, 8):
        box(x - 0.3, y - 2.0, 0.15, x + 0.3, y + 2.0, 0.6, stone, 0.02, "bench")

sky(-2.5, 300, strength=float(os.environ.get("SKYS", "0.9")), air=1.2, aerosol=1.4, ozone=1.8)
sc.view_settings.exposure = float(os.environ.get("EXPO", "0.4"))

camera((-11, -102, 1.6), (-2, 13, 1.6), lens=19, shift_y=0.26)
out = f"/home/claude/render/out/plaza_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "40")), pct=25 if PREVIEW else 100)
print("WROTE", out)
