from PIL import Image
import numpy as np

chassis = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/kangaroo/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
arr = np.array(chassis)
alpha = arr[:, :, 3]

print("Y-distribution of chassis pixels:")
for y in range(30, 128, 5):
    count = np.sum(alpha[y:y+5, :] > 20)
    xs = np.where(alpha[y:y+5, :] > 20)[1]
    min_x = xs.min() if len(xs) > 0 else -1
    max_x = xs.max() if len(xs) > 0 else -1
    print(f"  y={y:3d}..{y+4:3d}: count={count:4d}, x_range=[{min_x:2d}..{max_x:2d}]")

# Let's check leg regions specifically between y=90..120
print("\nLeg rows (y=90..120):")
for y in range(90, 120, 2):
    xs = np.where(alpha[y, :] > 20)[0]
    print(f"  y={y:3d}: xs={xs}")
