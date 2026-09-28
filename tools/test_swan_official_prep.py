#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/swan"
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# Let's inspect HUD crop from comp512
crop_box = (140, 15, 365, 265)
hud_crop = comp512.crop(crop_box)
h_bbox = hud_crop.getbbox()
print("HUD crop tight bbox:", h_bbox)
tight_hud = hud_crop.crop(h_bbox)
print("tight HUD size:", tight_hud.size)

# Scale to 128 (margin >= 8px -> content <= 112px, e.g. 104px)
scale_h = 104.0 / max(tight_hud.width, tight_hud.height)
sw_h = int(round(tight_hud.width * scale_h))
sh_h = int(round(tight_hud.height * scale_h))
scaled_hud = tight_hud.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_128.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
print("HUD 128 bbox:", hud_128.getbbox())

# Dialogue bust crop
# From y=10 to y=380, x=50 to 480
bust_crop = comp512.crop((50, 10, 480, 390))
print("Bust crop bbox:", bust_crop.getbbox())
