"""Scene 6 — premium office lobby, double height, marble and timber."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=8)

floor = mat_marble("floormarble", base=(0.80, 0.78, 0.74), vein=(0.45, 0.42, 0.39), scale=0.6, rough=0.08, coat=0.6)
wall = mat_varied("stonewall", (0.66, 0.62, 0.56), (0.74, 0.70, 0.64), rough=0.6, scale=1.5, bump=0.05)
slat = mat_wood("slat", dark=(0.24, 0.13, 0.06), light=(0.46, 0.28, 0.13), axis="Z", rough=0.45)
ceiling = mat("ceiling", (0.82, 0.80, 0.77), 0.9)
desk_stone = mat_marble("desk", base=(0.10, 0.10, 0.11), vein=(0.6, 0.57, 0.52), scale=1.2, rough=0.12)
bronze = mat("bronze", (0.52, 0.38, 0.22), 0.25, 1.0)
metal = mat("frame", (0.03, 0.03, 0.032), 0.35, 1.0)
glass = mat_window_glass("winglass", reflect=0.12)
leather = mat("leather", (0.32, 0.17, 0.08), 0.45, coat=0.2)
fabric = mat("fabric", (0.62, 0.58, 0.52), 1.0, sheen=0.4)
strip = mat_emit("linestrip", (1.0, 0.84, 0.66), 12.0)
outside = mat_varied("street", (0.30, 0.30, 0.30), (0.38, 0.38, 0.37), rough=0.8, scale=0.3, bump=0.0)

X0, X1, Y0, Y1, H = -11, 11, 0, 16, 8.4
box(X0, Y0, -0.2, X1, Y1, 0, floor, name="floor")
box(X0, Y0, H, X1, Y1, H + 0.3, ceiling, name="ceiling")
box(X1, Y0, 0, X1 + 0.3, Y1, H, wall, name="wallR")
box(X0, Y1, 0, X1, Y1 + 0.3, H, wall, name="wallBack")
box(X0, Y0 - 0.3, 0, X1, Y0, H, wall, name="wallFront")
# glass facade on the left (x = X0) with tall mullions
vplane((X0, Y0), (X0, Y1), 0, H, glass, "facade")
for i in range(0, 9):
    y = Y0 + i * 2.0
    box(X0 - 0.12, y - 0.04, 0, X0 + 0.02, y + 0.04, H, metal, name="mull")
box(X0 - 0.12, Y0, 4.2, X0 + 0.02, Y1, 4.28, metal, name="transom")
area((X0 - 0.4, (Y0 + Y1) / 2, H / 2), Y1 - Y0, 0.0, rot=(0, math.radians(-90), 0), size_y=H, portal=True, name="portal")
# street + trees outside
plane(-80, -40, X0 - 0.2, 60, -0.2, outside, "street")
for i in range(6):
    round_tree(X0 - 9 - random.random() * 4, -2 + i * 4.0, -0.2, 7.0, 2.4, n=6)
box(X0 - 60, -40, -0.2, X0 - 30, 60, 30, mat_varied("oppbld", (0.55, 0.52, 0.48), (0.62, 0.60, 0.56), rough=0.8, scale=0.2, bump=0.0), name="opposite")

# timber slat feature wall behind reception (back wall)
for i in range(0, int((X1 - X0 - 2) / 0.18)):
    x = X0 + 1 + i * 0.18
    box(x, Y1 - 0.25, 0, x + 0.1, Y1 - 0.05, H, slat, name="slat")
box(X0 + 1, Y1 - 0.06, 0, X1 - 1, Y1, H, mat("slatbg", (0.05, 0.04, 0.03), 0.8), name="slatbg")
# reception desk
box(-4.0, Y1 - 4.2, 0, 4.0, Y1 - 3.2, 1.1, desk_stone, 0.02, "desk")
box(-4.1, Y1 - 4.3, 1.1, 4.1, Y1 - 3.1, 1.16, bronze, 0.01, "desktop")
box(-4.0, Y1 - 4.25, 0.0, 4.0, Y1 - 4.2, 0.08, mat_emit("deskglow", (1.0, 0.78, 0.5), 6.0), name="deskglow")
# linear pendant lights
for x in (-6.5, 0, 6.5):
    box(x - 2.2, 6.0, 4.95, x + 2.2, 6.12, 5.0, bronze, name="lin")
    box(x - 2.15, 6.02, 4.94, x + 2.15, 6.1, 4.95, strip, name="linlight")
    for dx in (-2.0, 2.0):
        cyl(x + dx, 6.06, 5.0, H, 0.004, metal, 6, "wire")
# ceiling light slots
for y in (3.0, 9.0, 13.0):
    box(X0 + 1, y, H - 0.02, X1 - 1, y + 0.06, H, strip, name="slot")
# seating group
box(4.5, 3.0, 0.0, 9.5, 7.0, 0.012, mat_varied("rug", (0.36, 0.33, 0.29), (0.42, 0.39, 0.35), rough=1.0, scale=30, bump=0.1), name="rug")
for (x, y) in ((5.4, 4.2), (5.4, 6.0)):
    box(x - 0.45, y - 0.45, 0.0, x + 0.45, y + 0.45, 0.42, leather, 0.07, "chair")
    box(x - 0.45, y - 0.45, 0.0, x - 0.25, y + 0.45, 0.85, leather, 0.06, "chairback")
box(8.4, 3.4, 0, 9.3, 6.8, 0.42, fabric, 0.08, "sofa")
box(9.1, 3.4, 0, 9.4, 6.8, 0.82, fabric, 0.08, "sofab")
cyl(7.0, 5.1, 0, 0.38, 0.55, desk_stone, 48, "coffeetable")
# planter with tree
box(-8.5, 10.5, 0, -6.5, 12.5, 0.6, desk_stone, 0.02, "planter")
round_tree(-7.5, 11.5, 0.6, 4.2, 1.4, n=5)
# fill
for (x, y) in ((-5, 5), (5, 5), (0, 11)):
    area((x, y, H - 0.4), 3.0, 120, (1.0, 0.82, 0.62), name="fill")

sun(38, 250, strength=3.2, color=(1.0, 0.92, 0.80), angle=0.8)
sky(38, 250, strength=0.7, air=1.0, aerosol=0.6, ozone=1.2)
sc.cycles.diffuse_bounces = 4
sc.view_settings.exposure = float(os.environ.get("EXPO", "0.3"))

camera((8.8, 0.6, 1.5), (-3.0, 13.5, 1.5), lens=18, shift_y=0.05)
out = f"/home/claude/render/out/lobby_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "56")), pct=25 if PREVIEW else 100)
print("WROTE", out)
