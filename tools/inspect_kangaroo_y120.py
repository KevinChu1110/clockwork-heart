from PIL import Image
import numpy as np

ch = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
arr = np.array(ch)
for y in range(120, 128):
    row = arr[y, :, :]
    opaque = np.where(row[:, 3] > 0)[0]
    if len(opaque) > 0:
        alphas = row[opaque, 3]
        rgbs = row[opaque, :3]
        print(f"y={y}: count={len(opaque)} x={opaque.min()}..{opaque.max()} alpha={alphas.min()}..{alphas.max()} sample_rgb={rgbs[0]}")
