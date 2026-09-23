#!/usr/bin/env python3
import numpy as np
from PIL import Image

im = Image.open("/tmp/tortoise_lower_body.png").convert("RGBA")
w, h = im.size
print(f"Lower body size: {w}x{h}")

# The 5 limb positions mentioned by vision:
# 1. Leftmost foot (x approx 40..130)
# 2. Main fore-left foot (x approx 170..310)
# 3. Center hind foot (x approx 320..420)
# 4. Center raised foot/hand (x approx 400..550, elevated above ground)
# 5. Rightmost foot (x approx 570..680)

# Let's find the bottom-most y for each limb
arr = np.array(im)
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
# Foreground is anything where r+g+b < 600 or spread > 40
fg = (r < 200) | (g < 200) | (b < 200)

for x_start, x_end, name in [
    (30, 140, "Foot 1 (Leftmost)"),
    (150, 320, "Foot 2 (Fore-Left Main)"),
    (320, 420, "Foot 3 (Mid-Hind)"),
    (420, 560, "Foot 4 (Raised hand/foot)"),
    (560, 680, "Foot 5 (Rightmost)")
]:
    limb_fg = fg[:, x_start:x_end]
    ys, xs = np.where(limb_fg)
    if len(ys) > 0:
        print(f"{name}: x in [{np.min(xs)+x_start}, {np.max(xs)+x_start}], y in [{np.min(ys)}, {np.max(ys)}]")
