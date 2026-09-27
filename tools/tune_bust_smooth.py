from typing import cast
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"

key_512 = Image.open(f"{PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold_512.png").convert("RGBA")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_pangolin_segmented_scale_tail_512.png").convert("RGBA")
chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_pangolin_dune_orange_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_pangolin_brass_acoustic_ears_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_pangolin_sky_blue_optic_domes_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_pangolin_scavenger_tinker_vest_512.png").convert("RGBA")
weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_pangolin_dune_drill_claw_512.png").convert("RGBA")

# Full composite
comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp512.alpha_composite(key_512)
comp512.alpha_composite(curio_512)
comp512.alpha_composite(chassis_512)
comp512.alpha_composite(head_512)
comp512.alpha_composite(costume_512)
comp512.alpha_composite(core_512)
comp512.alpha_composite(weapon_512)

# Waist-up crop: from y=40 down to y=420 (waist level, above feet/ground shadow)
bust_crop = comp512.crop((35, 35, 465, 420))
bc_arr = np.array(bust_crop)

# Clean bottom edge
fade_rows = 12
h_c = bc_arr.shape[0]
for idx, r in enumerate(range(h_c - fade_rows, h_c)):
    factor = 1.0 - (idx / fade_rows) * 0.3  # slight soft rolloff
    bc_arr[r, :, 3] = (bc_arr[r, :, 3] * factor).astype(np.uint8)

bust_faded = Image.fromarray(bc_arr)
tight = bust_faded.crop(bust_faded.getbbox())
tw, th = tight.size
print(f"Tight size: {tw} x {th}")

# Scale to fit 384x480 with appropriate padding
# Let width be 352px (margins ~16px)
b_scale = 352.0 / tw
scaled_w = int(round(tw * b_scale))
scaled_h = int(round(th * b_scale))
print(f"Scaled size: {scaled_w} x {scaled_h}")

scaled_bust = tight.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_x = (384 - scaled_w) // 2
paste_y = 480 - scaled_h
dialogue_bust.alpha_composite(scaled_bust, (paste_x, paste_y))

bbox = dialogue_bust.getbbox()
assert bbox is not None
print(f"Final dialogue bust bbox: {bbox}, w={bbox[2]-bbox[0]}, h={bbox[3]-bbox[1]}")
dialogue_bust.save(f"{PORTRAITS_DIR}/dune_pangolin.png")
