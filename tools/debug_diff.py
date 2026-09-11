#!/usr/bin/env python3
import os
from PIL import Image, ImageChops

shot_dir = "/opt/side/bravesoul-game/screenshots"
p0 = os.path.join(shot_dir, "proof_explore_idle_breathe_t0.png")
p1 = os.path.join(shot_dir, "proof_explore_idle_breathe_t1.png")

img0 = Image.open(p0).convert("RGBA")
img1 = Image.open(p1).convert("RGBA")

diff = ImageChops.difference(img0, img1)
bbox = diff.getbbox(alpha_only=False)
print("diff bbox:", bbox)

# Let's see what is inside diff
# Let's save diff visual
diff.save(os.path.join(shot_dir, "debug_diff.png"))

# Where is the non-zero diff?
# Let's count non-zero per y row
w, h = diff.size
for y in range(0, h, 20):
    row_diff = sum(1 for x in range(w) if diff.getpixel((x, y))[:3] != (0, 0, 0))
    if row_diff > 0:
        print(f"y={y}: {row_diff} diff pixels")
