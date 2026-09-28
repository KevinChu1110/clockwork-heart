#!/usr/bin/env python3
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
idle = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/poses/courser/idle.png").convert("RGBA")
comp = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser/proof_paperdoll_courser_composite.png").convert("RGBA")

diff = ImageChops.difference(idle, comp)
bbox = diff.getbbox()
print(f"diff idle vs composite: bbox={bbox}")
if bbox:
    non_zero = sum(1 for y in range(128) for x in range(128) if cast(tuple[int, int, int, int], diff.getpixel((x, y)))[3] > 0)
    print(f"differing alpha pixels: {non_zero}")
