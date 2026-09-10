#!/usr/bin/env python3
"""
tools/create_rabbit_macaque_comparison.py
Creates side-by-side comparison of Rabbit and Macaque in battle:
- Left: Rabbit (proof_battle_rabbit.png) - passed baseline
- Middle: Macaque Dawn Monk (proof_battle_macaque_equipped_dawn_monk.png)
- Right: Macaque Zen Striker (proof_battle_macaque_equipped_zen_striker.png)
"""

import os
from PIL import Image

shot_dir = "/opt/side/bravesoul-game/screenshots"

rab_path = os.path.join(shot_dir, "proof_battle_rabbit.png")
dawn_path = os.path.join(shot_dir, "proof_battle_macaque_equipped_dawn_monk.png")
zen_path = os.path.join(shot_dir, "proof_battle_macaque_equipped_zen_striker.png")

im_rab = Image.open(rab_path).convert("RGBA")
im_dawn = Image.open(dawn_path).convert("RGBA")
im_zen = Image.open(zen_path).convert("RGBA")

# 1. Full-screen comparison (1280x720 side by side, scaled to fit)
# Scale each to 640x360
w, h = 640, 360
im_rab_s = im_rab.resize((w, h), Image.Resampling.LANCZOS)
im_zen_s = im_zen.resize((w, h), Image.Resampling.LANCZOS)

comp_full = Image.new("RGBA", (w * 2 + 10, h), (25, 25, 30, 255))
comp_full.paste(im_rab_s, (0, 0))
comp_full.paste(im_zen_s, (w + 10, 0))

out_full = os.path.join(shot_dir, "proof_battle_rabbit_macaque_comparison.png")
comp_full.save(out_full)
print(f"✓ Saved side-by-side battle comparison: {out_full}")

# 2. Also create character focus comparison:
# Crop player character region from both
# In 1280x720 battle screen, player is roughly around (200, 200, 560, 650)
crop_box = (200, 180, 580, 660)
c_rab = im_rab.crop(crop_box)
c_dawn = im_dawn.crop(crop_box)
c_zen = im_zen.crop(crop_box)

cw, ch = c_rab.size
comp_chars = Image.new("RGBA", (cw * 3 + 20, ch), (25, 25, 30, 255))
comp_chars.paste(c_rab, (0, 0))
comp_chars.paste(c_dawn, (cw + 10, 0))
comp_chars.paste(c_zen, (cw * 2 + 20, 0))

out_chars = os.path.join(shot_dir, "proof_battle_rabbit_macaque_characters_comparison.png")
comp_chars.save(out_chars)
print(f"✓ Saved character close-up comparison: {out_chars}")
