#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/marmot"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/marmot"

chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_marmot_quarry_tinplate_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_marmot_alloy_chisel_visor_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_marmot_scavenger_canvas_harness_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_marmot_amber_dust_goggles_512.png").convert("RGBA")
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# Composite clean bust_hud_512 (head, cowl, optics, costume, chassis)
bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_hud_512.alpha_composite(chassis_512)
bust_hud_512.alpha_composite(head_512)
bust_hud_512.alpha_composite(costume_512)
bust_hud_512.alpha_composite(core_512)

crop_box = (80, 0, 440, 320)
hud_crop = bust_hud_512.crop(crop_box)
h_cbbox = hud_crop.getbbox()
assert h_cbbox is not None
tight = hud_crop.crop(h_cbbox)

# HUD 128x128 (margin >= 8px)
scale_h = 104.0 / max(tight.width, tight.height)
sw_h = int(round(tight.width * scale_h))
sh_h = int(round(tight.height * scale_h))
scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))

bbox128 = hud_portrait.getbbox()
print("HUD 128 bbox:", bbox128)
l, t, r, b = bbox128[0], bbox128[1], 128 - bbox128[2], 128 - bbox128[3]
print(f"HUD 128 margins: L={l}, T={t}, R={r}, B={b} (req: all >= 8)")

# HUD 512x512 (margin >= 32px)
scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))

bbox512 = hud_portrait_512.getbbox()
print("HUD 512 bbox:", bbox512)
l, t, r, b = bbox512[0], bbox512[1], 512 - bbox512[2], 512 - bbox512[3]
print(f"HUD 512 margins: L={l}, T={t}, R={r}, B={b} (req: all >= 32)")

# Dialogue Bust (384x480): True waist-up bust with smooth bottom alpha fade
bust_crop = comp512.crop((10, 0, 502, 390))
bc_arr = np.array(bust_crop)
fade_rows = 50
h_c = bc_arr.shape[0]
for idx, r_row in enumerate(range(h_c - fade_rows, h_c)):
    factor = max(0.02, (1.0 - idx / float(fade_rows)) ** 1.8)
    new_a = (bc_arr[r_row, :, 3] * factor).astype(np.uint8)
    if r_row == h_c - 1:
        mask = bc_arr[r_row, :, 3] > 50
        new_a[mask] = np.maximum(new_a[mask], 2)
    bc_arr[r_row, :, 3] = new_a

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
db_bbox = dialogue_bust.getbbox()
print("Dialogue bust bbox:", db_bbox)
print(f"Dialogue bust bottom touches 480: {db_bbox[3] == 480}")
