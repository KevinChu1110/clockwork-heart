#!/usr/bin/env python3
from PIL import Image
import numpy as np

im = Image.open("/tmp/properly_keyed_boar.png")
w_raw, h_raw = im.size # 928, 1160

scale = 476.0 / 1120.0
target_w = int(w_raw * scale) # 394
target_h = int(h_raw * scale) # 493

scaled = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
paste_x = (512 - target_w) // 2 # 59
paste_y = 512 - target_h - 8   # 11
canvas.alpha_composite(scaled, (paste_x, paste_y))
canvas.save("/tmp/master_clean_512.png")
print("Saved /tmp/master_clean_512.png, bbox:", canvas.getbbox())

# Let's inspect the positions of key features in canvas:
# 1. Eye position in 512:
# In the original, where is the eye?
arr = np.array(canvas)
# Look for glowing cyan pixels (high G and B) around head (y: 100..200, x: 180..300)
cyan_mask = (arr[100:200, 180:300, 1] > 140) & (arr[100:200, 180:300, 2] > 140) & (arr[100:200, 180:300, 0] < 120)
ys, xs = np.where(cyan_mask)
if len(ys) > 0:
    eye_cy = 100 + int(np.mean(ys))
    eye_cx = 180 + int(np.mean(xs))
    print(f"Detected cyan eye center: ({eye_cx}, {eye_cy})")
    print(f"Eye range: Y: {100+ys.min()}..{100+ys.max()}, X: {180+xs.min()}..{180+xs.max()}")

# 2. Chest core center:
cyan_core = (arr[250:350, 180:280, 1] > 140) & (arr[250:350, 180:280, 2] > 140) & (arr[250:350, 180:280, 0] < 120)
ys_c, xs_c = np.where(cyan_core)
if len(ys_c) > 0:
    core_cy = 250 + int(np.mean(ys_c))
    core_cx = 180 + int(np.mean(xs_c))
    print(f"Detected chest core center: ({core_cx}, {core_cy})")
