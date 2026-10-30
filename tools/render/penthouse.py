"""Scene 3 — premium penthouse living room with city view at dusk."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=3)

oak = mat_wood("oak", dark=(0.30, 0.19, 0.10), light=(0.50, 0.34, 0.19), axis="X", rough=0.35, coat=0.25)
plaster = mat_varied("plaster", (0.80, 0.78, 0.74), (0.84, 0.82, 0.78), rough=0.9, scale=5, bump=0.01)
walnut = mat_wood("walnut", dark=(0.10, 0.055, 0.03), light=(0.24, 0.13, 0.07), axis="Z", rough=0.45)
fabric = mat("boucle", (0.78, 0.74, 0.67), 1.0, sheen=0.6)
leather = mat("leather", (0.30, 0.15, 0.07), 0.45, coat=0.2)
marble = mat_marble("marble", base=(0.88, 0.87, 0.85), vein=(0.35, 0.33, 0.32))
darkm = mat_marble("nero", base=(0.05, 0.05, 0.055), vein=(0.55, 0.53, 0.50), rough=0.15)
bronze = mat("bronze", (0.50, 0.37, 0.22), 0.3, 1.0)
metal = mat("frame", (0.03, 0.03, 0.032), 0.35, 1.0)
glass = mat_glass("glass", tint=(0.90, 0.94, 0.95))
rug = mat_varied("rug", (0.42, 0.38, 0.33), (0.50, 0.46, 0.40), rough=1.0, scale=40, bump=0.15)
cove = mat_emit("cove", (1.0, 0.72, 0.45), 9.0)
lampshade = mat_emit("shade", (1.0, 0.74, 0.48), 0.7)
sea = mat_sea("sea", color=(0.01, 0.025, 0.04), scale=0.02, strength=0.15)
ground = mat("cityground", (0.015, 0.015, 0.018), 0.9)
foliage = mat_varied("plant", (0.03, 0.08, 0.025), (0.08, 0.14, 0.05), rough=0.6, scale=8, bump=0.3)

W0, W1, D, H = -7.0, 7.0, 8.0, 3.3
# room shell
box(W0, 0, -0.2, W1, D, 0.0, oak, name="floor")
box(W0, -0.2, H, W1, D, H + 0.3, plaster, name="ceiling")
box(W0 - 0.2, -0.2, 0, W0, D, H, plaster, name="wallL")
box(W1, -0.2, 0, W1 + 0.2, D, H, plaster, name="wallR")
box(W0, -0.4, 0, W1, -0.2, H, plaster, name="wallBack")
# dropped ceiling with perimeter cove light
box(W0 + 0.6, 0.6, H - 0.25, W1 - 0.6, D - 0.6, H, plaster, name="drop")
box(W0 + 0.55, 0.55, H - 0.06, W1 - 0.55, 0.6, H - 0.02, cove, name="cv1")
box(W0 + 0.55, D - 0.6, H - 0.06, W1 - 0.55, D - 0.55, H - 0.02, cove, name="cv2")
box(W0 + 0.55, 0.6, H - 0.06, W0 + 0.6, D - 0.6, H - 0.02, cove, name="cv3")
# walnut feature wall left with niche light
box(W0, 0.5, 0, W0 + 0.12, D - 0.5, H - 0.25, walnut, name="walnutwall")
box(W0 + 0.12, 2.2, 0.0, W0 + 0.6, 6.0, 0.55, darkm, 0.01, "sideboard")
box(W0 + 0.13, 2.4, 1.6, W0 + 0.15, 5.8, 2.6, mat("art", (0.55, 0.42, 0.28), 0.9), name="art")
area((W0 + 1.2, 4.1, H - 0.4), 0.6, 30, (1.0, 0.75, 0.5), rot=(0, math.radians(-50), 0), name="artlight")
# window wall
vplane((W0, D), (W1, D), 0, H, glass, "glazing")
for i in range(0, 8):
    x = W0 + i * 2.0
    box(x - 0.025, D - 0.04, 0, x + 0.025, D + 0.04, H, metal, name="mull")
box(W0, D - 0.04, 0, W1, D + 0.06, 0.05, metal, name="sill")
# terrace beyond glass
box(W0, D + 0.06, -0.25, W1 + 2, D + 3.2, -0.05, mat_varied("terr", (0.38, 0.36, 0.33), (0.45, 0.43, 0.40), rough=0.6, scale=4, bump=0.05), name="terrace")
vplane((W0, D + 3.15), (W1 + 2, D + 3.15), -0.05, 1.0, glass, "balustrade")
box(W0, D + 3.12, 0.97, W1 + 2, D + 3.18, 1.02, metal, name="rail")

# furniture: L sofa, chairs, coffee table, rug, lamp
box(-4.8, 2.6, 0.0, 3.2, 6.6, 0.015, rug, name="rug")
box(-4.0, 2.4, 0.0, 1.6, 3.4, 0.45, fabric, 0.07, "sofa_seat")
box(-4.0, 2.0, 0.0, 1.6, 2.45, 0.85, fabric, 0.08, "sofa_back")
box(-4.6, 2.0, 0.0, -3.4, 5.8, 0.45, fabric, 0.07, "sofa_l")
box(-4.95, 2.0, 0.0, -4.55, 5.8, 0.85, fabric, 0.08, "sofa_lback")
for x in (-3.4, -1.6, 0.2):
    box(x, 2.5, 0.45, x + 1.0, 2.8, 0.85, mat("cush", (0.62, 0.55, 0.46), 1.0, sheen=0.5), 0.09, "cushion")
box(-2.3, 4.0, 0.0, -0.3, 5.2, 0.05, bronze, 0.005, "ct_base")
box(-2.2, 4.1, 0.05, -0.4, 5.1, 0.32, bronze, 0.005, "ct_leg")
box(-2.5, 3.85, 0.32, -0.1, 5.35, 0.38, marble, 0.008, "ct_top")
# lounge chair facing view
box(1.6, 4.6, 0.0, 2.6, 5.6, 0.4, leather, 0.06, "chair_seat")
box(1.6, 5.55, 0.0, 2.6, 5.85, 0.8, leather, 0.06, "chair_back")
box(2.9, 4.0, 0, 3.5, 4.6, 0.55, darkm, 0.01, "sidetable")
cyl(3.2, 4.3, 0.55, 1.15, 0.015, bronze, 8, "lampstem")
cyl(3.2, 4.3, 1.15, 1.45, 0.2, lampshade, 32, "lampshade")
point((3.2, 4.3, 1.3), 25, (1.0, 0.72, 0.45), 0.1)
# vase + decor
cyl(-1.0, 4.6, 0.38, 0.62, 0.08, mat("vase", (0.85, 0.83, 0.78), 0.3, coat=0.5), 32, "vase")
box(-2.1, 4.3, 0.38, -1.5, 4.7, 0.46, mat("books", (0.25, 0.20, 0.16), 0.8), 0.005, "books")
# plant in the corner
cyl(5.9, 7.2, 0, 0.6, 0.32, mat("pot", (0.12, 0.11, 0.10), 0.6), 32, "pot")
for i in range(6):
    o = sphere((5.9 + random.uniform(-0.4, 0.4), 7.2 + random.uniform(-0.3, 0.3), 1.0 + i * 0.25), (0.5, 0.5, 0.45), foliage, sub=2, name="leaf")
    displace(o, strength=0.35, size=0.12, seed=i + 2)
# interior fill lights (not visible in reflections)
for x in (-4, 0, 4):
    area((x, 3.5, H - 0.3), 1.5, 30, (1.0, 0.72, 0.48), name="fill")

# ---- the city below at dusk (penthouse ~70 m above street level)
GZ = -70
plane(-5000, -5000, 5000, 5000, GZ, ground, "cityground")
plane(-5000, 650, 5000, 1300, GZ + 0.2, sea, "strait")
win = mat_windows("citywin", strength=0.32, density=0.5, cell=(0.5, 0.5, 0.25))
win2 = mat_windows("citywin2", base=(0.025, 0.028, 0.035), lit=(1.0, 0.88, 0.70), strength=0.22, density=0.4, scale=(0.4, 0.4, 0.09), cell=(0.5, 0.5, 0.25))
random.seed(42)
for band, (y0, y1, hmin, hmax, step) in enumerate([(140, 640, 12, 58, 30), (1300, 2600, 10, 55, 38)]):
    y = y0
    while y < y1:
        x = -1600
        while x < 1600:
            if random.random() < 0.78:
                w = random.uniform(10, step * 0.85)
                d = random.uniform(10, step * 0.85)
                h = random.uniform(hmin, hmax) * (1.4 if random.random() < 0.08 else 1.0)
                box(x, y, GZ, x + w, y + d, GZ + h, win if random.random() < 0.6 else win2, name="bld")
            x += step + random.uniform(-4, 6)
        y += step + random.uniform(-3, 8)
# far hills on the opposite shore, with sparse lights
for (x, y, sx, sz) in [(-1500, 3200, 1400, 160), (600, 3500, 1300, 210), (2200, 3000, 900, 140)]:
    sphere((x, y, GZ), (sx, 400, sz), mat("farshore", (0.02, 0.022, 0.03), 1.0), sub=4, name="shore")
# a bridge line across the strait (generic suspension silhouette)
box(-1800, 980, GZ + 60, 1800, 990, GZ + 62, mat_emit("bridge", (1.0, 0.82, 0.6), 6.0), name="bridgedeck")

sky(-3.0, 20, strength=float(os.environ.get("SKYS", "0.45")), air=1.2, aerosol=1.3, ozone=1.6)
sc.view_settings.exposure = float(os.environ.get("EXPO", "0.0"))
sc.cycles.diffuse_bounces = 4

camera((5.9, 0.3, 1.25), (-1.8, 8.0, 1.25), lens=23, shift_y=-0.03, dof=6.0, fstop=5.6)
out = f"/home/claude/render/out/penthouse_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "48")), pct=25 if PREVIEW else 100)
print("WROTE", out)
