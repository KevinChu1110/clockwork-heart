import os
import hashlib
from PIL import Image, ImageChops

REPO = "."
BASE = "game/assets/sprites/player/paperdoll"

# ---------------------------------------------------------
# 1. Check MD5 uniqueness and absence of forbidden files
# ---------------------------------------------------------
forbidden_files = [
    f"{BASE}/lion/head_unit/ear_rabbit_straight.png",
    f"{BASE}/lion/head_unit/gilded_mane.png",
    f"{BASE}/lion/weapon/wpn_dawn_blade.png",
    f"{BASE}/lion/weapon/knight_lance.png",
    f"{BASE}/lion/back_curio/curio_clockwork_pigeon.png",
    f"{BASE}/lion/back_curio/curio_lion_articulated_tail.png",
    f"{BASE}/lion/costume/costume_royal_guard.png",
    f"{BASE}/fox/weapon/astral_staff.png",
    f"{BASE}/rabbit/weapon/dawn_blade.png",
]

for f in forbidden_files:
    assert not os.path.exists(f), f"Forbidden file still exists: {f}"
print("✓ All forbidden and redundant files successfully deleted!")

# Check MD5 duplicates within slots across all 5 races
for race in ['rabbit', 'lion', 'fox', 'boar', 'macaque']:
    rdir = f"{BASE}/{race}"
    for slot in ["winding_key", "back_curio", "chassis", "head_unit", "costume", "optic_core", "weapon"]:
        sdir = f"{rdir}/{slot}"
        hashes = {}
        for fn in os.listdir(sdir):
            if fn.endswith(".png"):
                fp = os.path.join(sdir, fn)
                h = hashlib.md5(open(fp, "rb").read()).hexdigest()
                if h in hashes:
                    raise AssertionError(f"Duplicate MD5 in {race}/{slot}: {fn} and {hashes[h]}")
                hashes[h] = fn
print("✓ Zero duplicate MD5 hashes within any slot across all 5 races!")

# ---------------------------------------------------------
# 2. Check rabbit chassis soft shadow density & body solidness
# ---------------------------------------------------------
r_chassis = Image.open(f"{BASE}/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")
r_brass = Image.open(f"{BASE}/rabbit/chassis/paint_brass_gold.png").convert("RGBA")

# Shadow density
shadow_non_trans = 0
total_box = 0
for y in range(118, 124):
    for x in range(36, 93):
        total_box += 1
        p = r_chassis.getpixel((x, y))
        assert isinstance(p, tuple)
        if p[3] >= 60:
            shadow_non_trans += 1

shadow_density = shadow_non_trans / total_box
print(f"Rabbit ground soft shadow density: {shadow_non_trans}/{total_box} = {shadow_density*100:.1f}%")
assert shadow_density >= 0.85, f"Shadow density {shadow_density*100:.1f}% < 85%!"

# Single-layer flood fill hole helper
def count_single_layer_holes(im, threshold=30):
    w, h = im.size
    visited = [[False for _ in range(w)] for _ in range(h)]
    queue = []
    for y in range(h):
        for x in [0, w - 1]:
            p = im.getpixel((x, y))
            assert isinstance(p, tuple)
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                queue.append((x, y))
    for x in range(w):
        for y in [0, h - 1]:
            p = im.getpixel((x, y))
            assert isinstance(p, tuple)
            if p[3] < threshold and not visited[y][x]:
                visited[y][x] = True
                queue.append((x, y))
    while queue:
        cx, cy = queue.pop(0)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                p = im.getpixel((nx, ny))
                assert isinstance(p, tuple)
                if not visited[ny][nx] and p[3] < threshold:
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    holes = []
    for y in range(h):
        for x in range(w):
            p = im.getpixel((x, y))
            assert isinstance(p, tuple)
            if p[3] < threshold and not visited[y][x]:
                holes.append((x, y))
    return holes

ivory_chassis_holes = count_single_layer_holes(r_chassis)
brass_chassis_holes = count_single_layer_holes(r_brass)
print(f"Chassis single-layer holes (Rule 4c-6): ivory={len(ivory_chassis_holes)} px, brass={len(brass_chassis_holes)} px (origin/main was 4 px)")
assert len(ivory_chassis_holes) == 0, f"Ivory chassis holes > 0: {len(ivory_chassis_holes)}"
assert len(brass_chassis_holes) == 0, f"Brass chassis holes > 0: {len(brass_chassis_holes)}"
print("✓ Rabbit chassis (ivory & brass) single layer flood-fill holes = 0 px!")

