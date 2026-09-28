#!/usr/bin/env python3
from PIL import Image
import numpy as np

idle_512 = Image.open("game/assets/sprites/player/poses/kite/idle_512.png").convert("RGBA")

# Test HUD portrait crop
# Head 512 is (155, 39, 361, 237)
crop_box = (145, 30, 375, 245)
hud_crop = idle_512.crop(crop_box)
bbox = hud_crop.getbbox()
print("HUD crop bbox inside crop_box:", bbox)

tight = hud_crop.crop(bbox)
scale_h = 104.0 / max(tight.width, tight.height)
sw_h = int(round(tight.width * scale_h))
sh_h = int(round(tight.height * scale_h))
scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_128.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
h128_bbox = hud_128.getbbox()
print("HUD 128 bbox:", h128_bbox, "Margins:", h128_bbox[0], h128_bbox[1], 128 - h128_bbox[2], 128 - h128_bbox[3])

scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
h512_bbox = hud_512.getbbox()
print("HUD 512 bbox:", h512_bbox, "Margins:", h512_bbox[0], h512_bbox[1], 512 - h512_bbox[2], 512 - h512_bbox[3])

# Test Dialogue bust (384x480)
# Waist up: y from 20 to 400
bust_crop = idle_512.crop((70, 20, 480, 400))
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
print("Bust faded bbox:", b_cbbox)
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
