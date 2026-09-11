import os
import sys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)

from tools.generate_fox_combat_poses import build_contact_shadow

body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
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
rot_pos14 = large_hit.rotate(14, resample=Image.Resampling.BICUBIC, center=(64 + 52, 64 + 118))
body_hit = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_hit.paste(rot_pos14, (-64, -64), rot_pos14)

bpx = body_hit.load()
assert bpx is not None

print("Foot contact profile:")
for y in range(114, 128):
    xs = [x for x in range(128) if cast(tuple[int,int,int,int], bpx[x, y])[3] > 50]
    if xs:
        print(f"y={y}: count={len(xs)}, x={min(xs)}..{max(xs)}")

# Shadow profile check
shadow = build_contact_shadow(cx=50, cy=119, rx=34, ry=5, blur=0.6)
spx = shadow.load()
assert spx is not None
print("\nShadow profile:")
for y in range(118, 128):
    c = sum(1 for x in range(128) if cast(tuple[int,int,int,int], spx[x, y])[3] >= 8)
    print(f"y={y}: shadow_px={c}")
