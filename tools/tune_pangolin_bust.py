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

# Dialogue bust (384x480): proper waist-up bust anchored to bottom
ch_bust_arr = np.array(chassis_512)
for y in range(320, 512):
    for x in range(512):
        if y > 380:
            ch_bust_arr[y, x] = [0, 0, 0, 0]
ch_bust = Image.fromarray(ch_bust_arr)

bust_dialogue_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
bust_dialogue_512.alpha_composite(key_512)
bust_dialogue_512.alpha_composite(curio_512)
bust_dialogue_512.alpha_composite(ch_bust)
bust_dialogue_512.alpha_composite(head_512)
bust_dialogue_512.alpha_composite(costume_512)
bust_dialogue_512.alpha_composite(core_512)
bust_dialogue_512.alpha_composite(weapon_512)

# Tight crop of the bust
bust_crop = bust_dialogue_512.crop((20, 15, 490, 380))
tight = bust_crop.crop(bust_crop.getbbox())
tw, th = tight.size
print(f"Tight bust size: {tw} x {th}")

# Scale so width fills ~348px (leaving 18px margin on left and right)
b_scale = 348.0 / tw
scaled_bw = int(round(tw * b_scale))
scaled_bh = int(round(th * b_scale))
print(f"Scaled bust size: {scaled_bw} x {scaled_bh}")

scaled_bust = tight.resize((scaled_bw, scaled_bh), Image.Resampling.LANCZOS)
dialogue_bust = Image.new("RGBA", (384, 480), (0, 0, 0, 0))
paste_bx = (384 - scaled_bw) // 2
paste_by = 480 - scaled_bh
dialogue_bust.alpha_composite(scaled_bust, (paste_bx, paste_by))

bbox = dialogue_bust.getbbox()
assert bbox is not None
print(f"Final dialogue bust bbox: {bbox}, w={bbox[2]-bbox[0]}, h={bbox[3]-bbox[1]}")
dialogue_bust.save(f"{PORTRAITS_DIR}/dune_pangolin.png")
