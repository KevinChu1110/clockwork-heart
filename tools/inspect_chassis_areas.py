#!/usr/bin/env python3
from PIL import Image
import numpy as np

ch_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/chassis"
for name in ["paint_brass_gold_512.png", "paint_ivory_stock_512.png", "paint_molten_crimson_512.png"]:
    p = f"{ch_dir}/{name}"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    print(f"=== {name} ===")
    print("Non-zero alpha pixels:", np.sum(arr[:, :, 3] > 0))
    # Check pixels at x > 300, y < 200 (around key area)
    key_area_pixels = np.sum(arr[0:200, 300:512, 3] > 0)
    print(f"  Key area (y<200, x>300) non-zero alpha count: {key_area_pixels}")
    # Check pixels at x > 200, y > 460 (around hammer shadow area)
    bottom_right_pixels = np.sum(arr[460:512, 200:512, 3] > 0)
    print(f"  Bottom right (y>460, x>200) non-zero alpha count: {bottom_right_pixels}")
