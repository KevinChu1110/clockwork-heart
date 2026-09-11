#!/usr/bin/env python3
import os
from PIL import Image, ImageChops

shot_dir = "/opt/side/bravesoul-game/screenshots"
p0 = os.path.join(shot_dir, "proof_explore_idle_breathe_t0.png")
p1 = os.path.join(shot_dir, "proof_explore_idle_breathe_t1.png")

img0 = Image.open(p0).convert("RGBA")
img1 = Image.open(p1).convert("RGBA")

# Let's crop just the character body around (550, 50, 700, 380)
crop0 = img0.crop((500, 50, 700, 380))
crop1 = img1.crop((500, 50, 700, 380))

diff = ImageChops.difference(crop0, crop1)
bbox = diff.getbbox(alpha_only=False)
print("character diff bbox:", bbox)

# Count diff pixels
diff_px = sum(1 for p in diff.getdata() if p[:3] != (0, 0, 0))
print("diff pixels in character body:", diff_px)

# Save an animated GIF or blinker to see it with human eyes
crop0.save(os.path.join(shot_dir, "breathe_anim.gif"), save_all=True, append_images=[crop1], duration=500, loop=0)
print("Saved breathe_anim.gif")
