#!/usr/bin/env python3
import os
from PIL import Image, ImageChops

shot_dir = "/opt/side/bravesoul-game/screenshots"
p0 = os.path.join(shot_dir, "proof_explore_idle_breathe_t0.png")
p1 = os.path.join(shot_dir, "proof_explore_idle_breathe_t1.png")
pw = os.path.join(shot_dir, "proof_explore_walking.png")

img0 = Image.open(p0).convert("RGBA")
img1 = Image.open(p1).convert("RGBA")
imgw = Image.open(pw).convert("RGBA")

# Let's inspect the diff bbox between t0 and t1
diff_t = ImageChops.difference(img0, img1)
bbox_t = diff_t.getbbox(alpha_only=False)
print("diff bbox between t0 and t1:", bbox_t)

# Let's measure the exact character width and height changes
# Let's isolate the character outline in crop0 and crop1
# In Godot, the character has an outline with OutlineShader (dark blue-purple outline Color(0.12, 0.10, 0.23))
# Let's find top-most, bottom-most, left-most, right-most character pixels
# The background is wood floor (tan/brown y ~ 200..720)
# Let's measure the diff overlay
diff_vis = Image.new("RGBA", (1280, 720), (0, 0, 0, 255))
pix_diff = diff_t.load()
pix_img0 = img0.load()
pix_out = diff_vis.load()
if pix_diff is not None and pix_img0 is not None and pix_out is not None:
    for y in range(720):
        for x in range(1280):
            p_diff = pix_diff[x, y]
            if p_diff[0] > 0 or p_diff[1] > 0 or p_diff[2] > 0:
                # Highlight diff in bright green
                pix_out[x, y] = (0, 255, 100, 255)
            else:
                pix_out[x, y] = pix_img0[x, y]

diff_vis_path = os.path.join(shot_dir, "proof_explore_breathe_diff_overlay.png")
diff_vis.save(diff_vis_path)
print(f"Saved diff overlay: {diff_vis_path}")

# Let's also create a 3-box comparison: t0, diff overlay, t1
char_box = (430, 10, 760, 420)
c0 = img0.crop(char_box)
c1 = img1.crop(char_box)
cd = diff_vis.crop(char_box)
cw, ch = c0.size

three_box = Image.new("RGBA", (cw * 3 + 20, ch), (20, 20, 20, 255))
three_box.paste(c0, (0, 0))
three_box.paste(cd, (cw + 10, 0))
three_box.paste(c1, (cw * 2 + 20, 0))
three_box_path = os.path.join(shot_dir, "proof_explore_breathe_3box.png")
three_box.save(three_box_path)
print(f"Saved 3-box comparison: {three_box_path}")
