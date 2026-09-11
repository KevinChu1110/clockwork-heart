import os
import sys
from typing import cast
from PIL import Image, ImageChops

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

# Let's test hit body with rotate(+14) and rotate(-14)
large_hit = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
large_hit.paste(body_clean, (64, 64))

# Let's test with rotate(14)
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit_pos14 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit_pos14.paste(rot_pos14, (-64, -64), rot_pos14)

# Let's test with rotate(-14)
rot_neg14 = large_hit.rotate(-14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit_neg14 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit_neg14.paste(rot_neg14, (-64, -64), rot_neg14)

os.makedirs("/tmp/fox_hit_candidates", exist_ok=True)

# Let's try different candidate (deg, target_hand) on body_hit_pos14
candidates = [
    ("pos14_deg-65_h96_64", 14, -65, (96, 64)),
    ("pos14_deg-70_h98_60", 14, -70, (98, 60)),
    ("pos14_deg-60_h96_58", 14, -60, (96, 58)),
    ("pos14_deg-75_h98_62", 14, -75, (98, 62)),
    ("pos14_deg-65_h94_70", 14, -65, (94, 70)),
    ("pos14_deg-55_h95_55", 14, -55, (95, 55)),
    ("neg14_deg-65_h96_64", -14, -65, (96, 64)),
    ("neg14_deg-70_h98_60", -14, -70, (98, 60)),
]

for name, rot_body, deg, hand in candidates:
    if rot_body == 14:
        b_img = body_hit_pos14
        shadow = build_contact_shadow(cx=48, cy=119, rx=34, ry=5, blur=0.6)
    else:
        b_img = body_hit_neg14
        shadow = build_contact_shadow(cx=52, cy=119, rx=34, ry=5, blur=0.6)
        
    staff = place_rigid_staff(clean_staff, deg=deg, target_hand=hand)
    
    # Check bbox and clipping
    s_bbox = staff.getbbox()
    
    # Composite
    comp = Image.alpha_composite(shadow, b_img)
    comp = Image.alpha_composite(comp, staff)
    
    comp.save(f"/tmp/fox_hit_candidates/{name}.png")
    print(f"Candidate {name}: staff_bbox={s_bbox}, comp_bbox={comp.getbbox()}")

print("Saved all candidates.")
