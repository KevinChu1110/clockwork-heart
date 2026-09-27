from PIL import Image, ImageChops

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
body_master = Image.open(f"{BASE_DIR}/proof_paperdoll_cat_composite.png").convert("RGBA")

key_src = Image.open(f"{BASE_DIR}/winding_key/key_cat_crescent_twin_ring_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_cat_segmented_gyro_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_cat_obsidian_steel_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_cat_brass_acoustic_ears.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_cat_slit_optic_emerald.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_cat_skyspire_prowler_vest.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_cat_shadowspring_stiletto.png").convert("RGBA")

orders = [
    ("standard_1", [key_src, curio_src, chassis_src, head_src, optic_src, costume_src, weapon_src]),
    ("standard_2", [key_src, curio_src, chassis_src, costume_src, head_src, optic_src, weapon_src]),
    ("standard_3", [curio_src, key_src, chassis_src, head_src, optic_src, costume_src, weapon_src]),
]

for name, layers in orders:
    comp = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for l in layers:
        comp.alpha_composite(l)
    diff = ImageChops.difference(comp, body_master)
    print(f"Order {name}: diff={diff.getbbox()}")
