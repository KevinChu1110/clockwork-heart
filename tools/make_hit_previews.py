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

large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))

# Rotate +14 (counter-clockwise backward recoil)
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_pos14 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_pos14.paste(rot_pos14, (-64, -64), rot_pos14)

# Shadow for backward recoil
shadow = build_contact_shadow(cx=50, cy=119, rx=34, ry=5, blur=0.6)

# Test combinations:
# 1. deg=-65, target_hand=(82, 55)
# 2. deg=-65, target_hand=(84, 58)
# 3. deg=-70, target_hand=(82, 58)
# 4. deg=-60, target_hand=(80, 55)
# 5. deg=-70, target_hand=(80, 52)
# 6. deg=-65, target_hand=(80, 52)

os.makedirs("/tmp/hit_preview", exist_ok=True)
combos = [
    ("v1_deg-65_h82_55", -65, (82, 55), 1.0),
    ("v2_deg-65_h84_58", -65, (84, 58), 0.98),
    ("v3_deg-70_h82_58", -70, (82, 58), 0.98),
    ("v4_deg-60_h80_55", -60, (80, 55), 1.0),
    ("v5_deg-70_h80_52", -70, (80, 52), 1.0),
    ("v6_deg-65_h80_52", -65, (80, 52), 1.0),
]

for name, deg, hand, scale in combos:
    staff = place_rigid_staff(clean_staff, deg=deg, target_hand=hand, scale=scale)
    comp = Image.alpha_composite(shadow, body_pos14)
    comp = Image.alpha_composite(comp, staff)
    comp.save(f"/tmp/hit_preview/{name}.png")
    
    # Calculate clipping
    cpx = comp.load()
    assert cpx is not None
    x0 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], cpx[0, y])[3] > 0)
    x127 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], cpx[127, y])[3] > 0)
    y0 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], cpx[x, 0])[3] > 0)
    y127 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], cpx[x, 127])[3] > 0)
    print(f"{name}: bbox={comp.getbbox()}, x0={x0}, x127={x127}, y0={y0}, y127={y127}")
