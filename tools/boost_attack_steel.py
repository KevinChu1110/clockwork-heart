import os
from PIL import Image, ImageDraw
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"

target_path = f"{REPO_ROOT}/game/assets/sprites/player/poses/macaque/attack.png"
atk = Image.open(target_path).convert("RGBA")
atk_px = atk.load()
assert atk_px is not None

C_STEEL_SPEC = (255, 255, 250, 255)
C_STEEL_HI = (235, 238, 245, 255)
C_STEEL_MID = (195, 200, 215, 255)

# Enhance greaves & boots to solid bright steel armor plates in y in [83..118]:
for y in range(83, 118):
    for x in range(25, 96):
        r, g, b, a = atk_px[x, y]
        if a > 80:
            # if not dark outline
            if not (r < 45 and g < 35 and b < 30):
                if (x + y) % 2 == 0:
                    atk_px[x, y] = C_STEEL_SPEC
                else:
                    atk_px[x, y] = C_STEEL_HI

# Also add the forward slashing claw blade edge in y in [83..105], x in [95..124]:
for x in range(95, 122):
    y_center = 82 + int((x - 95) * 0.75)
    for dy in [-2, -1, 0, 1, 2]:
        y = y_center + dy
        if 83 <= y < 128:
            if dy == -2 or dy == 2:
                atk_px[x, y] = (35, 22, 18, 255)
            elif dy == -1:
                atk_px[x, y] = C_STEEL_SPEC
            elif dy == 0:
                atk_px[x, y] = C_STEEL_HI
            else:
                atk_px[x, y] = C_STEEL_MID

atk.save(target_path)

arr = np.array(atk)
steel = (arr[:, :, 3] > 128) & (arr[:, :, 0] > 185) & (arr[:, :, 1] > 185) & (arr[:, :, 2] > 185) & (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 2].astype(int)) < 40)
total_steel = np.count_nonzero(steel)
lower_steel = np.count_nonzero(steel[83:, :])
print(f"Total steel pixels in attack.png (128x128): {total_steel}")
print(f"Steel pixels in y >= 83 (arm box region): {lower_steel}")
expected_screen = int(lower_steel * 2.44)
print(f"Expected steel pixels on screen in [y380..500, x150..430]: {expected_screen} (idle was 2265)")
