#!/usr/bin/env python3
from PIL import Image
import numpy as np

idle_512 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/sailfish/idle_512.png").convert("RGBA")

# In sailfish idle_512, where is the head and chest?
# head_unit_512 is (115, 35, 361, 245)
# key_512 is (223, 3, 441, 269)
# optic_core_512 is (159, 135, 357, 209)
# costume_512 is (147, 211, 353, 365)

# Test HUD crop
crop_box = (80, 10, 440, 310)
hud_crop = idle_512.crop(crop_box)
h_bbox = hud_crop.getbbox()
print("HUD crop bbox within box:", h_bbox)
tight = hud_crop.crop(h_bbox)
print("Tight HUD size:", tight.size)

# Scale to 128x128
scale_h = 104.0 / max(tight.width, tight.height)
sw_h = int(round(tight.width * scale_h))
sh_h = int(round(tight.height * scale_h))
scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_128.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
b128 = hud_128.getbbox()
print("HUD 128 bbox:", b128, "margins:", b128[0], 128 - b128[2], b128[1], 128 - b128[3])

# Scale to 512x512
scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
b512 = hud_512.getbbox()
print("HUD 512 bbox:", b512, "margins:", b512[0], 512 - b512[2], b512[1], 512 - b512[3])

# Test Dialogue bust (384x480)
bust_crop = idle_512.crop((40, 10, 460, 390))
bc_arr = np.array(bust_crop)
fade_rows = 50
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
tight_bust = bust_faded.crop(b_cbbox)
tw, th = tight_bust.size
b_scale = 356.0 / max(tw, th * 384.0 / 480.0)
scaled_bw = int(round(tw * b_scale))
scaled_bh = int(round(th * b_scale))
scaled_bust = tight_bust.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)

dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_bx = (384 - scaled_bw) // 2
paste_by = 480 - scaled_bh
dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
bu_bbox = dialogue_bust.getbbox()
print("Dialogue bust bbox:", bu_bbox)
