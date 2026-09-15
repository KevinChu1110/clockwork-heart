import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

battle_path = f"{REPO_ROOT}/game/assets/sprites/player/macaque_battle.png"
ivory_path = f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png"
key_path = f"{MACAQUE_DIR}/winding_key/key_classic_brass.png"

battle = Image.open(battle_path).convert("RGBA")
ivory = Image.open(ivory_path).convert("RGBA")
key = Image.open(key_path).convert("RGBA")

arr_b = np.array(battle)
arr_i = np.array(ivory)
arr_k = np.array(key)

# The face region where ivory was smeared:
mask = np.zeros((128, 128), dtype=bool)
for y in range(15, 65):
    for x in range(26, 80):
        if arr_b[y, x, 3] > 0:
            mask[y, x] = True

# Do not overwrite winding key area if any
mask &= (arr_k[:, :, 3] == 0)

arr_new_ivory = arr_i.copy()
arr_new_ivory[mask] = arr_b[mask]

new_ivory = Image.fromarray(arr_new_ivory)
new_ivory.save(ivory_path)
print(f"✓ Saved updated {ivory_path}")

# Regenerate bamboo bronze chassis
from build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze
create_macaque_paint_bamboo_bronze()

# Now composite with all 7 layers to generate proof_paperdoll_macaque_composite.png
layers = [
    f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png",
    f"{MACAQUE_DIR}/winding_key/key_classic_brass.png",
    ivory_path,
    f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png",
    f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png",
    f"{MACAQUE_DIR}/optic_core/core_cyan_emerald.png",
    f"{MACAQUE_DIR}/weapon/wpn_spring_claws.png",
]

comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for lyr in layers:
    im = Image.open(lyr).convert("RGBA")
    comp.alpha_composite(im)

proof_composite_path = f"{MACAQUE_DIR}/proof_paperdoll_macaque_composite.png"
comp.save(proof_composite_path)
print(f"✓ Saved updated {proof_composite_path}")
