#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

k128 = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass.png")
k512 = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass_512.png")

print("k128 size:", k128.size, "bbox:", k128.getbbox())
print("k512 size:", k512.size, "bbox:", k512.getbbox())

# 看看獅子、兔子的 key_classic_brass 512
for r in ["rabbit", "fox", "lion"]:
    p = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{r}/maple_parts/winding_key/key_classic_brass.png"
    im = Image.open(p)
    print(f"{r} maple key size:", im.size, "bbox:", im.getbbox())
