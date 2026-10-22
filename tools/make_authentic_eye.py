#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Load the authentic eye region from 512
im = Image.open("/tmp/authentic_eye_in_512.png").convert("RGBA")
arr = np.array(im)

# Let's inspect where the cyan eyeball is in this 90x60 crop
# Glowing cyan has high G and B, distinct from bronze/brass
eyeball_mask = (arr[:, :, 1] > 95) & (arr[:, :, 2] > 105) & (arr[:, :, 0] < 165)
# Also include specular highlight (near white: R>200, G>200, B>200) inside the eyeball radius
# First find eyeball center
ys, xs = np.where(eyeball_mask)
cy = int(np.mean(ys))
cx = int(np.mean(xs))
print(f"Eyeball center in crop: ({cx}, {cy})")

# Expand to include pupil, highlight, and glassy iris within radius 15 of (cx, cy)
eye_clean = Image.new("RGBA", (90, 60), (0, 0, 0, 0))
clean_arr = np.array(eye_clean)

for y in range(60):
    for x in range(90):
        dist = np.hypot(x - cx, y - cy)
        if dist <= 14.5:
            # Shift to center (45, 30)
            target_x = 45 + (x - cx)
            target_y = 30 + (y - cy)
            if 0 <= target_x < 90 and 0 <= target_y < 60:
                p = arr[y, x]
                if dist > 12.5:
                    # feather edge
                    fade = (14.5 - dist) / 2.0
                    clean_arr[target_y, target_x] = [p[0], p[1], p[2], int(p[3] * fade)]
                else:
                    clean_arr[target_y, target_x] = p

out_cyan = Image.fromarray(clean_arr, mode="RGBA")
out_cyan.save("/tmp/authentic_eye_cyan.png")
print("Saved /tmp/authentic_eye_cyan.png")
