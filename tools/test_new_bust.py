#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
comp512 = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/swan/idle_512.png").convert("RGBA")

# Let's crop true waist-up:
# y from 10 to 345 (cutting off below waist/belt, zero legs)
# x from 80 to 450 (includes head, wings top, lance upper blade, chest armor)
bust_crop = comp512.crop((80, 10, 450, 345))
bc_arr = np.array(bust_crop)
fade_rows = 45
h_c = bc_arr.shape[0]
for idx, r in enumerate(range(h_c - fade_rows, h_c)):
    t = idx / float(fade_rows)
    factor = max(0.02, (1.0 - t) ** 1.8)
    new_a = (bc_arr[r, :, 3] * factor).astype(np.uint8)
    if r == h_c - 1:
        mask = (bc_arr[r, :, 3] > 50)
        new_a[mask] = np.maximum(new_a[mask], 2)
    bc_arr[r, :, 3] = new_a

bust_faded = Image.fromarray(bc_arr)
b_cbbox = bust_faded.getbbox()
assert b_cbbox is not None
tight_bust = bust_faded.crop(b_cbbox)
tw, th = tight_bust.size
b_scale = 360.0 / max(tw, th * 384.0 / 480.0)
scaled_bw = int(round(tw * b_scale))
scaled_bh = int(round(th * b_scale))
scaled_bust = tight_bust.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)

dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_bx = (384 - scaled_bw) // 2
paste_by = 480 - scaled_bh
dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
dialogue_bust.save(f"{REPO_ROOT}/game/assets/sprites/portraits/melodic_swan.png")

print(f"New bust size: {dialogue_bust.size}, bbox: {dialogue_bust.getbbox()}, scaled size: ({scaled_bw}, {scaled_bh})")
