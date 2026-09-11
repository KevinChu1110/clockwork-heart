import os
from PIL import Image

POSES_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/poses/fox"
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

def measure_eyes(im):
    px = im.load()
    assert px is not None
    # Glowing cyan eye pixels: high G, high B, low R
    eyes = []
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3] > 100:
                is_eye = (p[0] < 120 and p[1] > 180 and p[2] > 180)
                if is_eye:
                    eyes.append((x, y))
    return eyes

for p in POSES:
    path = os.path.join(POSES_DIR, f"{p}.png")
    im = Image.open(path).convert("RGBA")
    eyes = measure_eyes(im)
    print(f"{p:10s}: cyan eyes pixel count = {len(eyes)}")
