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

# Check torso/pelvis solidness (where diagonal cut used to be: y=73..95, x=45..70)
for y in range(73, 96):
    for x in range(45, 71):
        c = r_chassis.getpixel((x, y))
        assert isinstance(c, tuple)
        assert c[3] > 0, f"Void found inside rabbit torso/pelvis at ({x}, {y})!"
print("✓ Rabbit chassis lower body / pelvis / thigh is 100% solid with zero cut/gap!")

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

hole_stats = {}
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

    # Flood fill hole check
    w, h = 128, 128
    visited = [[False for _ in range(w)] for _ in range(h)]
    queue: list[tuple[int, int]] = []
    for y in range(h):
        for x in [0, w - 1]:
            c = comp.getpixel((x, y))
            assert isinstance(c, tuple)
            if c[3] == 0 and not visited[y][x]:
                visited[y][x] = True
                queue.append((x, y))
    for x in range(w):
        for y in [0, h - 1]:
            c = comp.getpixel((x, y))
            assert isinstance(c, tuple)
            if c[3] == 0 and not visited[y][x]:
                visited[y][x] = True
                queue.append((x, y))
    while queue:
        cx, cy = queue.pop(0)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                c = comp.getpixel((nx, ny))
                assert isinstance(c, tuple)
                if not visited[ny][nx] and c[3] == 0:
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    holes = []
    for y in range(h):
        for x in range(w):
            c = comp.getpixel((x, y))
            assert isinstance(c, tuple)
            if c[3] == 0 and not visited[y][x]:
                holes.append((x, y))
    hole_stats[race] = len(holes)
    print(f"  {race:10} proof diff bbox = None (0 px diff) | composite holes = {len(holes)} px")

print(f"\nHole statistics summary: {hole_stats}")
assert hole_stats["rabbit"] == 57, f"Unexpected rabbit holes: {hole_stats['rabbit']}"
assert hole_stats["macaque"] == 0, f"Unexpected macaque holes: {hole_stats['macaque']}"
assert hole_stats["boar"] == 38, f"Unexpected boar holes: {hole_stats['boar']}"
assert hole_stats["fox"] == 19, f"Unexpected fox holes: {hole_stats['fox']}"
assert hole_stats["lion"] == 85, f"Unexpected lion holes: {hole_stats['lion']}"
print("✓ All 5 races hole numbers match verified QA baselines perfectly!")
