#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Load properly keyed boar
im = Image.open("/tmp/properly_keyed_boar.png")
w_raw, h_raw = im.size

scale = 476.0 / 1120.0
target_w = int(w_raw * scale)
target_h = int(h_raw * scale)

scaled = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
paste_x = (512 - target_w) // 2 # 59
paste_y = 512 - target_h - 8   # 11
canvas.alpha_composite(scaled, (paste_x, paste_y))

# Brow anchor in 512 is (235, 161)
# Eye sprite size in spec is (90, 60), origin is (45, 30)
# That means eye crop in 512 is:
# left = 235 - 45 = 190
# top = 161 - 30 = 131
# right = 190 + 90 = 280
# bottom = 131 + 60 = 191
eye_region = canvas.crop((190, 131, 280, 191))
eye_region.save("/tmp/authentic_eye_in_512.png")
print("Saved /tmp/authentic_eye_in_512.png")
