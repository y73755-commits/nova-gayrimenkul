"""Scene 4 — elegant residence interior, daylight through tall windows."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=9)

oak = mat_wood("oak", dark=(0.36, 0.24, 0.13), light=(0.56, 0.40, 0.24), axis="Y", rough=0.38, coat=0.2)
plaster = mat_varied("plaster", (0.86, 0.84, 0.80), (0.89, 0.87, 0.83), rough=0.9, scale=5, bump=0.01)
panel = mat("panel", (0.83, 0.81, 0.77), 0.7)
walnut = mat_wood("walnut", dark=(0.12, 0.065, 0.035), light=(0.28, 0.16, 0.08), axis="X", rough=0.4, coat=0.3)
fabric = mat("linen", (0.72, 0.66, 0.58), 1.0, sheen=0.5)
chairfab = mat("chairfab", (0.55, 0.47, 0.38), 1.0, sheen=0.5)
marble = mat_marble("marble", base=(0.90, 0.89, 0.86), vein=(0.50, 0.47, 0.44))
bronze = mat("bronze", (0.52, 0.38, 0.22), 0.28, 1.0)
metal = mat("frame", (0.03, 0.03, 0.032), 0.35, 1.0)
glass = mat_window_glass("winglass")
sheer = mat("sheer", (0.93, 0.91, 0.88), 0.9, sss=0.3)
foliage = mat_varied("plant", (0.03, 0.08, 0.025), (0.08, 0.14, 0.05), rough=0.6, scale=8, bump=0.3)
outside = mat_varied("outside", (0.20, 0.28, 0.14), (0.35, 0.42, 0.25), rough=1.0, scale=0.05, bump=0.0)

L, Wd, H = 11.0, 7.5, 3.2
box(0, 0, -0.2, L, Wd, 0, oak, name="floor")
box(0, 0, H, L, Wd, H + 0.2, plaster, name="ceiling")
box(0, Wd, 0, L, Wd + 0.2, H, plaster, name="wallBack")
box(L, 0, 0, L + 0.2, Wd, H, plaster, name="wallR")
box(0, -0.2, 0, L, 0, H, plaster, name="wallFront")
# window wall on the left (x=0): three tall openings
openings = [(0.8, 2.2), (2.9, 4.3), (5.0, 6.4)]
prev = 0.0
for (y0, y1) in openings:
    box(-0.3, prev, 0, 0, y0, H, plaster, name="pier")
    box(-0.3, y0, 2.75, 0, y1, H, plaster, name="lintel")
    vplane((-0.15, y0), (-0.15, y1), 0, 2.75, glass, "win")
    box(-0.3, y0 - 0.03, 0, -0.0, y0 + 0.03, 2.75, metal, name="wf")
    box(-0.3, y1 - 0.03, 0, -0.0, y1 + 0.03, 2.75, metal, name="wf")
    box(-0.3, y0, 1.85, -0.0, y1, 1.9, metal, name="wt")
    area((-0.35, (y0 + y1) / 2, 1.4), 1.4, 0.0, rot=(0, math.radians(-90), 0), size_y=2.8, portal=True, name="portal")
    prev = y1
box(-0.3, prev, 0, 0, Wd, H, plaster, name="pier")
# sheer curtains bunched at window sides
for (y0, y1) in openings:
    for yy in (y0 + 0.05, y1 - 0.35):
        box(0.05, yy, 0.02, 0.18, yy + 0.3, 2.7, sheer, 0.05, "curtain")
# wall panelling (back wall) + skirting
for i in range(0, 8):
    x = 0.6 + i * 1.3
    box(x, Wd - 0.03, 0.4, x + 1.1, Wd, 2.6, panel, 0.01, "moulding")
box(0, Wd - 0.04, 0, L, Wd, 0.12, panel, name="skirt")
# outside: garden greenery beyond windows
plane(-60, -40, -1, 60, -0.3, outside, "outground")
for i in range(14):
    round_tree(-38 - random.random() * 20, -20 + i * 4.0, -0.3, 7 + random.random() * 3, 3.0 + random.random())
for i in range(10):
    shrub(-4 - random.random() * 3, -2 + i * 1.2, -0.3, 0.6 + random.random() * 0.3)

# art + console on the front wall, rug under the dining table
box(3.0, 0.0, 1.15, 6.4, 0.04, 2.55, mat("canvas", (0.74, 0.66, 0.55), 0.95), name="bigart")
box(3.08, 0.04, 1.23, 6.32, 0.05, 2.47, mat_varied("paint", (0.55, 0.45, 0.35), (0.80, 0.72, 0.60), rough=0.9, scale=1.5, bump=0.2), name="paint")
box(3.2, 0.0, 0.0, 6.2, 0.45, 0.78, walnut, 0.01, "console")
box(2.0, 1.5, 0.0, 7.2, 5.3, 0.012, mat_varied("rug2", (0.60, 0.56, 0.50), (0.68, 0.64, 0.58), rough=1.0, scale=30, bump=0.1), name="rug2")
# dining set
box(2.6, 2.4, 0.72, 6.6, 4.4, 0.78, walnut, 0.01, "tabletop")
box(3.0, 3.0, 0.0, 3.3, 3.8, 0.72, walnut, 0.005, "leg1")
box(5.9, 3.0, 0.0, 6.2, 3.8, 0.72, walnut, 0.005, "leg2")
for x in (3.2, 4.6, 6.0):
    for side, yy in ((-1, 1.95), (1, 4.85)):
        box(x - 0.25, yy - 0.25, 0.45, x + 0.25, yy + 0.25, 0.52, chairfab, 0.04, "seat")
        by = yy - 0.25 if side == -1 else yy + 0.2
        box(x - 0.25, by, 0.52, x + 0.25, by + 0.05, 1.0, chairfab, 0.025, "back")
        for dx in (-0.21, 0.21):
            for dy in (-0.21, 0.21):
                box(x + dx - 0.015, yy + dy - 0.015, 0, x + dx + 0.015, yy + dy + 0.015, 0.45, bronze, name="cleg")
# table decor
cyl(4.6, 3.4, 0.78, 1.05, 0.11, mat("vase", (0.86, 0.84, 0.80), 0.25, coat=0.6), 32, "vase")
for i in range(5):
    o = sphere((4.6 + random.uniform(-0.15, 0.15), 3.4 + random.uniform(-0.15, 0.15), 1.25 + random.random() * 0.2), (0.18, 0.18, 0.16), foliage, sub=2, name="bouquet")
    displace(o, strength=0.08, size=0.05, seed=i)
# pendant: bronze ring with soft glow
bpy.ops.mesh.primitive_torus_add(major_radius=0.55, minor_radius=0.025, location=(4.6, 3.4, 2.1))
ring = bpy.context.active_object
ring.data.materials.append(bronze)
cyl(4.6, 3.4, 2.13, H, 0.003, metal, 6, "cable")
point((4.6, 3.4, 2.05), 18, (1.0, 0.8, 0.6), 0.4)
# sideboard + art on the back wall
box(7.6, Wd - 0.5, 0, 10.4, Wd - 0.05, 0.8, walnut, 0.01, "sideboard")
box(7.6, Wd - 0.5, 0.8, 10.4, Wd - 0.05, 0.84, marble, 0.005, "sbtop")
box(8.0, Wd - 0.06, 1.25, 10.0, Wd - 0.03, 2.45, mat("art", (0.70, 0.60, 0.48), 0.9), name="art")
box(8.05, Wd - 0.07, 1.3, 9.95, Wd - 0.055, 2.4, mat("art2", (0.52, 0.40, 0.30), 0.95), name="art2")
cyl(8.4, Wd - 0.25, 0.84, 1.3, 0.09, mat("ceramic", (0.20, 0.18, 0.16), 0.5), 32, "jar")
# lounge area to the right (rug, sofa)
box(7.0, 0.4, 0.0, 10.8, 3.4, 0.015, mat_varied("rug", (0.62, 0.58, 0.52), (0.70, 0.66, 0.60), rough=1.0, scale=30, bump=0.1), name="rug")
box(9.6, 0.6, 0.0, 10.7, 3.2, 0.42, fabric, 0.07, "sofa")
box(10.35, 0.6, 0.0, 10.75, 3.2, 0.82, fabric, 0.08, "sofab")
box(7.8, 1.4, 0.0, 8.8, 2.4, 0.38, marble, 0.01, "ctable")
cyl(1.0, 6.6, 0, 0.55, 0.28, mat("pot", (0.80, 0.76, 0.70), 0.7), 32, "pot")
for i in range(7):
    o = sphere((1.0 + random.uniform(-0.3, 0.3), 6.6 + random.uniform(-0.3, 0.3), 0.9 + i * 0.22), (0.42, 0.42, 0.38), foliage, sub=2, name="leaf")
    displace(o, strength=0.3, size=0.1, seed=i + 2)

sun(22, 262, strength=5.5, color=(1.0, 0.88, 0.72), angle=0.6)
sky(22, 262, strength=float(os.environ.get("SKYS","0.8")), air=1.0, aerosol=0.6, ozone=1.2)
sc.cycles.diffuse_bounces = 5
sc.cycles.samples = 64
sc.view_settings.exposure = float(os.environ.get("EXPO", "0.5"))

camera((10.4, 6.6, 1.35), (1.2, 2.6, 1.35), lens=24, shift_y=-0.02, dof=6.5, fstop=8)
out = f"/home/claude/render/out/residence_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=16 if PREVIEW else int(os.environ.get("SPP", "64")), pct=25 if PREVIEW else 100)
print("WROTE", out)
