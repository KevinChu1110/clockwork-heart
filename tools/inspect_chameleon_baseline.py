from PIL import Image
import numpy as np

base_dir = "game/assets/sprites/player/paperdoll/chameleon"
comp = Image.open(f"{base_dir}/proof_paperdoll_chameleon_composite.png").convert("RGBA")
print("Composite size:", comp.size, "bbox:", comp.getbbox())

slices = {
    "chassis": "chassis/chassis_chameleon_mirage_titanium_default.png",
    "head_unit": "head_unit/head_chameleon_crested_visor_cowl.png",
    "winding_key": "winding_key/key_chameleon_prismatic_trivane.png",
    "costume": "costume/costume_chameleon_wasteland_scout_rig.png",
    "optic_core": "optic_core/face_chameleon_turret_rangefinder_lens.png",
    "weapon": "weapon/weapon_chameleon_mirage_compound_bow.png",
    "back_curio": "back_curio/curio_chameleon_spiral_torsion_tail.png"
}

for name, fname in slices.items():
    im = Image.open(f"{base_dir}/{fname}").convert("RGBA")
    print(f"{name:12s}: bbox={im.getbbox()}")

arr = np.array(comp)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Baseline shadow counts (118..127):", shadow_counts)

# Margins of composite
bbox = comp.getbbox()
print(f"Composite margins: left={bbox[0]}, top={bbox[1]}, right={128-bbox[2]}, bottom={128-bbox[3]}")
