import os
from PIL import Image
import numpy as np

base_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo"

slices = [
    ("key", "winding_key/key_kangaroo_champion_double_ring.png"),
    ("curio", "back_curio/curio_kangaroo_steam_exhaust_backpack.png"),
    ("chassis", "chassis/chassis_kangaroo_caramel_bronze_default.png"),
    ("head", "head_unit/head_kangaroo_steampunk_boxer_visor.png"),
    ("costume", "costume/costume_kangaroo_champion_belt_harness.png"),
    ("optic", "optic_core/optic_kangaroo_amber_dial_core.png"),
    ("weapon", "weapon/weapon_kangaroo_piston_brass_knuckle.png"),
]

print("=== Slices BBox & Center ===")
for name, rel_path in slices:
    p = os.path.join(base_dir, rel_path)
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3]
    if bbox:
        ys, xs = np.where(alpha > 20)
        cx, cy = float(np.mean(xs)), float(np.mean(ys))
        print(f"{name:10s} bbox={bbox} center=({cx:.1f}, {cy:.1f})")

comp_path = os.path.join(base_dir, "proof_paperdoll_kangaroo_composite.png")
comp = Image.open(comp_path).convert("RGBA")
print(f"Composite bbox: {comp.getbbox()}")
