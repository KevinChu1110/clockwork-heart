#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"

comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# 1. HUD 512 & 128
# Crop head and upper torso
# Viper head is around y=35..260, x=120..400
crop_box = (60, 20, 460, 360)
hud_crop = comp512.crop(crop_box)
h_cbbox = hud_crop.getbbox()
assert h_cbbox is not None
tight = hud_crop.crop(h_cbbox)

scale_h = 104.0 / max(tight.width, tight.height)
sw_h = int(round(tight.width * scale_h))
sh_h = int(round(tight.height * scale_h))
scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))
h_bbox = hud_portrait.getbbox()
assert h_bbox is not None
print(f"HUD 128 bbox: {h_bbox}, margins: L={h_bbox[0]}, R={128 - h_bbox[2]}, T={h_bbox[1]}, B={128 - h_bbox[3]}")

# 2. HUD 512
scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
h512_bbox = hud_portrait_512.getbbox()
assert h512_bbox is not None
print(f"HUD 512 bbox: {h512_bbox}, margins: L={h512_bbox[0]}, R={512 - h512_bbox[2]}, T={h512_bbox[1]}, B={512 - h512_bbox[3]}")

# 3. Dialogue Bust (384x480)
bust_crop = comp512.crop((20, 20, 480, 420))
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
assert b_cbbox is not None
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
assert bu_bbox is not None
print(f"Dialogue Bust bbox: {bu_bbox}, bottom={bu_bbox[3]} (expect 480)")
