#!/usr/bin/env python3
"""
Verify alpha transparency and dimensions for game/assets/icons/hud/*.png.
"""
from PIL import Image
import numpy as np

def verify():
    targets = [
        ("icon_energy_key.png", (128, 128)),
        ("icon_gold_coin.png", (128, 128)),
        ("icon_gem_stardust.png", (128, 128)),
        ("icon_dock_village.png", (128, 128)),
        ("icon_dock_equip.png", (128, 128)),
        ("icon_dock_campaign.png", (128, 128)),
        ("icon_dock_soul.png", (128, 128)),
        ("icon_dock_bag.png", (128, 128))
    ]
    all_ok = True
    for name, expected_size in targets:
        path = f"/opt/side/bravesoul-game/game/assets/icons/hud/{name}"
        im = Image.open(path)
        arr = np.array(im)
        assert im.size == expected_size, f"{name} size mismatch: {im.size} vs {expected_size}"
        assert im.mode == "RGBA", f"{name} mode mismatch: {im.mode}"
        alpha = arr[:, :, 3]
        zero_alpha_cnt = (alpha == 0).sum()
        assert zero_alpha_cnt > 0, f"{name} has no transparent pixels!"
        print(f"PASS: {name} (size={im.size}, transparent_pixels={zero_alpha_cnt}/{alpha.size})")
    return all_ok

if __name__ == "__main__":
    verify()
