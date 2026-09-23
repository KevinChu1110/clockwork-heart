#!/usr/bin/env python3
from PIL import Image

for path in [
    "branding/char_tortoise.png",
    "branding/char_bear.png",
    "docs/art/char_tortoise_candidate_400x840.png",
    "docs/art/xuanji_tortoise_concept.png",
]:
    p = f"/opt/side/bravesoul-game/{path}"
    im = Image.open(p)
    print(f"{path:45s}: size={im.size} mode={im.mode}")
