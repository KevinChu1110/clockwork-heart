#!/usr/bin/env python3
from PIL import Image
import numpy as np

for race in ["rabbit", "fox", "lion"]:
    h_p = f"/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/{race}/maple_parts/head_unit"
    b_p = f"/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/{race}/maple_parts/body"
    print(f"=== {race} ===")
    import os
    if os.path.exists(h_p):
        for f in os.listdir(h_p):
            if f.endswith(".png"):
                im = Image.open(f"{h_p}/{f}").convert("RGBA")
                arr = np.array(im)
                cream = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 210) & (arr[:, :, 2] > 190) & (arr[:, :, 3] > 0)
                print(f"  Head {f}: size={im.size}, bbox={im.getbbox()}, cream={np.sum(cream)}")
                break
    if os.path.exists(b_p):
        for f in os.listdir(b_p):
            if f.endswith(".png"):
                im = Image.open(f"{b_p}/{f}").convert("RGBA")
                arr = np.array(im)
                cream = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 210) & (arr[:, :, 2] > 190) & (arr[:, :, 3] > 0)
                print(f"  Body {f}: size={im.size}, bbox={im.getbbox()}, cream={np.sum(cream)}")
                break
