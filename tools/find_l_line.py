#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PARTS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar/maple_parts"

slots = [
    ("weapon", f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png", (63, 270)),
    ("costume", f"{PARTS_DIR}/costume/costume_viking_harness.png", (180, 250)),
    ("body", f"{PARTS_DIR}/body/paint_brass_gold.png", (0, 0))
]

for name, path, offset in slots:
    im = Image.open(path).convert("RGBA")
    # 建立 512 畫布
    can = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    can.alpha_composite(im, offset)
    
    # 裁出 (140, 260, 240, 420)
    sub = can.crop((140, 260, 240, 420))
    arr = np.array(sub)
    print(f"Slot {name:10}: non-zero alpha in zoom = {np.sum(arr[:, :, 3] > 0)}, bbox={sub.getbbox()}")
    sub.save(f"/tmp/zoom_layer_{name}.png")
