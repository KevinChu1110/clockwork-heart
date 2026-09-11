import os
import sys
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
sys.path.insert(0, REPO_ROOT)

from tools.generate_fox_combat_poses import measure_staff_linearity

body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
print("body_clean linearity resid:", measure_staff_linearity(body_clean))

# Check what pixels in body_clean match is_bronze
px = body_clean.load()
assert px is not None
bronze_ys = []
for y in range(30, 124):
    xs = []
    for x in range(128):
        p = cast(tuple[int, int, int, int], px[x, y])
        if p[3] > 120:
            if 120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95:
                xs.append(x)
    if xs:
        bronze_ys.append((y, len(xs), min(xs), max(xs)))

print(f"body_clean has bronze pixels in {len(bronze_ys)} rows:")
for b in bronze_ys[:10]:
    print(f"  y={b[0]}: count={b[1]}, x={b[2]}..{b[3]}")
