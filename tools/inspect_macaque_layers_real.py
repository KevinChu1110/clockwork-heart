#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 看看 128x128 的各層疊加
slots = [
    ("winding_key", "key_classic_brass.png"),
    ("back_curio", "curio_spring_tail.png"),
    ("chassis", "paint_ivory_stock.png"),
    ("head_unit", "ear_macaque_coaxial.png"),
    ("costume", "costume_dawn_monk_tunic.png"),
    ("optic_core", "core_cyan_emerald.png"),
    ("weapon", "wpn_spring_claws.png"),
]

comp128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for slot, fn in slots:
    p = f"{MACAQUE_DIR}/{slot}/{fn}"
    layer = Image.open(p).convert("RGBA")
    comp128 = Image.alpha_composite(comp128, layer)

print("128 Composite complete.")
comp128.save("/tmp/macaque_test/real_128_comp.png")

# 檢查 512 的檔案
for slot, fn in slots:
    fn512 = fn.replace(".png", "_512.png")
    p512 = f"{MACAQUE_DIR}/{slot}/{fn512}"
    if os.path.exists(p512):
        im = Image.open(p512)
        print(f"Slot {slot} has 512: {im.size}, bbox={im.getbbox()}")
    else:
        print(f"Slot {slot} NO 512 version ({p512})")
