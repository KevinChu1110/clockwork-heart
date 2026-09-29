import os
from PIL import Image
import numpy as np

repo = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e4a76321"
PD_DIR = f"{repo}/game/assets/sprites/player/paperdoll/firefly"
POSES_DIR = f"{repo}/game/assets/sprites/player/poses/firefly"

chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_firefly_emerald_tinplate_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_firefly_brass_antenna_cowl_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_firefly_vine_harness_cuirass_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_firefly_dual_lantern_quartz_eyes_512.png").convert("RGBA")
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# Clean bust for HUD: chassis + head + costume + core
bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_hud_512.alpha_composite(chassis_512)
bust_hud_512.alpha_composite(head_512)
bust_hud_512.alpha_composite(costume_512)
bust_hud_512.alpha_composite(core_512)

# Check head bbox
head_bbox = head_512.getbbox()
print("Head bbox 512:", head_bbox)
core_bbox = core_512.getbbox()
print("Core bbox 512:", core_bbox)
bust_bbox = bust_hud_512.getbbox()
print("Bust composite bbox 512:", bust_bbox)

# In firefly: head bbox is (103, 11, 413, 253), core is (187, 139, 329, 201), costume is (163, 235, 353, 393)
# For HUD, we want head + facial features + upper torso/cowl
# Let's test a crop box around (60, 0, 450, 320) or similar
crop_box = (60, 0, 450, 320)
hud_crop = bust_hud_512.crop(crop_box)
h_cbbox = hud_crop.getbbox()
print("HUD crop bbox inside crop_box:", h_cbbox)
tight = hud_crop.crop(h_cbbox)
print("Tight HUD size:", tight.size)

# Test 128x128 HUD target sizing (target 104px or 100px so margin >= 8)
scale_h = 104.0 / max(tight.width, tight.height)
sw_h = int(round(tight.width * scale_h))
sh_h = int(round(tight.height * scale_h))
scaled_hud = tight.resize((sw_h, sh_h), Image.Resampling.LANCZOS)
hud_portrait = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
hud_portrait.alpha_composite(scaled_hud, ((128 - sw_h) // 2, (128 - sh_h) // 2))

bbox128 = hud_portrait.getbbox()
print("HUD 128 bbox:", bbox128)
m128 = [bbox128[0], bbox128[1], 128 - bbox128[2], 128 - bbox128[3]]
print(f"HUD 128 margins: L={m128[0]}, T={m128[1]}, R={m128[2]}, B={m128[3]} (all >= 8: {all(m >= 8 for m in m128)})")

# Test 512x512 HUD target sizing (target 416px so margin >= 32)
scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))

bbox512 = hud_portrait_512.getbbox()
print("HUD 512 bbox:", bbox512)
m512 = [bbox512[0], bbox512[1], 512 - bbox512[2], 512 - bbox512[3]]
print(f"HUD 512 margins: L={m512[0]}, T={m512[1]}, R={m512[2]}, B={m512[3]} (all >= 32: {all(m >= 32 for m in m512)})")

# Dialogue bust test: 384x480
# In comp512, let us inspect vertical extent:
comp_bbox = comp512.getbbox()
print("Comp512 bbox:", comp_bbox)
bust_crop_dialogue = comp512.crop((10, 0, 502, 390))
bc_arr = np.array(bust_crop_dialogue)
fade_rows = 50
h_c = bc_arr.shape[0]
for idx, r in enumerate(range(h_c - fade_rows, h_c)):
    t = idx / float(fade_rows)
    factor = max(0.02, (1.0 - t) ** 1.8)
    new_a = (bc_arr[r, :, 3] * factor).astype(np.uint8)
    if r == h_c - 1:
        mask = bc_arr[r, :, 3] > 50
        new_a[mask] = np.maximum(new_a[mask], 2)
    bc_arr[r, :, 3] = new_a

bust_faded = Image.fromarray(bc_arr)
b_cbbox = bust_faded.getbbox()
tight_bust = bust_faded.crop(b_cbbox)
tw, th = tight_bust.size
print("Tight dialogue bust size:", tight_bust.size)
b_scale = 356.0 / max(tw, th * 384.0 / 480.0)
scaled_bw = int(round(tw * b_scale))
scaled_bh = int(round(th * b_scale))
print(f"Scaled dialogue bust: {scaled_bw}x{scaled_bh}")
scaled_bust = tight_bust.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_bx = (384 - scaled_bw) // 2
paste_by = 480 - scaled_bh
dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))
db_bbox = dialogue_bust.getbbox()
assert db_bbox is not None
print("Dialogue bust bbox:", db_bbox, "bottom is 480:", db_bbox[3] == 480)