# Check costume combinations (bare, steam_artisan, nutcracker_guard)
costume_options = [
    ("bare", None),
    ("steam_artisan", "costume_steam_artisan.png"),
    ("nutcracker_guard", "costume_nutcracker_guard.png"),
]
r_base = f"{BASE}/rabbit"
for cname, cfile in costume_options:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for slot, fn in [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_clockwork_pigeon.png"),
        ("chassis", "paint_ivory_stock.png"),
        ("head_unit", "ear_rabbit_straight.png"),
    ]:
        comp = Image.alpha_composite(comp, Image.open(f"{r_base}/{slot}/{fn}").convert("RGBA"))
    if cfile:
        comp = Image.alpha_composite(comp, Image.open(f"{r_base}/costume/{cfile}").convert("RGBA"))
    for slot, fn in [
        ("optic_core", "core_cyan_emerald.png"),
        ("weapon", "wpn_dawn_blade.png"),
    ]:
        comp = Image.alpha_composite(comp, Image.open(f"{r_base}/{slot}/{fn}").convert("RGBA"))
    choles = count_single_layer_holes(comp)
    print(f"Rabbit costume '{cname}' composite holes: {len(choles)} px")
    assert len(choles) == 0, f"Costume {cname} has {len(choles)} holes!"
print("✓ Rabbit costume combinations (bare, steam_artisan, nutcracker_guard) composite holes = 0 px!")

# ---------------------------------------------------------
# 3. Check live composite vs proof images for all 5 races
# ---------------------------------------------------------
race_slots = {
    "rabbit": [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_clockwork_pigeon.png"),
        ("chassis", "paint_ivory_stock.png"),
        ("head_unit", "ear_rabbit_straight.png"),
        ("costume", "costume_nutcracker_guard.png"),
        ("optic_core", "core_cyan_emerald.png"),
        ("weapon", "wpn_dawn_blade.png"),
    ],
    "lion": [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_lion_fan_tail.png"),
        ("chassis", "paint_brass_gold.png"),
        ("head_unit", "ear_lion_gilded_mane.png"),
        ("costume", "costume_nutcracker_guard.png"),
        ("optic_core", "core_amber_sun.png"),
        ("weapon", "wpn_knight_lance.png"),
    ],
    "fox": [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_fox_astral_tail.png"),
        ("chassis", "paint_fox_orange.png"),
        ("head_unit", "ear_fox_radar.png"),
        ("costume", "costume_astral_cape.png"),
        ("optic_core", "core_cyan_emerald.png"),
        ("weapon", "wpn_astral_staff.png"),
    ],
    "boar": [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_spring_tail.png"),
        ("chassis", "paint_ivory_stock.png"),
        ("head_unit", "ear_boar_rivet_cowl.png"),
        ("costume", "costume_viking_harness.png"),
        ("optic_core", "core_cyan_emerald.png"),
        ("weapon", "wpn_anvil_greathammer.png"),
    ],
    "macaque": [
        ("winding_key", "key_classic_brass.png"),
        ("back_curio", "curio_spring_tail.png"),
        ("chassis", "paint_ivory_stock.png"),
        ("head_unit", "ear_macaque_coaxial.png"),
        ("costume", "costume_dawn_monk_tunic.png"),
        ("optic_core", "core_cyan_emerald.png"),
        ("weapon", "wpn_spring_claws.png"),
    ],
}

bg_magenta = Image.new("RGBA", (128, 128), (255, 0, 255, 255))
for race, slots in race_slots.items():
    rdir = f"{BASE}/{race}"
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for slot, fn in slots:
        layer = Image.open(f"{rdir}/{slot}/{fn}").convert("RGBA")
        comp = Image.alpha_composite(comp, layer)
    
    proof_p = f"{rdir}/proof_paperdoll_{race}_composite.png"
    assert os.path.exists(proof_p), f"Missing proof composite for {race}"
    proof_im = Image.open(proof_p).convert("RGBA")
    diff = ImageChops.difference(comp, proof_im)
    assert diff.getbbox(alpha_only=False) is None, f"Proof mismatch for {race}: {diff.getbbox()}"

    mag_p = f"{rdir}/proof_paperdoll_{race}_magenta.png"
    if os.path.exists(mag_p):
        expected_mag = Image.alpha_composite(bg_magenta, comp)
        actual_mag = Image.open(mag_p).convert("RGBA")
        diff_m = ImageChops.difference(expected_mag, actual_mag)
        assert diff_m.getbbox(alpha_only=False) is None, f"Magenta mismatch for {race}: {diff_m.getbbox()}"

    print(f"  {race:10} proof diff bbox = None (0 px diff) | composite & magenta verified identical")

print("✓ All checks in comprehensive_paperdoll_check passed successfully!")
