#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"
parts = [
    ("body", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png"),
    ("head", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png"),
    ("costume", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_harness.png"),
    ("weapon", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/weapon/wpn_anvil_greathammer.png"),
    ("key", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png"),
    ("tail", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/back_curio/curio_spring_tail.png"),
    ("eyes", f"{REPO}/game/assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_cyan_emerald.png"),
]

for name, path in parts:
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    # Check if there are pixels in upper-right or near bottom-right
    print(f"=== {name} ({im.size}) ===")
    # Save on white
    w_im = Image.new("RGBA", im.size, (255, 255, 255, 255))
    w_im.alpha_composite(im)
    w_im.save(f"/tmp/part_{name}.png")

print("Saved all parts on white")
