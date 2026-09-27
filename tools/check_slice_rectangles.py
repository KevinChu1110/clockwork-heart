from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"
BASE = f"{REPO}/game/assets/sprites/player/paperdoll/owl"

slices = [
    ("chassis", "chassis/chassis_owl_brass_lamellae_default.png"),
    ("head_unit", "head_unit/head_owl_brass_plume_antennas.png"),
    ("winding_key", "winding_key/key_owl_sun_moon_astrolabe_gold.png"),
    ("costume", "costume/costume_owl_dawn_astronomer_robe.png"),
    ("optic_core", "optic_core/face_owl_clockface_lens_dusk_gold.png"),
    ("weapon", "weapon/weapon_owl_armillary_escapement_scepter.png"),
    ("back_curio", "back_curio/curio_owl_floating_micro_orrery.png")
]

for name, rel in slices:
    p = f"{BASE}/{rel}"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    # Check if there are dark pixels with alpha == 255 in a rectangle
    print(f"Slice {name}: size={im.size}, bbox={im.getbbox()}")
    # Check bounding box borders
    if im.getbbox():
        bb = im.getbbox()
        crop_alpha = alpha[bb[1]:bb[3], bb[0]:bb[2]]
        # fraction of opaque pixels in bbox
        opaque_frac = np.mean(crop_alpha > 200)
        print(f"  bbox shape: {bb[2]-bb[0]}x{bb[3]-bb[1]}, opaque fraction: {opaque_frac:.3f}")
