#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

shot_dir = "/opt/side/bravesoul-game/screenshots"
for fn in [
    "proof_battle_boar_full_screen.png",
    "proof_battle_boar_attack_full_screen.png",
    "proof_battle_boar_attack_hammer.png"
]:
    p = os.path.join(shot_dir, fn)
    sim = Image.open(p).convert("L")
    feet_crop = sim.crop((260, 420, 680, 620))
    farr = np.array(feet_crop)
    shadow_dark_px = int((farr < 70).sum())
    print(f"{fn}: feet shadow dark px = {shadow_dark_px}")
