"""Scene 7 — home office with a view over water and hills, morning light."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nova3d import *

SHOT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "main"
PREVIEW = "--preview" in sys.argv
sc = reset(seed=14)

oak = mat_wood("oak", dark=(0.38, 0.25, 0.14), light=(0.58, 0.42, 0.26), axis="X", rough=0.4, coat=0.15)
desktop = mat_wood("desktop", dark=(0.28, 0.17, 0.09), light=(0.46, 0.30, 0.16), axis="X", rough=0.35, coat=0.3)
plaster = mat_varied("plaster", (0.84, 0.82, 0.78), (0.88, 0.86, 0.82), rough=0.9, scale=5, bump=0.01)
metal = mat("frame", (0.03, 0.03, 0.032), 0.35, 1.0)
bronze = mat("bronze", (0.52, 0.38, 0.22), 0.3, 1.0)
glass = mat_window_glass("winglass", reflect=0.1)
leather = mat("leather", (0.20, 0.11, 0.06), 0.45, coat=0.2)
laptop = mat("laptop", (0.55, 0.56, 0.58), 0.3, 1.0)
screen = mat_emit("screen", (0.75, 0.80, 0.88), 0.8)
sea = mat_sea("sea", color=(0.03, 0.09, 0.12), scale=0.05, strength=0.2)
hills = mat_varied("hills", (0.10, 0.16, 0.08), (0.16, 0.22, 0.12), rough=1.0, scale=0.01, bump=0.0)
farhills = mat("farhills", (0.24, 0.30, 0.36), 1.0)
foliage = mat_varied("plant", (0.03, 0.08, 0.025), (0.08, 0.14, 0.05), rough=0.6, scale=8, bump=0.3)

# room: 6 x 5 x 3 m; big corner window at y = 5 (view) and partial at x = 6
box(0, 0, -0.2, 6, 5, 0, oak, name="floor")
box(0, 0, 3.0, 6, 5, 3.2, plaster, name="ceiling")
box(-0.2, 0, 0, 0, 5, 3.0, plaster, name="wallL")
box(0, -0.2, 0, 6, 0, 3.0, plaster, name="wallB")
box(0, 5, 0, 0.6, 5.2, 3.0, plaster, name="pierL")
box(0, 5, 0, 6, 5.2, 0.45, plaster, name="sill")
vplane((0.6, 5.1), (6.0, 5.1), 0.45, 3.0, glass, "win")
vplane((6.1, 1.5), (6.1, 5.2), 0.45, 3.0, glass, "win2")
box(6.0, 0, 0, 6.2, 1.5, 3.0, plaster, name="wallR")
box(6.0, 1.5, 0, 6.2, 5.2, 0.45, plaster, name="sillR")
box(6.05, 5.05, 0.45, 6.15, 5.15, 3.0, metal, name="corner")
for x in (2.4, 4.2):
    box(x - 0.025, 5.07, 0.45, x + 0.025, 5.13, 3.0, metal, name="mull")
area((3.3, 5.4, 1.7), 5.4, 0.0, rot=(math.radians(90), 0, 0), size_y=2.6, portal=True, name="portal1")
area((6.4, 3.35, 1.7), 3.7, 0.0, rot=(0, math.radians(90), 0), size_y=2.6, portal=True, name="portal2")

# landscape outside: house sits on a slope above water
plane(-500, 5.2, 500, 60, -8, hills, "slope")
plane(-3000, 60, 3000, 3000, -40, sea, "sea")
for (x, y, sx, sy, sz) in [(-900, 1600, 900, 300, 140), (300, 1900, 800, 300, 190), (1500, 1500, 700, 300, 120)]:
    sphere((x, y, -40), (sx, sy, sz), farhills, sub=4, name="far")
for i in range(18):
    round_tree(-40 + i * 5 + random.random() * 3, 14 + random.random() * 30, -8, 6 + random.random() * 3, 2 + random.random(), n=5)
for i in range(6):
    cypress(-10 + i * 6 + random.random() * 2, 9 + random.random() * 4, -8, 10 + random.random() * 4, 0.8, seed=i)

# desk facing the window
box(1.6, 3.7, 0.74, 4.6, 4.5, 0.78, desktop, 0.008, "desk")
for (x, y) in ((1.7, 3.8), (4.5, 3.8), (1.7, 4.4), (4.5, 4.4)):
    box(x - 0.02, y - 0.02, 0, x + 0.02, y + 0.02, 0.74, metal, name="leg")
box(2.5, 3.95, 0.78, 3.4, 4.35, 0.795, laptop, 0.004, "laptopbase")
lt = box(2.5, 4.33, 0.78, 3.4, 4.345, 1.36, laptop, 0.004, "lid")
lt.rotation_euler = (math.radians(-12), 0, 0)
sc_ = box(2.53, 4.325, 0.81, 3.37, 4.328, 1.33, screen, name="screen")
sc_.rotation_euler = (math.radians(-12), 0, 0)
cyl(4.1, 4.2, 0.78, 1.25, 0.012, bronze, 8, "lampstem")
cyl(4.1, 4.2, 1.25, 1.4, 0.13, mat_emit("lamphead", (1.0, 0.8, 0.55), 2.0), 32, "lamphead")
cyl(1.95, 4.1, 0.78, 0.9, 0.05, mat("cup", (0.9, 0.88, 0.84), 0.3), 32, "cup")
box(3.6, 3.85, 0.78, 3.95, 4.15, 0.80, mat("notebook", (0.25, 0.20, 0.15), 0.8), 0.003, "notebook")
# chair
box(2.6, 2.8, 0.45, 3.4, 3.5, 0.55, leather, 0.05, "seat")
box(2.6, 2.75, 0.55, 3.4, 2.85, 1.15, leather, 0.04, "back")
cyl(3.0, 3.15, 0.1, 0.45, 0.03, metal, 12, "post")
cyl(3.0, 3.15, 0.0, 0.1, 0.3, metal, 24, "base")
# shelf on the left wall with books
box(0.0, 1.0, 0.0, 0.4, 3.6, 2.2, oak, 0.01, "shelf_case")
for z in (0.55, 1.1, 1.65):
    box(0.02, 1.05, z, 0.38, 3.55, z + 0.03, oak, name="shelf")
    x = 1.1
    while x < 3.4:
        w = random.uniform(0.03, 0.06)
        h = random.uniform(0.22, 0.32)
        col = random.choice([(0.55, 0.50, 0.42), (0.20, 0.18, 0.16), (0.70, 0.66, 0.58), (0.35, 0.22, 0.14)])
        box(0.05, x, z + 0.03, 0.3, x + w, z + 0.03 + h, mat(f"book{col}", col, 0.8), name="book")
        x += w + 0.005
        if random.random() < 0.08:
            x += 0.25
# plant
cyl(5.3, 0.8, 0, 0.5, 0.25, mat("pot", (0.75, 0.70, 0.64), 0.7), 32, "pot")
for i in range(6):
    o = sphere((5.3 + random.uniform(-0.25, 0.25), 0.8 + random.uniform(-0.25, 0.25), 0.8 + i * 0.2), (0.38, 0.38, 0.32), foliage, sub=2, name="leaf")
    displace(o, strength=0.28, size=0.1, seed=i + 1)
box(1.0, 1.0, 0.0, 5.0, 3.6, 0.012, mat_varied("rug", (0.40, 0.35, 0.29), (0.46, 0.41, 0.35), rough=1.0, scale=30, bump=0.1), name="rug")

sun(20, 70, strength=4.0, color=(1.0, 0.88, 0.72), angle=0.7)
sky(20, 70, strength=0.42, air=1.0, aerosol=0.5, ozone=1.3, extra_tint=(0.85, 0.92, 1.0))
sc.cycles.diffuse_bounces = 4
sc.view_settings.exposure = float(os.environ.get("EXPO", "-0.35"))

camera((0.75, 0.6, 1.35), (4.3, 4.8, 1.35), lens=20, shift_y=-0.03, dof=4.0, fstop=5.6)
out = f"/home/claude/render/out/homeoffice_{SHOT}{'_prev' if PREVIEW else ''}.png"
render(out, 1600, 1067, samples=12 if PREVIEW else int(os.environ.get("SPP", "56")), pct=25 if PREVIEW else 100)
print("WROTE", out)
