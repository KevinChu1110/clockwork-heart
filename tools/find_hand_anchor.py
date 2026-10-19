#!/usr/bin/env python3
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold_512.png").convert("RGBA")
weapon = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")

# 尋找 chassis 和 weapon 重疊的區域（即手握處）
c_arr = np.array(chassis)
w_arr = np.array(weapon)

overlap = (c_arr[:, :, 3] > 50) & (w_arr[:, :, 3] > 50)
ys, xs = np.where(overlap)

print(f"Overlap between Chassis and Weapon: count={len(ys)}")
if len(ys) > 0:
    print(f"X range: {xs.min()} .. {xs.max()}, Y range: {ys.min()} .. {ys.max()}")
    print(f"Overlap center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

# 觀察 weapon 的手柄 (Shaft)
# 戰錘在 512 的 bbox 是 (63, 270, 233, 509)
# 錘頭大約在底部或左側，柄在何處？
w_vis = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
w_vis.alpha_composite(weapon)
w_vis.alpha_composite(chassis)
w_vis.save("/tmp/boar_chassis_weapon.png")
