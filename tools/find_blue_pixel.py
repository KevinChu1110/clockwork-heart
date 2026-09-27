from PIL import Image
import numpy as np

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/poses/owl/idle.png").convert("RGBA")
arr = np.array(im)
for y in range(len(arr)):
    for x in range(len(arr[0])):
        if arr[y, x, 3] > 0 and arr[y, x, 0] <= 5 and arr[y, x, 1] <= 5 and arr[y, x, 2] >= 30:
            print(f"Pixel at ({x}, {y}): {arr[y, x]}")
