from typing import cast
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"

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

bbox = comp512.getbbox()
print("comp512 bbox:", bbox)

# For bust, we want from top of key/head down to waist/hips (say y ~ 420 or 440)
# Let's see what is between y=340 and 460
arr = np.array(comp512)
for y in range(350, 480, 10):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: xs in [{xs.min()} .. {xs.max()}], count={len(xs)}")
