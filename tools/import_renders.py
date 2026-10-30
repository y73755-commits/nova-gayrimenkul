"""Copies finished renders into src/assets/images with their site names (PNG masters).
Missing renders are temporarily filled with an existing image so the build never breaks."""
import os, shutil, sys
from PIL import Image
SRC = "/home/claude/render/out"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src/assets/images")
MAP = {
    "villa_desktop": "hero-villa-masaustu",
    "villa_mobile": "hero-villa-mobil",
    "villa_pool": "villa-havuz",
    "garden_main": "bahceli-mustakil",
    "penthouse_main": "penthouse-salon",
    "residence_main": "rezidans-ic-mekan",
    "plaza_main": "plaza-aksam",
    "lobby_main": "ofis-lobi",
    "homeoffice_main": "home-ofis",
    "detail_main": "malzeme-detay",
}
os.makedirs(DST, exist_ok=True)
fallback = os.path.join(SRC, "villa_pool.png")
missing = []
for src, dst in MAP.items():
    p = os.path.join(SRC, src + ".png")
    target = os.path.join(DST, dst + ".jpg")
    old_png = os.path.join(DST, dst + ".png")
    if os.path.exists(old_png):
        os.remove(old_png)
    src_file = p if os.path.exists(p) else fallback
    if not os.path.exists(p):
        missing.append(dst)
    # high-quality JPEG master (the build derives AVIF/WebP/JPG sizes from it)
    Image.open(src_file).convert("RGB").save(target, quality=92, optimize=True, progressive=True, subsampling=0)
print("missing (placeholder used):", missing or "none")
