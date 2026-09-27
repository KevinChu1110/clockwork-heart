from typing import cast
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"

key_512 = Image.open(f"{PD_DIR}/winding_key/key_wolf_heavy_pojun_cross_512.png").convert("RGBA")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_wolf_segmented_spring_tail_512.png").convert("RGBA")
chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_wolf_warm_orange_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_wolf_gear_mane_cowl_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_wolf_scavenger_scrap_plate_armor_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_wolf_twin_blue_optic_lens_512.png").convert("RGBA")
weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_wolf_scrap_sawblade_greatsword_512.png").convert("RGBA")

comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp512.alpha_composite(key_512)
comp512.alpha_composite(curio_512)
comp512.alpha_composite(chassis_512)
comp512.alpha_composite(head_512)
comp512.alpha_composite(costume_512)
comp512.alpha_composite(core_512)
comp512.alpha_composite(weapon_512)

# Bust for HUD
bust_hud_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_hud_512.alpha_composite(key_512)
bust_hud_512.alpha_composite(chassis_512)
bust_hud_512.alpha_composite(head_512)
bust_hud_512.alpha_composite(costume_512)
bust_hud_512.alpha_composite(core_512)

# Crop box around head and collar
crop_box = (50, 40, 460, 360)
hud_crop = bust_hud_512.crop(crop_box)
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
print("HUD 128 bbox:", h_bbox, "left_m:", h_bbox[0], "right_m:", 128 - h_bbox[2])

scale_h512 = 416.0 / max(tight.width, tight.height)
sw_h512 = int(round(tight.width * scale_h512))
sh_h512 = int(round(tight.height * scale_h512))
scaled_hud512 = tight.resize((sw_h512, sh_h512), Image.Resampling.LANCZOS)
hud_portrait_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
hud_portrait_512.alpha_composite(scaled_hud512, ((512 - sw_h512) // 2, (512 - sh_h512) // 2))
h512_bbox = hud_portrait_512.getbbox()
print("HUD 512 bbox:", h512_bbox, "left_m:", h512_bbox[0], "right_m:", 512 - h512_bbox[2])

# Dialogue Bust (384x480)
bust_crop = comp512.crop((40, 40, 490, 380))
bc_arr = np.array(bust_crop)
fade_rows = 16
h_c = bc_arr.shape[0]
for idx, r in enumerate(range(h_c - fade_rows, h_c)):
    factor = 1.0 - (idx / fade_rows) * 0.4
    bc_arr[r, :, 3] = (bc_arr[r, :, 3] * factor).astype(np.uint8)

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
print("Dialogue bust bbox:", bu_bbox, "bottom:", bu_bbox[3])
