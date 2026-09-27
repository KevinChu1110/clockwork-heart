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
    # Check top right quadrant: x: 70..120, y: 15..55
    sub = arr[15:55, 70:120]
    sub_alpha = sub[:, :, 3]
    sub_rgb = sub[:, :, :3]
    dark_mask = (sub_alpha > 50) & (sub_rgb[:, :, 0] < 45) & (sub_rgb[:, :, 1] < 45) & (sub_rgb[:, :, 2] < 65)
    cnt = np.sum(dark_mask)
    if cnt > 0:
        print(f"Slice {name:12s} has {cnt:4d} dark pixels in top right! bbox of dark pixels:")
        ys, xs = np.where(dark_mask)
        print(f"   x in [{xs.min()+70}, {xs.max()+70}], y in [{ys.min()+15}, {ys.max()+15}]")
        print("   unique dark RGB:", np.unique(sub_rgb[dark_mask], axis=0))
