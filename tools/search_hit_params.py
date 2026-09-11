import os
import sys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)

from tools.generate_fox_combat_poses import place_rigid_staff, build_contact_shadow, measure_staff_linearity, measure_shadow_rows

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

# Let's test with rotate(14) (backward recoil)
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit.paste(rot_pos14, (-64, -64), rot_pos14)

bpx = body_hit.load()
assert bpx is not None
body_mask = [[cast(tuple[int,int,int,int], bpx[x, y])[3] > 60 for x in range(128)] for y in range(128)]
body_boundary = [[False]*128 for _ in range(128)]
for y in range(128):
    for x in range(128):
        if body_mask[y][x]:
            if (x == 0 or not body_mask[y][x-1] or 
                x == 127 or not body_mask[y][x+1] or 
                y == 0 or not body_mask[y-1][x] or 
                y == 127 or not body_mask[y+1][x]):
                body_boundary[y][x] = True

shadow = build_contact_shadow(cx=48, cy=119, rx=34, ry=5, blur=0.6)

results = []

for deg in range(-85, -50, 5): # -85, -80, -75, -70, -65, -60, -55
    for hx in range(80, 102, 2):
        for hy in range(50, 80, 2):
            for scale in [0.95, 0.98, 1.0]:
                staff = place_rigid_staff(clean_staff, deg=deg, target_hand=(hx, hy), scale=scale)
                spx = staff.load()
                assert spx is not None
                
                # Check boundary clipping (must be 0 on borders)
                x0 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], spx[0, y])[3] > 0)
                x127 = sum(1 for y in range(128) if cast(tuple[int,int,int,int], spx[127, y])[3] > 0)
                y0 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], spx[x, 0])[3] > 0)
                y127 = sum(1 for x in range(128) if cast(tuple[int,int,int,int], spx[x, 127])[3] > 0)
                if x0 > 0 or x127 > 0 or y0 > 0 or y127 > 0:
                    continue
                
                # Count staff metrics
                total_staff = 0
                staff_outside_body = 0
                staff_on_body_boundary = 0
                for y in range(128):
                    for x in range(128):
                        if cast(tuple[int,int,int,int], spx[x, y])[3] > 60:
                            total_staff += 1
                            if not body_mask[y][x]:
                                staff_outside_body += 1
                            elif body_boundary[y][x]:
                                staff_on_body_boundary += 1
                                
                if total_staff == 0:
                    continue
                outside_pct = staff_outside_body / total_staff * 100.0
                boundary_pct = staff_on_body_boundary / total_staff * 100.0
                
                # Check composite linearity
                comp = Image.alpha_composite(shadow, body_hit)
                comp = Image.alpha_composite(comp, staff)
                resid = measure_staff_linearity(comp)
                
                # Filter: let us inspect top candidates
                results.append((outside_pct, boundary_pct, resid, deg, hx, hy, scale))

results.sort(key=lambda item: item[0], reverse=True)
print(f"Found {len(results)} unclipped configurations!")
for r in results[:20]:
    print(f"deg={r[3]}, hand=({r[4]}, {r[5]}), scale={r[6]} -> outside={r[0]:.1f}%, boundary={r[1]:.1f}%, resid={r[2]:.2f}px")
