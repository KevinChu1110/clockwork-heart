#!/usr/bin/env python3
from PIL import Image

shot_dir = "/opt/side/bravesoul-game/screenshots"
im_rab = Image.open(f"{shot_dir}/proof_battle_rabbit.png").convert("RGBA")
im_mac = Image.open(f"{shot_dir}/proof_battle_macaque_full_screen.png").convert("RGBA")

print("im_rab size:", im_rab.size)
print("im_mac size:", im_mac.size)

# Scale both to 640x360 and place side by side
w, h = 640, 360
im_rab_s = im_rab.resize((w, h), Image.Resampling.LANCZOS)
im_mac_s = im_mac.resize((w, h), Image.Resampling.LANCZOS)

comp = Image.new("RGBA", (w * 2 + 10, h), (25, 25, 30, 255))
comp.paste(im_rab_s, (0, 0))
comp.paste(im_mac_s, (w + 10, 0))

out = f"{shot_dir}/proof_battle_rabbit_macaque_fullscreen_comparison.png"
comp.save(out)
print(f"✓ Saved {out}")
