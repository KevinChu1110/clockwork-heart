import os
from PIL import Image

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

for p in POSES:
    path = os.path.join(POSES_DIR, f"{p}.png")
    im = Image.open(path).convert("RGBA")
    px = im.load()
    min_x, min_y, max_x, max_y = 128, 128, -1, -1
    for y in range(118):
        for x in range(128):
            if px[x, y][3] > 10:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
    h = max_y - min_y + 1 if max_y >= min_y else 0
    print(f"{p:10s}: top_y={min_y:2d}, bot_y={max_y:2d}, height={h:3d}, min_x={min_x:2d}, max_x={max_x:2d}")
