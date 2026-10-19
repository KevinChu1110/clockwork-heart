#!/usr/bin/env python3
from PIL import Image
import numpy as np

lion_core = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/lion/optic_core/core_cyan_emerald_512.png").convert("RGBA")
arr = np.array(lion_core)

# 找青綠色高亮度像素：G > 140, B > 140, G > R + 20
mask = (arr[:, :, 1] > 140) & (arr[:, :, 2] > 140) & (arr[:, :, 1] > arr[:, :, 0] + 20) & (arr[:, :, 3] > 100)
ys, xs = np.where(mask)
print(f"Cyan pixels in lion core: count={len(ys)}")
print(f"X: {xs.min()}..{xs.max()}, Y: {ys.min()}..{ys.max()}")
print(f"Center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

# 裁切出真正的圓球
crop = lion_core.crop((xs.min()-4, ys.min()-4, xs.max()+4, ys.max()+4))
crop.save("/tmp/true_cyan_orb.png")
print("Saved /tmp/true_cyan_orb.png, size:", crop.size)
