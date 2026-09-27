from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
wpn = Image.open(f"{BASE_DIR}/weapon/weapon_cat_shadowspring_stiletto.png").convert("RGBA")
bbox = wpn.getbbox()
print(f"Weapon full bbox: {bbox}")
wpn_crop = wpn.crop(bbox)
print(f"Weapon crop size: {wpn_crop.size}")

# Check center of mass / grip of weapon
arr = np.array(wpn)
alpha = arr[:, :, 3]
ys, xs = np.where(alpha > 20)
print(f"Weapon pixels x: {xs.min()}..{xs.max()}, y: {ys.min()}..{ys.max()}")
print(f"Weapon center: ({xs.mean():.1f}, {ys.mean():.1f})")

# Let's inspect cat composite body landmarks
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_cat_composite.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_cat_brass_acoustic_ears.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_cat_slit_optic_emerald.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/chassis_cat_obsidian_steel_default.png").convert("RGBA")
tail = Image.open(f"{BASE_DIR}/back_curio/curio_cat_segmented_gyro_tail.png").convert("RGBA")
key = Image.open(f"{BASE_DIR}/winding_key/key_cat_crescent_twin_ring_gold.png").convert("RGBA")
costume = Image.open(f"{BASE_DIR}/costume/costume_cat_skyspire_prowler_vest.png").convert("RGBA")

print("Head bbox:", head.getbbox())
print("Optic bbox:", optic.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Tail bbox:", tail.getbbox())
print("Key bbox:", key.getbbox())
print("Costume bbox:", costume.getbbox())
