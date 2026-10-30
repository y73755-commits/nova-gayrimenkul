"""Nova Gayrimenkul — procedural architectural scene toolkit (Blender/Cycles via bpy).

All geometry, materials and lighting are generated from code; no third-party
textures, photos or models are used, so every render is original.
"""
import bpy, bmesh, math, random, addon_utils
from mathutils import Vector

addon_utils.enable("cycles", default_set=True)

# ---------------------------------------------------------------- scene setup

def reset(seed=7):
    random.seed(seed)
    _mats.clear()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable("cycles", default_set=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    c = sc.cycles
    c.device = "CPU"
    c.samples = 64
    c.use_adaptive_sampling = True
    c.adaptive_threshold = 0.025
    c.use_denoising = True
    c.denoiser = "OPENIMAGEDENOISE"
    c.max_bounces = 8
    c.diffuse_bounces = 3
    c.glossy_bounces = 3
    c.transmission_bounces = 6
    c.transparent_max_bounces = 8
    c.volume_bounces = 0
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.blur_glossy = 1.0
    c.sample_clamp_indirect = 6.0
    sc.view_settings.view_transform = "AgX"
    for lk in ("AgX - Medium High Contrast", "Medium High Contrast"):
        try:
            sc.view_settings.look = lk
            break
        except TypeError:
            pass
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_depth = "8"
    sc.render.film_transparent = False
    sc.render.threads_mode = "AUTO"
    return sc


def render(path, w, h, samples=None, pct=100):
    sc = bpy.context.scene
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = pct
    if samples:
        sc.cycles.samples = samples
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob

# ---------------------------------------------------------------- materials

_mats = {}

def _principled(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    return m, p, m.node_tree


def mat(name, color=(0.8, 0.8, 0.8), rough=0.5, metal=0.0, **kw):
    key = name
    if key in _mats:
        return _mats[key]
    m, p, nt = _principled(name)
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    for k, v in kw.items():
        sock = {"coat": "Coat Weight", "coat_rough": "Coat Roughness", "sheen": "Sheen Weight",
                "transmission": "Transmission Weight", "ior": "IOR", "spec": "Specular IOR Level",
                "thin": "Thin Wall", "sss": "Subsurface Weight", "alpha": "Alpha"}[k]
        p.inputs[sock].default_value = v
    _mats[key] = m
    return m


def _noise(nt, scale=5.0, detail=6.0, rough=0.55, distortion=0.0, coord="Object"):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    n.inputs["Roughness"].default_value = rough
    n.inputs["Distortion"].default_value = distortion
    nt.links.new(tc.outputs[coord], n.inputs["Vector"])
    return n


def _ramp(nt, src, stops):
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    els[0].position, els[0].color = stops[0][0], (*stops[0][1], 1)
    els[1].position, els[1].color = stops[-1][0], (*stops[-1][1], 1)
    for pos, col in stops[1:-1]:
        e = els.new(pos)
        e.color = (*col, 1)
    nt.links.new(src, r.inputs["Fac"])
    return r


def _bump(nt, p, height_src, strength=0.1, dist=0.02):
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    b.inputs["Distance"].default_value = dist
    nt.links.new(height_src, b.inputs["Height"])
    nt.links.new(b.outputs["Normal"], p.inputs["Normal"])


def mat_varied(name, c1, c2, rough=0.6, scale=4.0, bump=0.05, detail=6.0, metal=0.0, coat=0.0):
    """Colour-varied surface (concrete, stone, plaster, foliage...)."""
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    n = _noise(nt, scale=scale, detail=detail)
    r = _ramp(nt, n.outputs["Fac"], [(0.3, c1), (0.7, c2)])
    nt.links.new(r.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    if bump:
        _bump(nt, p, n.outputs["Fac"], strength=bump)
    _mats[name] = m
    return m


def mat_wood(name="wood", dark=(0.20, 0.11, 0.05), light=(0.42, 0.25, 0.12), scale=3.0, rough=0.5, axis="Z", coat=0.0):
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    # stretch grain along an axis
    s = {"X": (0.15, 4, 4), "Y": (4, 0.15, 4), "Z": (4, 4, 0.15)}[axis]
    mp.inputs["Scale"].default_value = s
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    w = nt.nodes.new("ShaderNodeTexWave")
    w.wave_type = "RINGS"
    w.inputs["Scale"].default_value = scale
    w.inputs["Distortion"].default_value = 6.0
    w.inputs["Detail"].default_value = 3.0
    w.inputs["Detail Scale"].default_value = 1.5
    nt.links.new(mp.outputs["Vector"], w.inputs["Vector"])
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 18.0
    nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "FLOAT"
    mix.inputs[0].default_value = 0.35
    nt.links.new(w.outputs["Fac"], mix.inputs[2])
    nt.links.new(n.outputs["Fac"], mix.inputs[3])
    r = _ramp(nt, mix.outputs[0], [(0.25, dark), (0.55, light), (0.8, dark)])
    nt.links.new(r.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Coat Roughness"].default_value = 0.15
    _bump(nt, p, mix.outputs[0], strength=0.04)
    _mats[name] = m
    return m


def mat_marble(name="marble", base=(0.86, 0.85, 0.82), vein=(0.42, 0.40, 0.38), scale=1.6, rough=0.12, coat=0.4):
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    n = _noise(nt, scale=scale, detail=12.0, rough=0.62, distortion=3.2)
    w = nt.nodes.new("ShaderNodeTexWave")
    w.inputs["Scale"].default_value = 1.2
    w.inputs["Distortion"].default_value = 9.0
    w.inputs["Detail"].default_value = 8.0
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], w.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "FLOAT"
    mix.inputs[0].default_value = 0.5
    nt.links.new(n.outputs["Fac"], mix.inputs[2])
    nt.links.new(w.outputs["Fac"], mix.inputs[3])
    r = _ramp(nt, mix.outputs[0], [(0.0, base), (0.46, base), (0.5, vein), (0.54, base), (1.0, (base[0]*0.94, base[1]*0.93, base[2]*0.9))])
    nt.links.new(r.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Coat Roughness"].default_value = 0.05
    _mats[name] = m
    return m


def mat_glass(name="glass", tint=(0.92, 0.96, 0.96), rough=0.0, thin=True):
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    p.inputs["Base Color"].default_value = (*tint, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Transmission Weight"].default_value = 1.0
    p.inputs["IOR"].default_value = 1.5
    p.inputs["Thin Wall"].default_value = bool(thin)
    _mats[name] = m
    return m


def mat_water(name="water", tint=(0.70, 0.90, 0.92), wave_scale=2.0, strength=0.12):
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    p.inputs["Base Color"].default_value = (*tint, 1)
    p.inputs["Roughness"].default_value = 0.015
    p.inputs["Transmission Weight"].default_value = 1.0
    p.inputs["IOR"].default_value = 1.333
    n = _noise(nt, scale=wave_scale, detail=4.0, rough=0.5, coord="Object")
    _bump(nt, p, n.outputs["Fac"], strength=strength, dist=0.05)
    _mats[name] = m
    return m


def mat_sea(name="sea", color=(0.015, 0.05, 0.07), scale=0.08, strength=0.25):
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = 0.06
    p.inputs["Specular IOR Level"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, 3.0, 1.0)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = 10.0
    nt.links.new(mp.outputs["Vector"], n.inputs["Vector"])
    _bump(nt, p, n.outputs["Fac"], strength=strength, dist=0.4)
    _mats[name] = m
    return m


def mat_emit(name, color=(1.0, 0.78, 0.52), strength=8.0):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*color, 1)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs[0], out.inputs[0])
    _mats[name] = m
    return m


def mat_windows(name="citywin", base=(0.03, 0.035, 0.045), lit=(1.0, 0.72, 0.42), strength=3.0, density=0.45, scale=(0.33, 0.33, 0.08), cell=(1.5, 1.5, 0.25), rough=0.3, glow=0.0):
    """Building facade with a grid of randomly lit windows (for distant city / towers)."""
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    p.inputs["Base Color"].default_value = (*base, 1)
    p.inputs["Roughness"].default_value = rough
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    # window cells: brick texture gives a mortar/cell mask
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Mortar Size"].default_value = 0.05
    br.inputs["Color1"].default_value = (1, 1, 1, 1)
    br.inputs["Color2"].default_value = (1, 1, 1, 1)
    br.inputs["Mortar"].default_value = (0, 0, 0, 1)
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = 0.5
    br.inputs["Row Height"].default_value = 0.25
    nt.links.new(mp.outputs["Vector"], br.inputs["Vector"])
    # random on/off per cell via cellular noise
    vo = nt.nodes.new("ShaderNodeTexWhiteNoise")
    vo.noise_dimensions = "3D"
    fl = nt.nodes.new("ShaderNodeVectorMath")
    fl.operation = "SNAP"
    fl.inputs[1].default_value = cell
    nt.links.new(mp.outputs["Vector"], fl.inputs[0])
    nt.links.new(fl.outputs[0], vo.inputs["Vector"])
    gt = nt.nodes.new("ShaderNodeMath")
    gt.operation = "GREATER_THAN"
    gt.inputs[1].default_value = 1.0 - density
    nt.links.new(vo.outputs["Value"], gt.inputs[0])
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(br.outputs["Fac"], inv.inputs[1])
    # unlit windows keep a faint glow (glow fraction) so facades read as occupied buildings, not dominoes
    lift = nt.nodes.new("ShaderNodeMapRange")
    lift.inputs["From Min"].default_value = 0.0
    lift.inputs["From Max"].default_value = 1.0
    lift.inputs["To Min"].default_value = glow
    lift.inputs["To Max"].default_value = 1.0
    nt.links.new(gt.outputs[0], lift.inputs["Value"])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(lift.outputs[0], mul.inputs[0])
    nt.links.new(inv.outputs[0], mul.inputs[1])
    mul2 = nt.nodes.new("ShaderNodeMath")
    mul2.operation = "MULTIPLY"
    mul2.inputs[1].default_value = strength
    nt.links.new(mul.outputs[0], mul2.inputs[0])
    # slight per-window colour temperature variation
    cr = _ramp(nt, vo.outputs["Value"], [(0.0, (1.0, 0.86, 0.66)), (1.0, lit)])
    nt.links.new(cr.outputs["Color"], p.inputs["Emission Color"])
    nt.links.new(mul2.outputs[0], p.inputs["Emission Strength"])
    _mats[name] = m
    return m

# ---------------------------------------------------------------- geometry

def _obj(name, bm, material=None, smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for poly in me.polygons:
            poly.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    link(ob)
    if material:
        ob.data.materials.append(material)
    return ob


def box(x0, y0, z0, x1, y1, z1, material=None, bevel=0.0, name="box"):
    """Axis-aligned box from bounds (metres)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    sx, sy, sz = abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)
    for v in bm.verts:
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz
    ob = _obj(name, bm, material)
    ob.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    if bevel:
        md = ob.modifiers.new("bevel", "BEVEL")
        md.width = bevel
        md.segments = 2
        md.limit_method = "ANGLE"
    return ob


def plane(x0, y0, x1, y1, z=0.0, material=None, name="plane"):
    bm = bmesh.new()
    vs = [bm.verts.new((x0, y0, z)), bm.verts.new((x1, y0, z)), bm.verts.new((x1, y1, z)), bm.verts.new((x0, y1, z))]
    bm.faces.new(vs)
    return _obj(name, bm, material)


def vplane(p0, p1, z0, z1, material=None, name="vplane"):
    """Vertical rectangle between two XY points (glass panes, walls)."""
    bm = bmesh.new()
    a = bm.verts.new((p0[0], p0[1], z0))
    b = bm.verts.new((p1[0], p1[1], z0))
    c = bm.verts.new((p1[0], p1[1], z1))
    d = bm.verts.new((p0[0], p0[1], z1))
    bm.faces.new((a, b, c, d))
    return _obj(name, bm, material)


def cyl(x, y, z0, z1, r, material=None, seg=32, name="cyl"):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    ob = _obj(name, bm, material, smooth=True)
    ob.location = (x, y, (z0 + z1) / 2)
    return ob


def sphere(loc, scale, material=None, sub=3, name="sph", smooth=True):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
    ob = _obj(name, bm, material, smooth=smooth)
    ob.location = loc
    ob.scale = scale
    return ob


def displace(ob, strength=0.2, size=0.5, seed=0, subsurf=1):
    if subsurf:
        s = ob.modifiers.new("sub", "SUBSURF")
        s.levels = subsurf
        s.render_levels = subsurf
    tex = bpy.data.textures.new(f"cl{seed}{ob.name}", "CLOUDS")
    tex.noise_scale = size
    tex.noise_depth = 3
    d = ob.modifiers.new("disp", "DISPLACE")
    d.texture = tex
    d.strength = strength
    d.mid_level = 0.5
    d.texture_coords = "GLOBAL" if seed == 0 else "OBJECT"
    return ob


def cypress(x, y, z=0.0, h=6.0, r=0.6, foliage=None, seed=0):
    foliage = foliage or mat_varied("foliage_dark", (0.012, 0.03, 0.010), (0.035, 0.060, 0.020), rough=0.8, scale=9, bump=0.45)
    t = sphere((x, y, z + h * 0.5 + 0.15), (r, r, h * 0.5), foliage, sub=3, name="cypress")
    displace(t, strength=0.22 * r / 0.6, size=0.18 + random.random() * 0.05, seed=seed)
    cyl(x, y, z, z + 0.4, 0.08, mat("trunk", (0.12, 0.08, 0.05), 0.9))
    return t


def round_tree(x, y, z=0.0, h=4.5, r=1.6, foliage=None, n=5):
    foliage = foliage or mat_varied("foliage", (0.025, 0.05, 0.015), (0.07, 0.10, 0.035), rough=0.75, scale=7, bump=0.4)
    cyl(x, y, z, z + h * 0.62, 0.11, mat("trunk", (0.12, 0.08, 0.05), 0.9))
    for i in range(n):
        a = random.random() * math.tau
        d = random.random() * r * 0.45
        s = r * (0.55 + random.random() * 0.35)
        o = sphere((x + math.cos(a) * d, y + math.sin(a) * d, z + h * 0.7 + random.random() * r * 0.5), (s, s, s * 0.8), foliage, sub=3, name="crown")
        displace(o, strength=0.35 * s, size=0.25, seed=i + 1)


def shrub(x, y, z=0.0, r=0.5, foliage=None):
    foliage = foliage or mat_varied("shrub", (0.02, 0.05, 0.015), (0.06, 0.09, 0.03), rough=0.75, scale=10, bump=0.4)
    o = sphere((x, y, z + r * 0.55), (r, r, r * 0.7), foliage, sub=3, name="shrub")
    displace(o, strength=0.18 * r / 0.5, size=0.12, seed=7)
    return o


def lounger(x, y, rot=0.0, frame=None, cushion=None):
    frame = frame or mat("teak", (0.30, 0.18, 0.09), 0.55)
    cushion = cushion or mat("cushion", (0.85, 0.82, 0.76), 0.95, sheen=0.4)
    parts = [box(-0.33, -1.0, 0.0, 0.33, 1.0, 0.28, frame, 0.015),
             box(-0.3, -0.95, 0.28, 0.3, 0.4, 0.36, cushion, 0.04)]
    back = box(-0.3, 0.0, 0.0, 0.3, 0.08, 0.7, cushion, 0.04)
    back.location = (0, 0.55, 0.42)
    back.rotation_euler = (math.radians(-35), 0, 0)
    parts.append(back)
    for o in parts:
        o.location = Vector(o.location)
        v = o.location.copy()
        c, s = math.cos(rot), math.sin(rot)
        o.location = (x + v.x * c - v.y * s, y + v.x * s + v.y * c, v.z)
        o.rotation_euler[2] += rot
    return parts

# ---------------------------------------------------------------- lights, world, camera

def sun(elev_deg, azim_deg, strength=3.0, color=(1.0, 0.85, 0.65), angle=1.2):
    ld = bpy.data.lights.new("sun", "SUN")
    ld.energy = strength
    ld.color = color
    ld.angle = math.radians(angle)
    ob = bpy.data.objects.new("sun", ld)
    link(ob)
    # azimuth convention matches the sky texture: 0 = +Y, 90 = +X (clockwise seen from above)
    ob.rotation_euler = (math.radians(90 - elev_deg), 0, math.radians(180 - azim_deg))
    return ob


def area(loc, size, energy, color=(1.0, 0.78, 0.55), rot=(0, 0, 0), shape="RECTANGLE", size_y=None, portal=False, name="area"):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.color = color
    ld.shape = shape
    ld.size = size
    if size_y:
        ld.size_y = size_y
    if portal:
        try:
            ld.cycles.is_portal = True
        except Exception:
            pass
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = rot
    try:
        ob.visible_glossy = False
        ob.visible_camera = False
        ob.visible_transmission = False
    except Exception:
        pass
    link(ob)
    return ob


def point(loc, energy, color=(1.0, 0.75, 0.5), radius=0.05):
    ld = bpy.data.lights.new("pt", "POINT")
    ld.energy = energy
    ld.color = color
    ld.shadow_soft_size = radius
    ob = bpy.data.objects.new("pt", ld)
    ob.location = loc
    link(ob)
    return ob


def sky(elev_deg, azim_deg, strength=0.35, air=1.0, aerosol=1.0, ozone=1.0, sun_disc=False, extra_tint=None):
    w = bpy.data.worlds.new("world")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    s = nt.nodes.new("ShaderNodeTexSky")
    s.sky_type = "MULTIPLE_SCATTERING"
    s.sun_disc = sun_disc
    for prop, val in (("sun_elevation", math.radians(elev_deg)), ("sun_rotation", math.radians(azim_deg)),
                      ("air_density", air), ("aerosol_density", aerosol), ("ozone_density", ozone),
                      ("dust_density", aerosol)):
        if hasattr(s, prop):
            setattr(s, prop, val)
    if extra_tint:
        mix = nt.nodes.new("ShaderNodeMixRGB")
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[2].default_value = (*extra_tint, 1)
        nt.links.new(s.outputs[0], mix.inputs[1])
        nt.links.new(mix.outputs[0], bg.inputs[0])
    else:
        nt.links.new(s.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength
    return w


def camera(loc, target, lens=28, shift_x=0.0, shift_y=0.0, dof=None, fstop=4.0, level=True):
    cd = bpy.data.cameras.new("cam")
    cd.lens = lens
    cd.shift_x = shift_x
    cd.shift_y = shift_y
    cd.clip_end = 6000
    cd.clip_start = 0.05
    ob = bpy.data.objects.new("cam", cd)
    link(ob)
    ob.location = loc
    t = Vector(target)
    if level:
        # architectural two-point perspective: keep verticals vertical, use shift instead of tilt
        t = Vector((t.x, t.y, loc[2]))
    d = t - Vector(loc)
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    if dof:
        cd.dof.use_dof = True
        cd.dof.focus_distance = dof
        cd.dof.aperture_fstop = fstop
    bpy.context.scene.camera = ob
    return ob


def mat_paving(name="paving", c1=(0.70, 0.63, 0.52), c2=(0.80, 0.74, 0.63), w=1.2, h=0.6, rough=0.7):
    """Large-format stone pavers with recessed joints."""
    if name in _mats:
        return _mats[name]
    m, p, nt = _principled(name)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.5
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Brick Width"].default_value = w
    br.inputs["Row Height"].default_value = h
    br.inputs["Mortar Size"].default_value = 0.006
    br.inputs["Color1"].default_value = (*c1, 1)
    br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (c1[0]*0.6, c1[1]*0.6, c1[2]*0.6, 1)
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 6.0
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMixRGB")
    mix.blend_type = "OVERLAY"
    mix.inputs[0].default_value = 0.25
    nt.links.new(br.outputs["Color"], mix.inputs[1])
    nt.links.new(n.outputs["Color"], mix.inputs[2])
    nt.links.new(mix.outputs[0], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(br.outputs["Fac"], inv.inputs[1])
    _bump(nt, p, inv.outputs[0], strength=0.35, dist=0.01)
    _mats[name] = m
    return m


def mat_window_glass(name="winglass", reflect=0.08):
    """Arch-viz window glass: transparent to shadow rays (lets sun in) + fresnel reflection."""
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    tr.inputs["Color"].default_value = (0.96, 0.98, 0.98, 1)
    gl = nt.nodes.new("ShaderNodeBsdfGlossy")
    gl.inputs["Roughness"].default_value = 0.0
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = reflect
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lw.outputs["Fresnel"], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(gl.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    _mats[name] = m
    return m
