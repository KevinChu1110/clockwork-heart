#!/usr/bin/env python3
from PIL import Image
import numpy as np

base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/raccoon"
optic = Image.open(f"{base}/optic_core/face_raccoon_hud_polarizer_visor.png")
arr = np.array(optic)

print("Optic shape:", arr.shape)
ys, xs = np.where(arr[:, :, 3] > 20)
print(f"Non-zero pixels: {len(xs)}, x: {xs.min()}..{xs.max()}, y: {ys.min()}..{ys.max()}")

# Unique colors
colors = set(tuple(arr[y, x]) for y, x in zip(ys, xs))
print(f"Unique colors count: {len(colors)}")
for c in sorted(colors, key=lambda c: -c[3])[:10]:
    print("  Color:", c)
