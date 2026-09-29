from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
FIREFLY_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/firefly"

key_src = Image.open(f"{FIREFLY_PD}/winding_key/key_firefly_floral_gear_brass.png").convert("RGBA")
curio_src = Image.open(f"{FIREFLY_PD}/back_curio/curio_firefly_luminescent_resin_abdomen.png").convert("RGBA")
chassis_src = Image.open(f"{FIREFLY_PD}/chassis/chassis_firefly_emerald_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{FIREFLY_PD}/head_unit/head_firefly_brass_antenna_cowl.png").convert("RGBA")
costume_src = Image.open(f"{FIREFLY_PD}/costume/costume_firefly_vine_harness_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{FIREFLY_PD}/optic_core/face_firefly_dual_lantern_quartz_eyes.png").convert("RGBA")
weapon_src = Image.open(f"{FIREFLY_PD}/weapon/weapon_firefly_luminescent_vine_staff.png").convert("RGBA")

body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
comp.alpha_composite(key_src)
comp.alpha_composite(body_core)
comp.alpha_composite(weapon_src)

ref_comp = Image.open(f"{FIREFLY_PD}/proof_paperdoll_firefly_composite.png").convert("RGBA")
diff = ImageChops.difference(comp, ref_comp)
diff_arr = np.array(diff)
diff_count = int(np.sum(np.any(diff_arr > 0, axis=-1)))
print("Difference between assembled composite and proof_paperdoll_firefly_composite:", diff_count)
