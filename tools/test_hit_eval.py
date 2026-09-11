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

# Shadow for +14 recoil (shifted slightly left to cx=52)
shadow = build_contact_shadow(cx=52, cy=119, rx=34, ry=5, blur=0.6)

test_configs = [
    ("hit_pos14_deg-60_h90_58", -60, (90, 58), 0.98),
    ("hit_pos14_deg-65_h90_60", -65, (90, 60), 0.98),
    ("hit_pos14_deg-70_h92_60", -70, (92, 60), 0.96),
    ("hit_pos14_deg-65_h92_62", -65, (92, 62), 0.96),
    ("hit_pos14_deg-60_h88_56", -60, (88, 56), 1.0),
    ("hit_pos14_deg-70_h88_58", -70, (88, 58), 0.98),
    ("hit_pos14_deg-65_h88_55", -65, (88, 55), 0.98),
    ("hit_pos14_deg-75_h90_62", -75, (90, 62), 0.95),
]

os.makedirs("/tmp/hit_eval", exist_ok=True)

bpx = body_pos14.load()
assert bpx is not None

for name, deg, hand, scale in test_configs:
    staff = place_rigid_staff(clean_staff, deg=deg, target_hand=hand, scale=scale)
    spx = staff.load()
    assert spx is not None
    
    comp = Image.alpha_composite(shadow, body_pos14)
    comp = Image.alpha_composite(comp, staff)
    comp.save(f"/tmp/hit_eval/{name}.png")
    
    # Check clipping
    cpx = comp.load()
    assert cpx is not None
    x0 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], cpx[0, y])[3] > 0)
    x127 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], cpx[127, y])[3] > 0)
    y0 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], cpx[x, 0])[3] > 0)
    y127 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], cpx[x, 127])[3] > 0)
    
    # Calculate metrics
    total_staff = 0
    staff_outside = 0
    staff_on_edge = 0
    for y in range(128):
        for x in range(128):
            sp = cast(tuple[int,int,int,int], spx[x, y])
            if sp[3] > 50:
                total_staff += 1
                bp = cast(tuple[int,int,int,int], bpx[x, y])
                if bp[3] <= 50:
                    staff_outside += 1
                else:
                    # check edge of body
                    is_edge = False
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < 128 and 0 <= ny < 128:
                                np_val = cast(tuple[int,int,int,int], bpx[nx, ny])
                                if np_val[3] <= 50:
                                    is_edge = True
                                    break
                    if is_edge:
                        staff_on_edge += 1
                        
    out_pct = (staff_outside / total_staff * 100.0) if total_staff else 0.0
    edge_pct = (staff_on_edge / total_staff * 100.0) if total_staff else 0.0
    print(f"{name}:")
    print(f"  Bbox: {comp.getbbox()}, border: x0={x0}, x127={x127}, y0={y0}, y127={y127}")
    print(f"  Staff: total={total_staff}, outside={staff_outside} ({out_pct:.1f}%), on_body_edge={staff_on_edge} ({edge_pct:.1f}%)")
