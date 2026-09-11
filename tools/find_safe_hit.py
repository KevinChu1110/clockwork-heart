import os
import sys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)

from tools.generate_fox_combat_poses import place_rigid_staff, build_contact_shadow

staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")

clean_staff = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = staff_src.load()
cs_px = clean_staff.load()
assert s_px is not None and cs_px is not None
for y in range(128):
    for x in range(128):
        if 80 <= x <= 112 and 38 <= y <= 125:
            cs_px[x, y] = cast(tuple[int, int, int, int], s_px[x, y])

b_px = body_clean.load()
assert b_px is not None
for y in range(112, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], b_px[x, y])
        if p[3] > 0:
            is_solid_paw = (46 <= x <= 58 or 69 <= x <= 80) and y <= 122 and p[0] < 125 and p[1] < 105 and p[2] < 80
            if not is_solid_paw:
                b_px[x, y] = (0, 0, 0, 0)

# Rotate +14 (counter-clockwise = tilts backward to the left)
large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_pos14 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_pos14.paste(rot_pos14, (-64, -64), rot_pos14)

print("body_pos14 bbox:", body_pos14.getbbox())

# Let's search over (deg, hx, hy)
# Deg around -55 .. -75
# We want staff right edge <= 125, left edge >= 2, top edge >= 2, bottom edge <= 125
b_px_pos = body_pos14.load()
assert b_px_pos is not None

def evaluate(deg, hx, hy, scale=1.0):
    bpx = body_pos14.load()
    assert bpx is not None
    st = place_rigid_staff(clean_staff, deg=deg, target_hand=(hx, hy), scale=scale)
    bbox = st.getbbox()
    if not bbox:
        return None
    # Boundary safety
    if bbox[0] <= 1 or bbox[1] <= 1 or bbox[2] >= 127 or bbox[3] >= 127:
        return None
    
    st_px = st.load()
    assert st_px is not None
    
    total = 0
    outside = 0
    boundary = 0
    for y in range(128):
        for x in range(128):
            sp = cast(tuple[int,int,int,int], st_px[x, y])
            if sp[3] > 60:
                total += 1
                bp = cast(tuple[int,int,int,int], bpx[x, y])
                if bp[3] <= 60:
                    outside += 1
                else:
                    # check if bp is near edge of body
                    is_edge = False
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 128 and 0 <= ny < 128:
                                n_p = cast(tuple[int,int,int,int], bpx[nx, ny])
                                if n_p[3] <= 60:
                                    is_edge = True
                                    break
                    if is_edge:
                        boundary += 1
                        
    out_pct = outside / total * 100.0
    bound_pct = boundary / total * 100.0
    return (out_pct, bound_pct, bbox, deg, hx, hy, scale)

valid = []
for deg in range(-75, -45, 5):
    for hx in range(70, 105):
        for hy in range(45, 75):
            for scale in [0.92, 0.95, 0.98, 1.0]:
                ev = evaluate(deg, hx, hy, scale)
                if ev:
                    valid.append(ev)

print(f"Total safe configurations: {len(valid)}")
# Sort by outside % + boundary %
valid.sort(key=lambda x: (x[0] + x[1]), reverse=True)
for v in valid[:20]:
    print(f"deg={v[3]}, hand=({v[4]}, {v[5]}), scale={v[6]} -> outside={v[0]:.1f}%, boundary={v[1]:.1f}%, bbox={v[2]}")
