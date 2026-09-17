#!/usr/bin/env python3
import os
import shutil
from PIL import Image

BASE = "game/assets/sprites/player/paperdoll"

weapons = [
    ("lion", "wpn_knight_lance"),
    ("boar", "wpn_anvil_greathammer"),
    ("fox", "wpn_astral_staff"),
    ("macaque", "wpn_spring_claws"),
    ("tiger", "wpn_twin_ember_sabers"),
    ("crane", "wpn_zephyr_wing_bow"),
    ("bear", "wpn_eccentric_gyro_sledge"),
    ("penguin", "wpn_twin_harpoon_gun"),
]

for race, wpn in weapons:
    src = os.path.join(BASE, race, "weapon", f"{wpn}.png")
    dst_race = os.path.join(BASE, race, "weapon", f"{wpn}_512.png")
    dst_common = os.path.join(BASE, "weapon", f"{wpn}_512.png")

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source weapon {src} does not exist!")

    with Image.open(src) as img:
        rgba = img.convert("RGBA")
        resized = rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
        resized.save(dst_race, format="PNG")
        resized.save(dst_common, format="PNG")
        print(f"[{race}] Upscaled {wpn}.png ({rgba.size}) -> {dst_race} (512x512 RGBA) and {dst_common}")

# Ensure unique keys
keys_to_upscale = [
    ("bear/winding_key/key_cross_pendulum.png", "bear/winding_key/key_cross_pendulum_512.png"),
    ("crane/winding_key/key_tri_wing_zephyr.png", "crane/winding_key/key_tri_wing_zephyr_512.png"),
    ("penguin/winding_key/key_twin_ring_helm.png", "penguin/winding_key/key_twin_ring_helm_512.png"),
    ("tiger/winding_key/key_turbine_flame.png", "tiger/winding_key/key_turbine_flame_512.png"),
    ("key/key_cross_pendulum.png", "key/key_cross_pendulum_512.png"),
    ("key/key_tri_wing_zephyr.png", "key/key_tri_wing_zephyr_512.png"),
    ("key/key_twin_ring_helm.png", "key/key_twin_ring_helm_512.png"),
    ("key/key_turbine_flame.png", "key/key_turbine_flame_512.png"),
]

for rel_src, rel_dst in keys_to_upscale:
    src_path = os.path.join(BASE, rel_src)
    dst_path = os.path.join(BASE, rel_dst)
    if os.path.exists(src_path):
        with Image.open(src_path) as img:
            rgba = img.convert("RGBA")
            resized = rgba.resize((512, 512), resample=Image.Resampling.LANCZOS)
            resized.save(dst_path, format="PNG")
            print(f"[key] Upscaled {rel_src} -> {rel_dst} (512x512 RGBA)")

# key_classic_brass_512 copy to key/ and races using classic_brass
brass_src = os.path.join(BASE, "rabbit/winding_key/key_classic_brass_512.png")
brass_targets = [
    "key/key_classic_brass_512.png",
    "fox/winding_key/key_classic_brass_512.png",
    "lion/winding_key/key_classic_brass_512.png",
    "boar/winding_key/key_classic_brass_512.png",
    "macaque/winding_key/key_classic_brass_512.png",
]

for rel_t in brass_targets:
    target_path = os.path.join(BASE, rel_t)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copyfile(brass_src, target_path)
    print(f"[brass] Copied {brass_src} -> {target_path}")

print("All weapons and keys 512 generated successfully via LANCZOS.")
