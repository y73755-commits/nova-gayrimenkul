"""Scene 8 — material detail: marble island edge, fluted oak, bronze, warm light."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=2)

marble = mat_marble("calacatta", base=(0.90, 0.88, 0.84), vein=(0.42, 0.36, 0.30), scale=2.2, rough=0.1, coat=0.5)
oak = mat_wood("fluted", dark=(0.30, 0.18, 0.09), light=(0.52, 0.34, 0.18), axis="Z", rough=0.45, scale=4.0)
wall = mat_wood("wallwood", dark=(0.16, 0.09, 0.045), light=(0.30, 0.18, 0.09), axis="Z", rough=0.5)
bronze = mat("bronze", (0.62, 0.45, 0.26), 0.22, 1.0)
floor = mat_varied("floorstone", (0.30, 0.28, 0.26), (0.36, 0.34, 0.31), rough=0.4, scale=3, bump=0.03)
strip = mat_emit("ledstrip", (1.0, 0.76, 0.48), 10.0)
ceramic = mat("ceramic", (0.10, 0.09, 0.08), 0.55, coat=0.15)

# floor + back wall with LED reveal
box(-9, -3, -0.1, 4, 3, 0, floor, name="floor")
box(-9, -3, 0, -8.8, 3, 3, wall, name="sidewall")
box(-9, 2.2, 0, 4, 2.4, 3.2, wall, name="wall")
box(-9, 2.15, 1.55, 4, 2.2, 1.57, strip, name="reveal")
box(-9, 2.15, 1.57, 4, 2.2, 1.6, wall, name="shelfline")
# island: marble top 6 cm with waterfall end at x = 0
TOP = 0.92
box(-2.5, 0.0, TOP, 0.0, 0.9, TOP + 0.06, marble, 0.004, "top")
box(-0.06, 0.0, 0.0, 0.0, 0.9, TOP, marble, 0.004, "waterfall")
# fluted oak front: half-round flutes
for i in range(0, int(2.4 / 0.045)):
    x = -2.45 + i * 0.045
    c = cyl(x, 0.02, 0.06, TOP - 0.01, 0.021, oak, 16, "flute")
box(-2.5, 0.02, 0.0, -0.06, 0.88, TOP - 0.01, oak, name="core")
box(-2.5, 0.06, 0.0, -0.06, 0.88, 0.06, mat("plinth", (0.05, 0.05, 0.05), 0.5), name="plinth")
# bronze recessed handle line just below the top
box(-2.5, -0.005, TOP - 0.06, -0.06, 0.03, TOP - 0.015, bronze, 0.003, "handle")
# objects on the top
cyl(-0.55, 0.45, TOP + 0.06, TOP + 0.30, 0.07, ceramic, 48, "vase")
cyl(-0.9, 0.55, TOP + 0.06, TOP + 0.09, 0.15, mat("board", (0.42, 0.27, 0.14), 0.5), 48, "board")
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(-0.85, 0.5, TOP + 0.125))
bpy.context.active_object.data.materials.append(mat("lemon", (0.85, 0.62, 0.1), 0.45))
# warm pendant above, out of frame, plus grazing light from the left
point((-0.8, 0.4, 2.1), 70, (1.0, 0.76, 0.5), 0.15)
area((-3.5, -0.6, 1.4), 1.0, 90, (1.0, 0.8, 0.58), rot=(0, math.radians(-70), math.radians(-20)), name="graze")
area((1.5, -2.0, 2.4), 2.0, 40, (0.9, 0.92, 1.0), rot=(math.radians(50), 0, math.radians(35)), name="fill")

sky(10, 0, strength=0.05)
sc.cycles.diffuse_bounces = 4
sc.view_settings.exposure = float(os.environ.get("EXPO", "0.0"))

camera((0.75, -0.95, 1.18), (-0.45, 0.35, 0.95), lens=50, shift_y=0.0, dof=1.45, fstop=2.8, level=False)
out = f"/home/claude/render/out/detail_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "64")), pct=25 if PREVIEW else 100)
print("WROTE", out)
