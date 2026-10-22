#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

# 載入 128 composite
im_comp_128 = Image.open(f"{MACAQUE_DIR}/proof_paperdoll_macaque_composite.png")
# 載入 512 composite
im_comp_512 = Image.open("/tmp/macaque_test/composite_512.png")

# 放大 128 到 512
im_comp_128_up = im_comp_128.resize((512, 512), Image.Resampling.NEAREST)
im_comp_128_up.save("/tmp/macaque_test/comp_128_up.png")

print("128 up saved.")
