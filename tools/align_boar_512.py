#!/usr/bin/env python3
from PIL import Image
import numpy as np

# Load properly keyed boar
im = Image.open("/tmp/properly_keyed_boar.png")
w_raw, h_raw = im.size # 928, 1160

# We want the foot to touch ground around y = 480 (standard 512 baseline)
# Let's see the bounding box of non-zero pixels
bbox = im.getbbox()
print("Raw bbox:", bbox)
# Character bottom is around bbox[3]

# Scale factor: character height in raw is bbox[3] - bbox[1] = 1160 - 137 = 1023
# In 512, character height should be around 460..470 px
scale = 470.0 / (bbox[3] - bbox[1])
new_w = int(w_raw * scale)
new_h = int(h_raw * scale)
print(f"Scaled size: {new_w}x{new_h}, scale={scale:.4f}")

scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

# We want the feet/root around (256, 480)
# Let's align horizontally centered around x = 256
paste_x = 256 - int((bbox[0] + (bbox[2] - bbox[0]) * 0.44) * scale)
# And vertical position such that bottom is at 495 (with contact shadow)
paste_y = 500 - int(bbox[3] * scale)
print(f"Paste offset: ({paste_x}, {paste_y})")

canvas.alpha_composite(scaled, (paste_x, paste_y))
canvas.save("/tmp/boar_512_aligned.png")
print("Saved /tmp/boar_512_aligned.png, bbox:", canvas.getbbox())
