import os
from PIL import Image
import numpy as np

base_dir = "game/assets/sprites/player/paperdoll/chameleon"

slices = {
    "back_curio": "back_curio/curio_chameleon_spiral_torsion_tail.png",
    "winding_key": "winding_key/key_chameleon_prismatic_trivane.png",
    "chassis": "chassis/chassis_chameleon_mirage_titanium_default.png",
    "costume": "costume/costume_chameleon_wasteland_scout_rig.png",
    "head_unit": "head_unit/head_chameleon_crested_visor_cowl.png",
    "optic_core": "optic_core/face_chameleon_turret_rangefinder_lens.png",
    "weapon": "weapon/weapon_chameleon_mirage_compound_bow.png",
}

imgs = {name: Image.open(os.path.join(base_dir, path)).convert("RGBA") for name, path in slices.items()}

for name, im in imgs.items():
    arr = np.array(im)
    bbox = im.getbbox()
    opaque_count = int(np.sum(arr[:, :, 3] > 8))
    print(f"{name:12s}: bbox={bbox}, opaque_pixels={opaque_count}")

# Check composite order in test_paperdoll_chameleon_skeleton.gd or build_chameleon_canonical_clean.py
with open("tools/build_chameleon_canonical_clean.py", "r") as f:
    text = f.read()

import re
m = re.search(r"alpha_composite.*", text)
print("\nComposite snippet from build_chameleon_canonical_clean.py:")
for line in text.splitlines():
    if "composite" in line.lower() or "curio" in line.lower() or "z_index" in line.lower():
        if "alpha_composite" in line or "order" in line.lower():
            print("  ", line)
